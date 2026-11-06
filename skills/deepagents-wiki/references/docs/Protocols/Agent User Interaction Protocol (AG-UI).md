# Agent User Interaction Protocol (AG-UI)

> Expose deep agents over the Agent User Interaction Protocol (AG-UI) to stream events to any AG-UI client or frontend.

[Agent User Interaction Protocol (AG-UI)](https://docs.ag-ui.com) is an open, lightweight, event-based protocol that standardizes how AI agents connect to user-facing applications.
Exposing a deep agent over AG-UI turns its run into a typed event stream (messages, tool calls, reasoning, state, and lifecycle) that any AG-UI client can consume, so you can drive a frontend without coupling it to LangGraph internals.

> [!NOTE]
>
> AG-UI is designed for agent-to-user interaction: the connection between an agentic backend and a user-facing frontend. It is distinct from the other Deep Agents protocols:
>
> * **AG-UI** connects a deep agent to a frontend application (this page).
> * [Agent Client Protocol (ACP)](Agent%20Client%20Protocol%20%28ACP%29.md) connects a deep agent to code editors and IDEs.
> * [Model Context Protocol (MCP)](Model%20Context%20Protocol%20%28MCP%29.md) lets a deep agent call tools hosted by external servers.
> * [Agent2Agent (A2A)](A2A%20endpoint%20in%20Agent%20Server.md) connects a deep agent to other agents.

## Quickstart

Serve a deep agent as a LangGraph graph, then connect the TypeScript `@ag-ui/langgraph` adapter so AG-UI clients can drive it.

### Install dependencies

Install Deep Agents and the LangGraph CLI to serve the graph. The AG-UI adapter used in later steps is TypeScript (`@ag-ui/langgraph`). For a Python CopilotKit or AG-UI FastAPI bridge, see [CopilotKit](https://docs.langchain.com/oss/python/langchain/frontend/integrations/copilotkit.md).

```bash pip theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
pip install deepagents "langgraph-cli[inmem]"
```

```bash uv theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
uv add deepagents "langgraph-cli[inmem]"
```

A deep agent created with `createDeepAgent` (`create_deep_agent` in Python) is a LangGraph graph. Expose it to AG-UI clients by serving it as a LangGraph server, then point the AG-UI adapter at that server.

### Create a deep agent

Define the agent and export the graph so a LangGraph server can load it.

```python icon="robot" title="agent.py" theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent

agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",
    system_prompt="You are an expert researcher.",
)
```

### Serve the agent

Register the graph in a `langgraph.json` file at your project root.

```json icon="file-code" title="langgraph.json" theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
{
  "dependencies": ["."],
  "graphs": {
    "deep_agent": "./agent.py:agent"
  },
  "env": ".env"
}
```

Start the LangGraph development server. It exposes the graph over HTTP at `http://localhost:2024`.

```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
langgraph dev
```

### Connect the AG-UI adapter

The TypeScript `@ag-ui/langgraph` adapter wraps the running graph as an AG-UI agent that any client can drive. Point it at the LangGraph server and name the graph to load. This works whether the graph was authored in Python or TypeScript.

```ts icon="plug" title="ag-ui agent" theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
import { LangGraphAgent } from "@ag-ui/langgraph";

const agent = new LangGraphAgent({
  graphId: "deep_agent",
  deploymentUrl: "http://localhost:2024",
});
```

> [card] [AG-UI LangGraph adapter on npm](https://www.npmjs.com/package/@ag-ui/langgraph)
>
> The `@ag-ui/langgraph` package implements the AG-UI protocol for LangGraph graphs, including deep agents.

## Stream events

AG-UI is an event stream. As a deep agent runs, the adapter translates its LangGraph execution into typed AG-UI events. A client subscribes to those events and updates as they arrive, rather than waiting for the final answer.

A deep agent run maps onto many AG-UI event types. The main ones, among others:

| Deep agent activity | AG-UI events |
| - | - |
| Run lifecycle | `RUN_STARTED`, `RUN_FINISHED`, `RUN_ERROR` |
| Graph node progress | `STEP_STARTED`, `STEP_FINISHED` |
| Assistant text | `TEXT_MESSAGE_START`, `TEXT_MESSAGE_CONTENT`, `TEXT_MESSAGE_END` |
| Tool calls | `TOOL_CALL_START`, `TOOL_CALL_ARGS`, `TOOL_CALL_END`, `TOOL_CALL_RESULT` |
| Reasoning | `REASONING_START`, `REASONING_MESSAGE_CONTENT`, `REASONING_END` |
| Shared state (todos, subagents, custom keys) | `STATE_SNAPSHOT`, `STATE_DELTA` |
| Conversation history | `MESSAGES_SNAPSHOT` |

State updates use `STATE_SNAPSHOT` for a full baseline and `STATE_DELTA` (JSON Patch, RFC 6902) for incremental changes, so a client can keep todos, plans, and subagent status in sync without re-sending the whole state on every step.

To watch the stream directly, run the agent with a subscriber. Each event has a matching `on…Event` callback:

```ts icon="activity" title="observe.ts" theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
import { LangGraphAgent } from "@ag-ui/langgraph";

const agent = new LangGraphAgent({
  graphId: "deep_agent",
  deploymentUrl: "http://localhost:2024",
  initialMessages: [
    { id: "1", role: "user", content: "Research the AG-UI protocol." },
  ],
});

await agent.runAgent(
  {},
  {
    onTextMessageContentEvent({ event }) {
      process.stdout.write(event.delta);
    },
    onToolCallStartEvent({ event }) {
      console.log(`\n[tool] ${event.toolCallName}`);
    },
    onStateSnapshotEvent({ event }) {
      console.log("\n[state]", event.snapshot);
    },
    onRunFinishedEvent() {
      console.log("\n[done]");
    },
  },
);
```

When a deep agent pauses for human input, the run finishes with an interrupt. By default, `@ag-ui/langgraph` emits a legacy `on_interrupt` custom event alongside `RUN_FINISHED`. To receive the structured AG-UI interrupt outcome on `RUN_FINISHED` (`outcome.type === "interrupt"`), set `emitInterruptOutcome: true` when you construct the agent:

```ts icon="hand-stop" theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
const agent = new LangGraphAgent({
  graphId: "deep_agent",
  deploymentUrl: "http://localhost:2024",
  emitInterruptOutcome: true,
});
```

Resume the run by sending the standard AG-UI `resume` field on the next input:

```ts icon="hand-stop" theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
const input = {
  threadId: "t1",
  runId: "r2",
  messages: [],
  resume: [
    { interruptId: "int-abc", status: "resolved", payload: { approved: true } },
  ],
};
```

For the interrupt model itself, see [Human-in-the-loop](../Steering/Human-in-the-loop.md).

> [!NOTE]
>
> For the complete event schema, see the [AG-UI events reference](https://docs.ag-ui.com/concepts/events).

## Connect a frontend

Any AG-UI client can drive a deep agent exposed over the protocol, so you do not have to build message rendering, streaming, or state sync yourself. Point the client at the adapter (or a runtime that wraps it) and select the agent by its `graphId`.

> [card] [CopilotKit](https://docs.langchain.com/oss/python/langchain/frontend/integrations/copilotkit.md)
>
> React chat runtime with AG-UI support for LangGraph and Deep Agents, including the Python FastAPI bridge.

> [card] [AG-UI clients](https://docs.ag-ui.com/integrations)
>
> The full list of AG-UI clients and SDKs, including terminal and mobile clients.

> [card] [Build a custom client](https://docs.ag-ui.com/quickstart/clients)
>
> Consume the event stream directly with the AG-UI SDK to build your own interface.

## Programmatic API

`LangGraphAgent` connects to a deep agent on a LangGraph server and exposes it as an AG-UI agent. Construct it with the graph to load, then drive it with a few methods.

```ts icon="plug" theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
import { LangGraphAgent } from "@ag-ui/langgraph";

const agent = new LangGraphAgent({
  graphId: "deep_agent",              // matches a key in langgraph.json
  deploymentUrl: "http://localhost:2024",
});
```

* **`runAgent(parameters?, subscriber?)`**: Run the agent and stream AG-UI events to the subscriber's `on…Event` callbacks (see [Stream events](#stream-events)). Resolves when the run finishes.
* **`subscribe(subscriber)`**: Attach a persistent subscriber that receives events across every run, rather than for a single call.
* **`abortRun()`**: Cancel the run in progress.

To seed input, pass `initialMessages` to the constructor, or call `addMessage` or `setMessages` before running.

## See also

* [CopilotKit](https://docs.langchain.com/oss/python/langchain/frontend/integrations/copilotkit.md): Python and TypeScript CopilotKit runtime patterns for Deep Agents over AG-UI
* [Frontend overview](../Frontend/Overview.md): Build UIs that stream deep agent progress with the LangChain frontend SDKs
* [Human-in-the-loop](../Steering/Human-in-the-loop.md): Interrupt and resume model for deep agents
* [Agent Client Protocol (ACP)](Agent%20Client%20Protocol%20%28ACP%29.md): Connect deep agents to code editors and IDEs
* [AG-UI documentation](https://docs.ag-ui.com): Protocol concepts, events, and client SDKs

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/deepagents/ag-ui.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

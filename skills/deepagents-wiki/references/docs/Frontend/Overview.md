# Overview

> Build UIs that display real-time subagent streams, task progress, and sandbox for Deep Agents

Build frontends that visualize deep agent workflows in real time. These patterns
show how to render subagent progress, task planning, streaming content, and
IDE-like sandbox experiences from agents created with `createDeepAgent`.

Deep agents are most useful when the UI makes delegation visible. Instead of
showing a single opaque assistant bubble, the LangChain SDKs expose the
coordinator, subagent discovery, custom state, and sandbox-backed artifacts so
users can inspect how a long-running task is being decomposed and completed.

> [!NOTE]
>
> These patterns use the v1 frontend SDK packages. If you are using earlier versions, see the migration guides for [React](https://github.com/langchain-ai/langgraphjs/blob/main/libs/sdk-react/docs/v1-migration.md), [Vue](https://github.com/langchain-ai/langgraphjs/blob/main/libs/sdk-vue/docs/v1-migration.md), [Svelte](https://github.com/langchain-ai/langgraphjs/blob/main/libs/sdk-svelte/docs/v1-migration.md), and [Angular](https://github.com/langchain-ai/langgraphjs/blob/main/libs/sdk-angular/docs/v1-migration.md).

## Architecture

Deep Agents use a coordinator-worker architecture. The main agent plans tasks and delegates to specialized subagents, each running in isolation. On the frontend, the v1 stream handle surfaces coordinator messages on the root stream and exposes subagent discovery snapshots for scoped subagent views.

```mermaid theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
%%{
  init: {
    "fontFamily": "monospace",
    "flowchart": {
      "curve": "curve"
    }
  }
}%%
graph LR
  FRONTEND["useStream()"]
  SELECTORS["selector helpers"]
  BACKEND["createDeepAgent()"]
  SUB1["Subagent A"]
  SUB2["Subagent B"]

  BACKEND --"stream"--> FRONTEND
  FRONTEND --"scope by subagent"--> SELECTORS
  SELECTORS --> SUB1
  SELECTORS --> SUB2
  FRONTEND --"submit"--> BACKEND
  BACKEND --"delegate"--> SUB1
  BACKEND --"delegate"--> SUB2
  SUB1 --"result"--> BACKEND
  SUB2 --"result"--> BACKEND

  classDef blueHighlight fill:#E5F4FF,stroke:#006DDD,color:#030710;
  classDef greenHighlight fill:#F6FFDB,stroke:#6E8900,color:#2E3900;
  classDef purpleHighlight fill:#EBD0F0,stroke:#885270,color:#441E33;
  class FRONTEND,SELECTORS blueHighlight;
  class BACKEND greenHighlight;
  class SUB1,SUB2 purpleHighlight;
```

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent

agent = create_deep_agent(
    model="google_genai:gemini-3.6-flash",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
    subagents=[
        {
            "name": "researcher",
            "description": "Research assistant",
            "system_prompt": "You are a research assistant.",
        }
    ],
)
```

On the frontend, connect with [`useStream`](https://reference.langchain.com/javascript/langchain-react/index/useStream) the same way as with `createAgent`. Pass a [type parameter](https://docs.langchain.com/oss/python/langchain/frontend/overview.md) for type-safe stream state. Deep agent patterns use `stream.subagents`, selector helpers such as `useMessages(stream, subagent)`, and custom state values like `stream.values.todos` to render subagent-specific UIs.

```ts theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
import { useStream } from "@langchain/react";

function App() {
  const stream = useStream<typeof agent>({
    apiUrl: "http://localhost:2024",
    assistantId: "agent",
  });

  // Deep agent state beyond messages
  const todos = stream.values?.todos;
  const subagents = [...stream.subagents.values()];
}
```

## What the SDK exposes

Deep agent UIs usually need more than the final answer. The frontend SDK gives
you structured projections for the parts of the run users care about:

| Projection | Use it for |
| - | - |
| `stream.messages` | The coordinator conversation and final synthesis. |
| `stream.subagents` | Live discovery of specialist workers, including status and task metadata. |
| `stream.values` | Shared state such as todos, plans, report sections, sandbox metadata, or any custom key your agent writes. |
| Tool-call state | Rendering filesystem, search, browser, or domain tools as cards with progress and results. |
| Interrupts | Pausing delegated work for user approval or missing input without losing the run state. |

This lets you build interfaces that feel closer to an IDE, task board, or
workflow monitor than a plain chat transcript.

## Patterns

> [card] [Subagent streaming](Patterns/Subagent%20streaming.md)
>
> Display specialist subagents with streaming content, progress tracking, and collapsible cards.

> [card] [Todo list](Patterns/Todo%20list.md)
>
> Track progress with a real-time todo list when the agent opts into task planning.

> [card] [Sandbox](Patterns/Sandbox.md)
>
> Build an IDE-like UI with a file browser, code viewer, and diff panel backed by a sandbox.

## Related patterns

The [LangChain frontend patterns](https://docs.langchain.com/oss/python/langchain/frontend/overview.md), including
markdown messages, tool calling, and human-in-the-loop, all work with deep
agents too. Deep Agents are built on the same LangGraph runtime, so
`useStream` provides the same core API.

For lower-level graph visualizations, see the
[LangGraph frontend patterns](https://docs.langchain.com/oss/python/langgraph/frontend/overview.md). They show how
to map graph nodes and state keys directly to UI components.

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/deepagents/frontend/overview.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

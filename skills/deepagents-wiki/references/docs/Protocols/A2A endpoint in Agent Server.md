# A2A endpoint in Agent Server

> Use the A2A protocol to enable agent-to-agent communication with distributed tracing in LangSmith.

[Agent2Agent (A2A)](https://a2a-protocol.org/latest/) is Google's protocol for enabling communication between conversational AI agents. [LangSmith implements A2A support](https://docs.langchain.com/langsmith/server-api-ref.md#tag/a2a/post/a2a/\{assistant_id}), allowing your agents to communicate with other A2A-compatible agents through a standardized protocol.

The A2A endpoint is available in [Agent Server](https://docs.langchain.com/langsmith/agent-server.md) at `/a2a/{assistant_id}`.

## Protocol version

Agent Server speaks the A2A **v1.0** JSON-RPC binding and also accepts the v0.3 method names, so
existing v0.3 clients keep working. The agent card declares one interface:

```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
"supportedInterfaces": [
  {
    "url": "https://your-deployment/a2a/{assistant_id}",
    "protocolBinding": "JSONRPC",
    "protocolVersion": "1.0"
  }
]
```

> [!WARNING]
>
> The method name you send also selects the enum case in the response. A v1.0 name returns
> SCREAMING\_SNAKE\_CASE (`TASK_STATE_WORKING`, `ROLE_AGENT`); a v0.3 name returns lowercase
> (`working`, `agent`). Pick one family per client and stay on it.
>
> The envelope varies by method, not by family: `SendMessage` wraps the task in `result.task`, while
> `GetTask` and all v0.3 methods return it directly on `result`. `ListTasks` returns `result.tasks`.

## Supported methods

| v1.0 name | v0.3 name | Supported |
| - | - | - |
| `SendMessage` | `message/send` | Yes, blocking by default. See [Return before the run finishes](#return-before-the-run-finishes) |
| `SendStreamingMessage` | `message/stream` | Yes — Server-Sent Events |
| `GetTask` | `tasks/get` | Yes |
| `CancelTask` | `tasks/cancel` | Yes |
| `ListTasks` | — | Yes |
| `GetExtendedAgentCard` | — | Yes, under the v1.0 name only |
| `SubscribeToTask` | — | Not yet — returns `-32601` |
| `*TaskPushNotificationConfig` | — | Not yet — returns `-32601` |

Exactly four v0.3 names are accepted: `message/send`, `message/stream`, `tasks/get` and
`tasks/cancel`. Anything else — including `agent/getAuthenticatedExtendedCard` and
`tasks/resubscribe` — returns `-32601 Method not found`.

Only the JSON-RPC binding is available. gRPC and HTTP+JSON are not implemented.

### Return before the run finishes

By default, `SendMessage` holds the request open until the run finishes. To get the task back as
soon as the run is created, set `returnImmediately` to `true` in `configuration`:

```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
{
  "jsonrpc": "2.0",
  "id": "1",
  "method": "SendMessage",
  "params": {
    "message": {
      "role": "ROLE_USER",
      "parts": [{"text": "hello"}],
      "messageId": "message-1"
    },
    "configuration": {"returnImmediately": true}
  }
}
```

The response is a task in `TASK_STATE_SUBMITTED` or `TASK_STATE_WORKING`, with no artifacts. Poll
`GetTask` with the returned `id` until the state is terminal or `TASK_STATE_INPUT_REQUIRED`. A
completed task carries the agent's reply in `artifacts`, the same parts a blocking `SendMessage`
returns.

* **`returnImmediately`**: The v1.0 flag. Takes precedence when both flags are sent.
* **`blocking`**: The v0.3 flag. `"blocking": false` behaves like `"returnImmediately": true`.

Each flag must be a boolean or `null`, and `null` counts as unset. Any other value returns `-32602`
before a run is created.

### Task history in responses

A context holds many tasks. By default `SendMessage`, `GetTask` and `ListTasks` return the history
of the **whole context**, not just the task you asked about. The second task in a context replays
the first task's messages, so a client that renders every history entry shows earlier turns again —
including earlier tool results and A2UI payloads.

Set `historyScope` to `task` to get back only the messages that belong to the task you asked about.
The default stays `context`, so existing integrations are unaffected.

Where the option goes depends on the method. `SendMessage` reads it from `configuration`:

```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
{
  "jsonrpc": "2.0",
  "id": "1",
  "method": "SendMessage",
  "params": {
    "message": {
      "role": "ROLE_USER",
      "parts": [{"text": "Second request"}],
      "messageId": "message-2",
      "contextId": "8b1f0e5c-9a3d-4f27-b0c8-2e6a5d4c1b7a"
    },
    "configuration": {"historyScope": "task"}
  }
}
```

`GetTask` and `ListTasks` read it directly from `params`:

```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
{"jsonrpc": "2.0", "id": "2", "method": "GetTask",
 "params": {"id": "<taskId>", "historyScope": "task"}}
```

If your client cannot add fields to the request body, send the header instead. An explicit value in
the request wins over the header.

```
LangGraph-A2A-History-Scope: task
```

The agent card advertises this under `capabilities.extensions`, so you can detect support rather
than assume it:

```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
{
  "uri": "https://langchain.com/a2a/extensions/history-scope/v1",
  "description": "Choose task-only or full-context response history",
  "required": false,
  "params": {
    "header": "LangGraph-A2A-History-Scope",
    "values": ["context", "task"],
    "default": "context",
    "methods": ["SendMessage", "GetTask", "ListTasks"]
  }
}
```

Three limits worth knowing:

* Streaming ignores both history options. `SendStreamingMessage` reads neither `historyScope` nor `historyLength`, and returns no error if you send them — so do not rely on either over SSE.
* `historyLength` caps at 10. A larger value returns `-32602` with `historyLength cannot exceed 10`.
* Scope is applied before `historyLength`, so you get the last N messages *of that task*.

An unrecognized value returns `-32602` with `historyScope must be 'context' or 'task'`. A mis-cased
key such as `historyscope` is not an error — it is ignored, and you silently get full-context
history, so check the spelling if filtering appears not to work.

> [!WARNING]
>
> Do not resend a `taskId` from a completed task. Each new turn starts a new task inside the same
> context — send the `contextId` alone. A message naming a terminal task is rejected with `-32004`,
> and a `taskId` minted by another agent is rejected with `-32001`.

### Interrupts

When the graph calls `interrupt()`, the task moves to `TASK_STATE_INPUT_REQUIRED` and carries an
artifact named `Interrupt`. The artifact holds one `DataPart` per pending interrupt:

```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
{
  "name": "Interrupt",
  "description": "Agent requires input to continue",
  "parts": [
    {
      "kind": "data",
      "data": {
        "id": "<interruptId>",
        "value": "<value passed to interrupt()>",
        "response_schema": "<JSON Schema for the resume value>"
      }
    }
  ]
}
```

`response_schema` appears only when the graph passes one to `interrupt()`.

To resume, send a message with the interrupted task's `taskId` and `contextId`. Put the resume
value in a `DataPart` under a `resume` key, such as `{"data": {"resume": true}}`, or send a text
part, which is used as the resume value as is. Send at most one `resume` `DataPart`. More than one
returns `-32602`.

If the task is not waiting on input, a `resume` `DataPart` returns `-32602`, but a text part is
treated as an ordinary message rather than a resume value.

## Agent card discovery

Each assistant automatically exposes an A2A Agent Card that describes its capabilities and provides the information needed for other agents to connect. You can retrieve the agent card for any assistant using:

```
GET /.well-known/agent-card.json?assistant_id={assistant_id}
```

The agent card includes the assistant's name, description, available skills, supported input/output modes, and the A2A endpoint URL for communication.

To serve a card when the request omits `assistant_id`, set the [`DEFAULT_A2A_ASSISTANT_ID`](https://docs.langchain.com/langsmith/env-var-self-hosted) environment variable. If the agent card URLs show an internal host, set `LANGGRAPH_API_URL` to your deployment's public URL.

## Optional capabilities

These are configured per assistant through `metadata.a2a` on the Assistants API. `langgraph.json`
cannot set assistant metadata, so patch the assistant after deploy.

### Declare input and output modes

```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
{
  "metadata": {
    "a2a": {
      "input_modes": ["text/plain", "application/pdf"],
      "output_modes": ["text/plain", "application/pdf"]
    }
  }
}
```

The values feed both the card's `defaultInputModes`/`defaultOutputModes` and the generated skill's
modes. They are advertisement only — an undeclared mode is still accepted. Replacement is per
field, so send both if you want both overridden, and note that an empty list is rejected.

### File parts

`FilePart` works in both directions. Inbound file, image, audio and video parts become LangChain
content blocks. Outbound content blocks map back to `FilePart`, in task history and in the final
streamed artifact. MIME types, URIs and filenames pass through unchanged; inline data is
re-encoded as standard base64.

### A2UI v0.9

A2UI is off by default. Turn it on for every assistant in a deployment with an environment
variable:

```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
A2A_A2UI_ENABLED=true
```

Or opt in per assistant:

```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
{ "metadata": { "a2a": { "a2ui": true } } }
```

The per-assistant `a2ui` value wins over `A2A_A2UI_ENABLED`, so you can also turn A2UI off for one
assistant in an enabled deployment. Each run records the setting it started with, so `GetTask` and
`ListTasks` render an existing task the same way after you change it.

When A2UI is enabled, the card advertises the extension and appends the canonical MIME type to both mode lists:

```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
"capabilities": {
  "extensions": [
    {
      "uri": "https://a2ui.org/a2a-extension/a2ui/v0.9",
      "description": "Ability to render A2UI v0.9",
      "required": false,
      "params": {
        "v0.9": {
          "supportedCatalogIds": [],
          "acceptsInlineCatalogs": false
        }
      }
    }
  ]
}
```

A client activates the extension per request by sending its URI in the `A2A-Extensions` header.
The legacy `X-A2A-Extensions` header also works:

```txt theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
A2A-Extensions: https://a2ui.org/a2a-extension/a2ui/v0.9
```

The server reads A2UI client capabilities and the client data model from `params.message.metadata`
(`a2uiClientCapabilities` and `a2uiClientDataModel`), the location the A2UI v0.9 schema defines.
Capabilities use the tagged shape, such as `{"v0.9": {"supportedCatalogIds": [...]}}`. A flat
capabilities object is rejected.

An A2UI `DataPart` holds either one A2UI message object or an array of messages, with
`metadata.mimeType` set to an A2UI MIME type:

* **`application/json+a2ui`**: The canonical type. The card advertises it, and responses use it by
  default.
* **`application/a2ui+json`**: Accepted on input. When a request uses it, responses for that task
  echo it back, including later `GetTask` reads.

Payloads are validated in both directions against the v0.9 schemas. An invalid payload from the
client returns `-32602`. An invalid payload in the agent's reply fails the request with `-32603`.
A2UI parts are preserved in `SendMessage`, `GetTask`, and the final `SendStreamingMessage` artifact.

The server publishes A2UI output only when the assistant has A2UI enabled and the client sent the
extension header. Otherwise, it drops A2UI blocks from the agent's output and returns the rest of
the reply, rather than failing the request.

Client input is stricter. An A2UI `DataPart` sent to an assistant without A2UI enabled, or sent
without the extension header, returns `-32602`.

To publish a tool's result as A2UI, list the tool names on the deployment. The tool's result must
be A2UI JSON:

```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
A2A_A2UI_TOOL_CALL_RESULTS=generative_ui_tool,another_tool
```

Listed tool results are sent as A2UI `DataPart`s only when A2UI is active for the request. Error
results and results that fail validation are dropped.

### Filter tool results

By default every correlated tool result is published as a `DataPart`. To publish only some, set an
allowlist of tool names on the deployment:

```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
A2A_ALLOWED_TOOL_CALL_RESULTS=generative_ui_tool,another_tool
```

Unset means all tool results are published. The filter applies to both task history and streaming.

## Requirements

| Feature | Minimum version |
| - | - |
| A2A endpoint | `langgraph-api >= 0.4.21` |
| Inbound `FilePart` | `0.12.0` |
| Tool-result `DataPart`s | `0.12.2` |
| `A2A_ALLOWED_TOOL_CALL_RESULTS` | `0.12.4` |
| Outbound `FilePart`, configurable card modes | `0.13.0` |
| A2UI v0.9, `A2A_A2UI_ENABLED`, `A2A_A2UI_TOOL_CALL_RESULTS` | `0.15.0` |
| `historyScope` | `0.15.0` |
| `response_schema` in interrupt artifacts | `0.16.0` |
| `returnImmediately` and `blocking` on `SendMessage` | `0.18.0` |

```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
pip install "langgraph-api>=0.16.0"
```

Your graph's state must include a `messages` key to accept A2A text and file parts. An assistant
whose input schema has no `messages` field is rejected with an explanatory error.

## Create an A2A-compatible agent

This example creates an A2A-compatible agent that processes incoming messages using OpenAI's API and maintains conversational state. The agent defines a message-based state structure and handles the A2A protocol's message format.

To be compatible with the [A2A "text" parts](https://a2a-protocol.org/dev/specification/#651-textpart-object), the agent must have a `messages` key in state.

The A2A protocol uses two identifiers to maintain conversational continuity:

* `contextId`: Groups messages into a conversation thread (like a session ID)
* `taskId`: Identifies each individual request within that conversation

On the first message, omit both - the agent generates and returns them. For all subsequent messages in the conversation, send back the `contextId` from the prior response and omit `taskId`, so each turn opens a new task inside the same conversation. Send a `taskId` only to add to a task that is still running, such as one waiting on input.

**LangSmith Tracing:** The Langsmith Deployment A2A endpoint automatically converts the A2A `contextId` to `thread_id` for LangSmith tracing, grouping all messages in the conversation under a single thread.

For example:

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
"""LangGraph A2A conversational agent.

Supports the A2A protocol with messages input for conversational interactions.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, List, TypedDict

from langgraph.graph import StateGraph
from langgraph.runtime import Runtime
from openai import AsyncOpenAI


class Context(TypedDict):
    """Context parameters for the agent."""
    my_configurable_param: str


@dataclass
class State:
    """Input state for the agent.

    Defines the initial structure for A2A conversational messages.
    """
    messages: List[Dict[str, Any]]


async def call_model(state: State, runtime: Runtime[Context]) -> Dict[str, Any]:
    """Process conversational messages and returns output using OpenAI."""
    # Initialize OpenAI client
    client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Process the incoming messages
    latest_message = state.messages[-1] if state.messages else {}
    user_content = latest_message.get("content", "No message content")

    # Create messages for OpenAI API
    openai_messages = [
        {
            "role": "system",
            "content": "You are a helpful conversational agent. Keep responses brief and engaging."
        },
        {
            "role": "user",
            "content": user_content
        }
    ]

    try:
        # Make OpenAI API call
        response = await client.chat.completions.create(
            model="gpt-5.4-mini",
            messages=openai_messages,
            max_tokens=100,
            temperature=0.7
        )

        ai_response = response.choices[0].message.content

    except Exception as e:
        ai_response = f"I received your message but had trouble processing it. Error: {str(e)[:50]}..."

    # Create a response message
    response_message = {
        "role": "assistant",
        "content": ai_response
    }

    return {
        "messages": state.messages + [response_message]
    }


# Define the graph
graph = (
    StateGraph(State, context_schema=Context)
    .add_node(call_model)
    .add_edge("__start__", "call_model")
    .compile()
)
```

## Agent-to-agent communication

Once your agents are running locally via `langgraph dev` or [deployed to production](https://docs.langchain.com/langsmith/deployment.md), you can facilitate communication between them using the A2A protocol.

This example demonstrates how two agents can communicate by sending JSON-RPC messages to each other's A2A endpoints. The script simulates a multi-turn conversation where each agent processes the other's response and continues the dialogue.

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
#!/usr/bin/env python3
"""Agent-to-Agent conversation simulation using the LangGraph A2A endpoint."""

import asyncio
import aiohttp
import os
from langsmith import uuid7
def extract_text(result: dict) -> str:
    """Best-effort extraction of response text from an A2A result."""
    if "error" in result:
        raise RuntimeError(f"A2A error {result['error']['code']}: {result['error']['message']}")

    for art in result.get("result", {}).get("artifacts", []) or []:
        for part in art.get("parts", []) or []:
            if part.get("kind") == "text" and part.get("text"):
                return part["text"]

    msg = (result.get("result", {}).get("status", {}) or {}).get("message", {}) or {}
    for part in msg.get("parts", []) or []:
        if part.get("kind") == "text" and part.get("text"):
            return part["text"]

    return "(no text found)"


async def send_message(session, port, assistant_id, text, context_id=None):
    """Send an A2A message. Returns (response_text, returned_context_id)."""
    url = f"http://127.0.0.1:{port}/a2a/{assistant_id}"

    message = {
        "role": "user",
        "parts": [{"kind": "text", "text": text}],
        "messageId": str(uuid7()),
    }

    # A2A multi-turn continuity: reuse contextId across turns and agents.
    # Do not reuse taskId — each turn starts a new task within the same context.
    if context_id:
        message["contextId"] = context_id

    payload = {
        "jsonrpc": "2.0",
        "id": str(uuid7()),
        "method": "message/send",
        "params": {"message": message},
    }

    headers = {"Accept": "application/json"}
    async with session.post(url, json=payload, headers=headers) as response:
        result = await response.json()

    text = extract_text(result)
    returned_context_id = result.get("result", {}).get("contextId") or context_id
    return text, returned_context_id


async def simulate_conversation():
    """Simulate a conversation between two agents."""

    #Assistant IDs
    agent_a_id = os.getenv("AGENT_A_ID")
    agent_b_id = os.getenv("AGENT_B_ID")

    if not agent_a_id or not agent_b_id:
        print("Set AGENT_A_ID and AGENT_B_ID environment variables")
        return

    message = "Hello! Let's have a conversation."
    context_id = None

    async with aiohttp.ClientSession() as session:
        for i in range(3):
            print(f"--- Round {i + 1} ---")

            message, context_id = await send_message(
                session, 2024, agent_a_id, message, context_id=context_id
            )
            print(f"🔵 Agent A: {message}")

            message, context_id = await send_message(
                session, 2025, agent_b_id, message, context_id=context_id
            )
            print(f"🔴 Agent B: {message}\n")


if __name__ == "__main__":
    asyncio.run(simulate_conversation())
```

For complete working examples, see:

* [Two LangGraph agents communicating](https://github.com/langchain-samples/A2A-langgraph) - Example of two LangGraph agents using the A2A protocol
* [Google ADK agent with LangChain agent](https://github.com/langchain-samples/A2A-google-adk) - Example of a Google ADK agent interacting with a LangChain agent using the A2A protocol

## Distributed tracing

For non-LangGraph agents in an agent-based workspace, [register the agent and configure agent addressing](https://docs.langchain.com/langsmith/create-an-agent.md#configure-tracing-for-the-agent) before tracing. LangSmith deployments already provision their agents.

When multiple agents communicate over A2A, LangSmith can group all their [traces](https://docs.langchain.com/langsmith/observability-concepts.md#traces) into a single [thread](https://docs.langchain.com/langsmith/observability-concepts.md#threads), which gives you a unified view of the entire multi-agent conversation.

### How contextId maps to thread\_id

The Agent Server A2A endpoint automatically converts the A2A `contextId` to `thread_id` for LangSmith tracing. This means every message in a conversation, across all participating agents, is grouped under the same thread in LangSmith without any extra configuration on your part.

The flow works as follows:

1. On the first message, the client omits `contextId`. The server generates one and returns it in the response.
2. The client passes the `contextId` in all subsequent messages to maintain conversation continuity.
3. Agent Server maps the `contextId` to `thread_id` in LangSmith [metadata](https://docs.langchain.com/langsmith/add-metadata-tags.md), so all turns appear in the same thread.

> [!WARNING]
>
> The `contextId` is used directly as the LangGraph `thread_id`, so it must be a UUID. Echo back the
> one the server returned rather than minting your own identifier. A `contextId` such as
> `session-42` is rejected with `-32602` and the message `Failed to create run: Invalid thread ID`.

### Tracing across multiple agents

When agents from different frameworks communicate over A2A, `contextId` is what unifies their traces. Reuse the `contextId` returned by the first agent on every later request, to that agent and to the others.

> [!WARNING]
>
> Agent Server does not read a top-level `metadata` field on the JSON-RPC payload. There is no way for a client to set the LangGraph `thread_id` directly — it is always the `contextId`. Sending `metadata.thread_id` to an Agent Server deployment has no effect.

The following code snippet demonstrates the key concepts. For a complete runnable implementation with two agents, refer to the [Google ADK + LangChain example](https://github.com/langchain-samples/A2A-google-adk/blob/main/test_agent_conversation.py).

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
import asyncio
import aiohttp
from langsmith import uuid7
async def send_message(session, url, text, context_id=None):
    """Send an A2A message and return (response_text, context_id)."""

    # --- 1. Build the message ---
    # On follow-up turns, include contextId inside the message object so the server
    # associates them with the ongoing conversation. Do not resend taskId: each turn
    # opens a new task within that conversation.
    message = {
        "role": "user",
        "parts": [{"kind": "text", "text": text}],
        "messageId": str(uuid7()),
    }
    if context_id:
        message["contextId"] = context_id

    # --- 2. Send it ---
    # contextId travels inside the message. Agent Server turns it into the
    # LangGraph thread_id, so no separate tracing field is needed.
    payload = {
        "jsonrpc": "2.0",
        "id": str(uuid7()),
        "method": "message/send",
        "params": {"message": message},
    }

    async with session.post(url, json=payload, headers={"Accept": "application/json"}) as response:
        if response.status != 200:
            raise RuntimeError(f"HTTP {response.status}: {await response.text()}")
        result = await response.json()

    if "error" in result:
        raise RuntimeError(result["error"].get("message", "Unknown error"))

    result_obj = result.get("result", {})
    returned_context_id = result_obj.get("contextId") or context_id
    text_out = next(
        (
            part.get("text", "")
            for art in result_obj.get("artifacts", []) or []
            for part in art.get("parts", []) or []
            if part.get("kind") == "text"
        ),
        "(no text)",
    )
    return text_out, returned_context_id


async def run_conversation(agent_a_url, agent_b_url):
    # --- 3. Share the context across agents ---
    # The first response carries a contextId. Pass it to every agent from then
    # on, and all their traces land in one LangSmith thread.
    context_id = None
    message = "Hello! Let's collaborate."

    async with aiohttp.ClientSession() as session:
        for _ in range(3):
            message, context_id = await send_message(
                session, agent_a_url, message, context_id=context_id
            )

            message, context_id = await send_message(
                session, agent_b_url, message, context_id=context_id
            )


asyncio.run(run_conversation(
    "http://localhost:2024/a2a/<agent_a_assistant_id>",
    "http://localhost:2025/a2a/<agent_b_assistant_id>",
))
```

**1. Build the message**: Include `contextId` inside the `message` object on follow-up turns so the server can associate them with the ongoing conversation. Omit it on the first message, because the server generates a `contextId` and returns it in the response. Do not resend `taskId` from a finished turn.

**2. Send it**: The `contextId` travels inside `params.message`. Agent Server uses it as the LangGraph `thread_id`, so there is no separate tracing field to set.

**3. Share the context across agents**: Let the first agent mint the `contextId`, then pass that same value to every agent for the rest of the conversation. That is what groups their traces into one thread.

### Receive thread\_id in non-LangGraph agents

The [previous section](#tracing-across-multiple-agents) covers the client side — propagating `contextId` when sending messages. If one of your agents is not built on LangGraph, it also needs to read that `contextId` on the receiving end and attach it as the thread identifier, so its traces land in the same LangSmith thread. Use `langsmith.integrations.otel.configure()` to set up automatic tracing, and read `params.message.contextId` from the incoming A2A request.

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from fastapi import FastAPI, Request
from langsmith.integrations.otel import configure as configure_otel
from opentelemetry import trace
import json

# --- 1. Configure OTel ---
# Set up automatic tracing to LangSmith for your non-LangGraph agent.
configure_otel()
tracer = trace.get_tracer(__name__)

app = FastAPI()

@app.middleware("http")
async def set_thread_id_middleware(request: Request, call_next):
    thread_id = None
    if request.method == "POST":
        body_bytes = await request.body()
        if body_bytes:
            # --- 2. Extract contextId from the incoming A2A message ---
            try:
                body = json.loads(body_bytes)
                thread_id = body["params"]["message"].get("contextId")
            except (ValueError, KeyError, TypeError):
                pass
            # Re-inject the body so downstream handlers can still read it
            async def receive():
                return {"type": "http.request", "body": body_bytes}
            request._receive = receive

    # --- 3. Attach thread_id to the trace ---
    # langsmith.metadata.thread_id groups this trace with others in the same thread.
    with tracer.start_as_current_span("agent") as span:
        if thread_id:
            span.set_attribute("langsmith.metadata.thread_id", thread_id)
        return await call_next(request)
```

Register your agent routes on `app` after this middleware.

> [!NOTE]
>
> Set `LANGSMITH_API_KEY`, `LANGSMITH_AGENT_ID`, and `LANGSMITH_AGENT_ENVIRONMENT` in your environment. All participants in the conversation should use the same tracing destination so their traces are visible together.

### View traces in LangSmith

After running a multi-agent conversation, open the [LangSmith UI](https://smith.langchain.com?utm_source=docs\&utm_medium=cta\&utm_campaign=langsmith-signup\&utm_content=langsmith-server-a2a) and navigate to **Threads**. All turns from all participating agents will appear under a single thread, identified by the shared `thread_id`.

## Test your integration

### Against your own deployment

Fetch the card, then send a message:

```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
curl "https://your-deployment/a2a/{assistant_id}/.well-known/agent-card.json"
```

```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
curl -X POST "https://your-deployment/a2a/{assistant_id}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "SendMessage",
    "params": {
      "message": {
        "role": "ROLE_USER",
        "parts": [{"text": "hello"}],
        "messageId": "test-1"
      }
    }
  }'
```

The response contains `result.task.id` and `result.task.contextId`. Reuse the `contextId` on the
next message to continue the conversation.

For streaming, send `Accept: text/event-stream` and use `SendStreamingMessage`. The first event is
the `Task`; status and artifact updates follow.

### Against the official conformance suite

A2A publishes a Technology Compatibility Kit at
[a2aproject/a2a-tck](https://github.com/a2aproject/a2a-tck). It grades an implementation by
RFC 2119 level and works against any A2A endpoint, including yours.

```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
./run_tck.py --sut-host https://your-deployment/a2a/{assistant_id} --transport jsonrpc
```

> [!NOTE]
>
> The TCK drives some scenarios through `messageId` prefixes such as `tck-input-required`, described
> in its `docs/SUT_REQUIREMENTS.md`. A graph that does not implement those prefixes will report those
> requirements as skipped rather than failed.

### What Agent Server currently fails

Agent Server runs the TCK on every CI build as a required check, gated against a checked-in list of
known failures. CI fails if a new failure appears, and also if a listed requirement starts passing,
so the list cannot drift from what the server actually does.

Read this before you build against a capability:

| Gap | What you observe |
| - | - |
| Response wire shape is still v0.3 | Tasks, messages and parts carry `kind` and `mimeType` instead of v1.0 member-presence discrimination |
| Streaming events are flat | SSE emits v0.3 objects with `final`, not `statusUpdate` / `artifactUpdate` wrappers |
| `tool_results` is snake\_case | v1.0 expects `toolResults`. Kept deliberately, because live A2UI clients read this key |
| Timestamps | Serialized as `+00:00` rather than an ISO 8601 `Z` suffix |
| `SubscribeToTask` | Returns `-32601` where the spec requires `-32001` |
| Push notification config | Returns `-32601` where the spec requires `-32003` |
| Errors carry no `data` | No `google.rpc.ErrorInfo` reason or domain is attached |
| `A2A-Version` request header | Not read, so an unsupported version is processed instead of returning `-32009` |
| Agent card caching | No `Cache-Control`, `ETag` or `Last-Modified` headers |
| `GetExtendedAgentCard` | Served, but never advertised via `capabilities.extendedAgentCard` |

## Disable A2A

To disable the A2A endpoint, set `disable_a2a` to `true` in your `langgraph.json` configuration file:

```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
{
  "$schema": "https://langgra.ph/schema.json",
  "http": {
    "disable_a2a": true
  }
}
```

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/server-a2a.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

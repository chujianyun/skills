# Deploy Google ADK agents

> Deploy Google Agent Development Kit (ADK) agents to LangSmith Agent Server using the deployments-wrap-sdk package.

This guide shows you how to deploy a [Google Agent Development Kit (ADK)](https://github.com/google/adk-python) agent on [LangSmith Agent Server](../../Agent%20Server/Capabilities/Agent%20Server.md) using the [`deployments-wrap-sdk`](https://pypi.org/project/deployments-wrap-sdk/) package.

`deployments-wrap-sdk` provides a thin wrapper that turns a configured ADK `Runner` into a LangGraph-compatible graph, so you can deploy ADK agents without writing the [Functional API](https://docs.langchain.com/oss/python/langgraph/functional-api.md) glue yourself. The wrapper:

* Bridges ADK sessions to Agent Server's [checkpoint persistence](../../Agent%20Server/Capabilities/Agent%20Server.md#persistence), so session state survives restarts and resumes across runs.
* Forwards ADK token events through LangGraph's streaming pipeline, so partial tokens show up in [`stream_mode="messages"`](../../Agent%20Server/Capabilities/Streaming%20API.md) and in [LangSmith Studio](../../../Test/Test%20from%20Studio/LangSmith%20Studio.md).
* Automatically enables [LangSmith tracing](../../../Monitor/Trace/Tracing%20setup/Integrations/Agent%20frameworks/Trace%20Google%20ADK%20agents.md) for ADK when `LANGSMITH_TRACING` is set.

## Prerequisites

* Python 3.11+
* [LangGraph CLI](../Reference/LangGraph%20CLI.md) for local dev and deployment
* A LangSmith API key, refer to [Create an account and API key](../../../LangSmith%20setup/Account/Create%20an%20account%20and%20API%20key.md)
* A Google AI API key if you use Gemini models, refer to [Google AI Studio](https://aistudio.google.com/api-keys)

## Installation

Install the package with the `google-adk` extra. The extra pulls in `google-adk` and other dependencies needed for the wrapper:

```bash
pip install "deployments-wrap-sdk[google-adk]"
```

> [!NOTE]
>
> The PyPI distribution name is `deployments-wrap-sdk`, but the Python import path is `saf_sdk`. Both refer to the same package.

## Quickstart

This minimal example builds an agent that returns the input as its response and does not require a model API key. The agent bypasses the LLM call so you can verify that the deployment works correctly before connecting a real model.

Create `agent.py`:

```python agent.py
from google.adk.agents import Agent
from google.adk.models.llm_response import LlmResponse
from google.adk.runners import Runner
from google.genai.types import Content, Part
from saf_sdk.adk import LangsmithSessionService, wrap


def echo_callback(callback_context, llm_request):
    """Return the user's message instead of calling a real model."""
    user_text = ""
    if callback_context.user_content and callback_context.user_content.parts:
        for part in callback_context.user_content.parts:
            if part.text:
                user_text += part.text
    return LlmResponse(
        content=Content(role="model", parts=[Part(text=f"echo: {user_text}")])
    )


agent = wrap(
    Runner(
        agent=Agent(
            name="echo_agent",
            model="gemini-4-hydrogen",
            instruction="Echo the user message.",
            before_model_callback=echo_callback,
        ),
        app_name="adk_echo",
        session_service=LangsmithSessionService(),
    )
)
```

Two things are essential:

1. **Pass `LangsmithSessionService()`** as the runner's `session_service`. `wrap()` raises a `TypeError` if you forget. Agent Server needs this hook to load and save ADK session state through its checkpointer.
2. **Export the wrapped `agent`** as a module-level variable. Agent Server imports this symbol when serving the graph.

For a real agent, drop the `before_model_callback` and configure a model directly. For example, use Gemini by setting `model="gemini-4-hydrogen"` with `GOOGLE_API_KEY` set, or use Claude/OpenAI via ADK's LiteLLM adapter (`google.adk.models.lite_llm.LiteLlm`, available through `google-adk[extensions]`).

## Capabilities and limitations

`wrap()` bridges a defined subset of ADK's runtime to Agent Server. Review the boundaries below before porting an existing ADK agent, since some ADK features are passed through unchanged while others are intentionally not supported.

### Supported

* **Agent primitives**: `Agent`, `SequentialAgent`, and `ParallelAgent`, including nested sub-agent delegation through the `sub_agents` parameter.
* **Tools**: Python function tools and `LongRunningFunctionTool`.
* **Models**: Gemini models directly, and any model supported by ADK's LiteLLM adapter (`google.adk.models.lite_llm.LiteLlm`, available through `google-adk[extensions]`). Set the provider's API key on the deployment.
* **Token streaming**: ADK partial events are forwarded through LangGraph's async callback manager, so token chunks reach clients consuming `stream_mode="messages"` and the Studio chat view.
* **Structured output**: agents configured with `output_schema` and `output_key` expose the typed value on the graph's response in addition to `messages`.
* **Session persistence**: `LangsmithSessionService` stores ADK session state in the deployment's checkpoint store. State survives restarts and is loaded on each subsequent turn of the same thread.
* **Tracing**: when `LANGSMITH_TRACING=true`, the wrapper calls `configure_google_adk()` automatically (see [Enable tracing](#enable-tracing)).
* **Authentication**: if Agent Server [authentication](../../Agent%20Server/Auth%20%26%20access%20control/Authentication%20%26%20access%20control.md) is enabled, the authenticated user id becomes ADK's `user_id`. Otherwise the user id is `"anonymous"`.

### Not supported

* **Multimodal input**: the wrapper forwards only `messages[-1].content` as a single text part. Inbound images, files, audio, or inline binary blocks are not passed to the ADK runner.
* **Multiple new messages per turn**: only the last item in `messages` is treated as the new user message. Conversation history is reconstructed from ADK session state, not from the LangGraph message list.
* **Bidirectional / live streaming**: the wrapper hard-codes `RunConfig(streaming_mode=StreamingMode.SSE)`. ADK's `Runner.run_live()` and the bidirectional streaming mode used for audio or voice agents are not invoked, so live audio and voice agents cannot be deployed through `wrap()`.
* **Non-text output parts**: only `part.text` values are collected from ADK events. Inline images, audio, or files produced by the agent are not surfaced on the graph's `messages` output.
* **Intermediate events as messages**: the response is emitted as one `AIMessage` containing the concatenated text. Tool calls, tool results, and intermediate sub-agent turns are not exposed as separate items in the graph's `messages` field. Inspect them in [LangSmith traces](../../../Monitor/Overview/LangSmith%20Observability.md) instead.
* **Alternative ADK session services**: `runner.session_service` must be a `LangsmithSessionService`. ADK's `InMemorySessionService`, `DatabaseSessionService`, and `VertexAiSessionService` are rejected with a `TypeError`, because session state is held in the LangGraph checkpoint.
* **Native LangGraph interrupts**: the wrapper does not expose LangGraph's `interrupt` or `Command(resume=...)` mechanism. Human-in-the-loop flows built on `LongRunningFunctionTool` follow ADK's own pattern: the tool returns a status such as `pending_approval`, the agent replies, and a follow-up turn resolves the pending call.

## Project layout

A deployable project needs three files:

```
my-adk-agent/
├── agent.py              # exports the wrapped agent
├── langgraph.json        # Agent Server config
└── pyproject.toml        # Python dependencies
```

[`langgraph.json`](../../Agent%20Server/Develop%20your%20application/Application%20structure.md#configuration-file-concepts) points Agent Server at the exported symbol:

```json langgraph.json
{
  "$schema": "https://langgra.ph/schema.json",
  "dependencies": ["."],
  "graphs": {
    "adk_echo": "./agent.py:agent"
  },
  "env": ".env"
}
```

`pyproject.toml` declares dependencies:

```toml pyproject.toml
[project]
name = "my-adk-agent"
version = "0.0.1"
requires-python = ">=3.11"
dependencies = [
    "deployments-wrap-sdk[google-adk]>=0.0.1",
]
```

## Install dependencies

```bash
pip install -e .
```

## Run locally

Start the local Agent Server with the [LangGraph CLI](../Reference/LangGraph%20CLI.md):

```bash
langgraph dev
```

This serves the agent at `http://127.0.0.1:2024` and opens [LangSmith Studio](../../../Test/Test%20from%20Studio/LangSmith%20Studio.md) so you can chat with the agent. Send a request directly with `curl`:

```bash
# Create a thread
THREAD=$(curl -s -X POST http://127.0.0.1:2024/threads \
  -H "Content-Type: application/json" -d '{}' | python -c "import sys, json; print(json.load(sys.stdin)['thread_id'])")

# Run the agent and wait for the final response
curl -s -X POST "http://127.0.0.1:2024/threads/$THREAD/runs/wait" \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "adk_echo",
    "input": {"messages": [{"type": "human", "content": "Hello"}]}
  }'
```

## Deploy to LangSmith

Once the agent runs locally, deploy it to LangSmith with `langgraph deploy`:

```bash
langgraph deploy --name my-adk-agent
```

For environment configuration, deployment types, and revision management, refer to [Deploy to cloud](../../Deploy%20to%20Cloud/Deployment%20guide/Create%20an%20Agent%20Server.md). For self-hosted setups, refer to [Self-hosted deployments](../../../LangSmith%20setup/Self-hosted/Self-hosted%20LangSmith.md).

## Enable tracing

`wrap()` calls `langsmith.integrations.google_adk.configure_google_adk()` automatically whenever LangSmith tracing is enabled, so all you need to do is set the environment variables on the deployment:

```bash .env
LANGSMITH_API_KEY=your-langsmith-api-key
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=my-adk-agent     # optional
GOOGLE_API_KEY=your-google-api-key
```

[Traces](../../../Monitor/Overview/LangSmith%20Observability.md) show agent invocations, tool calls, and LLM interactions in the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-deploy-google-adk). For more on the underlying tracing integration, see [Trace Google ADK applications](../../../Monitor/Trace/Tracing%20setup/Integrations/Agent%20frameworks/Trace%20Google%20ADK%20agents.md).

## API reference

### `wrap(runner)`

Wraps a configured `google.adk.runners.Runner` and returns a LangGraph `Pregel` graph that can be exported from your module and served by Agent Server.

| Argument | Type | Description |
| - | - | - |
| `runner` | `google.adk.runners.Runner` | A configured ADK Runner. Its `session_service` **must** be a `LangsmithSessionService`. |

**Returns:** A `Pregel` graph whose name is `runner.app_name`.

**Raises:** `TypeError` if `runner.session_service` is not a `LangsmithSessionService`.

If `runner.agent` defines an `output_key`, that key's value is also exposed on the graph's output, in addition to `messages`. This is what makes ADK structured-output agents (`output_schema=...`, `output_key=...`) work with Studio and the `/runs/wait` response.

### `LangsmithSessionService`

A `google.adk.sessions.BaseSessionService` implementation backed by Agent Server's checkpoint store. The wrapper manages session lifecycle automatically. It creates a session on the first turn of a thread, loads it from the checkpoint on subsequent turns, and writes the updated session back when the run completes.

Use a fresh instance per `Runner`:

```python
session_service = LangsmithSessionService()
```

You should not need to call its methods directly; `wrap()` drives them through ADK's normal session lifecycle.

### `ADKInput`

The default input schema for a wrapped agent.

| Field | Type | Description |
| - | - | - |
| `messages` | `list[AnyMessage]` | (Required) Conversation messages; the wrapper sends `messages[-1].content` to the ADK runner as the new user message. |
| `state_delta` | `dict[str, Any] \| None` | (Optional) Passed through to `runner.run_async(state_delta=...)` to mutate ADK session state for this turn. |

### `ADKOutput`

The default output schema for a wrapped agent.

| Field | Type | Description |
| - | - | - |
| `messages` | `list[AnyMessage]` | The agent's response messages, appended to the thread via LangGraph's `add_messages` reducer. |

Exposing `messages` as a typed field (rather than a plain `dict`) is what lets Studio detect the graph as chat-compatible and enable the chat-mode toggle.

## How it works

When a run arrives:

1. The wrapped graph reads `thread_id` from the run config and uses it as the ADK `session_id`. If [authentication](../../Agent%20Server/Auth%20%26%20access%20control/Authentication%20%26%20access%20control.md) is enabled, the authenticated user's id becomes the ADK `user_id`; otherwise the user id is `"anonymous"`.
2. The wrapper loads the previous session (if any) from the LangGraph checkpoint into `LangsmithSessionService`, then asks the runner to handle the latest message.
3. The runner emits ADK events. The wrapper forwards partial-token events through LangGraph's async callback manager so they stream out via `stream_mode="messages"`, and collects final text for the response message.
4. When the run finishes, the wrapper serializes the ADK session and saves it to the checkpoint via `entrypoint.final(save=...)`. The next run on the same thread resumes from that state.

This means ADK's own session/state semantics are preserved end-to-end while the deployment gets the standard Agent Server features: durable runs, streaming, multi-thread persistence, and tracing.

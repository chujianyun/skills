# Event streaming

> Stream real-time updates from LangChain agent runs

LangChain agents are built on LangGraph, so they support the same streaming stack with agent-focused projections for messages, tool calls, state, and custom updates.

For most application and frontend use cases, use **Event Streaming** through `stream_events(..., version="v3")`. Event Streaming returns a run object with typed projections, so each projection can be consumed independently instead of parsing stream-mode tuples.

```py
from langchain.agents import create_agent


def get_weather(city: str) -> str:
    """Get weather for a city."""
    return f"It's always sunny in {city}!"


agent = create_agent(
    model="gpt-5-nano",
    tools=[get_weather],
)

stream = agent.stream_events({
    "messages": [{"role": "user", "content": "What is the weather in SF?"}],
}, version="v3")

for message in stream.messages:
    for delta in message.text:
        print(delta, end="", flush=True)

final_state = stream.output
```

## What you can stream

| Projection | Use |
| - | - |
| `for event in stream` | Raw protocol events with full envelope and access to every channel. |
| `stream.messages` | Model message streams, one per LLM call. |
| `message.text` | Text deltas and final text for a message. |
| `message.reasoning` | Reasoning deltas for models that expose reasoning content. |
| `message.tool_calls` | Tool-call argument chunks and finalized tool calls. |
| `message.output` | Final message object after the model call completes. |
| `stream.values` | Agent state snapshots. |
| `stream.output` | Final agent state. |
| `stream.subgraphs` | Nested graph runs (sub-agents and plain subgraphs). |
| `stream.extensions` | Custom transformer projections. |
| `stream.tool_calls` | Tool execution lifecycle, inputs, output deltas, final output, and errors. |

`stream.messages` yields `ChatModelStream` objects. Each message stream exposes `.text`, `.reasoning`, `.tool_calls`, and `.output`. Sync projections are iterable for live deltas and drainable for final values: use `str(message.text)` for final text and `message.tool_calls.get()` for finalized tool calls.

## Agent messages

Use `stream.messages` when you want model output from each LLM call.

```py
stream = agent.stream_events(input, version="v3")

for message in stream.messages:
    print(f"[{message.node}] ", end="")
    for delta in message.text:
        print(delta, end="", flush=True)

    full_message = message.output
    usage = full_message.usage_metadata
    if usage:
        print(usage)
```

`message.output` gives you the finalized AI message, including provider-specific content blocks. In TypeScript, use `message.usage` when you only need token counts or other usage metadata; in Python, read usage from `message.output.usage_metadata`.

## Reasoning content

Reasoning content uses the same shape as text content, but it is available only when the selected model emits reasoning blocks.

```py
stream = agent.stream_events(input, version="v3")

for message in stream.messages:
    for delta in message.reasoning:
        print(f"[thinking] {delta}", end="", flush=True)

    for delta in message.text:
        print(delta, end="", flush=True)
```

See the [reasoning guide](Models.md#reasoning) and your provider's integration page for model configuration details.

## Tool calls

There are two useful tool-call projections:

* `message.tool_calls` streams tool-call argument chunks while the model is producing the tool call.
* `stream.tool_calls` streams the lifecycle of tool execution after the tool call starts.

```py
stream = agent.stream_events(input, version="v3")

for message in stream.messages:
    for chunk in message.tool_calls:
        print(f"tool call chunk: {chunk}")

    finalized = message.tool_calls.get()
    if finalized:
        print(f"finalized tool calls: {finalized}")

for call in stream.tool_calls:
    print(f"{call.tool_name}({call.input})")
    for delta in call.output_deltas:
        print(delta, end="", flush=True)
    print(call.output, call.error)
```

Each chunk from `message.tool_calls` is a `tool_call_chunk` that holds the call's `id`, its `name`, and only the new part of its `args`. A call's chunks concatenate into its full arguments, and `message.tool_calls.get()` returns the parsed tool calls.

> [!NOTE]
>
> Chunks that hold only the new part of the arguments require `langchain-core>=1.6.13`. In earlier versions, each chunk holds all of the arguments so far.

## Streaming sub-agents

When a `create_agent` call invokes another named `create_agent` (via a wrapping tool, typically), the inner agent's events flow at a nested namespace. The `name=` you pass to `create_agent` identifies that inner agent in the stream, so you can filter and label per agent.

Named sub-agents surface on the dedicated `stream.subagents` projection. Each handle exposes the inner agent's own `.messages`, `.values`, `.tool_calls`, and `.output`, plus `.name` (the `name=` you passed) and `.cause` (the tool call that dispatched the sub-agent). Because only named `create_agent` runs appear here, you don't need to filter plain subgraphs out.

```py
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model


def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


weather_agent = create_agent(
    model=init_chat_model("openai:gpt-6.1-sol"),
    tools=[get_weather],
    name="weather_agent",
)


def call_weather(query: str) -> str:
    """Query the weather agent."""
    result = weather_agent.invoke({"messages": [{"role": "user", "content": query}]})
    return result["messages"][-1].text


supervisor = create_agent(
    model=init_chat_model("openai:gpt-6.1-sol"),
    tools=[call_weather],
    name="supervisor",
)

stream = supervisor.stream_events(
    {"messages": [{"role": "user", "content": "What's the weather in Boston?"}]},
    version="v3",
)

for subagent in stream.subagents:
    print(f"{subagent.name}: ", end="")
    for message in subagent.messages:
        for token in message.text:
            print(token, end="", flush=True)
    print()
```

Plain `StateGraph` subgraphs invoked from a tool also surface on `stream.subgraphs` — set `name=` on `.compile(name=...)` to get a label in `subagent.graph_name`.

`stream.subagents` is the focused view of named `create_agent` sub-agents, while `stream.subgraphs` covers every nested graph. Use whichever matches your UI.

## State and final output

Use `stream.values` for state snapshots and `stream.output` for the final agent state.

```py
stream = agent.stream_events(input, version="v3")

for snapshot in stream.values:
    print(snapshot)

final_state = stream.output
```

## Multiple projections

For concurrent consumption in async code, use `astream_events` with `asyncio.gather`:

```py
import asyncio

stream = await agent.astream_events(input, version="v3")

async def consume_messages():
    async for message in stream.messages:
        print(await message.text)

async def consume_tool_calls():
    async for call in stream.tool_calls:
        print(call.tool_name, call.input)

await asyncio.gather(consume_messages(), consume_tool_calls())
```

For synchronous code, use `stream.interleave(...)` instead:

```py
stream = agent.stream_events(input, version="v3")

for name, item in stream.interleave("messages", "tool_calls", "values"):
    if name == "messages":
        print(item.text)
    elif name == "tool_calls":
        print(item.tool_name, item.input)
    elif name == "values":
        print(item)
```

To access channels that aren't exposed as typed projections, or to inspect the full event envelope, iterate raw protocol events:

```py
for event in stream:
    print(event["method"], event["params"]["namespace"], event["params"]["data"])
```

## Custom updates

Use custom stream transformers when your application needs a projection that is not built in, such as retrieval progress, artifacts, or domain-specific events.

```py
stream = agent.stream_events(
    input,
    version="v3",
    transformers=[ToolActivityTransformer],
)

for activity in stream.extensions["tool_activity"]:
    print(activity)
```

### Register transformers on middleware

> [!NOTE]
>
> Middleware-registered transformers require `langchain>=1.3.2`.

Middleware can declare stream transformer factories alongside its hooks and tools. The factory shape differs between languages:

Set the `transformers` attribute on an `AgentMiddleware` subclass to a sequence of factories. Each factory has the shape `Callable[[tuple[str, ...]], StreamTransformer]` and is invoked as `factory(scope)`, where `scope` is the mini-mux scope tuple (`()` for the root mux, non-empty for subgraphs). Returning a fresh transformer per call keeps each subgraph isolated.

```py
from langchain.agents import create_agent
from langchain.agents.middleware import AgentMiddleware


class ToolActivityMiddleware(AgentMiddleware):
    transformers = (ToolActivityTransformer,)


agent = create_agent(
    model="gpt-5-nano",
    tools=[get_weather],
    middleware=[ToolActivityMiddleware()],
)
```

At compile time, `create_agent` merges middleware-registered factories with anything passed to its own `transformers=` argument. The final order on the compiled graph is:

1. The built-in `ToolCallTransformer`.
2. Middleware-registered factories, in middleware order.
3. Caller-supplied `transformers=` from `create_agent`.

This keeps the built-in tool-call projection in front of consumer transformers and gives caller-supplied entries the final word.

The built-in `PIIMiddleware` uses this hook to redact PII from streamed wire output. With `apply_to_output=True`, its registered transformer scrubs detected PII from text deltas, tool-call args, tool outputs, and state snapshots before they leave the run, closing the window where `after_model` state-level redaction would otherwise let raw PII through to live readers of `stream_events(version="v3")`.

```py
from langchain.agents import create_agent
from langchain.agents.middleware import PIIMiddleware

agent = create_agent(
    model="gpt-5-nano",
    tools=[],
    middleware=[
        PIIMiddleware("email", strategy="redact", apply_to_output=True),
    ],
)
```

See [PII detection](../Middleware/Prebuilt%20middleware.md#pii-detection) for the full configuration surface.

See [Build your own projection](https://docs.langchain.com/oss/python/langgraph/event-streaming.md#build-your-own-projection) for the transformer contract.

## Related

* [Streaming](Streaming.md) covers low-level Pregel stream modes.
* [Build your own projection](https://docs.langchain.com/oss/python/langgraph/event-streaming.md#build-your-own-projection) covers writing application-specific projections.
* [Frontend streaming patterns](../Frontend/Overview.md) shows UI use cases built on streamed state.

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/event-streaming.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

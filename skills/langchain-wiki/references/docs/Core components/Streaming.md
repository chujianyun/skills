# Streaming

> Stream real-time updates from agent runs

> [!TIP]
>
> For new applications, we recommend [event streaming](Event%20streaming.md)—the typed-projection API introduced in LangChain v1.3. Event streaming gives you separate iterators per projection (messages, values, tool calls, subgraphs) so you can consume them independently instead of branching on `stream_mode` chunks.

LangChain implements a streaming system to surface real-time updates.

Streaming is crucial for enhancing the responsiveness of applications built on LLMs. By displaying output progressively, even before a complete response is ready, streaming significantly improves user experience (UX), particularly when dealing with the latency of LLMs.

## Overview

LangChain's streaming system lets you surface live feedback from agent runs to your application.

What's possible with LangChain streaming:

* &#x20;[**Stream agent progress**](#agent-progress)—get state updates after each agent step.
* &#x20;[**Stream LLM tokens**](#llm-tokens)—stream language model tokens as they're generated.
* &#x20;[**Stream thinking / reasoning tokens**](#streaming-thinking-/-reasoning-tokens)—surface model reasoning as it's generated.
* &#x20;[**Stream custom updates**](#custom-updates)—emit user-defined signals (e.g., `"Fetched 10/100 records"`).
* &#x20;[**Stream multiple modes**](#stream-multiple-modes)—choose from `updates` (agent progress), `messages` (LLM tokens + metadata), or `custom` (arbitrary user data).

See the [common patterns](#common-patterns) section below for additional end-to-end examples.

## Supported stream modes

Pass one or more of the following stream modes as a list to the [`stream`](https://reference.langchain.com/python/langgraph/graphs/#langgraph.graph.state.CompiledStateGraph.stream) or [`astream`](https://reference.langchain.com/python/langgraph/graphs/#langgraph.graph.state.CompiledStateGraph.astream) methods:

| Mode | Description |
| - | - |
| `updates` | Streams state updates after each agent step. If multiple updates are made in the same step (e.g., multiple nodes are run), those updates are streamed separately. |
| `messages` | Streams tuples of `(token, metadata)` from any graph nodes where an LLM is invoked. |
| `custom` | Streams custom data from inside your graph nodes using the stream writer. |

## Agent progress

To stream agent progress, use the [`stream`](https://reference.langchain.com/python/langgraph/graphs/#langgraph.graph.state.CompiledStateGraph.stream) or [`astream`](https://reference.langchain.com/python/langgraph/graphs/#langgraph.graph.state.CompiledStateGraph.astream) methods with `stream_mode="updates"`. This emits an event after every agent step.

For example, if you have an agent that calls a tool once, you should see the following updates:

* **LLM node**: [`AIMessage`](https://reference.langchain.com/python/langchain-core/messages/ai/AIMessage) with tool call requests
* **Tool node**: [`ToolMessage`](https://reference.langchain.com/python/langchain-core/messages/tool/ToolMessage) with execution result
* **LLM node**: Final AI response

Pass a `thread_id` via `config` so the conversation is checkpointed and follow-up turns can resume the same history. `thread_id` is independent of `stream_mode`; you can also pass `context` alongside it for per-run data your tools read from `runtime.context`.

```python Google
from langchain.agents import create_agent
from langchain_core.utils.uuid import uuid7
from langgraph.checkpoint.memory import InMemorySaver

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="google_genai:gemini-4-hydrogen",
    tools=[get_weather],
    checkpointer=InMemorySaver()
)
config = {"configurable": {"thread_id": str(uuid7())}}
stream = agent.stream_events(  # [!code highlight]
    {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
    config=config,
    version="v3",  # [!code highlight]
)
for kind, item in stream.interleave("messages", "tool_calls"):  # [!code highlight]
    if kind == "messages":
        for token in item.text:
            print(token, end="", flush=True)
    elif kind == "tool_calls":
        print(f"\nTool call: {item.tool_name}({item.input})")
        for delta in item.output_deltas:
            print(delta, end="", flush=True)
        print(f"\nTool result: {item.output}")

final_state = stream.output  # [!code highlight]
```

```python OpenAI
from langchain.agents import create_agent
from langchain_core.utils.uuid import uuid7
from langgraph.checkpoint.memory import InMemorySaver

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="openai:gpt-6.1-sol",
    tools=[get_weather],
    checkpointer=InMemorySaver()
)
config = {"configurable": {"thread_id": str(uuid7())}}
stream = agent.stream_events(  # [!code highlight]
    {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
    config=config,
    version="v3",  # [!code highlight]
)
for kind, item in stream.interleave("messages", "tool_calls"):  # [!code highlight]
    if kind == "messages":
        for token in item.text:
            print(token, end="", flush=True)
    elif kind == "tool_calls":
        print(f"\nTool call: {item.tool_name}({item.input})")
        for delta in item.output_deltas:
            print(delta, end="", flush=True)
        print(f"\nTool result: {item.output}")

final_state = stream.output  # [!code highlight]
```

```python Anthropic
from langchain.agents import create_agent
from langchain_core.utils.uuid import uuid7
from langgraph.checkpoint.memory import InMemorySaver

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="anthropic:claude-sonnet-5",
    tools=[get_weather],
    checkpointer=InMemorySaver()
)
config = {"configurable": {"thread_id": str(uuid7())}}
stream = agent.stream_events(  # [!code highlight]
    {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
    config=config,
    version="v3",  # [!code highlight]
)
for kind, item in stream.interleave("messages", "tool_calls"):  # [!code highlight]
    if kind == "messages":
        for token in item.text:
            print(token, end="", flush=True)
    elif kind == "tool_calls":
        print(f"\nTool call: {item.tool_name}({item.input})")
        for delta in item.output_deltas:
            print(delta, end="", flush=True)
        print(f"\nTool result: {item.output}")

final_state = stream.output  # [!code highlight]
```

```python OpenRouter
from langchain.agents import create_agent
from langchain_core.utils.uuid import uuid7
from langgraph.checkpoint.memory import InMemorySaver

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="openrouter:z-ai/glm-5.2",
    tools=[get_weather],
    checkpointer=InMemorySaver()
)
config = {"configurable": {"thread_id": str(uuid7())}}
stream = agent.stream_events(  # [!code highlight]
    {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
    config=config,
    version="v3",  # [!code highlight]
)
for kind, item in stream.interleave("messages", "tool_calls"):  # [!code highlight]
    if kind == "messages":
        for token in item.text:
            print(token, end="", flush=True)
    elif kind == "tool_calls":
        print(f"\nTool call: {item.tool_name}({item.input})")
        for delta in item.output_deltas:
            print(delta, end="", flush=True)
        print(f"\nTool result: {item.output}")

final_state = stream.output  # [!code highlight]
```

```python Fireworks
from langchain.agents import create_agent
from langchain_core.utils.uuid import uuid7
from langgraph.checkpoint.memory import InMemorySaver

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="fireworks:accounts/fireworks/models/glm-5p2",
    tools=[get_weather],
    checkpointer=InMemorySaver()
)
config = {"configurable": {"thread_id": str(uuid7())}}
stream = agent.stream_events(  # [!code highlight]
    {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
    config=config,
    version="v3",  # [!code highlight]
)
for kind, item in stream.interleave("messages", "tool_calls"):  # [!code highlight]
    if kind == "messages":
        for token in item.text:
            print(token, end="", flush=True)
    elif kind == "tool_calls":
        print(f"\nTool call: {item.tool_name}({item.input})")
        for delta in item.output_deltas:
            print(delta, end="", flush=True)
        print(f"\nTool result: {item.output}")

final_state = stream.output  # [!code highlight]
```

```python Baseten
from langchain.agents import create_agent
from langchain_core.utils.uuid import uuid7
from langgraph.checkpoint.memory import InMemorySaver

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="baseten:zai-org/GLM-5.2",
    tools=[get_weather],
    checkpointer=InMemorySaver()
)
config = {"configurable": {"thread_id": str(uuid7())}}
stream = agent.stream_events(  # [!code highlight]
    {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
    config=config,
    version="v3",  # [!code highlight]
)
for kind, item in stream.interleave("messages", "tool_calls"):  # [!code highlight]
    if kind == "messages":
        for token in item.text:
            print(token, end="", flush=True)
    elif kind == "tool_calls":
        print(f"\nTool call: {item.tool_name}({item.input})")
        for delta in item.output_deltas:
            print(delta, end="", flush=True)
        print(f"\nTool result: {item.output}")

final_state = stream.output  # [!code highlight]
```

```python Ollama
from langchain.agents import create_agent
from langchain_core.utils.uuid import uuid7
from langgraph.checkpoint.memory import InMemorySaver

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="ollama:north-mini-code-1.0",
    tools=[get_weather],
    checkpointer=InMemorySaver()
)
config = {"configurable": {"thread_id": str(uuid7())}}
stream = agent.stream_events(  # [!code highlight]
    {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
    config=config,
    version="v3",  # [!code highlight]
)
for kind, item in stream.interleave("messages", "tool_calls"):  # [!code highlight]
    if kind == "messages":
        for token in item.text:
            print(token, end="", flush=True)
    elif kind == "tool_calls":
        print(f"\nTool call: {item.tool_name}({item.input})")
        for delta in item.output_deltas:
            print(delta, end="", flush=True)
        print(f"\nTool result: {item.output}")

final_state = stream.output  # [!code highlight]
```

> [card] [View example trace](https://smith.langchain.com/public/16eb839b-dd05-461e-9f4f-563852f198e0/r)
>
> Open a public LangSmith run for this example.

```shell title="Output"
step: model
content: [{'type': 'tool_call', 'name': 'get_weather', 'args': {'city': 'San Francisco'}, 'id': 'call_9lBtsDbmmobzyA8xc4I4Ctne'}]
step: tools
content: [{'type': 'text', 'text': "It's always sunny in San Francisco!"}]
step: model
content: [{'type': 'text', 'text': "San Francisco weather: It's always sunny in San Francisco!\n\nIf you’d like the exact current conditions (temperature, humidity, wind) and a short forecast, I can fetch that next. Would you like me to pull live details for San Francisco?"}]
```

> [!NOTE]
>
> Persisting conversation history with `thread_id` requires the agent to be configured with a [checkpointer](../Advanced%20usage/Long-term%20memory.md). On [LangSmith Agent Server](https://docs.langchain.com/langsmith/deployment.md), a checkpointer is provisioned automatically. Locally, pass one explicitly, for example `create_agent(..., checkpointer=InMemorySaver())`. The remaining snippets on this page omit `thread_id` for brevity, but you should pass it in production.

## LLM tokens

To stream tokens as they are produced by the LLM, use `stream_mode="messages"`. Below you can see the output of the agent streaming tool calls and the final response.

```python title="Streaming LLM tokens"
from langchain.agents import create_agent


def get_weather(city: str) -> str:
    """Get weather for a given city."""

    return f"It's always sunny in {city}!"

agent = create_agent(
    model="gpt-5-nano",
    tools=[get_weather],
)
for chunk in agent.stream(  # [!code highlight]
    {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
    stream_mode="messages",
    version="v2",  # [!code highlight]
):
    if chunk["type"] == "messages":  # [!code highlight]
        token, metadata = chunk["data"]  # [!code highlight]
        print(f"node: {metadata['langgraph_node']}")
        print(f"content: {token.content_blocks}")
        print("\n")
```

```shell title="Output" expandable
node: model
content: [{'type': 'tool_call_chunk', 'id': 'call_vbCyBcP8VuneUzyYlSBZZsVa', 'name': 'get_weather', 'args': '', 'index': 0}]


node: model
content: [{'type': 'tool_call_chunk', 'id': None, 'name': None, 'args': '{"', 'index': 0}]


node: model
content: [{'type': 'tool_call_chunk', 'id': None, 'name': None, 'args': 'city', 'index': 0}]


node: model
content: [{'type': 'tool_call_chunk', 'id': None, 'name': None, 'args': '":"', 'index': 0}]


node: model
content: [{'type': 'tool_call_chunk', 'id': None, 'name': None, 'args': 'San', 'index': 0}]


node: model
content: [{'type': 'tool_call_chunk', 'id': None, 'name': None, 'args': ' Francisco', 'index': 0}]


node: model
content: [{'type': 'tool_call_chunk', 'id': None, 'name': None, 'args': '"}', 'index': 0}]


node: model
content: []


node: tools
content: [{'type': 'text', 'text': "It's always sunny in San Francisco!"}]


node: model
content: []


node: model
content: [{'type': 'text', 'text': 'Here'}]


node: model
content: [{'type': 'text', 'text': ''s'}]


node: model
content: [{'type': 'text', 'text': ' what'}]


node: model
content: [{'type': 'text', 'text': ' I'}]


node: model
content: [{'type': 'text', 'text': ' got'}]


node: model
content: [{'type': 'text', 'text': ':'}]


node: model
content: [{'type': 'text', 'text': ' "'}]


node: model
content: [{'type': 'text', 'text': "It's"}]


node: model
content: [{'type': 'text', 'text': ' always'}]


node: model
content: [{'type': 'text', 'text': ' sunny'}]


node: model
content: [{'type': 'text', 'text': ' in'}]


node: model
content: [{'type': 'text', 'text': ' San'}]


node: model
content: [{'type': 'text', 'text': ' Francisco'}]


node: model
content: [{'type': 'text', 'text': '!"\n\n'}]
```

> [!NOTE]
>
> **Wrapping an agent as a node in a parent `StateGraph`?** [`create_agent`](https://reference.langchain.com/python/langchain/agents/factory/create_agent) returns a compiled graph, so using it as a node makes it a subgraph. `stream_mode="messages"` on the parent graph will not emit token chunks from the inner agent's LLM calls unless you pass `subgraphs=True`. See [Subgraph outputs](https://docs.langchain.com/oss/python/langgraph/streaming.md#subgraph-outputs).

## Custom updates

To stream updates from tools as they are executed, you can use [`get_stream_writer`](https://reference.langchain.com/python/langgraph/config/get_stream_writer).

```python title="Streaming custom updates"
from langchain.agents import create_agent
from langgraph.config import get_stream_writer  # [!code highlight]


def get_weather(city: str) -> str:
    """Get weather for a given city."""
    writer = get_stream_writer()  # [!code highlight]
    # stream any arbitrary data
    writer(f"Looking up data for city: {city}")
    writer(f"Acquired data for city: {city}")
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="claude-sonnet-4-6",
    tools=[get_weather],
)

for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
    stream_mode="custom",  # [!code highlight]
    version="v2",  # [!code highlight]
):
    if chunk["type"] == "custom":  # [!code highlight]
        print(chunk["data"])  # [!code highlight]
```

```shell title="Output"
Looking up data for city: San Francisco
Acquired data for city: San Francisco
```

> [!NOTE]
>
> If you add [`get_stream_writer`](https://reference.langchain.com/python/langgraph/config/get_stream_writer) inside your tool, you won't be able to invoke the tool outside of a LangGraph execution context.

## Stream multiple modes

You can specify multiple streaming modes by passing stream mode as a list: `stream_mode=["updates", "custom"]`.

Each streamed chunk is a `StreamPart` dict with `type`, `ns`, and `data` keys. Use `chunk["type"]` to determine the stream mode and `chunk["data"]` to access the payload.

```python title="Streaming multiple modes"
from langchain.agents import create_agent
from langgraph.config import get_stream_writer


def get_weather(city: str) -> str:
    """Get weather for a given city."""
    writer = get_stream_writer()
    writer(f"Looking up data for city: {city}")
    writer(f"Acquired data for city: {city}")
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="gpt-5-nano",
    tools=[get_weather],
)

for chunk in agent.stream(  # [!code highlight]
    {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
    stream_mode=["updates", "custom"],
    version="v2",  # [!code highlight]
):
    print(f"stream_mode: {chunk['type']}")  # [!code highlight]
    print(f"content: {chunk['data']}")  # [!code highlight]
    print("\n")
```

```shell title="Output"
stream_mode: updates
content: {'model': {'messages': [AIMessage(content='', response_metadata={'token_usage': {'completion_tokens': 280, 'prompt_tokens': 132, 'total_tokens': 412, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 256, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_provider': 'openai', 'model_name': 'gpt-5-nano-2025-08-07', 'system_fingerprint': None, 'id': 'chatcmpl-C9tlgBzGEbedGYxZ0rTCz5F7OXpL7', 'service_tier': 'default', 'finish_reason': 'tool_calls', 'logprobs': None}, id='lc_run--480c07cb-e405-4411-aa7f-0520fddeed66-0', tool_calls=[{'name': 'get_weather', 'args': {'city': 'San Francisco'}, 'id': 'call_KTNQIftMrl9vgNwEfAJMVu7r', 'type': 'tool_call'}], usage_metadata={'input_tokens': 132, 'output_tokens': 280, 'total_tokens': 412, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 256}})]}}


stream_mode: custom
content: Looking up data for city: San Francisco


stream_mode: custom
content: Acquired data for city: San Francisco


stream_mode: updates
content: {'tools': {'messages': [ToolMessage(content="It's always sunny in San Francisco!", name='get_weather', tool_call_id='call_KTNQIftMrl9vgNwEfAJMVu7r')]}}


stream_mode: updates
content: {'model': {'messages': [AIMessage(content='San Francisco weather: It's always sunny in San Francisco!\n\n', response_metadata={'token_usage': {'completion_tokens': 764, 'prompt_tokens': 168, 'total_tokens': 932, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 704, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_provider': 'openai', 'model_name': 'gpt-5-nano-2025-08-07', 'system_fingerprint': None, 'id': 'chatcmpl-C9tljDFVki1e1haCyikBptAuXuHYG', 'service_tier': 'default', 'finish_reason': 'stop', 'logprobs': None}, id='lc_run--acbc740a-18fe-4a14-8619-da92a0d0ee90-0', usage_metadata={'input_tokens': 168, 'output_tokens': 764, 'total_tokens': 932, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 704}})]}}
```

## Common patterns

Below are examples showing common use cases for streaming.

### Streaming thinking / reasoning tokens

Some models perform internal reasoning before producing a final answer. You can stream these thinking / reasoning tokens as they're generated by filtering [standard content blocks](Messages.md#standard-content-blocks) for the `type` `"reasoning"`.

> [!NOTE]
>
> Reasoning output must be enabled on the model.
>
> See the [reasoning section](Models.md#reasoning) and your [provider's integration page](https://docs.langchain.com/oss/python/integrations/providers/overview.md) for configuration details.
>
> To quickly check a model's reasoning support, see [models.dev](https://models.dev).

To stream thinking tokens from an agent, use `stream_mode="messages"` and filter for reasoning content blocks:

```python
from langchain.agents import create_agent
from langchain_anthropic import ChatAnthropic
from langchain_core.runnables import Runnable


def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


model = ChatAnthropic(
    model_name="claude-sonnet-4-6",
    timeout=None,
    stop=None,
    thinking={"type": "enabled", "budget_tokens": 5000},
)
agent: Runnable = create_agent(
    model=model,
    tools=[get_weather],
)

stream = agent.stream_events(  # [!code highlight]
    {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
    version="v3",
)
for message in stream.messages:
    for token in message.reasoning:
        print(f"[thinking] {token}", end="")
    for token in message.text:
        print(token, end="", flush=True)
```

> [card] [View example trace](https://smith.langchain.com/public/e729edb4-e67d-4418-85b3-e1ce4663e8e5/r)
>
> Open a public LangSmith run for this example.

```shell title="Output"
[thinking] The user is asking about the weather in San Francisco. I have a tool
[thinking]  available to get this information. Let me call the get_weather tool
[thinking]  with "San Francisco" as the city parameter.
The weather in San Francisco is: It's always sunny in San Francisco!
```

This works the same way regardless of the model provider—LangChain normalizes provider-specific formats (Anthropic `thinking` blocks, OpenAI `reasoning` summaries, etc.) into a standard `"reasoning"` content block type via the [`content_blocks`](Messages.md#standard-content-blocks) property.

To stream reasoning tokens directly from a chat model (without an agent), see [streaming with chat models](Models.md#reasoning).

### Streaming tool calls

You may want to stream both:

1. Partial JSON as [tool calls](Models.md#tool-calling) are generated
2. The completed, parsed tool calls that are executed

Specifying [`stream_mode="messages"`](#llm-tokens) will stream incremental [message chunks](Messages.md#streaming-and-chunks) generated by all LLM calls in the agent. To access the completed messages with parsed tool calls:

1. If those messages are tracked in the [state](Short-term%20memory.md) (as in the model node of [`create_agent`](Agents.md)), use `stream_mode=["messages", "updates"]` to access completed messages through [state updates](#agent-progress) (demonstrated below).
2. If those messages are not tracked in the state, use [custom updates](#custom-updates) or aggregate the chunks during the streaming loop ([next section](#accessing-completed-messages)).

> [!NOTE]
>
> Refer to the section below on [streaming from sub-agents](#streaming-from-sub-agents) if your agent includes multiple LLMs.

```python
from typing import Any

from langchain.agents import create_agent
from langchain.messages import AIMessage, AIMessageChunk, AnyMessage, ToolMessage


def get_weather(city: str) -> str:
    """Get weather for a given city."""

    return f"It's always sunny in {city}!"


agent = create_agent("openai:gpt-6.1-sol", tools=[get_weather])


def _render_message_chunk(token: AIMessageChunk) -> None:
    if token.text:
        print(token.text, end="|")
    if token.tool_call_chunks:
        print(token.tool_call_chunks)
    # N.B. all content is available through token.content_blocks


def _render_completed_message(message: AnyMessage) -> None:
    if isinstance(message, AIMessage) and message.tool_calls:
        print(f"Tool calls: {message.tool_calls}")
    if isinstance(message, ToolMessage):
        print(f"Tool response: {message.content_blocks}")


input_message = {"role": "user", "content": "What is the weather in Boston?"}
for chunk in agent.stream(
    {"messages": [input_message]},
    stream_mode=["messages", "updates"],  # [!code highlight]
    version="v2",  # [!code highlight]
):
    if chunk["type"] == "messages":  # [!code highlight]
        token, metadata = chunk["data"]  # [!code highlight]
        if isinstance(token, AIMessageChunk):
            _render_message_chunk(token)  # [!code highlight]
    elif chunk["type"] == "updates":  # [!code highlight]
        for source, update in chunk["data"].items():  # [!code highlight]
            if source in ("model", "tools"):  # `source` captures node name
                _render_completed_message(update["messages"][-1])  # [!code highlight]
```

```shell title="Output" expandable
[{'name': 'get_weather', 'args': '', 'id': 'call_D3Orjr89KgsLTZ9hTzYv7Hpf', 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '{"', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': 'city', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '":"', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': 'Boston', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '"}', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
Tool calls: [{'name': 'get_weather', 'args': {'city': 'Boston'}, 'id': 'call_D3Orjr89KgsLTZ9hTzYv7Hpf', 'type': 'tool_call'}]
Tool response: [{'type': 'text', 'text': "It's always sunny in Boston!"}]
The| weather| in| Boston| is| **|sun|ny|**|.|
```

#### Accessing completed messages

> [!NOTE]
>
> If completed messages are tracked in an agent's [state](Short-term%20memory.md), you can use `stream_mode=["messages", "updates"]` as demonstrated in the [Streaming tool calls](#streaming-tool-calls) section to access completed messages during streaming.

In some cases, completed messages are not reflected in [state updates](#agent-progress). If you have access to the agent internals, you can use [custom updates](#custom-updates) to access these messages during streaming. Otherwise, you can aggregate message chunks in the streaming loop (see below).

Consider the below example, where we incorporate a [stream writer](#custom-updates) into a simplified [guardrail middleware](../Advanced%20usage/Guardrails.md#after-agent-guardrails). This middleware demonstrates tool calling to generate a structured "safe / unsafe" evaluation (one could also use [structured outputs](Models.md#structured-output) for this):

```python
from typing import Any, Literal

from langchain.agents.middleware import after_agent, AgentState
from langgraph.runtime import Runtime
from langchain.messages import AIMessage
from langchain.chat_models import init_chat_model
from langgraph.config import get_stream_writer  # [!code highlight]
from pydantic import BaseModel


class ResponseSafety(BaseModel):
    """Evaluate a response as safe or unsafe."""
    evaluation: Literal["safe", "unsafe"]


safety_model = init_chat_model("openai:gpt-6.1-sol")

@after_agent(can_jump_to=["end"])
def safety_guardrail(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    """Model-based guardrail: Use an LLM to evaluate response safety."""
    stream_writer = get_stream_writer()  # [!code highlight]
    # Get the model response
    if not state["messages"]:
        return None

    last_message = state["messages"][-1]
    if not isinstance(last_message, AIMessage):
        return None

    # Use another model to evaluate safety
    model_with_tools = safety_model.bind_tools([ResponseSafety], tool_choice="any")
    result = model_with_tools.invoke(
        [
            {
                "role": "system",
                "content": "Evaluate this AI response as generally safe or unsafe."
            },
            {
                "role": "user",
                "content": f"AI response: {last_message.text}"
            }
        ]
    )
    stream_writer(result)  # [!code highlight]

    tool_call = result.tool_calls[0]
    if tool_call["args"]["evaluation"] == "unsafe":
        last_message.content = "I cannot provide that response. Please rephrase your request."

    return None
```

We can then incorporate this middleware into our agent and include its custom stream events:

```python
from typing import Any

from langchain.agents import create_agent
from langchain.messages import AIMessageChunk, AIMessage, AnyMessage


def get_weather(city: str) -> str:
    """Get weather for a given city."""

    return f"It's always sunny in {city}!"


agent = create_agent(
    model="openai:gpt-6.1-sol",
    tools=[get_weather],
    middleware=[safety_guardrail],  # [!code highlight]
)

def _render_message_chunk(token: AIMessageChunk) -> None:
    if token.text:
        print(token.text, end="|")
    if token.tool_call_chunks:
        print(token.tool_call_chunks)


def _render_completed_message(message: AnyMessage) -> None:
    if isinstance(message, AIMessage) and message.tool_calls:
        print(f"Tool calls: {message.tool_calls}")
    if isinstance(message, ToolMessage):
        print(f"Tool response: {message.content_blocks}")


input_message = {"role": "user", "content": "What is the weather in Boston?"}
for chunk in agent.stream(
    {"messages": [input_message]},
    stream_mode=["messages", "updates", "custom"],  # [!code highlight]
    version="v2",  # [!code highlight]
):
    if chunk["type"] == "messages":  # [!code highlight]
        token, metadata = chunk["data"]  # [!code highlight]
        if isinstance(token, AIMessageChunk):
            _render_message_chunk(token)
    elif chunk["type"] == "updates":  # [!code highlight]
        for source, update in chunk["data"].items():  # [!code highlight]
            if source in ("model", "tools"):
                _render_completed_message(update["messages"][-1])
    elif chunk["type"] == "custom":  # [!code highlight]
        # access completed message in stream
        print(f"Tool calls: {chunk['data'].tool_calls}")  # [!code highlight]
```

```shell title="Output" expandable
[{'name': 'get_weather', 'args': '', 'id': 'call_je6LWgxYzuZ84mmoDalTYMJC', 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '{"', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': 'city', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '":"', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': 'Boston', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '"}', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
Tool calls: [{'name': 'get_weather', 'args': {'city': 'Boston'}, 'id': 'call_je6LWgxYzuZ84mmoDalTYMJC', 'type': 'tool_call'}]
Tool response: [{'type': 'text', 'text': "It's always sunny in Boston!"}]
The| weather| in| **|Boston|**| is| **|sun|ny|**|.|[{'name': 'ResponseSafety', 'args': '', 'id': 'call_O8VJIbOG4Q9nQF0T8ltVi58O', 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '{"', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': 'evaluation', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '":"', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': 'safe', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '"}', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
Tool calls: [{'name': 'ResponseSafety', 'args': {'evaluation': 'safe'}, 'id': 'call_O8VJIbOG4Q9nQF0T8ltVi58O', 'type': 'tool_call'}]
```

Alternatively, if you aren't able to add custom events to the stream, you can aggregate message chunks within the streaming loop:

```python
input_message = {"role": "user", "content": "What is the weather in Boston?"}
full_message = None  # [!code highlight]
for chunk in agent.stream(
    {"messages": [input_message]},
    stream_mode=["messages", "updates"],
    version="v2",  # [!code highlight]
):
    if chunk["type"] == "messages":  # [!code highlight]
        token, metadata = chunk["data"]  # [!code highlight]
        if isinstance(token, AIMessageChunk):
            _render_message_chunk(token)
            full_message = token if full_message is None else full_message + token  # [!code highlight]
            if token.chunk_position == "last":  # [!code highlight]
                if full_message.tool_calls:  # [!code highlight]
                    print(f"Tool calls: {full_message.tool_calls}")  # [!code highlight]
                full_message = None  # [!code highlight]
    elif chunk["type"] == "updates":  # [!code highlight]
        for source, update in chunk["data"].items():  # [!code highlight]
            if source == "tools":
                _render_completed_message(update["messages"][-1])
```

### Streaming with human-in-the-loop

To handle human-in-the-loop [interrupts](../Advanced%20usage/Human-in-the-loop.md), we build on the [above example](#streaming-tool-calls):

1. We configure the agent with [human-in-the-loop middleware and a checkpointer](../Advanced%20usage/Human-in-the-loop.md#configuring-interrupts)
2. We collect interrupts generated during the `"updates"` stream mode
3. We respond to those interrupts with a [command](../Advanced%20usage/Human-in-the-loop.md#responding-to-interrupts)

```python
from typing import Any

from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain.messages import AIMessage, AIMessageChunk, AnyMessage, ToolMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command, Interrupt


def get_weather(city: str) -> str:
    """Get weather for a given city."""

    return f"It's always sunny in {city}!"


checkpointer = InMemorySaver()

agent = create_agent(
    "openai:gpt-6.1-sol",
    tools=[get_weather],
    middleware=[  # [!code highlight]
        HumanInTheLoopMiddleware(interrupt_on={"get_weather": True}),  # [!code highlight]
    ],  # [!code highlight]
    checkpointer=checkpointer,  # [!code highlight]
)


def _render_message_chunk(token: AIMessageChunk) -> None:
    if token.text:
        print(token.text, end="|")
    if token.tool_call_chunks:
        print(token.tool_call_chunks)


def _render_completed_message(message: AnyMessage) -> None:
    if isinstance(message, AIMessage) and message.tool_calls:
        print(f"Tool calls: {message.tool_calls}")
    if isinstance(message, ToolMessage):
        print(f"Tool response: {message.content_blocks}")


def _render_interrupt(interrupt: Interrupt) -> None:  # [!code highlight]
    interrupts = interrupt.value  # [!code highlight]
    for request in interrupts["action_requests"]:  # [!code highlight]
        print(request["description"])  # [!code highlight]


input_message = {
    "role": "user",
    "content": (
        "Can you look up the weather in Boston and San Francisco?"
    ),
}
config = {"configurable": {"thread_id": "some_id"}}  # [!code highlight]
interrupts = []  # [!code highlight]
for chunk in agent.stream(
    {"messages": [input_message]},
    config=config,  # [!code highlight]
    stream_mode=["messages", "updates"],
    version="v2",  # [!code highlight]
):
    if chunk["type"] == "messages":  # [!code highlight]
        token, metadata = chunk["data"]  # [!code highlight]
        if isinstance(token, AIMessageChunk):
            _render_message_chunk(token)
    elif chunk["type"] == "updates":  # [!code highlight]
        for source, update in chunk["data"].items():  # [!code highlight]
            if source in ("model", "tools"):
                _render_completed_message(update["messages"][-1])
            if source == "__interrupt__":  # [!code highlight]
                interrupts.extend(update)  # [!code highlight]
                _render_interrupt(update[0])  # [!code highlight]
```

```shell title="Output" expandable
[{'name': 'get_weather', 'args': '', 'id': 'call_GOwNaQHeqMixay2qy80padfE', 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '{"ci', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': 'ty": ', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '"Bosto', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': 'n"}', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': 'get_weather', 'args': '', 'id': 'call_Ndb4jvWm2uMA0JDQXu37wDH6', 'index': 1, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '{"ci', 'id': None, 'index': 1, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': 'ty": ', 'id': None, 'index': 1, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '"San F', 'id': None, 'index': 1, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': 'ranc', 'id': None, 'index': 1, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': 'isco"', 'id': None, 'index': 1, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '}', 'id': None, 'index': 1, 'type': 'tool_call_chunk'}]
Tool calls: [{'name': 'get_weather', 'args': {'city': 'Boston'}, 'id': 'call_GOwNaQHeqMixay2qy80padfE', 'type': 'tool_call'}, {'name': 'get_weather', 'args': {'city': 'San Francisco'}, 'id': 'call_Ndb4jvWm2uMA0JDQXu37wDH6', 'type': 'tool_call'}]
Tool execution requires approval

Tool: get_weather
Args: {'city': 'Boston'}
Tool execution requires approval

Tool: get_weather
Args: {'city': 'San Francisco'}
```

We next collect a [decision](../Advanced%20usage/Human-in-the-loop.md#interrupt-decision-types) for each interrupt. Importantly, the order of decisions must match the order of actions we collected.

To illustrate, we will edit one tool call and accept the other:

```python
def _get_interrupt_decisions(interrupt: Interrupt) -> list[dict]:
    return [
        {
            "type": "edit",
            "edited_action": {
                "name": "get_weather",
                "args": {"city": "Boston, U.K."},
            },
        }
        if "boston" in request["description"].lower()
        else {"type": "approve"}
        for request in interrupt.value["action_requests"]
    ]

decisions = {}
for interrupt in interrupts:
    decisions[interrupt.id] = {
        "decisions": _get_interrupt_decisions(interrupt)
    }

decisions
```

```shell title="Output"
{
    'a96c40474e429d661b5b32a8d86f0f3e': {
        'decisions': [
            {
                'type': 'edit',
                 'edited_action': {
                     'name': 'get_weather',
                     'args': {'city': 'Boston, U.K.'}
                 }
            },
            {'type': 'approve'},
        ]
    }
}
```

We can then resume by passing a [command](../Advanced%20usage/Human-in-the-loop.md#responding-to-interrupts) into the same streaming loop:

```python
interrupts = []
for chunk in agent.stream(
    Command(resume=decisions),  # [!code highlight]
    config=config,
    stream_mode=["messages", "updates"],
    version="v2",  # [!code highlight]
):
    # Streaming loop is unchanged
    if chunk["type"] == "messages":  # [!code highlight]
        token, metadata = chunk["data"]  # [!code highlight]
        if isinstance(token, AIMessageChunk):
            _render_message_chunk(token)
    elif chunk["type"] == "updates":  # [!code highlight]
        for source, update in chunk["data"].items():  # [!code highlight]
            if source in ("model", "tools"):
                _render_completed_message(update["messages"][-1])
            if source == "__interrupt__":
                interrupts.extend(update)
                _render_interrupt(update[0])
```

```shell title="Output"
Tool response: [{'type': 'text', 'text': "It's always sunny in Boston, U.K.!"}]
Tool response: [{'type': 'text', 'text': "It's always sunny in San Francisco!"}]
-| **|Boston|**|:| It|'s| always| sunny| in| Boston|,| U|.K|.|
|-| **|San| Francisco|**|:| It|'s| always| sunny| in| San| Francisco|!|
```

### Streaming from sub-agents

When there are multiple LLMs at any point in an agent, it's often necessary to disambiguate the source of messages as they are generated.

To do this, pass a [`name`](https://reference.langchain.com/python/langchain/agents/create_agent) to each agent when creating it. This name is then available in metadata via the `lc_agent_name` key when streaming in `"messages"` mode.

Below, we update the [streaming tool calls](#streaming-tool-calls) example:

1. We replace our tool with a `call_weather_agent` tool that invokes an agent internally
2. We add a `name` to each agent
3. We specify [`subgraphs=True`](https://docs.langchain.com/oss/python/langgraph/use-subgraphs#stream-subgraph-outputs) when creating the stream
4. Our stream processing is identical to before, but we add logic to keep track of what agent is active using `create_agent`'s `name` parameter

> [!TIP]
>
> When you set a `name` on an agent, that name is also attached to any `AIMessage`s generated by that agent.

First we construct the agent:

```python
from typing import Any

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.messages import AIMessage, AnyMessage


def get_weather(city: str) -> str:
    """Get weather for a given city."""

    return f"It's always sunny in {city}!"


weather_model = init_chat_model("openai:gpt-6.1-sol")
weather_agent = create_agent(
    model=weather_model,
    tools=[get_weather],
    name="weather_agent",  # [!code highlight]
)


def call_weather_agent(query: str) -> str:
    """Query the weather agent."""
    result = weather_agent.invoke({
        "messages": [{"role": "user", "content": query}]
    })
    return result["messages"][-1].text


supervisor_model = init_chat_model("openai:gpt-6.1-sol")
agent = create_agent(
    model=supervisor_model,
    tools=[call_weather_agent],
    name="supervisor",  # [!code highlight]
)
```

Next, we add logic to the streaming loop to report which agent is emitting tokens:

```python
def _render_message_chunk(token: AIMessageChunk) -> None:
    if token.text:
        print(token.text, end="|")
    if token.tool_call_chunks:
        print(token.tool_call_chunks)


def _render_completed_message(message: AnyMessage) -> None:
    if isinstance(message, AIMessage) and message.tool_calls:
        print(f"Tool calls: {message.tool_calls}")
    if isinstance(message, ToolMessage):
        print(f"Tool response: {message.content_blocks}")


input_message = {"role": "user", "content": "What is the weather in Boston?"}
current_agent = None  # [!code highlight]
for chunk in agent.stream(
    {"messages": [input_message]},
    stream_mode=["messages", "updates"],
    subgraphs=True,  # [!code highlight]
    version="v2",  # [!code highlight]
):
    if chunk["type"] == "messages":  # [!code highlight]
        token, metadata = chunk["data"]  # [!code highlight]
        if agent_name := metadata.get("lc_agent_name"):  # [!code highlight]
            if agent_name != current_agent:  # [!code highlight]
                print(f"🤖 {agent_name}: ")  # [!code highlight]
                current_agent = agent_name  # [!code highlight]
        if isinstance(token, AIMessageChunk):
            _render_message_chunk(token)
    elif chunk["type"] == "updates":  # [!code highlight]
        for source, update in chunk["data"].items():  # [!code highlight]
            if source in ("model", "tools"):
                _render_completed_message(update["messages"][-1])
```

```shell title="Output" expandable
🤖 supervisor:
[{'name': 'call_weather_agent', 'args': '', 'id': 'call_asorzUf0mB6sb7MiKfgojp7I', 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '{"', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': 'query', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '":"', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': 'Boston', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': ' weather', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': ' right', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': ' now', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': ' and', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': " today's", 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': ' forecast', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '"}', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
Tool calls: [{'name': 'call_weather_agent', 'args': {'query': "Boston weather right now and today's forecast"}, 'id': 'call_asorzUf0mB6sb7MiKfgojp7I', 'type': 'tool_call'}]
🤖 weather_agent:
[{'name': 'get_weather', 'args': '', 'id': 'call_LZ89lT8fW6w8vqck5pZeaDIx', 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '{"', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': 'city', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '":"', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': 'Boston', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '"}', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
Tool calls: [{'name': 'get_weather', 'args': {'city': 'Boston'}, 'id': 'call_LZ89lT8fW6w8vqck5pZeaDIx', 'type': 'tool_call'}]
Tool response: [{'type': 'text', 'text': "It's always sunny in Boston!"}]
Boston| weather| right| now|:| **|Sunny|**|.

|Today|'s| forecast| for| Boston|:| **|Sunny| all| day|**|.|Tool response: [{'type': 'text', 'text': 'Boston weather right now: **Sunny**.\n\nToday's forecast for Boston: **Sunny all day**.'}]
🤖 supervisor:
Boston| weather| right| now|:| **|Sunny|**|.

|Today|'s| forecast| for| Boston|:| **|Sunny| all| day|**|.|
```

## Disable streaming

In some applications you might need to disable streaming of individual tokens for a given model. This is useful when:

* Working with [multi-agent](../Advanced%20usage/Multi-agent/Multi-agent.md) systems to control which agents stream their output
* Mixing models that support streaming with those that do not
* Deploying to [LangSmith](https://docs.langchain.com/langsmith/observability.md) and wanting to prevent certain model outputs from being streamed to the client

Set `streaming=False` when initializing the model.

```python
from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    model="gpt-6.1-sol",
    streaming=False  # [!code highlight]
)
```

> [!TIP]
>
> When deploying to LangSmith, set `streaming=False` on any models whose output you don't want streamed to the client. This is configured in your graph code before deployment.

> [!NOTE]
>
> Not all chat model integrations support the `streaming` parameter. If your model doesn't support it, use `disable_streaming=True` instead. This parameter is available on all chat models via the base class.

See the [LangGraph streaming guide](https://docs.langchain.com/oss/python/langgraph/streaming.md#disable-streaming-for-specific-chat-models) for more details.

## v2 streaming format

> [!NOTE]
>
> Requires LangGraph 1.1 or later.

Pass `version="v2"` to `stream()` or `astream()` to get a unified output format. Every chunk is a `StreamPart` dict with `type`, `ns`, and `data` keys — the same shape regardless of stream mode or number of modes:

```python v2 (new)
# Unified format — no more tuple unpacking
for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
    stream_mode=["updates", "custom"],
    version="v2",
):
    print(chunk["type"])  # "updates" or "custom"
    print(chunk["data"])  # payload
```

```python v1 (current default)
# Must unpack (mode, data) tuples
for mode, chunk in agent.stream(
    {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
    stream_mode=["updates", "custom"],
):
    print(mode)   # "updates" or "custom"
    print(chunk)  # payload
```

The v2 format also improves `invoke()` — it returns a `GraphOutput` object with `.value` and `.interrupts` attributes, cleanly separating state from interrupt metadata:

```python
result = agent.invoke(
    {"messages": [{"role": "user", "content": "Hello"}]},
    version="v2",
)
print(result.value)       # state (dict, Pydantic model, or dataclass)
print(result.interrupts)  # tuple of Interrupt objects (empty if none)
```

See the [LangGraph streaming docs](https://docs.langchain.com/oss/python/langgraph/streaming.md#stream-output-format-v2) for more details on the v2 format, including type narrowing, Pydantic/dataclass coercion, and subgraph streaming.

## Related

* [Frontend streaming](../Frontend/Overview.md)—Build React UIs with [`useStream`](https://reference.langchain.com/javascript/langchain-react/index/useStream) for real-time agent interactions
* [Streaming with chat models](Models.md#stream)—Stream tokens directly from a chat model without using an agent or graph
* [Reasoning with chat models](Models.md#reasoning)—Configure and access reasoning output from chat models
* [Standard content blocks](Messages.md#standard-content-blocks)—Understand the normalized content block format used for reasoning, text, and other content types
* [Streaming with human-in-the-loop](../Advanced%20usage/Human-in-the-loop.md#streaming-with-human-in-the-loop)—Stream agent progress while handling interrupts for human review
* [LangGraph streaming](https://docs.langchain.com/oss/python/langgraph/streaming.md)—Advanced streaming options including `values`, `debug` modes, and subgraph streaming

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/streaming.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

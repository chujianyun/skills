# Configure nodes

> Add runtime configuration, retry policies, timeouts, error handling, defaults, and caching to LangGraph nodes.

[Nodes](Graph%20API%20overview.md#nodes) are the steps of a Graph API graph. This page covers how to attach runtime configuration, retries, timeouts, error handlers, defaults, and caching when you add a node. For wiring nodes into sequences, branches, and loops, see [Control flow](Build%20sequences%2C%20branches%2C%20and%20loops.md). For the full retry, timeout, and error lifecycle, see [Fault tolerance](../Capabilities/Fault%20tolerance.md).

## Add runtime configuration

Pass values into a run (for example, which LLM or system prompt to use) without putting those values in graph state.

To add runtime configuration:

1. Specify a schema for your configuration
2. Add the configuration to the function signature for nodes or conditional edges
3. Pass the configuration into the graph

See below for a simple example:

```python
from langgraph.graph import END, StateGraph, START
from langgraph.runtime import Runtime
from typing_extensions import TypedDict

# 1. Specify config schema
class ContextSchema(TypedDict):
    my_runtime_value: str

# 2. Define a graph that accesses the config in a node
class State(TypedDict):
    my_state_value: int

def node(state: State, runtime: Runtime[ContextSchema]):  # [!code highlight]
    if runtime.context["my_runtime_value"] == "a":  # [!code highlight]
        return {"my_state_value": 1}
    elif runtime.context["my_runtime_value"] == "b":  # [!code highlight]
        return {"my_state_value": 2}
    else:
        raise ValueError("Unknown values.")

builder = StateGraph(State, context_schema=ContextSchema)  # [!code highlight]
builder.add_node(node)
builder.add_edge(START, "node")
builder.add_edge("node", END)

graph = builder.compile()

# 3. Pass in configuration at runtime:
print(graph.invoke({}, context={"my_runtime_value": "a"}))  # [!code highlight]
print(graph.invoke({}, context={"my_runtime_value": "b"}))  # [!code highlight]
```

```
{'my_state_value': 1}
{'my_state_value': 2}
```

> [accordion] Extended example: specifying LLM at runtime
>
> Choose OpenAI or Anthropic at invoke time. These examples call live providers and need API keys.
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from dataclasses import dataclass
>
> from langchain.chat_models import init_chat_model
> from langgraph.graph import MessagesState, END, StateGraph, START
> from langgraph.runtime import Runtime
>
> @dataclass
> class ContextSchema:
>     model_provider: str = "anthropic"
>
> MODELS = {
>     "anthropic": init_chat_model("claude-haiku-4-5-20251001"),
>     "openai": init_chat_model("gpt-5.4-mini"),
> }
>
> def call_model(state: MessagesState, runtime: Runtime[ContextSchema]):
>     model = MODELS[runtime.context.model_provider]
>     response = model.invoke(state["messages"])
>     return {"messages": [response]}
>
> builder = StateGraph(MessagesState, context_schema=ContextSchema)
> builder.add_node("model", call_model)
> builder.add_edge(START, "model")
> builder.add_edge("model", END)
>
> graph = builder.compile()
>
> # Usage
> input_message = {"role": "user", "content": "hi"}
> # With no configuration, uses default (Anthropic)
> response_1 = graph.invoke({"messages": [input_message]}, context=ContextSchema())["messages"][-1]
> # Or, can set OpenAI
> response_2 = graph.invoke({"messages": [input_message]}, context={"model_provider": "openai"})["messages"][-1]
>
> print(response_1.response_metadata["model_name"])
> print(response_2.response_metadata["model_name"])
> ```
>
> ```
> claude-haiku-4-5-20251001
> gpt-5.4-mini
> ```

> [accordion] Extended example: specifying model and system message at runtime
>
> Configure both the model provider and a system message at invoke time. These examples call live providers and need API keys.
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from dataclasses import dataclass
> from langchain.chat_models import init_chat_model
> from langchain.messages import SystemMessage
> from langgraph.graph import END, MessagesState, StateGraph, START
> from langgraph.runtime import Runtime
>
> @dataclass
> class ContextSchema:
>     model_provider: str = "anthropic"
>     system_message: str | None = None
>
> MODELS = {
>     "anthropic": init_chat_model("claude-haiku-4-5-20251001"),
>     "openai": init_chat_model("gpt-5.4-mini"),
> }
>
> def call_model(state: MessagesState, runtime: Runtime[ContextSchema]):
>     model = MODELS[runtime.context.model_provider]
>     messages = state["messages"]
>     if (system_message := runtime.context.system_message):
>         messages = [SystemMessage(system_message)] + messages
>     response = model.invoke(messages)
>     return {"messages": [response]}
>
> builder = StateGraph(MessagesState, context_schema=ContextSchema)
> builder.add_node("model", call_model)
> builder.add_edge(START, "model")
> builder.add_edge("model", END)
>
> graph = builder.compile()
>
> # Usage
> input_message = {"role": "user", "content": "hi"}
> response = graph.invoke({"messages": [input_message]}, context={"model_provider": "openai", "system_message": "Respond in Italian."})
> for message in response["messages"]:
>     message.pretty_print()
> ```
>
> ```
> ================================ Human Message ================================
>
> hi
> ================================== Ai Message ==================================
>
> Ciao! Come posso aiutarti oggi?
> ```

## Add retry policies

Attach a retry policy when a node calls an API, database, or LLM that can fail transiently.

Pass `retry_policy` to [`add_node`](https://reference.langchain.com/python/langgraph/graph/state/StateGraph/add_node). The value is a `RetryPolicy` named tuple. This example uses the defaults:

```python
from langgraph.types import RetryPolicy

builder.add_node(
    "node_name",
    node_function,
    retry_policy=RetryPolicy(),
)
```

By default, `retry_on` uses `default_retry_on`, which retries any exception except:

* `ValueError`
* `TypeError`
* `ArithmeticError`
* `ImportError`
* `LookupError`
* `NameError`
* `SyntaxError`
* `RuntimeError`
* `ReferenceError`
* `StopIteration`
* `StopAsyncIteration`
* `OSError`

For exceptions from popular HTTP libraries such as `requests` and `httpx`, it only retries on 5xx status codes. See [Fault tolerance](../Capabilities/Fault%20tolerance.md#retries) for the full default list and parameters.

> [accordion] Extended example: customizing retry policies
>
> These snippets show how to attach different retry policies. They do not create database tables or invoke the graph.
>
> Pass different retry policies to a model node and a SQL node:
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import sqlite3
> from langchain.chat_models import init_chat_model
> from langgraph.graph import END, MessagesState, StateGraph, START
> from langgraph.types import RetryPolicy
> from langchain.messages import AIMessage
>
> con = sqlite3.connect(":memory:")
> model = init_chat_model("claude-haiku-4-5-20251001")
>
> def query_database(state: MessagesState):
>     cursor = con.cursor()
>     cursor.execute("SELECT * FROM Artist LIMIT 10;")
>     query_result = str(cursor.fetchall())
>     return {"messages": [AIMessage(content=query_result)]}
>
> def call_model(state: MessagesState):
>     response = model.invoke(state["messages"])
>     return {"messages": [response]}
>
> # Define a new graph
> builder = StateGraph(MessagesState)
> builder.add_node(
>     "query_database",
>     query_database,
>     retry_policy=RetryPolicy(retry_on=sqlite3.OperationalError),
> )
> builder.add_node("model", call_model, retry_policy=RetryPolicy(max_attempts=5))
> builder.add_edge(START, "model")
> builder.add_edge("model", "query_database")
> builder.add_edge("query_database", END)
> graph = builder.compile()
> ```

## Set node timeouts

> [!NOTE]
>
> Requires `langgraph>=1.2`.

Pass `timeout` to [`add_node`](https://reference.langchain.com/python/langgraph/graph/state/StateGraph/add_node) to cap how long a single async node attempt may run. Use a number (seconds), a `datetime.timedelta`, or a [`TimeoutPolicy`](https://reference.langchain.com/python/langgraph/types/TimeoutPolicy) for separate run and idle limits:

```python
import asyncio
from typing_extensions import TypedDict

from langgraph.errors import NodeTimeoutError
from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    value: str


async def call_model(state: State) -> State:
    await asyncio.sleep(2)
    return {"value": "done"}


builder = StateGraph(State)
builder.add_node("model", call_model, timeout=1.0)
# Or: timeout=TimeoutPolicy(run_timeout=120, idle_timeout=30)
builder.add_edge(START, "model")
builder.add_edge("model", END)
graph = builder.compile()


async def main():
    try:
        await graph.ainvoke({"value": "start"})
    except NodeTimeoutError:
        print("Node timed out")


asyncio.run(main())
```

Node timeouts apply only to **async** nodes. Setting `timeout` on a sync node fails at compile time, because sync Python execution cannot be safely canceled in-process. For separate run and idle limits, pass a [`TimeoutPolicy`](https://reference.langchain.com/python/langgraph/types/TimeoutPolicy).

When a node exceeds its timeout, LangGraph raises [`NodeTimeoutError`](https://reference.langchain.com/python/langgraph/errors/NodeTimeoutError). It does **not** subclass built-in `TimeoutError` (an `OSError` subclass), so the default retry policy treats it as retryable when a `retry_policy` is set. The timeout applies to each attempt independently, so the timer resets for every retry. Timed-out attempts do not commit buffered writes.

See [Fault tolerance](../Capabilities/Fault%20tolerance.md#timeouts) for the full timeout lifecycle, idle-timeout refresh sources, and `runtime.heartbeat()`.

## Handle node errors

> [!NOTE]
>
> Requires `langgraph>=1.2`.

Pass `error_handler` to [`add_node`](https://reference.langchain.com/python/langgraph/graph/state/StateGraph/add_node) to run a function after a node fails and all retries are exhausted. The handler receives the current state and a typed [`NodeError`](https://reference.langchain.com/python/langgraph/errors/NodeError), and can route to a recovery branch via [`Command`](https://reference.langchain.com/python/langgraph/types/Command):

```python
from langgraph.errors import NodeError
from langgraph.types import Command, RetryPolicy

def payment_error_handler(state: State, error: NodeError) -> Command:
    return Command(
        update={"status": f"compensated: {error.error}"},
        goto="finalize",
    )

builder.add_node(
    "charge_payment",
    charge_payment,
    retry_policy=RetryPolicy(max_attempts=3, retry_on=ConnectionError),
    error_handler=payment_error_handler,
)
```

See [Fault tolerance](../Capabilities/Fault%20tolerance.md#error-handling) for a full runnable example, compensation patterns, and `Command` routing.

## Set graph-wide node defaults

> [!NOTE]
>
> Requires `langgraph>=1.2`.

Use [`set_node_defaults`](https://reference.langchain.com/python/langgraph/graph/state/StateGraph/set_node_defaults) to set `retry_policy`, `timeout`, `cache_policy`, or `error_handler` once for every node in a graph, instead of repeating them on each [`add_node`](https://reference.langchain.com/python/langgraph/graph/state/StateGraph/add_node) call. Per-node values always win, and defaults are applied at [`StateGraph.compile`](https://reference.langchain.com/python/langgraph/graph/state/StateGraph/compile) time:

```python
from langgraph.types import RetryPolicy, TimeoutPolicy

graph = (
    StateGraph(State)
    .set_node_defaults(
        retry_policy=RetryPolicy(max_attempts=3),
        timeout=TimeoutPolicy(run_timeout=30),
        error_handler=fallback_handler,
    )
    .add_node("a", node_a)
    .add_node("b", node_b, retry_policy=RetryPolicy(max_attempts=5))  # overrides default
    .add_edge(START, "a")
    .compile()
)
```

`retry_policy` and `timeout` defaults apply to every node, including error-handler nodes. `cache_policy` and `error_handler` defaults apply only to regular nodes—handlers never catch themselves, and caching a handler result is unsafe. Defaults are not inherited by subgraphs.

See [Fault tolerance](../Capabilities/Fault%20tolerance.md#graph-defaults) for the full precedence rules and applicability table.

## Access execution info inside a node

Access execution identity and retry information via `runtime.execution_info`. This surfaces thread, run, and checkpoint identifiers as well as retry state, without reading from `config` directly.

| Attribute | Type | Description |
| - | - | - |
| `thread_id` | `str \| None` | Thread ID for the current execution. `None` without a checkpointer. |
| `run_id` | `str \| None` | Run ID for the current execution. `None` when not provided in config. |
| `checkpoint_id` | `str` | Checkpoint ID for the current execution. |
| `checkpoint_ns` | `str` | Checkpoint namespace for the current execution. |
| `task_id` | `str` | Task ID for the current execution. |
| `node_attempt` | `int` | Current execution attempt number (1-indexed). `1` on the first try, `2` on the first retry, etc. |
| `node_first_attempt_time` | `float \| None` | Unix timestamp (seconds) of when the first attempt started. Stays the same across retries. |

#### Access thread and run IDs

Use `execution_info` to access the thread ID, run ID, and other identity fields inside a node:

```python
from langgraph.graph import StateGraph, START, END
from langgraph.runtime import Runtime
from typing_extensions import TypedDict

class State(TypedDict):
    result: str

def my_node(state: State, runtime: Runtime):
    info = runtime.execution_info
    if info is None:
        return {"result": "done"}
    print(f"Thread: {info.thread_id}, Run: {info.run_id}")  # [!code highlight]
    return {"result": "done"}

builder = StateGraph(State)
builder.add_node("my_node", my_node)
builder.add_edge(START, "my_node")
builder.add_edge("my_node", END)
graph = builder.compile()
```

#### Adjust behavior based on retry state

When a node has a retry policy, use `execution_info` to inspect the current attempt number and switch to a fallback after the first attempt fails:

```python
from langgraph.graph import StateGraph, START, END
from langgraph.runtime import Runtime
from langgraph.types import RetryPolicy
from typing_extensions import TypedDict

class State(TypedDict):
    result: str

def my_node(state: State, runtime: Runtime):
    info = runtime.execution_info
    if info is not None and info.node_attempt > 1:  # [!code highlight]
        # use a fallback on retries
        return {"result": call_fallback_api()}
    return {"result": call_primary_api()}

builder = StateGraph(State)
builder.add_node("my_node", my_node, retry_policy=RetryPolicy(max_attempts=3))
builder.add_edge(START, "my_node")
builder.add_edge("my_node", END)
graph = builder.compile()
```

`execution_info` is set once the node task is prepared. Even without a retry policy, `node_attempt` defaults to `1`, and `node_first_attempt_time` is set when the node starts executing.

## Access server info inside a node

When your graph runs on LangGraph Server, you can access server-specific metadata via `runtime.server_info`. This surfaces the assistant ID, graph ID, and authenticated user without reading config metadata or configurable keys directly.

| Attribute | Type | Description |
| - | - | - |
| `assistant_id` | `str` | The assistant ID for the current deployment. |
| `graph_id` | `str` | The graph ID for the current deployment. |
| `user` | `BaseUser \| None` | The authenticated user, if [custom auth](https://docs.langchain.com/langsmith/custom-auth.md) is configured. |

```python
from langgraph.graph import StateGraph, START, END
from langgraph.runtime import Runtime
from typing_extensions import TypedDict

class State(TypedDict):
    result: str

def my_node(state: State, runtime: Runtime):
    server = runtime.server_info
    if server is not None:
        print(f"Assistant: {server.assistant_id}, Graph: {server.graph_id}")  # [!code highlight]
        if server.user is not None:
            print(f"User: {server.user.identity}")
    return {"result": "done"}

builder = StateGraph(State)
builder.add_node("my_node", my_node)
builder.add_edge(START, "my_node")
builder.add_edge("my_node", END)
graph = builder.compile()
```

`server_info` is `None` when the graph is not running on LangGraph Server (for example, during local development or testing).

> [!NOTE]
>
> Requires `langgraph>=1.1.5`.

## Access drain state inside a node

When a [graceful shutdown](../Capabilities/Fault%20tolerance.md#graceful-shutdown) has been requested, `runtime.drain_requested` is `True`. Read this inside a node to skip expensive work before the next superstep boundary:

```python
from langgraph.runtime import Runtime

def my_node(state: State, runtime: Runtime) -> State:
    if runtime.drain_requested:  # [!code highlight]
        return {"status": "skipped", "reason": runtime.drain_reason}
    return {"status": do_work()}
```

| Property | Type | Description |
| - | - | - |
| `drain_requested` | `bool` | `True` if `RunControl.request_drain()` has been called for this run. |
| `drain_reason` | `str \| None` | The reason string passed to `request_drain()`, or `None` if drain was not requested. |

> [!NOTE]
>
> Requires `langgraph>=1.2`. See [Graceful shutdown](../Capabilities/Fault%20tolerance.md#graceful-shutdown) for the full `RunControl` API.

## Add node caching

Use node caching when a step is expensive and you want to reuse results for the same input.

To enable caching:

1. Pass a cache when you compile the graph (for example, `InMemoryCache`). `SqliteCache` is also available in Python.
2. Attach a [`CachePolicy`](https://reference.langchain.com/python/langgraph/types/CachePolicy) on the node.

[`CachePolicy`](https://reference.langchain.com/python/langgraph/types/CachePolicy) options:

* **`key_func`**: Function that builds a cache key from the node input. Defaults to a hash of the input (via pickle).
* **`ttl`**: Time to live in seconds. When omitted, the cache entry does not expire.

```python
import time

from typing_extensions import TypedDict

from langgraph.cache.memory import InMemoryCache
from langgraph.graph import END, START, StateGraph
from langgraph.types import CachePolicy


class State(TypedDict):
    x: int
    result: int


def expensive_node(state: State) -> dict[str, int]:
    # Expensive computation
    time.sleep(2)
    return {"result": state["x"] * 2}


builder = StateGraph(State)
builder.add_node("expensive_node", expensive_node, cache_policy=CachePolicy(ttl=3))
builder.add_edge(START, "expensive_node")
builder.add_edge("expensive_node", END)

graph = builder.compile(cache=InMemoryCache())

print(graph.invoke({"x": 5}, stream_mode="updates"))  # [!code highlight]
# [{'expensive_node': {'result': 10}}]
print(graph.invoke({"x": 5}, stream_mode="updates"))  # [!code highlight]
# [{'expensive_node': {'result': 10}, '__metadata__': {'cached': True}}]
```

The first run takes about two seconds because of the mocked work. The second run returns from the cache.

You can also set `cache_policy` (and other node options) once for the graph with [`set_node_defaults`](https://reference.langchain.com/python/langgraph/graph/state/StateGraph/set_node_defaults). See [Set graph-wide node defaults](#set-graph-wide-node-defaults).

## See also

* [Graph API](Graph%20API%20overview.md#nodes)
* [Control flow](Build%20sequences%2C%20branches%2C%20and%20loops.md)
* [Fault tolerance](../Capabilities/Fault%20tolerance.md)
* [Define and update state](Define%20and%20update%20state.md)

# LangGraph runtime

[`Pregel`](https://reference.langchain.com/python/langgraph/pregel/main/Pregel) implements LangGraph's runtime, managing the execution of LangGraph applications.

Compiling a [StateGraph](https://reference.langchain.com/python/langgraph/graph/state/StateGraph) or creating an [`@entrypoint`](https://reference.langchain.com/python/langgraph/func/entrypoint) produces a [`Pregel`](https://reference.langchain.com/python/langgraph/pregel/main/Pregel) instance that can be invoked with input.

This guide explains the runtime at a high level and provides instructions for directly implementing applications with Pregel.

> **Note:** The [`Pregel`](https://reference.langchain.com/python/langgraph/pregel/main/Pregel) runtime is named after [Google's Pregel algorithm](https://research.google/pubs/pub37252/), which describes an efficient method for large-scale parallel computation using graphs.

## Overview

In LangGraph, Pregel combines [**actors**](https://en.wikipedia.org/wiki/Actor_model) and **channels** into a single application. **Actors** read data from channels and write data to channels. Pregel organizes the execution of the application into multiple steps, following the **Pregel Algorithm**/**Bulk Synchronous Parallel** model.

Each step consists of three phases:

* **Plan**: Determine which **actors** to execute in this step. For example, in the first step, select the **actors** that subscribe to the special **input** channels; in subsequent steps, select the **actors** that subscribe to channels updated in the previous step.
* **Execution**: Execute all selected **actors** in parallel, until all complete, or one fails, or a timeout is reached. During this phase, channel updates are invisible to actors until the next step.
* **Update**: Update the channels with the values written by the **actors** in this step.

Repeat until no **actors** are selected for execution, or a maximum number of steps is reached.

## Actors

An **actor** is a `PregelNode`. It subscribes to channels, reads data from them, and writes data to them. It can be thought of as an **actor** in the Pregel algorithm. `PregelNodes` implement LangChain's Runnable interface.

## Channels

Channels are used to communicate between actors (PregelNodes). Each channel has a value type, an update type, and an update function—which takes a sequence of updates and modifies the stored value. Channels can be used to send data from one chain to another, or to send data from a chain to itself in a future step.

### LastValue

[`LastValue`](https://reference.langchain.com/python/langgraph/channels/last_value/LastValue) is the default channel type. It stores the last value written to it, overwriting any previous value. Use it for input and output values, or for passing data from one step to the next.

```python
from langgraph.channels import LastValue

channel: LastValue[int] = LastValue(int)
```

### Topic

[`Topic`](https://reference.langchain.com/python/langgraph/channels/topic/Topic) is a configurable PubSub channel useful for sending multiple values between actors or accumulating output across steps. It can be configured to deduplicate values or to accumulate all values written during a run.

```python
from langgraph.channels import Topic

# Accumulate all values written across steps
channel: Topic[str] = Topic(str, accumulate=True)
```

### BinaryOperatorAggregate

[`BinaryOperatorAggregate`](https://reference.langchain.com/python/langgraph/channels/binop/BinaryOperatorAggregate) stores a persistent value that is updated by applying a binary operator to the current value and each new update. Use it to compute running aggregates across steps.

```python
import operator
from langgraph.channels import BinaryOperatorAggregate

# Running total: each write adds to the current value
total = BinaryOperatorAggregate(int, operator.add)
```

### DeltaChannel

> [!WARNING]
>
> `DeltaChannel` requires `langgraph>=1.2` and is currently in **beta**. The API may change in future releases.

[`DeltaChannel`](https://reference.langchain.com/python/langgraph/channels/delta/DeltaChannel) stores only the incremental delta at each step rather than the full accumulated value. This is most useful for channels that are written frequently and accumulate large values over time—for example, a conversation message list in a long-running thread. Without delta storage, the full list is re-serialized into every checkpoint; with `DeltaChannel`, only the new messages written at each step are stored.

> [!TIP]
>
> Consider `DeltaChannel` when a channel is both written to frequently and grows large over time. A good signal: if you notice checkpoint sizes growing linearly with thread length for a particular channel, `DeltaChannel` is likely a good fit.

Use `DeltaChannel` in an `Annotated` type annotation the same way you would use a plain reducer:

```python
from typing import Annotated, Sequence
from typing_extensions import TypedDict
from langgraph.channels import DeltaChannel


def my_reducer(state: list[str], writes: Sequence[list[str]]) -> list[str]:
    result = list(state)
    for write in writes:
        result.extend(write)
    return result


class State(TypedDict):
    messages: Annotated[list[str], DeltaChannel(my_reducer)]
```

#### Bulk reducer requirement

The `reducer` passed to `DeltaChannel` is a **bulk reducer**: it receives the current state and a *sequence* of all writes from the current step in a single call—not pairwise like a standard reducer. This differs from the per-key reducers used with `Annotated` in a `StateGraph`, where the reducer is called once per update.

> [!WARNING]
>
> The bulk reducer **must be associative** (batching-invariant):
>
> ```
> reducer(reducer(state, [xs]), [ys]) == reducer(state, [xs, ys])
> ```
>
> If your reducer is not associative, the reconstructed state may differ depending on how LangGraph batches writes across steps, producing inconsistent behavior.

> [!WARNING]
>
> **The reducer runs on reconstruction, not on write.** Unlike a [`BinaryOperatorAggregate`](https://reference.langchain.com/python/langgraph/channels/binop/BinaryOperatorAggregate), whose reducer is invoked at write time so the combined value is what gets serialized into the checkpoint, a `DeltaChannel` reducer is invoked when the channel value is *rebuilt* from its persisted writes. The raw per-step writes are what get serialized; the reducer is only called when the value is materialized—on the next read, on the next step's actors, or when replaying history.
>
> Practical consequences when designing a reducer:
>
> * **Make it a pure function of `(state, writes)`.** Any side effects, randomness, or wall-clock reads (e.g., `uuid.uuid4()`, `datetime.now()`) execute every time the value is reconstructed and produce different results on each replay. They are *not* baked into the persisted writes.
> * **Do not rely on mutations to incoming writes being persisted.** If your reducer mutates a write object (for example, assigning a stable ID to an item that arrived without one), that mutation lives only in the reconstructed value. The stored write still has the original shape, so the next reconstruction will see the un-mutated input again.
> * **Attach identity and other stable metadata upstream.** If downstream code needs to reference an item by ID across turns (e.g., to update or remove it later), assign that ID before the value is written to the channel—not inside the reducer.

Here are bulk reducers for the two most common cases:

```python
from typing import Any, Sequence


# List: append all writes in order
def list_reducer(state: list[Any], writes: Sequence[list[Any]]) -> list[Any]:
    result = list(state)
    for write in writes:
        result.extend(write)
    return result


# Dict: merge all writes, last write wins on key conflicts
def dict_reducer(
    state: dict[str, Any], writes: Sequence[dict[str, Any]]
) -> dict[str, Any]:
    result = dict(state)
    for write in writes:
        result.update(write)
    return result
```

Both are associative: applying batches one at a time produces the same result as applying them together.

#### Use snapshot\_frequency for bounded read latency

Without snapshots, reading a `DeltaChannel` value requires replaying the full write history—O(N) for a thread with N steps. Setting `snapshot_frequency=K` writes a full snapshot every K pregel steps, bounding read depth to at most K steps:

```python
class State(TypedDict):
    messages: Annotated[
        list[str],
        DeltaChannel(my_reducer, snapshot_frequency=5),
    ]
```

Higher values of `snapshot_frequency` reduce storage overhead but increase read latency. Lower values bound latency more tightly at the cost of larger checkpoints. `None` (the default) skips snapshots entirely—appropriate when reads are rare or threads are short.

#### Version compatibility and rollbacks

> [!WARNING]
>
> Changing a persisted channel from `DeltaChannel` to a non-delta channel is not recommended. Checkpoints encode these channel types differently, so changing the type for an existing thread can cause incomplete or incorrect state reconstruction. Keep channel definitions stable for the lifetime of a thread. Before changing a channel type, migrate affected threads to the new representation, or discard them and start new threads.
>
> **Rolling back to a version without `DeltaChannel` support is not supported.** `langgraph>=1.2` writes delta channel checkpoints in a new format that earlier versions cannot read. Once a thread has used `DeltaChannel`, downgrading LangGraph leaves those checkpoints unreadable as older runtimes do not understand the delta format and cannot reconstruct channel state. If you need to roll back, use the [delta-channel-dump recovery script](https://github.com/langchain-ai/langgraph/tree/main/examples/delta-channel-dump) to migrate affected threads, or discard them, before downgrading.

## Examples

While most users will interact with Pregel through the [StateGraph](https://reference.langchain.com/python/langgraph/graph/state/StateGraph) API or the [`@entrypoint`](https://reference.langchain.com/python/langgraph/func/entrypoint) decorator, it is possible to interact with Pregel directly.

Below are a few different examples to give you a sense of the Pregel API.

> [tab] Single node
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langgraph.channels import EphemeralValue
> from langgraph.pregel import Pregel, NodeBuilder
>
> node1 = (
>     NodeBuilder().subscribe_only("a")
>     .do(lambda x: x + x)
>     .write_to("b")
> )
>
> app = Pregel(
>     nodes={"node1": node1},
>     channels={
>         "a": EphemeralValue(str),
>         "b": EphemeralValue(str),
>     },
>     input_channels=["a"],
>     output_channels=["b"],
> )
>
> app.invoke({"a": "foo"})
> ```
>
> ```con theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> {'b': 'foofoo'}
> ```

> [tab] Multiple nodes
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langgraph.channels import LastValue, EphemeralValue
> from langgraph.pregel import Pregel, NodeBuilder
>
> node1 = (
>     NodeBuilder().subscribe_only("a")
>     .do(lambda x: x + x)
>     .write_to("b")
> )
>
> node2 = (
>     NodeBuilder().subscribe_only("b")
>     .do(lambda x: x + x)
>     .write_to("c")
> )
>
>
> app = Pregel(
>     nodes={"node1": node1, "node2": node2},
>     channels={
>         "a": EphemeralValue(str),
>         "b": LastValue(str),
>         "c": EphemeralValue(str),
>     },
>     input_channels=["a"],
>     output_channels=["b", "c"],
> )
>
> app.invoke({"a": "foo"})
> ```
>
> ```con theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> {'b': 'foofoo', 'c': 'foofoofoofoo'}
> ```

> [tab] Topic
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langgraph.channels import EphemeralValue, Topic
> from langgraph.pregel import Pregel, NodeBuilder
>
> node1 = (
>     NodeBuilder().subscribe_only("a")
>     .do(lambda x: x + x)
>     .write_to("b", "c")
> )
>
> node2 = (
>     NodeBuilder().subscribe_to("b")
>     .do(lambda x: x["b"] + x["b"])
>     .write_to("c")
> )
>
> app = Pregel(
>     nodes={"node1": node1, "node2": node2},
>     channels={
>         "a": EphemeralValue(str),
>         "b": EphemeralValue(str),
>         "c": Topic(str, accumulate=True),
>     },
>     input_channels=["a"],
>     output_channels=["c"],
> )
>
> app.invoke({"a": "foo"})
> ```
>
> ```pycon theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> {'c': ['foofoo', 'foofoofoofoo']}
> ```

> [tab] BinaryOperatorAggregate
>
> This example demonstrates how to use the [`BinaryOperatorAggregate`](https://reference.langchain.com/python/langgraph/channels/binop/BinaryOperatorAggregate) channel to implement a reducer.
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langgraph.channels import EphemeralValue, BinaryOperatorAggregate
> from langgraph.pregel import Pregel, NodeBuilder
>
>
> node1 = (
>     NodeBuilder().subscribe_only("a")
>     .do(lambda x: x + x)
>     .write_to("b", "c")
> )
>
> node2 = (
>     NodeBuilder().subscribe_only("b")
>     .do(lambda x: x + x)
>     .write_to("c")
> )
>
> def reducer(current, update):
>     if current:
>         return current + " | " + update
>     else:
>         return update
>
> app = Pregel(
>     nodes={"node1": node1, "node2": node2},
>     channels={
>         "a": EphemeralValue(str),
>         "b": EphemeralValue(str),
>         "c": BinaryOperatorAggregate(str, operator=reducer),
>     },
>     input_channels=["a"],
>     output_channels=["c"],
> )
>
> app.invoke({"a": "foo"})
> ```
>
> ```console theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> { 'c': 'foofoo | foofoofoofoo' }
> ```

> [tab] Cycle
>
> This example demonstrates how to introduce a cycle in the graph, by having
> a chain write to a channel it subscribes to. The node doubles the string
> until its length is at least 10, then writes an empty list. Because
> `Topic` clears between steps when it receives no new values, the channel
> becomes empty and the cycle ends.
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langgraph.channels import Topic
> from langgraph.pregel import Pregel, NodeBuilder
>
> example_node = (
>     NodeBuilder().subscribe_only("value")
>     .do(lambda xs: xs[0] + xs[0] if len(xs[0]) < 10 else [])
>     .write_to("value")
> )
>
> app = Pregel(
>     nodes={"example_node": example_node},
>     channels={
>         "value": Topic(str, accumulate=False),
>     },
>     input_channels=["value"],
>     output_channels=["value"],
> )
>
> app.invoke({"value": "a"})
> ```
>
> ```pycon theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> {'value': ['aaaaaaaaaaaaaaaa']}
> ```

## High-level API

LangGraph provides two high-level APIs for creating a Pregel application: the [StateGraph (Graph API)](../Build%20with%20the%20Graph%20API/Graph%20API%20overview.md) and the [Functional API](Build%20with%20the%20Functional%20API/Functional%20API%20overview.md).

> [tab] StateGraph (Graph API)
>
> The [StateGraph (Graph API)](https://reference.langchain.com/python/langgraph/graph/state/StateGraph) is a higher-level abstraction that simplifies the creation of Pregel applications. It allows you to define a graph of nodes and edges. When you compile the graph, the StateGraph API automatically creates the Pregel application for you.
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from typing import TypedDict
>
> from langgraph.constants import START
> from langgraph.graph import StateGraph
>
> class Essay(TypedDict):
>     topic: str
>     content: str | None
>     score: float | None
>
> def write_essay(essay: Essay):
>     return {
>         "content": f"Essay about {essay['topic']}",
>     }
>
> def score_essay(essay: Essay):
>     return {
>         "score": 10
>     }
>
> builder = StateGraph(Essay)
> builder.add_node(write_essay)
> builder.add_node(score_essay)
> builder.add_edge(START, "write_essay")
> builder.add_edge("write_essay", "score_essay")
>
> # Compile the graph.
> # This will return a Pregel instance.
> graph = builder.compile()
> ```
>
> The compiled Pregel instance will be associated with a list of nodes and channels. You can inspect the nodes and channels by printing them.
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> print(graph.nodes)
> ```
>
> You will see something like this:
>
> ```pycon theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> {'__start__': <langgraph.pregel.read.PregelNode at 0x7d05e3ba1810>,
>  'write_essay': <langgraph.pregel.read.PregelNode at 0x7d05e3ba14d0>,
>  'score_essay': <langgraph.pregel.read.PregelNode at 0x7d05e3ba1710>}
> ```
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> print(graph.channels)
> ```
>
> You should see something like this
>
> ```pycon theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> {'topic': <langgraph.channels.last_value.LastValue at 0x7d05e3294d80>,
>  'content': <langgraph.channels.last_value.LastValue at 0x7d05e3295040>,
>  'score': <langgraph.channels.last_value.LastValue at 0x7d05e3295980>,
>  '__start__': <langgraph.channels.ephemeral_value.EphemeralValue at 0x7d05e3297e00>,
>  'write_essay': <langgraph.channels.ephemeral_value.EphemeralValue at 0x7d05e32960c0>,
>  'score_essay': <langgraph.channels.ephemeral_value.EphemeralValue at 0x7d05e2d8ab80>,
>  'branch:__start__:__self__:write_essay': <langgraph.channels.ephemeral_value.EphemeralValue at 0x7d05e32941c0>,
>  'branch:__start__:__self__:score_essay': <langgraph.channels.ephemeral_value.EphemeralValue at 0x7d05e2d88800>,
>  'branch:write_essay:__self__:write_essay': <langgraph.channels.ephemeral_value.EphemeralValue at 0x7d05e3295ec0>,
>  'branch:write_essay:__self__:score_essay': <langgraph.channels.ephemeral_value.EphemeralValue at 0x7d05e2d8ac00>,
>  'branch:score_essay:__self__:write_essay': <langgraph.channels.ephemeral_value.EphemeralValue at 0x7d05e2d89700>,
>  'branch:score_essay:__self__:score_essay': <langgraph.channels.ephemeral_value.EphemeralValue at 0x7d05e2d8b400>,
>  'start:write_essay': <langgraph.channels.ephemeral_value.EphemeralValue at 0x7d05e2d8b280>}
> ```

> [tab] Functional API
>
> In the [Functional API](Build%20with%20the%20Functional%20API/Functional%20API%20overview.md), you can use an [`@entrypoint`](https://reference.langchain.com/python/langgraph/func/entrypoint) to create a Pregel application. The `entrypoint` decorator allows you to define a function that takes input and returns output.
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from typing import TypedDict
>
> from langgraph.checkpoint.memory import InMemorySaver
> from langgraph.func import entrypoint
>
> class Essay(TypedDict):
>     topic: str
>     content: str | None
>     score: float | None
>
>
> checkpointer = InMemorySaver()
>
> @entrypoint(checkpointer=checkpointer)
> def write_essay(essay: Essay):
>     return {
>         "content": f"Essay about {essay['topic']}",
>     }
>
> print("Nodes: ")
> print(write_essay.nodes)
> print("Channels: ")
> print(write_essay.channels)
> ```
>
> ```pycon theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> Nodes:
> {'write_essay': <langgraph.pregel.read.PregelNode object at 0x7d05e2f9aad0>}
> Channels:
> {'__start__': <langgraph.channels.ephemeral_value.EphemeralValue object at 0x7d05e2c906c0>, '__end__': <langgraph.channels.last_value.LastValue object at 0x7d05e2c90c40>, '__previous__': <langgraph.channels.last_value.LastValue object at 0x7d05e1007280>}
> ```

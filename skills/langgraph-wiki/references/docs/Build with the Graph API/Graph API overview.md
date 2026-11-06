# Graph API overview

> Learn how LangGraph models agent workflows as graphs of shared state, nodes, and edges.

The Graph API defines agent workflows as a graph of [state](#state), [nodes](#nodes), and [edges](#edges). [`Send`](#send) and [`Command`](#command) control how the graph runs work: `Send` dynamically invokes nodes for fan-out, and `Command` updates state while routing to the next node (including resume after an interrupt). Use the Graph API when you want explicit shared state and a visual control flow.

For step-by-step decisions while building, see the [Build checklist for the Graph API](Build%20checklist%20for%20the%20Graph%20API.md). For a guided walkthrough, see [Thinking in the Graph API](Thinking%20in%20the%20Graph%20API.md). To choose between this and the Functional API, see [Choosing between Graph and Functional APIs](../Get%20started/Choosing%20between%20Graph%20and%20Functional%20APIs.md).

## Graphs

LangGraph models agent workflows as graphs built from three parts:

1. [`State`](#state): A shared snapshot of the application. Usually a typed schema.
2. [`Nodes`](#nodes): Functions that read state, do work, and return updates.
3. [`Edges`](#edges): Fixed or conditional transitions that determine the next node.

Compose nodes and edges to build sequences, branches, and loops. Nodes and edges are ordinary functions. They can call an LLM or run other code.

In short: nodes do the work; edges decide what runs next.

### Super-steps

LangGraph runs graphs with [message passing](https://en.wikipedia.org/wiki/Message_passing), in the style of Google's [Pregel](https://research.google/pubs/pregel-a-system-for-large-scale-graph-processing/) system. Execution advances in discrete **super-steps**:

* Nodes that run in parallel share one super-step.
* Nodes that run in sequence use separate super-steps.
* A node becomes active when it receives input on an incoming edge.
* After a super-step, nodes with no pending messages become inactive.
* The run ends when every node is inactive and no messages remain in transit.

### StateGraph

[`StateGraph`](https://reference.langchain.com/python/langgraph/graph/state/StateGraph) is the main graph builder. Parameterize it with your state schema.

### Compiling your graph

Build a graph by defining [state](#state), adding [nodes](#nodes) and [edges](#edges), then compiling. Compilation checks the graph structure (for example for orphaned nodes). It is also where you attach runtime options such as [checkpointers](../Capabilities/Persistence.md) and breakpoints.

You must compile the graph before you invoke or stream it. This is the smallest end-to-end example:

```python
from typing_extensions import TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    text: str


def node_a(state: State):
    return {"text": state["text"] + "a"}


graph = (
    StateGraph(State)
    .add_node("node_a", node_a)
    .add_edge(START, "node_a")
    .add_edge("node_a", END)
    .compile()
)

graph.invoke({"text": ""})
# {'text': 'a'}
```

## State

State is the shared data that nodes read and update. LangGraph stores that data in **channels**: named slots in the state schema (the keys of your state object). Each channel holds a value and defines how updates merge into it. Most channels use last-write-wins. Channels with a [reducer](#reducers) combine values instead, for example by appending to a list.

State has two parts:

* A [schema](#schema) that declares the channels in the graph
* Optional [reducers](#reducers) that control how updates merge into each channel

Nodes return partial updates. LangGraph applies those updates through each channel's reducer.

Define state with a [`TypedDict`](https://docs.python.org/3/library/typing.html#typing.TypedDict), a [`dataclass`](https://docs.python.org/3/library/dataclasses.html) (for defaults), or a Pydantic [`BaseModel`](Define%20and%20update%20state.md#use-pydantic-models-for-graph-state) when you need validation. Prefer `TypedDict` or `dataclass` for performance.

> [!NOTE]
>
> [`create_agent`](https://docs.langchain.com/oss/python/langchain/agents) state schemas must be `TypedDict`. Pydantic models are not supported.

### Schema

By default, the graph input and output schemas match the full state. You can narrow them when some keys are internal only. See [Define input and output schemas](Define%20and%20update%20state.md#define-input-and-output-schemas).

#### Multiple schemas

Most graphs share one state schema. Use multiple schemas when you need either of the following:

* Private channels that internal nodes share, but that are not part of graph input or output
* Explicit input and output schemas that are subsets of the full internal state

A node can write to any channel in the graph state, including channels outside its declared input schema. Nodes can also introduce private channels when those schemas are defined. Input and output schemas constrain what `invoke` accepts and returns. They do not hide channels from [streaming](../Capabilities/Streaming.md) by default. See [Private channels and streaming](Define%20and%20update%20state.md#private-channels-and-streaming).

For examples, see [Define input and output schemas](Define%20and%20update%20state.md#define-input-and-output-schemas) and [Pass private state between nodes](Define%20and%20update%20state.md#pass-private-state-between-nodes).

### Reducers

Reducers control how node updates merge into state. Each key has its own reducer. With no reducer, updates overwrite the previous value.

#### Reducer arguments

A reducer is a binary function:

* **Left**: The current value in state for that key
* **Right**: The update returned by a node for that key

```python
new_value = reducer(left=current_state[key], right=node_update[key])
```

Define a reducer and attach it to a state key with `Annotated`:

```python
from typing import Annotated

from typing_extensions import TypedDict


def append_strings(left: list[str], right: list[str]) -> list[str]:
    """Combine the existing state value (left) with a node update (right)."""
    return left + right


class State(TypedDict):
    tags: Annotated[list[str], append_strings]
```

Calling the reducer with left and right shows how values combine:

```python
append_strings(left=["draft"], right=["review"])  # returns ["draft", "review"]
```

#### Default reducer

The default reducer replaces the left value with the right. Nodes return partial updates, not the full state.

For example, start with `{"foo": 1, "bar": ["hi"]}`. An update of `{"foo": 2}` yields `{"foo": 2, "bar": ["hi"]}`. A later `{"bar": ["bye"]}` yields `{"foo": 2, "bar": ["bye"]}`.

#### Custom reducers

Use a custom reducer to combine values, such as appending to a list.

```python
import operator
from typing import Annotated

from typing_extensions import TypedDict


class State(TypedDict):
    foo: int
    bar: Annotated[list[str], operator.add]
```

Here `foo` overwrites. `bar` appends with `operator.add`. From `{"foo": 1, "bar": ["hi"]}`, an update of `{"bar": ["bye"]}` becomes `{"foo": 1, "bar": ["hi", "bye"]}`.

#### Overwrite

To bypass a merging reducer and replace a value (including clearing it), use [`Overwrite`](https://reference.langchain.com/python/langgraph/types/). See [Bypass reducers with Overwrite](Define%20and%20update%20state.md#bypass-reducers-with-overwrite).

#### Resetting a reducer field

With a merging reducer, returning an empty value keeps prior data. That matters for error buffers or retry counters that must clear between attempts. See [Resetting a reducer field](Define%20and%20update%20state.md#resetting-a-reducer-field) and [Bypass reducers with Overwrite](Define%20and%20update%20state.md#bypass-reducers-with-overwrite).

### Working with messages in graph state

#### Why use messages?

Chat models take a list of messages as input. LangChain's [chat model interface](https://docs.langchain.com/oss/python/langchain/models.md) accepts message objects such as [`HumanMessage`](https://reference.langchain.com/python/langchain-core/messages/human/HumanMessage) and [`AIMessage`](https://reference.langchain.com/python/langchain-core/messages/ai/AIMessage). See the [Messages conceptual guide](https://docs.langchain.com/oss/python/langchain/messages.md).

#### Using messages in your graph

Store conversation history as a list of messages in state, with a reducer that appends new messages and updates existing ones by ID.

Use [`add_messages`](https://reference.langchain.com/python/langgraph/graph/message/add_messages) on a `messages` key. Plain `operator.add` only appends, so it cannot update an existing message in place during human-in-the-loop edits.

```python
from typing import Annotated

from langchain.messages import AnyMessage
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class GraphState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
```

#### Serialization

Message reducers also deserialize common wire formats into LangChain message objects.

```python
# Supported
{"messages": [HumanMessage(content="message")]}

# Also supported
{"messages": [{"type": "human", "content": "message"}]}
```

Access attributes with dot notation, for example `state["messages"][-1].content`. See [LangChain serialization](https://docs.langchain.com/oss/python/langchain/messages.md#serialization).

#### MessagesState

`MessagesState` is a prebuilt state with a single `messages` key that uses [`add_messages`](https://reference.langchain.com/python/langgraph/graph/message/add_messages). Subclass it to add fields:

```python
from langgraph.graph import MessagesState


class State(MessagesState):
    documents: list[str]
```

## Nodes

Nodes are sync or async functions that implement a step of the graph.

A node can accept:

1. `state`: The graph [state](#state)
2. `config`: A [`RunnableConfig`](https://reference.langchain.com/python/langchain-core/runnables/config/RunnableConfig) with values such as `thread_id` and `tags`
3. `runtime`: A `Runtime` object with [runtime context](#runtime-context), `store`, `stream_writer`, `execution_info`, and related helpers

Add nodes with [`add_node`](https://reference.langchain.com/python/langgraph/graph/state/StateGraph/add_node):

```python
from dataclasses import dataclass

from langgraph.graph import StateGraph
from langgraph.runtime import Runtime
from typing_extensions import TypedDict


class State(TypedDict):
    input: str
    results: str


@dataclass
class Context:
    user_id: str


builder = StateGraph(State)


def plain_node(state: State):
    return state


def node_with_runtime(state: State, runtime: Runtime[Context]):
    return {"results": f"Hello, {state['input']}!"}


builder.add_node("plain_node", plain_node)
builder.add_node("node_with_runtime", node_with_runtime)
```

Behind the scenes, LangGraph wraps functions as [`RunnableLambda`](https://reference.langchain.com/python/langchain-core/runnables/base/RunnableLambda) so they gain batching, async support, and [tracing](https://docs.langchain.com/langsmith/observability.md).

If you omit a node name, LangGraph uses the function name.

```python
builder.add_node(my_node)
# Reference the node as "my_node" in edges
```

### Re-execution and idempotency

With a [checkpointer](../Capabilities/Persistence.md), LangGraph saves checkpoints at [super-step](#super-steps) boundaries, not mid-function inside a node. After an [interrupt](../Capabilities/Interrupts.md) or [retry](../Capabilities/Fault%20tolerance.md#retries), the affected node runs again from the start of its function. Side effects before the pause run again.

Design node logic so re-execution is safe. Prefer idempotency keys, upserts, or read-before-write checks. For durable keys and external side effects under retries, see [Retry boundaries and idempotency](../Capabilities/Fault%20tolerance.md#retry-boundaries-and-idempotency). For effects around `interrupt()`, see [Side effects called before `interrupt` must be idempotent](../Capabilities/Interrupts.md#side-effects-called-before-interrupt-must-be-idempotent).

You can add or remove nodes and edges without breaking resume for existing threads. Resumed runs use saved state and the graph you compile now.

If a node calls [tasks](../Advanced/Build%20with%20the%20Functional%20API/Functional%20API%20overview.md#task) or [`interrupt`](https://reference.langchain.com/python/langgraph/types/interrupt), stricter [determinism](../Advanced/Build%20with%20the%20Functional%20API/Functional%20API%20overview.md#determinism) rules apply on resume. Completed task results are restored from the checkpointer. Changing task or interrupt order before the resume point can mismatch cached values. See [Idempotency](../Advanced/Build%20with%20the%20Functional%20API/Functional%20API%20overview.md#idempotency).

### Choose the unit of work

A [node](#nodes) is a checkpoint and retry boundary. It is also where the graph can take a different path. Deterministic work such as parsing, retrieval, or a fixed tool chain does not need its own node unless you want that boundary.

Ask whether the step decides what happens next, or executes something already decided. Then pick the primitive that matches the recovery behavior you need:

| Primitive | Own checkpoint | On resume or retry | Choose when |
| - | - | - | - |
| Plain function inside a node | No. It runs inside the node's [super-step](#super-steps). | Re-runs whenever the node re-runs. | No routing fork after the step, and repeating it with the rest of the node is acceptable. |
| [Task](../Advanced/Build%20with%20the%20Functional%20API/Functional%20API%20overview.md#task) | No new graph checkpoint. The result is stored with the running entrypoint or parent checkpoint. | The enclosing entrypoint or node replays from the start. Completed tasks return stored results. | The step has a side effect or is expensive, and must not repeat on resume. |
| [Subgraph](../Capabilities/Subgraphs.md) | Yes for stateful modes: nodes checkpoint under a namespace of the parent thread. Compile with `checkpointer=False` for no subgraph checkpoints. | Stateful modes resume inside the subgraph at the interrupted or failed node. | The unit has its own routing or state schema, or more than one parent graph reuses it. |
| Graph node | Yes. A checkpoint follows the [super-step](#super-steps) it runs in. | Resume starts at that node. Earlier nodes do not re-run. | A routing fork is possible after the step, or you need an interrupt, resume, or [time travel](../Capabilities/Use%20time-travel.md) boundary. |

For side effects under retries, see [Retry boundaries and idempotency](../Capabilities/Fault%20tolerance.md#retry-boundaries-and-idempotency). For task retries and timeouts, see [Tasks](../Advanced/Build%20with%20the%20Functional%20API/Configure%20Functional%20API%20tasks.md).

### Using tasks in nodes

When one node runs several operations that should checkpoint independently, wrap each operation in a [task](../Advanced/Build%20with%20the%20Functional%20API/Functional%20API%20overview.md#task) instead of splitting the work across nodes. With a checkpointer, completed task results are saved, so a resumed thread can skip finished work inside the node. For patterns and examples, see [Tasks](../Advanced/Build%20with%20the%20Functional%20API/Configure%20Functional%20API%20tasks.md) and [Common pitfalls](../Advanced/Build%20with%20the%20Functional%20API/Functional%20API%20overview.md#common-pitfalls).

### `START` node

[`START`](https://reference.langchain.com/python/langgraph/constants/START) is the virtual entry that delivers user input into the graph. Use it to mark which nodes run first.

```python
from langgraph.graph import START

graph.add_edge(START, "node_a")
```

### `END` node

`END` marks a terminal edge. Use it when a path should stop.

```python
from langgraph.graph import END

graph.add_edge("node_a", END)
```

### Node caching

LangGraph can cache node (and task) results by input. Pass a cache when you compile the graph, and attach a [`CachePolicy`](https://reference.langchain.com/python/langgraph/types/CachePolicy) on the node.

For options, end-to-end examples, and graph-wide defaults, see [Add node caching](Configure%20nodes.md#add-node-caching).

## Edges

Edges decide where control goes next:

* **Normal edges**: Always go from one node to the next
* **Conditional edges**: Call a function to determine the next node(s)
* **Entry point**: First node after user input (`START` → node)
* **Conditional entry point**: Route from `START` with a function

A node can have multiple outgoing edges. Destinations on those edges run in parallel in the next super-step.

> [!WARNING]
>
> For each node, use either static edges or dynamic routing ([conditional edges](#conditional-edges) / [`Command`](https://reference.langchain.com/python/langgraph/types/Command)), not both. Mixing them can run both paths.

### Normal edges

If you always want to go from node A to node B, use [`add_edge`](https://reference.langchain.com/python/langgraph/pregel/_draw/add_edge):

```python
graph.add_edge("node_a", "node_b")
```

### Conditional edges

If you want to optionally route to one or more nodes (or terminate), use [`add_conditional_edges`](https://reference.langchain.com/python/langgraph/graph/state/StateGraph/add_conditional_edges). Pass the source node and a routing function to call after that node runs:

```python
graph.add_conditional_edges("node_a", routing_function)
# Or with an explicit map:
graph.add_conditional_edges(
    "node_a",
    routing_function,
    {"path_a": "node_b", "path_b": "node_c"},
)
```

The routing function receives the current graph state. By default, its return value is the name of the next node (or a list of names). Those nodes run in parallel in the next super-step. You can also pass a dictionary that maps the function's output to node names.

The routing function can return a node name, `END`, a list of names (fan-out), or [`Send`](https://reference.langchain.com/python/langgraph/types/Send) objects for map-reduce. See [Build sequences, branches, and loops](Build%20sequences%2C%20branches%2C%20and%20loops.md).

> [!TIP]
>
> Use [`Command`](https://reference.langchain.com/python/langgraph/types/Command) instead of conditional edges when you want to combine state updates and routing in a single function.

### Entry point

The entry point is the first node (or nodes) that run when the graph starts. Add an edge from the virtual [`START`](https://reference.langchain.com/python/langgraph/constants/START) node to the first node to execute:

```python
graph.add_edge(START, "node_a")
```

### Conditional entry point

A conditional entry point lets you start at different nodes depending on custom logic. Use [`add_conditional_edges`](https://reference.langchain.com/python/langgraph/graph/state/StateGraph/add_conditional_edges) from [`START`](https://reference.langchain.com/python/langgraph/constants/START):

```python
graph.add_conditional_edges(START, routing_function)
```

You can optionally provide a dictionary that maps the routing function's output to the next node name.

## `Send`

Use [`Send`](https://reference.langchain.com/python/langgraph/types/Send) when you need to run the same node once per item, each with its own input, and the number of items is only known at runtime. That shape is often called map-reduce or orchestrator-worker: one node produces a list, workers process each item in parallel, then a later node reads the combined results.

Normal edges cannot do this. They choose which nodes run next, but every chosen node still receives the shared graph state, and the topology is fixed when you build the graph.

Return one or more `Send` objects from a conditional edge. Each `Send` names a target node and passes a custom argument as that invocation's input. LangGraph runs those invocations in parallel. When workers write to shared state keys, [reducers](#reducers) merge their updates, for example by concatenating lists.

The first argument to `Send` is the target node name. The second is the state (or partial state) for that invocation.

```python
from langgraph.types import Send


def continue_to_jokes(state: OverallState):
    return [Send("generate_joke", {"subject": s}) for s in state["subjects"]]


graph.add_conditional_edges("node_a", continue_to_jokes)
```

For a full map-reduce example, see [Use Send for map-reduce](Use%20Send%20and%20Command.md#use-send-for-map-reduce).

## `Command`

Use [`Command`](https://reference.langchain.com/python/langgraph/types/Command) when a single step must both update state and choose what runs next. Normally those jobs are separate: a node returns state updates, and [edges](#edges) (or [conditional edges](#conditional-edges)) decide the next node. Return `Command` from a node when the next hop depends on work you just did in that same function.

`Command` also covers two other cases that plain returns and edges do not: resume a run after an [interrupt](../Capabilities/Interrupts.md), and update or route from inside a [tool](#return-from-tools).

For routing alone, prefer conditional edges. Reach for `Command` when you need the update and the route together (or one of the interrupt / tool cases above).

`Command` accepts:

* **`update`**: State updates (like a normal node return)
* **`goto`**: Next node(s) (like a conditional edge)
* **`graph`**: Parent graph target when navigating from a [subgraph](../Capabilities/Subgraphs.md)
* **`resume`**: Value used to resume after an [interrupt](../Capabilities/Interrupts.md)

Use `Command` in three places:

* **[Return from nodes](#return-from-nodes)**: `update`, `goto`, and `graph`
* **[Input to `invoke` or `stream`](#input-to-invoke-or-stream)**: `resume` after an interrupt
* **[Return from tools](#return-from-tools)**: Updates and routing from inside a tool

### Return from nodes

#### `update` and `goto`

Return [`Command`](https://reference.langchain.com/python/langgraph/types/Command) to update state and route in one step:

```python
def my_node(state: CommandState) -> Command[Literal["my_other_node"]]:
    return Command(
        update={"foo": "bar"},
        goto="my_other_node",
    )
```

Annotate the return type with the allowed destinations, for example `Command[Literal["my_other_node"]]`. That tells LangGraph which edges to render.

Use [`Command`](https://reference.langchain.com/python/langgraph/types/Command) when you need both an update and a route. For routing alone, prefer [conditional edges](#conditional-edges).

> [!WARNING]
>
> `Command` adds dynamic edges. Static edges from the same node still run. Do not mix `Command` routing with `add_edge` from one node.

See [Combine control flow and state updates with Command](Use%20Send%20and%20Command.md#combine-control-flow-and-state-updates-with-command).

#### `graph`

From a [subgraph](../Capabilities/Subgraphs.md) node, navigate to a node in the parent graph with `Command.PARENT`:

```python
def my_node(state: CommandState) -> Command[Literal["other_subgraph"]]:
    return Command(
        update={"foo": "bar"},
        goto="other_subgraph",  # where `other_subgraph` is a node in the parent graph
        graph=Command.PARENT,
    )
```

When you update a parent key that the subgraph also uses, define a [reducer](#reducers) for that key in the parent. See [Navigate to a node in a parent graph](Use%20Send%20and%20Command.md#navigate-to-a-node-in-a-parent-graph).

### Input to `invoke` or `stream`

> [!WARNING]
>
> `Command(resume=...)` is the only `Command` pattern meant as input to `invoke()` / `stream()` (optionally with `update=...` while resuming). Do not pass `Command(update=...)` alone to continue a conversation. Any `Command` as input resumes from the latest checkpoint, not from `START`, so a finished thread can look stuck. Pass a plain dict to start a new turn:
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> # Wrong: resumes from the latest checkpoint
> graph.invoke(Command(update={  # [!code --]
>     "messages": [{"role": "user", "content": "follow up"}]  # [!code --]
> }), config)  # [!code --]
>
> # Correct: plain dict restarts from START
> graph.invoke({  # [!code ++]
>     "messages": [{"role": "user", "content": "follow up"}]  # [!code ++]
> }, config)  # [!code ++]
> ```

#### `resume`

Use `Command(resume=...)` after an [interrupt](../Capabilities/Interrupts.md). The value becomes the return value of the paused `interrupt()` call:

```python
graph.invoke(Command(resume="yes"), config)
```

See [Interrupts](../Capabilities/Interrupts.md) for full patterns.

### Return from tools

Return [`Command`](https://reference.langchain.com/python/langgraph/types/Command) from tools to update state and route after the tool finishes. `goto` from a tool adds a dynamic edge. Static edges on the calling node still run, so do not mix both.

See [Use inside tools](Use%20Send%20and%20Command.md#use-inside-tools).

## Graph migrations

You can change a graph's nodes, edges, and state schema even when a [checkpointer](../Capabilities/Persistence.md) already stores thread state. What is safe depends on whether the thread has finished or is paused.

**Topology (nodes and edges)**

* Finished threads (not interrupted): you can add, remove, or rename nodes and edges freely.
* Interrupted threads: you can change edges and add nodes. Do not rename or remove a node the thread is about to enter. On resume, LangGraph looks up that node by name, and a missing name fails the run.

**State schema**

* Adding or removing keys is backwards and forwards compatible.
* Renaming a key drops the saved value for that key in existing threads.
* Incompatible type changes on an existing key (for example, narrowing or requiring a field that old checkpoints omit) can break older thread state.

For logic changes that stay schema-compatible (for example, a new tool set), see [Business compatibility](../Deployment/Backward%20compatibility.md#business-compatibility).

## Runtime context

Runtime context passes dependencies into nodes without putting them in graph state (for example, model name or a database handle).

```python
from dataclasses import dataclass

from langgraph.graph import END, START, StateGraph
from langgraph.runtime import Runtime
from typing_extensions import TypedDict


class State(TypedDict):
    input: str
    output: str


@dataclass
class ContextSchema:
    llm_provider: str = "openai"


def get_llm(provider: str) -> str:
    return provider


def node_a(state: State, runtime: Runtime[ContextSchema]):
    llm = get_llm(runtime.context.llm_provider)
    return {"output": llm}


graph = (
    StateGraph(State, context_schema=ContextSchema)
    .add_node("node_a", node_a)
    .add_edge(START, "node_a")
    .add_edge("node_a", END)
    .compile()
)
graph.invoke({"input": "hi"}, context={"llm_provider": "anthropic"})
```

See [Add runtime configuration](Configure%20nodes.md#add-runtime-configuration).

### Recursion limit

The recursion limit caps how many [super-steps](#super-steps) one run may execute. When the limit is exceeded, LangGraph raises `GraphRecursionError`.

Starting in version 1.1.4, the default is 10,007 super-steps. Between 1.0.6 and 1.1.3, the default is 10,000 steps. Override it with the `LANGGRAPH_DEFAULT_RECURSION_LIMIT` environment variable, or pass `recursion_limit` as a top-level config key (not under `configurable`).

For recipes (catching the error, reading `langgraph_step`, and Python `RemainingSteps`), see [Impose a recursion limit](Build%20sequences%2C%20branches%2C%20and%20loops.md#impose-a-recursion-limit) and [Access and handle the recursion counter](Build%20sequences%2C%20branches%2C%20and%20loops.md#access-and-handle-the-recursion-counter).

## Learn more

* [Thinking in the Graph API](Thinking%20in%20the%20Graph%20API.md)
* [LangGraph quickstart](../Get%20started/Quickstart.md)
* [Build checklist for the Graph API](Build%20checklist%20for%20the%20Graph%20API.md)
* [Define and update state](Define%20and%20update%20state.md)
* [Build sequences, branches, and loops](Build%20sequences%2C%20branches%2C%20and%20loops.md)
* [Use Send and Command](Use%20Send%20and%20Command.md)
* [Configure nodes](Configure%20nodes.md)
* [Visualize your graph](Visualize%20your%20graph.md)
* [Functional API overview](../Advanced/Build%20with%20the%20Functional%20API/Functional%20API%20overview.md)

# Build sequences, branches, and loops

> Compose sequences, parallel branches, conditional edges, and loops with the LangGraph Graph API.

Compose [sequences](#create-a-sequence-of-steps), [parallel branches](#create-branches), [conditional edges](#conditional-branching), and [loops](#create-and-control-loops) with the Graph API. For map-reduce fan-out and returning edges from nodes, see [Use Send and Command](Use%20Send%20and%20Command.md). For node-level retries, timeouts, and caching, see [Configure nodes](Configure%20nodes.md).

## Create a sequence of steps

> [!NOTE]
>
> **Prerequisites**
> This guide assumes familiarity with [Define and update state](Define%20and%20update%20state.md).

This section shows how to build a sequential graph. Python also has an `add_sequence` shorthand for the same pattern.

```mermaid
%%{init:{'theme':'base','themeVariables':{'lineColor':'#40668D','primaryColor':'#E5F4FF','primaryTextColor':'#030710','primaryBorderColor':'#006DDD'}}}%%
flowchart LR
    startNode([START]) --> s1[step_1]
    s1 --> s2[step_2]
    s2 --> s3[step_3]

    classDef process fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710
    classDef terminal fill:#F2FAFF,stroke:#40668D,stroke-width:2px,color:#030710
    class s1,s2,s3 process
    class startNode terminal
```

Add a sequence of nodes with [`add_node`](https://reference.langchain.com/python/langgraph/graph/state/StateGraph/add_node) and [`add_edge`](https://reference.langchain.com/python/langgraph/pregel/_draw/add_edge) on a [StateGraph](Graph%20API%20overview.md#stategraph):

```python
from langgraph.graph import START, StateGraph

builder = StateGraph(State)

# Add nodes
builder.add_node(step_1)
builder.add_node(step_2)
builder.add_node(step_3)

# Add edges
builder.add_edge(START, "step_1")
builder.add_edge("step_1", "step_2")
builder.add_edge("step_2", "step_3")
```

Or use the built-in shorthand `.add_sequence`:

```python
builder = StateGraph(State).add_sequence([step_1, step_2, step_3])
builder.add_edge(START, "step_1")
```

> [accordion] Why split application steps into a sequence with LangGraph?
>
> LangGraph can add a persistence layer under the graph. State is checkpointed between nodes, so those nodes govern:
>
> * How state updates are [checkpointed](../Capabilities/Persistence.md)
> * How interruptions resume in [human-in-the-loop](../Capabilities/Interrupts.md) workflows
> * How to rewind and branch executions with [time travel](../Capabilities/Use%20time-travel.md)
>
> They also shape how steps are [streamed](../Capabilities/Streaming.md), and how the app is visualized and debugged in [Studio](../LangSmith%20Studio.md).

The following end-to-end example builds a sequence of three steps:

1. Populate a value in a key of the state
2. Update the same value
3. Populate a different value

First define the [state](Graph%20API%20overview.md#state). For how updates merge, see [Process state updates with reducers](Define%20and%20update%20state.md#process-state-updates-with-reducers).

This example tracks two values:

```python
from typing_extensions import TypedDict


class State(TypedDict):
    value_1: str
    value_2: int
```

[Nodes](Graph%20API%20overview.md#nodes) are Python functions that read graph state and return updates. The first argument is always the state:

```python
def step_1(state: State):
    return {"value_1": "a"}


def step_2(state: State):
    current_value_1 = state["value_1"]
    return {"value_1": f"{current_value_1} b"}


def step_3(state: State):
    return {"value_2": 10}
```

> [!NOTE]
>
> Each node update can name only the keys it changes.
>
> By default, that **overwrites** the previous value for those keys. Use [reducers](Graph%20API%20overview.md#reducers) when updates should append or combine instead. See [Process state updates with reducers](Define%20and%20update%20state.md#process-state-updates-with-reducers).

Next, define a [StateGraph](Graph%20API%20overview.md#stategraph) on that state and wire the nodes.

Use [`add_node`](Graph%20API%20overview.md#nodes) and [`add_edge`](Graph%20API%20overview.md#edges) to populate the graph and define its control flow.

```python
from langgraph.graph import START, StateGraph

builder = StateGraph(State)

# Add nodes
builder.add_node(step_1)
builder.add_node(step_2)
builder.add_node(step_3)

# Add edges
builder.add_edge(START, "step_1")
builder.add_edge("step_1", "step_2")
builder.add_edge("step_2", "step_3")
```

> [!TIP]
>
> **Specifying custom names**
> Pass an explicit name as the first argument to [`add_node`](https://reference.langchain.com/python/langgraph/graph/state/StateGraph/add_node):
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> builder.add_node("my_node", step_1)
> ```

Note that:

* [`add_edge`](https://reference.langchain.com/python/langgraph/pregel/_draw/add_edge) takes node names. For bare functions, the default name is `node.__name__`.
* The graph needs an entry point: add an edge from the [START node](Graph%20API%20overview.md#start-node).
* The graph halts when there are no more nodes to execute.

Then [compile](Graph%20API%20overview.md#compiling-your-graph) the graph. Compile runs basic structure checks (for example, orphaned nodes). Pass a [checkpointer](../Capabilities/Persistence.md) here when the app needs persistence.

```python
graph = builder.compile()
```

Invoke the graph:

```python
graph.invoke({"value_1": "c"})
```

```
{'value_1': 'a b', 'value_2': 10}
```

Note that:

* This invoke passes a value for one state key. Nodes can also write keys that were not in the input.
* The first node overwrites the value that was passed in.
* The second node updates that value.
* The third node populates a different key.

> [!TIP]
>
> **Built-in shorthand**
> `langgraph>=0.2.46` includes a built-in short-hand `add_sequence` for adding node sequences. You can compile the same graph as follows:
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> builder = StateGraph(State).add_sequence([step_1, step_2, step_3])  # [!code highlight]
> builder.add_edge(START, "step_1")
>
> graph = builder.compile()
>
> graph.invoke({"value_1": "c"})
> ```

## Create branches

Parallel node execution speeds up graph runs. LangGraph fans out and fans in with standard edges and [conditional\_edges](https://reference.langchain.com/python/langgraph/graph/state/StateGraph/add_conditional_edges). The following examples build branching dataflows. For map-reduce fan-out to dynamic targets, see [Use Send and Command](Use%20Send%20and%20Command.md).

### Run graph nodes in parallel

This example fans out from `Node A` to `B` and `C`, then fans in to `D`. The state uses a [reducer](Graph%20API%20overview.md#reducers) so values accumulate for that key instead of overwriting. For lists, that means concatenating the new list onto the existing list. See [Process state updates with reducers](Define%20and%20update%20state.md#process-state-updates-with-reducers).

```mermaid
%%{init:{'theme':'base','themeVariables':{'lineColor':'#40668D','primaryColor':'#E5F4FF','primaryTextColor':'#030710','primaryBorderColor':'#006DDD'}}}%%
flowchart LR
    startNode([START]) --> a[a]
    a --> b[b]
    a --> c[c]
    b --> d[d]
    c --> d
    d --> endNode([END])

    classDef process fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710
    classDef terminal fill:#F2FAFF,stroke:#40668D,stroke-width:2px,color:#030710
    class a,b,c,d process
    class startNode,endNode terminal
```

```python
import operator
from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    # The operator.add reducer fn makes this append-only
    aggregate: Annotated[list, operator.add]


def a(state: State):
    print(f'Adding "A" to {state["aggregate"]}')
    return {"aggregate": ["A"]}


def b(state: State):
    print(f'Adding "B" to {state["aggregate"]}')
    return {"aggregate": ["B"]}


def c(state: State):
    print(f'Adding "C" to {state["aggregate"]}')
    return {"aggregate": ["C"]}


def d(state: State):
    print(f'Adding "D" to {state["aggregate"]}')
    return {"aggregate": ["D"]}


builder = StateGraph(State)
builder.add_node(a)
builder.add_node(b)
builder.add_node(c)
builder.add_node(d)
builder.add_edge(START, "a")
builder.add_edge("a", "b")
builder.add_edge("a", "c")
builder.add_edge("b", "d")
builder.add_edge("c", "d")
builder.add_edge("d", END)
graph = builder.compile()
```

With the reducer, you can see that the values added in each node are accumulated.

```python
graph.invoke({"aggregate": []}, {"configurable": {"thread_id": "foo"}})
```

```
Adding "A" to []
Adding "B" to ['A']
Adding "C" to ['A']
Adding "D" to ['A', 'B', 'C']
```

> [!NOTE]
>
> In the above example, nodes `"b"` and `"c"` are executed concurrently in the same [superstep](Graph%20API%20overview.md#super-steps). Because they are in the same step, node `"d"` executes after both `"b"` and `"c"` are finished.
>
> Importantly, updates from a parallel superstep may not be ordered consistently. If you need a consistent, predetermined ordering of updates from a parallel superstep, you should write the outputs to a separate field in the state together with a value with which to order them.

> [accordion] Exception handling
>
> LangGraph runs nodes in [supersteps](Graph%20API%20overview.md#super-steps). Parallel branches in a superstep run concurrently, but the superstep is **transactional**: if any branch raises, **none** of that superstep's updates apply to state.
>
> With a [checkpointer](../Capabilities/Persistence.md), results from successful nodes in a completed superstep are saved and do not repeat when the run resumes.
>
> For flaky work such as unreliable API calls, use either:
>
> 1. Ordinary `try` / `except` (or equivalent) inside the node.
> 2. A **[`RetryPolicy`](https://reference.langchain.com/python/langgraph/types/#langgraph.types.RetryPolicy)** on the node so LangGraph retries selected exceptions. Only failing branches retry, so successful siblings are not re-run.
>
> Together, these keep parallel execution while you control how failures are handled. For a full guide, see [Fault tolerance](../Capabilities/Fault%20tolerance.md).

> [!TIP]
>
> **Set max concurrency**
> Pass `max_concurrency` as a top-level config key (not under `configurable`) when invoking the graph. See [RunnableConfig](https://reference.langchain.com/python/langchain-core/runnables/config/RunnableConfig).
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> graph.invoke({"value_1": "c"}, {"max_concurrency": 10})
> ```

### Defer node execution

Deferring node execution delays a node until all other pending tasks are completed. This matters when branches have different lengths, which is common in map-reduce workflows.

The parallel example above fans out and fans in when each path is one step. Add a node `"b_2"` on the `"b"` branch so the paths have unequal length. Node `d` uses `defer` so it waits for the longer branch:

```mermaid
%%{init:{'theme':'base','themeVariables':{'lineColor':'#40668D','primaryColor':'#E5F4FF','primaryTextColor':'#030710','primaryBorderColor':'#006DDD'}}}%%
flowchart LR
    startNode([START]) --> a[a]
    a --> b[b]
    a --> c[c]
    b --> b2[b_2]
    b2 --> d[d]
    c --> d
    d --> endNode([END])

    classDef process fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710
    classDef terminal fill:#F2FAFF,stroke:#40668D,stroke-width:2px,color:#030710
    class a,b,b2,c,d process
    class startNode,endNode terminal
```

```python
import operator
from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    # The operator.add reducer fn makes this append-only
    aggregate: Annotated[list, operator.add]


def a(state: State):
    print(f'Adding "A" to {state["aggregate"]}')
    return {"aggregate": ["A"]}


def b(state: State):
    print(f'Adding "B" to {state["aggregate"]}')
    return {"aggregate": ["B"]}


def b_2(state: State):
    print(f'Adding "B_2" to {state["aggregate"]}')
    return {"aggregate": ["B_2"]}


def c(state: State):
    print(f'Adding "C" to {state["aggregate"]}')
    return {"aggregate": ["C"]}


def d(state: State):
    print(f'Adding "D" to {state["aggregate"]}')
    return {"aggregate": ["D"]}


builder = StateGraph(State)
builder.add_node(a)
builder.add_node(b)
builder.add_node(b_2)
builder.add_node(c)
builder.add_node(d, defer=True)  # [!code highlight]
builder.add_edge(START, "a")
builder.add_edge("a", "b")
builder.add_edge("a", "c")
builder.add_edge("b", "b_2")
builder.add_edge("b_2", "d")
builder.add_edge("c", "d")
builder.add_edge("d", END)
graph = builder.compile()
```

```python
graph.invoke({"aggregate": []})
```

```
Adding "A" to []
Adding "B" to ['A']
Adding "C" to ['A']
Adding "B_2" to ['A', 'B', 'C']
Adding "D" to ['A', 'B', 'C', 'B_2']
```

Nodes `"b"` and `"c"` run concurrently in the same superstep. `defer=True` on node `d` keeps it from running until all pending tasks finish, so `"d"` waits for the full `"b"` branch.

When every branch always runs, you can wait with a list-form edge instead of `defer=True`. `add_edge` also accepts a list of start nodes. This is not shorthand for separate `add_edge` calls; the two forms behave differently:

```python
builder.add_edge(["b_2", "c"], "d")  # d runs once, after both b_2 and c complete
```

* **A list of start nodes** runs `d` once, after all of the listed nodes have completed. If one of them never runs (for example, a conditional edge does not select its branch), `d` never runs and no error is raised. State updates from branches that did complete remain in the graph state, but `d` does not consume them.
* **Separate edges** run `d` once per superstep in which any incoming branch completes. With branches of equal length, that is a single run; with branches of different lengths, `d` runs more than once.
* **Separate edges with `defer=True`** (the pattern in the example above) run `d` once, after every selected branch has completed, whether the fan-out selected all of the branches or only some of them.

`defer=True` postpones the node until no tasks are pending anywhere in the graph, not only in the branches that feed it. A [`Send`](Use%20Send%20and%20Command.md) addressed to the node still invokes it separately.

### Conditional branching

Route to different nodes at runtime from state. Node `a` updates state, then a conditional edge chooses `b` or `c`:

```mermaid
%%{init:{'theme':'base','themeVariables':{'lineColor':'#40668D','primaryColor':'#E5F4FF','primaryTextColor':'#030710','primaryBorderColor':'#006DDD'}}}%%
flowchart LR
    startNode([START]) --> a[a]
    a -.-> b[b]
    a -.-> c[c]
    b --> endNode([END])
    c --> endNode

    classDef process fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710
    classDef terminal fill:#F2FAFF,stroke:#40668D,stroke-width:2px,color:#030710
    class a,b,c process
    class startNode,endNode terminal
```

Dashed edges are conditional routes.

If your fan-out should vary at runtime based on the state, you can use [`add_conditional_edges`](https://reference.langchain.com/python/langgraph/graph/state/StateGraph/add_conditional_edges) to select one or more paths using the graph state. See the following example, where node `a` generates a state update that determines the next node.

```python
import operator
from typing import Annotated, Literal, Sequence

from typing_extensions import TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    aggregate: Annotated[list, operator.add]
    # Branching key set by node a
    which: str


def a(state: State):
    print(f'Adding "A" to {state["aggregate"]}')
    return {"aggregate": ["A"], "which": "c"}  # [!code highlight]


def b(state: State):
    print(f'Adding "B" to {state["aggregate"]}')
    return {"aggregate": ["B"]}


def c(state: State):
    print(f'Adding "C" to {state["aggregate"]}')
    return {"aggregate": ["C"]}


builder = StateGraph(State)
builder.add_node(a)
builder.add_node(b)
builder.add_node(c)
builder.add_edge(START, "a")
builder.add_edge("b", END)
builder.add_edge("c", END)


def conditional_edge(state: State) -> Literal["b", "c"]:
    # Fill in arbitrary logic here that uses the state
    # to determine the next node
    return state["which"]


builder.add_conditional_edges("a", conditional_edge)  # [!code highlight]

graph = builder.compile()
```

```python
result = graph.invoke({"aggregate": []})
print(result)
```

```
Adding "A" to []
Adding "C" to ['A']
{'aggregate': ['A', 'C'], 'which': 'c'}
```

> [!TIP]
>
> Your conditional edges can route to multiple destination nodes. For example:
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> def route_bc_or_cd(state: State) -> Sequence[str]:
>     if state["which"] == "cd":
>         return ["c", "d"]
>     return ["b", "c"]
> ```

## Create and control loops

A loop needs a way to stop. The usual pattern is a [conditional edge](Graph%20API%20overview.md#conditional-edges) that routes to [END](Graph%20API%20overview.md#end-node) when a termination condition is met.

You can also set a recursion limit when invoking or streaming. The limit is the number of [super-steps](Graph%20API%20overview.md#super-steps) allowed before LangGraph raises an error. See the [recursion limit concept](Graph%20API%20overview.md#recursion-limit).

The following examples use a simple looping graph. Node `a` either continues to `b` (which returns to `a`) or exits:

```mermaid
%%{init:{'theme':'base','themeVariables':{'lineColor':'#40668D','primaryColor':'#E5F4FF','primaryTextColor':'#030710','primaryBorderColor':'#006DDD'}}}%%
flowchart LR
    startNode([START]) --> a[a]
    a -.-> b[b]
    a -.-> endNode([END])
    b --> a

    classDef process fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710
    classDef terminal fill:#F2FAFF,stroke:#40668D,stroke-width:2px,color:#030710
    class a,b process
    class startNode,endNode terminal
```

Dashed edges are conditional routes.

> [!TIP]
>
> To catch `GraphRecursionError` after the limit is hit, see [Impose a recursion limit](#impose-a-recursion-limit). To route to a completion path before the limit, see [Handle recursion with RemainingSteps](#handle-recursion-with-remainingsteps).

Add a conditional edge that encodes the termination condition:

```python
builder = StateGraph(State)
builder.add_node(a)
builder.add_node(b)


def route(state: State) -> Literal["b", END]:
    if termination_condition(state):
        return END
    else:
        return "b"


builder.add_edge(START, "a")
builder.add_conditional_edges("a", route)
builder.add_edge("b", "a")
graph = builder.compile()
```

To control the recursion limit, specify `"recursion_limit"` in the config. This will raise a `GraphRecursionError`, which you can catch and handle:

```python
from langgraph.errors import GraphRecursionError

try:
    graph.invoke(inputs, {"recursion_limit": 3})
except GraphRecursionError:
    print("Recursion Error")
```

Define a graph with a simple loop. A conditional edge implements the termination condition.

```python
import operator
from typing import Annotated, Literal

from typing_extensions import TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    # The operator.add reducer fn makes this append-only
    aggregate: Annotated[list, operator.add]


def a(state: State):
    print(f'Node A sees {state["aggregate"]}')
    return {"aggregate": ["A"]}


def b(state: State):
    print(f'Node B sees {state["aggregate"]}')
    return {"aggregate": ["B"]}


# Define nodes
builder = StateGraph(State)
builder.add_node(a)
builder.add_node(b)


# Define edges
def route(state: State) -> Literal["b", END]:
    if len(state["aggregate"]) < 7:
        return "b"
    else:
        return END


builder.add_edge(START, "a")
builder.add_conditional_edges("a", route)
builder.add_edge("b", "a")
graph = builder.compile()
```

This architecture is similar to a [ReAct agent](../Patterns/Workflows%20and%20agents.md) in which node `"a"` is a tool-calling model, and node `"b"` represents the tools.

The `route` conditional edge ends the run after the `"aggregate"` list passes a threshold length.

When you invoke the graph, it alternates between nodes `"a"` and `"b"` until that condition is met.

```python
graph.invoke({"aggregate": []})
```

```
Node A sees []
Node B sees ['A']
Node A sees ['A', 'B']
Node B sees ['A', 'B', 'A']
Node A sees ['A', 'B', 'A', 'B']
Node B sees ['A', 'B', 'A', 'B', 'A']
Node A sees ['A', 'B', 'A', 'B', 'A', 'B']
```

### Impose a recursion limit

When a termination condition is not guaranteed, set the graph's [recursion limit](Graph%20API%20overview.md#recursion-limit). LangGraph raises `GraphRecursionError` after that many [supersteps](Graph%20API%20overview.md#super-steps). Catch and handle the exception:

```python
from langgraph.errors import GraphRecursionError

try:
    graph.invoke({"aggregate": []}, {"recursion_limit": 4})
except GraphRecursionError:
    print("Recursion Error")
```

```
Node A sees []
Node B sees ['A']
Node A sees ['A', 'B']
Node B sees ['A', 'B', 'A']
Node A sees ['A', 'B', 'A', 'B']
Recursion Error
```

> [accordion] Extended example: loops with branches
>
> A more complex loop fans out one step into two nodes:
>
> ```mermaid theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> %%{init:{'theme':'base','themeVariables':{'lineColor':'#40668D','primaryColor':'#E5F4FF','primaryTextColor':'#030710','primaryBorderColor':'#006DDD'}}}%%
> flowchart LR
>     startNode([START]) --> a[a]
>     a -.-> b[b]
>     a -.-> endNode([END])
>     b --> c[c]
>     b --> d[d]
>     c --> a
>     d --> a
>
>     classDef process fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710
>     classDef terminal fill:#F2FAFF,stroke:#40668D,stroke-width:2px,color:#030710
>     class a,b,c,d process
>     class startNode,endNode terminal
> ```
>
> Dashed edges are conditional routes from `a`.
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import operator
> from typing import Annotated, Literal
>
> from typing_extensions import TypedDict
>
> from langgraph.graph import END, START, StateGraph
>
>
> class State(TypedDict):
>     aggregate: Annotated[list, operator.add]
>
>
> def a(state: State):
>     print(f'Node A sees {state["aggregate"]}')
>     return {"aggregate": ["A"]}
>
>
> def b(state: State):
>     print(f'Node B sees {state["aggregate"]}')
>     return {"aggregate": ["B"]}
>
>
> def c(state: State):
>     print(f'Node C sees {state["aggregate"]}')
>     return {"aggregate": ["C"]}
>
>
> def d(state: State):
>     print(f'Node D sees {state["aggregate"]}')
>     return {"aggregate": ["D"]}
>
>
> builder = StateGraph(State)
> builder.add_node(a)
> builder.add_node(b)
> builder.add_node(c)
> builder.add_node(d)
>
>
> def route(state: State) -> Literal["b", END]:
>     if len(state["aggregate"]) < 7:
>         return "b"
>     else:
>         return END
>
>
> builder.add_edge(START, "a")
> builder.add_conditional_edges("a", route)
> builder.add_edge("b", "c")
> builder.add_edge("b", "d")
> builder.add_edge(["c", "d"], "a")
> graph = builder.compile()
> ```
>
> This graph is a loop of [supersteps](Graph%20API%20overview.md#super-steps): Node A, then B, then C and D concurrent, then back to A. The list-form edge waits for both `"c"` and `"d"` before returning to `"a"`. For how list-form edges differ from separate edges into the same node, see [Defer node execution](#defer-node-execution).
>
> Invoking without a recursion limit completes two full laps before the termination condition:
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> result = graph.invoke({"aggregate": []})
> ```
>
> ```
> Node A sees []
> Node B sees ['A']
> Node D sees ['A', 'B']
> Node C sees ['A', 'B']
> Node A sees ['A', 'B', 'C', 'D']
> Node B sees ['A', 'B', 'C', 'D', 'A']
> Node D sees ['A', 'B', 'C', 'D', 'A', 'B']
> Node C sees ['A', 'B', 'C', 'D', 'A', 'B']
> Node A sees ['A', 'B', 'C', 'D', 'A', 'B', 'C', 'D']
> ```
>
> With the recursion limit set to four, only one lap completes because each lap is four supersteps:
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langgraph.errors import GraphRecursionError
>
> try:
>     result = graph.invoke({"aggregate": []}, {"recursion_limit": 4})
> except GraphRecursionError:
>     print("Recursion Error")
> ```
>
> ```
> Node A sees []
> Node B sees ['A']
> Node C sees ['A', 'B']
> Node D sees ['A', 'B']
> Node A sees ['A', 'B', 'C', 'D']
> Recursion Error
> ```

### Access and handle the recursion counter

Nodes can read the current step from run metadata. Use that to react before the limit is hit.

```python
from langchain_core.runnables import RunnableConfig


def my_node(state: dict, config: RunnableConfig) -> dict:
    current_step = config["metadata"]["langgraph_step"]
    print(f"Currently on step: {current_step}")
    return state
```

#### Handle recursion with RemainingSteps

`RemainingSteps` is a Python-only managed value for how many steps remain before the recursion limit. Use it to route to a completion path before LangGraph raises `GraphRecursionError`:

```python
import operator
from typing import Annotated, Literal

from typing_extensions import TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.managed.is_last_step import RemainingSteps


class State(TypedDict):
    messages: Annotated[list, operator.add]
    remaining_steps: RemainingSteps


def reasoning_node(state: State) -> dict:
    remaining = state["remaining_steps"]
    if remaining <= 2:
        return {"messages": ["Approaching limit, wrapping up..."]}
    return {"messages": ["thinking..."]}


def route_decision(state: State) -> Literal["reasoning_node", "fallback_node"]:
    if state["remaining_steps"] <= 2:
        return "fallback_node"
    return "reasoning_node"


def fallback_node(state: State) -> dict:
    return {"messages": ["Reached complexity limit, providing best effort answer"]}


builder = StateGraph(State)
builder.add_node("reasoning_node", reasoning_node)
builder.add_node("fallback_node", fallback_node)
builder.add_edge(START, "reasoning_node")
builder.add_conditional_edges("reasoning_node", route_decision)
builder.add_edge("fallback_node", END)
graph = builder.compile()

result = graph.invoke({"messages": []}, {"recursion_limit": 10})
```

Handle the limit inside the graph with `RemainingSteps`, or catch `GraphRecursionError` outside the graph:

| Approach | Detection | Handling | Control flow |
| - | - | - | - |
| Proactive (`RemainingSteps`) | Before the limit | Inside the graph via conditional routing | Graph continues to a completion path |
| Reactive (`GraphRecursionError`) | After the limit | Outside the graph in `try` / `except` | Graph execution stops |

Related metadata keys include `langgraph_node`, `langgraph_triggers`, `langgraph_path`, and `langgraph_checkpoint_ns`.

## Async

Async helps when [IO-bound](https://en.wikipedia.org/wiki/I/O_bound) work can run concurrently. To convert a sync graph to async:

1. Define nodes with `async def` instead of `def`.
2. Use `await` for async calls inside those nodes.
3. Invoke with `.ainvoke` or `.astream`.

Many LangChain objects implement the [Runnable](https://reference.langchain.com/python/langchain-core/runnables/base/Runnable) protocol, which has async variants of the sync methods. See the [streaming guide](../Capabilities/Streaming.md) for async streaming examples.

## See also

* [Graph API overview](Graph%20API%20overview.md)
* [Use Send and Command](Use%20Send%20and%20Command.md)
* [Configure nodes](Configure%20nodes.md)
* [Visualize your graph](Visualize%20your%20graph.md)
* [Streaming](../Capabilities/Streaming.md)

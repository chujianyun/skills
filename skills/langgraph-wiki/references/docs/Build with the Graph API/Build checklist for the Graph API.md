# Build checklist for the Graph API

> Decide state, control flow, Send, Command, and node options as you build with the Graph API.

This guide walks through the decisions you make when building a graph. For install and an end-to-end agent example, see the [LangGraph quickstart](../Get%20started/Quickstart.md). For a design walkthrough, see [Thinking in the Graph API](Thinking%20in%20the%20Graph%20API.md). For concepts, see the [Graph API overview](Graph%20API%20overview.md). To choose between the Graph API and the Functional API, see [Choosing between Graph and Functional APIs](../Get%20started/Choosing%20between%20Graph%20and%20Functional%20APIs.md).

## Build your graph

Work through these decisions in order. Each step includes a short example and links to the how-to for full recipes.

**1. Define shared state**

Decide what data nodes share and how updates merge.

* Pick a schema (`TypedDict`, dataclass, or `StateSchema` in TypeScript).
* Add a [reducer](Graph%20API%20overview.md#reducers) for any key that multiple nodes write (for example, appending messages).
* Use private or input/output schemas when the graph should hide internal channels from callers.

```python
import operator
from typing import Annotated

from typing_extensions import TypedDict


class State(TypedDict):
    foo: int
    bar: Annotated[list[str], operator.add]
```

Here `foo` overwrites. `bar` appends with `operator.add`.

For schemas, reducers, messages, and private state, see [Define and update state](Define%20and%20update%20state.md).

**2. Choose control flow**

Decide how work moves between nodes.

* **Sequence**: Fixed steps in order.
* **Branch**: Conditional edges pick the next node from state.
* **Parallel**: Fan-out to several nodes, then fan-in (often with reducers).
* **Loop**: Cycle until a termination condition, or cap runs with a [recursion limit](Graph%20API%20overview.md#recursion-limit).

This sequence checks whether a number is even, then formats a message:

```python
from typing_extensions import TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    number: int
    is_even: bool
    message: str


def check_even(state: State):
    return {"is_even": state["number"] % 2 == 0}


def format_message(state: State):
    return {
        "message": (
            "The number is even." if state["is_even"] else "The number is odd."
        )
    }


workflow = StateGraph(State)
workflow.add_node("check_even", check_even)
workflow.add_node("format_message", format_message)
workflow.add_edge(START, "check_even")
workflow.add_edge("check_even", "format_message")
workflow.add_edge("format_message", END)
graph = workflow.compile()

graph.invoke({"number": 7})
```

For branches, parallel paths, and loops, see [Build sequences, branches, and loops](Build%20sequences%2C%20branches%2C%20and%20loops.md).

**3. Decide if you need Send or Command**

Most graphs only need nodes, edges, and conditional edges. Keep routing in edges unless you hit one of the cases below. For patterns and examples, see [Use Send and Command](Use%20Send%20and%20Command.md).

Reach for the extras when the default model is not enough:

* Use [`Send`](https://reference.langchain.com/python/langgraph/types/Send) when you must run the same node once per item, each with its own input, and the item count is only known at runtime (map-reduce / orchestrator-worker).
* Use [`Command`](https://reference.langchain.com/python/langgraph/types/Command) when one step must both update state and choose the next node, resume after an [interrupt](../Capabilities/Interrupts.md), or update state from a tool.

```python
from typing import Literal

from langgraph.types import Command, Send


# Send: fan out one worker per item
def continue_to_jokes(state: OverallState):
    return [Send("generate_joke", {"subject": s}) for s in state["subjects"]]


# Command: update state and route in one return
def my_node(state: State) -> Command[Literal["my_other_node"]]:
    return Command(
        update={"foo": "bar"},
        goto="my_other_node",
    )
```

**4. Configure nodes as needed**

Add runtime options when reliability or cost matters:

* Retries and timeouts for flaky or slow steps
* Error handlers and graph-wide node defaults
* Caching for expensive repeated work
* Runtime context or config for dependencies that do not belong in state

```python
from langgraph.types import RetryPolicy

builder.add_node(
    "node_name",
    node_function,
    retry_policy=RetryPolicy(),
)
```

See [Configure nodes](Configure%20nodes.md).

**5. Visualize the graph**

Render a Mermaid or PNG diagram to review topology and debug routing.

```python
print(graph.get_graph().draw_mermaid())
```

See [Visualize your graph](Visualize%20your%20graph.md).

## Next steps

* [Thinking in the Graph API](Thinking%20in%20the%20Graph%20API.md): Design walkthrough with the email agent
* [Graph API overview](Graph%20API%20overview.md): Concepts for state, nodes, edges, `Send`, and `Command`
* [Define and update state](Define%20and%20update%20state.md)
* [Build sequences, branches, and loops](Build%20sequences%2C%20branches%2C%20and%20loops.md)
* [Use Send and Command](Use%20Send%20and%20Command.md)
* [Configure nodes](Configure%20nodes.md)
* [Visualize your graph](Visualize%20your%20graph.md)
* [LangGraph quickstart](../Get%20started/Quickstart.md): End-to-end calculator agent
* [Choosing between Graph and Functional APIs](../Get%20started/Choosing%20between%20Graph%20and%20Functional%20APIs.md)

# Choosing between Graph and Functional APIs

> Prefer the LangGraph Graph API for new workflows. Use the Functional API when wrapping other frameworks for LangSmith Deployment.

LangGraph provides two APIs for agent workflows: the [Graph API](../Build%20with%20the%20Graph%20API/Graph%20API%20overview.md) and the [Functional API](../Advanced/Build%20with%20the%20Functional%20API/Functional%20API%20overview.md). Both share the same runtime (persistence, streaming, human-in-the-loop, and memory).

The Graph API is the default. Prefer it for new LangGraph agents and for any workflow that benefits from explicit state, branching, or graph visualization.

Use the Functional API when you need to [deploy other frameworks](https://docs.langchain.com/langsmith/deploy-other-frameworks.md) on LangSmith Deployment. Wrap an existing Claude Agent SDK, Strands, CrewAI, AutoGen, or similar agent with `@entrypoint` and `@task` so Agent Server can run it with persistence, streaming, and tracing.

## Graph API (default)

Choose the Graph API when you build with LangGraph itself:

* Explicit shared [state](../Build%20with%20the%20Graph%20API/Graph%20API%20overview.md#state) across nodes
* Conditional branching and parallel paths that merge later
* Graph diagrams for debugging and documentation
* Team review of workflow structure

Start with the [Build checklist for the Graph API](../Build%20with%20the%20Graph%20API/Build%20checklist%20for%20the%20Graph%20API.md) or [Thinking in the Graph API](../Build%20with%20the%20Graph%20API/Thinking%20in%20the%20Graph%20API.md).

## Functional API (other frameworks)

Choose the Functional API when you already have an agent in another framework and want LangSmith Deployment features without rewriting that agent as a graph:

* Minimal changes to existing procedural or framework code
* Standard control flow (`if`/`else`, loops, function calls)
* Function-scoped values instead of a shared state schema

For the wrap-and-deploy pattern, see [Deploy other frameworks](https://docs.langchain.com/langsmith/deploy-other-frameworks.md). For Functional API concepts and how-tos, see the [Functional API overview](../Advanced/Build%20with%20the%20Functional%20API/Functional%20API%20overview.md).

## Side-by-side shape

The same small workflow looks different in each API. This example classifies a number, then returns a message:

```python Graph API
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

```python Functional API
from langgraph.func import entrypoint, task


@task
def is_even(number: int) -> bool:
    return number % 2 == 0


@task
def format_message(is_even: bool) -> str:
    return "The number is even." if is_even else "The number is odd."


@entrypoint()
def workflow(inputs: dict) -> str:
    even = is_even(inputs["number"]).result()
    return format_message(even).result()


workflow.invoke({"number": 7})
```

The Graph API makes state and transitions explicit. The Functional API keeps ordinary control flow and passes values between tasks.

| Concern | Graph API | Functional API |
| - | - | - |
| Style | Declarative nodes, edges, and shared state | Imperative functions with `@entrypoint` / `@task` (Python) or `entrypoint` / `task` (TypeScript) |
| Control flow | Edges and conditional edges | Language `if`/`else`, loops, and calls |
| State | Explicit [state](../Build%20with%20the%20Graph%20API/Graph%20API%20overview.md#state) and [reducers](../Build%20with%20the%20Graph%20API/Graph%20API%20overview.md#reducers) | Scoped to the entrypoint and tasks |
| Checkpointing | New checkpoint after each [super-step](../Build%20with%20the%20Graph%20API/Graph%20API%20overview.md) | Task results saved to the entrypoint checkpoint |
| Visualization | First-class graph diagrams | No static graph visualization (graph is built at runtime) |
| Best fit | Default for LangGraph workflows | Wrapping other frameworks for deployment |

You can still combine both APIs in one application when a linear Functional API sub-workflow sits inside a Graph API coordinator, or the reverse.

## See also

* [Build checklist for the Graph API](../Build%20with%20the%20Graph%20API/Build%20checklist%20for%20the%20Graph%20API.md)
* [Thinking in the Graph API](../Build%20with%20the%20Graph%20API/Thinking%20in%20the%20Graph%20API.md)
* [Graph API overview](../Build%20with%20the%20Graph%20API/Graph%20API%20overview.md)
* [Choose the unit of work](../Build%20with%20the%20Graph%20API/Graph%20API%20overview.md#choose-the-unit-of-work)
* [Deploy other frameworks](https://docs.langchain.com/langsmith/deploy-other-frameworks.md)
* [Functional API overview](../Advanced/Build%20with%20the%20Functional%20API/Functional%20API%20overview.md)

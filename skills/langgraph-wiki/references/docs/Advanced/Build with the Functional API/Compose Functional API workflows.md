# Compose Functional API workflows

> Build entrypoints and tasks, run work in parallel, and call graphs or other entrypoints.

Use these recipes to compose Functional API workflows from [entrypoint](https://reference.langchain.com/python/langgraph/func/entrypoint) and [task](https://reference.langchain.com/python/langgraph/func/task) building blocks.

For concepts, see the [Functional API overview](Functional%20API%20overview.md). For an ordered build path, see the [Build checklist for the Functional API](Build%20checklist%20for%20the%20Functional%20API.md).

The examples use an in-memory [checkpointer](../../Capabilities/Persistence.md) so results persist on a thread.

## Create a simple workflow

This is the even/odd flow from [Choosing between Graph and Functional APIs](../../Get%20started/Choosing%20between%20Graph%20and%20Functional%20APIs.md). This version adds a checkpointer so the run has a thread.

```python
from langchain_core.utils.uuid import uuid7
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.func import entrypoint, task


@task
def is_even(number: int) -> bool:
    return number % 2 == 0


@task
def format_message(is_even: bool) -> str:
    return "The number is even." if is_even else "The number is odd."


checkpointer = InMemorySaver()


@entrypoint(checkpointer=checkpointer)
def workflow(inputs: dict) -> str:
    even = is_even(inputs["number"]).result()
    return format_message(even).result()


config = {"configurable": {"thread_id": str(uuid7())}}
result = workflow.invoke({"number": 7}, config=config)
print(result)
```

An entrypoint takes one positional argument as input. To pass multiple fields, use a dictionary:

```python
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.func import entrypoint

checkpointer = InMemorySaver()


@entrypoint(checkpointer=checkpointer)
def my_workflow(inputs: dict) -> dict:
    value = inputs["value"]
    another_value = inputs["another_value"]
    return {"sum": value + another_value}


config = {"configurable": {"thread_id": "1"}}
my_workflow.invoke({"value": 1, "another_value": 2}, config)
```

## Run tasks in parallel

A task starts as soon as you call it and returns a future. Collect those futures first, then wait with `.result()` so the work overlaps.

This pattern helps I/O-bound work, for example LLM API calls.

```python
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.func import entrypoint, task

checkpointer = InMemorySaver()


@task
def add_one(number: int) -> int:
    return number + 1


@entrypoint(checkpointer=checkpointer)
def workflow(numbers: list[int]) -> list[int]:
    futures = [add_one(i) for i in numbers]
    return [f.result() for f in futures]
```

> [accordion] Extended example: parallel LLM calls
>
> Each task generates a paragraph on a different topic. Results join into one string.
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langchain.chat_models import init_chat_model
> from langchain_core.utils.uuid import uuid7
> from langgraph.checkpoint.memory import InMemorySaver
> from langgraph.func import entrypoint, task
>
> model = init_chat_model("claude-sonnet-4-6")
>
>
> @task
> def generate_paragraph(topic: str) -> str:
>     response = model.invoke([
>         {"role": "system", "content": "You are a helpful assistant that writes educational paragraphs."},
>         {"role": "user", "content": f"Write a paragraph about {topic}."}
>     ])
>     return response.text
>
>
> checkpointer = InMemorySaver()
>
>
> @entrypoint(checkpointer=checkpointer)
> def workflow(topics: list[str]) -> str:
>     futures = [generate_paragraph(topic) for topic in topics]
>     paragraphs = [f.result() for f in futures]
>     return "\n\n".join(paragraphs)
>
>
> config = {"configurable": {"thread_id": str(uuid7())}}
> result = workflow.invoke(["quantum computing", "climate change", "history of aviation"], config=config)
> print(result)
> ```

## Call a graph

The Functional API and the [Graph API](../../Build%20with%20the%20Graph%20API/Graph%20API%20overview.md) share the same runtime. A compiled graph is another callable: invoke it from an entrypoint like any other function.

A nested graph does not share the outer thread unless you pass `config` into `invoke`. Request the injected `config` on the entrypoint and forward it.

```python
from typing import TypedDict

from langchain_core.runnables import RunnableConfig
from langchain_core.utils.uuid import uuid7
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.func import entrypoint
from langgraph.graph import START, StateGraph


class State(TypedDict):
    foo: int


def double(state: State) -> State:
    return {"foo": state["foo"] * 2}


builder = StateGraph(State)
builder.add_node("double", double)
builder.add_edge(START, "double")
graph = builder.compile()

checkpointer = InMemorySaver()


@entrypoint(checkpointer=checkpointer)
def workflow(x: int, *, config: RunnableConfig) -> dict:
    result = graph.invoke({"foo": x}, config)
    return {"bar": result["foo"]}


config = {"configurable": {"thread_id": str(uuid7())}}
print(workflow.invoke(5, config=config))  # {'bar': 10}
```

## Call other entrypoints

You can call other entrypoints from within an entrypoint or a task.

When the child is defined without a checkpointer, invoking it from a parent that has one uses the parent's checkpointer. Invoking the child on its own does not persist unless you pass a checkpointer.

```python
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.func import entrypoint

checkpointer = InMemorySaver()


@entrypoint()  # Inherits the checkpointer when invoked from my_workflow
def some_other_workflow(inputs: dict) -> int:
    return inputs["value"]


@entrypoint(checkpointer=checkpointer)
def my_workflow(inputs: dict) -> int:
    value = some_other_workflow.invoke({"value": 1})
    return value
```

> [accordion] Extended example: calling another entrypoint
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langchain_core.utils.uuid import uuid7
> from langgraph.checkpoint.memory import InMemorySaver
> from langgraph.func import entrypoint
>
> checkpointer = InMemorySaver()
>
>
> @entrypoint()
> def multiply(inputs: dict) -> int:
>     return inputs["a"] * inputs["b"]
>
>
> @entrypoint(checkpointer=checkpointer)
> def main(inputs: dict) -> dict:
>     result = multiply.invoke({"a": inputs["x"], "b": inputs["y"]})
>     return {"product": result}
>
>
> config = {"configurable": {"thread_id": str(uuid7())}}
> print(main.invoke({"x": 6, "y": 7}, config=config))  # {'product': 42}
> ```

## See also

* [Functional API overview](Functional%20API%20overview.md)
* [Build checklist for the Functional API](Build%20checklist%20for%20the%20Functional%20API.md)
* [Workflows and agents](../../Patterns/Workflows%20and%20agents.md)
* [Add LangGraph's features to other frameworks using the Functional API](https://docs.langchain.com/langsmith/deploy-other-frameworks.md)

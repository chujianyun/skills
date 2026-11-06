# Add human-in-the-loop with the Functional API

> Pause Functional API workflows for approval and review tool calls with interrupts.

Pause a Functional API [entrypoint](Functional%20API%20overview.md#entrypoint) with [`interrupt`](https://reference.langchain.com/python/langgraph/types/interrupt) and resume with [`Command`](../../Capabilities/Interrupts.md#resuming-interrupts).

For concepts, see the [Functional API overview](Functional%20API%20overview.md). For interrupt payloads and resume shapes, see [Interrupts](../../Capabilities/Interrupts.md). Persistence requires a [checkpointer](../../Capabilities/Persistence.md) and a `thread_id`.

## Pause for feedback

Create three [tasks](Functional%20API%20overview.md#task):

1. Append `"bar"`.
2. Pause for human input. When resuming, append that input.
3. Append `"qux"`.

Compose them in an entrypoint. `interrupt` runs inside `human_feedback` after `step_1` has finished. Those results are persisted, so `step_1` does not run again after resume.

Identify the run with `thread_id`. Drive the stream until it pauses, print the interrupt payload, then resume.

```python
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.func import entrypoint, task
from langgraph.types import Command, interrupt


@task
def step_1(input_query):
    """Append bar."""
    return f"{input_query} bar"


@task
def human_feedback(input_query):
    """Append user input."""
    feedback = interrupt(f"Please provide feedback: {input_query}")
    return f"{input_query} {feedback}"


@task
def step_3(input_query):
    """Append qux."""
    return f"{input_query} qux"


checkpointer = InMemorySaver()


@entrypoint(checkpointer=checkpointer)
def workflow(input_query):
    result_1 = step_1(input_query).result()
    result_2 = human_feedback(result_1).result()
    result_3 = step_3(result_2).result()
    return result_3


config = {"configurable": {"thread_id": "1"}}

stream = workflow.stream_events("foo", config, version="v3")
_ = stream.output
print(stream.interrupts[0].value)
# -> 'Please provide feedback: foo bar'

stream = workflow.stream_events(Command(resume="baz"), config, version="v3")
print(stream.output)
# -> 'foo bar baz qux'
```

The `Command` `resume` value is the data `human_feedback` expects. After resume, the run continues through `step_3` and returns `foo bar baz qux`.

## Review tool calls

To review tool calls before execution, call `interrupt` from a helper. Execution pauses until you resume with `Command`.

Given a tool call, choose one of:

* Accept the tool call
* Revise the tool call and continue
* Generate a custom tool message (for example, instruct the model to re-format its tool call)

```python
from typing import Any, Literal, TypedDict, Union

from langchain.messages import ToolMessage
from langgraph.types import interrupt


class ToolCallReview(TypedDict, total=False):
    action: Literal["continue", "update", "feedback"]
    data: Any


def review_tool_call(tool_call: dict) -> Union[dict, ToolMessage]:
    """Review a tool call, returning a validated version."""
    human_review: ToolCallReview = interrupt(
        {
            "question": "Is this correct?",
            "tool_call": tool_call,
        }
    )
    review_action = human_review["action"]
    review_data = human_review.get("data")
    if review_action == "continue":
        return tool_call
    if review_action == "update":
        return {**tool_call, "args": review_data}
    if review_action == "feedback":
        return ToolMessage(
            content=review_data, name=tool_call["name"], tool_call_id=tool_call["id"]
        )
    raise ValueError(f"Unknown review action: {review_action}")
```

Wire the helper into an entrypoint. Accepted or revised calls run through `call_tool`. Feedback becomes a [`ToolMessage`](https://reference.langchain.com/python/langchain-core/messages/tool/ToolMessage) and skips execution. Prior task results, here the first model call, stay on the thread after the interrupt.

`call_model` and `call_tool` below are stand-ins. Replace them with your model and tools. For more, see [Add memory with the Functional API](Add%20memory%20with%20the%20Functional%20API.md).

The entrypoint restores prior messages from the checkpointer with `previous`.

```python
from langchain.messages import AIMessage, HumanMessage, ToolMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.func import entrypoint, task
from langgraph.graph import add_messages
from langgraph.types import Command


checkpointer = InMemorySaver()


@task
def call_model(messages: list) -> AIMessage:
    last = messages[-1]
    if isinstance(last, ToolMessage):
        return AIMessage(content="Search complete.")
    return AIMessage(
        content="",
        tool_calls=[
            {
                "name": "search",
                "args": {"query": "weather"},
                "id": "call_1",
                "type": "tool_call",
            }
        ],
    )


@task
def call_tool(tool_call: dict) -> ToolMessage:
    return ToolMessage(
        content=f"result for {tool_call['args']}",
        name=tool_call["name"],
        tool_call_id=tool_call["id"],
    )


@entrypoint(checkpointer=checkpointer)
def agent(messages, *, previous=None):
    if previous is not None:
        messages = add_messages(previous, messages)

    model_response = call_model(messages).result()
    while True:
        if not model_response.tool_calls:
            break

        # Review tool calls
        tool_results = []
        tool_calls = []
        updated_tool_calls = list(model_response.tool_calls)
        for i, tool_call in enumerate(model_response.tool_calls):
            review = review_tool_call(tool_call)
            if isinstance(review, ToolMessage):
                tool_results.append(review)
            else:  # is a validated tool call
                tool_calls.append(review)
                updated_tool_calls[i] = review

        if updated_tool_calls != list(model_response.tool_calls):
            model_response = model_response.model_copy(
                update={"tool_calls": updated_tool_calls}
            )

        # Execute remaining tool calls
        tool_result_futures = [call_tool(tool_call) for tool_call in tool_calls]
        remaining_tool_results = [fut.result() for fut in tool_result_futures]

        # Append to message list
        messages = add_messages(
            messages,
            [model_response, *tool_results, *remaining_tool_results],
        )

        # Call model again
        model_response = call_model(messages).result()

    # Generate final response
    messages = add_messages(messages, model_response)
    return entrypoint.final(value=model_response, save=messages)


config = {"configurable": {"thread_id": "2"}}

stream = agent.stream_events(
    [HumanMessage("What's the weather?")], config, version="v3"
)
_ = stream.output
print(stream.interrupts[0].value)
# -> {'question': 'Is this correct?', 'tool_call': {'name': 'search', ...}}

result = agent.invoke(Command(resume={"action": "continue"}), config)
print(result)
```

## See also

* [Functional API overview](Functional%20API%20overview.md)
* [Build checklist for the Functional API](Build%20checklist%20for%20the%20Functional%20API.md)
* [Interrupts](../../Capabilities/Interrupts.md)
* [Add memory with the Functional API](Add%20memory%20with%20the%20Functional%20API.md)
* [Stream with the Functional API](Stream%20with%20the%20Functional%20API.md)

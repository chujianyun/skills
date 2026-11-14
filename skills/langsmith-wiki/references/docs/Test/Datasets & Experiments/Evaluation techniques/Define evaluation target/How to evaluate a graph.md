# How to evaluate a graph

> [!NOTE]
>
> [langgraph](https://docs.langchain.com/oss/python/langgraph/overview.md)

`langgraph` is a library for building stateful, multi-actor applications with LLMs, used to create agent and multi-agent workflows. Evaluating `langgraph` graphs can be challenging because a single invocation can involve many LLM calls, and which LLM calls are made may depend on the outputs of preceding calls. In this guide we will focus on the mechanics of how to pass graphs and graph nodes to `evaluate()` / `aevaluate()`. For evaluation techniques and best practices when building agents head to the [LangSmith evaluation docs](../../../Get%20started/LangSmith%20Evaluation.md).

## End-to-end evaluations

The most common type of evaluation is an end-to-end one, where we want to evaluate the final graph output for each example input.

### Define a graph

Lets construct a simple ReACT agent to start:

```python
from typing import Annotated, Literal, TypedDict
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langgraph.prebuilt import ToolNode
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

class State(TypedDict):
    # Messages have the type "list". The 'add_messages' function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]

# Define the tools for the agent to use
@tool
def search(query: str) -> str:
    """Call to surf the web."""
    # This is a placeholder, but don't tell the LLM that...
    if "sf" in query.lower() or "san francisco" in query.lower():
        return "It's 60 degrees and foggy."
    return "It's 90 degrees and sunny."

tools = [search]
tool_node = ToolNode(tools)
model = init_chat_model("claude-sonnet-4-6").bind_tools(tools)

# Define the function that determines whether to continue or not
def should_continue(state: State) -> Literal["tools", END]:
    messages = state['messages']
    last_message = messages[-1]

    # If the LLM makes a tool call, then we route to the "tools" node
    if last_message.tool_calls:
        return "tools"

    # Otherwise, we stop (reply to the user)
    return END

# Define the function that calls the model
def call_model(state: State):
    messages = state['messages']
    response = model.invoke(messages)

    # We return a list, because this will get added to the existing list
    return {"messages": [response]}

# Define a new graph
workflow = StateGraph(State)

# Define the two nodes we will cycle between
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

# Set the entrypoint as 'agent'
# This means that this node is the first one called
workflow.add_edge(START, "agent")

# We now add a conditional edge
workflow.add_conditional_edges(
    # First, we define the start node. We use 'agent'.
    # This means these are the edges taken after the 'agent' node is called.
    "agent",
    # Next, we pass in the function that will determine which node is called next.
    should_continue,
)

# We now add a normal edge from 'tools' to 'agent'.
# This means that after 'tools' is called, 'agent' node is called next.
workflow.add_edge("tools", 'agent')

# Finally, we compile it!
# This compiles it into a LangChain Runnable,
# meaning you can use it as you would any other runnable.
# Note that we're (optionally) passing the memory when compiling the graph
app = workflow.compile()
```

### Create a dataset

Let's create a simple dataset of questions and expected responses:

```python
from langsmith import Client

questions = [
    "what's the weather in sf",
    "what's the weather in san fran",
    "what's the weather in tangier"
]

answers = [
    "It's 60 degrees and foggy.",
    "It's 60 degrees and foggy.",
    "It's 90 degrees and sunny.",
]

ls_client = Client()
dataset = ls_client.create_dataset("weather agent")
ls_client.create_examples(
    inputs=[{"question": q} for q in questions],
    outputs=[{"answer": a} for a in answers],
    dataset_id=dataset.id,
)
```

### Create an evaluator

And a simple evaluator:

Requires `langsmith>=0.2.0`

```python
judge_llm = init_chat_model("gpt-6.1-sol")

async def correct(outputs: dict, reference_outputs: dict) -> bool:
    instructions = (
        "Given an actual answer and an expected answer, determine whether"
        " the actual answer contains all of the information in the"
        " expected answer. Respond with 'CORRECT' if the actual answer"
        " does contain all of the expected information and 'INCORRECT'"
        " otherwise. Do not include anything else in your response."
    )
    # Our graph outputs a State dictionary, which in this case means
    # we'll have a 'messages' key and the final message should
    # be our actual answer.
    actual_answer = outputs["messages"][-1].content
    expected_answer = reference_outputs["answer"]
    user_msg = (
        f"ACTUAL ANSWER: {actual_answer}"
        f"\n\nEXPECTED ANSWER: {expected_answer}"
    )
    response = await judge_llm.ainvoke(
        [
            {"role": "system", "content": instructions},
            {"role": "user", "content": user_msg}
        ]
    )
    return response.content.upper() == "CORRECT"
```

### Run evaluations

Now we can run our evaluations and explore the results. We'll just need to wrap our graph function so that it can take inputs in the format they're stored on our example:

> [!NOTE]
>
> If all of your graph nodes are defined as sync functions then you can use `evaluate` or `aevaluate`. If any of you nodes are defined as async, you'll need to use `aevaluate`

Requires `langsmith>=0.2.0`

```python
import asyncio
from langsmith import aevaluate

def example_to_state(inputs: dict) -> dict:
  return {"messages": [{"role": "user", "content": inputs['question']}]}

# We use LCEL declarative syntax here.
# Remember that langgraph graphs are also langchain runnables.
target = example_to_state | app

async def main():
    experiment_results = await aevaluate(
        target,
        data="weather agent",
        evaluators=[correct],
        max_concurrency=4,  # optional
        experiment_prefix="claude-sonnet-4-6-baseline",  # optional
        metadata={  # optional, used to populate model/prompt/tool columns in UI
            "models": "google_genai:gemini-4-hydrogen",
            "tools": [{"name": "search", "description": "Call to surf the web."}],
        },
    )
    print(experiment_results)

asyncio.run(main())
```

## Evaluating intermediate steps

Often it is valuable to evaluate not only the final output of an agent but also the intermediate steps it has taken. What's nice about `langgraph` is that the output of a graph is a state object that often already carries information about the intermediate steps taken. Usually we can evaluate whatever we're interested in just by looking at the messages in our state. For example, we can look at the messages to assert that the model invoked the 'search' tool upon as a first step.

Requires `langsmith>=0.2.0`

```python
def right_tool(outputs: dict) -> bool:
    tool_calls = outputs["messages"][1].tool_calls
    return bool(tool_calls and tool_calls[0]["name"] == "search")

async def main():
    experiment_results = await aevaluate(
        target,
        data="weather agent",
        evaluators=[correct, right_tool],
        max_concurrency=4,  # optional
        experiment_prefix="claude-sonnet-4-6-baseline",  # optional
        metadata={  # optional, used to populate model/prompt/tool columns in UI
            "models": "google_genai:gemini-4-hydrogen",
            "tools": [{"name": "search", "description": "Call to surf the web."}],
        },
    )
    print(experiment_results)
```

If we need access to information about intermediate steps that isn't in state, we can look at the Run object. This contains the full traces for all node inputs and outputs:

> [!TIP]
>
> See more about what arguments you can pass to custom evaluators in this [how-to guide](../../../Evaluators/Evaluator%20types/UI/How%20to%20define%20a%20code%20evaluator.md).

```python
from langsmith.schemas import Run, Example

def right_tool_from_run(run: Run, example: Example) -> dict:
    # Get documents and answer
    first_model_run = next(run for run in root_run.child_runs if run.name == "agent")
    tool_calls = first_model_run.outputs["messages"][-1].tool_calls
    right_tool = bool(tool_calls and tool_calls[0]["name"] == "search")
    return {"key": "right_tool", "value": right_tool}

async def main():
    experiment_results = await aevaluate(
        target,
        data="weather agent",
        evaluators=[correct, right_tool_from_run],
        max_concurrency=4,  # optional
        experiment_prefix="claude-sonnet-4-6-baseline",  # optional
        metadata={  # optional, used to populate model/prompt/tool columns in UI
            "models": "google_genai:gemini-4-hydrogen",
            "tools": [{"name": "search", "description": "Call to surf the web."}],
        },
    )
    print(experiment_results)
```

## Running and evaluating individual nodes

Sometimes you want to evaluate a single node directly to save time and costs. `langgraph` makes it easy to do this. In this case we can even continue using the evaluators we've been using.

```python
node_target = example_to_state | app.nodes["agent"]

async def main():
    node_experiment_results = await aevaluate(
        node_target,
        data="weather agent",
        evaluators=[right_tool_from_run],
        max_concurrency=4,  # optional
        experiment_prefix="claude-sonnet-4-6-model-node",  # optional
        metadata={  # optional, used to populate model/prompt/tool columns in UI
            "models": "google_genai:gemini-4-hydrogen",
            "tools": [{"name": "search", "description": "Call to surf the web."}],
        },
    )
    print(node_experiment_results)
```

## Related

* [`langgraph` evaluation docs](../../../Get%20started/LangSmith%20Evaluation.md)

## Reference code

> [accordion] Click to see a consolidated code snippet
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import asyncio
> from typing import Annotated, Literal, TypedDict
> from langchain.chat_models import init_chat_model
> from langchain.tools import tool
> from langgraph.prebuilt import ToolNode
> from langgraph.graph import END, START, StateGraph
> from langgraph.graph.message import add_messages
> from langsmith import Client, aevaluate
>
> # Define a graph
> class State(TypedDict):
>     # Messages have the type "list". The 'add_messages' function
>     # in the annotation defines how this state key should be updated
>     # (in this case, it appends messages to the list, rather than overwriting them)
>     messages: Annotated[list, add_messages]
>
> # Define the tools for the agent to use
> @tool
> def search(query: str) -> str:
>     """Call to surf the web."""
>     # This is a placeholder, but don't tell the LLM that...
>     if "sf" in query.lower() or "san francisco" in query.lower():
>         return "It's 60 degrees and foggy."
>     return "It's 90 degrees and sunny."
>
> tools = [search]
> tool_node = ToolNode(tools)
> model = init_chat_model("claude-sonnet-4-6").bind_tools(tools)
>
> # Define the function that determines whether to continue or not
> def should_continue(state: State) -> Literal["tools", END]:
>     messages = state['messages']
>     last_message = messages[-1]
>
>     # If the LLM makes a tool call, then we route to the "tools" node
>     if last_message.tool_calls:
>         return "tools"
>
>     # Otherwise, we stop (reply to the user)
>     return END
>
> # Define the function that calls the model
> def call_model(state: State):
>     messages = state['messages']
>     response = model.invoke(messages)
>     # We return a list, because this will get added to the existing list
>     return {"messages": [response]}
>
> # Define a new graph
> workflow = StateGraph(State)
>
> # Define the two nodes we will cycle between
> workflow.add_node("agent", call_model)
> workflow.add_node("tools", tool_node)
>
> # Set the entrypoint as 'agent'
> # This means that this node is the first one called
> workflow.add_edge(START, "agent")
>
> # We now add a conditional edge
> workflow.add_conditional_edges(
>     # First, we define the start node. We use 'agent'.
>     # This means these are the edges taken after the 'agent' node is called.
>     "agent",
>     # Next, we pass in the function that will determine which node is called next.
>     should_continue,
> )
>
> # We now add a normal edge from 'tools' to 'agent'.
> # This means that after 'tools' is called, 'agent' node is called next.
> workflow.add_edge("tools", 'agent')
>
> # Finally, we compile it!
> # This compiles it into a LangChain Runnable,
> # meaning you can use it as you would any other runnable.
> # Note that we're (optionally) passing the memory when compiling the graph
> app = workflow.compile()
>
> questions = [
>     "what's the weather in sf",
>     "what's the weather in san fran",
>     "what's the weather in tangier"
> ]
>
> answers = [
>     "It's 60 degrees and foggy.",
>     "It's 60 degrees and foggy.",
>     "It's 90 degrees and sunny.",
> ]
>
> # Create a dataset
> ls_client = Client()
> dataset = ls_client.create_dataset("weather agent")
> ls_client.create_examples(
>     inputs=[{"question": q} for q in questions],
>     outputs=[{"answer": a} for a in answers],
>     dataset_id=dataset.id,
> )
>
> # Define evaluators
>
> judge_llm = init_chat_model("gpt-6.1-sol")
>
> async def correct(outputs: dict, reference_outputs: dict) -> bool:
>     instructions = (
>         "Given an actual answer and an expected answer, determine whether"
>         " the actual answer contains all of the information in the"
>         " expected answer. Respond with 'CORRECT' if the actual answer"
>         " does contain all of the expected information and 'INCORRECT'"
>         " otherwise. Do not include anything else in your response."
>     )
>     # Our graph outputs a State dictionary, which in this case means
>     # we'll have a 'messages' key and the final message should
>     # be our actual answer.
>     actual_answer = outputs["messages"][-1].content
>     expected_answer = reference_outputs["answer"]
>     user_msg = (
>         f"ACTUAL ANSWER: {actual_answer}"
>         f"\n\nEXPECTED ANSWER: {expected_answer}"
>     )
>     response = await judge_llm.ainvoke(
>         [
>             {"role": "system", "content": instructions},
>             {"role": "user", "content": user_msg}
>         ]
>     )
>     return response.content.upper() == "CORRECT"
>
> def right_tool(outputs: dict) -> bool:
>     tool_calls = outputs["messages"][1].tool_calls
>     return bool(tool_calls and tool_calls[0]["name"] == "search")
>
> def example_to_state(inputs: dict) -> dict:
>   return {"messages": [{"role": "user", "content": inputs['question']}]}
>
> # We use LCEL declarative syntax here.
> # Remember that langgraph graphs are also langchain runnables.
> target = example_to_state | app
>
> # Run evaluation
> async def main():
>     experiment_results = await aevaluate(
>         target,
>         data="weather agent",
>         evaluators=[correct, right_tool],
>         max_concurrency=4,  # optional
>         experiment_prefix="claude-sonnet-4-6-baseline",  # optional
>         metadata={  # optional, used to populate model/prompt/tool columns in UI
>             "models": "google_genai:gemini-4-hydrogen",
>             "tools": [{"name": "search", "description": "Call to surf the web."}],
>         },
>     )
>     print(experiment_results)
>
> asyncio.run(main())
> ```

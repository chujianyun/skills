# Agent Evals

> Evaluate agent trajectories using deterministic matching or LLM-as-judge evaluators with AgentEvals and LangSmith.

Evaluations ("evals") measure how well your agent performs by assessing its execution trajectory, the sequence of messages and tool calls it produces. Unlike [integration tests](Integration%20testing.md) that verify basic correctness, evals score agent behavior against a reference or rubric, making them useful for catching regressions when you change prompts, tools, or models.

An evaluator is a function that takes agent outputs (and optionally reference outputs) and returns a score:

```python
def evaluator(*, outputs: dict, reference_outputs: dict):
    output_messages = outputs["messages"]
    reference_messages = reference_outputs["messages"]
    score = compare_messages(output_messages, reference_messages)
    return {"key": "evaluator_score", "score": score}
```

The [`agentevals`](https://github.com/langchain-ai/agentevals) package provides prebuilt evaluators for agent trajectories. You can evaluate by performing a **trajectory match** (deterministic comparison) or by using an **LLM judge** (qualitative assessment):

| Approach | When to use |
| - | - |
| [Trajectory match](#trajectory-match-evaluator) | You know the expected tool calls and want fast, deterministic, cost-free checks |
| [LLM-as-judge](#llm-as-judge-evaluator) | You want to assess overall quality and reasoning without strict expectations |

## Install AgentEvals

```bash pip
pip install -U agentevals
```

```bash uv
uv add agentevals
```

Or, clone the [AgentEvals repository](https://github.com/langchain-ai/agentevals) directly.

## Trajectory match evaluator

AgentEvals offers the `create_trajectory_match_evaluator` function to match your agent's trajectory against a reference. There are four modes:

| Mode | Description | Use case |
| - | - | - |
| `strict` | Exact match of message structure and tool calls in the same order (message content can differ) | Testing specific sequences (e.g., policy lookup before authorization) |
| `unordered` | Same message structure and tool calls as reference, but tool calls can happen in any order | Verifying information retrieval when order doesn't matter |
| `subset` | Agent calls only tools from reference (no extras) | Ensuring agent doesn't exceed expected scope |
| `superset` | Agent calls at least the reference tools (extras allowed) | Verifying minimum required actions are taken |

The examples below share a common setup, an agent with a `get_weather` tool:

```python
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import HumanMessage, AIMessage, ToolMessage
from agentevals.trajectory.match import create_trajectory_match_evaluator


@tool
def get_weather(city: str):
    """Get weather information for a city."""
    return f"It's 75 degrees and sunny in {city}."

agent = create_agent("claude-sonnet-4-6", tools=[get_weather])
```

> [accordion] Strict match
>
> The `strict` mode ensures trajectories contain identical messages in the same order with the same tool calls, though it allows for differences in message content. This is useful when you need to enforce a specific sequence of operations, such as requiring a policy lookup before authorizing an action.
>
> ```python
> evaluator = create_trajectory_match_evaluator(  # [!code highlight]
>     trajectory_match_mode="strict",  # [!code highlight]
> )  # [!code highlight]
>
> def test_weather_tool_called_strict():
>     result = agent.invoke({
>         "messages": [HumanMessage(content="What's the weather in San Francisco?")]
>     })
>
>     reference_trajectory = [
>         HumanMessage(content="What's the weather in San Francisco?"),
>         AIMessage(content="", tool_calls=[
>             {"id": "call_1", "name": "get_weather", "args": {"city": "San Francisco"}}
>         ]),
>         ToolMessage(content="It's 75 degrees and sunny in San Francisco.", tool_call_id="call_1"),
>         AIMessage(content="The weather in San Francisco is 75 degrees and sunny."),
>     ]
>
>     evaluation = evaluator(
>         outputs=result["messages"],
>         reference_outputs=reference_trajectory
>     )
>     # {
>     #     'key': 'trajectory_strict_match',
>     #     'score': True,
>     #     'comment': None,
>     # }
>     assert evaluation["score"] is True
> ```

> [accordion] Unordered match
>
> The `unordered` mode allows the same tool calls in any order. This is helpful when you want to verify that specific information was retrieved but don't care about the sequence. For example, an agent that checks both weather and events for a city with different tool calls.
>
> ```python
> @tool
> def get_events(city: str):
>     """Get events happening in a city."""
>     return f"Concert at the park in {city} tonight."
>
> agent = create_agent("claude-sonnet-4-6", tools=[get_weather, get_events])
>
> evaluator = create_trajectory_match_evaluator(  # [!code highlight]
>     trajectory_match_mode="unordered",  # [!code highlight]
> )  # [!code highlight]
>
> def test_multiple_tools_any_order():
>     result = agent.invoke({
>         "messages": [HumanMessage(content="What's happening in SF today?")]
>     })
>
>     reference_trajectory = [
>         HumanMessage(content="What's happening in SF today?"),
>         AIMessage(content="", tool_calls=[
>             {"id": "call_1", "name": "get_events", "args": {"city": "SF"}},
>             {"id": "call_2", "name": "get_weather", "args": {"city": "SF"}},
>         ]),
>         ToolMessage(content="Concert at the park in SF tonight.", tool_call_id="call_1"),
>         ToolMessage(content="It's 75 degrees and sunny in SF.", tool_call_id="call_2"),
>         AIMessage(content="Today in SF: 75 degrees and sunny with a concert at the park tonight."),
>     ]
>
>     evaluation = evaluator(
>         outputs=result["messages"],
>         reference_outputs=reference_trajectory,
>     )
>     assert evaluation["score"] is True
> ```

> [accordion] Subset and superset match
>
> The `superset` and `subset` modes match partial trajectories. The `superset` mode verifies that the agent called at least the tools in the reference trajectory, allowing additional tool calls. The `subset` mode ensures the agent did not call any tools beyond those in the reference.
>
> ```python
> @tool
> def get_detailed_forecast(city: str):
>     """Get detailed weather forecast for a city."""
>     return f"Detailed forecast for {city}: sunny all week."
>
> agent = create_agent("claude-sonnet-4-6", tools=[get_weather, get_detailed_forecast])
>
> evaluator = create_trajectory_match_evaluator(  # [!code highlight]
>     trajectory_match_mode="superset",  # [!code highlight]
> )  # [!code highlight]
>
> def test_agent_calls_required_tools_plus_extra():
>     result = agent.invoke({
>         "messages": [HumanMessage(content="What's the weather in Boston?")]
>     })
>
>     # Reference only requires get_weather, but agent may call additional tools
>     reference_trajectory = [
>         HumanMessage(content="What's the weather in Boston?"),
>         AIMessage(content="", tool_calls=[
>             {"id": "call_1", "name": "get_weather", "args": {"city": "Boston"}},
>         ]),
>         ToolMessage(content="It's 75 degrees and sunny in Boston.", tool_call_id="call_1"),
>         AIMessage(content="The weather in Boston is 75 degrees and sunny."),
>     ]
>
>     evaluation = evaluator(
>         outputs=result["messages"],
>         reference_outputs=reference_trajectory,
>     )
>     assert evaluation["score"] is True
> ```

> [!NOTE]
>
> You can also set the `tool_args_match_mode` property and/or `tool_args_match_overrides` to customize how the evaluator considers equality between tool calls in the actual trajectory vs. the reference. By default, only tool calls with the same arguments to the same tool are considered equal. Visit the [repository](https://github.com/langchain-ai/agentevals?tab=readme-ov-file#tool-args-match-modes) for more details.

## LLM-as-judge evaluator

You can use an LLM to evaluate the agent's execution path with the `create_trajectory_llm_as_judge` function. Unlike trajectory match evaluators, it doesn't require a reference trajectory, but one can be provided if available.

> [accordion] Without reference trajectory
>
> ```python
> from agentevals.trajectory.llm import create_trajectory_llm_as_judge, TRAJECTORY_ACCURACY_PROMPT
>
> evaluator = create_trajectory_llm_as_judge(  # [!code highlight]
>     model="openai:gpt-5.4-mini",  # [!code highlight]
>     prompt=TRAJECTORY_ACCURACY_PROMPT,  # [!code highlight]
> )  # [!code highlight]
>
> def test_trajectory_quality():
>     result = agent.invoke({
>         "messages": [HumanMessage(content="What's the weather in Seattle?")]
>     })
>
>     evaluation = evaluator(
>         outputs=result["messages"],
>     )
>     assert evaluation["score"] is True
> ```

> [accordion] With reference trajectory
>
> If you have a reference trajectory, use the prebuilt `TRAJECTORY_ACCURACY_PROMPT_WITH_REFERENCE` prompt:
>
> ```python
> from agentevals.trajectory.llm import create_trajectory_llm_as_judge, TRAJECTORY_ACCURACY_PROMPT_WITH_REFERENCE
>
> evaluator = create_trajectory_llm_as_judge(
>     model="openai:gpt-5.4-mini",
>     prompt=TRAJECTORY_ACCURACY_PROMPT_WITH_REFERENCE,
> )
> evaluation = evaluator(
>     outputs=result["messages"],
>     reference_outputs=reference_trajectory,
> )
> ```

> [!NOTE]
>
> For more configurability over how the LLM evaluates the trajectory, visit the [repository](https://github.com/langchain-ai/agentevals?tab=readme-ov-file#trajectory-llm-as-judge).

### Async support

All `agentevals` evaluators support Python asyncio. Async versions are available by adding `async` after `create_` in the function name.

> [accordion] Async judge and evaluator example
>
> ```python
> from agentevals.trajectory.llm import create_async_trajectory_llm_as_judge, TRAJECTORY_ACCURACY_PROMPT
> from agentevals.trajectory.match import create_async_trajectory_match_evaluator
>
> async_judge = create_async_trajectory_llm_as_judge(
>     model="openai:gpt-5.4-mini",
>     prompt=TRAJECTORY_ACCURACY_PROMPT,
> )
>
> async_evaluator = create_async_trajectory_match_evaluator(
>     trajectory_match_mode="strict",
> )
>
> async def test_async_evaluation():
>     result = await agent.ainvoke({
>         "messages": [HumanMessage(content="What's the weather?")]
>     })
>
>     evaluation = await async_judge(outputs=result["messages"])
>     assert evaluation["score"] is True
> ```

## Run evals in LangSmith

For tracking experiments over time, log evaluator results to [LangSmith](https://smith.langchain.com?utm_source=docs\&utm_medium=cta\&utm_campaign=langsmith-signup\&utm_content=oss-langchain-test-evals). First, set the required environment variables:

```bash
export LANGSMITH_API_KEY="<API_KEY>"
export LANGSMITH_TRACING="true"
```

LangSmith offers two main approaches for running evaluations: [pytest](https://docs.langchain.com/langsmith/pytest.md) integration and the `evaluate` function.

> [accordion] Use pytest integration
>
> ```python
> import pytest
> from langsmith import testing as t
> from agentevals.trajectory.llm import create_trajectory_llm_as_judge, TRAJECTORY_ACCURACY_PROMPT
>
> trajectory_evaluator = create_trajectory_llm_as_judge(
>     model="openai:gpt-5.4-mini",
>     prompt=TRAJECTORY_ACCURACY_PROMPT,
> )
>
> @pytest.mark.langsmith
> def test_trajectory_accuracy():
>     result = agent.invoke({
>         "messages": [HumanMessage(content="What's the weather in SF?")]
>     })
>
>     reference_trajectory = [
>         HumanMessage(content="What's the weather in SF?"),
>         AIMessage(content="", tool_calls=[
>             {"id": "call_1", "name": "get_weather", "args": {"city": "SF"}},
>         ]),
>         ToolMessage(content="It's 75 degrees and sunny in SF.", tool_call_id="call_1"),
>         AIMessage(content="The weather in SF is 75 degrees and sunny."),
>     ]
>
>     t.log_inputs({})
>     t.log_outputs({"messages": result["messages"]})
>     t.log_reference_outputs({"messages": reference_trajectory})
>
>     trajectory_evaluator(
>         outputs=result["messages"],
>         reference_outputs=reference_trajectory
>     )
> ```
>
> Run the evaluation with pytest:
>
> ```bash
> pytest test_trajectory.py --langsmith-output
> ```

> [accordion] Use the evaluate function
>
> Create a [LangSmith dataset](https://docs.langchain.com/langsmith/manage-datasets.md) and use the `evaluate` function. The dataset must have the following schema:
>
> * **input**: `{"messages": [...]}` input messages to call the agent with.
> * **output**: `{"messages": [...]}` expected message history in the agent output. For trajectory evaluation, you can choose to keep only assistant messages.
>
> ```python
> from langsmith import Client
> from agentevals.trajectory.llm import create_trajectory_llm_as_judge, TRAJECTORY_ACCURACY_PROMPT
>
> client = Client()
>
> trajectory_evaluator = create_trajectory_llm_as_judge(
>     model="openai:gpt-5.4-mini",
>     prompt=TRAJECTORY_ACCURACY_PROMPT,
> )
>
> def run_agent(inputs):
>     return agent.invoke(inputs)["messages"]
>
> experiment_results = client.evaluate(
>     run_agent,
>     data="your_dataset_name",
>     evaluators=[trajectory_evaluator]
> )
> ```

> [!TIP]
>
> To learn more about evaluating your agent, see the [LangSmith docs](https://docs.langchain.com/langsmith/pytest.md).

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/test/evals.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

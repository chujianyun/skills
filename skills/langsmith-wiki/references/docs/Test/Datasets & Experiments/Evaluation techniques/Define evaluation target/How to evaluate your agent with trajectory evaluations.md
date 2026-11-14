# How to evaluate your agent with trajectory evaluations

Many agent behaviors only emerge when using a real LLM, such as which tool the agent decides to call, how it formats responses, or whether a prompt modification affects the entire execution trajectory. LangChain's [`agentevals`](https://github.com/langchain-ai/agentevals) package provides evaluators specifically designed for testing agent trajectories with live models.

> [!NOTE]
>
> This guide covers the open source [LangChain](https://docs.langchain.com/oss/python/langchain/overview.md) `agentevals` package, which integrates with LangSmith for trajectory evaluation.

AgentEvals allows you to evaluate the trajectory of your agent (the exact sequence of messages, including tool calls) by performing a *trajectory match* or by using an *LLM judge*:

> [card] [Trajectory match](#trajectory-match-evaluator)
>
> Hard-code a reference trajectory for a given input and validate the run via a step-by-step comparison.
>
> Ideal for testing well-defined workflows where you know the expected behavior. Use when you have specific expectations about which tools should be called and in what order. This approach is deterministic, fast, and cost-effective since it doesn't require additional LLM calls.

> [card] [LLM-as-judge](#llm-as-judge-evaluator)
>
> Use an LLM to qualitatively validate your agent's execution trajectory. The "judge" LLM reviews the agent's decisions against a prompt rubric (which can include a reference trajectory).
>
> More flexible and can assess nuanced aspects like efficiency and appropriateness, but requires an LLM call and is less deterministic. Use when you want to evaluate the overall quality and reasonableness of the agent's trajectory without strict tool call or ordering requirements.

## Installing AgentEvals

```bash Python
pip install agentevals
```

```bash TypeScript
npm install agentevals @langchain/core
```

Or, clone the [AgentEvals repository](https://github.com/langchain-ai/agentevals) directly.

## Trajectory match evaluator

AgentEvals offers the `create_trajectory_match_evaluator` function in Python and `createTrajectoryMatchEvaluator` in TypeScript to match your agent's trajectory against a reference trajectory.

You can use the following modes:

| Mode | Description | Use Case |
| - | - | - |
| [`strict`](#strict-match) | Exact match of messages and tool calls in the same order | Testing specific sequences (e.g., policy lookup before authorization) |
| [`unordered`](#unordered-match) | Same tool calls allowed in any order | Verifying information retrieval when order doesn't matter |
| [`subset`](#subset-and-superset-match) | Agent calls only tools from reference (no extras) | Ensuring agent doesn't exceed expected scope |
| [`superset`](#subset-and-superset-match) | Agent calls at least the reference tools (extras allowed) | Verifying minimum required actions are taken |

### Strict match

The `strict` mode ensures trajectories contain identical messages in the same order with the same tool calls, though it allows for differences in message content. This is useful when you need to enforce a specific sequence of operations, such as requiring a policy lookup before authorizing an action.

```python Python
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import HumanMessage, AIMessage, ToolMessage
from agentevals.trajectory.match import create_trajectory_match_evaluator


@tool
def get_weather(city: str):
    """Get weather information for a city."""
    return f"It's 75 degrees and sunny in {city}."

agent = create_agent("gpt-6.1-sol", tools=[get_weather])

evaluator = create_trajectory_match_evaluator(  # [!code highlight]
    trajectory_match_mode="strict",  # [!code highlight]
)  # [!code highlight]

def test_weather_tool_called_strict():
    result = agent.invoke({
        "messages": [HumanMessage(content="What's the weather in San Francisco?")]
    })

    reference_trajectory = [
        HumanMessage(content="What's the weather in San Francisco?"),
        AIMessage(content="", tool_calls=[
            {"id": "call_1", "name": "get_weather", "args": {"city": "San Francisco"}}
        ]),
        ToolMessage(content="It's 75 degrees and sunny in San Francisco.", tool_call_id="call_1"),
        AIMessage(content="The weather in San Francisco is 75 degrees and sunny."),
    ]

    evaluation = evaluator(
        outputs=result["messages"],
        reference_outputs=reference_trajectory
    )
    # {
    #     'key': 'trajectory_strict_match',
    #     'score': True,
    #     'comment': None,
    # }
    assert evaluation["score"] is True
```

```ts TypeScript
import { createAgent, tool, HumanMessage, AIMessage, ToolMessage } from "langchain"
import { createTrajectoryMatchEvaluator } from "agentevals";
import * as z from "zod";

const getWeather = tool(
  async ({ city }: { city: string }) => {
    return `It's 75 degrees and sunny in ${city}.`;
  },
  {
    name: "get_weather",
    description: "Get weather information for a city.",
    schema: z.object({
      city: z.string(),
    }),
  }
);

const agent = createAgent({
  model: "gpt-6.1-sol",
  tools: [getWeather]
});

const evaluator = createTrajectoryMatchEvaluator({  // [!code highlight]
  trajectoryMatchMode: "strict",  // [!code highlight]
});  // [!code highlight]

async function testWeatherToolCalledStrict() {
  const result = await agent.invoke({
    messages: [new HumanMessage("What's the weather in San Francisco?")]
  });

  const referenceTrajectory = [
    new HumanMessage("What's the weather in San Francisco?"),
    new AIMessage({
      content: "",
      tool_calls: [
        { id: "call_1", name: "get_weather", args: { city: "San Francisco" } }
      ]
    }),
    new ToolMessage({
      content: "It's 75 degrees and sunny in San Francisco.",
      tool_call_id: "call_1"
    }),
    new AIMessage("The weather in San Francisco is 75 degrees and sunny."),
  ];

  const evaluation = await evaluator({
    outputs: result.messages,
    referenceOutputs: referenceTrajectory
  });
  // {
  //     'key': 'trajectory_strict_match',
  //     'score': true,
  //     'comment': null,
  // }
  expect(evaluation.score).toBe(true);
}
```

### Unordered match

The `unordered` mode allows the same tool calls in any order, which is helpful when you want to verify that the correct set of tools are being invoked but don't care about the sequence. For example, an agent might need to check both weather and events for a city, but the order doesn't matter.

```python Python
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import HumanMessage, AIMessage, ToolMessage
from agentevals.trajectory.match import create_trajectory_match_evaluator


@tool
def get_weather(city: str):
    """Get weather information for a city."""
    return f"It's 75 degrees and sunny in {city}."

@tool
def get_events(city: str):
    """Get events happening in a city."""
    return f"Concert at the park in {city} tonight."

agent = create_agent("gpt-6.1-sol", tools=[get_weather, get_events])

evaluator = create_trajectory_match_evaluator(  # [!code highlight]
    trajectory_match_mode="unordered",  # [!code highlight]
)  # [!code highlight]

def test_multiple_tools_any_order():
    result = agent.invoke({
        "messages": [HumanMessage(content="What's happening in SF today?")]
    })

    # Reference shows tools called in different order than actual execution
    reference_trajectory = [
        HumanMessage(content="What's happening in SF today?"),
        AIMessage(content="", tool_calls=[
            {"id": "call_1", "name": "get_events", "args": {"city": "SF"}},
            {"id": "call_2", "name": "get_weather", "args": {"city": "SF"}},
        ]),
        ToolMessage(content="Concert at the park in SF tonight.", tool_call_id="call_1"),
        ToolMessage(content="It's 75 degrees and sunny in SF.", tool_call_id="call_2"),
        AIMessage(content="Today in SF: 75 degrees and sunny with a concert at the park tonight."),
    ]

    evaluation = evaluator(
        outputs=result["messages"],
        reference_outputs=reference_trajectory,
    )
    # {
    #     'key': 'trajectory_unordered_match',
    #     'score': True,
    # }
    assert evaluation["score"] is True
```

```ts TypeScript
import { createAgent, tool, HumanMessage, AIMessage, ToolMessage } from "langchain"
import { createTrajectoryMatchEvaluator } from "agentevals";
import * as z from "zod";

const getWeather = tool(
  async ({ city }: { city: string }) => {
    return `It's 75 degrees and sunny in ${city}.`;
  },
  {
    name: "get_weather",
    description: "Get weather information for a city.",
    schema: z.object({ city: z.string() }),
  }
);

const getEvents = tool(
  async ({ city }: { city: string }) => {
    return `Concert at the park in ${city} tonight.`;
  },
  {
    name: "get_events",
    description: "Get events happening in a city.",
    schema: z.object({ city: z.string() }),
  }
);

const agent = createAgent({
  model: "gpt-6.1-sol",
  tools: [getWeather, getEvents]
});

const evaluator = createTrajectoryMatchEvaluator({  // [!code highlight]
  trajectoryMatchMode: "unordered",  // [!code highlight]
});  // [!code highlight]

async function testMultipleToolsAnyOrder() {
  const result = await agent.invoke({
    messages: [new HumanMessage("What's happening in SF today?")]
  });

  // Reference shows tools called in different order than actual execution
  const referenceTrajectory = [
    new HumanMessage("What's happening in SF today?"),
    new AIMessage({
      content: "",
      tool_calls: [
        { id: "call_1", name: "get_events", args: { city: "SF" } },
        { id: "call_2", name: "get_weather", args: { city: "SF" } },
      ]
    }),
    new ToolMessage({
      content: "Concert at the park in SF tonight.",
      tool_call_id: "call_1"
    }),
    new ToolMessage({
      content: "It's 75 degrees and sunny in SF.",
      tool_call_id: "call_2"
    }),
    new AIMessage("Today in SF: 75 degrees and sunny with a concert at the park tonight."),
  ];

  const evaluation = await evaluator({
    outputs: result.messages,
    referenceOutputs: referenceTrajectory,
  });
  // {
  //     'key': 'trajectory_unordered_match',
  //     'score': true,
  // }
  expect(evaluation.score).toBe(true);
}
```

### Subset and superset match

The `superset` and `subset` modes focus on which tools are called rather than the order of tool calls, allowing you to control how strictly the agent's tool calls must align with the reference.

* Use `superset` mode when you want to verify that a few key tools are called in the execution, but you're okay with the agent calling additional tools. The agent's trajectory must include at least all the tool calls in the reference trajectory, and may include additional tool calls beyond the reference.
* Use `subset` mode to ensure agent efficiency by verifying that the agent did not call any irrelevant or unnecessary tools beyond those in the reference. The agent's trajectory must include only tool calls that appear in the reference trajectory.

The following example demonstrates `superset` mode, where the reference trajectory only requires the `get_weather` tool, but the agent can call additional tools:

```python Python
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import HumanMessage, AIMessage, ToolMessage
from agentevals.trajectory.match import create_trajectory_match_evaluator


@tool
def get_weather(city: str):
    """Get weather information for a city."""
    return f"It's 75 degrees and sunny in {city}."

@tool
def get_detailed_forecast(city: str):
    """Get detailed weather forecast for a city."""
    return f"Detailed forecast for {city}: sunny all week."

agent = create_agent("gpt-6.1-sol", tools=[get_weather, get_detailed_forecast])

evaluator = create_trajectory_match_evaluator(  # [!code highlight]
    trajectory_match_mode="superset",  # [!code highlight]
)  # [!code highlight]

def test_agent_calls_required_tools_plus_extra():
    result = agent.invoke({
        "messages": [HumanMessage(content="What's the weather in Boston?")]
    })

    # Reference only requires get_weather, but agent may call additional tools
    reference_trajectory = [
        HumanMessage(content="What's the weather in Boston?"),
        AIMessage(content="", tool_calls=[
            {"id": "call_1", "name": "get_weather", "args": {"city": "Boston"}},
        ]),
        ToolMessage(content="It's 75 degrees and sunny in Boston.", tool_call_id="call_1"),
        AIMessage(content="The weather in Boston is 75 degrees and sunny."),
    ]

    evaluation = evaluator(
        outputs=result["messages"],
        reference_outputs=reference_trajectory,
    )
    # {
    #     'key': 'trajectory_superset_match',
    #     'score': True,
    #     'comment': None,
    # }
    assert evaluation["score"] is True
```

```ts TypeScript
import { createAgent } from "langchain"
import { tool } from "@langchain/core/tools";
import { HumanMessage, AIMessage, ToolMessage } from "@langchain/core/messages";
import { createTrajectoryMatchEvaluator } from "agentevals";
import * as z from "zod";

const getWeather = tool(
  async ({ city }: { city: string }) => {
    return `It's 75 degrees and sunny in ${city}.`;
  },
  {
    name: "get_weather",
    description: "Get weather information for a city.",
    schema: z.object({ city: z.string() }),
  }
);

const getDetailedForecast = tool(
  async ({ city }: { city: string }) => {
    return `Detailed forecast for ${city}: sunny all week.`;
  },
  {
    name: "get_detailed_forecast",
    description: "Get detailed weather forecast for a city.",
    schema: z.object({ city: z.string() }),
  }
);

const agent = createAgent({
  model: "gpt-6.1-sol",
  tools: [getWeather, getDetailedForecast]
});

const evaluator = createTrajectoryMatchEvaluator({  // [!code highlight]
  trajectoryMatchMode: "superset",  // [!code highlight]
});  // [!code highlight]

async function testAgentCallsRequiredToolsPlusExtra() {
  const result = await agent.invoke({
    messages: [new HumanMessage("What's the weather in Boston?")]
  });

  // Reference only requires getWeather, but agent may call additional tools
  const referenceTrajectory = [
    new HumanMessage("What's the weather in Boston?"),
    new AIMessage({
      content: "",
      tool_calls: [
        { id: "call_1", name: "get_weather", args: { city: "Boston" } },
      ]
    }),
    new ToolMessage({
      content: "It's 75 degrees and sunny in Boston.",
      tool_call_id: "call_1"
    }),
    new AIMessage("The weather in Boston is 75 degrees and sunny."),
  ];

  const evaluation = await evaluator({
    outputs: result.messages,
    referenceOutputs: referenceTrajectory,
  });
  // {
  //     'key': 'trajectory_superset_match',
  //     'score': true,
  //     'comment': null,
  // }
  expect(evaluation.score).toBe(true);
}
```

> [!NOTE]
>
> You can also customize how the evaluator considers equality between tool calls in the actual trajectory vs. the reference by setting the `tool_args_match_mode` (Python) or `toolArgsMatchMode` (TypeScript) property, as well as the `tool_args_match_overrides` (Python) or `toolArgsMatchOverrides` (TypeScript) property. By default, only tool calls with the same arguments to the same tool are considered equal. Visit the [repository](https://github.com/langchain-ai/agentevals?tab=readme-ov-file#tool-args-match-modes) for more details.

## LLM-as-judge evaluator

> [!NOTE]
>
> This section covers the trajectory-specific LLM-as-a-judge evaluator from the `agentevals` package. For general-purpose LLM-as-a-judge evaluators in LangSmith, refer to the [LLM-as-a-judge evaluator](../../../Evaluators/Evaluator%20types/UI/How%20to%20define%20an%20LLM-as-a-judge%20evaluator.md).

You can also use an LLM to evaluate the agent's execution path. Unlike the trajectory match evaluators, it doesn't require a reference trajectory, but one can be provided if available.

### Without reference trajectory

```python Python
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import HumanMessage, AIMessage, ToolMessage
from agentevals.trajectory.llm import create_trajectory_llm_as_judge, TRAJECTORY_ACCURACY_PROMPT


@tool
def get_weather(city: str):
    """Get weather information for a city."""
    return f"It's 75 degrees and sunny in {city}."

agent = create_agent("gpt-6.1-sol", tools=[get_weather])

evaluator = create_trajectory_llm_as_judge(  # [!code highlight]
    model="openai:gpt-5.4-mini",  # [!code highlight]
    prompt=TRAJECTORY_ACCURACY_PROMPT,  # [!code highlight]
)  # [!code highlight]

def test_trajectory_quality():
    result = agent.invoke({
        "messages": [HumanMessage(content="What's the weather in Seattle?")]
    })

    evaluation = evaluator(
        outputs=result["messages"],
    )
    # {
    #     'key': 'trajectory_accuracy',
    #     'score': True,
    #     'comment': 'The provided agent trajectory is reasonable...'
    # }
    assert evaluation["score"] is True
```

```ts TypeScript
import { createAgent } from "langchain"
import { tool } from "@langchain/core/tools";
import { HumanMessage, AIMessage, ToolMessage } from "@langchain/core/messages";
import { createTrajectoryLLMAsJudge, TRAJECTORY_ACCURACY_PROMPT } from "agentevals";
import * as z from "zod";

const getWeather = tool(
  async ({ city }: { city: string }) => {
    return `It's 75 degrees and sunny in ${city}.`;
  },
  {
    name: "get_weather",
    description: "Get weather information for a city.",
    schema: z.object({ city: z.string() }),
  }
);

const agent = createAgent({
  model: "gpt-6.1-sol",
  tools: [getWeather]
});

const evaluator = createTrajectoryLLMAsJudge({  // [!code highlight]
  model: "openai:gpt-5.4-mini",  // [!code highlight]
  prompt: TRAJECTORY_ACCURACY_PROMPT,  // [!code highlight]
});  // [!code highlight]

async function testTrajectoryQuality() {
  const result = await agent.invoke({
    messages: [new HumanMessage("What's the weather in Seattle?")]
  });

  const evaluation = await evaluator({
    outputs: result.messages,
  });
  // {
  //     'key': 'trajectory_accuracy',
  //     'score': true,
  //     'comment': 'The provided agent trajectory is reasonable...'
  // }
  expect(evaluation.score).toBe(true);
}
```

### With reference trajectory

If you have a reference trajectory, you can add an extra variable to your prompt and pass in the reference trajectory. Below, we use the prebuilt `TRAJECTORY_ACCURACY_PROMPT_WITH_REFERENCE` prompt and configure the `reference_outputs` variable:

```python Python
evaluator = create_trajectory_llm_as_judge(
    model="openai:gpt-5.4-mini",
    prompt=TRAJECTORY_ACCURACY_PROMPT_WITH_REFERENCE,
)
evaluation = evaluator(
    outputs=result["messages"],
    reference_outputs=reference_trajectory,
)
```

```ts TypeScript
import { TRAJECTORY_ACCURACY_PROMPT_WITH_REFERENCE } from "agentevals";

const evaluator = createTrajectoryLLMAsJudge({
  model: "openai:gpt-5.4-mini",
  prompt: TRAJECTORY_ACCURACY_PROMPT_WITH_REFERENCE,
});

const evaluation = await evaluator({
  outputs: result.messages,
  referenceOutputs: referenceTrajectory,
});
```

> [!NOTE]
>
> For more configurability over how the LLM evaluates the trajectory, visit the [repository](https://github.com/langchain-ai/agentevals?tab=readme-ov-file#trajectory-llm-as-judge).

## Async support (Python)

All `agentevals` evaluators support Python asyncio. For evaluators that use factory functions, async versions are available by adding `async` after `create_` in the function name.

Here's an example using the async judge and evaluator:

```python
from agentevals.trajectory.llm import create_async_trajectory_llm_as_judge, TRAJECTORY_ACCURACY_PROMPT
from agentevals.trajectory.match import create_async_trajectory_match_evaluator

async_judge = create_async_trajectory_llm_as_judge(
    model="openai:gpt-5.4-mini",
    prompt=TRAJECTORY_ACCURACY_PROMPT,
)

async_evaluator = create_async_trajectory_match_evaluator(
    trajectory_match_mode="strict",
)

async def test_async_evaluation():
    result = await agent.ainvoke({
        "messages": [HumanMessage(content="What's the weather?")]
    })

    evaluation = await async_judge(outputs=result["messages"])
    assert evaluation["score"] is True
```

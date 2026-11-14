# Test a ReAct agent with Pytest/Vitest and LangSmith

This tutorial will show you how to use LangSmith's integrations with popular testing tools (Pytest, Vitest, and Jest) to evaluate your LLM application. We will create a ReAct agent that answers questions about publicly traded stocks and write a comprehensive test suite for it.

## Setup

This tutorial uses [LangGraph](https://docs.langchain.com/oss/python/langgraph/quickstart.md) for agent orchestration, [OpenAI's GPT-4o](https://platform.openai.com/docs/models#gpt-4o), [Tavily](https://tavily.com/) for search, [E2B's](https://e2b.dev/) code interpreter, and [Polygon](https://polygon.io/stocks) to retrieve stock data but it can be adapted for other frameworks, models and tools with minor modifications. Tavily, E2B and Polygon are free to sign up for.

### Installation

First, install the packages required for making the agent:

```bash Python
pip install -U langgraph langchain[openai] langchain-community e2b-code-interpreter
```

```bash TypeScript
yarn add @langchain/openai @langchain/community @langchain/langgraph @langchain/core @e2b/code-interpreter @polygon.io/client-js openai zod
```

Next, install the testing framework:

```bash Pytest
# Make sure you have langsmith>=0.3.1
pip install -U "langsmith[pytest]"
```

```bash Vitest
yarn add -D langsmith vitest
```

```bash Jest
yarn add -D langsmith jest
```

### Environment variables

Set the following environment variables:

```bash
export LANGSMITH_TRACING=true
export LANGSMITH_API_KEY=<YOUR_LANGSMITH_API_KEY>
export OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
export TAVILY_API_KEY=<YOUR_TAVILY_API_KEY>
export E2B_API_KEY=<YOUR_E2B_API_KEY>
export POLYGON_API_KEY=<YOUR_POLYGON_API_KEY>
```

## Create your app

To define our React agent, we will use LangGraph/LangGraph.js for the orchestation and LangChain for the LLM and tools.

### Define tools

First we are going to define the tools we are going to use in our agent. There are going to be 3 tools:

* A search tool using Tavily
* A code interpreter tool using E2B
* A stock information tool using Polygon

> [!WARNING]
>
> The `langchain-community` package is no longer maintained. Examples that import from `langchain_community` may be outdated or broken. Use with caution.

> [!WARNING]
>
> The `@langchain/community` package is no longer maintained. Examples that import from `@langchain/community` may be outdated or broken. Use with caution.

```python Python
from langchain_community.tools import TavilySearchResults
from e2b_code_interpreter import Sandbox
from langchain_community.tools.polygon.aggregates import PolygonAggregates
from langchain_community.utilities.polygon import PolygonAPIWrapper
from typing_extensions import Annotated, TypedDict, Optional, Literal

# Define search tool
search_tool = TavilySearchResults(
  max_results=5,
  include_raw_content=True,
)

# Define code tool
def code_tool(code: str) -> str:
  """Execute python code and return the result."""
  sbx = Sandbox()
  execution = sbx.run_code(code)

  if execution.error:
      return f"Error: {execution.error}"
  return f"Results: {execution.results}, Logs: {execution.logs}"

# Define input schema for stock ticker tool
class TickerToolInput(TypedDict):
  """Input format for the ticker tool.
    The tool will pull data in aggregate blocks (timespan_multiplier * timespan) from the from_date to the to_date
  """
  ticker: Annotated[str, ..., "The ticker symbol of the stock"]
  timespan: Annotated[Literal["minute", "hour", "day", "week", "month", "quarter", "year"], ..., "The size of the time window."]
  timespan_multiplier: Annotated[int, ..., "The multiplier for the time window"]
  from_date: Annotated[str, ..., "The date to start pulling data from, YYYY-MM-DD format - ONLY include the year month and day"]
  to_date: Annotated[str, ..., "The date to stop pulling data, YYYY-MM-DD format - ONLY include the year month and day"]

api_wrapper = PolygonAPIWrapper()
polygon_aggregate = PolygonAggregates(api_wrapper=api_wrapper)

# Define stock ticker tool
def ticker_tool(query: TickerToolInput) -> str:
  """Pull data for the ticker."""
  return polygon_aggregate.invoke(query)
```

```typescript TypeScript
import { TavilySearchResults } from "@langchain/community/tools/tavily_search";
import { Sandbox } from "@e2b/code-interpreter";
import { tool } from "@langchain/core/tools";
import { z } from "zod";
import { restClient } from "@polygon.io/client-js";

// Define search tool
const searchTool = new TavilySearchResults({
  maxResults: 5,
});

// Define code tool
const codeTool = tool(async (input) => {
  const sbx = await Sandbox.create();
  const execution = await sbx.runCode(input.code);
  if (execution.error) {
    return `Error: ${execution.error}`;
  }
  return `Results: ${execution.results}, Logs: ${execution.logs}`;
}, {
  name: "code",
  description: "Execute python code and return the result.",
  schema: z.object({
    code: z.string().describe("The python code to execute"),
  }),
});

// Define input schema for stock ticker tool
const TickerToolInputSchema = z.object({
  ticker: z.string().describe("The ticker symbol of the stock"),
  timespan: z.enum(["minute", "hour", "day", "week", "month", "quarter", "year"]).describe("The size of the time window."),
  timespan_multiplier: z.number().describe("The multiplier for the time window"),
  from_date: z
    .string()
    .describe("The date to start pulling data from, YYYY-MM-DD format - ONLY include the year, month, and day"),
  to_date: z
    .string()
    .describe("The date to stop pulling data, YYYY-MM-DD format - ONLY include the year, month, and day"),
});

const rest = restClient(process.env.POLYGON_API_KEY);

// Define stock ticker tool
const tickerTool = tool(async (query) => {
  const parsed = TickerToolInputSchema.parse(query);
  const result = await rest.stocks.aggregates(
      parsed.ticker,
      parsed.timespan_multiplier,
      parsed.timespan,
      parsed.from_date,
      parsed.to_date
  );
  return JSON.stringify(result);
}, {
  name: "ticker",
  description: "Pull data for the ticker",
  schema: TickerToolInputSchema,
});
```

### Define agent

Now that we have defined all of our tools, we can use [`create_agent`](https://reference.langchain.com/python/langchain/agents/factory/create_agent) to create our agent.

```python Python
from typing_extensions import Annotated, TypedDict
from langchain.agents import create_agent


class AgentOutputFormat(TypedDict):
    numeric_answer: Annotated[float | None, ..., "The numeric answer, if the user asked for one"]
    text_answer: Annotated[str | None, ..., "The text answer, if the user asked for one"]
    reasoning: Annotated[str, ..., "The reasoning behind the answer"]

agent = create_agent(
    model="gpt-5.4-mini",
    tools=[code_tool, search_tool, polygon_aggregates],
    response_format=AgentOutputFormat,
    system_prompt="You are a financial expert. Respond to the users query accurately",
)
```

```typescript TypeScript
import { z } from "zod";
import { ChatOpenAI } from "@langchain/openai";
import { createReactAgent } from "@langchain/langgraph/prebuilt";

const AgentOutputFormatSchema = z.object({
  numeric_answer: z.number().optional().describe("The numeric answer, if the user asked for one"),
  text_answer: z.string().optional().describe("The text answer, if the user asked for one"),
  reasoning: z.string().describe("The reasoning behind the answer"),
})

const tools = [codeTool, searchTool, tickerTool];

const agent = createReactAgent({
  llm: new ChatOpenAI({ model: "gpt-6.1-sol" }),
  tools: tools,
  responseFormat: AgentOutputFormatSchema,
  stateModifier: "You are a financial expert. Respond to the users query accurately",
});

export default agent;
```

## Write tests

Now that we have defined our agent, let's write a few tests to ensure basic functionality. In this tutorial we are going to test whether the agent's tool calling abilities are working, whether the agent knows to ignore irrelevant questions, and whether it is able to answer complex questions that involve using all of the tools.

We need to first set up a test file and add the imports needed at the top of the file.

```python Pytest
Create a `tests/test_agent.py` file.

from app import agent, polygon_aggregates, search_tool # import from wherever your agent is defined
import pytest
from langsmith import testing as t
```

```typescript Vitest
Name your test file `agent.vitest.eval.ts`

import { expect } from "vitest";
import * as ls from "langsmith/vitest";
import agent from "../agent"; // import from wherever your agent is defined

// Optional, but recommended to group tests together
ls.describe("Agent Tests", () => {
  // PLACE TESTS Here
});
```

```typescript Jest
Name your test file `agent.jest.eval.ts`

import { expect } from "@jest/globals";
import * as ls from "langsmith/jest";
import agent from "../agent"; // import from wherever your agent is defined

// Optional, but recommended to group tests together
ls.describe("Agent Tests", () => {
  // PLACE TESTS Here
});
```

### Test 1: Handle off-topic questions

The first test will be a simple check that the agent does not use tools on irrelevant queries.

```python Pytest
@pytest.mark.langsmith
@pytest.mark.parametrize(
  # <-- Can still use all normal pytest markers
  "query",
  ["Hello!", "How are you doing?"],
)
def test_no_tools_on_offtopic_query(query: str) -> None:
  """Test that the agent does not use tools on offtopic queries."""
  # Log the test example
  t.log_inputs({"query": query})
  expected = []
  t.log_reference_outputs({"tool_calls": expected})
  # Call the agent's model node directly instead of running the ReACT loop.
  result = agent.nodes["agent"].invoke(
      {"messages": [{"role": "user", "content": query}]}
  )
  actual = result["messages"][0].tool_calls
  t.log_outputs({"tool_calls": actual})
  # Check that no tool calls were made.
  assert actual == expected
```

```typescript Vitest
ls.test.each([
  { inputs: { query: "Hello!" }, expected: { numMessages: 2 } },
  { inputs: { query: "How are you doing?" }, expected: { numMessages: 2 } },
])(
  "should not use tools on offtopic query: %s",
  async ({ inputs: { query }, expected: { numMessages } }) => {
    const result = await agent.invoke({ messages: [{ role: "user", content: query }] });
    ls.logOutputs(result);

    // Check that the flow was HUMAN -> AI FINAL RESPONSE (no tools called)
    expect(result.messages).toHaveLength(numMessages);
  }
);
```

```typescript Jest
ls.test.each([
  { inputs: { query: "Hello!" }, expected: { numMessages: 2 } },
  { inputs: { query: "How are you doing?" }, expected: { numMessages: 2 } },
])(
  "should not use tools on offtopic query: %s",
  async ({ inputs: { query }, expected: { numMessages } }) => {
    const result = await agent.invoke({ messages: [{ role: "user", content: query }] });
    ls.logOutputs(result);

    // Check that the flow was HUMAN -> AI FINAL RESPONSE (no tools called)
    expect(result.messages).toHaveLength(numMessages);
  }
);
```

### Test 2: Simple tool calling

For tool calling, we are going to verify that the agent calls the correct tool with the correct parameters.

```python Pytest
@pytest.mark.langsmith
def test_searches_for_correct_ticker() -> None:
  """Test that the model looks up the correct ticker on simple query."""
  # Log the test example
  query = "What is the price of Apple?"
  t.log_inputs({"query": query})
  expected = "AAPL"
  t.log_reference_outputs({"ticker": expected})
  # Call the agent's model node directly instead of running the full ReACT loop.
  result = agent.nodes["agent"].invoke(
      {"messages": [{"role": "user", "content": query}]}
  )
  tool_calls = result["messages"][0].tool_calls
  if tool_calls[0]["name"] == polygon_aggregates.name:
      actual = tool_calls[0]["args"]["ticker"]
  else:
      actual = None
  t.log_outputs({"ticker": actual})
  # Check that the right ticker was queried
  assert actual == expected
```

```typescript Vitest
ls.test(
  "should search for correct ticker",
  {
    inputs: { query: "What is the price of Apple?" },
    expected: { numMessages: 4 },
  },
  async ({ inputs: { query }, expected: { numMessages } }) => {
    const result = await agent.invoke({
      messages: [{ role: "user", content: query }],
    });

    ls.logOutputs(result);

    // The agent should have made a single tool call to the ticker tool
    const toolCalls = (result.messages[1] as AIMessage).tool_calls || [];
    const tickerQuery = JSON.parse(toolCalls[0].function.arguments).query.ticker;
    // Check that the right ticker was queried
    expect(tickerQuery).toBe("AAPL");

    // Check that the flow was HUMAN -> AI -> TOOL -> AI FINAL RESPONSE
    expect(result.messages).toHaveLength(numMessages);
  }
);
```

```typescript Jest
ls.test(
  "should search for correct ticker",
  {
    inputs: { query: "What is the price of Apple?" },
    expected: { numMessages: 4 },
  },
  async ({ inputs: { query }, expected: { numMessages } }) => {
    const result = await agent.invoke({
      messages: [{ role: "user", content: query }],
    });

    ls.logOutputs(result);

    // The agent should have made a single tool call to the ticker tool
    const toolCalls = (result.messages[1] as AIMessage).tool_calls || [];
    const tickerQuery = JSON.parse(toolCalls[0].function.arguments).query.ticker;
    // Check that the right ticker was queried
    expect(tickerQuery).toBe("AAPL");

    // Check that the flow was HUMAN -> AI -> TOOL -> AI FINAL RESPONSE
    expect(result.messages).toHaveLength(numMessages);
  }
);
```

### Test 3: Complex tool calling

Some tool calls are easier to test than others. With the ticker lookup, we can assert that the correct ticker is searched. With the coding tool, the inputs and outputs of the tool are much less constrained, and there are lots of ways to get to the right answer. In this case, it's simpler to test that the tool is used correctly by running the full agent and asserting that it both calls the coding tool and that it ends up with the right answer.

```python Pytest
@pytest.mark.langsmith
def test_executes_code_when_needed() -> None:
  query = (
      "In the past year Facebook stock went up by 66.76%, "
      "Apple by 25.24%, Google by 37.11%, Amazon by 47.52%, "
      "Netflix by 78.31%. What's the avg return in the past "
      "year of the FAANG stocks, expressed as a percentage?"
  )
  t.log_inputs({"query": query})
  expected = 50.988
  t.log_reference_outputs({"response": expected})
  # Test that the agent executes code when needed
  result = agent.invoke({"messages": [{"role": "user", "content": query}]})
  t.log_outputs({"result": result["structured_response"].get("numeric_answer")})
  # Grab all the tool calls made by the LLM
  tool_calls = [
      tc["name"]
      for msg in result["messages"]
      for tc in getattr(msg, "tool_calls", [])
  ]
  # This will log the number of steps taken by the agent, which is useful for
  # determining how efficiently the agent gets to an answer.
  t.log_feedback(key="num_steps", score=len(result["messages"]) - 1)
  # Assert that the code tool was used
  assert "code_tool" in tool_calls
  # Assert that a numeric answer was provided:
  assert result["structured_response"].get("numeric_answer") is not None
  # Assert that the answer is correct
  assert abs(result["structured_response"]["numeric_answer"] - expected) <= 0.01
```

```typescript Vitest
ls.test(
  "should execute code when needed",
  {
    inputs: { query: "What was the average return rate for FAANG stock in 2024?" },
    expected: { answer: 53 },
  },
  async ({ inputs: { query }, expected: { answer } }) => {
    const result = await agent.invoke({
      messages: [{ role: "user", content: query }],
    });

    ls.logOutputs(result);

    // Grab all the tool calls made by the LLM
    const toolCalls = result.messages
      .filter(m => (m as AIMessage).tool_calls)
      .flatMap(m => (m as AIMessage).tool_calls?.map(tc => tc.name));
    // This will log the number of steps taken by the LLM, which we can track over time to measure performance
    ls.logFeedback({
      key: "num_steps",
      score: result.messages.length - 1, // The first message is the user message
    });
    // Assert that the tool calls include the "code_tool" function
    expect(toolCalls).toContain("code_tool");
    // Assert that the answer is within 1 of the expected answer
    expect(Math.abs(result.structured_response.numeric_answer - answer)).toBeLessThanOrEqual(1);
  }
);
```

```typescript Jest
ls.test(
  "should execute code when needed",
  {
    inputs: { query: "What was the average return rate for FAANG stock in 2024?" },
    expected: { answer: 53 },
  },
  async ({ inputs: { query }, expected: { answer } }) => {
    const result = await agent.invoke({
      messages: [{ role: "user", content: query }],
    });

    ls.logOutputs(result);
    // Grab all the tool calls made by the LLM
    const toolCalls = result.messages
      .filter(m => (m as AIMessage).tool_calls)
      .flatMap(m => (m as AIMessage).tool_calls?.map(tc => tc.name));
    // This will log the number of steps taken by the LLM, which we can track over time to measure performance
    ls.logFeedback({
      key: "num_steps",
      score: result.messages.length - 1, // The first message is the user message
    });
    // Assert that the tool calls include the "code_tool" function
    expect(toolCalls).toContain("code_tool");
    // Assert that the answer is within 1 of the expected answer
    expect(Math.abs(result.structured_response.numeric_answer - answer)).toBeLessThanOrEqual(1);
  }
);
```

### Test 4: LLM-as-a-judge

We are going to ensure that the agent's answer is grounded in the search results by running an LLM-as-a-judge evaluation. In order to trace the LLM-as-a-Judge call separately from our agent, we will use the LangSmith provided `trace_feedback` context manager in Python and `wrapEvaluator` function in JS/TS.

```python Pytest
from typing_extensions import Annotated, TypedDict
from langchain.chat_models import init_chat_model

class Grade(TypedDict):
  """Evaluate the groundedness of an answer in source documents."""
  score: Annotated[
      bool,
      ...,
      "Return True if the answer is fully grounded in the source documents, otherwise False.",
  ]

judge_llm = init_chat_model("gpt-6.1-sol").with_structured_output(Grade)

@pytest.mark.langsmith
def test_grounded_in_source_info() -> None:
  """Test that response is grounded in the tool outputs."""
  query = "How did Nvidia stock do in 2024 according to analysts?"
  t.log_inputs({"query": query})
  result = agent.invoke({"messages": [{"role": "user", "content": query}]})
  # Grab all the search calls made by the LLM
  search_results = "\n\n".join(
      msg.content
      for msg in result["messages"]
      if msg.type == "tool" and msg.name == search_tool.name
  )
  t.log_outputs(
      {
          "response": result["structured_response"].get("text_answer"),
          "search_results": search_results,
      }
  )
  # Trace the feedback LLM run separately from the deployment run.
  with t.trace_feedback():
      # Instructions for the LLM judge
      instructions = (
          "Grade the following ANSWER. "
          "The ANSWER should be fully grounded in (i.e. supported by) the source DOCUMENTS. "
          "Return True if the ANSWER is fully grounded in the DOCUMENTS. "
          "Return False if the ANSWER is not grounded in the DOCUMENTS."
      )
      answer_and_docs = (
          f"ANSWER: {result['structured_response'].get('text_answer', '')}\n"
          f"DOCUMENTS:\n{search_results}"
      )
      # Run the judge LLM
      grade = judge_llm.invoke(
          [
              {"role": "system", "content": instructions},
              {"role": "user", "content": answer_and_docs},
          ]
      )
      t.log_feedback(key="groundedness", score=grade["score"])
  assert grade['score']
```

```typescript Vitest
// THIS CODE GOES OUTSIDE THE TEST - IT IS JUST A HELPER FUNCTION
const judgeLLM = new ChatOpenAI({ model: "gpt-6.1-sol" });
const groundedEvaluator = async (params: {
  answer: string;
  referenceDocuments: string,
}) => {
  // Instructions for the LLM judge
  const instructions = [
    "Return 1 if the ANSWER is grounded in the DOCUMENTS",
    "Return 0 if the ANSWER is not grounded in the DOCUMENTS",
  ].join("\n");

  // Run the judge LLM
  const grade = await judgeLLM.invoke([
    { role: "system", content: instructions },
    { role: "user", content: `ANSWER: ${params.answer}\nDOCUMENTS: ${params.referenceDocuments}` },
  ]);
  const score = parseInt(grade.content.toString());
  return { key: "groundedness", score };
};

// THIS CODE GOES INSIDE THE TEST
ls.test(
  "grounded in the source",
  {
    inputs: { query: "How did Nvidia stock do in 2024 according to analysts?" },
  },
  async ({ inputs: { query } }) => {
    const result = await agent.invoke({
      messages: [{ role: "user", content: query }],
    });
    const wrappedEvaluator = ls.wrapEvaluator(groundedEvaluator);
    await wrappedEvaluator({
      answer: result.structuredResponse.text_answer ?? "",
      referenceDocuments: result.structuredResponse.reasoning,
    })
    ls.logOutputs(result);
  }
);
```

```typescript Jest
// THIS CODE GOES OUTSIDE THE TEST - IT IS JUST A HELPER FUNCTION
const judgeLLM = new ChatOpenAI({ model: "gpt-6.1-sol" });
const groundedEvaluator = async (params: {
  answer: string;
  referenceDocuments: string,
}) => {
  // Instructions for the LLM judge
  const instructions = [
    "Return 1 if the ANSWER is grounded in the DOCUMENTS",
    "Return 0 if the ANSWER is not grounded in the DOCUMENTS",
  ].join("\n");

  // Run the judge LLM
  const grade = await judgeLLM.invoke([
    { role: "system", content: instructions },
    { role: "user", content: `ANSWER: ${params.answer}\nDOCUMENTS: ${params.referenceDocuments}` },
  ]);
  const score = parseInt(grade.content.toString());
  return { key: "groundedness", score };
};

// THIS CODE GOES INSIDE THE TEST
ls.test(
  "grounded in the source",
  {
    inputs: { query: "How did Nvidia stock do in 2024 according to analysts?" },
  },
  async ({ inputs: { query } }) => {
    const result = await agent.invoke({
      messages: [{ role: "user", content: query }],
    });
    const wrappedEvaluator = ls.wrapEvaluator(groundedEvaluator);
    await wrappedEvaluator({
      answer: result.structuredResponse.text_answer ?? "",
      referenceDocuments: result.structuredResponse.reasoning,
    })
    ls.logOutputs(result);
  }
);
```

## Run tests

Once you have setup your config files (if you are using Vitest or Jest), you can run your tests using the following commands:

> [accordion] Config files for Vitest/Jest
>
> ```typescript Vitest theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> Create a `ls.vitest.config.ts` file:
>
> import { defineConfig } from "vitest/config";
>
> export default defineConfig({
>   test: {
>     include: ["**/*.eval.?(c|m)[jt]s"],
>     reporters: ["langsmith/vitest/reporter"],
>     setupFiles: ["dotenv/config"],
>     testTimeout: 30000,
>   },
> });
> ```
>
> ```javascript Jest theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> Create a `ls.jest.config.ts` file:
>
> require('dotenv').config();
>
> module.exports = {
>   preset: 'ts-jest',
>   testEnvironment: 'node',
>   testMatch: [
>     '<rootDir>/tests/jest/**/*.jest.eval.ts'
>   ],
>   testPathIgnorePatterns: [
>     '<rootDir>/tests/vitest/.*.vitest.eval.ts$'
>   ],
>   reporters: ["langsmith/jest/reporter"],
>   testTimeout: 30000,
> };
> ```

```bash Pytest
pytest --langsmith-output tests
```

```bash Vitest
yarn vitest --config ls.vitest.config.ts
```

```bash Jest
yarn jest --config ls.jest.config.ts
```

## Reference code

Remember to also add the config files for Vitest and Jest to your project.

### Agent

> [accordion] Agent code
>
> > [!WARNING]
> >
> > The `langchain-community` package is no longer maintained. Examples that import from `langchain_community` may be outdated or broken. Use with caution.
>
> > [!WARNING]
> >
> > The `@langchain/community` package is no longer maintained. Examples that import from `@langchain/community` may be outdated or broken. Use with caution.
>
> ```python Python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from e2b_code_interpreter import Sandbox
> from langchain_community.tools import PolygonAggregates, TavilySearchResults
> from langchain_community.utilities.polygon import PolygonAPIWrapper
> from langchain.agents import create_agent
> from typing_extensions import Annotated, TypedDict
>
>
> search_tool = TavilySearchResults(
>     max_results=5,
>     include_raw_content=True,
> )
>
> def code_tool(code: str) -> str:
>     """Execute python code and return the result."""
>     sbx = Sandbox()
>     execution = sbx.run_code(code)
>
>     if execution.error:
>         return f"Error: {execution.error}"
>     return f"Results: {execution.results}, Logs: {execution.logs}"
>
> polygon_aggregates = PolygonAggregates(api_wrapper=PolygonAPIWrapper())
>
> class AgentOutputFormat(TypedDict):
>     numeric_answer: Annotated[
>         float | None, ..., "The numeric answer, if the user asked for one"
>     ]
>     text_answer: Annotated[
>         str | None, ..., "The text answer, if the user asked for one"
>     ]
>     reasoning: Annotated[str, ..., "The reasoning behind the answer"]
>
> agent = create_agent(
>     model="gpt-5.4-mini",
>     tools=[code_tool, search_tool, polygon_aggregates],
>     response_format=AgentOutputFormat,
>     system_prompt="You are a financial expert. Respond to the users query accurately",
> )
> ```
>
> ```typescript TypeScript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { ChatOpenAI } from "@langchain/openai";
> import { createReactAgent } from "@langchain/langgraph/prebuilt";
> import { TavilySearchResults } from "@langchain/community/tools/tavily_search";
> import { Sandbox } from '@e2b/code-interpreter'
> import { restClient } from '@polygon.io/client-js';
> import { tool } from "@langchain/core/tools";
> import { z } from "zod";
>
> const codeTool = tool(async (input) => {
>     const sbx = await Sandbox.create();
>     const execution = await sbx.runCode(input.code);
>     if (execution.error) {
>     return `Error: ${execution.error}`;
>     }
>     return `Results: ${execution.results}, Logs: ${execution.logs}`;
> }, {
>     name: "code",
>     description: "Execute python code and return the result.",
>     schema: z.object({
>     code: z.string().describe("The python code to execute"),
>     }),
> });
>
> const TickerToolInputSchema = z.object({
>     ticker: z.string().describe("The ticker symbol of the stock"),
>     timespan: z.enum(["minute", "hour", "day", "week", "month", "quarter", "year"]).describe("The size of the time window."),
>     timespan_multiplier: z.number().describe("The multiplier for the time window"),
>     from_date: z
>     .string()
>     .describe("The date to start pulling data from, YYYY-MM-DD format - ONLY include the year, month, and day"),
>     to_date: z
>     .string()
>     .describe("The date to stop pulling data, YYYY-MM-DD format - ONLY include the year, month, and day"),
> });
>
> const rest = restClient(process.env.POLYGON_API_KEY);
>
> const tickerTool = tool(async (query) => {
>     const parsed = TickerToolInputSchema.parse(query);
>     const result = await rest.stocks.aggregates(
>     parsed.ticker,
>     parsed.timespan_multiplier,
>     parsed.timespan,
>     parsed.from_date,
>     parsed.to_date
>     );
>     return JSON.stringify(result);
> }, {
>     name: "ticker",
>     description: "Pull data for the ticker",
>     schema: TickerToolInputSchema,
> });
>
> const searchTool = new TavilySearchResults({
>     maxResults: 5,
> });
>
> const AgentOutputFormatSchema = z.object({
>     numeric_answer: z.number().optional().describe("The numeric answer, if the user asked for one"),
>     text_answer: z.string().optional().describe("The text answer, if the user asked for one"),
>     reasoning: z.string().describe("The reasoning behind the answer"),
> })
>
> const tools = [codeTool, searchTool, tickerTool];
>
> const agent = createReactAgent({
>     llm: new ChatOpenAI({ model: "gpt-6.1-sol" }),
>     tools: tools,
>     responseFormat: AgentOutputFormatSchema,
>     stateModifier: "You are a financial expert. Respond to the users query accurately",
> });
>
> export default agent;
> ```

### Tests

> [accordion] Test code
>
> ```python Pytest theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> # from app import agent, polygon_aggregates, search_tool # import from wherever your agent is defined
> import pytest
> from langchain.chat_models import init_chat_model
> from langsmith import testing as t
> from typing_extensions import Annotated, TypedDict
>
> @pytest.mark.langsmith
> @pytest.mark.parametrize(
>   # <-- Can still use all normal pytest markers
>   "query",
>   ["Hello!", "How are you doing?"],
> )
> def test_no_tools_on_offtopic_query(query: str) -> None:
>   """Test that the agent does not use tools on offtopic queries."""
>   # Log the test example
>   t.log_inputs({"query": query})
>   expected = []
>   t.log_reference_outputs({"tool_calls": expected})
>   # Call the agent's model node directly instead of running the ReACT loop.
>   result = agent.nodes["agent"].invoke(
>       {"messages": [{"role": "user", "content": query}]}
>   )
>   actual = result["messages"][0].tool_calls
>   t.log_outputs({"tool_calls": actual})
>   # Check that no tool calls were made.
>   assert actual == expected
>
> @pytest.mark.langsmith
> def test_searches_for_correct_ticker() -> None:
>   """Test that the model looks up the correct ticker on simple query."""
>   # Log the test example
>   query = "What is the price of Apple?"
>   t.log_inputs({"query": query})
>   expected = "AAPL"
>   t.log_reference_outputs({"ticker": expected})
>   # Call the agent's model node directly instead of running the full ReACT loop.
>   result = agent.nodes["agent"].invoke(
>       {"messages": [{"role": "user", "content": query}]}
>   )
>   tool_calls = result["messages"][0].tool_calls
>   if tool_calls[0]["name"] == polygon_aggregates.name:
>       actual = tool_calls[0]["args"]["ticker"]
>   else:
>       actual = None
>   t.log_outputs({"ticker": actual})
>   # Check that the right ticker was queried
>   assert actual == expected
>
> @pytest.mark.langsmith
> def test_executes_code_when_needed() -> None:
>   query = (
>       "In the past year Facebook stock went up by 66.76%, "
>       "Apple by 25.24%, Google by 37.11%, Amazon by 47.52%, "
>       "Netflix by 78.31%. What's the avg return in the past "
>       "year of the FAANG stocks, expressed as a percentage?"
>   )
>   t.log_inputs({"query": query})
>   expected = 50.988
>   t.log_reference_outputs({"response": expected})
>   # Test that the agent executes code when needed
>   result = agent.invoke({"messages": [{"role": "user", "content": query}]})
>   t.log_outputs({"result": result["structured_response"].get("numeric_answer")})
>   # Grab all the tool calls made by the LLM
>   tool_calls = [
>       tc["name"]
>       for msg in result["messages"]
>       for tc in getattr(msg, "tool_calls", [])
>   ]
>   # This will log the number of steps taken by the agent, which is useful for
>   # determining how efficiently the agent gets to an answer.
>   t.log_feedback(key="num_steps", score=len(result["messages"]) - 1)
>   # Assert that the code tool was used
>   assert "code_tool" in tool_calls
>   # Assert that a numeric answer was provided:
>   assert result["structured_response"].get("numeric_answer") is not None
>   # Assert that the answer is correct
>   assert abs(result["structured_response"]["numeric_answer"] - expected) <= 0.01
>
> class Grade(TypedDict):
>   """Evaluate the groundedness of an answer in source documents."""
>   score: Annotated[
>       bool,
>       ...,
>       "Return True if the answer is fully grounded in the source documents, otherwise False.",
>   ]
>
> judge_llm = init_chat_model("gpt-6.1-sol").with_structured_output(Grade)
>
> @pytest.mark.langsmith
> def test_grounded_in_source_info() -> None:
>   """Test that response is grounded in the tool outputs."""
>   query = "How did Nvidia stock do in 2024 according to analysts?"
>   t.log_inputs({"query": query})
>   result = agent.invoke({"messages": [{"role": "user", "content": query}]})
>   # Grab all the search calls made by the LLM
>   search_results = "\n\n".join(
>       msg.content
>       for msg in result["messages"]
>       if msg.type == "tool" and msg.name == search_tool.name
>   )
>   t.log_outputs(
>       {
>           "response": result["structured_response"].get("text_answer"),
>           "search_results": search_results,
>       }
>   )
>   # Trace the feedback LLM run separately from the deployment run.
>   with t.trace_feedback():
>       # Instructions for the LLM judge
>       instructions = (
>           "Grade the following ANSWER. "
>           "The ANSWER should be fully grounded in (i.e. supported by) the source DOCUMENTS. "
>           "Return True if the ANSWER is fully grounded in the DOCUMENTS. "
>           "Return False if the ANSWER is not grounded in the DOCUMENTS."
>       )
>       answer_and_docs = (
>           f"ANSWER: {result['structured_response'].get('text_answer', '')}\n"
>           f"DOCUMENTS:\n{search_results}"
>       )
>       # Run the judge LLM
>       grade = judge_llm.invoke(
>           [
>               {"role": "system", "content": instructions},
>               {"role": "user", "content": answer_and_docs},
>           ]
>       )
>       t.log_feedback(key="groundedness", score=grade["score"])
>   assert grade["score"]
> ```
>
> ```typescript Vitest theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { expect } from "vitest";
> import * as ls from "langsmith/vitest";
> import agent from "../agent";
> import { AIMessage, ToolMessage } from "@langchain/core/messages";
> import { ChatOpenAI } from "@langchain/openai";
>
> const judgeLLM = new ChatOpenAI({ model: "gpt-6.1-sol" });
>
> const groundedEvaluator = async (params: {
>   answer: string;
>   referenceDocuments: string,
> }) => {
>   const instructions = [
>     "Return 1 if the ANSWER is grounded in the DOCUMENTS",
>     "Return 0 if the ANSWER is not grounded in the DOCUMENTS",
>   ].join("\n");
>
>   const grade = await judgeLLM.invoke([
>     { role: "system", content: instructions },
>     { role: "user", content: `ANSWER: ${params.answer}\nDOCUMENTS: ${params.referenceDocuments}` },
>   ]);
>   const score = parseInt(grade.content.toString());
>   return { key: "groundedness", score };
> };
>
> ls.describe("Agent Tests", () => {
>   ls.test.each([
>     { inputs: { query: "Hello!" }, referenceOutputs: { numMessages: 2 } },
>     { inputs: { query: "How are you doing?" }, referenceOutputs: { numMessages: 2 } },
>   ])(
>     "should not use tools on offtopic query: %s",
>     async ({ inputs: { query }, referenceOutputs: { numMessages } }) => {
>       const result = await agent.invoke({
>         messages: [{ role: "user", content: query }],
>       });
>       ls.logOutputs(result);
>       expect(result.messages).toHaveLength(numMessages);
>     }
>   );
>
>   ls.test(
>     "should search for correct ticker",
>     {
>       inputs: { query: "What is the price of Apple?" },
>       referenceOutputs: { numMessages: 4 },
>     },
>     async ({ inputs: { query }, referenceOutputs: { numMessages } }) => {
>       const result = await agent.invoke({
>         messages: [{ role: "user", content: query }],
>       });
>       const toolCalls = (result.messages[1] as AIMessage).tool_calls || [];
>       const tickerQuery = toolCalls[0].args.ticker;
>       ls.logOutputs(result);
>       expect(tickerQuery).toBe("AAPL");
>       expect(result.messages).toHaveLength(numMessages);
>     }
>   );
>
>   ls.test(
>     "should execute code when needed",
>     {
>       inputs: { query: "What was the average return rate for FAANG stock in 2024?" },
>       referenceOutputs: { answer: 53 },
>     },
>     async ({ inputs: { query }, referenceOutputs: { answer } }) => {
>       const result = await agent.invoke({
>         messages: [{ role: "user", content: query }],
>       });
>
>       const toolCalls = result.messages
>         .filter(m => (m as AIMessage).tool_calls)
>         .flatMap(m => (m as AIMessage).tool_calls?.map(tc => tc.name));
>       ls.logFeedback({
>         key: "num_steps",
>         score: result.messages.length - 1,
>       });
>       ls.logOutputs(result);
>       expect(toolCalls).toContain("code_tool");
>       expect(Math.abs((result.structuredResponse.numeric_answer ?? 0) - answer)).toBeLessThanOrEqual(1);
>     }
>   );
>
>   ls.test(
>     "grounded in the source",
>     {
>       inputs: { query: "How did Nvidia stock do in 2024?" },
>       referenceOutputs: {},
>     },
>     async ({ inputs: { query }, referenceOutputs: {} }) => {
>       const result = await agent.invoke({
>         messages: [{ role: "user", content: query }],
>       });
>       const referenceDocuments = result.messages
>         .filter((m): m is ToolMessage => m.name?.includes('tavily_search_results_json') ?? false)
>         .map(m => m.content)
>         .join('\n');
>       const wrappedEvaluator = ls.wrapEvaluator(groundedEvaluator);
>       await wrappedEvaluator({
>         answer: result.structuredResponse.text_answer ?? "",
>         referenceDocuments: referenceDocuments,
>       })
>       ls.logOutputs(result);
>     }
>   );
> });
> ```
>
> ```typescript Jest theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { expect } from "@jest/globals";
> import * as ls from "langsmith/jest";
> import agent from "../agent";
> import { AIMessage } from "@langchain/core/messages";
> import { ChatOpenAI } from "@langchain/openai";
>
> const judgeLLM = new ChatOpenAI({ model: "gpt-6.1-sol" });
>
> const groundedEvaluator = async (params: {
>   answer: string;
>   referenceDocuments: string,
> }) => {
>   const instructions = [
>     "Return 1 if the ANSWER is grounded in the DOCUMENTS",
>     "Return 0 if the ANSWER is not grounded in the DOCUMENTS",
>   ].join("\n");
>
>   const grade = await judgeLLM.invoke([
>     { role: "system", content: instructions },
>     { role: "user", content: `ANSWER: ${params.answer}\nDOCUMENTS: ${params.referenceDocuments}` },
>   ]);
>   const score = parseInt(grade.content.toString());
>   return { key: "groundedness", score };
> };
>
> ls.describe("Agent Tests", () => {
>   ls.test.each([
>     { inputs: { query: "Hello!" }, referenceOutputs: { numMessages: 2 } },
>     { inputs: { query: "How are you doing?" }, referenceOutputs: { numMessages: 2 } },
>   ])(
>     "should not use tools on offtopic query: %s",
>     async ({ inputs: { query }, referenceOutputs: { numMessages } }) => {
>       const result = await agent.invoke({
>         messages: [{ role: "user", content: query }],
>       });
>       ls.logOutputs(result);
>       expect(result.messages).toHaveLength(numMessages);
>     }
>   );
>
>   ls.test(
>     "should search for correct ticker",
>     {
>       inputs: { query: "What is the price of Apple?" },
>       referenceOutputs: { numMessages: 4 },
>     },
>     async ({ inputs: { query }, referenceOutputs: { numMessages } }) => {
>       const result = await agent.invoke({
>         messages: [{ role: "user", content: query }],
>       });
>       const toolCalls = (result.messages[1] as AIMessage).tool_calls || [];
>       const tickerQuery = toolCalls[0].args.ticker;
>       ls.logOutputs(result);
>       expect(tickerQuery).toBe("AAPL");
>       expect(result.messages).toHaveLength(numMessages);
>     }
>   );
>
>   ls.test(
>     "should execute code when needed",
>     {
>       inputs: { query: "What was the average return rate for FAANG stock in 2024?" },
>       referenceOutputs: { answer: 53 },
>     },
>     async ({ inputs: { query }, referenceOutputs: { answer } }) => {
>       const result = await agent.invoke({
>         messages: [{ role: "user", content: query }],
>       });
>       const toolCalls = result.messages
>         .filter(m => (m as AIMessage).tool_calls)
>         .flatMap(m => (m as AIMessage).tool_calls?.map(tc => tc.name));
>       ls.logFeedback({
>         key: "num_steps",
>         score: result.messages.length - 1,
>       });
>       ls.logOutputs(result);
>       expect(toolCalls).toContain("code_tool");
>       expect(Math.abs((result.structuredResponse.numeric_answer ?? 0) - answer)).toBeLessThanOrEqual(1);
>     }
>   );
>
>   ls.test(
>     "grounded in the source",
>     {
>       inputs: { query: "How did Nvidia stock do in 2024 according to analysts?" },
>       referenceOutputs: {},
>     },
>     async ({ inputs: { query }, referenceOutputs: {} }) => {
>       const result = await agent.invoke({
>         messages: [{ role: "user", content: query }],
>       });
>       const wrappedEvaluator = ls.wrapEvaluator(groundedEvaluator);
>       await wrappedEvaluator({
>         answer: result.structuredResponse.text_answer ?? "",
>         referenceDocuments: result.structuredResponse.reasoning,
>       })
>       ls.logOutputs(result);
>     }
>   );
> });
> ```

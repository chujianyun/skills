# Trace LangGraph agents

LangSmith smoothly integrates with LangGraph (Python and JS) to help you trace agents, whether you're using LangChain modules or other SDKs.

> [!NOTE]
>
> In an [agent-based workspace](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20Registry.md), [create an agent](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md) once before sending traces. Use [agent addressing](../../../Configuration%20%26%20troubleshooting/Agent%20%26%20environment%20settings/Log%20traces%20to%20an%20agent.md) to select its identifier and environment. If an integration requires `project_name`, use the selected environment's [`tracer_session_name`](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md#use-an-environment-project) as a compatibility value.

## With LangChain

If you are using LangChain modules within LangGraph, you only need to set a few environment variables to enable tracing.

This guide will walk through a basic example. For more detailed information on configuration, see the [Trace With LangChain](Trace%20LangChain%20agents%20%28Python%20and%20JS-TS%29.md) guide.

### 1. Installation

Install the LangGraph library and the OpenAI integration for Python and JS (we use the OpenAI integration for the code snippets below).

For a full list of packages available, see the [LangChain Python docs](https://docs.langchain.com/oss/python/integrations/providers/overview.md) and [LangChain JS docs](https://docs.langchain.com/oss/javascript/integrations/providers/overview.md).

```bash pip
pip install langchain_openai langgraph
```

```bash yarn
yarn add @langchain/openai @langchain/langgraph
```

```bash npm
npm install @langchain/openai @langchain/langgraph
```

```bash pnpm
pnpm add @langchain/openai @langchain/langgraph
```

### 2. Configure your environment

```bash wrap
export LANGSMITH_TRACING=true
export LANGSMITH_API_KEY=<your-api-key>
export LANGSMITH_AGENT_ID="<your-agent-id>"
export LANGSMITH_AGENT_ENVIRONMENT="local"
# This example uses OpenAI, but you can use any LLM provider of choice
export OPENAI_API_KEY=<your-openai-api-key>
# For LangSmith API keys linked to multiple workspaces, set the LANGSMITH_WORKSPACE_ID environment variable to specify which workspace to use.
export LANGSMITH_WORKSPACE_ID=<your-workspace-id>
```

> [!NOTE]
>
> If your account is in a region other than US (the default), also set `LANGSMITH_ENDPOINT` to the API URL for your region. Without this, your API key won't be recognized and requests will fail to authenticate.
>
> <table>
>   <thead>
>     <tr>
>       <th>Region</th>
>
>       <th>
>         URL
>       </th>
>     </tr>
>   </thead>
>
>   <tbody>
>     <tr>
>       <td>GCP US</td>
>
>       <td>
>         `https://api.smith.langchain.com`
>       </td>
>     </tr>
>
>     <tr>
>       <td>GCP EU</td>
>
>       <td>
>         `https://eu.api.smith.langchain.com`
>       </td>
>     </tr>
>
>     <tr>
>       <td>GCP APAC</td>
>
>       <td>
>         `https://apac.api.smith.langchain.com`
>       </td>
>     </tr>
>
>     <tr>
>       <td>AWS US</td>
>
>       <td>
>         `https://aws.api.smith.langchain.com`
>       </td>
>     </tr>
>
>     <tr><td>Azure US</td>
>     <td>`https://azure.api.smith.langchain.com`</td></tr>
>   </tbody>
> </table>
>
> For example, EU accounts: `export LANGSMITH_ENDPOINT="https://eu.api.smith.langchain.com"`.

> [!NOTE]
>
> If you are using LangChain.js with LangSmith and are not in a serverless environment, we also recommend setting the following explicitly to reduce latency:
>
> `export LANGCHAIN_CALLBACKS_BACKGROUND=true`
>
> If you are in a serverless environment, we recommend setting the reverse to allow tracing to finish before your function ends:
>
> `export LANGCHAIN_CALLBACKS_BACKGROUND=false`
>
> See [this LangChain.js guide](Trace%20LangChain%20agents%20%28Python%20and%20JS-TS%29.md#ensure-all-traces-are-submitted-before-exiting) for more information.

### 3. Log a trace

Once you've set up your environment, you can call LangChain runnables as normal. LangSmith will infer the proper tracing config:

```python Python
from typing import Literal
from langchain.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, MessagesState

@tool
def search(query: str):
    """Call to surf the web."""
    if "sf" in query.lower() or "san francisco" in query.lower():
        return "It's 60 degrees and foggy."
    return "It's 90 degrees and sunny."

tools = [search]
tool_node = ToolNode(tools)

model = ChatOpenAI(model="gpt-6-luna").bind_tools(tools)

def should_continue(state: MessagesState) -> Literal["tools", "__end__"]:
    messages = state['messages']
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return "__end__"

def call_model(state: MessagesState):
    messages = state['messages']
    # Invoking `model` will automatically infer the correct tracing context
    response = model.invoke(messages)
    return {"messages": [response]}

workflow = StateGraph(MessagesState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)
workflow.add_edge("__start__", "agent")
workflow.add_conditional_edges(
    "agent",
    should_continue,
)
workflow.add_edge("tools", 'agent')

app = workflow.compile()

final_state = app.invoke(
    {"messages": [HumanMessage(content="what is the weather in sf")]},
    config={"configurable": {"thread_id": 42}}
)

final_state["messages"][-1].content
```

```typescript TypeScript
import { HumanMessage, AIMessage } from "@langchain/core/messages";
import { tool } from "@langchain/core/tools";
import { z } from "zod";
import { ChatOpenAI } from "@langchain/openai";
import { StateGraph, StateGraphArgs } from "@langchain/langgraph";
import { ToolNode } from "@langchain/langgraph/prebuilt";

interface AgentState {
  messages: HumanMessage[];
}

const graphState: StateGraphArgs<AgentState>["channels"] = {
  messages: {
    reducer: (x: HumanMessage[], y: HumanMessage[]) => x.concat(y),
  },
};

const searchTool = tool(async ({ query }: { query: string }) => {
  if (query.toLowerCase().includes("sf") || query.toLowerCase().includes("san francisco")) {
    return "It's 60 degrees and foggy."
  }
  return "It's 90 degrees and sunny."
}, {
  name: "search",
  description:
    "Call to surf the web.",
  schema: z.object({
    query: z.string().describe("The query to use in your search."),
  }),
});

const tools = [searchTool];
const toolNode = new ToolNode<AgentState>(tools);

const model = new ChatOpenAI({
  model: "gpt-6-luna",
}).bindTools(tools);

function shouldContinue(state: AgentState) {
  const messages = state.messages;
  const lastMessage = messages[messages.length - 1] as AIMessage;
  if (lastMessage.tool_calls?.length) {
    return "tools";
  }
  return "__end__";
}

async function callModel(state: AgentState) {
  const messages = state.messages;
  // Invoking `model` will automatically infer the correct tracing context
  const response = await model.invoke(messages);
  return { messages: [response] };
}

const workflow = new StateGraph<AgentState>({ channels: graphState })
  .addNode("agent", callModel)
  .addNode("tools", toolNode)
  .addEdge("__start__", "agent")
  .addConditionalEdges("agent", shouldContinue)
  .addEdge("tools", "agent");

const app = workflow.compile();

const finalState = await app.invoke(
  { messages: [new HumanMessage("what is the weather in sf")] },
  { configurable: { thread_id: "42" } }
);

finalState.messages[finalState.messages.length - 1].content;
```

### Viewing the trace

**Details view**

Click on the trace, and toggle to the **Details** view on the top right. Your trace in LangSmith should [look like this](https://smith.langchain.com/public/79061a0f-c602-4012-b022-03fd46bce89e/r).

**Trajectory view**

The **Trajectory** view in the LangSmith UI shows a simplified conversation history between the user and the agent. This view pulls messages from the top-level trace (including the user’s initial request, tool calls, and the agent’s final response) and represents them in a chat-like format.

## Without LangChain

If you are using other SDKs or custom functions within LangGraph, you will need to [wrap or decorate them appropriately](../../Manual%20instrumentation/Custom%20instrumentation.md#use-%40traceable-%2F-traceable) (with the `@traceable` decorator in Python or the `traceable` function in JS, or something like e.g. `wrap_openai` for SDKs). If you do so, LangSmith will automatically nest traces from those wrapped methods.

Here's an example. You can also see this page for more information.

### 1. Installation

Install the LangGraph library and the OpenAI SDK for Python and JS (we use the OpenAI integration for the code snippets below).

```bash pip
pip install openai langsmith langgraph
```

```bash yarn
yarn add openai langsmith @langchain/langgraph
```

```bash npm
npm install openai langsmith @langchain/langgraph
```

```bash pnpm
pnpm add openai langsmith @langchain/langgraph
```

### 2. Configure your environment

```bash wrap
export LANGSMITH_TRACING=true
export LANGSMITH_API_KEY=<your-api-key>
export LANGSMITH_AGENT_ID="<your-agent-id>"
export LANGSMITH_AGENT_ENVIRONMENT="local"
# This example uses OpenAI, but you can use any LLM provider of choice
export OPENAI_API_KEY=<your-openai-api-key>
```

> [!NOTE]
>
> If your account is in a region other than US (the default), also set `LANGSMITH_ENDPOINT` to the API URL for your region. Without this, your API key won't be recognized and requests will fail to authenticate.
>
> <table>
>   <thead>
>     <tr>
>       <th>Region</th>
>
>       <th>
>         URL
>       </th>
>     </tr>
>   </thead>
>
>   <tbody>
>     <tr>
>       <td>GCP US</td>
>
>       <td>
>         `https://api.smith.langchain.com`
>       </td>
>     </tr>
>
>     <tr>
>       <td>GCP EU</td>
>
>       <td>
>         `https://eu.api.smith.langchain.com`
>       </td>
>     </tr>
>
>     <tr>
>       <td>GCP APAC</td>
>
>       <td>
>         `https://apac.api.smith.langchain.com`
>       </td>
>     </tr>
>
>     <tr>
>       <td>AWS US</td>
>
>       <td>
>         `https://aws.api.smith.langchain.com`
>       </td>
>     </tr>
>
>     <tr><td>Azure US</td>
>     <td>`https://azure.api.smith.langchain.com`</td></tr>
>   </tbody>
> </table>
>
> For example, EU accounts: `export LANGSMITH_ENDPOINT="https://eu.api.smith.langchain.com"`.

> [!NOTE]
>
> If you are using LangChain.js with LangSmith and are not in a serverless environment, we also recommend setting the following explicitly to reduce latency:
>
> `export LANGCHAIN_CALLBACKS_BACKGROUND=true`
>
> If you are in a serverless environment, we recommend setting the reverse to allow tracing to finish before your function ends:
>
> `export LANGCHAIN_CALLBACKS_BACKGROUND=false`
>
> See [this LangChain.js guide](Trace%20LangChain%20agents%20%28Python%20and%20JS-TS%29.md#ensure-all-traces-are-submitted-before-exiting) for more information.

### 3. Log a trace

Once you've set up your environment, [wrap or decorate the custom functions/SDKs](../../Manual%20instrumentation/Custom%20instrumentation.md#use-%40traceable-%2F-traceable) you want to trace. LangSmith will then infer the proper tracing config:

```python Python
import json
import openai
import operator
from langsmith import traceable
from langsmith.wrappers import wrap_openai
from typing import Annotated, Literal, TypedDict
from langgraph.graph import StateGraph

class State(TypedDict):
    messages: Annotated[list, operator.add]

tool_schema = {
    "type": "function",
    "function": {
        "name": "search",
        "description": "Call to surf the web.",
        "parameters": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
        },
    },
}

# Decorating the tool function will automatically trace it with the correct context
@traceable(run_type="tool", name="Search Tool")
def search(query: str):
    """Call to surf the web."""
    if "sf" in query.lower() or "san francisco" in query.lower():
        return "It's 60 degrees and foggy."
    return "It's 90 degrees and sunny."

tools = [search]

def call_tools(state):
    function_name_to_function = {"search": search}
    messages = state["messages"]
    tool_call = messages[-1]["tool_calls"][0]
    function_name = tool_call["function"]["name"]
    function_arguments = tool_call["function"]["arguments"]
    arguments = json.loads(function_arguments)
    function_response = function_name_to_function[function_name](**arguments)
    tool_message = {
        "tool_call_id": tool_call["id"],
        "role": "tool",
        "name": function_name,
        "content": function_response,
    }
    return {"messages": [tool_message]}

wrapped_client = wrap_openai(openai.Client())

def should_continue(state: State) -> Literal["tools", "__end__"]:
    messages = state["messages"]
    last_message = messages[-1]
    if last_message["tool_calls"]:
        return "tools"
    return "__end__"

def call_model(state: State):
    messages = state["messages"]
    # Calling the wrapped client will automatically infer the correct tracing context
    response = wrapped_client.chat.completions.create(
        messages=messages, model="gpt-6-luna", tools=[tool_schema]
    )
    raw_tool_calls = response.choices[0].message.tool_calls
    tool_calls = [tool_call.to_dict() for tool_call in raw_tool_calls] if raw_tool_calls else []
    response_message = {
        "role": "assistant",
        "content": response.choices[0].message.content,
        "tool_calls": tool_calls,
    }
    return {"messages": [response_message]}

workflow = StateGraph(State)
workflow.add_node("agent", call_model)
workflow.add_node("tools", call_tools)
workflow.add_edge("__start__", "agent")
workflow.add_conditional_edges(
    "agent",
    should_continue,
)
workflow.add_edge("tools", 'agent')

app = workflow.compile()

final_state = app.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)

final_state["messages"][-1]["content"]
```

```typescript TypeScript
**Note:** The below example requires `langsmith>=0.1.39` and `@langchain/langgraph>=0.0.31`

import OpenAI from "openai";
import { StateGraph } from "@langchain/langgraph";
import { wrapOpenAI } from "langsmith/wrappers/openai";
import { traceable } from "langsmith/traceable";

type GraphState = {
  messages: OpenAI.ChatCompletionMessageParam[];
};

const wrappedClient = wrapOpenAI(new OpenAI({}));

const toolSchema: OpenAI.ChatCompletionTool = {
  type: "function",
  function: {
    name: "search",
    description: "Use this tool to query the web.",
    parameters: {
      type: "object",
      properties: {
        query: {
          type: "string",
        },
      },
      required: ["query"],
    }
  }
};

// Wrapping the tool function will automatically trace it with the correct context
const search = traceable(async ({ query }: { query: string }) => {
  if (
    query.toLowerCase().includes("sf") ||
    query.toLowerCase().includes("san francisco")
  ) {
    return "It's 60 degrees and foggy.";
  }
  return "It's 90 degrees and sunny.";
}, { run_type: "tool", name: "Search Tool" });

const callTools = async ({ messages }: GraphState) => {
  const mostRecentMessage = messages[messages.length - 1];
  const toolCalls = (mostRecentMessage as OpenAI.ChatCompletionAssistantMessageParam).tool_calls;
  if (toolCalls === undefined || toolCalls.length === 0) {
    throw new Error("No tool calls passed to node.");
  }
  const toolNameMap = {
    search,
  };
  const functionName = toolCalls[0].function.name;
  const functionArguments = JSON.parse(toolCalls[0].function.arguments);
  const response = await toolNameMap[functionName](functionArguments);
  const toolMessage = {
    tool_call_id: toolCalls[0].id,
    role: "tool",
    name: functionName,
    content: response,
  }
  return { messages: [toolMessage] };
};

const callModel = async ({ messages }: GraphState) => {
  // Calling the wrapped client will automatically infer the correct tracing context
  const response = await wrappedClient.chat.completions.create({
    messages,
    model: "gpt-6-luna",
    tools: [toolSchema],
  });
  const responseMessage = {
    role: "assistant",
    content: response.choices[0].message.content,
    tool_calls: response.choices[0].message.tool_calls ?? [],
  };
  return { messages: [responseMessage] };
};

const shouldContinue = ({ messages }: GraphState) => {
  const lastMessage =
    messages[messages.length - 1] as OpenAI.ChatCompletionAssistantMessageParam;
  if (
    lastMessage?.tool_calls !== undefined &&
    lastMessage?.tool_calls.length > 0
  ) {
    return "tools";
  }
  return "__end__";
}

const workflow = new StateGraph<GraphState>({
  channels: {
    messages: {
      reducer: (a: any, b: any) => a.concat(b),
    }
  }
});

const graph = workflow
  .addNode("model", callModel)
  .addNode("tools", callTools)
  .addEdge("__start__", "model")
  .addConditionalEdges("model", shouldContinue, {
    tools: "tools",
    __end__: "__end__",
  })
  .addEdge("tools", "model")
  .compile();

await graph.invoke({
  messages: [{ role: "user", content: "what is the weather in sf" }]
});
```

### Viewing the trace

**Details view**

Click on the trace, and toggle to the **Details** view on the top right. Your trace in LangSmith should [look like this](https://smith.langchain.com/public/c3d128fa-c618-4b0e-b9d0-ccbb619440d8/r).

**Trajectory view**

The **Trajectory** view in the LangSmith UI shows a simplified conversation history between the user and the agent. This view pulls messages from the top-level trace (including the user’s initial request, tool calls, and the agent’s final response) and represents them in a chat-like format.

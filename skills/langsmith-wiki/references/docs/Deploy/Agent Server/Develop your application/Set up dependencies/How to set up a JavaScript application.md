# How to set up a JavaScript application

An application must be configured with a [configuration file](../../../Get%20started/Reference/LangGraph%20CLI.md#configuration-file) in order to be deployed to LangSmith (or to be self-hosted). This how-to guide discusses the basic steps to set up a JavaScript application for deployment using `package.json` to specify project dependencies.

This walkthrough is based on [this repository](https://github.com/langchain-ai/langgraphjs-studio-starter), which you can play around with to learn more about how to set up your application for deployment.

The final repository structure will look something like this:

```bash
my-app/
├── src # all project code lies within here
│   ├── utils # optional utilities for your graph
│   │   ├── tools.ts # tools for your graph
│   │   ├── nodes.ts # node functions for your graph
│   │   └── state.ts # state definition of your graph
│   └── agent.ts # code for constructing your graph
├── package.json # package dependencies
├── .env # environment variables
└── langgraph.json # configuration file for LangGraph
```

> [!TIP]
>
> LangSmith Agent Server supports deploying a [LangGraph](https://docs.langchain.com/oss/python/langgraph/overview.md) *graph*. However, the implementation of a *node* of a graph can contain arbitrary code. This means any framework can be implemented within a node and deployed on LangSmith Agent Server. This lets you implement your core application logic without using additional LangGraph OSS APIs while still using LangSmith for [deployment](../../../Get%20started/LangSmith%20Agent%20Server.md), scaling, and [observability](../../../../Monitor/Overview/LangSmith%20Observability.md). For more details, refer to [Use any framework with LangSmith Agent Server](../Application%20structure.md#use-any-framework-with-langsmith-deployment).

After each step, an example file directory is provided to demonstrate how code can be organized.

## Specify dependencies

Dependencies can be specified in a `package.json`. If none of these files is created, then dependencies can be specified later in the [configuration file](#create-the-api-config).

Example `package.json` file:

```json
{
  "name": "langgraphjs-studio-starter",
  "packageManager": "yarn@1.22.22",
  "dependencies": {
    "@langchain/core": "^0.2.31",
    "@langchain/langgraph": "^0.2.0",
    "@langchain/openai": "^0.2.8",
    "@langchain/tavily": "^0.1.5"
  }
}
```

When deploying your app, the dependencies will be installed using the package manager of your choice, provided they adhere to the compatible version ranges listed below:

```
"@langchain/core": "^0.3.42",
"@langchain/langgraph": "^0.2.57",
"@langchain/langgraph-checkpoint": "~0.0.16",
```

Example file directory:

```bash
my-app/
└── package.json # package dependencies
```

## Specify environment variables

Environment variables can optionally be specified in a file (e.g. `.env`). See the [Environment Variables reference](../../../Deploy%20to%20Cloud/Reference/Cloud%20Agent%20Server%20environment%20variables.md) to configure additional variables for a deployment.

Example `.env` file:

```
MY_ENV_VAR_1=foo
MY_ENV_VAR_2=bar
OPENAI_API_KEY=key
TAVILY_API_KEY=key_2
```

Example file directory:

```bash
my-app/
├── package.json
└── .env # environment variables
```

## Define graphs

Implement your graphs. Graphs can be defined in a single file or multiple files. Make note of the variable names of each compiled graph to be included in the application. The variable names will be used later when creating the [configuration file](../../../Get%20started/Reference/LangGraph%20CLI.md#configuration-file).

Here is an example `agent.ts`:

```ts
import type { AIMessage } from "@langchain/core/messages";
import { TavilySearch } from "@langchain/tavily";
import { ChatOpenAI } from "@langchain/openai";

import { MessagesAnnotation, StateGraph } from "@langchain/langgraph";
import { ToolNode } from "@langchain/langgraph/prebuilt";

const tools = [new TavilySearch({ maxResults: 3 })];

// Define the function that calls the model
async function callModel(state: typeof MessagesAnnotation.State) {
  /**
   * Call the LLM powering our agent.
   * Feel free to customize the prompt, model, and other logic!
   */
  const model = new ChatOpenAI({
    model: "gpt-6.1-sol",
  }).bindTools(tools);

  const response = await model.invoke([
    {
      role: "system",
      content: `You are a helpful assistant. The current date is ${new Date().getTime()}.`,
    },
    ...state.messages,
  ]);

  // MessagesAnnotation supports returning a single message or array of messages
  return { messages: response };
}

// Define the function that determines whether to continue or not
function routeModelOutput(state: typeof MessagesAnnotation.State) {
  const messages = state.messages;
  const lastMessage: AIMessage = messages[messages.length - 1];
  // If the LLM is invoking tools, route there.
  if ((lastMessage?.tool_calls?.length ?? 0) > 0) {
    return "tools";
  }
  // Otherwise end the graph.
  return "__end__";
}

// Define a new graph.
// See https://docs.langchain.com/oss/javascript/langgraph/graph-api#state for
// more on defining custom graph states.
const workflow = new StateGraph(MessagesAnnotation)
  // Define the two nodes we will cycle between
  .addNode("callModel", callModel)
  .addNode("tools", new ToolNode(tools))
  // Set the entrypoint as `callModel`
  // This means that this node is the first one called
  .addEdge("__start__", "callModel")
  .addConditionalEdges(
    // First, we define the edges' source node. We use `callModel`.
    // This means these are the edges taken after the `callModel` node is called.
    "callModel",
    // Next, we pass in the function that will determine the sink node(s), which
    // will be called after the source node is called.
    routeModelOutput,
    // List of the possible destinations the conditional edge can route to.
    // Required for conditional edges to properly render the graph in Studio
    ["tools", "__end__"]
  )
  // This means that after `tools` is called, `callModel` node is called next.
  .addEdge("tools", "callModel");

// Finally, we compile it!
// This compiles it into a graph you can invoke and deploy.
export const graph = workflow.compile();
```

Example file directory:

```bash
my-app/
├── src # all project code lies within here
│   ├── utils # optional utilities for your graph
│   │   ├── tools.ts # tools for your graph
│   │   ├── nodes.ts # node functions for your graph
│   │   └── state.ts # state definition of your graph
│   └── agent.ts # code for constructing your graph
├── package.json # package dependencies
├── .env # environment variables
└── langgraph.json # configuration file for LangGraph
```

## Create the API config

Create a [configuration file](../../../Get%20started/Reference/LangGraph%20CLI.md#configuration-file) called `langgraph.json`. See the [configuration file reference](../../../Get%20started/Reference/LangGraph%20CLI.md#configuration-file) for detailed explanations of each key in the JSON object of the configuration file.

Example `langgraph.json` file:

```json
{
  "node_version": "20",
  "dockerfile_lines": [],
  "dependencies": ["."],
  "graphs": {
    "agent": "./src/agent.ts:graph"
  },
  "env": ".env"
}
```

Note that the variable name of the `CompiledGraph` appears at the end of the value of each subkey in the top-level `graphs` key (i.e. `:<variable_name>`).

> [!NOTE]
>
> **Configuration Location**
> The configuration file must be placed in a directory that is at the same level or higher than the TypeScript files that contain compiled graphs and associated dependencies.

## Next

After you setup your project and place it in a GitHub repository, it's time to [deploy your app](../../../Get%20started/Deploy%20your%20app%20to%20cloud.md).

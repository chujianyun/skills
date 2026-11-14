# Application structure

To deploy on LangSmith, an application must consist of one or more graphs, a configuration file (`langgraph.json`), a file that specifies dependencies, and an optional `.env` file that specifies environment variables.

This page explains how a LangSmith application is organized and how to provide the configuration details required for deployment.

## Key concepts

To deploy using LangSmith, provide the following information:

1. A [configuration file](#configuration-file-concepts) (`langgraph.json`) that specifies the dependencies, graphs, and environment variables to use for the application.
2. The [graphs](#graphs) that implement the logic of the application.
3. A file that specifies [dependencies](#dependencies) required to run the application.
4. [Environment variables](#environment-variables) that are required for the application to run.

> [!TIP]
>
> **Framework agnostic**
>
> LangSmith Agent Server supports deploying a [LangGraph](https://docs.langchain.com/oss/python/langgraph/overview.md) *graph*. However, the implementation of a *node* of a graph can contain arbitrary code. This means any framework can be implemented within a node and deployed on LangSmith Agent Server. This lets you implement your core application logic without using additional LangGraph OSS APIs while still using LangSmith for [deployment](../../Get%20started/LangSmith%20Agent%20Server.md), scaling, and [observability](../../../Monitor/Overview/LangSmith%20Observability.md). For more details, refer to [Use any framework with LangSmith Agent Server](Application%20structure.md#use-any-framework-with-langsmith-deployment).

## File structure

The following are examples of directory structures for Python and JavaScript applications:

> [tab] Python (requirements.txt)
>
> ```plaintext theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> my-app/
> ├── my_agent # all project code lies within here
> │   ├── utils # utilities for your graph
> │   │   ├── __init__.py
> │   │   ├── tools.py # tools for your graph
> │   │   ├── nodes.py # node functions for your graph
> │   │   └── state.py # state definition of your graph
> │   ├── __init__.py
> │   └── agent.py # code for constructing your graph
> ├── .env # environment variables
> ├── requirements.txt # package dependencies
> └── langgraph.json # configuration file for LangGraph
> ```

> [tab] Python (pyproject.toml)
>
> ```plaintext theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> my-app/
> ├── my_agent # all project code lies within here
> │   ├── utils # utilities for your graph
> │   │   ├── __init__.py
> │   │   ├── tools.py # tools for your graph
> │   │   ├── nodes.py # node functions for your graph
> │   │   └── state.py # state definition of your graph
> │   ├── __init__.py
> │   └── agent.py # code for constructing your graph
> ├── .env # environment variables
> ├── langgraph.json  # configuration file for LangGraph
> └── pyproject.toml # dependencies for your project
> ```

> [tab] JS (package.json)
>
> ```plaintext theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> my-app/
> ├── src # all project code lies within here
> │   ├── utils # optional utilities for your graph
> │   │   ├── tools.ts # tools for your graph
> │   │   ├── nodes.ts # node functions for your graph
> │   │   └── state.ts # state definition of your graph
> │   └── agent.ts # code for constructing your graph
> ├── package.json # package dependencies
> ├── .env # environment variables
> └── langgraph.json # configuration file for LangGraph
> ```

> [!NOTE]
>
> The directory structure of an application can vary depending on the programming language and the package manager used.

## Configuration file

The `langgraph.json` file is a JSON file that specifies the dependencies, graphs, environment variables, and other settings required to deploy an application.

For details on all supported keys in the JSON file, refer to the [LangGraph configuration file reference](../../Get%20started/Reference/LangGraph%20CLI.md#configuration-file).

> [!TIP]
>
> The [LangGraph CLI](../../Get%20started/Reference/LangGraph%20CLI.md) defaults to using the configuration file `langgraph.json` in the current directory.

### Examples

> [tab] Python
>
> * The dependencies involve a custom local package and the `langchain_openai` package.
> * A single graph will be loaded from the file `./your_package/your_file.py` with the variable `agent`.
> * The environment variables are loaded from the `.env` file.
>
> ```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> {
>     "dependencies": [
>         "langchain_openai",
>         "./your_package"
>     ],
>     "graphs": {
>         "my_agent": "./your_package/your_file.py:agent"
>     },
>     "env": "./.env"
> }
> ```

> [tab] JavaScript
>
> * The dependencies will be loaded from a dependency file in the local directory (e.g., `package.json`).
> * A single graph will be loaded from the file `./your_package/your_file.js` with the function `agent`.
> * The environment variable `OPENAI_API_KEY` is set inline.
>
> ```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> {
>     "dependencies": [
>         "."
>     ],
>     "graphs": {
>         "my_agent": "./your_package/your_file.js:agent"
>     },
>     "env": {
>         "OPENAI_API_KEY": "secret-key"
>     }
> }
> ```

## Dependencies

An application may depend on other Python packages or JavaScript libraries (depending on the programming language in which the application is written).

You will generally need to specify the following information for dependencies to be set up correctly:

1. A file in the directory that specifies the dependencies (e.g., `requirements.txt`, `pyproject.toml`, or `package.json`).
2. Either:
   * A `dependencies` key in the [configuration file](#configuration-file-concepts) that points at those package definitions (for example, `"dependencies": ["."]`), or
   * For Python projects managed with [uv](https://docs.astral.sh/uv/), a `source` key with `"kind": "uv"` so the build installs from `pyproject.toml` and `uv.lock` instead of re-resolving from `dependencies`. See [LangGraph CLI](../../Get%20started/Reference/LangGraph%20CLI.md#install-from-a-uv-lockfile).
3. Any additional binaries or system libraries can be specified using `dockerfile_lines` key in the [LangGraph configuration file](#configuration-file-concepts).

## Graphs

Use the `graphs` key in the [configuration file](#configuration-file-concepts) to specify which graphs will be available in the deployed application.

You can specify one or more graphs in the configuration file. Each graph is identified by a unique name and a path to either (1) a compiled graph or (2) a function that defines a graph.

### Define multiple graphs in one deployment

A single `langgraph.json` can define several graphs, so one deployment can serve several agents. Add one entry to `graphs` for each agent:

```json
{
    "dependencies": ["."],
    "graphs": {
        "support_agent": "./my_agent/support.py:agent",
        "research_agent": "./my_agent/research.py:agent"
    },
    "env": "./.env"
}
```

Each key is a graph ID. All graphs in the file share the deployment's `dependencies`, `env`, and image. [Agent Server](../Capabilities/Agent%20Server.md) creates a default assistant for each graph, so clients choose a graph by passing its graph ID as the `assistant_id`. For more information, see [How assistants work with deployments](../Capabilities/Assistants/Assistants.md#how-assistants-work-with-deployments).

Running several agents on one deployment also reduces cost. See [Run multiple agents on one deployment](../../Deploy%20to%20Cloud/Cloud%20platform%20features.md#run-multiple-agents-on-one-deployment).

### Use any framework with LangSmith Agent Server

While LangSmith Agent Server requires applications to be structured as a LangGraph graph, individual nodes within that graph can contain arbitrary code. This means you can use any framework or library within your nodes while still benefiting from LangSmith's deployment infrastructure.

The graph structure serves as a deployment interface, but your core application logic can use whichever tools and frameworks best suit your needs.

To deploy with LangSmith, you need:

> [tab] Python
>
> 1. **A LangGraph graph structure**: Define a graph using [`StateGraph`](https://reference.langchain.com/python/langgraph/graph/state/StateGraph) with [`add_node`](https://reference.langchain.com/python/langgraph/graph/state/StateGraph/add_node) and [`add_edge`](https://reference.langchain.com/python/langgraph/pregel/_draw/add_edge).
> 2. **Node functions with arbitrary logic**: Your node functions can call any framework or library.
> 3. **A compiled graph**: [Compile](https://reference.langchain.com/python/langgraph/graph/state/StateGraph/compile) the graph to create a deployable application.
>
> The following example shows how to wrap your existing application logic within a minimal LangGraph structure:
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langgraph.graph import StateGraph, START, END
> from typing import TypedDict
>
> # Your existing application logic using any framework
> from app_logic import process_data
> from app_logic import fetch_data
>
> class State(TypedDict):
>     input: str
>     result: str
>
> def my_app_node(state: State) -> State:
>     """Node containing arbitrary framework code."""
>     # Use any framework or library here
>     raw_data = fetch_data(state["input"])
>     processed = process_data(raw_data)
>     return {"result": processed}
>
> # Define the graph structure
> graph = StateGraph(State)
> graph.add_node("process", my_app_node)  # Add node with your logic
> graph.add_edge(START, "process")  # Connect start to your node
> graph.add_edge("process", END)  # Connect your node to end
>
> # Compile for deployment
> app = graph.compile()
> ```

> [tab] JavaScript
>
> 1. **A LangGraph graph structure**: Define a graph using [`StateGraph`](https://reference.langchain.com/javascript/langchain-langgraph/index/StateGraph) with [`addNode`](https://reference.langchain.com/javascript/langchain-langgraph/index/StateGraph) and [`addEdge`](https://reference.langchain.com/javascript/langchain-langgraph/index/StateGraph).
> 2. **Node functions with arbitrary logic**: Your node functions can call any framework or library.
> 3. **A compiled graph**: [Compile](https://reference.langchain.com/javascript/langchain-langgraph/index/StateGraph) the graph to create a deployable application.
>
> The following example shows how to wrap your existing application logic within a minimal LangGraph structure:
>
> ```typescript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { StateGraph, START, END } from "@langchain/langgraph";
> import { Annotation } from "@langchain/langgraph";
>
> // Your existing application logic using any framework
> import { processData } from "./app-logic";
> import { fetchData } from "./app-logic";
>
> const State = Annotation.Root({
>   input: Annotation<string>,
>   result: Annotation<string>
> });
>
> async function myAppNode(state: typeof State.State) {
>   // Use any framework or library here
>   const rawData = await fetchData(state.input);
>   const processed = await processData(rawData);
>   return { result: processed };
> }
>
> // Define the graph structure
> const graph = new StateGraph(State)
>   .addNode("process", myAppNode)  // Add node with your logic
>   .addEdge(START, "process")  // Connect start to your node
>   .addEdge("process", END);  // Connect your node to end
>
> // Compile for deployment
> export const app = graph.compile();
> ```

In this example, the node functions (`my_app_node` for Python and `myAppNode` for JavaScript) can contain calls to any framework or library. The LangGraph structure simply provides the deployment interface and orchestration layer.

For end-to-end examples, refer to the deployment guides for [Google ADK](../../Get%20started/Frameworks%20and%20platforms/Deploy%20Google%20ADK%20agents.md) and [Claude Agent SDK, Strands, CrewAI, and AutoGen](../../Get%20started/Frameworks%20and%20platforms/Deploy%20other%20frameworks.md). LangSmith added support for Google ADK through [`deployments-wrap-sdk`](https://pypi.org/project/deployments-wrap-sdk/), an extensible package for wrapping agent SDKs to run on LangSmith Agent Server.

## Environment variables

If you're working with a deployed LangGraph application [locally](../../Get%20started/Develop%20%26%20test/Local%20development%20%26%20testing.md), you can configure environment variables in the `env` key of the [configuration file](#configuration-file-concepts).

For a production deployment, you will typically want to configure the environment variables in the deployment environment.

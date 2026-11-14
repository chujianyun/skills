# How to set up an application with pyproject.toml

An application must be configured with a [configuration file](../../../Get%20started/Reference/LangGraph%20CLI.md#configuration-file) in order to be deployed to LangSmith (or to be self-hosted). This how-to guide discusses the basic steps to set up an application for deployment using `pyproject.toml` to define your package's dependencies.

This example is based on [this repository](https://github.com/langchain-ai/langgraph-example-pyproject), which uses the LangGraph framework.

The final repository structure will look something like this:

```bash
my-app/
├── my_agent # all project code lies within here
│   ├── utils # utilities for your graph
│   │   ├── __init__.py
│   │   ├── tools.py # tools for your graph
│   │   ├── nodes.py # node functions for your graph
│   │   └── state.py # state definition of your graph
│   ├── __init__.py
│   └── agent.py # code for constructing your graph
├── .env # environment variables
├── langgraph.json  # configuration file for LangGraph
└── pyproject.toml # dependencies for your project
```

> [!TIP]
>
> LangSmith Agent Server supports deploying a [LangGraph](https://docs.langchain.com/oss/python/langgraph/overview.md) *graph*. However, the implementation of a *node* of a graph can contain arbitrary code. This means any framework can be implemented within a node and deployed on LangSmith Agent Server. This lets you implement your core application logic without using additional LangGraph OSS APIs while still using LangSmith for [deployment](../../../Get%20started/LangSmith%20Agent%20Server.md), scaling, and [observability](../../../../Monitor/Overview/LangSmith%20Observability.md). For more details, refer to [Use any framework with LangSmith Agent Server](../Application%20structure.md#use-any-framework-with-langsmith-deployment).

You can also set up with:

* `requirements.txt`: for dependency management, check out [this how-to guide](How%20to%20set%20up%20an%20application%20with%20requirements.txt.md) on using `requirements.txt` for LangSmith.
* a monorepo: To deploy a graph located inside a monorepo, take a look at [this repository](https://github.com/langchain-ai/langgraph-example-monorepo) for an example of how to do so.

After each step, an example file directory is provided to demonstrate how code can be organized.

## Specify dependencies

Dependencies can optionally be specified in one of the following files: `pyproject.toml`, `setup.py`, or `requirements.txt`. If none of these files is created, then dependencies can be specified later in the [configuration file](#create-the-configuration-file).

The dependencies below will be included in the image, you can also use them in your code, as long as with a compatible version range:

```
langgraph>=0.4.10,<2
langgraph-sdk>=0.4.4
langgraph-checkpoint>=3.0.1,<5
langchain-core>=0.3.66
langsmith>=0.7.31
orjson>=3.9.7
httpx>=0.25.0
tenacity>=8.0.0
uvicorn>=0.29.0
sse-starlette>=2.1.3,<4.0.0
uvloop>=0.18.0
httptools>=0.5.0
jsonschema-rs>=0.35.0
structlog>=24.1.0
cloudpickle>=3.0.0
truststore>=0.1
protobuf>=6.32.1,<7.0.0
grpcio>=1.85.0,<1.86.0
grpcio-tools>=1.81.0,<1.82.0
grpcio-health-checking>=1.81.0,<1.82.0
opentelemetry-api>=0.0.1
opentelemetry-sdk>=0.0.1
opentelemetry-exporter-otlp-proto-http>=0.0.1
```

Example `pyproject.toml` file:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "my-agent"
version = "0.0.1"
description = "An excellent agent build for LangSmith."
authors = [
    {name = "Assistant", email = "1223+assistant@users.noreply.github.com"}
]
license = {text = "MIT"}
readme = "README.md"
requires-python = ">=3.9"
dependencies = [
    "langgraph>=0.6.0",
    "langchain-fireworks>=0.1.3"
]

[tool.hatch.build.targets.wheel]
packages = ["my_agent"]
```

Example file directory:

```bash
my-app/
└── pyproject.toml   # Python packages required for your graph
```

## Specify environment variables

Environment variables can optionally be specified in a file (e.g. `.env`). See the [Environment Variables reference](../../../Deploy%20to%20Cloud/Reference/Cloud%20Agent%20Server%20environment%20variables.md) to configure additional variables for a deployment.

Example `.env` file:

```
MY_ENV_VAR_1=foo
MY_ENV_VAR_2=bar
FIREWORKS_API_KEY=key
```

Example file directory:

```bash
my-app/
├── .env # file with environment variables
└── pyproject.toml
```

> [!TIP]
>
> By default, LangSmith follows the `uv`/`pip` behavior of **not** installing prerelease versions unless explicitly allowed. If want to use prereleases, you have the following options:
>
> * With `pyproject.toml`: add `allow-prereleases = true` to your `[tool.uv]` section.
> * With `requirements.txt` or `setup.py`: you must explicitly specify every prerelease dependency, including transitive ones. For example, if you declare `a==0.0.1a1` and `a` depends on `b==0.0.1a1`, then you must also explicitly include `b==0.0.1a1` in your dependencies.

## Define graphs

Implement your graphs. Graphs can be defined in a single file or multiple files. Make note of the variable names of each [CompiledStateGraph](https://reference.langchain.com/python/langgraph/graph/state/CompiledStateGraph) to be included in the application. The variable names will be used later when creating the [configuration file](../../../Get%20started/Reference/LangGraph%20CLI.md#configuration-file).

Example `agent.py` file, which shows how to import from other modules you define (code for the modules is not shown here, please see [this repository](https://github.com/langchain-ai/langgraph-example-pyproject) to see their implementation):

```python
# my_agent/agent.py
from typing import Literal
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, END, START
from my_agent.utils.nodes import call_model, should_continue, tool_node # import nodes
from my_agent.utils.state import AgentState # import state

# Define the runtime context
class GraphContext(TypedDict):
    model_name: Literal["anthropic", "openai"]

workflow = StateGraph(AgentState, context_schema=GraphContext)
workflow.add_node("agent", call_model)
workflow.add_node("action", tool_node)
workflow.add_edge(START, "agent")
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "action",
        "end": END,
    },
)
workflow.add_edge("action", "agent")

graph = workflow.compile()
```

Example file directory:

```bash
my-app/
├── my_agent # all project code lies within here
│   ├── utils # utilities for your graph
│   │   ├── __init__.py
│   │   ├── tools.py # tools for your graph
│   │   ├── nodes.py # node functions for your graph
│   │   └── state.py # state definition of your graph
│   ├── __init__.py
│   └── agent.py # code for constructing your graph
├── .env
└── pyproject.toml
```

## Create the configuration file

Create a [configuration file](../../../Get%20started/Reference/LangGraph%20CLI.md#configuration-file) called `langgraph.json`. See the [configuration file reference](../../../Get%20started/Reference/LangGraph%20CLI.md#configuration-file) for detailed explanations of each key in the JSON object of the configuration file.

Example `langgraph.json` file:

```json
{
  "dependencies": ["."],
  "graphs": {
    "agent": "./my_agent/agent.py:graph"
  },
  "env": ".env"
}
```

Note that the variable name of the `CompiledGraph` appears at the end of the value of each subkey in the top-level `graphs` key (i.e. `:<variable_name>`).

> [!WARNING]
>
> **Configuration file location**
> The configuration file must be placed in a directory that is at the same level or higher than the Python files that contain compiled graphs and associated dependencies.

Example file directory:

```bash
my-app/
├── my_agent # all project code lies within here
│   ├── utils # utilities for your graph
│   │   ├── __init__.py
│   │   ├── tools.py # tools for your graph
│   │   ├── nodes.py # node functions for your graph
│   │   └── state.py # state definition of your graph
│   ├── __init__.py
│   └── agent.py # code for constructing your graph
├── .env # environment variables
├── langgraph.json  # configuration file for LangGraph
└── pyproject.toml # dependencies for your project
```

## Next

After you setup your project and place it in a GitHub repository, it's time to [deploy your app](../../../Get%20started/Deploy%20your%20app%20to%20cloud.md).

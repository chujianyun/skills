# Rebuild graph at runtime

> Rebuild your graph with different configurations for each run using ServerRuntime.

You might need to rebuild your graph with a different configuration for a new run. For example, you might want to load different tools depending on the user's credentials. This guide shows how you can do this using `ServerRuntime`.

> [!NOTE]
>
> In most cases, customization is best handled by conditioning on the config within individual nodes rather than dynamically changing the whole graph structure. This makes it easier to test and manage.

## Prerequisites

* Make sure to check out [this how-to guide](../Develop%20your%20application/Set%20up%20dependencies/How%20to%20set%20up%20an%20application%20with%20requirements.txt.md) on setting up your app for deployment first.
* `ServerRuntime` requires `langgraph-api >= 0.7.31` and `langgraph-sdk >= 0.3.5`. Prior to that, graph factories only accepted a single `config: RunnableConfig` argument.

## Define graphs

Let's say you have an app with a simple graph that calls an LLM and returns the response to the user. The app file directory looks like the following:

```
my-app/
|-- langgraph.json
|-- my_project/
|   |-- __init__.py
|   |-- agents.py     # code for your graph
|-- pyproject.toml
```

where the graph is defined in `agents.py`.

### No rebuild

The most common way to deploy your Agent Server is to reference a compiled graph instance that's defined at the top level of your file. An example is below:

```python
# my_project/agents.py
from langgraph.graph import StateGraph, MessagesState, START

async def model(state: MessagesState):
    return {"messages": [{"role": "assistant", "content": "Hi, there!"}]}

graph_workflow = StateGraph(MessagesState)
graph_workflow.add_node("model", model)
graph_workflow.add_edge(START, "model")
agent = graph_workflow.compile()
```

To make the server aware of your graph, you need to specify a path to the variable that contains the [`CompiledStateGraph`](https://reference.langchain.com/python/langgraph/graph/state/CompiledStateGraph) instance in your LangGraph API configuration (`langgraph.json`), e.g.:

```json
{
    "$schema": "https://langgra.ph/schema.json",
    "dependencies": ["."],
    "graphs": {
        "chat_agent": "my_project.agents:agent",
    }
}
```

### Rebuild

To rebuild your graph on each new run, provide a **factory function** that returns (or yields) a graph. The factory can optionally accept a `ServerRuntime` parameter or a `RunnableConfig`. The server inspects your function's type annotations to determine which arguments to inject, so make sure to include the correct type hints. The server's queue workers will call your factory function any time they need to process a run. The function will also be called for certain other endpoints to update state, read state, or to fetch assistant schemas. The `ServerRuntime` tells you which context triggered the call.

> [!NOTE]
>
> `ServerRuntime` is in [beta](../../../LangSmith%20setup/Cloud/Reference/Release%20stages.md) and may change in future releases.

#### Simple factory

The simplest form is a plain `async def` that returns a compiled graph:

```python
from langchain_openai import ChatOpenAI
from langgraph.graph import START, StateGraph
from langchain_core.runnables import RunnableConfig
from langgraph_sdk.runtime import ServerRuntime

from my_agent.utils.state import AgentState

model = ChatOpenAI(model="gpt-6.1-sol")


def make_graph_for_user(user_id: str):
    """Build a graph customized per user."""
    graph_workflow = StateGraph(AgentState)

    async def call_model(state):
        return {"messages": [await model.ainvoke(state["messages"])]}

    graph_workflow.add_node("agent", call_model)
    graph_workflow.add_edge(START, "agent")
    return graph_workflow.compile()


async def make_graph(config: RunnableConfig, runtime: ServerRuntime):
    user = runtime.ensure_user()
    return make_graph_for_user(user.identity)
```

#### Context manager factory

If you need to set up and tear down resources (database connections, load MCP tools, etc.), use an async context manager. Use `runtime.execution_runtime` to check whether the graph is being called for actual execution or just for introspection (schemas, visualization):

```python
import contextlib

from langchain_openai import ChatOpenAI
from langgraph.graph import START, StateGraph
from langchain_core.runnables import RunnableConfig
from langgraph_sdk.runtime import ServerRuntime

from my_agent.utils.state import AgentState

model = ChatOpenAI(model="gpt-6.1-sol")


def make_agent_graph(tools: list):
    """Make a simple LLM agent."""
    graph_workflow = StateGraph(AgentState)
    bound = model.bind_tools(tools)

    async def call_model(state):
        return {"messages": [await bound.ainvoke(state["messages"])]}

    graph_workflow.add_node("agent", call_model)
    graph_workflow.add_edge(START, "agent")
    return graph_workflow.compile()


@contextlib.asynccontextmanager
async def make_graph(runtime: ServerRuntime):
    if ert := runtime.execution_runtime:
        # Only set up expensive resources during actual execution.
        # Introspection calls (get_schema, get_graph, ...) skip this.
        mcp_tools = await connect_mcp(ert.ensure_user())  # your setup logic
        yield make_agent_graph(tools=mcp_tools)
        await disconnect_mcp()  # your teardown logic
    else:
        # For schema/state reads, return a graph with the same
        # topology but no expensive resource setup.
        yield make_agent_graph(tools=[])
```

Finally, specify the path to your factory in `langgraph.json`:

```json
{
    "$schema": "https://langgra.ph/schema.json",
    "dependencies": ["."],
    "graphs": {
        "chat_agent": "my_project.agents:make_graph",
    }
}
```

## ServerRuntime reference

Your factory function receives a `ServerRuntime` instance with the following attributes:

| Attribute | Type | Description |
| - | - | - |
| `access_context` | `str` | Why the factory was called: `"threads.create_run"`, `"threads.update"`, `"threads.read"`, or `"assistants.read"`. |
| `user` | `BaseUser \| None` | The authenticated user, or `None` if no [custom auth](../Auth%20%26%20access%20control/Add%20custom%20authentication.md) is configured. |
| `store` | `BaseStore` | The store instance for persistence and memory. |

**Methods:**

| Method | Description |
| - | - |
| `ensure_user()` | Returns the authenticated user. Raises `PermissionError` if no user is provided. |
| `execution_runtime` | Returns the execution runtime when `access_context` is `"threads.create_run"`, or `None` otherwise. Use this to conditionally set up expensive resources only during execution. |

### Access contexts

The server calls your factory in several contexts beyond just executing runs. In all contexts, the returned graph should have the **same topology** (nodes, edges, state schema). A mismatched topology in write contexts (`threads.create_run`, `threads.update`) can cause incorrect state updates. In read contexts (`threads.read`, `assistants.read`), a mismatch affects reported pending tasks, schemas, and visualizations but won't corrupt data. Use `execution_runtime` to conditionally set up expensive resources without changing the graph structure.

| Context | Description |
| - | - |
| `threads.create_run` | Full graph execution. `execution_runtime` is available. |
| `threads.update` | State update via `aupdate_state`. Does not execute node functions, but it can change the pending tasks. |
| `threads.read` | State reads via `aget_state` / `aget_state_history`. |
| `assistants.read` | Schema and graph introspection for visualization, MCP, A2A, etc. |

## Customize tracing per graph

You can use the factory function to customize or disable tracing for a specific graph. See [Conditional tracing: Customize tracing in deployed agents](../../../Monitor/Trace/Configuration%20%26%20troubleshooting/Agent%20%26%20environment%20settings/Conditional%20tracing.md#customize-tracing-in-deployed-agents) for examples.

See more info on the [LangGraph API configuration file](../../Get%20started/Reference/LangGraph%20CLI.md#configuration-file).

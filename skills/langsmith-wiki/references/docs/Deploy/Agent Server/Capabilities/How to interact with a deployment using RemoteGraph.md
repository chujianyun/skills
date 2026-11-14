# How to interact with a deployment using RemoteGraph

[`RemoteGraph`](../../Get%20started/Reference/RemoteGraph.md) is a client-side interface that allows you to interact with your [deployment](../../Get%20started/LangSmith%20Agent%20Server.md) as if it were a local graph. It provides API parity with [`CompiledGraph`](https://docs.langchain.com/oss/python/langgraph/graph-api#compiling-your-graph), which means that you can use the same methods (`invoke()`, `stream()`, `get_state()`, etc.) in your development and production environments. This page describes how to initialize a `RemoteGraph` and interact with it.

`RemoteGraph` is useful for the following:

* Separation of development and deployment: Build and test a graph locally with `CompiledGraph`, deploy it to LangSmith, and then [use `RemoteGraph`](#initialize-the-graph) to call it in production while working with the same API interface.
* Thread-level persistence: [Persist and fetch the state](#persist-state-at-the-thread-level) of a conversation across calls with a thread ID.
* Subgraph embedding: Compose modular graphs for a multi-agent workflow by embedding a `RemoteGraph` as a [subgraph](#use-as-a-subgraph) within another graph.
* Reusable workflows: Use deployed graphs as nodes or [tools](https://reference.langchain.com/python/langsmith/deployment/remote_graph/#langgraph.pregel.remote.RemoteGraph.as_tool), so that you can reuse and expose complex logic.

> [!WARNING]
>
> **Important: Avoid calling the same deployment**
>
> `RemoteGraph` is designed to call graphs on other deployments. Do not use `RemoteGraph` to call itself or another graph on the same deployment, as this can lead to deadlocks and resource exhaustion. Instead, use local graph composition or [subgraphs](https://docs.langchain.com/oss/python/langgraph/use-subgraphs.md) for graphs within the same deployment.

## Prerequisites

Before getting started with `RemoteGraph`, make sure you have:

* Access to [LangSmith](../../../Monitor/Overview/LangSmith%20Observability.md), where your graphs are developed and managed.
* A running [Agent Server](Agent%20Server.md), which hosts your deployed graphs for remote interaction.

## Initialize the graph

When initializing a `RemoteGraph`, you must always specify:

* `name`: The name of the graph you want to interact with **or** an assistant ID. If you specify a graph name, the default assistant will be used. If you specify an assistant ID, that specific assistant will be used. The graph name is the same name you use in the `langgraph.json` configuration file for your deployment.
* `api_key`: A valid [LangSmith API key](../../../LangSmith%20setup/Account/Create%20an%20account%20and%20API%20key.md). You can set as an environment variable (`LANGSMITH_API_KEY`) or pass directly in the `api_key` argument. You can also provide the API key in the `client` / `sync_client` arguments, if `LangGraphClient` / `SyncLangGraphClient` was initialized with the `api_key` argument.

Additionally, you have to provide one of the following:

* [`url`](#use-a-url): The URL of the deployment you want to interact with. If you pass the `url` argument, both sync and async clients will be created using the provided URL, headers (if provided), and default configuration values (e.g., timeout).
* [`client`](#use-a-client): A `LangGraphClient` instance for interacting with the deployment asynchronously (e.g., using `.astream()`, `.ainvoke()`, `.aget_state()`, `.aupdate_state()`).
* `sync_client`: A `SyncLangGraphClient` instance for interacting with the deployment synchronously (e.g., using `.stream()`, `.invoke()`, `.get_state()`, `.update_state()`).

> [!NOTE]
>
> If you pass both `client` or `sync_client` as well as the `url` argument, they will take precedence over the `url` argument. If none of the `client` / `sync_client` / `url` arguments are provided, `RemoteGraph` will raise a `ValueError` at runtime.

### Use a URL

```python Python
from langgraph.pregel.remote import RemoteGraph

url = "<DEPLOYMENT_URL>"

# Using graph name (uses default assistant)
graph_name = "agent"
remote_graph = RemoteGraph(graph_name, url=url)

# Using assistant ID
assistant_id = "<ASSISTANT_ID>"
remote_graph = RemoteGraph(assistant_id, url=url)
```

```typescript JavaScript
import { RemoteGraph } from "@langchain/langgraph/remote";

const url = "<DEPLOYMENT_URL>";

// Using graph name (uses default assistant)
const graphName = "agent";
const remoteGraph = new RemoteGraph({ graphId: graphName, url });

// Using assistant ID
const assistantId = "<ASSISTANT_ID>";
const remoteGraph = new RemoteGraph({ graphId: assistantId, url });
```

### Use a client

```python Python
from langgraph_sdk import get_client, get_sync_client
from langgraph.pregel.remote import RemoteGraph

url = "<DEPLOYMENT_URL>"
client = get_client(url=url)
sync_client = get_sync_client(url=url)

# Using graph name (uses default assistant)
graph_name = "agent"
remote_graph = RemoteGraph(graph_name, client=client, sync_client=sync_client)

# Using assistant ID
assistant_id = "<ASSISTANT_ID>"
remote_graph = RemoteGraph(assistant_id, client=client, sync_client=sync_client)
```

```typescript JavaScript
import { Client } from "@langchain/langgraph-sdk";
import { RemoteGraph } from "@langchain/langgraph/remote";

const client = new Client({ apiUrl: "<DEPLOYMENT_URL>" });

// Using graph name (uses default assistant)
const graphName = "agent";
const remoteGraph = new RemoteGraph({ graphId: graphName, client });

// Using assistant ID
const assistantId = "<ASSISTANT_ID>";
const remoteGraph = new RemoteGraph({ graphId: assistantId, client });
```

## Invoke the graph

`RemoteGraph` implements the same Runnable interface as `CompiledGraph`, so you can use it in the same way as a compiled graph. It supports the full set of standard methods, including `.invoke()`, `.stream()`, `.get_state()`, and `.update_state()`, as well as their asynchronous variants.

### Asynchronously

> [!NOTE]
>
> To use the graph asynchronously, you must provide either the `url` or `client` when initializing the `RemoteGraph`.

```python Python
# invoke the graph
result = await remote_graph.ainvoke({
    "messages": [{"role": "user", "content": "what's the weather in sf"}]
})

# stream outputs from the graph
async for chunk in remote_graph.astream({
    "messages": [{"role": "user", "content": "what's the weather in la"}]
}):
    print(chunk)
```

```typescript JavaScript
// invoke the graph
const result = await remoteGraph.invoke({
    messages: [{role: "user", content: "what's the weather in sf"}]
})

// stream outputs from the graph
for await (const chunk of await remoteGraph.stream({
    messages: [{role: "user", content: "what's the weather in la"}]
})):
    console.log(chunk)
```

### Synchronously

> [!NOTE]
>
> To use the graph synchronously, you must provide either the `url` or `sync_client` when initializing the `RemoteGraph`.

```python Python
# invoke the graph
result = remote_graph.invoke({
    "messages": [{"role": "user", "content": "what's the weather in sf"}]
})

# stream outputs from the graph
for chunk in remote_graph.stream({
    "messages": [{"role": "user", "content": "what's the weather in la"}]
}):
    print(chunk)
```

## Persist state at the thread level

By default, graph runs (for example, calls made with `.invoke()` or `.stream()`) are stateless, which means that intermediate checkpoints and the final state are not persisted after a run.

If you want to preserve the outputs of a run—for example, to support human-in-the-loop workflows—you can create a thread and pass its ID through the `config` argument. This works the same way as with a regular compiled graph:

> [!NOTE]
>
> `RemoteGraph` sends only `recursion_limit`, `tags`, `metadata`, and `configurable` from the config to the deployment, and sends `thread_id` from `configurable` as the run's thread. It drops `run_id` and `run_name`, so you cannot set a custom run ID or run name. Agent Server assigns the run ID.

```python Python
from langgraph_sdk import get_sync_client

url = "<DEPLOYMENT_URL>"
graph_name = "agent"
sync_client = get_sync_client(url=url)
remote_graph = RemoteGraph(graph_name, url=url)

# create a thread (or use an existing thread instead)
thread = sync_client.threads.create()

# invoke the graph with the thread config
config = {"configurable": {"thread_id": thread["thread_id"]}}
result = remote_graph.invoke({
    "messages": [{"role": "user", "content": "what's the weather in sf"}]
}, config=config)

# verify that the state was persisted to the thread
thread_state = remote_graph.get_state(config)
print(thread_state)
```

```typescript JavaScript
import { Client } from "@langchain/langgraph-sdk";
import { RemoteGraph } from "@langchain/langgraph/remote";

const url = "<DEPLOYMENT_URL>";
const graphName = "agent";
const client = new Client({ apiUrl: url });
const remoteGraph = new RemoteGraph({ graphId: graphName, url });

// create a thread (or use an existing thread instead)
const thread = await client.threads.create();

// invoke the graph with the thread config
const config = { configurable: { thread_id: thread.thread_id }};
const result = await remoteGraph.invoke({
  messages: [{ role: "user", content: "what's the weather in sf" }],
}, config);

// verify that the state was persisted to the thread
const threadState = await remoteGraph.getState(config);
console.log(threadState);
```

## Use as a subgraph

> [!NOTE]
>
> If you need to use a `checkpointer` with a graph that has a `RemoteGraph` subgraph node, make sure to use UUIDs as thread IDs.

A graph can also call out to multiple `RemoteGraph` instances as [*subgraph*](https://docs.langchain.com/oss/python/langgraph/use-subgraphs.md) nodes. This allows for modular, scalable workflows where different responsibilities are split across separate graphs.

`RemoteGraph` exposes the same interface as a regular `CompiledGraph`, so you can use it directly as a subgraph inside another graph. For example:

```python Python
from langgraph_sdk import get_sync_client
from langgraph.graph import StateGraph, MessagesState, START
from typing import TypedDict

url = "<DEPLOYMENT_URL>"
graph_name = "agent"
remote_graph = RemoteGraph(graph_name, url=url)

# define parent graph
builder = StateGraph(MessagesState)
# add remote graph directly as a node
builder.add_node("child", remote_graph)
builder.add_edge(START, "child")
graph = builder.compile()

# invoke the parent graph
result = graph.invoke({
    "messages": [{"role": "user", "content": "what's the weather in sf"}]
})
print(result)

# stream outputs from both the parent graph and subgraph
for chunk in graph.stream({
    "messages": [{"role": "user", "content": "what's the weather in sf"}]
}, subgraphs=True):
    print(chunk)
```

```typescript JavaScript
import { MessagesAnnotation, StateGraph, START } from "@langchain/langgraph";
import { RemoteGraph } from "@langchain/langgraph/remote";

const url = "<DEPLOYMENT_URL>";
const graphName = "agent";
const remoteGraph = new RemoteGraph({ graphId: graphName, url });

// define parent graph and add remote graph directly as a node
const graph = new StateGraph(MessagesAnnotation)
  .addNode("child", remoteGraph)
  .addEdge(START, "child")
  .compile()

// invoke the parent graph
const result = await graph.invoke({
  messages: [{ role: "user", content: "what's the weather in sf" }]
});
console.log(result);

// stream outputs from both the parent graph and subgraph
for await (const chunk of await graph.stream({
  messages: [{ role: "user", content: "what's the weather in la" }]
}, { subgraphs: true })) {
  console.log(chunk);
}
```

# Distributed tracing with Agent Server

> Unify traces when calling your deployed Agent Server from another service using RemoteGraph or the SDK.

When you call a deployed [Agent Server](Agent%20Server.md) from another service, you can propagate trace context so that the entire request appears as a single unified trace in LangSmith. This uses LangSmith's [distributed tracing](../../../Monitor/Trace/Configuration%20%26%20troubleshooting/Advanced%20tracing%20techniques/Implement%20distributed%20tracing.md) capabilities, which propagate context via HTTP headers.

## How it works

Distributed tracing links runs across services using context propagation headers:

1. The **client** infers the trace context from the current run and sends it as HTTP headers.
2. The **server** reads the headers and adds them to the run's config and metadata as `langsmith-trace` and `langsmith-project` configurable values. You can choose to use these to set the tracing context for a given run when your agent is used.

The headers used are:

* `langsmith-trace`: Contains the trace's dotted order.
* `baggage`: Specifies the LangSmith project and other optional tags and metadata.

To opt-in to distributed tracing, both client and server need to opt in.

## Configure the server

To accept distributed trace context, your graph must read the trace headers from the config and set the tracing context. The headers are passed through the `configurable` field as `langsmith-trace` and `langsmith-project`.

> [!WARNING]
>
> Distributed-tracing headers (`langsmith-trace`, `baggage`) are consumed as trusted tracing context. Only configure your server to apply inbound trace context for deployments called by trusted, internal services. If your Agent Server receives requests directly from untrusted third parties or the public internet, do not propagate these headers into the tracing context: strip them at your gateway or proxy instead. Trusting `baggage` from an external caller lets them influence how your runs are recorded.

```python
import contextlib
import langsmith as ls
from langgraph.graph import StateGraph, MessagesState

# Define your graph
builder = StateGraph(MessagesState)
# ... add nodes and edges ...
my_graph = builder.compile()

@contextlib.contextmanager
async def graph(config):
    configurable = config.get("configurable", {})
    parent_trace = configurable.get("langsmith-trace")
    parent_project = configurable.get("langsmith-project")
    # If you want to also include metadata and tags from the client
    metadata = configurable.get("langsmith-metadata")
    tags = configurable.get("langsmith-tags")
    with ls.tracing_context(parent=parent_trace, project_name=parent_project, metadata=metadata, tags=tags):
        yield my_graph
```

Export this `graph` function in your `langgraph.json`:

```json
{
  "graphs": {
    "agent": "./src/agent.py:graph"
  }
}
```

## Connect from the client

> [tab] RemoteGraph
>
> Set `distributed_tracing=True` when initializing [`RemoteGraph`](../../Get%20started/Reference/RemoteGraph.md). This automatically propagates trace headers on all requests.
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langgraph.graph import StateGraph
> from langgraph.pregel.remote import RemoteGraph
>
> remote_graph = RemoteGraph(
>     "agent",
>     url="<DEPLOYMENT_URL>",
>     distributed_tracing=True,  # Enable trace propagation
> )
>
> def subgraph_node(query: str):
>     # Trace context is automatically propagated
>     return remote_graph.invoke({
>         "messages": [{"role": "user", "content": query}]
>     })['messages'][-1]['content']
>
> # The RemoteGraph is called in the context of some on going work.
> # This could be a parent LangGraph agent, code traced with `@ls.traceable`,
> # or any other instrumented code.
> graph = (
>         StateGraph(str)
>             .add_node(subgraph_node)
>             .add_edge("__start__", "subgraph_node")
>             .compile()
> )
> # The remote graph's execution will appear as a child of this trace
> result = graph.invoke("What's the weather in SF?")
> ```

> [tab] SDK
>
> If you're using the [LangGraph SDK](../../../Monitor/Reference/LangSmith%20reference.md) directly, propagate trace headers manually using `run_tree.to_headers()`:
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langgraph_sdk import get_client
> import langsmith as ls
>
> client = get_client(url="<DEPLOYMENT_URL>")
>
> with ls.trace("call_remote_agent", inputs={"query": query}) as rt:
>     headers = rt.to_headers()
>     async for chunk in client.runs.stream(
>         thread_id=None,
>         assistant_id="agent",
>         input={"messages": [{"role": "user", "content": query}]},
>         stream_mode="values",
>         headers=headers,  # Pass trace headers
>     ):
>         pass
>     return chunk
>
> result = await call_remote_agent("What's the weather in SF?")
> ```

## Related

* [Distributed tracing](../../../Monitor/Trace/Configuration%20%26%20troubleshooting/Advanced%20tracing%20techniques/Implement%20distributed%20tracing.md): General distributed tracing concepts and patterns
* [RemoteGraph](How%20to%20interact%20with%20a%20deployment%20using%20RemoteGraph.md): Full guide to interacting with deployments using RemoteGraph

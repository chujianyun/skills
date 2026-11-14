# RemoteGraph

> **Class** in `langgraph`

📖 [View in docs](RemoteGraph.md)

The `RemoteGraph` class is a client implementation for calling remote
APIs that implement the LangGraph Server API specification.

For example, the `RemoteGraph` class can be used to call APIs from deployments
on LangSmith Deployment.

`RemoteGraph` behaves the same way as a `Graph` and can be used directly as
a node in another `Graph`.

## Signature

```python
RemoteGraph(
    self,
    assistant_id: str,
    /,
    *,
    url: str | None = None,
    api_key: str | None = None,
    headers: dict[str, str] | None = None,
    client: LangGraphClient | None = None,
    sync_client: SyncLangGraphClient | None = None,
    config: RunnableConfig | None = None,
    name: str | None = None,
    distributed_tracing: bool = False,
)
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `assistant_id` | `str` | Yes | The assistant ID or graph name of the remote graph to use. |
| `url` | `str \| None` | No | The URL of the remote API. (default: `None`) |
| `api_key` | `str \| None` | No | The API key to use for authentication. If not provided, it will be read from the environment (`LANGGRAPH_API_KEY`, `LANGSMITH_API_KEY`, or `LANGCHAIN_API_KEY`). (default: `None`) |
| `headers` | `dict[str, str] \| None` | No | Additional headers to include in the requests. (default: `None`) |
| `client` | `LangGraphClient \| None` | No | A `LangGraphClient` instance to use instead of creating a default client. (default: `None`) |
| `sync_client` | `SyncLangGraphClient \| None` | No | A `SyncLangGraphClient` instance to use instead of creating a default client. (default: `None`) |
| `config` | `RunnableConfig \| None` | No | An optional `RunnableConfig` instance with additional configuration. (default: `None`) |
| `name` | `str \| None` | No | Human-readable name to attach to the RemoteGraph instance. This is useful for adding `RemoteGraph` as a subgraph via `graph.add_node(remote_graph)`. If not provided, defaults to the assistant ID. (default: `None`) |
| `distributed_tracing` | `bool` | No | Whether to enable sending LangSmith distributed tracing headers. (default: `False`) |

## Extends

- `PregelProtocol`

## Constructors

```python
__init__(
    self,
    assistant_id: str,
    /,
    *,
    url: str | None = None,
    api_key: str | None = None,
    headers: dict[str, str] | None = None,
    client: LangGraphClient | None = None,
    sync_client: SyncLangGraphClient | None = None,
    config: RunnableConfig | None = None,
    name: str | None = None,
    distributed_tracing: bool = False,
)
```

| Name | Type |
|------|------|
| `assistant_id` | `str` |
| `url` | `str \| None` |
| `api_key` | `str \| None` |
| `headers` | `dict[str, str] \| None` |
| `client` | `LangGraphClient \| None` |
| `sync_client` | `SyncLangGraphClient \| None` |
| `config` | `RunnableConfig \| None` |
| `name` | `str \| None` |
| `distributed_tracing` | `bool` |


## Properties

- `assistant_id`
- `name`
- `config`
- `distributed_tracing`
- `client`
- `sync_client`

## Methods

- [`copy()`](https://reference.langchain.com/python/langgraph/pregel/remote/RemoteGraph/copy)
- [`with_config()`](https://reference.langchain.com/python/langgraph/pregel/remote/RemoteGraph/with_config)
- [`get_graph()`](https://reference.langchain.com/python/langgraph/pregel/remote/RemoteGraph/get_graph)
- [`aget_graph()`](https://reference.langchain.com/python/langgraph/pregel/remote/RemoteGraph/aget_graph)
- [`get_state()`](https://reference.langchain.com/python/langgraph/pregel/remote/RemoteGraph/get_state)
- [`aget_state()`](https://reference.langchain.com/python/langgraph/pregel/remote/RemoteGraph/aget_state)
- [`get_state_history()`](https://reference.langchain.com/python/langgraph/pregel/remote/RemoteGraph/get_state_history)
- [`aget_state_history()`](https://reference.langchain.com/python/langgraph/pregel/remote/RemoteGraph/aget_state_history)
- [`bulk_update_state()`](https://reference.langchain.com/python/langgraph/pregel/remote/RemoteGraph/bulk_update_state)
- [`abulk_update_state()`](https://reference.langchain.com/python/langgraph/pregel/remote/RemoteGraph/abulk_update_state)
- [`update_state()`](https://reference.langchain.com/python/langgraph/pregel/remote/RemoteGraph/update_state)
- [`aupdate_state()`](https://reference.langchain.com/python/langgraph/pregel/remote/RemoteGraph/aupdate_state)
- [`stream()`](https://reference.langchain.com/python/langgraph/pregel/remote/RemoteGraph/stream)
- [`astream()`](https://reference.langchain.com/python/langgraph/pregel/remote/RemoteGraph/astream)
- [`stream_events()`](https://reference.langchain.com/python/langgraph/pregel/remote/RemoteGraph/stream_events)
- [`astream_events()`](https://reference.langchain.com/python/langgraph/pregel/remote/RemoteGraph/astream_events)
- [`invoke()`](https://reference.langchain.com/python/langgraph/pregel/remote/RemoteGraph/invoke)
- [`ainvoke()`](https://reference.langchain.com/python/langgraph/pregel/remote/RemoteGraph/ainvoke)

---

[View source on GitHub](https://github.com/langchain-ai/langgraph/blob/a054ed08dcee7ecc4105706d38c0b4aa0b3c3c32/libs/langgraph/langgraph/pregel/remote.py#L120)

# Connections

> Connection lifecycle, multiple servers, deployment scaling, protocol eras, and caching for MCP in LangChain.

> [!NOTE]
>
> The `langchain.mcp` namespace requires `langchain[mcp]>=1.4.0` and is in beta. The API may change.

[`MCPAdapter`](https://reference.langchain.com/python/langchain/mcp/adapter/MCPAdapter) opens an MCP connection, discovers tools, and returns LangChain tools your agent can call. How you pass servers in, and how long you keep the adapter open, depends on the shape of your app. The connection itself is FastMCP's; this page covers the LangChain patterns and links out to FastMCP for transport and client details.

Prefer the [default lifecycle](#connection-lifecycle) unless you are connecting to several servers or deploying many concurrent runs. For what a single target can be (URL, script path, in-process server), see [Transports](Model%20Context%20Protocol%20%28MCP%29.md#transports).

## Choose a pattern

Pick one row from each table. Server shape and connection lifetime are independent; any shape works with any lifetime.

**Server shape**

| If you need… | Use | Go to |
| - | - | - |
| One server | A URL, `Path`, or in-process target | [Transports](Model%20Context%20Protocol%20%28MCP%29.md#transports) |
| Several servers behind one connection | An `MCPConfig` dict | [MCPConfig](#one-aggregate-connection-with-mcpconfig) |
| Several servers with separate auth, protocol eras, or pools | A [`ClientGroup`](https://gofastmcp.com/clients/client-groups) | [ClientGroup](#independent-connections-with-clientgroup) |

**Connection lifetime**

| Situation | Pattern | Go to |
| - | - | - |
| Script, notebook, or most agents | Discover inside `async with`, then exit | [Connection lifecycle](#connection-lifecycle) |
| Hold one session across several tool calls in a run | Keep the adapter open around the agent call | [One session per invocation](#one-session-per-invocation) |
| Many concurrent runs in a deployment | Discover per run; reuse a [shared pool](#shared-connection-pool) and [cache](#caching) | [Scale a deployment](#scale-a-deployment) |

## Connection lifecycle

[`MCPAdapter`](https://reference.langchain.com/python/langchain/mcp/adapter/MCPAdapter) is an async context manager. Entering it connects the underlying client; exiting it releases the connection. Discovery happens inside the context, but the tools it returns hold the client, so they stay callable after the context exits.

To discover tools and build an agent (the default pattern):

```python
from langchain.agents import create_agent
from langchain.mcp import MCPAdapter


async def build_agent(target):
    # Discover and build the agent inside the adapter's context. The tools hold
    # the client, so the agent stays usable after the context exits.
    async with MCPAdapter(target) as adapter:
        tools = await adapter.list_tools()
        return create_agent("claude-sonnet-5", tools)
```

You do not need to keep the adapter open for the life of the agent. Prefer this pattern unless you are [holding a session open](#one-session-per-invocation) or [scaling a deployment](#scale-a-deployment).

### One session per invocation

The tools [`MCPAdapter`](https://reference.langchain.com/python/langchain/mcp/adapter/MCPAdapter) returns are reentrant: each time a tool is invoked, it opens the client, runs the MCP call, and releases it, whether or not a connection is already held elsewhere. A single agent run therefore opens one session per tool call and closes it when the call returns, rather than holding a session open across the whole run. This keeps a long-running agent from pinning an idle connection between tool calls, and it is why the tools stay callable after the discovery context exits.

If you want a session held open across several calls, keep the adapter's context open when you call the agent. The reentrant client reuses the existing connection rather than opening a second one.

## Multiple servers

To give one agent tools from several servers, choose `MCPConfig` when a single aggregate connection is enough, or `ClientGroup` when each server needs its own connection (different [protocol eras](#protocol-eras), [per-server authentication](Authentication.md#per-server-authentication), or a [shared pool](#shared-connection-pool) configured per client).

### One aggregate connection with `MCPConfig`

Give the adapter an `MCPConfig` dict to connect to several servers behind one aggregate endpoint. FastMCP prefixes every tool with its config key, so two servers exposing the same tool name stay distinguishable in the list handed to a model:

```python
from langchain.agents import create_agent
from langchain.mcp import MCPAdapter

CONFIG = {
    "mcpServers": {
        "weather": {"command": "python", "args": ["/path/to/weather_server.py"]},
        "calc": {"command": "python", "args": ["/path/to/calc_server.py"]},
    }
}


async def fleet_agent(config):
    async with MCPAdapter(config) as adapter:
        # Every tool is prefixed with its config key (`weather_...`, `calc_...`),
        # so two servers exposing the same tool name stay distinguishable.
        tools = await adapter.list_tools()
        return create_agent("claude-sonnet-5", tools)
```

Each backend is addressed independently, so a fleet can mix transports: one server over stdio, another over HTTP. An `MCPConfig` fleet shares a single negotiated [protocol era](#protocol-eras) across every backend, though: add a legacy-only server and the whole fleet drops to the legacy era.

### Independent connections with `ClientGroup`

To keep each server on its own connection, pass a [`ClientGroup`](https://gofastmcp.com/clients/client-groups). Each member keeps its own negotiated protocol era, authentication, and handlers, and the group routes each call back to the client that advertised the tool. This is what lets a legacy and a modern server run side by side, and it namespaces tools the same way so identical tool names across servers never collide:

```python
from fastmcp.client import Client
from fastmcp.client.group import ClientGroup
from langchain.agents import create_agent
from langchain.mcp import MCPAdapter


async def agent_from_group(legacy_url: str, modern_url: str):
    # One connection per server: a `ClientGroup` keeps each server on its own
    # negotiated protocol era, so a legacy and a modern server run side by side.
    # It also namespaces every tool as `{server}_{tool}`, so two servers exposing
    # the same tool name stay distinct.
    group = ClientGroup(
        {
            "weather": Client(legacy_url, mode="legacy"),
            "calc": Client(modern_url, mode="auto"),
        }
    )
    async with MCPAdapter(group) as adapter:
        tools = await adapter.list_tools()
        return create_agent("claude-sonnet-5", tools)
```

## Scale a deployment

A deployment that serves many runs should discover per run but reuse its connections underneath, rather than reconnecting on every request. Build the agent inside a [`langgraph dev`](https://docs.langchain.com/oss/python/langgraph/local-server) graph factory so each run picks up the current tool catalog, and let a [shared connection pool](#shared-connection-pool) and [response cache](#caching) absorb the cost:

```python
SERVERS = {
    "weather": "http://localhost:8001/mcp",
    "calc": "http://localhost:8002/mcp",
}


async def make_graph():
    """Build an agent over an MCP fleet. Called once per run by `langgraph dev`."""
    config = {"mcpServers": {name: {"url": url} for name, url in SERVERS.items()}}
    # A long-lived deployment discovers per run, but reuses one HTTP connection
    # pool underneath. `cache_mode="use"` serves a cached tool list within the
    # server's TTL instead of re-listing on every run.
    async with MCPAdapter(config) as adapter:
        tools = await adapter.list_tools(cache_mode="use")
        return create_agent("claude-sonnet-5", tools)
```

> [!NOTE]
>
> In a `langgraph dev` graph factory, the annotated parameter types and the return type must be importable at runtime, not only under `TYPE_CHECKING`. `langgraph-api` classifies the factory with `typing.get_type_hints()`; if an annotation cannot resolve, it injects a config dict instead of the runtime.

On [Agent Server](https://docs.langchain.com/langsmith/agent-server-overview.md), register that factory in `langgraph.json` instead of exporting a static compiled graph. Tools from `list_tools()` stay callable after the adapter context exits, so returning the agent after discovery is enough for most MCP setups. Use a [context manager factory](https://docs.langchain.com/langsmith/graph-rebuild.md#context-manager-factory) when you need teardown around the run, or when you skip expensive MCP work on schema and state reads with `execution_runtime`.

For a fully worked deployment example, including per-user authentication that mints a token for each caller, see [Authentication](Authentication.md#per-user-authentication).

### Shared connection pool

By default each FastMCP client manages its own HTTP connections. Across a fleet of servers, or many concurrent runs, that means many independent pools. To share one pool, pass an `httpx_client_factory` that draws from a single transport, and lend it out without letting any one client close it:

```python
import httpx2
from fastmcp.client import Client
from fastmcp.client.group import ClientGroup
from fastmcp.client.transports import StreamableHttpTransport
from langchain.mcp import MCPAdapter

# One connection pool, shared by every server the deployment talks to.
_POOL = httpx2.AsyncHTTPTransport()


class _SharedPool(httpx2.AsyncBaseTransport):
    """Lend `_POOL` to each client without letting any client close it."""

    handle_async_request = _POOL.handle_async_request

    async def aclose(self) -> None: ...


def _client_factory(**kwargs: object) -> httpx2.AsyncClient:
    return httpx2.AsyncClient(transport=_SharedPool(), **kwargs)


async def load_over_shared_pool(servers: dict[str, str]) -> list:
    # Every client draws HTTP connections from the same pool, so a fleet of
    # servers does not each open its own.
    group = ClientGroup(
        {
            name: Client(
                StreamableHttpTransport(url, httpx_client_factory=_client_factory)
            )
            for name, url in servers.items()
        }
    )
    async with MCPAdapter(group) as adapter:
        return await adapter.list_tools()
```

Because every client borrows from `_POOL`, the deployment opens one set of HTTP connections for the whole fleet rather than one per server.

## Caching

FastMCP can cache the result of `list_tools` so repeated discovery avoids a network round trip. Caching is opt-in and honors the server's own cache hints, so it only takes effect against modern-era servers that advertise them.

`list_tools()` accepts a `cache_mode` that selects how discovery reads a configured cache:

* **`use`** (the default): serve a cached tool list when one is present and still within the server's TTL hint, otherwise fetch and store.
* **`refresh`**: fetch a fresh list from the server and repopulate the cache.
* **`bypass`**: skip the cache entirely.

```python
tools = await adapter.list_tools(cache_mode="refresh")
```

The cache and its per-principal isolation are configured on the client itself, with `Client(cache=...)`. For a shared store across a fleet of replicas, or partitioning cached responses per user, see [Response caching](https://gofastmcp.com/clients/client#response-caching) in the FastMCP documentation.

## Protocol eras

MCP changed how a client and server agree on what each supports. The **legacy** era begins every connection with an `initialize` handshake; the **modern** era (protocol version `2026-07-28` and later) discovers support by probing the server's `server/discover` endpoint. FastMCP negotiates the era per connection, so nothing on the LangChain side has to know which a given server speaks.

To hold tools from servers on different eras in one agent, give each its own connection so it keeps the best era its server supports, either through a [`ClientGroup`](#independent-connections-with-clientgroup) or one adapter per server. A prebuilt `fastmcp.Client` selects the era with its `mode` parameter:

```python
from fastmcp.client import Client


async def agent_across_eras(legacy_target, modern_target):
    # MCP has two protocol eras. FastMCP negotiates per connection, so a
    # separate adapter per server lets each keep the best era its own server
    # supports. `mode="legacy"` pins the handshake era; `mode="auto"` (the
    # default) negotiates the newest the server understands.
    legacy = Client(legacy_target, mode="legacy")
    modern = Client(modern_target, mode="auto")
    async with (
        MCPAdapter(legacy) as legacy_adapter,
        MCPAdapter(modern) as modern_adapter,
    ):
        tools = await legacy_adapter.list_tools() + await modern_adapter.list_tools()
        return create_agent("claude-sonnet-5", tools)
```

Passing both servers as a single `MCPConfig` fleet instead would negotiate one era for everything the fleet holds, dropping every server to the oldest era any member requires.

For the full negotiation rules, see [Protocol negotiation](https://gofastmcp.com/clients/client#protocol-negotiation) in the FastMCP documentation.

## See also

* [Authentication](Authentication.md): Bearer, OAuth, and per-user credentials.

* [Run a local Agent Server](https://docs.langchain.com/oss/python/langgraph/local-server.md): Graph factories for long-lived deployments.

* [Rebuild a graph at runtime](https://docs.langchain.com/langsmith/graph-rebuild.md): Factory forms for Agent Server, including the context manager pattern.

* [FastMCP connection lifecycle](https://gofastmcp.com/clients/client#connection-lifecycle)

* [MCP configuration format](https://gofastmcp.com/integrations/mcp-json-configuration)

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/mcp/connections.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

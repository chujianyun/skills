# Model Context Protocol (MCP)

> Connect LangChain agents to MCP servers with MCPAdapter.

[Model Context Protocol (MCP)](https://modelcontextprotocol.io) is an open protocol that standardizes how applications provide tools and context to language models. LangChain agents call tools defined on MCP servers through [`MCPAdapter`](https://reference.langchain.com/python/langchain/mcp/adapter/MCPAdapter), which discovers a server's tools and adapts them into LangChain tools you can pass straight to [`create_agent`](https://reference.langchain.com/python/langchain/agents/factory/create_agent).

[`MCPAdapter`](https://reference.langchain.com/python/langchain/mcp/adapter/MCPAdapter) is built on [FastMCP](https://gofastmcp.com), which handles transport inference, protocol negotiation, connection management, and authentication. This section covers the LangChain-specific layer and links out to the FastMCP client documentation for the connection details underneath.

> [!NOTE]
>
> The `langchain.mcp` namespace requires `langchain[mcp]>=1.4.0` and is in beta. Importing from it raises a `LangChainBetaWarning` once per process. The API may change.
>
> If you used MCP before v1.4.0, see [Migrate from `langchain-mcp-adapters`](https://docs.langchain.com/oss/python/migrate/langchain-mcp-adapters).

## Install

Install LangChain with the `mcp` extra, which pulls in FastMCP:

```bash pip
pip install "langchain[mcp]"
```

```bash uv
uv add "langchain[mcp]"
```

## Quickstart

Open an [`MCPAdapter`](https://reference.langchain.com/python/langchain/mcp/adapter/MCPAdapter), discover the server's tools with `list_tools()`, and build the agent inside the context. The tools hold the client, so the agent stays usable after the context exits:

```python
from langchain.agents import create_agent
from langchain.mcp import MCPAdapter


async def main():
    async with MCPAdapter("https://example.com/mcp") as adapter:
        tools = await adapter.list_tools()
        agent = create_agent("claude-sonnet-5", tools)
        return await agent.ainvoke({"messages": [{"role": "user", "content": "..."}]})
```

> [card] [View example trace](https://smith.langchain.com/public/a94096e8-5b52-4550-89f4-d4c40cff2834/r)
>
> Open a public LangSmith run for this example.

> [accordion] LangChain docs MCP server
>
> The [LangChain docs MCP server](https://docs.langchain.com/use-these-docs.md) is a public HTTP endpoint at `https://docs.langchain.com/mcp`.
>
> Connect an agent to it to search and read documentation without writing custom tools:
>
> ```python
> from langchain.agents import create_agent
> from langchain.mcp import MCPAdapter
>
>
> async def main():
>     async with MCPAdapter("https://docs.langchain.com/mcp") as adapter:  # [!code highlight]
>         tools = await adapter.list_tools()
>         agent = create_agent("claude-sonnet-5", tools)
>         return await agent.ainvoke(
>             {
>                 "messages": [
>                     {
>                         "role": "user",
>                         "content": "How do I add short-term memory to a LangChain agent?",
>                     }
>                 ]
>             }
>         )
> ```
>
> > [!NOTE]
> >
> > The docs MCP server is public and does not require an API key. For IDE and coding-agent setup (Claude Code, Cursor, and others), see [Use docs programmatically](https://docs.langchain.com/use-these-docs.md).
>
> The server exposes these tools:
>
> | Tool | Description |
> | - | - |
> | `search_docs_by_lang_chain` | Search docs for relevant guides, how-tos, and examples. |
> | `query_docs_filesystem_docs_by_lang_chain` | Read or search docs through a virtual filesystem (`rg`, `head`, `cat`, and related commands). |
> | `submit_feedback` | Report a problem with a documentation page. |

## Transports

[`MCPAdapter`](https://reference.langchain.com/python/langchain/mcp/adapter/MCPAdapter) infers the transport from the target you provide. The target is the only difference between an in-process server, a local script over stdio, and a remote URL:

```python
from pathlib import Path

from langchain.mcp import MCPAdapter

# An in-process FastMCP server: no subprocess, no socket. Ideal for tests.
in_memory = MCPAdapter(server)  # a FastMCP instance

# A script path is launched over stdio, one subprocess per adapter.
stdio = MCPAdapter(Path("weather_server.py"))

# A string must be an http(s) URL, reached over streamable HTTP.
http = MCPAdapter("https://example.com/mcp")
```

A target can be any of the following:

* **An `http`/`https` URL** (`str`): reached over Streamable HTTP.
* **A script path** (`Path`): launched as a subprocess over stdio.
* **A transport object** (`StreamableTransport`): a preconfigured transport object. See [Client Transports](https://gofastmcp.com/clients/transports).
* **An in-process `FastMCP` server**: connected in memory, without a subprocess or socket.
* **An `MCPConfig` dict** (`{"mcpServers": {...}}`): several servers behind one adapter. See [Connections](Connections.md#multiple-servers).
* **A prebuilt `fastmcp.Client`**: for full control over transport, [caching](https://gofastmcp.com/clients/client#response-caching), and [protocol negotiation](https://gofastmcp.com/clients/client#protocol-negotiation).

> [!WARNING]
>
> A `str` target must be an `http` or `https` URL. FastMCP resolves a string by testing it as a filesystem path before testing it as a URL, so a string naming an existing `.py` or `.js` file would launch that file as a subprocess. Because strings are the form a target most often arrives in from configuration or from a model, [`MCPAdapter`](https://reference.langchain.com/python/langchain/mcp/adapter/MCPAdapter) rejects strings that do not match the shape of a URL.

## Next steps

> [card] [Tools](Tools.md)
>
> Load MCP tools into agents, control their execution, and handle their outputs.

> [card] [Connections](Connections.md)
>
> Connection lifecycle, multiple servers, protocol eras, and caching.

> [card] [Authentication](Authentication.md)
>
> Bearer tokens, OAuth 2.1, and per-user server auth.

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/mcp/index.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

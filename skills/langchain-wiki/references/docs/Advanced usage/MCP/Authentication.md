# Authentication

> Authenticate MCP connections with bearer tokens, OAuth 2.1, or per-user credentials in LangChain.

Most remote MCP servers require authentication. [`MCPAdapter`](https://reference.langchain.com/python/langchain/mcp/adapter/MCPAdapter) delegates auth to FastMCP, so any credential a `fastmcp.Client` accepts works: a static [bearer token](#bearer-token), a full [OAuth 2.1](#oauth-authentication) flow, or any [`httpx.Auth`](https://www.python-httpx.org/advanced/authentication/). Pass the credential on a prebuilt client and hand that client to the adapter. When one agent talks to several servers, use [per-server authentication](#per-server-authentication); in a deployment, use [per-user authentication](#per-user-authentication) so each run reaches the server as the caller.

> [!NOTE]
>
> The `langchain.mcp` namespace requires `langchain[mcp]>=1.4.0` and is in beta. The API may change.

## Bearer token

The simplest case: the server verifies a token you provisioned and adds it in the `Authorization: Bearer <token>` header. There is no discovery, browser, or refresh. Pass the token as the client's `auth`:

```python
from fastmcp.client import Client
from langchain.mcp import MCPAdapter


async def load_tools_with_bearer(url: str, token: str) -> list:
    # `auth` accepts a bearer-token string, the literal "oauth" (full OAuth 2.1
    # with dynamic client registration), or any `httpx.Auth`.
    async with MCPAdapter(Client(url, auth=token)) as adapter:
        return await adapter.list_tools()
```

The `auth` argument accepts a bearer-token string, the literal `"oauth"`, or any `httpx.Auth`. In an `MCPConfig` fleet, each server takes the same key.

## OAuth authentication

For a server that issues its own credentials, pass the literal string `"oauth"`. FastMCP runs the full OAuth 2.1 flow: discovery, [dynamic client registration](https://modelcontextprotocol.io/specification/draft/basic/authorization), the browser redirect, and the token exchange. Dynamic client registration means the client registers itself at runtime instead of you pre-provisioning a client ID:

```python
async def load_tools_with_oauth(url: str) -> list:
    # "oauth" runs discovery, dynamic client registration, the browser redirect,
    # and the token exchange. Pass `OAuth(..., token_storage=...)` to persist
    # tokens across runs instead of repeating the browser step each time.
    async with MCPAdapter(Client(url, auth="oauth")) as adapter:
        return await adapter.list_tools()
```

By default tokens are held in memory, so each run repeats the browser step. Pass a prebuilt `OAuth` provider with a token store to persist them across runs:

```python
from fastmcp.client import Client
from fastmcp.client.auth import OAuth

oauth = OAuth(mcp_url="https://example.com/mcp", token_storage=...)
client = Client("https://example.com/mcp", auth=oauth)
```

FastMCP ships providers for common identity providers (Auth0, WorkOS, Okta, and more); the flow the client runs is identical across them. See [OAuth authentication](https://gofastmcp.com/clients/auth/oauth) in the FastMCP documentation.

## Per-server authentication

When one agent talks to several servers, each server may need its own credential. Give each its own connection with a [`ClientGroup`](Connections.md#independent-connections-with-clientgroup), and set `auth` per client, so every server authenticates independently:

```python
from fastmcp.client.group import ClientGroup


async def load_with_per_server_auth(
    billing_url: str, docs_token: str, docs_url: str
) -> list:
    # Each server carries its own credential. A `ClientGroup` keeps one
    # connection per server, so each authenticates independently.
    group = ClientGroup(
        {
            "billing": Client(billing_url, auth="oauth"),
            "docs": Client(docs_url, auth=docs_token),
        }
    )
    async with MCPAdapter(group) as adapter:
        return await adapter.list_tools()
```

## Per-user authentication

In a deployment, each run should reach the MCP server as the user who initiated it, not with one shared credential. The pattern has two halves:

1. **Authenticate the caller at LangSmith Agent Server.** A [custom auth handler](https://docs.langchain.com/langsmith/auth.md) resolves the incoming request to a user identity, which each run reads off its runtime.
2. **Mint or exchange a credential for that user.** Inside the [graph factory](Connections.md#scale-a-deployment), read the user's identity and build the MCP client with a per-user token, so the connection carries that user's authorization.

```python
from fastmcp.client import Client
from fastmcp.client.auth import BearerAuth

CONFIG = {
    "mcpServers": {
        "docs": { "url": "https://example.com/mcp" }
    }
}

async def make_graph(runtime):
    user = runtime.user.identity if runtime.user is not None else "anonymous"
    auth = BearerAuth(token_for(user))  # exchange for a per-user token
    async with MCPAdapter(Client(CONFIG, auth=auth)) as adapter:
        tools = await adapter.list_tools()
        return create_agent("claude-sonnet-5", tools)
```

In production, `token_for` stands in for whatever the deployment already has: an OAuth gateway that exchanges the session for a per-user token, or a `fastmcp.client.auth` provider that runs the authorization-code flow per identity. Isolate any [cached responses](Connections.md#caching) per user, keyed off the verified identity, so one user never sees another's cached tool list.

## See also

* [FastMCP OAuth authentication](https://gofastmcp.com/clients/auth/oauth)
* [FastMCP bearer token authentication](https://gofastmcp.com/clients/auth/bearer)
* [FastMCP machine-to-machine authentication](https://gofastmcp.com/clients/auth/client-credentials)
* [FastMCP client groups](https://gofastmcp.com/clients/client-groups) — independent connections for per-server auth
* [FastMCP server authentication providers](https://gofastmcp.com/servers/auth/authentication)
* [MCP authorization specification](https://modelcontextprotocol.io/specification/draft/basic/authorization)
* [Custom authentication for Agent Server](https://docs.langchain.com/langsmith/auth.md)

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/mcp/auth.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

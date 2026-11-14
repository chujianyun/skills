# LangSmith Tool Server

The LangSmith Tool Server is a standalone MCP framework for building and deploying tools with built-in authentication and authorization. Use the Tool Server when you want to:

* [Create custom tools](#create-a-custom-toolkit) that integrate with LangSmith's [Agent Auth](../../../Deploy/Agent%20Server/Auth%20%26%20access%20control/Set%20up%20Agent%20Auth.md) for OAuth authentication
* [Build an MCP gateway](#use-as-an-mcp-gateway) for agents you're building yourself (outside of Fleet)

> [!NOTE]
>
> If you're using [Fleet](../No-code%20agents%20with%20LangSmith%20Fleet.md), you don't need to interact with the Tool Server directly. Fleet provides [built-in tools](../Tools%20and%20automation/Tool%20integrations.md) and supports [remote MCP servers](../Tools%20and%20automation/Remote%20MCP%20servers.md) without requiring Tool Server setup.
>
> However, you can configure the associated tool server instance as an MCP server, which will allow you to use your custom MCP servers in your agent.

Download the [PyPI package](https://pypi.org/project/langsmith-tool-server/) to get started.

## Create a custom toolkit

Install the LangSmith Tool Server and LangChain CLI:

```bash
pip install langsmith-tool-server
pip install langchain-cli-v2
```

Create a new toolkit:

```bash
langchain tools new my-toolkit
cd my-toolkit
```

This creates a toolkit with the following structure:

```
my-toolkit/
├── pyproject.toml
├── toolkit.toml
└── my_toolkit/
    ├── __init__.py
    ├── auth.py
    └── tools/
        ├── __init__.py
        └── ...
```

Define your tools using the `@tool` decorator. For more on tool schemas, return values, error handling, and `ToolRuntime`, see the [Tools guide](https://docs.langchain.com/oss/python/langchain/tools.md).

```python
from langsmith_tool_server import tool

@tool
def hello(name: str) -> str:
    """Greet someone by name."""
    return f"Hello, {name}!"

@tool
def add(x: int, y: int) -> int:
    """Add two numbers."""
    return x + y

TOOLS = [hello, add]
```

Run the server:

```bash
langchain tools serve
```

Your tool server will start on `http://localhost:8000`.

## Call tools via MCP protocol

Below is an example that lists available tools and calls the `add` tool:

```python
import asyncio
import aiohttp

async def mcp_request(url: str, method: str, params: dict = None):
    async with aiohttp.ClientSession() as session:
        payload = {"jsonrpc": "2.0", "method": method, "params": params or {}, "id": 1}
        async with session.post(f"{url}/mcp", json=payload) as response:
            return await response.json()

async def main():
    url = "http://localhost:8000"

    tools = await mcp_request(url, "tools/list")
    print(f"Tools: {tools}")

    result = await mcp_request(url, "tools/call", {"name": "add", "arguments": {"a": 5, "b": 3}})
    print(f"Result: {result}")

asyncio.run(main())
```

## Use as an MCP gateway

The LangSmith Tool Server can act as an MCP gateway, aggregating tools from multiple MCP servers into a single endpoint. Configure MCP servers in your `toolkit.toml`:

```toml
[toolkit]
name = "my-toolkit"
tools = "./my_toolkit/__init__.py:TOOLS"

[[mcp_servers]]
name = "weather"
transport = "streamable_http"
url = "http://localhost:8001/mcp/"

[[mcp_servers]]
name = "math"
transport = "stdio"
command = "python"
args = ["-m", "mcp_server_math"]
```

All tools from connected MCP servers are exposed through your server's `/mcp` endpoint. MCP tools are prefixed with their server name to avoid conflicts (e.g., `weather_get_forecast`, `math_add`).

## Authenticate

### OAuth for third-party APIs

For tools that need to access third-party APIs (like Google, GitHub, Slack, etc.), you can use OAuth authentication with [Agent Auth](../../../Deploy/Agent%20Server/Auth%20%26%20access%20control/Set%20up%20Agent%20Auth.md).

Before using OAuth in your tools, you'll need to configure an OAuth provider in your LangSmith workspace settings. See the [Agent Auth documentation](../../../Deploy/Agent%20Server/Auth%20%26%20access%20control/Set%20up%20Agent%20Auth.md) for setup instructions.

Once configured, specify the `auth_provider` in your tool decorator:

```python
from langsmith_tool_server import tool, Context
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

@tool(
    auth_provider="google",
    scopes=["https://www.googleapis.com/auth/gmail.readonly"],
    integration="gmail"
)
async def read_emails(context: Context, max_results: int = 10) -> str:
    """Read recent emails from Gmail."""
    credentials = Credentials(token=context.token)
    service = build('gmail', 'v1', credentials=credentials)
    # ... Gmail API calls
    return f"Retrieved {max_results} emails"
```

Tools with `auth_provider` must:

* Have `context: Context` as the first parameter
* Specify at least one scope
* Use `context.token` to make authenticated API calls

### Custom request authentication

Custom authentication allows you to validate requests and integrate with your identity provider. Define an authentication handler in your `auth.py` file:

```python
from langsmith_tool_server import Auth

auth = Auth()

@auth.authenticate
async def authenticate(authorization: str = None) -> dict:
    """Validate requests and return user identity."""
    if not authorization or not authorization.startswith("Bearer "):
        raise auth.exceptions.HTTPException(
            status_code=401,
            detail="Unauthorized"
        )

    token = authorization.replace("Bearer ", "")
    # Validate token with your identity provider
    user = await verify_token_with_idp(token)

    return {"identity": user.id}
```

The handler runs on every request and must return a dict with `identity` (and optionally `permissions`).

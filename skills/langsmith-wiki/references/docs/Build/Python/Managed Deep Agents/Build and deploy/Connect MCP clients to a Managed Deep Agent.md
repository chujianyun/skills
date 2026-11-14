# Connect MCP clients to a Managed Deep Agent

> Expose a deployed Managed Deep Agent as a tool to MCP clients such as Claude Code.

Managed Deep Agents deployments run on [LangSmith Agent Server](../../../../Deploy/Agent%20Server/Agent%20Server.md), so every deployment serves the Agent Server [Model Context Protocol](https://modelcontextprotocol.io/introduction) (MCP) endpoint at `/mcp`. Any MCP client that supports the Streamable HTTP transport can call the deployed agent as a tool, so another assistant or agent can delegate work to it without calling the deployment API directly.

This page covers how to find the Managed Deep Agents URL and authenticate. For protocol behavior and generic Agent Server client setup, see [MCP endpoint in Agent Server](../../../../Deploy/Agent%20Server/Capabilities/MCP%20endpoint%20in%20Agent%20Server.md).

> [!NOTE]
>
> Managed Deep Agents is in **public [beta](../../../../LangSmith%20setup/Cloud/Reference/Release%20stages.md)** on [LangSmith Cloud](../../../../LangSmith%20setup/Cloud/Cloud%20%28SaaS%29.md) and [Bring Your Own Cloud (BYOC)](../../../../LangSmith%20setup/BYOC/Bring%20Your%20Own%20Cloud%20%28BYOC%29.md). Use Managed Deep Agents CLI and SDK v0.10 or later for BYOC.

The endpoint is the outbound direction. An [MCP connector](../Agent%20capabilities/Connect%20to%20MCP%20servers.md) points the other way: it adds tools from a remote MCP server to your agent. A deployment can use both.

## Find the endpoint URL

The endpoint is `/mcp` on the deployment's API URL:

```text
<DEPLOYMENT_API_URL>/mcp
```

`mda deploy` prints the LangSmith deployment dashboard URL, not the API URL. Open that dashboard, copy the **API URL** from the deployment details view, then append `/mcp`.

The local server started by [`mda dev`](Develop%20locally%20with%20LangSmith%20Studio.md) serves the same endpoint. Append `/mcp` to the local server URL the CLI prints.

## Authenticate requests

The MCP endpoint uses the deployment's [identity](../Agent%20capabilities/Add%20identity%20to%20Managed%20Deep%20Agents.md) configuration, the same as every other route on the deployment. Send the credential that matches the configured mode:

| Identity mode | Header |
| - | - |
| LangSmith API key (default) | `x-api-key: <LANGSMITH_API_KEY>` |
| Supabase | `Authorization: Bearer <access_token>` |

For the LangSmith API-key default, the key must belong to the workspace that owns the deployment. A key that is valid for another workspace is rejected.

Authentication failures return one of three responses:

| Status | Body | Cause |
| - | - | - |
| 401 | `{"detail":"missing x-api-key"}` | No credential header on the request. |
| 403 | `{"detail":"API key is forbidden"}` | The key is invalid, revoked, or expired. |
| 403 | `{"detail":"API key tenant mismatch"}` | The key is valid, but belongs to a different workspace than the deployment. |

The local server started by `mda dev` requires no credential. It grants every caller an unscoped local service principal, so any client on the machine can call `/mcp` and every other route. Only a deployment enforces the header.

> [!WARNING]
>
> Anyone holding the LangSmith API key can reach the deployment, and an MCP client stores the header in its own configuration. Treat a key added to a client config as a shared secret for the whole workspace.

> [!NOTE]
>
> Supabase identity expects an access token that a person obtains by signing in to your app. An MCP client that stores only static headers cannot mint one, so use the LangSmith API-key default for deployments that MCP clients call.

## Understand what the agent exposes

The Agent Server exposes the agent as an MCP tool:

* **Tool name**: The agent `name` set in the [agent definition](../Agent%20capabilities/Define%20a%20Managed%20Deep%20Agent.md#parameters).
* **Tool input schema**: The agent's input schema.

For transport details and other Agent Server MCP behavior, see [MCP endpoint in Agent Server](../../../../Deploy/Agent%20Server/Capabilities/MCP%20endpoint%20in%20Agent%20Server.md).

## Add the agent to Claude Code

Register the endpoint as an HTTP MCP server:

```bash
claude mcp add --transport http research-assistant \
  <DEPLOYMENT_API_URL>/mcp \
  --header "x-api-key: $LANGSMITH_API_KEY"
```

Claude Code lists the agent as a tool once the server connects.

In a JSON configuration, Claude Code expands `${VAR}` in header values, so the key stays in the environment instead of the config file:

```json
"headers": { "x-api-key": "${LANGSMITH_API_KEY}" }
```

## Add the agent to another MCP client

Clients that read an `mcpServers` configuration accept the endpoint and header directly:

```json
{
  "mcpServers": {
    "research-assistant": {
      "type": "http",
      "url": "<DEPLOYMENT_API_URL>/mcp",
      "headers": {
        "x-api-key": "<LANGSMITH_API_KEY>"
      }
    }
  }
}
```

A client that accepts only a URL and negotiates OAuth cannot authenticate to the endpoint, which requires a header credential. Configure the header explicitly. Without one, a client may fall back to OAuth and report a Dynamic Client Registration failure rather than the missing header, which obscures the real cause.

## Call the endpoint from code

Load the agent's tool through an MCP client library, then pass the tools to a model or another agent:

```python
import os

from fastmcp.client import Client
from fastmcp.client.transports import StreamableHttpTransport
from langchain.mcp import MCPAdapter

async with MCPAdapter(
    Client(
        StreamableHttpTransport(
            "<DEPLOYMENT_API_URL>/mcp",
            headers={"x-api-key": os.environ["LANGSMITH_API_KEY"]},
        )
    )
) as adapter:
    tools = await adapter.list_tools()
```

Read credentials from the environment. Do not hard-code them in client code.

## Understand session behavior

Agent Server MCP requests do not use [sessions](../../../../Deploy/Agent%20Server/Capabilities/MCP%20endpoint%20in%20Agent%20Server.md#session-behavior): separate tool calls do not share thread state. A tool call that pauses for input keeps its own state until the client answers. For more information, see [Human-in-the-loop over MCP](../../../../Deploy/Agent%20Server/Capabilities/Human-in-the-loop%20over%20MCP.md).

To retain knowledge across calls, [opt in to durable memory](../Agent%20capabilities/Add%20memory%20to%20Managed%20Deep%20Agents.md). Durable memory is optional and shared by every caller of the deployment. Do not enable it when MCP clients should not influence one another.

## When to use the MCP endpoint

| Concept | Kind | How it reaches the agent |
| - | - | - |
| **MCP endpoint** | Deployment API | Exposes the agent as a tool to MCP clients |
| **[MCP connectors](../Agent%20capabilities/Connect%20to%20MCP%20servers.md)** | Managed configuration | Add tools hosted by remote MCP servers to the agent |
| **[Channels](../Agent%20capabilities/Channels/Connect%20Managed%20Deep%20Agents%20to%20channels.md)** | Managed configuration | Receive messages from an external messaging service that start agent runs and deliver responses |

## Next steps

> [card] [Agent Server](../../../../Deploy/Agent%20Server/Agent%20Server.md)
>
> Explore the runtime that hosts every Managed Deep Agents deployment.

> [card] [Agent Server MCP](../../../../Deploy/Agent%20Server/Capabilities/MCP%20endpoint%20in%20Agent%20Server.md)
>
> Read the Agent Server MCP protocol reference.

> [card] [MCP connectors](../Agent%20capabilities/Connect%20to%20MCP%20servers.md)
>
> Add tools from remote MCP servers to the agent.

> [card] [Identity](../Agent%20capabilities/Add%20identity%20to%20Managed%20Deep%20Agents.md)
>
> Authenticate callers to the deployment.

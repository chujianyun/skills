# Connect to MCP servers

> Add tools from remote MCP servers to a managed deep agent.

Connect a managed deep agent to remote [Model Context Protocol (MCP)](https://docs.langchain.com/oss/javascript/deepagents/mcp.md) servers to add their tools to the agent. Managed Deep Agents creates the MCP client and loads the tools.

Most remote MCP servers require authentication. A [connection](Manage%20connections.md) supplies it, and declaring the connection as user-owned makes each caller authorize their own account.

> [!NOTE]
>
> Managed Deep Agents is in **public [beta](../../../../LangSmith%20setup/Cloud/Reference/Release%20stages.md)** on [LangSmith Cloud](../../../../LangSmith%20setup/Cloud/Cloud%20%28SaaS%29.md) and [Bring Your Own Cloud (BYOC)](../../../../LangSmith%20setup/BYOC/Bring%20Your%20Own%20Cloud%20%28BYOC%29.md). Use Managed Deep Agents CLI and SDK v0.10 or later for BYOC.

Declare MCP servers in `tools/mcp.ts`:

```text
my-agent/
  agent.ts
  tools/
    mcp.ts
```

For the full project layout, see [Project structure](../Get%20started/Managed%20Deep%20Agents%20project%20structure.md).

To implement application logic in the project instead, use an [authored tool](Add%20custom%20tools%20to%20Managed%20Deep%20Agents.md).

## Add MCP servers

Use an MCP server when tools already live on a remote MCP server and you want MDA to load them without importing them into the agent definition.

**1. Declare the servers**

Use `defineMcp` to declare one or more remote servers:

```ts tools/mcp.ts
import { defineMcp } from "managed-deepagents";

export const mcp = defineMcp({
  servers: {
    langchainDocs: {
      transport: "http",
      url: "https://docs.langchain.com/mcp",
    },
  },
});
```

The module must export a named `mcp`. A project has one MCP declaration, so declare every server in it. The file name also accepts the `.tsx`, `.mts`, or `.cts` variants.

Managed Deep Agents supports Streamable HTTP (`"http"`) and legacy SSE (`"sse"`) transports. Stdio MCP servers are not supported. Expose a stdio server over HTTP or implement its operation as an [authored tool](Add%20custom%20tools%20to%20Managed%20Deep%20Agents.md) instead.

For connection options, see [Manage connections](Manage%20connections.md).

**2. Select tools (Optional)**

By default, Managed Deep Agents exposes every tool from each server. To expose only selected tools, set an allowlist inside that server's configuration:

```ts
{
  transport: "http",
  url: "https://docs.langchain.com/mcp",
  includeTools: ["search_docs_by_lang_chain"],
}
```

To expose every tool except selected tools, replace `includeTools` with `excludeTools`.

You can use both options together. The denylist applies after the allowlist, and the same tool cannot appear in both lists.

Selection uses raw MCP tool names before Managed Deep Agents prefixes them. Tool names are prefixed with the server name by default to avoid collisions. For example, the `search_docs_by_lang_chain` tool from the `langchainDocs` server is exposed as `langchainDocs__search_docs_by_lang_chain`.

**3. Pass credentials (Optional)**

If an MCP server requires credentials, declare a connection on the server config and create that connection in the workspace.

* **MCP OAuth**: For servers that advertise OAuth and support automatic client registration, create with `mda connections create <slug>` (inferred from the MCP declaration) or `mda connections create <slug> --mcp <url>`. You do not supply a client ID or secret.
* **Opaque secret or general OAuth**: For a static API key, or for a BYOT OAuth app you register yourself, create an opaque secret or general OAuth connection, then set the server's `connection` option to `connections.get(...)`.

For create modes, owners, and runtime authorization, see [Manage connections](Manage%20connections.md).

## Configure MCP servers

Each server supports the following core options:

| Option | Description |
| - | - |
| `transport` | Required. Use `http` for Streamable HTTP or `sse` for legacy SSE. |
| `url` | Required. The remote MCP endpoint URL. |
| `headers` | Static headers to send to the server. |
| `include_tools` / `includeTools` | Raw MCP tool names to expose. |
| `exclude_tools` / `excludeTools` | Raw MCP tool names to hide. |
| `default_tool_timeout` / `defaultToolTimeout` | Timeout for each tool call, in seconds for Python and milliseconds for TypeScript. |
| `automatic_sse_fallback` / `automaticSSEFallback` | For HTTP, allow the client to fall back to SSE. |
| `reconnect` | For SSE, configure reconnection behavior. |

The MCP definition also accepts these options:

| Option | Default | Description |
| - | - | - |
| `prefixToolNameWithServerName` | `true` | Prefix each tool with `{server}__`. |
| `throwOnLoadError` | `true` | Fail loading instead of starting with a partial tool set. |
| `jitAuth` | `false` | For LangSmith managed-tools URLs only. When `true`, the model also gets tools for providers the caller has not connected. The first call to one of those tools asks the user to connect. When `false`, the run asks for every missing connection before it starts. Requires `managed-deepagents` 0.10.2 or later. |

## Deployment

`mda dev` and `mda deploy` discover the MCP declaration under `tools/` and include it in the managed configuration. The declaration is not synced to Context Hub.

## When to use MCP connectors

| Concept | Kind | How it reaches the agent |
| - | - | - |
| **MCP servers** | Managed configuration | Declared in the MCP module under `tools/`; no import into the agent entry |
| **[MCP endpoint](../Build%20and%20deploy/Connect%20MCP%20clients%20to%20a%20Managed%20Deep%20Agent.md)** | Deployment API | Exposes the agent as a tool to MCP clients |
| **[Authored tools](Add%20custom%20tools%20to%20Managed%20Deep%20Agents.md)** | Application code | Import and pass in the agent definition |
| **[Channels](Channels/Connect%20Managed%20Deep%20Agents%20to%20channels.md)** | Managed configuration | Receive external messages that start agent runs and deliver responses |

For more information, see [Project structure](../Get%20started/Managed%20Deep%20Agents%20project%20structure.md).

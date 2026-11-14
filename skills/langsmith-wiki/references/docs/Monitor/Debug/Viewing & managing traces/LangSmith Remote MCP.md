# LangSmith Remote MCP

> Connect MCP-compatible clients to LangSmith over OAuth, or authenticate programmatic clients with a LangSmith API key.

The LangSmith Remote MCP is a [Model Context Protocol](https://modelcontextprotocol.io/introduction) (MCP) server hosted by LangSmith. It exposes the same tools as the [standalone LangSmith MCP Server](LangSmith%20MCP%20Server.md) (conversation history, prompts, runs and traces, datasets, experiments, billing) without a separate deployment. Interactive MCP clients connect over OAuth with no API key or header configuration; programmatic clients can authenticate with a LangSmith API key via the `X-Api-Key` header.

## Endpoints

Point your MCP client at the Remote MCP endpoint for where your LangSmith runs: one URL per region on LangSmith Cloud, or a path on your own host for BYOC and self-hosted LangSmith.

### LangSmith Cloud

<table>
  <thead>
    <tr>
      <th>Region</th>

      <th>
        URL
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>GCP US</td>

      <td>
        `https://api.smith.langchain.com/mcp`
      </td>
    </tr>

    <tr>
      <td>GCP EU</td>

      <td>
        `https://eu.api.smith.langchain.com/mcp`
      </td>
    </tr>

    <tr>
      <td>GCP APAC</td>

      <td>
        `https://apac.api.smith.langchain.com/mcp`
      </td>
    </tr>

    <tr>
      <td>AWS US</td>

      <td>
        `https://aws.api.smith.langchain.com/mcp`
      </td>
    </tr>

    <tr><td>Azure US</td>
    <td>`https://azure.api.smith.langchain.com/mcp`</td></tr>
  </tbody>
</table>

The server discovers the rest of its OAuth metadata via [RFC 8414](https://datatracker.ietf.org/doc/html/rfc8414) at `/.well-known/oauth-authorization-server` on the same host, so a compliant MCP client only needs the URL above.

### BYOC

`https://<data_plane_url>/api/mcp`, where `<data_plane_url>` is the URL of your [BYOC](../../../LangSmith%20setup/BYOC/Bring%20Your%20Own%20Cloud%20%28BYOC%29.md) data plane.

### Self-hosted

`https://<your-langsmith-host>/api/mcp`, where `<your-langsmith-host>` is the hostname of your LangSmith instance. Requires LangSmith v0.16 or later and a signing JWKS. To turn it on, see [Enabling Remote MCP](#enabling-remote-mcp). Self-hosted deployments on earlier versions should continue to use the [standalone LangSmith MCP Server](LangSmith%20MCP%20Server.md).

## Authentication

The Remote MCP supports two authentication methods. Use **OAuth** for interactive MCP clients (Claude Code, Cursor, and similar), and an **API key** for programmatic or headless clients that can't complete a browser-based login.

### OAuth

OAuth 2.1 with [Dynamic Client Registration (RFC 7591)](https://datatracker.ietf.org/doc/html/rfc7591) is the default for interactive clients. Compatible MCP clients register themselves automatically on first use—there is no client ID to provision and no API key to manage.

After registration:

1. The client opens an authorization URL in your browser.
2. You log in to LangSmith (or use an existing session) and consent.
3. The client receives an access token and refresh token.
4. The access token is automatically refreshed by the client when it expires.

The session is scoped to your LangSmith user and workspace permissions—calls through the MCP server can only view what your account is permitted to view.

### API key

Send a [LangSmith API key](../../../LangSmith%20setup/Account/Create%20an%20account%20and%20API%20key.md) in the `X-Api-Key` header on every request. This suits backend services, scripts, and SDKs, for example, the [AI SDK](#ai-sdk), where the interactive OAuth flow is not practical.

Requests are authorized as the user that owns the API key, scoped to that key's workspace and permissions—the same authorization the key has elsewhere in the LangSmith API. Tools that accept a `workspace_id` argument can target a specific workspace; otherwise the key's own workspace is used.

> [!WARNING]
>
> On [BYOC](../../../LangSmith%20setup/BYOC/Bring%20Your%20Own%20Cloud%20%28BYOC%29.md), the API key must be assigned to your LangSmith workspace.

> [!NOTE]
>
> The `X-Api-Key` header is specific to the Remote MCP. The [standalone LangSmith MCP Server](LangSmith%20MCP%20Server.md) uses a different header, `LANGSMITH-API-KEY`.

## Quickstart

### Claude Code

Add the server to your project's `.mcp.json` (or run `claude mcp add --transport http -s user langsmith https://api.smith.langchain.com/mcp` to install it user-wide):

```json
{
  "mcpServers": {
    "langsmith": {
      "type": "http",
      "url": "https://api.smith.langchain.com/mcp"
    }
  }
}
```

Then run `/mcp` and select **langsmith** to complete the OAuth flow. Tools become available as `mcp__langsmith__<tool_name>`.

### Deep Agents Code (`dcode`)

Add the server to your user-level `~/.deepagents/.mcp.json` file to make it available in every Deep Agents Code project, or add it to a project-level `.mcp.json` file for only that project. See the [Deep Agents Code MCP tools docs](https://docs.langchain.com/oss/deepagents/code/mcp-tools.md) for discovery locations and precedence rules.

```json
{
  "mcpServers": {
    "langsmith": {
      "url": "https://api.smith.langchain.com/mcp",
      "transport": "http",
      "auth": "oauth"
    }
  }
}
```

Then complete the OAuth login flow in one of two ways:

* In the Deep Agents Code TUI, run `/mcp`, select **langsmith**, and follow the login prompt.
* From your shell, run:

  ```bash
  dcode mcp login langsmith
  ```

Launch `dcode`, or restart an active session, to load the LangSmith MCP tools. In an interactive session, run `/mcp` to inspect server status and loaded tools.

### Cursor

Add to your Cursor `mcp.json`:

```json
{
  "mcpServers": {
    "LangSmith": {
      "url": "https://api.smith.langchain.com/mcp"
    }
  }
}
```

Cursor will prompt you to complete the OAuth flow on first use.

### LangSmith CLI

The [LangSmith CLI](../../../LangSmith%20setup/Govern/Tools/LangSmith%20CLI.md) authenticates against this same OAuth server, so `langsmith auth login` logs you in via the OAuth device flow—no API key required:

```bash
# LangSmith Cloud
langsmith auth login

# Self-hosted (point at your instance's /api base)
langsmith auth login --api-url https://<your-langsmith-host>/api
```

The CLI prints an activation URL; open it, approve, and the CLI completes login and stores the token per profile in `~/.langsmith/config.json`. It then works against the same projects, traces, runs, datasets, experiments, and threads as the Remote MCP server.

### AI SDK

For programmatic use from the [AI SDK](https://ai-sdk.dev/), authenticate with an API key via the `X-Api-Key` header and the built-in `http` (Streamable HTTP) transport:

```ts
import { createMCPClient } from "@ai-sdk/mcp";

const client = await createMCPClient({
  transport: {
    type: "http",
    url: "https://api.smith.langchain.com/mcp",
    headers: { "X-Api-Key": process.env.LANGSMITH_API_KEY! },
  },
});

const tools = await client.tools();
```

Pass `tools` directly to `streamText` or `generateText`. The Remote MCP is stateless and responds with JSON over the standard Streamable HTTP transport, so the built-in transport works as-is—you don't need a custom transport.

### Other clients

Any MCP client supporting the [Streamable HTTP transport](https://spec.modelcontextprotocol.io/specification/2025-03-26/basic/transports/#streamable-http) can connect with just the URL above—using OAuth 2.1 with dynamic client registration, or a LangSmith API key in the `X-Api-Key` header.

## Known client incompatibilities

> [!NOTE]
>
> **OpenAI Codex CLI** does not work with the LangSmith Remote MCP. Codex omits the [RFC 8707](https://datatracker.ietf.org/doc/html/rfc8707) `resource` parameter required by the [MCP authorization spec](https://modelcontextprotocol.io/specification/draft/basic/authorization) during the OAuth flow, so login appears to succeed but the issued token is not bound to the LangSmith MCP and `initialize` fails with an auth-required error. Two upstream issues affect token exchange and authorize requests in Codex (refer to [openai/codex#20729](https://github.com/openai/codex/issues/20729) and [openai/codex#13891](https://github.com/openai/codex/issues/13891)). In the meantime, use the [LangSmith CLI](../../../LangSmith%20setup/Govern/Tools/LangSmith%20CLI.md) from Codex. The LangSmith CLI supports the same projects, traces, runs, datasets, experiments, and threads as the MCP server, with native OAuth login.

## Available tools

The Remote MCP exposes the same tool surface as the [standalone server](LangSmith%20MCP%20Server.md#available-tools):

* **Conversation and threads:** `get_thread_history`
* **Prompt management:** `list_prompts`, `get_prompt_by_name`, `push_prompt`
* **Traces and runs:** `fetch_runs`, `list_projects`
* **Datasets and examples:** `list_datasets`, `list_examples`, `read_dataset`, `read_example`, `create_dataset`, `update_examples`
* **Experiments and evaluations:** `list_experiments`, `run_experiment`
* **Billing:** `get_billing_usage`

See the [standalone server reference](LangSmith%20MCP%20Server.md#available-tools) for parameter and pagination details—both servers share the same tool implementations.

## Re-authenticating

If a client loses its session (for example, after revoking access in your LangSmith account, or if the refresh token is invalidated), trigger re-auth from the client:

* **Claude Code:** run `/mcp`, select **langsmith**, choose re-authenticate.
* **Cursor:** disable and re-enable the server in MCP settings.
* **Other clients:** consult the client's MCP settings UI.

## Self-hosted LangSmith

[Self-hosted LangSmith](../../../LangSmith%20setup/Self-hosted/Self-hosted%20LangSmith.md) deployments on v0.16 or later expose the Remote MCP at `https://<your-langsmith-host>/api/mcp`. Once enabled, authentication and the tool surface are identical to LangSmith Cloud.

### Enabling Remote MCP

The Remote MCP and its OAuth Authorization Server are wired automatically when `config.hostname` is set, but they stay **inert (404)** until you provide a signing JWKS. Follow [Configure a signing JWKS](../../../LangSmith%20setup/Self-hosted/Install%20an%20instance/Self-host%20LangSmith%20on%20Kubernetes.md#configure-a-signing-jwks), then set the installation hostname in your LangSmith `values.yaml`:

```yaml
config:
  hostname: "your-langsmith-host"
```

After upgrading, the OAuth discovery endpoints and `/api/mcp` become live. Verify with:

```bash
curl https://<your-langsmith-host>/api/.well-known/oauth-protected-resource/mcp
```

For deployments on earlier versions, run the [standalone LangSmith MCP Server](LangSmith%20MCP%20Server.md) in your own environment and point its `LANGSMITH_ENDPOINT` at your self-hosted instance.

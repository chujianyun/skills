# Web search

> Add web search powered by Parallel to Managed Deep Agents without a separate account or API key.

[Managed Deep Agents](../../Deep%20Agents/Deployment/Managed%20Deep%20Agents.md) includes built-in web search powered by [Parallel](https://parallel.ai). Give your agent access to current information from the web to help answer questions.

LangSmith manages the search infrastructure, so you can add search without hosting a service or creating a separate Parallel account or API key. The integration offers zero data retention.

> [!NOTE]
>
> Built-in search is available only on LangSmith Plus and Startup plans. Usage is free during private beta.
>
> Built-in search runs on LangSmith managed tools, which are available in GCP US only. [BYOC](../../../../LangSmith%20setup/BYOC/Bring%20Your%20Own%20Cloud%20%28BYOC%29.md) data planes cannot use it.

## Before you begin

You need an existing [Managed Deep Agents project](../Get%20started/Managed%20Deep%20Agents%20quickstart.md), your LangSmith workspace ID, and a personal LangSmith API key for use in Studio.

## Add Parallel search

To add Parallel search to your agent:

### Step 1. Set your workspace ID

In your project's `.env` file, set your LangSmith workspace ID:

```shell .env
LANGSMITH_WORKSPACE_ID=YOUR_WORKSPACE_ID
```

### Step 2. Set your LangSmith API key

In the same `.env` file, set a personal LangSmith API key for use in Studio:

```shell .env
LANGSMITH_API_KEY=YOUR_LANGSMITH_API_KEY
```

You do not need a Parallel API key.

### Step 3. Configure the search server

If the file already defines `mcp`, add `Parallel` to the existing `servers` map. Define `mcp` only once.

> [tab] Python
>
> Add `Parallel` to the `servers` map in `tools/mcp.py`.
>
> ```python tools/mcp.py theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from managed_deepagents import define_mcp
>
> mcp = define_mcp(
>     servers={
>         "Parallel": {
>             "transport": "http",
>             "url": "https://api.smith.langchain.com/v1/managed-tools/servers/parallel/mcp",
>         },
>     },
> )
> ```

> [tab] TypeScript
>
> Add `Parallel` to the `servers` map in `tools/mcp.ts`.
>
> ```typescript tools/mcp.ts theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { defineMcp } from "managed-deepagents";
>
> export const mcp = defineMcp({
>   servers: {
>     "Parallel": {
>       transport: "http",
>       url: "https://api.smith.langchain.com/v1/managed-tools/servers/parallel/mcp",
>     },
>   },
> });
> ```

Your agent can now use Parallel search alongside its other tools.

## Terms of use

Your use of this integration must comply with Parallel's terms of service, including its restrictions on prohibited or abusive use.

## See also

* [Connect to MCP servers](Connect%20to%20MCP%20servers.md)
* [Add custom tools](Add%20custom%20tools%20to%20Managed%20Deep%20Agents.md)

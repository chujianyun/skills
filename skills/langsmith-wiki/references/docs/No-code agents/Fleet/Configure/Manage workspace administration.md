# Manage workspace administration

> Configure workspace-level settings for Fleet.

Configure workspace secrets and manage spend limits for Fleet agents and users.

## Workspace secrets

Fleet uses [workspace secrets](../../../LangSmith%20setup/Govern/Organization/Workspace%20setup/Set%20up%20hierarchy.md#configure-workspace-settings) to store API keys for models and tools. The following secret types are available:

* **Model provider key**: By default, Fleet uses models managed by LangChain and does not require a model-provider API key. An OpenAI or Anthropic API key is required only when you use [custom models](../Get%20started/Essentials.md#custom-models). When set, the agent graphs load this key from workspace secrets for inference.
* **Fleet-specific secrets**: Secrets prefixed with `FLEET_` are prioritized over workspace secrets within Fleet. This way, you can better track the usage of Fleet vs other parts of LangSmith that use the same secrets. If you have both `OPENAI_API_KEY` and `FLEET_OPENAI_API_KEY`, the `FLEET_OPENAI_API_KEY` secret will be used.
* **Optional tool keys**: Add keys for any tools you enable. These are read from workspace secrets at runtime.
  * `EXA_API_KEY`: Required for Exa search tools (general web and LinkedIn profile search).
  * `TAVILY_API_KEY`: Required for Tavily web search.
  * `TWITTER_API_KEY` and `TWITTER_API_KEY_SECRET`: Required for Twitter/X read operations (app-only bearer). Posting/media upload is not enabled.
* **MCP server configuration**: Fleet can pull tools from one or more remote [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) servers. Configure MCP servers and headers in your [workspace](../../../LangSmith%20setup/Govern/Organization/Overview.md#workspaces) settings. Fleet automatically discovers tools and applies the configured headers when calling them. For more information, refer to the [Remote MCP servers](../Tools%20and%20automation/Remote%20MCP%20servers.md) page.

> [!NOTE]
>
> Custom models are available for enterprise deployments. See [Custom models](../Get%20started/Essentials.md#custom-models) for more information.

### Add a secret

Adding workspace secrets requires permission to manage secrets in the workspace. If you do not have it, ask a workspace admin to add the secret for you or to grant you access.

To add a secret:

1. In the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-fleet-workspace-admin), navigate to  **Settings** > **Integrations** > **Provider secrets**.
2. Select **+ Secret**.
3. Under **Provider**, select your model provider. LangSmith names the secret with the environment variable the provider expects, such as `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`. Enter your secret in that field.

   For tool keys, `FLEET_`-prefixed secrets, or a provider that is not listed, leave **Custom** as the provider. Enter the secret name as the **Key** (for example, `TAVILY_API_KEY` or `FLEET_OPENAI_API_KEY`) and your key as the **Value**.
4. Select **Save**.

## Usage and spend limits

The **Usage** page gives workspace admins visibility into Fleet spend and the ability to set spend limits for agents and users. This page will only be visible to users with the `fleet:read-admin-config` permission.

### View current spend

The **Usage** page shows your workspace's total spend over a selected time period (**Last 7 days** or **Last 14 days**), along with total threads and total runs.

A daily spend chart provides a visual breakdown of costs over the selected period. The **Breakdown** section lets you view spend details in two ways:

* **By agent**: See each agent's total cost, number of runs, first and last used dates, owner, and weekly limit.
* **By user**: See each user's spend and activity.

### Set spend limits

Spend limits let you control how much agents and users can spend. Managing spend limits requires the `fleet:write-admin-config` permission.

#### Default weekly spend limits

In the **Default Weekly Spend Limits** section, you can configure:

* **Per-Agent Default Limit (USD)**: Set a default weekly spend limit that applies to all agents in the workspace.
* **Per-User Default Limit (USD)**: Set a default weekly spend limit that applies to all users in the workspace.

Limits are week-to-date and reset on Mondays.

#### Override limits for individual agents and users

You can override the default spend limit for individual agents or users to set a custom weekly limit.

#### Spend limit behavior

* Changes to spend limits may take a few minutes to propagate across all running agents.
* Spend limits are checked at the start of each run. If a run begins while usage is under the limit, it will be allowed to complete even if the final cost exceeds the limit.
* Spend calculations are based on traces. Deleting traces will affect reported usage and spend enforcement.

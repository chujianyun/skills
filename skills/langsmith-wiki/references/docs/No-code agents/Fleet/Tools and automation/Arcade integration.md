# Arcade integration

> Connect your workspace to Arcade to give agents access to third-party tools like GitHub, Gmail, Slack, and more.

[Arcade](https://arcade.dev) provides managed MCP gateways that give your agents access to thousands of third-party tools behind a single integration. Supported services span email, calendars, code hosting, project management, CRM, messaging, search, and more, including GitHub, Gmail, Google Drive, Slack, Notion, Jira, Salesforce, Linear, and HubSpot.

When you connect Arcade to your workspace, a workspace admin selects an Arcade organization and project, then installs MCP gateways from that project. Each user connects their own Arcade account so that tool calls authenticate with their individual credentials.

## Prerequisites

* A LangSmith workspace with **admin** permissions (to configure the integration)
* An [Arcade](https://arcade.dev) account with at least one organization and project

## Set up Arcade as a workspace admin

Only [workspace admins](../../../LangSmith%20setup/Govern/Users%20%26%20access%20control/Role-based%20access%20control.md#workspace-admin) can configure the Arcade integration, including adding or deleting MCP Gateways. Once configured, the integration is available to all users in the workspace.

**1. Open the Integrations tab**

Navigate to [**Fleet** > **Integrations**](https://smith.langchain.com/agents/tools). In the left menu under **Apps**, click **Arcade**.

**2. Connect your Arcade account**

Click **Connect** to authenticate with Arcade via OAuth. This links your Arcade account to the workspace.

**3. Select an organization and project**

Choose the Arcade **Organization** and **Project** for the workspace. All MCP gateways installed in the workspace come from this project.

**4. Install MCP gateways**

Browse the available gateways from your Arcade project and click **Add to workspace** to install them. Installed gateways appear as MCP servers available to all agents in the workspace.

## Connect as a workspace member

After an admin configures Arcade, other users must connect their own Arcade account to use the tools. Each user authenticates individually so that tool calls use their own credentials, not the admin's.

**1. Get an invitation to the Arcade project**

Ask the workspace admin to invite you to their Arcade organization and project. You must be a member of the same project to access its gateways.

**2. Connect your account**

Navigate to [**Fleet** > **Integrations**](https://smith.langchain.com/agents/tools). In the left menu under **Apps**, click **Arcade**, then click **Connect** to authenticate via OAuth.

**3. Browse available tools**

After connecting, MCP servers installed by the admin appear automatically. You can add these tools to your agents from the agent editor.

> [!NOTE]
>
> Workspace members cannot change the Arcade organization or project. Only admins can modify the workspace-level configuration.

## Use Arcade tools with an agent

After connecting, add Arcade tools to a specific agent:

1. Open your agent in [Fleet](https://smith.langchain.com/agents?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-fleet-arcade).
2. In the sidebar, expand the **Connections** drawer and click **Add connection**.
3. Select the Arcade tools you want to enable for the agent.

The agent can now call these tools at runtime. When a tool requires authorization, Arcade prompts the user to grant access via OAuth.

## Change the organization or project

Admins can update the workspace-level Arcade organization and project at any time.

> [!WARNING]
>
> Changing the organization or project **removes all installed MCP servers** from the workspace. You will need to reinstall gateways from the new project afterward.

**1. Open configuration**

Navigate to [**Fleet** > **Integrations**](https://smith.langchain.com/agents/tools). In the left menu under **Apps**, click **Arcade**. Click the settings icon to open the **Arcade Workspace Configuration** dialog.

**2. Select new organization and project**

Choose the new organization and project from the dropdowns.

**3. Confirm the change**

Click **Save Changes**. If the change removes existing MCP servers, confirm in the follow-up dialog. All previously installed gateways are removed and you can install new ones from the updated project.

## Disconnect from Arcade

Navigate to [**Fleet** > **Integrations**](https://smith.langchain.com/agents/tools). In the left menu under **Apps**, click **Arcade**, then click **Disconnect**. This revokes your OAuth token but does not affect the workspace configuration or other users.

Admins can remove the Arcade integration entirely by deleting the workspace configuration, which also removes all installed Arcade MCP servers.

## Next steps

> [card] [Add more tools](Tool%20integrations.md)
>
> Connect additional services to your agent

> [card] [Remote MCP servers](Remote%20MCP%20servers.md)
>
> Connect custom MCP servers to your workspace

> [card] [Manage agent settings](../Configure/Manage%20agent%20settings.md)
>
> Configure agent behavior and permissions

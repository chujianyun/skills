# Manage agent settings

> Manage your agents in Fleet.

This page explains how to manage the settings for your agents in LangSmith Fleet.

## Change the model

To change the model for your agent:

1. In the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-fleet-manage-agent-settings), open your agent.
2. In the sidebar, expand the **Advanced settings** drawer.
3. In the **Model** section, select the model you want to use.
4. If the model requires an API key, add it in the **API keys** section.

Custom models are available for enterprise deployments. For more information, see [Custom models](../Get%20started/Essentials.md#custom-models).

## Reconnect tool integrations

To reconnect a tool integration to an agent:

1. In the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-fleet-manage-agent-settings), open your agent.
2. In the sidebar, expand the **Connections** drawer.
3. Click **Manage** next to the integration to review or reconnect it.

## Download agent files

To download the files for your agent, open the agent, expand the **Advanced settings** drawer in the sidebar, and under **Developer** click **Download ZIP**. This exports the agent configuration as a ZIP file.

## Change access to the agent

Agents can be private to the creator, shared with specific people, or shared with your entire LangSmith workspace.

| Feature | Private agents | [Workspace agents](#workspace-scoped-agent-details) |
| - | - | - |
| **Ownership and access** | Only visible to creator | Visible to anyone within the same LangSmith workspace |
| **OAuth authentication** | OAuth credentials are scoped to creator | OAuth credentials are scoped to each user; new users cloning workspace agents must re-authenticate with selected tools |
| **Secrets** | Uses workspace-scoped LangSmith secrets | Uses workspace-scoped LangSmith secrets (same as private agents) |

To change the agent visibility, open your agent, expand the **Sharing** drawer in the sidebar, and select **Private** or **Workspace**. To share with specific people, click **+ Add** next to **Specific people**.

### Workspace-scoped agent details

While workspace-scoped agents are shared, some details are public, while others are private:

* **Threads are always user-scoped**, so even if an agent is workspace-scoped, the chat history created within that agent will always be private and only accessible to the specific user who created them.
* **The system prompt, selected tools, and sub-agents will be public on workspace-scoped agents.** Users will not be able to modify these fields on the original workspace-scoped agent, but can make changes once they've cloned the agent.
* **The channel type on workspace-scoped agents is public** (for example, Slack message received), but the specific connection with the channel (for example, the Slack channel, or Gmail address) is not shared. This way, users know what channel to use when cloning an agent, but can't gain unauthorized access to any connections the original user has set up.

## Update memory

Your agent can remember information from previous conversations and use it to make better decisions in future conversations. Agents persist memories by writing files to a **memories folder** using `write_file` and `edit_file` tool calls.

By default, your agent requires approval before saving to the memories folder. When this setting is enabled, the agent pauses and waits for you to accept, edit, or reject each memory update in the Fleet UI before continuing.

> [!TIP]
>
> If your agent runs on a [schedule](../Tools%20and%20automation/Schedules.md#add-a-schedule) or other automated schedule, disable the memory approval requirement. Otherwise, the agent will pause on every scheduled run that involves a memory update and wait indefinitely for manual approval.

### Disable required approval for memory updates

To disable the memory approval requirement:

1. In the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-fleet-manage-agent-settings), open your agent.
2. In the sidebar, expand the **Knowledge** drawer.
3. In the **Memory** section, set **Update memory and instructions** to **Auto**.

## Use the agent programmatically

You can use the [LangGraph SDK](../../../Monitor/Reference/LangSmith%20reference.md) to connect to your agent through code. To view the code snippets needed to call your agent programmatically:

1. In the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-fleet-manage-agent-settings), open your agent.
2. In the sidebar, expand the **Advanced settings** drawer.
3. Under **Developer**, click **View code snippets**.
4. Copy the pre-populated code snippets for your agent.

For more information, see [Call agents from code](../Advanced/Use%20Fleet%20agents%20in%20code.md).

## Pause agent

To pause an agent, pause its channels:

1. In the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-fleet-manage-agent-settings), open your agent.
2. In the sidebar, expand the **Channels** drawer.
3. Click the **Pause channels** button.

> [!TIP]
>
> To resume, click the **Resume channels** button.

## Delete agent

To permanently delete an agent:

1. In the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-fleet-manage-agent-settings), open your agent.
2. In the sidebar, expand the **Advanced settings** drawer.
3. In the **Danger zone** section, click **Delete agent**.
4. To confirm the deletion, click the **Delete** button.

> [!WARNING]
>
> This action cannot be undone. It will permanently delete the agent, all threads linked to the agent, and unlink any attached channels.

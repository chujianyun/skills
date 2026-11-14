# Build an agent with LangSmith Studio

> Describe an agent in Studio, let LangSmith Chat draft its configuration, then review, save, and test it without writing code.

LangSmith Studio builds a no-code agent from a description. You describe what the agent should do, [LangSmith Chat](../../Test/Datasets%20%26%20Experiments/Analyze%20experiment%20results/LangSmith%20Chat.md) drafts its configuration, and you review each step before you save. Then you test the agent and see its traces without leaving Studio.

Use it when you want a working agent without a local project or a deployment. To build an agent from files on your own machine instead, see [Managed Deep Agents](../../Build/Python/Deep%20Agents/Deployment/Managed%20Deep%20Agents.md). The result is a regular [agent](../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20Registry.md#agent), so its traces, dashboards, and evaluators behave the same as one you instrumented yourself. Studio builds the same kind of no-code agent as [Fleet](../../Additional%20documentation/No-code%20agents%20with%20LangSmith%20Fleet.md), so the Fleet pages on tools, channels, schedules, and skills apply to it.

> [!NOTE]
>
> Agent-based workspaces are available on [LangSmith Cloud](../../LangSmith%20setup/Cloud/Cloud%20%28SaaS%29.md). They are not available on [self-hosted](../../LangSmith%20setup/Self-hosted/Self-hosted%20LangSmith.md) LangSmith. To check whether your workspace is agent-based, look at the control at the top left. In an agent-based workspace, it is a workspace switcher that names your workspace. In a [project-based](../../Monitor/Trace/Observability%20concepts.md#tracing-projects) workspace, it shows the LangSmith logo.

Creating an agent requires the `fleet-agents:create` [permission](../Fleet/Additional%20resources/Access%20%26%20oversight.md), which covers all no-code agents, including those built in Studio. Without it, Studio shows "Ask a workspace admin for permission to create agents."

## Start a new agent

Open the **Build an agent** screen from either place:

* **Studio**: In the left navigation, with **All agents** selected, click **Studio**, then click **Build a new agent**.
* **New agent menu**: In the [new agent menu](../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md#start-from-the-new-agent-menu), under **Build**, click **Without code**.

![The Build an agent screen in Studio, with a prompt box that reads Build me an agent that, a model menu, a send icon, six template cards, and a Build in code button.](../../../assets/images/ad2caad1df8d-studio-build-an-agent-light.png)

## Describe the agent

To describe the agent:

1. In the box that reads "Build me an agent that…", describe what the agent should do, up to 8,000 characters. To start from an example, click a template card instead: **Schedule manager**, **Slides designer**, **Support triage**, **Project manager**, **Deep researcher**, or **Data analyst**. Each card lists the apps its agent uses. The card fills in the prompt, and you can edit it before you send it.
2. (Optional) From the model menu in the bottom-left corner of the box, choose the model Chat uses to draft the agent. **Auto** uses the LangSmith-hosted model when it is available. Otherwise, the menu starts on your workspace's default model for Chat. This choice applies to Chat only. You set the agent's own model in the [Basics step](#configure-the-agent).
3. Click the **Build with AI**  icon.

To build the agent in code instead, click **Build in code** below the template cards. It opens the **Build with code** pane, which offers [Managed Deep Agents](../../Build/Python/Deep%20Agents/Deployment/Managed%20Deep%20Agents.md) hosted by LangSmith, or the open source frameworks to host yourself. For more information, see [Create an agent](../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md#start-from-the-new-agent-menu).

## Generate the draft

Chat drafts the agent's name, description, and instructions first. Once all three are filled in, LangSmith creates the agent and opens its configuration at the **Instructions** step.

> [!NOTE]
>
> The agent exists from this point, before you click **Save**. It appears in the agent list and the agent switcher for everyone in the workspace. If you leave the page without clicking **Cancel**, the agent stays in the workspace. To remove it, see [Save or cancel](#save-or-cancel).

If Chat stops before the name, description, and instructions are filled in, click **Retry** to send your original prompt again. **Retry** appears only before the agent is created, so retrying does not create a second agent.

Chat then suggests the remaining steps one at a time: connections, channels, and schedules. You can also edit any step directly.

## Configure the agent

The **Configure agent** view lists the configuration as steps:

* **Basics**: The agent's **Name**, a **Description** of what it does, and the **Model** that powers its responses. The name is the label you see in the agent switcher. The **Model** list shows the same models that are enabled for [Fleet](../Fleet/Configure/Manage%20agent%20settings.md#change-the-model).
* **Instructions**: What the agent should do and how it should work.
* **Connections**: The apps and tools the agent can use, added with **Add connection**. Details follow the list.
* **Channels**: Where people can chat with the agent, added with **Add channel**. The options are Slack, Gmail, Outlook, and Microsoft Teams. Microsoft Teams carries an **Admin** badge and is available only for agents with shared connections. Studio saves channel setup separately from the rest of the configuration. For more information, see [Channels](../Fleet/Tools%20and%20automation/Channels.md).
* **Schedules**: The [scheduled runs](../Fleet/Tools%20and%20automation/Schedules.md) the agent makes on its own, added with **Add schedule**.

When you edit an existing agent, the view also shows **Skills** and **Memory**. For more information, see [Skills](../Fleet/Tools%20and%20automation/Skills.md).

In **Connections**, the **Connection Type** heading shows whose accounts the agent uses:

* **Shared** (fixed credentials): Everyone uses one set of connected accounts.
* **Per-user** (user credentials): Each person connects their own accounts.

Studio creates new agents as **Per-user**. The heading shows the type but does not change it. For more information, see [Agent identity](../Fleet/Configure/Agent%20identity.md).

Account setup takes effect right away, while tool selections stay in the draft until you save. For each tool, choose one option:

* **Auto**: The agent runs the tool without asking.
* **Ask**: The agent asks for approval before it runs the tool.
* **Remove**: The tool is removed from the agent.

## Save or cancel

To save, click **Save** in the **Configure agent** header, or **Save agent** on the card above the Chat composer. The card appears only when there is something to save. Saving closes Chat and returns you to Studio, where you can test the agent.

To leave without keeping the agent, click **Cancel**. Because the agent already exists, the **Cancel agent creation?** dialog asks you to confirm:

* **Delete agent**: Permanently deletes the agent and discards its configuration.
* **Keep building**: Returns you to the configuration.

If you cancel before Chat finishes the first draft, the dialog offers **Discard and leave** instead of **Delete agent**, and nothing is created.

## Test the agent

After you save, Studio opens a chat with the agent. Send it a message to try it out. The traces panel beside the chat fills with the run's traces as the agent responds.

In Studio, you test a no-code agent through chat, so **Interact**, which needs an agent with a graph view, is unavailable for it.

## Change the configuration later

Editing an agent requires the `fleet-agents:update` [permission](../Fleet/Additional%20resources/Access%20%26%20oversight.md) and edit access on the agent. Without them, the configuration opens with a **Read-only configuration** banner.

To open an existing agent in Studio, use either path:

* In the left navigation, with **All agents** selected, click **Studio**, click **Select existing agent**, and pick the agent from the list.
* Select the agent in the agent switcher, then click **Studio** in the left navigation.

To edit an agent's configuration, use either control:

* In the Studio chat, click  **Edit**.
* On the agent's Overview, click the **Agent settings**  icon, then click **Edit configuration**.

Both open the configuration at the **Basics** step. Make your changes and click **Save**. **Cancel** discards them and returns you to Studio.

If you ask Chat to change the agent from elsewhere in LangSmith, it offers to open the configuration in Studio and keeps the conversation.

## Find traces and environments

Studio creates the agent with only a **Production** [environment](../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20environments.md), and its runs land there. It gains other environments only when something reports into them.

To find the agent's traces, select the agent and open **Tracing**. To see its environments, read the summary on the [agent Overview](../../LangSmith%20setup/Overview/Agent-based%20workspaces/Navigate%20agents.md#read-the-agent-overview).

LangSmith runs the agent on a Studio runtime, so you cannot create an Agent Server for it. The [agent environment deploy flags](../../LangSmith%20setup/Overview/Agent-based%20workspaces/Deploy%20to%20an%20agent%20environment.md) do not apply, and the **Agent Server** link in its Overview header is disabled.

## See also

* [Test from Studio](../../Test/Test%20from%20Studio/LangSmith%20Studio.md)
* [Create an agent](../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md)
* [Navigate agents](../../LangSmith%20setup/Overview/Agent-based%20workspaces/Navigate%20agents.md)
* [Agent Registry](../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20Registry.md)
* [Agent environments](../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20environments.md)
* [Fleet](../../Additional%20documentation/No-code%20agents%20with%20LangSmith%20Fleet.md)

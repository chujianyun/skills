# Quickstart

> Build an agent from a template

By the end of this quickstart, you will have an Executive Assistant that labels the Gmail messages needing your attention and pauses for approval before acting, all set up without code or a model API key and controlled through chat.

You interact with your agent through chat, just like texting a helpful assistant.

You will start from the prebuilt **Executive Assistant** [template](Templates.md), which manages your inbox, calendar, and daily brief.

## Before you start

You need:

* A LangSmith account ([sign up here](https://smith.langchain.com/agents?skipOnboarding=true&utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-fleet-quickstart)).
* A Gmail account.
* A Google Calendar.

Fleet manages the AI model for you, so you do not need your own model provider API key. For more information, see [Models](Essentials.md#models).

## 1. Create your agent

**1. Navigate to Fleet**

1. In the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-fleet-quickstart), click  **Switch to Fleet** at the top of the left-hand navigation.

**2. Choose a template**

1. Select **Templates** in the left-hand navigation, or click **+** in **My Agents** and select **From template**.
2. Select the **Executive Assistant** template to create your agent.
3. Click **Create Agent** at the top right.

> [!TIP]
>
> If you do not want to start with a template, choose **Build with AI** or **New agent** when you create an agent and describe the agent you want. The agent configures itself and pauses at key points for your input.

**3. Skip channel setup for now**

When the agent prompts you to connect a channel, click **Skip for now**. You connect channels in a [later step](#3-configure-your-agent).

**4. Answer onboarding questions**

Provide information so your agent knows how to work the way you prefer.

## 2. Connect tools

Your agent asks you to connect to your Gmail and Google Calendar accounts.

A connection gives your agent the [tools](../Tools%20and%20automation/Tool%20integrations.md) to use a service. A [channel](../Tools%20and%20automation/Channels.md) lets the service trigger the agent. You connect Gmail and Google Calendar here, then add Gmail as a channel in [Configure your agent](#3-configure-your-agent).

**1. Connect Gmail**

1. In the **Gmail** row, click **Connect** on the right.
2. In the dialog, click **+ Connect new account**.
3. Choose your account and click **Continue**.
4. Review permissions and click **Allow**.
5. LangSmith redirects you back to Fleet. Select **Gmail** to expand the row.
6. Click **Choose account** and select the account you chose in step 3.

**2. Connect Google Calendar**

1. Connecting Gmail authorized your Google account for Gmail only, not Google Calendar. To grant calendar access, click **Update permissions** on the right in the **Google Calendar** row.
2. In the dialog, click **Reauthorize**.
3. Choose your account and click **Continue**.
4. Review permissions and click **Allow**.
5. LangSmith redirects you back to Fleet. Close the dialog.
6. Click **Save and continue**.

> [!NOTE]
>
> Your agent only accesses your accounts when working on tasks you give it. You can revoke access anytime in the [agent sidebar](Essentials.md#agent-sidebar) or your Google account settings.

## 3. Configure your agent

There are two ways to configure your agent:

* Chatting with your agent directly
* Modifying settings in the [agent sidebar](Essentials.md#agent-sidebar)

This section describes how to configure your agent using the agent sidebar.

**1. Open the agent sidebar**

Click \*\* Configure\*\* at the top right to open the agent sidebar.

**2. View connections**

Expand the **Connections** drawer. **Gmail** and **Google Calendar** appear as **Connected**. If either shows as not connected, complete [2. Connect tools](#2-connect-tools) before continuing.

**3. Configure a tool to ask for approval**

In the **Connections** drawer, click **Gmail** to view the available tools. By default, the tools are enabled and set to **Auto**, so they run without your approval.

For **Apply Label**, click **Ask**, so your agent pauses and waits for your approval before continuing. You can accept the proposed action, or reject it and tell the agent what to change. For more information, see [Human-in-the-loop](Essentials.md#human-in-the-loop).

**4. Connect channels**

Expand the **Channels** drawer. Click **Gmail**. Select the account that you set up for **Connections**. Click **Confirm**.

**5. Save your changes**

Click **Save** at the top of the sidebar to save your changes, then click **X** to close the panel.

## 4. Test your agent

**1. Send your agent a task**

In the agent chat, try out the Executive Assistant, for example:

> *Apply a "Review" label to emails that I receive, which require some kind of review from me.*

**2. Accept or reject the agent's action**

Click **Accept** to approve the agent's proposed action or tell the agent what it did wrong and click **Reject**.

**3. Check your inbox in Gmail**

If you clicked **Accept**, emails that need review now have the **Review** label in your inbox.

## Edit your agent

You may want to update your agent's instructions or include more tools. You can chat with your agent directly to ask for updates, or configure it from the [agent sidebar](Essentials.md#agent-sidebar):

* Edit the agent's instructions (its `AGENTS.md`) in the **Knowledge** drawer. See [Instructions](Essentials.md#instructions).
* Add integrations and tools in the **Connections** drawer, and set each tool to run automatically or [ask for approval](Essentials.md#human-in-the-loop). See [Tools](../Tools%20and%20automation/Tool%20integrations.md).
* Connect [Slack](../Tools%20and%20automation/Integrate%20Slack%20with%20an%20agent.md), [Gmail](../Tools%20and%20automation/Channels.md#add-a-gmail-channel), or [Microsoft Teams](../Tools%20and%20automation/Integrate%20Microsoft%20Teams%20with%20an%20agent.md) in the **Channels** drawer.
* Run your agent on a [schedule](../Tools%20and%20automation/Schedules.md) in the **Schedules** drawer.
* Change the [model](../Configure/Manage%20agent%20settings.md#change-the-model) in the **Advanced settings** drawer.

## Next steps

Now that you have created your first agent, here is what to explore:

> [card] [Try more templates](Templates.md)
>
> Explore prebuilt agents for common tasks

> [card] [Add automation](Essentials.md#channels)
>
> Run your agent automatically with channels (Slack, email, schedules)

> [card] [Connect more tools](../Tools%20and%20automation/Tool%20integrations.md)
>
> Add Slack, GitHub, Linear, and more

> [card] [Build complex agents](Essentials.md#sub-agents)
>
> Use sub-agents to break down big tasks

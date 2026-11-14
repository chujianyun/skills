# Channels

> Configure channels to trigger your Fleet agents automatically.

Channels define when your agent starts running. Connect your agent to external events so it responds automatically to messages, emails, or other events.

> [!TIP]
>
> To trigger an agent on a recurring basis, use [schedules](Schedules.md).

## Add a channel

To add a channel:

**1. Open your agent**

Open your agent in the [Fleet](https://smith.langchain.com/agents?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-fleet-channels) inbox.

**2. Add the channel**

1. In the sidebar, expand the **Channels** drawer and click **Connect your first channel**.
2. Select the channel you want to add, then follow the prompts to authenticate.

### Add a Gmail channel

The Gmail channel activates your agent when new emails arrive in your inbox. To let your agent read and respond to emails, add Gmail tools in the **Tools** section. Available Gmail tools include reading emails, sending replies, creating drafts, managing labels, and marking messages as read. See [Tool integrations](Tool%20integrations.md) for more information.

> [!WARNING]
>
> The Gmail channel only monitors your primary inbox. The following emails do not activate the channel:
>
> * **Alias emails**: Messages sent to an email alias rather than your primary address.
> * **Mailing list emails**: Messages received through a mailing list or group.
> * **Emails outside the inbox**: Messages that skip the inbox due to filters, or that land in spam, trash, or other folders.

### Add a Slack channel

The Slack channel lets your team chat with your agent directly in Slack. After you authenticate with Slack once, Fleet adds the agent to Slack in one click and configures a Slack app with the agent's name, description, and icon. Mention the agent in a channel or send it a direct message to start a run.

For setup instructions, see [Integrate Slack with an agent](Integrate%20Slack%20with%20an%20agent.md).

### Add a Microsoft Teams channel

The Teams channel activates your agent when messages are sent in Microsoft Teams conversations.

For full setup instructions including Azure Bot creation, credential registration, and tool configuration, see [Integrate Microsoft Teams with an agent](Integrate%20Microsoft%20Teams%20with%20an%20agent.md).

## Pause and resume channels

You can pause and resume channels without removing them. To pause all channels:

1. In the [Fleet](https://smith.langchain.com/agents?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-fleet-channels) inbox, open your agent.
2. In the sidebar, expand the **Channels** drawer.
3. Click the  **Pause channels** button to pause all channels.

To resume all channels, click  **Resume channels** button.

## Thread behavior

How threads are marked depends on whether the agent uses channels:

* **Chat agents (no channel)**: Responses mark the thread as **unread**. Viewing the thread marks it as read.
* **Channel-based agents**: Responses keep the thread as **read** by default.

You can manually mark any thread as read or unread at any time.

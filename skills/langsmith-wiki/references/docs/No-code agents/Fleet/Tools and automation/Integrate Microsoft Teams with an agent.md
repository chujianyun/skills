# Integrate Microsoft Teams with an agent

> Connect LangSmith Fleet to Microsoft Teams by bringing your own Azure Bot to let agents communicate with users in Teams.

With LangSmith Fleet, you can connect your agents to Microsoft Teams by registering a custom Azure Bot. Once connected, your agents can:

* Receive messages from Teams users, starting a new run with the message content.
* Respond directly in Teams conversations using the Bot Framework.
* Access Teams channels and messages through Microsoft Graph API tools.

> [!NOTE]
>
> In channel conversations, the bot only responds when explicitly mentioned. In direct messages and group chats, the bot responds to all messages.

## Prerequisites

* An existing agent in Fleet (see [Quickstart](../Get%20started/Quickstart.md) to create one)
* An [Azure account](https://portal.azure.com) with permission to create resources
* Admin access to a Microsoft Teams workspace, or permission to install apps

## Create an Azure Bot

Before registering in Fleet, you need to create an Azure Bot resource and obtain its credentials.

**1. Create an Azure Bot resource**

1. Go to the [Azure Portal](https://portal.azure.com).
2. Search for **Azure Bot** and click **Create**.
3. Fill in the required fields:
   * **Bot handle**: A unique identifier for your bot.
   * **Subscription**: Select your Azure subscription.
   * **Resource group**: Create a new one or select an existing one.
   * **Type of App**: Select **Single Tenant**.
   * **Creation type**: Select **Create new Microsoft App ID**.
4. Click **Review + create**, then **Create**.

> [!NOTE]
>
> Azure no longer allows new Multi Tenant bots. Existing Multi Tenant bots still work.

**2. Get your app credentials**

After the resource is created:

1. Navigate to your bot resource and click **Configuration** in the left sidebar.
2. Copy the **Microsoft App ID** and the **App Tenant ID**. You will need both later.
3. Click **Manage Password** next to the App ID.
4. Click **New client secret**, add a description, and click **Add**.
5. Copy the **Value** of the new secret immediately — it is only shown once.

> [!WARNING]
>
> Copy the client secret value immediately after creation. You cannot retrieve it later. If you lose it, you must create a new one.

**3. Configure the messaging endpoint**

You will set the messaging endpoint after registering the bot in Fleet. Skip this field for now—you will return to this step later.

## Register the bot in Fleet

**1. Open the integrations page**

1. Navigate to **Fleet** in the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-fleet-teams-app).
2. Go to the **Integrations** page.
3. Click **Add Teams App**.

**2. Enter your credentials**

Fill in the following fields:

* **App Name**: A display name for the bot in Fleet.
* **Azure App ID**: The Microsoft App ID from the Azure Bot resource.
* **Azure App Password**: The client secret value you copied earlier.
* **Azure Tenant ID**: The App Tenant ID from the Azure Bot resource. Required for Single Tenant bots. Leave it empty only for an existing Multi Tenant bot.

Click **Create** to register the bot.

**3. Copy the webhook URL**

After registration, Fleet displays a **webhook URL**. Copy this URL—you need it to complete the Azure Bot configuration.

**4. Set the messaging endpoint in Azure**

1. Return to your Azure Bot resource in the [Azure Portal](https://portal.azure.com).
2. Go to **Configuration**.
3. Paste the webhook URL from Fleet into the **Messaging endpoint** field.
4. Click **Apply**.

## Add the bot to Teams

**1. Open the Teams channel**

1. In the Azure Portal, go to your bot resource.
2. Click **Channels** in the left sidebar.
3. Select **Microsoft Teams** and click **Apply**.
4. Agree to the terms of service.

**2. Install the bot in Teams**

1. In Teams, click **Apps** in the left sidebar.
2. Click **Manage your apps** then **Upload an app**.
3. Upload a [Teams app manifest](https://learn.microsoft.com/en-us/microsoftteams/platform/resources/schema/manifest-schema) that references your Azure App ID, or use the **Open in Teams** link from the Azure Bot Channels page.
4. Add the bot to the desired team or chat.

## Link the bot to an agent

You can link a Teams bot to an agent from the integrations page or from the agent sidebar.

### Link from the integrations page

1. Navigate to the **Teams Apps** section on the **Integrations** page in Fleet.
2. Select the bot you want to link.
3. From the dropdown menu, choose the agent you want to link to.

### Link from the agent sidebar

1. Select your agent from **My Agents** in the left-hand navigation.
2. In the sidebar, expand the **Channels** drawer.
3. Select **Teams**.
4. From the dropdown menu, select the Teams app you want to link.

## Add Teams tools

Tools let your agent take actions in Teams. To respond to messages and interact with Teams, add the relevant tools.

> [!TIP]
>
> You can also ask your agent to add these tools itself. In the agent chat, try: "Add the Teams tools so you can respond to messages."

1. In the sidebar, expand the **Connections** drawer and click **Add connection**.
2. Search for "Teams" and add the tools you need:
   * **teams\_bot\_send\_proactive\_message**: Send messages back to the Teams conversation
   * **microsoft\_teams\_list\_my\_teams**: List teams the authenticated user belongs to
   * **microsoft\_teams\_list\_channels**: List channels in a team
   * **microsoft\_teams\_post\_channel\_message**: Post a message to a channel
   * **microsoft\_teams\_read\_channel\_messages**: Read recent messages from a channel
3. If prompted, click **Connect** to authorize the Microsoft Graph tools.

> [!NOTE]
>
> The `teams_bot_send_proactive_message` tool uses Bot Framework credentials and does not require separate OAuth authorization. The other Teams tools use Microsoft Graph API and may require OAuth consent.

## Configure agent behavior (optional)

Your agent needs to know how to handle incoming Teams messages. Update its instructions by prompting it directly in the agent chat:

```
Update your instructions to handle the Teams Trigger and Teams Tools
for bidirectional communication
```

Adjust the instructions based on your use case—for example, you might want the agent to only respond to certain types of questions, or to pull information from specific sources before replying.

## Troubleshooting

### Agent does not respond

* Check the thread in Fleet for any approvals that need human input.
* In channel conversations, make sure you **@mention** the bot. Channel messages without a mention are ignored.
* Check the **Feed** tab for errors.
* Verify the messaging endpoint in the Azure Bot resource matches the webhook URL from Fleet.
* Ensure the bot registration is not paused in Fleet.

### Invalid credentials error during registration

* Verify that the **Azure App ID** and **App Password** (client secret) are correct.
* Make sure the client secret has not expired. Create a new secret in Azure if needed.
* For a Single Tenant bot, check that the **Azure Tenant ID** in Fleet matches the App Tenant ID in Azure.

### Bot works in direct messages but not in channels

* The bot must be explicitly **@mentioned** in channel conversations.
* Make sure the bot has been added to the team and has permission to read messages in the channel.

## Next steps

> [card] [Add more tools](Tool%20integrations.md)
>
> Connect additional services to your agent

> [card] [Add more channels](Channels.md)
>
> Set up email, schedule, or webhook channels

> [card] [Use templates](../Get%20started/Templates.md)
>
> Start from a prebuilt agent template

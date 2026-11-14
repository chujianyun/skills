# Salesforce integration

> Connect LangSmith Fleet to Salesforce so your agents can query records, navigate schemas, and read custom fields.

The Salesforce integration gives your agents read-only access to data in your Salesforce org. Once connected, an agent can:

* Query records across standard and custom objects.
* Navigate your Salesforce data schema, including relationships and custom fields.
* Pull live context from Salesforce into any thread or scheduled run.

> [!NOTE]
>
> Connecting Salesforce is a one-time setup per Salesforce org. A Salesforce System Administrator (or a user with the **Approve Uninstalled Connected Apps** permission) must install the connector before other users can authenticate.

## Prerequisites

* A LangSmith workspace with access to [Fleet](https://smith.langchain.com/agents?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-fleet-salesforce).
* A Salesforce org and user account.
* A Salesforce System Administrator to complete the install (or the **Approve Uninstalled Connected Apps** permission on your own user).

## Register the connector

The first connection attempt registers the **LangChain Fleet Connector** in your Salesforce org so that an administrator can install it. This initial attempt is expected to fail with an authentication error.

**1. Open the Integrations page**

In the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-fleet-salesforce), navigate to the [**Fleet** > **Integrations**](https://smith.langchain.com/agents/tools) tab.

**2. Start the Salesforce connection**

Find the **Salesforce** tool and click **Connect**.

**3. Sign in to Salesforce**

Sign in with your Salesforce credentials. If your org requires a custom domain or SSO, click **Use Custom Domain** and enter your org's My Domain before signing in. Then click **Allow** to authorize the connection.

> [!NOTE]
>
> The first attempt fails by design. The failed request registers the **LangChain Fleet Connector** in your Salesforce org so an administrator can install it in the next step.

> [!TIP]
>
> If you are not a Salesforce administrator, stop here and send your admin the link to this page. They need to follow the **Install the connector** and **Grant user access** steps below before you can complete the connection.

## Install the connector

> [!NOTE]
>
> This step must be completed by a Salesforce System Administrator.

**1. Open Salesforce Setup**

In Salesforce, click the  gear icon and select **Setup**.

**2. Open Connected Apps OAuth Usage**

In the **Quick Find** box, type `Connected Apps OAuth Usage` and open the page.

**3. Install the connector**

1. Find **LangChain Fleet Connector** in the list.
2. Click **Install**.
3. Confirm the installation on the next page.

## Grant user access

Granting access through a permission set is the recommended way to control which users can authenticate with Fleet.

> [!NOTE]
>
> This step must be completed by a Salesforce System Administrator.

**1. Open the app policies**

From **Connected Apps OAuth Usage**, click **Manage App Policies** next to **LangChain Fleet Connector**.

**2. Pre-authorize admin-approved users**

Under **OAuth Policies** > **Permitted Users**, select **Admin approved users are pre-authorized**, then click **Save**.

**3. Assign a permission set**

Use **Manage Permission Sets** to grant access to the users who need to connect the Salesforce tool in Fleet.

## Connect from Fleet

Once your administrator has installed the connector and granted access, return to Fleet to complete the connection.

1. In the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-fleet-salesforce), navigate to the [**Fleet** > **Integrations**](https://smith.langchain.com/agents/tools) tab.
2. Find the **Salesforce** tool and click **Connect**.
3. Sign in with your Salesforce credentials and click **Allow**.

The connection now succeeds and Salesforce tools become available to agents in your workspace.

## Use Salesforce with an agent

After connecting, add Salesforce tools to a specific agent:

1. Open your agent in [Fleet](https://smith.langchain.com/agents?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-fleet-salesforce).
2. In the sidebar, expand the **Connections** drawer and click **Add connection**.
3. Search for **Salesforce Query** and add it to the agent.

## Troubleshooting

### Connection fails with an authentication error

The first connection attempt is expected to fail. It registers the **LangChain Fleet Connector** in your Salesforce org so an administrator can install it. If the connection still fails after the connector is installed, confirm that:

* The administrator completed both **Install the connector** and **Grant user access**.
* Your Salesforce user is assigned to a permission set that grants access to the connector.
* You signed in through **Use Custom Domain** with the correct Salesforce domain.

### Agent cannot see an object or field

Salesforce tools run with the permissions of the connected user. If an agent cannot read an object or custom field, verify that the user's Salesforce profile and permission sets grant read access to that object.

## Next steps

> [card] [Add more tools](Tool%20integrations.md)
>
> Connect additional services to your agent

> [card] [Agent identity](../Configure/Agent%20identity.md)
>
> Choose whether the agent uses shared or per-user credentials

> [card] [Human-in-the-loop](../Get%20started/Essentials.md#human-in-the-loop)
>
> Require approval before the agent takes sensitive actions

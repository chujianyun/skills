# Create an account and API key

To get started with LangSmith, you need to create an account. You can sign up for a free account in the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-create-account-api-key). LangSmith supports sign in with Google, GitHub, and email.

## API keys

LangSmith supports three types of API keys with different permissions and lifecycles:

* [**Personal Access Tokens (PATs)**](../Govern/Organization/Overview.md#personal-access-tokens-pats) inherit the permissions of the user who created them. Use PATs for personal scripts or tools.
* [**Service keys**](../Govern/Organization/Overview.md#service-keys) scope to specific [workspaces](../Govern/Organization/Overview.md#workspaces) or the entire [organization](../Govern/Organization/Overview.md#organizations). Use service keys for agents and production services.
* [**Tracing keys**](#tracing-keys) only submit [traces](../../Monitor/Trace/Observability%20concepts.md#traces) in selected workspaces. Use tracing keys for agents that send traces but do not need to read them.

## Create a PAT or service key

To create a PAT or service key in the UI:

**1. Open API Keys settings**

Navigate to the [**Settings** page](https://smith.langchain.com/settings) and select the **API Keys** section.

**2. Configure the key type**

For service keys, choose **Full Organization** or **Specific Workspaces**. For **Specific Workspaces**, select the workspaces and choose the organization role: **Organization Viewer** (the default) or **Organization Restricted**. **Full Organization** keys retain their existing organization role options.

[Enterprise](https://docs.langchain.com/langsmith/pricing-plans.md) users can also [assign specific workspace roles](../Govern/Organization/Overview.md#workspace-roles) to service keys, which adjusts their permissions independently of any user.

**3. Set expiration**

Set the key's expiration. The key becomes unusable after the number of days chosen, or never, if that is selected.

**4. Create the key**

Click **Create API Key.** LangSmith will display the API key only once, so make sure to copy it and store it in a safe place.

> [!TIP]
>
> [Enterprise](https://docs.langchain.com/langsmith/pricing-plans.md) Organization Admins can edit the [role](../Govern/Organization/Overview.md#workspace-roles) on an existing service key without rotating the key. On the [**Settings** page](https://smith.langchain.com/settings) **API Keys** section, switch to the **Service** tab and click any service key row to open the edit dialog. Update the workspace role or organization role and click **Save**. Workspace-scoped keys support **Organization Viewer** or **Organization Restricted**. Existing workspace-scoped keys keep their current organization role until you change it. The key string itself is unchanged.

## Manage PATs and service keys

You can deactivate or delete a PAT, but you can only delete a service key.

### Deactivate or delete a personal access token

Deactivation temporarily stops a PAT from authenticating; deletion permanently removes it. Deactivate a token when you need to keep its record and reactivate it later.

Members can deactivate, reactivate, and delete their own PATs. [Organization Admins](../Govern/Users%20%26%20access%20control/Role-based%20access%20control.md#organization-admin) and [Organization Operators](../Govern/Users%20%26%20access%20control/Role-based%20access%20control.md#organization-operator) can also manage every member's PATs.

| Action | Effect | Reversible |
| - | - | - |
| **Deactivate** | Stops authentication and keeps the record, owner, and last use visible with a **Deactivated** badge. | Yes. Select **Reactivate key** to use the same token again. |
| **Reactivate** | Allows authentication again with the same token and its original expiration date. | Yes. Deactivate the token again at any time. |
| **Delete** | Permanently removes the token and its record. | No. Create a new token if you need access again. |

Deactivation does not change a token's expiration date, and **Reactivate key** is unavailable once that date has passed. Create a new token instead.

To deactivate or delete a PAT:

1. Go to [**Settings**](https://smith.langchain.com/settings) > **API Keys** and open the **Personal** tab.
2. Find the token under **My keys**. To manage another member's token, switch to **All members**.
3. In the **Actions** column, select **Deactivate key** or **Delete key**. Each action opens its own confirmation dialog.
4. Type the token's description, which the dialog displays. For a token with no description, type the short key from the **Key** column instead.
5. Select **Deactivate** or **Delete** to confirm. A success notification confirms the action.

To reactivate a deactivated PAT, select **Reactivate key** in the **Actions** column. Reactivation takes one click, without a confirmation dialog, and displays a success notification.

Authentication results are cached, so a deactivated or deleted token stops working within a minute rather than instantly. A reactivated token may remain unusable until a cached rejection expires.

[Audit logs](../Govern/Auditing/Audit%20logs.md) record deactivation as `revoke_personal_access_token` and reactivation as `reinstate_personal_access_token`.

### Delete a service key

Service keys can only be deleted, not deactivated. To delete one, go to [**Settings**](https://smith.langchain.com/settings) > **API Keys**, open the **Service** tab, and select **Delete key** in the **Actions** column. Confirm by typing the key's description, as you would for a PAT.

## Tracing keys

Tracing keys are organization-owned credentials for submitting traces in selected workspaces. They limit an agent's access to `runs:create` and `projects:create`.

A tracing key submits run updates through the tracing ingestion APIs. Before tracing in an agent-based workspace, [register the agent](../Overview/Agent-based%20workspaces/Create%20an%20agent.md) in the UI or with a PAT or service key that has `projects:create`. Tracing keys cannot call the agent creation API.

A tracing key cannot read stored traces, update agent environment settings, create saved views, run experiments, or manage keys. Legacy project upsert requests are also denied. Use a separate credential for operations that require those permissions.

### Create a tracing key

Tracing-key creation requires active organization membership and active membership in every selected workspace. You need `workspaces:tracing-keys:create` in each workspace, including permissions granted through teams. Built-in Workspace Admin and Workspace Editor roles receive this permission; Workspace Viewers do not. Administrators must grant it explicitly to custom roles. You do not need `runs:create` yourself.

To create a key in LangSmith:

1. Go to **Settings** > **API Keys** and select **API Key**.
2. Select **Tracing Only** and enter a description.
3. Select the workspaces and an expiration date, then select **Create API Key**.
4. Copy the key before closing the dialog.

The tracing option requires a supported deployment. For BYOC workspaces, the data plane must also support tracing keys. Only workspaces where you have the creation permission and the deployment supports tracing keys are available for selection.

You can also create the key with `POST /api/v1/orgs/current/tracing-keys`. Authenticate as a user, including through a PAT if organization policy permits API keys to create keys. Service-account keys cannot create tracing keys.

The request accepts:

* **`workspaces`**: A required list of one or more workspace IDs. The key has no organization-wide scope.
* **`description`**: An optional label for the key.
* **`expires_at`**: An optional expiration timestamp, subject to service-key expiry limits.

The response returns `201 Created`, a `Location` header, and the secret in `key`. Copy the secret when you create it; list responses do not return it. Tracing keys have the `lsv2_tr_` prefix.

Use the key as `LANGSMITH_API_KEY` with the [SDK configuration](#configure-the-sdk) below. For a key scoped to multiple workspaces, set `LANGSMITH_WORKSPACE_ID` to a selected workspace. Direct API requests use `X-Tenant-Id`.

### Scope and lifecycle

A tracing key has fixed permissions across its selected workspaces. It does not inherit the creator's roles or project-tag access policies. Its workspace scope and permissions cannot be edited. Create a replacement key to change the scope.

Removing or disabling the creator does not disable tracing with the key. Deleting a selected workspace removes access to that workspace; it does not add access to other workspaces. Expiration and key deletion stop authentication, subject to authentication caching.

### List and delete tracing keys

In **Settings** > **API Keys**, select **Tracing** to view keys. To delete a key, select its delete action and enter its description to confirm. The delete action appears only when you have permission to delete that key.

`GET /api/v1/orgs/current/tracing-keys` lists keys visible to the authenticated user. It returns `items` and `next_cursor`. Use `page_size` to request 1–100 keys per page; the default is 50. Pass `next_cursor` as `cursor` to request the next page. The optional `workspace_ids` filter limits results to matching visible workspaces.

Listing a key does not necessarily grant permission to delete it. Hidden workspace IDs and names are omitted for callers without access to the full scope. Check `can_delete` for deletion authority.

`DELETE /api/v1/orgs/current/tracing-keys/{api_key_id}` deletes a tracing key. Repeated deletion returns `204 No Content`. Deletion is allowed for:

* **Creators**: The creator must remain an active organization member.
* **Organization key managers**: Callers with `organization:service-key:manage`, including service-account automation.
* **Workspace key managers**: Active members with `workspaces:manage-keys` in every remaining selected workspace.

The create, list, and delete endpoints are available over HTTP. Generated SDK key-management methods do not expose them. An issued tracing key works with the SDK's tracing APIs.

## Configure the SDK

Install the SDK for your language:

> [tab] Python
>
> ```bash pip theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> pip install langsmith
> ```
>
> ```bash uv theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> uv add langsmith
> ```

> [tab] TypeScript
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> npm install langsmith
> ```

For full details, refer to the [Python SDK](../../Monitor/Reference/langsmith%20%28smith-python-sdk%29.md) or [JS/TS SDK](../../Monitor/Reference/langsmith%20%28smith-js-ts-sdk%29.md) reference.

Before tracing in an agent-based workspace, [register an agent](../Overview/Agent-based%20workspaces/Create%20an%20agent.md). Then, set your API key, enable tracing, and select its identifier and environment:

```bash
export LANGSMITH_API_KEY=<your-api-key>
export LANGSMITH_TRACING=true
export LANGSMITH_AGENT_ID="<your-agent-id>"
export LANGSMITH_AGENT_ENVIRONMENT="local"
```

Remove legacy destination variables when using agent addressing. In project-based workspaces, including self-hosted LangSmith, use `LANGSMITH_PROJECT` instead of the two agent variables.

You may also need the following additional environment variables:

* `LANGSMITH_ENDPOINT` controls which LangSmith server the SDK sends data to. It defaults to `https://api.smith.langchain.com` (GCP US). Set it only if you are on a different deployment. For regional SaaS, set it to the API URL for your region:

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
          `https://api.smith.langchain.com`
        </td>
      </tr>

      <tr>
        <td>GCP EU</td>

        <td>
          `https://eu.api.smith.langchain.com`
        </td>
      </tr>

      <tr>
        <td>GCP APAC</td>

        <td>
          `https://apac.api.smith.langchain.com`
        </td>
      </tr>

      <tr>
        <td>AWS US</td>

        <td>
          `https://aws.api.smith.langchain.com`
        </td>
      </tr>

      <tr><td>Azure US</td>
      <td>`https://azure.api.smith.langchain.com`</td></tr>
    </tbody>
  </table>

* `LANGSMITH_WORKSPACE_ID` is required only if your API key is scoped to more than one [workspace](../Govern/Organization/Overview.md#workspaces). Find your Workspace ID on the [**Settings** page](https://smith.langchain.com/settings) under **General**:

  `LANGSMITH_WORKSPACE_ID=<Workspace ID>`

To reuse endpoint, API key, and workspace settings across local shells or remote runtimes, refer to [Profile configuration](Profile%20configuration.md).

## Use API keys outside of the SDK

See [instructions for managing your organization via API](../Govern/Organization/Manage%20your%20organization%20using%20the%20API.md).

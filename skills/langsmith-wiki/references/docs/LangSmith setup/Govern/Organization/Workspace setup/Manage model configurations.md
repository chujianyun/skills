# Manage model configurations

> Manage model configurations and control their availability across LangSmith features.

Model configurations define the model and parameters that LangSmith features use when calling an AI provider. A single shared library of configurations spans your entire [workspace](../Overview.md#workspaces), so any configuration you create is available across the following features without duplication:

* [**Playground**](../../../../Deploy/Prompt%20%26%20Context%20Hub/Prompts/Prompt%20engineering%20concepts.md)
* [**Evaluators**](../../../../Test/Get%20started/LangSmith%20Evaluation.md)
* [**Fleet**](../../../../No-code%20agents/Fleet/No-code%20agents%20with%20LangSmith%20Fleet.md)
* [**Chat**](../../../../Test/Datasets%20%26%20Experiments/Analyze%20experiment%20results/LangSmith%20Chat.md)
* [**Insights**](../../../../Monitor/Observe/Monitoring%20%26%20alerting/Discover%20errors%20and%20usage%20patterns%20with%20Insights.md)
* [**LLM Gateway**](../../../../LLM%20Gateway/Models%20and%20reliability/Custom%20model%20configurations.md)

[Workspace admins](../../Users%20%26%20access%20control/Role-based%20access%20control.md#workspace-admin) can create, edit, and delete configurations and control which providers and models are available per feature. Non-admin members can view configurations but cannot modify them.

Configurations can also carry [OAuth client credentials](#oauth-client-credentials), so LangSmith mints short-lived bearer tokens against your IdP at request time instead of using a static API key.

## Feature Access

The **Feature Access** table controls provider and model availability independently for each LangSmith feature.

| **Feature** | **Model selection experience** |
| - | - |
| Playground | Full model controls—view and adjust all parameters. No built-in models; relies on workspace configurations. |
| Evaluators | Full model controls—view and adjust all parameters. No built-in models; relies on workspace configurations. |
| Fleet | Choose from a curated list by default. You can also add custom workspace configurations. |
| Chat | Choose from a curated list by default. You can also add custom workspace configurations. |
| Insights (Thinking) | Model used for deep analysis. Choose from a curated list with provider recommendations by default. You can also add custom workspace configurations. |
| Insights (Summarization) | Model used for lightweight summarization. Choose from a curated list with provider recommendations by default. You can also add custom workspace configurations. |

All features support custom workspace configurations, so you can use any provider or model—even for features that show a curated list by default.

> [!NOTE]
>
> **Insights** uses two separate rows—one for analysis and one for summarization. The UI displays a warning if you select incompatible providers or non-recommended models for either row.

### Configure feature access

To configure feature access in the [UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-model-configurations):

1. Navigate to **Settings** > **Model configurations**.
2. In the **Feature Access** table, find the feature you want to configure.
3. Click **Enabled Providers** and toggle providers on or off for that feature.
4. Click **Available Models** and select which models users can choose from.
5. Use the **Default Model** dropdown to set the model preselected when users open the feature.

> [!NOTE]
>
> Providers disabled for the whole organization in **Settings** > **Model providers** appear locked in this table and can't be re-enabled per workspace. See [Organization-wide provider control](#organization-wide-provider-control).

## Organization-wide provider control

Provider availability is controlled at two levels:

* **Organization** (organization admins): turn a provider on or off for the **entire organization**—every [workspace](../Overview.md#workspaces) and every feature. Managed in **Settings** > **Model providers**.
* **Workspace** (workspace admins): the [Feature Access](#feature-access) table above, which controls provider and model availability **per feature** within a single workspace.

The organization level takes precedence. A provider disabled for the organization is unavailable in every workspace and every feature, and shows as **locked** in each workspace's Feature Access table—workspace admins can see it but can't re-enable it. Workspaces choose only among the providers the organization allows.

Managing organization-wide providers requires the [Organization Admin](../../Users%20%26%20access%20control/Role-based%20access%20control.md#organization-admin) role (the `organization:manage` permission), and is available on LangSmith [Cloud](../../../Cloud/Cloud%20%28SaaS%29.md) and [Self-hosted](../../../Self-hosted/Self-hosted%20LangSmith.md) for organizations (not personal accounts).

### Disable a provider for the organization

1. Navigate to the [Model providers](https://smith.langchain.com/settings/model-providers) page under **Settings**.
2. Toggle a provider off to disable it across the organization, or on to re-enable it.

## Organization-scoped model configurations

> [!NOTE]
>
> Organization-scoped model configurations are available on LangSmith [Self-hosted](../../../Self-hosted/Self-hosted%20LangSmith.md) and [Cloud Enterprise](https://docs.langchain.com/langsmith/pricing-plans.md) only.
>
> On self-hosted installations, organization-scoped model configurations require Helm chart version `0.17.0-rc.42` or later and application version `0.17.28rc1` or later.

[Organization admins](../../Users%20%26%20access%20control/Role-based%20access%20control.md#organization-admin) can create model configurations at the organization level, so a single configuration is available across every [workspace](../Overview.md#workspaces) in the organization without duplicating it per workspace.

Organization-scoped configurations appear alongside workspace-scoped configurations in the **Configurations** table on each workspace's **Settings** > **Model configurations** page. To make an org-scoped configuration available in Fleet, Playground, Evaluators, or other features, a [workspace admin](../../Users%20%26%20access%20control/Role-based%20access%20control.md#workspace-admin) must enable it in the [Feature Access](#feature-access) table for that workspace.

### Create an organization-scoped configuration

Creating an organization-scoped configuration requires the [Organization Admin](../../Users%20%26%20access%20control/Role-based%20access%20control.md#organization-admin) role:

1. Navigate to **Settings** > **Model configurations** at the organization level.
2. Under **Configurations**, click **+ Create**.
3. Select a **Provider** and **Model**, and complete the remaining fields.
4. Click **Save**.

### Enable an org-scoped configuration in a workspace

After an org-scoped configuration is created, workspace admins must enable it before it appears in workspace features:

1. In the workspace, navigate to **Settings** > **Model configurations**.
2. Find the org-scoped configuration in the **Configurations** table.
3. In the **Feature Access** table, enable the configuration for each feature where it should appear.

### Limitations

Keep the following constraints in mind when working with org-scoped configurations:

* **Scope is immutable.** A configuration saved as org-scoped cannot be changed to workspace-scoped, and a workspace-scoped configuration cannot be promoted to org-scoped. Create a new configuration if you need to change the scope.
* **Workspace takes precedence on name collision.** When a workspace configuration and an org-scoped configuration share the same name, the workspace version takes precedence.
* **Secrets store location.** On LangChain Cloud (non-BYOC), secrets for org-scoped configurations are stored on the LangChain Cloud control plane. In a BYOC deployment, you can configure where model secrets are written using the data-plane switcher.

## Configurations

The **Configurations** table is a shared library of named model configurations for your workspace. Configurations you create in LangSmith (including from the [Playground](../../../../Deploy/Prompt%20%26%20Context%20Hub/Prompts/Create%20and%20manage%20prompts/Configure%20prompt%20settings.md)) appear here and you can reuse them across all features.

### Create a configuration

1. Navigate to **Settings** > **Model configurations**.
2. Under **Configurations**, click **+ Create**.
3. Select a **Provider** and **Model**.
4. Enter the **API Key Name**—the name of the secret in your workspace that stores the provider API key.
5. Adjust parameters as needed. Parameters are grouped into sections for:

   * **Standard sampling settings**: temperature, top P, top K, presence penalty, frequency penalty, max output tokens
   * **Reasoning**: reasoning effort, service tier
   * **Provider config**: provider API, base URL
   * **Options**: stop sequences, seed, JSON mode, extra headers, requests per second, extra parameters

   Available parameters vary by provider—refer to your provider's documentation for details.
6. Click **Save**.

### Edit a configuration

1. In the **Configurations** table, click the overflow menu  next to the configuration.
2. Select **Edit**.
3. Update the configuration and click **Save**.

### Delete a configuration

1. In the **Configurations** table, click the overflow menu  next to the configuration.
2. Select  **Delete** and confirm.

## OAuth client credentials

> [!NOTE]
>
> OAuth client credentials are available on LangSmith [Cloud](../../../Cloud/Cloud%20%28SaaS%29.md) and [Self-hosted](../../../Self-hosted/Self-hosted%20LangSmith.md) deployments running version `0.16.0-rc.6` or later.

When a model configuration sits behind an OAuth2 gateway, you can store the OAuth `client_credentials` directly on the configuration instead of distributing a static API key. LangSmith exchanges those credentials for a short-lived bearer token at request time, attaches it as `Authorization: Bearer <token>` on the outbound LLM call, and refreshes the token before it expires. This is a per-configuration self-service alternative to routing the workspace through the [LLM auth proxy](../../../Self-hosted/Configure%20an%20instance/Set%20up%20the%20LLM%20auth%20proxy.md); the two are mutually exclusive per configuration.

OAuth client credentials are available on every [plan](https://docs.langchain.com/langsmith/pricing-plans.md) that supports custom model configurations. The **Use Custom OAuth** toggle applies to bearer-token providers (OpenAI, Anthropic, OpenAI-compatible endpoints, and similar) and is not supported for Bedrock, Gemini Enterprise Agent Platform, or Google GenAI, which authenticate with native cloud identity. The toggle is also hidden for the **LangServe (Deprecated)** preset.

### Configure OAuth on a model configuration

Configuring OAuth requires the [Workspace Admin](../../Users%20%26%20access%20control/Role-based%20access%20control.md#workspace-admin) role, or a [custom role](../../Users%20%26%20access%20control/Role-based%20access%20control.md#custom-roles) with the `workspaces:manage-model-configs` permission. Members without it see the OAuth fields disabled, with a masked secret hint. In the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-model-configurations):

1. Navigate to **Settings** > **Model configurations** and either click **+ Create** or open an existing row through the overflow menu  > **Edit**.
2. Select a compatible provider and configure model parameters as usual.
3. Toggle **Use Custom OAuth** on.
4. Fill the OAuth fields:
   * **Token URL**: the IdP token endpoint, for example `https://login.example.com/oauth/token`.
   * **Client ID**: the OAuth client identifier.
   * **Client Secret**: the OAuth client secret. Encrypted at rest.
   * **Token Endpoint Auth Method**: `client_secret_basic` or `client_secret_post`.
   * **Extra parameters**: key/value rows sent in the token request body. Use these rows for `scope`, `audience`, `resource`, or any other parameter the IdP expects. Add one row per value when sending multiple scopes; duplicate keys are sent as multi-value pairs.
   * **Extra headers**: additional headers sent with the token request. Reserved headers such as `Authorization` are rejected at save time.
5. Click **Save**.

![Model configuration Create modal in LangSmith Settings with Use Custom OAuth toggled on, showing Token URL, Client ID, masked Client Secret, and Token Endpoint Auth Method set to HTTP Basic.](../../../../../assets/images/95df9f0df49c-model-config-oauth-create-light.png)

### Edit semantics

OAuth fields follow edit behaviors that protect the stored secret:

* **Secret round-trip**: the server returns the secret as `********`. The input renders empty with a *"Secret is set. Type to replace."* hint. Submitting without retyping leaves the stored secret unchanged.
* **Toggle off preserves credentials**: switching **Use Custom OAuth** off deactivates the OAuth flow but keeps the stored fields. Toggling back on resumes using the same credentials.
* **Clear a field**: edit the configuration and blank the field to clear it explicitly.
* **Clone via Save as preset**: when you save a one-off configuration as a new preset, non-secret OAuth fields copy into the new row. The secret cannot transfer because it is never exposed for read, so OAuth is force-disabled on the clone until you re-enter the secret.

### How a request flows

When a request runs against an OAuth-enabled configuration, LangSmith mints a bearer through an internal broker, caches the result, and stamps the bearer on every outbound LLM call until the cached token expires.

```mermaid actions={false}
sequenceDiagram
    autonumber
    participant Caller as LangSmith service<br/>(Playground, Evals, Insights, Chat, Fleet)
    participant Broker as Token broker
    participant Cache as Redis cache
    participant IdP as Customer IdP
    participant LLM as Upstream LLM provider

    Caller->>Broker: Mint token for configuration X
    Broker->>Cache: Lookup cached token for X
    alt Cache hit
        Cache-->>Broker: Cached token
    else Cache miss or expired
        Broker->>IdP: client_credentials grant
        IdP-->>Broker: access_token + expires_in
        Broker->>Cache: Store until expiry
    end
    Broker-->>Caller: access_token
    Caller->>LLM: Request with Authorization: Bearer <token>
    LLM-->>Caller: Response
```

Routing between OAuth and the [LLM auth proxy](../../../Self-hosted/Configure%20an%20instance/Set%20up%20the%20LLM%20auth%20proxy.md) is per-configuration, not per-organization. Each request resolves to OAuth or the LLM auth proxy based on the configuration's OAuth state. A single multi-model job (for example, [Insights](../../../../Monitor/Observe/Monitoring%20%26%20alerting/Discover%20errors%20and%20usage%20patterns%20with%20Insights.md) with separate Thinking and Summarization models) can mix the two flows because each model is resolved independently.

### Fallback behavior

If the broker cannot mint a token (IdP unreachable, credentials invalid, configuration deleted between request preparation and execution), the request falls back to the static workspace API key for the provider. If no workspace key is set, expect a provider 401 on the outbound call.

Token rotation propagates only after the cached bearer expires. Plan rotations around the access token TTL configured at the IdP.

### Surface coverage

OAuth-enabled configurations are honored wherever model configurations are consumed:

* [**Playground**](../../../../Deploy/Prompt%20%26%20Context%20Hub/Prompts/Prompt%20engineering%20concepts.md): chat runs and experiment runs.
* [**Evaluators**](../../../../Test/Get%20started/LangSmith%20Evaluation.md): LLM-as-judge configuration, Reuse, Preview Test, and Evaluator Details Test all skip the workspace-secrets prompt when every prompt resolves to an OAuth-enabled configuration.
* [**Insights**](../../../../Monitor/Observe/Monitoring%20%26%20alerting/Discover%20errors%20and%20usage%20patterns%20with%20Insights.md): Thinking and Summarization configurations are resolved independently.
* [**Chat**](../../../../Test/Datasets%20%26%20Experiments/Analyze%20experiment%20results/LangSmith%20Chat.md)
* [**Fleet**](../../../../No-code%20agents/Fleet/No-code%20agents%20with%20LangSmith%20Fleet.md)

When OAuth is enabled on a configuration, LangSmith does not prompt for a workspace secret for that configuration, because the broker supplies the credential at request time.

The [LLM Gateway](../../../../LLM%20Gateway/Models%20and%20reliability/Custom%20model%20configurations.md) does not use OAuth client credentials. A `custom/<name>` gateway request authenticates with the configuration's API key secret.

### Security and audit

* **Encryption at rest**: client secrets are Fernet-encrypted with the same derivation used for [workspace secrets](../Overview.md#workspaces).
* **Bearer caching**: access tokens are cached until expiry and are never written to logs.

### FAQ

> [accordion] Can a single set of OAuth credentials be shared across workspaces?
>
> No. OAuth credentials are stored on the model configuration, which is workspace-scoped. Each workspace enters its own credentials, even when the credentials point at the same IdP client.

> [accordion] Why is my OAuth-enabled configuration suddenly using a static workspace key?
>
> If the broker cannot mint a bearer (IdP unreachable, credentials invalid, configuration deleted between request preparation and execution), the request falls back to the static workspace API key for the provider. Re-open the model configuration and verify the Token URL is reachable, the Client ID and secret are current, and the Token Endpoint Auth Method matches what your IdP expects.

> [accordion] How do I rotate the client secret?
>
> Edit the model configuration and retype the secret in the **Client Secret** field. The previous secret is overwritten on save. The Redis-cached bearer continues to work until its TTL expires, after which the broker mints a new bearer using the rotated secret.

> [accordion] Can OAuth and the LLM auth proxy be used together?
>
> Yes. Routing is per-configuration. Configurations with OAuth enabled use OAuth; configurations without it fall through to the LLM auth proxy when the proxy is enabled at the organization level. A single multi-model job can mix the two flows.

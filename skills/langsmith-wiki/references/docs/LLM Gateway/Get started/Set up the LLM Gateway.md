# Set up the LLM Gateway

> Set up the LLM Gateway for your organization by adding provider keys, granting permission to call the gateway, issuing API keys, and setting governance policies.

> [!NOTE]
>
> The LLM Gateway is in [beta](../../LangSmith%20setup/Cloud/Reference/Release%20stages.md).

This page walks an admin through preparing the [LLM Gateway](LLM%20Gateway.md) for their organization: connecting providers, granting access, issuing API keys, and setting policies. Complete the following sections in order. Each one links to the page that covers its topic in full.

> [!TIP]
>
> Some users can start without this setup. A [Workspace Admin](../../LangSmith%20setup/Govern/Users%20%26%20access%20control/Role-based%20access%20control.md#workspace-admin) can already call the gateway, and can add a provider key from the Simulator's **Needs key** prompt. If you are the only user in your organization, go to [Send your first LLM Gateway request](Send%20your%20first%20LLM%20Gateway%20request.md) instead.

## Enable the gateway on self-hosted LangSmith

On self-hosted LangSmith, [enable the gateway in the Helm chart](../../LangSmith%20setup/Self-hosted/Install%20an%20instance/Additional%20features/Enable%20the%20LLM%20Gateway.md) before the other steps. Skip this section on other deployments.

## Add provider keys

Adding a provider key requires [permission to manage secrets](../../LangSmith%20setup/Govern/Users%20%26%20access%20control/Role-based%20access%20control.md#workspace-roles) in that workspace.

The gateway calls each provider with a key stored as a secret in the workspace that the caller's API key belongs to. Add a key for each provider you route requests to, in each workspace whose API keys send those requests. The gateway does not fall back to organization secrets for these calls.

Skip this section if you route requests only to [Gateway Credits](../Models%20and%20reliability/Gateway%20Credits.md) models, which need no provider key.

For the steps and the secret name each provider uses, see [Add a provider key](../Authentication/Provider%20authentication.md#add-a-provider-key).

## Grant permission to call the gateway

An API key needs the `gateway:invoke` and `workspaces:read` permissions to call the gateway. On plans without workspace roles, every user has the Workspace Admin role, which includes both, so no action is needed.

On the Enterprise plan, the built-in Workspace Editor and Workspace Viewer roles include neither permission. As an [Organization Admin](../../LangSmith%20setup/Govern/Users%20%26%20access%20control/Role-based%20access%20control.md#organization-admin), create a [custom role](../../LangSmith%20setup/Govern/Users%20%26%20access%20control/Role-based%20access%20control.md#custom-roles) with both permissions and assign it to the users who call the gateway, or assign them the Workspace Admin role.

For more information, see [Grant permission to call the gateway](../Authentication/Authenticate%20to%20the%20LLM%20Gateway.md#grant-permission-to-call-the-gateway).

## Decide how developers get API keys

Each request authenticates with a workspace-scoped LangSmith API key. Developers can create their own personal access token (PAT), which carries their role, or the Simulator creates one for them. For shared agents or a company-wide rollout through mobile device management (MDM), you can create service keys instead.

The key type also determines how the **Usage** tab can attribute spend. Requests made with a personal access token count toward a user, while requests made with a service key count only toward the key. If you plan to charge back LLM costs, see [Attribute spend for chargebacks](../Observability/Monitor%20LLM%20Gateway%20spend.md#attribute-spend-for-chargebacks) before you issue keys.

For key types and scoping, see [Choose a key type](../Authentication/Authenticate%20to%20the%20LLM%20Gateway.md#choose-a-key-type). For coding agent rollouts, see [Set up coding agents](../Call%20the%20gateway/Set%20up%20coding%20agents.md).

## Optional: Set policies

Creating policies requires the `organization:gateway:manage` permission, which Organization Admins and Organization Operators have by default. On self-hosted LangSmith earlier than application version 0.18.9 (Helm chart versions before 0.18.0-rc.22), it requires `organization:manage` instead.

Use the tabs on the **LLM Gateway** page to create any of these policy types:

* **[Spend limits](../Governance/Spend%20policies.md)**: Hard caps at the organization, workspace, API key, or user level. Your organization may already have a default limit on the **Cost Controls** tab.
* **[Rate limits](../Governance/Rate%20limit%20policies.md)**: Request or token limits in a time window.
* **[Model access](../Governance/Model%20access%20policies.md)**: Which models users can call.
* **[Header-based policies](../Governance/Header-based%20policies.md)**: Spend caps, rate limits, and model access scoped by a custom request header, such as a customer, tenant, or cost center identifier.
* **[Data policies](../Governance/Data%20policies.md)**: Detect and redact PII and secrets before they reach the model, and control whether request and response bodies are traced.

On the Enterprise plan, creating, updating, and deleting policies is recorded in [audit logs](../../LangSmith%20setup/Govern/Auditing/Audit%20logs.md).

## Send a test request

To confirm the setup, follow [Send your first LLM Gateway request](Send%20your%20first%20LLM%20Gateway%20request.md). It sends a request from the Simulator and from code, and shows its trace. Share the same page with developers as their starting guide.

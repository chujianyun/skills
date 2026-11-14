# Model access policies

> Control which model providers and models are accessible through the LLM Gateway for your organization, workspaces, users, or API keys.

> [!NOTE]
>
> The LLM Gateway is in [beta](../../LangSmith%20setup/Cloud/Reference/Release%20stages.md).

A model access policy defines which providers and models are permitted through the [LLM Gateway](../Get%20started/LLM%20Gateway.md). The gateway blocks requests for providers or models the policy does not include, returning a `403` response with a body that names the blocking policy:

```json
{"error":{"code":null,"message":"request blocked by gateway policies: <POLICY_NAME>","param":null,"type":"permission_error"}}
```

If no policy applies, all providers and models are available.

## Policy dimensions

A model access policy is scoped to one subject tier:

| Scope | Applies to |
| - | - |
| **Organization** | All users and workspaces in the organization |
| **Workspace** | All users in a workspace |
| **User** | A single user |
| **API key** | A single API key |

### Policy overrides

Policy overrides let you grant a more specific subject different access than the broader default. A common case is giving one API key access to a premium model that is not available to the rest of the organization.

When a request matches policies at multiple tiers, only the most specific tier applies, in the order API key, user, workspace, then organization. The more specific policy replaces the broader one entirely. For example, if the organization policy permits OpenAI and Anthropic, and an API key policy permits only OpenAI and Gemini, requests using that key can access OpenAI and Gemini only.

If multiple policies match at the same tier, a model must be permitted by all of them to be accessible. The error names only the policy that rejected the model.

## Allowed providers and models

A model access policy lists one or more providers, each with an access mode:

* **All models**: Every model the provider offers is permitted.
* **Selected models**: Only the models you specify are permitted. At least one model is required.

Under **Selected models**, the gateway also blocks a request whose model it cannot read, such as a request with no `model` field, a `model` that is not a string, or a `model` field sent twice.

### Allow saved model configurations

Requests that call a saved [model configuration](../Models%20and%20reliability/Custom%20model%20configurations.md) through a `custom/<name>` model ID or a fallback chain are blocked unless the policy lists the **Model configurations** provider. This provider uses the same two access modes, but **Selected** takes configuration names, matched exactly, instead of model IDs. Names resolve in the workspace of the calling API key, so one entry on an organization-level policy applies to each workspace's own configurations.

## Create a model access policy

> [!WARNING]
>
> Creating and managing policies requires `organization:gateway:manage` permission. Organization Admins and Organization Operators have it by default. For what each organization role can do, see [Organization roles](../../LangSmith%20setup/Govern/Users%20%26%20access%20control/Role-based%20access%20control.md#organization-roles).

1. Go to **LLM Gateway** and select the **Model Access** tab.
2. Click **Create model access**.
3. Under **Applies to**, select the scope (organization, workspace, user, or API key).
4. Under **Allowed providers and models**, turn on each provider to permit and choose its access mode. Providers are off by default, so any provider you leave off is blocked.
5. Click **Create model access**.

Policies take effect immediately.

## See also

* [Run a request in the Simulator](../Get%20started/Send%20your%20first%20LLM%20Gateway%20request.md#run-a-request-in-the-simulator): test a policy by requesting a model it blocks.
* [Spend policies](Spend%20policies.md): set cost caps on LLM usage.
* [Rate limit policies](Rate%20limit%20policies.md): limit request or token throughput.
* [Header-based policies](Header-based%20policies.md): narrow a policy to requests that carry a specific custom request header value.
* [Data policies](Data%20policies.md): add data protection policies.

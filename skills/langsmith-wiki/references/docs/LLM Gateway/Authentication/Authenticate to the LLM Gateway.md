# Authenticate to the LLM Gateway

> Choose a LangSmith API key for LLM Gateway requests, grant it permission to call the gateway, send it from your client, and fix authentication errors.

> [!NOTE]
>
> The LLM Gateway is in [beta](../../LangSmith%20setup/Cloud/Reference/Release%20stages.md).

Every request to the [LLM Gateway](../Get%20started/LLM%20Gateway.md) authenticates with a LangSmith API key, never with a model provider's key. This page covers which key to use, the permission it needs, and how each client sends it.

## Understand the two layers

A gateway request passes two separate authentication checks:

* **Your client to the gateway**: your code sends a LangSmith API key, which starts with `lsv2_`. The gateway checks the key's permissions, then applies your organization's policies.
* **The gateway to the provider**: the gateway calls the model provider with a credential stored in LangSmith, usually a provider API key saved as a workspace secret. Your code never holds this credential. For the credential types each provider accepts, see [Provider authentication](Provider%20authentication.md).

## Choose a key type

Two kinds of [LangSmith API key](../../LangSmith%20setup/Account/Create%20an%20account%20and%20API%20key.md) can call the gateway:

* **[Personal access token (PAT)](../../LangSmith%20setup/Govern/Organization/Overview.md#personal-access-tokens-pats)**: prefixed `lsv2_pt_`. A PAT carries the permissions of the user who created it. The Simulator's **Create Gateway Key** button creates a PAT.
* **[Service key](../../LangSmith%20setup/Govern/Organization/Overview.md#service-keys)**: prefixed `lsv2_sk_`. A service key belongs to the organization rather than a user. On the [Enterprise plan](https://docs.langchain.com/langsmith/pricing-plans.md), you can assign a service key its own workspace role.

> [!TIP]
>
> The key type changes how [spend limits](../Governance/Spend%20policies.md) apply. A user-scoped spend limit applies to requests made with that user's PATs. It does not apply to requests made with a service key, even one the same user created. To cap a service key, create a spend limit scoped to that API key.

## Grant permission to call the gateway

To call the gateway, an API key needs both `gateway:invoke` and `workspaces:read` in the workspace it belongs to. A PAT has these permissions when its user's role does.

Which roles include them depends on your plan:

* **Plans without [workspace roles](../../LangSmith%20setup/Govern/Users%20%26%20access%20control/Role-based%20access%20control.md#workspace-roles)**: every user has the Workspace Admin role, which includes both permissions. No setup is needed.
* **Enterprise plan**: the Workspace Admin role includes both permissions. The built-in Workspace Editor and Workspace Viewer roles include neither, and built-in roles cannot be edited. To grant gateway access without full admin rights, create a [custom role](../../LangSmith%20setup/Govern/Users%20%26%20access%20control/Role-based%20access%20control.md#custom-roles) with `gateway:invoke` and `workspaces:read`, and assign it to the users who call the gateway.

For a service key with its own role, grant the same two permissions to that role. A service key whose role lacks `gateway:invoke` gets a `403` with `missing permission gateway:invoke`.

## Use a workspace-scoped key

Use a LangSmith API key scoped to one workspace. That workspace determines which provider secrets the gateway reads, which policies apply, and where traces land. For a PAT, this is the key's default workspace. A key created in the Simulator belongs to the workspace that was open when you created it. Organization-scoped keys are not supported for gateway requests.

## Send the key

The gateway accepts the key in any of these headers:

* `Authorization: Bearer <key>`
* `X-Api-Key: <key>`
* `X-Goog-Api-Key: <key>`

Each client sends its API key in one of these headers, so you set the key where the client expects its provider key:

| Client | Where to set the LangSmith API key | Header the client sends |
| - | - | - |
| cURL or any HTTP client | The header itself | `Authorization: Bearer` |
| OpenAI SDK, Codex | `api_key` or `OPENAI_API_KEY` | `Authorization: Bearer` |
| Anthropic SDK, Claude Code | `api_key` or `ANTHROPIC_API_KEY` | `X-Api-Key` |
| Google Gen AI SDK, Gemini CLI | `api_key` or `GEMINI_API_KEY` | `X-Goog-Api-Key` |

Claude Code with a [Claude subscription](../Call%20the%20gateway/Set%20up%20coding%20agents.md#use-claude-subscription-oauth) is the exception: its `Authorization` header carries the Anthropic OAuth token, so it sends the LangSmith API key in `X-Api-Key` through `ANTHROPIC_CUSTOM_HEADERS`.

For base URLs and request examples, see [API formats](../Call%20the%20gateway/API%20formats.md) and [Direct model access](../Call%20the%20gateway/Direct%20model%20access.md).

## Set environment variables

[LangChain](https://docs.langchain.com/oss/python/langchain/overview.md) chat models and [Deep Agents](https://docs.langchain.com/oss/python/deepagents/overview.md) read the key from the environment:

* `LANGSMITH_API_KEY`: the LangSmith API key, also used for tracing.
* `LANGSMITH_GATEWAY`: set to `true` to send supported chat models through the gateway. For details, see [Direct model access](../Call%20the%20gateway/Direct%20model%20access.md#configure-langchain-and-deep-agents).
* `LANGSMITH_GATEWAY_API_KEY`: an override for gateway requests when they need a different key from `LANGSMITH_API_KEY`. It must meet the same requirements: workspace-scoped, with `gateway:invoke`.

[Deep Agents Code](https://docs.langchain.com/oss/deepagents/code/overview.md) requires `LANGSMITH_GATEWAY_API_KEY`, even when it holds the same key as `LANGSMITH_API_KEY`. With only `LANGSMITH_API_KEY` set, it stops at startup with `No credentials found for provider`.

## Fix authentication errors

| Status and response | Cause | Fix |
| - | - | - |
| `401` with `{"error":"Unauthorized"}` | The request reached the gateway without a LangSmith API key, for example with a provider key (`sk-...`) in its place. | Send your LangSmith API key in place of the provider key. |
| `401` from the provider, such as OpenAI's `Incorrect API key provided: lsv2_pt_***` or Anthropic's `invalid x-api-key` | The client sent your LangSmith API key straight to the provider, because it is not using the gateway base URL. | Set the client's base URL to the gateway. |
| `403` with `{"error":"Forbidden"}` | The LangSmith API key is invalid. | Check that you copied the whole key, or create a new one. |
| `403` with `{"error":"API key has expired"}` | The LangSmith API key has passed its expiry date. | Create a new key. |
| `403` with `missing permission gateway:invoke` | The key's role lacks `gateway:invoke`. | Ask an admin to [grant the permission](#grant-permission-to-call-the-gateway). |

For a `424`, an error that shows a masked provider key, or an Anthropic `invalid x-api-key` when your base URL already points at the gateway, the problem is the provider key stored in LangSmith, not your API key. See [Fix provider credential errors](Provider%20authentication.md#fix-provider-credential-errors).

Requests that a policy blocks return `402` for a [spend limit](../Governance/Spend%20policies.md) and `429` for a [rate limit](../Governance/Rate%20limit%20policies.md). The response body names the policy, for example `{"type":"error","error":{"message":"request blocked by gateway policies: <POLICY_NAME>"}}`.

## See also

* [Provider authentication](Provider%20authentication.md): store the credentials the gateway uses to call each provider.
* [Set up the LLM Gateway](../Get%20started/Set%20up%20the%20LLM%20Gateway.md): set up provider keys, permissions, and policies for your organization.
* [Create a LangSmith API key](../../LangSmith%20setup/Account/Create%20an%20account%20and%20API%20key.md): create a PAT or service key.

# How the LLM Gateway works

> Understand what the LLM Gateway does to each request, how upstream credentials are resolved, and where the gateway is available.

> [!NOTE]
>
> The LLM Gateway is in [beta](../../LangSmith%20setup/Cloud/Reference/Release%20stages.md).

The LLM Gateway sits between your application and the model providers your workspace has configured. It authenticates the caller, selects an upstream route, applies governance policies, translates between API formats, and traces the result.

## Follow a request through the gateway

The gateway performs these steps for each request to the standard endpoint. The provider keys, permissions, and policies it applies come from [setting up the gateway](Set%20up%20the%20LLM%20Gateway.md).

1. **Authenticate and authorize the caller** from the LangSmith API key, including the `gateway:invoke` permission check. For details, see [Authenticate to the LLM Gateway](../Authentication/Authenticate%20to%20the%20LLM%20Gateway.md).
2. **Resolve the route** from the endpoint and the model ID, including any configured [fallback candidates](../Models%20and%20reliability/Model%20fallbacks.md).
3. **Load the upstream credential**, such as a workspace provider key or a [Gateway Credits](../Models%20and%20reliability/Gateway%20Credits.md) credential. For details, see [Provider authentication](../Authentication/Provider%20authentication.md).
4. **Evaluate pre-request policies.** [Spend](../Governance/Spend%20policies.md), [rate](../Governance/Rate%20limit%20policies.md), and [model access](../Governance/Model%20access%20policies.md) limits can block the request. [Data protection policies](../Governance/Data%20policies.md) run against the request body and redact it when configured.
5. **Translate the request** when the selected provider uses a different API format. For details, see [Understand translation behavior](../Call%20the%20gateway/API%20formats.md#understand-translation-behavior).
6. **Send the request upstream** and receive or stream the provider response.
7. **Translate the response** back into the API format the client requested, and restore redaction placeholders where applicable.
8. **Return the response** to the caller, recording usage, cost, routing and policy metadata, and the LangSmith trace. For details, see [View LLM Gateway traces](../Observability/View%20LLM%20Gateway%20traces.md).

[Direct model access](../Call%20the%20gateway/Direct%20model%20access.md) skips steps 5 and 7. The gateway still authenticates, resolves credentials, evaluates policies, and traces the call, but it passes the request and response through in the provider's native format.

## Choose how credentials are managed

The gateway resolves an upstream credential for every call. A workspace can use its own provider keys, Gateway Credits, or both. For every credential source and who bills it, see [Provider authentication](../Authentication/Provider%20authentication.md#choose-a-credential-source).

## Understand workspace scope

A request uses the settings of the workspace that its API key belongs to. Gateway settings differ in scope:

* **Provider keys**: workspace secrets. Each workspace that calls a provider needs its own key.
* **Fallback chains**: created in one workspace, and they apply to requests from that workspace's API keys. See [Model fallbacks](../Models%20and%20reliability/Model%20fallbacks.md).
* **Traces**: recorded in the workspace of the API key that made the request.
* **Model configurations**: workspace or organization scope. Organization-scoped configurations read organization secrets. See [Custom model configurations](../Models%20and%20reliability/Custom%20model%20configurations.md).
* **Policies**: each [spend limit](../Governance/Spend%20policies.md), [rate limit](../Governance/Rate%20limit%20policies.md), [model access policy](../Governance/Model%20access%20policies.md), and [data policy](../Governance/Data%20policies.md) applies to the whole organization, one workspace, one user, or one API key.

## Check availability

The gateway runs on:

* LangSmith Cloud in every LangSmith region
* [Bring your own cloud (BYOC)](../../LangSmith%20setup/BYOC/Bring%20Your%20Own%20Cloud%20%28BYOC%29.md), where it runs inside your data plane so that model requests and their traces stay in your VPC
* [Self-hosted](../../LangSmith%20setup/Self-hosted/Self-hosted%20LangSmith.md) LangSmith

All three use the same API formats, model IDs, policies, and tracing. Only the hostname and path prefix differ. On self-hosted LangSmith earlier than application version 0.18.9 (Helm chart versions before 0.18.0-rc.22), managing policies requires `organization:manage` instead of `organization:gateway:manage`.

### Use a regional gateway

Replace `gateway.smith.langchain.com` with the hostname for your LangSmith region, and keep the same path for the API format you use:

| Region | Gateway hostname |
| - | - |
| GCP US | `gateway.smith.langchain.com` |
| GCP EU | `eu.gateway.smith.langchain.com` |
| GCP APAC | `apac.gateway.smith.langchain.com` |
| AWS US | `aws.gateway.smith.langchain.com` |

> [!NOTE]
>
> API keys from one region do not work on another region's gateway.

### Use a BYOC data plane

On BYOC, replace the gateway hostname with your [data plane endpoint](../../LangSmith%20setup/BYOC/BYOC%20usage.md#find-your-data-plane-endpoint) and prefix the path with `/gateway`:

| API format | Base URL | Prompt endpoint |
| - | - | - |
| OpenAI Chat Completions | `https://<data_plane_host>/gateway/v1` | `POST /chat/completions` |
| Anthropic Messages | `https://<data_plane_host>/gateway` | `POST /v1/messages` |
| OpenAI Responses | `https://<data_plane_host>/gateway/v1` | `POST /responses` |

Authenticate with an API key scoped to a workspace in that data plane, sent in any header listed in [Send the key](../Authentication/Authenticate%20to%20the%20LLM%20Gateway.md#send-the-key). Provider secrets, model IDs, policies, and tracing behave the same as on Cloud.

> [!WARNING]
>
> Data planes are provisioned with a private endpoint by default, so you need private connectivity to reach the base URL, such as Tailscale, AWS PrivateLink, or VPC peering.

### Use a self-hosted installation

On self-hosted LangSmith, an administrator first [enables the gateway in the Helm chart](../../LangSmith%20setup/Self-hosted/Install%20an%20instance/Additional%20features/Enable%20the%20LLM%20Gateway.md). Then replace the gateway hostname with your LangSmith hostname and prefix the path with `/gateway`:

| API format | Base URL | Prompt endpoint |
| - | - | - |
| OpenAI Chat Completions | `https://<your-hostname>/gateway/v1` | `POST /chat/completions` |
| Anthropic Messages | `https://<your-hostname>/gateway` | `POST /v1/messages` |
| OpenAI Responses | `https://<your-hostname>/gateway/v1` | `POST /responses` |

Authenticate with an API key scoped to a workspace in your installation, sent in any header listed in [Send the key](../Authentication/Authenticate%20to%20the%20LLM%20Gateway.md#send-the-key).

## See also

* [Send your first LLM Gateway request](Send%20your%20first%20LLM%20Gateway%20request.md): make your first request and view its trace.
* [Set up the LLM Gateway](Set%20up%20the%20LLM%20Gateway.md): add provider keys, grant developer access, and set policies.
* [API formats](../Call%20the%20gateway/API%20formats.md): use Chat Completions, Messages, or Responses through the standard endpoint.
* [View LLM Gateway traces](../Observability/View%20LLM%20Gateway%20traces.md): see where gateway traces appear and who can view them.

# API formats

> Use OpenAI Chat Completions, Anthropic Messages, or OpenAI Responses requests to call models across providers through the LLM Gateway.

> [!NOTE]
>
> The LLM Gateway is in [beta](../../LangSmith%20setup/Cloud/Reference/Release%20stages.md).

The standard LLM Gateway API supports three request and response formats. Choose the format your application already uses. Then call models with your own provider keys or Gateway Credits through the same endpoint.

## Compare API formats

On LangSmith Cloud in the US region, each format uses the following base URL and endpoint. For other regions, BYOC data planes, and self-hosted installations, see [Check availability](../Get%20started/How%20the%20LLM%20Gateway%20works.md#check-availability).

| API format | Base URL | Prompt endpoint | Common clients |
| - | - | - | - |
| OpenAI Chat Completions | `https://gateway.smith.langchain.com/v1` | `POST /chat/completions` | OpenAI SDK and most OpenAI-compatible tools |
| Anthropic Messages | `https://gateway.smith.langchain.com` | `POST /v1/messages` | Anthropic SDK, [Claude Code](Set%20up%20coding%20agents.md) |
| OpenAI Responses | `https://gateway.smith.langchain.com/v1` | `POST /responses` | OpenAI SDK, [Codex](Set%20up%20coding%20agents.md) |

> [!TIP]
>
> All formats authenticate with a workspace-scoped LangSmith API key. For key types, permissions, and the header each client sends, see [Authenticate to the LLM Gateway](../Authentication/Authenticate%20to%20the%20LLM%20Gateway.md).

## Understand translation behavior

The endpoint determines the format your application sends and receives. The model ID determines the upstream provider.

* When the provider supports the selected format natively, the gateway preserves that format.
* Otherwise, the gateway translates the request into a format supported by the provider and translates the response back, including streaming responses.
* Translation can reject fields that cannot be represented in the target provider format. Use [direct model access](Direct%20model%20access.md) when provider-native behavior is required.

Every request resolves the same provider secrets, policies, and tracing configuration regardless of format.

### Use prompt caching

How you request prompt caching depends on the format you send and the model you call:

* **OpenAI models**: OpenAI caches prompts automatically. To control cache lifetime or breakpoints, use OpenAI's caching fields, such as `prompt_cache_options` or `prompt_cache_retention`. Which fields and values each model accepts is set by OpenAI. For details, see the [OpenAI prompt caching guide](https://developers.openai.com/api/docs/guides/prompt-caching).
* **Anthropic models in Messages format**: Use Anthropic's `cache_control` field. For details, see the [Anthropic prompt caching guide](https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching).
* **Anthropic models in Chat Completions or Responses format**: Set any of `prompt_cache_options`, `prompt_cache_retention`, or `prompt_cache_key`. The gateway turns on Anthropic prompt caching with Anthropic's default five-minute cache lifetime. It does not carry over a requested lifetime, retention, or breakpoint mode.
* **OpenAI models in Messages format**: The gateway drops `cache_control` fields. OpenAI's automatic caching still applies.

## Send a request

Each format has its own request shape. For example, Chat Completions takes `messages`, Responses takes `input`, and Messages requires `max_tokens`. Replace `<MODEL_ID>` with a [model ID](#choose-a-model-id):

```bash Chat Completions
curl https://gateway.smith.langchain.com/v1/chat/completions \
    -H "Authorization: Bearer $LANGSMITH_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"model":"<MODEL_ID>","messages":[{"role":"user","content":"Hello!"}]}'
```

```bash Messages
curl https://gateway.smith.langchain.com/v1/messages \
    -H "Authorization: Bearer $LANGSMITH_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"model":"<MODEL_ID>","max_tokens":1024,"messages":[{"role":"user","content":"Hello!"}]}'
```

```bash Responses
curl https://gateway.smith.langchain.com/v1/responses \
    -H "Authorization: Bearer $LANGSMITH_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"model":"<MODEL_ID>","input":"Hello!"}'
```

For the full request and response schemas, see the [OpenAI Chat Completions API](https://platform.openai.com/docs/api-reference/chat), the [Anthropic Messages API](https://docs.anthropic.com/en/api/messages), and the [OpenAI Responses API](https://platform.openai.com/docs/api-reference/responses).

> [!TIP]
>
> For the same request in Python or TypeScript, open the **Simulator** tab in the **LLM Gateway**, select the format and language, then click the copy icon. The copied code already uses your deployment's gateway URL. For details, see [Send your first LLM Gateway request](../Get%20started/Send%20your%20first%20LLM%20Gateway%20request.md).

## Choose a model ID

The model ID selects the provider and the credential that pays for the call. Model IDs work the same way in every format:

* **Your own provider key**: `<provider>/<model>`, such as `openai/gpt-5.4-mini` or `azure/<deployment-name>`. The gateway calls the provider with the [provider key](../Authentication/Provider%20authentication.md) stored in your workspace.
* **Gateway Credits**: a hosted model slug, such as `moonshotai/kimi-k3`. [Gateway Credits](../Models%20and%20reliability/Gateway%20Credits.md) bill LangChain-hosted models to your LangSmith account, with no provider key required.
* **Saved model configuration**: `custom/<name>`. The gateway uses the provider, model, and credentials from the saved [model configuration](../Models%20and%20reliability/Custom%20model%20configurations.md).

### List models

Call `GET /v1/models` to list the model IDs your workspace can call. The gateway returns a single OpenAI-compatible list:

```bash
curl https://gateway.smith.langchain.com/v1/models \
    -H "Authorization: Bearer $LANGSMITH_API_KEY"
```

```json
{
  "object": "list",
  "data": [
    {"id": "openai/gpt-5.4-mini", "object": "model"},
    {"id": "fireworks/accounts/fireworks/models/glm-5p2", "object": "model"},
    {"id": "anthropic/claude-opus-5", "object": "model"},
    {"id": "moonshotai/kimi-k3", "object": "model"}
  ]
}
```

Pass an ID exactly as shown. The list omits providers without a configured provider key and models that your [model access policies](../Governance/Model%20access%20policies.md) block. Saved model configurations do not appear in the list.

## Read response metadata

The gateway adds an `X-LangSmith-Gateway-Metadata` header to its responses. The header is a JSON object that describes how the gateway handled the request, such as the provider and model it called and whether a policy blocked the request. It contains no credentials or prompt and response content.

To tell a gateway decision from a provider error, read two fields: `outcome` says how the request ended, such as `success`, `blocked`, or `upstream_error`, and `error_source` says whether a failure came from the caller (`request`), the provider (`upstream`), or the gateway (`internal`). When a [fallback chain](../Models%20and%20reliability/Model%20fallbacks.md#investigate-fallback-attempts) runs, the header also lists each attempt.

LangChain chat models in Python (`langchain-openai>=1.6.7` or `langchain-anthropic>=1.7.5`) attach the header to the model's run, so with [tracing](../../Monitor/Overview/LangSmith%20Observability.md) on, the same details appear in the run's **Gateway** section.

## Fix request errors

| Status or symptom | Meaning |
| - | - |
| `400 Bad Request` | The request is malformed, the model ID is unavailable or incorrectly formatted, or the request cannot be translated. |
| `429 Too Many Requests` | A gateway [rate limit policy](../Governance/Rate%20limit%20policies.md) or an upstream provider rate limit was reached. |
| No models with a provider prefix appear in `GET /v1/models` | The provider may not be configured or may not have returned a model catalog. |

To tell whether the gateway or the provider returned an error, read the `outcome` and `error_source` fields in the [response metadata](#read-response-metadata).

> [!TIP]
>
> For `401` and `403` errors, see [Fix authentication errors](../Authentication/Authenticate%20to%20the%20LLM%20Gateway.md#fix-authentication-errors). For `424` errors, see [Fix provider credential errors](../Authentication/Provider%20authentication.md#fix-provider-credential-errors).

## See also

* [Send your first LLM Gateway request](../Get%20started/Send%20your%20first%20LLM%20Gateway%20request.md): make your first request and view its trace.
* [How the gateway works](../Get%20started/How%20the%20LLM%20Gateway%20works.md): what happens to each request, and which hostname to use in each region and on BYOC.
* [Direct model access](Direct%20model%20access.md): bypass format translation and use provider-native APIs.
* [Model fallbacks](../Models%20and%20reliability/Model%20fallbacks.md): retry requests against backup models.

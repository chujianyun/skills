# Send your first LLM Gateway request

> Send your first request through the LLM Gateway from the Simulator, call the gateway from your code, and view the request's trace.

> [!NOTE]
>
> The LLM Gateway is in [beta](../../LangSmith%20setup/Cloud/Reference/Release%20stages.md).

The [LLM Gateway](LLM%20Gateway.md) calls models across providers through one endpoint, authenticated with one [LangSmith API key](../../LangSmith%20setup/Account/Create%20an%20account%20and%20API%20key.md). Instead of copying each provider's key into every app, your code uses one key and switches providers by changing the model ID, while LangSmith traces every call and applies your organization's spend limits.

On this page, you send a request from the Simulator in the LangSmith UI and from your code. Then, view its trace in LangSmith.

> [!TIP]
>
> This page is for developers sending requests through the gateway. If you are setting up the gateway for your organization, start with [Set up the LLM Gateway](Set%20up%20the%20LLM%20Gateway.md).

## Before you begin

You need:

* **Membership in a LangSmith organization on a paid plan.** On the Developer plan, the Simulator offers only LangChain-hosted models, which bill [Gateway Credits](../Models%20and%20reliability/Gateway%20Credits.md) instead of using a provider key.
* **An API key for a model provider**, unless your workspace already has one. The Simulator shows which providers are already set up.

## Run a request in the Simulator

The Simulator sends a sample request through the gateway from your browser, so you can confirm your keys and model work before you change any code.

The gateway uses two keys:

* Your provider key stays in LangSmith as a [workspace secret](../Authentication/Provider%20authentication.md#add-a-provider-key). The gateway uses it to call the provider.
* Your gateway key is a LangSmith API key, starting with `lsv2_`, that your code sends to the gateway.

To run a request:

1. In [LangSmith](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-llm-gateway-first-request), go to **LLM Gateway** and select the **Simulator** tab.
2. Under **Model routing**, select a model. **Needs key** on a model tile means your workspace has no key for that provider yet.
3. Click **Run request**. If a key is missing, the Simulator prompts you for it before it sends the request.

The response appears below the request. If the request fails, note the error, and see [Troubleshoot](#troubleshoot).

## Send a request from your code

Compared with calling a provider directly, a gateway request changes two things:

* The base URL points at the gateway instead of the provider's API.
* The API key is your LangSmith API key instead of the provider's key.

To send a request:

1. Set your LangSmith API key and the gateway's base URL in your environment:

   ```bash
   export LANGSMITH_API_KEY="lsv2_..."
   export LANGSMITH_GATEWAY_BASE_URL="https://gateway.smith.langchain.com/v1"
   ```

   This is the US gateway. For another region, replace the hostname with your [regional gateway](How%20the%20LLM%20Gateway%20works.md#use-a-regional-gateway). On [BYOC](How%20the%20LLM%20Gateway%20works.md#use-a-byoc-data-plane), use your data plane URL followed by `/gateway/v1`. On [self-hosted LangSmith](../../LangSmith%20setup/Self-hosted/Install%20an%20instance/Additional%20features/Enable%20the%20LLM%20Gateway.md#make-your-first-call), use your LangSmith URL followed by `/gateway/v1`.

2. [List the models](../Call%20the%20gateway/API%20formats.md#list-models) you can call:

   ```bash
   curl "$LANGSMITH_GATEWAY_BASE_URL/models" \
       -H "Authorization: Bearer $LANGSMITH_API_KEY"
   ```

   Each `id` in the response is a model ID. The list reflects your workspace's provider keys and model access policies.

3. Send a request. Replace `<MODEL_ID>` with a chat model ID from the list, such as the model you tested in the Simulator:

   ```bash
   curl "$LANGSMITH_GATEWAY_BASE_URL/chat/completions" \
       -H "Authorization: Bearer $LANGSMITH_API_KEY" \
       -H "Content-Type: application/json" \
       -d '{"model":"<MODEL_ID>","messages":[{"role":"user","content":"Explain what an LLM gateway does in one sentence."}]}'
   ```

   A successful request returns a JSON response that contains a one-sentence answer. If it fails instead, see [Fix authentication errors](../Authentication/Authenticate%20to%20the%20LLM%20Gateway.md#fix-authentication-errors).

> [!TIP]
>
> This request uses the Chat Completions [API format](../Call%20the%20gateway/API%20formats.md). For the same request in Python or TypeScript, or in the Anthropic Messages or Responses format, select the format and language in the Simulator, then click the copy icon. The copied code already uses your deployment's gateway URL.

[LangChain](https://docs.langchain.com/oss/python/langchain/overview.md) chat models and [Deep Agents](https://docs.langchain.com/oss/python/deepagents/overview.md) need no code changes. Set `LANGSMITH_GATEWAY` to `true` alongside `LANGSMITH_API_KEY`, and every supported chat model in the process calls the gateway in its provider's native API format. For details, see [Direct model access](../Call%20the%20gateway/Direct%20model%20access.md#configure-langchain-and-deep-agents).

## View the trace

In the Simulator, click **View trace** next to the response. Requests from your code appear in the same **Traces** tab of **LLM Gateway**. By default, a trace records metadata such as token counts and cost. For more information, see [View LLM Gateway traces](../Observability/View%20LLM%20Gateway%20traces.md).

## Troubleshoot

For `401` and `403` errors, see [Fix authentication errors](../Authentication/Authenticate%20to%20the%20LLM%20Gateway.md#fix-authentication-errors). For `424` errors, see [Fix provider credential errors](../Authentication/Provider%20authentication.md#fix-provider-credential-errors).

The Simulator signals missing permissions without an error code:

| Symptom | Cause | Fix |
| - | - | - |
| No **Run request** button | You lack the `gateway:invoke` permission. | Ask a workspace admin to grant it. |
| The Simulator asks you to contact an admin | You lack permission to add provider keys. | Ask a workspace admin to add the provider key. |

## Next steps

Now that you can send requests through the gateway, explore its other capabilities:

* [Set a spend limit](../Governance/Spend%20policies.md): cap spend by organization, workspace, API key, or user.
* [Add model fallbacks](../Models%20and%20reliability/Model%20fallbacks.md): retry failed requests on backup models, and test the chain in the Simulator.
* [API formats](../Call%20the%20gateway/API%20formats.md): send Chat Completions, Messages, or Responses requests.
* [Set up coding agents](../Call%20the%20gateway/Set%20up%20coding%20agents.md): route Claude Code, Codex, Gemini CLI, or Deep Agents Code through the gateway.
* [Gateway Credits](../Models%20and%20reliability/Gateway%20Credits.md): call LangChain-hosted models without a provider key.

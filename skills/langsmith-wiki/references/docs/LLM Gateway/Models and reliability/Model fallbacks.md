# Model fallbacks

> Automatically retry a request against backup models when the primary model rate-limits, errors, or returns another configured status code.

> [!NOTE]
>
> The LLM Gateway is in [beta](../../LangSmith%20setup/Cloud/Reference/Release%20stages.md).

Model fallbacks in the LLM Gateway allow you to retry a request against one or more backup models when the primary model returns a configured error, such as a rate limit or provider outage.

Define the fallback order once in LangSmith, and then continue using the standard LLM Gateway endpoint and model ID in your application.

## Understand fallback behavior

### Chain components

A model fallback chain has:

* **A primary model**: the provider and model that trigger the chain when a request fails.
* **One to five fallbacks**: an ordered list of provider models or saved [model configurations](../../LangSmith%20setup/Govern/Organization/Workspace%20setup/Manage%20model%20configurations.md). A provider model uses the workspace's secret for that provider, or Gateway Credits for eligible hosted models.
* **Fallback triggers**: the HTTP status codes that move the request to the next model. The defaults cover rate-limit, overload, server, and request timeout errors, such as `408`, `429`, `500`, and `503`.
* **A time to first output**: how long each attempt can wait before the gateway moves to the next model. It is on by default at 120 seconds, and each attempt gets a fresh timer. Streaming requests in a [unified API format](../Call%20the%20gateway/API%20formats.md) wait for the first output. Non-streaming requests and [direct model access](../Call%20the%20gateway/Direct%20model%20access.md) requests wait for response headers.
* **A model cooldown** (optional): how many failures make the gateway skip a model, and for how long. It is off by default. See [Model cooldowns](#model-cooldowns) to learn more.

> [!TIP]
>
> Two statuses behave differently with fallbacks:
>
> * **`429` from a rate limit policy**: a [rate limit policy](../Governance/Rate%20limit%20policies.md) blocks a request before the gateway calls the primary model, so its `429` does not trigger the chain. Only a `429` from a provider does.
> * **`424` for a missing provider key**: the default triggers do not include `424`. Add it to let the chain skip a fallback that has no [provider key](../Authentication/Provider%20authentication.md#fix-provider-credential-errors) in the workspace. A primary model without a key returns `424` without trying the chain.

### Model cooldowns

A cooldown is a period during which the gateway skips a model in a fallback chain without calling it. Skipping a model that is likely to fail saves each request the latency of a failed attempt. A model enters a cooldown in two ways:

* **Provider rate limits**: when a provider returns `429`, the gateway skips that model for the retry delay in the provider's response. If the response sets no delay, the cooldown lasts 5 seconds. No cooldown lasts longer than 300 seconds. Every chain in the workspace whose triggers include `429` skips the model.
* **Model cooldown**: when you turn on **Model cooldown** for a chain, a model that fails the chain's triggers a set number of times within the cooldown period is skipped by that chain for the cooldown period. Trigger statuses, timeouts, and provider transport errors count as failures. Other statuses and canceled requests do not, and a success does not reset the count. Failures are counted per model in each chain, so other chains keep calling the model. When on, a model is skipped for 60 seconds after 3 failures by default. When the period ends, the gateway calls the model again, and its failure count starts over.

The last model in a chain is always called, even while it is cooling down.

### Request flow

For each request:

1. The gateway matches the request's provider-prefixed model ID to a fallback chain and calls the primary model.
2. If the attempt fails with a trigger status, times out, or hits a transport error, the gateway calls the next fallback in order.
3. The gateway repeats the previous step until one of the following:
   * A model succeeds.
   * A model returns a status that is not a trigger.
   * No fallbacks remain.
4. The gateway returns the last response in the API format used by the client.

Each attempt receives the original request, translated to the model's API format when needed. The gateway does not shorten the conversation to fit a fallback model's context window. Therefore, a model with a smaller context window can return `400`, which ends the chain unless `400` is a trigger status.

The gateway skips any model that is [cooling down](#model-cooldowns), except the last, without calling it. A skipped model does not appear in the response body. To see skipped models, [investigate the chain's attempts](#investigate-fallback-attempts).

Once a streaming response starts sending output, the gateway commits to that model and no longer falls back, even if the stream fails later.

> [!TIP]
>
> All attempts appear in one [gateway trace](../Observability/View%20LLM%20Gateway%20traces.md#read-the-trace-tree), under a `gateway.request` root run. A request that uses two fallbacks has three `gateway.attempt #N` child runs: the primary attempt and two fallback attempts.
>
> Each provider call contributes to [spend policies](../Governance/Spend%20policies.md) separately, but a content-logged request counts once toward trace billing, regardless of the number of attempts. A model skipped for cooldown still appears as a `gateway.attempt #N` run with `gateway.attempt.outcome` set to `skipped`, but it has no provider LLM run.

### Supported formats and endpoints

Fallbacks can use a different provider and API format than the primary model. The gateway translates requests and responses between [supported API formats](../Call%20the%20gateway/API%20formats.md). For example, an Anthropic primary can fall back to an OpenAI model without client-side changes.

Fallback chains apply to Chat Completions, Responses, and Messages requests, on both the unified endpoints and direct model access paths. Other endpoints, such as embeddings and Gemini `generateContent` requests through direct model access, call the requested model without a fallback.

## Create a fallback chain

> [!WARNING]
>
> Creating and managing fallback chains requires `organization:gateway:manage` permission. Organization Admins and Organization Operators have it by default. For what each organization role can do, see [Organization roles](../../LangSmith%20setup/Govern/Users%20%26%20access%20control/Role-based%20access%20control.md#organization-roles).

To create a fallback chain:

1. Go to **LLM Gateway**, and select the **Model Fallbacks** tab.
2. Click **Create fallback chain**.
3. Select the **Workspace** where the chain applies.
4. Select the primary provider and model. Requests to this provider-prefixed model ID use the chain when the primary attempt fails.
5. Under **Fallbacks**, add one to five backup models in the order the gateway should try them. Choose a provider and model directly, select an existing model configuration, or create a custom model configuration.
6. Under **Fallback triggers**, review the status codes that send the request to the next model. Adjust them as needed.
7. (Optional) Adjust [**Time to first output**](#chain-components), in seconds. Leave the field blank to remove the timeout.
8. (Optional) Turn on [**Model cooldown**](#model-cooldowns), and set how long to skip a model and how many failures start a cooldown.
9. Click **Create chain**.

> [!TIP]
>
> A provider and model can have at most one fallback chain in each workspace. To change its behavior, edit the existing chain.

## Test a fallback chain

The Simulator sends a request through a fallback chain with a behavior you choose for each model, such as a rate limit or an outage. This way, you can check the chain's routing and added latency before a provider fails in production.

To test a chain:

1. Go to **LLM Gateway**, and select the **Model Fallbacks** tab.
2. On the chain's row, click **Open in Simulator →**.
3. Under **Simulate provider behaviour**, choose a behavior for each model in the chain (Healthy, Timeout, Rate limit, or Outage).
4. Click **Run request**.

The results show which model served the request, then list each attempt with its status and duration. Below the attempts are the number of **Fallback hops**, the **Latency added** by failed attempts, and the request's total **Tokens**. **View trace** opens the request's gateway trace, which includes the failed attempts and the attempt that served the request.

Keep the following in mind when testing:

* **Simulated failures send no inference request.** To approximate network latency, the gateway calls a provider endpoint that does not generate tokens. Simulated failures appear as attempt runs in the request trace, without a provider LLM run.
* **A simulated failure falls back only on a trigger status.** Rate limit and Outage move to the next model only while `429` and `503` are in the chain's triggers. Both are in the defaults.
* **The Simulator sends non-streaming requests only.** To check a chain's streaming behavior, send a streaming request from your code.
* **The Simulator ignores cooldowns.** It calls every model even while one is cooling down, and its failures do not count toward **Model cooldown**, so a test run cannot cool down a model for production traffic. To check cooldown behavior, send requests through the chain from your code.
* **Errors outside the simulation still surface.** If a fallback has no provider key in the workspace, its attempt returns `424`, as it would in production. If the primary has no key, the Simulator asks you to add one before it runs the chain.

## Make a call

Call the standard LLM Gateway endpoint with the primary model's provider-prefixed ID. You do not need a route-specific URL or additional request fields. This example uses the base URL and API key set in [Send your first LLM Gateway request](../Get%20started/Send%20your%20first%20LLM%20Gateway%20request.md#send-a-request-from-your-code):

```bash
curl "$LANGSMITH_GATEWAY_BASE_URL/chat/completions" \
    -H "Authorization: Bearer $LANGSMITH_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"model":"<PRIMARY_MODEL_ID>","messages":[{"role":"user","content":"Hello!"}]}'
```

The gateway applies the fallback chain configured for `<PRIMARY_MODEL_ID>` in the API key's workspace. If no chain matches, the gateway returns the primary model's response without attempting a fallback.

## Investigate fallback attempts

When a chain runs, the response records which models the gateway tried, each attempt's status code, and the model that served the request:

* **In gateway traces**: Open the request in the [gateway tracing project](../Observability/View%20LLM%20Gateway%20traces.md#find-gateway-traces), and expand `gateway.request`. Each `gateway.attempt #N` contains its policy checks and, when made, its provider LLM run. Select an attempt to inspect its outcome and upstream error metadata.
* **In application traces**: If your application calls the gateway through a LangChain chat model in Python (`langchain-openai>=1.6.7` or `langchain-anthropic>=1.7.5`) with [tracing](../../Monitor/Overview/LangSmith%20Observability.md) on, the model's run has a **Gateway** section that lists each attempt. The chat model reads this from the response header described in the next item.
* **In the response**: other clients can read the `X-LangSmith-Gateway-Metadata` [response header](../Call%20the%20gateway/API%20formats.md#read-response-metadata). Its `attempt_details` field lists each attempt's model and status code, and `selected_model` names the model that served the request. A model skipped because it was [cooling down](#model-cooldowns) has `fallback_trigger` set to `cooldown` and no status code.

## Set fallbacks for a prompt

A [prompt](../../Deploy/Prompt%20%26%20Context%20Hub/Prompts/Prompt%20engineering%20concepts.md#prompts-in-langsmith) saved in LangSmith stores a model selection with its template, so your application can pull and run both together. A fallback chain applies to every request for its primary model in its workspace.

To give one prompt fallback behavior that differs from other traffic to the same model, point the prompt at its own saved [model configuration](Custom%20model%20configurations.md), and make that configuration the chain's primary. The prompt calls the configuration as `custom/<name>`, and the gateway applies the configuration's chain.

To configure fallbacks for a prompt:

1. In **Settings** > **Model configurations**, [create a model configuration](../../LangSmith%20setup/Govern/Organization/Workspace%20setup/Manage%20model%20configurations.md#create-a-configuration) for the provider and model you want the prompt to use. Note the configuration's name, `<config_name>`, which the next two steps use. An organization-scoped configuration reads the provider key from organization secrets, so if the key is a workspace secret, create a workspace configuration.
2. [Create a fallback chain](#create-a-fallback-chain) in the same workspace. For the primary model, select your configuration from the **Model configurations** section at the end of the model list, rather than its underlying provider and model. The chain's primary model is `custom/<config_name>`, separate from any chain on the underlying model.
3. [Create a prompt](../../Deploy/Prompt%20%26%20Context%20Hub/Prompts/Create%20and%20manage%20prompts/Create%20a%20prompt.md) in the Playground. Click the current model's name to open **Model Configuration**, and select **LangSmith Gateway** as the **Provider**. Type `custom/<config_name>` in the **Model** field, and click **Apply**. Click **Start** to check that the prompt runs. Click **Save**, and name the prompt.
4. In your application, [pull the prompt with its model](../../Deploy/Prompt%20%26%20Context%20Hub/Prompts/Create%20and%20manage%20prompts/Manage%20prompts%20programmatically.md#pull-a-prompt). In Python, set `include_model=True` when calling `client.pull_prompt`.

Invoking the pulled prompt sends requests through the gateway, which applies the configuration's fallback chain. Pulling only the prompt template does not include the model configuration.

> [!TIP]
>
> The fallback chain belongs to the model configuration, not the prompt itself. Prompts that reference the same configuration share its fallbacks.

## See also

* [Add a provider key](../Authentication/Provider%20authentication.md#add-a-provider-key): give each model in a chain a provider key.
* [Monitor LLM Gateway spend](../Observability/Monitor%20LLM%20Gateway%20spend.md): review the cost of primary and fallback attempts by model.
* [Spend policies](../Governance/Spend%20policies.md): apply cost limits alongside fallback routing.

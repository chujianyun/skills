# Gateway Credits

> Use Gateway Credits to access models without a provider key, just authenticate with LangSmith.

> [!NOTE]
>
> The LLM Gateway is in [beta](../../LangSmith%20setup/Cloud/Reference/Release%20stages.md).

**Gateway Credits** let you call LangChain-hosted models through the standard LLM Gateway API without setting up a provider account or key. Authenticate with only your [LangSmith API key](../../LangSmith%20setup/Account/Create%20an%20account%20and%20API%20key.md). No [provider secret](../Authentication/Provider%20authentication.md#add-a-provider-key) is required.

The gateway routes each request based on its model ID. A hosted model slug such as `moonshotai/kimi-k3` uses Gateway Credits. A model ID that starts with a configured bring-your-own-key provider, such as `anthropic/claude-opus-5`, uses that provider's secret instead.

> [!NOTE]
>
> Gateway Credits are available on [paid plans](https://www.langchain.com/pricing) other than Enterprise.

## Available models

Select a hosted model by ID in the request body. Model IDs are case-insensitive.

| Model ID | Description |
| - | - |
| `moonshotai/kimi-k2.6` | Kimi K2.6 by Moonshot AI. A strong general-purpose model. Powered by Fireworks Inference. |
| `moonshotai/kimi-k3` | Kimi K3 by Moonshot AI. Powered by Fireworks Inference. |

> [!TIP]
>
> To list every model available to your workspace, including configured bring-your-own-key providers and hosted models, call [`GET /v1/models`](../Call%20the%20gateway/API%20formats.md#list-models). Use a returned model ID exactly as shown in the `model` field of a prompt request.

## Make a call

Hosted models use the same standard [API formats](../Call%20the%20gateway/API%20formats.md) as bring-your-own-key models. Point an OpenAI-compatible client at `https://gateway.smith.langchain.com/v1`, authenticate with your workspace-scoped LangSmith API key, and set `model` to a hosted model ID. For key types, permissions, and the header each client sends, see [Authenticate to the LLM Gateway](../Authentication/Authenticate%20to%20the%20LLM%20Gateway.md).

```bash cURL
curl https://gateway.smith.langchain.com/v1/chat/completions \
    -H "Authorization: Bearer $LANGSMITH_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"model":"moonshotai/kimi-k3","messages":[{"role":"user","content":"ping"}]}'
```

```python OpenAI SDK
import os

from openai import OpenAI

client = OpenAI(
    base_url="https://gateway.smith.langchain.com/v1",
    api_key=os.environ["LANGSMITH_API_KEY"],
)
response = client.chat.completions.create(
    model="moonshotai/kimi-k3",
    messages=[{"role": "user", "content": "ping"}],
)
print(response.choices[0].message.content)
```

```python LangChain
import os

from langchain.chat_models import init_chat_model

model = init_chat_model(
    model="moonshotai/kimi-k3",
    model_provider="openai",
    base_url="https://gateway.smith.langchain.com/v1",
    api_key=os.environ["LANGSMITH_API_KEY"],
)
print(model.invoke("ping").content)
```

This example calls the US gateway on LangSmith Cloud. For other regions, see [Use a regional gateway](../Get%20started/How%20the%20LLM%20Gateway%20works.md#use-a-regional-gateway).

## Pricing

Gateway Credits are denominated in **LangChain Standard Units (LSUs)**; each call consumes LSUs based on token usage. For plan details and current rates, see [the pricing page](https://www.langchain.com/pricing).

Standard gateway [spend policies](../Governance/Spend%20policies.md) apply to hosted-model traffic, so any configured organization, workspace, API key, or user cap also governs Gateway Credit usage. You can control Gateway Credit consumption with the same tools you use for bring-your-own-key providers. For example, cap a specific API key at \$200/month across every provider, or set a workspace-wide daily limit that includes hosted-model calls.

## Tracing

Like all gateway traffic, hosted-model calls are traced to LangSmith. For where traces land and how to control access to them, see [View LLM Gateway traces](../Observability/View%20LLM%20Gateway%20traces.md).

## Next steps

* [Send your first LLM Gateway request](../Get%20started/Send%20your%20first%20LLM%20Gateway%20request.md): make your first gateway-proxied call.
* [API formats](../Call%20the%20gateway/API%20formats.md): call models through Chat Completions, Messages, or Responses.
* [Spend policies](../Governance/Spend%20policies.md): add cost limits to Gateway Credit usage.
* [Direct model access](../Call%20the%20gateway/Direct%20model%20access.md): use provider-native APIs and model IDs.

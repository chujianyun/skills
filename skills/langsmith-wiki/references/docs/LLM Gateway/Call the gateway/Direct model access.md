# Direct model access

> Access provider APIs directly through provider-specific LLM Gateway paths without using the gateway standardization layer.

> [!NOTE]
>
> The LLM Gateway is in [beta](../../LangSmith%20setup/Cloud/Reference/Release%20stages.md).

Direct model access exposes each provider API through a provider-specific gateway path. The gateway still handles authentication, provider secrets, policies, and tracing, but it does not translate the request and response into another provider's API format.

Direct model access is the path [LangChain and Deep Agents](#configure-langchain-and-deep-agents) use by default. For other clients, use it when you want a provider's native request and response behavior. To call models across providers in one API format, use the [standard endpoint](API%20formats.md) instead.

## Choose a provider path

Append a provider path to your [regional gateway](../Get%20started/How%20the%20LLM%20Gateway%20works.md#use-a-regional-gateway) base URL, for example `https://eu.gateway.smith.langchain.com/anthropic` for direct Anthropic access in GCP EU:

| Provider | Gateway path |
| - | - |
| Anthropic | `/anthropic` |
| AWS Bedrock | `/bedrock` |
| Azure Foundry | `/azure` |
| Baseten | `/baseten` |
| Fireworks | `/fireworks` |
| Google Gemini | `/gemini` |
| Gemini Enterprise Agent Platform | `/vertex` |
| OpenAI | `/openai` |
| ScaleDown | `/scaledown` |
| TypeSafe | `/typesafe` |
| xAI | `/xai` |

Each path uses the provider key stored in the caller's workspace. For secret names, see [Provider authentication](../Authentication/Provider%20authentication.md#add-a-provider-key).

[Gateway Credits models](../Models%20and%20reliability/Gateway%20Credits.md) use the standard endpoint rather than a provider-specific path. These hosted models require no provider secret of your own.

## Configure provider SDKs

Set each provider SDK's base URL to its direct gateway path and use your LangSmith API key as the provider API key:

```bash
export LANGSMITH_API_KEY="<SECRET>"
export BASE_URL="https://gateway.smith.langchain.com"

export ANTHROPIC_BASE_URL="$BASE_URL/anthropic"
export OPENAI_BASE_URL="$BASE_URL/openai/v1"
export GOOGLE_GEMINI_BASE_URL="$BASE_URL/gemini"

export ANTHROPIC_API_KEY="<SECRET>"
export OPENAI_API_KEY="<SECRET>"
export GEMINI_API_KEY="<SECRET>"
export GOOGLE_API_KEY="<SECRET>"
```

The gateway resolves the actual provider key provider secrets, so the provider key does not need to be stored locally.

```python OpenAI SDK
import os

from openai import OpenAI

client = OpenAI(
    base_url=os.environ["OPENAI_BASE_URL"],
    api_key=os.environ["LANGSMITH_API_KEY"],
)
response = client.chat.completions.create(
    model="gpt-5.4-mini",
    messages=[{"role": "user", "content": "ping"}],
)
print(response.choices[0].message.content)
```

```python Anthropic SDK
import os

import anthropic

client = anthropic.Anthropic(
    base_url=os.environ["ANTHROPIC_BASE_URL"],
    api_key=os.environ["LANGSMITH_API_KEY"],
)
message = client.messages.create(
    model="claude-opus-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "ping"}],
)
print(message.content[0].text)
```

Direct paths use the provider's native model name without a provider prefix.

## Configure LangChain and Deep Agents

[LangChain](https://docs.langchain.com/oss/python/langchain/overview.md) chat models and [Deep Agents](https://docs.langchain.com/oss/python/deepagents/overview.md), including [Deep Agents Code](https://docs.langchain.com/oss/deepagents/code/overview.md), reach these provider paths through the `LANGSMITH_GATEWAY` environment variable:

```bash
export LANGSMITH_API_KEY="lsv2_..."
export LANGSMITH_GATEWAY="true"
```

Deep Agents Code also requires `LANGSMITH_GATEWAY_API_KEY`. Set it to the same key:

```bash
export LANGSMITH_GATEWAY_API_KEY="<SECRET>"
```

> [!NOTE]
>
> `LANGSMITH_GATEWAY` support requires these minimum Python package versions: `langchain-anthropic>=1.5.1`, `langchain-baseten>=0.2.3`, `langchain-fireworks>=1.5.1`, `langchain-google-genai>=4.3.2`, and `langchain-openai>=1.4.1`.

Each supported integration appends its own provider path, so `ChatAnthropic` calls `https://gateway.smith.langchain.com/anthropic` and `ChatOpenAI` calls `https://gateway.smith.langchain.com/openai/v1`. To route requests through the standard endpoint instead, see [Send your first LLM Gateway request](../Get%20started/Send%20your%20first%20LLM%20Gateway%20request.md#send-a-request-from-your-code).

## See also

* [Send your first LLM Gateway request](../Get%20started/Send%20your%20first%20LLM%20Gateway%20request.md): use the standard API to call models across providers.
* [Set up the LLM Gateway](../Get%20started/Set%20up%20the%20LLM%20Gateway.md): configure provider secrets and access.
* [View LLM Gateway traces](../Observability/View%20LLM%20Gateway%20traces.md): see where gateway traces appear and who can view them.

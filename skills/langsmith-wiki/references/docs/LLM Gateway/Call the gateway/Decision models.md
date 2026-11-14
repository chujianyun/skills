# Decision models

> Call TypeSafe and OpenAI decision models through the LangSmith LLM Gateway using the System One API or the OpenAI Decisions API.

Decision models classify or score text and return structured answers instead of generated chat messages. Call them through the [LLM Gateway](../Get%20started/LLM%20Gateway.md). Each model uses its own API:

| Model | API | Endpoint | Credentials |
| - | - | - | - |
| [TypeSafe (Jev)](#use-typesafe-jev) | System One | `/v1/systemone` | `TYPESAFE_API_KEY` provider secret |
| [OpenAI decision models](#use-openai-decision-models) | OpenAI Decisions | `/openai/v1/decisions` | `OPENAI_API_KEY` provider secret |

Both models require a workspace-scoped LangSmith API key and the matching workspace [provider secret](../Authentication/Provider%20authentication.md#add-a-provider-key). For key types, permissions, and the header each client sends, see [Authenticate to the LLM Gateway](../Authentication/Authenticate%20to%20the%20LLM%20Gateway.md). Set your LangSmith API key before you run the examples on this page:

```bash
export LANGSMITH_API_KEY="<API_KEY>"
```

## Use TypeSafe (Jev)

The gateway supports TypeSafe decision models with bring-your-own-key (BYOK). Configure `TYPESAFE_API_KEY` as a workspace [provider secret](../Authentication/Provider%20authentication.md#add-a-provider-key). See [TypeSafe setup](https://docs.langchain.com/oss/python/integrations/providers/typesafe#setup) to create a key and install the LangChain integration.

TypeSafe (Jev) uses the System One API. Pass the text to evaluate in `state` and one or more named questions in `questions`. System One supports three question types:

* **`noul`**: Returns the probability that the answer is true.
* **`choice`**: Classifies the state into one of the supplied options.
* **`score`**: Scores the state against a rubric.

The response contains `answers` keyed by question name rather than a chat message. Streaming is not supported.

The `typesafe/` prefix routes the request through your workspace's TypeSafe provider secret. Pass your LangSmith API key, not your TypeSafe API key, as the SDK's `api_key` or `apiKey`. Use the gateway base URL without `/v1` for the SDKs:

> [tab] Python
>
> Install the TypeSafe SDK:
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> pip install typesafe-sdk
> ```
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import os
>
> from typesafe_sdk import Noul, TypeSafeClient
>
> client = TypeSafeClient(
>     api_key=os.environ["LANGSMITH_API_KEY"],
>     base_url="https://gateway.smith.langchain.com",
> )
>
> response = client.system_one(
>     state="Hello!",
>     model="typesafe/jev-1.13.0",
>     questions={
>         "is_helpful": Noul(
>             instructions="Does this explain what an LLM gateway does?"
>         ),
>     },
> )
> ```

> [tab] JavaScript
>
> Install the TypeSafe SDK:
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> npm install @typesafe-ai/sdk
> ```
>
> ```javascript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { noul, TypeSafeClient } from "@typesafe-ai/sdk";
>
> const client = new TypeSafeClient({
>   apiKey: process.env.LANGSMITH_API_KEY,
>   baseURL: "https://gateway.smith.langchain.com",
> });
>
> const response = await client.systemOne({
>   state: "Hello!",
>   model: "typesafe/jev-1.13.0",
>   questions: {
>     is_helpful: noul("Does this explain what an LLM gateway does?"),
>   },
> });
> ```

> [tab] cURL
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl https://gateway.smith.langchain.com/v1/systemone \
>     -H "Authorization: Bearer $LANGSMITH_API_KEY" \
>     -H "Content-Type: application/json" \
>     -d '{
>       "state": "Hello!",
>       "model": "typesafe/jev-1.13.0",
>       "questions": {
>         "is_helpful": {
>           "type": "noul",
>           "instructions": "Does this explain what an LLM gateway does?"
>         }
>       }
>     }'
> ```

## Use OpenAI decision models

OpenAI decision models use the OpenAI Decisions API, which has its own request and response format, separate from System One. The gateway supports the OpenAI Decisions API through [direct model access](Direct%20model%20access.md). Configure `OPENAI_API_KEY` as a workspace [provider secret](../Authentication/Provider%20authentication.md#add-a-provider-key).

Send requests to `POST /openai/v1/decisions` using your workspace-scoped LangSmith API key. Set `model` to the native OpenAI model name without the `openai/` prefix:

```bash
curl https://gateway.smith.langchain.com/openai/v1/decisions \
    -H "Authorization: Bearer $LANGSMITH_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
      "model": "gpt-6-luna",
      "input": "The package arrived with a broken screen.",
      "questions": [
        {
          "type": "predicate",
          "name": "damaged",
          "instructions": "Does the customer report a damaged item?"
        }
      ]
    }'
```

The gateway preserves the native request and response format:

```json
{
  "model": "gpt-6-luna",
  "answers": [
    {
      "type": "predicate",
      "name": "damaged",
      "probability": 1.0
    }
  ],
  "usage": {
    "input_tokens": 164,
    "input_tokens_details": {
      "cached_tokens": 0,
      "cache_write_tokens": 0
    },
    "output_tokens": 0,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 164
  }
}
```

Gateway [access](../Governance/Model%20access%20policies.md), [rate-limit](../Governance/Rate%20limit%20policies.md), and [budget policies](../Governance/Spend%20policies.md) apply to Decisions requests, and token usage counts toward spend caps. The gateway traces each request to LangSmith with the request as input and the answers and token usage as output.

## See also

* [Set up the LLM Gateway](../Get%20started/Set%20up%20the%20LLM%20Gateway.md): Configure provider secrets and grant gateway access.
* [TypeSafe integration](https://docs.langchain.com/oss/python/integrations/providers/typesafe): Use TypeSafe decision models through LangChain.

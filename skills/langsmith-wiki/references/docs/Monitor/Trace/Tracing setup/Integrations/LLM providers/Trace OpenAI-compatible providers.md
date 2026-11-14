# Trace OpenAI-compatible providers

> Trace LLM calls from any OpenAI-compatible provider to LangSmith.

Many LLM providers accept requests in the same format as the OpenAI API. To trace calls from these providers to LangSmith, construct an OpenAI client pointed at the provider's base URL, then wrap it with [`wrap_openai`](https://reference.langchain.com/python/langsmith/wrappers/_openai/wrap_openai) / [`wrapOpenAI`](https://reference.langchain.com/javascript/modules/langsmith.html).

Use `wrap_openai` / `wrapOpenAI` for direct API calls. Use [`@traceable`](https://reference.langchain.com/python/langsmith/run_helpers/traceable) when you need to trace agent logic around the call or set metadata per invocation.

| | `wrap_openai` / `wrapOpenAI` | `@traceable` / `traceable` |
| - | - | - |
| Token tracking | Automatic | Requires `run_type="llm"` |
| Run type | LLM (set automatically) | Chain by default |
| Traces | The API call | The function wrapping it |
| Metadata | Client-level only (Python); client-level or per-call (TypeScript) | Per-call via [`langsmith_extra`](https://reference.langchain.com/python/langsmith/run_helpers/SupportsLangsmithExtra) |

> [!NOTE]
>
> To trace OpenAI directly, refer to [Trace with OpenAI](Trace%20with%20OpenAI.md).

> [!NOTE]
>
> In an [agent-based workspace](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20Registry.md), [create an agent](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md) once before sending traces. Use [agent addressing](../../../Configuration%20%26%20troubleshooting/Agent%20%26%20environment%20settings/Log%20traces%20to%20an%20agent.md) to select its identifier and environment. If an integration requires `project_name`, use the selected environment's [`tracer_session_name`](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md#use-an-environment-project) as a compatibility value.

## Setup

```bash Python
pip install langsmith openai
```

```bash npm
npm install langsmith openai
```

```bash
export LANGSMITH_API_KEY=<your-api-key>
export LANGSMITH_AGENT_ID="<your-agent-id>"
export LANGSMITH_AGENT_ENVIRONMENT="local"
export LANGSMITH_TRACING=true
```

## Trace API calls

```python Python
import os

import openai
from langsmith import wrappers

client = wrappers.wrap_openai(
    openai.OpenAI(
        base_url="https://<provider-base-url>/v1",
        api_key=os.environ["PROVIDER_API_KEY"],
    )
)

completion = client.chat.completions.create(
    model="<provider-model-name>",
    messages=[{"role": "user", "content": "Hello!"}],
)
print(completion.choices[0].message.content)
```

```typescript TypeScript
import OpenAI from "openai";
import { wrapOpenAI } from "langsmith/wrappers/openai";

const client = wrapOpenAI(
  new OpenAI({
    baseURL: "https://<provider-base-url>/v1",
    apiKey: process.env.PROVIDER_API_KEY!,
  })
);

const completion = await client.chat.completions.create({
  model: "<provider-model-name>",
  messages: [{ role: "user", content: "Hello!" }],
});
console.log(completion.choices[0].message.content);
```

## Add metadata

> [tab] Python
>
> Pass `tracing_extra` when wrapping the client. The metadata applies to all calls made with that client.
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import os
>
> import openai
>
> from langsmith import wrappers
>
> client = wrappers.wrap_openai(
>     openai.OpenAI(
>         base_url="https://<provider-base-url>/v1",
>         api_key=os.environ["PROVIDER_API_KEY"],
>     ),
>     tracing_extra={"metadata": {"environment": "production"}},
> )
> ```

> [tab] TypeScript
>
> Pass options as the second argument to `wrapOpenAI` for client-level metadata, or pass [`langsmithExtra`](https://reference.langchain.com/javascript/modules/langsmith.html) per call.
>
> ```typescript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import OpenAI from "openai";
> import { wrapOpenAI } from "langsmith/wrappers/openai";
>
> const client = wrapOpenAI(
>   new OpenAI({
>     baseURL: "https://<provider-base-url>/v1",
>     apiKey: process.env.PROVIDER_API_KEY!,
>   }),
>   { metadata: { environment: "production" } }
> );
>
> // Per-call metadata
> const completion = await client.chat.completions.create(
>   {
>     model: "<provider-model-name>",
>     messages: [{ role: "user", content: "Hello!" }],
>   },
>   { langsmithExtra: { metadata: { request_id: "abc123" } } }
> );
> ```

## Related guides

Some providers have dedicated setup guides that use `@traceable` or a native callback. These approaches trace at the function level rather than wrapping the client directly, or integrate with the provider's own SDK and routing layer.

* [DeepSeek](Trace%20with%20DeepSeek.md): OpenAI-compatible API; guide uses `@traceable` with custom provider metadata
* [LiteLLM](Trace%20with%20LiteLLM.md): proxy that exposes an OpenAI-compatible endpoint; guide covers `@traceable` and LiteLLM's built-in LangSmith callback

# developers.llamaindex.ai/python/framework/integrations/llm/vercel-ai-gateway/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/vercel-ai-gateway/index.md

--- title: Vercel AI Gateway | Developer Documentation ---

The AI Gateway is a proxy service from Vercel that routes model requests to various AI providers. It offers a unified API to multiple providers and gives you the ability to set budgets, monitor usage, load-balance requests, and manage fallbacks. You can find out more from their docs [1]

If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-llms-vercel-ai-gateway ```
``` !pip install llama-index ```
``` from llama_index.llms.vercel_ai_gateway import VercelAIGateway from llama_index.core.llms import ChatMessage

llm = VercelAIGateway( model="anthropic/claude-4-sonnet", max_tokens=64000, context_window=200000, api_key="<API_KEY>", default_headers={ "http-referer": "https://myapp.com/", # Optional: Your app URL "x-title": "My App", # Optional: Your app name }, )

print(llm.model) ```
## Call `chat` with ChatMessage List
You need to either set env var `VERCEL_AI_GATEWAY_API_KEY` or `VERCEL_OIDC_TOKEN` or set api\_key in the class constructor
``` # import os # os.environ['VERCEL_AI_GATEWAY_API_KEY'] = '<your-api-key>'

llm = VercelAIGateway( api_key="<API_KEY>", max_tokens=64000, context_window=200000, model="anthropic/claude-4-sonnet", ) ```

``` message = ChatMessage(role="user", content="Tell me a joke") resp = llm.chat([message]) print(resp) ```

### Streaming
``` message = ChatMessage(role="user", content="Tell me a story in 250 words") resp = llm.stream_chat([message]) for r in resp: print(r.delta, end="") ```

## Call `complete` with Prompt
``` resp = llm.complete("Tell me a joke") print(resp) ```

``` resp = llm.stream_complete("Tell me a story in 250 words") for r in resp: print(r.delta, end="") ```

## Model Configuration
``` # This example uses Anthropic's Claude 4 Sonnet (models are specified as `provider/model`): llm = VercelAIGateway( model="anthropic/claude-4-sonnet", api_key="<API_KEY>", ) ```

``` resp = llm.complete("Write a story about a dragon who can code in Rust") print(resp) ```

[1] https://vercel.com/docs/ai-gateway
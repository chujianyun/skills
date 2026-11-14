# Trace without setting environment variables

The following environment variables allow you to configure tracing enabled, the API endpoint, the API key, and the tracing destination:

* `LANGSMITH_TRACING`
* `LANGSMITH_API_KEY`
* `LANGSMITH_ENDPOINT`
* `LANGSMITH_AGENT_ID`
* `LANGSMITH_AGENT_ENVIRONMENT`

In an [agent-based workspace](../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20Registry.md), [create the agent](../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md) during setup. The examples below use its [agent address](Log%20traces%20to%20an%20agent.md) to configure tracing without environment variables.

If you need to trace runs with a custom configuration, are working in an environment that doesn’t support typical environment variables (such as Cloudflare Workers), or prefer not to rely on environment variables, LangSmith allows you to configure tracing programmatically.

> [!WARNING]
>
> In version **0.1.95** of the [Python SDK](../../../Reference/langsmith%20%28smith-python-sdk%29.md), `with trace` honors the `LANGSMITH_TRACING` environment variable. For details, refer to the [release notes](https://github.com/langchain-ai/langsmith-sdk/releases/tag/v0.1.95). To disable or enable tracing without setting environment variables, use the `with tracing_context` context manager, as shown in the following example.

* Python: The recommended way to do this in Python is to use the [`tracing_context`](../../Tracing%20setup/Manual%20instrumentation/Custom%20instrumentation.md#use-the-trace-context-manager-python-only) context manager. This works for both code annotated with `traceable` and code within the `trace` context manager.
* TypeScript: You can pass in both the client and the `tracingEnabled` flag to the [`traceable`](https://reference.langchain.com/javascript/langsmith/traceable) decorator.

```python Python
import openai
from langsmith import Client, agent_address, tracing_context, traceable
from langsmith.wrappers import wrap_openai

langsmith_client = Client(
  api_key="<API_KEY>",  # This can be retrieved from a secrets manager
  api_url="https://api.smith.langchain.com",  # Update appropriately for self-hosted installations or regional SaaS
  workspace_id="YOUR_WORKSPACE_ID", # Must be specified for API keys scoped to multiple workspaces
)

client = wrap_openai(openai.Client())

@traceable(run_type="tool", name="Retrieve Context")
def my_tool(question: str) -> str:
  return "During this morning's meeting, we solved all world conflict."

@traceable
def chat_pipeline(question: str):
  context = my_tool(question)
  messages = [
      { "role": "system", "content": "You are a helpful assistant. Please respond to the user's request only based on the given context." },
      { "role": "user", "content": f"Question: {question}\nContext: {context}"}
  ]
  chat_completion = client.chat.completions.create(
      model="gpt-5.4-mini", messages=messages
  )
  return chat_completion.choices[0].message.content

# Can set to False to disable tracing here without changing code structure
with tracing_context(enabled=True, address=agent_address("<your-agent-id>", "local")):
  # Use langsmith_extra to pass in a custom client
  chat_pipeline("Can you summarize this morning's meetings?", langsmith_extra={"client": langsmith_client})
```

```typescript TypeScript
import { AgentAddress, Client } from "langsmith";
import { traceable } from "langsmith/traceable";
import { wrapOpenAI } from "langsmith/wrappers";
import { OpenAI } from "openai";

const client = new Client({
    apiKey: "<API_KEY>",  // This can be retrieved from a secrets manager
    apiUrl: "https://api.smith.langchain.com",  // Update appropriately for self-hosted installations or regional SaaS
});

const openai = wrapOpenAI(new OpenAI());

const tool = traceable((question: string) => {
    return "During this morning's meeting, we solved all world conflict.";
}, { name: "Retrieve Context", runType: "tool" });

const pipeline = traceable(
    async (question: string) => {
        const context = await tool(question);

        const completion = await openai.chat.completions.create({
            model: "gpt-5.4-mini",
            messages: [
                { role: "system" as const, content: "You are a helpful assistant. Please respond to the user's request only based on the given context." },
                { role: "user" as const, content: `Question: ${question}\nContext: ${context}`}
            ]
        });

        return completion.choices[0].message.content;
    },
    { name: "Chat", client, tracingEnabled: true, address: new AgentAddress("<your-agent-id>", "local") }
);

await pipeline("Can you summarize this morning's meetings?");
```

If you prefer a video tutorial, check out the [Alternative Ways to Trace video](https://academy.langchain.com/pages/intro-to-langsmith-preview) from the Introduction to LangSmith Course.

## Related

If you need to dynamically enable or disable tracing based on runtime conditions (such as client requirements, data sensitivity, or compliance policies), refer to [Conditional tracing](Conditional%20tracing.md) for examples.

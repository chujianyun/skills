# Trace with OpenAI

The [`wrap_openai`](https://reference.langchain.com/python/langsmith/wrappers/_openai/wrap_openai) / [`wrapOpenAI`](https://reference.langchain.com/javascript/langsmith/wrappers/wrapOpenAI) methods in Python/TypeScript allow you to wrap your OpenAI client in order to automatically log traces -- no decorator or function wrapping required! Using the wrapper ensures that messages, including tool calls and multimodal content blocks will be rendered nicely in LangSmith. Also note that the wrapper works seamlessly with the [`@traceable`](https://reference.langchain.com/python/langsmith/run_helpers/traceable) decorator or [`traceable`](https://reference.langchain.com/javascript/langsmith/traceable/traceable) function and you can use both in the same agent.

> [!NOTE]
>
> In an [agent-based workspace](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20Registry.md), [create an agent](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md) once before sending traces. Use [agent addressing](../../../Configuration%20%26%20troubleshooting/Agent%20%26%20environment%20settings/Log%20traces%20to%20an%20agent.md) to select its identifier and environment. If an integration requires `project_name`, use the selected environment's [`tracer_session_name`](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md#use-an-environment-project) as a compatibility value.

> [!NOTE]
>
> The `LANGSMITH_TRACING` environment variable must be set to `'true'` in order for traces to be logged to LangSmith, even when using [`wrap_openai`](https://reference.langchain.com/python/langsmith/wrappers/_openai/wrap_openai) or [`wrapOpenAI`](https://reference.langchain.com/javascript/langsmith/wrappers/wrapOpenAI). This allows you to toggle tracing on and off without changing your code.
>
> Additionally, you will need to set the `LANGSMITH_API_KEY` environment variable to your API key (see [Setup](https://docs.langchain.com/index.md) for more information).
>
> If your LangSmith API key is linked to multiple workspaces, set the `LANGSMITH_WORKSPACE_ID` environment variable to specify which workspace to use.
>
> Set `LANGSMITH_AGENT_ID` and `LANGSMITH_AGENT_ENVIRONMENT` to the registered agent and environment. See [Configure tracing for the agent](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md#configure-tracing-for-the-agent).

```python Python
import openai
from langsmith import traceable
from langsmith.wrappers import wrap_openai

client = wrap_openai(openai.Client())

@traceable(run_type="tool", name="Retrieve Context")
def my_tool(question: str) -> str:
  return "During this morning's meeting, we solved all world conflict."

@traceable(name="Chat Pipeline")
def chat_pipeline(question: str):
  context = my_tool(question)
  messages = [
      { "role": "system", "content": "You are a helpful assistant. Please respond to the user's request only based on the given context." },
      { "role": "user", "content": f"Question: {question}\nContext: {context}"}
  ]
  chat_completion = client.chat.completions.create(
      model="gpt-6.1-sol", messages=messages
  )
  return chat_completion.choices[0].message.content

chat_pipeline("Can you summarize this morning's meetings?")
```

```typescript TypeScript
import OpenAI from "openai";
import { traceable } from "langsmith/traceable";
import { wrapOpenAI } from "langsmith/wrappers";

const client = wrapOpenAI(new OpenAI());

const myTool = traceable(async (question: string) => {
  return "During this morning's meeting, we solved all world conflict.";
}, { name: "Retrieve Context", run_type: "tool" });

const chatPipeline = traceable(async (question: string) => {
  const context = await myTool(question);
  const messages = [
      {
          role: "system",
          content:
              "You are a helpful assistant. Please respond to the user's request only based on the given context.",
      },
      { role: "user", content: `Question: ${question} Context: ${context}` },
  ];
  const chatCompletion = await client.chat.completions.create({
      model: "gpt-6.1-sol",
      messages: messages,
  });
  return chatCompletion.choices[0].message.content;
}, { name: "Chat Pipeline" });

await chatPipeline("Can you summarize this morning's meetings?");
```

To trace a provider with an OpenAI-compatible API, refer to [Trace OpenAI-compatible providers](Trace%20OpenAI-compatible%20providers.md).

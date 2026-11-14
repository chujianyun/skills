# Trace with LiteLLM

[LiteLLM](https://www.litellm.ai/) provides a unified interface for calling LLM providers using a consistent OpenAI-compatible API. It can be used either as a [Python SDK](https://docs.litellm.ai/docs/#litellm-python-sdk) embedded directly in your agent, or as a [proxy server](https://docs.litellm.ai/docs/simple_proxy) that exposes an OpenAI-compatible endpoint for client code.

This guide shows you how to trace LiteLLM calls with LangSmith using:

* The [LangSmith SDK](#use-langsmith_tracing-and-traceable) (`@traceable`) for agent-level tracing.
* [LiteLLM’s built-in langsmith callback](#log-litellm-call-with-the-langsmith-callback) for model-level logging.
* The [LiteLLM Proxy](#use-the-litellm-proxy) for gateway-level tracing.

> [!NOTE]
>
> In an [agent-based workspace](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20Registry.md), [create an agent](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md) once before sending traces. Use [agent addressing](../../../Configuration%20%26%20troubleshooting/Agent%20%26%20environment%20settings/Log%20traces%20to%20an%20agent.md) to select its identifier and environment. If an integration requires `project_name`, use the selected environment's [`tracer_session_name`](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md#use-an-environment-project) as a compatibility value.

## Installation

Install the following when using either the LiteLLM Python SDK or LiteLLM Proxy:

```bash Python SDK
pip install litellm langsmith openai
```

```bash Proxy usage
npm install openai langsmith
```

The examples in this guide use OpenAI models, but you can install the necessary provider for your use case.

## Use the LiteLLM Python SDK

LiteLLM supports two ways to send traces to LangSmith, which operate at different layers:

* [LangSmith SDK tracing](#use-langsmith_tracing-and-traceable) with `LANGSMITH_TRACING=true` enables agent-level tracing via the LangSmith SDK. This is useful when you want to trace broader business logic, multi-step pipelines, or spans created with `@traceable`.
* LiteLLM’s built-in [`langsmith` callback](#log-litellm-call-with-the-langsmith-callback) logs model calls directly from LiteLLM. This is recommended when you want to trace LiteLLM requests specifically, or run async agents.

> [!NOTE]
>
> Avoid enabling LiteLLM's `langsmith` callback and LangSmith tracing for the same LiteLLM calls, as this can result in duplicate traces.

### Use `LANGSMITH_TRACING` and `traceable`

You can use `LANGSMITH_TRACING=true` together with `@traceable` for predictable traces in LangSmith. This approach ensures that the **Input** and **Output** columns reflect your function arguments and return values, allowing you to preserve the full message structure (including `role` and `content`). It also works reliably in simple synchronous scripts, without requiring an asyncio event loop or additional callback configuration.

1. Sending traces to an agent requires `langsmith>=0.14.9`. Set the following environment variables to enable LangSmith tracing for LiteLLM Python SDK usage:

   ```bash
   export LANGSMITH_API_KEY="<API_KEY>"
   export LANGSMITH_AGENT_ID="<your-agent-id>"
   export LANGSMITH_AGENT_ENVIRONMENT="local"
   export LANGSMITH_TRACING="true"
   ```

   Create LangSmith [API keys](../../../../../LangSmith%20setup/Account/Create%20an%20account%20and%20API%20key.md) in the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-trace-litellm).

   Depending on what provider you're using, you'll also need to set API keys:

   ```bash
   export OPENAI_API_KEY="<API_KEY>"
   ```

2. Add the following code to your script file:

   ```python
   from langsmith import traceable
   from litellm import completion

   @traceable(name="LiteLLM Chat Completion")
   def run(messages):
       response = completion(
           model="gpt-6.1-sol",
           messages=messages,
       )
       # Return the assistant message so the LangSmith UI shows role + content
       return response["choices"][0]["message"]

   messages = [
       {"role": "user", "content": "Explain observability in LLM systems."}
   ]

   result = run(messages)
   print(result["content"])
   ```

   `@traceable` instruments your function as a LangSmith run. When `LANGSMITH_TRACING=true` is set, LangSmith automatically:

   * Creates a run when the function is invoked.
   * Records the function arguments as the run inputs.
   * Executes the function body (including the LiteLLM call).
   * Records the function's return value as the run output.
   * Captures timing, errors, and nested spans (if any).

   In this example, the `messages` argument becomes the trace input, and the returned assistant message object becomes the trace output. The LiteLLM call itself runs normally—`@traceable` wraps it with observability rather than modifying its behavior. This approach traces your agent logic, not just the model call.

   > [!TIP]
   >
   > For more general examples using `@traceable`, refer to the [Custom instrumentation](../../Manual%20instrumentation/Custom%20instrumentation.md#use-@traceable-/-traceable) page.

### Log LiteLLM call with the `langsmith` callback

This callback uses a legacy destination setting. Set it to the agent environment's [`tracer_session_name`](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md#use-an-environment-project). Use the SDK tracing approach above for agent addressing.

LiteLLM can send traces directly to LangSmith using its built-in [callback system](https://docs.litellm.ai/docs/observability/callbacks). This is useful when running LiteLLM inside an async Python service and you want LiteLLM itself to emit model-level logs.

LiteLLM callbacks run in an asynchronous environment. When making asynchronous calls with `litellm.acompletion()`, you can enable the `langsmith` callback to log successful model calls.

> [!TIP]
>
> This approach is best suited for async agents. For simple synchronous scripts, use the `@traceable` method shown in the [previous section](#use-langsmith_tracing-and-traceable).

1. Set the following environment variables:

   ```bash
   export LANGSMITH_API_KEY="<API_KEY>"
   export LANGSMITH_PROJECT="litellm-integration"
   ```

   Create LangSmith [API keys](../../../../../LangSmith%20setup/Account/Create%20an%20account%20and%20API%20key.md) in the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-trace-litellm).

   Depending on what provider you're using, you'll also need to set API keys:

   ```bash
   export OPENAI_API_KEY="<API_KEY>"
   ```

2. To run this in a minimal script:

   * Use `acompletion()` (async API).
   * Run with `asyncio.run(...)` to create an event loop.
   * Set `langsmith_batch_size = 1` to flush immediately.

   ```python
   import asyncio
   import litellm
   from litellm import acompletion

   # Enable LiteLLM → LangSmith callback
   litellm.success_callback = ["langsmith"]

   # For short-lived scripts, send immediately instead of waiting for batch flush
   litellm.langsmith_batch_size = 1

   async def main():
       response = await acompletion(
           model="gpt-6.1-sol",
           messages=[
               {"role": "user", "content": "Explain observability in LLM systems."}
           ],
       )

       # Print the assistant message content for local verification
       print(response["choices"][0]["message"]["content"])

       # Allow time for background logger to flush before process exit
       await asyncio.sleep(1)

   if __name__ == "__main__":
       asyncio.run(main())
   ```

   The callback sends LiteLLM’s model request and response data directly to LangSmith, including provider metadata and token usage. Because LiteLLM controls the payload, the **Input** and **Output** columns may include additional metadata compared to the `@traceable` example.

## Use the LiteLLM Proxy

The LiteLLM proxy runs as a standalone server and exposes an OpenAI-compatible API.

1. To have the proxy log requests directly to LangSmith, configure the callback in `config.yaml`:

   ```yaml
   model_list:
     - model_name: gpt-4o
       litellm_params:
         model: openai/gpt-4o

   litellm_settings:
     callbacks: ["langsmith"]
   ```

2. Set environment variables in your proxy environment:

   ```bash
   export LANGSMITH_API_KEY="<API_KEY>"
   export LANGSMITH_PROJECT="litellm-proxy"
   export OPENAI_API_KEY="<API_KEY>"
   ```

   > [!NOTE]
   >
   > The LiteLLM proxy runs as a separate service. If you enable LangSmith tracing at the proxy level, you must configure `LANGSMITH_API_KEY` and related environment variables in the proxy’s runtime environment. These settings are not shared with your process.

3. Start the proxy:

   ```bash
   litellm --config config.yaml
   ```

   By default, the proxy runs at `http://localhost:4000/v1`. Your agent calls it using any OpenAI-compatible client (Python, JavaScript, curl, etc.).

   With `callbacks: ["langsmith"]` enabled, the proxy sends model request and response data directly to LangSmith. No tracing configuration is required in the client code.

4. Call the proxy from another terminal window:

   ```python Python
   from openai import OpenAI

   client = OpenAI(
       base_url="http://localhost:4000/v1",
       api_key="anything"  # proxy may require a key but doesn't validate it by default
   )

   response = client.chat.completions.create(
       model="gpt-6.1-sol",
       messages=[
           {"role": "user", "content": "What is LiteLLM?"}
       ],
   )

   print(response.choices[0].message.content)
   ```

   ```javascript JavaScript
   import OpenAI from "openai";

   const client = new OpenAI({
   apiKey: "anything",
   baseURL: "http://localhost:4000/v1",
   });

   const response = await client.chat.completions.create({
   model: "gpt-6.1-sol",
   messages: [
       { role: "user", content: "Explain LiteLLM tracing." }
   ],
   });

   console.log(response.choices[0].message.content);
   ```

   The client sends a normal chat completion request, and the proxy handles provider routing and response formatting.

## Next steps

* [View traces in LangSmith](../../../../Debug/Viewing%20%26%20managing%20traces/Filter%20traces.md)
* [Add custom metadata](../../Manual%20instrumentation/Metadata%20parameters%20reference.md)
* [Filter and sample traces](../../../Configuration%20%26%20troubleshooting/Agent%20%26%20environment%20settings/Set%20a%20sampling%20rate%20for%20traces.md)

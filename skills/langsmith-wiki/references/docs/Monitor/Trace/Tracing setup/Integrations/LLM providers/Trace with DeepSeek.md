# Trace with DeepSeek

[DeepSeek](https://deepseek.com/) provides high-performance, OpenAI-compatible language models including `deepseek-chat` (for general conversations) and `deepseek-reasoner` (for advanced reasoning tasks). Using LangSmith allows you to debug, monitor, and evaluate your agents by capturing structured traces of inputs, outputs, and metadata.

This guide shows you how to integrate DeepSeek with LangSmith in both Python and TypeScript, using LangSmith's [`@traceable`](https://reference.langchain.com/python/langsmith/run_helpers/traceable) (Python) and [`traceable(...)`](../../../../Reference/langsmith%20%28smith-js-ts-sdk%29.md) (TypeScript) utilities to log LLM calls automatically.

> [!NOTE]
>
> In an [agent-based workspace](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20Registry.md), [create an agent](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md) once before sending traces. Use [agent addressing](../../../Configuration%20%26%20troubleshooting/Agent%20%26%20environment%20settings/Log%20traces%20to%20an%20agent.md) to select its identifier and environment. If an integration requires `project_name`, use the selected environment's [`tracer_session_name`](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md#use-an-environment-project) as a compatibility value.

## Installation

Install [OpenAI](https://platform.openai.com/docs/libraries) and LangSmith:

```bash pip
pip install openai langsmith
```

```bash uv
uv add openai langsmith
```

```bash npm
npm install openai langsmith dotenv
```

DeepSeek provides an [OpenAI-compatible API](https://api-docs.deepseek.com/), which means you can use the OpenAI SDK to interact with DeepSeek models. The only difference is that you configure the client to point to DeepSeek's base URL (`https://api.deepseek.com/v1`) instead of OpenAI's endpoint.

## Setup

Sending traces to an agent requires `langsmith>=0.14.9` in Python or `langsmith@>=0.11.0` in TypeScript.

Set your [API keys](../../../../../LangSmith%20setup/Account/Create%20an%20account%20and%20API%20key.md), agent identifier, and environment:

```bash
export LANGSMITH_API_KEY="<API_KEY>"
export LANGSMITH_TRACING="true"
export LANGSMITH_AGENT_ID="<your-agent-id>"
export LANGSMITH_AGENT_ENVIRONMENT="local"
export DEEPSEEK_API_KEY="<API_KEY>"
```

* Ensure you have a DeepSeek API key from your [DeepSeek account](https://platform.deepseek.com/).
* Set `LANGSMITH_TRACING=true` and provide your LangSmith API key (`LANGSMITH_API_KEY`) activates automatic logging of traces.
* Set `LANGSMITH_AGENT_ID` and `LANGSMITH_AGENT_ENVIRONMENT` to the registered agent and environment.
* The `LANGSMITH_TRACING` flag must be true for any traces to be recorded.

## Configure tracing

1. Instrument the DeepSeek API call with LangSmith. In your script, create an OpenAI client configured to use DeepSeek's API endpoint and wrap a call in a traced function:

   ```python Python
   import os
   from openai import OpenAI
   from langsmith import traceable

   # Create a client pointing to DeepSeek
   client = OpenAI(
       api_key=os.environ["DEEPSEEK_API_KEY"],
       base_url="https://api.deepseek.com/v1"
   )

   @traceable(
       run_type="llm",
       name="DeepSeek Chat Completion",
       metadata={"ls_provider": "deepseek", "ls_model_name": "deepseek-chat"},
   )
   def call_deepseek(messages: list[dict]):
       response = client.chat.completions.create(
           model="deepseek-chat",
           messages=messages
       )
       return response.choices[0].message

   if __name__ == "__main__":
       messages = [
           {"role": "system", "content": "You are a helpful assistant that translates English to French."},
           {"role": "user", "content": "I love programming."}
       ]
       result = call_deepseek(messages=messages)
       print("Model reply:", result.content)
   ```

   ```typescript TypeScript
   import { config } from "dotenv";
   import OpenAI from "openai";
   import { traceable } from "langsmith/traceable";

   config(); // Load env vars from .env

   const openai = new OpenAI({
   apiKey: process.env.DEEPSEEK_API_KEY,
   baseURL: "https://api.deepseek.com/v1"
   });

   type ChatMessage = {
   role: "system" | "user" | "assistant";
   content: string;
   };

   const callDeepSeek = traceable(
   async (messages: ChatMessage[]) => {
       const response = await openai.chat.completions.create({
       model: "deepseek-chat",
       messages
       });

       return response.choices[0].message;
   },
   {
       name: "DeepSeek Chat Completion",
       run_type: "llm",
       metadata: {
       ls_provider: "deepseek",
       ls_model_name: "deepseek-chat"
       }
   }
   );

   (async () => {
   const messages: ChatMessage[] = [
       {
       role: "system",
       content: "You are a helpful assistant that translates English to French."
       },
       {
       role: "user",
       content: "I love programming."
       }
   ];

   const result = await callDeepSeek(messages);
   console.log("Model reply:", result.content);
   })();

   ```

   In this example, you use the OpenAI SDK to interact with [DeepSeek's API](https://api-docs.deepseek.com/). The OpenAI client is configured with `base_url="https://api.deepseek.com/v1"` to route requests to DeepSeek's endpoint while maintaining OpenAI-compatible syntax.

   The `@traceable` decorator (Python) or `traceable` function (TypeScript) wraps your function so that each invocation is logged as a trace run of type `"llm"`. The `metadata` parameter tags the trace with:

   * `ls_provider`: Identifies the provider (DeepSeek) for filtering traces.
   * `ls_model_name`: Specifies the model used for cost tracking and analytics.

   The function returns the full message object (`response.choices[0].message`), which includes the response content along with metadata like the role and any additional fields. LangSmith automatically captures:

   * Input messages sent to the model.
   * The model's complete response (content, role, etc.).
   * Model name and token usage statistics.
   * Execution timing and any errors.

2. Execute your script to generate a trace:

   ```bash Python
   python deepseek_trace.py
   ```

   ```bash TypeScript
   node deepseek_trace.js
   ```

   The function call will reach out to DeepSeek's API, and because of the `@traceable`/`traceable` wrapper, LangSmith will log this call's inputs and outputs as a new trace. You'll find the model's response printed to the console, and a corresponding run appear in the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-trace-deepseek).

## View traces in LangSmith

After running the example, you can inspect the recorded traces in the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-trace-deepseek):

1. Open the LangSmith UI and log in to your account.
2. Select the agent and environment configured during setup.
3. Find the trace corresponding to your DeepSeek API call. It will be identified by the function name (`DeepSeek Chat Completion`).
4. Click on the trace to open it. You'll be able to inspect the model input and output, including the prompt messages you sent and the response from DeepSeek, as well as timing information (latency) and token usage.

With LangSmith's tracing, you have full visibility into your DeepSeek calls—allowing you to debug the behavior of DeepSeek's models, monitor performance (response time and token usage), and compare runs with different parameters.

## Cost tracking

Although DeepSeek models are open-weight, using the hosted DeepSeek API may incur usage-based costs depending on your plan.

LangSmith can automatically associate costs with traced LLM calls by estimating token usage and applying model-specific pricing. When tracing DeepSeek API calls, LangSmith uses the recorded prompt and response messages to calculate token counts and attach cost information to each run.

To enable automatic cost tracking for LLM calls, refer to [Automatically track costs based on token counts](../../../Configuration%20%26%20troubleshooting/Cost%20tracking.md#llm-calls:-automatically-track-costs-based-on-token-counts).

Once enabled, costs appear directly in the LangSmith UI alongside each traced DeepSeek run, allowing you to monitor usage and compare experiments over time.

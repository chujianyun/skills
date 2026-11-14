# Trace with Mistral

[Mistral](https://mistral.ai/) provides hosted access to open-weight language models via a simple API.

This guide shows you how to trace Mistral API calls with LangSmith, allowing you to record prompts, responses, and metadata for debugging and observability. Traces are sent directly to LangSmith using the [LangSmith SDK](https://reference.langchain.com/python/langsmith/) and standard span instrumentation.

> [!NOTE]
>
> In an [agent-based workspace](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20Registry.md), [create an agent](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md) once before sending traces. Use [agent addressing](../../../Configuration%20%26%20troubleshooting/Agent%20%26%20environment%20settings/Log%20traces%20to%20an%20agent.md) to select its identifier and environment. If an integration requires `project_name`, use the selected environment's [`tracer_session_name`](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md#use-an-environment-project) as a compatibility value.

## Installation

Install Mistral’s official library and LangSmith:

```bash Python
pip install mistralai langsmith
```

```bash JavaScript
npm install @mistralai/mistralai langsmith dotenv
```

[`mistralai`](https://docs.mistral.ai/getting-started/clients) provides a Mistral client for interacting with Mistral’s API.

## Setup

Sending traces to an agent requires `langsmith>=0.14.9` in Python or `langsmith@>=0.11.0` in TypeScript.

Set your [API keys](../../../../../LangSmith%20setup/Account/Create%20an%20account%20and%20API%20key.md), agent identifier, and environment:

```bash
export MISTRAL_API_KEY="<API_KEY>"
export LANGSMITH_TRACING="true"
export LANGSMITH_API_KEY="<API_KEY>"
export LANGSMITH_AGENT_ID="<your-agent-id>"
export LANGSMITH_AGENT_ENVIRONMENT="local"
```

* Ensure you have a Mistral API key from your [Mistral AI account](https://v2.auth.mistral.ai/login) (set this as `MISTRAL_API_KEY`).
* Set `LANGSMITH_TRACING=true` and provide your LangSmith API key (`LANGSMITH_API_KEY`) activates automatic logging of traces.
* Set `LANGSMITH_AGENT_ID` and `LANGSMITH_AGENT_ENVIRONMENT` to the registered agent and environment.
* The `LANGSMITH_TRACING` flag must be true for any traces to be recorded.

## Configure tracing

1. Instrument the Mistral API call with LangSmith. In your script, create a Mistral client and wrap a call in a traced function:

   ```python Python
   import os
   from mistralai import Mistral
   from langsmith import traceable

   # Initialize Mistral API client with your API key
   client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])

   @traceable(
       run_type="llm",
       metadata={"ls_provider": "mistral", "ls_model_name": "mistral-medium-latest"},
   )
   def query_mistral(prompt: str):
       response = client.chat.complete(
           model="mistral-medium-latest",
           messages=[{"role": "user", "content": prompt}],
       )
       return response.choices[0].message

   # Example usage
   result = query_mistral("Hello, how are you?")
   print("Mistral response:", result.content)
   ```

   ```typescript TypeScript
   import { Client } from "langsmith";
   import { traceable } from "langsmith/traceable";
   import { Mistral } from "@mistralai/mistralai";
   import "dotenv/config";

   const mistral = new Mistral({
     apiKey: process.env.MISTRAL_API_KEY,
   });

   const langsmith = new Client();

   const tracedChatCompletion = traceable(
     async (params: {
       model: string;
       messages: Array<{ role: string; content: string }>;
     }) => {
       const response = await mistral.chat.complete(params);
       // Return the message content so LangSmith captures it correctly
       return response.choices[0].message.content;
     },
     {
       name: "Mistral Chat Completion",
       run_type: "llm",
       metadata: {
         ls_provider: "mistral",
         ls_model_name: "mistral-small-latest",
       },
     }
   );

   async function main() {
     const response = await tracedChatCompletion({
       model: "mistral-small-latest",
       messages: [
         { role: "user", content: "Say hello in one short sentence." },
       ],
     });

     console.log(response);
   }

   main();
   ```

   In this example, you use the [Mistral SDK](https://docs.mistral.ai/getting-started/clients) to send a chat completion request (with a user prompt) and retrieve the model’s answer.

   The [`@traceable`](https://reference.langchain.com/python/langsmith/run_helpers/traceable) decorator (from the [LangSmith Python SDK](https://reference.langchain.com/python/langsmith/observability/sdk/)) wraps the `query_mistral` function so that each invocation is logged as a trace run of type `"llm"`. The `metadata={"ls_provider": "mistral", "ls_model_name": "mistral-medium-latest"}` tags the trace with the provider (Mistral) and model name.

   You can also refer to the [LangSmith JavaScript SDK](../../../../Reference/langsmith%20%28smith-js-ts-sdk%29.md).

2. Execute your script to generate a trace. For example:

   ```bash Python
   python mistral_trace.py
   ```

   ```bash JavaScript
   node index.js
   ```

   The `query_mistral("Hello, how are you?")` call will reach out to the Mistral API, and because of the `@traceable`/`traceable` wrapper, LangSmith will log this call’s inputs and outputs as a new trace. You'll find the model’s response printed to the console, and a corresponding run appear in [LangSmith](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-trace-with-mistral).

## View traces in LangSmith

After running the example, you can inspect the recorded traces in the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-trace-with-mistral):

1. Open the LangSmith UI and log in to your account.
2. Select the agent and environment configured during setup.
3. Find the trace corresponding to your Mistral API call. It will be identified by the function name (`query_mistral`) or a custom name if provided.
4. Click on the trace to open it. You’ll be able to inspect the model input and output, including the prompt messages you sent and the response from Mistral, as well as timing information (latency) and any error details if the call failed.

With LangSmith’s tracing, you have full visibility into your Mistral calls—allowing you to debug the behavior of Mistral’s models, monitor performance (e.g., response time and token usage), and compare runs with different parameters using the metadata tags.

## Cost tracking

Although Mistral models are open-weight, using the hosted Mistral API may incur usage-based costs depending on your plan.

LangSmith can automatically associate costs with traced LLM calls by estimating token usage and applying model-specific pricing. When tracing Mistral API calls, LangSmith uses the recorded prompt and response messages to calculate token counts and attach cost information to each run.

To enable automatic cost tracking for LLM calls, refer to [Automatically track costs based on token counts](../../../Configuration%20%26%20troubleshooting/Cost%20tracking.md#llm-calls:-automatically-track-costs-based-on-token-counts).

Once enabled, costs appear directly in the LangSmith UI alongside each traced Mistral run, so that you can monitor usage and compare experiments over time.

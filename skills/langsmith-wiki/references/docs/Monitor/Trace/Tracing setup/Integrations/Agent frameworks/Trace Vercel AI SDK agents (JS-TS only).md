# Trace Vercel AI SDK agents (JS/TS only)

> Trace Vercel AI SDK agents with LangSmith for AI SDK v5, v6, and v7.

You can use LangSmith to trace runs from the Vercel AI SDK. This guide shows you how to set up tracing for AI SDK v5, v6, and v7.

> [!NOTE]
>
> In an [agent-based workspace](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20Registry.md), [create an agent](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md) once before sending traces. Use [agent addressing](../../../Configuration%20%26%20troubleshooting/Agent%20%26%20environment%20settings/Log%20traces%20to%20an%20agent.md) to select its identifier and environment. If an integration requires `project_name`, use the selected environment's [`tracer_session_name`](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md#use-an-environment-project) as a compatibility value.

## Installation

Install the Vercel AI SDK, a model provider package, and LangSmith. This guide uses Vercel's OpenAI integration for the following code snippets, but you can use any other Vercel AI SDK provider.

> [tab] AI SDK v7
>
> > [!NOTE]
> >
> > `LangSmithTelemetry` requires AI SDK v7 and is available in `langsmith>=0.7.2`.
>
> ```bash npm theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> npm install ai @ai-sdk/openai zod langsmith
> ```
>
> ```bash yarn theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> yarn add ai @ai-sdk/openai zod langsmith
> ```
>
> ```bash pnpm theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> pnpm add ai @ai-sdk/openai zod langsmith
> ```

> [tab] AI SDK v5 and v6
>
> > [!NOTE]
> >
> > `wrapAISDK` supports AI SDK v6 and requires `langsmith>=0.3.63`. If you are using an older version of the AI SDK or `langsmith`, refer to the [OpenTelemetry (OTEL) based approach](https://docs.langchain.com/langsmith/legacy-trace-with-vercel-ai-sdk).
>
> ```bash npm theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> npm install ai @ai-sdk/openai zod langsmith
> ```
>
> ```bash yarn theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> yarn add ai @ai-sdk/openai zod langsmith
> ```
>
> ```bash pnpm theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> pnpm add ai @ai-sdk/openai zod langsmith
> ```

## Environment configuration

```bash Shell
export LANGSMITH_TRACING=true
export LANGSMITH_API_KEY=<your-api-key>
export LANGSMITH_AGENT_ID="<your-agent-id>"
export LANGSMITH_AGENT_ENVIRONMENT="local"

# The examples use OpenAI, but you can use any LLM provider of choice
export OPENAI_API_KEY=<your-openai-api-key>

# For LangSmith API keys linked to multiple workspaces, set the LANGSMITH_WORKSPACE_ID environment variable to specify which workspace to use.
export LANGSMITH_WORKSPACE_ID=<your-workspace-id>
```

## Basic setup

> [tab] AI SDK v7
>
> Register `LangSmithTelemetry` once, then use AI SDK methods as you normally would.
>
> ```typescript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { openai } from "@ai-sdk/openai";
> import { generateText, registerTelemetry } from "ai";
> import { LangSmithTelemetry } from "langsmith/experimental/vercel";
>
> registerTelemetry(LangSmithTelemetry());
>
> await generateText({
>     model: openai("gpt-6-luna"),
>     prompt: "Write a vegetarian lasagna recipe for 4 people.",
> });
> ```
>
> You should see a trace in your LangSmith dashboard [like this one](https://smith.langchain.com/public/4f0e689e-c801-44d3-8857-93b47ab100cc/r).
>
> You can also trace runs with tool calls:
>
> ```typescript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { openai } from "@ai-sdk/openai";
> import { generateText, registerTelemetry, stepCountIs, tool } from "ai";
> import { LangSmithTelemetry } from "langsmith/experimental/vercel";
> import { z } from "zod";
>
> registerTelemetry(LangSmithTelemetry());
>
> await generateText({
>     model: openai("gpt-6-luna"),
>     messages: [
>         {
>             role: "user",
>             content: "What are my orders and where are they? My user ID is 123",
>         },
>     ],
>     tools: {
>         listOrders: tool({
>             description: "list all orders",
>             inputSchema: z.object({ userId: z.string() }),
>             execute: async ({ userId }) => `User ${userId} has the following orders: 1`,
>         }),
>         viewTrackingInformation: tool({
>             description: "view tracking information for a specific order",
>             inputSchema: z.object({ orderId: z.string() }),
>             execute: async ({ orderId }) => `Here is the tracking information for ${orderId}`,
>         }),
>     },
>     stopWhen: stepCountIs(5),
> });
> ```
>
> Which results in a trace like [this one](https://smith.langchain.com/public/6075fa2c-d255-4885-a66a-4fc798afaa9f/r).

> [tab] AI SDK v5 and v6
>
> Wrap the AI SDK methods once with `wrapAISDK`, then call the wrapped methods as you normally would.
>
> ```typescript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { openai } from "@ai-sdk/openai";
> import * as ai from "ai";
> import { wrapAISDK } from "langsmith/experimental/vercel";
>
> const { generateText } = wrapAISDK(ai);
>
> await generateText({
>     model: openai("gpt-6-luna"),
>     prompt: "Write a vegetarian lasagna recipe for 4 people.",
> });
> ```
>
> You can also trace runs with tool calls:
>
> ```typescript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { openai } from "@ai-sdk/openai";
> import * as ai from "ai";
> import { wrapAISDK } from "langsmith/experimental/vercel";
> import { z } from "zod";
>
> const { generateText, tool } = wrapAISDK(ai);
>
> await generateText({
>     model: openai("gpt-6-luna"),
>     messages: [
>         {
>             role: "user",
>             content: "What are my orders and where are they? My user ID is 123",
>         },
>     ],
>     tools: {
>         listOrders: tool({
>             description: "list all orders",
>             parameters: z.object({ userId: z.string() }),
>             execute: async ({ userId }) => `User ${userId} has the following orders: 1`,
>         }),
>         viewTrackingInformation: tool({
>             description: "view tracking information for a specific order",
>             parameters: z.object({ orderId: z.string() }),
>             execute: async ({ orderId }) => `Here is the tracking information for ${orderId}`,
>         }),
>     },
>     maxSteps: 5,
> });
> ```

You can use other AI SDK methods exactly as you usually would.

### With `traceable`

You can wrap `traceable` calls around AI SDK calls or within AI SDK tool calls. This is useful if you want to group runs together in LangSmith.

> [tab] AI SDK v7
>
> ```typescript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { openai } from "@ai-sdk/openai";
> import { generateText, registerTelemetry, stepCountIs, tool } from "ai";
> import { LangSmithTelemetry } from "langsmith/experimental/vercel";
> import { traceable } from "langsmith/traceable";
> import { z } from "zod";
>
> registerTelemetry(LangSmithTelemetry());
>
> const wrapper = traceable(
>     async (input: string) => {
>         const { text } = await generateText({
>             model: openai("gpt-6-luna"),
>             messages: [
>                 {
>                     role: "user",
>                     content: input,
>                 },
>             ],
>             tools: {
>                 listOrders: tool({
>                     description: "list all orders",
>                     inputSchema: z.object({ userId: z.string() }),
>                     execute: async ({ userId }) => `User ${userId} has the following orders: 1`,
>                 }),
>                 viewTrackingInformation: tool({
>                     description: "view tracking information for a specific order",
>                     inputSchema: z.object({ orderId: z.string() }),
>                     execute: async ({ orderId }) => `Here is the tracking information for ${orderId}`,
>                 }),
>             },
>             stopWhen: stepCountIs(5),
>         });
>         return text;
>     },
>     { name: "wrapper" },
> );
>
> await wrapper("What are my orders and where are they? My user ID is 123.");
> ```
>
> The resulting trace will look [like this](https://smith.langchain.com/public/ff25bc26-9389-4798-8b91-2bdcc95d4a8e/r).

> [tab] AI SDK v5 and v6
>
> ```typescript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { openai } from "@ai-sdk/openai";
> import * as ai from "ai";
> import { wrapAISDK } from "langsmith/experimental/vercel";
> import { traceable } from "langsmith/traceable";
> import { z } from "zod";
>
> const { generateText, tool } = wrapAISDK(ai);
>
> const wrapper = traceable(
>     async (input: string) => {
>         const { text } = await generateText({
>             model: openai("gpt-6-luna"),
>             messages: [
>                 {
>                     role: "user",
>                     content: input,
>                 },
>             ],
>             tools: {
>                 listOrders: tool({
>                     description: "list all orders",
>                     parameters: z.object({ userId: z.string() }),
>                     execute: async ({ userId }) => `User ${userId} has the following orders: 1`,
>                 }),
>                 viewTrackingInformation: tool({
>                     description: "view tracking information for a specific order",
>                     parameters: z.object({ orderId: z.string() }),
>                     execute: async ({ orderId }) => `Here is the tracking information for ${orderId}`,
>                 }),
>             },
>             maxSteps: 5,
>         });
>         return text;
>     },
>     { name: "wrapper" },
> );
>
> await wrapper("What are my orders and where are they? My user ID is 123.");
> ```

## Tracing in serverless environments

When tracing in serverless environments, wait for all runs to flush before your environment shuts down.

> [tab] AI SDK v7
>
> Pass a LangSmith [`Client`](https://reference.langchain.com/javascript/langsmith/client/Client) instance to `LangSmithTelemetry`, then call `await client.awaitPendingTraceBatches()`. Make sure to also pass it into any `traceable` wrappers you create:
>
> ```typescript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { openai } from "@ai-sdk/openai";
> import { generateText, stepCountIs, tool } from "ai";
> import { Client } from "langsmith";
> import { LangSmithTelemetry } from "langsmith/experimental/vercel";
> import { traceable } from "langsmith/traceable";
> import { z } from "zod";
>
> const client = new Client();
> const telemetry = LangSmithTelemetry({ client });
>
> const wrapper = traceable(
>     async (input: string) => {
>         const { text } = await generateText({
>             model: openai("gpt-6-luna"),
>             messages: [
>                 {
>                     role: "user",
>                     content: input,
>                 },
>             ],
>             tools: {
>                 listOrders: tool({
>                     description: "list all orders",
>                     inputSchema: z.object({ userId: z.string() }),
>                     execute: async ({ userId }) => `User ${userId} has the following orders: 1`,
>                 }),
>                 viewTrackingInformation: tool({
>                     description: "view tracking information for a specific order",
>                     inputSchema: z.object({ orderId: z.string() }),
>                     execute: async ({ orderId }) => `Here is the tracking information for ${orderId}`,
>                 }),
>             },
>             stopWhen: stepCountIs(5),
>             telemetry: { integrations: [telemetry] },
>         });
>         return text;
>     },
>     {
>         name: "wrapper",
>         client,
>     },
> );
>
> try {
>     await wrapper("What are my orders and where are they? My user ID is 123.");
> } finally {
>     await client.awaitPendingTraceBatches();
> }
> ```

> [tab] AI SDK v5 and v6
>
> Pass a LangSmith [`Client`](https://reference.langchain.com/javascript/langsmith/client/Client) instance to `wrapAISDK` and any `traceable` wrappers you create, then call `await client.awaitPendingTraceBatches()`:
>
> ```typescript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { openai } from "@ai-sdk/openai";
> import * as ai from "ai";
> import { Client } from "langsmith";
> import { wrapAISDK } from "langsmith/experimental/vercel";
> import { traceable } from "langsmith/traceable";
> import { z } from "zod";
>
> const client = new Client();
> const { generateText, tool } = wrapAISDK(ai, { client });
>
> const wrapper = traceable(
>     async (input: string) => {
>         const { text } = await generateText({
>             model: openai("gpt-6-luna"),
>             messages: [
>                 {
>                     role: "user",
>                     content: input,
>                 },
>             ],
>             tools: {
>                 listOrders: tool({
>                     description: "list all orders",
>                     parameters: z.object({ userId: z.string() }),
>                     execute: async ({ userId }) => `User ${userId} has the following orders: 1`,
>                 }),
>                 viewTrackingInformation: tool({
>                     description: "view tracking information for a specific order",
>                     parameters: z.object({ orderId: z.string() }),
>                     execute: async ({ orderId }) => `Here is the tracking information for ${orderId}`,
>                 }),
>             },
>             maxSteps: 5,
>         });
>         return text;
>     },
>     {
>         name: "wrapper",
>         client,
>     },
> );
>
> try {
>     await wrapper("What are my orders and where are they? My user ID is 123.");
> } finally {
>     await client.awaitPendingTraceBatches();
> }
> ```

If you are using `Next.js`, there is a convenient [`after`](https://nextjs.org/docs/app/api-reference/functions/after) hook where you can put this logic:

```typescript
import { after } from "next/server";
import { Client } from "langsmith";

export async function POST(request: Request) {
    const client = new Client();
    const body = await request.json();

    after(async () => {
        await client.awaitPendingTraceBatches();
    });

    return Response.json({ ok: true, body });
}
```

See [Trace JS functions in serverless environments](../../../Configuration%20%26%20troubleshooting/Advanced%20tracing%20techniques/Trace%20JS%20functions%20in%20serverless%20environments.md) for more detail, including information around managing rate limits in serverless environments.

## Passing LangSmith config

You can pass LangSmith-specific config such as metadata, run names, tags, and custom client instances.

> [tab] AI SDK v7
>
> If you register the integration globally, the config applies to future AI SDK calls:
>
> ```typescript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { openai } from "@ai-sdk/openai";
> import { generateText, registerTelemetry } from "ai";
> import { LangSmithTelemetry } from "langsmith/experimental/vercel";
>
> registerTelemetry(
>     LangSmithTelemetry({
>         metadata: { key_for_all_runs: "value" },
>         tags: ["myrun"],
>     }),
> );
>
> await generateText({
>     model: openai("gpt-6-luna"),
>     prompt: "Write a vegetarian lasagna recipe for 4 people.",
> });
> ```
>
> To apply config to a single run, pass a telemetry integration in that AI SDK call:
>
> ```typescript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { openai } from "@ai-sdk/openai";
> import { generateText } from "ai";
> import { LangSmithTelemetry } from "langsmith/experimental/vercel";
>
> await generateText({
>     model: openai("gpt-6-luna"),
>     prompt: "Write a vegetarian lasagna recipe for 4 people.",
>     telemetry: {
>         integrations: [
>             LangSmithTelemetry({
>                 metadata: { individual_key: "value" },
>                 name: "my_individual_run",
>             }),
>         ],
>     },
> });
> ```

> [tab] AI SDK v5 and v6
>
> If you pass config into `wrapAISDK`, the config applies to the wrapped methods:
>
> ```typescript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { openai } from "@ai-sdk/openai";
> import * as ai from "ai";
> import { wrapAISDK } from "langsmith/experimental/vercel";
>
> const { generateText } = wrapAISDK(ai, {
>     metadata: { key_for_all_runs: "value" },
>     tags: ["myrun"],
> });
>
> await generateText({
>     model: openai("gpt-6-luna"),
>     prompt: "Write a vegetarian lasagna recipe for 4 people.",
> });
> ```
>
> To apply config to a single run, pass LangSmith provider options in that AI SDK call:
>
> ```typescript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { openai } from "@ai-sdk/openai";
> import * as ai from "ai";
> import {
>     createLangSmithProviderOptions,
>     wrapAISDK,
> } from "langsmith/experimental/vercel";
>
> const { generateText } = wrapAISDK(ai);
>
> await generateText({
>     model: openai("gpt-6-luna"),
>     prompt: "Write a vegetarian lasagna recipe for 4 people.",
>     providerOptions: {
>         langsmith: createLangSmithProviderOptions<typeof ai.generateText>({
>             metadata: { individual_key: "value" },
>             name: "my_individual_run",
>         }),
>     },
> });
> ```

## Redacting data

You can customize what inputs and outputs the AI SDK sends to LangSmith by specifying custom input/output processing functions. This is useful if you are dealing with sensitive data that you would like to avoid sending to LangSmith.

Because output formats vary depending on which AI SDK method you are using, we suggest defining and passing telemetry config individually into AI SDK calls. You will also need to provide separate functions for child LLM runs within AI SDK calls, since calling `generateText` at top level calls the LLM internally and can do so multiple times.

Here's an example for `generateText`:

> [tab] AI SDK v7
>
> ```typescript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { openai } from "@ai-sdk/openai";
> import { generateText } from "ai";
> import { LangSmithTelemetry } from "langsmith/experimental/vercel";
>
> const telemetry = LangSmithTelemetry({
>     processInputs: (inputs) => {
>         const messages = inputs.messages as Array<Record<string, unknown>> | undefined;
>         return {
>             messages: messages?.map((message) => ({
>                 providerMetadata: message.providerOptions,
>                 role: "assistant",
>                 content: "REDACTED",
>             })),
>             prompt: "REDACTED",
>         };
>     },
>     processOutputs: (outputs) => {
>         return {
>             providerMetadata: outputs.providerMetadata,
>             role: "assistant",
>             content: "REDACTED",
>         };
>     },
>     processChildLLMRunInputs: (inputs) => {
>         const messages = inputs.messages as Array<Record<string, unknown>> | undefined;
>         return {
>             messages: messages?.map((message) => ({
>                 ...message,
>                 content: "REDACTED CHILD INPUTS",
>             })),
>         };
>     },
>     processChildLLMRunOutputs: (outputs) => {
>         return {
>             providerMetadata: outputs.providerMetadata,
>             content: "REDACTED CHILD OUTPUTS",
>             role: "assistant",
>         };
>     },
> });
>
> const { text } = await generateText({
>     model: openai("gpt-6-luna"),
>     prompt: "What is the capital of France?",
>     telemetry: { integrations: [telemetry] },
> });
>
> console.log(text);
> ```

> [tab] AI SDK v5 and v6
>
> ```typescript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { openai } from "@ai-sdk/openai";
> import * as ai from "ai";
> import {
>     createLangSmithProviderOptions,
>     wrapAISDK,
> } from "langsmith/experimental/vercel";
>
> const { generateText } = wrapAISDK(ai);
>
> const langsmith = createLangSmithProviderOptions<typeof ai.generateText>({
>     processInputs: (inputs) => {
>         return {
>             messages: inputs.messages?.map((message) => ({
>                 providerMetadata: message.providerOptions,
>                 role: "assistant",
>                 content: "REDACTED",
>             })),
>             prompt: "REDACTED",
>         };
>     },
>     processOutputs: () => {
>         return {
>             role: "assistant",
>             content: "REDACTED",
>         };
>     },
>     processChildLLMRunInputs: (inputs) => {
>         return {
>             messages: inputs.prompt.map((message) => ({
>                 ...message,
>                 content: "REDACTED CHILD INPUTS",
>             })),
>         };
>     },
>     processChildLLMRunOutputs: () => {
>         return {
>             content: "REDACTED CHILD OUTPUTS",
>             role: "assistant",
>         };
>     },
> });
>
> const { text } = await generateText({
>     model: openai("gpt-6-luna"),
>     prompt: "What is the capital of France?",
>     providerOptions: { langsmith },
> });
>
> console.log(text);
> ```

The actual return value will contain the original, non-redacted result, but the trace in LangSmith will be redacted.

For redacting tool input/output, wrap your `execute` method in a `traceable` like this:

> [tab] AI SDK v7
>
> ```typescript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { openai } from "@ai-sdk/openai";
> import { generateText, stepCountIs, tool } from "ai";
> import { Client } from "langsmith";
> import { LangSmithTelemetry } from "langsmith/experimental/vercel";
> import { traceable } from "langsmith/traceable";
> import { z } from "zod";
>
> const client = new Client();
> const telemetry = LangSmithTelemetry({ client });
>
> await generateText({
>     model: openai("gpt-6-luna"),
>     messages: [
>         {
>             role: "user",
>             content: "What are my orders? My user ID is 123.",
>         },
>     ],
>     tools: {
>         listOrders: tool({
>             description: "list all orders",
>             inputSchema: z.object({ userId: z.string() }),
>             execute: traceable(
>                 async ({ userId }) => {
>                     return `User ${userId} has the following orders: 1`;
>                 },
>                 {
>                     processInputs: () => ({ text: "REDACTED" }),
>                     processOutputs: () => ({ text: "REDACTED" }),
>                     run_type: "tool",
>                     name: "listOrders",
>                 },
>             ) as (input: { userId: string }) => Promise<string>,
>         }),
>     },
>     stopWhen: stepCountIs(5),
>     telemetry: { integrations: [telemetry] },
> });
>
> await client.awaitPendingTraceBatches();
> ```

> [tab] AI SDK v5 and v6
>
> ```typescript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { openai } from "@ai-sdk/openai";
> import * as ai from "ai";
> import { Client } from "langsmith";
> import { wrapAISDK } from "langsmith/experimental/vercel";
> import { traceable } from "langsmith/traceable";
> import { z } from "zod";
>
> const client = new Client();
> const { generateText, tool } = wrapAISDK(ai, { client });
>
> await generateText({
>     model: openai("gpt-6-luna"),
>     messages: [
>         {
>             role: "user",
>             content: "What are my orders? My user ID is 123.",
>         },
>     ],
>     tools: {
>         listOrders: tool({
>             description: "list all orders",
>             parameters: z.object({ userId: z.string() }),
>             execute: traceable(
>                 async ({ userId }) => {
>                     return `User ${userId} has the following orders: 1`;
>                 },
>                 {
>                     processInputs: () => ({ text: "REDACTED" }),
>                     processOutputs: () => ({ text: "REDACTED" }),
>                     run_type: "tool",
>                     name: "listOrders",
>                 },
>             ) as (input: { userId: string }) => Promise<string>,
>         }),
>     },
>     maxSteps: 5,
> });
>
> await client.awaitPendingTraceBatches();
> ```

The `traceable` return type is complex, which makes the cast necessary. You may also omit the AI SDK `tool` helper if you wish to avoid the cast.

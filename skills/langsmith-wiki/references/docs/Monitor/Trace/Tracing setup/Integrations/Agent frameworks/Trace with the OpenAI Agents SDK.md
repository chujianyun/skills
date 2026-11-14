# Trace with the OpenAI Agents SDK

> Trace OpenAI Agents SDK Python and JavaScript agents with LangSmith.

The OpenAI Agents SDK lets you build agents powered by OpenAI models.

Use LangSmith to trace OpenAI Agents SDK runs, including agent steps, model calls, tool calls, and handoffs.

> [!NOTE]
>
> In an [agent-based workspace](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20Registry.md), [create an agent](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md) once before sending traces. Use [agent addressing](../../../Configuration%20%26%20troubleshooting/Agent%20%26%20environment%20settings/Log%20traces%20to%20an%20agent.md) to select its identifier and environment. If an integration requires `project_name`, use the selected environment's [`tracer_session_name`](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md#use-an-environment-project) as a compatibility value.

> [tab] Python
>
> ## Installation
>
> > [!NOTE]
> >
> > Requires Python SDK version `langsmith>=0.3.15`.
>
> Install LangSmith with OpenAI Agents support:
>
> ```bash pip theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> pip install "langsmith[openai-agents]"
> ```
>
> ```bash uv theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> uv add "langsmith[openai-agents]"
> ```
>
> This installs both the LangSmith library and the OpenAI Agents SDK.
>
> ## Environment configuration
>
> Sending traces to an agent requires `langsmith>=0.14.9`.
>
> ```bash Shell theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> export LANGSMITH_API_KEY=<your-api-key>
> export OPENAI_API_KEY=<your-openai-api-key>
>
> # Select the registered agent and environment
> export LANGSMITH_AGENT_ID="<your-agent-id>"
> export LANGSMITH_AGENT_ENVIRONMENT="local"
>
> # For LangSmith API keys linked to multiple workspaces, set the LANGSMITH_WORKSPACE_ID environment variable to specify which workspace to use.
> export LANGSMITH_WORKSPACE_ID=<your-workspace-id>
> ```
>
> ## Quick start
>
> Integrate LangSmith tracing with the OpenAI Agents SDK by using the `OpenAIAgentsTracingProcessor` class.
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import asyncio
>
> from agents import Agent, Runner, set_trace_processors
> from langsmith.integrations.openai_agents_sdk import OpenAIAgentsTracingProcessor
>
>
> async def main():
>     agent = Agent(
>         name="Captain Obvious",
>         instructions="You are Captain Obvious, the world's most literal technical support agent.",
>     )
>
>     question = "Why is my code failing when I try to divide by zero? I keep getting this error message."
>     result = await Runner.run(agent, question)
>     print(result.final_output)
>
>
> if __name__ == "__main__":
>     set_trace_processors([OpenAIAgentsTracingProcessor()])
>     asyncio.run(main())
> ```
>
> The agent's execution flow, including spans and their details, is logged to LangSmith.

> [tab] JavaScript
>
> ## Installation
>
> > [!NOTE]
> >
> > Requires JS SDK version `langsmith>=0.5.25`.
>
> Install LangSmith and the OpenAI Agents SDK:
>
> ```bash npm theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> npm install langsmith @openai/agents zod
> ```
>
> ```bash yarn theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> yarn add langsmith @openai/agents zod
> ```
>
> ```bash pnpm theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> pnpm add langsmith @openai/agents zod
> ```
>
> ## Environment configuration
>
> Sending traces to an agent requires `langsmith@>=0.11.0`.
>
> ```bash Shell theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> export LANGSMITH_API_KEY=<your-api-key>
> export OPENAI_API_KEY=<your-openai-api-key>
>
> # Select the registered agent and environment
> export LANGSMITH_AGENT_ID="<your-agent-id>"
> export LANGSMITH_AGENT_ENVIRONMENT="local"
>
> # For LangSmith API keys linked to multiple workspaces, set the LANGSMITH_WORKSPACE_ID environment variable to specify which workspace to use.
> export LANGSMITH_WORKSPACE_ID=<your-workspace-id>
> ```
>
> > [!NOTE]
> >
> > Installing `OpenAIAgentsTracingProcessor` is an explicit opt-in to tracing. The processor posts traces even when `LANGSMITH_TRACING` is not set, and nested `traceable` calls inside agent tools inherit the active trace context.
>
> ## Quick start
>
> Register `OpenAIAgentsTracingProcessor` with the OpenAI Agents SDK before running agents.
>
> ```typescript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { Agent, run, setTraceProcessors, tool } from "@openai/agents";
> import { z } from "zod";
>
> import { OpenAIAgentsTracingProcessor } from "langsmith/wrappers/openai_agents";
>
> setTraceProcessors([new OpenAIAgentsTracingProcessor()]);
>
> const getWeather = tool({
>   name: "get_weather",
>   description: "Get the current weather for a city",
>   parameters: z.object({
>     city: z.string().describe("The city to get weather for"),
>   }),
>   execute: async ({ city }: { city: string }) => {
>     return `The weather in ${city} is sunny.`;
>   },
> });
>
> const agent = new Agent({
>   name: "WeatherAgent",
>   instructions: "You are a helpful assistant. Use the get_weather tool when asked about weather.",
>   model: "gpt-6-luna",
>   tools: [getWeather],
> });
>
> const result = await run(agent, "What's the weather in San Francisco?");
> console.log(result.finalOutput);
> ```
>
> The resulting trace contains the root agent run, response spans, and nested tool call spans.
>
> ## Configure the processor
>
> Pass options to the processor to set a LangSmith client, tags, metadata, or root trace name. Leave `projectName` unset to use the configured agent and environment.
>
> ```typescript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { Agent, run, setTraceProcessors } from "@openai/agents";
>
> import { Client } from "langsmith";
> import { OpenAIAgentsTracingProcessor } from "langsmith/wrappers/openai_agents";
>
> const client = new Client();
> const processor = new OpenAIAgentsTracingProcessor({
>   client,
>   name: "Support agent workflow",
>   tags: ["openai-agents"],
>   metadata: {
>     environment: "development",
>   },
> });
>
> setTraceProcessors([processor]);
>
> const agent = new Agent({
>   name: "SupportAgent",
>   instructions: "You are a concise support agent.",
>   model: "gpt-6-luna",
> });
>
> const result = await run(agent, "Help me reset my password.");
> console.log(result.finalOutput);
> ```
>
> ## Nest `traceable` calls in tools
>
> You can use `traceable` inside OpenAI Agents SDK tool handlers. LangSmith nests those runs under the active tool span.
>
> ```typescript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { Agent, run, setTraceProcessors, tool } from "@openai/agents";
> import { z } from "zod";
>
> import { traceable } from "langsmith/traceable";
> import { OpenAIAgentsTracingProcessor } from "langsmith/wrappers/openai_agents";
>
> setTraceProcessors([new OpenAIAgentsTracingProcessor()]);
>
> const lookupOrder = traceable(
>   async (orderId: string) => {
>     return { orderId, status: "shipped" };
>   },
>   { name: "lookup_order" }
> );
>
> const orderStatus = tool({
>   name: "order_status",
>   description: "Look up the status of an order",
>   parameters: z.object({
>     orderId: z.string().describe("The order ID to look up"),
>   }),
>   execute: async ({ orderId }: { orderId: string }) => {
>     return JSON.stringify(await lookupOrder(orderId));
>   },
> });
>
> const agent = new Agent({
>   name: "OrdersAgent",
>   instructions: "Use the order_status tool to answer order questions.",
>   model: "gpt-6-luna",
>   tools: [orderStatus],
> });
>
> await run(agent, "Where is order 123?");
> ```
>
> ## Flush traces in serverless environments
>
> When tracing in serverless environments, flush pending traces before the process exits.
>
> ```typescript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { Agent, run, setTraceProcessors } from "@openai/agents";
>
> import { Client } from "langsmith";
> import { OpenAIAgentsTracingProcessor } from "langsmith/wrappers/openai_agents";
>
> const client = new Client();
> const processor = new OpenAIAgentsTracingProcessor({ client });
> setTraceProcessors([processor]);
>
> try {
>   const agent = new Agent({
>     name: "SupportAgent",
>     instructions: "You are a concise support agent.",
>     model: "gpt-6-luna",
>   });
>
>   const result = await run(agent, "Help me reset my password.");
>   console.log(result.finalOutput);
> } finally {
>   await processor.forceFlush();
> }
> ```

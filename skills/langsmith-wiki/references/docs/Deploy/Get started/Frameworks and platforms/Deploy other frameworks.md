# Deploy other frameworks

> Deploy agents built with Claude Agent SDK, Strands, CrewAI, AutoGen, and other frameworks to LangSmith Agent Server.

This guide is the how-to for deploying agents built outside LangGraph (Claude Agent SDK, Strands, CrewAI, AutoGen, and similar) to [LangSmith Agent Server](../LangSmith%20Agent%20Server.md), including tracing for [LangSmith Observability](../../../Monitor/Overview/LangSmith%20Observability.md). It walks through wrapping those agents with the [Functional API](https://docs.langchain.com/oss/python/langgraph/functional-api.md) so Agent Server can run them. For Functional API concepts (entrypoints, tasks, checkpointing, and resume rules), see the [Functional API overview](https://docs.langchain.com/oss/python/langgraph/functional-api.md).

LangSmith Agent Server runs any framework. For agents not built on Deep Agents, LangChain, or LangGraph, deploy using either the [`deployments-wrap-sdk`](https://pypi.org/project/deployments-wrap-sdk/) package (Google ADK) or the LangGraph Functional API (Claude Agent SDK, Strands, CrewAI, AutoGen, and other libraries).

> [!TIP]
>
> For new builds, consider [Managed Deep Agents](../../../Build/Python/Deep%20Agents/Deployment/Managed%20Deep%20Agents.md): a managed open-source harness for agents that plan, use tools, delegate to subagents, and work over long horizons. Alternatively, for maximum flexibility while using the same Deep Agents harness, use the [Deep Agents SDK](https://docs.langchain.com/oss/python/deepagents/overview.md#self-host-with-the-sdk) and host agents yourself, or run a custom [Agent Server](../LangSmith%20Agent%20Server.md).

## Supported frameworks

The following frameworks have end-to-end examples in this guide. Each example exports a LangGraph-compatible graph from `agent.py` that [Agent Server](../../Agent%20Server/Capabilities/Agent%20Server.md) can serve:

![](../../../../assets/images/6bac5875cc87-claude.svg)

Claude Agent SDK

[Open](#general-deployment-pattern)

![](../../../../assets/images/cefeaef310a0-bedrock.svg)

Strands Agents

[Open](#general-deployment-pattern)

![](../../../../assets/images/101363e871a8-crewai.svg)

CrewAI

[Open](#general-deployment-pattern)

![](../../../../assets/images/5a098c2a6bc2-autogen.svg)

AutoGen

[Open](#general-deployment-pattern)

> [!NOTE]
>
> Don't see your framework? The Functional API accepts any callable, so you can apply the same pattern shown in the following examples to any agent library. Wrap your agent's entrypoint with `@task` and `@entrypoint`, then deploy.

## How the Functional API works

When a run arrives on Agent Server for a Functional API-wrapped agent:

1. The platform invokes your `@entrypoint`-decorated `agent` function with the run input and any saved state from prior turns on the same thread (passed as the `previous` argument).
2. The entrypoint calls your `@task`-decorated function, which delegates to the framework agent (Claude Agent SDK, Strands, CrewAI, AutoGen, or another library).
3. The entrypoint returns `entrypoint.final(value=..., save=...)`. The `value` is the response for this turn; `save` is the checkpointed state used as `previous` on the next turn.
4. Agent Server persists the checkpoint, streams partial output when supported, and records traces when tracing is configured.

This pattern preserves your framework's execution semantics while giving you standard Agent Server features: durable runs, multi-thread persistence, streaming endpoints, and LangSmith observability.

## Prerequisites

Regardless of framework, you need:

* Python 3.10+ for Functional API frameworks (Strands Agents supports Python 3.9+)
* A [LangSmith API key](../../../LangSmith%20setup/Account/Create%20an%20account%20and%20API%20key.md)

## General deployment pattern

Follow the same steps for each framework. Choose your stack in the tabs inside each step, combine the snippets in one module (for example `agent.py`), and export the `@entrypoint`-decorated function as a module-level variable named `agent`. The [end-to-end example](#end-to-end-example) section shows complete files you can copy.

**1. Install dependencies**

Install Python packages for your framework plus LangGraph and LangSmith.

> [tab] Claude Agent SDK
>
> For [Claude Agent SDK](https://docs.claude.com/en/api/agent-sdk/overview):
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> pip install "langsmith[claude-agent-sdk]" langgraph "langgraph-cli[inmem]"
> ```
>
> Set `ANTHROPIC_API_KEY` in your environment. For an Anthropic API key, refer to the [Claude console](https://claude.ai/login).

> [tab] Strands Agents
>
> For [Strands Agents](https://strandsagents.com/docs/):
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> pip install strands-agents strands-agents-tools langgraph "langsmith[strands-agents]" "langgraph-cli[inmem]"
> ```
>
> Configure AWS credentials if you use Amazon Bedrock as the model provider.

> [tab] CrewAI
>
> For [CrewAI](https://docs.crewai.com/):
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> pip install crewai langgraph langsmith opentelemetry-instrumentation-crewai opentelemetry-instrumentation-openai "langgraph-cli[inmem]"
> ```
>
> Set LLM provider credentials in your environment (for example `OPENAI_API_KEY` if you use OpenAI-backed models).

> [tab] AutoGen
>
> For [AutoGen](https://microsoft.github.io/autogen/):
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> pip install autogen-agentchat autogen-ext langgraph langsmith opentelemetry-instrumentation-openai "langgraph-cli[inmem]"
> ```
>
> Set `OPENAI_API_KEY` (or your model provider credentials) in your environment.

**2. Define your agent**

Build your agent using the framework of your choice, exactly as you would outside of LangSmith.

> [tab] Claude Agent SDK
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from claude_agent_sdk import ClaudeAgentOptions
>
> options = ClaudeAgentOptions(
>     model="claude-sonnet-5-5",
>     system_prompt="You are a helpful assistant.",
> )
> ```

> [tab] Strands Agents
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from strands import Agent
>
> strands_agent = Agent(
>     system_prompt="You are a helpful assistant.",
>     model="us.anthropic.claude-sonnet-4-20250514-v1:0",
> )
> ```

> [tab] CrewAI
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from crewai import Agent as CrewAgent, Crew, Task
>
> researcher = CrewAgent(role="Researcher", goal="Research a topic", backstory="Expert researcher.")
> crew = Crew(
>     agents=[researcher],
>     tasks=[Task(description="{topic}", agent=researcher, expected_output="A short report.")],
> )
> ```

> [tab] AutoGen
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from autogen_agentchat.agents import AssistantAgent
> from autogen_ext.models.openai import OpenAIChatCompletionClient
>
> assistant = AssistantAgent(
>     name="assistant",
>     model_client=OpenAIChatCompletionClient(model="gpt-6.1-sol"),
> )
> ```

**3. Wrap with the Functional API**

Expose your agent through an `@entrypoint`-decorated function named `agent`. Inside, use `@task` for the unit of work that calls into the framework. Use `entrypoint.final()` to return the response and persist conversation history across turns on the same thread.

> [tab] Claude Agent SDK
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import operator
>
> from claude_agent_sdk import ClaudeSDKClient
> from langgraph.func import entrypoint, task
>
> @task
> async def invoke_claude(prompt: str) -> str:
>     async with ClaudeSDKClient(options=options) as client:
>         await client.query(prompt)
>         chunks: list[str] = []
>         async for message in client.receive_response():
>             chunks.append(str(message))
>         return "\n".join(chunks)
>
> @entrypoint()
> async def agent(messages: list[dict], previous: list[dict] | None = None):
>     history = operator.add(previous or [], messages)
>     prompt = history[-1]["content"]
>     response = await invoke_claude(prompt)
>     new_message = {"role": "assistant", "content": response}
>     return entrypoint.final(
>         value=[new_message],
>         save=operator.add(history, [new_message]),
>     )
> ```

> [tab] Strands Agents
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import operator
>
> from langgraph.func import entrypoint, task
> from strands.types.content import Message
>
> @task
> def invoke_strands(messages: list[Message]):
>     result = strands_agent(messages)
>     return [result.message]
>
> @entrypoint()
> def agent(messages: list[Message], previous: list[Message] | None = None):
>     messages = operator.add(previous or [], messages)
>     response = invoke_strands(messages).result()
>     return entrypoint.final(value=response, save=operator.add(messages, response))
> ```

> [tab] CrewAI
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import operator
>
> from langgraph.func import entrypoint, task
>
> @task
> def run_crew(topic: str) -> str:
>     return str(crew.kickoff(inputs={"topic": topic}))
>
> @entrypoint()
> def agent(messages: list[dict], previous: list[dict] | None = None):
>     history = operator.add(previous or [], messages)
>     response = run_crew(history[-1]["content"]).result()
>     new_message = {"role": "assistant", "content": response}
>     return entrypoint.final(value=[new_message], save=operator.add(history, [new_message]))
> ```

> [tab] AutoGen
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import operator
>
> from langgraph.func import entrypoint, task
>
> @task
> async def invoke_autogen(prompt: str) -> str:
>     result = await assistant.run(task=prompt)
>     return result.messages[-1].content
>
> @entrypoint()
> async def agent(messages: list[dict], previous: list[dict] | None = None):
>     history = operator.add(previous or [], messages)
>     response = await invoke_autogen(history[-1]["content"])
>     new_message = {"role": "assistant", "content": response}
>     return entrypoint.final(value=[new_message], save=operator.add(history, [new_message]))
> ```

**4. Configure tracing**

Forward the framework's native traces to LangSmith. Call tracing setup once at application startup, before creating or invoking agents.

> [tab] Claude Agent SDK
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langsmith.integrations.claude_agent_sdk import configure_claude_agent_sdk
>
> configure_claude_agent_sdk()
> ```
>
> For full setup details, see [Trace Claude Agent SDK applications](../../../Monitor/Trace/Tracing%20setup/Integrations/Agent%20frameworks/Trace%20with%20the%20Claude%20Agent%20SDK.md).

> [tab] Strands Agents
>
> Set your [LangSmith API key](../../../LangSmith%20setup/Account/Create%20an%20account%20and%20API%20key.md) and project name. If you use Amazon Bedrock, also configure AWS credentials.
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langsmith.integrations.strands_agents import setup_langsmith_telemetry
>
> setup_langsmith_telemetry()
> ```
>
> > [!NOTE]
> >
> > If you're [self-hosting LangSmith](../../../LangSmith%20setup/Self-hosted/Self-hosted%20LangSmith.md), configure the OpenTelemetry OTLP endpoint and headers for your deployment. See [Trace Strands Agents applications](../../../Monitor/Trace/Tracing%20setup/Integrations/Agent%20frameworks/Trace%20with%20Strands%20Agents.md).
>
> > [!NOTE]
> >
> > Strands' OTel tracing contains synchronous code. You may need to set `BG_JOB_ISOLATED_LOOPS=true` when deploying to Agent Server. See [`BG_JOB_ISOLATED_LOOPS`](../../Deploy%20to%20Cloud/Reference/Cloud%20Agent%20Server%20environment%20variables.md#bg_job_isolated_loops).
>
> For full setup details, see [Trace Strands Agents applications](../../../Monitor/Trace/Tracing%20setup/Integrations/Agent%20frameworks/Trace%20with%20Strands%20Agents.md).

> [tab] CrewAI
>
> Register the LangSmith span processor with the CrewAI and OpenAI instrumentors:
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langsmith.integrations.otel import OtelSpanProcessor
> from opentelemetry import trace
> from opentelemetry.instrumentation.crewai import CrewAIInstrumentor
> from opentelemetry.instrumentation.openai import OpenAIInstrumentor
> from opentelemetry.sdk.trace import TracerProvider
>
> current_provider = trace.get_tracer_provider()
> if isinstance(current_provider, TracerProvider):
>     tracer_provider = current_provider
> else:
>     tracer_provider = TracerProvider()
>     trace.set_tracer_provider(tracer_provider)
>
> tracer_provider.add_span_processor(OtelSpanProcessor())
> CrewAIInstrumentor().instrument(tracer_provider=tracer_provider)
> OpenAIInstrumentor().instrument(tracer_provider=tracer_provider)
> ```
>
> For full setup details, see [Trace CrewAI applications](../../../Monitor/Trace/Tracing%20setup/Integrations/Agent%20frameworks/Trace%20CrewAI%20agents.md).

> [tab] AutoGen
>
> Register the LangSmith span processor with the OpenAI instrumentor:
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langsmith.integrations.otel import OtelSpanProcessor
> from opentelemetry import trace
> from opentelemetry.instrumentation.openai import OpenAIInstrumentor
> from opentelemetry.sdk.trace import TracerProvider
>
> tracer_provider = TracerProvider()
> tracer_provider.add_span_processor(OtelSpanProcessor())
> trace.set_tracer_provider(tracer_provider)
> OpenAIInstrumentor().instrument()
> ```
>
> For full setup details, see [Trace AutoGen applications](../../../Monitor/Trace/Tracing%20setup/Integrations/Agent%20frameworks/Trace%20AutoGen%20agents.md).

## End-to-end example

The following examples combine agent definition, Functional API wrapping, tracing setup, and export of the `agent` symbol in a single `agent.py` file. Pick the tab for your framework.

> [tab] Claude Agent SDK
>
> ```python agent.py theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import operator
>
> from claude_agent_sdk import ClaudeAgentOptions, ClaudeSDKClient
> from langgraph.func import entrypoint, task
> from langsmith.integrations.claude_agent_sdk import configure_claude_agent_sdk
>
> configure_claude_agent_sdk()
>
> options = ClaudeAgentOptions(
>     model="claude-sonnet-5-5",
>     system_prompt="You are a helpful assistant.",
> )
>
> @task
> async def invoke_claude(prompt: str) -> str:
>     async with ClaudeSDKClient(options=options) as client:
>         await client.query(prompt)
>         chunks: list[str] = []
>         async for message in client.receive_response():
>             chunks.append(str(message))
>         return "\n".join(chunks)
>
> @entrypoint()
> async def agent(messages: list[dict], previous: list[dict] | None = None):
>     history = operator.add(previous or [], messages)
>     prompt = history[-1]["content"]
>     response = await invoke_claude(prompt)
>     new_message = {"role": "assistant", "content": response}
>     return entrypoint.final(
>         value=[new_message],
>         save=operator.add(history, [new_message]),
>     )
> ```

> [tab] Strands Agents
>
> ```python agent.py theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import operator
>
> from langgraph.func import entrypoint, task
> from langsmith.integrations.strands_agents import setup_langsmith_telemetry
> from strands import Agent
> from strands.types.content import Message
>
> setup_langsmith_telemetry()
>
> strands_agent = Agent(
>     system_prompt="You are a helpful assistant.",
>     model="us.anthropic.claude-sonnet-4-20250514-v1:0",
> )
>
> @task
> def invoke_strands(messages: list[Message]):
>     result = strands_agent(messages)
>     return [result.message]
>
> @entrypoint()
> def agent(messages: list[Message], previous: list[Message] | None = None):
>     messages = operator.add(previous or [], messages)
>     response = invoke_strands(messages).result()
>     return entrypoint.final(value=response, save=operator.add(messages, response))
> ```

> [tab] CrewAI
>
> ```python agent.py theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import operator
>
> from crewai import Agent as CrewAgent, Crew, Task
> from langgraph.func import entrypoint, task
> from langsmith.integrations.otel import OtelSpanProcessor
> from opentelemetry import trace
> from opentelemetry.instrumentation.crewai import CrewAIInstrumentor
> from opentelemetry.instrumentation.openai import OpenAIInstrumentor
> from opentelemetry.sdk.trace import TracerProvider
>
> current_provider = trace.get_tracer_provider()
> if isinstance(current_provider, TracerProvider):
>     tracer_provider = current_provider
> else:
>     tracer_provider = TracerProvider()
>     trace.set_tracer_provider(tracer_provider)
>
> tracer_provider.add_span_processor(OtelSpanProcessor())
> CrewAIInstrumentor().instrument(tracer_provider=tracer_provider)
> OpenAIInstrumentor().instrument(tracer_provider=tracer_provider)
>
> researcher = CrewAgent(role="Researcher", goal="Research a topic", backstory="Expert researcher.")
> crew = Crew(
>     agents=[researcher],
>     tasks=[Task(description="{topic}", agent=researcher, expected_output="A short report.")],
> )
>
> @task
> def run_crew(topic: str) -> str:
>     return str(crew.kickoff(inputs={"topic": topic}))
>
> @entrypoint()
> def agent(messages: list[dict], previous: list[dict] | None = None):
>     history = operator.add(previous or [], messages)
>     response = run_crew(history[-1]["content"]).result()
>     new_message = {"role": "assistant", "content": response}
>     return entrypoint.final(value=[new_message], save=operator.add(history, [new_message]))
> ```

> [tab] AutoGen
>
> ```python agent.py theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import operator
>
> from autogen_agentchat.agents import AssistantAgent
> from autogen_ext.models.openai import OpenAIChatCompletionClient
> from langgraph.func import entrypoint, task
> from langsmith.integrations.otel import OtelSpanProcessor
> from opentelemetry import trace
> from opentelemetry.instrumentation.openai import OpenAIInstrumentor
> from opentelemetry.sdk.trace import TracerProvider
>
> tracer_provider = TracerProvider()
> tracer_provider.add_span_processor(OtelSpanProcessor())
> trace.set_tracer_provider(tracer_provider)
> OpenAIInstrumentor().instrument()
>
> assistant = AssistantAgent(
>     name="assistant",
>     model_client=OpenAIChatCompletionClient(model="gpt-6.1-sol"),
> )
>
> @task
> async def invoke_autogen(prompt: str) -> str:
>     result = await assistant.run(task=prompt)
>     return result.messages[-1].content
>
> @entrypoint()
> async def agent(messages: list[dict], previous: list[dict] | None = None):
>     history = operator.add(previous or [], messages)
>     response = await invoke_autogen(history[-1]["content"])
>     new_message = {"role": "assistant", "content": response}
>     return entrypoint.final(value=[new_message], save=operator.add(history, [new_message]))
> ```

Two things are essential for every example:

1. **Export the `@entrypoint`-decorated function as `agent`** at module scope. Agent Server imports this symbol when serving the graph.
2. **Return `entrypoint.final()` with a `save` argument** so conversation state persists across turns on the same thread.

## Project layout

A deployable project needs these files:

```
my-agent/
├── agent.py              # exports the agent graph
├── langgraph.json        # Agent Server config
├── pyproject.toml        # Python dependencies
└── .env                  # Provider credentials and LangSmith variables
```

[`langgraph.json`](../../Agent%20Server/Develop%20your%20application/Application%20structure.md#configuration-file-concepts) points Agent Server at the exported symbol:

> [tab] Claude Agent SDK
>
> ```json langgraph.json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> {
>   "$schema": "https://langgra.ph/schema.json",
>   "dependencies": ["."],
>   "graphs": {
>     "claude_agent": "./agent.py:agent"
>   },
>   "env": ".env"
> }
> ```
>
> ```toml pyproject.toml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> [project]
> name = "my-claude-agent"
> version = "0.0.1"
> requires-python = ">=3.10"
> dependencies = [
>     "langsmith[claude-agent-sdk]>=0.3.0",
>     "langgraph>=0.4.0",
> ]
> ```
>
> ```bash .env theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> LANGSMITH_API_KEY=your-langsmith-api-key
> LANGSMITH_TRACING=true
> LANGSMITH_PROJECT=my-claude-agent
> ANTHROPIC_API_KEY=your-anthropic-api-key
> ```

> [tab] Strands Agents
>
> ```json langgraph.json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> {
>   "$schema": "https://langgra.ph/schema.json",
>   "dependencies": ["."],
>   "graphs": {
>     "strands_agent": "./agent.py:agent"
>   },
>   "env": ".env"
> }
> ```
>
> ```toml pyproject.toml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> [project]
> name = "my-strands-agent"
> version = "0.0.1"
> requires-python = ">=3.9"
> dependencies = [
>     "strands-agents>=0.1.0",
>     "strands-agents-tools>=0.1.0",
>     "langsmith[strands-agents]>=0.3.0",
>     "langgraph>=0.4.0",
> ]
> ```
>
> ```bash .env theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> LANGSMITH_API_KEY=your-langsmith-api-key
> LANGSMITH_TRACING=true
> LANGSMITH_PROJECT=my-strands-agent
> OTEL_EXPORTER_OTLP_TRACES_ENDPOINT=https://api.smith.langchain.com/otel/v1/traces
> OTEL_EXPORTER_OTLP_HEADERS=x-api-key=your-langsmith-api-key,Langsmith-Project=my-strands-agent
> AWS_REGION=your-aws-region
> AWS_PROFILE=your-aws-profile
> ```

> [tab] CrewAI
>
> ```json langgraph.json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> {
>   "$schema": "https://langgra.ph/schema.json",
>   "dependencies": ["."],
>   "graphs": {
>     "crewai_agent": "./agent.py:agent"
>   },
>   "env": ".env"
> }
> ```
>
> ```toml pyproject.toml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> [project]
> name = "my-crewai-agent"
> version = "0.0.1"
> requires-python = ">=3.10"
> dependencies = [
>     "crewai>=0.100.0",
>     "langgraph>=0.4.0",
>     "langsmith>=0.3.0",
>     "opentelemetry-instrumentation-crewai>=0.1.0",
>     "opentelemetry-instrumentation-openai>=0.1.0",
> ]
> ```
>
> ```bash .env theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> LANGSMITH_API_KEY=your-langsmith-api-key
> LANGSMITH_PROJECT=my-crewai-agent
> OPENAI_API_KEY=your-openai-api-key
> ```

> [tab] AutoGen
>
> ```json langgraph.json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> {
>   "$schema": "https://langgra.ph/schema.json",
>   "dependencies": ["."],
>   "graphs": {
>     "autogen_agent": "./agent.py:agent"
>   },
>   "env": ".env"
> }
> ```
>
> ```toml pyproject.toml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> [project]
> name = "my-autogen-agent"
> version = "0.0.1"
> requires-python = ">=3.10"
> dependencies = [
>     "autogen-agentchat>=0.4.0",
>     "autogen-ext>=0.4.0",
>     "langgraph>=0.4.0",
>     "langsmith>=0.3.0",
>     "opentelemetry-instrumentation-openai>=0.1.0",
> ]
> ```
>
> ```bash .env theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> LANGSMITH_API_KEY=your-langsmith-api-key
> LANGSMITH_PROJECT=my-autogen-agent
> OPENAI_API_KEY=your-openai-api-key
> ```

## Install dependencies

From your project directory:

```bash
pip install -e .
```

## Enable tracing

Use the framework-specific `.env` template in [Project layout](#project-layout). Agent Server loads this file when `"env": ".env"` is set in `langgraph.json`.

Set `LANGSMITH_PROJECT` and your framework provider credentials in that file. For Claude Agent SDK and Strands Agents, also set `LANGSMITH_TRACING=true`. For CrewAI and AutoGen, tracing is enabled in `agent.py` through `OtelSpanProcessor()` and the framework instrumentors, so set `LANGSMITH_API_KEY` and `LANGSMITH_PROJECT` only.

[Traces](../../../Monitor/Overview/LangSmith%20Observability.md) show agent invocations, tool calls, and LLM interactions in the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-deploy-other-frameworks). For framework-specific tracing options, see the links in [Configure tracing](#configure-tracing).

## Run locally

Start the local Agent Server with the [LangGraph CLI](../Reference/LangGraph%20CLI.md):

```bash
langgraph dev
```

> [!NOTE]
>
> If `langgraph dev` reports that `langgraph-api` is missing, install `langgraph-cli[inmem]` in the same environment.

This serves the agent at `http://127.0.0.1:2024` and opens [LangSmith Studio](../../../Test/Test%20from%20Studio/LangSmith%20Studio.md). Send a request with `curl`:

> [!NOTE]
>
> `langgraph dev` may serve on a different port. Check the URL in the terminal output and update the `curl` commands below if needed.

> [tab] Claude Agent SDK, CrewAI, AutoGen
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> # Create a thread
> THREAD=$(curl -s -X POST http://127.0.0.1:2024/threads \
>   -H "Content-Type: application/json" -d '{}' | python -c "import sys, json; print(json.load(sys.stdin)['thread_id'])")
>
> # Run the agent and wait for the final response
> curl -s -X POST "http://127.0.0.1:2024/threads/$THREAD/runs/wait" \
>   -H "Content-Type: application/json" \
>   -d '{
>     "assistant_id": "ASSISTANT_ID",
>     "input": [{"role": "user", "content": "Hello"}]
>   }'
> ```

> [tab] Strands Agents
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> # Create a thread
> THREAD=$(curl -s -X POST http://127.0.0.1:2024/threads \
>   -H "Content-Type: application/json" -d '{}' | python -c "import sys, json; print(json.load(sys.stdin)['thread_id'])")
>
> # Run the agent and wait for the final response
> curl -s -X POST "http://127.0.0.1:2024/threads/$THREAD/runs/wait" \
>   -H "Content-Type: application/json" \
>   -d '{
>     "assistant_id": "ASSISTANT_ID",
>     "input": [
>       {
>         "role": "user",
>         "content": [
>           {"type": "text", "text": "Hello"}
>         ]
>       }
>     ]
>   }'
> ```
>
> > [!NOTE]
> >
> > If this request fails with `NoCredentialsError`, configure AWS credentials for your model provider (for example `AWS_PROFILE` or `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`) and restart `langgraph dev`.

Replace `ASSISTANT_ID` with the graph key from your `langgraph.json` `graphs` object. For example, if your config is `"graphs": {"claude_agent": "./agent.py:agent"}`, use `claude_agent`; if your config is `"graphs": {"strands_agent": "./agent.py:agent"}`, use `strands_agent`.

> [!NOTE]
>
> [Verify that the LangGraph API runs locally](../Develop%20%26%20test/Local%20development%20%26%20testing.md) before deploying. If `langgraph dev` fails, deployment to LangSmith will fail as well.

## Deploy to LangSmith

Once the agent runs locally, deploy it with `langgraph deploy`:

```bash
langgraph deploy --name my-agent
```

For environment configuration, deployment types, and revision management, see [Deploy to cloud](../../Deploy%20to%20Cloud/Deployment%20guide/Create%20an%20Agent%20Server.md). For self-hosted setups, see [Self-hosted deployments](../../../LangSmith%20setup/Self-hosted/Self-hosted%20LangSmith.md). For Docker-only hosting without the control plane, see [Deploy standalone](../../Deploy%20to%20Self-hosted/Self-host%20standalone%20servers.md).

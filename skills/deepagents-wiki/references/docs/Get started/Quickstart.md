# Quickstart

> Build your first deep agent in minutes

This guide walks you through creating your first deep agent with the Deep Agents SDK. Use the SDK for maximum flexibility and host agents yourself or run a custom [LangSmith Deployment](https://docs.langchain.com/langsmith/deployment.md). To run agents in production without having to manage infrastructure, see the [Managed Deep Agents quickstart](https://docs.langchain.com/langsmith/python/managed-deep-agents-quickstart.md) instead.

You will build a research agent that can conduct research and write reports.

Build the Deep Agents research quickstart

Build a Deep Agents research agent in this working directory by following the Deep Agents quickstart.

## Step 1: Read the guide

Detect whether this project uses Python or TypeScript/JavaScript. Fetch and follow the matching page; treat it as the source of truth for package names, model strings, search-tool setup, and code:

* Python: [https://docs.langchain.com/oss/python/deepagents/quickstart.md](Quickstart.md)
* TypeScript: [https://docs.langchain.com/oss/javascript/deepagents/quickstart.md](https://docs.langchain.com/oss/javascript/deepagents/quickstart.md)

## Step 2: Install dependencies

Install `deepagents` (and `langchain` / `@langchain/core` on TypeScript) with the package manager already used in this project. Add Tavily only if the user is not using a Google, OpenAI, or Anthropic built-in provider search tool.

## Step 3: Configure model credentials

Check for a supported provider API key (for example `GOOGLE_API_KEY`, `OPENAI_API_KEY`, or `ANTHROPIC_API_KEY`). If none is set, ask the user which provider to use, then stop and wait while they create a key and set it in the shell or a `.env` file. Do not invent, hardcode, or commit API keys. If they need Tavily, ask them to set `TAVILY_API_KEY` the same way.

## Step 4: Implement the research agent

Follow the quickstart steps in order:

1. Create the internet search tool (prefer the provider built-in search tool when the chosen model supports it; otherwise use Tavily).
2. Call `create_deep_agent` with the search tool, a `provider:model` string (or initialized model) from the guide, and the research system prompt shown on the page.
3. For optional LangSmith tracing, follow [https://docs.langchain.com/langsmith/create-an-agent](https://docs.langchain.com/langsmith/create-an-agent.md) to register an agent in an agent-based workspace. Ask the user to set `LANGSMITH_AGENT_ID`, `LANGSMITH_AGENT_ENVIRONMENT`, `LANGSMITH_TRACING=true`, and `LANGSMITH_API_KEY` themselves.
4. Run the agent on a sample research query from the guide and print the final response.

## Rules

* Stay scoped to this self-hosted SDK quickstart. Do not add Managed Deep Agents deployment, evals, or unrelated frameworks. If the user wants the managed path, point them to the Managed Deep Agents quickstart instead.
* Prefer provider built-in web search when available; use Tavily only when needed.
* Ask rather than guess when a secret, provider choice, or project convention is unclear.

> [!TIP]
>
> **Using an AI coding assistant?**
>
> * Install the [LangChain Docs MCP servers](https://docs.langchain.com/use-these-docs.md) to give your agent access to up-to-date LangChain documentation and examples.
>
>   Connect LangChain docs MCP servers
>
>   Connect both LangChain documentation MCP servers to my coding agent so it can look up current LangChain, LangGraph, and LangSmith docs and API reference.
>
>   Servers to add:
>
>   * `docs-langchain`: [https://docs.langchain.com/mcp](https://docs.langchain.com/mcp)
>   * `reference-langchain`: [https://reference.langchain.com/mcp](https://reference.langchain.com/mcp)
>
>   Detect which agent or editor I am using (Claude Code, Cursor, Codex CLI, Claude Desktop, Deep Agents Code, VS Code, Antigravity, or another MCP-compatible client). Use the matching setup from [https://docs.langchain.com/use-these-docs.md](https://docs.langchain.com/use-these-docs.md):
>
>   * Claude Code: `claude mcp add --transport http` for each server (project scope by default; use `--scope user` only if I ask for global access).
>   * Codex CLI: `codex mcp add` with each server URL.
>   * Cursor, Deep Agents Code, VS Code, or Antigravity: merge both entries into the MCP settings JSON using the field names shown on that page for my client.
>   * Claude Desktop: add both URLs under Settings > Connectors.
>
>   Do not invent alternate MCP URLs. After configuring, confirm both servers are listed and reachable.
> * Install [LangChain Skills](https://github.com/langchain-ai/langchain-skills) to improve your agent's performance on LangChain ecosystem tasks.
>
>   Install LangChain Skills
>
>   Install LangChain Skills for my coding agent so it can perform better on LangChain, LangGraph, and Deep Agents tasks.
>
>   Use the Agent Skills installer from [https://github.com/langchain-ai/langchain-skills](https://github.com/langchain-ai/langchain-skills):
>
>   ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
>   npx skills add langchain-ai/langchain-skills --skill '*' --yes
>   ```
>
>   If I ask for a global install instead, use:
>
>   ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
>   npx skills add langchain-ai/langchain-skills --skill '*' --yes --global
>   ```
>
>   Detect which agent or editor I am using. If I use Claude Code and prefer the plugin path, follow the marketplace install from that repository README (`/plugin marketplace add` then `/plugin install`). Do not invent alternate skill package names or install URLs. After installing, confirm the skills are available to the agent.

## Prerequisites

Before you begin, make sure you have an API key from a model provider (e.g., Gemini, Anthropic, OpenAI).

> [!NOTE]
>
> Deep Agents require a model that supports [tool calling](https://docs.langchain.com/oss/python/langchain/models.md#tool-calling). See [customization](Customize%20Deep%20Agents.md#model) for how to configure your model.

## Step 1: Install dependencies

```bash pip theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
pip install deepagents
```

```bash uv theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
uv init
uv add deepagents
uv sync
```

> [!NOTE]
>
> Google, OpenAI, and Anthropic all provide built-in web search tools: no extra package or API key required. If you use a different provider or prefer [Tavily](https://tavily.com/) for search, install the Tavily package as well:
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> pip install tavily-python
> ```

## Step 2: Set up your API keys

> [tab] Google
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> export GOOGLE_API_KEY="<API_KEY>"
> ```

> [tab] OpenAI
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> export OPENAI_API_KEY="<API_KEY>"
> ```

> [tab] Anthropic
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> export ANTHROPIC_API_KEY="<API_KEY>"
> ```

> [tab] OpenRouter
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> export OPENROUTER_API_KEY="<API_KEY>"
> export TAVILY_API_KEY="<API_KEY>"
> ```

> [tab] Fireworks
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> export FIREWORKS_API_KEY="<API_KEY>"
> export TAVILY_API_KEY="<API_KEY>"
> ```

> [tab] Baseten
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> export BASETEN_API_KEY="<API_KEY>"
> export TAVILY_API_KEY="<API_KEY>"
> ```

> [tab] Ollama
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> # Local: Ollama must be running on your machine
> # Cloud: Set your Ollama API key for hosted inference
> export OLLAMA_API_KEY="<API_KEY>"
> export TAVILY_API_KEY="<API_KEY>"
> ```

> [tab] Other
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> # Set the API key for your provider
> export <PROVIDER>_API_KEY="<API_KEY>"
> export TAVILY_API_KEY="<API_KEY>"
> ```
>
> Deep Agents work with any [LangChain chat model](Models.md#supported-models). Set the API key for your provider.

> [!TIP]
>
> If you are using the LangSmith [LLM Gateway](https://docs.langchain.com/langsmith/llm-gateway.md), traffic to providers is routed through LangSmith. Use the gateway key as the API key instead.

## Step 3: Create a search tool

Google, OpenAI, and Anthropic offer built-in web search tools that run server-side: no extra package or API key needed. Pass a provider tool dict directly to `create_deep_agent`.

> [tab] Provider search (recommended)
>
> ```python Google theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from deepagents import create_deep_agent
>
> # Google's built-in search — no extra install or API key needed
> internet_search = {"google_search": {}}
> ```
>
> ```python OpenAI theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from deepagents import create_deep_agent
>
> # OpenAI's built-in web search — no extra install or API key needed
> internet_search = {"type": "web_search"}
> ```
>
> ```python Anthropic theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from deepagents import create_deep_agent
>
> # Anthropic's built-in web search — no extra install or API key needed
> internet_search = {"type": "web_search_20260209", "name": "web_search"}
> ```

> [tab] Tavily (any provider)
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import os
> from typing import Literal
>
> from tavily import TavilyClient
> from deepagents import create_deep_agent
>
> tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])
>
>
> def internet_search(
>     query: str,
>     max_results: int = 5,
>     topic: Literal["general", "news", "finance"] = "general",
>     include_raw_content: bool = False,
> ):
>     """Run a web search"""
>     return tavily_client.search(
>         query,
>         max_results=max_results,
>         include_raw_content=include_raw_content,
>         topic=topic,
>     )
> ```

## Step 4: Create a deep agent

Pass your search tool and model to `create_deep_agent`. Pass a `model` string in `provider:model` format, or an [initialized model instance](Models.md#configure-model-parameters). See [supported models](Models.md#supported-models) for all providers and [suggested models](Models.md#suggested-models) for tested recommendations.

```python Google theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
# System prompt to steer the agent to be an expert researcher
research_instructions = """You are an expert researcher. Your job is to conduct thorough research and then write a polished report.

You have access to an internet search tool as your primary means of gathering information.

## `internet_search`

Use this to run an internet search for a given query. You can specify the max number of results to return, the topic, and whether raw content should be included.
"""

agent = create_deep_agent(
    model="google_genai:gemini-3.6-flash",
    tools=[internet_search],
    system_prompt=research_instructions,
)
```

```python OpenAI theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
# System prompt to steer the agent to be an expert researcher
research_instructions = """You are an expert researcher. Your job is to conduct thorough research and then write a polished report.

You have access to an internet search tool as your primary means of gathering information.

## `internet_search`

Use this to run an internet search for a given query. You can specify the max number of results to return, the topic, and whether raw content should be included.
"""

agent = create_deep_agent(
    model="openai:gpt-5.5",
    tools=[internet_search],
    system_prompt=research_instructions,
)
```

```python Anthropic theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
# System prompt to steer the agent to be an expert researcher
research_instructions = """You are an expert researcher. Your job is to conduct thorough research and then write a polished report.

You have access to an internet search tool as your primary means of gathering information.

## `internet_search`

Use this to run an internet search for a given query. You can specify the max number of results to return, the topic, and whether raw content should be included.
"""

agent = create_deep_agent(
    model="anthropic:claude-sonnet-5",
    tools=[internet_search],
    system_prompt=research_instructions,
)
```

```python OpenRouter theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
# System prompt to steer the agent to be an expert researcher
research_instructions = """You are an expert researcher. Your job is to conduct thorough research and then write a polished report.

You have access to an internet search tool as your primary means of gathering information.

## `internet_search`

Use this to run an internet search for a given query. You can specify the max number of results to return, the topic, and whether raw content should be included.
"""

agent = create_deep_agent(
    model="openrouter:z-ai/glm-5.2",
    tools=[internet_search],
    system_prompt=research_instructions,
)
```

```python Fireworks theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
# System prompt to steer the agent to be an expert researcher
research_instructions = """You are an expert researcher. Your job is to conduct thorough research and then write a polished report.

You have access to an internet search tool as your primary means of gathering information.

## `internet_search`

Use this to run an internet search for a given query. You can specify the max number of results to return, the topic, and whether raw content should be included.
"""

agent = create_deep_agent(
    model="fireworks:accounts/fireworks/models/glm-5p2",
    tools=[internet_search],
    system_prompt=research_instructions,
)
```

```python Baseten theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
# System prompt to steer the agent to be an expert researcher
research_instructions = """You are an expert researcher. Your job is to conduct thorough research and then write a polished report.

You have access to an internet search tool as your primary means of gathering information.

## `internet_search`

Use this to run an internet search for a given query. You can specify the max number of results to return, the topic, and whether raw content should be included.
"""

agent = create_deep_agent(
    model="baseten:zai-org/GLM-5.2",
    tools=[internet_search],
    system_prompt=research_instructions,
)
```

```python Ollama theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
# System prompt to steer the agent to be an expert researcher
research_instructions = """You are an expert researcher. Your job is to conduct thorough research and then write a polished report.

You have access to an internet search tool as your primary means of gathering information.

## `internet_search`

Use this to run an internet search for a given query. You can specify the max number of results to return, the topic, and whether raw content should be included.
"""

agent = create_deep_agent(
    model="ollama:north-mini-code-1.0",
    tools=[internet_search],
    system_prompt=research_instructions,
)
```

## Step 5: Set up LangSmith tracing

> [!NOTE]
>
> In an [agent-based workspace](https://docs.langchain.com/langsmith/agent-registry.md), [create an agent](https://docs.langchain.com/langsmith/create-an-agent.md) once before sending traces. Use [agent addressing](https://docs.langchain.com/langsmith/log-traces-to-agent.md) to select its identifier and environment. If an integration requires `project_name`, use the selected environment's [`tracer_session_name`](https://docs.langchain.com/langsmith/create-an-agent#use-an-environment-project) as a compatibility value.

[LangSmith](https://smith.langchain.com?utm_source=docs\&utm_medium=cta\&utm_campaign=langsmith-signup\&utm_content=oss-deepagents-quickstart) provides you with visibility into your agent's execution, allowing you to view tool calls, subagent delegation, and LLM responses.

Sign up at [smith.langchain.com](https://smith.langchain.com?utm_source=docs\&utm_medium=cta\&utm_campaign=langsmith-signup\&utm_content=oss-deepagents-quickstart), create an API key, and set these environment variables:

```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
export LANGSMITH_AGENT_ID="<your-agent-id>"
export LANGSMITH_AGENT_ENVIRONMENT="local"
export LANGSMITH_TRACING=true
export LANGSMITH_API_KEY="<API_KEY>"
```

## Step 6: Run the agent

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
result = agent.invoke({"messages": [{"role": "user", "content": "What is langgraph?"}]})

# Print the agent's response
print(result["messages"][-1].content)
```

## How does it work?

Your deep agent automatically:

1. **Conducts research** by calling the `internet_search` tool to gather information.
2. **Manages context** by using file system tools ([`write_file`](../Deep%20Agents%20overview.md#virtual-filesystem-access), [`read_file`](../Deep%20Agents%20overview.md#virtual-filesystem-access)) to offload large search results.
3. **Spawns subagents** as needed to delegate complex subtasks to specialized subagents.
4. **Synthesizes a report** to compile findings into a coherent response.

To add structured task planning with `write_todos`, opt in with [`TodoListMiddleware`](https://reference.langchain.com/python/langchain/agents/middleware/todo/TodoListMiddleware). See [Task planning](../Deep%20Agents%20overview.md#task-planning).

## Examples

For examples of agents and patterns you can build with Deep Agents, see [Examples](https://github.com/langchain-ai/deepagents/tree/main/examples).

## Streaming

Deep Agents have built-in [streaming](https://docs.langchain.com/oss/python/langchain/event-streaming.md) for real-time updates from agent execution using LangGraph.
This allows you to observe output progressively and review and debug agent and subagent work, such as tool calls, tool results, and LLM responses.

## Next steps

Now that you've built your first deep agent:

* **Customize your agent**: Learn about [customization options](Customize%20Deep%20Agents.md), including custom system prompts, tools, and subagents.
* **Add long-term memory**: Enable [persistent memory](../Context%20management/Memory.md) across conversations.
* **Deploy to production**: Use [Managed Deep Agents](../Deployment/Managed%20Deep%20Agents.md) to create, run, and operate deep agents in LangSmith.
* **Test and evaluate**: Use [LangSmith evaluation](https://docs.langchain.com/langsmith/evaluation-quickstart.md) to run automated tests and measure your agent's performance against a dataset.

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/deepagents/quickstart.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

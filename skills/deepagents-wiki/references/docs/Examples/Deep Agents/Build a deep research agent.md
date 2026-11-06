# Build a deep research agent

> Build a multi-step web research agent with subagent delegation using Managed Deep Agents or the Deep Agents SDK

## Overview

This guide shows how to build a multi-step web research agent with [Deep Agents](https://docs.langchain.com/oss/python/deepagents.md). The agent decomposes research questions into focused tasks, delegates them to specialized sub-agents, and synthesizes findings into a comprehensive report.

The agent you build will:

1. Plan research using the opt-in todo list middleware
2. Delegate focused research tasks to sub-agents with isolated context
3. Assess search results and plan next steps as you gather information
4. Synthesize findings with proper citations into a final report

The spawned sub-agents conduct web searches with Tavily, fetching full webpage content for analysis.

### Key concepts

This tutorial covers:

* [Subagents](../../Delegation/Subagents.md) for parallel, context-isolated research
* Custom [tools](https://docs.langchain.com/oss/python/langchain/tools.md) for web search
* Multi-step planning with the opt-in [planning tool](../../Deep%20Agents%20overview.md#task-planning)

## Prerequisites

API keys for:

* Anthropic (Claude) or Google (Gemini)
* [Tavily](https://www.tavily.com/) for web search (optional; free tier is sufficient)
* [LangSmith](https://smith.langchain.com?utm_source=docs\&utm_medium=cta\&utm_campaign=langsmith-signup\&utm_content=oss-deepagents-deep-research) for tracing (optional if you are using the SDK; required for Managed Deep Agents)

## Choose your path

This guide shows how to build this agenet with [Managed Deep Agents](../../Deployment/Managed%20Deep%20Agents.md) and the Deep Agnets SDK. Managed Deep Agents laets you deploy agents without having to manage infrastructure. The Deep Agents SDK, lets you have maximum flexibility while using the same Deep Agents harness and you can host agents yourself, or run a custom [LangSmith Deployment](https://docs.langchain.com/langsmith/deployment.md).

> [tab] Managed Deep Agents
>
> > [!NOTE]
> >
> > Managed Deep Agents is in **public [beta](https://docs.langchain.com/langsmith/release-stages.md)** on [LangSmith Cloud](https://docs.langchain.com/langsmith/cloud.md) and [Bring Your Own Cloud (BYOC)](https://docs.langchain.com/langsmith/byoc.md). Use Managed Deep Agents CLI and SDK v0.10 or later for BYOC.
>
> ### Setup
>
> To follow along, you need:
>
> * Python and `uv`.
>
> * An API key for your model provider of choice.
>
> **1. Create the project**
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> uvx --from managed-deepagents mda init deep-research
> cd deep-research
> ```
>
> **2. Add API keys**
>
> Add your model provider key, Tavily key, and LangSmith API key to `.env`:
>
> > [tab] Claude
> >
> > ```text .env theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > ANTHROPIC_API_KEY=<ANTHROPIC_API_KEY>
> > TAVILY_API_KEY=<TAVILY_API_KEY>
> > LANGSMITH_API_KEY=<LANGSMITH_API_KEY>
> > ```
>
> > [tab] Gemini
> >
> > ```text .env theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > GOOGLE_API_KEY=<GOOGLE_API_KEY>
> > TAVILY_API_KEY=<TAVILY_API_KEY>
> > LANGSMITH_API_KEY=<LANGSMITH_API_KEY>
> > ```
>
> > [!WARNING]
> >
> > Do not commit the `.env` file into version control. It contains secrets.
>
> **3. Install search dependencies**
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> uv add tavily-python httpx markdownify
> ```
>
> ### Build the agent
>
> **1. Add tools**
>
> Create a custom search tool. The `tavily_search` tool uses Tavily for URL discovery, then fetches full webpage content so the agent can analyze complete sources instead of summaries.
>
> Create `tools/search.py`:
>
> ```python tools/search.py theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import os
> from typing import Annotated, Literal
>
> import httpx
> from langchain.tools import InjectedToolArg, tool
> from markdownify import markdownify
> from tavily import TavilyClient
>
> tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])
>
>
> def fetch_webpage_content(url: str, timeout: float = 10.0) -> str:
>     """Fetch webpage and convert HTML to markdown."""
>     headers = {
>         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
>     }
>     try:
>         response = httpx.get(url, headers=headers, timeout=timeout)
>         response.raise_for_status()
>         return markdownify(response.text)
>     except Exception as e:
>         return f"Error fetching {url}: {e!s}"
>
>
> @tool(parse_docstring=True)
> def tavily_search(
>     query: str,
>     max_results: Annotated[int, InjectedToolArg] = 1,
>     topic: Annotated[
>         Literal["general", "news", "finance"], InjectedToolArg
>     ] = "general",
> ) -> str:
>     """Search the web for information on a given query.
>
>     Uses Tavily to discover relevant URLs, then fetches and returns full webpage content as markdown.
>
>     Args:
>         query: Search query to execute
>         max_results: Maximum number of results to return (default: 1)
>         topic: Topic filter - 'general', 'news', or 'finance' (default: 'general')
>
>     Returns:
>         Formatted search results with full webpage content
>     """
>     search_results = tavily_client.search(
>         query,
>         max_results=max_results,
>         topic=topic,
>     )
>     result_texts = []
>     for result in search_results.get("results", []):
>         url = result["url"]
>         title = result["title"]
>         content = fetch_webpage_content(url)
>         result_texts.append(f"## {title}\n**URL:** {url}\n\n{content}\n---")
>
>     return f"Found {len(result_texts)} result(s) for '{query}':\n\n" + "\n".join(
>         result_texts
>     )
> ```
>
> **2. Add orchestrator instructions**
>
> Put the research workflow and sub-agent coordination guidance in `instructions.md`. Managed Deep Agents loads this file as the orchestrator system prompt:
>
> ```markdown instructions.md expandable wrap theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> # Research Workflow
>
> Follow this workflow for all research requests:
>
> 1. **Plan**: Create a todo list with write_todos to break down the research into focused tasks
> 2. **Save the request**: Use write_file() to save the user's research question to `/research_request.md`
> 3. **Research**: Delegate research tasks to sub-agents using the task() tool - ALWAYS use sub-agents for research, never conduct research yourself
> 4. **Synthesize**: Review all sub-agent findings and consolidate citations (each unique URL gets one number across all findings)
> 5. **Write Report**: Write a comprehensive final report to `/final_report.md` (see Report Writing Guidelines below)
> 6. **Verify**: Read `/research_request.md` and confirm you've addressed all aspects with proper citations and structure
>
> ## Research Planning Guidelines
> - Batch similar research tasks into a single TODO to minimize overhead
> - For simple fact-finding questions, use 1 sub-agent
> - For comparisons or multi-faceted topics, delegate to multiple parallel sub-agents
> - Each sub-agent should research one specific aspect and return findings
>
> ## Report Writing Guidelines
>
> When writing the final report to `/final_report.md`, follow these structure patterns:
>
> **For comparisons:**
> 1. Introduction
> 2. Overview of topic A
> 3. Overview of topic B
> 4. Detailed comparison
> 5. Conclusion
>
> **For lists/rankings:**
> Simply list items with details - no introduction needed:
> 1. Item 1 with explanation
> 2. Item 2 with explanation
> 3. Item 3 with explanation
>
> **For summaries/overviews:**
> 1. Overview of topic
> 2. Key concept 1
> 3. Key concept 2
> 4. Key concept 3
> 5. Conclusion
>
> **General guidelines:**
> - Use clear section headings (## for sections, ### for subsections)
> - Write in paragraph form by default - be text-heavy, not just bullet points
> - Do NOT use self-referential language ("I found...", "I researched...")
> - Write as a professional report without meta-commentary
> - Each section should be comprehensive and detailed
> - Use bullet points only when listing is more appropriate than prose
>
> **Citation format:**
> - Cite sources inline using [1], [2], [3] format
> - Assign each unique URL a single citation number across ALL sub-agent findings
> - End report with ### Sources section listing each numbered source
> - Number sources sequentially without gaps (1,2,3,4...)
> - Format: [1] Source Title: URL (each on separate line for proper list rendering)
> - Example:
>
>  Some important finding [1]. Another key insight [2].
>
>  ### Sources
>  [1] AI Research Paper: https://example.com/paper
>  [2] Industry Analysis: https://example.com/analysis
>
> # Sub-Agent Research Coordination
>
> Your role is to coordinate research by delegating tasks from your TODO list to specialized research sub-agents.
>
> ## Delegation Strategy
>
> **DEFAULT: Start with 1 sub-agent** for most queries:
> - "What is quantum computing?" -> 1 sub-agent (general overview)
> - "List the top 10 coffee shops in San Francisco" -> 1 sub-agent
> - "Summarize the history of the internet" -> 1 sub-agent
> - "Research context engineering for AI agents" -> 1 sub-agent (covers all aspects)
>
> **ONLY parallelize when the query EXPLICITLY requires comparison or has clearly independent aspects:**
>
> **Explicit comparisons** -> 1 sub-agent per element:
> - "Compare OpenAI vs Anthropic vs DeepMind AI safety approaches" -> 3 parallel sub-agents
> - "Compare Python vs JavaScript for web development" -> 2 parallel sub-agents
>
> **Clearly separated aspects** -> 1 sub-agent per aspect (use sparingly):
> - "Research renewable energy adoption in Europe, Asia, and North America" -> 3 parallel sub-agents (geographic separation)
> - Only use this pattern when aspects cannot be covered efficiently by a single comprehensive search
>
> ## Key Principles
> - **Bias towards single sub-agent**: One comprehensive research task is more token-efficient than multiple narrow ones
> - **Avoid premature decomposition**: Don't break "research X" into "research X overview", "research X techniques", "research X applications" - just use 1 sub-agent for all of X
> - **Parallelize only for clear comparisons**: Use multiple sub-agents when comparing distinct entities or geographically separated data
>
> ## Parallel Execution Limits
> - Use at most 3 parallel sub-agents per iteration
> - Make multiple task() calls in a single response to enable parallel execution
> - Each sub-agent returns findings independently
>
> ## Research Limits
> - Stop after 3 delegation rounds if you haven't found adequate sources
> - Stop when you have sufficient information to answer comprehensively
> - Bias towards focused research over exhaustive exploration
> ```
>
> When you deploy, Managed Deep Agents syncs these instructions to [Context Hub](https://docs.langchain.com/langsmith/python/managed-deep-agents-context-hub.md).
>
> **3. Create the agent**
>
> You just put the main agent's instructions in `instructions.md`. Replace the scaffolded agent entry with the full file below. It sets the model, tools, the research sub-agent (including that sub-agent's own prompt), and [`TodoListMiddleware`](https://reference.langchain.com/python/langchain/agents/middleware/todo/TodoListMiddleware) so the agent can call `write_todos` for [task planning](../../Deep%20Agents%20overview.md#task-planning). `name` is required: MDA uses it as the LangGraph assistant ID and the default deployment name.
>
> Replace `agent.py`. Choose your provider:
>
> > [tab] Claude
> >
> > ```python agent.py theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > from datetime import datetime
> >
> > from langchain.agents.middleware import TodoListMiddleware
> > from managed_deepagents import define_deep_agent
> >
> > from tools.search import tavily_search
> >
> > current_date = datetime.now().strftime("%Y-%m-%d")
> >
> > RESEARCHER_INSTRUCTIONS = """You are a research assistant conducting research on the user's input topic. For context, today's date is {date}.
> >
> > Your job is to use tools to gather information about the user's input topic.
> > You can use the tavily_search tool to find resources that can help answer the research question.
> > You can call it in series or in parallel, your research is conducted in a tool-calling loop.
> >
> > You have access to the tavily_search tool for conducting web searches.
> >
> > Think like a human researcher with limited time. Follow these steps:
> >
> > 1. **Read the question carefully** - What specific information does the user need?
> > 2. **Start with broader searches** - Use broad, comprehensive queries first
> > 3. **After each search, pause and assess** - Do I have enough to answer? What's still missing?
> > 4. **Execute narrower searches as you gather information** - Fill in the gaps
> > 5. **Stop when you can answer confidently** - Don't keep searching for perfection
> >
> > **Tool Call Budgets** (Prevent excessive searching):
> > - **Simple queries**: Use 2-3 search tool calls maximum
> > - **Complex queries**: Use up to 5 search tool calls maximum
> > - **Always stop**: After 5 search tool calls if you cannot find the right sources
> >
> > **Stop Immediately When**:
> > - You can answer the user's question comprehensively
> > - You have 3+ relevant examples/sources for the question
> > - Your last 2 searches returned similar information
> >
> > After each search, assess results before continuing: What key information did I find? What's missing? Do I have enough to answer? Should I search more or provide my answer?
> >
> > When providing your findings back to the orchestrator:
> >
> > 1. **Structure your response**: Organize findings with clear headings and detailed explanations
> > 2. **Cite sources inline**: Use [1], [2], [3] format when referencing information from your searches
> > 3. **Include Sources section**: End with ### Sources listing each numbered source with title and URL
> >
> > The orchestrator will consolidate citations from all sub-agents into the final report.
> > """
> >
> > research_sub_agent = {
> >     "name": "research-agent",
> >     "description": "Delegate research to the sub-agent. Give one topic at a time.",
> >     "system_prompt": RESEARCHER_INSTRUCTIONS.format(date=current_date),
> >     "tools": [tavily_search],
> > }
> >
> > agent = define_deep_agent(
> >     name="deep-research",
> >     model="anthropic:claude-sonnet-4-5-20250929",
> >     tools=[tavily_search],
> >     subagents=[research_sub_agent],
> >     middleware=[TodoListMiddleware()],
> > )
> > ```
>
> > [tab] Gemini
> >
> > ```python agent.py theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > from datetime import datetime
> >
> > from langchain.agents.middleware import TodoListMiddleware
> > from managed_deepagents import define_deep_agent
> >
> > from tools.search import tavily_search
> >
> > current_date = datetime.now().strftime("%Y-%m-%d")
> >
> > RESEARCHER_INSTRUCTIONS = """You are a research assistant conducting research on the user's input topic. For context, today's date is {date}.
> >
> > Your job is to use tools to gather information about the user's input topic.
> > You can use the tavily_search tool to find resources that can help answer the research question.
> > You can call it in series or in parallel, your research is conducted in a tool-calling loop.
> >
> > You have access to the tavily_search tool for conducting web searches.
> >
> > Think like a human researcher with limited time. Follow these steps:
> >
> > 1. **Read the question carefully** - What specific information does the user need?
> > 2. **Start with broader searches** - Use broad, comprehensive queries first
> > 3. **After each search, pause and assess** - Do I have enough to answer? What's still missing?
> > 4. **Execute narrower searches as you gather information** - Fill in the gaps
> > 5. **Stop when you can answer confidently** - Don't keep searching for perfection
> >
> > **Tool Call Budgets** (Prevent excessive searching):
> > - **Simple queries**: Use 2-3 search tool calls maximum
> > - **Complex queries**: Use up to 5 search tool calls maximum
> > - **Always stop**: After 5 search tool calls if you cannot find the right sources
> >
> > **Stop Immediately When**:
> > - You can answer the user's question comprehensively
> > - You have 3+ relevant examples/sources for the question
> > - Your last 2 searches returned similar information
> >
> > After each search, assess results before continuing: What key information did I find? What's missing? Do I have enough to answer? Should I search more or provide my answer?
> >
> > When providing your findings back to the orchestrator:
> >
> > 1. **Structure your response**: Organize findings with clear headings and detailed explanations
> > 2. **Cite sources inline**: Use [1], [2], [3] format when referencing information from your searches
> > 3. **Include Sources section**: End with ### Sources listing each numbered source with title and URL
> >
> > The orchestrator will consolidate citations from all sub-agents into the final report.
> > """
> >
> > research_sub_agent = {
> >     "name": "research-agent",
> >     "description": "Delegate research to the sub-agent. Give one topic at a time.",
> >     "system_prompt": RESEARCHER_INSTRUCTIONS.format(date=current_date),
> >     "tools": [tavily_search],
> > }
> >
> > agent = define_deep_agent(
> >     name="deep-research",
> >     model="google_genai:gemini-3-pro-preview",
> >     tools=[tavily_search],
> >     subagents=[research_sub_agent],
> >     middleware=[TodoListMiddleware()],
> > )
> > ```
>
> ### Run the agent
>
> **1. Run locally**
>
> Install dependencies and start the agent:
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> uv sync
> uv run mda dev
> ```
>
> `mda dev` loads API keys from `.env`, starts a local Agent Server, and opens the agent in LangSmith Studio.
>
> In Studio, send a research question such as:
>
> ```txt wrap theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> Compare the main approaches to context engineering for AI agents in 2025.
> ```
>
> You should see the orchestrator plan with `write_todos`, delegate to the research sub-agent, and write a report. For more information, see [Develop locally with LangSmith Studio](https://docs.langchain.com/langsmith/python/managed-deep-agents-local-development.md).
>
> **2. Deploy (optional)**
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> uv run mda deploy
> ```
>
> On success, the CLI prints the deployment dashboard URL. See [Deploy](https://docs.langchain.com/langsmith/python/managed-deep-agents-deploy.md).

> [tab] Deep Agents SDK
>
> ### Setup
>
> **1. Create project directory**
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> mkdir deep-research-agent
> cd deep-research-agent
> ```
>
> **2. Install dependencies**
>
> > [tab] Claude
> >
> > ```bash pip wrap theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > pip install deepagents tavily-python httpx markdownify langchain-anthropic langchain-core
> > ```
> >
> > ```bash uv wrap theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > uv init
> > uv add deepagents tavily-python httpx markdownify langchain-anthropic langchain-core
> > uv sync
> > ```
>
> > [tab] Gemini
> >
> > ```bash pip wrap theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > pip install deepagents tavily-python httpx markdownify langchain-google-genai langchain-core
> > ```
> >
> > ```bash uv wrap theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > uv init
> > uv add deepagents tavily-python httpx markdownify langchain-google-genai langchain-core
> > uv sync
> > ```
>
> **3. Set API keys**
>
> > [tab] Claude
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > export ANTHROPIC_API_KEY="<API_KEY>"
> > export TAVILY_API_KEY="<API_KEY>"
> > export LANGSMITH_API_KEY="<API_KEY>"   # Optional
> > ```
>
> > [tab] Gemini
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > export GOOGLE_API_KEY="<API_KEY>"
> > export TAVILY_API_KEY="<API_KEY>"
> > export LANGSMITH_API_KEY="<API_KEY>"   # Optional
> > ```
>
> ### Build the agent
>
> Create `agent.py` in your project directory:
>
> **1. Add tools**
>
> Add the custom search tool. The `tavily_search` tool uses Tavily for URL discovery, then fetches full webpage content so the agent can analyze complete sources instead of summaries.
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import os
> from typing import Annotated, Literal
>
> import httpx
> from langchain.tools import InjectedToolArg, tool
> from markdownify import markdownify
> from tavily import TavilyClient
>
> tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])
>
>
> def fetch_webpage_content(url: str, timeout: float = 10.0) -> str:
>     """Fetch webpage and convert HTML to markdown."""
>     headers = {
>         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
>     }
>     try:
>         response = httpx.get(url, headers=headers, timeout=timeout)
>         response.raise_for_status()
>         return markdownify(response.text)
>     except Exception as e:
>         return f"Error fetching {url}: {e!s}"
>
>
> @tool(parse_docstring=True)
> def tavily_search(
>     query: str,
>     max_results: Annotated[int, InjectedToolArg] = 1,
>     topic: Annotated[
>         Literal["general", "news", "finance"], InjectedToolArg
>     ] = "general",
> ) -> str:
>     """Search the web for information on a given query.
>
>     Uses Tavily to discover relevant URLs, then fetches and returns full webpage content as markdown.
>
>     Args:
>         query: Search query to execute
>         max_results: Maximum number of results to return (default: 1)
>         topic: Topic filter - 'general', 'news', or 'finance' (default: 'general')
>
>     Returns:
>         Formatted search results with full webpage content
>     """
>     search_results = tavily_client.search(
>         query,
>         max_results=max_results,
>         topic=topic,
>     )
>     result_texts = []
>     for result in search_results.get("results", []):
>         url = result["url"]
>         title = result["title"]
>         content = fetch_webpage_content(url)
>         result_texts.append(f"## {title}\n**URL:** {url}\n\n{content}\n---")
>
>     return f"Found {len(result_texts)} result(s) for '{query}':\n\n" + "\n".join(
>         result_texts
>     )
> ```
>
> **2. Create the agent**
>
> Below the tools, add the prompt constants and then create the agent. The three constants (`RESEARCH_WORKFLOW_INSTRUCTIONS`, `RESEARCHER_INSTRUCTIONS`, and `SUBAGENT_DELEGATION_INSTRUCTIONS`) must live in the same file as the `create_deep_agent` / `createDeepAgent` call. [`TodoListMiddleware`](https://reference.langchain.com/python/langchain/agents/middleware/todo/TodoListMiddleware) is opt-in [task planning](../../Deep%20Agents%20overview.md#task-planning) so the agent can call `write_todos`.
>
> Add the prompts to `agent.py`:
>
> ```python expandable wrap theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> RESEARCH_WORKFLOW_INSTRUCTIONS = """# Research Workflow
>
> Follow this workflow for all research requests:
>
> 1. **Plan**: Create a todo list with write_todos to break down the research into focused tasks
> 2. **Save the request**: Use write_file() to save the user's research question to `/research_request.md`
> 3. **Research**: Delegate research tasks to sub-agents using the task() tool - ALWAYS use sub-agents for research, never conduct research yourself
> 4. **Synthesize**: Review all sub-agent findings and consolidate citations (each unique URL gets one number across all findings)
> 5. **Write Report**: Write a comprehensive final report to `/final_report.md` (see Report Writing Guidelines below)
> 6. **Verify**: Read `/research_request.md` and confirm you've addressed all aspects with proper citations and structure
>
> ## Research Planning Guidelines
> - Batch similar research tasks into a single TODO to minimize overhead
> - For simple fact-finding questions, use 1 sub-agent
> - For comparisons or multi-faceted topics, delegate to multiple parallel sub-agents
> - Each sub-agent should research one specific aspect and return findings
>
> ## Report Writing Guidelines
>
> When writing the final report to `/final_report.md`, follow these structure patterns:
>
> **For comparisons:**
> 1. Introduction
> 2. Overview of topic A
> 3. Overview of topic B
> 4. Detailed comparison
> 5. Conclusion
>
> **For lists/rankings:**
> Simply list items with details - no introduction needed:
> 1. Item 1 with explanation
> 2. Item 2 with explanation
> 3. Item 3 with explanation
>
> **For summaries/overviews:**
> 1. Overview of topic
> 2. Key concept 1
> 3. Key concept 2
> 4. Key concept 3
> 5. Conclusion
>
> **General guidelines:**
> - Use clear section headings (## for sections, ### for subsections)
> - Write in paragraph form by default - be text-heavy, not just bullet points
> - Do NOT use self-referential language ("I found...", "I researched...")
> - Write as a professional report without meta-commentary
> - Each section should be comprehensive and detailed
> - Use bullet points only when listing is more appropriate than prose
>
> **Citation format:**
> - Cite sources inline using [1], [2], [3] format
> - Assign each unique URL a single citation number across ALL sub-agent findings
> - End report with ### Sources section listing each numbered source
> - Number sources sequentially without gaps (1,2,3,4...)
> - Format: [1] Source Title: URL (each on separate line for proper list rendering)
> - Example:
>
>  Some important finding [1]. Another key insight [2].
>
>  ### Sources
>  [1] AI Research Paper: https://example.com/paper
>  [2] Industry Analysis: https://example.com/analysis
> """
> ```
>
> ```python expandable wrap theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> RESEARCHER_INSTRUCTIONS = """You are a research assistant conducting research on the user's input topic. For context, today's date is {date}.
>
> Your job is to use tools to gather information about the user's input topic.
> You can use the tavily_search tool to find resources that can help answer the research question.
> You can call it in series or in parallel, your research is conducted in a tool-calling loop.
>
> You have access to the tavily_search tool for conducting web searches.
>
> Think like a human researcher with limited time. Follow these steps:
>
> 1. **Read the question carefully** - What specific information does the user need?
> 2. **Start with broader searches** - Use broad, comprehensive queries first
> 3. **After each search, pause and assess** - Do I have enough to answer? What's still missing?
> 4. **Execute narrower searches as you gather information** - Fill in the gaps
> 5. **Stop when you can answer confidently** - Don't keep searching for perfection
>
> **Tool Call Budgets** (Prevent excessive searching):
> - **Simple queries**: Use 2-3 search tool calls maximum
> - **Complex queries**: Use up to 5 search tool calls maximum
> - **Always stop**: After 5 search tool calls if you cannot find the right sources
>
> **Stop Immediately When**:
> - You can answer the user's question comprehensively
> - You have 3+ relevant examples/sources for the question
> - Your last 2 searches returned similar information
>
> After each search, assess results before continuing: What key information did I find? What's missing? Do I have enough to answer? Should I search more or provide my answer?
>
> When providing your findings back to the orchestrator:
>
> 1. **Structure your response**: Organize findings with clear headings and detailed explanations
> 2. **Cite sources inline**: Use [1], [2], [3] format when referencing information from your searches
> 3. **Include Sources section**: End with ### Sources listing each numbered source with title and URL
>
> Example:
> ## Key Findings
> Context engineering is a critical technique for AI agents [1]. Studies show that proper context management can improve performance by 40% [2].
>
> ### Sources
> [1] Context Engineering Guide: https://example.com/context-guide
> [2] AI Performance Study: https://example.com/study
>
> The orchestrator will consolidate citations from all sub-agents into the final report.
> """
> ```
>
> ```python expandable wrap theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> SUBAGENT_DELEGATION_INSTRUCTIONS = """# Sub-Agent Research Coordination
>
> Your role is to coordinate research by delegating tasks from your TODO list to specialized research sub-agents.
>
> ## Delegation Strategy
>
> **DEFAULT: Start with 1 sub-agent** for most queries:
> - "What is quantum computing?" -> 1 sub-agent (general overview)
> - "List the top 10 coffee shops in San Francisco" -> 1 sub-agent
> - "Summarize the history of the internet" -> 1 sub-agent
> - "Research context engineering for AI agents" -> 1 sub-agent (covers all aspects)
>
> **ONLY parallelize when the query EXPLICITLY requires comparison or has clearly independent aspects:**
>
> **Explicit comparisons** -> 1 sub-agent per element:
> - "Compare OpenAI vs Anthropic vs DeepMind AI safety approaches" -> 3 parallel sub-agents
> - "Compare Python vs JavaScript for web development" -> 2 parallel sub-agents
>
> **Clearly separated aspects** -> 1 sub-agent per aspect (use sparingly):
> - "Research renewable energy adoption in Europe, Asia, and North America" -> 3 parallel sub-agents (geographic separation)
> - Only use this pattern when aspects cannot be covered efficiently by a single comprehensive search
>
> ## Key Principles
> - **Bias towards single sub-agent**: One comprehensive research task is more token-efficient than multiple narrow ones
> - **Avoid premature decomposition**: Don't break "research X" into "research X overview", "research X techniques", "research X applications" - just use 1 sub-agent for all of X
> - **Parallelize only for clear comparisons**: Use multiple sub-agents when comparing distinct entities or geographically separated data
>
> ## Parallel Execution Limits
> - Use at most {max_concurrent_research_units} parallel sub-agents per iteration
> - Make multiple task() calls in a single response to enable parallel execution
> - Each sub-agent returns findings independently
>
> ## Research Limits
> - Stop after {max_researcher_iterations} delegation rounds if you haven't found adequate sources
> - Stop when you have sufficient information to answer comprehensively
> - Bias towards focused research over exhaustive exploration"""
> ```
>
> Then add the model and agent. Choose your provider:
>
> > [tab] Claude
> >
> > ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > from datetime import datetime
> >
> > from deepagents import create_deep_agent
> > from langchain.agents.middleware import TodoListMiddleware
> > from langchain.chat_models import init_chat_model
> >
> > max_concurrent_research_units = 3
> > max_researcher_iterations = 3
> >
> > current_date = datetime.now().strftime("%Y-%m-%d")
> >
> > INSTRUCTIONS = (
> >     RESEARCH_WORKFLOW_INSTRUCTIONS
> >     + "\n\n"
> >     + "=" * 80
> >     + "\n\n"
> >     + SUBAGENT_DELEGATION_INSTRUCTIONS.format(
> >         max_concurrent_research_units=max_concurrent_research_units,
> >         max_researcher_iterations=max_researcher_iterations,
> >     )
> > )
> >
> > research_sub_agent = {
> >     "name": "research-agent",
> >     "description": "Delegate research to the sub-agent. Give one topic at a time.",
> >     "system_prompt": RESEARCHER_INSTRUCTIONS.format(date=current_date),
> >     "tools": [tavily_search],
> > }
> >
> > model = init_chat_model(model="anthropic:claude-sonnet-4-5-20250929", temperature=0.0)
> >
> > agent = create_deep_agent(
> >     model=model,
> >     tools=[tavily_search],
> >     system_prompt=INSTRUCTIONS,
> >     subagents=[research_sub_agent],
> >     middleware=[TodoListMiddleware()],
> > )
> > ```
>
> > [tab] Gemini
> >
> > ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > from datetime import datetime
> >
> > from deepagents import create_deep_agent
> > from langchain.agents.middleware import TodoListMiddleware
> > from langchain_google_genai import ChatGoogleGenerativeAI
> >
> > max_concurrent_research_units = 3
> > max_researcher_iterations = 3
> >
> > current_date = datetime.now().strftime("%Y-%m-%d")
> >
> > INSTRUCTIONS = (
> >     RESEARCH_WORKFLOW_INSTRUCTIONS
> >     + "\n\n"
> >     + "=" * 80
> >     + "\n\n"
> >     + SUBAGENT_DELEGATION_INSTRUCTIONS.format(
> >         max_concurrent_research_units=max_concurrent_research_units,
> >         max_researcher_iterations=max_researcher_iterations,
> >     )
> > )
> >
> > research_sub_agent = {
> >     "name": "research-agent",
> >     "description": "Delegate research to the sub-agent. Give one topic at a time.",
> >     "system_prompt": RESEARCHER_INSTRUCTIONS.format(date=current_date),
> >     "tools": [tavily_search],
> > }
> >
> > model = ChatGoogleGenerativeAI(model="gemini-3-pro-preview", temperature=0.0)
> >
> > agent = create_deep_agent(
> >     model=model,
> >     tools=[tavily_search],
> >     system_prompt=INSTRUCTIONS,
> >     subagents=[research_sub_agent],
> >     middleware=[TodoListMiddleware()],
> > )
> > ```
>
> ### Run the agent
>
> You can run the agent synchronously, meaning it will wait for the full result and then print it, or you can stream updates as they come in.
>
> Add the code from the respective tab at the bottom of `agent.py`:
>
> > [tab] Run synchronously
> >
> > ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > from langchain.messages import HumanMessage
> >
> > if __name__ == "__main__":
> >     result = agent.invoke(
> >         {
> >             "messages": [
> >                 HumanMessage(
> >                     content="What are the main differences between RAG and fine-tuning for LLM applications?"
> >                 )
> >             ]
> >         }
> >     )
> >
> >     for msg in result.get("messages", []):
> >         if hasattr(msg, "content") and msg.content:
> >             print(msg.content)
> > ```
>
> > [tab] Stream updates
> >
> > ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > from langchain.messages import HumanMessage
> >
> > if __name__ == "__main__":
> >     stream = agent.stream_events(
> >         {
> >             "messages": [
> >                 HumanMessage(content="Compare Python vs JavaScript for web development")
> >             ]
> >         },
> >         version="v3",
> >     )
> >     for message in stream.messages:
> >         for token in message.text:
> >             print(token, end="", flush=True)
> > ```
>
> Run the agent from the project root:
>
> ```sh theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> python agent.py
> ```
>
> If you set the `LANGSMITH_API_KEY` environment variable before running, you can view the agent's traces in [LangSmith](https://docs.langchain.com/langsmith/observability.md) to debug and monitor multi-step behavior.
>
> ### Full code
>
> View the complete [Deep Research example](https://github.com/langchain-ai/deepagents/tree/main/examples/deep_research) on GitHub.

## Next steps

Now that you've built the agent, customize the workflow by editing the orchestrator instructions (Managed Deep Agents: `instructions.md`; SDK: prompt constants in your agent file). You can also tune the delegation limits to allow more parallel sub-agents or delegation rounds.

For more information on the concepts in this tutorial, see:

* [Subagents](../../Delegation/Subagents.md): Configure subagents with different tools and prompts
* [Customization](../../Get%20started/Customize%20Deep%20Agents.md): Customize models, tools, system prompts, and optional [task planning](../../Deep%20Agents%20overview.md#task-planning)
* [Managed Deep Agents](../../Deployment/Managed%20Deep%20Agents.md): Build deep agents with managed deployment infrastructure
* [LangSmith](https://docs.langchain.com/langsmith/observability.md): Trace research runs and debug multi-step behavior
* [Deep Research Course](https://academy.langchain.com/courses/deep-research-with-langgraph): Full course on deep research with LangGraph

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/deepagents/deep-research.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

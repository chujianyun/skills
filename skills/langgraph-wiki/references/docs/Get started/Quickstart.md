# Quickstart

This quickstart demonstrates how to build a calculator agent using the LangGraph Graph API or the Functional API.

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
See [chat model integrations](https://docs.langchain.com/oss/python/integrations/chat.md) for all available providers.

If you use [LangSmith Gateway](https://docs.langchain.com/langsmith/llm-gateway.md), you can [bring your own provider keys](https://docs.langchain.com/langsmith/llm-gateway-quickstart.md) or use [Gateway Credits](https://docs.langchain.com/langsmith/llm-gateway-credits.md) to access models without a provider key.

## Setup

Install `langgraph`, `langchain`, and `langchain-anthropic`:

```bash pip
pip install -U langgraph langchain langchain-anthropic
```

```bash uv
uv add langgraph langchain langchain-anthropic
```

This example uses Anthropic. Set your API key in the shell or a `.env` file:

```bash Shell
export ANTHROPIC_API_KEY="<API_KEY>"
```

```bash .env
ANTHROPIC_API_KEY=your-api-key
```

To use another provider, see [chat model integrations](https://docs.langchain.com/oss/python/integrations/chat.md) and adapt the model initialization in the next steps.

## 1. Choose the API

Both paths build the same calculator agent: the model can call tools, then the agent calls the model again until it returns a final answer.

* [Use the Graph API](#use-the-graph-api) if you prefer to define your agent as a graph of nodes and edges.
* [Use the Functional API](#use-the-functional-api) if you prefer to define your agent as a single function.

Pick a tab. Create one file. Add the code from each step below the previous step.

Not sure which to pick? See [Choosing between Graph and Functional APIs](Choosing%20between%20Graph%20and%20Functional%20APIs.md). For conceptual information, see [Graph API overview](../Build%20with%20the%20Graph%20API/Graph%20API%20overview.md) and [Functional API overview](../Advanced/Build%20with%20the%20Functional%20API/Functional%20API%20overview.md).

> [tab] Use the Graph API
>
> Build the LangGraph Graph API calculator quickstart
>
> Build a LangGraph calculator agent with the Graph API in this working directory by following the LangGraph quickstart.
>
> ## Step 1: Read the guide
>
> Detect whether this project uses Python or TypeScript/JavaScript. Fetch and follow the matching page; treat it as the source of truth for package names, model strings, and code:
>
> * Python: [https://docs.langchain.com/oss/python/langgraph/quickstart.md](Quickstart.md)
> * TypeScript: [https://docs.langchain.com/oss/javascript/langgraph/quickstart.md](https://docs.langchain.com/oss/javascript/langgraph/quickstart.md)
>
> Use only the **Use the Graph API** tab. Do not implement the Functional API path.
>
> ## Step 2: Install dependencies
>
> Install the packages required by the Graph API path with the package manager already used in this project.
>
> ## Step 3: Configure model credentials
>
> This quickstart uses Anthropic by default. Check whether `ANTHROPIC_API_KEY` is set. If it is not, ask the user to create a key and set it in the shell or a `.env` file, then stop and wait for confirmation. Do not invent, hardcode, or commit API keys. If the user prefers another chat model provider from the integrations docs, adapt the example accordingly after confirming.
>
> ## Step 4: Implement the calculator agent
>
> Define tools and model, then Graph API state, nodes, edges, and the compiled graph from the guide.
>
> ## Step 5: Optional LangSmith tracing
>
> Ask the user if they want tracing. If yes, ask them to set `LANGSMITH_TRACING=true` and `LANGSMITH_API_KEY` themselves. Do not invent a LangSmith key.
>
> ## Step 6: Run the agent
>
> Invoke the agent on a sample arithmetic query from the guide and print the final result.
>
> ## Rules
>
> * Stay scoped to this quickstart. Do not add deployment, evals, or unrelated frameworks unless the user asks.
> * Prefer the Graph API structure shown on the fetched guide over inventing a different agent pattern.
> * Ask rather than guess when a secret, provider choice, or project convention is unclear.
>
> ## 2. Define tools and model
>
> This example uses the Claude Sonnet model and defines tools for addition, multiplication, and division.
>
> Create a file for the agent (`agent.py` or `agent.ts`). Add the following:
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langchain.tools import tool
> from langchain.chat_models import init_chat_model
>
>
> model = init_chat_model(
>     "claude-sonnet-4-6",
>     temperature=0
> )
>
>
> # Define tools
> @tool
> def multiply(a: int, b: int) -> int:
>     """Multiply `a` and `b`.
>
>     Args:
>         a: First int
>         b: Second int
>     """
>     return a * b
>
>
> @tool
> def add(a: int, b: int) -> int:
>     """Adds `a` and `b`.
>
>     Args:
>         a: First int
>         b: Second int
>     """
>     return a + b
>
>
> @tool
> def divide(a: int, b: int) -> float:
>     """Divide `a` and `b`.
>
>     Args:
>         a: First int
>         b: Second int
>     """
>     return a / b
>
>
> # Augment the LLM with tools
> tools = [add, multiply, divide]
> tools_by_name = {tool.name: tool for tool in tools}
> model_with_tools = model.bind_tools(tools)
> ```
>
> ## 3. Define state
>
> The graph's state stores the messages and the number of LLM calls.
>
> Add the following below the tools and model:
>
> > [!TIP]
> >
> > State in LangGraph persists throughout the agent's execution.
> >
> > The `Annotated` type with `operator.add` appends new messages to the list instead of replacing it.
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langchain.messages import AnyMessage
> from typing_extensions import TypedDict, Annotated
> import operator
>
>
> class MessagesState(TypedDict):
>     messages: Annotated[list[AnyMessage], operator.add]
>     llm_calls: int
> ```
>
> ## 4. Define model node
>
> The model node calls the LLM and decides whether to call a tool.
>
> Add the following below the state schema:
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langchain.messages import SystemMessage
>
>
> def llm_call(state: dict):
>     """LLM decides whether to call a tool or not"""
>
>     return {
>         "messages": [
>             model_with_tools.invoke(
>                 [
>                     SystemMessage(
>                         content="You are a helpful assistant tasked with performing arithmetic on a set of inputs."
>                     )
>                 ]
>                 + state["messages"]
>             )
>         ],
>         "llm_calls": state.get('llm_calls', 0) + 1
>     }
> ```
>
> ## 5. Define tool node
>
> The tool node calls the tools and returns the results.
>
> Add the following below the model node:
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langchain.messages import ToolMessage
>
>
> def tool_node(state: dict):
>     """Performs the tool call"""
>
>     result = []
>     for tool_call in state["messages"][-1].tool_calls:
>         tool = tools_by_name[tool_call["name"]]
>         observation = tool.invoke(tool_call["args"])
>         result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
>     return {"messages": result}
> ```
>
> ## 6. Define end logic
>
> The conditional edge function routes to the tool node or to the end, depending on whether the LLM made a tool call.
>
> Add the following below the tool node:
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from typing import Literal
> from langgraph.graph import StateGraph, START, END
>
>
> def should_continue(state: MessagesState) -> Literal["tool_node", END]:
>     """Decide if we should continue the loop or stop based upon whether the LLM made a tool call"""
>
>     messages = state["messages"]
>     last_message = messages[-1]
>
>     # If the LLM makes a tool call, then perform an action
>     if last_message.tool_calls:
>         return "tool_node"
>
>     # Otherwise, we stop (reply to the user)
>     return END
> ```
>
> ## 7. Build and compile the agent
>
> Add the following below the routing function. Build the graph with [`StateGraph`](https://reference.langchain.com/python/langgraph/graph/state/StateGraph) and compile it with [`compile`](https://reference.langchain.com/python/langgraph/graph/state/StateGraph/compile):
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> # Build workflow
> agent_builder = StateGraph(MessagesState)
>
> # Add nodes
> agent_builder.add_node("llm_call", llm_call)
> agent_builder.add_node("tool_node", tool_node)
>
> # Add edges to connect nodes
> agent_builder.add_edge(START, "llm_call")
> agent_builder.add_conditional_edges(
>     "llm_call",
>     should_continue,
>     ["tool_node", END]
> )
> agent_builder.add_edge("tool_node", "llm_call")
>
> # Compile the agent
> agent = agent_builder.compile()
> ```
>
> ## 8. Set up LangSmith tracing
>
> [LangSmith](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=oss-langgraph-quickstart) shows tool calls and model responses as the agent runs.
>
> This step is optional. Sign up at [smith.langchain.com](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=oss-langgraph-quickstart), create an API key, and set these environment variables in the shell before you run the agent:
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> export LANGSMITH_TRACING=true
> export LANGSMITH_API_KEY="<API_KEY>"
> ```
>
> ## 9. Run the agent
>
> Add the following below the compiled graph:
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langchain.messages import HumanMessage
>
> messages = [HumanMessage(content="Add 3 and 4.")]
> messages = agent.invoke({"messages": messages})
> for m in messages["messages"]:
>     m.pretty_print()
> ```
>
> Run the file:
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> python agent.py
> ```
>
> You should see the human message, a tool call to `add`, the tool result `7`, and a final assistant reply. The exact text varies by model, but the tool result is `7`.
>
> To check your file, compare it with the full example:
>
> > [accordion] Full code example
> >
> > ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > # Step 2: Define tools and model
> >
> > from langchain.tools import tool
> > from langchain.chat_models import init_chat_model
> >
> >
> > model = init_chat_model(
> >     "claude-sonnet-4-6",
> >     temperature=0
> > )
> >
> >
> > # Define tools
> > @tool
> > def multiply(a: int, b: int) -> int:
> >     """Multiply `a` and `b`.
> >
> >     Args:
> >         a: First int
> >         b: Second int
> >     """
> >     return a * b
> >
> >
> > @tool
> > def add(a: int, b: int) -> int:
> >     """Adds `a` and `b`.
> >
> >     Args:
> >         a: First int
> >         b: Second int
> >     """
> >     return a + b
> >
> >
> > @tool
> > def divide(a: int, b: int) -> float:
> >     """Divide `a` and `b`.
> >
> >     Args:
> >         a: First int
> >         b: Second int
> >     """
> >     return a / b
> >
> >
> > # Augment the LLM with tools
> > tools = [add, multiply, divide]
> > tools_by_name = {tool.name: tool for tool in tools}
> > model_with_tools = model.bind_tools(tools)
> >
> > # Step 3: Define state
> >
> > from langchain.messages import AnyMessage
> > from typing_extensions import TypedDict, Annotated
> > import operator
> >
> >
> > class MessagesState(TypedDict):
> >     messages: Annotated[list[AnyMessage], operator.add]
> >     llm_calls: int
> >
> > # Step 4: Define model node
> > from langchain.messages import SystemMessage
> >
> >
> > def llm_call(state: MessagesState):
> >     """LLM decides whether to call a tool or not"""
> >
> >     return {
> >         "messages": [
> >             model_with_tools.invoke(
> >                 [
> >                     SystemMessage(
> >                         content="You are a helpful assistant tasked with performing arithmetic on a set of inputs."
> >                     )
> >                 ]
> >                 + state["messages"]
> >             )
> >         ],
> >         "llm_calls": state.get('llm_calls', 0) + 1
> >     }
> >
> >
> > # Step 5: Define tool node
> >
> > from langchain.messages import ToolMessage
> >
> >
> > def tool_node(state: MessagesState):
> >     """Performs the tool call"""
> >
> >     result = []
> >     for tool_call in state["messages"][-1].tool_calls:
> >         tool = tools_by_name[tool_call["name"]]
> >         observation = tool.invoke(tool_call["args"])
> >         result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
> >     return {"messages": result}
> >
> > # Step 6: Define end logic
> >
> > from typing import Literal
> > from langgraph.graph import StateGraph, START, END
> >
> >
> > # Conditional edge function to route to the tool node or end based upon whether the LLM made a tool call
> > def should_continue(state: MessagesState) -> Literal["tool_node", END]:
> >     """Decide if we should continue the loop or stop based upon whether the LLM made a tool call"""
> >
> >     messages = state["messages"]
> >     last_message = messages[-1]
> >
> >     # If the LLM makes a tool call, then perform an action
> >     if last_message.tool_calls:
> >         return "tool_node"
> >
> >     # Otherwise, we stop (reply to the user)
> >     return END
> >
> > # Step 7: Build and compile the agent
> >
> > # Build workflow
> > agent_builder = StateGraph(MessagesState)
> >
> > # Add nodes
> > agent_builder.add_node("llm_call", llm_call)
> > agent_builder.add_node("tool_node", tool_node)
> >
> > # Add edges to connect nodes
> > agent_builder.add_edge(START, "llm_call")
> > agent_builder.add_conditional_edges(
> >     "llm_call",
> >     should_continue,
> >     ["tool_node", END]
> > )
> > agent_builder.add_edge("tool_node", "llm_call")
> >
> > # Compile the agent
> > agent = agent_builder.compile()
> >
> >
> > # Step 8: Set up LangSmith tracing (optional)
> > # export LANGSMITH_TRACING=true
> > # export LANGSMITH_API_KEY="<API_KEY>"
> >
> > # Step 9: Run the agent
> > from langchain.messages import HumanMessage
> > messages = [HumanMessage(content="Add 3 and 4.")]
> > messages = agent.invoke({"messages": messages})
> > for m in messages["messages"]:
> >     m.pretty_print()
> > ```

> [tab] Use the Functional API
>
> Build the LangGraph Functional API calculator quickstart
>
> Build a LangGraph calculator agent with the Functional API in this working directory by following the LangGraph quickstart.
>
> ## Step 1: Read the guide
>
> Detect whether this project uses Python or TypeScript/JavaScript. Fetch and follow the matching page; treat it as the source of truth for package names, model strings, and code:
>
> * Python: [https://docs.langchain.com/oss/python/langgraph/quickstart.md](Quickstart.md)
> * TypeScript: [https://docs.langchain.com/oss/javascript/langgraph/quickstart.md](https://docs.langchain.com/oss/javascript/langgraph/quickstart.md)
>
> Use only the **Use the Functional API** tab. Do not implement the Graph API path.
>
> ## Step 2: Install dependencies
>
> Install the packages required by the Functional API path with the package manager already used in this project.
>
> ## Step 3: Configure model credentials
>
> This quickstart uses Anthropic by default. Check whether `ANTHROPIC_API_KEY` is set. If it is not, ask the user to create a key and set it in the shell or a `.env` file, then stop and wait for confirmation. Do not invent, hardcode, or commit API keys. If the user prefers another chat model provider from the integrations docs, adapt the example accordingly after confirming.
>
> ## Step 4: Implement the calculator agent
>
> Define tools and model, then Functional API tasks and the entrypoint from the guide.
>
> ## Step 5: Optional LangSmith tracing
>
> Ask the user if they want tracing. If yes, ask them to set `LANGSMITH_TRACING=true` and `LANGSMITH_API_KEY` themselves. Do not invent a LangSmith key.
>
> ## Step 6: Run the agent
>
> Invoke the agent on a sample arithmetic query from the guide and print the final result.
>
> ## Rules
>
> * Stay scoped to this quickstart. Do not add deployment, evals, or unrelated frameworks unless the user asks.
> * Prefer the Functional API structure shown on the fetched guide over inventing a different agent pattern.
> * Ask rather than guess when a secret, provider choice, or project convention is unclear.
>
> ## 2. Define tools and model
>
> This example uses the Claude Sonnet model and defines tools for addition, multiplication, and division.
>
> Create a file for the agent (`agent.py` or `agent.ts`). Add the following:
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langchain.tools import tool
> from langchain.chat_models import init_chat_model
>
>
> model = init_chat_model(
>     "claude-sonnet-4-6",
>     temperature=0
> )
>
>
> # Define tools
> @tool
> def multiply(a: int, b: int) -> int:
>     """Multiply `a` and `b`.
>
>     Args:
>         a: First int
>         b: Second int
>     """
>     return a * b
>
>
> @tool
> def add(a: int, b: int) -> int:
>     """Adds `a` and `b`.
>
>     Args:
>         a: First int
>         b: Second int
>     """
>     return a + b
>
>
> @tool
> def divide(a: int, b: int) -> float:
>     """Divide `a` and `b`.
>
>     Args:
>         a: First int
>         b: Second int
>     """
>     return a / b
>
>
> # Augment the LLM with tools
> tools = [add, multiply, divide]
> tools_by_name = {tool.name: tool for tool in tools}
> model_with_tools = model.bind_tools(tools)
>
> from langgraph.graph import add_messages
> from langchain.messages import (
>     SystemMessage,
>     HumanMessage,
>     ToolCall,
> )
> from langchain_core.messages import BaseMessage
> from langgraph.func import entrypoint, task
> ```
>
> ## 3. Define model task
>
> The model task calls the LLM and decides whether to call a tool.
>
> Add the following below the tools and model:
>
> > [!TIP]
> >
> > The [`@task`](https://reference.langchain.com/python/langgraph/func/task) decorator marks a function as a task in the agent. Call tasks synchronously or asynchronously from the entrypoint.
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> @task
> def call_llm(messages: list[BaseMessage]):
>     """LLM decides whether to call a tool or not"""
>     return model_with_tools.invoke(
>         [
>             SystemMessage(
>                 content="You are a helpful assistant tasked with performing arithmetic on a set of inputs."
>             )
>         ]
>         + messages
>     )
> ```
>
> ## 4. Define tool task
>
> The tool task calls the tools and returns the results.
>
> Add the following below the model task:
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> @task
> def call_tool(tool_call: ToolCall):
>     """Performs the tool call"""
>     tool = tools_by_name[tool_call["name"]]
>     return tool.invoke(tool_call)
>
> ```
>
> ## 5. Define agent
>
> Add the following below the tasks. Define the agent with [`@entrypoint`](https://reference.langchain.com/python/langgraph/func/entrypoint):
>
> > [!NOTE]
> >
> > The Functional API uses ordinary control flow (loops and conditionals) in a single function instead of explicit nodes and edges.
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> @entrypoint()
> def agent(messages: list[BaseMessage]):
>     model_response = call_llm(messages).result()
>
>     while True:
>         if not model_response.tool_calls:
>             break
>
>         # Execute tools
>         tool_result_futures = [
>             call_tool(tool_call) for tool_call in model_response.tool_calls
>         ]
>         tool_results = [fut.result() for fut in tool_result_futures]
>         messages = add_messages(messages, [model_response, *tool_results])
>         model_response = call_llm(messages).result()
>
>     messages = add_messages(messages, model_response)
>     return messages
> ```
>
> ## 6. Set up LangSmith tracing
>
> [LangSmith](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=oss-langgraph-quickstart) shows tool calls and model responses as the agent runs.
>
> This step is optional. Sign up at [smith.langchain.com](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=oss-langgraph-quickstart), create an API key, and set these environment variables in the shell before you run the agent:
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> export LANGSMITH_TRACING=true
> export LANGSMITH_API_KEY="<API_KEY>"
> ```
>
> ## 7. Run the agent
>
> Add the following below the entrypoint:
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langchain.messages import HumanMessage
>
> messages = [HumanMessage(content="Add 3 and 4.")]
> messages = agent.invoke(messages)
> for m in messages:
>     m.pretty_print()
> ```
>
> Run the file:
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> python agent.py
> ```
>
> You should see the human message, a tool call to `add`, the tool result `7`, and a final assistant reply. The exact text varies by model, but the tool result is `7`.
>
> To check your file, compare it with the full example:
>
> > [accordion] Full code example
> >
> > ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > # Step 2: Define tools and model
> >
> > from langchain.tools import tool
> > from langchain.chat_models import init_chat_model
> >
> >
> > model = init_chat_model(
> >     "claude-sonnet-4-6",
> >     temperature=0
> > )
> >
> >
> > # Define tools
> > @tool
> > def multiply(a: int, b: int) -> int:
> >     """Multiply `a` and `b`.
> >
> >     Args:
> >         a: First int
> >         b: Second int
> >     """
> >     return a * b
> >
> >
> > @tool
> > def add(a: int, b: int) -> int:
> >     """Adds `a` and `b`.
> >
> >     Args:
> >         a: First int
> >         b: Second int
> >     """
> >     return a + b
> >
> >
> > @tool
> > def divide(a: int, b: int) -> float:
> >     """Divide `a` and `b`.
> >
> >     Args:
> >         a: First int
> >         b: Second int
> >     """
> >     return a / b
> >
> >
> > # Augment the LLM with tools
> > tools = [add, multiply, divide]
> > tools_by_name = {tool.name: tool for tool in tools}
> > model_with_tools = model.bind_tools(tools)
> >
> > from langgraph.graph import add_messages
> > from langchain.messages import (
> >     SystemMessage,
> >     HumanMessage,
> >     ToolCall,
> > )
> > from langchain_core.messages import BaseMessage
> > from langgraph.func import entrypoint, task
> >
> >
> > # Step 3: Define model task
> >
> > @task
> > def call_llm(messages: list[BaseMessage]):
> >     """LLM decides whether to call a tool or not"""
> >     return model_with_tools.invoke(
> >         [
> >             SystemMessage(
> >                 content="You are a helpful assistant tasked with performing arithmetic on a set of inputs."
> >             )
> >         ]
> >         + messages
> >     )
> >
> >
> > # Step 4: Define tool task
> >
> > @task
> > def call_tool(tool_call: ToolCall):
> >     """Performs the tool call"""
> >     tool = tools_by_name[tool_call["name"]]
> >     return tool.invoke(tool_call)
> >
> >
> > # Step 5: Define agent
> >
> > @entrypoint()
> > def agent(messages: list[BaseMessage]):
> >     model_response = call_llm(messages).result()
> >
> >     while True:
> >         if not model_response.tool_calls:
> >             break
> >
> >         # Execute tools
> >         tool_result_futures = [
> >             call_tool(tool_call) for tool_call in model_response.tool_calls
> >         ]
> >         tool_results = [fut.result() for fut in tool_result_futures]
> >         messages = add_messages(messages, [model_response, *tool_results])
> >         model_response = call_llm(messages).result()
> >
> >     messages = add_messages(messages, model_response)
> >     return messages
> >
> > # Step 6: Set up LangSmith tracing (optional)
> > # export LANGSMITH_TRACING=true
> > # export LANGSMITH_API_KEY="<API_KEY>"
> >
> > # Step 7: Run the agent
> > messages = [HumanMessage(content="Add 3 and 4.")]
> > messages = agent.invoke(messages)
> > for m in messages:
> >     m.pretty_print()
> > ```

## Next steps

You now have a working calculator agent. Continue with one of the following subjects:

* **Learn the APIs**: [Choosing between Graph and Functional APIs](Choosing%20between%20Graph%20and%20Functional%20APIs.md), then the [Build checklist for the Graph API](../Build%20with%20the%20Graph%20API/Build%20checklist%20for%20the%20Graph%20API.md) or the [Build checklist for the Functional API](../Advanced/Build%20with%20the%20Functional%20API/Build%20checklist%20for%20the%20Functional%20API.md).
* **Add persistence**: Use a [checkpointer](../Capabilities/Persistence.md) so runs can pause and resume across sessions.
* **Add human-in-the-loop**: Pause with [interrupts](../Capabilities/Interrupts.md) for approval or edits.
* **Stream results**: Follow [streaming](../Capabilities/Streaming.md) for tokens and state updates.
* **Go deeper**: [Thinking in the Graph API](../Build%20with%20the%20Graph%20API/Thinking%20in%20the%20Graph%20API.md), [Thinking in the Functional API](../Advanced/Build%20with%20the%20Functional%20API/Thinking%20in%20the%20Functional%20API.md), and [Workflows and agents](../Patterns/Workflows%20and%20agents.md).
* **Deploy**: Host the agent with [LangSmith Deployment](https://docs.langchain.com/langsmith/deployment.md).
* **Evaluate**: Test behavior with [LangSmith evaluation](https://docs.langchain.com/langsmith/evaluation-quickstart.md).

# Tools

> Connect Deep Agents to custom functions, APIs, databases, and any MCP server

Deep Agents can call any tool you define, any [LangChain tool](https://docs.langchain.com/oss/python/langchain/tools.md), and tools from any [MCP server](#mcp-tools).
Pass them to `create_deep_agent` via the `tools=` parameter alongside the [built-in harness tools](../Deep%20Agents%20overview.md#execution-environment) for file management and subagent spawning.

```python Google theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent


agent = create_deep_agent(
    model="google_genai:gemini-3.6-flash",
    tools=[search, fetch_url, run_query],
)
```

```python OpenAI theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent


agent = create_deep_agent(
    model="openai:gpt-5.5",
    tools=[search, fetch_url, run_query],
)
```

```python Anthropic theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent


agent = create_deep_agent(
    model="anthropic:claude-sonnet-5",
    tools=[search, fetch_url, run_query],
)
```

```python OpenRouter theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent


agent = create_deep_agent(
    model="openrouter:z-ai/glm-5.2",
    tools=[search, fetch_url, run_query],
)
```

```python Fireworks theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent


agent = create_deep_agent(
    model="fireworks:accounts/fireworks/models/glm-5p2",
    tools=[search, fetch_url, run_query],
)
```

```python Baseten theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent


agent = create_deep_agent(
    model="baseten:zai-org/GLM-5.2",
    tools=[search, fetch_url, run_query],
)
```

```python Ollama theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent


agent = create_deep_agent(
    model="ollama:north-mini-code-1.0",
    tools=[search, fetch_url, run_query],
)
```

## Custom tools

Pass any callable, such as plain functions, LangChain `@tool`-decorated functions, or tool dicts—directly to `tools=`.
Deep Agents infers the tool schema from the function signature and docstring, so you don't need to define a separate schema in most cases.

```python Google theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
import os
from typing import Literal
from tavily import TavilyClient
from deepagents import create_deep_agent

tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])


def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
):
    """Run a web search"""
    return tavily_client.search(
        query,
        max_results=max_results,
        include_raw_content=include_raw_content,
        topic=topic,
    )


agent = create_deep_agent(
    model="google_genai:gemini-3.6-flash",
    tools=[internet_search],
)
```

```python OpenAI theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
import os
from typing import Literal
from tavily import TavilyClient
from deepagents import create_deep_agent

tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])


def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
):
    """Run a web search"""
    return tavily_client.search(
        query,
        max_results=max_results,
        include_raw_content=include_raw_content,
        topic=topic,
    )


agent = create_deep_agent(
    model="openai:gpt-5.5",
    tools=[internet_search],
)
```

```python Anthropic theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
import os
from typing import Literal
from tavily import TavilyClient
from deepagents import create_deep_agent

tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])


def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
):
    """Run a web search"""
    return tavily_client.search(
        query,
        max_results=max_results,
        include_raw_content=include_raw_content,
        topic=topic,
    )


agent = create_deep_agent(
    model="anthropic:claude-sonnet-5",
    tools=[internet_search],
)
```

```python OpenRouter theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
import os
from typing import Literal
from tavily import TavilyClient
from deepagents import create_deep_agent

tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])


def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
):
    """Run a web search"""
    return tavily_client.search(
        query,
        max_results=max_results,
        include_raw_content=include_raw_content,
        topic=topic,
    )


agent = create_deep_agent(
    model="openrouter:z-ai/glm-5.2",
    tools=[internet_search],
)
```

```python Fireworks theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
import os
from typing import Literal
from tavily import TavilyClient
from deepagents import create_deep_agent

tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])


def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
):
    """Run a web search"""
    return tavily_client.search(
        query,
        max_results=max_results,
        include_raw_content=include_raw_content,
        topic=topic,
    )


agent = create_deep_agent(
    model="fireworks:accounts/fireworks/models/glm-5p2",
    tools=[internet_search],
)
```

```python Baseten theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
import os
from typing import Literal
from tavily import TavilyClient
from deepagents import create_deep_agent

tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])


def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
):
    """Run a web search"""
    return tavily_client.search(
        query,
        max_results=max_results,
        include_raw_content=include_raw_content,
        topic=topic,
    )


agent = create_deep_agent(
    model="baseten:zai-org/GLM-5.2",
    tools=[internet_search],
)
```

```python Ollama theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
import os
from typing import Literal
from tavily import TavilyClient
from deepagents import create_deep_agent

tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])


def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
):
    """Run a web search"""
    return tavily_client.search(
        query,
        max_results=max_results,
        include_raw_content=include_raw_content,
        topic=topic,
    )


agent = create_deep_agent(
    model="ollama:north-mini-code-1.0",
    tools=[internet_search],
)
```

For full details on defining and using LangChain tools (tool dicts, `StructuredTool`, return types, error handling, and more), see [Tools](https://docs.langchain.com/oss/python/langchain/tools.md).

## MCP tools

> [!NOTE]
>
> Deep Agents fully support [Model Context Protocol (MCP)](../Protocols/Model%20Context%20Protocol%20%28MCP%29.md), the open standard for connecting agents to external services. Load tools from any MCP server and pass them directly to `create_deep_agent`.

MCP is an open protocol that lets agents connect to a growing ecosystem of servers—databases, APIs, file systems, browsers, and more—through a standard interface. Instead of writing custom integration code for each service, you point Deep Agents at an MCP server and it gets all the tools that server exposes.

Install LangChain with the `mcp` extra to connect to MCP servers:

```bash pip theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
pip install "langchain[mcp]"
```

```bash uv theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
uv add "langchain[mcp]"
```

```python Google theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
import asyncio

from deepagents import create_deep_agent
from langchain.mcp import MCPAdapter


async def main():
    config = {"mcpServers": {"my_server": {"url": "http://localhost:8000/mcp"}}}
    async with MCPAdapter(config) as adapter:
        tools = await adapter.list_tools()
        agent = create_deep_agent(
            model="google_genai:gemini-3.6-flash",
            tools=tools,
        )
        await agent.ainvoke(
            {
                "messages": [
                    {"role": "user", "content": "Use the MCP server to help me."}
                ]
            },
            config={"configurable": {"thread_id": "1"}},
        )
```

```python OpenAI theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
import asyncio

from deepagents import create_deep_agent
from langchain.mcp import MCPAdapter


async def main():
    config = {"mcpServers": {"my_server": {"url": "http://localhost:8000/mcp"}}}
    async with MCPAdapter(config) as adapter:
        tools = await adapter.list_tools()
        agent = create_deep_agent(
            model="openai:gpt-5.5",
            tools=tools,
        )
        await agent.ainvoke(
            {
                "messages": [
                    {"role": "user", "content": "Use the MCP server to help me."}
                ]
            },
            config={"configurable": {"thread_id": "1"}},
        )
```

```python Anthropic theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
import asyncio

from deepagents import create_deep_agent
from langchain.mcp import MCPAdapter


async def main():
    config = {"mcpServers": {"my_server": {"url": "http://localhost:8000/mcp"}}}
    async with MCPAdapter(config) as adapter:
        tools = await adapter.list_tools()
        agent = create_deep_agent(
            model="anthropic:claude-sonnet-5",
            tools=tools,
        )
        await agent.ainvoke(
            {
                "messages": [
                    {"role": "user", "content": "Use the MCP server to help me."}
                ]
            },
            config={"configurable": {"thread_id": "1"}},
        )
```

```python OpenRouter theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
import asyncio

from deepagents import create_deep_agent
from langchain.mcp import MCPAdapter


async def main():
    config = {"mcpServers": {"my_server": {"url": "http://localhost:8000/mcp"}}}
    async with MCPAdapter(config) as adapter:
        tools = await adapter.list_tools()
        agent = create_deep_agent(
            model="openrouter:z-ai/glm-5.2",
            tools=tools,
        )
        await agent.ainvoke(
            {
                "messages": [
                    {"role": "user", "content": "Use the MCP server to help me."}
                ]
            },
            config={"configurable": {"thread_id": "1"}},
        )
```

```python Fireworks theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
import asyncio

from deepagents import create_deep_agent
from langchain.mcp import MCPAdapter


async def main():
    config = {"mcpServers": {"my_server": {"url": "http://localhost:8000/mcp"}}}
    async with MCPAdapter(config) as adapter:
        tools = await adapter.list_tools()
        agent = create_deep_agent(
            model="fireworks:accounts/fireworks/models/glm-5p2",
            tools=tools,
        )
        await agent.ainvoke(
            {
                "messages": [
                    {"role": "user", "content": "Use the MCP server to help me."}
                ]
            },
            config={"configurable": {"thread_id": "1"}},
        )
```

```python Baseten theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
import asyncio

from deepagents import create_deep_agent
from langchain.mcp import MCPAdapter


async def main():
    config = {"mcpServers": {"my_server": {"url": "http://localhost:8000/mcp"}}}
    async with MCPAdapter(config) as adapter:
        tools = await adapter.list_tools()
        agent = create_deep_agent(
            model="baseten:zai-org/GLM-5.2",
            tools=tools,
        )
        await agent.ainvoke(
            {
                "messages": [
                    {"role": "user", "content": "Use the MCP server to help me."}
                ]
            },
            config={"configurable": {"thread_id": "1"}},
        )
```

```python Ollama theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
import asyncio

from deepagents import create_deep_agent
from langchain.mcp import MCPAdapter


async def main():
    config = {"mcpServers": {"my_server": {"url": "http://localhost:8000/mcp"}}}
    async with MCPAdapter(config) as adapter:
        tools = await adapter.list_tools()
        agent = create_deep_agent(
            model="ollama:north-mini-code-1.0",
            tools=tools,
        )
        await agent.ainvoke(
            {
                "messages": [
                    {"role": "user", "content": "Use the MCP server to help me."}
                ]
            },
            config={"configurable": {"thread_id": "1"}},
        )
```

For detailed configuration options—including stdio servers, OAuth authentication, tool filtering, and stateful sessions—see the full [MCP guide](../Protocols/Model%20Context%20Protocol%20%28MCP%29.md).

## Built-in harness tools

In addition to the tools you provide, every Deep Agent comes with a built-in set of tools from the harness:

| Tool | Description |
| - | - |
| `ls` | List files in a directory. |
| `read_file` | Read file contents (with pagination and multimodal support). |
| `write_file` | Create a new file, or overwrite an existing one. |
| `edit_file` | Perform exact string replacements in files. |
| `delete` | Delete a file, or a directory and its contents recursively. The `delete` tool requires `deepagents>=0.7`. |
| `glob` | Find files matching a glob pattern. |
| `grep` | Search file contents. |
| `execute` | Run shell commands (sandbox backends only). |
| `task` | Spawn a subagent to handle a delegated task. |

To add structured task planning with `write_todos`, opt in with [`TodoListMiddleware`](https://reference.langchain.com/python/langchain/agents/middleware/todo/TodoListMiddleware). See [Task planning](../Deep%20Agents%20overview.md#task-planning).

For a full breakdown of what each built-in tool does, see [Harness overview](../Deep%20Agents%20overview.md#execution-environment).

## Multimodal tool outputs

Custom tools can return plain text or [standard content blocks](https://docs.langchain.com/oss/python/langchain/messages.md#standard-content-blocks) (text, images, audio, video, and files) when the selected model supports multimodal tool results. The built-in `read_file` tool also returns multimodal blocks for supported non-text file types.

Return a string for text-only results, or an ordered list of content blocks for text plus media or interleaved multimodal output. See [Multimodal](Multimodal%20inputs%20and%20outputs.md) and [Tool return values](https://docs.langchain.com/oss/python/langchain/tools.md#return-multimodal-content) for examples and context-compression considerations.

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/deepagents/tools.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

# Agent Client Protocol (ACP)

> Expose Deep Agents over the Agent Client Protocol (ACP) to integrate with code editors and IDEs.

[Agent Client Protocol (ACP)](https://agentclientprotocol.com/get-started/introduction) standardizes communication between coding agents and code editors or IDEs.
With the ACP protocol, you can make use of your custom deep agents with any ACP-compatible client, allowing your code editor to provide project context and receive rich updates.

> [!NOTE]
>
> ACP is designed for agent-editor integrations. If you want your agent to call tools hosted by external servers, see [Model Context Protocol (MCP)](Model%20Context%20Protocol%20%28MCP%29.md).

## Quickstart

Install the ACP integration package:

```bash pip theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
pip install deepagents-acp
```

```bash uv theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
uv add deepagents-acp
```

Then expose a deep agent over ACP.

This starts an ACP server in stdio mode (it reads requests from stdin and writes responses to stdout). In practice, you usually run this as a command launched by an ACP client (for example, your editor), which then communicates with the server over stdio.

```python Google theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
import asyncio

from acp import run_agent
from deepagents import create_deep_agent
from langgraph.checkpoint.memory import MemorySaver

from deepagents_acp.server import AgentServerACP


async def main() -> None:
    agent = create_deep_agent(
        model="google_genai:gemini-3.6-flash",
        # You can customize your deep agent here: set a custom prompt,
        # add your own tools, attach middleware, or compose subagents.
        system_prompt="You are a helpful coding assistant",
        checkpointer=MemorySaver(),
    )

    server = AgentServerACP(agent)
    await run_agent(server)

if __name__ == "__main__":
    asyncio.run(main())
```

```python OpenAI theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
import asyncio

from acp import run_agent
from deepagents import create_deep_agent
from langgraph.checkpoint.memory import MemorySaver

from deepagents_acp.server import AgentServerACP


async def main() -> None:
    agent = create_deep_agent(
        model="openai:gpt-5.5",
        # You can customize your deep agent here: set a custom prompt,
        # add your own tools, attach middleware, or compose subagents.
        system_prompt="You are a helpful coding assistant",
        checkpointer=MemorySaver(),
    )

    server = AgentServerACP(agent)
    await run_agent(server)

if __name__ == "__main__":
    asyncio.run(main())
```

```python Anthropic theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
import asyncio

from acp import run_agent
from deepagents import create_deep_agent
from langgraph.checkpoint.memory import MemorySaver

from deepagents_acp.server import AgentServerACP


async def main() -> None:
    agent = create_deep_agent(
        model="anthropic:claude-sonnet-5",
        # You can customize your deep agent here: set a custom prompt,
        # add your own tools, attach middleware, or compose subagents.
        system_prompt="You are a helpful coding assistant",
        checkpointer=MemorySaver(),
    )

    server = AgentServerACP(agent)
    await run_agent(server)

if __name__ == "__main__":
    asyncio.run(main())
```

```python OpenRouter theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
import asyncio

from acp import run_agent
from deepagents import create_deep_agent
from langgraph.checkpoint.memory import MemorySaver

from deepagents_acp.server import AgentServerACP


async def main() -> None:
    agent = create_deep_agent(
        model="openrouter:z-ai/glm-5.2",
        # You can customize your deep agent here: set a custom prompt,
        # add your own tools, attach middleware, or compose subagents.
        system_prompt="You are a helpful coding assistant",
        checkpointer=MemorySaver(),
    )

    server = AgentServerACP(agent)
    await run_agent(server)

if __name__ == "__main__":
    asyncio.run(main())
```

```python Fireworks theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
import asyncio

from acp import run_agent
from deepagents import create_deep_agent
from langgraph.checkpoint.memory import MemorySaver

from deepagents_acp.server import AgentServerACP


async def main() -> None:
    agent = create_deep_agent(
        model="fireworks:accounts/fireworks/models/glm-5p2",
        # You can customize your deep agent here: set a custom prompt,
        # add your own tools, attach middleware, or compose subagents.
        system_prompt="You are a helpful coding assistant",
        checkpointer=MemorySaver(),
    )

    server = AgentServerACP(agent)
    await run_agent(server)

if __name__ == "__main__":
    asyncio.run(main())
```

```python Baseten theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
import asyncio

from acp import run_agent
from deepagents import create_deep_agent
from langgraph.checkpoint.memory import MemorySaver

from deepagents_acp.server import AgentServerACP


async def main() -> None:
    agent = create_deep_agent(
        model="baseten:zai-org/GLM-5.2",
        # You can customize your deep agent here: set a custom prompt,
        # add your own tools, attach middleware, or compose subagents.
        system_prompt="You are a helpful coding assistant",
        checkpointer=MemorySaver(),
    )

    server = AgentServerACP(agent)
    await run_agent(server)

if __name__ == "__main__":
    asyncio.run(main())
```

```python Ollama theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
import asyncio

from acp import run_agent
from deepagents import create_deep_agent
from langgraph.checkpoint.memory import MemorySaver

from deepagents_acp.server import AgentServerACP


async def main() -> None:
    agent = create_deep_agent(
        model="ollama:north-mini-code-1.0",
        # You can customize your deep agent here: set a custom prompt,
        # add your own tools, attach middleware, or compose subagents.
        system_prompt="You are a helpful coding assistant",
        checkpointer=MemorySaver(),
    )

    server = AgentServerACP(agent)
    await run_agent(server)

if __name__ == "__main__":
    asyncio.run(main())
```

> [card] [Example coding agent](https://github.com/langchain-ai/deepagents/blob/main/libs/acp/examples/demo_agent.py)
>
> The `deepagents-acp` package includes an example coding agent with filesystem and shell that you can run out of the box.

## Clients

Deep agents work anywhere you can run an ACP agent server. Some notable ACP clients include:

* [Zed](https://zed.dev/docs/ai/external-agents)
* [JetBrains IDEs](https://www.jetbrains.com/help/ai-assistant/acp.html)
* Visual Studio Code (via [vscode-acp](https://github.com/formulahendry/vscode-acp))
* Neovim (via ACP-compatible plugins)

### Zed

The `deepagents` repo includes [a demo ACP entrypoint](https://github.com/langchain-ai/deepagents/blob/main/libs/acp/run_demo_agent.sh) you can register with [Zed](https://zed.dev/docs/ai/external-agents):

1. Clone the `deepagents` repo and install dependencies:

```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
git clone https://github.com/langchain-ai/deepagents.git
cd deepagents/libs/acp
uv sync --all-groups
chmod +x run_demo_agent.sh
```

2. Configure credentials for the demo agent:

```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
cp .env.example .env
```

Then set `ANTHROPIC_API_KEY` in `.env`.

3. Configure your ACP agent server command in Zed's `settings.json`:

```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
{
  "agent_servers": {
    "DeepAgents": {
      "type": "custom",
      "command": "/your/absolute/path/to/deepagents/libs/acp/run_demo_agent.sh"
    }
  }
}
```

4. Open Zed's Agents panel and start a Deep Agents thread.

### Toad

If you want to run an ACP agent server as a local dev tool, you can use [Toad](https://github.com/batrachianai/toad) to manage the process.

```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
uv tool install -U batrachian-toad

toad acp "python path/to/your_server.py" .
# or
toad acp "uv run python path/to/your_server.py" .
```

> [!NOTE]
>
> See the upstream ACP docs for protocol details and editor support:
>
> * Introduction: [https://agentclientprotocol.com/get-started/introduction](https://agentclientprotocol.com/get-started/introduction)
> * Clients/editors: [https://agentclientprotocol.com/get-started/clients](https://agentclientprotocol.com/get-started/clients)

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/deepagents/acp.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

# Trace with the Claude Agent SDK

The [Claude Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) is an SDK for building agents with Claude. LangSmith provides native integration with the Claude Agent SDK to automatically trace your agent executions, tool calls, and interactions with Claude models.

> [!NOTE]
>
> In an [agent-based workspace](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20Registry.md), [create an agent](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md) once before sending traces. Use [agent addressing](../../../Configuration%20%26%20troubleshooting/Agent%20%26%20environment%20settings/Log%20traces%20to%20an%20agent.md) to select its identifier and environment. If an integration requires `project_name`, use the selected environment's [`tracer_session_name`](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md#use-an-environment-project) as a compatibility value.

## Installation

Install the LangSmith integration for Claude Agent SDK

```bash uv
uv add "langsmith[claude-agent-sdk]"
```

```bash pip
pip install langsmith[claude-agent-sdk]
```

```bash pnpm
pnpm add @anthropic-ai/claude-agent-sdk langsmith zod
```

```bash npm
npm install @anthropic-ai/claude-agent-sdk langsmith zod
```

## Setup

Sending traces to an agent requires `langsmith>=0.14.9` in Python or `langsmith@>=0.11.0` in TypeScript.

Set your [API keys](../../../../../LangSmith%20setup/Account/Create%20an%20account%20and%20API%20key.md), agent identifier, and environment:

```bash shell
export LANGSMITH_TRACING=true
export LANGSMITH_ENDPOINT=https://api.smith.langchain.com
export LANGSMITH_API_KEY=<your_langsmith_api_key>
export LANGSMITH_AGENT_ID="<your-agent-id>"
export LANGSMITH_AGENT_ENVIRONMENT="local"

export ANTHROPIC_API_KEY=<your_anthropic_api_key>
```

```dotenv .env
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=<your_langsmith_api_key>
LANGSMITH_AGENT_ID="<your-agent-id>"
LANGSMITH_AGENT_ENVIRONMENT="local"

ANTHROPIC_API_KEY=<your_anthropic_api_key>
```

Get your LangSmith API key from **Settings** in the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-trace-claude-agent-sdk). Use the agent identifier and environment selected during setup.

For an Anthropic API key, refer to the [Claude console](https://console.anthropic.com/settings/keys).

## Quickstart

To enable LangSmith tracing for your Claude Agent SDK code, call `configure_claude_agent_sdk()` before running your agent:

```python Python
import asyncio
from typing import Any

from claude_agent_sdk import (
    ClaudeAgentOptions,
    ClaudeSDKClient,
    create_sdk_mcp_server,
    tool,
)
from langsmith.integrations.claude_agent_sdk import configure_claude_agent_sdk

configure_claude_agent_sdk()


@tool(
    "get_weather",
    "Gets the current weather for a given city",
    {"city": str},
)
async def get_weather(args: dict[str, Any]) -> dict[str, Any]:
    city = args["city"]
    weather_data = {
        "San Francisco": "Foggy, 62°F",
        "New York": "Sunny, 75°F",
        "London": "Rainy, 55°F",
        "Tokyo": "Clear, 68°F",
    }
    weather = weather_data.get(city, "Weather data not available")
    return {"content": [{"type": "text", "text": f"Weather in {city}: {weather}"}]}


async def main() -> None:
    weather_server = create_sdk_mcp_server(
        name="weather",
        version="1.0.0",
        tools=[get_weather],
    )

    options = ClaudeAgentOptions(
        model="claude-sonnet-5-5",
        system_prompt="You are a friendly travel assistant who helps with weather information.",
        mcp_servers={"weather": weather_server},
        allowed_tools=["mcp__weather__get_weather"],
    )

    async with ClaudeSDKClient(options=options) as client:
        await client.query("What's the weather like in San Francisco and Tokyo?")

        async for message in client.receive_response():
            print(message)


if __name__ == "__main__":
    asyncio.run(main())
```

```typescript TypeScript
import * as originalSdk from '@anthropic-ai/claude-agent-sdk';

import { wrapClaudeAgentSDK } from 'langsmith/experimental/anthropic';
import { z } from 'zod/v4';

const sdk = wrapClaudeAgentSDK(originalSdk);

const getWeather = sdk.tool(
  'get_weather',
  'Gets the current weather for a given city',
  {
    city: z.string(),
  },
  async ({ city }) => {
    const weatherData: Record<string, string> = {
      'San Francisco': 'Foggy, 62°F',
      'New York': 'Sunny, 75°F',
      London: 'Rainy, 55°F',
      Tokyo: 'Clear, 68°F',
    };
    const weather = weatherData[city] ?? 'Weather data not available';
    return {
      content: [{ type: 'text' as const, text: weather }],
    };
  }
);

const weatherServer = sdk.createSdkMcpServer({
  name: 'weather',
  version: '1.0.0',
  tools: [getWeather],
});

const query = sdk.query({
  prompt: "What's the weather like in San Francisco and Tokyo?",
  options: {
    model: 'claude-sonnet-5-5',
    systemPrompt:
      'You are a friendly travel assistant who helps with weather information.',
    mcpServers: { weather: weatherServer },
    allowedTools: ['mcp__weather__get_weather'],
  },
});

for await (const chunk of query) {
  console.log(chunk);
}
```

Once configured, all Claude Agent SDK operations will be automatically traced to LangSmith, including:

* Agent queries and responses
* Tool invocations and results
* Claude model interactions
* MCP server operations

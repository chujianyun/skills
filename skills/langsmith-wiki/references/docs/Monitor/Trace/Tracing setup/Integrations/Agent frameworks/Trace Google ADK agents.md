# Trace Google ADK agents

This guide shows you how to trace [Google Agent Development Kit (ADK)](https://github.com/google/adk-python) agents in LangSmith. You'll configure automatic tracing for your ADK agents to capture agent invocations, tool calls, and LLM interactions.

> [!NOTE]
>
> This guide covers ADK's standard execution paths (text agents, tools, and multi-agent workflows). To trace a **Gemini Live** voice agent, which uses ADK's `Runner.run_live` streaming loop, see [Trace Gemini Live agents](../Voice%20AI%20frameworks/Trace%20Gemini%20Live%20agents.md).

> [!NOTE]
>
> In an [agent-based workspace](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20Registry.md), [create an agent](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md) once before sending traces. Use [agent addressing](../../../Configuration%20%26%20troubleshooting/Agent%20%26%20environment%20settings/Log%20traces%20to%20an%20agent.md) to select its identifier and environment. If an integration requires `project_name`, use the selected environment's [`tracer_session_name`](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md#use-an-environment-project) as a compatibility value.

## Installation

Install the required packages using your preferred package manager:

```bash uv
uv add "langsmith[google-adk]"
```

```bash pip
pip install langsmith[google-adk]
```

## Setup

Sending traces to an agent requires `langsmith>=0.14.9`.

Set your [API keys](../../../../../LangSmith%20setup/Account/Create%20an%20account%20and%20API%20key.md), agent identifier, and environment:

```bash shell
export LANGSMITH_TRACING=true
export LANGSMITH_ENDPOINT=https://api.smith.langchain.com
export LANGSMITH_API_KEY=<your_langsmith_api_key>
export LANGSMITH_AGENT_ID="<your-agent-id>"
export LANGSMITH_AGENT_ENVIRONMENT="local"

export GOOGLE_API_KEY=<your_google_api_key>
```

```dotenv .env
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=<your_langsmith_api_key>
LANGSMITH_AGENT_ID="<your-agent-id>"
LANGSMITH_AGENT_ENVIRONMENT="local"

GOOGLE_API_KEY=<your_google_api_key>
```

To create a Google API key, refer to [Google AI Studio](https://aistudio.google.com/api-keys).

## Configure tracing

To trace ADK agents, use `configure_google_adk()` from the LangSmith SDK. Call this function once before creating any ADK agents:

```python
from langsmith.integrations.google_adk import configure_google_adk

configure_google_adk()
```

The function accepts the following optional parameters:

* `address`: An agent address to send traces to instead of the one `LANGSMITH_AGENT_ID` and `LANGSMITH_AGENT_ENVIRONMENT` name, for example `ls.agent_address("my-agent", "production")`. Cannot be combined with `project_name`. Requires `langsmith>=0.14.14`.
* `project_name`: Compatibility override for project-based tracing. Leave it unset to use the configured agent and environment.
* `name`: Name for the root trace. Defaults to `"google_adk.session"`.
* `metadata`: Dictionary of key-value pairs for additional context.
* `tags`: List of strings to categorize traces.

## Example

This example creates a weather agent with a tool, then runs it with tracing enabled:

```python
import asyncio

from dotenv import load_dotenv  # Optional
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from langsmith.integrations.google_adk import configure_google_adk

load_dotenv()  # Optional


async def main():
    # Configure LangSmith tracing
    configure_google_adk()

    # Define a tool
    def get_weather(city: str) -> dict:
        """Get weather for a city."""
        return {"city": city, "temperature": "72°F", "conditions": "Sunny"}

    # Create the agent
    agent = Agent(
        name="weather_agent",
        model="gemini-4-hydrogen",
        description="Provides weather information.",
        instruction="Use the get_weather tool to answer weather questions.",
        tools=[get_weather],
    )

    # Set up session and runner
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name="weather_app",
        user_id="user_123",
        session_id="session_456",
    )

    runner = Runner(
        agent=agent,
        app_name="weather_app",
        session_service=session_service,
    )

    # Run the agent
    async for event in runner.run_async(
        user_id="user_123",
        session_id=session.id,
        new_message=types.Content(
            role="user",
            parts=[types.Part(text="What's the weather in San Francisco?")],
        ),
    ):
        if event.is_final_response():
            print(event.content.parts[0].text)


if __name__ == "__main__":
    asyncio.run(main())
```

## View traces in LangSmith

After running your agent, you can view traces in the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-trace-with-google-adk) that include:

* **Agent invocations**: Complete flows through your ADK agents
* **Tool calls**: Individual function calls made by agents
* **LLM interactions**: Requests and responses from Gemini models
* **Multi-agent workflows**: Traces from sequential and parallel agent compositions

## Custom metadata and tags

Add metadata and tags when configuring tracing to categorize and filter traces:

```python
from langsmith.integrations.google_adk import configure_google_adk

configure_google_adk(
    metadata={
        "environment": "production",
        "team": "ml-platform",
    },
    tags=["adk", "weather", "v2"],
)
```

## Multi-agent workflows

The integration automatically traces multi-agent workflows including sequential and parallel agent compositions:

```python
import asyncio

from dotenv import load_dotenv  # Optional
from google.adk.agents import Agent, SequentialAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from langsmith.integrations.google_adk import configure_google_adk

load_dotenv()  # Optional


async def main():
    # Configure LangSmith tracing
    # Traces go to LANGSMITH_PROJECT env var by default.
    # Pass project_name="my-project" to override.
    configure_google_adk()

    # Create sub-agents
    translator = Agent(
        name="translator",
        model="gemini-4-hydrogen",
        description="Translates text to English.",
    )

    summarizer = Agent(
        name="summarizer",
        model="gemini-4-hydrogen",
        description="Summarizes text concisely.",
    )

    # Create a sequential agent that runs sub-agents in order
    pipeline = SequentialAgent(
        name="translate_and_summarize",
        sub_agents=[translator, summarizer],
        description="Translates text then summarizes it.",
    )

    # Set up and run
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name="pipeline_app",
        user_id="user_123",
        session_id="session_456",
    )

    runner = Runner(
        agent=pipeline,
        app_name="pipeline_app",
        session_service=session_service,
    )

    events = runner.run_async(
        user_id="user_123",
        session_id=session.id,
        new_message=types.Content(
            role="user",
            parts=[types.Part(text="Quelle est la plus haute tour de Paris?")],
        ),
    )

    async for event in events:
        if event.is_final_response():
            print(event.content.parts[0].text)


if __name__ == "__main__":
    asyncio.run(main())
```

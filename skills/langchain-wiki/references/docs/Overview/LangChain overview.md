# LangChain overview

> LangChain provides create_agent: a minimal, highly configurable agent harness. Compose exactly the agent your use case needs from model, tools, prompt, and middleware.

**Agent = Model + Harness.** LangChain provides `create_agent`: a minimal, highly configurable harness. The harness is everything around the model loop: the prompt, the tools, and any middleware that shapes behavior. Start with the primitives and compose exactly what your use case needs. Supports [OpenAI, Anthropic, Google, and more](https://docs.langchain.com/oss/python/integrations/providers/overview.md).

> [!TIP]
>
> **LangChain vs. LangGraph vs. Deep Agents**
>
> Start with [Managed Deep Agents](https://docs.langchain.com/langsmith/python/managed-deep-agents-overview.md) for a batteries-included harness (context compression, virtual filesystem, subagents) when you want to run production agents without having to manage infrastructure. Alternatively, for maximum flexibility while using the same Deep Agents harness, use the [Deep Agents SDK](https://docs.langchain.com/oss/python/deepagents/overview.md#self-host-with-the-sdk) and host agents yourself, or run a custom [Agent Server](https://docs.langchain.com/langsmith/deployment.md). Deep Agents is built on LangChain [agents](../Core%20components/Agents.md), which you can also use directly.
>
> Use [LangChain](../Core%20components/Agents.md) (`create_agent`) for a highly customizable harness, easily tailored to your use case and data.
>
> Use [LangGraph](https://docs.langchain.com/oss/python/langgraph/overview.md), our low-level orchestration framework, for advanced needs combining deterministic and agentic workflows.
>
> Use [LangSmith](https://docs.langchain.com/langsmith/observability.md) to trace, debug, and evaluate agents built with any of these frameworks. Follow the [tracing quickstart](https://docs.langchain.com/langsmith/trace-with-langchain.md) to get set up. We recommend you also set up [LangSmith Engine](https://docs.langchain.com/langsmith/engine.md) which monitors your traces, detects issues, and proposes fixes.

## &#x20;Create an agent

This example demonstrates how to create a simple LangChain agent with a custom tool:

```python OpenAI
# pip install -qU langchain "langchain[openai]"
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="openai:gpt-6.1-sol",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
print(result["messages"][-1].content_blocks)
```

```python Google Gemini
# pip install -qU langchain "langchain[google-genai]"
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="google_genai:gemini-2.5-flash-lite",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
print(result["messages"][-1].content_blocks)
```

```python Claude (Anthropic)
# pip install -qU langchain "langchain[anthropic]"
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="claude-sonnet-4-6",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
print(result["messages"][-1].content_blocks)
```

```python OpenRouter
# pip install -qU langchain langchain-openrouter
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="openrouter:anthropic/claude-sonnet-4-6",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
print(result["messages"][-1].content_blocks)
```

```python Fireworks
# pip install -qU langchain langchain-fireworks
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="fireworks:accounts/fireworks/models/qwen3p5-397b-a17b",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
print(result["messages"][-1].content_blocks)
```

```python Baseten
# pip install -qU langchain langchain-baseten
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="baseten:zai-org/GLM-5.2",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
print(result["messages"][-1].content_blocks)
```

```python Ollama
# pip install -qU langchain langchain-ollama
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="ollama:devstral-2",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
print(result["messages"][-1].content_blocks)
```

```python Azure
# pip install -qU langchain "langchain[openai]"
import os
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

model = init_chat_model(
    "azure_openai:gpt-6.1-sol",
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
)
agent = create_agent(
    model=model,
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
print(result["messages"][-1].content_blocks)
```

```python AWS Bedrock
# pip install -qU langchain langchain-aws
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

# US cross-region inference profile; use global.anthropic.claude-sonnet-4-6 for worldwide routing.
agent = create_agent(
    model="bedrock_converse:us.anthropic.claude-sonnet-4-6",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
print(result["messages"][-1].content_blocks)
```

```python HuggingFace
# pip install -qU langchain "langchain[huggingface]"
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="huggingface:microsoft/Phi-3-mini-4k-instruct",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
print(result["messages"][-1].content_blocks)
```

See the [Installation instructions](../Get%20started/Install%20LangChain.md) and [Quickstart guide](../Get%20started/Quickstart.md) to get started building your own agents and applications with LangChain.

> [!TIP]
>
> Use [LangSmith](https://docs.langchain.com/langsmith/observability.md) to trace requests, debug agent behavior, and evaluate outputs. Set `LANGSMITH_TRACING=true` and your API key to get started.

## &#x20;Core benefits

> [card] [Standard model interface](../Core%20components/Models.md)
>
> Use one interface for chat models, embeddings, and more across providers. Switch models with minimal code changes and keep your application portable as requirements evolve.

> [card] [Highly configurable harness](../Core%20components/Agents.md)
>
> Start with `create_agent` as a minimal harness and add capabilities incrementally through middleware. Compose only what your use case needs, from guardrails and retries to routing and custom tool policies.

> [card] [Built on top of LangGraph](https://docs.langchain.com/oss/python/langgraph/overview.md)
>
> LangChain's agents are built on top of LangGraph. This allows us to take advantage of LangGraph's durable execution, human-in-the-loop support, persistence, and more.

> [card] [Debug with LangSmith](https://docs.langchain.com/langsmith/observability.md)
>
> Inspect traces, tool calls, state transitions, and latency in one place. Find failure modes, evaluate quality, and improve agent behavior with execution data.

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/overview.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

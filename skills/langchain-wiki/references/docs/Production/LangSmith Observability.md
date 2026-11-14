# LangSmith Observability

As you build and run agents with LangChain, you need visibility into how they behave: which [tools](../Core%20components/Tools.md) they call, what prompts they generate, and how they make decisions. LangChain agents built with [`create_agent`](https://reference.langchain.com/python/langchain/agents/factory/create_agent) automatically support tracing through [LangSmith](https://docs.langchain.com/langsmith/observability.md), a platform for capturing, debugging, evaluating, and monitoring agent behavior.

[*Traces*](https://docs.langchain.com/langsmith/observability-concepts.md#traces) record every step of your agent's execution, from the initial user input to the final response, including all tool calls, model interactions, and decision points. This execution data helps you debug issues, evaluate performance across different inputs, and monitor usage patterns in production.

This guide shows you how to enable tracing for your LangChain agents and use LangSmith to analyze their execution.

## Prerequisites

Before you begin, ensure you have the following:

* **A LangSmith account**: Sign up (for free) or log in at [smith.langchain.com](https://smith.langchain.com?utm_source=docs\&utm_medium=cta\&utm_campaign=langsmith-signup\&utm_content=oss-langchain-observability).
* **A LangSmith API key**: Follow the [Create an API key](https://docs.langchain.com/langsmith/create-account-api-key.md) guide.

## Enable tracing

> [!NOTE]
>
> In an [agent-based workspace](https://docs.langchain.com/langsmith/agent-registry.md), [create an agent](https://docs.langchain.com/langsmith/create-an-agent.md) once before sending traces. Use [agent addressing](https://docs.langchain.com/langsmith/log-traces-to-agent.md) to select its identifier and environment. If an integration requires `project_name`, use the selected environment's [`tracer_session_name`](https://docs.langchain.com/langsmith/create-an-agent#use-an-environment-project) as a compatibility value.

All LangChain agents automatically support LangSmith tracing. To enable it, set the following environment variables:

```bash
export LANGSMITH_AGENT_ID="<your-agent-id>"
export LANGSMITH_AGENT_ENVIRONMENT="local"
export LANGSMITH_TRACING=true
export LANGSMITH_API_KEY=<your-api-key>
```

## Quickstart

No extra code is needed to log a trace to LangSmith. Just run your agent code as you normally would:

```python
from langchain.agents import create_agent


def send_email(to: str, subject: str, body: str):
    """Send an email to a recipient."""
    # ... email sending logic
    return f"Email sent to {to}"

def search_web(query: str):
    """Search the web for information."""
    # ... web search logic
    return f"Search results for: {query}"

agent = create_agent(
    model="gpt-6.1-sol",
    tools=[send_email, search_web],
    system_prompt="You are a helpful assistant that can send emails and search the web."
)

# Run the agent - all steps will be traced automatically
response = agent.invoke({
    "messages": [{"role": "user", "content": "Search for the latest AI news and email a summary to john@example.com"}]
})
```

Traces appear in the destination configured during setup.

## Trace selectively

You may opt to trace specific invocations or parts of your agent using LangSmith's `tracing_context` context manager:

```python
import langsmith as ls

# This WILL be traced
with ls.tracing_context(enabled=True):
    agent.invoke({"messages": [{"role": "user", "content": "Send a test email to alice@example.com"}]})

# This will NOT be traced (if LANGSMITH_TRACING is not set)
agent.invoke({"messages": [{"role": "user", "content": "Send another email"}]})
```

## Select an agent and environment

Use `LANGSMITH_AGENT_ID` and `LANGSMITH_AGENT_ENVIRONMENT` to select the registered agent and environment. For per-request routing, pass an agent address in code. See [Log traces to an agent](https://docs.langchain.com/langsmith/log-traces-to-agent.md).

> [accordion] Project-based workspaces and self-hosted LangSmith
>
> Set `LANGSMITH_PROJECT` to the tracing project name instead of setting the agent variables. For integrations that require `project_name` in an agent-based workspace, use the environment's [`tracer_session_name`](https://docs.langchain.com/langsmith/create-an-agent#use-an-environment-project) as a compatibility value.

## Add metadata to traces

You can annotate your traces with custom metadata and tags:

```python
response = agent.invoke(
    {"messages": [{"role": "user", "content": "Send a welcome email"}]},
    config={
        "tags": ["production", "email-assistant", "v1.0"],
        "metadata": {
            "user_id": "user_123",
            "session_id": "session_456",
            "environment": "production"
        }
    }
)
```

`tracing_context` also accepts tags and metadata for fine-grained control:

```python
with ls.tracing_context(
    enabled=True,
    tags=["production", "email-assistant", "v1.0"],
    metadata={"user_id": "user_123", "session_id": "session_456", "environment": "production"}):
    response = agent.invoke(
        {"messages": [{"role": "user", "content": "Send a welcome email"}]}
    )
```

This custom metadata and tags will be attached to the trace in LangSmith.

> [!TIP]
>
> To learn more about how to use traces to debug, evaluate, and monitor your agents, see the [LangSmith documentation](https://docs.langchain.com/langsmith/observability.md).

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/observability.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

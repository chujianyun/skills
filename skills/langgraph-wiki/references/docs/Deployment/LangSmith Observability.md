# LangSmith Observability

Traces are a series of steps that your agent takes to go from input to output. Each of these individual steps is represented by a run. You can use [LangSmith](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=oss-langgraph-observability) to visualize these execution steps. To use it, [enable tracing for your agent](https://docs.langchain.com/langsmith/trace-with-langgraph.md). This enables you to do the following:

* [Debug a locally running agent](https://docs.langchain.com/langsmith/observability-studio.md#debug-langsmith-traces).
* [Evaluate the agent performance](https://docs.langchain.com/oss/python/langchain/test/evals.md).
* [Monitor the agent](https://docs.langchain.com/langsmith/dashboards.md).

## Prerequisites

Before you begin, ensure you have the following:

* **A LangSmith account**: Sign up (for free) or log in at [smith.langchain.com](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=oss-langgraph-observability).
* **A LangSmith API key**: Follow the [Create an API key](https://docs.langchain.com/langsmith/create-account-api-key.md) guide.

## Enable tracing

> [!NOTE]
>
> In an [agent-based workspace](https://docs.langchain.com/langsmith/agent-registry.md), [create an agent](https://docs.langchain.com/langsmith/create-an-agent.md) once before sending traces. Use [agent addressing](https://docs.langchain.com/langsmith/log-traces-to-agent.md) to select its identifier and environment. If an integration requires `project_name`, use the selected environment's [`tracer_session_name`](https://docs.langchain.com/langsmith/create-an-agent#use-an-environment-project) as a compatibility value.

To enable tracing for your agent, set the following environment variables:

```bash
export LANGSMITH_AGENT_ID="<your-agent-id>"
export LANGSMITH_AGENT_ENVIRONMENT="local"
export LANGSMITH_TRACING=true
export LANGSMITH_API_KEY=<your-api-key>
```

Traces appear in the destination configured during setup.

For more information, see [Trace with LangGraph](https://docs.langchain.com/langsmith/trace-with-langgraph.md).

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

## Use anonymizers to prevent logging of sensitive data in traces

You may want to mask sensitive data to prevent it from being logged to LangSmith. You can create [anonymizers](https://docs.langchain.com/langsmith/mask-inputs-outputs.md#rule-based-masking-of-inputs-and-outputs) and apply them to
your graph using configuration. This example will redact anything matching the Social Security Number format XXX-XX-XXXX from traces sent to LangSmith.

```python Python
from langchain_core.tracers.langchain import LangChainTracer
from langgraph.graph import StateGraph, MessagesState
from langsmith import Client
from langsmith.anonymizer import create_anonymizer

anonymizer = create_anonymizer([
    # Matches SSNs
    { "pattern": r"\b\d{3}-?\d{2}-?\d{4}\b", "replace": "<ssn>" }
])

tracer_client = Client(anonymizer=anonymizer)
tracer = LangChainTracer(client=tracer_client)
# Define the graph
graph = (
    StateGraph(MessagesState)
    ...
    .compile()
    .with_config({'callbacks': [tracer]})
)
```

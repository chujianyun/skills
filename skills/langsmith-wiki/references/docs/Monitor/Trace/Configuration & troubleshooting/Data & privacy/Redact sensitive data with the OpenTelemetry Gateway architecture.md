# Redact sensitive data with the OpenTelemetry Gateway architecture

> Use an OpenTelemetry collector to redact sensitive data from traces before they land in LangSmith.

Agents built with [LangChain](../../Tracing%20setup/Integrations/Agent%20frameworks/Trace%20LangChain%20agents%20%28Python%20and%20JS-TS%29.md), [LangGraph](../../Tracing%20setup/Integrations/Agent%20frameworks/Trace%20LangGraph%20agents.md), or [Deep Agents](../../Tracing%20setup/Integrations/Agent%20frameworks/Trace%20Deep%20Agents.md) support [OpenTelemetry-based tracing](../../Tracing%20setup/Integrations/Agent%20frameworks/Trace%20with%20OpenTelemetry.md). Instead of sending traces directly to LangSmith, you can route them through an OpenTelemetry collector you control, apply redaction rules to strip sensitive fields, and forward the sanitized traces to LangSmith.

Traces flow from your agent to the collector over OTLP/HTTP. The collector runs a transform processor that redacts sensitive span attributes, such as prompt inputs and model completions, before forwarding the sanitized spans to the LangSmith API.

You can send traces to the collector in two ways: [through the LangChain, LangGraph, or Deep Agents integration](#trace-with-langchain-langgraph-or-deep-agents), or by [configuring the OpenTelemetry SDK directly](#trace-with-the-opentelemetry-sdk-directly).

```mermaid
flowchart TD
    A["Agent code<br/>(LangChain / LangGraph / Deep Agents)"]

    subgraph collector[":4318"]
        B["Receiver<br/>OTLP/HTTP"]
        C["Transform Processor<br/>PII Redaction<br/>(email, phone, SSN, CC)"]
        D["OTLP/HTTP Exporter"]
        B --> C --> D
    end

    E["LangSmith API<br/>api.smith.langchain.com"]

    A -->|"OTLP/HTTP"| B
    D -->|"OTLP/HTTP"| E
```

> [!NOTE]
>
> In an [agent-based workspace](../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20Registry.md), [create an agent](../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md) once before sending traces. Use [agent addressing](../Agent%20%26%20environment%20settings/Log%20traces%20to%20an%20agent.md) to select its identifier and environment. If an integration requires `project_name`, use the selected environment's [`tracer_session_name`](../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md#use-an-environment-project) as a compatibility value.

## Prerequisites

Both approaches require the following environment variables. Set `OTEL_EXPORTER_OTLP_ENDPOINT` to the address of your collector:

```bash
LANGSMITH_OTEL_ENABLED="true"
LANGSMITH_TRACING="true"
LANGSMITH_OTEL_ONLY="true"
LANGSMITH_AGENT_ID="<your-agent-id>"
LANGSMITH_AGENT_ENVIRONMENT="production"
OTEL_EXPORTER_OTLP_ENDPOINT="http://<my-otel-collector-endpoint>:4318"
```

`LANGSMITH_AGENT_ID` and `LANGSMITH_AGENT_ENVIRONMENT` name the agent and environment the traces belong to. For more information, see [Log traces to an agent](../Agent%20%26%20environment%20settings/Log%20traces%20to%20an%20agent.md).

## Configure the collector

Both approaches also require an OpenTelemetry collector running as an intermediary between your agent and LangSmith. The following configuration sets up an OTLP receiver on port `4318`, a transform processor that redacts the `gen_ai.prompt` and `gen_ai.completion` span attributes, and an exporter that forwards the sanitized traces to the LangSmith API:

```yaml
receivers:
  otlp:
    protocols:
      http:
        endpoint: 0.0.0.0:4318


processors:
  transform/redact:
    error_mode: ignore
    trace_statements:
      - context: span
        statements:
          - replace_pattern(attributes["gen_ai.completion"], "[\\s\\S]*", "[REDACTED]")
          - replace_pattern(attributes["gen_ai.prompt"], "[\\s\\S]*", "[REDACTED]")

exporters:
  otlphttp/langsmith:
    traces_endpoint: "https://api.smith.langchain.com/otel/v1/traces"
    headers:
      x-api-key: "<SECRET>"
      Langsmith-Agent-Id: "${env:LANGSMITH_AGENT_ID}"
      Langsmith-Agent-Environment: "${env:LANGSMITH_AGENT_ENVIRONMENT}"
      x-Tenant-Id: "${env:LANGSMITH_TENANT_ID}" # Required if API key is not scoped to a specific workspace


service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [transform/redact]
      exporters: [otlphttp/langsmith]
```

The collector reads `LANGSMITH_API_KEY`, `LANGSMITH_AGENT_ID`, and `LANGSMITH_AGENT_ENVIRONMENT` from its own environment, not from your application's. Set them where the collector runs, along with `LANGSMITH_TENANT_ID` if your API key is not scoped to a specific workspace.

### Send traces to an agent

The collector, not your application, decides which agent and environment receive the traces. The collector sends its own headers to LangSmith and does not forward the headers your application sends by default. The `otlphttp/langsmith` exporter in the preceding configuration sets both agent headers:

* **`Langsmith-Agent-Id`**: The identifier of the agent. It must be 1 to 63 lowercase letters, digits, or hyphens, start with a letter, and end with a letter or digit.
* **`Langsmith-Agent-Environment`**: The environment the traces belong to. One of `local`, `development`, `staging`, or `production`.

Send both agent headers or neither. LangSmith rejects a request that sets one without the other, or that sets either alongside `Langsmith-Project`, with a `400` error.

The headers apply to every span the exporter sends. To send traces to more than one agent or environment, define one exporter for each, and route each agent's spans to its exporter. Span attributes, including `gen_ai.agent.name`, do not send traces to an agent. To learn more about sending traces to an agent, see [Log traces to an agent](../Agent%20%26%20environment%20settings/Log%20traces%20to%20an%20agent.md).

## Trace with LangChain, LangGraph, or Deep Agents

Use this approach if your agent already uses [LangChain](../../Tracing%20setup/Integrations/Agent%20frameworks/Trace%20LangChain%20agents%20%28Python%20and%20JS-TS%29.md), [LangGraph](../../Tracing%20setup/Integrations/Agent%20frameworks/Trace%20LangGraph%20agents.md), or [Deep Agents](../../Tracing%20setup/Integrations/Agent%20frameworks/Trace%20Deep%20Agents.md). The tracing integration handles span creation automatically based on your environment variables, so no additional instrumentation code is required:

```python
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI


@tool
def tell_joke(topic: str) -> str:
   llm = ChatOpenAI()
   response = llm.invoke(f"Tell me a short, funny joke about {topic}.")
   return response.content


agent = create_agent(
   model=ChatOpenAI(),
   tools=[tell_joke],
   system_prompt="When the user asks for jokes, use the tell_joke tool for each topic.",
)


topics = ["programming", "python", "kubernetes", "machine learning"]


result = agent.invoke(
   {"messages": [{"role": "user", "content": f"Tell me jokes about these topics: {', '.join(topics)}"}]}
)


print(result["messages"][-1].content)
```

## Trace with the OpenTelemetry SDK directly

Use this approach if you need programmatic control over the tracer provider and exporter, such as which span processors run or where the exporter sends spans. You configure the provider explicitly in code rather than relying on environment variables alone. The collector's exporter, not your code, decides which agent receives the traces:

```python
import os

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


otlp_endpoint = os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"]


provider = TracerProvider()
provider.add_span_processor(
   BatchSpanProcessor(
       OTLPSpanExporter(
           endpoint=otlp_endpoint+"/v1/traces",
       )
   )
)
trace.set_tracer_provider(provider)


chain = ChatPromptTemplate.from_template("Tell me a joke about {topic}") | ChatOpenAI()


for topic in ["programming", "python", "databases", "kubernetes", "machine learning"]:
   print(f"Asking about {topic}...")
   result = chain.invoke({"topic": topic})
   print(f"  {result.content[:100]}\n")


provider.force_flush()
provider.shutdown()
```

> [!NOTE]
>
> If you prefer to redact sensitive data without routing through a collector, see [Prevent logging of sensitive data in traces](Prevent%20logging%20of%20sensitive%20data%20in%20traces.md).

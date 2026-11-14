# Write traces to multiple destinations with replicas

> Send every trace to multiple agent environments or workspaces at the same time using replicas, configured by environment variable or at runtime.

Replicas let you send every trace to multiple agent environments or workspaces at the same time. Where [dynamic routing](Conditional%20tracing.md#customize-tracing-configuration-per-request) sends each trace to one destination, replicas duplicate the trace to all configured destinations in parallel.

Use replicas to:

* Mirror production traces into a Staging environment or a personal workspace for debugging.
* Write to multiple workspaces for multi-tenant isolation without changing any agent code.
* Send traces to the same server for different agent environments, with per-replica metadata overrides.

> [!NOTE]
>
> This integration uses a legacy destination setting such as `project_name` or `LANGSMITH_PROJECT`. [Create an agent](../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md), choose its environment, and [retrieve that environment's `tracer_session_name`](../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md#use-an-environment-project). Use that returned value in the destination setting and any overrides. For integrations that support agent addressing, use the [agent identifier and environment](Log%20traces%20to%20an%20agent.md) directly.

Provision every destination before enabling routing, including each replica and tenant workspace. Set each replica's `project_name` or `projectName` to its destination environment's `tracer_session_name`.

## Configure replicas via environment variable

Set the `LANGSMITH_RUNS_ENDPOINTS` environment variable to a JSON value. Two formats are supported:

* **Object format**: maps each endpoint URL to its API key. Each URL appears once, so use the array format when two replicas share a URL:

  ```bash
  export LANGSMITH_RUNS_ENDPOINTS='{
  "https://api.smith.langchain.com": "ls__key_us_workspace",
  "https://eu.api.smith.langchain.com": "ls__key_eu_workspace"
  }'
  ```

* **Array format**: a list of replica objects, useful when you need multiple replicas pointing at the same URL or when you want to set a `project_name` per replica:

  ```bash
  export LANGSMITH_RUNS_ENDPOINTS='[
  {"api_url": "https://api.smith.langchain.com", "api_key": "ls__key1", "project_name": "<production-tracer-session-name>"},
  {"api_url": "https://api.smith.langchain.com", "api_key": "ls__key2", "project_name": "<staging-tracer-session-name>"}
  ]'
  ```

> [!WARNING]
>
> You cannot use `LANGSMITH_RUNS_ENDPOINTS` alongside `LANGSMITH_ENDPOINT`. If you set both, LangSmith raises an error. Use only one to configure your endpoint.

## Configure replicas at runtime

You can also pass replicas directly in code, which is useful when destinations vary per request or tenant.

```python Python
from langsmith import traceable, tracing_context
from langsmith.run_trees import WriteReplica, ApiKeyAuth

@traceable
def my_pipeline(query: str) -> str:
    # Your agent logic here
    return f"Answer to: {query}"

replicas = [
    WriteReplica(
        api_url="https://api.smith.langchain.com",
        auth=ApiKeyAuth(api_key="<SECRET>"),
        project_name="<production-tracer-session-name>",
    ),
    WriteReplica(
        api_url="https://api.smith.langchain.com",
        auth=ApiKeyAuth(api_key="<SECRET>"),
        project_name="<staging-tracer-session-name>",
        # Optionally override fields on the replicated run
        updates={"metadata": {"environment": "staging"}},
    ),
]

with tracing_context(replicas=replicas):
    my_pipeline("What is LangSmith?")
```

```typescript TypeScript
import { traceable } from "langsmith/traceable";

const myPipeline = traceable(
  async (query: string): Promise<string> => {
    // Your agent logic here
    return `Answer to: ${query}`;
  },
  {
    name: "my_pipeline",
    replicas: [
      {
        apiUrl: "https://api.smith.langchain.com",
        apiKey: "<SECRET>",
        projectName: "<production-tracer-session-name>",
      },
      {
        apiUrl: "https://api.smith.langchain.com",
        apiKey: "<SECRET>",
        projectName: "<staging-tracer-session-name>",
        // Optionally override fields on the replicated run
        updates: { metadata: { environment: "staging" } },
      },
    ],
  }
);

await myPipeline("What is LangSmith?");
```

You can also use the `updates` field to merge additional fields (such as [metadata or tags](../../Tracing%20setup/Manual%20instrumentation/Metadata%20parameters%20reference.md)) into a run for a specific replica only, leaving the primary trace unchanged. Replica errors are non-fatal: if a replica endpoint is unavailable, LangSmith logs the error without affecting the primary trace.

> [!WARNING]
>
> Auth does not propagate in distributed traces. When a trace spans multiple services, LangSmith forwards replica `project_name` and `updates` to downstream services automatically, but not API keys or credentials. Each service must configure its own credentials for replica destinations.

## Replicate between environments on the same server

If all your replicas use the same LangSmith server, you can omit `api_url` and `auth` and specify only a `project_name`. The SDK reuses the default client credentials:

```python Python
from langsmith import traceable, tracing_context
from langsmith.run_trees import WriteReplica

@traceable
def my_pipeline(query: str) -> str:
    return f"Answer to: {query}"

with tracing_context(
    replicas=[
        WriteReplica(project_name="<production-tracer-session-name>"),
        WriteReplica(project_name="<staging-tracer-session-name>", updates={"metadata": {"env": "staging"}}),
    ]
):
    my_pipeline("What is LangSmith?")
```

```typescript TypeScript
import { traceable } from "langsmith/traceable";

const myPipeline = traceable(
  async (query: string) => `Answer to: ${query}`,
  {
    name: "my_pipeline",
    replicas: [
      { projectName: "<production-tracer-session-name>" },
      { projectName: "<staging-tracer-session-name>", updates: { metadata: { env: "staging" } } },
    ],
  }
);

await myPipeline("What is LangSmith?");
```

## Leave feedback on all replica instances

When you use replicas, each replica receives a copy of every run. To submit feedback for a run on a specific replica, you need that replica's run ID. In Python SDK 0.10.8 or later and JS SDK 0.8.5 or later, you can designate one replica as the **primary** and use `compute_run_id_for_secondary_replica` to deterministically calculate the run IDs for all other replicas.

The **primary** replica keeps the original run ID unchanged. Each **secondary** replica receives a deterministic run ID derived from the original run ID and the secondary destination's `tracer_session_name`. Use `compute_run_id_for_secondary_replica(original_run_id, project_name)` to compute the secondary run ID and pass it when calling `create_feedback`. Both SDKs raise an error if the run ID is not a UUID v7, or if `project_name` is empty.

```python Python
from langsmith import (
    Client,
    compute_run_id_for_secondary_replica,
    trace,
    tracing_context,
)

primary_client = Client(api_key="primary-key")
secondary_client = Client(api_key="<SECRET>")

primary_project = "<primary-tracer-session-name>"
secondary_project = "<replica-tracer-session-name>"

with tracing_context(
    replicas=[
        {
            "project_name": primary_project,
            "primary": True,
            "client": primary_client,
        },
        {
            "project_name": secondary_project,
            "primary": False,
            "client": secondary_client,
        },
    ]
):
    with trace("answer-question", inputs={"question": "Capital of France?"}) as run:
        run.outputs = {"answer": "Paris"}

# Compute the secondary replica's run ID from the original run ID and project name
secondary_run_id = compute_run_id_for_secondary_replica(
    run.id,
    secondary_project,
)

# Each destination has its own session_id; resolve it for feedback
primary_session_id = primary_client.read_project(project_name=primary_project).id
secondary_session_id = secondary_client.read_project(project_name=secondary_project).id

# Submit feedback to the primary replica using the original run ID
primary_client.create_feedback(
    trace_id=run.id,
    key="user-rating",
    score=1,
    session_id=primary_session_id,
)

# Submit feedback to the secondary replica using the computed run ID
secondary_client.create_feedback(
    trace_id=secondary_run_id,
    key="user-rating",
    score=1,
    session_id=secondary_session_id,
)
```

```typescript TypeScript
import { Client } from "langsmith";
import { traceable, getCurrentRunTree } from "langsmith/traceable";
import { computeRunIdForSecondaryReplica } from "langsmith";

const primaryClient = new Client({ apiKey: "primary-key" });
const secondaryClient = new Client({ apiKey: "<SECRET>" });

const primaryProject = "<primary-tracer-session-name>";
const secondaryProject = "<replica-tracer-session-name>";

let primaryRunId: string | undefined;

const answerQuestion = traceable(
  async (question: string) => {
    primaryRunId = getCurrentRunTree()?.id;
    return { answer: "Paris" };
  },
  {
    name: "answer-question",
    client: primaryClient,
    replicas: [
      {
        projectName: primaryProject,
        primary: true,
        client: primaryClient,
      },
      {
        projectName: secondaryProject,
        primary: false,
        client: secondaryClient,
      },
    ],
  }
);

await answerQuestion("Capital of France?");

if (primaryRunId) {
  // Compute the secondary replica's run ID
  const secondaryRunId = computeRunIdForSecondaryReplica(
    primaryRunId,
    secondaryProject
  );

  // Each destination has its own session_id; resolve it for feedback
  const { id: primarySessionId } = await primaryClient.readProject({
    projectName: primaryProject,
  });
  const { id: secondarySessionId } = await secondaryClient.readProject({
    projectName: secondaryProject,
  });

  // Submit feedback to the primary replica using the original run ID
  await primaryClient.createFeedback({
    runId: primaryRunId,
    sessionId: primarySessionId,
    key: "user-rating",
    score: 1,
  });

  // Submit feedback to the secondary replica using the computed run ID
  await secondaryClient.createFeedback({
    runId: secondaryRunId,
    sessionId: secondarySessionId,
    key: "user-rating",
    score: 1,
  });
}
```

> [!NOTE]
>
> The `compute_run_id_for_secondary_replica` / `computeRunIdForSecondaryReplica` helper is available in Python SDK 0.10.8 or later and JS SDK 0.8.5 or later. If you are using an earlier SDK version, upgrade to use this feature.

## Route between LangSmith and OpenTelemetry destinations

You can decide at runtime whether a given invocation sends traces to LangSmith, to an OpenTelemetry (OTel) backend, or to both, without redeploying or modifying agent logic. This is useful when you want to toggle between observability backends per environment, or even per request, making the decision at runtime.

Set the tracing mode using the `tracing_mode` constructor argument or the `LANGSMITH_TRACING_MODE` environment variable. Both accept the same values; an explicit `tracing_mode` argument always takes precedence over the env var:

* **`"langsmith"` (default)**: sends traces natively to LangSmith.
* **`"otel"`**: exports traces as OpenTelemetry spans to a configured OTel backend.
* **`"hybrid"` (Python only)**: sends to both LangSmith and an OTel backend from a single replica.

> [!NOTE]
>
> If you are using the deprecated `otel_enabled` parameter on `Client` (Python only), migrate to `tracing_mode`: `Client(otel_enabled=True)` → `Client(tracing_mode="hybrid")`. Passing `otel_enabled` still works, but emits a `FutureWarning`.

Pass a configured `Client` directly into a replica to apply the desired mode at runtime:

```python Python expandable wrap
from langsmith import Client, traceable, tracing_context
from langsmith.run_trees import WriteReplica
from langsmith.wrappers import wrap_openai
import openai

# Create clients with different tracing modes
ls_client = Client()                            # tracing_mode="langsmith" (default)
otel_client = Client(tracing_mode="otel")       # tracing_mode="otel"
hybrid_client = Client(tracing_mode="hybrid")   # tracing_mode="hybrid" (both)

openai_client = wrap_openai(openai.Client())

@traceable()
def joke():
    response = openai_client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[{"role": "user", "content": "Tell me a short joke."}],
    )
    return response.choices[0].message.content

# Mix tracing modes across replicas in a single invocation:
# one replica sends via LangSmith's native format, another as OTel spans.
with tracing_context(replicas=[
    WriteReplica(client=ls_client),    # tracing_mode="langsmith"
    WriteReplica(client=otel_client),  # tracing_mode="otel"
]):
    joke()

# Alternatively, a single hybrid replica sends to both simultaneously.
with tracing_context(replicas=[WriteReplica(client=hybrid_client)]):
    joke()

# Swap replica lists at runtime, for example based on a feature flag or environment.
def get_replicas(send_to_otel: bool):
    replicas = [WriteReplica(client=ls_client)]
    if send_to_otel:
        replicas.append(WriteReplica(client=otel_client))
    return replicas

with tracing_context(replicas=get_replicas(send_to_otel=True)):   # LangSmith + OTel
    joke()

with tracing_context(replicas=get_replicas(send_to_otel=False)):  # LangSmith only
    joke()
```

```typescript TypeScript expandable wrap
import { Client } from "langsmith";
import { traceable } from "langsmith/traceable";
import { wrapOpenAI } from "langsmith/wrappers";
import OpenAI from "openai";

// Note: tracingMode: "otel" requires OTel SDK initialization
// (TracerProvider, SpanProcessor, etc.) before creating the client.
// See the OpenTelemetry integration guide for setup details.

// Create clients with different tracing modes
const lsClient = new Client();                           // tracingMode: "langsmith" (default)
const otelClient = new Client({ tracingMode: "otel" });  // tracingMode: "otel"

const openaiClient = wrapOpenAI(new OpenAI());

async function jokeImpl() {
  const response = await openaiClient.chat.completions.create({
    model: "gpt-5.4-mini",
    messages: [{ role: "user", content: "Tell me a short joke." }],
  });
  return response.choices[0].message.content;
}

// Mix tracing modes across replicas in a single traceable call:
// the primary client sends via LangSmith, the replica sends as OTel spans.
const joke = traceable(jokeImpl, {
  name: "joke",
  client: lsClient,                    // tracingMode: "langsmith" (default)
  replicas: [{ client: otelClient }],  // tracingMode: "otel"
});
await joke();

// Build replicas dynamically for runtime switching, for example based on a feature flag.
function buildReplicas(sendToOtel: boolean) {
  return sendToOtel ? [{ client: otelClient }] : [];
}

const sendToOtel = process.env.ROUTE_TO_OTEL === "true";
const jokeDynamic = traceable(jokeImpl, {
  name: "joke",
  client: lsClient,
  replicas: buildReplicas(sendToOtel),
});
await jokeDynamic();
```

The `tracing_mode` on each `Client` determines that replica's export path. In Python, `"hybrid"` mode handles both destinations within a single replica. In TypeScript, the "send to both" case uses two separate replicas, one for each client, because there is no `"hybrid"` mode. Since each replica resolves its own client independently, you can also mix modes within a single `tracing_context`, for example keeping one replica sending to LangSmith while forwarding the same trace to an OTel collector via a second replica.

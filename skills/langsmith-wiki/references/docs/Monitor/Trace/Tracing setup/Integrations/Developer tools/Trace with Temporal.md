# Trace with Temporal

> Learn how to trace Temporal workflows and activities in LangSmith using OpenTelemetry.

[Temporal](https://temporal.io/) is a durable execution platform that enables developers to build resilient distributed workflows. This guide shows you how to trace Temporal workflows and activities in LangSmith using OpenTelemetry.

LangSmith supports OpenTelemetry (OTEL) trace ingestion, which integrates seamlessly with Temporal's native OpenTelemetry interceptors. This enables full distributed tracing across your workflow executions, activities, and any LLM calls within them.

> [!NOTE]
>
> In an [agent-based workspace](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20Registry.md), [create an agent](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md) once before sending traces. Use [agent addressing](../../../Configuration%20%26%20troubleshooting/Agent%20%26%20environment%20settings/Log%20traces%20to%20an%20agent.md) to select its identifier and environment. If an integration requires `project_name`, use the selected environment's [`tracer_session_name`](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md#use-an-environment-project) as a compatibility value.

## Prerequisites

* A [LangSmith account](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-trace-with-temporal) and API key
* Temporal server running (local or cloud)
* OpenTelemetry SDK for your language

## Environment variables

Set the following environment variables for all implementations:

| Variable | Required | Description |
| - | - | - |
| `LANGSMITH_API_KEY` | Yes | Your LangSmith API key from Settings. |
| `LANGSMITH_AGENT_ID` | Yes, for Python and TypeScript | Registered agent identifier. |
| `LANGSMITH_AGENT_ENVIRONMENT` | Yes, for Python and TypeScript | Agent environment, such as `local`. |

> [!NOTE]
>
> For regional SaaS or self-hosted LangSmith installations, also set `LANGCHAIN_BASE_URL` to your LangSmith instance URL.

## Set up tracing

> [tab] Go
>
> This Go example uses the `langsmith-go` SDK with Temporal's OpenTelemetry interceptors to trace workflows and activities. It uses project-based configuration: set `LANGSMITH_PROJECT` to the [environment's `tracer_session_name`](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md#use-an-environment-project), without the two agent variables. The Python and TypeScript exporters use agent-addressing headers.
>
> **1. Install**
>
> Install the LangSmith Go SDK, Temporal SDK, and OpenTelemetry interceptor:
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> go get github.com/langchain-ai/langsmith-go@v0.1.0-alpha.7
> go get go.temporal.io/sdk
> go get go.temporal.io/sdk/contrib/opentelemetry
> ```
>
> **2. Initialize tracer**
>
> Initialize the LangSmith tracer, create Temporal's OpenTelemetry interceptor, and register it with the Temporal client and worker:
>
> ```go theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> package main
>
> import (
> 	"context"
> 	"log"
>
> 	"github.com/langchain-ai/langsmith-go"
> 	"go.temporal.io/sdk/client"
> 	"go.temporal.io/sdk/contrib/opentelemetry"
> 	"go.temporal.io/sdk/interceptor"
> 	"go.temporal.io/sdk/worker"
> )
>
> func main() {
> 	ctx := context.Background()
>
> 	// Initialize LangSmith tracer (reads LANGSMITH_API_KEY and LANGSMITH_PROJECT)
> 	ls, err := langsmith.NewTracer(
> 		langsmith.WithServiceName("temporal-worker"),
> 	)
> 	if err != nil {
> 		log.Fatal("Failed to initialize LangSmith tracer:", err)
> 	}
> 	defer ls.Shutdown(ctx)
>
> 	// Create Temporal tracing interceptor
> 	tracer := ls.Tracer("temporal-app")
> 	tracingInterceptor, err := opentelemetry.NewTracingInterceptor(
> 		opentelemetry.TracerOptions{Tracer: tracer},
> 	)
> 	if err != nil {
> 		log.Fatal("Failed to create tracing interceptor:", err)
> 	}
>
> 	// Create Temporal client with tracing
> 	c, err := client.Dial(client.Options{
> 		Interceptors: []interceptor.ClientInterceptor{tracingInterceptor},
> 	})
> 	if err != nil {
> 		log.Fatal("Failed to create Temporal client:", err)
> 	}
> 	defer c.Close()
>
> 	// Create worker with tracing (uses same client)
> 	w := worker.New(c, "my-task-queue", worker.Options{})
> 	w.RegisterWorkflow(MyWorkflow)
> 	w.RegisterActivity(MyActivity)
>
> 	// Start worker
> 	if err := w.Run(worker.InterruptCh()); err != nil {
> 		log.Fatal("Worker failed:", err)
> 	}
> }
> ```
>
> **3. Define workflow and activity**
>
> Define a workflow that executes an activity. The activity demonstrates how to add custom span attributes for LangSmith visibility:
>
> ```go theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> package main
>
> import (
> 	"context"
> 	"fmt"
> 	"time"
>
> 	"go.opentelemetry.io/otel/attribute"
> 	"go.opentelemetry.io/otel/trace"
> 	"go.temporal.io/sdk/activity"
> 	"go.temporal.io/sdk/workflow"
> )
>
> // MyWorkflow executes an activity
> func MyWorkflow(ctx workflow.Context, input string) (string, error) {
> 	ao := workflow.ActivityOptions{
> 		StartToCloseTimeout: 10 * time.Second,
> 	}
> 	ctx = workflow.WithActivityOptions(ctx, ao)
>
> 	var result string
> 	err := workflow.ExecuteActivity(ctx, MyActivity, input).Get(ctx, &result)
> 	return result, err
> }
>
> // MyActivity processes input with custom span attributes
> func MyActivity(ctx context.Context, input string) (string, error) {
> 	logger := activity.GetLogger(ctx)
> 	logger.Info("Processing", "input", input)
>
> 	// Get the span created by Temporal's interceptor
> 	span := trace.SpanFromContext(ctx)
>
> 	// Add Gen AI attributes for LangSmith visibility
> 	span.SetAttributes(
> 		attribute.String("gen_ai.prompt", input),
> 		attribute.String("gen_ai.operation.name", "chat"),
> 	)
>
> 	result := fmt.Sprintf("Processed: %s", input)
>
> 	// Set completion attribute
> 	span.SetAttributes(
> 		attribute.String("gen_ai.completion", result),
> 	)
>
> 	return result, nil
> }
> ```
>
> **4. Execute workflow**
>
> In a separate client process, initialize the tracer and execute the workflow:
>
> ```go client.go theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> // In a separate function or client code
> func executeWorkflow() {
> 	ctx := context.Background()
>
> 	// Initialize tracer for client
> 	ls, err := langsmith.NewTracer(
> 		langsmith.WithServiceName("temporal-client"),
> 	)
> 	if err != nil {
> 		log.Fatal(err)
> 	}
> 	defer ls.Shutdown(ctx)
>
> 	// Create client with tracing
> 	tracer := ls.Tracer("temporal-app")
> 	tracingInterceptor, err := opentelemetry.NewTracingInterceptor(
> 		opentelemetry.TracerOptions{Tracer: tracer},
> 	)
> 	if err != nil {
> 		log.Fatal(err)
> 	}
>
> 	c, err := client.Dial(client.Options{
> 		Interceptors: []interceptor.ClientInterceptor{tracingInterceptor},
> 	})
> 	if err != nil {
> 		log.Fatal(err)
> 	}
> 	defer c.Close()
>
> 	// Execute workflow
> 	workflowOptions := client.StartWorkflowOptions{
> 		ID:        "my-workflow-1",
> 		TaskQueue: "my-task-queue",
> 	}
>
> 	we, err := c.ExecuteWorkflow(ctx, workflowOptions, MyWorkflow, "Hello World")
> 	if err != nil {
> 		log.Fatal(err)
> 	}
>
> 	var result string
> 	if err := we.Get(ctx, &result); err != nil {
> 		log.Fatal(err)
> 	}
>
> 	log.Printf("Workflow result: %s", result)
> }
> ```

> [tab] Python
>
> Python uses the `temporalio` SDK with OpenTelemetry interceptors, exporting traces to LangSmith via OTLP.
>
> **1. Install**
>
> Install the Temporal SDK, LangSmith SDK, and OpenTelemetry packages:
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> pip install temporalio
> pip install langsmith
> pip install opentelemetry-sdk
> pip install opentelemetry-exporter-otlp-proto-http
> ```
>
> **2. Initialize tracer**
>
> Create an OpenTelemetry `TracerProvider` with an OTLP exporter configured to send traces to LangSmith:
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import asyncio
> import os
> from datetime import timedelta
>
> from opentelemetry import trace
> from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
> from opentelemetry.sdk.resources import Resource, SERVICE_NAME
> from opentelemetry.sdk.trace import TracerProvider
> from opentelemetry.sdk.trace.export import BatchSpanProcessor
>
> from temporalio import activity, workflow
> from temporalio.client import Client
> from temporalio.contrib.opentelemetry import TracingInterceptor
> from temporalio.worker import Worker
>
>
> def init_tracer_provider() -> TracerProvider:
>     """Initialize OpenTelemetry with LangSmith exporter."""
>
>     # Create OTLP exporter for LangSmith
>     exporter = OTLPSpanExporter(
>         endpoint="https://api.smith.langchain.com/otel/v1/traces",
>         headers={
>             "x-api-key": os.environ.get("LANGSMITH_API_KEY", ""),
>             "Langsmith-Agent-Id": os.environ["LANGSMITH_AGENT_ID"],
>             "Langsmith-Agent-Environment": os.environ["LANGSMITH_AGENT_ENVIRONMENT"],
>         },
>     )
>
>     # Create TracerProvider with resource attributes
>     resource = Resource.create({
>         SERVICE_NAME: "temporal-worker",
>     })
>
>     provider = TracerProvider(resource=resource)
>     provider.add_span_processor(BatchSpanProcessor(exporter))
>
>     # Set as global provider
>     trace.set_tracer_provider(provider)
>
>     return provider
> ```
>
> **3. Define workflow and activity**
>
> Define a workflow class and activity function. The activity demonstrates how to add custom span attributes for LangSmith visibility:
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> @activity.defn
> async def process_activity(input: str) -> str:
>     """Activity that processes input with custom span attributes."""
>     activity.logger.info(f"Processing: {input}")
>
>     # Get current span and add Gen AI attributes
>     span = trace.get_current_span()
>     span.set_attribute("gen_ai.prompt", input)
>     span.set_attribute("gen_ai.operation.name", "chat")
>
>     result = f"Processed: {input}"
>
>     span.set_attribute("gen_ai.completion", result)
>
>     return result
>
>
> @workflow.defn
> class MyWorkflow:
>     @workflow.run
>     async def run(self, input: str) -> str:
>         return await workflow.execute_activity(
>             process_activity,
>             input,
>             start_to_close_timeout=timedelta(seconds=10),
>         )
> ```
>
> **4. Run worker**
>
> Create a Temporal client with the `TracingInterceptor` and start the worker:
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> async def main():
>     # Initialize tracing
>     provider = init_tracer_provider()
>
>     try:
>         # Create Temporal client with tracing interceptor
>         client = await Client.connect(
>             "localhost:7233",
>             interceptors=[TracingInterceptor()],
>         )
>
>         # Run worker
>         worker = Worker(
>             client,
>             task_queue="my-task-queue",
>             workflows=[MyWorkflow],
>             activities=[process_activity],
>         )
>
>         print("Starting worker...")
>         await worker.run()
>
>     finally:
>         # Shutdown tracer provider to flush traces
>         provider.shutdown()
>
>
> if __name__ == "__main__":
>     asyncio.run(main())
> ```
>
> **5. Execute workflow**
>
> In a separate script, connect to Temporal with the tracing interceptor and execute the workflow:
>
> ```python client.py theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import asyncio
> from temporalio.client import Client
> from temporalio.contrib.opentelemetry import TracingInterceptor
>
> # Import the same tracer setup
> from worker import init_tracer_provider
>
>
> async def main():
>     provider = init_tracer_provider()
>
>     try:
>         client = await Client.connect(
>             "localhost:7233",
>             interceptors=[TracingInterceptor()],
>         )
>
>         # Execute workflow
>         result = await client.execute_workflow(
>             MyWorkflow.run,
>             "Hello World",
>             id="my-workflow-1",
>             task_queue="my-task-queue",
>         )
>         print(f"Workflow result: {result}")
>
>     finally:
>         provider.shutdown()
>
>
> if __name__ == "__main__":
>     asyncio.run(main())
> ```

> [tab] TypeScript / JavaScript
>
> TypeScript uses the `@temporalio/sdk` with OpenTelemetry interceptors to send traces to LangSmith.
>
> **1. Install**
>
> Install the Temporal SDK, OpenTelemetry interceptors, and tracing packages:
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> npm install @temporalio/client @temporalio/worker @temporalio/activity @temporalio/workflow
> npm install @temporalio/interceptors-opentelemetry
> npm install @opentelemetry/sdk-node @opentelemetry/sdk-trace-node
> npm install @opentelemetry/exporter-trace-otlp-http
> npm install @opentelemetry/resources @opentelemetry/semantic-conventions
> ```
>
> **2. Initialize tracer**
>
> Create a `NodeTracerProvider` with an OTLP exporter configured to send traces to LangSmith:
>
> ```typescript tracer.ts theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { Resource } from '@opentelemetry/resources';
> import { ATTR_SERVICE_NAME } from '@opentelemetry/semantic-conventions';
> import { NodeTracerProvider } from '@opentelemetry/sdk-trace-node';
> import { BatchSpanProcessor } from '@opentelemetry/sdk-trace-base';
> import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';
>
> export function initTracerProvider(): NodeTracerProvider {
>   // Create OTLP exporter for LangSmith
>   const exporter = new OTLPTraceExporter({
>     url: 'https://api.smith.langchain.com/otel/v1/traces',
>     headers: {
>       'x-api-key': process.env.LANGSMITH_API_KEY || '',
>       'Langsmith-Agent-Id': process.env.LANGSMITH_AGENT_ID!,
>       'Langsmith-Agent-Environment': process.env.LANGSMITH_AGENT_ENVIRONMENT!,
>     },
>   });
>
>   // Create TracerProvider
>   const provider = new NodeTracerProvider({
>     resource: new Resource({
>       [ATTR_SERVICE_NAME]: 'temporal-worker',
>     }),
>   });
>
>   provider.addSpanProcessor(new BatchSpanProcessor(exporter));
>   provider.register();
>
>   return provider;
> }
> ```
>
> **3. Define workflow**
>
> Define a workflow that proxies activities with a timeout configuration:
>
> ```typescript workflows.ts theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { proxyActivities } from '@temporalio/workflow';
> import type * as activities from './activities';
>
> const { processActivity } = proxyActivities<typeof activities>({
>   startToCloseTimeout: '10 seconds',
> });
>
> export async function myWorkflow(input: string): Promise<string> {
>   return await processActivity(input);
> }
> ```
>
> **4. Define activity**
>
> Define an activity that demonstrates how to add custom span attributes for LangSmith visibility:
>
> ```typescript activities.ts theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { log } from '@temporalio/activity';
> import { trace } from '@opentelemetry/api';
>
> export async function processActivity(input: string): Promise<string> {
>   log.info('Processing', { input });
>
>   // Get current span and add Gen AI attributes
>   const span = trace.getActiveSpan();
>   span?.setAttribute('gen_ai.prompt', input);
>   span?.setAttribute('gen_ai.operation.name', 'chat');
>
>   const result = `Processed: ${input}`;
>
>   span?.setAttribute('gen_ai.completion', result);
>
>   return result;
> }
> ```
>
> **5. Run worker**
>
> Create a worker with OpenTelemetry interceptors for activities and a workflow exporter for workflow spans:
>
> ```typescript worker.ts theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { Worker, NativeConnection } from '@temporalio/worker';
> import { Resource } from '@opentelemetry/resources';
> import { ATTR_SERVICE_NAME } from '@opentelemetry/semantic-conventions';
> import {
>   makeWorkflowExporter,
>   OpenTelemetryActivityInboundInterceptor,
> } from '@temporalio/interceptors-opentelemetry';
> import { trace } from '@opentelemetry/api';
>
> import * as activities from './activities';
> import { initTracerProvider } from './tracer';
>
> async function run() {
>   const provider = initTracerProvider();
>
>   try {
>     const connection = await NativeConnection.connect({
>       address: 'localhost:7233',
>     });
>
>     const worker = await Worker.create({
>       connection,
>       namespace: 'default',
>       taskQueue: 'my-task-queue',
>       workflowsPath: require.resolve('./workflows'),
>       activities,
>       sinks: {
>         exporter: makeWorkflowExporter(
>           trace.getTracer('temporal-app'),
>           new Resource({ [ATTR_SERVICE_NAME]: 'temporal-worker' })
>         ),
>       },
>       interceptors: {
>         activity: [() => ({ inbound: new OpenTelemetryActivityInboundInterceptor() })],
>       },
>     });
>
>     console.log('Starting worker...');
>     await worker.run();
>   } finally {
>     await provider.shutdown();
>   }
> }
>
> run().catch((err) => {
>   console.error(err);
>   process.exit(1);
> });
> ```
>
> **6. Execute workflow**
>
> In a separate client file, connect to Temporal and execute the workflow:
>
> ```typescript client.ts theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { Client, Connection } from '@temporalio/client';
> import { initTracerProvider } from './tracer';
>
> async function run() {
>   // Initialize tracing
>   const provider = initTracerProvider();
>
>   try {
>     const connection = await Connection.connect({ address: 'localhost:7233' });
>     const client = new Client({ connection });
>
>     const result = await client.workflow.execute('myWorkflow', {
>       taskQueue: 'my-task-queue',
>       workflowId: 'my-workflow-1',
>       args: ['Hello World'],
>     });
>
>     console.log('Workflow result:', result);
>   } finally {
>     await provider.shutdown();
>   }
> }
>
> run().catch(console.error);
> ```

## View traces in LangSmith

Once configured, traces appear in the selected agent environment:

1. Navigate to your LangSmith instance.
2. Select your agent and environment.
3. View traces in the **Tracing** tab.
4. Click on individual traces to see the full span hierarchy.

## Configuration options

### Set a custom service name

Set a custom service name to distinguish different Temporal workers or services:

```go Go
ls, err := langsmith.NewTracer(
    langsmith.WithServiceName("my-temporal-worker"),
)
```

```python Python
resource = Resource.create({
    SERVICE_NAME: "my-temporal-worker",
})
```

```typescript TypeScript
const provider = new NodeTracerProvider({
  resource: new Resource({
    [ATTR_SERVICE_NAME]: 'my-temporal-worker',
  }),
});
```

### Add custom span attributes

Add custom attributes to enrich your traces:

```go Go
import "go.opentelemetry.io/otel/attribute"

span := trace.SpanFromContext(ctx)
span.SetAttributes(
    attribute.String("user.id", userID),
    attribute.String("workflow.version", "v2"),
)
```

```python Python
from opentelemetry import trace

span = trace.get_current_span()
span.set_attribute("user.id", user_id)
span.set_attribute("workflow.version", "v2")
```

```typescript TypeScript
import { trace } from '@opentelemetry/api';

const span = trace.getActiveSpan();
span?.setAttribute('user.id', userId);
span?.setAttribute('workflow.version', 'v2');
```

### Configure sampling

For high-volume workflows, configure sampling to reduce trace volume:

```go Go
// Note: langsmith.NewTracer() uses default sampling
// For custom sampling, use the TracerProvider directly
tp := sdktrace.NewTracerProvider(
    sdktrace.WithBatcher(exporter),
    sdktrace.WithSampler(sdktrace.TraceIDRatioBased(0.1)), // 10% sampling
)
```

```python Python
from opentelemetry.sdk.trace.sampling import TraceIdRatioBased

provider = TracerProvider(
    resource=resource,
    sampler=TraceIdRatioBased(0.1),  # 10% sampling
)
```

```typescript TypeScript
import { TraceIdRatioBasedSampler } from '@opentelemetry/sdk-trace-base';

const provider = new NodeTracerProvider({
  resource: resource,
  sampler: new TraceIdRatioBasedSampler(0.1), // 10% sampling
});
```

## Troubleshooting

### Traces not appearing

1. **Verify API key**: Ensure `LANGSMITH_API_KEY` is set correctly
2. **Check endpoint**: Confirm you're using `https://api.smith.langchain.com/otel/v1/traces`
3. **Flush on shutdown**: Call `provider.shutdown()` to flush pending spans before the process exits
4. **Check destination**: Verify the registered agent and environment in the exporter headers. For the Go compatibility example, verify the configured `tracer_session_name`.

### Missing activity spans

Ensure the tracing interceptor is configured on both the client and worker:

* **Client**: Needs interceptor for starting workflows
* **Worker**: Needs interceptor for executing activities

### Context propagation issues

Verify propagators are configured correctly:

* **Go**: `langsmith.NewTracer()` automatically configures propagators
* **Python/TypeScript**: Ensure OpenTelemetry SDK is properly initialized with trace propagators

### Worker shutdown hangs

If traces aren't flushing, ensure you're calling the shutdown method with proper timeout:

```go Go
defer ls.Shutdown(context.Background())
```

```python Python
finally:
    provider.shutdown()
```

```typescript TypeScript
finally {
  await provider.shutdown();
}
```

## Next steps

* [Learn about LangSmith tracing concepts](../../../Observability%20concepts.md)
* [Explore OpenTelemetry semantic conventions](../Agent%20frameworks/Trace%20with%20OpenTelemetry.md#supported-opentelemetry-attribute-and-event-mapping)

## Additional resources

* [Temporal Documentation](https://docs.temporal.io/)
* [Temporal Go SDK](https://github.com/temporalio/sdk-go)
* [Temporal Python SDK](https://github.com/temporalio/sdk-python)
* [Temporal TypeScript SDK](https://github.com/temporalio/sdk-typescript)
* [OpenTelemetry Documentation](https://opentelemetry.io/docs/)
* [LangSmith Go SDK](https://github.com/langchain-ai/langsmith-go)

# How to evaluate with OpenTelemetry

This guide shows you how to run an evaluation using OpenTelemetry tracing with LangSmith.

> [!NOTE]
>
> [Evaluations](../../Get%20started/Evaluation%20concepts.md#evaluation-lifecycle) | [Datasets](../../Get%20started/Evaluation%20concepts.md#datasets) | [Trace with OpenTelemetry](../../../Monitor/Trace/Tracing%20setup/Integrations/Agent%20frameworks/Trace%20with%20OpenTelemetry.md)

If you're already using OpenTelemetry for tracing your LLM application, you can run evaluations by routing traces to an experiment session. This approach is useful when you want to evaluate applications that are instrumented with OpenTelemetry but don't use the LangSmith SDK's [`evaluate()`](https://reference.langchain.com/python/langsmith/client/Client/evaluate) function.

## Overview

When evaluating with OpenTelemetry, you need to:

1. Create an experiment session in LangSmith.
2. Configure OpenTelemetry to send traces to LangSmith.
3. Add specific span attributes to link traces to the experiment and dataset examples.
4. Run your application for each example in the dataset.

## Prerequisites

This guide assumes you have:

* An application instrumented with OpenTelemetry that sends traces to LangSmith.
* A dataset created in LangSmith with examples to evaluate. You can create a dataset via the [LangSmith UI](../../Get%20started/Evaluation%20concepts.md#datasets) or via the [SDK](../Datasets/Create%20a%20dataset/How%20to%20create%20and%20manage%20datasets%20programmatically.md).

This tutorial uses Strands agents as example implementations, but the approach works with any OpenTelemetry-instrumentation.

Install dependencies:

```bash Python
pip install langsmith strands-agents strands-agents-tools opentelemetry-sdk opentelemetry-exporter-otlp
```

```bash TypeScript
npm install langsmith @strands-agents/sdk @opentelemetry/api @opentelemetry/sdk-trace-node @opentelemetry/sdk-trace-base @opentelemetry/exporter-trace-otlp-http @opentelemetry/resources
```

Set the following environment variables:

```bash
# Tracing configuration
LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
LANGSMITH_API_KEY="<API_KEY>"
OTEL_EXPORTER_OTLP_ENDPOINT = "https://api.smith.langchain.com/otel/"

# AWS Credentials
AWS_ACCESS_KEY_ID="<your-aws-access-key-id>"
AWS_SECRET_ACCESS_KEY="<your-aws-secret-access-key>"
AWS_REGION_NAME="<your-aws-region>"
```

Set `LANGSMITH_ENDPOINT` to your LangSmith API URL, and set `OTEL_EXPORTER_OTLP_ENDPOINT` to that URL plus `/otel`. On self-hosted LangSmith, the API URL includes `/api/v1`, for example `https://<host>/api/v1`. For the OTLP URL on each deployment type, see [Find your OTLP endpoint](../../../Monitor/Trace/Tracing%20setup/Integrations/Agent%20frameworks/Trace%20with%20OpenTelemetry.md#find-your-otlp-endpoint).

## Step 1. Create an experiment session

This guide assumes that a dataset has been created in LangSmith with examples to evaluate. You can create a dataset via the [LangSmith UI](../../Get%20started/Evaluation%20concepts.md#datasets) or via the [SDK](../Datasets/Create%20a%20dataset/How%20to%20create%20and%20manage%20datasets%20programmatically.md).

An experiment session groups all evaluation traces together. Create one using the LangSmith client:

```python Python
from langsmith import Client

# Initialize LangSmith client
client = Client()

experiment_name = "strands-agent-experiment"
# Assumes a dataset has been created. You can find the dataset ID in the LangSmith UI or via the SDK.
dataset_id = "<your-dataset-id>"

# Create an experiment session linked to the dataset
project = client.create_project(
    project_name=experiment_name,
    reference_dataset_id=dataset_id
)

experiment_id = str(project.id)
```

```typescript TypeScript
import { Client } from "langsmith";

// Initialize LangSmith client
const client = new Client({
  apiKey: process.env.LANGSMITH_API_KEY,
});

const experimentName = "strands-agent-experiment";
const datasetId = "your-dataset-id";

// Create an experiment session linked to the dataset
const project = await client.createProject({
  projectName: experimentName,
  referenceDatasetId: datasetId,
});

const experimentId = project.id;
```

Additionally, you can create evaluators in the LangSmith UI and bind them to your dataset. For evaluators defined in the UI and bound to your dataset, they will automatically run on experiment traces.

To learn more about evaluators, see [Evaluators](../../Get%20started/Evaluation%20concepts.md#evaluators).

## Step 2. Define an application and configure OpenTelemetry

First, you need an application that uses OpenTelemetry for tracing. This example uses a Strands agent, but you can use any OpenTelemetry-instrumented application. Set up OpenTelemetry to route traces to your experiment session by including the experiment ID in the OTEL headers. The general idea in this step is to have an agent or application that has been instrumented with OpenTelemetry.

> [!NOTE]
>
> TypeScript examples are not provided for this step as the `Strands TypeScript SDK` does not currently support `OpenTelemetry` observability (as of February 2026).

```python Python
import os
from strands import Agent
from strands_tools import file_read, file_write, python_repl, shell, journal
from strands.telemetry import StrandsTelemetry

# Set OTEL headers with experiment ID as the project
api_key = os.getenv('LANGSMITH_API_KEY')
os.environ['OTEL_EXPORTER_OTLP_HEADERS'] = f"x-api-key={api_key},Langsmith-Project={experiment_id}"

# Initialize telemetry
strands_telemetry = StrandsTelemetry()
strands_telemetry.setup_otlp_exporter()

# Create an agent (Strands automatically creates OTel spans)
agent = Agent(
    tools=[file_read, file_write, python_repl, shell, journal],
    system_prompt="You are an Expert Software Developer.",
    model="us.anthropic.claude-sonnet-4-20250514-v1:0",
)
```

For details on setting up OpenTelemetry tracing with LangSmith, see [Trace with OpenTelemetry](../../../Monitor/Trace/Tracing%20setup/Integrations/Agent%20frameworks/Trace%20with%20OpenTelemetry.md).

## Step 3. Set up key span attributes

Add the required span attributes to each application run. These attributes link each trace to the experiment and the specific dataset example.

The following attributes are relevant for experiment evaluation:

| Attribute | Purpose |
| - | - |
| `langsmith.trace.session_id` | Routes the trace to your experiment session |
| `langsmith.reference_example_id` | Links the trace to a specific dataset example |
| `langsmith.span.kind` | Sets the span type (e.g., "llm", "chain", "tool") |
| `inputs` | Records the input to your application |
| `outputs` | Records the output from your application |

For a complete list of supported OpenTelemetry attributes, see [Trace with OpenTelemetry](../../../Monitor/Trace/Tracing%20setup/Integrations/Agent%20frameworks/Trace%20with%20OpenTelemetry.md#supported-opentelemetry-attribute-and-event-mapping).

```python Python
from opentelemetry import trace

def evaluate_with_opentelemetry(agent, example_id: str, example_input: str, experiment_id: str):
    tracer = trace.get_tracer(__name__)

    # Wrapper span to add experiment metadata
    with tracer.start_as_current_span("experiment_evaluation") as span:
        # Route trace to the experiment
        span.set_attribute("langsmith.trace.session_id", experiment_id)

        # Link trace to the specific dataset example
        span.set_attribute("langsmith.reference_example_id", example_id)

        # Record input
        span.set_attribute("inputs", example_input)

        # Run the application
        response = agent(example_input)

        # Record output
        output_text = getattr(response, "output", str(response))
        span.set_attribute("outputs", output_text)

        return output_text
```

```typescript TypeScript
import { trace, Span } from "@opentelemetry/api";

async function evaluateWithAgent(
  agent: Agent,
  exampleId: string,
  exampleInput: string,
  experimentId: string
): Promise<string> {
  const tracer = trace.getTracer("experiment-runner");

  return await tracer.startActiveSpan(
    "experiment_evaluation",
    async (span: Span) => {
      try {
        // Route trace to the experiment
        span.setAttribute("langsmith.trace.session_id", experimentId);

        // Link trace to the specific dataset example
        span.setAttribute("langsmith.reference_example_id", exampleId);

        // Record input
        span.setAttribute("inputs", exampleInput);

        // Run the application
        const result = await agent.invoke(exampleInput);
        // Record output
        const response = String(result);
        span.setAttribute("outputs", response);

        return response;
      } finally {
        span.end();
      }
    }
  );
}
```

## Step 4. Run evaluation by iterating through dataset examples

Each experiment run creates traces in LangSmith that are linked to your dataset examples.

```python Python
# Iterate through dataset examples
for example in client.list_examples(dataset_name=dataset_name):

    # Extract input from the example inputs dictionary
    # Adjust the key based on your dataset structure
    # (e.g., "input", "question", etc.)
    example_input = example.inputs.get("input")

    evaluate_with_opentelemetry(
        agent=agent,
        example_id=str(example.id),
        example_input=str(example_input),
        experiment_id=experiment_id
    )
```

```typescript TypeScript
// Iterate through dataset examples
for await (const example of client.listExamples({ datasetName })) {
  // Extract input from the example inputs dictionary
  // Adjust the key based on your dataset structure
  // (e.g., "input", "question", etc.)
  const exampleInput = example.inputs.input;

  await evaluateWithAgent(
    agent,
    example.id,
    String(exampleInput),
    experimentId
  );
}
```

After running the evaluation, you can [analyze the experiment](../Analyze%20experiment%20results/Analyze%20an%20experiment.md) in the LangSmith UI to see:

* Individual trace details for each example
* Evaluator scores and feedback
* Comparisons between different experiment runs

Navigate to your experiment in the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-evaluate-with-opentelemetry) to analyze the results.

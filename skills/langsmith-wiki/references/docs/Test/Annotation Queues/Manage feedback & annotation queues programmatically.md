# Manage feedback & annotation queues programmatically

Use the LangSmith SDK to manage feedback configurations and [annotation queue](../Get%20started/Evaluation%20concepts.md#human) rubrics programmatically, and to add runs and threads to a queue for review. Define reusable feedback schemas at the organization level (like accuracy scores or pass/fail judgments), then assign them to specific queues with custom instructions. This enables version control, automation across projects, and consistency—particularly useful for CI/CD pipelines or replicating evaluation setups across environments.

This guide uses the Python and TypeScript SDKs. For installation and setup, refer to the [Python SDK documentation](../../Monitor/Reference/langsmith%20%28smith-python-sdk%29.md) and [TypeScript SDK documentation](../../Monitor/Reference/langsmith%20%28smith-js-ts-sdk%29.md).

> [!NOTE]
>
> To write free-form acceptance criteria on individual runs while reviewing in the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-annotation-queues-sdk), refer to [Use assertions](Use%20assertions.md).

## Feedback layers

LangSmith uses a three-layer architecture for structured human feedback:

1. **Feedback configs**: Organization-wide definitions of feedback keys that establish the schema for evaluation metrics. For example, you might define "accuracy" as a continuous 0–1 score or "correctness" as a pass/fail categorical choice. These configs are reusable across all annotation queues in your organization.
2. **Annotation queue rubric items**: Queue-specific assignments that determine which feedback configs annotators must fill out when reviewing [runs](../../Monitor/Trace/Observability%20concepts.md#runs) in a particular queue. Each rubric item can include custom descriptions, guidance for specific score values, and whether the feedback is required or optional.
3. **Feedback**: Individual scores and values that annotators submit on specific [runs](../../Monitor/Trace/Observability%20concepts.md#runs). This is the actual evaluation data collected using the schemas you've defined. Learn more about [feedback in LangSmith](../../Monitor/Trace/Observability%20concepts.md#feedback).

## Feedback configs

### Create a feedback config

Feedback configs define the schema for a feedback key—whether it's a continuous score, a categorical choice, or freeform text. A unique key identifies each config within your organization and specifies how annotators can submit feedback for that metric.

> [!NOTE]
>
> Calling [`create_feedback_config`](https://reference.langchain.com/python/langsmith/client/Client/create_feedback_config) with an identical config that already exists returns the existing config. If a different config already exists for the same key, the system raises a 400 error.

```python Python
from langsmith import Client

client = Client()

# Continuous score
client.create_feedback_config(
    "accuracy",
    feedback_config={
        "type": "continuous",
        "min": 0,
        "max": 1,
    },
    is_lower_score_better=False,
)

# Categorical
client.create_feedback_config(
    "correctness",
    feedback_config={
        "type": "categorical",
        "categories": [
            {"value": 1, "label": "Pass"},
            {"value": 0, "label": "Fail"},
        ],
    },
)

# Freeform text
client.create_feedback_config(
    "notes",
    feedback_config={"type": "freeform"},
)
```

```typescript TypeScript
import { Client } from "langsmith";

const client = new Client();

// Continuous score
await client.createFeedbackConfig({
  feedbackKey: "accuracy",
  feedbackConfig: { type: "continuous", min: 0, max: 1 },
  isLowerScoreBetter: false,
});

// Categorical
await client.createFeedbackConfig({
  feedbackKey: "correctness",
  feedbackConfig: {
    type: "categorical",
    categories: [
      { value: 1, label: "Pass" },
      { value: 0, label: "Fail" },
    ],
  },
});

// Freeform text
await client.createFeedbackConfig({
  feedbackKey: "notes",
  feedbackConfig: { type: "freeform" },
});
```

* **Continuous** (`"accuracy"`): Defines a numeric scale from 0 to 1. The `is_lower_score_better` parameter indicates whether lower values represent better performance. Use continuous configs for rating scales or percentage-based metrics.
* **Categorical** (`"correctness"`): Provides predefined options with associated values. Each category requires a `value` (used for scoring and analytics) and a `label` (shown to annotators). Use categorical configs for binary choices or multi-class classifications.
* **Freeform** (`"notes"`): Allows open-ended text input with no predefined structure. Use freeform configs for qualitative observations or explanations.

### List feedback configs

Retrieve feedback configs to see what evaluation criteria are available in your organization with [`list_feedback_configs`](https://reference.langchain.com/python/langsmith/client/Client/list_feedback_configs). You can list all configs or filter by specific keys. Each returned config object includes the key, type, configuration details (like `min`/`max` or `categories`), and metadata like `is_lower_score_better`:

```python Python
# List all configs
for config in client.list_feedback_configs():
    print(f"{config.feedback_key}: {config.feedback_config}")

# Filter by specific keys
for config in client.list_feedback_configs(
    feedback_key=["accuracy", "correctness"]
):
    print(config.feedback_key)
```

```typescript TypeScript
// List all configs
for await (const config of client.listFeedbackConfigs()) {
  console.log(`${config.feedback_key}: ${JSON.stringify(config.feedback_config)}`);
}

// Filter by specific keys
for await (const config of client.listFeedbackConfigs({
  feedbackKeys: ["accuracy", "correctness"],
})) {
  console.log(config.feedback_key);
}
```

### Update a feedback config

Modify an existing feedback config with [`update_feedback_config`](https://reference.langchain.com/python/langsmith/client/Client/update_feedback_config) by updating specific fields. The method only changes the fields you provide—the rest remain unchanged. This is a partial update that preserves other configuration settings:

```python Python
client.update_feedback_config(
    "accuracy",
    is_lower_score_better=True,
)
```

```typescript TypeScript
await client.updateFeedbackConfig("accuracy", {
  isLowerScoreBetter: true,
});
```

### Delete a feedback config

Remove a feedback config from your organization with [`delete_feedback_config`](https://reference.langchain.com/python/langsmith/client/Client/delete_feedback_config). This performs a soft delete, which marks the config as deleted but doesn't permanently remove it from the system. You can recreate a config with the same key later if needed:

```python Python
client.delete_feedback_config("accuracy")
```

```typescript TypeScript
await client.deleteFeedbackConfig("accuracy");
```

## Annotation queue rubric items

Rubric items assign feedback configs to a specific annotation queue. They control which feedback forms annotators see when reviewing [runs](../../Monitor/Trace/Observability%20concepts.md#runs) in that queue, and whether each form is required or optional.

### Create a queue with rubric items

Create an annotation queue with [`create_annotation_queue`](https://reference.langchain.com/python/langsmith/client/Client/create_annotation_queue) and assign feedback configs to it through rubric items. Each rubric item references a feedback config by its key and customizes how it appears to annotators in this specific queue.

The example creates a queue with three rubric items. The queue-level `rubric_instructions` provides general guidance shown at the top of the annotation interface:

```python Python
queue = client.create_annotation_queue(
    name="QA Review Queue",
    description="Review LLM outputs for accuracy and correctness",
    rubric_instructions="Score each response. Add notes for anything unusual.",
    rubric_items=[
        {
            "feedback_key": "accuracy",
            "description": "How accurate is the response?",
            "score_descriptions": {
                "0": "Completely wrong",
                "1": "Perfectly accurate",
            },
            "is_required": True,
        },
        {
            "feedback_key": "correctness",
            "description": "Did the response pass or fail?",
            "value_descriptions": {
                "Pass": "Factually correct",
                "Fail": "Contains errors",
            },
            "is_required": True,
        },
        {
            "feedback_key": "notes",
            "description": "Any additional observations",
            "is_required": False,
        },
    ],
)
```

```typescript TypeScript
const queue = await client.createAnnotationQueue({
  name: "QA Review Queue",
  description: "Review LLM outputs for accuracy and correctness",
  rubricInstructions: "Score each response. Add notes for anything unusual.",
  rubricItems: [
    {
      feedback_key: "accuracy",
      description: "How accurate is the response?",
      score_descriptions: { "0": "Completely wrong", "1": "Perfectly accurate" },
      is_required: true,
    },
    {
      feedback_key: "correctness",
      description: "Did the response pass or fail?",
      value_descriptions: { Pass: "Factually correct", Fail: "Contains errors" },
      is_required: true,
    },
    {
      feedback_key: "notes",
      description: "Any additional observations",
      is_required: false,
    },
  ],
});
```

* `feedback_key`: The key of an existing feedback config (create this first).
* `description`: Queue-specific guidance for annotators about this metric.
* `score_descriptions` / `value_descriptions`: Optional labels that explain what specific values mean (use `score_descriptions` for continuous configs, `value_descriptions` for categorical).
* `is_required`: Whether annotators must complete this feedback before submitting.

### Update rubric items on an existing queue

Modify the rubric items assigned to an annotation queue with [`update_annotation_queue`](https://reference.langchain.com/python/langsmith/client/Client/update_annotation_queue). This operation replaces the entire rubric items list, so you must include all items you want to keep—the operation removes any items you don't include.

You'll need the queue ID, which you get when you create the queue or by listing queues:

> [!NOTE]
>
> Updating rubric items replaces the full list. Include all items you want to keep.

```python Python
client.update_annotation_queue(
    queue.id,
    rubric_items=[
        {"feedback_key": "accuracy", "is_required": True},
        {"feedback_key": "correctness", "is_required": True},
        {
            "feedback_key": "tone",
            "description": "Is the tone appropriate?",
            "is_required": False,
        },
    ],
)
```

```typescript TypeScript
await client.updateAnnotationQueue(queue.id, {
  rubricItems: [
    { feedback_key: "accuracy", is_required: true },
    { feedback_key: "correctness", is_required: true },
    { feedback_key: "tone", description: "Is the tone appropriate?", is_required: false },
  ],
});
```

## Add runs and threads to a queue

Add [runs](../../Monitor/Trace/Observability%20concepts.md#runs) and [threads](../../Monitor/Trace/Observability%20concepts.md#threads) to a single-run annotation queue with the annotation queue `items` resource. A single request accepts a mixed batch of run items and thread items, so this method covers everything the UI [add flow](Use%20annotation%20queues.md#assign-runs-and-threads-to-a-single-run-queue) supports.

> [!NOTE]
>
> The `items` resource requires `langsmith>=0.10.13` (Python) or `langsmith>=0.8.8` (TypeScript), served by a LangSmith backend on version `0.16.14` or later.

Each item sets an `item_type` of `RUN` or `THREAD`:

* **RUN items** require `run_id`. Also provide `project_id` (the project UUID) and `start_time`, which together locate the run directly.
* **THREAD items** require `thread_id` and `project_id`.

Resolve these IDs with the SDK:

* **`project_id`**: Look up a project by name with [`read_project`](https://reference.langchain.com/python/langsmith/client/Client/read_project) and read its `id`, for example `client.read_project(project_name="my-project").id`.
* **`run_id`**: Query runs with `client.runs.query()`. Each run exposes `id`, `project_id`, and `start_time`, the fields a RUN item needs.
* **`thread_id`**: Query threads with `client.threads.query()`. Each result exposes its `thread_id`.

You can also find these IDs in the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-annotation-queues-sdk):

* **`project_id`**: In a [tracing project](../../Monitor/Trace/Observability%20concepts.md#tracing-projects), click the **ID** badge next to the project name to copy the project UUID.
* **`run_id`**: Open a run in the [Details view](../../Monitor/Debug/Viewing%20%26%20managing%20traces/View%20traces.md#details-view) and click the **ID** badge next to the run name to copy the run ID.
* **`thread_id`**: In the **Threads** view of a tracing project, copy the value from the **Thread ID** column.

To extend trace retention for the added run items, pass `extend_trace_retention=True`. The response is an envelope with an `items` array, one entry per added item.

> [!NOTE]
>
> In Python, `annotation_queues.items.create` is async, so `await` it inside an event loop.

```python Python
import asyncio

async def main():
    queue_name = "<queue_name>"
    project_id = "<project_id>"
    run_id = "<run_id>"
    thread_id = "<thread_id>"

    # Look up the annotation queue by name to get its ID.
    queue = next(client.list_annotation_queues(name=queue_name), None)
    if queue is None:
        raise SystemExit(f"No annotation queue named {queue_name!r}")

    # Fetch the run to add by id + project_id. runs.retrieve() requires
    # `selects` (uppercase RunSelectField names) to return fields like
    # start_time.
    run = await client.runs.retrieve(
        run_id=run_id,
        project_id=project_id,
        selects=["ID", "PROJECT_ID", "START_TIME"],
    )

    response = await client.annotation_queues.items.create(
        str(queue.id),
        items=[
            {
                "item_type": "RUN",
                "run_id": run_id,
                "project_id": project_id,
                "start_time": run.start_time,
            },
            {
                "item_type": "THREAD",
                "thread_id": thread_id,
                "project_id": project_id,
            },
        ],
    )

    # response.items contains one entry per added item.
    for item in response.items or []:
        print(item.id, item.item_type)

asyncio.run(main())
```

```typescript TypeScript
const queueName = "<queue_name>";
const projectId = "<project_id>";
const runId = "<run_id>";
const threadId = "<thread_id>";

// Look up the annotation queue by name to get its ID.
let queue;
for await (const q of client.listAnnotationQueues({ name: queueName })) {
  queue = q;
  break;
}
if (!queue) {
  throw new Error(`No annotation queue named ${queueName}`);
}

// Fetch the run to add by id + project_id. retrieve() requires `selects`
// (uppercase RunSelectField names) to return fields like start_time.
const run = await client.runs.retrieve(runId, {
  project_id: projectId,
  selects: ["ID", "PROJECT_ID", "START_TIME"],
});

const response = await client.annotationQueues.items.create(queue.id, {
  items: [
    {
      item_type: "RUN",
      run_id: runId,
      project_id: projectId,
      start_time: run.start_time,
    },
    {
      item_type: "THREAD",
      thread_id: threadId,
      project_id: projectId,
    },
  ],
});

// response.items contains one entry per added item.
for (const item of response.items ?? []) {
  console.log(item.id, item.item_type);
}
```

> [!NOTE]
>
> For runs-only additions, [`add_runs_to_annotation_queue`](https://reference.langchain.com/python/langsmith/client/Client/add_runs_to_annotation_queue) still works and remains the simplest option when you are not adding threads. New code that adds threads, or mixed run and thread batches, should use the `items` resource.

## Feedback config types (detailed)

### Continuous

Continuous configs define numeric rating scales with minimum and maximum values. Annotators can select any value within the range, making this ideal for scoring dimensions like accuracy, quality, or relevance on a numeric scale:

```python Python
# Simple continuous score
client.create_feedback_config(
    "accuracy",
    feedback_config={
        "type": "continuous",
        "min": 0,
        "max": 1,
    },
)

# Continuous with labeled points on the scale
client.create_feedback_config(
    "quality",
    feedback_config={
        "type": "continuous",
        "min": 1,
        "max": 5,
        "categories": [
            {"value": 1, "label": "Poor"},
            {"value": 3, "label": "Average"},
            {"value": 5, "label": "Excellent"},
        ],
    },
)
```

```typescript TypeScript
await client.createFeedbackConfig({
  feedbackKey: "accuracy",
  feedbackConfig: { type: "continuous", min: 0, max: 1 },
});

await client.createFeedbackConfig({
  feedbackKey: "quality",
  feedbackConfig: {
    type: "continuous",
    min: 1,
    max: 5,
    categories: [
      { value: 1, label: "Poor" },
      { value: 3, label: "Average" },
      { value: 5, label: "Excellent" },
    ],
  },
});
```

The first example shows a 0–1 scale without labels. The second example demonstrates adding `categories` with labeled anchor points on the scale (like "Poor", "Average", "Excellent") to help annotators understand what different values represent. These labels are optional but can improve consistency in how annotators interpret the scale.

### Categorical

Categorical configs provide a discrete set of predefined options for annotators to choose from. Each category must have a `value` (a numeric identifier used for scoring and analytics) and a `label` (the text shown to annotators). You must define at least 2 categories.

Use categorical configs for binary decisions (pass/fail, correct/incorrect), multi-class classifications (sentiment, topic categories), or any evaluation with a fixed set of discrete options. Do not set `min` or `max` for categorical configs:

```python Python
# Binary pass/fail
client.create_feedback_config(
    "correctness",
    feedback_config={
        "type": "categorical",
        "categories": [
            {"value": 1, "label": "Pass"},
            {"value": 0, "label": "Fail"},
        ],
    },
)

# Multi-class
client.create_feedback_config(
    "sentiment",
    feedback_config={
        "type": "categorical",
        "categories": [
            {"value": 0, "label": "Negative"},
            {"value": 1, "label": "Neutral"},
            {"value": 2, "label": "Positive"},
        ],
    },
)
```

```typescript TypeScript
await client.createFeedbackConfig({
  feedbackKey: "correctness",
  feedbackConfig: {
    type: "categorical",
    categories: [
      { value: 1, label: "Pass" },
      { value: 0, label: "Fail" },
    ],
  },
});

await client.createFeedbackConfig({
  feedbackKey: "sentiment",
  feedbackConfig: {
    type: "categorical",
    categories: [
      { value: 0, label: "Negative" },
      { value: 1, label: "Neutral" },
      { value: 2, label: "Positive" },
    ],
  },
});
```

The first example shows a binary pass/fail config. The second example demonstrates a multi-class config for sentiment with three options. The numeric values allow you to compute aggregate scores even for categorical feedback.

### Freeform

Freeform configs allow annotators to provide open-ended text feedback without any predefined structure or constraints. This type has no `min`, `max`, or `categories` fields—annotators can enter any text they want.

Freeform feedback is valuable for capturing nuanced insights but is harder to aggregate and analyze compared to structured feedback types:

```python Python
client.create_feedback_config(
    "notes",
    feedback_config={"type": "freeform"},
)
```

```typescript TypeScript
await client.createFeedbackConfig({
  feedbackKey: "notes",
  feedbackConfig: { type: "freeform" },
});
```

## Validation rules

| Type | min/max | categories | Constraints |
| - | - | - | - |
| `continuous` | Optional | Optional (labeled scale points) | `min < max`; category values within \[`min`, `max`] |
| `categorical` | Must not be set | Required, min 2 | Unique values and labels |
| `freeform` | Must not be set | Must not be set | N/A |

## Reference

### Feedback config types

| Type | Fields | Description |
| - | - | - |
| `continuous` | `min`, `max` | Numeric score within a range |
| `categorical` | categories (list of `{value, label}`) | Selection from predefined options |
| `freeform` | None | Free-text input |

### Rubric item fields

| Field | Type | Description |
| - | - | - |
| `feedback_key` | `string` | Required. Must match an existing feedback config key. |
| `description` | `string` | Shows annotators guidance for this item. |
| `score_descriptions` | `Record<string, string>` | Labels for specific score values (continuous). |
| `value_descriptions` | `Record<string, string>` | Labels for specific category values (categorical). |
| `is_required` | `boolean` | Whether annotators must complete this item before submitting. Defaults to false. |

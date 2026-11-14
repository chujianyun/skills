# How to fetch performance metrics for an experiment

> [!TIP]
>
> Tracing projects and experiments use the same underlying data structure in our backend, which is called a "session."
>
> You might see these terms interchangeably in our documentation, but they all refer to the same underlying data structure.
>
> We are working on unifying the terminology across our documentation and APIs.

When you run an experiment using `evaluate` with the Python or TypeScript SDK, you can fetch the performance metrics for the experiment using the `read_project`/`readProject` methods.

The payload for experiment details includes the following values:

```json
{
  "start_time": "2024-06-06T01:02:51.299960",
  "end_time": "2024-06-06T01:03:04.557530+00:00",
  "extra": {
    "metadata": {
      "git": {
        "tags": null,
        "dirty": true,
        "branch": "ankush/agent-eval",
        "commit": "...",
        "repo_name": "...",
        "remote_url": "...",
        "author_name": "Ankush Gola",
        "commit_time": "...",
        "author_email": "..."
      },
      "revision_id": null,
      "dataset_splits": ["base"],
      "dataset_version": "2024-06-05T04:57:01.535578+00:00",
      "num_repetitions": 3
    }
  },
  "name": "SQL Database Agent-ae9ad229",
  "description": null,
  "default_dataset_id": null,
  "reference_dataset_id": "...",
  "id": "...",
  "run_count": 9,
  "latency_p50": 7.896,
  "latency_p99": 13.09332,
  "first_token_p50": null,
  "first_token_p99": null,
  "total_tokens": 35573,
  "prompt_tokens": 32711,
  "completion_tokens": 2862,
  "total_cost": 0.206485,
  "prompt_cost": 0.163555,
  "completion_cost": 0.04293,
  "tenant_id": "...",
  "last_run_start_time": "2024-06-06T01:02:51.366397",
  "last_run_start_time_live": null,
  "feedback_stats": {
    "cot contextual accuracy": {
      "n": 9,
      "avg": 0.6666666666666666,
      "values": {
        "CORRECT": 6,
        "INCORRECT": 3
      }
    }
  },
  "session_feedback_stats": {},
  "run_facets": [],
  "error_rate": 0,
  "streaming_rate": 0,
  "test_run_number": 11
}
```

From here, you can extract performance metrics such as:

* `latency_p50`: The 50th percentile latency in seconds.
* `latency_p99`: The 99th percentile latency in seconds.
* `total_tokens`: The total number of tokens used.
* `prompt_tokens`: The number of prompt tokens used.
* `completion_tokens`: The number of completion tokens used.
* `total_cost`: The total cost of the experiment.
* `prompt_cost`: The cost of the prompt tokens.
* `completion_cost`: The cost of the completion tokens.
* `feedback_stats`: The feedback statistics for the experiment.
* `error_rate`: The error rate for the experiment.
* `first_token_p50`: The 50th percentile latency for the time to generate the first token (if using streaming).
* `first_token_p99`: The 99th percentile latency for the time to generate the first token (if using streaming).

Here is an example of how you can fetch the performance metrics for an experiment using the Python and TypeScript SDKs.

First, as a prerequisite, we will create a trivial dataset. Here, we only demonstrate this in Python, but you can do the same in TypeScript. Please view the [how-to guide](../Run%20an%20evaluation/How%20to%20evaluate%20agents.md) on evaluation for more details.

```python
from langsmith import Client

client = Client()

# Create a dataset
dataset_name = "HelloDataset"
dataset = client.create_dataset(dataset_name=dataset_name)

examples = [
    {
        "inputs": {"input": "Harrison"},
        "outputs": {"expected": "Hello Harrison"},
    },
    {
        "inputs": {"input": "Ankush"},
        "outputs": {"expected": "Hello Ankush"},
    },
]

client.create_examples(dataset_id=dataset.id, examples=examples)
```

Next, we will create an experiment, retrieve the experiment name from the result of `evaluate`, then fetch the performance metrics for the experiment.

```python Python
from langsmith.schemas import Example, Run
dataset_name = "HelloDataset"

def foo_label(root_run: Run, example: Example) -> dict:
    return {"score": 1, "key": "foo"}

from langsmith import evaluate

results = evaluate(
    lambda inputs: "Hello " + inputs["input"],
    data=dataset_name,
    evaluators=[foo_label],
    experiment_prefix="Hello",
)

resp = client.read_project(project_name=results.experiment_name, include_stats=True)
print(resp.model_dump_json(indent=2))
```

```typescript TypeScript
import { Client } from "langsmith";
import { evaluate } from "langsmith/evaluation";
import type { EvaluationResult } from "langsmith/evaluation";
import type { Run, Example } from "langsmith/schemas";

// Row-level evaluator
function fooLabel(rootRun: Run, example: Example): EvaluationResult {
    return {score: 1, key: "foo"};
}

const client = new Client();

const results = await evaluate(
    (inputs) => {
        return { output: "Hello " + inputs.input };
    },
    {
        data: "HelloDataset",
        experimentPrefix: "Hello",
        evaluators: [fooLabel],
    }
);

const resp = await client.readProject({
    projectName: results.experimentName,
    includeStats: true
})
console.log(JSON.stringify(resp, null, 2))
```

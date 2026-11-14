# How to read experiment results locally

When running [evaluations](../../../Get%20started/Evaluation%20concepts.md), you may want to process results programmatically in your script rather than viewing them in the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-read-local-experiment-results). This is useful for scenarios like:

* **CI/CD pipelines**: Implement quality gates that fail builds if evaluation scores drop below a threshold.
* **Local debugging**: Inspect and analyze results without API calls.
* **Custom aggregations**: Calculate metrics and statistics using your own logic.
* **Integration testing**: Use evaluation results to gate merges or deployments.

This guide shows you how to iterate over and process [experiment](../../../Get%20started/Evaluation%20concepts.md#experiment) results from the [`ExperimentResults`](https://reference.langchain.com/python/langsmith/schemas/ExperimentResults) object returned by [`Client.evaluate()`](https://reference.langchain.com/python/langsmith/client/Client/evaluate).

> [!NOTE]
>
> This page focuses on processing results programmatically while still uploading them to LangSmith.
>
> If you want to run evaluations locally **without** recording anything to LangSmith (for quick testing or validation), refer to [Run an evaluation locally](How%20to%20run%20an%20evaluation%20locally%20%28Python%20only%29.md) which uses `upload_results=False`.

## Iterate over evaluation results

The [`evaluate()`](https://reference.langchain.com/python/langsmith/client/Client/evaluate) function returns an [`ExperimentResults`](https://reference.langchain.com/python/langsmith/schemas/ExperimentResults) object that you can iterate over. The `blocking` parameter controls when results become available:

* `blocking=False`: Returns immediately with an iterator that yields results as they're produced. This allows you to process results in real-time as the evaluation runs.
* `blocking=True` (default): Blocks until all evaluations complete before returning. When you iterate over the results, all data is already available.

Both modes return the same `ExperimentResults` type; the difference is whether the function waits for completion before returning. Use `blocking=False` for streaming and real-time debugging, or `blocking=True` for batch processing when you need the complete dataset.

The following example demonstrates `blocking=False`. It iterates over results as they stream in, collects them in a list, then processes them in a separate loop:

```python
from langsmith import Client
import random

client = Client()

def target(inputs):
    """Your application or LLM chain"""
    return {"output": "MY OUTPUT"}

def evaluator(run, example):
    """Your evaluator function"""
    return {"key": "randomness", "score": random.randint(0, 1)}

# Run evaluation with blocking=False to get an iterator
streamed_results = client.evaluate(
    target,
    data="MY_DATASET_NAME",
    evaluators=[evaluator],
    blocking=False
)

# Collect results as they stream in
aggregated_results = []
for result in streamed_results:
    aggregated_results.append(result)

# Separate loop to avoid logging at the same time as logs from evaluate()
for result in aggregated_results:
    print("Input:", result["run"].inputs)
    print("Output:", result["run"].outputs)
    print("Evaluation Results:", result["evaluation_results"]["results"])
    print("--------------------------------")
```

This produces output like:

```
Input: {'input': 'MY INPUT'}
Output: {'output': 'MY OUTPUT'}
Evaluation Results: [EvaluationResult(key='randomness', score=1, value=None, comment=None, correction=None, evaluator_info={}, feedback_config=None, source_run_id=UUID('7ebb4900-91c0-40b0-bb10-f2f6a451fd3c'), target_run_id=None, extra=None)]
--------------------------------
```

## Understand the result structure

Each result in the iterator contains:

* `result["run"]`: The execution of your target function.
  * `result["run"].inputs`: The inputs from your [dataset](../../../Get%20started/Evaluation%20concepts.md#datasets) example.
  * `result["run"].outputs`: The outputs produced by your target function.
  * `result["run"].id`: The unique ID for this run.

* `result["evaluation_results"]["results"]`: A list of `EvaluationResult` objects, one per evaluator.
  * `key`: The metric name (from your evaluator's return value).
  * `score`: The numeric score (typically 0-1 or boolean).
  * `comment`: Optional explanatory text.
  * `source_run_id`: The ID of the evaluator run.

* `result["example"]`: The dataset example that was evaluated.
  * `result["example"].inputs`: The input values.
  * `result["example"].outputs`: The reference outputs (if any).

## Examples

### Implement a quality gate

This example uses evaluation results to pass or fail a CI/CD build automatically based on quality thresholds. The script iterates through results, calculates an average accuracy score, and exits with a non-zero status code if the accuracy falls below 85%. This ensures that you can deploy code changes that meet quality standards.

```python
from langsmith import Client
import sys

client = Client()

def my_application(inputs):
    # Your application logic
    return {"response": "..."}

def accuracy_evaluator(run, example):
    # Your evaluation logic
    is_correct = run.outputs["response"] == example.outputs["expected"]
    return {"key": "accuracy", "score": 1 if is_correct else 0}

# Run evaluation
results = client.evaluate(
    my_application,
    data="my_test_dataset",
    evaluators=[accuracy_evaluator],
    blocking=False
)

# Calculate aggregate metrics
total_score = 0
count = 0

for result in results:
    eval_result = result["evaluation_results"]["results"][0]
    total_score += eval_result.score
    count += 1

average_accuracy = total_score / count

print(f"Average accuracy: {average_accuracy:.2%}")

# Fail the build if accuracy is too low
if average_accuracy < 0.85:
    print("❌ Evaluation failed! Accuracy below 85% threshold.")
    sys.exit(1)

print("✅ Evaluation passed!")
```

### Batch processing with blocking=True

When you need to perform operations that require the complete dataset (like calculating percentiles, sorting by score, or generating summary reports), use `blocking=True` to wait for all evaluations to complete before processing:

```python
# Run evaluation and wait for all results
results = client.evaluate(
    target,
    data=dataset,
    evaluators=[evaluator],
    blocking=True  # Wait for all evaluations to complete
)

# Process all results after evaluation completes
for result in results:
    print("Input:", result["run"].inputs)
    print("Output:", result["run"].outputs)

    # Access individual evaluation results
    for eval_result in result["evaluation_results"]["results"]:
        print(f"  {eval_result.key}: {eval_result.score}")
```

With `blocking=True`, your processing code runs only after all evaluations are complete, avoiding mixed output with evaluation logs.

For more information on running evaluations without uploading results, refer to [Run an evaluation locally](How%20to%20run%20an%20evaluation%20locally%20%28Python%20only%29.md).

## Related

* [Evaluate your LLM application](../../Run%20an%20evaluation/How%20to%20evaluate%20agents.md)
* [Run an evaluation locally](How%20to%20run%20an%20evaluation%20locally%20%28Python%20only%29.md)
* [Fetch performance metrics from an experiment](../../Analyze%20experiment%20results/How%20to%20fetch%20performance%20metrics%20for%20an%20experiment.md)

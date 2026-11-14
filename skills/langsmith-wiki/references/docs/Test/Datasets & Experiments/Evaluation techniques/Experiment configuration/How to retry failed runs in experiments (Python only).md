# How to retry failed runs in experiments (Python only)

When running [evaluations](../../../Get%20started/Evaluation%20concepts.md#evaluation-lifecycle) on large [datasets](../../../Get%20started/Evaluation%20concepts.md#datasets), you may encounter failures on a small subset of examples due to rate limits, network issues, or other transient errors. Rather than re-running the entire evaluation, you can identify and retry only the failed examples on an [experiment](../../../Get%20started/Evaluation%20concepts.md#experiment).

This guide shows an approach to build retry logic into your evaluation workflow and to retry only the failed examples. You can use the `error_handling='ignore'` parameter to skip logging errored runs, then automatically identify unsuccessful examples and re-run them in Python.

## Step 1. Run the initial evaluation

Run the initial evaluation, ignoring errors to  prevent errored runs from being logged:

```python
from langsmith import Client

client = Client()

# Run initial evaluation, ignoring errors
# error_handling='ignore' prevents errored runs from being logged
results = await client.aevaluate(
    target,
    data="dataset",
    evaluators=[your_evaluators],
    error_handling='ignore'
)
```

## Step 2. Retry on failed examples and log to same experiment

Fetch all the unsuccessful examples:

```python
# Identify unsuccessful examples
experiment = client.read_project(project_name=results.experiment_name)
successful_example_ids = {
    run.reference_example_id
    async for run in client.runs.query(
        project_ids=[str(experiment.id)],
        min_start_time=experiment.start_time,
        is_root=True,
        has_error=False,
        selects=["REFERENCE_EXAMPLE_ID"],
    )
}
unsuccessful_examples = [
    e for e in client.list_examples(dataset_name="dataset") if str(e.id) not in successful_example_ids
]
```

Next, re-run all the failed examples and log them to the same experiment:

```python
# Retry only the failed examples, log
results_retry = await client.aevaluate(
    target,
    unsuccessful_examples,
    evaluators=[your_evaluators],
    experiment=results.experiment_name,
    error_handling='ignore'
)
```

## Related topics

* [Run an evaluation](../../Run%20an%20evaluation/How%20to%20evaluate%20agents.md)
* [Run an evaluation asynchronously](How%20to%20run%20an%20evaluation%20asynchronously.md)
* [Handle model rate limits](How%20to%20handle%20model%20rate%20limits.md)
* [Experiment configuration](Experiment%20configuration.md)
* [Evaluate existing experiment](How%20to%20add%20evaluators%20to%20an%20existing%20experiment%20%28Python%20only%29.md)

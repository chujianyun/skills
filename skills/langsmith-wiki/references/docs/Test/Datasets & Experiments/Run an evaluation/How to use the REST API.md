# How to use the REST API

The [Python](https://reference.langchain.com/python/langsmith/) and [TypeScript](https://reference.langchain.com/javascript/modules/langsmith.html) SDKs are the recommended way to run [evaluations](../../Get%20started/Evaluation%20concepts.md) in LangSmith. They include optimizations and features that enhance performance and reliability.

If you cannot use the SDKs—for example, if you are working in a different language or a restricted environment—you can use the REST API directly. This guide demonstrates how to run evaluations using the [REST API](../../../Monitor/Reference/LangSmith%20REST%20API/LangSmith%20API%20reference.md) with Python's [`requests`](https://requests.readthedocs.io/) library, but the same principles apply to any language.

Before diving into this content, it might be helpful to read the following:

* [Evaluate LLM applications](How%20to%20evaluate%20agents.md).
* [LangSmith API Reference](../../../Monitor/Reference/LangSmith%20REST%20API/LangSmith%20API%20reference.md): Complete API documentation for all endpoints used in this guide.

## Create a dataset

For this example, we use the Python SDK to create a [dataset](../../Get%20started/Evaluation%20concepts.md#datasets) quickly. To create datasets via the API or UI instead, refer to [Managing datasets](../Datasets/Create%20a%20dataset/Create%20and%20manage%20datasets%20in%20the%20UI.md).

```python
import os
import requests

from datetime import datetime
from langsmith import Client
from openai import OpenAI
from langsmith import uuid7
client = Client()
oa_client = OpenAI()

#  Create a dataset
examples = [
    {
        "inputs": {"text": "Shut up, idiot"},
        "outputs": {"label": "Toxic"},
    },
    {
        "inputs": {"text": "You're a wonderful person"},
        "outputs": {"label": "Not toxic"},
    },
    {
        "inputs": {"text": "This is the worst thing ever"},
        "outputs": {"label": "Toxic"},
    },
    {
        "inputs": {"text": "I had a great day today"},
        "outputs": {"label": "Not toxic"},
    },
    {
        "inputs": {"text": "Nobody likes you"},
        "outputs": {"label": "Toxic"},
    },
    {
        "inputs": {"text": "This is unacceptable. I want to speak to the manager."},
        "outputs": {"label": "Not toxic"},
    },
]

dataset_name = "Toxic Queries - API Example"
dataset = client.create_dataset(dataset_name=dataset_name)
client.create_examples(dataset_id=dataset.id, examples=examples)
```

## Run a single experiment

To run an experiment via the API, you'll need to:

1. Fetch the examples from your dataset.
2. Create an experiment (also called a "session" in the API).
3. For each example, create runs that reference both the example and the experiment.
4. Close the experiment by setting its `end_time`.

First, pull all of the examples you'd want to use in your experiment using the `/examples` endpoint:

```python
#  Pick a dataset id. In this case, we are using the dataset we created above.
#  API Reference: https://docs.langchain.com/langsmith/smith-api/examples/read-examples
dataset_id = dataset.id
params = { "dataset": dataset_id }

resp = requests.get(
    "https://api.smith.langchain.com/api/v1/examples",
    params=params,
    headers={"x-api-key": os.environ["LANGSMITH_API_KEY"]}
)

examples = resp.json()
```

from langsmith import uuid7

Next, define a function that will run your model on a single example and log the results to LangSmith. When using the API directly, you're responsible for:

* Creating run objects via POST to `/runs` with `reference_example_id` and `session_id` set.
* Tracking parent-child relationships between runs (e.g., a parent "chain" run containing a child "llm" run).
* Updating runs with outputs via PATCH to `/runs/{run_id}`.

```python
os.environ["OPENAI_API_KEY"] = "sk-..."

def run_completion_on_example(example, model_name, experiment_id):
    """Run completions on a list of examples."""
    # We are using the OpenAI API here, but you can use any model you like

    def _post_run(run_id, name, run_type, inputs, parent_id=None):
        """Function to post a new run to the API.
        API Reference: https://docs.langchain.com/langsmith/smith-api/runs/create-a-run
        """
        data = {
            "id": run_id.hex,
            "name": name,
            "run_type": run_type,
            "inputs": inputs,
            "start_time": datetime.utcnow().isoformat(),
            "reference_example_id": example["id"],
            "session_id": experiment_id,
        }
        if parent_id:
            data["parent_run_id"] = parent_id.hex
        resp = requests.post(
            "https://api.smith.langchain.com/api/v1/runs", # Update appropriately for self-hosted installations or regional SaaS
            json=data,
            headers=headers
        )
        resp.raise_for_status()

    def _patch_run(run_id, outputs):
        """Function to patch a run with outputs.
        API Reference: https://docs.langchain.com/langsmith/smith-api/run/update-run
        """
        resp = requests.patch(
            f"https://api.smith.langchain.com/api/v1/runs/{run_id}",
            json={
                "outputs": outputs,
                "end_time": datetime.utcnow().isoformat(),
            },
            headers=headers,
        )
        resp.raise_for_status()

    # Send your API Key in the request headers
    headers = {"x-api-key": os.environ["LANGSMITH_API_KEY"]}

    text = example["inputs"]["text"]

    messages = [
        {
            "role": "system",
            "content": "Please review the user query below and determine if it contains any form of toxic behavior, such as insults, threats, or highly negative comments. Respond with 'Toxic' if it does, and 'Not toxic' if it doesn't.",
        },
        {"role": "user", "content": text},
    ]


    # Create parent run
    parent_run_id = uuid7()
    _post_run(parent_run_id, "LLM Pipeline", "chain", {"text": text})

    # Create child run
    child_run_id = uuid7()
    _post_run(child_run_id, "OpenAI Call", "llm", {"messages": messages}, parent_run_id)

    # Generate completion
    chat_completion = oa_client.chat.completions.create(model=model_name, messages=messages)
    output_text = chat_completion.choices[0].message.content

    # End run
    _patch_run(child_run_id, {
    "messages": messages,
        "output": output_text,
        "model": model_name
    })

    _patch_run(parent_run_id, {"label": output_text})
```

Now create the experiments and run completions on all examples. In the API, an "experiment" is represented as a session (or "tracer session") that references a dataset via `reference_dataset_id`. The key difference from regular tracing is that runs in an experiment must have a `reference_example_id` that links each run to a specific example in the dataset.

```python
#  Create a new experiment using the /sessions endpoint
#  An experiment is a collection of runs with a reference to the dataset used
#  API Reference: https://docs.langchain.com/langsmith/smith-api/tracer-sessions/create-tracer-session

model_names = ("gpt-5.4-mini", "gpt-6.1-sol")
experiment_ids = []
for model_name in model_names:
    resp = requests.post(
        "https://api.smith.langchain.com/api/v1/sessions",
        json={
            "start_time": datetime.utcnow().isoformat(),
            "reference_dataset_id": str(dataset_id),
            "description": "An optional description for the experiment",
            "name": f"Toxicity detection - API Example - {model_name} - {str(uuid7())[0:8]}",  # A name for the experiment
            "extra": {
                "metadata": {"foo": "bar"},  # Optional metadata
            },
        },
        headers={"x-api-key": os.environ["LANGSMITH_API_KEY"]}
    )

    experiment = resp.json()
    experiment_ids.append(experiment["id"])

    # Run completions on all examples
    for example in examples:
        run_completion_on_example(example, model_name, experiment["id"])

    # Issue a patch request to "end" the experiment by updating the end_time
    requests.patch(
        f"https://api.smith.langchain.com/api/v1/sessions/{experiment['id']}",
        json={"end_time": datetime.utcnow().isoformat()},
        headers={"x-api-key": os.environ["LANGSMITH_API_KEY"]}
    )
```

### Add evaluation feedback

After running your [experiments](../../Get%20started/Evaluation%20concepts.md#experiment), you'll typically want to evaluate the results by adding feedback scores. This allows you to track metrics like correctness, accuracy, or any custom evaluation criteria.

In this example, the evaluation checks if each model's output matches the expected label in the dataset. The code posts a "correctness" score (1.0 for correct, 0.0 for incorrect) to track how accurately each model classifies toxic vs. non-toxic text.

The following code adds feedback to the runs from the [single experiment example](#run-a-single-experiment):

```python
# Fetch the runs from one of the experiments
# API Reference: https://docs.langchain.com/langsmith/smith-api/runs/query-runs
experiment_id = experiment_ids[0]  # Evaluate the first experiment

# Without min_start_time, the query only covers the last 24 hours.
# Start from the experiment's start time so older experiments still return all runs.
experiment = requests.get(
    f"https://api.smith.langchain.com/api/v1/sessions/{experiment_id}",
    headers={"x-api-key": os.environ["LANGSMITH_API_KEY"]}
).json()

runs_resp = requests.post(
    "https://api.smith.langchain.com/api/v2/runs/query",
    headers={"x-api-key": os.environ["LANGSMITH_API_KEY"]},
    json={
        "project_ids": [experiment_id],
        "min_start_time": experiment["start_time"],
        "is_root": True,  # Only fetch root runs
        "selects": ["ID", "REFERENCE_EXAMPLE_ID", "OUTPUTS", "PROJECT_ID"],
        "page_size": 1000,  # Up to 1000 runs per page; follow "next_cursor" for more
    }
)

runs = runs_resp.json()["items"]

# Evaluate each run by comparing outputs to expected values
for run in runs:
    # Get the expected output from the original example
    example_id = run["reference_example_id"]
    expected_output = next(
        ex["outputs"]["label"]
        for ex in examples
        if ex["id"] == example_id
    )

    # Compare the model output to the expected output
    actual_output = run["outputs"].get("label", "")
    is_correct = expected_output.lower() == actual_output.lower()

    # Post feedback score
    # API Reference: https://docs.langchain.com/langsmith/smith-api/feedback/create-feedback
    feedback = {
        "run_id": str(run["id"]),
        "key": "correctness",  # The name of your evaluation metric
        "score": 1.0 if is_correct else 0.0,
        "session_id": run["project_id"],  # Required: the run's tracing project UUID
        "comment": f"Expected: {expected_output}, Got: {actual_output}",  # Optional
    }

    resp = requests.post(
        "https://api.smith.langchain.com/api/v1/feedback",
        json=feedback,
        headers={"x-api-key": os.environ["LANGSMITH_API_KEY"]}
    )
    resp.raise_for_status()
```

You can add multiple feedback scores with different keys to track various metrics. For example, you might add both a "correctness" score and a "toxicity\_detected" score.

## Run a pairwise experiment

Next, we'll demonstrate how to run a pairwise experiment. In a pairwise experiment, you compare two examples against each other.

For more information, check out [How to run a pairwise evaluation](../../Evaluators/Evaluator%20types/SDK/How%20to%20run%20a%20pairwise%20evaluation.md).

```python
#  A comparative experiment allows you to provide a preferential ranking on the outputs of two or more experiments
#  API Reference: https://docs.langchain.com/langsmith/smith-api/datasets/create-comparative-experiment
resp = requests.post(
    "https://api.smith.langchain.com/api/v1/datasets/comparative",
    json={
        "experiment_ids": experiment_ids,
        "name": "Toxicity detection - API Example - Comparative - " + str(uuid7())[0:8],
        "description": "An optional description for the comparative experiment",
        "extra": {
            "metadata": {"foo": "bar"},  # Optional metadata
        },
        "reference_dataset_id": str(dataset_id),
    },
    headers={"x-api-key": os.environ["LANGSMITH_API_KEY"]}
)

comparative_experiment = resp.json()
comparative_experiment_id = comparative_experiment["id"]

#  You can iterate over the runs in the experiments belonging to the comparative experiment and preferentially rank the outputs

#  Fetch the comparative experiment
resp = requests.get(
    f"https://api.smith.langchain.com/api/v1/datasets/{str(dataset_id)}/comparative",
    params={"id": comparative_experiment_id},
    headers={"x-api-key": os.environ["LANGSMITH_API_KEY"]}
)

comparative_experiment = resp.json()[0]
experiment_ids = [info["id"] for info in comparative_experiment["experiments_info"]]

from collections import defaultdict
example_id_to_runs_map = defaultdict(list)

# Without min_start_time, the query only covers the last 24 hours.
# Start from the earliest experiment's start time.
min_start_time = min(
    requests.get(
        f"https://api.smith.langchain.com/api/v1/sessions/{experiment_id}",
        headers={"x-api-key": os.environ["LANGSMITH_API_KEY"]}
    ).json()["start_time"]
    for experiment_id in experiment_ids
)

#  API Reference: https://docs.langchain.com/langsmith/smith-api/runs/query-runs
runs = requests.post(
    "https://api.smith.langchain.com/api/v2/runs/query",
    headers={"x-api-key": os.environ["LANGSMITH_API_KEY"]},
    json={
        "project_ids": experiment_ids,
        "min_start_time": min_start_time,
        "is_root": True, # Only fetch root runs (spans) which contain the end outputs
        "selects": ["ID", "REFERENCE_EXAMPLE_ID", "OUTPUTS", "PROJECT_ID"],
        "page_size": 1000,  # Up to 1000 runs per page; follow "next_cursor" for more
    }
).json()
runs = runs["items"]
for run in runs:
    example_id = run["reference_example_id"]
    example_id_to_runs_map[example_id].append(run)

for example_id, runs in example_id_to_runs_map.items():
    print(f"Example ID: {example_id}")
    # Preferentially rank the outputs, in this case we will always prefer the first output
    # In reality, you can use an LLM to rank the outputs
    feedback_group_id = uuid7()

    # Post a feedback score for each run, with the first run being the preferred one
    # API Reference: https://docs.langchain.com/langsmith/smith-api/feedback/create-feedback
    # We'll use the feedback group ID to associate the feedback scores with the same group
    for i, run in enumerate(runs):
        print(f"Run ID: {run['id']}")
        feedback = {
            "score": 1 if i == 0 else 0,
            "run_id": str(run["id"]),
            "key": "ranked_preference",
            "session_id": run["project_id"],  # Required: the run's tracing project UUID
            "feedback_group_id": str(feedback_group_id),
            "comparative_experiment_id": comparative_experiment_id,
        }
        resp = requests.post(
            "https://api.smith.langchain.com/api/v1/feedback",
            json=feedback,
            headers={"x-api-key": os.environ["LANGSMITH_API_KEY"]}
        )
        resp.raise_for_status()
```

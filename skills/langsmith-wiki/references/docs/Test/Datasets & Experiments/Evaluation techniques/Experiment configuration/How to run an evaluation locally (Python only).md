# How to run an evaluation locally (Python only)

Sometimes it is helpful to run an evaluation locally without uploading any results to LangSmith. For example, if you're quickly iterating on a prompt and want to smoke test it on a few examples, or if you're validating that your target and evaluator functions are defined correctly, you may not want to record these evaluations.

You can do this by using the LangSmith Python SDK and passing `upload_results=False` to `evaluate()` / `aevaluate()`.

This will run you application and evaluators exactly as it always does and return the same output, but nothing will be recorded to LangSmith. This includes not just the experiment results but also the application and evaluator traces.

> [!NOTE]
>
> If you want to upload results to LangSmith but also need to process them in your script (for quality gates, custom aggregations, etc.), refer to [Read experiment results locally](How%20to%20read%20experiment%20results%20locally.md).

## Example

Let's take a look at an example:

Requires `langsmith>=0.2.0`. Example also uses `pandas`.

```python
from langsmith import Client

# 1. Create and/or select your dataset
ls_client = Client()
dataset = ls_client.clone_public_dataset(
    "https://smith.langchain.com/public/a63525f9-bdf2-4512-83e3-077dc9417f96/d"
)

# 2. Define an evaluator
def is_concise(outputs: dict, reference_outputs: dict) -> bool:
    return len(outputs["answer"]) < (3 * len(reference_outputs["answer"]))

# 3. Define the interface to your app
def chatbot(inputs: dict) -> dict:
    return {"answer": inputs["question"] + " is a good question. I don't know the answer."}

# 4. Run an evaluation
experiment = ls_client.evaluate(
    chatbot,
    data=dataset,
    evaluators=[is_concise],
    experiment_prefix="my-first-experiment",
    # 'upload_results' is the relevant arg.
    upload_results=False
)

# 5. Analyze results locally
results = list(experiment)

# Check if 'is_concise' returned False.
failed = [r for r in results if not r["evaluation_results"]["results"][0].score]

# Explore the failed inputs and outputs.
for r in failed:
    print(r["example"].inputs)
    print(r["run"].outputs)

# Explore the results as a Pandas DataFrame.
# Must have 'pandas' installed.
df = experiment.to_pandas()
df[["inputs.question", "outputs.answer", "reference.answer", "feedback.is_concise"]]
```

```python
{'question': 'What is the largest mammal?'}
{'answer': "What is the largest mammal? is a good question. I don't know the answer."}
{'question': 'What do mammals and birds have in common?'}
{'answer': "What do mammals and birds have in common? is a good question. I don't know the answer."}
```

| | inputs.question | outputs.answer | reference.answer | feedback.is\_concise |
| - | - | - | - | - |
| 0 | What is the largest mammal? | What is the largest mammal? is a good question. I don't know the answer. | The blue whale | False |
| 1 | What do mammals and birds have in common? | What do mammals and birds have in common? is a good question. I don't know the answer. | They are both warm-blooded | False |

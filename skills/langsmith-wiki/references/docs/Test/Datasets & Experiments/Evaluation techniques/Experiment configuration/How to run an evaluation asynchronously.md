# How to run an evaluation asynchronously

> [!NOTE]
>
> [Evaluations](../../../Get%20started/Evaluation%20concepts.md#evaluation-lifecycle) | [Evaluators](../../../Get%20started/Evaluation%20concepts.md#evaluators) | [Datasets](../../../Get%20started/Evaluation%20concepts.md#datasets) | [Experiments](../../../Get%20started/Evaluation%20concepts.md#experiment)

We can run evaluations asynchronously via the SDK using [aevaluate()](https://reference.langchain.com/python/langsmith/evaluation/_arunner/aevaluate), which accepts all of the same arguments as [evaluate()](https://reference.langchain.com/python/langsmith/evaluation/_runner/evaluate) but expects the application function to be asynchronous. To learn more, see [how to use the `evaluate()` function](../../Run%20an%20evaluation/How%20to%20evaluate%20agents.md).

> [!NOTE]
>
> This guide is only relevant when using the Python SDK. In JS/TS the `evaluate()` function is already async. For more information, see [Evaluate LLM applications](../../Run%20an%20evaluation/How%20to%20evaluate%20agents.md).

## Use `aevaluate()`

* Python

Requires `langsmith>=0.3.13`

```python
from langsmith import wrappers, Client
from openai import AsyncOpenAI

# Optionally wrap the OpenAI client to trace all model calls.
oai_client = wrappers.wrap_openai(AsyncOpenAI())

# Optionally add the 'traceable' decorator to trace the inputs/outputs of this function.
@traceable
async def researcher_app(inputs: dict) -> str:
    instructions = """You are an excellent researcher. Given a high-level research idea, \
list 5 concrete questions that should be investigated to determine if the idea is worth pursuing."""

    response = await oai_client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": inputs["idea"]},
        ],
    )
    return response.choices[0].message.content

# Evaluator functions can be sync or async
def concise(inputs: dict, outputs: dict) -> bool:
    return len(outputs["output"]) < 3 * len(inputs["idea"])

ls_client = Client()
ideas = [
    "universal basic income",
    "nuclear fusion",
    "hyperloop",
    "nuclear powered rockets",
]
dataset = ls_client.create_dataset("research ideas")
ls_client.create_examples(
    dataset_name=dataset.name,
    examples=[{"inputs": {"idea": i}} for i in ideas],
)

# Can equivalently use the 'aevaluate' function directly:
# from langsmith import aevaluate
# await aevaluate(...)
results = await ls_client.aevaluate(
    researcher_app,
    data=dataset,
    evaluators=[concise],
    # Optional, add concurrency.
    max_concurrency=2,  # Optional, add concurrency.
    experiment_prefix="gpt-5.4-mini-baseline"  # Optional, random by default.
)
```

## Related

* [Run an evaluation (synchronously)](../../Run%20an%20evaluation/How%20to%20evaluate%20agents.md)
* [Handle model rate limits](How%20to%20handle%20model%20rate%20limits.md)

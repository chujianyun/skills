# How to define a code evaluator

Code evaluators in the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-code-evaluator-ui) allow you to write custom evaluation logic using Python or TypeScript code directly in the interface. Unlike [LLM-as-a-judge](How%20to%20define%20an%20LLM-as-a-judge%20evaluator.md) evaluators that use a model to evaluate outputs, code evaluators use deterministic logic you define.

> [!NOTE]
>
> To create a code evaluator that appears in the LangSmith UI programmatically, refer to [Manage evaluators with the SDK](../../Manage%20evaluators%20with%20the%20SDK.md). To define a code evaluator function that you pass to `evaluate()`, refer to [How to define a code evaluator (SDK)](../SDK/How%20to%20define%20a%20code%20evaluator.md). To grade outputs against assertions saved on dataset examples, refer to [Use assertions](../../../Annotation%20Queues/Use%20assertions.md).

## Step 1. Create the evaluator

1. Create an evaluator from one of the following pages in the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-code-evaluator-ui):
   * In the Playground or from a dataset: Select the **+ Evaluator** button.
   * Select **Add rules**, configure your rule and select **Apply evaluator**.
2. Give your evaluator a clear name that describes what it measures (e.g., "Exact Match").
3. Select **Create code evaluator** from the evaluator type options.

## Step 2. Write your evaluator code

> [!NOTE]
>
> **Custom code evaluators restrictions.**
>
> **Allowed Libraries**: You can import all standard library functions, as well as the following public packages:
>
> ```
> numpy (v2.2.2): "numpy"
> pandas (v1.5.2): "pandas"
> jsonschema (v4.21.1): "jsonschema"
> scipy (v1.14.1): "scipy"
> sklearn (v1.26.4): "scikit-learn"
> ```
>
> **Network Access**: You cannot access the internet from a custom code evaluator.

In the **Add Custom Code Evaluator** page, define your evaluation logic using Python or TypeScript.

Your evaluator function must be named `perform_eval` and should:

1. Accept `run` and `example` parameters.
2. Access data via `run['inputs']`, `run['outputs']`, and `example['outputs']`.
3. Return a dictionary where each key is a metric name and each value is the score for that metric. Each key represents a piece of feedback you want to return. For example, `{"correctness": 1, "silliness": 0}` would create two pieces of feedback on the run.

### Function signature

```python
def perform_eval(run, example):
    # Access the data
    inputs = run['inputs']
    outputs = run['outputs']
    reference_outputs = example['outputs']  # Optional: reference/expected outputs

    # Your evaluation logic here
    score = ...

    # Return a dict with your metric name
    return {"metric_name": score}
```

### Example: Exact match evaluator

```python
def perform_eval(run, example):
    """Check if the answer exactly matches the expected answer."""
    actual = run['outputs']['answer']
    expected = example['outputs']['answer']

    is_correct = actual == expected
    return {"exact_match": is_correct}
```

### Example: Input-based evaluator

```python
def perform_eval(run, example):
    """Check if the input text contains toxic language."""
    text = run['inputs'].get('text', '').lower()
    toxic_words = ["idiot", "stupid", "hate", "awful"]

    is_toxic = any(word in text for word in toxic_words)
    return {"is_toxic": is_toxic}
```

## Step 3. Test and save

1. Test your evaluator on example data to ensure it works as expected
2. Click **Save** to make the evaluator available for use

## Use your code evaluator

Once created, you can use your code evaluator:

* When running evaluations from the [Playground](../../../../Deploy/Prompt%20%26%20Context%20Hub/Prompts/Prompt%20engineering%20concepts.md#playground)
* As part of a dataset to [automatically run evaluations on experiments](../../Automatically%20run%20evaluators%20on%20experiments.md)

## Related

* [LLM-as-a-judge evaluator (UI)](How%20to%20define%20an%20LLM-as-a-judge%20evaluator.md): Use an LLM to evaluate outputs
* [Composite evaluators](How%20to%20create%20a%20composite%20evaluator.md): Combine multiple evaluator scores

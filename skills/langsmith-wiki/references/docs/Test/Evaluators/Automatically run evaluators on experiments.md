# Automatically run evaluators on experiments

LangSmith supports two ways to grade experiments created via the SDK:

* **Programmatically**, by specifying evaluators in your code (see [How to evaluate an LLM application](../Datasets%20%26%20Experiments/Run%20an%20evaluation/How%20to%20evaluate%20agents.md) for details)
* By **binding evaluators to a dataset** in the UI. This will automatically run the evaluators on any new experiments created, in addition to any evaluators you've set up via the SDK. This is useful when you're iterating on your application (target function), and have a standard set of evaluators you want to run for all experiments.

## Configuring an evaluator on a dataset

1. In the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-bind-evaluator-to-dataset), select a dataset.
2. Click the **Evaluators** tab.
3. Click **+ Evaluator** to open the **Configure Evaluator** panel.
4. Choose one of the following:
   * **Create from scratch**: Build a new [LLM-as-a-Judge](Evaluator%20types/UI/How%20to%20define%20an%20LLM-as-a-judge%20evaluator.md), [Decision Model](Evaluator%20types/UI/How%20to%20define%20a%20decision%20model%20evaluator.md), [Code](../../Monitor/Observe/Online%20evaluators/Set%20up%20online%20code%20evaluators.md), or [Composite](Evaluator%20types/UI/How%20to%20create%20a%20composite%20evaluator.md) evaluator, or select **From labeled data** to create an LLM-as-a-judge evaluator [aligned to human feedback](Improve%20evaluators/Improve%20LLM-as-judge%20evaluators%20using%20human%20feedback.md).
   * **Attach an existing evaluator**: Select an evaluator already in your workspace to reuse it.
   * **Create from a template**: Start from a ready-made evaluator.

> [!NOTE]
>
> When you configure an evaluator for a dataset, it will only affect the experiment runs that are created after the evaluator is configured. It will not affect the evaluation of experiment runs that were created before the evaluator was configured.

## LLM-as-a-judge evaluators

The process for binding evaluators to a dataset is very similar to the process for configuring an LLM-as-a-judge evaluator in the Playground. View instructions for [configuring an LLM-as-a-judge evaluator in the Playground.](Evaluator%20types/UI/How%20to%20define%20an%20LLM-as-a-judge%20evaluator.md)

## Decision model evaluators

A decision model evaluator uses a decision model, such as Jev, as the judge. On a dataset, you can map the reference output into the evaluator's state and ask questions that compare it to the run's output. For instructions, see [How to define a decision model evaluator](Evaluator%20types/UI/How%20to%20define%20a%20decision%20model%20evaluator.md).

## Custom code evaluators

The process for binding a code evaluators to a dataset is very similar to the process for configuring a code evaluator in online evaluation. View instruction for [configuring code evaluators](../../Monitor/Observe/Online%20evaluators/Set%20up%20online%20code%20evaluators.md).

The only difference between configuring a code evaluator in online evaluation and binding a code evaluator to a dataset is that the custom code evaluator can reference outputs that are part of the dataset's `Example`.

For custom code evaluators bound to a dataset, the evaluator function takes in two arguments:

* A `Run` ([reference](../../Monitor/Debug/Data%20type%20reference/Run%20%28span%29%20data%20format.md)). This represents the new run in your experiment. For example, if you ran an experiment via SDK, this would contain the input/output from your chain or model you are testing.
* An `Example` ([reference](../Datasets%20%26%20Experiments/Common%20data%20types/Example%20data%20format.md)). This represents the reference example in your dataset that the chain or model you are testing uses. The `inputs` to the Run and Example should be the same. If your Example has a reference `outputs`, then you can use this to compare to the run's output for scoring.

The code below shows an example of a simple evaluator function that checks that the outputs exactly equal the reference outputs.

```python Python
import numpy as np

def perform_eval(run, example):
    # run is a Run object
    # example is an Example object
    output = run['outputs']['output']
    ref_output = example['outputs']['outputs']
    output_match = np.array_equal(output, ref_output)

    return { "exact_match": output_match }
```

```javascript JavaScript
function perform_eval(run, example) {
    // run is a Run object
    // example is an Example object
    const output = run.outputs.output;
    const refOutput = example.outputs.outputs;

    // Deep equality check for arrays/objects
    const outputMatch = JSON.stringify(output) === JSON.stringify(refOutput);

    return { "exact_match": outputMatch };
}
```

## Next steps

* Analyze your experiment results in the [experiments tab](../Datasets%20%26%20Experiments/Analyze%20experiment%20results/Analyze%20an%20experiment.md)
* Compare your experiment results in the [comparison view](../Datasets%20%26%20Experiments/Analyze%20experiment%20results/How%20to%20compare%20experiment%20results.md)

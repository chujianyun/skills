# How to define an LLM-as-a-judge evaluator

LLM applications can be challenging to evaluate since they often generate conversational text with no single correct answer.

This guide shows you how to define an [LLM-as-a-judge evaluator](../../../Get%20started/Evaluation%20concepts.md#llm-as-judge) for [offline evaluation](../../../Get%20started/Evaluation%20concepts.md#offline-evaluations) using the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-llm-as-judge).

> [!NOTE]
>
> This guide uses the LangSmith UI. You can also create an LLM-as-a-judge evaluator programmatically with the SDK, and it appears in the LangSmith UI the same as one created here. Refer to [Manage evaluators with the SDK](../../Manage%20evaluators%20with%20the%20SDK.md).
>
> To run evaluations in real-time on your production traces, refer to [setting up online evaluations](../../../../Monitor/Observe/Online%20evaluators/Set%20up%20LLM-as-a-judge%20online%20evaluators.md).

> [!TIP]
>
> If your dataset examples were built with [assertions written in an annotation queue](../../../Annotation%20Queues/Use%20assertions.md), an LLM-as-a-judge evaluator can read `example.outputs["assertions"]` and grade each one against your application's output.

## Step 1. Create the evaluator

1. In the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-llm-as-judge), click **+ Evaluator** from the [Evaluators](../../Manage%20evaluators.md) page, or from the **Evaluators** tab within a dataset or tracing project.
2. In the **Add Evaluator** panel, select **LLM-as-a-Judge Evaluator** under **Create from scratch**. Alternatively, select **Create from a template** to start from a ready-made evaluator and edit it.

### Evaluator templates

Evaluator templates are a useful starting point when setting up evaluations. Select **Create from a template** in the **Add Evaluator** panel to browse templates organized by category, such as Security, Safety, and Quality.

You can configure an LLM-as-a-Judge evaluator:

* From the [Evaluators](../../Manage%20evaluators.md) page
* As part of a dataset to [automatically run evaluations on experiments](../../Automatically%20run%20evaluators%20on%20experiments.md)
* When running an [online evaluation](../../../../Monitor/Observe/Online%20evaluators/Set%20up%20LLM-as-a-judge%20online%20evaluators.md)

### Customize your LLM-as-a-judge evaluator

Add specific instructions for your LLM-as-a-judge evaluator prompt and configure which parts of the input/output/reference output should be passed to the evaluator.

## Step 2. Configure the evaluator

### Prompt

Create a custom prompt inline for your evaluator.

### Model

Select the desired model from the provided options.

To use a decision model as the judge, see [How to define a decision model evaluator](How%20to%20define%20a%20decision%20model%20evaluator.md).

### Mapping variables

Use variable mapping to indicate the variables that are passed into your evaluator prompt from your run or example. To aid with variable mapping, an example (or run) is provided for reference. Click on the variables in your prompt and use the dropdown to map them to the relevant parts of the input, output, or reference output.

To add prompt variables type the variable with double curly brackets `{{prompt_var}}` if using mustache formatting (the default) or single curly brackets `{prompt_var}` if using f-string formatting.

You may remove variables as needed. For example if you are evaluating a metric such as conciseness, you typically don't need a reference output so you may remove that variable.

### Preview

Previewing the prompt will show you of what the formatted prompt will look like using the reference run and dataset example shown on the right.

### Improve your evaluator with few-shot examples

To better align the LLM-as-a-judge evaluator to human preferences, LangSmith allows you to collect [human corrections](../../Improve%20evaluators/How%20to%20improve%20your%20evaluator%20with%20few-shot%20examples.md#make-corrections) on evaluator scores. With this selection enabled, corrections are then inserted automatically as few-shot examples into your prompt.

Learn [how to set up few-shot examples and make corrections](../../Improve%20evaluators/How%20to%20improve%20your%20evaluator%20with%20few-shot%20examples.md).

### Feedback configuration

Feedback configuration is the scoring criteria that your LLM-as-a-judge evaluator will use. Think of this as the rubric that your evaluator will grade based on. Scores will be added as [feedback](../../../../Monitor/Trace/Observability%20concepts.md#feedback) to a run or example. Defining feedback for your evaluator:

1. **Name the feedback key**: This is the name that will appear when viewing evaluation results. Names should be unique across experiments.

2. **Add a description**: Describe what the feedback represents.

3. **Choose a feedback type**:

   * **Boolean**: True/false feedback.
   * **Categorical**: Select from predefined categories.
   * **Continuous**: Numerical scoring within a specified range.

Behind the scenes, feedback configuration is added as [structured output](https://docs.langchain.com/oss/python/langchain/structured-output.md) to the LLM-as-a-judge prompt. Each top-level key in the output schema will be treated as a separate piece of feedback.

## Step 3. Save the evaluator

Once you are finished configuring, save your changes.

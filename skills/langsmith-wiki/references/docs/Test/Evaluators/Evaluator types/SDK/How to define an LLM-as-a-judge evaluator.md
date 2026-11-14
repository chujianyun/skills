# How to define an LLM-as-a-judge evaluator

LLM applications can be challenging to evaluate since they often generate conversational text with no single correct answer.

This guide shows you how to define an [LLM-as-a-judge evaluator](../../../Get%20started/Evaluation%20concepts.md#llm-as-judge) for [offline evaluation](../../../Get%20started/Evaluation%20concepts.md#offline-evaluations) using the [LangSmith SDK](https://reference.langchain.com/python/langsmith/observability/sdk).

> [!TIP]
>
> For a quick start, use [openevals](../../Frameworks%20%26%20integrations/Run%20evals%20with%20openevals%20package.md), which provides ready-to-use LLM-as-a-judge evaluators.

> [!NOTE]
>
> The SDK does not support [decision model evaluators](../UI/How%20to%20define%20a%20decision%20model%20evaluator.md). These evaluators use a decision model, such as Jev, as the judge. To create one, use the UI.

## Create your own LLM-as-a-judge evaluator

For complete control of evaluator logic, create your own LLM-as-a-judge evaluator and run it using the LangSmith SDK ([Python](../../../../Monitor/Reference/langsmith%20%28smith-python-sdk%29.md) / [TypeScript](../../../../Monitor/Reference/langsmith%20%28smith-js-ts-sdk%29.md)).

Requires `langsmith>=0.2.0`

An LLM-as-a-judge evaluator consists of three key components:

1. **Evaluator function**: A function that receives the example inputs and application outputs, then uses an LLM to score the quality. The function should return a boolean, number, string, or dictionary with score information.
2. **Target function**: Your application logic being evaluated (wrapped with [`@traceable`](https://reference.langchain.com/python/langsmith/run_helpers/traceable) for observability).
3. **Dataset and evaluation**: A dataset of test examples and the `evaluate()` function that runs your target function on each example and applies your evaluators.

### Example

```python
from langsmith import evaluate, traceable, wrappers, Client
from openai import OpenAI
from pydantic import BaseModel

# Wrap the OpenAI client to automatically trace all LLM calls
oai_client = wrappers.wrap_openai(OpenAI())

# 1. Define your evaluator function
# This function receives the inputs and outputs from each test example
def valid_reasoning(inputs: dict, outputs: dict) -> bool:
    """Use an LLM to judge if the reasoning and the answer are consistent."""
    # Define the evaluation criteria
    instructions = """
Given the following question, answer, and reasoning, determine if the reasoning
for the answer is logically valid and consistent with the question and the answer."""

    # Use structured output to get a boolean score
    class Response(BaseModel):
        reasoning_is_valid: bool

    # Construct the prompt with the actual inputs and outputs
    msg = f"Question: {inputs['question']}\nAnswer: {outputs['answer']}\nReasoning: {outputs['reasoning']}"

    # Call the LLM to judge the output
    response = oai_client.beta.chat.completions.parse(
        model="gpt-6.1-sol",
        messages=[{"role": "system", "content": instructions}, {"role": "user", "content": msg}],
        response_format=Response
    )

    # Return the boolean score
    return response.choices[0].message.parsed.reasoning_is_valid

# 2. Define your target function (the application being evaluated)
# The @traceable decorator logs traces to LangSmith for debugging
@traceable
def dummy_app(inputs: dict) -> dict:
    return {"answer": "hmm i'm not sure", "reasoning": "i didn't understand the question"}

# 3. Create a dataset with test examples
ls_client = Client()
dataset = ls_client.create_dataset("big questions")
examples = [
    {"inputs": {"question": "how will the universe end"}},
    {"inputs": {"question": "are we alone"}},
]
ls_client.create_examples(dataset_id=dataset.id, examples=examples)

# 4. Run the evaluation
# This runs dummy_app on each example and applies the valid_reasoning evaluator
results = evaluate(
    dummy_app,              # Your application function
    data=dataset,           # Dataset to evaluate on
    evaluators=[valid_reasoning]  # List of evaluator functions
)
```

## Use reference outputs

When your dataset examples include reference outputs (expected answers), you can pass `reference_outputs` as a parameter to your evaluator function. LangSmith automatically provides the example's reference outputs to any evaluator that declares this parameter.

```python Python
from langsmith import evaluate, traceable, wrappers, Client
from openai import OpenAI
from pydantic import BaseModel

# Wrap the OpenAI client to automatically trace all LLM calls
oai_client = wrappers.wrap_openai(OpenAI())

# Define an evaluator that checks the answer against a reference answer
def matches_expected(inputs: dict, outputs: dict, reference_outputs: dict) -> bool:
    """Use an LLM to judge if the actual answer matches the expected answer."""
    instructions = """
Given a question, an expected answer, and an actual answer, determine if the
actual answer is semantically equivalent to the expected answer."""

    class Response(BaseModel):
        answers_match: bool

    msg = (
        f"Question: {inputs['question']}\n"
        f"Expected answer: {reference_outputs['answer']}\n"
        f"Actual answer: {outputs['answer']}"
    )

    response = oai_client.beta.chat.completions.parse(
        model="gpt-6.1-sol",
        messages=[{"role": "system", "content": instructions}, {"role": "user", "content": msg}],
        response_format=Response,
    )

    return response.choices[0].message.parsed.answers_match

@traceable
def my_app(inputs: dict) -> dict:
    # Your application logic here
    return {"answer": "Paris"}

# Create a dataset with reference outputs (expected answers)
ls_client = Client()
dataset = ls_client.create_dataset("geography-qa")
examples = [
    {
        "inputs": {"question": "What is the capital of France?"},
        "outputs": {"answer": "Paris"},
    },
    {
        "inputs": {"question": "What is the capital of Germany?"},
        "outputs": {"answer": "Berlin"},
    },
]
ls_client.create_examples(dataset_id=dataset.id, examples=examples)

results = evaluate(
    my_app,
    data=dataset,
    evaluators=[matches_expected]
)
```

```typescript TypeScript
import { evaluate } from "langsmith/evaluation";
import { Client } from "langsmith";
import OpenAI from "openai";
import { zodResponseFormat } from "openai/helpers/zod";
import { z } from "zod";

const oaiClient = new OpenAI();

const matchesExpected = async ({
  inputs,
  outputs,
  referenceOutputs,
}: {
  inputs: Record<string, any>;
  outputs: Record<string, any>;
  referenceOutputs?: Record<string, any>;
}): Promise<boolean> => {
  const instructions = `Given a question, an expected answer, and an actual answer, determine if the
actual answer is semantically equivalent to the expected answer.`;

  const ResponseSchema = z.object({ answers_match: z.boolean() });

  const msg = `Question: ${inputs.question}\nExpected answer: ${referenceOutputs?.answer}\nActual answer: ${outputs.answer}`;

  const response = await oaiClient.beta.chat.completions.parse({
    model: "gpt-6.1-sol",
    messages: [
      { role: "system", content: instructions },
      { role: "user", content: msg },
    ],
    response_format: zodResponseFormat(ResponseSchema, "response"),
  });

  return response.choices[0].message.parsed?.answers_match ?? false;
};

const myApp = async (inputs: Record<string, any>): Promise<Record<string, any>> => {
  // Your application logic here
  return { answer: "Paris" };
};

// Create a dataset with reference outputs (expected answers)
const lsClient = new Client();
const dataset = await lsClient.createDataset("geography-qa-ts");
await lsClient.createExamples({
  inputs: [
    { question: "What is the capital of France?" },
    { question: "What is the capital of Germany?" },
  ],
  outputs: [{ answer: "Paris" }, { answer: "Berlin" }],
  datasetId: dataset.id,
});

await evaluate(myApp, {
  data: dataset.name,
  evaluators: [matchesExpected],
});
```

For more information on how to write a custom evaluator, refer to [How to define a code evaluator (SDK)](How%20to%20define%20a%20code%20evaluator.md).

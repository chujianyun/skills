# Set up decision model online evaluators

> Evaluate production traces in LangSmith with a decision model as the judge and record each typed answer as feedback.

[Online evaluations](../../../Test/Get%20started/Evaluation%20concepts.md#online-evaluations) provide real-time feedback on your production traces. An online evaluator can use a decision model as the judge in place of an LLM. To use an LLM as the judge, see [Set up LLM-as-a-judge online evaluators](Set%20up%20LLM-as-a-judge%20online%20evaluators.md).

> [!NOTE]
>
> When an online evaluator runs on any run within a trace, LangSmith upgrades the trace to [extended data retention](../../Trace/Configuration%20%26%20troubleshooting/Usage%20and%20billing.md#data-retention-auto-upgrades).

## Decision models

Decision models answer structured questions about text and return typed answers, such as a probability, a selected option, or a score, rather than free-form text. For how they work, see [Decision models in the LLM Gateway](../../../LLM%20Gateway/Call%20the%20gateway/Decision%20models.md). When you use a decision model as the judge, LangSmith records the answer to each question you define under its own feedback key. You do not need to write an output schema or parse free-text reasoning.

### Supported models

LangSmith supports OpenAI and TypeSafe decision models for evaluators, on both tracing projects and datasets. To call a decision model through another provider or on your own server, use an OpenAI-Decisions-compatible or TypeSafe-compatible endpoint. See [Connect to a compatible decision model provider](../../../Deploy/Prompt%20%26%20Context%20Hub/Prompts/Connect%20to%20models/Connect%20to%20a%20compatible%20decision%20model%20provider.md).

| Model | Provider | Setup |
| - | - | - |
| [`gpt-6-luna`](../../../LLM%20Gateway/Call%20the%20gateway/Decision%20models.md#use-openai-decision-models) | **OpenAI** | Requires an OpenAI API key stored as a workspace secret. Defaults to `OPENAI_API_KEY`. |
| [Jev](../../../LLM%20Gateway/Call%20the%20gateway/Decision%20models.md#use-typesafe-jev) | **TypeSafe** | Requires a TypeSafe API key stored as a workspace secret. Defaults to `TYPESAFE_API_KEY`. |

> [!NOTE]
>
> You can create decision model evaluators only in the LangSmith UI. The LangSmith SDKs do not support creating them yet. To call a decision model through the LLM Gateway from your own application, see [Decision models in the LLM Gateway](../../../LLM%20Gateway/Call%20the%20gateway/Decision%20models.md).

### Question types

Each question you add to a decision model evaluator has one of three types. For full definitions, see the [TypeSafe primitives documentation](https://docs.typesafe.ai/primitives) or the [OpenAI Decisions guide](https://developers.openai.com/api/docs/guides/decisions).

* **Predicate** or **Noul**: A continuous boolean. OpenAI models and OpenAI-Decisions-compatible endpoints label this type **Predicate**, and TypeSafe models and TypeSafe-compatible endpoints label it **Noul**. Returns the probability, from 0 to 1, that a statement is true. Values near 1 mean yes, values near 0 mean no, and values near 0.5 mean the model is uncertain. Use it for yes or no checks, such as whether the output contains personally identifiable information. Phrase the instructions as a yes or no question, and optionally describe what true and false mean.
* **Choice**: Picks one option from a fixed, unordered list, such as classifying whether the user is asking a `question`, making a `request`, or neither (`other`). Give each option a name and, unless the name is self-explanatory, a description.
* **Score**: Rates the state along ordered levels, such as how frustrated the user is, from calm to very angry. Define the levels in order, starting at level 0. The score can fall between two levels.

The OpenAI Decisions API has no field for the true and false descriptions of a predicate. For OpenAI models and OpenAI-Decisions-compatible endpoints, LangSmith appends them to the question's instructions.

LangSmith enforces the following limits on decision model questions:

| Limit | Value |
| - | - |
| Options per choice question | 2 to 255 |
| Levels per score question | 2 to 10 |

### Map answers to feedback keys

Each question's name becomes a feedback key on the evaluated run or thread. LangSmith converts each typed answer to feedback as follows:

| Question type | Feedback field | Value |
| - | - | - |
| Predicate or Noul | `score` | A number from 0 to 1 |
| Choice | `value` | The name of the selected option |
| Score | `score` | A number from 0 to the index of the highest level. For example, a question with four levels returns a score from 0 to 3. |

Feedback stores only the score or value. The model's full answer, which includes `probabilities` and `confidence` for choice and score questions, appears in the evaluator's trace. LangSmith records this trace only when you turn on tracing for the evaluator. New evaluators start with tracing turned off. To turn on tracing and open the trace, see [Trace evaluator runs](../../../Test/Evaluators/Manage%20evaluators.md#trace-evaluator-runs). Because each answer is standard feedback, you can filter, chart, and alert on it, and trigger [automations](../Automations/Set%20up%20automation%20rules.md) from it, as you would with any other evaluator's feedback.

Question names follow the same limits as other feedback keys and must be unique within the evaluator.

## Add a decision model online evaluator

Decision model evaluators require a LangSmith Plus or Enterprise [plan](https://docs.langchain.com/langsmith/pricing-plans.md). They are not available on [BYOC](../../../LangSmith%20setup/BYOC/Bring%20Your%20Own%20Cloud%20%28BYOC%29.md) deployments.

To add a decision model online evaluator:

1. In the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-online-evaluations-decision-models), navigate to the **Tracing** page and select a tracing project.
2. Click the **Evaluators** tab.
3. Click **+ Evaluator** to open the **Configure Evaluator** panel.
4. Under **Create from scratch**, select **Decision Model Evaluator**, then name your evaluator.
5. Select a decision model, map run or thread variables into the **State**, and add questions. For each setting, see [How to define a decision model evaluator](../../../Test/Evaluators/Evaluator%20types/UI/How%20to%20define%20a%20decision%20model%20evaluator.md).
6. (Optional) Apply a [filter](Set%20up%20LLM-as-a-judge%20online%20evaluators.md#apply-a-filter-to-runs-that-trigger-the-evaluator), set a [sampling rate](Set%20up%20LLM-as-a-judge%20online%20evaluators.md#configure-a-sampling-rate), or [apply the rule to past runs or threads](Set%20up%20LLM-as-a-judge%20online%20evaluators.md#apply-a-rule-to-past-runs-or-threads). These settings work the same way as for LLM-as-a-judge online evaluators.
7. To save the evaluator, click **Create** or **Save**.

The evaluator checks each new run or thread that matches its filter. Each question's answer appears under its own feedback key.

## See also

* [How to define a decision model evaluator](../../../Test/Evaluators/Evaluator%20types/UI/How%20to%20define%20a%20decision%20model%20evaluator.md): Configure the model, state, and questions.
* [Connect to a compatible decision model provider](../../../Deploy/Prompt%20%26%20Context%20Hub/Prompts/Connect%20to%20models/Connect%20to%20a%20compatible%20decision%20model%20provider.md): Base URL format and example endpoints.
* [Decision models in the LLM Gateway](../../../LLM%20Gateway/Call%20the%20gateway/Decision%20models.md): Call decision models through the LLM Gateway from your own application.

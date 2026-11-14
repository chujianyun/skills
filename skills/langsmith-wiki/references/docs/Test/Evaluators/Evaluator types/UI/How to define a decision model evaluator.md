# How to define a decision model evaluator

> Set up a LangSmith evaluator that uses a decision model as the judge with questions that each return typed feedback.

A decision model evaluator uses a [decision model](../../../../Monitor/Observe/Online%20evaluators/Set%20up%20decision%20model%20online%20evaluators.md#decision-models) as the judge. Each question you define returns a typed answer that LangSmith records under its own feedback key.

This guide shows you how to define a decision model evaluator in the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-decision-model-evaluator) or [with the API](#create-the-evaluator-with-the-api). You can use it on a dataset to [automatically run evaluations on experiments](../../Automatically%20run%20evaluators%20on%20experiments.md), or on a tracing project as an [online evaluator](../../../../Monitor/Observe/Online%20evaluators/Set%20up%20decision%20model%20online%20evaluators.md). To use an LLM as the judge instead, see [How to define an LLM-as-a-judge evaluator](How%20to%20define%20an%20LLM-as-a-judge%20evaluator.md).

> [!NOTE]
>
> You can create decision model evaluators in the LangSmith UI or with the [LangSmith REST API](#create-the-evaluator-with-the-api). The LangSmith SDKs do not support creating them yet.

> [!NOTE]
>
> Decision model evaluators require a LangSmith Plus or Enterprise [plan](https://docs.langchain.com/langsmith/pricing-plans.md). They are not available on [BYOC](../../../../LangSmith%20setup/BYOC/Bring%20Your%20Own%20Cloud%20%28BYOC%29.md) deployments.

## Step 1. Create the evaluator

A decision model evaluator offers only decision model providers, and an LLM-as-a-judge evaluator offers only LLM providers. To switch between an LLM judge and a decision model, create a new evaluator.

To create a decision model evaluator:

1. Add an API key for your decision model provider. In LangSmith, go to **Settings > Integrations > Provider secrets** and click **+ Secret**:

   * For OpenAI, select **OpenAI** and paste your OpenAI API key. LangSmith stores it as the workspace secret `OPENAI_API_KEY`.
   * For TypeSafe, select **TypeSafe** and paste a key from your TypeSafe account. LangSmith stores it as the workspace secret `TYPESAFE_API_KEY`.

   To store a key under a different name, select **Custom** and enter your own secret name. For more information, see [Add a provider key](../../../../LLM%20Gateway/Authentication/Provider%20authentication.md#add-a-provider-key).
2. In the LangSmith UI, open the **Evaluators** tab of a dataset or tracing project and click **+ Evaluator**.
3. In the **Configure Evaluator** panel, select **Decision Model Evaluator** under **Create from scratch**.
4. Name your evaluator.

## Step 2. Configure the evaluator

Decision model evaluators support OpenAI and TypeSafe decision models with bring-your-own-key (BYOK). You define the state and questions in the evaluator itself. Decision model evaluators cannot load a prompt from the [Prompt Hub](../../../../Deploy/Prompt%20%26%20Context%20Hub/Prompt%20%26%20Context%20Hub.md#prompts) or use a custom output schema. They also do not support [few-shot examples](../../Improve%20evaluators/How%20to%20improve%20your%20evaluator%20with%20few-shot%20examples.md). To reuse a decision model evaluator on another dataset or tracing project, select **Attach an existing evaluator** in the **Configure Evaluator** panel.

### Model

Under **Prompt & Model**, open **Model Configuration** and select a provider and model:

* For OpenAI, select **OpenAI** as the provider, then select a decision model. If you stored your key under a name other than `OPENAI_API_KEY`, enter that name in **API Key Name**. Click **Apply**.
* For TypeSafe, select **TypeSafe** as the provider, then select a Jev model. If you stored your key under a name other than `TYPESAFE_API_KEY`, enter that name in **API Key Name**. Click **Apply**.
* For an OpenAI-Decisions-compatible endpoint or a TypeSafe-compatible endpoint, select its saved configuration. See [Use a compatible endpoint](#use-a-compatible-endpoint).

> [!TIP]
>
> If a trace is too large for Jev's context limit, open the Jev model configuration and add the `TypeSafe-Danger-Zone-Long-Context` header with the value `true` under **Extra Headers**. The header raises the context limit for each request. For the limits with and without the header, see [Long context](https://docs.typesafe.ai/models#long-context) in the TypeSafe docs.

For the supported models, see [Supported models](../../../../Monitor/Observe/Online%20evaluators/Set%20up%20decision%20model%20online%20evaluators.md#supported-models).

#### Use a compatible endpoint

A compatible endpoint points the evaluator at any server that implements the [OpenAI Decisions API](https://developers.openai.com/api/docs/guides/decisions) or the [TypeSafe System One API](https://docs.typesafe.ai). Examples include OpenRouter or a decision model you host yourself. An evaluator can use one only after you save it as a model configuration. For the settings, setup steps, and example base URLs, see [Connect to a compatible decision model provider](../../../../Deploy/Prompt%20%26%20Context%20Hub/Prompts/Connect%20to%20models/Connect%20to%20a%20compatible%20decision%20model%20provider.md).

### State

The **State** is the context the decision model evaluates. Map variables from your run or example into it:

* On a dataset, map the input, output, or reference output.
* On a tracing project, map run or thread variables, such as the run's inputs and outputs.

Unlike a prompt for an LLM judge, the state should not include grading instructions. Put grading criteria in the questions instead.

Decision models evaluate text only. If the state includes multimodal content, such as images, the evaluator run fails.

### Questions

Questions are the scoring criteria your decision model evaluator uses. Each question's name becomes a feedback key on the evaluated run or thread. To define questions:

1. Under **Feedback Configuration**, add one question for each criterion you want to evaluate.
2. For each question, enter a **Name**, select a **Type**, and write the **Instructions**. The yes or no question type is labeled **Predicate** for OpenAI models and OpenAI-Decisions-compatible endpoints, and **Noul** for TypeSafe models and TypeSafe-compatible endpoints.
3. Define the true and false meanings, options, or levels for the question type.

To edit the questions as JSON, click **Advanced**.

For what each question type returns and how answers map to feedback, see [Question types](../../../../Monitor/Observe/Online%20evaluators/Set%20up%20decision%20model%20online%20evaluators.md#question-types) and [Map answers to feedback keys](../../../../Monitor/Observe/Online%20evaluators/Set%20up%20decision%20model%20online%20evaluators.md#map-answers-to-feedback-keys).

## Step 3. Save the evaluator

To save the evaluator, click **Create** or **Save**.

On a dataset, the evaluator runs on each new experiment. On a tracing project, it evaluates incoming runs or threads that match its filter. For filters, sampling rates, and backfills, see [Set up decision model online evaluators](../../../../Monitor/Observe/Online%20evaluators/Set%20up%20decision%20model%20online%20evaluators.md).

## Create the evaluator with the API

To create a decision model evaluator and attach it to a dataset or tracing project in one request, send a `POST` request to the `/api/v1/runs/rules/decision-models` endpoint. The endpoint supports Jev, SemIf, and OpenAI decision models. Each question's key becomes a feedback key.

Before you send the request, add your provider's API key as a workspace secret, as described in [Step 1](#step-1-create-the-evaluator).

The following request creates a Jev evaluator on a dataset. Set `LANGSMITH_API_KEY` to your LangSmith API key and `LANGSMITH_WORKSPACE_ID` to the ID of the workspace that contains the dataset, and replace `<your-dataset-id>` with the ID of the dataset to evaluate:

```bash
curl -X POST 'https://api.smith.langchain.com/api/v1/runs/rules/decision-models' \
  -H 'Content-Type: application/json' \
  -H "X-API-Key: $LANGSMITH_API_KEY" \
  -H "X-Tenant-Id: $LANGSMITH_WORKSPACE_ID" \
  -d '{
    "display_name": "answer-quality",
    "dataset_id": "<your-dataset-id>",
    "prompt": [["human", "Question: {{input}}\nAnswer: {{output}}"]],
    "variable_mapping": {"input": "input", "output": "output"},
    "provider": "typesafe",
    "model": "jev-latest",
    "questions": {
      "helpful": {
        "type": "noul",
        "instructions": "Does the answer address the question?",
        "yes": "It answers the question",
        "no": "It does not"
      },
      "tone": {
        "type": "choice",
        "instructions": "What is the tone of the answer?",
        "options": ["formal", "casual"]
      },
      "quality": {
        "type": "score",
        "instructions": "Rate the overall quality of the answer.",
        "levels": ["poor", "ok", "great"]
      }
    }
  }'
```

The request body accepts the following fields:

* **`display_name`**: The evaluator name. Required.
* **`dataset_id`** or **`session_id`**: The dataset whose experiments to evaluate, or the tracing project whose runs to evaluate.
* **`prompt`**: The [state](#state) the decision model reads, as a list of `[role, template]` pairs. Required.
* **`template_format`**: `mustache` (the default) or `f-string`.
* **`variable_mapping`**: Maps each prompt variable to a run or example field, such as `input` or `output`. Map every variable in the prompt. The API accepts a request without a mapping, but the LangSmith UI cannot test or save the evaluator until each variable is mapped.
* **`questions`**: The [questions](#questions), keyed by feedback key, in the order to ask them. Required. Each question has a `type` and `instructions`:
  * **`noul`**: A yes or no question scored 0 to 1. Optionally set both `yes` and `no` to describe what each answer means.
  * **`choice`**: One of 2 to 255 `options`, given as a list of names or as names mapped to descriptions.
  * **`score`**: One of 2 to 10 `levels`, listed lowest first and scored by position.
* **`provider`**: `typesafe` (the default) for Jev and SemIf, `typesafe_compatible` for a TypeSafe-compatible endpoint, or `openai_decisions`.
* **`model`**: Defaults to `jev-latest` for `typesafe` and `gpt-6-luna` for `openai_decisions`. For SemIf, use `semif-qwen3.5-4b`.
* **`base_url`**: The model endpoint to call directly instead of through the LangSmith gateway, using the workspace's `TYPESAFE_API_KEY` or `OPENAI_API_KEY` secret. Required for `typesafe_compatible`.
* **`model_headers`**: Headers sent with each model call, such as `TypeSafe-Danger-Zone-Long-Context`. LangSmith saves them in the evaluator's prompt as given, so do not put API keys in them.
* **`timeout_seconds`**: Seconds to wait for each model call. Applies only to `openai_decisions`.
* **`max_retries`**: How many times to retry a failed model call. Applies only to `openai_decisions`.

For the full schema, including sampling rates, filters, and saved model configurations, see [Create decision model rule](../../../../Monitor/Reference/LangSmith%20REST%20API/Tracing/Create%20decision%20model%20rule.md) in the API reference.

## See also

* [Decision models](../../../../Monitor/Observe/Online%20evaluators/Set%20up%20decision%20model%20online%20evaluators.md#decision-models): Supported models, question types, and feedback keys.
* [Connect to a compatible decision model provider](../../../../Deploy/Prompt%20%26%20Context%20Hub/Prompts/Connect%20to%20models/Connect%20to%20a%20compatible%20decision%20model%20provider.md): Base URL format and example endpoints.
* [Decision models in the LLM Gateway](../../../../LLM%20Gateway/Call%20the%20gateway/Decision%20models.md): Call decision models through the LLM Gateway from your own application.

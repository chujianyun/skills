# Manage evaluators

> View and manage evaluators at the workspace level in LangSmith.

[Evaluators](../Get%20started/Evaluation%20concepts.md#evaluators) in LangSmith are [workspace-level](../../LangSmith%20setup/Govern/Organization/Overview.md#workspaces) resources. You can attach a single evaluator to multiple [trace containers](../../Monitor/Trace/Observability%20concepts.md#trace-containers) and [datasets](../Get%20started/Evaluation%20concepts.md#datasets), so you can apply consistent evaluation logic across your work without recreating it each time.

What an evaluator attaches to depends on how your workspace is organized.

> [!NOTE]
>
> **Agent-based workspaces.** This section applies if your workspace organizes traces by [agent and environment](../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20Registry.md). To check, look at the control at the top left: it names your workspace. If it shows the LangSmith logo instead, and the sidebar has an **Application** section with an application picker, your workspace is project-based. Skip this section and read [Tracing projects](../../Monitor/Trace/Observability%20concepts.md#tracing-projects).

An evaluator attaches to an [environment](../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20environments.md#environment-names) of an [agent](../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20Registry.md#agent). Attach it to **Production** alone to score production traffic without also scoring local runs.

> [!NOTE]
>
> **Project-based workspaces.** This section applies if your workspace organizes traces by [tracing project](../../Monitor/Trace/Observability%20concepts.md#tracing-projects). To check, look at the control at the top left. In a project-based workspace, it shows the LangSmith logo, and the sidebar has an **Application** section with an application picker. If the control shows your workspace name instead, your workspace is agent-based. Skip this section and read [Agent Registry](../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20Registry.md).

An evaluator attaches to a [tracing project](../../Monitor/Trace/Observability%20concepts.md#tracing-projects).

> [!TIP]
>
> Evaluator scores are a high-priority signal for the [LangSmith Engine](../../Engine/LangSmith%20Engine.md): it pulls low-scoring traces when choosing what to analyze, so attaching an evaluator to a project sharpens the issues Engine finds there.

## View evaluators

In the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-evaluators), select **Evaluators** in the left sidebar to view all evaluators in your workspace.

The evaluators table shows the following columns:

| Column | Description |
| - | - |
| Name | The evaluator name |
| Type | **LLM as a judge** or **Code**. Composite score evaluators are scoped to individual tracing projects and datasets and do not appear here. |
| Feedback Key | The feedback key the evaluator produces |
| Environments & Datasets | Agent environments and datasets this evaluator is attached to. In [self-hosted](../../LangSmith%20setup/Self-hosted/Self-hosted%20LangSmith.md) deployments, this column is **Projects & Datasets** and lists tracing projects and datasets. |
| Evaluator Trace Count (this week) | Number of traces this evaluator ran on in the past week. Only shown when spend tracking is enabled; **–** for Code evaluators or evaluators with no attached rules. |
| Spend (this week) | Estimated USD spend for this evaluator in the past week. Only shown when spend tracking is enabled; **–** for Code evaluators or evaluators with no attached rules. |
| Spend Status | Whether the evaluator is **Under limits**, **Unlimited**, or has hit one or more configured spend limits. Only shown when spend tracking is enabled; **–** for Code evaluators. |
| Created By | The workspace member who created the evaluator |
| Updated At | When the evaluator was last modified |
| Created At | When the evaluator was created |

## Create an evaluator

You can create an evaluator in the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-evaluators) or programmatically with the [SDK](#create-an-evaluator-with-the-sdk). Evaluators created either way are workspace-level resources that appear in the **Evaluators** table.

### Create an evaluator in the UI

1. In the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-evaluators), select **Evaluators** in the left sidebar.
2. Click **+ Evaluator** to open the new evaluator panel.
3. The panel lets you:
   * **Create from scratch**: Build a new [LLM-as-a-Judge](Evaluator%20types/UI/How%20to%20define%20an%20LLM-as-a-judge%20evaluator.md), [Decision Model](Evaluator%20types/UI/How%20to%20define%20a%20decision%20model%20evaluator.md), or [Code](../../Monitor/Observe/Online%20evaluators/Set%20up%20online%20code%20evaluators.md) evaluator.
   * **Add a LangChain Tuned Evaluator**: Attach a [specialized judge managed by LangChain](../../Monitor/Observe/Online%20evaluators/Set%20up%20LangChain%20Tuned%20Evaluators.md) to a compatible tracing project without configuring a prompt, model, or API key.
   * **Create from a template**: Start from a ready-made evaluator (also known as a prebuilt evaluator) for common evaluation patterns. A **Recommended** section lists popular templates first. The rest are grouped by category: Security, Safety, Quality, Conversation, Trajectory, Image Evaluations, and Voice Evaluation. For what each template scores, see [Prebuilt evaluator templates](#prebuilt-evaluator-templates).

You can also add an evaluator directly from a [tracing project](../../Monitor/Trace/Observability%20concepts.md#tracing-projects), an agent environment, or a [dataset](../Get%20started/Evaluation%20concepts.md#datasets). In that flow, you can additionally **attach an existing evaluator** from your workspace, or create a [Composite](Evaluator%20types/UI/How%20to%20create%20a%20composite%20evaluator.md) evaluator. Refer to [Set up LLM-as-a-judge online evaluators](../../Monitor/Observe/Online%20evaluators/Set%20up%20LLM-as-a-judge%20online%20evaluators.md) and [Automatically run evaluators on experiments](Automatically%20run%20evaluators%20on%20experiments.md).

### Create an evaluator with the SDK

Use the LangSmith SDK to create evaluators programmatically. The SDK is available for [Python](../../Monitor/Reference/langsmith%20%28smith-python-sdk%29.md) and [TypeScript](../../Monitor/Reference/langsmith%20%28smith-js-ts-sdk%29.md). Evaluators created through the SDK appear in the **Evaluators** table alongside those created in the UI.

The SDK does not support [decision model evaluators](Evaluator%20types/UI/How%20to%20define%20a%20decision%20model%20evaluator.md) yet. To create one, use the UI.

> [!NOTE]
>
> Managing evaluators through the SDK requires `langsmith>=0.9.8` (Python, PyPI) or `langsmith>=0.7.16` (TypeScript, npm).

```python Python
import asyncio

from langsmith import Client


async def main():
    client = Client()

    created = await client.evaluators.create(
        name="Correctness evaluator",
        type="code",
        code_evaluator={
            "code": "def perform_eval(run, example):\n    return {'score': 1}",
            "language": "python",
        },
    )
    print("Created evaluator:", created.evaluator.id)


asyncio.run(main())
```

```typescript TypeScript
import { Client } from "langsmith";

const client = new Client();

const created = await client.evaluators.create({
  name: "Correctness evaluator",
  type: "code",
  code_evaluator: {
    code: "def perform_eval(run, example):\n    return {'score': 1}",
    language: "python",
  },
});
console.log("Created evaluator:", created.evaluator?.id);
```

To create an LLM-as-a-judge evaluator and to retrieve, update, list, or delete evaluators, refer to [Manage evaluators with the SDK](Manage%20evaluators%20with%20the%20SDK.md).

## Prebuilt evaluator templates

Prebuilt evaluator templates are ready-made evaluators for common checks, such as hallucination, prompt injection, and task completion. Each template is a starting point. You can edit its prompt and scoring schema before you save it to your workspace.

Most templates are [LLM-as-a-judge](Evaluator%20types/UI/How%20to%20define%20an%20LLM-as-a-judge%20evaluator.md) evaluators whose prompts come from the open-source [openevals](https://github.com/langchain-ai/openevals) package. Two are exceptions: Assertions uses a prompt defined in LangSmith, and Exact Match is a [code evaluator](../../Monitor/Observe/Online%20evaluators/Set%20up%20online%20code%20evaluators.md).

Each LLM-as-a-judge template writes a score under its feedback key and a `comment` with the judge's reasoning. Language and Support Intent return a label without a `comment`.

A `true` score does not always mean a pass. Templates that detect a problem return `true` when they find it: the Security and Safety templates, Hallucination, Perceived Error, the Image templates, and Audio Quality. The rest return `true` when the output passes. The **Score** column in each table states what `true` means.

Templates differ in the data they read:

* **Whole threads**: Conversation and Trajectory templates read every message in a thread. When you add one to a tracing project, LangSmith configures it as a thread-level evaluator. For more information, see [Set up multi-turn online evaluators](../../Monitor/Observe/Online%20evaluators/Set%20up%20multi-turn%20online%20evaluators.md).
* **Reference outputs**: Correctness, Assertions, and Exact Match compare the output against a reference output, which comes from a [dataset](../Get%20started/Evaluation%20concepts.md#datasets) example.
* **Plan**: Plan Adherence reads a `plan` variable in addition to the thread messages.
* **Attachments**: Image and Voice templates read the run's attachments. For more information, see [Evaluate with attachments](../Datasets%20%26%20Experiments/Evaluation%20techniques/Multimodal%20evaluations/Run%20an%20evaluation%20with%20multimodal%20content.md).

### Security

Security templates detect leaks, injections, and adversarial inputs.

| Template | What it scores | Score |
| - | - | - |
| PII Leakage | Whether the input or output contains personal information that could identify or harm an individual. | `pii_leakage` (boolean): `true` when PII is found. |
| Prompt Injection | Whether the input contains embedded instructions that target the AI system. Reads the input only. | `prompt_injection` (boolean): `true` when an injection attempt is found. |
| Code Injection | Whether the input contains executable code embedded in data. Reads the input only. | `code_injection` (boolean): `true` when an injection attempt is found. |

### Safety

Safety templates evaluate content safety and moderation.

| Template | What it scores | Score |
| - | - | - |
| Toxicity | Whether the content contains toxic elements, such as personal attacks or hate speech. | `toxicity` (boolean): `true` when toxic content is found. |
| Bias & Fairness | Whether the content contains stereotyping, exclusionary language, or discriminatory framing. | `fairness` (boolean): `true` when bias or a fairness violation is found. |

### Quality

Quality templates measure output quality and accuracy.

| Template | What it scores | Score |
| - | - | - |
| Hallucination | Whether the output contains claims the input context does not support, such as contradictions, speculative details, or inaccurate facts. | `hallucination` (boolean): `true` when the output contains a hallucination. |
| Correctness | Whether the output is factually accurate, complete, and consistent with the reference output. | `correctness` (boolean): `true` when the output is correct. |
| Assertions | Whether the output satisfies each assertion in the reference output. The judge reads an `assertions` list from the reference output, where each entry has a `key` and a `comment`. A missing or empty list scores `false`. | `assertions_passed` (boolean): `true` only when every assertion passes. |
| Conciseness | How efficiently the output conveys the requested information, penalizing hedging, pleasantries, meta-commentary, and redundancy. | `conciseness` (number, 0 to 10): `10` when the output contains only essential information. |
| Code Checker | Whether the code solves every requirement in the input, handles edge cases, and would run without errors. | `code_checker` (boolean): `true` when the code is complete and correct. |
| Answer Relevance | Whether the output directly addresses the input question without off-topic tangents. | `answer_relevance` (boolean): `true` when the output is relevant. |
| Exact Match | Whether the run's outputs exactly equal the reference outputs. This template runs as code and makes no LLM call. | `exact_match` (boolean): `true` when the outputs match. |

### Conversation

Conversation templates evaluate conversational quality and user experience across a whole thread.

| Template | What it scores | Score |
| - | - | - |
| Perceived Error | Whether user signals, such as frustration or repeated corrections, show the user perceived the agent making an error. | `perceived_error` (boolean): `true` when the user perceived an error that caused significant frustration. |
| Language | The primary language of the conversation. | `language` (string): a language name in English, such as `Spanish`. |
| Support Intent | The primary intent of a support conversation. | `intent` (category): one of `Account & Billing`, `Order Management`, `Technical Support`, `Product Inquiry`, `Policy Inquiry`, `Status Check`, `Complaint & Feedback`, `Escalation`, or `Other`. |
| User Satisfaction | Whether the user's tone and satisfaction indicators show the user was satisfied. | `user_satisfaction` (boolean): `true` when the user appears satisfied. |
| Tone | Whether the agent's tone was appropriate for the context and consistent. | `agent_tone` (boolean): `true` when the tone was appropriate. |
| Task Completion | Whether the agent fully completed every user request in the conversation. | `task_completion` (boolean): `true` when every request was completed. |
| Knowledge Retention | Whether the agent retained and applied facts from earlier in the conversation, without contradictions or ignored context. | `knowledge_retention` (boolean): `true` when the agent retained earlier facts. |

### Trajectory

Trajectory templates evaluate agent tool use and decision paths across a whole thread.

| Template | What it scores | Score |
| - | - | - |
| Plan Adherence | Whether the agent's steps followed its declared plan. | `plan_adherence` (boolean): `true` when the agent followed the plan. |
| Tool Selection | Whether the agent chose the right tools, in a sensible order, without unnecessary calls. | `tool_selection` (boolean): `true` when tool selection was accurate and efficient. |
| Trajectory Accuracy | Whether the agent's path was logical, showed clear progress, and was reasonably efficient. | `trajectory_accuracy` (boolean): `true` when the trajectory was accurate and efficient. |

### Image Evaluations

Image templates evaluate image content quality and safety.

| Template | What it scores | Score |
| - | - | - |
| Explicit Content | Whether an image contains nudity, sexual content, or graphic violence. | `explicit_content` (boolean): `true` when explicit content is found. |
| Sensitive Imagery | Whether an image contains harmful, offensive, or inappropriate symbols or depictions. | `sensitive_imagery` (boolean): `true` when sensitive imagery is found. |

### Voice Evaluation

Voice templates evaluate voice and audio interaction quality.

| Template | What it scores | Score |
| - | - | - |
| Audio Quality | Whether the audio contains clipping, distortion, or glitches that degrade the listening experience. | `audio_quality` (boolean): `true` when quality issues are found. |
| Transcription Accuracy | Whether a speech-to-text transcription accurately reflects the spoken content. | `transcription_accuracy` (boolean): `true` when the transcription is accurate. |
| User Interrupts | Whether the agent handled user interruptions gracefully. | `user_interrupts` (boolean): `true` when interruptions were handled gracefully. |
| Vocal Affect | Whether the agent's vocal warmth, prosody, and emotional tone were appropriate and natural. | `vocal_affect` (boolean): `true` when vocal affect was appropriate. |

## View evaluator details

Click any evaluator in the table to open its detail view. The detail view has three tabs:

* **Overview**: The evaluator's feedback configuration and prompt or code definition.
* **Traces**: The evaluator's own runs across all attached resources, recorded when [tracing is turned on](#trace-evaluator-runs). This tab does not appear for [LangChain Tuned Evaluators](../../Monitor/Observe/Online%20evaluators/Set%20up%20LangChain%20Tuned%20Evaluators.md).
* **Environments & Datasets** (**Projects & Datasets** in self-hosted deployments): The agent environments, tracing projects, and datasets this evaluator is attached to, with each attachment's [weekly spend and limit](Track%20and%20limit%20evaluator%20spend.md). Click **Logs** on a row to view the evaluator's execution logs for that attachment.

## Edit an evaluator

Open an evaluator. In the **Overview** tab, click the **Edit evaluator**  icon to open the **Configure Evaluator** panel. Update the evaluator's configuration. Click **Save**.

Because the evaluator is shared, changes apply across every trace container and dataset it is attached to.

## Trace evaluator runs

Evaluator tracing records each evaluator run as a trace, so you can inspect what the evaluator received and returned when you debug its scores. New evaluators start with tracing turned off. Existing evaluators keep their current setting.

To turn on tracing for an evaluator:

1. When you [create](#create-an-evaluator) or [edit](#edit-an-evaluator) an evaluator, expand the **Advanced** section in the evaluator configuration panel.
2. Turn on **Trace Evaluator Runs**.
3. Click **Save**.

The setting applies to the tracing project, agent environment, or dataset you configure the evaluator on. It is not available for [LangChain Tuned Evaluators](../../Monitor/Observe/Online%20evaluators/Set%20up%20LangChain%20Tuned%20Evaluators.md).

To open an evaluator's traces on a tracing project, go to the **Evaluators** tab, click the evaluator, and click the **Traces** tab. In an experiment, hover over a score and click **Evaluator trace**.

### Turn on tracing with the REST API

In the [LangSmith REST API](https://docs.langchain.com/langsmith/smith-api), each attachment of an evaluator is a rule, and the setting is the rule's `is_tracing_disabled` field. The field defaults to `true`. To turn on tracing, set `is_tracing_disabled` to `false` when you [create a rule](../../Monitor/Reference/LangSmith%20REST%20API/Tracing/Create%20rule.md). The [create evaluator](../../Monitor/Reference/LangSmith%20REST%20API/Evaluation/Create%20evaluator.md) endpoint defines an evaluator without attaching it, so it has no tracing setting. The [create decision model rule](../../Monitor/Reference/LangSmith%20REST%20API/Tracing/Create%20decision%20model%20rule.md) endpoint does not accept `is_tracing_disabled`, so its rules start with tracing turned off.

To turn on tracing for an existing rule, get it with [list rules](../../Monitor/Reference/LangSmith%20REST%20API/Tracing/List%20rules.md), set `is_tracing_disabled` to `false`, and send the complete rule back with [update rule](../../Monitor/Reference/LangSmith%20REST%20API/Tracing/Update%20rule.md). Update rule replaces fields you leave out, such as the filter and the evaluator.

## Manage evaluator trace retention

When an online evaluator scores a trace, it attaches feedback to the trace. This can auto-upgrade the trace to [extended retention](../../Monitor/Trace/Configuration%20%26%20troubleshooting/Usage%20and%20billing.md#data-retention-auto-upgrades), depending on the evaluator's retention setting. When you set up an online evaluator on a [tracing project](../../Monitor/Trace/Observability%20concepts.md#tracing-projects), or on an agent environment, you can opt out of this upgrade so that scored traces stay at the base retention.

This control is available only when the project's [default retention](../../LangSmith%20setup/Account/Billing%20%26%20usage/Manage%20billing%20in%20your%20account.md#change-project-level-default-retention) is the [base tier](../../Monitor/Trace/Configuration%20%26%20troubleshooting/Usage%20and%20billing.md#how-it-works). If the project defaults to extended retention ([set at the project or workspace level](../../LangSmith%20setup/Govern/Data%20%26%20compliance/Data%20purging%20for%20compliance.md#data-retention)), traces scored by the evaluator follow that default and the option is locked.

To opt out of extending retention for scored traces:

1. When you [create](#create-an-evaluator) or [edit](#edit-an-evaluator) an online evaluator, set the source to a [tracing project](../../Monitor/Trace/Observability%20concepts.md#tracing-projects) or an agent environment, rather than a [dataset](../Get%20started/Evaluation%20concepts.md#datasets).
2. Expand the **Advanced** section in the evaluator configuration panel.
3. Clear **Extend trace retention**.

The change applies to traces scored after you save the evaluator. Existing scored traces keep their current retention tier.

The **Extend trace retention** toggle described above applies to both trace-level and thread-level (multi-turn) online evaluators. For more information on multi-turn evaluators, see [Set up multi-turn online evaluators](../../Monitor/Observe/Online%20evaluators/Set%20up%20multi-turn%20online%20evaluators.md).

## Include extended stats

Use **Include extended stats (feedback, costs, tokens)** in a [run-level evaluator](../../Monitor/Observe/Online%20evaluators/Set%20up%20LLM-as-a-judge%20online%20evaluators.md) to evaluate feedback statistics, token usage, or cost data from the run. The `feedback_stats` field contains feedback statistics, including the number and average for each feedback key. This option is not available for [multi-turn (thread-level) evaluators](../../Monitor/Observe/Online%20evaluators/Set%20up%20multi-turn%20online%20evaluators.md).

LangSmith fetches additional data for evaluators with this option enabled. Enable it only when your evaluation logic or prompt requires these fields.

To include extended stats:

1. When you [create](#create-an-evaluator) or [edit](#edit-an-evaluator) a run-level evaluator, expand the **Advanced** section in the evaluator configuration panel.
2. Select **Include extended stats (feedback, costs, tokens)**.

### Access extended stats

[Code evaluators](../../Monitor/Observe/Online%20evaluators/Set%20up%20online%20code%20evaluators.md) receive these fields in the `run` object, including `feedback_stats`, `total_tokens`, and `total_cost`. They also receive [individual feedback records](../../Monitor/Debug/Data%20type%20reference/Feedback%20data%20format.md) in `run["feedback"]`, regardless of whether you enable extended stats. For [LLM-as-a-judge evaluators](../../Monitor/Observe/Online%20evaluators/Set%20up%20LLM-as-a-judge%20online%20evaluators.md), map the corresponding `run.*` field to a prompt variable. For example, map `{{correctness_average}}` to `run.feedback_stats.correctness.avg` to include a `correctness` feedback average in the prompt. The available `run.*` fields also include prompt and completion token, cost, and detail fields. For the full run data schema, see [Run data format](../../Monitor/Debug/Data%20type%20reference/Run%20%28span%29%20data%20format.md).

## Chain evaluators

A chained evaluator is an online evaluator that triggers only on runs another evaluator has already scored. Chaining lets you use a more specific evaluator or reserve a more expensive evaluator for the runs that need it. For example, you can run an [LLM-as-a-judge evaluator](../../Monitor/Observe/Online%20evaluators/Set%20up%20LLM-as-a-judge%20online%20evaluators.md) only when an earlier `correctness` score is below a threshold.

The second evaluator must be a run-level evaluator because [multi-turn (thread-level) evaluators](../../Monitor/Observe/Online%20evaluators/Set%20up%20multi-turn%20online%20evaluators.md) cannot filter on feedback. The first evaluator can be either type. A multi-turn evaluator attaches its feedback to the last run in the thread, so a second evaluator chained onto it evaluates that run, not the full thread.

To chain a second evaluator onto a first:

1. Create or open the second evaluator and expand its filter. For more information, see [Apply a filter to runs that trigger the evaluator](../../Monitor/Observe/Online%20evaluators/Set%20up%20LLM-as-a-judge%20online%20evaluators.md#apply-a-filter-to-runs-that-trigger-the-evaluator) for LLM-as-a-judge evaluators or [Create a filter](../../Monitor/Observe/Online%20evaluators/Set%20up%20online%20code%20evaluators.md#3-create-a-filter) for code evaluators.

2. Filter on the first evaluator's feedback key. The filter matches on the key rather than the evaluator that produced it, so feedback from any source with that key triggers the second evaluator, including [user feedback](../Annotation%20Queues/Feedback/Log%20user%20feedback%20using%20the%20SDK.md). Use a key that only the first evaluator produces.
   * To trigger on every run the first evaluator scored, filter on the key alone:

     ```text
     eq(feedback_key, "correctness")
     ```

   * To trigger only when the score meets a condition, combine the key with a `feedback_score` comparison. For example, to trigger only when `correctness` is below `0.5`:

     ```text
     and(eq(feedback_key, "correctness"), lt(feedback_score, 0.5))
     ```

3. If the second evaluator reads the first score, [include extended stats](#include-extended-stats). LLM-as-a-judge evaluators require it, and code evaluators use it to read the score reliably. For more information, see [Read the first score](#read-the-first-score).

4. Save the evaluator.

The second evaluator picks up a run only after the first evaluator's score is attached to it, so the order in which the evaluators run does not matter. For the full filter syntax, see [Trace query syntax](../../Monitor/Debug/Viewing%20%26%20managing%20traces/Trace%20query%20syntax.md).

### Read the first score

How the second evaluator reads the first evaluator's score depends on its type:

* **LLM-as-a-judge evaluators**: [Include extended stats](#include-extended-stats), then map a prompt variable to `run.feedback_stats.<feedback_key>.avg`. For example, map `{{correctness_average}}` to `run.feedback_stats.correctness.avg`.
* **Code evaluators**: Read the [feedback record](../../Monitor/Debug/Data%20type%20reference/Feedback%20data%20format.md) in `run["feedback"]` whose `key` is the first evaluator's feedback key, and use its `score`. `run["feedback"]` holds at most 100 feedback records across each batch of runs the evaluator processes, and the oldest records are dropped first, so the score can be missing when the batch carries many feedback records. To read the score reliably, include extended stats and read the average from `run["feedback_stats"]["<feedback_key>"]["avg"]`.

The `avg` field averages every feedback record with that key on the run, so it equals the first evaluator's score only when the run has one record with that key. Another record with the same key, such as user feedback, changes the average.

## Delete an evaluator

You cannot delete an evaluator while it is attached to a trace container or dataset. To delete an evaluator:

1. In the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-evaluators), select **Evaluators** in the left sidebar.
2. Select the evaluator you want to delete.
3. Open the **Environments & Datasets** tab (**Projects & Datasets** in self-hosted deployments). For each attachment listed there, select **Detach** in the **Actions** menu at the right of the row.
4. Return to the **Evaluators** page and click **Delete** at the top of the page.

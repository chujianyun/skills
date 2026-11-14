# Set up LangChain Tuned Evaluators

> Use specialized LangChain-managed judges to attach quality feedback to traces.

> [!NOTE]
>
> LangChain Tuned Evaluators are in **[beta](../../../LangSmith%20setup/Cloud/Reference/Release%20stages.md)**. Their interface and behavior may change before general availability.

LangChain Tuned Evaluators attach feedback to your traces. Each evaluator uses a specialized judge trained for a specific evaluation task. LangChain writes, tests, versions, and maintains the prompt and judge model so that you can focus on using the feedback to find and fix problems in your agent.

Perceived Error (Tuned) detects conversations with evidence that an agent made a mistake, misunderstood a request, or took the interaction in the wrong direction. It returns `true` when the user appears to perceive an error and `false` otherwise. Evidence can include a user correction, repeated request, rejected action, contradictory response, acknowledged mistake, persistent misunderstanding, or unresolved outcome.

Use Perceived Error feedback to:

* Find failures that did not produce a system error or explicit user rating.
* Filter for conversations that need investigation and review the evaluator's explanation with the original interaction.
* Compare flagged threads to identify recurring failure modes.
* Add useful threads to evaluation datasets or send ambiguous cases for human review.
* Test agent changes against examples drawn from traced failures.

## Understand how LangChain Tuned Evaluators work

**1. Add an evaluator**

Add a LangChain Tuned Evaluator to a compatible tracing project.

**2. Identify an eligible thread**

LangSmith identifies a thread that meets the evaluator's requirements and the project's filters and sampling configuration.

**3. Evaluate the thread**

The specialized LangChain-managed judge evaluates the eligible thread.

**4. Attach feedback**

LangSmith attaches the result and its explanation to the thread as feedback.

## Before you begin

Before you add Perceived Error (Tuned):

* An [organization admin](../../../LangSmith%20setup/Govern/Users%20%26%20access%20control/Role-based%20access%20control.md#organization-admin) must enable LangChain Tuned Evaluators for the organization.
* The source must be a tracing project that uses [threads](../../Debug/Configure%20threads.md). The Perceived Error (Tuned) evaluator cannot run on individual runs.
* Thread traces must contain supported [message lists](Set%20up%20multi-turn%20online%20evaluators.md#prerequisites). At least one non-empty user message must be followed by a non-empty assistant message.
* Each thread must contain at least two traces before the evaluator can run.

## Enable LangChain Tuned Evaluators

Enabling LangChain Tuned Evaluators lets members attach them to tracing projects throughout the organization. Evaluation data is processed using LangChain-managed API keys.

To enable LangChain Tuned Evaluators as an organization admin:

1. In the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-tuned-evaluators), open **Settings**.
2. Select **Tuned evaluators**.
3. Turn on **Enable LangChain Tuned evaluators** and accept the terms.

An organization admin can also accept and enable LangChain Tuned Evaluators when first saving one from the evaluator gallery.

## Add a LangChain Tuned Evaluator to a project

To add Perceived Error (Tuned) to a tracing project:

1. Open a tracing project and select the **Evaluators** tab.
2. Select **+ Evaluator**.
3. Under **LangChain Tuned**, select **Perceived Error (Tuned)**.
4. (Optional) Configure filters and the sampling rate.
5. Click **Save**.

Before creating the evaluator, LangSmith checks the recent threads in the project for the supported message list with a complete user-to-assistant exchange.

LangSmith blocks creation when the project is empty or none of the recent threads has a compatible message structure.

## Disable LangChain Tuned Evaluators

To disable LangChain Tuned Evaluators for the organization:

1. Open **Settings** and select **Tuned evaluators**.
2. Turn off **Enable LangChain Tuned evaluators**.

Disabling the feature pauses attached LangChain Tuned Evaluators. LangSmith preserves their configuration, and they resume when an organization admin enables the feature again.

## Review usage charges

Availability and pricing vary by LangChain Tuned Evaluator. LangSmith charges LSUs only for an evaluation run that attaches feedback. Skipped and failed evaluation attempts that do not attach feedback are not billed.

Like other online evaluators, LangChain Tuned Evaluators upgrade evaluated traces to extended retention. This can increase trace storage charges. For current rates, see [LangSmith pricing](https://docs.langchain.com/langsmith/pricing-plans.md). For details about retention upgrades and trace charges, see [data retention auto-upgrades](../../Trace/Configuration%20%26%20troubleshooting/Usage%20and%20billing.md#data-retention-auto-upgrades).

## Troubleshoot LangChain Tuned Evaluators

### The project is empty

Add a thread to the tracing project, then try to save the evaluator again. The thread must contain supported message lists and at least one complete user-to-assistant exchange.

### The project does not contain a valid message list

Check the inputs and outputs of the project's most recent threads. Their top-level `messages` fields must contain message lists in a [supported format](Set%20up%20multi-turn%20online%20evaluators.md#prerequisites), and at least one user message must be followed by an assistant message.

### The evaluator does not produce feedback

Check the following conditions:

* The organization still has LangChain Tuned Evaluators enabled.
* The thread contains at least two traces.
* The project's thread idle time has elapsed.
* The thread matches the evaluator's filters and sampling configuration.
* The thread contains a complete user-to-assistant exchange in a supported message format.

To inspect evaluator activity, open the tracing project's **Evaluators** tab and select **Logs** for the evaluator.

### Enabling the feature does not take effect immediately

Organization settings can take a few seconds to propagate. If LangSmith reports that the managed-evaluator setting is still taking effect, wait a few seconds and try again.

## See also

* [Manage evaluators](../../../Test/Evaluators/Manage%20evaluators.md)
* [Set up multi-turn online evaluators](Set%20up%20multi-turn%20online%20evaluators.md)
* [Trace with threads](../../Debug/Configure%20threads.md)

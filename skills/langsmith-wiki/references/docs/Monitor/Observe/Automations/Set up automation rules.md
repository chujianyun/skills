# Set up automation rules

While you can manually sift through and process production logs from your LLM application, it often becomes difficult as your application scales to more users. LangSmith provides **Automations** that allow you to trigger certain actions on your trace data. You define an automation by an **item type**, **filter**, **sampling rate**, and **action**.

Automation rules can trigger actions such as: adding traces to a dataset, adding to an annotation queue, triggering a webhook (for example, for remote evaluations) or extending data retention. A rule matches either individual runs or entire [threads](../../Trace/Observability%20concepts.md#threads), depending on the item type you select. Some examples of automations you can set up:

* Send all traces with negative feedback to an annotation queue for human review.
* Send 10% of all traces or threads to an annotation queue for human review to spot check for issues.
* Post all traces with a low evaluator score to your webhook endpoint.
* Upgrade all traces with errors for extended data retention.

> [!NOTE]
>
> To configure online evaluations, visit the [online evaluations](../Online%20evaluators/Set%20up%20LLM-as-a-judge%20online%20evaluators.md) page.

> [!NOTE]
>
> An automation rule can upgrade matching traces to [extended data retention](../../Trace/Configuration%20%26%20troubleshooting/Usage%20and%20billing.md#data-retention-auto-upgrades) when retention extension is enabled for that rule. This ensures that traces meeting your automation criteria (typically those most valuable for analysis) are preserved for investigation. Each action type has its own default, refer to the [action-level retention settings](#create-a-rule) for details. For the full retention model, see [data retention auto-upgrades](../../Trace/Configuration%20%26%20troubleshooting/Usage%20and%20billing.md#data-retention-auto-upgrades).

## How automation rules execute

Each automation rule runs on an independent polling schedule. If you have multiple rules on the same project, a webhook rule may process a run before an evaluator rule has scored it, or vice versa.

Within a single rule, if multiple actions are configured, they execute in this order:

1. Add to annotation queue.
2. Add to dataset.
3. Trigger webhook.
4. Run online evaluator.
5. Run custom code evaluator.
6. Extend data retention.
7. Trigger alert.

If your workflow requires data produced by one rule to be present when another fires—for example, you want a webhook to include an evaluation score—use a filter on the downstream rule to create that dependency explicitly. For an example, refer to [Ensuring evaluations complete before the webhook fires](Configure%20webhook%20notifications%20for%20rules.md#ensuring-evaluations-complete-before-the-webhook-fires).

## Set the item type to runs or threads

The **Item Type** control determines what a rule matches. Set it to **Runs** and the rule evaluates each matching run as it arrives. Set it to **Threads** and the rule waits until a conversation is complete, then applies its action once to the whole thread. Choose **Threads** when the unit you want to review or export is the full conversation rather than a single turn.

Thread rules require a tracing project, or an agent environment, that groups traces into threads. For more information, refer to [Configure threads](../../Debug/Configure%20threads.md).

### Configure a thread rule

Selecting **Threads** changes three parts of the rule form:

* **Thread Filters**: The filter builder adds **Trace Count** and **Thread ID** to the available fields. Filter on **Trace Count** to scope a rule to conversations of a given length. The other fields evaluate each trace in the thread rather than the thread as a whole, so a thread matches when any of its traces match. For example, a filter on **Status** selects every thread that contains an errored trace, not only threads whose last trace errored.
* **Action**: The form offers **Add to Annotation Queue**, **Add to Dataset**, or **Trigger Webhooks**.

The three thread actions behave as follows:

* **Add to Annotation Queue**: Adds the thread to the queue as a thread item. Thread items display the conversation transcript and support rubric feedback only. For what differs between run items and thread items, refer to the [annotation queue capability table](../../../Test/Annotation%20Queues/Use%20annotation%20queues.md#single-run-annotation-queues).
* **Add to Dataset**: Creates one dataset example for each matching thread. Each example contains the thread's full conversation.
* **Trigger Webhooks**: Sends a payload whose top-level `threads` array holds every matching thread. For more information, refer to [Read a thread rule payload](Configure%20webhook%20notifications%20for%20rules.md#read-a-thread-rule-payload).

### Set the thread idle time

A thread rule acts only after the thread goes idle. Once the last trace in a thread is ingested, LangSmith waits for the idle time configured on the tracing project or agent environment to elapse, which signals that the conversation is complete. The idle time defaults to 10 minutes and cannot be set below 2 minutes.

The idle time is a project-level setting shared with [multi-turn online evaluators](../Online%20evaluators/Set%20up%20multi-turn%20online%20evaluators.md). Creating the first thread rule on a project applies the default without overwriting a value already set for that project, and changing the value affects every thread evaluator and thread rule in it.

These limits bound what a thread rule processes:

* **Runs must be less than one week old**: When a thread becomes idle, only runs from the past 7 days are eligible.
* **Maximum of 500 threads per execution**: A single execution processes at most 500 matching threads, ordered by most recent activity.

### Extend data retention for a thread

[Data retention](../../Trace/Configuration%20%26%20troubleshooting/Usage%20and%20billing.md#data-retention-auto-upgrades) is a property of a trace, not of a thread. When a thread rule has **Extend Data Retention** enabled, it upgrades **every trace in the matched thread** to extended retention, not only the most recent one.

Because each trace is upgraded individually, a longer conversation costs more to retain. In exchange, the entire conversation is preserved for investigation instead of expiring turn by turn.

## View automation rules

In the [UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-rules), navigate to **Tracing** in the sidebar and select a tracing project, or an agent environment. To view existing automation rules for that tracing project, click on the **Automations** tab.

## Create a rule

1. In the [UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-rules), navigate to **Tracing** in the sidebar and select a tracing project, or an agent environment. Click on **+ New** in the top right corner of the tracing project page, then click on **New Automation**.

2. Name your rule.

3. Select an **Item Type**, either **Runs** or **Threads**. The item type determines which filter fields and actions are available, so set it before configuring either. For more information, refer to [Set the item type to runs or threads](#set-the-item-type-to-runs-or-threads).

4. Create a filter. Rules use the filter builder, with the same fields and operators described in [Filter traces (ClickHouse)](../../Debug/Viewing%20%26%20managing%20traces/Filter%20traces%20%28ClickHouse%29.md).

5. Configure a **Sampling Rate** to control what percentage of the filtered items trigger the automation action. The form accepts a percentage from 0 to 100. For example, a sampling rate of 50% sends half of the items that pass the filter to the action. The equivalent API field, `sampling_rate`, takes a decimal from 0 to 1.

6. (Optional) Apply rule to past runs by toggling the **Apply to Past Runs** and entering a **Backfill From** date. This is only possible upon rule creation.

   > [!NOTE]
   >
   > The backfill is processed as a background job, so you will not see the results immediately. In order to track progress of the backfill, you can [view logs for your automations](#view-logs-for-your-automations).

7. Select the action the rule performs. Rules with the **Runs** item type support every action below. Rules with the **Threads** item type support only **Add to Annotation Queue**, **Add to Dataset**, and **Trigger Webhooks**.

   * **Add to Annotation Queue**: Add the matching run or trace to an [annotation queue](../../../Test/Annotation%20Queues/Use%20annotation%20queues.md) as a run item. A thread rule adds the entire conversation as a thread item instead. To add a thread by hand, refer to [Assign runs and threads](../../../Test/Annotation%20Queues/Use%20annotation%20queues.md#assign-runs-and-threads-to-a-single-run-queue).
   * **Add to Dataset**: A run rule adds the trace's inputs and outputs to a [dataset](../../../Test/Get%20started/Evaluation%20concepts.md#datasets). A thread rule creates one example for each matching thread. Each example contains the thread's full conversation.
   * **Trigger Webhooks**: Post the matched items to every [webhook](Configure%20webhook%20notifications%20for%20rules.md) URL configured on the rule.
   * **Extend Data Retention**: Extends the data retention period on matching traces that use base retention [(refer to the data retention docs for more details)](../../Trace/Configuration%20%26%20troubleshooting/Usage%20and%20billing.md#data-retention).

     > [!NOTE]
     >
     > Each action has an independent **Extend Data Retention** toggle that controls whether matching traces are upgraded to extended retention. The defaults are the same for both item types:
     >
     > * **Add to Dataset**: opt-in (default: off). Enable the toggle to upgrade matching traces.
     > * **Add to Annotation Queue**: opt-out (default: on). Disable the toggle to skip upgrading matching traces.
     > * **Trigger Webhooks**: opt-in (default: off). Enable the toggle to upgrade matching traces.
     > * **Extend Data Retention** action and online/code evaluators: unchanged; always upgrade matching traces.
     >
     > For a thread rule, an enabled toggle upgrades every trace in the matched thread. For more information, refer to [Extend data retention for a thread](#extend-data-retention-for-a-thread).
     >
     > The retention toggle for each action is an admin-only control, gated by the [`rules:configure-retention`](../../../LangSmith%20setup/Govern/Users%20%26%20access%20control/Organization%20and%20workspace%20operations%20reference.md#rules) permission. Non-admin workspace members see the toggles as disabled and cannot change them, but can still create and edit rules without affecting retention settings. For the full retention model, refer to [data retention auto-upgrades](../../Trace/Configuration%20%26%20troubleshooting/Usage%20and%20billing.md#data-retention-auto-upgrades).

## View logs for your automations

Logs allow you to gain confidence that your rules are working as expected. You can view logs for your automations by navigating to the **Automations** tab within a tracing project or agent environment and clicking the **Logs** button for the rule you created.

The logs tab allows you to:

* View all runs processed by a given rule for the time period selected.
* If a particular rule execution has triggered an error, you can view the error message by hovering over the error icon.
* You can monitor the progress of a backfill job by filtering to the rule's creation timestamp. This is because the backfill starts from when the rule was created.
* Inspect the run that the automation rule applied to using the **View run** button. For rules that add runs as examples to datasets, you can view the example produced.

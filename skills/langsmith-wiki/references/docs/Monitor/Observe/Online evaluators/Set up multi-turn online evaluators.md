# Set up multi-turn online evaluators

Multi-turn online evaluators allow you to evaluate entire conversations between a human and an agent, not just individual exchanges. They measure end-to-end interaction quality across all turns in a thread.

> [!TIP]
>
> To use a LangChain-managed, thread-level judge without configuring a model, API key, or prompt, see [LangChain Tuned Evaluators](Set%20up%20LangChain%20Tuned%20Evaluators.md).

You can use multi-turn evaluations to measure:

1. Semantic Intent: What the user was trying to do.
2. Semantic Outcome: What actually happened, did the task succeed.
3. Trajectory: How the conversation unfolded, including trajectory of tool calls.

> [!NOTE]
>
> Multi-turn online evaluators can extend trace retention by default. You can opt out when configuring the evaluator so that traces keep the project's configured retention tier. Traces are still upgraded if another action explicitly extends retention or the project already uses extended retention. For step-by-step opt-out instructions, see [Manage evaluator trace retention](../../../Test/Evaluators/Manage%20evaluators.md#manage-evaluator-trace-retention). For details, see [data retention auto-upgrades](../../Trace/Configuration%20%26%20troubleshooting/Usage%20and%20billing.md#data-retention-auto-upgrades).

## How it works

Multi-turn online evaluators follow this evaluation lifecycle:

1. **Trace ingestion**: Each turn in a conversation is traced as a separate run and associated with a thread using a shared thread ID.
2. **Idle time detection**: After the last trace in a thread is ingested, LangSmith waits for the configured idle time to elapse. This idle period signals that the conversation is complete and ready for evaluation.
3. **Message assembly**: LangSmith collects the `messages` from each trace in the thread and assembles them into a single conversation history. If each trace contains only the latest message, LangSmith stitches messages together across turns. If each trace contains the full history, LangSmith uses that directly. Because consecutive traces in a thread often resend prior history, LangSmith deduplicates overlapping messages so each one appears only once. The result is a single list of messages in OpenAI chat format (`{"role": ..., "content": ...}`), which is what the `all_messages` variable in your prompt resolves to.
4. **LLM-as-a-judge evaluation**: The assembled conversation is passed to your configured LLM-as-a-judge prompt. The evaluator scores the full thread based on your criteria: semantic intent, outcome, or trajectory.
5. **Feedback recording**: The evaluator writes feedback to LangSmith using the feedback key you configured, associated with the thread.

This lifecycle means that multi-turn evaluators run once per completed thread, not once per trace. Use [run-level online evaluators](Set%20up%20LLM-as-a-judge%20online%20evaluators.md) if you want per-trace evaluation.

## Prerequisites

* Your tracing project, or agent environment, must be using [threads](../../Debug/Configure%20threads.md).
* The top-level inputs and outputs of each trace in a thread must have a `messages` key that contains a list of messages. We support messages in [LangChain](../../Trace/Tracing%20setup/Manual%20instrumentation/Log%20LLM%20calls.md#messages-format), [OpenAI Chat Completions](https://platform.openai.com/docs/api-reference/chat/create), and [Anthropic Messages](https://platform.claude.com/docs/en/api/messages) formats.
  * If the top-level inputs and outputs of each trace only contain the latest message in the conversation, LangSmith will automatically combine messages across turns into a thread.
  * If the top-level inputs and outputs of each trace contain the full conversation history, LangSmith will use that directly.

> [!NOTE]
>
> If your traces don't follow the format above, thread level evaluators won't work. You'll need to update how you trace to LangSmith to ensure each trace's top-level inputs and outputs contain a list of `messages`.
>
> Please refer to the [troubleshooting](Set%20up%20multi-turn%20online%20evaluators.md#troubleshooting) section for more information.

## Configuration

1. Navigate to the **Tracing** page and select a tracing project, or an agent environment.

2. Click the **Evaluators** tab, then click **+ Evaluator**. Select **LLM-as-a-Judge Evaluator** under **Create from scratch**. Under **Source**, select **Threads**.

3. **Name your evaluator**.

4. Apply **Filters** or a **Sampling Rate**.

   Use filters or sampling to control evaluator cost. For example, evaluate only threads under *N* turns or sample 10% of all threads.

5. **Configure an idle time**.

   The first time you configure a thread-level evaluator, you can define the idle time, the amount of time after the last trace in a thread before it is considered complete and ready for evaluation. This value should reflect the expected length of user interactions in your app. The idle time defaults to 10 minutes and cannot be set below 2 minutes.

   > [!NOTE]
   >
   > The idle time is a project-level setting. It applies to every thread-level evaluator in the project and to every [automation rule](../Automations/Set%20up%20automation%20rules.md#set-the-thread-idle-time) whose item type is **Threads**.

   > [!TIP]
   >
   > When first testing your evaluator, use a short idle time so you can see results quickly, subject to the 2-minute minimum. Once validated, increase it to match the expected length of user interactions.

6. **Configure your model.**

   Select the provider and model you want to use for your evaluator. Threads tend to get long, so you should use a model with a higher context window in order to avoid running into limits. For example, OpenAI's GPT-5.4 mini or Gemini 2.5 Flash are good options as they both have 1M+ token context windows.

7. **Configure your LLM-as-a-judge prompt.**

   Define what you want to evaluate. This prompt will be used to evaluate the thread. You can also configure which parts of the assembled conversation are passed to the evaluator through the `all_messages` variable to control the content it receives:

   * All messages: Send the full conversation as a list of JSON message objects in OpenAI chat format (`{"role": ..., "content": ...}`), with each message rendered as indented JSON and separated by a blank line.
   * Human and AI pairs: Send only user and assistant messages, formatted as `<user>...</user>` and `<assistant>...</assistant>` and excluding system messages, tool calls, and other roles.
   * First human and last AI: Send only the first user message and the last assistant reply.

8. **Set up your feedback configuration**.

   Configure a name for the feedback key, the format for the feedback you want to collect and optionally enable reasoning on the feedback.

   > [!WARNING]
   >
   > Using the same feedback key for a thread-level evaluator and a run-level evaluator is **not recommended** as it can be hard to distinguish between the two.

9. **Save your evaluator.**

   After saving, your evaluator will appear in the **Evaluators** tab. You can test it once the idle time has passed for any new threads created after saving.

## Evaluate trajectories

`trajectory` is one of the variables a thread evaluator can use, alongside `all_messages`, `human_ai_pairs`, and `first_human_last_ai`. It resolves to the [trajectory](../../Trace/Observability%20concepts.md#trajectories) of the conversation: the flat, ordered list of messages from start to finish, including tool calls and their results. Use it to score the path an agent took, such as whether it picked the right tools, followed its plan, and got there without wasted steps.

> [!NOTE]
>
> On [LangSmith Cloud](../../../LangSmith%20setup/Cloud/Cloud%20%28SaaS%29.md), the `trajectory` variable is available in the GCP US, GCP EU, GCP APAC, and AWS US regions. It is not available on [BYOC](../../../LangSmith%20setup/BYOC/Bring%20Your%20Own%20Cloud%20%28BYOC%29.md) deployments.
>
> [Self-hosted](../../../LangSmith%20setup/Self-hosted/Self-hosted%20LangSmith.md) installations support the `trajectory` variable on LangSmith v0.17 or later, after you [switch queries to SmithDB](../../../LangSmith%20setup/Self-hosted/SmithDB/Install%20SmithDB/Install%20LangSmith%20with%20SmithDB.md#step-6-switch-queries-to-smithdb). See [SmithDB feature availability](../../../LangSmith%20setup/Self-hosted/SmithDB/SmithDB%20feature%20availability.md).

The variables differ in what the judge receives:

* **`all_messages`, `human_ai_pairs`, and `first_human_last_ai`** resolve to the conversation assembled from the inputs and outputs of each root run in the thread. Work that happens in child runs, such as intermediate model calls, tool calls, and tool result, is not included unless a root run's own inputs or outputs contain it. human\_ai\_pairs and first\_human\_last\_ai narrow further to user and assistant messages only.
* **`trajectory`** resolves to the trajectory built from the model and tool calls inside each trace. The tool calls and tool results the other views omit are preserved.

For the message shape each variable resolves to, see [Thread message variables](../../../Deploy/Prompt%20%26%20Context%20Hub/Prompts/Create%20and%20manage%20prompts/Prompt%20template%20format%20guide.md#thread-message-variables).

> [!WARNING]
>
> A trajectory is typically larger than any of the other views, because it encompasses both root and child runs. Choose a model with a high context window, as described in step 6 of [Configuration](#configuration), and expect higher token usage per evaluation.

### Use the trajectory variable

Follow the [configuration](#configuration) steps above. Two things change:

1. Under **Source**, select **Threads**. The variable is available only on an evaluator that runs against a tracing project, not against a dataset.
2. Reference `{{trajectory}}` in your prompt and map that variable to the `trajectory` source. The variable must be named `trajectory`: a differently named variable pointed at that source is rejected. The seeded default prompt and mapping already do this, so a new evaluator needs no changes here.

Switching **Source** between **Runs** and **Threads** reseeds the default prompt only while you have not edited it. Once you edit the prompt, your version is kept, and you map the variables yourself.

`{{trajectory}}` cannot appear alongside `{{all_messages}}`, `{{human_ai_pairs}}`, or `{{first_human_last_ai}}`. Once you map the trajectory source, the other sources are disabled in the variable source dropdown, and once you map one of the others, the trajectory source is disabled. Either way, the dropdown explains that trajectory variables and non-trajectory variables cannot be used together. Saving an evaluator that mixes them fails the same way.

When the evaluator completes, LangSmith writes feedback to the most recent root run in the thread, under the feedback key you configured, and associates that feedback with the thread. To find it later, see [View feedback](../../Debug/Configure%20threads.md#view-feedback).

For a complete prompt you can adapt, see [Example with trajectory context](../../../Deploy/Prompt%20%26%20Context%20Hub/Prompts/Create%20and%20manage%20prompts/Prompt%20template%20format%20guide.md#example-with-trajectory-context).

> [!WARNING]
>
> The choice is fixed when you create the evaluator. To move an existing evaluator between `trajectory` and the other thread variables, delete it and create a new one.

### Settings and constraints

An evaluator that uses `trajectory` supports the following settings:

* **Filters**: Limit which threads the evaluator runs on.
* **Sampling rate**: Evaluate a percentage of the threads that match your filters.
* **Idle time**: The project-level thread idle time, which applies to every thread-level evaluator in the project.

The following options are not available, and a configuration that includes one is rejected:

* Datasets and experiments as a source.
* Backfill over existing threads.
* Trace filters and tree filters.
* Few-shot examples, extended stats, and dataset corrections.
* Code evaluators on the same automation rule, and non-evaluator actions such as adding threads to an annotation queue.

A trajectory is not a run, so any option that reads run-level fields is unavailable.

## Limits

These are the current limits for thread-level processing (subject to change). They apply to multi-turn online evaluators and to [automation rules](../Automations/Set%20up%20automation%20rules.md#set-the-item-type-to-runs-or-threads) whose item type is **Threads**. Reach out if you are running into any of these limits.

* **Runs must be less than one week old**: When a thread becomes idle, only runs within the past 7 days are eligible for evaluation.
* **Maximum of 500 threads processed at once**: A single execution processes at most 500 matching threads, ordered by most recent activity.
* **Maximum of 10 multi-turn online evaluators per workspace**

## Troubleshooting

**Checking the status of your evaluator**

You can check when your evaluator was last run by heading to the **Evaluators** tab within a tracing project or agent environment and clicking the **Logs** button for the evaluator you created to view its run history.

**Inspect the data sent to the evaluator**

Inspect the data sent to the evaluator by heading to the **Evaluators** tab within a tracing project or agent environment, clicking on the evaluator you created and clicking the **Traces** tab. The tab shows traces only if you [turned on tracing for the evaluator](../../../Test/Evaluators/Manage%20evaluators.md#trace-evaluator-runs). New evaluators start with tracing turned off.

In this tab, you can see the inputs passed into the LLM-as-a-judge evaluator. If your messages are not being passed in correctly, you will see blank values in the inputs. This can happen if your messages are not formatted in one of [the expected formats](Set%20up%20multi-turn%20online%20evaluators.md#prerequisites).

# Find and fix your agent's issues with LangSmith Engine

> Review the issues LangSmith Engine detects, open pull requests with its proposed fixes, and turn failing traces into dataset examples.

The **Engine** page lists the issues [LangSmith Engine](LangSmith%20Engine.md) detects in a tracing project, each with a diagnosis, the traces that support it, and a proposed fix. Work through them to ship fixes and to turn real failures into evaluation datasets. If Engine is not running on your project yet, see [Set up Engine](Set%20up%20LangSmith%20Engine.md).

Click any issue to open its detail panel. At the top, a diagnosis describes the problem and its impact. Each issue has a toolbar for setting its priority, closing or reopening it, opening a pull request, creating a Linear issue, and watching it.

Engine learns from what you do with each issue: closing it, marking it as incorrectly flagged, changing its priority, or opening a pull request, along with any reason you give. For how those actions shape later scans, see [How Engine learns from your actions on issues](LangSmith%20Engine.md#how-engine-learns-from-your-actions-on-issues).

## Review evidence

The **Evidence** section contains traces that support a diagnosis, including a snippet from each trace. From this section, you can:

* **View a trace**: Click **Open trace** to open an evidence trace. When Engine identifies the child run that caused the issue, it opens that exact run. The trace view includes a **View issue** link back to the Engine issue.
* **Create offline examples**: Click [**Add offline examples**](#add-offline-examples) to generate custom ground truth [dataset examples](../Test/Datasets%20%26%20Experiments/Datasets/Manage%20datasets.md) from the production trace inputs for offline evaluation.
* **View project evidence**: Click **View all in project** to view the evidence in the tracing project.

For more information, see [Manage a trace](../Monitor/Debug/Viewing%20%26%20managing%20traces/Manage%20a%20trace.md).

When feedback on a trace surfaces or confirms an issue, the issue lists that feedback under **Feedback cited by Engine**, below the diagnosis. Each entry shows a feedback key, such as one written by an online evaluator or a user's thumbs-down rating, and how many evidence traces cite it. Click a key to open the newest trace with that feedback. In the **Evidence** section, each trace that cites feedback also shows the cited feedback values next to **Open trace**. For how Engine uses feedback, see [How Engine selects traces](LangSmith%20Engine.md#how-engine-selects-traces).

Engine keeps tracking an issue after it is filed. On later scans, any new trace that matches the issue's failure pattern is added to **Evidence** automatically, so the issue reflects how often the failure is still happening without you re-running anything.

The **Proposed Fix** section describes the issue and suggests how to address it, which may include specific code or prompt changes if a repository is connected.

## Change priority and status

Select **Low**, **Medium**, or **High** from the priority dropdown to update an issue's priority. You can optionally provide a reason, which Engine [learns from](LangSmith%20Engine.md#how-engine-learns-from-your-actions-on-issues) on later scans.

Closing records the outcome of your review. Click:

* **Close** to mark the issue as resolved.
* **Incorrectly Flagged** to dismiss the issue as not real or not worth fixing.

For either outcome, you can optionally provide a reason, which Engine [learns from](LangSmith%20Engine.md#how-engine-learns-from-your-actions-on-issues) on later scans.

You can reopen a closed issue at any time. Click **Reopen** to clear any fix in progress and stop watching the issue if it was being watched. Engine also reopens an issue automatically when it detects the same problem recurring in a later trace.

## Open a pull request

To open a pull request with the proposed code change, first [connect a repository](Connect%20Engine%20to%20your%20repository.md), then click **Open PR**. On GitLab, Engine opens a merge request, but the buttons keep their names, **Open PR** and **View PR**. Once a pull request exists, Engine replaces **Open PR** with **View PR**. Click **View PR** to open the pull request in GitHub or the merge request in GitLab. Engine reflects the PR's status (open, merged, or closed) throughout the issue.

You can also copy the issue's fix context to your clipboard for use with an LLM or coding assistant. Engine can propose code changes to any connected repository, including agents built with [Deep Agents](https://docs.langchain.com/oss/python/deepagents/overview.md), [LangChain](https://docs.langchain.com/oss/python/langchain/overview.md), and [LangGraph](https://docs.langchain.com/oss/python/langgraph/overview.md).

## Create a Linear issue

To create an issue, first [connect Linear](Set%20up%20LangSmith%20Engine.md#connect-to-linear), then click **Create in Linear** on an Engine issue. Engine shows **Linear creation pending** while it creates the issue. When creation completes, Engine displays the linked Linear issue identifier in the Engine issue and issue list.

The Linear issue includes the Engine issue title and description, severity, category, tags, a **View issue in LangSmith** link, and evidence trace IDs. Engine retains the link to the Linear issue. If you close the Linear ticket, Engine closes the corresponding issue. If you cancel the Linear ticket, Engine marks the corresponding issue as incorrectly flagged. Engine also tracks a pull request linked to the Linear ticket on the corresponding Engine issue.

## Add offline examples

This step captures the traces that surfaced the issue as ground-truth [dataset examples](../Test/Datasets%20%26%20Experiments/Datasets/Manage%20datasets.md), so you can evaluate the fix offline before it reaches production.

1. Click **Add offline examples** at the top right of the **Evidence** list to open the **Add as offline example** dialog.
2. Review each trace. The dialog shows the input, the wrong output the agent produced, and the proposed expected output as a custom ground truth example.
3. Click **Add to Dataset** to add them directly, or click **Edit in annotation queue** to review them first.
4. In the annotation queue, each example shows the run inputs alongside reference outputs proposed by Engine, structured as named [assertions](../Test/Annotation%20Queues/Use%20assertions.md) generated from trace analysis. Each assertion is a short claim describing what a correct answer should or shouldn't include. Edit the assertions as needed, add new ones with **+ Add assertion**, then click **Add to Dataset & Continue** to work through each example.

For more information, refer to [Manage datasets](../Test/Datasets%20%26%20Experiments/Datasets/Manage%20datasets.md), [Use annotation queues](../Test/Annotation%20Queues/Use%20annotation%20queues.md), and [Use assertions](../Test/Annotation%20Queues/Use%20assertions.md).

## Watch an issue

Watching keeps an issue open for monitoring without resolving it or marking it as incorrectly flagged. Click **Watch** when you are not ready to fix an issue but still want to know if it keeps happening.

To be alerted when a watched issue recurs, click **Alert me via Slack**, which opens the **Notifications** section of the [Engine settings](Set%20up%20LangSmith%20Engine.md#configure-engine) panel. See [Engine notifications](LangSmith%20Engine%20notifications.md).

When new traces link to a watched issue, Engine moves it to the top of your list and shows how many new traces arrived, so you can pick up the fix or keep watching.

> [!NOTE]
>
> Watching is only available for open issues without a pull request in flight: discard the fix to watch an issue again. Resolving a watched issue, or marking it as incorrectly flagged, automatically stops watching it.

## Flag a trace for Engine

A flagged trace is one you have asked Engine to review directly, for example a trace where your agent went wrong without raising an error or receiving a low score. Engine reviews flagged traces on its next scan. For how flags fit into trace selection, see [How Engine selects traces](LangSmith%20Engine.md#how-engine-selects-traces).

Flagging a trace requires Engine to be enabled for your organization and the `feedback:create` permission, which the Workspace Admin and Workspace Editor roles include. For more information, see [Feedback permissions](../LangSmith%20setup/Govern/Users%20%26%20access%20control/Organization%20and%20workspace%20operations%20reference.md#feedback).

To flag a trace:

1. Open the trace and click **Flag for Engine**.
2. (Optional) Add a note describing what went wrong or what Engine should look for.
3. Click **Flag for Engine** in the popover.

The button changes to **Queued** and stays that way until Engine links the trace to an issue. Click **Queued** to update your note, or click **Unflag** in the popover to remove the flag. When Engine links the trace to an issue, the trace view hides the button and shows a **View issue** link to that issue. If Engine is not set up yet for the tracing project or [agent environment](../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20environments.md) that contains the trace, the popover offers **Flag and set up Engine**, which saves the flag and opens its **Engine** tab to [finish setup](Set%20up%20LangSmith%20Engine.md).

## Filter and sort issues

### In the UI

The **Engine** page lists detected issues in the left panel. Each entry shows a title, a short description, the number of contributing traces, and how recently the issue was observed. Each issue is tagged with a failure category, such as **Silent tool error** or **Hallucination**.

At the top of the list, you can click:

* **Filter issues** icon to filter by **Priority**, **Status** and **Tags**.
* **Sort issues** icon to sort by **Severity**, **Last Updated**, and **Created**.
* **Configure Engine**  (gear) icon to [configure Engine](Set%20up%20LangSmith%20Engine.md#configure-engine).

Open [LangSmith Chat](../Test/Datasets%20%26%20Experiments/Analyze%20experiment%20results/LangSmith%20Chat.md#engine) to ask questions across your issues, for example, which issues need the most attention or how many new issues are open.

If no issues appear after setup completes, Engine found no recurring patterns in the analyzed traces. Try checking back after more traces have been collected.

### With the CLI

Use `langsmith project issues list` in the [LangSmith CLI](../Deploy/Get%20started/Reference/LangGraph%20CLI.md) to list a project's issues. Filter with `--status` (`open`, `fixing`, `watching`, `completed`, or `ignored`) and `--priority` (`urgent`, `high`, `medium`, or `low`), and page with `--limit` and `--offset`.

```bash
# List open, high-priority issues for a project
langsmith project issues list --project <project-name> --status open --priority high
```

## See also

* [LangSmith Engine](LangSmith%20Engine.md): How Engine detects issues and learns from your actions on them.
* [Set up Engine](Set%20up%20LangSmith%20Engine.md): Turn on Engine for a tracing project and configure what it focuses on.
* [Validate fixes automatically](Validate%20fixes%20automatically.md): Confirm that an issue reproduces and that Engine's fix resolves it.
* [Engine notifications](LangSmith%20Engine%20notifications.md): Get alerted in Slack, Jira, or a webhook when Engine finds issues.
* [Manage datasets](../Test/Datasets%20%26%20Experiments/Datasets/Manage%20datasets.md), [Use annotation queues](../Test/Annotation%20Queues/Use%20annotation%20queues.md), and [Use assertions](../Test/Annotation%20Queues/Use%20assertions.md): Work with the offline examples Engine generates.
* [LangSmith CLI](../Deploy/Get%20started/Reference/LangGraph%20CLI.md): List and manage issues programmatically.

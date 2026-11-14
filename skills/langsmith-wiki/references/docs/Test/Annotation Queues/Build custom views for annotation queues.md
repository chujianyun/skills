# Build custom views for annotation queues

> Build a custom view with LangSmith Chat to control how runs and threads appear to reviewers in an annotation queue.

A *custom view* replaces the default trace view in the middle pane of an [annotation queue](Use%20annotation%20queues.md) with a display you describe to [LangSmith Chat](../Datasets%20%26%20Experiments/Analyze%20experiment%20results/LangSmith%20Chat.md). Use one to show reviewers only what they need to score, such as a chat transcript without tool calls or a question-and-answer card.

A custom view is display only. It cannot call the LangSmith API or the network, and it does not change the item list, the rubric, or the feedback reviewers submit. Custom views are workspace resources, so one view can serve several queues.

Custom views succeed [custom output rendering](../Datasets%20%26%20Experiments/Datasets/Custom%20output%20rendering.md), which will be deprecated. A queue can use one or the other, not both.

> [!NOTE]
>
> Custom views are on by default on LangSmith Cloud. On self-hosted LangSmith, custom views require v0.18 or later, with [Chat enabled](../../LangSmith%20setup/Self-hosted/Install%20an%20instance/Configure%20Insights%20and%20Chat%20on%20self-hosted%20LangSmith.md).

## Requirements

* Creating, editing, renaming, or removing a queue's custom view requires the `annotation-queues:update` permission on that queue.
* Deleting a view from the workspace also requires the `annotation-queues:delete` permission.
* Custom views are available on [single-run annotation queues](Use%20annotation%20queues.md#single-run-annotation-queues) only, not on pairwise queues.

## Create a custom view

To create a custom view for a queue:

1. Open the annotation queue.
2. In the item header, turn on the **Custom view** toggle. If the queue has no view yet, the pane shows **No custom view configured for this annotation queue**.
3. Click **New custom view**. Chat opens and asks **What should reviewers see?**
4. Describe the view, or pick a suggestion such as **Show it as a chat conversation**, **Summarize as a Q\&A card**, or **Hide tool calls and system messages**.
5. Check the live preview, which renders the current queue item. Keep describing changes in Chat until the view looks right.
6. Click **Save**, enter a name in the **Name your custom view** dialog, and click **Save view**.

Nothing is saved until you click **Save**. To discard the draft, click **Cancel**.

One view renders every item in the queue. When a queue holds both runs and threads, ask Chat to handle both item types.

## Reuse a view across queues

To attach a view that already exists in the workspace, do one of the following:

* In the empty custom view pane, click **Use an existing view** and select the view.
* In the queue's settings, under **Custom View**, choose the view from the **Select a custom view** picker.

The settings picker is disabled while [custom output rendering](../Datasets%20%26%20Experiments/Datasets/Custom%20output%20rendering.md#for-annotation-queues) is on for the queue. Turn off custom output rendering to use a custom view.

## Edit or manage a view

With the **Custom view** toggle on, click **Edit** in the item header to open the view menu:

* **Edit current view**: Reopen Chat with the saved view and describe the changes.
* **Rename view**: Change the name. The new name shows on every queue that uses the view.
* **New custom view**: Build a different view for this queue.
* **Remove custom view**: Detach the view from this queue. The view stays in the workspace for other queues.
* **Delete view**: Delete the view from the workspace. This removes it from every queue that uses it and cannot be undone.

When you save edits to a view that other queues also use, LangSmith asks how to apply them:

* **Update for all queues**: Change the shared view everywhere it appears.
* **Save as new view**: Save a copy that only this queue uses.

## Switch between default and custom views

The **Custom view** toggle in the item header switches between the default trace view and the queue's custom view. When a queue has a custom view, reviewers start on it. LangSmith remembers each reviewer's choice per queue.

## See also

* [Use annotation queues](Use%20annotation%20queues.md)
* [LangSmith Chat](../Datasets%20%26%20Experiments/Analyze%20experiment%20results/LangSmith%20Chat.md)
* [Custom apps](../../Monitor/Observe/Monitoring%20%26%20alerting/Custom%20Apps.md)

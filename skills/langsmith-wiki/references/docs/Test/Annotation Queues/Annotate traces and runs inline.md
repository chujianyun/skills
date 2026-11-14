# Annotate traces and runs inline

LangSmith allows you to manually annotate traces with feedback within the application. This can be useful for adding context to a trace, such as a user's comment or a note about a specific issue.
You can annotate a trace either inline or by sending the trace to an annotation queue, which allows you to closely inspect and log feedbacks to runs one at a time.
Feedback tags are associated with your [workspace](../../LangSmith%20setup/Govern/Organization/Overview.md#workspaces).

To ask [LangSmith Engine](../../Engine/LangSmith%20Engine.md) to review a trace instead, click **Flag for Engine** in the trace view. For more information, see [Flag a trace for Engine](../../Engine/Find%20and%20fix%20your%20agent%27s%20issues%20with%20LangSmith%20Engine.md#flag-a-trace-for-engine).

> [!NOTE]
>
> **You can attach user feedback to ANY intermediate run (span) of the trace, not just the root span.**
>
> This is useful for critiquing specific parts of the LLM application, such as the retrieval step or generation step of the RAG pipeline.

To annotate a trace inline, open the three-dot menu (`...`) in the trace view for any particular run that is part of the trace, then click **Notes**.

This will open up a pane that allows you to choose from feedback tags associated with your workspace and add a score for particular tags. You can also add a standalone comment. Follow [Set up feedback criteria](Set%20up%20feedback%20criteria.md) to set up feedback tags for your workspace.
You can also set up new feedback criteria from within the pane itself.

Inline feedback and notes in the LangSmith UI do not change the trace's [retention tier](../../Monitor/Trace/Configuration%20%26%20troubleshooting/Usage%20and%20billing.md#data-retention-auto-upgrades); the trace keeps the retention configured for its project unless another action explicitly extends retention.

![Annotation sidebar](../../../assets/images/22ce08d360ca-annotation-sidebar.png)

You can use the labeled keyboard shortcuts to streamline the annotation process.

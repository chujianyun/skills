# SmithDB feature availability

> LangSmith features that are unavailable on self-hosted installations that query ClickHouse, and what still works without SmithDB.

Some LangSmith features read trace data only from [SmithDB](Overview/Enable%20SmithDB%20on%20self-hosted%20LangSmith.md). On a self-hosted installation that still queries ClickHouse, these features are hidden, disabled, or fall back to an older experience. Use this page to see what you gain by moving queries to SmithDB, and what keeps working if you have not.

> [!NOTE]
>
> ClickHouse support ends in LangSmith v0.19. For upgrade timing, see the [self-hosted changelog](../Reference/Self-hosted%20LangSmith%20changelog.md).

## Check whether queries use SmithDB

The features on this page turn on when LangSmith [queries SmithDB](Install%20SmithDB/Install%20LangSmith%20with%20SmithDB.md#step-6-switch-queries-to-smithdb). [Dual ingestion](Install%20SmithDB/Install%20LangSmith%20with%20SmithDB.md#step-4-enable-dual-ingestion) alone does not enable them. To check the current setting, read the `sdb_query_enabled` instance flag:

```bash
curl -s https://LANGSMITH_HOST/api/v1/info | jq '.instance_flags | {sdb_ingestion_enabled, sdb_query_enabled}'
```

SmithDB is necessary but not always sufficient. A feature can also depend on your LangSmith version, and some features roll out to self-hosted installations after they reach LangSmith Cloud. Each feature's page states its own version and region availability.

## Features that require SmithDB

Several rows cover a newer version of a feature that also works without SmithDB. The last column lists what you can still use on an installation that queries ClickHouse.

| Feature | What requires SmithDB | What works without SmithDB |
| - | - | - |
| [Filter query syntax](../../../Monitor/Debug/Viewing%20%26%20managing%20traces/Filter%20traces.md#query-syntax) | The filter search bar and `field:value` query syntax, with thread, root run, single run, and any run scopes. | Filtering with legacy function-style filters. |
| [Custom dashboard chart editor](../../../Monitor/Observe/Monitoring%20%26%20alerting/Monitor%20projects%20with%20dashboards.md#custom-dashboards) | The current chart editor, with templates, ratios, per-series filters, grouping, breakdowns, and chart drilldowns. | Creating custom dashboards and charts with [custom dashboards (legacy)](../../../Monitor/Observe/Monitoring%20%26%20alerting/Monitor%20projects%20with%20dashboards.md#custom-dashboards-legacy), and prebuilt dashboards. |
| [Trajectory view](../../../Monitor/Debug/Viewing%20%26%20managing%20traces/View%20traces.md#trajectory-view) | The deduplicated conversation across turns, model calls, tools, and subagents. Also powers the Markdown export of a thread and parsed messages in experiment run details. | Trace inspection and message rendering for a single run. |
| [Trajectory evaluators](../../../Monitor/Observe/Online%20evaluators/Set%20up%20multi-turn%20online%20evaluators.md#evaluate-trajectories) | Online evaluators that use the `trajectory` variable to score the full agent path, including child model and tool calls. | Run evaluators and thread evaluators that read root-run messages. |
| [Threads in annotation queues](../../../Test/Annotation%20Queues/Use%20annotation%20queues.md#assign-runs-and-threads-to-a-single-run-queue) | Adding a thread to an annotation queue from the thread view, and reviewing a thread item, which displays its trajectory. | Run-level annotation queues. |
| [Trajectory review in annotation queues](../../../Test/Annotation%20Queues/Use%20annotation%20queues.md#review-a-single-run-queue) | Opening a queued run in the Trajectory view, on the graded turn. | Reviewing a run's inputs and outputs, with tool calls collapsed. |
| [Threads in datasets](../../../Test/Datasets%20%26%20Experiments/Datasets/Create%20a%20dataset/Create%20and%20manage%20datasets%20in%20the%20UI.md#manually-from-a-tracing-project) | Adding selected threads, including thread items from an annotation queue, to a dataset as conversation examples. | Adding runs to a dataset. |
| [Thread automation rules](../../../Monitor/Observe/Automations/Set%20up%20automation%20rules.md#set-the-item-type-to-runs-or-threads) | Creating thread rules that add threads to annotation queues or datasets, or send [webhooks](../../../Monitor/Observe/Automations/Configure%20webhook%20notifications%20for%20rules.md#read-a-thread-rule-payload). Backfilling a thread rule over historical data. | Run automation rules. |
| Public thread sharing | Sharing a whole thread with a public link. | Sharing a single trace with a public link. |
| Large trace actions | The paginated trace tree for large traces, downloading a whole trace as JSON, and deleting a whole trace from the trace details page. | Viewing traces, downloading individual runs, and existing deletion workflows. |
| [LLM Gateway usage](../../../LLM%20Gateway/Observability/Monitor%20LLM%20Gateway%20spend.md) | The **Usage** dashboard: spend summary, charts, breakdowns, filters, and drilldowns. | Gateway routing and [policies](../../../LLM%20Gateway/Governance/Spend%20policies.md). |
| Agent trace volume | Trace-count sparklines on agent overview cards and the trace volume chart on an agent's overview. | Agent deployment, management, and other agent statistics. |
| [Bulk export filters](../../../Monitor/Debug/Bulk%20export%20trace%20data/Bulk%20export%20trace%20data.md#2-create-an-export-job) | Filtering exported runs with the `field:value` query syntax. | Filtering exported runs with function-style filters. |
| [Feedback in bulk exports](../../../Monitor/Debug/Bulk%20export%20trace%20data/Bulk%20export%20trace%20data.md#limit-exported-fields) | Exporting the `feedbacks` field, which holds feedback keys and comments. | Bulk exports of every other field. |

Tracing, thread listing, datasets, and experiments work on either datastore.

## See also

* [Enable SmithDB on self-hosted LangSmith](Overview/Enable%20SmithDB%20on%20self-hosted%20LangSmith.md)
* [Install SmithDB](Install%20SmithDB/Install%20LangSmith%20with%20SmithDB.md)
* [Migrate ClickHouse history to SmithDB](Install%20SmithDB/Migrate%20ClickHouse%20history%20to%20SmithDB.md)
* [Migrate to SmithDB-backed APIs](../../../Monitor/Reference/SmithDB%20API%20migration/Migrate%20to%20SmithDB-backed%20APIs.md)

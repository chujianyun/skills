# Granular billable usage

> Retrieve detailed trace and Agent Server usage data broken down by workspace, project, user, or API key.

> [!NOTE]
>
> **Trace usage:** For LangSmith [Cloud](../../Cloud/Cloud%20%28SaaS%29.md), granular billable trace data collection started on January 5, 2026. Data is not available for traces ingested before this date.
>
> For [Self-hosted](../../Self-hosted/Self-hosted%20LangSmith.md) instances, trace data collection begins when the feature is enabled via the following environment variables, or after [upgrading to a version with it enabled by default](../../Self-hosted/Reference/Self-hosted%20LangSmith%20changelog.md#langsmith-0-13-12).
>
> ```env theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> DEFAULT_ORG_FEATURE_ENABLE_GRANULAR_USAGE_REPORTING=true
> GRANULAR_USAGE_TABLE_ENABLED=true
> ```
>
> Starting with self-hosted version 0.16.0, long-lived trace usage is no longer tracked for [Self-hosted](../../Self-hosted/Self-hosted%20LangSmith.md) deployments. The **Long-lived only** retention filter always shows zero results for these deployments.
>
> **Agent Server usage** uses a separate data source. For more details, refer to the [Agent Server usage section](Granular%20billable%20usage.md#langsmith-deployment-usage-kind%3Dlangsmith_deployments).

LangSmith provides granular billable usage APIs that let you retrieve detailed usage data broken down by workspace, project, user, or API key. Two billable domains are supported by the same endpoint, selected via a `kind` query parameter:

* **Trace usage** (`kind=traces`, default): number of traces ingested.
* **Agent Server usage** (`kind=langsmith_deployments`): nodes executed, agent runs, and agent uptime for [LangSmith Agent Server](Manage%20billing%20in%20your%20account.md).

Both kinds share the same query parameters (time range, workspace filter, grouping dimension) and return the same time-bucketed shape. The data sources are separate, so a record returned by one kind will not appear in the other.

These APIs enable you to:

* Track usage across different teams or [workspaces](../../Govern/Organization/Overview.md).
* Identify which users or [API keys](../Create%20an%20account%20and%20API%20key.md#api-keys) are consuming the most traces or running the most agents.
* Analyze usage patterns over time.
* Export usage data for internal reporting.

## Prerequisites

* You must have the [`organization:read` permission](../../Govern/Users%20%26%20access%20control/Organization%20and%20workspace%20operations%20reference.md) to access granular usage data.
* You can only view usage for workspaces you have read access to.

## View in the UI

You can also view granular usage data in the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-granular-usage):

1. Navigate to **Settings** > **Billing and Usage**
2. Select the **Granular Usage** tab
3. Switch between the **LangSmith Traces** and **Agent Server** sub-tabs to view each domain. The active sub-tab is reflected in the URL (`?tab=traces` or `?tab=agent_server`) so you can bookmark the page to land on the same view.
4. Use the controls to:
   * Select a time range (Last 7 days, 30 days, 3 months, 6 months, 1 year, or custom)
   * Group by workspace, project, user, or API key
   * Filter to specific workspaces
   * On the **LangSmith Traces** tab, optionally filter by retention tier (`All Retention` / `Long-lived only` / `Short-lived only`)
5. Click **Export CSV** to download the data for the active tab.

Time range and workspace filters are shared across both sub-tabs, switching tabs preserves what you've selected. The **Agent Server** tab shows three stat cards (Total Nodes Executed / Total Agent Runs / Total Agent Uptime (seconds)) and one chart per metric stacked vertically, since the three metrics use different units.

## Query parameters

The granular usage endpoint accepts the following query parameters:

| Parameter | Type | Required | Description |
| - | - | - | - |
| `start_time` | datetime | Yes | Start of the time range (ISO 8601 format). |
| `end_time` | datetime | Yes | End of the time range. Must be after `start_time`. |
| `workspace_ids` | array of UUIDs | Yes | Filter results to specific workspaces. |
| `kind` | string | No | `traces` (default) or `langsmith_deployments`. Selects the billable domain. |
| `group_by` | string | No | Dimension to group by. One of: `workspace`, `project`, `user`, `api_key`. Default: `workspace`. |
| `trace_tier` | string | No | Trace-only retention filter: `longlived` or `shortlived`. Omit for all retention. Ignored when `kind=langsmith_deployments`. |

### Day-granular contract

Usage data is aggregated at day granularity. The endpoint normalizes the window to whole days at the API layer:

* `start_time` is rounded down to its day's UTC midnight.
* `end_time` is rounded up to the next UTC midnight (no-op when already at midnight).
* Any day overlapping the requested window is included in full.

A 24-hour window from `2026-01-01T12:00:00Z` to `2026-01-02T12:00:00Z` therefore returns usage for the full Jan 1 and Jan 2 buckets.

### Stride

The `stride` field in each response indicates the time bucket size used for aggregation, calculated from the requested time range. Daily is the minimum. Sub-day windows still bucket at one day.

| Time range | Aggregation | Stride |
| - | - | - |
| Up to 31 days | Daily | `days: 1` |
| 32–93 days (\~3 months) | Weekly | `days: 7` |
| 94–366 days (\~1 year) | Monthly | `days: 30` |
| More than 366 days | Yearly | `days: 365` |

### Compatibility

`kind=langsmith_deployments` combined with `group_by=trace_tier` returns `400 Bad Request`. Retention tiers only apply to traces.

## API endpoint

```
GET /api/v1/orgs/current/billing/granular-usage
```

Existing callers that omit `kind` continue to get trace usage with the same response shape they always did.

### Trace usage (`kind=traces`)

#### Response

```json
{
  "stride": {
    "days": 1,
    "hours": 0
  },
  "usage": [
    {
      "time_bucket": "2026-01-15T00:00:00Z",
      "dimensions": {
        "workspace_id": "uuid",
        "workspace_name": "My Workspace"
      },
      "traces": 1500
    }
  ]
}
```

#### Example: Get trace usage by workspace

```python Python
import httpx
from datetime import datetime, timedelta, timezone

client = httpx.Client(
    base_url="https://api.smith.langchain.com",
    headers={"x-api-key": "<your-api-key>"}
)

end_time = datetime.now(timezone.utc)
start_time = end_time - timedelta(days=30)

response = client.get(
    "/api/v1/orgs/current/billing/granular-usage",
    params={
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "workspace_ids": ["<workspace-id>"],
        "group_by": "workspace",
    },
)

data = response.json()
for record in data["usage"]:
    print(f"{record['time_bucket']}: {record['traces']} traces")
```

```typescript TypeScript
const response = await fetch(
  `https://api.smith.langchain.com/api/v1/orgs/current/billing/granular-usage?` +
  new URLSearchParams({
    start_time: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString(),
    end_time: new Date().toISOString(),
    workspace_ids: "<workspace-id>",
    group_by: "workspace",
  }),
  {
    headers: {
      "x-api-key": "<your-api-key>",
    },
  }
);

const data = await response.json();
for (const record of data.usage) {
  console.log(`${record.time_bucket}: ${record.traces} traces`);
}
```

```bash cURL
curl -X GET "https://api.smith.langchain.com/api/v1/orgs/current/billing/granular-usage?\
start_time=2026-01-01T00:00:00Z&\
end_time=2026-01-15T00:00:00Z&\
workspace_ids=<workspace-id>&\
group_by=workspace" \
  -H "x-api-key: <your-api-key>"
```

#### Example: Get trace usage by user, filtered to long-lived retention only

```python Python
response = client.get(
    "/api/v1/orgs/current/billing/granular-usage",
    params={
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "workspace_ids": ["<workspace-id>"],
        "group_by": "user",
        "trace_tier": "longlived",
    },
)

data = response.json()
for record in data["usage"]:
    user_email = record["dimensions"].get("user_email", "Unknown")
    print(f"{user_email}: {record['traces']} long-lived traces")
```

### Agent Server usage (`kind=langsmith_deployments`)

Each record carries three metrics together so a single fetch powers the whole Agent Server view.

> [!NOTE]
>
> **Agent Server usage** is sourced separately from trace usage and is available for the full retention window of your Agent Server usage.
>
> For self-hosted instances, the Agent Server usage endpoint is opt-in. Enable it via:
>
> ```env theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> REMOTE_METRICS_ROLLUP_ENABLED=true
> ```
>
> Or upgrade to a LangSmith version that enables it by default (see [self-hosted changelog](../../Self-hosted/Reference/Self-hosted%20LangSmith%20changelog.md)).

#### Response

```json
{
  "stride": {
    "days": 1,
    "hours": 0
  },
  "usage": [
    {
      "time_bucket": "2026-01-15T00:00:00Z",
      "dimensions": {
        "workspace_id": "uuid",
        "workspace_name": "My Workspace"
      },
      "nodes_executed": 12500,
      "agent_runs": 320,
      "agent_uptime_seconds": 86400
    }
  ]
}
```

| Field | Description |
| - | - |
| `nodes_executed` | Total LangGraph nodes executed in the time bucket. |
| `agent_runs` | Total agent runs (graph invocations) in the time bucket. |
| `agent_uptime_seconds` | Total replica uptime, in seconds, summed across Agent Server replicas. The deduplicated standby minutes used for invoicing is computed separately by the billing pipeline; this field is the raw sum surfaced for breakdown and analysis. |

#### Example: Get Agent Server usage by workspace

```python Python
response = client.get(
    "/api/v1/orgs/current/billing/granular-usage",
    params={
        "kind": "langsmith_deployments",
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "workspace_ids": ["<workspace-id>"],
        "group_by": "workspace",
    },
)

data = response.json()
for record in data["usage"]:
    print(
        f"{record['time_bucket']}: "
        f"{record['nodes_executed']} nodes, "
        f"{record['agent_runs']} runs, "
        f"{record['agent_uptime_seconds']}s uptime"
    )
```

```typescript TypeScript
const response = await fetch(
  `https://api.smith.langchain.com/api/v1/orgs/current/billing/granular-usage?` +
  new URLSearchParams({
    kind: "langsmith_deployments",
    start_time: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString(),
    end_time: new Date().toISOString(),
    workspace_ids: "<workspace-id>",
    group_by: "workspace",
  }),
  {
    headers: {
      "x-api-key": "<your-api-key>",
    },
  }
);

const data = await response.json();
for (const record of data.usage) {
  console.log(
    `${record.time_bucket}: ${record.nodes_executed} nodes, ` +
    `${record.agent_runs} runs, ${record.agent_uptime_seconds}s uptime`
  );
}
```

```bash cURL
curl -X GET "https://api.smith.langchain.com/api/v1/orgs/current/billing/granular-usage?\
kind=langsmith_deployments&\
start_time=2026-01-01T00:00:00Z&\
end_time=2026-01-15T00:00:00Z&\
workspace_ids=<workspace-id>&\
group_by=workspace" \
  -H "x-api-key: <your-api-key>"
```

## CSV export

```
GET /api/v1/orgs/current/billing/granular-usage/export
```

Same query parameters as the data endpoint, including `kind`. Returns a CSV file with one row per (time bucket, dimension) tuple. All dimension columns are always present; only the columns matching the selected `group_by` are populated.

For `kind=traces`, the value column is `Traces`. For `kind=langsmith_deployments`, the value columns are `Nodes Executed`, `Agent Runs`, and `Agent Uptime (seconds)`.

| Column | Present when |
| - | - |
| Time Bucket Start | Always |
| Time Bucket End | Always |
| Workspace ID / Name | Always (populated when `group_by=workspace`) |
| Project ID / Name | Always (populated when `group_by=project`) |
| User ID / Email | Always (populated when `group_by=user`) |
| API Key Short Key | Always (populated when `group_by=api_key`) |
| Traces | `kind=traces` |
| Nodes Executed / Agent Runs / Agent Uptime (seconds) | `kind=langsmith_deployments` |

Cells whose value would start with `=`, `+`, `-`, `@`, tab, or carriage-return are tab-prefixed to neutralize spreadsheet formula evaluation in Excel / Google Sheets / LibreOffice.

```python Python
response = client.get(
    "/api/v1/orgs/current/billing/granular-usage/export",
    params={
        "kind": "langsmith_deployments",
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "workspace_ids": ["<workspace-id>"],
        "group_by": "workspace",
    },
)

with open("deployment_usage_report.csv", "wb") as f:
    f.write(response.content)
```

```bash cURL
curl -X GET "https://api.smith.langchain.com/api/v1/orgs/current/billing/granular-usage/export?\
kind=langsmith_deployments&\
start_time=2026-01-01T00:00:00Z&\
end_time=2026-01-15T00:00:00Z&\
workspace_ids=<workspace-id>&\
group_by=workspace" \
  -H "x-api-key: <your-api-key>" \
  -o deployment_usage_report.csv
```

## Grouping options

The `group_by` parameter determines how usage data is aggregated:

| Value | Description | Dimensions returned | Available for |
| - | - | - | - |
| `workspace` | Group by workspace | `workspace_id`, `workspace_name` | Both kinds |
| `project` | Group by project | `project_id`, `project_name` | Both kinds |
| `user` | Group by user | `user_id`, `user_email` | Both kinds |
| `api_key` | Group by API key | `api_key_short_key` | Both kinds |

For trace usage, "project" refers to the [LangSmith tracer session](../../../Monitor/Trace/Observability%20concepts.md). For Agent Server usage, "project" refers to the Agent Server (a deployed agent).

In an [agent-based workspace](../../Overview/Agent-based%20workspaces/Agent%20Registry.md), grouping by project is the closest the export gets to an agent, because there is no agent or environment dimension. Each trace usage row covers one [environment](../../Overview/Agent-based%20workspaces/Agent%20environments.md) of one agent, so totaling an agent's usage means summing its environment rows. LangSmith names the tracing project it creates for an environment `<agent>-<environment>`, for example `support-triage-production`, while a project that predates the agent keeps the name it already had.

## Related resources

* [Manage billing in your account](Manage%20billing%20in%20your%20account.md)
* [Organization and workspace operations](../../Govern/Users%20%26%20access%20control/Organization%20and%20workspace%20operations%20reference.md)

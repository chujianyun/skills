# Bulk export trace data

> Export LangSmith trace data to an S3-compatible bucket in Parquet format.

> [!NOTE]
>
> **Plan restrictions apply**
>
> For customers who signed up after August 3, 2026, bulk export is only available on the [LangSmith Enterprise plan](https://www.langchain.com/pricing). Customers who signed up on or before August 3, 2026, can use bulk export on Plus or Enterprise plans until February 1, 2027.

LangSmith's bulk data export lets you export trace data from a specific project and date range to an S3-compatible bucket in [Parquet](https://parquet.apache.org/docs/overview/) format, matching the fields in the [Run data format](../Data%20type%20reference/Run%20%28span%29%20data%20format.md). This is useful for offline analysis in tools like BigQuery, Snowflake, Redshift, or Jupyter notebooks.

This page covers how to:

* Create an export destination.
* Create and configure an export job, including scheduled exports and field filtering.
* Monitor export progress.

## Before you start

Exports may take some time depending on data volume, and LangSmith limits how many exports can run concurrently. Bulk exports have a 72-hour runtime timeout. Refer to [Automatic retry behavior](Monitor%20and%20troubleshoot%20bulk%20exports.md#automatic-retry-behavior) for details. Once launched, LangSmith handles orchestration and [resilience of the export process](Monitor%20and%20troubleshoot%20bulk%20exports.md#failure-modes-and-retry-policy) automatically.

## 1. Create a destination

The destination tells LangSmith where to write your exported data. Before making this request, you will need:

* Your [LangSmith API key](../../../LangSmith%20setup/Account/Create%20an%20account%20and%20API%20key.md) and [workspace ID](../../../LangSmith%20setup/Govern/Organization/Workspace%20setup/Set%20up%20hierarchy.md#set-up-a-workspace).
* An S3 or S3-compatible bucket with **write access** granted to LangSmith (refer to [Permissions required](Manage%20bulk%20export%20destinations.md#permissions-required)).
* The bucket name, prefix, and either the AWS region (for AWS S3) or the endpoint URL (for GCS, MinIO, or other S3-compatible providers).
* An access key and secret key for the bucket.

```bash
curl --request POST \
  --url 'https://api.smith.langchain.com/api/v1/bulk-exports/destinations' \
  --header 'Content-Type: application/json' \
  --header 'X-API-Key: YOUR_API_KEY' \
  --header 'X-Tenant-Id: YOUR_WORKSPACE_ID' \
  --data '{
    "destination_type": "s3",
    "display_name": "My S3 Destination",
    "config": {
      "bucket_name": "your-s3-bucket-name",
      "prefix": "root_folder_prefix",
      "region": "your aws s3 region",
      "endpoint_url": "your endpoint url for s3 compatible buckets"
    },
    "credentials": {
      "access_key_id": "YOUR_S3_ACCESS_KEY_ID",
      "secret_access_key": "YOUR_S3_SECRET_ACCESS_KEY"
    }
  }'
```

Credentials are stored securely in encrypted form. The API will validate that the destination and credentials are valid before saving. If the request fails, refer to [Debug destination errors](Manage%20bulk%20export%20destinations.md#debug-destination-errors).

Save the `id` from the response; you will need it when creating an export job.

Refer to [Manage bulk export destinations](Manage%20bulk%20export%20destinations.md) for permissions setup, provider-specific configuration (AWS S3, GCS, MinIO), and credential options.

## 2. Create an export job

An export job targets a project (or all experiments in a workspace) and a date range. You will need:

* The destination `id` from the [previous step](#1-create-a-destination).
* Either a project ID (`session_id`) or `"all_experiments": true`. Copy the project ID from the individual project view in the [**Tracing Projects** list](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-data-export).
* A `start_time` and `end_time` in UTC ISO 8601 format.

```bash
curl --request POST \
  --url 'https://api.smith.langchain.com/api/v1/bulk-exports' \
  --header 'Content-Type: application/json' \
  --header 'X-API-Key: YOUR_API_KEY' \
  --header 'X-Tenant-Id: YOUR_WORKSPACE_ID' \
  --data '{
    "bulk_export_destination_id": "your_destination_id",
    "session_id": "project_uuid",
    "start_time": "2024-01-01T00:00:00Z",
    "end_time": "2024-01-03T00:00:00Z",
    "format_version": "v2_beta"
  }'
```

The `start_time` is inclusive and `end_time` is exclusive. The export will include all runs where `run.start_time >= start_time` and `run.start_time < end_time`.

Save the `id` from the response to monitor the export's progress.

You can optionally add a `filter` expression to narrow the set of runs exported. Refer to the [filter query language](../Viewing%20%26%20managing%20traces/Trace%20query%20syntax.md#filter-query-language) and [examples](../Viewing%20%26%20managing%20traces/Query%20traces%20using%20the%20SDK.md#use-filter-query-language) for syntax. Not setting the `filter` field will export all runs.

On exports that read from SmithDB, `filter` also accepts the [search bar query syntax](../Viewing%20%26%20managing%20traces/Filter%20traces.md#query-syntax), for example `run_type:llm AND status:error`. The filter matches individual runs, like the **Single run** scope.

LangSmith checks the filter when you create the export and rejects an invalid one with a `400` error. Filters can be at most 5,000 characters long.

> [!NOTE]
>
> Search bar syntax in bulk export filters is available on LangSmith Cloud and on self-hosted LangSmith with [SmithDB](../../../LangSmith%20setup/Self-hosted/SmithDB/SmithDB%20feature%20availability.md), Helm version `0.18.0-rc.50` or later (application version `0.18.19rc1` or later). Other installations accept only the [filter query language](../Viewing%20%26%20managing%20traces/Trace%20query%20syntax.md#filter-query-language).

> [!NOTE]
>
> **LangSmith Cloud limit: 250 bulk export creations per hour per workspace**
>
> On [LangSmith cloud](../../../LangSmith%20setup/Cloud/Cloud%20%28SaaS%29.md), each workspace can create at most 250 bulk exports per hour. This budget includes one-off exports and exports spawned by [scheduled bulk exports](#schedule-recurring-exports), so a workspace with many active schedules consumes part of the hourly budget automatically.
>
> If your workspace reaches the limit, new create requests will be rejected with a 429 until earlier creates age past the rolling 60-minute window. To raise the limit, contact support via [support.langchain.com](https://support.langchain.com).
>
> [Self-hosted LangSmith](../../../LangSmith%20setup/Self-hosted/Self-hosted%20LangSmith.md) does not enforce this limit by default.

### Export all experiments

To export every experiment in the workspace instead of targeting a single project with `session_id`, set `all_experiments: true`. LangSmith creates an experiment whenever you run an evaluation against a dataset, any tracing project with `reference_dataset_id` set qualifies.

`all_experiments` and `session_id` are mutually exclusive—set exactly one.

```bash
curl --request POST \
  --url 'https://api.smith.langchain.com/api/v1/bulk-exports' \
  --header 'Content-Type: application/json' \
  --header 'X-API-Key: YOUR_API_KEY' \
  --header 'X-Tenant-Id: YOUR_WORKSPACE_ID' \
  --data '{
    "bulk_export_destination_id": "your_destination_id",
    "all_experiments": true,
    "start_time": "2024-01-01T00:00:00Z",
    "end_time": "2024-02-01T00:00:00Z",
    "format_version": "v2_beta"
  }'
```

LangSmith resolves the set of experiment sessions at run time, so the export picks up any experiments you create after submitting the job but before the orchestrator starts processing.

The same `all_experiments` flag works with [scheduled exports](#schedule-recurring-exports)—include `interval_hours` and omit `end_time` instead of supplying `end_time`.

> [!NOTE]
>
> **Cloud limit: 250 experiments per export**
>
> On [LangSmith cloud](../../../LangSmith%20setup/Cloud/Cloud%20%28SaaS%29.md), each `all_experiments` export includes at most 250 experiments. To export more:
>
> * Query the completed `all_experiments` export to see which tracing projects were included, then create standard bulk exports with `session_id` for the remaining experiments.
> * Or, contact support via [support.langchain.com](https://support.langchain.com) to request a higher limit for your workspace.
>
> [Self-hosted LangSmith](../../../LangSmith%20setup/Self-hosted/Self-hosted%20LangSmith.md) has no per-export limit.

### Schedule recurring exports

> [!NOTE]
>
> Requires LangSmith Helm version `0.10.42` or later (application version `0.10.109` or later)

Scheduled exports collect runs periodically and export to the configured destination. To create a scheduled export, include `interval_hours` and omit `end_time`:

```bash
curl --request POST \
  --url 'https://api.smith.langchain.com/api/v1/bulk-exports' \
  --header 'Content-Type: application/json' \
  --header 'X-API-Key: YOUR_API_KEY' \
  --header 'X-Tenant-Id: YOUR_WORKSPACE_ID' \
  --data '{
    "bulk_export_destination_id": "your_destination_id",
    "session_id": "project_uuid",
    "start_time": "2024-01-01T00:00:00Z",
    "interval_hours": 1,
    "format_version": "v2_beta"
  }'
```

* `interval_hours` must be between 1 and 168 (1 week) inclusive.
* `end_time` must be omitted for scheduled exports; it is still required for one-time exports.
* Each spawned export covers `start_time` to `start_time + interval_hours`, then advances by `interval_hours` for each subsequent run. Since `end_time` is exclusive, consecutive exports do not overlap.
* Spawned exports run at `end_time + 10 minutes` to account for runs submitted with `end_time` in the recent past.
* Spawned exports have the `source_bulk_export_id` attribute filled. If desired, they must be cancelled separately—cancelling the source export **does not** cancel already-spawned exports.
* To stop a scheduled export, [cancel it](Monitor%20and%20troubleshoot%20bulk%20exports.md#stop-an-export).

> [!NOTE]
>
> **LangSmith Cloud limit: 200 scheduled bulk exports per workspace**
>
> On [LangSmith cloud](../../../LangSmith%20setup/Cloud/Cloud%20%28SaaS%29.md), each workspace can have at most 200 active **scheduled** (recurring) bulk exports at a time. That is, exports configured with an `interval_hours` value. The limit caps the number of **schedules**, not the number of times they run: a schedule that has produced thousands of historical export runs still counts as one.
>
> One-off (non-recurring) bulk exports are not subject to this limit.
>
> If your workspace reaches the limit, new scheduled export requests will be rejected with a `429` until you [cancel](Monitor%20and%20troubleshoot%20bulk%20exports.md#stop-an-export) an existing schedule. To raise the limit, contact support via [support.langchain.com](https://support.langchain.com).
>
> [Self-hosted LangSmith](../../../LangSmith%20setup/Self-hosted/Self-hosted%20LangSmith.md) does not enforce this limit by default.

**Example**

If a scheduled bulk export is created with `start_time=2025-07-16T00:00:00Z` and `interval_hours=6`:

| Export | Start Time | End Time | Runs At |
| - | - | - | - |
| 1 | 2025-07-16T00:00:00Z | 2025-07-16T06:00:00Z | 2025-07-16T06:10:00Z |
| 2 | 2025-07-16T06:00:00Z | 2025-07-16T12:00:00Z | 2025-07-16T12:10:00Z |
| 3 | 2025-07-16T12:00:00Z | 2025-07-16T18:00:00Z | 2025-07-16T18:10:00Z |

### Limit exported fields

> [!NOTE]
>
> Requires LangSmith Helm version `0.12.11` or later (application version `0.12.42` or later). Supported in both one-time and scheduled exports.

You can improve export speed and reduce file size by limiting which fields are included using the `export_fields` parameter. If you omit `export_fields`, all fields except `feedbacks` are included.

Feedback comments are opt-in. To include them, explicitly add `feedbacks` to `export_fields` along with the other relevant fields.

```bash
curl --request POST \
  --url 'https://api.smith.langchain.com/api/v1/bulk-exports' \
  --header 'Content-Type: application/json' \
  --header 'X-API-Key: YOUR_API_KEY' \
  --header 'X-Tenant-Id: YOUR_WORKSPACE_ID' \
  --data '{
    "bulk_export_destination_id": "your_destination_id",
    "session_id": "project_uuid",
    "start_time": "2024-01-01T00:00:00Z",
    "end_time": "2024-01-03T00:00:00Z",
    "export_fields": ["id", "name", "run_type", "start_time", "end_time", "status", "total_tokens", "total_cost"],
    "is_rollup_disabled": true,
    "format_version": "v2_beta"
  }'
```

> [!TIP]
>
> Excluding `inputs` and `outputs` can significantly improve export performance and reduce file sizes, especially for large runs. Only include these fields if you need them for your analysis.
>
> If your export includes token or cost fields, which it does by default, setting `is_rollup_disabled` to `true` can also speed it up because LangSmith skips computing trace-level rollups. Root runs then carry their own token and cost values instead of totals for the whole trace. `is_rollup_disabled` defaults to `false` and applies only to exports that read from SmithDB.

### Compression

Set the `compression` field to control how exported Parquet files are compressed. When omitted, LangSmith uses `zstandard`.

Allowed values: `zstandard`, `gzip`, `snappy`, `none`. Use `snappy` when loading into BigQuery, see [Export trace data to BigQuery](Export%20trace%20data%20to%20BigQuery.md).

> [!NOTE]
>
> As of Helm chart 0.17.0, [Self-hosted LangSmith](../../../LangSmith%20setup/Self-hosted/Self-hosted%20LangSmith.md) also defaults to `zstandard` when `compression` is omitted. On chart 0.16 and earlier, self-hosted defaults to `gzip`. To override the default, set the `FF_BULK_EXPORT_DEFAULT_COMPRESSION` environment variable.

### Exportable fields

By default, bulk exports include the following fields for each run:

**Identifiers & hierarchy:**

| Field | Description |
| - | - |
| `id` | Run ID |
| `tenant_id` | Workspace/tenant ID |
| `session_id` | Project/session ID |
| `trace_id` | Trace ID |
| `parent_run_id` | Parent run ID |
| `parent_run_ids` | List of all parent run IDs |
| `reference_example_id` | Reference to example if part of a dataset |

**Basic metadata:**

| Field | Description |
| - | - |
| `name` | Run name |
| `run_type` | Type of run (e.g., "chain", "llm", "tool") |
| `start_time` | Start timestamp (UTC) |
| `end_time` | End timestamp (UTC) |
| `status` | Run status (e.g., "success", "error") |
| `is_root` | Whether this is a root-level run |
| `dotted_order` | Hierarchical ordering string |
| `trace_tier` | Trace tier/retention level |

**Run data:**

| Field | Description |
| - | - |
| `inputs` | Run inputs (JSON) |
| `outputs` | Run outputs (JSON) |
| `error` | Error message if failed |
| `extra` | Extra metadata (JSON) |
| `events` | Run events (JSON) |

**Tags & feedback:**

| Field | Description |
| - | - |
| `tags` | List of tags |
| `feedback_stats` | Feedback statistics (JSON). Refer to the following note for aggregation limitations. |
| `feedbacks` | Feedback comments and keys (JSON) |

> [!NOTE]
>
> **`feedback_stats` aggregation limitation**
>
> The `feedback_stats` field only includes value breakdowns for string-type feedback. Feedback with non-string values (numeric, boolean, complex types) is excluded from these breakdowns. To analyze non-string feedback values, export the raw feedback data separately.

**Token usage & costs:**

| Field | Description |
| - | - |
| `total_tokens` | Total token count |
| `prompt_tokens` | Prompt token count |
| `completion_tokens` | Completion token count |
| `total_cost` | Total cost |
| `prompt_cost` | Prompt cost |
| `completion_cost` | Completion cost |
| `first_token_time` | Time to first token |

### Partitioning scheme

Data is exported into your bucket using the following Hive partitioned structure:

```
<bucket>/<prefix>/export_id=<export_id>/tenant_id=<tenant_id>/session_id=<session_id>/runs/year=<year>/month=<month>/day=<day>
```

## 3. Monitor your export

Poll the export status using the `id` from the [previous step](#2-create-an-export-job):

```bash
curl --request GET \
  --url 'https://api.smith.langchain.com/api/v1/bulk-exports/{export_id}' \
  --header 'Content-Type: application/json' \
  --header 'X-API-Key: YOUR_API_KEY' \
  --header 'X-Tenant-Id: YOUR_WORKSPACE_ID'
```

The `status` field in the response will be one of `CREATED`, `RUNNING`, `COMPLETED`, `FAILED`, `CANCELLED`, or `TIMEDOUT`. Exports may take some time depending on the volume of data. Once the status is `COMPLETED`, the Parquet files are available in your bucket.

Refer to [Monitor and troubleshoot bulk exports](Monitor%20and%20troubleshoot%20bulk%20exports.md) for how to list runs, stop an export, and diagnose failures.

# Monitor and troubleshoot bulk exports

> Monitor bulk export status, manage running exports, and troubleshoot failures.

Once you have [created an export job](Bulk%20export%20trace%20data.md#2-create-an-export-job), you can use the APIs on this page to track its progress, inspect individual runs, and stop it if needed. This page also covers how LangSmith handles failures automatically, and what to do when an export fails after exhausting retries.

This page covers:

* [Monitoring export status](#monitor-export-status) and [listing runs](#list-runs-for-an-export) for a specific export.
* [Listing all exports](#list-all-exports) in your workspace.
* [Stopping an export](#stop-an-export).
* [Failure modes and retry policy](#failure-modes-and-retry-policy), including automatic retry behavior, failure scenarios, status lifecycle, concurrency limits, and progress tracking.
* [Troubleshooting failed exports](#troubleshooting-failed-exports).

> [!NOTE]
>
> **For self-hosted, GCP EU, GCP APAC, and AWS US SaaS**
>
> Update the LangSmith URL in the requests below for self-hosted installs, GCP EU (`eu.api.smith.langchain.com`), GCP APAC (`apac.api.smith.langchain.com`), or AWS US (`aws.api.smith.langchain.com`).

## Monitor export status

To monitor the status of an export job, use the following cURL command:

```bash
curl --request GET \
  --url 'https://api.smith.langchain.com/api/v1/bulk-exports/{export_id}' \
  --header 'Content-Type: application/json' \
  --header 'X-API-Key: YOUR_API_KEY' \
  --header 'X-Tenant-Id: YOUR_WORKSPACE_ID'
```

Replace `{export_id}` with the ID of the export you want to monitor. This command retrieves the current status of the specified export job.

## List runs for an export

An export is typically broken up into multiple runs which correspond to a specific date partition to export.
To list all runs associated with a specific export, use the following cURL command:

```bash
curl --request GET \
  --url 'https://api.smith.langchain.com/api/v1/bulk-exports/{export_id}/runs' \
  --header 'Content-Type: application/json' \
  --header 'X-API-Key: YOUR_API_KEY' \
  --header 'X-Tenant-Id: YOUR_WORKSPACE_ID'
```

This command fetches all runs related to the specified export, providing details such as run ID, status, creation time, rows exported, etc.

## List all exports

To retrieve a list of all export jobs, use the following cURL command:

```bash
curl --request GET \
  --url 'https://api.smith.langchain.com/api/v1/bulk-exports' \
  --header 'Content-Type: application/json' \
  --header 'X-API-Key: YOUR_API_KEY' \
  --header 'X-Tenant-Id: YOUR_WORKSPACE_ID'
```

This command returns a list of all export jobs along with their current statuses and creation timestamps.

## Stop an export

To stop an existing export, use the following cURL command:

```bash
curl --request PATCH \
  --url 'https://api.smith.langchain.com/api/v1/bulk-exports/{export_id}' \
  --header 'Content-Type: application/json' \
  --header 'X-API-Key: YOUR_API_KEY' \
  --header 'X-Tenant-Id: YOUR_WORKSPACE_ID' \
  --data '{
    "status": "Cancelled"
}'
```

Replace `{export_id}` with the ID of the export you wish to cancel. Note that a job cannot be restarted once it has been cancelled,
you will need to create a new export job instead.

## Failure modes and retry policy

LangSmith bulk exports handle transient failures and infrastructure issues automatically to ensure resilience.

Each bulk export is divided into multiple *runs*, where each run processes data for a [specific date partition](Bulk%20export%20trace%20data.md#partitioning-scheme) (typically organized by day). Runs are processed independently, which enables:

* Parallel processing of different time periods.
* Independent retry logic for each run.
* Resumption from specific checkpoints if interrupted.

Each run (date range) in your export has its own [failure handling](#failure-scenarios) and [retry budget](#automatic-retry-behavior). If a run fails after exhausting all retries, the entire export is marked as `FAILED`.

### Automatic retry behavior

Export jobs automatically retry transient failures with the following behavior:

* **Maximum retry attempts**: 20 retries per run (subject to change).
* **Retry delay**: 30 seconds between attempts (fixed, no exponential backoff).
* **Run timeout**: 4 hours maximum per run.
* **Overall workflow timeout**: 72 hours for the entire export.

### Failure scenarios

| Failure type | Cause | Automatic retry? | Action required |
| - | - | - | - |
| **Infrastructure interruption** | [Deployments](../../../Deploy/Get%20started/LangSmith%20Agent%20Server.md), server restarts, worker crashes | Yes, automatically requeued with remaining retries. | None, jobs resume automatically. |
| **Run timeout** | Single run exceeds 4-hour limit | Yes, retried up to 20 times (subject to change). | If persistent, narrow date range, add filters, or [limit the exported fields](Bulk%20export%20trace%20data.md#limit-exported-fields). |
| **Workflow timeout** | Entire export exceeds 72 hours | No | Reduce export scope (date range, filters) or break into smaller exports. |
| **Storage/destination errors** | [Invalid credentials](Manage%20bulk%20export%20destinations.md#credentials-configuration), [missing bucket](Manage%20bulk%20export%20destinations.md#configuration-fields), [permission issues](Manage%20bulk%20export%20destinations.md#permissions-required) | No | Fix destination configuration and create new export. |
| **Destination deleted** | Bucket removed during export | No | Recreate destination and restart export. |
| **Terminal processing errors** | Data serialization issues, resource exhaustion | Yes, retried up to 20 times (subject to change). | Check run error details; may require investigation. |

> [!NOTE]
>
> Any single run failure (after all retries are exhausted) causes the entire export to fail.

### Export status lifecycle

Exports can have the following statuses:

| Status | Description |
| - | - |
| `CREATED` | Export has been created but not yet started processing. |
| `RUNNING` | Export is actively processing runs. |
| `COMPLETED` | All runs successfully exported. |
| `FAILED` | One or more runs failed after exhausting retries. |
| `CANCELLED` | Export was manually cancelled by user. |
| `TIMEDOUT` | Export exceeded the 48-hour workflow timeout. |

Individual runs can have the same possible statuses: `CREATED`, `RUNNING`, `COMPLETED`, `FAILED`, `CANCELLED`, or `TIMEDOUT`.

### Concurrency and rate limits

To ensure system stability, exports are subject to the following limits:

* **Maximum concurrent runs per export**: 45
* **Maximum concurrent exports per workspace**: 15

If you have multiple exports running, new run jobs will queue until capacity becomes available.

#### Self-hosted: tuning bulk export concurrency and payload size

On [LangSmith Self-hosted](../../../LangSmith%20setup/Self-hosted/Self-hosted%20LangSmith.md), the concurrency limits are the defaults. To tune pod memory usage during bulk exports, configure the following environment variables on the `langsmith-backend` service:

| Environment variable | Default | Description |
| - | - | - |
| `BULK_EXPORT_MAX_CONCURRENT_RUNS` | `5` | Maximum number of partition runs enqueued in parallel within a single export, per scheduling pass. Reduce to limit peak memory when processing large date partitions. |
| `DATA_EXPORT_RUN_LIMIT` | `500` | Page size (max rows) fetched from the runs store per query when paging through an export window. |
| `DATA_EXPORT_MAX_BATCH_PAYLOAD_SIZE_KB` | `100000` (100 MB) | Maximum accumulated payload size (KB) before a batch is flushed during an export run. Reduce to lower the memory footprint of each batch. |

**Example: conservative settings for memory-constrained deployments**

```yaml
# In your Helm values
BULK_EXPORT_MAX_CONCURRENT_RUNS: "10"
DATA_EXPORT_RUN_LIMIT: "5"
DATA_EXPORT_MAX_BATCH_PAYLOAD_SIZE_KB: "512"
```

Lowering these values reduces parallelism and may increase total export time, but lowers peak memory usage per pod. If you encounter out-of-memory (OOM) errors on memory-constrained nodes, these settings can help.

### Progress tracking and resumability

The export system maintains detailed progress metadata for each run:

* Latest cursor position in the data stream.
* Number of rows exported.
* List of Parquet files written.

This progress tracking enables:

* **Graceful resumption**: If a run is interrupted (e.g., by a deployment), it resumes from the last checkpoint rather than starting over.
* **Progress monitoring**: Track how much data has been exported through the API.
* **Efficient retries**: Failed runs don't re-export data that was already successfully written.

### Troubleshooting failed exports

If your export fails, follow these steps:

1. **Check the export status**: Use the [`GET /api/v1/bulk-exports/{export_id}` endpoint](../../Reference/LangSmith%20REST%20API/Monitoring/Get%20bulk%20export.md) to retrieve the export details and status.
2. **Review run errors**: You can monitor your runs using the [List Runs API](#list-runs-for-an-export). Each run includes an `errors` field with detailed error messages keyed by retry attempt (e.g., `retry_0`, `retry_1`).
3. **Verify destination access**: Ensure your [destination bucket](Manage%20bulk%20export%20destinations.md#configuration-fields) still exists and [credentials](Manage%20bulk%20export%20destinations.md#credentials-configuration) are valid.
4. **Check run size**: If you see timeout errors, your date partitions may contain too much data. It may be helpful to [limit the exported fields](Bulk%20export%20trace%20data.md#limit-exported-fields).
5. **Review system limits**: Ensure you're not hitting [concurrency limits](#concurrency-and-rate-limits) (5 runs per export, 3 exports per workspace).

For storage-related errors, you can test your destination configuration using the AWS CLI or gsutil before retrying the export.

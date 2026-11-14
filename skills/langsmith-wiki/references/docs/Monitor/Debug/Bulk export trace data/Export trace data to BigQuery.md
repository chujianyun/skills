# Export trace data to BigQuery

> Load LangSmith trace data into BigQuery using bulk export to GCS.

> [!NOTE]
>
> **Plan restrictions apply**
>
> For customers who signed up after August 3, 2026, bulk export is only available on the [LangSmith Enterprise plan](https://www.langchain.com/pricing). Customers who signed up on or before August 3, 2026, can use bulk export on Plus or Enterprise plans until February 1, 2027.

LangSmith can export trace data to a Google Cloud Storage (GCS) bucket in Parquet format. From there, you can load it into BigQuery as an external table (queried in place from GCS) or as a native table (copied into BigQuery storage).

This guide covers:

* Setting up a GCS bucket and HMAC credentials for LangSmith.
* Creating a bulk export destination and export job.
* Loading the exported data into BigQuery.

For full details on bulk export configuration options, refer to [Bulk export trace data](Bulk%20export%20trace%20data.md) and [Manage bulk export destinations](Manage%20bulk%20export%20destinations.md).

## Prerequisites

* Data in your LangSmith [Tracing project](https://smith.langchain.com/projects).
* [`gcloud` CLI installed](https://docs.cloud.google.com/sdk/docs/install-sdk). (You can also use the Google Cloud console for setup.)

## 1. Create a GCS bucket

Create a dedicated GCS bucket for LangSmith exports. Using a dedicated bucket makes it easier to grant scoped permissions without affecting other data:

```bash
gcloud storage buckets create gs://YOUR_BUCKET_NAME \
  --location=US \
  --uniform-bucket-level-access
```

Choose a region close to your BigQuery dataset to minimize latency and avoid cross-region egress charges.

## 2. Create a service account and grant access

Create a GCP service account that LangSmith will use to write data to GCS:

```bash
gcloud iam service-accounts create langsmith-bulk-export \
  --display-name="LangSmith Bulk Export"
```

Grant the service account write access to your bucket. The minimum required permission is `storage.objects.create`. Granting `storage.objects.delete` is optional, but recommended. LangSmith uses it to clean up a temporary test file created during destination validation. If this permission is absent, a `tmp/` folder may remain in your bucket.

The "Storage Object Admin" predefined role covers all required and recommended permissions:

```bash
gcloud storage buckets add-iam-policy-binding gs://YOUR_BUCKET_NAME \
  --member="serviceAccount:langsmith-bulk-export@YOUR_PROJECT.iam.gserviceaccount.com" \
  --role="roles/storage.objectAdmin"
```

To use a minimal custom role instead, grant only:

* `storage.objects.create` (required)
* `storage.objects.delete` (optional, for test file cleanup)
* `storage.objects.get` (optional but recommended, for file size verification)
* `storage.multipartUploads.create` (optional but recommended, for large file uploads)

## 3. Generate HMAC keys

LangSmith connects to GCS using the S3-compatible XML API, which requires HMAC keys rather than a service account JSON key.

Generate HMAC keys for your service account:

```bash
gcloud storage hmac create \
  langsmith-bulk-export@YOUR_PROJECT.iam.gserviceaccount.com
```

Save the `accessId` and `secret` from the output. You can also generate HMAC keys in the GCP Console under **Cloud Storage > Settings > Interoperability > Create a key for a service account**.

## 4. Create a bulk export destination

Create a destination in LangSmith pointing to your GCS bucket. Set `endpoint_url` to `https://storage.googleapis.com` to use the GCS S3-compatible API.

You will need your [LangSmith API key](../../../LangSmith%20setup/Account/Create%20an%20account%20and%20API%20key.md) and [workspace ID](../../../LangSmith%20setup/Govern/Organization/Workspace%20setup/Set%20up%20hierarchy.md#set-up-a-workspace).

```bash
curl --request POST \
  --url 'https://api.smith.langchain.com/api/v1/bulk-exports/destinations' \
  --header 'Content-Type: application/json' \
  --header 'X-API-Key: YOUR_API_KEY' \
  --header 'X-Tenant-Id: YOUR_WORKSPACE_ID' \
  --data '{
    "destination_type": "s3",
    "display_name": "GCS for BigQuery",
    "config": {
      "bucket_name": "YOUR_BUCKET_NAME",
      "prefix": "YOUR_PREFIX",
      "endpoint_url": "https://storage.googleapis.com"
    },
    "credentials": {
      "access_key_id": "YOUR_HMAC_ACCESS_ID",
      "secret_access_key": "YOUR_HMAC_SECRET"
    }
  }'
```

`prefix` is a path within the bucket where LangSmith will write exported files. For example, `langsmith-exports` or `data/traces`. Choose any value that works for your bucket layout.

LangSmith validates the credentials by performing a test write before saving the destination. If the request returns a `400` error, refer to [Debug destination errors](Manage%20bulk%20export%20destinations.md#debug-destination-errors).

Save the `id` from the response; you will need it in the next step.

### Temporary validation file

During destination creation (and [credential rotation](#credential-rotation)), LangSmith writes a temporary `.txt` file to `YOUR_PREFIX/tmp/` to verify write access, then attempts to delete it. The deletion is best-effort: if the service account lacks `storage.objects.delete`, the file is not deleted and the `tmp/` folder remains in your bucket.

The `tmp/` folder does not affect exports, but it will be included in broad GCS URI globs (e.g., `gs://YOUR_BUCKET_NAME/YOUR_PREFIX/*`).

## 5. Create a bulk export job

Create an export targeting a specific project. Use `format_version: v2_beta` for BigQuery compatibility—it produces UTC timezone-aware timestamps that BigQuery handles correctly.

You will need the project ID (`session_id`), which you can copy from the project view in the [**Tracing Projects** list](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-big-query-bulk-export).

**One-time export:**

```bash
curl --request POST \
  --url 'https://api.smith.langchain.com/api/v1/bulk-exports' \
  --header 'Content-Type: application/json' \
  --header 'X-API-Key: YOUR_API_KEY' \
  --header 'X-Tenant-Id: YOUR_WORKSPACE_ID' \
  --data '{
    "bulk_export_destination_id": "YOUR_DESTINATION_ID",
    "session_id": "YOUR_PROJECT_ID",
    "start_time": "2024-01-01T00:00:00Z",
    "end_time": "2024-02-01T00:00:00Z",
    "format_version": "v2_beta",
    "compression": "snappy"
  }'
```

**Scheduled (recurring) export:**

```bash
curl --request POST \
  --url 'https://api.smith.langchain.com/api/v1/bulk-exports' \
  --header 'Content-Type: application/json' \
  --header 'X-API-Key: YOUR_API_KEY' \
  --header 'X-Tenant-Id: YOUR_WORKSPACE_ID' \
  --data '{
    "bulk_export_destination_id": "YOUR_DESTINATION_ID",
    "session_id": "YOUR_PROJECT_ID",
    "start_time": "2024-01-01T00:00:00Z",
    "interval_hours": 24,
    "format_version": "v2_beta",
    "compression": "snappy"
  }'
```

Bulk exports default to `zstandard` compression. This example sets `snappy` because Snappy is fast and widely supported by BigQuery. For all available options, refer to [Bulk export trace data](Bulk%20export%20trace%20data.md#2-create-an-export-job), including field filtering and filter expressions.

> [!NOTE]
>
> On [Self-hosted LangSmith](../../../LangSmith%20setup/Self-hosted/Self-hosted%20LangSmith.md), the default is `gzip`. Set the `FF_BULK_EXPORT_DEFAULT_COMPRESSION` environment variable to change the default.

### Output file structure

Exported files land in GCS using a Hive-partitioned path structure:

```
gs://YOUR_BUCKET_NAME/YOUR_PREFIX/export_id=<uuid>/tenant_id=<uuid>/session_id=<uuid>/resource=runs/year=<year>/month=<month>/day=<day>/<filename>.parquet
```

The partition columns in the path (`export_id`, `tenant_id`, `session_id`, `resource`, `year`, `month`, `day`) are available as queryable columns in BigQuery when Hive partition detection is enabled.

## 6. Load data into BigQuery

BigQuery offers two ways to access your exported data. Both require granting the BigQuery service account read access to your GCS bucket first. Choose based on your needs:

* **External table:** data stays in GCS and BigQuery queries it in place. No storage costs in BigQuery, but query performance is slower than native storage. Refer to [Required roles](https://docs.cloud.google.com/bigquery/docs/query-cloud-storage-data#required-roles).
* **Native table:** data is copied into BigQuery storage. Faster queries and full support for BigQuery features, but incurs BigQuery storage costs. Refer to [Required permissions](https://docs.cloud.google.com/bigquery/docs/cloud-storage-transfer#required_permissions).

### Create the table

> [tab] External table
>
> An external table queries data directly from GCS without copying it into BigQuery.
>
> 1. In the BigQuery console, expand your project and dataset in the **Explorer** pane.
> 2. Click the dataset's **Actions** menu (three dots) and select **Create table**.
> 3. Under **Source**:
>    * Set **Create table from** to **Google Cloud Storage**.
>    * Set the file path to `gs://YOUR_BUCKET_NAME/YOUR_PREFIX/export_id=*`. Using `export_id=*` scopes BigQuery to Hive-partitioned export directories and excludes the `tmp/` folder that LangSmith writes during destination validation (see [Temporary validation file](#temporary-validation-file)).
>    * Set **File format** to **Parquet**.
> 4. Check **Source data partitioning**, then:
>    * Set **Source URI prefix** to `gs://YOUR_BUCKET_NAME/YOUR_PREFIX`.
>    * Set **Partition inference mode** to **Automatically infer types**.
> 5. Under **Destination**:
>    * Select your project and dataset.
>    * Enter a table name, for example `langsmith_runs`.
>    * Set **Table type** to **External table**.
> 6. Under **Schema**, enable **Auto-detect**.
> 7. Click **Create table**.
>
> The partition path columns (`export_id`, `tenant_id`, `session_id`, `resource`, `year`, `month`, `day`) are available as queryable columns. Filter on `year`, `month`, or `day` in your queries to enable partition pruning.

> [tab] Native table
>
> A native table transfers the Parquet data into BigQuery storage for full query performance.
>
> 1. Go to the [Data Transfer page](https://console.cloud.google.com/bigquery/transfers) in the Google Cloud console and select **+ Create transfer**.
>
> 2. For **Source type**, select **Google Cloud Storage**.
>
> 3. Enter a **Transfer name**. You'll have access to edit the transfer at a point if necessary.
>
> 4. Select a **Schedule option**. If you do not want to repeat the export, you can select **On demand** and trigger the export manually.
>
> 5. In the BigQuery console, expand your project and dataset in the **Explorer** pane.
>
> 6. Click the dataset's **Actions** menu (three dots) and select **Create table**.
>
> 7. Under **Source**:
>    * Set **Create table from** to **Google Cloud Storage**.
>    * Set the file path to `gs://YOUR_BUCKET_NAME/YOUR_PREFIX/export_id=*`. Using `export_id=*` excludes the `tmp/` folder that LangSmith writes during destination validation (see [Temporary validation file](#temporary-validation-file)).
>    * Set **File format** to **Parquet**.
>
> 8. Check **Source data partitioning**, then:
>    * Set **Source URI prefix** to `gs://YOUR_BUCKET_NAME/YOUR_PREFIX`.
>    * Set **Partition inference mode** to **Automatically infer types**.
>
> 9. Under **Destination**:
>    * Select your project and dataset.
>    * Enter a table name, for example `langsmith_runs`.
>    * Set **Table type** to **Native table**.
>
> 10. Under **Advanced options**, set **Write preference** to **Write if empty** for a new table.
>
> 11. Click **Create table**.
>
> BigQuery runs a load job to copy the data. The Hive partition columns appear as regular columns in the table. For the full list of available data columns, see [Exportable fields](Bulk%20export%20trace%20data.md#exportable-fields).

## Credential rotation

To rotate your HMAC keys without interrupting active exports:

1. **Generate new HMAC keys** in GCP for the same service account.

2. **Call the PATCH endpoint** with the new credentials:

   ```bash
   curl --request PATCH \
     --url 'https://api.smith.langchain.com/api/v1/bulk-exports/destinations/YOUR_DESTINATION_ID' \
     --header 'Content-Type: application/json' \
     --header 'X-API-Key: YOUR_API_KEY' \
     --header 'X-Tenant-Id: YOUR_WORKSPACE_ID' \
     --data '{
       "credentials": {
         "access_key_id": "NEW_HMAC_ACCESS_ID",
         "secret_access_key": "NEW_HMAC_SECRET"
       }
     }'
   ```

   LangSmith validates the new credentials with a test write before saving. A new `tmp/` file may appear in your bucket during this validation (see [Temporary validation file](#temporary-validation-file)).

3. **Keep old HMAC keys active** until all in-flight export runs complete. Both credential sets are valid simultaneously during the transition window.

4. **Delete the old HMAC keys** in GCP once you have confirmed no in-flight runs are using them.

For full details, see [Rotate destination credentials](Manage%20bulk%20export%20destinations.md#rotate-destination-credentials).

## Troubleshooting

| Symptom | Likely cause | Fix |
| - | - | - |
| `400 Access denied` on destination creation | HMAC credentials lack write permission | Verify the service account has `storage.objects.create` on the bucket |
| `400 Key ID you provided does not exist` | HMAC access ID is invalid | Regenerate HMAC keys in GCP |
| `400 Invalid endpoint` | Endpoint URL is malformed | Use exactly `https://storage.googleapis.com` |
| BigQuery table shows no rows | Export not yet complete | Check export status with `GET /api/v1/bulk-exports/{export_id}` |
| BigQuery partition pruning not working | Incorrect source URI prefix | Ensure the source URI prefix ends before the first partition key, e.g. `gs://BUCKET/PREFIX` |
| BigQuery picks up `tmp/` files | Broad file path glob | Use `export_id=*` in your file path instead of `*` |

For additional error codes and export status details, see [Monitor and troubleshoot bulk exports](Monitor%20and%20troubleshoot%20bulk%20exports.md).

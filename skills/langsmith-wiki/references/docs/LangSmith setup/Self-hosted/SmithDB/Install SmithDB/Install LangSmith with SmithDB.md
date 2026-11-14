# Install LangSmith with SmithDB

> Enable SmithDB on a self-hosted LangSmith Kubernetes installation through staged Helm updates.

This guide enables SmithDB on a LangSmith Kubernetes installation in stages so you can validate each change. Each stage is one Helm update that rolls the affected pods. ClickHouse stays in place throughout.

Migrating historical ClickHouse data is optional. History left in ClickHouse is not reachable through SmithDB-backed queries unless you migrate it.

## Before you begin

* Contact LangChain through the [Support Portal](https://support.langchain.com/) before you begin so the team can review your infrastructure plan.
* Set up [SmithDB observability](../Monitoring%20and%20alerting/Configure%20SmithDB%20observability.md) before you begin. The steps below use metrics to verify each stage.
* Start from a running LangSmith installation on Kubernetes. For a new installation on LangSmith 0.17, see [Install without ClickHouse](#install-without-clickhouse).
* Upgrade one major version at a time until the installation meets the [cloud support](../Overview/Enable%20SmithDB%20on%20self-hosted%20LangSmith.md#cloud-support) minimum: LangSmith 0.16 with Helm chart `0.16.14` or later on AWS (EKS) and GCP (GKE), or LangSmith 0.17 on Azure (AKS). Follow the [upgrade guide](../../Manage%20an%20instance/Upgrade%20an%20installation.md).
* Keep the Helm values from your current installation. This guide adds SmithDB configuration to them.
* Confirm you can apply the LangSmith Helm release to the cluster, directly or through your GitOps workflow.
* Review the [SDK migration guide](../../../../Monitor/Reference/SmithDB%20API%20migration/Migrate%20to%20SmithDB-backed%20APIs.md) and plan your SDK upgrade alongside this installation.

You can disable SmithDB later. To return query and ingestion traffic to ClickHouse and disable SmithDB services, see [Troubleshoot SmithDB](Troubleshoot%20SmithDB.md#disable-or-reset-smithdb).

## Installation sequence

### Step 1. Prepare supporting infrastructure

Follow [Prepare SmithDB supporting infrastructure](Prepare%20SmithDB%20supporting%20infrastructure.md) to provide:

* A dedicated PostgreSQL 18 or later metastore
* Dedicated object storage with workload identity or equivalent credentials
* Cache storage for SmithDB: network-attached disks, or local SSD for the best cache performance
* Network connectivity and a Kubernetes Secret containing the metastore connection details

Record the object-store configuration, metastore Secret and key mappings, service-account identity, and cache settings needed by the Helm chart.

At the end of this step, the shared infrastructure portion of your SmithDB Helm values might look like the following. Keep SmithDB disabled until Step 3.

Add the cache values for your version from [Cache storage](Prepare%20SmithDB%20supporting%20infrastructure.md#cache-storage). On LangSmith 0.17 that is usually one line, `smithdb.cache.storageClassName`. Local SSD on either version also needs the node selectors and tolerations shown there.

> [accordion] SmithDB infrastructure Helm values
>
> ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> smithdb:
>   serviceAccount:
>     annotations:
>       IDENTITY_ANNOTATION_KEY: IDENTITY_ANNOTATION_VALUE
>
>   config:
>     existingSecretName: smithdb-metastore
>     metastore:
>       hostSecretKey: smithdb_metastore_db_host
>       databaseSecretKey: smithdb_metastore_db_name
>       usernameSecretKey: smithdb_metastore_db_username
>       passwordSecretKey: smithdb_metastore_db_password
>       port: "5432"
>       useSsl: true
>     objectStore:
>       type: OBJECT_STORE_TYPE
>       bucket: BUCKET_NAME
> ```
>
> Replace the identity and object-store placeholders with the values for your provider. For Azure, also add the `azure.workload.identity/use: "true"` label to every SmithDB workload. See [Configure Blob Storage access](Prepare%20SmithDB%20supporting%20infrastructure.md#configure-blob-storage-access).
>
> ```yaml AWS theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> smithdb:
>   serviceAccount:
>     annotations:
>       eks.amazonaws.com/role-arn: arn:aws:iam::ACCOUNT_ID:role/ROLE_NAME
>
>   config:
>     objectStore:
>       type: s3
>       bucket: BUCKET_NAME
>       s3:
>         region: AWS_REGION
> ```
>
> ```yaml GCP theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> smithdb:
>   serviceAccount:
>     annotations:
>       iam.gke.io/gcp-service-account: GSA_NAME@PROJECT_ID.iam.gserviceaccount.com
>
>   config:
>     objectStore:
>       type: gcs
>       bucket: BUCKET_NAME
> ```
>
> ```yaml Azure theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> smithdb:
>   serviceAccount:
>     annotations:
>       azure.workload.identity/client-id: CLIENT_ID
>
>   config:
>     objectStore:
>       type: azure
>       bucket: CONTAINER_NAME
>       azure:
>         accountName: STORAGE_ACCOUNT_NAME
>         accessKeySecretKey: ""
> ```

### Step 2. Upgrade to the required LangSmith version

SmithDB requires the LangSmith version listed in [Cloud support](../Overview/Enable%20SmithDB%20on%20self-hosted%20LangSmith.md#cloud-support). Upgrade to it before enabling SmithDB. Preserve the existing ClickHouse configuration and keep SmithDB disabled:

```yaml
smithdb:
  enabled: false
```

Apply the upgrade and verify that the existing LangSmith pods are running and migration Jobs complete. Resolve upgrade failures before continuing.

### Step 3. Configure and deploy SmithDB services

Before enabling SmithDB, choose a [deployment mode](Configure%20SmithDB%20for%20scale.md#choose-a-deployment-mode) and a tested baseline from [Configure SmithDB for scale](Configure%20SmithDB%20for%20scale.md). Configure its replica counts and per-replica CPU, memory, and cache size, and confirm the cluster can provision the total.

Merge the infrastructure values prepared in Step 1 and your selected sizing baseline into the existing LangSmith values. Leave the existing ClickHouse configuration unchanged, then enable the SmithDB services without changing LangSmith ingestion or queries:

```yaml
smithdb:
  enabled: true
  langsmith:
    ingestion:
      enabled: false
    migration:
      enabled: false
    query:
      enabled: false
```

Apply the chart, then confirm every SmithDB pod is running and the metastore migration Job has completed:

```bash
kubectl get pods -n NAMESPACE | grep smithdb
kubectl get job -n NAMESPACE HELM_RELEASE-smithdb-metastore-migration
```

SmithDB components verify metastore and object-store connectivity at startup, so a running pod has already confirmed both. A pod stuck in `Pending` or `CrashLoopBackOff` has not. See [Troubleshoot SmithDB](Troubleshoot%20SmithDB.md#supporting-infrastructure).

Do not enable LangSmith integration flags until these checks pass.

### Step 4. Enable dual ingestion

Begin writing to SmithDB while continuing to write to ClickHouse:

```yaml
smithdb:
  langsmith:
    ingestion:
      enabled: true
    migration:
      enabled: false
    query:
      enabled: false
```

Verify the dual-ingestion path, in this order:

1. **Routing**: `sdb_ingestion_enabled` is `true` and `sdb_query_enabled` is `false`.
2. **Flow**: `ingest_flush_count` increases while traffic arrives. A flat counter means writes are not reaching object storage.
3. **Capacity**: `langsmith_asynq_ingestion_queue_pending` stays low and stable through a period that includes your peak traffic. Sustained growth means ingestion is undersized. Resolve it with [Configure SmithDB for scale](Configure%20SmithDB%20for%20scale.md) before Step 5 or Step 6.

Check routing with:

```bash
curl -s https://LANGSMITH_HOST/api/v1/info | jq '.instance_flags | {sdb_ingestion_enabled, sdb_query_enabled}'
```

Writes must continue to reach ClickHouse throughout. See [Essential SmithDB metrics](../Monitoring%20and%20alerting/Essential%20SmithDB%20metrics.md) for the remaining ingestion metrics.

### Step 5. Choose how to handle historical data

Once dual ingestion is stable, decide whether ClickHouse history needs to be reachable through SmithDB-backed queries:

* **Migrate it**: Follow [Migrate ClickHouse history to SmithDB](Migrate%20ClickHouse%20history%20to%20SmithDB.md), then return here for query cutover.
* **Leave it in ClickHouse**: Skip migration. Existing data stays in ClickHouse but is not queryable through LangSmith after cutover unless queries are directed back to ClickHouse.

### Step 6. Switch queries to SmithDB

After dual ingestion is healthy and any ClickHouse migration has completed, enable SmithDB-backed queries:

```yaml
smithdb:
  langsmith:
    ingestion:
      enabled: true
    migration:
      enabled: false
    query:
      enabled: true
```

Confirm both flags now report `true`:

```bash
curl -s https://LANGSMITH_HOST/api/v1/info | jq '.instance_flags | {sdb_ingestion_enabled, sdb_query_enabled}'
```

Then validate traces, projects, filters, and time ranges in the LangSmith UI and API, and continue monitoring ingestion and query errors.

> [!WARNING]
>
> Do not disable or remove ClickHouse on LangSmith 0.16. On 0.17, retiring ClickHouse from an existing installation is a separate procedure; contact LangChain through the [Support Portal](https://support.langchain.com/) before considering it.

## Install without ClickHouse

On LangSmith 0.17, a new installation can run SmithDB as its only trace store. Complete Step 1, then install LangSmith 0.17 with ClickHouse disabled and both SmithDB paths enabled, in place of Steps 2 through 6:

```yaml
clickhouse:
  enabled: false
smithdb:
  enabled: true
  langsmith:
    ingestion:
      enabled: true
    migration:
      enabled: false
    query:
      enabled: true
```

The chart requires at least one ingestion backend and one query backend, so both SmithDB flags must be on. This applies to new installations only.

## Troubleshooting

If something fails during or after installation, see [Troubleshoot SmithDB](Troubleshoot%20SmithDB.md) or contact LangChain through the [Support Portal](https://support.langchain.com/).

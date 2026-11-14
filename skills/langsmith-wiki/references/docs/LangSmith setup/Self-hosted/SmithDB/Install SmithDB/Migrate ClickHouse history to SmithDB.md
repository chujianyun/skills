# Migrate ClickHouse history to SmithDB

> Run the historical ClickHouse-to-SmithDB migration for a self-hosted LangSmith installation.

Run this migration when ClickHouse history must be queryable through SmithDB. If it does not need to be, skip this page and continue with query cutover.

> [!NOTE]
>
> Complete stages 1 through 4 of [Install LangSmith with SmithDB](Install%20LangSmith%20with%20SmithDB.md) before starting this guide. Return there for **Switch queries to SmithDB** after migration cleanup.

## How migration works

The migration Job reads runs from ClickHouse, writes them to SmithDB object storage, validates the result, and promotes each batch to the SmithDB metastore. TaskDB, a separate PostgreSQL database used only during migration, lets migration pods share work, recover from interruptions, and resume without starting over. It is distinct from both LangSmith PostgreSQL and the SmithDB metastore.

## Scope and prerequisites

Before starting:

* Keep the existing ClickHouse configuration enabled and unchanged.
* Confirm SmithDB services and dual ingestion are healthy, and that new writes continue to reach ClickHouse.

## Plan migration capacity

### Size migration workers

Scale migration with these Helm controls:

* **`smithdb.migration.job.parallelism`**: The number of migration Job pods that may run concurrently.
* **`smithdb.migration.job.resources`**: The CPU, memory, and ephemeral storage allocated to each migration pod. On LangSmith 0.16 this key is `smithdb.migration.deployment.resources`.

Use this formula as a rule of thumb:

```text
estimated allocated vCPUs = historical run count / 5,000,000 / target duration in days
```

Start from the chart default of 8 vCPU and 32 GiB per migration pod, and treat 32 GiB as a practical minimum rather than a function of CPU. Migrating 100 million runs in one day therefore suggests about 20 allocated vCPUs across the Job pods, for example three pods at the default size. This estimates total CPU, not pod count or per-pod resources. Actual requirements vary by data and environment.

You can run a single worker, and TaskDB persists its progress, but substantial histories may take impractically long that way. Choose parallelism and per-pod resources together based on estimated vCPUs and available capacity, and set both in the values block under [Enable migration](#enable-migration).

### Scale TaskDB

Monitor TaskDB CPU, memory, and active connections as parallelism increases, and raise `smithdb.migration.taskdb.postgres.statefulSet.resources` as needed. Do not use the main LangSmith PostgreSQL database or the SmithDB metastore as TaskDB.

## Enable migration

For chart-managed TaskDB, create a Secret in the LangSmith namespace with a strong generated password under `postgres_password`. Never store it in Helm values or source control. See [Use an existing secret for your installation](../../Platform%20auth%20%26%20access%20control/Use%20an%20existing%20secret%20for%20your%20installation%20%28Kubernetes%29.md). For external PostgreSQL, use the chart's external TaskDB settings instead.

Reference the TaskDB Secret and enable migration. The block below collects every migration setting in one place: the `langsmith` flags and the TaskDB Secret are required, and the rest are chart defaults to change only when scaling.

> [accordion] Sample migration Helm values
>
> ```yaml LangSmith 0.17 theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> smithdb:
>   enabled: true
>   langsmith:
>     ingestion:
>       enabled: true    # required: keep dual ingestion on
>     migration:
>       enabled: true    # required: runs the migration Job and TaskDB
>     query:
>       enabled: false   # required: keep queries on ClickHouse until migration completes
>   migration:
>     job:
>       parallelism: 1   # default: raise to run more migration pods
>       resources:       # default per pod: 32Gi is a practical minimum
>         requests:
>           cpu: "8"
>           memory: "32Gi"
>         limits:
>           cpu: "8"
>           memory: "32Gi"
>     taskdb:
>       postgres:
>         auth:
>           existingSecretName: "smithdb-migration-taskdb"   # required for chart-managed TaskDB
>           passwordSecretKey: "postgres_password"
>         maxConnectionsPerMigrationPod: 10   # default: server limit is (parallelism + 1) × this
>         statefulSet:
>           resources:   # default: raise for high parallelism
>             requests:
>               cpu: "2"
>               memory: "4Gi"
>             limits:
>               cpu: "4"
>               memory: "8Gi"
> ```
>
> ```yaml LangSmith 0.16 theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> smithdb:
>   enabled: true
>   langsmith:
>     ingestion:
>       enabled: true    # required: keep dual ingestion on
>     migration:
>       enabled: true    # required: runs the migration Job and TaskDB
>     query:
>       enabled: false   # required: keep queries on ClickHouse until migration completes
>   migration:
>     job:
>       parallelism: 1   # default: raise to run more migration pods
>     deployment:
>       resources:       # default per pod: 32Gi is a practical minimum
>         requests:
>           cpu: "8"
>           memory: "32Gi"
>           ephemeral-storage: "100Gi"
>         limits:
>           cpu: "8"
>           memory: "32Gi"
>           ephemeral-storage: "100Gi"
>     taskdb:
>       postgres:
>         auth:
>           existingSecretName: "smithdb-migration-taskdb"   # required for chart-managed TaskDB
>           passwordSecretKey: "postgres_password"
>         maxConnectionsPerMigrationPod: 10   # default: server limit is (parallelism + 1) × this
>         statefulSet:
>           resources:   # default: raise for high parallelism
>             requests:
>               cpu: "2"
>               memory: "4Gi"
>             limits:
>               cpu: "4"
>               memory: "8Gi"
> ```

Apply the chart through your normal workflow. It creates TaskDB and a one-shot migration Job that runs to completion and exits.

## Pause and resume migration

Suspending migration stops its pods but keeps the Job, TaskDB, and migration progress.

> [!NOTE]
>
> Available in all 0.17 Helm charts and version 0.16.40 or later on the 0.16 line.

Set `smithdb.migration.job.suspend: true` and apply the chart to pause. Keep `smithdb.langsmith.migration.enabled: true`. To resume from saved progress, set `smithdb.migration.job.suspend: false` and apply again.

> [!WARNING]
>
> Do not pause with `smithdb.langsmith.migration.enabled: false`. This removes the Job, chart-managed TaskDB, and, by default, the TaskDB PVC holding migration progress.

## Wait for completion

Keep SmithDB-backed queries disabled until the historical migration Job reports Kubernetes condition `Complete`.

Finished migration Jobs remain for seven days by default so you can inspect their logs. The logs are diagnostic only; the `Complete` condition is the signal that migration finished. Retain TaskDB only if needed for diagnosis. If the Job fails, preserve it and TaskDB, then see [Migration Job failures](Troubleshoot%20SmithDB.md#migration-job-failures).

Return to [Install LangSmith with SmithDB](Install%20LangSmith%20with%20SmithDB.md#step-6-switch-queries-to-smithdb) and complete the **Switch queries to SmithDB** step.

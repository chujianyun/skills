# Troubleshoot SmithDB

> Diagnose SmithDB failures, gather troubleshooting context, or disable and reset a SmithDB deployment on self-hosted LangSmith.

> [!NOTE]
>
> Keep ClickHouse configured and available throughout everything on this page. If no documented issue matches, contact LangChain through the [Support Portal](https://support.langchain.com/).

Use this page to diagnose SmithDB installation and migration failures, gather context before you escalate, or back SmithDB out of a deployment: return traffic to ClickHouse, disable the SmithDB services, and optionally remove SmithDB data.

## General best practices

* Stop at the current installation or migration stage until you understand the issue.
* Record the LangSmith and Helm chart versions and the most recent configuration change.
* Preserve failed Jobs, TaskDB, and relevant logs before deleting or recreating resources.
* Do not delete the SmithDB metastore or object-storage data while troubleshooting.

## Supporting infrastructure

Most SmithDB installation failures trace back to one of the following. For the configuration each depends on, see [Prepare SmithDB supporting infrastructure](Prepare%20SmithDB%20supporting%20infrastructure.md).

**Pods stay `Pending`.** On a network-attached cache, the claim cannot bind. Check the claim and the pod events for StorageClass, zone, or quota errors:

```bash
kubectl get pvc -n NAMESPACE
kubectl describe pod -n NAMESPACE POD_NAME | grep -A5 Events
```

For local SSD, compare the pod's `ephemeral-storage` request with node allocatable capacity:

```bash
kubectl get node NODE_NAME -o jsonpath='{.status.allocatable.ephemeral-storage}{"\n"}'
```

Either provision larger nodes or select a smaller tier. A node also needs headroom above the pod request for images, logs, and Kubernetes reservations. If you moved to network-attached caches on 0.17 and pods still request node storage, an `ephemeral-storage` override from an older values file is still in place; remove it.

**Object-store access is denied.** The workload identity binding does not match the ServiceAccount SmithDB actually runs as. The trust policy must name the release namespace and the ServiceAccount name, which defaults to `HELM_RELEASE-smithdb`. Confirm what the pod is using:

```bash
kubectl get pod -n NAMESPACE POD_NAME -o jsonpath='{.spec.serviceAccountName}{"\n"}'
```

With `create: false`, `name` is required. Otherwise pods fall back to the `default` ServiceAccount and the binding never applies.

**The metastore refuses connections.** Check that the database is reachable from the cluster, that `useSsl` matches what the server requires, and that the Secret keys named in `smithdb.config.metastore` match the keys actually present in the Secret.

**Ingestion or queries fail with `Unavailable` errors.** An HTTP proxy or service mesh blocks connections to SmithDB pod IPs. The `ingest-queue` logs show errors such as `closing SmithDB ingestion stream failed: rpc error: code = Unavailable`. Allow the connections described in [Pod network access](Prepare%20SmithDB%20supporting%20infrastructure.md#pod-network-access). Then restart `platform-backend`, `ingest-queue`, `queue`, and SmithDB query, because connections opened before the change keep failing.

**Cache I/O is slow.** On local SSD, the `emptyDir` is backed by the boot disk rather than the SSD. On a network-attached disk, the volume is under-provisioned: confirm the StorageClass sets at least 7000 IOPS and 1000 MiB/s. Check which device backs the cache filesystem inside a running pod:

```bash
kubectl exec -n NAMESPACE POD_NAME -- df -h /data
```

For local SSD, the filesystem should use the local NVMe device, such as `/dev/md0` or `/dev/nvme1n1`. For network disks, confirm `/data` mounts the provisioned claim.

## Migration Job failures

The migration Job defaults to `backoffLimit: 3`, allowing retries before Kubernetes marks it failed.

If the Job failed from under-provisioning, adjust both `smithdb.migration.job.parallelism` and `smithdb.migration.job.resources` (`smithdb.migration.deployment.resources` on LangSmith 0.16). Preserve TaskDB, delete only the migration Job, and run the normal Helm upgrade. Deleting an active Job may leave a small amount of untracked object-storage data from in-flight writes. The recreated Job resumes progress tracked in TaskDB.

> [!WARNING]
>
> When resetting the SmithDB metastore or object store, reset TaskDB too. The chart-managed TaskDB PVC is deleted by default when SmithDB is disabled. Clear an external or retained TaskDB manually, or stale migration state can cause work to be skipped.

> [!WARNING]
>
> For validation failures, unclear causes, or issues other than under-provisioning, stop and escalate. Keep queries disabled and migration enabled. Preserve the failed Job, TaskDB, SmithDB metastore, and object storage. Contact LangChain through the [Support Portal](https://support.langchain.com/).

## Disable or reset SmithDB

Use this section to route LangSmith traffic back to ClickHouse and disable the SmithDB services. For the installation and cutover sequence, see [Install LangSmith with SmithDB](Install%20LangSmith%20with%20SmithDB.md).

> [!WARNING]
>
> Disabling migration removes chart-managed TaskDB and, by default, its PVC holding migration progress. To pause without losing progress, keep migration enabled and use `smithdb.migration.job.suspend: true`. See [Pause and resume migration](Migrate%20ClickHouse%20history%20to%20SmithDB.md#pause-and-resume-migration).

If you re-enable SmithDB ingestion later, you need to run another migration to bring it back in sync with ClickHouse.

### Step 1. Route traffic back to ClickHouse

Keep the SmithDB services enabled, but disable query, ingestion, and migration:

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

Apply the chart through your normal deployment workflow and wait for the rollout to complete. This routes all query and ingestion traffic back to ClickHouse before any SmithDB workloads are removed.

### Step 2. Disable SmithDB services

After the first Helm update completes, disable SmithDB services while leaving the integration flags off:

```yaml
smithdb:
  enabled: false
  langsmith:
    ingestion:
      enabled: false
    migration:
      enabled: false
    query:
      enabled: false
```

Apply the chart again. Separating traffic cutover from workload removal avoids requests racing with SmithDB shutdown.

### Step 3. (Optional) Remove SmithDB data

> [!CAUTION]
>
> This cleanup is destructive. Continue only after the SmithDB services are disabled and you no longer need the data for re-enablement, diagnosis, or recovery.

Optionally remove the dedicated SmithDB object-storage data and PostgreSQL metastore. Re-enabling SmithDB after this cleanup requires recreating its supporting infrastructure and re-migrating data from ClickHouse.

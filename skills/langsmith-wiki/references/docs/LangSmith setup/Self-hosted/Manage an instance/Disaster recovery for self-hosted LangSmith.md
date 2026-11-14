# Disaster recovery for self-hosted LangSmith

This page describes how to plan, configure, and operate disaster recovery (DR) for self-hosted LangSmith Observability and Evaluation. It covers what data must be protected, where it lives, how to back it up, and how to recover the platform after a regional or zonal failure.

> [!NOTE]
>
> **Shared responsibility.** For self-hosted deployments you are responsible for backups, replication, restore testing, and recovery procedures for every component, including LangSmith pods and all backing data stores. LangChain is responsible only for the LangSmith software itself. For the equivalent SaaS responsibilities, see the [Shared responsibility model](../../Govern/Data%20%26%20compliance/LangSmith%20shared%20responsibility%20model.md).

> [!TIP]
>
> For details on the architectural primitives (stateless services, queue heartbeats, exactly-once semantics) that this page assumes, refer to [Scalability and resilience](../../Govern/Data%20%26%20compliance/Scalability%20%26%20resilience.md).

## What you are recovering

Self-hosted LangSmith is composed of stateless services backed by four state stores. Recovery planning is almost entirely about the state stores. You can recreate the stateless services at any time by reapplying the Helm chart.

| Layer | Components | State | Recovery action |
| - | - | - | - |
| LangSmith services | `langsmith-frontend`, `langsmith-backend`, `langsmith-platform-backend`, `langsmith-queue`, `langsmith-ingest-queue`, `langsmith-playground`, `langsmith-ace-backend` | Stateless | Reinstall the Helm chart |
| PostgreSQL | Operational data: orgs, workspaces, users, API keys, datasets, prompts, projects, deployments metadata | **Durable** | Restore from backup or replica |
| ClickHouse | Traces and feedback (high volume analytical data) | **Durable** | Restore from backup or replica |
| Blob storage (S3/GCS/Azure Blob) | Run inputs, outputs, errors, manifests, extras, events, attachments (when enabled) | **Durable** | Restore from versioned bucket or replica |
| Redis (or Valkey) | Ephemeral queue state, pub/sub, cache, run heartbeats | Ephemeral | Reprovision; no restore required |
| Kubernetes objects | Helm values, `Secret`s, TLS material, IRSA / Workload Identity bindings | Configuration | Re-apply from source control or back up cluster state |

> [!WARNING]
>
> All durable data stores must be protected together. Postgres, ClickHouse, and blob storage are the three stores that hold durable data; Redis is ephemeral and does not need to be backed up. Restoring Postgres without ClickHouse and blob storage (or vice versa) produces an inconsistent installation. References from Postgres to runs in ClickHouse and to objects in blob storage break across the divergence point. Always take coordinated backups, or use point-in-time recovery (PITR) targets that are close together across stores.

> [!WARNING]
>
> The Redis guidance above applies to the platform's caches and queues, not the JuiceFS metadata store used by Sandboxes. JuiceFS Redis holds durable filesystem metadata and requires persistence and backups alongside object storage. See [Protect sandbox storage](../Install%20an%20instance/Additional%20features/Enable%20Sandboxes/Operate%20self-hosted%20Sandboxes.md#protect-sandbox-storage).

## Plan your RPO and RTO

Before designing your DR architecture, define two targets:

* **Recovery Point Objective (RPO):** the maximum amount of data loss your organization can tolerate, measured in time. With managed Postgres PITR, RPO is typically less than 5 minutes. With nightly snapshots only, RPO can be up to 24 hours.
* **Recovery Time Objective (RTO):** the maximum time you can take to restore service after a failure. A warm cross-region replica can deliver RTO in minutes; a cold restore from snapshot can take hours, especially for large ClickHouse datasets.

The following deployment patterns assume one of three target profiles:

| Profile | Typical RPO | Typical RTO | Approach |
| - | - | - | - |
| Snapshot-only | 6 to 24 hours | Hours | Daily managed backups of each store. Lowest cost, longest restore. |
| Multi-AZ HA | Seconds | Minutes (zone failure) | Synchronous standby in another AZ for Postgres and ClickHouse, Multi-AZ Redis, zone-redundant blob storage. Standard production posture. |
| Cross-region DR | Minutes to hours | Hours | Backups of Postgres, ClickHouse, and blob storage copied to a second region, restored on demand. Optionally a Postgres cross-region replica for a tighter Postgres RPO. Highest cost, slower recovery than Multi-AZ, but protects against a regional outage. |

## Postgres

LangSmith uses PostgreSQL as the primary store for operational and transactional data. **All communication with Postgres uses retries for retry-able errors**, so a brief outage during failover usually does not surface as user-visible errors. A prolonged outage will render the LangSmith API unavailable.

### Use a managed service

We strongly recommend running Postgres on a managed service in production. Managed services provide built-in automated backups, PITR, and HA failover. For setup, refer to [Connect external Postgres](../Connect%20external%20services/Connect%20to%20an%20external%20PostgreSQL%20database.md).

> [tab] AWS
>
> Run [Amazon RDS for PostgreSQL](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_GettingStarted.CreatingConnecting.PostgreSQL.html) or [Aurora PostgreSQL](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Overview.html) in Multi-AZ mode.
>
> * **Backups:** Enable [automated backups](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html) with a retention window that matches your compliance posture (7 to 35 days is typical).
> * **PITR:** Automated backups include PITR within the retention window.
> * **HA:** Multi-AZ deployments maintain a synchronous standby in a second availability zone with automatic failover.
> * **Cross-region DR:** For Aurora, configure an [Aurora Global Database](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-global-database.html). For RDS, use [cross-region read replicas](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ReadRepl.XRgn.html) or copy automated snapshots to a secondary region.
> * **Encryption:** Enable storage encryption with a customer-managed [KMS](https://aws.amazon.com/kms/) key.

> [tab] GCP
>
> Run [Cloud SQL for PostgreSQL](https://cloud.google.com/sql/docs/postgres) with [high availability](https://cloud.google.com/sql/docs/postgres/high-availability) enabled.
>
> * **Backups:** Enable [automated backups](https://cloud.google.com/sql/docs/postgres/backup-recovery/backups) with PITR.
> * **HA:** Regional instances replicate synchronously to a standby in a second zone.
> * **Cross-region DR:** Configure [cross-region read replicas](https://cloud.google.com/sql/docs/postgres/replication/cross-region-replicas) and promote them on regional failure.
> * **Encryption:** Use [Cloud KMS customer-managed encryption keys](https://docs.cloud.google.com/sql/docs/postgres/cmek).

> [tab] Azure
>
> Run [Azure Database for PostgreSQL Flexible Server](https://learn.microsoft.com/en-us/azure/postgresql/flexible-server/overview) with zone-redundant HA.
>
> * **Backups:** Enable [automatic backups](https://learn.microsoft.com/en-us/azure/postgresql/flexible-server/concepts-backup-restore) with geo-redundant backup storage.
> * **HA:** Zone-redundant HA maintains a synchronous standby in a different availability zone.
> * **Cross-region DR:** Use [read replicas](https://learn.microsoft.com/en-us/azure/postgresql/flexible-server/concepts-read-replicas) in a secondary region for promotion on regional failure.

### In-cluster Postgres

If you must run Postgres in-cluster from the bundled chart, you are responsible for backing up the underlying PersistentVolume. Snapshot the PVC on a regular cadence using your CSI driver's snapshot class, and copy snapshots to object storage or a different region. **This path is not recommended for production.**

## ClickHouse

ClickHouse holds the high-volume trace and feedback data and is typically the largest data store in a LangSmith deployment. Backups and replication need to be planned for cost and restore-time impact.

### Managed ClickHouse

The fastest path to a resilient ClickHouse is a managed option. See [Connect external ClickHouse](../Connect%20external%20services/Connect%20to%20an%20external%20ClickHouse%20database.md).

* **[LangSmith Managed ClickHouse](../Connect%20external%20services/LangSmith-managed%20ClickHouse.md):** LangChain operates the ClickHouse cluster, including backups and replication. VPC peering connects it to your LangSmith installation.
* **[ClickHouse Cloud](https://clickhouse.cloud/):** Provides built-in backups, replication, and HA. Available on AWS, GCP, and Azure marketplaces.

### Self-managed replicated cluster

If you self-manage ClickHouse for compliance or air-gap reasons, use a replicated cluster. A single-node ClickHouse instance cannot meet a meaningful RPO.

* Configure a multi-node ClickHouse cluster with replication via [Keeper or ZooKeeper](https://clickhouse.com/docs/architecture/replication).
* Set the `cluster` value in the LangSmith chart so migrations create `Replicated` table engines from the start. **Clustered setups must be configured against a fresh schema**, you cannot convert a standalone instance to clustered later.
* Spread replicas across availability zones.
* Schedule [`BACKUP TABLE` or `BACKUP DATABASE`](https://clickhouse.com/docs/operations/backup) to object storage on a frequency matching your RPO. The community [`clickhouse-backup`](https://github.com/Altinity/clickhouse-backup) tool is also a popular option for scheduled, incremental backups with built-in S3, GCS, and Azure Blob support.
* For cross-region DR, copy the backup bucket to a secondary region. Cross-region ClickHouse replication is not generally supported in self-managed deployments and is not offered by ClickHouse Cloud either, so plan for a backup/restore failover model rather than a hot replica.

For an example replicated configuration, see the [replicated ClickHouse example](https://github.com/langchain-ai/helm/blob/main/charts/langsmith/examples/replicated-clickhouse/README.md) in the Helm repo.

> [!WARNING]
>
> Restoring ClickHouse can take significantly longer than restoring Postgres at the same data volume because trace tables are large. Account for this when setting your RTO. Validate restore time on a representative dataset during DR drills.

## Blob storage

If you have enabled [blob storage](../Connect%20external%20services/Enable%20blob%20storage.md) (recommended for production), your run inputs, outputs, errors, manifests, extras, events, and attachments live in S3, GCS, or Azure Blob Storage. Cloud blob services are durable by design, but you should still configure protection against accidental deletion and regional outages.

> [tab] AWS
>
> * Enable [S3 Versioning](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html) to protect against accidental deletes and overwrites.
> * Enable [MFA Delete](https://docs.aws.amazon.com/AmazonS3/latest/userguide/MultiFactorAuthenticationDelete.html) for high-security buckets.
> * For cross-region DR, configure [Cross-Region Replication (CRR)](https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication.html) to a bucket in your DR region.
> * Use [S3 Object Lock](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html) for write-once-read-many (WORM) retention.
> * Encrypt with [SSE-KMS](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingKMSEncryption.html). LangSmith supports passing a specific KMS key ARN, see [KMS encryption header support](../Connect%20external%20services/Enable%20blob%20storage.md#kms-encryption-header-support).

> [tab] GCP
>
> * Enable [Object Versioning](https://cloud.google.com/storage/docs/object-versioning) on the bucket.
> * Use [dual-region or multi-region buckets](https://cloud.google.com/storage/docs/locations) for geo-redundancy.
> * For cross-region DR, use [Storage Transfer Service](https://cloud.google.com/storage-transfer-service) or [Object Lifecycle Management](https://cloud.google.com/storage/docs/lifecycle) with replication policies.
> * Encrypt with [Customer-Managed Encryption Keys (CMEK)](https://cloud.google.com/storage/docs/encryption/customer-managed-keys).

> [tab] Azure
>
> * Choose a [redundancy tier](https://learn.microsoft.com/en-us/azure/storage/common/storage-redundancy) that matches your DR objectives. Use **RA-GRS** or **RA-GZRS** for cross-region read access during a primary region outage.
> * Enable [soft delete and blob versioning](https://learn.microsoft.com/en-us/azure/storage/blobs/soft-delete-blob-overview).
> * Encrypt with a [customer-managed key in Key Vault](https://learn.microsoft.com/en-us/azure/storage/common/customer-managed-keys-overview).

> [!WARNING]
>
> **Keep TTL lifecycle rules in your DR bucket.** If you copy data to a DR bucket, replicate the lifecycle rules for `ttl_s/`, `ttl_l/`, and any custom `ttl_XXd/` prefixes too. Missing rules in the DR bucket will cause data to be retained indefinitely after failover. See [TTL configuration](../Connect%20external%20services/Enable%20blob%20storage.md#ttl-configuration).

## Redis

Redis stores ephemeral metadata, queue state, and cross-instance pub/sub. **No durable data is stored in Redis, so you do not need to back it up.** Communication with Redis is retried for retry-able errors. The recovery design is to make Redis highly available within the active region and to reprovision it from scratch in the DR region.

* Use the managed service for your cloud: [Amazon ElastiCache](https://aws.amazon.com/elasticache/redis/), [Google Cloud Memorystore](https://cloud.google.com/memorystore), or [Azure Cache for Redis](https://azure.microsoft.com/en-us/products/cache).
* Enable Multi-AZ failover.
* For cross-region DR, provision a fresh Redis instance in the DR region during failover; do **not** reuse an active region's Redis URI in the new cluster.

> [!WARNING]
>
> Each LangSmith installation must use its own dedicated Redis instance. **Do not share a Redis instance across two installations**, including a primary and a DR replica that may both be active at any point. Sharing Redis causes deployment tasks to be routed to the wrong cluster. See [Connect external Redis](../Connect%20external%20services/Connect%20to%20an%20external%20Redis%20or%20Valkey%20database.md).

## Kubernetes configuration and secrets

The Helm chart values, Kubernetes `Secret`s, and identity bindings are as important as your data backups. A complete restore requires both.

* **Helm values:** Store `values.yaml` in source control. Track per-environment overrides separately.
* **Image versions:** Pin the LangSmith chart version and image tags so a recovery installs the same software version. See [Self-host upgrades](Upgrade%20an%20installation.md) and [Dependency versions](../Install%20an%20instance/Minimum%20versions%20for%20self-hosting%20dependencies.md).
* **Secrets:** LangSmith reads database, blob, and licensing credentials from Kubernetes `Secret`s. Mirror these to your DR cluster's secret manager ([AWS Secrets Manager](https://aws.amazon.com/secrets-manager/), [GCP Secret Manager](https://cloud.google.com/secret-manager), or [Azure Key Vault](https://azure.microsoft.com/en-us/products/key-vault/)). See [Use an existing secret](../Platform%20auth%20%26%20access%20control/Use%20an%20existing%20secret%20for%20your%20installation%20%28Kubernetes%29.md).
* **TLS material:** If you terminate TLS at the LangSmith ingress, back up the certificate and key, or reissue from your private CA in the DR region. See [Custom TLS certificates](../Platform%20auth%20%26%20access%20control/Configure%20custom%20TLS%20certificates.md).
* **IRSA / Workload Identity bindings:** Recreate IAM roles and service-account bindings in the DR region; service account ARNs and annotations are region-scoped.
* **License key:** Keep the LangSmith license key alongside other recovery secrets.

## Reference deployment patterns

### Single region with Multi-AZ HA (recommended baseline)

This is the minimum production posture and protects against zonal failures. It does not protect against a regional outage.

* Kubernetes node pools across at least two availability zones.
* Postgres in Multi-AZ HA mode (RDS Multi-AZ, Cloud SQL HA, or Flexible Server zone-redundant).
* ClickHouse as a managed service, or a 3-node replicated cluster spread across AZs.
* Redis with Multi-AZ failover enabled.
* Blob storage with versioning enabled and a redundancy tier of at least zone-redundant.
* Daily snapshots of every data store retained for at least 7 days.

### Cross-region active/passive DR

This protects against a regional outage. It is significantly more expensive but is the right pattern for tier-1 deployments.

* A second Kubernetes cluster in the DR region with the LangSmith Helm chart installed but scaled to a low replica count (warm) or zero (cold).
* Postgres cross-region replica (RDS or Aurora cross-region replica, Cloud SQL cross-region replica, Azure Flexible Server cross-region replica). Promote on failover.
* ClickHouse Cloud or LangSmith Managed ClickHouse with a region failover plan, **or** ClickHouse backups copied to the DR region and restored into a fresh self-managed cluster on failover. Cross-region ClickHouse replication is not generally supported (ClickHouse Cloud does not offer it either), so plan for backup/restore rather than a hot DR replica.
* Blob storage replicated to a DR bucket with versioning and matching lifecycle rules.
* Redis provisioned fresh in the DR region during failover.
* DNS managed by [Route 53](https://aws.amazon.com/route53/), [Cloud DNS](https://cloud.google.com/dns), or [Azure DNS](https://azure.microsoft.com/en-us/products/dns/) with health checks and failover policies pointing at the LangSmith frontend ingress in each region.

> [!NOTE]
>
> LangSmith is a single-write platform. A cross-region deployment should be **active/passive**, not active/active. Writing to both regions concurrently against the same logical installation is not supported and will produce data inconsistency.

## Recovery procedures

### Restore after a zonal failure

In a single-region Multi-AZ deployment, zonal failures are handled automatically by your cloud provider:

1. Managed Postgres fails over to its standby in another AZ. LangSmith pods reconnect via the cluster endpoint after retry.
2. Managed Redis fails over similarly. LangSmith retries reconnect automatically.
3. Kubernetes reschedules LangSmith pods on healthy nodes in remaining AZs. Verify that node pools and Horizontal Pod Autoscaler limits allow this headroom.
4. Verify ingest by submitting a test trace from the SDK and confirming it appears in the UI.

### Restore after a regional failure

This is the cross-region failover runbook. Adapt to your specific infrastructure.

**1. Declare failover**

Confirm the primary region is unavailable. Communicate to stakeholders that you are failing over and what the expected RTO is.

**2. Promote data stores**

Promote the Postgres cross-region replica to primary in the DR region. For ClickHouse Cloud or LangSmith Managed ClickHouse, initiate the documented region failover. For self-managed ClickHouse, restore the latest backup into the DR cluster (this is typically the longest step).

**3. Repoint blob storage**

Update the LangSmith Helm `config.blobStorage.bucketName` and `apiURL` to point at the DR bucket. Confirm the bucket has the same TTL lifecycle rules. See [Blob storage configuration](../Connect%20external%20services/Enable%20blob%20storage.md#configuration).

**4. Provision Redis**

Create a fresh managed Redis instance in the DR region. Update the LangSmith Helm `redis.external` values to point at it. **Do not import dumps from the primary Redis**; provision empty.

**5. Scale the DR cluster**

If running warm/cold, scale the LangSmith deployments to their production replica counts. Apply any pending Helm value updates from source control.

**6. Run smoke tests**

Submit a test trace, verify it lands in ClickHouse and (if blob storage is enabled) in the DR bucket. Open the UI and confirm traces, datasets, and projects load. Validate authentication. See [Diagnostics](../../../Deploy/Deploy%20to%20Self-hosted/Configure/Troubleshooting%20for%20self-hosted%20deployments.md).

**7. Cut DNS over**

Update DNS to route traffic to the DR ingress. Communicate the cutover to stakeholders.

**8. Plan failback**

Once the primary region is healthy, plan a controlled failback. This is typically scheduled into a maintenance window and involves rebuilding the primary as the new DR replica before swapping again.

### Restore from snapshot

If you have lost the primary data store entirely and need to restore from snapshot:

**1. Stop ingestion**

Scale `langsmith-queue` and `langsmith-ingest-queue` to zero so no new traces are written while you restore.

**2. Restore Postgres**

Restore the Postgres backup to a new instance or perform PITR to the latest pre-incident timestamp. Update the LangSmith Helm `postgres.external` connection details to point to the restored instance.

**3. Restore ClickHouse**

Restore the most recent ClickHouse backup that aligns in time with the Postgres restore point. Restore time scales with data size.

**4. Restore blob storage**

If you lost blob data (rare), restore versioned objects from S3/GCS/Azure or copy from a replicated DR bucket.

**5. Resume ingestion**

Scale `langsmith-queue` and `langsmith-ingest-queue` back to production replica counts. Submit a smoke-test trace and verify it lands.

> [!WARNING]
>
> Always restore Postgres, ClickHouse, and blob storage to the closest possible coordinated point in time. Restoring Postgres to a more recent point than ClickHouse can produce dangling project references and missing traces in the UI.

## Testing your DR plan

A backup is only as good as the last successful restore. Schedule the following exercises:

* **Quarterly:** Restore Postgres and ClickHouse snapshots into a non-production environment and run the [diagnostics tooling](../../../Deploy/Deploy%20to%20Self-hosted/Configure/Troubleshooting%20for%20self-hosted%20deployments.md) and a smoke trace test. Measure actual restore time and confirm it is within RTO.
* **Twice yearly:** Perform a full cross-region failover drill against a staging installation. Promote the replica, repoint blob storage, scale the DR cluster, run smoke tests, and roll back.
* **On every chart upgrade:** Verify that the upgrade path does not invalidate your DR plan (for example, schema migrations applied only to the primary will need to replicate to the DR replica). See [Self-host upgrades](Upgrade%20an%20installation.md).

## Related pages

* [Scalability and resilience](../../Govern/Data%20%26%20compliance/Scalability%20%26%20resilience.md)
* [Shared responsibility model](../../Govern/Data%20%26%20compliance/LangSmith%20shared%20responsibility%20model.md)
* [Connect external Postgres](../Connect%20external%20services/Connect%20to%20an%20external%20PostgreSQL%20database.md)
* [Connect external ClickHouse](../Connect%20external%20services/Connect%20to%20an%20external%20ClickHouse%20database.md)
* [Connect external Redis](../Connect%20external%20services/Connect%20to%20an%20external%20Redis%20or%20Valkey%20database.md)
* [Enable blob storage](../Connect%20external%20services/Enable%20blob%20storage.md)
* [Self-host upgrades](Upgrade%20an%20installation.md)
* [Use an existing secret](../Platform%20auth%20%26%20access%20control/Use%20an%20existing%20secret%20for%20your%20installation%20%28Kubernetes%29.md)
* [Diagnostics for self-hosted](../../../Deploy/Deploy%20to%20Self-hosted/Configure/Troubleshooting%20for%20self-hosted%20deployments.md)
* [AWS self-hosted reference architecture](../Get%20started%20by%20cloud%20provider/Self-hosted%20LangSmith%20on%20AWS.md)
* [GCP self-hosted reference architecture](../Get%20started%20by%20cloud%20provider/Self-hosted%20LangSmith%20on%20GCP.md)
* [Azure self-hosted reference architecture](../Get%20started%20by%20cloud%20provider/Self-hosted%20LangSmith%20on%20Azure.md)

# Enable SmithDB on self-hosted LangSmith

> Run SmithDB alongside ClickHouse on a self-hosted LangSmith Kubernetes installation.

> [!NOTE]
>
> SmithDB is an opt-in datastore for self-hosted LangSmith. ClickHouse is required on LangSmith 0.16 and remains the default on 0.17. Do not disable ClickHouse on any version below 0.17. The minimum LangSmith version depends on your cloud. See [Cloud support](#cloud-support).

SmithDB is a columnar datastore built for agent trace data: deeply nested spans, multi-modal content, and spans that stay open for hours. It keeps durable data in object storage with a per-pod disk cache, and serves LangSmith trace ingestion and queries alongside the existing ClickHouse datastore.

Some LangSmith features, such as the Trajectory view, trajectory evaluators, and the filter query syntax, require SmithDB. See [SmithDB feature availability](../SmithDB%20feature%20availability.md).

> [card] [Feature availability](../SmithDB%20feature%20availability.md)
>
> See which features need SmithDB and what keeps working on ClickHouse.

> [card] [Install SmithDB](../Install%20SmithDB/Install%20LangSmith%20with%20SmithDB.md)
>
> Stage infrastructure, deploy SmithDB services, enable dual ingestion, and switch queries after validation.

> [card] [Prepare supporting infrastructure](../Install%20SmithDB/Prepare%20SmithDB%20supporting%20infrastructure.md)
>
> Provide a dedicated PostgreSQL metastore, object storage, and cache storage.

> [card] [Configure for scale](../Install%20SmithDB/Configure%20SmithDB%20for%20scale.md)
>
> Choose a tested resource tier and size SmithDB workloads.

> [card] [Configure observability](../Monitoring%20and%20alerting/Configure%20SmithDB%20observability.md)
>
> Scrape SmithDB metrics and export logs and traces to your stack.

> [card] [Migrate historical data](../Install%20SmithDB/Migrate%20ClickHouse%20history%20to%20SmithDB.md)
>
> Backfill ClickHouse history into SmithDB before query cutover.

> [card] [Essential SmithDB metrics](../Monitoring%20and%20alerting/Essential%20SmithDB%20metrics.md)
>
> Metrics to watch on each SmithDB component and how to read them.

> [card] [Troubleshoot SmithDB](../Install%20SmithDB/Troubleshoot%20SmithDB.md)
>
> Gather context, disable SmithDB, or reset a deployment safely.

## Cloud support

You can enable SmithDB on any supported LangSmith Kubernetes installation, whether it is brand new or already serving traffic. [Self-host LangSmith on Kubernetes](../../Install%20an%20instance/Self-host%20LangSmith%20on%20Kubernetes.md) covers the base installation; the guides above cover everything SmithDB adds on top of it.

Examples in these guides cover managed Kubernetes on AWS, GCP, and Azure. They do not cover self-managed clusters.

| Cloud | Minimum version |
| - | - |
| AWS (EKS) | LangSmith 0.16, Helm chart `0.16.14` or later |
| GCP (GKE) | LangSmith 0.16, Helm chart `0.16.14` or later |
| Azure (AKS) | LangSmith 0.17 |

## Components

Enabling SmithDB in the default cluster mode adds the following workloads to your cluster. Three services cache trace data on disk, on a network-attached volume or local SSD; the other two services are small and run on general compute. See [Cache storage](../Install%20SmithDB/Prepare%20SmithDB%20supporting%20infrastructure.md#cache-storage). To run SmithDB as one pod instead, see [Choose a deployment mode](../Install%20SmithDB/Configure%20SmithDB%20for%20scale.md#choose-a-deployment-mode). For what each component does and how it works with LangSmith, see [SmithDB architecture](SmithDB%20architecture.md).

| Component | Type | Disk cache | Scaling |
| - | - | - | - |
| Ingestion | Service | Yes | Horizontal |
| Query | Service | Yes | Horizontal |
| Compaction worker | Service | Yes | Horizontal |
| Compaction | Service | No | Single instance |
| Cluster manager | Service | No | Single instance |
| Metastore migration | Job | No | Runs once |
| Migration | Job, only if you [migrate historical data](../Install%20SmithDB/Migrate%20ClickHouse%20history%20to%20SmithDB.md) | No | Parallelism |

SmithDB keeps all data in object storage and the metastore. Its pods hold only copies of data and work in progress, so Kubernetes can replace any pod without data loss, and each component recovers automatically when it starts again. LangSmith keeps writes in Redis until SmithDB confirms them, and sends them again if they fail. If the metastore, object storage, or Redis is unavailable, writes wait until it recovers. A long outage can exceed the retry limit.

## Storage requirements

A self-hosted LangSmith installation uses PostgreSQL for operational data, Redis or Valkey for queuing and caching, and optional blob storage. Traces and feedback live in ClickHouse, in SmithDB, or in both while an installation runs dual ingestion. SmithDB adds its own metastore, object store, and cache storage.

On 0.17, a new installation can run SmithDB without ClickHouse; see [Install without ClickHouse](../Install%20SmithDB/Install%20LangSmith%20with%20SmithDB.md#install-without-clickhouse). Retiring ClickHouse from an existing installation is a separate procedure; contact LangChain through the [Support Portal](https://support.langchain.com/) before considering it.

For SDK method changes that work with both ClickHouse and SmithDB, see [Migrate to SmithDB-backed APIs](../../../../Monitor/Reference/SmithDB%20API%20migration/Migrate%20to%20SmithDB-backed%20APIs.md).

# Minimum versions for self-hosting dependencies

> Minimum supported versions for the databases, tools, and infrastructure required to self-host LangSmith.

This page lists the minimum supported versions for the databases, tools, and infrastructure used by self-hosted LangSmith. Install a version that meets or exceeds the minimum before deploying or upgrading. Using a version below the minimum is not supported and may cause installation or runtime failures.

> [!TIP]
>
> If you are using a managed service (such as Amazon RDS, Google Cloud SQL, or Azure Database), pick a version at or above the minimum listed here. Refer to the linked "External services" pages for connection and authentication details.

## Datastores

| Dependency | Minimum version | Notes |
| - | - | - |
| [PostgreSQL](../Connect%20external%20services/Connect%20to%20an%20external%20PostgreSQL%20database.md) | 14 | Primary relational store for operational data. Required for both LangSmith and standalone Agent Server deployments. Used to install the `btree_gin`, `btree_gist`, `pgcrypto`, `citext`, `ltree`, and `pg_trgm` extensions. |
| [Redis](../Connect%20external%20services/Connect%20to%20an%20external%20Redis%20or%20Valkey%20database.md) | 6.2 | Used for queueing and caching. Standalone and Redis Cluster modes are both supported. As of Agent Server 0.8.0, the Redis-backed run queue requires Redis 6.2 or later: it enqueues runs with the `ZADD ... LT` flag, which was added in 6.2. |
| [Valkey](../Connect%20external%20services/Connect%20to%20an%20external%20Redis%20or%20Valkey%20database.md) | 8 | Officially supported as a drop-in replacement for Redis. Standalone and Cluster modes are both supported. |
| [ClickHouse](../Connect%20external%20services/Connect%20to%20an%20external%20ClickHouse%20database.md) | Version specified in the [LangSmith Helm chart](https://github.com/langchain-ai/helm/releases) or greater | Stores traces and feedback. ClickHouse 24.2 or later requires LangSmith v0.6 or later. Downgrades are not supported. |

> [!WARNING]
>
> **Redis \< 6.2 and PostgreSQL \< 14 are not supported.** A LangSmith installation pointed at an older Redis or PostgreSQL instance may fail to start or behave unpredictably. Upgrade your datastore before installing or upgrading LangSmith.

## Compute and orchestration

| Dependency | Minimum version | Notes |
| - | - | - |
| [Kubernetes](Self-host%20LangSmith%20on%20Kubernetes.md) | Any version supported by the [upstream Kubernetes release cycle](https://kubernetes.io/releases/) | LangSmith is regularly tested on GKE, EKS, AKS, Minikube, and Kind. |
| [OpenShift](Self-host%20LangSmith%20on%20Kubernetes.md) | 4.14 | Supported as a Kubernetes distribution for LangSmith. |
| [Helm](https://helm.sh/docs/intro/install/) | 3 | Used to install and upgrade the LangSmith Helm chart. |
| Docker | A version compatible with [Docker Compose v2](https://docs.docker.com/compose/) | Required for Docker-based standalone Agent Server deployments. |

## LangSmith chart and platform

| Dependency | Minimum version | Notes |
| - | - | - |
| [LangSmith Helm chart](https://github.com/langchain-ai/helm/releases) | Latest stable release | We recommend pinning to the latest stable chart release. Refer to the [self-hosted changelog](../Reference/Self-hosted%20LangSmith%20changelog.md) for per-release upgrade notes. |
| Egress to `https://beacon.langchain.com` | LangSmith 0.9.0 or later | Required for license verification and usage reporting unless running in [offline mode](../Configure%20an%20instance/Egress%20for%20billing%20and%20operational%20telemetry.md). |

## Where these versions are enforced

* PostgreSQL 14 or later: refer to [Connect to an external PostgreSQL database](../Connect%20external%20services/Connect%20to%20an%20external%20PostgreSQL%20database.md#requirements).
* Redis 6.2 or later and Valkey 8: refer to [Connect to an external Redis or Valkey database](../Connect%20external%20services/Connect%20to%20an%20external%20Redis%20or%20Valkey%20database.md#requirements).
* ClickHouse: use the version specified in the [LangSmith Helm chart](https://github.com/langchain-ai/helm/releases) or greater: refer to [Connect to an external ClickHouse database](../Connect%20external%20services/Connect%20to%20an%20external%20ClickHouse%20database.md#requirements).
* Kubernetes cluster prerequisites: refer to [Self-host LangSmith on Kubernetes](Self-host%20LangSmith%20on%20Kubernetes.md#prerequisites).

If you are unsure which version is currently running, contact your database administrator or refer to your cloud provider's console. If you need to upgrade a dependency before upgrading LangSmith, refer to your vendor's documentation.

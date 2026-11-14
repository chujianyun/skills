# Configure LangSmith for scale

> Scale a self-hosted LangSmith instance for trace ingestion, evaluation workloads, and concurrent users, with example configurations for different load patterns.

> [!WARNING]
>
> The scaling guidance and example configurations on this page apply to **LangSmith version v0.13.0 or higher**.

A self-hosted LangSmith instance can handle a large number of traces and users. The default configuration for the self-hosted deployment can handle substantial load, and you can configure your deployment to be able to achieve higher scale. This page describes scaling considerations and provides some examples to help configure your self-hosted instance.

This page covers the LangSmith instance, which ingests traces and runs evaluations. To scale the Agent Server that runs your deployed agents, see [Configure Agent Server for scale](../../../Deploy/Deploy%20to%20Self-hosted/Configure/Configure%20Agent%20Server%20for%20scale.md).

For example configurations, refer to [Example LangSmith configurations for scale](#example-langsmith-configurations-for-scale).

> [!NOTE]
>
> For SmithDB resource sizing, see [Configure SmithDB for scale](../SmithDB/Install%20SmithDB/Configure%20SmithDB%20for%20scale.md).

## Summary

The table below provides an overview comparing different LangSmith configurations for various load patterns (reads / writes):

| | **[Low / low](#low-reads-low-writes)** | **[Low / high](#low-reads-high-writes)** | **[High / low](#high-reads-low-writes)** | [Medium / medium](#medium-reads-medium-writes) | [High / high](#high-reads-high-writes) |
| :- | :- | :- | :- | :- | :- |
| Concurrent frontend users (Number of users actively viewing traces on the frontend) | 5 | 5 | 50 | 20 | 50 |
| Traces submitted per second (Number of traces being ingested via SDKs or API endpoints) | 10 | 1000 | 10 | 100 | 1000 |
| **Frontend replicas** (500m CPU, 1Gi requested per replica) | 1 (default) | 4 | 2 | 2 | 4 |
| **Platform backend replicas** (1 CPU, 2Gi requested per replica) | 3 (default) | 20 | 3 (default) | 3 (default) | 20 |
| **Ingest queue replicas** (1 CPU, 2Gi requested per replica) | 3 (default) | 24 | 3 (default) | 6 | 24 |
| **Backend replicas** (1 CPU, 2Gi requested per replica) | 2 (default) | 5 | 40 | 16 | 50 |
| **Redis resources** | 8 Gi (default) | 26 Gi external | 8 Gi (default) | 13Gi external | 26 Gi external |
| **ClickHouse resources** | 4 CPU 16 Gi (default) | 10 CPU 32Gi memory | 8 CPU 16 Gi per replica | 16 CPU 24Gi memory | 14 CPU 24 Gi per replica |
| **ClickHouse setup** | Single instance | Single instance | 3-node replicated cluster (Recommended for high read loads to prevent degraded performance. Another option would be [managed clickhouse](../Connect%20external%20services/Connect%20to%20an%20external%20ClickHouse%20database.md#langsmith-managed-clickhouse).) | Single instance | 3-node replicated cluster (Recommended for high read loads to prevent degraded performance. Another option would be [managed clickhouse](../Connect%20external%20services/Connect%20to%20an%20external%20ClickHouse%20database.md#langsmith-managed-clickhouse).) |
| Postgres resources (We recommend using an external instance and enabling autoexpansion for the disk to handle growing data requirements.) | 2 CPU 8 GB memory 10 GB storage (external) | 2 CPU 8 GB memory 10 GB storage (external) | 2 CPU 8 GB memory 10 GB storage (external) | 2 CPU 8 GB memory 10 GB storage (external) | 2 CPU 8 GB memory 10 GB storage (external) |
| **Blob storage** | Disabled | Enabled | Enabled | Enabled | Enabled |

> [!NOTE]
>
> The per-replica figures above are resource requests, what the Kubernetes scheduler reserves.
> The limits are higher in every case. For the defaults the chart ships, see
> [Default resource requests and limits](#default-resource-requests-and-limits).
>
> A container that exceeds its memory limit is OOM-killed, and one that exceeds its CPU limit is
> throttled. Do not lower either below the shipped default without load-testing the result.

Below we go into more details about the read and write paths as well as provide a `values.yaml` snippet for you to start with for your self-hosted LangSmith instance.

## Default resource requests and limits

The Helm chart ships these requests and limits for the LangSmith application services. The
[summary table](#summary) above covers Postgres, Redis, and ClickHouse, along with the replica
counts to run for each load pattern.

| `values.yaml` key | Requests (CPU / memory) | Limits (CPU / memory) | Default replicas |
| :- | :- | :- | :- |
| `frontend` | 500m / 1Gi | 1000m / 2Gi | 1 |
| `backend` | 1000m / 2Gi | 2000m / 4Gi | 2 |
| `platformBackend` | 1000m / 2Gi | 2000m / 4Gi | 3 |
| `ingestQueue` | 1000m / 2Gi | 2000m / 4Gi | 3 |
| `queue` | 1000m / 2Gi | 2000m / 4Gi | 1 |
| `playground` | 500m / 1Gi | 1000m / 8Gi | 1 |
| `aceBackend` | 1000m / 2000Mi | 2000m / 4000Mi | 1 |
| `hostBackend` | 200m / 1000Mi | 1000m / 2Gi | 1 |
| `listener` | 1000m / 2Gi | 2000m / 4Gi | 1 |
| `operator` | 1000m / 2Gi | 2000m / 4Gi | 1 |

Each key nests its resources under `deployment`, so the backend's requests are at
`backend.deployment.resources.requests`. `playground` is the one service whose memory limit
sits far above its request, 8Gi against 1Gi, so size the nodes it schedules onto for the
limit. To confirm the defaults for your chart version, run
`helm show values langchain/langsmith`.

## Default autoscaling ranges

Autoscaling is disabled by default on every service in the table below. Each one ships two
blocks with the same replica range: `autoscaling.hpa`, for a Kubernetes
HorizontalPodAutoscaler (HPA), and `autoscaling.keda`, for
[KEDA](https://keda.sh/) (Kubernetes Event-driven Autoscaling). Enable one or the other, not
both.

| `values.yaml` key | Min replicas | Max replicas |
| :- | :- | :- |
| `frontend` | 1 | 5 |
| `backend` | 2 | 6 |
| `platformBackend` | 3 | 10 |
| `ingestQueue` | 3 | 10 |
| `queue` | 1 | 10 |
| `playground` | 1 | 5 |
| `aceBackend` | 1 | 5 |
| `hostBackend` | 1 | 5 |
| `listener` | 1 | 10 |

The HPA keys are `minReplicas` and `maxReplicas`; the KEDA equivalents are `minReplicaCount`
and `maxReplicaCount`. `operator` has no autoscaling block and always runs at its configured
replica count. For the queue services, prefer KEDA, which scales on queue backlog rather than
on CPU and memory alone. For more information, see
[KEDA autoscaling for LangSmith queues](#keda-autoscaling-for-langsmith-queues).

> [!WARNING]
>
> Enabling autoscaling overrides your replica count. When either block is enabled for a
> service, the chart stops setting `replicas` on that deployment and the autoscaler owns it, so
> the `deployment.replicas` value you configured is no longer applied.
>
> The shipped maximums are generic starting points, not values matched to the load patterns in
> the [summary table](#summary). [High reads, high writes](#high-reads-high-writes) calls for
> 50 `backend` replicas, 24 `ingestQueue`, and 20 `platformBackend`, against shipped maximums
> of 6, 10, and 10. A deployment sized for that load and then switched to autoscaling runs at a
> fraction of the capacity you configured.

Set `maxReplicas` at or above the replica count for your load pattern, and `minReplicas` to
the steady-state count you want to hold. The
[example configurations](#example-langsmith-configurations-for-scale) give both a fixed
replica count and a commented autoscaling range for each service.

## Trace ingestion (write path)

Common usage that put load on the write path:

* Ingesting traces via the Python or JavaScript LangSmith SDK
* Ingesting traces via the `@traceable` wrapper
* Submitting traces via the `/runs/multipart` endpoint

Services that play a large role in trace ingestion:

* Platform backend service: Receives initial request to ingest traces and places traces on a Redis queue
* Redis cache: Used to queue traces that need to be persisted
* Ingest queue service: Persists traces from the Redis queue to each enabled trace store, ClickHouse, SmithDB, or both
* ClickHouse: Persistent storage used for traces
* SmithDB ingestion service: Receives traces from the ingest queue service and writes them to object storage. Runs only when SmithDB ingestion is enabled. In unified mode, the single SmithDB pod handles ingestion.

With [SmithDB](../SmithDB/Overview/Enable%20SmithDB%20on%20self-hosted%20LangSmith.md) dual ingestion enabled, the ingest queue service writes each batch to ClickHouse and SmithDB in parallel. A batch finishes only when both writes finish, so a slow store slows the ingest queue. When one write fails, the retry writes only to the store that failed. An installation that runs [without ClickHouse](../SmithDB/Install%20SmithDB/Install%20LangSmith%20with%20SmithDB.md#install-without-clickhouse) writes to SmithDB alone.

When scaling up the write path (trace ingestion), monitor the services and resources listed above. Here are some typical changes that can help increase performance of trace ingestion:

* Give ClickHouse more resources (CPU and memory) if it is approaching resource limits.
* If SmithDB ingestion is enabled, size the SmithDB ingestion service for your write load. See [Configure SmithDB for scale](../SmithDB/Install%20SmithDB/Configure%20SmithDB%20for%20scale.md).
* Increase the number of platform-backend pods if ingest requests are taking long to respond.
* Increase ingest queue service pod replicas if traces are not being processed from Redis fast enough.
* Use a larger Redis cache if you notice that the current Redis instance is reaching resource limits. This could also be a reason why ingest requests take a long time.

## Trace querying (read path)

Common usage that puts load on the read path:

* Users on the frontend looking at tracing projects or individual traces
* Scripts used to query for trace info
* Hitting either the `/runs/query` or `/runs/<run-id>` api endpoints

Services that play a large role in querying traces:

* Backend service: Receives the request and submits a query to ClickHouse to then respond to the request
* ClickHouse: Persistent storage for traces. This is the main database that is queried when requesting trace info.

When scaling up the read path (trace querying), it is helpful to monitor the two services/resources listed above. Here are some typical changes that can help improve performance of trace querying:

* Increase the number of backend service pods. This would be most impactful if backend service pods are reaching 1 core CPU usage.
* Give ClickHouse more resources (CPU or Memory). ClickHouse can be very resource intensive, but it should lead to better performance.
* Move to a [replicated ClickHouse cluster](../Connect%20external%20services/Connect%20to%20an%20external%20ClickHouse%20database.md#ha-replicated-clickhouse-cluster). Adding replicas of ClickHouse helps with read performance, but we recommend staying below 5 replicas (start with 3).

For more precise guidance on how this translates to helm chart values, refer to the examples the following [section](#example-langsmith-configurations-for-scale). If you are unsure why your LangSmith instance cannot handle a certain load pattern, contact the LangChain team.

## KEDA autoscaling for LangSmith queues

> [!NOTE]
>
> Available in LangSmith v0.13.0 and later.

We highly recommend installing KEDA on your cluster. KEDA enables the `queue` and `ingest-queue` services to scale automatically based on their queue backlog size, as well as CPU and memory. This results in more efficient resource utilization and better handling of traffic spikes.

### Install KEDA

```bash
helm repo add kedacore https://kedacore.github.io/charts
helm install keda kedacore/keda --namespace keda --create-namespace
```

### Configure KEDA autoscaling

Once KEDA is installed, you can enable KEDA-based autoscaling for the `queue` and `ingest-queue` services in your `values.yaml`:

```yaml
queue:
  autoscaling:
    keda:
      enabled: true

ingestQueue:
  autoscaling:
    keda:
      enabled: true
```

With KEDA enabled, the queue services will automatically scale up when their backlog grows and scale down when their backlog is processed. This is especially useful for handling variable trace ingestion loads without over-provisioning resources.

> [!NOTE]
>
> You can also enable KEDA for other services (`backend`, `platformBackend`, etc) but they will still only scale with CPU and memory.

## Example LangSmith configurations for scale

Below we provide some example LangSmith configurations based on expected read and write loads.

For read load (trace querying):

* Low means roughly 5 users looking at traces at a time (about 10 requests per second)
* Medium means roughly 20 users looking at traces at a time (about 40 requests per second)
* High means roughly 50 users looking at traces at a time (about 100 requests per second)

For write load (trace ingestion):

* Low means up to 10 traces submitted per second
* Medium means up to 100 traces submitted per second
* High means up to 1000 traces submitted per second

> [!NOTE]
>
> The exact optimal configuration depends on your usage and trace payloads. Use the examples below in combination with the information above and your specific usage to update your LangSmith configuration as you see fit. If you have any questions, please reach out to the LangChain team.

### Low reads, low writes&#x20;

The default LangSmith configuration will handle this load. No custom resource configuration is needed here.

### Low reads, high writes&#x20;

You have a very high scale of trace ingestions, but single digit number of users on the frontend querying traces at any one time.

For this, we recommend a configuration like this:

```yaml
config:
  blobStorage:
    # Please also set the other keys to connect to your blob storage. See configuration section.
    enabled: true
  settings:
    redisRunsExpirySeconds: "3600"
# ttl:
#   enabled: true
#   ttl_period_seconds:
#     longlived: "7776000"  # 90 days (default is 400 days)
#     shortlived: "604800"  # 7 days (default is 14 days)

frontend:
  deployment:
    replicas: 4 # OR enable autoscaling below
# autoscaling:
#   hpa:
#     enabled: true
#     minReplicas: 2
#     maxReplicas: 4

platformBackend:
  deployment:
    replicas: 20 # OR enable autoscaling below
# autoscaling:
#   hpa:
#     enabled: true
#     minReplicas: 8
#     maxReplicas: 20

ingestQueue:
  deployment:
    replicas: 24 # OR enable KEDA autoscaling below
# autoscaling:
#   keda:
#     enabled: true
#     minReplicaCount: 8
#     maxReplicaCount: 24

backend:
  deployment:
    replicas: 5 # OR enable autoscaling below
# autoscaling:
#   hpa:
#     enabled: true
#     minReplicas: 3
#     maxReplicas: 5

## Ensure your Redis cache is at least 26 GB for high write scale
redis:
  external:
    enabled: true
    existingSecretName: langsmith-redis-secret # Set the connection url for your external Redis instance (26+ GB)

clickhouse:
  statefulSet:
    persistence:
      # This may depend on your configured TTL (see config section).
      # We recommend 600Gi for every shortlived TTL day if operating at this scale constantly.
      size: 4200Gi # This assumes 7 days TTL and operating a this scale constantly.
    resources:
      requests:
        cpu: "10"
        memory: "32Gi"
      limits:
        cpu: "16"
        memory: "48Gi"

commonEnv:
  - name: "CLICKHOUSE_ASYNC_INSERT_WAIT_PCT_FLOAT"
    value: "0"
```

### High reads, low writes&#x20;

You have a relatively low scale of trace ingestions, but many frontend users querying traces and/or have scripts that hit the `/runs/query` or `/runs/<run-id>` endpoints frequently.

**For this, we strongly recommend setting up a replicated ClickHouse cluster to enable high read scale at low latency.** See our [external ClickHouse doc](../Connect%20external%20services/Connect%20to%20an%20external%20ClickHouse%20database.md#ha-replicated-clickhouse-cluster) for more guidance on how to setup a replicated ClickHouse cluster. For this load pattern, we recommend using a 3 node replicated setup, where each replica in the cluster should have resource requests of 8+ cores and 16+ GB memory, and resource limit of 12 cores and 32 GB memory.

For this, we recommend a configuration like this:

```yaml
config:
  blobStorage:
    # Please also set the other keys to connect to your blob storage. See configuration section.
    enabled: true

frontend:
  deployment:
    replicas: 2

ingestQueue:
  deployment:
    replicas: 3 # OR enable KEDA autoscaling below
# autoscaling:
#   keda:
#     enabled: true
#     minReplicaCount: 2
#     maxReplicaCount: 3

backend:
  deployment:
    replicas: 40 # OR enable autoscaling below
# autoscaling:
#   hpa:
#     enabled: true
#     minReplicas: 16
#     maxReplicas: 40

# We strongly recommend setting up a replicated clickhouse cluster for this load.
# Update these values as needed to connect to your replicated clickhouse cluster.
clickhouse:
  external:
    # If using a 3 node replicated setup, each replica in the cluster should have resource requests of 8+ cores and 16+ GB memory, and resource limit of 12 cores and 32 GB memory.
    enabled: true
    host: langsmith-ch-clickhouse-replicated.default.svc.cluster.local
    port: "8123"
    nativePort: "9000"
    user: "default"
    password: "password"
    database: "default"
    cluster: "replicated"
```

### Medium reads, medium writes&#x20;

This is a good all around configuration that should be able to handle most usage patterns of LangSmith. In internal testing, this configuration allowed us to scale to 100 traces ingested per second and 40 read requests per second.

For this, we recommend a configuration like this:

```yaml
config:
  blobStorage:
    # Please also set the other keys to connect to your blob storage. See configuration section.
    enabled: true
  settings:
    redisRunsExpirySeconds: "3600"

frontend:
  deployment:
    replicas: 2

ingestQueue:
  deployment:
    replicas: 6 # OR enable KEDA autoscaling below
# autoscaling:
#   keda:
#     enabled: true
#     minReplicaCount: 3
#     maxReplicaCount: 6

backend:
  deployment:
    replicas: 16 # OR enable autoscaling below
# autoscaling:
#   hpa:
#     enabled: true
#     minReplicas: 8
#     maxReplicas: 16

redis:
  statefulSet:
    resources:
      requests:
        memory: 13Gi
      limits:
        memory: 13Gi

  # -- For external redis instead use something like below --
  # external:
  #   enabled: true
  #   connectionUrl: "<URL>" OR existingSecretName: "<SECRET-NAME>"

clickhouse:
  statefulSet:
    persistence:
      # This may depend on your configured TTL.
      # We recommend 60Gi for every shortlived TTL day if operating at this scale constantly.
      size: 420Gi # This assumes 7 days TTL and operating a this scale constantly.
    resources:
      requests:
        cpu: "16"
        memory: "24Gi"
      limits:
        cpu: "28"
        memory: "40Gi"

commonEnv:
  - name: "CLICKHOUSE_ASYNC_INSERT_WAIT_PCT_FLOAT"
    value: "0"
```

> [!WARNING]
>
> If you still notice slow reads with the above configuration, we recommend moving to a [replicated Clickhouse cluster setup](../Connect%20external%20services/Connect%20to%20an%20external%20ClickHouse%20database.md#ha-replicated-clickhouse-cluster)

### High reads, high writes&#x20;

You have a very high rate of trace ingestion (approaching 1000 traces submitted per second) and also have many users querying traces on the frontend (over 50 users) and/or scripts that are consistently making requests to `/runs/query` or `/runs/<run-id>` endpoints.

**For this, we very strongly recommend setting up a replicated ClickHouse cluster to prevent degraded read performance at high write scale.** See our [external ClickHouse doc](../Connect%20external%20services/Connect%20to%20an%20external%20ClickHouse%20database.md#ha-replicated-clickhouse-cluster) for more guidance on how to set up a replicated ClickHouse cluster. For this load pattern, we recommend using a 3 node replicated setup, where each replica in the cluster should have resource requests of 14+ cores and 24+ GB memory, and resource limit of 20 cores and 48 GB memory. We also recommend that each node/instance of ClickHouse has 600 Gi of volume storage for each day of TTL that you enable (as per the configuration below).

Overall, we recommend a configuration like this:

```yaml
config:
  blobStorage:
    # Please also set the other keys to connect to your blob storage. See configuration section.
    enabled: true
  settings:
    redisRunsExpirySeconds: "3600"
# ttl:
#   enabled: true
#   ttl_period_seconds:
#     longlived: "7776000"  # 90 days (default is 400 days)
#     shortlived: "604800"  # 7 days (default is 14 days)

frontend:
  deployment:
    replicas: 4 # OR enable autoscaling below
# autoscaling:
#   hpa:
#     enabled: true
#     minReplicas: 2
#     maxReplicas: 4

platformBackend:
  deployment:
    replicas: 20 # OR enable autoscaling below
# autoscaling:
#   hpa:
#     enabled: true
#     minReplicas: 8
#     maxReplicas: 20

ingestQueue:
  deployment:
    replicas: 24 # OR enable KEDA autoscaling below
# autoscaling:
#   keda:
#     enabled: true
#     minReplicaCount: 8
#     maxReplicaCount: 24

backend:
  deployment:
    replicas: 50 # OR enable autoscaling below
# autoscaling:
#   hpa:
#     enabled: true
#     minReplicas: 20
#     maxReplicas: 50

## Ensure your Redis cache is at least 26 GB for high write scale
redis:
  external:
    enabled: true
    existingSecretName: langsmith-redis-secret # Set the connection url for your external Redis instance (26+ GB)

# We strongly recommend setting up a replicated clickhouse cluster for this load.
# Update these values as needed to connect to your replicated clickhouse cluster.
clickhouse:
  external:
    # If using a 3 node replicated setup, each replica in the cluster should have resource requests of 14+ cores and 24+ GB memory, and resource limit of 20 cores and 48 GB memory.
    enabled: true
    host: langsmith-ch-clickhouse-replicated.default.svc.cluster.local
    port: "8123"
    nativePort: "9000"
    user: "default"
    password: "password"
    database: "default"
    cluster: "replicated"

commonEnv:
  - name: "CLICKHOUSE_ASYNC_INSERT_WAIT_PCT_FLOAT"
    value: "0"
```

> [!NOTE]
>
> Ensure that the Kubernetes cluster is configured with sufficient resources to scale to the recommended size. After deployment, all of the pods in the Kubernetes cluster should be in a `Running` state. Pods stuck in `Pending` may indicate that you are reaching node pool limits or need larger nodes.
>
> Also, ensure that any ingress controller deployed on the cluster is able to handle the desired load to prevent bottlenecks.

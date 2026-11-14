# Configure SmithDB for scale

> Choose tested SmithDB resource tiers and size Kubernetes workloads and the PostgreSQL metastore.

> [!NOTE]
>
> For non-SmithDB LangSmith services, see [Configure LangSmith for scale](../../Configure%20an%20instance/Configure%20LangSmith%20for%20scale.md).

Use these tested tiers as starting configurations for SmithDB. Connect SmithDB to your monitoring stack before you tune capacity, so you can observe the effect of each change. See [Configure SmithDB observability](../Monitoring%20and%20alerting/Configure%20SmithDB%20observability.md).

## Choose a deployment mode

> [!NOTE]
>
> `smithdb.topology` requires Helm chart `0.18.0` or later.

Set `smithdb.topology` to `unified` or `cluster`, and enable dedicated query services on top of `cluster` when needed:

| Mode | What runs | Use it for |
| - | - | - |
| `unified` | One `smithdb all` pod that runs ingestion, query, and compaction | Test environments and low-volume installations |
| `cluster` (default) | Separate ingestion, query, and compaction workloads, coordinated by a cluster manager | Production installations |
| `cluster` with [dedicated query services](#dedicated-query-services) | Cluster mode plus separate services for run statistics, run rules, or mutations | Production installations where one kind of query load slows others |

```yaml
smithdb:
  topology: unified
```

Unified mode runs one `smithdb all` replica, sized by the [unified tiers](#unified-tiers). While the pod restarts or recovers from a node failure, queries fail. LangSmith queues incoming traces in Redis and writes them once the pod is running again, so ingestion is delayed rather than dropped. A PodDisruptionBudget keeps node drains from evicting the pod.

### Dedicated query services

In cluster mode, the query service serves all SmithDB reads. To isolate a workload, enable a dedicated service:

| Service | Serves | Enable with |
| - | - | - |
| Stats query | Run statistics, such as run counts, latency, and error rates | `smithdb.statsQuery.enabled` |
| Run rules | Automation rules and online evaluation | `smithdb.runRules.enabled` |
| Mutations | Feedback updates and run deletions | `smithdb.mutations.enabled` |

Each service has its own replicas and autoscaling, and uses the query tier's resources.

## Choose and scale a tier

The tiers are not throughput limits or prescribed configurations. CPU, memory, and cache size are per replica. Cache size is the volume each replica gets: the claim size on a network-attached disk, or the `emptyDir` limit on local SSD.

Choose the tier whose tested ingestion and query rates most closely match or exceed your expected steady-state load. To estimate your current trace volume, open **Settings > Usage** in LangSmith. See [Granular billable usage](../../../Account/Billing%20%26%20usage/Granular%20billable%20usage.md).

If you cannot measure your load, start at `small` and scale up.

Apply the per-replica resources and starting replica counts from the selected tier. If the workload later outgrows that starting point, you can scale SmithDB compute horizontally.

> [!NOTE]
>
> SmithDB query, ingestion, and compaction-worker HPAs are enabled by default. They require Kubernetes Metrics Server or another `metrics.k8s.io` provider. Verify availability with `kubectl get --raw /apis/metrics.k8s.io/v1beta1`.

### Scale with KEDA instead

> [!NOTE]
>
> KEDA scaling for SmithDB compaction workers requires Helm chart `0.17.0` or later.

SmithDB compaction workers can scale on queue depth through [KEDA](https://keda.sh/) rather than the CPU-based HPA. This suits bursty compaction backlogs, where queue depth rises before CPU does. LangSmith uses the same KEDA installation for its own queues; see [KEDA autoscaling for LangSmith queues](../../Configure%20an%20instance/Configure%20LangSmith%20for%20scale.md#keda-autoscaling-for-langsmith-queues) to install and configure it.

Enable the KEDA scaler for compaction workers:

```yaml
smithdb:
  compactionWorker:
    autoscaling:
      hpa:
        enabled: false
      keda:
        enabled: true
```

Use either the HPA or KEDA for a component, not both.

## Baseline tiers

In cluster mode, each tier sets the per-replica resources for each component:

| Component | Small 10 ingest / 10 query QPS | Medium 100 ingest / 40 query QPS | Large 1000 ingest / 100 query QPS |
| - | - | - | - |
| Ingestion | 1 replica 4 CPU 8 Gi memory 100 Gi cache | 1 replica 16 CPU 32 Gi memory 100 Gi cache | 2 replicas 56 CPU 150 Gi memory 1000 Gi cache |
| Query | 1 replica 4 CPU 8 Gi memory 200 Gi cache | 1 replica 28 CPU 48 Gi memory 200 Gi cache | 4 replicas 28 CPU 50 Gi memory 1000 Gi cache |
| Compaction | 1 replica 2 CPU 4 Gi memory | 1 replica 4 CPU 8 Gi memory | 1 replica 8 CPU 16 Gi memory |
| Compaction worker | 1 replica 8 CPU 16 Gi memory 100 Gi cache | 1 replica 16 CPU 32 Gi memory 100 Gi cache | 4 replicas 28 CPU 50 Gi memory 300 Gi cache |
| Cluster manager | 1 replica 250m CPU 256 Mi memory | 1 replica 250m CPU 256 Mi memory | 1 replica 2 CPU 2 Gi memory |

### Unified tiers

In unified mode, `smithdb.resourceTier` sizes the SmithDB pod:

| Component | Small | Medium | Large |
| - | - | - | - |
| Unified | 1 replica 4 CPU 16 Gi memory 100 Gi cache | 1 replica 16 CPU 64 Gi memory 300 Gi cache | 1 replica 32 CPU 128 Gi memory 1000 Gi cache |

To override the tier's CPU and memory, set `smithdb.unified.deployment.resources`. When the workload outgrows the large tier, switch to cluster mode.

## Configure resources with Helm

The chart defaults to `small`. Select `small`, `medium`, or `large`:

```yaml
smithdb:
  resourceTier: medium
```

On LangSmith 0.17 the tier's cache size becomes the generated claim's capacity. On 0.16 it is the `ephemeral-storage` request and limit, which also sizes the generated `emptyDir`. Replica counts and autoscaling are configured separately.

An explicit component `resources` block replaces the tier's CPU and memory. On 0.17 it does not change the cache size; pick a different tier or override `deployment.volumes` for that. For local SSD values, see [Cache storage](Prepare%20SmithDB%20supporting%20infrastructure.md#cache-storage).

See [SmithDB resource tiers](https://github.com/langchain-ai/helm/tree/main/charts/langsmith#smithdb-resource-tiers) for current values and chart details.

> [accordion] Example explicit resource configuration
>
> This example overrides the query component at medium-tier sizes.
>
> > [tab] LangSmith 0.17
> >
> > The cache claim stays at the tier size. These values request no node storage.
> >
> > ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > smithdb:
> >   resourceTier: medium
> >   query:
> >     deployment:
> >       resources:
> >         requests:
> >           cpu: "28"
> >           memory: "48Gi"
> >         limits:
> >           cpu: "28"
> >           memory: "48Gi"
> > ```
>
> > [tab] LangSmith 0.16
> >
> > The storage limit also sizes the default `emptyDir`.
> >
> > ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > smithdb:
> >   resourceTier: medium
> >   query:
> >     deployment:
> >       resources:
> >         requests:
> >           cpu: "28"
> >           memory: "48Gi"
> >           ephemeral-storage: "200Gi"
> >         limits:
> >           cpu: "28"
> >           memory: "48Gi"
> >           ephemeral-storage: "200Gi"
> > ```

## Metastore capacity

The baseline tiers cover SmithDB Kubernetes workloads only. They do not include the PostgreSQL metastore. Use these starting points for a dedicated metastore:

| Tier | vCPU | Memory |
| - | - | - |
| Small | 2 | 16 GiB |
| Medium | 4 | 32 GiB |
| Large | 8 | 64 GiB |

Choose the nearest supported PostgreSQL instance shape from your provider and monitor database resource use and transaction latency during rollout.

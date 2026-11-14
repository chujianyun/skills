# Scale self-hosted Sandboxes

> Plan self-hosted Sandbox capacity with host autoscaling, Kubernetes node scaling, memory headroom, and shared filesystem caching.

Self-hosted Sandboxes scale in two layers: LangSmith adjusts the host Deployment, and your node autoscaler supplies Kubernetes nodes. Plan both layers together so new hosts are ready before the existing pool runs out of capacity.

This guide builds on [Sandbox architecture](Self-hosted%20Sandbox%20architecture.md). For cloud-specific infrastructure setup, see [Enable Sandboxes](Enable%20Sandboxes%20on%20self-hosted%20LangSmith.md).

## Understand the two scaling layers

The built-in host autoscaler runs on an elected `sandbox-host`. Hosts publish their committed vCPU and sandbox counts through Kubernetes Leases. The leader uses that information to adjust the Deployment's replica count.

**autoscaling**

LangSmith requests host pods. Your infrastructure supplies nodes. A desired replica is not usable capacity until its host is ready.

The host autoscaler does not use an HPA, KEDA, or a Prometheus adapter. Do not configure another controller to manage the same Deployment's replica count.

A new host pod needs an eligible node without another host pod. When none is available, it stays `Pending` until your node autoscaler adds capacity. Configure that autoscaler for the dedicated KVM-capable node pool, including compatible labels, taints, and instance requirements.

During normal scale-down, the host autoscaler retains the recent peak target for a stabilization window. It then removes at most one host per window. Pod deletion costs favor less-loaded hosts. Removing a running host [drains its sandboxes](Operate%20self-hosted%20Sandboxes.md#follow-a-host-drain); it is not a disruption-free operation.

## Calculate a host target

Committed vCPU is the CPU requested by running sandboxes on ready hosts, not measured CPU usage. For a pool of equally sized hosts, the load-based target is:

```text
desired hosts = ceil(committed vCPU / (host vCPU × target fraction)) + headroom hosts
```

The autoscaler clamps the result to `minReplicas` and `maxReplicas`. Without a host capacity signal, it starts from the minimum. Use a homogeneous pool: the calculation assumes a common per-host CPU capacity.

For example, with 16-vCPU hosts, a 70% target, and one headroom host:

* **Per-host target**: `16 × 0.70 = 11.2` committed vCPU.
* **Workload**: 60 sandboxes requesting 0.5 vCPU each commit 30 vCPU.
* **Pool target**: `ceil(30 / 11.2) + 1 = 4` hosts, subject to the configured bounds.

The 70% target is not a per-host capacity limit. Placement can exceed it while the pool scales or when it reaches its maximum.

### Plan for bursts

The replica target can rise before nodes and hosts become ready. Headroom covers some of that delay; it does not make node provisioning instantaneous.

**scaling-behavior**

Illustrative scaling behavior, not a latency benchmark. Scale-up follows demand; scale-down waits through the stabilization window and proceeds gradually.

Choose `minReplicas` and `headroomHosts` for the burst you need to absorb while a node starts. Keep at least two hosts for a pool that must continue accepting work during a one-host rollout. Measure node startup, host readiness, and sandbox creation latency under representative load.

If the pool reaches its maximum, investigate demand and infrastructure limits rather than assuming the utilization target prevents overload. With no ready hosts, requests to create a sandbox fail. Clients need bounded retries and backoff for transient capacity failures.

## Configure the host autoscaler

The Helm values below live under `sandboxes.sandboxHost.autoscaling`. Check the values shipped with your chart version; existing overrides can change the effective settings.

| Value | Chart default | Operational guidance |
| - | - | - |
| `enabled` | `false` | Enable host autoscaling when your node pool can scale with it. |
| `minReplicas` | `1` | Use at least `2` to avoid zero ready hosts during a normal rollout. |
| `maxReplicas` | `10` | Align with eligible node capacity and infrastructure quotas. |
| `targetUtilizationPercent` | `70` | Lower values leave more CPU headroom. This measures commitment, not live usage. |
| `headroomHosts` | `1` | Adds spare capacity above the load-based target. |
| `scaleDownStabilizationSeconds` | `300` | Increase to reduce repeated drains during short demand dips. |

When autoscaling is enabled, the chart leaves the Deployment's replica count to the host autoscaler. Otherwise, `sandboxes.sandboxHost.deployment.replicas` sets a fixed host count.

Deployment annotations prefixed with `sandbox-host.smith.langchain.com/autoscale-` can override the baseline settings without restarting hosts. Inspect existing overrides when Helm values and observed scaling disagree. Prefer durable Helm configuration for normal operation.

Align three separate limits:

1. Set the host replica maximum for the peak workload.
2. Allow the node pool and infrastructure quotas to supply that many eligible nodes.
3. Set workspace sandbox quotas for the expected concurrent CPU, memory, and sandbox count.

Workspace quotas control what users can request. They do not provision nodes or guarantee physical capacity.

## Size CPU and memory together

The following example applies the same 70% target and one headroom host to 500 running sandboxes. It shows the CPU-based target before `maxReplicas` clamps it, not a performance guarantee.

| vCPU per sandbox | Total committed vCPU | 16-vCPU hosts | 32-vCPU hosts | 64-vCPU hosts |
| - | - | - | - | - |
| 0.5 | 250 | 24 | 13 | 7 |
| 1 | 500 | 46 | 24 | 13 |
| 2 | 1,000 | 91 | 46 | 24 |

Check memory separately. For example, 500 sandboxes configured with 2 GiB each request 1,000 GiB of guest memory, before host and filesystem overhead.

> [!WARNING]
>
> Host autoscaling uses committed CPU, not memory pressure. A CPU-sized pool can still run out of memory. Budget for guest memory, the host daemon, JuiceFS, caches, and Kubernetes overhead.

The host pod's memory request must reflect the workloads it contains. A small request for the daemon alone does not reserve memory for its microVMs. Review `sandboxes.sandboxHost.deployment.resources` against node allocatable memory and measured peak use.

## Balance node size and cache capacity

Larger nodes let more sandboxes share a local JuiceFS cache and amortize host overhead. However, each host failure or drain affects more sandboxes and can take longer to save their memory.

Choose nodes based on these constraints:

* **Virtualization**: Expose `/dev/kvm` on a supported Linux node configuration.
* **CPU compatibility**: Keep a consistent CPU model across the pool. See [Plan machine changes](Operate%20self-hosted%20Sandboxes.md#plan-machine-changes).
* **Memory**: Leave capacity for host and filesystem overhead, not only the requested guest memory.
* **Local storage**: Provide cache space for the working set and monitor disk pressure.
* **Failure impact**: Keep enough hosts and spare capacity to tolerate losing or draining one.

For host-owned JuiceFS mounts, `sandboxes.juicefs.hostMount.cacheDirs` selects node-local cache paths. `sandboxes.juicefs.hostMount.mountOptions` controls cache options. The chart's default cache budget is 50 GiB across the configured directories; installing a larger disk does not automatically raise that budget.

A cache can survive a pod replacement on the same node, but not replacement of that node. Treat cache warm-up as part of capacity testing, not as durable storage recovery.

## See also

* [Sandbox architecture and lifecycle](Self-hosted%20Sandbox%20architecture.md)
* [Upgrade and operate Sandboxes](Operate%20self-hosted%20Sandboxes.md)
* [Configure self-hosted resource usage](../../Interact%20with%20your%20self-hosted%20instance%20of%20LangSmith.md)

# Operate self-hosted Sandboxes

> Plan self-hosted Sandbox upgrades, understand host drains and failure recovery, protect shared storage, and monitor production capacity.

Self-hosted Sandbox operations center on the host pool and its shared storage. Host replacements affect running workloads; storage failures can affect the entire pool. Use this guide to plan upgrades and distinguish a recoverable interruption from loss of persistent data.

Start with [Sandbox architecture](Self-hosted%20Sandbox%20architecture.md) and [capacity planning](Scale%20self-hosted%20Sandboxes.md). Follow the [self-hosted upgrade guide](../../../Manage%20an%20instance/Upgrade%20an%20installation.md) for the platform-wide upgrade procedure and release requirements.

## Understand a rolling upgrade

The `sandbox-host` image packages the host daemon and runtime artifacts, including Firecracker, guest artifacts, and the JuiceFS client. Set `images.sandboxHostImage.tag` to the runtime image for your LangSmith release. Follow release-specific instructions when upgrading older storage layouts.

The host Deployment uses `maxSurge: 0` and `maxUnavailable: 1`. Kubernetes terminates a host before creating its replacement, then waits for the replacement to become ready. Required one-host-per-node placement and the shared host port prevent two host pods from occupying the same node.

**rollout**

A healthy four-host pool has three ready hosts during each replacement. The timeline is illustrative; drain and startup durations depend on the workload and storage.

A normal rollout temporarily removes one host's capacity. With a single-host pool, requests to create a sandbox fail until the replacement host is ready. Existing unready hosts or infrastructure failures can reduce capacity further; `maxUnavailable` is not a guarantee against unrelated outages.

For host-owned JuiceFS mounts, startup includes mounting the filesystem and checking storage access before opening the host listener. A replacement that cannot access storage blocks progress instead of accepting sandbox traffic.

> [!WARNING]
>
> A rolling upgrade does not guarantee uninterrupted execution. A draining host first tries to live-migrate each running Sandbox to another ready host; Sandboxes it cannot move, for example when no other host has room, are suspended and pause until they are started again. Open connections can disconnect either way. Applications must handle reconnects and interrupted work.

## Follow a host drain

A graceful host shutdown attempts to move or suspend persistent sandboxes before the pod exits:

**1. Stop new placement**

The host enters a draining state and notifies the platform backend. New sandbox placements use other ready hosts.

**2. Save running sandboxes**

The host first tries to live-migrate each running sandbox to another ready host. For each sandbox it cannot move, it stops routing to it as it suspends that VM, attempts to save the VM's memory to JuiceFS, and reports the sandbox stopped.

**3. Release the host**

The host keeps renewing its Lease while stopping workloads. Once the VMs have stopped, it releases the Lease and tears down its storage mount.

**4. Resume on demand**

A later start or wake request places the sandbox on an available, compatible host. A complete saved memory image allows processes to resume; otherwise recovery uses the persisted filesystem.

Stopped sandboxes do not all restart when the replacement host becomes ready. They remain stopped until explicitly started or reached through a request path that wakes them.

Open execution streams, tunnels, and service connections to affected sandboxes need to reconnect. A saved memory image does not preserve a client's network connection.

### Budget enough time to drain

`sandboxes.sandboxHost.deployment.terminationGracePeriodSeconds` defaults to `300`. Kubernetes can kill the host when that grace period expires, even if the host has not finished saving every sandbox's memory.

Measure a drain with representative sandbox density and memory use. Check the shutdown summary for the drain duration and how many sandboxes suspended successfully or failed to suspend. Increase the grace period when the host cannot save every sandbox's memory in time, and keep node-maintenance drain timeouts longer than that period.

An incomplete drain can lose running memory and require crash recovery for affected sandboxes. Increasing the timeout does not solve storage unavailability or insufficient capacity.

### Coordinate node maintenance

Node replacement and Kubernetes upgrades also terminate host pods. Configure your node maintenance process to respect graceful shutdown and avoid draining several sandbox hosts simultaneously.

Enable `sandboxes.sandboxHost.pdb.enabled` to use the chart's PodDisruptionBudget for voluntary evictions. Its default budget permits one unavailable host. A PDB does not prevent node failure, direct pod deletion, or every provider-specific maintenance action.

Keep node autoscaling consistent with the host autoscaler. Where your node autoscaler supports eviction protection, prevent it from independently evicting active host pods during routine consolidation. Let host scale-down drain workloads before removing empty nodes. Check your autoscaler's behavior rather than assuming one annotation works for every provider.

Do not accelerate a rollout by deleting multiple host pods or increasing disruption beyond the capacity you have tested.

### Diagnose a stalled rollout

LangSmith warns organization admins with **Sandbox host rollout is incomplete** when some hosts run its current release and others still run an older one 72 hours after it was upgraded, or at once when those hosts are two or more minor versions behind. The warning links this section for when the rollout is not progressing.

Compare desired, ready, and updated host counts, and see which release each host runs. Then inspect pod events and node provisioning:

```bash
kubectl -n <namespace> get deployment langsmith-sandbox-host
kubectl -n <namespace> get pods -l app.kubernetes.io/component=langsmith-sandbox-host \
  -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.phase}{"\t"}{.spec.containers[?(@.name=="sandbox-host")].image}{"\n"}{end}'
kubectl -n <namespace> describe pod <pending-host-pod>
kubectl -n <namespace> get events --sort-by=.lastTimestamp
```

These names assume a `langsmith` release named `langsmith`; the Deployment is `<release>-sandbox-host`. With the runtime in a [separate cluster](Run%20self-hosted%20Sandboxes%20in%20a%20separate%20cluster.md), run the commands against that cluster's context and the runtime release's namespace. There the Deployment and its component label are `<runtime release>-sandbox-host`, for example `langsmith-sandbox-sandbox-host`, and the settings on this page sit under `sandboxHost` in the `langsmith-sandbox` chart instead of `sandboxes.sandboxHost`.

* **Hosts stay `Pending`**: Check node pool limits, infrastructure quota, regional capacity, node selectors, taints, and resource requests.
* **Hosts start but do not become ready**: Check KVM availability, runtime logs, and access to JuiceFS metadata and object storage.
* **Hosts remain terminating**: Inspect drain progress and storage latency before changing the grace period.

If desired replicas exceed schedulable capacity, the rollout may be unable to meet its availability floor. Restore capacity first. The `sandbox-host.smith.langchain.com/autoscale-override` Deployment annotation can temporarily pin the host count when autoscaling is enabled. Use it only after evaluating remaining capacity, and remove the override afterward. A lower target does not fix the underlying capacity shortage.

## Plan machine changes

Memory snapshots include CPU and virtual machine state. Do not assume that a saved VM can resume across different CPU models or incompatible host kernels. [Firecracker's snapshot compatibility guidance](https://github.com/firecracker-microvm/firecracker/blob/main/docs/snapshotting/snapshot-support.md#where-can-i-resume-my-snapshots) requires matching hardware and software configurations, with limited, explicitly caveated exceptions.

Keep a consistent CPU model in the sandbox pool. Treat changes to the CPU vendor or model, host kernel, or sandbox runtime as transitions that require restore testing. A newer CPU or kernel does not automatically make a destination compatible. Compatibility in one direction does not establish compatibility in reverse.

### Example transitions, not a support matrix

> [!NOTE]
>
> These are documentation-based examples, not a tested LangSmith compatibility matrix or an expansion of supported platforms. Every lower-risk candidate still requires validation on your exact deployment. Keep the exposed CPU model and features, host kernel, and sandbox runtime consistent. Confirm that the destination meets the [Sandbox platform and KVM requirements](Enable%20Sandboxes%20on%20self-hosted%20LangSmith.md).

The examples concern host-node changes, not changes to a saved microVM's guest configuration.

| Cloud | Lower-risk candidate to validate | Do not assume memory-restore compatibility |
| - | - | - |
| AWS | Replace an `m6i.metal` node with another using the same exposed CPU configuration and software versions. [M6i instances](https://aws.amazon.com/ec2/instance-types/m6i/) use Intel Ice Lake processors. | `m6i.metal` (Ice Lake) → `m5n.metal` (Cascade Lake). Firecracker explicitly identifies this direction as incompatible. See also the [M5n processor specifications](https://aws.amazon.com/ec2/instance-types/m5/). |
| GCP | Replace or resize N2 nodes while preserving the same exposed CPU platform, kernel, and runtime. Verify the actual CPU rather than relying on the machine-family name. | An N2 node on Ice Lake → an N2 node on Cascade Lake. The [N2 series](https://docs.cloud.google.com/compute/docs/general-purpose-machines#n2_series) includes both platforms; staying within N2 does not establish memory compatibility. |
| Azure | `Standard_D16ds_v6` → `Standard_D32ds_v6`, with the same kernel and runtime. Both [Ddsv6 sizes](https://learn.microsoft.com/en-us/azure/virtual-machines/sizes/general-purpose/ddsv6-series) list the Intel Xeon Platinum 8573C (Emerald Rapids). Matching the listed processor makes this a candidate to test, not a guarantee. | A Dsv3 node replacement that exposes a different CPU model, even without a SKU change. The [Dsv3 series](https://learn.microsoft.com/en-us/azure/virtual-machines/sizes/general-purpose/dsv3-series) lists multiple generations, from Haswell through Emerald Rapids. |

A matching SKU or family is not sufficient evidence. Provider placement and available processors can vary. For example, [Google's CPU platform documentation](https://docs.cloud.google.com/compute/docs/cpu-platforms) describes machine types with multiple CPU platforms and how platform selection works.

> [!WARNING]
>
> An x86-64 memory snapshot cannot resume on an Arm CPU. An instruction-set change also requires architecture-compatible guest software; booting the same x86-64 filesystem on Arm is not a recovery strategy. Do not treat a CPU architecture change as an ordinary node resize.

### Validate a transition before rollout

To validate the source-to-target transition:

1. Confirm that the target exposes `/dev/kvm` and meets the supported platform requirements.
2. Record the exposed CPU model and features, host kernel, and `sandbox-host` image version on both source and target nodes.
3. Use isolated test capacity matching the target configuration. Resume a persistent sandbox suspended on a source node, and separately create a sandbox from a memory snapshot captured there. Confirm both run on a target node, not the original host.
4. Verify that in-memory state survives, then exercise representative workload paths. A successful VM boot alone does not establish compatibility.
5. Test the reverse direction if the rollout requires rollback. Do not assume that a snapshot captured on the target can resume on an older source configuration.

If restoration is incompatible, plan for cold starts and loss of in-memory work rather than relying on memory migration. Persistent disk recovery is separate from memory restore. Applications that need durable progress should write it to persistent storage rather than rely only on saved process memory.

## Understand failure impact

| Event | Platform behavior | Workload impact |
| - | - | - |
| Host crash or node loss | Waits for fencing before starting affected sandboxes on another host. | One host affected Running memory is lost. Persistent sandboxes recover from persisted disk on a later start or wake request. |
| Prolonged loss of Kubernetes API access | Hosts that cannot renew their Leases fence themselves to avoid conflicting writers. | One host or whole pool Can stop workloads on one host or across the pool, depending on the outage. |
| Host-owned JuiceFS mount failure | The host stops accepting work and stops its VMs before exiting. | One host affected Affected sandboxes lose running memory; recovery requires working shared storage. |
| Metadata Redis unavailable | Filesystem operations stall or fail; sustained mount health failures can stop hosts. | Pool-wide disruption Sandbox creation and running workloads can fail across the pool. |
| Object storage unavailable or throttled | Uncached reads and uploads stall or fail; new hosts may fail readiness. | Pool-wide disruption Slow or failing I/O and reduced ready capacity. |
| No ready hosts | Requests to create a sandbox fail with `NoSandboxHostsAvailable`. | Sandbox creation affected Clients must retry after capacity becomes available. |
| Metadata or object data lost | Restoring hosts alone cannot restore the filesystem. | Persistent data loss Recover the backing stores from tested backups. |

Fencing prevents a replacement from writing a persistent sandbox's disk while the old host might still be running. Recovery is therefore not instantaneous after a host disappears. Do not bypass that delay by manually changing sandbox ownership or deleting shared storage state.

## Protect sandbox storage

The JuiceFS metadata store and object store form one persistent filesystem. Protect them separately from the platform's cache and queue Redis.

* **Dedicated metadata Redis**: Use `noeviction`, high availability, persistence, and backups. Do not flush or recreate it as part of cache maintenance.
* **Memory headroom**: Alert before Redis reaches its memory limit. With `noeviction`, writes fail when memory is exhausted rather than evicting filesystem metadata.
* **Object retention**: Do not apply lifecycle rules that delete live JuiceFS objects or move them to an inaccessible storage tier.
* **Recovery testing**: Test restoring filesystem metadata and object data together. A replica improves availability but does not replace backups.
* **Private access**: Keep storage and host endpoints private. Use the installation guide's identity and secret configuration for your environment.

Choose backup frequency and retention for your recovery objectives. Do not assume an object-store backup alone contains the file tree needed to recover a sandbox.

## Monitor the pool

The host exposes Prometheus metrics on its internal `/metrics` endpoint. Scrape it through your private monitoring infrastructure, not public ingress. See [Export LangSmith telemetry](../../../Self-hosted%20observability/Export%20LangSmith%20telemetry%20to%20your%20observability%20backend.md) for platform monitoring setup.

The elected host exports these pool gauges:

| Metric | Meaning |
| - | - |
| `langsmith_sandbox_host_pool_assigned_cpu_millicores` | CPU committed to sandboxes on ready hosts. |
| `langsmith_sandbox_host_pool_capacity_cpu_millicores` | CPU capacity of ready hosts. |
| `langsmith_sandbox_host_pool_ready_hosts` | Ready hosts in the pool. |
| `langsmith_sandbox_host_pool_desired_replicas` | Replica target when autoscaling is active. |

Also monitor host pod readiness, `Pending` pods, node memory and disk pressure, storage latency, Redis memory and evictions, sandbox startup failures, and drain duration. A persistent gap between desired and ready hosts calls for checking node provisioning and host startup, not only workload demand.

### Check production readiness

Before running production workloads:

* Confirm the dedicated nodes expose KVM and match the host selector and tolerations.
* Reserve memory for guests, the host runtime, JuiceFS, and Kubernetes overhead.
* Align host limits, node limits, infrastructure quotas, and workspace quotas.
* Test scaling from the minimum pool size with a cold cache.
* Test one-host loss and a one-host-at-a-time upgrade under load.
* Verify application behavior when execution streams or service connections disconnect.
* Measure drain duration and set compatible pod and node shutdown timeouts.
* Confirm metadata Redis uses `noeviction` and has tested backups and restore procedures.
* Monitor object-store access, metadata capacity, and the gap between desired and ready hosts.

## See also

* [Sandbox architecture and lifecycle](Self-hosted%20Sandbox%20architecture.md)
* [Scale self-hosted Sandboxes](Scale%20self-hosted%20Sandboxes.md)
* [Enable Sandboxes](Enable%20Sandboxes%20on%20self-hosted%20LangSmith.md)
* [Upgrade self-hosted LangSmith](../../../Manage%20an%20instance/Upgrade%20an%20installation.md)
* [Plan platform disaster recovery](../../../Manage%20an%20instance/Disaster%20recovery%20for%20self-hosted%20LangSmith.md)

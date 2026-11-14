# Self-hosted Sandbox architecture

> Understand how self-hosted LangSmith Sandboxes use microVMs, Kubernetes hosts, and shared storage to run and resume workloads.

[LangSmith Sandboxes](../../../../../Deploy/Sandboxes/LangSmith%20Sandboxes.md) run code in isolated microVMs on a dedicated pool of Kubernetes nodes. This guide explains where the components run, how requests reach a sandbox, and which state survives a host restart.

For supported platforms, prerequisites, and installation instructions, see [Enable Sandboxes](Enable%20Sandboxes%20on%20self-hosted%20LangSmith.md). The architecture below describes the `sandbox-host` runtime. Storage mounting and configuration options can differ across Helm releases.

> [card] [Scaling and capacity](Scale%20self-hosted%20Sandboxes.md)
>
> Size the host pool, configure autoscaling, and plan memory and cache capacity.

> [card] [Upgrades and operations](Operate%20self-hosted%20Sandboxes.md)
>
> Understand host draining, failure recovery, and production monitoring.

## Understand the deployment model

A sandbox is a Firecracker microVM, not a Kubernetes pod. Each `sandbox-host` pod manages multiple microVMs, each with its own guest kernel. Kubernetes schedules the hosts; LangSmith places sandboxes onto them.

The host Deployment uses required pod anti-affinity to place at most one host pod on each node. Its node selector and tolerations target a dedicated, KVM-capable node pool. Adding a sandbox does not create another pod.

**architecture**

The platform backend manages sandbox placement and traffic. Hosts run microVMs; shared storage keeps persistent state independent of a node.

### Understand component failure impact

Each component has a different failure scope. Distinguish temporary unavailability from loss of its stored data when planning recovery.

| Component | Where it runs and what it holds | If unavailable or lost |
| - | - | - |
| `platform-backend` | Existing LangSmith node pool. Authenticates and authorizes requests, chooses hosts, and proxies traffic. Holds no durable sandbox state. | API unavailable Sandbox API and proxied traffic fail while the service is unavailable. Restarting it does not delete sandbox disks. |
| PostgreSQL | Existing LangSmith database. Holds sandbox records, the host registry, and placement. | API unavailable An outage blocks operations that need sandbox records or placement. Persistent data at risk Losing database contents requires restoring those records, not just restarting hosts. |
| `sandbox-host` | Dedicated sandbox node pool, one pod per node. Holds running microVMs and their memory. | One host affected Abrupt loss stops that host's sandboxes and loses running memory. Persistent disks remain on shared storage. |
| JuiceFS client | Host-owned mount inside each host pod. Connects the VMs to shared storage and manages a local cache. | One host affected Mount failure fences the host and stops its VMs. Restart requires working shared storage. |
| Kubernetes API | Kubernetes control plane. Holds host Leases and the host Deployment. | Pool-wide disruption Hosts that cannot renew Leases eventually fence themselves. A prolonged cluster-wide outage can stop the entire pool. |
| JuiceFS Redis | Dedicated metadata store. Holds the file tree, file sizes, and the mapping to data chunks. | Pool-wide disruption An outage stalls or fails filesystem operations across hosts. Persistent data at risk Lost metadata requires recovery from backup. Object storage alone cannot reconstruct the filesystem. |
| Object storage | Shared bucket or container. Holds data blocks for disk images, saved memory, and snapshots. | Pool-wide disruption An outage blocks uncached reads and uploads. New hosts may fail readiness. Persistent data at risk Deleted data blocks require recovery from backup for the affected disks and snapshots. |
| Node-local cache | Each sandbox node. Holds disposable copies of JuiceFS data blocks. | Cache rebuild only Persisted data remains on shared storage. Hosts fetch cached copies again, with slower I/O while the cache warms. |

For fencing, recovery behavior, and storage protection, see [Understand failure impact](Operate%20self-hosted%20Sandboxes.md#understand-failure-impact).

One elected host observes pool health and runs the [host autoscaler](Scale%20self-hosted%20Sandboxes.md#understand-the-two-scaling-layers). Other hosts continue serving sandboxes without holding leadership.

### Inspect one sandbox node

A host pod runs the sandbox daemon and Firecracker processes. In deployments with a host-owned JuiceFS mount, it also runs the JuiceFS client. The daemon connects to the agent inside each guest through `vsock`.

**node**

One Kubernetes pod contains multiple microVMs. The host needs KVM access; guest memory and node-local caches consume the node's resources.

The host uses host networking on port `19190`. The platform backend connects to the host's node address; clients use the LangSmith API or [service URLs](../../../../../Deploy/Sandboxes/Sandbox%20service%20URLs.md), not the host listener directly. Keep host listeners on private networks.

Host pods require privileged access for virtualization, networking, and mounts. Use dedicated nodes and restrict administrative access to them.

## Follow a request

Creating a sandbox passes through the platform backend before reaching a host. Subsequent command, file, and service requests follow the same authorization boundary.

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'fontFamily': 'TWK Lausanne, Inter', 'fontSize': '15px', 'lineColor': '#40668D', 'primaryColor': '#E5F4FF', 'primaryTextColor': '#030710', 'primaryBorderColor': '#006DDD', 'actorBkg': '#E5F4FF', 'actorBorder': '#006DDD', 'actorTextColor': '#030710', 'actorLineColor': '#40668D', 'signalColor': '#40668D', 'signalTextColor': '#030710'}, 'sequence': {'width': 130, 'actorMargin': 30, 'mirrorActors': false, 'wrap': true}}}%%
sequenceDiagram
    accTitle: Create and use a self-hosted sandbox
    accDescr: The client calls the platform backend, which records and places the sandbox. The selected host prepares its filesystem and boots a microVM. Later requests pass through the backend and host to the guest.
    participant C as Client
    participant P as Platform<br/>backend
    participant D as PostgreSQL
    participant H as Sandbox<br/>host
    participant V as MicroVM
    C->>P: Create sandbox
    P->>P: Authenticate<br/>and authorize
    P->>D: Record sandbox<br/>and assign host
    P->>H: Create
    H->>H: Prepare disk<br/>on JuiceFS
    H->>V: Warm restore<br/>or cold boot
    V->>H: Guest ready
    H->>P: Created
    P->>D: Mark ready
    P->>C: Ready
    C->>P: Execute / files /<br/>service URL
    P->>P: Authenticate<br/>and authorize
    P->>H: Authorized request
    H->>V: Forward to guest
    V->>H: Response
    H->>P: Response
    P->>C: Response
```

Placement considers committed CPU and prefers the sandbox's previous host when its load is close to the least-loaded candidate. Returning to that host can reuse cached data. It is a preference, not a guarantee that a sandbox stays on one node.

> [!NOTE]
>
> The utilization target controls scaling, not admission. A busy pool can still place work on an existing host. With no ready hosts, creation fails with `NoSandboxHostsAvailable` rather than waiting in a capacity queue. See [Plan for bursts](Scale%20self-hosted%20Sandboxes.md#plan-for-bursts).

## Track persistent state

JuiceFS separates a filesystem's metadata from its contents:

* **Redis metadata**: Directory entries, file sizes, and the mapping from files to data chunks.
* **Object storage**: Data chunks for disk images, saved memory images, and snapshots.
* **Local cache**: Copies of data blocks on individual nodes. A node replacement loses that cache, not the shared filesystem.

> [!WARNING]
>
> JuiceFS Redis is durable storage, not the LangSmith cache Redis. Object storage alone cannot reconstruct the filesystem without its metadata. Protect both stores, use `noeviction` for metadata Redis, and test recovery. See [Protect sandbox storage](Operate%20self-hosted%20Sandboxes.md#protect-sandbox-storage).

### Distinguish suspend from a crash

A persistent sandbox can resume on a different compatible host because its disk and successfully saved memory live on shared storage.

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'fontFamily': 'TWK Lausanne, Inter', 'fontSize': '15px', 'lineColor': '#40668D', 'primaryTextColor': '#030710', 'textColor': '#030710', 'edgeLabelBackground': '#F2FAFF'}, 'flowchart': {'nodeSpacing': 80, 'rankSpacing': 100, 'curve': 'linear'}}}%%
flowchart TB
    accTitle: Persistent sandbox lifecycle
    accDescr: Provisioning leads to running. A graceful stop saves memory and moves to stopped. A later start or wake restores on a compatible host. Host loss instead requires fencing and a cold boot from persisted disk, without the previous running memory.
    P[Provisioning] --> R[Running]
    R -->|Graceful stop| S[Stopped: memory saved]
    S -->|Start or wake| R
    R -->|Host loss| F[Wait for fencing]
    F -->|Cold boot from disk| R
    S -->|Delete| D[Deleted]
    R -->|Delete| D
    classDef process fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710
    classDef output fill:#EBD0F0,stroke:#885270,stroke-width:2px,color:#441E33
    classDef alert fill:#F8E8E6,stroke:#634643,stroke-width:2px,color:#634643
    classDef neutral fill:#F2FAFF,stroke:#40668D,stroke-width:1px,color:#2F4B68
    class P,R process
    class S output
    class F alert
    class D neutral
```

* **Graceful stop**: The host saves VM memory and stops the VM. A later start or wake request can restore running processes from that image.
* **Host loss**: Running memory is lost. Recovery waits for the fencing window before another host can start the sandbox from persisted disk.
* **Deletion**: Removes the sandbox rather than moving it to another host. A separately captured [snapshot](../../../../../Deploy/Sandboxes/Sandbox%20snapshots.md) has its own lifecycle.

Restoring memory requires a complete, compatible memory image. It is not live migration and does not preserve an open client connection. Unflushed writes and in-memory work can be lost after an abrupt failure. These persistence guarantees do not apply to ephemeral sandbox storage.

## See also

* [Enable Sandboxes](Enable%20Sandboxes%20on%20self-hosted%20LangSmith.md)
* [Scale self-hosted Sandboxes](Scale%20self-hosted%20Sandboxes.md)
* [Operate self-hosted Sandboxes](Operate%20self-hosted%20Sandboxes.md)
* [Sandbox permissions](../../../../../Deploy/Sandboxes/Sandbox%20access%20permissions.md)

# BYOC operations on Azure

> How LangChain scales, upgrades, and maintains a LangSmith BYOC data plane on Azure, including instance sizes, maintenance windows, and auditing.

LangChain operates your Azure data plane after provisioning, including upgrades, scaling, monitoring, and security patching. You do not need to size or tune each service. For BYOC on AWS, see [BYOC operations](../AWS/BYOC%20operations.md).

## Autoscaling

LangChain scales your data plane as load changes:

* **Stateless LangSmith services**: KEDA scales each service between its minimum and maximum replica counts. Most services target 70% CPU and 80% memory of their requested resources.
* **Cluster nodes**: AKS [node auto-provisioning](https://learn.microsoft.com/azure/aks/node-autoprovision) adds capacity for pods that cannot be scheduled and removes unused capacity. Each node pool has CPU and memory limits. The general pool is limited to 100 vCPUs and 400 GiB of memory. The system node pool stays at three nodes.
* **Storage**: PostgreSQL storage autogrow is enabled. Blob storage grows with usage, and lifecycle rules expire trace payloads according to their retention tier.
* **Databases**: LangChain monitors usage and can change PostgreSQL and Redis sizes, service replica counts, and node pool limits.

SmithDB uses dedicated node pools for compute and local NVMe cache storage. For storage configuration and retention, see [Data stores](BYOC%20architecture%20on%20Azure.md#data-stores) and [Data protection](BYOC%20architecture%20on%20Azure.md#data-protection).

## High availability

Data planes use zone-redundant PostgreSQL standby servers in regions that support them. Azure Managed Redis has a replica for high availability. Blob storage uses zone-redundant storage (ZRS) in regions with availability zones and locally redundant storage (LRS) elsewhere.

## Instance sizes

Data planes start with the following database and system node sizes. To request different sizes, contact the LangChain team.

| Resource | Default size |
| - | - |
| PostgreSQL (LangSmith) | PostgreSQL 18, `GP_Standard_D2ds_v4`, 32 GiB storage with autogrow |
| PostgreSQL (SmithDB metastore) | PostgreSQL 18, `GP_Standard_D2ds_v4`, 128 GiB storage with autogrow |
| Azure Managed Redis | `Balanced_B3`, high availability enabled, persistence disabled |
| AKS system node pool | Three `Standard_D2s_v6` nodes, fixed size |
| Application and SmithDB nodes | Node auto-provisioning, within each node pool's limits |

LangSmith services start with these resource requests and autoscaling bounds:

| Service | Minimum replicas | Maximum replicas | CPU request | Memory request |
| - | - | - | - | - |
| Backend | 2 | 20 | 1 | 4 GiB |
| Platform backend | 2 | 20 | 500m | 1 GiB |
| Ingest queue | 2 | 20 | 2 | 4 GiB |
| Queue | 1 | 10 | 1 | 4 GiB |
| Listener | 1 | 10 | 1 | 1500 MiB |
| Host backend | 1 | 10 | 500m | 1000 MiB |
| ACE backend | 1 | 10 | 1 | 2 GiB |
| Presidio | 1 | 10 | 250m | 2 GiB |

## LangSmith upgrades

LangChain manages LangSmith version upgrades. Services use horizontal pod autoscaling and pod disruption budgets to limit the impact of replacing pods. Availability during an update depends on the service's replica count and available cluster capacity.

## Supporting service upgrades

LangChain manages supporting services such as Istio and KEDA alongside the LangSmith workloads. Azure data planes store traces in SmithDB and do not run ClickHouse.

## Kubernetes cluster upgrades

AKS applies Kubernetes patch versions and node image updates automatically, within the data plane's maintenance window. The system node pool uses a surge node during upgrades so pods can move onto new capacity.

## Maintenance windows

Azure data planes have a weekly, four-hour maintenance window in UTC. The default is Sunday, 07:00–11:00 UTC (`sun:07:00-sun:11:00`). AKS upgrades and PostgreSQL maintenance use this window.

To change the window, use the API described in [Change data plane settings](BYOC%20onboarding%20on%20Azure.md#change-data-plane-settings). The maintenance-window settings form in the LangSmith UI supports AWS only.

## Observability

The data plane reads PostgreSQL and Redis metrics from Azure Monitor and reports health metrics to LangChain. You can configure LangSmith service logs, metrics, and traces as on self-hosted deployments. See [Export LangSmith telemetry to your observability backend](../../Self-hosted/Self-hosted%20observability/Export%20LangSmith%20telemetry%20to%20your%20observability%20backend.md).

You can deploy your own observability and security monitoring agents, as long as they do not interfere with LangSmith workloads.

## Troubleshooting

LangChain manages the resources in your data plane through delegated Microsoft Entra roles. Those management roles do not grant data roles on Blob storage, PostgreSQL, or Redis. For the full permission model, see [Access and permissions](BYOC%20architecture%20on%20Azure.md#access-and-permissions).

When troubleshooting requires data, you can run the query yourself, then validate and sanitize the output before sharing it with LangChain. If an engineer needs temporary access, the LangChain team coordinates the access with you.

## Auditing

* **LangSmith audit logs**: Data plane operations are recorded in the data plane, and control plane actions are recorded in the control plane. See [Audit logs](../../Govern/Auditing/Audit%20logs.md).
* **Azure Activity Log**: Records LangSmith calls to Azure Resource Manager in your subscription.
* **Resource and network logs**: LangSmith does not configure Azure diagnostic settings or VNet flow logs. AKS control plane and audit logs, Key Vault audit logs, PostgreSQL logs, and network flow logs are not collected by default. Configure diagnostic settings and flow logs to collect them.

You are responsible for reviewing those logs and configuring alerts.

## See also

* [BYOC architecture on Azure](BYOC%20architecture%20on%20Azure.md)
* [Azure data plane cost estimate](Azure%20data%20plane%20cost%20estimate.md)
* [Using BYOC](../BYOC%20usage.md)

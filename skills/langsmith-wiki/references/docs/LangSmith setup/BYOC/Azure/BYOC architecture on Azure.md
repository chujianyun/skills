# BYOC architecture on Azure

> What LangSmith BYOC deploys in your Azure subscription, how the data plane connects to the LangChain control plane, the access LangSmith gets, and how your data is protected.

BYOC on Azure runs the LangSmith data plane in a resource group in your Azure subscription, while LangChain runs the control plane in its own Azure environment in `centralus`. Your trace data stays in your subscription. This page describes what LangSmith deploys, how traffic flows, the access LangSmith gets, and how your data is protected. For BYOC on AWS, see [BYOC architecture](../AWS/BYOC%20architecture.md).

> [!NOTE]
>
> BYOC on Azure is in [beta](../../Cloud/Reference/Release%20stages.md). Resources and permissions can change between releases. The values on this page are the current defaults.

To set up a data plane, follow [BYOC onboarding on Azure](BYOC%20onboarding%20on%20Azure.md).

## Control plane and data plane

| Plane | Where it runs | What it holds |
| - | - | - |
| **Control plane** | LangChain's Azure environment, `centralus`, at [azure.smith.langchain.com](https://azure.smith.langchain.com) | Authentication, organization and workspace configuration, billing and usage metadata, LangSmith API keys, and the static frontend assets |
| **Data plane** | One resource group in your Azure subscription, in the region you choose | Traces, prompts, datasets, evaluators, experiments, annotation queues, agent deployments, workspace secrets, and other application data |

![BYOC architecture diagram for Azure. The LangSmith UI and the client apps in your application VNet reach the data plane over VNet peering or a VPN gateway, which terminates at an internal load balancer. The load balancer feeds an Istio ingress in an AKS cluster in your Azure subscription, which routes to the LangSmith services that run the backend and SmithDB, and those services read and write Blob Storage, Azure PostgreSQL, and Azure Managed Redis. The LangChain cloud control plane in centralus holds Crossplane, on-call engineers, alerting, and the LangSmith control plane services. Crossplane reaches the AKS API with Entra ID for scaling and upgrades, the data plane sends auth and telemetry back over Private Link, and the control plane uses Entra ID workload identity to provision resources in your subscription.](../../../../assets/images/6828987de646-byoc-architecture-azure.png)

The lifecycle of a data plane is:

1. You apply the LangSmith Terraform module, which creates a resource group and a Key Vault, and gives the LangSmith BYOC application two roles on the resource group.
2. You create the data plane with the LangSmith API. The control plane checks its access, and writes the data plane's bootstrap secret to your Key Vault.
3. The control plane creates the network, AKS cluster, databases, and storage in the resource group, then installs LangSmith on the cluster.
4. The data plane reports to the control plane, and its status becomes `active`.
5. LangChain upgrades, scales, and repairs the data plane until you delete it.

## What gets deployed

LangSmith creates all data plane resources in your resource group. AKS also creates a node resource group, `<name>-smith-aks-nodes`, and manages it.

### Network

LangSmith creates a VNet from the `vpc_cidr` range in the create request, and divides it into subnets. For a `/16` VNet:

| Subnet | Size | Use |
| - | - | - |
| AKS | `/20` | AKS nodes and pods. Outbound traffic goes through a NAT gateway with one static public IP address. |
| Private endpoints | `/24` | Shared private endpoints for PostgreSQL, Redis, Blob storage, Key Vault, and the LangSmith control plane. |

One network security group on the private endpoint subnet uses three application security groups to allow traffic from the AKS subnet only: TCP 5432 to PostgreSQL endpoints, TCP 10000 and 8500 to 8599 to Redis endpoints, and TCP 443 to Blob storage, Key Vault, and control plane endpoints.

The AKS subnet takes one sixteenth of the VNet, and the private endpoint subnet takes 1/256 of it. A `/18` VNet gives a `/22` AKS subnet and a `/26` private endpoint subnet. The Kubernetes service range comes from outside the VNet: `10.240.0.0/16`, or `192.168.0.0/16` if your VNet overlaps `10.240.0.0/16`.

Private DNS zones linked to the VNet resolve PostgreSQL, Redis, Key Vault, and Blob storage to their private endpoints.

### Compute

* **AKS**: Kubernetes 1.35 on the Standard tier. A private cluster with no public API endpoint. Local accounts and run command are disabled. Authentication uses Microsoft Entra ID with Azure RBAC for Kubernetes authorization. The OIDC issuer and workload identity are enabled.
* **Network plugin**: Azure CNI with Cilium for the data path and network policy.
* **System node pool**: Three `Standard_D2s_v6` nodes on Azure Linux, spread across the region's availability zones, reserved for critical add-ons.
* **Application nodes**: [Node auto-provisioning](https://learn.microsoft.com/azure/aks/node-autoprovision) adds and removes nodes as pods need them. It uses on-demand D, E, and F series VMs of version 5 or later. Each node pool has a CPU and memory limit. The general pool is limited to 100 vCPUs and 400 GiB of memory. SmithDB runs on its own pools, including a pool of VMs with local NVMe disks for its cache.
* **Upgrades**: AKS applies Kubernetes patch versions and node image updates automatically, in the data plane's [maintenance window](BYOC%20onboarding%20on%20Azure.md#change-data-plane-settings).

### Data stores

| Store | Configuration |
| - | - |
| **PostgreSQL** (LangSmith) | Azure Database for PostgreSQL flexible server, PostgreSQL 18, `GP_Standard_D2ds_v4`, 32 GiB storage with autogrow. Zone-redundant high availability in regions that support it. Backups kept 7 days, without geo-redundant backup. Microsoft Entra authentication only, no password authentication, no public access. |
| **PostgreSQL** (SmithDB metastore) | A second flexible server, PostgreSQL 18, `GP_Standard_D2ds_v4`, 128 GiB storage. Same availability, backup, and access settings. |
| **Azure Managed Redis** | `Balanced_B3` with high availability, OSS cluster policy, and no persistence. TLS only, access keys disabled, no public access. |
| **Blob storage** | Storage accounts for trace payloads and attachments, and for SmithDB data. StorageV2, Standard, ZRS in regions with availability zones and LRS in other regions. HTTPS only with TLS 1.2 or later. Shared key access and public network access are disabled. |
| **Key Vault** | The vault you create. The data plane reads its bootstrap secret through a private endpoint, and refreshes it every hour. |

Data planes store and query traces in [SmithDB](../../Self-hosted/SmithDB/Overview/Enable%20SmithDB%20on%20self-hosted%20LangSmith.md), with its data in Blob storage and its metadata in the SmithDB PostgreSQL server. They do not run ClickHouse.

### DNS and ingress

* **Hostname**: `<data_plane_id>.azure.langchain-byoc.com`. LangSmith creates a public DNS zone for the hostname in your resource group and delegates it from the parent zone that LangChain owns.
* **Load balancer**: An Azure Standard load balancer, public or internal, as set by `public_load_balancer` in the create request.
* **Private DNS**: For an internal load balancer, the hostname resolves through a private DNS zone linked to the data plane VNet. The public zone holds certificate validation records, not the internal endpoint address. Your users and applications need DNS resolution through the private zone.
* **Ingress**: An Istio ingress gateway. HTTP redirects to HTTPS, and the gateway rejects the `TRACE`, `TRACK`, and `CONNECT` methods.
* **TLS**: cert-manager gets a Let's Encrypt certificate for the hostname through a DNS-01 challenge.

### Identities

Data plane workloads use user-assigned managed identities in your resource group, through workload identity federation with the AKS OIDC issuer. No storage keys, database passwords, or client secrets exist. Each identity has only the roles its workload needs, such as a data role on one Blob container, the PostgreSQL database role, or `Key Vault Secrets User` on the vault.

## Connectivity

| Path | Network | Authentication |
| - | - | - |
| Control plane to Azure Resource Manager | HTTPS to the public Azure Resource Manager endpoint | A Microsoft Entra token of the LangSmith BYOC application in your tenant |
| Control plane to the AKS API | Private Link. A private endpoint in LangChain's control plane network connects to your cluster's API server. The AKS API has no public endpoint. | Microsoft Entra token and Azure RBAC |
| Data plane to control plane | Private Link. A private endpoint in the data plane's shared private endpoint subnet connects to the LangSmith control plane. Private DNS zones in your resource group resolve the LangSmith API and telemetry hostnames to it. | A data plane token |
| Your users and applications to the data plane | The public or internal load balancer | LangSmith API keys and sign-in through the control plane |

The data plane pulls LangSmith container images from LangChain's container registry through the NAT gateway.

The data plane sends operational data to the control plane, such as authentication requests, health metrics, and usage. As on AWS, the LangSmith UI loads static assets from the control plane and sends every request for application data to your data plane. See [Data traffic](../AWS/BYOC%20architecture.md#data-traffic).

## Access and permissions

LangChain manages your data plane through one multi-tenant Microsoft Entra application, **LangSmith BYOC**. You add its service principal to your tenant and give it roles on each data plane resource group. The application requests no Microsoft Graph permissions.

The control plane holds no stored credential for your tenant. It runs on AKS, and workload identity federation exchanges a pod token for a token of the LangSmith BYOC application in your tenant. Only the control plane services that provision and manage data planes can get that token.

### Role assignments

| Role | Scope | Why LangSmith needs it |
| - | - | - |
| `langsmith-byoc-<key>-<suffix>` (custom) | The data plane resource group | Create, update, and delete the data plane resources, write the bootstrap secret to the Key Vault, and approve the private endpoints to the AKS API and the data stores. The role names each action it allows. |
| Same custom role with `reduced_access = true` | The data plane resource group | Reduces the role actions in place once the data plane is active. Upgrades, scales, and repairs the data plane, but cannot delete it, its data stores, or its network, and cannot create role assignments. |
| `User Access Administrator` | The data plane resource group | Give roles to the data plane's managed identities, and create the custom Blob data roles. Terraform deletes this assignment when you set `reduced_access = true`. |
| `Azure Kubernetes Service RBAC Cluster Admin` | The data plane's AKS cluster | Install and upgrade LangSmith on the cluster. LangSmith creates this role assignment itself. |

The [Terraform module](https://github.com/langchain-ai/terraform/blob/main/modules/byoc/azure/langsmith-byoc-access/main.tf) creates one custom role per data plane, with the resource group as its only assignable scope. Both role assignments carry your organization's external ID as their description. LangSmith refuses to create a data plane when they do not match, which binds the resource group to your LangSmith organization.

### What LangChain can and cannot access

| Item | LangChain access |
| - | - |
| Resources in the data plane resource group | Create, change, and delete |
| Role assignments in the data plane resource group | Create and delete |
| The data plane's AKS cluster | Cluster admin |
| Other resource groups and resources in your subscription | None |
| The AKS node resource group | None. AKS manages it. |
| Your Microsoft Entra directory and Microsoft Graph | None |
| Data in Blob storage, PostgreSQL, and Redis | No data role. Until you set `reduced_access = true`, `User Access Administrator` can grant one. Your Activity Log records every role assignment. |
| Key Vault secret values | Write through Azure Resource Manager. No role to read secrets. |

To remove LangSmith's access, see [Remove LangSmith access](BYOC%20onboarding%20on%20Azure.md#remove-langsmith-access).

## Data protection

### Encryption

| Store | At rest | In transit |
| - | - | - |
| Blob storage | Microsoft-managed keys | HTTPS only, TLS 1.2 or later |
| PostgreSQL | Microsoft-managed keys | TLS, with Microsoft Entra authentication |
| Redis | Microsoft-managed keys | TLS only |
| Key Vault | Microsoft-managed keys | TLS, through a private endpoint |
| AKS disks | Microsoft-managed keys | Traffic stays in the cluster |

### Retention

* **Trace payloads**: Blob lifecycle rules delete each object when its retention tier ends. The defaults are 14 days for short-lived traces and 400 days for long-lived traces. You can change both with the `ttl` setting. See [Change data plane settings](BYOC%20onboarding%20on%20Azure.md#change-data-plane-settings).
* **Blob versions**: Versioning is enabled, and previous versions are deleted 7 days after they are created. Deleted containers can be restored for 7 days. Blob soft delete is disabled, so expired traces do not outlive their retention tier.
* **PostgreSQL**: Automated backups are kept for 7 days in the same region.
* **Redis**: No persistence and no backups. Redis holds only short-lived data.

### Deletion

When you delete a data plane, LangSmith deletes the AKS cluster, PostgreSQL, Redis, and the network resources. It keeps your resource group, your Key Vault, and the Blob storage accounts that hold trace and SmithDB data. For details, see [Delete a data plane](BYOC%20onboarding%20on%20Azure.md#delete-a-data-plane).

## Scaling and operations

LangChain operates your Azure data plane after provisioning. See [BYOC operations on Azure](BYOC%20operations%20on%20Azure.md) for autoscaling, default instance sizes, upgrades, and maintenance windows. For estimated infrastructure costs, see [Azure data plane cost estimate](Azure%20data%20plane%20cost%20estimate.md).

### Logs

Your Azure Activity Log records LangSmith calls to Azure Resource Manager. To collect resource and network logs, configure diagnostic settings and VNet flow logs in your subscription. See [Auditing](BYOC%20operations%20on%20Azure.md#auditing) for the logs available and your responsibilities.

## See also

* [BYOC overview](../Bring%20Your%20Own%20Cloud%20%28BYOC%29.md)
* [BYOC onboarding on Azure](BYOC%20onboarding%20on%20Azure.md)
* [BYOC shared responsibility model](../BYOC%20shared%20responsibility%20model.md)

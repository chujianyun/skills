# Azure data plane cost estimate

> Rough Azure infrastructure cost of a LangSmith BYOC data plane running SmithDB, with example node counts, sandboxes excluded, and additional charges.

> [!WARNING]
>
> These are estimates, not a quote. Azure changes its prices without notice. Your bill depends on region, usage, and discounts. The subtotal below excludes node disks, networking, object storage, and other usage charges. It is not a complete monthly bill.

This is a rough monthly infrastructure cost for a [LangSmith BYOC data plane on Azure](BYOC%20architecture%20on%20Azure.md). Azure data planes run SmithDB, not ClickHouse.

The estimate uses USD pay-as-you-go prices for `eastus`, Linux VMs, and 730 hours per month. The database and system node sizes match the [default profile](BYOC%20operations%20on%20Azure.md#instance-sizes). Application and SmithDB node counts are assumptions, not fixed deployment sizes. AKS node auto-provisioning selects VM sizes and counts within each pool's limits.

## Rough monthly estimate

This example budget assumes two to six application nodes, one SmithDB cache node, and one SmithDB compute node. Each compute row covers a separate set of VMs. SmithDB compute is not included in the application node estimate.

> [!NOTE]
>
> Sandboxes are excluded from the baseline, including their host compute, storage, and private endpoint. The estimate does not imply that sandboxes are disabled by default or that a self-service opt-out is available.

| Area | Rough monthly estimate | Notes |
| - | - | - |
| AKS control plane | \~\$73 | Standard tier at \$0.10/hour. |
| System node pool | \~\$221 | 3 `Standard_D2s_v6` nodes at \$0.101/hour each. Node disks are additional. |
| Application worker nodes | \$589–\$1,765 | Assumes 2 to 6 `Standard_D8s_v6` nodes at \$0.403/hour each for LangSmith pods. |
| SmithDB cache nodes | \~\$1,455 | Assumes 1 `Standard_D32ds_v6` at \$1.993/hour for query, ingestion, and compaction workers. Local NVMe is included in the VM price. |
| SmithDB compute nodes | \~\$294 | Assumes 1 `Standard_D8s_v6` at \$0.403/hour for compaction scheduling and the cluster manager. |
| PostgreSQL, LangSmith | \~\$267 | PostgreSQL 18, `GP_Standard_D2ds_v4`, 32 GiB storage, with a zone-redundant standby where supported. Includes primary and standby compute and storage. |
| PostgreSQL, SmithDB metastore | \~\$289 | PostgreSQL 18, `GP_Standard_D2ds_v4`, 128 GiB storage, with a zone-redundant standby where supported. Includes primary and standby compute and storage. |
| Azure Managed Redis | \~\$95 | `Balanced_B3`, high availability enabled. Two nodes at \$0.065/hour each. |
| Node disks | Additional, not included | Managed OS disks where nodes do not use ephemeral OS disks. SmithDB caches use local NVMe, not separately billed managed cache disks. |
| Networking | Additional, not included | NAT gateway, load balancers, private endpoints, public IP addresses, data processing, and data transfer. |
| Blob storage, Key Vault, DNS, and monitoring | Additional, not included | Storage capacity, operations, retention, and any diagnostic logs you enable. |

Estimated monthly subtotal for priced items, excluding sandboxes: **\$3,283–\$4,460**. Add the additional charges above, taxes, and LangSmith fees to estimate the full bill.

The system-node reduction from three `Standard_D4s_v6` to three `Standard_D2s_v6` saves about \$221 per month in VM compute. The older D8s\_v5-only SmithDB estimate does not represent the dedicated NVMe pool. Smaller system nodes alone do not establish a lower total bill.

The PostgreSQL estimates use \$0.089 per vCore-hour and \$0.115 per GiB-month of provisioned storage. Each server has two vCores and a matching standby. Storage growth and backup storage beyond the included allowance cost extra.

The SmithDB cache example has 32 vCPUs and 128 GiB of memory. Azure-specific pod requests are 4 vCPUs and 8 GiB for query, 4 vCPUs and 8 GiB for ingestion, and 8 vCPUs and 16 GiB per compaction worker. Their cache requests are 200 GiB, 100 GiB, and 100 GiB per worker, respectively. These run on the dedicated local NVMe pool, separate from the compaction scheduler and cluster manager. Replica counts, scheduling overhead, upgrades, and load can require more nodes. This example does not guarantee a throughput level or a highly available SmithDB node layout.

For networking, the NAT gateway alone costs about \$33 per month before data processing. Without sandboxes and with control-plane private access enabled, seven explicit customer-side private endpoints cost about \$51 per month: two PostgreSQL, two Blob storage, Redis, Key Vault, and control-plane access. The AKS management private endpoint runs in LangChain's subscription and is not part of your bill. A Standard load balancer's first five rules cost about \$18.25 per month. These charges are not included in the subtotal. Add the resources and traffic for your deployment in the Azure pricing calculator.

## Sandbox add-on

If your deployment includes sandboxes, budget separately for their dedicated host nodes, Blob storage, and private endpoint. One illustrative `Standard_D16ds_v6` host costs about **\$728 per month** at \$0.997/hour. Its private endpoint adds \$7.30 per month, plus sandbox storage and traffic charges. Additional hosts increase the compute cost.

## See also

* [Azure retail prices API](https://prices.azure.com/api/retail/prices)
* [Azure pricing calculator](https://azure.microsoft.com/en-us/pricing/calculator/)
* [Azure NAT Gateway pricing](https://azure.microsoft.com/en-us/pricing/details/azure-nat-gateway/)
* [Azure Managed Redis pricing](https://azure.microsoft.com/en-us/pricing/details/managed-redis/)
* [Azure Database for PostgreSQL pricing](https://azure.microsoft.com/en-us/pricing/details/postgresql/flexible-server/)
* [BYOC operations on Azure](BYOC%20operations%20on%20Azure.md)
* [Configure SmithDB for scale](../../Self-hosted/SmithDB/Install%20SmithDB/Configure%20SmithDB%20for%20scale.md)

# Azure Terraform variables reference

> Reference of the main Terraform variables for LangSmith self-hosted on Azure AKS.

Reference for the input variables you set in the [Azure Terraform module](https://github.com/langchain-ai/terraform/tree/main/modules/azure). Use it while filling in `terraform.tfvars` for the first time or tuning an existing deployment. For naming overrides and other advanced inputs not listed here, refer to [`infra/variables.tf`](https://github.com/langchain-ai/terraform/blob/main/modules/azure/infra/variables.tf).

Variables come in two categories:

* **Non-sensitive** (region, sizing, feature flags): set in `infra/terraform.tfvars`.
* **Sensitive** (license key, PostgreSQL password): set with `make setup-env`, which writes them to `infra/secrets.auto.tfvars` (gitignored, auto-loaded by Terraform). The application secrets are not Terraform variables. `make seed-secrets` writes them to Azure Key Vault, as the sensitive variables section at the end of this page describes.

For the end-to-end install, refer to the [deploy guide](Deploy%20LangSmith%20on%20Azure%20with%20Terraform.md). For how the modules fit together, refer to the [architecture reference](Azure%20Terraform%20architecture.md).

## Core

| Variable | Default | Required | Description |
| - | - | - | - |
| `subscription_id` | none | yes | Azure subscription ID (GUID) for the deployment. Get it with `az account show --query id -o tsv`. |
| `location` | `eastus` | no | Azure region for the deployment. |
| `azure_environment` | `public` | no | Azure cloud: `public` (commercial Azure) or `usgovernment` (Azure Government). Sets the provider environment and the DNS and Blob endpoint names that differ between the two clouds. Overrides `ARM_ENVIRONMENT`. Azure Government does not offer Azure Managed Redis, so `usgovernment` requires `redis_source = "in-cluster"`. |
| `name_prefix` | `""` | no | Name of this deployment, appended to every resource name and used as the default `environment` tag. Write it without a hyphen: `prod` gives `langsmith-rg-prod`, or `ls-rg-prod` with `unique_resource_names = true`. Lowercase letters and digits, separated by single hyphens. Empty means no suffix. |
| `unique_resource_names` | `false` | no | Use the collision-resistant naming scheme (`ls-` base plus a per-subscription hash on globally unique names). Every `terraform.tfvars` template sets `true`. Leave it `false` on an existing deployment: turning it on renames every resource, which destroys and recreates PostgreSQL and Storage and loses their data. |
| `name_suffix_salt` | `""` | no | Rotation counter mixed into the hash on the globally unique PostgreSQL, Redis, Storage, and Key Vault names. Bump it (`"2"`, then `"3"`) when an earlier deployment still holds those names, for example a soft-deleted Key Vault. No effect when `unique_resource_names = false`. Changing it on an existing deployment renames all four, which destroys and recreates PostgreSQL and Storage and loses their data. |
| `create_resource_group` | `true` | no | Create the resource group. Set `false` to deploy into an existing group named by `existing_resource_group_name`, so the deployer needs rights on that group only. Terraform leaves the group's tags, locks, and policy assignments unchanged, and `terraform destroy` leaves the group in place. |
| `existing_resource_group_name` | `""` | when `!create_resource_group` | Name of the existing resource group to deploy into. |
| `environment` | `""` | no | Value of the `environment` tag on all resources. Empty uses `name_prefix`. Set it only when the tag needs to differ from the deployment name. |
| `owner` | `""` | no | Email or team name of the resource owner. Applied as a tag. |
| `cost_center` | `""` | no | Cost center or billing code. Applied as a tag. |

`name_prefix` replaces `identifier`. A `terraform.tfvars` that still sets `identifier` fails the plan. Rename the variable and drop the leading hyphen: `identifier = "-prod"` becomes `name_prefix = "prod"`. Resource names do not change.

## Networking

| Variable | Default | Required | Description |
| - | - | - | - |
| `create_vnet` | `true` | no | Create a new VNet. Set `false` to bring your own VNet. |
| `vnet_address_space` | `["10.0.0.0/17"]` | no | Address space of the VNet Terraform creates. Ignored when `create_vnet = false`. Pick a range that does not overlap any network you peer with or reach over ExpressRoute or VPN. Plan rejects a subnet prefix outside this space, so move the subnet prefixes with it. |
| `vnet_id` | `""` | when `!create_vnet` | Existing VNet resource ID. Any subnet Terraform creates goes in this VNet's resource group. |
| `aks_subnet_id` | `""` | when `!create_cluster` | Existing subnet ID for the AKS cluster. Empty creates the subnet in `vnet_id`. An existing subnet must carry the `Microsoft.Storage` and `Microsoft.KeyVault` service endpoints, which plan checks. Set `manage_byo_subnet_service_endpoints = true` to have Terraform add them. With `keyvault_private_endpoint_enabled = true`, only `Microsoft.Storage` is required. |
| `postgres_subnet_id` | `""` | no | Existing subnet ID for the PostgreSQL server. Empty creates the subnet in `vnet_id`. An existing subnet must be delegated to `Microsoft.DBforPostgreSQL/flexibleServers` and hold no other resources. |
| `redis_subnet_id` | `""` | no | Existing subnet ID for the Redis private endpoint. Empty creates the subnet in `vnet_id`. The subnet must not be delegated. |
| `agic_subnet_id` | `""` | when `agic` and `!create_vnet` | Existing subnet ID for the Application Gateway. Terraform does not create this subnet in a VNet it does not own. The subnet must be dedicated and delegated to `Microsoft.Network/applicationGateways`. |
| `bastion_subnet_id` | `""` | when `create_bastion` and `!create_vnet` | Existing subnet ID for Azure Bastion. Azure requires the name `AzureBastionSubnet` and a `/26` or larger range. |
| `postgres_subnet_address_prefix` | `["10.0.32.0/20"]` | no | CIDR prefix for the PostgreSQL subnet. Can be disjoint ranges. With `create_vnet = false`, it must fall inside your VNet's address space. |
| `redis_subnet_address_prefix` | `["10.0.48.0/20"]` | no | CIDR prefix for the Redis subnet. Can be disjoint ranges. With `create_vnet = false`, it must fall inside your VNet's address space. |
| `aks_authorized_ip_ranges` | `[]` | no | External CIDRs permitted to reach the AKS API server. Empty leaves the API server publicly reachable from any apply host. Populate with operator and CI egress CIDRs for production. Cannot be combined with `aks_private_cluster_enabled`. |
| `aks_outbound_type` | `loadBalancer` | no | How nodes reach the internet. `loadBalancer` uses an outbound public IP on the AKS-managed load balancer. `userDefinedRouting` sends egress by the route table on `aks_subnet_id` to a firewall, network virtual appliance, or on-premises network; a `0.0.0.0/0` route must have next hop `VirtualAppliance` or `VirtualNetworkGateway`. `userAssignedNATGateway` sends egress through the NAT gateway on `aks_subnet_id`. Both custom types require `create_vnet = false`, a supplied `aks_subnet_id`, and a cluster Terraform creates. Plan checks the subnet. |
| `aks_nat_gateway` | `none` | when `userAssignedNATGateway` | NAT gateway on `aks_subnet_id`: `none`, `existing` (plan checks that one is attached), or `create` (Terraform creates a Standard NAT gateway and public IP and associates them with the subnet). Requires `aks_outbound_type` set to `userAssignedNATGateway` or `userDefinedRouting`. The `aks_nat_gateway_public_ip` output gives the created IP. |
| `aks_nat_gateway_idle_timeout_minutes` | `4` | no | TCP idle timeout of the NAT gateway that `aks_nat_gateway = "create"` makes, 4 to 120 minutes. |
| `aks_allow_outbound_type_change` | `false` | no | Allow a change to `aks_outbound_type` on an existing cluster. The change moves the cluster's egress IP and drops existing connections, so update firewall rules and `aks_authorized_ip_ranges` that name the old IP. |

## AKS

| Variable | Default | Required | Description |
| - | - | - | - |
| `create_cluster` | `true` | no | Create a new AKS cluster. Set `false` to attach to an existing cluster, which also requires `create_vnet = false` and `aks_subnet_id`. `istio-addon` ingress requires `true`. |
| `existing_cluster_name` | `""` | when `!create_cluster` | Name of the existing AKS cluster to attach to. |
| `existing_cluster_resource_group_name` | `""` | when `!create_cluster` | Resource group that holds the existing AKS cluster. |
| `aks_kube_auth` | `auto` | no | How Terraform's Kubernetes and Helm providers sign in to the cluster: `auto`, `entra`, or `certificate`. `auto` uses Microsoft Entra ID through kubelogin when the cluster has Entra ID integration, and the client certificate otherwise. Entra sign-in needs kubelogin on the `PATH` and an `az login` with cluster-admin rights. |
| `aks_private_cluster_enabled` | `false` | no | Give the API server a private endpoint in the cluster VNet and no public address. The apply host then needs a network path to that endpoint (a jump host, a VPN, or a runner in a peered VNet) and DNS that resolves the private zone. Cannot be combined with `aks_authorized_ip_ranges`. Set before the first apply: plan refuses a change on an existing cluster. |
| `aks_private_dns_zone_id` | `""` | no | Private DNS zone for a private API server. Empty or `System`: AKS creates the zone in the node resource group. `None`: AKS creates no private zone, and the module turns on the public FQDN, which Azure requires with `None`. The API server name then resolves through public DNS to its private IP, so node and operator DNS must resolve public names. v0.17.0 does not turn on the public FQDN; a later `v0.17.*` tag adds it. A zone resource ID: AKS registers the API server in that zone, which requires `aks_control_plane_identity = "user"`. Requires `aks_private_cluster_enabled = true`. Set before the first apply. |
| `aks_entra_only` | `false` | no | Entra ID integration with Azure RBAC for Kubernetes authorization, and local accounts disabled. Terraform's providers then sign in through kubelogin as the `az` identity, which needs cluster-admin through `aks_entra_admin_group_object_ids` or the Azure Kubernetes Service RBAC Cluster Admin role. Cannot be combined with `aks_kube_auth = "certificate"`. Azure cannot turn Entra integration off, so plan refuses `false` on a cluster that has it. To turn it on for an existing cluster, apply that change alone: a Helm or Kubernetes change in the same apply fails with a 401. |
| `aks_entra_admin_group_object_ids` | `[]` | no | Object IDs of Entra groups granted cluster-admin. Requires `aks_entra_only = true`. |
| `aks_control_plane_identity` | `system` | no | Identity the control plane runs as. `system`: a system-assigned identity, which exists only once the cluster does. `user`: a user-assigned identity, either `aks_control_plane_identity_id` or `<cluster_name>-control-plane`, which Terraform creates in the deployment resource group. Set before the first apply: plan refuses a change on an existing cluster. |
| `aks_control_plane_identity_id` | `""` | when grants are not managed | Resource ID of an existing user-assigned identity for the control plane. Requires `aks_control_plane_identity = "user"`. Required when `aks_control_plane_identity_manage_grants` resolves to `false`. Set before the first apply. |
| `aks_control_plane_identity_manage_grants` | `null` | no | Whether Terraform grants the user-assigned identity Network Contributor on the AKS subnet and, with a zone ID in `aks_private_dns_zone_id`, Network Contributor on the VNet and Private DNS Zone Contributor on the zone. `null` follows `create_vnet`. With `false`, plan checks the grants and prints the `az role assignment create` command for each missing one. Requires `aks_control_plane_identity = "user"`. See [PERMISSIONS.md](https://github.com/langchain-ai/terraform/blob/main/modules/azure/PERMISSIONS.md#control-plane-identity-grants). |
| `install_cert_manager` | `true` | no | Install cert-manager. Set `false` when an existing cluster already runs it, because Helm does not adopt a release it does not own. `tls_certificate_source = "dns01"` requires `true`. |
| `install_keda` | `true` | no | Install KEDA, which scales the LangSmith queue workers on Redis queue depth. Set `false` when an existing cluster already runs it. |
| `aks_sku_tier` | `Standard` | no | AKS control plane tier: `Free` (no SLA), `Standard` (uptime SLA), or `Premium` (allows long-term Kubernetes version support through `aks_support_plan = "AKSLongTermSupport"`). Updates in place. |
| `aks_kubernetes_version` | `1.35` | no | Kubernetes version for the AKS cluster. Use a version that has `KubernetesOfficial` support in your region, because Azure moves older minor versions to LTS-only. |
| `aks_network_mode` | `node-subnet` | no | Azure CNI IP address mode: `overlay` or `node-subnet`. Every `terraform.tfvars` template sets `overlay`, Microsoft's recommendation, where pods take addresses from `aks_pod_cidr` and the AKS subnet holds nodes only. The default keeps existing clusters unchanged. Fixed at cluster creation. |
| `aks_pod_cidr` | `10.244.0.0/16` | no | Pod address range in `overlay` mode; ignored in `node-subnet` mode. Must not overlap the VNet, peered or on-premises networks, or `aks_service_cidr`. Each node takes a `/24`, so a `/16` carries 256 nodes. |
| `aks_os_sku` | `Ubuntu` | no | Node OS image for the default pool and for additional pools that do not set `os_sku`: `Ubuntu`, `AzureLinux`, `AzureLinux3`, or `Ubuntu2204`. A change reimages the pool's nodes in place. |
| `default_node_pool_vm_size` | `Standard_D8s_v5` | no | VM size for the default node pool. `Standard_D8s_v5` (8 vCPU / 32 GiB) is the recommended baseline for the core platform with external Postgres and Redis. Use `Standard_D4s_v5` (4 vCPU / 16 GiB) only for light or demo deployments with in-cluster databases. |
| `default_node_pool_min_count` | `1` | no | Minimum node count for the default pool. Set to 3 for production (the core platform needs about 14.4 vCPU, which three `Standard_D8s_v5` nodes cover). Set to 1 for minimum or dev deployments. |
| `default_node_pool_max_count` | `10` | no | Maximum node count for the default pool. Core platform uses 4 to 6 nodes; add headroom as you enable add-ons (Agent Server hosting \~6, Fleet \~8, Insights 10 to 12). Raising this takes effect immediately with no node restarts. |
| `default_node_pool_max_pods` | `60` | no | Maximum pods per node in the default pool. The Azure CNI default of 30 is too low for LangSmith; 60 fits a full deployment on a single node. Immutable: changing it recreates the node pool. |
| `additional_node_pools` | `large: Standard_D16s_v5, 0 to 2` | no | Additional node pools. The default `large` pool (`Standard_D16s_v5`, 16 vCPU / 64 GiB) is required for in-cluster ClickHouse (requests up to 4 vCPU / 16 GiB, depending on `sizing_profile`) and Agent Server pods. `min_count = 0` scales it to zero when idle. Raise `max_count` to 3 or more for Fleet with multiple simultaneous deployments. A pool without `os_sku` uses `aks_os_sku`. |
| `aks_service_cidr` | `""` | when `!create_vnet` | Kubernetes service CIDR. Empty uses `10.0.64.0/20` when Terraform creates the VNet. Must not overlap the VNet or anything connected to it. Size it `/20`. Fixed at cluster creation. |
| `aks_dns_service_ip` | `""` | no | CoreDNS service IP. Must be within `aks_service_cidr`. Empty uses the eleventh address of `aks_service_cidr` (`10.0.64.10` for the default range). |
| `availability_zones` | `[]` | no | Availability zones for the AKS node pool and the PostgreSQL server. Empty lets Azure place them, the only setting that works when a SKU is not offered in every zone of the region. Use `["1", "2", "3"]` for zone-redundant HA. Applies at creation only. |

The private API server, Entra, and control-plane identity variables apply only to a cluster Terraform creates. On an attached cluster (`create_cluster = false`), Terraform makes no control-plane grants, and `aks_kube_auth = "auto"` detects Entra ID on the cluster itself.

## Data sources

| Variable | Default | Required | Description |
| - | - | - | - |
| `postgres_source` | `external` | no | `external` provisions Azure Database for PostgreSQL Flexible Server (private VNet). `in-cluster` uses the chart-managed Postgres pod (dev/demo only). |
| `redis_source` | `external` | no | `external` provisions Azure Managed Redis (private VNet). `in-cluster` uses the chart-managed Redis pod (dev/demo only). |
| `clickhouse_source` | `in-cluster` | no | `in-cluster` (dev/POC only) or `external` for [LangChain Managed ClickHouse](../../Connect%20external%20services/LangSmith-managed%20ClickHouse.md), recommended for production. |

## PostgreSQL

| Variable | Default | Required | Description |
| - | - | - | - |
| `postgres_admin_username` | `langsmith` | no | PostgreSQL administrator username. |
| `postgres_admin_password` | `""` | when external | PostgreSQL administrator password. Set via `make setup-env`. |
| `postgres_database_name` | `langsmith` | no | Name of the LangSmith database. With `postgres_source = "external"`, Terraform creates it on the Flexible Server. With `in-cluster`, it has no effect. |
| `postgres_version` | `16` | no | Major PostgreSQL version, 11 through 18. LangSmith requires 14 or later. Raising it on an existing server runs an irreversible in-place major upgrade. Lowering it destroys and recreates the server. |
| `postgres_sku_name` | `GP_Standard_D2ds_v4` | no | SKU for the PostgreSQL Flexible Server. A `LocationIsOfferRestricted` error or a zero vCPU quota can be scoped to one SKU family, so another family can clear it without a region change. |
| `postgres_high_availability` | `false` | no | Zone-redundant HA for PostgreSQL (primary and standby in different zones). Requires a General Purpose or Memory Optimized SKU. |
| `postgres_geo_redundant_backup` | `false` | no | Enable geo-redundant backups for PostgreSQL. |
| `postgres_standby_availability_zone` | `""` | no | Pin the HA standby to a zone. Empty lets Azure choose. Setting a zone also turns HA on. Pin the standby only alongside a pinned `availability_zones`. |
| `postgres_private_dns_zone_id` | `""` | no | Existing `privatelink.postgres` private DNS zone for the PostgreSQL servers, including the SmithDB metastore. Empty creates a zone in the deployment resource group and links it to the VNet. With a zone supplied, Terraform creates no zone and no VNet link, and the zone's owner links it. A zone in another subscription needs the `Microsoft.DBforPostgreSQL` resource provider registered there. Requires `postgres_source = "external"` or `enable_smithdb = true`. |

## Redis

| Variable | Default | Required | Description |
| - | - | - | - |
| `amr_sku` | `Balanced_B1` | no | Azure Managed Redis SKU. `Balanced_B1` is 1 GB. `Balanced_B0` sits on the most capacity-constrained pool and does not support HA. Move up (`Balanced_B3`, `Balanced_B5`, and so on) for more memory. A larger SKU does not fix `InsufficientCapacity`, which is regional; use `redis_location` instead. Replaces the classic `redis_capacity`. |
| `redis_high_availability` | `false` | no | Zone-redundant HA for Azure Managed Redis. Required for the Azure Managed Redis SLA, so set `true` for production. Not supported on `Balanced_B0`. |
| `redis_location` | `null` | no | Region for the Redis cluster. `null` uses `location`. Set it only when Azure Managed Redis reports `InsufficientCapacity` in your region. The private endpoint stays in `location`. |

## Blob storage

| Variable | Default | Required | Description |
| - | - | - | - |
| `blob_ttl_enabled` | `true` | no | Enable lifecycle TTL rules on the blob container. |
| `blob_ttl_short_days` | `14` | no | TTL in days for short-lived trace blobs. |
| `blob_ttl_long_days` | `400` | no | TTL in days for long-lived trace blobs. |
| `storage_replication_type` | `LRS` | no | Redundancy of the trace blob account: `LRS`, `GRS`, `RAGRS`, `ZRS`, `GZRS`, or `RAGZRS`. Use `ZRS` for zone-redundant deployments. A change between the zone-redundant and non-zonal groups needs an Azure account conversion first. Refer to the README [Storage redundancy](https://github.com/langchain-ai/terraform/blob/main/modules/azure/README.md#storage-redundancy) section. |
| `storage_allowed_ips` | `[]` | no | Public IPs or CIDRs allowed through the storage account default-deny firewall. AKS pod traffic is allowlisted automatically via the `Microsoft.Storage` service endpoint. Add only external clients (operator workstations, CI runners) that need the blob data plane. |
| `storage_private_endpoint_enabled` | `false` | no | Reach Blob Storage over Private Endpoints and turn off the public endpoint. Applies to the trace blob account and the SmithDB object store. `false` keeps the service endpoint firewall. |
| `storage_private_endpoint_subnet_id` | `""` | no | Subnet for the blob Private Endpoints. Empty uses the AKS subnet. |
| `storage_private_dns_zone_id` | `""` | no | Existing `privatelink.blob` private DNS zone to attach the endpoints to. Empty creates a zone and links it to the VNet. Supply the central zone when the VNet already resolves that name. |

## Key Vault

| Variable | Default | Required | Description |
| - | - | - | - |
| `create_keyvault` | `true` | no | Create a new Key Vault. Set `false` to attach to an existing vault. Terraform then writes its secrets into that vault and ignores `keyvault_default_action`, `keyvault_allowed_ips`, and `keyvault_purge_protection`. By default, Terraform does not grant itself access to an existing vault, so while `keyvault_manage_secrets = true`, grant the deployer Key Vault Secrets Officer on the vault before `make apply`, or the secret writes fail with 403. |
| `existing_keyvault_name` | `""` | when `!create_keyvault` | Name of the existing Key Vault to attach to. |
| `existing_keyvault_resource_group_name` | `""` | when `!create_keyvault` | Resource group that holds the existing Key Vault. |
| `keyvault_name` | `""` | no | Key Vault name. Must be globally unique, 3 to 24 characters. Empty derives the name from the naming scheme. Used only when `create_keyvault = true`. |
| `keyvault_purge_protection` | `true` | no | Enable purge protection. Set `false` for dev/test to allow immediate name reuse after destroy. |
| `keyvault_default_action` | `Allow` | no | Default action for the Key Vault data-plane firewall. `Allow` keeps `make apply` and `make seed-secrets` working, because both write secrets through the data plane. Production sets `Deny` and populates `keyvault_allowed_ips`. |
| `keyvault_manage_secrets` | `true` | no | Terraform writes `postgres-admin-password` and `langsmith-license-key` into the vault. `false` writes neither, so `make apply` needs no Key Vault data-plane access, and `make seed-secrets` writes all nine secrets afterward. Set `false` when the deployer cannot hold Key Vault Secrets Officer or when `keyvault_default_action = "Deny"` blocks the apply host. Changing it to `false` after an apply deletes both secrets from the vault, so remove them from state first. |
| `keyvault_manage_terraform_admin_assignment` | `null` | no | Whether Terraform creates the deployer's Key Vault Secrets Officer grant on the vault. `null` follows `create_keyvault`: a vault Terraform creates gets the grant, and an existing vault does not. Set `false` when the grant already exists, or when an ABAC condition on `principalType` rejects the request. A tenant admin must then grant the role before apply, or the secret writes fail with 403. |
| `terraform_principal_type` | `null` | no | Principal type of the identity running `terraform apply`, set on its Key Vault Secrets Officer grant: `User`, `Group`, or `ServicePrincipal`. `null` lets Azure infer it. Set it when the subscription delegates role assignment writes through an ABAC condition on `principalType`, which rejects requests that omit the field: `User` for an interactive `az login`, `ServicePrincipal` for CI. |
| `keyvault_allowed_ips` | `[]` | no | Public IPs or CIDRs allowed through the Key Vault firewall when `keyvault_default_action = "Deny"`. The AKS subnet is allowlisted automatically via the `Microsoft.KeyVault` service endpoint. Cannot be combined with `keyvault_private_endpoint_enabled`. |
| `keyvault_private_endpoint_enabled` | `false` | no | Reach the vault over a Private Endpoint and turn off its public network access. Plan, apply, `make seed-secrets`, and `make k8s-secrets` all read or write the vault, so run them from a machine that resolves the vault's `privatelink.vaultcore` record, such as a jump host or runner in the VNet or a peered network. `keyvault_manage_secrets = false` lets plan and apply run from outside. Requires `create_keyvault = true`. |
| `keyvault_private_endpoint_subnet_id` | `""` | no | Subnet for the vault's Private Endpoint. Empty uses `storage_private_endpoint_subnet_id`, which itself defaults to the AKS subnet. |
| `keyvault_private_dns_zone_id` | `""` | no | Existing `privatelink.vaultcore` private DNS zone for the endpoint. Empty creates a zone and links it to the VNet. With a zone supplied, Terraform creates no zone and no VNet link, and the deployer needs `Microsoft.Network/privateDnsZones/join/action` on the zone. See [PERMISSIONS.md](https://github.com/langchain-ai/terraform/blob/main/modules/azure/PERMISSIONS.md#private-dns-zones-you-own). |

## Ingress

| Variable | Default | Required | Description |
| - | - | - | - |
| `ingress_controller` | `envoy-gateway` | no | Ingress controller: `envoy-gateway` (Gateway API), `nginx` (legacy Ingress compatibility), `istio` (self-managed Helm), `istio-addon` (Azure managed Istio, for mTLS or multi-dataplane), `agic` (Application Gateway Ingress Controller), or `none`. Changing it on an existing deployment removes the old controller and its load balancer IP. See [`INGRESS_CONTROLLERS.md`](https://github.com/langchain-ai/terraform/blob/main/modules/azure/INGRESS_CONTROLLERS.md) for the TLS compatibility matrix. |
| `istio_version` | `1.29.1` | no | Istio Helm chart version. Used only when `ingress_controller = "istio"`. |
| `istio_addon_revision` | `asm-1-27` | no | Azure Service Mesh revision (`asm-1-<minor>`). List available revisions with `az aks mesh get-revisions --location <region>`. Used only when `ingress_controller = "istio-addon"`. |
| `agic_subnet_address_prefix` | `["10.0.96.0/24"]` | no | CIDR for the Application Gateway dedicated subnet. Must be `/24` or larger. Used only when `ingress_controller = "agic"`. |
| `agw_sku_tier` | `Standard_v2` | no | Application Gateway SKU tier. Used only when `ingress_controller = "agic"`. To turn on WAF, set `create_waf = true` instead of `WAF_v2`. |
| `envoy_gateway_version` | `v1.2.0` | no | Envoy Gateway Helm chart version. Used only when `ingress_controller = "envoy-gateway"`. |
| `ingress_ip` | `""` | no | Public IP of the ingress load balancer, used by the DNS module for the A record. For `envoy-gateway`, get it with `kubectl get svc -n envoy-gateway-system -l gateway.envoyproxy.io/owning-gateway-name=langsmith-gateway`. For `nginx`, use `kubectl get svc -n ingress-nginx`. |

## DNS and TLS

| Variable | Default | Required | Description |
| - | - | - | - |
| `dns_label` | `""` | no | Azure Public IP DNS label for the ingress load balancer. Results in `<label>.<region>.cloudapp.azure.com` (`cloudapp.usgovcloudapi.net` in Azure Government). Works with every controller except `none`. With `agic`, it serves HTTP only. Empty skips it. |
| `langsmith_domain` | `""` | when `dns01` or `create_dns_zone` | Custom hostname for LangSmith (for example, `langsmith.example.com`). Used in Helm values and ingress TLS. Takes priority over `dns_label`. |
| `tls_certificate_source` | `letsencrypt` | no | `letsencrypt` (HTTP-01 via cert-manager), `dns01` (DNS-01 via cert-manager), `existing` (your own certificate in a `kubernetes.io/tls` Secret named `langsmith-tls` in the LangSmith namespace, which `deploy.sh` checks), or `none` (HTTP only, demo/dev). |
| `letsencrypt_email` | `""` | when `letsencrypt` or `dns01` | Email for Let's Encrypt certificate notifications. |
| `create_dns_zone` | `false` | no | Create an Azure DNS zone and A record for the LangSmith domain. Required for DNS-01 issuance. |
| `langsmith_custom_ca_secret_name` | `""` | no | Secret in the LangSmith namespace that holds a CA bundle, for endpoints a private CA signed. The chart mounts it in the LangSmith services but not in the operator or the agent deployments it creates. Read by `init-values.sh` and `deploy.sh`; Terraform ignores it. |
| `langsmith_custom_ca_secret_key` | `ca.crt` | no | Key in `langsmith_custom_ca_secret_name` that holds the PEM bundle. |

## LangSmith application

| Variable | Default | Required | Description |
| - | - | - | - |
| `langsmith_namespace` | `langsmith` | no | Kubernetes namespace for LangSmith. Used to scope Workload Identity for blob storage. |
| `langsmith_release_name` | `langsmith` | no | Helm release name. Used for Workload Identity federated credential subjects. |
| `langsmith_domain` | `""` | when `dns01` or `create_dns_zone` | See [DNS and TLS](#dns-and-tls). |
| `langsmith_helm_chart_version` | `""` | no | Pin a chart version for reproducible deploys. The deploy script precedence is the `CHART_VERSION` environment variable, then this variable, then the pinned line default `~0.17.0` (latest `0.17.x` patch). The deploy fails on any other chart line. On a `v0.16.*` module tag, the default is `~0.16.0` and only the 0.16 line deploys, unless `enable_smithdb = true`, which requires the 0.17 line: set this variable to `~0.17.0`. |
| `langsmith_admin_email` | `""` | no | Initial org admin email (`initialOrgAdminEmail` in Helm values). Set via `make setup-env`. |

## Sizing and add-on flags

`init-values.sh` and `deploy.sh` read these flags. Terraform ignores them, except `enable_fleet` and a validation that `enable_gateway_pii_redaction` requires `enable_llm_gateway`. They control which Helm overlays the scripts generate. The `enable_llm_gateway`, `enable_gateway_pii_redaction`, and `enable_sso_oidc` flags exist only on `v0.17.*` module tags.

| Variable | Default | Required | Description |
| - | - | - | - |
| `sizing_profile` | `production` | no | Helm sizing overlay: `minimum`, `dev`, `production`, or `production-large`. |
| `enable_deployments` | `false` | no | Enable Agent Server hosting (host-backend, listener, operator). |
| `enable_agent_builder` | `false` | no | Enable the legacy Agent Builder UI, which Fleet replaces. Requires `enable_deployments = true`. Cannot be combined with `enable_fleet`. |
| `enable_fleet` | `false` | no | Enable Fleet, the successor to Agent Builder. Requires `enable_deployments = true` and `postgres_source = "external"`. Cannot be combined with `enable_agent_builder`. Terraform also creates a `langsmith_fleet` database and the `langsmith-fleet-postgres` Kubernetes secret, so run `make apply` before deploying. |
| `enable_insights` | `false` | no | Enable Insights (ClickHouse-backed analytics). |
| `enable_polly` | `false` | no | Enable Polly (AI evaluation and monitoring). Polly runs on Agent Server, so set `enable_deployments = true` as well. The deploy scripts do not check this. |
| `enable_llm_gateway` | `false` | no | Deploy the [LLM Gateway](../../../../LLM%20Gateway/Get%20started/LLM%20Gateway.md), which is in beta. Requires chart 0.17. See [LLM Gateway](Deploy%20LangSmith%20on%20Azure%20with%20Terraform.md#llm-gateway). |
| `enable_gateway_pii_redaction` | `false` | no | Run the Presidio analyzer beside the LLM Gateway to redact PII from gateway traffic, and turn redaction on for new organizations. Requires `enable_llm_gateway = true`. |
| `enable_sso_oidc` | `false` | no | Switch login to SSO through an OIDC provider and disable basic auth. `make k8s-secrets` copies the client ID, client secret, and issuer URL from Key Vault into `langsmith-config-secret`. Enable only after you have logged in as the org admin with basic auth. See [SSO with OIDC](Deploy%20LangSmith%20on%20Azure%20with%20Terraform.md#sso-with-oidc). |

## SmithDB

SmithDB is optional. `enable_smithdb` provisions Azure resources, so run `make apply` before deploying. It requires the chart 0.17 line, which `v0.17.*` module tags deploy by default. On a `v0.16.*` tag, SmithDB needs v0.16.56 or later and `langsmith_helm_chart_version = "~0.17.0"`. For the full requirements, refer to [`SMITHDB.md`](https://github.com/langchain-ai/terraform/blob/main/modules/azure/SMITHDB.md).

| Variable | Default | Required | Description |
| - | - | - | - |
| `enable_smithdb` | `false` | no | Provision SmithDB infrastructure: a dedicated PostgreSQL 18 metastore, a Blob container, Workload Identity, and Premium SSD v2 cache volumes. Requires a non-empty `availability_zones`, because Premium SSD v2 attaches only to zonal VMs in most regions. |
| `smithdb_ingestion_enabled` | `false` | no | Enable LangSmith writes to SmithDB once the infrastructure is healthy. Requires `enable_smithdb = true`. |
| `smithdb_migration_enabled` | `false` | no | Enable the ClickHouse-to-SmithDB migration job. Requires `smithdb_ingestion_enabled = true`. |
| `smithdb_query_enabled` | `false` | no | Enable SmithDB-backed queries. Requires `smithdb_ingestion_enabled = true`. |
| `smithdb_metastore_admin_username` | `smithdb` | no | Administrator username for the SmithDB PostgreSQL metastore. |
| `smithdb_metastore_admin_password` | `null` | no | Optional administrator password for the metastore. `null` authenticates through Microsoft Entra Workload Identity. Sensitive. |
| `smithdb_metastore_sku_name` | `GP_Standard_D2ds_v5` | no | PostgreSQL Flexible Server SKU for the metastore. |
| `smithdb_metastore_storage_mb` | `32768` | no | Allocated metastore storage in MiB. |
| `smithdb_metastore_backup_retention_days` | `7` | no | Automated backup retention for the metastore, in days. |
| `smithdb_storage_account_name` | `""` | no | Globally unique Storage Account name for SmithDB. Empty derives one from the deployment name. |
| `smithdb_storage_replication_type` | `LRS` | no | Redundancy of the SmithDB object store. Same values and rules as `storage_replication_type`. |
| `smithdb_storage_container_name` | `smithdb` | no | Blob container for SmithDB durable data. |
| `smithdb_cache_storage_class_name` | `""` | no | Name of the Premium SSD v2 StorageClass for SmithDB cache volumes. Empty derives a per-deployment name. |
| `smithdb_cache_disk_iops` | `7000` | no | Provisioned IOPS per cache volume, 3000 to 80000. The default needs a cache volume of at least 14 GiB. |
| `smithdb_cache_disk_throughput_mbps` | `1000` | no | Provisioned throughput per cache volume in MB/s, 125 to 1200. Azure allows at most 0.25 MB/s per provisioned IOPS. |

## Security and audit

| Variable | Default | Required | Description |
| - | - | - | - |
| `create_waf` | `false` | no | Deploy an Azure WAF policy (OWASP 3.2 plus bot protection). With `ingress_controller = "agic"`, Terraform attaches it to the Application Gateway and sets the `WAF_v2` tier. With any other controller, the policy stays unattached for an Application Gateway you own. Azure Front Door cannot use this policy type. |
| `waf_mode` | `Detection` | no | WAF enforcement mode: `Detection` (log only) or `Prevention` (block). OWASP rules match SQL and script fragments that appear legitimately in prompts and traces, so review the firewall log for false positives and add exclusions before you switch to `Prevention`. |
| `create_diagnostics` | `false` | no | Deploy a Log Analytics workspace and diagnostic settings for AKS, Key Vault, PostgreSQL, and the Application Gateway when `ingress_controller = "agic"`. |
| `log_retention_days` | `90` | no | Log Analytics workspace retention in days. |
| `create_bastion` | `false` | no | Deploy a jump VM for private AKS access via `az ssh vm`. |
| `bastion_vm_size` | `Standard_B2s` | no | VM SKU for the bastion host. |
| `bastion_admin_ssh_public_key` | `""` | no | SSH public key for emergency admin access to the bastion. |
| `bastion_allowed_ssh_cidrs` | `["0.0.0.0/0"]` | no | CIDRs allowed inbound SSH to the bastion. Restrict to VPN or corporate ranges in production. |

## Sensitive variables (set with `setup-env.sh`)

`make setup-env` writes `postgres_admin_password`, `langsmith_license_key`, and `langsmith_admin_email` to `secrets.auto.tfvars`. `make apply` stores the license key and the PostgreSQL password in Azure Key Vault. With `keyvault_manage_secrets = false`, `make seed-secrets` stores them instead. Never set these inline in `terraform.tfvars`.

`langsmith_license_key` holds the LangSmith enterprise license key. The [PostgreSQL](#postgresql) and [LangSmith application](#langsmith-application) sections document the other two.

The application secrets are not Terraform variables, so their values never enter Terraform state. `make seed-secrets` writes them to Key Vault after `make apply`: the initial org admin password, the API key salt, the JWT secret, and the Fernet encryption keys for Agent Server hosting, Agent Builder, Insights, and Polly. It never overwrites an existing secret, because changing any of them breaks running deployments. To rotate one deliberately, use `make keyvault`.

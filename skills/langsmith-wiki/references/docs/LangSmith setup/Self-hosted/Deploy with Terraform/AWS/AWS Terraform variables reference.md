# AWS Terraform variables reference

> Complete reference of Terraform variables for LangSmith self-hosted on AWS EKS.

Complete reference for every input variable exposed by the [AWS Terraform modules](https://github.com/langchain-ai/terraform/tree/main/modules/aws). Use it while filling in `terraform.tfvars` for the first time or tuning an existing deployment.

Variables come in two categories:

* **Non-sensitive** (region, sizing, feature flags): set in `infra/terraform.tfvars`.
* **Sensitive** (license key, passwords, encryption keys): sourced through `infra/scripts/setup-env.sh`, which writes them to AWS SSM Parameter Store; External Secrets Operator then syncs them into the cluster.

For the end-to-end install, refer to the [deploy guide](Deploy%20LangSmith%20on%20AWS%20with%20Terraform.md). For how the modules fit together, refer to the [architecture reference](AWS%20Terraform%20architecture.md).

## Core

| Variable | Default | Required | Description |
| - | - | - | - |
| `name_prefix` | none | yes | Prefix for all resource names. Maximum 15 characters: lowercase letters, digits, and hyphens, starting with a letter. Format: `{prefix}-{environment}-{resource}`. |
| `environment` | `dev` | no | Environment tag: `dev`, `staging`, `prod`, `test`, or `uat`. |
| `region` | `us-west-2` | no | AWS region for all resources. |
| `owner` | `""` | no | Team or individual responsible for the deployment. Applied as a tag. |
| `cost_center` | `""` | no | Cost center or billing label. Applied as a tag when non-empty. |
| `tags` | `{}` | no | Additional tags applied to all resources. |

## Networking

| Variable | Default | Required | Description |
| - | - | - | - |
| `create_vpc` | `true` | no | Create a new VPC. Set `false` to use an existing one. |
| `vpc_id` | `null` | when `!create_vpc` | Existing VPC ID. |
| `private_subnets` | `[]` | when `!create_vpc` | Existing private subnet IDs. |
| `public_subnets` | `[]` | when `!create_vpc` and `alb_scheme = "internet-facing"` | Existing public subnet IDs. Not needed for an `internal` ALB. |
| `vpc_cidr_block` | `null` | when `!create_vpc` | Existing VPC CIDR block. |
| `vpc_private_subnets` | `[]` | no | Override CIDRs for private subnets when `create_vpc = true`. Empty uses the module default. |
| `vpc_public_subnets` | `[]` | no | Override CIDRs for public subnets when `create_vpc = true`. Empty uses the module default. |

## EKS

| Variable | Default | Required | Description |
| - | - | - | - |
| `enable_public_eks_cluster` | `true` | no | Enable the public EKS API endpoint. Set `false` for a private cluster and enable `create_bastion` to run Terraform and Helm from the bastion via SSM. |
| `eks_public_access_cidrs` | `["0.0.0.0/0"]` | no | CIDRs allowed to reach the public EKS API endpoint. Restrict to corporate VPN egress CIDRs to lock down access. |
| `eks_cluster_version` | `1.34` | no | EKS Kubernetes version, in `X.Y` format. With `enable_smithdb = true`, keep `smithdb_karpenter_chart_version` compatible with it. |
| `eks_managed_node_group_defaults` | `{ami_type = "AL2023_x86_64_STANDARD"}` | no | Default configuration applied to all managed node groups. |
| `eks_managed_node_groups` | one `default` group: `m5.4xlarge`, min 3 / max 10 | no | Managed node group definitions. `desired_size` defaults to `min_size` when omitted. |
| `create_gp3_storage_class` | `true` | no | Create `gp3` and set it as the default `StorageClass` with volume expansion enabled. |
| `eks_cluster_enabled_log_types` | `["api", "audit", "authenticator", "controllerManager", "scheduler"]` | no | EKS control plane log types sent to CloudWatch. Set `[]` to disable. |
| `eks_addons` | `{}` | no | EKS managed add-on configurations (`coredns`, `kube-proxy`, `vpc-cni`, and similar). |
| `create_langsmith_irsa_role` | `true` | no | Create the IRSA role for LangSmith pods (S3 access). |
| `enable_bedrock_access` | `false` | no | Attach a Bedrock `InvokeModel` policy to the LangSmith IRSA role so LangSmith pods can call Bedrock models through workload identity instead of static AWS keys. Requires `create_langsmith_irsa_role = true`. |

## PostgreSQL (RDS)

| Variable | Default | Required | Description |
| - | - | - | - |
| `postgres_source` | `external` | no | `external` (RDS with private access) or `in-cluster` (deployed via Helm). |
| `postgres_instance_type` | `db.t3.large` | no | RDS instance class. |
| `postgres_storage_gb` | `10` | no | Initial RDS storage in GB. |
| `postgres_max_storage_gb` | `100` | no | Maximum RDS storage in GB (autoscaling). |
| `postgres_username` | `langsmith` | no | RDS database username. |
| `postgres_engine_version` | `16` | no | PostgreSQL engine version. PG 14 reaches EOL in November 2026; 16 is recommended for new deployments. |
| `postgres_password` | `""` | when external | RDS master password. `setup-env.sh` generates it (`openssl rand -hex 32`) and stores it in SSM if the parameter does not exist yet; to supply your own on first run, export `TF_VAR_postgres_password` before sourcing the script. To rotate it, run `manage-ssm.sh set`, then `unset TF_VAR_postgres_password` or open a new shell, source `setup-env.sh` again, and run `make apply` so Terraform updates RDS and the `langsmith-postgres` Secret. Then run `kubectl rollout restart deployment -n langsmith` so the pods read the new password. Must be 8 to 128 characters with no `/`, `@`, `"`, `'`, or space. |
| `postgres_iam_database_authentication_enabled` | `true` | no | Enable IAM database authentication on RDS. |
| `postgres_iam_database_user` | `null` | no | Database user for IAM authentication. Must exist in PostgreSQL with `GRANT rds_iam TO <user>`. |
| `postgres_deletion_protection` | `true` | no | Prevent accidental RDS deletion. Set `false` for dev/test environments. |
| `postgres_backup_retention_period` | `7` | no | Days to retain automated RDS backups. `0` disables backups. |
| `postgres_skip_final_snapshot` | `false` | no | Skip the final snapshot when the RDS instance is destroyed. Set `true` for dev/test stacks rebuilt under the same name; otherwise destroy leaves a `<name>-final` snapshot. |
| `postgres_existing_security_group_id` | `null` | no | Attach an existing security group to the RDS instance instead of creating one. Terraform does not manage its rules; it must already allow TCP 5432 from the VPC CIDR. |

## Redis (ElastiCache)

| Variable | Default | Required | Description |
| - | - | - | - |
| `redis_source` | `external` | no | `external` (ElastiCache with private access) or `in-cluster` (deployed via Helm). |
| `redis_instance_type` | `cache.m6g.xlarge` | no | ElastiCache node type. |
| `redis_auth_token` | `""` | when external | ElastiCache auth token, at least 16 characters. `setup-env.sh` generates it (`openssl rand -hex 32`) and stores it in SSM if the parameter does not exist yet; to supply your own on first run, export `TF_VAR_redis_auth_token` before sourcing the script. To rotate it, run `manage-ssm.sh set`, then `unset TF_VAR_redis_auth_token` or open a new shell, source `setup-env.sh` again, and run `make apply` so Terraform updates ElastiCache and the `langsmith-redis` Secret. Then run `kubectl rollout restart deployment -n langsmith` so the pods read the new token. |
| `redis_existing_security_group_id` | `null` | no | Attach an existing security group to the ElastiCache replication group instead of creating one. Terraform does not manage its rules; it must already allow TCP 6379 from the VPC CIDR. |

## S3

| Variable | Default | Required | Description |
| - | - | - | - |
| `s3_ttl_enabled` | `true` | no | Enable S3 lifecycle rules to expire trace blobs. |
| `s3_ttl_short_days` | `14` | no | Days before expiring short-lived objects (`ttl_s/` prefix). |
| `s3_ttl_long_days` | `400` | no | Days before expiring long-lived objects (`ttl_l/` prefix). |
| `s3_kms_key_arn` | `""` | no | KMS CMK ARN for S3 encryption. Empty uses SSE-S3 (AES256). |
| `s3_versioning_enabled` | `false` | no | Enable S3 bucket versioning. Increases storage cost as prior versions are retained. |

## TLS and DNS

| Variable | Default | Required | Description |
| - | - | - | - |
| `tls_certificate_source` | `acm` | no | TLS source: `acm`, `letsencrypt` (cert-manager HTTP-01 ACME solved through the ALB), or `none`. For DNS-01 challenges through Route 53 (in-cluster gateways), use `create_cert_manager_irsa` instead; the two are mutually exclusive. |
| `acm_certificate_arn` | `""` | when `acm` and `langsmith_domain` is empty | Existing ACM certificate ARN. Leave empty and set `langsmith_domain` to have Terraform request and validate a certificate. |
| `letsencrypt_email` | `""` | when `letsencrypt` or `create_cert_manager_irsa` | Email for Let's Encrypt ACME registration. |
| `langsmith_domain` | `""` | when `acm` and `acm_certificate_arn` is empty | Custom domain. When set and `acm_certificate_arn` is empty, Terraform creates a Route 53 hosted zone (or uses `dns_existing_zone_id`), requests an ACM certificate, and creates the ALB alias record. Empty uses the ALB hostname. |
| `dns_create_zone` | `true` | no | Create a public Route 53 hosted zone for `langsmith_domain`. Set `false` to write the validation and alias records into `dns_existing_zone_id`. |
| `dns_existing_zone_id` | `""` | when `dns_create_zone = false`, `langsmith_domain` is set, and `acm_certificate_arn` is empty | ID of an existing public Route 53 hosted zone for `langsmith_domain` or a parent domain (starts with `Z`). |
| `dns_include_wildcard_san` | `false` | no | Add a wildcard SAN (`*.<langsmith_domain>`) to the ACM certificate. Needed for HTTPS on subdomains. |
| `langsmith_namespace` | `langsmith` | no | Kubernetes namespace for LangSmith. |

## Ingress

| Variable | Default | Required | Description |
| - | - | - | - |
| `alb_scheme` | `internet-facing` | no | ALB scheme: `internet-facing` (public subnets) or `internal` (private subnets, reachable via VPN, peering, or PrivateLink). |
| `alb_allowed_cidr_blocks` | `["0.0.0.0/0"]` | no | CIDRs allowed to reach the ALB on HTTP/HTTPS. Restrict to VPN or office CIDRs for limited-access deployments. |
| `alb_access_logs_enabled` | `false` | no | Enable ALB access logging to a dedicated S3 bucket. |
| `alb_existing_security_group_id` | `null` | no | Attach an existing security group to the ALB instead of creating one. Terraform does not manage its rules; it must already allow HTTP and HTTPS from `alb_allowed_cidr_blocks`. |
| `enable_envoy_gateway` | `null` | no | Install Envoy Gateway; the chart creates Gateway API `HTTPRoute` resources behind the ALB. Unset means `true` unless `enable_istio_gateway` or `enable_nginx_ingress` is `true`. Set `false` for a plain ALB-backed Ingress. Supports split dataplane routing across namespaces. |
| `enable_nginx_ingress` | `false` | no | Install the NGINX ingress controller. The ALB forwards to NGINX controller pods via a `TargetGroupBinding`. Turns off the Envoy Gateway default. |
| `enable_istio_gateway` | `false` | no | Install Istio (`istio-base`, `istiod`, and an ingress gateway behind the ALB `TargetGroupBinding`) and open port 15017 on the node security group for the istiod sidecar-injector webhook. Turns off the Envoy Gateway default. |
| `create_cert_manager_irsa` | `false` | no | Create the IRSA role for cert-manager DNS-01 challenges through Route 53, and the `letsencrypt-prod` DNS-01 `ClusterIssuer` (needs `langsmith_domain` and `cert_manager_hosted_zone_id`). Use with Istio Gateway. Mutually exclusive with `tls_certificate_source = "letsencrypt"`. |
| `cert_manager_hosted_zone_id` | `""` | when `create_cert_manager_irsa` | Route 53 hosted zone ID for cert-manager DNS-01 TXT records. |

Terraform rejects a configuration that sets more than one of `enable_envoy_gateway`, `enable_istio_gateway`, and `enable_nginx_ingress` to `true`.

## ClickHouse

| Variable | Default | Required | Description |
| - | - | - | - |
| `clickhouse_source` | `in-cluster` | no | `in-cluster` or `external` (LangChain Managed ClickHouse). |

## SmithDB

`enable_smithdb` provisions the SmithDB dependencies. The three gates require `enable_smithdb = true`, and `smithdb_migration_enabled` and `smithdb_query_enabled` each require `smithdb_ingestion_enabled = true`.

| Variable | Default | Required | Description |
| - | - | - | - |
| `enable_smithdb` | `false` | no | Provision SmithDB dependencies: a dedicated metastore RDS, an S3 bucket, an IRSA role, and Karpenter node pools on local-NVMe instances. |
| `smithdb_ingestion_enabled` | `false` | no | Route new writes to SmithDB. Requires `enable_smithdb`. |
| `smithdb_migration_enabled` | `false` | no | Enable historical ClickHouse-to-SmithDB migration. Requires `smithdb_ingestion_enabled`. |
| `smithdb_query_enabled` | `false` | no | Serve queries from SmithDB. Requires `smithdb_ingestion_enabled`. |
| `langsmith_release_name` | `langsmith` | no | Helm release name; scopes the SmithDB IRSA trust to `<release>-langsmith-smithdb`. Must match the release `deploy.sh` uses. |
| `smithdb_metastore_source` | `create` | no | `create` (dedicated RDS) or `external`. Must be separate from the app database. |
| `smithdb_metastore_instance_class` | `db.m6g.large` | no | Metastore RDS instance class. |
| `smithdb_metastore_engine_version` | `18` | no | Metastore PostgreSQL version. |
| `smithdb_metastore_allocated_storage` | `50` | no | Metastore storage in GB. |
| `smithdb_metastore_multi_az` | `false` | no | Run the metastore Multi-AZ. |
| `smithdb_metastore_deletion_protection` | `true` | no | Prevent metastore deletion; set `false` before destroying. |
| `smithdb_metastore_backup_retention_period` | `7` | no | Days of metastore backups; `0` disables backups. |
| `smithdb_metastore_skip_final_snapshot` | `false` | no | Skip the final snapshot on destroy. |
| `smithdb_metastore_use_ssl` | `true` | no | Connect to the metastore over SSL. |
| `smithdb_metastore_master_username` | `smithdb` | no | Master username for the created metastore. Terraform generates the password. |
| `smithdb_external_metastore_host` | `null` | when `enable_smithdb` and `external` | Existing metastore hostname. |
| `smithdb_external_metastore_port` | `5432` | no | Existing metastore port. |
| `smithdb_external_metastore_database` | `smithdb` | no | Existing metastore database name. |
| `smithdb_external_metastore_username` | `null` | when `enable_smithdb` and `external` | Existing metastore username. |
| `smithdb_external_metastore_password` | `null` | when `enable_smithdb` and `external` | Existing metastore password. Sensitive; set with `TF_VAR_smithdb_external_metastore_password`. |
| `smithdb_existing_metastore_security_group_id` | `null` | no | Attach an existing security group to the created metastore. |
| `smithdb_manage_byo_security_group_rules` | `false` | no | Let Terraform add the TCP 5432 rule from the EKS nodes to the existing security group. |
| `smithdb_bucket_name` | `""` | no | Bucket name; empty generates `{name_prefix}-{environment}-smithdb-{suffix}`. |
| `smithdb_s3_versioning_enabled` | `false` | no | Enable bucket versioning. |
| `smithdb_s3_force_destroy` | `false` | no | Allow deleting a non-empty bucket. Test stacks only. |
| `smithdb_karpenter_chart_version` | `1.6.3` | no | Karpenter chart version; must match `eks_cluster_version` (1.34 needs 1.6 or later, 1.35 needs 1.9 or later, 1.36 needs 1.13). |
| `smithdb_karpenter_ami_alias` | `al2023@latest` | no | `EC2NodeClass` AMI alias. |
| `smithdb_node_arch` | `amd64` | no | `amd64` or `arm64`. |
| `smithdb_capacity_type` | `["on-demand"]` | no | Karpenter capacity types; on-demand recommended. |
| `smithdb_instance_store_sizes` | `["4xlarge", "8xlarge", "16xlarge"]` | no | Sizes allowed in the instance-store pool. |
| `smithdb_instance_store_min_local_nvme_gib` | `800` | no | Minimum local NVMe per instance-store node, in GiB. |
| `smithdb_instance_store_limits` | `{cpu = 512, memory = "4096Gi"}` | no | Instance-store pool CPU and memory cap. |
| `smithdb_compute_sizes` | `["2xlarge", "4xlarge", "8xlarge"]` | no | Sizes allowed in the compute pool. |
| `smithdb_compute_limits` | `{cpu = 256, memory = "1024Gi"}` | no | Compute pool CPU and memory cap. |
| `smithdb_node_root_volume_size_gb` | `100` | no | Root EBS size for SmithDB nodes, in GB. |

## Bastion (private cluster)

| Variable | Default | Required | Description |
| - | - | - | - |
| `create_bastion` | `false` | no | Create an EC2 bastion for private cluster access via SSM Session Manager or SSH. It runs in a private subnet unless `bastion_enable_ssh = true`. |
| `bastion_instance_type` | `t3.micro` | no | EC2 instance type for the bastion. |
| `bastion_key_name` | `null` | no | EC2 key pair for SSH. Empty uses SSM Session Manager only. |
| `bastion_enable_ssh` | `false` | no | Open port 22 on the bastion security group and place the bastion in a public subnet with a public IP. |
| `bastion_ssh_allowed_cidrs` | `[]` | no | CIDRs allowed to SSH to the bastion. Used only when `bastion_enable_ssh = true`. |
| `bastion_root_volume_size_gb` | `20` | no | Root EBS volume size in GB for the bastion. |
| `bastion_existing_security_group_id` | `null` | no | Attach an existing security group to the bastion instead of creating one. Terraform does not manage its rules. |

## Security and audit

| Variable | Default | Required | Description |
| - | - | - | - |
| `create_cloudtrail` | `false` | no | Create a CloudTrail trail logging AWS API calls to S3. Skip if an account-level or org-level trail already exists. |
| `cloudtrail_multi_region` | `true` | no | Record API calls across all regions. |
| `cloudtrail_log_retention_days` | `365` | no | Days to retain CloudTrail logs in S3. `0` keeps them indefinitely. |
| `create_waf` | `false` | no | Attach a WAFv2 Web ACL to the ALB (AWS managed rules for OWASP Top 10, IP reputation, bad inputs). Cost: about `$8` to `$10`/mo base. |
| `create_firewall` | `false` | no | Deploy AWS Network Firewall for FQDN-based egress filtering. Requires `create_vpc = true`. Cost: about `$0.395/hr` per endpoint plus `$0.065/GB`. |
| `firewall_allowed_fqdns` | `["beacon.langchain.com"]` | no | Domains allowed for outbound traffic when `create_firewall = true`. Matched against TLS SNI and HTTP Host headers. All other destinations are dropped. |
| `firewall_subnet_cidr` | `10.0.64.0/21` | no | CIDR for the firewall subnet. Must be within the VPC CIDR and must not overlap the private subnets (default `10.0.0.0/21`, `10.0.8.0/21`, and `10.0.16.0/21`) or the public subnets (default `10.0.40.0/21`, `10.0.48.0/21`, and `10.0.56.0/21`). |

## Sizing and feature flags

`sizing_profile` and the `enable_*` flags in this table are read by `init-values.sh` and `deploy.sh`, which pick the Helm overlay files. Terraform acts on a flag only when it needs a dedicated database: `enable_fleet` with `fleet_storage = "external"`, `enable_insights` or `enable_polly` with their `*_storage = "external"`, and `enable_standalone_insights` or `enable_standalone_polly`. For those, Terraform creates the database-init Job and Kubernetes secrets, and a plan-time precondition requires `postgres_source` and `redis_source` to be `external`.

| Variable | Default | Required | Description |
| - | - | - | - |
| `sizing_profile` | `default` | no | Helm sizing: `production`, `production-large`, `dev`, `minimum`, or `default`. |
| `langsmith_helm_chart_version` | `""` | no | Pin the LangSmith Helm chart to an exact `0.17.x` patch. Empty deploys the latest v17 patch. Validation rejects other lines. The `CHART_VERSION` environment variable overrides it. On `v0.16.*` module releases, use a `0.16.x` patch. |
| `enable_deployments` | `false` | no | Enable Agent Server hosting (listener, operator, host-backend). Requires the Deployments license entitlement. |
| `enable_fleet` | `false` | no | Enable Fleet and the host-backend it needs. Does not require `enable_deployments`. With `fleet_storage = "external"` (the default), requires `postgres_source` and `redis_source` to be `external`. Replaces `enable_agent_builder`. |
| `fleet_storage` | `external` | no | Where Fleet keeps its PostgreSQL and Redis data: `external` (requires `postgres_source` and `redis_source` to be `external`) or `in-cluster`. |
| `enable_insights` | `false` | no | Enable Insights (AI-powered trace analysis). Requires the Insights entitlement. Storage follows `insights_storage`. |
| `insights_storage` | `in-cluster` | no | Where Insights keeps its PostgreSQL and Redis data: `in-cluster` (chart StatefulSets) or `external` (dedicated databases on the shared RDS and ElastiCache; requires `postgres_source` and `redis_source` to be `external`). |
| `enable_polly` | `false` | no | Enable LangSmith Chat (formerly Polly). Does not require `enable_deployments`. Requires the LangSmith Chat entitlement. Storage follows `polly_storage`. |
| `polly_storage` | `in-cluster` | no | Where LangSmith Chat keeps its PostgreSQL and Redis data: `in-cluster` or `external` (same rules as `insights_storage`). |
| `enable_standalone_polly` | `false` | no | Legacy shorthand for `enable_polly = true` with `polly_storage = "external"`: dedicated databases on the shared RDS and ElastiCache. Requires `postgres_source` and `redis_source` to be `external`. |
| `enable_standalone_insights` | `false` | no | Legacy shorthand for `enable_insights = true` with `insights_storage = "external"`: dedicated databases on the shared RDS and ElastiCache. ClickHouse is still required. Requires `postgres_source` and `redis_source` to be `external`. |
| `enable_usage_telemetry` | `false` | no | Enable extended usage telemetry reporting. |
| `enable_sso_oidc` | `false` | no | Enable SSO through any OIDC provider and turn off basic auth. First store `oauth-client-id`, `oauth-client-secret`, and `oauth-issuer-url` in SSM with `infra/scripts/manage-ssm.sh set`; `make init-values` fails without them. Turn it on only after the first install, once org-admin access is confirmed. |

> [!WARNING]
>
> `enable_agent_builder` was removed in chart v16. Setting it to `true` fails validation at `terraform plan`, so replace `enable_agent_builder = true` with `enable_fleet = true`.

## Sandboxes

| Variable | Default | Required | Description |
| - | - | - | - |
| `enable_sandboxes` | `false` | no | Provision LangSmith Sandboxes prerequisites: a dedicated JuiceFS metadata ElastiCache, a `sandbox-host` node group, and the JuiceFS config secret. Sandbox hosts need usable KVM (`/dev/kvm`): bare-metal or nested-virtualization x86\_64 types. Requires LangSmith Helm chart v16 or later. |
| `sandbox_host_node_count` | `1` | no | Fixed number of sandbox-host nodes. At least `1`. |
| `sandbox_host_instance_types` | `["m5d.metal"]` | no | Instance types for the sandbox-host node group. Must expose KVM. On types without instance store, set `sandbox_host_local_nvme_bootstrap_enabled = false`. |
| `sandbox_host_local_nvme_bootstrap_enabled` | `true` | no | Format local NVMe instance-store devices: the first as swap, the rest as JuiceFS cache. |
| `sandbox_host_local_nvme_expected_device_count` | `4` | no | Number of instance-store NVMe devices each host must have. Must match the instance type. |
| `sandbox_host_node_group_overrides` | `{}` | no | Advanced overrides merged into the generated sandbox-host node group. |
| `sandbox_juicefs_name` | `sandbox-juicefs` | no | JuiceFS volume name for sandbox snapshots and filesystem state. |
| `sandbox_juicefs_redis_instance_type` | `cache.m6g.large` | no | ElastiCache node type for the JuiceFS metadata Redis. |
| `sandbox_juicefs_redis_snapshot_retention_limit` | `7` | no | Days of automated snapshots for the JuiceFS metadata Redis, `0` to `35`. |
| `sandbox_juicefs_csi_config_secret_name` | `juicefs-csi-config` | no | Name of the JuiceFS config secret Terraform creates in the LangSmith namespace, with the keys `name`, `metaurl`, `storage`, and `bucket`. Passed to the chart as `sandboxes.juicefs.existingSecretName` (chart v16: `sandboxes.juicefs.csi.existingSecretName`). |
| `sandbox_juicefs_csi_config_secret_revision` | `1` | no | Increment to rewrite the write-only JuiceFS config secret. The rewrite does not restart `sandbox-host`, so restart it after the apply, for example `kubectl rollout restart deployment/langsmith-sandbox-host -n langsmith` with the default release name and namespace. |
| `sandbox_service_url_base_url` | `""` | no | Base URL for HTTP services running inside sandboxes. Needs wildcard DNS and TLS for the host. |

## Sensitive values (set with `setup-env.sh`)

Sourcing `infra/scripts/setup-env.sh` reads each value from SSM Parameter Store under `/langsmith/{name_prefix}-{environment}/`. On first run it generates or prompts for the value and stores it in SSM; External Secrets Operator syncs SSM into the cluster. Terraform reads only `postgres_password`, `redis_auth_token`, and `sandbox_juicefs_redis_auth_token`; the other `TF_VAR_*` values are declared but unused, so a value in `terraform.tfvars` never reaches SSM. To supply your own value, export it before sourcing the script, which writes it to SSM only if the parameter does not exist yet. An exported value also takes precedence over SSM for Terraform. To change a stored value, run `manage-ssm.sh set`. For the three values Terraform reads, `setup-env.sh` does not re-read a variable that is already exported, so unset it or open a new shell, source `setup-env.sh` again, and run `make apply` so the RDS and ElastiCache credentials match. Then restart the deployments that read the changed credential.

| Variable | Description |
| - | - |
| `LANGSMITH_LICENSE_KEY` | Environment variable, not a Terraform variable. Enterprise license key. Prompted on first run. |
| `LANGSMITH_ADMIN_PASSWORD` | Environment variable. Initial org admin password. Prompted. Minimum 12 characters, with a lowercase letter, an uppercase letter, and a symbol. |
| `LANGSMITH_ADMIN_EMAIL` | Environment variable. Initial org admin email. Prompted. |
| `postgres_password` | RDS master password. Auto-generated. Read by Terraform. |
| `redis_auth_token` | ElastiCache auth token. Auto-generated. Read by Terraform. |
| `langsmith_api_key_salt` | Salt for hashing API keys. Auto-generated. Changing it invalidates every API key. |
| `langsmith_jwt_secret` | JWT secret for Basic Auth sessions. Auto-generated. Changing it signs out every user. |
| `langsmith_deployments_encryption_key` | Fernet key for Agent Server hosting. Auto-generated. Must never change. |
| `langsmith_agent_builder_encryption_key` | Fernet key for Fleet (name kept for compatibility). Auto-generated. Must never change. |
| `langsmith_insights_encryption_key` | Fernet key for Insights. Auto-generated. Must never change. |
| `langsmith_polly_encryption_key` | Fernet key for LangSmith Chat (formerly Polly). Auto-generated. Must never change. |
| `sandbox_juicefs_redis_auth_token` | JuiceFS metadata Redis auth token. Auto-generated when `enable_sandboxes = true`. Read by Terraform. |
| `sandbox_callback_signing_jwk` | Ed25519 private JWK for sandbox callbacks. Auto-generated when `enable_sandboxes = true`. |

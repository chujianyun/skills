# GCP Terraform variables reference

> Complete reference of Terraform variables for LangSmith self-hosted on GCP GKE.

Complete reference for every input variable exposed by the [GCP Terraform modules](https://github.com/langchain-ai/terraform/tree/main/modules/gcp). Use it while filling in `terraform.tfvars` for the first time or tuning an existing deployment.

Variables come in two categories:

* **Non-sensitive** (region, sizing, feature flags): set in `infra/terraform.tfvars`.
* **Sensitive** (license key, passwords, encryption keys): sourced through `infra/scripts/setup-env.sh`, which writes them to Google Secret Manager and exports them for the Terraform and Helm steps.

Defaults reflect the `main` branch and `v0.17.x` tags, which deploy Helm chart 0.17. Rows that differ on `v0.16.x` tags, which deploy chart 0.16, say so.

For the end-to-end install, refer to the [deploy guide](Deploy%20LangSmith%20on%20GCP%20with%20Terraform.md). For how the modules fit together, refer to the [architecture reference](GCP%20Terraform%20architecture.md).

## Core

| Variable | Default | Required | Description |
| - | - | - | - |
| `project_id` | — | yes | GCP project ID where resources are created. |
| `region` | `us-west2` | no | GCP region for regional resources. |
| `zone` | `us-west2-a` | no | GCP zone for zonal resources. |
| `environment` | `prod` | no | Environment name applied to labels and resource names: `dev`, `staging`, `prod`, `test`, or `uat`. `setup-env.sh` exports the value from `terraform.tfvars`, falling back to `dev`. Set it explicitly: when it is missing, `setup-env.sh` still names secrets with the empty value (`langsmith-<name_prefix>--<key>`). |
| `name_prefix` | `ls` | no | Prefix for all resource names. 1 to 11 characters, starting with a lowercase letter; lowercase letters, numbers, and hyphens only. |
| `unique_suffix` | `true` | no | Append a random suffix to resource names. Recommended for multi-tenant projects. |
| `owner` | `platform-team` | no | Owner label applied to all resources. Sourcing `setup-env.sh` overrides it with the `LANGSMITH_OWNER` environment variable, which is empty when unset. |
| `cost_center` | `""` | no | Cost center label for billing attribution. Sourcing `setup-env.sh` overrides it with `LANGSMITH_COST_CENTER`. |
| `labels` | `{}` | no | Additional labels applied to all resources. |

## Networking

| Variable | Default | Required | Description |
| - | - | - | - |
| `subnet_cidr` | `10.0.0.0/20` | no | CIDR for the GKE subnet. Must not overlap existing ranges. |
| `pods_cidr` | `10.4.0.0/14` | no | CIDR for GKE pods. Must not overlap the subnet or services range. |
| `services_cidr` | `10.8.0.0/20` | no | CIDR for GKE services. Must not overlap the subnet or pods range. |
| `gke_master_authorized_cidrs` | `[]` | no | External CIDRs permitted to reach the GKE control plane endpoint. Empty leaves the control plane publicly reachable so Terraform-managed Helm and `kubectl` steps work from any apply host. Populate with operator and CI egress CIDRs for production. |

## GKE

| Variable | Default | Required | Description |
| - | - | - | - |
| `gke_use_autopilot` | `false` | no | Use GKE Autopilot mode. Autopilot always uses Dataplane V2. |
| `gke_node_count` | `2` | no | Initial node count per zone (Standard mode only). |
| `gke_min_nodes` | `2` | no | Minimum nodes per zone for autoscaling. |
| `gke_max_nodes` | `10` | no | Maximum nodes per zone for autoscaling. |
| `gke_machine_type` | `e2-standard-4` | no | GKE node machine type (for example `e2-standard-4`, `n2-standard-8`). |
| `gke_disk_size` | `100` | no | Node disk size in GB. |
| `gke_release_channel` | `REGULAR` | no | GKE release channel: `RAPID`, `REGULAR`, or `STABLE`. |
| `gke_deletion_protection` | `true` | no | Enable deletion protection on the GKE cluster. |
| `gke_node_service_account_email` | `null` | no | Service account for Standard-mode GKE nodes. `null` keeps the GKE default; production deployments should pass a minimally privileged node service account. Pods use Workload Identity separately. |
| `gke_network_policy_provider` | `DATA_PLANE_V2` | no | Network policy provider: `CALICO` (legacy) or `DATA_PLANE_V2` (Cilium-based, recommended). |

## PostgreSQL (Cloud SQL)

| Variable | Default | Required | Description |
| - | - | - | - |
| `postgres_source` | `external` | no | `external` (Cloud SQL with private IP) or `in-cluster` (deployed via Helm). |
| `postgres_version` | `POSTGRES_15` | no | Cloud SQL PostgreSQL version. |
| `postgres_tier` | `db-custom-2-8192` | no | Cloud SQL machine tier (for example `db-f1-micro`, `db-custom-2-8192`). |
| `postgres_disk_size` | `50` | no | Cloud SQL disk size in GB. |
| `postgres_high_availability` | `true` | no | Enable Cloud SQL HA (regional standby). |
| `postgres_deletion_protection` | `true` | no | Prevent deletion of the Cloud SQL instance from Terraform and from the Cloud SQL API. Set `false` and apply that change before running destroy. |
| `postgres_database_flags` | see description | no | Database flags set on the Cloud SQL instance. Defaults to `max_connections = 500` plus checkpoint and connection logging flags. |
| `postgres_ssl_mode` | `ENCRYPTED_ONLY` | no | Cloud SQL SSL enforcement. `ENCRYPTED_ONLY` requires TLS for every connection. `ALLOW_UNENCRYPTED_AND_ENCRYPTED` accepts plaintext. `TRUSTED_CLIENT_CERTIFICATE_REQUIRED` also requires a client certificate. |
| `postgres_password` | `""` | when external | Cloud SQL password. Set via `TF_VAR_postgres_password`, or stored in Secret Manager by `setup-env.sh`. |

## Redis (Memorystore)

| Variable | Default | Required | Description |
| - | - | - | - |
| `redis_source` | `external` | no | `external` (Memorystore with private IP) or `in-cluster` (deployed via Helm). |
| `redis_version` | `REDIS_7_0` | no | Memorystore Redis version. |
| `redis_memory_size` | `5` | no | Memorystore Redis memory size in GB. |
| `redis_high_availability` | `true` | no | Enable Memorystore HA (Standard HA tier). |
| `redis_prevent_destroy` | `false` | no | Prevent accidental Terraform destroy of the Redis instance. |

## ClickHouse

| Variable | Default | Required | Description |
| - | - | - | - |
| `clickhouse_source` | `in-cluster` | no | `in-cluster` (dev/POC only), `langsmith-managed` (recommended for production), or `external` (self-hosted). |
| `clickhouse_host` | `""` | when managed or external | ClickHouse host. |
| `clickhouse_port` | `9440` | no | ClickHouse native protocol port (`9440` for TLS, `9000` for non-TLS). |
| `clickhouse_http_port` | `8443` | no | ClickHouse HTTP port (`8443` for TLS, `8123` for non-TLS). |
| `clickhouse_user` | `default` | no | ClickHouse username. |
| `clickhouse_password` | `""` | when managed or external | ClickHouse password. |
| `clickhouse_database` | `default` | no | ClickHouse database name. |
| `clickhouse_tls` | `true` | no | Enable TLS for ClickHouse connections. |
| `clickhouse_ca_cert` | `""` | no | ClickHouse CA certificate (PEM) for TLS verification. Empty uses system CAs. |

## GCS storage

| Variable | Default | Required | Description |
| - | - | - | - |
| `storage_ttl_short_days` | `14` | no | GCS TTL in days for the `ttl_s/` prefix. |
| `storage_ttl_long_days` | `400` | no | GCS TTL in days for the `ttl_l/` prefix. |
| `storage_force_destroy` | `false` | no | Allow bucket deletion even with objects inside. Use with caution. |

## LangSmith application

| Variable | Default | Required | Description |
| - | - | - | - |
| `langsmith_namespace` | `langsmith` | no | Kubernetes namespace for LangSmith. |
| `langsmith_domain` | `langsmith.example.com` | no | Fully qualified domain name for LangSmith. |
| `langsmith_license_key` | `""` | no | License key. Use `TF_VAR_langsmith_license_key`. |
| `langsmith_helm_chart_version` | `""` | no | Helm chart version for the deploy script. Empty installs the latest `0.17.x` patch (`~0.17.0`). An exported `CHART_VERSION` takes precedence. The deploy script refuses versions outside the 0.17 line. On chart 0.16, the default is `~0.16.0` and the line is 0.16. |
| `langsmith_release_name` | `langsmith` | no | Helm release name. Must match the release the deploy step installs, because chart-created service account names derive from it. |

## Ingress and TLS

| Variable | Default | Required | Description |
| - | - | - | - |
| `install_ingress` | `true` | no | Install Envoy Gateway through Terraform. The Gateway listeners follow `tls_certificate_source`: `none` creates an HTTP listener, `letsencrypt` creates HTTP and HTTPS listeners, and `existing` creates an HTTPS listener only. |
| `ingress_type` | `envoy` | no | Ingress type: `envoy` (implemented), or `istio` / `other` (reserved). |
| `tls_certificate_source` | `none` | no | `none`, `letsencrypt` (auto via cert-manager), or `existing` (provide your own certs). |
| `install_cert_manager` | `false` | no | Install cert-manager. Terraform also installs it when `tls_certificate_source = "letsencrypt"`. |
| `letsencrypt_email` | `""` | when `letsencrypt` | Email for Let's Encrypt notifications. |
| `tls_certificate_crt` | `""` | when `existing` | TLS certificate (PEM). Load with `file()`. |
| `tls_certificate_key` | `""` | when `existing` | TLS private key (PEM). Load with `file()`. |
| `tls_secret_name` | `langsmith-tls` | no | Name for the TLS secret in Kubernetes. |

## KEDA

| Variable | Default | Required | Description |
| - | - | - | - |
| `enable_langsmith_deployment` | `true` | no | Install KEDA for queue-driven autoscaling of LangSmith workers. This is the KEDA install toggle, not the Agent Server hosting feature (see `enable_deployments`). |

## Optional GCP modules

| Variable | Default | Required | Description |
| - | - | - | - |
| `enable_gcp_iam_module` | `true` | no | Wire `modules/iam` for Workload Identity and bucket IAM bindings. |
| `enable_secret_manager_module` | `false` | no | Wire `modules/secrets` to store generated bootstrap credentials in Secret Manager. |
| `grant_project_secret_accessor` | `false` | no | Grant the LangSmith service account `roles/secretmanager.secretAccessor` on the whole project. No module component needs it; set `true` only for a workload you added that reads Secret Manager as that service account. On chart 0.16, the grant is always on and this variable does not exist. |
| `enable_dns_module` | `false` | no | Wire `modules/dns` for Cloud DNS and a managed certificate. |
| `dns_create_zone` | `true` | no | Create a new Cloud DNS managed zone when the DNS module is enabled. |
| `dns_existing_zone_name` | `""` | when `!dns_create_zone` | Existing Cloud DNS zone to use. |
| `dns_create_certificate` | `true` | no | Create a Google-managed SSL certificate when the DNS module is enabled. |

## Sizing and feature flags

The Helm deploy scripts read these flags from `terraform.tfvars` to enable the matching chart components, and Terraform reads `enable_fleet`, `enable_standalone_polly`, and `enable_standalone_insights` to provision per-feature databases when Postgres and Redis are external. `sizing_profile` is read by the deploy scripts to select the Helm sizing overlay.

| Variable | Default | Required | Description |
| - | - | - | - |
| `sizing_profile` | `default` | no | Helm sizing: `production` (\~20 users, \~100 traces/sec), `production-large` (\~50 users, \~1000 traces/sec), `dev` (single-replica), `minimum` (cost-parking floor, not for production), or `default` (chart defaults). With `enable_smithdb = true`, also sets the `smithdb_sizing` default, and sets the `sandbox_host_machine_type` default. |
| `enable_deployments` | `false` | no | Enable Agent Server hosting (listener, operator, host-backend). Requires the Deployments license entitlement. |
| `enable_agent_builder` | `false` | no | Enable Agent Builder. Requires `enable_deployments = true` and the Agent Builder entitlement. |
| `enable_insights` | `false` | no | Enable Insights (ClickHouse-backed analytics). Requires the Insights entitlement. |
| `enable_polly` | `false` | no | Enable Polly (AI evaluation and monitoring). Requires `enable_deployments = true` and the Polly entitlement. |
| `enable_fleet` | `false` | no | Enable Fleet standalone deployment. Does not require `enable_deployments`. Mutually exclusive with `enable_agent_builder`. Reuses `langsmith_agent_builder_encryption_key` when migrating from `enable_agent_builder`. |
| `enable_standalone_polly` | `false` | no | Enable Polly standalone deployment. Does not require `enable_deployments`. Reuses `langsmith_polly_encryption_key`. |
| `enable_standalone_insights` | `false` | no | Enable Insights standalone deployment. Does not require `enable_deployments`. Reuses `langsmith_insights_encryption_key`. |
| `enable_sso_oidc` | `false` | no | Enable SSO login through a standard OIDC provider and turn off basic auth. `init-values.sh` reads the client ID, client secret, and issuer URL from the `TF_VAR_langsmith_oauth_client_id`, `TF_VAR_langsmith_oauth_client_secret`, and `TF_VAR_langsmith_oauth_issuer_url` variables, which `setup-env.sh` loads from Secret Manager. Enable only after the initial install with basic auth and after you confirm organization admin access, or you lock yourself out of the UI. Not available on chart 0.16. |
| `enable_usage_telemetry` | `false` | no | Enable extended usage telemetry reporting (`PHONE_HOME_USAGE_REPORTING_ENABLED`). |

## SmithDB

SmithDB requires GKE Standard. Terraform rejects `enable_smithdb` on Autopilot, and rejects the migration and query gates unless `smithdb_ingestion_enabled = true`.

| Variable | Default | Required | Description |
| - | - | - | - |
| `enable_smithdb` | `false` | no | Provision the SmithDB dependencies: Cloud SQL metastore, GCS object store, Workload Identity service account, and cache and compute node pools. |
| `smithdb_sizing` | `null` | no | `minimal`, `small`, `medium`, or `large`. `null` follows `sizing_profile`: `minimum` gives `minimal`, `dev` and `default` give `small`, `production` gives `medium`, and `production-large` gives `large`. `minimal` creates no SmithDB node pools and runs on the general node pool. Not available on chart 0.16. |
| `smithdb_cache_storage` | `null` | no | `local-ssd` (Local SSD cache nodes) or `network-disk` (a Hyperdisk Balanced volume per pod on a C3 or C3D cache pool, or `standard-rwo` for `minimal`). `null` gives `network-disk` for `minimal` and `local-ssd` otherwise. A change replaces the cache node pool. Not available on chart 0.16. |
| `smithdb_ingestion_enabled` | `false` | no | Route new writes to SmithDB as well as ClickHouse. Enable only after the SmithDB services pass readiness checks. |
| `smithdb_migration_enabled` | `false` | no | Backfill historical data from ClickHouse. Requires `smithdb_ingestion_enabled`. Also runs an in-chart Postgres for migration task state. On chart 0.16, requires Helm chart version 0.16.6 or later. |
| `smithdb_migration_start_time` | `""` | no | Backfill start time in RFC 3339 format, for example `2026-01-01T00:00:00Z`. Empty keeps the chart default window. Not available on chart 0.16. |
| `smithdb_query_enabled` | `false` | no | Serve UI and API reads from SmithDB. Requires `smithdb_ingestion_enabled`. |
| `smithdb_metastore_source` | `create` | no | `create` (dedicated Cloud SQL instance) or `external` (bring your own, for example AlloyDB behind the Auth Proxy). Must be a dedicated, empty database, never the LangSmith operational Postgres. |
| `smithdb_metastore_database_version` | `POSTGRES_18` | no | Cloud SQL version for the metastore. SmithDB requires PostgreSQL 18 or later. |
| `smithdb_metastore_tier` | `null` | no | Cloud SQL machine tier for a created metastore. `null` follows `smithdb_sizing`: `db-custom-2-8192` for `minimal`, `db-custom-4-16384` for `small`, `db-custom-6-32768` for `medium`, and `db-custom-10-65536` for `large`. On chart 0.16, the default is `db-custom-2-8192`. |
| `smithdb_metastore_disk_size` | `50` | no | Metastore disk size in GB. Autoresize is on, so this is a floor. |
| `smithdb_metastore_high_availability` | `false` | no | Run the metastore as a regional (HA) Cloud SQL instance. |
| `smithdb_metastore_deletion_protection` | `true` | no | Prevent deletion of the metastore from Terraform and from the Cloud SQL API. Set `false` and apply that change before running destroy. |
| `smithdb_metastore_ssl_mode` | `ENCRYPTED_ONLY` | no | Cloud SQL SSL enforcement for the metastore. |
| `smithdb_metastore_use_ssl` | `null` | no | Connect to the metastore over TLS directly. `null` resolves to the opposite of `smithdb_metastore_use_auth_proxy`. Must be `false` with the Auth Proxy. On chart 0.16, the default is `true`. |
| `smithdb_metastore_use_auth_proxy` | `null` | no | Run a Cloud SQL Auth Proxy sidecar in every SmithDB Pod. `null` resolves to `true` for `smithdb_metastore_source = "create"` and `false` for `external`. Requires `smithdb_metastore_source = "create"` and `smithdb_metastore_use_ssl = false`. On chart 0.16, the default is `false`. |
| `smithdb_auth_proxy_image` | `gcr.io/cloud-sql-connectors/cloud-sql-proxy:2.25.0` | no | Cloud SQL Auth Proxy image for the sidecar. Pin an exact tag. |
| `smithdb_metastore_master_username` | `smithdb` | no | Master username for the metastore. |
| `smithdb_metastore_master_password` | `null` | no | Master password for the metastore. `null` auto-generates one. Set with `TF_VAR_smithdb_metastore_master_password`. |
| `smithdb_external_metastore_host` | `null` | when `external` | Host of an existing Postgres instance for the metastore. Use `127.0.0.1` when fronting AlloyDB with the Auth Proxy sidecar. |
| `smithdb_external_metastore_port` | `5432` | no | Port of the existing metastore. |
| `smithdb_external_metastore_database` | `smithdb` | no | Database name on the existing metastore. |
| `smithdb_external_metastore_username` | `null` | when `external` | Username for the existing metastore. |
| `smithdb_external_metastore_password` | `null` | no | Password for the existing metastore. Empty when using AlloyDB IAM database authentication. Set with `TF_VAR_smithdb_external_metastore_password`. |
| `smithdb_bucket_name` | `""` | no | Object-store bucket name. Empty auto-generates one. Use a single-region bucket. |
| `smithdb_bucket_kms_key` | `""` | no | Cloud KMS key for CMEK on the bucket. Empty uses Google-managed encryption. |
| `smithdb_bucket_versioning_enabled` | `false` | no | Enable object versioning on the bucket. |
| `smithdb_bucket_force_destroy` | `false` | no | Allow Terraform to delete a non-empty bucket on destroy. Set `true` only for test stacks. |
| `smithdb_service_account_email` | `null` | no | Existing service account for the SmithDB pods. `null` creates a dedicated least-privilege one. |
| `smithdb_node_locations` | `[]` | no | Zones for the SmithDB node pools. Empty uses every zone in the region; pin this after verifying machine type and Local SSD availability. |
| `smithdb_instance_store_machine_type` | `null` | no | Machine type for the cache pool. `null` follows the size and cache mode: `n2-standard-16`, `n2-standard-32`, or `n2-standard-64` for `local-ssd`, and `c3-standard-22`, `c3-standard-44`, or `c3-standard-88` for `network-disk`, for `small`, `medium`, and `large`. `network-disk` requires a C3 or C3D type. On chart 0.16, the default is `n2-standard-16`. |
| `smithdb_instance_store_local_ssd_count` | `null` | no | Local SSDs per cache node. Each disk holds 375 GB. `null` gives `2`, `4`, or `8` for `small`, `medium`, and `large` with `local-ssd`, and `0` for `network-disk`. Compute Engine accepts only specific counts per machine type. Set `0` for `-lssd` machine types that bundle their disks. On chart 0.16, the default is `2`. |
| `smithdb_instance_store_disk_size` | `null` | no | Boot disk size in GB for cache pool nodes. `null` gives `100` for `local-ssd` and `300` for `network-disk`. `network-disk` with the backfill requires at least `300`. On chart 0.16, the default is `100`. |
| `smithdb_instance_store_min_nodes` | `0` | no | Minimum cache pool nodes per zone. `0` lets the pool scale to zero. |
| `smithdb_instance_store_max_nodes` | `3` | no | Maximum cache pool nodes per zone. |
| `smithdb_compute_machine_type` | `null` | no | Machine type for the compute pool (compaction, cluster manager, backfill task database). `null` gives `n2-standard-8` for `small` and `medium`, and `n2-standard-16` for `large`. On chart 0.16, the default is `n2-standard-8`. |
| `smithdb_compute_disk_size` | `100` | no | Boot disk size in GB for compute pool nodes. |
| `smithdb_compute_min_nodes` | `0` | no | Minimum compute pool nodes per zone. |
| `smithdb_compute_max_nodes` | `3` | no | Maximum compute pool nodes per zone. |

## Sandboxes

Sandboxes require GKE Standard and `enable_gcp_iam_module = true`.

| Variable | Default | Required | Description |
| - | - | - | - |
| `enable_sandboxes` | `false` | no | Provision the infrastructure for LangSmith Sandboxes. Requires Standard GKE, external Redis, Workload Identity, and sandbox-host nodes with usable Linux KVM (`/dev/kvm`). |
| `sandbox_host_image_tag` | `""` | no | Deprecated and ignored; remove it from `terraform.tfvars`. The deploy script sets the sandbox-host image tag from the chart's app version. On chart 0.16, required when sandboxes are enabled, and `init-values.sh` exits without it. |
| `sandbox_service_url_base_url` | `""` | no | Base URL for service URLs of HTTP services running inside sandboxes. Requires wildcard DNS and TLS for the host when set. |
| `platform_backend_component_label` | `langsmith-platform-backend` | no | Component label of the platform-backend pods, excluded from the default-deny network policy so the sandbox host can reach them. Set to `<release-name>-platform-backend` if your Helm release is not named `langsmith`. |
| `sandbox_host_machine_type` | `null` | no | Machine type for sandbox-host nodes. Must support nested virtualization. `null` follows `sizing_profile`: `n2-standard-32` for `production` and `production-large`, `n2-standard-8` otherwise. C4 types are not supported, because the pool uses a pd-ssd boot disk. On chart 0.16, the default is `n2-standard-8`. |
| `sandbox_host_node_count` | `1` | no | Initial sandbox-host nodes per zone. |
| `sandbox_host_min_node_count` | `0` | no | Minimum sandbox-host nodes per zone. `0` lets the autoscaler keep only the nodes sandbox-host needs. On chart 0.16, the default is `1`. |
| `sandbox_host_max_node_count` | `5` | no | Maximum sandbox-host nodes per zone. |
| `sandbox_host_disk_size_gb` | `200` | no | Boot disk size in GB for sandbox-host nodes. |
| `sandbox_host_ephemeral_local_ssd_count` | `0` | no | Local SSDs backing kubelet and container runtime ephemeral storage on sandbox-host nodes. The JuiceFS cache stays on the boot disk, so these disks do not speed up sandbox file I/O. Accepts `0`, `1`, `2`, `4`, `8`, `16`, or `24`, subject to the machine type. On chart 0.16, any non-negative integer is accepted. |
| `sandbox_default_container_requests` | `{ cpu = "100m", memory = "128Mi" }` | no | Default requests injected into sandbox containers that omit them. |
| `sandbox_juicefs_name` | `sandbox-juicefs` | no | JuiceFS volume name for sandbox snapshots and filesystem state. |
| `sandbox_juicefs_redis_memory_size` | `5` | no | Memory in GB for the dedicated JuiceFS metadata Memorystore instance. |
| `sandbox_juicefs_redis_high_availability` | `true` | no | Use the Standard HA tier for the JuiceFS metadata Redis. |
| `sandbox_juicefs_redis_prevent_destroy` | `false` | no | Prevent Terraform from destroying the JuiceFS metadata Redis. |
| `sandbox_juicefs_redis_rdb_snapshot_period` | `null` | no | RDB snapshot period for the JuiceFS metadata Redis, for example `ONE_HOUR`. `null` disables RDB persistence. |
| `sandbox_juicefs_csi_config_secret_name` | `juicefs-csi-config` | no | Kubernetes Secret holding the sandbox JuiceFS configuration, passed to the chart as `sandboxes.juicefs.existingSecretName`. On chart 0.16, passed as `sandboxes.juicefs.csi.existingSecretName`. |
| `sandbox_juicefs_csi_config_secret_revision` | `1` | no | Increment to rewrite the JuiceFS configuration Secret. The chart does not restart sandbox-host after the rewrite, so restart it after the apply. |

## Sensitive values (set with `setup-env.sh`)

Sourcing `infra/scripts/setup-env.sh` writes these to Google Secret Manager as `langsmith-<name_prefix>-<environment>-<key>` and exports them as `TF_VAR_*` variables in the current shell. Never set these inline in `terraform.tfvars`. `make deploy` also reads the initial admin email from the `LANGSMITH_ADMIN_EMAIL` environment variable, which `setup-env.sh` does not set.

| Variable | Description |
| - | - |
| `postgres_password` | Cloud SQL password. Prompted. |
| `langsmith_license_key` | LangSmith enterprise license key. Prompted. |
| `langsmith_admin_password` | Initial org admin password. Prompted. At least 12 characters with a lowercase letter, an uppercase letter, and a symbol. |
| `langsmith_api_key_salt` | Salt for hashing API keys. Must stay stable after first deploy. |
| `langsmith_jwt_secret` | JWT secret for Basic Auth sessions. Must stay stable. |
| `langsmith_deployments_encryption_key` | Fernet key for Agent Server hosting. Must never change. |
| `langsmith_agent_builder_encryption_key` | Fernet key for Agent Builder. Must never change. |
| `langsmith_insights_encryption_key` | Fernet key for Insights. Must never change. |
| `langsmith_polly_encryption_key` | Fernet key for Polly. Must never change. |
| `sandbox_callback_signing_jwk` | Sandbox callback signing key. Generated only when `enable_sandboxes = true`. Keep stable. |

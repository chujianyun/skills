# Deploy LangSmith with Terraform

> Provision LangSmith self-hosted on AWS, Azure, or GCP using LangChain's production-ready Terraform modules.

> [!NOTE]
>
> Self-hosted LangSmith is an add-on to the Enterprise plan designed for LangChain's largest, most security-conscious customers. See [pricing](https://www.langchain.com/pricing) for details, or [contact the LangChain sales team](https://www.langchain.com/contact-sales) to request a license key for trial.

LangChain publishes production-ready Terraform modules for [LangSmith self-hosted](../Self-hosted%20LangSmith.md) at [github.com/langchain-ai/terraform](https://github.com/langchain-ai/terraform). The modules provision the cloud foundation (network, cluster, database, cache, object storage, secrets, DNS) and install the LangSmith Helm chart with sensible defaults.

Use this path when you want infrastructure as code from day one. If you already manage cloud infrastructure with your own tooling and need only the application install, follow the [Helm installation guide](../Install%20an%20instance/Self-host%20LangSmith%20on%20Kubernetes.md) instead.

Each module release tag deploys one Helm chart line: the `v0.17.*` tags deploy chart 0.17, and the `v0.16.*` tags deploy chart 0.16. Check out the tag for the chart line you want before you configure the module.

> [!TIP]
>
> **Prefer Helm?** The [Kubernetes setup guide](../Install%20an%20instance/Self-host%20LangSmith%20on%20Kubernetes.md) walks through installing with Helm against any conformant cluster, no Terraform required. The Terraform path bundles cluster provisioning, secrets wiring, and the Helm release into one workflow.

## Choose a provider

> [card] [AWS (EKS)](AWS/Deploy%20LangSmith%20on%20AWS%20with%20Terraform.md)
>
> Provision EKS, RDS PostgreSQL, ElastiCache, S3, and networking.

> [card] [Azure (AKS)](Azure/Deploy%20LangSmith%20on%20Azure%20with%20Terraform.md)
>
> Provision AKS, Azure Database for PostgreSQL, Azure Managed Redis, Blob Storage, and Key Vault.

> [card] [GCP (GKE)](GCP/Deploy%20LangSmith%20on%20GCP%20with%20Terraform.md)
>
> Provision GKE, Cloud SQL, Memorystore, GCS, and Workload Identity.

## Prerequisites

Install the following tools before running the modules:

| Tool | Version | Purpose |
| - | - | - |
| `terraform` | 1.11 or later | Run the modules |
| `kubectl` | 1.34 or later | Inspect the cluster after provisioning |
| `helm` | 3.12 or later | Manage the LangSmith chart release |
| Cloud CLI | latest | `aws`, `az`, or `gcloud` for the target provider |

You also need:

* A LangSmith license key. [Contact the LangChain sales team](https://www.langchain.com/contact-sales) to request one.
* Permissions in the target cloud account to create VPC or VNet networking, a managed Kubernetes cluster, managed databases, object storage, secrets, and IAM roles.
* A registered domain (or subdomain) for the LangSmith UI endpoint. GCP needs one, set as `langsmith_domain`. It is optional on AWS, which can serve LangSmith on the load balancer hostname, and on Azure, which can serve it on a `dns_label` hostname with any ingress controller except `none`. With AGIC, a `dns_label` hostname serves HTTP only.

## Deployment tiers

Each tier is a combination of settings in `terraform.tfvars`: `postgres_source`, `redis_source`, and `clickhouse_source` place each data store in the cluster or in a managed service, and `sizing_profile` sizes the workloads.

| Tier | PostgreSQL | Redis | ClickHouse | Use case |
| - | - | - | - | - |
| `dev` | In-cluster | In-cluster | In-cluster | Demos, evaluations, short-lived POCs |
| `production` | Cloud-managed (RDS, Cloud SQL, Azure Database for PostgreSQL) | Cloud-managed (ElastiCache, Memorystore, Azure Managed Redis) | [LangChain Managed ClickHouse](../Connect%20external%20services/LangSmith-managed%20ClickHouse.md) | Persistent, scalable production |
| `production-large` | Cloud-managed, larger instance class | Cloud-managed, larger instance class | LangChain Managed ClickHouse | High-throughput production |

On AWS and Azure, start from the `terraform.tfvars.example`, `terraform.tfvars.minimum`, `terraform.tfvars.dev`, or `terraform.tfvars.production` template. On GCP, start from `terraform.tfvars.example` or `terraform.tfvars.minimum`. The templates do not map one-to-one to these tiers: every template keeps ClickHouse in-cluster, and the dev templates use managed PostgreSQL and Redis. After copying one, set the three `*_source` values and `sizing_profile` to match the tier you want.

> [!WARNING]
>
> Use in-cluster ClickHouse for development and POC, not production. Production deployments must use [LangChain Managed ClickHouse](../Connect%20external%20services/LangSmith-managed%20ClickHouse.md) or a self-managed external ClickHouse cluster. Blob storage is always required because trace payloads must not live in ClickHouse.

## What the modules provision

* **Networking:** VPC or VNet with public and private subnets, NAT, and security groups.
* **Compute:** Managed Kubernetes (EKS, AKS, or GKE) with autoscaling node pools sized per tier.
* **Data plane:** Managed or in-cluster PostgreSQL and Redis, and a blob storage bucket for trace payloads.
* **Secrets:** Each module keeps application secrets in the cloud's secret store, then writes them into Kubernetes its own way. On AWS, [External Secrets Operator](https://external-secrets.io/) syncs them from SSM Parameter Store. On GCP, `setup-env.sh` stores them in Secret Manager, Terraform writes the Kubernetes Secrets, and `make deploy` builds the `langsmith-config` Secret. On Azure, `secrets.auto.tfvars` holds the Terraform inputs, Key Vault holds the application secrets, and `make k8s-secrets` copies them into the `langsmith-config-secret` Kubernetes Secret.
* **Ingress:** Envoy Gateway (Gateway API) is the default on every provider. On AWS, an ALB forwards to it, and NGINX, Istio, or ALB Ingress alone are options. On Azure, NGINX, self-managed Istio, the AKS Istio add-on, and Application Gateway Ingress Controller (AGIC) are options. On GCP, Envoy Gateway is the only implemented option.
* **Optional hardening:** On AWS, AWS Network Firewall with FQDN egress allowlists, WAFv2, CloudTrail, and a private EKS API endpoint with SSM bastion access. On Azure, a WAF policy (OWASP 3.2 plus bot protection, attached to Application Gateway with AGIC), Azure Monitor diagnostic settings, a jump VM, a private AKS API server with Entra-only access, and private endpoints for Blob Storage and Key Vault. On GCP, `gke_master_authorized_cidrs` limits which CIDRs can reach the GKE control plane.

## Enterprise feature toggles

Each module exposes flags for the optional LangSmith add-ons. Toggle each in `terraform.tfvars`. Each module's deploy scripts read the flags and generate the matching Helm values.

* **[Agent Server hosting](../Install%20an%20instance/Additional%20features/Enable%20Agent%20Server%20hosting.md)** (`enable_deployments`): Agent Server plus the host-backend, listener, and operator that run and manage deployed agents.
* **[Fleet](../../../Additional%20documentation/No-code%20agents%20with%20LangSmith%20Fleet.md)** (`enable_fleet`): The agent-building product, formerly Agent Builder, deployed as a standalone service.
* **Insights** (`enable_insights`): ClickHouse-backed analytics.
* **Polly** (`enable_polly`): AI evaluation and monitoring.
* **[LLM Gateway](../../../LLM%20Gateway/Get%20started/LLM%20Gateway.md)** (`enable_llm_gateway`): One LangSmith API key for models across the providers your organization configures, in beta. `enable_gateway_pii_redaction` adds PII redaction.
* **[SSO with OIDC](../Platform%20auth%20%26%20access%20control/Set%20up%20SSO%20with%20OAuth2.0%20and%20OIDC.md)** (`enable_sso_oidc`): Log in through a standard OIDC provider instead of basic auth. Enable it only after you have logged in as the org admin with basic auth, because the flag disables basic auth.

> [!NOTE]
>
> Run `make init-values && make deploy` to apply a flag change. `enable_fleet` also creates Terraform resources, so run `make apply` first. Fleet replaces the legacy `enable_agent_builder` flag, and its prerequisites differ by provider. See the Fleet section of the [AWS](AWS/Deploy%20LangSmith%20on%20AWS%20with%20Terraform.md#fleet), [GCP](GCP/Deploy%20LangSmith%20on%20GCP%20with%20Terraform.md#fleet), or [Azure](Azure/Deploy%20LangSmith%20on%20Azure%20with%20Terraform.md#fleet) deploy guide.
>
> `enable_sso_oidc` is available in all three modules on the `v0.17.*` tags, and in the AWS module from v0.16.83. The LLM Gateway flags are available only in the Azure module, on the `v0.17.*` tags.

## Next steps

* Pick a provider above and follow the deployment guide.
* Review [required dependency versions](../Install%20an%20instance/Minimum%20versions%20for%20self-hosting%20dependencies.md) for PostgreSQL, ClickHouse, Redis, and Kubernetes.
* Plan capacity with the [scaling guide](../Configure%20an%20instance/Configure%20LangSmith%20for%20scale.md).
* After the application is running, enable [Agent Server hosting](../Install%20an%20instance/Additional%20features/Enable%20Agent%20Server%20hosting.md) to add agent deployment and management to the UI.

# Deploy LangSmith on AWS with Terraform

> End-to-end walkthrough for provisioning LangSmith self-hosted on AWS EKS using the LangChain Terraform modules.

Deploy LangSmith to AWS with the public [Terraform modules](https://github.com/langchain-ai/terraform/tree/main/modules/aws). Managing the deployment as code lets you version, review, and reproduce your LangSmith environment across accounts instead of clicking through the AWS Console.

The install runs in two stages:

1. **Infrastructure**: Terraform provisions VPC, EKS, RDS, ElastiCache, S3, the ALB, and IAM, then bootstraps the cluster add-ons.
2. **Application**: Helm installs the LangSmith chart against the cluster.

After the base install, enable optional add-ons by setting flags and redeploying.

```mermaid actions={false}
%%{init: {'flowchart': {'nodeSpacing': 25, 'rankSpacing': 30}}}%%
graph TB
    subgraph stage1["Set up infrastructure"]
        direction LR
        Start["source setup-env.sh<br/>secrets to SSM"]
        TF["make apply"]
        Infra["VPC · EKS · RDS<br/>ElastiCache · S3 · ALB<br/>IAM"]
        Bootstrap["k8s-bootstrap<br/>ESO · KEDA<br/>Envoy Gateway"]
        Start --> TF --> Infra -->|EKS ready| Bootstrap
    end
    subgraph stage2["Deploy the application"]
        direction LR
        Deploy["make init-values<br/>+ make deploy"]
        Helm["helm upgrade --install<br/>ESO syncs secrets"]
        Running["LangSmith running<br/>all pods healthy"]
        Deploy --> Helm --> Running
    end
    stage1 --> stage2

    classDef trigger fill:#F6FFDB,stroke:#6E8900,stroke-width:2px,color:#2E3900
    classDef process fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710
    classDef neutral fill:#F2FAFF,stroke:#40668D,stroke-width:2px,color:#2F4B68
    classDef output fill:#EBD0F0,stroke:#885270,stroke-width:2px,color:#441E33

    class Start trigger
    class TF,Bootstrap,Deploy,Helm process
    class Infra neutral
    class Running output

    style stage1 fill:none,stroke:#40668D,stroke-width:1px
    style stage2 fill:none,stroke:#40668D,stroke-width:1px
```

## Prerequisites

### Required tools

| Tool | Version | Purpose |
| - | - | - |
| AWS CLI | v2 | Authenticate, query AWS resources, manage EKS kubeconfig |
| Terraform | 1.11 or later | Run the infrastructure modules |
| `kubectl` | 1.34 or later | Inspect the EKS cluster |
| Helm | 3.12 or later | Install and manage the LangSmith chart |
| `eksctl` | latest | Optional, handy for kubeconfig and debugging |

Install on macOS:

```bash
brew install awscli kubectl helm eksctl
brew tap hashicorp/tap && brew install hashicorp/tap/terraform
```

Verify each tool is on `PATH`:

```bash
aws --version
terraform version
kubectl version --client
helm version
```

For Linux, follow the [AWS CLI install guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) and use your distribution's package manager for the remaining tools.

### Required AWS IAM permissions

The IAM user or role running Terraform needs `AdministratorAccess`, or `PowerUserAccess` plus `IAMFullAccess`. The module creates IAM roles and policies for IRSA, so `PowerUserAccess` alone is not enough. For a scoped-down policy, refer to [`PERMISSIONS.md`](https://github.com/langchain-ai/terraform/blob/main/modules/aws/PERMISSIONS.md) in the module.

> [!TIP]
>
> Run `make preflight` from `modules/aws/` after you authenticate and create `infra/terraform.tfvars` (see [Clone and configure](#clone-and-configure)). The read-only checks confirm the CLI tools, the `tfvars` file, the active credentials, and the region, then probe read access to each AWS service the module uses. To also test that the credentials can create resources, run `make preflight ARGS="--create-test-resources"`.

### Authenticate

Configure AWS credentials with the CLI:

```bash
aws configure
```

Or export environment variables:

```bash
export AWS_ACCESS_KEY_ID="..."
export AWS_SECRET_ACCESS_KEY="..."
export AWS_DEFAULT_REGION="us-west-2"
```

Confirm the credentials work and the target region is enabled in the account:

```bash
aws sts get-caller-identity
aws ec2 describe-availability-zones --query 'AvailabilityZones[].ZoneName' --output table
```

### License key and domain

* **LangSmith license key.** [Contact the LangChain sales team](https://www.langchain.com/contact-sales) to request one. The setup script stores the key in AWS SSM Parameter Store, not in `tfvars`.
* **Domain (optional).** Set `langsmith_domain` to serve LangSmith on your own hostname. With a domain and no `acm_certificate_arn`, Terraform creates a Route 53 hosted zone, requests an ACM certificate, and creates the ALB alias record. To use an existing hosted zone instead, set `dns_create_zone = false` and `dns_existing_zone_id`. To bring your own certificate, set `acm_certificate_arn`. Leave `langsmith_domain` empty to reach LangSmith on the ALB hostname. Without a domain, set `tls_certificate_source = "none"` to serve plain HTTP. An `acm_certificate_arn` also works without a domain, but `make preflight-post` then fails its TLS check because `acm` expects `langsmith_domain`.

### Cluster sizing reference

Two independent settings control capacity:

* **Infrastructure capacity** sets instance types and node counts directly through the infra variables `eks_managed_node_groups`, `postgres_instance_type`, and `redis_instance_type`. The module defaults are one `m5.4xlarge` node group (min 3, max 10), `db.t3.large` for RDS, and `cache.m6g.xlarge` for ElastiCache. The `infra/terraform.tfvars.dev`, `terraform.tfvars.minimum`, and `terraform.tfvars.production` templates set smaller or larger values.
* **`sizing_profile`** selects the Helm sizing overlay (pod resource requests and limits). `init-values.sh` and `deploy.sh` read it; Terraform does not.

Size the infrastructure for your target tier before deploying. For per-tier recommendations, refer to [Scaling guidance](../../Configure%20an%20instance/Configure%20LangSmith%20for%20scale.md).

> [!NOTE]
>
> For production workloads, also plan to provision external [LangChain Managed ClickHouse](../../Connect%20external%20services/LangSmith-managed%20ClickHouse.md) or a self-managed external ClickHouse cluster. In-cluster ClickHouse is supported for dev/POC only.

## Quickstart

> [!TIP]
>
> For a condensed cheat sheet of `make` targets, required variables, and common constraints, see the [AWS quick reference](AWS%20Terraform%20quick%20reference.md).

For the fastest path from zero to a running LangSmith instance, run these commands in order:

```bash
# 1. Clone the public modules
git clone https://github.com/langchain-ai/terraform.git
cd terraform/modules/aws

# 2. Generate terraform.tfvars interactively (Enter accepts current values)
make quickstart

# 3. Load secrets into SSM Parameter Store
#    Must be sourced, not executed
source infra/scripts/setup-env.sh

# 4. Provision infrastructure
make init
make plan
make apply

# 5. Configure kubectl
source infra/scripts/set-kubeconfig.sh
kubectl get nodes

# 6. Deploy LangSmith with Helm
make init-values
make deploy

# 7. Confirm
kubectl get pods -n langsmith
kubectl get httproute -n langsmith
```

`make deploy` prints the LangSmith URL when it finishes.

To chain infrastructure and application in one command, first run `make quickstart` and `source infra/scripts/setup-env.sh` in the same shell, then:

```bash
make quickdeploy          # interactive, prompts before terraform apply
make quickdeploy-auto     # non-interactive, auto-approves terraform
```

`make quickdeploy` first checks that the `setup-env.sh` exports are loaded and that `infra/terraform.tfvars` exists, and stops with the command to run if either is missing. It runs `terraform init` if `infra/.terraform/` does not exist, then runs `terraform apply`, sources `set-kubeconfig.sh`, and runs `init-values` and `deploy.sh`. If `terraform apply` fails, fix the issue and re-run `make quickdeploy`. If a later step fails, the command prints the `make` target to retry.

The following sections cover each stage in detail.

## Provision infrastructure

Terraform provisions the following AWS resources:

| Resource | Purpose |
| - | - |
| VPC + subnets + NAT | Private network for the cluster and managed services |
| EKS cluster + node groups | Kubernetes compute |
| RDS PostgreSQL | LangSmith operational data |
| ElastiCache Redis | Queue and cache |
| S3 bucket + VPC endpoint | Trace payload blob storage |
| ALB + listeners | Entry point; terminates TLS with `acm` |
| IRSA roles + IAM policies | Per-service AWS access |
| KEDA, External Secrets Operator, Envoy Gateway | Bootstrap workloads installed alongside infrastructure. Envoy Gateway is the default ingress. cert-manager is added only for Let's Encrypt. |

Application secrets live in SSM Parameter Store. `setup-env.sh` writes them, not Terraform, and External Secrets Operator syncs them into the cluster.

### Clone and configure

```bash
git clone https://github.com/langchain-ai/terraform.git
cd terraform/modules/aws
```

The `main` branch and `v0.17.*` release tags deploy LangSmith Helm chart v17, which this guide describes.

> [!NOTE]
>
> To stay on chart v16, run `git checkout release/0.16` or check out a `v0.16.*` tag. Callouts in this guide mark where chart v16 differs.

All subsequent commands run from `modules/aws/`. Run `make help` for the full target list.

Generate `terraform.tfvars` with the interactive wizard:

```bash
make quickstart
```

The wizard walks through 13 sections, including naming, region, networking, EKS sizing, data sources, TLS and DNS, ingress, and the optional add-on flags. It writes `infra/terraform.tfvars`. When the file already exists, the wizard offers to update it with the existing values preselected, start fresh, or cancel, and it backs up the original file first. Some settings, such as the bring-your-own security group variables (`*_existing_security_group_id`), are not in the wizard; set them in `terraform.tfvars` by hand. When the wizard updates an existing file, it drops hand-written settings like these, so restore them from `infra/terraform.tfvars.backup`.

Prefer to edit by hand? Copy the example and fill in the required fields:

```bash
cp infra/terraform.tfvars.example infra/terraform.tfvars
vi infra/terraform.tfvars
```

The minimum required variables:

```hcl
name_prefix = "acme"
environment = "prod"
region      = "us-west-2"

eks_cluster_version = "1.34"
eks_managed_node_groups = {
  default = {
    name           = "node-group-default"
    instance_types = ["m5.4xlarge"]
    min_size       = 3
    max_size       = 10
  }
}

postgres_source = "external"
redis_source    = "external"

tls_certificate_source = "acm"
langsmith_domain       = "langsmith.example.com"
# dns_create_zone      = false                    # write records into a zone that already resolves
# dns_existing_zone_id = "<hosted-zone-id>"
# acm_certificate_arn  = "arn:aws:acm:us-west-2:<account-id>:certificate/<cert-id>"  # optional with a domain
```

> [!NOTE]
>
> With a domain and no `acm_certificate_arn`, Terraform requests an ACM certificate, and `make apply` waits until DNS validation succeeds. With `dns_create_zone = true` (the default), Terraform creates a new hosted zone for `langsmith_domain`, and validation succeeds only after you delegate that zone's NS records from the parent domain. To validate in a zone that already resolves, set `dns_create_zone = false` and `dns_existing_zone_id`. To deploy before the delegation is in place, follow the staged deploy pattern in [Auto-provisioned DNS](AWS%20Terraform%20architecture.md#auto-provisioned-dns).

See the [AWS variables reference](AWS%20Terraform%20variables%20reference.md) for every input variable.

> [!TIP]
>
> Configure a remote state backend before applying. Copy `infra/backend.tf.example` to `infra/backend.tf` and set the S3 bucket, key, region, and DynamoDB lock table. Without it, Terraform keeps state locally.

### Load secrets into SSM Parameter Store

```bash
source infra/scripts/setup-env.sh
```

The script reads `terraform.tfvars`, derives the SSM path `/langsmith/{name_prefix}-{environment}/`, then for each secret either reuses an exported value, reads the existing SSM parameter, auto-generates one, or prompts you. You supply three values interactively: the license key, the admin password, and the admin email. The script must be sourced (not executed) because `make` cannot export environment variables back to the parent shell.

The script manages the following SSM parameters:

| SSM key | How it is set | Notes |
| - | - | - |
| `postgres-password` | Auto-generated (`openssl rand -hex 32`) | RDS master password |
| `redis-auth-token` | Auto-generated (hex) | ElastiCache auth token |
| `sandbox-juicefs-redis-auth-token` | Auto-generated (hex) | Only when `enable_sandboxes = true` |
| `langsmith-api-key-salt` | Auto-generated (`openssl rand -base64 32`) | Never rotate, breaks all API keys |
| `langsmith-jwt-secret` | Auto-generated (`openssl rand -base64 32`) | Never rotate, invalidates all sessions |
| `sandbox-callback-signing-jwk` | Auto-generated Ed25519 key | Only when `enable_sandboxes = true` |
| `langsmith-license-key` | Prompt | From [the LangChain sales team](https://www.langchain.com/contact-sales) |
| `langsmith-admin-password` | Prompt | At least 12 characters, with lowercase, uppercase, and a symbol |
| `langsmith-admin-email` | Prompt | Initial organization admin |
| `deployments-encryption-key` | Auto-generated Fernet key | Agent Server hosting add-on |
| `agent-builder-encryption-key` | Auto-generated Fernet key | Used by Fleet; the name predates the rename |
| `insights-encryption-key` | Auto-generated Fernet key | Insights add-on |
| `polly-encryption-key` | Auto-generated Fernet key | LangSmith Chat (formerly Polly) add-on |

If you turn on `enable_sandboxes` later, source `setup-env.sh` again before `make apply` so it creates the sandbox secrets.

Verify the secrets are present and the `TF_VAR_*` environment variables are exported:

```bash
make secrets
```

### Apply

```bash
make init
make plan
make apply
```

`make plan` shows the proposed diff. Review the output before applying. `make apply` runs a single `terraform apply` across all modules; Terraform orders the resources by dependency. Pass `ARGS="-auto-approve"` to skip the confirmation prompt.

### Configure kubectl

```bash
source infra/scripts/set-kubeconfig.sh
kubectl get nodes
kubectl get pods -A
```

`set-kubeconfig.sh` writes a dedicated `~/.kube/langsmith-<cluster>` file and exports `KUBECONFIG`, so it leaves `~/.kube/config` untouched. `make kubeconfig` only prints this command.

All nodes should report `Ready`. The core add-ons should be `Running`: CoreDNS, kube-proxy, and the VPC CNI in `kube-system`, KEDA in `keda`, External Secrets Operator in `external-secrets`, and Envoy Gateway in `envoy-gateway-system`. cert-manager runs only when `tls_certificate_source = "letsencrypt"` or `create_cert_manager_irsa = true`.

## Deploy LangSmith

```bash
make init-values
make deploy
```

`make init-values` reads `sizing_profile` and the `enable_*` flags from `terraform.tfvars`, writes `helm/values/langsmith-values-overrides.yaml` from the Terraform outputs, and copies the matching values files from `helm/values/examples/` into `helm/values/`. It reuses the admin email from the existing overrides file, or takes it from `LANGSMITH_ADMIN_EMAIL` (set by `setup-env.sh`), or prompts for it. On re-runs it refreshes the Terraform outputs and copies an add-on values file only when it is missing, so your edits to existing files survive.

`make deploy` runs `helm/scripts/deploy.sh`, which:

1. Resolves the chart version and confirms it is on the v17 line.
2. Refreshes the kubeconfig with `aws eks update-kubeconfig`.
3. Runs preflight checks (AWS credentials, cluster reachability, the `langchain` Helm repo).
4. Applies the External Secrets Operator `ClusterSecretStore` and `ExternalSecret` so the cluster reads secrets directly from SSM.
5. Runs `helm upgrade --install` with the layered values files and waits for the core pods.
6. Upgrades once more when no `langsmith_domain` is set and the load balancer hostname changed, then prints the LangSmith URL.

### Pin the chart version

`deploy.sh` installs the latest patch on the LangSmith Helm chart v17 line (`~0.17.0`) by default. To pin an exact patch, set `langsmith_helm_chart_version = "0.17.x"` in `terraform.tfvars`, or run `CHART_VERSION=0.17.x make deploy`. The environment variable wins over the `tfvars` setting. `deploy.sh` rejects versions off the v17 line, and Terraform validation rejects a `langsmith_helm_chart_version` off that line at plan time. `deploy.sh` also rejects values files that still use chart v15 keys (`config.insights`, `config.polly`, `backend.agentBootstrap`).

> [!NOTE]
>
> On chart v16, use a `v0.16.*` module release or the `release/0.16` branch. Those releases pin `~0.16.0` and accept only `0.16.x` versions. To move an existing chart v16 deployment to v17, follow [Upgrade from chart v16 to v17](#upgrade-from-chart-v16-to-v17).

### Verify

```bash
kubectl get pods -n langsmith
kubectl get httproute -n langsmith
```

When all pods are `Running`, open the URL that `make deploy` printed. It uses `langsmith_domain` when set, or the ALB hostname. Run `make status` at any time for a summary of every layer and the next step to run.

### Upgrade from chart v16 to v17

> [!WARNING]
>
> Downgrading from chart v17 to v16 is not supported. Back up the database before you upgrade.

A deployment with `enable_sandboxes = false` and `enable_smithdb = false` only moves the chart pin. Sandboxes and SmithDB need the extra steps below. The module sets no Engine values, so if you enabled Engine in your own values overrides, also apply the Engine change in [Upgrade from v16 to v17](../../Manage%20an%20instance/Upgrade%20an%20installation.md#upgrade-from-v16-to-v17).

1. Check out a `v0.17.*` tag, or pull `main`.
2. If `terraform.tfvars` pins `langsmith_helm_chart_version` to a `0.16.x` patch, clear it or set a `0.17.x` patch, and run `unset CHART_VERSION` if your shell sets it. Terraform validation rejects a `0.16.x` pin at plan time, and `deploy.sh` rejects a `0.16.x` value in `CHART_VERSION`.
3. Run `make apply`. From module release `v0.16.83` or later, the v17 module changes no AWS resources, so Terraform reports no infrastructure changes. From an earlier `v0.16.*` release, review `make plan` before you apply.
4. Run `make init-values`. It rewrites `langsmith-values-overrides.yaml` in the chart v17 sandbox schema.
5. With `enable_smithdb = true`, update the SmithDB keys in the values files that `make init-values` does not overwrite. Chart v17 fails to render the old keys:

   * In `helm/values/langsmith-values-smithdb.yaml`, rename `smithdb.migration.deployment` to `smithdb.migration.job`.
   * In `helm/values/langsmith-values-sizing-*.yaml`, move `smithdb.query.autoscaling.*`, `smithdb.ingestion.autoscaling.*`, and `smithdb.compactionWorker.autoscaling.*` under `autoscaling.hpa.*`. In `langsmith-values-sizing-production-large.yaml`, rename the `local-ssd-storage` volume to `cache`.

   If you have not customized these files, delete them and re-run `make init-values` to copy the v17 versions instead. For the chart changes behind these keys, see [Cache storage](../../SmithDB/Install%20SmithDB/Prepare%20SmithDB%20supporting%20infrastructure.md#cache-storage).

   Only the `production-large` sizing file defines a `cache` volume. With the `dev`, `minimum`, or `production` profile, chart v17 gives each SmithDB cache a per-pod PVC from `smithdb.cache.storageClassName`, or from the cluster default StorageClass when that is unset. On chart v16, each cache was an `emptyDir`. To choose where the cache lives, set `smithdb.cache.storageClassName`, or define a volume named `cache` for each SmithDB component that uses a disk.
6. Run `make deploy`. With sandboxes running on chart v16, the first run stops with `namespace langsmith still mounts sandbox volumes through the chart 0.16 JuiceFS CSI driver` and prints the commands that drain the old volumes. Run them, wait until only `juicefs-csi-*` pods remain, then run `make deploy` again. Running sandboxes stop during the drain. Their data stays in S3 and Redis, and chart v17 mounts the same JuiceFS volume.
7. Verify the sandbox cutover:

   ```bash
   kubectl get jobs -n langsmith -l app.kubernetes.io/component=juicefs-format
   kubectl rollout status deployment -n langsmith -l app=sandbox-host --timeout=10m
   kubectl get daemonset,statefulset -n langsmith | grep juicefs-csi   # expect no output
   ```

For every chart change in v17, see [Upgrade from v16 to v17](../../Manage%20an%20instance/Upgrade%20an%20installation.md#upgrade-from-v16-to-v17) and the [`MIGRATION-0.16-to-0.17.md`](https://github.com/langchain-ai/terraform/blob/main/MIGRATION-0.16-to-0.17.md) guide in the Terraform repository.

## Enable add-ons

Each add-on is gated by a flag in `infra/terraform.tfvars`. Set the flag, run `make apply`, re-run `make init-values` to copy the matching values file, then re-run `make deploy`. `make apply` is required for add-ons that Terraform provisions: Fleet with external storage (the default), LangSmith Chat or Insights with external storage, sandboxes, and SmithDB. Sandboxes and SmithDB create AWS resources. External storage creates a database on the existing RDS instance and the matching Kubernetes secrets. For the rest, `make apply` makes no changes.

```hcl
enable_deployments     = true            # Agent Server hosting (listener, operator, host-backend)
enable_fleet           = true            # Fleet (formerly Agent Builder)
fleet_storage          = "external"      # default; "in-cluster" uses chart StatefulSets
enable_polly           = true            # LangSmith Chat (formerly Polly)
polly_storage          = "in-cluster"    # default; "external" uses RDS and ElastiCache
enable_insights        = true            # AI-powered trace analysis
insights_storage       = "in-cluster"    # default; "external" uses RDS and ElastiCache
enable_sandboxes       = false           # LangSmith Sandboxes
enable_smithdb         = false           # SmithDB
enable_usage_telemetry = false           # Extended usage telemetry
```

```bash
make apply
make init-values
make deploy
```

`enable_agent_builder` was removed in chart v16. Setting it to `true` fails validation at `terraform plan`, so delete it from existing `tfvars` files and use `enable_fleet`. `enable_standalone_polly` and `enable_standalone_insights` remain as legacy shorthand that enables the add-on with external storage (`enable_polly = true` with `polly_storage = "external"`, and the same for Insights).

For details on agent deployment, see [Agent Server hosting](../../Install%20an%20instance/Additional%20features/Enable%20Agent%20Server%20hosting.md).

### Fleet

> [!NOTE]
>
> Fleet is the current form of the feature formerly called Agent Builder. It requires LangSmith Helm chart v15 or later and the Fleet entitlement in your license.

Enable Fleet with `enable_fleet = true`. Fleet installs the host-backend it needs, so `enable_deployments` is optional.

With `fleet_storage = "external"` (the default), Fleet requires external Postgres and Redis (`postgres_source = "external"` and `redis_source = "external"`). Terraform creates a dedicated `langsmith_fleet` database on RDS and wires the `langsmith-fleet-postgres` and `langsmith-fleet-redis` secrets to the existing RDS and ElastiCache instances. Set `fleet_storage = "in-cluster"` to use the PostgreSQL and Redis StatefulSets in the chart instead.

Fleet reuses the `agent-builder-encryption-key` SSM parameter, so deployments that migrate from Agent Builder keep the same key and data.

### LangSmith Chat and Insights

`enable_polly` turns on LangSmith Chat (formerly Polly), and `enable_insights` turns on Insights. Neither requires `enable_deployments`. Both default to in-cluster storage. Set `polly_storage = "external"` or `insights_storage = "external"` to use dedicated databases on the shared RDS and ElastiCache instances; this requires `postgres_source = "external"` and `redis_source = "external"`. Each add-on needs its entitlement in your license.

### Sandboxes

`enable_sandboxes = true` adds a sandbox-host node group on bare-metal x86\_64 instances with KVM (`m5d.metal` by default) and a dedicated ElastiCache instance for JuiceFS metadata. Sandboxes require LangSmith Helm chart v16 or later.

`sandbox-host` mounts JuiceFS itself, and a `juicefs-format` Job formats the volume. `make init-values` writes `sandboxes.juicefs.existingSecretName` pointing at the `juicefs-csi-config` Secret, sets `sandboxes.juicefs.hostMount.cacheDirs` to the local NVMe cache paths on sandbox-host nodes when there are any, and puts the IRSA role annotation on `sandboxes.sandboxHost.serviceAccount`.

> [!NOTE]
>
> On chart v16, the chart bundles the JuiceFS CSI driver instead. `make init-values` from a `v0.16.*` module release writes `sandboxes.juicefs.csi.existingSecretName` and puts the IRSA role annotation on `sandboxes.juicefs.csi.node.serviceAccount`. The `juicefs-csi-config` Secret is the same on both lines.

To enable sandboxes on an existing deployment:

```bash
# After setting enable_sandboxes = true in infra/terraform.tfvars
source infra/scripts/setup-env.sh
make apply
make init-values
make deploy
```

Sourcing `setup-env.sh` again creates the JuiceFS Redis auth token and the sandbox callback signing key. The `sandbox_*` variables control the node count, instance types, and JuiceFS settings; see the [variables reference](AWS%20Terraform%20variables%20reference.md#sandboxes).

### SmithDB

`enable_smithdb = true` provisions the SmithDB dependencies: a metastore PostgreSQL instance, an S3 bucket, an IRSA role, and Karpenter node pools on local NVMe instances. `make init-values` then writes `langsmith-values-smithdb.yaml` and `langsmith-values-smithdb-overrides.yaml`, and `make deploy` stops if either file is missing.

Three gates move traffic to SmithDB after the services are healthy:

* `smithdb_ingestion_enabled` routes new writes to SmithDB.
* `smithdb_migration_enabled` migrates historical ClickHouse data. It requires ingestion.
* `smithdb_query_enabled` serves queries from SmithDB. It requires ingestion.

All three require `enable_smithdb = true`. Keep `smithdb_karpenter_chart_version` (default `1.6.3`) compatible with `eks_cluster_version` per the [Karpenter compatibility matrix](https://karpenter.sh/docs/upgrading/compatibility/). See the [variables reference](AWS%20Terraform%20variables%20reference.md#smithdb) for the full list.

## Optional: private EKS cluster with bastion

For deployments that must run a fully private EKS API endpoint, the modules ship a bastion host pattern:

1. First, run from your workstation with `create_bastion = true` and `enable_public_eks_cluster = true` so the bastion can be created.
2. After the initial deployment, set `enable_public_eks_cluster = false` and re-apply. The EKS API endpoint becomes private only.
3. All subsequent Terraform work happens on the bastion. SSM into it, clone the repo, copy your `terraform.tfvars` and SSM secrets, then run the deployment from there.

```hcl
enable_public_eks_cluster = false
create_bastion            = true

# Optional SSH access (SSM is the default and requires no key):
# bastion_key_name          = "my-keypair"
# bastion_enable_ssh        = true
# bastion_ssh_allowed_cidrs = ["203.0.113.0/24"]
```

Connect through SSM Session Manager:

```bash
make tf ARGS="output bastion_ssm_command"
aws ssm start-session --target <instance-id> --region us-west-2
```

> [!NOTE]
>
> The bastion runs in a private subnet with no public IP and reaches SSM through the NAT gateway. Setting `bastion_enable_ssh = true` moves it to a public subnet with a public IP. Set `bastion_existing_security_group_id` to attach your own security group. The bastion comes preinstalled with `kubectl`, `helm`, `terraform`, `git`, and `jq`, with kubeconfig already configured for the EKS cluster. Install the [Session Manager plugin](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html) for the AWS CLI on your workstation.

## Ingress, DNS, and TLS

The ALB is always the entry point. With `acm`, it terminates TLS. Behind it, [Envoy Gateway](https://gateway.envoyproxy.io/) is the default ingress: the ALB forwards to the Envoy pods through a TargetGroupBinding, and the LangSmith chart creates `HTTPRoute` resources instead of an `Ingress`.

| Setting in `terraform.tfvars` | Ingress |
| - | - |
| None of the flags set | Envoy Gateway behind the ALB (default) |
| `enable_envoy_gateway = false` | ALB Ingress created by the AWS Load Balancer Controller |
| `enable_istio_gateway = true` | Istio gateway behind the ALB |
| `enable_nginx_ingress = true` | NGINX ingress controller behind the ALB (legacy) |

Terraform rejects a configuration that turns on more than one of these.

In ALB Ingress mode, the AWS Load Balancer Controller creates its own ALB, and the Terraform ALB goes unused. The Route 53 alias record that Terraform creates for `langsmith_domain` still points at the Terraform ALB, so point the domain at the Ingress hostname instead (`kubectl get ingress -n langsmith`).

> [!WARNING]
>
> Deployments created before Envoy Gateway became the default, with no gateway flag set, switch to Envoy Gateway on the next `make apply`. To keep ALB Ingress, set `enable_envoy_gateway = false` before applying.

`tls_certificate_source` selects the certificate:

* `acm` (default): An ACM certificate on the ALB, either created by Terraform for `langsmith_domain` or supplied with `acm_certificate_arn`. Works with every ingress option.
* `letsencrypt`: cert-manager with Let's Encrypt, solving an HTTP-01 challenge through the ALB Ingress class. Works only in ALB Ingress mode (`enable_envoy_gateway = false`). Requires `letsencrypt_email`.
* `none`: Plain HTTP with no certificate.

For Let's Encrypt DNS-01 through Route 53, which Istio requires, set `create_cert_manager_irsa = true`, `cert_manager_hosted_zone_id`, and `letsencrypt_email`. Terraform creates the DNS-01 issuer when `langsmith_domain` is set. `create_cert_manager_irsa` and `tls_certificate_source = "letsencrypt"` are mutually exclusive.

With `langsmith_domain` set and `acm_certificate_arn` empty, `make apply` creates the ACM certificate and the Route 53 alias record. `make tls` does the same outside Terraform: it requests and DNS-validates a certificate, writes the alias record, and writes the certificate ARN to `terraform.tfvars`.

> [!WARNING]
>
> Do not run `make tls` after `make apply` has created the certificate and alias for `langsmith_domain`. The ARN that `make tls` writes turns off the Terraform DNS module, so the next `make apply` destroys the Terraform certificate, the alias record, and the hosted zone if Terraform created it (`dns_create_zone = true`).

### Split dataplane namespace

Envoy Gateway supports routing to a `langgraph-dataplane` chart that runs in its own namespace. Apply the RBAC manifest once per dataplane namespace:

```bash
kubectl apply -f helm/values/examples/dataplane-rbac.yaml
```

The manifest targets the `langsmith-agents` namespace; edit it for a different namespace. It grants the `langsmith-host-backend` ServiceAccount read access to pods, pod logs, deployments, and ReplicaSets in the dataplane namespace. Without it, agent run logs do not stream in the LangSmith UI.

## Next steps

* Reference the [AWS variables](AWS%20Terraform%20variables%20reference.md) and the [quick reference](AWS%20Terraform%20quick%20reference.md).
* Review the [AWS architecture](AWS%20Terraform%20architecture.md) for platform layers, IRSA, and module dependencies.
* When something breaks, check the [AWS troubleshooting guide](AWS%20Terraform%20troubleshooting.md).
* Enable agent deployment in the UI with [Agent Server hosting](../../Install%20an%20instance/Additional%20features/Enable%20Agent%20Server%20hosting.md).

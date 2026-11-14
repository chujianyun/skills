# AWS Terraform quick reference

> Make targets, Terraform commands, kubectl, AWS CLI, and Helm operations for LangSmith self-hosted on AWS EKS.

Command cheat sheet for day-to-day operations against an AWS LangSmith deployment provisioned with the [AWS Terraform modules](https://github.com/langchain-ai/terraform/tree/main/modules/aws). All `make` targets run from `modules/aws/`. Run `make help` for an inline summary.

For the full deploy setup, refer to the [AWS deployment guide](Deploy%20LangSmith%20on%20AWS%20with%20Terraform.md).

## First-time setup

```bash
cd terraform/modules/aws

# 1. Generate terraform.tfvars (interactive wizard)
make quickstart

# 2. Load secrets into SSM Parameter Store and export TF_VAR_* into your shell.
#    Use `source`: Make runs each target in a subshell.
source infra/scripts/setup-env.sh

# 2a. Confirm secrets and TF_VAR_* are set (optional but recommended)
make secrets

# 3. Provision infrastructure
make init
make plan       # review: confirm no unexpected destroy or replace actions
make apply

# 4. Point kubectl at the EKS cluster
source infra/scripts/set-kubeconfig.sh

# 5. Generate Helm values from Terraform outputs
make init-values

# 5a. Verify post-infra state (optional)
make preflight-post

# 6. Deploy LangSmith
make deploy
```

Fast path once `make quickstart` and `source infra/scripts/setup-env.sh` are complete:

```bash
make quickdeploy        # interactive (prompts before terraform apply)
make quickdeploy-auto   # non-interactive (auto-approves terraform)
```

## Day-2 operations

```bash
# Check deployment state across all layers; print next-step guidance
make status

# Re-deploy after editing Helm values or upgrading
make deploy

# Pin a chart version for one deploy (or set langsmith_helm_chart_version in tfvars)
CHART_VERSION=<version> make deploy

# Raise the Helm timeout (default 30m)
HELM_TIMEOUT=45m make deploy

# Re-generate Helm values after Terraform changes
make init-values

# Re-sync ESO secrets without redeploying
make apply-eso

# Check SSM secrets and TF_VAR_* export status (read-only)
make secrets

# List all SSM parameters with last-modified timestamps
make secrets-list

# Manage SSM secrets interactively (view, set, diff vs cluster)
make ssm

# Point kubectl at the EKS cluster
source infra/scripts/set-kubeconfig.sh
```

## Preflight checks

```bash
# Pre-Terraform: AWS credentials + IAM permissions
make preflight

# Post-infra (after make init-values): kubectl, SSM params, Helm values, TLS config
make preflight-post

# SSM only: confirm all parameters are populated (after sourcing setup-env.sh)
make preflight-ssm
```

## Add-ons

Add-ons are controlled by `enable_*` flags in `infra/terraform.tfvars`. Set the flags, run `make apply`, re-run `make init-values` to copy the matching values files, then run `make deploy`. Fleet, Insights, and LangSmith Chat with external storage, sandboxes, and SmithDB all create Terraform resources.

```hcl
# infra/terraform.tfvars
enable_deployments     = true   # Agent Server hosting (listener, operator, host-backend)
enable_fleet           = true   # Fleet (formerly Agent Builder); needs external Postgres and Redis when fleet_storage = "external" (default)
enable_insights        = true   # AI-powered trace analysis
enable_polly           = true   # LangSmith Chat (formerly Polly)
enable_usage_telemetry = false  # Extended usage telemetry
```

```bash
make apply
make init-values
make deploy
```

`enable_agent_builder` was removed in chart v16. Setting it to `true` fails validation at `terraform plan`, so use `enable_fleet` instead.

## Sizing profiles

Set `sizing_profile` in `terraform.tfvars`, then re-run `make init-values && make deploy`.

```hcl
sizing_profile = "production"        # multi-replica with HPA (recommended)
sizing_profile = "production-large"  # high-volume (~50 users, ~1000 traces/sec)
sizing_profile = "dev"               # single-replica, minimal resources
sizing_profile = "minimum"           # smallest footprint, for constrained clusters
sizing_profile = "default"           # chart defaults (no sizing file)
```

## Make targets

### Setup and secrets

| Command | Description |
| - | - |
| `make quickstart` | Interactive wizard. Generates `infra/terraform.tfvars` (region, node size, TLS method, add-ons). |
| `make setup-env` | Prints the exact `source` command for loading secrets into your shell. Cannot export variables directly. |
| `make secrets` | Show SSM secrets status (`✓ SET` / `✗ MISSING`) per parameter, check `TF_VAR_*` exports, give next steps. |
| `make secrets-list` | List all SSM parameters for this deployment with last-modified timestamps. |
| `make ssm` | Interactive SSM parameter manager. View, set, validate, diff vs the cluster Secret. To rotate a value, set a new one. |

### Preflight

| Command | Description |
| - | - |
| `make preflight` | Verify AWS credentials, IAM permissions, and required CLI tools before Terraform runs. |
| `make preflight-post` | Run after `make init-values`, before `make deploy`. Checks kubectl context, cluster reachability, SSM params populated, Helm values present, TLS config. |
| `make preflight-ssm` | Check SSM params only. Narrower scope than `preflight-post`. |

### Infrastructure

`make init`, `make plan`, `make apply`, and `make destroy` pass `ARGS` through to Terraform. For example: `make plan ARGS="-target=module.eks"`, `make plan ARGS="-out=tfplan"` then `make apply ARGS="tfplan"`, `make apply ARGS="-auto-approve"`, or `make init ARGS="-upgrade"`.

| Command | Description |
| - | - |
| `make init` | `terraform init`. Downloads providers and modules. Safe to re-run. |
| `make plan` | `terraform plan`. Preview changes. Review before every apply. |
| `make apply` | `terraform apply`. Provisions VPC, EKS, RDS, ElastiCache, S3, ALB, IRSA. |
| `make destroy` | `terraform destroy`. Tears down all infrastructure. Run `make uninstall` and turn off deletion protection first. Prints `make purge-secrets` as the next step. |
| `make tf ARGS="<subcommand>"` | Run any Terraform subcommand in `infra/`, for example `make tf ARGS="output -raw cluster_name"` or `make tf ARGS="state list"`. |
| `make purge-secrets` | Delete this deployment's SSM parameters after `make destroy`. Refuses while Terraform state still has resources, and asks you to type the prefix to confirm. |
| `make teardown-byo-sg BYO_SECURITY_GROUP_IDS="sg-..."` | Delete security groups created outside Terraform from a module-created VPC so `make destroy` can remove the VPC. |

### Helm deploy

| Command | Description |
| - | - |
| `make init-values` | Generate `helm/values/langsmith-values-overrides.yaml` from Terraform outputs. Copy add-on values files based on `enable_*` flags. |
| `make deploy` | Deploy or upgrade LangSmith via Helm. Updates kubeconfig, runs preflight, ESO sync, layered values build, and core readiness checks. Clears a stuck `pending-upgrade` or `pending-install` release, and refreshes a stale ALB hostname. |
| `make apply-eso` | Re-apply ESO `ClusterSecretStore` and `ExternalSecret` only. Use after rotating secrets without a full Helm redeploy. |
| `make uninstall` | Uninstall the LangSmith Helm release. Terraform infrastructure stays intact. `DELETE_DATA_PVCS=true` also deletes the ClickHouse PVC. |

### Fast path

| Command | Description |
| - | - |
| `make quickdeploy` | Full deploy in one command. Chains `terraform apply`, kubeconfig, `init-values`, and the Helm deploy with gates. Requires `make quickstart` and a sourced `setup-env.sh`. |
| `make quickdeploy-auto` | Same as `quickdeploy` but non-interactive. Passes `-auto-approve` to terraform. |
| `make deploy-all` | Runs `make apply`, `make kubeconfig`, `make init-values`, and `make deploy` in sequence. `make deploy` refreshes the kubeconfig before installing. |

### Utilities

| Command | Description |
| - | - |
| `make status` | Check deployment state across all layers, print what to run next. Reports the SmithDB ingestion and query gates when SmithDB is enabled. |
| `make status-quick` | Same as `status` but skips SSM, kubeconfig, Helm release, and Kubernetes queries (faster). |
| `make kubeconfig` | Print a `source infra/scripts/set-kubeconfig.sh` command to run. Sourcing it exports `KUBECONFIG` to a dedicated `~/.kube/langsmith-<cluster>` file rather than editing `~/.kube/config`. |
| `make tls` | BYO ACM cert + Route 53 A alias. Use when `langsmith_domain` is set and you need DNS wiring. |
| `make clean` | Remove local Terraform state, backups, logs, generated Helm values, and `terraform.tfvars`. Run after `make destroy` and `make purge-secrets`. Refuses while Terraform state still tracks resources or SSM parameters remain. If the state is gone but local state backups remain, asks you to type `DELETE BACKUPS` before removing them. |

### Testing

| Command | Description |
| - | - |
| `make test-e2e` | End-to-end gateway tests (ALB or Envoy Gateway) against the current cluster. |
| `make test-permutations` | Permutation tests sequentially on the current cluster. Use `ARGS="1 2 5"` for a subset. |
| `make test-parallel` | Permutation tests in parallel across isolated clusters. Your cluster is untouched. |
| `make test-quickstart` | Test the `make quickstart` Route 53 choices and update-mode defaults. Makes no AWS calls. |

## kubectl

```bash
# Pod health
kubectl get pods -n langsmith
kubectl get pods -n langsmith -w
kubectl describe pod <pod-name> -n langsmith
kubectl logs <pod-name> -n langsmith --tail=100 -f
kubectl logs <pod-name> -n langsmith --previous --tail=50

# Gateway routes (default Envoy Gateway mode)
kubectl get gateway,httproute -n langsmith

# Ingress (classic ALB Ingress mode only)
kubectl get ingress -n langsmith
kubectl describe ingress -n langsmith

# External Secrets Operator sync status
kubectl get externalsecret langsmith-config -n langsmith

# TLS
kubectl get certificate -n langsmith
kubectl get challenges -n langsmith
kubectl describe certificate <cert-name> -n langsmith

# Helm
helm status langsmith -n langsmith
helm history langsmith -n langsmith
helm get values langsmith -n langsmith

# IRSA: check per-component service account annotations
kubectl get sa -n langsmith -o yaml | grep eks.amazonaws.com

# Agent Server hosting
kubectl get lgp -n langsmith
kubectl get crd | grep langchain
kubectl get pods -n keda
```

## AWS CLI

```bash
# EKS
aws eks list-clusters --region <region>
aws eks describe-cluster --name <cluster-name> --region <region>
aws eks update-kubeconfig --region <region> --name <cluster-name>

# RDS
aws rds describe-db-instances \
  --query "DBInstances[?contains(DBInstanceIdentifier,'<name_prefix>-<environment>')]"

# ElastiCache
aws elasticache describe-cache-clusters \
  --query "CacheClusters[?contains(CacheClusterId,'<name_prefix>-<environment>')]"

# S3
aws s3 ls s3://<bucket-name>
aws s3api get-bucket-location --bucket <bucket-name>

# ALB
aws elbv2 describe-load-balancers \
  --query "LoadBalancers[?contains(LoadBalancerName,'<name_prefix>-<environment>')]"

# VPC endpoint
aws ec2 describe-vpc-endpoints \
  --filters "Name=service-name,Values=com.amazonaws.<region>.s3" \
  --query "VpcEndpoints[].State"

# SSM secrets (names only, so no secret value is printed)
aws ssm get-parameters-by-path --path "/langsmith/<name_prefix>-<environment>/" \
  --query "Parameters[].Name"

# IAM role
aws iam get-role --role-name <irsa-role-name>
```

## Terraform

Run these from `modules/aws/`:

```bash
make plan ARGS="-target=module.eks"
make apply ARGS="-target=module.eks"
make tf ARGS="output"
make tf ARGS="output -raw cluster_name"
# Entry point in Envoy (default), Istio, and NGINX modes; unused in classic ALB Ingress mode
make tf ARGS="output -raw alb_dns_name"
make tf ARGS="output -raw langsmith_irsa_role_arn"
make tf ARGS="output -raw bucket_name"
make tf ARGS="state list"
```

## Teardown

> [!WARNING]
>
> Teardown permanently deletes LangSmith data. Step 1 deletes the ClickHouse volume, step 4 deletes every trace object in S3, and step 6 deletes the SSM parameters. Those parameters include the API key salt, the JWT secret, and the encryption keys, which must never change. A database restored from the `-final` RDS snapshot needs them: without the original salt and keys, existing API keys stop working and encrypted data cannot be read. If you keep the snapshot, export the SSM parameters to a secure location before `make purge-secrets`.

```bash
cd terraform/modules/aws

# 1. Uninstall LangSmith. DELETE_DATA_PVCS=true also deletes the ClickHouse PVC,
#    whose EBS volume is otherwise left behind after destroy.
DELETE_DATA_PVCS=true make uninstall

# 2. Load the database and Redis credentials that apply and destroy require
source infra/scripts/setup-env.sh

# 3. Turn off deletion protection in infra/terraform.tfvars, then apply:
#      postgres_deletion_protection          = false
#      smithdb_metastore_deletion_protection = false   # only if SmithDB is enabled
make apply

# 4. Empty the trace bucket, which Terraform cannot delete while it holds objects
aws s3 rm s3://<bucket-name> --recursive

# 5. Destroy infrastructure
make destroy

# 6. Delete this deployment's SSM parameters
make purge-secrets

# 7. Remove local state, generated values, logs, and terraform.tfvars
make clean
```

With SmithDB enabled, also empty the SmithDB bucket before `make destroy`, or set `smithdb_s3_force_destroy = true` in step 3. With bucket versioning enabled, `aws s3 rm` leaves old object versions behind; delete them in the S3 console or with `aws s3api delete-objects`.

If `make destroy` cannot delete a module-created VPC because security groups created outside Terraform are still in it, run `make teardown-byo-sg BYO_SECURITY_GROUP_IDS="sg-..."`, then run `make destroy` again. The script refuses to run when `create_vpc = false`.

RDS takes a final snapshot named `<identifier>-final` unless `postgres_skip_final_snapshot = true`. With SmithDB enabled, the metastore RDS also takes a `-final` snapshot unless `smithdb_metastore_skip_final_snapshot = true`. A repeat destroy fails with `DBSnapshotAlreadyExists` if that snapshot still exists.

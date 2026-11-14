# GCP Terraform quick reference

> Make targets, Terraform, kubectl, gcloud, and Helm commands for LangSmith self-hosted on GKE.

Command cheat sheet for day-to-day operations against a GCP LangSmith deployment provisioned with the [GCP Terraform modules](https://github.com/langchain-ai/terraform/tree/main/modules/gcp). All `make` targets run from `modules/gcp/`. Run `make help` for an inline summary. Commands reflect the `main` branch and `v0.17.x` tags, which deploy Helm chart 0.17. The `smithdb-*` targets do not exist on `v0.16.x` tags.

## Deployment overview

| Stage | What gets deployed | Command |
| - | - | - |
| Infrastructure | VPC + GKE + Cloud SQL + Memorystore + GCS + IAM + cert-manager + KEDA + Envoy Gateway | `make apply` |
| Cluster credentials | Kubeconfig wired to the new GKE cluster | `make kubeconfig` |
| LangSmith base | Frontend, backend, ingest, queue, ClickHouse | `make init-values && make deploy` |
| Fleet add-on (standalone) | standalone-fleet-\* API server, tool server, trigger server, queue | `make apply && make init-values && make deploy` |
| Agent Server hosting add-on | host-backend, listener, operator | `make init-values && make deploy` |
| Agent Builder add-on (deprecated) | tool-server, trigger-server | `make init-values && make deploy` |
| Insights + Polly add-on | Insights analytics, Polly eval agent | `make init-values && make deploy` |
| SmithDB add-on | Metastore, object-store bucket, node pools, SmithDB services | `make apply && make init-values && make deploy` |
| Sandboxes add-on | sandbox-host node pool, JuiceFS metadata Redis | `make apply && make init-values && make deploy` |

Each stage builds on the previous. Verify pods are healthy before enabling the next.

## First-time setup

```bash
cd terraform/modules/gcp

# Interactive wizard: generates terraform.tfvars
make quickstart

# Set up secrets in Secret Manager (auto-generates salts + Fernet keys)
# Must be sourced so it can export TF_VAR_* into your shell
source infra/scripts/setup-env.sh
export LANGSMITH_ADMIN_EMAIL="<your-admin-email>"

# Validate credentials, APIs, permissions, and quotas
make preflight

# Deploy infrastructure
make init
make plan
make apply

# Generate Helm values from Terraform outputs
make init-values

# Deploy LangSmith
make deploy
```

`make deploy-all` chains `apply`, `init-values`, and `deploy` in one command. Run `make init-values` and `make deploy` from the shell where you sourced `setup-env.sh`; the deploy script reads the `TF_VAR_*` secrets and `LANGSMITH_ADMIN_EMAIL` from it.

## Day-2 operations

```bash
# Check deployment state and next-step guidance
make status              # full check
make status-quick        # skip Secret Manager and K8s queries

# Re-deploy after changing Helm values or upgrading chart version
make deploy

# Re-generate Helm values after Terraform changes
make init-values

# Manage Secret Manager secrets interactively
make secrets

# Update kubeconfig for the GKE cluster
make kubeconfig

# SmithDB: run only the commands you need, with your own values
make smithdb-status                                  # read-only: gates, sizing, pods, backfill progress
make smithdb-configure SIZING=<size> CACHE=<cache>  # minimal | small | medium | large; local-ssd | network-disk
make smithdb-phase PHASE=<phase>                     # off | dual-write | backfill | cutover
make deploy-all                                      # apply the change: apply, init-values, deploy
```

`make kubeconfig` wraps `helm/scripts/get-kubeconfig.sh`. To call the script directly, pass the cluster name, region, and project as arguments, or omit them to read the Terraform outputs.

`make smithdb-configure` and `make smithdb-phase` only edit `terraform.tfvars`, and `make deploy-all` applies the change. A size change can replace the SmithDB node pools. Leaving the `backfill` phase removes the backfill Job and its task database; `make smithdb-phase PHASE=cutover` refuses until every backfill row is promoted, but an earlier phase has no such check.

For the SmithDB rollout stages, see [SmithDB](Deploy%20LangSmith%20on%20GCP%20with%20Terraform.md#smithdb) in the deployment guide.

## Add-ons

Set flags in `terraform.tfvars`, then `make init-values && make deploy`. `init-values.sh` copies the matching example file into `helm/values/` automatically.

```hcl
# terraform.tfvars
enable_deployments   = true
enable_fleet         = true   # Fleet (formerly Agent Builder), standalone; no enable_deployments required
enable_agent_builder = false  # deprecated, superseded by enable_fleet; mutually exclusive with it
enable_insights      = true
enable_polly         = true   # requires enable_deployments = true + Polly license
enable_usage_telemetry = true # extended usage telemetry
```

To add an add-on after initial install without re-running `init-values.sh`, copy manually:

```bash
cp helm/values/examples/langsmith-values-agent-deploys.yaml helm/values/
cp helm/values/examples/langsmith-values-fleet.yaml         helm/values/
cp helm/values/examples/langsmith-values-insights.yaml      helm/values/
cp helm/values/examples/langsmith-values-polly.yaml         helm/values/

make deploy
```

## Sizing profiles

Set `sizing_profile` in `terraform.tfvars`, then re-run `make init-values && make deploy`.

```hcl
sizing_profile = "production"   # default | minimum | dev | production | production-large
```

| Profile | When to use |
| - | - |
| `default` | Chart defaults: quick tests, no overlay applied |
| `minimum` | Absolute floor; fits `e2-standard-4`; use for cost parking or CI smoke tests |
| `dev` | Single replica, minimal resources |
| `production` | Multi-replica with HPA; recommended for real workloads |
| `production-large` | High memory and CPU; 50+ users or 1000+ traces/sec |

## kubectl

```bash
# Pod health
kubectl get pods -n langsmith
kubectl get pods -n langsmith -w
kubectl describe pod <pod-name> -n langsmith
kubectl logs <pod-name> -n langsmith --tail=100 -f
kubectl logs <pod-name> -n langsmith --previous --tail=50

# Backend logs (live)
kubectl logs -n langsmith deploy/langsmith-backend --tail=100 -f

# Gateway and HTTPRoute
kubectl get gateway -n envoy-gateway-system
kubectl get httproute -n langsmith
kubectl get svc -n envoy-gateway-system

# TLS
kubectl get certificate -n langsmith
kubectl get challenges -n langsmith
kubectl describe certificate <cert-name> -n langsmith
kubectl get clusterissuer

# Workload Identity
kubectl get serviceaccount langsmith-ksa -n langsmith -o yaml | grep annotation -A5

# Helm
helm status langsmith -n langsmith
helm history langsmith -n langsmith
helm get values langsmith -n langsmith

# Agent Server hosting
kubectl get lgp -n langsmith
kubectl get crd | grep langchain
```

## gcloud

```bash
# Re-auth if you hit oauth2 invalid_grant / invalid_rapt errors
gcloud auth login
gcloud auth application-default login

# Cluster credentials
gcloud container clusters get-credentials <cluster-name> --region <region> --project <project-id>

# List clusters
gcloud container clusters list --project <project-id>

# Cluster status
gcloud container clusters describe <cluster-name> --region <region> --format="value(status)"

# Cloud SQL
gcloud sql instances list --project <project-id>
gcloud sql instances describe <instance-name> --format="value(ipAddresses)"

# Memorystore Redis
gcloud redis instances list --region <region>
gcloud redis instances describe <instance-name> --region <region> --format="value(host)"

# GCS bucket
gsutil ls gs://<bucket-name>
gsutil iam get gs://<bucket-name>

# Workload Identity binding
gcloud iam service-accounts get-iam-policy <gsa-email> --project <project-id>

# Enabled APIs
gcloud services list --enabled --project <project-id>

# VPC peering
gcloud services vpc-peerings list --network <vpc-name> --project <project-id>

# Secret Manager
gcloud secrets list --project <project-id> --filter="name:langsmith"
gcloud secrets versions access latest --secret=<secret-id> --project <project-id>
```

## Terraform

```bash
cd modules/gcp/infra

terraform init
terraform plan
terraform apply

# Target a specific module
terraform apply -target=module.networking

# Outputs
terraform output
terraform output -raw cluster_name
terraform output -raw storage_bucket_name

# State
terraform state list
terraform state show module.gke_cluster
terraform refresh
```

## Key constraints

* Uninstall Helm before `terraform destroy`. The Envoy Gateway load balancer references the VPC; leaving it blocks network deletion. Always run `make uninstall` first.
* `config.deployment.url` must include `https://`. Without the protocol, operator-spawned agents stay stuck in `DEPLOYING`.
* `config.deployment.enabled: true` is required for the Agent Server hosting add-on. Setting only the URL without `enabled: true` silently skips `listener` and `operator`.
* Encryption keys must never change after first enable. Rotating `langsmith_insights_encryption_key` or `langsmith_polly_encryption_key` permanently breaks existing encrypted data.
* Envoy Gateway IP changes on teardown. GCP releases the external IP when the Gateway is deleted. After `terraform destroy` and re-apply, update your DNS A record.
* Upgrading from chart 0.16 has gates. `deploy.sh` refuses the upgrade while `values-overrides.yaml` still has a `sandboxes.juicefs.csi` block, while JuiceFS CSI volumes or mount pods remain, or while `helm/values/` still has the chart 0.16 SmithDB overlay. Each refusal prints the commands that clear it. For the full procedure, see [Upgrade from chart 0.16](Deploy%20LangSmith%20on%20GCP%20with%20Terraform.md#upgrade-from-chart-0-16).
* `langsmith-ksa` annotation is not permanent. Terraform creates the ServiceAccount in the `k8s-bootstrap` module, outside the Helm release, so it does not survive namespace deletion. `deploy.sh` re-creates and re-annotates it idempotently.

## Teardown

> [!WARNING]
>
> Teardown permanently deletes the Cloud SQL instances. Cloud SQL takes no final snapshot on delete: its automated backups, on-demand backups, and point-in-time recovery logs are deleted with the instance. To keep the data, export it to a bucket outside this deployment before step 1. Skip the export for a disposable test stack.

```bash
# Export the LangSmith database. Repeat for the SmithDB metastore with
# smithdb_metastore_instance_name and --database=smithdb.
PROJECT_ID=<project-id>
BACKUP_BUCKET=gs://<export-bucket>
PG=$(terraform -chdir=infra output -raw postgres_instance_name)
SA=$(gcloud sql instances describe "$PG" --project "$PROJECT_ID" \
  --format="value(serviceAccountEmailAddress)")
gcloud storage buckets add-iam-policy-binding "$BACKUP_BUCKET" \
  --member="serviceAccount:$SA" --role=roles/storage.objectAdmin
gcloud sql export sql "$PG" "$BACKUP_BUCKET/${PG}-final.sql.gz" \
  --database=langsmith --project "$PROJECT_ID"
```

```bash
# 1. Remove Agent Server hosting resources (if the add-on was enabled)
kubectl delete lgp --all -n langsmith 2>/dev/null || true

# 2. Uninstall LangSmith
make uninstall

# 3. Load the TF_VAR_* secrets
source infra/scripts/setup-env.sh

# 4. Set the teardown flags below in terraform.tfvars, then apply them
terraform -chdir=infra apply \
  -target=module.gke_cluster -target=module.cloudsql \
  -target=module.smithdb -target=module.networking

# 5. Destroy
make destroy
```

```hcl
# terraform.tfvars
gke_deletion_protection      = false
postgres_deletion_protection = false

# Only when enable_smithdb = true and smithdb_metastore_source = "create"
smithdb_metastore_deletion_protection = false

# Optional, any SmithDB install: lets make destroy delete the SmithDB bucket and
# its trace segments. With the default (false), make destroy stops at a
# non-empty SmithDB bucket.
smithdb_bucket_force_destroy = true
```

Deletion protection also applies at the Cloud SQL API level, so the targeted apply in step 4 must run before `make destroy`, even when protection is already off. Drop the `module.smithdb` target if you never enabled SmithDB. To also delete the persistent disks of in-cluster databases, run `DELETE_DATA_PVCS=true make uninstall` in step 2.

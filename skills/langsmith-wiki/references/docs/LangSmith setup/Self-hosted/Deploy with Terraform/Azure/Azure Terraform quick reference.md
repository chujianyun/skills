# Azure Terraform quick reference

> Make targets, Terraform, kubectl, Azure CLI, and Helm commands for LangSmith self-hosted on AKS.

Command cheat sheet for day-to-day operations against an Azure LangSmith deployment provisioned with the [Azure Terraform modules](https://github.com/langchain-ai/terraform/tree/main/modules/azure). All `make` targets run from `modules/azure/`. Run `make help` for an inline summary.

For the full deployment walkthrough, see the [Azure deployment guide](Deploy%20LangSmith%20on%20Azure%20with%20Terraform.md).

## Deployment overview

| Stage | What gets deployed | Command |
| - | - | - |
| Infrastructure | AKS + Postgres + Redis + Blob + Key Vault + cert-manager + KEDA + ingress | `make apply` |
| App secrets | LangSmith app secrets written to Key Vault. Never overwrites an existing secret | `make seed-secrets` |
| Cluster credentials | Kubeconfig + Kubernetes Secrets from Key Vault | `make kubeconfig && make k8s-secrets` |
| LangSmith | LangSmith Helm release via shell scripts | `make init-values && make deploy` |
| Agent Server hosting add-on | host-backend, listener, operator. Bump `default_node_pool_min_count` to 5 first | `make apply && make init-values && make deploy` |
| Fleet add-on | Fleet tool server and trigger server, plus a dedicated `langsmith_fleet` Postgres database. Requires `enable_deployments` and `postgres_source = "external"` | `make apply && make init-values && make deploy` |
| Agent Builder add-on | Legacy path that Fleet replaces: tool server and trigger server | `make init-values && make deploy` |
| Insights + Polly add-on | Insights analytics, Polly eval agent | `make init-values && make deploy` |
| SmithDB | PostgreSQL 18 metastore, Blob container, Workload Identity. Requires chart 0.17, the default on `v0.17.*` module tags | `make apply && make init-values && make deploy` |
| LLM Gateway add-on | Gateway pod, plus the Presidio analyzer with PII redaction. In beta | `make init-values && make deploy` |
| SSO with OIDC | OIDC login, which disables basic auth. Store the three `langsmith-oauth-*` secrets in Key Vault first | `make k8s-secrets && make init-values && make deploy` |

## First-time setup

```bash
cd terraform/modules/azure
git checkout "$(git tag -l 'v0.17.*' --sort=-v:refname | head -1)"   # newest v0.17 release

# 1. Generate terraform.tfvars (interactive wizard)
make quickstart

# 2. Write Terraform inputs (Postgres password, license key, admin email)
#    to secrets.auto.tfvars. Re-runs offer the previous values as defaults
make setup-env

# 3. Preflight (Azure CLI, RBAC, providers)
make preflight

# 4. Deploy infrastructure (~15 to 20 min)
#    make apply runs three stages, and each prompts for confirmation
make init
make apply

# 5. Write the LangSmith app secrets into Key Vault (never overwrites)
make seed-secrets

# 6. Cluster credentials + Kubernetes Secrets
make kubeconfig
make k8s-secrets

# 7. Generate Helm values from Terraform outputs
make init-values

# 8. Deploy LangSmith (~10 min)
make deploy

# 9. Health check
make status
```

Or, after `make init`, run the rest of steps 4 through 8 in one shot:

```bash
make deploy-all   # apply → seed-secrets → kubeconfig → k8s-secrets → init-values → deploy
```

## Day-2 operations

```bash
make status         # health check that prints the next command to run
make status-quick   # skip the Key Vault, kubeconfig, Kubernetes, and Helm checks (faster)
make deploy         # re-deploy after any Helm value changes
make init-values    # re-generate values after Terraform changes
make kubeconfig     # refresh cluster credentials
make seed-secrets   # write any missing app secrets into Key Vault
make k8s-secrets    # re-create langsmith-config-secret from Key Vault

# Manage Key Vault secrets
make keyvault                                       # interactive menu
./infra/scripts/manage-keyvault.sh list             # all secrets with timestamps
./infra/scripts/manage-keyvault.sh get <secret>     # read a secret
./infra/scripts/manage-keyvault.sh set <key> <val>  # update a secret
./infra/scripts/manage-keyvault.sh validate         # check all required secrets exist
./infra/scripts/manage-keyvault.sh diff             # compare KV vs K8s secret
./infra/scripts/manage-keyvault.sh delete <key>     # soft-delete (recoverable 90 days)
```

## Add-ons

Add-ons are controlled by flags in `infra/terraform.tfvars`. Set the flags, then re-run `make init-values && make deploy`. `enable_fleet` and `enable_smithdb` also create Terraform resources, so run `make apply` first. `init-values.sh` writes the matching overlay into `helm/values/` automatically.

```hcl
# infra/terraform.tfvars
sizing_profile       = "production"   # minimum | dev | production | production-large
enable_deployments   = true           # Agent Server hosting add-on (listener + operator + host-backend)
enable_fleet         = true           # Fleet add-on (requires enable_deployments and postgres_source = "external")
enable_agent_builder = false          # legacy Agent Builder (requires enable_deployments); cannot be combined with enable_fleet
enable_insights      = true           # Insights analytics add-on
enable_polly         = true           # Polly AI eval add-on (needs enable_deployments)
enable_llm_gateway   = false          # LLM Gateway, in beta (chart 0.17)
enable_gateway_pii_redaction = false  # Presidio PII redaction (requires enable_llm_gateway)
enable_sso_oidc      = false          # OIDC SSO; enable only after logging in as the org admin with basic auth
```

> [!WARNING]
>
> The Agent Server hosting add-on requires `default_node_pool_min_count = 5` first. Operator-spawned pods need node headroom; without it, agent pods stay in `Pending` indefinitely.

## Sizing profiles

Set `sizing_profile` in `terraform.tfvars`, then re-run `make init-values && make deploy`.

| Profile | When to use |
| - | - |
| `minimum` | Cost parking, CI smoke tests, single-user demos. Expect OOM under real traffic. |
| `dev` | Light non-production for local dev, CI pipelines, integration tests, short-lived POCs. |
| `production` | *Recommended* for production. Multi-replica with HPA on all stateless components. |
| `production-large` | High-volume starting point based on the scale guide (\~50 concurrent users, \~1000 traces/sec). |

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

# Envoy Gateway (default ingress_controller)
kubectl get gateway,httproute -n langsmith
kubectl get svc -n envoy-gateway-system -l gateway.envoyproxy.io/owning-gateway-name=langsmith-gateway

# Ingress (nginx, istio, agic)
kubectl get ingress -n langsmith
kubectl describe ingress -n langsmith

# NGINX LoadBalancer external IP (ingress_controller = "nginx")
kubectl get svc ingress-nginx-controller -n ingress-nginx

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

## Azure CLI

```bash
# Re-auth
az login
az account set --subscription <subscription-id>
az account show

# AKS
az aks list
az aks show --name <cluster> --resource-group <rg>
az aks get-credentials --name <cluster> --resource-group <rg>

# PostgreSQL
az postgres flexible-server list
az postgres flexible-server show --name <server> --resource-group <rg>

# Azure Managed Redis
az redisenterprise list
az redisenterprise show --cluster-name <cluster> --resource-group <rg>

# Blob Storage
az storage account list
az storage container list --account-name <account>

# Key Vault
az keyvault list
az keyvault secret list --vault-name <vault>
az keyvault secret show --vault-name <vault> --name <secret> --query value -o tsv

# Application Gateway (AGIC)
az network application-gateway list
```

## Terraform

Run Terraform through `make` from `modules/azure/`. `ARGS` is appended to the Terraform command, so you do not need `-chdir`.

```bash
make init ARGS="-upgrade"                  # re-resolve provider versions
make plan                                  # plan the full infrastructure
make plan ARGS="-out=tfplan"               # save a plan file
make apply ARGS="-auto-approve"            # three stages, no prompts
make tf ARGS="apply tfplan"                # apply a saved plan
make plan ARGS="-target=module.aks"        # plan one module

make tf ARGS="output"
make tf ARGS="output -raw aks_cluster_name"
make tf ARGS="output -raw keyvault_name"
make tf ARGS="output -raw storage_account_name"

make tf ARGS="state list"
```

## Key constraints

* `make apply` runs three targeted stages (Azure infrastructure, Kubernetes bootstrap, then everything else), and each stage prompts for confirmation. `ARGS="-auto-approve"` skips all three prompts.
* Uninstall Helm before `terraform destroy`. The Azure Load Balancer holds a subnet reference; leaving it blocks VNet deletion. Run `make uninstall` first.
* `config.deployment.url` must include `https://`. Without it, operator-spawned agents stay stuck in `DEPLOYING`.
* `config.deployment.enabled: true` is required for the Agent Server hosting add-on. Setting only the URL without `enabled: true` silently skips `listener` and `operator`.
* Encryption keys must never change after first enable. Rotating `insights_encryption_key` or `polly_encryption_key` permanently breaks existing encrypted data.
* Roll the frontend after first Polly enable. The `langsmith-polly-config` ConfigMap appears after Polly registers; frontend pods started earlier do not pick it up.
* `letsencrypt` (HTTP-01) only works with `nginx`, `istio` (self-managed), and `envoy-gateway`. For `istio-addon` or `agic`, use `dns01` with a custom domain, `existing` with your own certificate, or `none` for HTTP-only.
* Set `aks_private_cluster_enabled`, `aks_private_dns_zone_id`, and `aks_control_plane_identity` before the first apply. Plan refuses a change to any of them on an existing cluster.
* `v0.17.*` module tags deploy only the chart 0.17 line, and `v0.16.*` tags deploy only 0.16. On a `v0.16.*` tag, `enable_smithdb = true` requires the 0.17 line, so set `langsmith_helm_chart_version = "~0.17.0"` with it. A deployment that has run chart 0.17 cannot return to 0.16.
* Enable `enable_sso_oidc` only after you have logged in as the org admin with basic auth. The flag disables basic auth.
* Key Vault enters 90-day soft-delete after destroy. With `keyvault_purge_protection = false`, run `az keyvault purge` to reclaim the name immediately.

## Teardown

```bash
make uninstall   # removes Helm release + Agent Server hosting resources; prompts to delete namespace
helm uninstall ingress-nginx -n ingress-nginx --wait   # only with ingress_controller = "nginx"
make destroy     # destroys all Azure infrastructure via terraform destroy
make clean       # removes local secrets, config, helm values, and tfstate files
```

`make destroy-force` and `make clean-force` run the same steps without the confirmation prompt.

> [!WARNING]
>
> `make clean-force` also answers the prompt that guards a state file which still tracks resources, and then deletes `terraform.tfstate`. With the default local backend, that file is the only state, so running it before `make destroy` succeeds orphans the Azure resources. Run `make clean-force` only after a successful `make destroy`.

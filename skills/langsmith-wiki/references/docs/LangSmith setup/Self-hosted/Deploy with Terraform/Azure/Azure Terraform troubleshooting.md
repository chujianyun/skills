# Azure Terraform troubleshooting

> Common issues, fixes, and diagnostic commands for LangSmith self-hosted on Azure AKS deployed with the LangChain Terraform modules.

This page documents common issues, fixes, and diagnostic commands for LangSmith deployments provisioned with the [Azure Terraform modules](https://github.com/langchain-ai/terraform/tree/main/modules/azure).

> [!TIP]
>
> Before upgrading, review the [LangSmith self-hosted changelog](../../Reference/Self-hosted%20LangSmith%20changelog.md) for breaking changes and required variable updates. Run `make kubeconfig` before running any `kubectl` commands. It fetches the cluster credentials and, on Microsoft Entra ID clusters, converts them for `kubelogin`.

For a copy-paste reference of the `kubectl`, `helm`, and `az` calls used throughout this page, skip to [Diagnostic commands](#diagnostic-commands).

## Infrastructure stage

### Resource name is already taken globally

**Symptom:** `terraform apply` fails with `The name 'langsmith-redis-dev' is not available`, `StorageAccountAlreadyTaken`, or `VaultAlreadyExists`.

**Cause:** Postgres, Redis, Storage, and Key Vault names are global across all Azure tenants. With `unique_resource_names = false` (the default), the names derive from `name_prefix` alone, so another deployment with the same `name_prefix` can already hold them. A soft-deleted Key Vault from an earlier `terraform destroy` also holds its name until the retention window ends.

**Fix:**

* New deployment: set `unique_resource_names = true` in `terraform.tfvars`. This switches the base name from `langsmith` to `ls` and appends a hash of the subscription ID and `name_prefix` to the four global names.
* Existing deployment: do not change `unique_resource_names`, which renames and recreates every resource. Pin only the colliding name with `postgres_name`, `redis_name`, `storage_account_name`, or `keyvault_name`.
* A failed first apply with `unique_resource_names = true`: set `name_suffix_salt = "2"` to rotate all four hashed names. On a live deployment this destroys and recreates Postgres, Redis, Storage, and Key Vault.

Run `make preflight` before applying. It checks the Postgres, Storage, and Key Vault names and the `dns_label` against the Azure availability APIs. Redis names have no availability check.

### `K8sVersionNotSupported`: version is LTS-only

**Symptom**

```txt
Error: creating Kubernetes Cluster ... unexpected status 400
"code": "K8sVersionNotSupported"
"message": "Managed cluster ... is on version 1.32.x, which is only available for Long-Term Support (LTS).
If you intend to onboard to LTS, please ensure the cluster is in Premium tier ..."
```

**Cause:** Azure periodically retires minor versions from Standard tier support and moves them to LTS-only. As of April 2026, 1.32 and below are LTS-only in `eastus`. Standard tier clusters must use 1.33 or later.

**Fix:** Set `aks_kubernetes_version` to a version with `KubernetesOfficial` support. The module defaults to `1.35`.

```bash
az aks get-versions --location eastus -o table
# Versions with KubernetesOfficial in SupportPlan column work on Standard tier
```

Remove or update any `aks_kubernetes_version` pin in `terraform.tfvars`, then `make apply`. Existing clusters on 1.32 continue to run; this only blocks new cluster creation.

### vCPU quota exceeded

**Symptom (autoscaler backoff, pods Pending):**

```txt
Warning  FailedScheduling     pod/langsmith-backend-xxx  0/1 nodes are available: 1 Too many pods.
Normal   NotTriggerScaleUp    pod/langsmith-backend-xxx  pod didn't trigger scale-up: 2 in backoff after failed scale-up
```

**Symptom (node pool rotation):**

```txt
Error: creating temporary Agent Pool ... "code": "ErrCode_InsufficientVCPUQuota",
"message": "Insufficient vcpu quota requested 8, remaining 2 for family standardDSv5Family for region eastus."
```

**Cause:** Per-region vCPU quotas per VM family. Default for `standardDSv5Family` in `eastus` is often 10 cores. One `Standard_D8s_v5` node, the module default, uses 8; only 2 remain.

**Why `max_pods = 30` triggers it:** The base install runs \~37 pods (\~17 LangSmith plus \~20 system), more than the AKS default of 30 per node, so the autoscaler adds a second node, hits quota, and backs off. The module default `default_node_pool_max_pods = 60` fits all pods on one node. Check that `terraform.tfvars` does not lower it.

**Recommended quota** for multi-dataplane (3 dataplanes): 32 cores.

**Request a quota increase:**

```bash
# Azure portal usually auto-approves within minutes:
# Portal > Subscriptions > <sub> > Usage + Quotas > search "DSv5" > eastus > Request increase > 32

# Or via CLI
az quota update \
  --resource-name "standardDSv5Family" \
  --scope /subscriptions/<sub-id>/providers/Microsoft.Compute/locations/eastus \
  --limit-object value=32 limit-type=Independent \
  --resource-type dedicated

az vm list-usage --location eastus --query "[?contains(name.value,'DSv5')]" -o table
```

**Alternative, switch VM family if DSv5 quota is exhausted:** Set `default_node_pool_vm_size = "Standard_D8s_v3"` and use `Standard_D16s_v3` for the `large` pool in `additional_node_pools`. Same vCPU and RAM, different quota pool. Move back to v5 once the quota arrives. Do not fall back to DSv2 (`Standard_DS4_v2`, `Standard_DS5_v2`), which Azure has retired.

> [!NOTE]
>
> `max_pods` is immutable on an existing node pool. Set it before the first `terraform apply`.

### `LocationIsOfferRestricted`: Postgres Flexible Server blocked in the region

**Symptom:** AKS creates successfully, then Postgres fails with `Status: "LocationIsOfferRestricted"` or `ParameterOutOfRange: The value of the 'Version' should be in: []`.

**Cause:** Azure blocks some subscription offer types (Free Trial, Visual Studio and MSDN credit, Azure Pass, some sponsored subscriptions) from provisioning PostgreSQL Flexible Server in high-demand regions. The subscription type, not the region, determines the outcome. `make preflight` reports this before the apply starts.

**Fix:** Use one of the following, in order of preference:

1. Convert the subscription to Pay-As-You-Go.
2. Request an exemption at [aka.ms/postgres-request-quota-increase](https://aka.ms/postgres-request-quota-increase).
3. For a dev or demo deployment, set `postgres_source = "in-cluster"`. Not suitable for production.
4. Change `location` in `terraform.tfvars`. Postgres must sit in the same region as the VNet, so the whole deployment moves.

### Database SKU family has no quota in the region

**Symptom:** The apply builds the resource group, VNet, and AKS, then fails on the Flexible Server with a quota error naming a vCPU family and the region, such as `standardDDSv5Family` in `eastus`.

**Cause:** Postgres Flexible Server draws on the `Microsoft.Compute` per-family vCPU quota. Fresh subscriptions often ship some families with a limit of 0. `make preflight` maps `postgres_sku_name` to its family and fails on a zero limit before the apply starts.

**Fix:** Request an increase at [aka.ms/postgres-request-quota-increase](https://aka.ms/postgres-request-quota-increase), or set `postgres_sku_name` to a SKU in a family that has quota:

```bash
az vm list-usage -l eastus --only-show-errors --query "[?limit=='0'].name.value" -o tsv
```

### `AuthorizationFailed` on `roleAssignments/write`

**Symptom:** Resources create normally, then a role assignment fails with `does not have authorization to perform action 'Microsoft.Authorization/roleAssignments/write'`.

**Cause:** The deploying identity holds Contributor but no role-assignment role. The module creates role assignments for its own managed identities, which Contributor cannot do. If the identity already holds User Access Administrator, the subscription may gate that permission behind an ABAC condition on `principalType`, which returns the same message.

**Fix:**

* Grant `Role Based Access Control Administrator` at subscription scope, or `Owner` in place of both roles. Run `make preflight` to check the deploying identity's roles before the apply.
* For a `principalType` condition, set `terraform_principal_type = "User"` for an interactive `az login`, or `"ServicePrincipal"` in CI. If the condition permits only service principals, set `keyvault_manage_terraform_admin_assignment = false` and `keyvault_manage_secrets = false`. Have a tenant admin grant you Key Vault Secrets Officer on the vault, then write the secrets with `make seed-secrets`.

See [PERMISSIONS.md](https://github.com/langchain-ai/terraform/blob/main/modules/azure/PERMISSIONS.md) for the full permission inventory.

### `AuthorizationFailed` on a read during `terraform plan`

**Symptom:** `terraform plan` against an applied deployment fails while refreshing, with a 403 on a `read` action such as `Microsoft.Network/publicIPAddresses/read`.

**Cause:** Refresh reads every resource in state. When a read that worked earlier starts failing, the usual reason is an expired Privileged Identity Management (PIM) activation. Running `az login` again does not fix it.

**Fix:** Re-activate the role in the Azure portal (PIM > My roles > Activate) for longer than the apply takes. `make preflight` prints the time remaining on an active PIM activation.

### `LinkedAuthorizationFailed` creating a private endpoint

**Symptom:** With `storage_private_dns_zone_id` or `keyvault_private_dns_zone_id` set, `make apply` fails creating a private endpoint with `LinkedAuthorizationFailed`.

**Cause:** The endpoint registers its record in the zone you supplied, which needs `Microsoft.Network/privateDnsZones/join/action` on that zone. An endpoint in a subnet the module did not create also needs `Microsoft.Network/virtualNetworks/subnets/join/action` on the subnet. A new grant can take 12 to 40 minutes to take effect, and Azure fails the endpoint until it does.

**Fix:** Grant `Private DNS Zone Contributor` at the zone's resource group, and `Network Contributor` on the endpoint subnet, before the first apply. If the grants exist, wait and run `make apply` again. See [PERMISSIONS.md](https://github.com/langchain-ai/terraform/blob/main/modules/azure/PERMISSIONS.md#private-dns-zones-you-own).

### Istio addon revision not supported

**Symptom:** `terraform apply` rejects the Istio revision (`Revision asm-1-XX is not supported`). Azure retires old ASM revisions regularly.

**Fix:** Check currently available revisions and update `istio_addon_revision`:

```bash
az aks mesh get-revisions --location eastus -o table
```

Set the value in `terraform.tfvars` and re-apply.

### Key Vault purge protection cannot be disabled after enabling

**Symptom**

```txt
Error: updating Key Vault "langsmith-kv-dz":
once Purge Protection has been Enabled it's not possible to disable it
```

**Cause:** When a Key Vault is deleted via `terraform destroy`, Azure soft-deletes it for 90 days. The next `terraform apply` with the same name silently recovers the old Key Vault, including its original `purge_protection_enabled = true`. Purge protection is one-way (enabled → cannot be disabled).

**Fix (accept purge protection, test environments):**

```hcl
keyvault_purge_protection = true
```

**Fix (`purge_protection = false` required):** Purge protection also blocks `az keyvault purge` until the retention window ends, so the recovered vault cannot be purged to free its name. Give the deployment a new vault name instead:

```hcl
keyvault_name = "<new-unique-name>"   # 24 characters or fewer
```

Run `make apply`, then `make seed-secrets` to write the LangSmith app secrets into the new vault.

### Key Vault secrets already exist but are not in Terraform state

**Symptom**

```txt
Error: a resource with the ID "https://<vault>.vault.azure.net/secrets/langsmith-license-key/..."
already exists - to be managed via Terraform this resource needs to be imported into the State.
```

**Cause:** Something wrote the secret to Key Vault outside Terraform, or the state file lost the resource. Terraform manages only two secrets, `postgres-admin-password` and `langsmith-license-key`. With `keyvault_manage_secrets = false`, `make seed-secrets` writes both instead, so setting the flag back to `true` afterward causes this collision. An existing vault attached with `create_keyvault = false` that already holds either secret causes it too. The LangSmith app secrets have no Terraform resource and never produce this error.

**Fix:** Import the conflicting secret, then re-apply. Get `<vault>` from `make tf ARGS="output keyvault_name"`.

```bash
terraform -chdir=infra import \
  'module.keyvault.azurerm_key_vault_secret.langsmith_license_key[0]' \
  "$(az keyvault secret show --vault-name <vault> --name langsmith-license-key --query id -o tsv)"

make apply
```

For `postgres-admin-password`, import into `module.keyvault.azurerm_key_vault_secret.postgres_admin_password[0]`. To keep Terraform out of the vault's secrets entirely, set `keyvault_manage_secrets = false` and let `make seed-secrets` write all of them. On a deployment that already applied, drop both secrets from state first, or Terraform deletes them from the vault.

### Existing Key Vault: apply creates the role assignment, then fails with 403 on the secrets

**Symptom:** With `create_keyvault = false`, the apply gets past `azurerm_role_assignment` and fails on the first `azurerm_key_vault_secret` with `StatusCode=403`. `make seed-secrets` fails the same way.

**Cause:** One of three:

1. The vault firewall denies the apply host's IP. The message names `ForbiddenByFirewall` or the client address.
2. The deploying identity does not hold Key Vault Secrets Officer on the vault. Terraform does not create that grant for a vault it did not create.
3. The grant exists but has not propagated yet.

**Fix:**

```bash
# 1. Check the firewall, then allowlist the apply host
az keyvault show --name <vault> --query "properties.networkAcls" -o json
az keyvault network-rule add --name <vault> --ip-address "<apply-host-ip>/32"

# 2. Check the deploying identity's roles on the vault
az role assignment list --assignee "$(az ad signed-in-user show --query id -o tsv)" \
  --scope "$(az keyvault show --name <vault> --query id -o tsv)" \
  --include-inherited --query "[].roleDefinitionName" -o tsv

# 3. Confirm data-plane access, then re-run make apply
az keyvault secret list --vault-name <vault> --query "length(@)"
```

For cause 2, have the vault owner grant the deploying identity Key Vault Secrets Officer. For cause 3, wait a few minutes and re-run `make apply`. Setting `keyvault_manage_secrets = false` takes Terraform out of the vault's data plane, and `make seed-secrets` then writes the secrets under your own credentials, which also need Key Vault Secrets Officer.

### `make plan` or `make apply` stops: `ingress_controller is not set`

**Symptom:** `make plan`, `make apply`, or `make tf ARGS="apply"` exits before Terraform runs with `ingress_controller is not set, and this deployment runs ingress-nginx.`

**Cause:** The `ingress_controller` default changed from `nginx` to `envoy-gateway`. A deployment that never set the variable still runs ingress-nginx, and applying the new default would remove ingress-nginx and its load balancer, changing the public IP. A guard script stops the run until you choose.

**Fix:** Set `ingress_controller` in `terraform.tfvars`:

* To keep NGINX: `ingress_controller = "nginx"`.
* To move to Envoy Gateway: `ingress_controller = "envoy-gateway"`, then run `make apply`, `make init-values`, and `make deploy` back to back. LangSmith is unreachable from the apply until the deploy finishes. Update any DNS A record that points at the old IP.

## Application stage

### `Could not read aks_resource_group_name`

**Symptom:** After you upgrade the module, `make kubeconfig`, `make deploy`, or `make uninstall` stops with `Could not read aks_resource_group_name. Run 'make apply' to record it.`

**Cause:** The scripts read the cluster's resource group from the `aks_resource_group_name` output, which an apply from an earlier module release did not record.

**Fix:** Run `make apply`, then re-run the command.

### `dns_label` subdomain not resolving: TLS cert stuck pending

**Symptom:** `nslookup langsmith-demo.eastus.cloudapp.azure.com` returns NXDOMAIN. The cert-manager ACME challenge cannot complete; TLS certificate stays `READY: False`.

**Cause:** Azure assigns the DNS label to the public IP only when the ingress controller's LoadBalancer service carries the `service.beta.kubernetes.io/azure-dns-label-name` annotation. `make deploy` sets it; a direct `helm upgrade` does not.

**Fix with `ingress_controller = "envoy-gateway"` (the default):** The EnvoyProxy `langsmith-proxy` carries the annotation, and Envoy Gateway copies it onto the proxy service. Check both:

```bash
kubectl get envoyproxy langsmith-proxy -n envoy-gateway-system \
  -o jsonpath='{.spec.provider.kubernetes.envoyService.annotations}'
kubectl get svc -n envoy-gateway-system \
  -l gateway.envoyproxy.io/owning-gateway-name=langsmith-gateway \
  -o jsonpath='{.items[0].metadata.annotations.service\.beta\.kubernetes\.io/azure-dns-label-name}'
```

If either is missing, set `dns_label` in `terraform.tfvars`, then run `make init-values` and `make deploy`, which re-applies the EnvoyProxy. `make deploy` stops while `terraform.tfvars` and the generated values disagree on `dns_label`. Once DNS resolves, delete the stuck certificate as in the NGINX fix.

**Fix with `ingress_controller = "nginx"`:**

```bash
kubectl annotate svc ingress-nginx-controller -n ingress-nginx \
  service.beta.kubernetes.io/azure-dns-label-name=<dns_label> \
  --overwrite

# Wait 1-2 minutes, verify DNS resolves
nslookup <dns_label>.eastus.cloudapp.azure.com

# Delete the stuck cert to trigger re-issue
kubectl delete certificate langsmith-tls -n langsmith
```

### `istio-addon`: port 80/443 timeout, TLS handshake reset

**Symptom:** Site unreachable after `make deploy` with `ingress_controller = "istio-addon"`. Port 80 times out, port 443 resets.

`istio-addon` does not support `tls_certificate_source = "letsencrypt"`, because the add-on creates no IngressClass for the HTTP-01 solver. Use `dns01` with a custom domain, `existing`, or `none`.

**Causes (two compounding issues):**

1. **Wrong gateway label.** Kubernetes Ingress with `ingressClassName: istio` targets pods with label `istio: ingressgateway`. The AKS managed external gateway uses `istio: aks-istio-ingressgateway-external`.
2. **TLS secret in wrong namespace.** Istio SDS reads from the gateway pod namespace (`aks-istio-ingress`), not the app namespace (`langsmith`).

**Fix:** `make deploy` handles both automatically in the current scripts. If deploying manually, create an Istio `Gateway` targeting `istio: aks-istio-ingressgateway-external`, sync `langsmith-tls` to the `aks-istio-ingress` namespace, and create a `VirtualService` routing to the LangSmith frontend. See the [TROUBLESHOOTING.md source](https://github.com/langchain-ai/terraform/blob/main/modules/azure/TROUBLESHOOTING.md) for the full YAML.

### `letsencrypt-prod` ClusterIssuer missing

**Symptom:** `kubectl describe certificate langsmith-tls -n langsmith` shows `clusterissuers.cert-manager.io "letsencrypt-prod" not found`.

**Cause:** `deploy.sh` applies the `letsencrypt-prod` ClusterIssuer when `tls_certificate_source` is `letsencrypt` or `dns01`. Terraform never creates it. You hit this when `make deploy` has not run, when you ran `helm upgrade` directly, or when the `dns01` branch skipped the issuer because `langsmith_domain` was empty or the `cert_manager_identity_client_id` output was missing (`make deploy` prints a warning in both cases).

**Manual fix:** With `ingress_controller = "envoy-gateway"`, replace the `ingress:` solver in this command with the `gatewayHTTPRoute` solver that follows it.

```bash
kubectl apply -f - <<EOF
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: you@example.com
    privateKeySecretRef:
      name: letsencrypt-prod-account-key
    solvers:
    - http01:
        ingress:
          ingressClassName: nginx   # use "istio" with self-managed istio
EOF

kubectl delete certificate langsmith-tls -n langsmith
```

Solver for `ingress_controller = "envoy-gateway"`:

```yaml
    solvers:
    - http01:
        gatewayHTTPRoute:
          parentRefs:
          - name: langsmith-gateway
            namespace: langsmith
            kind: Gateway
```

### `langsmith-backend-auth-bootstrap` stuck in `CreateContainerConfigError`

**Cause:** The Job reads the admin password using key `initial_org_admin_password`. If the Secret was created with a different key name (for example `admin_password`), the container cannot start.

**Fix**

```bash
kubectl delete secret langsmith-config-secret -n langsmith
make k8s-secrets   # recreates with correct key names
make deploy
```

### Cannot roll back to an older chart version

**Cause:** LangSmith DB migrations are forward-only. Downgrading the chart leaves the DB at a revision the older app image cannot locate.

**Fix:** Roll forward to the version you were on (or newer). Set `langsmith_helm_chart_version` in `terraform.tfvars` and re-deploy. On a `v0.17.*` module tag, `make deploy` accepts only the chart 0.17 line. A deployment that has run chart 0.17 cannot return to 0.16. The `v0.16.*` tags are for installations that never left 0.16. Always test new chart versions in a separate environment before upgrading production.

### `make deploy` fails: `does not resolve to the chart 0.17 line`

**Cause:** The `CHART_VERSION` environment variable or `langsmith_helm_chart_version` names a chart outside the 0.17 line, such as a 0.16 version left from an earlier deploy. `v0.17.*` module tags deploy only chart 0.17.

**Fix:** Clear both to take the newest 0.17 patch (`unset CHART_VERSION`), or name a 0.17 patch such as `0.17.0`. To stay on chart 0.16, check out a `v0.16.*` module tag instead.

### `make init-values` fails: `enable_sso_oidc = true but the following Key Vault secrets are missing`

**Cause:** `enable_sso_oidc = true` disables basic auth, so the backend needs the OIDC client ID, client secret, and issuer URL. At least one of the `langsmith-oauth-*` secrets is not in Key Vault.

**Fix:** Write the missing secrets, then re-create the Kubernetes secret and deploy:

```bash
./infra/scripts/manage-keyvault.sh set langsmith-oauth-client-id '<client-id>'
./infra/scripts/manage-keyvault.sh set langsmith-oauth-issuer-url '<issuer-url>'
make keyvault   # set langsmith-oauth-client-secret; the prompt hides the value
make k8s-secrets
make init-values
make deploy
```

Set the client secret through `make keyvault` rather than on the command line, where it shows in the process list and in your shell history.

### Helm install times out

**Cause:** `langsmith-backend-auth-bootstrap` runs DB migrations on every `helm upgrade`; first install takes up to 5 minutes. Without `--timeout 20m`, Helm reports failure even though the install eventually succeeds.

**Fix:** `make deploy` already uses `--timeout 20m`. Running Helm manually, always include `--timeout 20m`.

## Add-ons

### Pods stay in `DEPLOYING`, never reach `HEALTHY`

**Cause:** `config.deployment.url` was empty or `config.deployment.tlsEnabled` was `false` when TLS is enabled. The operator builds agent endpoint URLs from these values.

**Fix:** `init-values.sh` automatically injects `url` and `tlsEnabled` after copying from examples. If deploying manually:

```yaml
config:
  deployment:
    enabled: true
    url: "https://langsmith-demo.eastus.cloudapp.azure.com"   # must include https://
    tlsEnabled: true   # must be true when tls_certificate_source = letsencrypt, dns01, or existing
```

### Insights add-on: `backend-ch-migrations` in `CreateContainerConfigError`

**Symptom:** Multiple pods fail with `CreateContainerConfigError` after enabling `enable_insights = true`. Logs: `secret "langsmith-clickhouse" not found`.

**Cause:** A `langsmith-values-insights.yaml` written by an older `init-values.sh` sets `clickhouse.external.enabled: true` with `existingSecretName: langsmith-clickhouse`. This overrides the in-cluster ClickHouse configuration and expects an external secret that does not exist.

**Fix:** `init-values.sh` no longer puts any ClickHouse configuration in the Insights file. For an existing deployment with this issue, overwrite the file and redeploy:

```bash
cat > helm/values/langsmith-values-insights.yaml << 'EOF'
insights:
  enabled: true
EOF
make deploy
```

For external ClickHouse, set `clickhouse_source = "external"` and re-run `make init-values`, which prompts for the connection details and creates the `langsmith-clickhouse` secret. The same symptom appears when a hand-made secret is missing a key. The chart requires all seven: `clickhouse_host`, `clickhouse_port`, `clickhouse_native_port`, `clickhouse_user`, `clickhouse_password`, `clickhouse_db`, and `clickhouse_tls`.

### Polly shows `Unable to connect to LangGraph server`

**Symptom:** Polly chat widget shows connection error. Browser console: `POST http://localhost:8123/threads net::ERR_FAILED` and CORS error.

**Cause A, frontend started before `langsmith-polly-config` was created.** The ConfigMap carrying `VITE_POLLY_DEPLOYMENT_URL` is written once Polly is registered. Env vars from ConfigMap load at pod start, not dynamically.

**Fix**

```bash
kubectl rollout restart deployment langsmith-frontend -n langsmith
kubectl exec -n langsmith deploy/langsmith-frontend -- env | grep POLLY
# expect: VITE_POLLY_DEPLOYMENT_URL=https://<hostname>/lgp/smith-polly-<hash>
```

**Cause B, `LANGCHAIN_ENDPOINT` set in `polly.agent.extraEnv`.** `LANGCHAIN_ENDPOINT` is reserved. Setting it makes registering Polly fail with `400 Bad Request: 'LANGCHAIN_ENDPOINT' is reserved`. Polly is never created.

**Fix:** Remove the `polly.agent.extraEnv` block entirely. The operator injects `LANGCHAIN_ENDPOINT` automatically.

### `listener` and `operator` pods never appear after enabling Agent Server hosting

**Cause:** `config.deployment.url` was set but `config.deployment.enabled: true` was omitted. The chart silently skips creating `listener` and `operator` when `enabled` is false (the default).

**Fix:** Add `enabled: true` inside the `deployment` block:

```yaml
config:
  deployment:
    enabled: true          # required; url alone is not enough
    url: "https://<your-hostname>"
```

### Duplicate top-level `config:` key silently drops values

**Cause:** YAML disallows duplicate top-level keys. A second `config:` block silently drops one of them.

**Fix:** Always add new config blocks inside the existing `config:` key. Verify with `helm get values langsmith -n langsmith`.

### Encryption keys must not change after first deploy

Changing `deployments_encryption_key`, `agent_builder_encryption_key`, `insights_encryption_key`, or `polly_encryption_key` after their first use permanently corrupts the data they protect. There is no recovery.

* Do not rotate these keys.
* Do not set `config.agentBuilder.encryptionKey`, `fleet.encryptionKey`, `insights.encryptionKey`, or `polly.encryptionKey` inline in `values-overrides.yaml`. The chart reads them from `langsmith-config-secret` via `existingSecretName`. Setting inline overrides the secret reference.

### `fleet-tool-server` or `polly` in CrashLoopBackOff

**Symptom:** Pod restarts indefinitely. No traceback. Logs show "Child process died" repeatedly.

**Cause:** A settings validation error at import time exits the uvicorn worker with code 0, and the parent process swallows the traceback. Common triggers: `BASIC_AUTH_ENABLED = true` but `BASIC_AUTH_JWT_SECRET` is empty, or a required feature-flag key absent from `langsmith-config`.

**Diagnose** by running the server in a debug pod with `envFrom` pointing at `langsmith-config` and `PYTHONUNBUFFERED=1`. **Fix:** add the missing key to Key Vault, rerun `make k8s-secrets`, restart the deployment.

## Workload Identity

### Pod panics: `AADSTS700213: No matching federated identity record found`

**Symptom**

```txt
panic: blob-storage health-check failed: get container properties failed:
DefaultAzureCredential: failed to acquire a token.
WorkloadIdentityCredential authentication failed.
  AADSTS700213: No matching federated identity record found for presented assertion subject
  'system:serviceaccount:langsmith:langsmith-<service>'
```

**Cause:** The pod's Kubernetes ServiceAccount has no federated credential on the Azure Managed Identity. Every pod that accesses Blob Storage needs one.

**Fix:** Add the missing ServiceAccount to `service_accounts_for_workload_identity` in `infra/modules/k8s-cluster/main.tf`. The module passes the chart fullname as `var.langsmith_release_name`: the release name when it contains `langsmith`, otherwise `<release>-langsmith`. The list on the `v0.17.*` module tags:

```hcl
service_accounts_for_workload_identity = [
  "${var.langsmith_release_name}-backend",
  "${var.langsmith_release_name}-platform-backend",
  "${var.langsmith_release_name}-queue",
  "${var.langsmith_release_name}-ingest-queue",
  "${var.langsmith_release_name}-host-backend",          # Agent Server hosting add-on
  "${var.langsmith_release_name}-listener",              # Agent Server hosting add-on
  "${var.langsmith_release_name}-fleet-tool-server",     # Fleet add-on
  "${var.langsmith_release_name}-fleet-trigger-server",  # Fleet add-on
  "${var.langsmith_release_name}-agent-gateway",         # LLM Gateway add-on
  "${var.langsmith_release_name}-presidio-analyzer",     # LLM Gateway PII redaction
]
```

The `v0.16.*` module tags list all except the two LLM Gateway entries.

```bash
make apply
kubectl rollout restart deployment/langsmith-<service> -n langsmith
```

See the [architecture page](Azure%20Terraform%20architecture.md#workload-identity) for the full pod-to-WI mapping.

## Teardown and cleanup

### `make clean` before `make destroy` orphans infrastructure

**Symptom:** `make destroy` after `make clean` fails with `No state file was found!`. Azure resources still run but Terraform has lost tracking.

**Cause:** `make clean` removes `terraform.tfvars`, `secrets.auto.tfvars`, and the local `terraform.tfstate` and its backups. It warns when state still tracks resources, but continues once you confirm. `make clean-force` gives that confirmation for you.

**Correct teardown order**

```txt
1. make uninstall   ← Helm release, then the namespace if you confirm
2. make destroy     ← Azure infra (needs tfstate + tfvars)
3. make clean       ← local secrets and generated files (LAST)
```

`make uninstall` asks before it deletes the namespace, and the default answer is No. Answer `y` to remove the namespace and everything left in it.

**Recovery when tfstate is gone**

```bash
az group delete --name langsmith-rg-<name_prefix> --yes --no-wait
az group show --name langsmith-rg-<name_prefix> 2>&1 | grep -E "provisioningState|ResourceGroupNotFound"
```

With `unique_resource_names = true`, the resource group is `ls-rg-<name_prefix>`. Do not delete the group when `create_resource_group = false`, since the module did not create it.

If you reuse the same `name_prefix` afterwards, Azure may recover the soft-deleted Key Vault on the next `terraform apply`. With `keyvault_purge_protection = false`, purge it first. Find its name with `az keyvault list-deleted -o table`, then run `az keyvault purge --name <vault> --location <region>`.

### `terraform destroy` stalls on VNet/subnet deletion

**Cause:** The Azure Load Balancer for the ingress controller's LoadBalancer service (the Envoy proxy service for `envoy-gateway`, `ingress-nginx-controller` for `nginx`) is not tracked by Terraform. Azure blocks VNet deletion while the LB holds a subnet reference.

**Fix:** Run `make uninstall` first. With `envoy-gateway`, it deletes the Gateway, which removes the proxy service and its LB. With `nginx`, also uninstall ingress-nginx.

```bash
make uninstall
helm uninstall ingress-nginx -n ingress-nginx --wait   # only with ingress_controller = "nginx"
kubectl delete namespace langsmith --timeout=60s
make destroy
```

### Orphaned `langsmith-agent-bootstrap` Job after upgrading to chart 0.16

**Symptom:** A Completed `langsmith-agent-bootstrap` Job remains in the namespace after upgrading from chart 0.15, and `helm uninstall` leaves it behind.

**Cause:** Chart 0.16 removed the bundled agent-bootstrap Job, so Helm no longer owns the object the 0.15 release created. The Azure `deploy.sh` does not delete it.

**Fix:** The Job blocks nothing. Delete it to keep the namespace clean:

```bash
kubectl delete job langsmith-agent-bootstrap -n langsmith --ignore-not-found
```

### `listener` pods OOMKilled

**Cause:** `make deploy` loads the sizing file after the add-on overlays, so its listener limit wins over the `langsmith-values-agent-deploys.yaml` overlay. The `dev` and `production` profiles cap the listener at `2Gi`, and `minimum` caps it at `1536Mi`. Sustained Deployments load can exceed that limit.

**Fix:** Set `sizing_profile = "production-large"` in `terraform.tfvars`, which gives the listener `4Gi`, then run `make init-values` and `make deploy`. To stay on your profile, raise `listener.deployment.resources.limits.memory` in `helm/values/langsmith-values-sizing-<profile>.yaml` and run `make deploy`. `make init-values` copies the sizing file again, so repeat the edit after each run.

> [!NOTE]
>
> The chart reads `listener.deployment.resources` for container limits, not the flat `listener.resources`. A `listener.resources` value in any overlay file is silently ignored.

### Stale HPA scales `listener` or `host-backend` to max replicas

**Cause:** A prior Helm revision created an HPA. Helm does not clean it up on failed hooks. On re-deploy with `enabled: false`, the stale HPA remains and overrides `replicas`.

**Fix**

```bash
kubectl delete hpa langsmith-listener langsmith-host-backend -n langsmith 2>/dev/null || true
kubectl scale deployment langsmith-listener -n langsmith --replicas=1
kubectl scale deployment langsmith-host-backend -n langsmith --replicas=1
make deploy
```

## AGIC (Application Gateway Ingress Controller)

### AGIC pod CrashLoopBackOff: 403 on AGW GET

**Symptom:** `ingress-appgw-deployment` is CrashLoopBackOff. Logs: `ErrorApplicationGatewayForbidden: does not have authorization to perform action Microsoft.Network/applicationGateways/read`.

**Cause:** The AGIC add-on's managed identity (`ingressapplicationgateway-<cluster>` in the `MC_` resource group) takes \~5 minutes to register in Microsoft Entra ID before its role assignments take effect.

**Fix:** The `k8s-cluster` module waits 300s after cluster creation (`time_sleep.agic_identity_propagation`) and creates the three required role assignments automatically. If AGIC is still 403 after `make apply`:

```bash
az aks update --name <CLUSTER> --resource-group <RG> --yes
kubectl delete pod -n kube-system -l app=ingress-azure
```

For manual role assignments (Reader on RG, Contributor on AGW, Network Contributor on VNet), see the [TROUBLESHOOTING.md source](https://github.com/langchain-ai/terraform/blob/main/modules/azure/TROUBLESHOOTING.md#agic-pod-crashloopbackoff--403-on-agw-get).

### AGIC: `ApplicationGatewayInsufficientPermissionOnSubnet`

**Cause:** AGIC add-on identity missing Network Contributor on the VNet.

**Fix**

```bash
AGIC_OID=$(az aks show -g <RG> -n <CLUSTER> \
  --query "addonProfiles.ingressApplicationGateway.identity.objectId" -o tsv)
VNET_ID=$(az network vnet show -g <RG> -n <VNET> --query id -o tsv)

az role assignment create --role "Network Contributor" --scope "$VNET_ID" \
  --assignee-object-id "$AGIC_OID" --assignee-principal-type ServicePrincipal

kubectl rollout restart deployment/ingress-appgw-deployment -n kube-system
```

### AGIC: `SecretNotFound` for TLS secret

**Cause:** AGIC saw the Ingress before cert-manager issued the TLS certificate.

**Fix:** Touch the Ingress to trigger re-sync:

```bash
kubectl get certificate langsmith-tls -n langsmith   # verify cert is ready
kubectl annotate ingress langsmith-ingress -n langsmith touch="$(date +%s)" --overwrite
```

### AGIC rejects `ingressClassName: azure/application-gateway`

**Cause:** The legacy annotation `kubernetes.io/ingress.class: azure/application-gateway` (with slash) is not a valid `ingressClassName`. AKS creates the `IngressClass` as `azure-application-gateway` (hyphen).

**Fix:** Use `ingressClassName: azure-application-gateway`. `make init-values` sets this automatically.

## Istio (self-managed Helm)

### Istio site returns connection refused / no routes

**Symptom:** Connection refused. `pilot-agent request GET config_dump` shows `LDS: PUSH resources:0`.

**Root causes (all three must be fixed):**

1. `meshConfig.ingressControllerMode` not set. Default is `DEFAULT`, which ignores `ingressClassName`. Must be `STRICT`.
2. `istio` IngressClass resource missing.
3. `meshConfig.ingressClass` not set to `istio`.

**Fix:** All three are automated. `meshConfig` is set in the istiod Helm release (Terraform), and `deploy.sh` creates the IngressClass. Manual fix: create the IngressClass and restart istiod.

### Istio HTTPS returns "no peer certificate available"

**Cause:** istiod reads the TLS secret via SDS (`kubernetes://langsmith-tls`). The secret must exist in `istio-system` (the gateway pod namespace). cert-manager issues it to the `langsmith` namespace; it is not copied automatically.

**Fix:** `deploy.sh` syncs the secret post-deploy. Manual fix: copy the secret to `istio-system`.

### Leftover CRDs from `istio-addon` block self-managed Helm install

**Symptom:** `make apply` fails: `CustomResourceDefinition "wasmplugins.extensions.istio.io" exists and cannot be imported into the current release: invalid ownership metadata`.

**Fix**

```bash
kubectl get crd | grep "istio.io" | awk '{print $1}' | xargs kubectl delete crd
make apply
```

## Diagnostic commands

### Cluster access

```bash
make kubeconfig
kubectl config current-context
kubectl get nodes -o wide
```

### Pods

```bash
kubectl get pods -n langsmith
kubectl get pods -n langsmith -w
kubectl describe pod <pod-name> -n langsmith
kubectl logs <pod-name> -n langsmith --tail=100 -f
kubectl logs <pod-name> -n langsmith --previous --tail=50
```

### Ingress and TLS

```bash
kubectl get gateway,httproute -n langsmith                     # envoy-gateway
kubectl get svc -n envoy-gateway-system \
  -l gateway.envoyproxy.io/owning-gateway-name=langsmith-gateway  # envoy-gateway
kubectl get ingress -n langsmith                                # nginx, istio, agic
kubectl get svc ingress-nginx-controller -n ingress-nginx       # nginx
kubectl get certificate -n langsmith
kubectl get challenges -n langsmith
kubectl get clusterissuer
```

### Workload Identity

```bash
kubectl get serviceaccount langsmith-ksa -n langsmith \
  -o jsonpath='{.metadata.annotations.azure\.workload\.identity/client-id}'

kubectl get pod <pod> -n langsmith \
  -o jsonpath='{.metadata.labels.azure\.workload\.identity/use}'
```

### Helm

```bash
helm status langsmith -n langsmith
helm history langsmith -n langsmith
helm get values langsmith -n langsmith
```

### Agent Server hosting

```bash
kubectl get pods -n langsmith | grep -E "host-backend|listener|operator"
kubectl get lgp -n langsmith
kubectl get crd | grep langchain
```

### Key Vault and Kubernetes Secrets

```bash
./infra/scripts/manage-keyvault.sh list
./infra/scripts/manage-keyvault.sh validate
./infra/scripts/manage-keyvault.sh diff

kubectl get secrets -n langsmith
kubectl get secret langsmith-config-secret -n langsmith -o jsonpath='{.data}' | jq 'keys'
```

### Quick health check

```bash
make status         # full automated check
make status-quick   # skip the Key Vault, kubeconfig, Kubernetes, and Helm checks
```

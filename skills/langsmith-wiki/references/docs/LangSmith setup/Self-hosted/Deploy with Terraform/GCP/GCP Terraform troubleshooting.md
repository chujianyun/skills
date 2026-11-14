# GCP Terraform troubleshooting

> Common issues, fixes, and diagnostic commands for LangSmith self-hosted on GKE deployed with the LangChain Terraform modules.

This page documents common issues, fixes, and diagnostic commands for LangSmith deployments provisioned with the [GCP Terraform modules](https://github.com/langchain-ai/terraform/tree/main/modules/gcp).

> [!TIP]
>
> Before upgrading, review the [LangSmith self-hosted changelog](../../Reference/Self-hosted%20LangSmith%20changelog.md) for breaking changes and required variable updates. Run `gcloud container clusters get-credentials <cluster-name> --region <region> --project <project-id>` before running any `kubectl` commands.

For a copy-paste reference of the `kubectl`, `helm`, and `gcloud` calls used throughout this page, skip to [Diagnostic commands](#diagnostic-commands).

## Automated diagnostics

Before running individual commands, try the bundled scripts:

```bash
# Full deployment health check + next-step guidance
make status

# Check that all required secrets exist in Secret Manager
./infra/scripts/manage-secrets.sh validate

# Interactive Secret Manager tool (list, get, set, validate, delete)
make secrets
```

## Known issues

### terraform apply fails: GCP APIs not enabled

**Symptom**

```
Error 403: ... has not been used in project <project-id> before or it is disabled.
```

**Cause:** Required GCP APIs are not enabled. Terraform enables them via `google_project_service`, but `cloudresourcemanager.googleapis.com` must already be enabled for Terraform to enable the others.

**Fix**

```bash
gcloud services enable cloudresourcemanager.googleapis.com --project <project-id>
cd modules/gcp/infra
terraform apply
```

### GKE cluster API server not accessible after apply

**Symptom**

```
Error: Get "https://<cluster-endpoint>/api/v1/namespaces": dial tcp: connection refused
```

**Cause:** The GKE control plane takes 10 to 15 minutes to become fully operational. Terraform waits for `RUNNING` then adds a 90-second buffer. Cold-start API activation on slow projects can exceed the window.

**Fix:** Wait for `RUNNING`, then re-run:

```bash
gcloud container clusters describe <cluster-name> \
  --region <region> --project <project-id> --format="value(status)"

terraform apply
```

### GKE nodes not joining (NotReady)

**Symptom:** `kubectl get nodes` shows no nodes or nodes stuck in `NotReady`.

**Cause:** Node pool service account lacks `roles/container.nodeServiceAccount`, or VPC firewall rules block node-to-control-plane communication.

**Fix**

```bash
gcloud container node-pools describe <pool-name> \
  --cluster <cluster-name> --region <region> \
  --format="value(config.serviceAccount)"

gcloud projects add-iam-policy-binding <project-id> \
  --member="serviceAccount:<node-sa-email>" \
  --role="roles/container.nodeServiceAccount"

gcloud compute firewall-rules list --filter="network:<vpc-name>"
```

### Cloud SQL connection refused from GKE pods

**Symptom:** Backend logs show `connection refused` or `no route to host` for the Cloud SQL private IP.

**Cause:** The private service connection (VPC peering) is not established, or the allocated IP range is too small. Often happens when `servicenetworking.googleapis.com` was not enabled before the networking module ran.

**Fix**

```bash
gcloud services vpc-peerings list --network <vpc-name> --project <project-id>
gcloud sql instances describe <instance-name> --format="value(ipAddresses)"
gcloud compute networks peerings list --network <vpc-name>
```

Terraform creates the private service connection when `postgres_source = "external"`, `redis_source = "external"`, `enable_sandboxes = true`, or SmithDB creates its own metastore. If peering is missing, confirm one of those settings is in `terraform.tfvars` and re-apply:

```bash
terraform apply -target=module.networking
terraform apply
```

### Memorystore Redis connection timeout

**Symptom:** Pods cannot connect to Redis. Logs show `dial tcp: connection timed out` or `redis: connection refused`.

**Cause:** The Memorystore `authorized_network` does not match the GKE VPC, or the Redis private IP is on a range not routable from the GKE subnet.

**Fix**

```bash
gcloud redis instances describe <instance-name> --region <region> \
  --format="value(host,authorizedNetwork)"

kubectl run redis-test --rm -it --image=redis:7 -n langsmith -- \
  redis-cli -h <redis-private-ip> ping
# Expected: PONG
```

### cert-manager fails to issue Let's Encrypt certificate

**Symptom:** `kubectl get certificate -n langsmith` shows `READY=False`. HTTP01 challenge failing.

**Cause:** The DNS A record does not point to the Envoy Gateway IP, or port 80 is blocked on the load balancer.

**Fix**

```bash
kubectl get gateway -n envoy-gateway-system \
  -o jsonpath='{.items[0].status.addresses[0].value}'

kubectl describe certificate <cert-name> -n langsmith
kubectl get challenges -n langsmith
kubectl describe challenge -n langsmith

dig +short <your-langsmith-domain>
```

The DNS A record must resolve to the Gateway IP before the certificate can be issued. cert-manager's HTTP01 solver needs port 80 to be reachable from the internet.

### GCS bucket access denied from LangSmith pods

**Symptom:** Backend logs show `AccessDeniedException: 403 Insufficient Permission` or `403 Forbidden` when writing to GCS.

**Cause:** In native GCS mode (the shipped default), the GCP service account bound through Workload Identity lacks `roles/storage.objectAdmin` on the bucket, or the pod's Kubernetes ServiceAccount is missing the `iam.gke.io/gcp-service-account` annotation. In the optional S3-compatible mode, the HMAC credentials passed to Helm are incorrect or their service account lacks `roles/storage.objectAdmin`.

**Fix**

```bash
# Confirm the bucket and its IAM bindings
helm get values langsmith -n langsmith | grep bucketName
gcloud storage buckets get-iam-policy gs://<bucket-name>

# Native GCS mode: verify the Workload Identity annotation on the pod ServiceAccount
kubectl get serviceaccount langsmith-backend -n langsmith \
  -o jsonpath='{.metadata.annotations.iam\.gke\.io/gcp-service-account}'
```

The GCP service account must have `roles/storage.objectAdmin` on the bucket. If the annotation itself is missing, apply the fix in the Workload Identity section below. For S3-compatible mode, create an HMAC key under **Cloud Storage** > **Settings** > **Interoperability**; its service account also needs `roles/storage.objectAdmin` on the bucket.

### Envoy Gateway webhook blocking GKE operations

**Symptom**

```
Error from server (InternalError): failed calling webhook "validate.gateway.envoyproxy.io"
```

**Cause:** The Envoy Gateway admission webhook is not ready or its `caBundle` is stale.

**Fix**

```bash
kubectl get pods -n envoy-gateway-system

kubectl rollout restart deployment/envoy-gateway -n envoy-gateway-system
kubectl rollout status deployment/envoy-gateway -n envoy-gateway-system
```

### Envoy Gateway external IP changed after re-apply

**Symptom:** DNS no longer resolves to the correct IP after Terraform re-apply, or existing firewall allowlists stop working.

**Cause:** The Envoy Gateway external IP is tied to the `Gateway` Kubernetes resource managed by Terraform. If the resource is deleted and recreated (`terraform taint`, a module change that forces replacement, or `terraform destroy` + re-apply), GCP issues a new IP. There is no way to reserve the original IP without pre-allocating a static regional address.

**Prevention**

* Do not `terraform taint` or manually delete the `Gateway` resource.
* Use `make destroy` + `make apply` only for full teardown and rebuild.
* Before any operation that might recreate the Gateway, note the current IP.

**Recovery:** Update your DNS A record to the new IP:

```bash
kubectl get gateway -n envoy-gateway-system -o jsonpath='{.items[0].status.addresses[0].value}'

gcloud dns record-sets update <your-domain>. \
  --type=A --ttl=300 \
  --rrdatas=<new-ip> \
  --zone=<zone-name> \
  --project=<project-id>
```

### terraform destroy fails: deletion protection enabled

**Symptom**

```
Error: googleapi: Error 409: The instance is protected from deletion.
```

**Cause:** `gke_deletion_protection`, `postgres_deletion_protection`, or `smithdb_metastore_deletion_protection` is `true`. Cloud SQL enforces deletion protection at the API level as well as in Terraform, so changing `terraform.tfvars` has no effect until the change is applied.

**Fix**

```hcl
# terraform.tfvars
gke_deletion_protection      = false
postgres_deletion_protection = false

# Only when enable_smithdb = true and smithdb_metastore_source = "create"
smithdb_metastore_deletion_protection = false
smithdb_bucket_force_destroy          = true
```

```bash
source infra/scripts/setup-env.sh

terraform -chdir=infra apply \
  -target=module.gke_cluster -target=module.cloudsql \
  -target=module.smithdb -target=module.networking

make destroy
```

Drop the `module.smithdb` target if you never enabled SmithDB. The targeted apply avoids reconciling the in-cluster add-ons that a full `make apply` would recreate.

### Workload Identity not working (GCS permission denied)

**Symptom**

```
AccessDeniedException: 403 <pod-sa>@<project>.iam.gserviceaccount.com
  does not have storage.objects.create access to the Google Cloud Storage bucket.
```

**Cause:** The Kubernetes ServiceAccount used by LangSmith pods is missing the Workload Identity annotation, or the GCP SA is missing the GCS IAM binding.

**Diagnosis**

```bash
kubectl get serviceaccount langsmith-backend -n langsmith \
  -o jsonpath='{.metadata.annotations}' | python3 -m json.tool

BUCKET=$(terraform -chdir=infra output -raw storage_bucket_name)
gsutil iam get gs://$BUCKET | grep -A3 "serviceAccount"

GSA=$(terraform -chdir=infra output -raw workload_identity_service_account_email)
gcloud projects get-iam-policy <project-id> \
  --flatten="bindings[].members" --filter="bindings.members:$GSA"
```

**Fix**

```bash
terraform -chdir=infra apply -target=module.iam
make init-values
make deploy
```

### `langsmith-ksa` missing Workload Identity annotation

**Symptom:** Operator-spawned agent pods fail to start or get stuck in `Pending`. Logs show permission errors.

**Cause:** Terraform creates `langsmith-ksa` in the `k8s-bootstrap` module and annotates it only when `enable_gcp_iam_module = true`. `deploy.sh` re-applies the annotation after each deploy. The annotation is missing if the IAM module is off, the namespace was deleted out-of-band, or a previous deploy was interrupted.

**Diagnosis**

```bash
kubectl get serviceaccount langsmith-ksa -n langsmith \
  -o jsonpath='{.metadata.annotations.iam\.gke\.io/gcp-service-account}'
```

**Fix**

If `enable_gcp_iam_module = false`, set it to `true` in `terraform.tfvars` and run `make apply`. For the other causes, re-run the deploy or annotate the ServiceAccount manually:

```bash
# Re-run deploy; idempotently creates and annotates langsmith-ksa
make deploy

# Or annotate manually
WI=$(terraform -chdir=infra output -raw workload_identity_annotation)
kubectl create serviceaccount langsmith-ksa -n langsmith --dry-run=client -o yaml \
  | kubectl apply -f -
kubectl annotate serviceaccount langsmith-ksa -n langsmith \
  iam.gke.io/gcp-service-account="$WI" --overwrite
```

### Deploy refuses chart 0.16 sandbox values

**Symptom**

```txt
ERROR: values-overrides.yaml carries sandboxes.juicefs.csi, the chart 0.16 sandbox schema.
```

**Cause:** `values-overrides.yaml` was generated for chart 0.16. Chart 0.17 has no JuiceFS CSI driver and ignores the `sandboxes.juicefs.csi` block.

**Fix:** Run `make apply`, then `make init-values` to regenerate the file, then `make deploy`.

### Deploy refuses while JuiceFS CSI volumes remain

**Symptom**

```txt
ERROR: namespace langsmith still mounts sandbox volumes through the chart 0.16 JuiceFS CSI driver.
```

**Cause:** Chart 0.17 removes the JuiceFS CSI driver. Upgrading while PersistentVolumeClaims or mount pods still use it leaves the old sandbox-host pods stuck in `Terminating`.

**Fix:** Run the `kubectl delete` commands that the error prints while the driver still runs. Wait until `kubectl get pods -n langsmith | grep juicefs` lists only `juicefs-csi-*` pods, then run `make deploy` again. Running sandboxes stop. Their data stays in object storage and Redis, and chart 0.17 mounts the same JuiceFS volume.

### Deploy refuses the chart 0.16 SmithDB overlay

**Symptom**

```txt
ERROR: langsmith-values-smithdb.yaml has chart 0.16 SmithDB values that chart 0.17 rejects:
```

**Cause:** `init-values.sh` copies the SmithDB overlay only once, so a chart 0.16 copy stays in `helm/values/`. It sets the `local-ssd-storage` volume or `smithdb.migration.deployment`, which chart 0.17 replaces.

**Fix:** Save your copy and start from the 0.17 example:

```bash
cp helm/values/langsmith-values-smithdb.yaml helm/values/langsmith-values-smithdb-0.16.yaml
cp helm/values/examples/langsmith-values-smithdb.yaml helm/values/langsmith-values-smithdb.yaml
```

Add back only the edits that do not set `nodeSelector`, `tolerations`, `volumes`, `volumeMounts`, or `resources`. The generated `langsmith-values-smithdb-sizing.yaml` now sets those.

### `init-values.sh` fails with missing SmithDB outputs

**Symptom**

```txt
ERROR: enable_smithdb = true but smithdb_helm_values or the resolved metastore TLS
       outputs are missing. The state is older than this module. Run 'make apply'.
```

**Cause:** The Terraform state predates the chart 0.17 module, which adds the SmithDB sizing and metastore outputs.

**Fix:** Run `make apply`, then `make init-values`.

### Deploy refuses because the SmithDB backfill Job changed

**Symptom**

```txt
ERROR: the existing <job-name> Job does not match what this deploy renders,
       and a Job's pod template cannot be changed in place:
```

**Cause:** A chart upgrade or a sizing change renders a different pod template for the backfill Job, and Kubernetes does not allow changing a Job's pod template.

**Fix:** Delete the Job with the command the error prints, then run `make deploy` again. The backfill keeps its progress in the task database, so the new Job resumes instead of starting over.

### JuiceFS format Job fails

**Symptom**

```txt
✗ The JuiceFS format Job for release langsmith failed (<reason>).
```

**Cause:** The `juicefs-format` Job formats the sandbox volume in the GCS bucket through the `langsmith-sandbox-host` Workload Identity binding. When the reason is `DeadlineExceeded`, the Job did not finish within 300 seconds, usually because the pod could not schedule or the image pull was slow. For any other reason, the binding is usually missing or out of date.

**Fix:**

1. Find the cause. For `DeadlineExceeded`, look for `FailedScheduling` events or a slow image pull:

   ```bash
   kubectl describe job -n langsmith -l app.kubernetes.io/component=juicefs-format
   ```

   For any other reason, read the Job logs, then run `make apply` to restore the Workload Identity binding:

   ```bash
   kubectl logs -n langsmith -l app.kubernetes.io/component=juicefs-format
   ```

2. Delete the failed Job and deploy again. Helm does not rerun a failed Job when its manifest is unchanged, so the Job must be deleted first:

   ```bash
   kubectl delete job -n langsmith -l app.kubernetes.io/component=juicefs-format
   make deploy
   ```

### Helm release stuck in `pending-upgrade`

**Symptom**

```
Error: UPGRADE FAILED: another operation (install/upgrade/rollback) is in progress
```

**Cause:** A previous `helm upgrade` was interrupted (Ctrl+C during `--wait`). Helm left the release locked.

**Fix:** `deploy.sh` detects and auto-recovers this state. If running manually:

```bash
helm rollback langsmith -n langsmith --wait --timeout 5m
make deploy
```

### Secret Manager access denied

**Symptom**

```
ERROR: PERMISSION_DENIED: Permission 'secretmanager.versions.access'
  denied on resource 'projects/.../secrets/...'
```

**Cause:** Either `secretmanager.googleapis.com` is not enabled, or the operator account lacks `roles/secretmanager.admin`.

**Fix**

```bash
gcloud services enable secretmanager.googleapis.com --project <project-id>

gcloud projects add-iam-policy-binding <project-id> \
  --member="user:$(gcloud config get account)" \
  --role="roles/secretmanager.admin"
```

A workload you added that reads Secret Manager as the LangSmith service account loses access after an upgrade to `main` or a `v0.17.x` tag, because the project-wide `roles/secretmanager.secretAccessor` grant is now opt-in. Grant access on the specific secrets, or set `grant_project_secret_accessor = true` and run `make apply`.

### `langsmith-postgres-credentials` or `langsmith-redis-credentials` Secret missing

**Symptom:** Pods crash with database connection errors immediately after deploy, or `kubectl get secrets -n langsmith` does not list `langsmith-postgres-credentials` / `langsmith-redis-credentials`.

**Cause:** The `k8s-bootstrap` module creates these Secrets when `postgres_source` or `redis_source` is `external`. They are absent if `terraform apply` was not run, failed partway through, or the namespace was deleted out-of-band.

**Fix**

```bash
terraform -chdir=infra apply -target=module.k8s_bootstrap

kubectl get secret langsmith-postgres-credentials -n langsmith
kubectl get secret langsmith-redis-credentials -n langsmith
```

## Diagnostic commands

### Cluster access

```bash
gcloud container clusters get-credentials <cluster-name> --region <region> --project <project-id>
kubectl config current-context
kubectl get nodes -o wide
```

### Pods

```bash
kubectl get pods -n langsmith
kubectl get pods -n langsmith -w
kubectl describe pod <pod-name> -n langsmith
kubectl logs <pod-name> -n langsmith --tail=50
kubectl logs <pod-name> -n langsmith --previous --tail=50
kubectl logs -n langsmith deploy/langsmith-backend --tail=100 -f
```

### TLS and certificates

```bash
kubectl get certificate -n langsmith
kubectl describe certificate <cert-name> -n langsmith
kubectl get challenges -n langsmith
kubectl get clusterissuer
```

### Gateway and load balancer

```bash
kubectl get gateway -n envoy-gateway-system
kubectl get httproute -n langsmith
kubectl get svc -n envoy-gateway-system -o wide
kubectl get pods -n envoy-gateway-system
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

### Workload Identity and IAM

```bash
kubectl get serviceaccount langsmith-backend -n langsmith \
  -o jsonpath='{.metadata.annotations}' | python3 -m json.tool

kubectl get serviceaccount langsmith-ksa -n langsmith \
  -o jsonpath='{.metadata.annotations.iam\.gke\.io/gcp-service-account}'

BUCKET=$(terraform -chdir=infra output -raw storage_bucket_name 2>/dev/null)
gsutil iam get gs://$BUCKET

gcloud iam service-accounts list --project <project-id> --filter="displayName:langsmith"
```

### Secrets and bootstrap

```bash
kubectl get secrets -n langsmith
kubectl get secret langsmith-postgres-credentials -n langsmith
kubectl get secret langsmith-redis-credentials -n langsmith

kubectl get secret langsmith-postgres-credentials -n langsmith \
  -o jsonpath='{.data.connection_url}' | base64 --decode

gcloud secrets list --project <project-id> --filter="name:langsmith"

gcloud secrets versions access latest \
  --secret=langsmith-<prefix>-<env>-postgres-password \
  --project <project-id>

./infra/scripts/manage-secrets.sh validate
```

### Quick health check

```bash
echo "=== Context ===" && kubectl config current-context
echo "=== Nodes ===" && kubectl get nodes
echo "=== Pods ===" && kubectl get pods -n langsmith
echo "=== Certificate ===" && kubectl get certificate -n langsmith
echo "=== Gateway ===" && kubectl get gateway -n envoy-gateway-system
echo "=== Secrets ===" && kubectl get secrets -n langsmith | grep -E "langsmith-postgres-credentials|langsmith-redis-credentials"
echo "=== Helm ===" && helm status langsmith -n langsmith 2>/dev/null | grep -E "STATUS|LAST DEPLOYED"
```

# Install Mission Control

> Install Mission Control, an in-cluster console for monitoring, configuring, and operating self-hosted LangSmith on Kubernetes.

Mission Control is an in-cluster console for monitoring, configuring, and operating LangSmith on Kubernetes. It runs inside your cluster and is accessed with `kubectl port-forward` by default, so no ingress is required.

There are two install paths:

| Path | Best for |
| - | - |
| [Quick install](#quick-install) | Customers who can run a reviewed shell installer and want the shortest setup. |
| [Manual install](#manual-install) | Organizations that do not allow installer scripts or need each Kubernetes command reviewed. |

The public install assets are:

* `install-script.sh`: one installer with separate `prereqs`, `namespace`, `secret`, `values`, `install`, and `forward` steps.
* `values.yaml`: default Helm values for a port-forward-only install.

Mission Control images are published to two Docker Hub repositories: `langchain/mission-control-backend` and `langchain/mission-control-frontend`. The latest images can be checked with:

```bash
docker pull langchain/mission-control-backend:latest
docker pull langchain/mission-control-frontend:latest
```

Browser review links:

* `https://github.com/langchain-ai/helm/tree/main/charts/mission-control/install-script.sh`
* `https://github.com/langchain-ai/helm/tree/main/charts/mission-control/values.yaml`

The commands below use raw GitHub URLs so `curl` can download the files directly. If you publish these files from a different repo or branch, replace the raw base URL below.

```bash
MC_RAW_BASE=https://raw.githubusercontent.com/langchain-ai/helm/main/charts/mission-control
```

## Prerequisites

| Tool | Minimum version | Install example |
| - | - | - |
| `kubectl` | 1.24+ | `brew install kubectl` |
| `helm` | 3.x | `brew install helm` |
| `curl` | any current version | Usually preinstalled |

You must run the installer against the Kubernetes cluster where LangSmith is installed or will be installed. Confirm the active context before continuing:

```bash
kubectl config current-context
```

The installer identity needs permission to create the Mission Control namespace resources and cluster-scoped RBAC:

```bash
kubectl auth can-i create clusterrole
kubectl auth can-i create clusterrolebinding
kubectl auth can-i create serviceaccount -n langsmith
kubectl auth can-i create deployment -n langsmith
kubectl auth can-i create secret -n langsmith
```

All five commands should return `yes`. See [Permissions reference](#permissions-reference) for the runtime permissions granted to Mission Control.

## Quick install

Run these three commands:

```bash
curl -fsSLO https://raw.githubusercontent.com/langchain-ai/helm/main/charts/mission-control/install-script.sh && chmod +x install-script.sh
curl -fsSL https://raw.githubusercontent.com/langchain-ai/helm/main/charts/mission-control/values.yaml -o values.yaml
./install-script.sh all -f values.yaml
```

The `all` step:

* Checks required tools and RBAC.
* Creates the `langsmith` namespace.
* Prompts for a Mission Control username and password.
* Stores those credentials in the `mission-control-auth` Kubernetes Secret.
* Writes `values.yaml` if one does not already exist.
* Installs from the public Helm chart repository if you are not running from a local chart checkout.
* Installs Mission Control with Helm.

The RBAC check runs:

```bash
kubectl auth can-i create clusterrole
kubectl auth can-i create clusterrolebinding
kubectl auth can-i create serviceaccount -n langsmith
kubectl auth can-i create deployment -n langsmith
kubectl auth can-i create secret -n langsmith
```

If your organization intentionally blocks `kubectl auth can-i` but Helm installs are approved through another control path, run:

```bash
./install-script.sh all -f values.yaml --skip-rbac-check
```

### Access the UI

After the install finishes, start a local port-forward:

```bash
./install-script.sh forward
```

Open [http://localhost:3000](http://localhost:3000/) and log in with the username and password you entered.

### Review the script first

The quick install path downloads the script before running it, so you can review `install-script.sh` locally before the third command.

### Edit values before install

The quick install path also downloads `values.yaml` before running the installer. Review or edit that file before the third command if you need to change namespace, resources, ingress, feature flags, or diagnostic persistence.

Common edits:

| Setting | When to change it |
| - | - |
| `namespace` | Install Mission Control somewhere other than `langsmith`. Also pass `-n <namespace>` to the script. |
| `resources` | Your namespace has a `ResourceQuota` or your platform requires specific requests/limits. |
| `ingress.enabled` and `ingress.host` | You want to expose Mission Control through your ingress controller instead of port-forwarding. |
| `config.features.*` | You need to remove specific write permissions or external egress features. |
| `diagnostics.persistence.enabled` | You want diagnostic bundles to survive pod restarts and Helm upgrades. |
| `backend.podSecurityContext` and `frontend.podSecurityContext` | Your platform requires containers to run as a specific non-root UID, such as `1001`. |

Example with a custom namespace:

```bash
curl -fsSLO https://raw.githubusercontent.com/langchain-ai/helm/main/charts/mission-control/install-script.sh && chmod +x install-script.sh
curl -fsSL https://raw.githubusercontent.com/langchain-ai/helm/main/charts/mission-control/values.yaml -o values.yaml
./install-script.sh all -n mission-control -f values.yaml
```

### Script command reference

```bash
./install-script.sh prereqs
./install-script.sh namespace
./install-script.sh secret
./install-script.sh values
./install-script.sh install
./install-script.sh forward
./install-script.sh all
```

Useful flags:

```bash
./install-script.sh all -n langsmith -f values.yaml
./install-script.sh all -u admin
printf '%s\n' 'your-password' | ./install-script.sh secret -u admin --password-stdin
./install-script.sh all -f values.yaml --skip-rbac-check
./install-script.sh install --chart-ref langchain/mission-control
./install-script.sh install --chart-path /path/to/mission-control
./install-script.sh forward --port 3001:3000
```

## Manual install

Use this path when installer scripts are not allowed. These steps use normal `kubectl`, `helm`, and `curl` commands only.

**1. Add the Helm repo and get the values file**

Add the LangChain Helm repo:

```bash
helm repo add langchain https://langchain-ai.github.io/helm
helm repo update langchain
```

Download the customer values file:

```bash
curl -fsSL https://raw.githubusercontent.com/langchain-ai/helm/main/charts/mission-control/values.yaml -o values.yaml
```

Review `values.yaml` before installing. Keep `config.auth.enabled: true` for production.

If your platform requires non-root containers, Mission Control can run as UID `1001`. Add this to `values.yaml` before installing:

```yaml
backend:
  podSecurityContext:
    runAsNonRoot: true
    runAsUser: 1001
    runAsGroup: 1001
    fsGroup: 1001
  securityContext:
    allowPrivilegeEscalation: false
    capabilities:
      drop:
        - ALL
  extraEnv:
    - name: HOME
      value: /tmp
    - name: HELM_CACHE_HOME
      value: /tmp/.cache/helm
    - name: HELM_CONFIG_HOME
      value: /tmp/.config/helm
    - name: HELM_DATA_HOME
      value: /tmp/.local/share/helm

frontend:
  podSecurityContext:
    runAsNonRoot: true
    runAsUser: 1001
    runAsGroup: 1001
  securityContext:
    allowPrivilegeEscalation: false
    capabilities:
      drop:
        - ALL
```

**2. Create the namespace**

```bash
kubectl create namespace langsmith --dry-run=client -o yaml | kubectl apply -f -
```

**3. Create the auth credentials Secret**

Credentials are stored in a Kubernetes Secret. They are not written to `values.yaml`.

```bash
read -r -p "Username: " MC_USER
read -r -s -p "Password: " MC_PASS; echo

kubectl create secret generic mission-control-auth \
  --namespace=langsmith \
  --from-literal=username="$MC_USER" \
  --from-literal=password="$MC_PASS" \
  --dry-run=client -o yaml | kubectl apply -f -
```

For multi-replica backend deployments, include a shared JWT signing key in the same Secret and set `config.auth.jwtSecretKey: jwtSecret` in `values.yaml`:

```bash
JWT_SECRET="<SECRET>"

kubectl create secret generic mission-control-auth \
  --namespace=langsmith \
  --from-literal=username="$MC_USER" \
  --from-literal=password="$MC_PASS" \
  --from-literal=jwtSecret="$JWT_SECRET" \
  --dry-run=client -o yaml | kubectl apply -f -
```

**4. Install with Helm**

```bash
helm upgrade --install mission-control langchain/mission-control \
  --namespace langsmith \
  --create-namespace \
  --values values.yaml \
  --rollback-on-failure
```

Wait for both workloads to become ready (the backend runs as a StatefulSet, the frontend as a Deployment):

```bash
kubectl rollout status statefulset/mission-control-backend -n langsmith
kubectl rollout status deployment/mission-control-frontend -n langsmith
```

You can also inspect the pods directly:

```bash
kubectl get pods -n langsmith
```

**5. Access the UI**

```bash
kubectl port-forward svc/mission-control-frontend 3000:3000 -n langsmith
```

Open [http://localhost:3000](http://localhost:3000/) and log in with the credentials from step 3.

## Upgrade

Download the latest public values file, merge in any local changes you need, then run:

```bash
helm repo update langchain

helm upgrade --install mission-control langchain/mission-control \
  --namespace langsmith \
  --values values.yaml \
  --rollback-on-failure
```

If you are working from a local chart checkout instead:

```bash
helm upgrade --install mission-control . \
  --namespace langsmith \
  --values values.yaml \
  --rollback-on-failure
```

If you installed with the quick script and kept it locally:

```bash
./install-script.sh install -f values.yaml
```

## Uninstall

```bash
helm uninstall mission-control -n langsmith
```

This removes the Mission Control release. It does not delete your namespace or unrelated LangSmith resources.

Optional cleanup of Mission Control-owned Secrets:

```bash
kubectl delete secret -n langsmith \
  mission-control-auth \
  mission-control-draft \
  mission-control-deployed \
  mission-control-backup \
  mission-control-history \
  mission-control-alerts-config \
  mission-control-alerts-log \
  mission-control-alerts-key \
  mission-control-setup-token \
  --ignore-not-found
```

## Additional resources

### Troubleshooting

| Symptom | What to check |
| - | - |
| `kubectl auth can-i ...` returns `no` | Ask a cluster admin to grant install-time RBAC or run the install for you. |
| Pods stay `Pending` | Check namespace `ResourceQuota`, node capacity, and PVC/storage class events with `kubectl describe pod -n langsmith <pod>`. |
| Image pull errors | Confirm the cluster can pull `langchain/mission-control-backend:latest` and `langchain/mission-control-frontend:latest`. |
| Login fails | Confirm `mission-control-auth` exists in the same namespace and has `username` and `password` keys. |
| Browser cannot connect | Confirm the port-forward command is still running and no other local process is using port `3000`. |

### Permissions reference

The Helm chart creates a `ServiceAccount`, `ClusterRole`, and `ClusterRoleBinding` named `mission-control`. Most permissions are read-only. Write verbs are narrow and controlled by feature flags.

Install or upgrade requires the ability to create cluster-scoped RBAC (`ClusterRole` and `ClusterRoleBinding`), usually `cluster-admin` or a custom equivalent. The broadest runtime permission set is only used when `config.features.deploy: true`; that flag is enabled by default, set it to `false` for read-only installs.

#### Always-present read-only permissions

| Resource group | Resources | Verbs |
| - | - | - |
| Workloads | pods, pods/log, deployments, statefulsets, replicasets, daemonsets, jobs, cronjobs | get, list, watch |
| Networking | services, endpoints, ingresses, ingressclasses | get, list, watch |
| Storage | persistentvolumeclaims, storageclasses | get, list, watch |
| Cluster | nodes, namespaces, events, serviceaccounts, resourcequotas | get, list, watch |
| Config | configmaps, secrets | get, list |
| Metrics | metrics.k8s.io pods/nodes | get, list, watch |
| RBAC | roles, rolebindings, clusterroles, clusterrolebindings | get, list, watch |
| CRDs and extensions | customresourcedefinitions, leases, scaledobjects, httproutes, virtualservices, lgps | get, list, watch |

#### Feature-gated permissions

| Feature flag | Resources | Extra verbs |
| - | - | - |
| `config.features.configSave` | secrets (`mission-control-draft`) | create, update, delete |
| `config.features.alerts` | secrets (`mission-control-alerts-*`) | create, update, delete |
| `config.features.fixIssue` | pods | delete |
| `config.features.adopt` | secrets, configmaps, serviceaccounts, deployments, statefulsets | patch |
| `config.auth.enabled` | secrets (`mission-control-auth`, setup-token), backend statefulset | create, update, delete, patch |
| `config.features.valuesOverride` | secrets (`mission-control-values-overrides`) | create, update, delete |
| `config.features.deploy` | workloads, networking, RBAC, CRDs, Helm release secrets | create, update, patch, delete |

Set feature flags to `false` in `values.yaml` to remove the corresponding write verbs. With all feature flags disabled, Mission Control is effectively read-only except for authentication setup permissions when `config.auth.enabled: true`.

# Enable Agent Server hosting

> Add a control plane and data plane to deploy and manage agents on self-hosted LangSmith.

[LangSmith Agent Server](../../../../Deploy/Get%20started/LangSmith%20Agent%20Server.md) hosting adds a [control plane](../../../../Deploy/Get%20started/Deployment%20components/LangSmith%20control%20plane.md) and [data plane](../../../../Deploy/Get%20started/Deployment%20components/LangSmith%20data%20plane.md) to your self-hosted LangSmith installation. It lets you deploy and manage Agent Servers through the LangSmith UI.

> [!NOTE]
>
> LangSmith Deployment is now **LangSmith Agent Server**.

Agent Server hosting is optional for observability and evaluation. Complete the [Kubernetes installation](../Self-host%20LangSmith%20on%20Kubernetes.md) first. For other optional features, see [Configure additional features](Configure%20additional%20self-hosted%20features.md). For Agent Servers without a control plane, see [Standalone servers](../../../../Deploy/Deploy%20to%20Self-hosted/Self-host%20standalone%20servers.md).

> [!NOTE]
>
> Agent Server hosting requires an [Enterprise](https://langchain.com/pricing) plan.

## Prerequisites

**1. Install the base LangSmith platform**

Follow the [Kubernetes installation guide](../Self-host%20LangSmith%20on%20Kubernetes.md) to install the base LangSmith platform before continuing.

**2. Install KEDA**

Run the following commands to install `KEDA` on your cluster:

```bash
helm repo add kedacore https://kedacore.github.io/charts
helm upgrade --install keda kedacore/keda --namespace keda --create-namespace
```

> [!NOTE]
>
> KEDA automatically scales the deployment system based on queue size.

**3. Configure an ingress**

Configure an ingress, gateway, or Istio for your LangSmith instance. All agents will be deployed as Kubernetes services behind this ingress. See [Set up an ingress](../../Configure%20an%20instance/Create%20an%20Ingress%20for%20installations%20%28Kubernetes%29.md). You must provide a `hostname` in your [`langsmith_config.yaml`](../Self-host%20LangSmith%20on%20Kubernetes.md#configure-your-helm-charts).

**4. Verify cluster capacity**

Ensure your cluster has available capacity for multiple deployments. A cluster autoscaler is recommended.

**5. Verify storage**

Ensure a valid dynamic PV provisioner or PVs are available on your cluster.

```bash
kubectl get storageclass
```

At least one StorageClass should have a `PROVISIONER` value (not `kubernetes.io/no-provisioner`) and be marked `(default)`, or you must configure one before proceeding.

**6. Verify egress**

Ensure egress to `https://beacon.langchain.com` is available. See the [egress documentation](../../Configure%20an%20instance/Egress%20for%20billing%20and%20operational%20telemetry.md).

## Enable Agent Server hosting

### Components

Enabling Agent Server hosting provisions the following resources in your cluster:

* `listener`: Listens to the [control plane](../../../../Deploy/Get%20started/Deployment%20components/LangSmith%20control%20plane.md) for changes to your deployments and creates or updates downstream CRDs.
* `LangGraphPlatform CRD`: Manages Agent Server deployments.
* `operator`: Handles changes to your LangSmith CRDs.
* `host-backend`: The [control plane](../../../../Deploy/Get%20started/Deployment%20components/LangSmith%20control%20plane.md).

### Enable the feature

To enable Agent Server hosting, update your [`langsmith_config.yaml`](../Self-host%20LangSmith%20on%20Kubernetes.md#configure-your-helm-charts):

**1. Enable deployment in your config**

In your `langsmith_config.yaml`, enable the `deployment` option. You must also have a valid ingress configured.

```yaml
config:
  deployment:
    enabled: true
```

> [!NOTE]
>
> As of v0.12.0, the `langgraphPlatform` option is deprecated. Use `config.deployment` for any version after v0.12.0.

**2. (Optional) Configure image mirroring**

If you need to mirror images to a private registry, configure the `hostBackendImage` and `operatorImage` options in your [`langsmith_config.yaml`](../Self-host%20LangSmith%20on%20Kubernetes.md#configure-your-helm-charts). Use the image tags specified in the [latest LangSmith Helm chart release](https://github.com/langchain-ai/helm/releases).

```yaml
hostBackendImage:
  repository: "docker.io/langchain/hosted-langserve-backend"
  pullPolicy: IfNotPresent
operatorImage:
  repository: "docker.io/langchain/langgraph-operator"
  pullPolicy: IfNotPresent
```

**3. (Optional) Configure base agent templates**

Override the [base agent templates in `values.yaml`](https://github.com/langchain-ai/helm/blob/main/charts/langsmith/values.yaml#L1428) if you need to customize how the operator creates agent Kubernetes resources. The most common use case is adding `imagePullSecrets` to authenticate with a private container registry. See [Configure authentication for private registries](#configure-authentication-for-private-registries) for details. To mount volumes, such as Amazon EFS, into agent pods, see [Volumes](../../../../Deploy/Deploy%20to%20Self-hosted/Configure/Self-hosted%20platform%20features.md#volumes).

**4. Apply the changes**

Run the following command to apply the changes. This command is used throughout this guide whenever you are asked to apply changes. Replace `<version>` and `<namespace>` with your values:

```bash
helm upgrade -i langsmith langchain/langsmith --values langsmith_config.yaml --version <version> -n <namespace> --wait --debug
```

Verify that the new pods are running before continuing:

```bash
kubectl get pods -n <namespace>
```

Your instance is now ready to create deployments.

## Optional configuration

### Configure additional data planes

> [!WARNING]
>
> **Not recommended; deprecation planned.** Configuring additional data planes through the control plane is not a recommended approach and will be deprecated in a future release. Instead, deploy [standalone Agent Servers](../../../../Deploy/Deploy%20to%20Self-hosted/Self-host%20standalone%20servers.md) and configure them to trace to your self-hosted LangSmith instance.

In addition to the data plane created above, you can create more data planes in different Kubernetes clusters or in the same cluster under a different namespace. There are different ways to achieve this, so implement the solution that works best for your use case.

#### Prerequisites

**1. Review cluster organization**

Read through the cluster organization guide in the [hybrid (legacy) documentation](../../Hybrid/Setup%20guide%20%28legacy%29.md#listeners) to understand how to organize this for your use case.

**2. Verify hybrid prerequisites**

Verify the prerequisites in the [hybrid section](../../Hybrid/Setup%20guide%20%28legacy%29.md#prerequisites) for the new cluster. In step 5 of the [prerequisites](../../Hybrid/Setup%20guide%20%28legacy%29.md#prerequisites), configure egress to your [self-hosted LangSmith instance](../Interact%20with%20your%20self-hosted%20instance%20of%20LangSmith.md#configuring-the-application-you-want-to-use-with-langsmith) instead of `https://api.host.langchain.com` and `https://api.smith.langchain.com`.

**3. Enable the feature in Postgres**

Run the following against your LangSmith Postgres instance to enable this feature. Note the workspace ID for later steps.

```sql
update organizations set config = config || '{"enable_lgp_listeners_page": true}' where id = '<org id here>';
update tenants set config = config || '{"langgraph_remote_reconciler_enabled": true}' where id = '<workspace id here>';
```

#### Deploy to a different cluster

**1. Follow the hybrid setup guide**

Follow steps 2 to 6 in the [hybrid setup guide](../../Hybrid/Setup%20guide%20%28legacy%29.md#setup). Set `config.langsmithWorkspaceId` to the workspace ID from the previous step.

**2. (Optional) Add more data planes to the same cluster**

To add more than one data plane to the same cluster, follow the instructions for [configuring additional data planes in the same cluster](../../Hybrid/Setup%20guide%20%28legacy%29.md#configuring-additional-data-planes-in-the-same-cluster).

#### Deploy to a different namespace in the same cluster

**1. Update your config**

In your [`langsmith_config.yaml`](../Self-host%20LangSmith%20on%20Kubernetes.md#configure-your-helm-charts), make the following modifications:

* Set `operator.watchNamespaces` to the current namespace your self-hosted LangSmith instance is running in. This prevents conflicts with the operator added by the new data plane.
* Use the [Gateway API](../../Configure%20an%20instance/Create%20an%20Ingress%20for%20installations%20%28Kubernetes%29.md#option-2%3A-gateway-api) or an [Istio Gateway](../../Configure%20an%20instance/Create%20an%20Ingress%20for%20installations%20%28Kubernetes%29.md#option-3%3A-istio-gateway). Adjust your `langsmith_config.yaml` accordingly.

**2. Apply the changes**

```bash
helm upgrade -i langsmith langchain/langsmith --values langsmith_config.yaml --version <version> -n <namespace> --wait --debug
```

**3. Follow the hybrid setup guide**

Follow steps 2 to 6 in the [hybrid setup guide](../../Hybrid/Setup%20guide%20%28legacy%29.md#setup). Set `config.langsmithWorkspaceId` to the workspace ID from the previous step. Set `config.watchNamespaces` to a different namespace than the one used by the existing data plane.

**4. (Optional) Configure log access**

Configure access for the control plane to read Agent Server deployment logs from the new namespace. See [Read Agent Server logs from other namespaces](#read-agent-server-logs-from-other-namespaces).

### Configure authentication for private registries

If your [Agent Server deployments](../../../../Deploy/Agent%20Server/Capabilities/Agent%20Server.md) will use images from private container registries (for example, AWS ECR, Azure ACR, or GCP Artifact Registry), configure image pull secrets. This configuration applies to all deployments automatically, allowing them to authenticate with your private registry.

**1. Create a Kubernetes image pull secret**

```bash
kubectl create secret docker-registry langsmith-registry-secret \
    --docker-server=myregistry.com \
    --docker-username=your-username \
    --docker-password=your-password \
    --docker-email=your-email@example.com \
    -n langsmith
```

Replace the values with your registry credentials:

* `myregistry.com`: Your registry URL
* `your-username`: Your registry username
* `your-password`: Your registry password or access token
* `langsmith`: The Kubernetes namespace where LangSmith is installed

**2. Configure the deployment template in your langsmith\_config.yaml**

To enable agent server deployments to use the private registry secret, add `imagePullSecrets` to the operator's deployment template:

```yaml {21-22}
operator:
  templates:
    deployment: |
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: ${name}
        namespace: ${namespace}
      spec:
        replicas: ${replicas}
        revisionHistoryLimit: 10
        selector:
          matchLabels:
            app: ${name}
        template:
          metadata:
            labels:
              app: ${name}
          spec:
            enableServiceLinks: false
            imagePullSecrets:
            - name: langsmith-registry-secret
            containers:
            - name: api-server
              image: ${image}
              ports:
              - name: api-server
                containerPort: 8000
                protocol: TCP
              livenessProbe:
                httpGet:
                  path: /ok
                  port: 8000
                periodSeconds: 15
                timeoutSeconds: 5
                failureThreshold: 6
              readinessProbe:
                httpGet:
                  path: /ok
                  port: 8000
                periodSeconds: 15
                timeoutSeconds: 5
                failureThreshold: 6
```

**3. Apply the changes**

```bash
helm upgrade -i langsmith langchain/langsmith --values langsmith_config.yaml --version <version> -n <namespace> --wait --debug
```

All user deployments created through the LangSmith UI will inherit these registry credentials.

For registry-specific authentication methods, refer to the [Kubernetes documentation on pulling images from private registries](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/).

### Read Agent Server logs from other namespaces

> [!WARNING]
>
> Retrieving server logs is not supported for self-hosted deployments where the control plane (`host-backend`) and data plane (`listener`) are deployed in different Kubernetes clusters.

For deployments where the control plane and data plane are in the same cluster, ensure the control plane Kubernetes deployment (`host-backend`) has permission to `get`, `list`, and `watch` Kubernetes `deployments`, `pods`, `replicasets`, and `logs` from the namespace where the Agent Server deployment exists. There are different ways to achieve this. The following example uses Kubernetes RBAC, but use the approach that best fits your use case:

**1. Create a Role with the required permissions**

Create a `Role` in the Agent Server namespace. Replace `<data_plane_namespace>`:

```bash
kubectl apply -n <data_plane_namespace> -f - <<EOF
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: read-agent-server-logs-role
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get","list","watch"]
- apiGroups: [""]
  resources: ["pods/log"]
  verbs: ["get","watch"]
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get","list","watch"]
- apiGroups: ["apps"]
  resources: ["replicasets"]
  verbs: ["get","list","watch"]
EOF
```

**2. Get the control plane ServiceAccount**

Replace `<control_plane_namespace>`:

```bash
kubectl get serviceaccounts -n <control_plane_namespace> | grep host-backend
```

**3. Bind the Role to the control plane ServiceAccount**

Replace `<data_plane_namespace>`, `<control_plane_namespace>`, and `<control_plane_service_account>`:

```bash
kubectl apply -n <data_plane_namespace> -f - <<EOF
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-agent-server-logs-role-binding
subjects:
- kind: ServiceAccount
  name: <control_plane_service_account>
  namespace: <control_plane_namespace>
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: read-agent-server-logs-role
EOF
```

> [!NOTE]
>
> In this example, the Role and RoleBinding are defined in the same Kubernetes namespace as the Agent Server deployment. You can assign any name to the Role and RoleBinding and customize them as needed.

## Next steps

Once Agent Server hosting is enabled, see [Deploy with control plane](../../../../Deploy/Deploy%20to%20Self-hosted/Deploy%20with%20control%20plane.md) to build and deploy your applications via the LangSmith UI.

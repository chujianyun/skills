# Enable Sandboxes on self-hosted LangSmith

> Configure Kubernetes nodes, storage, and Helm values for self-hosted LangSmith Sandboxes.

[Sandboxes](../../../../../Deploy/Sandboxes/LangSmith%20Sandboxes.md) provide isolated environments for running code and exposing services. Install them when you need sandbox workloads or a feature that requires them, such as [Engine](../../../../../Engine/Self-hosted%20and%20BYOC/LangSmith%20Engine%20on%20Self-hosted%20and%20BYOC.md).

> [!NOTE]
>
> Sandboxes require an [Enterprise](https://langchain.com/pricing) plan.

Sandboxes are disabled by default. After installation, see [LangSmith Sandboxes](../../../../../Deploy/Sandboxes/LangSmith%20Sandboxes.md) for user workflows in the LangSmith UI and APIs.

For the infrastructure model and production planning, see [Sandbox architecture](Self-hosted%20Sandbox%20architecture.md), [scaling and capacity](Scale%20self-hosted%20Sandboxes.md), and [upgrades and operations](Operate%20self-hosted%20Sandboxes.md).

This page installs the sandbox runtime in the same cluster as LangSmith. To run it in a dedicated Kubernetes cluster instead, see [Run Sandboxes in a separate cluster](Run%20self-hosted%20Sandboxes%20in%20a%20separate%20cluster.md).

## Supported platforms

Self-hosted Sandboxes are supported on:

* Amazon Elastic Kubernetes Service (EKS)
* Google Kubernetes Engine (GKE)
* Azure Kubernetes Service (AKS)
* Red Hat OpenShift, with the additional steps in [Configure OpenShift](#configure-openshift)
* Bare-metal and on-premises Kubernetes clusters that meet the [node requirements for bare-metal and on-premises clusters](#node-requirements-for-bare-metal-and-on-premises-clusters)

> [!NOTE]
>
> Self-hosted Sandboxes on Azure require LangSmith Helm chart v17 (`0.17.x`).

## Components

Enabling Sandboxes provisions the following resources:

* Sandbox runtime pods that run sandbox workloads on KVM-capable nodes.
* A JuiceFS metadata store backed by Redis and object storage backed by S3, GCS, or Azure Blob Storage.
* Optional wildcard ingress for services exposed from inside Sandboxes.

By default, the `langsmith` release deploys the sandbox runtime alongside LangSmith. With `sandboxes.external.enabled: true`, the runtime is external: a second Helm release, `langsmith-sandbox`, deploys it, usually in a dedicated cluster, and the wildcard ingress stays in the LangSmith cluster.

## Prerequisites

**1. Install the base LangSmith platform**

Install LangSmith on Kubernetes before enabling Sandboxes. See [Self-host LangSmith on Kubernetes](../../Self-host%20LangSmith%20on%20Kubernetes.md).

With the default embedded runtime, Sandboxes run in the same Kubernetes cluster and namespace as the LangSmith release.

If your cluster cannot pull from public registries, also mirror the sandbox runtime image. See [Additional images for Sandboxes](../../../Configure%20an%20instance/Mirror%20images%20for%20your%20LangSmith%20installation.md#additional-images-for-sandboxes).

**2. Add KVM-capable nodes**

Your cluster must include dedicated nodes that can run nested workloads with Linux KVM available at `/dev/kvm`.

These can be bare-metal machines or supported cloud instances with nested virtualization enabled. On AWS and GCP, use x86\_64 Linux instances that expose `/dev/kvm` to the sandbox runtime.

> [!WARNING]
>
> On EKS, the VPC CNI addon must be **v1.21 or later**. `v1.20.0` crashes on 8th-generation
> Intel instances (for example `m8i`): `aws-node` enters `CrashLoopBackOff`, the node reports
> `cni plugin not initialized`, and the managed node group eventually fails with
> `NodeCreationFailure: Unhealthy nodes in the kubernetes cluster`.

The default Helm scheduling values expect these nodes to have the following label and taint:

```yaml
label:
  sandbox.langsmith.com/host: "true"
taint:
  key: sandbox.langsmith.com/host
  value: "true"
  effect: NoSchedule
```

If your nodes use different labels or taints, override `sandboxes.sandboxHost.deployment.nodeSelector` and `sandboxes.sandboxHost.deployment.tolerations`.

**3. Configure JuiceFS storage**

Sandboxes require JuiceFS-backed shared storage. You must provide:

* A Redis-compatible metadata store.
* An object storage bucket or bucket root.
* A JuiceFS configuration Secret, or enough Helm values for the chart to create one.

Use these object storage backends for `sandboxes.juicefs.storage` and `sandboxes.juicefs.bucket`:

| **Platform** | **Storage value** | **Bucket format** |
| - | - | - |
| AWS | `s3` | Region-explicit HTTPS S3 endpoint, such as `https://bucket-name.s3.us-west-2.amazonaws.com` |
| GCP | `gs` | GCS URL, such as `gs://bucket-name` |
| Azure | `wasb` | Azure Blob Storage URL, such as `https://container-name.core.windows.net` |
| S3-compatible, such as MinIO | `s3` | Endpoint URL with the bucket as the path, such as `http://minio.example.com:9000/bucket-name`. Requires static keys; see [Use S3-compatible object storage](#use-s3-compatible-object-storage). |

Do not use object-store subpaths in `sandboxes.juicefs.name`. Use a flat name, such as `sandbox-juicefs`. JuiceFS stores objects under that name inside the configured bucket.

> [!TIP]
>
> For the Redis metadata store, we recommend setting `maxmemory-policy` to `noeviction`. This avoids evicting JuiceFS metadata under memory pressure. Monitor Redis capacity and scale it before it reaches memory limits.
>
> With `noeviction`, Redis writes can fail when the instance reaches max memory, so keep enough memory headroom for sandbox metadata growth.

**4. Configure sandbox secrets**

Sandboxes need additional secret material for service-to-service authentication and callback signing.

> [tab] Using Kubernetes secrets (recommended)
>
> If you use `config.existingSecretName`, add the sandbox keys to the same LangSmith app Secret. Do not set the secret values directly in Helm.
>
> ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> stringData:
>   sandbox_callback_signing_jwk: '<ed25519-private-jwk>'
> ```

> [tab] Using inline values
>
> If the Helm chart manages your LangSmith app Secret, set the sandbox secret values directly in your config file. Avoid committing this file to version control.
>
> ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> sandboxes:
>   callbackSigningJwk: '<ed25519-private-jwk>'
> ```

The callback signing value must be an Ed25519 private JWK. Keep it stable across upgrades.

To generate an Ed25519 private JWK with OpenSSL 1.1.1 or later, run:

```bash
openssl genpkey -algorithm ED25519 -out callback-signing.pem
d=$(openssl pkey -in callback-signing.pem -outform DER | tail -c 32 | base64 | tr '+/' '-_' | tr -d '=\n')
x=$(openssl pkey -in callback-signing.pem -pubout -outform DER | tail -c 32 | base64 | tr '+/' '-_' | tr -d '=\n')
printf '{"kty":"OKP","crv":"Ed25519","alg":"EdDSA","use":"sig","kid":"sandbox-callback-%s","x":"%s","d":"%s"}\n' "$(openssl rand -hex 8)" "$x" "$d"
rm callback-signing.pem
```

The command prints the JWK as one line of JSON. If `openssl genpkey` reports `Algorithm ED25519 not found`, your `openssl` is an older LibreSSL build. Install OpenSSL and run the command with it.

**5. Choose a proxy CA mode**

The sandbox egress authentication proxy uses this CA for TLS interception and credential injection.

The chart supports two proxy CA modes:

| Mode | Use when |
| - | - |
| `generatedSecret` | You want Helm to create a self-signed CA Secret. This is the default. |
| `existingSecret` | You manage the CA Secret outside the LangSmith chart. The Secret can be created manually, by cert-manager, or by another external process. |

In GitOps workflows that render manifests without live cluster access, prefer `existingSecret`. The `generatedSecret` mode uses Helm's live `lookup` behavior to reuse the generated Secret on upgrades; pure render workflows cannot read the live Secret and may produce new cert material on each render.

## Configure OpenShift

On Red Hat OpenShift, the sandbox runtime needs a security context constraint (SCC) that allows privileged containers. The sandbox runtime pods run privileged with host networking because they manage microVMs, network namespaces, and mounts on their node. Other LangSmith components, including the bundled PostgreSQL, Redis, and ClickHouse, run under the default `restricted-v2` SCC.

To prepare an OpenShift cluster, complete these steps before you [enable Sandboxes with Helm](#enable-with-helm):

**1. Add KVM-capable worker nodes**

Use bare-metal worker nodes, or virtual machine worker nodes with nested virtualization enabled. To confirm that a node exposes KVM, run:

```bash
oc debug node/<node-name> -- chroot /host ls -l /dev/kvm
```

Apply the label and taint that the chart expects:

```bash
oc label node <node-name> sandbox.langsmith.com/host=true
oc adm taint node <node-name> sandbox.langsmith.com/host=true:NoSchedule
```

Labels and taints applied to a node do not carry over to a replacement machine. To keep them, set them in the MachineSet that creates your sandbox nodes, under `spec.template.spec.metadata.labels` and `spec.template.spec.taints`.

**2. Grant the privileged SCC to the sandbox runtime**

Grant the built-in `privileged` SCC to the sandbox runtime service account only. The chart names this service account `<release-fullname>-sandbox-host`, which is `langsmith-sandbox-host` for a release named `langsmith`:

```bash
oc adm policy add-scc-to-user privileged -z langsmith-sandbox-host -n <namespace>
```

The JuiceFS formatter Job runs as the same service account, so it needs no separate grant. If you set `sandboxes.sandboxHost.serviceAccount.name`, grant the SCC to that name instead.

## Node requirements for bare-metal and on-premises clusters

On a managed cloud cluster, the KVM-capable node pool covers these requirements. On bare-metal and on-premises Kubernetes clusters, confirm that each sandbox node and the cluster meet them before you [enable Sandboxes with Helm](#enable-with-helm).

Each sandbox node needs:

* **CPU architecture**: x86-64 (`amd64`). The sandbox runtime does not run on Arm nodes.
* **Hardware virtualization**: Virtualization extensions enabled in the firmware, the KVM kernel module loaded, and `/dev/kvm` present.
* **cgroup v2**: The unified cgroup hierarchy with the `cpu` controller available. The sandbox runtime uses it to enforce per-sandbox CPU limits.
* **TUN/TAP and FUSE**: `/dev/net/tun` for sandbox network interfaces and `/dev/fuse` for the JuiceFS mount.
* **nftables**: Kernel support for `iptables` with the nftables backend. The sandbox runtime applies its egress rules inside a network namespace for each sandbox.
* **Local disk for the JuiceFS cache**: A node-local path for `sandboxes.juicefs.hostMount.cacheDirs`, which defaults to `/var/cache/juicefs` with a 50 GiB cache size.

The cluster needs:

* **Privileged pods**: The sandbox runtime pods run privileged, with host networking and `hostPath` volumes. If your cluster enforces Pod Security Admission, label the LangSmith namespace to allow privileged pods, for example `pod-security.kubernetes.io/enforce=privileged`.
* **Node port reachability**: The LangSmith platform backend connects to each sandbox node on TCP port `19190`. Allow this traffic from the LangSmith pods to the sandbox nodes, and keep the port on private networks.
* **Outbound access**: Sandbox nodes need network access to the JuiceFS Redis metadata store, the object storage backend, and the destinations that sandboxes call. To send sandbox egress through a corporate HTTP proxy, set `sandboxes.authProxy.httpProxy`.

If your cluster cannot pull from public registries, mirror the sandbox runtime image. For more information, see [Additional images for Sandboxes](../../../Configure%20an%20instance/Mirror%20images%20for%20your%20LangSmith%20installation.md#additional-images-for-sandboxes).

### Use S3-compatible object storage

On clusters without cloud workload identity, JuiceFS can store sandbox data in an S3-compatible object store, such as MinIO, using static access keys.

> [!NOTE]
>
> S3-compatible object storage with static keys requires LangSmith application version 0.17.35 or later.

Create a JuiceFS configuration Secret that includes the access keys, and set `sandboxes.juicefs.existingSecretName` to its name:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: langsmith-sandbox-juicefs
  namespace: <namespace>
type: Opaque
stringData:
  name: sandbox-juicefs
  metaurl: redis://<redis-host>:6379/1
  storage: s3
  bucket: http://<s3-endpoint>:9000/<bucket-name>
  access-key: <access-key>
  secret-key: <secret-key>
```

The JuiceFS formatter uses the keys only when the Secret contains both `access-key` and `secret-key`. JuiceFS stores the keys in its Redis metadata store, so restrict access to that Redis instance.

The object store must sustain the sandbox runtime's write throughput. When object storage writes stall, the JuiceFS mount health check fails and the sandbox runtime pod restarts, which interrupts the Sandboxes on that node.

## Enable with Helm

Enable Sandboxes by setting Helm values directly, as shown in this section. On AWS and GCP, you can instead [enable Sandboxes with Terraform](#enable-with-terraform), which provisions the infrastructure and generates the Helm values.

Add the following values to your `langsmith_config.yaml`, along with the sandbox secret values described in the [Prerequisites](#prerequisites). Replace placeholders with your deployment-specific values.

> [!NOTE]
>
> These values target chart 0.17. On chart 0.16, sandboxes mount JuiceFS through a bundled JuiceFS CSI driver, so the values differ:
>
> * Set the workload identity annotation on `sandboxes.juicefs.csi.node.serviceAccount.annotations` instead of `sandboxes.sandboxHost.serviceAccount.annotations`.
> * Set an existing config Secret with `sandboxes.juicefs.csi.existingSecretName` instead of `sandboxes.juicefs.existingSecretName`.
> * Omit `juicefsFormatJob`. Chart 0.16 does not support Azure Blob Storage for sandboxes.
>
> When you upgrade from chart 0.16 to 0.17, drain the JuiceFS volumes first, then remove the `sandboxes.juicefs.csi` block from your values. For the steps, see [Upgrade an installation](../../../Manage%20an%20instance/Upgrade%20an%20installation.md).

> [tab] AWS
>
> ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> images:
>   sandboxHostImage:
>     tag: "<same-release-tag-as-your-langsmith-images>"
>
> sandboxes:
>   enabled: true
>   juicefs:
>     name: "sandbox-juicefs"
>     storage: "s3"
>     bucket: "https://bucket-name.s3.us-west-2.amazonaws.com"
>     redis:
>       metaURL: "redis://redis-host:6379/1"
>   sandboxHost:
>     deployment:
>       nodeSelector:
>         kubernetes.io/arch: "amd64"
>         sandbox.langsmith.com/host: "true"
>     serviceAccount:
>       annotations:
>         eks.amazonaws.com/role-arn: "<role_arn>"
> ```

> [tab] GCP
>
> ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> images:
>   sandboxHostImage:
>     tag: "<same-release-tag-as-your-langsmith-images>"
>
> sandboxes:
>   enabled: true
>   juicefs:
>     name: "sandbox-juicefs"
>     storage: "gs"
>     bucket: "gs://bucket-name"
>     redis:
>       metaURL: "redis://redis-host:6379/1"
>   sandboxHost:
>     deployment:
>       nodeSelector:
>         kubernetes.io/arch: "amd64"
>         sandbox.langsmith.com/host: "true"
>     serviceAccount:
>       annotations:
>         iam.gke.io/gcp-service-account: "<gsa_name>@<project_id>.iam.gserviceaccount.com"
> ```
>
> On GKE, `sandbox-host` runs on the host network, and GKE does not give Workload Identity to host-network pods, so the annotation serves only the `juicefs-format` Job. Also grant the sandbox node pool's service account `roles/storage.objectAdmin` on the bucket, with an IAM condition limited to the JuiceFS prefix: objects under `sandbox-juicefs/` and list calls with that prefix. Without that grant, the JuiceFS mount gets 403 from Cloud Storage.

> [tab] Azure
>
> ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> images:
>   sandboxHostImage:
>     tag: "<same-release-tag-as-your-langsmith-images>"
>
> sandboxes:
>   enabled: true
>   juicefs:
>     name: "sandbox-juicefs"
>     storage: "wasb"
>     bucket: "https://container-name.core.windows.net"
>     storageAccountName: "<storage-account-name>"
>     redis:
>       metaURL: "redis://redis-host:6379/1"
>   juicefsFormatJob:
>     labels:
>       azure.workload.identity/use: "true"
>   sandboxHost:
>     deployment:
>       labels:
>         azure.workload.identity/use: "true"
>       nodeSelector:
>         kubernetes.io/arch: "amd64"
>         sandbox.langsmith.com/host: "true"
>     serviceAccount:
>       annotations:
>         azure.workload.identity/client-id: "<client_id>"
> ```

Apply the updated chart:

```bash
helm upgrade -i langsmith langchain/langsmith \
  --values langsmith_config.yaml \
  --version <version> \
  --namespace <namespace> \
  --wait
```

## Enable with Terraform

The LangSmith Terraform modules can provision the required AWS and GCP infrastructure and generate the corresponding Helm values.

> [tab] AWS
>
> In `modules/aws/infra/terraform.tfvars`, enable Sandboxes and configure the sandbox node capacity:
>
> ```hcl theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> enable_sandboxes = true
> redis_source     = "external"
>
> sandbox_juicefs_redis_instance_type             = "cache.m6g.large"
> sandbox_juicefs_redis_snapshot_retention_limit  = 7
>
> sandbox_host_node_count               = 1
> sandbox_host_instance_types           = ["m5d.metal"]
> sandbox_host_configure_instance_store = true
>
> sandbox_host_image_tag = "<same-release-tag-as-your-langsmith-images>"
> ```
>
> AWS Sandboxes require `redis_source = "external"`. The Terraform module:
>
> * Creates a dedicated ElastiCache Redis instance for JuiceFS sandbox metadata.
> * Configures that dedicated instance with the recommended `noeviction` policy.
> * Reuses the LangSmith S3 bucket for sandbox object storage.
> * Creates the JuiceFS configuration Secret.
> * Adds the expected node label and taint.
>
> The AWS setup script generates the sandbox service-auth secret, callback signing JWK, and dedicated JuiceFS Redis auth token through the normal SSM-backed setup flow. Run the infra setup script before applying Terraform if those values do not exist yet.
>
> If you deploy the Helm release with the Terraform app module, set the sandbox app values in `modules/aws/app/terraform.tfvars` as well:
>
> ```hcl theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> enable_sandboxes      = true
> chart_version          = "~0.17.0"
> sandbox_host_image_tag = "<same-release-tag-as-your-langsmith-images>"
> ```
>
> When `enable_sandboxes = true`, the Terraform app module requires an explicit LangSmith Helm chart v17 release and a sandbox runtime image tag.
>
> Run the normal AWS flow:
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> make apply
> make init-values
> CHART_VERSION="~0.17.0" make deploy
> ```

> [tab] GCP
>
> In `modules/gcp/infra/terraform.tfvars`, enable Sandboxes and configure a Standard GKE node pool:
>
> ```hcl theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> enable_sandboxes = true
> redis_source     = "external"
>
> gke_use_autopilot     = false
> enable_gcp_iam_module = true
>
> sandbox_juicefs_redis_memory_size       = 5
> sandbox_juicefs_redis_high_availability = true
>
> sandbox_host_node_count     = 1
> sandbox_host_min_node_count = 1
> sandbox_host_max_node_count = 5
> sandbox_host_machine_type   = "n2-standard-8"
>
> sandbox_host_image_tag = "<same-release-tag-as-your-langsmith-images>"
> ```
>
> GCP Sandboxes require `redis_source = "external"`. The Terraform module:
>
> * Creates a dedicated Memorystore Redis instance for JuiceFS sandbox metadata.
> * Configures that dedicated instance with the recommended `noeviction` policy.
> * Reuses the LangSmith GCS bucket for sandbox object storage.
> * Creates the JuiceFS configuration Secret.
> * Adds the expected node label and taint.
>
> The GCP setup script generates the sandbox service-auth secret and callback signing JWK through the normal Secret Manager setup flow. Run the infra setup script before applying Terraform if those values do not exist yet.
>
> If you deploy the Helm release with the Terraform app module, set the sandbox app values in `modules/gcp/app/terraform.tfvars` as well:
>
> ```hcl theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> enable_sandboxes      = true
> chart_version          = "~0.17.0"
> sandbox_host_image_tag = "<same-release-tag-as-your-langsmith-images>"
> ```
>
> When `enable_sandboxes = true`, the Terraform app module requires an explicit LangSmith Helm chart v17 release and a sandbox runtime image tag.
>
> Run the normal GCP flow:
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> make apply
> make init-values
> CHART_VERSION="~0.17.0" make deploy
> ```

## Optional: enable service URLs

Set `sandboxes.serviceUrlBaseUrl` when users need browser or programmatic access to HTTP services running inside Sandboxes.

```yaml
sandboxes:
  serviceUrlBaseUrl: "https://sandbox-services.example.com"
```

This requires wildcard DNS and TLS for `*.sandbox-services.example.com`. When `ingress.enabled` is `true`, the chart also adds a wildcard ingress rule that routes these service URLs to the LangSmith platform backend.

Service URLs also require an Ed25519 private JWKS with a nonempty `kid` on its first key. Set `config.signingJwks`, or add `langsmith_signing_jwks` to your [existing LangSmith app Secret](../../../Platform%20auth%20%26%20access%20control/Use%20an%20existing%20secret%20for%20your%20installation%20%28Kubernetes%29.md). This is separate from `sandboxes.callbackSigningJwk`. For key generation instructions, see [Configure a signing JWKS](../../Self-host%20LangSmith%20on%20Kubernetes.md#configure-a-signing-jwks).

Service URLs are required to [build and edit custom apps with chat](../../../../../Monitor/Observe/Monitoring%20%26%20alerting/Custom%20Apps.md#configure-self-hosted-chat), even though they are optional for other sandbox workflows.

## Optional: route egress through a forward proxy

Set `sandboxes.authProxy.httpProxy` when Sandboxes must reach the internet through a corporate HTTP or HTTPS forward proxy.

```yaml
sandboxes:
  authProxy:
    httpProxy:
      url: http://proxy.corp.internal:3128
```

For requirements, the bypass list, proxy authentication, CA trust for an HTTPS proxy, and security considerations, see [Route Sandbox egress through a forward proxy](Route%20self-hosted%20Sandbox%20egress%20through%20a%20forward%20proxy.md).

## Verify the installation

After the upgrade completes, verify that the sandbox runtime pods and JuiceFS volumes are ready:

```bash
kubectl rollout status deployment/sandbox-host -n <namespace>
kubectl get pods,pvc -n <namespace>
```

Then run a sandbox smoke test:

1. Create a sandbox from a public image, such as a Python image.
2. Start a Python HTTP server inside the sandbox.
3. Snapshot the sandbox with memory enabled.
4. Create a new sandbox from the snapshot.
5. Verify that the HTTP server is still running in the restored sandbox.

## Upgrade notes

Sandbox runtime image changes roll out through the `sandbox-host` Kubernetes Deployment. The chart uses a no-surge rolling update strategy by default, so hosts are replaced one at a time.

During a normal Helm upgrade, a terminating host stops accepting new Sandboxes, attempts to save each running Sandbox's VM memory to JuiceFS, and then stops those VMs before the pod exits. This shutdown is bounded by the `sandbox-host` pod termination grace period, which defaults to 300 seconds. This is not live migration: Sandboxes on that host are interrupted during the restart.

Sandboxes are not proactively restarted. They start again when a user or API action starts the Sandbox, or when a request path wakes it. LangSmith then places the Sandbox on an available host and restores from the saved memory image if the shutdown capture completed. If the memory image is absent or incomplete, the Sandbox starts from the saved root filesystem.

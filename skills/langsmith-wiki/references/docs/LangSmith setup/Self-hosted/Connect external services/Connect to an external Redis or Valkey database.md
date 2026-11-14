# Connect to an external Redis or Valkey database

LangSmith uses Redis to back our queuing/caching operations. By default, LangSmith Self-Hosted will use an internal Redis instance. However, you can configure LangSmith to use an external Redis instance. By configuring an external Redis instance, you can more easily manage backups, scaling, and other operational tasks for your Redis instance.

[Valkey](https://valkey.io/) is also officially supported as a drop-in replacement for Redis. Anywhere this page refers to Redis, you can use a compatible Valkey instance. See [Requirements](#requirements) for supported versions.

> [!WARNING]
>
> Each LangSmith installation must use its own dedicated Redis instance. Redis cannot be shared across separate LangSmith installations (for example, between an existing and new cluster during a migration). Sharing it across installations causes deployment tasks to be routed to the wrong cluster.

> [!TIP]
>
> **If you're using a managed Redis service**, we recommend:
>
> * [Amazon ElastiCache](https://aws.amazon.com/elasticache/redis/) (AWS)
> * [Google Cloud Memorystore](https://cloud.google.com/memorystore) (GCP)
> * [Azure Cache for Redis](https://azure.microsoft.com/en-us/services/cache/) (Azure)
>
> For cloud-specific IAM/Workload Identity authentication, refer to the [IAM authentication section](#iam-authentication).

## Requirements

* A provisioned Redis or [Valkey](https://valkey.io/) instance that your LangSmith instance will have network access to. We recommend using a managed service like:

  * [Amazon ElastiCache](https://aws.amazon.com/elasticache/redis/) (Redis or Valkey)
  * [Google Cloud Memorystore](https://cloud.google.com/memorystore) (Redis or Valkey)
  * [Azure Cache for Redis](https://azure.microsoft.com/en-us/services/cache/)

* **Supported versions:** Redis 6.2 or later, or Valkey 8. Valkey is treated as a drop-in replacement for Redis throughout this guide.

* We support both Standalone and Redis Cluster (including Valkey Cluster). See the appropriate sections for deployment instructions.

* We support no authentication, password, and [IAM/Workload Identity](#iam-authentication) authentication.

* By default, we recommend an instance with at least 2 vCPUs and 8GB of memory. However, the actual requirements will depend on your tracing workload. We recommend monitoring your Redis instance and scaling up as needed.

> [!NOTE]
>
> Redis 6.2 is the floor because of the Redis-backed run queue introduced in Agent Server (`langgraph-api`) 0.8.0. The queue enqueues runs with the `ZADD ... LT` flag, which was added in Redis 6.2. On Redis 5.0 through 6.1, run enqueue fails with a generic `ERR syntax error` that does not indicate a version mismatch. Valkey 8 includes the flag.

> [!TIP]
>
> If you enable [LangSmith Sandboxes](../Install%20an%20instance/Additional%20features/Enable%20Sandboxes/Enable%20Sandboxes%20on%20self-hosted%20LangSmith.md), we recommend setting the Redis `maxmemory-policy` to `noeviction` for the Redis metadata store used by sandbox storage. This avoids evicting filesystem metadata under memory pressure.
> With `noeviction`, Redis writes can fail when the instance reaches max memory, so keep enough memory headroom for sandbox metadata growth.

## Standalone Redis

### Connection string

You will need to assemble the connection string for your Redis instance. This connection string should include the following information:

* Host
* Database
* Port
* URL params

This will take the form of:

```
"redis://host:port/db?<url_params>"
```

An example connection string might look like:

```
"redis://langsmith-redis:6379/0"
```

Note: If your Standalone Redis requires authentication or TLS, include these directly in the connection URL:

* Use `rediss://` when TLS is enabled on your Redis server.
* Provide the password in the connection string.

For example:

```text
rediss://langsmith-redis:6380/0?password=foo
```

For IAM authentication, use the identity as the username (no password):

```text
rediss://<iam-identity>@host:6380
```

### Configuration

With your connection string in hand, you can configure your LangSmith instance to use an external Redis instance. You can do this by modifying the `values` file for your LangSmith Helm Chart installation.

```yaml Helm
redis:
  external:
    enabled: true
    connectionUrl: "Your connection url"
```

You can also store the connection URL in an existing Kubernetes Secret and reference it in your Helm values.

```yaml Helm (using an existing Secret)
redis:
  external:
    enabled: true
    # Name of an existing Secret that contains the connection URL
    existingSecretName: "my-redis-secret"
    # Key in the Secret that stores the connection URL (default shown)
    connectionUrlSecretKey: "connection_url"
```

```yaml Kubernetes Secret
apiVersion: v1
kind: Secret
metadata:
  name: my-redis-secret
type: Opaque
stringData:
  # Full connection URL, e.g., using TLS with password
  connection_url: "rediss://langsmith-redis:6380/0?password=foo"
```

Once configured, you should be able to reinstall your LangSmith instance. If everything is configured correctly, your LangSmith instance should now be using your external Redis instance.

## Redis cluster

As of LangSmith helm version **0.12.25**, we officially support **Redis Cluster**.

> [tab] v0.18.0 and later
>
> ### Cluster endpoint
>
> LangSmith discovers the nodes of a Redis Cluster from the endpoint it connects to. Set `redis.external.connectionUrl` to one endpoint that serves the cluster topology, such as a [Memorystore Cluster discovery endpoint](#memorystore-for-redis-iam-authentication), an ElastiCache configuration endpoint, or any node.
>
> The URL uses the same format as for standalone Redis, with the password in the URL:
>
> ```text theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> redis://:password@hostname:port
> ```
>
> Percent-encode special characters in the password. Use `rediss://` if your cluster uses TLS, as for standalone Redis. `redis.external.cluster.tlsEnabled` applies only to node URIs.
>
> > [!NOTE]
> >
> > Configuring Redis Cluster with `connectionUrl` requires LangSmith v0.18.0 or later. Earlier versions use node URIs (see the **Before v0.18.0** tab). Node URIs, the separate cluster password, and `redis.external.cluster.tlsEnabled` are deprecated in v0.18.0 and supported through v0.19. Node URIs take precedence over `connectionUrl` when set.
>
> ### Configuration
>
> Set `redis.external.cluster.enabled` and provide the cluster endpoint either directly in `values.yaml` or through an existing Kubernetes `Secret`.
>
> ```yaml Helm (inline values) theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> redis:
>   external:
>     enabled: true
>     # One endpoint that serves the cluster topology, with the password if your cluster requires one.
>     # Use rediss:// for TLS.
>     connectionUrl: "rediss://:your_redis_password@redis-cluster.example.internal:6379"
>     cluster:
>       enabled: true
> ```
>
> ```yaml Helm (using an existing Secret) theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> redis:
>   external:
>     enabled: true
>     # Name of an existing Secret that contains the cluster endpoint
>     existingSecretName: "my-redis-cluster-secret"
>     connectionUrlSecretKey: "connection_url"
>     cluster:
>       enabled: true
> ```
>
> If using an existing Secret, it should contain:
>
> ```yaml Kubernetes Secret theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> apiVersion: v1
> kind: Secret
> metadata:
>   name: my-redis-cluster-secret
> type: Opaque
> stringData:
>   connection_url: "rediss://:your_redis_password@redis-cluster.example.internal:6379"
> ```

> [tab] Before v0.18.0
>
> ### Host names
>
> When using Redis Cluster, provide a list of node hostnames and ports. Each node URI must be in the form:
>
> ```text theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> redis://hostname:port
> ```
>
> For example:
>
> ```text theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> redis://redis-node-0:6379
> redis://redis-node-1:6379
> redis://redis-node-2:6379
> ```
>
> Do not include a password in these URIs, and do not use `rediss` here. For Redis Cluster:
>
> * Provide the password separately via `redis.external.cluster.password` or through a Secret using `passwordSecretKey`.
> * TLS is enabled by default for Redis Cluster (`redis.external.cluster.tlsEnabled: true`). Set `tlsEnabled: false` if your cluster does not use TLS.
>
> ### Configuration
>
> When connecting to an external Redis Cluster, configure the Helm values under `redis.external.cluster`. You can either:
>
> * Provide node URIs and (optionally) a password directly in `values.yaml`.
> * Or reference an existing Kubernetes `Secret` containing node URIs and password.
>
> ```yaml Helm (inline values) theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> redis:
>   external:
>     enabled: true
>     cluster:
>       enabled: true
>       # List of cluster node URIs. Format: redis://host:port
>       nodeUris:
>         - "redis://redis-node-0:6379"
>         - "redis://redis-node-1:6379"
>         - "redis://redis-node-2:6379"
>       # Optional. If your cluster requires auth, set a password or use a Secret (recommended).
>       password: "your_redis_password"
>       # TLS is enabled by default. Set to false if your cluster does not use TLS.
>       tlsEnabled: true
> ```
>
> ```yaml Helm (using an existing Secret) theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> redis:
>   external:
>     enabled: true
>     # Name of an existing Secret that contains cluster connection details
>     existingSecretName: "my-redis-cluster-secret"
>     cluster:
>       enabled: true
>       # Keys in the Secret. Defaults shown here; override if your Secret uses different keys.
>       nodeUrisSecretKey: "redis_cluster_node_uris"
>       passwordSecretKey: "redis_cluster_password"
>       tlsEnabled: true
> ```
>
> If using an existing Secret, it should contain:
>
> ```yaml Kubernetes Secret theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> apiVersion: v1
> kind: Secret
> metadata:
>   name: my-redis-cluster-secret
> type: Opaque
> stringData:
>   # JSON array of node URIs (as a string)
>   redis_cluster_node_uris: '["redis://redis-node-0:6379","redis://redis-node-1:6379","redis://redis-node-2:6379"]'
>   # Optional if your cluster requires a password
>   redis_cluster_password: "your_redis_password"
> ```

## Azure managed Redis

[Azure Managed Redis](https://azure.microsoft.com/en-us/products/managed-redis) supports two clustering policies that affect how LangSmith connects to it. Choose the configuration below based on the clustering policy of your instance.

### OSS Cluster

LangSmith connects to OSS clustering policy instances using Redis Cluster mode.

As of LangSmith helm chart version **0.13.33**, `ssl_check_hostname=false` is supported as a node URI parameter. In our testing, the OSS clustering policy requires disabling SSL hostname verification. Azure's proxy resolves connections to internal node IPs that are not present in the certificate's SAN, causing hostname verification to fail.

```yaml
redis:
  external:
    enabled: true
    cluster:
      enabled: true
      nodeUris:
        - "redis://<node_url>:10000?ssl_check_hostname=false"
      tlsEnabled: true
```

### EnterpriseCluster

As of LangSmith helm chart version **0.13.33**, LangSmith supports Azure Managed Redis with the EnterpriseCluster policy. This policy exposes a single endpoint that handles sharding internally. LangSmith must connect to it as a standalone (single-instance) client, but it does not support cluster unsafe operations such as MULTI/EXEC. Set `redis.external.clusterSafeMode: true` to disable unsafe cluster operations.

```yaml
redis:
  external:
    enabled: true
    connectionUrl: "rediss://<azure-redis-host>:6380"
    # Required for EnterpriseCluster: use a single-instance client and disable unsafe cluster operations
    clusterSafeMode: true
```

For Microsoft Entra (IAM) authentication with EnterpriseCluster, see the [Azure tab in IAM authentication](#azure-cache-for-redis) and include `clusterSafeMode: true` in your Helm values.

## TLS with Redis

Use this section to configure TLS for Redis connections. For mounting internal/public CAs so LangSmith trusts your Redis server certificate, see [Configure custom TLS certificates](../Platform%20auth%20%26%20access%20control/Configure%20custom%20TLS%20certificates.md#mount-internal-cas-for-tls).

### Server TLS (one-way)

To validate the Redis server certificate:

* Provide a CA bundle using `config.customCa.secretName` and `config.customCa.secretKey`.
* For Standalone Redis, use `rediss://` in the connection URL.
* For Redis Cluster, `redis.external.cluster.tlsEnabled` defaults to `true`. Ensure it is not set to `false`.

> [!WARNING]
>
> Mount a custom CA only when your Redis server uses an internal or private CA. Publicly trusted CAs do not require this configuration.

```yaml Helm (Standalone - server TLS)
config:
  customCa:
    secretName: "langsmith-custom-ca"  # Secret containing your CA bundle
    secretKey: "ca.crt"    # Key in the Secret with the CA bundle
redis:
  external:
    enabled: true
    # Use rediss:// and include password if required by your server
    connectionUrl: "rediss://host:6380/0?password=<PASSWORD>"
```

```yaml Helm (Cluster - server TLS)
config:
  customCa:
    secretName: "langsmith-custom-ca"  # Secret containing your CA bundle
    secretKey: "ca.crt"    # Key in the Secret with the CA bundle
redis:
  external:
    enabled: true
    cluster:
      enabled: true
      tlsEnabled: true
      nodeUris:
        - "redis://redis-node-0:6379"
        - "redis://redis-node-1:6379"
        - "redis://redis-node-2:6379"
      password: "<PASSWORD>"
```

```yaml Kubernetes Secret (CA bundle)
apiVersion: v1
kind: Secret
metadata:
  name: langsmith-custom-ca
type: Opaque
stringData:
  ca.crt: |
    -----BEGIN CERTIFICATE-----
    <ROOT_OR_INTERMEDIATE_CA_CERT_CHAIN>
    -----END CERTIFICATE-----
```

### Mutual TLS with client auth (mTLS)

As of LangSmith helm chart version **0.12.29**, we support mTLS for Redis clients. For server-side authentication in mTLS, use the [Server TLS steps](#server-tls-one-way) (custom CA) in addition to the following client certificate configuration.

If your Redis server requires client certificate authentication:

* Provide a Secret with your client certificate and key.
* Reference it via `redis.external.clientCert.secretName` and specify the keys with `certSecretKey` and `keySecretKey`.
* For Standalone Redis, keep using `rediss://` in the connection URL.
* For Redis Cluster, `redis.external.cluster.tlsEnabled` defaults to `true`. Ensure it is not set to `false`.

```yaml Helm (client Auth)
redis:
  external:
    enabled: true
    clientCert:
      secretName: "redis-mtls-secret"
      certSecretKey: "tls.crt"
      keySecretKey: "tls.key"
    # Standalone example:
    # connectionUrl: "rediss://host:6380/0?password=<PASSWORD>"
    # Or, for Cluster:
    cluster:
      enabled: true
      tlsEnabled: true
      nodeUris:
        - "redis://redis-node-0:6379"
        - "redis://redis-node-1:6379"
        - "redis://redis-node-2:6379"
      password: "<PASSWORD>"
```

```yaml Kubernetes Secret (client cert/key)
apiVersion: v1
kind: Secret
metadata:
  name: redis-mtls-secret
type: Opaque
stringData:
  tls.crt: |
    -----BEGIN CERTIFICATE-----
    <CLIENT_CERT>
    -----END CERTIFICATE-----
  tls.key: |
    <PRIVATE_KEY_HEADER>
    <CLIENT_KEY>
    <PRIVATE_KEY_FOOTER>
```

#### Pod security context for certificate volumes

The certificate volumes mounted for mTLS are protected by file access restrictions. To ensure all LangSmith pods can read the certificate files, you must set `fsGroup: 1000` in the pod security context.

You can configure this in one of two ways:

**Option 1: Use `commonPodSecurityContext`**

Set the `fsGroup` at the top level to apply it to all pods:

```yaml
commonPodSecurityContext:
  fsGroup: 1000
```

**Option 2: Add to individual pod security contexts**

If you need more granular control, add the `fsGroup` to each pod's security context individually. See the [mtls configuration example](https://github.com/langchain-ai/helm/blob/main/charts/langsmith/examples/mtls_config.yaml) for a complete reference.

## IAM authentication

As of LangSmith helm chart version **0.12.34**, LangSmith supports IAM authentication for standalone Redis. As of LangSmith version **v0.16.0** (v16), Redis Cluster also supports IAM authentication. This allows you to use cloud provider workload identity instead of static passwords.

> [!NOTE]
>
> Redis Cluster with IAM authentication requires LangSmith v0.16.0 or later. Earlier LangSmith versions support IAM authentication only for standalone Redis. Also, not all cloud providers support IAM authentication for all Redis offerings. Check your cloud provider's documentation to verify IAM support for your specific Redis setup (e.g., GCP only supports IAM for Memorystore Cluster, not standalone Memorystore).

> [tab] AWS
>
> ### ElastiCache for Redis IAM authentication
>
> ElastiCache for Redis supports [IAM authentication](https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/auth-iam.html), which allows you to authenticate using AWS IAM credentials instead of Redis AUTH passwords.
>
> #### Prerequisites
>
> 1. **Configure workload identity** in your Kubernetes cluster using [AWS IRSA](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html) or [EKS Pod Identity](https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html)
> 2. **Enable IAM authentication** on your ElastiCache instance and grant access to your workload identity
>
> #### Configuration
>
> **Standalone Redis:**
>
> ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> redis:
>   external:
>     enabled: true
>     existingSecretName: "redis-secret"
>     iamAuthProvider: "aws"
> ```
>
> ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> apiVersion: v1
> kind: Secret
> metadata:
>   name: redis-secret
> type: Opaque
> stringData:
>   # IAM connection URL - identity as username, no password
>   connection_url: "rediss://<iam-identity>@<elasticache-host>:6380"
> ```
>
> **Redis Cluster:**
>
> ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> redis:
>   external:
>     enabled: true
>     existingSecretName: "redis-cluster-secret"
>     iamAuthProvider: "aws"
>     cluster:
>       enabled: true
>       nodeUrisSecretKey: "redis_cluster_node_uris"
>       tlsEnabled: true
> ```
>
> #### Required annotations
>
> You must apply the ServiceAccount annotations required by AWS IRSA to all LangSmith components that connect to Redis:
>
> **Deployments:** `backend`, `queue`, `platformBackend`, `hostBackend`, `ingestQueue`
>
> Example configuration:
>
> ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> backend:
>   serviceAccount:
>     annotations:
>       eks.amazonaws.com/role-arn: "arn:aws:iam::<account-id>:role/<role-name>"
>
> queue:
>   serviceAccount:
>     annotations:
>       eks.amazonaws.com/role-arn: "arn:aws:iam::<account-id>:role/<role-name>"
>
> platformBackend:
>   serviceAccount:
>     annotations:
>       eks.amazonaws.com/role-arn: "arn:aws:iam::<account-id>:role/<role-name>"
>
> hostBackend:
>   serviceAccount:
>     annotations:
>       eks.amazonaws.com/role-arn: "arn:aws:iam::<account-id>:role/<role-name>"
>
> ingestQueue:
>   serviceAccount:
>     annotations:
>       eks.amazonaws.com/role-arn: "arn:aws:iam::<account-id>:role/<role-name>"
> ```
>
> See the [Helm values reference](https://github.com/langchain-ai/helm/blob/main/charts/langsmith/values.yaml) for the full list of configurable services.

> [tab] GCP
>
> ### Memorystore for Redis IAM authentication
>
> Memorystore for Redis supports [IAM authentication](https://docs.cloud.google.com/memorystore/docs/cluster/about-iam-auth) for **Cluster instances only** (not standalone Memorystore). This allows you to authenticate using GCP service accounts.
>
> > [!NOTE]
> >
> > IAM authentication is only available for Memorystore Cluster, not standalone Memorystore instances.
>
> #### Prerequisites
>
> 1. **Configure workload identity** in your Kubernetes cluster using [GCP Workload Identity](https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity)
> 2. **Enable IAM authentication** on your Memorystore Cluster and grant access to your workload identity
>
> #### Configuration
>
> **LangSmith v0.18.0 and later:**
>
> Set the connection URL to the cluster's discovery endpoint. LangSmith discovers the cluster's shards from it. IAM authentication replaces the password, so the URL has none. Use `rediss://` if in-transit encryption is enabled on the cluster, and `redis://` if it is not.
>
> ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> redis:
>   external:
>     enabled: true
>     existingSecretName: "redis-cluster-secret"
>     connectionUrlSecretKey: "connection_url"
>     iamAuthProvider: "gcp"
>     cluster:
>       enabled: true
> ```
>
> ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> apiVersion: v1
> kind: Secret
> metadata:
>   name: redis-cluster-secret
> type: Opaque
> stringData:
>   # The cluster's discovery endpoint, for example rediss://10.1.2.3:6379
>   connection_url: "rediss://<discovery-endpoint-ip>:6379"
> ```
>
> **Before LangSmith v0.18.0:**
>
> ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> redis:
>   external:
>     enabled: true
>     existingSecretName: "redis-cluster-secret"
>     iamAuthProvider: "gcp"
>     cluster:
>       enabled: true
>       nodeUrisSecretKey: "redis_cluster_node_uris"
>       tlsEnabled: true
> ```
>
> ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> apiVersion: v1
> kind: Secret
> metadata:
>   name: redis-cluster-secret
> type: Opaque
> stringData:
>   redis_cluster_node_uris: '["redis://node-0:6379","redis://node-1:6379","redis://node-2:6379"]'
> ```
>
> #### Required annotations
>
> You must apply the ServiceAccount annotations required by GCP Workload Identity to all LangSmith components that connect to Redis:
>
> **Deployments:** `backend`, `queue`, `platformBackend`, `hostBackend`, `ingestQueue`
>
> Example configuration:
>
> ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> backend:
>   serviceAccount:
>     annotations:
>       iam.gke.io/gcp-service-account: "<service-account>@<project>.iam.gserviceaccount.com"
>
> queue:
>   serviceAccount:
>     annotations:
>       iam.gke.io/gcp-service-account: "<service-account>@<project>.iam.gserviceaccount.com"
>
> platformBackend:
>   serviceAccount:
>     annotations:
>       iam.gke.io/gcp-service-account: "<service-account>@<project>.iam.gserviceaccount.com"
>
> hostBackend:
>   serviceAccount:
>     annotations:
>       iam.gke.io/gcp-service-account: "<service-account>@<project>.iam.gserviceaccount.com"
>
> ingestQueue:
>   serviceAccount:
>     annotations:
>       iam.gke.io/gcp-service-account: "<service-account>@<project>.iam.gserviceaccount.com"
> ```
>
> See the [Helm values reference](https://github.com/langchain-ai/helm/blob/main/charts/langsmith/values.yaml) for the full list of configurable services.

> [tab] Azure
>
> ### Azure Cache for Redis with Microsoft Entra authentication
>
> Azure Cache for Redis supports [Microsoft Entra authentication](https://learn.microsoft.com/en-us/azure/azure-cache-for-redis/cache-azure-active-directory-for-authentication), which allows you to authenticate using Azure managed identities.
>
> #### Prerequisites
>
> 1. **Configure workload identity** in your Kubernetes cluster using [Azure Workload Identity](https://learn.microsoft.com/en-us/azure/aks/workload-identity-overview)
> 2. **Enable Microsoft Entra authentication** on your Azure Cache for Redis and grant access to your workload identity
>
> #### Configuration
>
> **Standalone Redis:**
>
> ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> redis:
>   external:
>     enabled: true
>     existingSecretName: "redis-secret"
>     iamAuthProvider: "azure"
>     # Include if using EnterpriseCluster policy. See the Azure managed Redis section for details.
>     # clusterSafeMode: true
> ```
>
> ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> apiVersion: v1
> kind: Secret
> metadata:
>   name: redis-secret
> type: Opaque
> stringData:
>   # IAM connection URL - managed identity as username, no password
>   connection_url: "rediss://<managed-identity>@<azure-redis-host>:6380"
> ```
>
> **Redis Cluster:**
>
> ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> redis:
>   external:
>     enabled: true
>     existingSecretName: "redis-cluster-secret"
>     iamAuthProvider: "azure"
>     cluster:
>       enabled: true
>       nodeUrisSecretKey: "redis_cluster_node_uris"
>       tlsEnabled: true
> ```
>
> #### Required annotations
>
> You must apply the ServiceAccount annotations and pod labels required by Azure Workload Identity to all LangSmith components that connect to Redis:
>
> **Deployments:** `backend`, `queue`, `platformBackend`, `hostBackend`, `ingestQueue`
>
> Example configuration:
>
> ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> backend:
>   serviceAccount:
>     annotations:
>       azure.workload.identity/client-id: "<managed-identity-client-id>"
>   deployment:
>     labels:
>       azure.workload.identity/use: "true"
>
> queue:
>   serviceAccount:
>     annotations:
>       azure.workload.identity/client-id: "<managed-identity-client-id>"
>   deployment:
>     labels:
>       azure.workload.identity/use: "true"
>
> platformBackend:
>   serviceAccount:
>     annotations:
>       azure.workload.identity/client-id: "<managed-identity-client-id>"
>   deployment:
>     labels:
>       azure.workload.identity/use: "true"
>
> hostBackend:
>   serviceAccount:
>     annotations:
>       azure.workload.identity/client-id: "<managed-identity-client-id>"
>   deployment:
>     labels:
>       azure.workload.identity/use: "true"
>
> ingestQueue:
>   serviceAccount:
>     annotations:
>       azure.workload.identity/client-id: "<managed-identity-client-id>"
>   deployment:
>     labels:
>       azure.workload.identity/use: "true"
> ```
>
> See the [Helm values reference](https://github.com/langchain-ai/helm/blob/main/charts/langsmith/values.yaml) for the full list of configurable services.

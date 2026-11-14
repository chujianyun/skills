# Connect to an external ClickHouse database

ClickHouse is a high-performance, column-oriented database system. It allows for fast ingestion of data and is optimized for analytical queries.

LangSmith uses ClickHouse as the primary data store for traces and feedback. By default, self-hosted LangSmith will use an internal ClickHouse database that is bundled with the LangSmith instance. This is run as a stateful set in the same Kubernetes cluster as the LangSmith application.

However, you can configure LangSmith to use an external ClickHouse database for easier management and scaling. By configuring an external ClickHouse database, you can manage backups, scaling, and other operational tasks for your database. While ClickHouse is not yet a native service in Azure, AWS, or Google Cloud, you can run LangSmith with an external ClickHouse database in the following ways:

* [LangSmith-managed ClickHouse](LangSmith-managed%20ClickHouse.md)

* Provision a [ClickHouse Cloud](https://clickhouse.cloud/) either directly or through a cloud provider marketplace:

  * [Azure Marketplace](https://azuremarketplace.microsoft.com/en-us/marketplace/apps/clickhouse.clickhouse_cloud?tab=Overview)
  * [Google Cloud Marketplace](https://console.cloud.google.com/marketplace/product/clickhouse-public/clickhouse-cloud)
  * [AWS Marketplace](https://aws.amazon.com/marketplace/seller-profile?id=adb43736-8b95-4d49-8009-3693cbee8578)

* On a VM in your cloud provider

> [!NOTE]
>
> Using the first two options (LangSmith-managed ClickHouse or ClickHouse Cloud) will provision a Clickhouse service OUTSIDE of your VPC. However, both options support private endpoints, meaning that you can direct traffic to the ClickHouse service without exposing it to the public internet (eg via AWS PrivateLink, or GCP Private Service Connect).
>
> Additionally, sensitive information can be configured to be not stored in Clickhouse. Please contact support via [support.langchain.com](https://support.langchain.com) for more information.

## Requirements

* A provisioned ClickHouse instance that your LangSmith application will have network access to (see above for options).
* A user with admin access to the ClickHouse database. This user will be used to create the necessary tables, indexes, and views.
* We support both standalone ClickHouse and externally managed clustered deployments. For clustered deployments, ensure all nodes are running the same version. Note that clustered setups are not supported with bundled ClickHouse installations.
* We only support ClickHouse 23.9 or later. Use of ClickHouse 24.2 or later requires LangSmith v0.6 or later.

> [!WARNING]
>
> Downgrading ClickHouse to an earlier version can cause data corruption of system tables and result in significant downtime. If you need assistance with a ClickHouse version change or are experiencing issues after an upgrade, contact support at [support.langchain.com](https://support.langchain.com) before attempting a downgrade.

* We rely on a few configuration parameters to be set on your ClickHouse instance. These are detailed below:

```xml
<profiles>
  <default>
      <async_insert>1</async_insert> # Turn on async insert
      <async_insert_max_data_size>25000000</async_insert_max_data_size> # Flush data to disk after 25MB. You may need to adjust this based on your workload.
      <wait_for_async_insert>0</wait_for_async_insert> # Disable waiting for async insert by default
      <parallel_view_processing>1</parallel_view_processing> # Enable parallel view processing
      <materialize_ttl_after_modify>0</materialize_ttl_after_modify> # Disable TTL materialization after modify
      <wait_for_async_insert_timeout>120</wait_for_async_insert_timeout> # Set the timeout for waiting for async insert
      <lightweight_deletes_sync>0</lightweight_deletes_sync> # Disable lightweight deletes sync
      <allow_materialized_view_with_bad_select>1</allow_materialized_view_with_bad_select> # Allow materialized views with legacy SELECT statements that cause CH to fail
  </default>
</profiles>
```

> [!WARNING]
>
> Our system has been tuned to work with the above configuration parameters. Changing these parameters may result in unexpected behavior.

## HA replicated Clickhouse cluster

> [!WARNING]
>
> By default, the setup process above will only work with a single node Clickhouse cluster.

If you would like to use a multi-node Clickhouse cluster for HA, we support this with additional required configuration. This setup can use a Clickhouse cluster with multiple nodes where data replicated via Zookeeper or Clickhouse Keeper. For more information on Clickhouse replication, see [Clickhouse Data Replication Docs](https://clickhouse.com/docs/architecture/replication).

In order to setup LangSmith with a replicated multi-node Clickhouse setup:

* You need to have a Clickhouse cluster that is setup with Keeper or Zookeeper for data replication and the appropriate settings. See [Clickhouse Replication Setup Docs](https://clickhouse.com/docs/architecture/replication).
* You need to set the cluster setting in the [LangSmith Configuration](#configuration) section, specifically the `cluster` settings to match your Clickhouse Cluster name. This will use the `Replicated` table engines when running the Clickhouse migrations.
* If in addition to HA, you would like to load balance among the Clickhouse nodes (to distribute reads or writes), we suggest using a load balancer or DNS load balancing to round robin among your Clickhouse servers.
* **Note**: You will need to enable your `cluster` setting before launching LangSmith for the first time and running the Clickhouse migrations. This is a requirement since the table engine will need to be created as a `Replicated` table engine vs the non replicated engine type.

When running migrations with `cluster` enabled, the migration will create the `Replicated` table engine flavor. This means that data will be replicated among the servers in the cluster. This is a master-master setup where any server can process reads, writes, or merges.

> [!NOTE]
>
> For an example setup of a replicated ClickHouse cluster, refer to the [replicated ClickHouse section](https://github.com/langchain-ai/helm/blob/main/charts/langsmith/examples/replicated-clickhouse/README.md) in the LangSmith Helm chart repo, under examples.

## LangSmith-managed ClickHouse

* If using LangSmith-managed ClickHouse, you will need to set up a VPC peering connection between the LangSmith VPC and the ClickHouse VPC. Please contact support via [support.langchain.com](https://support.langchain.com) for more information.
* You will also need to set up Blob Storage. You can read more about Blob Storage in the [Blob Storage documentation](Enable%20blob%20storage.md).

> [!NOTE]
>
> ClickHouse installations managed by LangSmith use a SharedMerge engine, which automatically clusters them and separates compute from storage.

For more information, refer to the [managed ClickHouse](LangSmith-managed%20ClickHouse.md) page.

## Parameters

You will need to provide several parameters to your LangSmith installation to configure an external ClickHouse database. These parameters include:

* **Host**: The hostname or IP address of the ClickHouse database
* **HTTP Port**: The port that the ClickHouse database listens on for HTTP connections
* **Native Port**: The port that the ClickHouse database listens on for [native connections](https://clickhouse.com/docs/en/interfaces/tcp)
* **Database**: The name of the ClickHouse database that LangSmith should use
* **Username**: The username to use to connect to the ClickHouse database
* **Password**: The password to use to connect to the ClickHouse database
* **Cluster (Optional)**: The name of the ClickHouse cluster if using an external Clickhouse cluster. When set, LangSmith will run migrations on the cluster and replicate data across instances.

> [!WARNING]
>
> Important considerations for clustered deployments:
>
> * Clustered setups must be configured on a fresh schema - existing standalone ClickHouse instances cannot be converted to clustered mode.
>
> * Clustering is only supported with externally managed ClickHouse deployments. It is not compatible with bundled ClickHouse installations as these do not include required ZooKeeper configurations.
>
> * When using a clustered deployment, LangSmith will automatically:
>
>   * Run database migrations across all nodes in the cluster
>   * Configure tables for data replication across the cluster
>
> Note that while data is replicated across nodes, LangSmith does not configure distributed tables or handle query routing - queries will be directed to the specified host. You will need to handle any load balancing or query distribution at the infrastructure level if desired.

## Configuration

With these parameters in hand, you can configure your LangSmith instance to use the provisioned ClickHouse database. You can do this by modifying the `config.yaml` file for your LangSmith Helm Chart installation.

```yaml Helm
clickhouse:
  external:
    enabled: true
    host: "host"
    port: "http port"
    nativePort: "native port"
    user: "default"
    password: "password"
    database: "default"
    tls: false
    cluster: "my_cluster_name"  # Optional: Set this if using an external Clickhouse cluster
```

Once configured, you should be able to reinstall your LangSmith instance. If everything is configured correctly, your LangSmith instance should now be using your external ClickHouse database.

## TLS with ClickHouse

Use this section to configure TLS for ClickHouse connections. For mounting internal/public CAs so LangSmith trusts your ClickHouse server certificate, see [Configure custom TLS certificates](../Platform%20auth%20%26%20access%20control/Configure%20custom%20TLS%20certificates.md#mount-internal-cas-for-tls).

### Server TLS (one-way)

To enable TLS for ClickHouse connections:

* Set `tls: true` in your configuration (or use `tlsSecretKey` with an external secret).
* Use the appropriate TLS ports (typically `8443` for HTTP and `9440` for native TCP connections).
* Provide a CA bundle using `config.customCa.secretName` and `config.customCa.secretKey` if using an internal CA.

> [!WARNING]
>
> Mount a custom CA only when your ClickHouse server uses an internal or private CA. Publicly trusted CAs do not require this configuration.
>
> If you do set `config.customCa`, that bundle becomes the only trust store for the ClickHouse migrations job. The job checks ClickHouse with `curl`, which reads `SSL_CERT_FILE` and ignores the system CA store. The backend pods use Python, which trusts both. So a bundle missing a root can leave the application working while every upgrade fails with `Timeout reached. ClickHouse is not ready.` and no further detail. Include every root your ClickHouse server chains to, not only your internal ones. For LangSmith-managed ClickHouse, that means ISRG Root X1 (see [TLS certificates](LangSmith-managed%20ClickHouse.md#tls-certificates)).

```yaml Helm (server TLS)
config:
  customCa:
    secretName: "langsmith-custom-ca"  # Secret containing your CA bundle
    secretKey: "ca.crt"    # Key in the Secret with the CA bundle
clickhouse:
  external:
    enabled: true
    host: "your-clickhouse-host.example.com"
    port: "8443"
    nativePort: "9440"
    user: "default"
    password: "password"
    database: "default"
    tls: true
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

As of LangSmith helm chart version **0.12.29**, we support mTLS for ClickHouse clients. For server-side authentication in mTLS, use the [Server TLS steps](#server-tls-one-way) (custom CA) in addition to the following client certificate configuration.

If your ClickHouse server requires client certificate authentication:

* Provide a Secret with your client certificate and key.
* Reference it via `clickhouse.external.clientCert.secretName` and specify the keys with `certSecretKey` and `keySecretKey`.

```yaml Helm (client auth)
clickhouse:
  external:
    enabled: true
    host: "your-clickhouse-host.example.com"
    port: "8443"
    nativePort: "9440"
    user: "default"
    password: "password"
    database: "default"
    tls: true
    clientCert:
      secretName: "clickhouse-client-cert"
      certSecretKey: "tls.crt"
      keySecretKey: "tls.key"
```

```yaml Kubernetes Secret (client cert/key)
apiVersion: v1
kind: Secret
metadata:
  name: clickhouse-client-cert
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

#### Migrations with TLS

The migration job uses the same TLS and client certificate configuration as the application and connects over the native protocol on `clickhouse.external.nativePort`. When TLS is enabled, set `nativePort` to your ClickHouse native TLS port (`9440` by default). A separate non-TLS native port is not required.

> [!WARNING]
>
> Leaving `nativePort` at `9000` with `tls: true` causes the migration job to fail, because it attempts a TLS handshake against the plaintext port.

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

If you need more granular control, add the `fsGroup` to each pod's security context individually. See the [mTLS configuration example](https://github.com/langchain-ai/helm/blob/main/charts/langsmith/examples/mtls_config.yaml) for a complete reference.

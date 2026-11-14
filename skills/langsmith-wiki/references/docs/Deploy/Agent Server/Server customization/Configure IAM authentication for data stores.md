# Configure IAM authentication for data stores

> Configure Agent Server to use cloud workload identities for PostgreSQL and Redis authentication.

Agent Server can use a cloud workload identity to generate short-lived PostgreSQL and Redis credentials at runtime. This removes static database and cache passwords from your deployment configuration. Connection and pooling behavior stay the same.

> [!NOTE]
>
> Data store IAM authentication requires `langgraph-api>=0.12.0`.

## Supported services

| Provider value | PostgreSQL | Redis | Credential source |
| - | - | - | - |
| `aws` | Amazon RDS or Aurora PostgreSQL | Amazon ElastiCache provisioned cache clusters or replication groups | AWS SDK default credential chain |
| `azure` | Azure Database for PostgreSQL Flexible Server | Azure Managed Redis or Azure Cache for Redis | Microsoft Entra `DefaultAzureCredential` |
| `gcp` | Cloud SQL for PostgreSQL | Memorystore for Redis Cluster | Google Application Default Credentials (ADC) |

> [!WARNING]
>
> The GCP PostgreSQL provider supports Cloud SQL. It does not support AlloyDB, which requires a different token scope.

The provider setting controls authentication only. Configure network access, TLS, database users, cache users, and provider permissions before starting Agent Server.

## Enable IAM authentication

To enable IAM authentication:

1. Enable IAM or identity-based authentication on the managed data store.
2. Create the database or cache principal and grant it only the permissions Agent Server needs.
3. Make workload identity credentials available to every Agent Server API and queue process.
4. Set a connection URI that contains the principal name but no static password.
5. Set the corresponding provider selector to `aws`, `azure`, or `gcp`:

   ```shell
   AGENT_POSTGRES_IAM_AUTH_PROVIDER=<provider>
   AGENT_REDIS_IAM_AUTH_PROVIDER=<provider>
   ```

You can enable IAM authentication for PostgreSQL, Redis, or both. When a selector is unset, Agent Server continues to use the password from that data store's connection URI.

Use these connection URI variables for your deployment type:

| Deployment | PostgreSQL URI | Redis URI |
| - | - | - |
| Standalone Agent Server | `DATABASE_URI` | `REDIS_URI` |
| Self-hosted deployment with a control plane | `POSTGRES_URI_CUSTOM` | `REDIS_URI_CUSTOM` |

The connection URIs must meet the following requirements:

* **Transport security**: Use `sslmode=require` or a stricter verification mode for PostgreSQL, and `rediss://` for Redis.
* **Character encoding**: Percent-encode URI-reserved characters in usernames, such as `@` as `%40`.
* **Private certificate authority**: If Redis TLS uses a private certificate authority, set `REDIS_TLS_CA_CERT` to the base64-encoded PEM CA bundle.
* **Cluster mode**: If the Redis service uses cluster mode, also set `REDIS_CLUSTER=true`.

## Configure AWS

Agent Server uses the AWS SDK default credential chain to create RDS authentication tokens and ElastiCache SigV4 authentication tokens.

Before configuring Agent Server:

* [Enable IAM database authentication](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.IAMDBAuth.html) for RDS or Aurora PostgreSQL. Grant the database user the `rds_iam` role and grant the workload identity `rds-db:connect` for that user.
* [Enable IAM authentication](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/auth-iam.html) for the ElastiCache user. Grant the workload identity `elasticache:Connect` for both the ElastiCache cache or replication group and the ElastiCache user.
* Configure AWS credentials through EKS Pod Identity, IAM roles for service accounts (IRSA), an instance profile, or another AWS SDK credential source. Set `AWS_REGION` or `AWS_DEFAULT_REGION` to the data store's region.

Set the database usernames in the connection URIs:

```shell
AWS_REGION=<region>
AGENT_POSTGRES_IAM_AUTH_PROVIDER=aws
AGENT_REDIS_IAM_AUTH_PROVIDER=aws
DATABASE_URI="postgresql://<rds-user>@<rds-endpoint>:5432/<database>?sslmode=require"
REDIS_URI="rediss://<elasticache-iam-user>@<elasticache-endpoint>:6379"
```

The Redis username must match the IAM-enabled ElastiCache user. Agent Server supports provisioned ElastiCache cache clusters and replication groups. ElastiCache IAM authentication requires in-transit encryption and either Valkey 7.2 or later or Redis OSS 7.0 or later.

## Configure Azure

Agent Server uses `DefaultAzureCredential` to obtain Microsoft Entra tokens for PostgreSQL and Redis. The credential chain supports Azure Workload Identity, managed identities, and service principals.

Before configuring Agent Server:

* [Configure Microsoft Entra authentication](https://learn.microsoft.com/azure/postgresql/security/security-connect-with-managed-identity) for Azure Database for PostgreSQL Flexible Server. Create a database role for the managed identity or service principal. Use that role name as the PostgreSQL URI username.
* [Configure Microsoft Entra authentication](https://learn.microsoft.com/azure/redis/entra-for-authentication) and a data access policy for Azure Managed Redis. Use the managed identity or service principal object ID as the Redis URI username.
* Configure Azure Workload Identity, a managed identity, or another `DefaultAzureCredential` source for each Agent Server workload.

Set the Microsoft Entra principal identifiers in the connection URIs:

```shell
AGENT_POSTGRES_IAM_AUTH_PROVIDER=azure
AGENT_REDIS_IAM_AUTH_PROVIDER=azure
DATABASE_URI="postgresql://<entra-principal-name>@<postgres-host>:5432/<database>?sslmode=require"
REDIS_URI="rediss://<entra-object-id>@<redis-host>:<port>"
```

Set `REDIS_CLUSTER=true` when using Azure Managed Redis in cluster mode. Agent Server refreshes Microsoft Entra tokens and reauthenticates open Redis connections before token expiration.

## Configure GCP

Agent Server uses Google ADC to obtain Cloud SQL login tokens and Memorystore access tokens. ADC supports GKE Workload Identity Federation, attached service accounts, service account impersonation, and `GOOGLE_APPLICATION_CREDENTIALS`.

Before configuring Agent Server:

* [Configure Cloud SQL IAM database authentication](https://cloud.google.com/sql/docs/postgres/iam-logins), add the IAM principal as a database user, and grant it `roles/cloudsql.instanceUser`. Grant database privileges separately.
* [Configure Memorystore IAM authentication](https://cloud.google.com/memorystore/docs/cluster/manage-iam-auth) and grant the workload identity `roles/redis.dbConnectionUser`.
* Configure ADC for each Agent Server workload. Prefer Workload Identity Federation or an attached service account over a service account key.

Set the Cloud SQL IAM database user in the PostgreSQL URI. Memorystore supports only the `default` Redis username:

```shell
AGENT_POSTGRES_IAM_AUTH_PROVIDER=gcp
AGENT_REDIS_IAM_AUTH_PROVIDER=gcp
DATABASE_URI="postgresql://<cloud-sql-iam-user>@<cloud-sql-host>:5432/<database>?sslmode=require"
REDIS_URI="rediss://default@<memorystore-discovery-endpoint>:<port>"
REDIS_CLUSTER=true
```

For a service account, the Cloud SQL database username is its email address without the `.gserviceaccount.com` suffix.

## Configure the standalone Helm chart

For a [standalone Agent Server deployment](../../Deploy%20to%20Self-hosted/Self-host%20standalone%20servers.md) on Kubernetes, set the provider selectors on every Agent Server workload. If the separate queue deployment is enabled, configure the API and queue deployments with the same identity and environment variables.

The following example uses AWS for both data stores. Set each provider value to `azure` or `gcp` when using another cloud provider:

```yaml
postgres:
  external:
    enabled: true
    connectionUrl: "postgresql://<database-user>@<postgres-host>:5432/<database>?sslmode=require"
redis:
  external:
    enabled: true
    connectionUrl: "rediss://<redis-user>@<redis-host>:<port>"

apiServer:
  deployment:
    extraEnv:
      - name: AGENT_POSTGRES_IAM_AUTH_PROVIDER
        value: "aws"
      - name: AGENT_REDIS_IAM_AUTH_PROVIDER
        value: "aws"

queue:
  enabled: true
  deployment:
    extraEnv:
      - name: AGENT_POSTGRES_IAM_AUTH_PROVIDER
        value: "aws"
      - name: AGENT_REDIS_IAM_AUTH_PROVIDER
        value: "aws"
```

Configure `apiServer.serviceAccount` and `queue.serviceAccount` with the cloud provider's workload identity mechanism. Both workloads must be able to obtain credentials and connect to the data stores.

## See also

* [Self-host standalone servers](../../Deploy%20to%20Self-hosted/Self-host%20standalone%20servers.md)
* [Self-hosted Agent Server environment variables](../../Deploy%20to%20Self-hosted/Reference/Self-hosted%20Agent%20Server%20environment%20variables.md)
* [Self-hosted platform features](../../Deploy%20to%20Self-hosted/Configure/Self-hosted%20platform%20features.md)
* [Configure Agent Server for scale](../../Deploy%20to%20Self-hosted/Configure/Configure%20Agent%20Server%20for%20scale.md)

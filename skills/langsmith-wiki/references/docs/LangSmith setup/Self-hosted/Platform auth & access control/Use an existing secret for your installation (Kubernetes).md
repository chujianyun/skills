# Use an existing secret for your installation (Kubernetes)

By default, LangSmith will provision several Kubernetes secrets to store sensitive information such as license keys, salts, and other configuration parameters. However, you may want to use an existing secret that you have already created in your Kubernetes cluster (or provisioned via some sort of secrets operator). This can be useful if you want to manage sensitive information in a centralized way or if you have specific security requirements.

By default we will provision the following secrets corresponding to different components of LangSmith:

* `langsmith-secrets`: This secret contains the license key and some other basic configuration parameters. To get started, use the [secrets template](https://github.com/langchain-ai/helm/blob/main/charts/langsmith/templates/secrets.yaml).
* `langsmith-redis`: This secret contains the Redis connection string (or node URIs if using Redis cluster) and password. To get started, use the [Redis secrets template](https://github.com/langchain-ai/helm/blob/main/charts/langsmith/templates/redis/secrets.yaml).
* `langsmith-postgres`: This secret contains the Postgres connection string and password. To get started, use the [Postgres secrets template](https://github.com/langchain-ai/helm/blob/main/charts/langsmith/templates/postgres/secrets.yaml).
* `langsmith-clickhouse`: This secret contains the ClickHouse connection string and password. To get started, use the [ClickHouse secrets template](https://github.com/langchain-ai/helm/blob/main/charts/langsmith/templates/clickhouse/secrets.yaml).

## Requirements

* An existing Kubernetes cluster
* A way to create Kubernetes secrets in your cluster. This can be done using `kubectl`, a Helm chart, or a secrets operator like [Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets)

## Parameters

You will need to create your own Kubernetes secrets that adhere to the structure of the secrets provisioned by the LangSmith Helm Chart.

> [!WARNING]
>
> The secrets must have the same structure as the ones provisioned by the LangSmith Helm Chart (refer to the links above to see the specific secrets). If you miss any of the required keys, your LangSmith instance may not work correctly.

An example secret may look like this:

> [!WARNING]
>
> Set `api_key_salt` once and do not change it. This value is used to hash all API keys at rest. Rotating it will permanently invalidate every existing API key in your organization, requiring all users to regenerate their keys.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: langsmith-secrets
  namespace: langsmith
stringData:
  oauth_client_id: foo
  oauth_client_secret: foo
  oauth_issuer_url: foo
  langsmith_license_key: foo
  langgraph_cloud_license_key: foo
  api_key_salt: foo
  jwt_secret: foo
  initial_org_admin_password: foo
  blob_storage_access_key: foo
  blob_storage_access_key_secret: foo
  azure_storage_account_key: foo
  azure_storage_connection_string: foo
  agent_builder_encryption_key: foo
  insights_encryption_key: foo
  # Chat (formerly Polly)
  polly_encryption_key: foo
  # Required only when enabling Engine.
  engine_encryption_key: foo
  # Optional; include only while rotating engine_encryption_key. Accepted for
  # decryption only, so runs encrypted just before the swap still complete.
  engine_encryption_key_previous: foo
  # Required only when enabling Engine. Signs Engine's usage reports; at least
  # 32 random characters.
  engine_usage_signing_secret: foo
  # Optional. Ed25519/OKP JWKS (JSON) that signs OAuth Authorization Server and
  # LLM auth proxy tokens. Required for self-hosted OAuth login, Remote MCP, and
  # the LLM auth proxy (see /langsmith/kubernetes#configure-a-signing-jwks).
  langsmith_signing_jwks: foo
  # Required only when enabling LangSmith Sandboxes. Ed25519 private JWK.
  sandbox_callback_signing_jwk: '<ed25519-private-jwk>'
  # A dedicated sandbox service-auth secret; name this key in
  # sandboxes.serviceAuth.secretKey (chart 0.18.0-rc.51 or later; earlier charts
  # sign sandbox calls with api_key_salt). Required when
  # sandboxes.external.enabled is true. Without it, the embedded sandbox runtime
  # uses api_key_salt.
  sandbox_service_auth_secret: foo
  # Optional; include only while rotating the sandbox service-auth secret, and
  # name this key in sandboxes.serviceAuth.previousSecretKey.
  sandbox_service_auth_secret_previous: foo
```

## Configuration

With these secrets provisioned, you can configure your LangSmith instance to use the secrets directly to avoid passing in secret values through plaintext. You can do this by modifying the `langsmith_config.yaml` file for your LangSmith Helm Chart installation.

```yaml
config:
  existingSecretName: "langsmith-secrets" # The name of the secret that contains the license key and other basic configuration parameters
redis:
  external:
    enabled: true # Set to true to use an external Redis instance. This secret is only needed if you are using an external Redis instance
    existingSecretName: "langsmith-redis" # The name of the secret that contains the Redis connection string and password
postgres:
  external:
    enabled: true # Set to true to use an external Postgres instance. This secret is only needed if you are using an external Postgres instance
    existingSecretName: "langsmith-postgres" # The name of the secret that contains the Postgres connection string and password
clickhouse:
  external:
    enabled: true # Set to true to use an external ClickHouse instance. This secret is only needed if you are using an external ClickHouse instance
    existingSecretName: "langsmith-clickhouse" # The name of the secret that contains the ClickHouse connection string and password
```

Once configured, you will need to update your LangSmith installation. You can follow the [upgrade guide](../Manage%20an%20instance/Upgrade%20an%20installation.md). If everything is configured correctly, your LangSmith instance should now be accessible via the Ingress. You can run the following to check that your secrets are being used correctly:

```bash
kubectl describe deployment langsmith-backend | grep -i <secret-name>
```

You should see something like this in the output:

```bash
POSTGRES_DATABASE_URI:                    <set to the key 'connection_url' in secret <your-secret-name>  Optional: false
CLICKHOUSE_DB:                            <set to the key 'clickhouse_db' in secret <your-secret-name>   Optional: false
```

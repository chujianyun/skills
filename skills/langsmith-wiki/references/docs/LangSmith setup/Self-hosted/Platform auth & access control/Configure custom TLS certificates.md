# Configure custom TLS certificates

Use this guide to configure TLS in LangSmith. Start by mounting internal certificate authorities (CAs) so your deployment trusts the right roots system‑wide, for database or external service calls. You can then configure [Playground](../../../Deploy/Prompt%20%26%20Context%20Hub/Prompts/Prompt%20engineering%20concepts.md#playground)-specific mTLS for communicating securely with supported model providers.

This page covers:

* [Mounting internal certificate authorities](#mount-internal-cas-for-tls) (CAs) system-wide to enable TLS for database connections and Playground model calls
* Using Playground-specific TLS settings to provide client certs/keys for mTLS with supported model providers

## Mount internal CAs for TLS

> [!NOTE]
>
> You must use Helm chart version 0.11.9 or later to mount internal CAs using the configuration below.

Use this approach to make internal/public CAs trusted system‑wide by LangSmith (Playground model calls and [database/external service connections](../Self-hosted%20LangSmith.md#storage-services)).

1. Create a file containing all CAs required for TLS with databases and external services. If your deployment is communicating directly to `beacon.langchain.com` without a proxy, make sure to include a public trusted CA. All certs should be concatenated in this file with an empty line in between.

   Include every root your databases chain to, public ones as well. Once this bundle is mounted, the database migration jobs trust only this file and not the system CA store, so a missing public root fails upgrades even though the application keeps running. If you use [LangSmith-managed ClickHouse](../Connect%20external%20services/LangSmith-managed%20ClickHouse.md#tls-certificates), add ISRG Root X1.

   ```
   -----BEGIN CERTIFICATE-----
   <PUBLIC_CA>
   -----END CERTIFICATE-----

   -----BEGIN CERTIFICATE-----
   <INTERNAL_CA>
   -----END CERTIFICATE-----

   ...
   ```
2. Create a Kubernetes secret with a key containing the contents of this file.
   ```bash
   kubectl create secret generic <SECRET_NAME> --from-file=<SECRET_KEY>=<CA_BUNDLE_FILE_PATH> -n <NAMESPACE>
   ```
3. If using custom CA for TLS with your databases and other external services, provide the following values to your LangSmith helm chart:
   ```yaml Helm
   config:
     customCa:
       secretName: <SECRET_NAME> # The name of the secret created in step 2.
       secretKey: <SECRET_KEY> # The key in the secret containing the CA bundle.

   clickhouse:
     external:
       tls: true # Only enable if you want TLS for Clickhouse.
   postgres:
     external:
       customTls: true # Only enable if you want TLS for Postgres.
   ```
4. Make sure to use TLS supported connection strings:
   * **Postgres**: Add `?sslmode=verify-full&sslrootcert=system` to the end.
   * **Redis**: Use `rediss://` instead of `redis://` as the prefix.

## Use custom TLS certificates for model providers

> [!NOTE]
>
> This feature is currently only available for the following model providers:
>
> * Azure OpenAI
> * OpenAI
> * Custom (our custom model server). Refer to the [custom model server documentation](../../../Deploy/Prompt%20%26%20Context%20Hub/Prompts/Connect%20to%20models/Connect%20to%20a%20custom%20model.md) for more information.
>
> These TLS settings apply to all invocations of the selected model providers (including Online Evaluation). Use them when the provider requires mutual TLS (client cert/key) or when you must override trust with a specific CA for provider calls. They complement the internal CA bundle configured above.

You can use custom TLS certificates to connect to model providers in the Playground. This is useful if you are using a self-signed certificate, a certificate from a custom certificate authority, or mutual TLS authentication.

To use custom TLS certificates, set the following environment variables. See the [self-hosted overview](../Self-hosted%20LangSmith.md) for more information on how to configure application settings.

* \[Optional] `LANGSMITH_PLAYGROUND_TLS_KEY`: The private key in PEM format. This must be a file path (for a mounted volume). This is usually only necessary for mutual TLS authentication.
* \[Optional] `LANGSMITH_PLAYGROUND_TLS_CERT`: The certificate in PEM format. This must be a file path (for a mounted volume). This is usually only necessary for mutual TLS authentication.
* \[Optional] `LANGSMITH_PLAYGROUND_TLS_CA`: The custom certificate authority (CA) certificate in PEM format. This must be a file path (for a mounted volume). Use this to mount CAs only if you're using a helm version below `0.11.9`; otherwise, use the [Mount internal CAs for TLS](Configure%20custom%20TLS%20certificates.md#mount-internal-cas-for-tls) section above.

Once you have set these environment variables, enter the Playground **Settings** page and select the **Provider** that requires custom TLS certificates. Set your model provider configuration as usual, and the custom TLS certificates will be used when connecting to the model provider.

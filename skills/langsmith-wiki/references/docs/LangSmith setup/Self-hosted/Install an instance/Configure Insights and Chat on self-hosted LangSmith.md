# Configure Insights and Chat on self-hosted LangSmith

> Configure encryption keys and model access for Insights and Chat on self-hosted LangSmith, disable either feature, or upgrade a legacy configuration.

[Insights](../../../Monitor/Observe/Monitoring%20%26%20alerting/Discover%20errors%20and%20usage%20patterns%20with%20Insights.md) analyzes traces, and [Chat](../../../Test/Datasets%20%26%20Experiments/Analyze%20experiment%20results/LangSmith%20Chat.md) (formerly Polly) helps you work with LangSmith data. Both are part of the base installation and are enabled by default in Helm chart version 0.15.1 or later. They do not require any [additional features](Additional%20features/Configure%20additional%20self-hosted%20features.md), such as Sandboxes, Fleet, or Agent Server hosting.

> [!NOTE]
>
> For charts before 0.15.1, Insights and Chat are not enabled by default. Use the configuration supported by your pinned chart, or upgrade before following this guide.

Each feature requires its own Fernet encryption key and model access. If you followed the [Kubernetes installation guide](Self-host%20LangSmith%20on%20Kubernetes.md), you already set the keys in `langsmith_config.yaml`. Continue with [Configure model access](#configure-model-access).

## Set the encryption keys

To generate one key per feature, see [Keys and secrets](Self-host%20LangSmith%20on%20Kubernetes.md#keys-and-secrets). Do not commit encryption keys to version control.

Provide the keys in one of two ways:

* **Inline**: Set `insights.encryptionKey` and `polly.encryptionKey` in `langsmith_config.yaml`, as in the [minimum configuration](Self-host%20LangSmith%20on%20Kubernetes.md#configure-your-helm-charts).
* **Existing Secret**: Add `insights_encryption_key` and `polly_encryption_key` to your [existing LangSmith app Secret](../Platform%20auth%20%26%20access%20control/Use%20an%20existing%20secret%20for%20your%20installation%20%28Kubernetes%29.md#parameters). Reference it through `config.existingSecretName`.

Apply your Helm configuration:

```bash
helm upgrade -i langsmith langchain/langsmith --values langsmith_config.yaml --version <version> -n <namespace> --wait --debug
```

## Configure model access

Insights and Chat call models through your [provider credentials and model configurations](../../Govern/Organization/Workspace%20setup/Manage%20model%20configurations.md). For keyless Vertex AI on GKE, see [Configure GKE workload identity](../Configure%20an%20instance/Authenticate%20Vertex%20AI%20with%20GKE%20workload%20identity.md).

## Disable Insights or Chat

Disable either feature when your installation does not need it. Set the corresponding top-level flag to `false` in your [`langsmith_config.yaml`](Self-host%20LangSmith%20on%20Kubernetes.md#configure-your-helm-charts). You do not need an encryption key for a disabled feature.

```yaml
insights:
  enabled: false

polly:
  enabled: false
```

Apply your Helm configuration:

```bash
helm upgrade -i langsmith langchain/langsmith --values langsmith_config.yaml --version <version> -n <namespace> --wait --debug
```

Disabling Insights does not disable Engine or remove their shared deployment when `engine.enabled` is `true`.

## Upgrade existing configurations

This section applies only to installations upgrading from earlier chart versions.

Current charts reject the legacy `config.insights`, `config.polly`, and `backend.agentBootstrap` settings. Remove these settings rather than setting them to `false`. Contact technical support through the [Support Portal](https://support.langchain.com) for legacy deployment migration guidance.

Starting with chart 0.16.0, Insights and Engine share the `langsmith-insights-engine` image and deployment. This does not enable Engine. Move legacy `insights.apiServer`, `insights.queue`, `insights.postgres`, `insights.redis`, and `insights.namePrefix` values to `engineInsightsAgent`. Keep `insights.enabled` and `insights.encryptionKey` under `insights`.

If you pin the retired `langsmith-clio` image, remove or update that pin before upgrading. For private registries, mirror `langsmith-insights-engine`. See [Mirroring images](../Configure%20an%20instance/Mirror%20images%20for%20your%20LangSmith%20installation.md#additional-images-for-engine).

For the general upgrade procedure, see [Upgrade an installation](../Manage%20an%20instance/Upgrade%20an%20installation.md).

## See also

* [Self-host LangSmith on Kubernetes](Self-host%20LangSmith%20on%20Kubernetes.md)
* [Configure model access](../../Govern/Organization/Workspace%20setup/Manage%20model%20configurations.md)
* [Configure additional self-hosted features](Additional%20features/Configure%20additional%20self-hosted%20features.md)

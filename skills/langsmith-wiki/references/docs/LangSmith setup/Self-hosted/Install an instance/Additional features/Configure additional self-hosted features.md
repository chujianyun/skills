# Configure additional self-hosted features

> Choose which optional self-hosted LangSmith features to install, such as Sandboxes, Engine, Fleet, and Agent Server hosting, and in what order.

[Self-hosted LangSmith](../../Self-hosted%20LangSmith.md) supports optional features beyond the base installation. Complete the [Kubernetes installation](../Self-host%20LangSmith%20on%20Kubernetes.md) first. It already includes observability and evaluation, plus [Insights and Chat](../Configure%20Insights%20and%20Chat%20on%20self-hosted%20LangSmith.md). Then follow only the guides your use case requires.

## Choose additional features

Each feature has its own setup guide. Follow only the guides for the features you need. When one feature depends on another, set up the dependency first.

* **[Sandboxes](Enable%20Sandboxes/Enable%20Sandboxes%20on%20self-hosted%20LangSmith.md)**: Run isolated code workloads. Its guide covers KVM-capable nodes, JuiceFS storage, and optional service URLs.
* **[Engine](../../../../Engine/Self-hosted%20and%20BYOC/LangSmith%20Engine%20on%20Self-hosted%20and%20BYOC.md)**: Diagnose recurring issues and propose fixes. Engine requires Sandboxes, a license with the Engine entitlement, a model configuration, and Helm chart version 0.16.0 or later. [Air-gapped installations](../../../../Engine/Self-hosted%20and%20BYOC/LangSmith%20Engine%20on%20Self-hosted%20and%20BYOC.md#air-gapped-installations) and your own model providers require Helm chart version 0.17.0 or later.
* **[Fleet](Enable%20Fleet%20on%20self-hosted%20LangSmith.md)**: Create and manage no-code agents. Its guide covers Fleet services and optional tools and triggers.
* **[LLM Gateway](Enable%20the%20LLM%20Gateway.md)**: Route model calls and apply policies. It requires Helm chart version 0.17.1 or later. Its guide covers service connectivity, provider configuration, and your first gateway call.
* **[Agent Server hosting](Enable%20Agent%20Server%20hosting.md)**: Deploy and manage Agent Servers through the LangSmith UI. Its guide covers KEDA, ingress, the control plane, and the data plane.

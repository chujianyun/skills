# Deploy to self-hosted

> Host LangSmith Agent Server on your own infrastructure with full control over data, networking, and resources.

Self-hosted Agent Server hosting runs [LangSmith Agent Server](../Agent%20Server/Capabilities/Agent%20Server.md) and its supporting databases inside infrastructure that you operate. With a full self-hosted LangSmith installation, you also run the control plane and data plane listener.

LangChain ships the container images, Helm charts, and license; you provide the Kubernetes cluster (or Docker host), PostgreSQL, Redis, and the networking and observability tooling that fit your environment. Self-hosted is the best deployment option when you have data residency, regulatory constraints, custom networking, or air-gapped requirements.

Self-hosted deployments require an [Enterprise plan](https://www.langchain.com/pricing) and the LangSmith license key delivered with that plan. For a setup guide, see [Self-hosted LangSmith](../../LangSmith%20setup/Self-hosted/Self-hosted%20LangSmith.md).

## Topologies

LangSmith supports three self-hosted topologies that trade off setup complexity against control-plane features. Reference pages for [platform features](Configure/Self-hosted%20platform%20features.md), [Agent Server metrics](Configure/Agent%20Server%20metrics.md), and [diagnostics](Configure/Troubleshooting%20for%20self-hosted%20deployments.md) apply to all three.

> [card] [Full self-hosted platform](Deploy%20with%20control%20plane.md)
>
> The complete LangSmith platform—[control plane](../Get%20started/Deployment%20components/LangSmith%20control%20plane.md) UI and APIs, [data plane](../Get%20started/Deployment%20components/LangSmith%20data%20plane.md) listener, observability, evaluation, and agent deployment management. Best for teams that want the LangSmith product experience inside their own network.

> [card] [Hybrid](Hybrid.md)
>
> LangChain-hosted control plane with the data plane (Agent Servers and databases) in your infrastructure. Best when you want managed deployment workflows but need agent workloads and customer data to stay inside your VPC.

> [card] [Standalone server](Self-host%20standalone%20servers.md)
>
> The lightest option—Agent Server containers (API + queue workers) with your own PostgreSQL and Redis. No control plane, no managed UI. Best for embedding the runtime into existing infrastructure or running air-gapped.

> [card] [Platform features](Configure/Self-hosted%20platform%20features.md)
>
> Reference for self-hosted-only platform behavior: custom Postgres and Redis, listeners, and resource customization.

> [card] [Agent Server metrics](Configure/Agent%20Server%20metrics.md)
>
> Prometheus and Datadog export for Agent Server, including Agent Server UI metrics and internal metrics.

> [card] [Diagnostics](Configure/Troubleshooting%20for%20self-hosted%20deployments.md)
>
> Collect logs, inspect state, and troubleshoot a self-hosted installation.

## Who manages what

Self-hosted shifts ownership of infrastructure operations from LangChain to your team, which provides flexibility and control over how you configure and operate is layer:

| | **Who manages it** | **Where it runs** |
| - | - | - |
| LangSmith platform (UI, APIs, datastores) | You | Your infrastructure |
| Agent Server runtime | You | Your infrastructure |
| PostgreSQL and Redis | You | Your infrastructure |
| CI/CD for your apps | You | Your CI environment |
| Upgrades, scaling, and backups | You | Your infrastructure |

In return, you can integrate with your own [Postgres](Configure/Self-hosted%20platform%20features.md#custom-postgresql) and [Redis](Configure/Self-hosted%20platform%20features.md#custom-redis), size [CPU and memory](Configure/Self-hosted%20platform%20features.md#resource-customization) for your workload, and operate inside your existing network and observability stack. For the corresponding Cloud-managed model, see [Deploy to Cloud](../Deploy%20to%20Cloud/Deploy%20to%20Cloud.md).

## Next steps

> [card] [Pick a topology](Self-host%20standalone%20servers.md)
>
> Compare standalone server, full platform, and hybrid to find the right fit.

> [card] [Enable Agent Server hosting](../../LangSmith%20setup/Self-hosted/Install%20an%20instance/Additional%20features/Enable%20Agent%20Server%20hosting.md)
>
> Add a control plane and data plane to deploy and manage agents on self-hosted LangSmith.

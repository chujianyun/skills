# Bring Your Own Cloud (BYOC)

> Deploy LangSmith services and store data in your own cloud environment while LangChain operates, scales, and upgrades the infrastructure.

> [!NOTE]
>
> BYOC is only available for customers on the [Enterprise plan](https://www.langchain.com/pricing).

Bring Your Own Cloud (BYOC) lets you deploy LangSmith services and store data in your own cloud environment, while LangChain operates, scales, and upgrades the infrastructure. BYOC suits organizations that require complete sovereignty over their data, but do not want the overhead of provisioning and managing infrastructure.

BYOC uses a split responsibility model: the control plane runs in LangChain's cloud, and the data plane runs entirely in your cloud environment. For details on what LangChain manages versus what you manage, see the [BYOC shared responsibility model](BYOC%20shared%20responsibility%20model.md).

## Get started

To deploy LangSmith BYOC, [contact our sales team](https://www.langchain.com/contact-sales). After the LangChain team enables BYOC for your organization, follow the onboarding guide for [AWS](AWS/BYOC%20onboarding.md), [GCP](GCP/BYOC%20onboarding%20on%20GCP.md), or [Azure](Azure/BYOC%20onboarding%20on%20Azure.md) to create your first data plane.

## Regions and cloud providers

BYOC is generally available (GA) on AWS. BYOC on GCP and Azure is available in [beta](../Cloud/Reference/Release%20stages.md).

### AWS

You can deploy LangSmith BYOC in any of the following AWS regions:

| Area | AWS regions |
| - | - |
| **US** | `us-east-1`, `us-east-2`, `us-west-1`, `us-west-2` |
| **Canada** | `ca-central-1` |
| **EU** | `eu-central-1`, `eu-west-1`, `eu-west-2`, `eu-west-3`, `eu-north-1` |
| **APAC** | `ap-south-1`, `ap-northeast-1`, `ap-northeast-2`, `ap-northeast-3`, `ap-southeast-1`, `ap-southeast-2` |

The AWS control plane runs in `us-east-2`, at [aws.smith.langchain.com](https://aws.smith.langchain.com), regardless of where you place your AWS data planes. If you provision a data plane outside the US, your sensitive application data stays in that region while control plane metadata remains in the US:

| Control plane (US) | Data plane (your region) |
| - | - |
| Users, roles, billing, organization configuration, SSO configuration, API keys | Traces, experiments, datasets, insights runs, annotation queues, workspace secrets, and all other sensitive application data |

### GCP

BYOC on GCP can run in any GCP region. If the region you need is not enabled yet, contact the LangChain team to add it.

The GCP control plane runs in `us-central1`, on the LangSmith US region at [smith.langchain.com](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-byoc). The same split of control plane metadata and data plane application data applies. For setup, see [BYOC onboarding on GCP](GCP/BYOC%20onboarding%20on%20GCP.md). For what LangSmith deploys in your project, see [BYOC architecture on GCP](GCP/BYOC%20architecture%20on%20GCP.md).

### Azure

BYOC on Azure can run in any Azure region. If the region you need is not enabled yet, contact the LangChain team to add it.

The Azure control plane runs in `centralus`, at [azure.smith.langchain.com](https://azure.smith.langchain.com). The same split of control plane metadata and data plane application data applies. For setup, see [BYOC onboarding on Azure](Azure/BYOC%20onboarding%20on%20Azure.md). For what LangSmith deploys in your subscription, see [BYOC architecture on Azure](Azure/BYOC%20architecture%20on%20Azure.md).

## Available features

The following features are supported on AWS. For GCP and Azure beta feature availability, confirm your requirements with the LangChain team before deployment:

* **[Observability](../../Monitor/Overview/LangSmith%20Observability.md)**: Tracing, projects, dashboards, and alerts.
* **[Evaluation](../../Test/Get%20started/LangSmith%20Evaluation.md)**: Datasets, experiments, evaluators, and annotation queues.
* **[Insights](../../Monitor/Observe/Monitoring%20%26%20alerting/Discover%20errors%20and%20usage%20patterns%20with%20Insights.md)**: Automatic analysis of traces to surface usage patterns, common agent behaviors, and failure modes.
* **[LangSmith Chat](../../Test/Datasets%20%26%20Experiments/Analyze%20experiment%20results/LangSmith%20Chat.md)**: Analyze traces, threads, prompts, and evaluations from inside your workspace.
* **[Prompt engineering](../../Deploy/Prompt%20%26%20Context%20Hub/Prompt%20%26%20Context%20Hub.md#prompts)**: Prompts and prompt commits.
* **[LangSmith Agent Server](../../Deploy/Get%20started/LangSmith%20Agent%20Server.md)**: The LangSmith Agent Server control plane runs inside your data plane's cluster, so both the agent management layer and your agents run in your private network.
* **[Sandboxes](../../Deploy/Sandboxes/LangSmith%20Sandboxes.md)**: Usage through the CLI and SDK is identical to Cloud, except that you point at your data plane's endpoint.
* **[LLM Gateway](../../LLM%20Gateway/Get%20started/LLM%20Gateway.md)**: Call models across providers with one LangSmith API key, with spend, rate limit, and data protection policies enforced centrally.
* **[LLM auth proxy](../Self-hosted/Configure%20an%20instance/Set%20up%20the%20LLM%20auth%20proxy.md)**: Enforce your own authentication flows for model invocations so provider credentials are never exposed to end users.
* **[LangSmith MCP](../../Monitor/Debug/Viewing%20%26%20managing%20traces/LangSmith%20Remote%20MCP.md)**: Connect MCP-compatible clients to LangSmith to query data.
* **[Fleet](../../No-code%20agents/Fleet/No-code%20agents%20with%20LangSmith%20Fleet.md)**: Build and run no-code agents from templates, connectors, and channels.
* **[SmithDB](../../Monitor/Reference/SmithDB%20API%20migration/Migrate%20to%20SmithDB-backed%20APIs.md)**: The purpose-built observability backend for trace data, persisting to S3 on AWS, Cloud Storage on GCP, or Blob Storage on Azure in your cloud environment. Data planes created on or after October 21, 2026 run SmithDB only. ClickHouse is deprecated, and support ends in LangSmith v0.19.
* **[Engine](../../Engine/LangSmith%20Engine.md)**: Automatic detection, diagnosis, and resolution of recurring issues found in production traces. On BYOC, Engine runs its models on your own model providers, and you configure your GitHub App and Slack app in the LangSmith UI. See [Engine on BYOC](../../Engine/Self-hosted%20and%20BYOC/LangSmith%20Engine%20on%20Self-hosted%20and%20BYOC.md#engine-on-byoc).
* **[Managed Deep Agents](../../Build/Python/Deep%20Agents/Deployment/Managed%20Deep%20Agents.md)**: Build and run deep agents with connectors, channels, and schedules.

> [!NOTE]
>
> Use Managed Deep Agents CLI and SDK v0.10 or later for BYOC. To get started, follow the [Managed Deep Agents quickstart](../../Build/Python/Managed%20Deep%20Agents/Get%20started/Managed%20Deep%20Agents%20quickstart.md).

## Prerequisites

Before LangChain can provision a data plane on AWS, you need the following:

* **A LangSmith organization on AWS**: Create one at [aws.smith.langchain.com](https://aws.smith.langchain.com), then send your organization ID to the LangChain team to enable BYOC.
* **An AWS account**: LangChain recommends a fresh account dedicated to LangSmith BYOC, but it is not required.
* **A supported region**: Pick one of the AWS regions listed above.
* **An IAM role and external ID**: LangChain provides the external ID. Copy it using the button next to the **Data Planes** header in **Settings > Data Planes**, then apply the [`langsmith-byoc-role` Terraform module](https://github.com/langchain-ai/terraform/tree/main/modules/byoc/aws/langsmith-byoc-role) with this value to create the role LangChain assumes to provision and manage your data plane. You must use this module.

For GCP, see the [prerequisites in BYOC onboarding on GCP](GCP/BYOC%20onboarding%20on%20GCP.md#before-you-start).

For Azure, see the [prerequisites in BYOC onboarding on Azure](Azure/BYOC%20onboarding%20on%20Azure.md#before-you-start).

# Deploy to Cloud

> Deploy LangSmith agents to LangChain-managed Cloud infrastructure on AWS, Azure, and GCP.

[LangSmith Cloud](../../LangSmith%20setup/Cloud/Cloud%20%28SaaS%29.md) is a **managed platform for deploying your agents**. LangChain hosts and operates the [control plane](../Get%20started/Deployment%20components/LangSmith%20control%20plane.md), [data plane](../Get%20started/Deployment%20components/LangSmith%20data%20plane.md), [Agent Server](../Agent%20Server/Capabilities/Agent%20Server.md) runtime, and supporting databases on AWS, Azure, and GCP. Push code to a connected GitHub repository or invoke the `langgraph deploy` CLI, and the platform handles build, provisioning, scaling, and ongoing operations. Deployments come in [two types](Cloud%20platform%20features.md#deployment-types):

* **Serverless**: Scales to zero when idle. Suits background agents, testing, and latency-tolerant production workloads.
* **Dedicated**: Stays on and autoscales across replicas. Suits latency-sensitive production workloads.

Agent deployments running on Cloud require a [Plus plan or above](https://www.langchain.com/pricing). Before creating your first agent deployment, verify that your application runs locally with `langgraph dev`. Refer to [Local development and testing](../Get%20started/Develop%20%26%20test/Local%20development%20%26%20testing.md).

> [card] [Deploy on Cloud](Deployment%20guide/Create%20an%20Agent%20Server.md)
>
> Step-by-step setup guide for creating, configuring, and managing Cloud deployments from the LangSmith UI or the `langgraph deploy` CLI.

> [card] [Cloud platform features](Cloud%20platform%20features.md)
>
> Reference for Cloud-only platform behavior: data regions, static IPs, payload limits, deployment types, and managed database provisioning.

> [card] [Quickstart](../Get%20started/Deploy%20your%20app%20to%20cloud.md)
>
> Deploy your first LangGraph application to Cloud in a few minutes.

To deploy a code-first Deep Agent without standing up your own Agent Server, [Managed Deep Agents](../../Build/Python/Deep%20Agents/Deployment/Managed%20Deep%20Agents.md) offers a CLI-first managed runtime in public beta.

## Next steps

> [card] [Run the quickstart](../Get%20started/Deploy%20your%20app%20to%20cloud.md)
>
> Deploy a starter LangGraph application end-to-end.

> [card] [Read the full deploy guide](Deployment%20guide/Create%20an%20Agent%20Server.md)
>
> Configure environment variables, secrets, revisions, and deployment settings.

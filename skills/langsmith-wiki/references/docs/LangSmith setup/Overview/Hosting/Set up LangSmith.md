# Set up LangSmith

> Host and manage LangSmith infrastructure for observability, evaluation, and prompt engineering.

Set up **LangSmith** for [observability](../../../Monitor/Overview/LangSmith%20Observability.md), [evaluation](../../../Test/Get%20started/LangSmith%20Evaluation.md), and [prompt engineering](../../../Deploy/Prompt%20%26%20Context%20Hub/Prompt%20%26%20Context%20Hub.md#prompts). LangSmith offers Cloud, Bring Your Own Cloud (BYOC), and Self-hosted options. Choose the option that matches where your data has to live and who runs the infrastructure.

> [!NOTE]
>
> If you also want to deploy agents in production, you can use [**LangSmith Agent Server**](../../../Deploy/Get%20started/LangSmith%20Agent%20Server.md) with Cloud, BYOC, or Self-hosted.

> [card] [Cloud](../../Cloud/Cloud%20%28SaaS%29.md)
>
> Fully managed observability, evaluation, and prompt engineering.

> [card] [BYOC](../../BYOC/Bring%20Your%20Own%20Cloud%20%28BYOC%29.md)
>
> Full control over your data, while LangChain manages the infrastructure.

> [card] [Self-hosted](../../Self-hosted/Self-hosted%20LangSmith.md)
>
> Full control with observability, evaluation, and prompt engineering in your infrastructure.

Self-hosted and BYOC are available on the [Enterprise plan](https://docs.langchain.com/langsmith/pricing-plans.md). [Get a demo](https://www.langchain.com/contact-sales) to learn more.

## Compare Cloud, BYOC, and Self-hosted

| Feature | **Cloud** | **BYOC** | **Self-hosted** |
| - | - | - | - |
| **Who runs the infrastructure** | LangChain | LangChain runs the control plane, you run your data planes | You |
| **Where sensitive data lives** | LangChain's cloud | Your VPC | Your VPC |
| **Upgrades and patches** | Automatic | Automatic | Manual |
| **Scaling** | Automatic | Automatic, managed by LangChain | Manual |

[Managed Deep Agents](../../../Build/Python/Deep%20Agents/Deployment/Managed%20Deep%20Agents.md) is available in public beta on Cloud and BYOC. For BYOC, use Managed Deep Agents CLI and SDK v0.10 or later.

Cloud, BYOC, and Self-hosted support [LangSmith Agent Server](../../../Deploy/Get%20started/LangSmith%20Agent%20Server.md) for agent workloads. Refer to the [LangSmith Agent Server overview](../../../Deploy/Get%20started/LangSmith%20Agent%20Server.md) to pick a topology (Cloud managed, BYOC, Hybrid, self-hosted with control plane, or standalone).

## Common setups

* **Fastest to start, managed everything.** [LangSmith Cloud](../../Cloud/Cloud%20%28SaaS%29.md) paired with [LangSmith Agent Server](../../../Deploy/Get%20started/LangSmith%20Agent%20Server.md) on Cloud. LangChain hosts the platform, and, when you use LangSmith Agent Server, also hosts your [Agent Servers](../../../Deploy/Agent%20Server/Capabilities/Agent%20Server.md).
* **Bring Your Own Cloud.** Data stays in your VPC, and LangChain manages the infrastructure. Refer to the [BYOC overview](../../BYOC/Bring%20Your%20Own%20Cloud%20%28BYOC%29.md).
* **Observability data must stay in your infrastructure.** Self-hosted LangSmith, paired with any Agent Server hosting topology, including [self-hosted Agent Server hosting](../../../Deploy/Deploy%20to%20Self-hosted/Deploy%20with%20control%20plane.md) for agent workloads.
* **Managed observability, agents in your VPC.** LangSmith Cloud paired with [Hybrid](../../../Deploy/Deploy%20to%20Self-hosted/Hybrid.md) LangSmith Agent Server. Traces and evaluations stay on SaaS while agent workloads stay in your infrastructure.
* **Observability only, no agent hosting.** LangSmith Cloud or self-hosted, without Agent Server hosting. Run your agents wherever you already run apps and send traces to LangSmith.

## Related

> [card] [Account setup](../../Account/Account.md)
>
> Create an account, manage API keys, and choose a pricing tier.

> [card] [Plans and pricing](https://www.langchain.com/pricing)
>
> Compare LangSmith plans and tiers.

> [card] [Observability](../../../Monitor/Overview/LangSmith%20Observability.md)
>
> Trace and monitor your LLM applications.

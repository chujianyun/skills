# LangSmith Agent Server

> Deploy and manage agents with durable execution, real-time streaming, and horizontal scaling.

**LangSmith Agent Server** is a workflow orchestration runtime purpose-built for agent workloads. Agent Server hosting provides infrastructure and deployment management for running agents in production at scale. Deploy to Cloud, BYOC, or your own infrastructure, or run a standalone Agent Server without a control plane.

> [!NOTE]
>
> LangSmith Deployment is now **LangSmith Agent Server**.

> [!NOTE]
>
> This page covers how your **agents** run in production with **LangSmith Agent Server**.
>
> Where you run LangSmith for observability, evaluation, and prompt engineering is separate; refer to [Platform setup](../../LangSmith%20setup/Overview/Hosting/Set%20up%20LangSmith.md) for details.

## Deployable products

LangSmith Agent Server is framework-agnostic, which means you can deploy agents built with:

> [card] [LangGraph (and LangChain)](Deploy%20your%20app%20to%20cloud.md)
>
> Use the LangGraph CLI and app templates to deploy an application to LangSmith.

> [card] [Google ADK](Frameworks%20and%20platforms/Deploy%20Google%20ADK%20agents.md)
>
> Deploy Google Agent Development Kit (ADK) agent as a LangGraph with the `deployments-wrap-sdk` package.

> [card] [Other frameworks](Frameworks%20and%20platforms/Deploy%20other%20frameworks.md)
>
> Deploy Claude Agent SDK, Strands, CrewAI, AutoGen, and other agent frameworks with the Functional API or `deployments-wrap-sdk`.

> [card] [Looking to deploy Deep Agents?](../../Build/Python/Deep%20Agents/Deployment/Managed%20Deep%20Agents.md)
>
> Use Managed Deep Agents: the managed runtime for deploying code-first Deep Agents.

## Agent Server hosting environments

Pick an environment based on where you want the [control plane](Deployment%20components/LangSmith%20control%20plane.md) and [data plane](Deployment%20components/LangSmith%20data%20plane.md) (Agent Servers and their databases) to run. All infrastructure types use the same [Agent Server](../Agent%20Server/Capabilities/Agent%20Server.md) runtime.

> [card] [Cloud](../Deploy%20to%20Cloud/Deploy%20to%20Cloud.md)
>
> Fully managed by LangChain on AWS, Azure, and GCP. Create deployments from GitHub in the LangSmith UI or with [`langgraph deploy`](Reference/LangGraph%20CLI.md#deploy). Requires a [Plus plan or above](https://www.langchain.com/pricing).

> [card] [Self-hosted with control plane](../Deploy%20to%20Self-hosted/Deploy%20with%20control%20plane.md)
>
> Run the LangSmith Agent Server control plane and Agent Servers in your own Kubernetes cluster, alongside self-hosted LangSmith. Requires the [Enterprise plan](https://www.langchain.com/pricing) with Agent Server hosting enabled.

> [card] [Hybrid](../Deploy%20to%20Self-hosted/Hybrid.md)
>
> LangChain-managed control plane with Agent Servers and their data plane in your infrastructure. Traces flow to LangSmith Cloud or self-hosted LangSmith.

> [card] [Standalone server](../Deploy%20to%20Self-hosted/Self-host%20standalone%20servers.md)
>
> Deploy Agent Server with Docker, Compose, or Kubernetes. Bring your own PostgreSQL, Redis, and LangSmith license; no control plane. Optional [LangSmith tracing](../../Monitor/Overview/LangSmith%20Observability.md) to Cloud or a self-hosted instance.

## Common setups

* **Managed hosting for your agents.** LangSmith Agent Server on [Cloud](../Deploy%20to%20Cloud/Deploy%20to%20Cloud.md). LangChain hosts the control plane, data plane, and databases. Pairs with LangSmith Cloud.
* **Agents in your VPC, control plane managed.** LangSmith Agent Server via [Hybrid](../Deploy%20to%20Self-hosted/Hybrid.md). LangChain hosts the control plane; you host Agent Servers and their data plane. Pairs with LangSmith Cloud or self-hosted LangSmith.
* **Full data residency or air-gapped.** [Self-hosted Agent Server hosting](../Deploy%20to%20Self-hosted/Deploy%20with%20control%20plane.md). You host the control plane and Agent Servers in your own infrastructure alongside self-hosted LangSmith.
* **Agent runtime only, no control plane.** [Standalone Agent Server](../Deploy%20to%20Self-hosted/Self-host%20standalone%20servers.md). Run Agent Server containers with Docker or Kubernetes without a control plane, optionally sending traces to LangSmith Cloud or self-hosted.

For where the LangSmith platform runs, see [Platform setup](../../LangSmith%20setup/Overview/Hosting/Set%20up%20LangSmith.md).

## Understand deployment pricing

Deployments on LangSmith Cloud are billed on the compute and database resources that each deployment requests.

> [!NOTE]
>
> Deployments on LangSmith Cloud require a Plus or Enterprise plan. For more information, see the [pricing page](https://www.langchain.com/pricing).

> [card] [LangSmith Agent Server billing](../../LangSmith%20setup/Account/Billing%20%26%20usage/Manage%20billing%20in%20your%20account.md#langsmith-deployment-billing)
>
> See the rates, the hourly cost of each deployment size, and ways to reduce deployment costs.

## After deployment

Once deployed, agents work with [Agent Server](../Agent%20Server/Capabilities/Assistants/Assistants.md)'s execution model: **assistants** for configuration, **threads** for state, and **runs** for workloads. For capabilities, tutorials, server customization, and operations, see [Agent Server](../Agent%20Server/Agent%20Server.md).

> [card] [Update prompts and contexts without redeploying](../Prompt%20%26%20Context%20Hub/Prompt%20%26%20Context%20Hub.md)
>
> Manage the prompts and versioned contexts your deployed agents pull at runtime, so you can change behavior without a full deploy.

> [card] [Interact with your deployment using RemoteGraph](../Agent%20Server/Capabilities/How%20to%20interact%20with%20a%20deployment%20using%20RemoteGraph.md)
>
> Call your deployed graph from client code as if it were a local compiled graph.

> [card] [Find and fix failures with Engine](../../Engine/LangSmith%20Engine.md)
>
> Once agents are in production, use LangSmith Engine to detect recurring failures in their traces, diagnose root causes, and resolve them.

## Full-stack web apps

Ship a LangChain.js agent and chat UI together as a single web app. The Vite example uses LangSmith Agent Server as the agent backend behind a separate UI. Other examples embed the agent inside the web framework's route handlers and ship to the host platform.

> [card] [Full-stack web apps](Frameworks%20and%20platforms/Full-stack%20web%20apps/Deploy%20full-stack%20web%20apps.md)
>
> Ship a LangChain.js chat app: embed the agent in Next.js, SvelteKit, Nuxt, Cloudflare Workers, or Deno Deploy (no Agent Server required), or pair LangSmith Agent Server with a Vite + React UI.
>
> ![LangSmith](../../../assets/images/7df8b298743a-langchain.svg)
>
> ![Next.js](../../../assets/images/0a591493463c-nextjs.svg)
>
> ![SvelteKit](../../../assets/images/393eb4c96c4b-svelte.svg)
>
> ![Nuxt](../../../assets/images/094c4ec1fa83-nuxt.svg)
>
> ![Cloudflare Workers](../../../assets/images/7444f405aba4-cloudflare.svg)
>
> ![Deno Deploy](../../../assets/images/133bdb0c41c7-deno.svg)

# Cloud platform features

> Cloud-only platform features for LangSmith Agent Server, including data regions, static IP addresses, payload limits, and deployment types.

This page describes the platform features that apply only to [Cloud](../../LangSmith%20setup/Cloud/Cloud%20%28SaaS%29.md) deployments. For self-hosted equivalents, see [Deploy to self-hosted](../Deploy%20to%20Self-hosted/Deploy%20to%20self-hosted.md).

## Data region

Deployments can be created in any [LangSmith Cloud region](../../LangSmith%20setup/Cloud/Cloud%20%28SaaS%29.md#regions).

The data region for a deployment is implied by the data region of the LangSmith organization where the deployment is created. Deployments and the underlying database for the deployments cannot be migrated between data regions.

## Static IP addresses

All traffic from deployments created after January 6, 2025 comes through a NAT gateway. This NAT gateway has several static IP addresses depending on the data region.

### Allowlist IP addresses

Use the following static IP addresses to allowlist traffic for each region:

> [!NOTE]
>
> Other LangSmith services egress from a [separate IP list](../../LangSmith%20setup/Cloud/Cloud%20%28SaaS%29.md#egress-from-langchain-saas).

For automated updates, use the [egress IP inventory (JSON)](https://docs.langchain.com/langsmith/egress-ip-addresses.json). Filter by `service: langsmith-deployment`, your cloud, and your data region. Allowlist every matching `cidr`. See [Egress IP inventory](../../LangSmith%20setup/Cloud/Cloud%20%28SaaS%29.md#egress-ip-inventory) for the field definitions and update guidance.

| GCP US | GCP EU | GCP APAC | AWS US |
| - | - | - | - |
| 35.197.29.146 | 34.90.213.236 | 34.40.236.16 | 3.13.80.97 |
| 34.145.102.123 | 34.13.244.114 | 34.40.140.88 | 3.146.216.198 |
| 34.169.45.153 | 34.32.180.189 | 34.151.88.209 | 16.59.72.244 |
| 34.82.222.17 | 34.34.69.108 | 35.189.51.120 | |
| 35.227.171.135 | 34.32.145.240 | 34.40.172.39 | |
| 34.169.88.30 | 34.90.157.44 | 35.189.56.87 | |
| 34.19.93.202 | 34.141.242.180 | 35.189.17.201 | |
| 34.19.34.50 | 34.32.141.108 | 35.244.99.196 | |
| 34.59.244.194 | 34.12.178.175 | 34.40.149.177 | |
| 34.9.99.224 | 34.91.192.230 | 34.40.144.104 | |
| 34.68.27.146 | 34.32.209.237 | 34.151.130.182 | |
| 34.41.178.137 | 34.178.128.69 | 34.116.82.199 | |
| 34.123.151.210 | | | |
| 34.135.61.140 | | | |
| 34.121.166.52 | | | |
| 34.31.121.70 | | | |
| 136.107.81.228 | | | |
| 136.107.155.54 | | | |
| 8.228.118.112 | | | |
| 136.70.239.145 | | | |
| 8.234.246.249 | | | |
| 35.221.47.168 | | | |
| 136.90.3.18 | | | |
| 34.48.88.158 | | | |
| 136.67.157.35 | | | |
| 136.69.232.150 | | | |
| 34.45.36.249 | | | |
| 34.121.5.92 | | | |
| 34.182.176.33 | | | |

## Payload size

The maximum payload size for all requests sent to Cloud deployments is 25 MB. A request with a payload larger than 25 MB returns a `413 Payload Too Large` error.

## Deployment types

The control plane offers two deployment types: Serverless and Dedicated. Each is available in three [sizes](#sizes): Small, Medium, and Large.

> [!NOTE]
>
> `langgraph deploy` creates Serverless deployments by default. Older CLI versions use `dev` for legacy Development deployments without scale-to-zero and `prod` for Dedicated deployments. Legacy `dev` is not equivalent to Serverless; see [`langgraph deploy`](../Get%20started/Reference/LangGraph%20CLI.md#deploy).

| **Agent Server type** | **Scaling** | **Database** | **Best for** |
| - | - | - | - |
| Serverless | Scales to zero after inactivity, wakes on the next request | Shared, multi-tenant | Background and other latency-tolerant production workloads, development, and testing |
| Dedicated | Always-on, autoscales across replicas | Dedicated, with automatic backups and high availability | Latency-sensitive workloads that need always-on capacity |

> [!WARNING]
>
> **Immutable deployment type**
> LangSmith does not support changing the type of a deployment after creation. To move to another type, create a new deployment and copy data from the previous deployment with the [Agent Server API](../Get%20started/Reference/Agent%20Server%20API/Agent%20Server%20API%20reference.md), or contact [support](https://support.langchain.com) for help with the migration. The [size](#sizes) of a deployment can still be changed.

Agent Server is fault-tolerant on both deployment types; it automatically recovers from transient Redis or Postgres interruptions and retries failed background runs.

### Serverless

A Serverless deployment runs one replica that scales to zero when idle and wakes on the next request. It suits background agents, development, and testing, plus production workloads that can tolerate cold-start latency.

Set **Scale down after** to `1 hour`, `1 day`, or `1 week` (the default) at creation or in the **Scaling** dialog. Shorter windows reduce idle compute charges; longer windows reduce cold starts.

The platform checks for scheduled runs and enabled [cron jobs](../Agent%20Server/Capabilities/Use%20cron%20jobs.md) due within 10 minutes to start a scaled-down deployment ahead of time. This reduces cold-start delays but does not guarantee readiness. Requests during startup wait up to 60 seconds by default, then time out.

The replica does not scale out. Its queue worker handles up to 10 concurrent runs by default, configurable with [`N_JOBS_PER_WORKER`](Reference/Cloud%20Agent%20Server%20environment%20variables.md#n_jobs_per_worker); additional runs queue.

> [!NOTE]
>
> Scale to zero is in [beta](../../LangSmith%20setup/Cloud/Reference/Release%20stages.md) and is initially available only for deployments on usage-based pricing. See [Manage billing](../../LangSmith%20setup/Account/Billing%20%26%20usage/Manage%20billing%20in%20your%20account.md#langsmith-deployment-billing) for pricing and the transition timeline.

### Dedicated

A Dedicated deployment stays on and [autoscales](#scaling) separate API server and queue worker replicas. Each has its own database with automatic backups, point-in-time recovery, and high availability. It suits latency-sensitive workloads that need always-on capacity.

Dedicated deployments are billed separately for runtime compute and database capacity, including while idle. Autoscaling changes runtime charges, not database charges. For rates and examples, see [LangSmith Agent Server billing](../../LangSmith%20setup/Account/Billing%20%26%20usage/Manage%20billing%20in%20your%20account.md#langsmith-deployment-billing).

To request more resources, [contact support](https://support.langchain.com). Increases depend on your use case and available capacity.

## Sizes

These tables show requested vCPU and memory for billable compute on LangSmith Cloud in GCP. Redis is excluded because it is not billed on any deployment type or size; see [Compute billing](../../LangSmith%20setup/Account/Billing%20%26%20usage/Manage%20billing%20in%20your%20account.md#langsmith-deployment-billing).

A Serverless deployment runs one replica containing an API server and a queue worker, plus a separate Redis container:

| Container | Serverless S | Serverless M | Serverless L |
| - | - | - | - |
| API server | 0.4 vCPU / 1 GiB | 2 vCPU / 2 GiB | 4 vCPU / 4 GiB |
| Queue worker | 0.4 vCPU / 1 GiB | 2 vCPU / 2 GiB | 4 vCPU / 4 GiB |
| **Billable runtime total** | **0.8 vCPU / 2 GiB** | **4 vCPU / 4 GiB** | **8 vCPU / 8 GiB** |
| Database | Shared, multi-tenant | Shared, multi-tenant | Shared, multi-tenant |

A Dedicated deployment runs separate pools of API server and queue worker replicas, a single Redis container, and its own database instance:

| Container | Dedicated S | Dedicated M | Dedicated L |
| - | - | - | - |
| API server, per replica | 1 vCPU / 2 GiB | 2 vCPU / 4 GiB | 4 vCPU / 8 GiB |
| API server replicas | 2 to 10 | 2 to 20 | 2 to 40 |
| Queue worker, per replica | 1 vCPU / 2 GiB | 2 vCPU / 4 GiB | 4 vCPU / 8 GiB |
| Queue worker replicas | 1 to 10 | 1 to 20 | 1 to 40 |
| **Minimum billable runtime total** | **3 vCPU / 6 GiB** | **6 vCPU / 12 GiB** | **12 vCPU / 24 GiB** |
| Database instance | 1 vCPU / 4 GiB | 2 vCPU / 8 GiB | 4 vCPU / 16 GiB |
| Database storage | Auto-scaling disk | Auto-scaling disk | Auto-scaling disk |

Minimum billable runtime totals include 2 API server replicas and 1 queue worker. Database capacity is billed separately and is not included in these totals. [Autoscaling](#scaling) adds runtime replicas at the listed per-replica size.

On a Dedicated deployment, the compute size and the database size can be set independently from the **Scaling** dialog. A size change rolls out as a new revision and keeps the deployment's threads, checkpoints, and API URL.

For the price of each size, see the [pricing page](https://www.langchain.com/pricing), which includes a deployment cost calculator. For how Serverless and Dedicated deployments are billed, see [Manage billing](../../LangSmith%20setup/Account/Billing%20%26%20usage/Manage%20billing%20in%20your%20account.md#langsmith-deployment-billing).

### Run multiple agents on one deployment

Deployments are [billed on the resources they consume](../../LangSmith%20setup/Account/Billing%20%26%20usage/Manage%20billing%20in%20your%20account.md#langsmith-deployment-billing), not on the number of agents they serve. To run several agents on the resources of one deployment, [define multiple graphs](../Agent%20Server/Develop%20your%20application/Application%20structure.md#define-multiple-graphs-in-one-deployment) in one `langgraph.json`. This works well for Dedicated: one always-on instance with its own database can host several production agents.

All graphs in a deployment share its compute, database, autoscaling, and deployment type. They also ship together as one revision. Give an agent its own deployment when it needs a different size, latency profile, or isolation from the other agents.

## Database provisioning

The control plane and [data plane](../Get%20started/Deployment%20components/LangSmith%20data%20plane.md) listener application coordinate to automatically create a Postgres database for each Cloud deployment. The database serves as the [persistence layer](https://docs.langchain.com/oss/python/langgraph/persistence.md#memory-store) for the deployment.

When implementing a LangGraph application, a [checkpointer](https://docs.langchain.com/oss/python/langgraph/persistence.md#checkpointer-libraries) does not need to be configured. A checkpointer is automatically configured for the graph. Any checkpointer configured for a graph is replaced by the one that is automatically configured.

There is no direct access to the database. All access to the database occurs through the [Agent Server](../Agent%20Server/Capabilities/Agent%20Server.md).

The database is never deleted until the deployment itself is deleted.

For self-hosted deployments, see [custom PostgreSQL configuration](../Deploy%20to%20Self-hosted/Configure/Self-hosted%20platform%20features.md#custom-postgresql).

## Scaling

Cloud deployments autoscale automatically. You do not configure queue workers, replicas, or pool sizes directly.

[Serverless](#serverless) scales between zero and one replica.

A Dedicated deployment adds and removes replicas up to the [maximum for its size](#sizes). [API servers](../Agent%20Server/Capabilities/Agent%20Server.md#runtime-architecture) and [queue workers](../Agent%20Server/Capabilities/Agent%20Server.md#runtime-architecture) are separate pools that scale independently, so read traffic does not slow run submission and vice versa:

* **API servers** scale on CPU. The target is 50% of the CPU limit, which is twice the requested vCPU in the [sizes table](#sizes). The minimum is 2 replicas.
* **Queue workers** scale on CPU or on run backlog, whichever needs more replicas. The CPU target is the same. The backlog target counts pending and running runs at 75% of [`N_JOBS_PER_WORKER`](Reference/Cloud%20Agent%20Server%20environment%20variables.md#n_jobs_per_worker), rounded down. With the default of 10, the target is 7 runs per replica; 30 runs require 5 workers. The minimum is 1 replica.

Memory does not trigger scaling. Redis and database compute do not autoscale. To avoid rapid scaling changes, scale-down waits 15 minutes, then removes at most 10% of replicas (at least one) every 2 minutes. It pauses during revision rollouts. Replicas remain [billable](../../LangSmith%20setup/Account/Billing%20%26%20usage/Manage%20billing%20in%20your%20account.md#langsmith-deployment-billing) until they scale down.

Autoscaling changes the number of replicas, but the CPU and memory available to each replica are fixed by the deployment's [size](#sizes). If a deployment is under sustained CPU pressure, or its containers run out of memory, upgrade it to a larger size. A size change rolls out as a new revision with no downtime; the deployment type cannot be changed.

Application-level scaling levers (durability modes, async patterns, avoiding synchronous blocking, using `/join` instead of polling) apply to Cloud the same as to self-hosted. See [Scaling on self-hosted](../Deploy%20to%20Self-hosted/Configure/Configure%20Agent%20Server%20for%20scale.md) for the underlying concepts; the Helm and resource configurations there do not apply to Cloud.

## Next steps

* [Create a deployment](Deployment%20guide/Create%20an%20Agent%20Server.md): Deploy from a GitHub repository or with the `langgraph deploy` CLI.
* [Manage billing](../../LangSmith%20setup/Account/Billing%20%26%20usage/Manage%20billing%20in%20your%20account.md#langsmith-deployment-billing): See how deployment compute and databases are billed.

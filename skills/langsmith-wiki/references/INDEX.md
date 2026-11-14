# LangSmith 文档索引

本文件由 `scripts/sync_wiki_docs.py` 生成。日常问答优先运行 `scripts/search_docs.py`，需要浏览主题结构时再读取本索引。

- 来源：<https://docs.langchain.com/langsmith>
- 文档数：1259

## 顶层目录

- `Additional documentation`：1 篇
- `Build`：66 篇
- `Deploy`：196 篇
- `Engine`：11 篇
- `LangSmith setup`：152 篇
- `LLM Gateway`：20 篇
- `Monitor`：709 篇
- `No-code agents`：25 篇
- `Test`：79 篇

## 目录树

```text
docs/
├── Additional documentation
│   └── No-code agents with LangSmith Fleet.md
├── Build
│   ├── Python
│   │   ├── Deep Agents
│   │   │   └── Deployment
│   │   │       └── Managed Deep Agents.md
│   │   └── Managed Deep Agents
│   │       ├── Agent capabilities
│   │       │   ├── Channels
│   │       │   │   ├── Connect a Managed Deep Agent to a custom channel over HTTP.md
│   │       │   │   ├── Connect a Managed Deep Agent to Slack.md
│   │       │   │   ├── Connect Managed Deep Agents to channels.md
│   │       │   │   └── Prompt Slack users with agent-owned interrupts.md
│   │       │   ├── Add a sandbox to Managed Deep Agents.md
│   │       │   ├── Add custom middleware to Managed Deep Agents.md
│   │       │   ├── Add custom tools to Managed Deep Agents.md
│   │       │   ├── Add identity to Managed Deep Agents.md
│   │       │   ├── Add instructions to Managed Deep Agents.md
│   │       │   ├── Add memory to Managed Deep Agents.md
│   │       │   ├── Add schedules to Managed Deep Agents.md
│   │       │   ├── Add skills to Managed Deep Agents.md
│   │       │   ├── Browser use.md
│   │       │   ├── Connect to MCP servers.md
│   │       │   ├── Define a Managed Deep Agent.md
│   │       │   ├── Evaluate Managed Deep Agents.md
│   │       │   ├── Manage connections.md
│   │       │   ├── Managed Deep Agents runtime.md
│   │       │   ├── Subagents.md
│   │       │   └── Web search.md
│   │       ├── Build and deploy
│   │       │   ├── Add a custom search tool, memory, and a schedule.md
│   │       │   ├── Build a custom frontend for a Managed Deep Agent.md
│   │       │   ├── Connect MCP clients to a Managed Deep Agent.md
│   │       │   ├── Deploy a Managed Deep Agent.md
│   │       │   ├── Develop locally with LangSmith Studio.md
│   │       │   ├── Manage Context Hub for Managed Deep Agents.md
│   │       │   └── Managed Deep Agents CLI reference.md
│   │       ├── Get started
│   │       │   ├── Managed Deep Agents project structure.md
│   │       │   ├── Managed Deep Agents quickstart.md
│   │       │   └── Move from Deep Agents to Managed Deep Agents.md
│   │       └── Templates
│   │           ├── Deploy the open-source design agent.md
│   │           └── Deploy the open-source paid media agent.md
│   └── TypeScript
│       ├── Deep Agents
│       │   └── Deployment
│       │       └── Managed Deep Agents.md
│       └── Managed Deep Agents
│           ├── Agent capabilities
│           │   ├── Channels
│           │   │   ├── Connect a Managed Deep Agent to a custom channel over HTTP.md
│           │   │   ├── Connect a Managed Deep Agent to Slack.md
│           │   │   ├── Connect Managed Deep Agents to channels.md
│           │   │   └── Prompt Slack users with agent-owned interrupts.md
│           │   ├── Add a sandbox to Managed Deep Agents.md
│           │   ├── Add custom middleware to Managed Deep Agents.md
│           │   ├── Add custom tools to Managed Deep Agents.md
│           │   ├── Add identity to Managed Deep Agents.md
│           │   ├── Add instructions to Managed Deep Agents.md
│           │   ├── Add memory to Managed Deep Agents.md
│           │   ├── Add schedules to Managed Deep Agents.md
│           │   ├── Add skills to Managed Deep Agents.md
│           │   ├── Browser use.md
│           │   ├── Connect to MCP servers.md
│           │   ├── Define a Managed Deep Agent.md
│           │   ├── Evaluate Managed Deep Agents.md
│           │   ├── Manage connections.md
│           │   ├── Managed Deep Agents runtime.md
│           │   ├── Subagents.md
│           │   └── Web search.md
│           ├── Build and deploy
│           │   ├── Add a custom search tool, memory, and a schedule.md
│           │   ├── Build a custom frontend for a Managed Deep Agent.md
│           │   ├── Connect MCP clients to a Managed Deep Agent.md
│           │   ├── Deploy a Managed Deep Agent.md
│           │   ├── Develop locally with LangSmith Studio.md
│           │   ├── Manage Context Hub for Managed Deep Agents.md
│           │   └── Managed Deep Agents CLI reference.md
│           ├── Get started
│           │   ├── Managed Deep Agents project structure.md
│           │   ├── Managed Deep Agents quickstart.md
│           │   └── Move from Deep Agents to Managed Deep Agents.md
│           └── Templates
│               ├── Deploy the open-source design agent.md
│               └── Deploy the open-source paid media agent.md
├── Deploy
│   ├── Agent Server
│   │   ├── Auth & access control
│   │   │   ├── Custom auth tutorial
│   │   │   │   ├── Connect an authentication provider.md
│   │   │   │   ├── Isolate store data per user.md
│   │   │   │   ├── Make conversations private.md
│   │   │   │   └── Set up custom authentication.md
│   │   │   ├── Add custom authentication.md
│   │   │   ├── Authentication & access control.md
│   │   │   ├── Document API authentication in OpenAPI.md
│   │   │   └── Set up Agent Auth.md
│   │   ├── Capabilities
│   │   │   ├── Assistants
│   │   │   │   ├── Assistants.md
│   │   │   │   └── Manage assistants.md
│   │   │   ├── Double-texting
│   │   │   │   ├── Double texting.md
│   │   │   │   ├── Enqueue concurrent.md
│   │   │   │   ├── Interrupt concurrent.md
│   │   │   │   ├── Reject Concurrent.md
│   │   │   │   └── Rollback Concurrent.md
│   │   │   ├── Runs
│   │   │   │   ├── How to cancel a run.md
│   │   │   │   ├── How to kick off background runs.md
│   │   │   │   ├── How to run multiple assistants on the same thread.md
│   │   │   │   ├── Prioritize runs.md
│   │   │   │   ├── Runs.md
│   │   │   │   └── Stateless runs.md
│   │   │   ├── A2A endpoint in Agent Server.md
│   │   │   ├── Agent Server.md
│   │   │   ├── Distributed tracing with Agent Server.md
│   │   │   ├── How to interact with a deployment using RemoteGraph.md
│   │   │   ├── Human-in-the-loop over MCP.md
│   │   │   ├── Human-in-the-loop using server API.md
│   │   │   ├── MCP endpoint in Agent Server.md
│   │   │   ├── Streaming API.md
│   │   │   ├── Time travel using the server API.md
│   │   │   ├── Use cron jobs.md
│   │   │   ├── Use threads.md
│   │   │   └── Use webhooks.md
│   │   ├── Develop your application
│   │   │   ├── Persistence
│   │   │   │   ├── Configure checkpointer backend.md
│   │   │   │   ├── How to add semantic search to your agent deployment.md
│   │   │   │   └── How to add TTLs to your application.md
│   │   │   ├── Set up dependencies
│   │   │   │   ├── How to customize the Dockerfile.md
│   │   │   │   ├── How to set up a JavaScript application.md
│   │   │   │   ├── How to set up an application with pyproject.toml.md
│   │   │   │   ├── How to set up an application with requirements.txt.md
│   │   │   │   └── Monorepo support.md
│   │   │   └── Application structure.md
│   │   ├── How to build
│   │   │   ├── How to collect user feedback for Agent Server runs.md
│   │   │   ├── How to implement generative user interfaces with LangGraph.md
│   │   │   └── Implement a CI-CD pipeline using LangSmith Agent Server and Evaluation.md
│   │   ├── Server customization
│   │   │   ├── Encryption at rest
│   │   │   │   ├── Configure AES encryption at rest.md
│   │   │   │   ├── Configure custom encryption at rest.md
│   │   │   │   └── Encryption at rest.md
│   │   │   ├── Extend the HTTP server
│   │   │   │   ├── How to add custom lifespan events.md
│   │   │   │   ├── How to add custom middleware.md
│   │   │   │   └── How to add custom routes.md
│   │   │   ├── Headers and logging
│   │   │   │   ├── Include HTTP headers in server logs.md
│   │   │   │   └── Use HTTP headers for runtime configuration.md
│   │   │   ├── Replace built-in backends
│   │   │   │   ├── How to use a custom checkpointer.md
│   │   │   │   └── How to use a custom store.md
│   │   │   ├── Configure IAM authentication for data stores.md
│   │   │   ├── Rebuild graph at runtime.md
│   │   │   └── Use server-side caching.md
│   │   └── Agent Server.md
│   ├── Deploy to Cloud
│   │   ├── Deployment guide
│   │   │   ├── Create an Agent Server.md
│   │   │   ├── Manage an Agent Server.md
│   │   │   ├── Monitor an Agent Server.md
│   │   │   ├── Preview builds.md
│   │   │   └── Revisions.md
│   │   ├── Reference
│   │   │   └── Cloud Agent Server environment variables.md
│   │   ├── Cloud platform features.md
│   │   └── Deploy to Cloud.md
│   ├── Deploy to Self-hosted
│   │   ├── Configure
│   │   │   ├── Agent Server metrics.md
│   │   │   ├── Configure Agent Server for scale.md
│   │   │   ├── Self-hosted platform features.md
│   │   │   ├── Set up a build machine on a restricted network.md
│   │   │   └── Troubleshooting for self-hosted deployments.md
│   │   ├── Reference
│   │   │   └── Self-hosted Agent Server environment variables.md
│   │   ├── Deploy to self-hosted.md
│   │   ├── Deploy with control plane.md
│   │   ├── Hybrid.md
│   │   └── Self-host standalone servers.md
│   ├── Get started
│   │   ├── Deployment components
│   │   │   ├── LangSmith Agent Server components.md
│   │   │   ├── LangSmith control plane.md
│   │   │   └── LangSmith data plane.md
│   │   ├── Develop & test
│   │   │   └── Local development & testing.md
│   │   ├── Frameworks and platforms
│   │   │   ├── Full-stack web apps
│   │   │   │   ├── Deploy full-stack web apps.md
│   │   │   │   ├── Deploy with Cloudflare Workers.md
│   │   │   │   ├── Deploy with Deno Deploy.md
│   │   │   │   ├── Deploy with LangSmith and Vite.md
│   │   │   │   ├── Deploy with Next.js.md
│   │   │   │   ├── Deploy with Nuxt.md
│   │   │   │   └── Deploy with SvelteKit.md
│   │   │   ├── Deploy Google ADK agents.md
│   │   │   └── Deploy other frameworks.md
│   │   ├── Reference
│   │   │   ├── Agent Server API
│   │   │   │   ├── A2A
│   │   │   │   │   └── A2A JSON-RPC.md
│   │   │   │   ├── Assistants
│   │   │   │   │   ├── Count Assistants.md
│   │   │   │   │   ├── Create Assistant.md
│   │   │   │   │   ├── Delete Assistant.md
│   │   │   │   │   ├── Get Assistant Graph.md
│   │   │   │   │   ├── Get Assistant Schemas.md
│   │   │   │   │   ├── Get Assistant Subgraphs by Namespace.md
│   │   │   │   │   ├── Get Assistant Subgraphs.md
│   │   │   │   │   ├── Get Assistant Versions.md
│   │   │   │   │   ├── Get Assistant.md
│   │   │   │   │   ├── Patch Assistant.md
│   │   │   │   │   ├── Search Assistants.md
│   │   │   │   │   └── Set Latest Assistant Version.md
│   │   │   │   ├── Crons
│   │   │   │   │   ├── Count Crons.md
│   │   │   │   │   ├── Create Cron.md
│   │   │   │   │   ├── Create Thread Cron.md
│   │   │   │   │   ├── Delete Cron.md
│   │   │   │   │   ├── Get Cron.md
│   │   │   │   │   ├── Search Crons.md
│   │   │   │   │   └── Update Cron.md
│   │   │   │   ├── MCP
│   │   │   │   │   ├── MCP Get.md
│   │   │   │   │   ├── MCP Post.md
│   │   │   │   │   └── Terminate Session.md
│   │   │   │   ├── Stateless Runs
│   │   │   │   │   ├── Create Background Run.md
│   │   │   │   │   ├── Create Run Batch.md
│   │   │   │   │   ├── Create Run, Stream Output.md
│   │   │   │   │   └── Create Run, Wait for Output.md
│   │   │   │   ├── Store
│   │   │   │   │   ├── Delete an item.md
│   │   │   │   │   ├── List namespaces with optional match conditions.md
│   │   │   │   │   ├── Retrieve a single item.md
│   │   │   │   │   ├── Search or list items within a namespace prefix.md
│   │   │   │   │   └── Store or update an item.md
│   │   │   │   ├── Streaming
│   │   │   │   │   ├── Protocol v2 Command.md
│   │   │   │   │   └── Protocol v2 Event Stream (SSE).md
│   │   │   │   ├── System
│   │   │   │   │   ├── API Documentation.md
│   │   │   │   │   ├── Health Check.md
│   │   │   │   │   ├── Server Information.md
│   │   │   │   │   └── System Metrics.md
│   │   │   │   ├── Thread Runs
│   │   │   │   │   ├── Cancel Run.md
│   │   │   │   │   ├── Cancel Runs.md
│   │   │   │   │   ├── Create Background Run.md
│   │   │   │   │   ├── Create Run, Stream Output.md
│   │   │   │   │   ├── Create Run, Wait for Output.md
│   │   │   │   │   ├── Delete Run.md
│   │   │   │   │   ├── Get Run.md
│   │   │   │   │   ├── Join Run Stream.md
│   │   │   │   │   ├── Join Run.md
│   │   │   │   │   └── List Runs.md
│   │   │   │   ├── Threads
│   │   │   │   │   ├── Copy Thread.md
│   │   │   │   │   ├── Count Threads.md
│   │   │   │   │   ├── Create Thread.md
│   │   │   │   │   ├── Delete Thread.md
│   │   │   │   │   ├── Get Thread History Post.md
│   │   │   │   │   ├── Get Thread History.md
│   │   │   │   │   ├── Get Thread State At Checkpoint (get-thread-state-at-checkpoint-1).md
│   │   │   │   │   ├── Get Thread State At Checkpoint.md
│   │   │   │   │   ├── Get Thread State.md
│   │   │   │   │   ├── Get Thread Storage.md
│   │   │   │   │   ├── Get Thread.md
│   │   │   │   │   ├── Join Thread Stream.md
│   │   │   │   │   ├── Patch Thread.md
│   │   │   │   │   ├── Prune Threads.md
│   │   │   │   │   ├── Search Threads.md
│   │   │   │   │   └── Update Thread State.md
│   │   │   │   └── Agent Server API reference.md
│   │   │   ├── Control Plane API
│   │   │   │   └── Control plane API reference for Agent Server hosting.md
│   │   │   ├── Related
│   │   │   │   ├── @langchain-langgraph-sdk.md
│   │   │   │   └── langgraph_sdk.md
│   │   │   ├── Agent Server changelog.md
│   │   │   ├── Deployment SDK.md
│   │   │   ├── LangGraph CLI.md
│   │   │   ├── Reference.md
│   │   │   └── RemoteGraph.md
│   │   ├── Deploy your app to cloud.md
│   │   └── LangSmith Agent Server.md
│   ├── Prompt & Context Hub
│   │   ├── Context Hub
│   │   │   ├── Configure Context Hub commit webhooks.md
│   │   │   ├── Context engineering concepts.md
│   │   │   ├── Manage contexts with the SDK.md
│   │   │   └── Use the Context Hub.md
│   │   ├── Prompts
│   │   │   ├── Connect to models
│   │   │   │   ├── Connect to a compatible decision model provider.md
│   │   │   │   ├── Connect to a custom model.md
│   │   │   │   └── Connect to an OpenAI compliant model provider-proxy.md
│   │   │   ├── Create and manage prompts
│   │   │   │   ├── Configure prompt settings.md
│   │   │   │   ├── Create a prompt.md
│   │   │   │   ├── Include multimodal content in a prompt.md
│   │   │   │   ├── Manage prompts programmatically.md
│   │   │   │   ├── Manage prompts.md
│   │   │   │   ├── Prompt template format guide.md
│   │   │   │   └── Use tools in a prompt.md
│   │   │   ├── Model providers.md
│   │   │   ├── Prompt engineering concepts.md
│   │   │   ├── Prompt engineering quickstart.md
│   │   │   └── Write your prompt with AI.md
│   │   ├── Tutorials
│   │   │   ├── How to sync prompts with GitHub.md
│   │   │   ├── Optimize a classifier.md
│   │   │   └── Test multi-turn conversations.md
│   │   └── Prompt & Context Hub.md
│   └── Sandboxes
│       ├── LangSmith Sandboxes.md
│       ├── Sandbox access permissions.md
│       ├── Sandbox auth proxy.md
│       ├── Sandbox CLI.md
│       ├── Sandbox download links.md
│       ├── Sandbox mounts.md
│       ├── Sandbox SDK usage.md
│       ├── Sandbox service URLs.md
│       └── Sandbox snapshots.md
├── Engine
│   ├── Self-hosted and BYOC
│   │   ├── Configure GitHub for Engine on self-hosted and BYOC.md
│   │   ├── Configure model providers for Engine on self-hosted and BYOC.md
│   │   └── LangSmith Engine on Self-hosted and BYOC.md
│   ├── Connect Engine to your repository.md
│   ├── Find and fix your agent's issues with LangSmith Engine.md
│   ├── LangSmith Engine notifications.md
│   ├── LangSmith Engine security.md
│   ├── LangSmith Engine.md
│   ├── Proactively identify issues with Red Teaming.md
│   ├── Set up LangSmith Engine.md
│   └── Validate fixes automatically.md
├── LangSmith setup
│   ├── Account
│   │   ├── Billing & usage
│   │   │   ├── Granular billable usage.md
│   │   │   ├── Manage billing in your account.md
│   │   │   └── View usage.md
│   │   ├── Account.md
│   │   ├── Create an account and API key.md
│   │   ├── LangSmith for Enterprise.md
│   │   └── Profile configuration.md
│   ├── BYOC
│   │   ├── AWS
│   │   │   ├── AWS data plane cost estimate.md
│   │   │   ├── Bring your own IAM roles (AWS).md
│   │   │   ├── Bring your own keys (CMK).md
│   │   │   ├── Bring your own VPC on AWS.md
│   │   │   ├── BYOC architecture.md
│   │   │   ├── BYOC billing.md
│   │   │   ├── BYOC onboarding.md
│   │   │   └── BYOC operations.md
│   │   ├── Azure
│   │   │   ├── Azure data plane cost estimate.md
│   │   │   ├── BYOC architecture on Azure.md
│   │   │   ├── BYOC onboarding on Azure.md
│   │   │   └── BYOC operations on Azure.md
│   │   ├── GCP
│   │   │   ├── BYOC architecture on GCP.md
│   │   │   └── BYOC onboarding on GCP.md
│   │   ├── Bring Your Own Cloud (BYOC).md
│   │   ├── BYOC FAQ.md
│   │   ├── BYOC shared responsibility model.md
│   │   ├── BYOC usage.md
│   │   ├── Migrate to BYOC.md
│   │   └── Why BYOC.md
│   ├── Cloud
│   │   ├── Reference
│   │   │   ├── API and SDK deprecation policy.md
│   │   │   ├── LangSmith Cloud changelog.md
│   │   │   └── Release stages.md
│   │   └── Cloud (SaaS).md
│   ├── Govern
│   │   ├── Additional resources
│   │   │   └── FAQ
│   │   │       ├── Frequently asked questions.md
│   │   │       └── Regions FAQ.md
│   │   ├── Auditing
│   │   │   └── Audit logs.md
│   │   ├── Data & compliance
│   │   │   ├── Data purging for compliance.md
│   │   │   ├── Data storage and privacy.md
│   │   │   ├── LangSmith shared responsibility model.md
│   │   │   └── Scalability & resilience.md
│   │   ├── Organization
│   │   │   ├── Workspace setup
│   │   │   │   ├── How agent-based workspaces differ.md
│   │   │   │   ├── Manage model configurations.md
│   │   │   │   ├── Set up hierarchy.md
│   │   │   │   ├── Set up resource tags.md
│   │   │   │   └── Workload isolation.md
│   │   │   ├── Manage LangSmith with Terraform.md
│   │   │   ├── Manage your organization using the API.md
│   │   │   ├── Overview.md
│   │   │   ├── Relays.md
│   │   │   └── Tunnels.md
│   │   ├── Tools
│   │   │   ├── LangSmith CLI.md
│   │   │   └── LangSmith skills.md
│   │   ├── Users & access control
│   │   │   ├── Attribute-based access control.md
│   │   │   ├── Authentication methods.md
│   │   │   ├── Manage user access in SSO organizations.md
│   │   │   ├── Organization and workspace operations reference.md
│   │   │   ├── Role-based access control.md
│   │   │   ├── Teams.md
│   │   │   └── User management.md
│   │   └── Govern.md
│   ├── Overview
│   │   ├── Agent-based workspaces
│   │   │   ├── Agent environments.md
│   │   │   ├── Agent Registry.md
│   │   │   ├── Create an agent.md
│   │   │   ├── Deploy to an agent environment.md
│   │   │   └── Navigate agents.md
│   │   ├── Hosting
│   │   │   └── Set up LangSmith.md
│   │   └── LangSmith setup.md
│   └── Self-hosted
│       ├── Configure an instance
│       │   ├── Authenticate Vertex AI with GKE workload identity.md
│       │   ├── Configure environment variables in the Helm chart.md
│       │   ├── Configure LangSmith for scale.md
│       │   ├── Create an Ingress for installations (Kubernetes).md
│       │   ├── Customize the UI.md
│       │   ├── Egress for billing and operational telemetry.md
│       │   ├── Enable TTL and data retention.md
│       │   ├── FIPS-compliant images.md
│       │   ├── Mirror images for your LangSmith installation.md
│       │   ├── Set up the LLM auth proxy.md
│       │   ├── Troubleshooting.md
│       │   └── Use environment variables for model providers.md
│       ├── Connect external services
│       │   ├── Connect self-hosted and BYOC LangSmith to Slack.md
│       │   ├── Connect to an external ClickHouse database.md
│       │   ├── Connect to an external PostgreSQL database.md
│       │   ├── Connect to an external Redis or Valkey database.md
│       │   ├── Enable blob storage.md
│       │   └── LangSmith-managed ClickHouse.md
│       ├── Deploy with Terraform
│       │   ├── AWS
│       │   │   ├── AWS Terraform architecture.md
│       │   │   ├── AWS Terraform quick reference.md
│       │   │   ├── AWS Terraform troubleshooting.md
│       │   │   ├── AWS Terraform variables reference.md
│       │   │   └── Deploy LangSmith on AWS with Terraform.md
│       │   ├── Azure
│       │   │   ├── Azure Terraform architecture.md
│       │   │   ├── Azure Terraform quick reference.md
│       │   │   ├── Azure Terraform troubleshooting.md
│       │   │   ├── Azure Terraform variables reference.md
│       │   │   └── Deploy LangSmith on Azure with Terraform.md
│       │   ├── GCP
│       │   │   ├── Deploy LangSmith on GCP with Terraform.md
│       │   │   ├── GCP Terraform architecture.md
│       │   │   ├── GCP Terraform quick reference.md
│       │   │   ├── GCP Terraform troubleshooting.md
│       │   │   └── GCP Terraform variables reference.md
│       │   └── Deploy LangSmith with Terraform.md
│       ├── Get started by cloud provider
│       │   ├── Self-hosted LangSmith on AWS.md
│       │   ├── Self-hosted LangSmith on Azure.md
│       │   └── Self-hosted LangSmith on GCP.md
│       ├── Hybrid
│       │   └── Setup guide (legacy).md
│       ├── Install an instance
│       │   ├── Additional features
│       │   │   ├── Enable Sandboxes
│       │   │   │   ├── Enable Sandboxes on self-hosted LangSmith.md
│       │   │   │   ├── Operate self-hosted Sandboxes.md
│       │   │   │   ├── Route self-hosted Sandbox egress through a forward proxy.md
│       │   │   │   ├── Run self-hosted Sandboxes in a separate cluster.md
│       │   │   │   ├── Scale self-hosted Sandboxes.md
│       │   │   │   └── Self-hosted Sandbox architecture.md
│       │   │   ├── Configure additional self-hosted features.md
│       │   │   ├── Enable Agent Server hosting.md
│       │   │   ├── Enable Fleet on self-hosted LangSmith.md
│       │   │   └── Enable the LLM Gateway.md
│       │   ├── Configure Insights and Chat on self-hosted LangSmith.md
│       │   ├── Interact with your self-hosted instance of LangSmith.md
│       │   ├── Minimum versions for self-hosting dependencies.md
│       │   └── Self-host LangSmith on Kubernetes.md
│       ├── Manage an instance
│       │   ├── Disaster recovery for self-hosted LangSmith.md
│       │   ├── Upgrade an installation.md
│       │   └── View trace counts across your organization.md
│       ├── Platform auth & access control
│       │   ├── Basic authentication with email and password.md
│       │   ├── Configure custom TLS certificates.md
│       │   ├── Customize user management.md
│       │   ├── Set up SSO with OAuth2.0 and OIDC.md
│       │   └── Use an existing secret for your installation (Kubernetes).md
│       ├── Reference
│       │   ├── Release policy.md
│       │   └── Self-hosted LangSmith changelog.md
│       ├── Scripts
│       │   ├── Delete organizations.md
│       │   ├── Delete traces.md
│       │   ├── Delete workspaces.md
│       │   ├── Generate ClickHouse stats.md
│       │   ├── Generate query stats.md
│       │   ├── Run support queries against ClickHouse.md
│       │   └── Run support queries against PostgreSQL.md
│       ├── Self-hosted observability
│       │   ├── Configure your collector for LangSmith telemetry.md
│       │   ├── Deploy an observability stack for your LangSmith deployment.md
│       │   ├── Export LangSmith telemetry to your observability backend.md
│       │   ├── Install Mission Control.md
│       │   └── Monitor self-hosted LangSmith with Datadog or Grafana.md
│       ├── SmithDB
│       │   ├── Install SmithDB
│       │   │   ├── Configure SmithDB for scale.md
│       │   │   ├── Install LangSmith with SmithDB.md
│       │   │   ├── Migrate ClickHouse history to SmithDB.md
│       │   │   ├── Prepare SmithDB supporting infrastructure.md
│       │   │   └── Troubleshoot SmithDB.md
│       │   ├── Monitoring and alerting
│       │   │   ├── Common SmithDB issues to monitor.md
│       │   │   ├── Configure SmithDB observability.md
│       │   │   └── Essential SmithDB metrics.md
│       │   ├── Overview
│       │   │   ├── Enable SmithDB on self-hosted LangSmith.md
│       │   │   ├── How SmithDB handles data.md
│       │   │   └── SmithDB architecture.md
│       │   └── SmithDB feature availability.md
│       └── Self-hosted LangSmith.md
├── LLM Gateway
│   ├── Authentication
│   │   ├── Authenticate to the LLM Gateway.md
│   │   └── Provider authentication.md
│   ├── Call the gateway
│   │   ├── API formats.md
│   │   ├── Decision models.md
│   │   ├── Direct model access.md
│   │   └── Set up coding agents.md
│   ├── Get started
│   │   ├── How the LLM Gateway works.md
│   │   ├── LLM Gateway.md
│   │   ├── Send your first LLM Gateway request.md
│   │   └── Set up the LLM Gateway.md
│   ├── Governance
│   │   ├── Data policies.md
│   │   ├── Header-based policies.md
│   │   ├── Model access policies.md
│   │   ├── Rate limit policies.md
│   │   └── Spend policies.md
│   ├── Models and reliability
│   │   ├── Custom model configurations.md
│   │   ├── Gateway Credits.md
│   │   └── Model fallbacks.md
│   └── Observability
│       ├── Monitor LLM Gateway spend.md
│       └── View LLM Gateway traces.md
├── Monitor
│   ├── Debug
│   │   ├── Bulk export trace data
│   │   │   ├── Bulk export trace data.md
│   │   │   ├── Export trace data to BigQuery.md
│   │   │   ├── Import exported data.md
│   │   │   ├── Manage bulk export destinations.md
│   │   │   └── Monitor and troubleshoot bulk exports.md
│   │   ├── Data type reference
│   │   │   ├── Feedback data format.md
│   │   │   └── Run (span) data format.md
│   │   ├── Trajectory view
│   │   │   └── Trajectory view integrations.md
│   │   ├── Viewing & managing traces
│   │   │   ├── Configure run input and output preview.md
│   │   │   ├── Filter traces (ClickHouse).md
│   │   │   ├── Filter traces.md
│   │   │   ├── LangSmith MCP Server.md
│   │   │   ├── LangSmith Remote MCP.md
│   │   │   ├── Manage a trace.md
│   │   │   ├── Query threads using the SDK.md
│   │   │   ├── Query traces using the SDK.md
│   │   │   ├── Resolve an agent environment.md
│   │   │   ├── Trace query syntax.md
│   │   │   └── View traces.md
│   │   └── Configure threads.md
│   ├── Observe
│   │   ├── Automations
│   │   │   ├── Configure webhook notifications for rules.md
│   │   │   └── Set up automation rules.md
│   │   ├── Monitoring & alerting
│   │   │   ├── Alerts in LangSmith.md
│   │   │   ├── Custom Apps.md
│   │   │   ├── Discover errors and usage patterns with Insights.md
│   │   │   └── Monitor projects with dashboards.md
│   │   └── Online evaluators
│   │       ├── Set up composite online evaluators.md
│   │       ├── Set up decision model online evaluators.md
│   │       ├── Set up LangChain Tuned Evaluators.md
│   │       ├── Set up LLM-as-a-judge online evaluators.md
│   │       ├── Set up multi-turn online evaluators.md
│   │       └── Set up online code evaluators.md
│   ├── Overview
│   │   └── LangSmith Observability.md
│   ├── Reference
│   │   ├── LangSmith REST API
│   │   │   ├── Administration
│   │   │   │   ├── Add basic auth members to current org.md
│   │   │   │   ├── Add member to current org.md
│   │   │   │   ├── Add member to current workspace.md
│   │   │   │   ├── Add members to current org batch.md
│   │   │   │   ├── Add members to current workspace batch.md
│   │   │   │   ├── Attach access policies to a role (attach-access-policies-to-a-role-1).md
│   │   │   │   ├── Attach access policies to a role.md
│   │   │   │   ├── AWS marketplace fulfillment URL registration.md
│   │   │   │   ├── Bulk unshare entities.md
│   │   │   │   ├── Change payment plan.md
│   │   │   │   ├── Check SSO email verification status.md
│   │   │   │   ├── Claim pending organization invite.md
│   │   │   │   ├── Claim pending workspace invite.md
│   │   │   │   ├── Confirm SSO user email.md
│   │   │   │   ├── Create a new data plane.md
│   │   │   │   ├── Create a SCIM token.md
│   │   │   │   ├── Create an access policy.md
│   │   │   │   ├── Create customers and get stripe setup intent.md
│   │   │   │   ├── Create onboarding state.md
│   │   │   │   ├── Create org personal access token.md
│   │   │   │   ├── Create org service key.md
│   │   │   │   ├── Create org tracing key.md
│   │   │   │   ├── Create organization roles.md
│   │   │   │   ├── Create organization.md
│   │   │   │   ├── Create service account.md
│   │   │   │   ├── Create SSO settings.md
│   │   │   │   ├── Create stripe checkout sessions endpoint.md
│   │   │   │   ├── Create tag key.md
│   │   │   │   ├── Create tag value.md
│   │   │   │   ├── Create tagging.md
│   │   │   │   ├── Create tenant.md
│   │   │   │   ├── Create workspace.md
│   │   │   │   ├── Delete a data plane.md
│   │   │   │   ├── Delete a SCIM token.md
│   │   │   │   ├── Delete an access policy.md
│   │   │   │   ├── Delete API key.md
│   │   │   │   ├── Delete current org pending member.md
│   │   │   │   ├── Delete current workspace member.md
│   │   │   │   ├── Delete current workspace pending member.md
│   │   │   │   ├── Delete current workspace secret.md
│   │   │   │   ├── Delete org personal access token.md
│   │   │   │   ├── Delete org service key.md
│   │   │   │   ├── Delete org tracing key.md
│   │   │   │   ├── Delete organization roles.md
│   │   │   │   ├── Delete pending organization invite.md
│   │   │   │   ├── Delete pending workspace invite.md
│   │   │   │   ├── Delete personal access token.md
│   │   │   │   ├── Delete service account.md
│   │   │   │   ├── Delete SSO settings.md
│   │   │   │   ├── Delete tag key.md
│   │   │   │   ├── Delete tag value.md
│   │   │   │   ├── Delete tagging.md
│   │   │   │   ├── Delete usage limit.md
│   │   │   │   ├── Delete workspace.md
│   │   │   │   ├── Detach access policies from a role.md
│   │   │   │   ├── Export granular usage csv.md
│   │   │   │   ├── Generate API key.md
│   │   │   │   ├── Generate personal access token.md
│   │   │   │   ├── Get a data plane.md
│   │   │   │   ├── Get a SCIM token.md
│   │   │   │   ├── Get an access policy.md
│   │   │   │   ├── Get API keys.md
│   │   │   │   ├── Get audit logs.md
│   │   │   │   ├── Get company info.md
│   │   │   │   ├── Get current active org members.md
│   │   │   │   ├── Get current active workspace members.md
│   │   │   │   ├── Get current org members.md
│   │   │   │   ├── Get current organization info (get-current-organization-info).md
│   │   │   │   ├── Get current organization info.md
│   │   │   │   ├── Get current pending org members.md
│   │   │   │   ├── Get current pending workspace members.md
│   │   │   │   ├── Get current SSO settings.md
│   │   │   │   ├── Get current user login methods.md
│   │   │   │   ├── Get current workspace encrypted secrets.md
│   │   │   │   ├── Get current workspace members.md
│   │   │   │   ├── Get current workspace stats.md
│   │   │   │   ├── Get current workspace usage limits info.md
│   │   │   │   ├── Get dashboard.md
│   │   │   │   ├── Get granular usage.md
│   │   │   │   ├── Get ls user ID.md
│   │   │   │   ├── Get onboarding state.md
│   │   │   │   ├── Get org usage.md
│   │   │   │   ├── Get organization billing info.md
│   │   │   │   ├── Get organization info.md
│   │   │   │   ├── Get personal access tokens.md
│   │   │   │   ├── Get public auth info.md
│   │   │   │   ├── Get service accounts.md
│   │   │   │   ├── Get shared tokens.md
│   │   │   │   ├── Get SSO settings.md
│   │   │   │   ├── Get tag key.md
│   │   │   │   ├── Get tag value.md
│   │   │   │   ├── Get the authenticated user's provider user ID.md
│   │   │   │   ├── Get workspace TTL settings.md
│   │   │   │   ├── Get workspace.md
│   │   │   │   ├── List access policies.md
│   │   │   │   ├── List all org personal access tokens.md
│   │   │   │   ├── List audit log operations.md
│   │   │   │   ├── List current workspace secrets.md
│   │   │   │   ├── List data planes for the current organization.md
│   │   │   │   ├── List org members with workspace roles.md
│   │   │   │   ├── List org personal access tokens.md
│   │   │   │   ├── List org service keys.md
│   │   │   │   ├── List org tracing keys.md
│   │   │   │   ├── List org usage limits.md
│   │   │   │   ├── List organization roles.md
│   │   │   │   ├── List organizations.md
│   │   │   │   ├── List pending organization invites.md
│   │   │   │   ├── List pending workspace invites.md
│   │   │   │   ├── List permissions.md
│   │   │   │   ├── List SCIM tokens.md
│   │   │   │   ├── List tag keys.md
│   │   │   │   ├── List tag values.md
│   │   │   │   ├── List taggings.md
│   │   │   │   ├── List tags for resource.md
│   │   │   │   ├── List tags for resources.md
│   │   │   │   ├── List tags.md
│   │   │   │   ├── List tenants.md
│   │   │   │   ├── List TTL settings (list-ttl-settings).md
│   │   │   │   ├── List TTL settings.md
│   │   │   │   ├── List usage limits.md
│   │   │   │   ├── List workspaces.md
│   │   │   │   ├── Login.md
│   │   │   │   ├── Lookup SSO by email.md
│   │   │   │   ├── On payment method created.md
│   │   │   │   ├── Patch current org pending member.md
│   │   │   │   ├── Patch current workspace member.md
│   │   │   │   ├── Patch current workspace pending member.md
│   │   │   │   ├── Patch workspace.md
│   │   │   │   ├── Put current workspace secret.md
│   │   │   │   ├── Reinstate org personal access token.md
│   │   │   │   ├── Remove member from current org.md
│   │   │   │   ├── Revoke org personal access token.md
│   │   │   │   ├── Send SSO email confirmation.md
│   │   │   │   ├── Set company info.md
│   │   │   │   ├── Set default SSO provision.md
│   │   │   │   ├── Set role restriction.md
│   │   │   │   ├── Update a SCIM token.md
│   │   │   │   ├── Update allowed login methods.md
│   │   │   │   ├── Update an access policy.md
│   │   │   │   ├── Update current org member.md
│   │   │   │   ├── Update current organization info.md
│   │   │   │   ├── Update current user.md
│   │   │   │   ├── Update data plane settings.md
│   │   │   │   ├── Update onboarding state field.md
│   │   │   │   ├── Update org service key.md
│   │   │   │   ├── Update organization roles.md
│   │   │   │   ├── Update SSO settings.md
│   │   │   │   ├── Update tag key.md
│   │   │   │   ├── Update tag value.md
│   │   │   │   ├── Update workspace TTL settings.md
│   │   │   │   ├── Upsert current workspace secrets.md
│   │   │   │   ├── Upsert TTL settings (upsert-ttl-settings).md
│   │   │   │   ├── Upsert TTL settings.md
│   │   │   │   └── Upsert usage limit.md
│   │   │   ├── Datasets
│   │   │   │   ├── Clone dataset.md
│   │   │   │   ├── Count examples.md
│   │   │   │   ├── Create comparative experiment.md
│   │   │   │   ├── Create dataset.md
│   │   │   │   ├── Create example.md
│   │   │   │   ├── Create examples.md
│   │   │   │   ├── Delete an example.md
│   │   │   │   ├── Delete comparative experiment.md
│   │   │   │   ├── Delete dataset.md
│   │   │   │   ├── Delete datasets.md
│   │   │   │   ├── Delete example.md
│   │   │   │   ├── Delete examples.md
│   │   │   │   ├── Diff dataset versions.md
│   │   │   │   ├── Download dataset csv.md
│   │   │   │   ├── Download dataset jsonl.md
│   │   │   │   ├── Download dataset openai ft.md
│   │   │   │   ├── Download dataset openai.md
│   │   │   │   ├── Fetch experiment runs for dataset examples.md
│   │   │   │   ├── Fetch shared experiment runs for dataset examples.md
│   │   │   │   ├── Generate.md
│   │   │   │   ├── Get dataset splits.md
│   │   │   │   ├── Get dataset version.md
│   │   │   │   ├── Get dataset versions.md
│   │   │   │   ├── Hard delete examples.md
│   │   │   │   ├── Legacy update examples.md
│   │   │   │   ├── Read dataset share state.md
│   │   │   │   ├── Read dataset.md
│   │   │   │   ├── Read datasets stream.md
│   │   │   │   ├── Read datasets.md
│   │   │   │   ├── Read example.md
│   │   │   │   ├── Read examples with runs.md
│   │   │   │   ├── Read examples.md
│   │   │   │   ├── Share dataset.md
│   │   │   │   ├── Studio experiment.md
│   │   │   │   ├── Unshare dataset.md
│   │   │   │   ├── Update dataset splits.md
│   │   │   │   ├── Update dataset version.md
│   │   │   │   ├── Update dataset.md
│   │   │   │   ├── Update example.md
│   │   │   │   ├── Update examples.md
│   │   │   │   ├── Upload csv dataset.md
│   │   │   │   ├── Upload examples from csv.md
│   │   │   │   ├── Upload examples.md
│   │   │   │   ├── Upload experiment.md
│   │   │   │   ├── Validate example.md
│   │   │   │   └── Validate examples.md
│   │   │   ├── Evaluation
│   │   │   │   ├── Bulk delete evaluators.md
│   │   │   │   ├── Create evaluator.md
│   │   │   │   ├── Create new experiment view override configuration for a dataset.md
│   │   │   │   ├── Delete evaluator.md
│   │   │   │   ├── Delete experiment view override configuration.md
│   │   │   │   ├── Evaluate experiment adhoc.md
│   │   │   │   ├── Get evaluator spend.md
│   │   │   │   ├── Get evaluator.md
│   │   │   │   ├── Get experiment view override configuration by specific ID.md
│   │   │   │   ├── Get experiment view override configurations for a dataset.md
│   │   │   │   ├── List evaluators.md
│   │   │   │   ├── Update evaluator.md
│   │   │   │   └── Update existing experiment view override configuration.md
│   │   │   ├── Feedback & Annotation
│   │   │   │   ├── Add a reviewer to an annotation queue.md
│   │   │   │   ├── Add annotation queue items.md
│   │   │   │   ├── Add runs to annotation queue by key.md
│   │   │   │   ├── Add runs to annotation queue.md
│   │   │   │   ├── Create annotation queue item status.md
│   │   │   │   ├── Create annotation queue.md
│   │   │   │   ├── Create feedback config endpoint.md
│   │   │   │   ├── Create feedback formula ep.md
│   │   │   │   ├── Create feedback ingest token.md
│   │   │   │   ├── Create feedback with token get.md
│   │   │   │   ├── Create feedback with token post.md
│   │   │   │   ├── Create feedback.md
│   │   │   │   ├── Create identity annotation queue run status.md
│   │   │   │   ├── Delete annotation queue items.md
│   │   │   │   ├── Delete annotation queue.md
│   │   │   │   ├── Delete annotation queues.md
│   │   │   │   ├── Delete feedback config endpoint.md
│   │   │   │   ├── Delete feedback formula endpoint.md
│   │   │   │   ├── Delete feedback.md
│   │   │   │   ├── Delete run from annotation queue.md
│   │   │   │   ├── Delete runs from annotation queue.md
│   │   │   │   ├── Export annotation queue archived runs.md
│   │   │   │   ├── Get annotation queue item placement.md
│   │   │   │   ├── Get annotation queue.md
│   │   │   │   ├── Get annotation queues for run.md
│   │   │   │   ├── Get annotation queues.md
│   │   │   │   ├── Get feedback formula ep.md
│   │   │   │   ├── Get run from annotation queue.md
│   │   │   │   ├── Get runs from annotation queue.md
│   │   │   │   ├── Get size from annotation queue.md
│   │   │   │   ├── Get the annotation queue item count.md
│   │   │   │   ├── Get total archived from annotation queue.md
│   │   │   │   ├── Get total size from annotation queue.md
│   │   │   │   ├── List annotation queue items.md
│   │   │   │   ├── List feedback configs endpoint.md
│   │   │   │   ├── List feedback formula ep.md
│   │   │   │   ├── List feedback ingest tokens.md
│   │   │   │   ├── Populate annotation queue.md
│   │   │   │   ├── Read feedback.md
│   │   │   │   ├── Read feedbacks.md
│   │   │   │   ├── Remove a reviewer from an annotation queue.md
│   │   │   │   ├── Resolve annotation queue run.md
│   │   │   │   ├── Update an annotation queue item.md
│   │   │   │   ├── Update annotation queue.md
│   │   │   │   ├── Update feedback config endpoint.md
│   │   │   │   ├── Update feedback formula ep.md
│   │   │   │   ├── Update feedback.md
│   │   │   │   └── Update run in annotation queue.md
│   │   │   ├── Integrations & Tools
│   │   │   │   ├── Approve OAuth2 authorization request.md
│   │   │   │   ├── Authorize a device code.md
│   │   │   │   ├── Create a tool.md
│   │   │   │   ├── Create an oauth client.md
│   │   │   │   ├── Create vendor settings.md
│   │   │   │   ├── Delete a tool by handle.md
│   │   │   │   ├── Delete a tool by ID.md
│   │   │   │   ├── Delete an oauth client.md
│   │   │   │   ├── Delete vendor settings.md
│   │   │   │   ├── Exchange grant for OAuth2 tokens.md
│   │   │   │   ├── Get a tool by handle.md
│   │   │   │   ├── Get a tool by ID.md
│   │   │   │   ├── Get agent builder integrations settings.md
│   │   │   │   ├── Get an oauth client.md
│   │   │   │   ├── Get MCP vendor.md
│   │   │   │   ├── Get OAuth2 authorization server metadata.md
│   │   │   │   ├── Get openid connect provider configuration.md
│   │   │   │   ├── Get openid connect userinfo.md
│   │   │   │   ├── Get public OAuth2 client metadata.md
│   │   │   │   ├── Get tools.md
│   │   │   │   ├── Get vendor account.md
│   │   │   │   ├── Get vendor settings.md
│   │   │   │   ├── Initiate OAuth2 authorization.md
│   │   │   │   ├── Invalidate tools cache.md
│   │   │   │   ├── List authorized applications.md
│   │   │   │   ├── List MCP servers for a vendor.md
│   │   │   │   ├── List MCP vendors.md
│   │   │   │   ├── List oauth clients.md
│   │   │   │   ├── List tools for a vendor.md
│   │   │   │   ├── List tools.md
│   │   │   │   ├── Proxy get.md
│   │   │   │   ├── Proxy.md
│   │   │   │   ├── Register an OAuth2 dynamic client.md
│   │   │   │   ├── Replace vendor settings.md
│   │   │   │   ├── Request OAuth2 device authorization.md
│   │   │   │   ├── Revoke an authorized application.md
│   │   │   │   ├── Revoke an OAuth2 token.md
│   │   │   │   ├── Rotate an oauth client secret.md
│   │   │   │   ├── Update a tool by handle.md
│   │   │   │   ├── Update a tool by ID.md
│   │   │   │   ├── Update agent builder integrations settings.md
│   │   │   │   └── Update an oauth client.md
│   │   │   ├── Issues
│   │   │   │   ├── Create the issues agent for a session (Beta).md
│   │   │   │   ├── Delete the issues agent for a session (Beta).md
│   │   │   │   ├── Get issue (Beta).md
│   │   │   │   ├── Get the issues agent config for a session (Beta).md
│   │   │   │   ├── List issues (Beta).md
│   │   │   │   ├── List issues agent configs (Beta).md
│   │   │   │   ├── List viewed issues for a session (Beta).md
│   │   │   │   ├── Mark issue viewed (Beta).md
│   │   │   │   ├── Roll an issues agent webhook signing secret.md
│   │   │   │   ├── Save the agent overview for a session (Beta).md
│   │   │   │   └── Update the issues agent config for a session (Beta).md
│   │   │   ├── LLM Gateway
│   │   │   │   ├── Create a gateway policy.md
│   │   │   │   ├── Delete a gateway policy.md
│   │   │   │   ├── Get a gateway policy.md
│   │   │   │   ├── List gateway policies.md
│   │   │   │   ├── Search gateway policies by subject value set.md
│   │   │   │   └── Update a gateway policy.md
│   │   │   ├── Monitoring
│   │   │   │   ├── Cancel bulk export.md
│   │   │   │   ├── Clone section.md
│   │   │   │   ├── Create an alert rule.md
│   │   │   │   ├── Create bulk export destination.md
│   │   │   │   ├── Create bulk export.md
│   │   │   │   ├── Create chart.md
│   │   │   │   ├── Create section.md
│   │   │   │   ├── Delete an alert rule.md
│   │   │   │   ├── Delete bulk export destination.md
│   │   │   │   ├── Delete chart.md
│   │   │   │   ├── Delete section.md
│   │   │   │   ├── Get an alert rule.md
│   │   │   │   ├── Get bulk export destination.md
│   │   │   │   ├── Get bulk export destinations.md
│   │   │   │   ├── Get bulk export run.md
│   │   │   │   ├── Get bulk export runs filtered.md
│   │   │   │   ├── Get bulk export runs.md
│   │   │   │   ├── Get bulk export.md
│   │   │   │   ├── Get bulk exports.md
│   │   │   │   ├── Org create chart.md
│   │   │   │   ├── Org create section.md
│   │   │   │   ├── Org delete chart.md
│   │   │   │   ├── Org delete section.md
│   │   │   │   ├── Org read chart preview.md
│   │   │   │   ├── Org read charts.md
│   │   │   │   ├── Org read sections.md
│   │   │   │   ├── Org read single chart.md
│   │   │   │   ├── Org read single section.md
│   │   │   │   ├── Org update chart.md
│   │   │   │   ├── Org update section.md
│   │   │   │   ├── Read chart preview.md
│   │   │   │   ├── Read charts.md
│   │   │   │   ├── Read sections.md
│   │   │   │   ├── Read single chart.md
│   │   │   │   ├── Read single section.md
│   │   │   │   ├── Test an alert action to determine if configuration is valid.md
│   │   │   │   ├── Update an alert rule.md
│   │   │   │   ├── Update bulk export destination.md
│   │   │   │   ├── Update chart.md
│   │   │   │   └── Update section.md
│   │   │   ├── Prompt Hub
│   │   │   │   ├── Add repo owner.md
│   │   │   │   ├── Create comment.md
│   │   │   │   ├── Create job.md
│   │   │   │   ├── Create log.md
│   │   │   │   ├── Create repo.md
│   │   │   │   ├── Create sub comment.md
│   │   │   │   ├── Create tag.md
│   │   │   │   ├── Delete job.md
│   │   │   │   ├── Delete log.md
│   │   │   │   ├── Delete repo.md
│   │   │   │   ├── Delete repos.md
│   │   │   │   ├── Delete tag.md
│   │   │   │   ├── Fork repo.md
│   │   │   │   ├── Get comments.md
│   │   │   │   ├── Get job.md
│   │   │   │   ├── Get log.md
│   │   │   │   ├── Get repo.md
│   │   │   │   ├── Get settings.md
│   │   │   │   ├── Get sub comments.md
│   │   │   │   ├── Get tag.md
│   │   │   │   ├── Get tags.md
│   │   │   │   ├── Like comment.md
│   │   │   │   ├── Like repo.md
│   │   │   │   ├── List job logs.md
│   │   │   │   ├── List jobs.md
│   │   │   │   ├── List repo owners.md
│   │   │   │   ├── List repo tags.md
│   │   │   │   ├── List repos.md
│   │   │   │   ├── Optimize prompt job.md
│   │   │   │   ├── Remove repo owner.md
│   │   │   │   ├── Set tenant handle.md
│   │   │   │   ├── Unlike comment.md
│   │   │   │   ├── Update job.md
│   │   │   │   ├── Update repo.md
│   │   │   │   └── Update tag.md
│   │   │   ├── Prompts & Playground
│   │   │   │   ├── Create a commit.md
│   │   │   │   ├── Create directory commit.md
│   │   │   │   ├── Create hub environments model.md
│   │   │   │   ├── Create playground settings.md
│   │   │   │   ├── Create prompt webhook.md
│   │   │   │   ├── Delete directory repository.md
│   │   │   │   ├── Delete hub environments model.md
│   │   │   │   ├── Delete playground settings.md
│   │   │   │   ├── Delete prompt webhook.md
│   │   │   │   ├── Get a commit.md
│   │   │   │   ├── Get directory contents.md
│   │   │   │   ├── Get playground settings.md
│   │   │   │   ├── Get prompt webhook.md
│   │   │   │   ├── Get tag transition history.md
│   │   │   │   ├── Invoke prompt.md
│   │   │   │   ├── List commits.md
│   │   │   │   ├── List hub environments.md
│   │   │   │   ├── List playground settings.md
│   │   │   │   ├── List prompt webhooks.md
│   │   │   │   ├── Test prompt webhook.md
│   │   │   │   ├── Update hub environments model.md
│   │   │   │   ├── Update playground settings.md
│   │   │   │   └── Update prompt webhook.md
│   │   │   ├── Sandboxes
│   │   │   │   ├── Attach a sandbox to a browser (Beta).md
│   │   │   │   ├── Batch delete sandboxes.md
│   │   │   │   ├── Capture a snapshot from a sandbox.md
│   │   │   │   ├── Clone a volume (Beta).md
│   │   │   │   ├── Close a tab in a browser window (Beta).md
│   │   │   │   ├── Create a browser (Beta).md
│   │   │   │   ├── Create a registry.md
│   │   │   │   ├── Create a sandbox.md
│   │   │   │   ├── Create a snapshot.md
│   │   │   │   ├── Create a volume (Beta).md
│   │   │   │   ├── Create links to a browser window (Beta).md
│   │   │   │   ├── Delete a registry.md
│   │   │   │   ├── Delete a sandbox.md
│   │   │   │   ├── Delete a snapshot.md
│   │   │   │   ├── Delete a volume (Beta).md
│   │   │   │   ├── Detach a sandbox from a browser (Beta).md
│   │   │   │   ├── Download a sandbox file (download-a-sandbox-file-1).md
│   │   │   │   ├── Download a sandbox file.md
│   │   │   │   ├── Execute a sandbox command over WebSocket.md
│   │   │   │   ├── Execute a sandbox command.md
│   │   │   │   ├── Generate a sandbox file download link.md
│   │   │   │   ├── Generate a service access token.md
│   │   │   │   ├── Get a browser (Beta).md
│   │   │   │   ├── Get a registry.md
│   │   │   │   ├── Get a sandbox.md
│   │   │   │   ├── Get a snapshot name.md
│   │   │   │   ├── Get a snapshot.md
│   │   │   │   ├── Get a volume (Beta).md
│   │   │   │   ├── Get sandbox resource usage.md
│   │   │   │   ├── Get sandbox status.md
│   │   │   │   ├── Glob a sandbox filesystem.md
│   │   │   │   ├── Grep a sandbox filesystem.md
│   │   │   │   ├── List a sandbox's shared service urls.md
│   │   │   │   ├── List hourly sandbox usage costs.md
│   │   │   │   ├── List registries.md
│   │   │   │   ├── List sandboxes.md
│   │   │   │   ├── List snapshots.md
│   │   │   │   ├── List volumes (Beta).md
│   │   │   │   ├── Load a browser's extensions (Beta).md
│   │   │   │   ├── Open a sandbox TCP tunnel.md
│   │   │   │   ├── Open a tab in a browser window (Beta).md
│   │   │   │   ├── Resize a browser window (Beta).md
│   │   │   │   ├── Resume a streamed sandbox command.md
│   │   │   │   ├── Set who controls a browser window (Beta).md
│   │   │   │   ├── Start a sandbox.md
│   │   │   │   ├── Start a streamed sandbox command.md
│   │   │   │   ├── Stop a sandbox.md
│   │   │   │   ├── Stop sharing a sandbox service URL.md
│   │   │   │   ├── Update a registry.md
│   │   │   │   ├── Update a sandbox.md
│   │   │   │   ├── Update a volume (Beta).md
│   │   │   │   └── Upload a sandbox file.md
│   │   │   ├── System
│   │   │   │   ├── Count shared examples.md
│   │   │   │   ├── Create a model price.md
│   │   │   │   ├── Delete a model price.md
│   │   │   │   ├── Delete default model for a feature.md
│   │   │   │   ├── Disable a model for a feature.md
│   │   │   │   ├── Execute.md
│   │   │   │   ├── Generate query for shared dataset runs.md
│   │   │   │   ├── Get health info.md
│   │   │   │   ├── Get message JSON schema.md
│   │   │   │   ├── Get server info.md
│   │   │   │   ├── Get shared run by ID.md
│   │   │   │   ├── Get shared run.md
│   │   │   │   ├── Get tool def JSON schema.md
│   │   │   │   ├── List feature configurations.md
│   │   │   │   ├── List model prices.md
│   │   │   │   ├── Query shared dataset runs.md
│   │   │   │   ├── Query shared runs.md
│   │   │   │   ├── Re-enable a disabled model for a feature.md
│   │   │   │   ├── Read shared comparative experiments.md
│   │   │   │   ├── Read shared dataset feedback.md
│   │   │   │   ├── Read shared dataset run.md
│   │   │   │   ├── Read shared dataset tracer sessions bulk.md
│   │   │   │   ├── Read shared dataset tracer sessions.md
│   │   │   │   ├── Read shared dataset.md
│   │   │   │   ├── Read shared examples.md
│   │   │   │   ├── Read shared feedbacks.md
│   │   │   │   ├── Replace a model price.md
│   │   │   │   ├── Restart a backfill job.md
│   │   │   │   ├── Set default model for a feature.md
│   │   │   │   └── Stats shared dataset runs.md
│   │   │   ├── teams
│   │   │   │   ├── Add members to a team.md
│   │   │   │   ├── Attach an access policy to a team.md
│   │   │   │   ├── Change a team's role in a workspace.md
│   │   │   │   ├── Create a team.md
│   │   │   │   ├── Delete a team.md
│   │   │   │   ├── Detach an access policy from a team.md
│   │   │   │   ├── Get a team's role in a workspace.md
│   │   │   │   ├── Get a team.md
│   │   │   │   ├── Grant a team a role in a workspace.md
│   │   │   │   ├── List a team's access policies.md
│   │   │   │   ├── List a team's workspace grants.md
│   │   │   │   ├── List organization teams.md
│   │   │   │   ├── List team members.md
│   │   │   │   ├── List workspace scoped team members.md
│   │   │   │   ├── Remove a member from a team.md
│   │   │   │   ├── Remove a team's access to a workspace.md
│   │   │   │   └── Update a team.md
│   │   │   ├── Threads
│   │   │   │   ├── Get a public shared thread's manifest.md
│   │   │   │   ├── Get one run in a public shared thread.md
│   │   │   │   ├── Get stats for a public shared thread.md
│   │   │   │   ├── List runs of one trace in a public shared thread.md
│   │   │   │   ├── List traces in a public shared thread.md
│   │   │   │   ├── Query single thread stats.md
│   │   │   │   ├── Query thread stats.md
│   │   │   │   ├── Query thread traces.md
│   │   │   │   ├── Query threads.md
│   │   │   │   ├── Read a thread's share state.md
│   │   │   │   ├── Share a thread.md
│   │   │   │   ├── Stream messages for a public shared thread.md
│   │   │   │   └── Unshare a thread.md
│   │   │   ├── Tracing
│   │   │   │   ├── Auto-generate insights job config (Beta).md
│   │   │   │   ├── Create a run.md
│   │   │   │   ├── Create decision model rule.md
│   │   │   │   ├── Create filter view.md
│   │   │   │   ├── Create insights job (Beta).md
│   │   │   │   ├── Create insights job config (Beta).md
│   │   │   │   ├── Create rule.md
│   │   │   │   ├── Create tracer session.md
│   │   │   │   ├── Delete filter view.md
│   │   │   │   ├── Delete insights job (Beta).md
│   │   │   │   ├── Delete insights job config (Beta).md
│   │   │   │   ├── Delete rule.md
│   │   │   │   ├── Delete runs abac.md
│   │   │   │   ├── Delete runs.md
│   │   │   │   ├── Delete tracer session.md
│   │   │   │   ├── Delete tracer sessions.md
│   │   │   │   ├── Generate query for runs.md
│   │   │   │   ├── Get a public shared trace run.md
│   │   │   │   ├── Get a single run.md
│   │   │   │   ├── Get insights job (Beta).md
│   │   │   │   ├── Get insights job configs (Beta).md
│   │   │   │   ├── Get insights jobs (Beta).md
│   │   │   │   ├── Get last applied rule.md
│   │   │   │   ├── Get run cluster from insights job (Beta).md
│   │   │   │   ├── Get runs from insights job (Beta).md
│   │   │   │   ├── Get the LangSmith UI URL for a run.md
│   │   │   │   ├── Get tracing project prebuilt dashboard.md
│   │   │   │   ├── Group runs.md
│   │   │   │   ├── Ingest runs (batch json).md
│   │   │   │   ├── Ingest runs (multipart).md
│   │   │   │   ├── List agent versions for a project.md
│   │   │   │   ├── List rule logs (v2).md
│   │   │   │   ├── List rule logs.md
│   │   │   │   ├── List rules.md
│   │   │   │   ├── List runs in a trace.md
│   │   │   │   ├── Query public shared trace runs.md
│   │   │   │   ├── Query runs (query-runs).md
│   │   │   │   ├── Query runs.md
│   │   │   │   ├── Query traces.md
│   │   │   │   ├── Read filter view.md
│   │   │   │   ├── Read filter views.md
│   │   │   │   ├── Read run share state.md
│   │   │   │   ├── Read run.md
│   │   │   │   ├── Read tracer session.md
│   │   │   │   ├── Read tracer sessions runs metadata.md
│   │   │   │   ├── Read tracer sessions.md
│   │   │   │   ├── Rename filter view.md
│   │   │   │   ├── Resolve an address to its tracing project.md
│   │   │   │   ├── Share a run.md
│   │   │   │   ├── Share run.md
│   │   │   │   ├── Stats group runs.md
│   │   │   │   ├── Stats runs.md
│   │   │   │   ├── Thread preview.md
│   │   │   │   ├── Trigger rule.md
│   │   │   │   ├── Trigger rules.md
│   │   │   │   ├── Unshare a run.md
│   │   │   │   ├── Unshare run.md
│   │   │   │   ├── Update a run.md
│   │   │   │   ├── Update filter view.md
│   │   │   │   ├── Update insights job (Beta).md
│   │   │   │   ├── Update insights job config (Beta).md
│   │   │   │   ├── Update rule.md
│   │   │   │   ├── Update tracer session.md
│   │   │   │   ├── Validate rule.md
│   │   │   │   └── Validate runs query.md
│   │   │   └── LangSmith API reference.md
│   │   ├── SmithDB API migration
│   │   │   ├── Migrate dataset experiment runs to SmithDB.md
│   │   │   ├── Migrate feedback and sharing methods to SmithDB.md
│   │   │   ├── Migrate run queries to SmithDB.md
│   │   │   ├── Migrate run retrieval to SmithDB.md
│   │   │   ├── Migrate thread methods to SmithDB.md
│   │   │   ├── Migrate to SmithDB-backed APIs.md
│   │   │   └── Migrate trace methods to SmithDB.md
│   │   ├── langsmith (smith-java-sdk).md
│   │   ├── langsmith (smith-js-ts-sdk).md
│   │   ├── langsmith (smith-python-sdk).md
│   │   ├── LangSmith reference.md
│   │   └── langsmith.md
│   └── Trace
│       ├── Configuration & troubleshooting
│       │   ├── Advanced tracing techniques
│       │   │   ├── Access the current run (span) within a traced function.md
│       │   │   ├── Implement distributed tracing.md
│       │   │   ├── Log multimodal traces.md
│       │   │   ├── Trace generator functions.md
│       │   │   └── Trace JS functions in serverless environments.md
│       │   ├── Agent & environment settings
│       │   │   ├── Conditional tracing.md
│       │   │   ├── Log traces to an agent.md
│       │   │   ├── Set a sampling rate for traces.md
│       │   │   ├── Trace without setting environment variables.md
│       │   │   └── Write traces to multiple destinations with replicas.md
│       │   ├── Data & privacy
│       │   │   ├── Add metadata and tags to traces.md
│       │   │   ├── Prevent logging of sensitive data in traces.md
│       │   │   ├── Redact secrets from traces.md
│       │   │   └── Redact sensitive data with the OpenTelemetry Gateway architecture.md
│       │   ├── Troubleshooting guides
│       │   │   ├── Troubleshoot trace nesting.md
│       │   │   └── Troubleshoot variable caching.md
│       │   ├── Cost tracking.md
│       │   └── Usage and billing.md
│       ├── Tracing setup
│       │   ├── Integrations
│       │   │   ├── Agent frameworks
│       │   │   │   ├── Trace AutoGen agents.md
│       │   │   │   ├── Trace Claude Managed Agents.md
│       │   │   │   ├── Trace CrewAI agents.md
│       │   │   │   ├── Trace Deep Agents.md
│       │   │   │   ├── Trace Google ADK agents.md
│       │   │   │   ├── Trace LangChain agents (Python and JS-TS).md
│       │   │   │   ├── Trace LangGraph agents.md
│       │   │   │   ├── Trace Mastra agents.md
│       │   │   │   ├── Trace PydanticAI agents.md
│       │   │   │   ├── Trace Semantic Kernel agents.md
│       │   │   │   ├── Trace Vercel AI SDK agents (JS-TS only).md
│       │   │   │   ├── Trace with Microsoft Agent Framework.md
│       │   │   │   ├── Trace with OpenTelemetry.md
│       │   │   │   ├── Trace with Strands Agents.md
│       │   │   │   ├── Trace with the Claude Agent SDK.md
│       │   │   │   └── Trace with the OpenAI Agents SDK.md
│       │   │   ├── Developer tools
│       │   │   │   ├── Coding agent metadata contract.md
│       │   │   │   ├── Trace Claude Code sessions.md
│       │   │   │   ├── Trace Cursor sessions.md
│       │   │   │   ├── Trace n8n workflows.md
│       │   │   │   ├── Trace OpenAI Codex sessions.md
│       │   │   │   ├── Trace OpenCode sessions.md
│       │   │   │   ├── Trace Pi coding agent sessions.md
│       │   │   │   ├── Trace Visual Studio Code Copilot Chat sessions.md
│       │   │   │   ├── Trace with Instructor.md
│       │   │   │   └── Trace with Temporal.md
│       │   │   ├── LLM providers
│       │   │   │   ├── Trace OpenAI-compatible providers.md
│       │   │   │   ├── Trace with Amazon Bedrock.md
│       │   │   │   ├── Trace with Anthropic.md
│       │   │   │   ├── Trace with DeepSeek.md
│       │   │   │   ├── Trace with Google Gemini.md
│       │   │   │   ├── Trace with LiteLLM.md
│       │   │   │   ├── Trace with Mistral.md
│       │   │   │   └── Trace with OpenAI.md
│       │   │   ├── Productivity
│       │   │   │   └── Trace Claude Cowork sessions.md
│       │   │   ├── Voice AI frameworks
│       │   │   │   ├── Trace Gemini Live agents.md
│       │   │   │   ├── Trace LiveKit agents.md
│       │   │   │   ├── Trace OpenAI Realtime agents.md
│       │   │   │   ├── Trace Pipecat agents.md
│       │   │   │   └── Voice tracing fundamentals.md
│       │   │   └── Integrations.md
│       │   └── Manual instrumentation
│       │       ├── Custom instrumentation.md
│       │       ├── Log LLM calls.md
│       │       ├── Log retriever traces.md
│       │       ├── Metadata parameters reference.md
│       │       ├── Trace with API.md
│       │       └── Upload files with traces.md
│       ├── Observability concepts.md
│       ├── Trace an agent.md
│       └── Tracing quickstart.md
├── No-code agents
│   ├── Fleet
│   │   ├── Additional resources
│   │   │   ├── Access & oversight.md
│   │   │   └── LangSmith Fleet changelog.md
│   │   ├── Advanced
│   │   │   ├── Auth-aware tool responses.md
│   │   │   ├── Fleet webhooks.md
│   │   │   ├── LangSmith Tool Server.md
│   │   │   └── Use Fleet agents in code.md
│   │   ├── Configure
│   │   │   ├── Agent identity.md
│   │   │   ├── Computer use.md
│   │   │   ├── Manage agent settings.md
│   │   │   └── Manage workspace administration.md
│   │   ├── Get started
│   │   │   ├── Agent platform comparison.md
│   │   │   ├── Essentials.md
│   │   │   ├── Quickstart.md
│   │   │   └── Templates.md
│   │   ├── Tools and automation
│   │   │   ├── Arcade integration.md
│   │   │   ├── Channels.md
│   │   │   ├── Integrate Microsoft Teams with an agent.md
│   │   │   ├── Integrate Slack with an agent.md
│   │   │   ├── Remote MCP servers.md
│   │   │   ├── Salesforce integration.md
│   │   │   ├── Schedules.md
│   │   │   ├── Skills.md
│   │   │   └── Tool integrations.md
│   │   └── No-code agents with LangSmith Fleet.md
│   └── Studio
│       └── Build an agent with LangSmith Studio.md
└── Test
    ├── Annotation Queues
    │   ├── Feedback
    │   │   ├── Collect feedback with presigned URLs.md
    │   │   └── Log user feedback using the SDK.md
    │   ├── Annotate traces and runs inline.md
    │   ├── Build custom views for annotation queues.md
    │   ├── Manage feedback & annotation queues programmatically.md
    │   ├── Set up feedback criteria.md
    │   ├── Use annotation queues.md
    │   └── Use assertions.md
    ├── Datasets & Experiments
    │   ├── Analyze experiment results
    │   │   ├── Analyze an experiment.md
    │   │   ├── How to compare experiment results.md
    │   │   ├── How to fetch performance metrics for an experiment.md
    │   │   ├── How to filter experiments in the UI.md
    │   │   ├── How to upload experiments run outside of LangSmith with the REST API.md
    │   │   └── LangSmith Chat.md
    │   ├── Common data types
    │   │   ├── Dataset prebuilt JSON schema types.md
    │   │   ├── Dataset transformations.md
    │   │   └── Example data format.md
    │   ├── Datasets
    │   │   ├── Create a dataset
    │   │   │   ├── Create and manage datasets in the UI.md
    │   │   │   └── How to create and manage datasets programmatically.md
    │   │   ├── Custom output rendering.md
    │   │   └── Manage datasets.md
    │   ├── Evaluation techniques
    │   │   ├── Define evaluation target
    │   │   │   ├── How to define a target function to evaluate.md
    │   │   │   ├── How to evaluate a graph.md
    │   │   │   ├── How to evaluate a runnable.md
    │   │   │   ├── How to evaluate an application's intermediate steps.md
    │   │   │   ├── How to evaluate your agent with trajectory evaluations.md
    │   │   │   └── How to simulate multi-turn interactions.md
    │   │   ├── Experiment configuration
    │   │   │   ├── Experiment configuration.md
    │   │   │   ├── How to add evaluators to an existing experiment (Python only).md
    │   │   │   ├── How to evaluate with repetitions.md
    │   │   │   ├── How to handle model rate limits.md
    │   │   │   ├── How to read experiment results locally.md
    │   │   │   ├── How to retry failed runs in experiments (Python only).md
    │   │   │   ├── How to run an evaluation asynchronously.md
    │   │   │   └── How to run an evaluation locally (Python only).md
    │   │   ├── Multimodal evaluations
    │   │   │   └── Run an evaluation with multimodal content.md
    │   │   └── Scoring methods
    │   │       ├── How to return categorical vs numerical metrics.md
    │   │       └── How to return multiple scores in one evaluator.md
    │   ├── Fine-tuning
    │   │   └── Fine-tune models with Smithtune.md
    │   ├── Run an evaluation
    │   │   ├── How to evaluate agents.md
    │   │   ├── How to evaluate with OpenTelemetry.md
    │   │   ├── How to use the REST API.md
    │   │   └── Run an evaluation from the Playground.md
    │   └── Tutorials
    │       ├── Evaluate a chatbot.md
    │       ├── Evaluate a complex agent.md
    │       ├── Evaluate a RAG application.md
    │       ├── Run backtests on a new version of an agent.md
    │       └── Test a ReAct agent with Pytest-Vitest and LangSmith.md
    ├── Evaluators
    │   ├── Evaluator types
    │   │   ├── SDK
    │   │   │   ├── How to create a composite evaluator.md
    │   │   │   ├── How to define a code evaluator.md
    │   │   │   ├── How to define a summary evaluator.md
    │   │   │   ├── How to define an LLM-as-a-judge evaluator.md
    │   │   │   └── How to run a pairwise evaluation.md
    │   │   └── UI
    │   │       ├── How to create a composite evaluator.md
    │   │       ├── How to define a code evaluator.md
    │   │       ├── How to define a decision model evaluator.md
    │   │       └── How to define an LLM-as-a-judge evaluator.md
    │   ├── Frameworks & integrations
    │   │   ├── Harbor integrations.md
    │   │   ├── How to run evaluations with pytest.md
    │   │   ├── How to run evaluations with Vitest-Jest.md
    │   │   └── Run evals with openevals package.md
    │   ├── Improve evaluators
    │   │   ├── How to audit evaluator scores.md
    │   │   ├── How to improve your evaluator with few-shot examples.md
    │   │   └── Improve LLM-as-judge evaluators using human feedback.md
    │   ├── Automatically run evaluators on experiments.md
    │   ├── Evaluation types.md
    │   ├── Manage evaluators with the SDK.md
    │   ├── Manage evaluators.md
    │   └── Track and limit evaluator spend.md
    ├── Get started
    │   ├── Application-specific evaluation approaches.md
    │   ├── Evaluation concepts.md
    │   ├── Evaluation quickstart.md
    │   └── LangSmith Evaluation.md
    ├── Test from Playground
    │   └── Test from the Playground.md
    └── Test from Studio
        ├── Get started with Studio.md
        ├── How to use Studio.md
        ├── LangSmith Studio.md
        ├── Observability in Studio.md
        └── Studio troubleshooting.md
```

## 全部文档

| 路径 | 标题 | 摘要 / 关键词 | 来源 |
|---|---|---|---|
| `Additional documentation/No-code agents with LangSmith Fleet.md` | No-code agents with LangSmith Fleet | Create helpful AI agents without code. Start from a template, connect your accounts, and let the agent handle routine work while you stay in control.；Additional documentation, fleet | [原文](<https://docs.langchain.com/langsmith/fleet>) |
| `Build/Python/Deep Agents/Deployment/Managed Deep Agents.md` | Managed Deep Agents | Build your agent as a directory of files while LangSmith runs the harness and runtime.；Build, Deep Agents, Deployment, Python, agents, deep, managed | [原文](<https://docs.langchain.com/langsmith/python/managed-deep-agents>) |
| `Build/Python/Managed Deep Agents/Agent capabilities/Add a sandbox to Managed Deep Agents.md` | Add a sandbox to Managed Deep Agents | Configure an isolated filesystem and shell for a managed deep agent.；Agent capabilities, Build, Managed Deep Agents, Python, agents, deep, managed, sandboxes | [原文](<https://docs.langchain.com/langsmith/python/managed-deep-agents-sandboxes>) |
| `Build/Python/Managed Deep Agents/Agent capabilities/Add custom middleware to Managed Deep Agents.md` | Add custom middleware to Managed Deep Agents | Add built-in or custom middleware to a managed deep agent.；Agent capabilities, Build, Managed Deep Agents, Python, agents, deep, managed, middleware | [原文](<https://docs.langchain.com/langsmith/python/managed-deep-agents-middleware>) |
| `Build/Python/Managed Deep Agents/Agent capabilities/Add custom tools to Managed Deep Agents.md` | Add custom tools to Managed Deep Agents | Define authored tools for managed deep agents projects.；Agent capabilities, Build, Managed Deep Agents, Python, agents, deep, managed, tools | [原文](<https://docs.langchain.com/langsmith/python/managed-deep-agents-tools>) |
| `Build/Python/Managed Deep Agents/Agent capabilities/Add identity to Managed Deep Agents.md` | Add identity to Managed Deep Agents | Authenticate callers to a Managed Deep Agents deployment with a LangSmith API key, Supabase, another JWT provider, or your own backend.；Agent capabilities, Build, Managed Deep Agents, Python, agents, deep, identity, managed | [原文](<https://docs.langchain.com/langsmith/python/managed-deep-agents-identity>) |
| `Build/Python/Managed Deep Agents/Agent capabilities/Add instructions to Managed Deep Agents.md` | Add instructions to Managed Deep Agents | Define the system prompt for a managed deep agent in instructions.md.；Agent capabilities, Build, Managed Deep Agents, Python, agents, deep, instructions, managed | [原文](<https://docs.langchain.com/langsmith/python/managed-deep-agents-instructions>) |
| `Build/Python/Managed Deep Agents/Agent capabilities/Add memory to Managed Deep Agents.md` | Add memory to Managed Deep Agents | Opt in to durable agent and user memory layers for a managed deep agent.；Agent capabilities, Build, Managed Deep Agents, Python, agents, deep, managed, memory | [原文](<https://docs.langchain.com/langsmith/python/managed-deep-agents-memory>) |
| `Build/Python/Managed Deep Agents/Agent capabilities/Add schedules to Managed Deep Agents.md` | Add schedules to Managed Deep Agents | Declare managed cron schedules for Managed Deep Agents deployments, or create them at runtime.；Agent capabilities, Build, Managed Deep Agents, Python, agents, deep, managed, schedules | [原文](<https://docs.langchain.com/langsmith/python/managed-deep-agents-schedules>) |
| `Build/Python/Managed Deep Agents/Agent capabilities/Add skills to Managed Deep Agents.md` | Add skills to Managed Deep Agents | Add reusable task-specific instructions to a managed deep agent.；Agent capabilities, Build, Managed Deep Agents, Python, agents, deep, managed, skills | [原文](<https://docs.langchain.com/langsmith/python/managed-deep-agents-skills>) |
| `Build/Python/Managed Deep Agents/Agent capabilities/Browser use.md` | Browser use | Configure browser sharing, website logins, and human handoff for a managed deep agent.；Agent capabilities, Build, Managed Deep Agents, Python, agents, browser, deep, managed, use | [原文](<https://docs.langchain.com/langsmith/python/managed-deep-agents-browser-use>) |
| `Build/Python/Managed Deep Agents/Agent capabilities/Channels/Connect Managed Deep Agents to channels.md` | Connect Managed Deep Agents to channels | Connect Managed Deep Agents to external messaging services that can start runs and receive responses.；Agent capabilities, Build, Channels, Managed Deep Agents, Python, agents, channels, deep, managed | [原文](<https://docs.langchain.com/langsmith/python/managed-deep-agents-channels>) |
| `Build/Python/Managed Deep Agents/Agent capabilities/Channels/Connect a Managed Deep Agent to Slack.md` | Connect a Managed Deep Agent to Slack | Start Managed Deep Agents runs from Slack messages and send responses to Slack conversations.；Agent capabilities, Build, Channels, Managed Deep Agents, Python, agents, channels, deep, managed, slack | [原文](<https://docs.langchain.com/langsmith/python/managed-deep-agents-channels-slack>) |
| `Build/Python/Managed Deep Agents/Agent capabilities/Channels/Connect a Managed Deep Agent to a custom channel over HTTP.md` | Connect a Managed Deep Agent to a custom channel over HTTP | Start Managed Deep Agents runs from any external service that can send a webhook, and return responses through your own transport.；Agent capabilities, Build, Channels, Managed Deep Agents, Python, agents, channels, deep, http, managed | [原文](<https://docs.langchain.com/langsmith/python/managed-deep-agents-channels-http>) |
| `Build/Python/Managed Deep Agents/Agent capabilities/Channels/Prompt Slack users with agent-owned interrupts.md` | Prompt Slack users with agent-owned interrupts | Post a Slack form from a Managed Deep Agents tool, pause the run, and resume it when the user submits the form.；Agent capabilities, Build, Channels, Managed Deep Agents, Python, agent, agents, deep, interrupts, managed, owned | [原文](<https://docs.langchain.com/langsmith/python/managed-deep-agents-agent-owned-interrupts>) |
| `Build/Python/Managed Deep Agents/Agent capabilities/Connect to MCP servers.md` | Connect to MCP servers | Add tools from remote MCP servers to a managed deep agent.；Agent capabilities, Build, Managed Deep Agents, Python, agents, connectors, deep, managed, mcp | [原文](<https://docs.langchain.com/langsmith/python/managed-deep-agents-mcp-connectors>) |
| `Build/Python/Managed Deep Agents/Agent capabilities/Define a Managed Deep Agent.md` | Define a Managed Deep Agent | Configure the model and core capabilities of a managed deep agent.；Agent capabilities, Build, Managed Deep Agents, Python, agent, agents, deep, definition, managed | [原文](<https://docs.langchain.com/langsmith/python/managed-deep-agents-agent-definition>) |
| `Build/Python/Managed Deep Agents/Agent capabilities/Evaluate Managed Deep Agents.md` | Evaluate Managed Deep Agents | Develop Harbor evals for Managed Deep Agents with a coding agent and the eval-engineering skill.；Agent capabilities, Build, Managed Deep Agents, Python, agents, deep, evals, managed | [原文](<https://docs.langchain.com/langsmith/python/managed-deep-agents-evals>) |
| `Build/Python/Managed Deep Agents/Agent capabilities/Manage connections.md` | Manage connections | Store API keys and OAuth grants so Managed Deep Agents can authenticate with external services at runtime.；Agent capabilities, Build, Managed Deep Agents, Python, agents, connections, deep, managed | [原文](<https://docs.langchain.com/langsmith/python/managed-deep-agents-connections>) |
| `Build/Python/Managed Deep Agents/Agent capabilities/Managed Deep Agents runtime.md` | Managed Deep Agents runtime | Read run context, the verified caller, the thread, and the sandbox from the native runtime types that agent factories, tools, and middleware receive.；Agent capabilities, Build, Managed Deep Agents, Python, agents, deep, managed, runtime | [原文](<https://docs.langchain.com/langsmith/python/managed-deep-agents-runtime>) |
| `Build/Python/Managed Deep Agents/Agent capabilities/Subagents.md` | Subagents | Delegate work to subagents that run inline or in the background for a managed deep agent.；Agent capabilities, Build, Managed Deep Agents, Python, agents, deep, managed, subagents | [原文](<https://docs.langchain.com/langsmith/python/managed-deep-agents-subagents>) |
| `Build/Python/Managed Deep Agents/Agent capabilities/Web search.md` | Web search | Add web search powered by Parallel to Managed Deep Agents without a separate account or API key.；Agent capabilities, Build, Managed Deep Agents, Python, agents, deep, managed, search | [原文](<https://docs.langchain.com/langsmith/python/managed-deep-agents-search>) |
| `Build/Python/Managed Deep Agents/Build and deploy/Add a custom search tool, memory, and a schedule.md` | Add a custom search tool, memory, and a schedule | Replace provider search with a Tavily tool, then add durable memory and a daily schedule to the research assistant from the quickstart.；Build, Build and deploy, Managed Deep Agents, Python, agents, deep, managed, tutorial | [原文](<https://docs.langchain.com/langsmith/python/managed-deep-agents-tutorial>) |
| `Build/Python/Managed Deep Agents/Build and deploy/Build a custom frontend for a Managed Deep Agent.md` | Build a custom frontend for a Managed Deep Agent | Call a Managed Deep Agents deployment from your own web or Python application with the LangChain frontend SDKs and the LangGraph SDK.；Build, Build and deploy, Managed Deep Agents, Python, agents, custom, deep, frontend, managed | [原文](<https://docs.langchain.com/langsmith/python/managed-deep-agents-custom-frontend>) |
| `Build/Python/Managed Deep Agents/Build and deploy/Connect MCP clients to a Managed Deep Agent.md` | Connect MCP clients to a Managed Deep Agent | Expose a deployed Managed Deep Agent as a tool to MCP clients such as Claude Code.；Build, Build and deploy, Managed Deep Agents, Python, agents, deep, endpoint, managed, mcp | [原文](<https://docs.langchain.com/langsmith/python/managed-deep-agents-mcp-endpoint>) |
| `Build/Python/Managed Deep Agents/Build and deploy/Deploy a Managed Deep Agent.md` | Deploy a Managed Deep Agent | Test and deploy a Managed Deep Agent with the mda CLI.；Build, Build and deploy, Managed Deep Agents, Python, agents, deep, deploy, managed | [原文](<https://docs.langchain.com/langsmith/python/managed-deep-agents-deploy>) |
| `Build/Python/Managed Deep Agents/Build and deploy/Develop locally with LangSmith Studio.md` | Develop locally with LangSmith Studio | Run and test a Managed Deep Agent locally with mda dev and LangSmith Studio.；Build, Build and deploy, Managed Deep Agents, Python, agents, deep, development, local, managed | [原文](<https://docs.langchain.com/langsmith/python/managed-deep-agents-local-development>) |
| `Build/Python/Managed Deep Agents/Build and deploy/Manage Context Hub for Managed Deep Agents.md` | Manage Context Hub for Managed Deep Agents | Understand how Managed Deep Agents stores instructions, skills, and durable memory in LangSmith Context Hub.；Build, Build and deploy, Managed Deep Agents, Python, agents, context, deep, hub, managed | [原文](<https://docs.langchain.com/langsmith/python/managed-deep-agents-context-hub>) |
| `Build/Python/Managed Deep Agents/Build and deploy/Managed Deep Agents CLI reference.md` | Managed Deep Agents CLI reference | Reference for mda commands, project files, and deploy behavior.；Build, Build and deploy, Managed Deep Agents, Python, agents, cli, deep, managed | [原文](<https://docs.langchain.com/langsmith/python/managed-deep-agents-cli>) |
| `Build/Python/Managed Deep Agents/Get started/Managed Deep Agents project structure.md` | Managed Deep Agents project structure | Understand the project layout for Managed Deep Agents.；Build, Get started, Managed Deep Agents, Python, agents, deep, managed, project, structure | [原文](<https://docs.langchain.com/langsmith/python/managed-deep-agents-project-structure>) |
| `Build/Python/Managed Deep Agents/Get started/Managed Deep Agents quickstart.md` | Managed Deep Agents quickstart | Create and deploy your first Managed Deep Agent with the mda CLI.；Build, Get started, Managed Deep Agents, Python, agents, deep, managed, quickstart | [原文](<https://docs.langchain.com/langsmith/python/managed-deep-agents-quickstart>) |
| `Build/Python/Managed Deep Agents/Get started/Move from Deep Agents to Managed Deep Agents.md` | Move from Deep Agents to Managed Deep Agents | Convert an agent built with create_deep_agent into a Managed Deep Agents project.；Build, Get started, Managed Deep Agents, Python, agents, deep, managed, migrate | [原文](<https://docs.langchain.com/langsmith/python/managed-deep-agents-migrate>) |
| `Build/Python/Managed Deep Agents/Templates/Deploy the open-source design agent.md` | Deploy the open-source design agent | Deploy Content Studio, an open-source design agent, to Slack as a Managed Deep Agents project.；Build, Managed Deep Agents, Python, Templates, agent, agents, deep, design, managed | [原文](<https://docs.langchain.com/langsmith/python/managed-deep-agents-design-agent>) |
| `Build/Python/Managed Deep Agents/Templates/Deploy the open-source paid media agent.md` | Deploy the open-source paid media agent | Deploy the open-source paid media agent to Slack as a Managed Deep Agents project for campaign analysis, scheduled reports, and reviewed changes.；Build, Managed Deep Agents, Python, Templates, agent, agents, deep, managed, media, paid | [原文](<https://docs.langchain.com/langsmith/python/managed-deep-agents-paid-media-agent>) |
| `Build/TypeScript/Deep Agents/Deployment/Managed Deep Agents.md` | Managed Deep Agents | Build your agent as a directory of files while LangSmith runs the harness and runtime.；Build, Deep Agents, Deployment, TypeScript, agents, deep, managed | [原文](<https://docs.langchain.com/langsmith/javascript/managed-deep-agents>) |
| `Build/TypeScript/Managed Deep Agents/Agent capabilities/Add a sandbox to Managed Deep Agents.md` | Add a sandbox to Managed Deep Agents | Configure an isolated filesystem and shell for a managed deep agent.；Agent capabilities, Build, Managed Deep Agents, TypeScript, agents, deep, managed, sandboxes | [原文](<https://docs.langchain.com/langsmith/javascript/managed-deep-agents-sandboxes>) |
| `Build/TypeScript/Managed Deep Agents/Agent capabilities/Add custom middleware to Managed Deep Agents.md` | Add custom middleware to Managed Deep Agents | Add built-in or custom middleware to a managed deep agent.；Agent capabilities, Build, Managed Deep Agents, TypeScript, agents, deep, managed, middleware | [原文](<https://docs.langchain.com/langsmith/javascript/managed-deep-agents-middleware>) |
| `Build/TypeScript/Managed Deep Agents/Agent capabilities/Add custom tools to Managed Deep Agents.md` | Add custom tools to Managed Deep Agents | Define authored tools for managed deep agents projects.；Agent capabilities, Build, Managed Deep Agents, TypeScript, agents, deep, managed, tools | [原文](<https://docs.langchain.com/langsmith/javascript/managed-deep-agents-tools>) |
| `Build/TypeScript/Managed Deep Agents/Agent capabilities/Add identity to Managed Deep Agents.md` | Add identity to Managed Deep Agents | Authenticate callers to a Managed Deep Agents deployment with a LangSmith API key, Supabase, another JWT provider, or your own backend.；Agent capabilities, Build, Managed Deep Agents, TypeScript, agents, deep, identity, managed | [原文](<https://docs.langchain.com/langsmith/javascript/managed-deep-agents-identity>) |
| `Build/TypeScript/Managed Deep Agents/Agent capabilities/Add instructions to Managed Deep Agents.md` | Add instructions to Managed Deep Agents | Define the system prompt for a managed deep agent in instructions.md.；Agent capabilities, Build, Managed Deep Agents, TypeScript, agents, deep, instructions, managed | [原文](<https://docs.langchain.com/langsmith/javascript/managed-deep-agents-instructions>) |
| `Build/TypeScript/Managed Deep Agents/Agent capabilities/Add memory to Managed Deep Agents.md` | Add memory to Managed Deep Agents | Opt in to durable agent and user memory layers for a managed deep agent.；Agent capabilities, Build, Managed Deep Agents, TypeScript, agents, deep, managed, memory | [原文](<https://docs.langchain.com/langsmith/javascript/managed-deep-agents-memory>) |
| `Build/TypeScript/Managed Deep Agents/Agent capabilities/Add schedules to Managed Deep Agents.md` | Add schedules to Managed Deep Agents | Declare managed cron schedules for Managed Deep Agents deployments, or create them at runtime.；Agent capabilities, Build, Managed Deep Agents, TypeScript, agents, deep, managed, schedules | [原文](<https://docs.langchain.com/langsmith/javascript/managed-deep-agents-schedules>) |
| `Build/TypeScript/Managed Deep Agents/Agent capabilities/Add skills to Managed Deep Agents.md` | Add skills to Managed Deep Agents | Add reusable task-specific instructions to a managed deep agent.；Agent capabilities, Build, Managed Deep Agents, TypeScript, agents, deep, managed, skills | [原文](<https://docs.langchain.com/langsmith/javascript/managed-deep-agents-skills>) |
| `Build/TypeScript/Managed Deep Agents/Agent capabilities/Browser use.md` | Browser use | Configure browser sharing, website logins, and human handoff for a managed deep agent.；Agent capabilities, Build, Managed Deep Agents, TypeScript, agents, browser, deep, managed, use | [原文](<https://docs.langchain.com/langsmith/javascript/managed-deep-agents-browser-use>) |
| `Build/TypeScript/Managed Deep Agents/Agent capabilities/Channels/Connect Managed Deep Agents to channels.md` | Connect Managed Deep Agents to channels | Connect Managed Deep Agents to external messaging services that can start runs and receive responses.；Agent capabilities, Build, Channels, Managed Deep Agents, TypeScript, agents, channels, deep, managed | [原文](<https://docs.langchain.com/langsmith/javascript/managed-deep-agents-channels>) |
| `Build/TypeScript/Managed Deep Agents/Agent capabilities/Channels/Connect a Managed Deep Agent to Slack.md` | Connect a Managed Deep Agent to Slack | Start Managed Deep Agents runs from Slack messages and send responses to Slack conversations.；Agent capabilities, Build, Channels, Managed Deep Agents, TypeScript, agents, channels, deep, managed, slack | [原文](<https://docs.langchain.com/langsmith/javascript/managed-deep-agents-channels-slack>) |
| `Build/TypeScript/Managed Deep Agents/Agent capabilities/Channels/Connect a Managed Deep Agent to a custom channel over HTTP.md` | Connect a Managed Deep Agent to a custom channel over HTTP | Start Managed Deep Agents runs from any external service that can send a webhook, and return responses through your own transport.；Agent capabilities, Build, Channels, Managed Deep Agents, TypeScript, agents, channels, deep, http, managed | [原文](<https://docs.langchain.com/langsmith/javascript/managed-deep-agents-channels-http>) |
| `Build/TypeScript/Managed Deep Agents/Agent capabilities/Channels/Prompt Slack users with agent-owned interrupts.md` | Prompt Slack users with agent-owned interrupts | Post a Slack form from a Managed Deep Agents tool, pause the run, and resume it when the user submits the form.；Agent capabilities, Build, Channels, Managed Deep Agents, TypeScript, agent, agents, deep, interrupts, managed, owned | [原文](<https://docs.langchain.com/langsmith/javascript/managed-deep-agents-agent-owned-interrupts>) |
| `Build/TypeScript/Managed Deep Agents/Agent capabilities/Connect to MCP servers.md` | Connect to MCP servers | Add tools from remote MCP servers to a managed deep agent.；Agent capabilities, Build, Managed Deep Agents, TypeScript, agents, connectors, deep, managed, mcp | [原文](<https://docs.langchain.com/langsmith/javascript/managed-deep-agents-mcp-connectors>) |
| `Build/TypeScript/Managed Deep Agents/Agent capabilities/Define a Managed Deep Agent.md` | Define a Managed Deep Agent | Configure the model and core capabilities of a managed deep agent.；Agent capabilities, Build, Managed Deep Agents, TypeScript, agent, agents, deep, definition, managed | [原文](<https://docs.langchain.com/langsmith/javascript/managed-deep-agents-agent-definition>) |
| `Build/TypeScript/Managed Deep Agents/Agent capabilities/Evaluate Managed Deep Agents.md` | Evaluate Managed Deep Agents | Develop Harbor evals for Managed Deep Agents with a coding agent and the eval-engineering skill.；Agent capabilities, Build, Managed Deep Agents, TypeScript, agents, deep, evals, managed | [原文](<https://docs.langchain.com/langsmith/javascript/managed-deep-agents-evals>) |
| `Build/TypeScript/Managed Deep Agents/Agent capabilities/Manage connections.md` | Manage connections | Store API keys and OAuth grants so Managed Deep Agents can authenticate with external services at runtime.；Agent capabilities, Build, Managed Deep Agents, TypeScript, agents, connections, deep, managed | [原文](<https://docs.langchain.com/langsmith/javascript/managed-deep-agents-connections>) |
| `Build/TypeScript/Managed Deep Agents/Agent capabilities/Managed Deep Agents runtime.md` | Managed Deep Agents runtime | Read run context, the verified caller, the thread, and the sandbox from the native runtime types that agent factories, tools, and middleware receive.；Agent capabilities, Build, Managed Deep Agents, TypeScript, agents, deep, managed, runtime | [原文](<https://docs.langchain.com/langsmith/javascript/managed-deep-agents-runtime>) |
| `Build/TypeScript/Managed Deep Agents/Agent capabilities/Subagents.md` | Subagents | Delegate work to subagents that run inline or in the background for a managed deep agent.；Agent capabilities, Build, Managed Deep Agents, TypeScript, agents, deep, managed, subagents | [原文](<https://docs.langchain.com/langsmith/javascript/managed-deep-agents-subagents>) |
| `Build/TypeScript/Managed Deep Agents/Agent capabilities/Web search.md` | Web search | Add web search powered by Parallel to Managed Deep Agents without a separate account or API key.；Agent capabilities, Build, Managed Deep Agents, TypeScript, agents, deep, managed, search | [原文](<https://docs.langchain.com/langsmith/javascript/managed-deep-agents-search>) |
| `Build/TypeScript/Managed Deep Agents/Build and deploy/Add a custom search tool, memory, and a schedule.md` | Add a custom search tool, memory, and a schedule | Replace provider search with a Tavily tool, then add durable memory and a daily schedule to the research assistant from the quickstart.；Build, Build and deploy, Managed Deep Agents, TypeScript, agents, deep, managed, tutorial | [原文](<https://docs.langchain.com/langsmith/javascript/managed-deep-agents-tutorial>) |
| `Build/TypeScript/Managed Deep Agents/Build and deploy/Build a custom frontend for a Managed Deep Agent.md` | Build a custom frontend for a Managed Deep Agent | Call a Managed Deep Agents deployment from your own web or Python application with the LangChain frontend SDKs and the LangGraph SDK.；Build, Build and deploy, Managed Deep Agents, TypeScript, agents, custom, deep, frontend, managed | [原文](<https://docs.langchain.com/langsmith/javascript/managed-deep-agents-custom-frontend>) |
| `Build/TypeScript/Managed Deep Agents/Build and deploy/Connect MCP clients to a Managed Deep Agent.md` | Connect MCP clients to a Managed Deep Agent | Expose a deployed Managed Deep Agent as a tool to MCP clients such as Claude Code.；Build, Build and deploy, Managed Deep Agents, TypeScript, agents, deep, endpoint, managed, mcp | [原文](<https://docs.langchain.com/langsmith/javascript/managed-deep-agents-mcp-endpoint>) |
| `Build/TypeScript/Managed Deep Agents/Build and deploy/Deploy a Managed Deep Agent.md` | Deploy a Managed Deep Agent | Test and deploy a Managed Deep Agent with the mda CLI.；Build, Build and deploy, Managed Deep Agents, TypeScript, agents, deep, deploy, managed | [原文](<https://docs.langchain.com/langsmith/javascript/managed-deep-agents-deploy>) |
| `Build/TypeScript/Managed Deep Agents/Build and deploy/Develop locally with LangSmith Studio.md` | Develop locally with LangSmith Studio | Run and test a Managed Deep Agent locally with mda dev and LangSmith Studio.；Build, Build and deploy, Managed Deep Agents, TypeScript, agents, deep, development, local, managed | [原文](<https://docs.langchain.com/langsmith/javascript/managed-deep-agents-local-development>) |
| `Build/TypeScript/Managed Deep Agents/Build and deploy/Manage Context Hub for Managed Deep Agents.md` | Manage Context Hub for Managed Deep Agents | Understand how Managed Deep Agents stores instructions, skills, and durable memory in LangSmith Context Hub.；Build, Build and deploy, Managed Deep Agents, TypeScript, agents, context, deep, hub, managed | [原文](<https://docs.langchain.com/langsmith/javascript/managed-deep-agents-context-hub>) |
| `Build/TypeScript/Managed Deep Agents/Build and deploy/Managed Deep Agents CLI reference.md` | Managed Deep Agents CLI reference | Reference for mda commands, project files, and deploy behavior.；Build, Build and deploy, Managed Deep Agents, TypeScript, agents, cli, deep, managed | [原文](<https://docs.langchain.com/langsmith/javascript/managed-deep-agents-cli>) |
| `Build/TypeScript/Managed Deep Agents/Get started/Managed Deep Agents project structure.md` | Managed Deep Agents project structure | Understand the project layout for Managed Deep Agents.；Build, Get started, Managed Deep Agents, TypeScript, agents, deep, managed, project, structure | [原文](<https://docs.langchain.com/langsmith/javascript/managed-deep-agents-project-structure>) |
| `Build/TypeScript/Managed Deep Agents/Get started/Managed Deep Agents quickstart.md` | Managed Deep Agents quickstart | Create and deploy your first Managed Deep Agent with the mda CLI.；Build, Get started, Managed Deep Agents, TypeScript, agents, deep, managed, quickstart | [原文](<https://docs.langchain.com/langsmith/javascript/managed-deep-agents-quickstart>) |
| `Build/TypeScript/Managed Deep Agents/Get started/Move from Deep Agents to Managed Deep Agents.md` | Move from Deep Agents to Managed Deep Agents | Convert an agent built with create_deep_agent into a Managed Deep Agents project.；Build, Get started, Managed Deep Agents, TypeScript, agents, deep, managed, migrate | [原文](<https://docs.langchain.com/langsmith/javascript/managed-deep-agents-migrate>) |
| `Build/TypeScript/Managed Deep Agents/Templates/Deploy the open-source design agent.md` | Deploy the open-source design agent | Deploy Content Studio, an open-source design agent, to Slack as a Managed Deep Agents project.；Build, Managed Deep Agents, Templates, TypeScript, agent, agents, deep, design, managed | [原文](<https://docs.langchain.com/langsmith/javascript/managed-deep-agents-design-agent>) |
| `Build/TypeScript/Managed Deep Agents/Templates/Deploy the open-source paid media agent.md` | Deploy the open-source paid media agent | Deploy the open-source paid media agent to Slack as a Managed Deep Agents project for campaign analysis, scheduled reports, and reviewed changes.；Build, Managed Deep Agents, Templates, TypeScript, agent, agents, deep, managed, media, paid | [原文](<https://docs.langchain.com/langsmith/javascript/managed-deep-agents-paid-media-agent>) |
| `Deploy/Agent Server/Agent Server.md` | Agent Server | Configure and operate the LangSmith Agent Server runtime, including capabilities, application structure, auth, and customization.；Agent Server, Deploy, agent, overview, server | [原文](<https://docs.langchain.com/langsmith/agent-server-overview>) |
| `Deploy/Agent Server/Auth & access control/Add custom authentication.md` | Add custom authentication | [!NOTE]；Agent Server, Auth & access control, Deploy, auth, custom | [原文](<https://docs.langchain.com/langsmith/custom-auth>) |
| `Deploy/Agent Server/Auth & access control/Authentication & access control.md` | Authentication & access control | [!NOTE]；Agent Server, Auth & access control, Deploy, auth | [原文](<https://docs.langchain.com/langsmith/auth>) |
| `Deploy/Agent Server/Auth & access control/Custom auth tutorial/Connect an authentication provider.md` | Connect an authentication provider | Agent Server, Auth & access control, Custom auth tutorial, Deploy, add, auth, server | [原文](<https://docs.langchain.com/langsmith/add-auth-server>) |
| `Deploy/Agent Server/Auth & access control/Custom auth tutorial/Isolate store data per user.md` | Isolate store data per user | Scope long-term store data to each authenticated user in LangSmith Agent Server using auth handlers.；Agent Server, Auth & access control, Custom auth tutorial, Deploy, auth, store | [原文](<https://docs.langchain.com/langsmith/store-auth>) |
| `Deploy/Agent Server/Auth & access control/Custom auth tutorial/Make conversations private.md` | Make conversations private | Agent Server, Auth & access control, Custom auth tutorial, Deploy, auth, resource | [原文](<https://docs.langchain.com/langsmith/resource-auth>) |
| `Deploy/Agent Server/Auth & access control/Custom auth tutorial/Set up custom authentication.md` | Set up custom authentication | [!NOTE]；Agent Server, Auth & access control, Custom auth tutorial, Deploy, auth, custom, set, up | [原文](<https://docs.langchain.com/langsmith/set-up-custom-auth>) |
| `Deploy/Agent Server/Auth & access control/Document API authentication in OpenAPI.md` | Document API authentication in OpenAPI | [!NOTE]；Agent Server, Auth & access control, Deploy, openapi, security | [原文](<https://docs.langchain.com/langsmith/openapi-security>) |
| `Deploy/Agent Server/Auth & access control/Set up Agent Auth.md` | Set up Agent Auth | Enable secure access from agents to any system using OAuth 2.0 credentials with Agent Auth.；Agent Server, Auth & access control, Deploy, agent, auth | [原文](<https://docs.langchain.com/langsmith/agent-auth>) |
| `Deploy/Agent Server/Capabilities/A2A endpoint in Agent Server.md` | A2A endpoint in Agent Server | Use the A2A protocol to enable agent-to-agent communication with distributed tracing in LangSmith.；Agent Server, Capabilities, Deploy, a2a, server | [原文](<https://docs.langchain.com/langsmith/server-a2a>) |
| `Deploy/Agent Server/Capabilities/Agent Server.md` | Agent Server | [!NOTE]；Agent Server, Capabilities, Deploy, agent, server | [原文](<https://docs.langchain.com/langsmith/agent-server>) |
| `Deploy/Agent Server/Capabilities/Assistants/Assistants.md` | Assistants | [!NOTE]；Agent Server, Assistants, Capabilities, Deploy, assistants | [原文](<https://docs.langchain.com/langsmith/assistants>) |
| `Deploy/Agent Server/Capabilities/Assistants/Manage assistants.md` | Manage assistants | [tab] SDK；Agent Server, Assistants, Capabilities, Deploy, cloud, configuration | [原文](<https://docs.langchain.com/langsmith/configuration-cloud>) |
| `Deploy/Agent Server/Capabilities/Distributed tracing with Agent Server.md` | Distributed tracing with Agent Server | Unify traces when calling your deployed Agent Server from another service using RemoteGraph or the SDK.；Agent Server, Capabilities, Deploy, agent, distributed, server, tracing | [原文](<https://docs.langchain.com/langsmith/agent-server-distributed-tracing>) |
| `Deploy/Agent Server/Capabilities/Double-texting/Double texting.md` | Double texting | [!NOTE]；Agent Server, Capabilities, Deploy, Double-texting, double, texting | [原文](<https://docs.langchain.com/langsmith/double-texting>) |
| `Deploy/Agent Server/Capabilities/Double-texting/Enqueue concurrent.md` | Enqueue concurrent | [tab] Javascript；Agent Server, Capabilities, Deploy, Double-texting, concurrent, enqueue | [原文](<https://docs.langchain.com/langsmith/enqueue-concurrent>) |
| `Deploy/Agent Server/Capabilities/Double-texting/Interrupt concurrent.md` | Interrupt concurrent | [tab] Javascript；Agent Server, Capabilities, Deploy, Double-texting, concurrent, interrupt | [原文](<https://docs.langchain.com/langsmith/interrupt-concurrent>) |
| `Deploy/Agent Server/Capabilities/Double-texting/Reject Concurrent.md` | Reject Concurrent | [tab] Javascript；Agent Server, Capabilities, Deploy, Double-texting, concurrent, reject | [原文](<https://docs.langchain.com/langsmith/reject-concurrent>) |
| `Deploy/Agent Server/Capabilities/Double-texting/Rollback Concurrent.md` | Rollback Concurrent | [tab] Javascript；Agent Server, Capabilities, Deploy, Double-texting, concurrent, rollback | [原文](<https://docs.langchain.com/langsmith/rollback-concurrent>) |
| `Deploy/Agent Server/Capabilities/How to interact with a deployment using RemoteGraph.md` | How to interact with a deployment using RemoteGraph | [!WARNING]；Agent Server, Capabilities, Deploy, graph, remote, use | [原文](<https://docs.langchain.com/langsmith/use-remote-graph>) |
| `Deploy/Agent Server/Capabilities/Human-in-the-loop over MCP.md` | Human-in-the-loop over MCP | Ask an MCP client for input when an agent exposed through the Agent Server MCP endpoint pauses, then resume the tool call with the answers.；Agent Server, Capabilities, Deploy, elicitation, mcp, server | [原文](<https://docs.langchain.com/langsmith/server-mcp-elicitation>) |
| `Deploy/Agent Server/Capabilities/Human-in-the-loop using server API.md` | Human-in-the-loop using server API | [tab] Python；Agent Server, Capabilities, Deploy, add, human, in, loop, the | [原文](<https://docs.langchain.com/langsmith/add-human-in-the-loop>) |
| `Deploy/Agent Server/Capabilities/MCP endpoint in Agent Server.md` | MCP endpoint in Agent Server | [!NOTE]；Agent Server, Capabilities, Deploy, mcp, server | [原文](<https://docs.langchain.com/langsmith/server-mcp>) |
| `Deploy/Agent Server/Capabilities/Runs/How to cancel a run.md` | How to cancel a run | Cancel a single run or multiple runs via the API, and choose between interrupt and rollback actions.；Agent Server, Capabilities, Deploy, Runs, cancel, run | [原文](<https://docs.langchain.com/langsmith/cancel-run>) |
| `Deploy/Agent Server/Capabilities/Runs/How to kick off background runs.md` | How to kick off background runs | [tab] Python；Agent Server, Capabilities, Deploy, Runs, background, run | [原文](<https://docs.langchain.com/langsmith/background-run>) |
| `Deploy/Agent Server/Capabilities/Runs/How to run multiple assistants on the same thread.md` | How to run multiple assistants on the same thread | [tab] Python；Agent Server, Capabilities, Deploy, Runs, same, thread | [原文](<https://docs.langchain.com/langsmith/same-thread>) |
| `Deploy/Agent Server/Capabilities/Runs/Prioritize runs.md` | Prioritize runs | Set a priority for each thread so that urgent runs start first.；Agent Server, Capabilities, Deploy, Runs, priority, run | [原文](<https://docs.langchain.com/langsmith/run-priority>) |
| `Deploy/Agent Server/Capabilities/Runs/Runs.md` | Runs | An overview of runs in Agent Server, including how to kick off background runs, stateless runs, and cancel runs.；Agent Server, Capabilities, Deploy, Runs, runs | [原文](<https://docs.langchain.com/langsmith/runs>) |
| `Deploy/Agent Server/Capabilities/Runs/Stateless runs.md` | Stateless runs | [tab] Python；Agent Server, Capabilities, Deploy, Runs, runs, stateless | [原文](<https://docs.langchain.com/langsmith/stateless-runs>) |
| `Deploy/Agent Server/Capabilities/Streaming API.md` | Streaming API | [!NOTE]；Agent Server, Capabilities, Deploy, streaming | [原文](<https://docs.langchain.com/langsmith/streaming>) |
| `Deploy/Agent Server/Capabilities/Time travel using the server API.md` | Time travel using the server API | [accordion] Example graph；Agent Server, Capabilities, Deploy, human, in, loop, the, time, travel | [原文](<https://docs.langchain.com/langsmith/human-in-the-loop-time-travel>) |
| `Deploy/Agent Server/Capabilities/Use cron jobs.md` | Use cron jobs | [!NOTE]；Agent Server, Capabilities, Deploy, cron, jobs | [原文](<https://docs.langchain.com/langsmith/cron-jobs>) |
| `Deploy/Agent Server/Capabilities/Use threads.md` | Use threads | [!NOTE]；Agent Server, Capabilities, Deploy, threads, use | [原文](<https://docs.langchain.com/langsmith/use-threads>) |
| `Deploy/Agent Server/Capabilities/Use webhooks.md` | Use webhooks | [!NOTE]；Agent Server, Capabilities, Deploy, use, webhooks | [原文](<https://docs.langchain.com/langsmith/use-webhooks>) |
| `Deploy/Agent Server/Develop your application/Application structure.md` | Application structure | [!TIP]；Agent Server, Deploy, Develop your application, application, structure | [原文](<https://docs.langchain.com/langsmith/application-structure>) |
| `Deploy/Agent Server/Develop your application/Persistence/Configure checkpointer backend.md` | Configure checkpointer backend | Configure Agent Server to use PostgreSQL, MongoDB, or a custom implementation for checkpoint storage.；Agent Server, Deploy, Develop your application, Persistence, checkpointer, configure | [原文](<https://docs.langchain.com/langsmith/configure-checkpointer>) |
| `Deploy/Agent Server/Develop your application/Persistence/How to add TTLs to your application.md` | How to add TTLs to your application | [!TIP]；Agent Server, Deploy, Develop your application, Persistence, configure, ttl | [原文](<https://docs.langchain.com/langsmith/configure-ttl>) |
| `Deploy/Agent Server/Develop your application/Persistence/How to add semantic search to your agent deployment.md` | How to add semantic search to your agent deployment | [!WARNING]；Agent Server, Deploy, Develop your application, Persistence, search, semantic | [原文](<https://docs.langchain.com/langsmith/semantic-search>) |
| `Deploy/Agent Server/Develop your application/Set up dependencies/How to customize the Dockerfile.md` | How to customize the Dockerfile | Agent Server, Deploy, Develop your application, Set up dependencies, custom, docker | [原文](<https://docs.langchain.com/langsmith/custom-docker>) |
| `Deploy/Agent Server/Develop your application/Set up dependencies/How to set up a JavaScript application.md` | How to set up a JavaScript application | [!TIP]；Agent Server, Deploy, Develop your application, Set up dependencies, javascript, setup | [原文](<https://docs.langchain.com/langsmith/setup-javascript>) |
| `Deploy/Agent Server/Develop your application/Set up dependencies/How to set up an application with pyproject.toml.md` | How to set up an application with pyproject.toml | [!TIP]；Agent Server, Deploy, Develop your application, Set up dependencies, pyproject, setup | [原文](<https://docs.langchain.com/langsmith/setup-pyproject>) |
| `Deploy/Agent Server/Develop your application/Set up dependencies/How to set up an application with requirements.txt.md` | How to set up an application with requirements.txt | [!TIP]；Agent Server, Deploy, Develop your application, Set up dependencies, app, requirements, setup, txt | [原文](<https://docs.langchain.com/langsmith/setup-app-requirements-txt>) |
| `Deploy/Agent Server/Develop your application/Set up dependencies/Monorepo support.md` | Monorepo support | Agent Server, Deploy, Develop your application, Set up dependencies, monorepo, support | [原文](<https://docs.langchain.com/langsmith/monorepo-support>) |
| `Deploy/Agent Server/How to build/How to collect user feedback for Agent Server runs.md` | How to collect user feedback for Agent Server runs | [tab] Python SDK；Agent Server, Deploy, How to build, agent, feedback, server | [原文](<https://docs.langchain.com/langsmith/agent-server-feedback>) |
| `Deploy/Agent Server/How to build/How to implement generative user interfaces with LangGraph.md` | How to implement generative user interfaces with LangGraph | [!NOTE]；Agent Server, Deploy, How to build, generative, react, ui | [原文](<https://docs.langchain.com/langsmith/generative-ui-react>) |
| `Deploy/Agent Server/How to build/Implement a CI-CD pipeline using LangSmith Agent Server and Evaluation.md` | Implement a CI/CD pipeline using LangSmith Agent Server and Evaluation | [!NOTE]；Agent Server, Deploy, How to build, cicd, example, pipeline | [原文](<https://docs.langchain.com/langsmith/cicd-pipeline-example>) |
| `Deploy/Agent Server/Server customization/Configure IAM authentication for data stores.md` | Configure IAM authentication for data stores | Configure Agent Server to use cloud workload identities for PostgreSQL and Redis authentication.；Agent Server, Deploy, Server customization, auth, configure, iam | [原文](<https://docs.langchain.com/langsmith/configure-iam-auth>) |
| `Deploy/Agent Server/Server customization/Encryption at rest/Configure AES encryption at rest.md` | Configure AES encryption at rest | Configure built-in AES encryption and lazy key rotation for Agent Server data.；Agent Server, Deploy, Encryption at rest, Server customization, aes, encryption | [原文](<https://docs.langchain.com/langsmith/aes-encryption>) |
| `Deploy/Agent Server/Server customization/Encryption at rest/Configure custom encryption at rest.md` | Configure custom encryption at rest | [!WARNING]；Agent Server, Deploy, Encryption at rest, Server customization, custom, encryption | [原文](<https://docs.langchain.com/langsmith/custom-encryption>) |
| `Deploy/Agent Server/Server customization/Encryption at rest/Encryption at rest.md` | Encryption at rest | Choose between built-in AES encryption and custom encryption handlers for Agent Server data.；Agent Server, Deploy, Encryption at rest, Server customization, encryption | [原文](<https://docs.langchain.com/langsmith/encryption>) |
| `Deploy/Agent Server/Server customization/Extend the HTTP server/How to add custom lifespan events.md` | How to add custom lifespan events | [!NOTE]；Agent Server, Deploy, Extend the HTTP server, Server customization, custom, lifespan | [原文](<https://docs.langchain.com/langsmith/custom-lifespan>) |
| `Deploy/Agent Server/Server customization/Extend the HTTP server/How to add custom middleware.md` | How to add custom middleware | [!NOTE]；Agent Server, Deploy, Extend the HTTP server, Server customization, custom, middleware | [原文](<https://docs.langchain.com/langsmith/custom-middleware>) |
| `Deploy/Agent Server/Server customization/Extend the HTTP server/How to add custom routes.md` | How to add custom routes | [tab] Python；Agent Server, Deploy, Extend the HTTP server, Server customization, custom, routes | [原文](<https://docs.langchain.com/langsmith/custom-routes>) |
| `Deploy/Agent Server/Server customization/Headers and logging/Include HTTP headers in server logs.md` | Include HTTP headers in server logs | Agent Server, Deploy, Headers and logging, Server customization, configurable, logs | [原文](<https://docs.langchain.com/langsmith/configurable-logs>) |
| `Deploy/Agent Server/Server customization/Headers and logging/Use HTTP headers for runtime configuration.md` | Use HTTP headers for runtime configuration | Agent Server, Deploy, Headers and logging, Server customization, configurable, headers | [原文](<https://docs.langchain.com/langsmith/configurable-headers>) |
| `Deploy/Agent Server/Server customization/Rebuild graph at runtime.md` | Rebuild graph at runtime | Rebuild your graph with different configurations for each run using ServerRuntime.；Agent Server, Deploy, Server customization, graph, rebuild | [原文](<https://docs.langchain.com/langsmith/graph-rebuild>) |
| `Deploy/Agent Server/Server customization/Replace built-in backends/How to use a custom checkpointer.md` | How to use a custom checkpointer | Replace the built-in Postgres checkpointer with a custom BaseCheckpointSaver implementation in your agent deployment.；Agent Server, Deploy, Replace built-in backends, Server customization, checkpointer, custom | [原文](<https://docs.langchain.com/langsmith/custom-checkpointer>) |
| `Deploy/Agent Server/Server customization/Replace built-in backends/How to use a custom store.md` | How to use a custom store | Replace the built-in Postgres store with a custom BaseStore implementation in your agent deployment.；Agent Server, Deploy, Replace built-in backends, Server customization, custom, store | [原文](<https://docs.langchain.com/langsmith/custom-store>) |
| `Deploy/Agent Server/Server customization/Use server-side caching.md` | Use server-side caching | Cache values server-side in your agent deployment using stale-while-revalidate and key-value cache APIs.；Agent Server, Deploy, Server customization, caching | [原文](<https://docs.langchain.com/langsmith/caching>) |
| `Deploy/Deploy to Cloud/Cloud platform features.md` | Cloud platform features | Cloud-only platform features for LangSmith Agent Server, including data regions, static IP addresses, payload limits, and deployment types.；Deploy, Deploy to Cloud, cloud, features, platform | [原文](<https://docs.langchain.com/langsmith/cloud-platform-features>) |
| `Deploy/Deploy to Cloud/Deploy to Cloud.md` | Deploy to Cloud | Deploy LangSmith agents to LangChain-managed Cloud infrastructure on AWS, Azure, and GCP.；Deploy, Deploy to Cloud, cloud, deploy, overview, to | [原文](<https://docs.langchain.com/langsmith/deploy-to-cloud-overview>) |
| `Deploy/Deploy to Cloud/Deployment guide/Create an Agent Server.md` | Create an Agent Server | Create an Agent Server on LangSmith Cloud from the LangSmith UI or LangGraph CLI.；Deploy, Deploy to Cloud, Deployment guide, cloud, deploy, to | [原文](<https://docs.langchain.com/langsmith/deploy-to-cloud>) |
| `Deploy/Deploy to Cloud/Deployment guide/Manage an Agent Server.md` | Manage an Agent Server | Configure the repository, branch, and automatic updates for an Agent Server on LangSmith Cloud, or delete it.；Deploy, Deploy to Cloud, Deployment guide, deployment, manage | [原文](<https://docs.langchain.com/langsmith/manage-deployment>) |
| `Deploy/Deploy to Cloud/Deployment guide/Monitor an Agent Server.md` | Monitor an Agent Server | View build logs, server logs, and metrics for an Agent Server on LangSmith Cloud.；Deploy, Deploy to Cloud, Deployment guide, deployment, monitor | [原文](<https://docs.langchain.com/langsmith/monitor-deployment>) |
| `Deploy/Deploy to Cloud/Deployment guide/Preview builds.md` | Preview builds | Create temporary preview Agent Servers for pull requests to test Agent Server changes before merging.；Deploy, Deploy to Cloud, Deployment guide, builds, preview | [原文](<https://docs.langchain.com/langsmith/preview-builds>) |
| `Deploy/Deploy to Cloud/Deployment guide/Revisions.md` | Revisions | Create and manage revisions for an Agent Server on LangSmith Cloud.；Deploy, Deploy to Cloud, Deployment guide, deployment, revisions | [原文](<https://docs.langchain.com/langsmith/deployment-revisions>) |
| `Deploy/Deploy to Cloud/Reference/Cloud Agent Server environment variables.md` | Cloud Agent Server environment variables | Environment variables supported by the LangSmith Agent Server when deployed on Cloud.；Deploy, Deploy to Cloud, Reference, cloud, env, var | [原文](<https://docs.langchain.com/langsmith/env-var-cloud>) |
| `Deploy/Deploy to Self-hosted/Configure/Agent Server metrics.md` | Agent Server metrics | Reference for Agent Server OpenTelemetry metrics on self-hosted deployments, including Agent Server UI metrics, internal metrics, and Datadog export.；Configure, Deploy, Deploy to Self-hosted, agent, hosted, metrics, self, server | [原文](<https://docs.langchain.com/langsmith/self-hosted-agent-server-metrics>) |
| `Deploy/Deploy to Self-hosted/Configure/Configure Agent Server for scale.md` | Configure Agent Server for scale | Tune the Agent Server for self-hosted deployments—write load, read load, and example Helm configurations for different load patterns.；Configure, Deploy, Deploy to Self-hosted, agent, scale, server | [原文](<https://docs.langchain.com/langsmith/agent-server-scale>) |
| `Deploy/Deploy to Self-hosted/Configure/Self-hosted platform features.md` | Self-hosted platform features | Self-hosted-only platform features for LangSmith Agent Server, including custom databases, listeners, and resource customization.；Configure, Deploy, Deploy to Self-hosted, features, hosted, platform, self | [原文](<https://docs.langchain.com/langsmith/self-hosted-platform-features>) |
| `Deploy/Deploy to Self-hosted/Configure/Set up a build machine on a restricted network.md` | Set up a build machine on a restricted network | Configure pip, uv, Python, and the LangGraph CLI to pull every package, interpreter, and image from an internal registry, then build a Python or JavaScript Agent Server image with no public internet access.；Configure, Deploy, Deploy to Self-hosted, build, host, network, restricted, self | [原文](<https://docs.langchain.com/langsmith/self-host-restricted-network-build>) |
| `Deploy/Deploy to Self-hosted/Configure/Troubleshooting for self-hosted deployments.md` | Troubleshooting for self-hosted deployments | Diagnostic steps for troubleshooting self-hosted LangSmith Agent Server issues before contacting support.；Configure, Deploy, Deploy to Self-hosted, diagnostics, hosted, self | [原文](<https://docs.langchain.com/langsmith/diagnostics-self-hosted>) |
| `Deploy/Deploy to Self-hosted/Deploy to self-hosted.md` | Deploy to self-hosted | Host LangSmith Agent Server on your own infrastructure with full control over data, networking, and resources.；Deploy, Deploy to Self-hosted, deploy, hosted, overview, self, to | [原文](<https://docs.langchain.com/langsmith/deploy-to-self-hosted-overview>) |
| `Deploy/Deploy to Self-hosted/Deploy with control plane.md` | Deploy with control plane | Build Docker images and deploy applications to a self-hosted LangSmith instance using the control plane UI.；Deploy, Deploy to Self-hosted, control, deploy, plane, with | [原文](<https://docs.langchain.com/langsmith/deploy-with-control-plane>) |
| `Deploy/Deploy to Self-hosted/Hybrid.md` | Hybrid | A LangSmith Agent Server setup where you self-host Agent Servers in your infrastructure and send traces to LangSmith Cloud or a self-hosted LangSmith instance.；Deploy, Deploy to Self-hosted, hybrid | [原文](<https://docs.langchain.com/langsmith/hybrid>) |
| `Deploy/Deploy to Self-hosted/Reference/Self-hosted Agent Server environment variables.md` | Self-hosted Agent Server environment variables | Environment variables supported by the LangSmith Agent Server when deployed on self-hosted infrastructure.；Deploy, Deploy to Self-hosted, Reference, env, hosted, self, var | [原文](<https://docs.langchain.com/langsmith/env-var-self-hosted>) |
| `Deploy/Deploy to Self-hosted/Self-host standalone servers.md` | Self-host standalone servers | Deploy standalone Agent Servers using Docker, Docker Compose, or Kubernetes without the LangSmith control plane.；Deploy, Deploy to Self-hosted, deploy, server, standalone | [原文](<https://docs.langchain.com/langsmith/deploy-standalone-server>) |
| `Deploy/Get started/Deploy your app to cloud.md` | Deploy your app to cloud | Deploy your first application to LangSmith Cloud in GCP using the LangGraph CLI.；Deploy, Get started, deployment, quickstart | [原文](<https://docs.langchain.com/langsmith/deployment-quickstart>) |
| `Deploy/Get started/Deployment components/LangSmith Agent Server components.md` | LangSmith Agent Server components | Overview of Agent Server, LangGraph CLI, Studio, SDKs, RemoteGraph, control plane, and data plane components.；Deploy, Deployment components, Get started, components | [原文](<https://docs.langchain.com/langsmith/components>) |
| `Deploy/Get started/Deployment components/LangSmith control plane.md` | LangSmith control plane | Deploy, Deployment components, Get started, control, plane | [原文](<https://docs.langchain.com/langsmith/control-plane>) |
| `Deploy/Get started/Deployment components/LangSmith data plane.md` | LangSmith data plane | [!NOTE]；Deploy, Deployment components, Get started, data, plane | [原文](<https://docs.langchain.com/langsmith/data-plane>) |
| `Deploy/Get started/Develop & test/Local development & testing.md` | Local development & testing | Compare langgraph dev and langgraph up for local development and production-like testing of Agent Server applications.；Deploy, Develop & test, Get started, dev, local, testing | [原文](<https://docs.langchain.com/langsmith/local-dev-testing>) |
| `Deploy/Get started/Frameworks and platforms/Deploy Google ADK agents.md` | Deploy Google ADK agents | Deploy Google Agent Development Kit (ADK) agents to LangSmith Agent Server using the deployments-wrap-sdk package.；Deploy, Frameworks and platforms, Get started, adk, deploy, google | [原文](<https://docs.langchain.com/langsmith/deploy-google-adk>) |
| `Deploy/Get started/Frameworks and platforms/Deploy other frameworks.md` | Deploy other frameworks | Deploy agents built with Claude Agent SDK, Strands, CrewAI, AutoGen, and other frameworks to LangSmith Agent Server.；Deploy, Frameworks and platforms, Get started, deploy, frameworks, other | [原文](<https://docs.langchain.com/langsmith/deploy-other-frameworks>) |
| `Deploy/Get started/Frameworks and platforms/Full-stack web apps/Deploy full-stack web apps.md` | Deploy full-stack web apps | Deploy LangChain agents as full-stack web apps on Next.js, SvelteKit, Nuxt, Cloudflare Workers, Deno Deploy, and Vite with streaming UI and thread history.；Deploy, Frameworks and platforms, Full-stack web apps, Get started, and, deploy, frameworks, platforms | [原文](<https://docs.langchain.com/langsmith/deploy-frameworks-and-platforms>) |
| `Deploy/Get started/Frameworks and platforms/Full-stack web apps/Deploy with Cloudflare Workers.md` | Deploy with Cloudflare Workers | Deploy a LangChain deep agent on Cloudflare Workers with Vite, React, Hono, and Durable Objects for SSE replay.；Deploy, Frameworks and platforms, Full-stack web apps, Get started, cloudflare, deploy, workers | [原文](<https://docs.langchain.com/langsmith/deploy-cloudflare-workers>) |
| `Deploy/Get started/Frameworks and platforms/Full-stack web apps/Deploy with Deno Deploy.md` | Deploy with Deno Deploy | Deploy a LangChain deep agent on Deno Deploy with Hono route handlers and a Vite React SPA served from one entrypoint.；Deploy, Frameworks and platforms, Full-stack web apps, Get started, deno, deploy | [原文](<https://docs.langchain.com/langsmith/deploy-deno>) |
| `Deploy/Get started/Frameworks and platforms/Full-stack web apps/Deploy with LangSmith and Vite.md` | Deploy with LangSmith and Vite | Deploy a LangChain deep agent to LangSmith Agent Server and stream from a Vite React chat UI on Vercel, Netlify, or Cloudflare Pages.；Deploy, Frameworks and platforms, Full-stack web apps, Get started, deploy, langsmith, vite | [原文](<https://docs.langchain.com/langsmith/deploy-vite-langsmith>) |
| `Deploy/Get started/Frameworks and platforms/Full-stack web apps/Deploy with Next.js.md` | Deploy with Next.js | Deploy a LangChain deep agent in a Next.js App Router project with streaming chat, subagents, and thread history.；Deploy, Frameworks and platforms, Full-stack web apps, Get started, deploy, nextjs | [原文](<https://docs.langchain.com/langsmith/deploy-nextjs>) |
| `Deploy/Get started/Frameworks and platforms/Full-stack web apps/Deploy with Nuxt.md` | Deploy with Nuxt | Deploy a LangChain deep agent in a Nuxt 4 app with Nitro server routes, Vue composables, and subagent-aware chat UI.；Deploy, Frameworks and platforms, Full-stack web apps, Get started, deploy, nuxt | [原文](<https://docs.langchain.com/langsmith/deploy-nuxt>) |
| `Deploy/Get started/Frameworks and platforms/Full-stack web apps/Deploy with SvelteKit.md` | Deploy with SvelteKit | Deploy a LangChain deep agent in a SvelteKit project on Cloudflare Workers with streaming chat and thread history.；Deploy, Frameworks and platforms, Full-stack web apps, Get started, deploy, sveltekit | [原文](<https://docs.langchain.com/langsmith/deploy-sveltekit>) |
| `Deploy/Get started/LangSmith Agent Server.md` | LangSmith Agent Server | Deploy and manage agents with durable execution, real-time streaming, and horizontal scaling.；Deploy, Get started, deployment | [原文](<https://docs.langchain.com/langsmith/deployment>) |
| `Deploy/Get started/Reference/Agent Server API/A2A/A2A JSON-RPC.md` | A2A JSON-RPC | Communicate with an assistant using the Agent-to-Agent (A2A) Protocol over JSON-RPC 2.0.；A2A, Agent Server API, Deploy, Get started, Reference, a2a, json, rpc | [原文](<https://docs.langchain.com/langsmith/agent-server-api/a2a/a2a-json-rpc>) |
| `Deploy/Get started/Reference/Agent Server API/Agent Server API reference.md` | Agent Server API reference | Browse the Agent Server API reference, available within each Agent Server at the /docs endpoint.；Agent Server API, Deploy, Get started, Reference, api, ref, server | [原文](<https://docs.langchain.com/langsmith/server-api-ref>) |
| `Deploy/Get started/Reference/Agent Server API/Assistants/Count Assistants.md` | Count Assistants | Get the count of assistants matching the specified criteria.；Agent Server API, Assistants, Deploy, Get started, Reference, assistants, count | [原文](<https://docs.langchain.com/langsmith/agent-server-api/assistants/count-assistants>) |
| `Deploy/Get started/Reference/Agent Server API/Assistants/Create Assistant.md` | Create Assistant | Create an assistant.；Agent Server API, Assistants, Deploy, Get started, Reference, assistant, create | [原文](<https://docs.langchain.com/langsmith/agent-server-api/assistants/create-assistant>) |
| `Deploy/Get started/Reference/Agent Server API/Assistants/Delete Assistant.md` | Delete Assistant | Delete an assistant by ID.；Agent Server API, Assistants, Deploy, Get started, Reference, assistant, delete | [原文](<https://docs.langchain.com/langsmith/agent-server-api/assistants/delete-assistant>) |
| `Deploy/Get started/Reference/Agent Server API/Assistants/Get Assistant Graph.md` | Get Assistant Graph | Get an assistant by ID.；Agent Server API, Assistants, Deploy, Get started, Reference, assistant, get, graph | [原文](<https://docs.langchain.com/langsmith/agent-server-api/assistants/get-assistant-graph>) |
| `Deploy/Get started/Reference/Agent Server API/Assistants/Get Assistant Schemas.md` | Get Assistant Schemas | Get an assistant by ID.；Agent Server API, Assistants, Deploy, Get started, Reference, assistant, get, schemas | [原文](<https://docs.langchain.com/langsmith/agent-server-api/assistants/get-assistant-schemas>) |
| `Deploy/Get started/Reference/Agent Server API/Assistants/Get Assistant Subgraphs by Namespace.md` | Get Assistant Subgraphs by Namespace | Get an assistant's subgraphs filtered by namespace.；Agent Server API, Assistants, Deploy, Get started, Reference, assistant, by, get, namespace, subgraphs | [原文](<https://docs.langchain.com/langsmith/agent-server-api/assistants/get-assistant-subgraphs-by-namespace>) |
| `Deploy/Get started/Reference/Agent Server API/Assistants/Get Assistant Subgraphs.md` | Get Assistant Subgraphs | Get an assistant's subgraphs.；Agent Server API, Assistants, Deploy, Get started, Reference, assistant, get, subgraphs | [原文](<https://docs.langchain.com/langsmith/agent-server-api/assistants/get-assistant-subgraphs>) |
| `Deploy/Get started/Reference/Agent Server API/Assistants/Get Assistant Versions.md` | Get Assistant Versions | Get all versions of an assistant.；Agent Server API, Assistants, Deploy, Get started, Reference, assistant, get, versions | [原文](<https://docs.langchain.com/langsmith/agent-server-api/assistants/get-assistant-versions>) |
| `Deploy/Get started/Reference/Agent Server API/Assistants/Get Assistant.md` | Get Assistant | Get an assistant by ID.；Agent Server API, Assistants, Deploy, Get started, Reference, assistant, get | [原文](<https://docs.langchain.com/langsmith/agent-server-api/assistants/get-assistant>) |
| `Deploy/Get started/Reference/Agent Server API/Assistants/Patch Assistant.md` | Patch Assistant | Update an assistant.；Agent Server API, Assistants, Deploy, Get started, Reference, assistant, patch | [原文](<https://docs.langchain.com/langsmith/agent-server-api/assistants/patch-assistant>) |
| `Deploy/Get started/Reference/Agent Server API/Assistants/Search Assistants.md` | Search Assistants | Search for assistants.；Agent Server API, Assistants, Deploy, Get started, Reference, assistants, search | [原文](<https://docs.langchain.com/langsmith/agent-server-api/assistants/search-assistants>) |
| `Deploy/Get started/Reference/Agent Server API/Assistants/Set Latest Assistant Version.md` | Set Latest Assistant Version | Set the latest version for an assistant.；Agent Server API, Assistants, Deploy, Get started, Reference, assistant, latest, set, version | [原文](<https://docs.langchain.com/langsmith/agent-server-api/assistants/set-latest-assistant-version>) |
| `Deploy/Get started/Reference/Agent Server API/Crons/Count Crons.md` | Count Crons | Get the count of crons matching the specified criteria.；Agent Server API, Crons, Deploy, Get started, Reference, count, crons | [原文](<https://docs.langchain.com/langsmith/agent-server-api/crons/count-crons>) |
| `Deploy/Get started/Reference/Agent Server API/Crons/Create Cron.md` | Create Cron | Create a cron to schedule runs on new threads.；Agent Server API, Crons, Deploy, Get started, Reference, create, cron | [原文](<https://docs.langchain.com/langsmith/agent-server-api/crons/create-cron>) |
| `Deploy/Get started/Reference/Agent Server API/Crons/Create Thread Cron.md` | Create Thread Cron | Create a cron to schedule runs on a thread.；Agent Server API, Crons, Deploy, Get started, Reference, create, cron, thread | [原文](<https://docs.langchain.com/langsmith/agent-server-api/crons/create-thread-cron>) |
| `Deploy/Get started/Reference/Agent Server API/Crons/Delete Cron.md` | Delete Cron | Delete a cron by ID.；Agent Server API, Crons, Deploy, Get started, Reference, cron, delete | [原文](<https://docs.langchain.com/langsmith/agent-server-api/crons/delete-cron>) |
| `Deploy/Get started/Reference/Agent Server API/Crons/Get Cron.md` | Get Cron | Get a cron by ID.；Agent Server API, Crons, Deploy, Get started, Reference, cron, get | [原文](<https://docs.langchain.com/langsmith/agent-server-api/crons/get-cron>) |
| `Deploy/Get started/Reference/Agent Server API/Crons/Search Crons.md` | Search Crons | Search all active crons；Agent Server API, Crons, Deploy, Get started, Reference, crons, search | [原文](<https://docs.langchain.com/langsmith/agent-server-api/crons/search-crons>) |
| `Deploy/Get started/Reference/Agent Server API/Crons/Update Cron.md` | Update Cron | Update a cron job by ID.；Agent Server API, Crons, Deploy, Get started, Reference, cron, update | [原文](<https://docs.langchain.com/langsmith/agent-server-api/crons/update-cron>) |
| `Deploy/Get started/Reference/Agent Server API/MCP/MCP Get.md` | MCP Get | Implemented according to the Streamable HTTP Transport specification.；Agent Server API, Deploy, Get started, MCP, Reference, get, mcp | [原文](<https://docs.langchain.com/langsmith/agent-server-api/mcp/mcp-get>) |
| `Deploy/Get started/Reference/Agent Server API/MCP/MCP Post.md` | MCP Post | Implemented according to the Streamable HTTP Transport specification.；Agent Server API, Deploy, Get started, MCP, Reference, mcp, post | [原文](<https://docs.langchain.com/langsmith/agent-server-api/mcp/mcp-post>) |
| `Deploy/Get started/Reference/Agent Server API/MCP/Terminate Session.md` | Terminate Session | Implemented according to the Streamable HTTP Transport specification.；Agent Server API, Deploy, Get started, MCP, Reference, session, terminate | [原文](<https://docs.langchain.com/langsmith/agent-server-api/mcp/terminate-session>) |
| `Deploy/Get started/Reference/Agent Server API/Stateless Runs/Create Background Run.md` | Create Background Run | Create a run and return the run ID immediately. Don't wait for the final run output.；Agent Server API, Deploy, Get started, Reference, Stateless Runs, background, create, run | [原文](<https://docs.langchain.com/langsmith/agent-server-api/stateless-runs/create-background-run>) |
| `Deploy/Get started/Reference/Agent Server API/Stateless Runs/Create Run Batch.md` | Create Run Batch | Create a batch of runs and return immediately.；Agent Server API, Deploy, Get started, Reference, Stateless Runs, batch, create, run | [原文](<https://docs.langchain.com/langsmith/agent-server-api/stateless-runs/create-run-batch>) |
| `Deploy/Get started/Reference/Agent Server API/Stateless Runs/Create Run, Stream Output.md` | Create Run, Stream Output | Create a run and stream the output.；Agent Server API, Deploy, Get started, Reference, Stateless Runs, create, output, run, stream | [原文](<https://docs.langchain.com/langsmith/agent-server-api/stateless-runs/create-run-stream-output>) |
| `Deploy/Get started/Reference/Agent Server API/Stateless Runs/Create Run, Wait for Output.md` | Create Run, Wait for Output | Create a run, wait for the final output and then return it.；Agent Server API, Deploy, Get started, Reference, Stateless Runs, create, for, output, run, wait | [原文](<https://docs.langchain.com/langsmith/agent-server-api/stateless-runs/create-run-wait-for-output>) |
| `Deploy/Get started/Reference/Agent Server API/Store/Delete an item.md` | Delete an item. | Agent Server API, Deploy, Get started, Reference, Store, an, delete, item | [原文](<https://docs.langchain.com/langsmith/agent-server-api/store/delete-an-item>) |
| `Deploy/Get started/Reference/Agent Server API/Store/List namespaces with optional match conditions.md` | List namespaces with optional match conditions. | Agent Server API, Deploy, Get started, Reference, Store, conditions, list, match, namespaces, optional, with | [原文](<https://docs.langchain.com/langsmith/agent-server-api/store/list-namespaces-with-optional-match-conditions>) |
| `Deploy/Get started/Reference/Agent Server API/Store/Retrieve a single item.md` | Retrieve a single item. | Agent Server API, Deploy, Get started, Reference, Store, a, item, retrieve, single | [原文](<https://docs.langchain.com/langsmith/agent-server-api/store/retrieve-a-single-item>) |
| `Deploy/Get started/Reference/Agent Server API/Store/Search or list items within a namespace prefix.md` | Search or list items within a namespace prefix. | Lists items ordered by last updated time. If a `query` is provided, performs a natural language search instead. Supports pagination via `limit` and `offset`, and filtering via `filter`.；Agent Server API, Deploy, Get started, Reference, Store, a, items, list, namespace, or, prefix, search, within | [原文](<https://docs.langchain.com/langsmith/agent-server-api/store/search-or-list-items-within-a-namespace-prefix>) |
| `Deploy/Get started/Reference/Agent Server API/Store/Store or update an item.md` | Store or update an item. | Agent Server API, Deploy, Get started, Reference, Store, an, item, or, store, update | [原文](<https://docs.langchain.com/langsmith/agent-server-api/store/store-or-update-an-item>) |
| `Deploy/Get started/Reference/Agent Server API/Streaming/Protocol v2 Command.md` | Protocol v2 Command | Send a single protocol command scoped to a thread. The request body is a `ProtocolCommand` envelope with a `method` (e.g. `run.start`, `input.respond`, `agent.getTree`) and method-specific `params`. The response is either a `ProtocolSuccess` (with method-specific `result`) or a `ProtocolError`.；Agent Server API, Deploy, Get started, Reference, Streaming, command, protocol, v2 | [原文](<https://docs.langchain.com/langsmith/agent-server-api/streaming/protocol-v2-command>) |
| `Deploy/Get started/Reference/Agent Server API/Streaming/Protocol v2 Event Stream (SSE).md` | Protocol v2 Event Stream (SSE) | Open a connection-scoped SSE event stream for a thread. The request body is a `ProtocolEventStreamRequest` carrying channel and namespace filters; the server replies with `Content-Type: text/event-stream` and pushes matching `ProtocolEvent` frames for the lifetime of the connection. Closing the connection unsubscribes — no state is persisted server；Agent Server API, Deploy, Get started, Reference, Streaming, event, protocol, sse, stream, v2 | [原文](<https://docs.langchain.com/langsmith/agent-server-api/streaming/protocol-v2-event-stream-sse>) |
| `Deploy/Get started/Reference/Agent Server API/System/API Documentation.md` | API Documentation | A local reference to the Agent Server API documentation.；Agent Server API, Deploy, Get started, Reference, System, api, documentation | [原文](<https://docs.langchain.com/langsmith/agent-server-api/system/api-documentation>) |
| `Deploy/Get started/Reference/Agent Server API/System/Health Check.md` | Health Check | Check the health status of the server. Optionally check database connectivity.；Agent Server API, Deploy, Get started, Reference, System, check, health | [原文](<https://docs.langchain.com/langsmith/agent-server-api/system/health-check>) |
| `Deploy/Get started/Reference/Agent Server API/System/Server Information.md` | Server Information | Get server version information, feature flags, and metadata.；Agent Server API, Deploy, Get started, Reference, System, information, server | [原文](<https://docs.langchain.com/langsmith/agent-server-api/system/server-information>) |
| `Deploy/Get started/Reference/Agent Server API/System/System Metrics.md` | System Metrics | Get system metrics in Prometheus or JSON format for monitoring and observability.；Agent Server API, Deploy, Get started, Reference, System, metrics, system | [原文](<https://docs.langchain.com/langsmith/agent-server-api/system/system-metrics>) |
| `Deploy/Get started/Reference/Agent Server API/Thread Runs/Cancel Run.md` | Cancel Run | Agent Server API, Deploy, Get started, Reference, Thread Runs, cancel, run | [原文](<https://docs.langchain.com/langsmith/agent-server-api/thread-runs/cancel-run>) |
| `Deploy/Get started/Reference/Agent Server API/Thread Runs/Cancel Runs.md` | Cancel Runs | Cancel one or more runs. Can cancel runs by thread ID and run IDs, or by status filter.；Agent Server API, Deploy, Get started, Reference, Thread Runs, cancel, runs | [原文](<https://docs.langchain.com/langsmith/agent-server-api/thread-runs/cancel-runs>) |
| `Deploy/Get started/Reference/Agent Server API/Thread Runs/Create Background Run.md` | Create Background Run | Create a run in existing thread, return the run ID immediately. Don't wait for the final run output.；Agent Server API, Deploy, Get started, Reference, Thread Runs, background, create, run | [原文](<https://docs.langchain.com/langsmith/agent-server-api/thread-runs/create-background-run>) |
| `Deploy/Get started/Reference/Agent Server API/Thread Runs/Create Run, Stream Output.md` | Create Run, Stream Output | Create a run in existing thread. Stream the output.；Agent Server API, Deploy, Get started, Reference, Thread Runs, create, output, run, stream | [原文](<https://docs.langchain.com/langsmith/agent-server-api/thread-runs/create-run-stream-output>) |
| `Deploy/Get started/Reference/Agent Server API/Thread Runs/Create Run, Wait for Output.md` | Create Run, Wait for Output | Create a run in existing thread. Wait for the final output and then return it.；Agent Server API, Deploy, Get started, Reference, Thread Runs, create, for, output, run, wait | [原文](<https://docs.langchain.com/langsmith/agent-server-api/thread-runs/create-run-wait-for-output>) |
| `Deploy/Get started/Reference/Agent Server API/Thread Runs/Delete Run.md` | Delete Run | Delete a run by ID.；Agent Server API, Deploy, Get started, Reference, Thread Runs, delete, run | [原文](<https://docs.langchain.com/langsmith/agent-server-api/thread-runs/delete-run>) |
| `Deploy/Get started/Reference/Agent Server API/Thread Runs/Get Run.md` | Get Run | Get a run by ID.；Agent Server API, Deploy, Get started, Reference, Thread Runs, get, run | [原文](<https://docs.langchain.com/langsmith/agent-server-api/thread-runs/get-run>) |
| `Deploy/Get started/Reference/Agent Server API/Thread Runs/Join Run Stream.md` | Join Run Stream | Join a run stream. This endpoint streams output in real-time from a run similar to the /threads/__THREAD_ID__/runs/stream endpoint. The stream can be resumed from the last seen event ID, or from a checkpoint of the run with `checkpoint_id`. In the in-memory runtime (`langgraph dev`), only a run created with `stream_resumable=true` can be resumed. A；Agent Server API, Deploy, Get started, Reference, Thread Runs, join, run, stream | [原文](<https://docs.langchain.com/langsmith/agent-server-api/thread-runs/join-run-stream>) |
| `Deploy/Get started/Reference/Agent Server API/Thread Runs/Join Run.md` | Join Run | Wait for a run to finish.；Agent Server API, Deploy, Get started, Reference, Thread Runs, join, run | [原文](<https://docs.langchain.com/langsmith/agent-server-api/thread-runs/join-run>) |
| `Deploy/Get started/Reference/Agent Server API/Thread Runs/List Runs.md` | List Runs | List runs for a thread.；Agent Server API, Deploy, Get started, Reference, Thread Runs, list, runs | [原文](<https://docs.langchain.com/langsmith/agent-server-api/thread-runs/list-runs>) |
| `Deploy/Get started/Reference/Agent Server API/Threads/Copy Thread.md` | Copy Thread | Create a new thread with a copy of the state and checkpoints from an existing thread.；Agent Server API, Deploy, Get started, Reference, Threads, copy, thread | [原文](<https://docs.langchain.com/langsmith/agent-server-api/threads/copy-thread>) |
| `Deploy/Get started/Reference/Agent Server API/Threads/Count Threads.md` | Count Threads | Get the count of threads matching the specified criteria.；Agent Server API, Deploy, Get started, Reference, Threads, count, threads | [原文](<https://docs.langchain.com/langsmith/agent-server-api/threads/count-threads>) |
| `Deploy/Get started/Reference/Agent Server API/Threads/Create Thread.md` | Create Thread | Create a thread.；Agent Server API, Deploy, Get started, Reference, Threads, create, thread | [原文](<https://docs.langchain.com/langsmith/agent-server-api/threads/create-thread>) |
| `Deploy/Get started/Reference/Agent Server API/Threads/Delete Thread.md` | Delete Thread | Delete a thread by ID.；Agent Server API, Deploy, Get started, Reference, Threads, delete, thread | [原文](<https://docs.langchain.com/langsmith/agent-server-api/threads/delete-thread>) |
| `Deploy/Get started/Reference/Agent Server API/Threads/Get Thread History Post.md` | Get Thread History Post | Get all past states for a thread. Can return fewer than `limit` states; page with `before` to read further.；Agent Server API, Deploy, Get started, Reference, Threads, get, history, post, thread | [原文](<https://docs.langchain.com/langsmith/agent-server-api/threads/get-thread-history-post>) |
| `Deploy/Get started/Reference/Agent Server API/Threads/Get Thread History.md` | Get Thread History | Get all past states for a thread. Can return fewer than `limit` states; page with `before` to read further.；Agent Server API, Deploy, Get started, Reference, Threads, get, history, thread | [原文](<https://docs.langchain.com/langsmith/agent-server-api/threads/get-thread-history>) |
| `Deploy/Get started/Reference/Agent Server API/Threads/Get Thread State At Checkpoint (get-thread-state-at-checkpoint-1).md` | Get Thread State At Checkpoint | Get state for a thread at a specific checkpoint.；1, Agent Server API, Deploy, Get started, Reference, Threads, at, checkpoint, get, state, thread | [原文](<https://docs.langchain.com/langsmith/agent-server-api/threads/get-thread-state-at-checkpoint-1>) |
| `Deploy/Get started/Reference/Agent Server API/Threads/Get Thread State At Checkpoint.md` | Get Thread State At Checkpoint | Get state for a thread at a specific checkpoint.；Agent Server API, Deploy, Get started, Reference, Threads, at, checkpoint, get, state, thread | [原文](<https://docs.langchain.com/langsmith/agent-server-api/threads/get-thread-state-at-checkpoint>) |
| `Deploy/Get started/Reference/Agent Server API/Threads/Get Thread State.md` | Get Thread State | Get state for a thread.；Agent Server API, Deploy, Get started, Reference, Threads, get, state, thread | [原文](<https://docs.langchain.com/langsmith/agent-server-api/threads/get-thread-state>) |
| `Deploy/Get started/Reference/Agent Server API/Threads/Get Thread Storage.md` | Get Thread Storage | Bytes the thread's checkpoints occupy in the built-in checkpointer, as stored: checkpoints, channel values (per channel) and pending writes. Returns 501 when a custom checkpointer is configured.；Agent Server API, Deploy, Get started, Reference, Threads, get, storage, thread | [原文](<https://docs.langchain.com/langsmith/agent-server-api/threads/get-thread-storage>) |
| `Deploy/Get started/Reference/Agent Server API/Threads/Get Thread.md` | Get Thread | Get a thread by ID.；Agent Server API, Deploy, Get started, Reference, Threads, get, thread | [原文](<https://docs.langchain.com/langsmith/agent-server-api/threads/get-thread>) |
| `Deploy/Get started/Reference/Agent Server API/Threads/Join Thread Stream.md` | Join Thread Stream | This endpoint streams output in real-time from a thread. The stream will include the output of each run executed sequentially on the thread and will remain open indefinitely. It is the responsibility of the calling client to close the connection.；Agent Server API, Deploy, Get started, Reference, Threads, join, stream, thread | [原文](<https://docs.langchain.com/langsmith/agent-server-api/threads/join-thread-stream>) |
| `Deploy/Get started/Reference/Agent Server API/Threads/Patch Thread.md` | Patch Thread | Update a thread.；Agent Server API, Deploy, Get started, Reference, Threads, patch, thread | [原文](<https://docs.langchain.com/langsmith/agent-server-api/threads/patch-thread>) |
| `Deploy/Get started/Reference/Agent Server API/Threads/Prune Threads.md` | Prune Threads | Prune threads by ID. The 'delete' strategy removes threads entirely. The 'keep_latest' strategy prunes old checkpoints but keeps threads and their latest state.；Agent Server API, Deploy, Get started, Reference, Threads, prune, threads | [原文](<https://docs.langchain.com/langsmith/agent-server-api/threads/prune-threads>) |
| `Deploy/Get started/Reference/Agent Server API/Threads/Search Threads.md` | Search Threads | Search for threads.；Agent Server API, Deploy, Get started, Reference, Threads, search, threads | [原文](<https://docs.langchain.com/langsmith/agent-server-api/threads/search-threads>) |
| `Deploy/Get started/Reference/Agent Server API/Threads/Update Thread State.md` | Update Thread State | Add state to a thread.；Agent Server API, Deploy, Get started, Reference, Threads, state, thread, update | [原文](<https://docs.langchain.com/langsmith/agent-server-api/threads/update-thread-state>) |
| `Deploy/Get started/Reference/Agent Server changelog.md` | Agent Server changelog | [accordion] v0.19 releases；Deploy, Get started, Reference, agent, changelog, server | [原文](<https://docs.langchain.com/langsmith/agent-server-changelog>) |
| `Deploy/Get started/Reference/Control Plane API/Control plane API reference for Agent Server hosting.md` | Control plane API reference for Agent Server hosting | Use the LangSmith control plane API to programmatically create, manage, and automate Agent Server deployments.；Control Plane API, Deploy, Get started, Reference, api, control, plane, ref | [原文](<https://docs.langchain.com/langsmith/api-ref-control-plane>) |
| `Deploy/Get started/Reference/Deployment SDK.md` | Deployment SDK | langsmith → Deployment SDK；Deploy, Get started, Reference, deployments, sdk, smith | [原文](<https://docs.langchain.com/langsmith/smith-deployments-sdk>) |
| `Deploy/Get started/Reference/LangGraph CLI.md` | LangGraph CLI | [!NOTE]；Deploy, Get started, Reference, cli | [原文](<https://docs.langchain.com/langsmith/cli>) |
| `Deploy/Get started/Reference/Reference.md` | Reference | Reference for the LangSmith Agent Server SDKs, CLI, and APIs for deploying and interacting with agents.；Deploy, Get started, Reference, deploy, overview, reference | [原文](<https://docs.langchain.com/langsmith/deploy-reference-overview>) |
| `Deploy/Get started/Reference/Related/@langchain-langgraph-sdk.md` | @langchain/langgraph-sdk | JavaScript/TypeScript package；Deploy, Get started, Reference, Related, js, langgraph, sdk, ts | [原文](<https://docs.langchain.com/langsmith/langgraph-js-ts-sdk>) |
| `Deploy/Get started/Reference/Related/langgraph_sdk.md` | langgraph_sdk | Python package；Deploy, Get started, Reference, Related, langgraph, python, sdk | [原文](<https://docs.langchain.com/langsmith/langgraph-python-sdk>) |
| `Deploy/Get started/Reference/RemoteGraph.md` | RemoteGraph | **Class** in `langgraph`；Deploy, Get started, Reference, graph, remote | [原文](<https://docs.langchain.com/langsmith/remote-graph>) |
| `Deploy/Prompt & Context Hub/Context Hub/Configure Context Hub commit webhooks.md` | Configure Context Hub commit webhooks | Send Context Hub commit events to an external HTTPS endpoint and verify that LangSmith signed each request.；Context Hub, Deploy, Prompt & Context Hub, context, hub, webhooks | [原文](<https://docs.langchain.com/langsmith/context-hub-webhooks>) |
| `Deploy/Prompt & Context Hub/Context Hub/Context engineering concepts.md` | Context engineering concepts | Core concepts for context engineering in LangSmith, including skills, agents, versioning, and sharing.；Context Hub, Deploy, Prompt & Context Hub, concepts, context, engineering | [原文](<https://docs.langchain.com/langsmith/context-engineering-concepts>) |
| `Deploy/Prompt & Context Hub/Context Hub/Manage contexts with the SDK.md` | Manage contexts with the SDK | Use the LangSmith SDK to push, pull, list, and delete agent and skill repos in the Context Hub programmatically.；Context Hub, Deploy, Prompt & Context Hub, contexts, manage, sdk | [原文](<https://docs.langchain.com/langsmith/manage-contexts-sdk>) |
| `Deploy/Prompt & Context Hub/Context Hub/Use the Context Hub.md` | Use the Context Hub | Learn how to create, view, and promote context in the LangSmith Context Hub.；Context Hub, Deploy, Prompt & Context Hub, context, hub, the, use | [原文](<https://docs.langchain.com/langsmith/use-the-context-hub>) |
| `Deploy/Prompt & Context Hub/Prompt & Context Hub.md` | Prompt & Context Hub | Store, version, and update the prompts and contexts your agents use in production.；Deploy, Prompt & Context Hub, context, hub, prompt | [原文](<https://docs.langchain.com/langsmith/prompt-context-hub>) |
| `Deploy/Prompt & Context Hub/Prompts/Connect to models/Connect to a compatible decision model provider.md` | Connect to a compatible decision model provider | Point LangSmith decision model evaluators at any server that implements the OpenAI Decisions API or the TypeSafe System One API, such as OpenRouter or a self-hosted model.；Connect to models, Deploy, Prompt & Context Hub, Prompts, compatible, decision, model, provider | [原文](<https://docs.langchain.com/langsmith/compatible-decision-model-provider>) |
| `Deploy/Prompt & Context Hub/Prompts/Connect to models/Connect to a custom model.md` | Connect to a custom model | Connect to models, Deploy, Prompt & Context Hub, Prompts, custom, endpoint | [原文](<https://docs.langchain.com/langsmith/custom-endpoint>) |
| `Deploy/Prompt & Context Hub/Prompts/Connect to models/Connect to an OpenAI compliant model provider-proxy.md` | Connect to an OpenAI compliant model provider/proxy | Connect to models, Deploy, Prompt & Context Hub, Prompts, compliant, custom, model, openai | [原文](<https://docs.langchain.com/langsmith/custom-openai-compliant-model>) |
| `Deploy/Prompt & Context Hub/Prompts/Create and manage prompts/Configure prompt settings.md` | Configure prompt settings | [!NOTE]；Create and manage prompts, Deploy, Prompt & Context Hub, Prompts, configurations, managing, model | [原文](<https://docs.langchain.com/langsmith/managing-model-configurations>) |
| `Deploy/Prompt & Context Hub/Prompts/Create and manage prompts/Create a prompt.md` | Create a prompt | [!TIP]；Create and manage prompts, Deploy, Prompt & Context Hub, Prompts, a, create, prompt | [原文](<https://docs.langchain.com/langsmith/create-a-prompt>) |
| `Deploy/Prompt & Context Hub/Prompts/Create and manage prompts/Include multimodal content in a prompt.md` | Include multimodal content in a prompt | [!NOTE]；Create and manage prompts, Deploy, Prompt & Context Hub, Prompts, content, multimodal | [原文](<https://docs.langchain.com/langsmith/multimodal-content>) |
| `Deploy/Prompt & Context Hub/Prompts/Create and manage prompts/Manage prompts programmatically.md` | Manage prompts programmatically | [!NOTE]；Create and manage prompts, Deploy, Prompt & Context Hub, Prompts, manage, programmatically, prompts | [原文](<https://docs.langchain.com/langsmith/manage-prompts-programmatically>) |
| `Deploy/Prompt & Context Hub/Prompts/Create and manage prompts/Manage prompts.md` | Manage prompts | Manage prompt versions, environments, and access controls in LangSmith.；Create and manage prompts, Deploy, Prompt & Context Hub, Prompts, manage, prompts | [原文](<https://docs.langchain.com/langsmith/manage-prompts>) |
| `Deploy/Prompt & Context Hub/Prompts/Create and manage prompts/Prompt template format guide.md` | Prompt template format guide | [!TIP]；Create and manage prompts, Deploy, Prompt & Context Hub, Prompts, format, prompt, template | [原文](<https://docs.langchain.com/langsmith/prompt-template-format>) |
| `Deploy/Prompt & Context Hub/Prompts/Create and manage prompts/Use tools in a prompt.md` | Use tools in a prompt | Create and manage prompts, Deploy, Prompt & Context Hub, Prompts, tools, use | [原文](<https://docs.langchain.com/langsmith/use-tools>) |
| `Deploy/Prompt & Context Hub/Prompts/Model providers.md` | Model providers | Configure model providers for the LangSmith Playground and LLM-as-a-judge evaluators.；Deploy, Prompt & Context Hub, Prompts, model, playground, providers | [原文](<https://docs.langchain.com/langsmith/playground-model-providers>) |
| `Deploy/Prompt & Context Hub/Prompts/Prompt engineering concepts.md` | Prompt engineering concepts | [!NOTE]；Deploy, Prompt & Context Hub, Prompts, concepts, engineering, prompt | [原文](<https://docs.langchain.com/langsmith/prompt-engineering-concepts>) |
| `Deploy/Prompt & Context Hub/Prompts/Prompt engineering quickstart.md` | Prompt engineering quickstart | [tab] UI；Deploy, Prompt & Context Hub, Prompts, engineering, prompt, quickstart | [原文](<https://docs.langchain.com/langsmith/prompt-engineering-quickstart>) |
| `Deploy/Prompt & Context Hub/Prompts/Write your prompt with AI.md` | Write your prompt with AI | [!NOTE]；Deploy, Prompt & Context Hub, Prompts, ai, prompt, with, write | [原文](<https://docs.langchain.com/langsmith/write-prompt-with-ai>) |
| `Deploy/Prompt & Context Hub/Tutorials/How to sync prompts with GitHub.md` | How to sync prompts with GitHub | [accordion] Sample Webhook Payload；Deploy, Prompt & Context Hub, Tutorials, commit, prompt | [原文](<https://docs.langchain.com/langsmith/prompt-commit>) |
| `Deploy/Prompt & Context Hub/Tutorials/Optimize a classifier.md` | Optimize a classifier | [!NOTE]；Deploy, Prompt & Context Hub, Tutorials, classifier, optimize | [原文](<https://docs.langchain.com/langsmith/optimize-classifier>) |
| `Deploy/Prompt & Context Hub/Tutorials/Test multi-turn conversations.md` | Test multi-turn conversations | Deploy, Prompt & Context Hub, Tutorials, messages, multiple | [原文](<https://docs.langchain.com/langsmith/multiple-messages>) |
| `Deploy/Sandboxes/LangSmith Sandboxes.md` | LangSmith Sandboxes | Use LangSmith managed sandboxes to safely execute code and interact with the filesystem in isolated environments.；Deploy, Sandboxes, sandboxes | [原文](<https://docs.langchain.com/langsmith/sandboxes>) |
| `Deploy/Sandboxes/Sandbox CLI.md` | Sandbox CLI | Create, inspect, connect to, and tunnel into LangSmith sandboxes from the command line.；Deploy, Sandboxes, cli, sandbox | [原文](<https://docs.langchain.com/langsmith/sandbox-cli>) |
| `Deploy/Sandboxes/Sandbox SDK usage.md` | Sandbox SDK usage | Create and manage sandboxes programmatically with the Python or TypeScript SDK.；Deploy, Sandboxes, sandbox, sdk | [原文](<https://docs.langchain.com/langsmith/sandbox-sdk>) |
| `Deploy/Sandboxes/Sandbox access permissions.md` | Sandbox access permissions | Control who in your workspace can interact with a sandbox after it has been created.；Deploy, Sandboxes, permissions, sandbox | [原文](<https://docs.langchain.com/langsmith/sandbox-permissions>) |
| `Deploy/Sandboxes/Sandbox auth proxy.md` | Sandbox auth proxy | Inject credentials into outbound requests and control which destinations a sandbox can reach.；Deploy, Sandboxes, auth, proxy, sandbox | [原文](<https://docs.langchain.com/langsmith/sandbox-auth-proxy>) |
| `Deploy/Sandboxes/Sandbox download links.md` | Sandbox download links | Share a single file from a sandbox as a link that needs no LangSmith credential.；Deploy, Sandboxes, download, links, sandbox | [原文](<https://docs.langchain.com/langsmith/sandbox-download-links>) |
| `Deploy/Sandboxes/Sandbox mounts.md` | Sandbox mounts | Mount S3 buckets, GCS buckets, public Git repositories, and Context Hub repos into LangSmith sandboxes.；Deploy, Sandboxes, mounts, sandbox | [原文](<https://docs.langchain.com/langsmith/sandbox-mounts>) |
| `Deploy/Sandboxes/Sandbox service URLs.md` | Sandbox service URLs | Access HTTP services running inside sandboxes via authenticated URLs, from a browser or programmatically.；Deploy, Sandboxes, sandbox, service, urls | [原文](<https://docs.langchain.com/langsmith/sandbox-service-urls>) |
| `Deploy/Sandboxes/Sandbox snapshots.md` | Sandbox snapshots | Build and capture reusable filesystem images for sandboxes.；Deploy, Sandboxes, sandbox, snapshots | [原文](<https://docs.langchain.com/langsmith/sandbox-snapshots>) |
| `Engine/Connect Engine to your repository.md` | Connect Engine to your repository | Connect your agent's GitHub repositories or GitLab projects to LangSmith Engine so it can read your source code when investigating issues and propose fixes as pull or merge requests.；Engine, engine, repositories | [原文](<https://docs.langchain.com/langsmith/engine-repositories>) |
| `Engine/Find and fix your agent's issues with LangSmith Engine.md` | Find and fix your agent's issues with LangSmith Engine | Review the issues LangSmith Engine detects, open pull requests with its proposed fixes, and turn failing traces into dataset examples.；Engine, engine, issues | [原文](<https://docs.langchain.com/langsmith/engine-issues>) |
| `Engine/LangSmith Engine notifications.md` | LangSmith Engine notifications | Send LangSmith Engine notifications to Slack, Jira Automation, and webhook endpoints.；Engine, engine, notifications | [原文](<https://docs.langchain.com/langsmith/engine-notifications>) |
| `Engine/LangSmith Engine security.md` | LangSmith Engine security | How LangSmith Engine handles your data, the GitHub, GitLab, and model subprocessor controls that govern its access, and its compliance posture.；Engine, engine, security | [原文](<https://docs.langchain.com/langsmith/engine-security>) |
| `Engine/LangSmith Engine.md` | LangSmith Engine | LangSmith Engine is the agent for agent engineering, turning production traces into tracked issues, fixes, and datasets across the development lifecycle.；Engine, engine | [原文](<https://docs.langchain.com/langsmith/engine>) |
| `Engine/Proactively identify issues with Red Teaming.md` | Proactively identify issues with Red Teaming | Test a deployed agent with synthetic LangSmith Engine probes to find prompt injection, data exposure, and unsafe tool use before they reach production.；Engine, engine, red, teaming | [原文](<https://docs.langchain.com/langsmith/engine-red-teaming>) |
| `Engine/Self-hosted and BYOC/Configure GitHub for Engine on self-hosted and BYOC.md` | Configure GitHub for Engine on self-hosted and BYOC | Register a GitHub App and configure self-hosted LangSmith or a BYOC data plane so LangSmith Engine can read repositories and open pull requests, on GitHub.com, Enterprise Cloud with data residency, or Enterprise Server.；Engine, Self-hosted and BYOC, engine, github, hosted, self | [原文](<https://docs.langchain.com/langsmith/engine-self-hosted-github>) |
| `Engine/Self-hosted and BYOC/Configure model providers for Engine on self-hosted and BYOC.md` | Configure model providers for Engine on self-hosted and BYOC | Choose the model providers LangSmith Engine uses on a self-hosted LangSmith instance, authenticate with credentials or cloud identity, and keep model traffic on private networking.；Engine, Self-hosted and BYOC, engine, hosted, model, providers, self | [原文](<https://docs.langchain.com/langsmith/engine-self-hosted-model-providers>) |
| `Engine/Self-hosted and BYOC/LangSmith Engine on Self-hosted and BYOC.md` | LangSmith Engine on Self-hosted and BYOC | Set up LangSmith Engine on a self-hosted LangSmith instance or a BYOC data plane, including model provider options and external network requirements.；Engine, Self-hosted and BYOC, engine, hosted, self | [原文](<https://docs.langchain.com/langsmith/engine-self-hosted>) |
| `Engine/Set up LangSmith Engine.md` | Set up LangSmith Engine | Enable LangSmith Engine for your organization, turn it on for a tracing project, and configure what it analyzes.；Engine, engine, setup | [原文](<https://docs.langchain.com/langsmith/engine-setup>) |
| `Engine/Validate fixes automatically.md` | Validate fixes automatically | Confirm that a LangSmith Engine issue reproduces on your deployment, and that Engine's fix resolves it, by replaying the issue's traces.；Engine, engine, fix, validation | [原文](<https://docs.langchain.com/langsmith/engine-fix-validation>) |
| `LLM Gateway/Authentication/Authenticate to the LLM Gateway.md` | Authenticate to the LLM Gateway | Choose a LangSmith API key for LLM Gateway requests, grant it permission to call the gateway, send it from your client, and fix authentication errors.；Authentication, LLM Gateway, authentication, gateway, llm | [原文](<https://docs.langchain.com/langsmith/llm-gateway-authentication>) |
| `LLM Gateway/Authentication/Provider authentication.md` | Provider authentication | Choose how the LLM Gateway authenticates to each model provider, add provider keys as workspace secrets, and fix provider credential errors.；Authentication, LLM Gateway, authentication, gateway, llm, provider | [原文](<https://docs.langchain.com/langsmith/llm-gateway-provider-authentication>) |
| `LLM Gateway/Call the gateway/API formats.md` | API formats | Use OpenAI Chat Completions, Anthropic Messages, or OpenAI Responses requests to call models across providers through the LLM Gateway.；Call the gateway, LLM Gateway, api, formats, gateway, llm | [原文](<https://docs.langchain.com/langsmith/llm-gateway-api-formats>) |
| `LLM Gateway/Call the gateway/Decision models.md` | Decision models | Call TypeSafe and OpenAI decision models through the LangSmith LLM Gateway using the System One API or the OpenAI Decisions API.；Call the gateway, LLM Gateway, decision, gateway, llm, models | [原文](<https://docs.langchain.com/langsmith/llm-gateway-decision-models>) |
| `LLM Gateway/Call the gateway/Direct model access.md` | Direct model access | Access provider APIs directly through provider-specific LLM Gateway paths without using the gateway standardization layer.；Call the gateway, LLM Gateway, access, direct, gateway, llm, model | [原文](<https://docs.langchain.com/langsmith/llm-gateway-direct-model-access>) |
| `LLM Gateway/Call the gateway/Set up coding agents.md` | Set up coding agents | Configure Claude Code, Codex, Gemini CLI, and Deep Agents Code to route LLM calls through the LLM Gateway.；Call the gateway, LLM Gateway, agents, coding, gateway, llm | [原文](<https://docs.langchain.com/langsmith/llm-gateway-coding-agents>) |
| `LLM Gateway/Get started/How the LLM Gateway works.md` | How the LLM Gateway works | Understand what the LLM Gateway does to each request, how upstream credentials are resolved, and where the gateway is available.；Get started, LLM Gateway, gateway, how, it, llm, works | [原文](<https://docs.langchain.com/langsmith/llm-gateway-how-it-works>) |
| `LLM Gateway/Get started/LLM Gateway.md` | LLM Gateway | Route model calls from your agents through one LangSmith endpoint, with each call traced in LangSmith and governed by your organization's policies.；Get started, LLM Gateway, gateway, llm | [原文](<https://docs.langchain.com/langsmith/llm-gateway>) |
| `LLM Gateway/Get started/Send your first LLM Gateway request.md` | Send your first LLM Gateway request | Send your first request through the LLM Gateway from the Simulator, call the gateway from your code, and view the request's trace.；Get started, LLM Gateway, first, gateway, llm, request | [原文](<https://docs.langchain.com/langsmith/llm-gateway-first-request>) |
| `LLM Gateway/Get started/Set up the LLM Gateway.md` | Set up the LLM Gateway | Set up the LLM Gateway for your organization by adding provider keys, granting permission to call the gateway, issuing API keys, and setting governance policies.；Get started, LLM Gateway, admin, gateway, llm, setup | [原文](<https://docs.langchain.com/langsmith/llm-gateway-admin-setup>) |
| `LLM Gateway/Governance/Data policies.md` | Data policies | Create data policies that redact sensitive data and control trace content in the LLM Gateway.；Governance, LLM Gateway, data, gateway, llm, policy | [原文](<https://docs.langchain.com/langsmith/llm-gateway-data-policy>) |
| `LLM Gateway/Governance/Header-based policies.md` | Header-based policies | Scope gateway spend caps, rate limits, and model access by a custom request header, such as a customer, tenant, or cost center identifier, without issuing a separate API key for each value.；Governance, LLM Gateway, gateway, header, llm, policies | [原文](<https://docs.langchain.com/langsmith/llm-gateway-header-policies>) |
| `LLM Gateway/Governance/Model access policies.md` | Model access policies | Control which model providers and models are accessible through the LLM Gateway for your organization, workspaces, users, or API keys.；Governance, LLM Gateway, access, gateway, llm, model, policies | [原文](<https://docs.langchain.com/langsmith/llm-gateway-model-access-policies>) |
| `LLM Gateway/Governance/Rate limit policies.md` | Rate limit policies | Limit the number of requests or tokens an organization, workspace, user, or API key can send through the LLM Gateway in a rolling time window.；Governance, LLM Gateway, gateway, limit, llm, policies, rate | [原文](<https://docs.langchain.com/langsmith/llm-gateway-rate-limit-policies>) |
| `LLM Gateway/Governance/Spend policies.md` | Spend policies | Set cost limits on LLM usage across your organization and prevent runaway spend before it reaches providers.；Governance, LLM Gateway, gateway, llm, policies, spend | [原文](<https://docs.langchain.com/langsmith/llm-gateway-spend-policies>) |
| `LLM Gateway/Models and reliability/Custom model configurations.md` | Custom model configurations | Call saved model configurations through the LLM Gateway to reach custom endpoints and use them in fallback chains.；LLM Gateway, Models and reliability, configurations, gateway, llm, model | [原文](<https://docs.langchain.com/langsmith/llm-gateway-model-configurations>) |
| `LLM Gateway/Models and reliability/Gateway Credits.md` | Gateway Credits | Use Gateway Credits to access models without a provider key, just authenticate with LangSmith.；LLM Gateway, Models and reliability, credits, gateway, llm | [原文](<https://docs.langchain.com/langsmith/llm-gateway-credits>) |
| `LLM Gateway/Models and reliability/Model fallbacks.md` | Model fallbacks | Automatically retry a request against backup models when the primary model rate-limits, errors, or returns another configured status code.；LLM Gateway, Models and reliability, fallbacks, gateway, llm | [原文](<https://docs.langchain.com/langsmith/llm-gateway-fallbacks>) |
| `LLM Gateway/Observability/Monitor LLM Gateway spend.md` | Monitor LLM Gateway spend | View and analyze LLM Gateway costs by user, API key, model, provider, and request header.；LLM Gateway, Observability, gateway, llm, monitoring | [原文](<https://docs.langchain.com/langsmith/llm-gateway-monitoring>) |
| `LLM Gateway/Observability/View LLM Gateway traces.md` | View LLM Gateway traces | Find LLM Gateway traces, read their policy and cost metadata, triage policy violations in LangSmith Engine, and control who can see gateway traces.；LLM Gateway, Observability, gateway, llm, traces | [原文](<https://docs.langchain.com/langsmith/llm-gateway-traces>) |
| `LangSmith setup/Account/Account.md` | Account | Set up your LangSmith account, including API keys, profile configuration, integrations, and pricing tiers.；Account, LangSmith setup, admin | [原文](<https://docs.langchain.com/langsmith/admin>) |
| `LangSmith setup/Account/Billing & usage/Granular billable usage.md` | Granular billable usage | Retrieve detailed trace and Agent Server usage data broken down by workspace, project, user, or API key.；Account, Billing & usage, LangSmith setup, granular, usage | [原文](<https://docs.langchain.com/langsmith/granular-usage>) |
| `LangSmith setup/Account/Billing & usage/Manage billing in your account.md` | Manage billing in your account | [!NOTE]；Account, Billing & usage, LangSmith setup, billing | [原文](<https://docs.langchain.com/langsmith/billing>) |
| `LangSmith setup/Account/Billing & usage/View usage.md` | View usage | What usage data is available in LangSmith, what each metric means, and what differs for Self-hosted.；Account, Billing & usage, LangSmith setup, usage, view | [原文](<https://docs.langchain.com/langsmith/view-usage>) |
| `LangSmith setup/Account/Create an account and API key.md` | Create an account and API key | [!TIP]；Account, LangSmith setup, account, api, create, key | [原文](<https://docs.langchain.com/langsmith/create-account-api-key>) |
| `LangSmith setup/Account/LangSmith for Enterprise.md` | LangSmith for Enterprise | Hosting options, access control, data privacy, cost controls, and security compliance for Enterprise users.；Account, LangSmith setup, enterprise | [原文](<https://docs.langchain.com/langsmith/enterprise>) |
| `LangSmith setup/Account/Profile configuration.md` | Profile configuration | Configure LangSmith SDK credentials and endpoints with a local profile file.；Account, LangSmith setup, configuration, profile | [原文](<https://docs.langchain.com/langsmith/profile-configuration>) |
| `LangSmith setup/BYOC/AWS/AWS data plane cost estimate.md` | AWS data plane cost estimate | Rough AWS cost of a LangSmith BYOC data plane running SmithDB, with a legacy estimate for data planes created with ClickHouse.；AWS, BYOC, LangSmith setup, aws, byoc, cost, data, plane | [原文](<https://docs.langchain.com/langsmith/byoc-data-plane-cost-aws>) |
| `LangSmith setup/BYOC/AWS/BYOC architecture.md` | BYOC architecture | How a LangSmith BYOC deployment is structured across the LangChain control plane and the data plane in your AWS account.；AWS, BYOC, LangSmith setup, architecture, aws, byoc | [原文](<https://docs.langchain.com/langsmith/byoc-architecture-aws>) |
| `LangSmith setup/BYOC/AWS/BYOC billing.md` | BYOC billing | How LangSmith BYOC is billed across your AWS account and your LangSmith contract, which AWS services carry cost, and the account quotas to check before you deploy.；AWS, BYOC, LangSmith setup, aws, billing, byoc | [原文](<https://docs.langchain.com/langsmith/byoc-billing-aws>) |
| `LangSmith setup/BYOC/AWS/BYOC onboarding.md` | BYOC onboarding | Set up a LangSmith BYOC data plane, from enabling BYOC on your organization to creating workspaces and connecting privately.；AWS, BYOC, LangSmith setup, aws, byoc, onboarding | [原文](<https://docs.langchain.com/langsmith/byoc-onboarding-aws>) |
| `LangSmith setup/BYOC/AWS/BYOC operations.md` | BYOC operations | How LangChain upgrades, patches, and maintains a LangSmith BYOC data plane, and when maintenance requires a scheduled window.；AWS, BYOC, LangSmith setup, aws, byoc, operations | [原文](<https://docs.langchain.com/langsmith/byoc-operations-aws>) |
| `LangSmith setup/BYOC/AWS/Bring your own IAM roles (AWS).md` | Bring your own IAM roles (AWS) | Create customer-managed IAM roles for LangSmith BYOC, remove IAM management permissions from the provisioning role, and deploy with existing roles.；AWS, BYOC, LangSmith setup, aws, byoc, byoiam | [原文](<https://docs.langchain.com/langsmith/byoc-byoiam-aws>) |
| `LangSmith setup/BYOC/AWS/Bring your own VPC on AWS.md` | Bring your own VPC on AWS | Create a customer-managed VPC for LangSmith BYOC, configure a reduced-permission IAM role, and supply your VPC and subnet IDs.；AWS, BYOC, LangSmith setup, aws, byoc, byovpc | [原文](<https://docs.langchain.com/langsmith/byoc-byovpc-aws>) |
| `LangSmith setup/BYOC/AWS/Bring your own keys (CMK).md` | Bring your own keys (CMK) | Encrypt a new LangSmith BYOC data plane on AWS with your own AWS KMS keys, using one key for every service or a separate key per service.；AWS, BYOC, LangSmith setup, aws, byoc, byok | [原文](<https://docs.langchain.com/langsmith/byoc-byok-aws>) |
| `LangSmith setup/BYOC/Azure/Azure data plane cost estimate.md` | Azure data plane cost estimate | Rough Azure infrastructure cost of a LangSmith BYOC data plane running SmithDB, with example node counts, sandboxes excluded, and additional charges.；Azure, BYOC, LangSmith setup, azure, byoc, cost, data, plane | [原文](<https://docs.langchain.com/langsmith/byoc-data-plane-cost-azure>) |
| `LangSmith setup/BYOC/Azure/BYOC architecture on Azure.md` | BYOC architecture on Azure | What LangSmith BYOC deploys in your Azure subscription, how the data plane connects to the LangChain control plane, the access LangSmith gets, and how your data is protected.；Azure, BYOC, LangSmith setup, architecture, azure, byoc | [原文](<https://docs.langchain.com/langsmith/byoc-architecture-azure>) |
| `LangSmith setup/BYOC/Azure/BYOC onboarding on Azure.md` | BYOC onboarding on Azure | Set up a LangSmith BYOC data plane in your Azure subscription, from granting LangSmith access to a resource group to creating, changing, and deleting the data plane.；Azure, BYOC, LangSmith setup, azure, byoc, onboarding | [原文](<https://docs.langchain.com/langsmith/byoc-onboarding-azure>) |
| `LangSmith setup/BYOC/Azure/BYOC operations on Azure.md` | BYOC operations on Azure | How LangChain scales, upgrades, and maintains a LangSmith BYOC data plane on Azure, including instance sizes, maintenance windows, and auditing.；Azure, BYOC, LangSmith setup, azure, byoc, operations | [原文](<https://docs.langchain.com/langsmith/byoc-operations-azure>) |
| `LangSmith setup/BYOC/BYOC FAQ.md` | BYOC FAQ | Answers to common questions about LangSmith BYOC, covering data residency, access, setup, the data plane model, and ongoing operations.；BYOC, LangSmith setup, byoc, faq | [原文](<https://docs.langchain.com/langsmith/byoc-faq>) |
| `LangSmith setup/BYOC/BYOC shared responsibility model.md` | BYOC shared responsibility model | How LangChain and your organization divide responsibility for a LangSmith BYOC deployment across operations, security, support, and compliance.；BYOC, LangSmith setup, byoc, responsibility, shared | [原文](<https://docs.langchain.com/langsmith/byoc-shared-responsibility>) |
| `LangSmith setup/BYOC/BYOC usage.md` | BYOC usage | Route tracing and API traffic to a LangSmith BYOC data plane, including tracing to multiple endpoints and the path prefixes for each service.；BYOC, LangSmith setup, byoc, usage | [原文](<https://docs.langchain.com/langsmith/byoc-usage>) |
| `LangSmith setup/BYOC/Bring Your Own Cloud (BYOC).md` | Bring Your Own Cloud (BYOC) | Deploy LangSmith services and store data in your own cloud environment while LangChain operates, scales, and upgrades the infrastructure.；BYOC, LangSmith setup, byoc | [原文](<https://docs.langchain.com/langsmith/byoc>) |
| `LangSmith setup/BYOC/GCP/BYOC architecture on GCP.md` | BYOC architecture on GCP | What LangSmith BYOC deploys in your GCP project, how the data plane connects to the LangChain control plane, and the access LangSmith gets in your project.；BYOC, GCP, LangSmith setup, architecture, byoc, gcp | [原文](<https://docs.langchain.com/langsmith/byoc-architecture-gcp>) |
| `LangSmith setup/BYOC/GCP/BYOC onboarding on GCP.md` | BYOC onboarding on GCP | Set up a LangSmith BYOC data plane in your GCP project, from the provisioner service account to creating, changing, and deleting the data plane with the API.；BYOC, GCP, LangSmith setup, byoc, gcp, onboarding | [原文](<https://docs.langchain.com/langsmith/byoc-onboarding-gcp>) |
| `LangSmith setup/BYOC/Migrate to BYOC.md` | Migrate to BYOC | Copy users, datasets, prompts, experiments, Fleet resources, and other data from an existing LangSmith instance into a BYOC data plane.；BYOC, LangSmith setup, byoc, migration | [原文](<https://docs.langchain.com/langsmith/byoc-migration>) |
| `LangSmith setup/BYOC/Why BYOC.md` | Why BYOC | Compare LangSmith BYOC with self-hosted LangSmith to decide which deployment model fits your organization.；BYOC, LangSmith setup, byoc, why | [原文](<https://docs.langchain.com/langsmith/byoc-why>) |
| `LangSmith setup/Cloud/Cloud (SaaS).md` | Cloud (SaaS) | Learn how LangChain hosts and operates LangSmith Cloud, including its regions, data storage locations, architecture, IP allowlists, private connectivity, and API rate limits.；Cloud, LangSmith setup, cloud | [原文](<https://docs.langchain.com/langsmith/cloud>) |
| `LangSmith setup/Cloud/Reference/API and SDK deprecation policy.md` | API and SDK deprecation policy | How LangSmith deprecates and removes API endpoints and SDK methods in cloud and self-hosted deployments.；Cloud, LangSmith setup, Reference, deprecation, endpoint | [原文](<https://docs.langchain.com/langsmith/endpoint-deprecation>) |
| `LangSmith setup/Cloud/Reference/LangSmith Cloud changelog.md` | LangSmith Cloud changelog | Weekly updates to LangSmith Cloud；Cloud, LangSmith setup, Reference, changelog | [原文](<https://docs.langchain.com/langsmith/changelog>) |
| `LangSmith setup/Cloud/Reference/Release stages.md` | Release stages | How LangSmith labels features as alpha, beta, or generally available, and what each stage means for stability, support, and availability；Cloud, LangSmith setup, Reference, release, stages | [原文](<https://docs.langchain.com/langsmith/release-stages>) |
| `LangSmith setup/Govern/Additional resources/FAQ/Frequently asked questions.md` | Frequently asked questions | Additional resources, FAQ, Govern, LangSmith setup, faq | [原文](<https://docs.langchain.com/langsmith/faq>) |
| `LangSmith setup/Govern/Additional resources/FAQ/Regions FAQ.md` | Regions FAQ | [!NOTE]；Additional resources, FAQ, Govern, LangSmith setup, faq, regions | [原文](<https://docs.langchain.com/langsmith/regions-faq>) |
| `LangSmith setup/Govern/Auditing/Audit logs.md` | Audit logs | Track and review administrative actions across your LangSmith organization for security, compliance, and operational visibility.；Auditing, Govern, LangSmith setup, audit, logs | [原文](<https://docs.langchain.com/langsmith/audit-logs>) |
| `LangSmith setup/Govern/Data & compliance/Data purging for compliance.md` | Data purging for compliance | [!NOTE]；Data & compliance, Govern, LangSmith setup, compliance, data, purging | [原文](<https://docs.langchain.com/langsmith/data-purging-compliance>) |
| `LangSmith setup/Govern/Data & compliance/Data storage and privacy.md` | Data storage and privacy | [!NOTE]；Data & compliance, Govern, LangSmith setup, and, data, privacy, storage | [原文](<https://docs.langchain.com/langsmith/data-storage-and-privacy>) |
| `LangSmith setup/Govern/Data & compliance/LangSmith shared responsibility model.md` | LangSmith shared responsibility model | Overview of how LangChain and customers share security responsibilities for the LangSmith platform.；Data & compliance, Govern, LangSmith setup, model, responsibility, shared | [原文](<https://docs.langchain.com/langsmith/shared-responsibility-model>) |
| `LangSmith setup/Govern/Data & compliance/Scalability & resilience.md` | Scalability & resilience | Data & compliance, Govern, LangSmith setup, and, resilience, scalability | [原文](<https://docs.langchain.com/langsmith/scalability-and-resilience>) |
| `LangSmith setup/Govern/Govern.md` | Govern | Administer users, access control, organizational structure, and compliance policies for your LangSmith organization.；Govern, LangSmith setup, govern, overview | [原文](<https://docs.langchain.com/langsmith/govern-overview>) |
| `LangSmith setup/Govern/Organization/Manage LangSmith with Terraform.md` | Manage LangSmith with Terraform | Use the official LangSmith Terraform provider to manage workspaces, access controls, resource tags, evaluators, run rules, and alert rules as code.；Govern, LangSmith setup, Organization, manage, terraform, with | [原文](<https://docs.langchain.com/langsmith/manage-with-terraform>) |
| `LangSmith setup/Govern/Organization/Manage your organization using the API.md` | Manage your organization using the API | [!TIP]；Govern, LangSmith setup, Organization, api, by, manage, organization | [原文](<https://docs.langchain.com/langsmith/manage-organization-by-api>) |
| `LangSmith setup/Govern/Organization/Overview.md` | Overview | Learn how LangSmith organizes organizations, workspaces, and resources, and how API keys, roles, data retention, rate limits, and usage limits work.；Govern, LangSmith setup, Organization, administration, overview | [原文](<https://docs.langchain.com/langsmith/administration-overview>) |
| `LangSmith setup/Govern/Organization/Relays.md` | Relays | Send a sandbox's outbound connections to hosts you choose through a connector in your network, so they reach private services and leave from your network's IP address.；Govern, LangSmith setup, Organization, relays | [原文](<https://docs.langchain.com/langsmith/relays>) |
| `LangSmith setup/Govern/Organization/Tunnels.md` | Tunnels | Reach services on your private network from LangSmith through an outbound-only connector, without exposing them to the public internet.；Govern, LangSmith setup, Organization, tunnels | [原文](<https://docs.langchain.com/langsmith/tunnels>) |
| `LangSmith setup/Govern/Organization/Workspace setup/How agent-based workspaces differ.md` | How agent-based workspaces differ | What changes when a workspace moves from organizing traces by tracing project to organizing them by agent and environment.；Govern, LangSmith setup, Organization, Workspace setup, agent, based, migrate, to, workspaces | [原文](<https://docs.langchain.com/langsmith/migrate-to-agent-based-workspaces>) |
| `LangSmith setup/Govern/Organization/Workspace setup/Manage model configurations.md` | Manage model configurations | Manage model configurations and control their availability across LangSmith features.；Govern, LangSmith setup, Organization, Workspace setup, configurations, model | [原文](<https://docs.langchain.com/langsmith/model-configurations>) |
| `LangSmith setup/Govern/Organization/Workspace setup/Set up hierarchy.md` | Set up hierarchy | [!TIP]；Govern, LangSmith setup, Organization, Workspace setup, hierarchy, set, up | [原文](<https://docs.langchain.com/langsmith/set-up-hierarchy>) |
| `LangSmith setup/Govern/Organization/Workspace setup/Set up resource tags.md` | Set up resource tags | Create and manage resource tags to organize projects, datasets, prompts, and other resources within a LangSmith workspace.；Govern, LangSmith setup, Organization, Workspace setup, resource, set, tags, up | [原文](<https://docs.langchain.com/langsmith/set-up-resource-tags>) |
| `LangSmith setup/Govern/Organization/Workspace setup/Workload isolation.md` | Workload isolation | [!TIP]；Govern, LangSmith setup, Organization, Workspace setup, isolation, workload | [原文](<https://docs.langchain.com/langsmith/workload-isolation>) |
| `LangSmith setup/Govern/Tools/LangSmith CLI.md` | LangSmith CLI | Query and manage agent traces, runs, datasets, evaluators, experiments, insights, and threads from the terminal；Govern, LangSmith setup, Tools, cli, langsmith | [原文](<https://docs.langchain.com/langsmith/langsmith-cli>) |
| `LangSmith setup/Govern/Tools/LangSmith skills.md` | LangSmith skills | Use Agent Skills to work with LangSmith traces, datasets, and evaluators from your coding agent.；Govern, LangSmith setup, Tools, skills | [原文](<https://docs.langchain.com/langsmith/skills>) |
| `LangSmith setup/Govern/Users & access control/Attribute-based access control.md` | Attribute-based access control | Grant or restrict access to LangSmith resources based on resource tags and root run metadata, using access policies that build on role-based access control.；Govern, LangSmith setup, Users & access control, abac | [原文](<https://docs.langchain.com/langsmith/abac>) |
| `LangSmith setup/Govern/Users & access control/Authentication methods.md` | Authentication methods | [!WARNING]；Govern, LangSmith setup, Users & access control, authentication, methods | [原文](<https://docs.langchain.com/langsmith/authentication-methods>) |
| `LangSmith setup/Govern/Users & access control/Manage user access in SSO organizations.md` | Manage user access in SSO organizations | [tab] UI；Govern, LangSmith setup, Users & access control, invite, jit, sso | [原文](<https://docs.langchain.com/langsmith/jit-invite-sso>) |
| `LangSmith setup/Govern/Users & access control/Organization and workspace operations reference.md` | Organization and workspace operations reference | [!NOTE]；Govern, LangSmith setup, Users & access control, operations, organization, workspace | [原文](<https://docs.langchain.com/langsmith/organization-workspace-operations>) |
| `LangSmith setup/Govern/Users & access control/Role-based access control.md` | Role-based access control | [!NOTE]；Govern, LangSmith setup, Users & access control, rbac | [原文](<https://docs.langchain.com/langsmith/rbac>) |
| `LangSmith setup/Govern/Users & access control/Teams.md` | Teams | Group organization members into teams, then give each team a role and access policies in the workspaces it can access.；Govern, LangSmith setup, Users & access control, teams | [原文](<https://docs.langchain.com/langsmith/teams>) |
| `LangSmith setup/Govern/Users & access control/User management.md` | User management | Configure role-based access control, SAML SSO, and SCIM user provisioning for your LangSmith organization.；Govern, LangSmith setup, Users & access control, management, user | [原文](<https://docs.langchain.com/langsmith/user-management>) |
| `LangSmith setup/Overview/Agent-based workspaces/Agent Registry.md` | Agent Registry | What LangSmith Agent Registry is, what an agent is, how environments divide an agent's traces, and how an identifier differs from a display name.；Agent-based workspaces, LangSmith setup, Overview, agent, registry | [原文](<https://docs.langchain.com/langsmith/agent-registry>) |
| `LangSmith setup/Overview/Agent-based workspaces/Agent environments.md` | Agent environments | How an agent's environments divide its traces, how to select one, and which parts of the set are fixed.；Agent-based workspaces, LangSmith setup, Overview, agent, environments | [原文](<https://docs.langchain.com/langsmith/agent-environments>) |
| `LangSmith setup/Overview/Agent-based workspaces/Create an agent.md` | Create an agent | Register an agent before tracing, choose its identifier, and configure an environment with the UI, Python SDK, or REST API.；Agent-based workspaces, LangSmith setup, Overview, agent, an, create | [原文](<https://docs.langchain.com/langsmith/create-an-agent>) |
| `LangSmith setup/Overview/Agent-based workspaces/Deploy to an agent environment.md` | Deploy to an agent environment | How the LangGraph and Managed Deep Agents CLIs bind a deployment to an agent and an environment, which values each flag takes, and which CLI versions accept them.；Agent-based workspaces, LangSmith setup, Overview, agent, deploy, environment, to | [原文](<https://docs.langchain.com/langsmith/deploy-to-agent-environment>) |
| `LangSmith setup/Overview/Agent-based workspaces/Navigate agents.md` | Navigate agents | How the agent switcher moves between the agent list and a single agent, which sections need an agent, and what the agent Overview shows.；Agent-based workspaces, LangSmith setup, Overview, agents, navigate | [原文](<https://docs.langchain.com/langsmith/navigate-agents>) |
| `LangSmith setup/Overview/Hosting/Set up LangSmith.md` | Set up LangSmith | Host and manage LangSmith infrastructure for observability, evaluation, and prompt engineering.；Hosting, LangSmith setup, Overview, platform, setup | [原文](<https://docs.langchain.com/langsmith/platform-setup>) |
| `LangSmith setup/Overview/LangSmith setup.md` | LangSmith setup | How a LangSmith workspace is organized, where LangSmith runs, and who can do what across your organization.；LangSmith setup, Overview, langsmith, overview, setup | [原文](<https://docs.langchain.com/langsmith/langsmith-setup-overview>) |
| `LangSmith setup/Self-hosted/Configure an instance/Authenticate Vertex AI with GKE workload identity.md` | Authenticate Vertex AI with GKE workload identity | Configure keyless Vertex AI authentication for Playground, Chat, and Insights on self-hosted LangSmith running on GKE.；Configure an instance, LangSmith setup, Self-hosted, ai, gke, host, identity, self, vertex, workload | [原文](<https://docs.langchain.com/langsmith/self-host-gke-vertex-ai-workload-identity>) |
| `LangSmith setup/Self-hosted/Configure an instance/Configure LangSmith for scale.md` | Configure LangSmith for scale | Scale a self-hosted LangSmith instance for trace ingestion, evaluation workloads, and concurrent users, with example configurations for different load patterns.；Configure an instance, LangSmith setup, Self-hosted, host, scale, self | [原文](<https://docs.langchain.com/langsmith/self-host-scale>) |
| `LangSmith setup/Self-hosted/Configure an instance/Configure environment variables in the Helm chart.md` | Configure environment variables in the Helm chart | How to use commonEnv and extraEnv to configure environment variables across LangSmith services in the Helm chart.；Configure an instance, LangSmith setup, Self-hosted, environment, host, self, variables | [原文](<https://docs.langchain.com/langsmith/self-host-environment-variables>) |
| `LangSmith setup/Self-hosted/Configure an instance/Create an Ingress for installations (Kubernetes).md` | Create an Ingress for installations (Kubernetes) | [!WARNING]；Configure an instance, LangSmith setup, Self-hosted, host, ingress, self | [原文](<https://docs.langchain.com/langsmith/self-host-ingress>) |
| `LangSmith setup/Self-hosted/Configure an instance/Customize the UI.md` | Customize the UI | Customize your LangSmith self-hosted deployment.；Configure an instance, LangSmith setup, Self-hosted, customization, host, self, ui | [原文](<https://docs.langchain.com/langsmith/self-host-ui-customization>) |
| `LangSmith setup/Self-hosted/Configure an instance/Egress for billing and operational telemetry.md` | Egress for billing and operational telemetry | [!NOTE]；Configure an instance, LangSmith setup, Self-hosted, egress, host, self | [原文](<https://docs.langchain.com/langsmith/self-host-egress>) |
| `LangSmith setup/Self-hosted/Configure an instance/Enable TTL and data retention.md` | Enable TTL and data retention | [!NOTE]；Configure an instance, LangSmith setup, Self-hosted, host, self, ttl | [原文](<https://docs.langchain.com/langsmith/self-host-ttl>) |
| `LangSmith setup/Self-hosted/Configure an instance/FIPS-compliant images.md` | FIPS-compliant images | Run self-hosted LangSmith installation on FIPS 140 compliant container images；Configure an instance, LangSmith setup, Self-hosted, fips, host, self | [原文](<https://docs.langchain.com/langsmith/self-host-fips>) |
| `LangSmith setup/Self-hosted/Configure an instance/Mirror images for your LangSmith installation.md` | Mirror images for your LangSmith installation | [!TIP]；Configure an instance, LangSmith setup, Self-hosted, host, images, mirroring, self | [原文](<https://docs.langchain.com/langsmith/self-host-mirroring-images>) |
| `LangSmith setup/Self-hosted/Configure an instance/Set up the LLM auth proxy.md` | Set up the LLM auth proxy | Deploy an Envoy-based auth proxy that validates LangSmith-signed JWTs and routes LLM requests to your upstream provider or gateway.；Configure an instance, LangSmith setup, Self-hosted, auth, hosted, llm, proxy, self | [原文](<https://docs.langchain.com/langsmith/llm-auth-proxy-self-hosted>) |
| `LangSmith setup/Self-hosted/Configure an instance/Troubleshooting.md` | Troubleshooting | Configure an instance, LangSmith setup, Self-hosted, troubleshooting | [原文](<https://docs.langchain.com/langsmith/troubleshooting>) |
| `LangSmith setup/Self-hosted/Configure an instance/Use environment variables for model providers.md` | Use environment variables for model providers | [!NOTE]；Configure an instance, LangSmith setup, Self-hosted, environment, host, playground, self, settings | [原文](<https://docs.langchain.com/langsmith/self-host-playground-environment-settings>) |
| `LangSmith setup/Self-hosted/Connect external services/Connect self-hosted and BYOC LangSmith to Slack.md` | Connect self-hosted and BYOC LangSmith to Slack | Configure your own Slack app for Engine and alert notifications on self-hosted LangSmith or a BYOC data plane.；Connect external services, LangSmith setup, Self-hosted, host, self, slack | [原文](<https://docs.langchain.com/langsmith/self-host-slack>) |
| `LangSmith setup/Self-hosted/Connect external services/Connect to an external ClickHouse database.md` | Connect to an external ClickHouse database | [!NOTE]；Connect external services, LangSmith setup, Self-hosted, clickhouse, external, host, self | [原文](<https://docs.langchain.com/langsmith/self-host-external-clickhouse>) |
| `LangSmith setup/Self-hosted/Connect external services/Connect to an external PostgreSQL database.md` | Connect to an external PostgreSQL database | [!TIP]；Connect external services, LangSmith setup, Self-hosted, external, host, postgres, self | [原文](<https://docs.langchain.com/langsmith/self-host-external-postgres>) |
| `LangSmith setup/Self-hosted/Connect external services/Connect to an external Redis or Valkey database.md` | Connect to an external Redis or Valkey database | [!WARNING]；Connect external services, LangSmith setup, Self-hosted, external, host, redis, self | [原文](<https://docs.langchain.com/langsmith/self-host-external-redis>) |
| `LangSmith setup/Self-hosted/Connect external services/Enable blob storage.md` | Enable blob storage | [!TIP]；Connect external services, LangSmith setup, Self-hosted, blob, host, self, storage | [原文](<https://docs.langchain.com/langsmith/self-host-blob-storage>) |
| `LangSmith setup/Self-hosted/Connect external services/LangSmith-managed ClickHouse.md` | LangSmith-managed ClickHouse | [!TIP]；Connect external services, LangSmith setup, Self-hosted, clickhouse, langsmith, managed | [原文](<https://docs.langchain.com/langsmith/langsmith-managed-clickhouse>) |
| `LangSmith setup/Self-hosted/Deploy with Terraform/AWS/AWS Terraform architecture.md` | AWS Terraform architecture | Platform layers, services, IRSA roles, networking, and module dependencies for LangSmith self-hosted on AWS EKS.；AWS, Deploy with Terraform, LangSmith setup, Self-hosted, architecture, aws, host, self, terraform | [原文](<https://docs.langchain.com/langsmith/self-host-terraform-aws-architecture>) |
| `LangSmith setup/Self-hosted/Deploy with Terraform/AWS/AWS Terraform quick reference.md` | AWS Terraform quick reference | Make targets, Terraform commands, kubectl, AWS CLI, and Helm operations for LangSmith self-hosted on AWS EKS.；AWS, Deploy with Terraform, LangSmith setup, Self-hosted, aws, host, quick, reference, self, terraform | [原文](<https://docs.langchain.com/langsmith/self-host-terraform-aws-quick-reference>) |
| `LangSmith setup/Self-hosted/Deploy with Terraform/AWS/AWS Terraform troubleshooting.md` | AWS Terraform troubleshooting | Common issues, fixes, and diagnostic commands for LangSmith self-hosted on AWS EKS deployed with the LangChain Terraform modules.；AWS, Deploy with Terraform, LangSmith setup, Self-hosted, aws, host, self, terraform, troubleshooting | [原文](<https://docs.langchain.com/langsmith/self-host-terraform-aws-troubleshooting>) |
| `LangSmith setup/Self-hosted/Deploy with Terraform/AWS/AWS Terraform variables reference.md` | AWS Terraform variables reference | Complete reference of Terraform variables for LangSmith self-hosted on AWS EKS.；AWS, Deploy with Terraform, LangSmith setup, Self-hosted, aws, host, self, terraform, variables | [原文](<https://docs.langchain.com/langsmith/self-host-terraform-aws-variables>) |
| `LangSmith setup/Self-hosted/Deploy with Terraform/AWS/Deploy LangSmith on AWS with Terraform.md` | Deploy LangSmith on AWS with Terraform | End-to-end walkthrough for provisioning LangSmith self-hosted on AWS EKS using the LangChain Terraform modules.；AWS, Deploy with Terraform, LangSmith setup, Self-hosted, aws, deploy, host, self, terraform | [原文](<https://docs.langchain.com/langsmith/self-host-terraform-aws-deploy>) |
| `LangSmith setup/Self-hosted/Deploy with Terraform/Azure/Azure Terraform architecture.md` | Azure Terraform architecture | Platform layers, services, Workload Identity, networking, ingress options, and module dependencies for LangSmith self-hosted on AKS.；Azure, Deploy with Terraform, LangSmith setup, Self-hosted, architecture, azure, host, self, terraform | [原文](<https://docs.langchain.com/langsmith/self-host-terraform-azure-architecture>) |
| `LangSmith setup/Self-hosted/Deploy with Terraform/Azure/Azure Terraform quick reference.md` | Azure Terraform quick reference | Make targets, Terraform, kubectl, Azure CLI, and Helm commands for LangSmith self-hosted on AKS.；Azure, Deploy with Terraform, LangSmith setup, Self-hosted, azure, host, quick, reference, self, terraform | [原文](<https://docs.langchain.com/langsmith/self-host-terraform-azure-quick-reference>) |
| `LangSmith setup/Self-hosted/Deploy with Terraform/Azure/Azure Terraform troubleshooting.md` | Azure Terraform troubleshooting | Common issues, fixes, and diagnostic commands for LangSmith self-hosted on Azure AKS deployed with the LangChain Terraform modules.；Azure, Deploy with Terraform, LangSmith setup, Self-hosted, azure, host, self, terraform, troubleshooting | [原文](<https://docs.langchain.com/langsmith/self-host-terraform-azure-troubleshooting>) |
| `LangSmith setup/Self-hosted/Deploy with Terraform/Azure/Azure Terraform variables reference.md` | Azure Terraform variables reference | Reference of the main Terraform variables for LangSmith self-hosted on Azure AKS.；Azure, Deploy with Terraform, LangSmith setup, Self-hosted, azure, host, self, terraform, variables | [原文](<https://docs.langchain.com/langsmith/self-host-terraform-azure-variables>) |
| `LangSmith setup/Self-hosted/Deploy with Terraform/Azure/Deploy LangSmith on Azure with Terraform.md` | Deploy LangSmith on Azure with Terraform | End-to-end walkthrough for provisioning LangSmith self-hosted on Azure AKS using the LangChain Terraform modules.；Azure, Deploy with Terraform, LangSmith setup, Self-hosted, azure, deploy, host, self, terraform | [原文](<https://docs.langchain.com/langsmith/self-host-terraform-azure-deploy>) |
| `LangSmith setup/Self-hosted/Deploy with Terraform/Deploy LangSmith with Terraform.md` | Deploy LangSmith with Terraform | Provision LangSmith self-hosted on AWS, Azure, or GCP using LangChain's production-ready Terraform modules.；Deploy with Terraform, LangSmith setup, Self-hosted, host, self, terraform | [原文](<https://docs.langchain.com/langsmith/self-host-terraform>) |
| `LangSmith setup/Self-hosted/Deploy with Terraform/GCP/Deploy LangSmith on GCP with Terraform.md` | Deploy LangSmith on GCP with Terraform | End-to-end walkthrough for provisioning LangSmith self-hosted on GCP GKE using the LangChain Terraform modules.；Deploy with Terraform, GCP, LangSmith setup, Self-hosted, deploy, gcp, host, self, terraform | [原文](<https://docs.langchain.com/langsmith/self-host-terraform-gcp-deploy>) |
| `LangSmith setup/Self-hosted/Deploy with Terraform/GCP/GCP Terraform architecture.md` | GCP Terraform architecture | Platform layers, services, Workload Identity, networking, and module dependencies for LangSmith self-hosted on GKE.；Deploy with Terraform, GCP, LangSmith setup, Self-hosted, architecture, gcp, host, self, terraform | [原文](<https://docs.langchain.com/langsmith/self-host-terraform-gcp-architecture>) |
| `LangSmith setup/Self-hosted/Deploy with Terraform/GCP/GCP Terraform quick reference.md` | GCP Terraform quick reference | Make targets, Terraform, kubectl, gcloud, and Helm commands for LangSmith self-hosted on GKE.；Deploy with Terraform, GCP, LangSmith setup, Self-hosted, gcp, host, quick, reference, self, terraform | [原文](<https://docs.langchain.com/langsmith/self-host-terraform-gcp-quick-reference>) |
| `LangSmith setup/Self-hosted/Deploy with Terraform/GCP/GCP Terraform troubleshooting.md` | GCP Terraform troubleshooting | Common issues, fixes, and diagnostic commands for LangSmith self-hosted on GKE deployed with the LangChain Terraform modules.；Deploy with Terraform, GCP, LangSmith setup, Self-hosted, gcp, host, self, terraform, troubleshooting | [原文](<https://docs.langchain.com/langsmith/self-host-terraform-gcp-troubleshooting>) |
| `LangSmith setup/Self-hosted/Deploy with Terraform/GCP/GCP Terraform variables reference.md` | GCP Terraform variables reference | Complete reference of Terraform variables for LangSmith self-hosted on GCP GKE.；Deploy with Terraform, GCP, LangSmith setup, Self-hosted, gcp, host, self, terraform, variables | [原文](<https://docs.langchain.com/langsmith/self-host-terraform-gcp-variables>) |
| `LangSmith setup/Self-hosted/Get started by cloud provider/Self-hosted LangSmith on AWS.md` | Self-hosted LangSmith on AWS | [!NOTE]；Get started by cloud provider, LangSmith setup, Self-hosted, aws, hosted, self | [原文](<https://docs.langchain.com/langsmith/aws-self-hosted>) |
| `LangSmith setup/Self-hosted/Get started by cloud provider/Self-hosted LangSmith on Azure.md` | Self-hosted LangSmith on Azure | [!NOTE]；Get started by cloud provider, LangSmith setup, Self-hosted, azure, hosted, self | [原文](<https://docs.langchain.com/langsmith/azure-self-hosted>) |
| `LangSmith setup/Self-hosted/Get started by cloud provider/Self-hosted LangSmith on GCP.md` | Self-hosted LangSmith on GCP | [!NOTE]；Get started by cloud provider, LangSmith setup, Self-hosted, gcp, hosted, self | [原文](<https://docs.langchain.com/langsmith/gcp-self-hosted>) |
| `LangSmith setup/Self-hosted/Hybrid/Setup guide (legacy).md` | Setup guide (legacy) | Legacy hybrid deployment model with a LangChain-managed control plane and a self-managed data plane.；Hybrid, LangSmith setup, Self-hosted, hybrid, legacy | [原文](<https://docs.langchain.com/langsmith/hybrid-legacy>) |
| `LangSmith setup/Self-hosted/Install an instance/Additional features/Configure additional self-hosted features.md` | Configure additional self-hosted features | Choose which optional self-hosted LangSmith features to install, such as Sandboxes, Engine, Fleet, and Agent Server hosting, and in what order.；Additional features, Install an instance, LangSmith setup, Self-hosted, additional, features, host, self | [原文](<https://docs.langchain.com/langsmith/self-host-additional-features>) |
| `LangSmith setup/Self-hosted/Install an instance/Additional features/Enable Agent Server hosting.md` | Enable Agent Server hosting | Add a control plane and data plane to deploy and manage agents on self-hosted LangSmith.；Additional features, Install an instance, LangSmith setup, Self-hosted, deployment, enable, hosted, self | [原文](<https://docs.langchain.com/langsmith/enable-self-hosted-deployment>) |
| `LangSmith setup/Self-hosted/Install an instance/Additional features/Enable Fleet on self-hosted LangSmith.md` | Enable Fleet on self-hosted LangSmith | Install Fleet and optionally configure tools and triggers on self-hosted LangSmith.；Additional features, Install an instance, LangSmith setup, Self-hosted, enable, fleet, hosted, self | [原文](<https://docs.langchain.com/langsmith/enable-self-hosted-fleet>) |
| `LangSmith setup/Self-hosted/Install an instance/Additional features/Enable Sandboxes/Enable Sandboxes on self-hosted LangSmith.md` | Enable Sandboxes on self-hosted LangSmith | Configure Kubernetes nodes, storage, and Helm values for self-hosted LangSmith Sandboxes.；Additional features, Enable Sandboxes, Install an instance, LangSmith setup, Self-hosted, enable, hosted, sandboxes, self | [原文](<https://docs.langchain.com/langsmith/enable-self-hosted-sandboxes>) |
| `LangSmith setup/Self-hosted/Install an instance/Additional features/Enable Sandboxes/Operate self-hosted Sandboxes.md` | Operate self-hosted Sandboxes | Plan self-hosted Sandbox upgrades, understand host drains and failure recovery, protect shared storage, and monitor production capacity.；Additional features, Enable Sandboxes, Install an instance, LangSmith setup, Self-hosted, host, operations, sandbox, self | [原文](<https://docs.langchain.com/langsmith/self-host-sandbox-operations>) |
| `LangSmith setup/Self-hosted/Install an instance/Additional features/Enable Sandboxes/Route self-hosted Sandbox egress through a forward proxy.md` | Route self-hosted Sandbox egress through a forward proxy | Send outbound connections from self-hosted LangSmith Sandboxes through a corporate HTTP or HTTPS forward proxy, with a bypass list, Basic proxy authentication, and custom CA trust.；Additional features, Enable Sandboxes, Install an instance, LangSmith setup, Self-hosted, egress, host, proxy, sandbox, self | [原文](<https://docs.langchain.com/langsmith/self-host-sandbox-egress-proxy>) |
| `LangSmith setup/Self-hosted/Install an instance/Additional features/Enable Sandboxes/Run self-hosted Sandboxes in a separate cluster.md` | Run self-hosted Sandboxes in a separate cluster | Run the self-hosted LangSmith Sandbox runtime in a dedicated Kubernetes cluster with the langsmith-sandbox Helm chart, connected to the LangSmith control plane in another cluster.；Additional features, Enable Sandboxes, Install an instance, LangSmith setup, Self-hosted, cluster, host, sandbox, self, separate | [原文](<https://docs.langchain.com/langsmith/self-host-sandbox-separate-cluster>) |
| `LangSmith setup/Self-hosted/Install an instance/Additional features/Enable Sandboxes/Scale self-hosted Sandboxes.md` | Scale self-hosted Sandboxes | Plan self-hosted Sandbox capacity with host autoscaling, Kubernetes node scaling, memory headroom, and shared filesystem caching.；Additional features, Enable Sandboxes, Install an instance, LangSmith setup, Self-hosted, host, sandbox, scaling, self | [原文](<https://docs.langchain.com/langsmith/self-host-sandbox-scaling>) |
| `LangSmith setup/Self-hosted/Install an instance/Additional features/Enable Sandboxes/Self-hosted Sandbox architecture.md` | Self-hosted Sandbox architecture | Understand how self-hosted LangSmith Sandboxes use microVMs, Kubernetes hosts, and shared storage to run and resume workloads.；Additional features, Enable Sandboxes, Install an instance, LangSmith setup, Self-hosted, architecture, host, sandbox, self | [原文](<https://docs.langchain.com/langsmith/self-host-sandbox-architecture>) |
| `LangSmith setup/Self-hosted/Install an instance/Additional features/Enable the LLM Gateway.md` | Enable the LLM Gateway | Enable the agent-gateway service on a self-hosted LangSmith install using the Helm chart, then make your first gateway call.；Additional features, Install an instance, LangSmith setup, Self-hosted, gateway, hosted, llm, self | [原文](<https://docs.langchain.com/langsmith/llm-gateway-self-hosted>) |
| `LangSmith setup/Self-hosted/Install an instance/Configure Insights and Chat on self-hosted LangSmith.md` | Configure Insights and Chat on self-hosted LangSmith | Configure encryption keys and model access for Insights and Chat on self-hosted LangSmith, disable either feature, or upgrade a legacy configuration.；Install an instance, LangSmith setup, Self-hosted, chat, host, insights, self | [原文](<https://docs.langchain.com/langsmith/self-host-insights-chat>) |
| `LangSmith setup/Self-hosted/Install an instance/Interact with your self-hosted instance of LangSmith.md` | Interact with your self-hosted instance of LangSmith | [!NOTE]；Install an instance, LangSmith setup, Self-hosted, host, self, usage | [原文](<https://docs.langchain.com/langsmith/self-host-usage>) |
| `LangSmith setup/Self-hosted/Install an instance/Minimum versions for self-hosting dependencies.md` | Minimum versions for self-hosting dependencies | Minimum supported versions for the databases, tools, and infrastructure required to self-host LangSmith.；Install an instance, LangSmith setup, Self-hosted, dependency, host, self, versions | [原文](<https://docs.langchain.com/langsmith/self-host-dependency-versions>) |
| `LangSmith setup/Self-hosted/Install an instance/Self-host LangSmith on Kubernetes.md` | Self-host LangSmith on Kubernetes | Install self-hosted LangSmith and its dependencies in a Kubernetes cluster with Helm, including Insights and Chat.；Install an instance, LangSmith setup, Self-hosted, kubernetes | [原文](<https://docs.langchain.com/langsmith/kubernetes>) |
| `LangSmith setup/Self-hosted/Manage an instance/Disaster recovery for self-hosted LangSmith.md` | Disaster recovery for self-hosted LangSmith | [!NOTE]；LangSmith setup, Manage an instance, Self-hosted, disaster, host, recovery, self | [原文](<https://docs.langchain.com/langsmith/self-host-disaster-recovery>) |
| `LangSmith setup/Self-hosted/Manage an instance/Upgrade an installation.md` | Upgrade an installation | [!WARNING]；LangSmith setup, Manage an instance, Self-hosted, host, self, upgrades | [原文](<https://docs.langchain.com/langsmith/self-host-upgrades>) |
| `LangSmith setup/Self-hosted/Manage an instance/View trace counts across your organization.md` | View trace counts across your organization | [!NOTE]；LangSmith setup, Manage an instance, Self-hosted, charts, host, organization, self | [原文](<https://docs.langchain.com/langsmith/self-host-organization-charts>) |
| `LangSmith setup/Self-hosted/Platform auth & access control/Basic authentication with email and password.md` | Basic authentication with email and password | [!TIP]；LangSmith setup, Platform auth & access control, Self-hosted, auth, basic, host, self | [原文](<https://docs.langchain.com/langsmith/self-host-basic-auth>) |
| `LangSmith setup/Self-hosted/Platform auth & access control/Configure custom TLS certificates.md` | Configure custom TLS certificates | [!NOTE]；LangSmith setup, Platform auth & access control, Self-hosted, certificates, custom, host, self, tls | [原文](<https://docs.langchain.com/langsmith/self-host-custom-tls-certificates>) |
| `LangSmith setup/Self-hosted/Platform auth & access control/Customize user management.md` | Customize user management | [!NOTE]；LangSmith setup, Platform auth & access control, Self-hosted, host, management, self, user | [原文](<https://docs.langchain.com/langsmith/self-host-user-management>) |
| `LangSmith setup/Self-hosted/Platform auth & access control/Set up SSO with OAuth2.0 and OIDC.md` | Set up SSO with OAuth2.0 and OIDC | [!NOTE]；LangSmith setup, Platform auth & access control, Self-hosted, host, self, sso | [原文](<https://docs.langchain.com/langsmith/self-host-sso>) |
| `LangSmith setup/Self-hosted/Platform auth & access control/Use an existing secret for your installation (Kubernetes).md` | Use an existing secret for your installation (Kubernetes) | [!WARNING]；LangSmith setup, Platform auth & access control, Self-hosted, an, existing, host, secret, self, using | [原文](<https://docs.langchain.com/langsmith/self-host-using-an-existing-secret>) |
| `LangSmith setup/Self-hosted/Reference/Release policy.md` | Release policy | Release channels, cadence, and version support for self-hosted LangSmith.；LangSmith setup, Reference, Self-hosted, release, versions | [原文](<https://docs.langchain.com/langsmith/release-versions>) |
| `LangSmith setup/Self-hosted/Reference/Self-hosted LangSmith changelog.md` | Self-hosted LangSmith changelog | LangSmith setup, Reference, Self-hosted, changelog, hosted, self | [原文](<https://docs.langchain.com/langsmith/self-hosted-changelog>) |
| `LangSmith setup/Self-hosted/Scripts/Delete organizations.md` | Delete organizations | LangSmith setup, Scripts, Self-hosted, an, delete, organization, script | [原文](<https://docs.langchain.com/langsmith/script-delete-an-organization>) |
| `LangSmith setup/Self-hosted/Scripts/Delete traces.md` | Delete traces | [!WARNING]；LangSmith setup, Scripts, Self-hosted, delete, script, traces | [原文](<https://docs.langchain.com/langsmith/script-delete-traces>) |
| `LangSmith setup/Self-hosted/Scripts/Delete workspaces.md` | Delete workspaces | [!NOTE]；LangSmith setup, Scripts, Self-hosted, a, delete, script, workspace | [原文](<https://docs.langchain.com/langsmith/script-delete-a-workspace>) |
| `LangSmith setup/Self-hosted/Scripts/Generate ClickHouse stats.md` | Generate ClickHouse stats | LangSmith setup, Scripts, Self-hosted, clickhouse, generate, script, stats | [原文](<https://docs.langchain.com/langsmith/script-generate-clickhouse-stats>) |
| `LangSmith setup/Self-hosted/Scripts/Generate query stats.md` | Generate query stats | LangSmith setup, Scripts, Self-hosted, generate, query, script, stats | [原文](<https://docs.langchain.com/langsmith/script-generate-query-stats>) |
| `LangSmith setup/Self-hosted/Scripts/Run support queries against ClickHouse.md` | Run support queries against ClickHouse | LangSmith setup, Scripts, Self-hosted, ch, queries, running, script, support | [原文](<https://docs.langchain.com/langsmith/script-running-ch-support-queries>) |
| `LangSmith setup/Self-hosted/Scripts/Run support queries against PostgreSQL.md` | Run support queries against PostgreSQL | [!NOTE]；LangSmith setup, Scripts, Self-hosted, pg, queries, running, script, support | [原文](<https://docs.langchain.com/langsmith/script-running-pg-support-queries>) |
| `LangSmith setup/Self-hosted/Self-hosted LangSmith.md` | Self-hosted LangSmith | Run LangSmith in your own Kubernetes cluster, with Insights and Chat enabled by default and optional features such as Sandboxes, Engine, Fleet, LLM Gateway, and Agent Server hosting.；LangSmith setup, Self-hosted, hosted, self | [原文](<https://docs.langchain.com/langsmith/self-hosted>) |
| `LangSmith setup/Self-hosted/Self-hosted observability/Configure your collector for LangSmith telemetry.md` | Configure your collector for LangSmith telemetry | [!WARNING]；LangSmith setup, Self-hosted, Self-hosted observability, collector, langsmith | [原文](<https://docs.langchain.com/langsmith/langsmith-collector>) |
| `LangSmith setup/Self-hosted/Self-hosted observability/Deploy an observability stack for your LangSmith deployment.md` | Deploy an observability stack for your LangSmith deployment | [!CAUTION]；LangSmith setup, Self-hosted, Self-hosted observability, observability, stack | [原文](<https://docs.langchain.com/langsmith/observability-stack>) |
| `LangSmith setup/Self-hosted/Self-hosted observability/Export LangSmith telemetry to your observability backend.md` | Export LangSmith telemetry to your observability backend | [!WARNING]；LangSmith setup, Self-hosted, Self-hosted observability, backend, export | [原文](<https://docs.langchain.com/langsmith/export-backend>) |
| `LangSmith setup/Self-hosted/Self-hosted observability/Install Mission Control.md` | Install Mission Control | Install Mission Control, an in-cluster console for monitoring, configuring, and operating self-hosted LangSmith on Kubernetes.；LangSmith setup, Self-hosted, Self-hosted observability, control, hosted, mission, self | [原文](<https://docs.langchain.com/langsmith/self-hosted-mission-control>) |
| `LangSmith setup/Self-hosted/Self-hosted observability/Monitor self-hosted LangSmith with Datadog or Grafana.md` | Monitor self-hosted LangSmith with Datadog or Grafana | Import tabbed SmithDB and Sandbox dashboards into your own monitoring instance and configure component telemetry collection.；LangSmith setup, Self-hosted, Self-hosted observability, dashboards, host, observability, self | [原文](<https://docs.langchain.com/langsmith/self-host-observability-dashboards>) |
| `LangSmith setup/Self-hosted/SmithDB/Install SmithDB/Configure SmithDB for scale.md` | Configure SmithDB for scale | Choose tested SmithDB resource tiers and size Kubernetes workloads and the PostgreSQL metastore.；Install SmithDB, LangSmith setup, Self-hosted, SmithDB, host, scale, self, smithdb | [原文](<https://docs.langchain.com/langsmith/self-host-smithdb-scale>) |
| `LangSmith setup/Self-hosted/SmithDB/Install SmithDB/Install LangSmith with SmithDB.md` | Install LangSmith with SmithDB | Enable SmithDB on a self-hosted LangSmith Kubernetes installation through staged Helm updates.；Install SmithDB, LangSmith setup, Self-hosted, SmithDB, host, install, self, smithdb | [原文](<https://docs.langchain.com/langsmith/self-host-smithdb-install>) |
| `LangSmith setup/Self-hosted/SmithDB/Install SmithDB/Migrate ClickHouse history to SmithDB.md` | Migrate ClickHouse history to SmithDB | Run the historical ClickHouse-to-SmithDB migration for a self-hosted LangSmith installation.；Install SmithDB, LangSmith setup, Self-hosted, SmithDB, host, migrate, self, smithdb | [原文](<https://docs.langchain.com/langsmith/self-host-smithdb-migrate>) |
| `LangSmith setup/Self-hosted/SmithDB/Install SmithDB/Prepare SmithDB supporting infrastructure.md` | Prepare SmithDB supporting infrastructure | Provide a dedicated PostgreSQL metastore, object storage, and cache storage before enabling SmithDB.；Install SmithDB, LangSmith setup, Self-hosted, SmithDB, host, infrastructure, self, smithdb | [原文](<https://docs.langchain.com/langsmith/self-host-smithdb-infrastructure>) |
| `LangSmith setup/Self-hosted/SmithDB/Install SmithDB/Troubleshoot SmithDB.md` | Troubleshoot SmithDB | Diagnose SmithDB failures, gather troubleshooting context, or disable and reset a SmithDB deployment on self-hosted LangSmith.；Install SmithDB, LangSmith setup, Self-hosted, SmithDB, host, self, smithdb, troubleshooting | [原文](<https://docs.langchain.com/langsmith/self-host-smithdb-troubleshooting>) |
| `LangSmith setup/Self-hosted/SmithDB/Monitoring and alerting/Common SmithDB issues to monitor.md` | Common SmithDB issues to monitor | The first metrics to check on self-hosted LangSmith, and how to detect and fix the SmithDB issues that occur most often in production.；LangSmith setup, Monitoring and alerting, Self-hosted, SmithDB, common, host, issues, self, smithdb | [原文](<https://docs.langchain.com/langsmith/self-host-smithdb-common-issues>) |
| `LangSmith setup/Self-hosted/SmithDB/Monitoring and alerting/Configure SmithDB observability.md` | Configure SmithDB observability | Scrape SmithDB application metrics and export logs and traces to your existing observability stack.；LangSmith setup, Monitoring and alerting, Self-hosted, SmithDB, host, observability, self, smithdb | [原文](<https://docs.langchain.com/langsmith/self-host-smithdb-observability>) |
| `LangSmith setup/Self-hosted/SmithDB/Monitoring and alerting/Essential SmithDB metrics.md` | Essential SmithDB metrics | The SmithDB and LangSmith metrics to monitor on self-hosted LangSmith, what they measure, and how to use them.；LangSmith setup, Monitoring and alerting, Self-hosted, SmithDB, host, metrics, self, smithdb | [原文](<https://docs.langchain.com/langsmith/self-host-smithdb-metrics>) |
| `LangSmith setup/Self-hosted/SmithDB/Overview/Enable SmithDB on self-hosted LangSmith.md` | Enable SmithDB on self-hosted LangSmith | Run SmithDB alongside ClickHouse on a self-hosted LangSmith Kubernetes installation.；LangSmith setup, Overview, Self-hosted, SmithDB, host, self, smithdb | [原文](<https://docs.langchain.com/langsmith/self-host-smithdb>) |
| `LangSmith setup/Self-hosted/SmithDB/Overview/How SmithDB handles data.md` | How SmithDB handles data | How SmithDB writes runs, answers queries, applies feedback and deletes, and compacts stored data on self-hosted LangSmith.；LangSmith setup, Overview, Self-hosted, SmithDB, data, host, paths, self, smithdb | [原文](<https://docs.langchain.com/langsmith/self-host-smithdb-data-paths>) |
| `LangSmith setup/Self-hosted/SmithDB/Overview/SmithDB architecture.md` | SmithDB architecture | How SmithDB and LangSmith components depend on each other on self-hosted LangSmith.；LangSmith setup, Overview, Self-hosted, SmithDB, architecture, host, self, smithdb | [原文](<https://docs.langchain.com/langsmith/self-host-smithdb-architecture>) |
| `LangSmith setup/Self-hosted/SmithDB/SmithDB feature availability.md` | SmithDB feature availability | LangSmith features that are unavailable on self-hosted installations that query ClickHouse, and what still works without SmithDB.；LangSmith setup, Self-hosted, SmithDB, features, host, self, smithdb | [原文](<https://docs.langchain.com/langsmith/self-host-smithdb-features>) |
| `Monitor/Debug/Bulk export trace data/Bulk export trace data.md` | Bulk export trace data | Export LangSmith trace data to an S3-compatible bucket in Parquet format.；Bulk export trace data, Debug, Monitor, data, export | [原文](<https://docs.langchain.com/langsmith/data-export>) |
| `Monitor/Debug/Bulk export trace data/Export trace data to BigQuery.md` | Export trace data to BigQuery | Load LangSmith trace data into BigQuery using bulk export to GCS.；Bulk export trace data, Debug, Monitor, big, bulk, export, query | [原文](<https://docs.langchain.com/langsmith/big-query-bulk-export>) |
| `Monitor/Debug/Bulk export trace data/Import exported data.md` | Import exported data | Import LangSmith bulk-exported Parquet data into BigQuery, Snowflake, Redshift, Clickhouse, or DuckDB.；Bulk export trace data, Debug, Monitor, data, downstream, export | [原文](<https://docs.langchain.com/langsmith/data-export-downstream>) |
| `Monitor/Debug/Bulk export trace data/Manage bulk export destinations.md` | Manage bulk export destinations | Configure and manage S3-compatible export destinations for LangSmith bulk exports.；Bulk export trace data, Debug, Monitor, data, destinations, export | [原文](<https://docs.langchain.com/langsmith/data-export-destinations>) |
| `Monitor/Debug/Bulk export trace data/Monitor and troubleshoot bulk exports.md` | Monitor and troubleshoot bulk exports | Monitor bulk export status, manage running exports, and troubleshoot failures.；Bulk export trace data, Debug, Monitor, data, export, monitor | [原文](<https://docs.langchain.com/langsmith/data-export-monitor>) |
| `Monitor/Debug/Configure threads.md` | Configure threads | [!WARNING]；Debug, Monitor, threads | [原文](<https://docs.langchain.com/langsmith/threads>) |
| `Monitor/Debug/Data type reference/Feedback data format.md` | Feedback data format | [!TIP]；Data type reference, Debug, Monitor, data, feedback, format | [原文](<https://docs.langchain.com/langsmith/feedback-data-format>) |
| `Monitor/Debug/Data type reference/Run (span) data format.md` | Run (span) data format | Data type reference, Debug, Monitor, data, format, run | [原文](<https://docs.langchain.com/langsmith/run-data-format>) |
| `Monitor/Debug/Trajectory view/Trajectory view integrations.md` | Trajectory view integrations | Frameworks and SDKs that render in the LangSmith Trajectory view and the metadata each one sets.；Debug, Monitor, Trajectory view, integrations, trajectory, view | [原文](<https://docs.langchain.com/langsmith/trajectory-view-integrations>) |
| `Monitor/Debug/Viewing & managing traces/Configure run input and output preview.md` | Configure run input and output preview | Customize what appears in the Input and Output columns of the Runs table by configuring custom preview paths for specific trace types.；Debug, Monitor, Viewing & managing traces, configure, input, output, preview | [原文](<https://docs.langchain.com/langsmith/configure-input-output-preview>) |
| `Monitor/Debug/Viewing & managing traces/Filter traces (ClickHouse).md` | Filter traces (ClickHouse) | Filter threads, traces, and runs in a LangSmith tracing project backed by ClickHouse, using the filter bar, filter shortcuts, and saved filters.；Debug, Monitor, Viewing & managing traces, application, filter, in, traces | [原文](<https://docs.langchain.com/langsmith/filter-traces-in-application>) |
| `Monitor/Debug/Viewing & managing traces/Filter traces.md` | Filter traces | Find specific threads, traces, and runs in a LangSmith tracing project by writing filter queries in the search bar.；Debug, Monitor, Viewing & managing traces, filter, traces | [原文](<https://docs.langchain.com/langsmith/filter-traces>) |
| `Monitor/Debug/Viewing & managing traces/LangSmith MCP Server.md` | LangSmith MCP Server | Use the Model Context Protocol (MCP) server to let language models fetch conversation history, prompts, runs, datasets, experiments, and billing from LangSmith.；Debug, Monitor, Viewing & managing traces, langsmith, mcp, server | [原文](<https://docs.langchain.com/langsmith/langsmith-mcp-server>) |
| `Monitor/Debug/Viewing & managing traces/LangSmith Remote MCP.md` | LangSmith Remote MCP | Connect MCP-compatible clients to LangSmith over OAuth, or authenticate programmatic clients with a LangSmith API key.；Debug, Monitor, Viewing & managing traces, langsmith, mcp, remote | [原文](<https://docs.langchain.com/langsmith/langsmith-remote-mcp>) |
| `Monitor/Debug/Viewing & managing traces/Manage a trace.md` | Manage a trace | Share traces publicly, and view server logs from the Details view in LangSmith.；Debug, Monitor, Viewing & managing traces, manage, trace | [原文](<https://docs.langchain.com/langsmith/manage-trace>) |
| `Monitor/Debug/Viewing & managing traces/Query threads using the SDK.md` | Query threads using the SDK | Programmatically fetch and inspect multi-turn conversation threads from your LangSmith projects.；Debug, Monitor, Viewing & managing traces, query, threads | [原文](<https://docs.langchain.com/langsmith/query-threads>) |
| `Monitor/Debug/Viewing & managing traces/Query traces using the SDK.md` | Query traces using the SDK | [!NOTE]；Debug, Monitor, Viewing & managing traces, export, traces | [原文](<https://docs.langchain.com/langsmith/export-traces>) |
| `Monitor/Debug/Viewing & managing traces/Resolve an agent environment.md` | Resolve an agent environment | Resolve an agent environment, experiment, or workspace evaluator traces to the session ID required by query and feedback APIs.；Debug, Monitor, Viewing & managing traces, agent, an, resolve | [原文](<https://docs.langchain.com/langsmith/resolve-an-agent>) |
| `Monitor/Debug/Viewing & managing traces/Trace query syntax.md` | Trace query syntax | [!NOTE]；Debug, Monitor, Viewing & managing traces, query, syntax, trace | [原文](<https://docs.langchain.com/langsmith/trace-query-syntax>) |
| `Monitor/Debug/Viewing & managing traces/View traces.md` | View traces | Inspect agent threads in LangSmith using the Trajectory view or Details view.；Debug, Monitor, Viewing & managing traces, traces, view | [原文](<https://docs.langchain.com/langsmith/view-traces>) |
| `Monitor/Observe/Automations/Configure webhook notifications for rules.md` | Configure webhook notifications for rules | Configure webhook notifications to receive POST requests when automation rules match new runs or threads in LangSmith.；Automations, Monitor, Observe, webhooks | [原文](<https://docs.langchain.com/langsmith/webhooks>) |
| `Monitor/Observe/Automations/Set up automation rules.md` | Set up automation rules | [!NOTE]；Automations, Monitor, Observe, rules | [原文](<https://docs.langchain.com/langsmith/rules>) |
| `Monitor/Observe/Monitoring & alerting/Alerts in LangSmith.md` | Alerts in LangSmith | [!NOTE]；Monitor, Monitoring & alerting, Observe, alerts | [原文](<https://docs.langchain.com/langsmith/alerts>) |
| `Monitor/Observe/Monitoring & alerting/Custom Apps.md` | Custom Apps | Build custom UIs that run inside LangSmith and call the LangSmith API, either by chatting with LangSmith Chat or locally with the LangSmith CLI.；Monitor, Monitoring & alerting, Observe, apps, custom | [原文](<https://docs.langchain.com/langsmith/custom-apps>) |
| `Monitor/Observe/Monitoring & alerting/Discover errors and usage patterns with Insights.md` | Discover errors and usage patterns with Insights | Use LangSmith Insights to automatically analyze traces, detect usage patterns, identify common agent behaviors, and surface failure modes without manual trace review.；Monitor, Monitoring & alerting, Observe, insights | [原文](<https://docs.langchain.com/langsmith/insights>) |
| `Monitor/Observe/Monitoring & alerting/Monitor projects with dashboards.md` | Monitor projects with dashboards | [!NOTE]；Monitor, Monitoring & alerting, Observe, dashboards | [原文](<https://docs.langchain.com/langsmith/dashboards>) |
| `Monitor/Observe/Online evaluators/Set up LLM-as-a-judge online evaluators.md` | Set up LLM-as-a-judge online evaluators | [!NOTE]；Monitor, Observe, Online evaluators, as, evaluations, judge, llm, online | [原文](<https://docs.langchain.com/langsmith/online-evaluations-llm-as-judge>) |
| `Monitor/Observe/Online evaluators/Set up LangChain Tuned Evaluators.md` | Set up LangChain Tuned Evaluators | Use specialized LangChain-managed judges to attach quality feedback to traces.；Monitor, Observe, Online evaluators, evaluators, tuned | [原文](<https://docs.langchain.com/langsmith/tuned-evaluators>) |
| `Monitor/Observe/Online evaluators/Set up composite online evaluators.md` | Set up composite online evaluators | [!NOTE]；Monitor, Observe, Online evaluators, composite, evaluations, online | [原文](<https://docs.langchain.com/langsmith/online-evaluations-composite>) |
| `Monitor/Observe/Online evaluators/Set up decision model online evaluators.md` | Set up decision model online evaluators | Evaluate production traces in LangSmith with a decision model as the judge and record each typed answer as feedback.；Monitor, Observe, Online evaluators, decision, evaluations, models, online | [原文](<https://docs.langchain.com/langsmith/online-evaluations-decision-models>) |
| `Monitor/Observe/Online evaluators/Set up multi-turn online evaluators.md` | Set up multi-turn online evaluators | [!TIP]；Monitor, Observe, Online evaluators, evaluations, multi, online, turn | [原文](<https://docs.langchain.com/langsmith/online-evaluations-multi-turn>) |
| `Monitor/Observe/Online evaluators/Set up online code evaluators.md` | Set up online code evaluators | [!NOTE]；Monitor, Observe, Online evaluators, code, evaluations, online | [原文](<https://docs.langchain.com/langsmith/online-evaluations-code>) |
| `Monitor/Overview/LangSmith Observability.md` | LangSmith Observability | Instrument your LLM application, investigate traces, and monitor performance in production with LangSmith.；Monitor, Overview, observability | [原文](<https://docs.langchain.com/langsmith/observability>) |
| `Monitor/Reference/LangSmith REST API/Administration/AWS marketplace fulfillment URL registration.md` | AWS marketplace fulfillment URL registration | Receives the x-amzn-marketplace-token posted by AWS Marketplace when a customer clicks "Set Up Account", resolves the customer identity, stores it in the DB, and redirects to the thank-you page.；Administration, LangSmith REST API, Monitor, Reference, aws, fulfillment, marketplace, registration, url | [原文](<https://docs.langchain.com/langsmith/smith-api/aws_marketplace/aws-marketplace-fulfillment-url-registration>) |
| `Monitor/Reference/LangSmith REST API/Administration/Add basic auth members to current org.md` | Add basic auth members to current org | Batch add up to 500 users to the org and specified workspaces in basic auth mode.；Administration, LangSmith REST API, Monitor, Reference, add, auth, basic, current, members, org, to | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/add-basic-auth-members-to-current-org>) |
| `Monitor/Reference/LangSmith REST API/Administration/Add member to current org.md` | Add member to current org | Administration, LangSmith REST API, Monitor, Reference, add, current, member, org, to | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/add-member-to-current-org>) |
| `Monitor/Reference/LangSmith REST API/Administration/Add member to current workspace.md` | Add member to current workspace | Add an existing organization member to the current workspace.；Administration, LangSmith REST API, Monitor, Reference, add, current, member, to, workspace | [原文](<https://docs.langchain.com/langsmith/smith-api/workspaces/add-member-to-current-workspace>) |
| `Monitor/Reference/LangSmith REST API/Administration/Add members to current org batch.md` | Add members to current org batch | Batch invite up to 500 users to the current org.；Administration, LangSmith REST API, Monitor, Reference, add, batch, current, members, org, to | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/add-members-to-current-org-batch>) |
| `Monitor/Reference/LangSmith REST API/Administration/Add members to current workspace batch.md` | Add members to current workspace batch | Batch invite up to 500 users to the current workspace and organization.；Administration, LangSmith REST API, Monitor, Reference, add, batch, current, members, to, workspace | [原文](<https://docs.langchain.com/langsmith/smith-api/workspaces/add-members-to-current-workspace-batch>) |
| `Monitor/Reference/LangSmith REST API/Administration/Attach access policies to a role (attach-access-policies-to-a-role-1).md` | Attach access policies to a role | Attaches one or more access policies to a specific role. The request body must contain an array of access policy IDs.；1, Administration, LangSmith REST API, Monitor, Reference, a, access, attach, policies, role, to | [原文](<https://docs.langchain.com/langsmith/smith-api/access_policies/attach-access-policies-to-a-role-1>) |
| `Monitor/Reference/LangSmith REST API/Administration/Attach access policies to a role.md` | Attach access policies to a role | Attaches one or more access policies to a specific role. The request body must contain an array of access policy IDs.；Administration, LangSmith REST API, Monitor, Reference, a, access, attach, policies, role, to | [原文](<https://docs.langchain.com/langsmith/smith-api/access_policies/attach-access-policies-to-a-role>) |
| `Monitor/Reference/LangSmith REST API/Administration/Bulk unshare entities.md` | Bulk unshare entities | Bulk unshare entities by share tokens for the workspace.；Administration, LangSmith REST API, Monitor, Reference, bulk, entities, unshare | [原文](<https://docs.langchain.com/langsmith/smith-api/workspaces/bulk-unshare-entities>) |
| `Monitor/Reference/LangSmith REST API/Administration/Change payment plan.md` | Change payment plan | Administration, LangSmith REST API, Monitor, Reference, change, payment, plan | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/change-payment-plan>) |
| `Monitor/Reference/LangSmith REST API/Administration/Check SSO email verification status.md` | Check SSO email verification status | Retrieve the email verification status of an SSO user.；Administration, LangSmith REST API, Monitor, Reference, check, email, sso, status, verification | [原文](<https://docs.langchain.com/langsmith/smith-api/auth/check-sso-email-verification-status>) |
| `Monitor/Reference/LangSmith REST API/Administration/Claim pending organization invite.md` | Claim pending organization invite | Administration, LangSmith REST API, Monitor, Reference, claim, invite, organization, pending | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/claim-pending-organization-invite>) |
| `Monitor/Reference/LangSmith REST API/Administration/Claim pending workspace invite.md` | Claim pending workspace invite | Administration, LangSmith REST API, Monitor, Reference, claim, invite, pending, workspace | [原文](<https://docs.langchain.com/langsmith/smith-api/workspaces/claim-pending-workspace-invite>) |
| `Monitor/Reference/LangSmith REST API/Administration/Confirm SSO user email.md` | Confirm SSO user email | Confirm the email of an SSO user.；Administration, LangSmith REST API, Monitor, Reference, confirm, email, sso, user | [原文](<https://docs.langchain.com/langsmith/smith-api/auth/confirm-sso-user-email>) |
| `Monitor/Reference/LangSmith REST API/Administration/Create SSO settings.md` | Create SSO settings | Create SSO provider settings for the current organization.；Administration, LangSmith REST API, Monitor, Reference, create, settings, sso | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/create-sso-settings>) |
| `Monitor/Reference/LangSmith REST API/Administration/Create a SCIM token.md` | Create a SCIM token | Create a new SCIM bearer token for the current organization. The full token value is only returned once upon creation.；Administration, LangSmith REST API, Monitor, Reference, a, create, scim, token | [原文](<https://docs.langchain.com/langsmith/smith-api/scim-tokens/create-a-scim-token>) |
| `Monitor/Reference/LangSmith REST API/Administration/Create a new data plane.md` | Create a new data plane | Creates a new data plane object. Persists the rendered data plane spec, and returns 202 with the data plane in status=requested. Requires BYOC enabled org and org admin.；Administration, LangSmith REST API, Monitor, Reference, a, create, data, new, plane | [原文](<https://docs.langchain.com/langsmith/smith-api/data_planes/create-a-new-data-plane>) |
| `Monitor/Reference/LangSmith REST API/Administration/Create an access policy.md` | Create an access policy | Creates a new access policy.；Administration, LangSmith REST API, Monitor, Reference, access, an, create, policy | [原文](<https://docs.langchain.com/langsmith/smith-api/access_policies/create-an-access-policy>) |
| `Monitor/Reference/LangSmith REST API/Administration/Create customers and get stripe setup intent.md` | Create customers and get stripe setup intent | Administration, LangSmith REST API, Monitor, Reference, and, create, customers, get, intent, setup, stripe | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/create-customers-and-get-stripe-setup-intent>) |
| `Monitor/Reference/LangSmith REST API/Administration/Create onboarding state.md` | Create onboarding state | Initialize onboarding state for the current user.；Administration, LangSmith REST API, Monitor, Reference, create, onboarding, state | [原文](<https://docs.langchain.com/langsmith/smith-api/me/create-onboarding-state>) |
| `Monitor/Reference/LangSmith REST API/Administration/Create org personal access token.md` | Create org personal access token | Administration, LangSmith REST API, Monitor, Reference, access, create, org, personal, token | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/create-org-personal-access-token>) |
| `Monitor/Reference/LangSmith REST API/Administration/Create org service key.md` | Create org service key | Create org-scoped service key. If workspaces is None, key is org-wide.；Administration, LangSmith REST API, Monitor, Reference, create, key, org, service | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/create-org-service-key>) |
| `Monitor/Reference/LangSmith REST API/Administration/Create org tracing key.md` | Create org tracing key | Administration, LangSmith REST API, Monitor, Reference, create, key, org, tracing | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/create-org-tracing-key>) |
| `Monitor/Reference/LangSmith REST API/Administration/Create organization roles.md` | Create organization roles | Administration, LangSmith REST API, Monitor, Reference, create, organization, roles | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/create-organization-roles>) |
| `Monitor/Reference/LangSmith REST API/Administration/Create organization.md` | Create organization | Administration, LangSmith REST API, Monitor, Reference, create, organization | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/create-organization>) |
| `Monitor/Reference/LangSmith REST API/Administration/Create service account.md` | Create service account | Create a service account；Administration, LangSmith REST API, Monitor, Reference, account, create, service | [原文](<https://docs.langchain.com/langsmith/smith-api/service-accounts/create-service-account>) |
| `Monitor/Reference/LangSmith REST API/Administration/Create stripe checkout sessions endpoint.md` | Create stripe checkout sessions endpoint | Kick off a Stripe checkout session flow.；Administration, LangSmith REST API, Monitor, Reference, checkout, create, endpoint, sessions, stripe | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/create-stripe-checkout-sessions-endpoint>) |
| `Monitor/Reference/LangSmith REST API/Administration/Create tag key.md` | Create tag key | Administration, LangSmith REST API, Monitor, Reference, create, key, tag | [原文](<https://docs.langchain.com/langsmith/smith-api/workspaces/create-tag-key>) |
| `Monitor/Reference/LangSmith REST API/Administration/Create tag value.md` | Create tag value | Administration, LangSmith REST API, Monitor, Reference, create, tag, value | [原文](<https://docs.langchain.com/langsmith/smith-api/workspaces/create-tag-value>) |
| `Monitor/Reference/LangSmith REST API/Administration/Create tagging.md` | Create tagging | Administration, LangSmith REST API, Monitor, Reference, create, tagging | [原文](<https://docs.langchain.com/langsmith/smith-api/workspaces/create-tagging>) |
| `Monitor/Reference/LangSmith REST API/Administration/Create tenant.md` | Create tenant | Create a new organization and corresponding workspace.；Administration, LangSmith REST API, Monitor, Reference, create, tenant | [原文](<https://docs.langchain.com/langsmith/smith-api/tenant/create-tenant>) |
| `Monitor/Reference/LangSmith REST API/Administration/Create workspace.md` | Create workspace | Create a new workspace.；Administration, LangSmith REST API, Monitor, Reference, create, workspace | [原文](<https://docs.langchain.com/langsmith/smith-api/workspaces/create-workspace>) |
| `Monitor/Reference/LangSmith REST API/Administration/Delete API key.md` | Delete API key | Delete an api key for the user；Administration, LangSmith REST API, Monitor, Reference, api, delete, key | [原文](<https://docs.langchain.com/langsmith/smith-api/api-key/delete-api-key>) |
| `Monitor/Reference/LangSmith REST API/Administration/Delete SSO settings.md` | Delete SSO settings | Delete SSO provider settings for the current organization.；Administration, LangSmith REST API, Monitor, Reference, delete, settings, sso | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/delete-sso-settings>) |
| `Monitor/Reference/LangSmith REST API/Administration/Delete a SCIM token.md` | Delete a SCIM token | Delete a SCIM bearer token from the current organization.；Administration, LangSmith REST API, Monitor, Reference, a, delete, scim, token | [原文](<https://docs.langchain.com/langsmith/smith-api/scim-tokens/delete-a-scim-token>) |
| `Monitor/Reference/LangSmith REST API/Administration/Delete a data plane.md` | Delete a data plane | Verifies that the stored customer AWS role has delete permissions, that the stored Azure subscription is reachable, or that the stored GCP provisioner service account can be impersonated. Then removes linked workspaces and starts asynchronous deprovisioning for an active or provisioning_failed data plane owned by the caller's organization. Azure an；Administration, LangSmith REST API, Monitor, Reference, a, data, delete, plane | [原文](<https://docs.langchain.com/langsmith/smith-api/data_planes/delete-a-data-plane>) |
| `Monitor/Reference/LangSmith REST API/Administration/Delete an access policy.md` | Delete an access policy | Deletes a specific access policy by ID.；Administration, LangSmith REST API, Monitor, Reference, access, an, delete, policy | [原文](<https://docs.langchain.com/langsmith/smith-api/access_policies/delete-an-access-policy>) |
| `Monitor/Reference/LangSmith REST API/Administration/Delete current org pending member.md` | Delete current org pending member | When an admin deletes a pending member invite.；Administration, LangSmith REST API, Monitor, Reference, current, delete, member, org, pending | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/delete-current-org-pending-member>) |
| `Monitor/Reference/LangSmith REST API/Administration/Delete current workspace member.md` | Delete current workspace member | Administration, LangSmith REST API, Monitor, Reference, current, delete, member, workspace | [原文](<https://docs.langchain.com/langsmith/smith-api/workspaces/delete-current-workspace-member>) |
| `Monitor/Reference/LangSmith REST API/Administration/Delete current workspace pending member.md` | Delete current workspace pending member | Administration, LangSmith REST API, Monitor, Reference, current, delete, member, pending, workspace | [原文](<https://docs.langchain.com/langsmith/smith-api/workspaces/delete-current-workspace-pending-member>) |
| `Monitor/Reference/LangSmith REST API/Administration/Delete current workspace secret.md` | Delete current workspace secret | Delete a workspace secret and its allowed hosts. Missing keys succeed.；Administration, LangSmith REST API, Monitor, Reference, current, delete, secret, workspace | [原文](<https://docs.langchain.com/langsmith/smith-api/workspaces/delete-current-workspace-secret>) |
| `Monitor/Reference/LangSmith REST API/Administration/Delete org personal access token.md` | Delete org personal access token | Delete a personal access token, removing the record entirely.；Administration, LangSmith REST API, Monitor, Reference, access, delete, org, personal, token | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/delete-org-personal-access-token>) |
| `Monitor/Reference/LangSmith REST API/Administration/Delete org service key.md` | Delete org service key | Administration, LangSmith REST API, Monitor, Reference, delete, key, org, service | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/delete-org-service-key>) |
| `Monitor/Reference/LangSmith REST API/Administration/Delete org tracing key.md` | Delete org tracing key | Revoke your tracing key, or one you have permission to manage.；Administration, LangSmith REST API, Monitor, Reference, delete, key, org, tracing | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/delete-org-tracing-key>) |
| `Monitor/Reference/LangSmith REST API/Administration/Delete organization roles.md` | Delete organization roles | Administration, LangSmith REST API, Monitor, Reference, delete, organization, roles | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/delete-organization-roles>) |
| `Monitor/Reference/LangSmith REST API/Administration/Delete pending organization invite.md` | Delete pending organization invite | Administration, LangSmith REST API, Monitor, Reference, delete, invite, organization, pending | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/delete-pending-organization-invite>) |
| `Monitor/Reference/LangSmith REST API/Administration/Delete pending workspace invite.md` | Delete pending workspace invite | Administration, LangSmith REST API, Monitor, Reference, delete, invite, pending, workspace | [原文](<https://docs.langchain.com/langsmith/smith-api/workspaces/delete-pending-workspace-invite>) |
| `Monitor/Reference/LangSmith REST API/Administration/Delete personal access token.md` | Delete personal access token | DEPRECATED: Use /orgs/current/personal-access-tokens/{pat_id} instead；Administration, LangSmith REST API, Monitor, Reference, access, delete, personal, token | [原文](<https://docs.langchain.com/langsmith/smith-api/api-key/delete-personal-access-token>) |
| `Monitor/Reference/LangSmith REST API/Administration/Delete service account.md` | Delete service account | Delete a service account；Administration, LangSmith REST API, Monitor, Reference, account, delete, service | [原文](<https://docs.langchain.com/langsmith/smith-api/service-accounts/delete-service-account>) |
| `Monitor/Reference/LangSmith REST API/Administration/Delete tag key.md` | Delete tag key | Administration, LangSmith REST API, Monitor, Reference, delete, key, tag | [原文](<https://docs.langchain.com/langsmith/smith-api/workspaces/delete-tag-key>) |
| `Monitor/Reference/LangSmith REST API/Administration/Delete tag value.md` | Delete tag value | Administration, LangSmith REST API, Monitor, Reference, delete, tag, value | [原文](<https://docs.langchain.com/langsmith/smith-api/workspaces/delete-tag-value>) |
| `Monitor/Reference/LangSmith REST API/Administration/Delete tagging.md` | Delete tagging | Administration, LangSmith REST API, Monitor, Reference, delete, tagging | [原文](<https://docs.langchain.com/langsmith/smith-api/workspaces/delete-tagging>) |
| `Monitor/Reference/LangSmith REST API/Administration/Delete usage limit.md` | Delete usage limit | Delete a specific usage limit.；Administration, LangSmith REST API, Monitor, Reference, delete, limit, usage | [原文](<https://docs.langchain.com/langsmith/smith-api/usage-limits/delete-usage-limit>) |
| `Monitor/Reference/LangSmith REST API/Administration/Delete workspace.md` | Delete workspace | Delete a workspace and its data.；Administration, LangSmith REST API, Monitor, Reference, delete, workspace | [原文](<https://docs.langchain.com/langsmith/smith-api/workspaces/delete-workspace>) |
| `Monitor/Reference/LangSmith REST API/Administration/Detach access policies from a role.md` | Detach access policies from a role | Detaches one or more access policies from a specific role.；Administration, LangSmith REST API, Monitor, Reference, a, access, detach, from, policies, role | [原文](<https://docs.langchain.com/langsmith/smith-api/access_policies/detach-access-policies-from-a-role>) |
| `Monitor/Reference/LangSmith REST API/Administration/Export granular usage csv.md` | Export granular usage csv | Export granular usage data as CSV.；Administration, LangSmith REST API, Monitor, Reference, csv, export, granular, usage | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/export-granular-usage-csv>) |
| `Monitor/Reference/LangSmith REST API/Administration/Generate API key.md` | Generate API key | Generate an api key for the user.；Administration, LangSmith REST API, Monitor, Reference, api, generate, key | [原文](<https://docs.langchain.com/langsmith/smith-api/api-key/generate-api-key>) |
| `Monitor/Reference/LangSmith REST API/Administration/Generate personal access token.md` | Generate personal access token | DEPRECATED: Use /orgs/current/personal-access-tokens instead；Administration, LangSmith REST API, Monitor, Reference, access, generate, personal, token | [原文](<https://docs.langchain.com/langsmith/smith-api/api-key/generate-personal-access-token>) |
| `Monitor/Reference/LangSmith REST API/Administration/Get API keys.md` | Get API keys | Get the current tenant's API keys；Administration, LangSmith REST API, Monitor, Reference, api, get, keys | [原文](<https://docs.langchain.com/langsmith/smith-api/api-key/get-api-keys>) |
| `Monitor/Reference/LangSmith REST API/Administration/Get SSO settings.md` | Get SSO settings | Get SSO provider settings from login slug.；Administration, LangSmith REST API, Monitor, Reference, get, settings, sso | [原文](<https://docs.langchain.com/langsmith/smith-api/auth/get-sso-settings>) |
| `Monitor/Reference/LangSmith REST API/Administration/Get a SCIM token.md` | Get a SCIM token | Retrieve a specific SCIM token by ID for the current organization. The full token value is not returned.；Administration, LangSmith REST API, Monitor, Reference, a, get, scim, token | [原文](<https://docs.langchain.com/langsmith/smith-api/scim-tokens/get-a-scim-token>) |
| `Monitor/Reference/LangSmith REST API/Administration/Get a data plane.md` | Get a data plane | Returns a data plane and its saved provisioning settings in any lifecycle state. Requires BYOC and organization:infrastructure:read.；Administration, LangSmith REST API, Monitor, Reference, a, data, get, plane | [原文](<https://docs.langchain.com/langsmith/smith-api/data_planes/get-a-data-plane>) |
| `Monitor/Reference/LangSmith REST API/Administration/Get an access policy.md` | Get an access policy | Gets a specific access policy by ID.；Administration, LangSmith REST API, Monitor, Reference, access, an, get, policy | [原文](<https://docs.langchain.com/langsmith/smith-api/access_policies/get-an-access-policy>) |
| `Monitor/Reference/LangSmith REST API/Administration/Get audit logs.md` | Get audit logs | Retrieve audit log records for the authenticated user's organization in OCSF format.；Administration, LangSmith REST API, Monitor, Reference, audit, get, logs | [原文](<https://docs.langchain.com/langsmith/smith-api/audit-logs/get-audit-logs>) |
| `Monitor/Reference/LangSmith REST API/Administration/Get company info.md` | Get company info | Administration, LangSmith REST API, Monitor, Reference, company, get, info | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/get-company-info>) |
| `Monitor/Reference/LangSmith REST API/Administration/Get current SSO settings.md` | Get current SSO settings | Get SSO provider settings for the current organization.；Administration, LangSmith REST API, Monitor, Reference, current, get, settings, sso | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/get-current-sso-settings>) |
| `Monitor/Reference/LangSmith REST API/Administration/Get current active org members.md` | Get current active org members | Administration, LangSmith REST API, Monitor, Reference, active, current, get, members, org | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/get-current-active-org-members>) |
| `Monitor/Reference/LangSmith REST API/Administration/Get current active workspace members.md` | Get current active workspace members | Administration, LangSmith REST API, Monitor, Reference, active, current, get, members, workspace | [原文](<https://docs.langchain.com/langsmith/smith-api/workspaces/get-current-active-workspace-members>) |
| `Monitor/Reference/LangSmith REST API/Administration/Get current org members.md` | Get current org members | Administration, LangSmith REST API, Monitor, Reference, current, get, members, org | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/get-current-org-members>) |
| `Monitor/Reference/LangSmith REST API/Administration/Get current organization info (get-current-organization-info).md` | Get current organization info | Administration, LangSmith REST API, Monitor, Reference, current, get, info, organization | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/get-current-organization-info>) |
| `Monitor/Reference/LangSmith REST API/Administration/Get current organization info.md` | Get current organization info | Returns organization info for the authenticated user's current organization.；Administration, LangSmith REST API, Monitor, Reference, current, get, info, organization | [原文](<https://docs.langchain.com/langsmith/smith-api/organizations/get-current-organization-info>) |
| `Monitor/Reference/LangSmith REST API/Administration/Get current pending org members.md` | Get current pending org members | Administration, LangSmith REST API, Monitor, Reference, current, get, members, org, pending | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/get-current-pending-org-members>) |
| `Monitor/Reference/LangSmith REST API/Administration/Get current pending workspace members.md` | Get current pending workspace members | Administration, LangSmith REST API, Monitor, Reference, current, get, members, pending, workspace | [原文](<https://docs.langchain.com/langsmith/smith-api/workspaces/get-current-pending-workspace-members>) |
| `Monitor/Reference/LangSmith REST API/Administration/Get current user login methods.md` | Get current user login methods | Get login methods for the current user.；Administration, LangSmith REST API, Monitor, Reference, current, get, login, methods, user | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/get-current-user-login-methods>) |
| `Monitor/Reference/LangSmith REST API/Administration/Get current workspace encrypted secrets.md` | Get current workspace encrypted secrets | Get encrypted workspace secrets for use with Fleet and external services.；Administration, LangSmith REST API, Monitor, Reference, current, encrypted, get, secrets, workspace | [原文](<https://docs.langchain.com/langsmith/smith-api/workspaces/get-current-workspace-encrypted-secrets>) |
| `Monitor/Reference/LangSmith REST API/Administration/Get current workspace members.md` | Get current workspace members | Administration, LangSmith REST API, Monitor, Reference, current, get, members, workspace | [原文](<https://docs.langchain.com/langsmith/smith-api/workspaces/get-current-workspace-members>) |
| `Monitor/Reference/LangSmith REST API/Administration/Get current workspace stats.md` | Get current workspace stats | Administration, LangSmith REST API, Monitor, Reference, current, get, stats, workspace | [原文](<https://docs.langchain.com/langsmith/smith-api/workspaces/get-current-workspace-stats>) |
| `Monitor/Reference/LangSmith REST API/Administration/Get current workspace usage limits info.md` | Get current workspace usage limits info | Administration, LangSmith REST API, Monitor, Reference, current, get, info, limits, usage, workspace | [原文](<https://docs.langchain.com/langsmith/smith-api/workspaces/get-current-workspace-usage-limits-info>) |
| `Monitor/Reference/LangSmith REST API/Administration/Get dashboard.md` | Get dashboard | Administration, LangSmith REST API, Monitor, Reference, dashboard, get | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/get-dashboard>) |
| `Monitor/Reference/LangSmith REST API/Administration/Get granular usage.md` | Get granular usage | Get granular usage data with flexible grouping.；Administration, LangSmith REST API, Monitor, Reference, get, granular, usage | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/get-granular-usage>) |
| `Monitor/Reference/LangSmith REST API/Administration/Get ls user ID.md` | Get ls user ID | Get the LangSmith user ID for the current user.；Administration, LangSmith REST API, Monitor, Reference, get, id, ls, user | [原文](<https://docs.langchain.com/langsmith/smith-api/me/get-ls-user-id>) |
| `Monitor/Reference/LangSmith REST API/Administration/Get onboarding state.md` | Get onboarding state | Get onboarding state for the current user.；Administration, LangSmith REST API, Monitor, Reference, get, onboarding, state | [原文](<https://docs.langchain.com/langsmith/smith-api/me/get-onboarding-state>) |
| `Monitor/Reference/LangSmith REST API/Administration/Get org usage.md` | Get org usage | Administration, LangSmith REST API, Monitor, Reference, get, org, usage | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/get-org-usage>) |
| `Monitor/Reference/LangSmith REST API/Administration/Get organization billing info.md` | Get organization billing info | Administration, LangSmith REST API, Monitor, Reference, billing, get, info, organization | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/get-organization-billing-info>) |
| `Monitor/Reference/LangSmith REST API/Administration/Get organization info.md` | Get organization info | Administration, LangSmith REST API, Monitor, Reference, get, info, organization | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/get-organization-info>) |
| `Monitor/Reference/LangSmith REST API/Administration/Get personal access tokens.md` | Get personal access tokens | DEPRECATED: Use /orgs/current/personal-access-tokens instead；Administration, LangSmith REST API, Monitor, Reference, access, get, personal, tokens | [原文](<https://docs.langchain.com/langsmith/smith-api/api-key/get-personal-access-tokens>) |
| `Monitor/Reference/LangSmith REST API/Administration/Get public auth info.md` | Get public auth info | Returns public authentication information for the current workspace-level session.；Administration, LangSmith REST API, Monitor, Reference, auth, get, info, public | [原文](<https://docs.langchain.com/langsmith/smith-api/auth/get-public-auth-info>) |
| `Monitor/Reference/LangSmith REST API/Administration/Get service accounts.md` | Get service accounts | Get the current organization's service accounts.；Administration, LangSmith REST API, Monitor, Reference, accounts, get, service | [原文](<https://docs.langchain.com/langsmith/smith-api/service-accounts/get-service-accounts>) |
| `Monitor/Reference/LangSmith REST API/Administration/Get shared tokens.md` | Get shared tokens | List all shared entities and their tokens by the workspace.；Administration, LangSmith REST API, Monitor, Reference, get, shared, tokens | [原文](<https://docs.langchain.com/langsmith/smith-api/workspaces/get-shared-tokens>) |
| `Monitor/Reference/LangSmith REST API/Administration/Get tag key.md` | Get tag key | Administration, LangSmith REST API, Monitor, Reference, get, key, tag | [原文](<https://docs.langchain.com/langsmith/smith-api/workspaces/get-tag-key>) |
| `Monitor/Reference/LangSmith REST API/Administration/Get tag value.md` | Get tag value | Administration, LangSmith REST API, Monitor, Reference, get, tag, value | [原文](<https://docs.langchain.com/langsmith/smith-api/workspaces/get-tag-value>) |
| `Monitor/Reference/LangSmith REST API/Administration/Get the authenticated user's provider user ID.md` | Get the authenticated user's provider user ID | Returns the provider user ID associated with the authenticated user for a given provider type, or null if not set. Scoped to the current tenant.；Administration, LangSmith REST API, Monitor, Reference, authenticated, get, id, provider, the, user, users | [原文](<https://docs.langchain.com/langsmith/smith-api/me/get-the-authenticated-users-provider-user-id>) |
| `Monitor/Reference/LangSmith REST API/Administration/Get workspace TTL settings.md` | Get workspace TTL settings | Get the longlived trace TTL settings for a workspace；Administration, LangSmith REST API, Monitor, Reference, get, settings, ttl, workspace | [原文](<https://docs.langchain.com/langsmith/smith-api/ttl-settings/get-workspace-ttl-settings>) |
| `Monitor/Reference/LangSmith REST API/Administration/Get workspace.md` | Get workspace | Get a single workspace by ID, scoped to the current org and identity.；Administration, LangSmith REST API, Monitor, Reference, get, workspace | [原文](<https://docs.langchain.com/langsmith/smith-api/workspaces/get-workspace>) |
| `Monitor/Reference/LangSmith REST API/Administration/List SCIM tokens.md` | List SCIM tokens | List all SCIM bearer tokens for the current organization. The full token values are not returned.；Administration, LangSmith REST API, Monitor, Reference, list, scim, tokens | [原文](<https://docs.langchain.com/langsmith/smith-api/scim-tokens/list-scim-tokens>) |
| `Monitor/Reference/LangSmith REST API/Administration/List TTL settings (list-ttl-settings).md` | List TTL settings | List out the configured TTL settings for a given tenant.；Administration, LangSmith REST API, Monitor, Reference, list, settings, ttl | [原文](<https://docs.langchain.com/langsmith/smith-api/ttl-settings/list-ttl-settings>) |
| `Monitor/Reference/LangSmith REST API/Administration/List TTL settings.md` | List TTL settings | List out the configured TTL settings for a given org (org-level and tenant-level).；Administration, LangSmith REST API, Monitor, Reference, list, settings, ttl | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/list-ttl-settings>) |
| `Monitor/Reference/LangSmith REST API/Administration/List access policies.md` | List access policies | Lists all access policies for the organization.；Administration, LangSmith REST API, Monitor, Reference, access, list, policies | [原文](<https://docs.langchain.com/langsmith/smith-api/access_policies/list-access-policies>) |
| `Monitor/Reference/LangSmith REST API/Administration/List all org personal access tokens.md` | List all org personal access tokens | List every organization member's personal access tokens.；Administration, LangSmith REST API, Monitor, Reference, access, all, list, org, personal, tokens | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/list-all-org-personal-access-tokens>) |
| `Monitor/Reference/LangSmith REST API/Administration/List audit log operations.md` | List audit log operations | List all possible audit log operation names, for populating filter UI.；Administration, LangSmith REST API, Monitor, Reference, audit, list, log, operations | [原文](<https://docs.langchain.com/langsmith/smith-api/audit-logs/list-audit-log-operations>) |
| `Monitor/Reference/LangSmith REST API/Administration/List current workspace secrets.md` | List current workspace secrets | Administration, LangSmith REST API, Monitor, Reference, current, list, secrets, workspace | [原文](<https://docs.langchain.com/langsmith/smith-api/workspaces/list-current-workspace-secrets>) |
| `Monitor/Reference/LangSmith REST API/Administration/List data planes for the current organization.md` | List data planes for the current organization | Returns up to 50 data planes owned by the caller's organization across all lifecycle states. Sorted by status priority (active first), then newest first. Requires BYOC to be enabled for the org.；Administration, LangSmith REST API, Monitor, Reference, current, data, for, list, organization, planes, the | [原文](<https://docs.langchain.com/langsmith/smith-api/data_planes/list-data-planes-for-the-current-organization>) |
| `Monitor/Reference/LangSmith REST API/Administration/List org members with workspace roles.md` | List org members with workspace roles | Returns a paginated list of org members (active and pending) enriched with workspace memberships.；Administration, LangSmith REST API, Monitor, Reference, list, members, org, roles, with, workspace | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/list-org-members-with-workspace-roles>) |
| `Monitor/Reference/LangSmith REST API/Administration/List org personal access tokens.md` | List org personal access tokens | Administration, LangSmith REST API, Monitor, Reference, access, list, org, personal, tokens | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/list-org-personal-access-tokens>) |
| `Monitor/Reference/LangSmith REST API/Administration/List org service keys.md` | List org service keys | Administration, LangSmith REST API, Monitor, Reference, keys, list, org, service | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/list-org-service-keys>) |
| `Monitor/Reference/LangSmith REST API/Administration/List org tracing keys.md` | List org tracing keys | List your tracing keys and keys visible through organization/workspace access.；Administration, LangSmith REST API, Monitor, Reference, keys, list, org, tracing | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/list-org-tracing-keys>) |
| `Monitor/Reference/LangSmith REST API/Administration/List org usage limits.md` | List org usage limits | List out the configured usage limits for a given organization.；Administration, LangSmith REST API, Monitor, Reference, limits, list, org, usage | [原文](<https://docs.langchain.com/langsmith/smith-api/usage-limits/list-org-usage-limits>) |
| `Monitor/Reference/LangSmith REST API/Administration/List organization roles.md` | List organization roles | Administration, LangSmith REST API, Monitor, Reference, list, organization, roles | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/list-organization-roles>) |
| `Monitor/Reference/LangSmith REST API/Administration/List organizations.md` | List organizations | Get all orgs visible to this auth；Administration, LangSmith REST API, Monitor, Reference, list, organizations | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/list-organizations>) |
| `Monitor/Reference/LangSmith REST API/Administration/List pending organization invites.md` | List pending organization invites | Get all pending orgs visible to this auth；Administration, LangSmith REST API, Monitor, Reference, invites, list, organization, pending | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/list-pending-organization-invites>) |
| `Monitor/Reference/LangSmith REST API/Administration/List pending workspace invites.md` | List pending workspace invites | Get all workspaces visible to this auth；Administration, LangSmith REST API, Monitor, Reference, invites, list, pending, workspace | [原文](<https://docs.langchain.com/langsmith/smith-api/workspaces/list-pending-workspace-invites>) |
| `Monitor/Reference/LangSmith REST API/Administration/List permissions.md` | List permissions | Administration, LangSmith REST API, Monitor, Reference, list, permissions | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/list-permissions>) |
| `Monitor/Reference/LangSmith REST API/Administration/List tag keys.md` | List tag keys | Administration, LangSmith REST API, Monitor, Reference, keys, list, tag | [原文](<https://docs.langchain.com/langsmith/smith-api/workspaces/list-tag-keys>) |
| `Monitor/Reference/LangSmith REST API/Administration/List tag values.md` | List tag values | Administration, LangSmith REST API, Monitor, Reference, list, tag, values | [原文](<https://docs.langchain.com/langsmith/smith-api/workspaces/list-tag-values>) |
| `Monitor/Reference/LangSmith REST API/Administration/List taggings.md` | List taggings | Administration, LangSmith REST API, Monitor, Reference, list, taggings | [原文](<https://docs.langchain.com/langsmith/smith-api/workspaces/list-taggings>) |
| `Monitor/Reference/LangSmith REST API/Administration/List tags for resource.md` | List tags for resource | Administration, LangSmith REST API, Monitor, Reference, for, list, resource, tags | [原文](<https://docs.langchain.com/langsmith/smith-api/workspaces/list-tags-for-resource>) |
| `Monitor/Reference/LangSmith REST API/Administration/List tags for resources.md` | List tags for resources | Administration, LangSmith REST API, Monitor, Reference, for, list, resources, tags | [原文](<https://docs.langchain.com/langsmith/smith-api/workspaces/list-tags-for-resources>) |
| `Monitor/Reference/LangSmith REST API/Administration/List tags.md` | List tags | Administration, LangSmith REST API, Monitor, Reference, list, tags | [原文](<https://docs.langchain.com/langsmith/smith-api/workspaces/list-tags>) |
| `Monitor/Reference/LangSmith REST API/Administration/List tenants.md` | List tenants | Get all tenants visible to this auth；Administration, LangSmith REST API, Monitor, Reference, list, tenants | [原文](<https://docs.langchain.com/langsmith/smith-api/tenant/list-tenants>) |
| `Monitor/Reference/LangSmith REST API/Administration/List usage limits.md` | List usage limits | List out the configured usage limits for a given tenant.；Administration, LangSmith REST API, Monitor, Reference, limits, list, usage | [原文](<https://docs.langchain.com/langsmith/smith-api/usage-limits/list-usage-limits>) |
| `Monitor/Reference/LangSmith REST API/Administration/List workspaces.md` | List workspaces | Get all workspaces visible to this auth in the current org. Does not create a new workspace/org.；Administration, LangSmith REST API, Monitor, Reference, list, workspaces | [原文](<https://docs.langchain.com/langsmith/smith-api/workspaces/list-workspaces>) |
| `Monitor/Reference/LangSmith REST API/Administration/Login.md` | Login | Administration, LangSmith REST API, Monitor, Reference, login | [原文](<https://docs.langchain.com/langsmith/smith-api/auth/login>) |
| `Monitor/Reference/LangSmith REST API/Administration/Lookup SSO by email.md` | Lookup SSO by email | Look up SSO providers available for a SCIM-provisioned email address.；Administration, LangSmith REST API, Monitor, Reference, by, email, lookup, sso | [原文](<https://docs.langchain.com/langsmith/smith-api/auth/lookup-sso-by-email>) |
| `Monitor/Reference/LangSmith REST API/Administration/On payment method created.md` | On payment method created | Administration, LangSmith REST API, Monitor, Reference, created, method, on, payment | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/on-payment-method-created>) |
| `Monitor/Reference/LangSmith REST API/Administration/Patch current org pending member.md` | Patch current org pending member | Update the role on a pending org member invite.；Administration, LangSmith REST API, Monitor, Reference, current, member, org, patch, pending | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/patch-current-org-pending-member>) |
| `Monitor/Reference/LangSmith REST API/Administration/Patch current workspace member.md` | Patch current workspace member | Administration, LangSmith REST API, Monitor, Reference, current, member, patch, workspace | [原文](<https://docs.langchain.com/langsmith/smith-api/workspaces/patch-current-workspace-member>) |
| `Monitor/Reference/LangSmith REST API/Administration/Patch current workspace pending member.md` | Patch current workspace pending member | Update the role on a pending workspace member invite.；Administration, LangSmith REST API, Monitor, Reference, current, member, patch, pending, workspace | [原文](<https://docs.langchain.com/langsmith/smith-api/workspaces/patch-current-workspace-pending-member>) |
| `Monitor/Reference/LangSmith REST API/Administration/Patch workspace.md` | Patch workspace | Rename a workspace in the current organization.；Administration, LangSmith REST API, Monitor, Reference, patch, workspace | [原文](<https://docs.langchain.com/langsmith/smith-api/workspaces/patch-workspace>) |
| `Monitor/Reference/LangSmith REST API/Administration/Put current workspace secret.md` | Put current workspace secret | Create or update a workspace secret and the hosts it may be sent to.；Administration, LangSmith REST API, Monitor, Reference, current, put, secret, workspace | [原文](<https://docs.langchain.com/langsmith/smith-api/workspaces/put-current-workspace-secret>) |
| `Monitor/Reference/LangSmith REST API/Administration/Reinstate org personal access token.md` | Reinstate org personal access token | Lift a revocation, so the personal access token authenticates again.；Administration, LangSmith REST API, Monitor, Reference, access, org, personal, reinstate, token | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/reinstate-org-personal-access-token>) |
| `Monitor/Reference/LangSmith REST API/Administration/Remove member from current org.md` | Remove member from current org | Remove a user from the current organization.；Administration, LangSmith REST API, Monitor, Reference, current, from, member, org, remove | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/remove-member-from-current-org>) |
| `Monitor/Reference/LangSmith REST API/Administration/Revoke org personal access token.md` | Revoke org personal access token | Revoke a personal access token, so it stops working but its record remains.；Administration, LangSmith REST API, Monitor, Reference, access, org, personal, revoke, token | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/revoke-org-personal-access-token>) |
| `Monitor/Reference/LangSmith REST API/Administration/Send SSO email confirmation.md` | Send SSO email confirmation | Send an email to confirm the email address for an SSO user.；Administration, LangSmith REST API, Monitor, Reference, confirmation, email, send, sso | [原文](<https://docs.langchain.com/langsmith/smith-api/auth/send-sso-email-confirmation>) |
| `Monitor/Reference/LangSmith REST API/Administration/Set company info.md` | Set company info | Administration, LangSmith REST API, Monitor, Reference, company, info, set | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/set-company-info>) |
| `Monitor/Reference/LangSmith REST API/Administration/Set default SSO provision.md` | Set default SSO provision | Set the current organization as the default for SSO provisioning in self-hosted environments.；Administration, LangSmith REST API, Monitor, Reference, default, provision, set, sso | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/set-default-sso-provision>) |
| `Monitor/Reference/LangSmith REST API/Administration/Set role restriction.md` | Set role restriction | Administration, LangSmith REST API, Monitor, Reference, restriction, role, set | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/set-role-restriction>) |
| `Monitor/Reference/LangSmith REST API/Administration/Update SSO settings.md` | Update SSO settings | Update SSO provider settings defaults for the current organization.；Administration, LangSmith REST API, Monitor, Reference, settings, sso, update | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/update-sso-settings>) |
| `Monitor/Reference/LangSmith REST API/Administration/Update a SCIM token.md` | Update a SCIM token | Update the description of an existing SCIM token for the current organization.；Administration, LangSmith REST API, Monitor, Reference, a, scim, token, update | [原文](<https://docs.langchain.com/langsmith/smith-api/scim-tokens/update-a-scim-token>) |
| `Monitor/Reference/LangSmith REST API/Administration/Update allowed login methods.md` | Update allowed login methods | Update allowed login methods for the current organization.；Administration, LangSmith REST API, Monitor, Reference, allowed, login, methods, update | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/update-allowed-login-methods>) |
| `Monitor/Reference/LangSmith REST API/Administration/Update an access policy.md` | Update an access policy | Updates one or more fields on an access policy.；Administration, LangSmith REST API, Monitor, Reference, access, an, policy, update | [原文](<https://docs.langchain.com/langsmith/smith-api/access_policies/update-an-access-policy>) |
| `Monitor/Reference/LangSmith REST API/Administration/Update current org member.md` | Update current org member | This is used for updating a user's role (all auth modes) or full_name/password (basic auth)；Administration, LangSmith REST API, Monitor, Reference, current, member, org, update | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/update-current-org-member>) |
| `Monitor/Reference/LangSmith REST API/Administration/Update current organization info.md` | Update current organization info | Administration, LangSmith REST API, Monitor, Reference, current, info, organization, update | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/update-current-organization-info>) |
| `Monitor/Reference/LangSmith REST API/Administration/Update current user.md` | Update current user | Update a user's full_name/password (basic auth only)；Administration, LangSmith REST API, Monitor, Reference, current, update, user | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/update-current-user>) |
| `Monitor/Reference/LangSmith REST API/Administration/Update data plane settings.md` | Update data plane settings | Update specific settings for a data plane owned by the caller's organization.；Administration, LangSmith REST API, Monitor, Reference, data, plane, settings, update | [原文](<https://docs.langchain.com/langsmith/smith-api/data_planes/update-data-plane-settings>) |
| `Monitor/Reference/LangSmith REST API/Administration/Update onboarding state field.md` | Update onboarding state field | Update a specific onboarding completion field for the current user.；Administration, LangSmith REST API, Monitor, Reference, field, onboarding, state, update | [原文](<https://docs.langchain.com/langsmith/smith-api/me/update-onboarding-state-field>) |
| `Monitor/Reference/LangSmith REST API/Administration/Update org service key.md` | Update org service key | Update an API key's role(s) in place without rotating the key.；Administration, LangSmith REST API, Monitor, Reference, key, org, service, update | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/update-org-service-key>) |
| `Monitor/Reference/LangSmith REST API/Administration/Update organization roles.md` | Update organization roles | Administration, LangSmith REST API, Monitor, Reference, organization, roles, update | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/update-organization-roles>) |
| `Monitor/Reference/LangSmith REST API/Administration/Update tag key.md` | Update tag key | Administration, LangSmith REST API, Monitor, Reference, key, tag, update | [原文](<https://docs.langchain.com/langsmith/smith-api/workspaces/update-tag-key>) |
| `Monitor/Reference/LangSmith REST API/Administration/Update tag value.md` | Update tag value | Administration, LangSmith REST API, Monitor, Reference, tag, update, value | [原文](<https://docs.langchain.com/langsmith/smith-api/workspaces/update-tag-value>) |
| `Monitor/Reference/LangSmith REST API/Administration/Update workspace TTL settings.md` | Update workspace TTL settings | Update the longlived trace TTL for a workspace.；Administration, LangSmith REST API, Monitor, Reference, settings, ttl, update, workspace | [原文](<https://docs.langchain.com/langsmith/smith-api/ttl-settings/update-workspace-ttl-settings>) |
| `Monitor/Reference/LangSmith REST API/Administration/Upsert TTL settings (upsert-ttl-settings).md` | Upsert TTL settings | Administration, LangSmith REST API, Monitor, Reference, settings, ttl, upsert | [原文](<https://docs.langchain.com/langsmith/smith-api/ttl-settings/upsert-ttl-settings>) |
| `Monitor/Reference/LangSmith REST API/Administration/Upsert TTL settings.md` | Upsert TTL settings | Administration, LangSmith REST API, Monitor, Reference, settings, ttl, upsert | [原文](<https://docs.langchain.com/langsmith/smith-api/orgs/upsert-ttl-settings>) |
| `Monitor/Reference/LangSmith REST API/Administration/Upsert current workspace secrets.md` | Upsert current workspace secrets | Administration, LangSmith REST API, Monitor, Reference, current, secrets, upsert, workspace | [原文](<https://docs.langchain.com/langsmith/smith-api/workspaces/upsert-current-workspace-secrets>) |
| `Monitor/Reference/LangSmith REST API/Administration/Upsert usage limit.md` | Upsert usage limit | Create a new usage limit.；Administration, LangSmith REST API, Monitor, Reference, limit, upsert, usage | [原文](<https://docs.langchain.com/langsmith/smith-api/usage-limits/upsert-usage-limit>) |
| `Monitor/Reference/LangSmith REST API/Datasets/Clone dataset.md` | Clone dataset | Copy examples from a source dataset into an existing target dataset.；Datasets, LangSmith REST API, Monitor, Reference, clone, dataset | [原文](<https://docs.langchain.com/langsmith/smith-api/datasets/clone-dataset>) |
| `Monitor/Reference/LangSmith REST API/Datasets/Count examples.md` | Count examples | Count the examples that match the filters.；Datasets, LangSmith REST API, Monitor, Reference, count, examples | [原文](<https://docs.langchain.com/langsmith/smith-api/examples/count-examples>) |
| `Monitor/Reference/LangSmith REST API/Datasets/Create comparative experiment.md` | Create comparative experiment | Create a comparative experiment.；Datasets, LangSmith REST API, Monitor, Reference, comparative, create, experiment | [原文](<https://docs.langchain.com/langsmith/smith-api/datasets/create-comparative-experiment>) |
| `Monitor/Reference/LangSmith REST API/Datasets/Create dataset.md` | Create dataset | Create a new dataset.；Datasets, LangSmith REST API, Monitor, Reference, create, dataset | [原文](<https://docs.langchain.com/langsmith/smith-api/datasets/create-dataset>) |
| `Monitor/Reference/LangSmith REST API/Datasets/Create example.md` | Create example | Create a new example.；Datasets, LangSmith REST API, Monitor, Reference, create, example | [原文](<https://docs.langchain.com/langsmith/smith-api/examples/create-example>) |
| `Monitor/Reference/LangSmith REST API/Datasets/Create examples.md` | Create examples | Create bulk examples.；Datasets, LangSmith REST API, Monitor, Reference, create, examples | [原文](<https://docs.langchain.com/langsmith/smith-api/examples/create-examples>) |
| `Monitor/Reference/LangSmith REST API/Datasets/Delete an example.md` | Delete an example | Soft-delete an example, preserving prior versions and their attachments. If the latest version is already deleted, the request succeeds without creating another version. Deletion is recorded at the current time or just after the latest version, whichever is later. For future-dated versions, latest reads reflect deletion immediately; timestamp reads；Datasets, LangSmith REST API, Monitor, Reference, an, delete, example | [原文](<https://docs.langchain.com/langsmith/smith-api/examples/delete-an-example>) |
| `Monitor/Reference/LangSmith REST API/Datasets/Delete comparative experiment.md` | Delete comparative experiment | Delete a specific comparative experiment.；Datasets, LangSmith REST API, Monitor, Reference, comparative, delete, experiment | [原文](<https://docs.langchain.com/langsmith/smith-api/datasets/delete-comparative-experiment>) |
| `Monitor/Reference/LangSmith REST API/Datasets/Delete dataset.md` | Delete dataset | Delete a specific dataset.；Datasets, LangSmith REST API, Monitor, Reference, dataset, delete | [原文](<https://docs.langchain.com/langsmith/smith-api/datasets/delete-dataset>) |
| `Monitor/Reference/LangSmith REST API/Datasets/Delete datasets.md` | Delete datasets | Delete multiple datasets.；Datasets, LangSmith REST API, Monitor, Reference, datasets, delete | [原文](<https://docs.langchain.com/langsmith/smith-api/datasets/delete-datasets>) |
| `Monitor/Reference/LangSmith REST API/Datasets/Delete example.md` | Delete example | Soft delete an example. Only deletes the example in the 'latest' version of the dataset.；Datasets, LangSmith REST API, Monitor, Reference, delete, example | [原文](<https://docs.langchain.com/langsmith/smith-api/examples/delete-example>) |
| `Monitor/Reference/LangSmith REST API/Datasets/Delete examples.md` | Delete examples | Soft delete examples. Only deletes the examples in the 'latest' version of the dataset.；Datasets, LangSmith REST API, Monitor, Reference, delete, examples | [原文](<https://docs.langchain.com/langsmith/smith-api/examples/delete-examples>) |
| `Monitor/Reference/LangSmith REST API/Datasets/Diff dataset versions.md` | Diff dataset versions | Get diff between two dataset versions.；Datasets, LangSmith REST API, Monitor, Reference, dataset, diff, versions | [原文](<https://docs.langchain.com/langsmith/smith-api/datasets/diff-dataset-versions>) |
| `Monitor/Reference/LangSmith REST API/Datasets/Download dataset csv.md` | Download dataset csv | Download a dataset as CSV format.；Datasets, LangSmith REST API, Monitor, Reference, csv, dataset, download | [原文](<https://docs.langchain.com/langsmith/smith-api/datasets/download-dataset-csv>) |
| `Monitor/Reference/LangSmith REST API/Datasets/Download dataset jsonl.md` | Download dataset jsonl | Download a dataset as CSV format.；Datasets, LangSmith REST API, Monitor, Reference, dataset, download, jsonl | [原文](<https://docs.langchain.com/langsmith/smith-api/datasets/download-dataset-jsonl>) |
| `Monitor/Reference/LangSmith REST API/Datasets/Download dataset openai ft.md` | Download dataset openai ft | Download a dataset as OpenAI Jsonl format.；Datasets, LangSmith REST API, Monitor, Reference, dataset, download, ft, openai | [原文](<https://docs.langchain.com/langsmith/smith-api/datasets/download-dataset-openai-ft>) |
| `Monitor/Reference/LangSmith REST API/Datasets/Download dataset openai.md` | Download dataset openai | Download a dataset as OpenAI Evals Jsonl format.；Datasets, LangSmith REST API, Monitor, Reference, dataset, download, openai | [原文](<https://docs.langchain.com/langsmith/smith-api/datasets/download-dataset-openai>) |
| `Monitor/Reference/LangSmith REST API/Datasets/Fetch experiment runs for dataset examples.md` | Fetch experiment runs for dataset examples | Returns a paginated page of dataset examples with runs from the requested experiments.；Datasets, LangSmith REST API, Monitor, Reference, dataset, examples, experiment, fetch, for, runs | [原文](<https://docs.langchain.com/langsmith/smith-api/datasets/fetch-experiment-runs-for-dataset-examples>) |
| `Monitor/Reference/LangSmith REST API/Datasets/Fetch shared experiment runs for dataset examples.md` | Fetch shared experiment runs for dataset examples | Public share-token variant of POST /v2/datasets/{dataset_id}/experiment-runs.；Datasets, LangSmith REST API, Monitor, Reference, dataset, examples, experiment, fetch, for, runs, shared | [原文](<https://docs.langchain.com/langsmith/smith-api/datasets/fetch-shared-experiment-runs-for-dataset-examples>) |
| `Monitor/Reference/LangSmith REST API/Datasets/Generate.md` | Generate | Generate synthetic examples for a dataset.；Datasets, LangSmith REST API, Monitor, Reference, generate | [原文](<https://docs.langchain.com/langsmith/smith-api/datasets/generate>) |
| `Monitor/Reference/LangSmith REST API/Datasets/Get dataset splits.md` | Get dataset splits | List the split names a dataset's examples belong to.；Datasets, LangSmith REST API, Monitor, Reference, dataset, get, splits | [原文](<https://docs.langchain.com/langsmith/smith-api/datasets/get-dataset-splits>) |
| `Monitor/Reference/LangSmith REST API/Datasets/Get dataset version.md` | Get dataset version | Get dataset version by as_of or exact tag.；Datasets, LangSmith REST API, Monitor, Reference, dataset, get, version | [原文](<https://docs.langchain.com/langsmith/smith-api/datasets/get-dataset-version>) |
| `Monitor/Reference/LangSmith REST API/Datasets/Get dataset versions.md` | Get dataset versions | Get dataset versions.；Datasets, LangSmith REST API, Monitor, Reference, dataset, get, versions | [原文](<https://docs.langchain.com/langsmith/smith-api/datasets/get-dataset-versions>) |
| `Monitor/Reference/LangSmith REST API/Datasets/Hard delete examples.md` | Hard delete examples | This endpoint hard deletes *all* versions of a dataset example(s).；Datasets, LangSmith REST API, Monitor, Reference, delete, examples, hard | [原文](<https://docs.langchain.com/langsmith/smith-api/examples/hard-delete-examples>) |
| `Monitor/Reference/LangSmith REST API/Datasets/Legacy update examples.md` | Legacy update examples | Legacy update examples in bulk. For update involving attachments, use PATCH /v1/platform/datasets/{dataset_id}/examples instead.；Datasets, LangSmith REST API, Monitor, Reference, examples, legacy, update | [原文](<https://docs.langchain.com/langsmith/smith-api/examples/legacy-update-examples>) |
| `Monitor/Reference/LangSmith REST API/Datasets/Read dataset share state.md` | Read dataset share state | Get a dataset's share token.；Datasets, LangSmith REST API, Monitor, Reference, dataset, read, share, state | [原文](<https://docs.langchain.com/langsmith/smith-api/datasets/read-dataset-share-state>) |
| `Monitor/Reference/LangSmith REST API/Datasets/Read dataset.md` | Read dataset | Get a specific dataset.；Datasets, LangSmith REST API, Monitor, Reference, dataset, read | [原文](<https://docs.langchain.com/langsmith/smith-api/datasets/read-dataset>) |
| `Monitor/Reference/LangSmith REST API/Datasets/Read datasets stream.md` | Read datasets stream | Stream all datasets by query params and owner as JSON patches.；Datasets, LangSmith REST API, Monitor, Reference, datasets, read, stream | [原文](<https://docs.langchain.com/langsmith/smith-api/datasets/read-datasets-stream>) |
| `Monitor/Reference/LangSmith REST API/Datasets/Read datasets.md` | Read datasets | Get all datasets by query params and owner.；Datasets, LangSmith REST API, Monitor, Reference, datasets, read | [原文](<https://docs.langchain.com/langsmith/smith-api/datasets/read-datasets>) |
| `Monitor/Reference/LangSmith REST API/Datasets/Read example.md` | Read example | Get a specific example.；Datasets, LangSmith REST API, Monitor, Reference, example, read | [原文](<https://docs.langchain.com/langsmith/smith-api/examples/read-example>) |
| `Monitor/Reference/LangSmith REST API/Datasets/Read examples with runs.md` | Read examples with runs | Fetch examples for a dataset, and fetch the runs for each example if they are associated with the given session_ids.；Datasets, LangSmith REST API, Monitor, Reference, examples, read, runs, with | [原文](<https://docs.langchain.com/langsmith/smith-api/datasets/read-examples-with-runs>) |
| `Monitor/Reference/LangSmith REST API/Datasets/Read examples.md` | Read examples | Get all examples by query params；Datasets, LangSmith REST API, Monitor, Reference, examples, read | [原文](<https://docs.langchain.com/langsmith/smith-api/examples/read-examples>) |
| `Monitor/Reference/LangSmith REST API/Datasets/Share dataset.md` | Share dataset | Share a dataset publicly and return its share token.；Datasets, LangSmith REST API, Monitor, Reference, dataset, share | [原文](<https://docs.langchain.com/langsmith/smith-api/datasets/share-dataset>) |
| `Monitor/Reference/LangSmith REST API/Datasets/Studio experiment.md` | Studio experiment | Datasets, LangSmith REST API, Monitor, Reference, experiment, studio | [原文](<https://docs.langchain.com/langsmith/smith-api/datasets/studio-experiment>) |
| `Monitor/Reference/LangSmith REST API/Datasets/Unshare dataset.md` | Unshare dataset | Stop sharing a dataset.；Datasets, LangSmith REST API, Monitor, Reference, dataset, unshare | [原文](<https://docs.langchain.com/langsmith/smith-api/datasets/unshare-dataset>) |
| `Monitor/Reference/LangSmith REST API/Datasets/Update dataset splits.md` | Update dataset splits | Add examples to a split, or remove them from it.；Datasets, LangSmith REST API, Monitor, Reference, dataset, splits, update | [原文](<https://docs.langchain.com/langsmith/smith-api/datasets/update-dataset-splits>) |
| `Monitor/Reference/LangSmith REST API/Datasets/Update dataset version.md` | Update dataset version | Tag a dataset version.；Datasets, LangSmith REST API, Monitor, Reference, dataset, update, version | [原文](<https://docs.langchain.com/langsmith/smith-api/datasets/update-dataset-version>) |
| `Monitor/Reference/LangSmith REST API/Datasets/Update dataset.md` | Update dataset | Update a dataset.；Datasets, LangSmith REST API, Monitor, Reference, dataset, update | [原文](<https://docs.langchain.com/langsmith/smith-api/datasets/update-dataset>) |
| `Monitor/Reference/LangSmith REST API/Datasets/Update example.md` | Update example | Update a specific example.；Datasets, LangSmith REST API, Monitor, Reference, example, update | [原文](<https://docs.langchain.com/langsmith/smith-api/examples/update-example>) |
| `Monitor/Reference/LangSmith REST API/Datasets/Update examples.md` | Update examples | This endpoint allows clients to update existing examples in a specified dataset by sending a multipart/form-data PATCH request.；Datasets, LangSmith REST API, Monitor, Reference, examples, update | [原文](<https://docs.langchain.com/langsmith/smith-api/examples/update-examples>) |
| `Monitor/Reference/LangSmith REST API/Datasets/Upload csv dataset.md` | Upload csv dataset | Create a new dataset from a CSV or JSONL file.；Datasets, LangSmith REST API, Monitor, Reference, csv, dataset, upload | [原文](<https://docs.langchain.com/langsmith/smith-api/datasets/upload-csv-dataset>) |
| `Monitor/Reference/LangSmith REST API/Datasets/Upload examples from csv.md` | Upload examples from csv | Upload examples from a CSV file.；Datasets, LangSmith REST API, Monitor, Reference, csv, examples, from, upload | [原文](<https://docs.langchain.com/langsmith/smith-api/examples/upload-examples-from-csv>) |
| `Monitor/Reference/LangSmith REST API/Datasets/Upload examples.md` | Upload examples | This endpoint allows clients to upload examples to a specified dataset by sending a multipart/form-data POST request.；Datasets, LangSmith REST API, Monitor, Reference, examples, upload | [原文](<https://docs.langchain.com/langsmith/smith-api/examples/upload-examples>) |
| `Monitor/Reference/LangSmith REST API/Datasets/Upload experiment.md` | Upload experiment | Upload an experiment that has already been run.；Datasets, LangSmith REST API, Monitor, Reference, experiment, upload | [原文](<https://docs.langchain.com/langsmith/smith-api/datasets/upload-experiment>) |
| `Monitor/Reference/LangSmith REST API/Datasets/Validate example.md` | Validate example | Validate an example.；Datasets, LangSmith REST API, Monitor, Reference, example, validate | [原文](<https://docs.langchain.com/langsmith/smith-api/examples/validate-example>) |
| `Monitor/Reference/LangSmith REST API/Datasets/Validate examples.md` | Validate examples | Validate examples in bulk.；Datasets, LangSmith REST API, Monitor, Reference, examples, validate | [原文](<https://docs.langchain.com/langsmith/smith-api/examples/validate-examples>) |
| `Monitor/Reference/LangSmith REST API/Evaluation/Bulk delete evaluators.md` | Bulk delete evaluators | Delete multiple evaluators by their IDs. Returns per-item success/failure.；Evaluation, LangSmith REST API, Monitor, Reference, bulk, delete, evaluators | [原文](<https://docs.langchain.com/langsmith/smith-api/evaluators/bulk-delete-evaluators>) |
| `Monitor/Reference/LangSmith REST API/Evaluation/Create evaluator.md` | Create evaluator | Create a new LLM or code evaluator for the current workspace.；Evaluation, LangSmith REST API, Monitor, Reference, create, evaluator | [原文](<https://docs.langchain.com/langsmith/smith-api/evaluators/create-evaluator>) |
| `Monitor/Reference/LangSmith REST API/Evaluation/Create new experiment view override configuration for a dataset.md` | Create new experiment view override configuration for a dataset | Creates a new experiment view override configuration for a dataset with column display settings.；Evaluation, LangSmith REST API, Monitor, Reference, a, configuration, create, dataset, experiment, for, new, override, view | [原文](<https://docs.langchain.com/langsmith/smith-api/experiment-view-overrides/create-new-experiment-view-override-configuration-for-a-dataset>) |
| `Monitor/Reference/LangSmith REST API/Evaluation/Delete evaluator.md` | Delete evaluator | Delete an evaluator. Returns 409 when a code evaluator build is ENQUEUED or BUILDING, or when run rules still reference the evaluator and delete_run_rules is false. When delete_run_rules is true, all run rules referencing this evaluator are deleted first (same tenant) if the build is not in flight. Associated llm_evaluators and code_evaluators rows；Evaluation, LangSmith REST API, Monitor, Reference, delete, evaluator | [原文](<https://docs.langchain.com/langsmith/smith-api/evaluators/delete-evaluator>) |
| `Monitor/Reference/LangSmith REST API/Evaluation/Delete experiment view override configuration.md` | Delete experiment view override configuration | Permanently deletes an experiment view override configuration for a dataset.；Evaluation, LangSmith REST API, Monitor, Reference, configuration, delete, experiment, override, view | [原文](<https://docs.langchain.com/langsmith/smith-api/experiment-view-overrides/delete-experiment-view-override-configuration>) |
| `Monitor/Reference/LangSmith REST API/Evaluation/Evaluate experiment adhoc.md` | Evaluate experiment adhoc | Evaluate an existing experiment with a specific evaluator.；Evaluation, LangSmith REST API, Monitor, Reference, adhoc, evaluate, experiment | [原文](<https://docs.langchain.com/langsmith/smith-api/experiments/evaluate-experiment-adhoc>) |
| `Monitor/Reference/LangSmith REST API/Evaluation/Get evaluator spend.md` | Get evaluator spend | Returns per-day LLM evaluator spend for the requested 7-day period, grouped by evaluator, resource, or run rule. Exactly one of group_by, evaluator_id, session_id, or dataset_id is required. resource_id, type, feedback_key, tag_value_id, and agent_id may be supplied with group_by to narrow listing aggregations.；Evaluation, LangSmith REST API, Monitor, Reference, evaluator, get, spend | [原文](<https://docs.langchain.com/langsmith/smith-api/evaluators/get-evaluator-spend>) |
| `Monitor/Reference/LangSmith REST API/Evaluation/Get evaluator.md` | Get evaluator | Retrieve a single evaluator by its ID.；Evaluation, LangSmith REST API, Monitor, Reference, evaluator, get | [原文](<https://docs.langchain.com/langsmith/smith-api/evaluators/get-evaluator>) |
| `Monitor/Reference/LangSmith REST API/Evaluation/Get experiment view override configuration by specific ID.md` | Get experiment view override configuration by specific ID | Retrieves a specific experiment view override configuration using both dataset ID and override ID.；Evaluation, LangSmith REST API, Monitor, Reference, by, configuration, experiment, get, id, override, specific, view | [原文](<https://docs.langchain.com/langsmith/smith-api/experiment-view-overrides/get-experiment-view-override-configuration-by-specific-id>) |
| `Monitor/Reference/LangSmith REST API/Evaluation/Get experiment view override configurations for a dataset.md` | Get experiment view override configurations for a dataset | Retrieves all experiment view override configurations for a specific dataset.；Evaluation, LangSmith REST API, Monitor, Reference, a, configurations, dataset, experiment, for, get, override, view | [原文](<https://docs.langchain.com/langsmith/smith-api/experiment-view-overrides/get-experiment-view-override-configurations-for-a-dataset>) |
| `Monitor/Reference/LangSmith REST API/Evaluation/List evaluators.md` | List evaluators | List evaluators for the current workspace, with optional filtering by type, name, tag, feedback key, or resource ID.；Evaluation, LangSmith REST API, Monitor, Reference, evaluators, list | [原文](<https://docs.langchain.com/langsmith/smith-api/evaluators/list-evaluators>) |
| `Monitor/Reference/LangSmith REST API/Evaluation/Update evaluator.md` | Update evaluator | Update an existing evaluator's name, LLM configuration, or code configuration. Returns 409 when a code evaluator build is ENQUEUED or BUILDING.；Evaluation, LangSmith REST API, Monitor, Reference, evaluator, update | [原文](<https://docs.langchain.com/langsmith/smith-api/evaluators/update-evaluator>) |
| `Monitor/Reference/LangSmith REST API/Evaluation/Update existing experiment view override configuration.md` | Update existing experiment view override configuration | Updates an existing experiment view override configuration by completely replacing；Evaluation, LangSmith REST API, Monitor, Reference, configuration, existing, experiment, override, update, view | [原文](<https://docs.langchain.com/langsmith/smith-api/experiment-view-overrides/update-existing-experiment-view-override-configuration>) |
| `Monitor/Reference/LangSmith REST API/Feedback & Annotation/Add a reviewer to an annotation queue.md` | Add a reviewer to an annotation queue | Assigns a single identity as a reviewer for the queue. Idempotent.；Feedback & Annotation, LangSmith REST API, Monitor, Reference, a, add, an, annotation, queue, reviewer, to | [原文](<https://docs.langchain.com/langsmith/smith-api/annotation_queues/add-a-reviewer-to-an-annotation-queue>) |
| `Monitor/Reference/LangSmith REST API/Feedback & Annotation/Add annotation queue items.md` | Add annotation queue items | Add RUN or THREAD items to a single annotation queue. RUN items require run_id unless they are created from a suggested example. THREAD items require thread_id and project_id.；Feedback & Annotation, LangSmith REST API, Monitor, Reference, add, annotation, items, queue | [原文](<https://docs.langchain.com/langsmith/smith-api/annotation_queues/add-annotation-queue-items>) |
| `Monitor/Reference/LangSmith REST API/Feedback & Annotation/Add runs to annotation queue by key.md` | Add runs to annotation queue by key | Self-hosted deployments require LangSmith `v0.16` or later.；Feedback & Annotation, LangSmith REST API, Monitor, Reference, add, annotation, by, key, queue, runs, to | [原文](<https://docs.langchain.com/langsmith/smith-api/annotation-queues/add-runs-to-annotation-queue-by-key>) |
| `Monitor/Reference/LangSmith REST API/Feedback & Annotation/Add runs to annotation queue.md` | Add runs to annotation queue | Feedback & Annotation, LangSmith REST API, Monitor, Reference, add, annotation, queue, runs, to | [原文](<https://docs.langchain.com/langsmith/smith-api/annotation-queues/add-runs-to-annotation-queue>) |
| `Monitor/Reference/LangSmith REST API/Feedback & Annotation/Create annotation queue item status.md` | Create annotation queue item status | Log the caller's reviewer status for a RUN or THREAD annotation queue item. A null status re-shows the item for this reviewer.；Feedback & Annotation, LangSmith REST API, Monitor, Reference, annotation, create, item, queue, status | [原文](<https://docs.langchain.com/langsmith/smith-api/annotation_queues/create-annotation-queue-item-status>) |
| `Monitor/Reference/LangSmith REST API/Feedback & Annotation/Create annotation queue.md` | Create annotation queue | Feedback & Annotation, LangSmith REST API, Monitor, Reference, annotation, create, queue | [原文](<https://docs.langchain.com/langsmith/smith-api/annotation-queues/create-annotation-queue>) |
| `Monitor/Reference/LangSmith REST API/Feedback & Annotation/Create feedback config endpoint.md` | Create feedback config endpoint | Feedback & Annotation, LangSmith REST API, Monitor, Reference, config, create, endpoint, feedback | [原文](<https://docs.langchain.com/langsmith/smith-api/feedback-configs/create-feedback-config-endpoint>) |
| `Monitor/Reference/LangSmith REST API/Feedback & Annotation/Create feedback formula ep.md` | Create feedback formula ep | Create a new feedback formula；Feedback & Annotation, LangSmith REST API, Monitor, Reference, create, ep, feedback, formula | [原文](<https://docs.langchain.com/langsmith/smith-api/feedback/create-feedback-formula-ep>) |
| `Monitor/Reference/LangSmith REST API/Feedback & Annotation/Create feedback ingest token.md` | Create feedback ingest token | Create a new feedback ingest token.；Feedback & Annotation, LangSmith REST API, Monitor, Reference, create, feedback, ingest, token | [原文](<https://docs.langchain.com/langsmith/smith-api/feedback/create-feedback-ingest-token>) |
| `Monitor/Reference/LangSmith REST API/Feedback & Annotation/Create feedback with token get.md` | Create feedback with token get | Create a new feedback with a token.；Feedback & Annotation, LangSmith REST API, Monitor, Reference, create, feedback, get, token, with | [原文](<https://docs.langchain.com/langsmith/smith-api/feedback/create-feedback-with-token-get>) |
| `Monitor/Reference/LangSmith REST API/Feedback & Annotation/Create feedback with token post.md` | Create feedback with token post | Submit feedback for the token's run and key. The token is the credential, so anyone with it can submit feedback.；Feedback & Annotation, LangSmith REST API, Monitor, Reference, create, feedback, post, token, with | [原文](<https://docs.langchain.com/langsmith/smith-api/feedback/create-feedback-with-token-post>) |
| `Monitor/Reference/LangSmith REST API/Feedback & Annotation/Create feedback.md` | Create feedback | Create a new feedback.；Feedback & Annotation, LangSmith REST API, Monitor, Reference, create, feedback | [原文](<https://docs.langchain.com/langsmith/smith-api/feedback/create-feedback>) |
| `Monitor/Reference/LangSmith REST API/Feedback & Annotation/Create identity annotation queue run status.md` | Create identity annotation queue run status | Feedback & Annotation, LangSmith REST API, Monitor, Reference, annotation, create, identity, queue, run, status | [原文](<https://docs.langchain.com/langsmith/smith-api/annotation-queues/create-identity-annotation-queue-run-status>) |
| `Monitor/Reference/LangSmith REST API/Feedback & Annotation/Delete annotation queue items.md` | Delete annotation queue items | Remove RUN or THREAD items from a single annotation queue by item ID. Both active and completed items can be removed.；Feedback & Annotation, LangSmith REST API, Monitor, Reference, annotation, delete, items, queue | [原文](<https://docs.langchain.com/langsmith/smith-api/annotation_queues/delete-annotation-queue-items>) |
| `Monitor/Reference/LangSmith REST API/Feedback & Annotation/Delete annotation queue.md` | Delete annotation queue | Feedback & Annotation, LangSmith REST API, Monitor, Reference, annotation, delete, queue | [原文](<https://docs.langchain.com/langsmith/smith-api/annotation-queues/delete-annotation-queue>) |
| `Monitor/Reference/LangSmith REST API/Feedback & Annotation/Delete annotation queues.md` | Delete annotation queues | Delete multiple annotation queues with partial success support.；Feedback & Annotation, LangSmith REST API, Monitor, Reference, annotation, delete, queues | [原文](<https://docs.langchain.com/langsmith/smith-api/annotation-queues/delete-annotation-queues>) |
| `Monitor/Reference/LangSmith REST API/Feedback & Annotation/Delete feedback config endpoint.md` | Delete feedback config endpoint | Soft delete one feedback config by id, or every config of a feedback key.；Feedback & Annotation, LangSmith REST API, Monitor, Reference, config, delete, endpoint, feedback | [原文](<https://docs.langchain.com/langsmith/smith-api/feedback-configs/delete-feedback-config-endpoint>) |
| `Monitor/Reference/LangSmith REST API/Feedback & Annotation/Delete feedback formula endpoint.md` | Delete feedback formula endpoint | Delete a feedback formula by id；Feedback & Annotation, LangSmith REST API, Monitor, Reference, delete, endpoint, feedback, formula | [原文](<https://docs.langchain.com/langsmith/smith-api/feedback/delete-feedback-formula-endpoint>) |
| `Monitor/Reference/LangSmith REST API/Feedback & Annotation/Delete feedback.md` | Delete feedback | Delete a feedback.；Feedback & Annotation, LangSmith REST API, Monitor, Reference, delete, feedback | [原文](<https://docs.langchain.com/langsmith/smith-api/feedback/delete-feedback>) |
| `Monitor/Reference/LangSmith REST API/Feedback & Annotation/Delete run from annotation queue.md` | Delete run from annotation queue | Feedback & Annotation, LangSmith REST API, Monitor, Reference, annotation, delete, from, queue, run | [原文](<https://docs.langchain.com/langsmith/smith-api/annotation-queues/delete-run-from-annotation-queue>) |
| `Monitor/Reference/LangSmith REST API/Feedback & Annotation/Delete runs from annotation queue.md` | Delete runs from annotation queue | Feedback & Annotation, LangSmith REST API, Monitor, Reference, annotation, delete, from, queue, runs | [原文](<https://docs.langchain.com/langsmith/smith-api/annotation-queues/delete-runs-from-annotation-queue>) |
| `Monitor/Reference/LangSmith REST API/Feedback & Annotation/Export annotation queue archived runs.md` | Export annotation queue archived runs | Feedback & Annotation, LangSmith REST API, Monitor, Reference, annotation, archived, export, queue, runs | [原文](<https://docs.langchain.com/langsmith/smith-api/annotation-queues/export-annotation-queue-archived-runs>) |
| `Monitor/Reference/LangSmith REST API/Feedback & Annotation/Get annotation queue item placement.md` | Get annotation queue item placement | Resolve a RUN or THREAD item to its current review section and zero-based position for deep linking. The returned cursor counts RUN and THREAD items together, so it is only valid for a list request with no item_type or start-time filter.；Feedback & Annotation, LangSmith REST API, Monitor, Reference, annotation, get, item, placement, queue | [原文](<https://docs.langchain.com/langsmith/smith-api/annotation_queues/get-annotation-queue-item-placement>) |
| `Monitor/Reference/LangSmith REST API/Feedback & Annotation/Get annotation queue.md` | Get annotation queue | Feedback & Annotation, LangSmith REST API, Monitor, Reference, annotation, get, queue | [原文](<https://docs.langchain.com/langsmith/smith-api/annotation-queues/get-annotation-queue>) |
| `Monitor/Reference/LangSmith REST API/Feedback & Annotation/Get annotation queues for run.md` | Get annotation queues for run | Feedback & Annotation, LangSmith REST API, Monitor, Reference, annotation, for, get, queues, run | [原文](<https://docs.langchain.com/langsmith/smith-api/annotation-queues/get-annotation-queues-for-run>) |
| `Monitor/Reference/LangSmith REST API/Feedback & Annotation/Get annotation queues.md` | Get annotation queues | Feedback & Annotation, LangSmith REST API, Monitor, Reference, annotation, get, queues | [原文](<https://docs.langchain.com/langsmith/smith-api/annotation-queues/get-annotation-queues>) |
| `Monitor/Reference/LangSmith REST API/Feedback & Annotation/Get feedback formula ep.md` | Get feedback formula ep | Get a feedback formula by id；Feedback & Annotation, LangSmith REST API, Monitor, Reference, ep, feedback, formula, get | [原文](<https://docs.langchain.com/langsmith/smith-api/feedback/get-feedback-formula-ep>) |
| `Monitor/Reference/LangSmith REST API/Feedback & Annotation/Get run from annotation queue.md` | Get run from annotation queue | Get a run from an annotation queue；Feedback & Annotation, LangSmith REST API, Monitor, Reference, annotation, from, get, queue, run | [原文](<https://docs.langchain.com/langsmith/smith-api/annotation-queues/get-run-from-annotation-queue>) |
| `Monitor/Reference/LangSmith REST API/Feedback & Annotation/Get runs from annotation queue.md` | Get runs from annotation queue | Feedback & Annotation, LangSmith REST API, Monitor, Reference, annotation, from, get, queue, runs | [原文](<https://docs.langchain.com/langsmith/smith-api/annotation-queues/get-runs-from-annotation-queue>) |
| `Monitor/Reference/LangSmith REST API/Feedback & Annotation/Get size from annotation queue.md` | Get size from annotation queue | Feedback & Annotation, LangSmith REST API, Monitor, Reference, annotation, from, get, queue, size | [原文](<https://docs.langchain.com/langsmith/smith-api/annotation-queues/get-size-from-annotation-queue>) |
| `Monitor/Reference/LangSmith REST API/Feedback & Annotation/Get the annotation queue item count.md` | Get the annotation queue item count | Returns the number of annotation queue items in one status bucket. The two time windows are independent: start_time/end_time bound when an item was archived, min_start_time/max_start_time bound when its trace ran. Items with no trace start time are excluded when either of the latter is set.；Feedback & Annotation, LangSmith REST API, Monitor, Reference, annotation, count, get, item, queue, the | [原文](<https://docs.langchain.com/langsmith/smith-api/annotation_queues/get-the-annotation-queue-item-count>) |
| `Monitor/Reference/LangSmith REST API/Feedback & Annotation/Get total archived from annotation queue.md` | Get total archived from annotation queue | Feedback & Annotation, LangSmith REST API, Monitor, Reference, annotation, archived, from, get, queue, total | [原文](<https://docs.langchain.com/langsmith/smith-api/annotation-queues/get-total-archived-from-annotation-queue>) |
| `Monitor/Reference/LangSmith REST API/Feedback & Annotation/Get total size from annotation queue.md` | Get total size from annotation queue | Feedback & Annotation, LangSmith REST API, Monitor, Reference, annotation, from, get, queue, size, total | [原文](<https://docs.langchain.com/langsmith/smith-api/annotation-queues/get-total-size-from-annotation-queue>) |
| `Monitor/Reference/LangSmith REST API/Feedback & Annotation/List annotation queue items.md` | List annotation queue items | List RUN and THREAD items in a single annotation queue for one review status section, with opaque cursor pagination. Optional item_type=RUN\|THREAD filters the page. Optional min_start_time/max_start_time bound the item's trace start time; items with no start time are excluded when either bound is set. direction=backward returns items before the sup；Feedback & Annotation, LangSmith REST API, Monitor, Reference, annotation, items, list, queue | [原文](<https://docs.langchain.com/langsmith/smith-api/annotation_queues/list-annotation-queue-items>) |
| `Monitor/Reference/LangSmith REST API/Feedback & Annotation/List feedback configs endpoint.md` | List feedback configs endpoint | Feedback & Annotation, LangSmith REST API, Monitor, Reference, configs, endpoint, feedback, list | [原文](<https://docs.langchain.com/langsmith/smith-api/feedback-configs/list-feedback-configs-endpoint>) |
| `Monitor/Reference/LangSmith REST API/Feedback & Annotation/List feedback formula ep.md` | List feedback formula ep | List feedback formulas for a given dataset or tracing project；Feedback & Annotation, LangSmith REST API, Monitor, Reference, ep, feedback, formula, list | [原文](<https://docs.langchain.com/langsmith/smith-api/feedback/list-feedback-formula-ep>) |
| `Monitor/Reference/LangSmith REST API/Feedback & Annotation/List feedback ingest tokens.md` | List feedback ingest tokens | List all feedback ingest tokens for a run.；Feedback & Annotation, LangSmith REST API, Monitor, Reference, feedback, ingest, list, tokens | [原文](<https://docs.langchain.com/langsmith/smith-api/feedback/list-feedback-ingest-tokens>) |
| `Monitor/Reference/LangSmith REST API/Feedback & Annotation/Populate annotation queue.md` | Populate annotation queue | Populate annotation queue with runs from an experiment.；Feedback & Annotation, LangSmith REST API, Monitor, Reference, annotation, populate, queue | [原文](<https://docs.langchain.com/langsmith/smith-api/annotation-queues/populate-annotation-queue>) |
| `Monitor/Reference/LangSmith REST API/Feedback & Annotation/Read feedback.md` | Read feedback | Get a specific feedback.；Feedback & Annotation, LangSmith REST API, Monitor, Reference, feedback, read | [原文](<https://docs.langchain.com/langsmith/smith-api/feedback/read-feedback>) |
| `Monitor/Reference/LangSmith REST API/Feedback & Annotation/Read feedbacks.md` | Read feedbacks | List all Feedback by query params.；Feedback & Annotation, LangSmith REST API, Monitor, Reference, feedbacks, read | [原文](<https://docs.langchain.com/langsmith/smith-api/feedback/read-feedbacks>) |
| `Monitor/Reference/LangSmith REST API/Feedback & Annotation/Remove a reviewer from an annotation queue.md` | Remove a reviewer from an annotation queue | Unassigns an identity as a reviewer for the queue. Idempotent.；Feedback & Annotation, LangSmith REST API, Monitor, Reference, a, an, annotation, from, queue, remove, reviewer | [原文](<https://docs.langchain.com/langsmith/smith-api/annotation_queues/remove-a-reviewer-from-an-annotation-queue>) |
| `Monitor/Reference/LangSmith REST API/Feedback & Annotation/Resolve annotation queue run.md` | Resolve annotation queue run | Resolve a queue run ID to its section and run data for deep linking.；Feedback & Annotation, LangSmith REST API, Monitor, Reference, annotation, queue, resolve, run | [原文](<https://docs.langchain.com/langsmith/smith-api/annotation-queues/resolve-annotation-queue-run>) |
| `Monitor/Reference/LangSmith REST API/Feedback & Annotation/Update an annotation queue item.md` | Update an annotation queue item | Partially update mutable timestamps (added_at, last_reviewed_time) for a RUN or THREAD annotation queue item. Omit a field, or pass JSON null, to leave it unchanged.；Feedback & Annotation, LangSmith REST API, Monitor, Reference, an, annotation, item, queue, update | [原文](<https://docs.langchain.com/langsmith/smith-api/annotation_queues/update-an-annotation-queue-item>) |
| `Monitor/Reference/LangSmith REST API/Feedback & Annotation/Update annotation queue.md` | Update annotation queue | Feedback & Annotation, LangSmith REST API, Monitor, Reference, annotation, queue, update | [原文](<https://docs.langchain.com/langsmith/smith-api/annotation-queues/update-annotation-queue>) |
| `Monitor/Reference/LangSmith REST API/Feedback & Annotation/Update feedback config endpoint.md` | Update feedback config endpoint | Feedback & Annotation, LangSmith REST API, Monitor, Reference, config, endpoint, feedback, update | [原文](<https://docs.langchain.com/langsmith/smith-api/feedback-configs/update-feedback-config-endpoint>) |
| `Monitor/Reference/LangSmith REST API/Feedback & Annotation/Update feedback formula ep.md` | Update feedback formula ep | Update a feedback formula；Feedback & Annotation, LangSmith REST API, Monitor, Reference, ep, feedback, formula, update | [原文](<https://docs.langchain.com/langsmith/smith-api/feedback/update-feedback-formula-ep>) |
| `Monitor/Reference/LangSmith REST API/Feedback & Annotation/Update feedback.md` | Update feedback | Replace an existing feedback entry with a new, modified entry.；Feedback & Annotation, LangSmith REST API, Monitor, Reference, feedback, update | [原文](<https://docs.langchain.com/langsmith/smith-api/feedback/update-feedback>) |
| `Monitor/Reference/LangSmith REST API/Feedback & Annotation/Update run in annotation queue.md` | Update run in annotation queue | Feedback & Annotation, LangSmith REST API, Monitor, Reference, annotation, in, queue, run, update | [原文](<https://docs.langchain.com/langsmith/smith-api/annotation-queues/update-run-in-annotation-queue>) |
| `Monitor/Reference/LangSmith REST API/Integrations & Tools/Approve OAuth2 authorization request.md` | Approve OAuth2 authorization request | Issues an authorization code after the authenticated user approves the request. Called by the frontend consent page. Requires authentication.；Integrations & Tools, LangSmith REST API, Monitor, Reference, approve, authorization, oauth2, request | [原文](<https://docs.langchain.com/langsmith/smith-api/oauth/approve-oauth2-authorization-request>) |
| `Monitor/Reference/LangSmith REST API/Integrations & Tools/Authorize a device code.md` | Authorize a device code | Marks a device code as authorized for the authenticated user. Called by the /activate page when the user enters their user code. Requires authentication.；Integrations & Tools, LangSmith REST API, Monitor, Reference, a, authorize, code, device | [原文](<https://docs.langchain.com/langsmith/smith-api/oauth/authorize-a-device-code>) |
| `Monitor/Reference/LangSmith REST API/Integrations & Tools/Create a tool.md` | Create a tool | Creates a new tool in the workspace.；Integrations & Tools, LangSmith REST API, Monitor, Reference, a, create, tool | [原文](<https://docs.langchain.com/langsmith/smith-api/tools/create-a-tool>) |
| `Monitor/Reference/LangSmith REST API/Integrations & Tools/Create an oauth client.md` | Create an oauth client | Registers a new OAuth 2.0 / OIDC client owned by the caller's organization. For confidential clients the response includes a client_secret that is shown only once.；Integrations & Tools, LangSmith REST API, Monitor, Reference, an, client, create, oauth | [原文](<https://docs.langchain.com/langsmith/smith-api/oauth/create-an-oauth-client>) |
| `Monitor/Reference/LangSmith REST API/Integrations & Tools/Create vendor settings.md` | Create vendor settings | Initializes vendor settings.；Integrations & Tools, LangSmith REST API, Monitor, Reference, create, settings, vendor | [原文](<https://docs.langchain.com/langsmith/smith-api/mcp_vendors/create-vendor-settings>) |
| `Monitor/Reference/LangSmith REST API/Integrations & Tools/Delete a tool by ID.md` | Delete a tool by ID | Deletes a tool identified by its UUID.；Integrations & Tools, LangSmith REST API, Monitor, Reference, a, by, delete, id, tool | [原文](<https://docs.langchain.com/langsmith/smith-api/tools/delete-a-tool-by-id>) |
| `Monitor/Reference/LangSmith REST API/Integrations & Tools/Delete a tool by handle.md` | Delete a tool by handle | Deletes a tool identified by its handle.；Integrations & Tools, LangSmith REST API, Monitor, Reference, a, by, delete, handle, tool | [原文](<https://docs.langchain.com/langsmith/smith-api/tools/delete-a-tool-by-handle>) |
| `Monitor/Reference/LangSmith REST API/Integrations & Tools/Delete an oauth client.md` | Delete an oauth client | Integrations & Tools, LangSmith REST API, Monitor, Reference, an, client, delete, oauth | [原文](<https://docs.langchain.com/langsmith/smith-api/oauth/delete-an-oauth-client>) |
| `Monitor/Reference/LangSmith REST API/Integrations & Tools/Delete vendor settings.md` | Delete vendor settings | Removes vendor settings.；Integrations & Tools, LangSmith REST API, Monitor, Reference, delete, settings, vendor | [原文](<https://docs.langchain.com/langsmith/smith-api/mcp_vendors/delete-vendor-settings>) |
| `Monitor/Reference/LangSmith REST API/Integrations & Tools/Exchange grant for OAuth2 tokens.md` | Exchange grant for OAuth2 tokens | Token endpoint that dispatches by grant_type: authorization_code, urn:ietf:params:oauth:grant-type:device_code, or refresh_token.；Integrations & Tools, LangSmith REST API, Monitor, Reference, exchange, for, grant, oauth2, tokens | [原文](<https://docs.langchain.com/langsmith/smith-api/oauth/exchange-grant-for-oauth2-tokens>) |
| `Monitor/Reference/LangSmith REST API/Integrations & Tools/Get MCP vendor.md` | Get MCP vendor | Returns vendor metadata and current settings.；Integrations & Tools, LangSmith REST API, Monitor, Reference, get, mcp, vendor | [原文](<https://docs.langchain.com/langsmith/smith-api/mcp_vendors/get-mcp-vendor>) |
| `Monitor/Reference/LangSmith REST API/Integrations & Tools/Get OAuth2 authorization server metadata.md` | Get OAuth2 authorization server metadata | Returns OAuth2 authorization server metadata per RFC 8414, including supported endpoints, grant types, and response types.；Integrations & Tools, LangSmith REST API, Monitor, Reference, authorization, get, metadata, oauth2, server | [原文](<https://docs.langchain.com/langsmith/smith-api/oauth/get-oauth2-authorization-server-metadata>) |
| `Monitor/Reference/LangSmith REST API/Integrations & Tools/Get a tool by ID.md` | Get a tool by ID | Returns a tool identified by its UUID.；Integrations & Tools, LangSmith REST API, Monitor, Reference, a, by, get, id, tool | [原文](<https://docs.langchain.com/langsmith/smith-api/tools/get-a-tool-by-id>) |
| `Monitor/Reference/LangSmith REST API/Integrations & Tools/Get a tool by handle.md` | Get a tool by handle | Returns a tool identified by its handle.；Integrations & Tools, LangSmith REST API, Monitor, Reference, a, by, get, handle, tool | [原文](<https://docs.langchain.com/langsmith/smith-api/tools/get-a-tool-by-handle>) |
| `Monitor/Reference/LangSmith REST API/Integrations & Tools/Get agent builder integrations settings.md` | Get agent builder integrations settings | Returns default policy, integration overrides, and known integrations for the current workspace.；Integrations & Tools, LangSmith REST API, Monitor, Reference, agent, builder, get, integrations, settings | [原文](<https://docs.langchain.com/langsmith/smith-api/integrations/get-agent-builder-integrations-settings>) |
| `Monitor/Reference/LangSmith REST API/Integrations & Tools/Get an oauth client.md` | Get an oauth client | Integrations & Tools, LangSmith REST API, Monitor, Reference, an, client, get, oauth | [原文](<https://docs.langchain.com/langsmith/smith-api/oauth/get-an-oauth-client>) |
| `Monitor/Reference/LangSmith REST API/Integrations & Tools/Get openid connect provider configuration.md` | Get openid connect provider configuration | Returns the OpenID Connect discovery document (OpenID Connect Discovery 1.0), advertising the authorization, token, userinfo, and JWKS endpoints plus supported scopes, response types, and signing algorithms.；Integrations & Tools, LangSmith REST API, Monitor, Reference, configuration, connect, get, openid, provider | [原文](<https://docs.langchain.com/langsmith/smith-api/oauth/get-openid-connect-provider-configuration>) |
| `Monitor/Reference/LangSmith REST API/Integrations & Tools/Get openid connect userinfo.md` | Get openid connect userinfo | Returns identity claims for the user represented by a LangSmith access token whose audience is the identity resource or the API resource. The token is passed as a Bearer credential in the Authorization header (OpenID Connect Core 1.0 §5.3).；Integrations & Tools, LangSmith REST API, Monitor, Reference, connect, get, openid, userinfo | [原文](<https://docs.langchain.com/langsmith/smith-api/oauth/get-openid-connect-userinfo>) |
| `Monitor/Reference/LangSmith REST API/Integrations & Tools/Get public OAuth2 client metadata.md` | Get public OAuth2 client metadata | Returns the display metadata (name, logo, homepage/terms/privacy links) for a registered OAuth2 client. Used by the consent screen to show a human-readable client identity instead of the raw client_id. Public endpoint; exposes only non-sensitive display fields.；Integrations & Tools, LangSmith REST API, Monitor, Reference, client, get, metadata, oauth2, public | [原文](<https://docs.langchain.com/langsmith/smith-api/oauth/get-public-oauth2-client-metadata>) |
| `Monitor/Reference/LangSmith REST API/Integrations & Tools/Get tools.md` | Get tools | Return MCP tools — from cache if fresh, otherwise by fetching from remote.；Integrations & Tools, LangSmith REST API, Monitor, Reference, get, tools | [原文](<https://docs.langchain.com/langsmith/smith-api/mcp/get-tools>) |
| `Monitor/Reference/LangSmith REST API/Integrations & Tools/Get vendor account.md` | Get vendor account | Resolves OAuth token and returns the vendor's account info.；Integrations & Tools, LangSmith REST API, Monitor, Reference, account, get, vendor | [原文](<https://docs.langchain.com/langsmith/smith-api/mcp_vendors/get-vendor-account>) |
| `Monitor/Reference/LangSmith REST API/Integrations & Tools/Get vendor settings.md` | Get vendor settings | Returns the current vendor-specific settings.；Integrations & Tools, LangSmith REST API, Monitor, Reference, get, settings, vendor | [原文](<https://docs.langchain.com/langsmith/smith-api/mcp_vendors/get-vendor-settings>) |
| `Monitor/Reference/LangSmith REST API/Integrations & Tools/Initiate OAuth2 authorization.md` | Initiate OAuth2 authorization | Validates authorization request parameters and redirects to the frontend consent page per RFC 6749.；Integrations & Tools, LangSmith REST API, Monitor, Reference, authorization, initiate, oauth2 | [原文](<https://docs.langchain.com/langsmith/smith-api/oauth/initiate-oauth2-authorization>) |
| `Monitor/Reference/LangSmith REST API/Integrations & Tools/Invalidate tools cache.md` | Invalidate tools cache | Invalidate cached MCP tools for a given server URL.；Integrations & Tools, LangSmith REST API, Monitor, Reference, cache, invalidate, tools | [原文](<https://docs.langchain.com/langsmith/smith-api/mcp/invalidate-tools-cache>) |
| `Monitor/Reference/LangSmith REST API/Integrations & Tools/List MCP servers for a vendor.md` | List MCP servers for a vendor | Returns the MCP gateways from the vendor for the workspace's configured org/project.；Integrations & Tools, LangSmith REST API, Monitor, Reference, a, for, list, mcp, servers, vendor | [原文](<https://docs.langchain.com/langsmith/smith-api/mcp_vendors/list-mcp-servers-for-a-vendor>) |
| `Monitor/Reference/LangSmith REST API/Integrations & Tools/List MCP vendors.md` | List MCP vendors | Returns the catalog of available MCP vendors.；Integrations & Tools, LangSmith REST API, Monitor, Reference, list, mcp, vendors | [原文](<https://docs.langchain.com/langsmith/smith-api/mcp_vendors/list-mcp-vendors>) |
| `Monitor/Reference/LangSmith REST API/Integrations & Tools/List authorized applications.md` | List authorized applications | Lists the third-party applications the authenticated user has authorized to sign in with LangSmith.；Integrations & Tools, LangSmith REST API, Monitor, Reference, applications, authorized, list | [原文](<https://docs.langchain.com/langsmith/smith-api/oauth/list-authorized-applications>) |
| `Monitor/Reference/LangSmith REST API/Integrations & Tools/List oauth clients.md` | List oauth clients | Lists the OAuth clients owned by the caller's organization.；Integrations & Tools, LangSmith REST API, Monitor, Reference, clients, list, oauth | [原文](<https://docs.langchain.com/langsmith/smith-api/oauth/list-oauth-clients>) |
| `Monitor/Reference/LangSmith REST API/Integrations & Tools/List tools for a vendor.md` | List tools for a vendor | Returns the tool catalog for this vendor.；Integrations & Tools, LangSmith REST API, Monitor, Reference, a, for, list, tools, vendor | [原文](<https://docs.langchain.com/langsmith/smith-api/mcp_vendors/list-tools-for-a-vendor>) |
| `Monitor/Reference/LangSmith REST API/Integrations & Tools/List tools.md` | List tools | Returns a paginated list of tools in the workspace.；Integrations & Tools, LangSmith REST API, Monitor, Reference, list, tools | [原文](<https://docs.langchain.com/langsmith/smith-api/tools/list-tools>) |
| `Monitor/Reference/LangSmith REST API/Integrations & Tools/Proxy get.md` | Proxy get | Integrations & Tools, LangSmith REST API, Monitor, Reference, get, proxy | [原文](<https://docs.langchain.com/langsmith/smith-api/mcp/proxy-get>) |
| `Monitor/Reference/LangSmith REST API/Integrations & Tools/Proxy.md` | Proxy | Integrations & Tools, LangSmith REST API, Monitor, Reference, proxy | [原文](<https://docs.langchain.com/langsmith/smith-api/mcp/proxy>) |
| `Monitor/Reference/LangSmith REST API/Integrations & Tools/Register an OAuth2 dynamic client.md` | Register an OAuth2 dynamic client | Public RFC 7591 Dynamic Client Registration endpoint. Only mints public clients with allowed loopback, HTTPS, or native client redirect URIs. Body limit 8 KB.；Integrations & Tools, LangSmith REST API, Monitor, Reference, an, client, dynamic, oauth2, register | [原文](<https://docs.langchain.com/langsmith/smith-api/oauth/register-an-oauth2-dynamic-client>) |
| `Monitor/Reference/LangSmith REST API/Integrations & Tools/Replace vendor settings.md` | Replace vendor settings | Replaces vendor settings.；Integrations & Tools, LangSmith REST API, Monitor, Reference, replace, settings, vendor | [原文](<https://docs.langchain.com/langsmith/smith-api/mcp_vendors/replace-vendor-settings>) |
| `Monitor/Reference/LangSmith REST API/Integrations & Tools/Request OAuth2 device authorization.md` | Request OAuth2 device authorization | Issues a device code and user code for the device authorization flow per RFC 8628.；Integrations & Tools, LangSmith REST API, Monitor, Reference, authorization, device, oauth2, request | [原文](<https://docs.langchain.com/langsmith/smith-api/oauth/request-oauth2-device-authorization>) |
| `Monitor/Reference/LangSmith REST API/Integrations & Tools/Revoke an OAuth2 token.md` | Revoke an OAuth2 token | Revokes an access token or refresh token per RFC 7009. Always returns 200 regardless of whether the token was found.；Integrations & Tools, LangSmith REST API, Monitor, Reference, an, oauth2, revoke, token | [原文](<https://docs.langchain.com/langsmith/smith-api/oauth/revoke-an-oauth2-token>) |
| `Monitor/Reference/LangSmith REST API/Integrations & Tools/Revoke an authorized application.md` | Revoke an authorized application | Revokes the authenticated user's authorization for an application and invalidates that application's active tokens for the user.；Integrations & Tools, LangSmith REST API, Monitor, Reference, an, application, authorized, revoke | [原文](<https://docs.langchain.com/langsmith/smith-api/oauth/revoke-an-authorized-application>) |
| `Monitor/Reference/LangSmith REST API/Integrations & Tools/Rotate an oauth client secret.md` | Rotate an oauth client secret | Generates a new client secret for a confidential client, invalidating the previous one. The new secret is shown only once.；Integrations & Tools, LangSmith REST API, Monitor, Reference, an, client, oauth, rotate, secret | [原文](<https://docs.langchain.com/langsmith/smith-api/oauth/rotate-an-oauth-client-secret>) |
| `Monitor/Reference/LangSmith REST API/Integrations & Tools/Update a tool by ID.md` | Update a tool by ID | Updates an existing tool identified by its UUID.；Integrations & Tools, LangSmith REST API, Monitor, Reference, a, by, id, tool, update | [原文](<https://docs.langchain.com/langsmith/smith-api/tools/update-a-tool-by-id>) |
| `Monitor/Reference/LangSmith REST API/Integrations & Tools/Update a tool by handle.md` | Update a tool by handle | Updates an existing tool identified by its handle.；Integrations & Tools, LangSmith REST API, Monitor, Reference, a, by, handle, tool, update | [原文](<https://docs.langchain.com/langsmith/smith-api/tools/update-a-tool-by-handle>) |
| `Monitor/Reference/LangSmith REST API/Integrations & Tools/Update agent builder integrations settings.md` | Update agent builder integrations settings | Replaces default policy and integration overrides for the current workspace.；Integrations & Tools, LangSmith REST API, Monitor, Reference, agent, builder, integrations, settings, update | [原文](<https://docs.langchain.com/langsmith/smith-api/integrations/update-agent-builder-integrations-settings>) |
| `Monitor/Reference/LangSmith REST API/Integrations & Tools/Update an oauth client.md` | Update an oauth client | Integrations & Tools, LangSmith REST API, Monitor, Reference, an, client, oauth, update | [原文](<https://docs.langchain.com/langsmith/smith-api/oauth/update-an-oauth-client>) |
| `Monitor/Reference/LangSmith REST API/Issues/Create the issues agent for a session (Beta).md` | Create the issues agent for a session (Beta) | **Beta:** This endpoint is in active development and may change without notice.；Issues, LangSmith REST API, Monitor, Reference, a, agent, beta, create, for, issues, session, the | [原文](<https://docs.langchain.com/langsmith/smith-api/issues-agent/create-the-issues-agent-for-a-session-beta>) |
| `Monitor/Reference/LangSmith REST API/Issues/Delete the issues agent for a session (Beta).md` | Delete the issues agent for a session (Beta) | **Beta:** This endpoint is in active development and may change without notice.；Issues, LangSmith REST API, Monitor, Reference, a, agent, beta, delete, for, issues, session, the | [原文](<https://docs.langchain.com/langsmith/smith-api/issues-agent/delete-the-issues-agent-for-a-session-beta>) |
| `Monitor/Reference/LangSmith REST API/Issues/Get issue (Beta).md` | Get issue (Beta) | **Beta:** This endpoint is in active development and may change without notice.；Issues, LangSmith REST API, Monitor, Reference, beta, get, issue | [原文](<https://docs.langchain.com/langsmith/smith-api/issues/get-issue-beta>) |
| `Monitor/Reference/LangSmith REST API/Issues/Get the issues agent config for a session (Beta).md` | Get the issues agent config for a session (Beta) | **Beta:** This endpoint is in active development and may change without notice.；Issues, LangSmith REST API, Monitor, Reference, a, agent, beta, config, for, get, issues, session, the | [原文](<https://docs.langchain.com/langsmith/smith-api/issues-agent/get-the-issues-agent-config-for-a-session-beta>) |
| `Monitor/Reference/LangSmith REST API/Issues/List issues (Beta).md` | List issues (Beta) | **Beta:** This endpoint is in active development and may change without notice.；Issues, LangSmith REST API, Monitor, Reference, beta, issues, list | [原文](<https://docs.langchain.com/langsmith/smith-api/issues/list-issues-beta>) |
| `Monitor/Reference/LangSmith REST API/Issues/List issues agent configs (Beta).md` | List issues agent configs (Beta) | **Beta:** This endpoint is in active development and may change without notice.；Issues, LangSmith REST API, Monitor, Reference, agent, beta, configs, issues, list | [原文](<https://docs.langchain.com/langsmith/smith-api/issues-agent/list-issues-agent-configs-beta>) |
| `Monitor/Reference/LangSmith REST API/Issues/List viewed issues for a session (Beta).md` | List viewed issues for a session (Beta) | **Beta:** Returns the issues in this session that the current；Issues, LangSmith REST API, Monitor, Reference, a, beta, for, issues, list, session, viewed | [原文](<https://docs.langchain.com/langsmith/smith-api/issues/list-viewed-issues-for-a-session-beta>) |
| `Monitor/Reference/LangSmith REST API/Issues/Mark issue viewed (Beta).md` | Mark issue viewed (Beta) | **Beta:** Records that the current user opened this issue.；Issues, LangSmith REST API, Monitor, Reference, beta, issue, mark, viewed | [原文](<https://docs.langchain.com/langsmith/smith-api/issues/mark-issue-viewed-beta>) |
| `Monitor/Reference/LangSmith REST API/Issues/Roll an issues agent webhook signing secret.md` | Roll an issues agent webhook signing secret | Replaces the signing secret for the given generic URL issues agent webhook. Slack；Issues, LangSmith REST API, Monitor, Reference, agent, an, issues, roll, secret, signing, webhook | [原文](<https://docs.langchain.com/langsmith/smith-api/issues-agent/roll-an-issues-agent-webhook-signing-secret>) |
| `Monitor/Reference/LangSmith REST API/Issues/Save the agent overview for a session (Beta).md` | Save the agent overview for a session (Beta) | **Beta:** This endpoint is in active development and may change without notice.；Issues, LangSmith REST API, Monitor, Reference, a, agent, beta, for, overview, save, session, the | [原文](<https://docs.langchain.com/langsmith/smith-api/issues-agent/save-the-agent-overview-for-a-session-beta>) |
| `Monitor/Reference/LangSmith REST API/Issues/Update the issues agent config for a session (Beta).md` | Update the issues agent config for a session (Beta) | **Beta:** This endpoint is in active development and may change without notice.；Issues, LangSmith REST API, Monitor, Reference, a, agent, beta, config, for, issues, session, the, update | [原文](<https://docs.langchain.com/langsmith/smith-api/issues-agent/update-the-issues-agent-config-for-a-session-beta>) |
| `Monitor/Reference/LangSmith REST API/LLM Gateway/Create a gateway policy.md` | Create a gateway policy | Creates a gateway policy for the calling organization.；LLM Gateway, LangSmith REST API, Monitor, Reference, a, create, gateway, policy | [原文](<https://docs.langchain.com/langsmith/smith-api/gateway-policies/create-a-gateway-policy>) |
| `Monitor/Reference/LangSmith REST API/LLM Gateway/Delete a gateway policy.md` | Delete a gateway policy | Deletes a gateway policy. Subsequent reads return 404.；LLM Gateway, LangSmith REST API, Monitor, Reference, a, delete, gateway, policy | [原文](<https://docs.langchain.com/langsmith/smith-api/gateway-policies/delete-a-gateway-policy>) |
| `Monitor/Reference/LangSmith REST API/LLM Gateway/Get a gateway policy.md` | Get a gateway policy | Returns a single gateway policy by id. Cross-org access is；LLM Gateway, LangSmith REST API, Monitor, Reference, a, gateway, get, policy | [原文](<https://docs.langchain.com/langsmith/smith-api/gateway-policies/get-a-gateway-policy>) |
| `Monitor/Reference/LangSmith REST API/LLM Gateway/List gateway policies.md` | List gateway policies | Returns every gateway policy in the current organization.；LLM Gateway, LangSmith REST API, Monitor, Reference, gateway, list, policies | [原文](<https://docs.langchain.com/langsmith/smith-api/gateway-policies/list-gateway-policies>) |
| `Monitor/Reference/LangSmith REST API/LLM Gateway/Search gateway policies by subject value set.md` | Search gateway policies by subject value set | Batch variant of GET /v1/platform/gateway-policies for；LLM Gateway, LangSmith REST API, Monitor, Reference, by, gateway, policies, search, set, subject, value | [原文](<https://docs.langchain.com/langsmith/smith-api/gateway-policies/search-gateway-policies-by-subject-value-set>) |
| `Monitor/Reference/LangSmith REST API/LLM Gateway/Update a gateway policy.md` | Update a gateway policy | Partially updates a gateway policy. Only fields present in；LLM Gateway, LangSmith REST API, Monitor, Reference, a, gateway, policy, update | [原文](<https://docs.langchain.com/langsmith/smith-api/gateway-policies/update-a-gateway-policy>) |
| `Monitor/Reference/LangSmith REST API/LangSmith API reference.md` | LangSmith API reference | The LangSmith REST API provides programmatic access to tracing, datasets, experiments, annotations, and other LangSmith platform features.；LangSmith REST API, Monitor, Reference, api, ref, smith | [原文](<https://docs.langchain.com/langsmith/smith-api-ref>) |
| `Monitor/Reference/LangSmith REST API/Monitoring/Cancel bulk export.md` | Cancel bulk export | Cancel a bulk export by ID；LangSmith REST API, Monitor, Monitoring, Reference, bulk, cancel, export | [原文](<https://docs.langchain.com/langsmith/smith-api/bulk-exports/cancel-bulk-export>) |
| `Monitor/Reference/LangSmith REST API/Monitoring/Clone section.md` | Clone section | Clone a dashboard.；LangSmith REST API, Monitor, Monitoring, Reference, clone, section | [原文](<https://docs.langchain.com/langsmith/smith-api/charts/clone-section>) |
| `Monitor/Reference/LangSmith REST API/Monitoring/Create an alert rule.md` | Create an alert rule | Creates a new alert rule. The request body must be a JSON-encoded alert rule object that follows the CreateAlertRuleRequest schema.；LangSmith REST API, Monitor, Monitoring, Reference, alert, an, create, rule | [原文](<https://docs.langchain.com/langsmith/smith-api/alert_rules/create-an-alert-rule>) |
| `Monitor/Reference/LangSmith REST API/Monitoring/Create bulk export destination.md` | Create bulk export destination | Create a new bulk export destination；LangSmith REST API, Monitor, Monitoring, Reference, bulk, create, destination, export | [原文](<https://docs.langchain.com/langsmith/smith-api/bulk-exports/create-bulk-export-destination>) |
| `Monitor/Reference/LangSmith REST API/Monitoring/Create bulk export.md` | Create bulk export | Create a new bulk export；LangSmith REST API, Monitor, Monitoring, Reference, bulk, create, export | [原文](<https://docs.langchain.com/langsmith/smith-api/bulk-exports/create-bulk-export>) |
| `Monitor/Reference/LangSmith REST API/Monitoring/Create chart.md` | Create chart | Create a chart or dashboard text block.；LangSmith REST API, Monitor, Monitoring, Reference, chart, create | [原文](<https://docs.langchain.com/langsmith/smith-api/charts/create-chart>) |
| `Monitor/Reference/LangSmith REST API/Monitoring/Create section.md` | Create section | Create a new section.；LangSmith REST API, Monitor, Monitoring, Reference, create, section | [原文](<https://docs.langchain.com/langsmith/smith-api/charts/create-section>) |
| `Monitor/Reference/LangSmith REST API/Monitoring/Delete an alert rule.md` | Delete an alert rule | Deletes an alert rule；LangSmith REST API, Monitor, Monitoring, Reference, alert, an, delete, rule | [原文](<https://docs.langchain.com/langsmith/smith-api/alert_rules/delete-an-alert-rule>) |
| `Monitor/Reference/LangSmith REST API/Monitoring/Delete bulk export destination.md` | Delete bulk export destination | Delete a bulk export destination that is not used by any bulk export；LangSmith REST API, Monitor, Monitoring, Reference, bulk, delete, destination, export | [原文](<https://docs.langchain.com/langsmith/smith-api/bulk-exports/delete-bulk-export-destination>) |
| `Monitor/Reference/LangSmith REST API/Monitoring/Delete chart.md` | Delete chart | Delete a chart.；LangSmith REST API, Monitor, Monitoring, Reference, chart, delete | [原文](<https://docs.langchain.com/langsmith/smith-api/charts/delete-chart>) |
| `Monitor/Reference/LangSmith REST API/Monitoring/Delete section.md` | Delete section | Delete a section.；LangSmith REST API, Monitor, Monitoring, Reference, delete, section | [原文](<https://docs.langchain.com/langsmith/smith-api/charts/delete-section>) |
| `Monitor/Reference/LangSmith REST API/Monitoring/Get an alert rule.md` | Get an alert rule | Gets an alert rule.；LangSmith REST API, Monitor, Monitoring, Reference, alert, an, get, rule | [原文](<https://docs.langchain.com/langsmith/smith-api/alert_rules/get-an-alert-rule>) |
| `Monitor/Reference/LangSmith REST API/Monitoring/Get bulk export destination.md` | Get bulk export destination | Get a single bulk export destination by ID；LangSmith REST API, Monitor, Monitoring, Reference, bulk, destination, export, get | [原文](<https://docs.langchain.com/langsmith/smith-api/bulk-exports/get-bulk-export-destination>) |
| `Monitor/Reference/LangSmith REST API/Monitoring/Get bulk export destinations.md` | Get bulk export destinations | Get the current workspace's bulk export destinations；LangSmith REST API, Monitor, Monitoring, Reference, bulk, destinations, export, get | [原文](<https://docs.langchain.com/langsmith/smith-api/bulk-exports/get-bulk-export-destinations>) |
| `Monitor/Reference/LangSmith REST API/Monitoring/Get bulk export run.md` | Get bulk export run | Get a single bulk export's run by ID；LangSmith REST API, Monitor, Monitoring, Reference, bulk, export, get, run | [原文](<https://docs.langchain.com/langsmith/smith-api/bulk-exports/get-bulk-export-run>) |
| `Monitor/Reference/LangSmith REST API/Monitoring/Get bulk export runs filtered.md` | Get bulk export runs filtered | Get bulk export runs for exports that were created from a scheduled bulk export；LangSmith REST API, Monitor, Monitoring, Reference, bulk, export, filtered, get, runs | [原文](<https://docs.langchain.com/langsmith/smith-api/bulk-exports/get-bulk-export-runs-filtered>) |
| `Monitor/Reference/LangSmith REST API/Monitoring/Get bulk export runs.md` | Get bulk export runs | Get a bulk export's runs；LangSmith REST API, Monitor, Monitoring, Reference, bulk, export, get, runs | [原文](<https://docs.langchain.com/langsmith/smith-api/bulk-exports/get-bulk-export-runs>) |
| `Monitor/Reference/LangSmith REST API/Monitoring/Get bulk export.md` | Get bulk export | Get a single bulk export by ID；LangSmith REST API, Monitor, Monitoring, Reference, bulk, export, get | [原文](<https://docs.langchain.com/langsmith/smith-api/bulk-exports/get-bulk-export>) |
| `Monitor/Reference/LangSmith REST API/Monitoring/Get bulk exports.md` | Get bulk exports | Get the current workspace's bulk exports；LangSmith REST API, Monitor, Monitoring, Reference, bulk, exports, get | [原文](<https://docs.langchain.com/langsmith/smith-api/bulk-exports/get-bulk-exports>) |
| `Monitor/Reference/LangSmith REST API/Monitoring/Org create chart.md` | Org create chart | Deprecated: organization usage charts have been retired (HTTP 410).；LangSmith REST API, Monitor, Monitoring, Reference, chart, create, org | [原文](<https://docs.langchain.com/langsmith/smith-api/charts/org-create-chart>) |
| `Monitor/Reference/LangSmith REST API/Monitoring/Org create section.md` | Org create section | Deprecated: organization usage charts have been retired (HTTP 410).；LangSmith REST API, Monitor, Monitoring, Reference, create, org, section | [原文](<https://docs.langchain.com/langsmith/smith-api/charts/org-create-section>) |
| `Monitor/Reference/LangSmith REST API/Monitoring/Org delete chart.md` | Org delete chart | Deprecated: organization usage charts have been retired (HTTP 410).；LangSmith REST API, Monitor, Monitoring, Reference, chart, delete, org | [原文](<https://docs.langchain.com/langsmith/smith-api/charts/org-delete-chart>) |
| `Monitor/Reference/LangSmith REST API/Monitoring/Org delete section.md` | Org delete section | Deprecated: organization usage charts have been retired (HTTP 410).；LangSmith REST API, Monitor, Monitoring, Reference, delete, org, section | [原文](<https://docs.langchain.com/langsmith/smith-api/charts/org-delete-section>) |
| `Monitor/Reference/LangSmith REST API/Monitoring/Org read chart preview.md` | Org read chart preview | Deprecated: organization usage charts have been retired (HTTP 410).；LangSmith REST API, Monitor, Monitoring, Reference, chart, org, preview, read | [原文](<https://docs.langchain.com/langsmith/smith-api/charts/org-read-chart-preview>) |
| `Monitor/Reference/LangSmith REST API/Monitoring/Org read charts.md` | Org read charts | Deprecated: organization usage charts have been retired (HTTP 410).；LangSmith REST API, Monitor, Monitoring, Reference, charts, org, read | [原文](<https://docs.langchain.com/langsmith/smith-api/charts/org-read-charts>) |
| `Monitor/Reference/LangSmith REST API/Monitoring/Org read sections.md` | Org read sections | Deprecated: organization usage charts have been retired (HTTP 410).；LangSmith REST API, Monitor, Monitoring, Reference, org, read, sections | [原文](<https://docs.langchain.com/langsmith/smith-api/charts/org-read-sections>) |
| `Monitor/Reference/LangSmith REST API/Monitoring/Org read single chart.md` | Org read single chart | Deprecated: organization usage charts have been retired (HTTP 410).；LangSmith REST API, Monitor, Monitoring, Reference, chart, org, read, single | [原文](<https://docs.langchain.com/langsmith/smith-api/charts/org-read-single-chart>) |
| `Monitor/Reference/LangSmith REST API/Monitoring/Org read single section.md` | Org read single section | Deprecated: organization usage charts have been retired (HTTP 410).；LangSmith REST API, Monitor, Monitoring, Reference, org, read, section, single | [原文](<https://docs.langchain.com/langsmith/smith-api/charts/org-read-single-section>) |
| `Monitor/Reference/LangSmith REST API/Monitoring/Org update chart.md` | Org update chart | Deprecated: organization usage charts have been retired (HTTP 410).；LangSmith REST API, Monitor, Monitoring, Reference, chart, org, update | [原文](<https://docs.langchain.com/langsmith/smith-api/charts/org-update-chart>) |
| `Monitor/Reference/LangSmith REST API/Monitoring/Org update section.md` | Org update section | Deprecated: organization usage charts have been retired (HTTP 410).；LangSmith REST API, Monitor, Monitoring, Reference, org, section, update | [原文](<https://docs.langchain.com/langsmith/smith-api/charts/org-update-section>) |
| `Monitor/Reference/LangSmith REST API/Monitoring/Read chart preview.md` | Read chart preview | Get a preview for a chart without actually creating it.；LangSmith REST API, Monitor, Monitoring, Reference, chart, preview, read | [原文](<https://docs.langchain.com/langsmith/smith-api/charts/read-chart-preview>) |
| `Monitor/Reference/LangSmith REST API/Monitoring/Read charts.md` | Read charts | Get all charts for the tenant.；LangSmith REST API, Monitor, Monitoring, Reference, charts, read | [原文](<https://docs.langchain.com/langsmith/smith-api/charts/read-charts>) |
| `Monitor/Reference/LangSmith REST API/Monitoring/Read sections.md` | Read sections | Get all sections for the tenant.；LangSmith REST API, Monitor, Monitoring, Reference, read, sections | [原文](<https://docs.langchain.com/langsmith/smith-api/charts/read-sections>) |
| `Monitor/Reference/LangSmith REST API/Monitoring/Read single chart.md` | Read single chart | Get a single chart or text block by ID.；LangSmith REST API, Monitor, Monitoring, Reference, chart, read, single | [原文](<https://docs.langchain.com/langsmith/smith-api/charts/read-single-chart>) |
| `Monitor/Reference/LangSmith REST API/Monitoring/Read single section.md` | Read single section | Get a single section by ID.；LangSmith REST API, Monitor, Monitoring, Reference, read, section, single | [原文](<https://docs.langchain.com/langsmith/smith-api/charts/read-single-section>) |
| `Monitor/Reference/LangSmith REST API/Monitoring/Test an alert action to determine if configuration is valid.md` | Test an alert action to determine if configuration is valid | Tests an alert action which will fire a notification to all configured recipients if the configuration is valid.；LangSmith REST API, Monitor, Monitoring, Reference, action, alert, an, configuration, determine, if, is, test, to, valid | [原文](<https://docs.langchain.com/langsmith/smith-api/alert_rules/test-an-alert-action-to-determine-if-configuration-is-valid>) |
| `Monitor/Reference/LangSmith REST API/Monitoring/Update an alert rule.md` | Update an alert rule | Updates an alert rule.；LangSmith REST API, Monitor, Monitoring, Reference, alert, an, rule, update | [原文](<https://docs.langchain.com/langsmith/smith-api/alert_rules/update-an-alert-rule>) |
| `Monitor/Reference/LangSmith REST API/Monitoring/Update bulk export destination.md` | Update bulk export destination | Update a bulk export destination；LangSmith REST API, Monitor, Monitoring, Reference, bulk, destination, export, update | [原文](<https://docs.langchain.com/langsmith/smith-api/bulk-exports/update-bulk-export-destination>) |
| `Monitor/Reference/LangSmith REST API/Monitoring/Update chart.md` | Update chart | Update a chart or text block.；LangSmith REST API, Monitor, Monitoring, Reference, chart, update | [原文](<https://docs.langchain.com/langsmith/smith-api/charts/update-chart>) |
| `Monitor/Reference/LangSmith REST API/Monitoring/Update section.md` | Update section | Update a section.；LangSmith REST API, Monitor, Monitoring, Reference, section, update | [原文](<https://docs.langchain.com/langsmith/smith-api/charts/update-section>) |
| `Monitor/Reference/LangSmith REST API/Prompt Hub/Add repo owner.md` | Add repo owner | Add an owner to a repo.；LangSmith REST API, Monitor, Prompt Hub, Reference, add, owner, repo | [原文](<https://docs.langchain.com/langsmith/smith-api/ownerships/add-repo-owner>) |
| `Monitor/Reference/LangSmith REST API/Prompt Hub/Create comment.md` | Create comment | LangSmith REST API, Monitor, Prompt Hub, Reference, comment, create | [原文](<https://docs.langchain.com/langsmith/smith-api/comments/create-comment>) |
| `Monitor/Reference/LangSmith REST API/Prompt Hub/Create job.md` | Create job | Create a new prompt optimization job.；LangSmith REST API, Monitor, Prompt Hub, Reference, create, job | [原文](<https://docs.langchain.com/langsmith/smith-api/optimization-jobs/create-job>) |
| `Monitor/Reference/LangSmith REST API/Prompt Hub/Create log.md` | Create log | Create a new log entry for a prompt optimization job.；LangSmith REST API, Monitor, Prompt Hub, Reference, create, log | [原文](<https://docs.langchain.com/langsmith/smith-api/optimization-jobs/create-log>) |
| `Monitor/Reference/LangSmith REST API/Prompt Hub/Create repo.md` | Create repo | Create a repo.；LangSmith REST API, Monitor, Prompt Hub, Reference, create, repo | [原文](<https://docs.langchain.com/langsmith/smith-api/repos/create-repo>) |
| `Monitor/Reference/LangSmith REST API/Prompt Hub/Create sub comment.md` | Create sub comment | LangSmith REST API, Monitor, Prompt Hub, Reference, comment, create, sub | [原文](<https://docs.langchain.com/langsmith/smith-api/comments/create-sub-comment>) |
| `Monitor/Reference/LangSmith REST API/Prompt Hub/Create tag.md` | Create tag | Create a tag. Requires repo ownership, prompts:tag permission, or ABAC grant.；LangSmith REST API, Monitor, Prompt Hub, Reference, create, tag | [原文](<https://docs.langchain.com/langsmith/smith-api/tags/create-tag>) |
| `Monitor/Reference/LangSmith REST API/Prompt Hub/Delete job.md` | Delete job | Delete a prompt optimization job.；LangSmith REST API, Monitor, Prompt Hub, Reference, delete, job | [原文](<https://docs.langchain.com/langsmith/smith-api/optimization-jobs/delete-job>) |
| `Monitor/Reference/LangSmith REST API/Prompt Hub/Delete log.md` | Delete log | Delete a prompt optimization job log.；LangSmith REST API, Monitor, Prompt Hub, Reference, delete, log | [原文](<https://docs.langchain.com/langsmith/smith-api/optimization-jobs/delete-log>) |
| `Monitor/Reference/LangSmith REST API/Prompt Hub/Delete repo.md` | Delete repo | Delete a repo.；LangSmith REST API, Monitor, Prompt Hub, Reference, delete, repo | [原文](<https://docs.langchain.com/langsmith/smith-api/repos/delete-repo>) |
| `Monitor/Reference/LangSmith REST API/Prompt Hub/Delete repos.md` | Delete repos | Delete multiple repos with partial success support.；LangSmith REST API, Monitor, Prompt Hub, Reference, delete, repos | [原文](<https://docs.langchain.com/langsmith/smith-api/repos/delete-repos>) |
| `Monitor/Reference/LangSmith REST API/Prompt Hub/Delete tag.md` | Delete tag | Delete a tag. Requires repo ownership, prompts:tag permission, or ABAC grant.；LangSmith REST API, Monitor, Prompt Hub, Reference, delete, tag | [原文](<https://docs.langchain.com/langsmith/smith-api/tags/delete-tag>) |
| `Monitor/Reference/LangSmith REST API/Prompt Hub/Fork repo.md` | Fork repo | Fork a repo.；LangSmith REST API, Monitor, Prompt Hub, Reference, fork, repo | [原文](<https://docs.langchain.com/langsmith/smith-api/repos/fork-repo>) |
| `Monitor/Reference/LangSmith REST API/Prompt Hub/Get comments.md` | Get comments | LangSmith REST API, Monitor, Prompt Hub, Reference, comments, get | [原文](<https://docs.langchain.com/langsmith/smith-api/comments/get-comments>) |
| `Monitor/Reference/LangSmith REST API/Prompt Hub/Get job.md` | Get job | Get a specific optimization job.；LangSmith REST API, Monitor, Prompt Hub, Reference, get, job | [原文](<https://docs.langchain.com/langsmith/smith-api/optimization-jobs/get-job>) |
| `Monitor/Reference/LangSmith REST API/Prompt Hub/Get log.md` | Get log | Get a specific prompt optimization job log.；LangSmith REST API, Monitor, Prompt Hub, Reference, get, log | [原文](<https://docs.langchain.com/langsmith/smith-api/optimization-jobs/get-log>) |
| `Monitor/Reference/LangSmith REST API/Prompt Hub/Get repo.md` | Get repo | Get a repo.；LangSmith REST API, Monitor, Prompt Hub, Reference, get, repo | [原文](<https://docs.langchain.com/langsmith/smith-api/repos/get-repo>) |
| `Monitor/Reference/LangSmith REST API/Prompt Hub/Get settings.md` | Get settings | Get settings.；LangSmith REST API, Monitor, Prompt Hub, Reference, get, settings | [原文](<https://docs.langchain.com/langsmith/smith-api/settings/get-settings>) |
| `Monitor/Reference/LangSmith REST API/Prompt Hub/Get sub comments.md` | Get sub comments | LangSmith REST API, Monitor, Prompt Hub, Reference, comments, get, sub | [原文](<https://docs.langchain.com/langsmith/smith-api/comments/get-sub-comments>) |
| `Monitor/Reference/LangSmith REST API/Prompt Hub/Get tag.md` | Get tag | LangSmith REST API, Monitor, Prompt Hub, Reference, get, tag | [原文](<https://docs.langchain.com/langsmith/smith-api/tags/get-tag>) |
| `Monitor/Reference/LangSmith REST API/Prompt Hub/Get tags.md` | Get tags | LangSmith REST API, Monitor, Prompt Hub, Reference, get, tags | [原文](<https://docs.langchain.com/langsmith/smith-api/tags/get-tags>) |
| `Monitor/Reference/LangSmith REST API/Prompt Hub/Like comment.md` | Like comment | LangSmith REST API, Monitor, Prompt Hub, Reference, comment, like | [原文](<https://docs.langchain.com/langsmith/smith-api/comments/like-comment>) |
| `Monitor/Reference/LangSmith REST API/Prompt Hub/Like repo.md` | Like repo | Like a repo.；LangSmith REST API, Monitor, Prompt Hub, Reference, like, repo | [原文](<https://docs.langchain.com/langsmith/smith-api/likes/like-repo>) |
| `Monitor/Reference/LangSmith REST API/Prompt Hub/List job logs.md` | List job logs | List all logs for a specific prompt optimization job.；LangSmith REST API, Monitor, Prompt Hub, Reference, job, list, logs | [原文](<https://docs.langchain.com/langsmith/smith-api/optimization-jobs/list-job-logs>) |
| `Monitor/Reference/LangSmith REST API/Prompt Hub/List jobs.md` | List jobs | List all prompt optimization jobs.；LangSmith REST API, Monitor, Prompt Hub, Reference, jobs, list | [原文](<https://docs.langchain.com/langsmith/smith-api/optimization-jobs/list-jobs>) |
| `Monitor/Reference/LangSmith REST API/Prompt Hub/List repo owners.md` | List repo owners | List all owners of a repo.；LangSmith REST API, Monitor, Prompt Hub, Reference, list, owners, repo | [原文](<https://docs.langchain.com/langsmith/smith-api/ownerships/list-repo-owners>) |
| `Monitor/Reference/LangSmith REST API/Prompt Hub/List repo tags.md` | List repo tags | Get all repo tags.；LangSmith REST API, Monitor, Prompt Hub, Reference, list, repo, tags | [原文](<https://docs.langchain.com/langsmith/smith-api/repos/list-repo-tags>) |
| `Monitor/Reference/LangSmith REST API/Prompt Hub/List repos.md` | List repos | Get all repos.；LangSmith REST API, Monitor, Prompt Hub, Reference, list, repos | [原文](<https://docs.langchain.com/langsmith/smith-api/repos/list-repos>) |
| `Monitor/Reference/LangSmith REST API/Prompt Hub/Optimize prompt job.md` | Optimize prompt job | Optimize prompt；LangSmith REST API, Monitor, Prompt Hub, Reference, job, optimize, prompt | [原文](<https://docs.langchain.com/langsmith/smith-api/repos/optimize-prompt-job>) |
| `Monitor/Reference/LangSmith REST API/Prompt Hub/Remove repo owner.md` | Remove repo owner | Remove an owner from a repo.；LangSmith REST API, Monitor, Prompt Hub, Reference, owner, remove, repo | [原文](<https://docs.langchain.com/langsmith/smith-api/ownerships/remove-repo-owner>) |
| `Monitor/Reference/LangSmith REST API/Prompt Hub/Set tenant handle.md` | Set tenant handle | Set tenant handle.；LangSmith REST API, Monitor, Prompt Hub, Reference, handle, set, tenant | [原文](<https://docs.langchain.com/langsmith/smith-api/settings/set-tenant-handle>) |
| `Monitor/Reference/LangSmith REST API/Prompt Hub/Unlike comment.md` | Unlike comment | LangSmith REST API, Monitor, Prompt Hub, Reference, comment, unlike | [原文](<https://docs.langchain.com/langsmith/smith-api/comments/unlike-comment>) |
| `Monitor/Reference/LangSmith REST API/Prompt Hub/Update job.md` | Update job | Replace an existing prompt optimization job with a new, modified job.；LangSmith REST API, Monitor, Prompt Hub, Reference, job, update | [原文](<https://docs.langchain.com/langsmith/smith-api/optimization-jobs/update-job>) |
| `Monitor/Reference/LangSmith REST API/Prompt Hub/Update repo.md` | Update repo | Update a repo.；LangSmith REST API, Monitor, Prompt Hub, Reference, repo, update | [原文](<https://docs.langchain.com/langsmith/smith-api/repos/update-repo>) |
| `Monitor/Reference/LangSmith REST API/Prompt Hub/Update tag.md` | Update tag | Update a tag. Requires repo ownership, prompts:tag permission, or ABAC grant.；LangSmith REST API, Monitor, Prompt Hub, Reference, tag, update | [原文](<https://docs.langchain.com/langsmith/smith-api/tags/update-tag>) |
| `Monitor/Reference/LangSmith REST API/Prompts & Playground/Create a commit.md` | Create a commit | Creates a new commit in a repository.；LangSmith REST API, Monitor, Prompts & Playground, Reference, a, commit, create | [原文](<https://docs.langchain.com/langsmith/smith-api/commits/create-a-commit>) |
| `Monitor/Reference/LangSmith REST API/Prompts & Playground/Create directory commit.md` | Create directory commit | Creates a new directory commit for an agent or skill repository by applying file/link create, update, and delete operations. Linked directories default to the LATEST selector; use COMMIT to pin one commit. The legacy commit_id write field is deprecated and resolves as LATEST.；LangSmith REST API, Monitor, Prompts & Playground, Reference, commit, create, directory | [原文](<https://docs.langchain.com/langsmith/smith-api/directories/create-directory-commit>) |
| `Monitor/Reference/LangSmith REST API/Prompts & Playground/Create hub environments model.md` | Create hub environments model | Creates the hub environments configuration for the current tenant.；LangSmith REST API, Monitor, Prompts & Playground, Reference, create, environments, hub, model | [原文](<https://docs.langchain.com/langsmith/smith-api/hub_environments/create-hub-environments-model>) |
| `Monitor/Reference/LangSmith REST API/Prompts & Playground/Create playground settings.md` | Create playground settings | Create playground settings.；LangSmith REST API, Monitor, Prompts & Playground, Reference, create, playground, settings | [原文](<https://docs.langchain.com/langsmith/smith-api/playground-settings/create-playground-settings>) |
| `Monitor/Reference/LangSmith REST API/Prompts & Playground/Create prompt webhook.md` | Create prompt webhook | Create a new prompt webhook.；LangSmith REST API, Monitor, Prompts & Playground, Reference, create, prompt, webhook | [原文](<https://docs.langchain.com/langsmith/smith-api/prompt-webhooks/create-prompt-webhook>) |
| `Monitor/Reference/LangSmith REST API/Prompts & Playground/Delete directory repository.md` | Delete directory repository | Deletes an agent or skill repository and its owned child file repositories.；LangSmith REST API, Monitor, Prompts & Playground, Reference, delete, directory, repository | [原文](<https://docs.langchain.com/langsmith/smith-api/directories/delete-directory-repository>) |
| `Monitor/Reference/LangSmith REST API/Prompts & Playground/Delete hub environments model.md` | Delete hub environments model | Deletes the hub environments configuration. Tenant reverts to defaults.；LangSmith REST API, Monitor, Prompts & Playground, Reference, delete, environments, hub, model | [原文](<https://docs.langchain.com/langsmith/smith-api/hub_environments/delete-hub-environments-model>) |
| `Monitor/Reference/LangSmith REST API/Prompts & Playground/Delete playground settings.md` | Delete playground settings | Delete playground settings.；LangSmith REST API, Monitor, Prompts & Playground, Reference, delete, playground, settings | [原文](<https://docs.langchain.com/langsmith/smith-api/playground-settings/delete-playground-settings>) |
| `Monitor/Reference/LangSmith REST API/Prompts & Playground/Delete prompt webhook.md` | Delete prompt webhook | Delete a specific prompt webhook.；LangSmith REST API, Monitor, Prompts & Playground, Reference, delete, prompt, webhook | [原文](<https://docs.langchain.com/langsmith/smith-api/prompt-webhooks/delete-prompt-webhook>) |
| `Monitor/Reference/LangSmith REST API/Prompts & Playground/Get a commit.md` | Get a commit | Retrieves a specific commit by hash, tag, or "latest" for a repository.；LangSmith REST API, Monitor, Prompts & Playground, Reference, a, commit, get | [原文](<https://docs.langchain.com/langsmith/smith-api/commits/get-a-commit>) |
| `Monitor/Reference/LangSmith REST API/Prompts & Playground/Get directory contents.md` | Get directory contents | Resolves the flattened file tree for an agent or skill repository at a specific commit, tag, or latest.；LangSmith REST API, Monitor, Prompts & Playground, Reference, contents, directory, get | [原文](<https://docs.langchain.com/langsmith/smith-api/directories/get-directory-contents>) |
| `Monitor/Reference/LangSmith REST API/Prompts & Playground/Get playground settings.md` | Get playground settings | Get a single playground settings by ID.；LangSmith REST API, Monitor, Prompts & Playground, Reference, get, playground, settings | [原文](<https://docs.langchain.com/langsmith/smith-api/playground-settings/get-playground-settings>) |
| `Monitor/Reference/LangSmith REST API/Prompts & Playground/Get prompt webhook.md` | Get prompt webhook | Get a specific prompt webhook.；LangSmith REST API, Monitor, Prompts & Playground, Reference, get, prompt, webhook | [原文](<https://docs.langchain.com/langsmith/smith-api/prompt-webhooks/get-prompt-webhook>) |
| `Monitor/Reference/LangSmith REST API/Prompts & Playground/Get tag transition history.md` | Get tag transition history | Returns the paginated audit log of transitions for a specific；LangSmith REST API, Monitor, Prompts & Playground, Reference, get, history, tag, transition | [原文](<https://docs.langchain.com/langsmith/smith-api/tag-transitions/get-tag-transition-history>) |
| `Monitor/Reference/LangSmith REST API/Prompts & Playground/Invoke prompt.md` | Invoke prompt | LangSmith REST API, Monitor, Prompts & Playground, Reference, invoke, prompt | [原文](<https://docs.langchain.com/langsmith/smith-api/prompts/invoke-prompt>) |
| `Monitor/Reference/LangSmith REST API/Prompts & Playground/List commits.md` | List commits | List commits for a repository, newest first, with pagination support.；LangSmith REST API, Monitor, Prompts & Playground, Reference, commits, list | [原文](<https://docs.langchain.com/langsmith/smith-api/commits/list-commits>) |
| `Monitor/Reference/LangSmith REST API/Prompts & Playground/List hub environments.md` | List hub environments | Returns the hub environments model for the current tenant.；LangSmith REST API, Monitor, Prompts & Playground, Reference, environments, hub, list | [原文](<https://docs.langchain.com/langsmith/smith-api/hub_environments/list-hub-environments>) |
| `Monitor/Reference/LangSmith REST API/Prompts & Playground/List playground settings.md` | List playground settings | Get all playground settings for this tenant id.；LangSmith REST API, Monitor, Prompts & Playground, Reference, list, playground, settings | [原文](<https://docs.langchain.com/langsmith/smith-api/playground-settings/list-playground-settings>) |
| `Monitor/Reference/LangSmith REST API/Prompts & Playground/List prompt webhooks.md` | List prompt webhooks | List all prompt webhooks for the current tenant.；LangSmith REST API, Monitor, Prompts & Playground, Reference, list, prompt, webhooks | [原文](<https://docs.langchain.com/langsmith/smith-api/prompt-webhooks/list-prompt-webhooks>) |
| `Monitor/Reference/LangSmith REST API/Prompts & Playground/Test prompt webhook.md` | Test prompt webhook | Test a specific prompt webhook.；LangSmith REST API, Monitor, Prompts & Playground, Reference, prompt, test, webhook | [原文](<https://docs.langchain.com/langsmith/smith-api/prompt-webhooks/test-prompt-webhook>) |
| `Monitor/Reference/LangSmith REST API/Prompts & Playground/Update hub environments model.md` | Update hub environments model | Replaces the environments array on an existing model.；LangSmith REST API, Monitor, Prompts & Playground, Reference, environments, hub, model, update | [原文](<https://docs.langchain.com/langsmith/smith-api/hub_environments/update-hub-environments-model>) |
| `Monitor/Reference/LangSmith REST API/Prompts & Playground/Update playground settings.md` | Update playground settings | Update playground settings.；LangSmith REST API, Monitor, Prompts & Playground, Reference, playground, settings, update | [原文](<https://docs.langchain.com/langsmith/smith-api/playground-settings/update-playground-settings>) |
| `Monitor/Reference/LangSmith REST API/Prompts & Playground/Update prompt webhook.md` | Update prompt webhook | Update a specific prompt webhook.；LangSmith REST API, Monitor, Prompts & Playground, Reference, prompt, update, webhook | [原文](<https://docs.langchain.com/langsmith/smith-api/prompt-webhooks/update-prompt-webhook>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/Attach a sandbox to a browser (Beta).md` | Attach a sandbox to a browser (Beta) | Beta: give a sandbox its own window of the browser, or, with no sandbox, open a window for the person calling (or, with controller "agent", for a client to drive over api_cdp_url). The response's cdp_url is the Chrome DevTools endpoint the sandbox connects to, and api_cdp_url the same endpoint through the API; a client can open more tabs, which sta；LangSmith REST API, Monitor, Reference, Sandboxes, a, attach, beta, browser, sandbox, to | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/attach-a-sandbox-to-a-browser-beta>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/Batch delete sandboxes.md` | Batch delete sandboxes | Delete multiple sandboxes by name or UUID in a single request.；LangSmith REST API, Monitor, Reference, Sandboxes, batch, delete, sandboxes | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/batch-delete-sandboxes>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/Capture a snapshot from a sandbox.md` | Capture a snapshot from a sandbox | Create a snapshot by capturing the current state of a sandbox or promoting an existing checkpoint.；LangSmith REST API, Monitor, Reference, Sandboxes, a, capture, from, sandbox, snapshot | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/capture-a-snapshot-from-a-sandbox>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/Clone a volume (Beta).md` | Clone a volume (Beta) | **Beta:** This API is in active development and may change without notice. Requires sandbox volumes to be enabled for your workspace. Create a new volume holding a copy-on-write copy of an existing one. A volume attached read-write to a sandbox that is not stopped cannot be cloned. Only the volume's creator, or a role with sandboxes:exec, may clone；LangSmith REST API, Monitor, Reference, Sandboxes, a, beta, clone, volume | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/clone-a-volume-beta>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/Close a tab in a browser window (Beta).md` | Close a tab in a browser window (Beta) | Beta: close a tab in the window.；LangSmith REST API, Monitor, Reference, Sandboxes, a, beta, browser, close, in, tab, window | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/close-a-tab-in-a-browser-window-beta>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/Create a browser (Beta).md` | Create a browser (Beta) | Beta: create a browser sandbox, which runs one persistent Chrome that other sandboxes attach to. Logins made in it persist across restarts. It keeps its memory when it stops. A stopped browser is deleted after the sandbox default, along with its logins, unless delete_after_stop_seconds sets another delay or 0 to keep it.；LangSmith REST API, Monitor, Reference, Sandboxes, a, beta, browser, create | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/create-a-browser-beta>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/Create a registry.md` | Create a registry | Create a sandbox registry for pulling private images.；LangSmith REST API, Monitor, Reference, Sandboxes, a, create, registry | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/create-a-registry>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/Create a sandbox.md` | Create a sandbox | Create a new sandbox from a snapshot. Provide at most one of `snapshot_id` or `snapshot_name`; if neither is provided, the server uses the default snapshot. `snapshot_name` accepts a Docker-style `name` or `name:tag` reference (a bare name resolves to `name:latest`).；LangSmith REST API, Monitor, Reference, Sandboxes, a, create, sandbox | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/create-a-sandbox>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/Create a snapshot.md` | Create a snapshot | Create a snapshot from a Docker image (async build). Names use lowercase registry-style components separated by slashes, up to 255 characters. The system/ namespace is read-only.；LangSmith REST API, Monitor, Reference, Sandboxes, a, create, snapshot | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/create-a-snapshot>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/Create a volume (Beta).md` | Create a volume (Beta) | **Beta:** This API is in active development and may change without notice. Requires sandbox volumes to be enabled for your workspace. Create an empty volume that can be attached to sandboxes at a mount path. The size is rounded up to a whole GiB.；LangSmith REST API, Monitor, Reference, Sandboxes, a, beta, create, volume | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/create-a-volume-beta>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/Create links to a browser window (Beta).md` | Create links to a browser window (Beta) | Beta: mint a view link and an act link for one window, as every attachment response does, with a chosen lifetime and the origins allowed to embed the window's pages in an iframe. Without embed_origins no page may frame them. view_embed_url and act_embed_url carry the same tokens in the URL fragment, for an iframe, so no server sees them. An embedde；LangSmith REST API, Monitor, Reference, Sandboxes, a, beta, browser, create, links, to, window | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/create-links-to-a-browser-window-beta>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/Delete a registry.md` | Delete a registry | Delete a sandbox registry by name.；LangSmith REST API, Monitor, Reference, Sandboxes, a, delete, registry | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/delete-a-registry>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/Delete a sandbox.md` | Delete a sandbox | Delete a sandbox by name or UUID. Tears down the sandbox runtime and removes the DB record.；LangSmith REST API, Monitor, Reference, Sandboxes, a, delete, sandbox | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/delete-a-sandbox>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/Delete a snapshot.md` | Delete a snapshot | Delete a snapshot by ID or by a Docker-style name[:tag] reference. The underlying storage is reclaimed asynchronously.；LangSmith REST API, Monitor, Reference, Sandboxes, a, delete, snapshot | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/delete-a-snapshot>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/Delete a volume (Beta).md` | Delete a volume (Beta) | **Beta:** This API is in active development and may change without notice. Requires sandbox volumes to be enabled for your workspace. Delete a volume and its data. A volume attached to any sandbox cannot be deleted. Storage is reclaimed asynchronously. Only the volume's creator, or a role with sandboxes:exec, may delete it.；LangSmith REST API, Monitor, Reference, Sandboxes, a, beta, delete, volume | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/delete-a-volume-beta>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/Detach a sandbox from a browser (Beta).md` | Detach a sandbox from a browser (Beta) | Beta: close the window and stop the sandbox from making new connections to the browser.；LangSmith REST API, Monitor, Reference, Sandboxes, a, beta, browser, detach, from, sandbox | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/detach-a-sandbox-from-a-browser-beta>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/Download a sandbox file (download-a-sandbox-file-1).md` | Download a sandbox file | Download file contents from a sandbox filesystem path. Supports HTTP range requests: send a Range header (for example `bytes=0-1023`) to receive a 206 with only that byte range. Every response carries an ETag; send it back as If-Range to resume safely (a changed file returns 200 with the whole file instead of mismatched bytes) or as If-None-Match t；1, LangSmith REST API, Monitor, Reference, Sandboxes, a, download, file, sandbox | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/download-a-sandbox-file-1>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/Download a sandbox file.md` | Download a sandbox file | Download file contents from a sandbox filesystem path. Supports HTTP range requests: send a Range header (for example `bytes=0-1023`) to receive a 206 with only that byte range. Every response carries an ETag; send it back as If-Range to resume safely (a changed file returns 200 with the whole file instead of mismatched bytes) or as If-None-Match t；LangSmith REST API, Monitor, Reference, Sandboxes, a, download, file, sandbox | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/download-a-sandbox-file>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/Execute a sandbox command over WebSocket.md` | Execute a sandbox command over WebSocket | Open a WebSocket connection for streaming command execution inside a sandbox.；LangSmith REST API, Monitor, Reference, Sandboxes, a, command, execute, over, sandbox, websocket | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/execute-a-sandbox-command-over-websocket>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/Execute a sandbox command.md` | Execute a sandbox command | Execute a command inside a sandbox and return stdout, stderr, and exit code. Use the streaming execute endpoints for long-running commands that may exceed the synchronous request deadline.；LangSmith REST API, Monitor, Reference, Sandboxes, a, command, execute, sandbox | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/execute-a-sandbox-command>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/Generate a sandbox file download link.md` | Generate a sandbox file download link | Generate a tokenized link that downloads a single file from a sandbox with no further authentication. This mints a token rather than creating an addressable resource, so it returns 200 with no Location header. The token pins the sandbox, the file path, the response content type and disposition, and the sandbox flags, so a link cannot be repointed a；LangSmith REST API, Monitor, Reference, Sandboxes, a, download, file, generate, link, sandbox | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/generate-a-sandbox-file-download-link>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/Generate a service access token.md` | Generate a service access token | Create a short-lived JWT for accessing an HTTP service running on a specific port inside a sandbox. Returns a browser_url (sets auth cookie via redirect), an embed_url (for an iframe; carries the token in the URL fragment, so no server or Referer sees it), a service_url (for use with the X-Langsmith-Sandbox-Service-Token header), the raw token, and；LangSmith REST API, Monitor, Reference, Sandboxes, a, access, generate, service, token | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/generate-a-service-access-token>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/Get a browser (Beta).md` | Get a browser (Beta) | Beta: get a browser and the windows attached to it.；LangSmith REST API, Monitor, Reference, Sandboxes, a, beta, browser, get | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/get-a-browser-beta>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/Get a registry.md` | Get a registry | Get a sandbox registry by name.；LangSmith REST API, Monitor, Reference, Sandboxes, a, get, registry | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/get-a-registry>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/Get a sandbox.md` | Get a sandbox | Retrieve a sandbox by name. Stale provisioning sandboxes are auto-failed.；LangSmith REST API, Monitor, Reference, Sandboxes, a, get, sandbox | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/get-a-sandbox>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/Get a snapshot name.md` | Get a snapshot name | Get a snapshot name and every tag under it, with the snapshot each tag resolves to. To fetch one snapshot, use /api/v2/sandboxes/snapshots/{snapshot_id}.；LangSmith REST API, Monitor, Reference, Sandboxes, a, get, name, snapshot | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/get-a-snapshot-name>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/Get a snapshot.md` | Get a snapshot | Get a sandbox snapshot by ID or a registry-style reference, including system/default:latest. URL-encode references containing slashes. A bare name means name:latest, falling back to the newest ready untagged snapshot of that name. To list the tags under a name, use /api/v2/sandboxes/snapshots-by-name/{name}.；LangSmith REST API, Monitor, Reference, Sandboxes, a, get, snapshot | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/get-a-snapshot>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/Get a volume (Beta).md` | Get a volume (Beta) | **Beta:** This API is in active development and may change without notice. Requires sandbox volumes to be enabled for your workspace. Get a sandbox volume by ID or name, with its current attachments.；LangSmith REST API, Monitor, Reference, Sandboxes, a, beta, get, volume | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/get-a-volume-beta>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/Get sandbox resource usage.md` | Get sandbox resource usage | Get current sandbox resource usage and quota limits for the workspace；LangSmith REST API, Monitor, Reference, Sandboxes, get, resource, sandbox, usage | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/get-sandbox-resource-usage>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/Get sandbox status.md` | Get sandbox status | Retrieve the lightweight status of a sandbox for polling.；LangSmith REST API, Monitor, Reference, Sandboxes, get, sandbox, status | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/get-sandbox-status>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/Glob a sandbox filesystem.md` | Glob a sandbox filesystem | Find files under a root path matching a glob pattern (supports **). Entries are returned in lexical order by path.；LangSmith REST API, Monitor, Reference, Sandboxes, a, filesystem, glob, sandbox | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/glob-a-sandbox-filesystem>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/Grep a sandbox filesystem.md` | Grep a sandbox filesystem | Search files under a root path for a literal text pattern (not a regex).；LangSmith REST API, Monitor, Reference, Sandboxes, a, filesystem, grep, sandbox | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/grep-a-sandbox-filesystem>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/List a sandbox's shared service urls.md` | List a sandbox's shared service urls | Returns one entry per port the sandbox is currently reachable on, so a caller can see what is shared before turning it off. Expired token grants are omitted.；LangSmith REST API, Monitor, Reference, Sandboxes, a, list, sandboxs, service, shared, urls | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/list-a-sandboxs-shared-service-urls>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/List hourly sandbox usage costs.md` | List hourly sandbox usage costs | Returns priced usage per sandbox or snapshot and UTC hour in the half-open requested interval. LCU uses the recorded compute amount for sandboxes; snapshots have zero LCU. LSU allocates the recorded workspace storage amount proportionally to attributed bytes, including checkpoints on their sandbox and snapshots as separate resources. Resource filte；LangSmith REST API, Monitor, Reference, Sandboxes, costs, hourly, list, sandbox, usage | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/list-hourly-sandbox-usage-costs>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/List registries.md` | List registries | List sandbox registries for pulling private images.；LangSmith REST API, Monitor, Reference, Sandboxes, list, registries | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/list-registries>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/List sandboxes.md` | List sandboxes | List sandboxes for the authenticated tenant, with optional filtering, sorting, and pagination.；LangSmith REST API, Monitor, Reference, Sandboxes, list, sandboxes | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/list-sandboxes>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/List snapshots.md` | List snapshots | List workspace and published system snapshots, with optional filtering, sorting, and pagination.；LangSmith REST API, Monitor, Reference, Sandboxes, list, snapshots | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/list-snapshots>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/List volumes (Beta).md` | List volumes (Beta) | **Beta:** This API is in active development and may change without notice. Requires sandbox volumes to be enabled for your workspace. List the workspace's sandbox volumes with their current attachments.；LangSmith REST API, Monitor, Reference, Sandboxes, beta, list, volumes | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/list-volumes-beta>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/Load a browser's extensions (Beta).md` | Load a browser's extensions (Beta) | Beta: load the unpacked extensions placed in the browser's /var/lib/browserd/extensions (one per directory) that its Chrome does not have yet. Chrome loads them while running, so windows, tabs and connections are left as they are. Extensions already loaded stay loaded, even if removed from the directory, until Chrome next launches.；LangSmith REST API, Monitor, Reference, Sandboxes, a, beta, browsers, extensions, load | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/load-a-browsers-extensions-beta>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/Open a sandbox TCP tunnel.md` | Open a sandbox TCP tunnel | Open a WebSocket tunnel to a specific port inside a sandbox.；LangSmith REST API, Monitor, Reference, Sandboxes, a, open, sandbox, tcp, tunnel | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/open-a-sandbox-tcp-tunnel>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/Open a tab in a browser window (Beta).md` | Open a tab in a browser window (Beta) | Beta: open a tab in the window, at about:blank when no URL is given.；LangSmith REST API, Monitor, Reference, Sandboxes, a, beta, browser, in, open, tab, window | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/open-a-tab-in-a-browser-window-beta>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/Resize a browser window (Beta).md` | Resize a browser window (Beta) | Beta: size a window so its page is width by height CSS pixels. The window keeps that size until resized again, through this call or over CDP with Browser.setWindowBounds; the live view scales to fit it rather than resizing it. A browser that is not running cannot be resized.；LangSmith REST API, Monitor, Reference, Sandboxes, a, beta, browser, resize, window | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/resize-a-browser-window-beta>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/Resume a streamed sandbox command.md` | Resume a streamed sandbox command | Continue streaming a command started by the stream start endpoint. The offsets are also the ack for everything below them, which frees the sandbox's output buffer and unpauses a command waiting for room. Attaches only: a command the sandbox no longer has returns 404 rather than running again.；LangSmith REST API, Monitor, Reference, Sandboxes, a, command, resume, sandbox, streamed | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/resume-a-streamed-sandbox-command>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/Set who controls a browser window (Beta).md` | Set who controls a browser window (Beta) | Beta: give the window to a person ("user") or back to the attached sandbox ("agent"). It takes effect at once and does not wait for anyone. While a person has control, the attached sandbox's commands that read or act on the page fail with a "human has control" error, and it receives no page content. The window's current controller is in the browser；LangSmith REST API, Monitor, Reference, Sandboxes, a, beta, browser, controls, set, who, window | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/set-who-controls-a-browser-window-beta>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/Start a sandbox.md` | Start a sandbox | Start a stopped or failed sandbox. This endpoint is not idempotent. The optional volumes field is beta and requires sandbox volumes to be enabled for your workspace. Omit it to keep attachments, or send an empty array to detach all volumes. Changing attachments requires a stopped or failed sandbox, runtime access to it (its creator or sandboxes:exe；LangSmith REST API, Monitor, Reference, Sandboxes, a, sandbox, start | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/start-a-sandbox>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/Start a streamed sandbox command.md` | Start a streamed sandbox command | Execute a command inside a sandbox and stream stdout/stderr as Server-Sent Events with base64 payloads. Requires a sandbox on the v2 runtime. Passing a command_id reuses a running command instead of starting a second one. The response ends with an ack_required event when the sandbox's output buffer needs an ack; continue from the reported offsets w；LangSmith REST API, Monitor, Reference, Sandboxes, a, command, sandbox, start, streamed | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/start-a-streamed-sandbox-command>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/Stop a sandbox.md` | Stop a sandbox | Stop a ready sandbox. This endpoint is not idempotent; the filesystem is preserved for later restart.；LangSmith REST API, Monitor, Reference, Sandboxes, a, sandbox, stop | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/stop-a-sandbox>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/Stop sharing a sandbox service URL.md` | Stop sharing a sandbox service URL | Removes the sharing grant for one port, or for every port when port is omitted. A LangSmith login URL stops working immediately. A previously minted service token is not revoked and stays valid until it expires, but no new one can be issued from the removed grant.；LangSmith REST API, Monitor, Reference, Sandboxes, a, sandbox, service, sharing, stop, url | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/stop-sharing-a-sandbox-service-url>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/Update a registry.md` | Update a registry | Update a sandbox registry's name and/or credentials.；LangSmith REST API, Monitor, Reference, Sandboxes, a, registry, update | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/update-a-registry>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/Update a sandbox.md` | Update a sandbox | Update a sandbox's display name, retention, resources, tags, or proxy configuration. The name must be unique within the tenant. Proxy configuration sent to a sandbox that is not running is stored and applied when it next starts.；LangSmith REST API, Monitor, Reference, Sandboxes, a, sandbox, update | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/update-a-sandbox>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/Update a volume (Beta).md` | Update a volume (Beta) | **Beta:** This API is in active development and may change without notice. Requires sandbox volumes to be enabled for your workspace. Update a volume's description or labels. Each field sent replaces the stored value; omitted fields are unchanged. Null, an empty description, or an empty labels object clears it. Only the volume's creator, or a role；LangSmith REST API, Monitor, Reference, Sandboxes, a, beta, update, volume | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/update-a-volume-beta>) |
| `Monitor/Reference/LangSmith REST API/Sandboxes/Upload a sandbox file.md` | Upload a sandbox file | Upload a file to a sandbox filesystem path.；LangSmith REST API, Monitor, Reference, Sandboxes, a, file, sandbox, upload | [原文](<https://docs.langchain.com/langsmith/smith-api/sandboxes/upload-a-sandbox-file>) |
| `Monitor/Reference/LangSmith REST API/System/Count shared examples.md` | Count shared examples | Count all examples by query params；LangSmith REST API, Monitor, Reference, System, count, examples, shared | [原文](<https://docs.langchain.com/langsmith/smith-api/public/count-shared-examples>) |
| `Monitor/Reference/LangSmith REST API/System/Create a model price.md` | Create a model price | Create a custom model price for this workspace.；LangSmith REST API, Monitor, Reference, System, a, create, model, price | [原文](<https://docs.langchain.com/langsmith/smith-api/model-price-map/create-a-model-price>) |
| `Monitor/Reference/LangSmith REST API/System/Delete a model price.md` | Delete a model price | Delete a custom model price from this workspace.；LangSmith REST API, Monitor, Reference, System, a, delete, model, price | [原文](<https://docs.langchain.com/langsmith/smith-api/model-price-map/delete-a-model-price>) |
| `Monitor/Reference/LangSmith REST API/System/Delete default model for a feature.md` | Delete default model for a feature | Removes the default model for a feature in the workspace.；LangSmith REST API, Monitor, Reference, System, a, default, delete, feature, for, model | [原文](<https://docs.langchain.com/langsmith/smith-api/features/delete-default-model-for-a-feature>) |
| `Monitor/Reference/LangSmith REST API/System/Disable a model for a feature.md` | Disable a model for a feature | Adds a model to the disabled list for a feature in the workspace.；LangSmith REST API, Monitor, Reference, System, a, disable, feature, for, model | [原文](<https://docs.langchain.com/langsmith/smith-api/features/disable-a-model-for-a-feature>) |
| `Monitor/Reference/LangSmith REST API/System/Execute.md` | Execute | Execute some custom code for testing purposes.；LangSmith REST API, Monitor, Reference, System, execute | [原文](<https://docs.langchain.com/langsmith/smith-api/ace/execute>) |
| `Monitor/Reference/LangSmith REST API/System/Generate query for shared dataset runs.md` | Generate query for shared dataset runs | Get runs in projects run over a dataset that has been shared.；LangSmith REST API, Monitor, Reference, System, dataset, for, generate, query, runs, shared | [原文](<https://docs.langchain.com/langsmith/smith-api/public/generate-query-for-shared-dataset-runs>) |
| `Monitor/Reference/LangSmith REST API/System/Get health info.md` | Get health info | Get health information about the current deployment of LangSmith.；LangSmith REST API, Monitor, Reference, System, get, health, info | [原文](<https://docs.langchain.com/langsmith/smith-api/info/get-health-info>) |
| `Monitor/Reference/LangSmith REST API/System/Get message JSON schema.md` | Get message JSON schema | LangSmith REST API, Monitor, Reference, System, get, json, message, schema | [原文](<https://docs.langchain.com/langsmith/smith-api/public/get-message-json-schema>) |
| `Monitor/Reference/LangSmith REST API/System/Get server info.md` | Get server info | Returns information about the current LangSmith deployment: version,；LangSmith REST API, Monitor, Reference, System, get, info, server | [原文](<https://docs.langchain.com/langsmith/smith-api/info/get-server-info>) |
| `Monitor/Reference/LangSmith REST API/System/Get shared run by ID.md` | Get shared run by ID | Get the shared run.；LangSmith REST API, Monitor, Reference, System, by, get, id, run, shared | [原文](<https://docs.langchain.com/langsmith/smith-api/public/get-shared-run-by-id>) |
| `Monitor/Reference/LangSmith REST API/System/Get shared run.md` | Get shared run | Get the shared run.；LangSmith REST API, Monitor, Reference, System, get, run, shared | [原文](<https://docs.langchain.com/langsmith/smith-api/public/get-shared-run>) |
| `Monitor/Reference/LangSmith REST API/System/Get tool def JSON schema.md` | Get tool def JSON schema | LangSmith REST API, Monitor, Reference, System, def, get, json, schema, tool | [原文](<https://docs.langchain.com/langsmith/smith-api/public/get-tool-def-json-schema>) |
| `Monitor/Reference/LangSmith REST API/System/List feature configurations.md` | List feature configurations | Returns a consolidated view of default models and disabled models per feature for the workspace.；LangSmith REST API, Monitor, Reference, System, configurations, feature, list | [原文](<https://docs.langchain.com/langsmith/smith-api/features/list-feature-configurations>) |
| `Monitor/Reference/LangSmith REST API/System/List model prices.md` | List model prices | List the model prices LangSmith uses to compute run costs in this workspace.；LangSmith REST API, Monitor, Reference, System, list, model, prices | [原文](<https://docs.langchain.com/langsmith/smith-api/model-price-map/list-model-prices>) |
| `Monitor/Reference/LangSmith REST API/System/Query shared dataset runs.md` | Query shared dataset runs | Get runs in projects run over a dataset that has been shared.；LangSmith REST API, Monitor, Reference, System, dataset, query, runs, shared | [原文](<https://docs.langchain.com/langsmith/smith-api/public/query-shared-dataset-runs>) |
| `Monitor/Reference/LangSmith REST API/System/Query shared runs.md` | Query shared runs | Get run by ids or the shared run if not specifed.；LangSmith REST API, Monitor, Reference, System, query, runs, shared | [原文](<https://docs.langchain.com/langsmith/smith-api/public/query-shared-runs>) |
| `Monitor/Reference/LangSmith REST API/System/Re-enable a disabled model for a feature.md` | Re-enable a disabled model for a feature | Removes a model from the disabled list for a feature in the workspace.；LangSmith REST API, Monitor, Reference, System, a, disabled, enable, feature, for, model, re | [原文](<https://docs.langchain.com/langsmith/smith-api/features/re-enable-a-disabled-model-for-a-feature>) |
| `Monitor/Reference/LangSmith REST API/System/Read shared comparative experiments.md` | Read shared comparative experiments | Get all comparative experiments for a given dataset.；LangSmith REST API, Monitor, Reference, System, comparative, experiments, read, shared | [原文](<https://docs.langchain.com/langsmith/smith-api/public/read-shared-comparative-experiments>) |
| `Monitor/Reference/LangSmith REST API/System/Read shared dataset feedback.md` | Read shared dataset feedback | Get feedback for runs in projects run over a dataset that has been shared.；LangSmith REST API, Monitor, Reference, System, dataset, feedback, read, shared | [原文](<https://docs.langchain.com/langsmith/smith-api/public/read-shared-dataset-feedback>) |
| `Monitor/Reference/LangSmith REST API/System/Read shared dataset run.md` | Read shared dataset run | Get runs in projects run over a dataset that has been shared.；LangSmith REST API, Monitor, Reference, System, dataset, read, run, shared | [原文](<https://docs.langchain.com/langsmith/smith-api/public/read-shared-dataset-run>) |
| `Monitor/Reference/LangSmith REST API/System/Read shared dataset tracer sessions bulk.md` | Read shared dataset tracer sessions bulk | Get sessions from multiple datasets using share tokens.；LangSmith REST API, Monitor, Reference, System, bulk, dataset, read, sessions, shared, tracer | [原文](<https://docs.langchain.com/langsmith/smith-api/public/read-shared-dataset-tracer-sessions-bulk>) |
| `Monitor/Reference/LangSmith REST API/System/Read shared dataset tracer sessions.md` | Read shared dataset tracer sessions | Get projects run on a dataset that has been shared.；LangSmith REST API, Monitor, Reference, System, dataset, read, sessions, shared, tracer | [原文](<https://docs.langchain.com/langsmith/smith-api/public/read-shared-dataset-tracer-sessions>) |
| `Monitor/Reference/LangSmith REST API/System/Read shared dataset.md` | Read shared dataset | Get dataset by ids or the shared dataset if not specifed.；LangSmith REST API, Monitor, Reference, System, dataset, read, shared | [原文](<https://docs.langchain.com/langsmith/smith-api/public/read-shared-dataset>) |
| `Monitor/Reference/LangSmith REST API/System/Read shared examples.md` | Read shared examples | Get example by ids or the shared example if not specifed.；LangSmith REST API, Monitor, Reference, System, examples, read, shared | [原文](<https://docs.langchain.com/langsmith/smith-api/public/read-shared-examples>) |
| `Monitor/Reference/LangSmith REST API/System/Read shared feedbacks.md` | Read shared feedbacks | LangSmith REST API, Monitor, Reference, System, feedbacks, read, shared | [原文](<https://docs.langchain.com/langsmith/smith-api/public/read-shared-feedbacks>) |
| `Monitor/Reference/LangSmith REST API/System/Replace a model price.md` | Replace a model price | Replace every field of a custom model price in this workspace.；LangSmith REST API, Monitor, Reference, System, a, model, price, replace | [原文](<https://docs.langchain.com/langsmith/smith-api/model-price-map/replace-a-model-price>) |
| `Monitor/Reference/LangSmith REST API/System/Restart a backfill job.md` | Restart a backfill job | Deletes the backfill job record, causing the backfill to restart from the beginning on the next cron tick. Requires instance admin access.；LangSmith REST API, Monitor, Reference, System, a, backfill, job, restart | [原文](<https://docs.langchain.com/langsmith/smith-api/backfills/restart-a-backfill-job>) |
| `Monitor/Reference/LangSmith REST API/System/Set default model for a feature.md` | Set default model for a feature | Sets or replaces the default model for a feature in the workspace.；LangSmith REST API, Monitor, Reference, System, a, default, feature, for, model, set | [原文](<https://docs.langchain.com/langsmith/smith-api/features/set-default-model-for-a-feature>) |
| `Monitor/Reference/LangSmith REST API/System/Stats shared dataset runs.md` | Stats shared dataset runs | Get run stats in projects run over a dataset that has been shared.；LangSmith REST API, Monitor, Reference, System, dataset, runs, shared, stats | [原文](<https://docs.langchain.com/langsmith/smith-api/public/stats-shared-dataset-runs>) |
| `Monitor/Reference/LangSmith REST API/Threads/Get a public shared thread's manifest.md` | Get a public shared thread's manifest | Returns the thread and project a share token is scoped to, plus the project's conversations config.；LangSmith REST API, Monitor, Reference, Threads, a, get, manifest, public, shared, threads | [原文](<https://docs.langchain.com/langsmith/smith-api/threads/get-a-public-shared-threads-manifest>) |
| `Monitor/Reference/LangSmith REST API/Threads/Get one run in a public shared thread.md` | Get one run in a public shared thread | Returns a single run, including full inputs and outputs, provided its trace root belongs to the shared thread.；LangSmith REST API, Monitor, Reference, Threads, a, get, in, one, public, run, shared, thread | [原文](<https://docs.langchain.com/langsmith/smith-api/threads/get-one-run-in-a-public-shared-thread>) |
| `Monitor/Reference/LangSmith REST API/Threads/Get stats for a public shared thread.md` | Get stats for a public shared thread | Returns aggregate stats for the thread identified by the share token.；LangSmith REST API, Monitor, Reference, Threads, a, for, get, public, shared, stats, thread | [原文](<https://docs.langchain.com/langsmith/smith-api/threads/get-stats-for-a-public-shared-thread>) |
| `Monitor/Reference/LangSmith REST API/Threads/List runs of one trace in a public shared thread.md` | List runs of one trace in a public shared thread | Returns every run in the given trace, provided that trace's root belongs to the shared thread.；LangSmith REST API, Monitor, Reference, Threads, a, in, list, of, one, public, runs, shared, thread, trace | [原文](<https://docs.langchain.com/langsmith/smith-api/threads/list-runs-of-one-trace-in-a-public-shared-thread>) |
| `Monitor/Reference/LangSmith REST API/Threads/List traces in a public shared thread.md` | List traces in a public shared thread | Returns a page of root traces belonging to the thread identified by the share token. The share token supplies the tenant, project, and thread scope.；LangSmith REST API, Monitor, Reference, Threads, a, in, list, public, shared, thread, traces | [原文](<https://docs.langchain.com/langsmith/smith-api/threads/list-traces-in-a-public-shared-thread>) |
| `Monitor/Reference/LangSmith REST API/Threads/Query single thread stats.md` | Query single thread stats | Compute aggregate stats for a single thread (turn count, latency percentiles, token/cost sums, and detail breakdowns) within a project.；LangSmith REST API, Monitor, Reference, Threads, query, single, stats, thread | [原文](<https://docs.langchain.com/langsmith/smith-api/threads/query-single-thread-stats>) |
| `Monitor/Reference/LangSmith REST API/Threads/Query thread stats.md` | Query thread stats | GET with body payload — no resources created. Returns aggregate statistics for threads in a tracing project.；LangSmith REST API, Monitor, Reference, Threads, query, stats, thread | [原文](<https://docs.langchain.com/langsmith/smith-api/threads/query-thread-stats>) |
| `Monitor/Reference/LangSmith REST API/Threads/Query thread traces.md` | Query thread traces | Retrieve all traces belonging to a specific thread within a project.；LangSmith REST API, Monitor, Reference, Threads, query, thread, traces | [原文](<https://docs.langchain.com/langsmith/smith-api/threads/query-thread-traces>) |
| `Monitor/Reference/LangSmith REST API/Threads/Query threads.md` | Query threads | GET with body payload — no resources created. Returns the threads in a tracing project matching the query passed as the request payload.；LangSmith REST API, Monitor, Reference, Threads, query, threads | [原文](<https://docs.langchain.com/langsmith/smith-api/threads/query-threads>) |
| `Monitor/Reference/LangSmith REST API/Threads/Read a thread's share state.md` | Read a thread's share state | Returns the share token for a thread. The token is omitted when；LangSmith REST API, Monitor, Reference, Threads, a, read, share, state, threads | [原文](<https://docs.langchain.com/langsmith/smith-api/threads/read-a-threads-share-state>) |
| `Monitor/Reference/LangSmith REST API/Threads/Share a thread.md` | Share a thread | Mints a public share token for a thread. Idempotent: sharing an；LangSmith REST API, Monitor, Reference, Threads, a, share, thread | [原文](<https://docs.langchain.com/langsmith/smith-api/threads/share-a-thread>) |
| `Monitor/Reference/LangSmith REST API/Threads/Stream messages for a public shared thread.md` | Stream messages for a public shared thread | Streams the thread's conversation as server-sent events. SSE only.；LangSmith REST API, Monitor, Reference, Threads, a, for, messages, public, shared, stream, thread | [原文](<https://docs.langchain.com/langsmith/smith-api/threads/stream-messages-for-a-public-shared-thread>) |
| `Monitor/Reference/LangSmith REST API/Threads/Unshare a thread.md` | Unshare a thread | Deletes the share token for a thread. Idempotent: returns 204；LangSmith REST API, Monitor, Reference, Threads, a, thread, unshare | [原文](<https://docs.langchain.com/langsmith/smith-api/threads/unshare-a-thread>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Auto-generate insights job config (Beta).md` | Auto-generate insights job config (Beta) | Generate an Insights job configuration for a project.；LangSmith REST API, Monitor, Reference, Tracing, auto, beta, config, generate, insights, job | [原文](<https://docs.langchain.com/langsmith/smith-api/tracer-sessions/auto-generate-insights-job-config-beta>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Create a run.md` | Create a run | Queues a single run for ingestion. The request body must be a JSON-encoded run object that follows the Run schema.；LangSmith REST API, Monitor, Reference, Tracing, a, create, run | [原文](<https://docs.langchain.com/langsmith/smith-api/runs/create-a-run>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Create decision model rule.md` | Create decision model rule | Create a decision-model evaluator (Jev, SemIf or OpenAI Decisions) from；LangSmith REST API, Monitor, Reference, Tracing, create, decision, model, rule | [原文](<https://docs.langchain.com/langsmith/smith-api/run/create-decision-model-rule>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Create filter view.md` | Create filter view | Create a new filter view.；LangSmith REST API, Monitor, Reference, Tracing, create, filter, view | [原文](<https://docs.langchain.com/langsmith/smith-api/tracer-sessions/create-filter-view>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Create insights job (Beta).md` | Create insights job (Beta) | Create an Insights job for a project.；LangSmith REST API, Monitor, Reference, Tracing, beta, create, insights, job | [原文](<https://docs.langchain.com/langsmith/smith-api/tracer-sessions/create-insights-job-beta>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Create insights job config (Beta).md` | Create insights job config (Beta) | Create an Insights job configuration for a project.；LangSmith REST API, Monitor, Reference, Tracing, beta, config, create, insights, job | [原文](<https://docs.langchain.com/langsmith/smith-api/tracer-sessions/create-insights-job-config-beta>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Create rule.md` | Create rule | Create a new run rule.；LangSmith REST API, Monitor, Reference, Tracing, create, rule | [原文](<https://docs.langchain.com/langsmith/smith-api/run/create-rule>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Create tracer session.md` | Create tracer session | Create a new project.；LangSmith REST API, Monitor, Reference, Tracing, create, session, tracer | [原文](<https://docs.langchain.com/langsmith/smith-api/tracer-sessions/create-tracer-session>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Delete filter view.md` | Delete filter view | Delete a specific filter view.；LangSmith REST API, Monitor, Reference, Tracing, delete, filter, view | [原文](<https://docs.langchain.com/langsmith/smith-api/tracer-sessions/delete-filter-view>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Delete insights job (Beta).md` | Delete insights job (Beta) | Delete an Insights job for a project.；LangSmith REST API, Monitor, Reference, Tracing, beta, delete, insights, job | [原文](<https://docs.langchain.com/langsmith/smith-api/tracer-sessions/delete-insights-job-beta>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Delete insights job config (Beta).md` | Delete insights job config (Beta) | Delete an Insights job configuration for a project.；LangSmith REST API, Monitor, Reference, Tracing, beta, config, delete, insights, job | [原文](<https://docs.langchain.com/langsmith/smith-api/tracer-sessions/delete-insights-job-config-beta>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Delete rule.md` | Delete rule | Delete a run rule.；LangSmith REST API, Monitor, Reference, Tracing, delete, rule | [原文](<https://docs.langchain.com/langsmith/smith-api/run/delete-rule>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Delete runs abac.md` | Delete runs abac | Delete specific runs by trace IDs.；LangSmith REST API, Monitor, Reference, Tracing, abac, delete, runs | [原文](<https://docs.langchain.com/langsmith/smith-api/run/delete-runs-abac>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Delete runs.md` | Delete runs | DELETE with body payload — removes the runs identified by the request payload.；LangSmith REST API, Monitor, Reference, Tracing, delete, runs | [原文](<https://docs.langchain.com/langsmith/smith-api/run/delete-runs>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Delete tracer session.md` | Delete tracer session | Delete a specific project.；LangSmith REST API, Monitor, Reference, Tracing, delete, session, tracer | [原文](<https://docs.langchain.com/langsmith/smith-api/tracer-sessions/delete-tracer-session>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Delete tracer sessions.md` | Delete tracer sessions | Delete projects.；LangSmith REST API, Monitor, Reference, Tracing, delete, sessions, tracer | [原文](<https://docs.langchain.com/langsmith/smith-api/tracer-sessions/delete-tracer-sessions>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Generate query for runs.md` | Generate query for runs | Get runs filter expression query for a given natural language query.；LangSmith REST API, Monitor, Reference, Tracing, for, generate, query, runs | [原文](<https://docs.langchain.com/langsmith/smith-api/run/generate-query-for-runs>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Get a public shared trace run.md` | Get a public shared trace run | Returns one run within the trace identified by the share token. The request supplies only the run ID and that run's exact start_time coordinate.；LangSmith REST API, Monitor, Reference, Tracing, a, get, public, run, shared, trace | [原文](<https://docs.langchain.com/langsmith/smith-api/runs/get-a-public-shared-trace-run>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Get a single run.md` | Get a single run | Returns one run by ID for the given session. Use the `selects` query parameter (repeatable) to select fields to return.；LangSmith REST API, Monitor, Reference, Tracing, a, get, run, single | [原文](<https://docs.langchain.com/langsmith/smith-api/runs/get-a-single-run>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Get insights job (Beta).md` | Get insights job (Beta) | Get an Insights job for a project.；LangSmith REST API, Monitor, Reference, Tracing, beta, get, insights, job | [原文](<https://docs.langchain.com/langsmith/smith-api/tracer-sessions/get-insights-job-beta>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Get insights job configs (Beta).md` | Get insights job configs (Beta) | List Insights job configurations for a project.；LangSmith REST API, Monitor, Reference, Tracing, beta, configs, get, insights, job | [原文](<https://docs.langchain.com/langsmith/smith-api/tracer-sessions/get-insights-job-configs-beta>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Get insights jobs (Beta).md` | Get insights jobs (Beta) | List Insights jobs for a project.；LangSmith REST API, Monitor, Reference, Tracing, beta, get, insights, jobs | [原文](<https://docs.langchain.com/langsmith/smith-api/tracer-sessions/get-insights-jobs-beta>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Get last applied rule.md` | Get last applied rule | Get the last applied rule.；LangSmith REST API, Monitor, Reference, Tracing, applied, get, last, rule | [原文](<https://docs.langchain.com/langsmith/smith-api/run/get-last-applied-rule>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Get run cluster from insights job (Beta).md` | Get run cluster from insights job (Beta) | Get a cluster from the report produced by an Insights job.；LangSmith REST API, Monitor, Reference, Tracing, beta, cluster, from, get, insights, job, run | [原文](<https://docs.langchain.com/langsmith/smith-api/tracer-sessions/get-run-cluster-from-insights-job-beta>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Get runs from insights job (Beta).md` | Get runs from insights job (Beta) | List runs analyzed by an Insights job, optionally filtered by report cluster.；LangSmith REST API, Monitor, Reference, Tracing, beta, from, get, insights, job, runs | [原文](<https://docs.langchain.com/langsmith/smith-api/tracer-sessions/get-runs-from-insights-job-beta>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Get the LangSmith UI URL for a run.md` | Get the LangSmith UI URL for a run | Returns the URL to view a specific run in the LangSmith UI. The caller must supply the；LangSmith REST API, Monitor, Reference, Tracing, a, for, get, langsmith, run, the, ui, url | [原文](<https://docs.langchain.com/langsmith/smith-api/runs/get-the-langsmith-ui-url-for-a-run>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Get tracing project prebuilt dashboard.md` | Get tracing project prebuilt dashboard | Get a prebuilt dashboard for a tracing project.；LangSmith REST API, Monitor, Reference, Tracing, dashboard, get, prebuilt, project, tracing | [原文](<https://docs.langchain.com/langsmith/smith-api/tracer-sessions/get-tracing-project-prebuilt-dashboard>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Group runs.md` | Group runs | Deprecated; sunset January 31, 2027. Use POST /api/v2/threads/query to query threads instead.；LangSmith REST API, Monitor, Reference, Tracing, group, runs | [原文](<https://docs.langchain.com/langsmith/smith-api/run/group-runs>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Ingest runs (batch json).md` | Ingest runs (batch json) | Ingests a batch of runs in a single JSON payload. The payload must have `post` and/or `patch` arrays containing run objects.；LangSmith REST API, Monitor, Reference, Tracing, batch, ingest, json, runs | [原文](<https://docs.langchain.com/langsmith/smith-api/runs/ingest-runs-batch-json>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Ingest runs (multipart).md` | Ingest runs (multipart) | Ingests multiple runs, feedback objects, and binary attachments in a single `multipart/form-data` request.；LangSmith REST API, Monitor, Reference, Tracing, ingest, multipart, runs | [原文](<https://docs.langchain.com/langsmith/smith-api/runs/ingest-runs-multipart>) |
| `Monitor/Reference/LangSmith REST API/Tracing/List agent versions for a project.md` | List agent versions for a project | Returns all agent versions (commit SHAs) seen in the given tracing project, ordered by first_seen_at descending.；LangSmith REST API, Monitor, Reference, Tracing, a, agent, for, list, project, versions | [原文](<https://docs.langchain.com/langsmith/smith-api/sessions/list-agent-versions-for-a-project>) |
| `Monitor/Reference/LangSmith REST API/Tracing/List rule logs (v2).md` | List rule logs (v2) | List logs for a particular rule with cursor-based pagination.；LangSmith REST API, Monitor, Reference, Tracing, list, logs, rule, v2 | [原文](<https://docs.langchain.com/langsmith/smith-api/run/list-rule-logs-v2>) |
| `Monitor/Reference/LangSmith REST API/Tracing/List rule logs.md` | List rule logs | List logs for a particular rule；LangSmith REST API, Monitor, Reference, Tracing, list, logs, rule | [原文](<https://docs.langchain.com/langsmith/smith-api/run/list-rule-logs>) |
| `Monitor/Reference/LangSmith REST API/Tracing/List rules.md` | List rules | List all run rules.；LangSmith REST API, Monitor, Reference, Tracing, list, rules | [原文](<https://docs.langchain.com/langsmith/smith-api/run/list-rules>) |
| `Monitor/Reference/LangSmith REST API/Tracing/List runs in a trace.md` | List runs in a trace | Returns runs for a trace ID within min/max start time. Optional `filter`; repeatable `selects` to select fields to return.；LangSmith REST API, Monitor, Reference, Tracing, a, in, list, runs, trace | [原文](<https://docs.langchain.com/langsmith/smith-api/runs/list-runs-in-a-trace>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Query public shared trace runs.md` | Query public shared trace runs | Returns all runs within the trace identified by the share token. The share token supplies the tenant, project, and trace scope.；LangSmith REST API, Monitor, Reference, Tracing, public, query, runs, shared, trace | [原文](<https://docs.langchain.com/langsmith/smith-api/runs/query-public-shared-trace-runs>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Query runs (query-runs).md` | Query runs | Returns a paginated list of runs for the given projects within min/max start_time. Supports filters, cursor pagination, and `selects` to select fields to return.；LangSmith REST API, Monitor, Reference, Tracing, query, runs | [原文](<https://docs.langchain.com/langsmith/smith-api/runs/query-runs>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Query runs.md` | Query runs | LangSmith REST API, Monitor, Reference, Tracing, query, runs | [原文](<https://docs.langchain.com/langsmith/smith-api/run/query-runs>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Query traces.md` | Query traces | Returns a paginated list of traces (root runs) for a single tracing project. Each item carries the trace's root run plus optional trace-wide aggregates (`total_tokens`, `total_cost`, `first_token_time`) under `trace_aggregates`, so clients never have to merge by `trace_id`.；LangSmith REST API, Monitor, Reference, Tracing, query, traces | [原文](<https://docs.langchain.com/langsmith/smith-api/runs/query-traces>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Read filter view.md` | Read filter view | Get a specific filter view.；LangSmith REST API, Monitor, Reference, Tracing, filter, read, view | [原文](<https://docs.langchain.com/langsmith/smith-api/tracer-sessions/read-filter-view>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Read filter views.md` | Read filter views | Get all filter views for a session.；LangSmith REST API, Monitor, Reference, Tracing, filter, read, views | [原文](<https://docs.langchain.com/langsmith/smith-api/tracer-sessions/read-filter-views>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Read run share state.md` | Read run share state | Get the state of sharing of a run.；LangSmith REST API, Monitor, Reference, Tracing, read, run, share, state | [原文](<https://docs.langchain.com/langsmith/smith-api/run/read-run-share-state>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Read run.md` | Read run | Get a specific run.；LangSmith REST API, Monitor, Reference, Tracing, read, run | [原文](<https://docs.langchain.com/langsmith/smith-api/run/read-run>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Read tracer session.md` | Read tracer session | Get a specific project.；LangSmith REST API, Monitor, Reference, Tracing, read, session, tracer | [原文](<https://docs.langchain.com/langsmith/smith-api/tracer-sessions/read-tracer-session>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Read tracer sessions runs metadata.md` | Read tracer sessions runs metadata | Given a session, a number K, and (optionally) a list of metadata keys, return the top K values for each key.；LangSmith REST API, Monitor, Reference, Tracing, metadata, read, runs, sessions, tracer | [原文](<https://docs.langchain.com/langsmith/smith-api/tracer-sessions/read-tracer-sessions-runs-metadata>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Read tracer sessions.md` | Read tracer sessions | List all projects.；LangSmith REST API, Monitor, Reference, Tracing, read, sessions, tracer | [原文](<https://docs.langchain.com/langsmith/smith-api/tracer-sessions/read-tracer-sessions>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Rename filter view.md` | Rename filter view | Rename a filter view (display_name and description only).；LangSmith REST API, Monitor, Reference, Tracing, filter, rename, view | [原文](<https://docs.langchain.com/langsmith/smith-api/tracer-sessions/rename-filter-view>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Resolve an address to its tracing project.md` | Resolve an address to its tracing project | Returns the tracing project (session) an address names. An address is an AGENT (`id` and `environment`), an EXPERIMENT (`id`), or an EVALUATOR (no `id`: evaluator traces share one project per workspace). Send `kind` and `environment` in upper case, as listed; they are matched case-insensitively, while the Agent `id` is case-sensitive. An address th；LangSmith REST API, Monitor, Reference, Tracing, address, an, its, project, resolve, to, tracing | [原文](<https://docs.langchain.com/langsmith/smith-api/sessions/resolve-an-address-to-its-tracing-project>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Share a run.md` | Share a run | Creates or returns a share token for a run. Child runs share their trace root.；LangSmith REST API, Monitor, Reference, Tracing, a, run, share | [原文](<https://docs.langchain.com/langsmith/smith-api/runs/share-a-run>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Share run.md` | Share run | Share a run.；LangSmith REST API, Monitor, Reference, Tracing, run, share | [原文](<https://docs.langchain.com/langsmith/smith-api/run/share-run>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Stats group runs.md` | Stats group runs | Get stats for the grouped runs.；LangSmith REST API, Monitor, Reference, Tracing, group, runs, stats | [原文](<https://docs.langchain.com/langsmith/smith-api/run/stats-group-runs>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Stats runs.md` | Stats runs | Get all runs by query in body payload.；LangSmith REST API, Monitor, Reference, Tracing, runs, stats | [原文](<https://docs.langchain.com/langsmith/smith-api/run/stats-runs>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Thread preview.md` | Thread preview | Get preview of a thread.；LangSmith REST API, Monitor, Reference, Tracing, preview, thread | [原文](<https://docs.langchain.com/langsmith/smith-api/run/thread-preview>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Trigger rule.md` | Trigger rule | Trigger a run rule manually.；LangSmith REST API, Monitor, Reference, Tracing, rule, trigger | [原文](<https://docs.langchain.com/langsmith/smith-api/run/trigger-rule>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Trigger rules.md` | Trigger rules | Trigger an array of run rules manually.；LangSmith REST API, Monitor, Reference, Tracing, rules, trigger | [原文](<https://docs.langchain.com/langsmith/smith-api/run/trigger-rules>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Unshare a run.md` | Unshare a run | Deletes the share token for the trace identified by trace_id and session_id. Idempotent: returns 204 whether or not a share token existed.；LangSmith REST API, Monitor, Reference, Tracing, a, run, unshare | [原文](<https://docs.langchain.com/langsmith/smith-api/runs/unshare-a-run>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Unshare run.md` | Unshare run | Unshare a run.；LangSmith REST API, Monitor, Reference, Tracing, run, unshare | [原文](<https://docs.langchain.com/langsmith/smith-api/run/unshare-run>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Update a run.md` | Update a run | Updates a run identified by its ID. The body should contain only the fields to be changed; unknown fields are ignored.；LangSmith REST API, Monitor, Reference, Tracing, a, run, update | [原文](<https://docs.langchain.com/langsmith/smith-api/runs/update-a-run>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Update filter view.md` | Update filter view | Update a filter view.；LangSmith REST API, Monitor, Reference, Tracing, filter, update, view | [原文](<https://docs.langchain.com/langsmith/smith-api/tracer-sessions/update-filter-view>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Update insights job (Beta).md` | Update insights job (Beta) | Update an Insights job for a project.；LangSmith REST API, Monitor, Reference, Tracing, beta, insights, job, update | [原文](<https://docs.langchain.com/langsmith/smith-api/tracer-sessions/update-insights-job-beta>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Update insights job config (Beta).md` | Update insights job config (Beta) | Update an Insights job configuration for a project.；LangSmith REST API, Monitor, Reference, Tracing, beta, config, insights, job, update | [原文](<https://docs.langchain.com/langsmith/smith-api/tracer-sessions/update-insights-job-config-beta>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Update rule.md` | Update rule | Update a run rule.；LangSmith REST API, Monitor, Reference, Tracing, rule, update | [原文](<https://docs.langchain.com/langsmith/smith-api/run/update-rule>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Update tracer session.md` | Update tracer session | Update a project.；LangSmith REST API, Monitor, Reference, Tracing, session, tracer, update | [原文](<https://docs.langchain.com/langsmith/smith-api/tracer-sessions/update-tracer-session>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Validate rule.md` | Validate rule | Validate a rule by executing it with test data without creating a saved rule.；LangSmith REST API, Monitor, Reference, Tracing, rule, validate | [原文](<https://docs.langchain.com/langsmith/smith-api/run/validate-rule>) |
| `Monitor/Reference/LangSmith REST API/Tracing/Validate runs query.md` | Validate runs query | Validate runs query syntax, returns errors for broken queries.；LangSmith REST API, Monitor, Reference, Tracing, query, runs, validate | [原文](<https://docs.langchain.com/langsmith/smith-api/run/validate-runs-query>) |
| `Monitor/Reference/LangSmith REST API/teams/Add members to a team.md` | Add members to a team | Adds organization members to a team and returns a status for each identity:；LangSmith REST API, Monitor, Reference, a, add, members, team, teams, to | [原文](<https://docs.langchain.com/langsmith/smith-api/teams/add-members-to-a-team>) |
| `Monitor/Reference/LangSmith REST API/teams/Attach an access policy to a team.md` | Attach an access policy to a team | Attaches an existing access policy in the organization to a team. A workspace；LangSmith REST API, Monitor, Reference, a, access, an, attach, policy, team, teams, to | [原文](<https://docs.langchain.com/langsmith/smith-api/teams/attach-an-access-policy-to-a-team>) |
| `Monitor/Reference/LangSmith REST API/teams/Change a team's role in a workspace.md` | Change a team's role in a workspace | Changes an organization-wide team's role in a workspace it has access to. Team；LangSmith REST API, Monitor, Reference, a, change, in, role, teams, workspace | [原文](<https://docs.langchain.com/langsmith/smith-api/teams/change-a-teams-role-in-a-workspace>) |
| `Monitor/Reference/LangSmith REST API/teams/Create a team.md` | Create a team | Creates an organization-wide team. Needs organization:teams:manage. Workspace scoped；LangSmith REST API, Monitor, Reference, a, create, team, teams | [原文](<https://docs.langchain.com/langsmith/smith-api/teams/create-a-team>) |
| `Monitor/Reference/LangSmith REST API/teams/Delete a team.md` | Delete a team | Deletes an organization-wide team with its members, workspace grants and access；LangSmith REST API, Monitor, Reference, a, delete, team, teams | [原文](<https://docs.langchain.com/langsmith/smith-api/teams/delete-a-team>) |
| `Monitor/Reference/LangSmith REST API/teams/Detach an access policy from a team.md` | Detach an access policy from a team | Detaches an access policy from a team. A workspace scoped team's policy is detached；LangSmith REST API, Monitor, Reference, a, access, an, detach, from, policy, team, teams | [原文](<https://docs.langchain.com/langsmith/smith-api/teams/detach-an-access-policy-from-a-team>) |
| `Monitor/Reference/LangSmith REST API/teams/Get a team's role in a workspace.md` | Get a team's role in a workspace | Gets an organization-wide team's grant in one workspace. A workspace scoped team；LangSmith REST API, Monitor, Reference, a, get, in, role, teams, workspace | [原文](<https://docs.langchain.com/langsmith/smith-api/teams/get-a-teams-role-in-a-workspace>) |
| `Monitor/Reference/LangSmith REST API/teams/Get a team.md` | Get a team | Gets one team in the organization.；LangSmith REST API, Monitor, Reference, a, get, team, teams | [原文](<https://docs.langchain.com/langsmith/smith-api/teams/get-a-team>) |
| `Monitor/Reference/LangSmith REST API/teams/Grant a team a role in a workspace.md` | Grant a team a role in a workspace | Gives an organization-wide team a role in a workspace. Team members who are；LangSmith REST API, Monitor, Reference, a, grant, in, role, team, teams, workspace | [原文](<https://docs.langchain.com/langsmith/smith-api/teams/grant-a-team-a-role-in-a-workspace>) |
| `Monitor/Reference/LangSmith REST API/teams/List a team's access policies.md` | List a team's access policies | Lists the access policies attached to a team. A page carries next_cursor, which is；LangSmith REST API, Monitor, Reference, a, access, list, policies, teams | [原文](<https://docs.langchain.com/langsmith/smith-api/teams/list-a-teams-access-policies>) |
| `Monitor/Reference/LangSmith REST API/teams/List a team's workspace grants.md` | List a team's workspace grants | Lists the workspaces an organization-wide team has access to and its role in each.；LangSmith REST API, Monitor, Reference, a, grants, list, teams, workspace | [原文](<https://docs.langchain.com/langsmith/smith-api/teams/list-a-teams-workspace-grants>) |
| `Monitor/Reference/LangSmith REST API/teams/List organization teams.md` | List organization teams | Lists the organization's teams in name order. A page carries next_cursor, which is；LangSmith REST API, Monitor, Reference, list, organization, teams | [原文](<https://docs.langchain.com/langsmith/smith-api/teams/list-organization-teams>) |
| `Monitor/Reference/LangSmith REST API/teams/List team members.md` | List team members | Lists the members of a team. A page carries next_cursor, which is the value to send；LangSmith REST API, Monitor, Reference, list, members, team, teams | [原文](<https://docs.langchain.com/langsmith/smith-api/teams/list-team-members>) |
| `Monitor/Reference/LangSmith REST API/teams/List workspace scoped team members.md` | List workspace scoped team members | Lists the workspace identities of a workspace scoped team's members. A page carries；LangSmith REST API, Monitor, Reference, list, members, scoped, team, teams, workspace | [原文](<https://docs.langchain.com/langsmith/smith-api/teams/list-workspace-scoped-team-members>) |
| `Monitor/Reference/LangSmith REST API/teams/Remove a member from a team.md` | Remove a member from a team | Removes an organization member from a team, along with the workspace identities；LangSmith REST API, Monitor, Reference, a, from, member, remove, team, teams | [原文](<https://docs.langchain.com/langsmith/smith-api/teams/remove-a-member-from-a-team>) |
| `Monitor/Reference/LangSmith REST API/teams/Remove a team's access to a workspace.md` | Remove a team's access to a workspace | Removes an organization-wide team's grant in a workspace. This also detaches the；LangSmith REST API, Monitor, Reference, a, access, remove, teams, to, workspace | [原文](<https://docs.langchain.com/langsmith/smith-api/teams/remove-a-teams-access-to-a-workspace>) |
| `Monitor/Reference/LangSmith REST API/teams/Update a team.md` | Update a team | Renames an organization-wide team or changes its description or IdP group mapping.；LangSmith REST API, Monitor, Reference, a, team, teams, update | [原文](<https://docs.langchain.com/langsmith/smith-api/teams/update-a-team>) |
| `Monitor/Reference/LangSmith reference.md` | LangSmith reference | [card] [Python SDK](langsmith%20%28smith-python-sdk%29.md)；Monitor, Reference, reference | [原文](<https://docs.langchain.com/langsmith/reference>) |
| `Monitor/Reference/SmithDB API migration/Migrate dataset experiment runs to SmithDB.md` | Migrate dataset experiment runs to SmithDB | Migrate the LangSmith SDK dataset experiment run methods to their SmithDB-backed equivalents.；Monitor, Reference, SmithDB API migration, experiments, migration, sdk, smithdb | [原文](<https://docs.langchain.com/langsmith/smithdb-sdk-migration-experiments>) |
| `Monitor/Reference/SmithDB API migration/Migrate feedback and sharing methods to SmithDB.md` | Migrate feedback and sharing methods to SmithDB | Migrate the LangSmith SDK feedback, annotation queue, and public run methods to their SmithDB-backed equivalents.；Monitor, Reference, SmithDB API migration, feedback, migration, sdk, smithdb | [原文](<https://docs.langchain.com/langsmith/smithdb-sdk-migration-feedback>) |
| `Monitor/Reference/SmithDB API migration/Migrate run queries to SmithDB.md` | Migrate run queries to SmithDB | Migrate the LangSmith SDK run query methods to their SmithDB-backed equivalents.；Monitor, Reference, SmithDB API migration, migration, query, runs, sdk, smithdb | [原文](<https://docs.langchain.com/langsmith/smithdb-sdk-migration-query-runs>) |
| `Monitor/Reference/SmithDB API migration/Migrate run retrieval to SmithDB.md` | Migrate run retrieval to SmithDB | Migrate the LangSmith SDK methods that retrieve a single run or build a run URL.；Monitor, Reference, SmithDB API migration, migration, runs, sdk, smithdb | [原文](<https://docs.langchain.com/langsmith/smithdb-sdk-migration-runs>) |
| `Monitor/Reference/SmithDB API migration/Migrate thread methods to SmithDB.md` | Migrate thread methods to SmithDB | Migrate the LangSmith SDK thread methods to their SmithDB-backed equivalents.；Monitor, Reference, SmithDB API migration, migration, sdk, smithdb, threads | [原文](<https://docs.langchain.com/langsmith/smithdb-sdk-migration-threads>) |
| `Monitor/Reference/SmithDB API migration/Migrate to SmithDB-backed APIs.md` | Migrate to SmithDB-backed APIs | Migrate your existing LangSmith SDK methods to their SmithDB-backed equivalents for faster agent observability.；Monitor, Reference, SmithDB API migration, migration, sdk, smithdb | [原文](<https://docs.langchain.com/langsmith/smithdb-sdk-migration>) |
| `Monitor/Reference/SmithDB API migration/Migrate trace methods to SmithDB.md` | Migrate trace methods to SmithDB | Migrate the LangSmith SDK trace methods to their SmithDB-backed equivalents.；Monitor, Reference, SmithDB API migration, migration, sdk, smithdb, traces | [原文](<https://docs.langchain.com/langsmith/smithdb-sdk-migration-traces>) |
| `Monitor/Reference/langsmith (smith-java-sdk).md` | langsmith | JavaScript/TypeScript package；Monitor, Reference, java, sdk, smith | [原文](<https://docs.langchain.com/langsmith/smith-java-sdk>) |
| `Monitor/Reference/langsmith (smith-js-ts-sdk).md` | langsmith | JavaScript/TypeScript package；Monitor, Reference, js, sdk, smith, ts | [原文](<https://docs.langchain.com/langsmith/smith-js-ts-sdk>) |
| `Monitor/Reference/langsmith (smith-python-sdk).md` | langsmith | Python package；Monitor, Reference, python, sdk, smith | [原文](<https://docs.langchain.com/langsmith/smith-python-sdk>) |
| `Monitor/Reference/langsmith.md` | langsmith | JavaScript/TypeScript package；Monitor, Reference, go, sdk, smith | [原文](<https://docs.langchain.com/langsmith/smith-go-sdk>) |
| `Monitor/Trace/Configuration & troubleshooting/Advanced tracing techniques/Access the current run (span) within a traced function.md` | Access the current run (span) within a traced function | Advanced tracing techniques, Configuration & troubleshooting, Monitor, Trace, access, current, span | [原文](<https://docs.langchain.com/langsmith/access-current-span>) |
| `Monitor/Trace/Configuration & troubleshooting/Advanced tracing techniques/Implement distributed tracing.md` | Implement distributed tracing | [!WARNING]；Advanced tracing techniques, Configuration & troubleshooting, Monitor, Trace, distributed, tracing | [原文](<https://docs.langchain.com/langsmith/distributed-tracing>) |
| `Monitor/Trace/Configuration & troubleshooting/Advanced tracing techniques/Log multimodal traces.md` | Log multimodal traces | Advanced tracing techniques, Configuration & troubleshooting, Monitor, Trace, log, multimodal, traces | [原文](<https://docs.langchain.com/langsmith/log-multimodal-traces>) |
| `Monitor/Trace/Configuration & troubleshooting/Advanced tracing techniques/Trace JS functions in serverless environments.md` | Trace JS functions in serverless environments | [!NOTE]；Advanced tracing techniques, Configuration & troubleshooting, Monitor, Trace, environments, serverless | [原文](<https://docs.langchain.com/langsmith/serverless-environments>) |
| `Monitor/Trace/Configuration & troubleshooting/Advanced tracing techniques/Trace generator functions.md` | Trace generator functions | [!NOTE]；Advanced tracing techniques, Configuration & troubleshooting, Monitor, Trace, functions, generator, trace | [原文](<https://docs.langchain.com/langsmith/trace-generator-functions>) |
| `Monitor/Trace/Configuration & troubleshooting/Agent & environment settings/Conditional tracing.md` | Conditional tracing | [!TIP]；Agent & environment settings, Configuration & troubleshooting, Monitor, Trace, conditional, tracing | [原文](<https://docs.langchain.com/langsmith/conditional-tracing>) |
| `Monitor/Trace/Configuration & troubleshooting/Agent & environment settings/Log traces to an agent.md` | Log traces to an agent | Configure an agent identifier and environment to send traces from your code to LangSmith.；Agent & environment settings, Configuration & troubleshooting, Monitor, Trace, agent, log, to, traces | [原文](<https://docs.langchain.com/langsmith/log-traces-to-agent>) |
| `Monitor/Trace/Configuration & troubleshooting/Agent & environment settings/Set a sampling rate for traces.md` | Set a sampling rate for traces | [!TIP]；Agent & environment settings, Configuration & troubleshooting, Monitor, Trace, sample, traces | [原文](<https://docs.langchain.com/langsmith/sample-traces>) |
| `Monitor/Trace/Configuration & troubleshooting/Agent & environment settings/Trace without setting environment variables.md` | Trace without setting environment variables | [!WARNING]；Agent & environment settings, Configuration & troubleshooting, Monitor, Trace, env, trace, vars, without | [原文](<https://docs.langchain.com/langsmith/trace-without-env-vars>) |
| `Monitor/Trace/Configuration & troubleshooting/Agent & environment settings/Write traces to multiple destinations with replicas.md` | Write traces to multiple destinations with replicas | Send every trace to multiple agent environments or workspaces at the same time using replicas, configured by environment variable or at runtime.；Agent & environment settings, Configuration & troubleshooting, Monitor, Trace, replicas, trace | [原文](<https://docs.langchain.com/langsmith/trace-replicas>) |
| `Monitor/Trace/Configuration & troubleshooting/Cost tracking.md` | Cost tracking | [!NOTE]；Configuration & troubleshooting, Monitor, Trace, cost, tracking | [原文](<https://docs.langchain.com/langsmith/cost-tracking>) |
| `Monitor/Trace/Configuration & troubleshooting/Data & privacy/Add metadata and tags to traces.md` | Add metadata and tags to traces | [!TIP]；Configuration & troubleshooting, Data & privacy, Monitor, Trace, add, metadata, tags | [原文](<https://docs.langchain.com/langsmith/add-metadata-tags>) |
| `Monitor/Trace/Configuration & troubleshooting/Data & privacy/Prevent logging of sensitive data in traces.md` | Prevent logging of sensitive data in traces | [!NOTE]；Configuration & troubleshooting, Data & privacy, Monitor, Trace, inputs, mask, outputs | [原文](<https://docs.langchain.com/langsmith/mask-inputs-outputs>) |
| `Monitor/Trace/Configuration & troubleshooting/Data & privacy/Redact secrets from traces.md` | Redact secrets from traces | Prevent API keys, tokens, and other secrets from appearing in LangSmith traces using marked secrets and the SDK anonymizer.；Configuration & troubleshooting, Data & privacy, Monitor, Trace, redact, secrets | [原文](<https://docs.langchain.com/langsmith/redact-secrets>) |
| `Monitor/Trace/Configuration & troubleshooting/Data & privacy/Redact sensitive data with the OpenTelemetry Gateway architecture.md` | Redact sensitive data with the OpenTelemetry Gateway architecture | Use an OpenTelemetry collector to redact sensitive data from traces before they land in LangSmith.；Configuration & troubleshooting, Data & privacy, Monitor, Trace, gateway, otel, redaction, trace | [原文](<https://docs.langchain.com/langsmith/otel-gateway-trace-redaction>) |
| `Monitor/Trace/Configuration & troubleshooting/Troubleshooting guides/Troubleshoot trace nesting.md` | Troubleshoot trace nesting | Configuration & troubleshooting, Monitor, Trace, Troubleshooting guides, nest, traces | [原文](<https://docs.langchain.com/langsmith/nest-traces>) |
| `Monitor/Trace/Configuration & troubleshooting/Troubleshooting guides/Troubleshoot variable caching.md` | Troubleshoot variable caching | Configuration & troubleshooting, Monitor, Trace, Troubleshooting guides, caching, troubleshooting, variable | [原文](<https://docs.langchain.com/langsmith/troubleshooting-variable-caching>) |
| `Monitor/Trace/Configuration & troubleshooting/Usage and billing.md` | Usage and billing | Understand LangSmith trace data retention tiers, pricing, rate limits, and usage limits.；Configuration & troubleshooting, Monitor, Trace, and, billing, usage | [原文](<https://docs.langchain.com/langsmith/usage-and-billing>) |
| `Monitor/Trace/Observability concepts.md` | Observability concepts | How LangSmith structures observability data as runs, traces, threads, and trajectories, and how to send traces.；Monitor, Trace, concepts, observability | [原文](<https://docs.langchain.com/langsmith/observability-concepts>) |
| `Monitor/Trace/Trace an agent.md` | Trace an agent | Add LangSmith observability to an agent across prototyping, beta testing, and production.；Monitor, Trace, llm, observability, tutorial | [原文](<https://docs.langchain.com/langsmith/observability-llm-tutorial>) |
| `Monitor/Trace/Tracing quickstart.md` | Tracing quickstart | Add LangSmith tracing to an agent in minutes.；Monitor, Trace, observability, quickstart | [原文](<https://docs.langchain.com/langsmith/observability-quickstart>) |
| `Monitor/Trace/Tracing setup/Integrations/Agent frameworks/Trace AutoGen agents.md` | Trace AutoGen agents | [!NOTE]；Agent frameworks, Integrations, Monitor, Trace, Tracing setup, autogen, trace, with | [原文](<https://docs.langchain.com/langsmith/trace-with-autogen>) |
| `Monitor/Trace/Tracing setup/Integrations/Agent frameworks/Trace Claude Managed Agents.md` | Trace Claude Managed Agents | Automatically trace Claude Managed Agent sessions and events with LangSmith.；Agent frameworks, Integrations, Monitor, Trace, Tracing setup, agents, claude, managed, trace, with | [原文](<https://docs.langchain.com/langsmith/trace-with-claude-managed-agents>) |
| `Monitor/Trace/Tracing setup/Integrations/Agent frameworks/Trace CrewAI agents.md` | Trace CrewAI agents | [!NOTE]；Agent frameworks, Integrations, Monitor, Trace, Tracing setup, crewai, trace, with | [原文](<https://docs.langchain.com/langsmith/trace-with-crewai>) |
| `Monitor/Trace/Tracing setup/Integrations/Agent frameworks/Trace Deep Agents.md` | Trace Deep Agents | [!NOTE]；Agent frameworks, Integrations, Monitor, Trace, Tracing setup, agents, deep, trace | [原文](<https://docs.langchain.com/langsmith/trace-deep-agents>) |
| `Monitor/Trace/Tracing setup/Integrations/Agent frameworks/Trace Google ADK agents.md` | Trace Google ADK agents | [!NOTE]；Agent frameworks, Integrations, Monitor, Trace, Tracing setup, adk, google, trace, with | [原文](<https://docs.langchain.com/langsmith/trace-with-google-adk>) |
| `Monitor/Trace/Tracing setup/Integrations/Agent frameworks/Trace LangChain agents (Python and JS-TS).md` | Trace LangChain agents (Python and JS/TS) | [!NOTE]；Agent frameworks, Integrations, Monitor, Trace, Tracing setup, langchain, trace, with | [原文](<https://docs.langchain.com/langsmith/trace-with-langchain>) |
| `Monitor/Trace/Tracing setup/Integrations/Agent frameworks/Trace LangGraph agents.md` | Trace LangGraph agents | [!NOTE]；Agent frameworks, Integrations, Monitor, Trace, Tracing setup, langgraph, trace, with | [原文](<https://docs.langchain.com/langsmith/trace-with-langgraph>) |
| `Monitor/Trace/Tracing setup/Integrations/Agent frameworks/Trace Mastra agents.md` | Trace Mastra agents | [!NOTE]；Agent frameworks, Integrations, Monitor, Trace, Tracing setup, mastra, trace, with | [原文](<https://docs.langchain.com/langsmith/trace-with-mastra>) |
| `Monitor/Trace/Tracing setup/Integrations/Agent frameworks/Trace PydanticAI agents.md` | Trace PydanticAI agents | [!NOTE]；Agent frameworks, Integrations, Monitor, Trace, Tracing setup, ai, pydantic, trace, with | [原文](<https://docs.langchain.com/langsmith/trace-with-pydantic-ai>) |
| `Monitor/Trace/Tracing setup/Integrations/Agent frameworks/Trace Semantic Kernel agents.md` | Trace Semantic Kernel agents | [!NOTE]；Agent frameworks, Integrations, Monitor, Trace, Tracing setup, kernel, semantic, trace, with | [原文](<https://docs.langchain.com/langsmith/trace-with-semantic-kernel>) |
| `Monitor/Trace/Tracing setup/Integrations/Agent frameworks/Trace Vercel AI SDK agents (JS-TS only).md` | Trace Vercel AI SDK agents (JS/TS only) | Trace Vercel AI SDK agents with LangSmith for AI SDK v5, v6, and v7.；Agent frameworks, Integrations, Monitor, Trace, Tracing setup, ai, sdk, trace, vercel, with | [原文](<https://docs.langchain.com/langsmith/trace-with-vercel-ai-sdk>) |
| `Monitor/Trace/Tracing setup/Integrations/Agent frameworks/Trace with Microsoft Agent Framework.md` | Trace with Microsoft Agent Framework | [!NOTE]；Agent frameworks, Integrations, Monitor, Trace, Tracing setup, agent, framework, microsoft, trace, with | [原文](<https://docs.langchain.com/langsmith/trace-with-microsoft-agent-framework>) |
| `Monitor/Trace/Tracing setup/Integrations/Agent frameworks/Trace with OpenTelemetry.md` | Trace with OpenTelemetry | Configure OpenTelemetry tracing in LangSmith, including LANGSMITH_OTEL_ENABLED and OTEL fanout with the OpenTelemetry Collector.；Agent frameworks, Integrations, Monitor, Trace, Tracing setup, opentelemetry, trace, with | [原文](<https://docs.langchain.com/langsmith/trace-with-opentelemetry>) |
| `Monitor/Trace/Tracing setup/Integrations/Agent frameworks/Trace with Strands Agents.md` | Trace with Strands Agents | Trace with Strands Agents with LangSmith.；Agent frameworks, Integrations, Monitor, Trace, Tracing setup, agents, strands, trace, with | [原文](<https://docs.langchain.com/langsmith/trace-with-strands-agents>) |
| `Monitor/Trace/Tracing setup/Integrations/Agent frameworks/Trace with the Claude Agent SDK.md` | Trace with the Claude Agent SDK | [!NOTE]；Agent frameworks, Integrations, Monitor, Trace, Tracing setup, agent, claude, sdk, trace | [原文](<https://docs.langchain.com/langsmith/trace-claude-agent-sdk>) |
| `Monitor/Trace/Tracing setup/Integrations/Agent frameworks/Trace with the OpenAI Agents SDK.md` | Trace with the OpenAI Agents SDK | Trace OpenAI Agents SDK Python and JavaScript agents with LangSmith.；Agent frameworks, Integrations, Monitor, Trace, Tracing setup, agents, openai, sdk, trace, with | [原文](<https://docs.langchain.com/langsmith/trace-with-openai-agents-sdk>) |
| `Monitor/Trace/Tracing setup/Integrations/Developer tools/Coding agent metadata contract.md` | Coding agent metadata contract | The metadata schema that standardizes what trace metadata coding agents must emit when sending runs to LangSmith.；Developer tools, Integrations, Monitor, Trace, Tracing setup, agent, coding, contract, metadata | [原文](<https://docs.langchain.com/langsmith/coding-agent-metadata-contract>) |
| `Monitor/Trace/Tracing setup/Integrations/Developer tools/Trace Claude Code sessions.md` | Trace Claude Code sessions | [!WARNING]；Developer tools, Integrations, Monitor, Trace, Tracing setup, claude, code, trace | [原文](<https://docs.langchain.com/langsmith/trace-claude-code>) |
| `Monitor/Trace/Tracing setup/Integrations/Developer tools/Trace Cursor sessions.md` | Trace Cursor sessions | Capture Cursor agent turns, tool calls, model metadata, token usage, attachments, and subagents in LangSmith.；Developer tools, Integrations, Monitor, Trace, Tracing setup, cursor, trace, with | [原文](<https://docs.langchain.com/langsmith/trace-with-cursor>) |
| `Monitor/Trace/Tracing setup/Integrations/Developer tools/Trace OpenAI Codex sessions.md` | Trace OpenAI Codex sessions | Capture OpenAI Codex agent turns, tool calls, model metadata, and subagent threads in LangSmith.；Developer tools, Integrations, Monitor, Trace, Tracing setup, codex, trace, with | [原文](<https://docs.langchain.com/langsmith/trace-with-codex>) |
| `Monitor/Trace/Tracing setup/Integrations/Developer tools/Trace OpenCode sessions.md` | Trace OpenCode sessions | Capture OpenCode sessions, assistant turns, tool calls, and subagent activity in LangSmith.；Developer tools, Integrations, Monitor, Trace, Tracing setup, opencode, trace, with | [原文](<https://docs.langchain.com/langsmith/trace-with-opencode>) |
| `Monitor/Trace/Tracing setup/Integrations/Developer tools/Trace Pi coding agent sessions.md` | Trace Pi coding agent sessions | Trace Pi coding agent invocations to LangSmith to observe turns, debug tool calls, track token usage, and inspect individual LLM invocations.；Developer tools, Integrations, Monitor, Trace, Tracing setup, pi, trace, with | [原文](<https://docs.langchain.com/langsmith/trace-with-pi>) |
| `Monitor/Trace/Tracing setup/Integrations/Developer tools/Trace Visual Studio Code Copilot Chat sessions.md` | Trace Visual Studio Code Copilot Chat sessions | Capture VS Code Copilot Chat agent interactions, LLM calls, tool executions, and token usage in LangSmith via OpenTelemetry.；Developer tools, Integrations, Monitor, Trace, Tracing setup, copilot, trace, vscode, with | [原文](<https://docs.langchain.com/langsmith/trace-with-vscode-copilot>) |
| `Monitor/Trace/Tracing setup/Integrations/Developer tools/Trace n8n workflows.md` | Trace n8n workflows | Learn how to trace n8n AI workflows in LangSmith.；Developer tools, Integrations, Monitor, Trace, Tracing setup, n8n, trace, with | [原文](<https://docs.langchain.com/langsmith/trace-with-n8n>) |
| `Monitor/Trace/Tracing setup/Integrations/Developer tools/Trace with Instructor.md` | Trace with Instructor | [!NOTE]；Developer tools, Integrations, Monitor, Trace, Tracing setup, instructor, trace, with | [原文](<https://docs.langchain.com/langsmith/trace-with-instructor>) |
| `Monitor/Trace/Tracing setup/Integrations/Developer tools/Trace with Temporal.md` | Trace with Temporal | Learn how to trace Temporal workflows and activities in LangSmith using OpenTelemetry.；Developer tools, Integrations, Monitor, Trace, Tracing setup, temporal, trace, with | [原文](<https://docs.langchain.com/langsmith/trace-with-temporal>) |
| `Monitor/Trace/Tracing setup/Integrations/Integrations.md` | Integrations | Integrations, Monitor, Trace, Tracing setup, integrations | [原文](<https://docs.langchain.com/langsmith/integrations>) |
| `Monitor/Trace/Tracing setup/Integrations/LLM providers/Trace OpenAI-compatible providers.md` | Trace OpenAI-compatible providers | Trace LLM calls from any OpenAI-compatible provider to LangSmith.；Integrations, LLM providers, Monitor, Trace, Tracing setup, compatible, openai, trace, with | [原文](<https://docs.langchain.com/langsmith/trace-with-openai-compatible>) |
| `Monitor/Trace/Tracing setup/Integrations/LLM providers/Trace with Amazon Bedrock.md` | Trace with Amazon Bedrock | [!NOTE]；Integrations, LLM providers, Monitor, Trace, Tracing setup, bedrock, trace | [原文](<https://docs.langchain.com/langsmith/trace-bedrock>) |
| `Monitor/Trace/Tracing setup/Integrations/LLM providers/Trace with Anthropic.md` | Trace with Anthropic | Send Anthropic traces to LangSmith from the Claude Platform, from the Claude SDKs over OpenTelemetry, or with the LangSmith SDK wrapper.；Integrations, LLM providers, Monitor, Trace, Tracing setup, anthropic, trace | [原文](<https://docs.langchain.com/langsmith/trace-anthropic>) |
| `Monitor/Trace/Tracing setup/Integrations/LLM providers/Trace with DeepSeek.md` | Trace with DeepSeek | [!NOTE]；Integrations, LLM providers, Monitor, Trace, Tracing setup, deepseek, trace | [原文](<https://docs.langchain.com/langsmith/trace-deepseek>) |
| `Monitor/Trace/Tracing setup/Integrations/LLM providers/Trace with Google Gemini.md` | Trace with Google Gemini | [!NOTE]；Integrations, LLM providers, Monitor, Trace, Tracing setup, gemini, google, trace, with | [原文](<https://docs.langchain.com/langsmith/trace-with-google-gemini>) |
| `Monitor/Trace/Tracing setup/Integrations/LLM providers/Trace with LiteLLM.md` | Trace with LiteLLM | [!NOTE]；Integrations, LLM providers, Monitor, Trace, Tracing setup, litellm, trace | [原文](<https://docs.langchain.com/langsmith/trace-litellm>) |
| `Monitor/Trace/Tracing setup/Integrations/LLM providers/Trace with Mistral.md` | Trace with Mistral | [!NOTE]；Integrations, LLM providers, Monitor, Trace, Tracing setup, mistral, trace, with | [原文](<https://docs.langchain.com/langsmith/trace-with-mistral>) |
| `Monitor/Trace/Tracing setup/Integrations/LLM providers/Trace with OpenAI.md` | Trace with OpenAI | [!NOTE]；Integrations, LLM providers, Monitor, Trace, Tracing setup, openai, trace | [原文](<https://docs.langchain.com/langsmith/trace-openai>) |
| `Monitor/Trace/Tracing setup/Integrations/Productivity/Trace Claude Cowork sessions.md` | Trace Claude Cowork sessions | Send Claude Cowork tasks, tool calls, and skill use to LangSmith with the LangSmith tracing plugin for Claude.；Integrations, Monitor, Productivity, Trace, Tracing setup, claude, cowork, trace | [原文](<https://docs.langchain.com/langsmith/trace-claude-cowork>) |
| `Monitor/Trace/Tracing setup/Integrations/Voice AI frameworks/Trace Gemini Live agents.md` | Trace Gemini Live agents | Trace Gemini Live voice agents in LangSmith using the LangSmith SDK.；Integrations, Monitor, Trace, Tracing setup, Voice AI frameworks, gemini, live, trace | [原文](<https://docs.langchain.com/langsmith/trace-gemini-live>) |
| `Monitor/Trace/Tracing setup/Integrations/Voice AI frameworks/Trace LiveKit agents.md` | Trace LiveKit agents | [!NOTE]；Integrations, Monitor, Trace, Tracing setup, Voice AI frameworks, livekit, trace, with | [原文](<https://docs.langchain.com/langsmith/trace-with-livekit>) |
| `Monitor/Trace/Tracing setup/Integrations/Voice AI frameworks/Trace OpenAI Realtime agents.md` | Trace OpenAI Realtime agents | Trace OpenAI Realtime voice agents in LangSmith using the LangSmith SDK.；Integrations, Monitor, Trace, Tracing setup, Voice AI frameworks, openai, realtime, trace | [原文](<https://docs.langchain.com/langsmith/trace-openai-realtime>) |
| `Monitor/Trace/Tracing setup/Integrations/Voice AI frameworks/Trace Pipecat agents.md` | Trace Pipecat agents | [!NOTE]；Integrations, Monitor, Trace, Tracing setup, Voice AI frameworks, pipecat, trace, with | [原文](<https://docs.langchain.com/langsmith/trace-with-pipecat>) |
| `Monitor/Trace/Tracing setup/Integrations/Voice AI frameworks/Voice tracing fundamentals.md` | Voice tracing fundamentals | Best practices for tracing voice and audio agents in LangSmith, including conversation audio, single-trace conversations, and the audio modality flag.；Integrations, Monitor, Trace, Tracing setup, Voice AI frameworks, fundamentals, trace, voice | [原文](<https://docs.langchain.com/langsmith/trace-voice-fundamentals>) |
| `Monitor/Trace/Tracing setup/Manual instrumentation/Custom instrumentation.md` | Custom instrumentation | Instrument your code directly to control which functions are traced and how they appear in LangSmith.；Manual instrumentation, Monitor, Trace, Tracing setup, annotate, code | [原文](<https://docs.langchain.com/langsmith/annotate-code>) |
| `Monitor/Trace/Tracing setup/Manual instrumentation/Log LLM calls.md` | Log LLM calls | [!NOTE]；Manual instrumentation, Monitor, Trace, Tracing setup, llm, log, trace | [原文](<https://docs.langchain.com/langsmith/log-llm-trace>) |
| `Monitor/Trace/Tracing setup/Manual instrumentation/Log retriever traces.md` | Log retriever traces | Log retrieval steps in LangSmith traces for document-level visibility into your RAG pipeline.；Manual instrumentation, Monitor, Trace, Tracing setup, log, retriever, trace | [原文](<https://docs.langchain.com/langsmith/log-retriever-trace>) |
| `Monitor/Trace/Tracing setup/Manual instrumentation/Metadata parameters reference.md` | Metadata parameters reference | Manual instrumentation, Monitor, Trace, Tracing setup, ls, metadata, parameters | [原文](<https://docs.langchain.com/langsmith/ls-metadata-parameters>) |
| `Monitor/Trace/Tracing setup/Manual instrumentation/Trace with API.md` | Trace with API | Learn how to trace LLM applications using the LangSmith REST API directly.；Manual instrumentation, Monitor, Trace, Tracing setup, api, trace, with | [原文](<https://docs.langchain.com/langsmith/trace-with-api>) |
| `Monitor/Trace/Tracing setup/Manual instrumentation/Upload files with traces.md` | Upload files with traces | [!NOTE]；Manual instrumentation, Monitor, Trace, Tracing setup, files, traces, upload, with | [原文](<https://docs.langchain.com/langsmith/upload-files-with-traces>) |
| `No-code agents/Fleet/Additional resources/Access & oversight.md` | Access & oversight | Control who can access agents, how they authenticate, and audit everything they do.；Additional resources, Fleet, No-code agents, access, and, oversight | [原文](<https://docs.langchain.com/langsmith/fleet/access-and-oversight>) |
| `No-code agents/Fleet/Additional resources/LangSmith Fleet changelog.md` | LangSmith Fleet changelog | Weekly updates to LangSmith Fleet；Additional resources, Fleet, No-code agents, changelog | [原文](<https://docs.langchain.com/langsmith/fleet/changelog>) |
| `No-code agents/Fleet/Advanced/Auth-aware tool responses.md` | Auth-aware tool responses | Format tool responses to trigger OAuth flows and resume execution automatically.；Advanced, Fleet, No-code agents, auth, format | [原文](<https://docs.langchain.com/langsmith/fleet/auth-format>) |
| `No-code agents/Fleet/Advanced/Fleet webhooks.md` | Fleet webhooks | Integrate agent publishing with external systems, CI/CD pipelines, or custom deployment workflows.；Advanced, Fleet, No-code agents, webhooks | [原文](<https://docs.langchain.com/langsmith/fleet/webhooks>) |
| `No-code agents/Fleet/Advanced/LangSmith Tool Server.md` | LangSmith Tool Server | [!NOTE]；Advanced, Fleet, No-code agents, framework, mcp | [原文](<https://docs.langchain.com/langsmith/fleet/mcp-framework>) |
| `No-code agents/Fleet/Advanced/Use Fleet agents in code.md` | Use Fleet agents in code | Invoke Fleet agents via the LangGraph SDK or REST API, or download and run them locally with the fleet-deepagents-export package.；Advanced, Fleet, No-code agents, code | [原文](<https://docs.langchain.com/langsmith/fleet/code>) |
| `No-code agents/Fleet/Configure/Agent identity.md` | Agent identity | Choose whether your Fleet agent authenticates with its own credentials or with each user's credentials.；Configure, Fleet, No-code agents, agent, identity | [原文](<https://docs.langchain.com/langsmith/fleet/agent-identity>) |
| `No-code agents/Fleet/Configure/Computer use.md` | Computer use | Run code, manage files, and call authenticated APIs from a persistent virtual computer attached to your Fleet agent.；Configure, Fleet, No-code agents, computer, use | [原文](<https://docs.langchain.com/langsmith/fleet/computer-use>) |
| `No-code agents/Fleet/Configure/Manage agent settings.md` | Manage agent settings | Manage your agents in Fleet.；Configure, Fleet, No-code agents, agent, manage, settings | [原文](<https://docs.langchain.com/langsmith/fleet/manage-agent-settings>) |
| `No-code agents/Fleet/Configure/Manage workspace administration.md` | Manage workspace administration | Configure workspace-level settings for Fleet.；Configure, Fleet, No-code agents, admin, workspace | [原文](<https://docs.langchain.com/langsmith/fleet/workspace-admin>) |
| `No-code agents/Fleet/Get started/Agent platform comparison.md` | Agent platform comparison | Compare LangSmith Fleet with Claude Cowork, Amazon Quick, Google Workspace Studio, and Microsoft Copilot to choose the right enterprise agent platform for your team；Fleet, Get started, No-code agents, comparison | [原文](<https://docs.langchain.com/langsmith/fleet/comparison>) |
| `No-code agents/Fleet/Get started/Essentials.md` | Essentials | Fleet's core features；Fleet, Get started, No-code agents, essentials | [原文](<https://docs.langchain.com/langsmith/fleet/essentials>) |
| `No-code agents/Fleet/Get started/Quickstart.md` | Quickstart | Build an agent from a template；Fleet, Get started, No-code agents, quickstart | [原文](<https://docs.langchain.com/langsmith/fleet/quickstart>) |
| `No-code agents/Fleet/Get started/Templates.md` | Templates | Start faster with curated Fleet templates and customize tools, prompts, and channels.；Fleet, Get started, No-code agents, templates | [原文](<https://docs.langchain.com/langsmith/fleet/templates>) |
| `No-code agents/Fleet/No-code agents with LangSmith Fleet.md` | No-code agents with LangSmith Fleet | Create helpful AI agents without code. Start from a template, connect your accounts, and let the agent handle routine work while you stay in control.；Fleet, No-code agents, index | [原文](<https://docs.langchain.com/langsmith/fleet/index>) |
| `No-code agents/Fleet/Tools and automation/Arcade integration.md` | Arcade integration | Connect your workspace to Arcade to give agents access to third-party tools like GitHub, Gmail, Slack, and more.；Fleet, No-code agents, Tools and automation, arcade | [原文](<https://docs.langchain.com/langsmith/fleet/arcade>) |
| `No-code agents/Fleet/Tools and automation/Channels.md` | Channels | Configure channels to trigger your Fleet agents automatically.；Fleet, No-code agents, Tools and automation, channels | [原文](<https://docs.langchain.com/langsmith/fleet/channels>) |
| `No-code agents/Fleet/Tools and automation/Integrate Microsoft Teams with an agent.md` | Integrate Microsoft Teams with an agent | Connect LangSmith Fleet to Microsoft Teams by bringing your own Azure Bot to let agents communicate with users in Teams.；Fleet, No-code agents, Tools and automation, app, teams | [原文](<https://docs.langchain.com/langsmith/fleet/teams-app>) |
| `No-code agents/Fleet/Tools and automation/Integrate Slack with an agent.md` | Integrate Slack with an agent | Connect LangSmith Fleet to your Slack workspace so your agents work as Slack bots your team can tag directly.；Fleet, No-code agents, Tools and automation, app, slack | [原文](<https://docs.langchain.com/langsmith/fleet/slack-app>) |
| `No-code agents/Fleet/Tools and automation/Remote MCP servers.md` | Remote MCP servers | Connect Fleet to popular remote MCP servers；Fleet, No-code agents, Tools and automation, mcp, remote, servers | [原文](<https://docs.langchain.com/langsmith/fleet/remote-mcp-servers>) |
| `No-code agents/Fleet/Tools and automation/Salesforce integration.md` | Salesforce integration | Connect LangSmith Fleet to Salesforce so your agents can query records, navigate schemas, and read custom fields.；Fleet, No-code agents, Tools and automation, salesforce | [原文](<https://docs.langchain.com/langsmith/fleet/salesforce>) |
| `No-code agents/Fleet/Tools and automation/Schedules.md` | Schedules | Configure schedules to run your Fleet agents on a recurring basis.；Fleet, No-code agents, Tools and automation, schedules | [原文](<https://docs.langchain.com/langsmith/fleet/schedules>) |
| `No-code agents/Fleet/Tools and automation/Skills.md` | Skills | Use skills to give your agents access to specific capabilities.；Fleet, No-code agents, Tools and automation, skills | [原文](<https://docs.langchain.com/langsmith/fleet/skills>) |
| `No-code agents/Fleet/Tools and automation/Tool integrations.md` | Tool integrations | Give your agents access to a wide range of tools and services.；Fleet, No-code agents, Tools and automation, tools | [原文](<https://docs.langchain.com/langsmith/fleet/tools>) |
| `No-code agents/Studio/Build an agent with LangSmith Studio.md` | Build an agent with LangSmith Studio | Describe an agent in Studio, let LangSmith Chat draft its configuration, then review, save, and test it without writing code.；No-code agents, Studio, agent, an, build | [原文](<https://docs.langchain.com/langsmith/build-an-agent>) |
| `Test/Annotation Queues/Annotate traces and runs inline.md` | Annotate traces and runs inline | [!NOTE]；Annotation Queues, Test, annotate, inline, traces | [原文](<https://docs.langchain.com/langsmith/annotate-traces-inline>) |
| `Test/Annotation Queues/Build custom views for annotation queues.md` | Build custom views for annotation queues | Build a custom view with LangSmith Chat to control how runs and threads appear to reviewers in an annotation queue.；Annotation Queues, Test, annotation, custom, queue, views | [原文](<https://docs.langchain.com/langsmith/annotation-queue-custom-views>) |
| `Test/Annotation Queues/Feedback/Collect feedback with presigned URLs.md` | Collect feedback with presigned URLs | Use presigned feedback tokens to collect user feedback from client-side applications without exposing your LangSmith API key.；Annotation Queues, Feedback, Test, feedback, presigned, tokens | [原文](<https://docs.langchain.com/langsmith/presigned-feedback-tokens>) |
| `Test/Annotation Queues/Feedback/Log user feedback using the SDK.md` | Log user feedback using the SDK | [!NOTE]；Annotation Queues, Feedback, Test, attach, feedback, user | [原文](<https://docs.langchain.com/langsmith/attach-user-feedback>) |
| `Test/Annotation Queues/Manage feedback & annotation queues programmatically.md` | Manage feedback & annotation queues programmatically | [!NOTE]；Annotation Queues, Test, annotation, queues, sdk | [原文](<https://docs.langchain.com/langsmith/annotation-queues-sdk>) |
| `Test/Annotation Queues/Set up feedback criteria.md` | Set up feedback criteria | [!TIP]；Annotation Queues, Test, criteria, feedback, set, up | [原文](<https://docs.langchain.com/langsmith/set-up-feedback-criteria>) |
| `Test/Annotation Queues/Use annotation queues.md` | Use annotation queues | [!NOTE]；Annotation Queues, Test, annotation, queues | [原文](<https://docs.langchain.com/langsmith/annotation-queues>) |
| `Test/Annotation Queues/Use assertions.md` | Use assertions | Capture free-form acceptance criteria as dataset examples by writing assertions while reviewing runs in an annotation queue.；Annotation Queues, Test, assertions | [原文](<https://docs.langchain.com/langsmith/assertions>) |
| `Test/Datasets & Experiments/Analyze experiment results/Analyze an experiment.md` | Analyze an experiment | [!TIP]；Analyze experiment results, Datasets & Experiments, Test, an, analyze, experiment | [原文](<https://docs.langchain.com/langsmith/analyze-an-experiment>) |
| `Test/Datasets & Experiments/Analyze experiment results/How to compare experiment results.md` | How to compare experiment results | Analyze experiment results, Datasets & Experiments, Test, compare, experiment, results | [原文](<https://docs.langchain.com/langsmith/compare-experiment-results>) |
| `Test/Datasets & Experiments/Analyze experiment results/How to fetch performance metrics for an experiment.md` | How to fetch performance metrics for an experiment | [!TIP]；Analyze experiment results, Datasets & Experiments, Test, experiment, fetch, metrics, perf | [原文](<https://docs.langchain.com/langsmith/fetch-perf-metrics-experiment>) |
| `Test/Datasets & Experiments/Analyze experiment results/How to filter experiments in the UI.md` | How to filter experiments in the UI | Analyze experiment results, Datasets & Experiments, Test, experiments, filter, ui | [原文](<https://docs.langchain.com/langsmith/filter-experiments-ui>) |
| `Test/Datasets & Experiments/Analyze experiment results/How to upload experiments run outside of LangSmith with the REST API.md` | How to upload experiments run outside of LangSmith with the REST API | Analyze experiment results, Datasets & Experiments, Test, existing, experiments, upload | [原文](<https://docs.langchain.com/langsmith/upload-existing-experiments>) |
| `Test/Datasets & Experiments/Analyze experiment results/LangSmith Chat.md` | LangSmith Chat | Use Chat in LangSmith to analyze traces, threads, prompts, and evaluations.；Analyze experiment results, Datasets & Experiments, Test, chat, evaluation | [原文](<https://docs.langchain.com/langsmith/chat-evaluation>) |
| `Test/Datasets & Experiments/Common data types/Dataset prebuilt JSON schema types.md` | Dataset prebuilt JSON schema types | Common data types, Datasets & Experiments, Test, dataset, json, types | [原文](<https://docs.langchain.com/langsmith/dataset-json-types>) |
| `Test/Datasets & Experiments/Common data types/Dataset transformations.md` | Dataset transformations | [!TIP]；Common data types, Datasets & Experiments, Test, dataset, transformations | [原文](<https://docs.langchain.com/langsmith/dataset-transformations>) |
| `Test/Datasets & Experiments/Common data types/Example data format.md` | Example data format | [!TIP]；Common data types, Datasets & Experiments, Test, data, example, format | [原文](<https://docs.langchain.com/langsmith/example-data-format>) |
| `Test/Datasets & Experiments/Datasets/Create a dataset/Create and manage datasets in the UI.md` | Create and manage datasets in the UI | [!TIP]；Create a dataset, Datasets, Datasets & Experiments, Test, application, datasets, in, manage | [原文](<https://docs.langchain.com/langsmith/manage-datasets-in-application>) |
| `Test/Datasets & Experiments/Datasets/Create a dataset/How to create and manage datasets programmatically.md` | How to create and manage datasets programmatically | [!TIP]；Create a dataset, Datasets, Datasets & Experiments, Test, datasets, manage, programmatically | [原文](<https://docs.langchain.com/langsmith/manage-datasets-programmatically>) |
| `Test/Datasets & Experiments/Datasets/Custom output rendering.md` | Custom output rendering | [!NOTE]；Datasets, Datasets & Experiments, Test, custom, output, rendering | [原文](<https://docs.langchain.com/langsmith/custom-output-rendering>) |
| `Test/Datasets & Experiments/Datasets/Manage datasets.md` | Manage datasets | [!TIP]；Datasets, Datasets & Experiments, Test, datasets, manage | [原文](<https://docs.langchain.com/langsmith/manage-datasets>) |
| `Test/Datasets & Experiments/Evaluation techniques/Define evaluation target/How to define a target function to evaluate.md` | How to define a target function to evaluate | [!TIP]；Datasets & Experiments, Define evaluation target, Evaluation techniques, Test, define, function, target | [原文](<https://docs.langchain.com/langsmith/define-target-function>) |
| `Test/Datasets & Experiments/Evaluation techniques/Define evaluation target/How to evaluate a graph.md` | How to evaluate a graph | [!NOTE]；Datasets & Experiments, Define evaluation target, Evaluation techniques, Test, evaluate, graph | [原文](<https://docs.langchain.com/langsmith/evaluate-graph>) |
| `Test/Datasets & Experiments/Evaluation techniques/Define evaluation target/How to evaluate a runnable.md` | How to evaluate a runnable | [!NOTE]；Datasets & Experiments, Define evaluation target, Evaluation techniques, Test, langchain, runnable | [原文](<https://docs.langchain.com/langsmith/langchain-runnable>) |
| `Test/Datasets & Experiments/Evaluation techniques/Define evaluation target/How to evaluate an application's intermediate steps.md` | How to evaluate an application's intermediate steps | Datasets & Experiments, Define evaluation target, Evaluation techniques, Test, evaluate, intermediate, on, steps | [原文](<https://docs.langchain.com/langsmith/evaluate-on-intermediate-steps>) |
| `Test/Datasets & Experiments/Evaluation techniques/Define evaluation target/How to evaluate your agent with trajectory evaluations.md` | How to evaluate your agent with trajectory evaluations | [!NOTE]；Datasets & Experiments, Define evaluation target, Evaluation techniques, Test, evals, trajectory | [原文](<https://docs.langchain.com/langsmith/trajectory-evals>) |
| `Test/Datasets & Experiments/Evaluation techniques/Define evaluation target/How to simulate multi-turn interactions.md` | How to simulate multi-turn interactions | [!NOTE]；Datasets & Experiments, Define evaluation target, Evaluation techniques, Test, multi, simulation, turn | [原文](<https://docs.langchain.com/langsmith/multi-turn-simulation>) |
| `Test/Datasets & Experiments/Evaluation techniques/Experiment configuration/Experiment configuration.md` | Experiment configuration | Datasets & Experiments, Evaluation techniques, Experiment configuration, Test, configuration, experiment | [原文](<https://docs.langchain.com/langsmith/experiment-configuration>) |
| `Test/Datasets & Experiments/Evaluation techniques/Experiment configuration/How to add evaluators to an existing experiment (Python only).md` | How to add evaluators to an existing experiment (Python only) | Datasets & Experiments, Evaluation techniques, Experiment configuration, Test, evaluate, existing, experiment | [原文](<https://docs.langchain.com/langsmith/evaluate-existing-experiment>) |
| `Test/Datasets & Experiments/Evaluation techniques/Experiment configuration/How to evaluate with repetitions.md` | How to evaluate with repetitions | Datasets & Experiments, Evaluation techniques, Experiment configuration, Test, repetition | [原文](<https://docs.langchain.com/langsmith/repetition>) |
| `Test/Datasets & Experiments/Evaluation techniques/Experiment configuration/How to handle model rate limits.md` | How to handle model rate limits | Datasets & Experiments, Evaluation techniques, Experiment configuration, Test, handle, limiting, model, rate | [原文](<https://docs.langchain.com/langsmith/handle-model-rate-limiting>) |
| `Test/Datasets & Experiments/Evaluation techniques/Experiment configuration/How to read experiment results locally.md` | How to read experiment results locally | [!NOTE]；Datasets & Experiments, Evaluation techniques, Experiment configuration, Test, experiment, local, read, results | [原文](<https://docs.langchain.com/langsmith/read-local-experiment-results>) |
| `Test/Datasets & Experiments/Evaluation techniques/Experiment configuration/How to retry failed runs in experiments (Python only).md` | How to retry failed runs in experiments (Python only) | Datasets & Experiments, Evaluation techniques, Experiment configuration, Test, evaluate, retry, with | [原文](<https://docs.langchain.com/langsmith/evaluate-with-retry>) |
| `Test/Datasets & Experiments/Evaluation techniques/Experiment configuration/How to run an evaluation asynchronously.md` | How to run an evaluation asynchronously | [!NOTE]；Datasets & Experiments, Evaluation techniques, Experiment configuration, Test, async, evaluation | [原文](<https://docs.langchain.com/langsmith/evaluation-async>) |
| `Test/Datasets & Experiments/Evaluation techniques/Experiment configuration/How to run an evaluation locally (Python only).md` | How to run an evaluation locally (Python only) | [!NOTE]；Datasets & Experiments, Evaluation techniques, Experiment configuration, Test, local | [原文](<https://docs.langchain.com/langsmith/local>) |
| `Test/Datasets & Experiments/Evaluation techniques/Multimodal evaluations/Run an evaluation with multimodal content.md` | Run an evaluation with multimodal content | Learn how to create dataset examples with file attachments and use them in prompts and evaluators when running LangSmith evaluations with multimodal content.；Datasets & Experiments, Evaluation techniques, Multimodal evaluations, Test, attachments, evaluate, with | [原文](<https://docs.langchain.com/langsmith/evaluate-with-attachments>) |
| `Test/Datasets & Experiments/Evaluation techniques/Scoring methods/How to return categorical vs numerical metrics.md` | How to return categorical vs numerical metrics | Datasets & Experiments, Evaluation techniques, Scoring methods, Test, metric, type | [原文](<https://docs.langchain.com/langsmith/metric-type>) |
| `Test/Datasets & Experiments/Evaluation techniques/Scoring methods/How to return multiple scores in one evaluator.md` | How to return multiple scores in one evaluator | Datasets & Experiments, Evaluation techniques, Scoring methods, Test, multiple, scores | [原文](<https://docs.langchain.com/langsmith/multiple-scores>) |
| `Test/Datasets & Experiments/Fine-tuning/Fine-tune models with Smithtune.md` | Fine-tune models with Smithtune | Use Smithtune to fine-tune models on LangSmith conversations and compare the results in LangSmith.；Datasets & Experiments, Fine-tuning, Test, smithtune | [原文](<https://docs.langchain.com/langsmith/smithtune>) |
| `Test/Datasets & Experiments/Run an evaluation/How to evaluate agents.md` | How to evaluate agents | [!NOTE]；Datasets & Experiments, Run an evaluation, Test, application, evaluate, llm | [原文](<https://docs.langchain.com/langsmith/evaluate-llm-application>) |
| `Test/Datasets & Experiments/Run an evaluation/How to evaluate with OpenTelemetry.md` | How to evaluate with OpenTelemetry | [!NOTE]；Datasets & Experiments, Run an evaluation, Test, evaluate, opentelemetry, with | [原文](<https://docs.langchain.com/langsmith/evaluate-with-opentelemetry>) |
| `Test/Datasets & Experiments/Run an evaluation/How to use the REST API.md` | How to use the REST API | Datasets & Experiments, Run an evaluation, Test, api, evals, only, run | [原文](<https://docs.langchain.com/langsmith/run-evals-api-only>) |
| `Test/Datasets & Experiments/Run an evaluation/Run an evaluation from the Playground.md` | Run an evaluation from the Playground | Datasets & Experiments, Run an evaluation, Test, link, playground | [原文](<https://docs.langchain.com/langsmith/playground-link>) |
| `Test/Datasets & Experiments/Tutorials/Evaluate a RAG application.md` | Evaluate a RAG application | [!NOTE]；Datasets & Experiments, Test, Tutorials, evaluate, rag, tutorial | [原文](<https://docs.langchain.com/langsmith/evaluate-rag-tutorial>) |
| `Test/Datasets & Experiments/Tutorials/Evaluate a chatbot.md` | Evaluate a chatbot | [accordion] Click to see a consolidated code snippet；Datasets & Experiments, Test, Tutorials, chatbot, evaluate, tutorial | [原文](<https://docs.langchain.com/langsmith/evaluate-chatbot-tutorial>) |
| `Test/Datasets & Experiments/Tutorials/Evaluate a complex agent.md` | Evaluate a complex agent | [accordion] Reference code；Datasets & Experiments, Test, Tutorials, agent, complex, evaluate | [原文](<https://docs.langchain.com/langsmith/evaluate-complex-agent>) |
| `Test/Datasets & Experiments/Tutorials/Run backtests on a new version of an agent.md` | Run backtests on a new version of an agent | [!NOTE]；Datasets & Experiments, Test, Tutorials, agent, backtests, new, run | [原文](<https://docs.langchain.com/langsmith/run-backtests-new-agent>) |
| `Test/Datasets & Experiments/Tutorials/Test a ReAct agent with Pytest-Vitest and LangSmith.md` | Test a ReAct agent with Pytest/Vitest and LangSmith | [!WARNING]；Datasets & Experiments, Test, Tutorials, agent, pytest, react, test | [原文](<https://docs.langchain.com/langsmith/test-react-agent-pytest>) |
| `Test/Evaluators/Automatically run evaluators on experiments.md` | Automatically run evaluators on experiments | [!NOTE]；Evaluators, Test, bind, dataset, evaluator, to | [原文](<https://docs.langchain.com/langsmith/bind-evaluator-to-dataset>) |
| `Test/Evaluators/Evaluation types.md` | Evaluation types | Evaluators, Test, evaluation, types | [原文](<https://docs.langchain.com/langsmith/evaluation-types>) |
| `Test/Evaluators/Evaluator types/SDK/How to create a composite evaluator.md` | How to create a composite evaluator | [!NOTE]；Evaluator types, Evaluators, SDK, Test, composite, evaluators, sdk | [原文](<https://docs.langchain.com/langsmith/composite-evaluators-sdk>) |
| `Test/Evaluators/Evaluator types/SDK/How to define a code evaluator.md` | How to define a code evaluator | [!TIP]；Evaluator types, Evaluators, SDK, Test, code, evaluator, sdk | [原文](<https://docs.langchain.com/langsmith/code-evaluator-sdk>) |
| `Test/Evaluators/Evaluator types/SDK/How to define a summary evaluator.md` | How to define a summary evaluator | Evaluator types, Evaluators, SDK, Test, summary | [原文](<https://docs.langchain.com/langsmith/summary>) |
| `Test/Evaluators/Evaluator types/SDK/How to define an LLM-as-a-judge evaluator.md` | How to define an LLM-as-a-judge evaluator | [!TIP]；Evaluator types, Evaluators, SDK, Test, as, judge, llm, sdk | [原文](<https://docs.langchain.com/langsmith/llm-as-judge-sdk>) |
| `Test/Evaluators/Evaluator types/SDK/How to run a pairwise evaluation.md` | How to run a pairwise evaluation | [!NOTE]；Evaluator types, Evaluators, SDK, Test, evaluate, pairwise | [原文](<https://docs.langchain.com/langsmith/evaluate-pairwise>) |
| `Test/Evaluators/Evaluator types/UI/How to create a composite evaluator.md` | How to create a composite evaluator | [!NOTE]；Evaluator types, Evaluators, Test, UI, composite, evaluators, ui | [原文](<https://docs.langchain.com/langsmith/composite-evaluators-ui>) |
| `Test/Evaluators/Evaluator types/UI/How to define a code evaluator.md` | How to define a code evaluator | [!NOTE]；Evaluator types, Evaluators, Test, UI, code, evaluator, ui | [原文](<https://docs.langchain.com/langsmith/code-evaluator-ui>) |
| `Test/Evaluators/Evaluator types/UI/How to define a decision model evaluator.md` | How to define a decision model evaluator | Set up a LangSmith evaluator that uses a decision model as the judge with questions that each return typed feedback.；Evaluator types, Evaluators, Test, UI, decision, evaluator, model | [原文](<https://docs.langchain.com/langsmith/decision-model-evaluator>) |
| `Test/Evaluators/Evaluator types/UI/How to define an LLM-as-a-judge evaluator.md` | How to define an LLM-as-a-judge evaluator | [!NOTE]；Evaluator types, Evaluators, Test, UI, as, judge, llm | [原文](<https://docs.langchain.com/langsmith/llm-as-judge>) |
| `Test/Evaluators/Frameworks & integrations/Harbor integrations.md` | Harbor integrations | Run evaluations, Deep Agents, and sandboxes on LangSmith with Harbor.；Evaluators, Frameworks & integrations, Test, harbor, integrations | [原文](<https://docs.langchain.com/langsmith/harbor-integrations>) |
| `Test/Evaluators/Frameworks & integrations/How to run evaluations with Vitest-Jest.md` | How to run evaluations with Vitest/Jest | [!NOTE]；Evaluators, Frameworks & integrations, Test, jest, vitest | [原文](<https://docs.langchain.com/langsmith/vitest-jest>) |
| `Test/Evaluators/Frameworks & integrations/How to run evaluations with pytest.md` | How to run evaluations with pytest | [!NOTE]；Evaluators, Frameworks & integrations, Test, pytest | [原文](<https://docs.langchain.com/langsmith/pytest>) |
| `Test/Evaluators/Frameworks & integrations/Run evals with openevals package.md` | Run evals with openevals package | Run evaluations using the open-source openevals and agentevals packages with LangSmith.；Evaluators, Frameworks & integrations, Test, openevals | [原文](<https://docs.langchain.com/langsmith/openevals>) |
| `Test/Evaluators/Improve evaluators/How to audit evaluator scores.md` | How to audit evaluator scores | Evaluators, Improve evaluators, Test, audit, evaluator, scores | [原文](<https://docs.langchain.com/langsmith/audit-evaluator-scores>) |
| `Test/Evaluators/Improve evaluators/How to improve your evaluator with few-shot examples.md` | How to improve your evaluator with few-shot examples | [!NOTE]；Evaluators, Improve evaluators, Test, create, evaluators, few, shot | [原文](<https://docs.langchain.com/langsmith/create-few-shot-evaluators>) |
| `Test/Evaluators/Improve evaluators/Improve LLM-as-judge evaluators using human feedback.md` | Improve LLM-as-judge evaluators using human feedback | [!TIP]；Evaluators, Improve evaluators, Test, evaluator, feedback, improve, judge | [原文](<https://docs.langchain.com/langsmith/improve-judge-evaluator-feedback>) |
| `Test/Evaluators/Manage evaluators with the SDK.md` | Manage evaluators with the SDK | Create, retrieve, update, list, and delete LangSmith evaluators programmatically with the SDK.；Evaluators, Test, evaluators, manage, sdk | [原文](<https://docs.langchain.com/langsmith/manage-evaluators-sdk>) |
| `Test/Evaluators/Manage evaluators.md` | Manage evaluators | View and manage evaluators at the workspace level in LangSmith.；Evaluators, Test, evaluators | [原文](<https://docs.langchain.com/langsmith/evaluators>) |
| `Test/Evaluators/Track and limit evaluator spend.md` | Track and limit evaluator spend | Cap weekly LLM spend on evaluators with an organization-wide default or per-evaluator overrides to keep evaluator costs predictable.；Evaluators, Test, evaluator, spend | [原文](<https://docs.langchain.com/langsmith/evaluator-spend>) |
| `Test/Get started/Application-specific evaluation approaches.md` | Application-specific evaluation approaches | Get started, Test, approaches, evaluation | [原文](<https://docs.langchain.com/langsmith/evaluation-approaches>) |
| `Test/Get started/Evaluation concepts.md` | Evaluation concepts | Get started, Test, concepts, evaluation | [原文](<https://docs.langchain.com/langsmith/evaluation-concepts>) |
| `Test/Get started/Evaluation quickstart.md` | Evaluation quickstart | [tab] UI；Get started, Test, evaluation, quickstart | [原文](<https://docs.langchain.com/langsmith/evaluation-quickstart>) |
| `Test/Get started/LangSmith Evaluation.md` | LangSmith Evaluation | Evaluate and test agent quality at scale with datasets, evaluators, prompts, and Studio.；Get started, Test, evaluation | [原文](<https://docs.langchain.com/langsmith/evaluation>) |
| `Test/Test from Playground/Test from the Playground.md` | Test from the Playground | Test prompts and model configurations over datasets in the LangSmith Playground without writing code.；Test, Test from Playground, from, playground, test | [原文](<https://docs.langchain.com/langsmith/test-from-playground>) |
| `Test/Test from Studio/Get started with Studio.md` | Get started with Studio | [tab] VS Code；Test, Test from Studio, quick, start, studio | [原文](<https://docs.langchain.com/langsmith/quick-start-studio>) |
| `Test/Test from Studio/How to use Studio.md` | How to use Studio | [tab] Graph；Test, Test from Studio, studio, use | [原文](<https://docs.langchain.com/langsmith/use-studio>) |
| `Test/Test from Studio/LangSmith Studio.md` | LangSmith Studio | [!NOTE]；Test, Test from Studio, studio | [原文](<https://docs.langchain.com/langsmith/studio>) |
| `Test/Test from Studio/Observability in Studio.md` | Observability in Studio | [accordion] Full example configuration；Test, Test from Studio, observability, studio | [原文](<https://docs.langchain.com/langsmith/observability-studio>) |
| `Test/Test from Studio/Studio troubleshooting.md` | Studio troubleshooting | [tab] Python；Test, Test from Studio, studio, troubleshooting | [原文](<https://docs.langchain.com/langsmith/troubleshooting-studio>) |

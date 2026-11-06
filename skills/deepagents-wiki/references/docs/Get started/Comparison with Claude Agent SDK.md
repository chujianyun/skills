# Comparison with Claude Agent SDK

> Compare LangChain Deep Agents and Managed Deep Agents with the Claude Agent SDK to choose the right tool for your use case.

This page explains how [Deep Agents](../Deep%20Agents%20overview.md) compares to the [Claude Agent SDK](https://platform.anthropic.com/docs/en/agent-sdk/overview). Both are harnesses for building custom agents, but they make different tradeoffs around execution environments, deployment, and vendor coupling.

> [!NOTE]
>
> Deep Agents is used in production by [OpenSWE](https://github.com/langchain-ai/open-swe) and [LangSmith Fleet](https://docs.langchain.com/langsmith/fleet/index.md).

## At a glance

| | **Deep Agents** | **Claude Agent SDK** |
| - | - | - |
| **Where the agent runs** | Inside a sandbox, or outside a sandbox executing commands remotely | Inside a sandbox |
| **Execution backend** | Pluggable in the [SDK](../Execution%20environment/Backends.md): local, virtual filesystem, remote sandbox, or custom. [Managed Deep Agents](https://docs.langchain.com/langsmith/python/managed-deep-agents-sandboxes.md) uses one managed sandbox declared in the project. | Local filesystem of the sandbox it runs in |
| **Model provider** | Any (Anthropic, OpenAI, Google, 100+ others) | Claude (Anthropic, Bedrock, Vertex, Azure) |
| **Per-provider/model tuning** | [Harness profiles](../Context%20management/Profiles.md) (beta): declarative bundles of system prompt, tool, middleware, and subagent tweaks, registered per provider or specific model | Configure in code at each model call site |
| **Deployment** | Default: [Managed Deep Agents](../Deployment/Managed%20Deep%20Agents.md) (`mda deploy` on LangSmith). Or self-host a [standalone image](https://docs.langchain.com/langsmith/deploy-standalone-server.md) via [`langgraph build`](https://docs.langchain.com/langsmith/cli#build). | [Self-host](https://code.claude.com/docs/en/agent-sdk/hosting). You build the server, auth, and streaming layer. [Claude managed agents](https://platform.claude.com/docs/en/managed-agents/overview) is a separate product |
| **Multi-tenancy** | [Built-in](../Deployment/Going%20to%20production/index.md#multi-tenancy): scoped threads, per-user sandboxes, RBAC. Managed Deep Agents adds [identity](https://docs.langchain.com/langsmith/python/managed-deep-agents-identity.md) and per-user connections. | Build it yourself |
| **License** | MIT | MIT (Claude Code itself is proprietary) |

## Main differences

### Agent and execution environment

There are [two patterns for connecting agents to sandboxes](https://www.langchain.com/blog/the-two-patterns-by-which-agents-connect-sandboxes): running the agent *inside* the sandbox, or running the agent outside and **using the sandbox as a tool**.

The Claude Agent SDK only supports the first. Your agent runs inside a sandbox and executes tools against the sandbox's local filesystem. Anthropic's hosted model [Claude managed agents](https://platform.claude.com/docs/en/managed-agents/overview) use a decoupled model, which reflects where production agent architectures are heading.

Deep Agents supports both. With the [Deep Agents SDK](../Deep%20Agents%20overview.md#self-host-with-the-sdk), you pick a [backend](../Execution%20environment/Backends.md#quickstart) to wire them together:

* Run the agent inside a sandbox (same model as Claude Agent SDK).
* Run the agent in a long-lived container and [use a remote sandbox as a tool](https://www.langchain.com/blog/the-two-patterns-by-which-agents-connect-sandboxes), executing commands over the network.
* Swap in a virtual filesystem for tests, or a custom backend for your own infrastructure.

With [Managed Deep Agents](https://docs.langchain.com/langsmith/python/managed-deep-agents-sandboxes.md), LangSmith owns the sandbox lifecycle. You declare a sandbox in the project; the managed runtime creates it, snapshots it, and stops it when idle.

### Multi-tenancy

When you put your application into production, you generally expose it to many end users and must isolate the environment for each user.

In Claude Agent SDK, the SDK ties the agent to its sandbox. To give each user an isolated execution environment, you must build an API wrapper that spins up a sandbox per user, tracks which sandbox belongs to whom, and tears it down afterwards.

Deep Agents handles this directly: configure a sandbox [per user or per assistant](../Deployment/Going%20to%20production/index.md#lifecycle) in the harness, with scoped threads, run history, and [RBAC](../Deployment/Going%20to%20production/index.md#role-based-access-control) included. If you use [LangSmith Sandbox](https://docs.langchain.com/langsmith/sandbox-auth-proxy.md), you also get an auth proxy out of the box so end users can call third-party APIs from the sandbox without you provisioning credentials per user.

Managed Deep Agents builds on that with managed [identity](https://docs.langchain.com/langsmith/python/managed-deep-agents-identity.md) for callers and [connections](https://docs.langchain.com/langsmith/python/managed-deep-agents-connections.md) that run OAuth, so end users authorize their own accounts instead of you storing credentials for each one.

### A production agent server

To expose a [self-hosted Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk/hosting) app to end users, you write your own HTTP/WebSocket or SSE server that invokes the agent, streams tokens back, and manages conversation threads. That server is yours to build, operate, and secure.

Deep Agents deployments include an [agent server](https://docs.langchain.com/langsmith/agent-server.md) out of the box: streaming endpoints, thread management, run history, webhooks, and [authentication](https://docs.langchain.com/langsmith/auth.md).

With Managed Deep Agents, every deployment runs on Agent Server without you operating it. You get the Agent Server API, threads, runs, streaming, and the [MCP endpoint](https://docs.langchain.com/langsmith/python/managed-deep-agents-mcp-endpoint.md). See [Managed Deep Agents overview](../Deployment/Managed%20Deep%20Agents.md).

### Managed cloud or self-hosted

Claude Agent SDK deployments are [self-hosted](https://code.claude.com/docs/en/agent-sdk/hosting). The SDK and [Claude managed agents](https://platform.claude.com/docs/en/managed-agents/overview) are separate products. Code written against the SDK does not deploy directly to the managed offering.

Deep Agents runs in two modes, and your tools, middleware, and subagents carry over unchanged between them:

* **Managed:** create, run, and operate deep agents with [Managed Deep Agents](../Deployment/Managed%20Deep%20Agents.md) in LangSmith. The managed runtime owns the backend, store, and checkpointer. Instructions, skills, and memory live in project files and [Context Hub](https://docs.langchain.com/langsmith/python/managed-deep-agents-context-hub.md). See [Relationship to Deep Agents](../Deployment/Managed%20Deep%20Agents.md#relationship-to-deep-agents).
* **Self-hosted:** run the [Deep Agents SDK](../Deep%20Agents%20overview.md#self-host-with-the-sdk) yourself, or use [`langgraph build`](https://docs.langchain.com/langsmith/cli#build) to produce a [standalone Docker image](https://docs.langchain.com/langsmith/deploy-standalone-server.md) you can deploy anywhere.

If you already built with the SDK and want the managed runtime, see [Move from Deep Agents](https://docs.langchain.com/langsmith/python/managed-deep-agents-migrate.md).

> [!TIP]
>
> For a no-code managed agent platform that works across any model provider, use [LangSmith Fleet](https://docs.langchain.com/langsmith/fleet/index.md). [Claude managed agents](https://platform.claude.com/docs/en/managed-agents/overview) is limited to the Anthropic ecosystem.

### LLM

Claude Agent SDK execution bundles the model, backend, and deployment and optimizes support between all three.

With Deep Agents, you pick the model provider, the execution backend, and the deployment target independently. If you want a more managed approach, Managed Deep Agents keeps that model flexibility while LangSmith owns the runtime. By choosing this harness you retain flexibility in your choice of model and infrastructure.

### Ecosystems

The Claude Agent SDK is purpose-built for Claude and Anthropic's product surface. Deep Agents integrates with the broader LangChain ecosystem, including LangSmith for observability, evaluation, and deployment, and works across any model provider. Managed Deep Agents is the LangSmith-hosted path for that same harness.

## Summary

* **Choose Deep Agents** if you want model and infrastructure flexibility, built-in multi-tenant deployment, and the option to run managed or self-hosted with the same agent code.
* **Choose Claude Agent SDK** if you are already invested in the Anthropic ecosystem and wish to self-host and build the API, auth, and multi-tenant layers yourself.

> [!NOTE]
>
> **Notice a mistake?**
>
> We drafted this comparison on April 16th, 2026. If products have changed, please [file an issue](https://github.com/langchain-ai/docs/issues).

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/deepagents/comparison.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

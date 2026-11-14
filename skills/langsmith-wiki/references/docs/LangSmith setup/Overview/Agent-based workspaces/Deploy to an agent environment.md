# Deploy to an agent environment

> How the LangGraph and Managed Deep Agents CLIs bind a deployment to an agent and an environment, which values each flag takes, and which CLI versions accept them.

Deploying to an agent environment binds a [deployment](../../../Deploy/Get%20started/LangSmith%20Agent%20Server.md) to one [agent](Agent%20Registry.md#agent) and one of that agent's [environments](Agent%20environments.md). Two flags carry the binding, and the LangGraph CLI and the `mda` CLI both accept them.

Use it to keep a staging build and a production build of the same agent apart, so each one reports into its own environment.

> [!NOTE]
>
> Agent-based workspaces are available on [LangSmith Cloud](../../Cloud/Cloud%20%28SaaS%29.md). They are not available on [self-hosted](../../Self-hosted/Self-hosted%20LangSmith.md) LangSmith. To check whether your workspace is agent-based, look at the control at the top left. In an agent-based workspace, it is a workspace switcher that names your workspace. In a [project-based](../../../Monitor/Trace/Observability%20concepts.md#tracing-projects) workspace, it shows the LangSmith logo.

## Prerequisites

Both CLIs need the following:

* A [LangSmith API key](../../Account/Create%20an%20account%20and%20API%20key.md) in `.env` or your shell environment.
* A project folder holding `langgraph.json`. Run the CLI from that folder.
* An agent-based workspace, because the flags require agent mode on the workspace.

An org-scoped API key also needs the workspace, and each CLI reads it from a different variable: `LANGSMITH_TENANT_ID` for the LangGraph CLI, and `LANGSMITH_WORKSPACE_ID` for the `mda` CLI. A workspace-scoped key needs neither. The LangGraph CLI prompts for the value when the key is org-scoped. In a script or CI job, set `LANGSMITH_TENANT_ID` ahead of time, and pass `--no-input` so the LangGraph CLI fails instead of waiting for input. Both the Python and the TypeScript LangGraph CLI accept `--no-input`.

## Addressing flags

Both CLIs take the same two flags:

* **`--agent-id`**: The agent to deploy to. The value is the agent's identifier, not its display name. For which value is which, see [Identifiers and display names](Agent%20Registry.md#identifiers-and-display-names).
* **`--agent-environment`**: The environment the deployment reports into, and one of `development`, `staging`, or `production`. A deployment cannot take `local`. That environment [does not display on deployments](Agent%20environments.md#select-an-environment) at all, which is the one way this set differs from the four values the [agent variables](../../../Monitor/Trace/Configuration%20%26%20troubleshooting/Agent%20%26%20environment%20settings/Log%20traces%20to%20an%20agent.md#using-environment-variables) accept.

The flags name the same pair that agent addressing names on the tracing side. The LangGraph CLI also reads the flags from the same two variables, `LANGSMITH_AGENT_ID` and `LANGSMITH_AGENT_ENVIRONMENT`. The `mda` CLI does not read those variables, so pass the flags to it directly.

## Deploy with the LangGraph CLI

These flags require `langgraph-cli` v0.4.32 or later in Python, and `@langchain/langgraph-cli` 1.5.2-dev.0 in TypeScript. The TypeScript version is a prerelease build. Install it exactly, because the current stable release, 1.5.1, does not accept the flags. To deploy:

1. Install the CLI:

   ```bash Python
   uv tool install --force "langgraph-cli>=0.4.32"
   ```

   ```bash TypeScript
   npm install -g "@langchain/langgraph-cli@1.5.2-dev.0"
   ```

2. Deploy, naming the agent and the environment:

   ```bash Python
   langgraph deploy --agent-id my-agent --agent-environment staging --remote
   ```

   ```bash TypeScript
   langgraphjs deploy --agent-id my-agent --agent-environment staging --remote
   ```

Pass both flags or neither, because the CLI rejects either one on its own. Do not combine them with `--name` or an Agent Server ID flag. The Python CLI uses `--agent-server-id`, with `--deployment-id` accepted as a compatibility alias; older Python versions may require the legacy spelling. The TypeScript prerelease above uses `--deployment-id`. These flag names are separate from the version requirements for agent binding.

`--remote` forces a remote build. Without it, the CLI builds locally whenever Docker is available. For the rest of the flags, see [`langgraph deploy`](../../../Deploy/Get%20started/Reference/LangGraph%20CLI.md#deploy).

## Deploy with the mda CLI

These flags require `managed-deepagents` 0.7.5.dev4 in Python, or 0.7.5-dev.4 in TypeScript. Both are prerelease builds. Install that version exactly, because 0.8.0 and later do not accept the flags and a version range resolves to a build that rejects them. To deploy:

1. Install the CLI:

   ```bash Python
   uv tool install --force --prerelease allow "managed-deepagents==0.7.5.dev4"
   uv add --prerelease allow "managed-deepagents==0.7.5.dev4"
   ```

   ```bash TypeScript
   npm install "managed-deepagents@0.7.5-dev.4"
   ```

2. Deploy the project in the current folder:

   ```bash Python
   mda deploy . --agent-id my-agent --agent-environment staging
   ```

   ```bash TypeScript
   npx mda deploy . --agent-id my-agent --agent-environment staging
   ```

In Python, installing the CLI as a tool and pinning the same version as a project dependency keeps the global `mda` binary and the project's own dependency on one version. For the rest of the flags, see [Deploy projects](../../../Build/Python/Managed%20Deep%20Agents/Build%20and%20deploy/Managed%20Deep%20Agents%20CLI%20reference.md#deploy-projects), and for deploying without the agent flags, see [Deploy a Managed Deep Agent](../../../Build/Python/Managed%20Deep%20Agents/Build%20and%20deploy/Deploy%20a%20Managed%20Deep%20Agent.md).

## Confirm the binding

Open the agent's [Overview](Navigate%20agents.md#read-the-agent-overview), then select **Agent Server** in the header. Check that the Agent Server appears in the intended environment. When active revisions are available, the header also shows revision information by environment.

If the Agent Server is missing from the intended environment, check the agent ID and environment passed to the CLI. The pinned `mda` versions above require explicit `--agent-id` and `--agent-environment` flags; they ignore `LANGSMITH_AGENT_ID` and `LANGSMITH_AGENT_ENVIRONMENT`.

## See also

* [Agent Registry](Agent%20Registry.md)
* [Agent environments](Agent%20environments.md)
* [Log traces to an agent](../../../Monitor/Trace/Configuration%20%26%20troubleshooting/Agent%20%26%20environment%20settings/Log%20traces%20to%20an%20agent.md)
* [Deployment](../../../Deploy/Get%20started/LangSmith%20Agent%20Server.md)

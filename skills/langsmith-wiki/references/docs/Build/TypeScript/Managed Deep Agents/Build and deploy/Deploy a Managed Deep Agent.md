# Deploy a Managed Deep Agent

> Test and deploy a Managed Deep Agent with the mda CLI.

Deploying a Managed Deep Agent compiles a code-first project into a managed LangGraph app, syncs deploy-owned context to [Context Hub](Manage%20Context%20Hub%20for%20Managed%20Deep%20Agents.md), uploads the compiled source, and triggers a LangSmith hosted deployment build. The result is an [Agent Server](../../../../Deploy/Agent%20Server/Agent%20Server.md) deployment, including the Agent Server API and [MCP endpoint](Connect%20MCP%20clients%20to%20a%20Managed%20Deep%20Agent.md).

> [!NOTE]
>
> Managed Deep Agents is in **public [beta](../../../../LangSmith%20setup/Cloud/Reference/Release%20stages.md)** on [LangSmith Cloud](../../../../LangSmith%20setup/Cloud/Cloud%20%28SaaS%29.md) and [Bring Your Own Cloud (BYOC)](../../../../LangSmith%20setup/BYOC/Bring%20Your%20Own%20Cloud%20%28BYOC%29.md). Use Managed Deep Agents CLI and SDK v0.10 or later for BYOC.

This page covers secrets routing and deploy options. To test the agent before deploying, see [Develop locally with LangSmith Studio](Develop%20locally%20with%20LangSmith%20Studio.md). For command flags, the deploy step list, and troubleshooting, see the [CLI reference](Managed%20Deep%20Agents%20CLI%20reference.md). To deploy a finished open-source project instead, see the [design agent](../Templates/Deploy%20the%20open-source%20design%20agent.md) and [paid media agent](../Templates/Deploy%20the%20open-source%20paid%20media%20agent.md) templates.

## Prerequisites

Before you deploy, make sure you have:

* A LangSmith Cloud workspace or a workspace in a [BYOC data plane](../../../../LangSmith%20setup/BYOC/AWS/BYOC%20onboarding.md).

* A [LangSmith API key](../../../../LangSmith%20setup/Account/Create%20an%20account%20and%20API%20key.md) for that workspace, in `.env` or your shell environment. On an interactive terminal, `mda deploy` prompts for a key or signs you in through the browser instead.

* The `mda` CLI installed from `managed-deepagents`.

* Project dependencies installed with `npm install` for TypeScript projects.

* Model provider credentials, such as `OPENAI_API_KEY`, in `.env`, your shell environment, or LangSmith workspace secrets.

## Select a SaaS region

`LANGSMITH_ENDPOINT` selects the LangSmith region the CLI deploys to. The CLI targets GCP US by default.

Set `LANGSMITH_ENDPOINT` in your project's `.env` or your shell environment before your first deploy:

| Region | Endpoint | Deployment support |
| - | - | - |
| GCP US (`smith.langchain.com`) | `https://api.smith.langchain.com` | Supported |
| GCP EU (`eu.smith.langchain.com`) | `https://eu.api.smith.langchain.com` | Supported |
| GCP APAC (`apac.smith.langchain.com`) | `https://apac.api.smith.langchain.com` | Supported |
| AWS US (`aws.smith.langchain.com`) | `https://aws.api.smith.langchain.com` | Supported |
| Azure US (`azure.smith.langchain.com`) | `https://azure.api.smith.langchain.com` | Supported |

For example, to deploy to GCP EU:

```text .env
LANGSMITH_ENDPOINT=https://eu.api.smith.langchain.com
```

Credentials must belong to the target region. Set `LANGSMITH_ENDPOINT` before the first deploy, because it also selects the region that browser sign-in authenticates against. A non-interactive run cannot fall back to browser sign-in, so in CI set `LANGSMITH_API_KEY` for the target region.

For more information on regions, see the [Regions FAQ](../../../../LangSmith%20setup/Govern/Additional%20resources/FAQ/Regions%20FAQ.md).

> [!NOTE]
>
> LangSmith managed tools are available in GCP US only.

## Select a BYOC data plane

For BYOC, use Managed Deep Agents CLI and SDK v0.10 or later. Set `LANGSMITH_ENDPOINT` to your data plane's API URL, not a SaaS regional endpoint. Find the endpoint in **Settings > Data Planes**. See [BYOC usage](../../../../LangSmith%20setup/BYOC/BYOC%20usage.md).

Set `LANGSMITH_API_KEY` to a key for a workspace inside that data plane. Set `LANGSMITH_WORKSPACE_ID` to the target workspace ID, or pass `--workspace-id` to `mda deploy`. Configure these values in your project's `.env` or shell environment before deploying.

The CLI derives the Deployment API URL from the data plane endpoint. Do not append `/api-host` to `LANGSMITH_ENDPOINT`.

BYOC data planes do not support Serverless Agent Servers. Run `mda deploy --push-to <image-repository>` to build and push your agent image. The CLI creates a Dedicated Agent Server by default, so you do not need to pass `--agent-server-type dedicated`.

## Deploy to LangSmith

Deploy the local project:

```bash npm
npx mda deploy
```

```bash pnpm
pnpm exec mda deploy
```

```bash bun
bunx mda deploy
```

> [!TIP]
>
> `mda deploy` routes local project inputs to different managed surfaces:
>
> ```text theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> instructions.md + skills/**  -> Context Hub deploy-owned context
> .env                         -> deploy auth + non-reserved hosted secrets, not archived
> project source files         -> .mda/build source archive -> hosted deployment
> schedules/**                 -> LangSmith cron jobs after the deployment is live
> ```

Set the deployment name explicitly when the directory name is not the name you want:

```bash npm
npx mda deploy --name research-assistant
```

```bash pnpm
pnpm exec mda deploy --name research-assistant
```

```bash bun
bunx mda deploy --name research-assistant
```

`mda deploy` creates a Serverless Agent Server by default. Use `--agent-server-type dedicated` when creating a Dedicated Agent Server. The legacy `--deployment-type` spelling remains accepted. If your CLI does not recognize the Agent Server flag, use the legacy spelling or upgrade.

Serverless is available in every LangSmith Cloud region. Self-hosted and hybrid environments reject Serverless deployments. Use `dedicated` for always-on capacity.

```bash npm
npx mda deploy --agent-server-type dedicated
```

```bash pnpm
pnpm exec mda deploy --agent-server-type dedicated
```

```bash bun
bunx mda deploy --agent-server-type dedicated
```

Use `--no-wait` to trigger the build without polling for completion:

```bash npm
npx mda deploy --no-wait
```

```bash pnpm
pnpm exec mda deploy --no-wait
```

```bash bun
bunx mda deploy --no-wait
```

When `--no-wait` is set, schedule reconciliation is skipped for that deploy invocation because the CLI exits before the deployment reaches `DEPLOYED`.

On success, the CLI prints the LangSmith deployment dashboard URL. For the full deploy step list, see the [CLI reference](Managed%20Deep%20Agents%20CLI%20reference.md#deploy-projects).

## Secrets and environment files

`mda deploy` reads project `.env` values before shell environment variables. Use `.env` for the LangSmith API key that authenticates the deploy and for runtime secrets the hosted deployment needs:

```text .env
LANGSMITH_API_KEY=<LANGSMITH_API_KEY>
OPENAI_API_KEY=<OPENAI_API_KEY>
GITHUB_MCP_TOKEN=<GITHUB_MCP_TOKEN>
DATABASE_URL=<DATABASE_URL>
MDA_INGRESS_SECRET=<MDA_INGRESS_SECRET>
```

`MDA_INGRESS_SECRET` is required only when the project declares [backend identity](../Agent%20capabilities/Add%20identity%20to%20Managed%20Deep%20Agents.md#configure-identity-with-your-own-backend). Deploy fails preflight when that declaration is present and the value is missing.

`LANGSMITH_API_KEY`, `LANGGRAPH_HOST_API_KEY`, `LANGCHAIN_API_KEY`, and other platform variables are reserved. They can authenticate the deploy, but they are not uploaded as user-managed deployment secrets.

Non-reserved `.env` entries, such as model provider keys, MCP tokens, and custom tool credentials, are forwarded as hosted deployment secrets when `mda deploy` creates or updates the deployment. If the configured model requires a provider key, deploy fails before upload unless that key is available from `.env`, the shell environment, or LangSmith workspace secrets. When the provider key is only in the shell environment, `mda deploy` forwards it as a secret for that deploy.

Reserved platform variables, empty values, `.env`, and `.env.*` files are not copied into the compiled build archive.

For authentication key order and reserved variables, see the [CLI reference](Managed%20Deep%20Agents%20CLI%20reference.md#authentication).

## Troubleshoot a deploy

For deploy troubleshooting, see the [CLI reference](Managed%20Deep%20Agents%20CLI%20reference.md#troubleshooting).

If a deployment reaches `BUILD_FAILED` or `DEPLOY_FAILED`, open the printed deployment URL in LangSmith and inspect the revision logs.

## Next steps

> [card] [Agent Server](../../../../Deploy/Agent%20Server/Agent%20Server.md)
>
> Explore the runtime that hosts the deployment.

> [card] [MCP endpoint](Connect%20MCP%20clients%20to%20a%20Managed%20Deep%20Agent.md)
>
> Expose the deployed agent as a tool to MCP clients.

> [card] [Identity](../Agent%20capabilities/Add%20identity%20to%20Managed%20Deep%20Agents.md)
>
> Authenticate callers and provide private threads.

> [card] [Schedules](../Agent%20capabilities/Add%20schedules%20to%20Managed%20Deep%20Agents.md)
>
> Run agents on managed cron schedules.

> [card] [Custom tools](../Agent%20capabilities/Add%20custom%20tools%20to%20Managed%20Deep%20Agents.md)
>
> Add authored LangChain tools to the agent definition.

> [card] [CLI reference](Managed%20Deep%20Agents%20CLI%20reference.md)
>
> Look up every `mda` command and flag.

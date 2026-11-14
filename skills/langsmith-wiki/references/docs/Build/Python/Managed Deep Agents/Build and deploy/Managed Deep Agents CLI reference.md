# Managed Deep Agents CLI reference

> Reference for mda commands, project files, and deploy behavior.

The `mda` CLI compiles and deploys code-first [Managed Deep Agents](../../Deep%20Agents/Deployment/Managed%20Deep%20Agents.md).

It is included with the `managed-deepagents` Python package.

> [!NOTE]
>
> Managed Deep Agents is in **public [beta](../../../../LangSmith%20setup/Cloud/Reference/Release%20stages.md)** on [LangSmith Cloud](../../../../LangSmith%20setup/Cloud/Cloud%20%28SaaS%29.md) and [Bring Your Own Cloud (BYOC)](../../../../LangSmith%20setup/BYOC/Bring%20Your%20Own%20Cloud%20%28BYOC%29.md). Use Managed Deep Agents CLI and SDK v0.10 or later for BYOC.

For the fastest end-to-end path, see the [quickstart](../Get%20started/Managed%20Deep%20Agents%20quickstart.md). For workflow guidance, see [Identity](../Agent%20capabilities/Add%20identity%20to%20Managed%20Deep%20Agents.md), [Memory](../Agent%20capabilities/Add%20memory%20to%20Managed%20Deep%20Agents.md), [Evals](../Agent%20capabilities/Evaluate%20Managed%20Deep%20Agents.md), [Custom tools](../Agent%20capabilities/Add%20custom%20tools%20to%20Managed%20Deep%20Agents.md), [Connections](../Agent%20capabilities/Manage%20connections.md), [Custom middleware](../Agent%20capabilities/Add%20custom%20middleware%20to%20Managed%20Deep%20Agents.md), [Sandboxes](../Agent%20capabilities/Add%20a%20sandbox%20to%20Managed%20Deep%20Agents.md), [Channels](../Agent%20capabilities/Channels/Connect%20Managed%20Deep%20Agents%20to%20channels.md), [Schedules](../Agent%20capabilities/Add%20schedules%20to%20Managed%20Deep%20Agents.md), and [Deploy an agent](Deploy%20a%20Managed%20Deep%20Agent.md).

## Install

`mda init` declares `managed-deepagents` as a project dependency, so run the `mda` binary from the project.

```bash uv
uvx --from managed-deepagents mda init my-agent
cd my-agent
uv sync
uv run mda --version
```

The package provides agent, identity, schedule, and sandbox authoring APIs with snake-case names, plus the `mda` console script.

## Authentication

`mda deploy` reads API keys in this order:

1. `LANGGRAPH_HOST_API_KEY`
2. `LANGSMITH_API_KEY`
3. `LANGCHAIN_API_KEY`

The CLI reads those values from the project `.env` file first, then from the process environment. If no key is found in an interactive terminal, `mda deploy` prompts for a LangSmith API key and saves it to the project `.env` file.

```text .env
LANGSMITH_API_KEY=<LANGSMITH_API_KEY>
OPENAI_API_KEY=<OPENAI_API_KEY>
```

To deploy with an organization-scoped key, set `LANGSMITH_WORKSPACE_ID` or pass `--workspace-id` to `mda deploy`.

The LangSmith API key authenticates the deploy. The agent's model provider also needs credentials at runtime. Set the provider key in `.env`, export it in your shell, or configure it as a LangSmith workspace secret. For example, `openai:gpt-6.1-sol` requires `OPENAI_API_KEY`.

`mda deploy` forwards non-reserved `.env` entries, such as `OPENAI_API_KEY`, MCP tokens, and custom tool credentials, as hosted deployment secrets. Reserved platform variables, including `LANGSMITH_API_KEY`, `LANGGRAPH_HOST_API_KEY`, `LANGCHAIN_API_KEY`, and `LANGSMITH_WORKSPACE_ID`, are used for CLI authentication and deploy routing but are not uploaded as user-managed deployment secrets.

## Command overview

| Command | Use |
| - | - |
| `mda --help` | Show CLI help. |
| `mda --version` | Show the installed CLI version. |
| `mda init <name>` | Scaffold a Python Managed Deep Agents project. |
| `mda build [path]` | Compile a project into a managed LangGraph app without deploying. |
| `mda evals …` | Initialize a Harbor workspace and continue eval authoring in a coding agent. |
| `mda dev [path]` | Compile a project and run it on the local LangGraph dev server. |
| `mda chat [path]` | Chat with the agent from the terminal through a local dev server. |
| `mda connections …` | Manage authentication for tools and MCP connectors. |
| `mda deploy [path]` | Compile, sync Context Hub context, upload, and deploy to LangSmith. |
| `mda pull [path]` | Pull instructions and skills from Context Hub into a local project. |
| `mda channels init slack` | Add a Slack channel declaration to the current project. |
| `mda channels setup [channel]` | Set up the project's channels for a deployed agent without deploying. |
| `mda logs [path]` | Tail Agent Server logs for a deployed agent. |
| `mda delete [path]` / `mda destroy [path]` | Delete a deployed agent and the LangSmith resources it created. |

## Initialize projects

Use `mda init` to create a new project directory:

```bash
uvx --from managed-deepagents mda init my-agent
```

| Argument or flag | Use |
| - | - |
| `name` | Required project directory name. The command fails if the destination already exists. |
| `--instructions TEXT` | System prompt to write into `instructions.md`. |
| `--instructions-file PATH` | Read the system prompt for `instructions.md` from a file, or from stdin when set to `-`. |
| `--identity` | Add managed authentication with user-owned threads. |
| `--memory agent\|none` | Optionally write a root memory declaration. If omitted, no memory file is created and durable memory is off. |
| `--model SPEC` | Model the agent runs on, as `provider:model`. |
| `--no-sandbox` | Leave out the managed sandbox declaration. |
| `--channel slack` | Initialize the agent with a Slack channel declaration. Repeatable; `--channels` is an alias. |

To include Slack in a new project:

```bash
uvx --from managed-deepagents mda init my-agent --channel slack
```

The scaffold language comes from the package you run, not from the current directory: the PyPI package always writes a Python project. A CLI installed from PyPI refuses a TypeScript project.

The scaffold creates:

| File | Description |
| - | - |
| `agent.py` | Named `agent` export from `define_deep_agent(...)`. |
| `instructions.md` | Managed system prompt. |
| `pyproject.toml` | Minimal language-specific manifest. |
| `README.md` | Local project instructions. |
| `.env` | Deploy auth and runtime secrets. Do not commit real secrets. |
| `.gitignore` | Ignores `.env`, `.env.*`, `.mda/`, and dependency caches. |

Eval tasks are opt-in and are not created by `mda init`. Run `mda evals init -i` from the project root to initialize the Harbor workspace and continue in a coding agent with the `eval-engineering` skill.

## Initialize a Slack channel

Run the following command from the root of an existing managed deep agent project:

```bash
uv run mda channels init slack
```

The command creates a Slack channel declaration in the `channels/` directory. The next `mda deploy` sets up the resources the agent needs to appear in Slack. For the complete workflow, see [Connect a Managed Deep Agent to Slack](../Agent%20capabilities/Channels/Connect%20a%20Managed%20Deep%20Agent%20to%20Slack.md).

## Build projects

Use `mda build` to compile a project into a managed LangGraph app without deploying it:

```bash
uv run mda build
```

| Argument or flag | Use |
| - | - |
| `path` | Project directory. Defaults to the current directory. |
| `--out OUT` | Output directory for the compiled app. Defaults to `<path>/.mda/build`. The directory is emptied before the build, so it must be missing, empty, or a directory a previous build wrote. |

## Evaluate projects

Use `mda evals init` to initialize a Harbor workspace. Use the interactive handoff to develop complete tasks with a coding agent and the `eval-engineering` skill.

```bash
uv run mda evals init -i
```

| Command or flag | Use |
| - | - |
| `mda evals init` | Create `evals/harbor-job.json` when missing and generate the Harbor adapter and runtime settings under `.mda/evals/`. Run this command from the project root. |
| `-i`, `--interactive` | Start a detected coding agent with the eval-engineering prompt, or copy the prompt for another agent. |

The handoff asks the coding agent to install the `eval-engineering` skill, inspect the managed agent, and write complete Harbor tasks under `evals/<task>/`. It also includes the pinned Harbor command that loads the MDA job plugin and LangSmith plugin.

`mda evals compile` is an internal command used by the Harbor job plugin. The plugin runs it when a Harbor job starts, so you do not compile eval artifacts separately.

For workflow guidance, see [Evals](../Agent%20capabilities/Evaluate%20Managed%20Deep%20Agents.md).

## Develop locally

Use `mda dev` to compile a project and run the local LangGraph dev server:

```bash
uv run mda dev
```

| Argument or flag | Use |
| - | - |
| `path` | Project directory. Defaults to the current directory. |
| `--port PORT` | Forward a port to the LangGraph dev server. |
| `--hostname HOSTNAME` | Forward a host to the LangGraph dev server. |
| `--no-browser` | Prevent the dev server from opening Studio in a browser when it starts. |
| `--no-reload` | Disable the dev server's hot reload. |
| `--no-schedules` | Do not create the project's schedules on the local server. |

`mda dev` compiles into `.mda/build`, then starts the language-specific LangGraph dev server from that directory:

| Project language | Dev server command |
| - | - |
| Python | `uv run --with langgraph-cli[inmem]>=0.4.36 langgraph dev` |

Install `uv` before running `mda dev`. The CLI resolves the local LangGraph dev server automatically, so you do not need to install `langgraph-cli[inmem]` yourself.

When a sandbox is configured, `mda dev` tries the configured provider. If provider credentials are unavailable or provider creation fails, it falls back to a local temp-directory sandbox and prints the chosen path.

For local development, `mda dev` stages the project `.env` file into `.mda/build/.env` so LangGraph can load model provider keys and other runtime credentials.

## Chat from the terminal

Use `mda chat` to talk to the agent from the terminal. It reuses a local dev server that is already running, or starts one for the session:

```bash
uv run mda chat
```

| Argument or flag | Use |
| - | - |
| `path` | Project directory. Defaults to the current directory. |
| `--url URL` | Agent Server URL to use instead of the local one. Must be a local dev server or a tunnel to one, because `mda chat` sends no credentials. |
| `--assistant ID` | Assistant ID. Defaults to the one `mda dev` staged, then the agent `name`. |
| `-t`, `--thread ID` | Continue an existing thread. |
| `--env-file PATH` | Read environment variables from this file instead of the project `.env` when `mda chat` starts a dev server. Requires `mda` 0.10.0 or later. |

## Manage connections

A connection links a managed deep agent to an external service. The credential lives in the LangSmith workspace, so it rotates without a redeploy, and a user-owned connection resolves the credential of whoever called the agent. Tools and MCP connectors resolve connections at runtime with `connections.get(...)`.

Create connections in one of three modes: opaque secret (fixed API key), general OAuth (BYOT app from the catalog or custom endpoints), or MCP OAuth (discover and register from an MCP server URL). Use `mda connections` to manage these credentials in the current workspace.

| Command | Use |
| - | - |
| `mda connections catalog` | List services with preconfigured OAuth settings. |
| `mda connections create <slug>` | Create an opaque secret, general OAuth, or MCP OAuth connection. |
| `mda connections list` | List connection metadata for the workspace. |
| `mda connections get <slug>` | Show metadata for one connection. |
| `mda connections delete <slug>` | Delete a connection and its stored material. |

The first argument to `mda connections create` is a slug, which is your name for the connection and the name code passes to `connections.get(...)`. Provider names go to `--oauth`.

The OAuth catalog saves you from looking up a provider's OAuth settings. When you pass a listed service to `--oauth`, the CLI supplies its authorization URL, token URL, token endpoint authentication method, authorization parameters, and default scopes, so you provide only your client ID and client secret. The catalog does not limit which providers you can use: for anything else, pass `--authorize-url` and `--token-url`. Catalog names include `github`, `google`, `linear`, `slack`, `atlassian`, and `notion-api`:

```bash
uv run mda connections catalog
```

Create an agent-owned API key for a custom Tavily tool:

```bash
uv run mda connections create organization-tavily --secret-from-env TAVILY_API_KEY
```

The following flags control connection creation:

| Flag | Use |
| - | - |
| `--project PATH` | Set the project directory. Defaults to the current directory. |
| `--workspace-id WORKSPACE_ID` | Override `LANGSMITH_WORKSPACE_ID`. |
| `--agent-server-id AGENT_SERVER_ID` | Set the Agent Server ID for agent-owned secrets or OAuth grants without a local project. |
| `--secret-from-env VAR` | Read a fixed value or OAuth client secret from the shell or project `.env`. |
| `--secret-from-file PATH` | Read a fixed value or OAuth client secret from a file. |
| `--oauth SERVICE` | Use the preconfigured settings for a service in `mda connections catalog`. |
| `--grant-type GRANT` | Set the OAuth grant to `authorization_code` or `client_credentials`. Defaults to `authorization_code`. |
| `--client-id CLIENT_ID` | Set the OAuth client ID. |
| `--auth-method METHOD` | Set the token endpoint method to `client_secret_basic`, `client_secret_post`, or `none`. |
| `--scope SCOPE` | Replace the provider's default scopes. Repeat for each scope. |
| `--allowed-scope SCOPE` | Set the maximum scope that an authorization flow can request. Repeat for each scope. |
| `--authorization-param KEY=VALUE` | Add an OAuth authorization query parameter. Repeat for each parameter. |
| `--token-param KEY=VALUE` | Add a parameter to the OAuth token request. Repeat for each parameter. |
| `--authorize-url URL` | Set a custom OAuth authorization endpoint. Requires `--token-url`. |
| `--token-url URL` | Set a custom OAuth token endpoint. Requires `--authorize-url` for the `authorization_code` grant. |
| `--mcp URL` | Create an MCP OAuth connection by discovering OAuth from the MCP server URL. |
| `--authorize` | Sign in to the account the deployed agent uses, storing an agent-owned OAuth grant. Requires OAuth flags and either a project directory or `--agent-server-id`. |

`--deployment-id` remains a hidden compatibility alias for `--agent-server-id`. Older CLI versions may require the legacy spelling. Check `mda connections create --help` for supported flags.

With no value flags and no `--oauth` endpoints, `mda connections create <slug>` infers MCP OAuth when that slug matches exactly one user-owned MCP connection in the project.

Use `--json` with `catalog`, `list`, or `get` for machine-readable output. Use `--yes` with `delete` to skip the confirmation prompt.

For credential owners, create modes, caller identity, and runtime examples, see [Manage connections](../Agent%20capabilities/Manage%20connections.md).

## Deploy projects

Use `mda deploy` to compile and deploy a project to LangSmith:

```bash
uv run mda deploy
```

| Argument or flag | Use |
| - | - |
| `path` | Project directory. Defaults to the current directory. |
| `--name NAME` | Agent Server name. Defaults to the agent `name` from `define_deep_agent`. |
| `--agent-server-type serverless\|dedicated` | Agent Server type when creating an Agent Server. Defaults to `serverless`. |
| `--workspace-id WORKSPACE_ID` | Workspace ID to deploy into. Overrides `LANGSMITH_WORKSPACE_ID`. |
| `--context-strategy overwrite\|keep-hub` | Resolve Context Hub conflicts when `instructions.md` or `skills/` changed in Hub since the last sync. Required in non-interactive shells. See [Context Hub](Manage%20Context%20Hub%20for%20Managed%20Deep%20Agents.md#source-of-truth). |
| `--no-wait` | Trigger the remote build and exit without polling for deployment completion. |

The Python and JavaScript packages use the same `mda` CLI. It accepts `--deployment-type` as a hidden compatibility alias for `--agent-server-type`. Older versions may require the legacy spelling. Check `mda deploy --help` for the flags your installed version supports.

Deploy runs these steps:

1. Validate the project directory and load the agent entry file.
2. Resolve the LangSmith API key and optional workspace ID.
3. Collect non-reserved `.env` values as hosted deployment secrets.
4. Verify the model provider API key is available from `.env`, the shell environment, or LangSmith workspace secrets.
5. Sync deploy-owned context to Context Hub.
6. Compile the project into `.mda/build` and extract optional `schedules/` and `channels/` declarations.
7. Create or find a LangSmith hosted deployment by name.
8. Archive the build, upload it, and trigger a remote build.
9. Poll the revision until it reaches `DEPLOYED` unless `--no-wait` is set.
10. Reconcile the managed LangSmith cron jobs for schedules unless `--no-wait` is set.
11. Provision the declared Slack channel. If Slack authorization or workspace approval is required, display the action and continue after you complete it.

A project with a Slack channel cannot use `--no-wait` because Slack provisioning requires the deployed Agent Server URL. For the complete workflow, see [Connect a Managed Deep Agent to Slack](../Agent%20capabilities/Channels/Connect%20a%20Managed%20Deep%20Agent%20to%20Slack.md).

On success, the CLI prints the LangSmith deployment dashboard URL. For secrets routing and deploy tips, see [Deploy an agent](Deploy%20a%20Managed%20Deep%20Agent.md).

## Pull context from LangSmith

Use `mda pull` to copy `instructions.md` and `skills/` from the deployed agent's [Context Hub](Manage%20Context%20Hub%20for%20Managed%20Deep%20Agents.md) entry into a local project. Use it after someone edits the agent's instructions or skills in LangSmith and you want those changes in your local project.

> [!NOTE]
>
> `mda pull` requires `mda` 0.10.2 or later.

```bash
uv run mda pull --dry-run
```

`mda pull` lists each file it adds, overwrites, or deletes, then asks before it changes files. It does not change agent code or memories, and it makes no remote writes.

| Argument or flag | Use |
| - | - |
| `path` | Project directory. Defaults to the current directory. |
| `-n`, `--name NAME` | Deployment name. Defaults to the agent `name`. |
| `--dry-run` | Show the changes without changing files. |
| `-y`, `--yes` | Apply the changes without asking. Required without a terminal. |
| `--workspace-id ID` | Workspace to read from. Overrides `LANGSMITH_WORKSPACE_ID`. |
| `--agent-environment ENV` | Agent environment to read from. Defaults to `LANGSMITH_AGENT_ENVIRONMENT` in `.env`. |
| `--env-file PATH` | Read credentials from this file instead of the project `.env`. |

## Set up channels without deploying

Use `mda channels setup` to add a channel to an agent that is already deployed. It runs the same channel setup as `mda deploy`, without deploying.

To check channel status without changing anything, add `--json`. The command exits with a non-zero code if a channel is not set up, so you can use it as a check in CI.

> [!NOTE]
>
> `mda channels setup` requires `mda` 0.10.1 or later and is experimental.

```bash
uv run mda channels setup
```

In a terminal, the command asks which channels to set up. Without a terminal, or with `--json`, it only reports the state of each channel. It exits non-zero unless every channel is set up.

| Argument or flag | Use |
| - | - |
| `channel` | Channel to set up, such as `slack`. Defaults to every channel in the project. |
| `-n`, `--name NAME` | Deployment name. Defaults to the agent `name`. |
| `--json` | Print the state of each channel as JSON. Does not set anything up. |
| `--workspace-id ID` | Workspace of the deployment. Overrides `LANGSMITH_WORKSPACE_ID`. |
| `--agent-environment ENV` | Agent environment to target. Defaults to `LANGSMITH_AGENT_ENVIRONMENT` in `.env`. |
| `--env-file PATH` | Read environment variables from this file instead of the project `.env`. |

`mda deploy` also sets up the channels of an existing deployment before it uploads the new revision. A channel that cannot be set up stops the deploy before the upload.

## Read deployment logs

Use `mda logs` to tail Agent Server logs for a deployed agent:

```bash
uv run mda logs
```

| Argument or flag | Use |
| - | - |
| `path` | Project directory. Defaults to the current directory. |
| `--name NAME` | Agent Server name. Defaults to the agent `name` from the project. |
| `--lines LINES` | Number of recent log lines to fetch. Defaults to `1000`. |
| `--level LEVEL` | Only show entries at or above the given severity: `debug`, `info`, `warning`, `error`, or `critical`. |
| `--follow` | Keep streaming new logs. This is the default in an interactive terminal. |
| `--no-follow` | Print recent logs and exit. This is the default when output is piped. |
| `--workspace-id WORKSPACE_ID` | Workspace ID to read from. Overrides `LANGSMITH_WORKSPACE_ID`. |

## Delete deployments

Use `mda delete` to delete a deployed Managed Deep Agent and the LangSmith resources it created. `mda destroy` is an alias.

```bash
uv run mda delete
```

| Argument or flag | Use |
| - | - |
| `path` | Project directory. Defaults to the current directory. |
| `--name NAME` | Agent Server name. Defaults to the agent `name` from `define_deep_agent`. |
| `--workspace-id WORKSPACE_ID` | Workspace ID the deployment lives in. Overrides `LANGSMITH_WORKSPACE_ID`. |
| `--yes` | Delete without asking for confirmation. |

## Troubleshooting

| Symptom | Cause and fix |
| - | - |
| `project root ... is not a directory` | Pass a directory path to `mda dev` or `mda deploy`. |
| `no agent entry file found` | Add `agent.py` at the project root. |
| `mda dev` cannot find `uv` | Install `uv` so `mda dev` can resolve the local LangGraph dev server. |
| `No LangSmith API key found` | Set `LANGSMITH_API_KEY` or add it to the project `.env`. |
| Deploy fails with 401 or 403 | Confirm the API key belongs to a workspace with deployments access. See [Pricing plans](https://docs.langchain.com/langsmith/pricing-plans.md). |
| Deploy reports a missing model provider API key | Add the provider key, such as `OPENAI_API_KEY`, to `.env`, export it in your shell, or configure it as a LangSmith workspace secret. |
| Deploy reports a Context Hub conflict | `instructions.md` or `skills/` changed in Context Hub since the last sync, or the repo changed during sync. In an interactive terminal, answer the overwrite prompt. In a non-interactive shell, re-run with `--context-strategy overwrite` or `--context-strategy keep-hub`. See [Context Hub](Manage%20Context%20Hub%20for%20Managed%20Deep%20Agents.md#source-of-truth). |
| The build exceeds 200 MB | Remove generated artifacts or large files from the project before deploying. |
| Deployment reaches `BUILD_FAILED` or `DEPLOY_FAILED` | Open the printed deployment URL in LangSmith and inspect the revision logs. |

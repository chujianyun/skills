# Move from Deep Agents to Managed Deep Agents

> Convert an agent built with create_deep_agent into a Managed Deep Agents project.

Managed Deep Agents runs the same [Deep Agents](https://docs.langchain.com/oss/python/deepagents/overview.md) harness you already build against, so moving an existing agent is a repackaging job rather than a rewrite. Your tools, middleware, and subagents carry over as they are. The agent entry changes, and the system prompt, skills, and memory move into project files.

> [!NOTE]
>
> Managed Deep Agents is in **public [beta](../../../../LangSmith%20setup/Cloud/Reference/Release%20stages.md)** on [LangSmith Cloud](../../../../LangSmith%20setup/Cloud/Cloud%20%28SaaS%29.md) and [Bring Your Own Cloud (BYOC)](../../../../LangSmith%20setup/BYOC/Bring%20Your%20Own%20Cloud%20%28BYOC%29.md). Use Managed Deep Agents CLI and SDK v0.10 or later for BYOC.

## Decide whether to move

Managed Deep Agents runs the same harness, so the agent itself behaves the same. Tools, middleware, and subagents work as they do today. Moving adds the layer around the agent: Slack and other chat surfaces, OAuth for end users, scheduled runs, a managed sandbox, and durable memory become declarations in a project file rather than services you build and operate.

Move an agent when you want that layer without running it. Stay on Deep Agents when you need to own it.

| | Deep Agents | Managed Deep Agents |
| - | - | - |
| **Hosting** | You run the agent in your own process or container, or deploy it on [LangSmith Agent Server](../../../../Deploy/Get%20started/LangSmith%20Agent%20Server.md). | LangSmith hosts the agent on [Agent Server](../../../../Deploy/Agent%20Server/Agent%20Server.md). `mda deploy` is the whole deployment step. |
| **Filesystem and shell** | Any [backend](https://docs.langchain.com/oss/python/deepagents/backends.md): agent state, local disk, a store, or a [sandbox](https://docs.langchain.com/oss/python/deepagents/sandboxes.md) you provision with a provider. | One managed [sandbox](../Agent%20capabilities/Add%20a%20sandbox%20to%20Managed%20Deep%20Agents.md), declared in a file. LangSmith creates it, snapshots it, and stops it when idle. |
| **Memory across conversations** | You run the storage and wire it up yourself. | One shared [memory](../Agent%20capabilities/Add%20memory%20to%20Managed%20Deep%20Agents.md) tree, enabled by adding a file. |
| **Third-party access for end users** | You provision and store credentials for each user. | [Connections](../Agent%20capabilities/Manage%20connections.md) hold workspace secrets and run OAuth, so end users authorize services themselves. |
| **Chat surfaces** | You write the integration. | [Channels](../Agent%20capabilities/Channels/Connect%20Managed%20Deep%20Agents%20to%20channels.md) connect Slack and other messaging services. |
| **Scheduled runs** | You run the scheduler. | [Schedules](../Agent%20capabilities/Add%20schedules%20to%20Managed%20Deep%20Agents.md) run managed cron jobs. |
| **Code around the agent** | Yours to write, including custom routes and application code. | The agent only. For custom routes or application code, use [LangSmith Agent Server](../../../../Deploy/Get%20started/LangSmith%20Agent%20Server.md). |

The harness is the same either way. Start with [Managed Deep Agents](../../Deep%20Agents/Deployment/Managed%20Deep%20Agents.md) for new agents when you want to run production agents without having to manage infrastructure. Use this guide when you already have a Deep Agents SDK agent and want the managed runtime. For using the same Deep Agents harness and hosting agents yourself or running a custom [Agent Server](../../../../Deploy/Get%20started/LangSmith%20Agent%20Server.md), see [Going to production](https://docs.langchain.com/oss/python/deepagents/going-to-production).

## Understand what changes

[create\_deep\_agent](https://reference.langchain.com/python/deepagents/graph/create_deep_agent) compiles an agent in your process, so it takes the backend, store, and checkpointer as parameters. `define_deep_agent` returns a definition instead, and the managed runtime compiles it. The definition is configuration rather than a runnable agent: the `mda` CLI consumes it on `mda dev` and `mda deploy`, and the runtime supplies the managed pieces at that point. For the full picture, see [Relationship to Deep Agents](../../Deep%20Agents/Deployment/Managed%20Deep%20Agents.md#relationship-to-deep-agents).

## Check what does not carry over

Most agents move without changes beyond the entry file. Four cases need a decision first:

* **Custom backends**: Managed Deep Agents supplies the agent's default backend. This is thread-scoped agent state, or a [managed sandbox](../Agent%20capabilities/Add%20a%20sandbox%20to%20Managed%20Deep%20Agents.md) when the project declares one. You cannot replace the default backend. To keep your own backend, mount it at a path prefix, such as `/documents/`, with [`routes`](../Agent%20capabilities/Define%20a%20Managed%20Deep%20Agent.md#mount-your-own-backends). Routes require 0.10.3 or later.
* **Your own store or checkpointer**: Threads, runs, and persistence come from [Agent Server](../../../../Deploy/Agent%20Server/Agent%20Server.md). An agent that depends on a specific store implementation needs that logic moved into a tool or middleware.
* **Custom application code and routes**: Managed Deep Agents hosts the agent, not an arbitrary web application. For custom routes, advanced authentication, or application code around the agent, use [LangSmith Agent Server](../../../../Deploy/Get%20started/LangSmith%20Agent%20Server.md) instead.
* **Custom state schemas in Python**: `define_deep_agent` does not accept `state_schema`, so an agent that extends `DeepAgentState` cannot move as is. The TypeScript `defineDeepAgent` does accept `stateSchema`.

If none of these apply, the agent logic transfers as written.

Convert a Deep Agents project into a Managed Deep Agents project.

Convert this codebase from a self-hosted Deep Agents agent into a Managed Deep Agents (MDA) project.

## Step 1: Read the guide

Fetch and follow [https://docs.langchain.com/langsmith/python/managed-deep-agents-migrate.md](Move%20from%20Deep%20Agents%20to%20Managed%20Deep%20Agents.md) as the source of truth for the parameter mapping and project layout.

## Step 2: Add the SDK

Convert the project in place; do not run `mda init`, which only creates a new directory. Add `managed-deepagents` to the existing project manifest, pinned to the version `mda --version` reports, and leave every existing dependency alone.

In Python, if the manifest sets `build-backend = "hatchling.build"`, also add `[tool.hatch.metadata] allow-direct-references = true`. `mda build` rewrites the requirement into a path reference that Hatchling otherwise rejects at install time.

## Step 3: Move the configuration

Find the `create_deep_agent` (or `createDeepAgent`) call site, then:

* Replace it with `define_deep_agent` (or `defineDeepAgent`) in `agent.py` (or `agent.ts`) at the project root, exporting a variable named `agent`. The definition call must live in that file, not be re-exported into it.
* Add a static `name`, which is required. Use a string matching `[a-zA-Z][a-zA-Z0-9_-]*`.
* Move the `system_prompt` text into `instructions.md` next to the agent entry, and remove the parameter.
* Move the files referenced by `skills` into `skills/<name>/SKILL.md`, and remove the parameter.
* Replace `memory` with a root `memory.py` (or `memory.ts`) exporting a variable named `memory` set to `define_memory(scope="agent")`, and remove the parameter. Leave the file out if the agent needs no durable memory. Warn the user that this mounts an empty tree and any existing memory content must be moved into `instructions.md` or a skill.
* Delete `backend`, `store`, and `checkpointer`. The runtime owns all three. If the agent used a sandbox backend, add a `sandbox/` declaration exporting `define_sandbox(...)` instead. If the agent sent paths to other backends through `CompositeBackend` routes, move those routes to `routes` on `define_deep_agent`.
* Keep `model`, `tools`, `middleware`, `subagents`, `permissions`, `cache`, and `debug` as they are, along with the interrupt, response-format, and context-schema parameters under their existing names. Warn the user that a project declaring `sandbox/` runs with `permissions` cleared, because a filesystem permission rule disables the sandbox `execute` tool.
* Leave tool and middleware modules where they already live and keep importing them from the agent entry. Do not restructure the project.

## Step 4: Handle gaps explicitly

If the codebase passes `state_schema` in Python, needs a custom backend for every path rather than under a prefix, or wraps the agent in its own server routes or application code, stop and ask the user how to proceed. Managed Deep Agents does not accept these. Do not invent replacements.

## Step 5: Verify

Run `mda build`, then `mda dev`, and confirm the agent starts and answers a test message. `mda build` does not validate the definition call, so a leftover managed parameter only appears at graph load. Report anything that could not be migrated.

## Map the parameters

Most of the surface transfers to `define_deep_agent` unchanged, under the same names: `model`, `tools`, `middleware`, `subagents`, `interrupt_on`, `response_format`, `context_schema`, `cache`, and `debug`. Leave the tool and middleware modules where they already live and keep importing them from the agent entry.

`define_deep_agent` adds one required parameter. Pass `name` a static string that starts with a letter and contains only letters, numbers, underscores, or hyphens. Managed Deep Agents uses it as the agent's graph ID and the default deployment name.

The rest move to a project file or become the runtime's job:

| `create_deep_agent` | Where it goes | Notes |
| - | - | - |
| `system_prompt` | `instructions.md` | Move the text into the file, then remove the parameter. See [Instructions](../Agent%20capabilities/Add%20instructions%20to%20Managed%20Deep%20Agents.md). |
| `skills` | `skills/` | One directory per skill, each with a `SKILL.md`. See [Skills](../Agent%20capabilities/Add%20skills%20to%20Managed%20Deep%20Agents.md). |
| `memory` | `memory.py` | Export `define_memory(scope="agent")`. Omit the file for no durable memory. See [Memory](../Agent%20capabilities/Add%20memory%20to%20Managed%20Deep%20Agents.md). |
| `backend` | `sandbox/` or `routes` | Declare a managed sandbox for the filesystem and shell. To keep other backends, mount them at path prefixes with `routes`. See [Sandboxes](../Agent%20capabilities/Add%20a%20sandbox%20to%20Managed%20Deep%20Agents.md) and [Mount your own backends](../Agent%20capabilities/Define%20a%20Managed%20Deep%20Agent.md#mount-your-own-backends). |
| `permissions` | Stays a parameter | Accepted, and cleared when the project declares a sandbox. See [Permissions](https://docs.langchain.com/oss/python/deepagents/permissions.md). |
| `store`, `checkpointer` | Managed runtime | Remove both. |
| `state_schema` | No equivalent | `define_deep_agent` does not accept it. |

Deep Agents backends are pluggable, and the managed runtime supplies its own. A project that declares `sandbox/` gets a managed sandbox for the agent filesystem and shell. A project without one gets thread-scoped agent state, alongside read-only [Context Hub](../Build%20and%20deploy/Manage%20Context%20Hub%20for%20Managed%20Deep%20Agents.md) mounts for instructions, skills, and memory. You cannot replace this default backend. To keep a specific backend, mount it at a path prefix with [`routes`](../Agent%20capabilities/Define%20a%20Managed%20Deep%20Agent.md#mount-your-own-backends). An agent that needs its own backend for every path stays on Deep Agents.

## Move an agent

Convert the project in place. The existing layout, module structure, and dependencies stay as they are: `mda build` merges the dependencies it needs into the project manifest rather than replacing it.

To install the `mda` CLI first, see the [quickstart](Managed%20Deep%20Agents%20quickstart.md).

**1. Add the SDK to the project**

```bash
uv add managed-deepagents
```

Pin the version to match the CLI, which `mda --version` reports.

If the project builds with Hatchling, allow direct references in `pyproject.toml`:

```toml pyproject.toml
[tool.hatch.metadata]
allow-direct-references = true
```

`mda build` rewrites the `managed-deepagents` requirement into a path reference to the runtime it stages, and Hatchling rejects that by default. Without the setting, `mda build` still succeeds and `mda dev` fails while installing the project, with `Dependency #N of field project.dependencies cannot be a direct reference`. Projects scaffolded by `mda init` declare no build backend, so the setting only comes up when converting an existing project.

Leave every dependency the project already declares in place. Tools and middleware keep importing what they always did.

**2. Rewrite the agent entry**

Convert the call site using the table above, in a file named `agent.py` at the project root:

```python agent.py (before)
from deepagents import create_deep_agent

from tools.search import internet_search

agent = create_deep_agent(
    model="openai:gpt-5.5",
    tools=[internet_search],
    system_prompt=SYSTEM_PROMPT,
    skills=["/skills/research/"],
    checkpointer=checkpointer,  # yours to construct and wire
)
```

```python agent.py (after)
from managed_deepagents import define_deep_agent

from tools.search import internet_search

agent = define_deep_agent(
    name="research-assistant",
    model="openai:gpt-5.5",
    tools=[internet_search],
)
```

The entry must export a variable named `agent`, and the definition call itself has to live in this file. A root entry that re-exports the definition from another module fails, and the error names `name` rather than the real problem.

A `src/` layout is otherwise fine. Keep the packages where they are and import them from the root entry.

**3. Move the prompt, skills, and memory into files**

Put the system prompt in `instructions.md` at the project root. Give each skill its own directory under `skills/` with a `SKILL.md`.

If the agent needs memory that persists across threads, declare it in a root file exporting a variable named `memory`:

```python memory.py
from managed_deepagents import define_memory

memory = define_memory(scope="agent")
```

Durable memory is opt-in, and a project without the file mounts none. The scope is the only knob: `"agent"` mounts one tree that every caller of the deployment shares. To control what the agent keeps there, write a memory policy into `instructions.md`. See [Guide what to remember](../Agent%20capabilities/Add%20memory%20to%20Managed%20Deep%20Agents.md#guide-what-to-remember).

> [!WARNING]
>
> `define_memory` mounts an empty memory tree. Content from the files the old `memory` parameter pointed at does not transfer, so move anything the agent still needs into `instructions.md` or a skill before deleting those files.

**4. Declare a sandbox**

An agent that passed a sandbox `backend` needs a managed sandbox declaration instead. Create the directory and declare it:

```python sandbox/__init__.py
from managed_deepagents import define_sandbox

sandbox = define_sandbox(
    idle_ttl_seconds=600,
    default_timeout=600,
)
```

> [!WARNING]
>
> Declaring a sandbox clears `permissions`. A filesystem permission rule disables the sandbox `execute` tool, so the runtime drops the rules rather than the shell. Restrict a sandboxed agent through the tools you give it instead.

To provision a snapshot, add `sandbox/setup.sh`. Skip this step for an agent that had no sandbox backend. See [Sandboxes](../Agent%20capabilities/Add%20a%20sandbox%20to%20Managed%20Deep%20Agents.md).

**5. Declare identity**

(Optional) To give each caller private threads and downstream credentials, add a root identity declaration:

```python identity.py
from managed_deepagents import auth, define_identity

identity = define_identity(auth=auth.langsmith_api_key())
```

Without the file the deployment runs with no managed auth, which `mda dev` reports as `Identity none`. See [Identity](../Agent%20capabilities/Add%20identity%20to%20Managed%20Deep%20Agents.md).

**6. Set credentials and ignore the build output**

Put the model and tool API keys in a `.env` file at the project root. A value exported in your shell is not read. For shared workspace secrets and OAuth, use [connections](../Agent%20capabilities/Manage%20connections.md) instead.

Add the build directory to `.gitignore`:

```text .gitignore
.env
.env.*
.mda/
```

`mda build` copies the whole project root into `.mda/build`, and `mda deploy` uploads it. Anything sitting next to the agent entry ships with the agent, so move what the deployment does not need out of the project root.

**7. Compile, then run**

Compile without deploying:

```bash
mda build
```

Then start it locally:

```bash
mda dev
```

> [!NOTE]
>
> `mda build` does not inspect the definition call, so it exits 0 even when a managed parameter is still there. A leftover parameter surfaces when the graph loads under `mda dev`.

See [Local development](../Build%20and%20deploy/Develop%20locally%20with%20LangSmith%20Studio.md).

**8. Deploy**

Upload the project and let LangSmith build and host it:

```bash
mda deploy
```

See [Deploy](../Build%20and%20deploy/Deploy%20a%20Managed%20Deep%20Agent.md).

> [!TIP]
>
> Starting a new agent rather than moving one? Scaffold the whole project, including the identity, sandbox, `.env`, and `.gitignore` files above:
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> mda init research-assistant
> ```
>
> The install channel selects the authoring language: the npm package scaffolds TypeScript, and the PyPI package scaffolds Python. The command creates a new directory and does not run in place, so it suits a greenfield project rather than a migration. See the [quickstart](Managed%20Deep%20Agents%20quickstart.md).

## See also

* [Relationship to Deep Agents](../../Deep%20Agents/Deployment/Managed%20Deep%20Agents.md#relationship-to-deep-agents): why the two entry points differ.
* [Agent definition](../Agent%20capabilities/Define%20a%20Managed%20Deep%20Agent.md): the full parameter reference.
* [Project structure](Managed%20Deep%20Agents%20project%20structure.md): where each file goes.
* [Going to production](https://docs.langchain.com/oss/python/deepagents/going-to-production): deployment options for Deep Agents.

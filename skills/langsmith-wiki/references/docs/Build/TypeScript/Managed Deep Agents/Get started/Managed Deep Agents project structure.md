# Managed Deep Agents project structure

> Understand the project layout for Managed Deep Agents.

A Managed Deep Agents project is a normal TypeScript package with one required root agent entry. Other paths are either ordinary modules you import, or files and directories that MDA discovers to enable managed capabilities.

> [!NOTE]
>
> Managed Deep Agents is in **public [beta](../../../../LangSmith%20setup/Cloud/Reference/Release%20stages.md)** on [LangSmith Cloud](../../../../LangSmith%20setup/Cloud/Cloud%20%28SaaS%29.md) and [Bring Your Own Cloud (BYOC)](../../../../LangSmith%20setup/BYOC/Bring%20Your%20Own%20Cloud%20%28BYOC%29.md). Use Managed Deep Agents CLI and SDK v0.10 or later for BYOC.

## Project layout

```text Project layout
my-agent/
├── agent.ts | agent.tsx            # Core agent definition

├── instructions.md                 # Managed context
├── skills/
│   └── <name>/
│       └── SKILL.md

├── tools/                          # Application code
│   └── mcp.ts                      # MCP server declaration
├── middleware/

├── channels/                       # Managed configuration
│   └── <name>.ts
├── schedules/
│   └── <name>.ts
├── sandbox/
│   └── index.ts
├── identity.ts
├── memory.ts

├── package.json                    # Dependencies
├── .env                            # Local and deploy secrets

└── evals/                          # Harbor workspace
    ├── harbor-job.json
    └── <task>/                     # Harbor task
        ├── Task.md
        ├── instruction.md
        ├── environment/
        └── tests/
```

The only required file is `agent.ts` or `agent.tsx` at the project root containing the [agent definition](../Agent%20capabilities/Define%20a%20Managed%20Deep%20Agent.md) as a named `agent`. It must export a named `agent` created with `defineDeepAgent`. Use only one agent entry in a project.

The layout above shows the common `.ts` names. TypeScript managed declarations also accept the supported `.tsx`, `.mts`, or `.cts` variants.

## How MDA treats project files

* **Managed context**: [`instructions.md`](../Agent%20capabilities/Add%20instructions%20to%20Managed%20Deep%20Agents.md) defines the system prompt. Each directory under [`skills/`](../Agent%20capabilities/Add%20skills%20to%20Managed%20Deep%20Agents.md) contains task-specific instructions, such as a `SKILL.md` and any supporting files. MDA syncs both `instructions.md` and `skills/` to [Context Hub](../Build%20and%20deploy/Manage%20Context%20Hub%20for%20Managed%20Deep%20Agents.md). Optional [durable memory](../Agent%20capabilities/Add%20memory%20to%20Managed%20Deep%20Agents.md) is also backed by Context Hub.

* **Application code**: Files under [`tools/`](../Agent%20capabilities/Add%20custom%20tools%20to%20Managed%20Deep%20Agents.md) and [`middleware/`](../Agent%20capabilities/Add%20custom%20middleware%20to%20Managed%20Deep%20Agents.md) are ordinary project modules. Import them from the agent entry.

* **Managed configuration**: Certain paths enable capabilities when present. For `channels/` and `schedules/`, only direct children are managed declarations; nested modules are not.

  | Path | Enables |
  | - | - |
  | `identity.ts` | [Caller authentication](../Agent%20capabilities/Add%20identity%20to%20Managed%20Deep%20Agents.md) |
  | `memory.ts` | [Durable memory](../Agent%20capabilities/Add%20memory%20to%20Managed%20Deep%20Agents.md) |
  | `channels/<name>.ts` | [Messaging channels](../Agent%20capabilities/Channels/Connect%20Managed%20Deep%20Agents%20to%20channels.md) |
  | `tools/mcp.ts` | [MCP connectors](../Agent%20capabilities/Connect%20to%20MCP%20servers.md) |
  | `schedules/<name>.ts` | [Cron schedules](../Agent%20capabilities/Add%20schedules%20to%20Managed%20Deep%20Agents.md) |
  | `sandbox/index.ts` | [Sandbox filesystem and shell](../Agent%20capabilities/Add%20a%20sandbox%20to%20Managed%20Deep%20Agents.md) |

  `tools/` holds ordinary modules with one exception. `tools/mcp.ts` is a managed declaration and exports a named `mcp`. Every other module under `tools/` is application code you import.

* **Dependencies and secrets**: Declare dependencies in `package.json`. MDA loads `.env` locally and forwards non-reserved values as deployment secrets. Reserved platform variables and `.env` files are not included in the build archive. For more information, see [Deploy a Managed Deep Agent](../Build%20and%20deploy/Deploy%20a%20Managed%20Deep%20Agent.md).

* **Evals**: Managed Deep Agents [evals](../Agent%20capabilities/Evaluate%20Managed%20Deep%20Agents.md) are Harbor evals. Run `mda evals init -i` and develop tasks with a coding agent and the `eval-engineering` skill. Generated runtime files stay under `.mda/evals/` and are not included in the deployed agent build.

## Share code from outside the project

The build copies only the project directory. To use a package from a sibling directory, declare it as a local dependency:

```bash npm
npm install ../shared
```

```bash pnpm
pnpm add ../shared
```

```ts
import { helper } from "@acme/shared";
```

Put the shared code in its own package. Its `package.json` needs a `name` and a `main` or `exports` entry, which can point to `.ts` files:

```json ../shared/package.json
{
  "name": "@acme/shared",
  "main": "./index.ts"
}
```

MDA copies the package into the build. `mda dev` reloads when you edit it, and `mda deploy` ships it.

## Next steps

> [card] [Quickstart](Managed%20Deep%20Agents%20quickstart.md)
>
> Create and deploy your first Managed Deep Agent with the `mda` CLI.

> [card] [Tutorial](../Build%20and%20deploy/Add%20a%20custom%20search%20tool%2C%20memory%2C%20and%20a%20schedule.md)
>
> Add durable memory and a daily schedule to the quickstart research assistant.

> [card] [Design agent template](../Templates/Deploy%20the%20open-source%20design%20agent.md)
>
> A complete project that maps each root file to an MDA capability.

> [card] [Paid media agent template](../Templates/Deploy%20the%20open-source%20paid%20media%20agent.md)
>
> A complete project that maps each root file to an MDA capability.

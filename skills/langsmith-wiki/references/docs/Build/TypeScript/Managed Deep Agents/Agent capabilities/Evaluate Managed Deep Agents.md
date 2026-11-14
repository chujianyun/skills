# Evaluate Managed Deep Agents

> Develop Harbor evals for Managed Deep Agents with a coding agent and the eval-engineering skill.

Managed Deep Agents evals are [Harbor](https://www.harborframework.com/docs/tasks) tasks. Use a coding agent with the [`eval-engineering` skill](https://github.com/langchain-ai/langchain-skills/blob/main/config/skills/eval-engineering/SKILL.md) to inspect the project, draft a Task Spec for your review, and write complete tasks under `evals/`.

Managed Deep Agents initializes the Harbor workspace. Harbor runs the managed agent against each task in an isolated environment and records the result.

> [!NOTE]
>
> Managed Deep Agents is in **public [beta](../../../../LangSmith%20setup/Cloud/Reference/Release%20stages.md)** on [LangSmith Cloud](../../../../LangSmith%20setup/Cloud/Cloud%20%28SaaS%29.md) and [Bring Your Own Cloud (BYOC)](../../../../LangSmith%20setup/BYOC/Bring%20Your%20Own%20Cloud%20%28BYOC%29.md). Use Managed Deep Agents CLI and SDK v0.10 or later for BYOC.

## Prerequisites

Before you evaluate, make sure you have:

* A Managed Deep Agents project created with `mda init`, or an existing project with an agent entry.
* [`uv`](https://docs.astral.sh/uv/), which runs the pinned Harbor version and plugins.
* [Docker](https://docs.docker.com/get-docker/), which Harbor uses for task environments.
* A coding agent. Agents that support Agent Skills can install `eval-engineering` directly. For other agents, provide the skill instructions in the session.

## Add the `eval-engineering` skill

The [`eval-engineering` skill](https://github.com/langchain-ai/langchain-skills/blob/main/config/skills/eval-engineering/SKILL.md) walks a coding agent through discovering the agent, proposing a Task Spec, and building a reviewed Harbor task. To add it to the current project, run:

```bash
npx skills add langchain-ai/langchain-skills --skill eval-engineering --yes
```

You can use any coding agent.

> [!TIP]
>
> To use [Deep Agents Code](https://docs.langchain.com/oss/deepagents/code/overview.md) (`dcode`), install it with:
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl -LsSf https://langch.in/dcode | bash
> ```
>
> See the [Deep Agents Code quickstart](https://docs.langchain.com/oss/deepagents/code/quickstart.md) for provider setup and interactive use.

## Develop evals with a coding agent

**1. Initialize the eval workspace**

From the project root, run:

```bash npm
npx mda evals init -i
```

```bash pnpm
pnpm exec mda evals init -i
```

```bash bun
bunx mda evals init -i
```

The interactive handoff lists detected coding agents, including Deep Agents Code, Claude Code, Codex, and Cursor. Selecting an agent starts that agent in the project directory and runs the eval-engineering prompt. You can also copy the prompt for another agent, or exit and return later.

Initialization creates:

```text
my-agent/
├── evals/
│   └── harbor-job.json
└── .mda/
    └── evals/
        ├── runtime.json
        └── harbor-adapter/
```

`evals/harbor-job.json` is user-owned. Managed Deep Agents writes it only when it is missing, so later edits are preserved. Files under `.mda/evals/` are generated.

**2. Start the coding-agent session**

The handoff asks the selected coding agent to install the `eval-engineering` skill and use it for the project. If you already added the skill, continue in that session.

Ask the coding agent to follow the skill's review flow and use the Managed Deep Agents task layout:

Develop Harbor evals with the eval-engineering skill

Use the eval-engineering skill to develop Harbor evals for this Managed
Deep Agent. Inspect the project and existing evals first. Draft the Task
Spec and wait for my review before implementing the approved task directly
under evals/\<task>/.

Work with the coding agent to review the Task Spec, task instruction, environment, verifier, and reusable project knowledge. The coding agent writes the runnable task after you approve the design.

**3. Review the Harbor task**

Each direct child of `evals/` that contains an instruction and tests is a Harbor task:

```text
evals/
├── harbor-job.json
└── <task>/
    ├── Task.md
    ├── instruction.md
    ├── task.toml
    ├── environment/
    │   └── Dockerfile
    └── tests/
        ├── test.sh
        └── <verifier>
```

`Task.md` is the human-reviewed spec. `instruction.md` tells the agent what to do. Harbor builds the task environment, runs the managed agent, and then runs `tests/test.sh`. The verifier writes a numeric reward to `/logs/verifier/reward.txt` or numeric metrics to `/logs/verifier/reward.json`.

For the full task format, see the [Harbor task documentation](https://www.harborframework.com/docs/tasks).

**4. Run the evals**

The coding-agent handoff includes a command configured for the project and current shell. Run that command from the project root.

On macOS or Linux, it has the following form:

```bash
HARBOR_LANGSMITH_DATASET=mda-my-agent-evals \
PYTHONPATH=.mda/evals/harbor-adapter \
uv run --env-file .env --python 3.12 --with 'harbor[langsmith]==0.21.0' harbor run \
  --config evals/harbor-job.json --yes \
  --plugin mda_harbor.job_plugin:MDAJobPlugin \
  --plugin mda_harbor.langsmith_plugin:LangSmithPlugin
```

Replace `my-agent` with the project directory name. The generated command fills in the name and uses PowerShell syntax on Windows.

Re-running the command after editing the agent picks up the project changes.

**5. Inspect the results**

Open the Harbor results:

```bash
uv run --python 3.12 --with 'harbor[langsmith]==0.21.0' \
  harbor view .mda/evals/jobs
```

Review failed trials with your coding agent. Update the task or verifier when the eval does not measure the intended behavior. Update the managed agent when the eval exposes a product failure, then run the same Harbor command again.

## Edit the Harbor job

Edit `evals/harbor-job.json` to change datasets, attempts, concurrency, environment settings, or agent environment variables. Managed Deep Agents preserves the file when you run `mda evals init` again.

## Record runs in LangSmith

When `LANGSMITH_API_KEY` is available, the LangSmith plugin records the Harbor runs in the dataset named by `HARBOR_LANGSMITH_DATASET`.

## See also

* [CLI reference](../Build%20and%20deploy/Managed%20Deep%20Agents%20CLI%20reference.md): review `mda evals init` and related flags.
* [Deploy an agent](../Build%20and%20deploy/Deploy%20a%20Managed%20Deep%20Agent.md): deploy the agent after its evals pass.
* [Deep Agents Code quickstart](https://docs.langchain.com/oss/deepagents/code/quickstart.md): install and run `dcode`.
* [Harbor integrations](../../../../Test/Evaluators/Frameworks%20%26%20integrations/Harbor%20integrations.md): record Harbor jobs in LangSmith.
* [Harbor task documentation](https://www.harborframework.com/docs/tasks): configure tasks, environments, and verifiers.

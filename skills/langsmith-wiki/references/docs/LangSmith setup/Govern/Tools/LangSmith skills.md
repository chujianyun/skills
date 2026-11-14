# LangSmith skills

> Use Agent Skills to work with LangSmith traces, datasets, and evaluators from your coding agent.

Agent Skills are reusable, on‑demand capabilities that bundle instructions plus optional helper scripts. This page summarizes the LangSmith‑oriented skills you can add to a compatible coding agent to query traces, generate datasets, and define evaluators. To work with the same LangSmith data directly from the terminal, use the [LangSmith CLI](LangSmith%20CLI.md).

> [!NOTE]
>
> These skills follow the Agent Skills specification and are maintained in the [`langsmith-skills` GitHub repository](https://github.com/langchain-ai/langsmith-skills). You can copy the `SKILL.md` and any referenced `scripts/` into your agent’s skills directory. The installers below only install the LangSmith skills (trace, dataset, evaluator).

## Quick install

Install only the LangSmith skills (trace, dataset, evaluator) using `npx skills`:

```bash Local (current project)
npx skills add langchain-ai/langsmith-skills --skill '*' --yes
```

```bash Global (all projects)
npx skills add langchain-ai/langsmith-skills --skill '*' --yes --global
```

```bash Link to a specific agent (e.g., Claude Code)
npx skills add langchain-ai/langsmith-skills --agent claude-code --skill '*' --yes --global
```

> [!TIP]
>
> To update, re‑run the command. If target skill folders already exist, remove them first (e.g., `rm -rf ~/.claude/skills/langsmith-*`).

## Configure environment

These helpers use `LANGSMITH_PROJECT` to select traces. [Retrieve the selected agent environment's `tracer_session_name`](../../Overview/Agent-based%20workspaces/Create%20an%20agent.md#use-an-environment-project) and use that returned value.

After installing the skills, set environment variables used by all LangSmith skills, helper scripts, and the [LangSmith CLI](LangSmith%20CLI.md):

```bash
export LANGSMITH_API_KEY=<your-key>
# Optional defaults
export LANGSMITH_PROJECT="<environment-tracer-session-name>"
# Advanced: multi-workspace or certain self-hosted setups only
# export LANGSMITH_WORKSPACE_ID=<workspace-id>
```

## What these skills cover

* [Traces](../../../Monitor/Trace/Observability%20concepts.md#traces): Add tracing to agents; list, filter, inspect, and export traces for debugging and analysis.
* [Datasets](../../../Test/Get%20started/Evaluation%20concepts.md#datasets): Turn traces into evaluation datasets (final\_response, single\_step, trajectory, RAG) and optionally upload to LangSmith.
* [Evaluators](../../../Test/Get%20started/Evaluation%20concepts.md#evaluators): Define code or LLM‑as‑judge evaluators and attach them to datasets (offline) or agent environments (online).

Each skill directory ships with a `SKILL.md` plus optional `scripts/` helpers you can run or adapt. These skills are designed to plug into compatible coding agents (such as Claude Code or Deep Agents Code), though you can also reuse the helper scripts directly if you prefer not to wire up a full agent. For heavier querying, exports, or automation, you can pair these skills with the [LangSmith CLI](LangSmith%20CLI.md) to script against the same agent environments, datasets, and evaluators from your terminal.

## Manual install

Clone the repo and run the install script for more options:

```bash
git clone https://github.com/langchain-ai/langsmith-skills.git
cd langsmith-skills

# Install for Claude Code in current directory (default)
./install.sh

# Install for Claude Code globally
./install.sh --global

# Install for Deep Agents Code in current directory
./install.sh --deepagents

# Install for Deep Agents Code globally (includes agent persona)
./install.sh --deepagents --global

# Install only LangSmith skills (any target)
./install.sh --langsmith
```

If you prefer to copy only specific skills, copy the desired directory from `config/skills/` into your agent's skills folder.

Included LangSmith skills:

* langsmith-trace — Traces (query/export)
* langsmith-dataset — Datasets (generate/upload)
* langsmith-evaluator — Evaluators (create/attach)

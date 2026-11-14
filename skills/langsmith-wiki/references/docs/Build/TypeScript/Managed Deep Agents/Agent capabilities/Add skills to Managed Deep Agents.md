# Add skills to Managed Deep Agents

> Add reusable task-specific instructions to a managed deep agent.

Skills package task-specific procedures and supporting files into reusable directories. MDA discovers them automatically. The agent loads a skill's full contents only when the task matches the description in the frontmatter.

> [!NOTE]
>
> Managed Deep Agents is in **public [beta](../../../../LangSmith%20setup/Cloud/Reference/Release%20stages.md)** on [LangSmith Cloud](../../../../LangSmith%20setup/Cloud/Cloud%20%28SaaS%29.md) and [Bring Your Own Cloud (BYOC)](../../../../LangSmith%20setup/BYOC/Bring%20Your%20Own%20Cloud%20%28BYOC%29.md). Use Managed Deep Agents CLI and SDK v0.10 or later for BYOC.

Put each skill under `skills/` at the project root:

```text
my-agent/
  agent.ts
  skills/
    research/
      SKILL.md
```

For the full project layout, see [Project structure](../Get%20started/Managed%20Deep%20Agents%20project%20structure.md).

## Add a skill

Use skills for procedures the agent should follow only when a task matches the description in the frontmatter:

**1. Create a skill directory**

Each skill directory needs a `SKILL.md` file with `name` and `description` frontmatter:

```markdown skills/research/SKILL.md
---
name: research
description: Gather and synthesize context before answering complex questions.
---

# Research

Use this skill when a task needs more than a direct answer.

1. Identify what information is missing.
2. Use `query_db` to look up relevant records.
3. Summarize findings before responding to the user.
```

For skill authoring patterns and the complete format, see [Skills](https://docs.langchain.com/oss/javascript/deepagents/skills.md).

To understand progressive disclosure, see [How the agent uses skills](#how-the-agent-uses-skills).

**2. Add supporting files (Optional)**

A skill directory can also contain supporting scripts, reference files, and templates. Reference these files from `SKILL.md` so the agent knows when to use them:

```text
skills/
  research/
    SKILL.md
    templates/
      report.md
    scripts/
      fetch_sources.ts
```

## How the agent uses skills

At startup, the agent sees each skill's `name` and `description`. When a task matches a skill's description, the agent reads the full `SKILL.md` and follows its instructions. Supporting files are loaded only when needed.

The agent cannot modify skills at runtime.

## Deployment

When you run `mda deploy`, MDA syncs every UTF-8 file under `skills/` to the agent's [Context Hub](../Build%20and%20deploy/Manage%20Context%20Hub%20for%20Managed%20Deep%20Agents.md).

You can then edit skills in the LangSmith UI and apply those changes to the agent.

It is best to keep the skill files in the repo as the source of truth for lasting changes, as later deployments sync the project copies again and remove deployed skill files that do not exist locally.

For what syncs, what does not, and how to open the repo from a deployment, see [Context Hub](../Build%20and%20deploy/Manage%20Context%20Hub%20for%20Managed%20Deep%20Agents.md).

## When to use skills

| Concept | Role | Loaded when |
| - | - | - |
| **[Instructions](Add%20instructions%20to%20Managed%20Deep%20Agents.md)** | Always-on system prompt | Every run |
| **Skills** | Task-specific procedures | When the agent selects them |
| **[Memory](Add%20memory%20to%20Managed%20Deep%20Agents.md)** | Knowledge the agent can update | When durable memory is enabled |

For more information, see [Project structure](../Get%20started/Managed%20Deep%20Agents%20project%20structure.md). For complete projects that ship many skills, see the [design agent](../Templates/Deploy%20the%20open-source%20design%20agent.md) and [paid media agent](../Templates/Deploy%20the%20open-source%20paid%20media%20agent.md) templates.

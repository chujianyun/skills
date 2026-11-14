# Skills

> Use skills to give your agents access to specific capabilities.

Skills are reusable capabilities that provide specialized workflows and domain knowledge to your agent. Each skill is stored in the agent's long-term memory at `memories/skills/<skill-name>`. The skill's name and description is loaded when the agent starts. Based on this info the agent can decide to use the skill. The full skill file is only loaded when the agent determines it is relevant to the current task. Any referenced additional resources may be loaded by the agent if they become relevant.

Using skills can help:

* Save on token usage by only providing context relevant to the current task.
* Prevent the agent from having too much context in the system prompt, which can lead to hallucinations and incorrect responses.

> [!NOTE]
>
> Fleet skills are built on [Deep Agents](https://docs.langchain.com/oss/python/deepagents/skills.md) and follow the [Agent Skills specification](https://agentskills.io/specification). For details on skill structure, the `SKILL.md` format, and authoring best practices, see the [Deep Agents skills documentation](https://docs.langchain.com/oss/python/deepagents/skills.md).

## Private vs. shared skills

Skills can be **private** to a single agent or **shared** across a workspace:

* **Private skills**: Private to the agent they belong to and are stored in the agent's long-term memory.
* **Shared skills**: Shared with the workspace and listed on the [**Skills**](https://smith.langchain.com/agents/skills) page.
  * Visible to all agents in the workspace.
  * Only the user who created the skill can edit or delete it.
  * Can be added to any agent in the workspace and stay in sync as skill is updated.
  * Accessed automatically by the general-purpose chat.

## Write effective skill descriptions

Write the description as instructions for when to use the skill, not as a label for what it does. The agent routes tasks based on the description alone. It reads the full skill file only after deciding to use it.

For example, instead of "Helps with email," write: "Use when drafting, replying to, or summarizing emails. Covers tone adjustments, follow-up scheduling, and inbox triage."

A description that is too broad means the agent may not use the skill even when it would handle the task correctly. A description that overlaps with another skill means the agent may route to the wrong one or fail to choose. As your skill library grows, review descriptions for overlap and narrow any that are ambiguous.

## Create a skill

You can create a skill two ways:

* **With AI**: Use natural language to describe the skill and the agent will create it for you. You can also add additional resources. Any additional files must be referenced in `SKILL.md` for the agent to be aware of them.
* **Manually**: Create a skill with a `SKILL.md` file.

> [!NOTE]
>
> By default, skills are **private** to the agent they belong to and are stored in the agent's long-term memory. You can [share a skill with the workspace](#share-a-skill).

> [tab] With AI
>
> In [Fleet](https://smith.langchain.com/agents?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-fleet-skills), select an agent and prompt it to create a skill:
>
> Create a skill that helps the agent use the web to research a topic.
>
> Create a skill that helps the agent use the web to research a topic. Use when asked to research a topic, person, company, technology, event, or any question that requires gathering and synthesizing information from the web. Covers news lookups, competitive analysis, background research, and fact-finding tasks. Prefer `tavily_web_search` for most queries.
>
> You can also turn a previous conversation into a reusable skill at any time. After completing a task, ask the agent to capture the workflow:
>
> Turn this conversation into a reusable skill.
>
> Turn what we just did into a skill so you can repeat it in the future.

> [tab] From a template
>
> 1. Navigate to [**Fleet > Skills**](https://smith.langchain.com/agents/skills).
> 2. Browse available templates and select one to add to your agent.

> [tab] Manually
>
> 1. Select an agent in [Fleet](https://smith.langchain.com/agents?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-fleet-skills).
> 2. In the sidebar, expand the **Knowledge** drawer.
> 3. In the **Skills** section, click **+ Add skill**.
> 4. Enter the skill name, description, and instructions.

> [!TIP]
>
> When you create a new agent, Fleet automatically generates relevant skills if the agent would benefit from them. These skills are private by default. You can [share them to your workspace](#share-a-skill) from the agent sidebar.

## Fix recurring mistakes

The default response to an agent mistake is to correct it in the moment. A skill changes this: it gives the agent explicit rules to follow every time it encounters that class of task, so the same mistake cannot happen again.

When an agent handles a task incorrectly, correct it, then ask it to capture the fix:

Capture this fix as a skill.

Turn this correction into a skill so you always handle it this way.

The agent creates a `SKILL.md` encoding the correct behavior. On future sessions, it reads the skill before handling that task rather than reasoning from scratch.

## Edit a private skill

1. Select an agent in [Fleet](https://smith.langchain.com/agents?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-fleet-skills).
2. In the sidebar, expand the **Knowledge** drawer.
3. In the **Skills** section, select the skill to edit.
4. Update the skill name, description, or instructions.

## Edit a shared skill

> [!NOTE]
>
> Only the user who created the shared skill can edit it.

1. Navigate to [**Fleet > Skills**](https://smith.langchain.com/agents/skills).
2. Select the skill to edit.
3. Update the skill name, description, or instructions.
4. Click **Save Changes**.

## Share a skill

1. Select an agent in [Fleet](https://smith.langchain.com/agents?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-fleet-skills).
2. In the sidebar, expand the **Knowledge** drawer.
3. In the **Skills** section, select the skill to share.
4. Click  **Share**.

Once shared, the skill appears on the [**Skills**](https://smith.langchain.com/agents/skills) page. You can add shared skills to any agent in the workspace from the agent sidebar, and the general-purpose chat picks them up automatically.

> [!NOTE]
>
> Only the creator of a shared skill can edit or delete it.

## Delete a private skill

Deleting a private skill removes it permanently, since it is stored in that agent's memory.

1. Select the agent in [Fleet](https://smith.langchain.com/agents?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-fleet-skills).
2. In the sidebar, expand the **Knowledge** drawer.
3. In the **Skills** section, click the  icon for the skill to delete.

## Delete a shared skill

Only the user who created the shared skill can delete it.

> [!WARNING]
>
> Deleting a skill removes it from the workspace and from all agents that use it. This action cannot be undone.

1. Navigate to [**Fleet > Skills**](https://smith.langchain.com/agents/skills).
2. Select the skill to delete.
3. Click the  **Delete skill** icon.

## Use Fleet skills in local development

Download skills from your Fleet workspace with the LangSmith CLI and install them locally for use in coding agents like Claude Code, Cursor, or Codex.

By default, files are saved to `~/.agents/skills/[skill-name]/` and symlinked into `~/.claude/skills/[skill-name]/`.

```bash
langsmith fleet skills pull [skill-name] [flags]
```

| Flag | Description |
| - | - |
| `--global=false` | Install to project-level directories (`.agents/` and `.claude/`) instead of the home directory. |
| `--agent` | Target a specific agent (`claude`, `cursor`, `codex`). |
| `--copy` | Copy files instead of symlinking. |
| `--format pretty` | Display the installed skill's file tree. |

For example:

```bash
$ langsmith fleet skills pull web-research --format pretty
Installed skill "web-research" to ~/.agents/skills/web-research
  Linked: ~/.claude/skills/web-research

web-research/
├── SKILL.md
└── references/
    └── search-tips.md
```

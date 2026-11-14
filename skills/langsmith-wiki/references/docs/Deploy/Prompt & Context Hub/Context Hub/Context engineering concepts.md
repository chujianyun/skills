# Context engineering concepts

> Core concepts for context engineering in LangSmith, including skills, agents, versioning, and sharing.

Agents behave inconsistently in production when their context is poorly managed. *Context* is the information an agent relies on to act, such as system instructions, tool definitions, and reference material. *Context engineering* is the practice of building and optimizing that context to improve agent performance and capabilities.

This page covers the core concepts of context engineering in LangSmith: [skills](#skills), [agents](#agents), [the Context Hub](#context-hub-vs-store-backend), [versioning](#versioning), and [sharing](#sharing-and-permissions).

## Skills

A *skill* is a versioned repo in the Context Hub that packages a reusable capability an agent can invoke.

Skill repos usually contain:

**Common files:**

* `SKILL.md` in the root directory for instructions and usage guidance.
* Optional supporting files such as references, templates, and schemas.

Examples include email formatting, code review, and web research.

## Agents

An *agent* is an AI system that completes tasks end to end using tools, skills, and subagents. An *agent repo* packages its configuration, including high-level instructions, linked skills and subagents, and tool configuration.

Agent repos usually contain:

**Common files:**

* `AGENTS.md` for system prompt and operating instructions.
* Optional files such as `tools.json` and linked `agents/*` or `skills/*` entries.

Examples include an email assistant, coding copilot, or customer support agent.

## Choose between skills and agents

Skills are reusable context modules. Agent repos are top-level bundles that define how an agent should operate.

* Use skills for reusable instructions, policies, or examples shared across agents.
* Use agent repos for one agent's operating instructions, tools, and linked dependencies.

## Linked repos

Context Hub commits support three entry types in `files`:

* `file`: inline file content.
* `agent`: link to another agent repo.
* `skill`: link to another skill repo.

When a linked agent or skill repo gets a new commit, LangSmith propagates that update to parent repos that reference it.

> [!TIP]
>
> If you find yourself copying the same block of context into several agents, pull it out into a skill repo and reference it from each agent.

## Context Hub vs. store backend

Context in LangSmith can be managed by two different backends: the
**Context Hub** and a **store backend**. They serve different purposes, and most agents use both.

The [Context Hub](Use%20the%20Context%20Hub.md) is your agents' long-term context store. It tracks every change as a commit and supports versioning, sharing, and continuous improvement.

A *store backend* is built for runtime state. It holds the information an agent accumulates while running: memories, conversation history, user preferences, learned facts, and other data that evolves per session or per user.

## Versioning

Every change to a repo in the **Context Hub** creates a new commit. Commits are immutable, browsable, and comparable, so you can:

* See exactly what changed between two versions of an agent.
* Revert to any prior commit if a change regresses behavior.
* Tag important commits (for example, the commit you shipped on a
  specific date) for easy reference.
* Promote a commit to an **environment** like `Staging` or `Production`
  so downstream agents pull a stable version rather than the latest
  edit.

If this workflow looks familiar, that is intentional: Context Hub brings the same discipline to agent instructions that Git brings to code.

## Sharing and permissions

The **Context Hub** is designed for teams. Every repo lives in a [workspace](../../../LangSmith%20setup/Govern/Organization/Overview.md#workspaces), and access depends on workspace permissions plus repo visibility:

* **Private** repos are visible only inside the workspace.
* **Public** repos can be discovered and pulled by anyone.
* Creating commits, adding tags, and promoting environments requires update access in the workspace.

Workspace-level sharing and visibility controls make the Hub a natural place to collaborate on agents and skills, and improve them over time.

## Next steps

* [Use the Context Hub](Use%20the%20Context%20Hub.md) to create your first skill or agent.

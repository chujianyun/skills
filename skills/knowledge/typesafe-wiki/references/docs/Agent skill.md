# Agent skill

> Drop-in skill for Claude Code, Codex, and other agent environments.

The TypeSafe agent skill gives your AI coding agent full context on the TypeSafe API: the three question [types](Primitives/Primitives (Questions).md), the architectural [patterns](Patterns/Patterns.md), and best practices for structuring evaluations.

## Installation


**Claude Code**

    Run these two commands in your terminal:

    ```bash
    claude plugin marketplace add typesafe-ai/skills
    claude plugin install typesafe@typesafe-ai
    ```



**Other agents**

    ```bash
    npx skills add typesafe-ai/skills --skill typesafe-ai
    ```

    Choose your agent when prompted. Installation is project-local by default; add `-g` to install globally.



**Copy to your agent**

    Paste this prompt into your coding agent:

    ```text
    Install the TypeSafe skill. If you're in Claude Code, run `claude plugin marketplace add typesafe-ai/skills`, then `claude plugin install typesafe@typesafe-ai`. If you're in another agent, run `npx skills add typesafe-ai/skills --skill typesafe-ai` and select your agent. Use one installation method. You can read the skill directly at https://github.com/typesafe-ai/skills/blob/main/skills/typesafe-ai/SKILL.md (raw: https://raw.githubusercontent.com/typesafe-ai/skills/main/skills/typesafe-ai/SKILL.md). Then use the TypeSafe skill when working on this project.
    ```


Read [SKILL.md on GitHub](https://github.com/typesafe-ai/skills/blob/main/skills/typesafe-ai/SKILL.md) or fetch the [raw Markdown](https://raw.githubusercontent.com/typesafe-ai/skills/main/skills/typesafe-ai/SKILL.md) directly. For manual installation, copy the entire [skills/typesafe-ai directory](https://github.com/typesafe-ai/skills/tree/main/skills/typesafe-ai), including its reference files, into your agent's skills directory.

Choose one installation method to avoid duplicate copies.

### Updates

For the Claude Code plugin, run:

```bash
claude plugin marketplace update typesafe-ai
claude plugin update typesafe@typesafe-ai
```

Restart Claude Code or run `/reload-plugins` to load the update. To enable automatic updates, open `/plugin`, select **Marketplaces → typesafe-ai → Enable auto-update**.

For skills.sh installations, run `npx skills update`. For manual copies, replace the entire skill directory with the latest GitHub version.

## Example prompts

Naming the skill in your prompt — "use the TypeSafe skill" — works in any agent, so each of the prompts below does that. With the Claude Code plugin, you can also invoke `/typesafe:typesafe-ai` directly.

* A good prompt to start with is a brainstorming prompt to help you figure out where TypeSafe can best be used in a project.

  ```text
  Using the TypeSafe skill, explore the project and find opportunities for using
  intelligent judgement to stand in for complex parsing or other fragile code.
  ```

* You can also create an [API key](https://console.typesafe.ai/keys) and give your agent permission to figure out the best way to use TypeSafe by running cheap test queries.

  ```text
  Using the TypeSafe skill, run some experiments using the TypeSafe API key that I've
  exported to `TYPESAFE_API_KEY`. Propose changes based on the most promising results.
  ```

* Point your agent at a [specific cookbook](Cookbooks/Self-consistency nouls.md) that solves a problem you have in your codebase, or point it at the [cookbooks index](https://docs.typesafe.ai/cookbooks) and ask if there are any patterns that are similar to the ones in your project.

  ```text
  Using the TypeSafe skill, analyze my code and see if there are any applicable
  cookbooks (https://console.typesafe.ai/docs/cookbooks) that show how I could
  refactor my code to be less fragile or complex.
  ```

## Good vibe coding principles

1. Talk it out with your agent, using the example prompts above as a starting point.
2. Review the plan and ensure it makes sense before implementing it.
3. Put the constants (questions and thresholds) in a single place so they're easy to review. Agents aren't great at writing questions, so expect to edit collaboratively with them.
4. Don't take assertions at face value; encourage the agent to validate its assumptions.

## Common issues

### The agent isn't using the skill

With the Claude Code plugin, invoke `/typesafe:typesafe-ai`. In other agents, ask to "use the TypeSafe skill". If it still does not load, confirm the installer targeted the agent you are using, then restart the agent.

### Routing isn't working like you expect

Check the questions and thresholds. It's possible that your thresholds are either set too high (causing false negatives) or too low (causing false positives). You may also need to tweak your questions to be more specific.

### You're using confidence thresholds everywhere

If all you care about is choosing the best option, you just need to choose the option with the highest confidence (rather than setting a confidence threshold). If you have a specific statistical algorithm in mind, you should probably be using probabilities instead of confidence.

### It's difficult to review TypeSafe code

The most important thing for humans to review is the questions and any threshold constants used in your TypeSafe code. These should be defined in a single code file so that they're easy to find without too much spelunking.

### The agent invents request or response fields

A stale skill can cause this. Update it using your installation method above and retry.

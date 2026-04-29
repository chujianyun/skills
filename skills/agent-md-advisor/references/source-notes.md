# Source Notes

These notes summarize the local materials used to build this skill. Do not quote long passages; use them to ground recommendations.

## Local Source Files

- `/Users/liuwangyang/Downloads/CLAUDE/Agents.md best practices.md`
- `/Users/liuwangyang/Downloads/CLAUDE/Best practices – Codex  OpenAI Developers.md`
- `/Users/liuwangyang/Downloads/CLAUDE/CLAUDE.md Best Practices. 10 Sections to Include in your…  by Nick Babich  Mar, 2026  UX Planet.md`
- `/Users/liuwangyang/Downloads/CLAUDE/CLAUDE.md best practices - From Basic to Adaptive - DEV Community.md`
- `/Users/liuwangyang/Downloads/CLAUDE/Claude Code Best Practices Lessons From Real Projects.md`
- `/Users/liuwangyang/Downloads/CLAUDE/How to Write a CLAUDE.md File That Actually Works Best Practices for API Projects  TurboDocx.md`
- `/Users/liuwangyang/Downloads/CLAUDE/Writing a good CLAUDE.md  HumanLayer Blog.md`
- `/Users/liuwangyang/Downloads/CLAUDE/claude-code-best-practiceCLAUDE.md at main · shanraisshanclaude-code-best-practice.md`

## Article Notes

- `https://x.com/zodchiii/status/2048683276194185640` - darkzodchi article distilled through WuMing's Chinese translation, emphasizing `CLAUDE.md` as a technical brief rather than a persona prompt.

## Distilled Claims

- `AGENTS.md` is best treated as a tool-neutral README for agents, while `CLAUDE.md` is Claude Code project memory.
- The highest-value content is exact operational context: commands, structure, non-default conventions, testing, safety, and known gotchas.
- Concision matters because these files are loaded into the agent context. Long, irrelevant, or generic instructions reduce adherence; for `CLAUDE.md`, prefer roughly 80-120 high-signal lines when possible.
- Use progressive disclosure: root files should route to deeper docs, nested instruction files, rules, commands, skills, or hooks when needed.
- Split guidance across global, project, and local layers so shared files do not mix project facts with personal habits.
- Reserve emphasized critical rules for a small number of constraints that prevent specific repeated mistakes.
- Prefer deterministic tools for formatting, linting, type checking, secret scanning, and repeatable validation.
- Mature setups evolve from absent/basic files to scoped, structured, path-aware, maintained, and adaptive systems.
- Security guidance should describe where secrets live and how to access them safely, never include the values.
- Effective files are maintained like code: reviewed, pruned, updated when commands or architecture change, and improved after repeated agent mistakes.
- A useful maintenance loop is to add rules after the agent repeatedly makes a concrete mistake, not to pre-fill a giant rulebook on day one.

## Tensions In The Sources

- Some sources recommend many common sections; others argue for aggressively short files. Resolve this by starting from the common section list, then deleting anything not project-specific, stable, and useful in most sessions.
- Some sources mention generated `/init` files as useful starts; others warn against accepting generated files blindly. Resolve this by using generated output only as a draft to be reviewed line-by-line.
- Advanced features such as `.claude/rules`, skills, hooks, and MCP can be powerful but are not automatically better. Recommend them only when they reduce repeated friction or context noise.

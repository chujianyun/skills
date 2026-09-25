# Templates

Use these as starting points. Always adapt to the actual project and delete sections that do not earn their place.

## Minimal AGENTS.md

```md
# AGENTS.md

## Project
[One sentence: what this project is, who it serves, and primary stack.]

## Commands
- Install: `[command]`
- Dev: `[command]`
- Test: `[command]`
- Lint: `[command]`
- Build: `[command]`

## Project Structure
- `[path]/` - [purpose]
- `[path]/` - [purpose]
- Add new [feature/type] code in `[path]/`.

## Conventions
- [Non-default convention the agent would not infer.]
- [Forbidden library/pattern, if any.]

## Testing
- Prefer targeted tests for changed files.
- Add tests for new behavior or changed business logic.
- Before finishing, run: `[targeted command]`.

## Safety
- Do not commit secrets or `.env` files.
- Ask before package installs, destructive file operations, git pushes, or infrastructure changes.
```

## Full AGENTS.md

```md
# AGENTS.md

## Project Overview
[1-2 short paragraphs: product purpose, users, constraints, what to optimize for.]

## Tech Stack
- Runtime: [version]
- Framework: [framework]
- Package manager: [tool]
- Testing: [framework]
- Do not introduce: [libraries/patterns]

## Commands

### File-Scoped Checks (Preferred)
- Test one file: `[command]`
- Lint one file: `[command]`
- Typecheck: `[command]`

### Full Checks
- Test suite: `[command]`
- Build: `[command]`

## Project Structure
- `[path]/` - [responsibility]
- `[path]/` - [responsibility]

Where new code goes:
- [Rule]
- [Rule]

## Conventions
- [Project-specific rule]
- [Project-specific rule]
- [Anti-pattern to avoid]

## Testing And Quality
- [When tests are required]
- [What states or cases to verify]
- Done means: [checks that must pass]

## Safety And Permissions

Allowed without asking:
- Read source files
- Run targeted lint/typecheck/test commands

Ask before:
- Installing packages
- Deleting files or directories
- Running full E2E suites or expensive builds
- Git commit/push
- Infrastructure apply/destroy

## Reference Documents
- `[path]` - Read when [trigger]. Covers [summary].
- `[path]` - Read when [trigger]. Covers [summary].

## Good Patterns / Avoid
- Good: `[path]` - [why]
- Avoid: `[path]` - [why]
```

## Minimal CLAUDE.md

```md
# CLAUDE.md

This file is a short technical brief for Claude Code. Keep only stable project context that prevents concrete mistakes.

## Project
[One sentence project description and stack.]

## Commands
- Dev: `[command]`
- Test: `[command]`
- Lint: `[command]`
- Build: `[command]`

## Structure
- `[path]/` - [purpose]
- `[path]/` - [purpose]

## Rules
- [Use MUST / MUST NOT only for critical constraints.]
- [Non-default convention.]
- Never commit secrets or `.env` files.

## References
- `@[path]` - Read when [trigger].
```

## CLAUDE.md With Progressive Disclosure

```md
# CLAUDE.md

This file gives Claude Code the stable project context needed for every session. Keep it short; put personal preferences in local/user memory and load detailed docs only when relevant.

## Project
[One or two lines: product, users, stack, what matters most.]

## Commands
- Install: `[command]`
- Dev: `[command]`
- Targeted test: `[command]`
- Full test: `[command]`
- Build: `[command]`

## Architecture Map
- `[path]/` - [responsibility]
- `[path]/` - [responsibility]
- New [type] code belongs in `[path]/`.

## Critical Rules
- MUST [critical project-specific rule].
- MUST NOT [critical forbidden action].
- Prefer [project-specific choice] over [alternative].
- Ask before changing [risky area].

Keep this section under about 15 items. Each rule should prevent a specific mistake.

## Reference Documents
- `@[path]` - Read when [trigger]. Covers [summary].
- `@[path]` - Read when [trigger]. Covers [summary].

## Safety
- Secrets live in [secret manager / `.env.example` pattern], never in committed files.
- Ask before package installs, destructive file changes, git pushes, or infrastructure changes.
```

## Monorepo Pattern

```text
repo/
├── AGENTS.md                  # Shared standards and integration points
├── apps/web/AGENTS.md         # Frontend-specific commands and rules
├── services/api/AGENTS.md     # Backend-specific commands and rules
└── infra/AGENTS.md            # Infrastructure-specific safety and commands
```

Root file:

```md
# AGENTS.md

## Repository
[One paragraph explaining the monorepo and shared constraints.]

## Shared Commands
- Install: `[command]`
- Check all changed packages: `[command]`

## Workspaces
- `apps/web/` - [purpose]. See `apps/web/AGENTS.md`.
- `services/api/` - [purpose]. See `services/api/AGENTS.md`.
- `infra/` - [purpose]. See `infra/AGENTS.md`.

## Shared Rules
- [Repo-wide rule]
- [Cross-package boundary rule]
- Ask before changing public APIs, database schema, or infrastructure.
```

## Reference Document Entry

```md
## Reference Documents
- `docs/api-architecture.md` - Read when adding or changing API endpoints. Covers route conventions, auth middleware, and response shapes.
- `docs/testing.md` - Read when adding tests or debugging CI failures. Covers fixtures, mocks, and commands.
```

## Safety Section

```md
## Safety And Permissions

Allowed without prompting:
- Read files and inspect git status
- Run targeted lint, typecheck, and unit test commands
- Format files with the project formatter

Require approval first:
- Installing or upgrading dependencies
- Deleting files or directories
- Running migrations against shared environments
- Applying infrastructure changes
- Committing, pushing, or opening PRs

Secrets:
- Never commit `.env`, tokens, private keys, or credentials
- Use `.env.example` for variable names only
- Production secrets live in [secret manager name/path]
```

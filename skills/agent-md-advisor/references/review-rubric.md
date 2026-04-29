# Review Rubric

Use this rubric to diagnose `AGENTS.md`, `CLAUDE.md`, `CLAUDE.local.md`, and related agent instruction files.

## Review Procedure

1. Identify scope: tool-neutral, Claude-specific, personal, team-shared, repo-root, or subdirectory.
2. Count rough length and scan for low-signal sections, persona prompts, and motivational language.
3. Verify commands against project files before recommending them.
4. Check whether rules are project-specific, stable, and actionable.
5. Ask whether each important line prevents a concrete mistake the agent would otherwise make.
6. Check whether long task-specific content should be split into references, commands, skills, rules, or hooks.
7. Check for secrets, risky operations, and missing permission boundaries.
8. Assign a maturity level and prioritize fixes.

## Maturity Level

- **L0 Absent**: no file exists.
- **L1 Basic**: file exists but mostly generic or generated.
- **L2 Scoped**: contains explicit project constraints and commands.
- **L3 Structured**: uses references or modular docs with clear triggers.
- **L4 Abstracted**: uses nested/path-scoped files or tool-specific rules.
- **L5 Maintained**: concise, current, reviewed, and aligned with repo reality.
- **L6 Adaptive**: uses skills, commands, hooks, MCP, or dynamic context appropriately.

Pick the highest level that is actually supported by the content, not by directory presence alone.

## Scorecard

Rate each category 0-3:

| Category | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| Scope | Missing or wrong file | Unclear audience | Mostly clear | Correct file, scope, and hierarchy |
| Signal | Empty or noisy | Long/generic | Mostly concise | Short, precise, high-signal |
| Commands | Missing | Vague/unverified | Some exact commands | Exact, current, file-scoped + full |
| Structure | No navigation | Basic folders only | Useful map | Placement rules and examples |
| Conventions | Generic | Too many defaults | Some project-specific | Non-default, actionable, stable |
| Testing | Missing | “run tests” only | Basic test commands | Done criteria and targeted checks |
| Safety | Missing | Generic warnings | Some boundaries | Secrets and approval gates clear |
| Disclosure | Everything inline | Some links | Clear references | Task/path-specific loading where useful |
| Maintenance | Stale | No review habit | Mostly current | Treated as code and actively pruned |

Interpretation:

- **0-8**: high risk; create or rewrite
- **9-16**: usable but inconsistent; focused cleanup
- **17-23**: strong; refine edge cases
- **24-27**: excellent; avoid over-engineering

## Common Violations And Fixes

### Too long

Symptoms:

- More than 300 lines
- Full docs pasted inline
- Many rarely relevant rules

Fix:

- Keep only global constraints in the root file
- Move long sections to docs with “Read when”
- Use nested files for subprojects

### Vague commands

Symptoms:

- “Run tests”
- “Build normally”
- “Check quality”

Fix:

- Replace with exact commands
- Include file-scoped fast checks
- Mention full suite only when needed

### Generic style rules

Symptoms:

- “Act like a senior engineer”
- “Write clean code”
- “Follow best practices”
- “Think step by step”
- Long language basics

Fix:

- Remove obvious rules
- Keep only project-specific conventions and forbidden alternatives
- Point to linters/formatters for mechanical style

### Persona prompt instead of technical brief

Symptoms:

- The file mostly describes attitude, tone, or intelligence
- The file lacks commands, architecture, safety boundaries, and done criteria
- Rules sound inspiring but do not prevent a named failure mode

Fix:

- Replace persona language with exact commands, architecture map, and hard constraints
- Keep only rules that answer: “What mistake does this prevent?”
- Add examples using real paths when behavior is hard to infer

### Overloaded critical rules

Symptoms:

- Dozens of `MUST` / `MUST NOT` bullets
- Every preference is marked as critical
- Important safety constraints are buried among generic quality advice

Fix:

- Keep critical rules under about 15 items
- Reserve emphasis for safety, data loss, forbidden tools, and repeated project-specific mistakes
- Move normal conventions to a separate section or deterministic tooling

### Duplicated documentation

Symptoms:

- README content pasted
- API reference pasted
- Architecture docs copied into the file

Fix:

- Summarize in one or two lines
- Link to authoritative docs
- Add “Read when” triggers

### Missing safety boundary

Symptoms:

- No approval rules
- No destructive-operation guidance
- No secret handling guidance

Fix:

- Add allowed operations
- Add approval-required operations
- Add secret storage rules without revealing secrets

### Wrong abstraction level

Symptoms:

- Small repo has a complex agent/rules/hooks system
- Large monorepo has one huge root file
- Personal preferences are committed into team-shared files

Fix:

- For small projects: compress to one simple file
- For monorepos: split by domain or directory
- Add skills/hooks only when repeated workflow justifies them
- Keep global, project, and local guidance in separate files or memory layers

## Diagnostic Output Template

```markdown
# Agent 指令文件诊断

结论：优秀 / 基本可用 / 需要重构 / 风险较高
成熟度：L0-L6
总分：X/27

## 主要问题
1. [P1] 问题标题
   - 位置：`path:line`
   - 为什么影响 agent：...
   - 建议：...

## 做得好的地方
- ...

## 优化建议
1. ...
2. ...

## 建议改法
- 保留：...
- 删除：...
- 拆分：...
- 新增：...
```

## Optimization Checklist

Before editing, decide:

- What should remain in the root file?
- What should move to references or nested files?
- Which commands are verified?
- Which rules are project-specific and stable?
- Which rules prevent a concrete known mistake?
- Which personal preferences should stay local?
- Which risky operations need explicit approval?

After editing, verify:

- File is shorter and more actionable
- No secrets or private values were introduced
- Commands match real project scripts
- Critical rules are few enough to stay salient
- References point to existing files, or are clearly marked as proposed
- The result answers what a new AI teammate needs to know before the first change

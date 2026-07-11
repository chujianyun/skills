# AGENTS.md

## Project

This repository is WuMing's public collection of reusable Agent Skills. Skills are grouped by domain, validated as independent capability folders, and distributed through the Claude plugin marketplace plus an optional enterprise Skills market.

## Commands

- List Skills: `find skills -mindepth 3 -maxdepth 3 -type f -name SKILL.md | sort`
- Validate one Skill: `python3 scripts/validate_skill.py <skill-name>`
- Run repository tests: `python3 -m unittest discover -s tests -v`
- Validate marketplace JSON: `python3 -m json.tool .claude-plugin/marketplace.json >/dev/null`
- Validate taxonomy JSON: `python3 -m json.tool config/skill-categories.json >/dev/null`
- Record completed optimizer review: `python3 scripts/record_optimizer_review.py <skill-name> --status passed`
- Publish one Skill: `/publish-skill <skill-name>`
- Publishing backend: `python3 scripts/publish_skill.py <skill-name>`

## Repository Map

- `skills/<category>/<skill-name>/SKILL.md` — required Skill entry point.
- `skills/<category>/<skill-name>/references/` — detailed guidance loaded only when needed.
- `skills/<category>/<skill-name>/scripts/` — deterministic helpers.
- `skills/<category>/<skill-name>/assets/` — templates and output resources.
- `skills/<category>/<skill-name>/agents/openai.yaml` — optional Codex UI metadata.
- `config/skill-categories.json` — category source of truth.
- `.claude-plugin/marketplace.json` — public Claude plugin registrations.
- `.claude/commands/publish-skill.md` — Agent-facing publication workflow.
- `scripts/` — validation, optimizer attestation, and publishing tools.
- `tests/` — standard-library unit tests for repository governance.

## Category Routing

Choose exactly one existing category before creating a Skill. Do not invent a near-duplicate category without team approval.

| Category | Put the Skill here when its primary responsibility is |
|---|---|
| `knowledge` | Product documentation, a knowledge base, or domain reference |
| `review` | Reviewing or optimizing prompts, Agents, configuration, or Skills |
| `career` | Career-level evaluation, promotion, or professional coaching |
| `content` | Interpreting or transforming articles, papers, source code, or prose |
| `visual` | Producing diagrams, visual assets, or QR codes |
| `media` | Processing audio, PDFs, images, downloads, or other media |
| `operations` | Operating services, troubleshooting, cleanup, or platform integration |
| `distribution` | Installing, synchronizing, packaging, publishing, or distributing Skills |

If two categories seem plausible, classify by the Skill's primary output, not by incidental tools it uses. Update `config/skill-categories.json`, `README.md`, and `.claude-plugin/marketplace.json` together.

## Skill Standard

- Directory names and frontmatter `name` MUST use the same lowercase-hyphen form.
- Frontmatter MUST contain only `name` and `description`.
- `description` MUST work as a trigger rule: state what the Skill does and when to use it; add a non-use case when overlap is likely.
- Keep `SKILL.md` as the dispatcher. Move long rules and checklists to `references/`, deterministic work to `scripts/`, and reusable output material to `assets/`.
- Link every required reference directly from `SKILL.md`; avoid multi-hop reference chains.
- Define ordered workflow steps, failure behavior, stopping conditions, and an output contract.
- Add explicit confirmation gates for deletion, overwrite, restart, deployment, external writes, paid calls, credential changes, and other high-impact actions.
- Document external dependencies with installation, verification, and missing-dependency behavior.
- `README.md` inside a Skill is optional and human-facing; it must not duplicate the AI execution contract in `SKILL.md`.
- Include `agents/openai.yaml` when the Skill should have curated UI metadata.

## New Skill Workflow

Follow this sequence; publication is blocked if any gate fails.

1. **Classify** — select one category from `config/skill-categories.json`.
2. **Create** — add `skills/<category>/<skill-name>/` and register it in the taxonomy, README, and marketplace.
3. **Optimize** — use `skill-optimizer` to scan triggering, workflow, failure handling, confirmation gates, output contract, progressive disclosure, dependencies, sensitive data, and high-impact operations.
4. **Fix** — apply safe optimizer findings inside the new Skill. Creating and publishing a new Skill is authorization for these in-scope fixes; high-risk or out-of-scope changes still require approval.
5. **Validate** — run `python3 scripts/validate_skill.py <skill-name>` until it passes.
6. **Attest** — only after semantic review and validation pass, record the content-bound optimizer report.
7. **Publish** — run `/publish-skill <skill-name>`; the enterprise market must confirm success before Git commit and push.

For an existing Skill, `skill-optimizer` keeps its normal review → plan → explicit confirmation → modification workflow.

## Enterprise Market Contract

`SKILLS_MARKET_PUBLISHER` must point to an executable maintained by the enterprise market team. The repository invokes:

```text
<publisher> --skill-dir <absolute-path> --name <skill-name> --category <category>
```

Exit code `0` means the market confirmed upload. Missing configuration, timeout, or any nonzero exit code is a hard failure. Credentials belong in the adapter's environment or secret manager, never in this repository.

Invoking `/publish-skill <skill-name>` explicitly authorizes market upload, a scoped commit, and pushing the current non-main branch for that Skill. It does not authorize unrelated files, destructive cleanup, force push, publishing from `main`, or bypassing a failed gate.

## Verification And Done Criteria

A Skill change is complete only when:

- It is listed exactly once in the taxonomy and marketplace with its classified path.
- Its README link uses `skills/<category>/<skill-name>/SKILL.md`.
- `python3 scripts/validate_skill.py <skill-name>` passes.
- `python3 -m unittest discover -s tests -v` passes after governance-script changes.
- `python3 -m json.tool .claude-plugin/marketplace.json >/dev/null` passes.
- `git diff --check` passes.
- Market publication and Git push are reported separately; neither is implied when an adapter is unavailable.

## Safety

- Never commit secrets, tokens, cookies, private keys, production credentials, private market URLs, or machine-specific overrides.
- Preserve unrelated and untracked user files; use path-limited staging.
- Ask before deleting Skills, rewriting many existing Skills, changing license or marketplace owner metadata, changing remotes, force pushing, or publishing outside `/publish-skill`.
- Do not claim success when optimizer review, validation, market upload, commit, or push has failed.

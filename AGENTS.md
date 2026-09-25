# AGENTS.md

## Project

This repository is WuMing's public collection of reusable Agent Skills. Skills live flat under `skills/`, validated as independent capability folders, and registered in the Claude plugin marketplace.

## Commands

- List Skills: `find skills -mindepth 2 -maxdepth 2 -type f -name SKILL.md | sort`
- Validate one Skill: `python3 scripts/validate_skill.py <skill-name>`
- Run repository tests: `python3 -m unittest discover -s tests -v`
- Validate marketplace JSON: `python3 -m json.tool .claude-plugin/marketplace.json >/dev/null`
- Validate registry JSON: `python3 -m json.tool config/skills.json >/dev/null`

## Repository Map

- `skills/<skill-name>/SKILL.md` — required Skill entry point.
- `skills/<skill-name>/references/` — detailed guidance loaded only when needed.
- `skills/<skill-name>/scripts/` — deterministic helpers.
- `skills/<skill-name>/assets/` — templates and output resources.
- `skills/<skill-name>/agents/openai.yaml` — optional Codex UI metadata.
- `config/skills.json` — flat Skill registry, the source of truth.
- `.claude-plugin/marketplace.json` — public Claude plugin registrations.
- `scripts/` — validation and repository governance tools.
- `tests/` — standard-library unit tests for repository governance.

## Registration

Skills are not grouped into physical categories. When adding or removing a Skill, update `config/skills.json`, `README.md`, and `.claude-plugin/marketplace.json` together.

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

## Branch Policy

- Make all changes directly on `main` by default.
- If a new branch is needed, run the repository tests and all checks applicable to the change. Once they pass, immediately merge the branch into `main`; do not leave tested changes on a separate branch at task completion.
- If tests or checks fail, fix the failures before merging. Resolve any merge conflicts and rerun the affected checks before considering the merge complete.
- When a task requires a push, push the completed changes on `main` to `origin/main`.

## Skill Optimizer Repository Sync

- Whenever any file under `skills/skill-optimizer/` changes, push the completed changes to this repository and also synchronize and push the Skill's own code and supporting files to `https://github.com/chujianyun/skill-optimizer.git`.
- Sync only the `skill-optimizer` Skill's contents, respecting the standalone repository's layout and preserving unrelated files; do not copy this collection's other Skills or repository-level files.
- This additional push is part of the authorized Skill-change workflow. A `skill-optimizer` change is complete only after both repository pushes succeed; report any sync or push failure explicitly.

## New Skill Checklist

Copy this checklist into the task progress before creating a Skill. Complete it from top to bottom; do not mark a later item complete while an earlier item is still open.

- [ ] **Create and register** — add `skills/<skill-name>/` and register it in `config/skills.json`, README, and marketplace.
- [ ] **Optimize and validate** — use `skill-optimizer` to automatically review and fix triggering, workflow, failure handling, confirmation gates, output contract, progressive disclosure, dependencies, sensitive data, and high-impact operations; then run `python3 scripts/validate_skill.py <skill-name>` until it passes.
- [ ] **Commit and push** — stage only the new Skill and its registry, README, and marketplace registrations; commit on `main`, or immediately merge a new branch into `main` after tests and applicable checks pass, then push `main` to `origin`.

Creating a new Skill authorizes safe, in-scope optimizer fixes plus a path-limited commit and push after validation. High-risk or out-of-scope changes still require approval. For an existing Skill, `skill-optimizer` keeps its normal review → plan → explicit confirmation → modification workflow.

## Verification And Done Criteria

A Skill change is complete only when:

- It is listed exactly once in `config/skills.json` and the marketplace with its flat path.
- Its README link uses `skills/<skill-name>/SKILL.md`.
- `python3 scripts/validate_skill.py <skill-name>` passes.
- `python3 -m unittest discover -s tests -v` passes after governance-script changes.
- `python3 -m json.tool .claude-plugin/marketplace.json >/dev/null` passes.
- `git diff --check` passes.
- The scoped commit is on `main` (with any new branch merged immediately after tests and applicable checks pass) and pushed successfully to `origin/main`.

## Safety

- Never commit secrets, tokens, cookies, private keys, production credentials, private market URLs, or machine-specific overrides.
- Preserve unrelated and untracked user files; use path-limited staging.
- Ask before deleting Skills, rewriting many existing Skills, changing license or marketplace owner metadata, changing remotes, or force pushing.
- Do not claim success when optimizer review, validation, commit, or push has failed.

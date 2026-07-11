# Skill Taxonomy And Publishing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reorganize every Skill under a governed category and add a quality-gated command that publishes to an internal Skills market before committing and pushing Git changes.

**Architecture:** A JSON taxonomy is the single source of truth for category placement. Small Python standard-library modules discover and validate Skills, record optimizer attestations, and orchestrate market upload plus Git; a tracked Agent command connects the semantic `skill-optimizer` review to the deterministic scripts.

**Tech Stack:** Markdown, JSON, Python 3 standard library, `unittest`, Git, Claude-compatible command Markdown.

## Global Constraints

- Skill directories use `skills/<category>/<skill-name>/`.
- Valid categories are exactly `knowledge`, `review`, `career`, `content`, `visual`, `media`, `operations`, and `distribution`.
- Frontmatter contains only `name` and `description`.
- Market credentials, URLs, and tokens must not be committed or printed.
- Market upload must succeed before Git commit or push runs.
- The existing untracked `skills/local-audio-transcriber/README.md` must be preserved during migration.
- The implementation must not push the feature branch while building the publishing capability.

---

### Task 1: Taxonomy Manifest And Physical Migration

**Files:**
- Create: `config/skill-categories.json`
- Move: `skills/<skill-name>/` to `skills/<category>/<skill-name>/` for all 25 existing Skills
- Modify: `.claude-plugin/marketplace.json`

**Interfaces:**
- Produces: `config/skill-categories.json` with `categories.<category>.description` and `categories.<category>.skills`.
- Produces: canonical marketplace paths in the form `./skills/<category>/<skill-name>`.

- [ ] **Step 1: Add the complete category manifest**

Create all eight category objects and list each existing Skill exactly once. Use this mapping:

```text
knowledge: qoder-wiki
review: prompt-optimizer, agent-md-advisor, claude-config-advisor, skill-optimizer, agent-optimizer
career: p7-advisor, p8-advisor, p9-advisor
content: article-interpreter, github-code-interpreter, paper-interpreter, remove-ai-flavor
visual: mermaid, wechat-official-account-qr
media: local-audio-transcriber, opendataloader-pdf, alltuu-downloader, photoplus-downloader
operations: copaw-ops, openclaw-ops, openclaw-session-cleaner, hermes-ops, hermes-qq
distribution: claudian-installer
```

- [ ] **Step 2: Move complete Skill directories**

Use `mkdir -p skills/<category>` followed by `git mv skills/<skill-name> skills/<category>/<skill-name>` for tracked content. Move the untracked audio README together with its parent directory and confirm it remains untracked.

- [ ] **Step 3: Rewrite marketplace paths mechanically**

Change every plugin `skills` entry to its manifest-derived classified path. Do not alter owner metadata, descriptions, plugin names, or licensing.

- [ ] **Step 4: Check migration completeness**

Run:

```bash
find skills -mindepth 3 -maxdepth 3 -type f -name SKILL.md | sort
python3 -m json.tool .claude-plugin/marketplace.json >/dev/null
```

Expected: 25 `SKILL.md` files and valid JSON; no `skills/<skill-name>/SKILL.md` remains.

- [ ] **Step 5: Commit the migration**

```bash
git add config/skill-categories.json skills .claude-plugin/marketplace.json
git commit -m "refactor: classify skills by domain"
```

Use a path-limited add so the user's untracked README is not staged.

---

### Task 2: Repository Discovery And Deterministic Quality Gate

**Files:**
- Create: `scripts/skill_repository.py`
- Create: `scripts/validate_skill.py`
- Create: `tests/test_skill_repository.py`

**Interfaces:**
- Produces: `load_taxonomy(root: Path) -> dict[str, set[str]]`.
- Produces: `discover_skills(root: Path) -> dict[str, Path]`.
- Produces: `validate_skill(root: Path, name: str) -> list[str]`, where an empty list means pass.
- Produces CLI: `python3 scripts/validate_skill.py <skill-name>`.

- [ ] **Step 1: Write failing discovery tests**

Cover duplicate manifest membership, unknown category folders, missing Skill names, frontmatter keys beyond `name` and `description`, directory/name mismatch, missing local Markdown references, marketplace path mismatch, README legacy links, and common secret patterns.

Run:

```bash
python3 -m unittest tests.test_skill_repository -v
```

Expected: FAIL because `scripts.skill_repository` does not exist.

- [ ] **Step 2: Implement taxonomy loading and recursive discovery**

Use `pathlib.Path.rglob("SKILL.md")` and accept only files exactly three directory levels below the repository root: `skills/category/name/SKILL.md`. Reject duplicate names rather than silently choosing one.

- [ ] **Step 3: Implement frontmatter and repository checks**

Parse the opening YAML subset without adding PyYAML: require opening and closing `---`, accept only scalar `name:` and `description:` keys, and report unsupported or duplicate keys. Resolve local Markdown links relative to `SKILL.md`; ignore `http:`, `https:`, anchors, and template placeholders.

- [ ] **Step 4: Add the validation CLI**

Print each error to stderr and exit `1`; on success print the canonical Skill path and exit `0`. Also call the installed official validator when `~/.agents/skills/.system/skill-creator/scripts/quick_validate.py` exists.

- [ ] **Step 5: Run focused tests and repository validation**

```bash
python3 -m unittest tests.test_skill_repository -v
python3 scripts/validate_skill.py qoder-wiki
```

Expected: all tests pass and `qoder-wiki` reports success.

- [ ] **Step 6: Commit the quality gate**

```bash
git add scripts/skill_repository.py scripts/validate_skill.py tests/test_skill_repository.py
git commit -m "feat: add classified skill quality gate"
```

---

### Task 3: Optimizer Attestation And Agent Command

**Files:**
- Create: `scripts/record_optimizer_review.py`
- Create: `tests/test_optimizer_review.py`
- Modify: `.gitignore`
- Create: `.claude/commands/publish-skill.md`

**Interfaces:**
- Produces: `skill_digest(skill_dir: Path) -> str`, a SHA-256 digest over stable relative paths and file bytes.
- Produces CLI: `python3 scripts/record_optimizer_review.py <skill-name> --status passed`.
- Produces report: `.skill-publish/<skill-name>.optimizer.json` containing `skill`, `category`, `digest`, `status`, `reviewer`, and UTC `reviewed_at`.

- [ ] **Step 1: Write failing attestation tests**

Test deterministic hashing, report creation, refusal of a non-passed status for publication, and digest changes after a Skill file changes.

Run:

```bash
python3 -m unittest tests.test_optimizer_review -v
```

Expected: FAIL because `scripts.record_optimizer_review` does not exist.

- [ ] **Step 2: Implement digest and report writing**

Hash every regular file below the target Skill except `.DS_Store`, `__pycache__`, and bytecode. Write JSON atomically into ignored `.skill-publish/` and never include file contents in the report.

- [ ] **Step 3: Track only the team command**

Keep `.claude` ignored by default but unignore `.claude/commands/publish-skill.md`. Add `.skill-publish/` to `.gitignore`.

- [ ] **Step 4: Define `/publish-skill <skill-name>`**

The command must perform these ordered actions:

1. Resolve the classified Skill.
2. Invoke `skill-optimizer` and apply safe changes within the target new Skill.
3. Stop if high-risk changes need approval or any review item remains unresolved.
4. Run `scripts/validate_skill.py`.
5. Record a passed optimizer report only after the semantic review and deterministic validation pass.
6. Run `scripts/publish_skill.py` with the report.

The command must state that a missing market adapter is a hard stop and must not be represented as success.

- [ ] **Step 5: Run tests and inspect ignore behavior**

```bash
python3 -m unittest tests.test_optimizer_review -v
git check-ignore .skill-publish/example.optimizer.json
git check-ignore .claude/commands/publish-skill.md
```

Expected: tests pass; report is ignored; command is not ignored.

- [ ] **Step 6: Commit the optimizer bridge**

```bash
git add .gitignore .claude/commands/publish-skill.md scripts/record_optimizer_review.py tests/test_optimizer_review.py
git commit -m "feat: require optimizer attestation before publishing"
```

---

### Task 4: Market Upload And Git Publishing Pipeline

**Files:**
- Create: `scripts/publish_skill.py`
- Create: `tests/test_publish_skill.py`

**Interfaces:**
- Consumes: classified Skill discovery and deterministic validation from `scripts.skill_repository`.
- Consumes: optimizer report from `.skill-publish/<skill-name>.optimizer.json`.
- Consumes: executable path from `SKILLS_MARKET_PUBLISHER`.
- Produces: market invocation `<publisher> --skill-dir <absolute-path> --name <name> --category <category>`.
- Produces CLI: `python3 scripts/publish_skill.py <skill-name> [--report <path>] [--no-git]`.

- [ ] **Step 1: Write failing pipeline tests**

Use temporary Git repositories and fake executable publishers. Cover missing adapter, stale digest, validation failure, market failure, forbidden `main`, dirty unrelated files, success with `--no-git`, and ordering that prevents Git calls before market success.

Run:

```bash
python3 -m unittest tests.test_publish_skill -v
```

Expected: FAIL because `scripts.publish_skill` does not exist.

- [ ] **Step 2: Implement preflight and report verification**

Require a passed report with reviewer `skill-optimizer`, matching Skill name/category, and current digest. Run deterministic validation before invoking the market adapter.

- [ ] **Step 3: Implement market invocation**

Resolve `SKILLS_MARKET_PUBLISHER` as a single executable path and call it with an argument list, never via `shell=True`. Forward normal output, enforce a finite timeout, and treat any nonzero result as failure.

- [ ] **Step 4: Implement guarded Git commit and push**

Reject `main`, `master`, and detached HEAD. Reject unrelated working-tree changes. Stage only the target Skill and required repository metadata, commit `publish: <skill-name>`, then run `git push -u origin <current-branch>`. `--no-git` supports safe integration testing after a successful fake market upload.

- [ ] **Step 5: Run focused tests**

```bash
python3 -m unittest tests.test_publish_skill -v
```

Expected: all tests pass, and failure-path tests show no Git commit.

- [ ] **Step 6: Commit the pipeline**

```bash
git add scripts/publish_skill.py tests/test_publish_skill.py
git commit -m "feat: publish optimized skills before git push"
```

---

### Task 5: Team Instructions And Human Documentation

**Files:**
- Modify: `AGENTS.md`
- Modify: `README.md`

**Interfaces:**
- Documents: category selection, Skill creation, optimizer gate, validation, internal market adapter, and Git ordering.
- Documents commands using recursive classified paths.

- [ ] **Step 1: Rewrite `AGENTS.md` as an executable team brief**

Keep it under 150 lines. Include exact commands, the eight-category routing table, file placement rules, required optimizer and validation gates, market adapter contract, done criteria, and safety boundaries. Remove the obsolete `skills/<skill-name>` convention and the contradictory blanket rule against Skill README files.

- [ ] **Step 2: Update `README.md` links and publishing guidance**

Keep the human-facing Skill map, update every link to its classified path, explain the directory taxonomy, and document `/publish-skill <skill-name>` plus `SKILLS_MARKET_PUBLISHER`. Do not include private market URLs or credentials.

- [ ] **Step 3: Check all old paths are gone**

```bash
rg -n 'skills/[a-z0-9-]+/SKILL\.md|\./skills/[a-z0-9-]+"' README.md AGENTS.md .claude-plugin/marketplace.json
```

Expected: no matches for legacy two-level Skill paths.

- [ ] **Step 4: Commit documentation**

```bash
git add AGENTS.md README.md
git commit -m "docs: define team skill publishing standards"
```

---

### Task 6: Full Repository Verification

**Files:**
- Modify only files that fail an in-scope verification check.

**Interfaces:**
- Consumes every implementation deliverable.
- Produces a verified branch ready for Qoder handoff.

- [ ] **Step 1: Run all unit tests**

```bash
python3 -m unittest discover -s tests -v
```

Expected: all tests pass.

- [ ] **Step 2: Validate every Skill**

```bash
find skills -mindepth 3 -maxdepth 3 -type f -name SKILL.md -print0 | while IFS= read -r -d '' file; do python3 scripts/validate_skill.py "$(basename "$(dirname "$file")")"; done
```

Expected: all 25 Skills pass.

- [ ] **Step 3: Validate repository metadata and whitespace**

```bash
python3 -m json.tool .claude-plugin/marketplace.json >/dev/null
python3 -m json.tool config/skill-categories.json >/dev/null
git diff --check
```

Expected: all commands exit `0`.

- [ ] **Step 4: Exercise safe publishing failure**

```bash
env -u SKILLS_MARKET_PUBLISHER python3 scripts/publish_skill.py qoder-wiki --no-git
```

Expected: nonzero exit with a clear missing-adapter message and no new Git commit.

- [ ] **Step 5: Review final scope**

Run `git status --short --branch` and `git log --oneline main..HEAD`. Confirm the user's audio README remains untracked and the branch has not been pushed.

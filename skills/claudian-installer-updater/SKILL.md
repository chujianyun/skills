---
name: claudian-installer-updater
description: 更新私有 skill 仓库中的 claudian-installer 资源文件。适用于用户提到“更新 Claudian 安装器”“同步 Claudian releases”“检查 claudian-installer 是否有新版本”“刷新 claudian-installer assets”时使用。会读取 claudian-installer/SKILL.md 中记录的基线版本，查询 GitHub releases；若发现新版本，则下载并替换 main.js、manifest.json、styles.css，并把新版本写回 SKILL.md。
---

# Claudian Installer Updater

Update the private `claudian-installer` skill by syncing its bundled plugin assets to the latest Claudian GitHub release.

## Naming note

Keep the skill folder name as `claudian-installer-updater`. It is explicit, stable, and matches the target skill plus the action performed.

## Target paths

- Source skill: `/Users/liuwangyang/Documents/coding/our/skills/skills/claudian-installer`
- Assets dir: `/Users/liuwangyang/Documents/coding/our/skills/skills/claudian-installer/assets`
- Skill doc: `/Users/liuwangyang/Documents/coding/our/skills/skills/claudian-installer/SKILL.md`
- Release page/API: `https://github.com/YishenTu/claudian/releases` and `https://api.github.com/repos/YishenTu/claudian/releases/latest`

## Required behavior

1. Read `claudian-installer/SKILL.md` first.
2. Ensure the file contains a recorded base version line in the form:
   - `Current bundled Claudian version: X.Y.Z`
3. If the version line is missing, infer the current bundled version from `assets/manifest.json` and write the line into `SKILL.md` before doing anything else.
4. Query the latest GitHub release.
5. If the latest release version equals the recorded version, stop and report that no update is needed.
6. If the latest release is newer, download these exact assets from the release and overwrite the local copies:
   - `main.js`
   - `manifest.json`
   - `styles.css`
7. After replacement, verify:
   - all three files exist
   - `manifest.json` parses
   - `manifest.json.version` equals the release version
8. Update `SKILL.md` so `Current bundled Claudian version: ...` matches the new version.
9. Report the old version, new version, and which files changed.

## Execution workflow

### Step 1: Read current state

- Read `SKILL.md`.
- Read `assets/manifest.json`.
- Prefer the explicit version line in `SKILL.md` as the source of truth.
- If `SKILL.md` has no version line, use `manifest.json.version` as the baseline and insert the version line under the main intro section.

Suggested placement in `SKILL.md`:

```md
## Bundled Version

Current bundled Claudian version: 1.2.3
```

### Step 2: Check upstream release

Use the GitHub API endpoint:

```bash
curl -L -s https://api.github.com/repos/YishenTu/claudian/releases/latest
```

Extract:
- `tag_name`
- asset download URLs for `main.js`, `manifest.json`, `styles.css`

Normalize the version by stripping a leading `v` if present.

### Step 3: Decide whether to update

- If upstream version == recorded version: do nothing else.
- If upstream version != recorded version: continue.

Do not ask the user for confirmation; this skill is intended to perform the sync automatically.

### Step 4: Download and replace assets

Download the three files from the latest release into a temp directory first. Only overwrite local assets after all downloads succeed.

Use a deterministic script rather than ad-hoc shell pipelines. Run `scripts/update_claudian_installer.py`.

### Step 5: Verify and persist version

After overwrite:
- parse local `assets/manifest.json`
- confirm `version` matches the release version
- update the version line in `SKILL.md`

## Script

Use `scripts/update_claudian_installer.py` in this skill. It should:
- read the current version from `SKILL.md`, falling back to `manifest.json`
- fetch latest release JSON
- skip if unchanged
- download assets to a temp dir
- verify downloads
- overwrite the target assets atomically
- update the version line in `SKILL.md`
- print a compact JSON summary

## Pitfalls

- The target CSS filename is `styles.css`, not `styles.cc`.
- Always use `manifest.json.version` as the fallback source when `SKILL.md` lacks a version line.
- Do not partially update only one or two asset files.
- Normalize release tags like `v2.0.2` to `2.0.2` before comparison.
- If GitHub API rate limits or returns malformed data, stop without modifying local assets.

## Verification

After running the script, verify by reading:
- `claudian-installer/SKILL.md`
- `claudian-installer/assets/manifest.json`

The versions must match.

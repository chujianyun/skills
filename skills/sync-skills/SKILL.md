---
name: sync-skills
description: Skills 同步助手。适用于用户想把本地 skill 目录、GitHub 仓库或 skillsmp.com 页面同步到多个 AI 编码工具目录时使用。会先识别来源类型，再列出目标目录并执行同步，且必须包含 ~/.agents/skills。
---

# Sync Skills

## Overview
Automatically sync skills from multiple sources to all installed AI coding tool directories. Lists all existing target directories for user confirmation before syncing.

> **🚨 CRITICAL REQUIREMENT:** All sync operations **MUST** include `~/.agents/skills` as the primary target. This universal skill directory is used by multiple AI coding tools and is **non-negotiable**. If the directory doesn't exist, it will be created automatically.

## When to Use

开始前先确认同步范围：
- 来源是什么（本地目录 / GitHub / skillsmp.com）
- 是同步到所有已存在目标，还是只同步到指定目录
- 是否允许覆盖已有同名 skill

如果用户没有特别指定，默认先列出目标目录并等待确认，不要直接覆盖。

```dot
digraph when_sync {
    "Need to sync skill?" [shape=diamond];
    "Source type?" [shape=diamond];
    "Local folder" [shape=box];
    "GitHub URL" [shape=box];
    "skillsmp.com URL" [shape=box];

    "Need to sync skill?" -> "Source type?";
    "Source type?" -> "Local folder" [label="Local path"];
    "Source type?" -> "GitHub URL" [label="github.com"];
    "Source type?" -> "skillsmp.com URL" [label="skillsmp.com"];
}
```

Use when:
- User provides local skill folder path
- User provides GitHub repository URL
- User provides skillsmp.com skill detail page URL
- Need to distribute skill across multiple AI tools

**How it works:**
1. Auto-detect source type from input
2. Prepare skill content based on source
3. Check all target directories (only existing ones)
4. **List existing targets for user confirmation**
5. Copy/clone to each confirmed target

## Target Directories

Checks these paths in order, only syncs if directory exists:

| Tool               | Project Level      | User Level                     |
| ------------------ | ------------------ | ------------------------------ |
| **Agents (Universal)** ⭐ | `.agents/skills`   | `~/.agents/skills` **[REQUIRED]** |
| Claude Code        | `.claude/skills`   | `~/.claude/skills`             |
| GitHub Copilot     | `.github/skills`   | `~/.copilot/skills`            |
| Google Antigravity | `.agents/skills`   | `~/.gemini/antigravity/skills` |
| Cursor             | `.cursor/skills`   | `~/.cursor/skills`             |
| OpenCode           | `.opencode/skill`  | `~/.config/opencode/skill`     |
| OpenAI Codex       | `.codex/skills`    | `~/.codex/skills`              |
| Gemini CLI         | `.gemini/skills`   | `~/.gemini/skills`             |
| Windsurf           | `.windsurf/skills` | `~/.codeium/windsurf/skills`   |
| Qwen Code          | `.qwen/skills`     | `~/.qwen/skills`               |
| Qoder              | `.qoder/skills`    | `~/.qoder/skills`              |
| OpenClaw           | `.openclaw/skills` | `~/.openclaw/skills`           |

> **⚠️ CRITICAL:** `~/.agents/skills` is a **MANDATORY** sync target. This universal skill directory is used by multiple AI coding tools and **MUST ALWAYS** be included in sync operations. Never skip this directory.

## Quick Reference

**Basic Usage:**
```bash
./sync-skill.sh <source>
```

**Examples:**
```bash
# Local folder
./sync-skill.sh /Users/user/skills/my-skill

# GitHub repository
./sync-skill.sh https://github.com/user/skill-repo

# skillsmp.com page
./sync-skill.sh https://skillsmp.com/skills/skill-name
```

### Source Type Detection

```bash
# Local folder
/Users/user/skills/my-skill
./skills/my-skill
~/skills/my-skill

# GitHub URL
https://github.com/user/skill-repo
https://github.com/user/skill-repo.git
git@github.com:user/skill-repo.git

# skillsmp.com URL
https://skillsmp.com/skills/skill-name
https://www.skillsmp.com/skills/skill-name
```

### Sync Commands by Source Type

**Local folder:**
```bash
# MANDATORY: Always sync to ~/.agents/skills first
cp -r /path/to/skill-name ~/.agents/skills/
cp -r /path/to/skill-name ~/.claude/skills/
cp -r /path/to/skill-name ~/.qoder/skills/
# ... for each existing target
```

**GitHub:**
```bash
# Clone to temp
git clone https://github.com/user/skill-repo.git /tmp/skill-sync

# Copy skill folder (might be in subdirectory)
# MANDATORY: Always sync to ~/.agents/skills first
cp -r /tmp/skill-sync/skill-name ~/.agents/skills/
cp -r /tmp/skill-sync/skill-name ~/.claude/skills/
# ... for each existing target

# Cleanup
rm -rf /tmp/skill-sync
```

**skillsmp.com:**
```bash
# Fetch page content
curl -s https://skillsmp.com/skills/skill-name > /tmp/skill-page.html

# Parse and download skill files
# Extract skill content from page
# Create skill directory structure
# Copy to each target
```

## Implementation

**Executable script:** See `sync-skill.sh` in this skill directory.

**Features:**
- Auto-detects source type (local, GitHub, skillsmp.com)
- Checks all target directories for existence
- **Lists existing targets and waits for user confirmation before syncing**
- Only syncs to user-confirmed directories
- Overwrites existing skills without prompting
- Cleans up temporary files after use
- Provides clear output with emoji indicators

**Exit codes:**
- 0: Success
- 1: Error (missing source, clone failure, etc.)

**Using from AI assistant:**
When user asks to sync a skill, invoke the script with appropriate source:

```bash
# User says: "Sync the skill at /path/to/my-skill"
./sync-skill.sh /path/to/my-skill

# User says: "Sync this GitHub repo: https://github.com/user/skill"
./sync-skill.sh https://github.com/user/skill
```

### Source Detection

```javascript
function detectSource(input) {
  // Local folder
  if (input.startsWith('/') || input.startsWith('./') || input.startsWith('~')) {
    return { type: 'local', path: input };
  }

  // GitHub URL
  if (input.includes('github.com')) {
    const url = input.replace(/\.git$/, '');
    return { type: 'github', url };
  }

  // skillsmp.com URL
  if (input.includes('skillsmp.com')) {
    return { type: 'skillsmp', url: input };
  }

  throw new Error(`Unknown source type: ${input}`);
}
```

### Directory Existence Check and Confirmation

```bash
# Check if directory exists and collect for confirmation
check_and_sync() {
  local source=$1
  local skill_name=$2

  # Array of all target directories
  # IMPORTANT: ~/.agents/skills is MANDATORY and must be first
  local targets=(
    "$HOME/.agents/skills"     # MANDATORY - Universal skill directory
    "$HOME/.claude/skills"
    "$HOME/.qoder/skills"
    "$HOME/.copilot/skills"
    # ... all others
  )

  local existing_targets=()

  # First pass: collect existing directories
  # MANDATORY: ~/.agents/skills must exist for sync to proceed
  local agents_dir="$HOME/.agents/skills"
  if [ ! -d "$agents_dir" ]; then
    echo "⚠️  Creating mandatory directory: $agents_dir"
    mkdir -p "$agents_dir"
  fi
  existing_targets+=("$agents_dir")

  # Collect other existing directories
  for target in "${targets[@]:1}"; do
    if [ -d "$target" ]; then
      existing_targets+=("$target")
    fi
  done

  # List existing targets and ask for confirmation
  if [ ${#existing_targets[@]} -eq 0 ]; then
    echo "❌ No target directories found. Please install at least one AI coding tool."
    exit 1
  fi

  echo "📋 Found ${#existing_targets[@]} existing target directory(s):"
  echo ""
  for i in "${!existing_targets[@]}"; do
    echo "  $((i+1)). ${existing_targets[$i]}"
  done
  echo ""
  read -p "✅ Sync to these directories? (y/N): " confirm

  if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo "❌ Sync cancelled by user."
    exit 1
  fi

  echo ""
  echo "🚀 Starting sync..."

  # Second pass: sync to confirmed targets
  for target in "${existing_targets[@]}"; do
    echo "  → Syncing to $target..."
    # Perform sync
  done
}
```

### GitHub Repository Handling

```bash
# Clone to temp directory
git clone https://github.com/user/repo.git /tmp/skill-sync-XXXXX

# Find skill folder (might be root or subdirectory)
if [ -f /tmp/skill-sync-XXXXX/SKILL.md ]; then
  skill_folder="/tmp/skill-sync-XXXXX"
elif [ -d /tmp/skill-sync-XXXXx/skills/* ]; then
  skill_folder="/tmp/skill-sync-XXXXx/skills/*"
fi

# Copy to each existing target
for target in "${existing_targets[@]}"; do
  cp -r "$skill_folder" "$target/"
done

# Cleanup
rm -rf /tmp/skill-sync-XXXXX
```

### skillsmp.com Page Handling

```bash
# Fetch page
url="https://skillsmp.com/skills/skill-name"
curl -s "$url" > /tmp/skill-page.html

# Extract skill name and files
skill_name=$(grep -o '<h1[^>]*>.*</h1>' /tmp/skill-page.html | sed 's/<[^>]*>//g')

# Download or extract skill content
# This depends on skillsmp.com's structure
# Might need to parse JSON, download files, etc.

# Create skill directory
mkdir -p "/tmp/$skill_name"

# Save content to SKILL.md
# ... parsing logic ...

# Sync to targets
for target in "${existing_targets[@]}"; do
  cp -r "/tmp/$skill_name" "$target/"
done
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| **⚠️ Skipping ~/.agents/sync** | **CRITICAL: NEVER skip this directory. It's MANDATORY for all sync operations** |
| Syncing without user confirmation | Always list targets and wait for `y/N` confirmation |
| Syncing to non-existent directories | Always check `-d` before copying (except ~/.agents/skills - create if missing) |
| Leaving temp files | Always cleanup `/tmp/skill-sync-*` after use |
| GitHub subdirectory confusion | Check for SKILL.md in root and subdirectories |
| Not handling .git suffix | Strip `.git` from URLs before cloning |
| skillsmp.com parsing failures | Inspect page structure first, adapt parsing |
| Forgetting to show skill name | Always display skill name in confirmation prompt |

> **🚨 CRITICAL:** The most serious mistake is **skipping ~/.agents/skills**. This directory is used by multiple AI coding tools and must always be included in every sync operation.

## Conflict Handling

**Policy: Always overwrite existing skills**

If a skill with the same name exists in a target directory:
- Overwrite without prompting
- Log what was overwritten: `"Overwriting existing skill at $target/$skill_name"`
- No backup (user should use git if they need history)

**Rationale:** Sync operations are expected to update content. If user wants to preserve local changes, they should manage version control separately.

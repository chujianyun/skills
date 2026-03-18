---
name: sync-skills
description: Skills 同步助手。将本地目录、GitHub 仓库或 skillsmp.com 页面的 skill 同步到用户选择的 AI 编码工具目录。使用 AskUserQuestion 选择目标（支持多选和自定义路径），展示同步计划后执行，同名 skill 会被覆盖。必须包含 ~/.agents/skills 作为同步目标。
---

# Sync Skills

将 skill 从本地目录、GitHub 仓库或 skillsmp.com 页面同步到多个 AI 编码工具目录。

> **🚨 核心要求**：
> 1. **必须包含 `~/.agents/skills`** 作为同步目标（不存在则自动创建）
> 2. **必须使用 AskUserQuestion** 让用户选择目标目录
> 3. **展示同步计划** 并等待用户最终确认
> 4. 同名 skill 直接覆盖，不单独提示

## When to Use

**触发场景：**
- 用户提供本地 skill 文件夹路径
- 用户提供 GitHub 仓库 URL
- 用户提供 skillsmp.com skill 页面 URL
- 需要将 skill 分发到多个 AI 工具目录

**工作流程：**
```
用户输入 → 识别来源类型 → 收集目标目录 → 用户选择目标 → 展示计划 → 用户确认 → 执行同步 → 报告结果
```

## Workflow

### Step 1: 识别来源类型

```bash
# 判断输入类型
if [[ "$input" =~ ^(/|~/|\./) ]]; then
    SOURCE_TYPE="local"
    SOURCE_PATH="$input"
elif [[ "$input" =~ github\.com ]]; then
    SOURCE_TYPE="github"
    SOURCE_URL="${input%.git}"
elif [[ "$input" =~ skillsmp\.com ]]; then
    SOURCE_TYPE="skillsmp"
    SOURCE_URL="$input"
else
    echo "❌ 无法识别来源类型"
    exit 1
fi
```

### Step 2: 收集目标目录

```bash
# 定义所有可能的目标目录
ALL_TARGETS=(
    "$HOME/.agents/skills"      # MANDATORY
    "$HOME/.claude/skills"
    "$HOME/.qoder/skills"
    "$HOME/.copilot/skills"
    "$HOME/.cursor/skills"
    "$HOME/.gemini/skills"
    "$HOME/.codex/skills"
    "$HOME/.config/opencode/skill"
    "$HOME/.codeium/windsurf/skills"
    "$HOME/.qwen/skills"
    "$HOME/.openclaw/skills"
)

# 确保 ~/.agents/skills 存在
mkdir -p "$HOME/.agents/skills"

# 收集已存在的目录
EXISTING_TARGETS=("$HOME/.agents/skills")
for target in "${ALL_TARGETS[@]:1}"; do
    [ -d "$target" ] && EXISTING_TARGETS+=("$target")
done
```

### Step 3: 使用 AskUserQuestion 让用户选择目标

```xml
<parameter name="questions">[
  {
    "question": "选择要同步到的目标目录（可多选）",
    "header": "目标目录",
    "multiSelect": true,
    "options": [
      {
        "label": "~/.agents/skills",
        "description": "通用技能目录（所有工具共用）",
        "markdown": "✅ **必选**"
      },
      {
        "label": "~/.claude/skills",
        "description": "Claude Code 技能目录"
      },
      {
        "label": "~/.qoder/skills",
        "description": "Qoder 技能目录"
      }
      // ... 根据实际存在的目录动态生成
    ]
  }
]</parameter>
```

**关键点：**
- `~/.agents/skills` 始终作为第一个选项并标记为必选
- 支持多选
- 用户可通过 "Other" 输入自定义路径

### Step 4: 准备 skill 内容

```bash
case "$SOURCE_TYPE" in
    local)
        SKILL_NAME=$(basename "$SOURCE_PATH")
        SKILL_SOURCE="$SOURCE_PATH"
        ;;
    github)
        TEMP_DIR=$(mktemp -d)
        git clone -q "$SOURCE_URL" "$TEMP_DIR"
        # 查找 SKILL.md 位置
        if [ -f "$TEMP_DIR/SKILL.md" ]; then
            SKILL_NAME=$(basename "$SOURCE_URL")
            SKILL_SOURCE="$TEMP_DIR"
        elif find "$TEMP_DIR" -name "SKILL.md" -quit; then
            SKILL_SOURCE=$(find "$TEMP_DIR" -name "SKILL.md" -printf "%h" -quit)
            SKILL_NAME=$(basename "$SKILL_SOURCE")
        fi
        ;;
    skillsmp)
        # 抓取并解析页面内容
        TEMP_DIR=$(mktemp -d)
        # ... 解析逻辑 ...
        ;;
esac
```

### Step 5: 展示同步计划并等待确认

**将同步计划以清晰格式展示给用户：**

```
📋 同步计划：

来源：$SOURCE_TYPE
Skill：$SKILL_NAME

目标目录（共 $SELECTED_COUNT 个）：
  1. ~/.agents/skills [新建]
  2. ~/.claude/skills [覆盖已有]
  3. ~/custom/skills [新建]

⚠️  同名 skill 将被直接覆盖，不会备份

确认执行？(Y/n)
```

### Step 6: 执行同步

```bash
for target in "${SELECTED_TARGETS[@]}"; do
    # 创建目标目录（如不存在）
    mkdir -p "$target"

    # 删除同名 skill
    if [ -d "$target/$SKILL_NAME" ]; then
        echo "  → 覆盖: $target/$SKILL_NAME"
        rm -rf "$target/$SKILL_NAME"
    else
        echo "  → 新建: $target/$SKILL_NAME"
    fi

    # 复制 skill
    cp -r "$SKILL_SOURCE" "$target/"
done

# 清理临时目录
[ -n "$TEMP_DIR" ] && rm -rf "$TEMP_DIR"
```

### Step 7: 报告结果

```
✅ 同步完成！

已成功同步到 $SUCCESS_COUNT 个目录：
  ✓ ~/.agents/skills
  ✓ ~/.claude/skills
  ✓ ~/custom/skills

❌ 失败 $FAIL_COUNT 个目录：
  ✗ ~/.qoder/skills (权限拒绝)
```

## Reference

### 支持的目标目录

| Tool | User Level |
|------|------------|
| **Agents (Universal)** ⭐ | `~/.agents/skills` **[必选]** |
| Claude Code | `~/.claude/skills` |
| GitHub Copilot | `~/.copilot/skills` |
| Cursor | `~/.cursor/skills` |
| Qoder | `~/.qoder/skills` |
| Gemini CLI | `~/.gemini/skills` |
| OpenAI Codex | `~/.codex/skills` |
| Windsurf | `~/.codeium/windsurf/skills` |
| Qwen Code | `~/.qwen/skills` |
| OpenClaw | `~/.openclaw/skills` |
| OpenCode | `~/.config/opencode/skill` |

### 来源类型识别

```bash
# 本地目录
/path/to/skill
./skill
~/skill

# GitHub URL
https://github.com/user/repo
https://github.com/user/repo.git
git@github.com:user/repo.git

# skillsmp.com URL
https://skillsmp.com/skills/skill-name
```

### AskUserQuestion 完整示例

```xml
<function_calls>
<invoke name="AskUserQuestion">
<parameter name="questions">[
  {
    "question": "选择要同步到的目标目录（可多选，或选择「其他」输入自定义路径）：",
    "header": "目标目录选择",
    "multiSelect": true,
    "options": [
      {
        "label": "~/.agents/skills",
        "description": "通用技能目录（所有工具共用）",
        "markdown": "✅ **必选** - 多个 AI 工具共享"
      },
      {
        "label": "~/.claude/skills",
        "description": "Claude Code 技能目录"
      },
      {
        "label": "~/.qoder/skills",
        "description": "Qoder 技能目录"
      }
    ]
  },
  {
    "question": "同名 skill 将被直接覆盖，是否继续？",
    "header": "覆盖策略确认",
    "multiSelect": false,
    "options": [
      {"label": "继续执行", "description": "直接覆盖同名 skill"},
      {"label": "取消操作", "description": "取消本次同步"}
    ]
  }
]</parameter>
</invoke>
</function_calls>
```

## Gotchas

| 错误 | 正确做法 |
|------|----------|
| 跳过 `~/.agents/skills` | **始终包含**，不存在则创建 |
| 不使用 AskUserQuestion | **必须使用**让用户选择目标 |
| 不展示同步计划 | **必须展示**并等待用户确认 |
| 同步到不存在的目录 | 先检查 `-d`，不存在则创建 |
| GitHub 仓库结构判断错误 | 先查找 SKILL.md 位置 |
| 忘记清理临时文件 | 始终 `rm -rf /tmp/skill-sync-*` |
| GitHub URL 带 .git 后缀 | 先用 `${url%.git}` 去除 |
| 不处理用户自定义路径 | 通过 "Other" 选项支持 |

> **🚨 最常见错误**：
> 1. 跳过 `~/.agents/skills` - **这是严重错误**
> 2. 不展示同步计划直接执行 - **用户体验差**

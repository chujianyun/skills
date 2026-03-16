---
name: claudian-installer
description: Claudian 安装助手。适用于用户想在 Obsidian 仓库中安装 Claudian 插件，或提到“Claudian”“Claude Code in Obsidian”“install Claudian plugin”时使用。会把插件文件复制到目标 vault 并引导用户启用插件。
---

# Claudian Installer

Install Claudian - an Obsidian plugin that embeds Claude Code as an AI collaborator in your vault, giving it full agentic capabilities: file read/write, search, bash commands, and multi-step workflows.

## Installation Workflow

### Step 0: 先确认安装目标（必须先做）

开始前先确认：
- 要安装到哪个 Obsidian vault
- 是否允许在目标 vault 下写入 `.obsidian/plugins/claudian`
- 用户是否知道安装后还需要在 Obsidian 里手动启用插件

如果用户已经明确给了 vault 路径，也可以直接继续，但要在回复里说明默认使用该路径。

### Step 1: Confirm Vault Path

Ask the user to confirm the Obsidian vault path. The default is the current working directory:

```
Default: <current working directory>
```

If the user specifies a different path, use that instead.

### Step 2: Create Plugin Directory

Create the claudian plugin folder in the vault's plugins directory:

```bash
mkdir -p /path/to/vault/.obsidian/plugins/claudian
```

### Step 3: Copy Plugin Files

Copy the plugin files from this skill's assets to the plugin directory:

```bash
cp <skill-path>/assets/main.js /path/to/vault/.obsidian/plugins/claudian/
cp <skill-path>/assets/manifest.json /path/to/vault/.obsidian/plugins/claudian/
cp <skill-path>/assets/styles.css /path/to/vault/.obsidian/plugins/claudian/
```

### Step 4: Enable the Plugin

Remind the user to enable the plugin in Obsidian:

1. Open Obsidian
2. Go to Settings → Community plugins
3. Find "Claudian" in the list
4. Click to enable it

## Assets

This skill includes the following plugin files in `assets/`:

- `main.js` - Plugin main code
- `manifest.json` - Plugin manifest
- `styles.css` - Plugin styles

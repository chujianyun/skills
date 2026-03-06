## Skills

This project provides WuMing's original AI assistant skills for personal learning and research purposes.

## Directory Structure

| Skill Name | Description |
|------------|-------------|
| [prompt-optimizer](skills/prompt-optimizer/SKILL.md) | Prompt engineering expert that helps users craft optimized prompts using many proven frameworks. Use when users want to optimize prompts, improve AI instructions, create better prompts for specific tasks, or need help selecting the best prompt framework for their use case. |
| [qoder-wiki](skills/qoder-wiki/SKILL.md) | Qoder official documentation knowledge base covering product overview, user guides, feature configuration, extensions, pricing, and troubleshooting. Use when users ask about Qoder topics such as installation, usage, features, pricing, shortcuts, MCP, Skills, Quest Mode, Repo Wiki, etc. |
| [openclaw-wiki](skills/openclaw-wiki/SKILL.md) | OpenClaw official documentation knowledge base for the multi-channel AI Agent gateway. Use when users ask about OpenClaw topics such as installation, Gateway, WhatsApp/Telegram/Discord channel connections, Sessions, Tools, troubleshooting, etc. |
| [sync-skills](skills/sync-skills/README.md) | Automatically sync skills from multiple sources (Local, GitHub, skillsmp.com) to all installed AI coding tool directories (Claude Code, Cursor, Windsurf, etc.). |
| [openclaw-ops](skills/openclaw-ops/SKILL.md) | OpenClaw operations assistant providing CLI command reference and troubleshooting workflows. Use when users need to run OpenClaw commands, diagnose service issues, fix Gateway or channel connection failures, view logs, or manage channels and agents. |
| [claudian-installer](skills/claudian-installer/SKILL.md) | Install Claudian Obsidian plugin which embeds Claude Code as an AI collaborator in your vault. Use when the user wants to install Claudian plugin to their Obsidian vault. |

## Usage

### Method 1: Install directly in Claude Code

1. Add plugin marketplace
```
/plugin marketplace add chujianyun/skills
```

2. Install skills
Install `prompt-optimizer`
```
/plugin install prompt-engineering-skills@chujianyun/skills
```

Install `qoder-wiki`
```
/plugin install qoder-wiki@chujianyun/skills
```

Install `openclaw-wiki`
```
/plugin install openclaw-wiki@chujianyun/skills
```

Install `sync-skills`
```
/plugin install sync-skills@chujianyun/skills
```

Install `claudian-installer`
```
/plugin install claudian-installer@chujianyun/skills
```

Install `openclaw-ops`
```
/plugin install openclaw-ops@chujianyun/skills
```
### Method 2: Using [openskills](https://github.com/numman-ali/openskills)

```
openskills install chujianyun/skills --global
```

## Contact

![](https://mingmingruyue-hz.oss-cn-hangzhou.aliyuncs.com/2025/20260121123942301.png)

## License

All Skill files in this project are licensed under [CC BY-NC-SA 4.0](LICENSE-CC-BY-NC-SA) (Attribution-NonCommercial-ShareAlike).

For commercial use, please contact the author for authorization.

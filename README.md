## Skills 
This project provides WuMing's（悟鸣） original Skills for personal learning and research purposes.

## Directory Structure

| Skill Name | Description |
|------------|-------------|
| [prompt-optimizer](skills/prompt-optimizer/SKILL.md) | Prompt engineering expert that helps users craft optimized prompts using many proven frameworks. Use when users want to optimize prompts, improve AI instructions, create better prompts for specific tasks, or need help selecting the best prompt framework for their use case. |
| [qoder-wiki](skills/qoder-wiki/SKILL.md) | Qoder 官方文档知识库，包含产品介绍、用户指南、功能配置、扩展能力、账户定价和故障排查。当用户询问 Qoder 相关问题（如安装、使用、功能、定价、快捷键、MCP、Skills、Quest Mode、Repo Wiki 等）时使用此 skill。 |
| [openclaw-wiki](skills/openclaw-wiki/SKILL.md) | OpenClaw 官方文档知识库，多渠道 AI Agent 网关。当用户询问 OpenClaw 相关问题（如安装、Gateway、WhatsApp/Telegram/Discord 等渠道连接、Sessions、Tools、故障排查等）时使用此 skill。 |
| [sync-skills](skills/sync-skills/README.md) | Automatically sync skills from multiple sources (Local, GitHub, skillsmp.com) to all installed AI coding tool directories (Claude Code, Cursor, Windsurf, etc.). |
| [openclaw-ops](skills/openclaw-ops/SKILL.md) | OpenClaw 运维助手，提供命令参考和故障排查修复流程。当用户需要执行 OpenClaw 命令、诊断服务问题、修复 Gateway 或渠道连接故障、查看日志、管理渠道或 Agent 时使用此 skill。 |
| [claudian-installer](skills/claudian-installer/SKILL.md) | Install Claudian Obsidian plugin which embeds Claude Code as an AI collaborator in your vault. Use when the user wants to install Claudian plugin to their Obsidian vault. |

## Usage

### Method 1: Install directly in Claude Code

1. Add plugin marketplace
```
/plugin marketplace add chujianyun/skills
```

2. Install skills
install `prompt-optimizer`
```
/plugin install prompt-engineering-skills@chujianyun/skills
```

install `qoder-wiki`
```
/plugin install qoder-wiki@chujianyun/skills
```

install `openclaw-wiki`
```
/plugin install openclaw-wiki@chujianyun/skills
```

install `sync-skills`
```
/plugin install sync-skills@chujianyun/skills
```

install `claudian-installer`
```
/plugin install claudian-installer@chujianyun/skills
```

install `openclaw-ops`
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

## Skills

This project provides WuMing's original AI assistant skills for personal learning and research purposes.

## Directory Structure

| Skill Name                                               | Description                                                                                                                                                                                                                                                                                    |
| -------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [prompt-optimizer](skills/prompt-optimizer/SKILL.md)     | Prompt engineering expert that helps users craft optimized prompts using many proven frameworks. Use when users want to optimize prompts, improve AI instructions, create better prompts for specific tasks, or need help selecting the best prompt framework for their use case.              |
| [qoder-wiki](skills/qoder-wiki/SKILL.md)                 | Qoder official documentation knowledge base covering product overview, user guides, feature configuration, extensions, pricing, and troubleshooting. Use when users ask about Qoder topics such as installation, usage, features, pricing, shortcuts, MCP, Skills, Quest Mode, Repo Wiki, etc. |
| [openclaw-wiki](skills/openclaw-wiki/SKILL.md)           | OpenClaw official documentation knowledge base for the multi-channel AI Agent gateway. Use when users ask about OpenClaw topics such as installation, Gateway, WhatsApp/Telegram/Discord channel connections, Sessions, Tools, troubleshooting, etc.                                           |
| [sync-skills](skills/sync-skills/SKILL.md)              | Automatically sync skills from multiple sources (Local, GitHub, skillsmp.com) to all installed AI coding tool directories. **MUST include `~/.agents/skills` as mandatory target** for universal compatibility across AI coding tools. Supports Claude Code, GitHub Copilot, Cursor, Windsurf, and more.                                                                                                                               |
| [openclaw-ops](skills/openclaw-ops/SKILL.md)             | OpenClaw operations assistant providing CLI command reference and troubleshooting workflows. Use when users need to run OpenClaw commands, diagnose service issues, fix Gateway or channel connection failures, view logs, or manage channels and agents.                                      |
| [claudian-installer](skills/claudian-installer/SKILL.md) | Install Claudian Obsidian plugin which embeds Claude Code as an AI collaborator in your vault. Use when the user wants to install Claudian plugin to their Obsidian vault.                                                                                                                     |
| [claude-config-advisor](skills/claude-config-advisor/SKILL.md) | Review or design Claude Code project configuration. Use when the user asks about `.claude`, `CLAUDE.md`, Claude configuration files, structural quality, or needs guidance on which files to create. |
| [copaw-ops](skills/copaw-ops/SKILL.md)                   | CoPaw 运维助手，提供服务启停、配置管理、模型与渠道管理、定时任务巡检、日志排查和故障恢复流程。当用户提到 copaw 运维、服务无响应、渠道断连、MCP 失败、模型调用失败、cron 不执行、Docker 部署或重置恢复时使用此技能。                                                                                                                                                                       |
| [skill-optimizer](skills/skill-optimizer/SKILL.md)       | 优化和重构现有 skill。用于检查目标 skill 的触发描述、SKILL.md 工作流、确认门槛、渐进式披露，以及 references/scripts/assets 的组织方式。当用户提到”优化 skill””检查 skill 质量””改进某个 skill””重构技能说明”时使用。                                                                                                  |
| [github-code-interpreter](skills/github-code-interpreter/SKILL.md) | GitHub 源码解读助手。当用户提供 GitHub 仓库链接并希望解读源码、理解原理、生成学习报告或快速上手项目时使用。会在 working 目录下创建解读文件夹，生成源码解读报告和快速上手文档两份文档，报告包含 Mermaid 架构图，并安排 1 小时后的复查完善。 **注意：此技能默认使用 `~/Documents/coding/github` 和 `~/Documents/working` 目录，建议根据个人习惯调整。** |
| [paper-interpreter](skills/paper-interpreter/SKILL.md)   | 论文解读助手。当用户发送 arXiv 论文链接并希望下载论文、解读论文、生成读书笔记或详细报告时使用。会在指定目录创建论文文件夹，下载 PDF 和 TeX Source，生成中文 Markdown 解读报告（含 Mermaid 图），并安排 1 小时后和 2 小时后的自动复查任务。 **注意：此技能默认使用 `~/Documents/working/papers` 目录，建议根据个人习惯调整。** |

## Usage

**⚠️ Important Note About Default Directories**

Some skills in this collection use default directory paths for storing files and working data. **Before using these skills, you should customize them to match your preferred directory structure:**

- **github-code-interpreter**: Default paths are `~/Documents/coding/github` (for repositories) and `~/Documents/working` (for analysis reports)
- **paper-interpreter**: Default path is `~/Documents/working/papers` (for papers and reports)

To customize these paths, edit the respective `SKILL.md` files and update the directory references in the workflow sections. This ensures the skills work with your existing file organization.

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

Install `copaw-ops`
```
/plugin install copaw-ops@chujianyun/skills
```

Install `skill-optimizer`
```
/plugin install skill-optimizer@chujianyun/skills
```

Install `claude-config-advisor`
```
/plugin install claude-config-advisor@chujianyun/skills
```

Install `github-code-interpreter`
```
/plugin install github-code-interpreter@chujianyun/skills
```

Install `paper-interpreter`
```
/plugin install paper-interpreter@chujianyun/skills
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

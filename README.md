## 技能集合

本项目提供悟鸣（WuMing）原创的 AI 辅助技能，用于个人学习和研究目的。

## 目录结构

| 技能名称 | 描述 |
|----------|------|
| [prompt-optimizer](skills/prompt-optimizer/SKILL.md) | Prompt 工程专家，帮助用户使用多种经过验证的框架来优化提示词。当用户想要优化提示词、改进 AI 指令、为特定任务创建更好的提示词，或需要帮助选择最适合其用例的提示词框架时使用。 |
| [qoder-wiki](skills/qoder-wiki/SKILL.md) | Qoder 官方文档知识库，包含产品介绍、用户指南、功能配置、扩展能力、账户定价和故障排查。当用户询问 Qoder 相关问题（如安装、使用、功能、定价、快捷键、MCP、Skills、Quest Mode、Repo Wiki 等）时使用此 skill。 |
| [openclaw-wiki](skills/openclaw-wiki/SKILL.md) | OpenClaw 官方文档知识库，多渠道 AI Agent 网关。当用户询问 OpenClaw 相关问题（如安装、Gateway、WhatsApp/Telegram/Discord 等渠道连接、Sessions、Tools、故障排查等）时使用此 skill。 |
| [sync-skills](skills/sync-skills/README.md) | 自动将技能从多个来源（本地、GitHub、skillsmp.com）同步到所有已安装的 AI 编程工具目录（Claude Code、Cursor、Windsurf 等）。 |
| [openclaw-ops](skills/openclaw-ops/SKILL.md) | OpenClaw 运维助手，提供命令参考和故障排查修复流程。当用户需要执行 OpenClaw 命令、诊断服务问题、修复 Gateway 或渠道连接故障、查看日志、管理渠道或 Agent 时使用此 skill。 |
| [claudian-installer](skills/claudian-installer/SKILL.md) | 安装 Claudian Obsidian 插件，将 Claude Code 作为 AI 协作者嵌入到你的 Obsidian 知识库中。当用户想要将 Claudian 插件安装到他们的 Obsidian 知识库时使用。 |

## 使用方法

### 方法 1：在 Claude Code 中直接安装

1. 添加插件市场
```
/plugin marketplace add chujianyun/skills
```

2. 安装技能
安装 `prompt-optimizer`
```
/plugin install prompt-engineering-skills@chujianyun/skills
```

安装 `qoder-wiki`
```
/plugin install qoder-wiki@chujianyun/skills
```

安装 `openclaw-wiki`
```
/plugin install openclaw-wiki@chujianyun/skills
```

安装 `sync-skills`
```
/plugin install sync-skills@chujianyun/skills
```

安装 `claudian-installer`
```
/plugin install claudian-installer@chujianyun/skills
```

安装 `openclaw-ops`
```
/plugin install openclaw-ops@chujianyun/skills
```
### 方法 2：使用 [openskills](https://github.com/numman-ali/openskills)

```
openskills install chujianyun/skills --global
```

## 联系方式

![](https://mingmingruyue-hz.oss-cn-hangzhou.aliyuncs.com/2025/20260121123942301.png)

## 许可证

本项目中的所有技能文件均采用 [CC BY-NC-SA 4.0](LICENSE-CC-BY-NC-SA)（署名-非商业性使用-相同方式共享）许可证。

商业用途请联系作者获取授权。

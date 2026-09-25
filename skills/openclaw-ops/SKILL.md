---
name: openclaw-ops
description: OpenClaw 运维助手。用于用户提到 OpenClaw、小龙虾、gateway、渠道连接、消息发送失败、服务不可达、日志排查、渠道或 Agent 管理时使用。优先执行状态检查与故障分流；涉及重启、修复、更新、配置变更等高影响操作时，先向用户说明再执行。
---

# OpenClaw Ops

OpenClaw 是一个多渠道 AI Agent 网关，支持 WhatsApp、Telegram、Discord 等消息平台。本技能提供运维所需的命令参考和故障排查能力。

## 设计模式

本 skill 主要采用：
- **Tool Wrapper**：提供 OpenClaw 命令、诊断路径和参考资料
- **Runbook / Pipeline**：按“状态检查 → 问题分流 → 选择修复动作 → 验证结果”的顺序执行
- **Reviewer（轻度）**：先判断问题类型，再决定是否需要修复

## Gotchas

- 不要一上来就重启或自动修复，先看状态和问题类型
- 涉及重启、更新、repair、配置修改等高影响操作时，要先向用户说明再执行
- 不要编造 OpenClaw CLI 子命令；不确定时先查文档或本地参考
- 不要把渠道问题、模型问题、gateway 问题混成一个锅端命令
- 修完后一定要回到健康检查，不要停在“已经执行了修复命令”

## 标准诊断流程

当用户报告 OpenClaw 问题时，按以下步骤执行：

### 0. 先判断是否需要确认

以下操作默认可以直接做：
- `openclaw status`
- `openclaw channels status --probe`
- `openclaw logs --limit 200`
- `openclaw health`

以下操作属于高影响动作，执行前应先向用户说明：
- `openclaw doctor --repair`
- `openclaw doctor --repair --force`
- `openclaw gateway restart`
- `openclaw update`
- 任何明确会修改配置、重连渠道、重置状态的命令

```bash
# 1. 快速状态检查
openclaw status

# 2. 深度渠道探测
openclaw channels status --probe

# 3. 自动修复
openclaw doctor --repair

# 4. 验证健康状态
openclaw health
```

## 问题分类处理

根据问题类型选择对应处理路径：

**服务无法启动** → `openclaw gateway status` → `openclaw doctor --repair` → `openclaw gateway restart`

**渠道连接失败** → `openclaw channels status --probe` → `openclaw channels login --channel <name>` → 查看渠道日志

**消息发送失败** → `openclaw logs --limit 200` → 检查渠道状态 → 验证目标格式

**性能问题** → `openclaw status --usage` → 查看系统日志 → 检查资源使用

**配置查询** → 查阅 [openclaw_commands.md](references/openclaw_commands.md) 对应章节

## 修复策略

- **首选：** `openclaw doctor --repair` 自动修复
- **Gateway 未运行：** `openclaw gateway restart`
- **修复后仍不健康：** `openclaw doctor --repair --force`
- **更新后修复：** `openclaw update` → `openclaw doctor` → `openclaw health`

## 成功判断标准

- `openclaw health` 返回无错误
- `openclaw channels status --probe` 所有渠道状态正常
- `openclaw status` 显示 gateway 可达

## 最常用命令速查

| 命令 | 用途 |
|------|------|
| `openclaw status` | 查看整体状态 |
| `openclaw health` | 健康检查 |
| `openclaw doctor --repair` | 自动修复 |
| `openclaw gateway restart` | 重启服务 |
| `openclaw channels status --probe` | 检查渠道 |
| `openclaw logs --limit 200` | 查看日志 |

## macOS 注意事项

- Gateway 由 OpenClaw Mac app 管理，不要用 tmux 手动启动
- 检查 launchd 环境变量覆盖：`launchctl getenv OPENCLAW_GATEWAY_TOKEN`
- 系统日志：`/tmp/openclaw/openclaw-YYYY-MM-DD.log`
- 服务日志：`~/.openclaw/logs/gateway.log`
- macOS 错误日志：`./scripts/clawlog.sh -e`

## 详细参考

- 完整命令手册：[openclaw_commands.md](references/openclaw_commands.md)
- 故障排查与修复流程：[openclaw_fix.md](references/openclaw_fix.md)

## 汇报规范

向用户汇报时应包含：发现的问题、执行的操作、当前的状态、后续建议。

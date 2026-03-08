---
name: copaw-ops
description: CoPaw 运维助手，提供服务启停、配置管理、模型与渠道管理、定时任务巡检、日志排查和故障恢复流程。当用户提到 copaw 运维、服务无响应、渠道断连、MCP 失败、模型调用失败、cron 不执行、Docker 部署或重置恢复时使用此技能。
---

# CoPaw Ops

本技能用于 CoPaw 的日常巡检、故障定位与恢复操作，优先给出可执行命令和最短恢复路径。

## 触发场景

- 用户要求排查 CoPaw 服务不可用、响应慢、报错。
- 用户要求查看或修改 CoPaw 配置、模型、渠道、定时任务、会话。
- 用户要求执行 CoPaw 重启、重载、清理、重置。
- 用户要求 Docker / supervisord 场景下的 CoPaw 运维操作。

## 标准诊断流程

当用户报告 CoPaw 故障时，按以下最小闭环执行：

```bash
# 1) 基础状态
copaw daemon status
copaw daemon version

# 2) 关键运行面检查
copaw models list
copaw channels list
copaw cron list

# 3) 最近日志
copaw daemon logs -n 100

# 4) 针对性恢复（按症状）
copaw daemon reload-config
```

若在聊天渠道中可直接执行 Magic Commands，则优先：

```text
/status
/restart
/daemon logs 50
```

## 故障分流

- 服务无响应：先 `/restart`，再 `copaw daemon reload-config`，仍失败再按部署方式重启进程。
- 配置错误：`copaw daemon reload-config` + `copaw daemon logs -n 200`，必要时 `copaw init --force`。
- 渠道断连：`copaw channels list` -> `copaw channels config` -> `/daemon restart`。
- 模型调用失败：`copaw models list` -> `copaw models config-key <provider>` -> `copaw models set-llm`。
- 定时任务不执行：`copaw cron state <job_id>` -> `copaw cron resume <job_id>` -> `copaw cron run <job_id>`。
- 上下文爆满：`/compact` 或 `/new`，并用 `/history` 验证 Token 使用。

## 成功判定标准

- `copaw daemon status` 正常，且无关键报错。
- `copaw channels list` 渠道状态符合预期。
- `copaw models list` 当前模型可用。
- `copaw cron list` / `copaw cron state <job_id>` 显示任务正常。
- 最近日志未持续出现相同错误。

## 按需加载参考

- 常用命令与巡检清单：`references/copaw_commands.md`
- 故障恢复策略：`references/copaw_recovery.md`

## 回复模板

向用户汇报时使用以下结构：

1. 现象：用户侧症状 + 影响范围
2. 诊断：执行过的命令与关键输出
3. 处理：已执行恢复动作
4. 结果：当前状态是否恢复
5. 建议：后续预防或观察项


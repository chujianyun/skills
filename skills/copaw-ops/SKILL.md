---
name: copaw-ops
description: CoPaw 运维助手。用于用户提到 copaw 运维、服务无响应、渠道断连、MCP 失败、模型调用失败、cron 不执行、Docker 部署、重载、重启或重置恢复时使用。优先执行状态检查与故障分流；涉及重启、重载、重置、配置修改等高影响动作时，先向用户说明再执行。
---

# CoPaw Ops

本技能用于 CoPaw 的日常巡检、故障定位与恢复操作，优先给出可执行命令和最短恢复路径。

## 设计模式

本 skill 主要采用：
- **Tool Wrapper**：提供 CoPaw 命令、诊断路径和参考资料
- **Runbook / Pipeline**：按"状态检查 → 问题分流 → 选择修复动作 → 验证结果"的顺序执行
- **Reviewer（轻度）**：先判断问题类型，再决定是否需要恢复动作

## Gotchas

- 不要一上来就重启或重置，先看状态和症状
- 涉及重启、reload、init --force、重置、配置修改等高影响动作时，要先向用户说明再执行
- 不要把模型问题、渠道问题、daemon 问题、cron 问题混成一个通用修复命令
- 不要假装 Magic Commands 在所有环境都可用，要先判断当前渠道/环境是否支持
- 修复后一定要回到状态检查，不要停在"命令执行了"
- **多 agent 环境**：检查和修复时注意指定正确的 `--agent-id`（默认：default）

## 触发场景

- 用户要求排查 CoPaw 服务不可用、响应慢、报错。
- 用户要求查看或修改 CoPaw 配置、模型、渠道、定时任务、会话。
- 用户要求执行 CoPaw 重启、重载、清理、重置。
- 用户要求 Docker / supervisord 场景下的 CoPaw 运维操作。
- 用户要求排查多 agent 环境下的特定 agent 问题。

## 标准诊断流程

### 0. 先判断是否需要确认

以下操作默认可以直接做：
- `copaw daemon status`
- `copaw daemon version`
- `copaw agent list`（新增）
- `copaw workspace list`（新增）
- `copaw models list [--agent-id <id>]`
- `copaw channels list [--agent-id <id>]`
- `copaw cron list [--agent-id <id>]`
- `copaw daemon logs -n 100`

以下操作属于高影响动作，执行前应先向用户说明：
- `copaw daemon reload-config`
- `/restart`
- `/daemon restart`
- `copaw init --force`
- `copaw workspace delete <id>`
- 任何明确会修改配置、重连渠道、重置状态的命令

### 1. 基础状态检查

当用户报告 CoPaw 故障时，按以下最小闭环执行：

```bash
# 1) 基础状态（全局）
copaw daemon status
copaw daemon version

# 2) 多 agent 检查（新增）
copaw agent list              # 列出所有 agent
copaw workspace list          # 列出所有工作区

# 3) 特定 agent 检查（指定 --agent-id）
copaw models list --agent-id <id>
copaw channels list --agent-id <id>
copaw cron list --agent-id <id>

# 4) 最近日志
copaw daemon logs -n 100

# 5) 针对性恢复（按症状）
copaw daemon reload-config
```

### 2. 工作区检查（新增）

```bash
# 检查工作区结构
ls -la ~/.copaw/workspaces/

# 检查特定 agent 的工作区
ls -la ~/.copaw/workspaces/<agent-id>/

# 检查配置文件
cat ~/.copaw/workspaces/<agent-id>/agent.json

# 检查内置 skills
ls -la ~/.copaw/workspaces/<agent-id>/active_skills/

# 检查向量数据库（如果启用）
ls -la ~/.copaw/workspaces/<agent-id>/file_store/
```

若在聊天渠道中可直接执行 Magic Commands，则优先：

```text
/status
/restart
/daemon logs 50
```

## 故障分流

### 服务无响应
1. 先 `/restart`，再 `copaw daemon reload-config`
2. 检查工作区是否正常：`ls -la ~/.copaw/workspaces/`
3. 检查 agent 是否启动：`copaw agent list`
4. 仍失败再按部署方式重启进程

### 配置错误
1. `copaw daemon reload-config` + `copaw daemon logs -n 200`
2. 检查 agent.json 配置：`cat ~/.copaw/workspaces/<id>/agent.json`
3. 必要时 `copaw init --force`

### 渠道断连
1. `copaw channels list --agent-id <id>` 检查配置
2. `copaw channels config <channel> --agent-id <id>` 查看详细配置
3. 针对特定渠道：
   - **钉钉**：检查 `client_id`, `client_secret`, `robot_code`；使用 `dingtalk_channel` skill 自动连接
   - **飞书**：检查 `app_id`, `app_secret`, `encrypt_key`
   - **QQ**：检查 `app_id`, `client_secret`
4. `/daemon restart` 重启服务

### 模型调用失败
1. `copaw models list --agent-id <id>` 检查当前模型
2. `copaw models config-key <provider> --agent-id <id>` 检查 API key
3. `copaw models set-llm --agent-id <id>` 切换模型

### 定时任务不执行
1. `copaw cron list --agent-id <id>` 列出所有任务
2. `copaw cron state <job_id> --agent-id <id>` 检查任务状态
3. 检查 jobs.json：`cat ~/.copaw/workspaces/<id>/jobs.json`
4. `copaw cron resume <job_id> --agent-id <id>` 恢复任务
5. `copaw cron run <job_id> --agent-id <id>` 手动执行测试

### 内置 Skills 故障（新增）
1. 检查 skill 是否存在：`ls ~/.copaw/workspaces/<id>/active_skills/`
2. 检查依赖项：
   - Office skills（docx/pptx/xlsx）：检查 Python 依赖库
   - PDF skill：检查 PDF 工具（pdfplumber 等）
   - himalaya skill：检查邮件配置
   - browser_visible skill：检查浏览器连接

### 上下文爆满
1. `/compact` 或 `/new`
2. 用 `/history` 验证 Token 使用

### 钉钉渠道特殊处理（新增）
1. 检查配置：
   ```bash
   copaw channels config dingtalk --agent-id <id>
   ```
2. 检查必填字段：
   - `client_id`
   - `client_secret`
   - `robot_code`（可选）
3. 使用自动连接 skill：
   ```bash
   # 需要可视化浏览器
   copaw skills run dingtalk_channel --agent-id <id>
   ```
4. 检查机器人是否发布（重要！）
5. 检查 Stream 模式配置

## 成功判定标准

- `copaw daemon status` 正常，且无关键报错。
- `copaw agent list` 显示所有 agent 正常。
- `copaw channels list --agent-id <id>` 渠道状态符合预期。
- `copaw models list --agent-id <id>` 当前模型可用。
- `copaw cron list --agent-id <id>` / `copaw cron state <job_id>` 显示任务正常。
- 工作区结构完整：`agent.json` 存在，`active_skills/` 存在。
- 最近日志未持续出现相同错误。

## 按需加载参考

- 常用命令与巡检清单：`references/copaw_commands.md`
- 故障恢复策略：`references/copaw_recovery.md`
- 多 agent 架构说明：`references/multi_agent.md`（新增）
- 内置 skills 说明：`references/builtin_skills.md`（新增）

## 回复模板

向用户汇报时使用以下结构：

1. **现象**：用户侧症状 + 影响范围
2. **诊断**：执行过的命令与关键输出（注明 agent-id）
3. **处理**：已执行恢复动作
4. **结果**：当前状态是否恢复
5. **建议**：后续预防或观察项

## 多 Agent 环境注意事项

1. **默认 agent**：所有命令默认操作 `default` agent
2. **指定 agent**：使用 `--agent-id <id>` 参数指定
3. **工作区隔离**：每个 agent 有独立的工作区、配置、skills
4. **批量操作**：暂不支持批量操作所有 agent，需要逐个检查
5. **日志查看**：daemon 日志包含所有 agent，需要过滤查看

## 常见错误

### Agent 不存在
```
Error: Agent 'xxx' not found
```
**解决**：
1. 检查 agent 列表：`copaw agent list`
2. 创建新 agent：`copaw workspace create <id>`

### 工作区损坏
```
Error: Workspace directory not found
```
**解决**：
1. 检查工作区：`ls -la ~/.copaw/workspaces/`
2. 重新初始化：`copaw init --force`

### 内置 Skill 加载失败
```
Error: Failed to load skill 'xxx'
```
**解决**：
1. 检查 skill 目录：`ls ~/.copaw/workspaces/<id>/active_skills/`
2. 检查依赖项：`pip list`
3. 查看详细错误：`copaw daemon logs -n 200`

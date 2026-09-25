# CoPaw 多 Agent 架构

## 概述

CoPaw 从单 agent 架构升级为多 agent 架构（2026-03-18），支持同时运行多个独立的 agent 实例，每个 agent 有独立的工作区、配置、skills 和记忆。

## 架构说明

### 工作区结构

```
~/.copaw/
├── config.json              # 根配置（多 agent 架构）
├── copaw.log                # 全局日志
├── bin/
│   └── copaw                # CLI wrapper 脚本
└── workspaces/
    ├── default/             # 默认 agent 工作区
    │   ├── agent.json       # Agent 配置
    │   ├── active_skills/   # 内置 skills
    │   ├── file_store/      # 向量数据库（可选）
    │   ├── chats.json       # 聊天记录
    │   ├── jobs.json        # 定时任务
    │   ├── AGENTS.md        # Agent 说明
    │   ├── MEMORY.md        # 记忆
    │   ├── HEARTBEAT.md     # 心跳检查
    │   └── memory/          # 记忆目录
    └── <agent-id>/          # 其他 agent 工作区
        └── ...
```

### 配置层次

1. **根配置**：`~/.copaw/config.json`
   - 定义所有 agent 的共享配置
   - 管理多 agent 架构

2. **Agent 配置**：`~/.copaw/workspaces/<agent-id>/agent.json`
   - 每个 agent 的独立配置
   - 渠道、模型、skills 等设置

## Agent 管理

### 列出所有 Agent

```bash
copaw agent list
```

输出示例：
```
Agent ID    Name              Status    Workspace
default     Default Agent     running   ~/.copaw/workspaces/default
agent-2     Secondary Agent   running   ~/.copaw/workspaces/agent-2
```

### 创建新 Agent

```bash
# 创建新工作区
copaw workspace create <agent-id>

# 示例
copaw workspace create agent-2
```

### 删除 Agent

```bash
# 删除工作区（高影响操作）
copaw workspace delete <agent-id>

# 示例
copaw workspace delete agent-2
```

**注意**：删除工作区会清除所有数据（聊天记录、定时任务、记忆等），需谨慎操作。

### 验证工作区

```bash
# 检查工作区状态
copaw workspace validate <agent-id>

# 示例
copaw workspace validate default
```

## 多 Agent 操作

### 指定 Agent

几乎所有命令都支持 `--agent-id` 参数：

```bash
# 模型管理
copaw models list --agent-id <id>
copaw models set-llm --agent-id <id>

# 渠道管理
copaw channels list --agent-id <id>
copaw channels config dingtalk --agent-id <id>

# 定时任务
copaw cron list --agent-id <id>
copaw cron create --agent-id <id> ...

# 会话管理
copaw chats list --agent-id <id>
```

### 默认 Agent

如果不指定 `--agent-id`，默认操作 `default` agent：

```bash
# 这两个命令等价
copaw models list
copaw models list --agent-id default
```

### 批量操作

目前不支持批量操作所有 agent，需要逐个检查：

```bash
# 检查所有 agent 的模型
copaw agent list | awk '{print $1}' | while read id; do
  echo "=== Agent: $id ==="
  copaw models list --agent-id $id
done
```

## 配置迁移

### 从单 agent 迁移

CoPaw 会自动迁移旧配置：

```
2026-03-18 09:04:13 | Checking for legacy config migration...
2026-03-18 09:04:13 | ============================================================
2026-03-18 09:04:13 | Migrating legacy config to multi-agent structure...
2026-03-18 09:04:13 | ============================================================
2026-03-18 09:04:13 | Created default agent workspace: /Users/liuwangyang/.copaw/workspaces/default
2026-03-18 09:04:13 | Created agent config: /Users/liuwangyang/.copaw/workspaces/default/agent.json
2026-03-18 09:04:13 | Updated root config.json to multi-agent structure
2026-03-18 09:04:13 | ============================================================
2026-03-18 09:04:13 | Migration completed successfully!
2026-03-18 09:04:13 |   Default agent workspace: /Users/liuwangyang/.copaw/workspaces/default
2026-03-18 09:04:13 |   Default agent config: /Users/liuwangyang/.copaw/workspaces/default/agent.json
2026-03-18 09:04:13 | ============================================================
```

### 手动迁移

如果自动迁移失败，可以手动迁移：

1. 备份旧配置：
   ```bash
   cp -r ~/.copaw ~/.copaw.backup
   ```

2. 创建新工作区：
   ```bash
   copaw workspace create default
   ```

3. 复制配置：
   ```bash
   cp ~/.copaw.backup/config.json ~/.copaw/workspaces/default/agent.json
   ```

4. 重启服务：
   ```bash
   copaw daemon reload-config
   ```

## 工作区检查

### 检查工作区结构

```bash
# 列出所有工作区
ls -la ~/.copaw/workspaces/

# 检查特定工作区
ls -la ~/.copaw/workspaces/<agent-id>/
```

### 检查配置文件

```bash
# 查看 agent 配置
cat ~/.copaw/workspaces/<agent-id>/agent.json

# 查看定时任务
cat ~/.copaw/workspaces/<agent-id>/jobs.json

# 查看聊天记录
cat ~/.copaw/workspaces/<agent-id>/chats.json
```

### 检查内置 Skills

```bash
# 列出内置 skills
ls -la ~/.copaw/workspaces/<agent-id>/active_skills/

# 查看特定 skill
cat ~/.copaw/workspaces/<agent-id>/active_skills/cron/SKILL.md
```

### 检查向量数据库

```bash
# 检查向量数据库（如果启用）
ls -la ~/.copaw/workspaces/<agent-id>/file_store/
```

## 常见问题

### Agent 不存在

**错误**：
```
Error: Agent 'xxx' not found
```

**解决**：
1. 检查 agent 列表：`copaw agent list`
2. 创建新 agent：`copaw workspace create <id>`
3. 检查拼写错误

### 工作区损坏

**错误**：
```
Error: Workspace directory not found
```

**解决**：
1. 检查工作区：`ls -la ~/.copaw/workspaces/`
2. 重新初始化：`copaw init --force`
3. 从备份恢复：`cp -r ~/.copaw.backup/workspaces/<id> ~/.copaw/workspaces/`

### 配置冲突

**错误**：
```
Error: Configuration conflict
```

**解决**：
1. 检查 agent.json 格式：`cat ~/.copaw/workspaces/<id>/agent.json`
2. 验证 JSON 格式：`python -m json.tool ~/.copaw/workspaces/<id>/agent.json`
3. 重置配置：`copaw init --force`

### Skills 加载失败

**错误**：
```
Error: Failed to load skill 'xxx'
```

**解决**：
1. 检查 skill 目录：`ls ~/.copaw/workspaces/<id>/active_skills/`
2. 检查依赖项：`pip list`
3. 查看详细错误：`copaw daemon logs -n 200`

## 日志查看

### 全局日志

```bash
# 查看所有 agent 的日志
copaw daemon logs -n 100

# 过滤特定 agent 的日志
copaw daemon logs -n 100 | grep "agent-2"
```

### 工作区日志

```bash
# 查看特定工作区的日志
tail -f ~/.copaw/workspaces/<agent-id>/copaw.log
```

## 性能优化

### 资源隔离

每个 agent 独立运行，资源隔离：
- 独立的内存空间
- 独立的向量数据库
- 独立的聊天记录

### 并发控制

默认情况下，所有 agent 共享同一个 daemon 进程。如果需要更高的并发性能：

1. 增加工作线程：
   ```bash
   copaw app --workers 4
   ```

2. 使用多进程部署（Docker）：
   ```bash
   docker run -d -p 8088:8088 copaw:latest
   docker run -d -p 8089:8088 copaw:latest
   ```

## 最佳实践

### Agent 命名

- 使用有意义的名称：`production`, `staging`, `dev`
- 避免特殊字符：只使用字母、数字、下划线、连字符
- 保持简短：建议不超过 20 个字符

### 配置管理

1. **独立配置**：每个 agent 有独立的配置文件
2. **版本控制**：将 agent.json 加入 Git 管理
3. **环境隔离**：不同环境使用不同的 agent

### 监控和告警

1. **定期检查**：使用 heartbeat 定期检查所有 agent 状态
2. **日志监控**：监控 daemon 日志，及时发现异常
3. **资源监控**：监控 CPU、内存、磁盘使用情况

### 备份策略

1. **定期备份**：定期备份工作区目录
2. **配置备份**：备份所有 agent.json 文件
3. **数据备份**：备份向量数据库和聊天记录

## 参考资料

- [CoPaw 命令速查](copaw_commands.md)
- [故障恢复策略](copaw_recovery.md)
- [内置 Skills 说明](builtin_skills.md)

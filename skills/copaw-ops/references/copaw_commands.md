# CoPaw 命令速查

## 1. 服务启停与状态

```bash
copaw app
copaw app --host 0.0.0.0 --port 9090
copaw app --reload
copaw app --workers 4
copaw app --log-level debug

copaw daemon status
copaw daemon version
copaw daemon logs -n 100
copaw daemon reload-config
```

Magic Commands（聊天中）：

```text
/status
/restart
/daemon reload-config
/daemon logs 50
```

## 2. 多 Agent 管理（新增）

```bash
# 列出所有 agent
copaw agent list

# 列出所有工作区
copaw workspace list

# 创建新工作区
copaw workspace create <agent-id>

# 删除工作区（高影响操作）
copaw workspace delete <agent-id>

# 检查工作区状态
copaw workspace validate <agent-id>
```

**多 agent 参数说明**：
- `--agent-id <id>`：指定操作的 agent（默认：default）
- 适用于：models、channels、cron、chats、skills 等命令

**工作区结构**：
```
~/.copaw/workspaces/<agent-id>/
├── agent.json          # Agent 配置
├── active_skills/      # 内置 skills
├── file_store/         # 向量数据库（可选）
├── chats.json          # 聊天记录
├── jobs.json           # 定时任务
├── AGENTS.md           # Agent 说明
├── MEMORY.md           # 记忆
├── HEARTBEAT.md        # 心跳检查
└── memory/             # 记忆目录
```

## 3. 初始化与配置

```bash
copaw init
copaw init --defaults
copaw init --force
```

默认工作目录：`~/.copaw/`

- `config.json` - 根配置（多 agent 架构）
- `workspaces/` - 工作区目录
- `copaw.log` - 日志文件

环境变量覆盖：

```bash
export COPAW_WORKING_DIR=/custom/path
export COPAW_LOG_LEVEL=debug
export COPAW_MEMORY_COMPACT_THRESHOLD=100000
```

## 4. 模型管理

```bash
# 默认 agent
copaw models list
copaw models config
copaw models config-key dashscope
copaw models set-llm

# 指定 agent
copaw models list --agent-id <id>
copaw models config --agent-id <id>
copaw models set-llm --agent-id <id>

# 本地模型
copaw models download Qwen/Qwen3-4B-GGUF
copaw models local
copaw models remove-local <model_id> --yes

# Ollama 模型
copaw models ollama-pull qwen3:8b
copaw models ollama-list
copaw models ollama-remove qwen3:8b
```

## 5. 渠道管理

```bash
# 默认 agent
copaw channels list
copaw channels config
copaw channels add dingtalk
copaw channels remove my_channel

# 指定 agent
copaw channels list --agent-id <id>
copaw channels config dingtalk --agent-id <id>
copaw channels add dingtalk --agent-id <id>
```

支持渠道：`iMessage, Discord, DingTalk, Feishu, QQ, Console, Telegram, Matrix, Mattermost, MQTT`

**钉钉渠道配置**：
```bash
copaw channels config dingtalk --agent-id <id>
```

必填字段：
- `client_id`
- `client_secret`
- `robot_code`（可选）

## 6. 定时任务管理

```bash
# 默认 agent
copaw cron list
copaw cron get <job_id>
copaw cron state <job_id>
copaw cron create ...
copaw cron delete <job_id>
copaw cron pause <job_id>
copaw cron resume <job_id>
copaw cron run <job_id>

# 指定 agent
copaw cron list --agent-id <id>
copaw cron state <job_id> --agent-id <id>
copaw cron create --agent-id <id> ...
copaw cron resume <job_id> --agent-id <id>
copaw cron run <job_id> --agent-id <id>
```

创建示例：

```bash
copaw cron create \
  --agent-id default \
  --type agent \
  --name "每日检查" \
  --cron "0 9 * * *" \
  --channel dingtalk \
  --target-user "user_id" \
  --target-session "session_id" \
  --text "今日待办有哪些？"
```

## 7. 会话与技能

```bash
# 默认 agent
copaw chats list
copaw chats list --channel dingtalk
copaw chats get <chat_id>
copaw chats delete <chat_id>

copaw skills list
copaw skills config

# 指定 agent
copaw chats list --agent-id <id>
copaw skills list --agent-id <id>
```

**内置 Skills**：
- `cron` - 定时任务管理
- `dingtalk_channel` - 钉钉自动连接
- `docx/pptx/xlsx` - Office 文档操作
- `pdf` - PDF 操作
- `himalaya` - 邮件客户端
- `browser_visible` - 浏览器可视化
- `news` - 新闻
- `file_reader` - 文件读取
- `guidance` - 指导

聊天命令：

```text
/compact
/new
/clear
/history
/compact_str
```

## 8. 环境变量与清理

```bash
copaw env list
copaw env set TAVILY_API_KEY "xxx"
copaw env delete TAVILY_API_KEY

copaw clean
copaw clean --yes
copaw clean --dry-run
```

## 9. Docker / Supervisord

```bash
docker run -d -p 8088:8088 -v ~/.copaw:/app/working -e COPAW_PORT=8088 copaw:latest
docker exec -it <container_id> bash

supervisorctl status
supervisorctl restart app
supervisorctl tail -f app
```

日志路径：

- `/var/log/supervisord.log`
- `/var/log/app.out.log`
- `/var/log/app.err.log`
- `/app/working/copaw.log`

## 10. 监控巡检清单

```bash
# 全局状态
copaw daemon status
copaw daemon version
copaw daemon logs -n 50

# 多 agent 检查
copaw agent list
copaw workspace list

# 特定 agent 检查
copaw models list --agent-id <id>
copaw channels list --agent-id <id>
copaw cron list --agent-id <id>
copaw chats list --agent-id <id>

# 工作区检查
ls -la ~/.copaw/workspaces/<id>/
cat ~/.copaw/workspaces/<id>/agent.json
```

聊天中补充检查：

```text
/history
```

## 11. 常用参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--agent-id <id>` | 指定操作的 agent | default |
| `--channel <name>` | 指定渠道 | - |
| `--target-user <id>` | 目标用户标识 | - |
| `--target-session <id>` | 目标会话标识 | - |
| `-n, --lines <num>` | 日志行数 | 100 |
| `--yes` | 跳过确认 | false |
| `--dry-run` | 试运行 | false |

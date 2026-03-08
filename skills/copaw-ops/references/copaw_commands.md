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

## 2. 初始化与配置

```bash
copaw init
copaw init --defaults
copaw init --force
```

默认工作目录：`~/.copaw/`

- `config.json`
- `HEARTBEAT.md`
- `jobs.json`
- `chats.json`
- `copaw.log`
- `SOUL.md`
- `AGENTS.md`
- `MEMORY.md`
- `memory/`

环境变量覆盖：

```bash
export COPAW_WORKING_DIR=/custom/path
export COPAW_LOG_LEVEL=debug
export COPAW_MEMORY_COMPACT_THRESHOLD=100000
```

## 3. 模型管理

```bash
copaw models list
copaw models config
copaw models config-key dashscope
copaw models set-llm

copaw models download Qwen/Qwen3-4B-GGUF
copaw models local
copaw models remove-local <model_id> --yes

copaw models ollama-pull qwen3:8b
copaw models ollama-list
copaw models ollama-remove qwen3:8b
```

## 4. 渠道管理

```bash
copaw channels list
copaw channels config
copaw channels add dingtalk
copaw channels remove my_channel
```

支持渠道：`iMessage, Discord, DingTalk, Feishu, QQ, Console`

## 5. 定时任务管理

```bash
copaw cron list
copaw cron get <job_id>
copaw cron state <job_id>
copaw cron create ...
copaw cron delete <job_id>
copaw cron pause <job_id>
copaw cron resume <job_id>
copaw cron run <job_id>
```

创建示例：

```bash
copaw cron create \
  --type agent \
  --name "每日检查" \
  --cron "0 9 * * *" \
  --channel dingtalk \
  --target-user "user_id" \
  --target-session "session_id" \
  --text "今日待办有哪些？"
```

## 6. 会话与技能

```bash
copaw chats list
copaw chats list --channel dingtalk
copaw chats get <chat_id>
copaw chats delete <chat_id>

copaw skills list
copaw skills config
```

聊天命令：

```text
/compact
/new
/clear
/history
/compact_str
```

## 7. 环境变量与清理

```bash
copaw env list
copaw env set TAVILY_API_KEY "xxx"
copaw env delete TAVILY_API_KEY

copaw clean
copaw clean --yes
copaw clean --dry-run
```

## 8. Docker / Supervisord

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

## 9. 监控巡检清单

```bash
copaw daemon status
copaw daemon version
copaw daemon logs -n 50
copaw models list
copaw channels list
copaw cron list
copaw chats list
```

聊天中补充检查：

```text
/history
```


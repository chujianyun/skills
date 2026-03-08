# CoPaw 故障恢复手册

## 1. 服务无响应

优先级从高到低：

```text
/restart
```

```bash
copaw daemon reload-config
```

按部署方式重启：

```bash
sudo systemctl restart copaw
docker restart <container_id>
supervisorctl restart app
```

## 2. MCP 客户端连接失败

- 系统会自动重试最多 3 次。
- 重试失败后应跳过故障客户端并继续运行其他功能。
- 修复配置后修改 `config.json` 触发热重载，或执行 `copaw daemon reload-config`。

## 3. 渠道断连

```bash
copaw channels list
copaw channels config
```

聊天中执行：

```text
/daemon restart
```

## 4. Token 超限 / 上下文爆满

```text
/compact
/new
/history
```

## 5. 配置错误导致启动失败

```bash
copaw daemon reload-config
copaw daemon logs -n 200
copaw init --force
```

## 6. 模型调用失败

```bash
copaw models list
copaw models config-key <provider>
copaw models set-llm
```

## 7. 定时任务不执行

```bash
copaw cron state <job_id>
copaw cron list
copaw cron resume <job_id>
copaw cron run <job_id>
```

## 8. 清理与重置

仅清理记忆：

```bash
rm -rf ~/.copaw/memory/ ~/.copaw/MEMORY.md
```

完全重置：

```bash
copaw clean --yes
copaw init
```

## 9. 恢复后验证

恢复动作执行后，必须复核：

```bash
copaw daemon status
copaw daemon logs -n 100
copaw channels list
copaw models list
copaw cron list
```

若仍有错误，记录最近日志中的首个关键异常并切换到对应分支策略重试。


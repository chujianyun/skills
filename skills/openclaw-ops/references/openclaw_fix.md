按以下流程检查并修复 OpenClaw：

## 检查流程

1. 运行 `openclaw status` 查看快速状态
2. 若 gateway 不可达，运行 `openclaw gateway status` 确认服务状态
3. 运行 `openclaw channels status --probe` 检查渠道连接
4. 若发现问题，运行 `openclaw logs --limit 200` 查看最近日志
5. 在 macOS 上可用 `./scripts/clawlog.sh -e` 查看系统错误日志

## 修复流程

- **首选：** 运行 `openclaw doctor --repair` 自动修复（无需人工确认）
- **若 gateway 未运行：** 运行 `openclaw gateway restart`
- **若修复后仍不健康：** 运行 `openclaw doctor --repair --force`
- **更新后修复：** 先 `openclaw update`，再 `openclaw doctor`，再 `openclaw health`

## 判断成功的标准

- `openclaw health` 返回无错误
- `openclaw channels status --probe` 所有渠道状态正常
- `openclaw status` 显示 gateway 可达

## 注意事项

- macOS 上 gateway 由 OpenClaw Mac app 管理，不要用 tmux 手动启动
- 检查 launchd 环境变量覆盖问题：`launchctl getenv OPENCLAW_GATEWAY_TOKEN`
- 日志文件路径：`/tmp/openclaw/openclaw-YYYY-MM-DD.log`
- 服务日志（macOS）：`~/.openclaw/logs/gateway.log`

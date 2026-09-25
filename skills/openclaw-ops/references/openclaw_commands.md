
openclaw 的常见指令：

---

## 初始化与配置

| 指令 | 说明 |
|---|---|
| `openclaw setup` | 初始化本地配置和 agent 工作区 |
| `openclaw onboard` | 交互式引导向导（gateway、工作区、skills） |
| `openclaw configure` | 交互式配置向导（凭据、渠道、gateway 等） |
| `openclaw config get <key>` | 读取配置项 |
| `openclaw config set <key> <val>` | 写入配置项 |
| `openclaw config unset <key>` | 删除配置项 |

---

## Gateway 服务管理

| 指令 | 说明 |
|---|---|
| `openclaw gateway run` | 前台运行 Gateway |
| `openclaw gateway run --port 18789` | 指定端口运行 |
| `openclaw gateway run --force` | 强制释放端口后启动 |
| `openclaw gateway restart` | **重启** Gateway 服务 |
| `openclaw gateway start` | 启动 Gateway 服务 |
| `openclaw gateway stop` | 停止 Gateway 服务 |
| `openclaw gateway status` | 查看 Gateway 服务状态 |
| `openclaw gateway status --deep` | 深度检查系统级服务 |
| `openclaw gateway install` | 注册为系统服务（launchd/systemd） |
| `openclaw gateway uninstall` | 卸载系统服务 |
| `openclaw --dev gateway` | 以开发模式运行（隔离状态） |

---

## 状态与诊断

| 指令 | 说明 |
|---|---|
| `openclaw status` | 显示渠道健康状态与近期会话 |
| `openclaw status --all` | 完整诊断（只读，可粘贴） |
| `openclaw status --deep` | 探测所有渠道连通性 |
| `openclaw status --usage` | 显示模型用量/配额快照 |
| `openclaw health` | 从运行中的 Gateway 获取健康信息 |
| `openclaw doctor` | Gateway 与渠道健康检查 + 快速修复 |
| `openclaw logs` | 拖尾 Gateway 日志 |

---

## 渠道管理

| 指令 | 说明 |
|---|---|
| `openclaw channels list` | 列出已配置渠道和认证配置 |
| `openclaw channels status --probe` | 探测渠道状态 |
| `openclaw channels login --channel whatsapp` | 连接 WhatsApp Web（扫码） |
| `openclaw channels login --verbose` | 连接并显示详细日志 |
| `openclaw channels logout --channel <name>` | 登出渠道 |
| `openclaw channels add --channel telegram --token <token>` | 非交互式添加渠道账号 |
| `openclaw channels remove --channel <name>` | 移除渠道账号 |
| `openclaw channels capabilities` | 查看渠道权限/功能支持 |

---

## 消息操作

| 指令 | 说明 |
|---|---|
| `openclaw message send --target +15555550123 --message "Hi"` | 发送消息 |
| `openclaw message send --channel telegram --target @chat --message "Hi"` | 指定渠道发送 |
| `openclaw message send --target ... --media photo.jpg` | 发送带媒体的消息 |
| `openclaw message read --target <dest>` | 读取最近消息 |
| `openclaw message broadcast --targets <t1> <t2>` | 广播消息到多个目标 |
| `openclaw message edit --target ... --message-id <id> -m "新内容"` | 编辑消息 |
| `openclaw message delete --target ... --message-id <id>` | 删除消息 |
| `openclaw message react --target ... --message-id <id> --emoji "✅"` | 添加消息反应 |

---

## Agent 操作

| 指令 | 说明 |
|---|---|
| `openclaw agent --message "做个总结"` | 通过 Gateway 运行一次 agent |
| `openclaw agent --to +15555550123 --message "Run summary" --deliver` | 运行 agent 并将回复发回 WhatsApp |
| `openclaw agents list` | 列出所有隔离 agent |
| `openclaw agents add` | 添加新 agent |
| `openclaw sessions` | 列出已存储的会话 |

---

## 模型管理

| 指令 | 说明 |
|---|---|
| `openclaw models list` | 列出已配置模型 |
| `openclaw models list --all` | 列出完整模型目录 |
| `openclaw models status` | 显示当前模型配置状态 |
| `openclaw models status --probe` | 实时探测认证状态 |
| `openclaw models set <model>` | 设置默认模型 |
| `openclaw models scan` | 扫描可用模型 |
| `openclaw models auth add` | 添加模型认证 |

---

## 插件与技能

| 指令 | 说明 |
|---|---|
| `openclaw plugins` | 管理插件和扩展 |
| `openclaw skills list` | 列出可用 skills |
| `openclaw update` | 更新 OpenClaw |

---

## 其他实用指令

| 指令 | 说明 |
|---|---|
| `openclaw dashboard` | 打开 Control UI 控制面板 |
| `openclaw memory` | 搜索/重建记忆索引 |
| `openclaw sandbox` | 管理 agent 隔离沙箱 |
| `openclaw tui` | 打开终端 UI |
| `openclaw security` | 安全审计工具 |
| `openclaw reset` | 重置本地配置/状态 |
| `openclaw completion` | 生成 shell 自动补全脚本 |
| `openclaw docs` | 搜索官方文档 |
| `openclaw <command> --help` | 查看任意指令的详细帮助 |

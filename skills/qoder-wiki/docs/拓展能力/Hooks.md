# Hooks

来源: https://docs.qoder.com/zh/extensions/hooks

## 概述

Hooks 允许你在 Qoder IDE 和 JetBrains 插件的关键执行节点插入确定性的自定义逻辑，无需修改 Qoder 本身代码。

与 Prompt 不同，Hooks 是“事件触发即执行”的机制。

## 支持的事件

| 事件 | 触发时机 | 是否可阻断 |
| --- | --- | --- |
| `UserPromptSubmit` | 用户提交 Prompt 后、Agent 处理前 | 是 |
| `PreToolUse` | 工具执行前 | 是 |
| `PostToolUse` | 工具成功后 | 否 |
| `PostToolUseFailure` | 工具失败后 | 否 |
| `Stop` | Agent 完成响应时 | 否 |

## 典型场景

- 拦截危险命令
- 限制文件写入路径
- 写文件后自动跑 lint / format
- 工具失败时记录日志
- 完成任务后弹桌面通知
- 审查用户 Prompt

## 配置文件位置

多级配置会合并执行，优先级从低到高：

| 路径 | 作用域 | 优先级 |
| --- | --- | --- |
| `~/.qoder/settings.json` | 用户级 | 1 |
| `.qoder/settings.json` | 项目级 | 2 |
| `.qoder/settings.local.json` | 项目本地 | 3 |

说明：

- IDE / JetBrains 插件 / CLI 共用同一套 Hook 配置
- 当前版本文档说明修改后需要重启 IDE 才生效

## 配置格式

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.qoder/hooks/block-rm.sh"
          }
        ]
      }
    ]
  }
}
```

## 脚本协议

- 通过 `stdin` 接收 JSON 事件上下文
- `exit 0`：放行
- `exit 2`：阻断，并把 `stderr` 反馈给 Agent
- 其他退出码：视为错误，但通常不中断主流程

## 示例

官方文档重点演示了：

- 用 `PreToolUse` 阻止 `rm -rf`
- 用 `PostToolUse` 在写文件后自动执行 Lint
- 用 `Stop` 做桌面通知


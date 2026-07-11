# Deeplinks

Deeplinks 允许您通过简单的 URL 与他人分享 AI Chat 提示词、Quest 任务、规则和 MCP 服务器配置。当您点击深链时，IDE 会打开并显示确认对话框，展示即将添加的内容。

## URL 格式

```
{scheme}://{host}/{path}?{parameters}
```

| 组成部分 | 说明 | 示例 |
| --- | --- | --- |
| `scheme` | 协议 | `qoder` |
| `host` | 深链处理器标识 | `aicoding.aicoding-deeplink` |
| `path` | 操作路径 | `/chat`, `/quest`, `/rule`, `/mcp/add` |
| `parameters` | URL 查询参数 | `text=hello&mode=agent` |

## 可用的深链类型

| 路径 | 说明 | 是否需要登录 |
| --- | --- | --- |
| `/chat` | 创建智能会话 | 是 |
| `/quest` | 创建 Quest 任务 | 是 |
| `/rule` | 创建规则 | 否 |
| `/mcp/add` | 添加 MCP 服务器 | 否 |

## 创建智能会话 /chat

分享可直接用于聊天的提示词。

### URL 格式

```
qoder://aicoding.aicoding-deeplink/chat?text={prompt}&mode={mode}
```

### 参数说明

| 参数 | 是否必需 | 说明 |
| --- | --- | --- |
| `text` | 是 | 要预填充的提示内容 |
| `mode` | 否 | 聊天模式：`agent` 或 `ask` |

## 创建 Quest 任务 /quest

分享 Quest 任务，让 AI 自主完成复杂的开发任务。

### 参数说明

| 参数 | 是否必需 | 说明 |
| --- | --- | --- |
| `text` | 是 | 任务描述 |
| `agentClass` | 否 | 执行模式：`LocalAgent`、`LocalWorktree` 或 `RemoteAgent` |

## 创建规则 /rule

分享规则来指导 AI 行为。

### 参数说明

| 参数 | 是否必需 | 说明 |
| --- | --- | --- |
| `name` | 是 | 规则名称 |
| `text` | 是 | 规则内容 |

## 添加 MCP 服务器 /mcp/add

分享 MCP 服务器配置。

### 参数说明

| 参数 | 是否必需 | 说明 |
| --- | --- | --- |
| `name` | 是 | MCP 服务器名称 |
| `config` | 是 | Base64 编码的 MCP server JSON 配置 |

## 安全注意事项

- **不要包含敏感数据**：不要在深链中嵌入 API 密钥、密码或专有代码
- **验证来源**：只点击来自可信来源的深链
- **确认前仔细审核**：IDE 始终会显示确认对话框

## URL 长度限制

深链 URL 不应超过 **8,000 个字符**。

# MCP（Model Context Protocol）

模型上下文协议（MCP）通过与外部系统和数据源的无缝集成，扩展了 Qoder 的功能。

## 什么是 MCP

MCP 是一种开放协议，用于标准化应用如何向大语言模型（LLM）提供 context 和工具。通过以一致的接口暴露功能，MCP 使 LLM 能够以结构化且安全的方式与外部系统（如 API、数据库和本地工具）进行交互。

### 为什么使用 MCP

MCP 通过标准化接口使 Qoder 智能体能够连接到各类外部系统和数据源，从而增强智能体在以下方面的能力：

- 获取实时信息
- 在外部系统中执行操作
- 处理结构化或非结构化数据

### 支持的传输方式

- **标准输入/输出（STDIO）**：通过 stdin/stdout 流进行通信，适用于本地工具
- **服务发送事件（SSE）**：HTTP POST 请求 + 事件流响应，远程托管，易于配置

> **注意：** MCP 服务仅在智能体模式下受支持，且最多可同时使用 10 个 MCP 服务。

## 配置 MCP 服务

1. 在 Qoder IDE 的右上角，点击用户图标，然后选择 **Qoder 设置**
2. 在左侧导航窗格中，点击 **MCP**
3. 选择以下任一方式：

### 连接到自己的 MCP 服务

在 **我的服务** 选项卡中，点击右上角的 **+ 添加**，在 JSON 文件中添加配置：

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "<YOUR_TOKEN>"
      }
    }
  }
}
```

### 从 MCP 广场安装

1. 点击 **MCP 广场** 选项卡
2. 浏览可用服务列表，在目标服务上点击 **安装**

## 使用 MCP 工具

Qoder 会根据以下内容自动选择合适的 MCP 工具：

- 你的输入提示
- 工具的名称和描述

在 Qoder 调用 MCP 工具之前，会先请求你确认。

## 示例：检索网页内容

使用 MCP 服务将网页内容从 HTML 获取并转换为 Markdown：

```json
{
  "mcpServers": {
    "fetch": {
      "type": "sse",
      "url": "https://mcp.api-inference.modelscope.net/******/sse"
    }
  }
}
```

然后在智能体模式中输入：

```
总结此文档：https://docs.qoder.com/user-guide/chat/overview
```

## 示例：查询天气

```json
{
  "mcpServers": {
    "weather": {
      "command": "npx",
      "args": ["-y", "@h1deya/mcp-server-weather"]
    }
  }
}
```

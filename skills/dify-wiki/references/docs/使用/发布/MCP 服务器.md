# MCP 服务器

> 本文档由 AI 自动翻译。如有任何不准确之处，请参考 [英文原版](https://docs.dify.ai/en/cloud/use-dify/publish/publish-mcp.md)。

Dify 现在支持将你的应用作为 [MCP](https://modelcontextprotocol.io/docs/getting-started/intro)（Model Context Protocol）服务器公开，实现与 Claude Desktop 等 AI 助手和 Cursor 等开发环境的无缝集成。这使得这些工具可以直接与你的 Dify 应用交互，就像它们是原生扩展一样。

> [!NOTE]
>
> 如果你希望在 Dify 工作流和 Agent 中使用 MCP 工具，请参阅 [此处](../%E9%9B%86%E6%88%90/Dify%20%E5%B7%A5%E5%85%B7.md#mcp)。

## 将你的 Dify 应用配置为 MCP 服务器

在应用的 **访问入口** 标签页找到 **MCP 服务** 卡片。该功能默认处于禁用状态。当你开启它时，Dify 会为你的应用生成一个唯一的 MCP 服务器地址。该地址作为外部工具的连接点。

> [!CAUTION]
>
> 你的 MCP 服务器 URL 包含身份验证凭据，因此请像对待 API 密钥一样对待它。如果你怀疑它已被泄露，请使用重新生成按钮创建新的 URL。旧的 URL 将立即停止工作。

## 与 Claude Desktop 集成

要将你的 Dify 应用连接到 Claude Desktop，你需要添加一个 Claude 集成。转到你的 Claude Profile > Settings > Integrations > Add integration。用你的 Dify 应用的服务器 URL 替换集成 URL。

## 与 Cursor 集成

对于 Cursor，在你的项目根目录中创建或编辑 `.cursor/mcp.json` 文件：

```json theme={null}
{
  "mcpServers": {
    "your-server-name": {
      "url": "your-server-url"
    }
  }
}
```

只需用你的 Dify 应用的 MCP 服务器地址替换 URL。Cursor 会自动检测此配置并将你的 Dify 应用作为工具提供。你可以通过在 `mcpServers` 对象中添加其他条目来添加多个 Dify 应用。

## 实用注意事项

* 描述性

  在为你的工具及其输入参数设计描述时，考虑 AI 如何解释它们。清晰、具体的描述能带来更好的调用效果。不要使用"输入数据"，而是指定"包含用户配置文件的 JSON 对象，必需字段：姓名、邮箱、偏好设置"。
* 延迟

  MCP 协议处理通信层，但你的 Dify 应用的性能仍然很重要。如果你的应用通常需要 30 秒来处理，那么这种延迟在客户端应用中会被感受到。考虑添加进度指示器或将复杂的工作流分解为更小、更快的操作。

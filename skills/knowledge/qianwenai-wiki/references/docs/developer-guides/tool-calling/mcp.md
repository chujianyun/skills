> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# MCP

> 在对话中使用外部工具

模型上下文协议（Model Context Protocol, MCP）可帮助大模型使用外部工具与数据，相比 Function Calling，MCP 更灵活且易于使用。本文介绍通过 Responses API 接入 MCP 的方法。

使用 Responses API，在 `tools` 参数中配置 MCP Server 信息。

<Note>
  支持配置 SSE 协议的 MCP Server。最多添加 10 个 MCP Server。
</Note>

## 快速开始

以下示例接入[魔搭社区](https://www.modelscope.cn/mcp)的 [Fetch](https://www.modelscope.cn/mcp/servers/@modelcontextprotocol/fetch) MCP 服务，展示如何通过 Responses API 调用 MCP 工具。您可以在服务详情页右侧的"服务配置"中获取 SSE Endpoint 和鉴权信息。

获取[千问AI平台 API Key](/api-reference/preparation/api-key)并[配置环境变量](/api-reference/preparation/export-api-key-env)。

<Note>
  请将示例代码中 MCP 工具配置的 `server_url` 替换为 MCP 服务平台提供的 SSE 端点，将 `headers` 替换为平台提供的鉴权信息。
</Note>

<Tabs>
  <Tab title="Python">
    ```python
    import os
    from openai import OpenAI

    client = OpenAI(
      # 若没有配置环境变量，请用千问AI平台 API Key 将下行替换为：api_key="sk-xxx"（不建议）,
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )

    # MCP 工具配置
    # 将 server_url 替换为从魔搭等平台获取的 SSE Endpoint
    # 如需鉴权，将平台提供的 token 添加到 headers 中
    mcp_tool = {
      "type": "mcp",
      "server_protocol": "sse",
      "server_label": "fetch",
      "server_description": "Fetch MCP Server，提供网页抓取能力，可抓取指定 URL 的内容并以文本形式返回。",
      "server_url": "https://mcp.api-inference.modelscope.net/xxx/sse",
    }

    response = client.responses.create(
      model="qwen3.7-plus",
      input="https://news.aibase.com/zh/news，今天有什么 AI 新闻？",
      tools=[mcp_tool]
    )

    print("[模型回复]")
    print(response.output_text)
    print(f"\n[Token 用量] 输入: {response.usage.input_tokens}, 输出: {response.usage.output_tokens}, 合计: {response.usage.total_tokens}")
    ```
  </Tab>

  <Tab title="Node.js">
    ```javascript
    import OpenAI from "openai";
    import process from 'process';

    const openai = new OpenAI({
      // 若没有配置环境变量，请用千问AI平台 API Key 将下行替换为：apiKey: "sk-xxx",
      apiKey: process.env.DASHSCOPE_API_KEY,
      baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    });

    async function main() {
      // MCP 工具配置
      // 将 server_url 替换为从魔搭等平台获取的 SSE Endpoint
      // 如需鉴权，将平台提供的 token 添加到 headers 中
      const mcpTool = {
        type: "mcp",
        server_protocol: "sse",
        server_label: "fetch",
        server_description: "Fetch MCP Server，提供网页抓取能力，可抓取指定 URL 的内容并以文本形式返回。",
        server_url: "https://mcp.api-inference.modelscope.net/xxx/sse",
      };

      const response = await openai.responses.create({
        model: "qwen3.7-plus",
        input: "https://news.aibase.com/zh/news，今天有什么 AI 新闻？",
        tools: [mcpTool]
      });

      console.log("[模型回复]");
      console.log(response.output_text);
      console.log(`\n[Token 用量] 输入: ${response.usage.input_tokens}, 输出: ${response.usage.output_tokens}, 合计: ${response.usage.total_tokens}`);
    }

    main();
    ```
  </Tab>

  <Tab title="curl">
    ```bash
    # 将 server_url 替换为从魔搭等平台获取的 SSE Endpoint
    # 如需鉴权，将平台提供的 token 添加到 headers 中
    curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/responses \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
      "model": "qwen3.7-plus",
      "input": "https://news.aibase.com/zh/news，今天有什么 AI 新闻？",
      "tools": [
        {
          "type": "mcp",
          "server_protocol": "sse",
          "server_label": "fetch",
          "server_description": "Fetch MCP Server，提供网页抓取能力，可抓取指定 URL 的内容并以文本形式返回。",
          "server_url": "https://mcp.api-inference.modelscope.net/xxx/sse"
        }
      ]
    }'
    ```
  </Tab>
</Tabs>

## 流式输出

MCP 工具调用可能涉及多次外部服务交互，建议启用流式输出，实时获取工具调用过程与回复内容。

<Tabs>
  <Tab title="Python">
    ```python
    import os
    from openai import OpenAI

    client = OpenAI(
      # 若没有配置环境变量，请用千问AI平台 API Key 将下行替换为：api_key="sk-xxx"（不建议）,
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )

    # 将 server_url 替换为从魔搭等平台获取的 SSE Endpoint
    # 如需鉴权，将平台提供的 token 添加到 headers 中
    mcp_tool = {
      "type": "mcp",
      "server_protocol": "sse",
      "server_label": "fetch",
      "server_description": "Fetch MCP Server，提供网页抓取能力，可抓取指定 URL 的内容并以文本形式返回。",
      "server_url": "https://mcp.api-inference.modelscope.net/xxx/sse",
    }

    stream = client.responses.create(
      model="qwen3.7-plus",
      input="https://news.aibase.com/zh/news，今天有什么 AI 新闻？",
      tools=[mcp_tool],
      stream=True
    )

    for event in stream:
      # 模型回复开始
      if event.type == "response.content_part.added":
        print("[模型回复]")
      # 流式文本输出
      elif event.type == "response.output_text.delta":
        print(event.delta, end="", flush=True)
      # 响应完成，输出用量
      elif event.type == "response.completed":
        usage = event.response.usage
        print(f"\n\n[Token 用量] 输入: {usage.input_tokens}, 输出: {usage.output_tokens}, 合计: {usage.total_tokens}")
    ```
  </Tab>

  <Tab title="Node.js">
    ```javascript
    import OpenAI from "openai";
    import process from 'process';

    const openai = new OpenAI({
      // 若没有配置环境变量，请用千问AI平台 API Key 将下行替换为：apiKey: "sk-xxx",
      apiKey: process.env.DASHSCOPE_API_KEY,
      baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    });

    async function main() {
      // 将 server_url 替换为从魔搭等平台获取的 SSE Endpoint
      // 如需鉴权，将平台提供的 token 添加到 headers 中
      const mcpTool = {
        type: "mcp",
        server_protocol: "sse",
        server_label: "fetch",
        server_description: "Fetch MCP Server，提供网页抓取能力，可抓取指定 URL 的内容并以文本形式返回。",
        server_url: "https://mcp.api-inference.modelscope.net/xxx/sse",
      };

      const stream = await openai.responses.create({
        model: "qwen3.7-plus",
        input: "https://news.aibase.com/zh/news，今天有什么 AI 新闻？",
        tools: [mcpTool],
        stream: true
      });

      for await (const event of stream) {
        // 模型回复开始
        if (event.type === "response.content_part.added") {
          console.log("[模型回复]");
        }
        // 流式文本输出
        else if (event.type === "response.output_text.delta") {
          process.stdout.write(event.delta);
        }
        // 响应完成，输出用量
        else if (event.type === "response.completed") {
          const usage = event.response.usage;
          console.log(`\n\n[Token 用量] 输入: ${usage.input_tokens}, 输出: ${usage.output_tokens}, 合计: ${usage.total_tokens}`);
        }
      }
    }

    main();
    ```
  </Tab>

  <Tab title="curl">
    ```bash
    # 将 server_url 替换为从魔搭等平台获取的 SSE Endpoint
    # 如需鉴权，将平台提供的 token 添加到 headers 中
    curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/responses \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
      "model": "qwen3.7-plus",
      "input": "https://news.aibase.com/zh/news，今天有什么 AI 新闻？",
      "tools": [
        {
          "type": "mcp",
          "server_protocol": "sse",
          "server_label": "fetch",
          "server_description": "Fetch MCP Server，提供网页抓取能力，可抓取指定 URL 的内容并以文本形式返回。",
          "server_url": "https://mcp.api-inference.modelscope.net/xxx/sse"
        }
      ],
      "stream": true
    }'
    ```
  </Tab>
</Tabs>

## 参数说明

| 参数                   | 必填 | 说明                                                                  |
| -------------------- | -- | ------------------------------------------------------------------- |
| `type`               | 是  | 固定值 `"mcp"`。                                                        |
| `server_protocol`    | 是  | 通信协议，仅支持 `"sse"`。                                                   |
| `server_label`       | 是  | MCP 服务器的简短标识。                                                       |
| `server_description` | 否  | 服务器功能的自然语言描述。清晰的描述有助于模型判断何时调用该服务器的工具，提高工具选择的准确性。建议为所有 MCP 服务器提供此参数。 |
| `server_url`         | 是  | MCP 服务器的 SSE 端点 URL。                                                |
| `headers`            | 否  | 连接 MCP 服务器时附带的 HTTP 头，例如用于认证的 `Authorization`。                      |

**配置示例**：

```json
{
  "type": "mcp",
  "server_protocol": "sse",
  "server_label": "fetch",
  "server_description": "Fetch MCP Server，提供网页抓取能力，可抓取指定 URL 的内容并以文本形式返回。",
  "server_url": "https://mcp.api-inference.modelscope.net/xxx/sse"
}
```

## 支持的模型

MCP 仅通过 Responses API 提供。以下模型支持 MCP 工具调用：

- 千问Max：qwen3.8-max、Qwen3.7-Max 系列
- 千问Plus：Qwen3.7-Plus 系列、Qwen3.6-Plus 系列、Qwen3.5-Plus 系列
- 千问Flash：Qwen3.7-Flash 系列、Qwen3.6-Flash 系列、Qwen3.5-Flash 系列
- Qwen3.6 开源系列（qwen3.6-27b 除外）
- Qwen3.5 开源系列

## 计费

使用 MCP 时涉及两类费用：

- **模型推理费用**：根据模型的 Token 用量计费。
- **MCP 服务器费用**：按各 MCP 服务器提供商的计费规则收取。

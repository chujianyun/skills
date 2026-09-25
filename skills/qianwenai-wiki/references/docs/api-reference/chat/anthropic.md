> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Anthropic Messages API 参考

> 通过 Anthropic SDK 调用 Qwen 模型

## FAQ

**配置 Claude Desktop 或 Claude Code 后，连接测试报 `Model discovery — Gateway /v1/models returned HTTP 404`，或请求 URL 中出现 `/v1/v1/models`，如何解决？**

Claude Desktop、Claude Code 等客户端的模型发现功能会自动在配置的 base URL 后追加 `/v1/models`。请检查以下两点：

- **base URL 不要以 `/v1/` 结尾**：应以 `/apps/anthropic` 结尾（例如 `https://dashscope.aliyuncs.com/apps/anthropic`）。如果误输入 `.../apps/anthropic/v1/`，客户端追加后会产生重复路径 `/v1/v1/models`，返回 HTTP 404。

- **手动添加模型以跳过发现**：Anthropic 兼容端点仅提供 Messages API（`/v1/messages`），不提供模型列表端点（`/v1/models`），因此模型发现请求也会返回 404。在客户端的 Models 中手动添加模型（例如 `qwen3.8-max`）即可跳过自动发现。

## OpenAPI

````yaml post /apps/anthropic/v1/messages
openapi: 3.1.0
info:
  title: Anthropic 兼容 Messages API
  description: |-
    通过兼容 Anthropic 格式的 Messages API 调用 Qwen 模型，支持深度思考、工具调用、流式输出、图片视频理解和上下文缓存。

    认证方式：通过 `x-api-key` 请求头或 `Authorization: Bearer` 请求头传入 API Key，二者选其一即可。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com
    description: 中国
security:
  - ApiKeyAuth: []
paths:
  /apps/anthropic/v1/messages:
    post:
      operationId: anthropicMessages
      summary: 创建消息
      description: 通过 Anthropic 兼容接口向 Qwen 模型发送消息并获取生成回复。支持多轮对话、流式输出、深度思考、工具调用、图片视频理解和上下文缓存。
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/AnthropicMessagesRequest"
            example:
              model: qwen3.7-plus
              max_tokens: 1024
              system: You are a helpful assistant
              messages:
                - role: user
                  content: 你是谁？
      responses:
        "200":
          description: 请求成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/AnthropicMessage"
              example:
                id: msg_e2898f19-fc0e-4cb3-bd9b-5b7dc4ea3bc9
                type: message
                role: assistant
                model: qwen3.7-plus
                content:
                  - type: thinking
                    thinking: 让我分析一下这个问题...
                    signature: ""
                  - type: text
                    text: 你好！我是通义千问...
                stop_reason: end_turn
                stop_sequence: null
                usage:
                  input_tokens: 22
                  output_tokens: 223
                  cache_creation_input_tokens: 0
                  cache_read_input_tokens: 0
            text/event-stream:
              schema:
                $ref: "#/components/schemas/AnthropicStreamEvent"
              example:
                type: content_block_delta
                index: 1
                delta:
                  type: text_delta
                  text: 人工智能（Artificial Intelligence，简称AI）是计算机科学的重要分支...
        "400":
          description: 请求参数错误
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/AnthropicErrorResponse"
              example:
                type: error
                error:
                  type: invalid_request_error
                  message: "max_tokens: Field required"
        "401":
          description: 认证失败
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/AnthropicErrorResponse"
              example:
                type: error
                error:
                  type: authentication_error
                  message: invalid x-api-key
        "429":
          description: 请求频率超限
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/AnthropicErrorResponse"
              example:
                type: error
                error:
                  type: rate_limit_error
                  message: Rate limit exceeded
      x-codeSamples:
        - lang: python
          label: 基础调用
          source: |-
            import anthropic
            import os

            client = anthropic.Anthropic(
                api_key=os.getenv("DASHSCOPE_API_KEY"),
                base_url="https://dashscope.aliyuncs.com/apps/anthropic",
            )

            message = client.messages.create(
                model="qwen3.7-plus",
                max_tokens=1024,
                system="You are a helpful assistant",
                messages=[
                    {
                        "role": "user",
                        "content": "你是谁？"
                    }
                ],
                thinking={"type": "disabled"},
            )

            print(message.content[0].text)
        - lang: javascript
          label: 基础调用
          source: |-
            import Anthropic from "@anthropic-ai/sdk";

            const anthropic = new Anthropic({
              apiKey: process.env.DASHSCOPE_API_KEY,
              baseURL: "https://dashscope.aliyuncs.com/apps/anthropic",
            });

            async function main() {
              const message = await anthropic.messages.create({
                model: "qwen3.7-plus",
                max_tokens: 1024,
                system: "You are a helpful assistant",
                messages: [{
                  role: "user",
                  content: "你是谁？"
                }],
                thinking: { type: "disabled" },
              });

              console.log(message.content[0].text);
            }

            main().catch(console.error);
        - lang: curl
          label: 基础调用
          source: |-
            curl -X POST "https://dashscope.aliyuncs.com/apps/anthropic/v1/messages" \
              -H "Content-Type: application/json" \
              -H "x-api-key: $DASHSCOPE_API_KEY" \
              -d '{
                "model": "qwen3.7-plus",
                "max_tokens": 1024,
                "system": "You are a helpful assistant",
                "messages": [
                    {
                        "role": "user",
                        "content": "你是谁？"
                    }
                ],
                "thinking": {"type": "disabled"}
            }'
        - lang: python
          label: 流式输出
          source: |-
            import anthropic
            import os

            client = anthropic.Anthropic(
                api_key=os.getenv("DASHSCOPE_API_KEY"),
                base_url="https://dashscope.aliyuncs.com/apps/anthropic",
            )

            stream = client.messages.create(
                model="qwen3.7-plus",
                max_tokens=1024,
                stream=True,
                messages=[
                    {
                        "role": "user",
                        "content": "请简单介绍一下人工智能。"
                    }
                ],
                thinking={"type": "disabled"},
            )

            for chunk in stream:
                if chunk.type == "content_block_delta":
                    if hasattr(chunk.delta, 'text'):
                        print(chunk.delta.text, end="", flush=True)
        - lang: javascript
          label: 流式输出
          source: |-
            import Anthropic from "@anthropic-ai/sdk";

            async function main() {
              const anthropic = new Anthropic({
                apiKey: process.env.DASHSCOPE_API_KEY,
                baseURL: "https://dashscope.aliyuncs.com/apps/anthropic",
              });

              const stream = await anthropic.messages.create({
                model: "qwen3.7-plus",
                max_tokens: 1024,
                stream: true,
                messages: [{
                  role: "user",
                  content: "请简单介绍一下人工智能。"
                }],
                thinking: { type: "disabled" },
              });

              for await (const chunk of stream) {
                if (chunk.type === "content_block_delta" && 'text' in chunk.delta) {
                  process.stdout.write(chunk.delta.text);
                }
              }
            }

            main().catch(console.error);
        - lang: curl
          label: 流式输出
          source: |-
            curl -X POST "https://dashscope.aliyuncs.com/apps/anthropic/v1/messages" \
              -H "Content-Type: application/json" \
              -H "x-api-key: $DASHSCOPE_API_KEY" \
              --no-buffer \
              -d '{
                "model": "qwen3.7-plus",
                "max_tokens": 1024,
                "stream": true,
                "messages": [
                    {
                        "role": "user",
                        "content": "请简单介绍一下人工智能。"
                    }
                ],
                "thinking": {"type": "disabled"}
            }'
        - lang: python
          label: 深度思考
          source: |-
            import anthropic
            import os

            client = anthropic.Anthropic(
                api_key=os.getenv("DASHSCOPE_API_KEY"),
                base_url="https://dashscope.aliyuncs.com/apps/anthropic",
            )

            stream = client.messages.create(
                model="qwen3.7-plus",
                max_tokens=2048,
                stream=True,
                thinking={
                    "type": "enabled",
                    "budget_tokens": 1024
                },
                messages=[
                    {
                        "role": "user",
                        "content": "分析一下量子计算的发展前景。"
                    }
                ]
            )

            for chunk in stream:
                if chunk.type == "content_block_delta":
                    if hasattr(chunk.delta, 'thinking'):
                        print(chunk.delta.thinking, end="", flush=True)
                    elif hasattr(chunk.delta, 'text'):
                        print(chunk.delta.text, end="", flush=True)
        - lang: javascript
          label: 深度思考
          source: |-
            import Anthropic from "@anthropic-ai/sdk";

            async function main() {
              const anthropic = new Anthropic({
                apiKey: process.env.DASHSCOPE_API_KEY,
                baseURL: "https://dashscope.aliyuncs.com/apps/anthropic",
              });

              const stream = await anthropic.messages.create({
                model: "qwen3.7-plus",
                max_tokens: 2048,
                stream: true,
                thinking: { type: "enabled", budget_tokens: 1024 },
                messages: [{
                  role: "user",
                  content: "分析一下量子计算的发展前景。"
                }]
              });

              for await (const chunk of stream) {
                if (chunk.type === "content_block_delta") {
                  if ('thinking' in chunk.delta) {
                    process.stdout.write(chunk.delta.thinking);
                  } else if ('text' in chunk.delta) {
                    process.stdout.write(chunk.delta.text);
                  }
                }
              }
            }

            main().catch(console.error);
        - lang: curl
          label: 深度思考
          source: |-
            curl -X POST "https://dashscope.aliyuncs.com/apps/anthropic/v1/messages" \
              -H "Content-Type: application/json" \
              -H "x-api-key: $DASHSCOPE_API_KEY" \
              -d '{
                "model": "qwen3.7-plus",
                "max_tokens": 2048,
                "stream": true,
                "thinking": {
                    "type": "enabled",
                    "budget_tokens": 1024
                },
                "messages": [
                    {
                        "role": "user",
                        "content": "分析一下量子计算的发展前景。"
                    }
                ]
            }'
        - lang: python
          label: 图片理解
          source: |-
            import anthropic
            import os

            client = anthropic.Anthropic(
                api_key=os.getenv("DASHSCOPE_API_KEY"),
                base_url="https://dashscope.aliyuncs.com/apps/anthropic",
            )

            stream = client.messages.create(
                model="qwen3.7-plus",
                max_tokens=1024,
                stream=True,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "url",
                                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250414/mqqmiy/animal_01.jpg",
                                },
                            },
                            {
                                "type": "text",
                                "text": "描述这张图片的内容。"
                            },
                        ],
                    }
                ],
                thinking={"type": "disabled"},
            )

            for chunk in stream:
                if chunk.type == "content_block_delta":
                    if hasattr(chunk.delta, 'text'):
                        print(chunk.delta.text, end="", flush=True)
        - lang: javascript
          label: 图片理解
          source: |-
            import Anthropic from "@anthropic-ai/sdk";

            async function main() {
              const anthropic = new Anthropic({
                apiKey: process.env.DASHSCOPE_API_KEY,
                baseURL: "https://dashscope.aliyuncs.com/apps/anthropic",
              });

              const stream = await anthropic.messages.create({
                model: "qwen3.7-plus",
                max_tokens: 1024,
                stream: true,
                messages: [{
                  role: "user",
                  content: [
                    {
                      type: "image",
                      source: {
                        type: "url",
                        url: "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250414/mqqmiy/animal_01.jpg",
                      },
                    },
                    { type: "text", text: "描述这张图片的内容。" },
                  ],
                }],
                thinking: { type: "disabled" },
              });

              for await (const chunk of stream) {
                if (chunk.type === "content_block_delta" && 'text' in chunk.delta) {
                  process.stdout.write(chunk.delta.text);
                }
              }
            }

            main().catch(console.error);
        - lang: curl
          label: 图片理解
          source: |-
            curl -X POST "https://dashscope.aliyuncs.com/apps/anthropic/v1/messages" \
              -H "Content-Type: application/json" \
              -H "x-api-key: $DASHSCOPE_API_KEY" \
              -d '{
                "model": "qwen3.7-plus",
                "max_tokens": 1024,
                "stream": true,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "url",
                                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250414/mqqmiy/animal_01.jpg"
                                }
                            },
                            {
                                "type": "text",
                                "text": "描述这张图片的内容。"
                            }
                        ]
                    }
                ],
                "thinking": {"type": "disabled"}
            }'
        - lang: python
          label: 视频理解
          source: |-
            import anthropic
            import os

            client = anthropic.Anthropic(
                api_key=os.getenv("DASHSCOPE_API_KEY"),
                base_url="https://dashscope.aliyuncs.com/apps/anthropic",
            )

            stream = client.messages.create(
                model="qwen3.7-plus",
                max_tokens=1024,
                stream=True,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "video",
                                "source": {
                                    "type": "url",
                                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251208/zpupby/3e81ef38-98f0-4d55-bbb6-259334ca18d0.mp4",
                                },
                            },
                            {
                                "type": "text",
                                "text": "描述这段视频的内容。"
                            },
                        ],
                    }
                ],
                thinking={"type": "disabled"},
            )

            for chunk in stream:
                if chunk.type == "content_block_delta":
                    if hasattr(chunk.delta, 'text'):
                        print(chunk.delta.text, end="", flush=True)
        - lang: javascript
          label: 视频理解
          source: |-
            import Anthropic from "@anthropic-ai/sdk";

            async function main() {
              const anthropic = new Anthropic({
                apiKey: process.env.DASHSCOPE_API_KEY,
                baseURL: "https://dashscope.aliyuncs.com/apps/anthropic",
              });

              const stream = await anthropic.messages.create({
                model: "qwen3.7-plus",
                max_tokens: 1024,
                stream: true,
                messages: [{
                  role: "user",
                  content: [
                    {
                      type: "video",
                      source: {
                        type: "url",
                        url: "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251208/zpupby/3e81ef38-98f0-4d55-bbb6-259334ca18d0.mp4",
                      },
                    },
                    { type: "text", text: "描述这段视频的内容。" },
                  ],
                }],
                thinking: { type: "disabled" },
              });

              for await (const chunk of stream) {
                if (chunk.type === "content_block_delta" && 'text' in chunk.delta) {
                  process.stdout.write(chunk.delta.text);
                }
              }
            }

            main().catch(console.error);
        - lang: curl
          label: 视频理解
          source: |-
            curl -X POST "https://dashscope.aliyuncs.com/apps/anthropic/v1/messages" \
              -H "Content-Type: application/json" \
              -H "x-api-key: $DASHSCOPE_API_KEY" \
              -d '{
                "model": "qwen3.7-plus",
                "max_tokens": 1024,
                "stream": true,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "video",
                                "source": {
                                    "type": "url",
                                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251208/zpupby/3e81ef38-98f0-4d55-bbb6-259334ca18d0.mp4"
                                }
                            },
                            {
                                "type": "text",
                                "text": "描述这段视频的内容。"
                            }
                        ]
                    }
                ],
                "thinking": {"type": "disabled"}
            }'
        - lang: python
          label: Function Call
          source: |-
            import anthropic
            import os

            client = anthropic.Anthropic(
                api_key=os.getenv("DASHSCOPE_API_KEY"),
                base_url="https://dashscope.aliyuncs.com/apps/anthropic",
            )

            tools = [
                {
                    "name": "get_weather",
                    "description": "获取指定城市的天气信息",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "city": {
                                "type": "string",
                                "description": "城市名称"
                            }
                        },
                        "required": ["city"]
                    }
                }
            ]

            message = client.messages.create(
                model="qwen3.7-plus",
                max_tokens=1024,
                tools=tools,
                messages=[
                    {
                        "role": "user",
                        "content": "杭州今天天气怎么样？"
                    }
                ]
            )

            print(message.content)
        - lang: javascript
          label: Function Call
          source: |-
            import Anthropic from "@anthropic-ai/sdk";

            async function main() {
              const anthropic = new Anthropic({
                apiKey: process.env.DASHSCOPE_API_KEY,
                baseURL: "https://dashscope.aliyuncs.com/apps/anthropic",
              });

              const message = await anthropic.messages.create({
                model: "qwen3.7-plus",
                max_tokens: 1024,
                tools: [
                  {
                    name: "get_weather",
                    description: "获取指定城市的天气信息",
                    input_schema: {
                      type: "object",
                      properties: {
                        city: { type: "string", description: "城市名称" }
                      },
                      required: ["city"],
                    },
                  },
                ],
                messages: [{
                  role: "user",
                  content: "杭州今天天气怎么样？"
                }],
              });

              console.log(JSON.stringify(message.content, null, 2));
            }

            main().catch(console.error);
        - lang: curl
          label: Function Call
          source: |-
            curl -X POST "https://dashscope.aliyuncs.com/apps/anthropic/v1/messages" \
              -H "Content-Type: application/json" \
              -H "x-api-key: $DASHSCOPE_API_KEY" \
              -d '{
                "model": "qwen3.7-plus",
                "max_tokens": 1024,
                "tools": [
                    {
                        "name": "get_weather",
                        "description": "获取指定城市的天气信息",
                        "input_schema": {
                            "type": "object",
                            "properties": {
                                "city": {
                                    "type": "string",
                                    "description": "城市名称"
                                }
                            },
                            "required": ["city"]
                        }
                    }
                ],
                "messages": [
                    {
                        "role": "user",
                        "content": "杭州今天天气怎么样？"
                    }
                ]
            }'
        - lang: python
          label: 显式缓存
          source: |-
            import anthropic
            import os

            client = anthropic.Anthropic(
                api_key=os.getenv("DASHSCOPE_API_KEY"),
                base_url="https://dashscope.aliyuncs.com/apps/anthropic",
            )

            # 模拟代码仓库内容，需达到最小可缓存长度（1024 Token）
            long_text_content = "<Your Code Here>" * 400

            def get_completion(user_input):
                response = client.messages.create(
                    # 选择支持显式缓存的模型
                    model="qwen3.7-plus",
                    max_tokens=1024,
                    system=[
                        {
                            "type": "text",
                            "text": long_text_content,
                            # 在 text 块上添加 cache_control 即标记缓存断点；也可放在 messages 数组的 content 块上
                            "cache_control": {"type": "ephemeral"},
                        }
                    ],
                    messages=[
                        {"role": "user", "content": user_input},
                    ],
                )
                return response

            # 第一次请求：创建缓存
            first = get_completion("这段代码的内容是什么")
            print(f"创建缓存 Token：{first.usage.cache_creation_input_tokens}")
            print(f"命中缓存 Token：{first.usage.cache_read_input_tokens}")
            print("=" * 20)
            # 第二次请求：长内容相同，仅修改提问 → 命中缓存
            second = get_completion("这段代码可以怎么优化")
            print(f"创建缓存 Token：{second.usage.cache_creation_input_tokens}")
            print(f"命中缓存 Token：{second.usage.cache_read_input_tokens}")
        - lang: javascript
          label: 显式缓存
          source: |-
            import Anthropic from "@anthropic-ai/sdk";

            const client = new Anthropic({
              apiKey: process.env.DASHSCOPE_API_KEY,
              baseURL: "https://dashscope.aliyuncs.com/apps/anthropic",
            });

            // 模拟代码仓库内容，需达到最小可缓存长度（1024 Token）
            const longTextContent = "<Your Code Here>".repeat(400);

            async function getCompletion(userInput) {
              return client.messages.create({
                // 选择支持显式缓存的模型
                model: "qwen3.7-plus",
                max_tokens: 1024,
                system: [
                  {
                    type: "text",
                    text: longTextContent,
                    // 在 text 块上添加 cache_control 即标记缓存断点；也可放在 messages 数组的 content 块上
                    cache_control: { type: "ephemeral" },
                  },
                ],
                messages: [{ role: "user", content: userInput }],
              });
            }

            // 第一次请求：创建缓存
            const first = await getCompletion("这段代码的内容是什么");
            console.log(`创建缓存 Token：${first.usage.cache_creation_input_tokens}`);
            console.log(`命中缓存 Token：${first.usage.cache_read_input_tokens}`);
            console.log("=".repeat(20));
            // 第二次请求：长内容相同，仅修改提问 → 命中缓存
            const second = await getCompletion("这段代码可以怎么优化");
            console.log(`创建缓存 Token：${second.usage.cache_creation_input_tokens}`);
            console.log(`命中缓存 Token：${second.usage.cache_read_input_tokens}`);
        - lang: curl
          label: 显式缓存
          source: |-
            curl -X POST "https://dashscope.aliyuncs.com/apps/anthropic/v1/messages" \
              -H "Content-Type: application/json" \
              -H "x-api-key: $DASHSCOPE_API_KEY" \
              -d '{
                "model": "qwen3.7-plus",
                "max_tokens": 1024,
                "system": [
                  {
                    "type": "text",
                    "text": "<请在此处放置长度 ≥ 1024 Token 的可缓存内容>",
                    "cache_control": {"type": "ephemeral"}
                  }
                ],
                "messages": [
                  {"role": "user", "content": "这段代码的内容是什么"}
                ]
            }'
        - lang: python
          label: 结构化输出
          source: |-
            import anthropic
            import os

            client = anthropic.Anthropic(
              api_key=os.getenv("DASHSCOPE_API_KEY"),
              base_url="https://dashscope.aliyuncs.com/apps/anthropic",
            )

            message = client.messages.create(
              model="deepseek-v4-pro",
              max_tokens=1024,
              messages=[
                {
                  "role": "user",
                  "content": "提取以下邮件的关键信息：张三 (zhangsan@example.com) 对企业版方案感兴趣，希望预约下周二下午 2 点的演示。"
                }
              ],
              extra_body={
                "output_config": {
                  "format": {
                    "type": "json_schema",
                    "schema": {
                      "type": "object",
                      "properties": {
                        "name": {"type": "string"},
                        "email": {"type": "string"},
                        "plan_interest": {"type": "string"},
                        "demo_requested": {"type": "boolean"}
                      },
                      "required": ["name", "email", "plan_interest", "demo_requested"],
                      "additionalProperties": False
                    }
                  }
                }
              },
            )

            # deepseek-v4-pro 模型会返回 thinking 块，需要找到 type='text' 的内容块
            text_block = next(block for block in message.content if block.type == "text")
            print(text_block.text)
        - lang: javascript
          label: 结构化输出
          source: |-
            import Anthropic from "@anthropic-ai/sdk";

            const anthropic = new Anthropic({
              apiKey: process.env.DASHSCOPE_API_KEY,
              baseURL: "https://dashscope.aliyuncs.com/apps/anthropic",
            });

            async function main() {
              const message = await anthropic.messages.create({
                model: "deepseek-v4-pro",
                max_tokens: 1024,
                messages: [{
                  role: "user",
                  content: "提取以下邮件的关键信息：张三 (zhangsan@example.com) 对企业版方案感兴趣，希望预约下周二下午 2 点的演示。"
                }],
                output_config: {
                  format: {
                    type: "json_schema",
                    schema: {
                      type: "object",
                      properties: {
                        name: { type: "string" },
                        email: { type: "string" },
                        plan_interest: { type: "string" },
                        demo_requested: { type: "boolean" }
                      },
                      required: ["name", "email", "plan_interest", "demo_requested"],
                      additionalProperties: false
                    }
                  }
                }
              });

              // deepseek-v4-pro 模型会返回 thinking 块，需要找到 type='text' 的内容块
              const textBlock = message.content.find((block) => block.type === "text");
              console.log(textBlock.text);
            }

            main().catch(console.error);
        - lang: curl
          label: 结构化输出
          source: |-
            curl -X POST "https://dashscope.aliyuncs.com/apps/anthropic/v1/messages" \
              -H "Content-Type: application/json" \
              -H "x-api-key: $DASHSCOPE_API_KEY" \
              -d '{
                "model": "deepseek-v4-pro",
                "max_tokens": 1024,
                "messages": [
                    {
                        "role": "user",
                        "content": "提取以下邮件的关键信息：张三 (zhangsan@example.com) 对企业版方案感兴趣，希望预约下周二下午 2 点的演示。"
                    }
                ],
                "output_config": {
                    "format": {
                        "type": "json_schema",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "email": {"type": "string"},
                                "plan_interest": {"type": "string"},
                                "demo_requested": {"type": "boolean"}
                            },
                            "required": ["name", "email", "plan_interest", "demo_requested"],
                            "additionalProperties": false
                        }
                    }
                }
            }'
components:
  securitySchemes:
    ApiKeyAuth:
      type: apiKey
      in: header
      name: x-api-key
      description: "通过 `x-api-key` 请求头传入[千问AI平台 API Key](/api-reference/preparation/api-key)。也支持 `Authorization: Bearer` 请求头，二者选其一即可。"
  schemas:
    AnthropicMessagesRequest:
      type: object
      required:
        - model
        - max_tokens
        - messages
      properties:
        model:
          type: string
          description: |-
            模型名称。支持范围如下：

            **千问Max**：qwen3.8-max、qwen3.7-max、qwen3.7-max-2026-06-08、qwen3.7-max-2026-05-20、qwen3.6-max-preview、qwen3-max、qwen3-max-2026-01-23、qwen3-max-preview

            **千问Plus**：qwen3.6-plus、qwen3.6-plus-2026-04-02、qwen3.5-plus、qwen3.5-plus-2026-04-20、qwen3.5-plus-2026-02-15、qwen-plus、qwen-plus-latest、qwen-plus-2025-09-11

            **千问Flash**：qwen3.7-flash、qwen3.7-flash-2026-07-15、qwen3.6-flash、qwen3.6-flash-2026-04-16、qwen3.5-flash、qwen3.5-flash-2026-02-23、qwen-flash、qwen-flash-2025-07-28

            **千问Turbo**：qwen-turbo、qwen-turbo-latest

            **千问Coder**：qwen3-coder-next、qwen3-coder-plus、qwen3-coder-plus-2025-09-23、qwen3-coder-flash

            **千问VL**：qwen3-vl-plus、qwen3-vl-flash、qwen-vl-max、qwen-vl-plus

            **千问开源模型**：qwen3.6-27b、qwen3.5-397b-a17b、qwen3.5-122b-a10b、qwen3.5-27b、qwen3.5-35b-a3b、qwen3.8-2.4t-a95b

            **第三方模型**：deepseek-v4-pro-0813、deepseek-v4-pro、deepseek-v4-flash、deepseek-v4-flash-0731、deepseek-v3.2、kimi-k2.7-code、kimi-k2.6、kimi-k2.5、kimi-k2-thinking、glm-5.2、glm-5.1、glm-5、glm-4.7、glm-4.6、MiniMax-M2.5、MiniMax-M2.1
        max_tokens:
          type: integer
          description: |-
            模型回复内容的最大 Token 数。模型输出超过此值时生成将提前停止，`stop_reason` 为 `max_tokens`。

            - deepseek-v4-pro-0813、deepseek-v4-pro、deepseek-v4-flash、deepseek-v4-flash-0731、qwen3.8-max：`max_tokens` 为模型回复内容和思维链内容之和的最大 Token 数，限制模型回复内容+思考过程的长度。开启深度思考时，`max_tokens` > `thinking.budget_tokens`。
            - glm-5.2：不传入 `thinking.budget_tokens` 参数时，`max_tokens` 为模型回复内容和思维链内容之和的最大 Token 数，模型输出超过此值时生成将提前停止，`stop_reason` 为 `max_tokens`；传入 `thinking.budget_tokens` 参数时，`max_tokens` 仅为模型回复内容的最大 Token 数，思考部分的 Token 数由 `thinking.budget_tokens` 单独控制。
            - 其他模型：`max_tokens` 不限制思考过程的长度。开启深度思考时，思考部分的 Token 数由 `thinking.budget_tokens` 单独控制。
        system:
          oneOf:
            - type: string
            - type: array
              items:
                type: object
                required:
                  - type
                  - text
                properties:
                  type:
                    type: string
                    enum:
                      - text
                    description: 固定为 `text`。
                  text:
                    type: string
                    description: 系统提示词文本。
                  cache_control:
                    type: object
                    description: 在该内容块上标记显式缓存断点。
                    properties:
                      type:
                        type: string
                        enum:
                          - ephemeral
                        description: 固定为 `ephemeral`。
          description: 系统提示词，用于设定模型的角色或行为。`system` 通过顶层参数传入，`messages` 数组中不接受 `system` 角色。传入字符串等价于单个 `type="text"` 的内容块。当需要为系统提示词标记显式缓存断点时，必须传入数组形式。
        messages:
          type: array
          description: 消息数组，按对话顺序排列。
          items:
            type: object
            required:
              - role
              - content
            properties:
              role:
                type: string
                enum:
                  - user
                  - assistant
                  - system
                description: 消息角色。
              content:
                oneOf:
                  - type: string
                  - type: array
                    description: 结构化内容数组，支持文本、图片、视频、工具调用和工具结果类型。
                    items:
                      type: object
                      required:
                        - type
                      properties:
                        type:
                          type: string
                          enum:
                            - text
                            - image
                            - video
                            - tool_use
                            - tool_result
                          description: 内容块类型。
                        text:
                          type: string
                          description: "`text` 类型时的文本内容。"
                        source:
                          type: object
                          description: "`image` / `video` 类型时的数据来源。"
                          properties:
                            type:
                              type: string
                              enum:
                                - url
                                - base64
                              description: 取值：`url`（公网地址）、`base64`（Base64 编码）。
                            url:
                              type: string
                              description: 公网地址。当 `type` 为 `url` 时必填。
                            media_type:
                              type: string
                              description: MIME 类型，如 `image/jpeg`、`video/mp4`。当 `type` 为 `base64` 时必填。
                            data:
                              type: string
                              description: Base64 编码数据。当 `type` 为 `base64` 时必填。
                        id:
                          type: string
                          description: "`tool_use` 类型时的工具调用唯一标识。"
                        name:
                          type: string
                          description: "`tool_use` 类型时被调用的工具名称。"
                        input:
                          type: object
                          description: "`tool_use` 类型时的工具调用入参。"
                        tool_use_id:
                          type: string
                          description: "`tool_result` 类型时对应的 `tool_use` id。"
                        cache_control:
                          type: object
                          description: 在该内容块上标记显式缓存断点。
                          properties:
                            type:
                              type: string
                              enum:
                                - ephemeral
                description: 消息内容。可以是纯文本字符串，也可以是结构化内容数组。
        stream:
          type: boolean
          default: false
          description: 是否启用流式输出，默认为 `false`。
        temperature:
          type: number
          description: |-
            控制生成文本的多样性，取值范围 [0, 2)。值越大，生成结果越随机。该范围与 Anthropic 官方的 [0.0, 1.0] 不同，从 Anthropic 迁移时请确认该参数取值。

            **qwen3.8-max 说明**：思考模式下默认值为 0.6，传入值小于 0.6 时自动调整为 0.6。
        top_p:
          type: number
          description: 核采样的概率阈值，控制生成文本的多样性。`temperature` 与 `top_p` 均可控制多样性，建议只设置其中一个值。
        top_k:
          type: integer
          description: 生成过程中采样候选集的大小。
        stop_sequences:
          type: array
          items:
            type: string
          description: 指定停止生成的文本序列。模型生成到该序列前会停止输出，且不包含该序列本身。命中后，响应的 `stop_reason` 仍为 `end_turn`，响应不会回填命中的序列。
        thinking:
          type: object
          description: 深度思考配置。开启后，模型会在生成回复前先进行推理，以提升回答准确度。开启后，响应会包含 `thinking` 类型的内容块。
          properties:
            type:
              type: string
              enum:
                - enabled
                - disabled
              description: "`enabled`（开启思考模式）或 `disabled`（关闭思考模式）。"
            budget_tokens:
              type: integer
              description: |-
                （即将废弃）该参数即将废弃，并将在后续模型中逐步停止支持，新接入建议使用 `output_config.effort` 控制模型的思考强度。

                思考过程可使用的最大 Token 数，与 `max_tokens` 互不重叠：本参数限制思考，`max_tokens` 限制最终回复。预算越大，在复杂问题上的分析越充分。当 `type` 为 `enabled` 时生效。
        tools:
          type: array
          description: 工具定义数组，用于 Function Call 场景。
          items:
            type: object
            required:
              - name
              - input_schema
            properties:
              name:
                type: string
                description: 工具名称。
              description:
                type: string
                description: 工具的功能描述。
              input_schema:
                type: object
                description: 工具输入参数的 JSON Schema 定义。
        tool_choice:
          type: object
          description: '工具选择策略。`{"type": "auto"}`：模型自行决定是否调用工具（默认）。`{"type": "any"}`：强制调用任意一个工具。`{"type": "none"}`：禁止调用工具。`{"type": "tool", "name": "tool_name"}`：强制调用指定工具。'
          properties:
            type:
              type: string
              enum:
                - auto
                - any
                - none
                - tool
              description: 策略类型。
            name:
              type: string
              description: 当 `type` 为 `tool` 时，指定要调用的工具名称。
        output_config:
          type: object
          description: 输出参数设置。
          properties:
            effort:
              type: string
              enum:
                - high
                - max
                - low
                - medium
                - xhigh
              description: |-
                控制模型的推理力度。不同模型的默认值和有效值不同：

                - **glm-5.2、deepseek-v4-pro-0813、deepseek-v4-pro、deepseek-v4-flash（包含 deepseek-v4-flash-0731）（阿里云直供）**：默认值为 `max`。可选值：

                  - `high`：高力度推理
                  - `max`：最大力度推理

                  `low` 和 `medium` 映射为 `high`，`xhigh` 映射为 `max`。
                - **qwen3.8-max**：默认值为 `xhigh`。可选值：

                  - `xhigh`：高力度推理
                  - `medium`：中力度推理
                  - `low`：低力度推理

                  `max` 和 `high` 映射为 `xhigh`。
            format:
              type: object
              description: |-
                结构化输出配置。启用后，模型返回 JSON 字符串。不同模型行为有差异：

                - **严格结构化输出**：适用于 deepseek 和 glm 系列模型。模型严格遵循提供的 JSON Schema，保证字段类型和层级一致。
                - **常规结构化输出**：适用于其他所有模型，不会强制约束 schema 字段，API 会自动降级为普通 JSON 模式（仅保证输出为合法的 JSON 字符串）。在此降级模式下，请求必须同时满足以下两点：(1) 显式提供 `output_config` 参数；(2) `system` 或 `messages` 内容中包含关键词 "JSON"（不区分大小写）。若缺少关键词 "JSON"，API 会抛出错误：`'messages' must contain the word 'json' in some form`。
              required:
                - type
                - schema
              properties:
                type:
                  type: string
                  enum:
                    - json_schema
                  description: 固定值：`json_schema`。
                schema:
                  type: object
                  description: 遵循标准 JSON Schema 规范的 JSON Schema 对象。应包含 `type`（数据类型）、`properties`（字段定义）、`required`（必填字段名数组）和 `additionalProperties`（必须设为 `false`）等字段。
    AnthropicMessage:
      type: object
      description: 非流式响应的消息对象。
      properties:
        id:
          type: string
          description: 消息的唯一标识。
        type:
          type: string
          enum:
            - message
          description: 固定为 `message`。
        role:
          type: string
          enum:
            - assistant
          description: 固定为 `assistant`。
        model:
          type: string
          description: 使用的模型名称。
        content:
          type: array
          description: 内容数组，元素类型可为 `text`（文本信息）、`thinking`（思考信息，开启深度思考时返回）或 `tool_use`（工具调用信息）。
          items:
            type: object
            properties:
              type:
                type: string
                enum:
                  - text
                  - thinking
                  - tool_use
                description: 内容块类型。
              text:
                type: string
                description: "`text` 类型时的模型生成文本回复。"
              thinking:
                type: string
                description: "`thinking` 类型时的模型思考过程。"
              signature:
                type: string
                description: "`thinking` 类型时的签名，当前固定为空字符串。"
              id:
                type: string
                description: "`tool_use` 类型时的工具调用唯一标识。"
              name:
                type: string
                description: "`tool_use` 类型时被调用的工具名称。"
              input:
                type: object
                description: "`tool_use` 类型时的工具调用入参。"
        stop_reason:
          type: string
          enum:
            - end_turn
            - max_tokens
            - tool_use
          description: 停止原因：`end_turn`（正常结束）、`max_tokens`（达到 Token 上限）、`tool_use`（工具调用）。
        stop_sequence:
          type:
            - string
            - "null"
          description: 固定为 `null`。
        usage:
          $ref: "#/components/schemas/AnthropicUsage"
    AnthropicStreamEvent:
      type: object
      description: 流式响应事件。事件按以下顺序发送：`message_start` → `content_block_start` → `content_block_delta`（重复） → `content_block_stop` → `message_delta` → `message_stop`。此外会定期发送 `ping` 事件（`{"type":"ping"}`）用于保持连接活跃，客户端可忽略。
      properties:
        type:
          type: string
          enum:
            - message_start
            - content_block_start
            - content_block_delta
            - content_block_stop
            - message_delta
            - message_stop
            - ping
          description: 事件类型。`message_start`：流的第一个事件，标记消息开始，含初始消息对象。`content_block_start`：每个内容块开始时发送，标记新内容块的索引和类型。`content_block_delta`：内容块的增量更新，`delta.type` 取值 `text_delta`（含 `text` 字段）、`thinking_delta`（含 `thinking` 字段）、`signature_delta`（含 `signature` 字段，当前固定为空字符串）或 `input_json_delta`（含 `partial_json` 字段）。`content_block_stop`：内容块结束事件。`message_delta`：消息级更新，含 `stop_reason`、`stop_sequence` 和完整的 Token 用量统计。`message_stop`：流的最后一个事件。
        index:
          type: integer
          description: 内容块索引（`content_block_start`、`content_block_delta`、`content_block_stop` 事件中出现）。
        message:
          type: object
          description: "`message_start` 事件中的初始消息对象，`content` 为空数组。"
        content_block:
          type: object
          description: "`content_block_start` 事件中的初始内容块对象。`type` 取值为 `text`、`thinking` 或 `tool_use`。"
        delta:
          type: object
          description: "`content_block_delta` 事件中的增量对象或 `message_delta` 事件中的停止信息。"
        usage:
          $ref: "#/components/schemas/AnthropicUsage"
    AnthropicUsage:
      type: object
      description: Token 用量统计。流式调用中，`message_start` 事件的 `usage` 仅包含 `input_tokens` 和 `output_tokens`；完整 4 个字段在 `message_delta` 事件中返回。
      properties:
        input_tokens:
          type: integer
          description: 输入 Token 数量。
        output_tokens:
          type: integer
          description: 输出 Token 数量。
        cache_creation_input_tokens:
          type: integer
          description: 缓存创建消耗的输入 Token 数量。
        cache_read_input_tokens:
          type: integer
          description: 缓存读取消耗的输入 Token 数量。
    AnthropicErrorResponse:
      type: object
      description: 错误响应。
      properties:
        type:
          type: string
          enum:
            - error
          description: 固定为 `error`。
        error:
          type: object
          properties:
            type:
              type: string
              description: 错误类型，如 `invalid_request_error`、`authentication_error`、`rate_limit_error`。
            message:
              type: string
              description: 错误详情。
````

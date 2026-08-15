> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 创建响应

> 兼容 Responses API

<Warning>
  旧版 URL 路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 即将停止维护，请尽快迁移至新版路径 `/compatible-mode/v1/responses`。
</Warning>

## 与 OpenAI 的兼容性

本 API 兼容 OpenAI，但在参数、功能和行为上存在差异。

请求仅处理本文档中列出的参数，未提及的 OpenAI 参数将被忽略。

主要差异：

- **不支持的参数**：部分参数不支持，例如 `background`（仅支持同步调用）。

- **扩展参数**：支持 OpenAI 规范之外的额外参数，例如 `enable_thinking`。

## OpenAPI

````yaml post /compatible-mode/v1/responses
openapi: 3.1.0
info:
  title: Qwen OpenAI 兼容 Responses API
  description: 使用 OpenAI 兼容 Responses API 调用通义模型。支持内置工具、基于 `previous_response_id` 的多轮上下文管理，以及思考模式。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com
    description: 北京
security:
  - BearerAuth: []
paths:
  /compatible-mode/v1/responses:
    post:
      operationId: openaiResponses
      summary: 创建响应
      description: 向通义模型发送输入内容，通过 OpenAI 兼容的 Responses API 获取生成的响应。支持内置工具（联网搜索、代码解释器、网页抓取、图片搜索、MCP、知识库检索）、通过 `previous_response_id` 进行多轮上下文管理，以及思考模式。
      parameters:
        - name: x-dashscope-session-cache
          in: header
          required: false
          schema:
            type: string
            enum:
              - enable
              - disable
            default: disable
          description: |-
            控制多轮对话中的[会话缓存](/developer-guides/run-and-scale/context-cache#session-cache)（需配合 `previous_response_id` 使用）。启用后，服务器将自动缓存对话上下文，从而降低延迟和费用。

            - `enable`：启用会话缓存。缓存创建按标准输入价格的 125% 计费；缓存命中按 10% 计费。缓存有效期为 5 分钟（命中后重置）。创建缓存至少需要 1024 个 Token。
            - `disable`（默认值）：禁用会话缓存。如模型支持，则回退到隐式缓存。

            支持的模型：`qwen3.8-max`、`qwen3.7-max`、`qwen3.7-max-2026-06-08`、`qwen3.7-max-2026-05-20`、`qwen3-max`、`qwen3.7-plus`、`qwen3.7-plus-2026-05-26`、`qwen3.6-plus`、`qwen3.5-plus`、`qwen3.7-flash`、`qwen3.6-flash`、`qwen3.5-flash`、`qwen-plus`、`qwen-flash`、`qwen3-coder-plus`、`qwen3-coder-flash`。

            SDK 传参方式：Python 使用 `default_headers`，Node.js 使用 `defaultHeaders`。
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/ResponsesRequest"
            example:
              model: qwen3.8-max
              input: What can you do?
      responses:
        "200":
          description: 请求成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ResponseObject"
              example:
                created_at: 1771165900
                id: f75c28fb-4064-48ed-90da-4d2cc4362xxx
                model: qwen3.8-max
                object: response
                output:
                  - content:
                      - annotations: []
                        text: Hello! I am Qwen3.5, a large language model developed by Alibaba Cloud with knowledge up to 2026, designed to assist you with complex reasoning, creative tasks, and multilingual conversations.
                        type: output_text
                    id: msg_89ad23e6-f128-4d4c-b7a1-a786e7880xxx
                    role: assistant
                    status: completed
                    type: message
                parallel_tool_calls: false
                status: completed
                tool_choice: auto
                tools: []
                usage:
                  input_tokens: 57
                  input_tokens_details:
                    cached_tokens: 0
                  output_tokens: 44
                  output_tokens_details:
                    reasoning_tokens: 0
                  total_tokens: 101
                  x_details:
                    - input_tokens: 57
                      output_tokens: 44
                      total_tokens: 101
                      x_billing_type: response_api
            text/event-stream:
              schema:
                $ref: "#/components/schemas/ResponseChunk"
              examples:
                basic_call:
                  summary: 基础调用
                  value:
                    response:
                      id: 428c90e9-9cd6-90a6-9726-c02b08ebexxx
                      created_at: 1769082930
                      object: response
                      status: queued
                    sequence_number: 0
                    type: response.created
                web_scraping:
                  summary: 网页抓取
                  value:
                    sequence_number: 2
                    item:
                      summary: []
                      type: reasoning
                      id: msg_5bd0c6df-19b8-4a04-bc00-8042a224exxx
                    output_index: 0
                    type: response.output_item.added
                text_to_image_search:
                  summary: 文生图搜索
                  value:
                    sequence_number: 11
                    item:
                      name: web_search_image
                      arguments: '{"queries": ["cat picture", "cute cat"]}'
                      id: msg_xxx
                      type: web_search_image_call
                      status: in_progress
                    output_index: 1
                    type: response.output_item.added
                image_search:
                  summary: 图片搜索
                  value:
                    sequence_number: 29
                    item:
                      name: image_search
                      arguments: '{"img_idx": 0, "bbox": [0, 0, 1000, 1000]}'
                      id: msg_xxx
                      type: image_search_call
                      status: in_progress
                    output_index: 1
                    type: response.output_item.added
                mcp:
                  summary: MCP
                  value:
                    sequence_number: 28
                    item:
                      name: amap-maps-maps_weather
                      server_label: MCP Server
                      arguments: '{"city": "Beijing"}'
                      id: msg_xxx
                      type: mcp_call
                      status: in_progress
                    output_index: 1
                    type: response.output_item.added
                knowledge_base_search:
                  summary: 知识库检索
                  value:
                    sequence_number: 18
                    item:
                      id: msg_xxx
                      type: file_search_call
                      queries:
                        - Bailian X1 phone
                        - Bailian X1
                      status: in_progress
                    output_index: 1
                    type: response.output_item.added
        "400":
          description: 请求参数无效
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
              example:
                request_id: 0bf11b24-0c67-95da-bb15-f85dabcfdb7f
                code: InvalidParameter
                message: "[400] missing_required_parameter: Missing required parameter: 'model'."
        "401":
          description: 认证失败
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
              example:
                request_id: 5dc15bba-5586-9f64-980f-c36b679d9a65
                code: InvalidApiKey
                message: Invalid API-key provided.
        "429":
          description: 请求频率超出限制。该接口的频率限制错误通过 HTTP 200 而非 429 状态码返回。响应体为 ResponseObject 格式，其中 `status` 为 `"failed"`，`error` 字段包含错误详情。请以响应体中的 `status` 字段为准，而非 HTTP 状态码。
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ResponseObject"
              example:
                created_at: 1775189716
                error:
                  code: server_error
                  message: Operation model request rate limit exceeded, please try again later.
                id: resp_e158ca4e-a71c-9a8b-aebe-169a650508d0
                model: ""
                object: response
                output: []
                parallel_tool_calls: false
                status: failed
                tool_choice: auto
                tools: []
      x-codeSamples:
        - lang: python
          label: 基础调用
          source: |-
            import os
            from openai import OpenAI

            client = OpenAI(
              # 若未设置环境变量，请替换为：api_key="sk-xxx"
              api_key=os.getenv("DASHSCOPE_API_KEY"),
              base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            )

            response = client.responses.create(
              model="qwen3.8-max",
              input="What can you do?"
            )

            # 获取模型回复
            print(response.output_text)
        - lang: javascript
          label: 基础调用
          source: |-
            import OpenAI from "openai";

            const openai = new OpenAI({
              // 若未设置环境变量，请替换为：apiKey: "sk-xxx"
              apiKey: process.env.DASHSCOPE_API_KEY,
              baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
            });

            async function main() {
              const response = await openai.responses.create({
                model: "qwen3.8-max",
                input: "What can you do?"
              });

              // 获取模型回复
              console.log(response.output_text);
            }

            main();
        - lang: curl
          label: 基础调用
          source: |-
            curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/responses \
            -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
            -H "Content-Type: application/json" \
            -d '{
              "model": "qwen3.8-max",
              "input": "What can you do?"
            }'
        - lang: python
          label: 流式输出
          source: |-
            import os
            from openai import OpenAI

            client = OpenAI(
              api_key=os.getenv("DASHSCOPE_API_KEY"),
              base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            )

            stream = client.responses.create(
              model="qwen3.8-max",
              input="Please briefly introduce artificial intelligence.",
              stream=True
            )

            print("Receiving stream output:")
            for event in stream:
              if event.type == 'response.output_text.delta':
                print(event.delta, end='', flush=True)
              elif event.type == 'response.completed':
                print("\nStream completed")
                print(f"Total tokens: {event.response.usage.total_tokens}")
        - lang: javascript
          label: 流式输出
          source: |-
            import OpenAI from "openai";

            const openai = new OpenAI({
              apiKey: process.env.DASHSCOPE_API_KEY,
              baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
            });

            async function main() {
              const stream = await openai.responses.create({
                model: "qwen3.8-max",
                input: "Please briefly introduce artificial intelligence.",
                stream: true
              });

              console.log("Receiving stream output:");
              for await (const event of stream) {
                if (event.type === 'response.output_text.delta') {
                  process.stdout.write(event.delta);
                } else if (event.type === 'response.completed') {
                  console.log("\nStream completed");
                  console.log(`Total tokens: ${event.response.usage.total_tokens}`);
                }
              }
            }

            main();
        - lang: curl
          label: 流式输出
          source: |-
            curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/responses \
            -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
            -H "Content-Type: application/json" \
            --no-buffer \
            -d '{
              "model": "qwen3.8-max",
              "input": "Please briefly introduce artificial intelligence.",
              "stream": true
            }'
        - lang: python
          label: 多轮对话
          source: |-
            import os
            from openai import OpenAI

            client = OpenAI(
              api_key=os.getenv("DASHSCOPE_API_KEY"),
              base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            )

            # 第一轮对话
            response1 = client.responses.create(
              model="qwen3.8-max",
              input="我的名字是张三，请记住。"
            )
            print(f"第一轮回复: {response1.output_text}")

            # 第二轮对话 - 使用 previous_response_id 关联上下文
            response2 = client.responses.create(
              model="qwen3.8-max",
              input="你还记得我的名字吗？",
              previous_response_id=response1.id
            )
            print(f"第二轮回复: {response2.output_text}")
        - lang: javascript
          label: 多轮对话
          source: |-
            import OpenAI from "openai";

            const openai = new OpenAI({
              apiKey: process.env.DASHSCOPE_API_KEY,
              baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
            });

            async function main() {
              const response1 = await openai.responses.create({
                model: "qwen3.8-max",
                input: "我的名字是张三，请记住。"
              });
              console.log(`第一轮回复: ${response1.output_text}`);

              const response2 = await openai.responses.create({
                model: "qwen3.8-max",
                input: "你还记得我的名字吗？",
                previous_response_id: response1.id
              });
              console.log(`第二轮回复: ${response2.output_text}`);
            }

            main();
        - lang: curl
          label: 多轮对话
          source: |-
            # 第一轮对话
            curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/responses \
            -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
            -H "Content-Type: application/json" \
            -d '{
              "model": "qwen3.8-max",
              "input": "我的名字是张三，请记住。"
            }'

            # 第二轮对话 - 使用上一轮返回的 id 作为 previous_response_id
            curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/responses \
            -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
            -H "Content-Type: application/json" \
            -d '{
              "model": "qwen3.8-max",
              "input": "你还记得我的名字吗？",
              "previous_response_id": "上一轮返回的响应id"
            }'
        - lang: python
          label: 深度思考
          source: |-
            import os
            from openai import OpenAI

            client = OpenAI(
              api_key=os.getenv("DASHSCOPE_API_KEY"),
              base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            )

            response = client.responses.create(
              model="qwen3.8-max",
              input="9.9和9.11谁大？",
              reasoning={"effort": "medium"}
            )

            for item in response.output:
              if item.type == "reasoning":
                print("=== 思考过程 ===")
                for summary in item.summary:
                  print(summary.text)
              elif item.type == "message":
                print("\n=== 最终答案 ===")
                print(item.content[0].text)

            print(f"\n思考 Token 数: {response.usage.output_tokens_details.reasoning_tokens}")
        - lang: javascript
          label: 深度思考
          source: |-
            import OpenAI from "openai";

            const openai = new OpenAI({
              apiKey: process.env.DASHSCOPE_API_KEY,
              baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
            });

            async function main() {
              const response = await openai.responses.create({
                model: "qwen3.8-max",
                input: "9.9和9.11谁大？",
                reasoning: { effort: "medium" }
              });

              for (const item of response.output) {
                if (item.type === "reasoning") {
                  console.log("=== 思考过程 ===");
                  for (const summary of item.summary) {
                    console.log(summary.text);
                  }
                } else if (item.type === "message") {
                  console.log("\n=== 最终答案 ===");
                  console.log(item.content[0].text);
                }
              }
              console.log(`\n思考 Token 数: ${response.usage.output_tokens_details.reasoning_tokens}`);
            }

            main();
        - lang: curl
          label: 深度思考
          source: |-
            curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/responses \
            -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
            -H "Content-Type: application/json" \
            -d '{
              "model": "qwen3.8-max",
              "input": "9.9和9.11谁大？",
              "reasoning": {"effort": "medium"}
            }'
        - lang: python
          label: 调用内置工具
          source: |-
            import os
            from openai import OpenAI

            client = OpenAI(
              api_key=os.getenv("DASHSCOPE_API_KEY"),
              base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            )

            response = client.responses.create(
              model="qwen3.8-max",
              input="帮我搜索一下今天杭州的天气",
              tools=[
                {"type": "web_search"},
                {"type": "code_interpreter"},
                {"type": "web_extractor"}
              ],
              reasoning={"effort": "medium"}
            )

            print(response.output_text)
        - lang: javascript
          label: 调用内置工具
          source: |-
            import OpenAI from "openai";

            const openai = new OpenAI({
              apiKey: process.env.DASHSCOPE_API_KEY,
              baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
            });

            async function main() {
              const response = await openai.responses.create({
                model: "qwen3.8-max",
                input: "帮我搜索一下今天杭州的天气",
                tools: [
                  { type: "web_search" },
                  { type: "code_interpreter" },
                  { type: "web_extractor" }
                ],
                reasoning: { effort: "medium" }
              });

              for (const item of response.output) {
                if (item.type === "reasoning") {
                  console.log("模型正在思考...");
                } else if (item.type === "web_search_call") {
                  console.log(`搜索查询: ${item.action.query}`);
                } else if (item.type === "message") {
                  console.log(`回复: ${item.content[0].text}`);
                }
              }
            }

            main();
        - lang: curl
          label: 调用内置工具
          source: |-
            curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/responses \
            -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
            -H "Content-Type: application/json" \
            -d '{
              "model": "qwen3.8-max",
              "input": "帮我搜索一下今天杭州的天气",
              "tools": [
                {"type": "web_search"},
                {"type": "code_interpreter"},
                {"type": "web_extractor"}
              ],
              "reasoning": {"effort": "medium"}
            }'
        - lang: python
          label: Session 缓存
          source: |-
            import os
            from openai import OpenAI

            client = OpenAI(
              api_key=os.getenv("DASHSCOPE_API_KEY"),
              base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
              default_headers={"x-dashscope-session-cache": "enable"}
            )

            # 构造长文本触发缓存（需超过 1024 Token）
            long_context = "人工智能是计算机科学的一个重要分支。" * 50

            response1 = client.responses.create(
              model="qwen3.8-max",
              input=long_context + "\n\n请简短介绍随机森林算法。"
            )
            print(f"第一轮回复: {response1.output_text}")

            # 第二轮对话，缓存由服务端自动处理
            response2 = client.responses.create(
              model="qwen3.8-max",
              input="它和 GBDT 有什么主要区别？",
              previous_response_id=response1.id
            )
            print(f"第二轮回复: {response2.output_text}")
            print(f"缓存命中 Token: {response2.usage.input_tokens_details.cached_tokens}")
        - lang: javascript
          label: Session 缓存
          source: |-
            import OpenAI from "openai";

            const openai = new OpenAI({
              apiKey: process.env.DASHSCOPE_API_KEY,
              baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
              defaultHeaders: { "x-dashscope-session-cache": "enable" }
            });

            const longContext = "人工智能是计算机科学的一个重要分支。".repeat(50);

            async function main() {
              const response1 = await openai.responses.create({
                model: "qwen3.8-max",
                input: longContext + "\n\n请简短介绍随机森林算法。"
              });
              console.log(`第一轮回复: ${response1.output_text}`);

              const response2 = await openai.responses.create({
                model: "qwen3.8-max",
                input: "它和 GBDT 有什么主要区别？",
                previous_response_id: response1.id
              });
              console.log(`第二轮回复: ${response2.output_text}`);
              console.log(`缓存命中 Token: ${response2.usage.input_tokens_details.cached_tokens}`);
            }

            main();
        - lang: curl
          label: Session 缓存
          source: |-
            # 第一轮对话（input 需超过 1024 Token 以触发缓存）
            curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/responses \
            -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
            -H "Content-Type: application/json" \
            -H "x-dashscope-session-cache: enable" \
            -d '{
              "model": "qwen3.8-max",
              "input": "人工智能是计算机科学的一个重要分支...（重复至超过1024 Token）\n\n请简短介绍随机森林算法。"
            }'

            # 第二轮对话 - 使用 previous_response_id 关联上下文
            curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/responses \
            -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
            -H "Content-Type: application/json" \
            -H "x-dashscope-session-cache: enable" \
            -d '{
              "model": "qwen3.8-max",
              "input": "它和 GBDT 有什么主要区别？",
              "previous_response_id": "上一轮返回的响应id"
            }'
        - lang: python
          label: Function calling
          source: |-
            from openai import OpenAI
            import json
            import os
            import random

            client = OpenAI(
              api_key=os.getenv("DASHSCOPE_API_KEY"),
              base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            )

            tools = [
              {
                "type": "function",
                "name": "get_current_weather",
                "description": "当你想查询指定城市的天气时非常有用。",
                "parameters": {
                  "type": "object",
                  "properties": {
                    "location": {
                      "type": "string",
                      "description": "城市或县区，比如北京市、杭州市、余杭区等。",
                    }
                  },
                  "required": ["location"],
                },
              }
            ]

            def get_current_weather(arguments):
              weather_conditions = ["晴天", "多云", "雨天"]
              random_weather = random.choice(weather_conditions)
              location = arguments["location"]
              return f"{location}今天是{random_weather}。"

            def get_response(input_data):
              response = client.responses.create(
                model="qwen3.8-max",
                input=input_data,
                tools=tools,
              )
              return response

            conversation = [{"role": "user", "content": "北京天气咋样"}]
            response = get_response(conversation)
            function_calls = [item for item in response.output if item.type == "function_call"]

            if not function_calls:
              print(f"助手最终回复：{response.output_text}")
            else:
              while function_calls:
                for fc in function_calls:
                  arguments = json.loads(fc.arguments)
                  print(f"正在调用工具 [{fc.name}]，参数：{arguments}")
                  tool_result = get_current_weather(arguments)
                  print(f"工具返回：{tool_result}")
                  conversation.append({
                    "type": "function_call",
                    "name": fc.name,
                    "arguments": fc.arguments,
                    "call_id": fc.call_id,
                  })
                  conversation.append({
                    "type": "function_call_output",
                    "call_id": fc.call_id,
                    "output": tool_result,
                  })
                response = get_response(conversation)
                function_calls = [item for item in response.output if item.type == "function_call"]
              print(f"助手最终回复：{response.output_text}")
        - lang: javascript
          label: Function calling
          source: |-
            import OpenAI from "openai";

            const openai = new OpenAI({
              apiKey: process.env.DASHSCOPE_API_KEY,
              baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
            });

            const tools = [
              {
                type: "function",
                name: "get_current_weather",
                description: "当你想查询指定城市的天气时非常有用。",
                parameters: {
                  type: "object",
                  properties: {
                    location: {
                      type: "string",
                      description: "城市或县区，比如北京市、杭州市、余杭区等。",
                    },
                  },
                  required: ["location"],
                },
              },
            ];

            const getCurrentWeather = (args) => {
              const weatherConditions = ["晴天", "多云", "雨天"];
              const randomWeather = weatherConditions[Math.floor(Math.random() * weatherConditions.length)];
              return `${args.location}今天是${randomWeather}。`;
            };

            const getResponse = async (inputData) => {
              return await openai.responses.create({
                model: "qwen3.8-max",
                input: inputData,
                tools: tools,
              });
            };

            async function main() {
              const conversation = [{ role: "user", content: "北京天气" }];
              let response = await getResponse(conversation);
              let functionCalls = response.output.filter(item => item.type === "function_call");

              if (functionCalls.length === 0) {
                console.log(`助手最终回复：${response.output_text}`);
              } else {
                while (functionCalls.length > 0) {
                  for (const fc of functionCalls) {
                    const args = JSON.parse(fc.arguments);
                    console.log(`正在调用工具 [${fc.name}]，参数：`, args);
                    const toolResult = getCurrentWeather(args);
                    console.log(`工具返回：${toolResult}`);
                    conversation.push({ type: "function_call", name: fc.name, arguments: fc.arguments, call_id: fc.call_id });
                    conversation.push({ type: "function_call_output", call_id: fc.call_id, output: toolResult });
                  }
                  response = await getResponse(conversation);
                  functionCalls = response.output.filter(item => item.type === "function_call");
                }
                console.log(`助手最终回复：${response.output_text}`);
              }
            }

            main().catch(console.error);
        - lang: python
          label: 文档理解
          source: |-
            import os
            from openai import OpenAI

            client = OpenAI(
              api_key=os.getenv("DASHSCOPE_API_KEY"),
              base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            )

            response = client.responses.create(
              model="qwen3.5-ocr",
              input=[
                {
                  "role": "user",
                  "content": [
                    {
                      "type": "input_file",
                      "file_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260616/qmycjl/1506.02640v5.pdf",
                    },
                    {
                      "type": "input_text",
                      "text": "Read all the text in the file.",
                    },
                  ],
                }
              ],
              extra_body={
                "ocr_options": {}
              },
            )
            print(response.output_text)
        - lang: javascript
          label: 文档理解
          source: |-
            import OpenAI from "openai";

            const client = new OpenAI({
              apiKey: process.env.DASHSCOPE_API_KEY,
              baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
            });

            async function main() {
              const response = await client.responses.create({
                model: "qwen3.5-ocr",
                input: [{
                  role: "user",
                  content: [{
                    type: "input_file",
                    file_url: "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260616/qmycjl/1506.02640v5.pdf"
                  }]
                }],
                ocr_options: {}
              });
              console.log(response.output_text);
            }

            main();
        - lang: curl
          label: 文档理解
          source: |-
            curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/responses \
            -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
            -H "Content-Type: application/json" \
            -d '{
              "model": "qwen3.5-ocr",
              "input": [
                {
                  "role": "user",
                  "content": [
                    {
                      "type": "input_file",
                      "file_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260616/qmycjl/1506.02640v5.pdf"
                    },
                    {
                      "type": "input_text",
                      "text": "Read all the text in the file."
                    }
                  ]
                }
              ],
              "ocr_options": {}
            }'
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    ResponsesRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称。支持的模型包括 qwen3.8-max、qwen3.7-max、qwen3.7-max-2026-06-08、qwen3.7-max-2026-05-20、qwen3.7-max-preview、qwen3.7-max-2026-05-17、qwen3-max、qwen3-max-2026-01-23、qwen3.7-plus、qwen3.7-plus-2026-05-26、qwen3.6-plus、qwen3.6-plus-2026-04-02、qwen3.5-plus、qwen3.5-plus-2026-04-20、qwen3.5-plus-2026-02-15、qwen3.7-flash、qwen3.7-flash-2026-07-15、qwen3.6-flash、qwen3.6-flash-2026-04-16、qwen3.5-flash、qwen3.5-flash-2026-02-23、qwen3.8-2.4t-a95b、qwen3.6-35b-a3b、qwen3.5-397b-a17b、qwen3.5-122b-a10b、qwen3.5-27b、qwen3.5-35b-a3b、qwen-plus、qwen-flash、qwen3-coder-plus、qwen3-coder-flash、qwen3.5-ocr、qwen-plus-character、qwen-flash-character、deepseek-v4-pro-0813、deepseek-v4-pro、deepseek-v4-flash、deepseek-v4-flash-0731。
        input:
          oneOf:
            - type: string
              description: 纯文本输入，例如 "你好"。
            - type: array
              description: 按对话顺序排列的消息数组。
              items:
                oneOf:
                  - $ref: "#/components/schemas/SystemMessage"
                  - $ref: "#/components/schemas/DeveloperMessage"
                  - $ref: "#/components/schemas/UserMessage"
                  - $ref: "#/components/schemas/AssistantMessage"
                  - $ref: "#/components/schemas/WebSearchCallInput"
          description: 模型的输入内容。支持纯文本字符串，或按对话顺序排列的消息数组。
        instructions:
          type: string
          description: 插入到上下文开头的系统指令。使用 `previous_response_id` 时，上一轮中指定的 instructions 不会延续到当前上下文。
        previous_response_id:
          type: string
          description: 上一轮响应的唯一 ID，有效期为 7 天。通过该参数可实现多轮对话，服务器会自动检索并将上一轮的输入和输出作为上下文传入。若同时提供了消息数组和 `previous_response_id`，input 中的新消息将追加到历史上下文之后。不能与 `conversation` 同时使用。使用示例请参考[多轮对话指南](/developer-guides/run-and-scale/multi-turn)。
        conversation:
          type: string
          description: 当前响应所属的会话。会话中的历史记录将自动作为上下文传入当前请求，当前请求的输入和输出也会在响应完成后自动添加到会话中。不能与 `previous_response_id` 同时使用。
        stream:
          type: boolean
          default: false
          description: 是否启用流式输出。设置为 `true` 时，模型响应数据将实时以流的形式返回给客户端。
        store:
          type: boolean
          default: true
          description: |-
            是否储存本次会话生成的模型响应。

            - `true`：储存，当前模型响应可被 `previous_response_id` 和后续 API 使用。
            - `false`：不储存，对话内容不能被 `previous_response_id` 和后续 API 使用。
        tools:
          type: array
          description: |-
            模型可使用的工具列表。支持的工具类型：`web_search`、`code_interpreter`、`web_extractor`、`web_search_image`、`image_search`、`file_search`、`mcp`、`function`。

            **内置工具**使用 `{"type": "<tool_name>"}` 格式。例如：`{"type": "web_search"}`。

            **MCP 工具**使用以下格式：
            ```json
            {
                "type": "mcp",
                "server_protocol": "sse",
                "server_label": "amap-maps",
                "server_description": "AMAP MCP Server...",
                "server_url": "https://dashscope.aliyuncs.com/api/v1/mcps/amap-maps/sse",
                "headers": {
                    "Authorization": "Bearer $DASHSCOPE_API_KEY"
                }
            }
            ```

            **Function 工具**使用以下格式：
            ```json
            [{
              "type": "function",
              "name": "get_weather",
              "description": "Get weather information for a specified city",
              "parameters": {
                "type": "object",
                "properties": {
                  "city": {
                    "type": "string",
                    "description": "The name of the city"
                  }
                },
                "required": ["city"]
              }
            }]
            ``` 使用示例请参考[函数调用指南](/developer-guides/tool-calling/function-calling)和[联网搜索指南](/developer-guides/tool-calling/web-search)。
          items:
            type: object
            properties:
              type:
                type: string
                description: 工具类型。有效值：`web_search`、`code_interpreter`、`web_extractor`、`web_search_image`、`image_search`、`file_search`、`mcp`、`function`。
            required:
              - type
        tool_choice:
          description: |-
            控制模型选择和调用工具的方式。支持字符串格式和对象格式。

            **字符串格式：**
            - `auto`：模型自动决定是否调用工具。
            - `none`：阻止模型调用任何工具。
            - `required`：强制模型调用工具。仅当 tools 列表中只有一个工具时可用。

            **对象格式：**指定模型可使用的工具范围，模型只能从预定义的工具列表中选择并调用。
          oneOf:
            - type: string
              enum:
                - auto
                - none
                - required
              default: auto
            - type: object
              properties:
                mode:
                  type: string
                  enum:
                    - auto
                    - required
                  description: "`auto`：模型自动决定是否调用工具。`required`：强制模型调用工具。"
                tools:
                  type: array
                  description: '允许模型调用的工具定义列表。示例：`[{"type": "function", "name": "get_weather"}]`'
                  items:
                    type: object
                    properties:
                      type:
                        type: string
                        description: 工具的类型。
                      name:
                        type: string
                        description: 工具的名称。
                type:
                  type: string
                  enum:
                    - allowed_tools
                  description: 允许的工具配置类型。值必须为 `allowed_tools`。
        temperature:
          type: number
          description: 控制生成文本多样性的采样温度。温度越高，生成的文本越多样；温度越低，生成的文本越确定。取值范围：[0, 2)。`temperature` 和 `top_p` 都能控制生成文本的多样性，建议只设置其中一个。
        top_p:
          type: number
          description: 控制生成文本多样性的核采样概率阈值。`top_p` 越高，生成文本越多样；`top_p` 越低，生成文本越确定。取值范围：(0, 1.0]。`temperature` 和 `top_p` 都能控制生成文本的多样性，建议只设置其中一个。
        enable_thinking:
          type: boolean
          description: |-
            是否启用思考模式。设置为 `true` 时，模型在回复前会先进行思考，思考内容通过 `reasoning` 类型的输出项返回。推理 Token 计入 `output_tokens_details.reasoning_tokens`，并按推理 Token 价格计费。启用思考模式时，建议同时启用内置工具，以在复杂任务上获得最佳模型性能。

            **该参数不是标准 OpenAI 参数。** Python SDK 需通过 `extra_body={"enable_thinking": True}` 传递；Node.js SDK 和 curl 可直接在顶层参数中使用 `enable_thinking: true`。建议使用 `reasoning.effort` 替代，`enable_thinking` 后续将不再支持。
        reasoning:
          type: object
          description: 思考模式相关配置。
          properties:
            effort:
              type: string
              enum:
                - none
                - minimal
                - low
                - medium
                - high
                - xhigh
                - max
              default: xhigh
              description: 思考强度档位，默认值为 `xhigh`。支持 `none`、`minimal`、`low`、`medium`、`high`、`xhigh`、`max` 共 7 个递增档位。降低该值可加快响应速度并减少推理 Token 的消耗。
        max_output_tokens:
          type: integer
          minimum: 16
          description: |-
            输出 Token 的最大数量，最小值为 16。

            - **Qwen3.8 系列**：模型回复内容和思维链内容之和的最大 Token 数。
            - **其余模型**：模型回复内容的最大 Token 数。

            模型输出超过此值时生成将提前停止，状态为 `incomplete`。
        ocr_options:
          type: object
          description: |-
            OCR 内置任务参数，仅适用于 `qwen3.5-ocr` 模型。通过此参数调用内置 OCR 任务（如信息抽取、文字定位等），内置任务结果通过响应中的 `ocr_result` 字段返回。

            **该参数非 OpenAI 标准参数。** Python SDK 通过 `extra_body={"ocr_options": {...}}` 传递；Node.js SDK 和 curl 直接使用 `ocr_options` 作为顶层参数。
    SystemMessage:
      type: object
      description: 设置模型角色、语气、任务目标或约束条件的系统消息。
      required:
        - role
        - content
      properties:
        role:
          type: string
          enum:
            - system
          description: 消息角色。值必须为 `system`。
        content:
          type: string
          description: 系统指令内容，定义模型的角色、行为、回复风格和任务约束。
    DeveloperMessage:
      type: object
      description: 与系统消息功能相同的开发者消息，用于设置模型的角色和行为。
      properties:
        role:
          type: string
          enum:
            - developer
          description: 消息角色。值必须为 `developer`。
        content:
          type: string
          description: 开发者指令，定义模型的角色、行为、回复风格和任务约束。
    UserMessage:
      type: object
      description: 向模型传递问题、指令或上下文的用户消息。
      required:
        - role
        - content
      properties:
        role:
          type: string
          enum:
            - user
          description: 消息角色。值必须为 `user`。
        content:
          oneOf:
            - type: string
              description: 纯文本内容。
            - type: array
              description: 用于多模态输入的内容块数组。Responses API 目前不支持视频或音频输入，如需输入视频或音频，请使用 Chat Completions API 或 DashScope API。
              items:
                type: object
                required:
                  - type
                properties:
                  type:
                    type: string
                    enum:
                      - text
                      - image_url
                    description: 内容类型。文本输入设为 `text`，图片输入设为 `image_url`。
                  text:
                    type: string
                    description: "`type` 为 `text` 时必填，表示输入的文本内容。"
                  image_url:
                    type: object
                    description: "`type` 为 `image_url` 时必填，表示图片 URL 对象。"
                    properties:
                      url:
                        type: string
                        description: 输入图片的公共 URL 或 Base64 编码数据。
          description: 消息内容。仅含文本时为字符串类型；包含图片或启用显式缓存时为数组类型。
    AssistantMessage:
      type: object
      description: 包含模型历史回复的助手消息，用于在多轮对话中提供上下文。
      required:
        - role
        - content
      properties:
        role:
          type: string
          enum:
            - assistant
          description: 消息角色。值必须为 `assistant`。
        content:
          type: string
          description: 助手回复的文本内容。
    WebSearchCallInput:
      type: object
      description: 搜索调用对象。可直接将上一轮响应的 output 中的 web_search_call 项传回 input，用于在多轮对话中传递搜索结果上下文。
      required:
        - type
        - id
        - status
        - action
      properties:
        type:
          type: string
          enum:
            - web_search_call
          description: 固定为 `web_search_call`。
        id:
          type: string
          description: 搜索调用的唯一标识，来自上一轮响应。
        status:
          type: string
          enum:
            - in_progress
            - searching
            - completed
            - failed
          description: 搜索状态。
        action:
          type: object
          description: 搜索信息。仅支持 `search` 类型。
          required:
            - type
          properties:
            type:
              type: string
              enum:
                - search
              description: 搜索类型，固定为 `search`。
            queries:
              type: array
              items:
                type: string
              description: 搜索查询词列表。
            sources:
              type: array
              description: 搜索结果来源列表。
              items:
                type: object
                required:
                  - type
                  - url
                properties:
                  type:
                    type: string
                    enum:
                      - url
                    description: 来源类型，固定为 `url`。
                  url:
                    type: string
                    description: 来源 URL。
    ResponseObject:
      type: object
      description: 响应对象（非流式输出）。
      properties:
        id:
          type: string
          description: 本次响应的唯一 ID，有效期为 7 天。可将此 ID 传入 `previous_response_id` 参数以实现多轮对话。
        created_at:
          type: number
          description: 本次请求的 Unix 时间戳（秒）。
        object:
          type: string
          enum:
            - response
          description: 对象类型。值为 `response`。
        status:
          type: string
          enum:
            - completed
            - failed
            - in_progress
            - cancelled
            - queued
            - incomplete
          description: 响应生成的状态。
        model:
          type: string
          description: 生成本次响应所使用的模型 ID。
        output:
          type: array
          description: 模型生成的输出项数组。数组中元素的类型和顺序取决于模型的响应。
          items:
            $ref: "#/components/schemas/OutputItem"
        parallel_tool_calls:
          type: boolean
          description: 是否启用了并行工具调用。
        tool_choice:
          type: string
          description: 请求中 `tool_choice` 参数的回显值。有效值为 `auto`、`none` 和 `required`。
        tools:
          type: array
          description: 请求中 tools 参数的完整内容回显。结构与请求体中的 tools 参数相同。
          items:
            type: object
        error:
          type: object
          nullable: true
          description: 模型生成响应失败时返回的错误对象。成功时此字段为 `null`。
          properties:
            code:
              type: string
              description: 错误码。
            message:
              type: string
              description: 可读的错误信息。
        usage:
          $ref: "#/components/schemas/Usage"
    OutputItem:
      type: object
      description: 模型生成的输出项。
      properties:
        type:
          type: string
          enum:
            - message
            - reasoning
            - function_call
            - web_search_call
            - code_interpreter_call
            - web_extractor_call
            - web_search_image_call
            - image_search_call
            - mcp_call
            - file_search_call
          description: |-
            输出项的类型。
            - `message`：包含模型生成的最终回复内容。
            - `reasoning`：启用思考模式（`enable_thinking: true`）时返回。推理 Token 计入 `output_tokens_details.reasoning_tokens`，并按推理 Token 价格计费。
            - `function_call`：使用用户自定义 function 工具时返回，需要处理函数调用并返回结果。
            - `web_search_call`：使用 `web_search` 工具时返回。
            - `code_interpreter_call`：使用 `code_interpreter` 工具时返回。
            - `web_extractor_call`：使用 `web_extractor` 工具时返回，必须配合 `web_search` 工具使用。
            - `web_search_image_call`：使用 `web_search_image` 工具时返回，包含搜索到的图片列表。
            - `image_search_call`：使用 `image_search` 工具时返回，包含相似图片列表。
            - `mcp_call`：使用 `mcp` 工具时返回，包含 MCP 服务调用的结果。
            - `file_search_call`：使用 `file_search` 工具时返回，包含搜索查询和知识库检索结果。
        id:
          type: string
          description: 输出项的唯一标识符，所有类型的输出项均包含此字段。
        role:
          type: string
          enum:
            - assistant
          description: 消息角色。值为 `assistant`。仅当 type 为 `message` 时存在此字段。
        status:
          type: string
          enum:
            - completed
            - in_progress
          description: 输出项的生成状态。
        name:
          type: string
          description: 工具或函数名称。当 type 为 `function_call`、`web_search_image_call`、`image_search_call` 或 `mcp_call` 时存在此字段。对于 `web_search_image_call` 和 `image_search_call`，值固定为 `web_search_image` 和 `image_search`。对于 `mcp_call`，值为 MCP 服务中调用的具体函数名，例如 `amap-maps-maps_geo`。
        arguments:
          type: string
          description: |-
            工具调用的参数，为 JSON 字符串格式。当 type 为 `function_call`、`web_search_image_call`、`image_search_call` 或 `mcp_call` 时存在此字段。使用前需通过 `JSON.parse()` 解析。

            **各工具类型的参数内容：**
            - `web_search_image_call`：`{"queries": ["search term 1", "search term 2"]}`，其中 queries 为模型自动生成的搜索词列表。
            - `image_search_call`：`{"img_idx": 0, "bbox": [0, 0, 1000, 1000]}`，其中 `img_idx` 为输入图片的索引（从 0 开始），`bbox` 为搜索区域的边界框坐标 `[x1, y1, x2, y2]`，范围为 0-1000。
            - `function_call`：根据用户自定义函数参数的 schema 生成的参数对象。
            - `mcp_call`：MCP 服务中调用的函数的参数对象。
        call_id:
          type: string
          description: 函数调用的唯一标识符。仅当 type 为 `function_call` 时存在此字段。返回函数调用结果时，必须使用此 ID 关联请求与响应。
        content:
          type: array
          description: 消息内容数组。仅当 type 为 `message` 时存在此字段。
          items:
            type: object
            properties:
              type:
                type: string
                enum:
                  - output_text
                description: 内容类型。值为 `output_text`。
              text:
                type: string
                description: 模型生成的文本内容。
              annotations:
                type: array
                description: 文本注释数组。通常为空数组。
                items:
                  type: object
        summary:
          type: array
          description: 推理摘要数组。仅当 type 为 `reasoning` 时存在此字段。每个元素包含 `type` 字段（值为 `summary_text`）和 `text` 字段（包含摘要文本）。
          items:
            type: object
            properties:
              type:
                type: string
                enum:
                  - summary_text
              text:
                type: string
        action:
          type: object
          description: 搜索动作信息。仅当 type 为 `web_search_call` 时存在此字段。
          properties:
            query:
              type: string
              description: 搜索查询关键词。
            type:
              type: string
              enum:
                - search
              description: 搜索类型。值为 `search`。
            sources:
              type: array
              description: 搜索来源列表。每个元素包含 `type` 字段和 `url` 字段。
              items:
                type: object
                properties:
                  type:
                    type: string
                  url:
                    type: string
        code:
          type: string
          description: 模型生成并执行的代码。仅当 type 为 `code_interpreter_call` 时存在此字段。
        outputs:
          type: array
          description: 代码执行输出数组。仅当 type 为 `code_interpreter_call` 时存在此字段。每个元素包含 `type` 字段（值为 `logs`）和 `logs` 字段（包含代码执行日志）。
          items:
            type: object
            properties:
              type:
                type: string
                enum:
                  - logs
              logs:
                type: string
        container_id:
          type: string
          description: 代码解释器容器的标识符。仅当 type 为 `code_interpreter_call` 时存在此字段。用于在同一会话中关联多次代码执行。
        goal:
          type: string
          description: 提取目标的描述，说明需要从网页中提取哪些信息。仅当 type 为 `web_extractor_call` 时存在此字段。
        output:
          type: string
          description: |-
            工具调用的输出结果，为字符串格式。
            - 当 type 为 `web_extractor_call` 时，为提取的网页内容摘要。
            - 当 type 为 `web_search_image_call` 或 `image_search_call` 时，为包含图片搜索结果数组的 JSON 字符串。每个元素包含 `title` 字段（图片标题）、`url` 字段（图片 URL）和 `index` 字段（序号）。
            - 当 type 为 `mcp_call` 时，为 MCP 服务返回的 JSON 字符串结果。
        urls:
          type: array
          description: 已抓取网页的 URL 列表。仅当 type 为 `web_extractor_call` 时存在此字段。
          items:
            type: string
        server_label:
          type: string
          description: MCP 服务标签。仅当 type 为 `mcp_call` 时存在此字段，用于标识本次调用使用的 MCP 服务。
        queries:
          type: array
          description: 用于知识库检索的查询列表。仅当 type 为 `file_search_call` 时存在此字段。数组元素为模型生成的搜索查询字符串。
          items:
            type: string
        results:
          type: array
          description: 知识库检索结果数组。仅当 type 为 `file_search_call` 时存在此字段。
          items:
            type: object
            properties:
              file_id:
                type: string
                description: 匹配文档的文件 ID。
              filename:
                type: string
                description: 匹配文档的文件名。
              score:
                type: number
                description: 匹配相关性分数，范围为 0 到 1。值越高表示相关性越强。
              text:
                type: string
                description: 匹配文档内容的片段。
    ResponseChunk:
      type: object
      description: 响应数据块对象（流式输出）。流式输出返回一系列 JSON 对象，每个对象包含用于标识事件类型的 `type` 字段和表示事件顺序的 `sequence_number` 字段。`response.completed` 事件标志流的结束。
      properties:
        type:
          type: string
          enum:
            - response.created
            - response.in_progress
            - response.output_item.added
            - response.content_part.added
            - response.output_text.delta
            - response.output_text.done
            - response.content_part.done
            - response.output_item.done
            - response.reasoning_text.delta
            - response.reasoning_text.done
            - response.web_search_call.in_progress
            - response.web_search_call.searching
            - response.web_search_call.completed
            - response.code_interpreter_call.in_progress
            - response.code_interpreter_call.interpreting
            - response.code_interpreter_call.completed
            - response.mcp_call.in_progress
            - response.mcp_call_arguments.delta
            - response.mcp_call_arguments.done
            - response.mcp_call.completed
            - response.custom_tool_call_input.delta
            - response.custom_tool_call_input.done
            - response.file_search_call.in_progress
            - response.file_search_call.searching
            - response.file_search_call.completed
            - response.completed
            - response.incomplete
          description: |-
            事件类型标识符。
            - `response.created`：响应创建时触发，状态为 `queued`。
            - `response.in_progress`：响应开始处理时触发，状态变为 `in_progress`。
            - `response.output_item.added`：向输出数组中新增输出项时触发。若 `item.type` 为 `web_extractor_call`，表示网页抓取工具调用已开始。
            - `response.content_part.added`：向输出项的 content 数组中新增内容块时触发。
            - `response.output_text.delta`：增量文本生成时触发，可触发多次，`delta` 字段包含新增的文本片段。
            - `response.output_text.done`：文本生成完成时触发，`text` 字段包含完整文本。
            - `response.content_part.done`：内容块生成完成时触发。
            - `response.output_item.done`：输出项生成完成时触发。若 `item.type` 为 `web_extractor_call`，表示网页抓取工具调用已完成。
            - `response.reasoning_text.delta`：（启用思考模式时）推理内容的增量文本。
            - `response.reasoning_text.done`：（启用思考模式时）推理内容生成完成。
            - `response.web_search_call.in_progress` / `searching` / `completed`：（使用 `web_search` 工具时）搜索状态变更事件。
            - `response.code_interpreter_call.in_progress` / `interpreting` / `completed`：（使用 `code_interpreter` 工具时）代码执行状态变更事件。
            - `response.mcp_call.in_progress`：（使用 `mcp` 工具时）MCP 服务调用开始。
            - `response.mcp_call_arguments.delta` / `response.mcp_call_arguments.done`：（使用 `mcp` 工具时）MCP 调用参数的增量和完成事件。
            - `response.mcp_call.completed`：（使用 `mcp` 工具时）MCP 服务调用完成。
            - `response.custom_tool_call_input.delta` / `response.custom_tool_call_input.done`：（使用自定义工具时）工具输入内容的增量文本和完成事件。
            - `response.file_search_call.in_progress` / `searching` / `completed`：（使用 `file_search` 工具时）知识库检索状态变更事件。
            - `response.completed`：响应生成完成时触发，响应对象包含完整响应（含用量信息），此事件标志流的结束。
            - `response.incomplete`：响应因达到 `max_output_tokens` 等限制而提前结束。

            **注意：** 使用 `web_extractor` 工具时，没有专用的事件类型标识符。网页抓取工具调用通过通用的 `response.output_item.added` 和 `response.output_item.done` 事件传达，通过 `item.type` 字段（值为 `web_extractor_call`）进行识别。

            **注意：** 使用 `web_search_image` 或 `image_search` 工具时，没有专用的中间状态事件。工具调用通过 `response.output_item.added`（调用开始）和 `response.output_item.done`（调用完成）事件传达。
        sequence_number:
          type: integer
          description: 事件序号，从 0 开始递增。可用于确保客户端按正确顺序处理事件。
        response:
          type: object
          description: 响应对象。出现在 `response.created`、`response.in_progress`、`response.completed` 和 `response.incomplete` 事件中。在 `response.completed` 和 `response.incomplete` 事件中，包含完整的响应数据（含输出和用量信息），结构与非流式响应的响应对象一致。
        item:
          type: object
          description: 输出项对象。出现在 `response.output_item.added` 和 `response.output_item.done` 事件中。在 added 事件中，为初始骨架，content 为空数组；在 done 事件中，为完整对象。
          properties:
            id:
              type: string
              description: 输出项的唯一标识符，例如 `msg_xxx`。
            type:
              type: string
              enum:
                - message
                - reasoning
                - web_search_call
                - web_search_image_call
                - image_search_call
                - mcp_call
                - file_search_call
              description: 输出项的类型。
            role:
              type: string
              enum:
                - assistant
              description: 消息角色。值为 `assistant`。仅当 type 为 `message` 时存在此字段。
            status:
              type: string
              enum:
                - in_progress
                - completed
              description: 生成状态。在 added 事件中，状态为 `in_progress`；在 done 事件中，状态为 `completed`。
            content:
              type: array
              description: 消息内容数组。在 added 事件中为空数组 `[]`；在 done 事件中包含完整的内容块对象，结构与 `part` 对象相同。
              items:
                type: object
        part:
          type: object
          description: 内容块对象。出现在 `response.content_part.added` 和 `response.content_part.done` 事件中。
          properties:
            type:
              type: string
              enum:
                - output_text
              description: 内容块类型。值为 `output_text`。
            text:
              type: string
              description: 文本内容。在 added 事件中为空字符串；在 done 事件中为完整文本。
            annotations:
              type: array
              description: 文本注释数组。通常为空数组。
              items:
                type: object
            logprobs:
              type: object
              nullable: true
              description: Token 的对数概率信息。目前为 `null`。
        delta:
          type: string
          description: 增量文本内容。出现在 `response.output_text.delta` 事件中，包含新增的文本片段。客户端应将所有 delta 片段拼接以获得完整文本。
        text:
          type: string
          description: 完整文本内容。出现在 `response.output_text.done` 事件中，包含内容块的完整文本，可用于验证拼接的 delta 结果。
        item_id:
          type: string
          description: 输出项的唯一标识符，用于关联同一输出项的相关事件。
        output_index:
          type: integer
          description: 输出项在 output 数组中的索引位置。
        content_index:
          type: integer
          description: 内容块在 content 数组中的索引位置。
    Usage:
      type: object
      description: 本次请求的 Token 消耗信息。
      properties:
        input_tokens:
          type: integer
          description: 输入 Token 数量。
        output_tokens:
          type: integer
          description: 模型输出的 Token 数量。
        total_tokens:
          type: integer
          description: 消耗的 Token 总数，即 `input_tokens` 与 `output_tokens` 之和。
        input_tokens_details:
          type: object
          description: 输入 Token 的细分类别。
          properties:
            cached_tokens:
              type: integer
              description: 命中缓存的 Token 数量。
        output_tokens_details:
          type: object
          description: 输出 Token 的细分类别。
          properties:
            reasoning_tokens:
              type: integer
              description: 思考过程中消耗的 Token 数量。
        x_details:
          type: array
          description: 按计费类型细分的 Token 详情。
          items:
            type: object
            properties:
              input_tokens:
                type: integer
                description: 输入 Token 数量。
              output_tokens:
                type: integer
                description: 模型输出的 Token 数量。
              total_tokens:
                type: integer
                description: 消耗的 Token 总数。
              x_billing_type:
                type: string
                description: 值为 `response_api`。
        x_tools:
          type: object
          description: '工具使用的统计信息。如使用了内置工具，此字段包含每个工具的调用次数。示例：`{"web_search": {"count": 1}}`'
    ErrorResponse:
      type: object
      properties:
        request_id:
          type: string
          description: 用于追踪和调试的唯一请求 ID。
        code:
          type: string
          description: 错误码。
        message:
          type: string
          description: 可读的错误信息。
    DeleteResponseResult:
      type: object
      properties:
        id:
          type: string
          description: 被删除的 Response ID。
        deleted:
          type: boolean
          description: 是否删除成功，成功为 `true`。
    InputItemsList:
      type: object
      properties:
        data:
          type: array
          description: 输入项列表。每个元素是一个消息对象。多轮对话（使用 `previous_response_id` 串联）中，会按发生顺序包含历史用户消息与历史模型回复。
          items:
            type: object
            properties:
              id:
                type: string
                description: 消息的唯一标识符。
              role:
                type: string
                enum:
                  - user
                  - assistant
                description: 消息角色，取值为 `user` 或 `assistant`。
              content:
                type: array
                description: 消息内容数组。元素的 `type` 取值为 `input_text`（用户输入）或 `output_text`（模型回复）。
                items:
                  type: object
                  properties:
                    type:
                      type: string
                      description: 内容类型：`input_text` 或 `output_text`。
                    text:
                      type: string
                      description: 文本内容。
              type:
                type: string
                description: 固定为 `message`。
              status:
                type: string
                description: 消息状态，固定为 `completed`。
        first_id:
          type: string
          description: 列表中第一个元素的 ID。
        last_id:
          type: string
          description: 列表中最后一个元素的 ID。
        has_more:
          type: boolean
          description: 是否还有未返回的数据。当为 `true` 时，把本次返回的 `last_id` 作为下一次请求的 `after` 参数，可继续获取后续数据。
        id:
          type: string
          description: 对应的 Response ID。
        model:
          type: string
          description: 生成该 Response 时使用的模型名称。
        created_at:
          type: integer
          description: Response 创建时间的 Unix 时间戳（毫秒）。注意：与创建响应/获取响应接口返回的 `created_at`（秒）单位不同。
        previous_response_id:
          type: string
          nullable: true
          description: 多轮对话时返回，值为上一轮的 Response ID。
````

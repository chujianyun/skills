> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Qwen-OCR 文字提取模型

> 通过 OpenAI 兼容接口调用 Qwen-OCR 文字提取模型。

## OpenAPI

````yaml post /compatible-mode/v1/chat/completions
openapi: 3.1.0
info:
  title: Qwen-OCR 文字提取 API
  description: Qwen-OCR 文字提取模型的 API 参考文档，支持 OpenAI 兼容协议和 DashScope 协议。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com
    description: 北京
security:
  - bearer: []
paths:
  /compatible-mode/v1/chat/completions:
    post:
      operationId: ocrOpenAIChatCompletions
      summary: 文字提取（OpenAI 兼容）
      description: 使用 OpenAI 兼容 API 调用 Qwen-OCR 文字提取模型，支持非流式和流式输出模式。
      security:
        - bearer: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/OpenAIRequest"
      responses:
        "200":
          description: 成功响应
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/OpenAIResponse"
            text/event-stream:
              schema:
                $ref: "#/components/schemas/OpenAIStreamResponse"
      x-codeSamples:
        - lang: python
          label: 非流式输出
          source: |-
            from openai import OpenAI
            import os

            PROMPT_TICKET_EXTRACTION = """
            Please extract the invoice number, train number, departure station, arrival station, departure date and time, seat number, seat class, ticket price, ID card number, and passenger name from the train ticket image.
            You must accurately extract the key information. Do not omit or fabricate information. Replace any single character that is blurry or obscured by strong light with an English question mark (?).
            Return the data in JSON format as follows: {'invoice_number': 'xxx', 'departure_station': 'xxx', 'arrival_station': 'xxx', 'departure_date_and_time':'xxx', 'seat_number': 'xxx','ticket_price':'xxx', 'id_card_number': 'xxx', 'passenger_name': 'xxx'},
            """

            try:
              client = OpenAI(
                # 如果未配置环境变量，请将下行替换为您的 API Key：api_key="sk-xxx",
                api_key=os.getenv("DASHSCOPE_API_KEY"),
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
              )
              completion = client.chat.completions.create(
                model="qwen3.5-ocr",
                messages=[
                  {
                    "role": "user",
                    "content": [
                      {
                        "type": "image_url",
                        "image_url": {"url":"https://img.alicdn.com/imgextra/i2/O1CN01ktT8451iQutqReELT_!!6000000004408-0-tps-689-487.jpg"},
                        # 输入图像的最小像素阈值。如果图像的像素数低于该值，则图像会被放大，直到总像素数超过 min_pixels。
                        "min_pixels": 32 * 32 * 3,
                        # 输入图像的最大像素阈值。如果图像的像素数超过该值，则图像会被缩小，直到总像素数低于 max_pixels。
                        "max_pixels": 32 * 32 * 8192
                      },
                      # 模型支持在以下 text 字段中传入提示词。如果未传入提示词，则使用默认提示词：请输出图片中的文本内容，不要输出其他内容。
                      {"type": "text",
                                 "text": PROMPT_TICKET_EXTRACTION}
                    ]
                  }
                ])
              print(completion.choices[0].message.content)
            except Exception as e:
              print(f"Error message: {e}")
        - lang: javascript
          label: 非流式输出
          source: |-
            import OpenAI from 'openai';

            // 定义提取火车票信息的提示词。
            const PROMPT_TICKET_EXTRACTION = `
            Please extract the invoice number, train number, departure station, arrival station, departure date and time, seat number, seat class, ticket price, ID card number, and passenger name from the train ticket image.
            You must accurately extract the key information. Do not omit or fabricate information. Replace any single character that is blurry or obscured by strong light with an English question mark (?).
            Return the data in JSON format as follows: {'invoice_number': 'xxx', 'departure_station': 'xxx', 'arrival_station': 'xxx', 'departure_date_and_time':'xxx', 'seat_number': 'xxx','ticket_price':'xxx', 'id_card_number': 'xxx', 'passenger_name': 'xxx'}
            `;

            const client = new OpenAI({
              // 如果未配置环境变量，请将下行替换为您的 API Key：apiKey: "sk-xxx",
              apiKey: process.env.DASHSCOPE_API_KEY,
              baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1',
            });

            async function main() {
              const response = await client.chat.completions.create({
                model: 'qwen3.5-ocr',
                messages: [
                  {
                    role: 'user',
                    content: [
                      // 模型支持在 text 字段中传入提示词。如果未传入提示词，则使用默认提示词：请输出图片中的文本内容，不要输出其他内容。
                      { type: 'text', text: PROMPT_TICKET_EXTRACTION},
                      {
                        type: 'image_url',
                        image_url: {
                          url: 'https://img.alicdn.com/imgextra/i2/O1CN01ktT8451iQutqReELT_!!6000000004408-0-tps-689-487.jpg',
                        },
                          //  输入图像的最小像素阈值。如果图像的像素数低于该值，则图像会被放大，直到总像素数超过 min_pixels。
                          "min_pixels": 32 * 32 * 3,
                          // 输入图像的最大像素阈值。如果图像的像素数超过该值，则图像会被缩小，直到总像素数低于 max_pixels。
                          "max_pixels": 32 * 32 * 8192
                      }
                    ]
                  }
                ],
              });
              console.log(response.choices[0].message.content)
            }

            main();
        - lang: bash
          label: 非流式输出
          source: |-
            # === 执行前请删除此注释 ===

            curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
            -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
            -H "Content-Type: application/json" \
            -d '{
              "model": "qwen3.5-ocr",
              "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {"url":"https://img.alicdn.com/imgextra/i2/O1CN01ktT8451iQutqReELT_!!6000000004408-0-tps-689-487.jpg"},
                                "min_pixels": 3072,
                                "max_pixels": 8388608
                            },
                            {"type": "text", "text": "Please extract the invoice number, train number, departure station, arrival station, departure date and time, seat number, seat class, ticket price, ID card number, and passenger name from the train ticket image. You must accurately extract the key information. Do not omit or fabricate information. Replace any single character that is blurry or obscured by strong light with an English question mark (?). Return the data in JSON format as follows: {\'invoice_number\': \'xxx\', \'departure_station\': \'xxx\', \'arrival_station\': \'xxx\', \'departure_date_and_time\':\'xxx\', \'seat_number\': \'xxx\',\'ticket_price\':\'xxx\', \'id_card_number\': \'xxx\', \'passenger_name\': \'xxx\'}"}
                        ]
                    }
                ]
            }'
        - lang: python
          label: 流式输出
          source: |-
            import os
            from openai import OpenAI

            PROMPT_TICKET_EXTRACTION = """
            Please extract the invoice number, train number, departure station, arrival station, departure date and time, seat number, seat class, ticket price, ID card number, and passenger name from the train ticket image.
            You must accurately extract the key information. Do not omit or fabricate information. Replace any single character that is blurry or obscured by strong light with an English question mark (?).
            Return the data in JSON format as follows: {'invoice_number': 'xxx','departure_station': 'xxx', 'arrival_station': 'xxx', 'departure_date_and_time':'xxx', 'seat_number': 'xxx','ticket_price':'xxx', 'id_card_number': 'xxx', 'passenger_name': 'xxx'},
            """

            client = OpenAI(
              # 如果未配置环境变量，请将下行替换为您的 API Key：api_key="sk-xxx",
              api_key=os.getenv("DASHSCOPE_API_KEY"),
              base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            )
            completion = client.chat.completions.create(
              model="qwen3.5-ocr",
              messages=[
                {
                  "role": "user",
                  "content": [
                    {
                      "type": "image_url",
                      "image_url": {"url":"https://img.alicdn.com/imgextra/i2/O1CN01ktT8451iQutqReELT_!!6000000004408-0-tps-689-487.jpg"},
                      # 输入图像的最小像素阈值。如果图像的像素数低于该值，则图像会被放大，直到总像素数超过 min_pixels。
                      "min_pixels": 32 * 32 * 3,
                      # 输入图像的最大像素阈值。如果图像的像素数超过该值，则图像会被缩小，直到总像素数低于 max_pixels。
                      "max_pixels": 32 * 32 * 8192
                    },
                              # 模型支持在以下 text 字段中传入提示词。如果未传入提示词，则使用默认提示词：请输出图片中的文本内容，不要输出其他内容。
                    {"type": "text","text": PROMPT_TICKET_EXTRACTION}
                  ]
                }
              ],
              stream=True,
              stream_options={"include_usage": True}
            )

            for chunk in completion:
              print(chunk.model_dump_json())
        - lang: javascript
          label: 流式输出
          source: |-
            import OpenAI from 'openai';

            // 定义提取火车票信息的提示词。
            const PROMPT_TICKET_EXTRACTION = `
            Please extract the invoice number, train number, departure station, arrival station, departure date and time, seat number, seat class, ticket price, ID card number, and passenger name from the train ticket image.
            You must accurately extract the key information. Do not omit or fabricate information. Replace any single character that is blurry or obscured by strong light with an English question mark (?).
            Return the data in JSON format as follows: {'invoice_number': 'xxx', 'departure_station': 'xxx', 'arrival_station': 'xxx', 'departure_date_and_time':'xxx', 'seat_number': 'xxx','ticket_price':'xxx', 'id_card_number': 'xxx', 'passenger_name': 'xxx'}
            `;

            const openai = new OpenAI({
              // 如果未配置环境变量，请将下行替换为您的 API Key：apiKey: "sk-xxx",
              apiKey: process.env.DASHSCOPE_API_KEY,
              baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1',
            });

            async function main() {
              const response = await openai.chat.completions.create({
                model: 'qwen3.5-ocr',
                messages: [
                  {
                    role: 'user',
                    content: [
                      // 模型支持在以下 text 字段中传入提示词。如果未传入提示词，则使用默认提示词：请输出图片中的文本内容，不要输出其他内容。
                      { type: 'text', text: PROMPT_TICKET_EXTRACTION},
                      {
                        type: 'image_url',
                        image_url: {
                          url: 'https://img.alicdn.com/imgextra/i2/O1CN01ktT8451iQutqReELT_!!6000000004408-0-tps-689-487.jpg',
                        },
                          //  输入图像的最小像素阈值。如果图像的像素数低于该值，则图像会被放大，直到总像素数超过 min_pixels。
                          "min_pixels": 32 * 32 * 3,
                          // 输入图像的最大像素阈值。如果图像的像素数超过该值，则图像会被缩小，直到总像素数低于 max_pixels。
                          "max_pixels": 32 * 32 * 8192
                      }
                    ]
                  }
                ],
                stream: true,
                stream_options:{"include_usage": true}
              });
            let fullContent = ""
              console.log("Streaming output content:")
              for await (const chunk of response) {
                if (chunk.choices[0] && chunk.choices[0].delta.content != null) {
                  fullContent += chunk.choices[0].delta.content;
                  console.log(chunk.choices[0].delta.content);
                }
            }
              console.log(`Full output content: ${fullContent}`)
            }

            main();
        - lang: bash
          label: 流式输出
          source: |-
            # === 执行前请删除此注释 ===

            curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
            -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
            -H "Content-Type: application/json" \
            -d '{
              "model": "qwen3.5-ocr",
              "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {"url":"https://img.alicdn.com/imgextra/i2/O1CN01ktT8451iQutqReELT_!!6000000004408-0-tps-689-487.jpg"},
                                "min_pixels": 3072,
                                "max_pixels": 8388608
                            },
                            {"type": "text", "text": "Please extract the invoice number, train number, departure station, arrival station, departure date and time, seat number, seat class, ticket price, ID card number, and passenger name from the train ticket image. You must accurately extract the key information. Do not omit or fabricate information. Replace any single character that is blurry or obscured by strong light with an English question mark (?). Return the data in JSON format as follows: {\'invoice_number\': \'xxx\', \'departure_station\': \'xxx\', \'arrival_station\': \'xxx\', \'departure_date_and_time\':\'xxx\', \'seat_number\': \'xxx\',\'ticket_price\':\'xxx\', \'id_card_number\': \'xxx\', \'passenger_name\': \'xxx\'}"}
                        ]
                    }
                ],
                "stream": true,
                "stream_options": {"include_usage": true}
            }'
components:
  securitySchemes:
    bearer:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    OpenAIRequest:
      type: object
      required:
        - model
        - messages
      properties:
        model:
          type: string
          description: 模型名称。支持的模型列表请参见 [Qwen-OCR](#)。
          example: qwen3.5-ocr
        messages:
          type: array
          description: 按对话顺序向模型提供上下文的消息序列。
          items:
            type: object
            title: 用户消息
            description: 包含指令和图像的用户消息，供模型处理。
            required:
              - role
              - content
            properties:
              role:
                type: string
                description: 用户消息的角色，值必须为 `user`。
                enum:
                  - user
              content:
                type: array
                description: 消息内容。
                items:
                  type: object
                  properties:
                    type:
                      type: string
                      description: 内容类型。文本输入使用 `text`，图像输入使用 `image_url`。
                      enum:
                        - text
                        - image_url
                    text:
                      type: string
                      description: 输入文本。默认值：`Please output only the text content from the image without any additional descriptions or formatting.`
                    image_url:
                      type: object
                      description: 输入图像的相关信息。当 type 为 `image_url` 时必填。
                      properties:
                        url:
                          type: string
                          description: 图像的 URL 或 Base64 编码的 Data URL。有关传入本地文件的更多信息，请参见文字提取。
                      required:
                        - url
                    min_pixels:
                      type: integer
                      description: |-
                        输入图像的最小像素阈值（单位：像素）。如果输入图像的像素数低于 min_pixels，则图像会被放大，直到总像素数超过 min_pixels。

                        **图像 token 与像素的换算关系：**
                        - qwen3.5-ocr、qwen-vl-ocr-latest：每个 token 对应 32×32 像素。
                        - qwen-vl-ocr、qwen-vl-ocr-2025-08-28 及更早版本：每个 token 对应 28×28 像素。

                        **取值范围：**
                        - qwen3.5-ocr、qwen-vl-ocr-latest：默认值和最小值为 3072（3×32×32）。
                        - qwen-vl-ocr、qwen-vl-ocr-2025-08-28 及更早版本：默认值和最小值为 3136（4×28×28）。
                    max_pixels:
                      type: integer
                      description: |-
                        输入图像的最大像素阈值（单位：像素）。如果输入图像的像素数在 [min_pixels, max_pixels] 范围内，模型将直接处理原始图像，不进行缩放。如果像素数超过 max_pixels，则图像会被缩小，直到像素数小于 max_pixels。

                        **图像 token 与像素的换算关系：**
                        - qwen3.5-ocr、qwen-vl-ocr-latest：每个 token 对应 32×32 像素。
                        - qwen-vl-ocr、qwen-vl-ocr-2025-08-28 及更早版本：每个 token 对应 28×28 像素。

                        **取值范围：**
                        - qwen3.5-ocr、qwen-vl-ocr-latest：默认值 8388608（8192×32×32），最大值 30720000（30000×32×32）。
                        - qwen-vl-ocr、qwen-vl-ocr-2025-08-28 及更早版本：默认值 6422528（8192×28×28），最大值 23520000（30000×28×28）。
        stream:
          type: boolean
          default: false
          description: 指定是否以流式模式返回响应。`false`：一次性返回完整响应。`true`：随模型生成过程逐块返回数据。
        stream_options:
          type: object
          description: 流式输出的配置项，仅在 `stream` 为 `true` 时生效。
          properties:
            include_usage:
              type: boolean
              default: false
              description: 是否在流式输出的最后一个数据块中包含 token 用量信息。
        max_tokens:
          type: integer
          description: |-
            输出的最大 token 数。如果生成内容超过该值，响应将被截断。

            - 对于 qwen3.5-ocr、qwen-vl-ocr-latest 和 qwen-vl-ocr-2024-10-28，默认值和最大值与模型的最大输出长度相同。
            - 对于 qwen-vl-ocr、qwen-vl-ocr-2025-04-13 和 qwen-vl-ocr-2025-08-28，默认值和最大值均为 4096。
        logprobs:
          type: boolean
          default: false
          description: 指定是否返回输出 token 的对数概率。
        top_logprobs:
          type: integer
          default: 0
          description: 指定每个生成步骤中返回的最可能 token 数量。取值范围：[0, 5]。仅在 `logprobs` 为 `true` 时生效。
        temperature:
          type: number
          default: 0.01
          description: 采样温度，控制生成文本的多样性。值越高越多样，值越低越确定。取值范围：[0, 2)。`temperature` 和 `top_p` 只能设置其中之一。
        top_p:
          type: number
          default: 0.001
          description: 核采样的概率阈值。值越高越多样，值越低越确定。取值范围：(0, 1.0]。`temperature` 和 `top_p` 只能设置其中之一。
        top_k:
          type: integer
          default: 1
          description: '采样候选集大小。值越大随机性越高。若为 None 或大于 100，则仅 `top_p` 生效。必须 >= 0。非标准 OpenAI 参数，Python SDK 中请使用 `extra_body={"top_k": xxx}`。'
        repetition_penalty:
          type: number
          default: 1
          description: 重复序列的惩罚系数。值越高越能减少重复。1.0 表示不惩罚。
        presence_penalty:
          type: number
          default: 0
          description: 控制内容重复程度。取值范围：[-2.0, 2.0]。正值减少重复，负值增加重复。
        seed:
          type: integer
          description: 用于复现结果的随机数种子。取值范围：[0, 2^31−1]。
        stop:
          description: 停止词。当出现指定字符串或 token_id 时，立即停止生成。可以是字符串或数组。stop 为数组时，不能混用 token_id 和字符串。
          oneOf:
            - type: string
            - type: array
              items:
                type: string
    OpenAIResponse:
      type: object
      properties:
        id:
          type: string
          description: 本次请求的唯一标识符。
        choices:
          type: array
          items:
            type: object
            properties:
              finish_reason:
                type: string
                description: 模型停止生成的原因。完成时为 `stop`，截断时为 `length`。
                enum:
                  - stop
                  - length
              index:
                type: integer
                description: 在 choices 数组中的索引。
              logprobs:
                type: object
                nullable: true
                description: 对数概率信息。除非启用 `logprobs`，否则为 null。
              message:
                type: object
                properties:
                  content:
                    type: string
                    description: 模型返回的内容。
                  processed_text:
                    type: string
                    description: 对模型原始输出进行后处理的结果，自动删除重复片段等。当模型输出存在重复内容时，该字段提供清洗后的文本。
                  refusal:
                    type: string
                    nullable: true
                    description: 始终为 null。
                  role:
                    type: string
                    description: 始终为 `assistant`。
                    enum:
                      - assistant
                  audio:
                    type: object
                    nullable: true
                    description: 始终为 null。
                  function_call:
                    type: object
                    nullable: true
                    description: 始终为 null。
                  tool_calls:
                    type: array
                    nullable: true
                    description: 始终为 null。
                  annotations:
                    type:
                      - array
                      - "null"
                    description: 预留字段，当前为 null。
        created:
          type: integer
          description: 本次请求创建时的 UNIX 时间戳。
        model:
          type: string
          description: 本次请求使用的模型。
        object:
          type: string
          description: 始终为 `chat.completion`。
          enum:
            - chat.completion
        service_tier:
          type: string
          nullable: true
          description: 始终为 null。
        system_fingerprint:
          type: string
          nullable: true
          description: 始终为 null。
        usage:
          type: object
          description: Token 用量信息。
          properties:
            completion_tokens:
              type: integer
              description: 模型输出的 token 数量。
            prompt_tokens:
              type: integer
              description: 输入的 token 数量。
            total_tokens:
              type: integer
              description: prompt_tokens 和 completion_tokens 的总和。
            completion_tokens_details:
              type: object
              properties:
                accepted_prediction_tokens:
                  type: integer
                  nullable: true
                  description: 始终为 null。
                audio_tokens:
                  type: integer
                  nullable: true
                  description: 始终为 null。
                reasoning_tokens:
                  type: integer
                  nullable: true
                  description: 始终为 null。
                text_tokens:
                  type: integer
                  description: 文本输出的 token 数量。
                rejected_prediction_tokens:
                  type: integer
                  nullable: true
                  description: 始终为 null。
            prompt_tokens_details:
              type: object
              properties:
                audio_tokens:
                  type: integer
                  nullable: true
                  description: 始终为 null。
                cached_tokens:
                  type: integer
                  nullable: true
                  description: 始终为 null。
                image_tokens:
                  type: integer
                  description: 图像输入的 token 数量。
                text_tokens:
                  type: integer
                  description: 文本输入的 token 数量。
    OpenAIStreamResponse:
      type: object
      properties:
        id:
          type: string
          description: 本次调用的唯一标识符，每个数据块的 id 相同。
        choices:
          type: array
          description: 生成的内容。当 `include_usage` 为 true 时，最后一个数据块的 choices 为空。
          items:
            type: object
            properties:
              delta:
                type: object
                description: 流式模式下返回的输出内容。
                properties:
                  content:
                    type: string
                    description: 模型返回的内容。
                  processed_text:
                    type: string
                    description: 对模型原始输出进行后处理的结果，自动删除重复片段等。当模型输出存在重复内容时，该字段提供清洗后的文本。
                  function_call:
                    type: object
                    nullable: true
                    description: 当前为 null。
                  refusal:
                    type: object
                    nullable: true
                    description: 当前为 null。
                  role:
                    type: string
                    description: 消息的角色，仅在第一个数据块中出现。
              finish_reason:
                type: string
                nullable: true
                description: 生成完成时为 `stop`，生成中为 `null`，截断时为 `length`。
              index:
                type: integer
              logprobs:
                type: object
                nullable: true
        created:
          type: integer
          description: UNIX 时间戳，每个数据块相同。
        model:
          type: string
        object:
          type: string
          description: 始终为 `chat.completion.chunk`。
          enum:
            - chat.completion.chunk
        service_tier:
          type: string
          nullable: true
          description: 当前为 null。
        system_fingerprint:
          type: string
          nullable: true
          description: 当前为 null。
        usage:
          type: object
          nullable: true
          description: Token 用量，仅在 `include_usage` 为 true 时的最后一个数据块中出现。
          properties:
            completion_tokens:
              type: integer
            prompt_tokens:
              type: integer
            total_tokens:
              type: integer
            completion_tokens_details:
              type: object
              properties:
                accepted_prediction_tokens:
                  type: integer
                  nullable: true
                audio_tokens:
                  type: integer
                  nullable: true
                reasoning_tokens:
                  type: integer
                  nullable: true
                text_tokens:
                  type: integer
                rejected_prediction_tokens:
                  type: integer
                  nullable: true
            prompt_tokens_details:
              type: object
              properties:
                audio_tokens:
                  type: integer
                  nullable: true
                cached_tokens:
                  type: integer
                  nullable: true
                image_tokens:
                  type: integer
                text_tokens:
                  type: integer
    DashScopeRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称。支持的模型列表请参见 [Qwen-OCR](#)。
          example: qwen3.5-ocr
        input:
          type: object
          required:
            - messages
          description: 包含消息的输入对象。
          properties:
            messages:
              type: array
              description: 以消息序列形式提供给模型的上下文。
              items:
                type: object
                title: 用户消息
                description: 包含图像和可选文本的用户消息。
                required:
                  - role
                  - content
                properties:
                  role:
                    type: string
                    enum:
                      - user
                    description: 必须为 `user`。
                  content:
                    type: array
                    description: 消息内容，图像输入使用数组格式。
                    items:
                      type: object
                      properties:
                        text:
                          type: string
                          description: 输入文本。默认值：`Please output only the text content from the image without any additional descriptions or formatting.`
                        image:
                          type: string
                          description: 图像的 URL、Base64 Data URL 或本地路径。有关传入本地文件的更多信息，请参见传入本地文件。
                        enable_rotate:
                          type: boolean
                          default: false
                          description: 是否对倾斜图像进行校正。
                        min_pixels:
                          type: integer
                          description: |-
                            输入图像的最小像素阈值（单位：像素）。如果输入图像的像素数低于 min_pixels，则图像会被放大，直到总像素数超过 min_pixels。

                            **图像 token 与像素的换算关系：**
                            - qwen3.5-ocr、qwen-vl-ocr-latest：每个 token 对应 32×32 像素。
                            - qwen-vl-ocr、qwen-vl-ocr-2025-08-28 及更早版本：每个 token 对应 28×28 像素。

                            **取值范围：**
                            - qwen3.5-ocr、qwen-vl-ocr-latest：默认值和最小值为 3072（3×32×32）。
                            - qwen-vl-ocr、qwen-vl-ocr-2025-08-28 及更早版本：默认值和最小值为 3136（4×28×28）。
                        max_pixels:
                          type: integer
                          description: |-
                            输入图像的最大像素阈值（单位：像素）。如果输入图像的像素数在 [min_pixels, max_pixels] 范围内，模型将直接处理原始图像，不进行缩放。如果像素数超过 max_pixels，则图像会被缩小，直到像素数小于 max_pixels。

                            **图像 token 与像素的换算关系：**
                            - qwen3.5-ocr、qwen-vl-ocr-latest：每个 token 对应 32×32 像素。
                            - qwen-vl-ocr、qwen-vl-ocr-2025-08-28 及更早版本：每个 token 对应 28×28 像素。

                            **取值范围：**
                            - qwen3.5-ocr、qwen-vl-ocr-latest：默认值 8388608（8192×32×32），最大值 30720000（30000×32×32）。
                            - qwen-vl-ocr、qwen-vl-ocr-2025-08-28 及更早版本：默认值 6422528（8192×28×28），最大值 23520000（30000×28×28）。
        parameters:
          type: object
          description: 模型参数。
          properties:
            ocr_options:
              type: object
              description: 内置 OCR 任务的配置项。使用内置任务时，模型会使用默认提示词，无需在用户消息中传入文本。最低 SDK 版本要求：Python 1.22.2，Java 2.18.4。
              properties:
                task:
                  type: string
                  description: 内置任务名称。
                  enum:
                    - text_recognition
                    - key_information_extraction
                    - document_parsing
                    - table_parsing
                    - formula_recognition
                    - multi_lan
                    - advanced_recognition
                task_config:
                  type: object
                  description: "`key_information_extraction` 任务的配置项，用于指定要提取的字段。如果省略，则提取所有字段。"
                  properties:
                    result_schema:
                      type: object
                      description: 指定要提取字段的 JSON 对象。键为字段名，值为字段描述或格式要求。最多支持 3 层嵌套。
                      additionalProperties:
                        type: string
            max_tokens:
              type: integer
              description: |-
                输出的最大 token 数。如果生成内容超过该值，响应将被截断。

                - 对于 qwen3.5-ocr、qwen-vl-ocr-latest 和 qwen-vl-ocr-2024-10-28，默认值和最大值与模型的最大输出长度相同。
                - 对于 qwen-vl-ocr、qwen-vl-ocr-2025-04-13 和 qwen-vl-ocr-2025-08-28，默认值和最大值均为 4096。
            seed:
              type: integer
              description: 用于复现结果的随机数种子。取值范围：[0, 2^31−1]。
            temperature:
              type: number
              default: 0.01
              description: 采样温度。值越高越多样，值越低越确定。取值范围：[0, 2)。`temperature` 和 `top_p` 只能设置其中之一。
            top_p:
              type: number
              default: 0.001
              description: 核采样阈值。取值范围：(0, 1.0]。`temperature` 和 `top_p` 只能设置其中之一。
            top_k:
              type: integer
              default: 1
              description: 采样候选集大小。值越大随机性越高。必须 >= 0。
            repetition_penalty:
              type: number
              default: 1
              description: 重复序列的惩罚系数。1.0 表示不惩罚。
            presence_penalty:
              type: number
              default: 0
              description: 控制内容重复程度。取值范围：[-2.0, 2.0]。
            stop:
              description: 停止词。可以是字符串或数组。stop 为数组时，不能混用 token_id 和字符串。
              oneOf:
                - type: string
                - type: array
                  items:
                    type: string
            logprobs:
              type: boolean
              default: false
              description: 是否返回对数概率。支持的版本：qwen-vl-ocr-2025-04-13 及更高版本。
            top_logprobs:
              type: integer
              default: 0
              description: 每个生成步骤中返回的最可能 token 数量。取值范围：[0, 5]。仅在 `logprobs` 为 true 时生效。
            incremental_output:
              type: boolean
              default: false
              description: 流式输出时，`true` 表示每个数据块仅返回新生成的内容；`false` 表示返回累积的完整内容。
            stream:
              type: boolean
              default: false
              description: |-
                指定是否流式返回响应。

                - Python SDK：在调用时设置 `stream=True`。
                - Java SDK：使用 `streamCall` 接口。
                - HTTP：在请求头中设置 `X-DashScope-SSE: enable`。
    DashScopeResponse:
      type: object
      properties:
        status_code:
          type: integer
          description: 请求状态码。200 表示成功。Java SDK 不返回此字段。
        request_id:
          type: string
          description: 本次调用的唯一标识符。Java SDK 返回 `requestId`。
        code:
          type: string
          description: 错误码。成功时为空。仅由 Python SDK 返回。
        message:
          type: string
          description: 错误信息。成功时为空。
        output:
          type: object
          description: 调用结果信息。
          properties:
            text:
              type: string
              nullable: true
              description: 当前固定为 null。
            finish_reason:
              type: string
              nullable: true
              description: 生成中为 `null`，完成时为 `stop`，截断时为 `length`。
            choices:
              type: array
              description: 模型输出。
              items:
                type: object
                properties:
                  finish_reason:
                    type: string
                    nullable: true
                    description: 生成中为 `null`，完成时为 `stop`，截断时为 `length`。
                  message:
                    type: object
                    properties:
                      role:
                        type: string
                        description: 始终为 `assistant`。
                        enum:
                          - assistant
                      content:
                        type: array
                        description: 输出消息内容。
                        items:
                          type: object
                          properties:
                            text:
                              type: string
                              description: 输出的文本内容。
                            processed_text:
                              type: string
                              description: 对模型原始输出进行后处理的结果，自动删除重复片段等。当模型输出存在重复内容时，该字段提供清洗后的文本。
                            ocr_result:
                              type: object
                              description: 信息提取（`key_information_extraction`）和高精度识别（`advanced_recognition`）任务的返回结果。
                              properties:
                                kv_result:
                                  type: object
                                  description: 信息提取任务的结果。
                                  additionalProperties:
                                    type: string
                                words_info:
                                  type: array
                                  description: 高精度识别任务的结果。
                                  items:
                                    type: object
                                    properties:
                                      rotate_rect:
                                        type: array
                                        description: 旋转矩形 [center_x, center_y, width, height, angle]。angle 取值范围：[-90, 90]。
                                        items:
                                          type: number
                                      location:
                                        type: array
                                        description: 四顶点坐标 [x1,y1,x2,y2,x3,y3,x4,y4]，从左上角顺时针排列。
                                        items:
                                          type: number
                                      text:
                                        type: string
                                        description: 文本行内容。
                      logprobs:
                        type: object
                        nullable: true
                        description: 对数概率信息。
                        properties:
                          content:
                            type: array
                            items:
                              type: object
                              properties:
                                token:
                                  type: string
                                bytes:
                                  type: array
                                  items:
                                    type: integer
                                  description: token 的 UTF-8 字节序列。
                                logprob:
                                  type: number
                                  nullable: true
                                top_logprobs:
                                  type: array
                                  items:
                                    type: object
                                    properties:
                                      token:
                                        type: string
                                      bytes:
                                        type: array
                                        items:
                                          type: integer
                                      logprob:
                                        type: number
                                        nullable: true
        usage:
          type: object
          description: Token 用量信息。
          properties:
            input_tokens:
              type: integer
              description: 输入 token 数量。
            output_tokens:
              type: integer
              description: 输出 token 数量。
            total_tokens:
              type: integer
              description: input_tokens 和 output_tokens 的总和。
            characters:
              type: integer
              description: 当前固定为 0。
            image_tokens:
              type: integer
              description: 图像输入的 token 数量。
            input_tokens_details:
              type: object
              properties:
                image_tokens:
                  type: integer
                  description: 图像输入的 token 数量。
                text_tokens:
                  type: integer
                  description: 文本输入的 token 数量。
            output_tokens_details:
              type: object
              properties:
                text_tokens:
                  type: integer
                  description: 模型输出的 token 数量。
````

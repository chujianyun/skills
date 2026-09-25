> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 创建 Conversation

## OpenAPI

````yaml post /conversations
openapi: 3.1.0
info:
  title: 千问AI平台会话管理 API
  description: 自动管理多轮对话历史，支持跨设备、跨会话的上下文管理。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v2/apps/protocols/compatible-mode/v1
    description: DashScope
security:
  - BearerAuth: []
paths:
  /conversations:
    post:
      operationId: createConversation
      summary: 创建会话
      description: 创建会话，可选择性地添加初始消息。
      requestBody:
        required: false
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/CreateConversationRequest"
      responses:
        "200":
          description: 会话创建成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ConversationObject"
              example:
                created_at: 1771316949128
                id: conv_xxx
                metadata:
                  topic: demo
                object: conversation
      x-codeSamples:
        - lang: python
          label: Python
          source: |-
            import os
            from openai import OpenAI

            client = OpenAI(
              api_key=os.getenv("DASHSCOPE_API_KEY"),
              base_url="https://dashscope.aliyuncs.com/api/v2/apps/protocols/compatible-mode/v1",
            )

            conversation = client.conversations.create(
              metadata={"topic": "demo"},
              items=[
                {"type": "message", "role": "system", "content": "Alice, a gentle and resilient woman, was born in Beijing. She is 20 years old, and her hobbies are music and chess."}
              ]
            )
            print(conversation)
        - lang: javascript
          label: Node.js
          source: |-
            import OpenAI from "openai";

            const client = new OpenAI({
              apiKey: process.env.DASHSCOPE_API_KEY,
              baseURL: "https://dashscope.aliyuncs.com/api/v2/apps/protocols/compatible-mode/v1",
            });

            const conversation = await client.conversations.create({
              metadata: { topic: "demo" },
              items: [
                {
                  type: "message",
                  role: "system",
                  content: "Alice, a gentle and resilient woman, was born in Beijing. She is 20 years old, and her hobbies are music and chess."
                }
              ]
            });
            console.log(conversation);
        - lang: curl
          label: cURL
          source: |-
            curl -X POST "https://dashscope.aliyuncs.com/api/v2/apps/protocols/compatible-mode/v1/conversations" \
              -H "Content-Type: application/json" \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -d '{
                "metadata": {
                  "topic": "demo"
                },
                "items": [
                  {
                    "type": "message",
                    "role": "system",
                    "content": "Alice, a gentle and resilient woman, was born in Beijing. She is 20 years old, and her hobbies are music and chess."
                  }
                ]
              }'
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    MessageItemInput:
      type: object
      required:
        - type
        - role
        - content
      properties:
        type:
          type: string
          enum:
            - message
          description: 仅支持 `message`。
        role:
          type: string
          enum:
            - user
            - assistant
            - system
            - developer
          description: 消息角色。`system` 和 `developer` 角色的优先级高于 `user`。`assistant` 表示模型在此前交互中生成的消息。
        content:
          description: 消息内容，支持纯文本字符串或结构化内容列表（如 ContentPart 对象数组）。
          oneOf:
            - type: string
            - type: array
              items:
                $ref: "#/components/schemas/ContentPart"
    ContentPart:
      type: object
      properties:
        type:
          type: string
          description: 内容类型，如 `input_text`（用户输入）或 `output_text`（模型输出）。
          example: input_text
        text:
          type: string
          description: 文本内容。
    CreateConversationRequest:
      type: object
      properties:
        items:
          type: array
          description: 初始消息列表，最多 20 条。
          maxItems: 20
          items:
            $ref: "#/components/schemas/MessageItemInput"
        metadata:
          type: object
          description: 会话元数据。最多 16 个键值对（键最长 64 字符，值最长 512 字符）。
          additionalProperties:
            type: string
    UpdateConversationRequest:
      type: object
      required:
        - metadata
      properties:
        metadata:
          type: object
          description: 会话元数据。**此操作会完全覆盖已有的元数据。**最多 16 个键值对（键最长 64 字符，值最长 512 字符）。
          additionalProperties:
            type: string
    CreateItemsRequest:
      type: object
      required:
        - items
      properties:
        items:
          type: array
          description: 待添加的消息列表（每次请求最多 20 条）。
          maxItems: 20
          items:
            $ref: "#/components/schemas/MessageItemInput"
    ConversationObject:
      type: object
      properties:
        created_at:
          type: integer
          description: 会话创建时间，Unix 时间戳（毫秒）。
          example: 1771316949128
        id:
          type: string
          description: 会话 ID。
          example: conv_xxx
        metadata:
          type: object
          description: 元数据键值对。最多 16 个键值对（键最长 64 字符，值最长 512 字符）。
          additionalProperties:
            type: string
        object:
          type: string
          enum:
            - conversation
          description: 固定值 `conversation`。
    DeleteConversationResponse:
      type: object
      properties:
        deleted:
          type: boolean
          description: 是否删除成功。
        id:
          type: string
          description: 已删除的会话 ID。
          example: conv_xxx
        object:
          type: string
          enum:
            - conversation.deleted
          description: 固定值 `conversation.deleted`。
    MessageItem:
      type: object
      properties:
        id:
          type: string
          description: 消息 ID。
          example: msg_xxx
        content:
          description: 消息内容，支持纯文本字符串或结构化内容列表（如 ContentPart 对象数组）。
          oneOf:
            - type: string
            - type: array
              items:
                $ref: "#/components/schemas/ContentPart"
        role:
          type: string
          enum:
            - user
            - assistant
            - system
            - developer
          description: 消息角色：`user`、`assistant`、`system` 或 `developer`。
        status:
          type: string
          enum:
            - in_progress
            - completed
            - incomplete
          description: 处理状态：`in_progress`、`completed` 或 `incomplete`。
        type:
          type: string
          enum:
            - message
          description: 固定值 `message`。
    ItemListResponse:
      type: object
      properties:
        data:
          type: array
          description: 已创建的消息列表。
          items:
            $ref: "#/components/schemas/MessageItem"
        first_id:
          type: string
          description: 首条消息的 ID。
        has_more:
          type: boolean
          description: 是否还有更多数据。
        last_id:
          type: string
          description: 末条消息的 ID。
    ItemListWithObjectResponse:
      type: object
      properties:
        data:
          type: array
          description: 消息列表。
          items:
            $ref: "#/components/schemas/MessageItem"
        first_id:
          type: string
          description: 首条消息的 ID。
        has_more:
          type: boolean
          description: 是否还有更多数据。
        last_id:
          type: string
          description: 末条消息的 ID。
        object:
          type: string
          enum:
            - list
          description: 固定值 `list`。
    DeleteItemResponse:
      type: object
      properties:
        deleted:
          type: boolean
          description: 是否删除成功。
        id:
          type: string
          description: 已删除的消息 ID。
          example: msg_xxx
        object:
          type: string
          enum:
            - conversation.item.deleted
          description: 固定值 `conversation.item.deleted`。
````

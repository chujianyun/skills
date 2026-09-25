> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 查询消息列表

## OpenAPI

````yaml get /conversations/{conversation_id}/items
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
  /conversations/{conversation_id}/items:
    get:
      operationId: listItems
      summary: 查询消息列表
      description: 查询会话中的消息列表。
      parameters:
        - name: conversation_id
          in: path
          required: true
          description: 会话 ID。
          schema:
            type: string
            example: conv_xxx
        - name: after
          in: query
          required: false
          description: 分页游标。返回指定消息 ID 之后创建的消息。
          schema:
            type: string
        - name: order
          in: query
          required: false
          description: 排序方式：`asc`（升序）或 `desc`（降序）。默认值：`desc`。
          schema:
            type: string
            enum:
              - asc
              - desc
            default: desc
        - name: limit
          in: query
          required: false
          description: 返回的消息数量（1-100）。默认值：20。
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 20
      responses:
        "200":
          description: 消息列表查询成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ItemListWithObjectResponse"
              example:
                data:
                  - content:
                      - text: Alice, a gentle and resilient woman, was born in Beijing. She is 20 years old, and her hobbies are music and chess.
                        type: input_text
                    id: msg_7639f8f6-484b-454a-8125-96a3f40eb9e8
                    role: user
                    status: completed
                    type: message
                  - content:
                      - text: Alice's best friend is Bob
                        type: input_text
                    id: msg_288594f6-6ef1-4519-94d4-a545ca311828
                    role: user
                    status: completed
                    type: message
                first_id: msg_7639f8f6-484b-454a-8125-96a3f40eb9e8
                has_more: false
                last_id: msg_288594f6-6ef1-4519-94d4-a545ca311828
                object: list
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

            items = client.conversations.items.list("conv_xxx")
            print(items.data)
        - lang: javascript
          label: Node.js
          source: |-
            import OpenAI from "openai";

            const client = new OpenAI({
              apiKey: process.env.DASHSCOPE_API_KEY,
              baseURL: "https://dashscope.aliyuncs.com/api/v2/apps/protocols/compatible-mode/v1",
            });

            const items = await client.conversations.items.list(
              "conv_xxx"
            );
            console.log(items.data);
        - lang: curl
          label: cURL
          source: |-
            curl "https://dashscope.aliyuncs.com/api/v2/apps/protocols/compatible-mode/v1/conversations/conv_xxx/items?limit=10&order=asc" \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY"
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

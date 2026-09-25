> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 查询克隆音色列表（CosyVoice）

> 分页查询当前账号下的 CosyVoice 克隆音色列表。

## OpenAPI

````yaml post /services/audio/tts/customization
openapi: 3.1.0
info:
  title: 声音复刻 API — 查询克隆音色列表（CosyVoice）
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
security:
  - BearerAuth: []
paths:
  /services/audio/tts/customization:
    post:
      operationId: listVoiceCloningCosyVoice
      summary: 查询克隆音色列表（CosyVoice）
      description: 分页查询当前账号下的 CosyVoice 克隆音色列表。
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/ListRequest"
      responses:
        "200":
          description: 查询成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ListResponse"
      x-codeSamples:
        - lang: bash
          label: cURL
          source: |-
            curl -X POST https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization \
            -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
            -H "Content-Type: application/json" \
            -d '{
              "model": "voice-enrollment",
              "input": {
                "action": "list_voice",
                "prefix": "myvoice",
                "page_size": 10,
                "page_index": 0
              }
            }'
components:
  schemas:
    ListRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 固定为 `voice-enrollment`。
          enum:
            - voice-enrollment
          example: voice-enrollment
        input:
          type: object
          required:
            - action
          properties:
            action:
              type: string
              description: 固定为 `list_voice`。
              enum:
                - list_voice
              example: list_voice
            prefix:
              type: string
              description: 按名称前缀过滤。
              example: myvoice
            page_index:
              type: integer
              description: 页码，从 0 开始。
              default: 0
              example: 0
            page_size:
              type: integer
              description: 每页条数。
              default: 10
              example: 10
    ListResponse:
      type: object
      properties:
        output:
          type: object
          properties:
            voice_list:
              type: array
              description: 音色对象数组。
              items:
                $ref: "#/components/schemas/VoiceItem"
        usage:
          type: object
          properties:
            count:
              type: integer
              description: 固定为 `1`。
              example: 1
        request_id:
          type: string
          description: 请求 ID，用于问题排查。
          example: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    VoiceItem:
      type: object
      properties:
        voice_id:
          type: string
          description: 音色 ID。
          example: cosyvoice-v3.5-plus-myvoice-xxxxxx
        gmt_create:
          type: string
          description: 创建时间。
          example: 2024-12-11 13:38:02
        gmt_modified:
          type: string
          description: 最后修改时间。
          example: 2024-12-11 13:38:02
        status:
          type: string
          description: 音色状态：`DEPLOYING`（审核中）、`OK`（可使用）、`UNDEPLOYED`（未通过）。
          enum:
            - DEPLOYING
            - OK
            - UNDEPLOYED
          example: OK
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: DashScope API Key。前往[获取 API Key](/api-reference/preparation/api-key)。
````

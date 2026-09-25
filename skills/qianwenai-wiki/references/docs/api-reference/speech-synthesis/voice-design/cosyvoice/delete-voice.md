> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 删除设计音色（CosyVoice）

> 删除指定的 CosyVoice 设计音色。

## OpenAPI

````yaml post /services/audio/tts/customization
openapi: 3.1.0
info:
  title: CosyVoice 音色管理 API — 删除音色
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
security:
  - BearerAuth: []
paths:
  /services/audio/tts/customization:
    post:
      operationId: deleteVoiceCosyVoice
      summary: 删除音色（CosyVoice）
      description: 删除指定的 CosyVoice 音色。
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/DeleteRequest"
      responses:
        "200":
          description: 删除成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DeleteResponse"
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
                "action": "delete_voice",
                "voice_id": "cosyvoice-v3.5-plus-myvoice-xxxxxx"
              }
            }'
components:
  schemas:
    DeleteRequest:
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
            - voice_id
          properties:
            action:
              type: string
              description: 固定为 `delete_voice`。
              enum:
                - delete_voice
              example: delete_voice
            voice_id:
              type: string
              description: 要删除的音色 ID。
              example: cosyvoice-v3.5-plus-myvoice-xxxxxx
    DeleteResponse:
      type: object
      properties:
        output:
          type: object
          description: 删除操作返回空对象。
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
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: DashScope API Key。前往[获取 API Key](/api-reference/preparation/api-key)。
````

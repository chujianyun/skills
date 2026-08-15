> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 更新克隆音色

> 替换已有克隆音色的音频文件。音色 ID 保持不变。

## OpenAPI

````yaml post /services/audio/tts/customization
openapi: 3.1.0
info:
  title: 声音复刻 API — 更新克隆音色
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
security:
  - BearerAuth: []
paths:
  /services/audio/tts/customization:
    post:
      operationId: updateVoiceCloning
      summary: 更新克隆音色
      description: 替换已有克隆音色的音频。音色 ID 保持不变。
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/UpdateRequest"
      responses:
        "200":
          description: 更新成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/UpdateResponse"
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
                "action": "update_voice",
                "voice_id": "cosyvoice-v3-plus-myvoice-xxxxxx",
                "url": "https://new-audio-url.wav"
              }
            }'
components:
  schemas:
    UpdateRequest:
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
            - url
          properties:
            action:
              type: string
              description: 固定为 `update_voice`。
              enum:
                - update_voice
              example: update_voice
            voice_id:
              type: string
              description: 要更新的音色 ID。
              example: cosyvoice-v3-plus-myvoice-xxxxxx
            url:
              type: string
              description: 新的音频文件 URL，必须可公开访问。
              format: uri
              example: https://new-audio-url.wav
            language_hints:
              type: array
              items:
                type: string
              description: 新音频的语言提示，仅使用第一个元素。
              default:
                - zh
              example:
                - zh
            max_prompt_audio_length:
              type: number
              description: 预处理后的最大音频时长（秒）。范围：[3.0, 30.0]。
              minimum: 3
              maximum: 30
              default: 10
              example: 15
            enable_preprocess:
              type: boolean
              description: 是否启用音频预处理（降噪、增强、音量归一化）。
              default: false
              example: false
    UpdateResponse:
      type: object
      properties:
        output:
          type: object
          description: 更新操作返回空对象。
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

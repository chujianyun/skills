> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 创建克隆音色（CosyVoice）

> 通过上传音频创建 CosyVoice 克隆音色。

<Note>
  音色创建后需要审核。通过[查询音色详情](/api-reference/speech-synthesis/voice-cloning/cosyvoice/query-voice)确认状态为 `OK` 后方可使用。状态说明参见[概述](/api-reference/speech-synthesis/voice-cloning/overview)。
</Note>

## OpenAPI

````yaml post /services/audio/tts/customization
openapi: 3.1.0
info:
  title: 声音复刻 API — 创建克隆音色（CosyVoice）
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
security:
  - BearerAuth: []
paths:
  /services/audio/tts/customization:
    post:
      operationId: createVoiceCloningCosyVoice
      summary: 创建克隆音色（CosyVoice）
      description: 通过上传音频创建 CosyVoice 克隆音色。无需训练，即时返回音色 ID。
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/CreateRequest"
      responses:
        "200":
          description: 创建成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/CreateResponse"
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
                "action": "create_voice",
                "target_model": "cosyvoice-v3.5-plus",
                "prefix": "myvoice",
                "url": "https://your-audio-url.wav",
                "language_hints": ["zh"],
                "enable_volume_normalization": "false"
              }
            }'
components:
  schemas:
    CreateRequest:
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
            - target_model
            - prefix
            - url
          properties:
            action:
              type: string
              description: 固定为 `create_voice`。
              enum:
                - create_voice
              example: create_voice
            target_model:
              type: string
              description: 克隆音色绑定的语音合成模型。后续合成调用的 model 必须与此一致。支持 Qwen-Audio-TTS（`qwen-audio-3.0-tts-plus`、`qwen-audio-3.0-tts-flash`）与 CosyVoice（`cosyvoice-v3.5-plus`、`cosyvoice-v3.5-flash`、`cosyvoice-v3-plus`、`cosyvoice-v3-flash`）系列模型。
              enum:
                - qwen-audio-3.0-tts-plus
                - qwen-audio-3.0-tts-flash
                - cosyvoice-v3.5-plus
                - cosyvoice-v3.5-flash
                - cosyvoice-v3-plus
                - cosyvoice-v3-flash
              example: cosyvoice-v3.5-plus
            prefix:
              type: string
              description: 音色名称前缀，仅限字母和数字，最长 10 个字符。生成的名称格式：`{target_model}-{prefix}-{unique_id}`。
              maxLength: 10
              pattern: ^[a-zA-Z0-9]+$
              example: myvoice
            url:
              type: string
              description: 用于克隆的音频文件 URL，必须可公开访问。
              format: uri
              example: https://your-audio-url.wav
            language_hints:
              type: array
              items:
                type: string
              description: 音频的语言提示，仅使用第一个元素。默认：`["zh"]`。支持的语言代码（因模型而异）：**qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash**：`zh`（中文）、`en`（英语）、`fr`（法语）、`de`（德语）、`ja`（日语）、`ko`（韩语）、`ru`（俄语）、`pt`（葡萄牙语）、`th`（泰语）、`id`（印尼语）、`vi`（越南语）、`it`（意大利语）、`es`（西班牙语）、`ms`（马来西亚语）、`ar`（阿拉伯语）。
              default:
                - zh
              example:
                - zh
            max_prompt_audio_length:
              type: number
              description: 预处理后的最大音频时长（秒）。范围：[3.0, 30.0]。默认：10.0。
              minimum: 3
              maximum: 30
              default: 10
              example: 10
            enable_preprocess:
              type: boolean
              description: 是否启用音频预处理（降噪、增强、音量归一化）。默认：`false`。
              default: false
              example: false
            enable_volume_normalization:
              type: string
              description: 是否对用于声音复刻的样本音频进行音量归一化。取值：`"true"`（开启）、`"false"`（关闭）。开启后，使用所创建音色合成的音频，其音量可能与关闭该参数时创建的音色不同。默认：`"false"`。
              enum:
                - "true"
                - "false"
              default: "false"
              example: "false"
    CreateResponse:
      type: object
      properties:
        output:
          type: object
          properties:
            voice_id:
              type: string
              description: 生成的音色 ID。在合成调用中将此值作为 `voice` 参数传入。
              example: cosyvoice-v3.5-plus-myvoice-xxxxxx
        usage:
          type: object
          properties:
            count:
              type: integer
              description: 计费的声音创建次数。成功创建时固定为 `1`。
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

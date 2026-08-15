> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 音乐生成（Fun-Music）

> 音乐生成 Fun-Music 模型 API 参考

**用户指南**：关于模型介绍和选型建议请参见[音乐生成](/developer-guides/speech/music-generation)。

## 前提条件

已获取 API Key。获取方式请参见[获取 API Key](/api-reference/preparation/api-key)。

## OpenAPI

````yaml post /api/v1/services/audio/music/generation
openapi: 3.1.0
info:
  title: Fun-Music 音乐生成 API
  description: 音乐生成 Fun-Music 模型的 API 参考文档，支持流式和非流式输出。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com
    description: 中国（北京）
security:
  - bearer: []
paths:
  /api/v1/services/audio/music/generation:
    post:
      operationId: createMusicGeneration
      summary: 音乐生成（Fun-Music）
      description: "通过 DashScope API 调用 Fun-Music 音乐生成模型，根据歌词或提示词生成歌曲。如需通过 HTTP 实现流式输出，请在请求头中设置 `X-DashScope-SSE: enable`。"
      security:
        - bearer: []
      parameters:
        - name: X-DashScope-SSE
          in: header
          required: false
          description: 设置为 `enable` 可通过 HTTP 实现流式输出。
          schema:
            type: string
            enum:
              - enable
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/FunMusicRequest"
      responses:
        "200":
          description: 成功响应
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/FunMusicResponse"
      x-codeSamples:
        - lang: bash
          label: 非流式
          source: |-
            curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/audio/music/generation' \
            -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
            -H 'Content-Type: application/json' \
            -d '{
              "model": "fun-music-v1",
              "input": {
                "prompt": "夏日清新民谣，木吉他与口琴伴奏，轻快节奏，适合旅行Vlog背景音乐",
                "gender": "female"
              }
            }'
        - lang: bash
          label: 流式
          source: |-
            curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/audio/music/generation' \
            -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
            -H 'Content-Type: application/json' \
            -H 'X-DashScope-SSE: enable' \
            -d '{
              "model": "fun-music-v1",
              "input": {
                "prompt": "节奏感强的电子舞曲，合成器音效，充满能量，适合健身运动场景",
                "gender": "male"
              }
            }'
        - lang: python
          label: 非流式
          source: |-
            import requests
            import os

            api_key = os.getenv("DASHSCOPE_API_KEY")
            url = "https://dashscope.aliyuncs.com/api/v1/services/audio/music/generation"

            response = requests.post(url,
              headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
              },
              json={
                "model": "fun-music-v1",
                "input": {
                  "prompt": "夏日清新民谣，木吉他与口琴伴奏，轻快节奏，适合旅行Vlog背景音乐",
                  "gender": "female"
                }
              }
            )

            result = response.json()
            audio_url = result["output"]["audio"]["url"]
            print(f"音乐生成成功！下载地址：{audio_url}")
        - lang: python
          label: 流式
          source: |-
            import requests
            import os
            import json
            import base64

            api_key = os.getenv("DASHSCOPE_API_KEY")
            url = "https://dashscope.aliyuncs.com/api/v1/services/audio/music/generation"

            response = requests.post(url,
              headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "X-DashScope-SSE": "enable"
              },
              json={
                "model": "fun-music-v1",
                "input": {
                  "prompt": "节奏感强的电子舞曲，合成器音效，充满能量，适合健身运动场景",
                  "gender": "male"
                }
              },
              stream=True
            )

            output_file = "output.mp3"
            with open(output_file, "wb") as f:
              for line in response.iter_lines():
                if not line:
                  continue
                decoded = line.decode("utf-8")
                if decoded.startswith("data:"):
                  data = json.loads(decoded[5:])
                  finish_reason = data.get("output", {}).get("finish_reason")
                  if finish_reason == "null":
                    audio_data = data["output"]["audio"].get("data", "")
                    if audio_data:
                      f.write(base64.b64decode(audio_data))
                  elif finish_reason == "stop":
                    print(f"音乐生成完成！已保存到 {output_file}")
components:
  securitySchemes:
    bearer:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    FunMusicRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称。可选值：`fun-music-v1`、`fun-music-preview`。
          enum:
            - fun-music-v1
            - fun-music-preview
        input:
          type: object
          description: 输入参数对象。
          properties:
            prompt:
              type: string
              description: |-
                提示词内容，模型将根据提示词自动创作并生成音乐。

                - `fun-music-v1`：与 `lyrics` 二选一，至少传入其中之一。
                - `fun-music-preview`：必选。

                字符限制：
                - 非流式模式：1~2000 字符
                - 流式模式：5~1000 个中文汉字或英文单词

                当同时传入 `prompt` 和 `lyrics` 时，仅 `lyrics` 生效，`prompt` 将被忽略。
            lyrics:
              type: string
              description: |-
                歌词内容。

                - `fun-music-v1`：与 `prompt` 二选一，至少传入其中之一。
                - `fun-music-preview`：可选。

                字符限制：
                - 非流式模式：中文 5~350 字符，英文 5~2000 字符
                - 流式模式：中文 300~350 字，英文 200~250 词

                当同时传入 `lyrics` 和 `prompt` 时，仅 `lyrics` 生效，`prompt` 将被忽略。
            is_instrumental:
              type: boolean
              description: |-
                是否生成纯音乐。设为 `true` 时生成纯音乐（无人声演唱），设为 `false` 时生成歌曲。

                当 `is_instrumental` 为 `true` 时，`lyrics` 和 `gender` 参数无效。
              default: false
            gender:
              type: string
              description: 演唱声音的性别。仅 `fun-music-v1` 模型支持该参数。
              default: female
              enum:
                - male
                - female
            format:
              type: string
              description: 音频编码格式。`mp3` 适合网络传输和存储，`wav` 适合后期处理和高质量播放。
              default: mp3
              enum:
                - mp3
                - wav
            enable_aigc_watermark:
              type: boolean
              description: AIGC 水印开关。开启后，会在生成的音频末尾追加表示"AI"的摩尔斯电码音频信号（·— ··），用于标识该音频为 AI 生成内容。开启水印会增加音频时长。
              default: false
    FunMusicResponse:
      type: object
      properties:
        request_id:
          type: string
          description: 请求 ID，用于问题排查和日志追踪。
          example: 46c51288-7ed6-95cc-a119-xxxxxxxxxxxx
        output:
          type: object
          description: 模型的输出。
          properties:
            audio:
              type: object
              description: 模型输出的音频信息。
              properties:
                data:
                  type: string
                  description: 流式输出时的 Base64 音频数据片段。非流式输出时为空字符串。
                  example: ""
                url:
                  type: string
                  description: 完整音频文件的 OSS URL，有效期 24 小时。非流式模式下直接返回；流式模式下仅在最终消息中出现。
                  example: http://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/pre/fun-music/20260330/xxxxxxxx/a8db24cc-d35f-961b-af81-a9e8d8b01f67.mp3?xxx
                id:
                  type: string
                  description: 音频文件 ID。
                  example: audio_46c51288-7ed6-95cc-a119-xxxxxxxxxxxx
                expires_at:
                  type: integer
                  description: 音频 URL 过期时间戳（Unix timestamp）。
                  example: 1774936147
            extra_info:
              type: object
              description: 额外信息。
              properties:
                channels:
                  type: integer
                  description: 音频声道数（如：2 表示立体声）。
                  example: 2
                sample_rate:
                  type: string
                  description: 音频采样率（如："48000"）。
                  example: "48000"
                lyrics:
                  type: string
                  description: 歌词内容。
                  example: |-
                    [verse]
                    清晨的阳光穿过窗帘,
                    咖啡的香气弥漫房间.
                    翻开昨天未读完的书,
                    时光就这样悄悄流转.

                    [chorus]
                    慢慢来不着急,
                    生活本该如此惬意.
                    把烦恼都丢进风里,
                    拥抱每一个晴天雨季.
            finish_reason:
              type: string
              description: 结束原因。生成过程中为 `null`；当生成自然结束时，值为 `"stop"`。
              enum:
                - stop
                - null
              example: stop
        usage:
          type: object
          description: 本次请求的计费信息。
          properties:
            duration:
              type: integer
              description: 音乐时长（秒），用于计费。
              example: 200
      examples:
        - summary: 非流式输出
          value:
            output:
              audio:
                data: ""
                expires_at: 1774936147
                id: audio_46c51288-7ed6-95cc-a119-xxxxxxxxxxxx
                url: http://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/pre/fun-music/20260330/xxxxxxxx/a8db24cc-d35f-961b-af81-a9e8d8b01f67.mp3?xxx
              extra_info:
                channels: 2
                lyrics: |-
                  [verse]
                  清晨的阳光穿过窗帘,
                  咖啡的香气弥漫房间.
                  翻开昨天未读完的书,
                  时光就这样悄悄流转.

                  [chorus]
                  慢慢来不着急,
                  生活本该如此惬意.
                  把烦恼都丢进风里,
                  拥抱每一个晴天雨季.
                sample_rate: "48000"
              finish_reason: stop
            usage:
              duration: 200
            request_id: 46c51288-7ed6-95cc-a119-xxxxxxxxxxxx
        - summary: 流式输出（中间消息）
          value:
            output:
              audio:
                data: base64 音频数据
                expires_at: 1774937185
                id: audio_a8db24cc-d35f-961b-af81-xxxxxxxxxxxx
              finish_reason: "null"
            request_id: a8db24cc-d35f-961b-af81-xxxxxxxxxxxx
        - summary: 流式输出（最终消息）
          value:
            output:
              audio:
                expires_at: 1774937185
                id: audio_a8db24cc-d35f-961b-af81-xxxxxxxxxxxx
                data: ""
                url: http://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/pre/fun-music/20260330/xxxxxxxx/a8db24cc-d35f-961b-af81-a9e8d8b01f67.mp3?xxx
              extra_info:
                channels: 2
                sample_rate: "48000"
                lyrics: |-
                  [verse]
                  清晨的阳光穿过窗帘,
                  咖啡的香气弥漫房间.
                  翻开昨天未读完的书,
                  时光就这样悄悄流转.

                  [chorus]
                  慢慢来不着急,
                  生活本该如此惬意.
                  把烦恼都丢进风里,
                  拥抱每一个晴天雨季.
              finish_reason: stop
            usage:
              duration: 200
            request_id: a8db24cc-d35f-961b-af81-xxxxxxxxxxxx
````

> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 爱诗 PixVerse — 创建任务

> 提交 PixVerse 视频对口型任务

传入视频和音频（或 TTS 文本），生成与音频同步的对口型视频。

## 输入方式

- **音频驱动**：传入 `video_url` 和 `audio_url`，模型将音频中的语音与视频人脸口型对齐。
- **TTS 文本驱动**：传入 `video_url`、`lip_sync_tts_speaker_id` 和 `lip_sync_tts_content`，由模型合成语音并生成对口型视频。

两种方式二选一，不能同时传入音频与 TTS 参数。

## OpenAPI

````yaml post /services/aigc/video-generation/video-synthesis
openapi: 3.1.0
info:
  title: 爱诗 PixVerse 视频对口型 API
  description: 爱诗 PixVerse 视频对口型模型支持输入视频和音频（或 TTS 文本），生成与音频同步的对口型视频。API 采用异步调用方式：先 POST 创建任务获取 task_id，再 GET 轮询查询任务状态与结果。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 千问AI平台
security:
  - BearerAuth: []
paths:
  /services/aigc/video-generation/video-synthesis:
    post:
      operationId: createPixVerseLipsync
      summary: 创建视频对口型任务
      description: 提交视频对口型异步任务，返回 task_id 用于后续轮询查询。task_id 有效期为 24 小时，请勿重复创建任务。
      parameters:
        - name: X-DashScope-Async
          in: header
          required: true
          description: 异步处理配置参数。HTTP 请求只支持异步，必须设置为 `enable`。缺少此请求头将报错："current user api does not support synchronous calls"。
          schema:
            type: string
            enum:
              - enable
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/PixVerseLipsyncRequest"
      responses:
        "200":
          description: 任务创建成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/AsyncTaskSubmitResponse"
        "400":
          description: 请求参数错误
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
      x-codeSamples:
        - lang: curl
          label: cURL - 音频驱动
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
                "model": "pixverse/pixverse-lipsync",
                "input": {
                    "media": [
                        {
                            "type": "video_url",
                            "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250717/pvegot/input_video_01.mp4"
                        },
                        {
                            "type": "audio_url",
                            "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250717/aumwir/stella2.wav"
                        }
                    ]
                },
                "parameters": {
                    "watermark": true
                }
            }'
        - lang: curl
          label: cURL - TTS 文本驱动
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
                "model": "pixverse/pixverse-lipsync",
                "input": {
                    "media": [
                        {
                            "type": "video_url",
                            "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250717/pvegot/input_video_01.mp4"
                        },
                        {
                            "type": "lip_sync_tts_speaker_id",
                            "id": "auto"
                        },
                        {
                            "type": "lip_sync_tts_content",
                            "content": "保持热爱持续开心，琐碎小事不值得烦心"
                        }
                    ]
                },
                "parameters": {
                    "watermark": true
                }
            }'
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    PixVerseLipsyncRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称。固定值：`pixverse/pixverse-lipsync`。
          enum:
            - pixverse/pixverse-lipsync
          example: pixverse/pixverse-lipsync
        input:
          type: object
          required:
            - media
          description: 输入的基本信息，包括人脸视频和音频来源。
          properties:
            media:
              type: array
              description: 媒体资源列表。必须包含一个 `video_url` 类型的视频，以及音频来源（二选一）：方式一（音频驱动）传入 `audio_url` 类型的音频文件；方式二（TTS 合成）同时传入 `lip_sync_tts_speaker_id` 和 `lip_sync_tts_content`。`audio_url` 与 `lip_sync_tts_speaker_id` + `lip_sync_tts_content` 不允许同时传入。
              items:
                type: object
                properties:
                  type:
                    type: string
                    description: 媒体类型标识符。
                    enum:
                      - video_url
                      - audio_url
                      - lip_sync_tts_speaker_id
                      - lip_sync_tts_content
                  url:
                    type: string
                    format: uri
                    description: 当 type 为 `video_url` 或 `audio_url` 时必填。媒体资源的 URL 地址。`video_url`：输入视频的 URL，需包含可用于对口型的人脸画面，文件大小不超过 250MB，时长不超过 300 秒，支持 MP4、MOV、WebM 格式。`audio_url`：音频文件的 URL，文件大小不超过 100MB，时长不超过 300 秒，支持 MP3、WAV、M4A、AAC 格式。
                  id:
                    type: string
                    description: 当 type 为 `lip_sync_tts_speaker_id` 时必填。TTS 音色 ID。取值为 `auto` 时随机选择音色，取值为数字字符串时按音色 ID 指定。可选音色 ID：2（詹有鱼）、4（外国阿利）、6（李解）、10（姜姜好）、11（老森）、12（李杰克）、13（钱多多）、14（呆萌王小拍）、16（屯里大嗓）、18（豫语汉子）、19（宝岛囡囡）、20（陕西掌柜）、21（港风阿sir）。
                    example: auto
                  content:
                    type: string
                    description: 当 type 为 `lip_sync_tts_content` 时必填。需要驱动口型的文本内容，支持中英文，不超过 200 字（UTF-8 编码）。
        parameters:
          $ref: "#/components/schemas/PixVerseLipsyncParameters"
    PixVerseLipsyncParameters:
      type: object
      description: 视频生成参数。如设置是否添加水印等。
      properties:
        watermark:
          type: boolean
          description: 是否添加水印标识，水印位于视频右下角，文案固定为“AI生成”。
          default: false
          enum:
            - false
            - true
    AsyncTaskSubmitResponse:
      type: object
      description: 异步任务提交响应。请保存 task_id，用于查询任务状态与结果。
      properties:
        request_id:
          type: string
          description: 请求唯一标识。可用于请求明细溯源和问题排查。
          example: 4909100c-7b5a-9f92-bfe5-xxxxxx
        output:
          type: object
          description: 任务输出信息。
          properties:
            task_id:
              type: string
              description: 任务 ID。查询有效期 24 小时。
              example: 0385dc79-5ff8-4d82-bcb6-xxxxxx
            task_status:
              type: string
              description: 任务状态。初始状态通常为 `PENDING`。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
    PixVerseLipsyncTaskStatusResponse:
      type: object
      description: 任务状态查询响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识。可用于请求明细溯源和问题排查。
        output:
          type: object
          description: 任务输出信息。
          properties:
            task_id:
              type: string
              description: 任务 ID。查询有效期 24 小时。
            task_status:
              type: string
              description: 任务状态。状态流转：PENDING（排队中）→ RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。CANCELED 表示任务已取消，UNKNOWN 表示任务不存在或状态未知。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - CANCELED
                - UNKNOWN
            submit_time:
              type: string
              description: 任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。
            scheduled_time:
              type: string
              description: 任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。
            end_time:
              type: string
              description: 任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。仅在任务状态为 SUCCEEDED 或 FAILED 时返回。
            video_url:
              type: string
              format: uri
              description: 视频 URL。仅在 task_status 为 SUCCEEDED 时返回。视频格式为 MP4（H.264 编码）。视频链接暂无过期时间，但不建议将其作为长期存储依赖，请及时下载。
              example: https://media.pixverseai.cn/xxxx.mp4
            code:
              type: string
              description: 请求失败的错误码。请求成功时不会返回此参数。
            message:
              type: string
              description: 请求失败的详细信息。请求成功时不会返回此参数。
        usage:
          type: object
          description: 输出信息统计，只对成功的结果计数。
          properties:
            duration:
              type: integer
              description: 计费时长（秒）。音频驱动方式为音频时长向上取整；TTS 方式为文本字节数（UTF-8）÷ 15 向上取整。
            size:
              type: string
              description: 输出视频的分辨率。
            fps:
              type: integer
              description: 输出视频的帧率。
            video_count:
              type: integer
              description: 视频数量，固定为 1。
            SR:
              type: string
              description: 输出视频的分辨率档位。
    DashScopeErrorResponse:
      type: object
      description: DashScope API 错误响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识。可用于问题排查。
        code:
          type: string
          description: 错误码。
          example: InvalidParameter
        message:
          type: string
          description: 错误详情。
          example: Invalid model name
````

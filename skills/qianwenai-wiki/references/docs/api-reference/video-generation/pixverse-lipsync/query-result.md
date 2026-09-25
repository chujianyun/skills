> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 爱诗 PixVerse — 查询视频对口型任务结果

> 查询 PixVerse 视频对口型任务状态

查询任务状态并获取生成的视频。

## 轮询策略

1. 通过[创建任务](/api-reference/video-generation/pixverse-lipsync/create-task)接口提交任务，保存返回的 `task_id`。
2. 每 **15 秒**轮询一次，直到 `task_status` 变为 `SUCCEEDED` 或 `FAILED`。
3. 任务成功后，从 `video_url` 下载视频。

## 注意事项

- **URL 有效期**：`video_url` 在 **24 小时**后过期，请及时下载。
- **状态流转**：`PENDING` → `RUNNING` → `SUCCEEDED` 或 `FAILED`。`CANCELED` 表示任务已取消。`UNKNOWN` 表示任务不存在或已过期（超过 24 小时）。

## OpenAPI

````yaml get /tasks/{task_id}
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
  /tasks/{task_id}:
    get:
      operationId: getPixVerseLipsyncTaskStatus
      summary: 查询任务结果
      description: 根据 task_id 查询任务状态与结果。建议采用轮询机制，设置合理的查询间隔（如 15 秒）来获取结果。任务状态流转：PENDING（排队中）→ RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。
      parameters:
        - name: task_id
          in: path
          required: true
          description: 任务 ID，来自创建任务接口的返回。查询有效期 24 小时。
          schema:
            type: string
      responses:
        "200":
          description: 成功获取任务状态
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/PixVerseLipsyncTaskStatusResponse"
              examples:
                SUCCEEDED:
                  summary: 任务执行成功
                  value:
                    request_id: ddf8140e-67c6-9e70-8953-xxxxxx
                    output:
                      task_id: 1acb9d0c-7a63-4ff6-a198-xxxxxx
                      task_status: SUCCEEDED
                      submit_time: 2026-07-15 17:01:49.352
                      scheduled_time: 2026-07-15 17:01:49.398
                      end_time: 2026-07-15 17:02:29.724
                      video_url: https://media.pixverseai.cn/xxxx.mp4
                    usage:
                      duration: 7
                      size: 1080*1920
                      fps: 24
                      video_count: 1
                      SR: ""
                FAILED:
                  summary: 任务执行失败
                  value:
                    request_id: e5d70b02-ebd3-98ce-9fe8-759d7d7b107d
                    output:
                      task_id: 86ecf553-d340-4e21-af6e-a0c6a421c010
                      task_status: FAILED
                      code: InvalidParameter
                      message: Invalid field type or value. Please verify your input data.
                RUNNING:
                  summary: 任务处理中
                  value:
                    request_id: c1209113-8437-424f-a386-xxxxxx
                    output:
                      task_id: 86ecf553-d340-4e21-af6e-a0c6a421c010
                      task_status: RUNNING
                      submit_time: 2026-07-15 17:01:49.352
                      scheduled_time: 2026-07-15 17:01:49.398
        "400":
          description: 请求参数错误
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
      x-codeSamples:
        - lang: curl
          label: cURL - 查询任务结果
          source: |-
            # 将 {task_id} 替换为创建任务接口返回的 task_id
            curl -X GET 'https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY"
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

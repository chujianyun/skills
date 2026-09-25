> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Wan 2.7 — 查询结果

> 查询 Wan 2.7 图生视频任务状态

查询任务状态并获取生成的视频。

## 轮询策略

1. 通过[创建任务](/api-reference/video-generation/wan27-image-to-video/create-task)接口提交任务，保存返回的 `task_id`。
2. 每 **15 秒**轮询一次，直到 `task_status` 变为 `SUCCEEDED` 或 `FAILED`。
3. 任务成功后，从 `video_url` 下载视频。

## 注意事项

- **URL 有效期**：`video_url` 在 **24 小时**后过期，请及时下载。
- **状态流转**：`PENDING` → `RUNNING` → `SUCCEEDED`、`FAILED` 或 `CANCELED`。`UNKNOWN` 表示任务不存在或查询已超过 24 小时。

## OpenAPI

````yaml get /tasks/{task_id}
openapi: 3.1.0
info:
  title: Wan 2.7 图像转视频 API
  description: 基于 Wan 2.7 模型，从图片、音频和视频片段生成视频。以异步方式提交任务，然后通过 `GET /tasks/{task_id}` 轮询获取结果。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 千问AI平台
security:
  - BearerAuth: []
paths:
  /tasks/{task_id}:
    get:
      operationId: getWan27ImageToVideoTaskStatus
      summary: 查询任务结果
      description: 轮询已提交任务的状态，任务完成后获取视频链接。
      parameters:
        - name: task_id
          in: path
          required: true
          description: POST 响应中返回的任务 ID。
          schema:
            type: string
      responses:
        "200":
          description: 成功获取任务状态
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Wan27I2VTaskStatusResponse"
              examples:
                SUCCEEDED:
                  summary: 任务成功
                  value:
                    request_id: 2ca1c497-f9e0-449d-9a3f-xxxxxx
                    output:
                      task_id: af6efbc0-4bef-4194-8246-xxxxxx
                      task_status: SUCCEEDED
                      submit_time: 2025-09-25 11:07:28.590
                      scheduled_time: 2025-09-25 11:07:35.349
                      end_time: 2025-09-25 11:17:11.650
                      orig_prompt: A scene of urban fantasy art. A dynamic graffiti art character. A boy made of spray paint comes to life on a concrete wall. He sings an English rap song at high speed while striking a classic, energetic rapper pose. The scene is set under an urban railway bridge at night. The light comes from a single street lamp, creating a cinematic atmosphere full of high energy and amazing detail. The audio of the video consists entirely of his rap, with no other dialogue or noise.
                      video_url: https://dashscope-result-sh.oss-accelerate.aliyuncs.com/xxx.mp4?Expires=xxx
                    usage:
                      duration: 15
                      input_video_duration: 0
                      output_video_duration: 15
                      video_count: 1
                      SR: 720
                FAILED:
                  summary: 任务失败
                  value:
                    request_id: e5d70b02-ebd3-98ce-9fe8-759d7d7b107d
                    output:
                      task_id: 86ecf553-d340-4e21-af6e-a0c6a421c010
                      task_status: FAILED
                      code: InvalidParameter
                      message: The size does not match xxxxxx
                RUNNING:
                  summary: 任务运行中
                  value:
                    request_id: c1209113-8437-424f-a386-xxxxxx
                    output:
                      task_id: 86ecf553-d340-4e21-af6e-a0c6a421c010
                      task_status: RUNNING
                      submit_time: 2025-09-25 11:07:28.590
                      scheduled_time: 2025-09-25 11:07:35.349
                UNKNOWN:
                  summary: 任务已过期
                  value:
                    request_id: a4de7c32-7057-9f82-8581-xxxxxx
                    output:
                      task_id: 502a00b1-19d9-4839-a82f-xxxxxx
                      task_status: UNKNOWN
        "400":
          description: 请求参数无效
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
      x-codeSamples:
        - lang: curl
          label: cURL - 查询任务结果
          source: |-
            # 将 {task_id} 替换为提交任务时返回的实际任务 ID
            curl -X GET 'https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY"
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    Wan27ImageToVideoRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型标识符。可选值：`wan2.7-i2v`（主线版本，持续更新）、`wan2.7-i2v-2026-04-25`（快照版本，能力与主线一致）。
          enum:
            - wan2.7-i2v
            - wan2.7-i2v-2026-04-25
          example: wan2.7-i2v
        input:
          type: object
          required:
            - media
          description: 视频生成的输入数据。
          properties:
            prompt:
              type: string
              description: 描述希望生成的视频内容，支持中英文，最多 5,000 个字符（超出自动截断）。
              example: A kitten runs on the grass.
            negative_prompt:
              type: string
              description: 描述不希望出现在视频中的内容（如 `低质量、模糊、多余手指`），支持中英文，最多 500 个字符（超出自动截断）。
              example: low resolution, error, worst quality, low quality, deformed, extra fingers, bad proportions
            media:
              type: array
              description: |-
                视频生成所需的参考素材，每个元素指定 `type` 和 `url`，每种 `type` 最多出现一次。

                支持的组合：
                - `first_frame`
                - `first_frame` + `driving_audio`
                - `first_frame` + `last_frame`
                - `first_frame` + `last_frame` + `driving_audio`
                - `first_clip`
                - `first_clip` + `last_frame`
              items:
                type: object
                required:
                  - type
                  - url
                properties:
                  type:
                    type: string
                    description: |-
                      素材类型。

                      - `first_frame`：首帧图片，支持 JPEG/JPG/PNG/BMP/WEBP，每边 240-8000 px，宽高比 1:8 至 8:1，最大 20 MB。
                      - `last_frame`：尾帧图片，限制与 `first_frame` 相同。
                      - `driving_audio`：用于口型同步或语音驱动动画的音频，支持 WAV/MP3，时长 2-30 秒，最大 15 MB。若不提供，模型将自动生成配套音效。
                      - `first_clip`：用于续生的输入视频，支持 MP4/MOV，时长 2-10 秒，每边 240-4096 px，宽高比 1:8 至 8:1，最大 100 MB。
                    enum:
                      - first_frame
                      - last_frame
                      - driving_audio
                      - first_clip
                  url:
                    type: string
                    format: uri
                    description: 素材的公开访问 URL（HTTP/HTTPS）。
        parameters:
          $ref: "#/components/schemas/Wan27ImageToVideoParameters"
    Wan27ImageToVideoParameters:
      type: object
      description: 视频生成参数。
      properties:
        resolution:
          type: string
          description: 视频清晰度档位。模型会自动缩放输出分辨率并保持输入素材的宽高比，分辨率越高费用越高。
          enum:
            - 720P
            - 1080P
          default: 1080P
        duration:
          type: integer
          description: 视频时长（秒），取整数，范围 2-15，时长越长费用越高，按秒计费。对于视频续生（`first_clip`），此参数为包含输入片段的总输出时长。例如，若 `duration=15` 而输入视频为 3 秒，则模型将生成 12 秒的新内容。
          minimum: 2
          maximum: 15
          default: 5
        prompt_extend:
          type: boolean
          description: 在生成前使用大语言模型对提示词进行扩写优化，适合简短或模糊的提示词，但会增加耗时。设置为 `false` 则按原始提示词生成。
          default: true
        watermark:
          type: boolean
          description: 在视频右下角添加 "AI 生成" 水印。
          default: false
        seed:
          type: integer
          description: 随机种子，用于生成可复现的结果。相同种子和参数会产生相似（但不完全相同）的输出。
          minimum: 0
          maximum: 2147483647
    AsyncTaskSubmitResponse:
      type: object
      description: 异步任务提交的响应结果。
      properties:
        request_id:
          type: string
          description: 请求的唯一标识符，用于追踪和排查问题。
          example: 4909100c-7b5a-9f92-bfe5-xxxxxx
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 用于轮询任务状态的任务 ID，配合 `GET /tasks/{task_id}` 使用。
              example: 0385dc79-5ff8-4d82-bcb6-xxxxxx
            task_status:
              type: string
              description: 任务的初始状态，通常为 `PENDING`。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
    Wan27I2VTaskStatusResponse:
      type: object
      description: wan2.7 图像转视频任务的状态响应。
      properties:
        request_id:
          type: string
          description: 请求 ID，用于排查问题。联系支持时请提供此 ID。
          example: 2ca1c497-f9e0-449d-9a3f-xxxxxx
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID，提交后 24 小时内可查询。
              example: af6efbc0-4bef-4194-8246-xxxxxx
            task_status:
              type: string
              description: 任务生命周期：`PENDING` → `RUNNING` → `SUCCEEDED` 或 `FAILED`。主动停止时为 `CANCELED`，过期后为 `UNKNOWN`。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - CANCELED
                - UNKNOWN
            submit_time:
              type: string
              description: 任务提交时间（UTC+8，格式：`YYYY-MM-DD HH:mm:ss.SSS`）。
              example: 2025-09-25 11:07:28.590
            scheduled_time:
              type: string
              description: 任务开始执行时间（UTC+8，格式：`YYYY-MM-DD HH:mm:ss.SSS`）。
              example: 2025-09-25 11:07:35.349
            end_time:
              type: string
              description: 任务结束时间（UTC+8，格式：`YYYY-MM-DD HH:mm:ss.SSS`），仅在 `SUCCEEDED` 或 `FAILED` 状态下出现。
              example: 2025-09-25 11:17:11.650
            orig_prompt:
              type: string
              description: 原始提示词文本，对应请求参数 `prompt`。
            video_url:
              type: string
              format: uri
              description: 生成视频的 URL（MP4，H.264 编码），仅在 `task_status` 为 `SUCCEEDED` 时出现。**有效期 24 小时**，请及时下载。
              example: https://dashscope-result-sh.oss-accelerate.aliyuncs.com/xxx.mp4?Expires=xxx
            code:
              type: string
              description: 错误码，仅在 `task_status` 为 `FAILED` 时出现。
            message:
              type: string
              description: 错误信息，仅在 `task_status` 为 `FAILED` 时出现。
        usage:
          type: object
          description: 资源消耗信息，仅在 `task_status` 为 `SUCCEEDED` 时出现。
          properties:
            duration:
              type: integer
              description: 计费视频时长（秒）。
            input_video_duration:
              type: integer
              description: 输入视频时长（秒），首帧任务时为 `0`。
            output_video_duration:
              type: integer
              description: 输出视频时长（秒）。
            video_count:
              type: integer
              description: 生成的视频数量，固定为 `1`。
            SR:
              type: integer
              description: 所用分辨率档位（例如，`720` 对应 720P，`1080` 对应 1080P）。
    DashScopeErrorResponse:
      type: object
      description: DashScope API 错误响应。
      properties:
        request_id:
          type: string
          description: 请求的唯一标识符，用于追踪和支持。
        code:
          type: string
          description: 机器可读的错误码（如 `InvalidParameter`、`Throttling`、`Unauthorized`）。
          example: InvalidParameter
        message:
          type: string
          description: 人类可读的错误信息。
          example: Invalid model name
````

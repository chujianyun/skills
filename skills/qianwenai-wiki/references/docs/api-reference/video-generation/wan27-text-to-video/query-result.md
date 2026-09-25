> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Wan 2.7 — 查询结果

> 查询 Wan 2.7 文生视频任务状态

轮询任务状态，任务完成后下载生成的视频。

## 轮询策略

1. 保存[提交任务](/api-reference/video-generation/wan27-text-to-video/create-task)返回的 `task_id`。
2. 每 **15 秒**轮询一次本接口，直到 `task_status` 为 `SUCCEEDED` 或 `FAILED`。
3. 任务成功后，从 `video_url` 下载视频。

## 注意事项

- **链接有效期**：`video_url` 在 **24 小时**后过期，请及时下载。
- **状态流转**：`PENDING` → `RUNNING` → `SUCCEEDED` / `FAILED`。

## OpenAPI

````yaml get /tasks/{task_id}
openapi: 3.1.0
info:
  title: Wan 2.7 文字生成视频 API
  description: 使用 Wan 2.7 模型从文本生成视频。提交异步任务后，通过轮询 `GET /tasks/{task_id}` 获取生成结果。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 千问AI平台
security:
  - BearerAuth: []
paths:
  /tasks/{task_id}:
    get:
      operationId: getWan27TextToVideoTaskStatus
      summary: 查询任务结果
      description: 轮询已提交任务的状态，任务完成后获取视频 URL。
      parameters:
        - name: task_id
          in: path
          required: true
          description: 来自 POST 响应的任务 ID。
          schema:
            type: string
      responses:
        "200":
          description: 成功获取任务状态
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Wan27TaskStatusResponse"
              examples:
                SUCCEEDED:
                  summary: 任务成功
                  value:
                    request_id: caa62a12-8841-41a6-8af2-xxxxxx
                    output:
                      task_id: eff1443c-ccab-4676-aad3-xxxxxx
                      task_status: SUCCEEDED
                      submit_time: 2025-09-29 14:18:52.331
                      scheduled_time: 2025-09-29 14:18:59.290
                      end_time: 2025-09-29 14:23:39.407
                      orig_prompt: An epic and cute scene. A small, adorable cartoon kitten general, wearing exquisitely detailed golden armor and a slightly oversized helmet, stands bravely on a cliff.
                      video_url: https://dashscope-result-sh.oss-accelerate.aliyuncs.com/xxx.mp4?Expires=xxx
                    usage:
                      duration: 10
                      input_video_duration: 0
                      output_video_duration: 10
                      video_count: 1
                      ratio: 16:9
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
                      submit_time: 2025-09-29 14:18:52.331
                      scheduled_time: 2025-09-29 14:18:59.290
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
            # 将 {task_id} 替换为提交任务后返回的实际任务 ID
            curl -X GET 'https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY"
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    Wan27TextToVideoRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型标识符。可选值：`wan2.7-t2v`（主线版本，持续更新）、`wan2.7-t2v-2026-06-12`（最新快照版本）、`wan2.7-t2v-2026-04-25`（旧快照版本）。
          enum:
            - wan2.7-t2v
            - wan2.7-t2v-2026-06-12
            - wan2.7-t2v-2026-04-25
          example: wan2.7-t2v
        input:
          type: object
          required:
            - prompt
          description: 视频生成的输入内容。
          properties:
            prompt:
              type: string
              description: "描述您想要生成的视频内容，支持中英文，最多 5,000 个字符（超出自动截断）。多镜头视频可按时间戳描述每个镜头，例如：`Shot 1 [0-3 seconds] wide shot: ...`。"
              example: A kitten running in the moonlight.
            negative_prompt:
              type: string
              description: 描述视频中不想出现的内容（如 `low quality, blurry, extra fingers`），支持中英文，最多 500 个字符（超出自动截断）。
              example: low resolution, error, worst quality, low quality, deformed, extra fingers, bad proportions
            audio_url:
              type: string
              format: uri
              description: 用于口型同步和动作对齐的音频文件 URL。模型会将人物的口型动作与音频轨道匹配。支持通过 HTTP/HTTPS 访问的 WAV 和 MP3 格式，时长 2-30 秒，大小不超过 15 MB。音频长于视频时将被截断；短于视频时，剩余部分保持静音。若不填写，模型将自动生成匹配的背景音乐或音效。
        parameters:
          $ref: "#/components/schemas/Wan27TextToVideoParameters"
    Wan27TextToVideoParameters:
      type: object
      description: 视频生成参数。
      properties:
        resolution:
          type: string
          description: |-
            视频清晰度等级，分辨率越高费用越高。

            实际输出尺寸取决于 `ratio`：
            - **720P**：16:9=1280x720，9:16=720x1280，1:1=960x960，4:3=1104x832，3:4=832x1104
            - **1080P**：16:9=1920x1080，9:16=1080x1920，1:1=1440x1440，4:3=1648x1248，3:4=1248x1648
          enum:
            - 720P
            - 1080P
          default: 1080P
        ratio:
          type: string
          description: 生成视频的宽高比，默认值：`16:9`。
          enum:
            - 16:9
            - 9:16
            - 1:1
            - 4:3
            - 3:4
          default: 16:9
        duration:
          type: integer
          description: 视频时长（秒），取整数，范围 2-15。时长越长费用越高，按秒计费。
          minimum: 2
          maximum: 15
          default: 5
        prompt_extend:
          type: boolean
          description: 在生成前使用大语言模型对提示词进行改写扩展。对简短或模糊的提示词效果提升明显，但会增加响应时延。设为 `false` 可直接使用原始提示词。
          default: true
        watermark:
          type: boolean
          description: 在视频右下角添加「AI 生成」水印。
          default: false
        seed:
          type: integer
          description: 用于生成可复现结果的随机种子。相同种子和参数产生相近（而非完全相同）的输出。
          minimum: 0
          maximum: 2147483647
    AsyncTaskSubmitResponse:
      type: object
      description: 异步任务提交的响应。
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
              description: 任务初始状态，通常为 `PENDING`。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
    Wan27TaskStatusResponse:
      type: object
      description: Wan 2.7 文字生成视频的任务状态响应。
      properties:
        request_id:
          type: string
          description: 请求 ID，用于排查问题。联系技术支持时请提供此 ID。
          example: caa62a12-8841-41a6-8af2-xxxxxx
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID，提交后 24 小时内可查询。
              example: eff1443c-ccab-4676-aad3-xxxxxx
            task_status:
              type: string
              description: 任务生命周期：`PENDING` -> `RUNNING` -> `SUCCEEDED` 或 `FAILED`。手动停止时为 `CANCELED`，超期后为 `UNKNOWN`。
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
              example: 2025-09-29 14:18:52.331
            scheduled_time:
              type: string
              description: 任务开始执行的时间（UTC+8，格式：`YYYY-MM-DD HH:mm:ss.SSS`）。
              example: 2025-09-29 14:18:59.290
            end_time:
              type: string
              description: 任务结束时间（UTC+8，格式：`YYYY-MM-DD HH:mm:ss.SSS`）。仅在任务状态为 `SUCCEEDED` 或 `FAILED` 时返回。
              example: 2025-09-29 14:23:39.407
            orig_prompt:
              type: string
              description: 经 `prompt_extend` 改写前的原始提示词。
            video_url:
              type: string
              format: uri
              description: 生成视频的 URL（MP4 格式，H.264 编码）。仅在 `task_status` 为 `SUCCEEDED` 时返回。**链接 24 小时内有效**，请及时下载。
              example: https://dashscope-result-sh.oss-accelerate.aliyuncs.com/xxx.mp4?Expires=xxx
            code:
              type: string
              description: 错误码，仅在 `task_status` 为 `FAILED` 时返回。
            message:
              type: string
              description: 错误信息，仅在 `task_status` 为 `FAILED` 时返回。
        usage:
          type: object
          description: 资源用量，仅在 `task_status` 为 `SUCCEEDED` 时返回。
          properties:
            duration:
              type: number
              description: 计费视频时长（秒），等于 `output_video_duration`。
            input_video_duration:
              type: integer
              description: 文字生成视频时始终为 `0`（无输入视频）。
            output_video_duration:
              type: integer
              description: 输出视频时长（秒），与请求的 `duration` 一致。
            video_count:
              type: integer
              description: 生成的视频数量，始终为 `1`。
            ratio:
              type: string
              description: 实际使用的宽高比（如 `16:9`），与请求的 `ratio` 一致。
            SR:
              type: integer
              description: 实际使用的分辨率等级（如 `720` 对应 720P，`1080` 对应 1080P），与请求的 `resolution` 一致。
    DashScopeErrorResponse:
      type: object
      description: DashScope API 错误响应。
      properties:
        request_id:
          type: string
          description: 请求的唯一标识符，用于追踪和技术支持。
        code:
          type: string
          description: 机器可读的错误码（如 `InvalidParameter`、`Throttling`、`Unauthorized`）。
          example: InvalidParameter
        message:
          type: string
          description: 人类可读的错误信息。
          example: Invalid model name
````

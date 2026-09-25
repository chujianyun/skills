> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Wan — 查询结果

> 查询视频生成任务状态

查询首尾帧视频生成任务的状态和结果。

## 轮询策略

1. [创建任务](/api-reference/video-generation/wan-image-to-video-first-last-frames/create-task)，获取 `task_id`。
2. 每 **15 秒**轮询一次，直到 `task_status` 为 `SUCCEEDED` 或 `FAILED`。
3. 任务成功后，从 `video_url` 获取生成的视频。

## 注意事项

- **URL 有效期**：视频 URL 在 **24 小时**后过期，请及时下载。
- **状态流转**：`PENDING` → `RUNNING` → `SUCCEEDED` 或 `FAILED`。

## OpenAPI

````yaml get /tasks/{task_id}
openapi: 3.1.0
info:
  title: Wan 图生视频（首尾帧）API
  description: 使用 Wan kf2v 模型，基于首帧图像、尾帧图像和文本提示词，生成过渡自然流畅的视频。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 千问AI平台
security:
  - BearerAuth: []
paths:
  /tasks/{task_id}:
    get:
      operationId: getI2VFirstLastTaskStatus
      summary: 查询任务结果
      description: 查询视频生成任务的状态和结果。
      parameters:
        - name: task_id
          in: path
          required: true
          description: 要查询的任务 ID。
          schema:
            type: string
      responses:
        "200":
          description: 成功获取任务状态
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/TaskStatusResponse"
              examples:
                SUCCEEDED:
                  summary: 任务成功
                  value:
                    request_id: c1209113-8437-424f-a386-xxxxxx
                    output:
                      task_id: 966cebcd-dedc-4962-af88-xxxxxx
                      task_status: SUCCEEDED
                      video_url: https://dashscope-result-sh.oss-accelerate.aliyuncs.com/xxx.mp4?Expires=xxx
                      task_metrics:
                        TOTAL: 1
                        SUCCEEDED: 1
                        FAILED: 0
                    usage:
                      video_count: 1
                      video_duration: 5
                FAILED:
                  summary: 任务失败
                  value:
                    request_id: c1209113-8437-424f-a386-xxxxxx
                    output:
                      task_id: 966cebcd-dedc-4962-af88-xxxxxx
                      task_status: FAILED
                      code: InvalidParameter
                      message: The specified parameter is not valid.
                      task_metrics:
                        TOTAL: 1
                        SUCCEEDED: 0
                        FAILED: 1
                RUNNING:
                  summary: 任务进行中
                  value:
                    request_id: c1209113-8437-424f-a386-xxxxxx
                    output:
                      task_id: 966cebcd-dedc-4962-af88-xxxxxx
                      task_status: RUNNING
                      task_metrics:
                        TOTAL: 1
                        SUCCEEDED: 0
                        FAILED: 0
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
    I2VFirstLastRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称。
          enum:
            - wan2.2-kf2v-flash
            - wan2.1-kf2v-plus
          example: wan2.2-kf2v-flash
        input:
          type: object
          required:
            - first_frame_url
            - last_frame_url
          description: 输入数据，包含首尾帧图像和可选提示词。
          properties:
            prompt:
              type: string
              description: 描述期望视频内容的文本提示词。支持中英文，最长 800 个字符，超出部分自动截断。若首尾帧的主体或场景发生变化，建议描述过渡方式（如镜头运动或主体动作）。
              maxLength: 800
              example: Realistic style, a small black cat looks up at the sky curiously, the camera gradually rises from eye level, and finally captures its curious gaze from a top-down view.
            negative_prompt:
              type: string
              description: 描述视频中不希望出现的内容。支持中英文，最长 500 个字符，超出部分自动截断。
              maxLength: 500
              example: low resolution, error, worst quality, low quality, deformed, extra fingers, bad proportions
            first_frame_url:
              type: string
              description: 首帧图像的 URL。输出视频的宽高比与该图像一致。必须可公开访问（HTTP 或 HTTPS）。**图像要求**：格式：JPEG、JPG、PNG（无 Alpha 通道）、BMP 或 WEBP；分辨率：每边 360–2000 像素；文件大小：不超过 10 MB。
              example: https://wanx.alicdn.com/material/20250318/first_frame.png
            last_frame_url:
              type: string
              description: 尾帧图像的 URL。必须可公开访问（HTTP 或 HTTPS）。分辨率可与首帧不同，无需对齐。**图像要求**：格式：JPEG、JPG、PNG（无 Alpha 通道）、BMP 或 WEBP；分辨率：每边 360–2000 像素；文件大小：不超过 10 MB。
              example: https://wanx.alicdn.com/material/20250318/last_frame.png
        parameters:
          $ref: "#/components/schemas/I2VFirstLastParameters"
    I2VFirstLastParameters:
      type: object
      description: 视频生成参数。
      properties:
        resolution:
          type: string
          description: 生成视频的分辨率档位。调整清晰度（总像素数）但不改变宽高比。视频宽高比与首帧图像一致。**分辨率影响计费**：1080P > 720P > 480P。可选值取决于模型：`wan2.2-kf2v-flash`：480P、720P、1080P（默认：720P）；`wan2.1-kf2v-plus`：480P、720P（默认：720P）。
          enum:
            - 480P
            - 720P
            - 1080P
          default: 720P
          example: 720P
        duration:
          type: integer
          description: 生成视频的时长（秒）。固定为 5 秒，不可修改。
          enum:
            - 5
          default: 5
        prompt_extend:
          type: boolean
          description: 是否启用提示词优化。启用后，大语言模型将对输入提示词进行改写，对短提示词效果更佳，但会增加处理时间。默认值：`true`。
          default: true
        watermark:
          type: boolean
          description: 在视频右下角添加「AI 生成」水印。默认值：`false`。
          default: false
        seed:
          type: integer
          description: 随机数种子，用于控制生成结果的可复现性。范围：[0, 2147483647]。不填则使用随机种子。即使设置种子，结果仍可能因模型随机性而有所不同。
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
              description: 用于轮询任务状态的任务 ID，配合 `GET /tasks/{task_id}` 使用。有效期 24 小时。
              example: 0385dc79-5ff8-4d82-bcb6-xxxxxx
            task_status:
              type: string
              description: 任务的初始状态，通常为 `PENDING`。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - CANCELED
                - UNKNOWN
    TaskStatusResponse:
      type: object
      description: 查询任务状态的响应结果。
      properties:
        request_id:
          type: string
          description: 请求的唯一标识符，用于追踪和排查问题。
          example: ec016349-6b14-9ad6-8009-xxxxxx
        output:
          type: object
          description: 任务输出信息。
          properties:
            task_id:
              type: string
              description: 任务 ID。
              example: 3f21a745-9f4b-4588-b643-xxxxxx
            task_status:
              type: string
              description: 任务当前状态。状态流转：PENDING → RUNNING → SUCCEEDED 或 FAILED。UNKNOWN 表示任务不存在或已过期。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - CANCELED
                - UNKNOWN
            submit_time:
              type: string
              description: 任务提交时间（UTC+8）。格式：YYYY-MM-DD HH:mm:ss.SSS。
              example: 2025-04-18 10:36:58.394
            scheduled_time:
              type: string
              description: 任务开始运行时间（UTC+8）。格式：YYYY-MM-DD HH:mm:ss.SSS。
              example: 2025-04-18 10:37:13.802
            end_time:
              type: string
              description: 任务完成时间（UTC+8）。格式：YYYY-MM-DD HH:mm:ss.SSS。
              example: 2025-04-18 10:45:23.004
            video_url:
              type: string
              description: 生成视频的 URL（MP4 格式，H.264 编码）。仅在 `task_status` 为 `SUCCEEDED` 时返回。有效期 24 小时。
              example: https://dashscope-result-wlcb.oss-cn-wulanchabu.aliyuncs.com/xxx.mp4?xxxxx
            orig_prompt:
              type: string
              description: 原始输入提示词。
            actual_prompt:
              type: string
              description: 启用提示词优化后实际使用的改写提示词。未启用提示词优化时不返回此字段。
            code:
              type: string
              description: 错误码。仅在任务失败时返回。
            message:
              type: string
              description: 详细错误信息。仅在任务失败时返回。
        usage:
          type: object
          description: 用量统计。仅在任务成功时返回。
          properties:
            video_duration:
              type: integer
              description: 视频时长（秒）。固定值：5。计费公式：费用 = 视频时长（秒）× 单价。
              example: 5
            video_count:
              type: integer
              description: 生成的视频数量。固定为 1。
              example: 1
            video_ratio:
              type: string
              description: 视频宽高比。仅 wan2.1 模型返回。固定为 `standard`。
              example: standard
            SR:
              type: integer
              description: 视频分辨率档位。仅 wan2.2 模型返回。可选值：480、720 或 1080。
              enum:
                - 480
                - 720
                - 1080
              example: 480
    DashScopeErrorResponse:
      type: object
      description: DashScope API 错误响应。
      properties:
        request_id:
          type: string
          description: 请求的唯一标识符。
        code:
          type: string
          description: 错误码（如 `InvalidParameter`、`InvalidApiKey`、`Throttling`）。
          example: InvalidApiKey
        message:
          type: string
          description: 人类可读的错误信息。
          example: No API-key provided.
````

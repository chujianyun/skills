> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Wan — 查询结果

> 查询动画生成状态

查询任务状态并获取生成的动画。

## 轮询策略

1. 调用[创建任务](/api-reference/video-generation/wan-image-to-animation/create-task)接口获取 `task_id`。
2. 每 **15 秒**轮询一次，直到 `task_status` 为 `SUCCEEDED`、`FAILED` 或 `CANCELED`。
3. 任务成功后，从 `output.results.video_url` 获取动画。

## 注意事项

- **URL 有效期**：动画 URL 在 **24 小时**后过期，请及时下载。
- **状态流转**：`PENDING` → `RUNNING` → `SUCCEEDED`、`FAILED` 或 `CANCELED`。`UNKNOWN` 表示任务不存在或查询已超过 24 小时。

## OpenAPI

````yaml get /tasks/{task_id}
openapi: 3.1.0
info:
  title: Wan 图像转动画 API
  description: 使用 wan2.2-animate-move 模型，将参考视频中的人物动作与表情迁移到输入图片，生成动画视频。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 千问AI平台
security:
  - BearerAuth: []
paths:
  /tasks/{task_id}:
    get:
      operationId: getImageToAnimationTaskStatus
      summary: 查询任务结果
      description: 查询动画任务的状态和结果。
      parameters:
        - name: task_id
          in: path
          required: true
          description: POST 接口返回的任务 ID。
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
                    request_id: a67f8716-18ef-447c-a286-xxxxxx
                    output:
                      task_id: 0385dc79-5ff8-4d82-bcb6-xxxxxx
                      task_status: SUCCEEDED
                      submit_time: 2025-09-18 15:32:00.105
                      scheduled_time: 2025-09-18 15:32:15.066
                      end_time: 2025-09-18 15:34:41.898
                      results:
                        video_url: https://dashscope-result-sh.oss-accelerate.aliyuncs.com/xxxxx.mp4?Expires=xxxxxx
                    usage:
                      video_duration: 5.2
                      video_ratio: standard
                FAILED:
                  summary: 任务失败
                  value:
                    request_id: daad9007-6acd-9fb3-a6bc-xxxxxx
                    output:
                      task_id: fe8aa114-d9f1-4f76-b598-xxxxxx
                      task_status: FAILED
                      code: InternalError
                      message: xxxxxx
                RUNNING:
                  summary: 任务运行中
                  value:
                    request_id: c1209113-8437-424f-a386-xxxxxx
                    output:
                      task_id: 0385dc79-5ff8-4d82-bcb6-xxxxxx
                      task_status: RUNNING
        "400":
          description: 无效请求
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
      x-codeSamples:
        - lang: curl
          label: cURL - 查询任务结果
          source: |-
            # 将 {task_id} 替换为提交响应中返回的实际任务 ID
            curl -X GET 'https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY"
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    ImageToAnimationRequest:
      type: object
      required:
        - model
        - input
        - parameters
      properties:
        model:
          type: string
          description: 模型名称，必须为 `wan2.2-animate-move`。
          enum:
            - wan2.2-animate-move
          example: wan2.2-animate-move
        input:
          type: object
          required:
            - image_url
            - video_url
          description: 输入数据，包含人物图像和参考视频。
          properties:
            image_url:
              type: string
              description: |-
                人物输入图像的公开访问 URL。

                **图像要求：**
                - 格式：JPG、JPEG、PNG、BMP 或 WEBP。
                - 尺寸：宽和高均须在 [200, 4096] 像素范围内，宽高比须在 1:3 至 3:1 之间。
                - 文件大小：不超过 5 MB。
                - 内容：图像中须包含单个正面朝向的人物，面部清晰无遮挡，占画面比例适中。

                包含非 ASCII 字符（如中文）的 URL 须进行 URL 编码。
              example: https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250919/adsyrp/move_input_image.jpeg
            video_url:
              type: string
              description: |-
                参考视频的公开访问 URL。模型将该视频中的人物动作和表情迁移到输入图像上。

                **视频要求：**
                - 格式：MP4、AVI 或 MOV。
                - 时长：2 至 30 秒。
                - 尺寸：宽和高均须在 [200, 2048] 像素范围内，宽高比须在 1:3 至 3:1 之间。
                - 文件大小：不超过 200 MB。
                - 内容：视频中须包含单个正面朝向的人物，面部清晰无遮挡，占画面比例适中。

                使用分辨率更高、帧率更高的参考视频可获得更好的效果。包含非 ASCII 字符的 URL 须进行 URL 编码。
              example: https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250919/kaakcn/move_input_video.mp4
            watermark:
              type: boolean
              description: 是否在视频右下角添加"由通义 AI 生成"水印。
              default: false
              example: true
        parameters:
          $ref: "#/components/schemas/ImageToAnimationParameters"
    ImageToAnimationParameters:
      type: object
      required:
        - mode
      description: 视频生成参数。
      properties:
        mode:
          type: string
          description: |-
            服务模式。
            - `wan-std`：标准模式，生成速度更快，成本更低，适合快速预览和基础动画效果。
            - `wan-pro`：专业模式，动画效果更流畅、质量更高，但处理时间较长，成本更高。
          enum:
            - wan-std
            - wan-pro
          example: wan-std
        check_image:
          type: boolean
          description: 是否对输入图像进行合规性校验。
          default: true
          example: true
    AsyncTaskSubmitResponse:
      type: object
      description: 异步任务提交的响应结果。
      properties:
        request_id:
          type: string
          description: 用于追踪和排查问题的唯一请求标识符。
          example: 4909100c-7b5a-9f92-bfe5-xxxxxx
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 用于轮询任务状态的任务 ID，配合 `GET /tasks/{task_id}` 使用，有效期 24 小时。
              example: 0385dc79-5ff8-4d82-bcb6-xxxxxx
            task_status:
              type: string
              description: 初始任务状态，通常为 `PENDING`。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - CANCELED
                - UNKNOWN
              example: PENDING
    TaskStatusResponse:
      type: object
      description: 轮询任务状态的响应结果。
      properties:
        request_id:
          type: string
          description: 唯一请求标识符。
          example: a67f8716-18ef-447c-a286-xxxxxx
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID。
              example: 0385dc79-5ff8-4d82-bcb6-xxxxxx
            task_status:
              type: string
              description: 当前任务状态。状态流转：PENDING → RUNNING → SUCCEEDED 或 FAILED。CANCELED 表示任务已取消。UNKNOWN 表示任务不存在或查询已超过 24 小时。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - CANCELED
                - UNKNOWN
            submit_time:
              type: string
              description: 任务提交时间，UTC+8 格式：YYYY-MM-DD HH:mm:ss.SSS。
              example: 2025-09-18 15:32:00.105
            scheduled_time:
              type: string
              description: 任务开始运行时间，UTC+8 格式：YYYY-MM-DD HH:mm:ss.SSS。
              example: 2025-09-18 15:32:15.066
            end_time:
              type: string
              description: 任务完成时间，UTC+8 格式：YYYY-MM-DD HH:mm:ss.SSS。
              example: 2025-09-18 15:34:41.898
            results:
              type: object
              description: 任务结果，仅在 `task_status` 为 `SUCCEEDED` 时返回。
              properties:
                video_url:
                  type: string
                  description: 生成视频的 URL，有效期 24 小时，请及时下载。MP4 格式，H.264 编码。
                  example: https://dashscope-result-sh.oss-accelerate.aliyuncs.com/xxxxx.mp4?Expires=xxxxxx
            code:
              type: string
              description: 错误码，仅在任务失败时返回。
            message:
              type: string
              description: 详细错误信息，仅在任务失败时返回。
        usage:
          type: object
          description: 输出统计信息，仅在任务成功时返回。
          properties:
            video_duration:
              type: number
              description: 生成视频的时长，单位为秒。
              example: 5.2
            video_ratio:
              type: string
              description: 实际使用的服务模式：`wan-std` 对应 `standard`，`wan-pro` 对应 `pro`。
              enum:
                - standard
                - pro
              example: standard
    DashScopeErrorResponse:
      type: object
      description: DashScope API 错误响应。
      properties:
        request_id:
          type: string
          description: 唯一请求标识符。
        code:
          type: string
          description: 错误码（例如 `InvalidApiKey`、`InvalidParameter`、`Throttling`）。
          example: InvalidApiKey
        message:
          type: string
          description: 可读的错误描述信息。
          example: No API-key provided.
````

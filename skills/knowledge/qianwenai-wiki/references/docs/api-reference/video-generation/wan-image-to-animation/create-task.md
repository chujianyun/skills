> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Wan — 创建任务

> 提交动画生成任务

## OpenAPI

````yaml post /services/aigc/image2video/video-synthesis
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
  /services/aigc/image2video/video-synthesis:
    post:
      operationId: createImageToAnimationTask
      summary: 创建图像转动画任务
      description: 创建图像转动画任务。
      parameters:
        - name: X-DashScope-Async
          in: header
          required: true
          description: 必须设置为 `enable`。HTTP 请求仅支持异步处理。省略此请求头将返回"当前用户 API 不支持同步调用"的错误。
          schema:
            type: string
            enum:
              - enable
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/ImageToAnimationRequest"
      responses:
        "200":
          description: 任务提交成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/AsyncTaskSubmitResponse"
        "400":
          description: 请求参数无效
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
      x-codeSamples:
        - lang: curl
          label: cURL - 图像转动画
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
              "model": "wan2.2-animate-move",
              "input": {
                "image_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250919/adsyrp/move_input_image.jpeg",
                "video_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250919/kaakcn/move_input_video.mp4",
                "watermark": true
              },
              "parameters": {
                "mode": "wan-std"
              }
            }'
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

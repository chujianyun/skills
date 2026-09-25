> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Wan — 创建任务

> 提交视频角色替换任务

该模型将视频中的主角替换为指定图片中的人物，同时保留原始场景、光照、动作和表情，实现自然融合。

## 服务模式

`wan2.2-animate-mix` 提供两种服务模式：

| 模式   | 取值        | 说明                     |
| ---- | --------- | ---------------------- |
| 标准模式 | `wan-std` | 速度更快、成本更低，适合快速预览。      |
| 专业模式 | `wan-pro` | 画面更流畅、质量更高，但速度较慢、成本较高。 |

## OpenAPI

````yaml post /services/aigc/image2video/video-synthesis
openapi: 3.1.0
info:
  title: Wan 视频换脸 API
  description: Wan 视频换脸 API。将视频中的主角替换为图片中的人物，同时保留原视频的场景、光线和色调。采用异步任务方式处理。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 千问AI平台
security:
  - BearerAuth: []
paths:
  /services/aigc/image2video/video-synthesis:
    post:
      operationId: createCharacterSwap
      summary: 创建换脸任务
      description: 创建视频换脸任务。
      parameters:
        - name: X-DashScope-Async
          in: header
          required: true
          description: 异步任务提交时必须设置为 `enable`。若不包含此头部，将返回"当前用户 API 不支持同步调用"错误。
          schema:
            type: string
            enum:
              - enable
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/CharacterSwapRequest"
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
          label: cURL（提交任务）
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis' \
            --header 'X-DashScope-Async: enable' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --header 'Content-Type: application/json' \
            --data '{
              "model": "wan2.2-animate-mix",
              "input": {
                "image_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250919/bhkfor/mix_input_image.jpeg",
                "video_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250919/wqefue/mix_input_video.mp4",
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
    CharacterSwapRequest:
      type: object
      required:
        - model
        - input
        - parameters
      properties:
        model:
          type: string
          description: 模型名称。
          enum:
            - wan2.2-animate-mix
          example: wan2.2-animate-mix
        input:
          type: object
          required:
            - image_url
            - video_url
          description: 基础输入信息。
          properties:
            image_url:
              type: string
              format: uri
              description: |-
                输入人物图片的公开 HTTP 或 HTTPS 链接。URL 中不能包含非 ASCII 字符，如有请先进行编码。图片中需有单个正面人物，面部清晰可见，且在画面中占比适中。

                - **格式**：JPG、JPEG、PNG、BMP 或 WEBP。
                - **分辨率**：宽高均需在 [200, 4096] 像素范围内，宽高比需在 1:3 至 3:1 之间。
                - **文件大小**：不超过 5 MB。
              example: https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250919/bhkfor/mix_input_image.jpeg
            video_url:
              type: string
              format: uri
              description: |-
                输入参考视频的公开 HTTP 或 HTTPS 链接。URL 中不能包含非 ASCII 字符，如有请先进行编码。视频中需有单个正面人物，面部清晰可见，且在画面中占比适中。提高参考视频的分辨率和帧率有助于提升生成视频的质量。

                - **格式**：MP4、AVI 或 MOV。
                - **分辨率**：宽高均需在 [200, 2048] 像素范围内，宽高比需在 1:3 至 3:1 之间。
                - **文件大小**：不超过 200 MB。
                - **时长**：2 至 30 秒。
              example: https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250919/wqefue/mix_input_video.mp4
            watermark:
              type: boolean
              description: 是否在视频右下角添加"由 qwen.ai 生成"水印。
              default: false
        parameters:
          type: object
          required:
            - mode
          description: 生成参数。
          properties:
            check_image:
              type: boolean
              description: 是否对输入图片进行检测。`true`（默认）：API 对输入图片进行检测；`false`：跳过图片检测。
              default: true
            mode:
              type: string
              description: |-
                模型服务模式。

                - `wan-std`：标准模式。生成速度更快，成本更低，适合快速预览和基础动画场景。
                - `wan-pro`：专业模式。动画效果更流畅、质量更高，但处理时间和成本相应增加。
              enum:
                - wan-std
                - wan-pro
              example: wan-std
    AsyncTaskSubmitResponse:
      type: object
      description: 异步任务提交的响应结果。
      properties:
        request_id:
          type: string
          description: 唯一请求标识符，用于追踪和排查问题。
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
              description: 任务初始状态，通常为 `PENDING`。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - CANCELED
                - UNKNOWN
    TaskStatusResponse:
      type: object
      description: 轮询任务状态的响应结果。
      properties:
        request_id:
          type: string
          description: 唯一请求标识符，用于追踪和排查问题。
          example: a67f8716-18ef-447c-a286-xxxxxx
        output:
          type: object
          description: 任务输出信息。
          properties:
            task_id:
              type: string
              description: 任务 ID。有效期 24 小时。
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
              description: 任务提交时间，UTC+8，格式为 `YYYY-MM-DD HH:mm:ss.SSS`。
              example: 2025-09-18 15:32:00.105
            scheduled_time:
              type: string
              description: 任务开始运行的时间，UTC+8，格式为 `YYYY-MM-DD HH:mm:ss.SSS`。
              example: 2025-09-18 15:32:15.066
            end_time:
              type: string
              description: 任务完成时间，UTC+8，格式为 `YYYY-MM-DD HH:mm:ss.SSS`。
              example: 2025-09-18 15:34:41.898
            results:
              type: object
              description: 任务结果。仅在 `task_status` 为 `SUCCEEDED` 时返回。
              properties:
                video_url:
                  type: string
                  format: uri
                  description: 生成视频的 URL，MP4 格式（H.264 编码）。有效期 24 小时，请及时下载。
                  example: http://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxxxx.mp4?Expires=xxxxxx
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
              type: number
              description: 生成视频的时长，单位为秒。
              example: 5.2
            video_ratio:
              type: string
              description: 所使用的模型服务模式。`standard` 对应 `wan-std`；`pro` 对应 `wan-pro`。
              enum:
                - standard
                - pro
    DashScopeErrorResponse:
      type: object
      description: DashScope API 错误响应。
      properties:
        request_id:
          type: string
          description: 唯一请求标识符。
          example: 7438d53d-6eb8-4596-8835-xxxxxx
        code:
          type: string
          description: 错误码（如 `InvalidApiKey`、`Throttling`、`InvalidParameter`）。
          example: InvalidApiKey
        message:
          type: string
          description: 可读的错误描述信息。
          example: No API-key provided.
````

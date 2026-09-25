> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Wan — 查询结果

> 查询视频编辑任务状态

查询任务状态并获取编辑后的视频。

## 轮询策略

1. 调用[编辑视频](/api-reference/video-generation/wan-general-video-editing/create-task)接口获取 `task_id`。
2. 每 **15 秒**轮询一次本接口，直到 `task_status` 为 `SUCCEEDED` 或 `FAILED`。
3. 任务成功后，从 `video_url` 字段下载视频。

## 注意事项

- **URL 有效期**：`video_url` 在 **24 小时**后过期，请及时下载。
- **任务状态流转**：`PENDING` → `RUNNING` → `SUCCEEDED`、`FAILED` 或 `CANCELLED`。

## OpenAPI

````yaml get /tasks/{task_id}
openapi: 3.1.0
info:
  title: Wan 视频编辑 API
  description: Wan 统一视频编辑 API，支持多模态输入（文本、图像、视频），提供五大核心能力：多图参考、视频重绘、局部编辑、视频续写和画面扩展。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 千问AI平台
security:
  - BearerAuth: []
paths:
  /tasks/{task_id}:
    get:
      operationId: getVideoEditingTaskStatus
      summary: 查询任务结果
      description: 查询视频编辑任务的状态与结果。
      parameters:
        - name: task_id
          in: path
          required: true
          description: 视频编辑任务创建接口返回的任务标识符。
          schema:
            type: string
      responses:
        "200":
          description: 任务状态获取成功。
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
                  summary: 任务运行中
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
          description: 请求参数无效。
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
    VideoEditingRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称。
          enum:
            - wanx2.1-vace-plus
          example: wanx2.1-vace-plus
        input:
          $ref: "#/components/schemas/VideoEditingInput"
        parameters:
          $ref: "#/components/schemas/VideoEditingParameters"
    VideoEditingInput:
      type: object
      required:
        - function
        - prompt
      description: 视频编辑的输入数据，各功能所需字段不同。
      properties:
        function:
          type: string
          description: 要使用的视频编辑能力。
          enum:
            - image_reference
            - video_repainting
            - video_edit
            - video_extension
            - video_outpainting
          example: image_reference
        prompt:
          type: string
          description: 对目标视频内容的文字描述。
          example: In the video, a girl walks out from the depths of an ancient, misty forest.
        ref_images_url:
          type: array
          description: 参考图像 URL 数组。`image_reference` 功能使用（1-3 张图像），`video_repainting` 和 `video_edit` 可选使用（1 张图像，用于替换主体）。
          items:
            type: string
            format: uri
          minItems: 1
          maxItems: 3
          example:
            - http://wanx.alicdn.com/material/20250318/image_reference_2_5_16.png
            - http://wanx.alicdn.com/material/20250318/image_reference_1_5_16.png
        video_url:
          type: string
          format: uri
          description: 输入视频的 URL。`video_repainting`、`video_edit` 和 `video_outpainting` 必填。格式须为 MP4，大小不超过 50 MB，时长不超过 5 秒。
          example: http://wanx.alicdn.com/material/20250318/video_repainting_1.mp4
        mask_image_url:
          type: string
          format: uri
          description: 用于 `video_edit` 的蒙版图像 URL。白色区域将被编辑，黑色区域保持不变。与 `mask_video_url` 二选一。
        mask_video_url:
          type: string
          format: uri
          description: 用于 `video_edit` 的蒙版视频 URL。与 `mask_image_url` 二选一，推荐使用 `mask_image_url`。
        mask_frame_id:
          type: integer
          description: 用于带 `mask_image_url` 的 `video_edit`：指定蒙版对应的视频帧索引。默认为第一帧（0）。
          default: 0
          example: 1
        first_clip_url:
          type: string
          format: uri
          description: 用于 `video_extension`：第一段视频片段的 URL（不超过 3 秒）。模型将基于此片段生成后续内容。
        last_clip_url:
          type: string
          format: uri
          description: 用于 `video_extension`：最后一段视频片段的 URL（不超过 3 秒）。模型将生成其前面的内容。
        first_frame_url:
          type: string
          format: uri
          description: 用于 `video_extension`：首帧图像的 URL，视频将从该帧向后延伸生成。
        last_frame_url:
          type: string
          format: uri
          description: 用于 `video_extension`：末帧图像的 URL，视频将从该帧向前追溯生成。
    VideoEditingParameters:
      type: object
      description: 视频编辑的生成参数，可用参数因功能而异。
      properties:
        prompt_extend:
          type: boolean
          description: 启用提示词改写。`true`（默认）：模型自动优化提示词；`false`：原样使用提示词。`video_repainting` 时建议关闭此项。
          default: true
        size:
          type: string
          description: 输出分辨率，格式为 `宽*高`。用于 `image_reference` 和 `video_edit`。
          example: 1280*720
        obj_or_bg:
          type: array
          description: 用于 `image_reference`：标识每张参考图像为主体（`obj`）或背景（`bg`）。数组长度须与 `ref_images_url` 一致。
          items:
            type: string
            enum:
              - obj
              - bg
          example:
            - obj
            - bg
        control_condition:
          type: string
          description: 用于 `video_repainting`：视频特征提取方式，决定保留原视频中的哪些特征。
          enum:
            - posebodyface
            - posebody
            - depth
            - scribble
          example: depth
        strength:
          type: number
          description: 用于 `video_repainting`：控制特征提取强度。值越高，输出越接近原视频；值越低，创意空间越大。
          minimum: 0
          maximum: 1
          default: 1
        mask_type:
          type: string
          description: 用于 `video_edit`：指定编辑区域的行为。`tracking`（默认）：编辑区域自动跟随目标运动；`fixed`：编辑区域固定不动。
          enum:
            - tracking
            - fixed
          default: tracking
        expand_ratio:
          type: number
          description: "用于带 `mask_type: tracking` 的 `video_edit`：蒙版区域向外扩展的比例。值越小越贴合目标，值越大扩展范围越广。"
          minimum: 0
          maximum: 1
          default: 0.05
        top_scale:
          type: number
          description: 用于 `video_outpainting`：向上扩展比例。设为 1.5 时，顶部扩展至原高度的 1.5 倍。
          minimum: 1
          maximum: 2
          default: 1
        bottom_scale:
          type: number
          description: 用于 `video_outpainting`：向下扩展比例。
          minimum: 1
          maximum: 2
          default: 1
        left_scale:
          type: number
          description: 用于 `video_outpainting`：向左扩展比例。
          minimum: 1
          maximum: 2
          default: 1
        right_scale:
          type: number
          description: 用于 `video_outpainting`：向右扩展比例。
          minimum: 1
          maximum: 2
          default: 1
    AsyncTaskSubmitResponse:
      type: object
      description: 异步任务创建成功后的响应。
      properties:
        request_id:
          type: string
          description: 唯一请求标识符。
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务标识符，可使用 `GET /tasks/{task_id}` 轮询任务结果。
            task_status:
              type: string
              description: 初始任务状态，通常为 `PENDING`。
              enum:
                - PENDING
    TaskStatusResponse:
      type: object
      description: 包含视频编辑任务当前状态与结果的响应。
      properties:
        request_id:
          type: string
          description: 唯一请求标识符。
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务标识符。
            task_status:
              type: string
              description: 当前任务状态。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - CANCELLED
            video_url:
              type: string
              format: uri
              description: 生成的视频 URL，仅在 `task_status` 为 `SUCCEEDED` 时存在。有效期 24 小时，请及时下载。
            code:
              type: string
              description: 错误代码，仅在 `task_status` 为 `FAILED` 时存在。
            message:
              type: string
              description: 错误信息，仅在 `task_status` 为 `FAILED` 时存在。
        usage:
          type: object
          description: 用量统计（仅在任务成功时存在）。
          properties:
            video_count:
              type: integer
              description: 生成的视频数量。
            video_duration:
              type: integer
              description: 生成视频的时长（秒）。
    DashScopeErrorResponse:
      type: object
      description: DashScope API 错误响应。
      properties:
        request_id:
          type: string
          description: 唯一请求标识符。
        code:
          type: string
          description: 错误代码（如 `InvalidParameter`、`Throttling`、`Unauthorized`）。
          example: InvalidParameter
        message:
          type: string
          description: 可读的错误描述。
          example: "Invalid parameter: function"
````

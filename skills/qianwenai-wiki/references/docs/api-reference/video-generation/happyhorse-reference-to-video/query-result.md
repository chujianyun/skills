> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# HappyHorse -- 查询参考生视频结果

> 查询 HappyHorse 参考生视频任务状态

轮询任务状态，任务成功后下载视频。

## 轮询策略

1. 保存[提交任务](/api-reference/video-generation/happyhorse-reference-to-video/create-task)响应中的 `task_id`。
2. 每 **15 秒**轮询本接口，直到 `task_status` 为 `SUCCEEDED` 或 `FAILED`。
3. 在 **24 小时**内通过 `video_url` 下载视频 -- 链接过期后将无法访问。

## OpenAPI

````yaml get /tasks/{task_id}
openapi: 3.1.0
info:
  title: HappyHorse 参考生视频 API
  description: 使用 HappyHorse 模型传入多张参考图像生成视频。异步提交任务后，通过 `GET /tasks/{task_id}` 轮询获取结果。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 华北2（北京）
security:
  - BearerAuth: []
paths:
  /tasks/{task_id}:
    get:
      operationId: getHappyHorseRefToVideoTaskStatus
      summary: 查询参考生视频任务结果
      description: 轮询任务状态，任务成功后获取视频 URL。
      parameters:
        - name: task_id
          in: path
          required: true
          description: 提交任务时返回的任务 ID。
          schema:
            type: string
      responses:
        "200":
          description: 任务状态查询成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/HappyHorseR2VTaskStatusResponse"
              examples:
                SUCCEEDED:
                  summary: 任务执行成功
                  value:
                    request_id: 35137489-2862-96cb-b6f2-xxxxxx
                    output:
                      task_id: 1469cfc3-3004-4d9e-ab10-xxxxxx
                      task_status: SUCCEEDED
                      submit_time: 2026-04-25 15:03:25.848
                      scheduled_time: 2026-04-25 15:03:25.884
                      end_time: 2026-04-25 15:04:05.882
                      orig_prompt: "[Image 1]中身着红色旗袍的女性，镜头先以侧面中景勾勒旗袍修身剪裁与S型曲线，随即切换至低角度仰拍，捕捉她轻抬玉手展开[Image 2]中的折扇的同时，[Image 3]中的流苏耳坠随头部转动轻盈摆动的细节，最后推近至面部特写，定格在她指尖轻点扇骨、眼波流转间的含蓄风情，多视角全方位展现东方韵味。"
                      video_url: https://dashscope-result.oss-cn-beijing.aliyuncs.com/xxxx.mp4
                    usage:
                      duration: 5
                      input_video_duration: 0
                      output_video_duration: 5
                      video_count: 1
                      SR: 720
                      ratio: 16:9
                FAILED:
                  summary: 任务执行失败
                  value:
                    request_id: e5d70b02-ebd3-98ce-9fe8-759d7d7b107d
                    output:
                      task_id: 86ecf553-d340-4e21-af6e-a0c6a421c010
                      task_status: FAILED
                      code: InvalidParameter
                      message: The resolution is not valid xxxxxx
                RUNNING:
                  summary: 任务执行中
                  value:
                    request_id: c1209113-8437-424f-a386-xxxxxx
                    output:
                      task_id: 1469cfc3-3004-4d9e-ab10-xxxxxx
                      task_status: RUNNING
                      submit_time: 2026-04-25 15:03:25.848
                      scheduled_time: 2026-04-25 15:03:25.884
                UNKNOWN:
                  summary: 任务查询过期
                  value:
                    request_id: a4de7c32-7057-9f82-8581-xxxxxx
                    output:
                      task_id: 1469cfc3-3004-4d9e-ab10-xxxxxx
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
    HappyHorseRefToVideoRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称。可选值：`happyhorse-1.1-r2v`、`happyhorse-1.0-r2v`。
          enum:
            - happyhorse-1.1-r2v
            - happyhorse-1.0-r2v
          example: happyhorse-1.1-r2v
        input:
          type: object
          required:
            - prompt
            - media
          description: 输入的基本信息，包括参考图像和提示词。
          properties:
            prompt:
              type: string
              description: 文本提示词，用来描述生成视频中期望包含的元素和视觉特点。在 prompt 中通过 `[Image 1]`、`[Image 2]` 等标识指代 `media` 数组中对应位置的参考图像，顺序与 `media` 数组顺序一致。使用时需要指明参考图中的具体对象，例如"[Image 1]中身着红色旗袍的女性"。支持任何语言输入，长度不超过5000个非中文字符或2500个中文字符，超过部分会自动截断。
              example: "[Image 1]中身着红色旗袍的女性，优雅站立。"
            media:
              type: array
              description: 媒体素材列表（1-9张参考图像）。数组中的第 1 个 `reference_image` 对应 `[Image 1]`，第 2 个对应 `[Image 2]`，以此类推。
              items:
                type: object
                required:
                  - type
                  - url
                properties:
                  type:
                    type: string
                    description: 媒体素材类型。固定值：`reference_image`（参考图像）。
                    enum:
                      - reference_image
                  url:
                    type: string
                    format: uri
                    description: |-
                      参考图像 URL 或 Base64 编码数据。

                      **图像限制**：格式：JPEG、JPG、PNG、WEBP。分辨率：短边不低于 400 像素，推荐 720P 以上清晰图。文件大小：不超过 20 MB。

                      **支持的输入格式**：
                      - 公网 URL：支持 HTTP 或 HTTPS 协议。
                      - Base64 编码：格式为 `data:{MIME_type};base64,{base64_data}`。
              minItems: 1
              maxItems: 9
        parameters:
          $ref: "#/components/schemas/HappyHorseRefToVideoParameters"
    HappyHorseRefToVideoParameters:
      type: object
      description: 视频生成参数。
      properties:
        resolution:
          type: string
          description: 生成视频的分辨率档位。
          enum:
            - 480P
            - 720P
            - 1080P
          default: 1080P
        ratio:
          type: string
          description: 生成视频的宽高比。
          enum:
            - 16:9
            - 9:16
            - 1:1
            - 4:3
            - 3:4
            - 4:5
            - 5:4
            - 9:21
            - 21:9
          default: 16:9
        duration:
          type: integer
          description: 生成视频的时长，单位为秒。取值范围：3~15 之间的整数。
          minimum: 3
          maximum: 15
          default: 5
        watermark:
          type: boolean
          description: 是否在生成的视频上添加水印标识。水印位于视频右下角，文案固定为"Happy Horse"。`true`（默认）：添加水印。`false`：不添加水印。
          default: true
        seed:
          type: integer
          description: 随机数种子。相同的种子和参数会生成相似（但不完全相同）的结果。
          minimum: 0
          maximum: 2147483647
    AsyncTaskSubmitResponse:
      type: object
      description: 异步任务提交响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识，用于链路追踪和问题排查。
          example: 4909100c-7b5a-9f92-bfe5-xxxxxx
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID，用于后续轮询查询任务状态。配合 `GET /tasks/{task_id}` 使用。
              example: 0385dc79-5ff8-4d82-bcb6-xxxxxx
            task_status:
              type: string
              description: 初始任务状态，通常为 `PENDING`。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
    HappyHorseR2VTaskStatusResponse:
      type: object
      description: HappyHorse 参考生视频任务状态响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识。联系技术支持时请提供此 ID。
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID。提交后 24 小时内可查询。
            task_status:
              type: string
              description: 任务状态流转：`PENDING` -> `RUNNING` -> `SUCCEEDED` 或 `FAILED`。手动取消为 `CANCELED`，过期为 `UNKNOWN`。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - CANCELED
                - UNKNOWN
            submit_time:
              type: string
              description: 任务提交时间（UTC+8，`YYYY-MM-DD HH:mm:ss.SSS`）。
            scheduled_time:
              type: string
              description: 任务开始执行时间（UTC+8，`YYYY-MM-DD HH:mm:ss.SSS`）。
            end_time:
              type: string
              description: 任务结束时间（UTC+8）。仅在 `SUCCEEDED` 或 `FAILED` 时返回。
            orig_prompt:
              type: string
              description: 原始提示词文本。
            video_url:
              type: string
              format: uri
              description: 生成视频的 URL（MP4，H.264 编码）。仅在 `task_status` 为 `SUCCEEDED` 时返回。**链接有效期 24 小时**，请及时下载。
            code:
              type: string
              description: 错误码。仅在 `task_status` 为 `FAILED` 时返回。
            message:
              type: string
              description: 错误信息。仅在 `task_status` 为 `FAILED` 时返回。
        usage:
          type: object
          description: 资源消耗统计。仅在 `task_status` 为 `SUCCEEDED` 时返回。
          properties:
            duration:
              type: number
              description: 总的视频时长，用于计费，单位为秒。
            input_video_duration:
              type: integer
              description: 输入视频时长，单位秒。参考生视频固定为 0。
            output_video_duration:
              type: integer
              description: 输出视频时长，单位秒。
            video_count:
              type: integer
              description: 输出视频数量。固定为 1。
            ratio:
              type: string
              description: 生成视频的宽高比。
            SR:
              type: integer
              description: 输出视频的分辨率档位（如 720 表示 720P，1080 表示 1080P）。
    DashScopeErrorResponse:
      type: object
      description: DashScope API 错误响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识，用于链路追踪和问题排查。
        code:
          type: string
          description: 错误码（如 `InvalidParameter`、`Throttling`、`Unauthorized`）。
          example: InvalidParameter
        message:
          type: string
          description: 错误描述信息。
          example: Invalid model name
````

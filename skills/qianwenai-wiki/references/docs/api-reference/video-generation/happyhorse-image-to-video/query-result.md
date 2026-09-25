> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# HappyHorse -- 查询图生视频结果

> 查询 HappyHorse 图生视频任务状态

轮询任务状态，任务成功后下载视频。

## 轮询策略

1. 保存[提交任务](/api-reference/video-generation/happyhorse-image-to-video/create-task)响应中的 `task_id`。
2. 每 **15 秒**轮询本接口，直到 `task_status` 为 `SUCCEEDED` 或 `FAILED`。
3. 在 **24 小时**内通过 `video_url` 下载视频 -- 链接过期后将无法访问。

## OpenAPI

````yaml get /tasks/{task_id}
openapi: 3.1.0
info:
  title: HappyHorse 图生视频 API
  description: 使用 HappyHorse 模型以首帧图片为基础生成视频。异步提交任务后，通过 `GET /tasks/{task_id}` 轮询获取结果。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 华北2（北京）
security:
  - BearerAuth: []
paths:
  /tasks/{task_id}:
    get:
      operationId: getHappyHorseImageToVideoTaskStatus
      summary: 查询图生视频任务结果
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
                $ref: "#/components/schemas/HappyHorseI2VTaskStatusResponse"
              examples:
                SUCCEEDED:
                  summary: 任务执行成功
                  value:
                    request_id: 8ae698ba-df2d-966c-abcf-xxxxxx
                    output:
                      task_id: e56d806f-76f9-4037-aefa-xxxxxx
                      task_status: SUCCEEDED
                      submit_time: 2026-04-20 19:33:50.425
                      scheduled_time: 2026-04-20 19:33:50.463
                      end_time: 2026-04-20 19:35:34.216
                      orig_prompt: 一只猫在草地上奔跑
                      video_url: https://dashscope-result.oss-cn-beijing.aliyuncs.com/xxx.mp4?Expires=xxx
                    usage:
                      duration: 5
                      input_video_duration: 0
                      output_video_duration: 5
                      video_count: 1
                      SR: 720
                FAILED:
                  summary: 任务执行失败
                  value:
                    request_id: e5d70b02-ebd3-98ce-9fe8-759d7d7b107d
                    output:
                      task_id: 86ecf553-d340-4e21-af6e-a0c6a421c010
                      task_status: FAILED
                      code: InvalidParameter
                      message: The parameter is invalid.
                RUNNING:
                  summary: 任务执行中
                  value:
                    request_id: c1209113-8437-424f-a386-xxxxxx
                    output:
                      task_id: e56d806f-76f9-4037-aefa-xxxxxx
                      task_status: RUNNING
                      submit_time: 2026-04-20 19:33:50.425
                      scheduled_time: 2026-04-20 19:33:50.463
                UNKNOWN:
                  summary: 任务查询过期
                  value:
                    request_id: a4de7c32-7057-9f82-8581-xxxxxx
                    output:
                      task_id: e56d806f-76f9-4037-aefa-xxxxxx
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
    HappyHorseImageToVideoRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称。可选值：`happyhorse-1.1-i2v`、`happyhorse-1.0-i2v`。
          enum:
            - happyhorse-1.1-i2v
            - happyhorse-1.0-i2v
          example: happyhorse-1.1-i2v
        input:
          type: object
          required:
            - media
          description: 输入的基本信息，如提示词等。
          properties:
            prompt:
              type: string
              description: 文本提示词，用于描述期望生成的视频内容。可选 -- 不传时模型根据图像自行推断运动。支持任何语言输入，长度不超过5000个非中文字符或2500个中文字符，超过部分将自动截断。
              example: 一只猫在草地上奔跑
            media:
              type: array
              description: 输入媒体列表。有且仅有1张首帧图像。生成视频的宽高比自动跟随输入首帧图像。
              items:
                type: object
                required:
                  - type
                  - url
                properties:
                  type:
                    type: string
                    description: 媒体素材类型。固定值：`first_frame`（首帧）。
                    enum:
                      - first_frame
                  url:
                    type: string
                    format: uri
                    description: |-
                      首帧图像 URL 或 Base64 编码数据。

                      **图像限制**：格式：JPEG、JPG、PNG、WEBP。分辨率：宽和高不小于 300 像素。宽高比：1:2.5 ~ 2.5:1。文件大小：不超过 20 MB。

                      **支持的输入格式**：
                      - 公网 URL：支持 HTTP 或 HTTPS 协议。
                      - Base64 编码：格式为 `data:{MIME_type};base64,{base64_data}`。
        parameters:
          $ref: "#/components/schemas/HappyHorseImageToVideoParameters"
    HappyHorseImageToVideoParameters:
      type: object
      description: 视频处理参数。
      properties:
        resolution:
          type: string
          description: 指定生成视频的分辨率档位。模型根据选择的分辨率档位，自动缩放至相近总像素。输出的视频宽高比与输入首帧近似一致。
          enum:
            - 480P
            - 720P
            - 1080P
          default: 1080P
        duration:
          type: integer
          description: 指定生成视频的时长，单位为秒。取值为 [3, 15] 之间的整数。
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
    HappyHorseI2VTaskStatusResponse:
      type: object
      description: HappyHorse 图生视频任务状态响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识。联系技术支持时请提供此 ID。
          example: 8ae698ba-df2d-966c-abcf-xxxxxx
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID。提交后 24 小时内可查询。
              example: e56d806f-76f9-4037-aefa-xxxxxx
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
              description: 生成视频的 URL（MP4，H.264 编码，24fps）。仅在 `task_status` 为 `SUCCEEDED` 时返回。**链接有效期 24 小时**，请及时下载。
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
              description: 输入视频时长，单位秒。图生视频固定为 0。
            output_video_duration:
              type: integer
              description: 输出视频时长，单位秒。
            video_count:
              type: integer
              description: 输出视频数量。固定为 1。
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

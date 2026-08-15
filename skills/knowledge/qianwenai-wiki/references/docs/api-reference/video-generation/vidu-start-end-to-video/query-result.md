> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Vidu — 查询结果

> 查询 Vidu 首尾帧生视频任务的状态与结果。

提交任务后，请调用此接口轮询任务状态。任务提交请参考[生成视频](/api-reference/video-generation/vidu-start-end-to-video/create-task)。

## 轮询策略

1. 调用[生成视频](/api-reference/video-generation/vidu-start-end-to-video/create-task)接口，获取 `task_id`。
2. 每隔 **15 秒**轮询，直到 `task_status` 为 `SUCCEEDED` 或 `FAILED`。
3. 成功后，从 `output.video_url` 下载生成的视频。

## 注意事项

- **URL 有效期**：视频链接自任务完成后 **24 小时**内有效，请及时下载。
- **状态流转**：`PENDING`（排队中）→ `RUNNING`（处理中）→ `SUCCEEDED`（成功）或 `FAILED`（失败）。`CANCELED` 表示任务已取消。`UNKNOWN` 表示任务不存在或查询已超过 24 小时。

## 常见问题

**首帧和尾帧图像的顺序如何确定？**

`input.media` 数组中，第一个元素为首帧（起始帧），第二个元素为尾帧（结束帧）。请按此顺序传入，否则生成效果可能不符合预期。

**首帧和尾帧的分辨率有何限制？**

首帧和尾帧的总像素数（宽×高）比值需在 0.8～1.25 之间。比值过大或过小都会导致任务失败。

## OpenAPI

````yaml get /tasks/{task_id}
openapi: 3.1.0
info:
  title: Vidu 首尾帧生视频 API
  description: 基于首帧图像和尾帧图像生成平滑过渡视频。采用异步任务模式：提交任务后轮询获取结果。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 千问AI平台
security:
  - BearerAuth: []
paths:
  /tasks/{task_id}:
    get:
      operationId: getViduStartEndToVideoTaskStatus
      summary: 查询任务结果
      description: 查询 Vidu 首尾帧生视频任务的状态与结果。
      parameters:
        - name: task_id
          in: path
          required: true
          description: POST 接口返回的任务 ID。查询有效期为 24 小时。
          schema:
            type: string
      responses:
        "200":
          description: 查询成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/TaskStatusResponse"
              examples:
                SUCCEEDED:
                  summary: 任务执行成功
                  value:
                    request_id: cf7a3a1d-27b0-4d45-8b89-xxxxxx
                    output:
                      task_id: 88125b85-b53d-45f1-ba13-xxxxxx
                      task_status: SUCCEEDED
                      submit_time: 2026-03-27 14:39:15.041
                      scheduled_time: 2026-03-27 14:39:15.081
                      end_time: 2026-03-27 14:40:03.428
                      orig_prompt: 一只小猫从窗台向下跳跃，轻盈地落在沙发上，然后好奇地环顾四周。
                      video_url: https://prod-ss-vidu.s3.cn-northwest-1.amazonaws.com.cn/xxx.mp4?xxx
                    usage:
                      duration: 5
                      size: 828*624
                      output_video_duration: 5
                      fps: 24
                      video_count: 1
                      audio: false
                      SR: "540"
                FAILED:
                  summary: 任务执行失败
                  value:
                    request_id: e5d70b02-ebd3-98ce-9fe8-759d7d7b107d
                    output:
                      task_id: 86ecf553-d340-4e21-af6e-a0c6a421c010
                      task_status: FAILED
                      code: InvalidParameter
                      message: The size is not match xxxxxx
                RUNNING:
                  summary: 任务处理中
                  value:
                    request_id: 7574ee8f-38a3-4b1e-9280-xxxxxx
                    output:
                      task_id: a8532587-fa8c-4ef8-82be-xxxxxx
                      task_status: RUNNING
                UNKNOWN:
                  summary: 任务不存在或已过期
                  value:
                    request_id: a4de7c32-7057-9f82-8581-xxxxxx
                    output:
                      task_id: 502a00b1-19d9-4839-a82f-xxxxxx
                      task_status: UNKNOWN
        "400":
          description: 请求无效
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
      x-codeSamples:
        - lang: curl
          label: cURL
          source: |-
            curl -X GET 'https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY"
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    ViduStartEndToVideoRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: |-
            模型名称。

            | 模型 | 最高分辨率 | 最长时长 |
            |------|-----------|----------|
            | `vidu/viduq3-pro_start-end2video` | 1080P | 16 s |
            | `vidu/viduq3-turbo_start-end2video` | 1080P | 16 s |
            | `vidu/viduq2-pro_start-end2video` | 1080P | 10 s |
            | `vidu/viduq2-turbo_start-end2video` | 1080P | 10 s |
          enum:
            - vidu/viduq3-pro_start-end2video
            - vidu/viduq3-turbo_start-end2video
            - vidu/viduq2-pro_start-end2video
            - vidu/viduq2-turbo_start-end2video
          example: vidu/viduq3-turbo_start-end2video
        input:
          type: object
          required:
            - media
            - prompt
          description: 输入的基本信息，包含首帧、尾帧图像和提示词。
          properties:
            media:
              type: array
              description: |-
                媒体资源列表，包含首帧和尾帧图像。数组必须恰好包含两个图像对象：第一个为首帧，第二个为尾帧。

                **图像限制：**
                - 格式：JPG、PNG、WEBP。
                - 宽高比：1:4～4:1。
                - 文件大小：不超过 50 MB。
                - 分辨率：首帧和尾帧的总像素数（宽×高）比值需在 0.8～1.25 之间。
              minItems: 2
              maxItems: 2
              items:
                type: object
                required:
                  - type
                  - url
                properties:
                  type:
                    type: string
                    description: 媒体类型。固定值为 `image`。
                    enum:
                      - image
                    example: image
                  url:
                    type: string
                    description: 图像的公网可访问 URL。支持 HTTP 或 HTTPS 协议。
                    example: https://wanx.alicdn.com/material/20250318/first_frame.png
            prompt:
              type: string
              description: |-
                文本提示词，用来描述首帧到尾帧之间的变化过程。支持中英文，不超过 5000 个字符，超过部分会自动截断。

                提示词编写请参见Vidu视频生成Prompt指南。
              example: 一只小猫从窗台向下跳跃，轻盈地落在沙发上，然后好奇地环顾四周。
        parameters:
          $ref: "#/components/schemas/ViduStartEndToVideoParameters"
    ViduStartEndToVideoParameters:
      type: object
      description: 视频生成参数。
      properties:
        resolution:
          type: string
          description: 生成视频的分辨率。resolution 直接影响费用，请在调用前确认模型价格。可选值：`540P`、`720P`（默认）、`1080P`。
          enum:
            - 540P
            - 720P
            - 1080P
          default: 720P
          example: 720P
        duration:
          type: integer
          description: |-
            生成视频的时长，单位为秒。duration 直接影响费用，按秒计费。

            - `viduq3` 模型：取值为 [1, 16] 之间的整数，默认值为 5。
            - `viduq2` 模型：取值为 [1, 10] 之间的整数，默认值为 5。
          default: 5
          example: 5
        audio:
          type: boolean
          description: 是否生成有声视频。开启后模型将根据视频内容自动生成匹配的背景音乐或音效。仅 `viduq3` 模型支持。默认值为 `false`。
          default: false
          example: false
        watermark:
          type: boolean
          description: 是否添加水印标识。水印位于视频右下角，文案固定为"内容由 AI 生成"。默认值为 `false`。
          default: false
          example: false
        seed:
          type: integer
          description: 随机数种子，取值范围为 [0, 2147483647]。未指定时系统自动生成随机种子。固定 seed 值可提升生成结果的可复现性，但不能保证每次结果完全一致。
          minimum: 0
          maximum: 2147483647
          example: 12345
    AsyncTaskSubmitResponse:
      type: object
      description: 异步任务提交的响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识，可用于请求明细溯源和问题排查。
          example: 4909100c-7b5a-9f92-bfe5-xxxxxx
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID，用于轮询任务状态。查询有效期为 24 小时。请使用该值调用 `GET /tasks/{task_id}`。
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
              example: PENDING
    TaskStatusResponse:
      type: object
      description: 查询任务状态的响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识。
          example: cf7a3a1d-27b0-4d45-8b89-xxxxxx
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID。
              example: 88125b85-b53d-45f1-ba13-xxxxxx
            task_status:
              type: string
              description: 任务状态。状态流转：PENDING（排队中）→ RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。CANCELED 表示任务已取消。UNKNOWN 表示任务不存在或查询已过期（超过 24 小时）。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - CANCELED
                - UNKNOWN
            submit_time:
              type: string
              description: 任务提交时间。格式为 `YYYY-MM-DD HH:mm:ss.SSS`。仅在任务完成后返回。
              example: 2026-03-27 14:39:15.041
            scheduled_time:
              type: string
              description: 任务执行时间。格式为 `YYYY-MM-DD HH:mm:ss.SSS`。仅在任务完成后返回。
              example: 2026-03-27 14:39:15.081
            end_time:
              type: string
              description: 任务完成时间。格式为 `YYYY-MM-DD HH:mm:ss.SSS`。仅在任务完成后返回。
              example: 2026-03-27 14:40:03.428
            orig_prompt:
              type: string
              description: 原始输入的 prompt，对应请求参数 `prompt`。仅在任务成功时返回。
              example: 一只小猫从窗台向下跳跃，轻盈地落在沙发上，然后好奇地环顾四周。
            video_url:
              type: string
              description: 生成的视频 URL（MP4 格式，H.264 编码）。仅在 `task_status` 为 `SUCCEEDED` 时返回。视频链接有效期为 24 小时，请及时下载。
              example: https://prod-ss-vidu.s3.cn-northwest-1.amazonaws.com.cn/xxx.mp4?xxx
            code:
              type: string
              description: 错误码。仅在任务失败时返回。
            message:
              type: string
              description: 错误详细信息。仅在任务失败时返回。
        usage:
          type: object
          description: 输出信息统计。仅对成功的结果返回。
          properties:
            duration:
              type: integer
              description: 总的视频计费时长（秒）。
              example: 5
            size:
              type: string
              description: 输出视频的分辨率，格式为 `宽*高`。
              example: 828*624
            output_video_duration:
              type: integer
              description: 输出视频的实际时长（秒）。
              example: 5
            fps:
              type: integer
              description: 输出视频的帧率。
              example: 24
            audio:
              type: boolean
              description: 输出视频是否为有声视频。
              example: false
            SR:
              type: string
              description: 输出视频的分辨率档位（垂直方向像素数）。
              example: "540"
            video_count:
              type: integer
              description: 输出视频的数量。固定为 1。
              example: 1
    DashScopeErrorResponse:
      type: object
      description: DashScope API 错误响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识。
        code:
          type: string
          description: 错误码（如 `InvalidApiKey`、`InvalidParameter`、`Throttling`）。
          example: InvalidApiKey
        message:
          type: string
          description: 错误详细信息。
          example: No API-key provided.
````

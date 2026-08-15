> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Vidu — 创建任务

> 提交一个基于首帧图像的 Vidu 图生视频任务。

使用图像作为首帧生成视频。任务异步执行，提交后请调用[查询视频结果](/api-reference/video-generation/vidu-image-to-video/query-result)接口获取任务状态和视频 URL。

## 模型

| 模型                            | 最高分辨率 | 最长时长 |
| ----------------------------- | ----- | ---- |
| `vidu/viduq3-pro_img2video`   | 1080P | 16 秒 |
| `vidu/viduq3-turbo_img2video` | 1080P | 16 秒 |
| `vidu/viduq2-pro_img2video`   | 1080P | 10 秒 |
| `vidu/viduq2-turbo_img2video` | 1080P | 10 秒 |

## 图像要求

- 格式：JPG、PNG 或 WEBP
- 宽高比：1:4 到 4:1 之间
- 文件大小：最大 50 MB

## 轮询

提交任务后，每隔 15 秒轮询[查询视频结果](/api-reference/video-generation/vidu-image-to-video/query-result)接口，直到 `task_status` 变为 `SUCCEEDED` 或 `FAILED`。生成的视频 URL 自任务完成起 24 小时内有效，请及时下载。

## OpenAPI

````yaml post /services/aigc/video-generation/video-synthesis
openapi: 3.1.0
info:
  title: Vidu 图生视频 API
  description: 使用 Vidu 模型从图像生成视频（基于首帧）。采用异步任务提交模式——提交任务后轮询结果。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 千问AI平台
security:
  - BearerAuth: []
paths:
  /services/aigc/video-generation/video-synthesis:
    post:
      operationId: createViduImageToVideoTask
      summary: 创建图生视频任务
      description: 提交一个图生视频任务。输入图像将作为生成视频的首帧。
      parameters:
        - name: X-DashScope-Async
          in: header
          required: true
          description: 必须设置为 `enable`。此 API 仅支持异步处理。
          schema:
            type: string
            enum:
              - enable
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/ViduImageToVideoRequest"
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
          label: cURL
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
                -H 'X-DashScope-Async: enable' \
                -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
                -H 'Content-Type: application/json' \
                -d '{
                "model": "vidu/viduq3-pro_img2video",
                "input": {
                    "media": [
                        {
                            "type": "image",
                            "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260121/zlpocv/wan-i2v-haigui.webp"
                        }
                    ],
                    "prompt": "镜头从海龟下方缓缓上移，海龟悠然游动，腹部细节清晰可见。"
                },
                "parameters": {
                    "duration": 5,
                    "resolution": "720P",
                    "watermark": true
                }
            }'
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    ViduImageToVideoRequest:
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
            |-------|---------------|-------------|
            | `vidu/viduq3-pro_img2video` | 1080P | 16 秒 |
            | `vidu/viduq3-turbo_img2video` | 1080P | 16 秒 |
            | `vidu/viduq2-pro_img2video` | 1080P | 10 秒 |
            | `vidu/viduq2-turbo_img2video` | 1080P | 10 秒 |
          enum:
            - vidu/viduq3-pro_img2video
            - vidu/viduq3-turbo_img2video
            - vidu/viduq2-pro_img2video
            - vidu/viduq2-turbo_img2video
          example: vidu/viduq3-pro_img2video
        input:
          type: object
          required:
            - media
          description: 图生视频的输入数据。
          properties:
            media:
              type: array
              description: |-
                包含一个图像对象的数组。该图像将作为生成视频的首帧。

                **图像约束：**
                - 格式：JPG、PNG 或 WEBP。
                - 宽高比：1:4 到 4:1 之间。
                - 文件大小：最大 50 MB。
              minItems: 1
              maxItems: 1
              items:
                type: object
                required:
                  - type
                  - url
                properties:
                  type:
                    type: string
                    description: 媒体类型，必须为 `image`。
                    enum:
                      - image
                    example: image
                  url:
                    type: string
                    description: 可公开访问的图像 URL。
                    example: https://example.com/portrait.jpg
            prompt:
              type: string
              description: 可选的文本描述，用于引导生成视频的动作或内容。最多 5000 个字符。
              example: 镜头从海龟下方缓缓上移，海龟悠然游动，腹部细节清晰可见。
        parameters:
          $ref: "#/components/schemas/ViduImageToVideoParameters"
    ViduImageToVideoParameters:
      type: object
      description: 视频生成参数。
      properties:
        resolution:
          type: string
          description: |-
            输出视频分辨率。

            - `viduq3` 模型：`540P`、`720P`（默认）、`1080P`。
            - `viduq2` 模型：`720P`（默认）、`1080P`。
          enum:
            - 540P
            - 720P
            - 1080P
          default: 720P
          example: 720P
        duration:
          type: integer
          description: |-
            输出视频时长（秒）。

            - `viduq3` 模型：1–16 秒，默认 5 秒。
            - `viduq2` 模型：1–10 秒，默认 5 秒。
          default: 5
          example: 5
        audio:
          type: boolean
          description: 是否生成音频。仅 `viduq3` 模型支持，默认为 `false`。
          default: false
          example: false
        watermark:
          type: boolean
          description: 是否在输出视频中添加水印（视频右下角显示"内容由AI生成"）。默认为 `false`。
          default: false
          example: false
        seed:
          type: integer
          description: 用于可复现生成的随机种子。范围：0–2147483647。
          minimum: 0
          maximum: 2147483647
          example: 42
    AsyncTaskSubmitResponse:
      type: object
      description: 异步任务提交的响应。
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
              description: 用于轮询状态的任务 ID。配合 `GET /tasks/{task_id}` 使用。
              example: 0385dc79-5ff8-4d82-bcb6-xxxxxx
            task_status:
              type: string
              description: 初始任务状态，通常为 `PENDING`。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - UNKNOWN
              example: PENDING
    TaskStatusResponse:
      type: object
      description: 轮询任务状态的响应。
      properties:
        request_id:
          type: string
          description: 唯一请求标识符。
          example: 3606f9f4-b833-44ec-8385-xxxxxx
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID。
              example: 2846881f-0496-4288-947f-xxxxxx
            task_status:
              type: string
              description: 当前任务状态。状态转换：PENDING → RUNNING → SUCCEEDED 或 FAILED。UNKNOWN 表示任务不存在或已过期。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - UNKNOWN
            submit_time:
              type: string
              description: 任务提交时间（格式：`YYYY-MM-DD HH:mm:ss.SSS`）。仅在任务完成后返回。
              example: 2026-03-27 14:25:32.057
            scheduled_time:
              type: string
              description: 任务开始执行时间（格式：`YYYY-MM-DD HH:mm:ss.SSS`）。仅在任务完成后返回。
              example: 2026-03-27 14:25:32.084
            end_time:
              type: string
              description: 任务完成时间（格式：`YYYY-MM-DD HH:mm:ss.SSS`）。仅在任务完成后返回。
              example: 2026-03-27 14:28:29.600
            orig_prompt:
              type: string
              description: 生成时使用的原始提示词。仅在任务成功时返回。
              example: 镜头从海龟下方缓缓上移，海龟悠然游动，腹部细节清晰可见。
            video_url:
              type: string
              description: 生成视频的 URL（MP4 格式）。任务完成后 24 小时内有效，请及时下载。
              example: https://prod-ss-vidu.s3.cn-northwest-1.amazonaws.com.cn/xxx.mp4?xxxx
            code:
              type: string
              description: 错误码。仅在任务失败时返回。
            message:
              type: string
              description: 详细错误信息。仅在任务失败时返回。
        usage:
          type: object
          description: 输出统计信息。仅在任务成功时返回。
          properties:
            duration:
              type: integer
              description: 计费视频时长（秒）。
              example: 5
            size:
              type: string
              description: 输出视频分辨率，格式为 `宽*高`。
              example: 988*932
            output_video_duration:
              type: integer
              description: 实际生成视频的时长（秒）。
              example: 5
            fps:
              type: integer
              description: 生成视频的帧率。
              example: 24
            audio:
              type: boolean
              description: 生成的视频是否包含音频。
              example: false
            SR:
              type: string
              description: 生成视频的垂直分辨率。
              example: "720"
            video_count:
              type: integer
              description: 生成的视频数量。
              example: 1
    DashScopeErrorResponse:
      type: object
      description: DashScope API 错误响应。
      properties:
        request_id:
          type: string
          description: 唯一请求标识符。
        code:
          type: string
          description: 错误码（如 `InvalidApiKey`、`InvalidParameter`、`Throttling`）。
          example: InvalidApiKey
        message:
          type: string
          description: 人类可读的错误信息。
          example: No API-key provided.
````

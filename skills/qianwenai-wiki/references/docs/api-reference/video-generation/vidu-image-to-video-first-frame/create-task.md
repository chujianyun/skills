> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Vidu — 创建任务

> 基于首帧图片提交 Vidu 图生视频异步任务

<Note>
  请先[获取 API Key](/api-reference/preparation/api-key) 并[配置为环境变量](/api-reference/preparation/export-api-key-env)。
</Note>

## 模型概览

| 模型名                           | 说明                      |
| ----------------------------- | ----------------------- |
| `vidu/viduq3-pro_img2video`   | q3 旗舰版，最高 1080P，最长 16 秒 |
| `vidu/viduq3-turbo_img2video` | q3 快速版，最高 1080P，最长 16 秒 |
| `vidu/viduq2-pro_img2video`   | q2 旗舰版，最高 1080P，最长 10 秒 |
| `vidu/viduq2-turbo_img2video` | q2 快速版，最高 1080P，最长 10 秒 |

## 输入限制

**首帧图像要求**

| 限制项    | 要求                 |
| ------ | ------------------ |
| 格式     | JPG、PNG、WEBP       |
| 宽高比    | 1:4 到 4:1          |
| 文件大小   | 不超过 50 MB          |
| URL 类型 | HTTP/HTTPS 公网可访问地址 |
| 数量     | 必须且仅能传入 1 张图片      |

**分辨率与时长**

| 模型                            | 支持分辨率           | 支持时长   |
| ----------------------------- | --------------- | ------ |
| `vidu/viduq3-pro_img2video`   | 540P、720P、1080P | 1–16 秒 |
| `vidu/viduq3-turbo_img2video` | 540P、720P、1080P | 1–16 秒 |
| `vidu/viduq2-pro_img2video`   | 720P、1080P      | 1–10 秒 |
| `vidu/viduq2-turbo_img2video` | 720P、1080P      | 1–10 秒 |

## 背景音效

`parameters.audio` 参数仅 **q3 模型**（viduq3-pro、viduq3-turbo）支持。设为 `true` 后，模型将根据视频内容自动生成 AI 背景音效。

## 使用流程

1. 调用本接口提交图生视频任务，获取 `task_id`。
2. 调用[查询图生视频任务结果（基于首帧）](/api-reference/video-generation/vidu-image-to-video-first-frame/query-result)接口，使用 `task_id` 轮询任务状态，直到获取生成的视频 URL。

## 错误码

大模型服务通用状态码请查阅[错误信息](/api-reference/preparation/error-messages)。

## OpenAPI

````yaml post /api/v1/services/aigc/video-generation/video-synthesis
openapi: 3.1.0
info:
  title: Vidu 图生视频（基于首帧）API
  version: 1.0.0
  description: 基于首帧图片，使用 Vidu 模型生成视频。
servers:
  - url: https://dashscope.aliyuncs.com
    description: 千问AI平台
security:
  - BearerAuth: []
paths:
  /api/v1/services/aigc/video-generation/video-synthesis:
    post:
      summary: 提交图生视频任务（基于首帧）
      description: 提交 Vidu 图生视频（基于首帧）异步任务。任务提交后返回 `task_id`，通过查询接口轮询任务状态直至获取生成的视频。
      operationId: createViduI2VFirstFrameTask
      parameters:
        - name: X-DashScope-Async
          in: header
          required: true
          schema:
            type: string
            enum:
              - enable
          description: 固定值 `enable`，启用异步模式。
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/ViduI2VFirstFrameRequest"
      responses:
        "200":
          description: 任务提交成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ViduSubmitResponse"
              example:
                output:
                  task_status: PENDING
                  task_id: 0385dc79-5ff8-4d82-bcb6-xxxxxx
                request_id: 4909100c-7b5a-9f92-bfe5-xxxxxx
        "400":
          description: 请求参数错误
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
              example:
                code: InvalidParameter
                message: The request parameter is invalid.
                request_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        "401":
          description: 认证失败
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
              example:
                code: InvalidApiKey
                message: No API-key provided.
                request_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        "429":
          description: 请求频率超限
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
              example:
                code: Throttling
                message: Requests throttling triggered.
                request_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
      x-codeSamples:
        - lang: curl
          label: cURL
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
                "model": "vidu/viduq3-pro-fast_img2video",
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
  schemas:
    ViduI2VFirstFrameRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          enum:
            - vidu/viduq3-pro_img2video
            - vidu/viduq3-pro-fast_img2video
            - vidu/viduq3-turbo_img2video
            - vidu/viduq2-pro_img2video
            - vidu/viduq2-turbo_img2video
          description: |-
            模型名称。可选值：
            - `vidu/viduq3-pro_img2video`：q3 旗舰版，最高 1080P，最长 16 秒
            - `vidu/viduq3-pro-fast_img2video`：q3 旗舰极速版，最高 1080P，最长 16 秒
            - `vidu/viduq3-turbo_img2video`：q3 快速版，最高 1080P，最长 16 秒
            - `vidu/viduq2-pro_img2video`：q2 旗舰版，最高 1080P，最长 10 秒
            - `vidu/viduq2-turbo_img2video`：q2 快速版，最高 1080P，最长 10 秒
        input:
          type: object
          required:
            - media
          properties:
            media:
              type: array
              description: 输入图片列表，必须包含且仅包含 **1** 张图片，作为视频的首帧。
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
                    enum:
                      - image
                    description: 媒体类型，固定为 `image`。
                  url:
                    type: string
                    description: |-
                      图片的公网 URL。

                      **图片要求**：
                      - **格式**：JPG、PNG、WEBP
                      - **宽高比**：1:4 到 4:1（即宽/高在 0.25 到 4 之间）
                      - **文件大小**：不超过 50 MB
                      - **URL 类型**：HTTP/HTTPS 公网可访问地址
            prompt:
              type: string
              description: |-
                视频内容的文字描述，引导模型生成特定风格或动作的视频。

                提示词编写请参见Vidu视频生成Prompt指南。
        parameters:
          type: object
          properties:
            duration:
              type: integer
              description: |-
                生成视频的时长（秒）。

                - **q3 模型**（viduq3-pro、viduq3-turbo）：1–16 秒
                - **q2 模型**（viduq2-pro、viduq2-turbo）：1–10 秒

                各模型取值范围：
                - `vidu/viduq3-pro-fast_img2video`：取值为[1, 16]之间的整数，默认值为5
            resolution:
              type: string
              enum:
                - 540P
                - 720P
                - 1080P
              description: |-
                生成视频的分辨率。

                - **q3 模型**：支持 540P、720P、1080P
                - **q2 模型**：支持 720P、1080P

                各模型默认值：
                - `vidu/viduq3-pro-fast_img2video`：可选值：720P、1080P。默认值为 720P
            watermark:
              type: boolean
              default: true
              description: 是否在视频中添加水印。默认为 `true`。
            audio:
              type: boolean
              default: false
              description: 是否为生成的视频添加 AI 背景音效。默认为 `false`。**仅 q3 模型支持**（viduq3-pro、viduq3-pro-fast、viduq3-turbo）。
    ViduSubmitResponse:
      type: object
      properties:
        request_id:
          type: string
          description: 本次请求的唯一 ID。
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 异步任务 ID，用于查询任务状态。
            task_status:
              type: string
              enum:
                - PENDING
              description: 任务初始状态，值为 `PENDING`。
    ViduQueryResponse:
      type: object
      properties:
        request_id:
          type: string
          description: 本次请求的唯一 ID。
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 异步任务 ID。
            task_status:
              type: string
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - CANCELED
                - UNKNOWN
              description: 任务状态。`PENDING`：排队中；`RUNNING`：处理中；`SUCCEEDED`：成功；`FAILED`：失败；`CANCELED`：已取消；`UNKNOWN`：任务不存在或已过期（超过 24 小时）。
            submit_time:
              type: string
              description: 任务提交时间。
            scheduled_time:
              type: string
              description: 任务开始调度时间。
            end_time:
              type: string
              description: 任务结束时间（成功或失败时返回）。
            orig_prompt:
              type: string
              description: 原始提示词（任务成功时返回）。
            video_url:
              type: string
              description: 生成视频的 URL，有效期 24 小时，请及时下载保存。视频格式为 MP4，编码为 H.264。
            code:
              type: string
              description: 任务失败时的错误码。
            message:
              type: string
              description: 任务失败时的错误信息。
        usage:
          type: object
          description: 任务成功时返回的用量信息。
          properties:
            duration:
              type: integer
              description: 请求的视频时长（秒）。
            output_video_duration:
              type: integer
              description: 实际生成的视频时长（秒）。
            size:
              type: string
              description: 生成视频的分辨率，格式为 `宽*高`，例如 `988*932`。
            fps:
              type: integer
              description: 生成视频的帧率。
            video_count:
              type: integer
              description: 生成的视频数量。
            audio:
              type: boolean
              description: 生成的视频是否包含音频。
            SR:
              type: string
              description: 分辨率档位，例如 `720`（720P）。
    DashScopeErrorResponse:
      type: object
      properties:
        code:
          type: string
          description: 错误码。
        message:
          type: string
          description: 错误信息。
        request_id:
          type: string
          description: 请求唯一标识。
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
````

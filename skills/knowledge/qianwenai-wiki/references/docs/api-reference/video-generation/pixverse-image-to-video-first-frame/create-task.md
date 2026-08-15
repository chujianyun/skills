> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 爱诗 PixVerse — 创建任务

> 基于首帧图片提交爱诗 PixVerse 图生视频异步任务

<Note>
  请先[获取 API Key](/api-reference/preparation/api-key) 并[配置为环境变量](/api-reference/preparation/export-api-key-env)。
</Note>

## 模型概览

| 模型名                         | 说明                                             |
| --------------------------- | ---------------------------------------------- |
| pixverse/pixverse-c1-it2v   | 旗舰动作与特效模型，适合动态镜头、打光等复杂运动场景；首帧模式支持通过提示词格式指定镜头类型 |
| pixverse/pixverse-v6-it2v   | 通用高质量模型，适合人像、风景等多种主题；通过 `shot_type` 参数开启多镜头模式  |
| pixverse/pixverse-v5.6-it2v | 旧版模型，最大分辨率 720P，支持时长 5、8、10 秒                  |

## 输入限制

**首帧图像要求**

| 限制项    | 要求                 |
| ------ | ------------------ |
| 格式     | JPG、PNG、WEBP       |
| 最长边    | 不超过 10000 像素       |
| 文件大小   | 不超过 20 MB          |
| URL 类型 | HTTP/HTTPS 公网可访问地址 |

**分辨率与时长**

| 模型                          | 支持分辨率                | 支持时长     |
| --------------------------- | -------------------- | -------- |
| pixverse/pixverse-c1-it2v   | 360P、540P、720P、1080P | 1–15 秒   |
| pixverse/pixverse-v6-it2v   | 360P、540P、720P、1080P | 1–15 秒   |
| pixverse/pixverse-v5.6-it2v | 360P、540P、720P       | 5、8、10 秒 |

## 多镜头模式

**c1 模型**：在 `input.prompt` 中以 `[shot_type]` 格式指定镜头类型（如 `[close-up] 人物特写`），模型会根据提示词内容自动生成对应镜头运动。

**v6 模型**：将 `parameters.shot_type` 设为 `multi`，模型将自动生成多镜头组合视频；设为 `single`（默认）则输出单一连续镜头。

## 使用流程

1. 调用本接口提交图生视频任务，获取 `task_id`。
2. 调用[查询图生视频任务结果（基于首帧）](/api-reference/video-generation/pixverse-image-to-video-first-frame/query-result)接口，使用 `task_id` 轮询任务状态，直到获取生成的视频 URL。

## 错误码

大模型服务通用状态码请查阅[错误码](/api-reference/preparation/error-messages)。

## OpenAPI

````yaml post /services/aigc/video-generation/video-synthesis
openapi: 3.1.0
info:
  title: 爱诗 PixVerse 图生视频（基于首帧）API
  version: 1.0.0
  description: 基于首帧图片生成视频。提交异步任务后，通过 `GET /tasks/{task_id}` 轮询结果。
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
security:
  - BearerAuth: []
paths:
  /services/aigc/video-generation/video-synthesis:
    post:
      operationId: createPixVerseI2VFirstFrameTask
      summary: 提交图生视频任务
      description: 提交爱诗 PixVerse 图生视频（基于首帧）异步任务。返回 `task_id`，通过查询接口轮询获取结果。
      parameters:
        - name: X-DashScope-Async
          in: header
          required: true
          description: 固定值 `enable`，启用异步模式。
          schema:
            type: string
            enum:
              - enable
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/PixVerseI2VFirstFrameRequest"
      responses:
        "200":
          description: 任务提交成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/PixVerseI2VSubmitResponse"
              example:
                request_id: 4909100c-7b5a-9f92-bfe5-xxxxxx
                output:
                  task_id: 0385dc79-5ff8-4d82-bcb6-xxxxxx
                  task_status: PENDING
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
          label: cURL - 基础用法（c1 模型）
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
              --header 'X-DashScope-Async: enable' \
              --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
              --header 'Content-Type: application/json' \
              --data '{
                "model": "pixverse/pixverse-c1-it2v",
                "input": {
                  "media": [
                    {
                      "type": "image_url",
                      "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260121/zlpocv/wan-i2v-haigui.webp"
                    }
                  ],
                  "prompt": "镜头从海龟下方缓缓上移，海龟悠然游动，腹部细节清晰可见。"
                },
                "parameters": {
                  "resolution": "720P",
                  "duration": 5,
                  "audio": false,
                  "watermark": false
                }
              }'
        - lang: curl
          label: cURL - 多镜头（c1 模型，提示词描述）
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
              --header 'X-DashScope-Async: enable' \
              --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
              --header 'Content-Type: application/json' \
              --data '{
                "model": "pixverse/pixverse-c1-it2v",
                "input": {
                  "media": [
                    {
                      "type": "image_url",
                      "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260121/zlpocv/wan-i2v-haigui.webp"
                    }
                  ],
                  "prompt": "镜头1：从海龟下方缓缓上移，海龟悠然游动，腹部细节清晰可见。镜头2：远景，海龟旁边围绕着海草，海草也在左右摇摆"
                },
                "parameters": {
                  "resolution": "720P",
                  "duration": 8,
                  "audio": false,
                  "watermark": false
                }
              }'
        - lang: curl
          label: cURL - 多镜头（v6 模型，shot_type 参数）
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
              --header 'X-DashScope-Async: enable' \
              --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
              --header 'Content-Type: application/json' \
              --data '{
                "model": "pixverse/pixverse-v6-it2v",
                "input": {
                  "media": [
                    {
                      "type": "image_url",
                      "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260121/zlpocv/wan-i2v-haigui.webp"
                    }
                  ],
                  "prompt": "镜头1：从海龟下方缓缓上移，海龟悠然游动，腹部细节清晰可见。镜头2：远景，海龟旁边围绕着海草，海草也在左右摇摆"
                },
                "parameters": {
                  "resolution": "720P",
                  "duration": 8,
                  "shot_type": "multi",
                  "audio": false,
                  "watermark": false
                }
              }'
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    PixVerseI2VFirstFrameRequest:
      type: object
      required:
        - model
        - input
        - parameters
      properties:
        model:
          type: string
          description: |-
            模型名称。

            - `pixverse/pixverse-c1-it2v`：擅长动作、特效和高速运动场景。
            - `pixverse/pixverse-v6-it2v`：通用图生视频模型。
            - `pixverse/pixverse-v5.6-it2v`：旧版模型，建议升级至 v6。
          enum:
            - pixverse/pixverse-c1-it2v
            - pixverse/pixverse-v6-it2v
            - pixverse/pixverse-v5.6-it2v
          example: pixverse/pixverse-c1-it2v
        input:
          type: object
          required:
            - media
          description: 视频生成的输入内容。
          properties:
            prompt:
              type: string
              description: 视频内容描述，支持中英文。c1/v6 模型最长 5000 字符，v5.6 模型最长 2048 字符（超出自动截断）。
              example: 镜头从海龟下方缓缓上移，海龟悠然游动，腹部细节清晰可见。
            media:
              type: array
              description: 首帧参考图片，仅支持传入 1 个元素，`type` 固定为 `image_url`。
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
                    description: 媒体类型，固定为 `image_url`。
                    enum:
                      - image_url
                  url:
                    type: string
                    format: uri
                    description: 图片公网 URL（HTTP/HTTPS）。支持 JPG、PNG、WEBP 格式，每边最大 10000 像素，文件大小不超过 20 MB。
        parameters:
          $ref: "#/components/schemas/PixVerseI2VFirstFrameParameters"
    PixVerseI2VFirstFrameParameters:
      type: object
      required:
        - resolution
        - duration
      description: 视频生成参数。
      properties:
        resolution:
          type: string
          description: 生成视频的分辨率档位。模型自动按首帧图片比例缩放输出尺寸，分辨率越高消耗的资源越多。
          enum:
            - 360P
            - 540P
            - 720P
            - 1080P
        duration:
          type: integer
          description: 视频时长（秒）。c1/v6 模型支持 1–15 秒；v5.6 模型支持 5、8、10 秒。视频越长消耗资源越多，按秒计费。
          minimum: 1
          maximum: 15
        audio:
          type: boolean
          description: 是否为视频自动生成背景音效。
          default: false
        shot_type:
          type: string
          description: 镜头模式。`single`：单镜头连续画面；`multi`：多镜头，视频中存在场景切换，需配合多镜头提示词（如`镜头1：…镜头2：…`）使用。**仅 v6 模型支持**；c1 模型通过提示词格式实现多镜头，无需设置该参数。
          enum:
            - single
            - multi
          default: single
        watermark:
          type: boolean
          description: 是否在视频右下角添加「AI生成」水印。
          default: false
        seed:
          type: integer
          description: 随机种子，用于复现相近结果。相同种子和参数可生成相似（非完全相同）的输出。取值范围 0–2147483647。
          minimum: 0
          maximum: 2147483647
    PixVerseI2VSubmitResponse:
      type: object
      description: 异步任务提交响应。
      properties:
        request_id:
          type: string
          description: 本次请求的唯一 ID，用于排查问题。
          example: 4909100c-7b5a-9f92-bfe5-xxxxxx
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 异步任务 ID，用于查询任务状态。
              example: 0385dc79-5ff8-4d82-bcb6-xxxxxx
            task_status:
              type: string
              description: 任务初始状态，值为 `PENDING`。
              enum:
                - PENDING
    PixVerseI2VQueryResponse:
      type: object
      description: 任务查询响应。
      properties:
        request_id:
          type: string
          description: 本次请求的唯一 ID。
          example: 7df19cf7-d76c-4bb8-b4c5-xxxxxx
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 异步任务 ID。
              example: 5abf2c85-ea81-4cbf-8918-xxxxxx
            task_status:
              type: string
              description: 任务状态。`PENDING`：排队中；`RUNNING`：处理中；`SUCCEEDED`：成功；`FAILED`：失败；`CANCELED`：已取消；`UNKNOWN`：任务不存在或已过期（24 小时后）。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - CANCELED
                - UNKNOWN
            submit_time:
              type: string
              description: 任务提交时间（UTC+8，格式 `YYYY-MM-DD HH:mm:ss.SSS`）。
              example: 2026-03-20 11:48:50.499
            scheduled_time:
              type: string
              description: 任务开始执行时间（UTC+8，格式 `YYYY-MM-DD HH:mm:ss.SSS`）。
              example: 2026-03-20 11:48:50.551
            end_time:
              type: string
              description: 任务结束时间（UTC+8，格式 `YYYY-MM-DD HH:mm:ss.SSS`）。仅在任务 `SUCCEEDED` 或 `FAILED` 时返回。
              example: 2026-03-20 11:49:46.462
            orig_prompt:
              type: string
              description: 实际使用的提示词，对应请求中的 `input.prompt`。
            video_url:
              type: string
              format: uri
              description: 生成视频的 URL（MP4 格式，H.264 编码）。仅在任务 `SUCCEEDED` 时返回。请及时下载保存。
              example: https://media.pixverseai.cn/xxxx.mp4
            code:
              type: string
              description: 错误码，仅在任务 `FAILED` 时返回。
            message:
              type: string
              description: 错误信息，仅在任务 `FAILED` 时返回。
        usage:
          type: object
          description: 资源消耗信息，仅在任务 `SUCCEEDED` 时返回。
          properties:
            duration:
              type: integer
              description: 生成视频的时长（秒），为计费依据。
            shot_type:
              type: string
              description: 实际使用的镜头模式（`single` 或 `multi`）。
            size:
              type: string
              description: 输出视频的分辨率，例如 `992*944`。
              example: 992*944
            fps:
              type: integer
              description: 输出视频的帧率。
              example: 24
            video_count:
              type: integer
              description: 生成的视频数量，固定为 `1`。
            audio:
              type: boolean
              description: 是否生成了音效。
            SR:
              type: string
              description: 实际使用的分辨率档位，例如 `720` 表示 720P。
              example: "720"
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
````

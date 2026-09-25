> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 灵动人像 LivePortrait — 创建任务

> 提交灵动人像 LivePortrait 播报视频生成异步任务

<Note>
  请先[获取 API Key](/api-reference/preparation/api-key) 并[配置为环境变量](/api-reference/preparation/export-api-key-env)。
</Note>

## 模型概览

**模型简介**

| 模型名          | 模型简介                                                             |
| ------------ | ---------------------------------------------------------------- |
| liveportrait | 灵动人像 LivePortrait，基于人物肖像图片和语音音频，生成口型与音频同步的播报视频。适用于数字人播报、虚拟主播等场景。 |

## 前置条件

在调用本接口前，建议先调用 [LivePortrait 图像检测](/api-reference/video-generation/liveportrait-video/liveportrait-detect) 接口对人物图片进行检测，确认图片符合模型输入规范。

## 头部运动模板

| 模板名    | 说明                   |
| ------ | -------------------- |
| normal | 默认，中等幅度头部运动，适用于多种场景。 |
| calm   | 平静，小幅度头部运动，推荐用于播报场景。 |
| active | 活跃，大幅度头部运动，推荐用于演唱场景。 |

## 使用流程

1. 调用 [LivePortrait 图像检测](/api-reference/video-generation/liveportrait-video/liveportrait-detect) 接口，传入人物图片，确认通过检测。
2. 调用本接口，将图片 URL、音频 URL 及可选参数一并提交，获取 `task_id`。
3. 调用[查询视频生成结果](/api-reference/video-generation/liveportrait-video/query-result)接口，使用 `task_id` 轮询任务状态，直到获取生成的视频 URL。

## 错误码

大模型服务通用状态码请查阅[错误信息](/api-reference/preparation/error-messages)。

## OpenAPI

````yaml post /services/aigc/image2video/video-synthesis/
openapi: 3.1.0
info:
  title: 灵动人像 LivePortrait 视频生成 API
  version: 1.0.0
  description: 基于人物肖像图片和语音音频，生成口型与音频同步的播报视频。
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 千问AI平台
security:
  - BearerAuth: []
paths:
  /services/aigc/image2video/video-synthesis/:
    post:
      summary: 提交视频生成任务
      operationId: createLivePortraitVideoTask
      description: 提交灵动人像 LivePortrait 视频生成异步任务。需要先调用 [LivePortrait 图像检测](/api-reference/video-generation/liveportrait-detect) 接口确认输入图片符合规范。
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
              $ref: "#/components/schemas/LivePortraitVideoRequest"
      responses:
        "200":
          description: 任务提交成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/LivePortraitVideoSubmitResponse"
              example:
                output:
                  task_id: a8532587-fa8c-4ef8-82be-0c46b17950d1
                  task_status: PENDING
                request_id: 7574ee8f-38a3-4b1e-9280-11c33ab46e51
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
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis/' \
              --header 'X-DashScope-Async: enable' \
              --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
              --header 'Content-Type: application/json' \
              --data '{
                "model": "liveportrait",
                "input": {
                  "image_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250911/ynhjrg/p874909.png",
                  "audio_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251226/fwnqyq/liveportrait_boy.mp3"
                },
                "parameters": {
                  "template_id": "normal",
                  "eye_move_freq": 0.5,
                  "video_fps": 30,
                  "mouth_move_strength": 1,
                  "paste_back": true,
                  "head_move_strength": 0.7
                }
              }'
components:
  schemas:
    LivePortraitVideoRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          enum:
            - liveportrait
          description: 模型名称，固定为 `liveportrait`。
        input:
          type: object
          required:
            - image_url
            - audio_url
          properties:
            image_url:
              type: string
              description: |-
                人物肖像图片公网 URL。建议先通过 [LivePortrait 图像检测](/api-reference/video-generation/liveportrait-detect) 接口验证图片是否符合规范。

                **图片要求**：
                - **格式**：jpeg、jpg、png、bmp、webp
                - **文件大小**：小于 10 MB
                - **宽高比**：不超过 2
                - **最大边长**：不超过 4096 像素
                - **URL**：HTTP/HTTPS 公网可访问地址
            audio_url:
              type: string
              description: |-
                驱动视频的语音音频公网 URL。

                **音频要求**：
                - **格式**：wav、mp3
                - **文件大小**：小于 15 MB
                - **时长**：1 秒到 3 分钟之间
                - **内容**：必须包含清晰的人声
                - **URL**：HTTP/HTTPS 公网可访问地址
        parameters:
          type: object
          properties:
            template_id:
              type: string
              enum:
                - normal
                - calm
                - active
              default: normal
              description: 头部运动模板，控制头部运动风格。`normal`：默认，中等幅度头部运动，适用于多种场景；`calm`：平静，小幅度头部运动，推荐用于播报场景；`active`：活跃，大幅度头部运动，推荐用于演唱场景。默认为 `normal`。
            eye_move_freq:
              type: number
              minimum: 0
              maximum: 1
              default: 0.5
              description: 眨眼频率，取值范围 0～1。值越大眨眼次数越多。默认为 `0.5`。
            video_fps:
              type: integer
              minimum: 15
              maximum: 30
              default: 24
              description: 生成视频的帧率，取值范围 15～30（整数）。默认为 `24`。
            mouth_move_strength:
              type: number
              minimum: 0
              maximum: 1.5
              default: 1
              description: 嘴部运动幅度，取值范围 0～1.5。`0` 表示嘴部不动。默认为 `1`。
            paste_back:
              type: boolean
              default: true
              description: 是否将面部粘贴回原始图像身体上。`true`：输出完整人物图像；`false`：仅输出面部区域。默认为 `true`。
            head_move_strength:
              type: number
              minimum: 0
              maximum: 1
              default: 0.7
              description: 头部运动幅度，取值范围 0～1。默认为 `0.7`。
    LivePortraitVideoSubmitResponse:
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
    LivePortraitVideoQueryResponse:
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
                - UNKNOWN
              description: 任务状态。`PENDING`：排队等待；`RUNNING`：处理中；`SUCCEEDED`：成功；`FAILED`：失败；`UNKNOWN`：任务不存在或已过期。
            submit_time:
              type: string
              description: 任务提交时间。
            scheduled_time:
              type: string
              description: 任务开始调度时间。
            end_time:
              type: string
              description: 任务结束时间（成功或失败时返回）。
            results:
              type: object
              description: 任务成功时返回。
              properties:
                video_url:
                  type: string
                  description: 生成视频的 URL，有效期 24 小时，请及时下载保存。
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
            video_duration:
              type: number
              description: 生成视频的时长，单位为秒。
            video_ratio:
              type: string
              description: 生成视频的规格，值为 `standard`。
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

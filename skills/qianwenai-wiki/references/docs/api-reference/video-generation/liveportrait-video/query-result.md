> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 灵动人像 LivePortrait — 查询视频生成结果

> 查询灵动人像 LivePortrait 视频生成任务状态，获取生成的视频

<Note>
  请先[获取 API Key](/api-reference/preparation/api-key) 并[配置为环境变量](/api-reference/preparation/export-api-key-env)。
</Note>

## 轮询策略

1. 调用[提交视频生成任务](/api-reference/video-generation/liveportrait-video/create-task)接口获取 `task_id`。
2. 每 **15 秒**轮询一次，直到 `task_status` 为 `SUCCEEDED` 或 `FAILED`。
3. 任务成功后，从 `output.results.video_url` 获取视频。

## 注意事项

- **URL 有效期**：视频 URL 在 **24 小时**后过期，请及时下载保存。
- **状态流转**：`PENDING` → `RUNNING` → `SUCCEEDED` 或 `FAILED`。`UNKNOWN` 表示任务不存在或已过期。

**任务状态说明**：

| task\_status | 说明     |
| ------------ | ------ |
| PENDING      | 任务排队中  |
| RUNNING      | 任务处理中  |
| SUCCEEDED    | 任务成功完成 |
| FAILED       | 任务失败   |
| UNKNOWN      | 任务状态未知 |

## OpenAPI

````yaml get /tasks/{task_id}
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
  /tasks/{task_id}:
    get:
      summary: 查询视频生成结果
      operationId: getLivePortraitVideoTask
      description: 查询灵动人像 LivePortrait 视频生成任务状态，并在任务成功后获取视频 URL。
      parameters:
        - name: task_id
          in: path
          required: true
          schema:
            type: string
          description: 提交任务时返回的 `task_id`。
      responses:
        "200":
          description: 查询成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/LivePortraitVideoQueryResponse"
              examples:
                SUCCEEDED:
                  summary: 任务成功
                  value:
                    request_id: b64e9c68-3923-462d-b25a-xxxxxx
                    output:
                      task_id: a1c69ca5-810b-49ae-8b20-xxxxxx
                      task_status: SUCCEEDED
                      submit_time: 2025-12-26 11:33:03.146
                      scheduled_time: 2025-12-26 11:33:13.312
                      end_time: 2025-12-26 11:33:22.455
                      results:
                        video_url: http://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxx.mp4?Expires=xxxx
                    usage:
                      video_duration: 2.79
                      video_ratio: standard
                FAILED:
                  summary: 任务失败
                  value:
                    request_id: 7574ee8f-38a3-4b1e-9280-xxxxxx
                    output:
                      task_id: a8532587-fa8c-4ef8-82be-xxxxxx
                      task_status: FAILED
                      code: InvalidURL
                      message: Required URL is missing or invalid, please check the request URL.
                RUNNING:
                  summary: 任务处理中
                  value:
                    request_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
                    output:
                      task_id: a8532587-fa8c-4ef8-82be-xxxxxx
                      task_status: RUNNING
                      submit_time: 2025-12-26 11:33:03.146
                      scheduled_time: 2025-12-26 11:33:13.312
        "401":
          description: 认证失败
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
      x-codeSamples:
        - lang: curl
          label: cURL
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}' \
              --header "Authorization: Bearer $DASHSCOPE_API_KEY"
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

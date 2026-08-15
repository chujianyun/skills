> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Wan 2.6 — 查询结果

> 查询视频生成任务状态

查询任务状态并获取生成的视频。

## 轮询策略

1. [创建任务](/api-reference/video-generation/wan-reference-to-video/create-task)，获取 `task_id`。
2. 每 **15 秒**轮询一次，直到 `task_status` 为 `SUCCEEDED` 或 `FAILED`。
3. 任务成功后，从 `video_url` 获取视频。

## 注意事项

- **URL 有效期**：视频 URL 在 **24 小时**后过期，请及时下载。
- **状态流转**：`PENDING` → `RUNNING` → `SUCCEEDED` 或 `FAILED`。

## OpenAPI

````yaml get /tasks/{task_id}
openapi: 3.1.0
info:
  title: Wan 参考驱动视频生成 API
  description: Wan 参考驱动视频生成 API，支持通过参考图片或视频结合多模态输入（文本、图片、视频）生成表演视频，覆盖单人或多人互动、多镜头叙事及音视频同步等场景。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 千问AI平台
security:
  - BearerAuth: []
paths:
  /tasks/{task_id}:
    get:
      operationId: getRefToVideoTaskStatus
      summary: 查询任务结果
      description: 查询视频生成任务的状态与结果。
      parameters:
        - name: task_id
          in: path
          required: true
          description: 视频创建接口返回的任务标识符。
          schema:
            type: string
      responses:
        "200":
          description: 成功获取任务状态。
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
                  summary: 任务进行中
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
    RefToVideoRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称。
          enum:
            - wan2.6-r2v-flash
            - wan2.6-r2v
          example: wan2.6-r2v-flash
        input:
          $ref: "#/components/schemas/RefToVideoInput"
        parameters:
          $ref: "#/components/schemas/RefToVideoParameters"
    RefToVideoInput:
      type: object
      required:
        - prompt
        - reference_urls
      description: 参考驱动视频生成的输入数据。
      properties:
        prompt:
          type: string
          description: 描述目标视频内容的文本提示词。使用 `character1`、`character2` 等标识符，按顺序引用 `reference_urls` 中的参考角色，每个参考资源只能包含单个角色。
          example: 'Character1 says to Character2: "that sounds great"'
        reference_urls:
          type: array
          description: 参考图片或视频的 URL 列表，最多 5 个（最多 5 张图片，最多 3 个视频）。每个参考资源只能包含单个角色，顺序决定角色标识符（`character1`、`character2` 等）。
          items:
            type: string
            format: uri
          minItems: 1
          maxItems: 5
          example:
            - https://example.com/person1.mp4
            - https://example.com/person2.mp4
            - https://example.com/object.png
    RefToVideoParameters:
      type: object
      description: 参考驱动视频生成的生成参数。
      properties:
        size:
          type: string
          description: 输出分辨率，格式为 `宽*高`，决定视频画面比例（例如 `1280*720` 对应 16:9，`720*1280` 对应 9:16）。
          enum:
            - 1280*720
            - 720*1280
            - 960*960
            - 1920*1080
            - 1080*1920
          example: 1280*720
        duration:
          type: integer
          description: 视频时长，单位为秒，两个模型均支持 2 到 10 的整数值。
          minimum: 2
          maximum: 10
          example: 10
        audio:
          type: boolean
          description: 是否在视频中生成音频。`true`（默认）：生成带音频的视频；`false`：生成静音视频。静音视频仅 `wan2.6-r2v-flash` 支持。
          default: true
        shot_type:
          type: string
          description: 镜头模式。`multi`：多镜头切换，通过自然对话和场景转换增强表现力；`single`：固定单镜头视角。
          enum:
            - multi
            - single
          example: multi
        watermark:
          type: boolean
          description: 为输出视频添加水印。
          default: false
    AsyncTaskSubmitResponse:
      type: object
      description: 异步任务创建成功后的响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识符。
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务标识符，可通过 `GET /tasks/{task_id}` 轮询任务结果。
            task_status:
              type: string
              description: 任务初始状态，通常为 `PENDING`。
              enum:
                - PENDING
    TaskStatusResponse:
      type: object
      description: 包含参考驱动视频任务当前状态和结果的响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识符。
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务标识符。
            task_status:
              type: string
              description: 任务当前状态。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
            video_url:
              type: string
              format: uri
              description: 生成的视频 URL，仅在 `task_status` 为 `SUCCEEDED` 时出现。有效期 24 小时，请及时下载。
            code:
              type: string
              description: 错误码，仅在 `task_status` 为 `FAILED` 时出现。
            message:
              type: string
              description: 错误信息，仅在 `task_status` 为 `FAILED` 时出现。
        usage:
          type: object
          description: 用量统计（仅在任务成功时出现）。
          properties:
            video_count:
              type: integer
              description: 生成的视频数量。
            video_duration:
              type: integer
              description: 生成视频的时长，单位为秒。
    DashScopeErrorResponse:
      type: object
      description: DashScope API 错误响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识符。
        code:
          type: string
          description: 错误码（例如 `InvalidParameter`、`Throttling`、`Unauthorized`）。
          example: InvalidParameter
        message:
          type: string
          description: 可读的错误信息。
          example: "Invalid parameter: size"
````

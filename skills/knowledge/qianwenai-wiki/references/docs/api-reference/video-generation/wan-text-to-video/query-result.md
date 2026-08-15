> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Wan — 查询结果

> 查询视频生成任务状态（wan2.6 及更早版本）

查询任务状态并获取生成的视频。

## 轮询策略

1. 通过[创建任务](/api-reference/video-generation/wan-text-to-video/create-task)接口提交任务，保存返回的 `task_id`。
2. 每 **15 秒**轮询一次，直到 `task_status` 变为 `SUCCEEDED` 或 `FAILED`。
3. 任务成功后，从 `video_url` 下载视频。

## 注意事项

- **URL 有效期**：`video_url` 在 **24 小时**后过期，请及时下载。
- **状态流转**：`PENDING` → `RUNNING` → `SUCCEEDED` / `FAILED`。

## OpenAPI

````yaml get /tasks/{task_id}
openapi: 3.1.0
info:
  title: Wan 文本生成视频 API
  description: Wan 文本生成视频 API。支持多模态输入（文字、图像、音频），可生成最长 15 秒、分辨率高达 1080P 的视频。采用异步任务模式——先提交任务，再轮询获取结果。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 千问AI平台
security:
  - BearerAuth: []
paths:
  /tasks/{task_id}:
    get:
      operationId: getTextToVideoTaskStatus
      summary: 查询任务结果
      description: 查询视频生成任务的状态和结果。
      parameters:
        - name: task_id
          in: path
          required: true
          description: POST 提交端点返回的任务 ID。
          schema:
            type: string
      responses:
        "200":
          description: 成功获取任务状态
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
                      video_duration: 10
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
          description: 请求参数无效
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
    TextToVideoRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称。支持的模型及其能力详见端点描述中的模型列表。
          enum:
            - wan2.6-t2v
            - wan2.5-t2v-preview
            - wan2.2-t2v-plus
            - wan2.1-t2v-turbo
            - wan2.1-t2v-plus
          example: wan2.6-t2v
        input:
          type: object
          required:
            - prompt
          description: 视频生成的输入数据。
          properties:
            prompt:
              type: string
              description: "描述目标视频内容的文字提示词。生成多镜头视频（wan2.6）时，请使用以下格式：`Shot 1 [0–3 s]: 内容描述。Shot 2 [3–6 s]: 内容描述。` 以此类推。"
              example: A thrilling detective chase story with cinematic storytelling.
            audio_url:
              type: string
              format: uri
              description: 用于音视频同步的音频文件 URL。模型会根据音频对齐口型动作。支持 HTTP/HTTPS URL。**仅 wan2.5 和 wan2.6 系列支持。** 若在 wan2.5/wan2.6 上省略此参数，模型将自动生成背景音频（自动配音）。
        parameters:
          $ref: "#/components/schemas/TextToVideoParameters"
    TextToVideoParameters:
      type: object
      description: 视频生成参数。
      properties:
        size:
          type: string
          description: |-
            输出视频分辨率，格式为 `宽*高`。可用尺寸因模型而异：
            - **wan2.6-t2v**：`1280*720`（720P）、`1920*1080`（1080P）
            - **wan2.5-t2v-preview**：`832*480`（480P）、`1280*720`（720P）、`1920*1080`（1080P）
            - **wan2.2-t2v-plus**：`832*480`（480P）、`1920*1080`（1080P）
            - **wan2.1-t2v-turbo**：`832*480`（480P）、`1280*720`（720P）
            - **wan2.1-t2v-plus**：`1280*720`（720P）
          example: 1280*720
        duration:
          type: integer
          description: |-
            视频时长（秒）。可用时长因模型而异：
            - **wan2.6-t2v**：2 至 15 的整数
            - **wan2.5-t2v-preview**：5 或 10
            - **wan2.2-t2v-plus、wan2.1 系列**：固定为 5
          example: 15
        shot_type:
          type: string
          description: 镜头构成模式。设置为 `"multi"` 可启用多镜头叙事，自动进行镜头切换。**仅 wan2.6 系列支持。**
          enum:
            - multi
        prompt_extend:
          type: boolean
          description: 启用提示词优化。`true`（默认）：模型对提示词进行优化以提升生成效果。`false`：直接使用原始提示词。生成多镜头视频时建议启用。
          default: true
        watermark:
          type: boolean
          description: 在生成的视频上添加水印。默认值：`true`。
          default: true
        negative_prompt:
          type: string
          description: 描述不希望出现在视频中的内容。
        seed:
          type: integer
          description: 随机数种子，用于结果复现。取值范围：[0, 2147483647]。在相同参数下使用相同种子可获得更一致（但不完全相同）的结果。
          minimum: 0
          maximum: 2147483647
    AsyncTaskSubmitResponse:
      type: object
      description: 异步任务提交的响应结果。
      properties:
        request_id:
          type: string
          description: 请求的唯一标识符，用于追踪和排查问题。
          example: c1209113-8437-424f-a386-xxxxxx
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 用于轮询任务状态的任务 ID。配合 `GET /tasks/{task_id}` 使用。
              example: 966cebcd-dedc-4962-af88-xxxxxx
            task_status:
              type: string
              description: 任务初始状态，通常为 `PENDING`。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
    TaskStatusResponse:
      type: object
      description: 查询异步任务状态的响应结果。
      properties:
        request_id:
          type: string
          description: 请求的唯一标识符。
          example: c1209113-8437-424f-a386-xxxxxx
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID。
              example: 966cebcd-dedc-4962-af88-xxxxxx
            task_status:
              type: string
              description: 当前任务状态。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
            video_url:
              type: string
              format: uri
              description: 生成视频的 URL（MP4 格式）。仅在 `task_status` 为 `SUCCEEDED` 时返回。**有效期 24 小时**——请及时下载。
              example: https://dashscope-result-sh.oss-accelerate.aliyuncs.com/xxx.mp4?Expires=xxx
            code:
              type: string
              description: 错误代码。仅在 `task_status` 为 `FAILED` 时返回。
            message:
              type: string
              description: 错误信息。仅在 `task_status` 为 `FAILED` 时返回。
            task_metrics:
              type: object
              description: 任务结果统计。
              properties:
                TOTAL:
                  type: integer
                  description: 任务总数。
                SUCCEEDED:
                  type: integer
                  description: 成功任务数。
                FAILED:
                  type: integer
                  description: 失败任务数。
        usage:
          type: object
          description: 用量统计。仅在任务成功时返回。
          properties:
            video_count:
              type: integer
              description: 生成的视频数量。
            video_duration:
              type: integer
              description: 生成视频的总时长（秒）。
    DashScopeErrorResponse:
      type: object
      description: DashScope API 错误响应。
      properties:
        request_id:
          type: string
          description: 请求的唯一标识符。
        code:
          type: string
          description: 错误代码（如 `InvalidParameter`、`Throttling`、`Unauthorized`）。
          example: InvalidParameter
        message:
          type: string
          description: 人类可读的错误信息。
          example: Invalid model name
````

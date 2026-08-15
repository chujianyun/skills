> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Vidu -- 查询结果

> 查询 Vidu 图像生成任务的状态与结果。

提交任务后，建议每隔 **5 秒**轮询一次该接口，直到 `task_status` 为 `SUCCEEDED` 或 `FAILED`。

## 任务状态流转

`PENDING` -> `RUNNING` -> `SUCCEEDED` 或 `FAILED`

| 状态          | 说明                                |
| ----------- | --------------------------------- |
| `PENDING`   | 任务排队等待中                           |
| `RUNNING`   | 任务生成中                             |
| `SUCCEEDED` | 任务成功，可获取图片链接                      |
| `FAILED`    | 任务失败，查看 `code` 和 `message` 字段获取原因 |
| `CANCELED`  | 任务已取消                             |
| `UNKNOWN`   | 任务不存在或已过期（超过 24 小时）               |

<Note>
  - 成功响应中的图片下载链接有效期为 **24 小时**，请及时下载保存。
  - 支持配置异步回调，免去主动轮询。详见[配置异步回调](/developer-guides/run-and-scale/async-task-management)。
</Note>

## 错误码

请参见[错误信息](/api-reference/preparation/error-messages)。

## OpenAPI

````yaml get /tasks/{task_id}
openapi: 3.0.0
info:
  title: Vidu 图像生成 API
  description: Vidu 参考生图模型支持文生图、图片编辑、参考图生图等任务。API 采用异步调用模式，包含"创建任务"和"查询结果"两个步骤。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 千问AI平台
security:
  - BearerAuth: []
paths:
  /tasks/{task_id}:
    get:
      operationId: getViduImageGenerationTaskStatus
      summary: 查询任务结果
      description: 根据 task_id 查询任务状态与结果。task_id 有效期为 24 小时。建议设置合理的查询间隔（如 5 秒）进行轮询。
      parameters:
        - name: Authorization
          in: header
          required: true
          description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
          schema:
            type: string
        - name: task_id
          in: path
          required: true
          description: 任务 ID。将上一步接口返回的 task_id 完整替换。查询有效期为 24 小时。
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
                    request_id: f584a817-6e00-9841-961a-49f7382a03d4
                    output:
                      task_id: 6404d4ec-4cdf-45b5-8d7d-3d429c6baed5
                      task_status: SUCCEEDED
                      submit_time: 2026-07-13 20:27:41.291
                      scheduled_time: 2026-07-13 20:27:41.320
                      end_time: 2026-07-13 20:28:39.767
                      finished: true
                      choices:
                        - finish_reason: stop
                          message:
                            role: assistant
                            content:
                              - image: https://example.com/generated-image.png
                                type: image
                    usage:
                      SR: 2K
                      size: 2048*2048
                      image_count: 1
                RUNNING:
                  summary: 任务生成中
                  value:
                    request_id: b3c41e52-9d1a-4f87-bc23-xxxxxx
                    output:
                      task_id: 6404d4ec-4cdf-45b5-8d7d-3d429c6baed5
                      task_status: RUNNING
                      submit_time: 2026-07-13 20:27:41.291
                      scheduled_time: 2026-07-13 20:27:41.320
                FAILED:
                  summary: 任务执行失败
                  value:
                    request_id: 1f015514-b04c-9190-b4dd-8ba11bb15708
                    output:
                      task_id: ccae6c03-fe9f-48fd-b3d6-a524c4707f17
                      task_status: FAILED
                      submit_time: 2026-07-13 20:27:50.654
                      scheduled_time: 2026-07-13 20:27:50.689
                      end_time: 2026-07-13 20:27:51.090
                      code: InvalidParameter
                      message: Missing required field 'parameters.n' in request body
                UNKNOWN:
                  summary: 任务查询过期
                  value:
                    request_id: a4de7c32-7057-9f82-8581-xxxxxx
                    output:
                      task_id: 502a00b1-19d9-4839-a82f-xxxxxx
                      task_status: UNKNOWN
        "400":
          description: 请求失败
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
      x-codeSamples:
        - lang: curl
          label: cURL
          source: |-
            curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id} \
              --header "Authorization: Bearer $DASHSCOPE_API_KEY"
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    ViduImageGenerationRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称。
          enum:
            - vidu/vidu-image_reference2image
            - vidu/viduq3-fast_reference2image
            - vidu/viduq2-pro_reference2image
            - vidu/viduq2-fast_reference2image
          example: vidu/vidu-image_reference2image
        input:
          type: object
          required:
            - messages
          description: 输入参数对象。
          properties:
            messages:
              type: array
              description: 消息列表。数组内有且只有一个对象，该对象包含 role 和 content 两个属性。服务端会提取第一个非空 text 作为提示词，并提取全部 image 作为参考图。
              items:
                type: object
                properties:
                  role:
                    type: string
                    description: 消息的角色，建议设置为 user。
                    example: user
                  content:
                    type: array
                    description: 消息内容，包含文本提示词（text）和可选的参考图像（image，最多 14 张）。
                    items:
                      type: object
                      properties:
                        text:
                          type: string
                          description: 正向提示词，用于描述期望生成的图像内容、风格和构图。支持中英文，长度不超过 5000 个字符。整个 messages 中至少需要一个非空文本。
                          example: 一间有着精致窗户的花店,漂亮的木质门,摆放着花朵
                        image:
                          type: string
                          description: 参考图像的 URL。支持 HTTP 或 HTTPS 协议。所有模型最多支持输入 14 张参考图。图像格式：PNG、JPG、WEBP。宽高比：1:4 ~ 4:1。文件大小：所有图片总和不超过 50MB。
                          example: https://cdn.wanx.aliyuncs.com/tmp/pressure/umbrella1.png
        parameters:
          $ref: "#/components/schemas/ViduImageGenerationParameters"
    ViduImageGenerationParameters:
      type: object
      description: 控制图像生成参数。
      properties:
        size:
          type: string
          description: 图片尺寸，格式为宽*高（如 2048*2048）。不传时默认 1024*1024。不同模型支持的尺寸列表请参见页面下方的可用尺寸列表。
          default: 1024*1024
          example: 1024*1024
        n:
          type: integer
          description: 生成图片数量，当前仅支持 1。
          enum:
            - 1
          default: 1
          example: 1
        seed:
          type: integer
          description: 随机数种子，取值范围 [0, 2147483647]，0 表示随机。使用相同的 seed 参数值可使生成内容保持相对稳定。若不提供，算法将自动使用随机数种子。
          minimum: 0
          maximum: 2147483647
          example: 12345
        watermark:
          type: boolean
          description: 是否添加水印标识。false（默认）：不添加水印。true：添加水印。
          default: false
          example: false
    AsyncTaskSubmitResponse:
      type: object
      description: 异步任务创建成功响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识。可用于请求明细溯源和问题排查。
          example: 4909100c-7b5a-9f92-bfe5-xxxxxx
        output:
          type: object
          description: 任务输出信息。
          properties:
            task_id:
              type: string
              description: 任务 ID。用于查询任务状态与结果，有效期 24 小时。
              example: 0385dc79-5ff8-4d82-bcb6-xxxxxx
            task_status:
              type: string
              description: 任务状态。初始状态通常为 PENDING。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - CANCELED
                - UNKNOWN
              example: PENDING
        code:
          type: string
          description: 请求失败的错误码。请求成功时不会返回此参数。
        message:
          type: string
          description: 请求失败的详细信息。请求成功时不会返回此参数。
    TaskStatusResponse:
      type: object
      description: 任务查询响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识。可用于请求明细溯源和问题排查。
          example: f584a817-6e00-9841-961a-49f7382a03d4
        output:
          type: object
          description: 任务输出信息。
          properties:
            task_id:
              type: string
              description: 任务 ID。查询有效期 24 小时。
              example: 6404d4ec-4cdf-45b5-8d7d-3d429c6baed5
            task_status:
              type: string
              description: 任务状态。状态流转：PENDING（排队中）→ RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - CANCELED
                - UNKNOWN
            submit_time:
              type: string
              description: 任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。
              example: 2026-07-13 20:27:41.291
            scheduled_time:
              type: string
              description: 任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。
              example: 2026-07-13 20:27:41.320
            end_time:
              type: string
              description: 任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。
              example: 2026-07-13 20:28:39.767
            finished:
              type: boolean
              description: 是否完成，仅在 task_status=SUCCEEDED 时返回。
            choices:
              type: array
              description: 图片输出候选列表，仅在 task_status=SUCCEEDED 时返回。
              items:
                type: object
                properties:
                  finish_reason:
                    type: string
                    description: 结束原因，成功时通常为 stop。
                    example: stop
                  message:
                    type: object
                    description: 模型返回的消息。
                    properties:
                      role:
                        type: string
                        description: 消息的角色，固定为 assistant。
                        example: assistant
                      content:
                        type: array
                        description: 消息内容。
                        items:
                          type: object
                          properties:
                            type:
                              type: string
                              description: 输出内容的类型，固定为 image。
                              example: image
                            image:
                              type: string
                              description: 生成图像的下载链接，图像格式为 PNG。链接有效期为 24 小时，请及时下载并保存图像。
                              example: https://example.com/generated-image.png
            code:
              type: string
              description: 请求失败的错误码。请求成功时不会返回此参数。
            message:
              type: string
              description: 请求失败的详细信息。请求成功时不会返回此参数。
        usage:
          type: object
          description: 资源用量信息。只对成功的结果计数。
          properties:
            image_count:
              type: integer
              description: 生成图像的数量。
              example: 1
            size:
              type: string
              description: 生成图片的分辨率，格式为宽*高。
              example: 2048*2048
            SR:
              type: string
              description: 生成图像的分辨率档位。
              example: 2K
    DashScopeErrorResponse:
      type: object
      description: DashScope API 错误响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识。
          example: 7438d53d-6eb8-4596-8835-xxxxxx
        code:
          type: string
          description: 错误码。
          example: InvalidApiKey
        message:
          type: string
          description: 错误详细信息。
          example: No API-key provided.
````

> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Vidu -- 创建任务

> 使用 Vidu 模型提交图像生成任务（文生图/参考图生图），异步生成图像。

提交图像生成任务后，服务将异步生成图像。提交任务后，使用[查询任务结果](/api-reference/image-generation/vidu-image-generation/query-result)接口轮询任务状态，直到 `task_status` 为 `SUCCEEDED` 或 `FAILED`。

## 模型列表

| 模型                                 | 能力                                   | 输入模态  | 输出图像规格           |
| ---------------------------------- | ------------------------------------ | ----- | ---------------- |
| `vidu/vidu-image_reference2image`  | 参考生图、文生图、图片编辑，中英文字精准渲染、UI/图表像素级还原    | 文本、图像 | 1K/2K/4K，1 张，PNG |
| `vidu/viduq3-fast_reference2image` | 参考生图、文生图、图片编辑，高速高质低成本（比 Pro 降低约 50%） | 文本、图像 | 1K/2K/4K，1 张，PNG |
| `vidu/viduq2-pro_reference2image`  | 参考生图、文生图、图片编辑，复杂逻辑处理、上下文一致性          | 文本、图像 | 1K/2K/4K，1 张，PNG |
| `vidu/viduq2-fast_reference2image` | 参考生图、文生图、图片编辑，语义理解增强                 | 文本、图像 | 1K，1 张，PNG       |

## HTTP 调用

图像生成接口仅支持异步调用，请求时必须携带请求头 `X-DashScope-Async: enable`。

任务提交成功后返回 `task_id`，使用[查询任务结果](/api-reference/image-generation/vidu-image-generation/query-result)接口获取生成结果。

## 可用尺寸列表

### vidu-image

| 分辨率 | 支持尺寸                                                                                                                               |
| --- | ---------------------------------------------------------------------------------------------------------------------------------- |
| 1K  | 1024\*1024, 720\*1440, 1440\*720, 1024\*768, 768\*1024, 1920\*1088, 1088\*1920, 1536\*1024, 1024\*1536, 1920\*816, 816\*1920       |
| 2K  | 2048\*2048, 1088\*2160, 2160\*1088, 2736\*2048, 2048\*2736, 2560\*1440, 1440\*2560, 3072\*2048, 2048\*3072, 2560\*1104, 1104\*2560 |
| 4K  | 2880\*2880, 1440\*2880, 2880\*1440, 3312\*2480, 2480\*3312, 3840\*2160, 2160\*3840, 3520\*2352, 2352\*3520, 3840\*1648, 1648\*3840 |

### viduq3-fast

| 分辨率 | 支持尺寸                                                                                                                                                                     |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1K  | 1024\*1024, 768\*1376, 848\*1264, 896\*1200, 928\*1152, 1152\*928, 1200\*896, 1264\*848, 1376\*768, 1584\*672, 512\*2064, 2064\*512, 352\*2928, 2928\*352                |
| 2K  | 2048\*2048, 1536\*2752, 1696\*2528, 1792\*2400, 1856\*2304, 2304\*1856, 2400\*1792, 2528\*1696, 2752\*1536, 3168\*1344, 1024\*4128, 4128\*1024, 704\*5856, 5856\*704     |
| 4K  | 4096\*4096, 3072\*5504, 3392\*5056, 3584\*4800, 3712\*4608, 4608\*3712, 4800\*3584, 5056\*3392, 5504\*3072, 6336\*2688, 2048\*8256, 8256\*2048, 1408\*11712, 11712\*1408 |

### viduq2-pro

| 分辨率 | 支持尺寸                                                                                                                   |
| --- | ---------------------------------------------------------------------------------------------------------------------- |
| 1K  | 1024\*1024, 768\*1376, 848\*1264, 896\*1200, 928\*1152, 1152\*928, 1200\*896, 1264\*848, 1376\*768, 1584\*672          |
| 2K  | 2048\*2048, 1536\*2752, 1696\*2528, 1792\*2400, 1856\*2304, 2304\*1856, 2400\*1792, 2528\*1696, 2752\*1536, 3168\*1344 |
| 4K  | 4096\*4096, 3072\*5504, 3392\*5056, 3584\*4800, 3712\*4608, 4608\*3712, 4800\*3584, 5056\*3392, 5504\*3072, 6336\*2688 |

### viduq2-fast

| 分辨率 | 支持尺寸                                                                                                          |
| --- | ------------------------------------------------------------------------------------------------------------- |
| 1K  | 1024\*1024, 768\*1376, 848\*1264, 896\*1200, 928\*1152, 1152\*928, 1200\*896, 1264\*848, 1376\*768, 1584\*672 |

## OpenAPI

````yaml post /services/aigc/image-generation/generation
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
  /services/aigc/image-generation/generation:
    post:
      operationId: createViduImageGenerationTask
      summary: 创建图像生成任务
      description: 提交图像生成任务，返回 task_id 用于后续轮询查询。
      parameters:
        - name: Content-Type
          in: header
          required: true
          description: 请求内容类型，必须设置为 application/json。
          schema:
            type: string
            enum:
              - application/json
        - name: X-DashScope-Async
          in: header
          required: true
          description: 异步处理配置参数。HTTP 请求只支持异步，必须设置为 enable。缺少此请求头将报错："current user api does not support synchronous calls"。
          schema:
            type: string
            enum:
              - enable
        - name: X-DashScope-Callback-URL
          in: header
          required: false
          description: 任务完成后的回调通知地址。
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/ViduImageGenerationRequest"
      responses:
        "200":
          description: 任务创建成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/AsyncTaskSubmitResponse"
        "400":
          description: 请求失败
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
      x-codeSamples:
        - lang: curl
          label: 文生图
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image-generation/generation' \
              --header 'X-DashScope-Async: enable' \
              --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
              --header 'Content-Type: application/json' \
              --data '{
              "model": "vidu/vidu-image_reference2image",
              "input": {
                "messages": [
                  {
                    "role": "user",
                    "content": [
                      {
                        "text": "一间有着精致窗户的花店,漂亮的木质门,摆放着花朵"
                      }
                    ]
                  }
                ]
              },
              "parameters": {
                "size": "1024*1024",
                "n": 1,
                "watermark": false
              }
            }'
        - lang: curl
          label: 参考图生图
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image-generation/generation' \
              --header 'X-DashScope-Async: enable' \
              --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
              --header 'Content-Type: application/json' \
              --data '{
              "model": "vidu/vidu-image_reference2image",
              "input": {
                "messages": [
                  {
                    "role": "user",
                    "content": [
                      {
                        "text": "参考图片的风格，生成一只坐着的橘黄色的猫"
                      },
                      {
                        "image": "https://cdn.wanx.aliyuncs.com/tmp/pressure/umbrella1.png"
                      }
                    ]
                  }
                ]
              },
              "parameters": {
                "size": "2048*2048",
                "n": 1,
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

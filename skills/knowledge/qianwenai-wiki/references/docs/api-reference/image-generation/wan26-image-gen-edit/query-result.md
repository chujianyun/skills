> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Wan 2.6 — 查询结果

> 查询 Wan 2.6 图像任务状态

查询任务状态和结果。

## 轮询策略

使用返回的 `task_id` 轮询此接口，建议轮询间隔为 **5-10 秒**。

## 注意事项

- **URL 有效期**：图片 URL 在 **24 小时**后过期，请及时下载。
- **任务状态流转**：`PENDING` → `RUNNING` → `SUCCEEDED` 或 `FAILED`。
- **其他状态**：`CANCELED`（任务已取消）、`UNKNOWN`（task\_id 无效或已过期）。
- **task\_id 有效期**：task\_id 有效期为 24 小时，过期后无法查询任务状态和结果。
- **避免重复提交**：请通过轮询获取结果，不要重复提交请求。

## OpenAPI

````yaml get /tasks/{task_id}
openapi: 3.1.0
info:
  title: Wan2.6 图像生成与编辑 API
  description: Wan2.6 图像生成与编辑 API，支持多图输入、图像编辑及图文交织输出。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 北京
security:
  - BearerAuth: []
paths:
  /tasks/{task_id}:
    get:
      operationId: getWan26ImageTaskResult
      summary: 查询任务结果
      description: 查询异步图像任务的状态和结果。
      parameters:
        - name: task_id
          in: path
          required: true
          description: 异步任务创建接口返回的任务标识符。
          schema:
            type: string
      responses:
        "200":
          description: 成功获取任务状态。
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Wan26TaskStatusResponse"
              examples:
                SUCCEEDED:
                  summary: 任务成功
                  value:
                    request_id: 43d9e959-25bc-4dc7-9888-xxxxxx
                    output:
                      task_id: 858cad55-4bdc-4ba3-ae6c-xxxxxx
                      task_status: SUCCEEDED
                      submit_time: 2025-12-16 04:21:02.275
                      scheduled_time: 2025-12-16 04:21:02.304
                      end_time: 2025-12-16 04:24:46.658
                      finished: true
                      choices:
                        - finish_reason: stop
                          message:
                            role: assistant
                            content:
                              - image: https://dashscope-result.oss-cn-shanghai.aliyuncs.com/1xxx.png?Expires=xxx
                                type: image
                        - finish_reason: stop
                          message:
                            role: assistant
                            content:
                              - image: https://dashscope-result.oss-cn-shanghai.aliyuncs.com/2xxx.png?Expires=xxx
                                type: image
                    usage:
                      size: 1376*768
                      total_tokens: 0
                      image_count: 2
                      output_tokens: 0
                      input_tokens: 0
                FAILED:
                  summary: 任务失败
                  value:
                    request_id: a4d78a5f-655f-9639-8437-xxxxxx
                    output:
                      task_id: 858cad55-4bdc-4ba3-ae6c-xxxxxx
                      task_status: FAILED
                    code: InvalidParameter
                    message: num_images_per_prompt must be 1
                RUNNING:
                  summary: 任务运行中
                  value:
                    request_id: c1209113-8437-424f-a386-xxxxxx
                    output:
                      task_id: 858cad55-4bdc-4ba3-ae6c-xxxxxx
                      task_status: RUNNING
        "400":
          description: 请求参数无效。
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
      x-codeSamples:
        - lang: curl
          label: cURL - Query task result
          source: |-
            # 将 {task_id} 替换为前一个 API 调用返回的 task_id 值。
            # task_id 有效期为 24 小时。
            curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id} \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY"
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    Wan26ImageRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称。设置为 `wan2.6-image`。
          enum:
            - wan2.6-image
          example: wan2.6-image
        input:
          type: object
          required:
            - messages
          description: 包含消息数组的输入数据。
          properties:
            messages:
              type: array
              description: "请求内容数组。仅支持单轮对话，提供一条 `role: user` 的消息。"
              minItems: 1
              maxItems: 1
              items:
                $ref: "#/components/schemas/Wan26ImageMessage"
        parameters:
          $ref: "#/components/schemas/Wan26ImageParameters"
    Wan26ImageMessage:
      type: object
      required:
        - role
        - content
      properties:
        role:
          type: string
          enum:
            - user
          description: 消息角色。必须为 `user`。
        content:
          type: array
          description: |-
            消息内容数组。必须包含且仅包含一个 `text` 对象。图像对象的数量取决于模式：
            - 图像编辑模式（`enable_interleave=false`）：需要 **1 到 4** 个图像对象。
            - 图文交织模式（`enable_interleave=true`）：**0 到 1** 个图像对象。

            使用多张图像时，在数组中包含多个 `image` 对象，图像顺序由数组位置决定。
          items:
            $ref: "#/components/schemas/Wan26ImageContentPart"
    Wan26ImageContentPart:
      type: object
      description: 图像或文本内容部分。
      properties:
        text:
          type: string
          description: 正向提示词，描述期望的图像内容、风格和构图。支持中英文，最多 2,000 个字符（每个汉字、字母、数字或符号均计为一个字符），超出部分将自动截断。`content` 数组中必须且仅包含一个 `text` 对象。
          maxLength: 2000
          example: Generate a tomato and egg stir-fry based on the style of image 1 and the background of image 2
        image:
          type: string
          description: |-
            输入图像，可以是公开 URL（HTTP/HTTPS）或 Base64 编码字符串（`data:{mime_type};base64,{data}`）。

            **图像限制：**
            - 格式：JPEG、JPG、PNG（不支持透明通道）、BMP、WEBP。
            - 分辨率：宽和高各在 240 到 8,000 像素之间。
            - 文件大小：最大 10 MB。

            **图像数量限制：**
            - `enable_interleave=false`（图像编辑）：需输入 1 到 4 张图像。
            - `enable_interleave=true`（图文交织）：可输入 0 到 1 张图像。
          example: https://cdn.wanx.aliyuncs.com/tmp/pressure/umbrella1.png
    Wan26ImageParameters:
      type: object
      description: 图像处理参数。
      properties:
        negative_prompt:
          type: string
          description: |-
            反向提示词，描述不希望出现在图像中的内容。支持中英文，最多 500 个字符，超出部分将自动截断。

            示例：`低分辨率、低质量、肢体变形、手指变形、颜色过度饱和、蜡像感、面部细节缺失、皮肤过度光滑、AI 痕迹明显、构图混乱、文字模糊或扭曲。`
          maxLength: 500
        size:
          type: string
          description: |-
            输出图像分辨率。支持两种方式：参考输入图像比例或直接指定尺寸。

            **图像编辑模式**（`enable_interleave=false`）：
            - 方式一（推荐）：`1K`（默认）或 `2K`。输出总像素接近 1280\*1280 或 2048\*2048，并保持最后一张输入图像的宽高比。
            - 方式二：直接指定 `宽*高`（像素）。总像素需在 [768\*768, 2048\*2048] 范围内，宽高比在 [1:4, 4:1] 之间，实际值为 16 的倍数。

            **图文交织模式**（`enable_interleave=true`）：
            - 方式一（默认）：参考输入图像比例。若总像素 <= 1280\*1280，输出与输入一致；若 > 1280\*1280，则缩放至约 1280\*1280。
            - 方式二：指定 `宽*高`。总像素需在 [768\*768, 1280\*1280] 范围内，宽高比在 [1:4, 4:1] 之间。

            **推荐分辨率：** 1280\*1280（1:1）、800\*1200（2:3）、1200\*800（3:2）、960\*1280（3:4）、1280\*960（4:3）、720\*1280（9:16）、1280\*720（16:9）、1344\*576（21:9）。
          example: 1K
        enable_interleave:
          type: boolean
          description: |-
            控制图像生成模式：
            - `false`（默认）：图像编辑模式。支持多图输入（1-4 张），可进行主体一致性生成，可生成 1 到 4 张结果图像。
            - `true`：图文交织输出模式。支持 0-1 张输入图像，生成包含文本和图像的混合内容。**仅同步调用时**，必须同时设置 `stream=true` 并添加 `X-DashScope-Sse: enable` 请求头；异步调用无需设置。
          default: false
        n:
          type: integer
          description: |-
            生成图像数量。行为取决于模式：
            - 图像编辑模式（`enable_interleave=false`）：范围 1-4，默认值为 4。
            - 图文交织模式（`enable_interleave=true`）：必须为 1，使用 `max_images` 控制图像数量。

            **注意：** `n` 直接影响计费。费用 = 单价 × 成功生成的图像数量。
          minimum: 1
          maximum: 4
          default: 4
        max_images:
          type: integer
          description: |-
            仅在图文交织模式（`enable_interleave=true`）下生效。指定模型在单次响应中最多可生成的图像数量，范围 1-5，默认值为 5。实际生成数量由模型推理决定，可能少于该值。

            **注意：** `max_images` 影响计费。费用 = 单价 × 成功生成的图像数量。
          minimum: 1
          maximum: 5
          default: 5
        prompt_extend:
          type: boolean
          description: 仅在图像编辑模式（`enable_interleave=false`）下生效。启用智能提示词改写，对正向提示词进行优化扩展。反向提示词不受影响。
          default: true
        stream:
          type: boolean
          description: 控制是否使用流式输出。仅同步调用时，在图文交织模式（`enable_interleave=true`）下**必须**设置为 `true`；异步调用无需设置此参数。
          default: false
        watermark:
          type: boolean
          description: 在图像右下角添加固定文本「AI Generated」的水印标识。
          default: false
        seed:
          type: integer
          description: 随机数种子，范围 [0, 2147483647]。相同种子可产生更一致（但不完全相同）的结果。若不指定，则使用随机种子。
          minimum: 0
          maximum: 2147483647
    Wan26ImageResponse:
      type: object
      description: Wan2.6 图像生成响应。
      example:
        output:
          choices:
            - finish_reason: stop
              message:
                content:
                  - image: https://dashscope-result.oss-cn-shanghai.aliyuncs.com/xxx.png?Expires=xxx
                    type: image
                role: assistant
          finished: true
        usage:
          image_count: 1
          input_tokens: 0
          output_tokens: 0
          size: 1376*768
          total_tokens: 0
        request_id: a3f4befe-cacd-49c9-8298-xxxxxx
      properties:
        output:
          type: object
          properties:
            choices:
              type: array
              description: 生成结果列表。
              items:
                $ref: "#/components/schemas/Wan26ImageChoice"
            finished:
              type: boolean
              description: 是否已完成生成。
        usage:
          type: object
          description: 用量统计。用量统计在与 `output` 同级的顶层 `usage` 字段中返回，读取方式为 `response.usage["image_count"]`。`output` 对象中不包含用量统计：`response.output.usage` 返回 `{}`，其中没有 `image_count`。
          properties:
            image_count:
              type: integer
              description: 生成的图像数量。
            input_tokens:
              type: integer
              description: 消耗的输入 token 数量。
            output_tokens:
              type: integer
              description: 消耗的输出 token 数量。
            size:
              type: string
              description: 生成图像的分辨率。
            total_tokens:
              type: integer
              description: 消耗的总 token 数量（输入 + 输出）。
        request_id:
          type: string
          description: 用于追踪和排查问题的唯一请求标识符。
          example: a3f4befe-cacd-49c9-8298-xxxxxx
    Wan26ImageChoice:
      type: object
      properties:
        finish_reason:
          type: string
          description: "`stop` 表示正常完成；`null` 表示流式输出仍在进行中。"
          example: stop
        message:
          type: object
          properties:
            role:
              type: string
              description: 固定为 `assistant`。
              enum:
                - assistant
            content:
              type: array
              description: 响应内容数组，包含生成的图像 URL 和/或文本（图文交织模式下）。
              items:
                $ref: "#/components/schemas/Wan26ImageResponseContentPart"
    Wan26ImageResponseContentPart:
      type: object
      description: 响应中的内容部分，可以是图像或文本。
      properties:
        type:
          type: string
          description: 内容类型：`image` 或 `text`。
          enum:
            - image
            - text
        image:
          type: string
          description: 生成的图像 URL（PNG 格式）。**有效期为 24 小时**，请及时下载。
        text:
          type: string
          description: 文本内容（仅在图文交织输出模式下存在）。
    Wan26ImageAsyncRequest:
      type: object
      description: Wan2.6 图像生成/编辑异步任务的请求体。
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称。设置为 `wan2.6-image`。
          enum:
            - wan2.6-image
          example: wan2.6-image
        input:
          type: object
          required:
            - messages
          description: 包含消息数组的输入数据。
          properties:
            messages:
              type: array
              description: "请求内容数组。仅支持单轮对话，提供一条 `role: user` 的消息。"
              minItems: 1
              maxItems: 1
              items:
                $ref: "#/components/schemas/Wan26ImageMessage"
        parameters:
          $ref: "#/components/schemas/Wan26ImageParameters"
    AsyncTaskSubmitResponse:
      type: object
      description: 异步任务创建成功后返回的响应。
      example:
        output:
          task_status: PENDING
          task_id: 0385dc79-5ff8-4d82-bcb6-xxxxxx
        request_id: 4909100c-7b5a-9f92-bfe5-xxxxxx
      properties:
        request_id:
          type: string
          description: 用于排查问题的唯一请求标识符。
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务标识符。通过 `GET /tasks/{task_id}` 查询任务状态，有效期为 24 小时。
            task_status:
              type: string
              description: 初始任务状态，通常为 `PENDING`。
              enum:
                - PENDING
    Wan26TaskStatusResponse:
      type: object
      description: 查询异步任务状态时返回的响应。
      properties:
        request_id:
          type: string
          description: 用于排查问题的唯一请求标识符。
        output:
          type: object
          description: 任务输出信息。
          properties:
            task_id:
              type: string
              description: 任务标识符。
            task_status:
              type: string
              description: 当前任务状态。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - CANCELED
                - UNKNOWN
            submit_time:
              type: string
              description: 任务提交时间，采用 UTC+8 时区。格式：`YYYY-MM-DD HH:mm:ss.SSS`。
            scheduled_time:
              type: string
              description: 任务开始运行的时间。格式：`YYYY-MM-DD HH:mm:ss.SSS`。
            end_time:
              type: string
              description: 任务完成的时间。格式：`YYYY-MM-DD HH:mm:ss.SSS`。
            finished:
              type: boolean
              description: 任务是否已完成。
            choices:
              type: array
              description: 生成结果列表。`task_status` 为 `SUCCEEDED` 时返回。
              items:
                $ref: "#/components/schemas/Wan26ImageChoice"
        usage:
          type: object
          description: 用量统计，仅统计成功生成的结果。用量统计在与 `output` 同级的顶层 `usage` 字段中返回，读取方式为 `response.usage["image_count"]`，其中 `image_count` 为该任务生成的图片总数。`output` 对象中不包含用量统计：`response.output.usage` 返回 `{}`，其中没有 `image_count`。
          properties:
            image_count:
              type: integer
              description: 生成的图像数量。
            input_tokens:
              type: integer
              description: 消耗的输入 token 数量。
            output_tokens:
              type: integer
              description: 消耗的输出 token 数量。
            size:
              type: string
              description: 生成图像的分辨率。
            total_tokens:
              type: integer
              description: 消耗的总 token 数量（输入 + 输出）。
        code:
          type: string
          description: 错误码，仅在请求失败时返回。
        message:
          type: string
          description: 详细错误信息，仅在请求失败时返回。
    DashScopeErrorResponse:
      type: object
      description: DashScope API 错误响应。
      example:
        request_id: a4d78a5f-655f-9639-8437-xxxxxx
        code: InvalidParameter
        message: num_images_per_prompt must be 1
      properties:
        request_id:
          type: string
          description: 唯一请求标识符。
        code:
          type: string
          description: 错误码（如 `InvalidParameter`、`Throttling`、`InvalidApiKey`）。
          example: InvalidParameter
        message:
          type: string
          description: 人类可读的错误信息。
          example: num_images_per_prompt must be 1
````

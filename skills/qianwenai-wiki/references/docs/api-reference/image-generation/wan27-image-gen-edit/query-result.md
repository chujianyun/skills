> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Wan 2.7 — 查询结果

> 查询 Wan 2.7 图像任务状态

查询任务状态和结果。

## 轮询策略

使用返回的 `task_id` 轮询此接口，建议每 **5-10 秒**轮询一次。

## 注意事项

- **URL 有效期**：图片 URL 在 **24 小时**后过期，请及时下载。
- **任务状态流转**：`PENDING` → `RUNNING` → `SUCCEEDED` 或 `FAILED`。
- **其他状态**：`CANCELED`（任务已取消）、`UNKNOWN`（任务 ID 无效或已过期）。
- **`task_id` 有效期**：`task_id` 有效期为 24 小时，过期后无法查询状态和结果。
- **避免重复提交**：请通过轮询获取结果，不要重复提交请求。

## OpenAPI

````yaml get /tasks/{task_id}
openapi: 3.1.0
info:
  title: Wan2.7 图像生成与编辑 API
  description: Wan2.7 图像生成与编辑 API，支持文生图、多图编辑、边界框交互式编辑以及图像集生成。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 北京
security:
  - BearerAuth: []
paths:
  /tasks/{task_id}:
    get:
      operationId: getWan27ImageTaskResult
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
                $ref: "#/components/schemas/Wan27TaskStatusResponse"
              examples:
                SUCCEEDED:
                  summary: 任务成功
                  value:
                    request_id: 43d9e959-25bc-4dc7-9888-xxxxxx
                    output:
                      task_id: 858cad55-4bdc-4ba3-ae6c-xxxxxx
                      task_status: SUCCEEDED
                      submit_time: 2026-03-31 19:57:58.840
                      scheduled_time: 2026-03-31 19:57:58.877
                      end_time: 2026-03-31 19:58:11.563
                      finished: true
                      choices:
                        - finish_reason: stop
                          message:
                            role: assistant
                            content:
                              - image: https://dashscope-result.oss-cn-shanghai.aliyuncs.com/1xxx.png?Expires=xxx
                                type: image
                    usage:
                      size: 2985*1405
                      total_tokens: 18792
                      image_count: 1
                      output_tokens: 2
                      input_tokens: 18790
                FAILED:
                  summary: 任务失败
                  value:
                    request_id: a4d78a5f-655f-9639-8437-xxxxxx
                    output:
                      task_id: 858cad55-4bdc-4ba3-ae6c-xxxxxx
                      task_status: FAILED
                      code: InvalidParameter
                      message: Invalid parameter value
                RUNNING:
                  summary: 任务执行中
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
            # 将 {task_id} 替换为上一次 API 调用返回的 task_id 值。
            # task_id 在 24 小时内有效。
            curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id} \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY"
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    Wan27ImageRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称。可选值：wan2.7-image-pro、wan2.7-image。
          enum:
            - wan2.7-image-pro
            - wan2.7-image
          example: wan2.7-image-pro
        input:
          type: object
          required:
            - messages
          description: 包含消息数组的输入数据。
          properties:
            messages:
              type: array
              description: 请求内容数组。目前仅支持单轮对话，即只能传入一组 role 和 content 参数，不支持多轮对话。
              minItems: 1
              maxItems: 1
              items:
                $ref: "#/components/schemas/Wan27ImageMessage"
        parameters:
          $ref: "#/components/schemas/Wan27ImageParameters"
    Wan27ImageMessage:
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
            消息内容数组。必须包含一个 `text` 对象和 0 到 9 个 `image` 对象。

            使用多张图片时，在数组中放入多个 `image` 对象。图片顺序由数组位置决定。
          items:
            $ref: "#/components/schemas/Wan27ImageContentPart"
    Wan27ImageContentPart:
      type: object
      description: 图片或文本内容部分。
      properties:
        text:
          type: string
          description: 用户输入的提示词。支持中英文。长度不超过 5000 个字符（每个中文字符、字母、数字或符号均计为一个字符，超出部分自动截断）。`content` 数组中必须包含且仅包含一个 `text` 对象。
          maxLength: 5000
          example: Spray the graffiti from image 2 onto the car in image 1
        image:
          type: string
          description: |-
            输入图片，支持公开 URL（HTTP/HTTPS）或 Base64 编码字符串（`data:{mime_type};base64,{data}`）。

            **图片约束：**
            - 格式：JPEG、JPG、PNG（不支持 Alpha 通道）、BMP、WEBP。
            - 分辨率：宽和高各自在 240 到 8000 像素之间，宽高比在 [1:8, 8:1] 范围内。
            - 文件大小：最大 20 MB。
            - 数量：每次请求最多 9 张图片。
          example: https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/pjeqdf/car.webp
    Wan27ImageParameters:
      type: object
      description: 图像处理参数。
      properties:
        size:
          type: string
          description: |-
            输出图像分辨率。支持两种指定方式，不可同时使用。

            **wan2.7-image-pro：**
            - 方式一（推荐）：`1K`、`2K`（默认）或 `4K`。
              - 适用范围：文生图（无图片输入，且非图像集生成模式）支持 1K、2K 和 4K；其他场景仅支持 1K 和 2K。
              - 总像素数：1K = 1024×1024，2K = 2048×2048，4K = 4096×4096。
              - 宽高比：有图片输入时，输出图像按最后一张输入图片的宽高比缩放到对应分辨率；无图片输入时，输出为正方形。
            - 方式二：以 `width*height` 形式指定像素数，宽高比在 [1:8, 8:1] 范围内。
              - 文生图：总像素数在 [768×768, 4096×4096] 范围内。
              - 其他场景：总像素数在 [768×768, 2048×2048] 范围内。

            **wan2.7-image：**
            - 方式一（推荐）：`1K` 或 `2K`（默认），不支持 4K。
            - 方式二：以 `width*height` 形式指定像素数。所有场景总像素数在 [768×768, 2048×2048] 范围内，宽高比在 [1:8, 8:1] 范围内。

            输出图像的实际像素值可能与指定值略有差异。
          example: 2K
        n:
          type: integer
          description: |-
            生成图像的数量。

            **注意：** `n` 的值直接影响费用。费用 = 单价 × 成功生成的图像数量。

            - 未启用图像集模式（`enable_sequential=false`）：表示生成图像的数量，范围 1–4，默认为 4。
            - 启用图像集模式（`enable_sequential=true`）：表示最多生成的图像数量，范围 1–12，默认为 12。实际数量由模型决定，不超过 `n`。
          minimum: 1
          maximum: 12
          default: 4
        enable_sequential:
          type: boolean
          description: |-
            控制图像生成模式。
            - `false`：默认值。
            - `true`：启用图像集输出模式。
          default: false
        thinking_mode:
          type: boolean
          description: 是否启用思考模式。默认为 `true`（启用）。仅在未启用图像集模式且无图片输入时生效。启用后，模型将增强推理能力以提升图像质量，但会增加生成时间。
          default: true
        bbox_list:
          type: array
          description: |-
            交互式编辑的选区。

            - 对应关系：列表长度必须与输入图片数量一致。若某张图片无需编辑，对应位置传入空列表 `[]`。
            - 坐标格式：`[x1, y1, x2, y2]`（左上角 x、左上角 y、右下角 x、右下角 y），使用原始图片的绝对像素坐标，左上角为 (0, 0)。
            - 限制：单张图片最多支持 2 个边界框。
          items:
            type: array
            description: 单张输入图片的边界框列表。空数组表示无边界框。
            items:
              type: array
              description: 单个边界框 [x1, y1, x2, y2]。
              items:
                type: integer
              minItems: 4
              maxItems: 4
            maxItems: 2
        color_palette:
          type: array
          description: 自定义色彩主题。由颜色（`hex`）和比例（`ratio`）对象组成的数组，须包含 3 到 10 种颜色（推荐设置为 8 种）。仅在未启用图像集模式（`enable_sequential=false`）时可用。
          minItems: 3
          maxItems: 10
          items:
            type: object
            required:
              - hex
              - ratio
            properties:
              hex:
                type: string
                description: 十六进制（HEX）格式的颜色值。示例：`#C2D1E6`。
              ratio:
                type: string
                description: 该颜色的占比，精确到小数点后两位（例如 `"25.00%"`）。所有 `ratio` 值之和必须为 100.00%。
          example:
            - hex: "#C2D1E6"
              ratio: 60.00%
            - hex: "#636574"
              ratio: 25.00%
            - hex: "#CBD4E4"
              ratio: 15.00%
        watermark:
          type: boolean
          description: 在图像右下角添加固定文字水印"AI Generated"。
          default: false
        seed:
          type: integer
          description: 随机数种子。有效范围：[0, 2147483647]。使用相同种子可生成相似结果。若不指定，算法将使用随机种子。注意：图像生成具有概率性，即使使用相同种子，结果也可能存在差异。
          minimum: 0
          maximum: 2147483647
    Wan27ImageResponse:
      type: object
      description: Wan2.7 图像生成响应。
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
          input_tokens: 18790
          output_tokens: 2
          size: 2985*1405
          total_tokens: 18792
        request_id: a3f4befe-cacd-49c9-8298-xxxxxx
      properties:
        output:
          type: object
          properties:
            choices:
              type: array
              description: 生成结果列表。
              items:
                $ref: "#/components/schemas/Wan27ImageChoice"
            finished:
              type: boolean
              description: 生成是否已完成。
        usage:
          type: object
          description: 用量统计。
          properties:
            image_count:
              type: integer
              description: 已生成的图像数量。
            input_tokens:
              type: integer
              description: 消耗的输入 token 数量。
            output_tokens:
              type: integer
              description: 消耗的输出 token 数量。
            total_tokens:
              type: integer
              description: 消耗的总 token 数量。
            size:
              type: string
              description: 实际输出图像尺寸（宽×高）。
              example: 2985*1405
        request_id:
          type: string
          description: 唯一请求标识符。
          example: a3f4befe-cacd-49c9-8298-xxxxxx
    Wan27ImageChoice:
      type: object
      properties:
        finish_reason:
          type: string
          description: 生成完成的原因。
          example: stop
        message:
          type: object
          properties:
            role:
              type: string
              example: assistant
            content:
              type: array
              items:
                type: object
                properties:
                  image:
                    type: string
                    description: 生成图像的 URL。**URL 在 24 小时后失效，请及时下载保存。**
                    example: https://dashscope-result.oss-cn-shanghai.aliyuncs.com/xxx.png?Expires=xxx
                  type:
                    type: string
                    example: image
    AsyncTaskSubmitResponse:
      type: object
      description: 异步任务提交成功后返回的响应。
      example:
        request_id: ccf4b2f4-bf30-9e13-9461-3a28c6a7bxxx
        output:
          task_id: 8811b4a4-00ac-4aa2-a2fd-017d3b90cxxx
          task_status: PENDING
      properties:
        request_id:
          type: string
          description: 唯一请求标识符。
          example: ccf4b2f4-bf30-9e13-9461-3a28c6a7bxxx
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务标识符。用于轮询结果接口，24 小时内有效。
              example: 8811b4a4-00ac-4aa2-a2fd-017d3b90cxxx
            task_status:
              type: string
              description: 初始任务状态。创建完成后始终为 `PENDING`。
              example: PENDING
    Wan27TaskStatusResponse:
      type: object
      description: 任务状态查询接口的响应。
      properties:
        request_id:
          type: string
          description: 唯一请求标识符。
          example: 43d9e959-25bc-4dc7-9888-xxxxxx
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务标识符。
              example: 858cad55-4bdc-4ba3-ae6c-xxxxxx
            task_status:
              type: string
              description: 当前任务状态：`PENDING`（排队中）、`RUNNING`（处理中）、`SUCCEEDED`（已完成）、`FAILED`（失败）、`CANCELED`（已取消）、`UNKNOWN`（任务 ID 无效或已过期）。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - CANCELED
                - UNKNOWN
              example: SUCCEEDED
            submit_time:
              type: string
              description: 任务提交时间。
              example: 2026-03-31 19:57:58.840
            scheduled_time:
              type: string
              description: 任务调度时间。
              example: 2026-03-31 19:57:58.877
            end_time:
              type: string
              description: 任务完成时间。
              example: 2026-03-31 19:58:11.563
            finished:
              type: boolean
              description: 任务是否已结束。
              example: true
            choices:
              type: array
              description: 已生成的图像。仅在 `task_status` 为 `SUCCEEDED` 时存在。
              items:
                $ref: "#/components/schemas/Wan27ImageChoice"
            code:
              type: string
              description: 错误码。仅在 `task_status` 为 `FAILED` 时存在。
            message:
              type: string
              description: 错误信息。仅在 `task_status` 为 `FAILED` 时存在。
        usage:
          type: object
          description: 用量统计。仅在 `task_status` 为 `SUCCEEDED` 时存在。
          properties:
            image_count:
              type: integer
              description: 已生成的图像数量。
            input_tokens:
              type: integer
              description: 消耗的输入 token 数量。
            output_tokens:
              type: integer
              description: 消耗的输出 token 数量。
            total_tokens:
              type: integer
              description: 消耗的总 token 数量。
            size:
              type: string
              description: 实际输出图像尺寸。
              example: 2985*1405
    DashScopeErrorResponse:
      type: object
      properties:
        code:
          type: string
          description: 错误码。
          example: InvalidParameter
        message:
          type: string
          description: 错误信息。
          example: Invalid parameter value
        request_id:
          type: string
          description: 唯一请求标识符。
          example: a3f4befe-cacd-49c9-8298-xxxxxx
````

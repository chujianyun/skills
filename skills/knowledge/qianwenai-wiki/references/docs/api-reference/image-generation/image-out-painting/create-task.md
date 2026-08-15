> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 图像画面扩展 — 创建任务

> 创建图像画面扩展异步任务

<Note>
  请先[获取 API Key](/api-reference/preparation/api-key) 并[设置为环境变量](/api-reference/preparation/export-api-key-env)。
</Note>

支持旋转图像、等比例扩图、指定方向扩图、指定宽高比扩图。

## 扩图模式与优先级

参数存在优先级关系：当同时设置多个扩图模式的参数时，仅高优先级的参数生效。旋转参数 `angle` 不受优先级影响，可与任意扩图模式叠加使用。

| 功能      | 参数                                                        | 说明                      |
| ------- | --------------------------------------------------------- | ----------------------- |
| 旋转      | `angle`                                                   | 先旋转，后扩展。可与下方任意扩图模式同时使用。 |
| 扩图优先级 1 | `output_ratio`                                            | 按宽高比扩展画面。               |
| 扩图优先级 2 | `x_scale`、`y_scale`                                       | 按比例扩展画面。                |
| 扩图优先级 3 | `left_offset`、`right_offset`、`top_offset`、`bottom_offset` | 在指定方向添加像素扩展画面。          |

## 参数设置建议

- **仅按宽高比扩图**：设置 `output_ratio` 为非空值（如 `"4:3"`）。
- **仅按比例扩图**：设置 `x_scale` 和 `y_scale`，至少一个大于 1.0。
- **仅在指定方向添加像素扩图**：设置 `left_offset`、`right_offset`、`top_offset`、`bottom_offset`，至少一个大于 0。
- **仅旋转图像**：设置 `angle` 为 \[1, 359] 之间的值。建议避免设置为 90、180、270 度。
- **先旋转再扩图**：设置 `angle` 的同时，搭配上述任一扩图模式的参数。

## 参数组合示例

<Accordion title="查看组合示例">
| 参数设置                                                               | 生效参数                     | 说明                              |
| ------------------------------------------------------------------ | ------------------------ | ------------------------------- |
| `output_ratio="4:3"`, `x_scale=2.0`                                | `output_ratio`           | `output_ratio` 优先级高于 `x_scale`。 |
| `x_scale=2.0`, `left_offset=100`                                   | `x_scale`                | `x_scale` 优先级高于 `left_offset`。  |
| `angle=90`, `x_scale=2.0`                                          | `angle` + `x_scale`      | 旋转与扩图叠加，两者均生效。                  |
| `angle=90`, `output_ratio="4:3"`, `x_scale=2.0`, `left_offset=100` | `angle` + `output_ratio` | 旋转与最高优先级扩图模式生效。                 |
</Accordion>

## 错误码

| HTTP 状态码 | 错误码                             | 错误信息                                                              | 说明                     |
| -------- | ------------------------------- | ----------------------------------------------------------------- | ---------------------- |
| 400      | InvalidParameter.JsonPhrase     | input json error                                                  | 输入 JSON 格式错误。          |
| 400      | InvalidParameter.FileDownload   | oss download error                                                | 输入图像下载失败，请检查 URL 是否有效。 |
| 400      | InvalidParameter.ImageFormat    | read image error                                                  | 读取图像失败，请检查图像格式。        |
| 400      | InvalidParameter.ImageContent   | The image content does not comply with green network verification | 图像内容不合规。               |
| 400      | InvalidParameter                | the parameters must conform to the specification: xxx             | 输入参数值超出范围。             |
| 400      | InvalidParameter.DataInspection | The image size is not supported for the data inspection.          | 输出图像尺寸超限（大于 10 MB）。    |
| 500      | InternalError.Algo              | algorithm process error                                           | 算法处理错误。                |
| 500      | InternalError.FileUpload        | oss upload error                                                  | 文件上传失败。                |

## FAQ

<Accordion title="创建任务接口响应成功，但没有返回图像 URL？">
  创建任务接口只返回 `task_id` 和 `task_status`。请使用[查询扩图结果](/api-reference/image-generation/image-out-painting/query-result)接口，通过 `task_id` 轮询获取生成结果。
</Accordion>

<Accordion title="设置 output_ratio 后，为什么模型没有根据 x_scale 或 y_scale 自动计算另一个方向的比例？">
  三种扩图方式（宽高比、比例缩放、方向偏移）是互斥的，存在优先级关系。`output_ratio` 优先级最高，设置后 `x_scale`/`y_scale` 和 `*_offset` 参数不生效。如需按比例扩图，请不要设置 `output_ratio`。
</Accordion>

## OpenAPI

````yaml post /services/aigc/image2image/out-painting
openapi: 3.1.0
info:
  title: Image Out-Painting API
  description: 图像画面扩展 API。支持旋转图像、等比例扩图、指定方向扩图、指定宽高比扩图。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: DashScope API
security:
  - BearerAuth: []
paths:
  /services/aigc/image2image/out-painting:
    post:
      operationId: createImageOutPainting
      summary: 创建扩图任务
      description: 创建图像画面扩展任务。支持旋转图像、等比例扩图、指定方向扩图、指定宽高比扩图。
      parameters:
        - name: X-DashScope-Async
          in: header
          required: true
          description: 开启异步处理，必须设为 `enable`。HTTP 调用仅支持异步方式，不设置此 Header 会返回错误。
          schema:
            type: string
            enum:
              - enable
            default: enable
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/ImageOutPaintingRequest"
      responses:
        "200":
          description: 任务提交成功。使用返回的 `task_id` 轮询任务结果。
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/AsyncTaskSubmitResponse"
              example:
                output:
                  task_status: PENDING
                  task_id: 0385dc79-5ff8-4d82-bcb6-xxxxxx
                request_id: 4909100c-7b5a-9f92-bfe5-xxxxxx
        "400":
          description: 请求参数错误。
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
              example:
                code: InvalidParameter
                message: Invalid request parameters.
                request_id: 7438d53d-6eb8-4596-8835-xxxxxx
        "401":
          description: 认证失败，API Key 无效。
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
              example:
                code: InvalidApiKey
                message: Invalid API-key provided.
                request_id: fb53c4ec-1c12-4fc4-a580-xxxxxx
      x-codeSamples:
        - lang: curl
          label: 旋转图像
          source: |-
            curl --location --request POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/out-painting' \
              --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
              --header 'X-DashScope-Async: enable' \
              --header 'Content-Type: application/json' \
              --data '{
              "model": "image-out-painting",
              "input": {
                "image_url": "http://xxx/image.jpg"
              },
              "parameters": {
                "angle": 45,
                "x_scale": 1.5,
                "y_scale": 1.5
              }
            }'
        - lang: curl
          label: 等比例扩图
          source: |-
            curl --location --request POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/out-painting' \
              --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
              --header 'X-DashScope-Async: enable' \
              --header 'Content-Type: application/json' \
              --data '{
              "model": "image-out-painting",
              "input": {
                "image_url": "http://xxx/image.jpg"
              },
              "parameters": {
                "x_scale": 2,
                "y_scale": 2,
                "best_quality": false,
                "limit_image_size": true
              }
            }'
        - lang: curl
          label: 指定方向扩图
          source: |-
            curl --location --request POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/out-painting' \
              --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
              --header 'X-DashScope-Async: enable' \
              --header 'Content-Type: application/json' \
              --data '{
              "model": "image-out-painting",
              "input": {
                "image_url": "http://xxx/image.jpg"
              },
              "parameters": {
                "left_offset": 200,
                "right_offset": 100,
                "best_quality": false,
                "limit_image_size": true
              }
            }'
        - lang: curl
          label: 指定宽高比扩图
          source: |-
            curl --location --request POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/out-painting' \
              --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
              --header 'X-DashScope-Async: enable' \
              --header 'Content-Type: application/json' \
              --data '{
              "model": "image-out-painting",
              "input": {
                "image_url": "http://xxx/image.jpg"
              },
              "parameters": {
                "angle": 0,
                "output_ratio": "4:3",
                "best_quality": false,
                "limit_image_size": true
              }
            }'
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    ImageOutPaintingRequest:
      type: object
      required:
        - model
        - input
        - parameters
      properties:
        model:
          type: string
          description: 模型名称。
          enum:
            - image-out-painting
          example: image-out-painting
        input:
          $ref: "#/components/schemas/OutPaintingInput"
        parameters:
          $ref: "#/components/schemas/OutPaintingParameters"
    OutPaintingInput:
      type: object
      required:
        - image_url
      description: 输入数据。
      properties:
        image_url:
          type: string
          description: |-
            待扩展图像的 URL。

            **图片限制：**
            - 支持格式：JPG、JPEG、PNG、HEIF、WEBP
            - 单边像素范围：512 ~ 4096
            - 文件大小：≤ 10 MB
          example: http://xxx/image.jpg
    OutPaintingParameters:
      type: object
      description: 扩图参数。支持四种扩图模式：旋转、宽高比、等比例缩放、指定方向偏移。存在优先级：`angle`（旋转） → `output_ratio`（宽高比） → `x_scale`/`y_scale`（等比例） → `*_offset`（方向偏移）。
      properties:
        angle:
          type: integer
          description: |-
            旋转角度，逆时针方向旋转。取值范围：0 ~ 359。默认值：0。

            旋转后系统自动扩展画面以填充因旋转产生的空白区域。建议避免设置为 90、180、270 度。
          default: 0
          minimum: 0
          maximum: 359
          example: 45
        output_ratio:
          type: string
          description: |-
            输出图像的宽高比。设置后，系统按照指定比例扩展画面。

            可选值：`""`（不使用）、`"1:1"`、`"3:4"`、`"4:3"`、`"9:16"`、`"16:9"`。默认值：`""`。
          default: ""
          enum:
            - ""
            - 1:1
            - 3:4
            - 4:3
            - 9:16
            - 16:9
          example: 4:3
        x_scale:
          type: number
          description: 水平方向缩放倍数。取值范围：1.0 ~ 3.0。默认值：1.0。
          default: 1
          minimum: 1
          maximum: 3
          example: 2
        y_scale:
          type: number
          description: 垂直方向缩放倍数。取值范围：1.0 ~ 3.0。默认值：1.0。
          default: 1
          minimum: 1
          maximum: 3
          example: 2
        top_offset:
          type: integer
          description: |-
            向上扩展的像素数。默认值：0。

            约束：`top_offset + bottom_offset` 必须小于原图高度的 3 倍。
          default: 0
          example: 0
        bottom_offset:
          type: integer
          description: |-
            向下扩展的像素数。默认值：0。

            约束：`top_offset + bottom_offset` 必须小于原图高度的 3 倍。
          default: 0
          example: 0
        left_offset:
          type: integer
          description: |-
            向左扩展的像素数。默认值：0。

            约束：`left_offset + right_offset` 必须小于原图宽度的 3 倍。
          default: 0
          example: 200
        right_offset:
          type: integer
          description: |-
            向右扩展的像素数。默认值：0。

            约束：`left_offset + right_offset` 必须小于原图宽度的 3 倍。
          default: 0
          example: 100
        best_quality:
          type: boolean
          description: 是否开启高质量模式。开启后生成质量更高，但耗时更长。默认值：`false`。
          default: false
          example: false
        limit_image_size:
          type: boolean
          description: 是否限制输出图像的尺寸。开启后，当输出图像尺寸超过原图尺寸时，系统会等比缩放到原图大小。默认值：`true`。
          default: true
          example: true
        add_watermark:
          type: boolean
          description: 是否在图像右下角添加水印。默认值：`true`。
          default: true
          example: true
    AsyncTaskSubmitResponse:
      type: object
      properties:
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID，有效期为 24 小时。
            task_status:
              type: string
              description: 任务状态。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - CANCELED
                - UNKNOWN
        request_id:
          type: string
          description: 请求唯一标识，用于排查问题。
    OutPaintingTaskStatusResponse:
      type: object
      properties:
        request_id:
          type: string
          description: 请求唯一标识，用于排查问题。
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID，有效期为 24 小时。
            task_status:
              type: string
              description: 任务状态。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - CANCELED
                - UNKNOWN
            submit_time:
              type: string
              description: 任务提交时间。UTC+8 时区，格式：`YYYY-MM-DD HH:mm:ss.SSS`。
            scheduled_time:
              type: string
              description: 任务开始执行时间。UTC+8 时区，格式：`YYYY-MM-DD HH:mm:ss.SSS`。
            end_time:
              type: string
              description: 任务完成时间。UTC+8 时区，格式：`YYYY-MM-DD HH:mm:ss.SSS`。
            output_image_url:
              type: string
              description: 生成的图片 URL。有效期为 24 小时，请及时下载保存。仅在任务成功时返回。
            task_metrics:
              type: object
              description: 任务统计信息。
              properties:
                TOTAL:
                  type: integer
                  description: 总任务数。
                SUCCEEDED:
                  type: integer
                  description: 成功数。
                FAILED:
                  type: integer
                  description: 失败数。
            code:
              type: string
              description: 错误码。仅在任务失败时返回。
            message:
              type: string
              description: 错误详情。仅在任务失败时返回。
        usage:
          type: object
          description: 用量统计，仅统计成功的结果。
          properties:
            image_count:
              type: integer
              description: 成功生成的图像数量。计费公式：费用 = 图像数量 × 单价。
    DashScopeErrorResponse:
      type: object
      properties:
        code:
          type: string
          description: 错误码。
        message:
          type: string
          description: 错误详情。
        request_id:
          type: string
          description: 请求唯一标识，用于排查问题。
````

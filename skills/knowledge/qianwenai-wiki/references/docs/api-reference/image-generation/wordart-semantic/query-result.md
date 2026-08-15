> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 文字变形 — 查询结果

> 查询文字变形任务状态

查询任务状态并获取生成的文字变形图片。

## 轮询策略

1. 通过[提交文字变形任务](/api-reference/image-generation/wordart-semantic/create-task)接口提交任务，获取 `task_id`。
2. 每 **5 秒**轮询一次，直到 `task_status` 为 `SUCCEEDED` 或 `FAILED`。
3. 任务成功后，从 `results` 中获取 `png_url` 和 `svg_url`。

## 响应字段说明

任务成功后，`results` 数组中每个元素包含以下字段：

| 字段        | 说明                      |
| --------- | ----------------------- |
| `png_url` | 生成的 PNG 格式图片 URL        |
| `svg_url` | 生成的 SVG 格式图片 URL        |
| `code`    | 单张图片的错误码（仅在该图片生成失败时返回）  |
| `message` | 单张图片的错误信息（仅在该图片生成失败时返回） |

## 注意事项

- **部分失败**：当 `n > 1` 时，部分图片可能因内容安全审核未通过而失败，此时对应元素返回 `code` 和 `message`，其余图片正常返回。
- **URL 有效期**：生成的图片 URL 有效期为 **24 小时**，请及时下载。
- **任务状态流转**：`PENDING` → `RUNNING` → `SUCCEEDED`、`FAILED` 或 `UNKNOWN`。
- **任务 ID 有效期**：`task_id` 有效期为 24 小时，过期后无法查询状态和结果。

## OpenAPI

````yaml get /tasks/{task_id}
openapi: 3.1.0
info:
  title: WordArt Semantic API
  version: 1.0.0
  description: WordArt 锦书-文字变形 API
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: DashScope
security:
  - BearerAuth: []
paths:
  /tasks/{task_id}:
    get:
      summary: 查询文字变形结果
      operationId: getWordArtSemanticTaskResult
      parameters:
        - name: task_id
          in: path
          required: true
          schema:
            type: string
          description: 任务 ID，由[提交文字变形任务](/api-reference/image-generation/wordart-semantic/create-task)接口返回。
      responses:
        "200":
          description: 任务状态查询结果
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/TaskStatusResponse"
              examples:
                SUCCEEDED:
                  summary: 任务成功
                  value:
                    request_id: 7574ee8f-38a3-4b1e-9280-11c33ab46e51
                    output:
                      task_id: a8532587-fa8c-4ef8-82be-0c46b17950d1
                      task_status: SUCCEEDED
                      results:
                        - png_url: https://xxx/1.png
                          svg_url: https://xxx/1.svg
                        - png_url: https://xxx/2.png
                          svg_url: https://xxx/2.svg
                        - code: DataInspectionFailed
                          message: The output image may contain inappropriate content.
                        - png_url: https://xxx/4.png
                          svg_url: https://xxx/4.svg
                    usage:
                      image_count: 3
                FAILED:
                  summary: 任务失败
                  value:
                    request_id: 7574ee8f-38a3-4b1e-9280-11c33ab46e51
                    output:
                      task_id: a8532587-fa8c-4ef8-82be-0c46b17950d1
                      task_status: FAILED
                      code: xxx
                      message: xxxxxx
                RUNNING:
                  summary: 任务运行中
                  value:
                    request_id: e5d70b02-ebd3-98ce-9fe8-759d7d7b107d
                    output:
                      task_id: 86ecf553-d340-4e21-af6e-a0c6a421c010
                      task_status: RUNNING
                      task_metrics:
                        TOTAL: 2
                        SUCCEEDED: 0
                        FAILED: 0
                PENDING:
                  summary: 任务排队中
                  value:
                    request_id: 7574ee8f-38a3-4b1e-9280-11c33ab46e51
                    output:
                      task_id: a8532587-fa8c-4ef8-82be-0c46b17950d1
                      task_status: PENDING
      x-codeSamples:
        - lang: curl
          label: 查询任务结果
          source: |-
            curl -X GET \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    WordArtSemanticRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          enum:
            - wordart-semantic
          description: 模型名称。
        input:
          type: object
          required:
            - text
            - prompt
          description: 输入参数。
          properties:
            text:
              type: string
              description: 用户输入的文字内容。
            prompt:
              type: string
              maxLength: 200
              description: 描述提示词，1-200 个字。用于描述文字变形的风格和元素。
        parameters:
          type: object
          description: 模型参数。
          properties:
            n:
              type: integer
              minimum: 1
              maximum: 4
              default: 4
              description: 生成的图片数量，取值范围 1~4，默认 4。
            steps:
              type: integer
              minimum: 10
              maximum: 100
              default: 30
              description: 变形迭代次数，数字越大文字变化程度越大。取值范围 10~100，默认 30。
            font_name:
              type: string
              enum:
                - dongfangdakai
                - puhuiti_m
                - shuheiti
                - jinbuti
                - kuheiti
                - kuaileti
                - wenyiti
                - logoti
                - cangeryuyangti_m
                - siyuansongti_b
                - siyuanheiti_m
                - fangzhengkaiti
              description: 字体类型。不指定则使用默认字体（方正楷体）。与 `ttf_url` 不能同时使用。
            ttf_url:
              type: string
              description: 自定义 TTF 字体文件 URL，文件大小需小于 30 MB。与 `font_name` 不能同时使用。
            output_image_ratio:
              type: string
              enum:
                - 1280x720
                - 720x1280
                - 1024x1024
              default: 1280x720
              description: 输出图片比例。默认 `1280x720`。
    AsyncTaskSubmitResponse:
      type: object
      properties:
        request_id:
          type: string
          description: 请求唯一标识。
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID，用于查询任务状态和结果。
            task_status:
              type: string
              enum:
                - PENDING
              description: 任务状态。
    TaskStatusResponse:
      type: object
      properties:
        request_id:
          type: string
          description: 请求唯一标识。
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID。
            task_status:
              type: string
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - UNKNOWN
              description: 任务状态。
            results:
              type: array
              items:
                type: object
                properties:
                  png_url:
                    type: string
                    description: 生成的 PNG 格式图片 URL。
                  svg_url:
                    type: string
                    description: 生成的 SVG 格式图片 URL。
                  code:
                    type: string
                    description: 单张图片的错误码（仅在该图片生成失败时返回）。
                  message:
                    type: string
                    description: 单张图片的错误信息（仅在该图片生成失败时返回）。
              description: 生成结果列表，每个元素包含 `png_url` 和 `svg_url`。部分图片可能因内容安全审核失败，此时返回 `code` 和 `message`。
            task_metrics:
              type: object
              properties:
                TOTAL:
                  type: integer
                  description: 总任务数。
                SUCCEEDED:
                  type: integer
                  description: 成功任务数。
                FAILED:
                  type: integer
                  description: 失败任务数。
            code:
              type: string
              description: 错误码（仅在任务失败时返回）。
            message:
              type: string
              description: 错误信息（仅在任务失败时返回）。
        usage:
          type: object
          properties:
            image_count:
              type: integer
              description: 生成的图片数量。
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

> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 文字变形 — 创建任务

> 提交文字变形异步任务

<Note>
  请先[获取 API Key](/api-reference/preparation/api-key) 并[设置为环境变量](/api-reference/preparation/export-api-key-env)。
</Note>

## 模型信息

| 模型                 | 描述                         |
| ------------------ | -------------------------- |
| `wordart-semantic` | 文字变形模型，根据提示词对文字边缘轮廓进行语义化变形 |

## 输出说明

模型生成的图片为**黑底白色蒙版**，包含 PNG 和 SVG 两种格式。

## 字体列表

通过 `font_name` 参数指定预设字体，或通过 `ttf_url` 参数传入自定义字体文件（两者不可同时使用）。

| 参数值                | 字体名称     |
| ------------------ | -------- |
| `dongfangdakai`    | 东方大楷     |
| `puhuiti_m`        | 普惠体      |
| `shuheiti`         | 书黑体      |
| `jinbuti`          | 金簿体      |
| `kuheiti`          | 酷黑体      |
| `kuaileti`         | 快乐体      |
| `wenyiti`          | 文艺体      |
| `logoti`           | Logo体    |
| `cangeryuyangti_m` | 仓耳渔阳体    |
| `siyuansongti_b`   | 思源宋体     |
| `siyuanheiti_m`    | 思源黑体     |
| `fangzhengkaiti`   | 方正楷体（默认） |

## OpenAPI

````yaml post /services/aigc/wordart/semantic
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
  /services/aigc/wordart/semantic:
    post:
      summary: 提交文字变形任务
      operationId: createWordArtSemanticTask
      parameters:
        - name: X-DashScope-Async
          in: header
          required: true
          schema:
            type: string
            enum:
              - enable
          description: 启用异步模式。
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/WordArtSemanticRequest"
      responses:
        "200":
          description: 任务提交成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/AsyncTaskSubmitResponse"
        "400":
          description: 请求错误
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
      x-codeSamples:
        - lang: curl
          label: 提交文字变形任务
          source: |-
            curl --location --request POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/wordart/semantic' \
            --header 'X-DashScope-Async: enable' \
            --header 'Content-Type: application/json' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --data-raw '{
                "model": "wordart-semantic",
                "input": {
                    "text": "文字创意",
                    "prompt": "水果，蔬菜，温暖的色彩空间"
                },
                "parameters": {
                    "steps": 80,
                    "n": 2,
                    "output_image_ratio": "1024x1024",
                    "font_name": "dongfangdakai"
                }
            }'
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

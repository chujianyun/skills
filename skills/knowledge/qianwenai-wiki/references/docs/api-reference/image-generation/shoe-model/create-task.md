> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 鞋靴模特 — 创建任务

> 异步鞋靴模特图像生成

<Note>
  请先[获取 API Key](/api-reference/preparation/api-key) 并[设置为环境变量](/api-reference/preparation/export-api-key-env)。
</Note>

上传模特模板图和鞋靴商品图，自动生成模特上脚效果图。支持多角度鞋靴图片输入（最多3张），可批量生成多张结果图。

## 前提条件

鞋靴模特为免费试用服务。免费额度详情请参见[免费额度](/resources/free-quota)，限流信息请在[控制台](https://platform.qianwenai.com/home/benefits)查看。

## OpenAPI

````yaml post /services/aigc/virtualmodel/generation
openapi: 3.1.0
info:
  title: 鞋靴模特 API
  description: AI 鞋靴模特上脚效果图生成。上传模特模板图和鞋靴商品图，自动生成模特上脚效果图。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 华北2（北京）
security:
  - BearerAuth: []
paths:
  /services/aigc/virtualmodel/generation:
    post:
      summary: 创建鞋靴模特任务
      operationId: createShoeModelTask
      description: 提交鞋靴模特上脚效果图生成任务，返回任务 ID 用于轮询。
      parameters:
        - name: X-DashScope-Async
          in: header
          required: true
          description: 启用异步模式，必须设置为 `enable`。
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
              $ref: "#/components/schemas/ShoeModelRequest"
      responses:
        "200":
          description: 任务提交成功。
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/AsyncTaskSubmitResponse"
              example:
                output:
                  task_id: d76ec1e8-ea27-4038-8913-xxxxxxxxxxxx
                  task_status: PENDING
                request_id: 7574ee8f-38a3-4b1e-9280-11c33ab46e51
        "400":
          description: 请求无效。
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
              example:
                code: InvalidApiKey
                message: Invalid API-key provided.
                request_id: fb53c4ec-1c12-4fc4-a580-cdb7c3261fc1
      x-codeSamples:
        - lang: curl
          label: curl
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/virtualmodel/generation' \
            --header 'X-DashScope-Async: enable' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --header 'Content-Type: application/json' \
            --data '{
              "model": "shoemodel-v1",
              "input": {
                "template_image_url": "https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8268778171/p809310.webp",
                "shoe_image_url": ["https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8268778171/p809301.webp"]
              },
              "parameters": {
                "n": 1
              }
            }'
components:
  schemas:
    ShoeModelRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 调用的模型名称，固定为 `shoemodel-v1`。
          enum:
            - shoemodel-v1
          example: shoemodel-v1
        input:
          $ref: "#/components/schemas/ShoeModelInput"
        parameters:
          $ref: "#/components/schemas/ShoeModelParameters"
    ShoeModelInput:
      type: object
      required:
        - template_image_url
        - shoe_image_url
      description: 输入图片。
      properties:
        template_image_url:
          type: string
          description: |-
            模特模板图的 URL 地址，须为可公开访问的 HTTP/HTTPS 地址。

            图片要求：
            - 大小：< 5 MB
            - 格式：jpg、png、jpeg、bmp、webp、avif
            - 宽高比：介于 2:3 与 3:2 之间（推荐 4:3）
          example: https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8268778171/p809310.webp
        shoe_image_url:
          type: array
          items:
            type: string
          maxItems: 3
          description: |-
            多角度鞋靴商品图的 URL 列表，最多 3 张，须为可公开访问的 HTTP/HTTPS 地址。

            图片要求：
            - 大小：< 5 MB
            - 格式：jpg、png、jpeg、bmp、webp、avif
            - 宽高比：介于 2:3 与 3:2 之间（推荐 4:3，与模板图保持一致）
          example:
            - https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8268778171/p809301.webp
    ShoeModelParameters:
      type: object
      description: 生成参数。
      properties:
        n:
          type: integer
          minimum: 1
          maximum: 4
          default: 1
          description: 生成图片数量，取值范围：1~4。
          example: 1
        scale:
          type: number
          format: float
          minimum: 2
          maximum: 8
          default: 5
          description: 生成强度，取值范围：[2.0, 8.0]。值越大，颜色越鲜艳。
          example: 5
    AsyncTaskSubmitResponse:
      type: object
      description: 任务提交响应。
      properties:
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID，用于轮询任务状态。
            task_status:
              type: string
              description: 任务状态。
              enum:
                - PENDING
        request_id:
          type: string
          description: 请求唯一标识，可用于问题排查。
    ShoeModelTaskStatusResponse:
      type: object
      description: 任务状态响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识，可用于问题排查。
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID。
            task_status:
              type: string
              description: 任务状态：`PENDING`（排队中）、`RUNNING`（处理中）、`SUCCEEDED`（成功）、`FAILED`（失败）、`CANCELED`（已取消）、`UNKNOWN`（task_id 无效或已过期）。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - SUSPENDED
                - CANCELED
                - UNKNOWN
            submit_time:
              type: string
              description: 任务提交时间。
            scheduled_time:
              type: string
              description: 任务调度时间。
            end_time:
              type: string
              description: 任务完成时间。
            results:
              type: array
              description: 生成的图片列表，每项包含 `url` 字段。
              items:
                type: object
                properties:
                  url:
                    type: string
                    description: 生成图片的下载 URL，24 小时后过期。
            task_metrics:
              type: object
              description: 任务统计信息。
              properties:
                TOTAL:
                  type: integer
                  description: 任务总数。
                SUCCEEDED:
                  type: integer
                  description: 成功数量。
                FAILED:
                  type: integer
                  description: 失败数量。
            code:
              type: string
              description: 错误码（仅任务失败时存在）。
            message:
              type: string
              description: 错误信息（仅任务失败时存在）。
        usage:
          type: object
          description: 用量统计。
          properties:
            image_count:
              type: integer
              description: 本次生成的图片数量。
    DashScopeErrorResponse:
      type: object
      description: 错误响应。
      properties:
        code:
          type: string
          description: 错误码。
        message:
          type: string
          description: 错误信息。
        request_id:
          type: string
          description: 请求唯一标识，可用于问题排查。
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
````

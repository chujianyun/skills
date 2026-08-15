> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 鞋靴模特 — 查询结果

> 查询鞋靴模特图像生成任务状态

<Note>
  请先[获取 API Key](/api-reference/preparation/api-key) 并[设置为环境变量](/api-reference/preparation/export-api-key-env)。
</Note>

查询任务状态和结果。

## 轮询策略

1. 通过[创建任务](/api-reference/image-generation/shoe-model/create-task)接口提交请求，获取 `task_id`。
2. 每 **10 秒**轮询一次，直到 `task_status` 为 `SUCCEEDED` 或 `FAILED`。
3. 任务成功后，`results` 中包含图片下载 URL。

## 注意事项

- **URL 有效期**：图片 URL 在 **24 小时**后过期，请及时下载。
- **任务状态流转**：`PENDING` → `RUNNING` → `SUCCEEDED` 或 `FAILED`。
- **其他状态**：`SUSPENDED`（任务已暂停）、`CANCELED`（任务已取消）、`UNKNOWN`（`task_id` 无效或已过期）。
- **`task_id` 有效期**：`task_id` 有效期为 **24 小时**，过期后无法查询任务状态和结果。
- **避免重复提交**：请通过轮询获取结果，不要重复提交请求。
- **部分失败**：当 `n > 1` 时，只要有一张图片生成成功，任务状态即为 `SUCCEEDED`。失败的图片会在 `results` 中包含错误详情，仅成功的图片计入用量。

## OpenAPI

````yaml get /tasks/{task_id}
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
  /tasks/{task_id}:
    get:
      summary: 查询鞋靴模特任务
      operationId: getShoeModelTaskResult
      description: 查询鞋靴模特上脚效果图生成任务的状态和结果。
      parameters:
        - name: task_id
          in: path
          required: true
          description: 创建任务接口返回的任务 ID。
          schema:
            type: string
      responses:
        "200":
          description: 任务状态和结果。
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ShoeModelTaskStatusResponse"
              examples:
                SUCCEEDED:
                  summary: SUCCEEDED
                  value:
                    request_id: e5d70b02-ebd3-98ce-9fe8-759d7d7b107d
                    output:
                      task_id: 86ecf553-d340-4e21-af6e-a0c6a421c010
                      task_status: SUCCEEDED
                      submit_time: 2024-05-16 13:50:00.000
                      scheduled_time: 2024-05-16 13:50:01.000
                      end_time: 2024-05-16 13:50:30.000
                      results:
                        - url: https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx/res_img.png?Expires=xxx&OSSAccessKeyId=xxx&Signature=xxx
                      task_metrics:
                        TOTAL: 1
                        SUCCEEDED: 1
                        FAILED: 0
                    usage:
                      image_count: 1
                RUNNING:
                  summary: RUNNING
                  value:
                    request_id: e5d70b02-ebd3-98ce-9fe8-759d7d7b107d
                    output:
                      task_id: 86ecf553-d340-4e21-af6e-a0c6a421c010
                      task_status: RUNNING
                      task_metrics:
                        TOTAL: 1
                        SUCCEEDED: 0
                        FAILED: 0
                FAILED:
                  summary: FAILED
                  value:
                    request_id: e5d70b02-ebd3-98ce-9fe8-759d7d7b107d
                    output:
                      task_id: 86ecf553-d340-4e21-af6e-a0c6a421c010
                      task_status: FAILED
                      submit_time: 2024-05-16 13:50:00.000
                      scheduled_time: 2024-05-16 13:50:01.000
                      end_time: 2024-05-16 13:50:30.000
                      code: InvalidFile.Resolution
                      message: The image resolution is invalid, please make sure that the aspect ratio is smaller than 3:2, and largest length of image is smaller than 4096.
                    usage:
                      image_count: 0
      x-codeSamples:
        - lang: curl
          label: curl
          source: |-
            curl --location --request GET 'https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY"
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

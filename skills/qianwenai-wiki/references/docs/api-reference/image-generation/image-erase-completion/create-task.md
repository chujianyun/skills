> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 图像擦除补全 — 创建任务

> 异步提交图像擦除补全任务

## OpenAPI

````yaml post /services/aigc/image2image/image-synthesis
openapi: 3.1.0
info:
  title: 图像擦除补全 API
  description: 图像擦除补全（image-erase-completion）API，可根据mask区域对原图进行擦除补全。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: DashScope API (Beijing)
paths:
  /services/aigc/image2image/image-synthesis:
    post:
      operationId: createImageEraseCompletion
      summary: 创建擦除补全任务
      description: 提交一个异步图像擦除补全任务。需要设置 `X-DashScope-Async` header 为 `enable`。
      parameters:
        - name: X-DashScope-Async
          in: header
          required: true
          schema:
            type: string
            enum:
              - enable
            default: enable
          description: 必须设置为 `enable`，表示使用异步方式提交任务。
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/ImageEraseCompletionRequest"
      responses:
        "200":
          description: 任务提交成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/AsyncTaskSubmitResponse"
              example:
                output:
                  task_status: PENDING
                  task_id: 53950fb7-281a-4e60-b543-xxxxxxxxxxxx
                request_id: 7574ee8f-38a3-4b1e-9280-11c33ab46e51
        "400":
          description: 请求参数错误
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
              example:
                code: InvalidParameter
                message: The model is not supported.
                request_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        "401":
          description: 认证失败
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
              example:
                code: InvalidApiKey
                message: Invalid API-key provided.
                request_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
      x-codeSamples:
        - lang: curl
          label: curl
          source: |-
            curl --location --request POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
            --header 'X-DashScope-Async: enable' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --header 'Content-Type: application/json' \
            --data-raw '{
                "model": "image-erase-completion",
                "input": {
                        "image_url": "http://xxx/input.png",
                        "mask_url": "http://xxx/mask.png",
                        "foreground_url": "http://xxx/foreground.png"
                    },
                "parameters":{
                    "dilate_flag":true
                }
            }'
      security:
        - BearerAuth: []
components:
  schemas:
    ImageEraseCompletionRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          enum:
            - image-erase-completion
          description: 模型名称，固定值为 `image-erase-completion`。
        input:
          $ref: "#/components/schemas/ImageEraseCompletionInput"
        parameters:
          $ref: "#/components/schemas/ImageEraseCompletionParameters"
    ImageEraseCompletionInput:
      type: object
      required:
        - image_url
        - mask_url
      properties:
        image_url:
          type: string
          description: 待擦除处理的输入图片的URL链接。图片格式支持JPEG、PNG、JPG、BMP、WEBP，图片分辨率在512×512~4096×4096之间，文件大小不超过10MB。
        mask_url:
          type: string
          description: 蒙版图片的URL链接。蒙版区域为白色，保留区域为黑色。图片格式支持JPEG、PNG、JPG、BMP、WEBP，图片分辨率在512×512~4096×4096之间，文件大小不超过10MB。
        foreground_url:
          type: string
          description: 前景图片的URL链接。指定前景，可避免擦除结果改变前景。图片格式支持JPEG、PNG、JPG、BMP、WEBP，图片分辨率在512×512~4096×4096之间，文件大小不超过10MB。
    ImageEraseCompletionParameters:
      type: object
      properties:
        fast_mode:
          type: boolean
          default: false
          description: 是否使用快速模式，开启后可加快推理速度。默认值为false。
        dilate_flag:
          type: boolean
          default: true
          description: 是否使用mask扩展功能。开启后，将对mask进行自动扩展来增强擦除效果。默认值为true。
        add_watermark:
          type: boolean
          default: true
          description: 是否添加水印。默认值为true。添加的水印不影响图像质量。
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
              description: 任务ID，用于后续查询任务状态和结果。
            task_status:
              type: string
              enum:
                - PENDING
              description: 任务状态，提交成功时为 PENDING。
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
              description: 任务ID。
            task_status:
              type: string
              enum:
                - PENDING
                - RUNNING
                - SUSPENDED
                - SUCCEEDED
                - FAILED
              description: 任务状态。
            submit_time:
              type: string
              description: 任务提交时间。
            scheduled_time:
              type: string
              description: 任务调度时间。
            end_time:
              type: string
              description: 任务结束时间。
            output_image_url:
              type: string
              description: 擦除补全后的结果图片URL。仅在任务成功时返回。URL有效期为24小时。
            task_metrics:
              type: object
              properties:
                TOTAL:
                  type: integer
                  description: 总任务数。
                SUCCEEDED:
                  type: integer
                  description: 成功的任务数。
                FAILED:
                  type: integer
                  description: 失败的任务数。
              description: 任务的执行指标。
            code:
              type: string
              description: 错误码，仅在任务失败时返回。
            message:
              type: string
              description: 错误信息，仅在任务失败时返回。
        usage:
          type: object
          properties:
            image_count:
              type: integer
              description: 生成的图片数量。
          description: 计量信息。仅在任务成功时返回。
    ErrorResponse:
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
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
````

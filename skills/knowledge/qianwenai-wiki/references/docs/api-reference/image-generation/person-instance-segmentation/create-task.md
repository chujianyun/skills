> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 人物实例分割 — 创建任务

> 提交人物实例分割任务

<Note>
  请先[获取 API Key](/api-reference/preparation/api-key) 并[设置为环境变量](/api-reference/preparation/export-api-key-env)。
</Note>

## OpenAPI

````yaml post /services/aigc/image2image/image-synthesis
openapi: 3.1.0
info:
  title: Person Instance Segmentation API
  description: 人物实例分割 API。对输入图像中的每个人物实例进行分割，输出每个实例的分割掩码图像和可视化结果。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: Beijing
security:
  - BearerAuth: []
paths:
  /services/aigc/image2image/image-synthesis:
    post:
      operationId: createPersonInstanceSegmentationTask
      summary: 提交人物实例分割任务
      description: 提交异步人物实例分割任务。API 立即返回 `task_id`，通过 `GET /tasks/{task_id}` 轮询获取结果。
      parameters:
        - name: X-DashScope-Async
          in: header
          required: true
          description: 异步任务提交标识，必须设置为 `enable`。
          schema:
            type: string
            enum:
              - enable
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/PersonInstanceSegmentationRequest"
      responses:
        "200":
          description: 任务提交成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/AsyncTaskSubmitResponse"
              examples:
                success:
                  summary: 任务已接收
                  value:
                    output:
                      task_status: PENDING
                      task_id: 53950fb7-281a-4e60-xxxxxxxxxxxx
                    request_id: 4909100c-7b5a-9f92-bfe5-28c7cece6b47
        "400":
          description: 请求参数无效
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
              examples:
                InvalidParameter.JsonPhrase:
                  summary: JSON 解析错误
                  value:
                    request_id: a4d78a5f-655f-9639-8437-xxxxxx
                    code: InvalidParameter.JsonPhrase
                    message: input json error
                InvalidParameter.FileDownload:
                  summary: 图像下载失败
                  value:
                    request_id: a4d78a5f-655f-9639-8437-xxxxxx
                    code: InvalidParameter.FileDownload
                    message: oss download error
                InvalidParameter.ImageFormat:
                  summary: 图像格式错误
                  value:
                    request_id: a4d78a5f-655f-9639-8437-xxxxxx
                    code: InvalidParameter.ImageFormat
                    message: read image error
                InvalidParameter.ImageContent:
                  summary: 图像内容不合规
                  value:
                    request_id: a4d78a5f-655f-9639-8437-xxxxxx
                    code: InvalidParameter.ImageContent
                    message: The image content does not comply with green network verification
                InvalidParameter:
                  summary: 参数超出范围
                  value:
                    request_id: a4d78a5f-655f-9639-8437-xxxxxx
                    code: InvalidParameter
                    message: "the parameters must conform to the specification: xxx"
        "401":
          description: 认证失败 — API Key 无效或缺失
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
        "429":
          description: 超出速率限制
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
        "500":
          description: 服务端内部错误
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
              examples:
                InternalError.Algo:
                  summary: 算法处理错误
                  value:
                    request_id: a4d78a5f-655f-9639-8437-xxxxxx
                    code: InternalError.Algo
                    message: algorithm process error
                InternalError.FileUpload:
                  summary: 文件上传失败
                  value:
                    request_id: a4d78a5f-655f-9639-8437-xxxxxx
                    code: InternalError.FileUpload
                    message: oss upload error
      x-codeSamples:
        - lang: curl
          label: cURL
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
            --header 'X-DashScope-Async: enable' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --header 'Content-Type: application/json' \
            --data '{
              "model": "image-instance-segmentation",
              "input": {
                "image_url": "http://xxx/image.png"
              },
              "parameters": {}
            }'
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    PersonInstanceSegmentationRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称，固定为 `image-instance-segmentation`。
          enum:
            - image-instance-segmentation
          example: image-instance-segmentation
        input:
          type: object
          required:
            - image_url
          description: 输入图像参数。
          properties:
            image_url:
              type: string
              format: uri
              description: |-
                待分割图像的公网可访问 URL。URL 中不能包含中文字符。

                - **格式**：JPEG、PNG、JPG、BMP、WEBP
                - **分辨率**：宽和高必须在 512 到 4096 像素之间
                - **文件大小**：不超过 10 MB
              example: http://xxx/image.png
        parameters:
          type: object
          description: 生成参数。当前无可用参数，传空对象 `{}` 即可。
          properties: {}
    AsyncTaskSubmitResponse:
      type: object
      description: 异步任务提交响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识符，用于链路追踪和问题排查。
          example: 4909100c-7b5a-9f92-bfe5-28c7cece6b47
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID，用于通过 `GET /tasks/{task_id}` 轮询任务状态。有效期 24 小时。
              example: 53950fb7-281a-4e60-xxxxxxxxxxxx
            task_status:
              type: string
              description: 初始任务状态，通常为 `PENDING`。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - SUSPENDED
                - UNKNOWN
    TaskStatusResponse:
      type: object
      description: 任务状态查询响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识符，用于链路追踪和问题排查。
          example: b67df059-ca6a-9d51-afcd-9b3c4456b1e2
        output:
          type: object
          description: 任务输出信息。
          properties:
            task_id:
              type: string
              description: 任务 ID。
              example: 53950fb7-281a-4e60-xxxxxxxxxxxx
            task_status:
              type: string
              description: 当前任务状态。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - SUSPENDED
                - UNKNOWN
            submit_time:
              type: string
              description: 任务提交时间。UTC+8，格式：`YYYY-MM-DD HH:mm:ss.SSS`。
              example: 2024-05-16 13:50:01.247
            scheduled_time:
              type: string
              description: 任务开始执行时间。UTC+8，格式：`YYYY-MM-DD HH:mm:ss.SSS`。
              example: 2024-05-16 13:50:01.354
            end_time:
              type: string
              description: 任务完成时间。UTC+8，格式：`YYYY-MM-DD HH:mm:ss.SSS`。
              example: 2024-05-16 13:50:27.795
            output_image_url:
              type: string
              format: uri
              description: |-
                分割掩码图像 URL。仅在 `task_status` 为 `SUCCEEDED` 时返回。**有效期 24 小时**，请及时下载。

                掩码图像中，每个人物实例用不同灰度值（1, 2, 3...）表示，背景为 0。
              example: http://xxx/result1.png
            output_vis_image_url:
              type: string
              format: uri
              description: |-
                可视化结果图像 URL。仅在 `task_status` 为 `SUCCEEDED` 时返回。**有效期 24 小时**，请及时下载。

                可视化图像中，不同人物实例用不同颜色叠加显示在原图上。
              example: http://xxx/result2.png
            code:
              type: string
              description: 错误码。仅在 `task_status` 为 `FAILED` 时返回。
              example: InvalidParameter.FileDownload
            message:
              type: string
              description: 错误详细信息。仅在 `task_status` 为 `FAILED` 时返回。
              example: download for input_image error
            task_metrics:
              type: object
              description: 任务完成指标。
              properties:
                TOTAL:
                  type: integer
                  description: 子任务总数。
                  example: 1
                SUCCEEDED:
                  type: integer
                  description: 成功的子任务数。
                  example: 1
                FAILED:
                  type: integer
                  description: 失败的子任务数。
                  example: 0
        usage:
          type: object
          description: 使用量统计。仅在任务成功时返回。
          properties:
            image_count:
              type: integer
              description: 处理的图像数量。
              example: 1
    DashScopeErrorResponse:
      type: object
      description: DashScope API 错误响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识符。
          example: a4d78a5f-655f-9639-8437-xxxxxx
        code:
          type: string
          description: 错误码。可能的值包括：`InvalidParameter.JsonPhrase`、`InvalidParameter.FileDownload`、`InvalidParameter.ImageFormat`、`InvalidParameter.ImageContent`、`InvalidParameter`、`InternalError.Algo`、`InternalError.FileUpload`。
          example: InvalidParameter
        message:
          type: string
          description: 错误描述信息。
          example: the parameters must conform to the specification
````

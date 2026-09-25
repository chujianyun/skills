> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 人物实例分割 — 查询结果

> 查询人物实例分割任务的状态和结果

<Note>
  请先[获取 API Key](/api-reference/preparation/api-key) 并[设置为环境变量](/api-reference/preparation/export-api-key-env)。
</Note>

## OpenAPI

````yaml get /tasks/{task_id}
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
  /tasks/{task_id}:
    get:
      operationId: getPersonInstanceSegmentationTaskStatus
      summary: 查询任务结果
      description: 轮询人物实例分割任务的状态和结果。持续轮询直到 `task_status` 为 `SUCCEEDED` 或 `FAILED`。结果中的图片 URL 有效期为 24 小时。
      parameters:
        - name: task_id
          in: path
          required: true
          description: 由 `POST /services/aigc/image2image/image-synthesis` 接口返回的任务 ID。
          schema:
            type: string
          example: 53950fb7-281a-4e60-xxxxxxxxxxxx
      responses:
        "200":
          description: 成功获取任务状态
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/TaskStatusResponse"
              examples:
                SUCCEEDED:
                  summary: 任务成功
                  value:
                    request_id: b67df059-ca6a-9d51-afcd-9b3c4456b1e2
                    output:
                      task_id: 53950fb7-281a-4e60-xxxxxxxxxxxx
                      task_status: SUCCEEDED
                      submit_time: 2024-05-16 13:50:01.247
                      scheduled_time: 2024-05-16 13:50:01.354
                      end_time: 2024-05-16 13:50:27.795
                      output_image_url: http://xxx/result1.png
                      output_vis_image_url: http://xxx/result2.png
                    usage:
                      image_count: 1
                FAILED:
                  summary: 任务失败
                  value:
                    request_id: dccfdf23-b38e-97a6-a07b-f35118c1ada6
                    output:
                      task_id: 53950fb7-281a-4e60-xxxxxxxxxxxx
                      task_status: FAILED
                      submit_time: 2024-05-16 14:15:14.103
                      scheduled_time: 2024-05-16 14:15:14.154
                      end_time: 2024-05-16 14:15:14.694
                      code: InvalidParameter.FileDownload
                      message: download for input_image error
                RUNNING:
                  summary: 任务运行中
                  value:
                    request_id: 7574ee8f-38a3-4b1e-xxxxxxxxxxxx
                    output:
                      task_id: 53950fb7-281a-4e60-xxxxxxxxxxxx
                      task_status: RUNNING
                      task_metrics:
                        TOTAL: 1
                        SUCCEEDED: 1
                        FAILED: 0
        "400":
          description: 请求参数无效
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
      x-codeSamples:
        - lang: curl
          label: cURL — 查询任务结果
          source: |-
            # 将 {task_id} 替换为提交任务时返回的实际任务 ID
            curl -X GET 'https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY"
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

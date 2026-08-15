> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 图像画面扩展 — 查询结果

> 查询图像画面扩展任务状态

查询任务状态和结果。

## 轮询策略

1. 通过[创建扩图任务](/api-reference/image-generation/image-out-painting/create-task)接口提交请求，获取 `task_id`。
2. 每 **10 秒**轮询一次，直到 `task_status` 为 `SUCCEEDED` 或 `FAILED`。
3. 任务成功后，`output_image_url` 中包含图片下载 URL。

## 注意事项

- **URL 有效期**：图片 URL 在 **24 小时**后过期，请及时下载。
- **任务状态流转**：`PENDING` → `RUNNING` → `SUCCEEDED` 或 `FAILED`。
- **其他状态**：`CANCELED`（任务已取消）、`UNKNOWN`（`task_id` 无效或已过期）。
- **`task_id` 有效期**：`task_id` 有效期为 **24 小时**，过期后无法查询任务状态和结果。
- **避免重复提交**：请通过轮询获取结果，不要重复提交请求。

## OpenAPI

````yaml get /tasks/{task_id}
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
  /tasks/{task_id}:
    get:
      operationId: getImageOutPaintingTaskStatus
      summary: 查询扩图结果
      description: 查询图像画面扩展任务的状态和结果。
      parameters:
        - name: task_id
          in: path
          required: true
          description: 创建扩图任务时返回的任务 ID。
          schema:
            type: string
      responses:
        "200":
          description: 任务状态查询成功。
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/OutPaintingTaskStatusResponse"
              examples:
                SUCCEEDED:
                  summary: 任务成功
                  value:
                    request_id: b67df059-ca6a-9d51-afcd-9b3c4456b1e2
                    output:
                      task_id: d76ec1e8-ea27-4038-8913-235c88ef0f70
                      task_status: SUCCEEDED
                      submit_time: 2024-05-16 13:50:01.247
                      scheduled_time: 2024-05-16 13:50:01.354
                      end_time: 2024-05-16 13:50:27.795
                      output_image_url: https://xxxx/xxxx
                    usage:
                      image_count: 1
                FAILED:
                  summary: 任务失败
                  value:
                    request_id: dccfdf23-b38e-97a6-a07b-f35118c1ada6
                    output:
                      task_id: 4cbabbdf-2c1f-43f4-b983-c2cc47f4c115
                      task_status: FAILED
                      submit_time: 2024-05-16 14:15:14.103
                      scheduled_time: 2024-05-16 14:15:14.154
                      end_time: 2024-05-16 14:15:14.694
                      code: InvalidParameter.FileDownload
                      message: download for input_image error
                RUNNING:
                  summary: 任务运行中
                  value:
                    request_id: e5d70b02-ebd3-98ce-9fe8-759d7d7b107d
                    output:
                      task_id: d76ec1e8-ea27-4038-8913-235c88ef0f70
                      task_status: RUNNING
                      task_metrics:
                        TOTAL: 1
                        SUCCEEDED: 1
                        FAILED: 0
        "400":
          description: 请求参数错误。
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
      x-codeSamples:
        - lang: curl
          label: 查询任务结果
          source: |-
            # 将 {task_id} 替换为创建任务时返回的实际任务 ID
            curl -X GET 'https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY"
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

> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Wan 2.1 — 查询结果

> 查询 Wan 2.1 图像编辑任务状态

查询任务状态和结果。

## 轮询策略

1. 通过[创建任务](/api-reference/image-generation/wan21-general-image-editing/create-task)接口提交请求，获取 `task_id`。
2. 每 **10 秒**轮询一次，直到 `task_status` 为 `SUCCEEDED` 或 `FAILED`。
3. 任务成功后，`results` 中包含图片下载 URL。

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
  title: Wan2.1 通用图像编辑 API
  description: Wan 2.1 通用图像编辑 API。支持 10 种编辑功能：整图风格化、局部风格化、指令编辑、蒙版编辑、去水印、扩图、超分辨率、上色、涂鸦成图、卡通特征控制。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: DashScope API
security:
  - BearerAuth: []
paths:
  /tasks/{task_id}:
    get:
      operationId: getWan21ImageEditTaskStatus
      summary: 查询任务结果
      description: 查询图像编辑任务的状态和结果。
      parameters:
        - name: task_id
          in: path
          required: true
          description: 创建任务时返回的任务标识符。
          schema:
            type: string
      responses:
        "200":
          description: 成功获取任务状态。
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ImageEditTaskStatusResponse"
              examples:
                SUCCEEDED:
                  summary: 任务成功
                  value:
                    request_id: eeef0935-02e9-9742-bb55-xxxxxx
                    output:
                      task_id: a425c46f-dc0a-400f-879e-xxxxxx
                      task_status: SUCCEEDED
                      submit_time: 2025-02-21 17:56:31.786
                      scheduled_time: 2025-02-21 17:56:31.821
                      end_time: 2025-02-21 17:56:42.530
                      results:
                        - url: https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/aaa.png
                      task_metrics:
                        TOTAL: 1
                        SUCCEEDED: 1
                        FAILED: 0
                    usage:
                      image_count: 1
                FAILED:
                  summary: 任务失败
                  value:
                    request_id: e5d70b02-ebd3-98ce-9fe8-759d7d7b107d
                    output:
                      task_id: 86ecf553-d340-4e21-af6e-xxxxxx
                      task_status: FAILED
                      code: InvalidParameter
                      message: xxxxxx
                      task_metrics:
                        TOTAL: 4
                        SUCCEEDED: 0
                        FAILED: 4
                RUNNING:
                  summary: 任务运行中
                  value:
                    request_id: c1209113-8437-424f-a386-xxxxxx
                    output:
                      task_id: 966cebcd-dedc-4962-af88-xxxxxx
                      task_status: RUNNING
                      task_metrics:
                        TOTAL: 1
                        SUCCEEDED: 0
                        FAILED: 0
        "400":
          description: 请求参数无效。
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
      x-codeSamples:
        - lang: curl
          label: cURL - 查询任务结果
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
    Wan21ImageEditRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称。
          enum:
            - wanx2.1-imageedit
          example: wanx2.1-imageedit
        input:
          $ref: "#/components/schemas/Wan21ImageEditInput"
        parameters:
          $ref: "#/components/schemas/Wan21ImageEditParameters"
    Wan21ImageEditInput:
      type: object
      required:
        - function
        - prompt
        - base_image_url
      description: 图像编辑的输入数据。
      properties:
        function:
          type: string
          description: |-
            编辑功能类型。

            | 值 | 功能 |
            |---|---|
            | `stylization_all` | 整图风格化 |
            | `stylization_local` | 局部风格化 |
            | `description_edit` | 指令编辑 |
            | `description_edit_with_mask` | 蒙版编辑（需要 `mask_image_url`） |
            | `remove_watermark` | 去水印 |
            | `expand` | 扩图 |
            | `super_resolution` | 超分辨率 |
            | `colorization` | 上色 |
            | `doodle` | 涂鸦成图 |
            | `control_cartoon_feature` | 卡通特征控制 |
          enum:
            - stylization_all
            - stylization_local
            - description_edit
            - description_edit_with_mask
            - remove_watermark
            - expand
            - super_resolution
            - colorization
            - doodle
            - control_cartoon_feature
          example: description_edit_with_mask
        prompt:
          type: string
          description: 文本提示词，描述对图像的编辑要求。支持中英文。最大长度：800 字符，超出部分将被截断。
          maxLength: 800
          example: 陶瓷兔子拿着陶瓷小花。
        base_image_url:
          type: string
          description: |-
            待编辑的原始图像 URL 或 Base64 编码字符串。

            **图像要求：**
            - 支持格式：JPG、JPEG、PNG、BMP、TIFF、WEBP
            - 分辨率：宽高各需在 512~4096 像素之间
            - 最大文件大小：10 MB

            **支持的输入格式：**
            - **公网 URL**：支持 HTTP 和 HTTPS
            - **Base64 编码**：格式为 `data:{MIME_type};base64,{base64_data}`
          example: http://wanx.alicdn.com/material/20250318/description_edit_with_mask_3.jpeg
        mask_image_url:
          type: string
          description: 蒙版图像 URL 或 Base64 编码字符串。仅当 `function` 为 `description_edit_with_mask` 时需要。蒙版图像中白色区域为需要编辑的区域，黑色区域为保留区域。蒙版图像的尺寸应与原始图像一致。
          example: http://wanx.alicdn.com/material/20250318/description_edit_with_mask_3_mask.png
    Wan21ImageEditParameters:
      type: object
      description: 控制输出数量、随机种子、水印等处理选项。不同编辑功能支持不同的参数。
      properties:
        n:
          type: integer
          description: 生成图片的数量。取值范围：1~4，默认值：1。
          default: 1
          minimum: 1
          maximum: 4
          example: 1
        seed:
          type: integer
          description: 随机种子。取值范围：[0, 2147483647]。不设置时算法自动生成。固定种子可复现结果，但由于固有随机性，相同种子不保证完全一致的结果。
          minimum: 0
          maximum: 2147483647
        watermark:
          type: boolean
          description: 是否在图片右下角添加固定文字 "AI生成" 水印。默认值：false。
          default: false
          example: false
        strength:
          type: number
          description: 图像修改强度。仅适用于 `stylization_all` 和 `description_edit` 功能。取值范围：0.0~1.0，默认值：0.5。值越大，生成图像与原图差异越大。
          minimum: 0
          maximum: 1
          default: 0.5
          example: 0.5
        top_scale:
          type: number
          description: 向上扩展比例。仅适用于 `expand` 功能。取值范围：1.0~2.0，默认值：1.0。例如 1.5 表示向上扩展原图高度的 50%。
          minimum: 1
          maximum: 2
          default: 1
          example: 1.5
        bottom_scale:
          type: number
          description: 向下扩展比例。仅适用于 `expand` 功能。取值范围：1.0~2.0，默认值：1.0。
          minimum: 1
          maximum: 2
          default: 1
          example: 1.5
        left_scale:
          type: number
          description: 向左扩展比例。仅适用于 `expand` 功能。取值范围：1.0~2.0，默认值：1.0。
          minimum: 1
          maximum: 2
          default: 1
          example: 1.5
        right_scale:
          type: number
          description: 向右扩展比例。仅适用于 `expand` 功能。取值范围：1.0~2.0，默认值：1.0。
          minimum: 1
          maximum: 2
          default: 1
          example: 1.5
        upscale_factor:
          type: integer
          description: 超分辨率放大倍数。仅适用于 `super_resolution` 功能。取值范围：1~4，默认值：1。
          minimum: 1
          maximum: 4
          default: 1
          example: 2
        is_sketch:
          type: boolean
          description: 是否为线稿输入。仅适用于 `doodle` 功能。默认值：false。当为 false 时，模型会先从输入图像中提取线稿；当为 true 时，直接将输入图像作为线稿使用。
          default: false
          example: false
    AsyncTaskSubmitResponse:
      type: object
      properties:
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID，可在 24 小时内用于查询任务状态。
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
          description: 请求的唯一标识符，用于问题排查。
    ImageEditTaskStatusResponse:
      type: object
      properties:
        request_id:
          type: string
          description: 请求的唯一标识符。
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID，可在 24 小时内用于查询任务状态。
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
              description: 任务提交时间。时区为 UTC+8，格式：`YYYY-MM-DD HH:mm:ss.SSS`。
            scheduled_time:
              type: string
              description: 任务开始执行时间。时区为 UTC+8，格式：`YYYY-MM-DD HH:mm:ss.SSS`。
            end_time:
              type: string
              description: 任务完成时间。时区为 UTC+8，格式：`YYYY-MM-DD HH:mm:ss.SSS`。
            results:
              type: array
              description: 生成结果数组。每个条目包含图片 URL，或失败时的错误详情。
              items:
                type: object
                properties:
                  url:
                    type: string
                    description: 生成图像的 URL，有效期 24 小时。
                  code:
                    type: string
                    description: 单张图片生成失败的错误码。仅在部分失败时返回。
                  message:
                    type: string
                    description: 单张图片生成失败的错误信息。仅在部分失败时返回。
            task_metrics:
              type: object
              description: 任务结果统计。
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
          description: 用量统计。仅统计成功的结果。
          properties:
            image_count:
              type: integer
              description: 成功生成的图片数量。计费公式：费用 = 图片数量 x 单价。
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
          description: 请求的唯一标识符，用于问题排查。
````

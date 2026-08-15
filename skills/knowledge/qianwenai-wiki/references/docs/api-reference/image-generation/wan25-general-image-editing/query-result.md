> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Wan 2.5 — 查询结果

> 查询 Wan 2.5 图像编辑任务状态

查询任务状态和结果。

## 轮询策略

1. 通过[创建任务](/api-reference/image-generation/wan25-general-image-editing/create-task)接口提交请求，获取 `task_id`。
2. 每 **10 秒**轮询一次，直到 `task_status` 为 `SUCCEEDED` 或 `FAILED`。
3. 任务成功后，`results` 中包含图片下载 URL。

## 注意事项

- **URL 有效期**：图片 URL 在 **24 小时**后过期，请及时下载。
- **任务状态流转**：`PENDING` → `RUNNING` → `SUCCEEDED` 或 `FAILED`。
- **其他状态**：`CANCELED`（任务已取消）、`UNKNOWN`（`task_id` 无效或已过期）。
- **`task_id` 有效期**：`task_id` 有效期为 **24 小时**，过期后无法查询任务状态和结果。
- **避免重复提交**：请通过轮询获取结果，不要重复提交请求。
- **部分失败**：当 `n > 1` 时，只要有一张图片生成成功，任务状态即为 `SUCCEEDED`。失败的图片会在 `results` 中包含错误详情，仅成功的图片计入用量。

## OpenAPI

````yaml get /tasks/{task_id}
openapi: 3.1.0
info:
  title: Wan2.5 通用图像编辑 API
  description: Wan2.5 通用图像编辑 API。通过文本提示词对图像进行编辑，保持主体一致性。支持单图编辑和多图融合，最多支持三张参考图。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: DashScope API
security:
  - BearerAuth: []
paths:
  /tasks/{task_id}:
    get:
      operationId: getWan25ImageEditTaskStatus
      summary: 查询任务结果
      description: 查询图像编辑任务的状态和结果。
      parameters:
        - name: task_id
          in: path
          required: true
          description: 图像编辑创建接口返回的任务标识符。
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
                    request_id: d1f2a1be-9c58-48af-b43f-xxxxxx
                    output:
                      task_id: 7f4836cd-1c47-41b3-b3a4-xxxxxx
                      task_status: SUCCEEDED
                      submit_time: 2025-09-23 22:14:10.800
                      scheduled_time: 2025-09-23 22:14:10.825
                      end_time: 2025-09-23 22:15:23.456
                      results:
                        - orig_prompt: Change the floral dress to a vintage-style lace long dress with exquisite embroidery details on the collar and cuffs.
                          actual_prompt: Replace the pink pleated dress with a vintage-style lace long dress with exquisite embroidery details on the collar and cuffs. Keep the person's hairstyle, makeup, and posture unchanged. The overall style should be consistent with the soft tones and classic atmosphere of the original image.
                          url: https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxx.png?Expires=xxx
                      task_metrics:
                        TOTAL: 1
                        FAILED: 0
                        SUCCEEDED: 1
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
                      message: The specified parameter is not valid.
                      task_metrics:
                        TOTAL: 4
                        SUCCEEDED: 0
                        FAILED: 4
                RUNNING:
                  summary: 任务执行中
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
            # 将 {task_id} 替换为提交响应中返回的实际任务 ID
            curl -X GET 'https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY"
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    Wan25ImageEditRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称。
          enum:
            - wan2.5-i2i-preview
          example: wan2.5-i2i-preview
        input:
          $ref: "#/components/schemas/Wan25ImageEditInput"
        parameters:
          $ref: "#/components/schemas/Wan25ImageEditParameters"
    Wan25ImageEditInput:
      type: object
      required:
        - prompt
        - images
      description: 图像编辑的输入数据。
      properties:
        prompt:
          type: string
          description: 正向提示词，描述生成图像中需要包含的元素和视觉特征。支持中英文。最多 2,000 个字符，超出部分将被截断。
          example: Change the floral dress to a vintage-style lace long dress with exquisite embroidery details on the collar and cuffs.
        images:
          type: array
          description: |-
            输入图像 URL 数组。每次请求最多支持 3 张图像。多张图像时，数组顺序定义图像序号（图像 1、图像 2 等）。

            **图像限制：**
            - 支持格式：JPEG、JPG、PNG、BMP 和 WEBP。PNG alpha 通道将被忽略。
            - 分辨率：宽和高均须在 384 到 5,000 像素之间。
            - 最大文件大小：10 MB。

            **支持的输入格式：**
            - **公开 URL**：支持 HTTP 和 HTTPS。
            - **Base64 编码字符串**：格式：`data:{MIME_type};base64,{base64_data}`。
            - **本地文件路径**：格式：`file://{绝对路径}`（仅适用于 SDK 调用）。
          items:
            type: string
          minItems: 1
          maxItems: 3
          example:
            - https://img.alicdn.com/imgextra/i2/O1CN01vHOj4h28jOxUJPwY8_!!6000000007968-49-tps-1344-896.webp
        negative_prompt:
          type: string
          description: 反向提示词，描述生成图像中需要排除的元素。支持中英文。最多 500 个字符，超出部分将被截断。
          example: low resolution, error, worst quality, low quality, disfigured, extra fingers, bad proportions
    Wan25ImageEditParameters:
      type: object
      description: 控制输出分辨率、提示词改写、水印及其他处理选项。
      properties:
        size:
          type: string
          description: |-
            输出分辨率，格式为 `{宽度}*{高度}`。默认值：`1280*1280`。总像素数须在 589,824（768*768）到 1,638,400（1280*1280）之间，宽高比须在 1:4 到 4:1 之间。

            推荐分辨率：
            - 1280*1280 (1:1)
            - 1024*1024 (1:1)
            - 800*1200 (2:3)
            - 1200*800 (3:2)
            - 960*1280 (3:4)
            - 1280*960 (4:3)
            - 720*1280 (9:16)
            - 1280*720 (16:9)
            - 1344*576 (21:9)

            未指定时，系统默认输出 1280*1280 总像素数的图像，并保留与输入图像相近的宽高比：
            - 单图输入：宽高比与输入图像保持一致。
            - 多图输入：宽高比与最后一张输入图像保持一致。
          default: 1280*1280
          example: 1280*1280
        n:
          type: integer
          description: 生成图像的数量。有效范围：1 到 4。默认值：4。`n` 参数直接影响计费，值越大费用越高。建议测试时明确设置为 1 以控制成本。
          default: 4
          minimum: 1
          maximum: 4
          example: 1
        watermark:
          type: boolean
          description: 是否在图像右下角添加固定文字 "AI-generated" 水印。
          default: false
          example: false
        prompt_extend:
          type: boolean
          description: 开启智能提示词改写。启用后，大语言模型将优化您的提示词以获得更好的效果，但会增加处理时间。默认值：true。
          default: true
          example: true
        seed:
          type: integer
          description: 随机数种子。取值范围：[0, 2147483647]。未指定时，算法自动生成随机数作为种子。指定后，算法为每张图像（共 `n` 张）分别生成一个种子值（seed、seed+1、seed+2……）。若需复现特定结果，请使用固定种子值。注意：由于固有随机性，相同种子不一定能生成完全相同的结果。
          minimum: 0
          maximum: 2147483647
    AsyncTaskSubmitResponse:
      type: object
      properties:
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID。可在 24 小时内用于查询任务状态。
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
          description: 请求的唯一标识符，可用于问题追踪与排查。
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
              description: 任务 ID。可在 24 小时内用于查询任务状态。
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
              description: 任务提交时间，北京时间（UTC+8）。格式：`YYYY-MM-DD HH:mm:ss.SSS`。
            scheduled_time:
              type: string
              description: 任务开始执行时间，北京时间（UTC+8）。格式：`YYYY-MM-DD HH:mm:ss.SSS`。
            end_time:
              type: string
              description: 任务完成时间，北京时间（UTC+8）。格式：`YYYY-MM-DD HH:mm:ss.SSS`。
            results:
              type: array
              description: 生成结果数组。每个条目包含图像 URL、提示词，或生成失败时的错误信息。
              items:
                type: object
                properties:
                  orig_prompt:
                    type: string
                    description: 原始输入提示词。
                  actual_prompt:
                    type: string
                    description: 启用提示词改写时实际使用的优化后提示词。未启用该功能时不返回。
                  url:
                    type: string
                    description: 生成图像的 URL。有效期 24 小时。
                  code:
                    type: string
                    description: 图像生成失败时的错误码。仅在部分失败时返回。
                  message:
                    type: string
                    description: 图像生成失败时的错误信息。仅在部分失败时返回。
            task_metrics:
              type: object
              description: 任务结果统计信息。
              properties:
                TOTAL:
                  type: integer
                  description: 任务总数。
                SUCCEEDED:
                  type: integer
                  description: 成功任务数。
                FAILED:
                  type: integer
                  description: 失败任务数。
            code:
              type: string
              description: 错误码。仅在任务失败时返回。
            message:
              type: string
              description: 详细错误信息。仅在任务失败时返回。
        usage:
          type: object
          description: 输出统计信息。仅统计成功生成的结果。
          properties:
            image_count:
              type: integer
              description: 成功生成的图像数量。计费公式：费用 = 图像数量 × 单价。
    DashScopeErrorResponse:
      type: object
      properties:
        code:
          type: string
          description: 标识错误类型的错误码。
        message:
          type: string
          description: 详细错误信息。
        request_id:
          type: string
          description: 用于问题排查的唯一请求标识符。
````

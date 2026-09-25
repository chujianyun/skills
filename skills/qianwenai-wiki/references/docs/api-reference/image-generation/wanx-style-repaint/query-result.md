> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 人像风格重绘 — 查询结果

> 查询人像风格重绘任务状态

查询任务状态和结果。

## 轮询策略

1. 通过[创建任务](/api-reference/image-generation/wanx-style-repaint/create-task)接口提交请求，获取 `task_id`。
2. 每 **3 秒**轮询一次，直到 `task_status` 为 `SUCCEEDED` 或 `FAILED`。
3. 任务成功后，`results` 中包含图片下载 URL。

## 注意事项

- **URL 有效期**：图片 URL 在 **24 小时**后过期，请及时下载。
- **任务状态流转**：`PENDING` → `RUNNING` → `SUCCEEDED` 或 `FAILED`。
- **其他状态**：`CANCELED`（任务已取消）、`UNKNOWN`（`task_id` 无效或已过期）。
- **`task_id` 有效期**：`task_id` 有效期为 **24 小时**，过期后无法查询任务状态和结果。
- **避免重复提交**：请通过轮询获取结果，不要重复提交请求。

## 错误码

| 错误码                      | HTTP 状态码 | 说明                                                      |
| ------------------------ | -------- | ------------------------------------------------------- |
| `InvalidURL`             | 400      | 图片 URL 无效或无法访问。请检查 URL 是否可公开访问。                         |
| `InvalidImageFormat`     | 400      | 图片格式不支持。支持的格式：JPEG、JPG、PNG、BMP、WEBP。                    |
| `InvalidImageResolution` | 400      | 图片分辨率过大或过小。宽高最小 256 像素，最大不超过 5760×3240 像素，长短边比例不超过 2:1。 |

## 常见问题

**图片报错 InvalidImageFormat 怎么办？**

请确保图片格式为 JPEG、JPG、PNG、BMP 或 WEBP。如果后缀名正确但仍报错，请检查文件实际编码格式是否与后缀名一致。

**输出图片的尺寸是多少？**

输出图片的短边固定为 1536 像素，长边根据原图比例自动计算。

## OpenAPI

````yaml get /tasks/{task_id}
openapi: 3.1.0
info:
  title: 人像风格重绘 API
  description: 人像风格重绘模型支持将人物照片转换为多种预设或自定义的艺术风格。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: DashScope API 端点
security:
  - BearerAuth: []
paths:
  /tasks/{task_id}:
    get:
      operationId: getWanxStyleRepaintTaskStatus
      summary: 查询人像风格重绘任务结果
      description: 使用 task_id 轮询任务状态，直至完成并获取生成的图像URL。图像URL有效期为24小时。模型耗时约15秒，建议采用轮询机制并设置合理的查询间隔（如3秒）。
      parameters:
        - name: task_id
          in: path
          required: true
          description: 任务ID。创建任务接口返回的唯一标识。
          schema:
            type: string
      responses:
        "200":
          description: 成功获取任务状态。
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StyleRepaintTaskStatusResponse"
              examples:
                SUCCEEDED:
                  summary: 任务执行成功
                  value:
                    request_id: f7fee4f1-1f68-9f17-85df-xxxxx
                    output:
                      task_id: 316c7af0-e91f-476f-99bd-xxxxxx
                      task_status: SUCCEEDED
                      submit_time: 2025-08-12 10:55:43.768
                      scheduled_time: 2025-08-12 10:55:43.799
                      end_time: 2025-08-12 10:55:48
                      error_message: Success
                      start_time: 2025-08-12 10:55:43
                      style_index: 0
                      error_code: 0
                      results:
                        - url: https://oss.aliyuncs.com/xxx/abc.jpg
                    usage:
                      image_count: 1
                FAILED:
                  summary: 任务执行失败
                  value:
                    request_id: a3b4c5d6-e7f8-9012-abcd-xxxxxx
                    output:
                      task_id: 1a2b3c4d-5e6f-7890-bcde-xxxxxx
                      task_status: FAILED
                      submit_time: 2025-08-12 10:55:43.768
                      scheduled_time: 2025-08-12 10:55:43.799
                      end_time: 2025-08-12 10:55:44
                      code: InvalidImageResolution
                      message: The input image resolution is too large or small
                    usage:
                      image_count: 0
                RUNNING:
                  summary: 任务执行中
                  value:
                    request_id: e5d70b02-ebd3-98ce-9fe8-759d7d7b107d
                    output:
                      task_id: 86ecf553-d340-4e21-af6e-a0c6a421c010
                      task_status: RUNNING
                      task_metrics:
                        TOTAL: 1
                        SUCCEEDED: 1
                        FAILED: 0
        "400":
          description: 请求参数无效。
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
      x-codeSamples:
        - lang: curl
          label: 查询任务结果
          source: |-
            # 将 {task_id} 替换为上一步接口返回的 task_id 的值
            curl -X GET 'https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}' \
              --header "Authorization: Bearer $DASHSCOPE_API_KEY"
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    WanxStyleRepaintRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称。示例值：wanx-style-repaint-v1。
          enum:
            - wanx-style-repaint-v1
          example: wanx-style-repaint-v1
        input:
          $ref: "#/components/schemas/WanxStyleRepaintInput"
    WanxStyleRepaintInput:
      type: object
      required:
        - image_url
        - style_index
      description: 输入图像的基本信息，比如图像URL地址。
      properties:
        image_url:
          type: string
          description: |-
            输入的图像URL地址。

            - 支持公网可访问的HTTP/HTTPS地址，不包含中文字符。
            - 支持传入Base64编码字符串。
            - 对于本地文件，可通过以下方式获取合法参数值：
              - 获取URL：请参见上传文件获取临时URL。
              - 生成Base64编码字符串：请参见图像Base64编码传值方式。

            **图像限制：**
            - 图像分辨率：不低于256×256像素，不超过5760×3240像素。
            - 图像格式：JPEG、PNG、JPG、BMP、WEBP。
            - 图像比例：长短边比例不超过2:1。
            - 图像大小：不超过10M。
            - 图像质量：为确保生成质量，请上传脸部清晰照片，人脸比例不宜过小，并避免夸张姿势和表情。
          example: https://vigen-video.oss-cn-shanghai.aliyuncs.com/demo_image/image_demo_input.png
        style_index:
          type: integer
          description: |-
            选择一个预置的风格索引值，即可生成风格化人像。

            **枚举值：**
            - `-1`：使用参考图像风格（需提供 `style_ref_url`）
            - `0`：复古漫画
            - `1`：3D童话
            - `2`：二次元
            - `3`：小清新
            - `4`：未来科技
            - `5`：国画古风
            - `6`：将军百战
            - `7`：炫彩卡通
            - `8`：清雅国风
            - `9`：喜迎新年
            - `14`：国风工笔
            - `15`：恭贺新禧
            - `30`：童话世界
            - `31`：黏土世界
            - `32`：像素世界
            - `33`：冒险世界
            - `34`：日漫世界
            - `35`：3D世界
            - `36`：二次元世界
            - `37`：手绘世界
            - `38`：蜡笔世界
            - `39`：冰箱贴世界
            - `40`：吧唧世界
          enum:
            - -1
            - 0
            - 1
            - 2
            - 3
            - 4
            - 5
            - 6
            - 7
            - 8
            - 9
            - 14
            - 15
            - 30
            - 31
            - 32
            - 33
            - 34
            - 35
            - 36
            - 37
            - 38
            - 39
            - 40
          example: 3
        style_ref_url:
          type: string
          description: |-
            风格参考图像URL地址。当 `style_index=-1` 时必须传入，其他风格无需传入。

            - 支持公网可访问的HTTP/HTTPS地址，不包含中文字符。
            - 支持传入Base64编码字符串。
            - 对于本地文件，可通过以下方式获取合法参数值：
              - 获取URL：请参见上传文件获取临时URL。
              - 生成Base64编码字符串：请参见图像Base64编码传值方式。

            **图像限制：**
            - 图像分辨率：不低于256×256像素且不超过5760×3240像素。
            - 图像比例：为取得最佳效果，建议图像长短边比例不超过2:1，否则可能影响生成或导致报错。
            - 图像格式：JPEG、PNG、JPG、BMP、WEBP。
            - 图像大小：不超过10M。
          example: https://vigen-video.oss-cn-shanghai.aliyuncs.com/demo_image/style_example.png
    AsyncTaskSubmitResponse:
      type: object
      properties:
        output:
          type: object
          description: 任务输出信息。
          properties:
            task_id:
              type: string
              description: 任务ID。查询有效期24小时。
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
          description: 请求唯一标识。可用于请求明细溯源和问题排查。
        code:
          type: string
          description: 请求失败的错误码。请求成功时不会返回此参数。
        message:
          type: string
          description: 请求失败的详细信息。请求成功时不会返回此参数。
    StyleRepaintTaskStatusResponse:
      type: object
      properties:
        request_id:
          type: string
          description: 请求唯一标识。可用于请求明细溯源和问题排查。
        output:
          type: object
          description: 任务输出信息。
          properties:
            task_id:
              type: string
              description: 任务ID。查询有效期24小时。
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
              description: 任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。
            scheduled_time:
              type: string
              description: 任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。
            start_time:
              type: string
              description: 任务开始时间。
            end_time:
              type: string
              description: 任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。
            style_index:
              type: integer
              description: 返回指定所选风格的索引值。
            error_code:
              type: integer
              description: 错误码。正常请求时返回，可忽略。
            error_message:
              type: string
              description: 错误信息。正常请求时返回，可忽略。
            results:
              type: array
              description: 任务结果列表，包括图像URL、prompt、部分任务执行失败报错信息等。
              items:
                type: object
                properties:
                  url:
                    type: string
                    description: 生成的图像URL地址。有效期为24小时，请及时下载并保存。
                  orig_prompt:
                    type: string
                    description: 原始prompt。
                  actual_prompt:
                    type: string
                    description: 实际使用的prompt。
                  code:
                    type: string
                    description: 部分任务执行失败的错误码。
                  message:
                    type: string
                    description: 部分任务执行失败的错误信息。
            task_metrics:
              type: object
              description: 任务结果统计。
              properties:
                TOTAL:
                  type: integer
                  description: 总的任务数。
                SUCCEEDED:
                  type: integer
                  description: 任务状态为成功的任务数。
                FAILED:
                  type: integer
                  description: 任务状态为失败的任务数。
            code:
              type: string
              description: 请求失败的错误码。请求成功时不会返回此参数。
            message:
              type: string
              description: 请求失败的详细信息。请求成功时不会返回此参数。
        usage:
          type: object
          description: 输出信息统计。只对成功的结果计数。
          properties:
            image_count:
              type: integer
              description: 模型成功生成图片的数量。计费公式：费用 = 图片数量 × 单价。
    DashScopeErrorResponse:
      type: object
      properties:
        code:
          type: string
          description: 错误码，标识错误类型。
        message:
          type: string
          description: 错误详细信息。
        request_id:
          type: string
          description: 请求唯一标识，用于排查问题。
````

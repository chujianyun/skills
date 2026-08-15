> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 万相涂鸦作画 — 查询结果

> 通过任务 ID 查询涂鸦作画任务的状态和结果。

查询任务状态和生成结果。

## 轮询策略

1. 通过[创建任务](/api-reference/image-generation/wanx-sketch-to-image/create-task)接口提交请求，获取 `task_id`。
2. 每 **3 秒**轮询一次，直到 `task_status` 为 `SUCCEEDED` 或 `FAILED`。
3. 任务成功后，`results` 中包含图片下载 URL。

## 注意事项

- **URL 有效期**：图片 URL 在 **24 小时**后过期，请及时下载。
- **任务状态流转**：`PENDING` → `RUNNING` → `SUCCEEDED` 或 `FAILED`。
- **其他状态**：`CANCELED`（任务已取消）、`UNKNOWN`（`task_id` 无效或已过期）。
- **`task_id` 有效期**：`task_id` 有效期为 **24 小时**，过期后无法查询任务状态和结果。
- **避免重复提交**：请通过轮询获取结果，不要重复提交请求。

## OpenAPI

````yaml get /tasks/{task_id}
openapi: 3.0.0
info:
  title: 万相-涂鸦作画
  description: 本文介绍万相-涂鸦作画模型的API输入输出参数。万相-涂鸦作画通过手绘图案和文字描述，生成精美的涂鸦绘画作品。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
security:
  - ApiKeyAuth: []
paths:
  /tasks/{task_id}:
    get:
      summary: 根据任务ID查询结果
      description: 使用任务ID查询任务状态及结果。任务成功执行时将返回图像URL，有效期24小时。
      operationId: getSketchToImageTaskResult
      parameters:
        - name: task_id
          in: path
          required: true
          description: 任务ID。查询有效期24小时。
          schema:
            type: string
      responses:
        "200":
          description: 成功查询任务
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/QueryTaskResponse"
              examples:
                succeeded:
                  summary: 任务执行成功
                  value:
                    request_id: 85eaba38-0185-99d7-8d16-4d9135238846
                    output:
                      task_id: 86ecf553-d340-4e21-af6e-a0c6a421c010
                      task_status: SUCCEEDED
                      results:
                        - url: https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/123/a1.png
                        - url: https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/123/b2.png
                      task_metrics:
                        TOTAL: 2
                        SUCCEEDED: 2
                        FAILED: 0
                    usage:
                      image_count: 2
                failed:
                  summary: 任务执行失败
                  value:
                    request_id: e5d70b02-ebd3-98ce-9fe8-759d7d7b107d
                    output:
                      task_id: 86ecf553-d340-4e21-af6e-a0c6a421c010
                      task_status: FAILED
                      code: InvalidParameter
                      message: The size is not match the allowed size ['1024*1024', '720*1280', '1280*720']
                      task_metrics:
                        TOTAL: 4
                        SUCCEEDED: 0
                        FAILED: 4
                partial_failed:
                  summary: 任务部分失败
                  value:
                    request_id: 85eaba38-0185-99d7-8d16-4d9135238846
                    output:
                      task_id: 86ecf553-d340-4e21-af6e-a0c6a421c010
                      task_status: SUCCEEDED
                      results:
                        - url: https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/123/a1.png
                        - code: InternalError.Timeout
                          message: An internal timeout error has occurred during execution, please try again later or contact service support.
                      task_metrics:
                        TOTAL: 2
                        SUCCEEDED: 1
                        FAILED: 1
                    usage:
                      image_count: 1
                running:
                  summary: 任务处理中
                  value:
                    request_id: c5d70b02-ebd3-98ce-9fe8-759d7d7b107e
                    output:
                      task_id: 86ecf553-d340-4e21-af6e-a0c6a421c010
                      task_status: RUNNING
                      task_metrics:
                        TOTAL: 2
                        SUCCEEDED: 0
                        FAILED: 0
      x-codeSamples:
        - lang: cURL
          label: curl
          source: |-
            curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/86ecf553-d340-4e21-xxxxxxxxx \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY"
components:
  schemas:
    CreateTaskRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 调用模型，固定为 wanx-sketch-to-image-lite。
          example: wanx-sketch-to-image-lite
        input:
          $ref: "#/components/schemas/Input"
        parameters:
          $ref: "#/components/schemas/Parameters"
    Input:
      type: object
      required:
        - prompt
        - sketch_image_url
      description: 输入的基本信息，比如提示词、图像URL地址。
      properties:
        prompt:
          type: string
          description: 提示词，用来描述生成图像中期望包含的元素和视觉特点。支持中英文，长度不超过75个字符，超过部分会自动截断。
          example: 一棵参天大树
        sketch_image_url:
          type: string
          description: 输入草图的URL地址。输入草图需要与输出图像的分辨率比例保持一致，否则会导致图片拉伸变形，建议使用白色背景图。URL需为公网可访问的地址，并支持HTTP或HTTPS协议，URL地址中不能包含中文字符。图像格式支持JPG、JPEG、PNG、TIFF、WEBP。图像分辨率不小于256×256像素且不超过2048×2048像素。图像大小不超过10 MB。
    Parameters:
      type: object
      description: 图像处理参数。
      properties:
        style:
          type: string
          description: 输出图像的风格。
          enum:
            - <auto>
            - <3d cartoon>
            - <anime>
            - <oil painting>
            - <watercolor>
            - <sketch>
            - <chinese painting>
            - <flat illustration>
          default: <auto>
          x-enumDescriptions:
            <auto>: 默认值，由模型随机输出图像风格。
            <3d cartoon>: 3D卡通。
            <anime>: 二次元。
            <oil painting>: 油画。
            <watercolor>: 水彩。
            <sketch>: 素描。
            <chinese painting>: 中国画。
            <flat illustration>: 扁平插画。
        size:
          type: string
          description: 输出图像的分辨率。目前仅支持一种图像分辨率：768*768，且为默认值。
          default: 768*768
        n:
          type: integer
          description: 生成图片的数量。取值范围为1~4张，默认为4。
          default: 4
          minimum: 1
          maximum: 4
        sketch_weight:
          type: integer
          description: 输入草图对输出图像的约束程度。取值范围为0-10，取值间隔为1，默认值为10。取值越大表示输出图像跟输入草图越相似。
          default: 10
          minimum: 0
          maximum: 10
        sketch_extraction:
          type: boolean
          description: 如果上传图片是RGB图片，而非草图（sketch线稿），此参数可控制是否对输入图片进行sketch边缘提取。默认值为False，表示不进行提取。设置为True时，表示进行提取，此时sketch_color字段失效。
          default: false
        sketch_color:
          type: array
          description: 此字段在sketch_extraction=false时生效，所包含数值均被视为画笔色，其余数值均会视为背景色。模型会基于一种或多种画笔色描绘的区域生成新的画作。默认值为[]。当sketch_image_url线稿中的线条不是黑色，而是包含其他一种或多种颜色时，可以指定一个或多个RGB颜色数值作为画笔色。
          default: []
          items:
            type: array
            items:
              type: integer
            minItems: 3
            maxItems: 3
          example:
            - - 134
              - 134
              - 134
            - - 0
              - 0
              - 0
    CreateTaskResponse:
      type: object
      properties:
        output:
          $ref: "#/components/schemas/CreateTaskOutput"
        request_id:
          type: string
          description: 请求唯一标识。可用于请求明细溯源和问题排查。
        code:
          type: string
          description: 请求失败的错误码。请求成功时不会返回此参数。
        message:
          type: string
          description: 请求失败的详细信息。请求成功时不会返回此参数。
    CreateTaskOutput:
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
          x-enumDescriptions:
            PENDING: 任务排队中
            RUNNING: 任务处理中
            SUCCEEDED: 任务执行成功
            FAILED: 任务执行失败
            CANCELED: 任务已取消
            UNKNOWN: 任务不存在或状态未知
    QueryTaskResponse:
      type: object
      properties:
        request_id:
          type: string
          description: 请求唯一标识。可用于请求明细溯源和问题排查。
        output:
          $ref: "#/components/schemas/QueryTaskOutput"
        usage:
          $ref: "#/components/schemas/Usage"
    QueryTaskOutput:
      type: object
      description: 任务输出信息。任务数据（如任务状态、图像URL等）仅保留24小时，超时后会被自动清除。请您务必及时保存生成的图像。
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
          x-enumDescriptions:
            PENDING: 任务排队中
            RUNNING: 任务处理中
            SUCCEEDED: 任务执行成功
            FAILED: 任务执行失败
            CANCELED: 任务已取消
            UNKNOWN: 任务不存在或状态未知
        results:
          type: array
          description: 任务结果列表，包括图像URL、部分任务执行失败报错信息等。
          items:
            $ref: "#/components/schemas/ResultItem"
        task_metrics:
          $ref: "#/components/schemas/TaskMetrics"
        code:
          type: string
          description: 请求失败的错误码。请求成功时不会返回此参数。
        message:
          type: string
          description: 请求失败的详细信息。请求成功时不会返回此参数。
    ResultItem:
      type: object
      description: 单个任务结果。
      properties:
        url:
          type: string
          description: 生成图像的URL地址。
        code:
          type: string
          description: 该任务结果失败的错误码。
        message:
          type: string
          description: 该任务结果失败的详细信息。
    TaskMetrics:
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
    Usage:
      type: object
      description: 输出信息统计。只对成功的结果计数。
      properties:
        image_count:
          type: integer
          description: 模型成功生成图片的数量。计费公式：费用 = 图片数量 × 单价。
  securitySchemes:
    ApiKeyAuth:
      type: http
      scheme: bearer
      bearerFormat: token
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
````

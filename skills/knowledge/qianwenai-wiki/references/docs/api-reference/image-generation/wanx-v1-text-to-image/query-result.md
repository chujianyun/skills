> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# wanx-v1 — 查询结果

> 查询 wanx-v1 图像生成任务状态

查询任务状态并获取生成的图像。

## 轮询策略

1. 通过[创建任务](/api-reference/image-generation/wanx-v1-text-to-image/create-task)接口提交任务，获取 `task_id`。
2. 每 **5 秒**轮询一次，直到 `output.task_status` 为 `SUCCEEDED` 或 `FAILED`。
3. 任务成功后，从 `output.results[].url` 获取图像链接。

## 注意事项

- **URL 有效期**：生成的图像 URL 有效期为 **24 小时**，请及时下载。
- **任务状态流转**：`PENDING` → `RUNNING` → `SUCCEEDED`、`FAILED`、`CANCELED` 或 `UNKNOWN`。
- **任务 ID 有效期**：`task_id` 有效期为 24 小时，过期后无法查询状态和结果。
- **避免重复提交**：请通过轮询获取结果，不要重复提交请求。

## OpenAPI

````yaml get /tasks/{task_id}
openapi: 3.1.0
info:
  title: Wan 文生图 V1 API
  description: 使用 wanx-v1 模型根据文本描述生成图像。本 API 采用异步任务模式：先通过 POST 请求提交任务，再通过 GET 请求轮询结果。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 阿里云 DashScope API
security:
  - BearerAuth: []
paths:
  /tasks/{task_id}:
    get:
      operationId: getWanxV1TaskResult
      summary: 查询任务结果
      description: 查询异步文生图任务的状态和结果。每 5 秒轮询一次，直到 `output.task_status` 为 `SUCCEEDED` 或 `FAILED`。
      parameters:
        - name: task_id
          in: path
          required: true
          description: 任务 ID，由创建任务接口返回的 `output.task_id`。
          schema:
            type: string
      responses:
        "200":
          description: 查询成功。
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/WanxV1TaskStatusResponse"
              examples:
                SUCCEEDED:
                  summary: 任务成功
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
                SUCCEEDED_PARTIAL:
                  summary: 任务成功（部分图像生成失败）
                  value:
                    request_id: 85eaba38-0185-99d7-8d16-4d9135238847
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
                FAILED:
                  summary: 任务失败
                  value:
                    request_id: e5d70b02-ebd3-98ce-9fe8-759d7d7b107d
                    output:
                      task_id: 86ecf553-d340-4e21-af6e-a0c6a421c010
                      task_status: FAILED
                      code: InvalidParameter
                      message: The size is not match the allowed size ['1024*1024', '720*1280', '768*1152', '1280*720']
                      task_metrics:
                        TOTAL: 4
                        SUCCEEDED: 0
                        FAILED: 4
                RUNNING:
                  summary: 任务执行中
                  value:
                    request_id: f3a91c2d-7b6e-4d5f-a8c2-xxxxxx
                    output:
                      task_id: 86ecf553-d340-4e21-af6e-a0c6a421c010
                      task_status: RUNNING
                      task_metrics:
                        TOTAL: 4
                        SUCCEEDED: 0
                        FAILED: 0
                PENDING:
                  summary: 任务等待中
                  value:
                    request_id: c826b6cd-e3f4-4a6f-b3b1-xxxxxx
                    output:
                      task_id: 86ecf553-d340-4e21-af6e-a0c6a421c010
                      task_status: PENDING
                      task_metrics:
                        TOTAL: 4
                        SUCCEEDED: 0
                        FAILED: 0
        4XX:
          description: 请求失败。
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
      x-codeSamples:
        - lang: curl
          label: cURL
          source: |-
            curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/86ecf553-d340-4e21-xxxxxxxxx \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY"
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    WanxV1TextToImageRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称。
          example: wanx-v1
        input:
          type: object
          required:
            - prompt
          description: 输入内容。
          properties:
            prompt:
              type: string
              description: 正向文本描述，即期望图像中出现的内容。最大 800 个字符。
              maxLength: 800
            negative_prompt:
              type: string
              description: 反向文本描述，即不希望图像中出现的内容。最大 500 个字符。
              maxLength: 500
            ref_img:
              type: string
              description: 参考图像 URL。支持 JPG、PNG、BMP、TIFF、WEBP 格式，大小不超过 10 MB，分辨率在 256×256 至 4096×4096 之间，URL 不能包含中文字符。
        parameters:
          type: object
          description: 生成参数（可选）。
          properties:
            style:
              type: string
              description: 图像风格。
              enum:
                - <auto>
                - <photography>
                - <portrait>
                - <3d cartoon>
                - <anime>
                - <oil painting>
                - <watercolor>
                - <sketch>
                - <chinese painting>
                - <flat illustration>
              default: <auto>
            size:
              type: string
              description: 图像分辨率，格式为 `宽*高`。
              enum:
                - 1024*1024
                - 720*1280
                - 768*1152
                - 1280*720
              default: 1024*1024
            n:
              type: integer
              description: 生成图像数量。
              minimum: 1
              maximum: 4
              default: 4
            seed:
              type: integer
              description: 随机种子，用于结果复现。范围 [0, 2147483647]。
              minimum: 0
              maximum: 2147483647
            ref_strength:
              type: number
              description: 参考图强度，控制生成图像与参考图的相似程度。范围 [0.0, 1.0]，值越大越相似。
              minimum: 0
              maximum: 1
            ref_mode:
              type: string
              description: 参考图模式。`repaint` 基于参考图内容生成，`refonly` 基于参考图风格生成。
              enum:
                - repaint
                - refonly
              default: repaint
    WanxV1CreateTaskResponse:
      type: object
      properties:
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID，用于查询任务状态和结果。有效期 24 小时。
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
          description: 请求唯一标识。
    WanxV1TaskStatusResponse:
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
              description: 任务 ID。
            task_status:
              type: string
              description: 任务状态：`PENDING`（等待）、`RUNNING`（运行中）、`SUCCEEDED`（成功）、`FAILED`（失败）、`CANCELED`（已取消）、`UNKNOWN`（未知）。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - CANCELED
                - UNKNOWN
            results:
              type: array
              description: 生成的图像列表。任务成功后返回。
              items:
                type: object
                properties:
                  url:
                    type: string
                    description: 图像 URL，有效期 24 小时，请及时下载。
                  code:
                    type: string
                    description: 当该图像生成失败时，返回错误码。
                  message:
                    type: string
                    description: 当该图像生成失败时，返回错误信息。
            task_metrics:
              type: object
              description: 任务统计信息。
              properties:
                TOTAL:
                  type: integer
                  description: 图像总数。
                SUCCEEDED:
                  type: integer
                  description: 成功生成的图像数量。
                FAILED:
                  type: integer
                  description: 生成失败的图像数量。
            code:
              type: string
              description: 任务失败时的错误码。
            message:
              type: string
              description: 任务失败时的错误信息。
        usage:
          type: object
          description: 资源用量统计。
          properties:
            image_count:
              type: integer
              description: 成功生成的图像数量。
    DashScopeErrorResponse:
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
````

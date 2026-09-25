> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 取消 Batch

## OpenAPI

````yaml post /batches/{batch_id}/cancel
openapi: 3.1.0
info:
  title: 千问AI平台 Batch API
  description: 通过文件上传提交批量推理任务，费用仅为实时 API 调用的50%。兼容 OpenAI 接口。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/compatible-mode/v1
    description: DashScope API
security:
  - BearerAuth: []
paths:
  /batches/{batch_id}/cancel:
    post:
      operationId: cancelBatch
      summary: 取消批量任务
      description: 取消正在执行或排队中的批量任务。状态将先变为 `cancelling`（等待当前正在执行的请求完成），然后变为 `cancelled`。取消前已完成的请求仍会计费。
      parameters:
        - name: batch_id
          in: path
          required: true
          description: 要取消的批量任务 ID。
          schema:
            type: string
            example: batch_abc123
      responses:
        "200":
          description: 批量任务取消已发起
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/BatchObject"
        "400":
          description: 请求无效——批量任务当前状态不允许取消
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
      x-codeSamples:
        - lang: python
          label: Python
          source: |-
            from openai import OpenAI
            import os

            client = OpenAI(
              api_key=os.getenv("DASHSCOPE_API_KEY"),
              base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            )

            batch = client.batches.cancel("batch_abc123")

            print(f"Status: {batch.status}")
        - lang: javascript
          label: Node.js
          source: |-
            import OpenAI from "openai";

            const client = new OpenAI({
              apiKey: process.env.DASHSCOPE_API_KEY,
              baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
            });

            const batch = await client.batches.cancel("batch_abc123");

            console.log(`Status: ${batch.status}`);
        - lang: curl
          label: cURL
          source: |-
            curl -X POST "https://dashscope.aliyuncs.com/compatible-mode/v1/batches/batch_abc123/cancel" \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY"
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    UploadFileRequest:
      type: object
      required:
        - file
        - purpose
      properties:
        file:
          type: string
          format: binary
          description: 要上传的 JSONL 文件。必须为 UTF-8 编码，每行一个 JSON 对象。最大文件大小为 500 MB，最多 50,000 条请求。
        purpose:
          type: string
          enum:
            - batch
          description: 文件的用途。批量处理必须设为 `"batch"`。
    FileObject:
      type: object
      properties:
        id:
          type: string
          description: 文件唯一标识符。
          example: file-abc123
        object:
          type: string
          enum:
            - file
          description: 固定为 `"file"`。
        bytes:
          type: integer
          description: 文件大小（字节）。
          example: 2048
        created_at:
          type: integer
          description: 文件上传时间的 Unix 时间戳（秒）。
          example: 1735113344
        filename:
          type: string
          description: 原始文件名。
          example: input.jsonl
        purpose:
          type: string
          enum:
            - batch
          description: 文件用途。批量输入文件固定为 `"batch"`。
        status:
          type: string
          description: 当前文件状态。
          example: processed
        status_details:
          type: string
          nullable: true
          description: 附加状态详情。无可用详情时为 `null`。
    CreateBatchRequest:
      type: object
      required:
        - input_file_id
        - endpoint
        - completion_window
      properties:
        input_file_id:
          type: string
          description: 已上传输入文件的 ID。通过文件上传接口的响应获取。
          example: file-abc123
        endpoint:
          type: string
          enum:
            - /v1/chat/completions
            - /v1/embeddings
            - /v1/chat/ds-test
          description: 批量请求的 API 接口路径。必须与输入文件中的 `url` 字段一致。文本生成使用 `/v1/chat/completions`，向量化使用 `/v1/embeddings`，测试模型使用 `/v1/chat/ds-test`。
          example: /v1/chat/completions
        completion_window:
          type: string
          description: 批量任务的最大完成时间。取值范围：`24h` 至 `336h`（14 天）。支持小时（`h`）和天（`d`）为单位，如 `24h`、`7d`。仅支持整数。
          example: 24h
        metadata:
          type: object
          nullable: true
          description: 批量任务的可选键值对元数据。
          additionalProperties:
            type: string
          properties:
            ds_name:
              type: string
              description: 任务名称。最多 100 个字符。如果多次定义，取最后一个值。
              example: nightly evaluation
            ds_description:
              type: string
              description: 任务描述。最多 200 个字符。如果多次定义，取最后一个值。
              example: Daily model evaluation batch
            ds_batch_finish_callback:
              type: string
              description: 可公开访问的回调 URL。任务完成时系统将发送包含任务状态的 POST 请求。
              example: https://example.com/callback
          example:
            ds_name: Task name
            ds_description: Task description
    BatchObject:
      type: object
      properties:
        id:
          type: string
          description: 批量任务唯一标识符。
          example: batch_abc123
        object:
          type: string
          enum:
            - batch
          description: 固定为 `"batch"`。
        endpoint:
          type: string
          description: 该批量任务使用的 API 接口路径。
          example: /v1/chat/completions
        errors:
          type: object
          nullable: true
          description: 批量处理过程中遇到的错误。
          properties:
            object:
              type: string
              enum:
                - list
              description: 固定为 `"list"`。
            data:
              type: array
              description: 错误详情列表。
              items:
                $ref: "#/components/schemas/BatchError"
        input_file_id:
          type: string
          description: 输入文件的 ID。
          example: file-abc123
        completion_window:
          type: string
          description: 批量任务的完成时间窗口。
          example: 24h
        status:
          type: string
          enum:
            - validating
            - in_progress
            - finalizing
            - completed
            - failed
            - expired
            - cancelling
            - cancelled
          description: 批量任务的当前状态。`validating`：正在验证输入文件。`in_progress`：正在处理中。`finalizing`：正在汇总结果。`completed`：所有请求已完成。`failed`：任务失败。`expired`：任务超过完成时间窗口。`cancelling`：正在取消中。`cancelled`：任务已取消。
        output_file_id:
          type: string
          nullable: true
          description: 包含成功结果的文件 ID。状态为 `completed` 时可用。通过下载文件内容接口获取。
          example: file-xyz789
        error_file_id:
          type: string
          nullable: true
          description: 包含错误详情的文件 ID。部分请求失败时可用。通过下载文件内容接口获取。
          example: file-err456
        created_at:
          type: integer
          description: 批量任务创建时间的 Unix 时间戳（秒）。
          example: 1735113344
        in_progress_at:
          type: integer
          nullable: true
          description: 批量任务开始处理时间的 Unix 时间戳（秒）。
        expires_at:
          type: integer
          nullable: true
          description: 批量任务预计过期时间的 Unix 时间戳（秒）。根据创建时间和 `completion_window` 计算得出。
        finalizing_at:
          type: integer
          nullable: true
          description: 批量任务开始汇总结果时间的 Unix 时间戳（秒）。
        completed_at:
          type: integer
          nullable: true
          description: 批量任务完成时间的 Unix 时间戳（秒）。
        failed_at:
          type: integer
          nullable: true
          description: 批量任务失败时间的 Unix 时间戳（秒）。
        expired_at:
          type: integer
          nullable: true
          description: 批量任务实际过期时间的 Unix 时间戳（秒）。仅当任务状态为 `expired` 时有值。
        cancelled_at:
          type: integer
          nullable: true
          description: 批量任务取消时间的 Unix 时间戳（秒）。
        cancelling_at:
          type: integer
          nullable: true
          description: 批量任务进入取消中状态的 Unix 时间戳（秒）。
        request_counts:
          type: object
          description: 请求处理计数。
          properties:
            total:
              type: integer
              description: 批量任务中的总请求数。
            completed:
              type: integer
              description: 成功完成的请求数。
            failed:
              type: integer
              description: 失败的请求数。
        metadata:
          type: object
          nullable: true
          description: 附加到批量任务的键值对元数据。
          additionalProperties:
            type: string
          properties:
            ds_name:
              type: string
              description: 任务名称。
            ds_description:
              type: string
              description: 任务描述。
    BatchError:
      type: object
      properties:
        code:
          type: string
          description: 错误代码。
        message:
          type: string
          description: 人类可读的错误消息。
        param:
          type: string
          nullable: true
          description: 导致错误的参数。
        line:
          type: integer
          nullable: true
          description: 输入文件中导致错误的行号。
    BatchResultLine:
      type: object
      description: 输出 JSONL 文件中的一行，表示一个批量请求的结果。
      properties:
        id:
          type: string
          description: 结果唯一标识符。
        custom_id:
          type: string
          description: 对应输入请求中的 custom_id，用于匹配结果。
          example: "1"
        response:
          type: object
          nullable: true
          description: 该请求的响应数据。
          properties:
            status_code:
              type: integer
              description: 响应的 HTTP 状态码。
              example: 200
            request_id:
              type: string
              description: 服务端生成的请求唯一 ID。
              example: c308ef7f-0824-9c46-96eb-73566f062426
            body:
              type: object
              description: 响应体，格式与对应 API 的响应格式一致（如 chat completion 或 embedding 响应）。
              properties:
                id:
                  type: string
                  description: 补全结果唯一标识符。
                created:
                  type: integer
                  description: 补全结果创建时间的 Unix 时间戳（秒）。
                object:
                  type: string
                  description: 对象类型（如 `chat.completion`）。
                model:
                  type: string
                  description: 用于生成补全的模型。
                choices:
                  type: array
                  description: 生成的回复列表。
                  items:
                    type: object
                    properties:
                      index:
                        type: integer
                        description: 该选项的索引。
                      message:
                        type: object
                        properties:
                          role:
                            type: string
                            description: 固定为 `assistant`。
                          content:
                            type: string
                            description: 生成的文本。
                      finish_reason:
                        type: string
                        description: 生成停止的原因。
                usage:
                  type: object
                  description: Token 用量。
                  properties:
                    prompt_tokens:
                      type: integer
                    completion_tokens:
                      type: integer
                    total_tokens:
                      type: integer
        error:
          type: object
          nullable: true
          description: 请求失败时的错误信息。成功时为 `null`。
          properties:
            code:
              type: string
              description: 错误代码。
            message:
              type: string
              description: 错误消息。
    ErrorResponse:
      type: object
      properties:
        error:
          type: object
          properties:
            message:
              type: string
              description: 错误消息。
            type:
              type: string
              description: 错误类型。
            code:
              type: string
              description: 错误代码。
            param:
              type: string
              nullable: true
              description: 导致错误的参数。
    ListBatchesResponse:
      type: object
      properties:
        object:
          type: string
          enum:
            - list
          description: 固定为 `list`。
        data:
          type: array
          description: 批量任务对象列表。
          items:
            $ref: "#/components/schemas/BatchObject"
        first_id:
          type: string
          nullable: true
          description: 列表中第一个批量任务的 ID。
          example: batch_abc123
        last_id:
          type: string
          nullable: true
          description: 列表中最后一个批量任务的 ID。
          example: batch_abc456
        has_more:
          type: boolean
          description: 当前页之后是否还有更多批量任务。
````

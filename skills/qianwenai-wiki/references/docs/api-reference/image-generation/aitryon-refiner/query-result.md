> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# AI试衣精修 — 查询结果

> 查询AI试衣-图片精修任务的状态和结果

<Note>
  请先[获取 API Key](/api-reference/preparation/api-key) 并[设置为环境变量](/api-reference/preparation/export-api-key-env)。
</Note>

## OpenAPI

````yaml get /tasks/{task_id}
openapi: 3.1.0
info:
  title: Try-on Refiner API
  version: 1.0.0
  description: AI试衣-图片精修是一个后处理模型，可增强AI试衣生成图片的真实感与清晰度。
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
security:
  - BearerAuth: []
paths:
  /tasks/{task_id}:
    get:
      summary: Query task result
      operationId: getAitryonRefinerTaskResult
      description: 查询AI试衣-图片精修任务的状态和结果。
      parameters:
        - name: task_id
          in: path
          required: true
          schema:
            type: string
          description: 任务ID，从创建任务的响应中获取。
      responses:
        "200":
          description: 查询成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/TaskStatusResponse"
              examples:
                SUCCEEDED:
                  summary: 任务成功完成
                  value:
                    request_id: 98d46cd0-1f90-9231-9a6c-xxxxxx
                    output:
                      task_id: 15991992-1487-40d4-ae66-xxxxxx
                      task_status: SUCCEEDED
                      submit_time: 2025-06-30 14:37:53.838
                      scheduled_time: 2025-06-30 14:37:53.858
                      end_time: 2025-06-30 14:38:11.472
                      image_url: https://dashscope-result-hz.oss-cn-hangzhou.aliyuncs.com/tryon.jpg?Expires=xxx
                    usage:
                      image_count: 1
                FAILED:
                  summary: 任务失败
                  value:
                    request_id: 6bf4693b-c6d0-933a-b7b7-xxxxxx
                    output:
                      task_id: e32bd911-5a3d-4687-bf53-xxxxxx
                      task_status: FAILED
                      code: InvalidParameter
                      message: The request is missing required parameters xxxxx
                RUNNING:
                  summary: 任务运行中
                  value:
                    request_id: 98d46cd0-1f90-9231-9a6c-xxxxxx
                    output:
                      task_id: 15991992-1487-40d4-ae66-xxxxxx
                      task_status: RUNNING
                      submit_time: 2025-06-30 14:37:53.838
                      scheduled_time: 2025-06-30 14:37:53.858
      x-codeSamples:
        - lang: curl
          label: cURL — Query task result
          source: |-
            # Replace {task_id} with the actual task ID from the submit response
            curl -X GET 'https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY"
components:
  schemas:
    AitryonRefinerRequest:
      type: object
      required:
        - model
        - input
        - parameters
      properties:
        model:
          type: string
          enum:
            - aitryon-refiner
          description: 模型名称，固定为 `aitryon-refiner`。
        input:
          type: object
          required:
            - top_garment_url
            - person_image_url
            - coarse_image_url
          properties:
            top_garment_url:
              type: string
              description: 上半身服装图片URL。图片大小范围5KB~5MB，图片分辨率范围150px~4096px（宽和高均需满足），支持格式：jpg、png、jpeg、bmp、heic。
            bottom_garment_url:
              type: string
              description: 下半身服装图片URL。图片大小范围5KB~5MB，图片分辨率范围150px~4096px（宽和高均需满足），支持格式：jpg、png、jpeg、bmp、heic。
            person_image_url:
              type: string
              description: 模特人台图片URL。图片中有且仅有一个完整人物。
            coarse_image_url:
              type: string
              description: AI试衣的结果图片URL。调用AI试衣接口时，需要设置 `resolution=-1` 和 `restore_face=true`。
        parameters:
          type: object
          required:
            - gender
          properties:
            gender:
              type: string
              enum:
                - woman
                - man
              description: 性别。可选值为 `woman` 或 `man`。
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
              description: 任务ID，用于后续查询任务结果。
            task_status:
              type: string
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - SUSPENDED
                - UNKNOWN
              description: 任务状态。提交成功后通常为 `PENDING`。
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
                - PRE-PROCESSING
                - RUNNING
                - POST-PROCESSING
                - SUCCEEDED
                - FAILED
                - UNKNOWN
                - CANCELED
              description: 任务状态。
            image_url:
              type: string
              description: 图片精修结果图片URL。24小时内有效。仅在任务成功时返回。
            submit_time:
              type: string
              description: 任务提交时间。
            scheduled_time:
              type: string
              description: 任务调度时间。
            end_time:
              type: string
              description: 任务结束时间。仅在任务完成时返回。
            code:
              type: string
              description: 错误码。仅在任务失败时返回。
            message:
              type: string
              description: 错误信息。仅在任务失败时返回。
        usage:
          type: object
          properties:
            image_count:
              type: integer
              description: 生成的图片数量。
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
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
````

> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# AI试衣精修 — 创建任务

> 提交AI试衣-图片精修任务

<Note>
  请先[获取 API Key](/api-reference/preparation/api-key) 并[设置为环境变量](/api-reference/preparation/export-api-key-env)。
</Note>

## OpenAPI

````yaml post /services/aigc/image2image/image-synthesis/
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
  /services/aigc/image2image/image-synthesis/:
    post:
      summary: Create task
      operationId: createAitryonRefinerTask
      description: 提交AI试衣-图片精修任务。该模型可增强AI试衣生成图片的真实感与清晰度。
      parameters:
        - name: X-DashScope-Async
          in: header
          required: true
          schema:
            type: string
            enum:
              - enable
          description: 必须设置为 `enable` 以使用异步模式。
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/AitryonRefinerRequest"
      responses:
        "200":
          description: 任务提交成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/AsyncTaskSubmitResponse"
              example:
                output:
                  task_status: PENDING
                  task_id: 0385dc79-5ff8-4d82-bcb6-xxxxxx
                request_id: 4909100c-7b5a-9f92-bfe5-xxxxxx
        "400":
          description: 请求参数错误
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
              examples:
                InvalidParameter:
                  summary: 缺少必传参数或格式错误
                  value:
                    code: InvalidParameter
                    message: The request is missing required parameters xxxxx
                    request_id: 7438d53d-6eb8-4596-8835-xxxxxx
                InvalidURL:
                  summary: 图片URL无法访问
                  value:
                    code: InvalidURL
                    message: The image URL is not accessible.
                    request_id: 7438d53d-6eb8-4596-8835-xxxxxx
                InvalidPerson:
                  summary: 未检测到人体或检测到多个人体
                  value:
                    code: InvalidPerson
                    message: No human body detected or multiple human bodies detected.
                    request_id: 7438d53d-6eb8-4596-8835-xxxxxx
                InvalidInputLength:
                  summary: 图片分辨率不合规
                  value:
                    code: InvalidInputLength
                    message: Image resolution is invalid.
                    request_id: 7438d53d-6eb8-4596-8835-xxxxxx
        "401":
          description: 认证失败
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
              example:
                code: InvalidApiKey
                message: No API-key provided.
                request_id: 7438d53d-6eb8-4596-8835-xxxxxx
        "429":
          description: 请求频率超限
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
              example:
                code: Throttling
                message: Requests throttling triggered.
                request_id: 7438d53d-6eb8-4596-8835-xxxxxx
      x-codeSamples:
        - lang: curl
          label: cURL
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis/' \
              --header 'X-DashScope-Async: enable' \
              --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
              --header 'Content-Type: application/json' \
              --data '{
                "model": "aitryon-refiner",
                "input": {
                    "top_garment_url": "https://dashscope-swap.oss-cn-beijing.aliyuncs.com/aa-test/sample-top.jpg",
                    "bottom_garment_url": "https://dashscope-swap.oss-cn-beijing.aliyuncs.com/aa-test/sample-bottom.jpg",
                    "person_image_url": "https://dashscope-swap.oss-cn-beijing.aliyuncs.com/aa-test/sample-person.png",
                    "coarse_image_url": "https://dashscope-swap.oss-cn-beijing.aliyuncs.com/aa-test/result.png"
                },
                "parameters": {
                    "gender": "woman"
                }
            }'
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

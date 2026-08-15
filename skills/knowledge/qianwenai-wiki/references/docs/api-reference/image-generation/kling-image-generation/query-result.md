> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 查询图像生成任务结果

> 通过 task_id 轮询查询可灵图像生成任务的执行状态与生成图像。

## OpenAPI

````yaml get /tasks/{task_id}
openapi: 3.0.0
info:
  title: 可灵图像生成 API
  description: 可灵图像生成模型支持文生图、参考图生图两种任务。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
paths:
  /tasks/{task_id}:
    get:
      summary: 查询图像生成任务结果
      description: 查询可灵图像生成任务的执行状态与结果。建议采用轮询机制，并设置合理的查询间隔（如5秒）。task_id 查询有效期为24小时。
      operationId: queryKlingImageGenerationTask
      parameters:
        - name: task_id
          in: path
          required: true
          description: 任务ID，由创建任务接口返回。
          schema:
            type: string
      responses:
        "200":
          description: 查询成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/QueryTaskResponse"
              examples:
                SUCCEEDED:
                  summary: 任务执行成功
                  value:
                    request_id: 95146d89-9d70-481a-8c16-xxxxxx
                    output:
                      task_id: 2c502d25-12a9-4517-8972-xxxxxx
                      task_status: SUCCEEDED
                      submit_time: 2026-03-27 22:46:01.536
                      scheduled_time: 2026-03-27 22:46:01.580
                      end_time: 2026-03-27 22:46:24.831
                      finished: true
                      choices:
                        - finish_reason: stop
                          message:
                            role: assistant
                            content:
                              - image: https://p4-fdl.klingai.com/xxx.png?xxx
                                type: image
                              - image: https://p4-fdl.klingai.com/xxx.png?xxx
                                type: image
                    usage:
                      size: 1024*1024
                      image_count: 2
                      SR: "1080"
                FAILED:
                  summary: 任务执行异常
                  value:
                    request_id: a4d78a5f-655f-9639-8437-xxxxxx
                    code: InvalidParameter
                    message: num_images_per_prompt must be 1
                RUNNING:
                  summary: 任务处理中
                  value:
                    request_id: b5e89c60-766g-0740-9548-yyyyyy
                    output:
                      task_id: 3d613e36-23ba-5628-9083-yyyyyy
                      task_status: RUNNING
      security:
        - BearerAuth: []
      x-codeSamples:
        - lang: curl
          label: 查询任务结果
          source: |-
            curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id} \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY"
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    KlingImageGenerationRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称。
          enum:
            - kling/kling-v3-image-generation
            - kling/kling-v3-omni-image-generation
        input:
          type: object
          required:
            - messages
          description: 输入参数对象。
          properties:
            messages:
              type: array
              description: 请求内容数组。当前仅支持单轮对话，因此数组内有且只有一个对象，该对象包含 `role` 和 `content` 两个属性。
              items:
                type: object
                properties:
                  role:
                    type: string
                    description: 消息的角色。此参数必须设置为 `user`。
                    enum:
                      - user
                  content:
                    type: array
                    description: 消息内容，包含文本提示词（text）和可选的参考图像（image，支持多张）。
                    items:
                      type: object
                      properties:
                        text:
                          type: string
                          description: 正向提示词，用于描述期望生成的图像内容、风格和构图。支持中英文，长度不超过2500个字符，每个汉字、字母、数字或符号计为一个字符，超过将返回错误。注意：仅支持传入一个text，不传或传入多个将报错。示例值：一只坐着的橘黄色的猫，表情愉悦，活泼可爱，逼真准确。
                        image:
                          type: string
                          description: 参考图像的URL。支持 HTTP 或 HTTPS 协议。示例值：https://xxx/xxx.png。图像限制：格式为JPEG、JPG、PNG（不支持透明通道）；宽和高的范围为[300, 8000]像素；宽高比在1:2.5 ~ 2.5:1之间；文件大小不超过10MB；参考图片数量和参考主体数量（element_list数组长度）之和不得超过10。
            element_list:
              type: array
              description: 主体列表，用于指定需要保持的主体。参考图片数量和参考主体数量（element_list数组长度）之和不得超过10。
              items:
                type: object
                properties:
                  element_id:
                    type: integer
                    description: 传 element_list 时必填，表示主体ID。请在可灵-主体ID列表获取主体ID。参考图片数量和参考主体数量（element_list数组长度）之和不得超过10。
        parameters:
          type: object
          description: 控制图像生成，比如图像张数、宽高比等。
          properties:
            n:
              type: integer
              description: |-
                生成的图像张数。
                - kling/kling-v3-image-generation：取值范围为1～9，默认值为1。
                - kling/kling-v3-omni-image-generation：当且仅当 `result_type=single` 时生效，取值范围为1～9，默认值为1。
            result_type:
              type: string
              description: |-
                生成图像的类型。仅支持模型 kling/kling-v3-omni-image-generation。
                - `single`（默认值）：单图。批量生成时仅风格相似，无分镜关联。
                - `series`：组图。生成具有叙事/视觉连续性的分镜系列图像。
              enum:
                - single
                - series
            series_amount:
              type: integer
              description: 组图模式下的输出张数。仅支持模型 kling/kling-v3-omni-image-generation。取值范围为2～9，默认值为4。当且仅当 `result_type=series` 时生效。
            aspect_ratio:
              type: string
              description: 输出图像的宽高比。示例值：16:9。
              enum:
                - 16:9
                - 9:16
                - 1:1
              default: 16:9
            resolution:
              type: string
              description: |-
                输出图像分辨率。
                - kling/kling-v3-image-generation：可选值为 `1k`、`2k`，默认值为 `1k`。
                - kling/kling-v3-omni-image-generation：可选值为 `1k`、`2k`、`4k`，默认值为 `1k`。
                示例值：1k。
              enum:
                - 1k
                - 2k
                - 4k
            watermark:
              type: boolean
              description: |-
                是否同时生成含水印的图像。水印位于图像右下角，文案固定为"可灵AI"。
                - `false`（默认值）：不生成含水印的图像。
                - `true`：同时生成含水印的图像。
                示例值：false。
              default: false
    CreateTaskResponse:
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
    QueryTaskResponse:
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
              description: 任务ID。
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
              description: 任务提交时间。
            scheduled_time:
              type: string
              description: 任务调度时间。
            end_time:
              type: string
              description: 任务结束时间。
            finished:
              type: boolean
              description: 任务是否已完成。
            choices:
              type: array
              description: 模型生成的输出内容。此数组仅包含一个元素。
              items:
                type: object
                properties:
                  finish_reason:
                    type: string
                    description: 任务停止原因，自然停止时为 `stop`。
                  message:
                    type: object
                    description: 模型返回的消息。
                    properties:
                      role:
                        type: string
                        description: 消息的角色，固定为 `assistant`。
                      content:
                        type: array
                        description: 生成的图像列表。
                        items:
                          type: object
                          properties:
                            type:
                              type: string
                              description: 输出内容的类型。固定为 `image`。
                            image:
                              type: string
                              description: 生成图像的URL，图像格式为PNG。链接有效期为30天，请及时下载并保存图像。
        usage:
          type: object
          description: 输出信息统计。只对成功的结果计数。
          properties:
            image_count:
              type: integer
              description: 生成图像的数量。
            size:
              type: string
              description: 生成图片的分辨率，格式为`宽*高`。示例值：1360*768。
            SR:
              type: string
              description: 生成图像的分辨率档位。示例值：1080。
        code:
          type: string
          description: 请求失败的错误码。请求成功时不会返回此参数。
        message:
          type: string
          description: 请求失败的详细信息。请求成功时不会返回此参数。
    ErrorResponse:
      type: object
      properties:
        code:
          type: string
          description: 请求失败的错误码。
        message:
          type: string
          description: 请求失败的详细信息。
        request_id:
          type: string
          description: 请求唯一标识。
````

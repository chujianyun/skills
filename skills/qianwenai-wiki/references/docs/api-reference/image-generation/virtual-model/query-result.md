> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 虚拟模特 — 查询结果

> 查询虚拟模特任务的状态和结果

<Note>
  请先[获取 API Key](/api-reference/preparation/api-key) 并[设置为环境变量](/api-reference/preparation/export-api-key-env)。
</Note>

## OpenAPI

````yaml get /tasks/{task_id}
openapi: 3.0.0
info:
  title: 万相-虚拟模特 API
  description: 万相-虚拟模特可以对上传的真人实拍商品展示图进行智能生成，将其中的模特和背景替换为心仪的内容，在保持人物姿态不变的情况下，使用虚拟模特对商品进行更加精美、多样的展示。支持各种与模特产生互动的商品，如手持小商品、服装、鞋靴、配饰等。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 北京
security:
  - BearerAuth: []
paths:
  /tasks/{task_id}:
    get:
      operationId: getVirtualModelTaskStatus
      summary: 根据任务ID查询结果
      description: 使用任务ID查询模型生成的结果。请持续轮询直至 `task_status` 为 `SUCCEEDED` 或 `FAILED`。任务数据（如任务状态、图像URL等）仅保留24小时，超时后会被自动清除，请及时保存生成的图像。
      parameters:
        - name: task_id
          in: path
          required: true
          description: 创建任务接口返回的任务ID。
          schema:
            type: string
          example: 0385dc79-5ff8-4d82-bcb6-xxxxxx
      responses:
        "200":
          description: 获取任务状态成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/TaskStatusResponse"
              examples:
                SUCCEEDED:
                  summary: 任务执行成功
                  value:
                    request_id: f24149fe-4722-9763-xxxxxx
                    output:
                      task_id: 9d62befa-0139-4e4d-xxxxxx
                      task_status: SUCCEEDED
                      submit_time: 2025-04-24 10:51:35.004
                      scheduled_time: 2025-04-24 10:51:35.033
                      end_time: 2025-04-24 10:51:59.424
                      results:
                        - url: https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/test_1.png
                        - url: https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/test_2.png
                      task_metrics:
                        TOTAL: 2
                        SUCCEEDED: 2
                        FAILED: 0
                    usage:
                      image_count: 2
                FAILED:
                  summary: 任务执行失败
                  value:
                    request_id: f24149fe-4722-9763-xxxxxx
                    output:
                      task_id: 9d62befa-0139-4e4d-xxxxxx
                      task_status: FAILED
                      submit_time: 2024-05-16 13:50:23.001
                      scheduled_time: 2024-05-16 13:50:23.033
                      end_time: 2024-05-16 13:51:05.412
                      code: InvalidImageResolution
                      message: The input image resolution is too large or small
                    usage:
                      image_count: 0
                RUNNING:
                  summary: 任务处理中
                  value:
                    request_id: c1209113-8437-424f-a386-xxxxxx
                    output:
                      task_id: 0385dc79-5ff8-4d82-bcb6-xxxxxx
                      task_status: RUNNING
                      task_metrics:
                        TOTAL: 1
                        SUCCEEDED: 0
                        FAILED: 0
        "400":
          description: 请求参数无效
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
      x-codeSamples:
        - lang: curl
          label: cURL — 获取任务结果
          source: |-
            curl --location --request GET 'https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY"
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    VirtualModelRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: |-
            调用的模型名称。
            - `wanx-virtualmodel`：虚拟模特V1版本，支持 `short_side_size` 取值 `"512"` 和 `"1024"`，支持 `predefined_face_id`。
            - `virtualmodel-v2`：虚拟模特V2版本，支持 `short_side_size` 取值 `"1024"` 和 `"2048"`，支持 `bgstyle_scale`、`realPerson`、`style`、`seed`、`aspect_ratio`。
          enum:
            - wanx-virtualmodel
            - virtualmodel-v2
          example: virtualmodel-v2
        input:
          type: object
          required:
            - base_image_url
            - mask_image_url
            - prompt
            - face_prompt
          description: 输入图像的基本信息，比如图像URL地址。
          properties:
            base_image_url:
              type: string
              format: uri
              description: |-
                原始真人展示图像URL地址。

                URL需为公网可访问的地址，并支持HTTP或HTTPS协议。

                图像限制：
                - 图像格式：JPEG、JPG、PNG、WEBP。
                - 图像分辨率：不低于256×256像素且不超过4096×4096像素，人脸占比不低于128×128像素。
                - 长宽比：大于1:2且小于2:1。
                - 图像大小：不超过5MB。
                - URL地址中不能包含中文字符。
              example: https://example.com/model.jpg
            mask_image_url:
              type: string
              format: uri
              description: |-
                对应原图的期望保留区域mask图URL，图片为（0,255）的黑白图，其中白色表示商品主体区域。

                URL需为公网可访问的地址，并支持HTTP或HTTPS协议。

                图片限制：
                - 图像格式：JPEG、JPG、PNG、WEBP。
                - 图像分辨率：与base_image_url参数对应的图像保持一致。
                - 长宽比：大于1:2且小于2:1。
                - 图像大小：不超过5MB。
                - URL地址中不能包含中文字符。
              example: https://example.com/mask.png
            prompt:
              type: string
              description: |-
                针对生成图像背景环境、模特的全身形象描述。支持中英文，小于100字符。

                示例：一名年轻女子，身穿白色短裤，极简风格调色板，长镜头，双色效果，暗银色和浅粉色。
              maxLength: 100
              example: 一名年轻女子，身穿白色短裤，极简风格调色板
            face_prompt:
              type: string
              description: |-
                生成人像面部描述。支持中英文，小于100字符。

                示例：年轻女子，面容姣好，最高品质。
              maxLength: 100
              example: 年轻女子，面容姣好，最高品质
            predefined_face_id:
              type: string
              description: |-
                预设人物ID。仅在V1版本（wanx-virtualmodel）使用。优先级高于face_image_url。

                枚举值：`girl1`、`girl2`、`girl3`、`boy1`、`boy2`、`boy3`。
              enum:
                - girl1
                - girl2
                - girl3
                - boy1
                - boy2
                - boy3
            face_image_url:
              type: string
              format: uri
              description: |-
                期望替换的人物图像URL地址。优先级低于predefined_face_id参数。

                图片限制：
                - 图像格式：JPEG、JPG、PNG、WEBP。
                - 图像分辨率：长边像素不大于2048，人脸区域大于128×128像素。
                - 图像大小：建议不超过5MB。
                - URL地址中不能包含中文字符。
              example: https://example.com/face.jpg
            background_image_url:
              type: string
              format: uri
              description: |-
                背景环境参考图像URL地址。仅在V2版本（virtualmodel-v2）使用。

                URL需为公网可访问的地址，并支持HTTP或HTTPS协议。

                图片限制：
                - 图像格式：JPEG、JPG、PNG、WEBP。
                - 图像分辨率：图像长边像素不大于4096。
                - 图像比例：长宽比小于等于2。
                - 图像大小：不超过5MB。
                - URL地址中不能包含中文字符。
              example: https://example.com/background.jpg
            bgstyle_scale:
              type: number
              description: |-
                背景参考图像权重控制。仅在V2版本（virtualmodel-v2）使用。

                取值范围：[0.0, 1.0]，默认0.7。数值越大表示参考程度越大。
              minimum: 0
              maximum: 1
              default: 0.7
              example: 0.7
            realPerson:
              type: boolean
              description: |-
                输入图片是否是真人。仅在V2版本（virtualmodel-v2）使用。
                - `true`（默认）：表示输入图像是真人。
                - `false`：表示输入图像是人台或者非真人。
              default: true
            style:
              type: string
              description: |-
                生成图片风格。仅在V2版本（virtualmodel-v2）使用。
                - `"portrait"`（默认）：增加景深，突出人像效果。
                - `""`（空字符串）：标准风格。
              enum:
                - portrait
                - ""
              default: portrait
            seed:
              type: integer
              description: |-
                控制生成seed。仅在V2版本（virtualmodel-v2）使用。

                取值范围：[-1,10000000]。默认值为-1，表示系统随机内置seed。同样的seed值会生成相同的结果。
              minimum: -1
              maximum: 10000000
            aspect_ratio:
              type: string
              description: |-
                生成图片长宽比例。仅在V2版本（virtualmodel-v2）使用。

                可选值：`unchanged`（比例不变，默认值）、`2:1`、`16:9`、`4:3`、`1:1`、`3:4`、`9:16`、`1:2`。
              enum:
                - unchanged
                - 2:1
                - 16:9
                - 4:3
                - 1:1
                - 3:4
                - 9:16
                - 1:2
              default: unchanged
        parameters:
          type: object
          description: 生成参数。
          properties:
            short_side_size:
              type: string
              description: |-
                指定生成的图像短边大小，单位：像素。生成图片和输入原图会保持相同的长宽比。
                - V1版本（wanx-virtualmodel）可选值：`"512"` 和 `"1024"`。
                - V2版本（virtualmodel-v2）可选值：`"1024"` 和 `"2048"`。
              enum:
                - "512"
                - "1024"
                - "2048"
              example: "1024"
            n:
              type: integer
              description: 生成图像的数量。取值范围：[1, 4]，默认值 1。
              minimum: 1
              maximum: 4
              default: 1
              example: 1
    AsyncTaskSubmitResponse:
      type: object
      description: 异步任务提交响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识。可用于请求明细溯源和问题排查。
          example: 4909100c-7b5a-9f92-bfe5-28c7cece6b47
        output:
          type: object
          description: 任务输出信息。
          properties:
            task_id:
              type: string
              description: 任务ID。用于轮询 GET /tasks/{task_id} 查询结果。
              example: 0385dc79-5ff8-4d82-bcb6-xxxxxx
            task_status:
              type: string
              description: 任务状态。初始状态通常为 `PENDING`。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - SUSPENDED
                - UNKNOWN
    TaskStatusResponse:
      type: object
      description: 任务状态查询响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识。可用于请求明细溯源和问题排查。
          example: f24149fe-4722-9763-xxxxxx
        output:
          type: object
          description: 任务输出信息。
          properties:
            task_id:
              type: string
              description: 任务ID。
              example: 9d62befa-0139-4e4d-xxxxxx
            task_status:
              type: string
              description: |-
                任务状态。
                - `PENDING`：排队中
                - `RUNNING`：处理中
                - `SUSPENDED`：挂起
                - `SUCCEEDED`：执行成功
                - `FAILED`：执行失败
                - `UNKNOWN`：任务不存在或状态未知
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - SUSPENDED
                - UNKNOWN
            submit_time:
              type: string
              description: 任务提交时间。
              example: 2025-04-24 10:51:35.004
            scheduled_time:
              type: string
              description: 任务排期执行时间。
              example: 2025-04-24 10:51:35.033
            end_time:
              type: string
              description: 任务完成时间。
              example: 2025-04-24 10:51:59.424
            results:
              type: array
              description: 任务结果列表，包括图像URL。仅在 `task_status` 为 `SUCCEEDED` 时返回。
              items:
                type: object
                properties:
                  url:
                    type: string
                    format: uri
                    description: 模型生成图片的URL地址。
                    example: https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/test_1.png
            result_url:
              type: string
              format: uri
              description: 输出图片URL。
            code:
              type: string
              description: 任务执行失败的错误码。仅在 `task_status` 为 `FAILED` 时返回。
              example: InvalidImageResolution
            message:
              type: string
              description: 任务执行失败的详细信息。仅在 `task_status` 为 `FAILED` 时返回。
              example: The input image resolution is too large or small
            task_metrics:
              type: object
              description: 任务信息统计指标。
              properties:
                TOTAL:
                  type: integer
                  description: 总的任务数。
                  example: 2
                SUCCEEDED:
                  type: integer
                  description: 任务状态为成功的任务数。
                  example: 2
                FAILED:
                  type: integer
                  description: 任务状态为失败的任务数。
                  example: 0
        usage:
          type: object
          description: 输出信息统计。仅在任务成功时返回。
          properties:
            image_count:
              type: integer
              description: 模型生成图像的数量。
              example: 2
    DashScopeErrorResponse:
      type: object
      description: DashScope API错误响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识。
          example: fb53c4ec-1c12-4fc4-a580-cdb7c3261fc1
        code:
          type: string
          description: 接口错误码。接口成功请求不会返回该参数。
          example: InvalidParameter
        message:
          type: string
          description: 接口错误信息。接口成功请求不会返回该参数。
          example: The request is missing required parameters or in a wrong format, please check the parameters that you send.
````

> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 人物写真生成 — 查询结果

> 查询FaceChain人物写真生成任务的状态和结果

<Note>
  请先[获取 API Key](/api-reference/preparation/api-key) 并[设置为环境变量](/api-reference/preparation/export-api-key-env)。
</Note>

## OpenAPI

````yaml get /tasks/{task_id}
openapi: 3.1.0
info:
  title: 人物写真生成 FaceChain API
  description: 基于 FaceChain 模型生成人物写真。支持两种模式：人物形象训练 LoRA 模式（需先完成人物形象训练）和人物形象免训练 TrainFree 模式（推荐，无需训练，一键极速生成）。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 千问AI平台
security:
  - BearerAuth: []
paths:
  /tasks/{task_id}:
    get:
      operationId: getFaceChainGenerationTaskStatus
      summary: 查询人物写真生成任务状态
      description: 轮询人物写真生成任务的状态和结果。持续轮询直到 `task_status` 为 `SUCCEEDED` 或 `FAILED`。结果图像的 URL 有效期为 24 小时，请及时下载或转存。
      parameters:
        - name: task_id
          in: path
          required: true
          description: 提交人物写真生成任务时返回的任务 ID。
          schema:
            type: string
          example: 86ecf553-d340-4e21-af6e-a0c6a421c010
      responses:
        "200":
          description: 获取任务状态成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/TaskStatusResponse"
              examples:
                SUCCEEDED:
                  summary: 任务成功
                  value:
                    request_id: 0b6a411a-56e6-9028-84eb-6852183248d8
                    output:
                      task_id: 7eb1032e-09a1-4df5-96ed-14091859ad57
                      task_status: SUCCEEDED
                      submit_time: 2025-08-15 10:20:22.629
                      scheduled_time: 2025-08-15 10:20:22.655
                      end_time: 2025-08-15 10:20:50.540
                      results:
                        - url: https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx/image1.jpg
                        - url: https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx/image2.jpg
                        - url: https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx/image3.jpg
                        - url: https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx/image4.jpg
                      task_metrics:
                        TOTAL: 4
                        SUCCEEDED: 4
                        FAILED: 0
                    usage:
                      image_count: 4
                FAILED:
                  summary: 任务失败
                  value:
                    request_id: f24149fe-4722-9763-xxxxxx
                    output:
                      task_id: 9d62befa-0139-4e4d-xxxxxx
                      task_status: FAILED
                      submit_time: 2025-08-15 10:20:22.629
                      scheduled_time: 2025-08-15 10:20:22.655
                      end_time: 2025-08-15 10:20:50.540
                      code: InvalidImageResolution
                      message: The input image resolution is too large or small
                    usage:
                      image_count: 0
                RUNNING:
                  summary: 任务处理中
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
          description: 请求参数错误
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
      x-codeSamples:
        - lang: curl
          label: 查询任务状态
          source: |-
            curl -X GET 'https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}' \
              --header 'Authorization: Bearer $DASHSCOPE_API_KEY'
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    FaceChainGenerationRequest:
      type: object
      required:
        - model
      properties:
        model:
          type: string
          description: 模型名称。此处固定为 `facechain-generation`。
          enum:
            - facechain-generation
          example: facechain-generation
        resources:
          type: array
          description: 人物形象 LoRA 资源列表。使用预设风格或自定义模板模式（非免训练模式）时为必填，从人物形象训练 API 获取。使用免训练模式（TrainFree）时无需填写，填写也会被忽略。
          items:
            type: object
            properties:
              resource_id:
                type: string
                description: 模型定制得到的 LoRA 数据 ID，从人物形象训练任务的成功结果中获取。
                example: women_model
              resource_type:
                type: string
                description: 资源类型。固定为 `facelora`。
                enum:
                  - facelora
                example: facelora
        parameters:
          type: object
          description: 生成参数。
          properties:
            style:
              type: string
              description: |-
                输出图像的预设风格或自定义模板模式。

                **预设风格**（需要 LoRA 资源）：
                - `f_idcard_male` — 证件照男
                - `f_business_male` — 商务写真男
                - `f_idcard_female` — 证件照女
                - `f_business_female` — 商务写真女
                - `m_springflower_female` — 春日花园
                - `f_summersport_female` — 夏日运动
                - `f_autumnleaf_female` — 秋日印象
                - `m_winterchinese_female` — 冬日国风
                - `f_hongkongvintage_female` — 港风复古
                - `f_lightportray_female` — 轻写真

                **自定义模板模式**：
                - `portrait_url_template` — 自定义模板 + LoRA（需传入 `input.template_url` 和 LoRA 资源）
                - `train_free_portrait_url_template` — 自定义模板免训练（需传入 `input.template_url` 和 `input.user_urls`，无需 LoRA 资源）
              example: f_idcard_female
            size:
              type: string
              description: 生成图像的分辨率。目前支持 `768*1024`。使用自定义模板模式或免训练模式时不需要该参数。
              example: 768*1024
            n:
              type: integer
              description: 生成图片数量。取值范围 `1~5`，默认值为 `4`。
              minimum: 1
              maximum: 5
              default: 4
              example: 4
            skin_retouch:
              type: boolean
              description: 免训练写真生成时是否对输入用户图进行自动美颜处理。默认为 `true`（自动美颜），可设置为 `false`（不美颜，用户可自行前后处理）。
              default: true
        input:
          type: object
          description: 自定义模板模式下的输入数据。
          properties:
            template_url:
              type: string
              format: uri
              description: |-
                用户自定义模板的 URL 链接。当 `parameters.style` 为 `portrait_url_template` 或 `train_free_portrait_url_template` 时为必填。

                - **格式**：JPEG、JPG、PNG
                - **大小**：不超过 5MB
                - **分辨率**：512×512 ~ 1680×1260 像素
                - **要求**：单人、清晰且高质量的风格模板图，人脸无遮挡和模糊。URL 中不能包含中文字符。
              example: https://example.com/template.jpg
            user_urls:
              type: array
              description: |-
                一组包含用户正脸单人照的 URL 链接。当 `parameters.style` 为 `train_free_portrait_url_template` 时为必填。至少 1 张，最多 5 张，需通过人物图像检测 API（facechain-facedetect）验证通过。

                - **格式**：JPEG、JPG、PNG
                - **大小**：每张不超过 3MB
                - **分辨率**：256×256 ~ 2048×2048 像素
                - **人脸**：占比不低于 128×128 像素
                - **要求**：清晰正脸单人照，人脸角度不超过 15 度。URL 中不能包含中文字符。
              items:
                type: string
                format: uri
              minItems: 1
              maxItems: 5
              example:
                - https://example.com/face.jpg
    AsyncTaskSubmitResponse:
      type: object
      description: 异步任务提交接口的响应。
      properties:
        request_id:
          type: string
          description: 本次请求的系统唯一码。
          example: 0b6a411a-56e6-9028-84eb-6852183248d8
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 提交异步任务的作业 ID。实际作业结果需要通过异步任务查询接口获取。
              example: 7eb1032e-09a1-4df5-96ed-14091859ad57
            task_status:
              type: string
              description: 提交异步任务后的作业状态，初始状态通常为 `PENDING`。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - UNKNOWN
    TaskStatusResponse:
      type: object
      description: 查询任务状态接口的响应。
      properties:
        request_id:
          type: string
          description: 本次请求的系统唯一码。
          example: e5d70b02-ebd3-98ce-9fe8-759d7d7b107d
        output:
          type: object
          description: 任务输出信息。
          properties:
            task_id:
              type: string
              description: 任务 ID。
              example: 86ecf553-d340-4e21-af6e-a0c6a421c010
            task_status:
              type: string
              description: |-
                被查询作业的作业状态。

                - `PENDING` — 排队中
                - `RUNNING` — 处理中
                - `SUCCEEDED` — 成功
                - `FAILED` — 失败
                - `UNKNOWN` — 作业不存在或状态未知
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - UNKNOWN
            submit_time:
              type: string
              description: 任务提交时间（UTC+8），格式为 `YYYY-MM-DD HH:mm:ss.SSS`。
              example: 2025-08-15 10:20:22.629
            scheduled_time:
              type: string
              description: 任务开始执行的时间（UTC+8），格式为 `YYYY-MM-DD HH:mm:ss.SSS`。
              example: 2025-08-15 10:20:22.655
            end_time:
              type: string
              description: 任务完成时间（UTC+8），格式为 `YYYY-MM-DD HH:mm:ss.SSS`。
              example: 2025-08-15 10:20:50.540
            results:
              type: array
              description: 生成的图像结果。仅当 `task_status` 为 `SUCCEEDED` 时返回。
              items:
                type: object
                properties:
                  url:
                    type: string
                    format: uri
                    description: 生成图像的 URL。有效期 24 小时，请及时下载。
                    example: https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx/image1.jpg
            result_url:
              type: string
              format: uri
              description: 包含模型生成结果的 URL，可在 24 小时内随时下载。输出图像分辨率为 768×1024。仅当 `task_status` 为 `SUCCEEDED` 时返回。
            code:
              type: string
              description: 错误码。仅当 `task_status` 为 `FAILED` 时返回。
              example: InvalidImageResolution
            message:
              type: string
              description: 错误详细信息。仅当 `task_status` 为 `FAILED` 时返回。
              example: The input image resolution is too large or small
            task_metrics:
              type: object
              description: 任务完成指标。
              properties:
                TOTAL:
                  type: integer
                  description: 子任务总数。
                  example: 4
                SUCCEEDED:
                  type: integer
                  description: 成功的子任务数。
                  example: 4
                FAILED:
                  type: integer
                  description: 失败的子任务数。
                  example: 0
        usage:
          type: object
          description: 本次请求的计量信息。
          properties:
            image_count:
              type: integer
              description: 本次请求生成图像的数量。
              example: 4
    DashScopeErrorResponse:
      type: object
      description: DashScope API 错误响应。
      properties:
        request_id:
          type: string
          description: 本次请求的系统唯一码。
          example: fb53c4ec-1c12-4fc4-a580-cdb7c3261fc1
        code:
          type: string
          description: 错误码。可能值包括 `InvalidParameter`（参数无效）、`InvalidURL`（URL 无效）、`InvalidImageResolution`（图像分辨率无效）、`InvalidParameter.DataInspection`（数据安全审查无法访问资源）、`BadRequest.EmptyModel`（缺少必选参数 model）、`Resource.AccessDenied`（资源无访问权限）、`InvalidApiKey`（API Key 无效）、`InternalError.Algo`（算法内部错误）。
          example: InvalidParameter
        message:
          type: string
          description: 错误详情。
          example: The request is missing required parameters or the parameters are out of the specified range, please check the parameters that you send
````

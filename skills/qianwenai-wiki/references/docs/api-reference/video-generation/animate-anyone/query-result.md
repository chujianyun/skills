> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# AnimateAnyone — 查询结果

> 查询舞动人像视频生成状态

查询任务状态并获取生成的视频。

## 轮询策略

1. 调用[创建任务](/api-reference/video-generation/animate-anyone/create-task)接口获取 `task_id`。
2. 每 **15 秒**轮询一次，直到 `task_status` 为 `SUCCEEDED` 或 `FAILED`。
3. 任务成功后，从 `output.video_url` 获取视频。

## 注意事项

- **URL 有效期**：视频 URL 在 **24 小时**后过期，请及时下载。
- **状态流转**：`PENDING` → `PRE-PROCESSING` → `RUNNING` → `POST-PROCESSING` → `SUCCEEDED` 或 `FAILED`。`UNKNOWN` 表示任务不存在或已过期。

## OpenAPI

````yaml get /tasks/{task_id}
openapi: 3.1.0
info:
  title: 舞动人像 AnimateAnyone 视频生成 API
  description: AnimateAnyone模型，可基于AnimateAnyone-template模型生成的动作模板，以及通过AnimateAnyone-detect模型检测的人物图像生成人物动作视频。本文档介绍了该模型提供的视频生成能力的API调用方法。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: DashScope API
security:
  - BearerAuth: []
paths:
  /tasks/{task_id}:
    get:
      operationId: getAnimateAnyoneTaskStatus
      summary: 根据任务ID查询结果
      description: 查询异步任务的状态及结果。异步任务查询接口提供 20 QPS 的访问流量限制。若有更高频次的查询需求，可通过EventBridge配置事件转发。已提交的异步任务列表查询和异步任务的取消管理，详见管理异步任务接口。
      parameters:
        - name: Authorization
          in: header
          required: true
          description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
          schema:
            type: string
            example: Bearer $DASHSCOPE_API_KEY
        - name: task_id
          in: path
          required: true
          description: 需要查询任务的task_id。
          schema:
            type: string
            example: a8532587-fa8c-4ef8-82be-0c46b17950d1
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
                    request_id: 7574ee8f-38a3-4b1e-9280-xxxxxx
                    output:
                      task_id: a8532587-fa8c-4ef8-82be-xxxxxx
                      task_status: SUCCEEDED
                      video_url: https://xxx/1.mp4
                    usage:
                      video_duration: 10.23
                      video_ratio: standard
                FAILED:
                  summary: 任务失败
                  value:
                    request_id: 7574ee8f-38a3-4b1e-9280-xxxxxx
                    output:
                      task_id: a8532587-fa8c-4ef8-82be-xxxxxx
                      task_status: FAILED
                      code: xxx
                      message: xxxxxx
                RUNNING:
                  summary: 任务处理中
                  value:
                    request_id: 7574ee8f-38a3-4b1e-9280-xxxxxx
                    output:
                      task_id: a8532587-fa8c-4ef8-82be-xxxxxx
                      task_status: RUNNING
        "400":
          description: 请求无效
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
      x-codeSamples:
        - lang: curl
          label: cURL - 查询任务结果
          source: |-
            # 将 {task_id} 替换为提交响应中返回的实际任务ID
            curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id} \
              --header "Authorization: Bearer $DASHSCOPE_API_KEY"
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    AnimateAnyoneRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 指明需要调用的模型。
          enum:
            - animate-anyone-gen2
          example: animate-anyone-gen2
        input:
          type: object
          required:
            - image_url
            - template_id
          description: 输入数据，包含人物图片和动作模板。
          properties:
            image_url:
              type: string
              description: |-
                用户上传的图片 URL，该图应先通过AnimateAnyone 图像检测API，并结合所需生成的画幅进行适当裁剪。

                **图像要求：**
                - 格式：JPG、PNG、JPEG 或 BMP
                - 文件大小：＜5M
                - 宽高比：≤2
                - 最大边长：≤4096像素

                **说明：**上传文件支持HTTP或HTTPS链接方式，不支持本地链接方式。您也可在此获取临时公网URL。
              example: http://aaa/bbb.jpg
            template_id:
              type: string
              description: |-
                动作模板ID，用于指明所需使用的动作模板。应输入AnimateAnyone 动作模板生成API生成的template_id。

                **说明：**动作模板ID会进行权限校验，请确保所使用的template_id是由当前的云账号创建得到的。

                **使用建议：**提高模板视频的分辨率和帧率，可有效提升生成视频的画质效果。
              example: AACT.xxx.xxx-xxx.xxx
        parameters:
          $ref: "#/components/schemas/AnimateAnyoneParameters"
    AnimateAnyoneParameters:
      type: object
      description: 视频生成参数配置。
      properties:
        use_ref_img_bg:
          type: boolean
          description: |-
            生成视频的背景控制，可设值为true或false。
            - 设true时将以输入图片的画面为背景生成视频（按图片背景生成）。
            - 设false时将以模板文件的原视频画面为背景生成视频（按视频背景生成）。默认值为false。

            **说明：**按视频背景生成时，需将图片中人像匹配到视频中人像的对应位置。对于半身人像图中未出现的区域（如腿部），模型将随机生成补全，有较大不确定性，故不推荐在该条件下做视频生成。
          default: false
          example: false
        video_ratio:
          type: string
          description: |-
            选择按图片背景生成视频时，可选画幅为 "9:16"或"3:4"，默认为"9:16"。

            **说明：**选择按视频背景生成时，即use_ref_img_bg设false时，该参数不生效。将按模板视频的比例生成新视频。

            **说明：**应确保输入图像的画幅与所选画幅一致，以避免生成视频的画面变形。
          enum:
            - 9:16
            - 3:4
          default: 9:16
          example: 9:16
    AsyncTaskSubmitResponse:
      type: object
      description: 异步任务提交响应。
      properties:
        request_id:
          type: string
          description: 本次请求的系统唯一码。
          example: 7574ee8f-38a3-4b1e-9280-11c33ab46e51
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 提交异步任务的任务ID，实际任务结果需要通过异步任务查询接口获取。
              example: a8532587-fa8c-4ef8-82be-0c46b17950d1
            task_status:
              type: string
              description: 提交异步任务后的任务状态。
              enum:
                - PENDING
                - PRE-PROCESSING
                - RUNNING
                - POST-PROCESSING
                - SUCCEEDED
                - FAILED
                - UNKNOWN
              example: PENDING
    TaskStatusResponse:
      type: object
      description: 异步任务查询响应。
      properties:
        request_id:
          type: string
          description: 本次请求的系统唯一码。
          example: 7574ee8f-38a3-4b1e-9280-11c33ab46e51
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 查询任务的 task_id。
              example: a8532587-fa8c-4ef8-82be-0c46b17950d1
            task_status:
              type: string
              description: 被查询任务的任务状态。
              enum:
                - PENDING
                - PRE-PROCESSING
                - RUNNING
                - POST-PROCESSING
                - SUCCEEDED
                - FAILED
                - UNKNOWN
              x-enumDescriptions:
                PENDING: 排队中
                PRE-PROCESSING: 前置处理中
                RUNNING: 处理中
                POST-PROCESSING: 后置处理中
                SUCCEEDED: 成功
                FAILED: 失败
                UNKNOWN: 任务不存在或状态未知
            video_url:
              type: string
              description: 平台输出的视频结果，**video_url有效期为任务完成后24小时**。
              example: https://xxx/1.mp4
            code:
              type: string
              description: 错误码。仅在任务失败时返回。
            message:
              type: string
              description: 错误详情。仅在任务失败时返回。
        usage:
          type: object
          description: 输出统计信息。仅在任务成功时返回。
          properties:
            video_duration:
              type: number
              description: 本次请求生成视频时长计量，单位：秒。
              example: 10.23
            video_ratio:
              type: string
              description: 本次请求生成视频的画幅类型，该值为standard。
              example: standard
    DashScopeErrorResponse:
      type: object
      description: DashScope API 错误响应。
      properties:
        request_id:
          type: string
          description: 本次请求的系统唯一码。
        code:
          type: string
          description: 错误码（如 InvalidApiKey、InvalidParameter、Throttling）。
          example: InvalidApiKey
        message:
          type: string
          description: 人类可读的错误描述。
          example: No API-key provided.
````

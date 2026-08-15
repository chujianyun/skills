> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# AnimateAnyone 动作模板生成 — 查询结果

> 根据任务 ID 查询 AnimateAnyone 动作模板生成任务的状态和结果

<Note>
  请先[获取 API Key](/api-reference/preparation/api-key) 并[设置为环境变量](/api-reference/preparation/export-api-key-env)。
</Note>

<Note>
  异步任务查询接口提供 20 QPS 的访问流量限制。
</Note>

## 状态说明

| 状态          | 说明         |
| ----------- | ---------- |
| `PENDING`   | 排队中        |
| `RUNNING`   | 处理中        |
| `SUCCEEDED` | 成功         |
| `FAILED`    | 失败         |
| `CANCELED`  | 已取消        |
| `UNKNOWN`   | 任务不存在或状态未知 |

## 状态码

通用状态码请参阅[错误信息](/api-reference/preparation/error-messages)。

## OpenAPI

````yaml get /tasks/{task_id}
openapi: 3.0.3
info:
  title: AnimateAnyone 动作模板生成 API
  description: AnimateAnyone动作模板生成模型，可基于人物运动视频提取人物动作，并生成可供AnimateAnyone视频生成模型使用的人物动作模板。本文档介绍了该模型提供的动作模板生成能力的API调用方法。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 千问AI平台
security:
  - BearerAuth: []
paths:
  /tasks/{task_id}:
    get:
      operationId: getAnimateAnyoneTemplateGenTaskStatus
      summary: 根据任务ID查询结果
      description: 查询动作模板生成任务的状态及结果。异步任务查询接口提供 20 QPS 的访问流量限制。若有更高频次的查询需求，可通过EventBridge配置事件转发。
      parameters:
        - name: task_id
          in: path
          required: true
          description: 需要查询任务的task_id。
          schema:
            type: string
      responses:
        "200":
          description: 成功获取任务状态
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/TaskStatusResponse"
              examples:
                SUCCEEDED:
                  summary: 任务成功
                  value:
                    request_id: 7574ee8f-38a3-4b1e-9280-11c33ab46e51
                    output:
                      task_id: a8532587-fa8c-4ef8-82be-0c46b17950d1
                      task_status: SUCCEEDED
                      template_id: AACT.xxx.xxx-xxx.xxx
                    usage:
                      video_duration: 10.23
                      video_ratio: standard
                FAILED:
                  summary: 任务失败
                  value:
                    request_id: 7574ee8f-38a3-4b1e-9280-11c33ab46e51
                    output:
                      task_id: a8532587-fa8c-4ef8-82be-0c46b17950d1
                      task_status: FAILED
                      code: xxx
                      message: xxxxxx
                RUNNING:
                  summary: 任务处理中
                  value:
                    request_id: 7574ee8f-38a3-4b1e-9280-11c33ab46e51
                    output:
                      task_id: a8532587-fa8c-4ef8-82be-0c46b17950d1
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
            curl -X GET \
              --header 'Authorization: Bearer $DASHSCOPE_API_KEY' \
              https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    TemplateGenRequest:
      type: object
      required:
        - model
      properties:
        model:
          type: string
          description: 指明需要调用的模型，此处用 animate-anyone-template-gen2。
          enum:
            - animate-anyone-template-gen2
          example: animate-anyone-template-gen2
        input:
          type: object
          description: 输入数据，包含用于动作模板提取的参考视频。
          properties:
            video_url:
              type: string
              description: |-
                用户上传的视频 URL，用于生成基于指定视频的动作模板。

                **视频约束：**
                - 格式：支持 MP4、AVI、MOV。
                - 时长：不小于 2s 且不大于 60s。
                - 边长：不低于 200，不大于 2048；长宽比介于 1:3 到 3:1。
                - 帧率：≥ 24fps，视频编码采用 H.264 或 H.265。
                - 文件大小：不大于 200MB。
                - 内容：人物应全身入镜、身体无遮挡、保持人脸清晰。人物应从画面首帧开始出现，动作连贯，一镜到底。

                上传文件支持HTTP或HTTPS链接方式，不支持本地链接方式。也可使用平台提供的文件存储API上传本地文件并创建链接。
              example: https://example.com/video.mp4
    AsyncTaskSubmitResponse:
      type: object
      description: 异步任务提交的响应结果。
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
              description: 提交异步任务的任务 ID，实际任务结果需要通过异步任务查询接口获取。
              example: a8532587-fa8c-4ef8-82be-0c46b17950d1
            task_status:
              type: string
              description: 提交异步任务后的任务状态。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - CANCELED
                - UNKNOWN
              example: PENDING
    TaskStatusResponse:
      type: object
      description: 查询任务状态及结果的响应。
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
                - RUNNING
                - SUCCEEDED
                - FAILED
                - CANCELED
                - UNKNOWN
              example: SUCCEEDED
            template_id:
              type: string
              description: 平台输出的动作模板ID，可作为"Animate-Anyone 视频生成接口"的入参。动作模板ID会进行权限校验，请确保使用template_id的云账号与当前生产该动作模板的云账号一致。
              example: AACT.xxx.xxx-xxx.xxx
            code:
              type: string
              description: 错误码，任务失败时返回。
            message:
              type: string
              description: 错误详情，任务失败时返回。
        usage:
          type: object
          description: 本次请求的用量统计，仅任务成功时返回。
          properties:
            video_duration:
              type: number
              format: float
              description: 本次请求生成模板时长计量，单位：秒。
              example: 10.23
            video_ratio:
              type: string
              description: 本次请求生成视频模板的画幅类型，该值为 standard。
              enum:
                - standard
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
          description: 错误详情描述。
          example: No API-key provided.
````

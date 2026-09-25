> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# AnimateAnyone 动作模板生成 — 创建任务

> 提交 AnimateAnyone 动作模板生成任务

<Note>
  请先[获取 API Key](/api-reference/preparation/api-key) 并[设置为环境变量](/api-reference/preparation/export-api-key-env)。
</Note>

## 模型信息

| 模型名                            | 模型简介                            |
| ------------------------------ | ------------------------------- |
| `animate-anyone-template-gen2` | 人物动作模板生成模型，可基于人物运动视频提取人物动作并制作模板 |

## 输入视频要求

上传的视频中人物应全身入镜、身体无遮挡、保持人脸清晰。人物应从画面首帧开始出现，动作连贯，一镜到底（有场景切换的视频建议拆分成多段）。建议画面首帧人物正面朝向镜头；避免人物运动中出现大幅弯腰、下蹲、身体蜷缩等动作。

<Warning>
  为保障模板制作效果，应避免上传视频中的任一帧画面出现以下情况：身体蜷缩或遮挡、画面有多人、人物模糊、人物过小（人脸不清晰）、人物过大（人物不完整）。当视频首帧画面出现上述错误情形时，当次提交的任务可能报错并中止。
</Warning>

<Warning>
  请确保上传的视频文件来源符合相关法律法规。生成的动作模板的音频与上传的视频文件中的音频一致。若不希望使用该音频，或尚未取得该音频（如音乐等）的使用许可，请在上传视频文件前消除其中的音频信息。
</Warning>

## 输入限制

- 视频格式：支持 MP4、AVI、MOV。
- 视频文件不大于 200 MB。
- 视频边长不低于 200，不大于 2048 像素；长宽比介于 1:3 到 3:1。
- 视频帧率 ≥ 24 fps，视频编码采用 H.264 或 H.265。
- 视频时长不小于 2s 且不大于 60s。
- 上传的视频文件支持 HTTP/HTTPS 链接，不支持本地路径。也可使用[文件上传 API](/api-reference/platform-api/file/upload-file) 上传本地文件并创建链接。

## OpenAPI

````yaml post /services/aigc/image2video/aa-template-generation/
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
  /services/aigc/image2video/aa-template-generation/:
    post:
      operationId: createAnimateAnyoneTemplateGenTask
      summary: 创建动作模板生成任务
      description: 用于生成人物动作模板，该模板可作为AnimateAnyone视频生成API的输入物，以生成人物动作视频。因该算法调用耗时较长，采用异步调用的方式提交任务。任务提交之后，系统会返回对应的任务ID，后续可通过根据任务ID查询结果接口获取任务状态及对应结果。
      parameters:
        - name: X-DashScope-Async
          in: header
          required: true
          description: 使用 enable，表明使用异步方式提交任务。
          schema:
            type: string
            enum:
              - enable
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/TemplateGenRequest"
      responses:
        "200":
          description: 任务提交成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/AsyncTaskSubmitResponse"
        "400":
          description: 请求参数无效
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
      x-codeSamples:
        - lang: curl
          label: cURL - 创建动作模板
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/aa-template-generation/' \
              --header 'X-DashScope-Async: enable' \
              --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
              --header 'Content-Type: application/json' \
              --data '{
                "model": "animate-anyone-template-gen2",
                "input": {
                    "video_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241210/cwjmsz/1.mp4"
                }
              }'
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

> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 声动人像 VideoRetalk — 创建任务

> 提交声动人像 VideoRetalk 视频口型替换异步任务

<Note>
  请先[获取 API Key](/api-reference/preparation/api-key) 并[配置为环境变量](/api-reference/preparation/export-api-key-env)。
</Note>

## 模型概览

**模型简介**

| 模型名         | 模型简介                                                                  |
| ----------- | --------------------------------------------------------------------- |
| videoretalk | 声动人像 VideoRetalk，基于人物视频和人声音频，生成人物讲话口型与输入音频相匹配的新视频。适用于视频配音、数字人口型替换等场景。 |

## 使用说明

- 上传的视频、音频、图像文件支持 HTTP 链接，不支持本地路径。也可使用平台提供的[临时存储空间](/api-reference/more/upload-file-get-temporary-url)上传本地文件并创建链接。
- 如果使用临时存储空间上传文件后获取到的 `oss://` 前缀 URL，在 HTTP 请求头中必须添加 `X-DashScope-OssResourceResolve: enable` 参数。未添加该参数会导致报错 `No connection adapters were found for 'oss://...'`。详细说明请参见[上传文件获取临时 URL](/api-reference/more/upload-file-get-temporary-url)。

## 输入限制

**视频要求**

| 限制项  | 要求                       |
| ---- | ------------------------ |
| 格式   | mp4、avi、mov              |
| 文件大小 | 不超过 300 MB               |
| 时长   | 2 秒到 120 秒之间             |
| 帧率   | 15 fps 到 60 fps          |
| 编码   | H.264 或 H.265            |
| 边长   | 640 到 2048 像素            |
| 内容   | 人物正面出镜的近景画面，避免大角度侧脸或人脸过小 |

**音频要求**

| 限制项  | 要求                         |
| ---- | -------------------------- |
| 格式   | wav、mp3、aac                |
| 文件大小 | 不超过 30 MB                  |
| 时长   | 2 秒到 120 秒之间               |
| 内容   | 需包含清晰、响亮的人声语音，已去除环境噪音和背景音乐 |

**人物参考图要求**（可选，用于多人场景指定目标人物）

| 限制项  | 要求                      |
| ---- | ----------------------- |
| 格式   | jpeg、jpg、png、bmp、webp   |
| 文件大小 | 不超过 10 MB               |
| 宽高比  | 不超过 2                   |
| 最大边长 | 不超过 4096 像素             |
| 内容   | 需包含一张清晰的人物正脸，且为视频中出现的人物 |

## 使用流程

1. 调用本接口，将视频 URL、音频 URL 及可选参数一并提交，获取 `task_id`。
2. 调用[查询视频口型替换任务结果](/api-reference/video-generation/video-retalk/query-result)接口，使用 `task_id` 轮询任务状态，直到获取生成的视频 URL。

## 错误码

大模型服务通用状态码请查阅[错误信息](/api-reference/preparation/error-messages)。本模型特定错误码：

| HTTP 状态码 | 错误码                          | 含义说明                           |
| -------- | ---------------------------- | ------------------------------ |
| 400      | InvalidParameter             | 缺少必填参数或格式错误                    |
| 400      | InvalidURL.ConnectionRefused | 下载被拒绝，请提供可用的 URL               |
| 400      | InvalidURL.Timeout           | 下载超时（60 秒超时）                   |
| 400      | InvalidFile.Size             | 视频/音频/图像文件大小超限                 |
| 400      | InvalidFile.Format           | 文件格式不符合要求                      |
| 400      | InvalidFile.Resolution       | 视频边长需介于 640–2048 之间            |
| 400      | InvalidFile.FPS              | 视频帧率需介于 15–60 fps              |
| 400      | InvalidFile.Duration         | 视频/音频时长需介于 2–120 秒             |
| 400      | InvalidFile.ImageSize        | 图片大小超出限制（长宽比不大于 2，最长边不大于 4096） |
| 400      | InvalidFile.Openerror        | 视频/音频/图像文件无法打开                 |
| 400      | InvalidFile.Content          | 输入图片中没有人或有多人                   |
| 400      | InvalidFile.FaceNotMatch     | 参考图与视频人脸匹配失败                   |

## OpenAPI

````yaml post /api/v1/services/aigc/image2video/video-synthesis
openapi: 3.1.0
info:
  title: 声动人像 VideoRetalk 视频口型替换 API
  version: 1.0.0
  description: 基于人物视频和人声音频，生成人物讲话口型与输入音频相匹配的新视频。
servers:
  - url: https://dashscope.aliyuncs.com
    description: 千问AI平台
security:
  - BearerAuth: []
paths:
  /api/v1/services/aigc/image2video/video-synthesis:
    post:
      summary: 提交视频口型替换任务
      description: 提交声动人像 VideoRetalk 视频口型替换异步任务。任务提交后返回 `task_id`，通过查询接口获取结果。
      operationId: createVideoRetalkTask
      parameters:
        - name: X-DashScope-Async
          in: header
          required: true
          schema:
            type: string
            enum:
              - enable
          description: 固定值 `enable`，启用异步模式。
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/VideoRetalkRequest"
      responses:
        "200":
          description: 任务提交成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/VideoRetalkSubmitResponse"
              example:
                output:
                  task_id: a8532587-fa8c-4ef8-82be-0c46b17950d1
                  task_status: PENDING
                request_id: 7574ee8f-38a3-4b1e-9280-11c33ab46e51
        "400":
          description: 请求参数错误
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
              example:
                code: InvalidParameter
                message: The request parameter is invalid.
                request_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        "401":
          description: 认证失败
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
              example:
                code: InvalidApiKey
                message: No API-key provided.
                request_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        "429":
          description: 请求频率超限
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
              example:
                code: Throttling
                message: Requests throttling triggered.
                request_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
      x-codeSamples:
        - lang: curl
          label: cURL
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis' \
              --header 'X-DashScope-Async: enable' \
              --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
              --header 'Content-Type: application/json' \
              --data '{
                "model": "videoretalk",
                "input": {
                  "video_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250717/pvegot/input_video_01.mp4",
                  "audio_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250717/aumwir/stella2-%E6%9C%89%E5%A3%B0%E4%B9%A67.wav",
                  "ref_image_url": ""
                },
                "parameters": {
                  "video_extension": false
                }
              }'
components:
  schemas:
    VideoRetalkRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          enum:
            - videoretalk
          description: 模型名称，固定为 `videoretalk`。
        input:
          type: object
          required:
            - video_url
            - audio_url
          properties:
            video_url:
              type: string
              description: |-
                人物视频公网 URL。

                **视频要求**：
                - **格式**：mp4、avi、mov
                - **文件大小**：不超过 300 MB
                - **时长**：2 秒到 120 秒之间
                - **帧率**：15 fps 到 60 fps
                - **编码**：H.264 或 H.265
                - **边长**：640 到 2048 像素
                - **内容**：人物正面出镜的近景画面，避免大角度侧脸或人脸过小
                - **URL**：HTTP/HTTPS 公网可访问地址
            audio_url:
              type: string
              description: |-
                驱动口型的语音音频公网 URL。

                **音频要求**：
                - **格式**：wav、mp3、aac
                - **文件大小**：不超过 30 MB
                - **时长**：2 秒到 120 秒之间
                - **内容**：需包含清晰、响亮的人声语音，已去除环境噪音和背景音乐
                - **URL**：HTTP/HTTPS 公网可访问地址
            ref_image_url:
              type: string
              description: |-
                人脸参考图公网 URL（可选）。当输入视频中存在多张人脸时，通过该参数指定用于口型匹配的人脸。若不输入，默认选择视频中第一个有人脸画面中占比最大的人物。

                **图像要求**：
                - **格式**：jpeg、jpg、png、bmp、webp
                - **文件大小**：不超过 10 MB
                - **宽高比**：不超过 2
                - **最大边长**：不超过 4096 像素
                - **内容**：需包含一张清晰的人物正脸，且为视频中出现的人物
                - **URL**：HTTP/HTTPS 公网可访问地址
        parameters:
          type: object
          properties:
            video_extension:
              type: boolean
              default: false
              description: 当输入的音频时长大于视频时长时，是否扩展视频长度。`true`：使用原视频画面「倒放-正放」交替模式扩展视频时长，直至与音频相同；`false`：不扩展，音频将被截断。默认为 `false`。
            query_face_threshold:
              type: integer
              minimum: 120
              maximum: 200
              default: 170
              description: 当输入人脸参考图时，调整人脸匹配的置信度。取值范围 120–200，值越小匹配越宽松，值越大匹配越严格。默认为 `170`。`input.ref_image_url` 为空时该参数不生效。
    VideoRetalkSubmitResponse:
      type: object
      properties:
        request_id:
          type: string
          description: 本次请求的唯一 ID。
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 异步任务 ID，用于查询任务状态。
            task_status:
              type: string
              enum:
                - PENDING
              description: 任务初始状态，值为 `PENDING`。
    VideoRetalkQueryResponse:
      type: object
      properties:
        request_id:
          type: string
          description: 本次请求的唯一 ID。
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 异步任务 ID。
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
              description: 任务状态。`PENDING`：排队中；`PRE-PROCESSING`：前置处理中；`RUNNING`：处理中；`POST-PROCESSING`：后置处理中；`SUCCEEDED`：成功；`FAILED`：失败；`UNKNOWN`：任务不存在或已过期。
            submit_time:
              type: string
              description: 任务提交时间。
            scheduled_time:
              type: string
              description: 任务开始调度时间。
            end_time:
              type: string
              description: 任务结束时间（成功或失败时返回）。
            video_url:
              type: string
              description: 生成视频的 URL，有效期 24 小时，请及时下载保存。
            code:
              type: string
              description: 任务失败时的错误码。
            message:
              type: string
              description: 任务失败时的错误信息。
        usage:
          type: object
          description: 任务成功时返回的用量信息。
          properties:
            video_duration:
              type: number
              description: 生成视频的时长，单位为秒。
            size:
              type: string
              description: 生成视频的分辨率，与输入视频一致。
            video_ratio:
              type: string
              description: 生成视频的画幅类型，值为 `standard`，默认按原视频比例输出。
            fps:
              type: integer
              description: 生成视频的帧率，与输入视频一致。
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

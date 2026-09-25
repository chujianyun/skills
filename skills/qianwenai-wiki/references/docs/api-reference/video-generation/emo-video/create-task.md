> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 悦动人像 EMO — 创建任务

> 提交悦动人像 EMO 唱演视频生成异步任务

<Note>
  请先[获取 API Key](/api-reference/preparation/api-key) 并[配置为环境变量](/api-reference/preparation/export-api-key-env)。
</Note>

## 模型概览

**模型简介**

| 模型名    | 模型简介                                                        |
| ------ | ----------------------------------------------------------- |
| emo-v1 | 悦动人像 EMO，基于人物肖像图片和音频，生成口型与音频同步的唱演视频。适用于数字人播报、音乐 MV、虚拟主播等场景。 |

## 前置条件

在调用本接口前，需先调用 [EMO 图像检测](/api-reference/video-generation/emo-video/emo-detect) 接口对人物图片进行检测，获取 `face_bbox`（人脸边界框）和 `ext_bbox`（扩展边界框），再将其传入本接口。

## 使用流程

1. 调用 [EMO 图像检测](/api-reference/video-generation/emo-video/emo-detect) 接口，传入人物图片，获取 `face_bbox` 和 `ext_bbox`。
2. 调用本接口，将图片 URL、音频 URL 及上一步获取的 bbox 信息一并提交，获取 `task_id`。
3. 调用[查询视频生成结果](/api-reference/video-generation/emo-video/query-result)接口，使用 `task_id` 轮询任务状态，直到获取生成的视频 URL。

## 错误码

大模型服务通用状态码请查阅[错误信息](/api-reference/preparation/error-messages)。

## OpenAPI

````yaml post /services/aigc/image2video/video-synthesis
openapi: 3.1.0
info:
  title: 悦动人像 EMO 视频生成 API
  version: 1.0.0
  description: 基于人物肖像图片和音频，生成口型与音频同步的唱演视频。
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
security:
  - BearerAuth: []
paths:
  /services/aigc/image2video/video-synthesis:
    post:
      summary: 提交视频生成任务
      operationId: createEmoVideoTask
      description: 提交悦动人像 EMO 视频生成异步任务。需要先调用 [EMO 图像检测](/api-reference/video-generation/emo-detect) 接口获取 `face_bbox` 和 `ext_bbox`。
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
              $ref: "#/components/schemas/EmoVideoRequest"
      responses:
        "200":
          description: 任务提交成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/EmoVideoSubmitResponse"
              example:
                output:
                  task_id: a8532587-fa8c-4ef8-82be-xxxxxx
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
                "model": "emo-v1",
                "input": {
                  "image_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251225/onmomb/emo.png",
                  "audio_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250825/aejgyj/input_audio.mp3",
                  "face_bbox": [302, 286, 610, 593],
                  "ext_bbox": [71, 9, 840, 778]
                },
                "parameters": {
                  "style_level": "normal"
                }
              }'
components:
  schemas:
    EmoVideoRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          enum:
            - emo-v1
          description: 模型名称，固定为 `emo-v1`。
        input:
          type: object
          required:
            - image_url
            - audio_url
            - face_bbox
            - ext_bbox
          properties:
            image_url:
              type: string
              description: 人物肖像图片公网 URL。模型将根据 EMO 图像检测 API 返回的 `ext_bbox` 参数对原始图片进行裁剪，裁剪后区域的宽高比决定输出视频的画幅比例与分辨率。支持 jpg、png、jpeg、bmp 格式；图像最小边长 >= 400 像素，最大边长 <= 7000 像素。仅支持 HTTP/HTTPS 链接。
            audio_url:
              type: string
              description: 驱动视频的音频公网 URL。支持 wav、mp3 格式；文件大小不超过 15MB；音频时长不超过 60 秒。仅支持 HTTP/HTTPS 链接。
            face_bbox:
              type: array
              items:
                type: integer
              minItems: 4
              maxItems: 4
              description: 人脸边界框，格式为 `[x1, y1, x2, y2]`，代表人脸区域的左上角和右下角坐标。可通过 [EMO 图像检测](/api-reference/video-generation/emo-detect) 接口获取。
            ext_bbox:
              type: array
              items:
                type: integer
              minItems: 4
              maxItems: 4
              description: 图片中动态区域 bbox 的像素坐标，应输入 EMO 图像检测 API 出参中同名字段的值。该区域的宽高比为 1:1 或 3:4。坐标格式 `[x1, y1, x2, y2]`，分别对应左上角和右下角两个点的坐标。可通过 [EMO 图像检测](/api-reference/video-generation/emo-detect) 接口获取。
        parameters:
          type: object
          properties:
            style_level:
              type: string
              enum:
                - normal
                - calm
                - active
              default: normal
              description: 生成视频的动态程度。`normal`：正常动态幅度；`calm`：较平静，动态幅度更小；`active`：较活跃，动态幅度更大。默认为 `normal`。
    EmoVideoSubmitResponse:
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
    EmoVideoQueryResponse:
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
                - RUNNING
                - SUCCEEDED
                - FAILED
                - UNKNOWN
              description: 任务状态。`PENDING`：排队等待；`RUNNING`：处理中；`SUCCEEDED`：成功；`FAILED`：失败；`UNKNOWN`：任务不存在或已过期。
            submit_time:
              type: string
              description: 任务提交时间。
            scheduled_time:
              type: string
              description: 任务开始调度时间。
            end_time:
              type: string
              description: 任务结束时间（成功或失败时返回）。
            results:
              type: object
              description: 任务成功时返回。
              properties:
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
            video_ratio:
              type: string
              description: 生成视频的宽高比，例如 `1:1`、`3:4`。
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

> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 万相数字人 — 创建任务

> 基于单张图片和音频，异步生成数字人视频

<Note>
  请先[获取 API Key](/api-reference/preparation/api-key) 并[配置为环境变量](/api-reference/preparation/export-api-key-env)。
</Note>

wan2.2-s2v 模型能基于单张图片和音频，生成动作自然的说话、唱歌或表演视频。

## OpenAPI

````yaml post /services/aigc/image2video/video-synthesis
openapi: 3.1.0
info:
  title: 万相数字人视频生成 API
  description: 数字人 wan2.2-s2v 模型能基于单张图片和音频，生成动作自然的说话、唱歌或表演视频。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 千问AI平台
security:
  - BearerAuth: []
paths:
  /services/aigc/image2video/video-synthesis:
    post:
      operationId: createWanS2vTask
      summary: 创建数字人视频任务
      description: 基于单张图片和音频，异步生成数字人视频。支持说话、唱歌、表演三种口型场景。
      parameters:
        - name: X-DashScope-Async
          in: header
          required: true
          schema:
            type: string
            enum:
              - enable
          description: 固定值为 enable，表示使用异步调用方式。
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/WanS2vRequest"
            examples:
              basic:
                summary: 基础示例
                value:
                  model: wan2.2-s2v
                  input:
                    image_url: https://img.alicdn.com/imgextra/i3/O1CN011FObkp1T7Ttowoq4F_!!6000000002335-0-tps-1440-1797.jpg
                    audio_url: https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250825/iaqpio/input_audio.MP3
                  parameters:
                    resolution: 480P
      responses:
        "200":
          description: 任务创建成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/WanS2vCreateResponse"
              examples:
                success:
                  summary: 创建成功
                  value:
                    output:
                      task_id: a8532587-fa8c-4ef8-82be-xxxxxx
                      task_status: PENDING
                    request_id: 7574ee8f-38a3-4b1e-9280-xxxxxx
      x-codeSamples:
        - lang: curl
          label: cURL
          source: |-
            curl 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis/' \
             --header 'X-DashScope-Async: enable' \
             --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
             --header 'Content-Type: application/json' \
             --data '{
                 "model": "wan2.2-s2v",
                 "input": {
                        "image_url": "https://img.alicdn.com/imgextra/i3/O1CN011FObkp1T7Ttowoq4F_!!6000000002335-0-tps-1440-1797.jpg",
                        "audio_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250825/iaqpio/input_audio.MP3"
                    },
                    "parameters": {
                        "resolution": "480P"
                    }
                }'
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    WanS2vRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 指明需要调用的模型。
          enum:
            - wan2.2-s2v
          example: wan2.2-s2v
        input:
          type: object
          required:
            - image_url
            - audio_url
          properties:
            image_url:
              type: string
              description: |-
                上传的图片 URL。

                - 图像格式：支持 jpg、jpeg、png、bmp、webp。
                - 图像分辨率：图像的宽度和高度范围为 [400, 7000] 像素。
                - 仅支持公网可访问的 HTTP/HTTPS 链接。本地文件可通过[上传文件获取临时URL](/api-reference/platform-api/file/upload-file)。
              example: http://aaa/bbb.jpg
            audio_url:
              type: string
              description: |-
                上传的音频文件 URL。

                - 音频格式：支持 wav、mp3。
                - 音频限制：文件 < 15M，时长 < 20s。
                - 音频内容：需包含清晰、响亮的人声语音，并去除环境噪音、背景音乐等干扰。
                - 仅支持公网可访问的 HTTP/HTTPS 链接。本地文件可通过[上传文件获取临时URL](/api-reference/platform-api/file/upload-file)。
              example: http://aaa/bbb.mp3
        parameters:
          type: object
          properties:
            resolution:
              type: string
              description: |-
                视频分辨率档位。可选值为 480P、720P，默认值为 480P。

                模型会尽量保持输出视频与输入图像的宽高比一致，在宽高比不变的基础上，将视频总像素调整到所选档位附近。

                - 480P：视频分辨率通常指 640×480（约 31 万像素），视频宽高比为 4:3。
                - 720P：视频分辨率通常指 1280×720（约 92 万像素），视频宽高比为 16:9。
              enum:
                - 480P
                - 720P
              default: 480P
              example: 480P
    WanS2vCreateResponse:
      type: object
      properties:
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 异步任务的唯一ID。
              example: a8532587-fa8c-4ef8-82be-0c46b17950d1
            task_status:
              type: string
              description: 提交异步任务后的作业状态。
              example: PENDING
        request_id:
          type: string
          description: 本次请求的唯一ID。
          example: 7574ee8f-38a3-4b1e-9280-11c33ab46e51
    WanS2vQueryResponse:
      type: object
      properties:
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 查询的任务ID。
              example: a8532587-fa8c-4ef8-82be-0c46b17950d1
            task_status:
              type: string
              description: 任务状态。可能的值包括：PENDING（排队中）、RUNNING（处理中）、SUCCEEDED（成功）、FAILED（失败）、UNKNOWN（任务不存在或状态未知）、CANCELED（任务取消成功）。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - UNKNOWN
                - CANCELED
              example: SUCCEEDED
            submit_time:
              type: string
              description: 任务提交时间。
              example: 2025-09-01 09:37:27.468
            scheduled_time:
              type: string
              description: 任务执行时间。
              example: 2025-09-01 09:37:34.885
            end_time:
              type: string
              description: 任务完成时间。
              example: 2025-09-01 09:40:20.734
            results:
              type: object
              properties:
                video_url:
                  type: string
                  description: 生成的视频文件 URL。**video_url 有效期为 24 小时**，请及时下载。
                  example: https://xxx/1.mp4?Expires=xxx
            code:
              type: string
              description: 错误码。任务失败时返回此参数。
              example: InvalidParameter
            message:
              type: string
              description: 错误详情。任务失败时返回此参数。
              example: The request is missing required parameters or in a wrong format
        usage:
          type: object
          properties:
            duration:
              type: number
              format: float
              description: 视频时长（秒），用于计费，按秒计费。
              example: 10.23
            video_count:
              type: integer
              description: 生成视频的数量。
              example: 1
            SR:
              type: integer
              description: 生成视频分辨率档位。
              example: 480
            size:
              type: string
              description: 本次请求生成视频的分辨率。
              example: 640*480
            fps:
              type: integer
              description: 本次请求生成视频的帧率。
              example: 16
        request_id:
          type: string
          description: 本次请求的唯一ID。
          example: 7574ee8f-38a3-4b1e-9280-11c33ab46e51
````

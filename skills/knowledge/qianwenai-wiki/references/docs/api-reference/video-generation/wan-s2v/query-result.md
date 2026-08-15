> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 万相数字人 — 查询结果

> 查询 wan2.2-s2v 数字人视频生成任务状态和结果

查询任务状态和结果。

## 轮询策略

使用返回的 `task_id` 轮询此接口，建议每 **15 秒**轮询一次（视频生成耗时约 5-10 分钟）。

## 注意事项

- **URL 有效期**：视频 URL 在 **24 小时**后过期，请及时下载。
- **视频时长**：生成视频的时长与输入音频的时长一致，因此单次生成的视频时长同样受音频时长限制（须小于 20 秒）；若输入音频超过 20 秒，会导致任务报错。如需生成更长的视频，可将长音频按小于 20 秒切分为多段，分别调用创建任务接口生成对应的视频片段，再使用剪辑工具将多段视频拼接合并为一个完整的长视频。
- **任务状态流转**：`PENDING` → `RUNNING` → `SUCCEEDED` 或 `FAILED`。
- **其他状态**：`CANCELED`（任务已取消）、`UNKNOWN`（任务 ID 无效或已过期）。
- **`task_id` 有效期**：`task_id` 有效期为 24 小时，过期后无法查询状态和结果。
- **避免重复提交**：请通过轮询获取结果，不要重复提交请求。

## OpenAPI

````yaml get /tasks/{task_id}
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
  /tasks/{task_id}:
    get:
      operationId: getWanS2vTaskResult
      summary: 查询数字人视频任务结果
      description: 根据任务ID查询数字人视频生成任务的状态和结果。视频生成任务耗时约 5-10 分钟，建议每 15 秒轮询一次。
      parameters:
        - name: task_id
          in: path
          required: true
          schema:
            type: string
          description: 需要查询任务的ID。
          example: a8532587-fa8c-4ef8-82be-0c46b17950d1
      responses:
        "200":
          description: 查询成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/WanS2vQueryResponse"
              examples:
                SUCCEEDED:
                  summary: 成功响应
                  value:
                    output:
                      task_id: bcae8761-f242-4775-a11e-xxxxxx
                      task_status: SUCCEEDED
                      submit_time: 2025-09-01 09:37:27.468
                      scheduled_time: 2025-09-01 09:37:34.885
                      end_time: 2025-09-01 09:40:20.734
                      results:
                        video_url: http://dashscope-result-hz.oss-cn-hangzhou.aliyuncs.com/1d/xxx.mp4?Expires=xxxxxx
                    usage:
                      duration: 18.13
                      size: 512*640
                      fps: 16
                      video_count: 1
                      SR: 480
                    request_id: 28cfedb1-cd60-9e0c-b920-xxxxxx
                FAILED:
                  summary: 失败响应
                  value:
                    request_id: 8d49f522-f6a4-9eed-b322-xxxxxx
                    output:
                      task_id: 101ad32f-7653-4ae9-8f22-xxxxxx
                      task_status: FAILED
                      submit_time: 2025-09-01 11:43:41.174
                      scheduled_time: 2025-09-01 11:43:48.937
                      end_time: 2025-09-01 11:43:49.802
                      code: InvalidURL
                      message: Required URL is missing or invalid, please check the request URL.
                RUNNING:
                  summary: 处理中响应
                  value:
                    output:
                      task_id: bcae8761-f242-4775-a11e-xxxxxx
                      task_status: RUNNING
                      submit_time: 2025-09-01 09:37:27.468
                      scheduled_time: 2025-09-01 09:37:34.885
                    request_id: 28cfedb1-cd60-9e0c-b920-xxxxxx
      x-codeSamples:
        - lang: curl
          label: cURL
          source: |-
            curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/86ecf553-d340-4e21-xxxxxxxxx \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY"
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

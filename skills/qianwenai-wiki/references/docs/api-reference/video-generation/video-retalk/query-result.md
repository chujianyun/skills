> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 声动人像 VideoRetalk — 查询视频口型替换任务结果

> 查询声动人像 VideoRetalk 视频口型替换任务状态，获取生成的视频

查询任务状态并获取生成的视频。

## 轮询策略

1. 调用[提交视频口型替换任务](/api-reference/video-generation/video-retalk/create-task)接口获取 `task_id`。
2. 每 **15 秒**轮询一次，直到 `task_status` 为 `SUCCEEDED` 或 `FAILED`。
3. 任务成功后，从 `output.video_url` 获取视频。

## 注意事项

- **URL 有效期**：视频 URL 在任务完成后 **24 小时**过期，请及时下载保存。
- **状态流转**：`PENDING` → `PRE-PROCESSING` → `RUNNING` → `POST-PROCESSING` → `SUCCEEDED` 或 `FAILED`。`UNKNOWN` 表示任务不存在或已过期。

## 常见问题

**输入语音和视频长度不一致，会如何处理？**

默认按音频、视频两者中时长较短的来截断。当输入的音频时长大于视频时长时，若希望按音频长度来生成，可将 `parameters.video_extension` 设为 `true`，算法将使用原视频画面"倒放-正放"交替模式扩展视频时长，直至与音频相同。

**输入音频中有静音情况，会如何处理？**

音频静音的时段，预期视频中人物也会闭嘴。

**输入视频中有无人脸/脸拍不全的情况，会如何处理？**

若音频中有人声，但画面无人或未出现人物嘴型，则保留原视频画面，音频正常播放。

**输入视频中有多人的情况，会如何处理？**

仅支持替换一个人物。算法会按照输入人脸参考图（`input.ref_image_url`）识别指定人脸。若未输入人脸参考图，则默认选择第一个有人脸画面中占比最大的人脸。

## OpenAPI

````yaml get /api/v1/tasks/{task_id}
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
  /api/v1/tasks/{task_id}:
    get:
      summary: 查询视频口型替换任务结果
      description: 查询声动人像 VideoRetalk 视频口型替换任务状态，任务成功后返回生成的视频 URL。
      operationId: queryVideoRetalkTask
      parameters:
        - name: task_id
          in: path
          required: true
          schema:
            type: string
          description: 提交任务时返回的 `task_id`。
      responses:
        "200":
          description: 查询成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/VideoRetalkQueryResponse"
              examples:
                SUCCEEDED:
                  summary: 任务成功
                  value:
                    request_id: 87b9dce5-7f36-4305-a347-xxxxxx
                    output:
                      task_id: 3afd65eb-9604-48ea-8a91-xxxxxx
                      task_status: SUCCEEDED
                      submit_time: 2025-09-11 20:15:29.887
                      scheduled_time: 2025-09-11 20:15:36.741
                      end_time: 2025-09-11 20:16:40.577
                      video_url: http://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxx.mp4?Expires=xxx
                    usage:
                      video_duration: 7.2
                      size: 1080*1920
                      video_ratio: standard
                      fps: 25
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
                      submit_time: 2025-09-11 20:15:29.887
                      scheduled_time: 2025-09-11 20:15:36.741
        "401":
          description: 认证失败
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
      x-codeSamples:
        - lang: curl
          label: cURL
          source: |-
            curl -X GET 'https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}' \
              --header "Authorization: Bearer $DASHSCOPE_API_KEY"
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

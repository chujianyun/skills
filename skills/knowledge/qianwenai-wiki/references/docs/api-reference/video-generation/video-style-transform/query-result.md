> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 视频风格重绘 — 查询结果

> 查询视频风格重绘任务状态

查询任务状态并获取生成的视频。

## 轮询策略

1. 通过[提交任务](/api-reference/video-generation/video-style-transform/create-task)接口提交任务，保存返回的 `task_id`。
2. 每 **15 秒**轮询一次，直到 `task_status` 变为 `SUCCEEDED` 或 `FAILED`。
3. 任务成功后，从 `output_video_url` 下载视频。

## 注意事项

- **URL 有效期**：`output_video_url` 在 **24 小时**后过期，请及时下载。
- **状态流转**：`PENDING` → `RUNNING` → `SUCCEEDED` 或 `FAILED`。`SUSPENDED` 表示任务已暂停。`UNKNOWN` 表示任务不存在或已过期（超过 24 小时）。

## OpenAPI

````yaml get /tasks/{task_id}
openapi: 3.1.0
info:
  title: Video Style Transform API
  description: 视频风格重绘 API。将真实视频转换为多种艺术风格（日式漫画、美式漫画、3D卡通等8种风格）。使用异步任务模式——提交任务后轮询获取结果。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 千问AI平台
security:
  - BearerAuth: []
paths:
  /tasks/{task_id}:
    get:
      operationId: getVideoStyleTransformTaskStatus
      summary: 查询视频风格重绘任务结果
      description: 查询视频风格重绘任务的状态和结果。
      parameters:
        - name: task_id
          in: path
          required: true
          description: POST 提交接口返回的任务 ID。
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
                    request_id: b67df059-ca6a-9d51-afcd-xxxxxxxxxxxx
                    output:
                      task_id: d76ec1e8-ea27-4038-8913-xxxxxxxxxxxx
                      task_status: SUCCEEDED
                      submit_time: 2024-05-16 13:50:01.247
                      scheduled_time: 2024-05-16 13:50:01.354
                      end_time: 2024-05-16 13:50:27.795
                      output_video_url: http://xxx/result.mp4
                    usage:
                      duration: 3
                      SR: 720
                RUNNING:
                  summary: 任务运行中
                  value:
                    request_id: e5d70b02-ebd3-98ce-9fe8-xxxxxxxxxxxx
                    output:
                      task_id: 13b1848b-5493-4c0e-8c71-xxxxxxxxxxxx
                      task_status: RUNNING
                      submit_time: 2025-09-08 15:53:13.143
                      scheduled_time: 2025-09-08 15:53:13.169
                FAILED:
                  summary: 任务失败
                  value:
                    request_id: dccfdf23-b38e-97a6-a07b-xxxxxxxxxxxx
                    output:
                      task_id: 4cbabbdf-2c1f-43f4-b983-xxxxxxxxxxxx
                      task_status: FAILED
                      submit_time: 2024-05-16 14:15:14.103
                      scheduled_time: 2024-05-16 14:15:14.154
                      end_time: 2024-05-16 14:15:14.694
                      code: InvalidParameter.FileDownload
                      message: download for input video error
                UNKNOWN:
                  summary: 任务不存在或已过期
                  value:
                    request_id: aabbccdd-1234-5678-abcd-xxxxxxxxxxxx
                    output:
                      task_id: not-exist-task-id-xxxxxxxxxxxx
                      task_status: UNKNOWN
        "400":
          description: 请求参数无效
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
      x-codeSamples:
        - lang: curl
          label: cURL - 查询任务结果
          source: |-
            # 将 {task_id} 替换为提交任务时返回的实际任务 ID
            curl -X GET 'https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY"
        - lang: python
          label: Python - 查询任务结果
          source: |-
            import requests
            import os

            DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
            task_id = "0c9c33e6-b2e7-41e5-8d3f-xxxxxxxxxxxx"

            task_response = requests.get(
              f"https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}",
              headers={
                "Authorization": f"Bearer {DASHSCOPE_API_KEY}"
              })
            print(task_response.json())
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    VideoStyleTransformRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称，固定为 `video-style-transform`。
          enum:
            - video-style-transform
          example: video-style-transform
        input:
          type: object
          required:
            - video_url
          description: 输入数据。
          properties:
            video_url:
              type: string
              format: uri
              description: |-
                输入视频的 URL 地址。支持 HTTP/HTTPS 协议。

                **视频要求**：
                - 格式：MP4、AVI、MKV、MOV、FLV、TS、MPG、MXF
                - 时长：不超过 30 秒
                - 大小：不超过 100 MB
                - 分辨率：短边和长边均在 256~4096 像素
                - 宽高比：不超过 1.8
                - 编码：H.264 或 H.265
              example: https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250704/viwndw/%E5%8E%9F%E8%A7%86%E9%A2%91.mp4
        parameters:
          $ref: "#/components/schemas/VideoStyleTransformParameters"
    VideoStyleTransformParameters:
      type: object
      description: 视频风格重绘参数。
      properties:
        style:
          type: integer
          description: |-
            目标艺术风格。可选值：
            - `0`：日式漫画
            - `1`：美式漫画
            - `2`：清新漫画
            - `3`：3D卡通
            - `4`：国风卡通（古装输入最佳）
            - `5`：纸艺风格
            - `6`：简易插画
            - `7`：国风水墨
          enum:
            - 0
            - 1
            - 2
            - 3
            - 4
            - 5
            - 6
            - 7
          default: 0
          example: 0
        video_fps:
          type: integer
          description: 输出视频帧率（FPS）。取值范围：15~25。帧率越高，画面越流畅但计费时长越长。
          minimum: 15
          maximum: 25
          default: 15
          example: 15
        animate_emotion:
          type: boolean
          description: 是否开启情绪表情迁移。开启后，输出视频中人物表情更丰富，但部分场景可能出现表情夸张。
          default: true
        min_len:
          type: integer
          description: |-
            输出视频短边分辨率。可选值：
            - `720`：720P 输出
            - `540`：540P 输出

            分辨率越高，画质越好，计费单价越高。
          enum:
            - 720
            - 540
          default: 720
          example: 720
        use_SR:
          type: boolean
          description: 是否开启超分辨率增强。开启后可提升输出画质，但会增加处理时间。
          default: false
    AsyncTaskSubmitResponse:
      type: object
      description: 异步任务提交响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识，用于追踪和排查问题。
          example: 7574ee8f-38a3-4b1e-9280-11c33ab46e51
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID，用于轮询任务状态。配合 `GET /tasks/{task_id}` 使用。
              example: xxxxxxxx
            task_status:
              type: string
              description: 初始任务状态，通常为 `PENDING`。
              enum:
                - PENDING
                - RUNNING
                - SUSPENDED
                - SUCCEEDED
                - FAILED
    TaskStatusResponse:
      type: object
      description: 异步任务状态查询响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识。
          example: b67df059-ca6a-9d51-afcd-xxxxxxxxxxxx
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID。
              example: d76ec1e8-ea27-4038-8913-xxxxxxxxxxxx
            task_status:
              type: string
              description: 当前任务状态。
              enum:
                - PENDING
                - RUNNING
                - SUSPENDED
                - SUCCEEDED
                - FAILED
                - UNKNOWN
            output_video_url:
              type: string
              format: uri
              description: 生成的视频 URL。仅当 `task_status` 为 `SUCCEEDED` 时返回。**24 小时后过期**，请及时下载。
            submit_time:
              type: string
              description: 任务提交时间。
              example: 2024-05-16 13:50:01.247
            scheduled_time:
              type: string
              description: 任务调度时间。
              example: 2024-05-16 13:50:01.354
            end_time:
              type: string
              description: 任务结束时间。仅当任务完成（成功或失败）时返回。
              example: 2024-05-16 13:50:27.795
            code:
              type: string
              description: 错误码。仅当 `task_status` 为 `FAILED` 时返回。
            message:
              type: string
              description: 错误信息。仅当 `task_status` 为 `FAILED` 时返回。
        usage:
          type: object
          description: 用量统计。仅当任务成功时返回。
          properties:
            duration:
              type: integer
              description: 输出视频时长（秒）。
            SR:
              type: integer
              description: 输出视频短边分辨率。
    DashScopeErrorResponse:
      type: object
      description: DashScope API 错误响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识。
        code:
          type: string
          description: 错误码（如 `InvalidApiKey`、`Throttling`）。
          example: InvalidApiKey
        message:
          type: string
          description: 错误描述信息。
          example: Invalid API-key provided.
````

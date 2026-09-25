> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 爱诗 PixVerse — 查询图生视频任务结果

> 查询 PixVerse 图生视频任务状态

查询任务状态并获取生成的视频。

## 轮询策略

1. 通过[创建任务](/api-reference/video-generation/pixverse-image-to-video/create-task)接口提交任务，保存返回的 `task_id`。
2. 每 **15 秒**轮询一次，直到 `task_status` 变为 `SUCCEEDED` 或 `FAILED`。
3. 任务成功后，从 `video_url` 下载视频。

## 注意事项

- **URL 有效期**：`video_url` 在 **24 小时**后过期，请及时下载。
- **状态流转**：`PENDING` → `RUNNING` → `SUCCEEDED` 或 `FAILED`。`CANCELED` 表示任务已取消。`UNKNOWN` 表示任务不存在或已过期（超过 24 小时）。

## OpenAPI

````yaml get /tasks/{task_id}
openapi: 3.1.0
info:
  title: 爱诗 PixVerse 图生视频 API
  description: 爱诗 PixVerse 图生视频模型根据输入图像和文本提示词，生成一段流畅的视频。API 采用异步调用方式：先 POST 创建任务获取 task_id，再 GET 轮询查询任务状态与结果。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 千问AI平台
security:
  - BearerAuth: []
paths:
  /tasks/{task_id}:
    get:
      operationId: getPixVerseImageToVideoTaskStatus
      summary: 查询任务结果
      description: 根据 task_id 查询任务状态与结果。建议采用轮询机制，设置合理的查询间隔（如 15 秒）来获取结果。任务状态流转：PENDING（排队中）→ RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。
      parameters:
        - name: task_id
          in: path
          required: true
          description: 任务 ID，来自创建任务接口的返回。查询有效期 24 小时。
          schema:
            type: string
      responses:
        "200":
          description: 成功获取任务状态
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/PixVerseI2VTaskStatusResponse"
              examples:
                SUCCEEDED:
                  summary: 任务执行成功
                  value:
                    request_id: 7df19cf7-d76c-4bb8-b4c5-xxxxxx
                    output:
                      task_id: 5abf2c85-ea81-4cbf-8918-xxxxxx
                      task_status: SUCCEEDED
                      submit_time: 2026-03-20 11:48:50.499
                      scheduled_time: 2026-03-20 11:48:50.551
                      end_time: 2026-03-20 11:49:46.462
                      orig_prompt: 镜头从海龟下方缓缓上移，海龟悠然游动，腹部细节清晰可见。
                      video_url: https://media.pixverseai.cn/xxxx.mp4
                    usage:
                      duration: 5
                      shot_type: single
                      size: 992*944
                      fps: 24
                      video_count: 1
                      audio: false
                      SR: "720"
                FAILED:
                  summary: 任务执行失败
                  value:
                    request_id: e5d70b02-ebd3-98ce-9fe8-759d7d7b107d
                    output:
                      task_id: 86ecf553-d340-4e21-af6e-a0c6a421c010
                      task_status: FAILED
                      code: InvalidParameter
                      message: The size is not match xxxxxx
                RUNNING:
                  summary: 任务处理中
                  value:
                    request_id: c1209113-8437-424f-a386-xxxxxx
                    output:
                      task_id: 86ecf553-d340-4e21-af6e-a0c6a421c010
                      task_status: RUNNING
                      submit_time: 2026-03-20 11:48:50.499
                      scheduled_time: 2026-03-20 11:48:50.551
                UNKNOWN:
                  summary: 任务查询过期
                  value:
                    request_id: a4de7c32-7057-9f82-8581-xxxxxx
                    output:
                      task_id: 502a00b1-19d9-4839-a82f-xxxxxx
                      task_status: UNKNOWN
        "400":
          description: 请求参数错误
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
      x-codeSamples:
        - lang: curl
          label: cURL - 查询任务结果
          source: |-
            # 将 {task_id} 替换为创建任务接口返回的 task_id
            curl -X GET 'https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY"
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    PixVerseImageToVideoRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: |-
            模型名称。可选值：
            - `pixverse/pixverse-c1-it2v`：针对打斗、法术特效及高速运动等动态场景
            - `pixverse/pixverse-v6-it2v`：通用场景
            - `pixverse/pixverse-v5.6-it2v`：建议升级至 v6
          enum:
            - pixverse/pixverse-c1-it2v
            - pixverse/pixverse-v6-it2v
            - pixverse/pixverse-v5.6-it2v
          example: pixverse/pixverse-c1-it2v
        input:
          type: object
          required:
            - media
          description: 输入的基本信息，如提示词、媒体素材等。
          properties:
            prompt:
              type: string
              description: 文本提示词，用来描述生成视频中期望包含的元素和视觉特点。支持中英文，每个汉字/字母占一个字符。pixverse-c1-it2v 和 pixverse-v6-it2v 不超过 5000 个字符，pixverse-v5.6-it2v 不超过 2048 个字符，超过部分会自动截断。
              example: 镜头从海龟下方缓缓上移，海龟悠然游动，腹部细节清晰可见。
            media:
              type: array
              description: 媒体素材列表，用于指定视频生成所需的图像。图像数量推荐为 1 张，若传入多张图像系统将默认采用最后一个。
              items:
                type: object
                required:
                  - type
                  - url
                properties:
                  type:
                    type: string
                    description: 媒体素材类型。固定值为 `image_url`（图像 URL）。
                    enum:
                      - image_url
                  url:
                    type: string
                    format: uri
                    description: 图像文件的 URL 地址，必须为公网可访问的 URL。支持 HTTP 或 HTTPS 协议。格式支持 JPG、PNG、WEBP，分辨率不超过 10000 像素，文件大小不超过 20MB。
        parameters:
          $ref: "#/components/schemas/PixVerseImageToVideoParameters"
    PixVerseImageToVideoParameters:
      type: object
      required:
        - resolution
        - duration
      description: 视频处理参数，如设置视频分辨率、设置视频时长、开启音频生成、添加水印等。
      properties:
        resolution:
          type: string
          description: 指定生成的视频分辨率档位。resolution 直接影响费用，请在调用前确认模型价格。可选值：`360P`、`540P`、`720P`、`1080P`。
          enum:
            - 360P
            - 540P
            - 720P
            - 1080P
        duration:
          type: integer
          description: |-
            生成视频的时长，单位为秒。duration 直接影响费用，按秒计费。
            - pixverse-c1-it2v 和 pixverse-v6-it2v：取值范围 [1, 15] 之间的整数
            - pixverse-v5.6-it2v：360P/540P/720P 时取值为 5、8、10；1080P 时取值为 5、8
          minimum: 1
          maximum: 15
        audio:
          type: boolean
          description: 是否生成有声视频。开启后模型将根据视频内容自动生成匹配的背景音乐或音效。audio 直接影响费用，请在调用前确认模型价格。
          default: false
          enum:
            - false
            - true
        shot_type:
          type: string
          description: |-
            指定生成视频的镜头类型，控制视频是由一个连续镜头还是多镜头组成。仅 pixverse-v6-it2v 模型支持。
            - `single`：默认值，生成单镜头视频
            - `multi`：多镜头，系统会进行智能分镜

            使用建议：prompt 参数优先级高于 shot_type。若想稳定输出单镜头，设置 `shot_type="single"` 并在 prompt 中描述单镜头场景；若想稳定输出多镜头，设置 `shot_type="multi"` 并在 prompt 中描述多镜头场景。
          enum:
            - single
            - multi
          default: single
        watermark:
          type: boolean
          description: 是否添加水印标识，水印位于视频右下角，文案固定为"AI生成"。
          default: false
          enum:
            - false
            - true
        seed:
          type: integer
          description: 随机数种子，取值范围为 [0, 2147483647]。未指定时系统自动生成随机种子。若需提升生成结果的可复现性，建议固定 seed 值。注意：即使使用相同 seed，也不能保证每次生成结果完全一致。
          minimum: 0
          maximum: 2147483647
    AsyncTaskSubmitResponse:
      type: object
      description: 异步任务提交响应。请保存 task_id，用于查询任务状态与结果。
      properties:
        request_id:
          type: string
          description: 请求唯一标识。可用于请求明细溯源和问题排查。
          example: 4909100c-7b5a-9f92-bfe5-xxxxxx
        output:
          type: object
          description: 任务输出信息。
          properties:
            task_id:
              type: string
              description: 任务 ID。查询有效期 24 小时。
              example: 0385dc79-5ff8-4d82-bcb6-xxxxxx
            task_status:
              type: string
              description: 任务状态。初始状态通常为 `PENDING`。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
    PixVerseI2VTaskStatusResponse:
      type: object
      description: 任务状态查询响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识。可用于请求明细溯源和问题排查。
          example: 7df19cf7-d76c-4bb8-b4c5-xxxxxx
        output:
          type: object
          description: 任务输出信息。
          properties:
            task_id:
              type: string
              description: 任务 ID。查询有效期 24 小时。
              example: 5abf2c85-ea81-4cbf-8918-xxxxxx
            task_status:
              type: string
              description: 任务状态。状态流转：PENDING（排队中）→ RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。CANCELED 表示任务已取消，UNKNOWN 表示任务不存在或状态未知。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - CANCELED
                - UNKNOWN
            submit_time:
              type: string
              description: 任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。
              example: 2026-03-20 11:48:50.499
            scheduled_time:
              type: string
              description: 任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。
              example: 2026-03-20 11:48:50.551
            end_time:
              type: string
              description: 任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。仅在任务状态为 SUCCEEDED 或 FAILED 时返回。
              example: 2026-03-20 11:49:46.462
            orig_prompt:
              type: string
              description: 原始输入的 prompt，对应请求参数 prompt。
            video_url:
              type: string
              format: uri
              description: 视频 URL。仅在 task_status 为 SUCCEEDED 时返回。视频格式为 MP4（H.264 编码）。视频链接暂无过期时间，但不建议将其作为长期存储依赖，请及时下载。
              example: https://media.pixverseai.cn/xxxx.mp4
            code:
              type: string
              description: 请求失败的错误码。请求成功时不会返回此参数。
            message:
              type: string
              description: 请求失败的详细信息。请求成功时不会返回此参数。
        usage:
          type: object
          description: 输出信息统计，只对成功的结果计数。
          properties:
            duration:
              type: integer
              description: 生成视频的总视频时长，用于计费。
            shot_type:
              type: string
              description: 生成视频的镜头类型。
            size:
              type: string
              description: 生成视频的分辨率。
              example: 992*944
            fps:
              type: integer
              description: 生成视频的帧率。
              example: 24
            video_count:
              type: integer
              description: 生成视频的数量。固定为 1。
            audio:
              type: boolean
              description: 生成视频是否为有声视频。
            SR:
              type: string
              description: 生成视频的分辨率档位。
              example: "720"
    DashScopeErrorResponse:
      type: object
      description: DashScope API 错误响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识。可用于问题排查。
        code:
          type: string
          description: 错误码。
          example: InvalidParameter
        message:
          type: string
          description: 错误详情。
          example: Invalid model name
````

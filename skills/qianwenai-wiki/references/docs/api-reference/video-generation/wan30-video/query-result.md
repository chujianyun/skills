> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# wan3.0-video 查询任务结果

> 查询 wan3.0-video 视频生成任务的状态和结果。

## OpenAPI

````yaml get /tasks/{task_id}
openapi: 3.1.0
info:
  title: 万相 3.0 视频生成 API
  description: 万相 3.0 是全能参考视频生成模型（All-in-One），统一支持文生视频、图生视频（首帧/首尾帧）、参考生视频和参考文件生视频等多种用法，最长可生成30秒视频。提交异步任务后，通过 `GET /tasks/{task_id}` 轮询获取结果。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 千问AI平台
security:
  - BearerAuth: []
paths:
  /tasks/{task_id}:
    get:
      operationId: getWan30VideoTaskStatus
      summary: 查询视频生成任务结果
      description: 轮询任务状态，任务成功后获取视频 URL。建议轮询间隔为 15 秒。task_id 有效期为 24 小时。
      parameters:
        - name: task_id
          in: path
          required: true
          description: 提交任务时返回的任务 ID。
          schema:
            type: string
      responses:
        "200":
          description: 任务状态查询成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Wan30VideoTaskStatusResponse"
              examples:
                SUCCEEDED:
                  summary: 任务执行成功
                  value:
                    request_id: 78c9b768-0285-996c-b682-xxxxxx
                    output:
                      task_id: 17ed7e50-00cf-4509-aea1-xxxxxx
                      task_status: SUCCEEDED
                      submit_time: 2026-08-06 10:01:35.452
                      scheduled_time: 2026-08-06 10:01:35.507
                      end_time: 2026-08-06 10:13:33.838
                      orig_prompt: A golden retriever running on a sunny beach, waves crashing in the background, cinematic lighting
                      video_url: https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx/video.mp4
                    usage:
                      video_count: 1
                      duration: 5
                      input_video_duration: 0
                      output_video_duration: 5
                      fps: 30
                      SR: 720
                      ratio: 16:9
                FAILED:
                  summary: 任务执行失败
                  value:
                    request_id: e5e57877-c0fc-47ed-8fad-xxxxxx
                    output:
                      task_id: eff1443c-ccab-4676-aad3-xxxxxx
                      task_status: FAILED
                      code: InvalidParameter
                      message: The two modes are mutually exclusive. Do not pass reference_xx and first_frame/last_frame at the same time.
                RUNNING:
                  summary: 任务执行中
                  value:
                    request_id: c1209113-8437-424f-a386-xxxxxx
                    output:
                      task_id: 17ed7e50-00cf-4509-aea1-xxxxxx
                      task_status: RUNNING
                      submit_time: 2026-08-06 10:01:35.452
                      scheduled_time: 2026-08-06 10:01:35.507
                UNKNOWN:
                  summary: 任务查询过期
                  value:
                    request_id: a4de7c32-7057-9f82-8581-xxxxxx
                    output:
                      task_id: 502a00b1-19d9-4839-a82f-xxxxxx
                      task_status: UNKNOWN
        "400":
          description: 请求参数无效
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
      x-codeSamples:
        - lang: curl
          label: 查询任务结果
          source: |-
            curl -X GET 'https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}' \
                --header "Authorization: Bearer $DASHSCOPE_API_KEY"
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    Wan30VideoRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称。固定值：`wan3.0-video`。
          enum:
            - wan3.0-video
          example: wan3.0-video
        input:
          type: object
          description: 输入的基本信息。`prompt` 和 `media` 必填其一。
          properties:
            prompt:
              type: string
              description: 文本提示词，用来描述期望生成的视频内容。和 `media` 必填其一。支持中英文，每个汉字/字母占一个字符，不超过 20000 个字符，超过部分会自动截断。在全能参考模式下，prompt 中可以用"图1""视频1"等指代 media 数组中对应顺序的媒体素材。
              maxLength: 20000
              example: 一只小猫在月光下的屋顶上奔跑，城市的霓虹灯在远处闪烁，电影级画质，流畅运镜。
            media:
              type: array
              description: 媒体素材数组，支持图像、视频、音频、文件和网页作为输入。和 `prompt` 必填其一。在参考生视频模式下，按照数组顺序定义 prompt 中素材引用的顺序（图和视频分别计数）。`reference_xx`/`file`/`link` 类型和 `first_frame`/`last_frame` 类型互斥，不能在同一请求中混用。
              items:
                $ref: "#/components/schemas/MediaItem"
        parameters:
          $ref: "#/components/schemas/Wan30VideoParameters"
    MediaItem:
      type: object
      required:
        - type
        - url
      properties:
        type:
          type: string
          description: 媒体素材类型。`reference_xx`/`file`/`link` 类型和 `first_frame`/`last_frame` 类型互斥。
          enum:
            - first_frame
            - last_frame
            - reference_image
            - reference_video
            - reference_audio
            - file
            - link
        url:
          type: string
          description: 媒体素材 URL 或 Base64 编码数据。支持公网 URL（HTTP/HTTPS）、OSS 临时 URL（`oss://dashscope-instant/...`）和 Base64 编码（`data:{MIME_type};base64,{data}`）。
    Wan30VideoParameters:
      type: object
      description: 视频处理参数。
      properties:
        resolution:
          type: string
          description: 生成视频的分辨率档位。
          enum:
            - 480P
            - 720P
            - 1080P
          default: 1080P
        ratio:
          type: string
          description: 生成视频的宽高比。`adaptive` 表示根据输入媒体比例和意图自动推荐合适的长宽比。
          enum:
            - adaptive
            - 16:9
            - 4:3
            - 1:1
            - 3:4
            - 9:16
          default: adaptive
        duration:
          type: integer
          description: 生成视频的时长，单位为秒。无视频输入时取值范围为 [2, 30] 的整数；有视频输入时输入视频总时长 + 输出视频时长不超过 30 秒。传 `-1` 时为智能时长模式，模型根据输入自动推荐合适时长。
          default: 5
        audio:
          type: boolean
          description: 输出视频是否包含音频。`true`（默认）：包含声音；`false`：不包含音轨。开关声音价格相同。
          default: true
        seed:
          type: integer
          description: 随机种子，用于复现生成结果。
          minimum: 0
          maximum: 2147483647
        watermark:
          type: boolean
          description: 是否添加水印标识。
          default: false
    AsyncTaskSubmitResponse:
      type: object
      description: 异步任务提交响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识，用于链路追踪和问题排查。
          example: 4909100c-7b5a-9f92-bfe5-xxxxxx
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID，查询有效期 24 小时。配合 `GET /tasks/{task_id}` 使用。请勿重复创建任务，轮询获取即可。
              example: 0385dc79-5ff8-4d82-bcb6-xxxxxx
            task_status:
              type: string
              description: 初始任务状态，通常为 `PENDING`。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - CANCELED
                - UNKNOWN
    Wan30VideoTaskStatusResponse:
      type: object
      description: 万相 3.0 视频生成任务状态响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识。可用于请求明细溯源和问题排查。
          example: 78c9b768-0285-996c-b682-xxxxxx
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID。
              example: 17ed7e50-00cf-4509-aea1-xxxxxx
            task_status:
              type: string
              description: 任务状态。流转：`PENDING`（排队中）-> `RUNNING`（处理中）-> `SUCCEEDED`（成功）/ `FAILED`（失败）。手动取消为 `CANCELED`，过期为 `UNKNOWN`。
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
              example: 2026-08-06 10:01:35.452
            scheduled_time:
              type: string
              description: 任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。
              example: 2026-08-06 10:01:35.507
            end_time:
              type: string
              description: 任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。仅在 `SUCCEEDED` 或 `FAILED` 时返回。
              example: 2026-08-06 10:13:33.838
            orig_prompt:
              type: string
              description: 原始输入的提示词。
            video_url:
              type: string
              format: uri
              description: 生成视频的 URL 地址。仅在 `task_status` 为 `SUCCEEDED` 时返回。视频 URL 仅保留 24 小时，请及时保存。
              example: https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx/video.mp4
            code:
              type: string
              description: 错误码。仅在 `task_status` 为 `FAILED` 时返回。
            message:
              type: string
              description: 错误信息。仅在 `task_status` 为 `FAILED` 时返回。
        usage:
          type: object
          description: 输出信息统计。只对成功的结果计数。
          properties:
            video_count:
              type: integer
              description: 生成视频的数量。固定为 1。
            duration:
              type: number
              description: 生成视频的时长，单位为秒。
            input_video_duration:
              type: number
              description: 输入视频的时长，单位为秒。无视频输入时为 0.0。
            output_video_duration:
              type: number
              description: 输出视频的时长，单位为秒。
            fps:
              type: integer
              description: 生成视频的帧率。
            SR:
              type: integer
              description: 生成视频的分辨率。示例值：720。
            ratio:
              type: string
              description: 生成视频的宽高比。示例值：16:9。
    DashScopeErrorResponse:
      type: object
      description: API 错误响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识，用于链路追踪和问题排查。
        code:
          type: string
          description: 错误码。
          example: InvalidApiKey
        message:
          type: string
          description: 错误描述信息。
          example: No API-key provided.
````

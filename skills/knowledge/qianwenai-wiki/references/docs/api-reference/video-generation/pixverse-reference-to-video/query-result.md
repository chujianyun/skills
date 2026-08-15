> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# PixVerse — 查询参考生视频结果

> 查询 PixVerse 参考生视频任务状态

轮询任务状态，任务完成后下载视频。响应包含时间戳和原始提示词，便于追踪。

## 轮询策略

1. 保存[提交任务](/api-reference/video-generation/pixverse-reference-to-video/create-task)返回的 `task_id`。
2. 每 **15 秒**轮询一次本接口，直到 `task_status` 为 `SUCCEEDED` 或 `FAILED`。
3. 任务成功后，从 `video_url` 下载视频。

## 注意事项

- **链接有效期**：视频下载链接在 **24 小时**后失效，请及时下载。
- **状态流转**：`PENDING` → `RUNNING` → `SUCCEEDED` 或 `FAILED`。
- **任务过期**：长时间未查询的任务可能返回 `UNKNOWN` 状态，表示任务已过期。
- **计量详情**：响应中的 `usage` 字段返回视频时长、分辨率、帧率等计量信息。

## OpenAPI

````yaml get /tasks/{task_id}
openapi: 3.1.0
info:
  title: PixVerse-参考生视频
  description: PixVerse 参考生视频模型支持传入多张参考图片或视频，通过文本提示词描述场景，将图片中的主体角色融合生成一段流畅的视频。支持通过 `@ref_name` 语法精确引用参考图中的主体。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 千问AI平台
security:
  - BearerAuth: []
paths:
  /tasks/{task_id}:
    get:
      operationId: getPixVerseRefToVideoTaskStatus
      summary: 查询任务结果
      description: 根据任务 ID 查询参考生视频任务的状态和结果。创建任务成功后，使用接口返回的 task_id 查询结果，task_id 有效期为 24 小时。
      parameters:
        - name: task_id
          in: path
          required: true
          description: 任务 ID。由创建任务接口返回，查询有效期 24 小时。
          schema:
            type: string
        - name: Authorization
          in: header
          required: true
          description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
          schema:
            type: string
      responses:
        "200":
          description: 成功获取任务状态和结果。
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/TaskStatusResponse"
              examples:
                SUCCEEDED:
                  summary: 任务执行成功
                  value:
                    request_id: 35137489-2862-96cb-b6f2-xxxxxx
                    output:
                      task_id: 1469cfc3-3004-4d9e-ab10-xxxxxx
                      task_status: SUCCEEDED
                      submit_time: 2026-03-10 15:03:25.848
                      scheduled_time: 2026-03-10 15:03:25.884
                      end_time: 2026-03-10 15:04:05.882
                      orig_prompt: 男人坐在靠窗的椅子上，手持吉他，在咖啡厅旁演奏一首舒缓的美国乡村民谣
                      video_url: https://media.pixverseai.cn/xxxx.mp4
                    usage:
                      duration: 5
                      size: 1280*720
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
                      task_id: 966cebcd-dedc-4962-af88-xxxxxx
                      task_status: RUNNING
                UNKNOWN:
                  summary: 任务查询过期
                  value:
                    request_id: a4de7c32-7057-9f82-8581-xxxxxx
                    output:
                      task_id: 502a00b1-19d9-4839-a82f-xxxxxx
                      task_status: UNKNOWN
        "400":
          description: 请求参数无效。
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
      x-codeSamples:
        - lang: curl
          label: 查询任务结果
          source: |-
            # 将 {task_id} 替换为创建任务接口返回的实际 task ID
            curl -X GET 'https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY"
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    PixVerseRefToVideoRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称。可选值：`pixverse/pixverse-v6-r2v-omni`（需要图片+视频融合参考生成时推荐）、`pixverse/pixverse-c1-r2v`（适用于打斗、法术特效及高速运动等动态场景以及多宫格场景）、`pixverse/pixverse-v6-r2v`（通用场景推荐）、`pixverse/pixverse-v5.6-r2v`（建议升级至v6）。
          enum:
            - pixverse/pixverse-v6-r2v-omni
            - pixverse/pixverse-c1-r2v
            - pixverse/pixverse-v6-r2v
            - pixverse/pixverse-v5.6-r2v
          example: pixverse/pixverse-c1-r2v
        input:
          $ref: "#/components/schemas/PixVerseRefToVideoInput"
        parameters:
          $ref: "#/components/schemas/PixVerseRefToVideoParameters"
    PixVerseRefToVideoInput:
      type: object
      required:
        - prompt
        - media
      description: 输入的基本信息，包括参考图片和提示词。
      properties:
        prompt:
          type: string
          description: |-
            文本提示词，用来描述生成视频中期望包含的元素和视觉特点。支持中英文，每个汉字/字母占一个字符，超过部分会自动截断。`pixverse/pixverse-v6-r2v-omni` 不超过 5000 个字符，`pixverse/pixverse-c1-r2v` 不超过 5000 个字符，`pixverse/pixverse-v6-r2v` 不超过 2048 个字符，`pixverse/pixverse-v5.6-r2v` 不超过 2048 个字符。

            当在 media 参数中传入参考图时，可以通过 `@ref_name` 在 prompt 中直接引用该图片。media 中设置的 ref_name 在同一请求内必须全局唯一，且须与 prompt 中的引用一一对应。书写规范：必须在 `@ref_name` 后保留一个空格作为分隔。
          example: "@男人 坐在靠窗的椅子上，手持@吉他 ，在@咖啡厅 旁演奏一首舒缓的美国乡村民谣"
        media:
          type: array
          description: 媒体素材列表，用于指定视频生成所需的参考图像或视频。数组的每个元素为一个媒体对象，包含 type 和 url 字段。图像数量：1～7 张。
          items:
            $ref: "#/components/schemas/MediaItem"
          minItems: 1
          maxItems: 7
    MediaItem:
      type: object
      required:
        - type
        - url
      description: 媒体素材对象。
      properties:
        type:
          type: string
          description: 媒体素材类型。`image_url`（图像 URL）或 `video_url`（视频 URL，仅 pixverse/pixverse-v6-r2v-omni 支持）。
          enum:
            - image_url
            - video_url
        url:
          type: string
          format: uri
          description: 媒体文件的 URL 地址，必须为公网可访问的 URL。支持 HTTP 或 HTTPS 协议。图像格式支持 JPG、PNG、WEBP，分辨率宽度和高度均不超过 10000 像素，文件大小不超过 20MB。视频格式支持 MP4。
        ref_name:
          type: string
          description: 参考图片中主体的名称标识，用于在 prompt 中通过 `@ref_name` 引用对应的参考图片主体。
    PixVerseRefToVideoParameters:
      type: object
      description: 视频生成参数，如设置视频分辨率、时长、是否生成音频等。
      required:
        - duration
      properties:
        resolution:
          type: string
          description: 生成视频的分辨率档位。仅 `pixverse/pixverse-v6-r2v-omni` 使用此参数（omni 模型必选）。
          enum:
            - 360P
            - 540P
            - 720P
            - 1080P
          example: 720P
        aspect_ratio:
          type: string
          description: 生成视频的宽高比。仅 `pixverse/pixverse-v6-r2v-omni` 使用此参数（omni 模型必选）。`auto` 表示自动采用第一个图片或视频的宽高比。
          enum:
            - auto
            - 16:9
            - 4:3
            - 1:1
            - 3:4
            - 9:16
            - 3:2
            - 2:3
            - 21:9
          example: 16:9
        size:
          type: string
          description: |-
            生成视频的分辨率，格式为 `宽*高` 的像素值。c1/v6/v5.6 模型必选，不支持 pixverse/pixverse-v6-r2v-omni 模型（omni 使用 `resolution` + `aspect_ratio`）。

            **pixverse/pixverse-c1-r2v 支持的分辨率：**
            - 360P：`640*360`(16:9)、`640*480`(4:3)、`640*640`(1:1)、`480*640`(3:4)、`360*640`(9:16)、`640*432`(3:2)、`432*640`(2:3)、`640*288`(21:9)
            - 540P：`1024*576`、`1024*768`、`1024*1024`、`768*1024`、`576*1024`、`1024*688`、`688*1024`、`1024*448`
            - 720P：`1280*720`、`1108*832`、`960*960`、`832*1108`、`720*1280`、`1200*800`、`800*1200`、`1280*560`
            - 1080P：`1920*1080`、`1664*1248`、`1440*1440`、`1248*1664`、`1080*1920`、`1776*1184`、`1184*1776`、`1920*832`

            **pixverse/pixverse-v6-r2v 支持的分辨率：**
            - 360P：`640*360`(16:9)、`640*480`(4:3)、`640*640`(1:1)、`480*640`(3:4)、`360*640`(9:16)、`640*432`(3:2)、`432*640`(2:3)、`640*288`(21:9)
            - 540P：`1024*576`、`1024*768`、`1024*1024`、`768*1024`、`576*1024`、`1024*688`、`688*1024`、`1024*448`
            - 720P：`1280*720`、`1108*832`、`960*960`、`832*1108`、`720*1280`、`1200*800`、`800*1200`、`1280*560`
            - 1080P：`1920*1080`、`1664*1248`、`1440*1440`、`1248*1664`、`1080*1920`、`1776*1184`、`1184*1776`、`1920*832`

            **pixverse/pixverse-v5.6-r2v 支持的分辨率（建议升级至v6）：**
            - 360P：`640*360`(16:9)、`640*480`(4:3)、`640*640`(1:1)、`480*640`(3:4)、`360*640`(9:16)
            - 540P：`1024*576`、`1024*768`、`1024*1024`、`768*1024`、`576*1024`
            - 720P：`1280*720`、`1108*830`(4:3)、`960*960`、`830*1108`(3:4)、`720*1280`
            - 1080P：`1920*1080`、`1662*1246`(4:3)、`1440*1440`、`1246*1662`(3:4)、`1080*1920`
          example: 1280*720
        duration:
          type: integer
          description: |-
            生成视频的时长，单位为秒。

            - `pixverse/pixverse-v6-r2v-omni`：有视频参考时必须填 `0`，系统将自动取输入视频中的最长时长；仅图片参考时取值范围为 [1, 15] 之间的整数。
            - `pixverse/pixverse-c1-r2v`：取值范围为 [1, 15] 之间的整数。
            - `pixverse/pixverse-v6-r2v`：取值范围为 [1, 15] 之间的整数。
            - `pixverse/pixverse-v5.6-r2v`：当 size 为 360P/540P/720P 时，取值为 5、8、10；当 size 为 1080P 时，取值为 5、8。
          example: 5
        audio:
          type: boolean
          description: 是否生成有声视频。开启后模型将根据视频内容自动生成匹配的背景音乐或音效。`false`（默认值）：输出无声视频；`true`：输出有声视频。
          default: false
        watermark:
          type: boolean
          description: 是否添加水印标识，水印位于视频右下角，文案固定为"AI生成"。`false`（默认值）：不添加水印；`true`：添加水印。
          default: false
        seed:
          type: integer
          description: 随机数种子，取值范围为 [0, 2147483647]。未指定时系统自动生成随机种子。若需提升生成结果的可复现性，建议固定 seed 值。由于模型生成具有概率性，即使使用相同 seed 也不能保证每次生成结果完全一致。
          minimum: 0
          maximum: 2147483647
    AsyncTaskSubmitResponse:
      type: object
      description: 异步任务创建成功的响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识。可用于请求明细溯源和问题排查。
        output:
          type: object
          description: 任务输出信息。
          properties:
            task_id:
              type: string
              description: 任务 ID。使用 `GET /tasks/{task_id}` 查询结果，查询有效期 24 小时。
            task_status:
              type: string
              description: 任务状态。初始创建后通常为 `PENDING`。
              enum:
                - PENDING
    TaskStatusResponse:
      type: object
      description: 任务状态和结果的响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识。可用于请求明细溯源和问题排查。
        output:
          type: object
          description: 任务输出信息。
          properties:
            task_id:
              type: string
              description: 任务 ID。查询有效期 24 小时。
            task_status:
              type: string
              description: 任务状态。状态流转：PENDING（排队中）→ RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）/ CANCELED（已取消）。初次查询状态通常为 PENDING 或 RUNNING。当状态变为 SUCCEEDED 时，响应中将包含生成的视频 URL。
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
            scheduled_time:
              type: string
              description: 任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。
            end_time:
              type: string
              description: 任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。
            orig_prompt:
              type: string
              description: 原始输入的 prompt，对应请求参数 prompt。
            video_url:
              type: string
              format: uri
              description: 视频 URL。仅在 task_status 为 SUCCEEDED 时返回。视频格式为 MP4（H.264 编码），请及时下载。
            code:
              type: string
              description: 请求失败的错误码。仅在 task_status 为 FAILED 时返回。
            message:
              type: string
              description: 请求失败的详细信息。仅在 task_status 为 FAILED 时返回。
        usage:
          type: object
          description: 输出信息统计。只对成功的结果返回。
          properties:
            duration:
              type: integer
              description: 生成视频的时长（秒），用于计费。
            size:
              type: string
              description: 生成视频的分辨率。
            fps:
              type: integer
              description: 生成视频的帧率。
            SR:
              type: string
              description: 生成视频的分辨率档位。
            audio:
              type: boolean
              description: 生成视频是否为有声视频。
            video_count:
              type: integer
              description: 生成视频的数量，固定为 1。
    DashScopeErrorResponse:
      type: object
      description: DashScope API 错误响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识。
        code:
          type: string
          description: 请求失败的错误码。请求成功时不会返回此参数。
          example: InvalidParameter
        message:
          type: string
          description: 请求失败的详细信息。请求成功时不会返回此参数。
          example: The size is not match xxxxxx
````

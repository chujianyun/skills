> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# PixVerse — 创建任务

> 提交 PixVerse 参考生视频任务

基于参考图片与文本提示词，使用 PixVerse 模型生成视频。

- **模型选型**：`pixverse/pixverse-c1-r2v` 适用于打斗、法术特效及高速运动等动态场景以及多宫格场景；`pixverse/pixverse-v6-r2v` 通用场景推荐使用。
- **参考图绑定**：通过 `media` 数组提供最多 7 张参考图片，在提示词中使用 `@ref_name` 精确绑定角色或物体。
- **灵活分辨率**：支持从 360P 到 1080P 多种分辨率与画面比例（16:9、4:3、1:1、3:4、9:16 等）。
- **音频与水印**：可选生成带音频的视频，支持添加"AI生成"水印。
- **可复现结果**：通过 `seed` 参数固定随机种子，实现结果复现。

## OpenAPI

````yaml post /services/aigc/video-generation/video-synthesis
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
  /services/aigc/video-generation/video-synthesis:
    post:
      operationId: createPixVerseRefToVideo
      summary: 创建参考生视频任务
      description: 创建 PixVerse 参考生视频任务，通过参考图片和文本提示词生成视频。由于任务耗时较长（通常为1-5分钟），API 采用异步调用方式。
      parameters:
        - name: X-DashScope-Async
          in: header
          required: true
          description: 异步处理配置参数。HTTP 请求只支持异步，必须设置为 `enable`。缺少此请求头将报错："current user api does not support synchronous calls"。
          schema:
            type: string
            enum:
              - enable
        - name: Content-Type
          in: header
          required: true
          description: 请求内容类型。此参数必须设置为 `application/json`。
          schema:
            type: string
        - name: Authorization
          in: header
          required: true
          description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/PixVerseRefToVideoRequest"
      responses:
        "200":
          description: 任务创建成功，返回任务 ID。
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/AsyncTaskSubmitResponse"
        "400":
          description: 请求参数无效。
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
      x-codeSamples:
        - lang: curl
          label: 参考生视频（图片+视频，omni）
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
              "model": "pixverse/pixverse-v6-r2v-omni",
              "input": {
                "media": [
                  {
                    "type": "video_url",
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qigswt/wan-r2v-role2.mp4",
                    "ref_name": "参考视频"
                  },
                  {
                    "type": "image_url",
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260320/knsple/wan-r2v-role-frame.jpg",
                    "ref_name": "男人"
                  },
                  {
                    "type": "image_url",
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/wfjikw/wan-r2v-backgroud5.png",
                    "ref_name": "咖啡厅"
                  }
                ],
                "prompt": "@男人 在@咖啡厅 中弹吉他 参考@参考视频"
              },
              "parameters": {
                "resolution": "720P",
                "aspect_ratio": "16:9",
                "duration": 0,
                "audio": true,
                "watermark": false
              }
            }'
        - lang: curl
          label: 参考生视频
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
              "model": "pixverse/pixverse-c1-r2v",
              "input": {
                "media": [
                  {
                    "type": "image_url",
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260320/knsple/wan-r2v-role-frame.jpg"
                  },
                  {
                    "type": "image_url",
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qpzxps/wan-r2v-object4.png"
                  },
                  {
                    "type": "image_url",
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/wfjikw/wan-r2v-backgroud5.png"
                  }
                ],
                "prompt": "男人坐在靠窗的椅子上，手持吉他，在咖啡厅旁演奏一首舒缓的美国乡村民谣"
              },
              "parameters": {
                "size": "1280*720",
                "duration": 5,
                "audio": false,
                "watermark": true
              }
            }'
        - lang: curl
          label: 参考生视频（使用ref_name）
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
              "model": "pixverse/pixverse-c1-r2v",
              "input": {
                "media": [
                  {
                    "type": "image_url",
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260320/knsple/wan-r2v-role-frame.jpg",
                    "ref_name": "男人"
                  },
                  {
                    "type": "image_url",
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qpzxps/wan-r2v-object4.png",
                    "ref_name": "吉他"
                  },
                  {
                    "type": "image_url",
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/wfjikw/wan-r2v-backgroud5.png",
                    "ref_name": "咖啡厅"
                  }
                ],
                "prompt": "@男人 坐在靠窗的椅子上，手持@吉他 ，在@咖啡厅 旁演奏一首舒缓的美国乡村民谣"
              },
              "parameters": {
                "size": "1280*720",
                "duration": 5,
                "audio": false,
                "watermark": true
              }
            }'
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

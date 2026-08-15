> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# PixVerse — 创建任务

> 提交 PixVerse 首尾帧图生视频任务

根据**首帧图像**、**尾帧图像**和**文本提示词**，生成平滑过渡的视频。

## 模型选择

- **pixverse/pixverse-c1-kf2v**：擅长打斗、法术特效和高速运动场景。
- **pixverse/pixverse-v6-kf2v**：通用模型。
- **pixverse/pixverse-v5.6-kf2v**：旧版模型，建议升级至 v6。

## OpenAPI

````yaml post /services/aigc/video-generation/video-synthesis
openapi: 3.1.0
info:
  title: 爱诗-图生视频-基于首尾帧API
  description: 爱诗-首尾帧生视频模型基于首帧图像、尾帧图像和文本提示词，生成一段平滑过渡的视频。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: DashScope API
security:
  - BearerAuth: []
paths:
  /services/aigc/video-generation/video-synthesis:
    post:
      operationId: createPixVerseKf2v
      summary: 创建首尾帧生视频任务
      description: 基于首帧图像、尾帧图像和文本提示词，使用爱诗首尾帧生视频模型创建视频生成任务。该接口采用异步调用方式，返回 task_id 用于后续查询。
      parameters:
        - name: X-DashScope-Async
          in: header
          required: true
          description: 异步处理配置参数。HTTP请求只支持异步，必须设置为 `enable`。缺少此请求头将报错："current user api does not support synchronous calls"。
          schema:
            type: string
            enum:
              - enable
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/PixVerseKf2vRequest"
      responses:
        "200":
          description: 任务提交成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/AsyncTaskSubmitResponse"
        "400":
          description: 请求参数错误
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
      x-codeSamples:
        - lang: curl
          label: cURL
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
              "model": "pixverse/pixverse-c1-kf2v",
              "input": {
                "media": [
                  {"type": "first_frame", "url": "https://wanx.alicdn.com/material/20250318/first_frame.png"},
                  {"type": "last_frame", "url": "https://wanx.alicdn.com/material/20250318/last_frame.png"}
                ],
                "prompt": "一只小猫从窗台向下跳跃，轻盈地落在沙发上，然后好奇地环顾四周。"
              },
              "parameters": {
                "resolution": "720P",
                "duration": 5,
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
    PixVerseKf2vRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称。可选值：`pixverse/pixverse-c1-kf2v`（针对打斗、法术特效及高速运动等动态场景）、`pixverse/pixverse-v6-kf2v`（通用场景）、`pixverse/pixverse-v5.6-kf2v`（建议升级至v6）。
          enum:
            - pixverse/pixverse-c1-kf2v
            - pixverse/pixverse-v6-kf2v
            - pixverse/pixverse-v5.6-kf2v
          example: pixverse/pixverse-c1-kf2v
        input:
          type: object
          required:
            - media
            - prompt
          description: 输入的基本信息，包含首帧、尾帧图像和提示词。
          properties:
            prompt:
              type: string
              description: 文本提示词。用来描述首帧到尾帧之间的变化过程。支持中英文，每个汉字/字母占一个字符，字符编码为UTF-8，超过部分会自动截断。pixverse/pixverse-c1-kf2v 和 pixverse/pixverse-v6-kf2v：不超过5000个字符；pixverse/pixverse-v5.6-kf2v：不超过2048个字符。
              maxLength: 5000
              example: 一只小猫从窗台向下跳跃，轻盈地落在沙发上，然后好奇地环顾四周。
            media:
              type: array
              description: 媒体资源列表，包含首帧和尾帧图像。数组的每个元素为一个媒体对象，包含 type 与 url 字段。media数组中需要包含两个对象，分别设置type为first_frame（首帧）和last_frame（尾帧），顺序不影响结果，系统会根据type字段自动识别。首帧和尾帧图像的分辨率不需要一致，系统会自动处理，输出视频的宽高比将以首帧图像为基准（近似）。
              items:
                type: object
                required:
                  - type
                  - url
                properties:
                  type:
                    type: string
                    description: 媒体类型。`first_frame`：首帧图像，有且仅有1张。`last_frame`：尾帧图像，有且仅有1张。
                    enum:
                      - first_frame
                      - last_frame
                  url:
                    type: string
                    description: 图像的公网可访问URL，支持 HTTP 或 HTTPS 协议。示例值：https://xxx/xxx.png。图像限制：格式为JPG、PNG、WEBP；宽度和高度均不超过10000像素；文件大小不超过20MB。
                    example: https://wanx.alicdn.com/material/20250318/first_frame.png
              minItems: 2
              maxItems: 2
              example:
                - type: first_frame
                  url: https://wanx.alicdn.com/material/20250318/first_frame.png
                - type: last_frame
                  url: https://wanx.alicdn.com/material/20250318/last_frame.png
        parameters:
          $ref: "#/components/schemas/PixVerseKf2vParameters"
    PixVerseKf2vParameters:
      type: object
      required:
        - resolution
        - duration
      description: 视频生成参数。如设置视频分辨率、时长、是否生成音频等。
      properties:
        resolution:
          type: string
          description: 生成视频的分辨率。可选值：360P、540P、720P、1080P。resolution直接影响费用，请在调用前确认模型价格。
          enum:
            - 360P
            - 540P
            - 720P
            - 1080P
          example: 720P
        duration:
          type: integer
          description: 生成视频的时长，单位为秒。pixverse/pixverse-c1-kf2v 和 pixverse/pixverse-v6-kf2v：取值范围为[1, 15]之间的整数。pixverse/pixverse-v5.6-kf2v：当resolution为360P/540P/720P时取值为5、8、10；当resolution为1080P时取值为5、8。duration直接影响费用，请在调用前确认模型价格。
          minimum: 1
          maximum: 15
          example: 5
        audio:
          type: boolean
          description: 是否生成有声视频。开启后模型将根据视频内容自动生成匹配的背景音乐或音效。默认值：false（输出无声视频）。audio直接影响费用，请在调用前确认模型价格。
          default: false
        watermark:
          type: boolean
          description: 是否添加水印标识，水印位于视频右下角，文案固定为"AI生成"。默认值：false（不添加水印）。
          default: false
        seed:
          type: integer
          description: 随机数种子，取值范围为 [0, 2147483647]。未指定时，系统自动生成随机种子。若需提升生成结果的可复现性，建议固定seed值。请注意，由于模型生成具有概率性，即使使用相同 seed，也不能保证每次生成结果完全一致。
          minimum: 0
          maximum: 2147483647
    AsyncTaskSubmitResponse:
      type: object
      description: 异步任务提交响应。创建成功后，使用接口返回的 task_id 查询结果，task_id 有效期为 24 小时。请勿重复创建任务，轮询获取即可。
      properties:
        request_id:
          type: string
          description: 请求唯一标识。可用于请求明细溯源和问题排查。
          example: 4909100c-7b5a-9f92-bfe5-xxxxxx
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务ID。用于查询任务状态与结果，有效期24小时。
              example: 0385dc79-5ff8-4d82-bcb6-xxxxxx
            task_status:
              type: string
              description: 任务状态。初始状态通常为 PENDING。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - CANCELED
                - UNKNOWN
    TaskStatusResponse:
      type: object
      description: 查询任务状态与结果的响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识。可用于请求明细溯源和问题排查。
          example: 40799260-689c-4c44-9d7c-xxxxxx
        output:
          type: object
          description: 任务输出信息。
          properties:
            task_id:
              type: string
              description: 任务ID。查询有效期24小时。
              example: 408b6c3b-27c9-43dd-b928-xxxxxx
            task_status:
              type: string
              description: 任务状态。轮询过程中的状态流转：PENDING（排队中）→ RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。初次查询状态通常为 PENDING 或 RUNNING。UNKNOWN 表示任务不存在或状态未知。
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
              example: 2026-03-20 13:47:42.916
            scheduled_time:
              type: string
              description: 任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。
              example: 2026-03-20 13:47:42.949
            end_time:
              type: string
              description: 任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。
              example: 2026-03-20 13:48:41.896
            video_url:
              type: string
              description: 视频URL。仅在 task_status 为 SUCCEEDED 时返回。视频格式为MP4（H.264 编码）。视频链接暂无过期时间，但不建议将其作为长期存储，请及时下载。
              example: https://media.pixverseai.cn/xxx.mp4
            orig_prompt:
              type: string
              description: 原始输入的prompt，对应请求参数 prompt。
            code:
              type: string
              description: 请求失败的错误码。请求成功时不会返回此参数。
            message:
              type: string
              description: 请求失败的详细信息。请求成功时不会返回此参数。
        usage:
          type: object
          description: 输出信息统计。只对成功的结果计数。
          properties:
            duration:
              type: integer
              description: 生成视频的总视频时长，用于计费。
              example: 5
            size:
              type: string
              description: 生成视频的分辨率。
              example: 1280*960
            fps:
              type: integer
              description: 生成视频的帧率。
              example: 24
            video_count:
              type: integer
              description: 生成视频的数量。固定为1。
              example: 1
            audio:
              type: boolean
              description: 生成视频是否为有声视频。
              example: false
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
          description: 请求唯一标识。
        code:
          type: string
          description: 错误码。请参见错误信息文档进行解决。
          example: InvalidApiKey
        message:
          type: string
          description: 错误详情。
          example: No API-key provided.
````

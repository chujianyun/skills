> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Vidu — 查询结果

> 查询 Vidu 文生视频任务的状态与生成结果。

提交任务后，建议每隔 **15 秒**轮询一次该接口，直到 `task_status` 为 `SUCCEEDED` 或 `FAILED`。

## 任务状态流转

`PENDING` → `RUNNING` → `SUCCEEDED` 或 `FAILED`

| 状态          | 说明                                |
| ----------- | --------------------------------- |
| `PENDING`   | 任务排队等待中                           |
| `RUNNING`   | 任务生成中                             |
| `SUCCEEDED` | 任务成功，可获取视频链接                      |
| `FAILED`    | 任务失败，查看 `code` 和 `message` 字段获取原因 |
| `CANCELED`  | 任务已取消                             |
| `UNKNOWN`   | 任务不存在或已过期（超过 24 小时）               |

<Note>
  - 成功响应中的 `video_url` 有效期为 **24 小时**，请及时下载视频。
  - 查询接口的 QPS 限制为 **8 次/秒**。
  - 支持配置异步回调，免去主动轮询。详见[配置异步回调](/developer-guides/run-and-scale/async-task-management)。
  - 如需取消任务或批量管理任务，参见[管理异步任务](/developer-guides/run-and-scale/async-task-management)。
</Note>

## 常见问题

**size 和 resolution 有什么区别？**

- `size` 直接指定输出视频的宽高（像素），优先级高于 `resolution`。
- `resolution` 指定分辨率档位（540P / 720P / 1080P），可与 `size` 配合使用；两者均传入时以 `size` 为准。
- 推荐使用 `size` 精确控制输出尺寸，可用值参见[提交视频任务](/api-reference/video-generation/vidu-text-to-video/create-task)中的 size 参数取值对照表。

## 错误码

请参见[错误信息](/api-reference/preparation/error-messages)。

## OpenAPI

````yaml get /tasks/{task_id}
openapi: 3.0.0
info:
  title: Vidu 文生视频 API
  description: Vidu 文生视频模型基于文本提示词，生成一段流畅的视频。API 采用异步调用模式，包含"创建任务"和"查询结果"两个步骤。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 千问AI平台
security:
  - BearerAuth: []
paths:
  /tasks/{task_id}:
    get:
      operationId: getViduTextToVideoTaskStatus
      summary: 查询任务结果
      description: 根据 task_id 查询任务状态与结果。task_id 有效期为 24 小时。建议设置合理的查询间隔（如 15 秒）进行轮询。
      parameters:
        - name: Authorization
          in: header
          required: true
          description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
          schema:
            type: string
        - name: task_id
          in: path
          required: true
          description: 任务 ID。将上一步接口返回的 task_id 完整替换。查询有效期为 24 小时。
          schema:
            type: string
      responses:
        "200":
          description: 查询成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/TaskStatusResponse"
              examples:
                SUCCEEDED:
                  summary: 任务执行成功
                  value:
                    request_id: eda50dad-a6d3-4e62-a70b-26bbb797ae81
                    output:
                      task_id: d9254244-1f9b-4b4c-be82-d9560ba25708
                      task_status: SUCCEEDED
                      submit_time: 2026-03-27 13:32:13.962
                      scheduled_time: 2026-03-27 13:32:14.008
                      end_time: 2026-03-27 13:32:43.375
                      orig_prompt: 一只小猫在月光下奔跑
                      video_url: https://prod-ss-vidu.s3.cn-northwest-1.amazonaws.com.cn/xxx.mp4?xxx
                    usage:
                      duration: 5
                      size: 960*528
                      output_video_duration: 5
                      fps: 24
                      video_count: 1
                      audio: false
                      SR: "540"
                RUNNING:
                  summary: 任务生成中
                  value:
                    request_id: b3c41e52-9d1a-4f87-bc23-xxxxxx
                    output:
                      task_id: d9254244-1f9b-4b4c-be82-d9560ba25708
                      task_status: RUNNING
                      submit_time: 2026-03-27 13:32:13.962
                      scheduled_time: 2026-03-27 13:32:14.008
                FAILED:
                  summary: 任务执行失败
                  value:
                    request_id: e5d70b02-ebd3-98ce-9fe8-759d7d7b107d
                    output:
                      task_id: 86ecf553-d340-4e21-af6e-a0c6a421c010
                      task_status: FAILED
                      code: InvalidParameter
                      message: The size is not match xxxxxx
                UNKNOWN:
                  summary: 任务查询过期
                  value:
                    request_id: a4de7c32-7057-9f82-8581-xxxxxx
                    output:
                      task_id: 502a00b1-19d9-4839-a82f-xxxxxx
                      task_status: UNKNOWN
        "400":
          description: 请求失败
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
      x-codeSamples:
        - lang: curl
          label: cURL
          source: |-
            curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id} \
              --header "Authorization: Bearer $DASHSCOPE_API_KEY"
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    ViduTextToVideoRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称。
          enum:
            - vidu/viduq3-turbo_text2video
            - vidu/viduq3-pro_text2video
            - vidu/viduq2_text2video
          example: vidu/viduq3-turbo_text2video
        input:
          type: object
          required:
            - prompt
          description: 输入的基本信息，如提示词等。
          properties:
            prompt:
              type: string
              description: |-
                文本提示词。用来描述生成视频中期望包含的元素和视觉特点。支持中英文，每个汉字/字母占一个字符，不能超过 5000 个字符，超过部分会自动截断。示例值：一只小猫在月光下奔跑。

                提示词编写请参见Vidu视频生成Prompt指南。
              example: 一只小猫在月光下奔跑
        parameters:
          $ref: "#/components/schemas/ViduTextToVideoParameters"
    ViduTextToVideoParameters:
      type: object
      description: 视频生成参数，如设置视频分辨率、时长等。
      properties:
        resolution:
          type: string
          description: 分辨率档位。resolution 直接影响费用，请在调用前确认模型价格。
          enum:
            - 540P
            - 720P
            - 1080P
          default: 720P
          example: 720P
        size:
          type: string
          description: 生成视频的分辨率，格式为宽*高的像素值。默认值根据 resolution 而定：resolution=540P 时默认为 960*528，resolution=720P 时默认为 1280*720，resolution=1080P 时默认为 1920*1080。
        duration:
          type: integer
          description: 生成视频的时长，单位为秒。duration 直接影响费用，按秒计费，时间越长费用越高。vidu/viduq3-pro_text2video 和 vidu/viduq3-turbo_text2video：取值为 [1, 16] 之间的整数，默认值为 5。vidu/viduq2_text2video：取值为 [1, 10] 之间的整数，默认值为 5。
          default: 5
          example: 5
        audio:
          type: boolean
          description: 是否生成有声视频。开启后模型将根据视频内容自动生成匹配的背景音乐或音效。支持模型：vidu/viduq3-pro_text2video、vidu/viduq3-turbo_text2video。
          default: false
          example: false
        watermark:
          type: boolean
          description: 是否添加水印标识，水印位于视频右下角，文案固定为"内容由 AI 生成"。
          default: false
          example: false
        seed:
          type: integer
          description: 随机数种子，取值范围为 [0, 2147483647]。未指定时系统自动生成随机种子。若需提升生成结果的可复现性，建议固定 seed 值。由于模型生成具有概率性，即使使用相同 seed，也不能保证每次生成结果完全一致。示例值：12345。
          minimum: 0
          maximum: 2147483647
          example: 12345
    AsyncTaskSubmitResponse:
      type: object
      description: 异步任务创建成功响应。
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
              description: 任务 ID。用于查询任务状态与结果，有效期 24 小时。
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
              example: PENDING
        code:
          type: string
          description: 请求失败的错误码。请求成功时不会返回此参数。
        message:
          type: string
          description: 请求失败的详细信息。请求成功时不会返回此参数。
    TaskStatusResponse:
      type: object
      description: 任务查询响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识。可用于请求明细溯源和问题排查。
          example: eda50dad-a6d3-4e62-a70b-26bbb797ae81
        output:
          type: object
          description: 任务输出信息。
          properties:
            task_id:
              type: string
              description: 任务 ID。查询有效期 24 小时。
              example: d9254244-1f9b-4b4c-be82-d9560ba25708
            task_status:
              type: string
              description: 任务状态。状态流转：PENDING（排队中）→ RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。初次查询状态通常为 PENDING 或 RUNNING。当状态变为 SUCCEEDED 时，响应中将包含生成的视频 URL。若状态为 FAILED，请检查错误信息并重试。
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
              example: 2026-03-27 13:32:13.962
            scheduled_time:
              type: string
              description: 任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。
              example: 2026-03-27 13:32:14.008
            end_time:
              type: string
              description: 任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。
              example: 2026-03-27 13:32:43.375
            orig_prompt:
              type: string
              description: 原始输入的 prompt，对应请求参数 prompt。
              example: 一只小猫在月光下奔跑
            video_url:
              type: string
              description: 视频 URL。仅在 task_status 为 SUCCEEDED 时返回。视频格式为 MP4（H.264 编码），链接有效期 24 小时，请及时下载。
              example: https://prod-ss-vidu.s3.cn-northwest-1.amazonaws.com.cn/xxx.mp4?xxx
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
              description: 总的视频计费时长（秒）。示例值：5。
              example: 5
            size:
              type: string
              description: 生成视频的分辨率。示例值：960*528。
              example: 960*528
            output_video_duration:
              type: integer
              description: 输出视频的时长（秒）。示例值：5。
              example: 5
            fps:
              type: integer
              description: 生成视频的帧率。示例值：24。
              example: 24
            audio:
              type: boolean
              description: 生成视频是否为有声视频。示例值：false。
              example: false
            SR:
              type: string
              description: 生成视频的分辨率档位。示例值：540。
              example: "540"
            video_count:
              type: integer
              description: 生成视频的数量。固定为 1。
              example: 1
    DashScopeErrorResponse:
      type: object
      description: DashScope API 错误响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识。
          example: 7438d53d-6eb8-4596-8835-xxxxxx
        code:
          type: string
          description: 错误码。
          example: InvalidApiKey
        message:
          type: string
          description: 错误详细信息。
          example: No API-key provided.
````

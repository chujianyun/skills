> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 表情包视频 Emoji — 查询结果

> 查询表情包视频生成状态

查询任务状态并获取生成的表情包视频。

## 轮询策略

1. 调用[创建任务](/api-reference/video-generation/emoji-video/create-task)接口获取 `task_id`。
2. 每 **15 秒**轮询一次，直到 `task_status` 为 `SUCCEEDED` 或 `FAILED`。
3. 任务成功后，从 `output.video_url` 获取视频。

## 注意事项

- **URL 有效期**：视频 URL 在 **24 小时**后过期，请及时下载。
- **状态流转**：`PENDING` → `RUNNING` → `SUCCEEDED` 或 `FAILED`。`UNKNOWN` 表示任务不存在或已过期。

## OpenAPI

````yaml get /tasks/{task_id}
openapi: 3.0.0
info:
  title: 表情包视频生成 API
  description: 表情包emoji-v1模型可基于人物肖像图片和预设模板ID，生成人脸表情包视频。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: DashScope API
security:
  - BearerAuth: []
paths:
  /tasks/{task_id}:
    get:
      operationId: getEmojiVideoTaskStatus
      summary: 根据任务ID查询结果
      description: 根据任务ID查询视频生成任务的状态和结果。视频生成过程约需数分钟，建议采用轮询机制，并设置合理的查询间隔（如15秒）来获取结果。task_id 有效期为24小时，超时后将无法查询结果。
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
          description: 任务ID。由创建任务接口返回。
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
                  description: 视频URL仅保留24小时，超时后会被自动清除，请及时保存生成的视频。
                  value:
                    request_id: ad225054-6c94-47e5-9356-xxxxxxx
                    output:
                      task_id: b56f509a-3ea9-4cfe-848d-xxxxxxx
                      task_status: SUCCEEDED
                      submit_time: 2025-10-14 11:28:04.372
                      scheduled_time: 2025-10-14 11:28:04.400
                      end_time: 2025-10-14 11:29:03.924
                      video_url: http://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xx.mp4?Expires=xxx
                    usage:
                      video_duration: 2
                      video_ratio: standard
                FAILED:
                  summary: 任务执行失败
                  description: 若任务执行失败，task_status将置为 FAILED，并提供错误码和信息。请参见错误信息进行解决。
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
                    request_id: ad225054-6c94-47e5-9356-xxxxxxx
                    output:
                      task_id: b56f509a-3ea9-4cfe-848d-xxxxxxx
                      task_status: RUNNING
                UNKNOWN:
                  summary: 任务查询过期
                  description: task_id查询有效期为24小时，超时后将无法查询，返回以下报错信息。
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
            # 请将 86ecf553-d340-4e21-xxxxxxxxx 替换为真实的 task_id
            curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/86ecf553-d340-4e21-xxxxxxxxx \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY"
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    EmojiVideoRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称。固定为 emoji-v1。
          enum:
            - emoji-v1
          example: emoji-v1
        input:
          type: object
          required:
            - image_url
            - face_bbox
            - ext_bbox
            - driven_id
          description: 输入的基本信息，如人脸图像、人脸区域、表情包区域等。
          properties:
            image_url:
              type: string
              description: |-
                人脸正面肖像图像的公网 URL。支持 HTTP 或 HTTPS 协议。本地文件可通过上传文件接口获取临时URL。

                图像限制：
                - 图像格式：JPEG、JPG、PNG、BMP、WEBP。
                - 图像分辨率：图像的宽度和高度均在[400, 7000]像素之间。
                - 文件大小：不超过10MB。
                - 此图像必须通过 Emoji 图像检测接口进行检测。
              example: https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250912/uopnly/emoji-%E5%9B%BE%E5%83%8F%E6%A3%80%E6%B5%8B.png
            face_bbox:
              type: array
              items:
                type: integer
              description: 图片中人脸区域坐标，格式为 [x1, y1, x2, y2]，单位为像素，对应左上和右下两个点的坐标。此参数需填入 Emoji 图像检测接口响应中的 output.bbox_face 字段的值。
              example:
                - 212
                - 194
                - 460
                - 441
            ext_bbox:
              type: array
              items:
                type: integer
              description: |-
                动态表情区域坐标，该区域的宽高比约为1:1，格式为 [x1, y1, x2, y2]，单位为像素，对应左上和右下两个点的坐标。此参数需填入 Emoji 图像检测接口响应中的 output.ext_bbox_face 字段的值。

                说明：动态表情区域指的是模型进行视频生成时实际关注的正方形图像区域，它通常比人脸区域稍大，以包含部分背景和肩膀，确保动画效果自然。
              example:
                - 63
                - 30
                - 609
                - 575
            driven_id:
              type: string
              description: 预设模板ID，可选值参见附录表情包模板ID列表。
              enum:
                - mengwa_kaixin
                - mengwa_dengyan
                - mengwa_gandong
                - mengwa_renzhen_1
                - mengwa_jidong
                - mengwa_kun_1
                - mengwa_jiaoxie
                - dagong_kaixin
                - dagong_yangwang
                - dagong_kunhuo
                - dagong_zhuakuang
                - dagong_wunai
                - dagong_weixiao
                - dagong_ganji
                - jingdian_tiaopi
                - jingdian_deyi_1
                - jingdian_qidai
                - jingdian_landuo_1
                - jingdian_xianqi
                - jingdian_lei
              example: mengwa_kaixin
    AsyncTaskSubmitResponse:
      type: object
      description: 异步任务提交响应。请保存 task_id，用于查询任务状态与结果。
      properties:
        output:
          type: object
          description: 任务输出信息。
          properties:
            task_id:
              type: string
              description: 任务ID。查询有效期24小时。
              example: 0385dc79-5ff8-4d82-bcb6-xxxxxx
            task_status:
              type: string
              description: 任务状态。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - CANCELED
                - UNKNOWN
              example: PENDING
        request_id:
          type: string
          description: 请求唯一标识。可用于请求明细溯源和问题排查。
          example: 4909100c-7b5a-9f92-bfe5-xxxxxx
    TaskStatusResponse:
      type: object
      description: 查询任务状态响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识。可用于请求明细溯源和问题排查。
          example: ad225054-6c94-47e5-9356-xxxxxxx
        output:
          type: object
          description: 任务输出信息。
          properties:
            task_id:
              type: string
              description: 任务ID。查询有效期24小时。
              example: b56f509a-3ea9-4cfe-848d-xxxxxxx
            task_status:
              type: string
              description: |-
                任务状态。

                枚举值：
                - PENDING：任务排队中
                - RUNNING：任务处理中
                - SUCCEEDED：任务执行成功
                - FAILED：任务执行失败
                - CANCELED：任务已取消
                - UNKNOWN：任务不存在或状态未知

                轮询过程中的状态流转：
                - PENDING（排队中） → RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。
                - 初次查询状态通常为 PENDING（排队中）或 RUNNING（处理中）。
                - 当状态变为 SUCCEEDED 时，响应中将包含生成的视频URL。
                - 若状态为 FAILED，请检查错误信息并重试。
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
              example: 2025-10-14 11:28:04.372
            scheduled_time:
              type: string
              description: 任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。
              example: 2025-10-14 11:28:04.400
            end_time:
              type: string
              description: 任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。
              example: 2025-10-14 11:29:03.924
            video_url:
              type: string
              description: 视频URL。仅在 task_status 为 SUCCEEDED 时返回。链接有效期24小时，可通过此URL下载视频。视频格式为MP4（H.264 编码）。
              example: http://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xx.mp4?Expires=xxx
            code:
              type: string
              description: 请求失败的错误码。请求成功时不会返回此参数，详情请参见错误信息。
            message:
              type: string
              description: 请求失败的详细信息。请求成功时不会返回此参数，详情请参见错误信息。
        usage:
          type: object
          description: 输出信息统计，只对成功的结果计数。
          properties:
            video_duration:
              type: integer
              description: 生成视频的时长，单位为秒。计费公式：费用 = 视频秒数 × 单价。
              example: 2
            video_ratio:
              type: string
              description: 生成视频的画幅，固定为standard，表示生成1:1画幅的视频。
              example: standard
    DashScopeErrorResponse:
      type: object
      description: DashScope API 错误响应。创建任务失败或查询失败时返回，请参见错误信息进行解决。
      properties:
        request_id:
          type: string
          description: 请求唯一标识。
          example: fb53c4ec-1c12-4fc4-a580-xxxxxx
        code:
          type: string
          description: 错误码。
          example: InvalidApiKey
        message:
          type: string
          description: 错误信息。
          example: Invalid API-key provided.
````

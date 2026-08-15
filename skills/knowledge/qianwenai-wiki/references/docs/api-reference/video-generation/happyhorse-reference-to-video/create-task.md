> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# HappyHorse -- 参考生视频

> 提交 HappyHorse 参考生视频任务

传入多张参考图像，通过文本提示词描述场景，将图像中的主体角色融合生成一段流畅的视频，最长 15 秒，支持 1080P 分辨率。在 prompt 中使用 `character1`、`character2` 等标识指代 `media` 数组中对应位置的参考图像。

## OpenAPI

````yaml post /services/aigc/video-generation/video-synthesis
openapi: 3.1.0
info:
  title: HappyHorse 参考生视频 API
  description: 使用 HappyHorse 模型传入多张参考图像生成视频。异步提交任务后，通过 `GET /tasks/{task_id}` 轮询获取结果。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 华北2（北京）
security:
  - BearerAuth: []
paths:
  /services/aigc/video-generation/video-synthesis:
    post:
      operationId: createHappyHorseRefToVideo
      summary: 提交参考生视频任务
      description: 提交参考生视频任务，返回 `task_id` 用于轮询查询。
      parameters:
        - name: X-DashScope-Async
          in: header
          required: true
          description: 必须设置为 `enable`，表示异步提交任务。
          schema:
            type: string
            enum:
              - enable
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/HappyHorseRefToVideoRequest"
      responses:
        "200":
          description: 任务提交成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/AsyncTaskSubmitResponse"
        "400":
          description: 请求参数无效
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
      x-codeSamples:
        - lang: curl
          label: cURL - 参考生视频（多图像）
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
              "model": "happyhorse-1.1-r2v",
              "input": {
                "prompt": "[Image 1]中身着红色旗袍的女性，镜头先以侧面中景勾勒旗袍修身剪裁与S型曲线，随即切换至低角度仰拍，捕捉她轻抬玉手展开[Image 2]中的折扇的同时，[Image 3]中的流苏耳坠随头部转动轻盈摆动的细节，最后推近至面部特写，定格在她指尖轻点扇骨、眼波流转间的含蓄风情，多视角全方位展现东方韵味。",
                "media": [
                  {
                    "type": "reference_image",
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260424/mvzfud/hh-v2v-girl.jpg"
                  },
                  {
                    "type": "reference_image",
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260424/fvuihk/hh-v2v2-folding-fan.jpg"
                  },
                  {
                    "type": "reference_image",
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260424/imerii/hh-v2v-earrings.jpg"
                  }
                ]
              },
              "parameters": {
                "resolution": "720P",
                "ratio": "16:9",
                "duration": 5
              }
            }'
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    HappyHorseRefToVideoRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称。可选值：`happyhorse-1.1-r2v`、`happyhorse-1.0-r2v`。
          enum:
            - happyhorse-1.1-r2v
            - happyhorse-1.0-r2v
          example: happyhorse-1.1-r2v
        input:
          type: object
          required:
            - prompt
            - media
          description: 输入的基本信息，包括参考图像和提示词。
          properties:
            prompt:
              type: string
              description: 文本提示词，用来描述生成视频中期望包含的元素和视觉特点。在 prompt 中通过 `[Image 1]`、`[Image 2]` 等标识指代 `media` 数组中对应位置的参考图像，顺序与 `media` 数组顺序一致。使用时需要指明参考图中的具体对象，例如"[Image 1]中身着红色旗袍的女性"。支持任何语言输入，长度不超过5000个非中文字符或2500个中文字符，超过部分会自动截断。
              example: "[Image 1]中身着红色旗袍的女性，优雅站立。"
            media:
              type: array
              description: 媒体素材列表（1-9张参考图像）。数组中的第 1 个 `reference_image` 对应 `[Image 1]`，第 2 个对应 `[Image 2]`，以此类推。
              items:
                type: object
                required:
                  - type
                  - url
                properties:
                  type:
                    type: string
                    description: 媒体素材类型。固定值：`reference_image`（参考图像）。
                    enum:
                      - reference_image
                  url:
                    type: string
                    format: uri
                    description: |-
                      参考图像 URL 或 Base64 编码数据。

                      **图像限制**：格式：JPEG、JPG、PNG、WEBP。分辨率：短边不低于 400 像素，推荐 720P 以上清晰图。文件大小：不超过 20 MB。

                      **支持的输入格式**：
                      - 公网 URL：支持 HTTP 或 HTTPS 协议。
                      - Base64 编码：格式为 `data:{MIME_type};base64,{base64_data}`。
              minItems: 1
              maxItems: 9
        parameters:
          $ref: "#/components/schemas/HappyHorseRefToVideoParameters"
    HappyHorseRefToVideoParameters:
      type: object
      description: 视频生成参数。
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
          description: 生成视频的宽高比。
          enum:
            - 16:9
            - 9:16
            - 1:1
            - 4:3
            - 3:4
            - 4:5
            - 5:4
            - 9:21
            - 21:9
          default: 16:9
        duration:
          type: integer
          description: 生成视频的时长，单位为秒。取值范围：3~15 之间的整数。
          minimum: 3
          maximum: 15
          default: 5
        watermark:
          type: boolean
          description: 是否在生成的视频上添加水印标识。水印位于视频右下角，文案固定为"Happy Horse"。`true`（默认）：添加水印。`false`：不添加水印。
          default: true
        seed:
          type: integer
          description: 随机数种子。相同的种子和参数会生成相似（但不完全相同）的结果。
          minimum: 0
          maximum: 2147483647
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
              description: 任务 ID，用于后续轮询查询任务状态。配合 `GET /tasks/{task_id}` 使用。
              example: 0385dc79-5ff8-4d82-bcb6-xxxxxx
            task_status:
              type: string
              description: 初始任务状态，通常为 `PENDING`。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
    HappyHorseR2VTaskStatusResponse:
      type: object
      description: HappyHorse 参考生视频任务状态响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识。联系技术支持时请提供此 ID。
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID。提交后 24 小时内可查询。
            task_status:
              type: string
              description: 任务状态流转：`PENDING` -> `RUNNING` -> `SUCCEEDED` 或 `FAILED`。手动取消为 `CANCELED`，过期为 `UNKNOWN`。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - CANCELED
                - UNKNOWN
            submit_time:
              type: string
              description: 任务提交时间（UTC+8，`YYYY-MM-DD HH:mm:ss.SSS`）。
            scheduled_time:
              type: string
              description: 任务开始执行时间（UTC+8，`YYYY-MM-DD HH:mm:ss.SSS`）。
            end_time:
              type: string
              description: 任务结束时间（UTC+8）。仅在 `SUCCEEDED` 或 `FAILED` 时返回。
            orig_prompt:
              type: string
              description: 原始提示词文本。
            video_url:
              type: string
              format: uri
              description: 生成视频的 URL（MP4，H.264 编码）。仅在 `task_status` 为 `SUCCEEDED` 时返回。**链接有效期 24 小时**，请及时下载。
            code:
              type: string
              description: 错误码。仅在 `task_status` 为 `FAILED` 时返回。
            message:
              type: string
              description: 错误信息。仅在 `task_status` 为 `FAILED` 时返回。
        usage:
          type: object
          description: 资源消耗统计。仅在 `task_status` 为 `SUCCEEDED` 时返回。
          properties:
            duration:
              type: number
              description: 总的视频时长，用于计费，单位为秒。
            input_video_duration:
              type: integer
              description: 输入视频时长，单位秒。参考生视频固定为 0。
            output_video_duration:
              type: integer
              description: 输出视频时长，单位秒。
            video_count:
              type: integer
              description: 输出视频数量。固定为 1。
            ratio:
              type: string
              description: 生成视频的宽高比。
            SR:
              type: integer
              description: 输出视频的分辨率档位（如 720 表示 720P，1080 表示 1080P）。
    DashScopeErrorResponse:
      type: object
      description: DashScope API 错误响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识，用于链路追踪和问题排查。
        code:
          type: string
          description: 错误码（如 `InvalidParameter`、`Throttling`、`Unauthorized`）。
          example: InvalidParameter
        message:
          type: string
          description: 错误描述信息。
          example: Invalid model name
````

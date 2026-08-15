> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Wan 2.6 — 创建任务

> 提交参考视频生成任务

通过多模态输入（文本、图像或视频），生成自然逼真的表演视频。可将人物或物体作为主角。

- **基础能力**：支持设置时长（2–10 秒）、分辨率（720P/1080P）和水印。
- **角色刻画**：从参考图像或视频中复刻外观。视频参考还可复刻音色。支持单人或多人表演。
- **多镜头叙事**：智能多镜头调度，在对话和互动场景中保持角色一致性。

## OpenAPI

````yaml post /services/aigc/video-generation/video-synthesis
openapi: 3.1.0
info:
  title: Wan 参考驱动视频生成 API
  description: Wan 参考驱动视频生成 API，支持通过参考图片或视频结合多模态输入（文本、图片、视频）生成表演视频，覆盖单人或多人互动、多镜头叙事及音视频同步等场景。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 千问AI平台
security:
  - BearerAuth: []
paths:
  /services/aigc/video-generation/video-synthesis:
    post:
      operationId: createRefToVideo
      summary: 创建参考驱动视频生成任务
      description: 创建一个参考驱动视频生成任务。
      parameters:
        - name: X-DashScope-Async
          in: header
          required: true
          description: 固定填写 `enable`，以创建异步任务。
          schema:
            type: string
            enum:
              - enable
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/RefToVideoRequest"
      responses:
        "200":
          description: 任务创建成功。
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
          label: 多角色（提交任务）
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
              "model": "wan2.6-r2v-flash",
              "input": {
                "prompt": "Character2 sits on a chair by the window, holding character3, and plays a soothing American country folk song next to character4. Character1 says to Character2: \"that sounds great\"",
                "reference_urls": [
                  "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260205/aacgyk/wan-r2v-role1.mp4",
                  "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260205/mmizqq/wan-r2v-role2.mp4",
                  "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qpzxps/wan-r2v-object4.png",
                  "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/wfjikw/wan-r2v-backgroud5.png"
                ]
              },
              "parameters": {
                "size": "1280*720",
                "duration": 10,
                "audio": true,
                "shot_type": "multi",
                "watermark": true
              }
            }'
        - lang: curl
          label: 单角色（提交任务）
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
              "model": "wan2.6-r2v-flash",
              "input": {
                "prompt": "Create a festive holiday unboxing experience. Shot 1 [0-2s]: Character1 sits by a beautifully decorated Christmas tree with twinkling lights, holding a wrapped gift box with elegant red and gold wrapping. Shot 2 [2-4s]: Close-up as Character1 carefully unwraps the gift, revealing premium skincare products inside. Shot 3 [4-6s]: Character1 applies the product with delight, saying: \"This holiday glow is exactly what I wanted!\" Shot 4 [6-10s]: Character1 admires their radiant skin in a handheld mirror, surrounded by festive decorations, ending with a warm smile to camera.",
                "reference_urls": ["https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260205/mjgmzx/wan-r2v-role-4.mp4"]
              },
              "parameters": {
                "size": "1280*720",
                "duration": 10,
                "shot_type": "multi",
                "watermark": true
              }
            }'
        - lang: curl
          label: 静音视频（提交任务）
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
              "model": "wan2.6-r2v-flash",
              "input": {
                "prompt": "character1 drinks bubble tea while dancing spontaneously to the music.",
                "reference_urls": ["https://cdn.wanx.aliyuncs.com/static/demo-wan26/vace.mp4"]
              },
              "parameters": {
                "size": "1280*720",
                "duration": 5,
                "shot_type": "multi",
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
    RefToVideoRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称。
          enum:
            - wan2.6-r2v-flash
            - wan2.6-r2v
          example: wan2.6-r2v-flash
        input:
          $ref: "#/components/schemas/RefToVideoInput"
        parameters:
          $ref: "#/components/schemas/RefToVideoParameters"
    RefToVideoInput:
      type: object
      required:
        - prompt
        - reference_urls
      description: 参考驱动视频生成的输入数据。
      properties:
        prompt:
          type: string
          description: 描述目标视频内容的文本提示词。使用 `character1`、`character2` 等标识符，按顺序引用 `reference_urls` 中的参考角色，每个参考资源只能包含单个角色。
          example: 'Character1 says to Character2: "that sounds great"'
        reference_urls:
          type: array
          description: 参考图片或视频的 URL 列表，最多 5 个（最多 5 张图片，最多 3 个视频）。每个参考资源只能包含单个角色，顺序决定角色标识符（`character1`、`character2` 等）。
          items:
            type: string
            format: uri
          minItems: 1
          maxItems: 5
          example:
            - https://example.com/person1.mp4
            - https://example.com/person2.mp4
            - https://example.com/object.png
    RefToVideoParameters:
      type: object
      description: 参考驱动视频生成的生成参数。
      properties:
        size:
          type: string
          description: 输出分辨率，格式为 `宽*高`，决定视频画面比例（例如 `1280*720` 对应 16:9，`720*1280` 对应 9:16）。
          enum:
            - 1280*720
            - 720*1280
            - 960*960
            - 1920*1080
            - 1080*1920
          example: 1280*720
        duration:
          type: integer
          description: 视频时长，单位为秒，两个模型均支持 2 到 10 的整数值。
          minimum: 2
          maximum: 10
          example: 10
        audio:
          type: boolean
          description: 是否在视频中生成音频。`true`（默认）：生成带音频的视频；`false`：生成静音视频。静音视频仅 `wan2.6-r2v-flash` 支持。
          default: true
        shot_type:
          type: string
          description: 镜头模式。`multi`：多镜头切换，通过自然对话和场景转换增强表现力；`single`：固定单镜头视角。
          enum:
            - multi
            - single
          example: multi
        watermark:
          type: boolean
          description: 为输出视频添加水印。
          default: false
    AsyncTaskSubmitResponse:
      type: object
      description: 异步任务创建成功后的响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识符。
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务标识符，可通过 `GET /tasks/{task_id}` 轮询任务结果。
            task_status:
              type: string
              description: 任务初始状态，通常为 `PENDING`。
              enum:
                - PENDING
    TaskStatusResponse:
      type: object
      description: 包含参考驱动视频任务当前状态和结果的响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识符。
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务标识符。
            task_status:
              type: string
              description: 任务当前状态。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
            video_url:
              type: string
              format: uri
              description: 生成的视频 URL，仅在 `task_status` 为 `SUCCEEDED` 时出现。有效期 24 小时，请及时下载。
            code:
              type: string
              description: 错误码，仅在 `task_status` 为 `FAILED` 时出现。
            message:
              type: string
              description: 错误信息，仅在 `task_status` 为 `FAILED` 时出现。
        usage:
          type: object
          description: 用量统计（仅在任务成功时出现）。
          properties:
            video_count:
              type: integer
              description: 生成的视频数量。
            video_duration:
              type: integer
              description: 生成视频的时长，单位为秒。
    DashScopeErrorResponse:
      type: object
      description: DashScope API 错误响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识符。
        code:
          type: string
          description: 错误码（例如 `InvalidParameter`、`Throttling`、`Unauthorized`）。
          example: InvalidParameter
        message:
          type: string
          description: 可读的错误信息。
          example: "Invalid parameter: size"
````

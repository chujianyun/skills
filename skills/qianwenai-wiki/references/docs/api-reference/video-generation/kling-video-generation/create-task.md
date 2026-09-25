> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 可灵视频生成 — 创建任务

> 提交可灵视频生成异步任务

可灵视频生成模型支持文本、图片和视频素材输入，可生成最长 15 秒、最高 1080P 分辨率的视频。

- **文生视频**：输入文字提示词生成视频，支持智能分镜（由模型自动规划多镜头叙事）和自定义分镜。
- **图生视频（首帧）**：以图片作为视频首帧驱动视频生成。
- **图生视频（首尾帧）**：同时指定首帧和尾帧，模型生成中间过渡内容。
- **参考生视频**：以参考图像、视频素材为主体，结合提示词生成新视频，支持多主体组合。

<Note>
  所有视频生成接口均为异步接口。提交任务后，使用返回的 `task_id` 轮询[查询接口](/api-reference/video-generation/kling-video-generation/query-result)获取结果。
</Note>

## OpenAPI

````yaml post /services/aigc/video-generation/video-synthesis
openapi: 3.1.0
info:
  title: 可灵视频生成 API
  version: 1.0.0
  description: 可灵（Kling）视频生成异步 API，支持文生视频、图生视频（首帧/首尾帧）、参考生视频等多种模式。
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 千问AI平台
security:
  - BearerAuth: []
paths:
  /services/aigc/video-generation/video-synthesis:
    post:
      operationId: createKlingVideoTask
      summary: 提交可灵视频生成任务
      description: 提交可灵视频生成异步任务。任务提交后返回 `task_id`，通过查询接口轮询任务状态。
      parameters:
        - name: X-DashScope-Async
          in: header
          required: true
          schema:
            type: string
            enum:
              - enable
          description: 固定填 `enable`，启用异步模式。
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/KlingVideoRequest"
      responses:
        "200":
          description: 任务提交成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/AsyncTaskSubmitResponse"
              example:
                output:
                  task_status: PENDING
                  task_id: 0385dc79-5ff8-4d82-bcb6-xxxxxx
                request_id: 4909100c-7b5a-9f92-bfe5-xxxxxx
        4XX:
          description: 请求错误
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
              example:
                code: InvalidApiKey
                message: No API-key provided.
                request_id: 7438d53d-6eb8-4596-8835-xxxxxx
      x-codeSamples:
        - lang: bash
          label: 文生视频
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
                -H 'X-DashScope-Async: enable' \
                -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
                -H 'Content-Type: application/json' \
                -d '{
                "model": "kling/kling-v3-video-generation",
                "input": {
                    "prompt": "一只小猫在月光下奔跑"
                },
                "parameters": {
                    "mode": "std",
                    "aspect_ratio": "16:9",
                    "duration": 5,
                    "audio": false,
                    "watermark": true
                }
            }'
        - lang: bash
          label: 文生视频（智能分镜）
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
                -H 'X-DashScope-Async: enable' \
                -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
                -H 'Content-Type: application/json' \
                -d '{
                "model": "kling/kling-v3-video-generation",
                "input": {
                    "prompt": "",
                    "multi_shot": true,
                    "shot_type": "customize",
                    "multi_prompt": [
                        {"index": 1, "prompt": "雾岭镇比地图上更小，山雾像棉絮一样堵在街口。邮局背后果然有三棵槐树，第三棵树根旁的泥土被人动过。", "duration": 5},
                        {"index": 2, "prompt": "林澈蹲下挖出一个铁盒，里面除了一把生锈的钥匙，还有一盘老旧的录音带。录音机是邮局借的，按下播放键时，父亲的声音从沙沙杂音里爬出来："如果你听到这段话，说明你已经走到我走过的路上了。"", "duration": 5}
                    ],
                    "media": [],
                    "element_list": []
                },
                "parameters": {
                    "mode": "pro",
                    "duration": 10,
                    "audio": true,
                    "aspect_ratio": "9:16",
                    "watermark": true
                }
            }'
        - lang: bash
          label: 图生视频（首帧）
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
                -H 'X-DashScope-Async: enable' \
                -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
                -H 'Content-Type: application/json' \
                -d '{
                "model": "kling/kling-v3-omni-video-generation",
                "input": {
                    "prompt": "让图片中的人物动起来，头发被微风吹动",
                    "media": [{"type": "first_frame", "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260121/zlpocv/wan-i2v-haigui.webp"}]
                },
                "parameters": {
                    "mode": "std",
                    "duration": 5,
                    "audio": false,
                    "watermark": true
                }
            }'
        - lang: bash
          label: 图生视频（首尾帧）
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
                -H 'X-DashScope-Async: enable' \
                -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
                -H 'Content-Type: application/json' \
                -d '{
                "model": "kling/kling-v3-omni-video-generation",
                "input": {
                    "prompt": "写实风格，一只黑色小猫好奇地看向天空，镜头从平视逐渐上升，最后俯拍它的好奇的眼神。",
                    "media": [
                        {"type": "first_frame", "url": "https://wanx.alicdn.com/material/20250318/first_frame.png"},
                        {"type": "last_frame", "url": "https://wanx.alicdn.com/material/20250318/last_frame.png"}
                    ]
                },
                "parameters": {
                    "mode": "std",
                    "duration": 5,
                    "audio": false,
                    "watermark": true
                }
            }'
        - lang: bash
          label: 参考生视频（视频+图像）
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
                -H 'X-DashScope-Async: enable' \
                -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
                -H 'Content-Type: application/json' \
                -d '{
                "model": "kling/kling-v3-omni-video-generation",
                "input": {
                    "prompt": "<<<element_1>>>背景，<<<image_2>>>和<<<image_1>>>握手交谈，<<<video_1>>>人物穿着黑色风衣的侦探站在公寓楼顶，手持望远镜观察街道",
                    "multi_shot": false,
                    "shot_type": "intelligence",
                    "multi_prompt": [],
                    "media": [
                        {"url": "https://p2-kling.klingai.com/kcdn/cdn-kcdn112452/kling-qa-test/lip_sync_5s.mp4", "type": "base", "keep_original_sound": "yes"},
                        {"type": "refer", "url": "https://p2-kling.klingai.com/kcdn/cdn-kcdn112452/kling-qa-test/zem_test/yangmi01.jpg"},
                        {"type": "refer", "url": "https://p2-kling.klingai.com/kcdn/cdn-kcdn112452/kling-qa-test/human_2.JPG"}
                    ],
                    "element_list": [{"element_id": 171}]
                },
                "parameters": {
                    "mode": "pro",
                    "duration": "10",
                    "audio": false,
                    "aspect_ratio": "1:1",
                    "watermark": true
                }
            }'
components:
  schemas:
    KlingVideoRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          enum:
            - kling/kling-v3-omni-video-generation
            - kling/kling-v3-video-generation
          description: 模型 ID。`kling-v3-omni-video-generation` 支持图生视频（首帧/首尾帧）、参考生视频等所有模式；`kling-v3-video-generation` 支持文生视频和多镜头叙事。
        input:
          type: object
          required: []
          description: 任务输入参数。
          properties:
            prompt:
              type: string
              maxLength: 2500
              description: 视频描述提示词，最多 2500 个字符。使用 omni 模型的参考生视频模式时，可通过 `<<<element_1>>>`、`<<<image_1>>>`、`<<<video_1>>>` 语法引用 `element_list` 和 `media` 中的素材。`shot_type=intelligence` 时必填；`shot_type=customize` 时不使用本字段。
            media:
              type: array
              description: 输入媒体列表。kling-v3-video-generation 仅支持 `first_frame`、`last_frame`；kling-v3-omni-video-generation 额外支持 `refer`、`base`、`feature`。
              items:
                type: object
                required:
                  - type
                  - url
                properties:
                  type:
                    type: string
                    enum:
                      - first_frame
                      - last_frame
                      - refer
                      - base
                      - feature
                    description: 媒体类型。`first_frame`：图生视频首帧；`last_frame`：图生视频尾帧；`refer`：参考图像；`base`：参考视频（omni 模型）；`feature`：特征参考视频（omni 模型）。
                  url:
                    type: string
                    format: uri
                    description: 媒体文件的公网 URL。
                  keep_original_sound:
                    type: string
                    enum:
                      - yes
                      - no
                    default: no
                    description: 是否保留原视频音频，仅 omni 模型且 `type` 为 `base` 或 `feature` 时有效。`yes`：保留；`no`（默认）：不保留。
            multi_shot:
              type: boolean
              default: false
              description: 是否启用多镜头模式。启用时须指定 `shot_type`。
            shot_type:
              type: string
              enum:
                - intelligence
                - customize
              description: 多镜头分镜策略，`multi_shot=true` 时必填。`intelligence`：由模型自动规划分镜；`customize`：按 `multi_prompt` 自定义分镜。
            multi_prompt:
              type: array
              description: 自定义多镜头提示词列表，`shot_type=customize` 时必填。最多 6 个镜头，index 从 1 开始。
              maxItems: 6
              items:
                type: object
                required:
                  - index
                  - prompt
                  - duration
                properties:
                  index:
                    type: integer
                    minimum: 1
                    maximum: 6
                    description: 镜头编号，从 1 开始。
                  prompt:
                    type: string
                    maxLength: 512
                    description: 该镜头的描述提示词，最多 512 个字符。
                  duration:
                    type: integer
                    minimum: 1
                    description: 该镜头时长（秒），须 ≥ 1 且 ≤ `parameters.duration`。
            element_list:
              type: array
              description: 元素列表，用于参考生视频模式。
              items:
                type: object
                required:
                  - element_id
                properties:
                  element_id:
                    type: integer
                    description: 元素 ID。
        parameters:
          type: object
          description: 生成参数。
          properties:
            mode:
              type: string
              enum:
                - pro
                - std
                - 4k
              default: pro
              description: 生成模式。`pro`（默认）：专业模式，输出 1080P；`std`：标准模式，输出 720P；`4k`：4K模式，输出视频分辨率为4K。
            aspect_ratio:
              type: string
              enum:
                - 16:9
                - 9:16
                - 1:1
              default: 16:9
              description: 视频宽高比。文生视频和参考生视频（refer/feature）模式必填；图生视频（首帧/首尾帧）模式自动继承输入图像比例。
            duration:
              type: integer
              minimum: 3
              maximum: 15
              default: 5
              description: 视频时长（秒），默认 5 秒，范围 3–15。使用 omni 模型且传入视频时：`type=feature`：取值为[3, 10]之间的整数，默认值为5。`type=base`：输出视频时长与传入视频时长相同，此时当前参数无效。按输入视频时长四舍五入取整计量计费。
            audio:
              type: boolean
              default: false
              description: 是否自动生成配音，默认 false。注意：当传入视频（`type` 为 `base` 或 `feature`）时，`audio` 只能设置为 `false`。
            watermark:
              type: boolean
              default: false
              description: 是否同时生成含水印的视频。水印位于视频右下角，文案固定为"可灵AI"。设置为 true 时，响应中将额外返回 `watermark_video_url` 字段。默认 false。
    AsyncTaskSubmitResponse:
      type: object
      properties:
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID，用于轮询任务状态。
            task_status:
              type: string
              enum:
                - PENDING
              description: 任务初始状态，固定为 `PENDING`。
        request_id:
          type: string
          description: 请求唯一标识符。
    KlingTaskQueryResponse:
      type: object
      properties:
        request_id:
          type: string
          description: 请求唯一标识符。
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID。
            task_status:
              type: string
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - UNKNOWN
              description: 任务状态。`PENDING`：等待中；`RUNNING`：生成中；`SUCCEEDED`：成功；`FAILED`：失败；`UNKNOWN`：task_id 查询有效期（24 小时）已过期。
            submit_time:
              type: string
              description: 任务提交时间。
            scheduled_time:
              type: string
              description: 任务调度时间。
            end_time:
              type: string
              description: 任务结束时间。
            video_url:
              type: string
              format: uri
              description: 生成的视频 URL，任务成功后返回，有效期 **30 天**。
            watermark_video_url:
              type: string
              format: uri
              description: 带水印视频 URL，任务成功且 `watermark=true` 时返回，有效期 **30 天**。
            orig_prompt:
              type: string
              description: 实际使用的提示词（经模型改写后）。
            code:
              type: string
              description: 错误码，任务失败时返回。
            message:
              type: string
              description: 错误信息，任务失败时返回。
        usage:
          type: object
          description: 用量统计，任务成功后返回。
          properties:
            duration:
              type: number
              description: 视频时长（秒）。
            size:
              type: string
              description: 视频分辨率，格式如 `1280*720`。
            fps:
              type: integer
              description: 帧率（FPS）。
            video_count:
              type: integer
              description: 生成的视频数量。
            audio:
              type: boolean
              description: 是否包含音频。
            SR:
              type: string
              description: 超分辨率信息。
    DashScopeErrorResponse:
      type: object
      properties:
        code:
          type: string
          description: 错误码。
        message:
          type: string
          description: 错误信息。
        request_id:
          type: string
          description: 请求唯一标识符。
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
````

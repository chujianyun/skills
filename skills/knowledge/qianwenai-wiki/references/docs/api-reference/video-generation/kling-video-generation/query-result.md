> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 可灵视频生成 — 查询结果

> 查询可灵视频生成任务状态并获取视频

查询任务状态并获取生成的视频。

## 轮询策略

1. 通过[提交任务](/api-reference/video-generation/kling-video-generation/create-task)接口提交任务，保存返回的 `task_id`。
2. 每 **15 秒**轮询一次，直到 `task_status` 变为 `SUCCEEDED` 或 `FAILED`。
3. 任务成功后，从 `video_url` 下载视频。

## 注意事项

- **视频 URL 有效期**：`video_url` 和 `watermark_video_url` 在 **30 天**后过期，请及时下载。
- **task\_id 查询有效期**：`task_id` 仅在提交后 **24 小时**内有效。超出后查询返回 `task_status: UNKNOWN`。
- **查询频率限制**：接口 RPS 限制为 20，建议以 15 秒为间隔轮询。
- **状态流转**：`PENDING` → `RUNNING` → `SUCCEEDED` / `FAILED`。

## OpenAPI

````yaml get /tasks/{task_id}
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
  /tasks/{task_id}:
    get:
      operationId: getKlingVideoTask
      summary: 查询可灵视频生成任务状态
      description: 查询视频生成任务状态，任务成功后返回视频 URL。
      parameters:
        - name: task_id
          in: path
          required: true
          schema:
            type: string
          description: 任务 ID，由提交任务接口返回。
      responses:
        "200":
          description: 查询成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/KlingTaskQueryResponse"
              examples:
                SUCCEEDED:
                  summary: 任务成功
                  value:
                    request_id: 340f0d7d-bf7e-4c8f-9c03-xxxxxx
                    output:
                      task_id: 24f5c51e-d67b-44dc-9acb-xxxxxx
                      task_status: SUCCEEDED
                      submit_time: 2026-03-27 21:30:32.575
                      scheduled_time: 2026-03-27 21:30:32.603
                      end_time: 2026-03-27 21:31:09.177
                      video_url: https://v4-fdl.kechuangai.com/ksc2/xxx.mp4?xxxx
                      watermark_video_url: https://v2-fdl.kechuangai.com/ksc2/xxx.mp4?xxxx
                    usage:
                      duration: 5
                      size: 1280*720
                      fps: 24
                      video_count: 1
                      audio: false
                      SR: "720"
                FAILED:
                  summary: 任务失败
                  value:
                    request_id: e5d70b02-ebd3-98ce-9fe8-759d7d7b107d
                    output:
                      task_id: 86ecf553-d340-4e21-af6e-a0c6a421c010
                      task_status: FAILED
                      code: InvalidParameter
                      message: The parameter is invalid xxxxxx
                RUNNING:
                  summary: 任务处理中
                  value:
                    request_id: 7574ee8f-38a3-4b1e-9280-xxxxxx
                    output:
                      task_id: a8532587-fa8c-4ef8-82be-xxxxxx
                      task_status: RUNNING
                UNKNOWN:
                  summary: task_id 已超过24小时查询期
                  value:
                    request_id: a4de7c32-7057-9f82-8581-xxxxxx
                    output:
                      task_id: 502a00b1-19d9-4839-a82f-xxxxxx
                      task_status: UNKNOWN
      x-codeSamples:
        - lang: bash
          label: 查询任务状态
          source: |-
            curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id} \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY"
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

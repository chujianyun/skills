> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 创意文字纹理 — 查询结果

> 查询创意文字纹理生成任务的状态和结果

查询任务状态并获取生成的文字纹理图片。

## 轮询策略

1. 通过[提交创意文字纹理任务](/api-reference/image-generation/wordart-texture/create-task)接口提交任务，获取 `task_id`。
2. 每 **5 秒**轮询一次，直到 `task_status` 为 `SUCCEEDED` 或 `FAILED`。
3. 任务成功后，从 `results` 数组中获取各图片的 `url`。

## 注意事项

- **URL 有效期**：生成的图片 URL 有效期为 **24 小时**，请及时下载。
- **任务状态流转**：`PENDING` → `RUNNING` → `SUCCEEDED`、`FAILED` 或 `UNKNOWN`。
- **任务 ID 有效期**：`task_id` 有效期为 24 小时，过期后无法查询状态和结果。

## OpenAPI

````yaml get /tasks/{task_id}
openapi: 3.1.0
info:
  title: WordArt Texture Generation API
  version: 1.0.0
  description: 创意文字纹理生成 API
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 千问AI平台
security:
  - BearerAuth: []
paths:
  /tasks/{task_id}:
    get:
      summary: 查询文字纹理生成结果
      operationId: getWordArtTextureTaskResult
      parameters:
        - name: task_id
          in: path
          required: true
          schema:
            type: string
          description: 任务 ID，由[生成文字纹理](/api-reference/image-generation/wordart-texture/create-task)接口返回。
      responses:
        "200":
          description: 任务状态查询结果
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/TaskStatusResponse"
              examples:
                SUCCEEDED:
                  summary: 任务成功
                  value:
                    request_id: 7574ee8f-38a3-4b1e-9280-11c33ab46e51
                    output:
                      task_id: a8532587-fa8c-4ef8-82be-0c46b17950d1
                      task_status: SUCCEEDED
                      submit_time: 2025-08-15 10:46:20.054
                      scheduled_time: 2025-08-15 10:46:20.087
                      end_time: 2025-08-15 10:46:27.768
                      results:
                        - url: https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx/1.jpg
                        - url: https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx/2.jpg
                        - url: https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx/3.jpg
                        - url: https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx/4.jpg
                    usage:
                      image_count: 4
                FAILED:
                  summary: 任务失败
                  value:
                    request_id: 7574ee8f-38a3-4b1e-9280-11c33ab46e51
                    output:
                      task_id: a8532587-fa8c-4ef8-82be-0c46b17950d1
                      task_status: FAILED
                      code: InvalidParameter
                      message: The request is missing required parameters or the parameters are out of the specified range
                RUNNING:
                  summary: 任务运行中
                  value:
                    request_id: e5d70b02-ebd3-98ce-9fe8-759d7d7b107d
                    output:
                      task_id: 86ecf553-d340-4e21-af6e-a0c6a421c010
                      task_status: RUNNING
                      submit_time: 2025-08-15 10:46:20.054
                      scheduled_time: 2025-08-15 10:46:20.087
                      task_metrics:
                        TOTAL: 2
                        SUCCEEDED: 1
                        FAILED: 0
                PENDING:
                  summary: 任务排队中
                  value:
                    request_id: 7574ee8f-38a3-4b1e-9280-11c33ab46e51
                    output:
                      task_id: a8532587-fa8c-4ef8-82be-0c46b17950d1
                      task_status: PENDING
      x-codeSamples:
        - lang: curl
          label: 查询任务结果
          source: |-
            curl -X GET \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    WordArtTextureRequest:
      type: object
      required:
        - model
        - input
        - parameters
      properties:
        model:
          type: string
          enum:
            - wordart-texture
          description: 模型名称。
        input:
          type: object
          required:
            - prompt
          description: 输入参数。
          properties:
            image:
              type: object
              description: 图片输入模式，与 `text` 互斥。传入黑底白字的文字图片。
              properties:
                image_url:
                  type: string
                  description: 文字图片 URL。要求：黑底白字、小于 5M、支持 jpg/png/jpeg/bmp、宽高比不超过 2:1、长边不超过 2048 像素。
              required:
                - image_url
            text:
              type: object
              description: 文字输入模式，与 `image` 互斥。直接传入文字内容。
              properties:
                text_content:
                  type: string
                  maxLength: 6
                  description: 文字内容，最多 6 个字符，支持中文、阿拉伯数字和英文。
                ttf_url:
                  type: string
                  description: 自定义字体文件 URL（TTF 格式，小于 30M），与 `font_name` 互斥。
                font_name:
                  type: string
                  enum:
                    - dongfangdakai
                    - puhuiti_m
                    - shuheiti
                    - jinbuti
                    - kuheiti
                    - kuaileti
                    - wenyiti
                    - logoti
                    - cangeryuyangti_m
                    - siyuansongti_b
                    - siyuanheiti_m
                    - fangzhengkaiti
                  default: dongfangdakai
                  description: 预设字体名称，与 `ttf_url` 互斥。默认为 `dongfangdakai`。
                output_image_ratio:
                  type: string
                  enum:
                    - 1:1
                    - 16:9
                    - 9:16
                  default: 1:1
                  description: 输出图片宽高比，默认 `1:1`。
              required:
                - text_content
            prompt:
              type: string
              maxLength: 200
              description: 纹理描述文本，最多 200 个字符，不能为空字符串。
            texture_style:
              type: string
              enum:
                - material
                - scene
                - lighting
                - waterfall
                - snow_plateau
                - forest
                - sky
                - chinese_building
                - cartoon
                - lego
                - flower
                - acrylic
                - marble
                - felt
                - oil_painting
                - watercolor_painting
                - chinese_painting
                - claborate_style_painting
                - city_night
                - mountain_lake
                - autumn_leaves
                - green_dragon
                - red_dragon
              default: material
              description: 纹理风格。自定义风格：`material`（立体材质）、`scene`（场景融合）、`lighting`（光影特效）。预设风格：`waterfall`、`snow_plateau`、`forest`、`sky`、`chinese_building`、`cartoon`、`lego`、`flower`、`acrylic`、`marble`、`felt`、`oil_painting`、`watercolor_painting`、`chinese_painting`、`claborate_style_painting`、`city_night`、`mountain_lake`、`autumn_leaves`、`green_dragon`、`red_dragon`。
            ref_image_url:
              type: string
              description: 参考风格图片 URL。传入后将覆盖 `texture_style` 设置。
        parameters:
          type: object
          description: 模型参数。
          properties:
            image_short_size:
              type: integer
              minimum: 512
              maximum: 1024
              default: 704
              description: 生成图片短边长度，取值范围 [512, 1024]，必须为 64 的倍数，默认 704。
            n:
              type: integer
              minimum: 1
              maximum: 4
              default: 1
              description: 生成图片数量，取值范围 1~4，默认 1。
            alpha_channel:
              type: boolean
              default: false
              description: 是否生成透明背景图片，默认 false。
    AsyncTaskSubmitResponse:
      type: object
      properties:
        request_id:
          type: string
          description: 请求唯一标识。
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID，用于查询任务状态和结果。
            task_status:
              type: string
              enum:
                - PENDING
              description: 任务状态。
    TaskStatusResponse:
      type: object
      properties:
        request_id:
          type: string
          description: 请求唯一标识。
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
              description: 当前任务状态。状态流转：PENDING → RUNNING → SUCCEEDED 或 FAILED。UNKNOWN 表示任务不存在或查询已超过 24 小时。
            submit_time:
              type: string
              description: 任务提交时间。
            scheduled_time:
              type: string
              description: 任务调度时间。
            end_time:
              type: string
              description: 任务结束时间。
            results:
              type: array
              items:
                type: object
                properties:
                  url:
                    type: string
                    description: 生成的图片 URL。
              description: 生成结果列表，每个元素包含一张图片的 URL。
            task_metrics:
              type: object
              properties:
                TOTAL:
                  type: integer
                  description: 总任务数。
                SUCCEEDED:
                  type: integer
                  description: 成功任务数。
                FAILED:
                  type: integer
                  description: 失败任务数。
            code:
              type: string
              description: 错误码（仅在任务失败时返回）。
            message:
              type: string
              description: 错误信息（仅在任务失败时返回）。
        usage:
          type: object
          properties:
            image_count:
              type: integer
              description: 生成的图片数量。
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
          description: 请求唯一标识。
````

> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 创意文字纹理 — 创建任务

> 提交创意文字纹理生成异步任务

<Note>
  请先[获取 API Key](/api-reference/preparation/api-key) 并[设置为环境变量](/api-reference/preparation/export-api-key-env)。
</Note>

## 模型信息

| 模型                | 描述         |
| ----------------- | ---------- |
| `wordart-texture` | 创意文字纹理生成模型 |

## 输入模式

支持两种互斥的输入模式：

| 模式      | 说明                        |
| ------- | ------------------------- |
| `image` | 图片输入模式，传入黑底白字的文字图片        |
| `text`  | 文字输入模式，直接传入文字内容（最多 6 个字符） |

## 纹理风格

通过 `texture_style` 参数指定纹理风格，或通过 `ref_image_url` 传入参考风格图片（将覆盖 `texture_style` 设置）。

**自定义风格**：`material`（立体材质）、`scene`（场景融合）、`lighting`（光影特效）

**预设风格**：`waterfall`、`snow_plateau`、`forest`、`sky`、`chinese_building`、`cartoon`、`lego`、`flower`、`acrylic`、`marble`、`felt`、`oil_painting`、`watercolor_painting`、`chinese_painting`、`claborate_style_painting`、`city_night`、`mountain_lake`、`autumn_leaves`、`green_dragon`、`red_dragon`

## 注意事项

- **QPS 限制**：单账户（含主账号与 RAM 子账号）任务下发接口限制 QPS 为 2，并发任务数量限制为 1。

## OpenAPI

````yaml post /services/aigc/wordart/texture
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
  /services/aigc/wordart/texture:
    post:
      summary: 生成文字纹理
      operationId: createWordArtTextureTask
      parameters:
        - name: X-DashScope-Async
          in: header
          required: true
          schema:
            type: string
            enum:
              - enable
          description: 启用异步模式。
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/WordArtTextureRequest"
      responses:
        "200":
          description: 任务提交成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/AsyncTaskSubmitResponse"
        "400":
          description: 请求错误
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
      x-codeSamples:
        - lang: curl
          label: 图片输入
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/wordart/texture' \
            --header 'X-DashScope-Async: enable' \
            --header 'Content-Type: application/json' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --data '{
              "model": "wordart-texture",
              "input": {
                "image": {
                  "image_url": "https://dmshared-new.oss-cn-hangzhou.aliyuncs.com/junyan.hjy/wordart/lcy/example.png"
                },
                "prompt": "水果，蔬菜，温暖的色彩空间",
                "texture_style": "material"
              },
              "parameters": {
                "image_short_size": 704,
                "n": 2,
                "alpha_channel": false
              }
            }'
        - lang: curl
          label: 文字输入
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/wordart/texture' \
            --header 'X-DashScope-Async: enable' \
            --header 'Content-Type: application/json' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --data '{
              "model": "wordart-texture",
              "input": {
                "text": {
                  "text_content": "文字创意",
                  "font_name": "dongfangdakai",
                  "output_image_ratio": "1:1"
                },
                "prompt": "水果，蔬菜，温暖的色彩空间",
                "texture_style": "material"
              },
              "parameters": {
                "image_short_size": 704,
                "n": 2,
                "alpha_channel": false
              }
            }'
        - lang: curl
          label: 参考图片输入
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/wordart/texture' \
            --header 'X-DashScope-Async: enable' \
            --header 'Content-Type: application/json' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --data '{
              "model": "wordart-texture",
              "input": {
                "text": {
                  "text_content": "文字创意",
                  "font_name": "dongfangdakai",
                  "output_image_ratio": "16:9"
                },
                "prompt": "鲜花",
                "ref_image_url": "https://dmshared-new.oss-cn-hangzhou.aliyuncs.com/0ximian/transfer_20230801/new_design/tmp/wordposter/ref_images/flower2.png"
              },
              "parameters": {
                "image_short_size": 704,
                "n": 2,
                "alpha_channel": false
              }
            }'
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

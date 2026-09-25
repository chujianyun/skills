> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Vidu — 创建任务

> 使用 Vidu 模型提交参考视频生成任务。

生成保留参考图片或视频中主体外观的视频。

## 可用模型

| 模型                                | 参考输入              | 最大时长 |
| --------------------------------- | ----------------- | ---- |
| `vidu/viduq2_reference2video`     | 1–7 张图片           | 10 秒 |
| `vidu/viduq2-pro_reference2video` | 1–4 张图片 + 0–2 段视频 | 10 秒 |

## 图片要求

- **格式**：JPEG、JPG、PNG 或 WEBP
- **宽高比**：1:4 到 4:1 之间
- **文件大小**：每张图片不超过 50 MB

## 视频要求（仅 pro 模型）

- **格式**：MP4、AVI 或 MOV
- **最小尺寸**：128 × 128 像素
- **宽高比**：1:4 到 4:1 之间
- **时长**：1–5 秒
- **文件大小**：每段视频不超过 50 MB

## 轮询结果

该 API 为异步接口。提交任务后：

1. 记录响应中的 `task_id`。
2. 每 **15 秒**轮询一次[查询视频结果](/api-reference/video-generation/vidu-reference-to-video/query-result)。
3. 当 `task_status` 为 `SUCCEEDED` 时，从 `output.video_url` 获取视频。

## OpenAPI

````yaml post /services/aigc/video-generation/video-synthesis
openapi: 3.1.0
info:
  title: Vidu-参考生视频 API
  description: Vidu-参考生视频模型支持传入参考图片和文本提示词，将图片中的主体角色融合到提示词描述的场景中，生成流畅的视频内容。API 采用异步调用模式，包含"创建任务"和"查询结果"两个步骤。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 千问AI平台
security:
  - BearerAuth: []
paths:
  /services/aigc/video-generation/video-synthesis:
    post:
      operationId: createViduReferenceToVideoTask
      summary: 创建参考生视频任务
      description: 提交参考生视频生成任务，支持传入参考图像（或视频）和文本提示词。该接口为异步接口，提交后需轮询查询结果。
      parameters:
        - name: X-DashScope-Async
          in: header
          required: true
          description: |-
            异步处理配置参数。HTTP 请求只支持异步，必须设置为 `enable`。

            > 缺少此请求头将报错："current user api does not support synchronous calls"。
          schema:
            type: string
            enum:
              - enable
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/ViduReferenceToVideoRequest"
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
          label: cURL - 仅参考图像
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
              "model": "vidu/viduq2_reference2video",
              "input": {
                "media": [
                  {
                    "type": "image",
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260320/knsple/wan-r2v-role-frame.jpg"
                  },
                  {
                    "type": "image",
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qpzxps/wan-r2v-object4.png"
                  },
                  {
                    "type": "image",
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/wfjikw/wan-r2v-backgroud5.png"
                  }
                ],
                "prompt": "男人坐在靠窗的椅子上，手持吉他，在咖啡厅旁演奏一首舒缓的美国乡村民谣"
              },
              "parameters": {
                "duration": 5,
                "size": "1280*720",
                "resolution": "720P",
                "watermark": true
              }
            }'
        - lang: curl
          label: cURL - 参考图像+视频
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
              "model": "vidu/viduq2-pro_reference2video",
              "input": {
                "media": [
                  {
                    "type": "video",
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qigswt/wan-r2v-role2.mp4"
                  },
                  {
                    "type": "image",
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qpzxps/wan-r2v-object4.png"
                  },
                  {
                    "type": "image",
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/wfjikw/wan-r2v-backgroud5.png"
                  }
                ],
                "prompt": "男人坐在靠窗的椅子上，手持吉他，在咖啡厅旁演奏一首舒缓的美国乡村民谣"
              },
              "parameters": {
                "duration": 5,
                "size": "1280*720",
                "resolution": "720P",
                "watermark": true
              }
            }'
        - lang: curl
          label: cURL - 广告参考生视频
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
              "model": "vidu/viduq3-ad_reference2video",
              "input": {
                "media": [
                  {
                    "type": "image",
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260320/knsple/wan-r2v-role-frame.jpg"
                  },
                  {
                    "type": "image",
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qpzxps/wan-r2v-object4.png"
                  },
                  {
                    "type": "image",
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/wfjikw/wan-r2v-backgroud5.png"
                  }
                ],
                "prompt": "产品广告展示，镜头从近景推向远景，产品细节清晰可见"
              },
              "parameters": {
                "duration": 5,
                "resolution": "720P",
                "watermark": true
              }
            }'
        - lang: curl
          label: cURL - 精品剧参考生视频
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
              "model": "vidu/viduq3-drama_reference2video",
              "input": {
                "media": [
                  {
                    "type": "image",
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260320/knsple/wan-r2v-role-frame.jpg"
                  },
                  {
                    "type": "image",
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qpzxps/wan-r2v-object4.png"
                  },
                  {
                    "type": "image",
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/wfjikw/wan-r2v-backgroud5.png"
                  },
                  {
                    "type": "image",
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/wfjikw/wan-r2v-backgroud5.png"
                  }
                ],
                "prompt": "角色走进房间，缓缓坐下，表情凝重，灯光从窗外洒落"
              },
              "parameters": {
                "duration": 5,
                "resolution": "1080P",
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
    ViduReferenceToVideoRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: |-
            模型名称。

            | 模型 | 参考输入 | 最大时长 |
            |------|---------|--------|
            | `vidu/viduq2_reference2video` | 1～7 张图像 | 10 秒 |
            | `vidu/viduq2-pro_reference2video` | 1～4 张图像 + 0～2 个视频 | 10 秒 |
            | `vidu/viduq3-ad_reference2video` | 广告视频场景 | 15 秒 |
            | `vidu/viduq3-drama_reference2video` | 精品剧/AI漫剧场景 | 15 秒 |

            **如何选择模型：**
            - 广告视频：选择 `viduq3-ad_reference2video`
            - 精品剧/AI漫剧：选择 `viduq3-drama_reference2video`
            - 通用场景：选择 `viduq2-pro_reference2video` 或 `viduq2_reference2video`（viduq3-mix）
            - 追求速度与性价比：选择 `viduq2_reference2video`（viduq3-turbo）
          enum:
            - vidu/viduq2_reference2video
            - vidu/viduq2-pro_reference2video
            - vidu/viduq3-ad_reference2video
            - vidu/viduq3-drama_reference2video
          example: vidu/viduq2_reference2video
        input:
          type: object
          required:
            - media
            - prompt
          description: 输入的基本信息，包括参考图片和提示词。
          properties:
            prompt:
              type: string
              description: |-
                文本提示词。用来描述生成视频中期望包含的元素和视觉特点。

                - 支持中英文
                - 不超过 5000 个字符，超过部分会自动截断

                示例值：男人坐在靠窗的椅子上，手持吉他，在咖啡厅旁演奏一首舒缓的美国乡村民谣。

                提示词编写请参见Vidu视频生成Prompt指南。
              example: 男人坐在靠窗的椅子上，手持吉他，在咖啡厅旁演奏一首舒缓的美国乡村民谣
            media:
              type: array
              description: |-
                媒体素材列表，用于指定视频生成所需的参考图像或参考视频。

                **vidu/viduq2_reference2video 模型：**
                - 仅支持图像，数量为 1～7 张。
                - type 固定为 `image`。

                **vidu/viduq2-pro_reference2video 模型：**
                - 图像：必选，数量为 1～4 张。
                - 视频：可选，数量为 1～2 个。
                - 仅参考图像时，图像数量为 1～7 张。
                - 参考图像和视频同时使用时，图像数量为 1～4 张，视频数量为 1～2 个。

                **图像限制：**
                - 格式：JPEG、JPG、PNG、WEBP
                - 宽高比：1:4～4:1
                - 文件大小：不超过 50MB

                **视频限制（仅 pro 模型）：**
                - 格式：mp4、avi、mov
                - 分辨率：总像素值不小于 128×128
                - 宽高比：1:4～4:1
                - 时长：1～5 秒
                - 文件大小：不超过 50MB
              minItems: 1
              items:
                type: object
                required:
                  - type
                  - url
                properties:
                  type:
                    type: string
                    description: |-
                      媒体素材类型。可选值与模型有关：
                      - `image`：参考图像
                      - `video`：参考视频（仅 viduq2-pro_reference2video 模型支持）
                    enum:
                      - image
                      - video
                    example: image
                  url:
                    type: string
                    description: |-
                      媒体素材 URL，必须为公网可访问的 URL，支持 HTTP 或 HTTPS 协议。

                      示例值：https://xxx/xxx.png
                    example: https://example.com/character.jpg
        parameters:
          $ref: "#/components/schemas/ViduReferenceToVideoParameters"
    ViduReferenceToVideoParameters:
      type: object
      description: 视频生成参数。用于设置视频分辨率、时长等。
      properties:
        resolution:
          type: string
          description: |-
            生成视频的分辨率。

            > resolution 直接影响费用，请在调用前确认模型价格。

            可选值：
            - `540P`
            - `720P`：默认值
            - `1080P`

            各模型默认值：
            - `vidu/viduq3-ad_reference2video`：可选720P、1080P。默认值为720P
            - `vidu/viduq3-drama_reference2video`：可选720P、1080P。默认值为1080P
          enum:
            - 540P
            - 720P
            - 1080P
          default: 720P
          example: 720P
        size:
          type: string
          description: |-
            生成视频的分辨率，格式为 宽*高 的像素值。

            默认值根据 resolution 而定：
            - resolution=540P 时，size 默认为 960*528
            - resolution=720P 时，size 默认为 1280*720
            - resolution=1080P 时，size 默认为 1920*1080

            各模型支持的宽高比有所不同：
            - vidu/viduq3-drama_reference2video：仅支持 16:9 和 9:16。
            - 其他模型：支持 16:9、4:3、1:1、3:4、9:16。

            > 推荐 resolution 和 size 同时传入，以精准控制生成视频的宽高比。

            **各分辨率档位下 size 的取值：**

            | 分辨率 | 宽高比 | size 取值 |
            |--------|--------|----------|
            | 540P | 16:9 | 960*540 |
            | 540P | 4:3 | 720*540 |
            | 540P | 1:1 | 540*540 |
            | 540P | 3:4 | 540*720 |
            | 540P | 9:16 | 540*960 |
            | 720P | 16:9 | 1280*720 |
            | 720P | 4:3 | 960*720 |
            | 720P | 1:1 | 720*720 |
            | 720P | 3:4 | 720*960 |
            | 720P | 9:16 | 720*1280 |
            | 1080P | 16:9 | 1920*1080 |
            | 1080P | 4:3 | 1440*1080 |
            | 1080P | 1:1 | 1080*1080 |
            | 1080P | 3:4 | 1080*1440 |
            | 1080P | 9:16 | 1080*1920 |
          example: 1280*720
        duration:
          type: integer
          description: |-
            生成视频的时长，单位为秒。

            > duration 直接影响费用，按秒计费，请在调用前确认模型价格。

            **vidu/viduq2-pro_reference2video：**
            - 取值为 [1, 10] 之间的整数，默认值为 5
            - 支持设置为 0，表示自动规划时长，上限不超过 10 秒
            - 若上传 1 个参考视频：生成视频时长通常等于该参考视频时长
            - 若上传 2 个参考视频：生成视频时长通常等于"主要参考视频"的时长

            **vidu/viduq2_reference2video：**
            - 取值为 [1, 10] 之间的整数，默认值为 5

            **vidu/viduq3-ad_reference2video：**
            - 取值为[3, 15]之间的整数，默认值为5

            **vidu/viduq3-drama_reference2video：**
            - 取值为[2, 15]之间的整数，默认值为5
          minimum: 0
          maximum: 15
          default: 5
          example: 5
        watermark:
          type: boolean
          description: |-
            是否添加水印标识，水印位于视频右下角，文案固定为"内容由 AI 生成"。

            - `false`：默认值，不添加水印
            - `true`：添加水印
          default: false
          example: false
        seed:
          type: integer
          description: |-
            随机数种子，取值范围为 [0, 2147483647]。

            未指定时，系统自动生成随机种子。若需提升生成结果的可复现性，建议固定 seed 值。

            > 由于模型生成具有概率性，即使使用相同 seed，也不能保证每次生成结果完全一致。

            示例值：12345
          minimum: 0
          maximum: 2147483647
          example: 12345
        sound_effect:
          type: boolean
          description: |-
            是否为生成的视频添加 AI 音效。

            - `false`：默认值，输出无声视频
            - `true`：输出有声视频

            **支持的模型：** `vidu/viduq3-ad_reference2video`。

            > `vidu/viduq3-drama_reference2video` 默认生成有声视频，不支持此参数。
          default: false
          example: false
    AsyncTaskSubmitResponse:
      type: object
      description: 异步任务提交响应。
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
              description: 任务 ID。查询有效期 24 小时。用于后续调用 GET /tasks/{task_id} 查询任务状态。
              example: 0385dc79-5ff8-4d82-bcb6-xxxxxx
            task_status:
              type: string
              description: 任务状态。初始状态通常为 `PENDING`。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - UNKNOWN
              example: PENDING
    TaskStatusResponse:
      type: object
      description: 任务状态查询响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识。可用于请求明细溯源和问题排查。
          example: 8f240644-efe8-43bf-86ff-xxxxxx
        output:
          type: object
          description: 任务输出信息。
          properties:
            task_id:
              type: string
              description: 任务 ID。查询有效期 24 小时。
              example: b7e05baa-c318-440d-b293-xxxxxx
            task_status:
              type: string
              description: |-
                任务状态。

                - `PENDING`：任务排队中
                - `RUNNING`：任务处理中
                - `SUCCEEDED`：任务执行成功
                - `FAILED`：任务执行失败
                - `CANCELED`：任务已取消
                - `UNKNOWN`：任务不存在或状态未知

                状态流转：PENDING → RUNNING → SUCCEEDED/FAILED
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
              example: 2026-03-27 15:10:42.723
            scheduled_time:
              type: string
              description: 任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。
              example: 2026-03-27 15:10:42.754
            end_time:
              type: string
              description: 任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。
              example: 2026-03-27 15:11:17.388
            orig_prompt:
              type: string
              description: 原始输入的 prompt，对应请求参数 prompt。
              example: 男人坐在靠窗的椅子上，手持吉他，在咖啡厅旁演奏一首舒缓的美国乡村民谣
            video_url:
              type: string
              description: |-
                视频 URL。仅在 task_status 为 SUCCEEDED 时返回。

                视频格式为 MP4（H.264 编码）。视频链接有效期 24 小时，请及时下载。
              example: https://prod-ss-vidu.s3.cn-northwest-1.amazonaws.com.cn/xxx.mp4?xxx
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
              description: 生成视频的分辨率。示例值：960*528。
              example: 960*528
            output_video_duration:
              type: integer
              description: 生成视频的实际时长（秒）。
              example: 5
            fps:
              type: integer
              description: 生成视频的帧率。固定为 24。
              example: 24
            audio:
              type: boolean
              description: 生成视频是否为有声视频。
              example: false
            SR:
              type: string
              description: 生成视频的分辨率档位。示例值：540。
              example: "540"
            video_count:
              type: integer
              description: 生成视频的数量。固定为 1。
              example: 1
            reference_type:
              type: string
              description: 参考素材类型。示例值：image,video。
              example: image,video
    DashScopeErrorResponse:
      type: object
      description: DashScope API 错误响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识。
        code:
          type: string
          description: 错误码，例如 `InvalidApiKey`、`InvalidParameter`。
          example: InvalidApiKey
        message:
          type: string
          description: 错误详情。
          example: No API-key provided.
````

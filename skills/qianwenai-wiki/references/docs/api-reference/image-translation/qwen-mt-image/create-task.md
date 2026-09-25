> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 创建图像翻译任务

> 提交 qwen-mt-image 图像翻译异步任务

## OpenAPI

````yaml post /services/aigc/image2image/image-synthesis
openapi: 3.0.0
info:
  title: 千问-图像翻译 API 参考
  description: |-
    千问-图像翻译模型（Qwen-MT-Image）可精准翻译图像中的文字，并保留原始排版。该模型还支持领域提示、敏感词过滤、术语干预等自定义功能。

    HTTP API 采用异步模式，调用流程分两步：
    1. **创建任务获取任务 ID**：发送 POST 请求创建任务，返回 task_id。
    2. **根据任务 ID 查询结果**：使用 task_id 轮询任务状态，直到任务完成并获得图像 URL。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: DashScope API
security:
  - BearerAuth: []
paths:
  /services/aigc/image2image/image-synthesis:
    post:
      operationId: createImageTranslationTask
      summary: 创建图像翻译任务
      description: 创建一个异步图像翻译任务。输入图像需包含支持语种的文字，且源语种或目标语种中至少有一项为中文或英文。
      parameters:
        - name: X-DashScope-Async
          in: header
          required: true
          description: |-
            异步处理配置参数。HTTP 请求只支持异步，必须设置为 `enable`。

            缺少此请求头将报错："current user api does not support synchronous calls"。
          schema:
            type: string
            enum:
              - enable
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/ImageTranslationRequest"
      responses:
        "200":
          description: 任务创建成功，返回 task_id 用于查询任务状态与结果。
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
          label: cURL
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
            --header 'X-DashScope-Async: enable' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --header 'Content-Type: application/json' \
            --data '{
                "model": "qwen-mt-image",
                "input": {
                    "image_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250916/ordhsk/1.webp",
                    "source_lang": "zh",
                    "target_lang": "en",
                    "ext": {
                        "config": {
                            "imageSegment": false
                        }
                    }
                }
            }'
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    ImageTranslationRequest:
      type: object
      description: 图像翻译请求体。使用 qwen-mt-image 模型进行图像翻译。
      required:
        - model
        - input
      properties:
        model:
          type: string
          enum:
            - qwen-mt-image
          description: 模型名称，必须设置为 `qwen-mt-image`。
        input:
          type: object
          description: 输入参数对象。
          required:
            - image_url
            - source_lang
            - target_lang
          properties:
            image_url:
              type: string
              description: |-
                图像的公网可访问 URL，支持 HTTP 和 HTTPS 协议。

                - **格式限制**：JPG、JPEG、PNG、BMP、PNM、PPM、TIFF、WEBP
                - **尺寸限制**：图像的宽度和高度均需在 15-8192 像素范围内，宽高比在 1:10 至 10:1 范围内
                - **大小限制**：不超过 100MB
                - URL 地址中不能包含中文字符
            source_lang:
              type: string
              description: |-
                源语种。支持语种全称、语种编码或 `auto`（自动检测），对大小写不敏感。

                与 `target_lang` 不同，且至少有一项为中文或英文。

                支持的源语种：`zh`（简体中文）、`en`（英文）、`ko`（韩语）、`ja`（日语）、`ru`（俄语）、`es`（西班牙语）、`fr`（法语）、`pt`（葡萄牙语）、`it`（意大利语）、`vi`（越南语）、`de`（德语）。

                示例：`Chinese`、`en`、`auto`
            target_lang:
              type: string
              description: |-
                目标语种。支持语种全称或语种编码，对大小写不敏感。

                与 `source_lang` 不同，且至少有一项为中文或英文。

                支持的目标语种：`zh`（简体中文）、`en`（英文）、`ko`（韩语）、`ja`（日语）、`ru`（俄语）、`es`（西班牙语）、`fr`（法语）、`pt`（葡萄牙语）、`it`（意大利语）、`vi`（越南语）、`ms`（马来语）、`th`（泰语）、`id`（印尼语）、`ar`（阿拉伯语）。

                注意：德语（`de`）仅支持作为源语种，不支持作为目标语种。

                示例：`Chinese`、`en`
            ext:
              type: object
              description: 可选扩展参数。
              properties:
                domainHint:
                  type: string
                  description: |-
                    领域提示。为使译文风格更贴合特定领域，可以使用英文描述使用场景、译文风格等需求。为确保翻译效果，建议不超过 200 个英文单词。

                    当前只支持英文。
                sensitives:
                  type: array
                  description: |-
                    敏感词列表，用于在翻译前过滤图像中**完全匹配**的文本，**对大小写敏感**。敏感词的语种可与源语种不一致，支持全部源语种和目标语种。建议单次请求添加的敏感词不超过 50 个。

                    示例：["全场9折", "七天无理由退换"]
                  items:
                    type: string
                  maxItems: 50
                terminologies:
                  type: array
                  description: |-
                    术语干预，为特定术语设定译文，以满足特定领域的翻译需求。术语对的语种需要与 `source_lang` 和 `target_lang` 对应。

                    示例：[{"src": "应用程序接口", "tgt": "API"}, {"src": "机器学习", "tgt": "ML"}]
                  items:
                    type: object
                    required:
                      - src
                      - tgt
                    properties:
                      src:
                        type: string
                        description: 术语的源文本，语种需要与源语种 `source_lang` 一致。
                      tgt:
                        type: string
                        description: 术语的目标文本，语种需要与目标语种 `target_lang` 一致。
                config:
                  type: object
                  description: 额外配置选项。
                  properties:
                    imageSegment:
                      type: boolean
                      default: false
                      description: |-
                        是否开启图像主体分割。开启后，将跳过对图像中主体（如人物、商品、Logo）上文字的翻译。

                        - `false`：（默认值）翻译图像中的所有文字
                        - `true`：不翻译图像主体的文字

                        旧版本参数名为 `skipImgSegment`，为保持兼容仍受支持，但建议使用新的 `imageSegment` 参数。
    AsyncTaskSubmitResponse:
      type: object
      description: 异步任务成功创建时的响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识。可用于请求明细溯源和问题排查。
        output:
          type: object
          description: 任务输出信息。
          properties:
            task_id:
              type: string
              description: 任务 ID。查询有效期 24 小时。
            task_status:
              type: string
              enum:
                - PENDING
              description: 任务状态。新创建的任务始终返回 `PENDING`。
    ImageTranslationTaskStatusResponse:
      type: object
      description: 查询图像翻译任务状态和结果时的响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识。可用于请求明细溯源和问题排查。
        output:
          type: object
          description: 任务输出信息。
          properties:
            task_id:
              type: string
              description: 任务 ID。查询有效期 24 小时。
            task_status:
              type: string
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - CANCELED
                - UNKNOWN
              description: |-
                任务状态。
                - PENDING：任务排队中
                - RUNNING：任务处理中
                - SUCCEEDED：任务执行成功
                - FAILED：任务执行失败
                - CANCELED：任务已取消
                - UNKNOWN：任务不存在或状态未知
            submit_time:
              type: string
              description: 任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。
            scheduled_time:
              type: string
              description: 任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。
            end_time:
              type: string
              description: 任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。
            image_url:
              type: string
              description: 模型生成图像的 URL 地址，与原图长宽相同，JPG 格式。有效期为 24 小时，请及时下载并保存图像。
            message:
              type: string
              description: 附加信息。通常不会返回此参数，仅在图像中无可翻译文本时，任务仍会成功并正常计费，但会返回 `No text detected for translation` 的提示；任务失败时会返回失败详情。
            code:
              type: string
              description: 请求失败的错误码。请求成功时不会返回此参数。
        usage:
          type: object
          description: 输出信息统计。只对成功的结果计数。
          properties:
            image_count:
              type: integer
              description: 模型生成图像的数量，固定为 1。
    DashScopeErrorResponse:
      type: object
      description: DashScope API 错误响应。
      properties:
        code:
          type: string
          description: 错误码（如 `InvalidApiKey`、`InvalidParameter`）。
        message:
          type: string
          description: 人类可读的错误描述。
        request_id:
          type: string
          description: 请求唯一标识。
````

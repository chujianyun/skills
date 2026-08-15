> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Z-Image

> 轻量快速图像生成

<Note>
  请先[获取 API Key](/api-reference/preparation/api-key) 并[配置为环境变量](/api-reference/preparation/export-api-key-env)。如需使用 SDK，请先[安装](/api-reference/preparation/install-sdk)。
</Note>

Z-Image 是一款轻量级文生图模型，生成速度快。支持中英文文字渲染，适配多种分辨率和宽高比。

**快速链接**：[模型体验](https://platform.qianwenai.com/home/try-ai/chat?models=z-image-turbo) | [技术博客](https://tongyi-mai.github.io/Z-Image-blog/)

## OpenAPI

````yaml post /services/aigc/multimodal-generation/generation
openapi: 3.1.0
info:
  title: Z-Image API
  description: Z-Image 文生图 API。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 北京
security:
  - BearerAuth: []
paths:
  /services/aigc/multimodal-generation/generation:
    post:
      operationId: createZImage
      summary: 生成图像
      description: 使用 z-image-turbo 根据文本提示词生成图像。结果同步返回，无需轮询。
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/ZImageRequest"
      responses:
        "200":
          description: 图像生成结果
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ZImageResponse"
              examples:
                success:
                  summary: 生成成功
                  value:
                    output:
                      choices:
                        - finish_reason: stop
                          message:
                            role: assistant
                            content:
                              - image: https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx.png?Expires=xxx
                              - text: Photo of a stylish young woman...
                            reasoning_content: ""
                    usage:
                      width: 1024
                      height: 1024
                      image_count: 1
                      input_tokens: 0
                      output_tokens: 0
                      total_tokens: 0
                    request_id: abf1645b-b630-433a-92f6-xxxxxx
        "400":
          description: 请求参数无效
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
              examples:
                error:
                  summary: 参数错误
                  value:
                    request_id: a4d78a5f-655f-9639-8437-xxxxxx
                    code: InvalidParameter
                    message: num_images_per_prompt must be 1
        "401":
          description: 鉴权失败，API Key 无效或缺失
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
        "429":
          description: 请求频率超限
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
      x-codeSamples:
        - lang: curl
          label: cURL
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
            --header 'Content-Type: application/json' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --data '{
              "model": "z-image-turbo",
              "input": {
                "messages": [
                  {
                    "role": "user",
                    "content": [
                      {
                        "text": "A sitting orange cat with a happy expression, lively and cute, realistic and accurate"
                      }
                    ]
                  }
                ]
              },
              "parameters": {
                "prompt_extend": false,
                "size": "1024*1024"
              }
            }'
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    ZImageRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称。
          enum:
            - z-image-turbo
          example: z-image-turbo
        input:
          type: object
          required:
            - messages
          description: 输入内容。
          properties:
            messages:
              type: array
              description: "请求内容数组。**仅支持单轮对话**，传入一条 `role: user` 的消息，不支持多轮。"
              minItems: 1
              maxItems: 1
              items:
                $ref: "#/components/schemas/ZImageMessage"
        parameters:
          $ref: "#/components/schemas/ZImageParameters"
    ZImageMessage:
      type: object
      required:
        - role
        - content
      properties:
        role:
          type: string
          enum:
            - user
          description: 消息角色。必须为 `user`。
        content:
          type: array
          description: 消息内容数组。必须包含且仅包含一个文本对象；传入零个或超过一个对象时将返回错误。
          items:
            $ref: "#/components/schemas/ZImageContentPart"
    ZImageContentPart:
      type: object
      properties:
        text:
          type: string
          description: 描述所需内容、风格和构图的正向提示词，支持中英文。最多 800 个字符（每个汉字、字母、数字或符号均计为 1 个字符），超出部分将被截断。
          maxLength: 800
          example: A sitting orange cat with a happy expression, lively and cute, realistic and accurate
    ZImageParameters:
      type: object
      description: 图像生成参数。
      properties:
        size:
          type: string
          description: |-
            输出图像分辨率，格式为 `宽*高`。范围：512×512 至 2048×2048 像素，推荐范围：1024×1024 至 1536×1536。默认值：`1024*1536`。

            推荐分辨率（总像素约 1024×1024）：`1024*1024`（1:1）、`832*1248`（2:3）、`1248*832`（3:2）、`864*1152`（3:4）、`1152*864`（4:3）、`720*1280`（9:16）、`1280*720`（16:9）。

            推荐分辨率（总像素约 1280×1280）：`1280*1280`（1:1）、`1024*1536`（2:3）、`1536*1024`（3:2）、`1104*1472`（3:4）、`1472*1104`（4:3）、`864*1536`（9:16）、`1536*864`（16:9）。

            推荐分辨率（总像素约 1536×1536）：`1536*1536`（1:1）、`1248*1872`（2:3）、`1872*1248`（3:2）、`1296*1728`（3:4）、`1728*1296`（4:3）、`1152*2048`（9:16）、`2048*1152`（16:9）。
          default: 1024*1536
          example: 1024*1024
        prompt_extend:
          type: boolean
          description: |-
            开启基于大模型的智能提示词改写。

            - `false`（默认）：返回图像和原始提示词，不产生额外费用。
            - `true`：返回图像、优化后的提示词及推理内容，会增加响应时间和费用。
          default: false
        seed:
          type: integer
          description: |-
            用于控制生成结果可复现性的随机种子。有效范围：`[0, 2147483647]`。相同种子通常生成相似结果；不填时使用随机种子。

            **注意：** 图像生成具有随机性，即使使用相同种子，结果也可能存在差异。
          minimum: 0
          maximum: 2147483647
    ZImageResponse:
      type: object
      description: 图像生成响应。
      properties:
        output:
          type: object
          description: 模型输出。
          properties:
            choices:
              type: array
              description: 模型输出内容，数组中包含一个元素。
              items:
                $ref: "#/components/schemas/ZImageChoice"
        usage:
          $ref: "#/components/schemas/ZImageUsage"
        request_id:
          type: string
          description: 请求唯一标识符，可用于追踪和排查问题。
          example: abf1645b-b630-433a-92f6-xxxxxx
    ZImageChoice:
      type: object
      properties:
        finish_reason:
          type: string
          description: 生成结束原因。`stop` 表示成功。
          example: stop
        message:
          type: object
          description: 模型响应消息。
          properties:
            role:
              type: string
              description: 消息角色。固定为 `assistant`。
              enum:
                - assistant
            content:
              type: array
              description: 响应内容项，包含带有生成图像 URL 的 `image` 对象和带有提示词的 `text` 对象。
              items:
                $ref: "#/components/schemas/ZImageResponseContentPart"
            reasoning_content:
              type: string
              description: 模型推理输出。仅在 `prompt_extend=true` 时返回，否则为空字符串。
    ZImageResponseContentPart:
      type: object
      description: 响应中的内容项，每项包含 `image` 或 `text` 字段之一。
      properties:
        image:
          type: string
          description: 生成的图像 URL（PNG 格式）。**有效期 24 小时**，请及时下载。
        text:
          type: string
          description: 原始提示词（当 `prompt_extend=false` 时）或经过优化的提示词（当 `prompt_extend=true` 时）。
    ZImageUsage:
      type: object
      description: 用量统计，仅包含成功生成的数据。
      properties:
        width:
          type: integer
          description: 生成图像的宽度（像素）。
        height:
          type: integer
          description: 生成图像的高度（像素）。
        image_count:
          type: integer
          description: 生成图像数量。固定为 1。
        input_tokens:
          type: integer
          description: 消耗的输入 token 数。`prompt_extend=false` 时为 `0`。
        output_tokens:
          type: integer
          description: 消耗的输出 token 数。`prompt_extend=false` 时为 `0`。
        output_tokens_details:
          type: object
          description: 输出 token 明细，仅在 `prompt_extend=true` 时返回。
          properties:
            reasoning_tokens:
              type: integer
              description: 用于推理的 token 数。
        total_tokens:
          type: integer
          description: 消耗的总 token 数。`prompt_extend=false` 时为 `0`。
    ErrorResponse:
      type: object
      description: 错误响应，请求失败时返回。
      properties:
        request_id:
          type: string
          description: 请求唯一标识符。
        code:
          type: string
          description: 错误码（如 `InvalidParameter`、`Throttling`、`Unauthorized`）。
          example: InvalidParameter
        message:
          type: string
          description: 可读的错误说明。
          example: num_images_per_prompt must be 1
````

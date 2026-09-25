> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# DashScope 多模态向量

> 多模态向量化 API

将文本、图像和视频转换为统一语义空间中的数值向量，用于跨模态检索、相似度搜索和内容分类。

<Note>
  开始前：[获取 API Key](/api-reference/preparation/api-key)，[将其设置为环境变量](/api-reference/preparation/export-api-key-env)，如需使用 SDK 请先[安装 DashScope SDK](/api-reference/preparation/install-sdk)。
</Note>

## 请求地址

- HTTP：`POST https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding`
- SDK `base_http_api_url`：`https://dashscope.aliyuncs.com/api/v1`

## 模型概览

| 模型                            | 支持模态        | 向量维度                         | 单张图片大小 |
| ----------------------------- | ----------- | ---------------------------- | ------ |
| tongyi-embedding-vision-plus  | 文本、图像、视频、多图 | 64、128、256、512、1024、1152（默认） | 10 MB  |
| tongyi-embedding-vision-flash | 文本、图像、视频、多图 | 64、128、256、512、768（默认）       | 5 MB   |

## 使用说明

- **图像输入**：公网 URL 或 Base64 数据 URI（`data:image/{format};base64,{data}`）。
- **多图输入**：使用 `multi_images` 字段，值为图像 URL 列表，最多 8 张。
- **视频输入**：必须为公网 URL。通过 `parameters` 中的 `fps` 参数控制采样帧率（取值范围 \[0, 1]，默认 1.0）。

## OpenAPI

````yaml post /services/embeddings/multimodal-embedding/multimodal-embedding
openapi: 3.1.0
info:
  title: 千问AI平台图像 API
  description: DashScope 图像 API，涵盖图像生成、图像编辑、专项图像任务及多模态向量嵌入。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: DashScope API
security:
  - BearerAuth: []
paths:
  /services/embeddings/multimodal-embedding/multimodal-embedding:
    post:
      operationId: createMultimodalEmbedding
      summary: 创建多模态向量嵌入
      description: 将文本、图像和视频映射到统一向量空间。适用于跨模态检索、语义相似度计算、内容分类等场景。所有模态共享同一语义空间，可直接通过余弦相似度跨模态比较向量。
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/MultimodalEmbeddingRequest"
      responses:
        "200":
          description: 多模态向量嵌入结果
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/MultimodalEmbeddingResponse"
        "400":
          description: 请求参数无效
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
        "401":
          description: 认证失败——API Key 无效或未提供
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
        "429":
          description: 请求频率超出限制
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
      x-codeSamples:
        - lang: curl
          label: cURL (Independent Vectors)
          source: |-
            curl --location --request POST \
              'https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --header 'Content-Type: application/json' \
            --data '{
                "model": "tongyi-embedding-vision-plus",
                "input": {
                    "contents": [
                        {"text": "Multimodal embedding model"},
                        {"image": "https://example.com/image.jpg"},
                        {"video": "https://example.com/video.mp4"}
                    ]
                }
            }'
        - lang: curl
          label: cURL (Fused Vector)
          source: |-
            curl --location --request POST \
              'https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --header 'Content-Type: application/json' \
            --data '{
                "model": "tongyi-embedding-vision-plus",
                "input": {
                    "contents": [
                        {
                            "text": "Test text for generating a fused multimodal vector",
                            "image": "https://example.com/image.png",
                            "video": "https://example.com/video.mp4"
                        }
                    ]
                },
                "parameters": {
                    "dimension": 1024
                }
            }'
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    SyncImageRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称。文生图使用 `wan2.6-t2i`，图像编辑与图文交替输出使用 `wan2.6-image`，轻量快速生成使用 `z-image-turbo`。
          enum:
            - wan2.6-t2i
            - wan2.6-image
            - z-image-turbo
          example: wan2.6-t2i
        input:
          type: object
          required:
            - messages
          description: 包含消息数组的输入数据。
          properties:
            messages:
              type: array
              description: 仅支持单轮对话，包含一条角色为 `user` 的消息。
              minItems: 1
              maxItems: 1
              items:
                $ref: "#/components/schemas/ImageMessage"
        parameters:
          $ref: "#/components/schemas/SyncImageParameters"
    ImageMessage:
      type: object
      required:
        - role
        - content
      properties:
        role:
          type: string
          enum:
            - user
          description: 必须为 `user`。
        content:
          type: array
          description: 内容项数组，必须包含且仅包含一个文本对象。使用图像编辑模式（`wan2.6-image`）时，还可包含 1-4 个图像对象（编辑模式）或 0-1 个图像对象（图文交替模式）。
          items:
            $ref: "#/components/schemas/ImageContentPart"
    ImageContentPart:
      type: object
      description: 消息中的内容项。每个对象只能提供 `text` 或 `image` 其中之一，不可同时包含两者。
      properties:
        text:
          type: string
          description: 图像生成提示词。`wan2.6-t2i` 最多 2100 个字符，`wan2.6-image` 最多 2000 个字符，`z-image-turbo` 最多 800 个字符。每个内容数组中只允许包含一个文本对象。
          maxLength: 2100
        image:
          type: string
          description: 参考图像 URL（HTTP/HTTPS）或 Base64 数据 URI（`data:{MIME_type};base64,{data}`）。仅限图像编辑模式（`wan2.6-image` 且 `enable_interleave=false`）：需提供 1-4 张图像；图文交替模式：0-1 张图像。支持格式：JPEG、JPG、PNG、BMP、WEBP。分辨率：每边 [384, 5000] 像素，最大 10 MB。
    SyncImageParameters:
      type: object
      description: 生成参数。
      properties:
        size:
          type: string
          description: 输出分辨率，格式为 `宽*高`。`wan2.6-t2i`：总像素范围 [1280x1280, 1440x1440]，宽高比 [1:4, 4:1]，默认值：`1280*1280`。`wan2.6-image`：总像素范围 [768x768, 1280x1280]，宽高比 [1:4, 4:1]，默认值：`1280*1280`。`z-image-turbo`：总像素范围 [512x512, 2048x2048]，默认值：`1024*1536`。
          default: 1280*1280
          example: 1280*1280
        n:
          type: integer
          description: 生成图像数量，范围 1-4，默认值：4，按实际生成张数计费。图文交替模式下必须为 1。
          minimum: 1
          maximum: 4
          default: 4
        prompt_extend:
          type: boolean
          description: 开启智能提示词扩写，会增加约 3-4 秒延迟。适用于 `wan2.6-t2i`、`wan2.6-image`（仅编辑模式）及 `z-image-turbo`。`z-image-turbo` 开启后费用更高（详见定价）。wan2.6 系列默认值：`true`，z-image-turbo 默认值：`false`。
          default: true
        watermark:
          type: boolean
          description: 在输出图像上添加 "AI 生成" 水印，默认值：`false`。
          default: false
        negative_prompt:
          type: string
          description: 生成图像时需排除的元素，仅适用于 `wan2.6-t2i`。
        enable_interleave:
          type: boolean
          description: 仅适用于 `wan2.6-image`。`false`（默认）：图像编辑模式；`true`：图文交替输出模式（需开启流式输出）。
          default: false
        max_images:
          type: integer
          description: 仅适用于 `wan2.6-image` 图文交替模式，每次响应最多生成的图像数量，范围 1-5，默认值：5。实际数量由模型决定。
          minimum: 1
          maximum: 5
          default: 5
        stream:
          type: boolean
          description: 开启流式输出。图文交替模式（`enable_interleave=true`）时必须设置为 `true`，默认值：`false`。
          default: false
    AsyncImageRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 异步图像生成的模型名称。
          enum:
            - wan2.6-t2i
            - wan2.5-t2i-preview
            - wan2.2-t2i-flash
            - wan2.2-t2i-plus
            - wanx2.1-t2i-turbo
            - wanx2.1-t2i-plus
            - flux-schnell
            - flux-dev
            - flux-merged
          example: wan2.6-t2i
        input:
          type: object
          required:
            - messages
          description: 包含消息数组的输入数据。
          properties:
            messages:
              type: array
              description: 仅支持单轮对话，包含一条角色为 `user` 的消息。
              minItems: 1
              maxItems: 1
              items:
                $ref: "#/components/schemas/ImageMessage"
        parameters:
          $ref: "#/components/schemas/AsyncImageParameters"
    AsyncImageParameters:
      type: object
      description: 异步图像生成的生成参数。
      properties:
        size:
          type: string
          description: 输出分辨率，格式为 `宽*高`，支持的值因模型而异。Wan 系列：参见各模型限制；FLUX 系列：`512*1024`、`768*512`、`768*1024`、`1024*576`、`576*1024`、`1024*1024`。默认值：`1280*1280`（Wan）或 `1024*1024`（FLUX）。
          example: 1280*1280
        n:
          type: integer
          description: 生成图像数量，范围 1-4，默认值：4（Wan 系列）或 1（FLUX 系列）。
          minimum: 1
          maximum: 4
        prompt_extend:
          type: boolean
          description: 开启智能提示词扩写，会增加约 3-4 秒延迟，默认值：`true`。
          default: true
        watermark:
          type: boolean
          description: 在输出图像上添加 "AI 生成" 水印，默认值：`false`。
          default: false
        negative_prompt:
          type: string
          description: 生成图像时需排除的元素。
    SpecializedImageRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 专项图像任务的模型名称。
          enum:
            - wanx-style-repaint-v1
            - wanx-background-generation-v2
            - image-expansion
            - wanx-poster-generation-v1
            - image-inpainting
            - person-segmentation
            - wanx-sketch-to-image-v1
            - aitryon-v1
            - aitryon-v2
            - virtual-model
            - shoe-model
            - facechain-generation
          example: aitryon-v2
        input:
          type: object
          description: 特定于模型的输入数据，结构因模型而异。详见上方接口描述中各模型的参数说明。
          properties:
            person_image_url:
              type: string
              description: 人物图像 URL，适用于 `aitryon-v1` 和 `aitryon-v2`。
            garment_image_url:
              type: string
              description: 服装图像 URL，适用于 `aitryon-v1` 和 `aitryon-v2`。
            base_image_url:
              type: string
              description: 前景/产品图像 URL，适用于 `wanx-background-generation-v2`。
            prompt:
              type: string
              description: 描述期望输出效果的文本提示词，适用于 `wanx-background-generation-v2` 及其他模型。
        parameters:
          $ref: "#/components/schemas/SpecializedImageParameters"
    SpecializedImageParameters:
      type: object
      description: 专项图像任务的参数，可用参数因模型而异。
      properties:
        n:
          type: integer
          description: 生成图像数量，范围 1-4，默认值因模型而异。
          minimum: 1
          maximum: 4
        resolution:
          type: integer
          description: 输出分辨率（短边像素数），适用于虚拟试穿模型，默认值：768。
          default: 768
    WordArtRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 艺术字生成的模型名称。
          enum:
            - wordart-texture
            - wordart-deformation-v1
          example: wordart-texture
        input:
          type: object
          required:
            - text
            - prompt
          description: 艺术字生成的输入数据。
          properties:
            text:
              type: object
              required:
                - text_content
                - font_name
              description: 文字配置。
              properties:
                text_content:
                  type: string
                  description: 要渲染的文本内容，最多 6 个字符。
                  maxLength: 6
                  example: AI
                font_name:
                  type: string
                  description: 基础文字的字体名称。
                  example: dongfangdakai
            prompt:
              type: string
              description: 纹理效果的风格描述。
              example: Flames and fire, burning effect
        parameters:
          type: object
          description: 生成参数。
          properties:
            n:
              type: integer
              description: 生成图像数量，默认值：4。
              default: 4
    MultimodalEmbeddingRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 多模态向量嵌入的模型名称。
          enum:
            - tongyi-embedding-vision-plus
            - tongyi-embedding-vision-flash
          example: tongyi-embedding-vision-plus
        input:
          type: object
          required:
            - contents
          description: 包含内容项的输入数据。
          properties:
            contents:
              type: array
              description: 内容项列表，每项为包含一个或多个模态键（`text`、`image`、`video`、`multi_images`）的对象。生成独立向量时每个对象只使用一种模态；生成融合向量时将多种模态组合在同一对象中。
              items:
                $ref: "#/components/schemas/MultimodalContentItem"
        parameters:
          $ref: "#/components/schemas/MultimodalEmbeddingParameters"
    MultimodalContentItem:
      type: object
      description: 多模态向量嵌入的内容项，可包含一个或多个模态键。生成独立向量时每个对象使用一个键；生成融合向量时在同一对象中组合多个键。
      properties:
        text:
          type: string
          description: 要嵌入的文本内容。
        image:
          type: string
          description: 图像 URL（公开的 HTTP/HTTPS 链接）或 Base64 数据 URI（`data:image/{format};base64,{data}`）。
        video:
          type: string
          description: 视频 URL（必须为公开链接）。
        multi_images:
          type: array
          description: 用于多图嵌入的图像 URL 列表，最多 8 张图像，仅 `tongyi-embedding-vision-plus` 和 `tongyi-embedding-vision-flash` 支持。
          items:
            type: string
          maxItems: 8
    MultimodalEmbeddingParameters:
      type: object
      description: 多模态向量嵌入的参数。
      properties:
        output_type:
          type: string
          description: 输出格式，目前仅支持 `dense`。
          enum:
            - dense
          default: dense
        dimension:
          type: integer
          description: 输出向量维度，支持的值因模型而异，详见模型概览表中的默认值与可选项。
        fps:
          type: number
          description: 视频帧采样率，范围 [0, 1]，默认值：1.0。
          minimum: 0
          maximum: 1
          default: 1
        instruct:
          type: string
          description: 自定义任务指令，建议使用英文，通常可使检索任务效果提升 1-5%。
    SyncImageResponse:
      type: object
      description: 同步图像生成或编辑的响应结果。
      properties:
        output:
          type: object
          properties:
            choices:
              type: array
              description: 生成结果列表。
              items:
                $ref: "#/components/schemas/ImageChoice"
            finished:
              type: boolean
              description: 任务是否已完成。
        usage:
          $ref: "#/components/schemas/ImageUsage"
        request_id:
          type: string
          description: 唯一请求标识符。
          example: 815505c6-7c3d-49d7-b197-xxxxx
    ImageChoice:
      type: object
      properties:
        finish_reason:
          type: string
          description: 正常完成时为 `stop`，流式输出过程中为 `null`。
          example: stop
        message:
          type: object
          properties:
            role:
              type: string
              description: 始终为 `assistant`。
              enum:
                - assistant
            content:
              type: array
              description: 内容项数组，每项包含图像 URL 或文本（图文交替模式下）。
              items:
                $ref: "#/components/schemas/ImageResponseContentPart"
    ImageResponseContentPart:
      type: object
      description: 响应消息中的内容项。
      properties:
        type:
          type: string
          description: 内容类型：`image` 或 `text`（仅图文交替模式下包含文本）。
          enum:
            - image
            - text
        image:
          type: string
          description: 生成的图像 URL（PNG 格式），**有效期 24 小时**，当 `type` 为 `image` 时存在。
        text:
          type: string
          description: 生成的文本内容，当 `type` 为 `text` 时存在（图文交替模式）。
    ImageUsage:
      type: object
      description: 图像生成的用量统计。
      properties:
        image_count:
          type: integer
          description: 已生成的图像数量。
        input_tokens:
          type: integer
          description: 消耗的输入 token 数，编辑模式下为 0，图文交替模式下为实际值。
        output_tokens:
          type: integer
          description: 消耗的输出 token 数，编辑模式下为 0，图文交替模式下为实际值。
        size:
          type: string
          description: 输出分辨率。
          example: 1280*1280
        total_tokens:
          type: integer
          description: 总 token 数（input_tokens + output_tokens）。
    AsyncTaskSubmitResponse:
      type: object
      description: 异步任务提交后的响应结果。
      properties:
        request_id:
          type: string
          description: 唯一请求标识符。
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 用于轮询状态的任务 ID，配合 `GET /tasks/{task_id}` 使用。
            task_status:
              type: string
              description: 任务初始状态，通常为 `PENDING`。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
    AsyncTaskStatusResponse:
      type: object
      description: 异步任务的状态与结果。
      properties:
        request_id:
          type: string
          description: 唯一请求标识符。
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID。
            task_status:
              type: string
              description: 当前任务状态。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
            results:
              type: array
              description: 已生成的图像结果列表，当 `task_status` 为 `SUCCEEDED` 时存在。
              items:
                $ref: "#/components/schemas/AsyncTaskResult"
            task_metrics:
              $ref: "#/components/schemas/TaskMetrics"
        usage:
          type: object
          description: 用量统计。
          properties:
            image_count:
              type: integer
              description: 成功生成的图像数量。
    AsyncTaskResult:
      type: object
      description: 异步任务的单条结果。
      properties:
        url:
          type: string
          description: 生成图像的 URL，**有效期 24 小时**。
    TaskMetrics:
      type: object
      description: 任务完成情况统计。
      properties:
        TOTAL:
          type: integer
          description: 请求生成的图像总数。
        SUCCEEDED:
          type: integer
          description: 成功生成的图像数量。
        FAILED:
          type: integer
          description: 生成失败的图像数量。
    MultimodalEmbeddingResponse:
      type: object
      description: 多模态向量嵌入的响应结果。
      properties:
        output:
          type: object
          properties:
            embeddings:
              type: array
              description: 向量嵌入结果列表。
              items:
                $ref: "#/components/schemas/MultimodalEmbeddingData"
        usage:
          type: object
          description: Token 用量统计。不同模型返回的字段存在差异：`tongyi-embedding-vision-*` 系列返回 `input_tokens`（含文本和图片 Token 总和）、`input_tokens_details`、`output_tokens`、`total_tokens`；其他模型返回的字段可能不同，详见各字段说明。
          properties:
            input_tokens:
              type: integer
              description: 本次请求输入内容的 Token 数目。对于 `tongyi-embedding-vision-*` 系列模型，该值包含文本和图片/视频 Token 的总和。
            input_tokens_details:
              type: object
              description: 输入 Token 的详细分类信息。仅 `tongyi-embedding-vision-*` 系列模型返回此字段。
              properties:
                image_tokens:
                  type: integer
                  description: 输入内容中图片或视频等视觉部分消耗的 Token 数量，不包含文本（文本部分见 `text_tokens`）。图片消耗的 Token 数量与输入图片的分辨率有关，分辨率越高消耗的 Token 越多；若输入为视频，系统会先对视频抽帧，再基于抽帧结果计算 Token。
                text_tokens:
                  type: integer
                  description: 输入内容中文本部分消耗的 Token 数量（不包含图片或视频等视觉部分）。
            output_tokens:
              type: integer
              description: 本次请求输出的 Token 数目。仅 `tongyi-embedding-vision-*` 系列模型返回此字段。
            total_tokens:
              type: integer
              description: 输入与输出的 Token 总数。
            image_tokens:
              type: integer
              description: 本次请求输入的图片或视频等视觉部分消耗的 Token 数量（不包含文本）。图片消耗的 Token 数量与输入图片的分辨率有关；系统会对输入视频进行抽帧处理，帧数上限受系统配置控制，随后基于处理结果计算 Token。仅 `qwen3-vl-embedding`、`qwen2.5-vl-embedding` 和 `multimodal-embedding-v1` 返回此字段（作为顶层字段），`tongyi-embedding-vision-*` 系列模型的图片 Token 包含在 `input_tokens_details.image_tokens` 中。
        request_id:
          type: string
          description: 唯一请求标识符。
          example: 1fff9502-a6c5-9472-9ee1-73930fdd04c5
    MultimodalEmbeddingData:
      type: object
      description: 单条向量嵌入结果。
      properties:
        index:
          type: integer
          description: 在输入内容列表中的位置索引。
        embedding:
          type: array
          description: 浮点数向量。
          items:
            type: number
        type:
          type: string
          description: 本条嵌入结果的内容类型。
          enum:
            - text
            - image
            - video
    DashScopeErrorResponse:
      type: object
      description: DashScope API 错误响应。
      properties:
        request_id:
          type: string
          description: 唯一请求标识符。
        code:
          type: string
          description: 错误码（如 `InvalidParameter`、`Throttling`、`Unauthorized`）。
          example: InvalidParameter
        message:
          type: string
          description: 可读的错误信息。
          example: num_images_per_prompt must be 1
````

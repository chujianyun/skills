> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Wan v2 — 同步调用

> Wan 文生图同步接口

<Note>
  [获取 API Key](/api-reference/preparation/api-key) 并[将其设置为环境变量](/api-reference/preparation/export-api-key-env)。如需使用 SDK，请先[安装 SDK](/api-reference/preparation/install-sdk)。
</Note>

该同步接口仅适用于 **wan2.6-t2i** 模型，可在单次请求中直接返回生成的图像，无需轮询。

wan2.5 及更早版本，或需要异步处理时，请使用[异步提交](/api-reference/image-generation/wan-text-to-image-v2/create-task)接口。

## SDK 版本要求

- **DashScope Python SDK**：需 **1.25.7** 或更高版本。
- **DashScope Java SDK**：需 **2.22.6** 或更高版本。

## OpenAPI

````yaml post /services/aigc/multimodal-generation/generation
openapi: 3.1.0
info:
  title: Wan 文生图 V2 API
  description: 使用 Wan 文生图模型系列，根据文本描述生成图像。支持多种艺术风格和写实摄影效果，满足多样化的创意需求。本 API 采用异步任务模式：先通过 POST 请求提交任务，再通过 GET 请求轮询结果。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 阿里云 DashScope
security:
  - BearerAuth: []
paths:
  /services/aigc/multimodal-generation/generation:
    post:
      operationId: createWanT2ISyncGeneration
      summary: 同步生成图像
      description: 使用 Wan2.6 模型同步生成图像。
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/Wan26TextToImageRequest"
      responses:
        "200":
          description: 图像生成成功。
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Wan26SyncResponse"
        "400":
          description: 请求参数无效。
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
      x-codeSamples:
        - lang: curl
          label: cURL - wan2.6-t2i (sync)
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
            --header 'Content-Type: application/json' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --data '{
              "model": "wan2.6-t2i",
              "input": {
                "messages": [
                  {
                    "role": "user",
                    "content": [
                      {
                        "text": "A flower shop with exquisite windows, a beautiful wooden door, and flowers on display"
                      }
                    ]
                  }
                ]
              },
              "parameters": {
                "prompt_extend": true,
                "watermark": false,
                "n": 1,
                "negative_prompt": "",
                "size": "1280*1280"
              }
            }'
        - lang: python
          label: Python - wan2.6-t2i (sync, DashScope SDK)
          source: |-
            import os
            import dashscope
            from dashscope.aigc.image_generation import ImageGeneration
            from dashscope.api_entities.dashscope_response import Message

            # wan2.6-t2i 需要 SDK 版本 1.25.7 或更高版本
            dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
            api_key = os.getenv("DASHSCOPE_API_KEY")

            message = Message(
              role="user",
              content=[
                {
                  'text': 'A flower shop with exquisite windows, a beautiful wooden door, and flowers on display'
                }
              ]
            )
            print("----sync call, please wait a moment----")
            rsp = ImageGeneration.call(
              model="wan2.6-t2i",
              api_key=api_key,
              messages=[message],
              negative_prompt="",
              prompt_extend=True,
              watermark=False,
              n=1,
              size="1280*1280"
            )
            print(rsp)
        - lang: java
          label: Java - wan2.6-t2i (sync, DashScope SDK)
          source: |-
            import com.alibaba.dashscope.aigc.imagegeneration.*;
            import com.alibaba.dashscope.exception.ApiException;
            import com.alibaba.dashscope.exception.NoApiKeyException;
            import com.alibaba.dashscope.exception.UploadFileException;
            import com.alibaba.dashscope.utils.Constants;
            import com.alibaba.dashscope.utils.JsonUtils;
            import java.util.Collections;

            public class Main {

              static {
                Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
              }

              // wan2.6-t2i 需要 SDK 版本 2.22.6 或更高版本
              static String apiKey = System.getenv("DASHSCOPE_API_KEY");

              public static void basicCall() throws ApiException, NoApiKeyException, UploadFileException {
                ImageGenerationMessage message = ImageGenerationMessage.builder()
                    .role("user")
                    .content(Collections.singletonList(
                        Collections.singletonMap("text", "A flower shop with exquisite windows, a beautiful wooden door, and flowers on display")
                    )).build();

                ImageGenerationParam param = ImageGenerationParam.builder()
                    .apiKey(apiKey)
                    .model("wan2.6-t2i")
                    .n(1)
                    .size("1280*1280")
                    .negativePrompt("")
                    .promptExtend(true)
                    .watermark(false)
                    .messages(Collections.singletonList(message))
                    .build();

                ImageGeneration imageGeneration = new ImageGeneration();
                ImageGenerationResult result = null;
                try {
                  System.out.println("---sync call, please wait a moment----");
                  result = imageGeneration.call(param);
                } catch (ApiException | NoApiKeyException | UploadFileException e) {
                  throw new RuntimeException(e.getMessage());
                }
                System.out.println(JsonUtils.toJson(result));
              }

              public static void main(String[] args) {
                try {
                  basicCall();
                } catch (ApiException | NoApiKeyException | UploadFileException e) {
                  System.out.println(e.getMessage());
                }
              }
            }
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    Wan26TextToImageRequest:
      type: object
      description: wan2.6-t2i 模型的请求体，`input` 对象中使用 `messages` 格式。
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称。wan2.6-t2i 模型请填写 `wan2.6-t2i`。
          enum:
            - wan2.6-t2i
          example: wan2.6-t2i
        input:
          type: object
          description: 包含消息数组的输入对象。
          required:
            - messages
          properties:
            messages:
              type: array
              description: 请求内容数组，仅支持单轮对话（一组 role 和 content）。
              items:
                type: object
                required:
                  - role
                  - content
                properties:
                  role:
                    type: string
                    description: 消息角色，必须为 `user`。
                    enum:
                      - user
                  content:
                    type: array
                    description: 消息内容数组。
                    items:
                      type: object
                      required:
                        - text
                      properties:
                        text:
                          type: string
                          description: 正向提示词，描述生成图像的内容、风格和构图。支持中英文，最多 2,100 个字符。每次请求只允许一个 text。
                          example: A flower shop with exquisite windows, a beautiful wooden door, and flowers on display
        parameters:
          $ref: "#/components/schemas/Wan26Parameters"
    WanLegacyTextToImageRequest:
      type: object
      description: wan2.5 及更早版本模型的请求体，`input` 对象中使用 `prompt` 格式。**注意**：这些模型使用端点 `POST /services/aigc/text2image/image-synthesis`，而非主端点。
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称。支持以下模型：`wan2.5-t2i-preview`、`wan2.2-t2i-plus`、`wan2.2-t2i-flash`、`wan2.1-t2i-plus`、`wan2.1-t2i-turbo`。
          enum:
            - wan2.5-t2i-preview
            - wan2.2-t2i-plus
            - wan2.2-t2i-flash
            - wan2.1-t2i-plus
            - wan2.1-t2i-turbo
          example: wan2.5-t2i-preview
        input:
          type: object
          description: 包含提示词字符串的输入对象。
          required:
            - prompt
          properties:
            prompt:
              type: string
              description: 正向提示词，描述期望的图像内容。支持中英文。各模型最大长度不同：wan2.5-t2i-preview（2,000 字符）、wan2.2、wan2.1 系列（500 字符）。
              example: A flower shop with exquisite windows, a beautiful wooden door, and flowers on display
            negative_prompt:
              type: string
              description: 可选。描述不希望出现在图像中的内容。最多 500 字符，支持中英文。
              example: low resolution, low quality, deformed limbs
        parameters:
          $ref: "#/components/schemas/WanLegacyParameters"
    Wan26Parameters:
      type: object
      description: wan2.6-t2i 模型的参数。
      properties:
        negative_prompt:
          type: string
          description: 可选。描述不希望出现在图像中的内容，最多 500 字符，支持中英文。示例：低分辨率、低质量、肢体变形、手指变形、过度饱和、蜡质感、无面部细节、过度平滑、AI 感、构图混乱、文字模糊、文字扭曲。
        size:
          type: string
          description: 输出图像的分辨率，格式为 `宽*高`。默认值：`1280*1280`。总像素数须在 1280*1280 至 1440*1440 之间，宽高比须在 1:4 至 4:1 之间。推荐分辨率：1:1（1280*1280）、3:4（1104*1472）、4:3（1472*1104）、9:16（960*1696）、16:9（1696*960）。
          default: 1280*1280
          example: 1280*1280
        n:
          type: integer
          description: 生成图像的数量，取值范围 1 至 4，默认值 `4`。注意：按图计费（费用 = 单价 × 图像数量），测试时建议设为 1。
          minimum: 1
          maximum: 4
          default: 4
        prompt_extend:
          type: boolean
          description: |-
            是否开启提示词扩写。开启后，系统将使用大模型优化正向提示词，对较短提示词效果提升明显，但会增加几秒处理时间。默认值：`true`。

            注意：开启智能改写后，改写生成的提示词可能引入受版权保护的内容，从而触发内容审核，返回 `IPInfringementSuspect` 或 `DataInspectionFailed` 报错。遇到上述报错时，可将 `prompt_extend` 设置为 `false` 后重试。若提示词本身直接包含受版权保护的角色名或作品名，关闭智能改写仍会报错，需修改提示词本身。
          default: true
        watermark:
          type: boolean
          description: 是否在图像右下角添加 "AI 生成" 水印。默认值：`false`。
          default: false
        seed:
          type: integer
          description: 可选。随机数种子，取值范围 [0, 2147483647]。相同种子可获得更一致的结果，但不保证完全相同。不填时系统随机生成。
          minimum: 0
          maximum: 2147483647
    WanLegacyParameters:
      type: object
      description: wan2.5 及更早版本模型的参数。
      properties:
        size:
          type: string
          description: 输出图像的分辨率，格式为 `宽*高`。wan2.5-t2i-preview 默认为 `1280*1280`（总像素 1280*1280 至 1440*1440，宽高比 1:4 至 4:1）。wan2.2 及更早版本默认为 `1024*1024`（边长 512 至 1440，最大 1440*1440）。wan2.5 推荐分辨率：1:1（1280*1280）、3:4（1104*1472）、4:3（1472*1104）、9:16（960*1696）、16:9（1696*960）。
          example: 1280*1280
        n:
          type: integer
          description: 生成图像的数量，取值范围 1 至 4，默认值 `4`。注意：按图计费（费用 = 单价 × 图像数量），测试时建议设为 1。
          minimum: 1
          maximum: 4
          default: 4
        prompt_extend:
          type: boolean
          description: |-
            是否开启提示词扩写。开启后，系统将使用大模型优化正向提示词，对较短提示词效果提升明显，但会增加几秒处理时间。默认值：`true`。

            注意：开启智能改写后，改写生成的提示词可能引入受版权保护的内容，从而触发内容审核，返回 `IPInfringementSuspect` 或 `DataInspectionFailed` 报错。遇到上述报错时，可将 `prompt_extend` 设置为 `false` 后重试。若提示词本身直接包含受版权保护的角色名或作品名，关闭智能改写仍会报错，需修改提示词本身。
          default: true
        watermark:
          type: boolean
          description: 是否在图像右下角添加 "AI 生成" 水印。默认值：`false`。
          default: false
        seed:
          type: integer
          description: 可选。随机数种子，取值范围 [0, 2147483647]。相同种子可获得更一致的结果，但不保证完全相同。不填时系统随机生成。
          minimum: 0
          maximum: 2147483647
    Wan26SyncResponse:
      type: object
      description: wan2.6-t2i 模型的同步响应。
      example:
        output:
          choices:
            - finish_reason: stop
              message:
                content:
                  - image: https://dashscope-463f.oss-accelerate.aliyuncs.com/xxxx.png?Expires=xxx
                    type: image
                role: assistant
          finished: true
        usage:
          image_count: 1
          input_tokens: 0
          output_tokens: 0
          size: 1280*1280
          total_tokens: 0
        request_id: 815505c6-7c3d-49d7-b197-xxxxxx
      properties:
        output:
          type: object
          properties:
            choices:
              type: array
              description: 生成结果列表。
              items:
                type: object
                properties:
                  finish_reason:
                    type: string
                    description: "`stop` 表示正常完成。"
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
                        description: 包含生成图像 URL 的响应内容数组。
                        items:
                          type: object
                          properties:
                            image:
                              type: string
                              description: 生成图像的 URL（PNG 格式）。**有效期 24 小时**，请及时下载。
                            type:
                              type: string
                              description: 内容类型，始终为 `image`。
                              enum:
                                - image
            finished:
              type: boolean
              description: 生成是否已完成。
        usage:
          type: object
          description: 用量统计信息。
          properties:
            image_count:
              type: integer
              description: 已生成的图像数量。
            input_tokens:
              type: integer
              description: 输入 token 数量，当前固定为 0。
            output_tokens:
              type: integer
              description: 输出 token 数量，当前固定为 0。
            size:
              type: string
              description: 生成图像的分辨率。
            total_tokens:
              type: integer
              description: 消耗的 token 总量，当前固定为 0。
        request_id:
          type: string
          description: 唯一请求标识符，用于追踪和问题排查。
    AsyncTaskSubmitResponse:
      type: object
      description: 异步任务创建成功后返回的响应。
      properties:
        request_id:
          type: string
          description: 唯一请求标识符，用于问题排查。
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务标识符。可通过 `GET /tasks/{task_id}` 查询任务状态，有效期 24 小时。
            task_status:
              type: string
              description: 任务初始状态，通常为 `PENDING`。
              enum:
                - PENDING
    TaskStatusResponse:
      type: object
      description: 查询任务状态时返回的响应，输出格式取决于所用模型。
      properties:
        request_id:
          type: string
          description: 唯一请求标识符，用于问题排查。
        output:
          type: object
          description: 任务输出信息。
          properties:
            task_id:
              type: string
              description: 任务标识符。
            task_status:
              type: string
              description: 当前任务状态。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - CANCELLED
            choices:
              type: array
              description: 输出内容（wan2.6-t2i 格式），当 task_status 为 SUCCEEDED 时返回。
              items:
                type: object
                properties:
                  finish_reason:
                    type: string
                    description: 任务停止原因，`stop` 表示正常完成。
                  message:
                    type: object
                    properties:
                      role:
                        type: string
                        description: 角色，始终为 `assistant`。
                      content:
                        type: array
                        items:
                          type: object
                          properties:
                            image:
                              type: string
                              description: 生成图像的 URL，有效期 24 小时。
                            type:
                              type: string
                              description: 内容类型，始终为 `image`。
            results:
              type: array
              description: 输出内容（wan2.5 及更早版本格式），当 task_status 为 SUCCEEDED 时返回。
              items:
                type: object
                properties:
                  url:
                    type: string
                    description: 生成图像的 URL，有效期 24 小时。
                  orig_prompt:
                    type: string
                    description: 原始输入提示词。
                  actual_prompt:
                    type: string
                    description: 生成时实际使用的优化后提示词（仅在开启提示词扩写时返回）。
                  code:
                    type: string
                    description: 错误码（仅当单张图像生成失败时返回）。
                  message:
                    type: string
                    description: 错误信息（仅当单张图像生成失败时返回）。
            finished:
              type: boolean
              description: 任务是否已完成（wan2.6 格式）。
            submit_time:
              type: string
              description: 任务提交时间。
            scheduled_time:
              type: string
              description: 任务调度时间。
            end_time:
              type: string
              description: 任务完成时间。
            task_metrics:
              type: object
              description: 任务结果统计信息。
              properties:
                TOTAL:
                  type: integer
                  description: 任务总数。
                SUCCEEDED:
                  type: integer
                  description: 成功任务数。
                FAILED:
                  type: integer
                  description: 失败任务数。
            code:
              type: string
              description: 错误码（仅当任务失败时返回）。
            message:
              type: string
              description: 错误信息（仅当任务失败时返回）。
        usage:
          type: object
          description: 用量统计信息，仅统计成功结果。
          properties:
            image_count:
              type: integer
              description: 成功生成的图像数量。计费公式：费用 = 图像数量 × 单价。
            size:
              type: string
              description: 生成图像的分辨率。
            input_tokens:
              type: integer
              description: 输入 token 数量（wan2.6 格式）。
            output_tokens:
              type: integer
              description: 输出 token 数量（wan2.6 格式）。
            total_tokens:
              type: integer
              description: Token 总量（wan2.6 格式）。
    DashScopeErrorResponse:
      type: object
      description: 请求失败时返回的错误响应。
      properties:
        code:
          type: string
          description: 错误码。
        message:
          type: string
          description: 详细错误信息。
        request_id:
          type: string
          description: 唯一请求 ID，用于问题排查。
````

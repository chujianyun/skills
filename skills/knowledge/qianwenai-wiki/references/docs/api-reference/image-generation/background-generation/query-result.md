> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 图像背景生成 — 查询结果

> 查询图像背景生成任务的状态和结果

<Note>
  请先[获取 API Key](/api-reference/preparation/api-key) 并[设置为环境变量](/api-reference/preparation/export-api-key-env)。
</Note>

## OpenAPI

````yaml get /tasks/{task_id}
openapi: 3.1.0
info:
  title: 图像背景生成 API
  description: 本文介绍Wan-背景生成模型的输入输出参数。Wan-图像背景生成模型为主体商品生成背景图，适用于电商和海报场景。支持多种背景生成方法：文本引导、图像引导、文本与图像结合引导，以及文本、图像与边缘引导元素的综合应用。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 中国内地（北京）
security:
  - BearerAuth: []
paths:
  /tasks/{task_id}:
    get:
      operationId: getBackgroundGenerationTaskStatus
      summary: 根据任务ID查询结果
      description: 轮询背景生成任务的状态及结果。持续轮询直到 task_status 变为 SUCCEEDED 或 FAILED。任务数据（如任务状态、图像 URL 等）仅保留 24 小时，超时后会被自动清除，请及时保存生成的图像。
      parameters:
        - name: Authorization
          in: header
          required: true
          description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
          schema:
            type: string
        - name: task_id
          in: path
          required: true
          description: 创建任务接口返回的任务 ID。
          schema:
            type: string
          example: 86ecf553-d340-4e21-xxxxxxxxx
      responses:
        "200":
          description: 成功获取任务状态
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/TaskStatusResponse"
              examples:
                SUCCEEDED:
                  summary: 任务执行成功
                  value:
                    request_id: ded2407a-ec61-4a7d-adc0-xxxxxxxxxxxx
                    output:
                      task_id: 86ecf553-d340-4e21-xxxxxxxxx
                      task_status: SUCCEEDED
                      submit_time: 2025-12-23 10:25:26.436
                      scheduled_time: 2025-12-23 10:25:26.471
                      end_time: 2025-12-23 10:26:06.390
                      results:
                        - url: https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx.png?Expires=xxx
                        - url: https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx.png?Expires=xxx
                        - url: https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx.png?Expires=xxx
                        - url: https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx.png?Expires=xxx
                      task_metrics:
                        TOTAL: 4
                        SUCCEEDED: 4
                        FAILED: 0
                    usage:
                      image_count: 4
                FAILED:
                  summary: 任务执行失败
                  value:
                    request_id: dccfdf23-b38e-97a6-a07b-f35118c1ada6
                    output:
                      task_id: 4cbabbdf-2c1f-43f4-b983-c2cc47f4c115
                      task_status: FAILED
                      submit_time: 2024-05-16 14:15:14.103
                      scheduled_time: 2024-05-16 14:15:14.154
                      end_time: 2024-05-16 14:15:14.694
                      code: InvalidParameter.FileDownload
                      message: download for input_image error
                RUNNING:
                  summary: 任务执行中
                  value:
                    request_id: e5d70b02-ebd3-98ce-9fe8-xxxxxxxxxxxx
                    output:
                      task_id: 13b1848b-5493-4c0e-xxxxxxxxxxxx
                      task_status: RUNNING
                      task_metrics:
                        TOTAL: 1
                        SUCCEEDED: 1
                        FAILED: 0
        "400":
          description: 请求参数无效
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
      x-codeSamples:
        - lang: curl
          label: cURL — 查询任务结果
          source: |-
            # 将 {task_id} 替换为创建任务接口返回的真实 task_id
            curl -X GET 'https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY"
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    BackgroundGenerationRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称。当前仅支持填写 wanx-background-generation-v2。通过 parameters.model_version 参数切换 v2/v3 版本，请勿将 model 设置为 wanx-background-generation-v3。
          enum:
            - wanx-background-generation-v2
          example: wanx-background-generation-v2
        input:
          type: object
          required:
            - base_image_url
          description: 输入图像的基本信息。ref_image_url 和 ref_prompt 至少需要填写一个。
          properties:
            base_image_url:
              type: string
              format: uri
              description: 主体图像 URL。主体图像必须为带透明背景的 RGBA 四通道 PNG 图像，输出图像的分辨率与该图像保持一致。图像长边不超过 2048 像素。
              example: https://vision-poster.oss-cn-shanghai.aliyuncs.com/lllcho.lc/data/test_data/images/main_images/new_main_img/a.png
            ref_image_url:
              type: string
              format: uri
              description: 引导图像 URL。用于引导背景风格。与 ref_prompt 至少需要填写一个。支持 jpg、png、webp 等常见格式。引导图像可以是 RGB 图像或带透明背景的 RGBA 图像。
              example: http://vision-poster.oss-cn-shanghai.aliyuncs.com/lllcho.lc/data/test_data/images/ref_images/c5e50d27be534709817b2ab080b0162f_0.jpg
            ref_prompt:
              type: string
              description: 引导文本提示词，支持中英双语。与 ref_image_url 至少需要填写一个。英文最多支持 150 个单词，中文约 100-120 个中文字符，超过部分会被自动忽略。示例：山脉和晚霞。
              example: 山脉和晚霞
            neg_ref_prompt:
              type: string
              description: 负向提示词，描述画面不希望出现的内容。一般不填，使用模型内置的默认值。英文最多支持 150 个单词，中文约 100-120 个中文字字符。示例：低质量的，模糊的，错误的。
            reference_edge:
              type: object
              description: 边缘引导元素图像，包括前景元素图像列表和背景元素图像列表。
              properties:
                foreground_edge:
                  type: array
                  items:
                    type: string
                    format: uri
                  description: 前景元素图像 URL 列表。每个图像必须为带透明背景的 RGBA 四通道图像，分辨率和主体图像相同。所有前景元素生成的图层在主体前面，可以对主体形成遮挡。foreground_edge 和 background_edge 图像列表之和不得超过 10。
                foreground_edge_prompt:
                  type: array
                  items:
                    type: string
                  description: 前景元素列表对应的 prompt 列表。如果输入该参数，长度必须和 foreground_edge 列表相等，且顺序一一对应。无需填写某个元素的 prompt 时，可用空字符串占位。
                background_edge:
                  type: array
                  items:
                    type: string
                    format: uri
                  description: 背景元素图像 URL 列表。每个图像必须为带透明背景的 RGBA 四通道图像。生成图层在主体的后面，如果重叠会被主体遮挡。foreground_edge 和 background_edge 图像列表之和不得超过 10。
                background_edge_prompt:
                  type: array
                  items:
                    type: string
                  description: 背景元素列表对应的 prompt 列表。如果输入该参数，长度必须和 background_edge 列表相等，且顺序一一对应。无需填写某个元素的 prompt 时，可用空字符串占位。
            title:
              type: string
              deprecated: true
              description: 已废弃，建议使用图配文。图像上添加文字主标题，算法自动确定文字的大小和位置，限制 1-8 个字符。
              minLength: 1
              maxLength: 8
            sub_title:
              type: string
              deprecated: true
              description: 已废弃，建议使用图配文。图像上添加文字副标题，算法自动确定文字的大小和位置，限制 1-10 个字符。仅当 title 不为空时生效。
              minLength: 1
              maxLength: 10
        parameters:
          type: object
          description: 图像处理参数。
          properties:
            n:
              type: integer
              description: 图片生成的数量，支持 1-4 张，默认值 1。
              minimum: 1
              maximum: 4
              default: 1
              example: 4
            model_version:
              type: string
              description: 模型版本。v2：旧版模型，速度快（默认值）。v3：新版模型，速度稍慢但效果更好，推荐切换到 v3。
              enum:
                - v2
                - v3
              default: v2
              example: v3
            noise_level:
              type: integer
              description: 当 ref_image_url 不为空时生效。该参数在图像引导的过程中添加随机变化，数值越大生成背景与引导图像的相关性越低。默认值 300，取值范围 [0, 999]。
              minimum: 0
              maximum: 999
              default: 300
            ref_prompt_weight:
              type: number
              description: 仅当 ref_image_url 和 ref_prompt 同时输入时生效，表示引导文本 prompt 的权重。取值范围 [0, 1]，默认值 0.5。数值越大表示引导文本对生成背景的影响程度越大。
              minimum: 0
              maximum: 1
              default: 0.5
              example: 0.5
            scene_type:
              type: string
              deprecated: true
              description: 已废弃，不建议使用。使用场景：GENERAL（通用场景，默认值）、ROOM（室内家居场景）、COSMETIC（美妆场景，也适用于大部分小商品摆放场景）。
              enum:
                - GENERAL
                - ROOM
                - COSMETIC
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
              description: 任务 ID。用于查询任务状态及结果，查询有效期 24 小时。
              example: 0385dc79-5ff8-4d82-bcb6-xxxxxx
            task_status:
              type: string
              description: 任务状态。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - CANCELED
                - UNKNOWN
    TaskStatusResponse:
      type: object
      description: 任务状态轮询响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识。可用于请求明细溯源和问题排查。
          example: ded2407a-ec61-4a7d-adc0-xxxxxxxxxxxx
        output:
          type: object
          description: 任务输出信息。
          properties:
            task_id:
              type: string
              description: 任务 ID。查询有效期 24 小时。
              example: 86ecf553-d340-4e21-xxxxxxxxx
            task_status:
              type: string
              description: 任务状态。
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
              example: 2025-12-23 10:25:26.436
            scheduled_time:
              type: string
              description: 任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。
              example: 2025-12-23 10:25:26.471
            end_time:
              type: string
              description: 任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。
              example: 2025-12-23 10:26:06.390
            results:
              type: array
              description: 返回结果图像。仅在 task_status 为 SUCCEEDED 时返回。图像分辨率与输入图像（base_image_url）保持一致。
              items:
                type: object
                properties:
                  url:
                    type: string
                    format: uri
                    description: 生成图像的 URL。有效期 24 小时，请及时下载保存。
                    example: https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx.png?Expires=xxx
            code:
              type: string
              description: 错误码。仅在 task_status 为 FAILED 时返回。
              example: InvalidParameter.FileDownload
            message:
              type: string
              description: 错误详情。仅在 task_status 为 FAILED 时返回。
              example: download for input_image error
            task_metrics:
              type: object
              description: 任务结果统计。
              properties:
                TOTAL:
                  type: integer
                  description: 总的任务数。
                  example: 4
                SUCCEEDED:
                  type: integer
                  description: 任务状态为成功的任务数。
                  example: 4
                FAILED:
                  type: integer
                  description: 任务状态为失败的任务数。
                  example: 0
        usage:
          type: object
          description: 输出信息统计。计费公式：费用 = 图片数量 × 单价。
          properties:
            image_count:
              type: integer
              description: 模型成功生成图片的数量。
              example: 4
    DashScopeErrorResponse:
      type: object
      description: DashScope API 错误响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识。
          example: fb53c4ec-1c12-4fc4-a580-xxxxxx
        code:
          type: string
          description: 请求失败的错误码。请求成功时不会返回此参数。
          example: InvalidApiKey
        message:
          type: string
          description: 请求失败的详细信息。请求成功时不会返回此参数。
          example: Invalid API-key provided.
````

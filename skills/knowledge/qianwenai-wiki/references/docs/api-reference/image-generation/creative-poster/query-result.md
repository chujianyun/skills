> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 创意海报 — 查询结果

> 查询创意海报生成任务状态

查询任务状态并获取生成的海报图片。

## 轮询策略

1. 通过[生成海报](/api-reference/image-generation/creative-poster/create-task)接口提交任务，获取 `task_id`。
2. 每 **5 秒**轮询一次，直到 `task_status` 为 `SUCCEEDED` 或 `FAILED`。
3. 任务成功后，从响应中获取海报图片。

## 响应字段说明

任务成功后，响应中包含以下字段：

| 字段                     | 说明                             |
| ---------------------- | ------------------------------ |
| `render_urls`          | 渲染后的海报图片 URL 列表                |
| `bg_urls`              | 背景图片 URL 列表                    |
| `auxiliary_parameters` | 辅助参数列表，用于 `sr` 或 `hrf` 模式的二次生成 |

## 注意事项

- **URL 有效期**：生成的图片 URL 有效期为 **24 小时**，请及时下载。
- **任务状态流转**：`PENDING` → `RUNNING` → `SUCCEEDED`、`FAILED` 或 `SUSPENDED`。
- **任务 ID 有效期**：`task_id` 有效期为 24 小时，过期后无法查询状态和结果。
- **避免重复提交**：请通过轮询获取结果，不要重复提交请求。

## 错误码

| HTTP 状态码 | 错误码              | 错误信息                   | 含义          |
| -------- | ---------------- | ---------------------- | ----------- |
| 400      | InvalidParameter | check input data style | 输入参数不满足入参要求 |
| 500      | InternalError    | inference error        | 算法内部错误      |

## 常见问题

**Q：创意海报生成需要多长时间？**

A：生成时间一般为 20\~60 秒，受排队情况影响可能有所延迟。建议以 5 秒为间隔轮询查询接口，避免频繁请求。

**Q：`render_urls` 和 `bg_urls` 有什么区别？**

A：`render_urls` 是包含文字排版的完整海报图片；`bg_urls` 是不含文字的背景图片，可用于后续二次编辑。

## OpenAPI

````yaml get /tasks/{task_id}
openapi: 3.1.0
info:
  title: Creative Poster Generation API
  version: 1.0.0
  description: 创意海报生成 API
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: DashScope
security:
  - BearerAuth: []
paths:
  /tasks/{task_id}:
    get:
      summary: 查询海报生成结果
      operationId: getCreativePosterTaskResult
      parameters:
        - name: task_id
          in: path
          required: true
          schema:
            type: string
          description: 任务 ID，由[生成海报](/api-reference/image-generation/creative-poster/create-task)接口返回。
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
                    request_id: b67df059-ca6a-9d51-afcd-9b3c4456b1e2
                    output:
                      task_id: d76ec1e8-ea27-4038-8913-235c88ef0f70
                      task_status: SUCCEEDED
                      submit_time: 2024-05-16 13:50:01.247
                      scheduled_time: 2024-05-16 13:50:01.354
                      end_time: 2024-05-16 13:50:27.795
                      render_urls:
                        - http://vision-poster.oss-cn-shanghai.aliyuncs.com/xxxxxx
                      auxiliary_parameters:
                        - xxxxxx
                      bg_urls:
                        - http://vision-poster.oss-cn-shanghai.aliyuncs.com/xxxxxx
                    usage:
                      image_count: 1
                FAILED:
                  summary: 任务失败
                  value:
                    request_id: dccfdf23-b38e-97a6-a07b-f35118c1ada6
                    output:
                      task_id: 4cbabbdf-2c1f-43f4-b983-c2cc47f4c115
                      task_status: FAILED
                      submit_time: 2024-05-16 14:15:14.103
                      scheduled_time: 2024-05-16 14:15:14.154
                      end_time: 2024-05-16 14:15:14.694
                      code: InvalidParameter
                      message: check input data style
                RUNNING:
                  summary: 任务运行中
                  value:
                    request_id: e5d70b02-ebd3-98ce-9fe8-759d7d7b107d
                    output:
                      task_id: 86ecf553-d340-4e21-af6e-a0c6a421c010
                      task_status: RUNNING
                      task_metrics:
                        TOTAL: 1
                        SUCCEEDED: 1
                        FAILED: 0
                PENDING:
                  summary: 任务排队中
                  value:
                    request_id: 7574ee8f-38a3-4b1e-9280-11c33ab46e51
                    output:
                      task_id: d76ec1e8-ea27-4038-8913-xxxxxxxxxxxx
                      task_status: PENDING
      x-codeSamples:
        - lang: curl
          label: 查询任务结果
          source: |-
            curl --location --request GET 'https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY"
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    CreativePosterRequest:
      type: object
      required:
        - model
        - input
        - parameters
      properties:
        model:
          type: string
          enum:
            - wanx-poster-generation-v1
          description: 模型名称。
        input:
          type: object
          required:
            - generate_mode
            - title
          description: 输入参数。
          properties:
            generate_mode:
              type: string
              enum:
                - generate
                - sr
                - hrf
              description: 生成模式。`generate`：默认生成模式；`sr`：超分辨率模式，需要传入 `auxiliary_parameters`（由 generate 模式返回）；`hrf`：高分辨率修复模式，需要传入 `auxiliary_parameters`（由 generate 模式返回）。
            title:
              type: string
              maxLength: 30
              description: 海报主标题，最多 30 个字符。
            sub_title:
              type: string
              maxLength: 30
              description: 海报副标题，最多 30 个字符。
            body_text:
              type: string
              maxLength: 50
              description: 海报正文内容，最多 50 个字符。
            prompt_text_zh:
              type: string
              description: 中文关键词，用于描述海报背景。
            prompt_text_en:
              type: string
              description: 英文关键词，用于描述海报背景。
            wh_ratios:
              type: string
              enum:
                - 横版
                - 竖版
              description: 海报版式。`横版`：横版海报；`竖版`：竖版海报。
            lora_name:
              type: string
              enum:
                - 2D插画1
                - 2D插画2
                - 浩瀚星云
                - 浓郁色彩
                - 光线粒子
                - 透明玻璃
                - 剪纸工艺
                - 折纸工艺
                - 中国水墨
                - 中国刺绣
                - 真实场景
                - 2D卡通
                - 儿童水彩
                - 赛博背景
                - 浅蓝抽象
                - 深蓝抽象
                - 抽象点线
                - 童话油画
              description: 海报风格。
            lora_weight:
              type: number
              minimum: 0
              maximum: 1
              default: 0.8
              description: 风格权重，取值范围 0~1，默认 0.8。
            ctrl_ratio:
              type: number
              minimum: 0
              maximum: 1
              default: 0.7
              description: 控制比例，取值范围 0~1，默认 0.7。
            ctrl_step:
              type: number
              minimum: 0
              maximum: 1
              default: 0.7
              description: 控制步长，取值范围 0~1，默认 0.7。
            generate_num:
              type: integer
              minimum: 1
              maximum: 4
              description: 生成图片数量，取值范围 1~4。
            auxiliary_parameters:
              type: string
              description: 辅助参数，在 `sr` 或 `hrf` 模式下必传。该值由 `generate` 模式的任务结果返回。
            creative_title_layout:
              type: boolean
              default: false
              description: 是否使用创意标题排版，默认 false。
        parameters:
          type: object
          description: 模型参数，传空对象 `{}`。
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
                - SUSPENDED
                - SUCCEEDED
                - FAILED
              description: 任务状态。
            submit_time:
              type: string
              description: 任务提交时间。
            scheduled_time:
              type: string
              description: 任务调度时间。
            end_time:
              type: string
              description: 任务结束时间。
            render_urls:
              type: array
              items:
                type: string
              description: 渲染后的海报图片 URL 列表。
            auxiliary_parameters:
              type: array
              items:
                type: string
              description: 辅助参数列表，用于 `sr` 或 `hrf` 模式的二次生成。
            bg_urls:
              type: array
              items:
                type: string
              description: 背景图片 URL 列表。
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

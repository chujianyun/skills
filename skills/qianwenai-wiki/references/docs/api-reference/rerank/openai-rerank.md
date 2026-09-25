> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# OpenAI 兼容重排序

> OpenAI 兼容的重排序 API

使用 qwen3-rerank 根据语义相关性对文档进行重排序。

<Note>
  调用 API 前，请先[获取 API Key](/api-reference/preparation/api-key) 并[设置为环境变量](/api-reference/preparation/export-api-key-env)。如果使用 OpenAI SDK，请先[安装 SDK](/api-reference/preparation/install-sdk)。
</Note>

**支持的模型**： 仅支持 qwen3-rerank。

## 接入点

- HTTP：`POST https://dashscope.aliyuncs.com/compatible-api/v1/reranks`
- SDK `base_url`：`https://dashscope.aliyuncs.com/compatible-api/v1`

## 模型概览

| 模型           | 最大文档数 | 单文档最大 Token 数 | 请求最大 Token 数 | 支持语言     | 适用场景       |
| ------------ | ----- | ------------- | ------------ | -------- | ---------- |
| qwen3-rerank | 500   | 4,000         | 120,000      | 100+ 种语言 | 文本语义搜索、RAG |

关于模型计费，请参见[模型市场](https://www.qianwenai.com/models)。

**参数说明**：

- **单文档最大 Token 数**：单条查询或文档允许的最大 Token 数量。超出此限制的内容将被截断，可能影响排序准确性。
- **最大文档数**：单次请求允许的最大文档数量。
- **请求最大 Token 数**：计算公式为 `查询 Token 数 x 文档数量 + 所有文档 Token 总数`，不得超过此限制。

## OpenAPI

````yaml post /reranks
openapi: 3.1.0
info:
  title: 千问AI平台 Reranking API
  description: 对召回文档按语义相关度重新排序，提升 RAG 和检索系统的搜索精准度。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/compatible-api/v1
    description: 北京
security:
  - BearerAuth: []
paths:
  /reranks:
    post:
      operationId: createTextRerank
      summary: OpenAI compatible
      description: |-
        使用 qwen3-rerank 对文档按语义相关度重新排序。采用扁平请求结构，`query`、`documents`、`top_n`、`instruct` 均位于请求体顶层。

        > 不同模型使用不同的 API 接口：**qwen3-rerank** 使用此接口（`/compatible-api/v1/reranks`）；**qwen3-vl-rerank** 和 **gte-rerank-v2** 使用 DashScope 接口（`/api/v1/services/rerank/text-rerank/text-rerank`）。
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/TextRerankRequest"
      responses:
        "200":
          description: 重排序结果
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/TextRerankResponse"
        "400":
          description: 请求参数无效
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
        "401":
          description: 鉴权失败 — API Key 无效或缺失
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
        "429":
          description: 请求频率超出限制
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
      x-codeSamples:
        - lang: bash
          label: qwen3-rerank
          source: |-
            curl --request POST \
              --url https://dashscope.aliyuncs.com/compatible-api/v1/reranks \
              --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
              --header "Content-Type: application/json" \
              --data '{
                    "model": "qwen3-rerank",
                    "documents": [
                            "Rerank models are widely used in search engines and recommendation systems. They sort candidate documents based on text relevance.",
                            "Quantum computing is a cutting-edge field of computer science.",
                            "The development of pre-trained language models has brought new advancements to rerank models."
                    ],
                    "query": "What is a rerank model?",
                    "top_n": 2,
                    "instruct": "Given a web search query, retrieve relevant passages that answer the query."
            }'
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    TextRerankRequest:
      type: object
      required:
        - model
        - query
        - documents
      properties:
        model:
          type: string
          enum:
            - qwen3-rerank
            - qwen3-vl-rerank
            - gte-rerank-v2
          description: 模型名称。可选值：`qwen3-rerank`、`qwen3-vl-rerank`、`gte-rerank-v2`（将于 2026-05-30 下线，推荐使用 qwen3-rerank）。
          example: qwen3-rerank
        query:
          type: string
          description: 查询文本。最大 4,000 个 token。
          example: What is a reranking model
        documents:
          type: array
          items:
            type: string
          description: 待排序的文档列表，字符串数组。最多 500 篇文档。
          example:
            - Reranking models are widely used in search engines and recommendation systems to sort candidates by relevance
            - Quantum computing is a frontier field of computer science
            - The development of pre-trained language models has brought new advances to reranking
        top_n:
          type: integer
          minimum: 1
          description: 仅返回得分最高的前 N 个结果。默认返回全部文档。
          example: 2
        instruct:
          type: string
          description: 自定义排序任务指令，建议使用英文。默认行为为问答检索：`"Given a web search query, retrieve relevant passages that answer the query."`
          example: Given a web search query, retrieve relevant passages that answer the query.
    DashScopeRerankRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          enum:
            - qwen3-vl-rerank
            - gte-rerank-v2
          description: 模型名称。可选值：`qwen3-vl-rerank`、`gte-rerank-v2`（将于 2026-05-30 下线，推荐使用 qwen3-rerank）。
          example: qwen3-vl-rerank
        input:
          type: object
          required:
            - query
            - documents
          description: 输入数据，包含查询和待排序文档。
          properties:
            query:
              oneOf:
                - type: string
                - type: object
              description: '查询内容。最大 4,000 个 token。字符串格式或对象格式（`qwen3-vl-rerank` 支持 `{"text": "..."}` 或 `{"image": "URL"}`）。'
              example: What is a reranking model
            documents:
              type: array
              items:
                oneOf:
                  - type: string
                  - type: object
              description: 待排序的文档列表。`gte-rerank-v2` 使用字符串数组；`qwen3-vl-rerank` 使用对象数组，支持 `text`、`image`、`video` 三种模态。最多 100 篇文档（`qwen3-vl-rerank`）或 500 篇文档（`gte-rerank-v2`）。
        parameters:
          type: object
          description: 重排序请求的配置参数，需封装在此 `parameters` 对象中。
          properties:
            top_n:
              type: integer
              minimum: 1
              description: 仅返回得分最高的前 N 个结果。默认返回全部文档。
              example: 2
            return_documents:
              type: boolean
              default: false
              description: 是否在结果中返回原始文档内容。默认值：`false`。支持的模型：`gte-rerank-v2`、`qwen3-vl-rerank`。
              example: true
            instruct:
              type: string
              description: 自定义排序任务指令，建议使用英文。仅 `qwen3-vl-rerank` 支持。默认行为为问答检索：`"Given a web search query, retrieve relevant passages that answer the query."`
              example: Given a web search query, retrieve relevant passages that answer the query.
            fps:
              type: number
              format: float
              description: 仅 `qwen3-vl-rerank` 支持。控制视频的帧采样比例，范围为 [0, 1]。默认值：`1.0`。值越小，实际抽取的帧数越少。
              default: 1
              example: 1
    TextRerankResponse:
      type: object
      properties:
        id:
          type: string
          description: 请求的唯一标识符。
        object:
          type: string
          description: 对象类型。固定值为 `list`。
          example: list
        model:
          type: string
          description: 本次重排序使用的模型。
          example: qwen3-rerank
        results:
          type: array
          description: 排序结果，按 `relevance_score` 从高到低排列。
          items:
            $ref: "#/components/schemas/RerankResult"
        usage:
          type: object
          description: Token 用量统计。
          properties:
            total_tokens:
              type: integer
              description: 本次请求消耗的 token 总数。
    DashScopeRerankResponse:
      type: object
      properties:
        output:
          type: object
          description: 输出包装对象，包含排序结果。
          properties:
            results:
              type: array
              description: 排序结果，按 `relevance_score` 从高到低排列。
              items:
                $ref: "#/components/schemas/RerankResult"
        usage:
          type: object
          description: Token 用量统计。
          properties:
            total_tokens:
              type: integer
              description: 本次请求消耗的 token 总数。
        request_id:
          type: string
          description: 请求的唯一标识符。
          example: 85ba5752-1900-47d2-8896-23f99b13f6e1
    RerankResult:
      type: object
      properties:
        document:
          type: object
          description: 原始文档内容。仅当 `return_documents` 为 `true` 时返回。
          properties:
            text:
              type: string
              description: 文档的文本内容。
        index:
          type: integer
          description: 该文档在输入 `documents` 列表中的原始位置索引。
          example: 0
        relevance_score:
          type: number
          format: double
          description: 相关度评分，范围 0.0 到 1.0，分值越高表示相关性越强。该分值为本次请求的相对分数，不可跨请求比较。
          example: 0.9334521178273196
    ErrorResponse:
      type: object
      properties:
        error:
          type: object
          properties:
            message:
              type: string
              description: 错误信息。
            type:
              type: string
              description: 错误类型。
            code:
              type: string
              description: 错误码。
            param:
              type: string
              nullable: true
              description: 导致错误的参数名。
````

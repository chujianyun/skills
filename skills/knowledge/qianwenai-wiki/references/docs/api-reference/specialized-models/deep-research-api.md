> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Qwen-Deep-Research API 参考

> Qwen-Deep-Research 深入研究模型的输入与输出参数说明

<Note>
  - 模型当前仅支持通过 DashScope SDK（Python）和 HTTP API 调用，暂不支持 Java SDK 与 OpenAI 兼容接口。
  - 如需通过 HTTP 实现流式输出，请添加 `X-DashScope-SSE: enable` 请求头。
</Note>

## 调用流程

Qwen-Deep-Research 采用两步式调用流程：

1. **反问确认**：发送用户研究主题，模型返回澄清式问题帮助聚焦方向。
2. **深入研究**：将原始问题、模型反问、用户回答作为多轮对话发送，模型执行深度搜索并生成研究报告。

设置 `parameters.enable_feedback` 为 `false` 可跳过第一步，直接进入研究流程。

## 流式响应阶段

通过 `X-DashScope-SSE: enable` 请求头启用流式输出后，响应按以下阶段依次返回：

<CodeGroup>
  ```json 研究规划阶段
  {
    "output": {
      "message": {
        "phase": "ResearchPlanning",
        "role": "assistant",
        "content": "",
        "extra": { "deep_research": {} },
        "status": "typing"
      },
      "fininshed": false,
      "fininshed_reason": "null"
    },
    "usage": { "input_tokens": 694, "output_tokens": 0 }
  }
  ```

  ```json 网络搜索阶段
  {
    "output": {
      "message": {
        "phase": "WebResearch",
        "role": "assistant",
        "content": "",
        "extra": {
          "deep_research": {
            "query": {
              "researchGoal": "通过查找相关资料...",
              "query": "人工智能 教育 应用",
              "id": 1
            }
          }
        },
        "status": "streamingThinking"
      },
      "fininshed": false,
      "fininshed_reason": "null"
    },
    "usage": { "input_tokens": 694, "output_tokens": 0 }
  }
  ```

  ```json 连接保持阶段
  {
    "output": {
      "message": {
        "phase": "KeepAlive",
        "role": "assistant",
        "content": "",
        "extra": { "deep_research": {} },
        "status": "typing"
      },
      "fininshed": false,
      "fininshed_reason": "null"
    },
    "usage": { "input_tokens": 694, "output_tokens": 0 }
  }
  ```

  ```json 回答阶段
  {
    "output": {
      "message": {
        "phase": "answer",
        "role": "assistant",
        "content": "根据研究分析，人工智能在教育领域...",
        "extra": {
          "deep_research": {
            "references": [
              {
                "icon": "",
                "index_number": 1,
                "description": "AI 在个性化学习中的应用研究",
                "title": "人工智能与教育变革",
                "url": "https://example.com/ai-education"
              }
            ]
          }
        },
        "status": "typing"
      },
      "fininshed": false,
      "fininshed_reason": "null"
    },
    "usage": { "input_tokens": 694, "output_tokens": 128 }
  }
  ```
</CodeGroup>

## 模型版本差异

| 特性                    | qwen-deep-research                        | qwen-deep-research-2025-12-15 |
| --------------------- | ----------------------------------------- | ----------------------------- |
| `enable_feedback`     | 支持                                        | 支持                            |
| `research_tools`（MCP） | 不支持                                       | 支持                            |
| WebResearch 阶段 status | `streamingQueries` / `streamingWebResult` | `streamingThinking`（合并了前两者）   |

## OpenAPI

````yaml post /api/v1/services/aigc/text-generation/generation
openapi: 3.1.0
info:
  title: Qwen-Deep-Research API
  description: 通过 DashScope API 调用 Qwen-Deep-Research 深入研究模型。支持两步式调用流程（反问确认 + 深入研究）和流式输出。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com
    description: 北京
security:
  - ApiKeyAuth: []
paths:
  /api/v1/services/aigc/text-generation/generation:
    post:
      operationId: deepResearchGeneration
      summary: 深入研究
      description: |-
        向 Qwen-Deep-Research 模型发送研究主题并获取深度研究报告。支持两步式调用流程：

        1. **反问确认**：发送用户研究主题，模型返回澄清式问题帮助聚焦方向。
        2. **深入研究**：将原始问题、模型反问、用户回答作为多轮对话发送，模型执行深度搜索并生成研究报告。

        如需通过 HTTP 实现流式输出，请添加 `X-DashScope-SSE: enable` 请求头。设置 `parameters.enable_feedback` 为 `false` 可跳过反问确认阶段。
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/DeepResearchRequest"
            example:
              model: qwen-deep-research
              input:
                messages:
                  - role: user
                    content: 研究一下人工智能在教育中的应用
      responses:
        "200":
          description: 请求成功。流式输出时，每个 SSE 事件返回一个 JSON 对象。
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DeepResearchResponse"
              example:
                status_code: 200
                request_id: 2a6187f0-7e7b-40bb-a87e-xxx
                code: ""
                message: ""
                output:
                  text: null
                  finish_reason: null
                  choices: null
                  message:
                    phase: answer
                    role: assistant
                    content: 根据研究分析，人工智能在教育领域的应用主要体现在以下几个方面...
                    extra:
                      deep_research:
                        references:
                          - icon: ""
                            index_number: 1
                            description: AI 在个性化学习中的应用研究
                            title: 人工智能与教育变革
                            url: https://example.com/ai-education
                    status: typing
                  fininshed: false
                  fininshed_reason: "null"
                usage:
                  input_tokens: 694
                  output_tokens: 128
        "400":
          description: 请求参数无效
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DeepResearchError"
              example:
                status_code: 400
                request_id: a1b2c3d4-e5f6-7890-abcd-ef1234567890
                code: InvalidParameter
                message: The parameter 'model' is required.
        "401":
          description: 鉴权失败
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DeepResearchError"
              example:
                status_code: 401
                request_id: a1b2c3d4-e5f6-7890-abcd-ef1234567890
                code: InvalidApiKey
                message: Invalid API key provided.
        "429":
          description: 请求超过限流
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DeepResearchError"
              example:
                status_code: 429
                request_id: a1b2c3d4-e5f6-7890-abcd-ef1234567890
                code: Throttling
                message: Request was throttled.
      x-codeSamples:
        - lang: python
          label: 两步调用流程
          source: |-
            import os
            import dashscope

            # 第一步：模型反问确认
            messages = [{'role': 'user', 'content': '研究一下人工智能在教育中的应用'}]

            responses = dashscope.Generation.call(
              api_key=os.getenv('DASHSCOPE_API_KEY'),
              model='qwen-deep-research',
              messages=messages,
              stream=True
            )

            # 获取模型反问内容
            step1_content = ''
            for response in responses:
              if hasattr(response, 'output') and response.output:
                message = response.output.get('message', {})
                content = message.get('content', '')
                if content:
                  step1_content += content
                  print(content, end='', flush=True)

            # 第二步：深入研究
            messages = [
              {'role': 'user', 'content': '研究一下人工智能在教育中的应用'},
              {'role': 'assistant', 'content': step1_content},
              {'role': 'user', 'content': '我主要关注个性化学习和智能评估这两个方面'}
            ]

            responses = dashscope.Generation.call(
              api_key=os.getenv('DASHSCOPE_API_KEY'),
              model='qwen-deep-research',
              messages=messages,
              stream=True
            )

            for response in responses:
              if hasattr(response, 'output') and response.output:
                message = response.output.get('message', {})
                content = message.get('content', '')
                if content:
                  print(content, end='', flush=True)
        - lang: python
          label: 跳过反问确认
          source: |-
            import os
            import dashscope

            messages = [{'role': 'user', 'content': '研究一下人工智能在教育中的应用'}]

            responses = dashscope.Generation.call(
              api_key=os.getenv('DASHSCOPE_API_KEY'),
              model='qwen-deep-research',
              messages=messages,
              stream=True,
              enable_feedback=False  # <-- 跳过反问确认，直接进入研究
            )

            for response in responses:
              if hasattr(response, 'output') and response.output:
                message = response.output.get('message', {})
                content = message.get('content', '')
                if content:
                  print(content, end='', flush=True)
        - lang: curl
          label: 第一步：模型反问确认
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation' \
            --header 'X-DashScope-SSE: enable' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --header 'Content-Type: application/json' \
            --data '{
              "model": "qwen-deep-research",
              "input": {
                "messages": [
                  {
                    "role": "user",
                    "content": "研究一下人工智能在教育中的应用"
                  }
                ]
              }
            }'
        - lang: curl
          label: 第二步：深入研究
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation' \
            --header 'X-DashScope-SSE: enable' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --header 'Content-Type: application/json' \
            --data '{
              "model": "qwen-deep-research",
              "input": {
                "messages": [
                  {
                    "role": "user",
                    "content": "研究一下人工智能在教育中的应用"
                  },
                  {
                    "role": "assistant",
                    "content": "请告诉我您希望重点研究人工智能在教育中的哪些具体应用场景？"
                  },
                  {
                    "role": "user",
                    "content": "我主要关注个性化学习方面"
                  }
                ]
              }
            }'
        - lang: curl
          label: 跳过反问确认
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation' \
            --header 'X-DashScope-SSE: enable' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --header 'Content-Type: application/json' \
            --data '{
              "model": "qwen-deep-research",
              "input": {
                "messages": [
                  {
                    "role": "user",
                    "content": "研究一下人工智能在教育中的应用"
                  }
                ]
              },
              "parameters": {
                "enable_feedback": false
              }
            }'
        - lang: curl
          label: MCP 工具（仅 2025-12-15）
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation' \
            --header 'X-DashScope-SSE: enable' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --header 'Content-Type: application/json' \
            --data '{
              "model": "qwen-deep-research-2025-12-15",
              "input": {
                "messages": [
                  {
                    "role": "user",
                    "content": "研究一下人工智能在教育中的应用"
                  }
                ]
              },
              "parameters": {
                "enable_feedback": false,
                "research_tools": [
                  {
                    "type": "mcp",
                    "server_label": "my-knowledge-base",
                    "server_url": "https://your-mcp-server.example.com/sse",
                    "allowed_tools": ["search", "fetch"],
                    "authentication": {
                      "bearer": "your_jwt_token_here"
                    }
                  }
                ]
              }
            }'
components:
  securitySchemes:
    ApiKeyAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    DeepResearchRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称。
          enum:
            - qwen-deep-research
            - qwen-deep-research-2025-12-15
        input:
          type: object
          required:
            - messages
          description: 输入信息。
          properties:
            messages:
              type: array
              description: 传递给大模型的上下文，按对话顺序排列。
              items:
                $ref: "#/components/schemas/DeepResearchMessage"
        output_format:
          type: string
          description: |-
            指定输出研究报告的格式和详细程度。

            - `model_detailed_report`（默认）：结构完整、内容详尽的深度研究报告，篇幅约 6000 Token。
            - `model_summary_report`：核心观点突出、内容精炼的摘要式研究报告，篇幅约 1500-2000 Token。
          enum:
            - model_detailed_report
            - model_summary_report
          default: model_detailed_report
        parameters:
          $ref: "#/components/schemas/DeepResearchParameters"
    DeepResearchMessage:
      oneOf:
        - title: 用户消息
          type: object
          required:
            - role
            - content
          description: 用户消息，用于向模型传递研究主题或回答模型的澄清式问题。
          properties:
            role:
              type: string
              description: 固定为 `user`。
              enum:
                - user
            content:
              description: |-
                消息内容。支持两种格式：

                - **文本输入**：直接传入字符串。
                - **图片输入**：使用数组格式，包含 `{"image": "图片URL或Base64编码"}` 和 `{"text": "文本描述"}` 对象。支持 JPEG、PNG、BMP、WEBP 格式，单张不超过 10MB，单次请求最多 5 张图片。
              oneOf:
                - type: string
                  title: 文本输入
                - type: array
                  title: 图片+文本输入
                  items:
                    type: object
                    properties:
                      image:
                        type: string
                        description: 图片 URL 或 Base64 编码。
                      text:
                        type: string
                        description: 文本描述。
        - title: 助手消息
          type: object
          required:
            - role
          description: 模型对用户消息的回复。在第二步（深入研究）调用中，用于传入模型在第一步（反问确认）中返回的澄清式问题。
          properties:
            role:
              type: string
              description: 固定为 `assistant`。
              enum:
                - assistant
            content:
              type: string
              description: 消息内容。
    DeepResearchParameters:
      type: object
      description: 模型调用参数。
      properties:
        enable_feedback:
          type: boolean
          description: 是否启用反问确认。设为 `false` 可跳过反问确认阶段，模型将直接进入研究流程。默认为 `true`。两个模型均支持此参数。
          default: true
        research_tools:
          type: array
          description: MCP（Model Context Protocol）工具配置。通过此参数可接入外部 MCP Server，使模型在研究过程中调用指定工具进行信息检索。仅 `qwen-deep-research-2025-12-15` 模型支持。
          items:
            $ref: "#/components/schemas/ResearchTool"
    ResearchTool:
      type: object
      required:
        - type
        - server_label
        - server_url
        - allowed_tools
      description: 'MCP 工具配置对象。MCP Server 需实现 `search`（模糊搜索，输入 `{"query": "关键词"}`，返回 `results` 数组，最多 30 条，每条含 `id`/`title`/`description`）和 `fetch`（根据 ID 获取详情，返回 `resource` 对象，含 `id`/`title`/`markdown`，推荐 10 万字符以内）两种工具。'
      properties:
        type:
          type: string
          description: 工具类型，当前仅支持 `mcp`。
          enum:
            - mcp
        server_label:
          type: string
          description: MCP Server 标签，用于标识不同的 MCP 服务。
        server_url:
          type: string
          description: MCP Server 的服务地址。
        allowed_tools:
          type: array
          description: 允许调用的工具列表，如 `["search", "fetch"]`。
          items:
            type: string
        require_approval:
          type: boolean
          description: 是否开启鉴权。
        authentication:
          type: object
          description: 鉴权参数，支持 `bearer` 和 `oauth` 两种方式。
          properties:
            bearer:
              type: string
              description: Bearer Token（JWT）。
            oauth:
              type: object
              description: OAuth 鉴权参数。
    DeepResearchResponse:
      type: object
      description: 流式输出时，每个 SSE 事件返回的 JSON 对象。响应按阶段依次输出：ResearchPlanning（研究规划）→ WebResearch（网络搜索）→ KeepAlive（连接保持）→ answer（回答）。
      properties:
        status_code:
          type: integer
          description: 请求状态码。200 表示请求成功，否则表示请求失败。调用失败会抛出异常，异常信息为 `status_code` 和 `message` 的内容。
        request_id:
          type: string
          description: 本次调用的唯一标识符。
        code:
          type: string
          description: 错误码，调用成功时为空值。仅 Python SDK 返回该参数。
        message:
          type: string
          description: 错误提示信息，调用成功时为空值。
        output:
          $ref: "#/components/schemas/DeepResearchOutput"
        usage:
          $ref: "#/components/schemas/DeepResearchUsage"
    DeepResearchOutput:
      type: object
      description: 调用结果信息。
      properties:
        text:
          type: string
          nullable: true
          description: 当前固定为 `null`。
        finish_reason:
          type: string
          nullable: true
          description: 模型结束生成的原因。正在生成时为 `null`；模型输出自然结束为 `stop`；因生成长度过长而结束为 `length`。
          enum:
            - stop
            - length
        choices:
          type: array
          nullable: true
          description: 模型的输出信息。
          items:
            type: object
            properties:
              finish_reason:
                type: string
                nullable: true
                description: 正在生成时为 `null`；模型输出自然结束为 `stop`；因生成长度过长而结束为 `length`。
                enum:
                  - stop
                  - length
        message:
          $ref: "#/components/schemas/DeepResearchOutputMessage"
        fininshed:
          type: boolean
          description: 标识模型的内容流式输出是否已全部完成。输出中为 `false`，全部完成时为 `true`。注意：字段名为 `fininshed`，这是 API 返回的实际拼写。
        fininshed_reason:
          type: string
          nullable: true
          description: 标识模型的内容流式输出结束的原因。正在生成时为 `null`；自然结束为 `stop`。注意：字段名为 `fininshed_reason`，这是 API 返回的实际拼写。
    DeepResearchOutputMessage:
      type: object
      description: 模型输出的消息对象。
      properties:
        phase:
          type: string
          description: |-
            当前所处阶段。

            - `ResearchPlanning`：研究规划阶段
            - `WebResearch`：网络搜索阶段
            - `KeepAlive`：连接保持阶段
            - `answer`：反问确认与回答阶段
          enum:
            - ResearchPlanning
            - WebResearch
            - KeepAlive
            - answer
        role:
          type: string
          description: 输出消息的角色，固定为 `assistant`。
          enum:
            - assistant
        content:
          type: string
          description: 模型的输出内容。
        extra:
          type: object
          description: 模型获取的网络搜索与参考信息。
          properties:
            deep_research:
              $ref: "#/components/schemas/DeepResearchExtra"
        status:
          type: string
          description: |-
            模型输出过程中不同阶段的状态。

            - `typing`：正在生成该阶段内容
            - `finished`：阶段已完成
            - `streamingThinking`：正在拆解研究任务并总结网页内容（仅 `qwen-deep-research-2025-12-15`，替代 `streamingQueries` 和 `streamingWebResult`）
            - `streamingQueries`：正在生成研究目标和搜索查询（仅 `qwen-deep-research`）
            - `streamingWebResult`：正在执行搜索、网页阅读和代码执行（仅 `qwen-deep-research`）
            - `WebResultFinished`：单轮搜索结束
          enum:
            - typing
            - finished
            - streamingThinking
            - streamingQueries
            - streamingWebResult
            - WebResultFinished
    DeepResearchExtra:
      type: object
      description: 仅在 `answer` 与 `WebResearch` 阶段包含获取的网络搜索与参考信息，其余阶段均为空对象。
      properties:
        query:
          type: object
          description: 模型的研究过程与内容信息（仅 `WebResearch` 阶段）。
          properties:
            researchGoal:
              type: string
              description: 研究目标。
            query:
              type: string
              description: 研究过程中的搜索内容。
            id:
              type: integer
              description: 搜索的轮数，取值范围 [1-15]。
              minimum: 1
              maximum: 15
            learningMap:
              type: object
              description: 从调用工具总结获取到的内容，和调用工具相关联。
        references:
          type: array
          description: 模型生成答案所引用的内容（仅 `answer` 阶段）。
          items:
            $ref: "#/components/schemas/WebReference"
        webSites:
          type: array
          description: 模型研究过程中所参考的内容（仅 `WebResearch` 阶段）。
          items:
            $ref: "#/components/schemas/WebReference"
    WebReference:
      type: object
      description: 参考内容信息。
      properties:
        icon:
          type: string
          description: 参考内容 URL 的网页图标链接。
        index_number:
          type: integer
          description: 参考内容的索引。
        description:
          type: string
          description: 参考内容的简介。
        title:
          type: string
          description: 参考内容的网页标题。
        url:
          type: string
          description: 参考内容的网页 URL。
    DeepResearchUsage:
      type: object
      description: 本次请求使用的 Token 信息。
      properties:
        input_tokens:
          type: integer
          description: 输入 Token 数。
        output_tokens:
          type: integer
          description: 输出 Token 数。
    DeepResearchError:
      type: object
      description: 错误响应。
      properties:
        status_code:
          type: integer
          description: 错误状态码。
        request_id:
          type: string
          description: 请求唯一标识符。
        code:
          type: string
          description: 错误码。
        message:
          type: string
          description: 错误详细信息。
````

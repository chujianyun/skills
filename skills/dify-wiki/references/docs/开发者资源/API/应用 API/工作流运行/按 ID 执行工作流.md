# 按 ID 执行工作流

> **适用于**：Workflow。

运行指定的已发布工作流版本，由路径中的 `workflow_id` 指定。请求体、响应和流式行为与 [执行工作流](%E6%89%A7%E8%A1%8C%E5%B7%A5%E4%BD%9C%E6%B5%81.md) 相同，仅执行的版本不同。



## OpenAPI

````yaml /zh/api-reference/openapi_service.json post /workflows/{workflow_id}/run
openapi: 3.0.1
info:
  description: 用于 Dify 应用与知识库的 REST API。应用类接口使用应用 API 密钥认证，知识库类接口使用知识库 API 密钥认证。
  title: Dify 服务 API
  version: 1.0.0
servers:
  - description: Dify 服务 API 的基础 URL。自部署时，替换为你的 API 基础 URL。
    url: https://{api_base_url}
    variables:
      api_base_url:
        default: api.dify.ai/v1
        description: API 基础 URL 的主机与路径，不含 `https://` 前缀。
security:
  - ApiKeyAuth: []
tags:
  - description: 与聊天消息和交互相关的操作。
    name: 对话消息
  - description: 文件上传和预览操作。
    name: 文件操作
  - description: 终端用户信息相关操作。
    name: 终端用户
  - description: 用户反馈操作。
    name: 消息反馈
  - description: 与管理会话相关的操作。
    name: 会话管理
  - description: 文字转语音和语音转文字操作。
    name: 语音与文字转换
  - description: 获取应用设置和信息的操作。
    name: 应用配置
  - description: 与管理标注直接回复相关的操作。
    name: 标注管理
  - description: 暂停等待人工输入的工作流恢复操作。
    name: 人工介入
  - description: 用于执行和管理工作流的操作。
    name: 工作流运行
  - description: 文本生成相关操作。
    name: 文本生成消息
  - description: 用于管理知识库的操作，包括创建、配置和检索。
    name: 知识库
  - description: 用于在知识库中创建、更新和管理文档的操作。
    name: 文档
  - description: 用于管理分段和子分段的操作。
    name: 分段
  - description: 用于管理知识库元数据字段和文档元数据值的操作。
    name: 元数据
  - description: 用于管理知识库标签和标签绑定的操作。
    name: 标签
  - description: 用于获取可用模型的操作。
    name: 模型
  - description: 用于管理和运行知识流水线的操作，包括数据源插件和流水线执行。
    name: 知识流水线
  - description: 向知识库提问，并流式返回回答。
    name: 查询
  - description: 查看一次查询检索到了什么，以及原因。
    name: 查询记录
  - description: 在后台运行研究问题，并获取其结果。
    name: 研究任务
  - description: 读取知识库中的文档及其文件、修订版本和分段，并用元数据标注文档。
    name: 文档与分段
  - description: 跟踪、取消或重试索引，并列出知识库的后台任务。
    name: 索引任务
  - description: 跟踪文档文件、一批文件或数据源的删除，直到完成。
    name: 删除作业
  - description: 管理为知识库提供内容的数据源，以及它们的定时同步设置和连接。
    name: 数据源
  - description: 立即同步数据源，导入网站页面或提供商条目，并跟踪、取消或重试运行。
    name: 数据源同步与导入
  - description: 读取和更改知识库的模型与检索设置，并跟踪更改触发的迁移。
    name: 设置
paths:
  /workflows/{workflow_id}/run:
    post:
      tags:
        - 工作流运行
      summary: 按 ID 执行工作流
      description: >-
        **适用于**：Workflow。


        运行指定的已发布工作流版本，由路径中的 `workflow_id` 指定。请求体、响应和流式行为与
        [执行工作流](/zh/api-reference/workflow-runs/run-workflow) 相同，仅执行的版本不同。
      operationId: runWorkflowByIdZh
      parameters:
        - description: >-
            要运行的已发布工作流版本。在 [执行工作流](/zh/api-reference/workflow-runs/run-workflow)
            响应和
            [获取工作流运行详情](/zh/api-reference/workflow-runs/get-workflow-run-detail)
            的 `workflow_id` 字段中返回。必须指向已发布版本；草稿版本 ID 会返回 `bad_request`。
          in: path
          name: workflow_id
          required: true
          schema:
            type: string
      requestBody:
        content:
          application/json:
            examples:
              example:
                summary: 请求示例
                value:
                  inputs:
                    query: Summarize this article
                  response_mode: blocking
                  user: user_workflow_123
            schema:
              $ref: '#/components/schemas/WorkflowExecutionRequest'
        required: true
      responses:
        '200':
          content:
            application/json:
              examples:
                blockingResponse:
                  summary: 响应示例 - 阻塞式返回
                  value:
                    data:
                      created_at: 1705407629
                      elapsed_time: 2.45
                      error: null
                      finished_at: 1705407631
                      id: fb47b2e6-5e43-4f90-be01-d5c5a088d156
                      outputs:
                        result: Article summary here
                      status: succeeded
                      total_steps: 4
                      total_tokens: 280
                      workflow_id: 7c3e33d4-2a8b-4e5f-9b1a-d3c6e8f12345
                    task_id: c3800678-a077-43df-a102-53f23ed20b88
                    workflow_run_id: fb47b2e6-5e43-4f90-be01-d5c5a088d156
              schema:
                $ref: '#/components/schemas/WorkflowBlockingResponse'
            text/event-stream:
              examples:
                humanInputPause:
                  summary: 响应示例 - 人工介入暂停
                  value: >-
                    event: ping


                    data: {"event": "workflow_started", "task_id":
                    "c3800678-a077-43df-a102-53f23ed20b88", "workflow_run_id":
                    "fb47b2e6-5e43-4f90-be01-d5c5a088d156", "data": {"id":
                    "fb47b2e6-5e43-4f90-be01-d5c5a088d156", "workflow_id":
                    "7c3e33d4-2a8b-4e5f-9b1a-d3c6e8f12345", "inputs": {"draft":
                    "Hello"}, "created_at": 1705407629, "reason": "initial"}}


                    data: {"event": "human_input_required", "task_id":
                    "c3800678-a077-43df-a102-53f23ed20b88", "workflow_run_id":
                    "fb47b2e6-5e43-4f90-be01-d5c5a088d156", "data": {"form_id":
                    "a1b2c3d4-e5f6-7890-abcd-ef1234567890", "form_token":
                    "tok_abc123", "approval_channels": [], "node_id":
                    "approval_node", "node_title": "Approval", "form_content":
                    "请审阅草稿。", "inputs": [{"type": "paragraph",
                    "output_variable_name": "comment", "default": null}],
                    "actions": [{"id": "approve", "title": "批准", "button_style":
                    "primary"}], "display_in_ui": false,
                    "resolved_default_values": {"comment": ""},
                    "expiration_time": 1705494029}}


                    data: {"event": "workflow_paused", "task_id":
                    "c3800678-a077-43df-a102-53f23ed20b88", "workflow_run_id":
                    "fb47b2e6-5e43-4f90-be01-d5c5a088d156", "data":
                    {"workflow_run_id": "fb47b2e6-5e43-4f90-be01-d5c5a088d156",
                    "status": "paused", "created_at": 1705407629,
                    "elapsed_time": 0.5}}
                streamingResponse:
                  summary: 响应示例 - 流式返回
                  value: >-
                    event: ping


                    data: {"event": "workflow_started", "task_id":
                    "c3800678-a077-43df-a102-53f23ed20b88", "workflow_run_id":
                    "fb47b2e6-5e43-4f90-be01-d5c5a088d156", "data": {"id":
                    "fb47b2e6-5e43-4f90-be01-d5c5a088d156", "workflow_id":
                    "7c3e33d4-2a8b-4e5f-9b1a-d3c6e8f12345", "inputs": {"query":
                    "Translate this"}, "created_at": 1705407629, "reason":
                    "initial"}}


                    data: {"event": "node_started", "task_id":
                    "c3800678-a077-43df-a102-53f23ed20b88", "workflow_run_id":
                    "fb47b2e6-5e43-4f90-be01-d5c5a088d156", "data": {"id":
                    "node_exec_1", "node_id": "node_1", "node_type": "llm",
                    "title": "LLM Node", "index": 1, "created_at": 1705407629}}


                    data: {"event": "reasoning_chunk", "task_id":
                    "c3800678-a077-43df-a102-53f23ed20b88", "workflow_run_id":
                    "fb47b2e6-5e43-4f90-be01-d5c5a088d156", "data":
                    {"reasoning": "Let me translate that.", "node_id": "node_1",
                    "is_final": false}}


                    data: {"event": "reasoning_chunk", "task_id":
                    "c3800678-a077-43df-a102-53f23ed20b88", "workflow_run_id":
                    "fb47b2e6-5e43-4f90-be01-d5c5a088d156", "data":
                    {"reasoning": "", "node_id": "node_1", "is_final": true}}


                    data: {"event": "text_chunk", "task_id":
                    "c3800678-a077-43df-a102-53f23ed20b88", "workflow_run_id":
                    "fb47b2e6-5e43-4f90-be01-d5c5a088d156", "data": {"text":
                    "Bonjour", "from_variable_selector": ["node_1", "text"]}}


                    data: {"event": "workflow_finished", "task_id":
                    "c3800678-a077-43df-a102-53f23ed20b88", "workflow_run_id":
                    "fb47b2e6-5e43-4f90-be01-d5c5a088d156", "data": {"id":
                    "fb47b2e6-5e43-4f90-be01-d5c5a088d156", "workflow_id":
                    "7c3e33d4-2a8b-4e5f-9b1a-d3c6e8f12345", "status":
                    "succeeded", "outputs": {"result": "Bonjour le monde"},
                    "elapsed_time": 1.23, "total_tokens": 150, "total_steps": 3,
                    "created_at": 1705407629, "finished_at": 1705407630}}
              schema:
                description: >-
                  Server-Sent Events (SSE) 流。按 [SSE
                  流式传输指南](/zh/api-reference/guides/streaming) 解析：读取 `data:` 行，根据
                  `event` 字段分派，忽略 `ping`（保活；流以 `ping` 开头，之后约每 10 秒到达一次）。


                  **流生命周期**：收到 `workflow_finished`、`workflow_paused` 或 `error`
                  事件时流关闭。错误以流内 `error` 事件的形式返回，HTTP 状态码始终为
                  `200`；请检查事件载荷获取详情，不要依赖状态码判断。


                  **推理事件**：

                  - `reasoning_chunk`：来自 `reasoning_format` 为 `separated` 的 LLM
                  节点的推理内容增量。拼接连续的 `reasoning_chunk` 事件即可还原完整推理内容；`is_final:
                  true` 的事件标志该节点思考结束（且 `reasoning` 可能为空）。载荷位于 `data`
                  下，与对话应用不同，`message_id` 为 `null`，且不含 `conversation_id`。并行的
                  `text_chunk` 流不含 `<think>` 标签。


                  **人工介入事件**：

                  - `human_input_required`：工作流到达人工介入节点时与 `workflow_paused`
                  一同触发。使用载荷中的 `form_token` 通过 [人工介入
                  API](/zh/api-reference/human-input/get-human-input-form) 处理表单。

                  - `human_input_form_filled`：接收者提交了表单，工作流恢复执行。

                  - `human_input_form_timeout`：表单超时未响应。如定义了超时回退分支，工作流将沿该分支执行。
                type: string
          description: >-
            请求成功。内容类型和结构取决于请求中的 `response_mode` 参数。


            - 如果 `response_mode` 为 `blocking`，返回 `application/json` 和
            `WorkflowBlockingResponse` 对象。

            - 如果 `response_mode` 为 `streaming`，返回 `text/event-stream` 和
            `ChunkWorkflowEvent` 对象流。
        '400':
          content:
            application/json:
              examples:
                bad_request:
                  summary: bad_request
                  value:
                    code: bad_request
                    message: >-
                      Cannot use draft workflow version. Workflow ID:
                      7c3e33d4-2a8b-4e5f-9b1a-d3c6e8f12345. Please use a
                      published workflow version or leave workflow_id empty.
                    status: 400
                completion_request_error:
                  summary: completion_request_error
                  value:
                    code: completion_request_error
                    message: Completion request failed.
                    status: 400
                invalid_param:
                  summary: invalid_param
                  value:
                    code: invalid_param
                    message: Arg user must be provided.
                    status: 400
                model_currently_not_support:
                  summary: model_currently_not_support
                  value:
                    code: model_currently_not_support
                    message: >-
                      Dify Hosted OpenAI trial currently not support the GPT-4
                      model.
                    status: 400
                not_workflow_app:
                  summary: not_workflow_app
                  value:
                    code: not_workflow_app
                    message: Please check if your app mode matches the right API route.
                    status: 400
                provider_not_initialize:
                  summary: provider_not_initialize
                  value:
                    code: provider_not_initialize
                    message: >-
                      No valid model provider credentials found. Please go to
                      Settings -> Model Provider to complete your provider
                      credentials.
                    status: 400
                provider_quota_exceeded:
                  summary: provider_quota_exceeded
                  value:
                    code: provider_quota_exceeded
                    message: >-
                      Your quota for Dify Hosted OpenAI has been exhausted.
                      Please go to Settings -> Model Provider to complete your
                      own provider credentials.
                    status: 400
          description: |-
            - `not_workflow_app` : 应用模式与 API 路由不匹配。
            - `bad_request` : 工作流为草稿或 ID 格式无效。
            - `provider_not_initialize` : 未找到有效的模型供应商凭据。
            - `provider_quota_exceeded` : 模型供应商配额已用尽。
            - `model_currently_not_support` : 当前模型不可用。
            - `completion_request_error` : 工作流执行请求失败。
            - `invalid_param` : 请求参数缺失或无效，例如缺少 `user`。
        '403':
          content:
            application/json:
              examples:
                trigger_workflow_service_mode_unavailable:
                  summary: trigger_workflow_service_mode_unavailable
                  value:
                    code: trigger_workflow_service_mode_unavailable
                    message: >-
                      This workflow uses a trigger entry and cannot be invoked
                      through Web App, Service API, OpenAPI, or MCP.
                    status: 403
                workflow_version_execution_not_allowed:
                  summary: workflow_version_execution_not_allowed
                  value:
                    code: workflow_version_execution_not_allowed
                    message: >-
                      Workflow version execution is not available on your
                      current plan. Please upgrade to a paid plan.
                    status: 403
          description: >-
            - `workflow_version_execution_not_allowed` : Dify Cloud Sandbox
            套餐无法执行指定的工作流版本。

            - `trigger_workflow_service_mode_unavailable` :
            所选工作流版本以触发器为起始节点，只能由触发器启动。检查只针对所选版本，以用户输入为起始节点的版本仍可按 ID 运行。
        '404':
          content:
            application/json:
              examples:
                not_found:
                  summary: not_found
                  value:
                    code: not_found
                    message: >-
                      Workflow not found with id:
                      7c3e33d4-2a8b-4e5f-9b1a-d3c6e8f12345
                    status: 404
          description: '`not_found` : 工作流 not found.'
        '429':
          content:
            application/json:
              examples:
                rate_limit_error:
                  summary: rate_limit_error
                  value:
                    code: rate_limit_error
                    message: >-
                      Workflow execution quota limit reached for tenant
                      8f1e2a90-3b7c-4d55-9a01-6c2f4e8b1d33
                    status: 429
                too_many_requests:
                  summary: too_many_requests
                  value:
                    code: too_many_requests
                    message: Too many requests. Please try again later.
                    status: 429
          description: |-
            - `too_many_requests` : 该应用的并发请求过多。
            - `rate_limit_error` : 此工作空间在 Dify Cloud 的工作流执行配额已达上限。
        '500':
          content:
            application/json:
              examples:
                internal_server_error:
                  summary: internal_server_error
                  value:
                    code: internal_server_error
                    message: Internal Server Error.
                    status: 500
          description: '`internal_server_error` : 内部服务器错误。'
components:
  schemas:
    WorkflowExecutionRequest:
      properties:
        files:
          description: >-
            文件列表。适用于需要将文件与文本组合输入的场景，仅在模型支持 Vision 能力时可用。要附加本地文件，请先通过
            [上传文件](/zh/api-reference/files/upload-file) 上传，然后将返回的 `id` 作为
            `upload_file_id`，并设置 `transfer_method: local_file`。
          items:
            $ref: '#/components/schemas/InputFileObject'
          nullable: true
          type: array
        inputs:
          additionalProperties:
            oneOf:
              - type: string
              - type: number
              - type: boolean
              - type: object
              - items:
                  $ref: '#/components/schemas/InputFileObject'
                nullable: true
                type: array
          description: >-
            工作流输入变量的键值对。变量名称和类型可从
            [获取应用参数](/zh/api-reference/applications/get-app-parameters) 响应中的
            `user_input_form` 字段获取。


            文件类型变量的值为文件对象数组，包含 `type`、`transfer_method` 以及 `url` 或
            `upload_file_id`。省略文件或文件列表类型的输入，或传入 `null` 时，将使用应用中为该输入配置的默认文件。
          type: object
        response_mode:
          description: >-
            响应模式。省略时默认为阻塞式返回。


            - `streaming`：运行事件以 Server-Sent Events 形式返回。

            - `blocking`：运行结束后一次性返回。运行时间较长时有中断风险：在 Dify Cloud
            上，如果边缘代理在超时时间内未收到响应，就可能中断连接。
          enum:
            - streaming
            - blocking
          type: string
        user:
          description: >-
            终端用户标识，由你的应用定义，需在应用内唯一。用于限定数据访问范围：工作流运行及其文件仅对携带相同 `user` 的后续请求可见。参见
            [终端用户身份](/zh/api-reference/guides/end-user-identity)。
          type: string
      required:
        - inputs
        - user
      type: object
    WorkflowBlockingResponse:
      properties:
        data:
          $ref: '#/components/schemas/WorkflowFinishedData'
        task_id:
          description: >-
            进行中的执行任务 ID。配合
            [停止工作流任务](/zh/api-reference/workflow-runs/stop-workflow-task)
            使用以取消运行中的工作流。仅在执行期间有效。
          format: uuid
          type: string
        workflow_run_id:
          description: >-
            此工作流运行记录的持久化标识符。配合
            [获取工作流运行详情](/zh/api-reference/workflow-runs/get-workflow-run-detail)
            使用以在执行后获取结果。
          format: uuid
          type: string
      type: object
    InputFileObject:
      anyOf:
        - not:
            required:
              - upload_file_id
          properties:
            transfer_method:
              enum:
                - remote_url
            url:
              format: url
              type: string
          required:
            - url
        - not:
            required:
              - url
          properties:
            transfer_method:
              enum:
                - local_file
            upload_file_id:
              type: string
          required:
            - upload_file_id
      properties:
        transfer_method:
          description: 传输方式：文件 URL 使用 `remote_url`，上传文件使用 `local_file`。
          enum:
            - remote_url
            - local_file
          type: string
        type:
          description: 文件类型。
          enum:
            - image
            - document
            - audio
            - video
            - custom
          type: string
        upload_file_id:
          description: >-
            已上传文件 ID，通过 [上传文件](/zh/api-reference/files/upload-file) API 预先上传获取（当
            `transfer_method` 为 `local_file` 时使用）。
          type: string
        url:
          description: 文件 URL（当 `transfer_method` 为 `remote_url` 时）。
          format: url
          type: string
      required:
        - type
        - transfer_method
      type: object
    WorkflowFinishedData:
      properties:
        created_at:
          description: 工作流运行创建时的 Unix 时间戳。
          format: int64
          type: integer
        created_by:
          additionalProperties: true
          description: 创建者信息。仅存在于流式 `workflow_finished` 事件中。
          type: object
        elapsed_time:
          description: 总耗时（秒），不含运行暂停的时间。
          format: float
          type: number
        error:
          description: 工作流失败时的错误消息。
          nullable: true
          type: string
        exceptions_count:
          description: 执行过程中遇到的异常数量。仅在流式 `workflow_finished` 事件中出现。
          nullable: true
          type: integer
        files:
          description: 工作流执行期间生成的文件。仅存在于流式 `workflow_finished` 事件中。
          items:
            additionalProperties: true
            type: object
          nullable: true
          type: array
        finished_at:
          description: 工作流运行结束时的 Unix 时间戳。
          format: int64
          nullable: true
          type: integer
        id:
          description: 工作流运行 ID。
          format: uuid
          type: string
        outputs:
          additionalProperties: true
          description: 工作流的输出数据。
          nullable: true
          type: object
        status:
          description: >-
            工作流执行状态。`running` 表示执行中，`succeeded` 表示成功完成，`failed` 表示执行出错，`stopped`
            表示手动停止，`partial-succeeded` 表示部分节点成功但其他失败，`paused` 表示等待人工介入。
          type: string
        total_steps:
          description: 已执行的工作流总步数。
          type: integer
        total_tokens:
          description: 所有节点消耗的总令牌数。
          type: integer
        workflow_id:
          description: 工作流 ID.
          format: uuid
          type: string
      type: object
  securitySchemes:
    ApiKeyAuth:
      bearerFormat: API_KEY
      description: >-
        每个请求都通过 API Key 认证：`Authorization: Bearer {API_KEY}`。应用接口使用应用 API
        Key，知识库接口使用知识库 API Key（[快速开始](/zh/api-reference/guides/get-started)）。


        API Key 应保存在服务端，切勿嵌入客户端代码。缺失或无效的 Key 会返回 HTTP `401`（`unauthorized`）。
      scheme: bearer
      type: http

````

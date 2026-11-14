# A2A JSON-RPC

> Communicate with an assistant using the Agent-to-Agent (A2A) Protocol over JSON-RPC 2.0.
This endpoint accepts a JSON-RPC envelope and dispatches based on `method`.

**Supported Methods:**
- `message/send`: Send a message and wait for the final Task result.
- `message/stream`: Send a message and receive Server-Sent Events (SSE) JSON-RPC responses.
- `tasks/get`: Fetch the current state of a Task by ID.
- `tasks/cancel`: Request cancellation (currently not supported; returns an error).

**LangGraph Mapping:**
- `message.contextId` maps to LangGraph `thread_id`.

**Notes:**
- Only `text` and `data` parts are supported; `file` parts are not.
- If `message.contextId` is omitted, a new context is created.
- Text parts require the assistant input schema to include a `messages` field.




## OpenAPI

````yaml /langsmith/agent-server-openapi.json post /a2a/{assistant_id}
openapi: 3.1.0
info:
  title: LangSmith Agent Server
  version: 0.1.0
servers: []
security: []
tags:
  - name: Assistants
    description: An assistant is a configured instance of a graph.
  - name: Threads
    description: A thread contains the accumulated outputs of a group of runs.
  - name: Thread Runs
    description: >-
      A run is an invocation of a graph / assistant on a thread. It updates the
      state of the thread.
  - name: Stateless Runs
    description: >-
      A run is an invocation of a graph / assistant, with no state or memory
      persistence.
  - name: Crons
    description: >-
      A cron is a periodic run that recurs on a given schedule. The repeats can
      be isolated, or share state in a thread
  - name: Store
    description: >-
      Store is an API for managing persistent key-value store (long-term memory)
      that is available from any thread.
  - name: A2A
    description: >-
      Agent-to-Agent Protocol related endpoints for exposing assistants as
      A2A-compliant agents.
  - name: MCP
    description: >-
      Model Context Protocol related endpoints for exposing an agent as an MCP
      server.
  - name: System
    description: System endpoints for health checks, metrics, and server information.
  - name: Streaming
    description: >-
      Thread-centric streaming endpoints. Provides a structured command/event
      surface over SSE+HTTP; WebSocket is also supported at
      `/threads/{thread_id}/stream/events` (not documented here — OpenAPI 3.1
      does not describe WebSocket).
paths:
  /a2a/{assistant_id}:
    post:
      tags:
        - A2A
      summary: A2A JSON-RPC
      description: >
        Communicate with an assistant using the Agent-to-Agent (A2A) Protocol
        over JSON-RPC 2.0.

        This endpoint accepts a JSON-RPC envelope and dispatches based on
        `method`.


        **Supported Methods:**

        - `message/send`: Send a message and wait for the final Task result.

        - `message/stream`: Send a message and receive Server-Sent Events (SSE)
        JSON-RPC responses.

        - `tasks/get`: Fetch the current state of a Task by ID.

        - `tasks/cancel`: Request cancellation (currently not supported; returns
        an error).


        **LangGraph Mapping:**

        - `message.contextId` maps to LangGraph `thread_id`.


        **Notes:**

        - Only `text` and `data` parts are supported; `file` parts are not.

        - If `message.contextId` is omitted, a new context is created.

        - Text parts require the assistant input schema to include a `messages`
        field.
      operationId: post_a2a
      parameters:
        - name: assistant_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
          description: The ID of the assistant to communicate with
        - name: Accept
          in: header
          required: true
          schema:
            type: string
          description: >-
            For `message/stream`, must include `text/event-stream`. For all
            other methods, use `application/json`.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                jsonrpc:
                  type: string
                  enum:
                    - '2.0'
                  description: JSON-RPC version
                id:
                  type: string
                  description: Request identifier
                method:
                  type: string
                  enum:
                    - message/send
                    - message/stream
                    - tasks/get
                    - tasks/cancel
                  description: The method to invoke
                params:
                  type: object
                  description: Method parameters; shape depends on the method.
                  oneOf:
                    - title: Message Send/Stream Parameters
                      type: object
                      properties:
                        message:
                          type: object
                          properties:
                            role:
                              type: string
                              enum:
                                - user
                                - agent
                              description: A2A role for the message sender.
                            parts:
                              type: array
                              items:
                                oneOf:
                                  - title: Text Part
                                    type: object
                                    properties:
                                      kind:
                                        type: string
                                        enum:
                                          - text
                                      text:
                                        type: string
                                        description: Text content.
                                    required:
                                      - kind
                                      - text
                                  - title: Data Part
                                    type: object
                                    properties:
                                      kind:
                                        type: string
                                        enum:
                                          - data
                                      data:
                                        type: object
                                        description: >-
                                          Structured JSON merged into the
                                          assistant input.
                                    required:
                                      - kind
                                      - data
                              description: Message parts (text/data only).
                            messageId:
                              type: string
                              description: Client-generated message identifier.
                            contextId:
                              type: string
                              description: >-
                                Conversation context ID; maps to LangGraph
                                thread_id.
                            taskId:
                              type: string
                              description: >-
                                Optional task ID. Currently ignored by this
                                implementation.
                          required:
                            - role
                            - parts
                            - messageId
                      required:
                        - message
                    - title: Task Get Parameters
                      type: object
                      properties:
                        id:
                          type: string
                          description: Task (run) identifier to retrieve.
                        contextId:
                          type: string
                          description: Context identifier (thread_id) for the task.
                        historyLength:
                          type: integer
                          minimum: 0
                          maximum: 10
                          description: Maximum number of history messages to include.
                      required:
                        - id
                        - contextId
                    - title: Task Cancel Parameters
                      type: object
                      properties:
                        id:
                          type: string
                          description: Task (run) identifier to cancel.
                        contextId:
                          type: string
                          description: Context identifier (thread_id) for the task.
                      required:
                        - id
                        - contextId
              required:
                - jsonrpc
                - id
                - method
            examples:
              message_send:
                summary: Send a message (synchronous)
                value:
                  jsonrpc: '2.0'
                  id: '1'
                  method: message/send
                  params:
                    message:
                      role: user
                      parts:
                        - kind: text
                          text: Hello from A2A
                        - kind: data
                          data:
                            locale: en-US
                      messageId: msg-1
                      contextId: f5bd2a40-74b6-4f7a-b649-ea3f09890003
              message_stream:
                summary: Send a message (streaming)
                value:
                  jsonrpc: '2.0'
                  id: '2'
                  method: message/stream
                  params:
                    message:
                      role: user
                      parts:
                        - kind: text
                          text: Stream this response
                      messageId: msg-2
                      contextId: f5bd2a40-74b6-4f7a-b649-ea3f09890003
              tasks_get:
                summary: Get a task
                value:
                  jsonrpc: '2.0'
                  id: '3'
                  method: tasks/get
                  params:
                    id: run-uuid
                    contextId: f5bd2a40-74b6-4f7a-b649-ea3f09890003
                    historyLength: 10
              tasks_cancel:
                summary: Cancel a task (currently unsupported)
                value:
                  jsonrpc: '2.0'
                  id: '4'
                  method: tasks/cancel
                  params:
                    id: run-uuid
                    contextId: f5bd2a40-74b6-4f7a-b649-ea3f09890003
              message_stream_with_context:
                summary: Stream multi-turn messages using the same contextId
                description: >-
                  Send a streaming message; reuse the same contextId for
                  subsequent turns to keep conversation state.
                value:
                  jsonrpc: '2.0'
                  id: '1'
                  method: message/stream
                  params:
                    message:
                      role: user
                      contextId: thread-123
                      parts:
                        - kind: text
                          text: Hello!
                      messageId: msg-1
              interrupt_resume_text:
                summary: Resume an interrupted task with a text reply
                description: >-
                  When a task is in input-required state, send a normal text
                  part with the same contextId and taskId to resume.
                value:
                  jsonrpc: '2.0'
                  id: '2'
                  method: message/send
                  params:
                    message:
                      role: user
                      contextId: thread-123
                      parts:
                        - kind: text
                          text: Here is the info you asked for.
                      messageId: msg-2
                      taskId: thread-123:run-456
              interrupt_resume_data_parallel:
                summary: Resume parallel interrupts with a data part
                description: >-
                  Advanced: if your agent supports parallel interrupts, provide
                  a structured resume payload in a data part with the same
                  contextId and taskId.
                value:
                  jsonrpc: '2.0'
                  id: '3'
                  method: message/send
                  params:
                    message:
                      role: user
                      contextId: thread-123
                      parts:
                        - kind: data
                          data:
                            resume:
                              - id: interrupt-1
                                value:
                                  choice: A
                              - id: interrupt-2
                                value:
                                  choice: B
                      messageId: msg-3
                      taskId: thread-123:run-456
      responses:
        '200':
          description: >-
            JSON-RPC response for non-streaming methods. For `message/stream`,
            the response is an SSE stream of JSON-RPC envelopes.
          content:
            application/json:
              schema:
                type: object
                properties:
                  jsonrpc:
                    type: string
                    enum:
                      - '2.0'
                  id:
                    type: string
                  result:
                    type: object
                    description: Success result containing task information or task details
                  error:
                    type: object
                    properties:
                      code:
                        type: integer
                      message:
                        type: string
                    description: Error information if request failed
                required:
                  - jsonrpc
                  - id
              examples:
                task_result:
                  summary: Task result (message/send)
                  value:
                    jsonrpc: '2.0'
                    id: '1'
                    result:
                      kind: task
                      id: run-uuid
                      contextId: f5bd2a40-74b6-4f7a-b649-ea3f09890003
                      status:
                        state: completed
                      artifacts:
                        - artifactId: artifact-uuid
                          name: Assistant Response
                          parts:
                            - kind: text
                              text: Hello back
                error_result:
                  summary: Error response
                  value:
                    jsonrpc: '2.0'
                    id: '1'
                    error:
                      code: -32602
                      message: 'Invalid request: Missing required parameter: contextId'
            text/event-stream:
              schema:
                type: string
                description: SSE stream of JSON-RPC response objects.
              examples:
                stream_event:
                  summary: SSE data chunk (JSON-RPC)
                  value: >+
                    data:
                    {"jsonrpc":"2.0","id":"2","result":{"kind":"status-update","taskId":"run-uuid","contextId":"f5bd2a40-74b6-4f7a-b649-ea3f09890003","status":{"state":"working"},"final":false}}

        '400':
          description: >-
            Bad Request (invalid JSON-RPC, invalid params, or missing Accept
            header).
        '404':
          description: Assistant not found
        '500':
          description: Internal server error

````

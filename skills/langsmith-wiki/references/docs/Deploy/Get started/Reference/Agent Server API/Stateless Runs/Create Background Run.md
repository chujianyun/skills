# Create Background Run

> Create a run and return the run ID immediately. Don't wait for the final run output.



## OpenAPI

````yaml /langsmith/agent-server-openapi.json post /runs
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
  /runs:
    post:
      tags:
        - Stateless Runs
      summary: Create Background Run
      description: >-
        Create a run and return the run ID immediately. Don't wait for the final
        run output.
      operationId: run_stateless_runs_post
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/RunCreateStateless'
        required: true
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema: {}
          headers:
            Content-Location:
              description: >-
                The URL of the run that was created. Can be used to later join
                the stream.
              schema:
                type: string
        '404':
          description: Not Found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
        '409':
          description: Conflict
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
components:
  schemas:
    RunCreateStateless:
      properties:
        assistant_id:
          anyOf:
            - type: string
              format: uuid
              title: Assistant Id
            - type: string
              title: Graph Id
          description: >-
            The assistant ID or graph name to run. If using graph name, will
            default to first assistant created from that graph.
        input:
          anyOf:
            - type: object
            - type: array
            - type: string
            - type: number
            - type: boolean
            - type: 'null'
          title: Input
          description: The input to the graph.
        command:
          anyOf:
            - $ref: '#/components/schemas/Command'
            - type: 'null'
          title: Input
          description: The input to the graph.
        metadata:
          type: object
          title: Metadata
          description: Metadata to assign to the run.
        config:
          properties:
            tags:
              items:
                type: string
              type: array
              title: Tags
            recursion_limit:
              type: integer
              title: Recursion Limit
            configurable:
              type: object
              title: Configurable
          type: object
          title: Config
          description: The configuration for the assistant.
        context:
          type: object
          title: Context
          description: Static context added to the assistant.
        webhook:
          type: string
          maxLength: 65536
          minLength: 1
          format: uri-reference
          title: Webhook
          description: Webhook to call after LangGraph API call is done.
        stream_mode:
          anyOf:
            - items:
                type: string
                enum:
                  - values
                  - messages
                  - messages-tuple
                  - tasks
                  - checkpoints
                  - updates
                  - events
                  - debug
                  - custom
                  - tools
                  - lifecycle
              type: array
            - type: string
              enum:
                - values
                - messages
                - messages-tuple
                - tasks
                - checkpoints
                - updates
                - events
                - debug
                - custom
                - tools
                - lifecycle
          title: Stream Mode
          description: >-
            The stream mode(s) to use. `lifecycle` sends `lifecycle|<namespace>`
            events when a subagent (a subgraph) starts and ends: `{"event":
            "started" | "completed" | "failed" | "interrupted", "namespace",
            "tool_call_id"?, "error"?}`, with the id of the tool call that
            started it, with or without `stream_subgraphs`. `tools` sends
            `on_tool_start`, `on_tool_event`, `on_tool_end` and `on_tool_error`
            events with `toolCallId` and `name` (from langgraph 1.2.19 and
            @langchain/langgraph 1.6.0; a tool error's text is never sent).
          default:
            - values
        feedback_keys:
          items:
            type: string
          type: array
          title: Feedback Keys
          description: >-
            Generate pre-signed URLs for assigning feedback keys to the run.


            For each key specified, a unique URL will be generated that can be
            called to assign the feedback key to the run. See [LangSmith
            Feedback](https://docs.langchain.com/langsmith/observability-concepts#feedback)
            for more details.
        stream_subgraphs:
          type: boolean
          title: Stream Subgraphs
          description: Whether to stream output from subgraphs.
          default: false
        stream_resumable:
          type: boolean
          title: Stream Resumable
          description: >-
            Whether to keep the run's stream events so a client can rejoin the
            run. Deployments keep every run's events for
            `RESUMABLE_STREAM_TTL_SECONDS` (2 minutes by default) regardless of
            this field. The in-memory runtime (`langgraph dev`) keeps them only
            when it is true.
          default: false
        on_completion:
          type: string
          enum:
            - delete
            - keep
          title: On Completion
          description: >-
            Whether to delete or keep the thread created for a stateless run.
            Must be one of 'delete' or 'keep'.
          default: delete
        after_seconds:
          type: number
          title: After Seconds
          description: >-
            The number of seconds to wait before starting the run. Use to
            schedule future runs.
        checkpoint_during:
          type: boolean
          title: Checkpoint During
          description: >-
            Whether to checkpoint during the run.


            Deprecated. Use `durability` instead to control checkpoint
            persistence behavior during the run.
          deprecated: true
          default: false
        durability:
          type: string
          enum:
            - sync
            - async
            - exit
          title: Durability
          description: >-
            Durability level for the run. Must be one of `sync`, `async`, or
            `exit`. See [durability
            modes](https://docs.langchain.com/oss/python/langgraph/checkpointers#durability-modes)
            for more details.
          default: async
      type: object
      required:
        - assistant_id
      title: RunCreateStateless
      description: Payload for creating a run.
    ErrorResponse:
      type: object
      required:
        - detail
      properties:
        detail:
          type: string
          description: Human-readable error message
      title: ErrorResponse
      description: Error response returned from the server
    Command:
      type: object
      title: Command
      description: The command to run.
      properties:
        update:
          type:
            - object
            - array
            - 'null'
          title: Update
          description: An update to the state.
        resume:
          type:
            - object
            - array
            - number
            - string
            - boolean
            - 'null'
          title: Resume
          description: A value to pass to an interrupted node.
        goto:
          anyOf:
            - $ref: '#/components/schemas/Send'
            - type: array
              items:
                $ref: '#/components/schemas/Send'
            - type: string
            - items:
                type: string
              type: array
            - type: 'null'
          title: Goto
          description: >-
            Name of the node(s) to navigate to next or node(s) to be executed
            with a provided input.
    Send:
      type: object
      title: Send
      description: A message to send to a node.
      properties:
        node:
          type: string
          title: Node
          description: The node to send the message to.
        input:
          type:
            - object
            - array
            - number
            - string
            - boolean
            - 'null'
          title: Message
          description: The message to send.
      required:
        - node
        - input

````

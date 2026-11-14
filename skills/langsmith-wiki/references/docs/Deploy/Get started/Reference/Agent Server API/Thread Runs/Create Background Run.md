# Create Background Run

> Create a run in existing thread, return the run ID immediately. Don't wait for the final run output.



## OpenAPI

````yaml /langsmith/agent-server-openapi.json post /threads/{thread_id}/runs
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
  /threads/{thread_id}/runs:
    post:
      tags:
        - Thread Runs
      summary: Create Background Run
      description: >-
        Create a run in existing thread, return the run ID immediately. Don't
        wait for the final run output.
      operationId: create_run_threads__thread_id__runs_post
      parameters:
        - description: The ID of the thread.
          required: true
          schema:
            type: string
            format: uuid
            title: Thread Id
            description: The ID of the thread.
          name: thread_id
          in: path
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/RunCreateStateful'
        required: true
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Run'
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
    RunCreateStateful:
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
        checkpoint:
          $ref: '#/components/schemas/CheckpointConfig'
          type: object
          title: Checkpoint
          description: The checkpoint to resume from.
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
        interrupt_before:
          anyOf:
            - type: string
              enum:
                - '*'
            - items:
                type: string
              type: array
          title: Interrupt Before
          description: Nodes to interrupt immediately before they get executed.
        interrupt_after:
          anyOf:
            - type: string
              enum:
                - '*'
            - items:
                type: string
              type: array
          title: Interrupt After
          description: Nodes to interrupt immediately after they get executed.
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
        strict_resume:
          type: boolean
          title: Strict Resume
          description: >-
            Refuse a `command.resume` that names an interrupt that isn't
            pending, before the graph runs: the run ends with
            `UnknownInterruptError` and the thread keeps its state. Needs a
            langgraph version with strict resume; `/info` reports
            `strict_resume` when it is available.
          default: false
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
        multitask_strategy:
          type: string
          enum:
            - reject
            - rollback
            - interrupt
            - enqueue
          title: Multitask Strategy
          description: >-
            Multitask strategy to use. Must be one of 'reject', 'interrupt',
            'rollback', or 'enqueue'.
          default: enqueue
        if_not_exists:
          type: string
          enum:
            - create
            - reject
          title: If Not Exists
          description: >-
            How to handle missing thread. Must be either 'reject' (raise error
            if missing), or 'create' (create new thread).
          default: reject
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
      title: RunCreateStateful
      description: Payload for creating a run.
    Run:
      properties:
        run_id:
          type: string
          format: uuid
          title: Run Id
          description: The ID of the run.
        thread_id:
          type: string
          format: uuid
          title: Thread Id
          description: The ID of the thread.
        assistant_id:
          type: string
          format: uuid
          title: Assistant Id
          description: The assistant that was used for this run.
        created_at:
          type: string
          format: date-time
          title: Created At
          description: The time the run was created.
        updated_at:
          type: string
          format: date-time
          title: Updated At
          description: The last time the run was updated.
        status:
          type: string
          enum:
            - pending
            - running
            - error
            - success
            - timeout
            - interrupted
          title: Status
          description: >-
            The status of the run. One of 'pending', 'running', 'error',
            'success', 'timeout', 'interrupted'.
        metadata:
          type: object
          title: Metadata
          description: The run metadata.
        kwargs:
          type: object
          title: Kwargs
        multitask_strategy:
          type: string
          enum:
            - reject
            - rollback
            - interrupt
            - enqueue
          title: Multitask Strategy
          description: Strategy to handle concurrent runs on the same thread.
        langsmith_session_name:
          type: string
          title: Langsmith Session Name
          description: >-
            LangSmith tracing session (project) name for this run, when tracing
            is enabled at creation time.
          nullable: true
        cancel_reason:
          type: string
          title: Cancel Reason
          description: >-
            Why the run was cancelled, if it was: for example an explicit cancel
            request, a client disconnecting, or a newer run superseding it.
            Server-generated.
          nullable: true
        priority:
          type: integer
          minimum: -5
          maximum: 5
          title: Priority
          description: >-
            Queue priority level of the run, from -5 to 5. When all workers are
            busy, runs at a lower level start first.
      type: object
      required:
        - run_id
        - thread_id
        - assistant_id
        - created_at
        - updated_at
        - status
        - metadata
        - kwargs
        - multitask_strategy
      title: Run
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
    CheckpointConfig:
      type: object
      title: CheckpointConfig
      description: Checkpoint config.
      properties:
        thread_id:
          type: string
          description: Unique identifier for the thread associated with this checkpoint.
        checkpoint_ns:
          type: string
          description: Namespace for the checkpoint, used for organization and retrieval.
        checkpoint_id:
          type: string
          description: Optional unique identifier for the checkpoint itself.
        checkpoint_map:
          type: object
          description: Optional dictionary containing checkpoint-specific data.
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

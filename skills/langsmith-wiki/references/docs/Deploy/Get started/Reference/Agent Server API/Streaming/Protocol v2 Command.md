# Protocol v2 Command

> Send a single protocol command scoped to a thread. The request body is a `ProtocolCommand` envelope with a `method` (e.g. `run.start`, `input.respond`, `agent.getTree`) and method-specific `params`. The response is either a `ProtocolSuccess` (with method-specific `result`) or a `ProtocolError`.

Commands that create runs (`run.start`, `input.respond`) leave the run executing in the background on the worker queue. Event streaming for that run is observed via a concurrent `POST /threads/{thread_id}/stream/events` connection.

WebSocket clients use the same command envelope in-band on `/threads/{thread_id}/stream/events` and additionally have access to `subscription.subscribe` / `subscription.unsubscribe` over the same connection.



## OpenAPI

````yaml /langsmith/agent-server-openapi.json post /threads/{thread_id}/commands
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
  /threads/{thread_id}/commands:
    post:
      tags:
        - Streaming
      summary: Protocol v2 Command
      description: >-
        Send a single protocol command scoped to a thread. The request body is a
        `ProtocolCommand` envelope with a `method` (e.g. `run.start`,
        `input.respond`, `agent.getTree`) and method-specific `params`. The
        response is either a `ProtocolSuccess` (with method-specific `result`)
        or a `ProtocolError`.


        Commands that create runs (`run.start`, `input.respond`) leave the run
        executing in the background on the worker queue. Event streaming for
        that run is observed via a concurrent `POST
        /threads/{thread_id}/stream/events` connection.


        WebSocket clients use the same command envelope in-band on
        `/threads/{thread_id}/stream/events` and additionally have access to
        `subscription.subscribe` / `subscription.unsubscribe` over the same
        connection.
      operationId: protocol_thread_command_post
      parameters:
        - name: thread_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
            title: Thread Id
            description: The ID of the thread the command applies to.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ProtocolCommand'
      responses:
        '200':
          description: Protocol response — either `ProtocolSuccess` or `ProtocolError`.
          content:
            application/json:
              schema:
                oneOf:
                  - $ref: '#/components/schemas/ProtocolSuccess'
                  - $ref: '#/components/schemas/ProtocolError'
        '400':
          description: Malformed command envelope
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ProtocolError'
components:
  schemas:
    ProtocolCommand:
      type: object
      title: ProtocolCommand
      description: >-
        A client → server command envelope. Known methods: `run.start`,
        `input.respond`, `subscription.subscribe` (WS only),
        `subscription.unsubscribe` (WS only), `agent.getTree`.
      required:
        - id
        - method
      properties:
        id:
          type: integer
          minimum: 0
          description: Client-assigned command id; echoed in the response.
        method:
          type: string
          description: Command method name (e.g. `run.start`).
        params:
          type: object
          description: Method-specific parameters. See the CDDL spec for per-method shapes.
          additionalProperties: true
      additionalProperties: true
    ProtocolSuccess:
      type: object
      title: ProtocolSuccess
      description: Successful command response.
      required:
        - type
        - id
        - result
      properties:
        type:
          type: string
          const: success
        id:
          type: integer
          minimum: 0
        result:
          type: object
          description: Method-specific result payload.
          additionalProperties: true
        meta:
          $ref: '#/components/schemas/ProtocolResponseMeta'
      additionalProperties: true
    ProtocolError:
      type: object
      title: ProtocolError
      description: Error response for a command.
      required:
        - type
        - id
        - error
        - message
      properties:
        type:
          type: string
          const: error
        id:
          oneOf:
            - type: integer
              minimum: 0
            - type: 'null'
          description: >-
            The `id` of the offending command, or null if the envelope was
            unparseable.
        error:
          type: string
          enum:
            - invalid_argument
            - unknown_command
            - unknown_error
            - no_such_run
            - no_such_subscription
            - no_such_namespace
            - no_such_interrupt
            - no_such_checkpoint
            - permission_denied
            - not_supported
        message:
          type: string
        stacktrace:
          type: string
        meta:
          $ref: '#/components/schemas/ProtocolResponseMeta'
      additionalProperties: true
    ProtocolResponseMeta:
      type: object
      title: ProtocolResponseMeta
      description: Optional metadata attached to command responses.
      properties:
        applied_through_seq:
          type: integer
          minimum: 0
          description: >-
            Highest event `seq` observed on the session when this response was
            generated.
      additionalProperties: true

````

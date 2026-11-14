# Get Thread

> Get a thread by ID.



## OpenAPI

````yaml /langsmith/agent-server-openapi.json get /threads/{thread_id}
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
  /threads/{thread_id}:
    get:
      tags:
        - Threads
      summary: Get Thread
      description: Get a thread by ID.
      operationId: get_thread_threads__thread_id__get
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
        - description: >-
            Comma-separated list of additional fields to include. Supported
            values: ttl
          required: false
          schema:
            type: string
            title: Include
            description: Comma-separated list of additional fields to include.
          name: include
          in: query
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Thread'
        '404':
          description: Not Found
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
    Thread:
      properties:
        thread_id:
          type: string
          format: uuid
          title: Thread Id
          description: The ID of the thread.
        created_at:
          type: string
          format: date-time
          title: Created At
          description: The time the thread was created.
        updated_at:
          type: string
          format: date-time
          title: Updated At
          description: The last time the thread was updated.
        state_updated_at:
          type: string
          format: date-time
          title: State Updated At
          description: The last time the thread state was updated.
        metadata:
          type: object
          title: Metadata
          description: The thread metadata.
        config:
          type: object
          title: Config
          description: The thread config.
        status:
          type: string
          enum:
            - idle
            - busy
            - interrupted
            - error
          title: Status
          description: The status of the thread.
        values:
          type: object
          title: Values
          description: The current state of the thread.
        interrupts:
          type: object
          title: Interrupts
          description: The current interrupts of the thread.
        run_priority:
          type: integer
          minimum: -5
          maximum: 5
          title: Run Priority
          description: >-
            The queue priority level of the thread's runs, from -5 (highest
            priority) to 5 (lowest priority). Set at the thread's first run;
            null until then.
          nullable: true
        fairness_group:
          type: string
          title: Fairness Group
          description: >-
            A label for the thread's runs, such as a tenant or customer ID, kept
            for sharing workers fairly between tenants; scheduling doesn't use
            it yet. Set at the thread's first run with a default of "default";
            null until then.
          nullable: true
        ttl:
          type: object
          title: TTL Info
          description: >-
            TTL information if set for this thread. Only present when
            ?include=ttl is passed.
          properties:
            strategy:
              type: string
              enum:
                - delete
                - keep_latest
              description: The TTL strategy.
            ttl_minutes:
              type: number
              description: The TTL in minutes.
            expires_at:
              type: string
              format: date-time
              description: When the thread will expire.
        extracted:
          type: object
          title: Extracted
          description: >-
            Extracted values from thread JSONB columns, populated when extract
            is specified in search request.
      type: object
      required:
        - thread_id
        - created_at
        - updated_at
        - metadata
        - status
      title: Thread
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

````

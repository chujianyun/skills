# Search Threads

> Search for threads.

This endpoint also functions as the endpoint to list all threads.



## OpenAPI

````yaml /langsmith/agent-server-openapi.json post /threads/search
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
  /threads/search:
    post:
      tags:
        - Threads
      summary: Search Threads
      description: |-
        Search for threads.

        This endpoint also functions as the endpoint to list all threads.
      operationId: search_threads_threads_search_post
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ThreadSearchRequest'
        required: true
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                items:
                  $ref: '#/components/schemas/Thread'
                type: array
                title: Response Search Threads Threads Search Post
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
components:
  schemas:
    ThreadSearchRequest:
      properties:
        ids:
          type: array
          items:
            type: string
            format: uuid
          title: Ids
          description: List of thread IDs to include. Others are excluded.
        metadata:
          type: object
          title: Metadata
          description: Thread metadata to filter on.
        exclude_metadata:
          oneOf:
            - type: object
              minProperties: 1
            - type: array
              items:
                type: object
                minProperties: 1
              minItems: 1
          title: Exclude Metadata
          description: >-
            Exclude threads whose metadata contains this object, or any object
            in this list. Uses the same matching as `metadata`; threads missing
            the keys are not excluded.
        created_after:
          type: string
          format: date-time
          title: Created After
          description: >-
            Only include threads created at or after this time (ISO 8601).
            Timestamps without a timezone are treated as UTC.
        created_before:
          type: string
          format: date-time
          title: Created Before
          description: >-
            Only include threads created before this time (ISO 8601). Timestamps
            without a timezone are treated as UTC.
        state_updated_after:
          type: string
          format: date-time
          title: State Updated After
          description: >-
            Only include threads whose state last changed at or after this time
            (ISO 8601). Timestamps without a timezone are treated as UTC.
        state_updated_before:
          type: string
          format: date-time
          title: State Updated Before
          description: >-
            Only include threads whose state last changed before this time (ISO
            8601). Timestamps without a timezone are treated as UTC.
        values:
          type: object
          title: Values
          description: State values to filter on.
        status:
          type: string
          enum:
            - idle
            - busy
            - interrupted
            - error
          title: Status
          description: Thread status to filter on.
        limit:
          type: integer
          title: Limit
          description: Maximum number to return.
          default: 10
          minimum: 1
          maximum: 1000
        offset:
          type: integer
          title: Offset
          description: Offset to start from.
          default: 0
          minimum: 0
        sort_by:
          type: string
          enum:
            - thread_id
            - status
            - created_at
            - updated_at
            - state_updated_at
          title: Sort By
          description: Sort by field.
        sort_order:
          type: string
          enum:
            - asc
            - desc
          title: Sort Order
          description: Sort order.
        select:
          type: array
          items:
            type: string
            enum:
              - thread_id
              - created_at
              - updated_at
              - state_updated_at
              - metadata
              - config
              - status
              - values
              - interrupts
              - run_priority
              - fairness_group
          title: Select
          description: >-
            Specify which fields to return. If not provided, all fields are
            returned.
        extract:
          type: object
          additionalProperties:
            type: string
          title: Extract
          description: >-
            Map of alias to JSONB path for extracting specific values. Paths
            must start with values, metadata, config, or interrupts. Example:
            {"last_msg": "values.messages[-1]"}.
          maxProperties: 10
      type: object
      title: ThreadSearchRequest
      description: Payload for listing threads.
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

# Get Thread Storage

> Bytes the thread's checkpoints occupy in the built-in checkpointer, as stored: checkpoints, channel values (per channel) and pending writes. Returns 501 when a custom checkpointer is configured.



## OpenAPI

````yaml /langsmith/agent-server-openapi.json get /threads/{thread_id}/storage
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
  /threads/{thread_id}/storage:
    get:
      tags:
        - Threads
      summary: Get Thread Storage
      description: >-
        Bytes the thread's checkpoints occupy in the built-in checkpointer, as
        stored: checkpoints, channel values (per channel) and pending writes.
        Returns 501 when a custom checkpointer is configured.
      operationId: get_thread_storage_threads__thread_id__storage_get
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
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ThreadStorage'
        '404':
          description: Thread not found
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
    ThreadStorage:
      properties:
        thread_id:
          type: string
          format: uuid
          title: Thread Id
        total_bytes:
          type: integer
          title: Total Bytes
          description: Sum of the three sections below.
        checkpoints:
          type: object
          title: Checkpoints
          description: 'Checkpoint rows: serialized checkpoint plus metadata.'
          properties:
            count:
              type: integer
              title: Count
            bytes:
              type: integer
              title: Bytes
          required:
            - count
            - bytes
        channel_values:
          type: object
          title: Channel Values
          description: Stored channel values, one row per channel version.
          properties:
            count:
              type: integer
              title: Count
            bytes:
              type: integer
              title: Bytes
            by_channel:
              type: object
              title: By Channel
              additionalProperties:
                type: object
                properties:
                  versions:
                    type: integer
                    title: Versions
                  bytes:
                    type: integer
                    title: Bytes
                required:
                  - versions
                  - bytes
          required:
            - count
            - bytes
            - by_channel
        pending_writes:
          type: object
          title: Pending Writes
          description: Task writes not yet folded into a checkpoint.
          properties:
            count:
              type: integer
              title: Count
            bytes:
              type: integer
              title: Bytes
          required:
            - count
            - bytes
      type: object
      required:
        - thread_id
        - total_bytes
        - checkpoints
        - channel_values
        - pending_writes
      title: ThreadStorage
      description: Bytes a thread occupies in the checkpointer, as stored.
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

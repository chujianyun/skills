# Get Thread State At Checkpoint

> Get state for a thread at a specific checkpoint.



## OpenAPI

````yaml /langsmith/agent-server-openapi.json get /threads/{thread_id}/state/{checkpoint_id}
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
  /threads/{thread_id}/state/{checkpoint_id}:
    get:
      tags:
        - Threads
      summary: Get Thread State At Checkpoint
      description: Get state for a thread at a specific checkpoint.
      operationId: >-
        get_thread_state_at_checkpoint_threads__thread_id__state__checkpoint_id__get
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
        - description: The ID of the checkpoint.
          required: true
          schema:
            type: string
            format: uuid
            title: Checkpoint Id
            description: The ID of the checkpoint.
          name: checkpoint_id
          in: path
        - description: Whether to include subgraphs in the response.
          required: false
          schema:
            type: boolean
            title: Subgraphs
            description: Whether to include subgraphs in the response.
          name: subgraphs
          in: query
        - required: false
          schema:
            type: array
            items:
              anyOf:
                - type: string
                  enum:
                    - values
                    - next
                    - tasks
                    - checkpoint
                    - metadata
                    - created_at
                    - parent_checkpoint
                    - interrupts
                - type: string
                  pattern: ^values\.[A-Za-z0-9_-]+$
            title: Select
            description: >-
              Specify which fields of the state to return. Use `values.<key>` to
              return only that key of the state values, for example
              `values.messages`. If not provided, all fields are returned.
          name: select
          in: query
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ThreadState'
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
components:
  schemas:
    ThreadState:
      properties:
        values:
          anyOf:
            - items:
                type: object
              type: array
            - type: object
          title: Values
        next:
          items:
            type: string
          type: array
          title: Next
        tasks:
          items:
            type: object
            properties:
              id:
                type: string
                title: Task Id
              name:
                type: string
                title: Node Name
              error:
                type: string
                title: Error
              interrupts:
                type: array
                items:
                  $ref: '#/components/schemas/Interrupt'
              checkpoint:
                $ref: '#/components/schemas/CheckpointConfig'
                title: Checkpoint
              state:
                $ref: '#/components/schemas/ThreadState'
            required:
              - id
              - name
          type: array
          title: Tasks
        checkpoint:
          $ref: '#/components/schemas/CheckpointConfig'
          title: Checkpoint
        metadata:
          type: object
          title: Metadata
        created_at:
          type: string
          title: Created At
        parent_checkpoint:
          type: object
          title: Parent Checkpoint
        interrupts:
          type: array
          items:
            $ref: '#/components/schemas/Interrupt'
      type: object
      required:
        - values
        - next
        - checkpoint
        - metadata
        - created_at
      title: ThreadState
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
    Interrupt:
      type: object
      properties:
        id:
          type:
            - string
            - 'null'
        value:
          type: object
        response_schema:
          type: object
          description: >-
            JSON Schema for the value expected when resuming the interrupt, if
            the graph provided one.
      title: Interrupt
      required:
        - value
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

````

# Update Thread State

> Add state to a thread.



## OpenAPI

````yaml /langsmith/agent-server-openapi.json post /threads/{thread_id}/state
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
  /threads/{thread_id}/state:
    post:
      tags:
        - Threads
      summary: Update Thread State
      description: Add state to a thread.
      operationId: update_thread_state_threads__thread_id__state_post
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
              $ref: '#/components/schemas/ThreadStateUpdate'
        required: true
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ThreadStateUpdateResponse'
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
components:
  schemas:
    ThreadStateUpdate:
      properties:
        values:
          anyOf:
            - items: {}
              type: array
            - type: object
            - type: 'null'
          title: Values
          description: The values to update the state with.
        checkpoint:
          $ref: '#/components/schemas/CheckpointConfig'
          title: Checkpoint
          description: The checkpoint to update the state of.
        as_node:
          type: string
          title: As Node
          description: Update the state as if this node had just executed.
      type: object
      title: ThreadStateUpdate
      description: Payload for updating the state of a thread.
    ThreadStateUpdateResponse:
      properties:
        checkpoint:
          type: object
          title: Checkpoint
      type: object
      title: ThreadStateUpdateResponse
      description: Response for adding state to a thread.
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

````

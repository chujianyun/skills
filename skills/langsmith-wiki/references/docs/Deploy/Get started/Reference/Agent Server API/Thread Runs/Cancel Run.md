# Cancel Run



## OpenAPI

````yaml /langsmith/agent-server-openapi.json post /threads/{thread_id}/runs/{run_id}/cancel
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
  /threads/{thread_id}/runs/{run_id}/cancel:
    post:
      tags:
        - Thread Runs
      summary: Cancel Run
      operationId: cancel_run_http_threads__thread_id__runs__run_id__cancel_post
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
        - description: The ID of the run.
          required: true
          schema:
            type: string
            format: uuid
            title: Run Id
            description: The ID of the run.
          name: run_id
          in: path
        - required: false
          schema:
            type: boolean
            title: Wait
            default: false
          name: wait
          in: query
        - description: >-
            Action to take when cancelling the run. Possible values are
            `interrupt` or `rollback`. `interrupt` will simply cancel the run.
            `rollback` will cancel the run and delete the run and associated
            checkpoints afterwards.
          required: false
          schema:
            type: string
            enum:
              - interrupt
              - rollback
            title: Action
            default: interrupt
          name: action
          in: query
        - description: >-
            Use `taken` to mark run input absorbed for steering. Records a
            `cancel_reason` starting with `taken:`. Only supported with
            `action=interrupt`; cancellation behavior is unchanged. A 404
            response means the run was not cancelled.
          required: false
          schema:
            type: string
            enum:
              - taken
            title: Reason
          name: reason
          in: query
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema: {}
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

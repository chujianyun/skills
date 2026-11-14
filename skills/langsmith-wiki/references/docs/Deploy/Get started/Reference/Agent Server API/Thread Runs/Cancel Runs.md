# Cancel Runs

> Cancel one or more runs. Can cancel runs by thread ID and run IDs, or by status filter.



## OpenAPI

````yaml /langsmith/agent-server-openapi.json post /runs/cancel
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
  /runs/cancel:
    post:
      tags:
        - Thread Runs
      summary: Cancel Runs
      description: >-
        Cancel one or more runs. Can cancel runs by thread ID and run IDs, or by
        status filter.
      operationId: cancel_runs_post
      parameters:
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
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/RunsCancel'
        required: true
      responses:
        '204':
          description: Success - Runs cancelled
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
    RunsCancel:
      type: object
      title: RunsCancel
      description: Payload for cancelling runs.
      properties:
        status:
          type: string
          enum:
            - pending
            - running
            - all
          title: Status
          description: >-
            Filter runs by status to cancel. Must be one of 'pending',
            'running', or 'all'.
        thread_id:
          type: string
          format: uuid
          title: Thread Id
          description: The ID of the thread containing runs to cancel.
        run_ids:
          type: array
          items:
            type: string
            format: uuid
          title: Run Ids
          description: List of run IDs to cancel.
      oneOf:
        - required:
            - status
        - required:
            - thread_id
            - run_ids
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

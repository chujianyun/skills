# List Runs

> List runs for a thread.



## OpenAPI

````yaml /langsmith/agent-server-openapi.json get /threads/{thread_id}/runs
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
    get:
      tags:
        - Thread Runs
      summary: List Runs
      description: List runs for a thread.
      operationId: list_runs_http_threads__thread_id__runs_get
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
        - required: false
          schema:
            type: integer
            title: Limit
            default: 10
          name: limit
          in: query
        - required: false
          schema:
            type: integer
            title: Offset
            default: 0
          name: offset
          in: query
        - required: false
          schema:
            type: string
            enum:
              - pending
              - running
              - error
              - success
              - timeout
              - interrupted
          name: status
          in: query
        - required: false
          schema:
            type: array
            items:
              type: string
              enum:
                - run_id
                - thread_id
                - assistant_id
                - created_at
                - updated_at
                - status
                - metadata
                - kwargs
                - multitask_strategy
                - langsmith_session_name
                - cancel_reason
                - priority
            title: Select
            description: >-
              Specify which fields to return. If not provided, all fields are
              returned.
          name: select
          in: query
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                items:
                  $ref: '#/components/schemas/Run'
                type: array
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

````

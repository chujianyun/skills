# Get Cron

> Get a cron by ID.



## OpenAPI

````yaml /langsmith/agent-server-openapi.json get /runs/crons/{cron_id}
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
  /runs/crons/{cron_id}:
    get:
      tags:
        - Crons
      summary: Get Cron
      description: Get a cron by ID.
      operationId: get_cron_runs_crons__cron_id__get
      parameters:
        - required: true
          schema:
            type: string
            format: uuid
            title: Cron Id
          name: cron_id
          in: path
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Cron'
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
    Cron:
      properties:
        cron_id:
          type: string
          format: uuid
          title: Cron Id
          description: The ID of the cron.
        assistant_id:
          type:
            - string
            - 'null'
          format: uuid
          title: Assistant Id
          description: The ID of the assistant.
        thread_id:
          type: string
          format: uuid
          title: Thread Id
          description: The ID of the thread.
        end_time:
          type: string
          format: date-time
          title: End Time
          description: The end date to stop running the cron.
        schedule:
          type: string
          title: Schedule
          description: The schedule to run, cron format.
        created_at:
          type: string
          format: date-time
          title: Created At
          description: The time the cron was created.
        updated_at:
          type: string
          format: date-time
          title: Updated At
          description: The last time the cron was updated.
        user_id:
          type:
            - string
            - 'null'
          title: User Id
          description: The ID of the user.
        payload:
          type: object
          title: Payload
          description: The run payload to use for creating new run.
        next_run_date:
          type:
            - string
            - 'null'
          format: date-time
          title: Next Run Date
          description: The next run date of the cron.
        metadata:
          type: object
          title: Metadata
          description: The cron metadata.
        enabled:
          type: boolean
          title: Enabled
          description: >-
            Whether the cron job should be enabled. Disabled crons are not
            executed.
          default: true
      type: object
      required:
        - cron_id
        - thread_id
        - end_time
        - schedule
        - created_at
        - updated_at
        - payload
        - enabled
      title: Cron
      description: Represents a scheduled task.
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

# Search Crons

> Search all active crons



## OpenAPI

````yaml /langsmith/agent-server-openapi.json post /runs/crons/search
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
  /runs/crons/search:
    post:
      tags:
        - Crons
      summary: Search Crons
      description: Search all active crons
      operationId: search_crons_runs_crons_post
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CronSearch'
        required: true
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                items:
                  $ref: '#/components/schemas/Cron'
                type: array
                title: Response Search Crons Search Post
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
components:
  schemas:
    CronSearch:
      properties:
        assistant_id:
          type: string
          format: uuid
          title: Assistant Id
          description: The assistant ID or graph name to filter by using exact match.
        thread_id:
          type: string
          format: uuid
          title: Thread Id
          description: The thread ID to search for.
        enabled:
          type: boolean
          title: Enabled
          description: >-
            Filter by enabled status. If not provided, returns both enabled and
            disabled crons.
        metadata:
          type: object
          title: Metadata
          description: Metadata to filter by. Exact match filter for each KV pair.
        limit:
          type: integer
          title: Limit
          description: The maximum number of results to return.
          default: 10
          minimum: 1
          maximum: 1000
        offset:
          type: integer
          title: Offset
          description: The number of results to skip.
          default: 0
          minimum: 0
        sort_by:
          type: string
          title: Sort By
          description: The field to sort by.
          default: created_at
          enum:
            - cron_id
            - assistant_id
            - thread_id
            - next_run_date
            - end_time
            - created_at
            - updated_at
        sort_order:
          type: string
          title: Sort Order
          description: The order to sort by.
          default: desc
          enum:
            - asc
            - desc
        select:
          type: array
          items:
            type: string
            enum:
              - cron_id
              - assistant_id
              - thread_id
              - on_run_completed
              - end_time
              - schedule
              - timezone
              - created_at
              - updated_at
              - user_id
              - payload
              - next_run_date
              - metadata
              - enabled
          title: Select
          description: >-
            Specify which fields to return. If not provided, all fields are
            returned.
      type: object
      required: []
      title: CronSearch
      description: Payload for listing crons
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

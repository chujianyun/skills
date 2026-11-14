# Update Cron

> Update a cron job by ID.



## OpenAPI

````yaml /langsmith/agent-server-openapi.json patch /runs/crons/{cron_id}
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
    patch:
      tags:
        - Crons
      summary: Update Cron
      description: Update a cron job by ID.
      operationId: patch_cron_runs_crons__cron_id__patch
      parameters:
        - required: true
          schema:
            type: string
            format: uuid
            title: Cron Id
          name: cron_id
          in: path
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CronPatch'
        required: true
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
    CronPatch:
      properties:
        schedule:
          type: string
          title: Schedule
          description: The cron schedule to execute this job on.
        timezone:
          type: string
          title: Timezone
          description: >-
            IANA timezone for the cron schedule (e.g. 'America/New_York').
            Defaults to null, which is treated as UTC.
        end_time:
          type:
            - string
            - 'null'
          format: date-time
          title: End Time
          description: >-
            The end date to stop running the cron. Send null to clear a
            previously set end time; omit this field to leave the existing value
            unchanged.
        input:
          anyOf:
            - items:
                type: object
              type: array
            - type: object
          title: Input
          description: The input to the graph.
        metadata:
          type: object
          title: Metadata
          description: Metadata to merge with existing cron job metadata.
        config:
          properties:
            tags:
              items:
                type: string
              type: array
              title: Tags
            recursion_limit:
              type: integer
              title: Recursion Limit
            configurable:
              type: object
              title: Configurable
          type: object
          title: Config
          description: The configuration for the assistant.
        context:
          type: object
          title: Context
          description: Static context added to the assistant.
        webhook:
          type: string
          maxLength: 65536
          minLength: 1
          format: uri-reference
          title: Webhook
          description: Webhook to call after LangGraph API call is done.
        interrupt_before:
          anyOf:
            - type: string
              enum:
                - '*'
            - items:
                type: string
              type: array
          title: Interrupt Before
          description: Nodes to interrupt immediately before they get executed.
        interrupt_after:
          anyOf:
            - type: string
              enum:
                - '*'
            - items:
                type: string
              type: array
          title: Interrupt After
          description: Nodes to interrupt immediately after they get executed.
        on_run_completed:
          type: string
          enum:
            - delete
            - keep
          title: On Run Completed
          description: >-
            What to do with the thread after the run completes. 'delete' removes
            the thread after execution. 'keep' creates a new thread for each
            execution but does not clean them up.
        enabled:
          type: boolean
          title: Enabled
          description: Enable or disable the cron job.
        stream_mode:
          anyOf:
            - items:
                type: string
                enum:
                  - values
                  - messages
                  - messages-tuple
                  - tasks
                  - checkpoints
                  - updates
                  - events
                  - debug
                  - custom
              type: array
            - type: string
              enum:
                - values
                - messages
                - messages-tuple
                - tasks
                - checkpoints
                - updates
                - events
                - debug
                - custom
          title: Stream Mode
          description: The stream mode(s) to use.
          default:
            - values
        stream_subgraphs:
          type: boolean
          title: Stream Subgraphs
          description: Whether to stream output from subgraphs.
          default: false
        stream_resumable:
          type: boolean
          title: Stream Resumable
          description: >-
            Whether to keep the run's stream events so a client can rejoin the
            run. Deployments keep every run's events for
            `RESUMABLE_STREAM_TTL_SECONDS` (2 minutes by default) regardless of
            this field. The in-memory runtime (`langgraph dev`) keeps them only
            when it is true.
          default: false
        durability:
          type: string
          enum:
            - sync
            - async
            - exit
          title: Durability
          description: >-
            Durability level for the run. Must be one of `sync`, `async`, or
            `exit`. See [durability
            modes](https://docs.langchain.com/oss/python/langgraph/checkpointers#durability-modes)
            for more details.
          default: async
      type: object
      title: CronPatch
      description: Payload for updating a cron job. All fields are optional.
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

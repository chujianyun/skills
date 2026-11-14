# Join Run Stream

> Join a run stream. This endpoint streams output in real-time from a run similar to the /threads/__THREAD_ID__/runs/stream endpoint. The stream can be resumed from the last seen event ID, or from a checkpoint of the run with `checkpoint_id`. In the in-memory runtime (`langgraph dev`), only a run created with `stream_resumable=true` can be resumed. A `gap` event is sent, first on a resume or mid-stream, when events the client should receive may be missing. Its `reason` is `expired` when they may have aged out of the stream's history; `unknown_id` when the `Last-Event-ID` is later than any event the thread streamed, and the stream starts over from the run's first event; or `too_large` when an event was over the size limit, with that event's stream mode in `mode`. `expired` errs on the safe side: once the stream's history has expired, a resume gets it unless its ID is the thread's last streamed event, which is kept for an hour after that.



## OpenAPI

````yaml /langsmith/agent-server-openapi.json get /threads/{thread_id}/runs/{run_id}/stream
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
  /threads/{thread_id}/runs/{run_id}/stream:
    get:
      tags:
        - Thread Runs
      summary: Join Run Stream
      description: >-
        Join a run stream. This endpoint streams output in real-time from a run
        similar to the /threads/__THREAD_ID__/runs/stream endpoint. The stream
        can be resumed from the last seen event ID, or from a checkpoint of the
        run with `checkpoint_id`. In the in-memory runtime (`langgraph dev`),
        only a run created with `stream_resumable=true` can be resumed. A `gap`
        event is sent, first on a resume or mid-stream, when events the client
        should receive may be missing. Its `reason` is `expired` when they may
        have aged out of the stream's history; `unknown_id` when the
        `Last-Event-ID` is later than any event the thread streamed, and the
        stream starts over from the run's first event; or `too_large` when an
        event was over the size limit, with that event's stream mode in `mode`.
        `expired` errs on the safe side: once the stream's history has expired,
        a resume gets it unless its ID is the thread's last streamed event,
        which is kept for an hour after that.
      operationId: stream_run_http_threads__thread_id__runs__run_id__join_get
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
            type: string
            title: Last Event ID
            description: >-
              The ID of the last event received. Set to -1 if you want to stream
              all events. In the in-memory runtime (`langgraph dev`), requires
              `stream_resumable=true` when creating the run.
          name: Last-Event-ID
          in: header
        - required: false
          schema:
            type: string
            format: uuid
            title: Checkpoint ID
            description: >-
              Resume after this checkpoint of the run, such as the one the
              thread's state was just loaded at: events up to the checkpoint are
              skipped. Used when `Last-Event-ID` is absent, `-` or `-1`; a real
              `Last-Event-ID` takes precedence. If the run's stream has no
              record of the checkpoint, the stream starts from the beginning of
              the run, as with -1. Send it with `Last-Event-ID: -1`, so a server
              that ignores it replays the whole run instead of streaming only
              new events. The in-memory runtime (`langgraph dev`) ignores it and
              replays the whole run, which needs `stream_resumable=true` when
              creating the run.
          name: checkpoint_id
          in: query
        - required: false
          schema:
            anyOf:
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
                  - tools
                  - lifecycle
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
                    - tools
                    - lifecycle
                type: array
            title: Stream Mode
            description: >-
              Stream modes to control which of the run's events are returned.
              Only modes the run was created with have events. Events about the
              whole run, such as `metadata` (which starts each attempt of the
              run), `error` and `feedback`, always pass, except on the
              `langgraph dev` server, which passes only `error`. If not
              provided, all of the run's events are returned.
          name: stream_mode
          in: query
        - required: false
          schema:
            type: array
            items:
              type: string
            maxItems: 32
            title: Namespace
            description: >-
              A conversation to stream: a `|`-joined namespace, empty for the
              main agent (the root graph) or a subagent's, such as
              `tools:<task_id>`. The stream keeps that conversation's events
              without those of the subagents it starts (subgraphs that the
              `tools` node runs), but with the `lifecycle` events of every
              subagent below it. Repeat it to stream several conversations.
              Events about the whole run, such as `metadata` and `error`, always
              pass. Events of the `events` and `messages` modes (not
              `messages-tuple`) carry no namespace, so they stream with the main
              agent's conversation. Subagent events exist only on runs created
              with `stream_subgraphs`, except `lifecycle` events, which come
              either way. If not provided, all of the run's events are returned.
          name: namespace
          in: query
        - required: false
          schema:
            type: boolean
            title: Cancel On Disconnect
            description: If true, the run will be cancelled if the client disconnects.
            default: false
          name: cancel_on_disconnect
          in: query
      responses:
        '200':
          description: Success
          content:
            text/event-stream:
              schema:
                type: string
                description: >-
                  The server will send a stream of events in SSE format. The
                  last event is `end`, with data `{"run_id": ..., "status":
                  ...}` giving the run's final status: `success` (also when the
                  run stops at an interrupt), `error`, `timeout`, `interrupted`
                  (the run was cancelled) or, for a stateless run, `rollback`. A
                  run that was deleted, or rolled back on a thread, has no
                  status left, so its stream ends with its `error` event
                  instead. If a stream closes with neither, get the run to see
                  how it ended.


                  **Example event**:


                  id: 1


                  event: message


                  data: {}
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

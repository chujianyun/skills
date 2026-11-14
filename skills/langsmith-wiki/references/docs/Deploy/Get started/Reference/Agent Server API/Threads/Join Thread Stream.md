# Join Thread Stream

> This endpoint streams output in real-time from a thread. The stream will include the output of each run executed sequentially on the thread and will remain open indefinitely. It is the responsibility of the calling client to close the connection.



## OpenAPI

````yaml /langsmith/agent-server-openapi.json get /threads/{thread_id}/stream
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
  /threads/{thread_id}/stream:
    get:
      tags:
        - Threads
      summary: Join Thread Stream
      description: >-
        This endpoint streams output in real-time from a thread. The stream will
        include the output of each run executed sequentially on the thread and
        will remain open indefinitely. It is the responsibility of the calling
        client to close the connection.
      operationId: join_thread_stream_threads__thread_id__stream_get
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
            type: string
            title: Last Event ID
            description: >-
              The ID of the last event received. Used to resume streaming from a
              specific point. Pass '-' to resume from the beginning. A `gap`
              event is sent, first on a resume or mid-stream, when events the
              client should receive may be missing. Its `reason` is `expired`
              when they may have aged out of the stream's history; `unknown_id`
              when the ID is later than any event the thread streamed, and the
              stream starts over from the beginning; or `too_large` when an
              event was over the size limit, with that event's stream mode in
              `mode`. `expired` errs on the safe side: once the stream's history
              has expired, a resume gets it unless its ID is the thread's last
              streamed event, which is kept for an hour after that.
          name: Last-Event-ID
          in: header
        - required: false
          schema:
            anyOf:
              - type: string
                enum:
                  - lifecycle
                  - run_modes
                  - state_update
              - type: array
                items:
                  type: string
                  enum:
                    - lifecycle
                    - run_modes
                    - state_update
            default:
              - run_modes
            title: Stream Modes
            description: >-
              Stream modes to control which events are returned. 'lifecycle'
              returns only run start/end events and `interrupts` events (the
              interrupts a run answers), 'run_modes' returns all run events
              (default behavior), 'state_update' returns only state update
              events.
          name: stream_modes
          in: query
        - required: false
          schema:
            anyOf:
              - type: string
                enum:
                  - lifecycle
                  - run_modes
                  - state_update
              - type: array
                items:
                  type: string
                  enum:
                    - lifecycle
                    - run_modes
                    - state_update
            title: Stream Mode
            description: >-
              Alias of `stream_modes`, the name the SDKs send. Ignored when
              `stream_modes` is set.
          name: stream_mode
          in: query
      responses:
        '200':
          description: Success
          content:
            text/event-stream:
              schema:
                type: string
                description: |-
                  The server will send a stream of events in SSE format.

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

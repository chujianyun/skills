# Protocol v2 Event Stream (SSE)

> Open a connection-scoped SSE event stream for a thread. The request body is a `ProtocolEventStreamRequest` carrying channel and namespace filters; the server replies with `Content-Type: text/event-stream` and pushes matching `ProtocolEvent` frames for the lifetime of the connection. Closing the connection unsubscribes — no state is persisted server-side.

Reconnect: clients pass the last `seq` they received as `since` in the body. Buffered events with `seq > since` are replayed before the stream goes live. The endpoint is POST-only, so browser-native `EventSource` auto-resume (`Last-Event-ID`) does not apply — clients drive resume explicitly via the body.



## OpenAPI

````yaml /langsmith/agent-server-openapi.json post /threads/{thread_id}/stream/events
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
  /threads/{thread_id}/stream/events:
    post:
      tags:
        - Streaming
      summary: Protocol v2 Event Stream (SSE)
      description: >-
        Open a connection-scoped SSE event stream for a thread. The request body
        is a `ProtocolEventStreamRequest` carrying channel and namespace
        filters; the server replies with `Content-Type: text/event-stream` and
        pushes matching `ProtocolEvent` frames for the lifetime of the
        connection. Closing the connection unsubscribes — no state is persisted
        server-side.


        Reconnect: clients pass the last `seq` they received as `since` in the
        body. Buffered events with `seq > since` are replayed before the stream
        goes live. The endpoint is POST-only, so browser-native `EventSource`
        auto-resume (`Last-Event-ID`) does not apply — clients drive resume
        explicitly via the body.
      operationId: protocol_thread_events_post
      parameters:
        - name: thread_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
            title: Thread Id
            description: The ID of the thread to observe.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ProtocolEventStreamRequest'
      responses:
        '200':
          description: SSE event stream
          content:
            text/event-stream:
              schema:
                type: string
                description: >-
                  Stream of `ProtocolEvent` frames. Each SSE frame uses the
                  event's `method` as the `event:` field and a JSON-encoded
                  `ProtocolEvent` as the `data:` field; `id:` is set to the
                  event's `seq`.


                  If reading the thread's event stream fails, the server ends
                  the stream with a final frame whose `event:` field is `error`
                  and whose `data:` field is a `ProtocolError` with `id: null`
                  and `error: "unknown_error"`. That frame has no `id:` field.


                  **Example frame:**


                  id: 42


                  event: messages


                  data:
                  {"type":"event","event_id":"42","seq":42,"method":"messages","params":{"namespace":[],"timestamp":1700000000000,"data":{...}}}
        '400':
          description: Invalid request body
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
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
    ProtocolEventStreamRequest:
      type: object
      title: ProtocolEventStreamRequest
      description: >-
        Body of `POST /threads/{thread_id}/stream/events`. Filters the
        connection-scoped SSE stream.
      required:
        - channels
      properties:
        channels:
          type: array
          items:
            $ref: '#/components/schemas/ProtocolChannel'
          minItems: 1
          description: Channels to subscribe to for the lifetime of this connection.
        namespaces:
          type: array
          items:
            $ref: '#/components/schemas/ProtocolNamespace'
          description: >-
            Prefix-match filter. An event matches if its namespace starts with
            any of these prefixes. Omit for all namespaces.
        depth:
          type: integer
          minimum: 0
          description: Max depth below the namespace prefix. Omit for unbounded depth.
        since:
          type: integer
          minimum: 0
          description: >-
            Replay events with `seq` greater than this value before streaming
            live events.
      additionalProperties: true
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
    ProtocolChannel:
      type: string
      title: Protocol Channel
      description: >-
        Subscribable event channel. One of the eight fixed channels or a
        user-defined `custom:<name>` namespaced custom channel emitted by a
        stream transformer. `debug` and `checkpoints` were removed from the
        protocol in `@langchain/protocol@0.0.10` — task-level debug info now
        flows on the `tasks` channel, and checkpoint pointers ride on `values`
        events as an attached `checkpoint` envelope.
      anyOf:
        - type: string
          enum:
            - values
            - updates
            - messages
            - tools
            - lifecycle
            - input
            - tasks
            - custom
        - type: string
          pattern: ^custom:.+$
          description: User-defined namespaced custom channel.
    ProtocolNamespace:
      type: array
      items:
        type: string
      title: Protocol Namespace
      description: >-
        Hierarchical path identifying a position in the agent tree. Empty array
        denotes the root agent; each segment names a nested subgraph.

````

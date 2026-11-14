# MCP Post

> Implemented according to the Streamable HTTP Transport specification.
Sends a JSON-RPC 2.0 message to the server.

- **Request**: Provide an object with `jsonrpc`, `id`, `method`, and optional `params`.
- **Response**: Returns a JSON-RPC response or acknowledgment.

**Notes:**
- Stateless: Sessions are not persisted across requests.




## OpenAPI

````yaml /langsmith/agent-server-openapi.json post /mcp/
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
  /mcp/:
    post:
      tags:
        - MCP
      summary: MCP Post
      description: >
        Implemented according to the Streamable HTTP Transport specification.

        Sends a JSON-RPC 2.0 message to the server.


        - **Request**: Provide an object with `jsonrpc`, `id`, `method`, and
        optional `params`.

        - **Response**: Returns a JSON-RPC response or acknowledgment.


        **Notes:**

        - Stateless: Sessions are not persisted across requests.
      operationId: post_mcp
      parameters:
        - name: Accept
          in: header
          required: true
          schema:
            type: string
            enum:
              - application/json, text/event-stream
          description: >-
            Accept header must include both 'application/json' and
            'text/event-stream' media types.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              description: A JSON-RPC 2.0 request, notification, or response object.
            example:
              jsonrpc: '2.0'
              id: '1'
              method: initialize
              params:
                clientInfo:
                  name: test_client
                  version: 1.0.0
                protocolVersion: '2024-11-05'
                capabilities: {}
      responses:
        '200':
          description: Successful JSON-RPC response.
          content:
            application/json:
              schema:
                type: object
        '202':
          description: Notification or response accepted; no content body.
        '400':
          description: >-
            Bad request: invalid JSON or message format, or unacceptable Accept
            header.
        '405':
          description: HTTP method not allowed.
        '500':
          description: Internal server error or unexpected failure.

````

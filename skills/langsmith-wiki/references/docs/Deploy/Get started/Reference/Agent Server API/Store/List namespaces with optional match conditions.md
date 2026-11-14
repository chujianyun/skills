# List namespaces with optional match conditions.



## OpenAPI

````yaml /langsmith/agent-server-openapi.json post /store/namespaces
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
  /store/namespaces:
    post:
      tags:
        - Store
      summary: List namespaces with optional match conditions.
      operationId: list_namespaces
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/StoreListNamespacesRequest'
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ListNamespaceResponse'
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
components:
  schemas:
    StoreListNamespacesRequest:
      type: object
      properties:
        prefix:
          type: array
          items:
            type: string
          title: Prefix
          description: >-
            Optional list of strings representing the prefix to filter
            namespaces.
        suffix:
          type: array
          items:
            type: string
          title: Suffix
          description: >-
            Optional list of strings representing the suffix to filter
            namespaces.
        max_depth:
          type: integer
          title: Max Depth
          description: >-
            Optional integer specifying the maximum depth of namespaces to
            return.
        limit:
          type: integer
          default: 100
          title: Limit
          description: Maximum number of namespaces to return (default is 100).
        offset:
          type: integer
          default: 0
          title: Offset
          description: >-
            Number of namespaces to skip before returning results (default is
            0).
    ListNamespaceResponse:
      type: array
      items:
        items:
          type: string
        type: array
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

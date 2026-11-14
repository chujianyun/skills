# Store or update an item.



## OpenAPI

````yaml /langsmith/agent-server-openapi.json put /store/items
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
  /store/items:
    put:
      tags:
        - Store
      summary: Store or update an item.
      operationId: put_item
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/StorePutRequest'
      responses:
        '204':
          description: Success
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
components:
  schemas:
    StorePutRequest:
      type: object
      required:
        - namespace
        - key
        - value
      properties:
        namespace:
          type: array
          items:
            type: string
          title: Namespace
          description: A list of strings representing the namespace path.
        key:
          type: string
          title: Key
          description: The unique identifier for the item within the namespace.
        value:
          type: object
          title: Value
          description: A dictionary containing the item's data.
        index:
          oneOf:
            - type: boolean
              enum:
                - false
            - items:
                type: string
              type: array
            - type: 'null'
          default: null
          title: Index
          description: >-
            Controls search indexing - null (use defaults), false (disable), or
            list of field paths to index.
        ttl:
          type:
            - number
            - 'null'
          default: null
          title: TTL
          description: >-
            Optional time-to-live in minutes for the item, or null for no
            expiration.
      title: StorePutRequest
      description: Request to store or update an item.
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

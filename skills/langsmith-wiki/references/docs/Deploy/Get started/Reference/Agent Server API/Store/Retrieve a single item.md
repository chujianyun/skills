# Retrieve a single item.



## OpenAPI

````yaml /langsmith/agent-server-openapi.json get /store/items
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
    get:
      tags:
        - Store
      summary: Retrieve a single item.
      operationId: get_item
      parameters:
        - name: key
          in: query
          required: true
          schema:
            type: string
        - name: namespace
          in: query
          required: false
          schema:
            items:
              type: string
            type: array
        - name: refresh_ttl
          in: query
          required: false
          schema:
            type: boolean
          description: >-
            Whether to refresh the TTL on this read operation. If not provided,
            uses the store's default behavior.
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Item'
        '400':
          description: Bad Request
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
    Item:
      type: object
      required:
        - namespace
        - key
        - value
        - created_at
        - updated_at
      properties:
        namespace:
          type: array
          items:
            type: string
          description: >-
            The namespace of the item. A namespace is analogous to a document's
            directory.
        key:
          type: string
          description: >-
            The unique identifier of the item within its namespace. In general,
            keys needn't be globally unique.
        value:
          type: object
          description: The value stored in the item. This is the document itself.
        created_at:
          type: string
          format: date-time
          description: The timestamp when the item was created.
        updated_at:
          type: string
          format: date-time
          description: The timestamp when the item was last updated.
      description: >-
        Represents a single document or data entry in the graph's Store. Items
        are used to store cross-thread memories.
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

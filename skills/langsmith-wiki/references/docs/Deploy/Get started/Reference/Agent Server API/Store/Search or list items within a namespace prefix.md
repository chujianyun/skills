# Search or list items within a namespace prefix.

> Lists items ordered by last updated time. If a `query` is provided, performs a natural language search instead. Supports pagination via `limit` and `offset`, and filtering via `filter`.



## OpenAPI

````yaml /langsmith/agent-server-openapi.json post /store/items/search
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
  /store/items/search:
    post:
      tags:
        - Store
      summary: Search or list items within a namespace prefix.
      description: >-
        Lists items ordered by last updated time. If a `query` is provided,
        performs a natural language search instead. Supports pagination via
        `limit` and `offset`, and filtering via `filter`.
      operationId: search_items
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/StoreSearchRequest'
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/SearchItemsResponse'
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
components:
  schemas:
    StoreSearchRequest:
      type: object
      properties:
        namespace_prefix:
          type:
            - array
            - 'null'
          items:
            type: string
          title: Namespace Prefix
          description: List of strings representing the namespace prefix.
        filter:
          type:
            - object
            - 'null'
          additionalProperties: true
          title: Filter
          description: Optional dictionary of key-value pairs to filter results.
        limit:
          type: integer
          default: 10
          title: Limit
          description: Maximum number of items to return (default is 10).
        offset:
          type: integer
          default: 0
          title: Offset
          description: Number of items to skip before returning results (default is 0).
        query:
          type:
            - string
            - 'null'
          title: Query
          description: >-
            Optional natural language search query. If not provided, items are
            returned ordered by last updated time (listing mode). If provided,
            performs a natural language search over item contents.
        refresh_ttl:
          type:
            - boolean
            - 'null'
          default: null
          title: Refresh TTL
          description: >-
            Whether to refresh the TTL on items returned by this search. If
            null, uses the store's default behavior.
      title: StoreSearchRequest
      description: >-
        Request to list or search for items within a namespace prefix. Without a
        query, lists items by last updated time. With a query, performs natural
        language search.
    SearchItemsResponse:
      type: object
      required:
        - items
      properties:
        items:
          type: array
          items:
            $ref: '#/components/schemas/Item'
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

````

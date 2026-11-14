# Search Assistants

> Search for assistants.

This endpoint also functions as the endpoint to list all assistants.



## OpenAPI

````yaml /langsmith/agent-server-openapi.json post /assistants/search
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
  /assistants/search:
    post:
      tags:
        - Assistants
      summary: Search Assistants
      description: |-
        Search for assistants.

        This endpoint also functions as the endpoint to list all assistants.
      operationId: search_assistants_assistants_search_post
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AssistantSearchRequest'
        required: true
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                items:
                  $ref: '#/components/schemas/Assistant'
                type: array
                title: Response Search Assistants Assistants Search Post
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
    AssistantSearchRequest:
      properties:
        metadata:
          type: object
          title: Metadata
          description: Metadata to filter by. Exact match filter for each KV pair.
        graph_id:
          type: string
          title: Graph Id
          description: >-
            The ID of the graph to filter by. The graph ID is normally set in
            your langgraph.json configuration.
        name:
          type: string
          title: Name
          description: >-
            Name of the assistant to filter by. The filtering logic will match
            (case insensitive) assistants where 'name' is a substring of the
            assistant name.
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
          enum:
            - assistant_id
            - created_at
            - updated_at
            - name
            - graph_id
          title: Sort By
          description: The field to sort by.
        sort_order:
          type: string
          enum:
            - asc
            - desc
          title: Sort Order
          description: The order to sort by.
        select:
          type: array
          items:
            type: string
            enum:
              - assistant_id
              - graph_id
              - name
              - description
              - config
              - context
              - created_at
              - updated_at
              - metadata
              - version
          title: Select
          description: >-
            Specify which fields to return. If not provided, all fields are
            returned.
      type: object
      title: AssistantSearchRequest
      description: Payload for listing assistants.
    Assistant:
      properties:
        assistant_id:
          type: string
          format: uuid
          title: Assistant Id
          description: The ID of the assistant.
        graph_id:
          type: string
          title: Graph Id
          description: The ID of the graph.
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
          description: The assistant config.
        context:
          type: object
          title: Context
          description: Static context added to the assistant.
        created_at:
          type: string
          format: date-time
          title: Created At
          description: The time the assistant was created.
        updated_at:
          type: string
          format: date-time
          title: Updated At
          description: The last time the assistant was updated.
        metadata:
          type: object
          title: Metadata
          description: The assistant metadata.
        version:
          type: integer
          title: Version
          description: The version of the assistant
        name:
          type: string
          title: Assistant Name
          description: The name of the assistant
        description:
          type:
            - string
            - 'null'
          title: Assistant Description
          description: The description of the assistant
      type: object
      required:
        - assistant_id
        - graph_id
        - config
        - created_at
        - updated_at
        - metadata
      title: Assistant
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

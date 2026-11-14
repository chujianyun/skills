# Count Assistants

> Get the count of assistants matching the specified criteria.



## OpenAPI

````yaml /langsmith/agent-server-openapi.json post /assistants/count
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
  /assistants/count:
    post:
      tags:
        - Assistants
      summary: Count Assistants
      description: Get the count of assistants matching the specified criteria.
      operationId: count_assistants_assistants_count_post
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AssistantCountRequest'
        required: true
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                type: integer
                title: Count
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
    AssistantCountRequest:
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
      type: object
      title: AssistantCountRequest
      description: Payload for counting assistants.
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

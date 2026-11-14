# Get Assistant

> Get an assistant by ID.



## OpenAPI

````yaml /langsmith/agent-server-openapi.json get /assistants/{assistant_id}
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
  /assistants/{assistant_id}:
    get:
      tags:
        - Assistants
      summary: Get Assistant
      description: Get an assistant by ID.
      operationId: get_assistant_assistants__assistant_id__get
      parameters:
        - description: The ID of the assistant.
          required: true
          schema:
            type: string
            format: uuid
            title: Assistant ID
            description: The ID of the assistant.
          name: assistant_id
          in: path
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Assistant'
        '404':
          description: Not Found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
components:
  schemas:
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

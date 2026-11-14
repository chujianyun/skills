# Get Assistant Schemas

> Get an assistant by ID.



## OpenAPI

````yaml /langsmith/agent-server-openapi.json get /assistants/{assistant_id}/schemas
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
  /assistants/{assistant_id}/schemas:
    get:
      tags:
        - Assistants
      summary: Get Assistant Schemas
      description: Get an assistant by ID.
      operationId: get_assistant_schemas_assistants__assistant_id__schemas_get
      parameters:
        - description: The ID of the assistant.
          required: true
          schema:
            type: string
            format: uuid
            title: Assistant Id
            description: The ID of the assistant.
          name: assistant_id
          in: path
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/GraphSchema'
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
    GraphSchema:
      properties:
        graph_id:
          type: string
          title: Graph Id
          description: The ID of the graph.
        input_schema:
          type: object
          title: Input Schema
          description: >-
            The schema for the graph input. Missing if unable to generate JSON
            schema from graph.
        output_schema:
          type: object
          title: Output Schema
          description: >-
            The schema for the graph output. Missing if unable to generate JSON
            schema from graph.
        state_schema:
          type: object
          title: State Schema
          description: >-
            The schema for the graph state. Missing if unable to generate JSON
            schema from graph.
        config_schema:
          type: object
          title: Config Schema
          description: >-
            The schema for the graph config. Missing if unable to generate JSON
            schema from graph.
        context_schema:
          type: object
          title: Context Schema
          description: >-
            The schema for the graph context. Missing if unable to generate JSON
            schema from graph.
      type: object
      required:
        - graph_id
        - state_schema
      title: GraphSchema
      description: Defines the structure and properties of a graph.
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

# Get Assistant Subgraphs

> Get an assistant's subgraphs.



## OpenAPI

````yaml /langsmith/agent-server-openapi.json get /assistants/{assistant_id}/subgraphs
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
  /assistants/{assistant_id}/subgraphs:
    get:
      tags:
        - Assistants
      summary: Get Assistant Subgraphs
      description: Get an assistant's subgraphs.
      operationId: get_assistant_subgraphs_assistants__assistant_id__subgraphs_get
      parameters:
        - description: The ID of the assistant.
          required: true
          schema:
            type: string
            format: uuid
            title: Assistant Id
          name: assistant_id
          in: path
        - description: Recursively retrieve subgraphs of subgraphs.
          required: false
          schema:
            type: boolean
            title: Recurse
            default: false
          name: recurse
          in: query
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Subgraphs'
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
    Subgraphs:
      type: object
      additionalProperties:
        $ref: '#/components/schemas/GraphSchemaNoId'
      title: Subgraphs
      description: >-
        Map of graph name to graph schema metadata (`input_schema`,
        `output_schema`, `state_schema`, `config_schema`, `context_schema`).
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
    GraphSchemaNoId:
      properties:
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
        - input_schema
        - output_schema
        - state_schema
      title: GraphSchemaNoId
      description: Defines the structure and properties of a graph without an ID.

````

# System Metrics

> Get system metrics in Prometheus or JSON format for monitoring and observability.



## OpenAPI

````yaml /langsmith/agent-server-openapi.json get /metrics
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
  /metrics:
    get:
      tags:
        - System
      summary: System Metrics
      description: >-
        Get system metrics in Prometheus or JSON format for monitoring and
        observability.
      operationId: system_metrics_metrics_get
      parameters:
        - name: format
          in: query
          required: false
          schema:
            type: string
            enum:
              - prometheus
              - json
            default: prometheus
            title: Output Format
            description: 'Response format: prometheus (default) or json'
      responses:
        '200':
          description: Success
          content:
            text/plain:
              schema:
                type: string
                title: Prometheus Metrics
                description: Metrics in Prometheus exposition format
            application/json:
              schema:
                type: object
                title: JSON Metrics
                description: >-
                  Metrics in JSON format including queue stats, worker stats,
                  and HTTP metrics

````

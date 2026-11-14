# Prune Threads

> Prune threads by ID. The 'delete' strategy removes threads entirely. The 'keep_latest' strategy prunes old checkpoints but keeps threads and their latest state.



## OpenAPI

````yaml /langsmith/agent-server-openapi.json post /threads/prune
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
  /threads/prune:
    post:
      tags:
        - Threads
      summary: Prune Threads
      description: >-
        Prune threads by ID. The 'delete' strategy removes threads entirely. The
        'keep_latest' strategy prunes old checkpoints but keeps threads and
        their latest state.
      operationId: prune_threads_threads_prune_post
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ThreadPruneRequest'
        required: true
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ThreadPruneResponse'
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
components:
  schemas:
    ThreadPruneRequest:
      properties:
        thread_ids:
          type: array
          items:
            type: string
            format: uuid
          title: Thread IDs
          description: List of thread IDs to prune.
        strategy:
          type: string
          enum:
            - delete
            - keep_latest
          title: Strategy
          description: >-
            The prune strategy. 'delete' removes threads entirely. 'keep_latest'
            prunes old checkpoints but keeps threads and their latest state.
          default: delete
        sync_checkpoint_delete:
          type: boolean
          title: Sync Checkpoint Delete
          description: >-
            If true, delete checkpoints before responding instead of deferring
            them to background deletion. Use when thread data must be gone on
            return.
          default: false
      required:
        - thread_ids
      type: object
      title: ThreadPruneRequest
      description: Payload for pruning threads.
    ThreadPruneResponse:
      properties:
        pruned_count:
          type: integer
          title: Pruned Count
          description: Number of threads successfully pruned.
      required:
        - pruned_count
      type: object
      title: ThreadPruneResponse
      description: Response from pruning threads.
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

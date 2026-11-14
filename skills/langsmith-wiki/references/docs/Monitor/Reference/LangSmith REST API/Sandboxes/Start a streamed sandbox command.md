# Start a streamed sandbox command

> Execute a command inside a sandbox and stream stdout/stderr as Server-Sent Events with base64 payloads. Requires a sandbox on the v2 runtime. Passing a command_id reuses a running command instead of starting a second one. The response ends with an ack_required event when the sandbox's output buffer needs an ack; continue from the reported offsets with the resume endpoint.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json post /api/v2/sandboxes/{sandbox_id}/execute/stream/start
openapi: 3.1.0
info:
  title: LangSmith
  description: >+
    The LangSmith API is used to programmatically create and manage LangSmith
    resources.


    ## Host

    https://api.smith.langchain.com


    ## Authentication

    To authenticate with the LangSmith API, set the `X-Api-Key` header

    to a valid [LangSmith API
    key](https://docs.langchain.com/langsmith/create-account-api-key#create-an-api-key).

  version: 0.1.0
servers:
  - url: /
security: []
tags:
  - name: run
    x-group: Tracing
  - name: runs
    x-group: Tracing
  - name: sessions
    x-group: Tracing
  - name: tracer-sessions
    x-group: Tracing
  - name: threads
    x-group: Threads
  - name: datasets
    x-group: Datasets
  - name: examples
    x-group: Datasets
  - name: evaluators
    x-group: Evaluation
  - name: experiment-view-overrides
    x-group: Evaluation
  - name: experiments
    x-group: Evaluation
  - name: annotation-queues
    x-group: Feedback & Annotation
  - name: annotation_queues
    x-group: Feedback & Annotation
  - name: feedback
    x-group: Feedback & Annotation
  - name: feedback-configs
    x-group: Feedback & Annotation
  - name: alert_rules
    x-group: Monitoring
  - name: bulk-exports
    x-group: Monitoring
  - name: charts
    x-group: Monitoring
  - name: commits
    x-group: Prompts & Playground
  - name: directories
    x-group: Prompts & Playground
  - name: hub_environments
    x-group: Prompts & Playground
  - name: playground-settings
    x-group: Prompts & Playground
  - name: prompt-webhooks
    x-group: Prompts & Playground
  - name: prompts
    x-group: Prompts & Playground
  - name: tag-transitions
    x-group: Prompts & Playground
  - name: comments
    x-group: Prompt Hub
  - name: likes
    x-group: Prompt Hub
  - name: optimization-jobs
    x-group: Prompt Hub
  - name: ownerships
    x-group: Prompt Hub
  - name: repos
    x-group: Prompt Hub
  - name: settings
    x-group: Prompt Hub
  - name: tags
    x-group: Prompt Hub
  - name: integrations
    x-group: Integrations & Tools
  - name: mcp
    x-group: Integrations & Tools
  - name: mcp_vendors
    x-group: Integrations & Tools
  - name: oauth
    x-group: Integrations & Tools
  - name: tools
    x-group: Integrations & Tools
  - name: gateway-policies
    x-group: LLM Gateway
  - name: sandboxes
    x-group: Sandboxes
  - name: issues
    x-group: Issues
  - name: issues-agent
    x-group: Issues
  - name: Organizations
    x-group: Administration
  - name: SCIM Tokens
    x-group: Administration
  - name: TTL Settings
    x-group: Administration
  - name: access_policies
    x-group: Administration
  - name: api-key
    x-group: Administration
  - name: audit-logs
    x-group: Administration
  - name: auth
    x-group: Administration
  - name: aws_marketplace
    x-group: Administration
  - name: data_planes
    x-group: Administration
  - name: me
    x-group: Administration
  - name: orgs
    x-group: Administration
  - name: service-accounts
    x-group: Administration
  - name: tenant
    x-group: Administration
  - name: ttl-settings
    x-group: Administration
  - name: usage-limits
    x-group: Administration
  - name: workspaces
    x-group: Administration
  - name: ace
    x-group: System
  - name: backfills
    x-group: System
  - name: features
    x-group: System
  - name: info
    x-group: System
  - name: model-price-map
    x-group: System
  - name: public
    x-group: System
  - name: agents
    x-hidden: true
  - name: fleet orgs
  - name: fleet secrets
  - name: fleet tenants
  - name: fleet threads
    x-hidden: true
  - name: fleet users
  - name: productfeedback
    x-hidden: true
  - name: teams
  - name: usage
paths:
  /api/v2/sandboxes/{sandbox_id}/execute/stream/start:
    post:
      tags:
        - sandboxes
      summary: Start a streamed sandbox command
      description: >-
        Execute a command inside a sandbox and stream stdout/stderr as
        Server-Sent Events with base64 payloads. Requires a sandbox on the v2
        runtime. Passing a command_id reuses a running command instead of
        starting a second one. The response ends with an ack_required event when
        the sandbox's output buffer needs an ack; continue from the reported
        offsets with the resume endpoint.
      parameters:
        - description: Sandbox ID or name
          name: sandbox_id
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/sandboxes.ExecStreamRequest'
      responses:
        '200':
          description: SSE event stream
          content:
            text/event-stream:
              schema:
                type: string
        '400':
          description: Bad Request
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/sandboxes.ErrorResponse'
        '403':
          description: Forbidden
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/sandboxes.ErrorResponse'
        '404':
          description: Not Found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/sandboxes.ErrorResponse'
        '409':
          description: Conflict
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/sandboxes.ErrorResponse'
        '500':
          description: Internal Server Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/sandboxes.ErrorResponse'
      security:
        - API Key: []
        - Tenant ID: []
        - Bearer Auth: []
components:
  schemas:
    sandboxes.ExecStreamRequest:
      type: object
      properties:
        command:
          description: >-
            Command accepts either a shell command string or an argv string
            array.
          type: array
          items:
            type: string
        command_id:
          description: |-
            CommandID makes the request idempotent: a known ID attaches to that
            running command instead of starting a second one.
          type: string
        cwd:
          description: >-
            Deprecated: use run_config.work_dir. Rejected when run_config is
            also set.
          type: string
          deprecated: true
        env:
          description: >-
            Deprecated: use run_config.env_vars. Rejected when run_config is
            also set.
          type: object
          additionalProperties:
            type: string
          deprecated: true
        idle_timeout_seconds:
          description: 0 = default, -1 = never idle-kill
          type: integer
        run_config:
          description: >-
            RunConfig overrides, for this command only, the user, working
            directory and env the sandbox's commands run with.
          allOf:
            - $ref: '#/components/schemas/sandboxapi.RunConfig'
        shell:
          type: string
        stdin:
          description: >-
            Stdin is the process's entire standard input, base64 on the wire. It
            is

            written once when the command is spawned and then closed, so the
            process

            reads EOF; there is no stdin streaming on this endpoint.
          type: string
          format: byte
        timeout_seconds:
          description: 0 = no timeout
          type: integer
        ttl_seconds:
          description: 0 = default, -1 = keep forever
          type: integer
    sandboxes.ErrorResponse:
      type: object
      properties:
        detail:
          type: object
          properties:
            error:
              type: string
            error_id:
              type: string
            message:
              type: string
    sandboxapi.RunConfig:
      type: object
      properties:
        env_vars:
          type: object
          additionalProperties:
            type: string
        user:
          type: string
        work_dir:
          type: string
  securitySchemes:
    API Key:
      type: apiKey
      in: header
      name: X-API-Key
    Tenant ID:
      type: apiKey
      in: header
      name: X-Tenant-Id
    Bearer Auth:
      type: http
      description: >-
        Bearer tokens are used to authenticate from the UI. Must also specify
        x-tenant-id or x-organization-id (for org scoped apis).
      scheme: bearer

````

# Query thread traces

> Retrieve all traces belonging to a specific thread within a project.

Self-hosted deployments require LangSmith `v0.16` or later.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json get /api/v2/threads/{thread_id}/traces
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
  /api/v2/threads/{thread_id}/traces:
    get:
      tags:
        - threads
      summary: Query thread traces
      description: |-
        Retrieve all traces belonging to a specific thread within a project.

        Self-hosted deployments require LangSmith `v0.16` or later.
      parameters:
        - description: Thread ID
          name: thread_id
          in: path
          required: true
          schema:
            type: string
        - description: >-
            `cursor` is the opaque string from a previous response's
            `next_cursor`. Omit on the first request; pass the returned cursor
            to fetch the next page.
          name: cursor
          in: query
          schema:
            type: string
            title: Cursor
        - description: >-
            `filter` narrows which traces are returned for this thread, using a
            LangSmith filter expression evaluated against each root trace run.

            For example: eq(status, "success") or has(tags, "production").

            See
            https://docs.langchain.com/langsmith/trace-query-syntax#filter-query-language
            for syntax.
          name: filter
          in: query
          schema:
            type: string
            title: Filter
        - example: 20
          description: >-
            `page_size` is the maximum number of traces to return in this
            response. Defaults to 20 when omitted; must be between 1 and 100
            inclusive when set.
          name: page_size
          in: query
          schema:
            type: integer
            maximum: 100
            minimum: 1
            title: Page Size
            default: 20
        - description: '`project_id` is the tracing project UUID (required).'
          name: project_id
          in: query
          required: true
          schema:
            format: uuid
            type: string
            title: Project Id
        - example:
            - NAME
            - START_TIME
          description: >-
            `selects` lists which properties to include on each returned trace
            (repeatable query parameter). Accepts any value of the
            `ThreadTraceSelectField` enum. Properties not listed are omitted
            from each trace object; `trace_id` is always returned.
          name: selects
          in: query
          style: form
          explode: true
          schema:
            type: array
            items:
              enum:
                - THREAD_ID
                - TRACE_ID
                - OP
                - PROMPT_TOKENS
                - COMPLETION_TOKENS
                - TOTAL_TOKENS
                - START_TIME
                - END_TIME
                - LATENCY
                - FIRST_TOKEN_TIME
                - INPUTS_PREVIEW
                - OUTPUTS_PREVIEW
                - INPUTS
                - OUTPUTS
                - ERROR
                - PROMPT_COST
                - COMPLETION_COST
                - TOTAL_COST
                - PROMPT_TOKEN_DETAILS
                - COMPLETION_TOKEN_DETAILS
                - PROMPT_COST_DETAILS
                - COMPLETION_COST_DETAILS
                - NAME
                - ERROR_PREVIEW
                - TURN_NUMBER
              type: string
            title: Selects
        - description: >-
            `trace_filter` narrows traces by applying a LangSmith filter
            expression to each trace's root run.
          name: trace_filter
          in: query
          schema:
            type: string
            title: Trace Filter
        - description: >-
            `tree_filter` narrows traces to those containing at least one run
            that matches the LangSmith filter expression.
          name: tree_filter
          in: query
          schema:
            type: string
            title: Tree Filter
      responses:
        '200':
          description: items and pagination
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/threads.QueryThreadTracesResponseBody'
        '400':
          description: bad request (missing or invalid query parameters)
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/shared.ProblemDetails'
        '403':
          description: forbidden (insufficient permission)
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/shared.ProblemDetails'
        '404':
          description: session not found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/shared.ProblemDetails'
        '422':
          description: unprocessable entity (e.g. invalid project UUID)
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/shared.ProblemDetails'
        '501':
          description: V2 filter syntax or TURN_NUMBER is unavailable for this deployment
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/shared.ProblemDetails'
      security:
        - API Key: []
          Tenant ID: []
        - Bearer Auth: []
          Tenant ID: []
components:
  schemas:
    threads.QueryThreadTracesResponseBody:
      type: object
      properties:
        items:
          description: >-
            `items` is the page of root traces in this thread. Which properties
            are populated on each trace depends on the `selects` query
            parameter.
          type: array
          items:
            $ref: '#/components/schemas/threads.ThreadTraceListItem'
        next_cursor:
          description: >-
            `next_cursor` is the opaque cursor to pass as `cursor` on the next
            request. Null on the final page.
          type: string
          example: eyJydW5zX2N1cnNvciI6Imx0KGN1cnNvciwiLi4uIikifQ==
    shared.ProblemDetails:
      description: RFC 7807 problem details returned on V2 API errors.
      type: object
      properties:
        detail:
          type: string
        details:
          description: >-
            Details is a LangSmith extension carrying structured fields for
            ErrorClass.
          allOf:
            - $ref: '#/components/schemas/shared.ParseErrorDetails'
        error_class:
          description: |-
            ErrorClass is a LangSmith extension sub-categorizing a status code.
            Additional values require expanding this enum and adding a oneOf
            discriminator on Details to keep the class↔details contract typed.
          type: string
          enum:
            - PARSE_FAILURE
        instance:
          type: string
        remedy:
          description: Remedy is a LangSmith extension for user-recoverable errors.
          type: string
        status:
          type: integer
        title:
          type: string
        type:
          type: string
    threads.ThreadTraceListItem:
      type: object
      properties:
        completion_cost:
          description: >-
            `completion_cost` is the estimated USD cost for the completion.
            Omitted unless included in `selects`.
          type: number
        completion_cost_details:
          description: >-
            `completion_cost_details` is the USD cost breakdown for
            completion-side categories; per-category values are under `raw`.
            Omitted unless included in `selects`.
          allOf:
            - $ref: '#/components/schemas/query.RunCompletionCostDetails'
        completion_token_details:
          description: >-
            `completion_token_details` is the completion-side token breakdown by
            category; per-category counts are under `raw`. Omitted unless
            included in `selects`.
          allOf:
            - $ref: '#/components/schemas/query.RunCompletionTokenDetails'
        completion_tokens:
          description: >-
            `completion_tokens` is the completion-side token count. Omitted
            unless included in `selects`.
          type: integer
        end_time:
          description: >-
            `end_time` is when the root run ended (RFC3339 date-time). JSON null
            if the run is still in progress. Omitted unless included in
            `selects`.
          type: string
          format: date-time
          example: '2025-01-15T12:00:01.500Z'
        error:
          description: >-
            `error` is the full root run error message when the run failed.
            Omitted unless included in `selects`.
          type: string
          example: context deadline exceeded
        error_preview:
          description: >-
            `error_preview` is a short error summary when the run failed.
            Omitted unless included in `selects`.
          type: string
        first_token_time:
          description: >-
            `first_token_time` is when the first output token was produced
            (RFC3339 date-time), for streamed runs when that metadata exists.
            Omitted unless included in `selects`.
          type: string
          format: date-time
          example: '2024-01-15T10:30:00.312Z'
        inputs:
          description: >-
            `inputs` is the full root run input payload. Omitted unless included
            in `selects`.
          type: object
        inputs_preview:
          description: >-
            `inputs_preview` is a truncated text preview of inputs. Omitted
            unless included in `selects`.
          type: string
        latency:
          description: >-
            `latency` is wall-clock duration from start to end in seconds.
            Omitted unless included in `selects`.
          type: number
        name:
          description: >-
            `name` is a human-readable label for the root run (for example the
            model name, function name, or step name chosen when the run was
            traced). Omitted unless included in `selects`.
          type: string
        op:
          description: >-
            `op` is a numeric code identifying the root run's `run_type` (for
            example LLM vs. tool vs. chain). Encoded as a number for
            compatibility with legacy clients; prefer the string `run_type` on
            `RunResponse` when available. Omitted unless included in `selects`.
          type: number
        outputs:
          description: >-
            `outputs` is the full root run output payload. Omitted unless
            included in `selects`.
          type: object
        outputs_preview:
          description: >-
            `outputs_preview` is a truncated text preview of outputs. Omitted
            unless included in `selects`.
          type: string
        prompt_cost:
          description: >-
            `prompt_cost` is the estimated USD cost for the prompt. Omitted
            unless included in `selects`.
          type: number
        prompt_cost_details:
          description: >-
            `prompt_cost_details` is the USD cost breakdown for prompt-side
            categories; per-category values are under `raw`. Omitted unless
            included in `selects`.
          allOf:
            - $ref: '#/components/schemas/query.RunPromptCostDetails'
        prompt_token_details:
          description: >-
            `prompt_token_details` is the prompt-side token breakdown by
            category; per-category counts are under nested `raw`. Omitted unless
            included in `selects`.
          allOf:
            - $ref: '#/components/schemas/query.RunPromptTokenDetails'
        prompt_tokens:
          description: >-
            `prompt_tokens` is the prompt-side token count. Omitted unless
            included in `selects`.
          type: integer
        start_time:
          description: >-
            `start_time` is when the trace started (RFC3339 date-time). Omitted
            unless included in `selects`.
          type: string
          format: date-time
          example: '2025-01-15T12:00:00.000Z'
        thread_id:
          description: >-
            `thread_id` is the conversation thread UUID that contains this
            trace. Matches the `thread_id` path parameter of the request.
            Omitted unless included in `selects`.
          type: string
          format: uuid
          example: d4e5f6a7-b8c9-4d5e-1f2a-3b4c5d6e7f8a
        total_cost:
          description: >-
            `total_cost` is the estimated total USD cost for the root run.
            Omitted unless included in `selects`.
          type: number
        total_tokens:
          description: >-
            `total_tokens` is the total token count (prompt plus completion).
            Omitted unless included in `selects`.
          type: integer
        trace_id:
          description: >-
            `trace_id` is the UUID of this trace (the root run). Returned when
            `TRACE_ID` is in `selects`,

            or when `selects` is omitted entirely (sole fallback field).
          type: string
          format: uuid
          example: 018e4c7e-a9fb-7ef0-a5b6-6ea3a82e9327
        turn_number:
          description: >-
            `turn_number` is the 1-based position in the whole thread, ordered
            by start_time then trace_id ascending, before filtering or
            pagination. Updates and deletions can change this position. Omitted
            unless TURN_NUMBER is included in `selects`.
          type: integer
          minimum: 1
          example: 1
    shared.ParseErrorDetails:
      description: Structured fields describing an adapter parse failure.
      type: object
      required:
        - adapter
        - item_type
      properties:
        adapter:
          type: string
        item_type:
          type: string
        run_id:
          type: string
    query.RunCompletionCostDetails:
      type: object
      properties:
        raw:
          description: '`raw` maps each category name to its estimated USD cost.'
          type: object
          additionalProperties:
            type: number
            format: double
    query.RunCompletionTokenDetails:
      type: object
      properties:
        raw:
          description: '`raw` maps each category name to its completion-token count.'
          type: object
          additionalProperties:
            type: integer
            format: int64
    query.RunPromptCostDetails:
      type: object
      properties:
        raw:
          description: '`raw` maps each category name to its estimated USD cost.'
          type: object
          additionalProperties:
            type: number
            format: double
    query.RunPromptTokenDetails:
      type: object
      properties:
        raw:
          description: '`raw` maps each category name to its prompt-token count.'
          type: object
          additionalProperties:
            type: integer
            format: int64
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

# Query single thread stats

> Compute aggregate stats for a single thread (turn count, latency percentiles, token/cost sums, and detail breakdowns) within a project.

Self-hosted deployments require LangSmith `v0.16` or later.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json get /api/v2/threads/{thread_id}/stats
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
  /api/v2/threads/{thread_id}/stats:
    get:
      tags:
        - threads
      summary: Query single thread stats
      description: >-
        Compute aggregate stats for a single thread (turn count, latency
        percentiles, token/cost sums, and detail breakdowns) within a project.


        Self-hosted deployments require LangSmith `v0.16` or later.
      parameters:
        - description: Thread ID
          name: thread_id
          in: path
          required: true
          schema:
            type: string
        - description: >-
            `filter` narrows which of the thread's traces are aggregated, using
            a LangSmith filter expression. For example: lt(start_time,
            "2025-01-01T00:00:00Z") or eq(trace_id,
            "0190a1b2-c3d4-7ef0-a5b6-6ea3a82e9328").

            See
            https://docs.langchain.com/langsmith/trace-query-syntax#filter-query-language
            for syntax.
          name: filter
          in: query
          schema:
            type: string
            title: Filter
        - example:
            - TURNS
            - LATENCY_P50
          description: >-
            `selects` lists which aggregate stats to compute and return
            (repeatable query parameter). At least one value is required.
            Accepts any value of `SingleThreadStatsSelectField`.
          name: selects
          in: query
          required: true
          style: form
          explode: true
          schema:
            type: array
            items:
              enum:
                - TURNS
                - FIRST_START_TIME
                - LAST_START_TIME
                - LAST_END_TIME
                - LATENCY_P50
                - LATENCY_P99
                - PROMPT_TOKENS
                - PROMPT_COST
                - COMPLETION_TOKENS
                - COMPLETION_COST
                - TOTAL_TOKENS
                - TOTAL_COST
                - PROMPT_TOKEN_DETAILS
                - COMPLETION_TOKEN_DETAILS
                - PROMPT_COST_DETAILS
                - COMPLETION_COST_DETAILS
                - FEEDBACK_STATS
              type: string
            title: Selects
        - description: '`session_id` is the tracing project (session) UUID (required).'
          name: session_id
          in: query
          required: true
          schema:
            type: string
            format: uuid
            title: Session Id
      responses:
        '200':
          description: aggregate stats for the thread
          content:
            application/json:
              schema:
                $ref: >-
                  #/components/schemas/threads.QuerySingleThreadStatsResponseBody
        '400':
          description: bad request (missing or invalid query parameters)
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/shared.ProblemDetails'
        '401':
          description: missing or invalid authentication
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
        '500':
          description: internal server error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/shared.ProblemDetails'
        '503':
          description: service unavailable
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/shared.ProblemDetails'
        '504':
          description: gateway timeout or deadline exceeded
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
    threads.QuerySingleThreadStatsResponseBody:
      type: object
      properties:
        completion_cost:
          description: >-
            `completion_cost` is the sum of per-trace completion costs across
            the thread, in USD. Populated when `COMPLETION_COST` is selected.
          type: number
        completion_cost_details:
          description: >-
            `completion_cost_details` is the per-sub-category sum of completion
            cost details across the thread. Populated when
            `COMPLETION_COST_DETAILS` is selected.
          allOf:
            - $ref: '#/components/schemas/query.RunCompletionCostDetails'
        completion_token_details:
          description: >-
            `completion_token_details` is the per-sub-category sum of completion
            token details across the thread. Populated when
            `COMPLETION_TOKEN_DETAILS` is selected.
          allOf:
            - $ref: '#/components/schemas/query.RunCompletionTokenDetails'
        completion_tokens:
          description: >-
            `completion_tokens` is the sum of per-trace completion token counts
            across the thread. Populated when `COMPLETION_TOKENS` is selected.
          type: integer
        feedback_stats:
          description: >-
            `feedback_stats` aggregates run-level feedback across the thread's
            traces, keyed by feedback key. Populated when `FEEDBACK_STATS` is
            selected.
          allOf:
            - $ref: '#/components/schemas/query.RunFeedbackStats'
        first_start_time:
          description: >-
            `first_start_time` is the earliest trace start time in the thread
            (RFC3339). Populated when `FIRST_START_TIME` is selected.
          type: string
          format: date-time
        last_end_time:
          description: >-
            `last_end_time` is the latest trace end time in the thread
            (RFC3339). Populated when `LAST_END_TIME` is selected.
          type: string
          format: date-time
        last_start_time:
          description: >-
            `last_start_time` is the latest trace start time in the thread
            (RFC3339). Populated when `LAST_START_TIME` is selected.
          type: string
          format: date-time
        latency_p50_seconds:
          description: >-
            `latency_p50_seconds` is the approximate p50 of trace latency across
            the thread, in seconds. Populated when `LATENCY_P50` is selected.
          type: number
        latency_p99_seconds:
          description: >-
            `latency_p99_seconds` is the approximate p99 of trace latency across
            the thread, in seconds. Populated when `LATENCY_P99` is selected.
          type: number
        prompt_cost:
          description: >-
            `prompt_cost` is the sum of per-trace prompt costs across the
            thread, in USD. Populated when `PROMPT_COST` is selected.
          type: number
        prompt_cost_details:
          description: >-
            `prompt_cost_details` is the per-sub-category sum of prompt cost
            details across the thread. Populated when `PROMPT_COST_DETAILS` is
            selected.
          allOf:
            - $ref: '#/components/schemas/query.RunPromptCostDetails'
        prompt_token_details:
          description: >-
            `prompt_token_details` is the per-sub-category sum of prompt token
            details across the thread. Populated when `PROMPT_TOKEN_DETAILS` is
            selected.
          allOf:
            - $ref: '#/components/schemas/query.RunPromptTokenDetails'
        prompt_tokens:
          description: >-
            `prompt_tokens` is the sum of per-trace prompt token counts across
            the thread. Populated when `PROMPT_TOKENS` is selected.
          type: integer
        total_cost:
          description: >-
            `total_cost` is the sum of per-trace total costs across the thread,
            in USD. Populated when `TOTAL_COST` is selected.
          type: number
        total_tokens:
          description: >-
            `total_tokens` is the sum of per-trace total token counts across the
            thread. Populated when `TOTAL_TOKENS` is selected.
          type: integer
        turns:
          description: >-
            `turns` is the number of distinct traces (turns) in the thread.
            Populated when `TURNS` is selected.
          type: integer
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
    query.RunFeedbackStats:
      type: object
      additionalProperties:
        $ref: '#/components/schemas/query.RunFeedbackStat'
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
    query.RunFeedbackStat:
      type: object
      properties:
        avg:
          description: >-
            `avg` is the arithmetic mean of numeric feedback scores for this key
            on the run, or `null` when no numeric score has been recorded (for
            example purely categorical feedback).
          type: number
          example: 0.87
        comments:
          description: >-
            `comments` is a sample of human-readable comments attached to
            feedback points for this key, in no particular order. May be empty;
            is not exhaustive when many comments exist.
          type: array
          items:
            type: string
          example:
            - good answer
            - needs citation
        contains_thread_feedback:
          description: >-
            `contains_thread_feedback` is true when at least one feedback point
            for this key was submitted at the thread level (rather than at an
            individual run). Always false on responses that already describe a
            single run in isolation.
          type: boolean
          example: false
        errors:
          description: >-
            `errors` is the number of feedback points recorded as errors rather
            than successful scores (for example an automated evaluator that
            raised an exception). Defaults to 0 when no errors occurred.
          type: integer
          default: 0
          example: 0
        max:
          description: >-
            `max` is the largest numeric feedback score recorded for this key on
            the run, or `null` when no numeric score has been recorded.
          type: number
          example: 0.95
        min:
          description: >-
            `min` is the smallest numeric feedback score recorded for this key
            on the run, or `null` when no numeric score has been recorded.
          type: number
          example: 0.8
        'n':
          description: >-
            `n` is the number of feedback points recorded for this key on the
            run. For numeric feedback this is the sample size behind `avg`,
            `min`, `max`, and `stdev`; for categorical feedback it is the sum of
            the `values` counts.
          type: integer
          example: 42
        sources:
          description: >-
            `sources` is a sample of feedback sources for this key. Each entry
            is either a plain string identifier (for example `"api"`, `"app"`,
            `"model"`) or a JSON object describing a synthetic source (for
            example `{"type": "__ls_composite_feedback"}` for a computed
            aggregate). Clients must tolerate both shapes.
          type: array
          items: {}
        stdev:
          description: >-
            `stdev` is the sample standard deviation of numeric feedback scores
            for this key on the run, or `null` when it cannot be computed (for
            example fewer than two numeric scores, or purely categorical
            feedback).
          type: number
          example: 0.05
        values:
          description: >-
            `values` is the distribution of categorical feedback labels for this
            key, mapping each label to its occurrence count. Empty (`{}`) for
            purely numeric feedback.
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

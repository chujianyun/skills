# Query thread stats

> GET with body payload — no resources created. Returns aggregate statistics for threads in a tracing project.
The response includes the thread counts, run counts, latency percentiles, rates, token totals, and cost totals requested in `select`.

Self-hosted deployments require LangSmith `v0.17` or later.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json post /api/v2/threads/stats
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
  /api/v2/threads/stats:
    post:
      tags:
        - threads
      summary: Query thread stats
      description: >-
        GET with body payload — no resources created. Returns aggregate
        statistics for threads in a tracing project.

        The response includes the thread counts, run counts, latency
        percentiles, rates, token totals, and cost totals requested in `select`.


        Self-hosted deployments require LangSmith `v0.17` or later.
      parameters: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/threads.QueryThreadStatsRequestBody'
      responses:
        '200':
          description: aggregate thread statistics
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/threads.QueryThreadStatsResponseBody'
        '400':
          description: bad request (malformed JSON or invalid parameters)
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
          description: SmithDB query is unavailable for this deployment
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
    threads.QueryThreadStatsRequestBody:
      type: object
      required:
        - project_id
        - select
      properties:
        filter:
          description: >-
            `filter` is a deprecated, unscoped LangSmith filter expression
            evaluated

            against trace root runs. Kept for compatibility with deployments
            that

            serve this endpoint via the legacy ClickHouse backend (no SmithDB
            query

            service configured); prefer `trace_filter`, `tree_filter`, or

            `thread_filter` otherwise, since those require SmithDB.
          type: string
          example: eq(status, "error")
        max_start_time:
          description: >-
            `max_start_time` is the exclusive upper bound on thread activity
            (RFC3339 date-time). Defaults to now (UTC) when omitted.
          type: string
          format: date-time
        min_start_time:
          description: >-
            `min_start_time` is the inclusive lower bound on thread activity
            (RFC3339 date-time). Defaults to 1 day before now (UTC) when
            omitted.
          type: string
          format: date-time
        project_id:
          description: '`project_id` is the tracing project UUID.'
          type: string
          format: uuid
          example: 0190a1b2-c3d4-7ef0-a5b6-6ea3a82e9328
        select:
          description: >-
            `select` lists the aggregate statistics to compute and return. At
            least one value is required.
          type: array
          minItems: 1
          items:
            $ref: '#/components/schemas/threads.ThreadStatsSelectField'
          example:
            - THREAD_COUNT
            - TRACE_COUNT
            - TOTAL_TOKENS
            - TOTAL_COST
        thread_filter:
          description: >-
            `thread_filter` narrows eligible threads using a LangSmith filter
            expression evaluated against the complete thread summary.
          type: string
          example: gte(turn_count, 3)
        trace_filter:
          description: >-
            `trace_filter` narrows eligible threads to those containing a trace
            whose root run matches this LangSmith filter expression.
          type: string
          example: eq(status, "error")
        tree_filter:
          description: >-
            `tree_filter` narrows eligible threads to those containing a
            matching run anywhere in a trace tree.
          type: string
          example: has(tags, "production")
    threads.QueryThreadStatsResponseBody:
      type: object
      properties:
        completion_cost:
          description: >-
            `completion_cost` is the completion cost across matching traces in
            USD.
          type: number
        completion_cost_details:
          description: >-
            `completion_cost_details` contains completion-cost totals by
            category.
          type: object
          additionalProperties:
            type: number
            format: double
        completion_token_details:
          description: >-
            `completion_token_details` contains completion-token totals by
            category.
          type: object
          additionalProperties:
            type: integer
            format: int64
        completion_tokens:
          description: >-
            `completion_tokens` is the sum of completion tokens across matching
            traces.
          type: integer
        error_rate:
          description: >-
            `error_rate` is the fraction of matching traces that contain an
            error.
          type: number
        first_token_p50_seconds:
          description: >-
            `first_token_p50_seconds` is the approximate median time to first
            token in seconds. Populated when `FIRST_TOKEN_P50` is selected.
          type: number
        first_token_p99_seconds:
          description: >-
            `first_token_p99_seconds` is the approximate p99 time to first token
            in seconds. Populated when `FIRST_TOKEN_P99` is selected.
          type: number
        latency_p50_seconds:
          description: >-
            `latency_p50_seconds` is the approximate median trace latency in
            seconds. Populated when `LATENCY_P50` is selected.
          type: number
        latency_p99_seconds:
          description: >-
            `latency_p99_seconds` is the approximate p99 trace latency in
            seconds. Populated when `LATENCY_P99` is selected.
          type: number
        median_tokens:
          description: >-
            `median_tokens` is the approximate median of total tokens across
            matching traces. Populated when `MEDIAN_TOKENS` is selected.
          type: integer
        prompt_cost:
          description: '`prompt_cost` is the prompt cost across matching traces in USD.'
          type: number
        prompt_cost_details:
          description: '`prompt_cost_details` contains prompt-cost totals by category.'
          type: object
          additionalProperties:
            type: number
            format: double
        prompt_token_details:
          description: '`prompt_token_details` contains prompt-token totals by category.'
          type: object
          additionalProperties:
            type: integer
            format: int64
        prompt_tokens:
          description: '`prompt_tokens` is the sum of prompt tokens across matching traces.'
          type: integer
        streaming_rate:
          description: >-
            `streaming_rate` is the fraction of completed matching traces that
            streamed tokens.
          type: number
        thread_count:
          description: >-
            `thread_count` is the number of distinct threads matching the query.
            Populated when `THREAD_COUNT` is selected.
          type: integer
        thread_feedback_stats:
          description: >-
            `thread_feedback_stats` contains aggregate thread-level feedback
            statistics keyed by feedback key. Populated when
            `THREAD_FEEDBACK_STATS` is selected.
          allOf:
            - $ref: '#/components/schemas/query.RunFeedbackStats'
        total_cost:
          description: '`total_cost` is the total cost across matching traces in USD.'
          type: number
        total_tokens:
          description: '`total_tokens` is the sum of all tokens across matching traces.'
          type: integer
        trace_count:
          description: >-
            `trace_count` is the number of traces in the matching threads.
            Populated when `TRACE_COUNT` is selected.
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
    threads.ThreadStatsSelectField:
      type: string
      enum:
        - THREAD_COUNT
        - TRACE_COUNT
        - TOTAL_TOKENS
        - TOTAL_COST
        - ERROR_RATE
        - STREAMING_RATE
        - LATENCY_P50
        - LATENCY_P99
        - MEDIAN_TOKENS
        - FIRST_TOKEN_P50
        - FIRST_TOKEN_P99
        - PROMPT_TOKENS
        - COMPLETION_TOKENS
        - PROMPT_COST
        - COMPLETION_COST
        - PROMPT_TOKEN_DETAILS
        - COMPLETION_TOKEN_DETAILS
        - PROMPT_COST_DETAILS
        - COMPLETION_COST_DETAILS
        - THREAD_FEEDBACK_STATS
      x-enum-varnames:
        - ThreadStatsSelectThreadCount
        - ThreadStatsSelectTraceCount
        - ThreadStatsSelectTotalTokens
        - ThreadStatsSelectTotalCost
        - ThreadStatsSelectErrorRate
        - ThreadStatsSelectStreamingRate
        - ThreadStatsSelectLatencyP50
        - ThreadStatsSelectLatencyP99
        - ThreadStatsSelectMedianTokens
        - ThreadStatsSelectFirstTokenP50
        - ThreadStatsSelectFirstTokenP99
        - ThreadStatsSelectPromptTokens
        - ThreadStatsSelectCompletionTokens
        - ThreadStatsSelectPromptCost
        - ThreadStatsSelectCompletionCost
        - ThreadStatsSelectPromptTokenDetails
        - ThreadStatsSelectCompletionTokenDetails
        - ThreadStatsSelectPromptCostDetails
        - ThreadStatsSelectCompletionCostDetails
        - ThreadStatsSelectThreadFeedbackStats
    query.RunFeedbackStats:
      type: object
      additionalProperties:
        $ref: '#/components/schemas/query.RunFeedbackStat'
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

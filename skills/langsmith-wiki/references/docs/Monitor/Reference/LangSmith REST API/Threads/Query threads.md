# Query threads

> GET with body payload — no resources created. Returns the threads in a tracing project matching the query passed as the request payload.
Results are filtered by the given time range and optional filters, with cursor-based pagination.

When `ai_search` is set, `Accept: text/event-stream` is required; requests without it return 406. AI search is unavailable on deployments that route queries to the v1 backend and returns 501 there.

Self-hosted deployments require LangSmith `v0.16` or later.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json post /api/v2/threads/query
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
  /api/v2/threads/query:
    post:
      tags:
        - threads
      summary: Query threads
      description: >-
        GET with body payload — no resources created. Returns the threads in a
        tracing project matching the query passed as the request payload.

        Results are filtered by the given time range and optional filters, with
        cursor-based pagination.


        When `ai_search` is set, `Accept: text/event-stream` is required;
        requests without it return 406. AI search is unavailable on deployments
        that route queries to the v1 backend and returns 501 there.


        Self-hosted deployments require LangSmith `v0.16` or later.
      parameters:
        - description: >-
            application/json, or text/event-stream (required when ai_search is
            set)
          name: Accept
          in: header
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/threads.QueryThreadsRequestBody'
      responses:
        '200':
          description: items and pagination
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/threads.QueryThreadsResponseBody'
            text/event-stream:
              schema:
                $ref: '#/components/schemas/shared.SSEEvent'
        '400':
          description: bad request (malformed JSON or invalid parameters)
          content:
            application/problem+json:
              schema:
                $ref: '#/components/schemas/shared.ProblemDetails'
        '403':
          description: forbidden (insufficient permission)
          content:
            application/problem+json:
              schema:
                $ref: '#/components/schemas/shared.ProblemDetails'
        '404':
          description: session not found
          content:
            application/problem+json:
              schema:
                $ref: '#/components/schemas/shared.ProblemDetails'
        '422':
          description: unprocessable entity (e.g. invalid project UUID)
          content:
            application/problem+json:
              schema:
                $ref: '#/components/schemas/shared.ProblemDetails'
        '501':
          description: >-
            V2 filter syntax, thread_filters, or ai_search are unavailable for
            this deployment; use legacy function-style filters without
            thread_filters or set SMITHDB_QUERY_ENABLED=true
          content:
            application/problem+json:
              schema:
                $ref: '#/components/schemas/shared.ProblemDetails'
      security:
        - API Key: []
          Tenant ID: []
        - Bearer Auth: []
          Tenant ID: []
components:
  schemas:
    threads.QueryThreadsRequestBody:
      type: object
      properties:
        ai_search:
          description: >-
            `ai_search` is a plain-language criterion evaluated against the
            messages from the agent trajectory scoped to the thread.

            AND-ed with the ordinary filters. Requires semantic filtering
            enabled for the deployment.

            Must contain nonempty text of at most 2000 UTF-8 bytes.
          type: string
          maxLength: 2000
          minLength: 1
          example: A conversation about a refund request
        cursor:
          description: >-
            `cursor` is the opaque string from a previous response's
            `next_cursor`. Omit on the first request; pass the returned cursor
            to fetch the next page.
          type: string
        filter:
          description: >-
            `filter` narrows which threads are returned, using a LangSmith
            filter expression evaluated against each thread's root run.

            For example: has(tags, "production") or eq(status, "error").

            See
            https://docs.langchain.com/langsmith/trace-query-syntax#filter-query-language
            for syntax.
          type: string
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
        page_size:
          description: >-
            `page_size` is the maximum number of threads to return in this
            response. Defaults to 20 when omitted; must be between 1 and 100
            inclusive when set. The response may contain fewer threads than
            `page_size` even when `next_cursor` is non-null.
          type: integer
          default: 20
          maximum: 100
          minimum: 1
          example: 20
        project_id:
          description: '`project_id` is the tracing project UUID.'
          type: string
          format: uuid
          example: 0190a1b2-c3d4-7ef0-a5b6-6ea3a82e9328
        thread_filter:
          description: >-
            `thread_filter` narrows results using a LangSmith filter expression
            evaluated against each complete thread summary.

            Self-hosted deployments require LangSmith v0.17 or later;
            unsupported deployments return 501.

            See
            https://docs.langchain.com/langsmith/trace-query-syntax#filter-query-language
            for syntax.
          type: string
          example: gte(turn_count, 3)
        trace_filter:
          description: >-
            `trace_filter` narrows results to threads containing at least one
            trace whose root run matches this LangSmith filter expression.

            Trace-level aggregate fields are evaluated using the complete trace
            summary.

            Self-hosted deployments require LangSmith v0.17 or later;
            unsupported deployments return 501.

            See
            https://docs.langchain.com/langsmith/trace-query-syntax#filter-query-language
            for syntax.
          type: string
          example: eq(status, "error")
        tree_filter:
          description: >-
            `tree_filter` narrows results to threads containing at least one
            trace with a matching run anywhere in its run tree.

            Self-hosted deployments require LangSmith v0.17 or later;
            unsupported deployments return 501.

            See
            https://docs.langchain.com/langsmith/trace-query-syntax#filter-query-language
            for syntax.
          type: string
          example: has(tags, "production")
    threads.QueryThreadsResponseBody:
      type: object
      properties:
        items:
          description: >-
            `items` is the page of thread summaries, sorted by the thread's most
            recent activity.
          type: array
          items:
            $ref: '#/components/schemas/threads.ThreadListItem'
        next_cursor:
          description: >-
            `next_cursor` is the opaque cursor to pass as `cursor` on the next
            request. Null on the final page.
          type: string
          example: eyJydW5zX2N1cnNvciI6Imx0KGN1cnNvciwiLi4uIikifQ==
    shared.SSEEvent:
      type: object
      description: One parsed event from a v2 query Server-Sent Events response.
      required:
        - event
        - data
      properties:
        event:
          type: string
          description: The event name.
          enum:
            - data
            - end
            - error
        data:
          type: string
          description: >-
            For data events, a JSON-encoded array of RFC 6902 patch operations;
            for end events, an empty string; for error events, a JSON-encoded
            ProblemDetails object.
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
    threads.ThreadListItem:
      type: object
      properties:
        count:
          description: >-
            `count` is how many root traces (conversation turns) fall in this
            thread for the query time range.
          type: integer
          example: 3
        feedback_stats:
          description: >-
            `feedback_stats` is the aggregated feedback across traces in the
            thread, keyed by feedback key; shape matches `feedback_stats` on a
            single run.
          allOf:
            - $ref: '#/components/schemas/query.RunFeedbackStats'
        first_inputs:
          description: >-
            `first_inputs` is a truncated preview of inputs from the earliest
            trace in the thread for the query window.
          type: string
        first_trace_id:
          description: >-
            `first_trace_id` is the root trace UUID for the chronologically
            first trace in the query time window.
          type: string
          format: uuid
          example: 018e4c7e-a9fb-7ef0-a5b6-6ea3a82e9327
        last_error:
          description: >-
            `last_error` is a short error summary from the most recent failing
            trace in the thread. Absent when there is no error in the window.
          type: string
        last_outputs:
          description: >-
            `last_outputs` is a truncated preview of outputs from the latest
            trace in the thread for the query window.
          type: string
        last_trace_id:
          description: >-
            `last_trace_id` is the root trace UUID for the chronologically last
            trace in the query time window.
          type: string
          format: uuid
          example: 0190a1b2-c3d4-7ef0-a5b6-6ea3a82e9328
        latency_p50:
          description: >-
            `latency_p50` is the approximate median end-to-end latency of traces
            in the thread, in seconds.
          type: number
          example: 0.15
        latency_p99:
          description: >-
            `latency_p99` is the approximate 99th percentile end-to-end latency
            of traces in the thread, in seconds.
          type: number
          example: 0.42
        max_start_time:
          description: >-
            `max_start_time` is the latest trace start time in the thread
            (RFC3339 date-time).
          type: string
          format: date-time
          example: '2025-01-15T12:05:00.000Z'
        min_start_time:
          description: >-
            `min_start_time` is the earliest trace start time in the thread
            (RFC3339 date-time).
          type: string
          format: date-time
          example: '2025-01-15T12:00:00.000Z'
        num_errored_turns:
          description: >-
            `num_errored_turns` is the count of root traces in the thread
            (within the query window) whose status was an error.
          type: integer
          example: 1
        query_metadata:
          description: >-
            `query_metadata` describes why this thread matched the query,
            including `sem_filter_score` when a semantic filter is used.
            Returned automatically, or null when unavailable.
          anyOf:
            - type: object
            - type: 'null'
        start_time:
          description: >-
            `start_time` is a reference start time for this row (RFC3339
            date-time), such as for sorting.
          type: string
          format: date-time
          example: '2025-01-15T12:00:00.000Z'
        thread_id:
          description: >-
            `thread_id` identifies this conversation thread within the project
            from the request body `project_id`.
          type: string
          format: uuid
          example: 018e4c7e-a9fb-7ef0-a5b6-6ea3a82e9327
        total_cost:
          description: '`total_cost` is the sum of estimated USD cost across those traces.'
          type: number
          example: 0.045
        total_cost_details:
          description: >-
            `total_cost_details` sums per-category estimated USD cost across
            traces in the thread. Keys mirror `total_token_details`.


            Example: `{"cache_read": 0.012, "reasoning": 0.008}`.
          type: object
          additionalProperties:
            type: number
            format: double
        total_token_details:
          description: >-
            `total_token_details` sums per-category token counts across traces
            in the thread. Keys are model-specific category names (for example
            `cache_read`, `cache_write`, `reasoning`, `audio`).


            Example: `{"cache_read": 400, "reasoning": 120}`.
          type: object
          additionalProperties:
            type: integer
            format: int64
        total_tokens:
          description: '`total_tokens` is the sum of token usage across those traces.'
          type: integer
          example: 450
        trace_id:
          description: >-
            `trace_id` is a representative root trace UUID when the summary
            includes one, for example for deep links.
          type: string
          format: uuid
          example: 018e4c7e-a9fb-7ef0-a5b6-6ea3a82e9328
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
    query.RunFeedbackStats:
      type: object
      additionalProperties:
        $ref: '#/components/schemas/query.RunFeedbackStat'
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

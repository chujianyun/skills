# Query runs

> Returns a paginated list of runs for the given projects within min/max start_time. Supports filters, cursor pagination, and `selects` to select fields to return.

When `ai_search` is set, `Accept: text/event-stream` is required; requests without it return 406. AI search is unavailable on deployments that route queries to the v1 backend and returns 501 there.

Self-hosted deployments require LangSmith `v0.16` or later.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json post /api/v2/runs/query
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
  /api/v2/runs/query:
    post:
      tags:
        - runs
      summary: Query runs
      description: >-
        Returns a paginated list of runs for the given projects within min/max
        start_time. Supports filters, cursor pagination, and `selects` to select
        fields to return.


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
        - description: application/json (required for JSON body)
          name: Content-Type
          in: header
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/query.QueryRunsRequestBody'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/query.QueryRunsResponseBody'
            text/event-stream:
              schema:
                $ref: '#/components/schemas/shared.SSEEvent'
        '400':
          description: bad request (malformed JSON or invalid parameters)
          content:
            application/problem+json:
              schema:
                $ref: '#/components/schemas/shared.ProblemDetails'
        '401':
          description: missing or invalid authentication
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
        '406':
          description: 'not acceptable (ai_search requires Accept: text/event-stream)'
          content:
            application/problem+json:
              schema:
                $ref: '#/components/schemas/shared.ProblemDetails'
        '422':
          description: unprocessable entity (e.g. invalid UUID)
          content:
            application/problem+json:
              schema:
                $ref: '#/components/schemas/shared.ProblemDetails'
        '500':
          description: internal server error
          content:
            application/problem+json:
              schema:
                $ref: '#/components/schemas/shared.ProblemDetails'
        '501':
          description: >-
            The requested filter syntax or ai_search is unavailable for this
            deployment
          content:
            application/problem+json:
              schema:
                $ref: '#/components/schemas/shared.ProblemDetails'
        '503':
          description: service unavailable
          content:
            application/problem+json:
              schema:
                $ref: '#/components/schemas/shared.ProblemDetails'
        '504':
          description: gateway timeout or deadline exceeded
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
    query.QueryRunsRequestBody:
      type: object
      properties:
        ai_search:
          description: >-
            `ai_search` is a plain-language criterion evaluated against the
            messages from the agent trajectory scoped to the run.

            AND-ed with the ordinary filters. Requires semantic filtering
            enabled for the deployment.

            Must contain nonempty text of at most 2000 UTF-8 bytes. Not
            supported on public dataset queries.
          type: string
          maxLength: 2000
          minLength: 1
          example: The customer was charged twice
        cursor:
          description: >-
            `cursor` is the opaque string from a previous response's
            `next_cursor`. Treat it as opaque and pass it back unmodified.
          type: string
          example: >-
            eyJ2IjoxLCJhIjoicnVucy5xdWVyeSIsImsiOiJwYXNzIiwiYiI6InNkYiIsInQiOiJsdChjdXJzb3IsICcyMDI1LTEyLTEyIDE5OjAzOjI4LjQ4MTI1NTAxOWIxM2YyJykifQ
        filter:
          description: >-
            `filter` narrows results to runs matching this LangSmith filter
            expression, evaluated against each individual run.

            For example: and(eq(run_type, "llm"), gt(latency, 5)) or eq(status,
            "error").

            See
            https://docs.langchain.com/langsmith/trace-query-syntax#filter-query-language
            for syntax.
          type: string
          example: and(eq(run_type, "llm"), gt(latency, 5))
        has_error:
          description: >-
            `has_error` filters to runs that errored (true) or completed without
            error (false).
          type: boolean
          example: false
        ids:
          description: '`ids` optionally limits the request to these run UUIDs.'
          type: array
          items:
            type: string
            format: uuid
          example:
            - 018e4c7e-a9fb-7ef0-a5b6-6ea3a82e9327
            - f47ac10b-58cc-4372-a567-0e02b2c3d479
        include_subtree_usage:
          description: >-
            `include_subtree_usage` enriches selected token and cost fields on
            root and intermediate runs with subtree totals, and selected
            `first_token_time` with the earliest observed subtree timestamp.

            Descendants contribute regardless of this request's filters or time
            bounds. Runs without observed descendants retain their original
            values. Defaults to false.
          type: boolean
          default: false
        is_root:
          description: >-
            `is_root` returns only root runs (true) or only non-root runs
            (false).
          type: boolean
          example: true
        max_feedback_modified_at:
          description: >-
            `max_feedback_modified_at` is the exclusive upper bound (RFC3339) on
            feedback `modified_at`, applied to the feedback conditions in
            `filter`, `trace_filter`, or `tree_filter` (for example
            eq(feedback_key, "correctness")).

            Requires at least one feedback condition. Runs must still fall
            within the `start_time` window.
          type: string
          format: date-time
          example: '2024-12-31T23:59:59Z'
        max_start_time:
          description: >-
            `max_start_time` is the upper bound for run `start_time` (RFC3339).
            Defaults to now.
          type: string
          format: date-time
          example: '2024-12-31T23:59:59Z'
        min_feedback_modified_at:
          description: >-
            `min_feedback_modified_at` is the inclusive lower bound (RFC3339) on
            feedback `modified_at`, applied to the feedback conditions in
            `filter`, `trace_filter`, or `tree_filter` (for example
            eq(feedback_key, "correctness")).

            Requires at least one feedback condition. Runs must still fall
            within the `start_time` window.
          type: string
          format: date-time
          example: '2024-01-01T00:00:00Z'
        min_start_time:
          description: >-
            `min_start_time` is the lower bound for run `start_time` (RFC3339).
            Defaults to 1 day ago.
          type: string
          format: date-time
          example: '2024-01-01T00:00:00Z'
        page_size:
          description: >-
            `page_size` is the maximum number of runs to return in this
            response. Defaults to 100 when omitted; must be between 1 and 1000
            inclusive when set.
          type: integer
          default: 100
          maximum: 1000
          minimum: 1
          example: 100
        project_ids:
          description: >-
            `project_ids` lists tracing project UUIDs to query.

            Required unless `reference_dataset_id` is set. Mutually exclusive
            with `reference_dataset_id` — set exactly one of them.
          type: array
          items:
            type: string
            format: uuid
          example:
            - 018e4c7e-a9fb-7ef0-a5b6-6ea3a82e9327
            - 0190a1b2-c3d4-7ef0-a5b6-6ea3a82e9328
        reference_dataset_id:
          description: >-
            `reference_dataset_id` resolves session IDs server-side from the
            dataset.

            Required unless `project_ids` is set. Mutually exclusive with
            `project_ids` — set exactly one of them.

            When provided and `min_start_time` is omitted, the server derives it
            from the earliest session creation date.
          type: string
          format: uuid
          example: 018e4c7e-a9fb-7ef0-a5b6-6ea3a82e9327
        reference_examples:
          description: >-
            `reference_examples` optionally limits to runs linked to these
            dataset example UUIDs.
          type: array
          items:
            type: string
            format: uuid
          example:
            - b2c3d4e5-f6a7-4b5c-9d0e-1f2a3b4c5d6e
            - c3d4e5f6-a7b8-4c5d-0e1f-2a3b4c5d6e7f
        run_type:
          description: >-
            `run_type`, when set, restricts results to runs whose `run_type`
            equals this value.
          allOf:
            - $ref: '#/components/schemas/query.RunType'
          example: LLM
        selects:
          description: >-
            `selects` lists which properties to include on each returned run. If
            omitted, only `id` is returned. Properties not listed are omitted
            from each run object.
          type: array
          items:
            $ref: '#/components/schemas/query.RunSelectField'
          example:
            - ID
            - NAME
            - PROJECT_ID
            - START_TIME
            - RUN_TYPE
            - STATUS
        trace_filter:
          description: >-
            `trace_filter` narrows results to runs whose root trace matches this
            LangSmith filter expression.

            Use this to filter by properties of the trace's root run — for
            example eq(status, "success") to include only traces that completed
            without error.

            See
            https://docs.langchain.com/langsmith/trace-query-syntax#filter-query-language
            for syntax.
          type: string
          example: eq(status, "success")
        trace_id:
          description: >-
            `trace_id` optionally limits results to runs belonging to this trace
            UUID.
          type: string
          format: uuid
          example: f47ac10b-58cc-4372-a567-0e02b2c3d479
        tree_filter:
          description: >-
            `tree_filter` narrows results to runs that belong to a trace
            containing at least one run matching this LangSmith filter
            expression anywhere in the run tree (not just the root).

            Use this to find runs inside traces that involved a specific tool,
            tag, or model — for example has(tags, "production") or eq(name,
            "my_tool").

            See
            https://docs.langchain.com/langsmith/trace-query-syntax#filter-query-language
            for syntax.
          type: string
          example: has(tags, "production")
    query.QueryRunsResponseBody:
      type: object
      properties:
        items:
          description: '`items` is the page of runs, sorted by `start_time` descending.'
          type: array
          items:
            $ref: '#/components/schemas/query.RunResponse'
        next_cursor:
          description: >-
            `next_cursor` is the opaque cursor to pass as `cursor` on the next
            request. Null on the final page.
          type: string
          example: >-
            eyJ2IjoxLCJhIjoicnVucy5xdWVyeSIsImsiOiJwYXNzIiwiYiI6InNkYiIsInQiOiJsdChjdXJzb3IsICcyMDI1LTEyLTEyIDE5OjAzOjI4LjQ4MTI1NTAxOWIxM2YyJykifQ
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
    query.RunType:
      type: string
      enum:
        - TOOL
        - CHAIN
        - LLM
        - RETRIEVER
        - EMBEDDING
        - PROMPT
        - PARSER
      x-enum-varnames:
        - RunTypeTool
        - RunTypeChain
        - RunTypeLLM
        - RunTypeRetriever
        - RunTypeEmbedding
        - RunTypePrompt
        - RunTypeParser
    query.RunSelectField:
      type: string
      enum:
        - ID
        - NAME
        - RUN_TYPE
        - STATUS
        - START_TIME
        - END_TIME
        - LATENCY_SECONDS
        - FIRST_TOKEN_TIME
        - ERROR
        - ERROR_PREVIEW
        - EXTRA
        - METADATA
        - EVENTS
        - INPUTS
        - INPUTS_PREVIEW
        - OUTPUTS
        - OUTPUTS_PREVIEW
        - MANIFEST
        - PARENT_RUN_IDS
        - PROJECT_ID
        - TRACE_ID
        - THREAD_ID
        - DOTTED_ORDER
        - IS_ROOT
        - REFERENCE_EXAMPLE_ID
        - REFERENCE_DATASET_ID
        - TOTAL_TOKENS
        - PROMPT_TOKENS
        - COMPLETION_TOKENS
        - TOTAL_COST
        - PROMPT_COST
        - COMPLETION_COST
        - PROMPT_TOKEN_DETAILS
        - COMPLETION_TOKEN_DETAILS
        - PROMPT_COST_DETAILS
        - COMPLETION_COST_DETAILS
        - PRICE_MODEL_ID
        - TAGS
        - APP_PATH
        - ATTACHMENTS
        - THREAD_EVALUATION_TIME
        - IS_IN_DATASET
        - LAST_QUEUED_AT
        - SHARE_URL
        - FEEDBACK_STATS
        - LS_USER_ID
      x-enum-varnames:
        - RunSelectID
        - RunSelectName
        - RunSelectRunType
        - RunSelectStatus
        - RunSelectStartTime
        - RunSelectEndTime
        - RunSelectLatencySeconds
        - RunSelectFirstTokenTime
        - RunSelectError
        - RunSelectErrorPreview
        - RunSelectExtra
        - RunSelectMetadata
        - RunSelectEvents
        - RunSelectInputs
        - RunSelectInputsPreview
        - RunSelectOutputs
        - RunSelectOutputsPreview
        - RunSelectManifest
        - RunSelectParentRunIDs
        - RunSelectProjectID
        - RunSelectTraceID
        - RunSelectThreadID
        - RunSelectDottedOrder
        - RunSelectIsRoot
        - RunSelectReferenceExampleID
        - RunSelectReferenceDatasetID
        - RunSelectTotalTokens
        - RunSelectPromptTokens
        - RunSelectCompletionTokens
        - RunSelectTotalCost
        - RunSelectPromptCost
        - RunSelectCompletionCost
        - RunSelectPromptTokenDetails
        - RunSelectCompletionTokenDetails
        - RunSelectPromptCostDetails
        - RunSelectCompletionCostDetails
        - RunSelectPriceModelID
        - RunSelectTags
        - RunSelectAppPath
        - RunSelectAttachments
        - RunSelectThreadEvaluationTime
        - RunSelectIsInDataset
        - RunSelectLastQueuedAt
        - RunSelectShareURL
        - RunSelectFeedbackStats
        - RunSelectLsUserID
    query.RunResponse:
      type: object
      properties:
        app_path:
          description: >-
            `app_path` identifies the application code location that produced
            this run, if recorded.
          type: string
          example: /app/chains/chat.py:invoke
        attachments:
          description: >-
            `attachments` maps each attachment file name to a pre-signed HTTPS
            download URL.
          allOf:
            - $ref: '#/components/schemas/query.RunAttachmentURLs'
          example:
            '{"output.png"': '"https://storage.example.com/bucket/key?X-Amz-Signature=abc"}'
        completion_cost:
          description: '`completion_cost` is estimated USD cost for the completion.'
          type: number
          example: 0.0003
        completion_cost_details:
          description: >-
            `completion_cost_details` is the per-category USD breakdown of
            `completion_cost`. Categories mirror `completion_token_details`.
            Returned only when the `COMPLETION_COST_DETAILS` field is requested.
          allOf:
            - $ref: '#/components/schemas/query.RunCompletionCostDetails'
        completion_token_details:
          description: >-
            `completion_token_details` is the per-category breakdown of
            `completion_tokens`. Category names are model-specific (for example
            `reasoning`, `audio`). Returned only when the
            `COMPLETION_TOKEN_DETAILS` field is requested.
          allOf:
            - $ref: '#/components/schemas/query.RunCompletionTokenDetails'
        completion_tokens:
          description: '`completion_tokens` is the completion-side token count.'
          type: integer
          example: 150
        dotted_order:
          description: '`dotted_order` is the hierarchical ordering key for trace trees.'
          type: string
          example: 20240115T103000000000Z018e4c7ea9fb7ef0a5b66ea3a82e9327.
        end_time:
          description: >-
            `end_time` is when the run ended (RFC3339 date-time). JSON null if
            the run has not finished yet.
          type: string
          format: date-time
          example: '2024-01-15T10:30:01.500Z'
        error:
          description: '`error` is the error message when `status` indicates failure.'
          type: string
          example: context deadline exceeded
        error_preview:
          description: '`error_preview` is a truncated plain-text error snippet.'
          type: string
        events:
          description: >-
            `events` is the ordered list of run events (for example streaming
            tokens).
          type: array
          items:
            $ref: '#/components/schemas/query.RunEvent'
        extra:
          description: '`extra` is additional runtime JSON attached to the run.'
          type: object
        feedback_stats:
          description: '`feedback_stats` aggregates feedback scores keyed by feedback key.'
          allOf:
            - $ref: '#/components/schemas/query.RunFeedbackStats'
        first_token_time:
          description: >-
            `first_token_time` is when the first output token was produced
            (RFC3339 date-time), when recorded for streamed runs.
          type: string
          format: date-time
          example: '2024-01-15T10:30:00.312Z'
        id:
          description: '`id` is this run''s UUID.'
          type: string
          format: uuid
          example: 018e4c7e-a9fb-7ef0-a5b6-6ea3a82e9327
        inputs:
          description: '`inputs` is the run input payload (arbitrary JSON object).'
          type: object
        inputs_preview:
          description: '`inputs_preview` is a truncated plain-text preview of inputs.'
          type: string
        is_in_dataset:
          description: >-
            `is_in_dataset` is true when this run is linked to a dataset
            example.
          type: boolean
          example: true
        is_root:
          description: >-
            `is_root` is true when this run has no parent (it is the trace
            root).
          type: boolean
          example: true
        last_queued_at:
          description: >-
            `last_queued_at` is the most recent time this run was added to an
            annotation queue.
          type: string
          format: date-time
          example: '2024-01-15T10:31:00Z'
        latency_seconds:
          description: >-
            `latency_seconds` is wall-clock duration from start to end in
            seconds.
          type: number
          example: 1.523
        ls_user_id:
          description: >-
            `ls_user_id` identifies the LangSmith user whose credential traced
            the run. It is absent for runs traced with a service-account API
            key, which has no associated user.
          type: string
          format: uuid
          example: f6a7b8c9-d0e1-4f2a-3b4c-5d6e7f8a9b0c
        manifest:
          description: >-
            `manifest` is the serialized configuration of the traced component
            (for example the model parameters, prompt template, or pipeline
            definition), when recorded.
          type: object
        metadata:
          description: '`metadata` is arbitrary user-defined JSON metadata.'
          type: object
        name:
          description: >-
            `name` is a human-readable label for the run (for example the model
            name, function name, or step name chosen when the run was traced).
          type: string
          example: ChatOpenAI
        outputs:
          description: '`outputs` is the run output payload (arbitrary JSON object).'
          type: object
        outputs_preview:
          description: '`outputs_preview` is a truncated plain-text preview of outputs.'
          type: string
        parent_run_ids:
          description: >-
            `parent_run_ids` lists ancestor run UUIDs from the trace root down
            to the direct parent.
          type: array
          items:
            type: string
            format: uuid
          example:
            - 018e4c7e-a9fb-7ef0-a5b6-6ea3a82e9327
            - a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d
        price_model_id:
          description: >-
            `price_model_id` identifies the pricing model UUID used for cost
            estimates, when recorded.
          type: string
          format: uuid
          example: e5f6a7b8-c9d0-4e1f-2a3b-4c5d6e7f8a9b
        project_id:
          description: '`project_id` is the tracing project UUID this run was logged to.'
          type: string
          format: uuid
          example: 018e4c7e-a9fb-7ef0-a5b6-6ea3a82e9327
        prompt_cost:
          description: '`prompt_cost` is estimated USD cost for the prompt.'
          type: number
          example: 0.0002
        prompt_cost_details:
          description: >-
            `prompt_cost_details` is the per-category USD breakdown of
            `prompt_cost`. Categories mirror `prompt_token_details`. Returned
            only when the `PROMPT_COST_DETAILS` field is requested.
          allOf:
            - $ref: '#/components/schemas/query.RunPromptCostDetails'
        prompt_token_details:
          description: >-
            `prompt_token_details` is the per-category breakdown of
            `prompt_tokens`. Category names are model-specific (for example
            `cache_read`, `cache_write`). Returned only when the
            `PROMPT_TOKEN_DETAILS` field is requested.
          allOf:
            - $ref: '#/components/schemas/query.RunPromptTokenDetails'
        prompt_tokens:
          description: '`prompt_tokens` is the prompt-side token count.'
          type: integer
          example: 200
        query_metadata:
          description: >-
            `query_metadata` describes this query result, including
            `sem_filter_score` when a semantic filter is used. Returned
            automatically by run queries, or null when unavailable.
          anyOf:
            - type: object
            - type: 'null'
        reference_dataset_id:
          description: >-
            `reference_dataset_id` is the dataset UUID for the reference
            example, if any.
          type: string
          format: uuid
          example: c3d4e5f6-a7b8-4c5d-0e1f-2a3b4c5d6e7f
        reference_example_id:
          description: >-
            `reference_example_id` is the dataset example UUID this run was
            compared against, if any.
          type: string
          format: uuid
          example: b2c3d4e5-f6a7-4b5c-9d0e-1f2a3b4c5d6e
        run_type:
          description: >-
            `run_type` identifies what kind of operation this run represents
            (for example an LLM call, a tool invocation, or a chain step). See
            the `RunType` enum for allowed values.
          allOf:
            - $ref: '#/components/schemas/query.RunType'
          example: LLM
        share_url:
          description: >-
            `share_url` is the fully-qualified URL of this run's public view,
            rooted at the deployment's LangSmith app origin (for example
            `https://smith.langchain.com/public/4f7a1b2c-8d9e-4a0b-9c1d-2e3f4a5b6c7d/r`).
            It is returned only when `SHARE_URL` is included in `selects`, and
            only when the run has been explicitly shared; the URL remains stable
            until the run is unshared. Anyone with this URL can view the run
            anonymously, so treat it as a secret and do not log it.
          type: string
          example: >-
            https://smith.langchain.com/public/4f7a1b2c-8d9e-4a0b-9c1d-2e3f4a5b6c7d/r
        start_time:
          description: '`start_time` is when the run started (RFC3339 date-time).'
          type: string
          format: date-time
          example: '2024-01-15T10:30:00.000Z'
        status:
          description: '`status` is the completion status of the run.'
          allOf:
            - $ref: '#/components/schemas/query.RunStatus'
          example: SUCCESS
        tags:
          description: '`tags` lists user-defined tags on this run.'
          type: array
          items:
            type: string
          example:
            - production
            - gpt-4
        thread_evaluation_time:
          description: >-
            `thread_evaluation_time` is thread-level evaluation timing (RFC3339
            date-time), when recorded.
          type: string
          format: date-time
        thread_id:
          description: >-
            `thread_id` is the conversation thread UUID this run belongs to, if
            any.
          type: string
          format: uuid
          example: d4e5f6a7-b8c9-4d5e-1f2a-3b4c5d6e7f8a
        total_cost:
          description: '`total_cost` is total estimated USD cost (prompt plus completion).'
          type: number
          example: 0.000525
        total_tokens:
          description: '`total_tokens` is prompt plus completion tokens.'
          type: integer
          example: 350
        trace_id:
          description: '`trace_id` is the root trace UUID; for a root run it matches `id`.'
          type: string
          format: uuid
          example: 018e4c7e-a9fb-7ef0-a5b6-6ea3a82e9327
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
    query.RunAttachmentURLs:
      type: object
      additionalProperties:
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
    query.RunEvent:
      type: object
      properties:
        kwargs:
          description: >-
            `kwargs` is the event payload — an opaque JSON object whose shape
            depends on `name` and on the emitting SDK. For example LangChain
            emits `{"token": {...}}` for `new_token` events, tool-call start/end
            details for tool events, and arbitrary user-defined payloads for
            custom events. Clients should treat `kwargs` as untyped JSON: do not
            assume specific keys exist for a given `name`, and tolerate
            additional unknown keys appearing over time.
          type: object
        name:
          description: >-
            `name` is the event kind. Common values emitted by the
            LangChain/LangSmith tracer SDKs include `"start"`, `"end"`, and
            `"new_token"`, but applications may emit arbitrary strings for their
            own instrumentation.
          type: string
          example: new_token
        time:
          description: >-
            `time` is when the event occurred (RFC3339 date-time with
            millisecond precision).
          type: string
          format: date-time
          example: '2024-01-15T10:30:00.312Z'
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
    query.RunStatus:
      type: string
      enum:
        - SUCCESS
        - ERROR
        - PENDING
      x-enum-varnames:
        - RunStatusSuccess
        - RunStatusError
        - RunStatusPending
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

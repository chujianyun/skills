# Stats runs

> Get all runs by query in body payload.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json post /api/v1/runs/stats
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
  /api/v1/runs/stats:
    post:
      tags:
        - run
      summary: Stats runs
      description: Get all runs by query in body payload.
      operationId: stats_runs_api_v1_runs_stats_post
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/RunStatsQueryParams'
        required: true
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                anyOf:
                  - $ref: '#/components/schemas/RunStats'
                  - additionalProperties:
                      $ref: '#/components/schemas/RunStats'
                    type: object
                title: Response Stats Runs Api V1 Runs Stats Post
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
      security:
        - API Key: []
        - Tenant ID: []
        - Bearer Auth: []
components:
  schemas:
    RunStatsQueryParams:
      properties:
        id:
          anyOf:
            - items:
                type: string
                format: uuid
              type: array
            - type: 'null'
          title: Id
        trace:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Trace
          description: >-
            Filter runs by trace ID. When set, limit and cursor-based pagination
            are not applied — all runs in the trace are returned in a single
            response.
        parent_run:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Parent Run
        run_type:
          anyOf:
            - $ref: '#/components/schemas/RunTypeEnum'
            - type: 'null'
        session:
          items:
            type: string
            format: uuid
          type: array
          minItems: 1
          title: Session
        reference_example:
          anyOf:
            - items:
                type: string
                format: uuid
              type: array
            - type: 'null'
          title: Reference Example
        execution_order:
          anyOf:
            - type: integer
              maximum: 1
              minimum: 1
            - type: 'null'
          title: Execution Order
        start_time:
          anyOf:
            - type: string
              format: date-time
            - type: 'null'
          title: Start Time
        end_time:
          anyOf:
            - type: string
              format: date-time
            - type: 'null'
          title: End Time
        error:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Error
        query:
          anyOf:
            - type: string
            - type: 'null'
          title: Query
        filter:
          anyOf:
            - type: string
            - type: 'null'
          title: Filter
        trace_filter:
          anyOf:
            - type: string
            - type: 'null'
          title: Trace Filter
        tree_filter:
          anyOf:
            - type: string
            - type: 'null'
          title: Tree Filter
        is_root:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Is Root
        data_source_type:
          anyOf:
            - $ref: '#/components/schemas/RunsFilterDataSourceTypeEnum'
            - type: 'null'
        skip_pagination:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Skip Pagination
        search_filter:
          anyOf:
            - type: string
            - type: 'null'
          title: Search Filter
        use_experimental_search:
          type: boolean
          title: Use Experimental Search
          default: false
        group_by:
          anyOf:
            - $ref: '#/components/schemas/RunStatsGroupBy'
            - type: 'null'
        groups:
          anyOf:
            - items:
                anyOf:
                  - type: string
                  - type: 'null'
              type: array
            - type: 'null'
          title: Groups
        select:
          anyOf:
            - items:
                $ref: '#/components/schemas/RunStatsSelect'
              type: array
            - type: 'null'
          title: Select
        reference_dataset_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Reference Dataset Id
        include_details:
          type: boolean
          title: Include Details
          default: false
      type: object
      required:
        - session
      title: RunStatsQueryParams
      description: Query params for run stats.
    RunStats:
      properties:
        run_count:
          anyOf:
            - type: integer
            - type: 'null'
          title: Run Count
        latency_p50:
          anyOf:
            - type: number
            - type: 'null'
          title: Latency P50
        latency_p99:
          anyOf:
            - type: number
            - type: 'null'
          title: Latency P99
        first_token_p50:
          anyOf:
            - type: number
            - type: 'null'
          title: First Token P50
        first_token_p99:
          anyOf:
            - type: number
            - type: 'null'
          title: First Token P99
        total_tokens:
          anyOf:
            - type: integer
            - type: 'null'
          title: Total Tokens
        prompt_tokens:
          anyOf:
            - type: integer
            - type: 'null'
          title: Prompt Tokens
        completion_tokens:
          anyOf:
            - type: integer
            - type: 'null'
          title: Completion Tokens
        median_tokens:
          anyOf:
            - type: integer
            - type: 'null'
          title: Median Tokens
        completion_tokens_p50:
          anyOf:
            - type: integer
            - type: 'null'
          title: Completion Tokens P50
        prompt_tokens_p50:
          anyOf:
            - type: integer
            - type: 'null'
          title: Prompt Tokens P50
        tokens_p99:
          anyOf:
            - type: integer
            - type: 'null'
          title: Tokens P99
        completion_tokens_p99:
          anyOf:
            - type: integer
            - type: 'null'
          title: Completion Tokens P99
        prompt_tokens_p99:
          anyOf:
            - type: integer
            - type: 'null'
          title: Prompt Tokens P99
        last_run_start_time:
          anyOf:
            - type: string
              format: date-time
            - type: 'null'
          title: Last Run Start Time
        feedback_stats:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Feedback Stats
        run_facets:
          anyOf:
            - items:
                additionalProperties: true
                type: object
              type: array
            - type: 'null'
          title: Run Facets
        error_rate:
          anyOf:
            - type: number
            - type: 'null'
          title: Error Rate
        streaming_rate:
          anyOf:
            - type: number
            - type: 'null'
          title: Streaming Rate
        total_cost:
          anyOf:
            - type: number
            - type: 'null'
          title: Total Cost
        prompt_cost:
          anyOf:
            - type: number
            - type: 'null'
          title: Prompt Cost
        completion_cost:
          anyOf:
            - type: number
            - type: 'null'
          title: Completion Cost
        cost_p50:
          anyOf:
            - type: number
            - type: 'null'
          title: Cost P50
        cost_p99:
          anyOf:
            - type: number
            - type: 'null'
          title: Cost P99
        prompt_token_details:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Prompt Token Details
        completion_token_details:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Completion Token Details
        prompt_cost_details:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Prompt Cost Details
        completion_cost_details:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Completion Cost Details
      type: object
      title: RunStats
    HTTPValidationError:
      properties:
        detail:
          items:
            type: string
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    RunTypeEnum:
      type: string
      enum:
        - tool
        - chain
        - llm
        - retriever
        - embedding
        - prompt
        - parser
      title: RunTypeEnum
      description: Enum for run types.
    RunsFilterDataSourceTypeEnum:
      type: string
      enum:
        - current
        - historical
        - lite
        - root_lite
        - runs_feedbacks_rmt_wide
      title: RunsFilterDataSourceTypeEnum
      description: Enum for run data source types.
    RunStatsGroupBy:
      properties:
        attribute:
          type: string
          enum:
            - name
            - run_type
            - tag
            - metadata
          title: Attribute
        path:
          anyOf:
            - type: string
            - type: 'null'
          title: Path
        max_groups:
          type: integer
          title: Max Groups
          default: 5
      type: object
      required:
        - attribute
      title: RunStatsGroupBy
      description: Group by param for run stats.
    RunStatsSelect:
      type: string
      enum:
        - run_count
        - latency_p50
        - latency_p99
        - latency_avg
        - first_token_p50
        - first_token_p99
        - total_tokens
        - prompt_tokens
        - completion_tokens
        - median_tokens
        - completion_tokens_p50
        - prompt_tokens_p50
        - tokens_p99
        - completion_tokens_p99
        - prompt_tokens_p99
        - last_run_start_time
        - feedback_stats
        - thread_feedback_stats
        - run_facets
        - error_rate
        - streaming_rate
        - total_cost
        - prompt_cost
        - completion_cost
        - cost_p50
        - cost_p99
        - session_feedback_stats
        - all_run_stats
        - all_token_stats
        - group_count
        - prompt_token_details
        - completion_token_details
        - prompt_cost_details
        - completion_cost_details
      title: RunStatsSelect
      description: Metrics you can select from run stats endpoint.
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

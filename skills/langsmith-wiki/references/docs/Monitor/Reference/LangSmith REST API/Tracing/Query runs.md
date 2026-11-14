# Query runs



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json post /api/v1/runs/query
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
  /api/v1/runs/query:
    post:
      tags:
        - run
      summary: Query runs
      operationId: query_runs_api_v1_runs_query_post
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/BodyParamsForRunsQuerySchema'
        required: true
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ListRunsResponse'
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
      deprecated: true
      security:
        - API Key: []
        - Tenant ID: []
        - Bearer Auth: []
components:
  schemas:
    BodyParamsForRunsQuerySchema:
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
          anyOf:
            - items:
                type: string
                format: uuid
              type: array
            - type: 'null'
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
        cursor:
          anyOf:
            - type: string
            - type: 'null'
          title: Cursor
        limit:
          type: integer
          maximum: 100
          minimum: 1
          title: Limit
          description: >-
            Maximum number of runs to return. Not applied when trace is set —
            all runs in the trace are returned in a single response.
          default: 100
        select:
          items:
            $ref: '#/components/schemas/RunSelect'
          type: array
          title: Select
          default:
            - id
            - name
            - run_type
            - start_time
            - end_time
            - status
            - error
            - extra
            - events
            - inputs
            - outputs
            - parent_run_id
            - manifest_id
            - manifest_s3_id
            - manifest
            - session_id
            - serialized
            - reference_example_id
            - reference_dataset_id
            - total_tokens
            - prompt_tokens
            - prompt_token_details
            - completion_tokens
            - completion_token_details
            - total_cost
            - prompt_cost
            - prompt_cost_details
            - completion_cost
            - completion_cost_details
            - price_model_id
            - first_token_time
            - trace_id
            - dotted_order
            - last_queued_at
            - feedback_stats
            - parent_run_ids
            - tags
            - in_dataset
            - app_path
            - share_token
            - trace_tier
            - trace_first_received_at
            - ttl_seconds
            - trace_upgrade
            - thread_id
        order:
          $ref: '#/components/schemas/RunDateOrder'
          default: desc
        skip_prev_cursor:
          type: boolean
          title: Skip Prev Cursor
          default: false
      type: object
      title: BodyParamsForRunsQuerySchema
      description: Query params for runs query endpoint.
    ListRunsResponse:
      properties:
        runs:
          items:
            $ref: '#/components/schemas/RunSchema'
          type: array
          title: Runs
        cursors:
          additionalProperties:
            anyOf:
              - type: string
              - type: 'null'
          type: object
          title: Cursors
        search_cursors:
          anyOf:
            - additionalProperties:
                anyOf:
                  - {}
                  - type: 'null'
              type: object
            - type: 'null'
          title: Search Cursors
        parsed_query:
          anyOf:
            - type: string
            - type: 'null'
          title: Parsed Query
      type: object
      required:
        - runs
        - cursors
      title: ListRunsResponse
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
    RunSelect:
      type: string
      enum:
        - id
        - name
        - run_type
        - start_time
        - end_time
        - status
        - error
        - extra
        - events
        - inputs
        - inputs_preview
        - inputs_s3_urls
        - inputs_or_signed_url
        - outputs
        - outputs_preview
        - outputs_s3_urls
        - outputs_or_signed_url
        - s3_urls
        - error_or_signed_url
        - events_or_signed_url
        - extra_or_signed_url
        - serialized_or_signed_url
        - parent_run_id
        - manifest_id
        - manifest_s3_id
        - manifest
        - session_id
        - serialized
        - reference_example_id
        - reference_dataset_id
        - total_tokens
        - prompt_tokens
        - prompt_token_details
        - completion_tokens
        - completion_token_details
        - total_cost
        - prompt_cost
        - prompt_cost_details
        - completion_cost
        - completion_cost_details
        - price_model_id
        - first_token_time
        - trace_id
        - dotted_order
        - last_queued_at
        - feedback_stats
        - child_run_ids
        - parent_run_ids
        - tags
        - in_dataset
        - app_path
        - share_token
        - trace_tier
        - trace_first_received_at
        - ttl_seconds
        - trace_upgrade
        - thread_id
        - trace_min_max_start_time
        - messages
        - inserted_at
      title: RunSelect
      description: Enum for available run columns.
    RunDateOrder:
      type: string
      enum:
        - asc
        - desc
      title: RunDateOrder
      description: Enum for run start date order.
    RunSchema:
      properties:
        name:
          type: string
          title: Name
        inputs:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Inputs
        inputs_preview:
          anyOf:
            - type: string
            - type: 'null'
          title: Inputs Preview
        run_type:
          $ref: '#/components/schemas/RunTypeEnum'
        start_time:
          type: string
          format: date-time
          title: Start Time
        end_time:
          anyOf:
            - type: string
              format: date-time
            - type: 'null'
          title: End Time
        extra:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Extra
        error:
          anyOf:
            - type: string
            - type: 'null'
          title: Error
        execution_order:
          type: integer
          minimum: 1
          title: Execution Order
          default: 1
        serialized:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Serialized
        outputs:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Outputs
        outputs_preview:
          anyOf:
            - type: string
            - type: 'null'
          title: Outputs Preview
        parent_run_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Parent Run Id
        manifest_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Manifest Id
        manifest_s3_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Manifest S3 Id
        events:
          anyOf:
            - items:
                additionalProperties: true
                type: object
              type: array
            - type: 'null'
          title: Events
        tags:
          anyOf:
            - items:
                type: string
              type: array
            - type: 'null'
          title: Tags
        inputs_s3_urls:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Inputs S3 Urls
        outputs_s3_urls:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Outputs S3 Urls
        s3_urls:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: S3 Urls
        trace_id:
          type: string
          format: uuid
          title: Trace Id
        dotted_order:
          type: string
          title: Dotted Order
        trace_min_start_time:
          anyOf:
            - type: string
              format: date-time
            - type: 'null'
          title: Trace Min Start Time
        trace_max_start_time:
          anyOf:
            - type: string
              format: date-time
            - type: 'null'
          title: Trace Max Start Time
        id:
          type: string
          format: uuid
          title: Id
        status:
          type: string
          title: Status
        child_run_ids:
          anyOf:
            - items:
                type: string
                format: uuid
              type: array
            - type: 'null'
          title: Child Run Ids
        direct_child_run_ids:
          anyOf:
            - items:
                type: string
                format: uuid
              type: array
            - type: 'null'
          title: Direct Child Run Ids
        parent_run_ids:
          anyOf:
            - items:
                type: string
                format: uuid
              type: array
            - type: 'null'
          title: Parent Run Ids
        feedback_stats:
          anyOf:
            - additionalProperties:
                additionalProperties: true
                type: object
              type: object
            - type: 'null'
          title: Feedback Stats
        reference_example_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Reference Example Id
        total_tokens:
          type: integer
          title: Total Tokens
          default: 0
        prompt_tokens:
          type: integer
          title: Prompt Tokens
          default: 0
        completion_tokens:
          type: integer
          title: Completion Tokens
          default: 0
        prompt_token_details:
          anyOf:
            - additionalProperties:
                type: integer
              type: object
            - type: 'null'
          title: Prompt Token Details
        completion_token_details:
          anyOf:
            - additionalProperties:
                type: integer
              type: object
            - type: 'null'
          title: Completion Token Details
        total_cost:
          anyOf:
            - type: string
              pattern: ^(?!^[-+.]*$)[+-]?0*\d*\.?\d*$
            - type: 'null'
          title: Total Cost
        prompt_cost:
          anyOf:
            - type: string
              pattern: ^(?!^[-+.]*$)[+-]?0*\d*\.?\d*$
            - type: 'null'
          title: Prompt Cost
        completion_cost:
          anyOf:
            - type: string
              pattern: ^(?!^[-+.]*$)[+-]?0*\d*\.?\d*$
            - type: 'null'
          title: Completion Cost
        prompt_cost_details:
          anyOf:
            - additionalProperties:
                type: string
                pattern: ^(?!^[-+.]*$)[+-]?0*\d*\.?\d*$
              type: object
            - type: 'null'
          title: Prompt Cost Details
        completion_cost_details:
          anyOf:
            - additionalProperties:
                type: string
                pattern: ^(?!^[-+.]*$)[+-]?0*\d*\.?\d*$
              type: object
            - type: 'null'
          title: Completion Cost Details
        price_model_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Price Model Id
        first_token_time:
          anyOf:
            - type: string
              format: date-time
            - type: 'null'
          title: First Token Time
        messages:
          anyOf:
            - items:
                additionalProperties: true
                type: object
              type: array
            - type: 'null'
          title: Messages
        session_id:
          type: string
          format: uuid
          title: Session Id
        app_path:
          type: string
          title: App Path
        last_queued_at:
          anyOf:
            - type: string
              format: date-time
            - type: 'null'
          title: Last Queued At
        in_dataset:
          anyOf:
            - type: boolean
            - type: 'null'
          title: In Dataset
        share_token:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Share Token
        trace_tier:
          anyOf:
            - $ref: '#/components/schemas/TraceTier'
            - type: 'null'
        trace_first_received_at:
          anyOf:
            - type: string
              format: date-time
            - type: 'null'
          title: Trace First Received At
        ttl_seconds:
          anyOf:
            - type: integer
            - type: 'null'
          title: Ttl Seconds
        trace_upgrade:
          type: boolean
          title: Trace Upgrade
          default: false
        reference_dataset_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Reference Dataset Id
        thread_id:
          anyOf:
            - type: string
            - type: 'null'
          title: Thread Id
      type: object
      required:
        - name
        - run_type
        - trace_id
        - dotted_order
        - id
        - status
        - session_id
        - app_path
      title: RunSchema
      description: Run schema.
    TraceTier:
      enum:
        - longlived
        - shortlived
      title: TraceTier
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

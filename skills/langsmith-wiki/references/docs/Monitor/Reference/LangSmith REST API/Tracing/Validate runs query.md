# Validate runs query

> Validate runs query syntax, returns errors for broken queries.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json post /api/v1/runs/query/validate
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
  /api/v1/runs/query/validate:
    post:
      tags:
        - run
      summary: Validate runs query
      description: Validate runs query syntax, returns errors for broken queries.
      operationId: validate_runs_query_api_v1_runs_query_validate_post
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
                $ref: '#/components/schemas/RunsQueryValidationResponse'
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
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
    RunsQueryValidationResponse:
      properties:
        valid:
          type: boolean
          title: Valid
        errors:
          items:
            $ref: '#/components/schemas/RunsQueryValidationError'
          type: array
          title: Errors
      type: object
      required:
        - valid
      title: RunsQueryValidationResponse
      description: Response for POST /runs/query/validate.
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
    RunsQueryValidationError:
      properties:
        field:
          type: string
          title: Field
        message:
          type: string
          title: Message
      type: object
      required:
        - field
        - message
      title: RunsQueryValidationError
      description: A single validation error for the runs query validate endpoint.

````

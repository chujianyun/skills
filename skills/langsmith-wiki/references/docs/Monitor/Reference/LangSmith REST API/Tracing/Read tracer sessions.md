# Read tracer sessions

> List all projects.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json get /api/v1/sessions
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
  /api/v1/sessions:
    get:
      tags:
        - tracer-sessions
      summary: Read tracer sessions
      description: List all projects.
      operationId: read_tracer_sessions_api_v1_sessions_get
      parameters:
        - name: reference_free
          in: query
          required: false
          schema:
            anyOf:
              - type: boolean
              - type: 'null'
            title: Reference Free
        - name: reference_dataset
          in: query
          required: false
          schema:
            anyOf:
              - items:
                  type: string
                  format: uuid
                type: array
              - type: 'null'
            title: Reference Dataset
        - name: id
          in: query
          required: false
          schema:
            anyOf:
              - items:
                  type: string
                  format: uuid
                type: array
              - type: 'null'
            title: Id
        - name: name
          in: query
          required: false
          schema:
            anyOf:
              - type: string
              - type: 'null'
            title: Name
        - name: name_contains
          in: query
          required: false
          schema:
            anyOf:
              - type: string
              - type: 'null'
            title: Name Contains
        - name: dataset_version
          in: query
          required: false
          schema:
            anyOf:
              - type: string
              - type: 'null'
            title: Dataset Version
        - name: sort_by
          in: query
          required: false
          schema:
            $ref: '#/components/schemas/SessionSortableColumns'
            default: start_time
        - name: sort_by_desc
          in: query
          required: false
          schema:
            type: boolean
            default: true
            title: Sort By Desc
        - name: metadata
          in: query
          required: false
          schema:
            anyOf:
              - type: string
              - type: 'null'
            title: Metadata
        - name: sort_by_feedback_key
          in: query
          required: false
          schema:
            anyOf:
              - type: string
              - type: 'null'
            title: Sort By Feedback Key
        - name: sort_by_feedback_source
          in: query
          required: false
          schema:
            anyOf:
              - $ref: '#/components/schemas/FeedbackSourceParam'
              - type: 'null'
            title: Sort By Feedback Source
        - name: offset
          in: query
          required: false
          schema:
            type: integer
            minimum: 0
            title: Offset
            default: 0
        - name: limit
          in: query
          required: false
          schema:
            type: integer
            maximum: 100
            minimum: 1
            title: Limit
            default: 100
        - name: tag_value_id
          in: query
          required: false
          schema:
            anyOf:
              - items:
                  type: string
                  format: uuid
                type: array
              - type: 'null'
            title: Tag Value Id
        - name: facets
          in: query
          required: false
          schema:
            type: boolean
            default: false
            title: Facets
        - name: filter
          in: query
          required: false
          schema:
            anyOf:
              - type: string
              - type: 'null'
            title: Filter
        - name: include_stats
          in: query
          required: false
          schema:
            type: boolean
            default: false
            title: Include Stats
        - name: use_approx_stats
          in: query
          required: false
          schema:
            type: boolean
            title: Use Approx Stats
            default: false
        - name: stats_start_time
          in: query
          required: false
          schema:
            anyOf:
              - type: string
                format: date-time
              - type: 'null'
            title: Stats Start Time
        - name: stats_select
          in: query
          required: false
          schema:
            anyOf:
              - items:
                  type: string
                type: array
              - type: 'null'
            title: Stats Select
        - name: stats_filter
          in: query
          required: false
          schema:
            anyOf:
              - type: string
              - type: 'null'
            title: Stats Filter
        - name: accept
          in: header
          required: false
          schema:
            anyOf:
              - type: string
              - type: 'null'
            title: Accept
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/TracerSession'
                title: Response Read Tracer Sessions Api V1 Sessions Get
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
    SessionSortableColumns:
      type: string
      enum:
        - name
        - start_time
        - last_run_start_time
        - latency_p50
        - latency_p99
        - error_rate
        - feedback
      title: SessionSortableColumns
    FeedbackSourceParam:
      type: string
      enum:
        - session
        - run
      title: FeedbackSourceParam
    TracerSession:
      properties:
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
        name:
          type: string
          title: Name
        description:
          anyOf:
            - type: string
            - type: 'null'
          title: Description
        default_dataset_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Default Dataset Id
        reference_dataset_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Reference Dataset Id
        trace_tier:
          anyOf:
            - $ref: '#/components/schemas/TraceTier'
            - type: 'null'
        id:
          type: string
          format: uuid
          title: Id
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
        tenant_id:
          type: string
          format: uuid
          title: Tenant Id
        last_run_start_time:
          anyOf:
            - type: string
              format: date-time
            - type: 'null'
          title: Last Run Start Time
        last_run_start_time_live:
          anyOf:
            - type: string
              format: date-time
            - type: 'null'
          title: Last Run Start Time Live
        feedback_stats:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Feedback Stats
        session_feedback_stats:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Session Feedback Stats
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
        test_run_number:
          anyOf:
            - type: integer
            - type: 'null'
          title: Test Run Number
        experiment_progress:
          anyOf:
            - $ref: '#/components/schemas/ExperimentProgress'
            - type: 'null'
      type: object
      required:
        - id
        - tenant_id
      title: TracerSession
      description: TracerSession schema.
    HTTPValidationError:
      properties:
        detail:
          items:
            type: string
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    TraceTier:
      enum:
        - longlived
        - shortlived
      title: TraceTier
      type: string
    ExperimentProgress:
      properties:
        expected_run_count:
          type: integer
          title: Expected Run Count
        run_progress:
          type: number
          title: Run Progress
        evaluator_progress:
          additionalProperties:
            type: number
          type: object
          title: Evaluator Progress
      type: object
      required:
        - expected_run_count
        - run_progress
        - evaluator_progress
      title: ExperimentProgress
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

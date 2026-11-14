# Get tracing project prebuilt dashboard

> Get a prebuilt dashboard for a tracing project.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json post /api/v1/sessions/{session_id}/dashboard
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
  /api/v1/sessions/{session_id}/dashboard:
    post:
      tags:
        - tracer-sessions
      summary: Get tracing project prebuilt dashboard
      description: Get a prebuilt dashboard for a tracing project.
      operationId: >-
        get_tracing_project_prebuilt_dashboard_api_v1_sessions__session_id__dashboard_post
      parameters:
        - name: session_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
            title: Session Id
        - name: accept
          in: header
          required: false
          schema:
            anyOf:
              - type: string
              - type: 'null'
            title: Accept
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CustomChartsSectionRequest'
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CustomChartsSection'
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
    CustomChartsSectionRequest:
      properties:
        timezone:
          type: string
          title: Timezone
          default: UTC
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
        stride:
          $ref: '#/components/schemas/TimedeltaInput'
          default:
            days: 0
            hours: 0
            minutes: 15
        omit_data:
          type: boolean
          title: Omit Data
          default: false
        group_by:
          anyOf:
            - $ref: '#/components/schemas/RunStatsGroupBy'
            - type: 'null'
      type: object
      title: CustomChartsSectionRequest
    CustomChartsSection:
      properties:
        title:
          type: string
          title: Title
        description:
          anyOf:
            - type: string
            - type: 'null'
          title: Description
        index:
          anyOf:
            - type: integer
            - type: 'null'
          title: Index
        id:
          anyOf:
            - type: string
              format: uuid
            - type: string
          title: Id
        session_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Session Id
        charts:
          items:
            oneOf:
              - $ref: '#/components/schemas/SingleCustomChartResponse'
              - $ref: '#/components/schemas/CustomTextBlock'
            discriminator:
              propertyName: chart_type
              mapping:
                bar: '#/components/schemas/SingleCustomChartResponse'
                kpi: '#/components/schemas/SingleCustomChartResponse'
                line: '#/components/schemas/SingleCustomChartResponse'
                pie: '#/components/schemas/SingleCustomChartResponse'
                table: '#/components/schemas/SingleCustomChartResponse'
                text: '#/components/schemas/CustomTextBlock'
                top-k: '#/components/schemas/SingleCustomChartResponse'
          type: array
          title: Charts
        sub_sections:
          anyOf:
            - items:
                $ref: '#/components/schemas/SingleCustomChartSubSectionResponse'
              type: array
            - type: 'null'
          title: Sub Sections
        layout:
          anyOf:
            - $ref: '#/components/schemas/DashboardLayout-Output'
            - type: 'null'
      type: object
      required:
        - title
        - id
        - charts
      title: CustomChartsSection
    HTTPValidationError:
      properties:
        detail:
          items:
            type: string
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    TimedeltaInput:
      properties:
        days:
          type: integer
          title: Days
          default: 0
        hours:
          type: integer
          title: Hours
          default: 0
        minutes:
          type: integer
          title: Minutes
          default: 0
      type: object
      title: TimedeltaInput
      description: Timedelta input.
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
    SingleCustomChartResponse:
      $ref: '#/components/schemas/SingleCustomChartResponseSerialized'
    CustomTextBlock:
      properties:
        id:
          type: string
          format: uuid
          title: Id
        chart_type:
          type: string
          const: text
          title: Chart Type
        markdown:
          type: string
          title: Markdown
        index:
          type: integer
          title: Index
        metadata:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Metadata
      type: object
      required:
        - id
        - chart_type
        - markdown
        - index
      title: CustomTextBlock
    SingleCustomChartSubSectionResponse:
      properties:
        title:
          type: string
          title: Title
        description:
          anyOf:
            - type: string
            - type: 'null'
          title: Description
        index:
          type: integer
          title: Index
        id:
          anyOf:
            - type: string
              format: uuid
            - type: string
          title: Id
        charts:
          items:
            $ref: '#/components/schemas/SingleCustomChartResponse'
          type: array
          title: Charts
      type: object
      required:
        - title
        - index
        - id
        - charts
      title: SingleCustomChartSubSectionResponse
    DashboardLayout-Output:
      properties:
        version:
          type: integer
          const: 1
          title: Version
        breakpoints:
          $ref: '#/components/schemas/DashboardLayoutBreakpoints-Output'
      type: object
      required:
        - version
        - breakpoints
      title: DashboardLayout
    SingleCustomChartResponseSerialized:
      properties:
        data:
          items:
            $ref: '#/components/schemas/CustomChartsDataPoint'
          type: array
          title: Data
        id:
          anyOf:
            - type: string
              format: uuid
            - type: string
          title: Id
        title:
          type: string
          title: Title
        description:
          anyOf:
            - type: string
            - type: 'null'
          title: Description
        metadata:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Metadata
        index:
          type: integer
          title: Index
        chart_type:
          type: string
          enum:
            - line
            - bar
            - table
            - kpi
            - top-k
            - pie
          title: Chart Type
        series:
          items:
            $ref: '#/components/schemas/CustomChartSeries-Output'
          type: array
          title: Series
        common_filters:
          anyOf:
            - $ref: '#/components/schemas/CustomChartSeriesFilters'
            - type: 'null'
      type: object
      required:
        - data
        - id
        - title
        - index
        - chart_type
        - series
      title: SingleCustomChartResponseSerialized
    DashboardLayoutBreakpoints-Output:
      properties:
        sm:
          $ref: '#/components/schemas/DashboardBreakpointLayout-Output'
        md:
          $ref: '#/components/schemas/DashboardBreakpointLayout-Output'
      type: object
      required:
        - sm
        - md
      title: DashboardLayoutBreakpoints
    CustomChartsDataPoint:
      properties:
        series_id:
          type: string
          title: Series Id
        timestamp:
          type: string
          format: date-time
          title: Timestamp
        value:
          anyOf:
            - type: integer
            - type: number
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Value
        group:
          anyOf:
            - type: string
            - type: 'null'
          title: Group
      type: object
      required:
        - series_id
        - timestamp
        - value
      title: CustomChartsDataPoint
    CustomChartSeries-Output:
      properties:
        name:
          type: string
          title: Name
        metadata:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Metadata
        filters:
          anyOf:
            - $ref: '#/components/schemas/CustomChartSeriesFilters'
            - type: 'null'
        metric:
          anyOf:
            - $ref: '#/components/schemas/CustomChartMetric'
            - type: 'null'
        project_metric:
          anyOf:
            - $ref: '#/components/schemas/HostProjectChartMetric'
            - type: 'null'
        feedback_key:
          anyOf:
            - type: string
            - type: 'null'
          title: Feedback Key
        workspace_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Workspace Id
        metric_definition:
          anyOf:
            - $ref: '#/components/schemas/CustomChartFeedbackCountMetric'
            - $ref: '#/components/schemas/CustomChartMetricCount'
            - $ref: '#/components/schemas/CustomChartFeedbackScoreMetricScalar'
            - $ref: '#/components/schemas/CustomChartMetricScalar'
            - $ref: '#/components/schemas/CustomChartFeedbackScoreMetricPercentile'
            - $ref: '#/components/schemas/CustomChartMetricPercentile'
            - $ref: '#/components/schemas/CustomChartMetricRatio-Output'
            - type: 'null'
          title: Metric Definition
        group_by_definitions:
          anyOf:
            - items:
                anyOf:
                  - $ref: '#/components/schemas/CustomChartGroupByPlain'
                  - $ref: '#/components/schemas/CustomChartGroupByComplex'
              type: array
            - type: 'null'
          title: Group By Definitions
        filter_definition:
          anyOf:
            - $ref: '#/components/schemas/CustomChartFilterByTracingProject'
            - $ref: '#/components/schemas/CustomChartFilterByDataset'
            - type: 'null'
          title: Filter Definition
        id:
          anyOf:
            - type: string
              format: uuid
            - type: string
          title: Id
        group_by:
          anyOf:
            - $ref: '#/components/schemas/RunStatsGroupBySeriesResponse'
            - type: 'null'
      type: object
      required:
        - name
        - id
      title: CustomChartSeries
    CustomChartSeriesFilters:
      properties:
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
        session:
          anyOf:
            - items:
                type: string
                format: uuid
              type: array
            - type: 'null'
          title: Session
      type: object
      title: CustomChartSeriesFilters
    DashboardBreakpointLayout-Output:
      properties:
        rows:
          items:
            $ref: '#/components/schemas/DashboardLayoutRow'
          type: array
          title: Rows
      type: object
      required:
        - rows
      title: DashboardBreakpointLayout
    CustomChartMetric:
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
        - feedback
        - feedback_score_avg
        - feedback_values
        - total_cost
        - prompt_cost
        - completion_cost
        - error_rate
        - streaming_rate
        - cost_p50
        - cost_p99
      title: CustomChartMetric
      description: >-
        Metrics you can chart. Feedback metrics are not available for
        organization-scoped charts.
    HostProjectChartMetric:
      type: string
      enum:
        - memory_usage
        - cpu_usage
        - disk_usage
        - restart_count
        - replica_count
        - worker_count
        - lg_run_count
        - responses_per_second
        - error_responses_per_second
        - p95_latency
        - run_queue_wait_time
      title: HostProjectChartMetric
      description: LGP Metrics you can chart.
    CustomChartFeedbackCountMetric:
      properties:
        type:
          type: string
          const: count
          title: Type
          default: count
        entity:
          type: string
          const: feedback
          title: Entity
        filter:
          anyOf:
            - type: string
            - type: 'null'
          title: Filter
        params:
          $ref: '#/components/schemas/CustomChartFeedbackCountMetricParams'
      type: object
      required:
        - entity
        - params
      title: CustomChartFeedbackCountMetric
    CustomChartMetricCount:
      properties:
        type:
          type: string
          const: count
          title: Type
          default: count
        filter:
          anyOf:
            - type: string
            - type: 'null'
          title: Filter
      type: object
      title: CustomChartMetricCount
    CustomChartFeedbackScoreMetricScalar:
      properties:
        type:
          anyOf:
            - type: string
              const: sum
            - type: string
              const: max
            - type: string
              const: min
            - type: string
              const: avg
          title: Type
        field:
          type: string
          const: feedback_score
          title: Field
        filter:
          anyOf:
            - type: string
            - type: 'null'
          title: Filter
        params:
          $ref: '#/components/schemas/CustomChartFeedbackScoreMetricScalarParams'
      type: object
      required:
        - type
        - field
        - params
      title: CustomChartFeedbackScoreMetricScalar
    CustomChartMetricScalar:
      properties:
        type:
          anyOf:
            - type: string
              const: sum
            - type: string
              const: max
            - type: string
              const: min
            - type: string
              const: avg
          title: Type
        field:
          $ref: '#/components/schemas/CustomChartMetricField'
        filter:
          anyOf:
            - type: string
            - type: 'null'
          title: Filter
      type: object
      required:
        - type
        - field
      title: CustomChartMetricScalar
    CustomChartFeedbackScoreMetricPercentile:
      properties:
        type:
          type: string
          const: percentile
          title: Type
        filter:
          anyOf:
            - type: string
            - type: 'null'
          title: Filter
        field:
          type: string
          const: feedback_score
          title: Field
        params:
          $ref: '#/components/schemas/CustomChartFeedbackScoreMetricPercentileParams'
      type: object
      required:
        - type
        - field
        - params
      title: CustomChartFeedbackScoreMetricPercentile
    CustomChartMetricPercentile:
      properties:
        type:
          type: string
          const: percentile
          title: Type
        filter:
          anyOf:
            - type: string
            - type: 'null'
          title: Filter
        field:
          $ref: '#/components/schemas/CustomChartMetricField'
        params:
          $ref: '#/components/schemas/CustomChartMetricPercentileParams'
      type: object
      required:
        - type
        - field
        - params
      title: CustomChartMetricPercentile
    CustomChartMetricRatio-Output:
      properties:
        type:
          type: string
          const: ratio
          title: Type
        numerator:
          anyOf:
            - $ref: '#/components/schemas/CustomChartFeedbackCountMetric'
            - $ref: '#/components/schemas/CustomChartMetricCount'
            - $ref: '#/components/schemas/CustomChartFeedbackScoreMetricScalar'
            - $ref: '#/components/schemas/CustomChartMetricScalar'
            - $ref: '#/components/schemas/CustomChartFeedbackScoreMetricPercentile'
            - $ref: '#/components/schemas/CustomChartMetricPercentile'
          title: Numerator
        denominator:
          anyOf:
            - $ref: '#/components/schemas/CustomChartFeedbackCountMetric'
            - $ref: '#/components/schemas/CustomChartMetricCount'
            - $ref: '#/components/schemas/CustomChartFeedbackScoreMetricScalar'
            - $ref: '#/components/schemas/CustomChartMetricScalar'
            - $ref: '#/components/schemas/CustomChartFeedbackScoreMetricPercentile'
            - $ref: '#/components/schemas/CustomChartMetricPercentile'
          title: Denominator
      type: object
      required:
        - type
        - numerator
        - denominator
      title: CustomChartMetricRatio
    CustomChartGroupByPlain:
      properties:
        attribute:
          anyOf:
            - type: string
              const: name
            - type: string
              const: run_type
            - type: string
              const: tag
            - type: string
              const: project
            - type: string
              const: status
          title: Attribute
      type: object
      required:
        - attribute
      title: CustomChartGroupByPlain
    CustomChartGroupByComplex:
      properties:
        attribute:
          anyOf:
            - type: string
              const: metadata
            - type: string
              const: feedback_label
          title: Attribute
        path:
          type: string
          title: Path
      type: object
      required:
        - attribute
        - path
      title: CustomChartGroupByComplex
    CustomChartFilterByTracingProject:
      properties:
        source_type:
          type: string
          const: tracing_project
          title: Source Type
        run_filter:
          anyOf:
            - type: string
            - type: 'null'
          title: Run Filter
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
        project_ids:
          items:
            type: string
            format: uuid
          type: array
          title: Project Ids
      type: object
      required:
        - source_type
        - project_ids
      title: CustomChartFilterByTracingProject
    CustomChartFilterByDataset:
      properties:
        source_type:
          type: string
          const: dataset
          title: Source Type
        dataset_ids:
          items:
            type: string
            format: uuid
          type: array
          title: Dataset Ids
      type: object
      required:
        - source_type
        - dataset_ids
      title: CustomChartFilterByDataset
    RunStatsGroupBySeriesResponse:
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
        set_by:
          anyOf:
            - type: string
              enum:
                - section
                - series
            - type: 'null'
          title: Set By
      type: object
      required:
        - attribute
      title: RunStatsGroupBySeriesResponse
      description: Include additional information about where the group_by param was set.
    DashboardLayoutRow:
      properties:
        height_units:
          type: integer
          title: Height Units
        items:
          items:
            $ref: '#/components/schemas/DashboardLayoutItem'
          type: array
          minItems: 1
          title: Items
      type: object
      required:
        - height_units
        - items
      title: DashboardLayoutRow
    CustomChartFeedbackCountMetricParams:
      properties:
        feedback_key:
          type: string
          title: Feedback Key
      type: object
      required:
        - feedback_key
      title: CustomChartFeedbackCountMetricParams
    CustomChartFeedbackScoreMetricScalarParams:
      properties:
        feedback_key:
          type: string
          title: Feedback Key
      type: object
      required:
        - feedback_key
      title: CustomChartFeedbackScoreMetricScalarParams
    CustomChartMetricField:
      type: string
      enum:
        - latency_seconds
        - first_token_seconds
        - total_tokens
        - prompt_tokens
        - completion_tokens
        - prompt_token_details.cache_creation
        - prompt_token_details.cache_read
        - prompt_token_details.ephemeral_1h_input_tokens
        - prompt_token_details.ephemeral_5m_input_tokens
        - prompt_token_details.audio
        - prompt_token_details.image
        - prompt_token_details.video
        - completion_token_details.reasoning
        - completion_token_details.audio
        - completion_token_details.image
        - completion_token_details.video
        - total_cost
        - prompt_cost
        - completion_cost
        - feedback_score
      title: CustomChartMetricField
    CustomChartFeedbackScoreMetricPercentileParams:
      properties:
        p:
          type: number
          maximum: 1
          minimum: 0
          title: P
        feedback_key:
          type: string
          title: Feedback Key
      type: object
      required:
        - p
        - feedback_key
      title: CustomChartFeedbackScoreMetricPercentileParams
    CustomChartMetricPercentileParams:
      properties:
        p:
          type: number
          maximum: 1
          minimum: 0
          title: P
      type: object
      required:
        - p
      title: CustomChartMetricPercentileParams
    DashboardLayoutItem:
      properties:
        chart_id:
          type: string
          format: uuid
          title: Chart Id
        width_units:
          type: integer
          minimum: 20
          title: Width Units
      type: object
      required:
        - chart_id
        - width_units
      title: DashboardLayoutItem
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

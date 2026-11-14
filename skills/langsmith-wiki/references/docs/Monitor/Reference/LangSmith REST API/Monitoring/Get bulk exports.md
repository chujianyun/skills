# Get bulk exports

> Get the current workspace's bulk exports



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json get /api/v1/bulk-exports
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
  /api/v1/bulk-exports:
    get:
      tags:
        - bulk-exports
      summary: Get bulk exports
      description: Get the current workspace's bulk exports
      operationId: get_bulk_exports_api_v1_bulk_exports_get
      parameters:
        - name: limit
          in: query
          required: false
          schema:
            anyOf:
              - type: integer
                maximum: 1000
                minimum: 1
              - type: 'null'
            title: Limit
        - name: offset
          in: query
          required: false
          schema:
            type: integer
            minimum: 0
            title: Offset
            default: 0
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/BulkExport'
                title: Response Get Bulk Exports Api V1 Bulk Exports Get
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
    BulkExport:
      properties:
        bulk_export_destination_id:
          type: string
          format: uuid
          title: Bulk Export Destination Id
        session_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Session Id
        all_experiments:
          type: boolean
          title: All Experiments
          default: false
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
        filter:
          anyOf:
            - type: string
            - type: 'null'
          title: Filter
          description: >-
            LangSmith filter expression that selects the runs to export. Accepts
            the function-style syntax, for example eq(run_type, "llm"), and, on
            LangSmith Cloud and self-hosted versions that support it, the v2
            syntax, for example run_type:llm.

            See
            https://docs.langchain.com/langsmith/trace-query-syntax#filter-query-language
            for syntax.
        format:
          $ref: '#/components/schemas/BulkExportFormat'
          default: Parquet
        format_version:
          $ref: '#/components/schemas/BulkExportFormatVersion'
          default: v1
        compression:
          $ref: '#/components/schemas/BulkExportCompression'
          default: zstandard
        is_rollup_disabled:
          type: boolean
          title: Is Rollup Disabled
          default: false
        interval_hours:
          anyOf:
            - type: integer
            - type: 'null'
          title: Interval Hours
        export_fields:
          anyOf:
            - items:
                type: string
              type: array
            - type: 'null'
          title: Export Fields
        id:
          type: string
          format: uuid
          title: Id
        tenant_id:
          type: string
          format: uuid
          title: Tenant Id
        status:
          $ref: '#/components/schemas/BulkExportStatus'
        created_at:
          type: string
          format: date-time
          title: Created At
        updated_at:
          type: string
          format: date-time
          title: Updated At
        finished_at:
          anyOf:
            - type: string
              format: date-time
            - type: 'null'
          title: Finished At
        source_bulk_export_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Source Bulk Export Id
      type: object
      required:
        - bulk_export_destination_id
        - start_time
        - id
        - tenant_id
        - status
        - created_at
        - updated_at
        - finished_at
      title: BulkExport
    HTTPValidationError:
      properties:
        detail:
          items:
            type: string
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    BulkExportFormat:
      type: string
      enum:
        - Parquet
      title: BulkExportFormat
    BulkExportFormatVersion:
      type: string
      enum:
        - v1
        - v2_beta
      title: BulkExportFormatVersion
      description: Enum for bulk export format versions.
    BulkExportCompression:
      type: string
      enum:
        - none
        - gzip
        - snappy
        - zstandard
      title: BulkExportCompression
    BulkExportStatus:
      type: string
      enum:
        - Cancelled
        - Completed
        - Created
        - IntervalScheduled
        - Failed
        - TimedOut
        - Running
      title: BulkExportStatus
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

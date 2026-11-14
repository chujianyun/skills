# Get bulk export runs

> Get a bulk export's runs



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json get /api/v1/bulk-exports/{bulk_export_id}/runs
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
  /api/v1/bulk-exports/{bulk_export_id}/runs:
    get:
      tags:
        - bulk-exports
      summary: Get bulk export runs
      description: Get a bulk export's runs
      operationId: get_bulk_export_runs_api_v1_bulk_exports__bulk_export_id__runs_get
      parameters:
        - name: bulk_export_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
            title: Bulk Export Id
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
                  $ref: '#/components/schemas/BulkExportRun'
                title: >-
                  Response Get Bulk Export Runs Api V1 Bulk Exports  Bulk Export
                  Id  Runs Get
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
    BulkExportRun:
      properties:
        bulk_export_id:
          type: string
          format: uuid
          title: Bulk Export Id
        metadata:
          $ref: '#/components/schemas/BulkExportRunMetadata'
        session_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Session Id
        id:
          type: string
          format: uuid
          title: Id
        status:
          $ref: '#/components/schemas/BulkExportRunStatus'
        retry_number:
          type: integer
          title: Retry Number
          default: 0
        errors:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Errors
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
      type: object
      required:
        - bulk_export_id
        - metadata
        - id
        - status
        - created_at
        - updated_at
        - finished_at
      title: BulkExportRun
    HTTPValidationError:
      properties:
        detail:
          items:
            type: string
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    BulkExportRunMetadata:
      properties:
        prefix:
          type: string
          title: Prefix
        start_time:
          type: string
          format: date-time
          title: Start Time
        end_time:
          type: string
          format: date-time
          title: End Time
        execution_backend:
          anyOf:
            - type: string
              enum:
                - clickhouse
                - smithdb
            - type: 'null'
          title: Execution Backend
        result:
          anyOf:
            - $ref: '#/components/schemas/BulkExportRunProgress'
            - type: 'null'
      type: object
      required:
        - prefix
        - start_time
        - end_time
      title: BulkExportRunMetadata
    BulkExportRunStatus:
      type: string
      enum:
        - Cancelled
        - Completed
        - Created
        - Failed
        - TimedOut
        - Running
      title: BulkExportRunStatus
    BulkExportRunProgress:
      properties:
        rows_written:
          type: integer
          title: Rows Written
        exported_files:
          items:
            type: string
          type: array
          title: Exported Files
        export_path:
          type: string
          title: Export Path
        latest_cursor:
          anyOf:
            - type: string
            - type: 'null'
          title: Latest Cursor
        pending_upload:
          anyOf:
            - $ref: '#/components/schemas/PendingUpload'
            - type: 'null'
      type: object
      required:
        - rows_written
        - exported_files
        - export_path
        - latest_cursor
      title: BulkExportRunProgress
    PendingUpload:
      properties:
        target_cursor:
          anyOf:
            - type: string
            - type: 'null'
          title: Target Cursor
        file_path:
          type: string
          title: File Path
        rows_count:
          type: integer
          title: Rows Count
      type: object
      required:
        - target_cursor
        - file_path
        - rows_count
      title: PendingUpload
      description: |-
        Tracks a file upload that is in progress or needs to be verified.

        This allows us to handle cases where:
        1. File upload succeeds but progress update fails
        2. Job crashes during upload
        3. Need to verify uploaded files before advancing cursor
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

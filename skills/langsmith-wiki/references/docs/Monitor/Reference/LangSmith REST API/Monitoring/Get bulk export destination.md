# Get bulk export destination

> Get a single bulk export destination by ID



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json get /api/v1/bulk-exports/destinations/{destination_id}
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
  /api/v1/bulk-exports/destinations/{destination_id}:
    get:
      tags:
        - bulk-exports
      summary: Get bulk export destination
      description: Get a single bulk export destination by ID
      operationId: >-
        get_bulk_export_destination_api_v1_bulk_exports_destinations__destination_id__get
      parameters:
        - name: destination_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
            title: Destination Id
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BulkExportDestination'
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
    BulkExportDestination:
      properties:
        destination_type:
          $ref: '#/components/schemas/BulkExportDestinationType'
          default: s3
        display_name:
          type: string
          minLength: 1
          pattern: ^[a-zA-Z0-9\-_ ']+$
          title: Display Name
        config:
          $ref: '#/components/schemas/BulkExportDestinationS3Config'
        id:
          type: string
          format: uuid
          title: Id
        tenant_id:
          type: string
          format: uuid
          title: Tenant Id
        created_at:
          type: string
          format: date-time
          title: Created At
        updated_at:
          type: string
          format: date-time
          title: Updated At
        credentials_keys:
          items:
            type: string
          type: array
          title: Credentials Keys
      type: object
      required:
        - display_name
        - config
        - id
        - tenant_id
        - created_at
        - updated_at
        - credentials_keys
      title: BulkExportDestination
    HTTPValidationError:
      properties:
        detail:
          items:
            type: string
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    BulkExportDestinationType:
      type: string
      enum:
        - s3
      title: BulkExportDestinationType
    BulkExportDestinationS3Config:
      properties:
        endpoint_url:
          anyOf:
            - type: string
              maxLength: 2048
            - type: 'null'
          title: Endpoint Url
        prefix:
          type: string
          maxLength: 2048
          title: Prefix
          default: ''
        bucket_name:
          anyOf:
            - type: string
              maxLength: 63
              minLength: 3
            - type: 'null'
          title: Bucket Name
        region:
          anyOf:
            - type: string
              minLength: 1
            - type: 'null'
          title: Region
        s3_additional_kwargs:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: S3 Additional Kwargs
        config_kwargs_s3:
          anyOf:
            - $ref: '#/components/schemas/BotocoreS3Config'
            - type: 'null'
          description: >-
            Passed to botocore Config s3 parameter. Use {"addressing_style":
            "virtual"} for S3-compatible services that require virtual-hosted
            style addressing (e.g. Volcengine TOS), or {"addressing_style":
            "path"} for path-style.
        include_bucket_in_prefix:
          type: boolean
          title: Include Bucket In Prefix
          description: >-
            Whether to prepend the bucket name to the S3 file path. Defaults to
            True. Set to False to skip prepending the bucket name if bucket name
            is already in the endpoint URL.
          default: true
        aws_role_arn:
          anyOf:
            - type: string
            - type: 'null'
          title: Aws Role Arn
          description: >-
            AWS IAM role ARN that LangSmith assumes instead of using static
            credentials.
      type: object
      title: BulkExportDestinationS3Config
    BotocoreS3Config:
      properties:
        addressing_style:
          anyOf:
            - type: string
              enum:
                - auto
                - virtual
                - path
            - type: 'null'
          title: Addressing Style
          description: >-
            S3 addressing style. Use "virtual" for services that require
            virtual-hosted style (e.g. Volcengine TOS), "path" for path-style,
            or "auto" (default) to let boto3 decide.
        use_accelerate_endpoint:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Use Accelerate Endpoint
          description: Whether to use the S3 Accelerate endpoint.
        payload_signing_enabled:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Payload Signing Enabled
          description: Whether to SHA256 sign SigV4 payloads.
        us_east_1_regional_endpoint:
          anyOf:
            - type: string
              enum:
                - regional
                - legacy
            - type: 'null'
          title: Us East 1 Regional Endpoint
          description: Which S3 endpoint to use when region is us-east-1.
      type: object
      title: BotocoreS3Config
      description: >-
        Typed subset of botocore Config s3 parameter.


        See:
        https://botocore.amazonaws.com/v1/documentation/api/latest/reference/config.html
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

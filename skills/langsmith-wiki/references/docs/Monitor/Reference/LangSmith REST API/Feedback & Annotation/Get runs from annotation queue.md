# Get runs from annotation queue



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json get /api/v1/annotation-queues/{queue_id}/runs
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
  /api/v1/annotation-queues/{queue_id}/runs:
    get:
      tags:
        - annotation-queues
      summary: Get runs from annotation queue
      operationId: >-
        get_runs_from_annotation_queue_api_v1_annotation_queues__queue_id__runs_get
      parameters:
        - name: queue_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
            title: Queue Id
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
        - name: archived
          in: query
          required: false
          schema:
            anyOf:
              - type: boolean
              - type: 'null'
            title: Archived
        - name: include_stats
          in: query
          required: false
          schema:
            anyOf:
              - type: boolean
              - type: 'null'
            title: Include Stats
        - name: status
          in: query
          required: false
          schema:
            anyOf:
              - enum:
                  - needs_my_review
                  - needs_others_review
                  - completed
                type: string
              - type: 'null'
            title: Status
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/RunSchemaWithAnnotationQueueInfo'
                title: >-
                  Response Get Runs From Annotation Queue Api V1 Annotation
                  Queues  Queue Id  Runs Get
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
    RunSchemaWithAnnotationQueueInfo:
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
        queue_run_id:
          type: string
          format: uuid
          title: Queue Run Id
        last_reviewed_time:
          anyOf:
            - type: string
              format: date-time
            - type: 'null'
          title: Last Reviewed Time
        added_at:
          anyOf:
            - type: string
              format: date-time
            - type: 'null'
          title: Added At
        effective_added_at:
          anyOf:
            - type: string
              format: date-time
            - type: 'null'
          title: Effective Added At
        reserved_by:
          items:
            type: string
            format: uuid
          type: array
          title: Reserved By
          default: []
        completed_by:
          items:
            type: string
            format: uuid
          type: array
          title: Completed By
          default: []
        source_proposed_example_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Source Proposed Example Id
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
        - queue_run_id
      title: RunSchemaWithAnnotationQueueInfo
      description: Run schema with annotation queue info.
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

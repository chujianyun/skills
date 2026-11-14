# Add runs to annotation queue by key

> Self-hosted deployments require LangSmith `v0.16` or later.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json post /api/v1/annotation-queues/{queue_id}/runs/by-key
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
  /api/v1/annotation-queues/{queue_id}/runs/by-key:
    post:
      tags:
        - annotation-queues
      summary: Add runs to annotation queue by key
      description: Self-hosted deployments require LangSmith `v0.16` or later.
      operationId: >-
        add_runs_to_annotation_queue_by_key_api_v1_annotation_queues__queue_id__runs_by_key_post
      parameters:
        - name: queue_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
            title: Queue Id
        - name: extend_trace_retention
          in: query
          required: false
          schema:
            type: boolean
            default: false
            title: Extend Trace Retention
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: array
              items:
                $ref: '#/components/schemas/AddRunToQueueByKeyRequest'
              title: Runs
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/AnnotationQueueRunSchema'
                title: >-
                  Response Add Runs To Annotation Queue By Key Api V1 Annotation
                  Queues  Queue Id  Runs By Key Post
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
    AddRunToQueueByKeyRequest:
      properties:
        run_id:
          type: string
          format: uuid
          title: Run Id
        session_id:
          type: string
          format: uuid
          title: Session Id
        start_time:
          type: string
          format: date-time
          title: Start Time
        source_proposed_example_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Source Proposed Example Id
      type: object
      required:
        - run_id
        - session_id
        - start_time
      title: AddRunToQueueByKeyRequest
      description: Add run to AQ by SmithDB key. is_root derived server-side (LSAQ-141).
    AnnotationQueueRunSchema:
      properties:
        run_id:
          type: string
          format: uuid
          title: Run Id
        queue_id:
          type: string
          format: uuid
          title: Queue Id
        last_reviewed_time:
          anyOf:
            - type: string
              format: date-time
            - type: 'null'
          title: Last Reviewed Time
        added_at:
          type: string
          format: date-time
          title: Added At
        source_proposed_example_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Source Proposed Example Id
        id:
          type: string
          format: uuid
          title: Id
      type: object
      required:
        - run_id
        - queue_id
        - id
      title: AnnotationQueueRunSchema
    HTTPValidationError:
      properties:
        detail:
          items:
            type: string
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
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

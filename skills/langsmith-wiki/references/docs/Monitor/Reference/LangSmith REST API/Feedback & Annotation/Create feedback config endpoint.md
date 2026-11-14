# Create feedback config endpoint



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json post /api/v1/feedback-configs
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
  /api/v1/feedback-configs:
    post:
      tags:
        - feedback-configs
      summary: Create feedback config endpoint
      operationId: create_feedback_config_endpoint_api_v1_feedback_configs_post
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateFeedbackConfigSchema'
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/FeedbackConfigSchema'
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
    CreateFeedbackConfigSchema:
      properties:
        feedback_key:
          type: string
          title: Feedback Key
        feedback_config:
          $ref: '#/components/schemas/FeedbackConfig'
        is_lower_score_better:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Is Lower Score Better
          default: false
        is_enforced:
          type: boolean
          title: Is Enforced
          default: false
      type: object
      required:
        - feedback_key
        - feedback_config
      title: CreateFeedbackConfigSchema
    FeedbackConfigSchema:
      properties:
        id:
          type: string
          format: uuid
          title: Id
        feedback_key:
          type: string
          title: Feedback Key
        feedback_config:
          $ref: '#/components/schemas/FeedbackConfig'
        tenant_id:
          type: string
          format: uuid
          title: Tenant Id
        modified_at:
          type: string
          format: date-time
          title: Modified At
        is_lower_score_better:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Is Lower Score Better
        is_enforced:
          type: boolean
          title: Is Enforced
          default: false
        is_first:
          type: boolean
          title: Is First
          default: false
        is_deleted:
          type: boolean
          title: Is Deleted
          default: false
      type: object
      required:
        - id
        - feedback_key
        - feedback_config
        - tenant_id
        - modified_at
      title: FeedbackConfigSchema
    HTTPValidationError:
      properties:
        detail:
          items:
            type: string
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    FeedbackConfig:
      properties:
        type:
          $ref: '#/components/schemas/FeedbackType'
        min:
          anyOf:
            - type: number
            - type: 'null'
          title: Min
        max:
          anyOf:
            - type: number
            - type: 'null'
          title: Max
        categories:
          anyOf:
            - items:
                $ref: '#/components/schemas/FeedbackCategory'
              type: array
            - type: 'null'
          title: Categories
        allows_multiple_categories:
          type: boolean
          title: Allows Multiple Categories
          description: >-
            Whether a reviewer can pick several categories. Categorical feedback
            only.
          default: false
      type: object
      required:
        - type
      title: FeedbackConfig
    FeedbackType:
      type: string
      enum:
        - continuous
        - categorical
        - freeform
      title: FeedbackType
      description: Enum for feedback types.
    FeedbackCategory:
      properties:
        value:
          type: number
          title: Value
        label:
          anyOf:
            - type: string
              minLength: 1
            - type: 'null'
          title: Label
      type: object
      required:
        - value
      title: FeedbackCategory
      description: Specific value and label pair for feedback
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

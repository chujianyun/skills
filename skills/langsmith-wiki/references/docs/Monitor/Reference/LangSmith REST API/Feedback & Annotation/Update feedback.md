# Update feedback

> Replace an existing feedback entry with a new, modified entry.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json patch /api/v1/feedback/{feedback_id}
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
  /api/v1/feedback/{feedback_id}:
    patch:
      tags:
        - feedback
      summary: Update feedback
      description: Replace an existing feedback entry with a new, modified entry.
      operationId: update_feedback_api_v1_feedback__feedback_id__patch
      parameters:
        - name: feedback_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
            title: Feedback Id
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/FeedbackUpdateSchema'
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/FeedbackSchema'
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
    FeedbackUpdateSchema:
      properties:
        score:
          anyOf:
            - type: number
            - type: integer
            - type: boolean
            - type: 'null'
          title: Score
        value:
          anyOf:
            - type: number
            - type: integer
            - type: boolean
            - type: string
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Value
        comment:
          anyOf:
            - type: string
            - type: 'null'
          title: Comment
        correction:
          anyOf:
            - additionalProperties: true
              type: object
            - type: string
            - type: 'null'
          title: Correction
        feedback_config:
          anyOf:
            - $ref: '#/components/schemas/FeedbackConfig'
            - type: 'null'
      type: object
      title: FeedbackUpdateSchema
      description: Schema used for updating feedback
    FeedbackSchema:
      properties:
        created_at:
          type: string
          format: date-time
          title: Created At
        modified_at:
          type: string
          format: date-time
          title: Modified At
        key:
          type: string
          title: Key
        score:
          anyOf:
            - type: number
            - type: integer
            - type: boolean
            - type: 'null'
          title: Score
        value:
          anyOf:
            - type: number
            - type: integer
            - type: boolean
            - type: string
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Value
        comment:
          anyOf:
            - type: string
            - type: 'null'
          title: Comment
        correction:
          anyOf:
            - additionalProperties: true
              type: object
            - type: string
            - type: 'null'
          title: Correction
        feedback_group_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Feedback Group Id
        comparative_experiment_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Comparative Experiment Id
        run_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Run Id
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
        trace_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Trace Id
        start_time:
          anyOf:
            - type: string
              format: date-time
            - type: 'null'
          title: Start Time
        is_root:
          type: boolean
          title: Is Root
          default: false
        feedback_source:
          anyOf:
            - $ref: '#/components/schemas/FeedbackSource'
            - type: 'null'
        extra:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Extra
        feedback_thread_id:
          anyOf:
            - type: string
            - type: 'null'
          title: Feedback Thread Id
      type: object
      required:
        - key
        - id
      title: FeedbackSchema
      description: Schema for getting feedback.
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
    FeedbackSource:
      properties:
        type:
          anyOf:
            - type: string
            - type: 'null'
          title: Type
        metadata:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Metadata
        user_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: User Id
        ls_user_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Ls User Id
        user_name:
          anyOf:
            - type: string
            - type: 'null'
          title: User Name
      type: object
      title: FeedbackSource
      description: The feedback source loaded from the database.
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

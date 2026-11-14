# Create annotation queue



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json post /api/v1/annotation-queues
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
  /api/v1/annotation-queues:
    post:
      tags:
        - annotation-queues
      summary: Create annotation queue
      operationId: create_annotation_queue_api_v1_annotation_queues_post
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AnnotationQueueCreateSchema'
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AnnotationQueueSchema'
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
    AnnotationQueueCreateSchema:
      properties:
        description:
          anyOf:
            - type: string
            - type: 'null'
          title: Description
        created_at:
          type: string
          format: date-time
          title: Created At
        updated_at:
          type: string
          format: date-time
          title: Updated At
        num_reviewers_per_item:
          anyOf:
            - type: integer
            - type: 'null'
          title: Num Reviewers Per Item
          default: 1
        enable_reservations:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Enable Reservations
          default: true
        reservation_minutes:
          anyOf:
            - type: integer
            - type: 'null'
          title: Reservation Minutes
          default: 1
        reviewer_access_mode:
          type: string
          title: Reviewer Access Mode
          default: any
        name:
          type: string
          title: Name
        id:
          type: string
          format: uuid
          title: Id
        default_dataset:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Default Dataset
        rubric_items:
          anyOf:
            - items:
                $ref: '#/components/schemas/AnnotationQueueRubricItemSchema'
              type: array
            - type: 'null'
          title: Rubric Items
        rubric_instructions:
          anyOf:
            - type: string
            - type: 'null'
          title: Rubric Instructions
        session_ids:
          anyOf:
            - items:
                type: string
                format: uuid
              type: array
            - type: 'null'
          title: Session Ids
        metadata:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Metadata
      type: object
      required:
        - name
      title: AnnotationQueueCreateSchema
      description: AnnotationQueue schema.
    AnnotationQueueSchema:
      properties:
        description:
          anyOf:
            - type: string
            - type: 'null'
          title: Description
        created_at:
          type: string
          format: date-time
          title: Created At
        updated_at:
          type: string
          format: date-time
          title: Updated At
        num_reviewers_per_item:
          anyOf:
            - type: integer
            - type: 'null'
          title: Num Reviewers Per Item
          default: 1
        enable_reservations:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Enable Reservations
          default: true
        reservation_minutes:
          anyOf:
            - type: integer
            - type: 'null'
          title: Reservation Minutes
          default: 1
        reviewer_access_mode:
          type: string
          title: Reviewer Access Mode
          default: any
        name:
          type: string
          title: Name
        id:
          type: string
          format: uuid
          title: Id
        tenant_id:
          type: string
          format: uuid
          title: Tenant Id
        source_rule_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Source Rule Id
        run_rule_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Run Rule Id
        default_dataset:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Default Dataset
        queue_type:
          type: string
          enum:
            - single
            - pairwise
          title: Queue Type
        metadata:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Metadata
        assigned_reviewers:
          items:
            $ref: '#/components/schemas/AssignedReviewerSchema'
          type: array
          title: Assigned Reviewers
          default: []
      type: object
      required:
        - name
        - id
        - tenant_id
        - queue_type
      title: AnnotationQueueSchema
      description: AnnotationQueue schema.
    HTTPValidationError:
      properties:
        detail:
          items:
            type: string
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    AnnotationQueueRubricItemSchema:
      properties:
        feedback_key:
          type: string
          title: Feedback Key
        description:
          anyOf:
            - type: string
            - type: 'null'
          title: Description
        value_descriptions:
          anyOf:
            - type: object
              additionalProperties:
                type: string
            - type: 'null'
          title: Value Descriptions
        score_descriptions:
          anyOf:
            - type: object
              additionalProperties:
                type: string
            - type: 'null'
          title: Score Descriptions
        is_required:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Is Required
        required_if:
          anyOf:
            - $ref: '#/components/schemas/RubricItemConditions'
            - type: 'null'
        visible_if:
          anyOf:
            - $ref: '#/components/schemas/RubricItemConditions'
            - type: 'null'
        is_assertion:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Is Assertion
        regex_validator:
          anyOf:
            - anyOf:
                - type: string
                - $ref: '#/components/schemas/Missing'
              maxLength: 500
            - type: 'null'
          title: Regex Validator
          default:
            __missing__: __missing__
        feedback_config_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Feedback Config Id
        feedback_config:
          anyOf:
            - $ref: '#/components/schemas/FeedbackConfigSchema'
            - type: 'null'
          title: Feedback Config
      type: object
      required:
        - feedback_key
      title: AnnotationQueueRubricItemSchema
    AssignedReviewerSchema:
      properties:
        id:
          type: string
          format: uuid
          title: Id
        name:
          anyOf:
            - type: string
            - type: 'null'
          title: Name
        email:
          anyOf:
            - type: string
            - type: 'null'
          title: Email
      type: object
      required:
        - id
      title: AssignedReviewerSchema
      description: Identity info for an assigned reviewer on an annotation queue.
    RubricItemConditions:
      properties:
        join:
          type: string
          enum:
            - all
            - any
          title: Join
        rules:
          items:
            $ref: '#/components/schemas/RubricItemConditionRule'
          type: array
          minItems: 1
          title: Rules
      type: object
      required:
        - join
        - rules
      title: RubricItemConditions
    Missing:
      properties:
        __missing__:
          type: string
          const: __missing__
          title: Missing
      type: object
      required:
        - __missing__
      title: Missing
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
    RubricItemConditionRule:
      properties:
        key:
          type: string
          title: Key
        op:
          type: string
          enum:
            - is
            - is_one_of
            - is_empty
            - is_not_empty
          title: Op
        values:
          items:
            type: number
          type: array
          title: Values
          default: []
      type: object
      required:
        - key
        - op
      title: RubricItemConditionRule
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

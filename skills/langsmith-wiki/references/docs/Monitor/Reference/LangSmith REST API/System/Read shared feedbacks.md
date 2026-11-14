# Read shared feedbacks



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json get /api/v1/public/{share_token}/feedbacks
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
  /api/v1/public/{share_token}/feedbacks:
    get:
      tags:
        - public
      summary: Read shared feedbacks
      operationId: read_shared_feedbacks_api_v1_public__share_token__feedbacks_get
      parameters:
        - name: share_token
          in: path
          required: true
          schema:
            type: string
            format: uuid
            title: Share Token
        - name: run
          in: query
          required: false
          schema:
            anyOf:
              - items:
                  type: string
                  format: uuid
                type: array
              - type: 'null'
            title: Run
        - name: key
          in: query
          required: false
          schema:
            anyOf:
              - items:
                  type: string
                type: array
              - type: 'null'
            title: Key
        - name: session
          in: query
          required: false
          schema:
            anyOf:
              - items:
                  type: string
                  format: uuid
                type: array
              - type: 'null'
            title: Session
        - name: source
          in: query
          required: false
          schema:
            anyOf:
              - type: array
                items:
                  $ref: '#/components/schemas/SourceType'
              - type: 'null'
            title: Source
        - name: limit
          in: query
          required: false
          schema:
            type: integer
            maximum: 100
            minimum: 1
            title: Limit
            default: 100
        - name: offset
          in: query
          required: false
          schema:
            type: integer
            minimum: 0
            title: Offset
            default: 0
        - name: user
          in: query
          required: false
          schema:
            anyOf:
              - items:
                  type: string
                  format: uuid
                type: array
              - type: 'null'
            title: User
        - name: has_comment
          in: query
          required: false
          schema:
            anyOf:
              - type: boolean
              - type: 'null'
            title: Has Comment
        - name: has_score
          in: query
          required: false
          schema:
            anyOf:
              - type: boolean
              - type: 'null'
            title: Has Score
        - name: level
          in: query
          required: false
          schema:
            anyOf:
              - $ref: '#/components/schemas/FeedbackLevel'
              - type: 'null'
            title: Level
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/FeedbackSchema'
                title: >-
                  Response Read Shared Feedbacks Api V1 Public  Share Token
                  Feedbacks Get
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
components:
  schemas:
    SourceType:
      type: string
      enum:
        - api
        - model
        - app
        - auto_eval
      title: SourceType
      description: Enum for feedback source types.
    FeedbackLevel:
      type: string
      enum:
        - run
        - session
      title: FeedbackLevel
      description: Enum for feedback levels.
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

````

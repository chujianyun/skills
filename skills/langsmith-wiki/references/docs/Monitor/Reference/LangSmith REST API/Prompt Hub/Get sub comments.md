# Get sub comments



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json get /api/v1/comments/{owner}/{repo}/{parent_comment_id}
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
  /api/v1/comments/{owner}/{repo}/{parent_comment_id}:
    get:
      tags:
        - comments
      summary: Get sub comments
      operationId: get_sub_comments_api_v1_comments__owner___repo___parent_comment_id__get
      parameters:
        - name: owner
          in: path
          required: true
          schema:
            type: string
            title: Owner
        - name: repo
          in: path
          required: true
          schema:
            type: string
            title: Repo
        - name: parent_comment_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
            title: Parent Comment Id
        - name: limit
          in: query
          required: false
          schema:
            type: integer
            maximum: 100
            minimum: 1
            default: 20
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
                $ref: '#/components/schemas/ListCommentsResponse'
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
    ListCommentsResponse:
      properties:
        comments:
          items:
            $ref: '#/components/schemas/Comment'
          type: array
          title: Comments
        total:
          type: integer
          title: Total
      type: object
      required:
        - comments
        - total
      title: ListCommentsResponse
    HTTPValidationError:
      properties:
        detail:
          items:
            type: string
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    Comment:
      properties:
        id:
          type: string
          format: uuid
          title: Id
        comment_by:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Comment By
        comment_on:
          type: string
          format: uuid
          title: Comment On
        parent_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Parent Id
        content:
          type: string
          title: Content
        created_at:
          type: string
          format: date-time
          title: Created At
        updated_at:
          type: string
          format: date-time
          title: Updated At
        comment_by_name:
          anyOf:
            - type: string
            - type: 'null'
          title: Comment By Name
        num_sub_comments:
          type: integer
          title: Num Sub Comments
        num_likes:
          type: integer
          title: Num Likes
        liked_by_auth_user:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Liked By Auth User
      type: object
      required:
        - id
        - comment_on
        - content
        - created_at
        - updated_at
        - num_sub_comments
        - num_likes
      title: Comment
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

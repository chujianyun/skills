# Get shared tokens

> List all shared entities and their tokens by the workspace.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json get /api/v1/workspaces/current/shared
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
  /api/v1/workspaces/current/shared:
    get:
      tags:
        - workspaces
      summary: Get shared tokens
      description: List all shared entities and their tokens by the workspace.
      operationId: get_shared_tokens_api_v1_workspaces_current_shared_get
      parameters:
        - name: limit
          in: query
          required: false
          schema:
            type: integer
            maximum: 100
            minimum: 1
            default: 50
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
                $ref: '#/components/schemas/TenantShareTokensResponse'
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
    TenantShareTokensResponse:
      properties:
        entities:
          items:
            oneOf:
              - $ref: '#/components/schemas/TenantShareRunToken'
              - $ref: '#/components/schemas/TenantShareDatasetToken'
              - $ref: '#/components/schemas/TenantShareThreadToken'
            discriminator:
              propertyName: type
              mapping:
                dataset: '#/components/schemas/TenantShareDatasetToken'
                run: '#/components/schemas/TenantShareRunToken'
                thread: '#/components/schemas/TenantShareThreadToken'
          type: array
          title: Entities
      type: object
      required:
        - entities
      title: TenantShareTokensResponse
    HTTPValidationError:
      properties:
        detail:
          items:
            type: string
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    TenantShareRunToken:
      properties:
        type:
          type: string
          const: run
          title: Type
        share_token:
          type: string
          title: Share Token
        created_at:
          type: string
          format: date-time
          title: Created At
        run_id:
          type: string
          format: uuid
          title: Run Id
        run_name:
          anyOf:
            - type: string
            - type: 'null'
          title: Run Name
        run_type:
          anyOf:
            - type: string
            - type: 'null'
          title: Run Type
        session_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Session Id
        session_name:
          anyOf:
            - type: string
            - type: 'null'
          title: Session Name
      type: object
      required:
        - type
        - share_token
        - created_at
        - run_id
      title: TenantShareRunToken
    TenantShareDatasetToken:
      properties:
        type:
          type: string
          const: dataset
          title: Type
        share_token:
          type: string
          title: Share Token
        created_at:
          type: string
          format: date-time
          title: Created At
        dataset_id:
          type: string
          format: uuid
          title: Dataset Id
        dataset_name:
          anyOf:
            - type: string
            - type: 'null'
          title: Dataset Name
      type: object
      required:
        - type
        - share_token
        - created_at
        - dataset_id
      title: TenantShareDatasetToken
    TenantShareThreadToken:
      properties:
        type:
          type: string
          const: thread
          title: Type
        share_token:
          type: string
          title: Share Token
        created_at:
          type: string
          format: date-time
          title: Created At
        thread_id:
          type: string
          title: Thread Id
        session_id:
          type: string
          format: uuid
          title: Session Id
        session_name:
          anyOf:
            - type: string
            - type: 'null'
          title: Session Name
      type: object
      required:
        - type
        - share_token
        - created_at
        - thread_id
        - session_id
      title: TenantShareThreadToken
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

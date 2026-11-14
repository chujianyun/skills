# Create prompt webhook

> Create a new prompt webhook.

LangSmith sends a POST request to the webhook URL for each event listed in
triggers on the prompts it matches. A workspace can have one prompt webhook
unless its limit was raised; creating one past the limit returns 400.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json post /api/v1/prompt-webhooks
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
  /api/v1/prompt-webhooks:
    post:
      tags:
        - prompt-webhooks
      summary: Create prompt webhook
      description: >-
        Create a new prompt webhook.


        LangSmith sends a POST request to the webhook URL for each event listed
        in

        triggers on the prompts it matches. A workspace can have one prompt
        webhook

        unless its limit was raised; creating one past the limit returns 400.
      operationId: create_prompt_webhook_api_v1_prompt_webhooks_post
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PromptWebhookCreate'
        required: true
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PromptWebhook'
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
    PromptWebhookCreate:
      properties:
        url:
          type: string
          minLength: 1
          format: uri
          title: Url
          description: URL that receives a POST request with the prompt event payload.
        headers:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Headers
          description: >-
            HTTP headers sent with each request, for example an Authorization
            header. Values are stored encrypted and are masked in responses to
            callers who cannot update prompts.
        include_prompts:
          anyOf:
            - items:
                type: string
                format: uuid
              type: array
            - type: 'null'
          title: Include Prompts
          description: >-
            IDs of the prompts whose events fire the webhook. When empty, events
            from every prompt in the workspace fire it.
        exclude_prompts:
          anyOf:
            - items:
                type: string
                format: uuid
              type: array
            - type: 'null'
          title: Exclude Prompts
          description: IDs of prompts whose events never fire the webhook.
        triggers:
          items:
            $ref: '#/components/schemas/EPromptWebhookTrigger'
          type: array
          title: Triggers
          description: >-
            Events that fire the webhook: commit (a new prompt commit),
            tag:create, and tag:update. A webhook with no triggers never fires.
        id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Id
          description: ID to assign to the webhook. Generated when omitted.
      type: object
      required:
        - url
      title: PromptWebhookCreate
      description: Schema for creating a prompt webhook.
    PromptWebhook:
      properties:
        url:
          type: string
          minLength: 1
          format: uri
          title: Url
          description: URL that receives a POST request with the prompt event payload.
        headers:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Headers
          description: >-
            HTTP headers sent with each request, for example an Authorization
            header. Values are stored encrypted and are masked in responses to
            callers who cannot update prompts.
        include_prompts:
          anyOf:
            - items:
                type: string
                format: uuid
              type: array
            - type: 'null'
          title: Include Prompts
          description: >-
            IDs of the prompts whose events fire the webhook. When empty, events
            from every prompt in the workspace fire it.
        exclude_prompts:
          anyOf:
            - items:
                type: string
                format: uuid
              type: array
            - type: 'null'
          title: Exclude Prompts
          description: IDs of prompts whose events never fire the webhook.
        triggers:
          items:
            $ref: '#/components/schemas/EPromptWebhookTrigger'
          type: array
          title: Triggers
          description: >-
            Events that fire the webhook: commit (a new prompt commit),
            tag:create, and tag:update. A webhook with no triggers never fires.
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
      type: object
      required:
        - url
        - id
        - tenant_id
        - created_at
        - updated_at
      title: PromptWebhook
      description: Schema for a prompt webhook.
    HTTPValidationError:
      properties:
        detail:
          items:
            type: string
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    EPromptWebhookTrigger:
      type: string
      enum:
        - commit
        - tag:create
        - tag:update
      title: EPromptWebhookTrigger
      description: Valid trigger types for prompt webhooks.
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

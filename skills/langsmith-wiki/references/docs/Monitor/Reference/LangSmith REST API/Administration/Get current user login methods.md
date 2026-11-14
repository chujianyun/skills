# Get current user login methods

> Get login methods for the current user.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json get /api/v1/orgs/current/user/login-methods
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
  /api/v1/orgs/current/user/login-methods:
    get:
      tags:
        - orgs
      summary: Get current user login methods
      description: Get login methods for the current user.
      operationId: >-
        get_current_user_login_methods_api_v1_orgs_current_user_login_methods_get
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                items:
                  $ref: '#/components/schemas/ProviderUserSlim'
                type: array
                title: >-
                  Response Get Current User Login Methods Api V1 Orgs Current
                  User Login Methods Get
      security:
        - API Key: []
        - Organization ID: []
        - Bearer Auth: []
components:
  schemas:
    ProviderUserSlim:
      properties:
        id:
          type: string
          format: uuid
          title: Id
        provider:
          anyOf:
            - $ref: '#/components/schemas/AuthProvider'
            - type: 'null'
        ls_user_id:
          type: string
          format: uuid
          title: Ls User Id
        saml_provider_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Saml Provider Id
        provider_user_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Provider User Id
        created_at:
          type: string
          format: date-time
          title: Created At
        updated_at:
          type: string
          format: date-time
          title: Updated At
        email:
          anyOf:
            - type: string
            - type: 'null'
          title: Email
        full_name:
          anyOf:
            - type: string
            - type: 'null'
          title: Full Name
        first_name:
          anyOf:
            - type: string
            - type: 'null'
          title: First Name
        last_name:
          anyOf:
            - type: string
            - type: 'null'
          title: Last Name
        username:
          anyOf:
            - type: string
            - type: 'null'
          title: Username
        is_disabled:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Is Disabled
        provisioning_method:
          anyOf:
            - $ref: '#/components/schemas/ProvisioningMethod'
            - type: 'null'
        email_confirmed_at:
          anyOf:
            - type: string
              format: date-time
            - type: 'null'
          title: Email Confirmed At
      type: object
      required:
        - id
        - ls_user_id
        - created_at
        - updated_at
      title: ProviderUserSlim
    AuthProvider:
      type: string
      enum:
        - email
        - supabase:non-sso
        - supabase:sso
        - oidc
        - custom-oidc
        - oidc-sso
      title: AuthProvider
    ProvisioningMethod:
      type: string
      enum:
        - scim
        - saml:jit
        - bootstrap
      title: ProvisioningMethod
  securitySchemes:
    API Key:
      type: apiKey
      in: header
      name: X-API-Key
    Organization ID:
      type: apiKey
      in: header
      name: X-Organization-Id
    Bearer Auth:
      type: http
      description: >-
        Bearer tokens are used to authenticate from the UI. Must also specify
        x-tenant-id or x-organization-id (for org scoped apis).
      scheme: bearer

````

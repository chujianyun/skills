# List organizations

> Get all orgs visible to this auth



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json get /api/v1/orgs
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
  /api/v1/orgs:
    get:
      tags:
        - orgs
      summary: List organizations
      description: Get all orgs visible to this auth
      operationId: list_organizations_api_v1_orgs_get
      parameters:
        - name: skip_create
          in: query
          required: false
          schema:
            type: boolean
            default: false
            title: Skip Create
        - name: include_tier
          in: query
          required: false
          schema:
            type: boolean
            default: false
            title: Include Tier
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/OrganizationPGSchemaSlim'
                title: Response List Organizations Api V1 Orgs Get
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
      security:
        - Bearer Auth: []
components:
  schemas:
    OrganizationPGSchemaSlim:
      properties:
        id:
          type: string
          format: uuid
          title: Id
        display_name:
          type: string
          title: Display Name
        avatar_url:
          anyOf:
            - type: string
            - type: 'null'
          title: Avatar Url
        tier:
          anyOf:
            - $ref: '#/components/schemas/PaymentPlanTier'
            - type: 'null'
        created_at:
          anyOf:
            - type: string
              format: date-time
            - type: 'null'
          title: Created At
        created_by_user_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Created By User Id
        created_by_ls_user_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Created By Ls User Id
        modified_at:
          anyOf:
            - type: string
              format: date-time
            - type: 'null'
          title: Modified At
        is_personal:
          type: boolean
          title: Is Personal
        disabled:
          type: boolean
          title: Disabled
        sso_login_slug:
          anyOf:
            - type: string
            - type: 'null'
          title: Sso Login Slug
        sso_only:
          type: boolean
          title: Sso Only
          default: false
        jit_provisioning_enabled:
          type: boolean
          title: Jit Provisioning Enabled
          default: true
        invites_enabled:
          type: boolean
          title: Invites Enabled
          default: true
        public_sharing_disabled:
          type: boolean
          title: Public Sharing Disabled
          default: false
        pat_creation_disabled:
          type: boolean
          title: Pat Creation Disabled
          default: false
        api_key_creation_from_api_keys_enabled:
          type: boolean
          title: Api Key Creation From Api Keys Enabled
        workspace_admin_can_invite_to_org:
          type: boolean
          title: Workspace Admin Can Invite To Org
          default: false
        byoc_create_saas_workspace_enabled:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Byoc Create Saas Workspace Enabled
        default_sso_provision:
          type: boolean
          title: Default Sso Provision
          default: false
        max_api_key_expiry_days:
          anyOf:
            - type: integer
            - type: 'null'
          title: Max Api Key Expiry Days
        security_contact:
          anyOf:
            - type: string
            - type: 'null'
          title: Security Contact
        max_pat_expiry_days:
          anyOf:
            - type: integer
            - type: 'null'
          title: Max Pat Expiry Days
        max_service_key_expiry_days:
          anyOf:
            - type: integer
            - type: 'null'
          title: Max Service Key Expiry Days
        max_tracing_key_expiry_days:
          anyOf:
            - type: integer
            - type: 'null'
          title: Max Tracing Key Expiry Days
        scim_group_name_separator:
          type: string
          title: Scim Group Name Separator
          default: ':'
        llm_auth_proxy_enabled:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Llm Auth Proxy Enabled
        oidc_login_enabled:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Oidc Login Enabled
        llm_auth_proxy_jwt_audience:
          anyOf:
            - type: string
            - type: 'null'
          title: Llm Auth Proxy Jwt Audience
        ip_allowlist:
          anyOf:
            - items:
                type: string
              type: array
            - type: 'null'
          title: Ip Allowlist
        disabled_model_providers:
          anyOf:
            - items:
                type: string
              type: array
            - type: 'null'
          title: Disabled Model Providers
        restrict_browser_secrets:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Restrict Browser Secrets
        llm_auth_proxy_allowed_urls:
          anyOf:
            - items:
                type: string
              type: array
            - type: 'null'
          title: Llm Auth Proxy Allowed Urls
        topic_search_enabled:
          type: boolean
          title: Topic Search Enabled
          default: false
        engine_enabled:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Engine Enabled
        engine_lcu_spend_limit_monthly:
          anyOf:
            - type: string
              pattern: ^(?!^[-+.]*$)[+-]?0*\d*\.?\d*$
            - type: 'null'
          title: Engine Lcu Spend Limit Monthly
        managed_evals_enabled:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Managed Evals Enabled
      type: object
      required:
        - id
        - display_name
        - is_personal
        - disabled
      title: OrganizationPGSchemaSlim
      description: Schema for an organization in postgres for list views.
    HTTPValidationError:
      properties:
        detail:
          items:
            type: string
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    PaymentPlanTier:
      type: string
      enum:
        - no_plan
        - developer
        - developer_01_2026
        - developer_07_2026
        - developer_10_2026
        - plus
        - plus_01_2026
        - plus_07_2026
        - plus_10_2026
        - enterprise
        - developer_legacy
        - plus_legacy
        - free
        - free_07_2026
        - free_10_2026
        - enterprise_legacy
        - startup
        - startup_v0
        - startup_07_2026
        - startup_10_2026
        - partner
        - premier
      title: PaymentPlanTier
  securitySchemes:
    Bearer Auth:
      type: http
      description: >-
        Bearer tokens are used to authenticate from the UI. Must also specify
        x-tenant-id or x-organization-id (for org scoped apis).
      scheme: bearer

````

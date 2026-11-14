# Get current active workspace members



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json get /api/v1/workspaces/current/members/active
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
  /api/v1/workspaces/current/members/active:
    get:
      tags:
        - workspaces
      summary: Get current active workspace members
      operationId: >-
        get_current_active_workspace_members_api_v1_workspaces_current_members_active_get
      parameters:
        - name: limit
          in: query
          required: false
          schema:
            type: integer
            maximum: 500
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
        - name: emails
          in: query
          required: false
          schema:
            type: array
            items:
              type: string
            default: []
            title: Emails
        - name: q
          in: query
          required: false
          schema:
            anyOf:
              - type: string
              - type: 'null'
            description: Search query for email or name
            title: Q
          description: Search query for email or name
        - name: sort_by_desc
          in: query
          required: false
          schema:
            type: boolean
            description: Sort in descending order
            default: true
            title: Sort By Desc
          description: Sort in descending order
        - name: ls_user_ids
          in: query
          required: false
          schema:
            type: array
            items:
              type: string
              format: uuid
            default: []
            title: Ls User Ids
        - name: user_ids
          in: query
          required: false
          schema:
            type: array
            items:
              type: string
              format: uuid
            deprecated: true
            title: User Ids
          deprecated: true
        - name: is_disabled
          in: query
          required: false
          schema:
            anyOf:
              - type: boolean
              - type: 'null'
            title: Is Disabled
        - name: sort_by
          in: query
          required: false
          schema:
            $ref: '#/components/schemas/MemberSortField'
            description: Field to sort by
            default: created_at
          description: Field to sort by
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/MemberIdentity'
                title: >-
                  Response Get Current Active Workspace Members Api V1
                  Workspaces Current Members Active Get
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
    MemberSortField:
      type: string
      enum:
        - name
        - email
        - role
        - created_at
      title: MemberSortField
      description: Sort fields for members list endpoints.
    MemberIdentity:
      properties:
        id:
          type: string
          format: uuid
          title: Id
        organization_id:
          type: string
          format: uuid
          title: Organization Id
        tenant_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Tenant Id
        created_at:
          type: string
          format: date-time
          title: Created At
        user_id:
          type: string
          format: uuid
          title: User Id
        ls_user_id:
          type: string
          format: uuid
          title: Ls User Id
        read_only:
          type: boolean
          title: Read Only
          deprecated: true
        role_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Role Id
        role_name:
          anyOf:
            - type: string
            - type: 'null'
          title: Role Name
        access_scope:
          $ref: '#/components/schemas/AccessScope'
          default: workspace
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
        avatar_url:
          anyOf:
            - type: string
            - type: 'null'
          title: Avatar Url
        linked_login_methods:
          items:
            $ref: '#/components/schemas/ProviderUserSlim'
          type: array
          title: Linked Login Methods
          default: []
        display_name:
          anyOf:
            - type: string
            - type: 'null'
          title: Display Name
        is_disabled:
          type: boolean
          title: Is Disabled
          default: false
        org_identity_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Org Identity Id
        org_role_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Org Role Id
        org_role_name:
          anyOf:
            - type: string
            - type: 'null'
          title: Org Role Name
      type: object
      required:
        - id
        - organization_id
        - created_at
        - user_id
        - ls_user_id
        - read_only
      title: MemberIdentity
    HTTPValidationError:
      properties:
        detail:
          items:
            type: string
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    AccessScope:
      type: string
      enum:
        - organization
        - workspace
      title: AccessScope
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

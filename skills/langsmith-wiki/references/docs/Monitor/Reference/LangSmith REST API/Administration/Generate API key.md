# Generate API key

> Generate an api key for the user.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json post /api/v1/api-key
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
  /api/v1/api-key:
    post:
      tags:
        - api-key
      summary: Generate API key
      description: Generate an api key for the user.
      operationId: generate_api_key_api_v1_api_key_post
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/APIKeyCreateRequest'
              default:
                description: Default API key
                read_only: false
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/APIKeyCreateResponse'
        '403':
          description: >-
            Insufficient permission or the organization blocks API keys from
            creating other API keys.
          content:
            application/problem+json:
              schema:
                $ref: '#/components/schemas/ProblemDetails'
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
    APIKeyCreateRequest:
      properties:
        description:
          type: string
          title: Description
          default: Default API key
        read_only:
          type: boolean
          title: Read Only
          default: false
          deprecated: true
        expires_at:
          anyOf:
            - type: string
              format: date-time
            - type: 'null'
          title: Expires At
        workspaces:
          anyOf:
            - items:
                type: string
                format: uuid
              type: array
            - type: 'null'
          title: Workspaces
        role_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Role Id
        org_role_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Org Role Id
        default_workspace_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Default Workspace Id
      type: object
      title: APIKeyCreateRequest
      description: >-
        API key POST schema.


        expires_at: Optional datetime when the API key will expire.

        workspaces: List of workspace UUIDs this key can access
        (feature-flagged).

        role_id: Optional UUID of the role to assign to API key.
            If not provided, uses default role based on read_only flag:
            - WORKSPACE_ADMIN if read_only is False
            - WORKSPACE_READER if read_only is True
        org_role_id: UUID of an org role for service keys.
            Workspace-scoped keys accept only the built-in ORGANIZATION_VIEWER
            or ORGANIZATION_RESTRICTED role.
            Defaults to ORGANIZATION_VIEWER for workspace-scoped keys,
            or ORGANIZATION_USER for org-scoped keys.
        default_workspace_id: UUID of the default workspace for PATs.
            If not provided, uses the current logic (first available workspace).
    APIKeyCreateResponse:
      properties:
        created_at:
          anyOf:
            - type: string
              format: date-time
            - type: 'null'
          title: Created At
        id:
          type: string
          format: uuid
          title: Id
        short_key:
          type: string
          title: Short Key
        description:
          type: string
          title: Description
        read_only:
          type: boolean
          title: Read Only
          default: false
          deprecated: true
        last_used_at:
          anyOf:
            - type: string
              format: date-time
            - type: 'null'
          title: Last Used At
        expires_at:
          anyOf:
            - type: string
              format: date-time
            - type: 'null'
          title: Expires At
        revoked_at:
          anyOf:
            - type: string
              format: date-time
            - type: 'null'
          title: Revoked At
        workspace_names:
          anyOf:
            - items:
                type: string
              type: array
            - type: 'null'
          title: Workspace Names
        default_workspace_name:
          anyOf:
            - type: string
            - type: 'null'
          title: Default Workspace Name
        role_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Role Id
        org_role_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Org Role Id
        access_scope:
          anyOf:
            - $ref: '#/components/schemas/AccessScope'
            - type: 'null'
        created_by:
          anyOf:
            - type: string
            - type: 'null'
          title: Created By
        is_tracing_key:
          type: boolean
          title: Is Tracing Key
          default: false
        workspace_ids:
          items:
            type: string
            format: uuid
          type: array
          title: Workspace Ids
          default: []
        can_delete:
          type: boolean
          title: Can Delete
          description: >-
            Whether tracing-key deletion authority has been confirmed. Legacy
            key responses do not evaluate this capability.
          default: false
        key:
          type: string
          title: Key
      type: object
      required:
        - id
        - short_key
        - description
        - key
      title: APIKeyCreateResponse
      description: API key POST schema.
    ProblemDetails:
      properties:
        type:
          type: string
          title: Type
        title:
          type: string
          title: Title
        status:
          type: integer
          title: Status
        detail:
          type: string
          title: Detail
      type: object
      required:
        - type
        - title
        - status
        - detail
      title: ProblemDetails
      description: Problem details describing an error response, as defined by RFC 7807.
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

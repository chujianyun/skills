# Get current pending org members



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json get /api/v1/orgs/current/members/pending
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
  /api/v1/orgs/current/members/pending:
    get:
      tags:
        - orgs
      summary: Get current pending org members
      operationId: get_current_pending_org_members_api_v1_orgs_current_members_pending_get
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
                  $ref: '#/components/schemas/OrgPendingIdentity'
                title: >-
                  Response Get Current Pending Org Members Api V1 Orgs Current
                  Members Pending Get
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
      security:
        - API Key: []
        - Organization ID: []
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
    OrgPendingIdentity:
      properties:
        email:
          type: string
          title: Email
        read_only:
          type: boolean
          title: Read Only
          default: false
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
        workspace_ids:
          anyOf:
            - items:
                type: string
                format: uuid
              type: array
            - type: 'null'
          title: Workspace Ids
        workspace_role_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Workspace Role Id
        workspace_role_name:
          anyOf:
            - type: string
            - type: 'null'
          title: Workspace Role Name
        password:
          anyOf:
            - type: string
            - type: 'null'
          title: Password
        full_name:
          anyOf:
            - type: string
            - type: 'null'
          title: Full Name
        access_scope:
          $ref: '#/components/schemas/AccessScope'
          default: workspace
        id:
          type: string
          format: uuid
          title: Id
        user_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: User Id
        tenant_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Tenant Id
        organization_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Organization Id
        created_at:
          type: string
          format: date-time
          title: Created At
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
        tenant_ids:
          items:
            type: string
            format: uuid
          type: array
          title: Tenant Ids
          default: []
      type: object
      required:
        - email
        - id
        - created_at
      title: OrgPendingIdentity
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

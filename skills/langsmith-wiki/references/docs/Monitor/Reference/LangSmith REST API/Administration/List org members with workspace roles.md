# List org members with workspace roles

> Returns a paginated list of org members (active and pending) enriched with workspace memberships.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json get /api/v1/platform/orgs/current/members
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
  /api/v1/platform/orgs/current/members:
    get:
      tags:
        - orgs
      summary: List org members with workspace roles
      description: >-
        Returns a paginated list of org members (active and pending) enriched
        with workspace memberships.
      parameters:
        - description: Page size (default 50, max 500)
          name: limit
          in: query
          schema:
            type: integer
            title: Limit
        - description: Page offset (default 0)
          name: offset
          in: query
          schema:
            type: integer
            title: Offset
        - description: 'Filter: true = only active members; false = only pending members'
          name: active_is
          in: query
          schema:
            type: boolean
            title: Active Is
        - description: 'Filter: true = only pending members; false = only active members'
          name: pending_is
          in: query
          schema:
            type: boolean
            title: Pending Is
        - description: >-
            Glob filter on display name; use * as wildcard (repeatable, matches
            any)
          name: name_like
          in: query
          style: form
          explode: true
          schema:
            type: array
            items:
              type: string
            title: Name Like
        - description: Glob filter on email; use * as wildcard (repeatable, matches any)
          name: email_like
          in: query
          style: form
          explode: true
          schema:
            type: array
            items:
              type: string
            title: Email Like
        - description: >-
            Glob filter on workspace name or ID; use * as wildcard (repeatable,
            matches any)
          name: workspace_name_like
          in: query
          style: form
          explode: true
          schema:
            type: array
            items:
              type: string
            title: Workspace Name Like
        - description: >-
            Glob filter on organization role name; use * as wildcard
            (repeatable, matches any)
          name: organization_role_like
          in: query
          style: form
          explode: true
          schema:
            type: array
            items:
              type: string
            title: Organization Role Like
        - description: >-
            Glob filter on workspace role name; use * as wildcard (repeatable,
            matches any)
          name: workspace_role_like
          in: query
          style: form
          explode: true
          schema:
            type: array
            items:
              type: string
            title: Workspace Role Like
      responses:
        '200':
          description: Org members
          headers:
            X-Members-Anonymity-Restricted:
              description: >-
                Set to 'true' when the response was restricted by the
                organization's anonymity setting.
              schema:
                type: string
            X-Members-List-All-Workspaces:
              description: true if caller has organization:members:manage
              schema:
                type: string
            X-Pagination-Total:
              description: Total number of matching members
              schema:
                type: string
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/orgs.OrgMemberEnriched'
        '400':
          description: Bad request
          content:
            application/json:
              schema:
                type: object
                additionalProperties:
                  type: string
        '401':
          description: Unauthorized
          content:
            application/json:
              schema:
                type: object
                additionalProperties:
                  type: string
        '500':
          description: Internal server error
          content:
            application/json:
              schema:
                type: object
                additionalProperties:
                  type: string
      security:
        - API Key: []
        - Organization ID: []
        - Bearer Auth: []
components:
  schemas:
    orgs.OrgMemberEnriched:
      type: object
      properties:
        avatar_url:
          type: string
        created_at:
          type: string
        display_name:
          description: auth-resolved display name
          type: string
        email:
          type: string
        id:
          description: identity_id or pending_identity_id
          type: string
        is_disabled:
          description: user disabled
          type: boolean
        is_pending:
          description: true for pending invitations
          type: boolean
        linked_login_methods:
          type: array
          items:
            $ref: '#/components/schemas/orgs.LinkedLoginMethod'
        ls_user_id:
          description: nil for pending members
          type: string
        role_id:
          description: org role
          type: string
        role_name:
          description: org role name
          type: string
        scim_groups:
          type: array
          items:
            $ref: '#/components/schemas/orgs.SCIMGroup'
        workspace_memberships:
          type: array
          items:
            $ref: '#/components/schemas/orgs.WorkspaceMembership'
    orgs.LinkedLoginMethod:
      type: object
      properties:
        provider:
          type: string
        provisioning:
          description: provisioning_method
          type: string
    orgs.SCIMGroup:
      type: object
      properties:
        created_at:
          type: string
        name:
          type: string
    orgs.WorkspaceMembership:
      type: object
      properties:
        role_id:
          type: string
        role_name:
          type: string
        workspace_id:
          type: string
        workspace_name:
          type: string
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

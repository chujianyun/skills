# List organization teams

> Lists the organization's teams in name order. A page carries next_cursor, which is
the value to send back as cursor for the next page, and null once the last page
has been read. A cursor this endpoint did not issue, or one issued for different
filters, starts again at the first page. Organization scoped teams are listed when
the caller has organization:teams:read. Workspace scoped teams are listed only in
workspaces where the caller has workspaces:teams:read. With workspace_id, the list
has the workspace's own teams and the organization scoped teams granted into it,
each with role_id and role_name; granted teams are also listed when the caller has
workspaces:teams:read in that workspace.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json get /api/v1/platform/orgs/current/teams
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
  /api/v1/platform/orgs/current/teams:
    get:
      tags:
        - teams
      summary: List organization teams
      description: >-
        Lists the organization's teams in name order. A page carries
        next_cursor, which is

        the value to send back as cursor for the next page, and null once the
        last page

        has been read. A cursor this endpoint did not issue, or one issued for
        different

        filters, starts again at the first page. Organization scoped teams are
        listed when

        the caller has organization:teams:read. Workspace scoped teams are
        listed only in

        workspaces where the caller has workspaces:teams:read. With
        workspace_id, the list

        has the workspace's own teams and the organization scoped teams granted
        into it,

        each with role_id and role_name; granted teams are also listed when the
        caller has

        workspaces:teams:read in that workspace.
      parameters:
        - description: Only return teams that belong to or are granted into this workspace
          name: workspace_id
          in: query
          schema:
            type: string
            format: uuid
            title: Workspace Id
        - description: Only return workspace teams under this organization-wide team
          name: parent_team_id
          in: query
          schema:
            format: uuid
            type: string
            title: Parent Team Id
        - description: Only return teams this organization identity is a direct member of
          name: identity_id
          in: query
          schema:
            type: string
            format: uuid
            title: Identity Id
        - description: Teams per page
          name: page_size
          in: query
          schema:
            type: integer
            maximum: 100
            minimum: 1
            title: Page Size
            default: 20
        - description: Where to resume, taken from the previous page
          name: cursor
          in: query
          schema:
            type: string
            title: Cursor
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/teams.ListTeamsResponse'
        '400':
          description: invalid page_size, workspace_id, parent_team_id or identity_id
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/shared.ProblemDetails'
        '403':
          description: Forbidden
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/shared.ProblemDetails'
        '500':
          description: Internal Server Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/shared.ProblemDetails'
      security:
        - API Key: []
          Organization ID: []
        - Bearer Auth: []
          Organization ID: []
components:
  schemas:
    teams.ListTeamsResponse:
      type: object
      required:
        - items
        - next_cursor
      properties:
        items:
          type: array
          items:
            $ref: '#/components/schemas/teams.TeamListItem'
        next_cursor:
          anyOf:
            - type: string
            - type: 'null'
    shared.ProblemDetails:
      description: RFC 7807 problem details returned on V2 API errors.
      type: object
      properties:
        detail:
          type: string
        details:
          description: >-
            Details is a LangSmith extension carrying structured fields for
            ErrorClass.
          allOf:
            - $ref: '#/components/schemas/shared.ParseErrorDetails'
        error_class:
          description: |-
            ErrorClass is a LangSmith extension sub-categorizing a status code.
            Additional values require expanding this enum and adding a oneOf
            discriminator on Details to keep the class↔details contract typed.
          type: string
          enum:
            - PARSE_FAILURE
        instance:
          type: string
        remedy:
          description: Remedy is a LangSmith extension for user-recoverable errors.
          type: string
        status:
          type: integer
        title:
          type: string
        type:
          type: string
    teams.TeamListItem:
      type: object
      required:
        - created_at
        - description
        - id
        - idp_sync_enabled
        - name
        - organization_id
        - updated_at
      properties:
        created_at:
          type: string
        description:
          type: string
        id:
          type: string
          format: uuid
        idp_group_name:
          type: string
        idp_sync_enabled:
          type: boolean
        name:
          type: string
        organization_id:
          type: string
          format: uuid
        parent_team_id:
          description: >-
            ParentTeamID is the organization-wide team a workspace team belongs
            to.

            It is omitted for organization-wide teams.
          type: string
          format: uuid
        role_id:
          description: >-
            RoleID is the role an organization scoped team is granted in the
            workspace given by the

            workspace_id filter. It is omitted otherwise.
          type: string
          format: uuid
        role_name:
          description: RoleName is the display name of RoleID.
          type: string
        updated_at:
          type: string
        workspace_id:
          description: |-
            WorkspaceID is the workspace the team belongs to. It is omitted for
            organization-wide teams.
          type: string
          format: uuid
    shared.ParseErrorDetails:
      description: Structured fields describing an adapter parse failure.
      type: object
      required:
        - adapter
        - item_type
      properties:
        adapter:
          type: string
        item_type:
          type: string
        run_id:
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

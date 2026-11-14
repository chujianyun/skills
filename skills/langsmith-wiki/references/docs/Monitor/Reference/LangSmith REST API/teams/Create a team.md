# Create a team

> Creates an organization-wide team. Needs organization:teams:manage. Workspace scoped
teams are not created here: granting an organization-wide team access to a
workspace creates its workspace scoped team there, so workspace_id and
parent_team_id return 400.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json post /api/v1/platform/orgs/current/teams
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
    post:
      tags:
        - teams
      summary: Create a team
      description: >-
        Creates an organization-wide team. Needs organization:teams:manage.
        Workspace scoped

        teams are not created here: granting an organization-wide team access to
        a

        workspace creates its workspace scoped team there, so workspace_id and

        parent_team_id return 400.
      parameters: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/teams.CreateTeamPayload'
      responses:
        '201':
          description: Created
          headers:
            Location:
              description: URL of the new team
              schema:
                type: string
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/teams.Team'
        '400':
          description: invalid request, or workspace_id or parent_team_id is set
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/shared.ProblemDetails'
        '403':
          description: caller lacks organization:teams:manage
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/shared.ProblemDetails'
        '409':
          description: a team with this name already exists
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
    teams.CreateTeamPayload:
      type: object
      required:
        - name
      properties:
        description:
          type: string
        name:
          type: string
          maxLength: 255
          minLength: 1
        parent_team_id:
          type: string
          format: uuid
        workspace_id:
          description: >-
            Rejected with 400, so a request for a workspace team does not create
            an

            organization-wide team. Granting a team a workspace creates its
            workspace team.
          type: string
          format: uuid
    teams.Team:
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
        updated_at:
          type: string
        workspace_id:
          description: |-
            WorkspaceID is the workspace the team belongs to. It is omitted for
            organization-wide teams.
          type: string
          format: uuid
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

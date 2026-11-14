# List org tracing keys

> List your tracing keys and keys visible through organization/workspace access.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json get /api/v1/orgs/current/tracing-keys
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
  /api/v1/orgs/current/tracing-keys:
    get:
      tags:
        - orgs
      summary: List org tracing keys
      description: >-
        List your tracing keys and keys visible through organization/workspace
        access.
      operationId: list_org_tracing_keys_api_v1_orgs_current_tracing_keys_get
      parameters:
        - name: workspace_ids
          in: query
          required: false
          schema:
            items:
              type: string
              format: uuid
            type: array
            title: Workspace Ids
            default: []
        - name: page_size
          in: query
          required: false
          schema:
            type: integer
            maximum: 100
            minimum: 1
            default: 50
            title: Page Size
        - name: cursor
          in: query
          required: false
          schema:
            anyOf:
              - type: string
                maxLength: 1024
              - type: 'null'
            title: Cursor
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TracingKeyListResponse'
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
    TracingKeyListResponse:
      properties:
        items:
          items:
            $ref: '#/components/schemas/APIKeyGetResponse'
          type: array
          title: Items
        next_cursor:
          anyOf:
            - type: string
            - type: 'null'
          title: Next Cursor
      type: object
      required:
        - items
        - next_cursor
      title: TracingKeyListResponse
    HTTPValidationError:
      properties:
        detail:
          items:
            type: string
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    APIKeyGetResponse:
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
      type: object
      required:
        - id
        - short_key
        - description
      title: APIKeyGetResponse
      description: |-
        API key GET schema.

        role_id, org_role_id, and access_scope let clients render the key's
        current role state without a second round trip. For workspace-scoped
        service keys, org_role_id comes from the parent organization identity.
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

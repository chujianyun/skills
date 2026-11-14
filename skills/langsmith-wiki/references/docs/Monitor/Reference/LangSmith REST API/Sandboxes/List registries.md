# List registries

> List sandbox registries for pulling private images.
Page with page_size and cursor, replaying next_cursor until it is null. Results are ordered newest first, with stable ordering for equal creation times. Keep filters unchanged between pages.
Requests without page_size or cursor retain the legacy default of 50 results. Cursor requests default to 20 results, with a maximum of 100.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json get /api/v2/sandboxes/registries
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
  /api/v2/sandboxes/registries:
    get:
      tags:
        - sandboxes
      summary: List registries
      description: >-
        List sandbox registries for pulling private images.

        Page with page_size and cursor, replaying next_cursor until it is null.
        Results are ordered newest first, with stable ordering for equal
        creation times. Keep filters unchanged between pages.

        Requests without page_size or cursor retain the legacy default of 50
        results. Cursor requests default to 20 results, with a maximum of 100.
      parameters:
        - description: Number of results per cursor page
          name: page_size
          in: query
          schema:
            type: integer
            maximum: 100
            minimum: 1
            title: Page Size
            default: 20
        - description: Opaque cursor from a prior response's next_cursor
          name: cursor
          in: query
          schema:
            type: string
            title: Cursor
        - description: 'Deprecated: use page_size. Maximum number of registries to return'
          name: limit
          in: query
          schema:
            type: integer
            title: Limit
        - description: 'Deprecated: use cursor. Number of registries to skip'
          name: offset
          in: query
          schema:
            type: integer
            title: Offset
        - description: Filter to registries whose name contains this substring
          name: name_contains
          in: query
          schema:
            type: string
            title: Name Contains
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/sandboxes.RegistryListResponse'
        '400':
          description: invalid cursor pagination or mixed pagination parameters
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/sandboxes.ErrorResponse'
        '403':
          description: Forbidden
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/sandboxes.ErrorResponse'
        '422':
          description: out-of-range legacy limit or offset
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/sandboxes.ValidationErrors'
        '500':
          description: Internal Server Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/sandboxes.ErrorResponse'
      security:
        - API Key: []
        - Tenant ID: []
        - Bearer Auth: []
components:
  schemas:
    sandboxes.RegistryListResponse:
      type: object
      properties:
        items:
          type: array
          items:
            $ref: '#/components/schemas/sandboxes.RegistryResponse'
        next_cursor:
          anyOf:
            - type: string
            - type: 'null'
        offset:
          description: >-
            Deprecated: only applies to limit/offset requests. Use next_cursor
            when paging with a cursor.
          type: integer
        registries:
          description: 'Deprecated: use items.'
          type: array
          items:
            $ref: '#/components/schemas/sandboxes.RegistryResponse'
    sandboxes.ErrorResponse:
      type: object
      properties:
        detail:
          type: object
          properties:
            error:
              type: string
            error_id:
              type: string
            message:
              type: string
    sandboxes.ValidationErrors:
      type: object
      properties:
        detail:
          type: array
          items:
            $ref: '#/components/schemas/sandboxes.ValidationErrorDetail'
    sandboxes.RegistryResponse:
      type: object
      properties:
        auth_type:
          type: string
          enum:
            - DOCKER_CONFIG
            - AWS_ROLE
        aws_role_arn:
          type: string
        created_at:
          type: string
        created_by:
          type: string
        id:
          type: string
        name:
          type: string
        provider:
          type: string
          enum:
            - DOCKER_REGISTRY
            - HARBOR
            - GHCR
            - ECR
            - GAR
            - DOCKER_HUB
        repository_search_mode:
          type: string
          enum:
            - GLOBAL
            - SCOPED
            - NONE
        updated_at:
          type: string
        updated_by:
          type: string
        url:
          type: string
    sandboxes.ValidationErrorDetail:
      type: object
      properties:
        loc:
          items:
            type: string
          type: array
        msg:
          type: string
        type:
          type: string
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

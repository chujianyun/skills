# List a sandbox's shared service urls

> Returns one entry per port the sandbox is currently reachable on, so a caller can see what is shared before turning it off. Expired token grants are omitted.
Cursors are opaque and only valid on this endpoint; do not parse or construct one.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json get /api/v2/sandboxes/boxes/{name}/service-urls
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
  /api/v2/sandboxes/boxes/{name}/service-urls:
    get:
      tags:
        - sandboxes
      summary: List a sandbox's shared service urls
      description: >-
        Returns one entry per port the sandbox is currently reachable on, so a
        caller can see what is shared before turning it off. Expired token
        grants are omitted.

        Cursors are opaque and only valid on this endpoint; do not parse or
        construct one.
      parameters:
        - description: Sandbox name or ID
          name: name
          in: path
          required: true
          schema:
            type: string
        - description: Number of results per page
          name: page_size
          in: query
          schema:
            type: integer
            default: 20
            title: Page Size
        - description: Opaque pagination cursor from a prior response's next_cursor
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
                $ref: '#/components/schemas/sandboxes.ServiceURLGrantListResponse'
        '400':
          description: invalid page_size or cursor
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/shared.ProblemDetails'
        '401':
          description: missing or invalid authentication
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/shared.ProblemDetails'
        '403':
          description: forbidden (insufficient permission)
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/shared.ProblemDetails'
        '404':
          description: sandbox not found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/shared.ProblemDetails'
        '500':
          description: internal server error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/shared.ProblemDetails'
      security:
        - API Key: []
          Tenant ID: []
        - Bearer Auth: []
          Tenant ID: []
components:
  schemas:
    sandboxes.ServiceURLGrantListResponse:
      type: object
      required:
        - items
        - next_cursor
      properties:
        items:
          description: This page of the ports the sandbox is shared on.
          type: array
          items:
            $ref: '#/components/schemas/sandboxes.ServiceURLGrantResponse'
        next_cursor:
          description: >-
            Cursor for the next page, or null on the last page. A non-null value
            is

            the only signal that more pages exist. Treat it as opaque.
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
    sandboxes.ServiceURLGrantResponse:
      type: object
      required:
        - access
        - created_at
        - port
      properties:
        access:
          description: |-
            How the port is shared: "token" for a minted service token, or
            "restricted"/"workspace" for LangSmith login.
          type: string
          enum:
            - token
            - restricted
            - workspace
        created_at:
          type: string
          format: date-time
        created_by:
          description: The LangSmith user who first shared this port, when known.
          type: string
          format: uuid
        embed_origins:
          description: >-
            Origins that may embed a LangSmith login URL in an iframe; omitted
            when there are none.
          type: array
          items:
            type: string
        expires_at:
          description: >-
            When the share expires. Set only for "token"; a login grant does not
            expire.
          type: string
          format: date-time
        port:
          type: integer
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

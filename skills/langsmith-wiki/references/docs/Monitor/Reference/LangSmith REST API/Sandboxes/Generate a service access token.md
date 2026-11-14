# Generate a service access token

> Create a short-lived JWT for accessing an HTTP service running on a specific port inside a sandbox. Returns a browser_url (sets auth cookie via redirect), an embed_url (for an iframe; carries the token in the URL fragment, so no server or Referer sees it), a service_url (for use with the X-Langsmith-Sandbox-Service-Token header), the raw token, and its expiry. Set access=restricted|workspace to instead enable durable LangSmith login (no token; users authenticate with their normal LangSmith session), or access=off to disable it. embed_origins names the pages that may show the URL in an iframe. In token mode they are bound into the minted token; with LangSmith login they are stored on the grant and a viewer signs in from inside the frame through a LangSmith popup. LangSmith login and token access are mutually exclusive per service URL.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json post /api/v2/sandboxes/boxes/{name}/service-url
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
  /api/v2/sandboxes/boxes/{name}/service-url:
    post:
      tags:
        - sandboxes
      summary: Generate a service access token
      description: >-
        Create a short-lived JWT for accessing an HTTP service running on a
        specific port inside a sandbox. Returns a browser_url (sets auth cookie
        via redirect), an embed_url (for an iframe; carries the token in the URL
        fragment, so no server or Referer sees it), a service_url (for use with
        the X-Langsmith-Sandbox-Service-Token header), the raw token, and its
        expiry. Set access=restricted|workspace to instead enable durable
        LangSmith login (no token; users authenticate with their normal
        LangSmith session), or access=off to disable it. embed_origins names the
        pages that may show the URL in an iframe. In token mode they are bound
        into the minted token; with LangSmith login they are stored on the grant
        and a viewer signs in from inside the frame through a LangSmith popup.
        LangSmith login and token access are mutually exclusive per service URL.
      parameters:
        - description: Sandbox display name
          name: name
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/sandboxes.ServiceURLPayload'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/sandboxes.ServiceURLResponse'
        '400':
          description: Bad Request
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/sandboxes.ErrorResponse'
        '404':
          description: Not Found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/sandboxes.ErrorResponse'
        '409':
          description: Conflict
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/sandboxes.ErrorResponse'
        '422':
          description: Unprocessable Entity
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/sandboxes.ErrorResponse'
        '500':
          description: Internal Server Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/sandboxes.ErrorResponse'
        '501':
          description: Not Implemented
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
    sandboxes.ServiceURLPayload:
      type: object
      properties:
        access:
          description: >-
            Access selects the login mode, mutually exclusive with the minted
            token.

            Omit the field for token mode: mint a short-lived service token
            (default).
              "restricted" — LangSmith login: the sandbox's creator, or any user with SandboxesExec on it (admins by default).
              "workspace"  — LangSmith login: any member of the owning workspace.
              "off"        — remove an existing LangSmith login grant and mint a token.
            A LangSmith login grant is durable; token mode is refused (409)
            while one exists.
          type: string
          enum:
            - restricted
            - workspace
            - 'off'
        embed_origins:
          description: >-
            EmbedOrigins are the pages allowed to show the service URL in an
            iframe,

            besides LangSmith itself: at most 5 origins such as

            https://app.example.com (http only for localhost). In token mode
            they are

            bound into the minted token, so they last as long as it does. With

            access "restricted" or "workspace" each call sets the grant's whole
            list,

            so omitting the field removes any origins set before.
          type: array
          items:
            type: string
        expires_in_seconds:
          type: integer
        port:
          type: integer
    sandboxes.ServiceURLResponse:
      type: object
      properties:
        access:
          description: >-
            Access echoes the enabled LangSmith login level
            ("restricted"/"workspace"); omitted in token mode.
          type: string
          enum:
            - restricted
            - workspace
        browser_url:
          type: string
        embed_origins:
          description: >-
            EmbedOrigins echoes the origins that may embed the URL, normalized;
            omitted when there are none.
          type: array
          items:
            type: string
        embed_url:
          description: >-
            EmbedURL opens the service in an iframe: the token rides the URL

            fragment, which no server, log or Referer header sees, and the page
            it

            loads trades it for the cookie. Append &redirect=/path to land

            elsewhere than /. Omitted in LangSmith login mode.
          type: string
        expires_at:
          type: string
        service_url:
          type: string
        token:
          description: >-
            Token and ExpiresAt are empty in LangSmith login mode (no token is
            minted).
          type: string
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

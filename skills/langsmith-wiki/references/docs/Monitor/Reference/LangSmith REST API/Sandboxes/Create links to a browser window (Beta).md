# Create links to a browser window (Beta)

> Beta: mint a view link and an act link for one window, as every attachment response does, with a chosen lifetime and the origins allowed to embed the window's pages in an iframe. Without embed_origins no page may frame them. view_embed_url and act_embed_url carry the same tokens in the URL fragment, for an iframe, so no server sees them. An embedded page sends its parent window messages when control changes and when it connects or disconnects (see the browser guide). Either link opens the window to anyone who holds it until it expires; detaching the window ends it early. A stopped browser starts when links are minted and when a link is opened, and resumes with its windows. Minting takes being the browser's creator or a role with sandboxes:exec.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json post /api/v2/sandboxes/browsers/{name}/attachments/{attachment_id}/links
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
  /api/v2/sandboxes/browsers/{name}/attachments/{attachment_id}/links:
    post:
      tags:
        - sandboxes
      summary: Create links to a browser window (Beta)
      description: >-
        Beta: mint a view link and an act link for one window, as every
        attachment response does, with a chosen lifetime and the origins allowed
        to embed the window's pages in an iframe. Without embed_origins no page
        may frame them. view_embed_url and act_embed_url carry the same tokens
        in the URL fragment, for an iframe, so no server sees them. An embedded
        page sends its parent window messages when control changes and when it
        connects or disconnects (see the browser guide). Either link opens the
        window to anyone who holds it until it expires; detaching the window
        ends it early. A stopped browser starts when links are minted and when a
        link is opened, and resumes with its windows. Minting takes being the
        browser's creator or a role with sandboxes:exec.
      parameters:
        - description: Browser name or ID
          name: name
          in: path
          required: true
          schema:
            type: string
        - description: Attachment ID
          name: attachment_id
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: false
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/sandboxes.CreateBrowserWindowLinksPayload'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/sandboxes.BrowserWindowLinks'
        '400':
          description: >-
            An embed origin is not an https origin, or ttl_seconds is out of
            range
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/sandboxes.ErrorResponse'
        '403':
          description: The caller neither created the browser nor has sandboxes:exec
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/sandboxes.ErrorResponse'
        '404':
          description: Browser or attachment not found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/sandboxes.ErrorResponse'
        '501':
          description: The browser beta is not enabled, or window links are not available
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
    sandboxes.CreateBrowserWindowLinksPayload:
      type: object
      properties:
        embed_origins:
          description: >-
            EmbedOrigins are the origins whose pages may show the window's pages
            in

            an iframe, such as https://app.example.com: https, or http on

            localhost, with no path. Without them no page may frame the window.
          type: array
          maxItems: 5
          items:
            type: string
        ttl_seconds:
          description: |-
            TTLSeconds is how long the links work, from 60 seconds to 24 hours.
            Defaults to 24 hours.
          type: integer
          maximum: 86400
          minimum: 60
    sandboxes.BrowserWindowLinks:
      type: object
      properties:
        act_embed_url:
          type: string
        act_url:
          description: |-
            ActURL also lets the person take control of the window, use it, and
            hand it back.
          type: string
        expires_at:
          type: string
          format: date-time
        view_embed_url:
          description: >-
            ViewEmbedURL and ActEmbedURL open the same window in an iframe with
            the

            token in the URL fragment, which no server, log or Referer header
            sees.

            Viewer options follow the token in the fragment, as in

            {act_embed_url}&fit=follow&zoom=1.
          type: string
        view_url:
          description: ViewURL shows the window and takes no input.
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

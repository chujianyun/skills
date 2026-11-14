# Resize a browser window (Beta)

> Beta: size a window so its page is width by height CSS pixels. The window keeps that size until resized again, through this call or over CDP with Browser.setWindowBounds; the live view scales to fit it rather than resizing it. A browser that is not running cannot be resized.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json patch /api/v2/sandboxes/browsers/{name}/attachments/{attachment_id}
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
  /api/v2/sandboxes/browsers/{name}/attachments/{attachment_id}:
    patch:
      tags:
        - sandboxes
      summary: Resize a browser window (Beta)
      description: >-
        Beta: size a window so its page is width by height CSS pixels. The
        window keeps that size until resized again, through this call or over
        CDP with Browser.setWindowBounds; the live view scales to fit it rather
        than resizing it. A browser that is not running cannot be resized.
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
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/sandboxes.UpdateBrowserAttachmentPayload'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/sandboxes.BrowserAttachment'
        '400':
          description: Size out of range
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
        '409':
          description: The browser is not running
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/sandboxes.ErrorResponse'
        '501':
          description: The browser beta is not enabled
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
    sandboxes.UpdateBrowserAttachmentPayload:
      type: object
      properties:
        height:
          type: integer
          maximum: 2400
          minimum: 300
        width:
          description: Width and Height are the window's new page size in CSS pixels.
          type: integer
          maximum: 3840
          minimum: 400
    sandboxes.BrowserAttachment:
      type: object
      properties:
        act_url:
          type: string
        api_cdp_url:
          description: >-
            APICDPURL is the same Chrome DevTools endpoint through the LangSmith
            API,

            for clients outside any sandbox. It takes any API credential:
            headers as

            for any API call (X-Api-Key, or Authorization: Bearer with an OAuth

            access token, plus X-Tenant-Id where needed), or, for clients that
            take

            only a URL, api_key, token and tenant_id query parameters.
          type: string
        cdp_url:
          description: >-
            CDPURL is the Chrome DevTools endpoint the attached sandbox connects
            to,

            for example with Playwright's connect_over_cdp. It works only from
            inside

            that sandbox.
          type: string
        clients:
          description: >-
            Clients are the sandboxes currently connected to this window, with
            "api"

            for each client connected through api_cdp_url. An unrestricted
            window's

            connections are not listed.
          type: array
          items:
            type: string
        controller:
          description: >-
            Controller is "agent" while the attached sandbox drives the window
            and

            "user" while a person has taken it over.
          type: string
          enum:
            - agent
            - user
        created_at:
          type: string
        height:
          type: integer
        id:
          type: string
        links_expire_at:
          type: string
          format: date-time
        localhost_alias:
          description: >-
            LocalhostAlias is the sandbox's localhost as the browser sees it:
            open

            http://<localhost_alias>:<port> in a window to reach a server
            listening

            on that port in the sandbox, whether bound to localhost or to all

            interfaces (any port but 80 and 443). While this is the only sandbox

            sharing its localhost, http://localhost:<port> works too. Pages on
            other

            sites can navigate to a plain-HTTP server there but cannot fetch
            from it.

            Set only for windows attached with share_localhost.
          type: string
        name:
          type: string
        reason:
          description: Reason is why the agent asked a person to take over, when it did.
          type: string
        sandbox:
          description: Sandbox is the attached sandbox; empty for a window a person opened.
          type: string
        tabs:
          type: array
          items:
            $ref: '#/components/schemas/sandboxes.BrowserTab'
        unrestricted:
          description: >-
            Unrestricted windows give their sandbox the whole browser over CDP,
            with

            nothing filtered: every window and tab, every site's cookies, and

            commands that close or crash the browser. Taking over such a window
            does

            not pause its sandbox, and the LSBrowserControl domain is not
            available.
          type: boolean
        view_url:
          description: >-
            ViewURL and ActURL open the window on the sandbox service domain
            with no

            LangSmith login, for an agent to send to a person: ViewURL to watch
            it,

            ActURL also to use it while its controller is "user". Anyone holding
            a

            link can open the window until LinksExpireAt. Each response mints
            new

            ones; they are returned only to those who may use the browser.
          type: string
        width:
          description: >-
            Width and Height are the window's page size in CSS pixels, when it
            was

            given one; a window without one keeps Chrome's default of 1280x800.
          type: integer
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
    sandboxes.BrowserTab:
      type: object
      properties:
        id:
          type: string
        title:
          type: string
        url:
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

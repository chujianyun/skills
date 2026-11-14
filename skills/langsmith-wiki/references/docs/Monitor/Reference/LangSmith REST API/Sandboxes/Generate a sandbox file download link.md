# Generate a sandbox file download link

> Generate a tokenized link that downloads a single file from a sandbox with no further authentication. This mints a token rather than creating an addressable resource, so it returns 200 with no Location header. The token pins the sandbox, the file path, the response content type and disposition, and the sandbox flags, so a link cannot be repointed at another file or served under a weaker policy. The file is always served with a Content-Security-Policy: a sandbox directive, plus a default-src holding every fetch to the file's own download host and a set of pre-approved third-party origins. csp_sandbox_flags may loosen the sandbox with allow-downloads, allow-forms, allow-modals, allow-orientation-lock, allow-pointer-lock, allow-popups, allow-presentation, allow-same-origin, allow-scripts, or allow-top-navigation-by-user-activation. Every file is served from its own host, derived from the sandbox and the path, so allow-same-origin gives a page localStorage and IndexedDB that no other file can read, and re-minting a link for the same file keeps them. csp_sandbox set to false drops the sandbox directive altogether, and csp_sandbox_flags must then be omitted. csp_source_bundles selects the third-party origins: cdnjs, google-fonts, jsdelivr, and unpkg are all allowed when the field is omitted, 'none' holds the file to its own host, and 'any' sends no default-src at all. Links never expire unless expires_in_seconds is set. The link is served from the sandbox service domain, not the API host.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json post /api/v2/sandboxes/boxes/{name}/download-url
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
  /api/v2/sandboxes/boxes/{name}/download-url:
    post:
      tags:
        - sandboxes
      summary: Generate a sandbox file download link
      description: >-
        Generate a tokenized link that downloads a single file from a sandbox
        with no further authentication. This mints a token rather than creating
        an addressable resource, so it returns 200 with no Location header. The
        token pins the sandbox, the file path, the response content type and
        disposition, and the sandbox flags, so a link cannot be repointed at
        another file or served under a weaker policy. The file is always served
        with a Content-Security-Policy: a sandbox directive, plus a default-src
        holding every fetch to the file's own download host and a set of
        pre-approved third-party origins. csp_sandbox_flags may loosen the
        sandbox with allow-downloads, allow-forms, allow-modals,
        allow-orientation-lock, allow-pointer-lock, allow-popups,
        allow-presentation, allow-same-origin, allow-scripts, or
        allow-top-navigation-by-user-activation. Every file is served from its
        own host, derived from the sandbox and the path, so allow-same-origin
        gives a page localStorage and IndexedDB that no other file can read, and
        re-minting a link for the same file keeps them. csp_sandbox set to false
        drops the sandbox directive altogether, and csp_sandbox_flags must then
        be omitted. csp_source_bundles selects the third-party origins: cdnjs,
        google-fonts, jsdelivr, and unpkg are all allowed when the field is
        omitted, 'none' holds the file to its own host, and 'any' sends no
        default-src at all. Links never expire unless expires_in_seconds is set.
        The link is served from the sandbox service domain, not the API host.
      parameters:
        - description: Sandbox ID or name
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
              $ref: '#/components/schemas/sandboxes.DownloadURLPayload'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/sandboxes.DownloadURLResponse'
        '400':
          description: Bad Request
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
        '404':
          description: Not Found
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
    sandboxes.DownloadURLPayload:
      type: object
      required:
        - path
      properties:
        content_disposition:
          type: string
        content_type:
          type: string
        csp_sandbox:
          description: >-
            CSPSandbox false serves the file with no CSP sandbox directive; omit
            to keep it.
          type: boolean
        csp_sandbox_flags:
          description: >-
            CSPSandboxFlags loosen the CSP sandbox the file is served under;
            omit for the most restrictive policy.
          type: array
          items:
            type: string
            enum:
              - allow-downloads
              - allow-forms
              - allow-modals
              - allow-orientation-lock
              - allow-pointer-lock
              - allow-popups
              - allow-presentation
              - allow-scripts
              - allow-top-navigation-by-user-activation
              - allow-same-origin
        csp_source_bundles:
          description: >-
            CSPSourceBundles allow the served file to fetch from named
            third-party origins; omit to send no fetch directive.
          type: array
          items:
            type: string
            enum:
              - cdnjs
              - google-fonts
              - jsdelivr
              - unpkg
              - none
              - any
        expires_in_seconds:
          description: ExpiresInSeconds is optional; a link with no expiry never expires.
          type: integer
        path:
          type: string
    sandboxes.DownloadURLResponse:
      type: object
      required:
        - download_url
        - token
      properties:
        download_url:
          type: string
        expires_at:
          description: ExpiresAt is null for a link that never expires.
          anyOf:
            - type: string
            - type: 'null'
        token:
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

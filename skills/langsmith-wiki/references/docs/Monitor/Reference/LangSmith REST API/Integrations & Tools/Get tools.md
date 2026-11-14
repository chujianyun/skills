# Get tools

> Return MCP tools — from cache if fresh, otherwise by fetching from remote.

On cache miss, tries manifest fetch first (fast), then falls back to full
MCP handshake. Caches the result before returning.

Pass force_refresh=true to bypass the cache and always fetch from the
remote server (the result is still cached via upsert for future requests).

``agent_id`` lets deployment/service-key callers name an agent OAuth
subject. ``ls_user_id`` overrides are limited to service identities.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json get /api/v1/mcp/tools
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
  /api/v1/mcp/tools:
    get:
      tags:
        - mcp
      summary: Get tools
      description: >-
        Return MCP tools — from cache if fresh, otherwise by fetching from
        remote.


        On cache miss, tries manifest fetch first (fast), then falls back to
        full

        MCP handshake. Caches the result before returning.


        Pass force_refresh=true to bypass the cache and always fetch from the

        remote server (the result is still cached via upsert for future
        requests).


        ``agent_id`` lets deployment/service-key callers name an agent OAuth

        subject. ``ls_user_id`` overrides are limited to service identities.
      operationId: get_tools_api_v1_mcp_tools_get
      parameters:
        - name: url
          in: query
          required: true
          schema:
            type: string
            title: Url
        - name: oauth_provider_id
          in: query
          required: false
          schema:
            anyOf:
              - type: string
              - type: 'null'
            title: Oauth Provider Id
        - name: ls_user_id
          in: query
          required: false
          schema:
            anyOf:
              - type: string
              - type: 'null'
            title: Ls User Id
        - name: agent_id
          in: query
          required: false
          schema:
            anyOf:
              - type: string
              - type: 'null'
            title: Agent Id
        - name: force_refresh
          in: query
          required: false
          schema:
            type: boolean
            default: false
            title: Force Refresh
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/McpToolsResponse'
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
      security:
        - API Key: []
        - Tenant ID: []
        - Bearer Auth: []
components:
  schemas:
    McpToolsResponse:
      properties:
        tools:
          items:
            additionalProperties: true
            type: object
          type: array
          title: Tools
        cached:
          type: boolean
          title: Cached
        fetched_at:
          anyOf:
            - type: string
              format: date-time
            - type: 'null'
          title: Fetched At
        server_icon_url:
          anyOf:
            - type: string
            - type: 'null'
          title: Server Icon Url
      type: object
      required:
        - tools
        - cached
        - fetched_at
      title: McpToolsResponse
    HTTPValidationError:
      properties:
        detail:
          items:
            type: string
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
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

# List MCP servers for a vendor

> Returns the MCP gateways from the vendor for the workspace's configured org/project.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json get /api/v1/platform/mcp-vendors/{vendor_slug}/mcp-servers
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
  /api/v1/platform/mcp-vendors/{vendor_slug}/mcp-servers:
    get:
      tags:
        - mcp_vendors
      summary: List MCP servers for a vendor
      description: >-
        Returns the MCP gateways from the vendor for the workspace's configured
        org/project.
      parameters:
        - description: Vendor slug (e.g. arcade)
          name: vendor_slug
          in: path
          required: true
          schema:
            type: string
        - description: Max items to return (default 100)
          name: limit
          in: query
          schema:
            type: integer
            title: Limit
        - description: Number of items to skip (default 0)
          name: offset
          in: query
          schema:
            type: integer
            title: Offset
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/mcp_vendors.ListMcpGatewaysResponse'
        '400':
          description: Bad Request
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/mcp_vendors.ErrorResponse'
        '401':
          description: Unauthorized
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/mcp_vendors.ErrorResponse'
        '403':
          description: Forbidden
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/mcp_vendors.ErrorResponse'
        '404':
          description: Not Found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/mcp_vendors.ErrorResponse'
        '502':
          description: Bad Gateway
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/mcp_vendors.ErrorResponse'
      security:
        - API Key: []
        - Tenant ID: []
        - Bearer Auth: []
components:
  schemas:
    mcp_vendors.ListMcpGatewaysResponse:
      type: object
      properties:
        items:
          type: array
          items:
            $ref: '#/components/schemas/mcp_vendors.McpGateway'
        limit:
          type: integer
        offset:
          type: integer
        page_count:
          type: integer
        total_count:
          type: integer
    mcp_vendors.ErrorResponse:
      type: object
      properties:
        detail:
          type: string
        message:
          type: string
    mcp_vendors.McpGateway:
      type: object
      properties:
        auth_type:
          type: string
        binding:
          $ref: '#/components/schemas/mcp_vendors.McpGatewayBinding'
        created_at:
          type: string
        description:
          type: string
        id:
          type: string
        instructions:
          type: string
        name:
          type: string
        slug:
          type: string
        status:
          type: string
        tool_filter:
          $ref: '#/components/schemas/mcp_vendors.McpGatewayToolFilter'
        updated_at:
          type: string
    mcp_vendors.McpGatewayBinding:
      type: object
      properties:
        id:
          type: string
        type:
          type: string
    mcp_vendors.McpGatewayToolFilter:
      type: object
      properties:
        allowed_tools:
          items:
            type: string
          type: array
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

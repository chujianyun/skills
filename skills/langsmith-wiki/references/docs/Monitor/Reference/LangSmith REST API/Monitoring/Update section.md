# Update section

> Update a section.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json patch /api/v1/charts/section/{section_id}
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
  /api/v1/charts/section/{section_id}:
    patch:
      tags:
        - charts
      summary: Update section
      description: Update a section.
      operationId: update_section_api_v1_charts_section__section_id__patch
      parameters:
        - name: section_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
            title: Section Id
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CustomChartsSectionUpdate'
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CustomChartsSectionResponse'
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
    CustomChartsSectionUpdate:
      properties:
        title:
          anyOf:
            - type: string
            - $ref: '#/components/schemas/Missing'
          title: Title
          default:
            __missing__: __missing__
        description:
          anyOf:
            - type: string
            - $ref: '#/components/schemas/Missing'
            - type: 'null'
          title: Description
          default:
            __missing__: __missing__
        index:
          anyOf:
            - type: integer
            - $ref: '#/components/schemas/Missing'
          title: Index
          default:
            __missing__: __missing__
        layout:
          anyOf:
            - $ref: '#/components/schemas/DashboardLayout-Input'
            - $ref: '#/components/schemas/Missing'
            - type: 'null'
          title: Layout
          default:
            __missing__: __missing__
      type: object
      title: CustomChartsSectionUpdate
    CustomChartsSectionResponse:
      properties:
        title:
          type: string
          title: Title
        description:
          anyOf:
            - type: string
            - type: 'null'
          title: Description
        index:
          anyOf:
            - type: integer
            - type: 'null'
          title: Index
        id:
          type: string
          format: uuid
          title: Id
        chart_count:
          anyOf:
            - type: integer
            - type: 'null'
          title: Chart Count
        created_at:
          anyOf:
            - type: string
              format: date-time
            - type: 'null'
          title: Created At
        modified_at:
          anyOf:
            - type: string
              format: date-time
            - type: 'null'
          title: Modified At
      type: object
      required:
        - title
        - id
      title: CustomChartsSectionResponse
    HTTPValidationError:
      properties:
        detail:
          items:
            type: string
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    Missing:
      properties:
        __missing__:
          type: string
          const: __missing__
          title: Missing
      type: object
      required:
        - __missing__
      title: Missing
    DashboardLayout-Input:
      properties:
        version:
          type: integer
          const: 1
          title: Version
        breakpoints:
          $ref: '#/components/schemas/DashboardLayoutBreakpoints-Input'
      type: object
      required:
        - version
        - breakpoints
      title: DashboardLayout
    DashboardLayoutBreakpoints-Input:
      properties:
        sm:
          $ref: '#/components/schemas/DashboardBreakpointLayout-Input'
        md:
          $ref: '#/components/schemas/DashboardBreakpointLayout-Input'
      type: object
      required:
        - sm
        - md
      title: DashboardLayoutBreakpoints
    DashboardBreakpointLayout-Input:
      properties:
        rows:
          items:
            $ref: '#/components/schemas/DashboardLayoutRow'
          type: array
          title: Rows
      type: object
      required:
        - rows
      title: DashboardBreakpointLayout
    DashboardLayoutRow:
      properties:
        height_units:
          type: integer
          title: Height Units
        items:
          items:
            $ref: '#/components/schemas/DashboardLayoutItem'
          type: array
          minItems: 1
          title: Items
      type: object
      required:
        - height_units
        - items
      title: DashboardLayoutRow
    DashboardLayoutItem:
      properties:
        chart_id:
          type: string
          format: uuid
          title: Chart Id
        width_units:
          type: integer
          minimum: 20
          title: Width Units
      type: object
      required:
        - chart_id
        - width_units
      title: DashboardLayoutItem
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

# List model prices

> List the model prices LangSmith uses to compute run costs in this workspace.

Returns both the workspace's custom entries (`tenant_id` set) and the
LangSmith default entries (`tenant_id` null). Default entries can be read
but not updated or deleted; to price a model differently, for example
because of a negotiated rate with an inference provider, create a custom
entry with the same match pattern.

The total number of matching entries is returned in the
`X-Pagination-Total` response header.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json get /api/v1/model-price-map
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
  /api/v1/model-price-map:
    get:
      tags:
        - model-price-map
      summary: List model prices
      description: >-
        List the model prices LangSmith uses to compute run costs in this
        workspace.


        Returns both the workspace's custom entries (`tenant_id` set) and the

        LangSmith default entries (`tenant_id` null). Default entries can be
        read

        but not updated or deleted; to price a model differently, for example

        because of a negotiated rate with an inference provider, create a custom

        entry with the same match pattern.


        The total number of matching entries is returned in the

        `X-Pagination-Total` response header.
      operationId: read_model_price_map_api_v1_model_price_map_get
      parameters:
        - name: offset
          in: query
          required: false
          schema:
            type: integer
            minimum: 0
            description: Number of entries to skip before this page.
            default: 0
            title: Offset
          description: Number of entries to skip before this page.
        - name: limit
          in: query
          required: false
          schema:
            type: integer
            maximum: 100
            minimum: 1
            description: Maximum number of entries to return.
            default: 100
            title: Limit
          description: Maximum number of entries to return.
        - name: q
          in: query
          required: false
          schema:
            anyOf:
              - type: string
                maxLength: 200
              - type: 'null'
            description: >-
              Case-insensitive substring matched against the entry name, match
              pattern, and provider. Hyphens and spaces are treated as
              equivalent.
            title: Q
          description: >-
            Case-insensitive substring matched against the entry name, match
            pattern, and provider. Hyphens and spaces are treated as equivalent.
        - name: provider
          in: query
          required: false
          schema:
            anyOf:
              - type: array
                items:
                  type: string
                  minLength: 1
                maxItems: 20
              - type: 'null'
            description: Only return price maps for these providers (case-insensitive).
            title: Provider
          description: Only return price maps for these providers (case-insensitive).
        - name: sort_by
          in: query
          required: false
          schema:
            anyOf:
              - const: start_time
                type: string
              - type: 'null'
            description: Field to sort on. Defaults to match priority order.
            title: Sort By
          description: Field to sort on. Defaults to match priority order.
        - name: sort_order
          in: query
          required: false
          schema:
            enum:
              - asc
              - desc
            type: string
            description: Sort direction for sort_by. Unset start dates sort last.
            default: desc
            title: Sort Order
          description: Sort direction for sort_by. Unset start dates sort last.
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/ModelPriceMapSchema'
                title: Response Read Model Price Map Api V1 Model Price Map Get
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
    ModelPriceMapSchema:
      properties:
        id:
          type: string
          format: uuid
          title: Id
          description: ID of the entry.
        name:
          type: string
          title: Name
          description: Display name for the entry, usually the model name.
        start_time:
          anyOf:
            - type: string
              format: date-time
            - type: 'null'
          title: Start Time
          description: >-
            Only price runs that started at or after this time. Null applies to
            runs from any time.
        tenant_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Tenant Id
          description: >-
            Workspace that owns the entry. Null for organization entries and for
            LangSmith default entries.
        organization_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Organization Id
          description: >-
            Organization that owns the entry, which every workspace in it prices
            against unless the workspace overrides it. Null otherwise.
        scope:
          type: string
          enum:
            - BUILTIN
            - ORGANIZATION
            - WORKSPACE
          title: Scope
          description: >-
            Which scope owns the entry. Server-assigned from the route that
            created it.
          default: BUILTIN
        match_path:
          items:
            type: string
          type: array
          title: Match Path
          description: >-
            Invocation parameter keys checked, in order, for the model name when
            the run does not report `ls_model_name` metadata.
          default:
            - model
            - model_name
            - model_id
            - model_path
            - endpoint_name
        match_pattern:
          type: string
          title: Match Pattern
          description: >-
            Regular expression matched against the run's model name, for example
            `^gpt-4o-mini$`.
        prompt_cost:
          type: string
          pattern: ^(?!^[-+.]*$)[+-]?0*\d*\.?\d*$
          title: Prompt Cost
          description: Cost in US dollars per input (prompt) token.
        completion_cost:
          type: string
          pattern: ^(?!^[-+.]*$)[+-]?0*\d*\.?\d*$
          title: Completion Cost
          description: Cost in US dollars per output (completion) token.
        prompt_cost_details:
          anyOf:
            - additionalProperties:
                type: string
                pattern: ^(?!^[-+.]*$)[+-]?0*\d*\.?\d*$
              type: object
            - type: 'null'
          title: Prompt Cost Details
          description: >-
            Cost in US dollars per input token for specific token types, keyed
            by the token detail name the run reports, for example `cache_read`.
            Input tokens not covered here are priced at `prompt_cost`.
        completion_cost_details:
          anyOf:
            - additionalProperties:
                type: string
                pattern: ^(?!^[-+.]*$)[+-]?0*\d*\.?\d*$
              type: object
            - type: 'null'
          title: Completion Cost Details
          description: >-
            Cost in US dollars per output token for specific token types, keyed
            by the token detail name the run reports, for example `audio`.
            Output tokens not covered here are priced at `completion_cost`.
        provider:
          anyOf:
            - type: string
            - type: 'null'
          title: Provider
          description: >-
            Only price runs from this provider (the `ls_provider` metadata,
            case-insensitive), for example `openai` or `anthropic`. Null matches
            any provider.
        prompt_tokens_above:
          anyOf:
            - type: integer
              maximum: 9007199254740991
              minimum: 0
            - type: 'null'
          title: Prompt Tokens Above
          description: >-
            Only price requests with more input tokens than this, for
            long-context pricing tiers. Null applies to every request.
      type: object
      required:
        - name
        - match_pattern
        - prompt_cost
        - completion_cost
      title: ModelPriceMapSchema
      description: A model price entry used to compute the cost of LLM runs.
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

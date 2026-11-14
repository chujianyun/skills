# Replace a model price

> Replace every field of a custom model price in this workspace.

The request body is the full entry, not a partial update: omitted
optional fields are reset to their defaults. Only the workspace's own
entries can be updated; LangSmith default entries cannot. Costs already
recorded on existing runs are not recomputed.

Returns 404 if the workspace has no entry with this ID, including
LangSmith default entries. Returns 409 if the change would duplicate
another entry's match conditions.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json put /api/v1/model-price-map/{id}
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
  /api/v1/model-price-map/{id}:
    put:
      tags:
        - model-price-map
      summary: Replace a model price
      description: |-
        Replace every field of a custom model price in this workspace.

        The request body is the full entry, not a partial update: omitted
        optional fields are reset to their defaults. Only the workspace's own
        entries can be updated; LangSmith default entries cannot. Costs already
        recorded on existing runs are not recomputed.

        Returns 404 if the workspace has no entry with this ID, including
        LangSmith default entries. Returns 409 if the change would duplicate
        another entry's match conditions.
      operationId: update_model_price_api_v1_model_price_map__id__put
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
            title: Id
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ModelPriceMapUpdateSchema'
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema: {}
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
    ModelPriceMapUpdateSchema:
      properties:
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
          anyOf:
            - type: number
            - type: string
              pattern: ^(?!^[-+.]*$)[+-]?0*\d*\.?\d*$
          title: Prompt Cost
          description: Cost in US dollars per input (prompt) token.
        completion_cost:
          anyOf:
            - type: number
            - type: string
              pattern: ^(?!^[-+.]*$)[+-]?0*\d*\.?\d*$
          title: Completion Cost
          description: Cost in US dollars per output (completion) token.
        prompt_cost_details:
          anyOf:
            - additionalProperties:
                anyOf:
                  - type: number
                  - type: string
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
                anyOf:
                  - type: number
                  - type: string
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
      title: ModelPriceMapUpdateSchema
      description: The full replacement for a custom model price entry.
      examples:
        - completion_cost: '0.000008'
          match_pattern: ^gpt-4o$
          name: gpt-4o (negotiated rate)
          prompt_cost: '0.000002'
          prompt_cost_details:
            cache_read: '0.000001'
          provider: openai
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

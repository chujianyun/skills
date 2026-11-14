# Update a gateway policy

> Partially updates a gateway policy. Only fields present in
the request body are applied; absent fields are left
unchanged. `policy_type` is immutable — to change a
policy's type, delete it and create a new one.

**config** if supplied must match the policy's type:
- spend-cap:  `{"window": ..., "limit_usd": ...}`
- guard:      `{"version": 1, "detect": {...}, "timeout_seconds": <number>, "timeout_action": "allow"|"block"}`
- rate-limit: `{"version": 1, "limits": [{"metric": "requests"|"tokens", "window": "minute"|"hour", "value": <integer>}]}`
Mismatched shapes are rejected with 400.

**default cascade:** editing a `default_spend_cap` or
`default_rate_limit` updates the config/action/enabled/priority
on every attached child policy so the template stays the source
of truth across rollouts.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json patch /api/v1/platform/gateway-policies/{id}
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
  /api/v1/platform/gateway-policies/{id}:
    patch:
      tags:
        - gateway-policies
      summary: Update a gateway policy
      description: >-
        Partially updates a gateway policy. Only fields present in

        the request body are applied; absent fields are left

        unchanged. `policy_type` is immutable — to change a

        policy's type, delete it and create a new one.


        **config** if supplied must match the policy's type:

        - spend-cap:  `{"window": ..., "limit_usd": ...}`

        - guard:      `{"version": 1, "detect": {...}, "timeout_seconds":
        <number>, "timeout_action": "allow"|"block"}`

        - rate-limit: `{"version": 1, "limits": [{"metric": "requests"|"tokens",
        "window": "minute"|"hour", "value": <integer>}]}`

        Mismatched shapes are rejected with 400.


        **default cascade:** editing a `default_spend_cap` or

        `default_rate_limit` updates the config/action/enabled/priority

        on every attached child policy so the template stays the source

        of truth across rollouts.
      parameters:
        - description: Policy ID
          name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/gateway_policies.UpdateGatewayPolicyRequest'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/gateway_policies.GatewayPolicyRecord'
        '400':
          description: validation error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/gateway_policies.errorResponse'
        '401':
          description: Unauthorized
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/gateway_policies.errorResponse'
        '403':
          description: LLM Gateway not enabled, or caller lacks organization:gateway:manage
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/gateway_policies.errorResponse'
        '404':
          description: policy not found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/gateway_policies.errorResponse'
        '409':
          description: matcher edit collides with another policy in the same family
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/gateway_policies.errorResponse'
        '500':
          description: Internal Server Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/gateway_policies.errorResponse'
      security:
        - API Key: []
        - Bearer Auth: []
      x-codeSamples:
        - label: spend_cap
          lang: json
          source: |-
            {
              "config": {"window": "monthly", "limit_usd": 200},
              "enabled": false
            }
        - label: spend_cap (per-window limits)
          lang: json
          source: |-
            {
              "config": {"version": 2, "limits": [{"window": "daily", "limit_usd": 50}, {"window": "monthly", "limit_usd": 200}]}
            }
        - label: guard
          lang: json
          source: |-
            {
              "config": {"version": 1, "detect": {"pii": true, "secrets": true}, "timeout_seconds": 5},
              "enabled": true
            }
        - label: rate_limit
          lang: json
          source: |-
            {
              "config": {"version": 1, "limits": [{"metric": "requests", "window": "minute", "value": 100}]},
              "enabled": true
            }
components:
  schemas:
    gateway_policies.UpdateGatewayPolicyRequest:
      type: object
      properties:
        action:
          type: string
          example: block
        config:
          type: object
        description:
          type: string
          example: Blocks overspend on the production org
        enabled:
          type: boolean
          example: true
        name:
          type: string
          example: monthly-cap
        priority:
          type: integer
          example: 0
        subject_matchers:
          type: array
          items:
            $ref: '#/components/schemas/gateway_policies.SubjectMatcher'
    gateway_policies.GatewayPolicyRecord:
      type: object
      properties:
        action:
          type: string
        config:
          type: object
        created_at:
          type: string
        created_by:
          type: string
        current_spend:
          description: |-
            CurrentSpend is the list of spends recorded for each of the
            tracked spend limit windows, used in v2 of spend_cap policy type.
          type: array
          items:
            $ref: '#/components/schemas/gateway_policies.SpendUsage'
        current_spend_usd:
          description: |-
            CurrentSpendUSD is the spend in the policy's current window. Set for
            any spend_cap policy regardless of enabled state — disabled policies
            still surface usage so users can see what would have been counted.
            Nil for non-spend_cap policies or when the spend lookup failed.
          type: number
        current_usage:
          description: >-
            CurrentUsage is the consumed units in each configured limit's
            current

            window. Set for any rate_limit policy regardless of enabled state,
            one

            entry per limit in the config. Nil for non-rate_limit policies or
            when

            the usage lookup failed.
          type: array
          items:
            $ref: '#/components/schemas/gateway_policies.RateLimitUsage'
        description:
          type: string
        enabled:
          type: boolean
        id:
          type: string
        is_system_generated:
          type: boolean
        name:
          type: string
        organization_id:
          type: string
        parent_policy_id:
          description: >-
            ParentPolicyID is set on materialized children of a
            default_spend_cap

            to the default's id. An explicit Update or a Create with the same

            matchers clears the link and takes ownership of the materialized
            row.

            Delete on the parent cascade-soft-deletes children still attached.
          type: string
        policy_type:
          type: string
        priority:
          type: integer
        subject_matchers:
          type: array
          items:
            $ref: '#/components/schemas/gateway_policies.SubjectMatcher'
        updated_at:
          type: string
    gateway_policies.errorResponse:
      type: object
      properties:
        error:
          type: string
    gateway_policies.SubjectMatcher:
      type: object
      properties:
        key:
          type: string
        value:
          type: string
    gateway_policies.SpendUsage:
      type: object
      properties:
        spend_usd:
          description: SpendUSD is the spend recorded in this window.
          type: number
        window:
          description: Window is the spend limit period.
          type: string
    gateway_policies.RateLimitUsage:
      type: object
      properties:
        metric:
          description: 'Metric is the counted usage dimension: requests or tokens.'
          allOf:
            - $ref: '#/components/schemas/gateway_policies.RateLimitMetric'
        value:
          description: Value is the units consumed so far in the current window.
          type: integer
        window:
          description: Window is the time window the usage is measured over.
          allOf:
            - $ref: '#/components/schemas/gateway_policies.RateLimitWindow'
    gateway_policies.RateLimitMetric:
      type: string
      enum:
        - requests
        - tokens
      x-enum-varnames:
        - RateLimitMetricRequests
        - RateLimitMetricTokens
    gateway_policies.RateLimitWindow:
      type: string
      enum:
        - minute
        - hour
      x-enum-varnames:
        - RateLimitWindowMinute
        - RateLimitWindowHour
  securitySchemes:
    API Key:
      type: apiKey
      in: header
      name: X-API-Key
    Bearer Auth:
      type: http
      description: >-
        Bearer tokens are used to authenticate from the UI. Must also specify
        x-tenant-id or x-organization-id (for org scoped apis).
      scheme: bearer

````

# Create a gateway policy

> Creates a gateway policy for the calling organization.

**policy_type** is one of `spend_cap`, `default_spend_cap`,
`guard`, `route_config`, `model_fallback`, `rate_limit`, or `default_rate_limit`.
The shape of `config` depends on policy_type:
- `spend_cap` / `default_spend_cap`, one limit:
`{"window": "hourly"|"daily"|"weekly"|"monthly", "limit_usd": <number>}`
- `spend_cap` / `default_spend_cap`, a limit per window:
`{"version": 2, "limits": [{"window": "hourly"|"daily"|"weekly"|"monthly", "limit_usd": <number>}]}`
- `guard`:
`{"version": 1, "detect": {"pii": <bool>, "secrets": <bool>, "custom": [{"pattern": "<regex>"}]}, "timeout_seconds": <number>, "timeout_action": "allow"|"block"}`
`timeout_seconds` (optional, 0.1–30) caps guard pipeline execution time; defaults to 2s. `timeout_action` defaults to `allow`.
`detect.custom` (optional) holds at most one Go regexp (RE2 syntax) of up to 512 bytes; matching text is redacted. Avoid capture groups: if present, only the first group is redacted, wherever that text appears.
- `route_config`:
`{"strategy": "priority_fallback", "triggers": {"status_codes": [<int>]}, "fallbacks": [{"model_configs": [{"model_config_id": "<playground-settings-uuid>"}]}]}`
`triggers` is required, with no default: `status_codes` must be a non-empty list (include 502 and 504 for upstream transport failures). `fallbacks` contains an entry whose `model_configs` are tried in priority order (1–5). `subject_matchers` must be a single `workspace_id` entry.
- `model_fallback`:
`{"strategy": "priority_fallback", "triggers": {"status_codes": [429, 502, 503, 504]}, "chain": {"selector": {"type": "provider_model", "provider": "openai", "model": "gpt-4o"}, "candidates": [{"type": "provider_model", "provider": "openai", "model": "gpt-4o-mini"}, {"type": "model_config", "model_config_id": "<playground-settings-uuid>"}]}}`
Optional `ejection: {"failure_threshold": <1-1000>, "cooldown_seconds": <1-300>}` skips a candidate for `cooldown_seconds` after it fails the chain's triggers `failure_threshold` times within `cooldown_seconds`. Failures are counted per policy and candidate, only provider failures count, and success does not reset the count. The last candidate is never skipped.
`chain.candidates` is an ordered list of 1–5 direct provider models or saved workspace model configurations. A non-empty `workspace_id` matcher is required. `provider_model` selectors are workspace-only; `alias` selectors may be narrowed by `user_id` or `api_key_id`. Provider/model selectors are unique within a workspace, while alias names are reserved across the organization and may intentionally shadow a model name.
- `rate_limit` / `default_rate_limit`:
`{"version": 1, "limits": [{"metric": "requests"|"tokens", "window": "minute"|"hour", "value": <integer>}]}`
`limits` must be non-empty; each `metric`/`window` pair may appear at most once. `value` is 1..1000000000000000.

**subject_matchers** is a list of `{key, value}` pairs. Built-in
keys are `organization_id`, `workspace_id`, `agent_id`,
`agent_environment`, `user_id`, `api_key_id`, and `run_rule_id`.
Values under the same key are ORed; distinct keys are ANDed.
`agent_id` and `agent_environment` target requests from Agent
deployments and must be combined with exactly one `workspace_id`
matcher: `agent_id` alone targets those Agents, `agent_environment`
(`LOCAL`, `DEVELOPMENT`, `STAGING`, or `PRODUCTION`) alone targets
every Agent in those environments, and both together target those
Agents in those environments. Agent keys are
not supported in default policies. A default policy uses an empty built-in matcher value so
the runtime materializes a child for each subject it sees. A
`default_spend_cap` and `default_rate_limit` may add one empty custom
metadata key to bucket each subject by the corresponding
`X-Gateway-*` request header; the materialized child stores both values.

**action** is currently always `block`. Spend caps reject the
request with 402 when the limit is hit; rate limits reject with
429 (with a `Retry-After` hint) when a limit is exceeded; guard
policies redact matched content in-place before forwarding upstream.

**Upsert by matchers:** for `spend_cap`, `default_spend_cap`,
`rate_limit`, `default_rate_limit`, and `guard`, if a policy with
the same `subject_matchers` already exists in this organization,
the existing policy is updated in place instead of a duplicate
being created. `id` is preserved. `route_config` and `model_fallback` do not upsert
by matchers — name must be unique per organization (409 on
conflict). Returns 201 either way.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json post /api/v1/platform/gateway-policies
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
  /api/v1/platform/gateway-policies:
    post:
      tags:
        - gateway-policies
      summary: Create a gateway policy
      description: >-
        Creates a gateway policy for the calling organization.


        **policy_type** is one of `spend_cap`, `default_spend_cap`,

        `guard`, `route_config`, `model_fallback`, `rate_limit`, or
        `default_rate_limit`.

        The shape of `config` depends on policy_type:

        - `spend_cap` / `default_spend_cap`, one limit:

        `{"window": "hourly"|"daily"|"weekly"|"monthly", "limit_usd": <number>}`

        - `spend_cap` / `default_spend_cap`, a limit per window:

        `{"version": 2, "limits": [{"window":
        "hourly"|"daily"|"weekly"|"monthly", "limit_usd": <number>}]}`

        - `guard`:

        `{"version": 1, "detect": {"pii": <bool>, "secrets": <bool>, "custom":
        [{"pattern": "<regex>"}]}, "timeout_seconds": <number>,
        "timeout_action": "allow"|"block"}`

        `timeout_seconds` (optional, 0.1–30) caps guard pipeline execution time;
        defaults to 2s. `timeout_action` defaults to `allow`.

        `detect.custom` (optional) holds at most one Go regexp (RE2 syntax) of
        up to 512 bytes; matching text is redacted. Avoid capture groups: if
        present, only the first group is redacted, wherever that text appears.

        - `route_config`:

        `{"strategy": "priority_fallback", "triggers": {"status_codes":
        [<int>]}, "fallbacks": [{"model_configs": [{"model_config_id":
        "<playground-settings-uuid>"}]}]}`

        `triggers` is required, with no default: `status_codes` must be a
        non-empty list (include 502 and 504 for upstream transport failures).
        `fallbacks` contains an entry whose `model_configs` are tried in
        priority order (1–5). `subject_matchers` must be a single `workspace_id`
        entry.

        - `model_fallback`:

        `{"strategy": "priority_fallback", "triggers": {"status_codes": [429,
        502, 503, 504]}, "chain": {"selector": {"type": "provider_model",
        "provider": "openai", "model": "gpt-4o"}, "candidates": [{"type":
        "provider_model", "provider": "openai", "model": "gpt-4o-mini"},
        {"type": "model_config", "model_config_id":
        "<playground-settings-uuid>"}]}}`

        Optional `ejection: {"failure_threshold": <1-1000>, "cooldown_seconds":
        <1-300>}` skips a candidate for `cooldown_seconds` after it fails the
        chain's triggers `failure_threshold` times within `cooldown_seconds`.
        Failures are counted per policy and candidate, only provider failures
        count, and success does not reset the count. The last candidate is never
        skipped.

        `chain.candidates` is an ordered list of 1–5 direct provider models or
        saved workspace model configurations. A non-empty `workspace_id` matcher
        is required. `provider_model` selectors are workspace-only; `alias`
        selectors may be narrowed by `user_id` or `api_key_id`. Provider/model
        selectors are unique within a workspace, while alias names are reserved
        across the organization and may intentionally shadow a model name.

        - `rate_limit` / `default_rate_limit`:

        `{"version": 1, "limits": [{"metric": "requests"|"tokens", "window":
        "minute"|"hour", "value": <integer>}]}`

        `limits` must be non-empty; each `metric`/`window` pair may appear at
        most once. `value` is 1..1000000000000000.


        **subject_matchers** is a list of `{key, value}` pairs. Built-in

        keys are `organization_id`, `workspace_id`, `agent_id`,

        `agent_environment`, `user_id`, `api_key_id`, and `run_rule_id`.

        Values under the same key are ORed; distinct keys are ANDed.

        `agent_id` and `agent_environment` target requests from Agent

        deployments and must be combined with exactly one `workspace_id`

        matcher: `agent_id` alone targets those Agents, `agent_environment`

        (`LOCAL`, `DEVELOPMENT`, `STAGING`, or `PRODUCTION`) alone targets

        every Agent in those environments, and both together target those

        Agents in those environments. Agent keys are

        not supported in default policies. A default policy uses an empty
        built-in matcher value so

        the runtime materializes a child for each subject it sees. A

        `default_spend_cap` and `default_rate_limit` may add one empty custom

        metadata key to bucket each subject by the corresponding

        `X-Gateway-*` request header; the materialized child stores both values.


        **action** is currently always `block`. Spend caps reject the

        request with 402 when the limit is hit; rate limits reject with

        429 (with a `Retry-After` hint) when a limit is exceeded; guard

        policies redact matched content in-place before forwarding upstream.


        **Upsert by matchers:** for `spend_cap`, `default_spend_cap`,

        `rate_limit`, `default_rate_limit`, and `guard`, if a policy with

        the same `subject_matchers` already exists in this organization,

        the existing policy is updated in place instead of a duplicate

        being created. `id` is preserved. `route_config` and `model_fallback` do
        not upsert

        by matchers — name must be unique per organization (409 on

        conflict). Returns 201 either way.
      parameters: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/gateway_policies.CreateGatewayPolicyRequest'
      responses:
        '201':
          description: Created
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
          description: missing or invalid auth
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/gateway_policies.errorResponse'
        '403':
          description: >-
            LLM Gateway not enabled for the organization, or caller lacks
            organization:gateway:manage
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/gateway_policies.errorResponse'
        '409':
          description: policy name conflict
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
              "name": "monthly-cap",
              "policy_type": "spend_cap",
              "action": "block",
              "subject_matchers": [{"key":"organization_id","value":"<org-uuid>"}],
              "config": {"window": "monthly", "limit_usd": 100}
            }
        - label: spend_cap (per-window limits)
          lang: json
          source: |-
            {
              "name": "daily-and-monthly-cap",
              "policy_type": "spend_cap",
              "action": "block",
              "subject_matchers": [{"key":"organization_id","value":"<org-uuid>"}],
              "config": {"version": 2, "limits": [{"window": "daily", "limit_usd": 25}, {"window": "monthly", "limit_usd": 100}]}
            }
        - label: guard
          lang: json
          source: |-
            {
              "name": "redact-pii",
              "policy_type": "guard",
              "action": "block",
              "subject_matchers": [{"key":"organization_id","value":"<org-uuid>"}],
              "config": {"version": 1, "detect": {"pii": true, "secrets": true, "custom": [{"pattern": "BLD-[A-Z]{3}-[0-9]{4}"}]}, "timeout_seconds": 3}
            }
        - label: route_config
          lang: json
          source: |-
            {
              "name": "gpt-fallback",
              "policy_type": "route_config",
              "action": "block",
              "subject_matchers": [{"key": "workspace_id", "value": "<workspace-uuid>"}],
              "config": {"strategy": "priority_fallback", "triggers": {"status_codes": [429, 500, 502, 503, 504]}, "fallbacks": [{"model_configs": [{"model_config_id": "11111111-1111-1111-1111-111111111111"}]}]}
            }
components:
  schemas:
    gateway_policies.CreateGatewayPolicyRequest:
      type: object
      properties:
        action:
          type: string
        config:
          type: object
        description:
          type: string
        enabled:
          type: boolean
        name:
          type: string
        policy_type:
          type: string
        priority:
          type: integer
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

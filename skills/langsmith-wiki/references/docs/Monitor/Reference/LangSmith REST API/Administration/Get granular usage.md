# Get granular usage

> Get granular usage data with flexible grouping.

`kind` selects the billable usage domain:
- `traces` (default): trace counts.
- `langsmith_deployments`: LangSmith Deployment metrics (nodes
  executed, agent runs, agent uptime). The three Deployment fields
  are populated and `traces` is `0`.

`trace_tier` (only meaningful for `kind=traces`) optionally restricts
results to a single retention tier (longlived = extended retention,
shortlived = standard retention). When `group_by=trace_tier`, results
are split into one record per retention tier per time bucket.

`workspace_ids` filters results to the specified workspaces. Only
workspaces the user has read access to are included. When omitted, all
workspaces the user can read are included (avoids enumerating every
workspace id in the URL, which can exceed proxy header limits).



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json get /api/v1/orgs/current/billing/granular-usage
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
  /api/v1/orgs/current/billing/granular-usage:
    get:
      tags:
        - orgs
      summary: Get granular usage
      description: |-
        Get granular usage data with flexible grouping.

        `kind` selects the billable usage domain:
        - `traces` (default): trace counts.
        - `langsmith_deployments`: LangSmith Deployment metrics (nodes
          executed, agent runs, agent uptime). The three Deployment fields
          are populated and `traces` is `0`.

        `trace_tier` (only meaningful for `kind=traces`) optionally restricts
        results to a single retention tier (longlived = extended retention,
        shortlived = standard retention). When `group_by=trace_tier`, results
        are split into one record per retention tier per time bucket.

        `workspace_ids` filters results to the specified workspaces. Only
        workspaces the user has read access to are included. When omitted, all
        workspaces the user can read are included (avoids enumerating every
        workspace id in the URL, which can exceed proxy header limits).
      operationId: get_granular_usage_api_v1_orgs_current_billing_granular_usage_get
      parameters:
        - name: start_time
          in: query
          required: true
          schema:
            type: string
            format: date-time
            title: Start Time
        - name: end_time
          in: query
          required: true
          schema:
            type: string
            format: date-time
            title: End Time
        - name: workspace_ids
          in: query
          required: false
          schema:
            anyOf:
              - items:
                  type: string
                  format: uuid
                type: array
              - type: 'null'
            title: Workspace Ids
        - name: group_by
          in: query
          required: false
          schema:
            $ref: '#/components/schemas/GranularUsageGroupBy'
            default: workspace
        - name: kind
          in: query
          required: false
          schema:
            $ref: '#/components/schemas/GranularUsageKind'
            default: traces
        - name: trace_tier
          in: query
          required: false
          schema:
            anyOf:
              - $ref: '#/components/schemas/TraceTier'
              - type: 'null'
            title: Trace Tier
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/GranularUsageResponse'
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
      security:
        - API Key: []
        - Organization ID: []
        - Bearer Auth: []
components:
  schemas:
    GranularUsageGroupBy:
      type: string
      enum:
        - user
        - api_key
        - project
        - workspace
        - trace_tier
      title: GranularUsageGroupBy
      description: Dimensions for grouping granular usage data.
    GranularUsageKind:
      type: string
      enum:
        - traces
        - langsmith_deployments
      title: GranularUsageKind
      description: |-
        Which billable usage domain a granular-usage query targets.

        - `traces`: trace counts.
        - `langsmith_deployments`: LangSmith Deployment metrics (nodes executed,
          agent runs, agent uptime).

        Default is `traces` for backward compatibility — existing callers of
        `GET /granular-usage` without a `kind` query param get the same
        response shape they always did.
    TraceTier:
      enum:
        - longlived
        - shortlived
      title: TraceTier
      type: string
    GranularUsageResponse:
      properties:
        stride:
          $ref: '#/components/schemas/GranularUsageStride'
        usage:
          items:
            $ref: '#/components/schemas/GranularUsageRecord'
          type: array
          title: Usage
      type: object
      required:
        - stride
        - usage
      title: GranularUsageResponse
      description: Response for granular usage query.
    HTTPValidationError:
      properties:
        detail:
          items:
            type: string
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    GranularUsageStride:
      properties:
        days:
          type: integer
          title: Days
          default: 0
        hours:
          type: integer
          title: Hours
          default: 0
      type: object
      title: GranularUsageStride
      description: >-
        Stride configuration for time bucketing - only ONE field should be
        non-zero.
    GranularUsageRecord:
      properties:
        time_bucket:
          anyOf:
            - type: string
              format: date-time
            - type: 'null'
          title: Time Bucket
        dimensions:
          $ref: '#/components/schemas/GranularUsageDimensions'
        traces:
          type: integer
          title: Traces
          default: 0
        nodes_executed:
          type: integer
          title: Nodes Executed
          default: 0
        agent_runs:
          type: integer
          title: Agent Runs
          default: 0
        agent_uptime_seconds:
          type: integer
          title: Agent Uptime Seconds
          default: 0
      type: object
      required:
        - dimensions
      title: GranularUsageRecord
      description: |-
        A single granular usage data point.

        Carries both trace and LangSmith Deployment metric fields; the
        `kind` query param on `GET /granular-usage` picks which metric domain
        the row's values come from. Fields for the unselected domain are
        always `0`. Backwards-compat: callers that only read `traces` (the
        pre-existing field) keep working unchanged.
    GranularUsageDimensions:
      properties:
        user_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: User Id
        user_email:
          anyOf:
            - type: string
            - type: 'null'
          title: User Email
        api_key_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Api Key Id
        api_key_short_key:
          anyOf:
            - type: string
            - type: 'null'
          title: Api Key Short Key
        project_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Project Id
        project_name:
          anyOf:
            - type: string
            - type: 'null'
          title: Project Name
        workspace_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Workspace Id
        workspace_name:
          anyOf:
            - type: string
            - type: 'null'
          title: Workspace Name
        trace_tier:
          anyOf:
            - $ref: '#/components/schemas/TraceTier'
            - type: 'null'
      type: object
      title: GranularUsageDimensions
      description: Dimension values for a granular usage record.
  securitySchemes:
    API Key:
      type: apiKey
      in: header
      name: X-API-Key
    Organization ID:
      type: apiKey
      in: header
      name: X-Organization-Id
    Bearer Auth:
      type: http
      description: >-
        Bearer tokens are used to authenticate from the UI. Must also specify
        x-tenant-id or x-organization-id (for org scoped apis).
      scheme: bearer

````

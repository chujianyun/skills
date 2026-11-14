# Get evaluator spend

> Returns per-day LLM evaluator spend for the requested 7-day period, grouped by evaluator, resource, or run rule. Exactly one of group_by, evaluator_id, session_id, or dataset_id is required. resource_id, type, feedback_key, tag_value_id, and agent_id may be supplied with group_by to narrow listing aggregations.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json get /api/v1/platform/evaluators/spend
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
  /api/v1/platform/evaluators/spend:
    get:
      tags:
        - evaluators
      summary: Get evaluator spend
      description: >-
        Returns per-day LLM evaluator spend for the requested 7-day period,
        grouped by evaluator, resource, or run rule. Exactly one of group_by,
        evaluator_id, session_id, or dataset_id is required. resource_id, type,
        feedback_key, tag_value_id, and agent_id may be supplied with group_by
        to narrow listing aggregations.
      parameters:
        - description: >-
            Aggregation mode: 'evaluator', 'resource', or 'run_rule'. Mutually
            exclusive with entity filters.
          name: group_by
          in: query
          schema:
            type: string
            title: Group By
        - description: >-
            Filter to a specific evaluator (UUID). Mutually exclusive with
            group_by.
          name: evaluator_id
          in: query
          schema:
            type: string
            title: Evaluator Id
        - description: >-
            Filter to a specific project (UUID). Mutually exclusive with
            group_by.
          name: session_id
          in: query
          schema:
            type: string
            title: Session Id
        - description: >-
            Filter to a specific dataset (UUID). Mutually exclusive with
            group_by.
          name: dataset_id
          in: query
          schema:
            type: string
            title: Dataset Id
        - description: >-
            Filter grouped results to evaluators attached to all supplied
            project or dataset IDs. Only valid with group_by.
          name: resource_id
          in: query
          style: form
          explode: false
          schema:
            type: array
            items:
              type: string
            title: Resource Id
        - description: >-
            Filter grouped results by evaluator type: 'llm', 'code' or
            'decision_model'. Only valid with group_by.
          name: type
          in: query
          schema:
            type: string
            title: Type
        - description: >-
            Filter grouped results by evaluator feedback key. Only valid with
            group_by.
          name: feedback_key
          in: query
          schema:
            type: string
            title: Feedback Key
        - description: >-
            Filter grouped results to evaluators, projects, or datasets tagged
            with all supplied tag value IDs. Only valid with group_by.
          name: tag_value_id
          in: query
          style: form
          explode: false
          schema:
            type: array
            items:
              type: string
            title: Tag Value Id
        - description: >-
            Filter grouped results to spend from evaluator attachments on the
            agent's environments or tagged datasets. Only valid with group_by.
          name: agent_id
          in: query
          schema:
            type: string
            title: Agent Id
        - description: Start of the 7-day window (YYYY-MM-DD).
          name: period_start
          in: query
          required: true
          schema:
            type: string
            title: Period Start
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/evaluators.GetEvaluatorSpendResponse'
        '400':
          description: Bad Request
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/evaluators.ErrorResponse'
        '401':
          description: Unauthorized
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/evaluators.ErrorResponse'
        '403':
          description: Forbidden
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/evaluators.ErrorResponse'
        '404':
          description: Not Found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/evaluators.ErrorResponse'
        '500':
          description: Internal Server Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/evaluators.ErrorResponse'
      security:
        - API Key: []
        - Tenant ID: []
        - Bearer Auth: []
components:
  schemas:
    evaluators.GetEvaluatorSpendResponse:
      type: object
      properties:
        groups:
          type: array
          items:
            $ref: '#/components/schemas/evaluators.SpendGroup'
        period_end:
          type: string
        period_start:
          type: string
    evaluators.ErrorResponse:
      type: object
      properties:
        error:
          description: Error message
          type: string
    evaluators.SpendGroup:
      type: object
      properties:
        dataset_id:
          type: string
        dataset_name:
          type: string
        days:
          type: array
          items:
            $ref: '#/components/schemas/evaluators.SpendDay'
        evaluator_id:
          type: string
        evaluator_name:
          type: string
        prev_total_spend_usd:
          type: number
        prev_total_trace_count:
          type: integer
        run_rule_id:
          type: string
        run_rule_name:
          type: string
        session_id:
          type: string
        session_name:
          type: string
        spend_limit:
          $ref: '#/components/schemas/evaluators.SpendLimit'
        total_spend_usd:
          type: number
        total_trace_count:
          type: integer
    evaluators.SpendDay:
      type: object
      properties:
        date:
          type: string
        spend_usd:
          type: number
        trace_count:
          type: integer
    evaluators.SpendLimit:
      type: object
      properties:
        limit_usd:
          type: number
        utilization_pct:
          type: number
        window:
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

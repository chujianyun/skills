# Update an alert rule

> Updates an alert rule.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json patch /api/v1/platform/alerts/{session_id}/{alert_rule_id}
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
  /api/v1/platform/alerts/{session_id}/{alert_rule_id}:
    patch:
      tags:
        - alert_rules
      summary: Update an alert rule
      description: Updates an alert rule.
      parameters:
        - description: Session ID
          name: session_id
          in: path
          required: true
          schema:
            type: string
        - description: Alert rule ID
          name: alert_rule_id
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/alerts.UpdateAlertRuleRequest'
      responses:
        '200':
          description: Alert rule updated
          content:
            application/json:
              schema:
                type: object
                additionalProperties:
                  allOf:
                    - type: string
                    - type: object
                      properties:
                        message:
                          type: string
        '400':
          description: Bad request
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/alerts.ErrorResponse'
        '403':
          description: Forbidden
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/alerts.ErrorResponse'
        '404':
          description: Not found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/alerts.ErrorResponse'
        '500':
          description: Internal server error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/alerts.ErrorResponse'
        '503':
          description: Service unavailable
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/alerts.ErrorResponse'
      security:
        - API Key: []
        - Tenant ID: []
        - Bearer Auth: []
components:
  schemas:
    alerts.UpdateAlertRuleRequest:
      type: object
      required:
        - actions
        - rule
      properties:
        actions:
          type: array
          minItems: 1
          items:
            $ref: '#/components/schemas/alerts.AlertActionBase'
        rule:
          $ref: '#/components/schemas/alerts.AlertRuleBase'
    alerts.ErrorResponse:
      type: object
      properties:
        error:
          type: string
          example: 'Invalid request: missing required fields'
    alerts.AlertActionBase:
      type: object
      required:
        - config
        - target
      properties:
        alert_rule_id:
          type: string
        config:
          type: object
        id:
          type: string
        target:
          type: string
          enum:
            - pagerduty
            - webhook
            - dynatrace
            - slack
    alerts.AlertRuleBase:
      type: object
      required:
        - aggregation
        - attribute
        - description
        - name
        - operator
        - type
        - window_minutes
      properties:
        aggregation:
          type: string
          enum:
            - avg
            - sum
            - pct
        attribute:
          type: string
          enum:
            - latency
            - error_count
            - feedback_score
            - run_latency
            - run_count
            - total_cost
        denominator_filter:
          type: string
        description:
          type: string
        filter:
          type: string
        id:
          type: string
        name:
          type: string
        operator:
          type: string
          enum:
            - gte
            - lte
            - gt
            - lt
        threshold:
          type: number
        threshold_multiplier:
          type: number
        threshold_window_minutes:
          type: integer
          maximum: 60
        type:
          type: string
          enum:
            - threshold
            - change
        window_minutes:
          description: 1-60 minutes for alert rule
          type: integer
          maximum: 60
          minimum: 1
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

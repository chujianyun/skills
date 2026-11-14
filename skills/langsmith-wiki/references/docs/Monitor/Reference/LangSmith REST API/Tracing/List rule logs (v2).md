# List rule logs (v2)

> List logs for a particular rule with cursor-based pagination.

This endpoint handles S3-stored outcomes correctly by using run_outcomes_count
to predict batch sizes and avoid over-fetching.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json get /api/v1/runs/rules/{rule_id}/logs/v2
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
  /api/v1/runs/rules/{rule_id}/logs/v2:
    get:
      tags:
        - run
      summary: List rule logs (v2)
      description: >-
        List logs for a particular rule with cursor-based pagination.


        This endpoint handles S3-stored outcomes correctly by using
        run_outcomes_count

        to predict batch sizes and avoid over-fetching.
      operationId: list_rule_logs_v2_api_v1_runs_rules__rule_id__logs_v2_get
      parameters:
        - name: rule_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
            title: Rule Id
        - name: limit
          in: query
          required: false
          schema:
            type: integer
            maximum: 1440
            minimum: 1
            default: 150
            title: Limit
        - name: cursor
          in: query
          required: false
          schema:
            anyOf:
              - type: string
              - type: 'null'
            title: Cursor
        - name: backfill
          in: query
          required: false
          schema:
            type: boolean
            default: false
            title: Backfill
        - name: start_time
          in: query
          required: false
          schema:
            anyOf:
              - type: string
                format: date-time
              - type: 'null'
            title: Start Time
        - name: end_time
          in: query
          required: false
          schema:
            anyOf:
              - type: string
                format: date-time
              - type: 'null'
            title: End Time
        - name: session_id
          in: query
          required: false
          schema:
            anyOf:
              - type: string
                format: uuid
              - type: 'null'
            title: Session Id
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/RuleLogsPaginatedResponse'
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
    RuleLogsPaginatedResponse:
      properties:
        logs:
          items:
            $ref: '#/components/schemas/RuleLogSchema'
          type: array
          title: Logs
        cursor:
          anyOf:
            - type: string
            - type: 'null'
          title: Cursor
      type: object
      required:
        - logs
      title: RuleLogsPaginatedResponse
      description: Paginated response for rule logs with cursor-based pagination.
    HTTPValidationError:
      properties:
        detail:
          items:
            type: string
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    RuleLogSchema:
      properties:
        rule_id:
          type: string
          format: uuid
          title: Rule Id
        run_id:
          type: string
          format: uuid
          title: Run Id
        run_name:
          anyOf:
            - type: string
            - type: 'null'
          title: Run Name
        run_type:
          anyOf:
            - type: string
            - type: 'null'
          title: Run Type
        run_session_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Run Session Id
        run_trace_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Run Trace Id
        start_time:
          type: string
          format: date-time
          title: Start Time
        end_time:
          type: string
          format: date-time
          title: End Time
        application_time:
          anyOf:
            - type: string
              format: date-time
            - type: 'null'
          title: Application Time
        add_to_annotation_queue:
          anyOf:
            - $ref: '#/components/schemas/RuleLogActionResponse'
            - type: 'null'
        add_to_dataset:
          anyOf:
            - $ref: '#/components/schemas/RuleLogActionResponse'
            - type: 'null'
        evaluators:
          anyOf:
            - $ref: '#/components/schemas/RuleLogActionResponse'
            - type: 'null'
        alerts:
          anyOf:
            - $ref: '#/components/schemas/RuleLogActionResponse'
            - type: 'null'
        webhooks:
          anyOf:
            - $ref: '#/components/schemas/RuleLogActionResponse'
            - type: 'null'
        extend_only:
          anyOf:
            - $ref: '#/components/schemas/RuleLogActionResponse'
            - type: 'null'
        thread_id:
          anyOf:
            - type: string
            - type: 'null'
          title: Thread Id
      type: object
      required:
        - rule_id
        - run_id
        - start_time
        - end_time
      title: RuleLogSchema
      description: Run rules log schema.
    RuleLogActionResponse:
      properties:
        outcome:
          $ref: '#/components/schemas/RuleLogActionOutcome'
        payload:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Payload
      type: object
      required:
        - outcome
      title: RuleLogActionResponse
    RuleLogActionOutcome:
      type: string
      enum:
        - success
        - skipped
        - error
      title: RuleLogActionOutcome
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

# List rules

> List all run rules.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json get /api/v1/runs/rules
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
  /api/v1/runs/rules:
    get:
      tags:
        - run
      summary: List rules
      description: List all run rules.
      operationId: list_rules_api_v1_runs_rules_get
      parameters:
        - name: dataset_id
          in: query
          required: false
          schema:
            anyOf:
              - type: string
                format: uuid
              - type: 'null'
            title: Dataset Id
        - name: session_id
          in: query
          required: false
          schema:
            anyOf:
              - type: string
                format: uuid
              - type: 'null'
            title: Session Id
        - name: type
          in: query
          required: false
          schema:
            anyOf:
              - enum:
                  - session
                  - dataset
                type: string
              - type: 'null'
            title: Type
        - name: name_contains
          in: query
          required: false
          schema:
            anyOf:
              - type: string
              - type: 'null'
            title: Name Contains
        - name: id
          in: query
          required: false
          schema:
            anyOf:
              - items:
                  type: string
                  format: uuid
                type: array
              - type: 'null'
            title: Id
        - name: evaluator_id
          in: query
          required: false
          schema:
            anyOf:
              - type: string
                format: uuid
              - type: 'null'
            title: Evaluator Id
        - name: tag_value_id
          in: query
          required: false
          schema:
            anyOf:
              - items:
                  type: string
                  format: uuid
                type: array
              - type: 'null'
            title: Tag Value Id
        - name: include_backfill_progress
          in: query
          required: false
          schema:
            type: boolean
            default: false
            title: Include Backfill Progress
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/RunRulesSchema'
                title: Response List Rules Api V1 Runs Rules Get
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
    RunRulesSchema:
      properties:
        id:
          type: string
          format: uuid
          title: Id
        tenant_id:
          type: string
          format: uuid
          title: Tenant Id
        is_enabled:
          type: boolean
          title: Is Enabled
          default: true
        session_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Session Id
        session_name:
          anyOf:
            - type: string
            - type: 'null'
          title: Session Name
        dataset_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Dataset Id
        dataset_name:
          anyOf:
            - type: string
            - type: 'null'
          title: Dataset Name
        display_name:
          type: string
          title: Display Name
        sampling_rate:
          type: number
          title: Sampling Rate
        filter:
          anyOf:
            - type: string
            - type: 'null'
          title: Filter
        trace_filter:
          anyOf:
            - type: string
            - type: 'null'
          title: Trace Filter
        tree_filter:
          anyOf:
            - type: string
            - type: 'null'
          title: Tree Filter
        add_to_annotation_queue_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Add To Annotation Queue Id
        add_to_annotation_queue_name:
          anyOf:
            - type: string
            - type: 'null'
          title: Add To Annotation Queue Name
        add_to_dataset_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Add To Dataset Id
        add_to_dataset_name:
          anyOf:
            - type: string
            - type: 'null'
          title: Add To Dataset Name
        add_to_dataset_prefer_correction:
          type: boolean
          title: Add To Dataset Prefer Correction
          default: false
        corrections_dataset_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Corrections Dataset Id
        use_corrections_dataset:
          type: boolean
          title: Use Corrections Dataset
          default: false
        num_few_shot_examples:
          anyOf:
            - type: integer
            - type: 'null'
          title: Num Few Shot Examples
        evaluators:
          anyOf:
            - items:
                $ref: '#/components/schemas/EvaluatorTopLevel'
              type: array
            - type: 'null'
          title: Evaluators
        code_evaluators:
          anyOf:
            - items:
                $ref: '#/components/schemas/CodeEvaluatorTopLevel'
              type: array
            - type: 'null'
          title: Code Evaluators
        alerts:
          anyOf:
            - items:
                $ref: '#/components/schemas/RunRulesPagerdutyAlertSchema'
              type: array
            - type: 'null'
          title: Alerts
        webhooks:
          anyOf:
            - items:
                $ref: '#/components/schemas/RunRulesWebhookSchema'
              type: array
            - type: 'null'
          title: Webhooks
        extend_only:
          type: boolean
          title: Extend Only
          default: false
        is_managed_evaluator:
          type: boolean
          title: Is Managed Evaluator
          default: false
        is_tracing_disabled:
          type: boolean
          title: Is Tracing Disabled
          default: false
        extend_evaluator_trace_retention:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Extend Evaluator Trace Retention
        extend_dataset_trace_retention:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Extend Dataset Trace Retention
        extend_annotation_queue_trace_retention:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Extend Annotation Queue Trace Retention
        extend_webhook_trace_retention:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Extend Webhook Trace Retention
        include_extended_stats:
          type: boolean
          title: Include Extended Stats
          default: false
        created_at:
          type: string
          format: date-time
          title: Created At
        updated_at:
          type: string
          format: date-time
          title: Updated At
        backfill_from:
          anyOf:
            - type: string
              format: date-time
            - type: 'null'
          title: Backfill From
        backfill_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Backfill Id
        backfill_status:
          anyOf:
            - type: string
            - type: 'null'
          title: Backfill Status
        backfill_progress:
          anyOf:
            - type: number
            - type: 'null'
          title: Backfill Progress
        backfill_error:
          anyOf:
            - type: string
            - type: 'null'
          title: Backfill Error
        backfill_completed_at:
          anyOf:
            - type: string
              format: date-time
            - type: 'null'
          title: Backfill Completed At
        transient:
          type: boolean
          title: Transient
          default: false
        evaluator_version:
          type: integer
          title: Evaluator Version
        evaluator_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Evaluator Id
        evaluator_name:
          anyOf:
            - type: string
            - type: 'null'
          title: Evaluator Name
        evaluator_type:
          anyOf:
            - type: string
            - type: 'null'
          title: Evaluator Type
        alignment_annotation_queue_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Alignment Annotation Queue Id
        group_by:
          anyOf:
            - type: string
              enum:
                - thread_id
                - trajectory_id
            - type: 'null'
          title: Group By
        spend_limit:
          anyOf:
            - $ref: '#/components/schemas/RunRuleSpendLimitSchema-Output'
            - type: 'null'
        effective_spend_limit:
          anyOf:
            - $ref: '#/components/schemas/RunRuleSpendLimitSchema-Output'
            - type: 'null'
          description: >-
            spend_limit if set; otherwise the organization's default evaluator
            spend limit, once the rule has made its first evaluator call.
        trace_count:
          anyOf:
            - type: integer
            - type: 'null'
          title: Trace Count
        spend_usd:
          anyOf:
            - type: number
            - type: 'null'
          title: Spend Usd
      type: object
      required:
        - id
        - tenant_id
        - display_name
        - sampling_rate
        - webhooks
        - created_at
        - updated_at
        - evaluator_version
      title: RunRulesSchema
      description: Run rules schema.
    HTTPValidationError:
      properties:
        detail:
          items:
            type: string
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    EvaluatorTopLevel:
      properties:
        structured:
          $ref: '#/components/schemas/EvaluatorStructuredOutput'
      type: object
      required:
        - structured
      title: EvaluatorTopLevel
    CodeEvaluatorTopLevel:
      properties:
        code:
          type: string
          title: Code
        language:
          anyOf:
            - $ref: '#/components/schemas/CodeEvaluatorLanguage'
            - type: 'null'
          default: python
        require_attachments:
          type: boolean
          title: Require Attachments
          default: false
        code_evaluator_input:
          anyOf:
            - $ref: '#/components/schemas/CodeEvaluatorInputType'
            - type: 'null'
        advanced_features_enabled:
          type: boolean
          title: Advanced Features Enabled
      type: object
      required:
        - code
      title: CodeEvaluatorTopLevel
    RunRulesPagerdutyAlertSchema:
      properties:
        type:
          anyOf:
            - $ref: '#/components/schemas/RunRulesAlertType'
            - type: 'null'
          default: pagerduty
        routing_key:
          type: string
          title: Routing Key
        summary:
          anyOf:
            - type: string
            - type: 'null'
          title: Summary
        severity:
          anyOf:
            - $ref: '#/components/schemas/PagerdutySeverity'
            - type: 'null'
          default: warning
      type: object
      required:
        - routing_key
      title: RunRulesPagerdutyAlertSchema
    RunRulesWebhookSchema:
      properties:
        url:
          type: string
          title: Url
        headers:
          anyOf:
            - type: object
              additionalProperties:
                type: string
            - type: 'null'
          title: Headers
      type: object
      required:
        - url
      title: RunRulesWebhookSchema
    RunRuleSpendLimitSchema-Output:
      properties:
        limit_usd:
          type: string
          pattern: ^(?!^[-+.]*$)[+-]?0*\d*\.?\d*$
          title: Limit Usd
        window:
          $ref: '#/components/schemas/RunRuleSpendLimitWindow'
      type: object
      required:
        - limit_usd
        - window
      title: RunRuleSpendLimitSchema
    EvaluatorStructuredOutput:
      properties:
        hub_ref:
          anyOf:
            - type: string
            - type: 'null'
          title: Hub Ref
        prompt:
          anyOf:
            - items:
                prefixItems:
                  - type: string
                  - type: string
                type: array
                maxItems: 2
                minItems: 2
              type: array
            - type: 'null'
          title: Prompt
        template_format:
          anyOf:
            - type: string
            - type: 'null'
          title: Template Format
        schema:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Schema
        variable_mapping:
          anyOf:
            - type: object
              additionalProperties:
                type: string
            - type: 'null'
          title: Variable Mapping
        model:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Model
        playground_settings_id:
          anyOf:
            - type: string
            - type: 'null'
          title: Model Configuration ID
      type: object
      title: EvaluatorStructuredOutput
      description: Evaluator structured output schema.
    CodeEvaluatorLanguage:
      type: string
      enum:
        - python
        - javascript
      title: CodeEvaluatorLanguage
    CodeEvaluatorInputType:
      type: string
      enum:
        - thread
        - all_messages
        - human_ai_pairs
        - first_human_last_ai
        - trajectory
      title: CodeEvaluatorInputType
      description: Input provided to a code evaluator.
    RunRulesAlertType:
      type: string
      enum:
        - pagerduty
      title: RunRulesAlertType
      description: Enum for alert types.
    PagerdutySeverity:
      type: string
      enum:
        - critical
        - warning
        - error
        - info
      title: PagerdutySeverity
      description: Enum for severity.
    RunRuleSpendLimitWindow:
      type: string
      enum:
        - weekly
      title: RunRuleSpendLimitWindow
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

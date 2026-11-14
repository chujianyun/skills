# Validate rule

> Validate a rule by executing it with test data without creating a saved rule.

This endpoint allows testing LLM-as-judge evaluators before saving them. It accepts
a rule configuration (same as rule creation) and test data, executes the evaluator,
and returns the evaluation results in the same format as batch_invoke_evaluator.

Only LLM-as-judge rules (evaluators) are supported. Code evaluators are not allowed.

The evaluator execution traces are written to the database (in the "evaluators"
project), which allows users to see the evaluator execution history.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json post /api/v1/runs/rules/validate
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
  /api/v1/runs/rules/validate:
    post:
      tags:
        - run
      summary: Validate rule
      description: >-
        Validate a rule by executing it with test data without creating a saved
        rule.


        This endpoint allows testing LLM-as-judge evaluators before saving them.
        It accepts

        a rule configuration (same as rule creation) and test data, executes the
        evaluator,

        and returns the evaluation results in the same format as
        batch_invoke_evaluator.


        Only LLM-as-judge rules (evaluators) are supported. Code evaluators are
        not allowed.


        The evaluator execution traces are written to the database (in the
        "evaluators"

        project), which allows users to see the evaluator execution history.
      operationId: validate_rule_api_v1_runs_rules_validate_post
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/RunRulesValidateSchema'
        required: true
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                items:
                  additionalProperties: true
                  type: object
                type: array
                title: Response Validate Rule Api V1 Runs Rules Validate Post
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
    RunRulesValidateSchema:
      properties:
        display_name:
          type: string
          title: Display Name
        session_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Session Id
        is_enabled:
          type: boolean
          title: Is Enabled
          default: true
        dataset_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Dataset Id
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
        backfill_from:
          anyOf:
            - type: string
              format: date-time
            - type: 'null'
          title: Backfill From
        use_corrections_dataset:
          type: boolean
          title: Use Corrections Dataset
          default: false
        num_few_shot_examples:
          anyOf:
            - type: integer
            - type: 'null'
          title: Num Few Shot Examples
        extend_only:
          type: boolean
          title: Extend Only
          default: false
        is_tracing_disabled:
          type: boolean
          title: Is Tracing Disabled
          default: true
        extend_evaluator_trace_retention:
          type: boolean
          title: Extend Evaluator Trace Retention
          default: false
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
        transient:
          type: boolean
          title: Transient
          default: false
        add_to_annotation_queue_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Add To Annotation Queue Id
        add_to_dataset_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Add To Dataset Id
        add_to_dataset_prefer_correction:
          type: boolean
          title: Add To Dataset Prefer Correction
          default: false
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
        evaluator_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Evaluator Id
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
        evaluator_version:
          anyOf:
            - type: integer
            - type: 'null'
          title: Evaluator Version
        create_alignment_queue:
          type: boolean
          title: Create Alignment Queue
          default: false
        include_extended_stats:
          type: boolean
          title: Include Extended Stats
          default: false
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
            - $ref: '#/components/schemas/RunRuleSpendLimitSchema-Input'
            - type: 'null'
        tracer_session_issue_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Tracer Session Issue Id
        test_inputs:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Test Inputs
        test_outputs:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Test Outputs
        test_reference_outputs:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Test Reference Outputs
        test_attachments:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Test Attachments
        test_thread_id:
          anyOf:
            - type: string
            - type: 'null'
          title: Test Thread Id
        validate_project_compatibility:
          type: boolean
          title: Validate Project Compatibility
          default: false
      type: object
      required:
        - display_name
        - sampling_rate
      title: RunRulesValidateSchema
      description: >-
        Schema for validating rules without creating them.


        Extends RunRulesCreateSchema with test data fields for validation.

        Only LLM-as-judge rules (evaluators) are supported, not code_evaluators.


        For trace-level evaluators, provide test_inputs / test_outputs.

        For thread evaluators (group_by="thread_id"), provide test_thread_id +

        session_id instead; the backend fetches and assembles all turns
        automatically.
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
    RunRuleSpendLimitSchema-Input:
      properties:
        limit_usd:
          anyOf:
            - type: number
              exclusiveMinimum: 0
            - type: string
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

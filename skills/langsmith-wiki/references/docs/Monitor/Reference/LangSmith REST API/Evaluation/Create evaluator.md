# Create evaluator

> Create a new LLM or code evaluator for the current workspace.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json post /api/v1/platform/evaluators
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
  /api/v1/platform/evaluators:
    post:
      tags:
        - evaluators
      summary: Create evaluator
      description: Create a new LLM or code evaluator for the current workspace.
      parameters: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/evaluators.CreateEvaluatorRequest'
      responses:
        '201':
          description: Created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/evaluators.CreateEvaluatorResponse'
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
    evaluators.CreateEvaluatorRequest:
      type: object
      properties:
        code_evaluator:
          $ref: '#/components/schemas/evaluators.CreateCodeEvaluatorRequest'
        llm_evaluator:
          $ref: '#/components/schemas/evaluators.CreateLLMEvaluatorRequest'
        name:
          type: string
        type:
          $ref: '#/components/schemas/evaluators.EvaluatorType'
    evaluators.CreateEvaluatorResponse:
      type: object
      properties:
        evaluator:
          $ref: '#/components/schemas/evaluators.Evaluator'
    evaluators.ErrorResponse:
      type: object
      properties:
        error:
          description: Error message
          type: string
    evaluators.CreateCodeEvaluatorRequest:
      type: object
      properties:
        advanced_features_enabled:
          type: boolean
        code:
          type: string
        code_evaluator_input:
          description: |-
            CodeEvaluatorInput is which thread data the evaluator receives.
            Null or omitted for run evaluators.
          anyOf:
            - allOf:
                - $ref: '#/components/schemas/evaluators.CodeEvaluatorInput'
            - type: 'null'
        dependencies:
          anyOf:
            - type: string
            - type: 'null'
        language:
          description: 'Default: "python"'
          type: string
        managed_code_evaluator_key:
          $ref: '#/components/schemas/evaluators.ManagedCodeEvaluatorKey'
        managed_code_evaluator_settings:
          $ref: '#/components/schemas/evaluators.ManagedCodeEvaluatorSettings'
        require_attachments:
          description: |-
            RequireAttachments opts the evaluator into selecting/presigning run
            attachments (s3_urls) at evaluation time. Default false.
          type: boolean
        workspace_secrets_keys:
          description: >-
            WorkspaceSecretsKeys names the workspace secrets this evaluator may
            use.

            Each is sent as a header on requests to the hosts allowed for that

            secret; evaluator code never sees the value. Requires

            advanced_features_enabled, and each secret needs an allowed host
            with a

            header.
          type: array
          items:
            type: string
    evaluators.CreateLLMEvaluatorRequest:
      type: object
      properties:
        commit_hash_or_tag:
          type: string
        playground_settings_id:
          description: Model Configuration ID
          type: string
        prompt_repo_handle:
          type: string
        variable_mapping:
          type: object
    evaluators.EvaluatorType:
      type: string
      enum:
        - llm
        - code
        - decision_model
      x-enum-varnames:
        - EvaluatorTypeLLM
        - EvaluatorTypeCode
        - EvaluatorTypeDecisionModel
    evaluators.Evaluator:
      type: object
      properties:
        code_evaluator:
          $ref: '#/components/schemas/evaluators.CodeEvaluator'
        created_at:
          type: string
        created_by:
          type: string
        feedback_keys:
          items:
            type: string
          type: array
        id:
          type: string
        is_managed:
          description: >-
            IsManaged marks a LangChain Tuned Evaluator (currently the tuned

            Perceived Error judge). NULL in the DB is read as false via
            COALESCE.
          type: boolean
        llm_evaluator:
          description: Embedded child evaluator (populated based on type)
          allOf:
            - $ref: '#/components/schemas/evaluators.LLMEvaluator'
        name:
          type: string
        run_rules:
          type: array
          items:
            $ref: '#/components/schemas/evaluators.EvaluatorRunRule'
        tenant_id:
          type: string
        type:
          $ref: '#/components/schemas/evaluators.EvaluatorType'
        updated_at:
          type: string
    evaluators.CodeEvaluatorInput:
      type: string
      enum:
        - thread
        - all_messages
        - human_ai_pairs
        - first_human_last_ai
        - trajectory
      x-enum-varnames:
        - CodeEvaluatorInputThread
        - CodeEvaluatorInputAllMessages
        - CodeEvaluatorInputHumanAIPairs
        - CodeEvaluatorInputFirstHumanLastAI
        - CodeEvaluatorInputTrajectory
    evaluators.ManagedCodeEvaluatorKey:
      type: string
      enum:
        - voice_metrics
      x-enum-varnames:
        - ManagedCodeEvaluatorKeyVoiceMetrics
    evaluators.ManagedCodeEvaluatorSettings:
      type: object
      additionalProperties:
        $ref: '#/components/schemas/evaluators.ManagedCodeEvaluatorMetricSetting'
    evaluators.CodeEvaluator:
      type: object
      properties:
        advanced_features_enabled:
          type: boolean
        code:
          type: string
        code_evaluator_input:
          description: |-
            CodeEvaluatorInput is which thread data the evaluator receives.
            Null for run evaluators.
          anyOf:
            - allOf:
                - $ref: '#/components/schemas/evaluators.CodeEvaluatorInput'
            - type: 'null'
        dependencies:
          type: string
        evaluator_build_error:
          type: string
        evaluator_build_status:
          $ref: '#/components/schemas/evaluators.EvaluatorBuildStatus'
        evaluator_id:
          type: string
        language:
          description: 'Default: "python"'
          type: string
        managed_code_evaluator_key:
          $ref: '#/components/schemas/evaluators.ManagedCodeEvaluatorKey'
        managed_code_evaluator_settings:
          $ref: '#/components/schemas/evaluators.ManagedCodeEvaluatorSettings'
        require_attachments:
          description: |-
            RequireAttachments opts the evaluator into selecting/presigning run
            attachments (s3_urls) at evaluation time. Default false.
          type: boolean
        workspace_secrets_keys:
          description: >-
            WorkspaceSecretsKeys names the workspace secrets this evaluator may
            use.

            Each is sent as a header on requests to the hosts allowed for that

            secret; evaluator code never sees the value. Requires

            advanced_features_enabled, and each secret needs an allowed host
            with a

            header.
          type: array
          items:
            type: string
    evaluators.LLMEvaluator:
      type: object
      properties:
        annotation_queue_id:
          type: string
        commit_hash_or_tag:
          type: string
        corrections_dataset_id:
          type: string
        evaluator_id:
          type: string
        num_few_shot_examples:
          type: integer
        prompt_id:
          type: string
        prompt_repo_handle:
          type: string
        use_corrections_dataset:
          description: >-
            Derived from the evaluator's run rules — shared across all rules on
            this evaluator.

            Nil when the evaluator has no run rules.
          type: boolean
        variable_mapping:
          description: JSONB
          type: object
    evaluators.EvaluatorRunRule:
      type: object
      properties:
        corrections_dataset_id:
          type: string
        dataset_id:
          type: string
        dataset_name:
          type: string
        group_by:
          type: string
        id:
          type: string
        num_few_shot_examples:
          type: integer
        session_id:
          type: string
        session_name:
          type: string
        spend_limit:
          description: >-
            SpendLimit is the effective spend-cap limit for this rule (nil when
            unconfigured).
          allOf:
            - $ref: '#/components/schemas/evaluators.SpendLimit'
        spend_usd:
          description: >-
            Per-rule usage for the current ISO week (omitted when feature is
            disabled).

            LLM-evaluator rules are initialized to 0; code-evaluator rules
            include trace counts only.
          type: number
        trace_count:
          type: integer
        use_corrections_dataset:
          type: boolean
    evaluators.ManagedCodeEvaluatorMetricSetting:
      type: object
      properties:
        is_enabled:
          type: boolean
          default: true
        key_name:
          type: string
    evaluators.EvaluatorBuildStatus:
      type: string
      enum:
        - ENQUEUED
        - BUILDING
        - READY
        - FAILED
      x-enum-varnames:
        - EvaluatorBuildStatusEnqueued
        - EvaluatorBuildStatusBuilding
        - EvaluatorBuildStatusReady
        - EvaluatorBuildStatusFailed
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

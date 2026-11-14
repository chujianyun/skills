# Upload experiment

> Upload an experiment that has already been run.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json post /api/v1/datasets/upload-experiment
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
  /api/v1/datasets/upload-experiment:
    post:
      tags:
        - datasets
      summary: Upload experiment
      description: Upload an experiment that has already been run.
      operationId: upload_experiment_api_v1_datasets_upload_experiment_post
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ExperimentResultsUpload'
        required: true
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ExperimentResultsUploadResult'
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
    ExperimentResultsUpload:
      properties:
        tag_value_ids:
          anyOf:
            - items:
                type: string
                format: uuid
              type: array
              maxItems: 100
            - type: 'null'
          title: Tag Value Ids
        experiment_name:
          type: string
          title: Experiment Name
        experiment_description:
          anyOf:
            - type: string
            - type: 'null'
          title: Experiment Description
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
        dataset_description:
          anyOf:
            - type: string
            - type: 'null'
          title: Dataset Description
        summary_experiment_scores:
          anyOf:
            - items:
                $ref: '#/components/schemas/FeedbackCreateCoreSchema'
              type: array
            - type: 'null'
          title: Summary Experiment Scores
        results:
          items:
            $ref: '#/components/schemas/ExperimentResultRow'
          type: array
          title: Results
        experiment_start_time:
          type: string
          format: date-time
          title: Experiment Start Time
        experiment_end_time:
          type: string
          format: date-time
          title: Experiment End Time
        experiment_metadata:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Experiment Metadata
      type: object
      required:
        - experiment_name
        - results
        - experiment_start_time
        - experiment_end_time
      title: ExperimentResultsUpload
      description: Class for uploading the results of an already-run experiment.
    ExperimentResultsUploadResult:
      properties:
        dataset:
          $ref: '#/components/schemas/Dataset'
        experiment:
          $ref: '#/components/schemas/TracerSession'
      type: object
      required:
        - dataset
        - experiment
      title: ExperimentResultsUploadResult
      description: Class for uploading the results of an already-run experiment.
    HTTPValidationError:
      properties:
        detail:
          items:
            type: string
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    FeedbackCreateCoreSchema:
      properties:
        created_at:
          type: string
          format: date-time
          title: Created At
        modified_at:
          type: string
          format: date-time
          title: Modified At
        key:
          type: string
          maxLength: 180
          title: Key
        score:
          anyOf:
            - type: number
            - type: integer
            - type: boolean
            - type: 'null'
          title: Score
        value:
          anyOf:
            - type: number
            - type: integer
            - type: boolean
            - type: string
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Value
        comment:
          anyOf:
            - type: string
            - type: 'null'
          title: Comment
        correction:
          anyOf:
            - additionalProperties: true
              type: object
            - type: string
            - type: 'null'
          title: Correction
        feedback_group_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Feedback Group Id
        comparative_experiment_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Comparative Experiment Id
        id:
          type: string
          format: uuid
          title: Id
        feedback_source:
          anyOf:
            - oneOf:
                - $ref: '#/components/schemas/AppFeedbackSource'
                - $ref: '#/components/schemas/APIFeedbackSource'
                - $ref: '#/components/schemas/ModelFeedbackSource'
                - $ref: '#/components/schemas/AutoEvalFeedbackSource'
              discriminator:
                propertyName: type
                mapping:
                  api: '#/components/schemas/APIFeedbackSource'
                  app: '#/components/schemas/AppFeedbackSource'
                  auto_eval: '#/components/schemas/AutoEvalFeedbackSource'
                  model: '#/components/schemas/ModelFeedbackSource'
            - type: 'null'
          title: Feedback Source
        feedback_config:
          anyOf:
            - $ref: '#/components/schemas/FeedbackConfig'
            - type: 'null'
        extra:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Extra
      type: object
      required:
        - key
      title: FeedbackCreateCoreSchema
      description: Schema used for creating feedback without run id or session id.
    ExperimentResultRow:
      properties:
        row_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Row Id
        inputs:
          additionalProperties: true
          type: object
          title: Inputs
        expected_outputs:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Expected Outputs
        actual_outputs:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Actual Outputs
        evaluation_scores:
          anyOf:
            - items:
                $ref: '#/components/schemas/FeedbackCreateCoreSchema'
              type: array
            - type: 'null'
          title: Evaluation Scores
        start_time:
          type: string
          format: date-time
          title: Start Time
        end_time:
          type: string
          format: date-time
          title: End Time
        run_name:
          anyOf:
            - type: string
            - type: 'null'
          title: Run Name
        error:
          anyOf:
            - type: string
            - type: 'null'
          title: Error
        run_metadata:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Run Metadata
      type: object
      required:
        - inputs
        - start_time
        - end_time
      title: ExperimentResultRow
      description: Class for a single row in the uploaded experiment results.
    Dataset:
      properties:
        name:
          type: string
          title: Name
        description:
          anyOf:
            - type: string
            - type: 'null'
          title: Description
        created_at:
          type: string
          format: date-time
          title: Created At
        inputs_schema_definition:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Inputs Schema Definition
        outputs_schema_definition:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Outputs Schema Definition
        externally_managed:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Externally Managed
          default: false
        transformations:
          anyOf:
            - items:
                $ref: '#/components/schemas/DatasetTransformation'
              type: array
            - type: 'null'
          title: Transformations
        data_type:
          anyOf:
            - $ref: '#/components/schemas/DataType'
            - type: 'null'
          default: kv
        id:
          type: string
          format: uuid
          title: Id
        tenant_id:
          type: string
          format: uuid
          title: Tenant Id
        example_count:
          anyOf:
            - type: integer
            - type: 'null'
          title: Example Count
        session_count:
          type: integer
          title: Session Count
        modified_at:
          type: string
          format: date-time
          title: Modified At
        last_session_start_time:
          anyOf:
            - type: string
              format: date-time
            - type: 'null'
          title: Last Session Start Time
        metadata:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Metadata
        baseline_experiment_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Baseline Experiment Id
      type: object
      required:
        - name
        - id
        - tenant_id
        - session_count
        - modified_at
      title: Dataset
      description: Dataset schema.
    TracerSession:
      properties:
        start_time:
          type: string
          format: date-time
          title: Start Time
        end_time:
          anyOf:
            - type: string
              format: date-time
            - type: 'null'
          title: End Time
        extra:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Extra
        name:
          type: string
          title: Name
        description:
          anyOf:
            - type: string
            - type: 'null'
          title: Description
        default_dataset_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Default Dataset Id
        reference_dataset_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Reference Dataset Id
        trace_tier:
          anyOf:
            - $ref: '#/components/schemas/TraceTier'
            - type: 'null'
        id:
          type: string
          format: uuid
          title: Id
        run_count:
          anyOf:
            - type: integer
            - type: 'null'
          title: Run Count
        latency_p50:
          anyOf:
            - type: number
            - type: 'null'
          title: Latency P50
        latency_p99:
          anyOf:
            - type: number
            - type: 'null'
          title: Latency P99
        first_token_p50:
          anyOf:
            - type: number
            - type: 'null'
          title: First Token P50
        first_token_p99:
          anyOf:
            - type: number
            - type: 'null'
          title: First Token P99
        total_tokens:
          anyOf:
            - type: integer
            - type: 'null'
          title: Total Tokens
        prompt_tokens:
          anyOf:
            - type: integer
            - type: 'null'
          title: Prompt Tokens
        completion_tokens:
          anyOf:
            - type: integer
            - type: 'null'
          title: Completion Tokens
        total_cost:
          anyOf:
            - type: string
              pattern: ^(?!^[-+.]*$)[+-]?0*\d*\.?\d*$
            - type: 'null'
          title: Total Cost
        prompt_cost:
          anyOf:
            - type: string
              pattern: ^(?!^[-+.]*$)[+-]?0*\d*\.?\d*$
            - type: 'null'
          title: Prompt Cost
        completion_cost:
          anyOf:
            - type: string
              pattern: ^(?!^[-+.]*$)[+-]?0*\d*\.?\d*$
            - type: 'null'
          title: Completion Cost
        tenant_id:
          type: string
          format: uuid
          title: Tenant Id
        last_run_start_time:
          anyOf:
            - type: string
              format: date-time
            - type: 'null'
          title: Last Run Start Time
        last_run_start_time_live:
          anyOf:
            - type: string
              format: date-time
            - type: 'null'
          title: Last Run Start Time Live
        feedback_stats:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Feedback Stats
        session_feedback_stats:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Session Feedback Stats
        run_facets:
          anyOf:
            - items:
                additionalProperties: true
                type: object
              type: array
            - type: 'null'
          title: Run Facets
        error_rate:
          anyOf:
            - type: number
            - type: 'null'
          title: Error Rate
        streaming_rate:
          anyOf:
            - type: number
            - type: 'null'
          title: Streaming Rate
        test_run_number:
          anyOf:
            - type: integer
            - type: 'null'
          title: Test Run Number
        experiment_progress:
          anyOf:
            - $ref: '#/components/schemas/ExperimentProgress'
            - type: 'null'
      type: object
      required:
        - id
        - tenant_id
      title: TracerSession
      description: TracerSession schema.
    AppFeedbackSource:
      properties:
        type:
          type: string
          const: app
          title: Type
          default: app
        metadata:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Metadata
      type: object
      title: AppFeedbackSource
      description: Feedback from the LangChainPlus App.
    APIFeedbackSource:
      properties:
        type:
          type: string
          const: api
          title: Type
          default: api
        metadata:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Metadata
      type: object
      title: APIFeedbackSource
      description: API feedback source.
    ModelFeedbackSource:
      properties:
        type:
          type: string
          const: model
          title: Type
          default: model
        metadata:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Metadata
      type: object
      title: ModelFeedbackSource
      description: Model feedback source.
    AutoEvalFeedbackSource:
      properties:
        type:
          type: string
          const: auto_eval
          title: Type
          default: auto_eval
        metadata:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Metadata
      type: object
      title: AutoEvalFeedbackSource
      description: Auto eval feedback source.
    FeedbackConfig:
      properties:
        type:
          $ref: '#/components/schemas/FeedbackType'
        min:
          anyOf:
            - type: number
            - type: 'null'
          title: Min
        max:
          anyOf:
            - type: number
            - type: 'null'
          title: Max
        categories:
          anyOf:
            - items:
                $ref: '#/components/schemas/FeedbackCategory'
              type: array
            - type: 'null'
          title: Categories
        allows_multiple_categories:
          type: boolean
          title: Allows Multiple Categories
          description: >-
            Whether a reviewer can pick several categories. Categorical feedback
            only.
          default: false
      type: object
      required:
        - type
      title: FeedbackConfig
    DatasetTransformation:
      properties:
        path:
          items:
            type: string
          type: array
          title: Path
        transformation_type:
          $ref: '#/components/schemas/DatasetTransformationType'
      type: object
      required:
        - path
        - transformation_type
      title: DatasetTransformation
    DataType:
      type: string
      enum:
        - kv
        - llm
        - chat
      title: DataType
      description: Enum for dataset data types.
    TraceTier:
      enum:
        - longlived
        - shortlived
      title: TraceTier
      type: string
    ExperimentProgress:
      properties:
        expected_run_count:
          type: integer
          title: Expected Run Count
        run_progress:
          type: number
          title: Run Progress
        evaluator_progress:
          additionalProperties:
            type: number
          type: object
          title: Evaluator Progress
      type: object
      required:
        - expected_run_count
        - run_progress
        - evaluator_progress
      title: ExperimentProgress
    FeedbackType:
      type: string
      enum:
        - continuous
        - categorical
        - freeform
      title: FeedbackType
      description: Enum for feedback types.
    FeedbackCategory:
      properties:
        value:
          type: number
          title: Value
        label:
          anyOf:
            - type: string
              minLength: 1
            - type: 'null'
          title: Label
      type: object
      required:
        - value
      title: FeedbackCategory
      description: Specific value and label pair for feedback
    DatasetTransformationType:
      type: string
      enum:
        - convert_to_openai_message
        - convert_to_openai_tool
        - remove_system_messages
        - remove_extra_fields
        - extract_tools_from_run
      title: DatasetTransformationType
      description: >-
        Enum for dataset transformation types.

        Ordering determines the order in which transformations are applied if
        there are multiple transformations on the same path.
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

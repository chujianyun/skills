# Read examples with runs

> Fetch examples for a dataset, and fetch the runs for each example if they are associated with the given session_ids.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json post /api/v1/datasets/{dataset_id}/runs
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
  /api/v1/datasets/{dataset_id}/runs:
    post:
      tags:
        - datasets
      summary: Read examples with runs
      description: >-
        Fetch examples for a dataset, and fetch the runs for each example if
        they are associated with the given session_ids.
      operationId: read_examples_with_runs_api_v1_datasets__dataset_id__runs_post
      parameters:
        - name: dataset_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
            title: Dataset Id
        - name: format
          in: query
          required: false
          schema:
            anyOf:
              - const: csv
                type: string
              - type: 'null'
            description: Response format, e.g., 'csv'
            title: Format
          description: Response format, e.g., 'csv'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/QueryExampleSchemaWithRunsRequest'
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                anyOf:
                  - type: array
                    items:
                      $ref: '#/components/schemas/ExampleWithRunsCH'
                    title: ExamplesWithRuns
                  - type: 'null'
                title: >-
                  Response Read Examples With Runs Api V1 Datasets  Dataset Id
                  Runs Post
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
      deprecated: true
      security:
        - API Key: []
        - Tenant ID: []
        - Bearer Auth: []
components:
  schemas:
    QueryExampleSchemaWithRunsRequest:
      properties:
        session_ids:
          items:
            type: string
            format: uuid
          type: array
          minItems: 1
          title: Session Ids
        offset:
          type: integer
          minimum: 0
          title: Offset
          default: 0
        limit:
          anyOf:
            - type: integer
              minimum: 1
            - type: 'null'
          title: Limit
        preview:
          type: boolean
          title: Preview
          default: false
        comparative_experiment_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Comparative Experiment Id
        sort_params:
          anyOf:
            - $ref: '#/components/schemas/SortParamsForRunsComparisonView'
            - type: 'null'
        filters:
          anyOf:
            - additionalProperties:
                items:
                  type: string
                type: array
              propertyNames:
                format: uuid
              type: object
            - type: 'null'
          title: Filters
        example_ids:
          anyOf:
            - items:
                type: string
                format: uuid
              type: array
              maxItems: 1000
            - type: 'null'
          title: Example Ids
        include_annotator_detail:
          type: boolean
          title: Include Annotator Detail
          default: false
      type: object
      required:
        - session_ids
      title: QueryExampleSchemaWithRunsRequest
      description: >-
        Request DTO for querying examples with runs - used for API input.


        This is separate from the internal schema to cleanly handle optional
        limit values.

        When limit is None, the internal schema will apply appropriate defaults
        based on

        format.
    ExampleWithRunsCH:
      properties:
        outputs:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Outputs
        dataset_id:
          type: string
          format: uuid
          title: Dataset Id
        source_run_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Source Run Id
        source_session_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Source Session Id
        source_run_start_time:
          anyOf:
            - type: string
              format: date-time
            - type: 'null'
          title: Source Run Start Time
        source_trace_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Source Trace Id
        metadata:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Metadata
        inputs:
          additionalProperties: true
          type: object
          title: Inputs
        created_at:
          type: string
          format: date-time
          title: Created At
        id:
          type: string
          format: uuid
          title: Id
        name:
          type: string
          title: Name
        modified_at:
          anyOf:
            - type: string
              format: date-time
            - type: 'null'
          title: Modified At
        source_thread_id:
          anyOf:
            - type: string
            - type: 'null'
          title: Source Thread Id
        attachment_urls:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Attachment Urls
        runs:
          items:
            $ref: '#/components/schemas/RunSchemaComparisonView'
          type: array
          title: Runs
      type: object
      required:
        - dataset_id
        - inputs
        - id
        - name
        - runs
      title: ExampleWithRunsCH
      description: >-
        Example schema with list of runs from ClickHouse.


        For non-grouped endpoint (/datasets/{dataset_id}/runs): runs from single
        session.

        For grouped endpoint (/datasets/{dataset_id}/group/runs): flat array of
        runs from

        all sessions, where each run has a session_id field for frontend to
        determine column placement.
    HTTPValidationError:
      properties:
        detail:
          items:
            type: string
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    SortParamsForRunsComparisonView:
      properties:
        sort_by:
          type: string
          title: Sort By
        sort_order:
          type: string
          enum:
            - ASC
            - DESC
          title: Sort Order
          default: DESC
      type: object
      required:
        - sort_by
      title: SortParamsForRunsComparisonView
    RunSchemaComparisonView:
      properties:
        name:
          type: string
          title: Name
        inputs:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Inputs
        inputs_preview:
          anyOf:
            - type: string
            - type: 'null'
          title: Inputs Preview
        run_type:
          $ref: '#/components/schemas/RunTypeEnum'
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
        error:
          anyOf:
            - type: string
            - type: 'null'
          title: Error
        execution_order:
          type: integer
          minimum: 1
          title: Execution Order
          default: 1
        serialized:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Serialized
        outputs:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Outputs
        outputs_preview:
          anyOf:
            - type: string
            - type: 'null'
          title: Outputs Preview
        parent_run_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Parent Run Id
        manifest_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Manifest Id
        manifest_s3_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Manifest S3 Id
        events:
          anyOf:
            - items:
                additionalProperties: true
                type: object
              type: array
            - type: 'null'
          title: Events
        tags:
          anyOf:
            - items:
                type: string
              type: array
            - type: 'null'
          title: Tags
        inputs_s3_urls:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Inputs S3 Urls
        outputs_s3_urls:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Outputs S3 Urls
        s3_urls:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: S3 Urls
        trace_id:
          type: string
          format: uuid
          title: Trace Id
        dotted_order:
          anyOf:
            - type: string
            - type: 'null'
          title: Dotted Order
        trace_min_start_time:
          anyOf:
            - type: string
              format: date-time
            - type: 'null'
          title: Trace Min Start Time
        trace_max_start_time:
          anyOf:
            - type: string
              format: date-time
            - type: 'null'
          title: Trace Max Start Time
        id:
          type: string
          format: uuid
          title: Id
        session_id:
          type: string
          format: uuid
          title: Session Id
        reference_example_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Reference Example Id
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
        first_token_time:
          anyOf:
            - type: string
              format: date-time
            - type: 'null'
          title: First Token Time
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
        status:
          type: string
          title: Status
        feedback_stats:
          anyOf:
            - additionalProperties:
                additionalProperties: true
                type: object
              type: object
            - type: 'null'
          title: Feedback Stats
        app_path:
          anyOf:
            - type: string
            - type: 'null'
          title: App Path
      type: object
      required:
        - name
        - run_type
        - trace_id
        - id
        - session_id
        - status
      title: RunSchemaComparisonView
      description: Run schema for comparison view.
    RunTypeEnum:
      type: string
      enum:
        - tool
        - chain
        - llm
        - retriever
        - embedding
        - prompt
        - parser
      title: RunTypeEnum
      description: Enum for run types.
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

# Read dataset

> Get a specific dataset.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json get /api/v1/datasets/{dataset_id}
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
  /api/v1/datasets/{dataset_id}:
    get:
      tags:
        - datasets
      summary: Read dataset
      description: Get a specific dataset.
      operationId: read_dataset_api_v1_datasets__dataset_id__get
      parameters:
        - name: dataset_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
            title: Dataset Id
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Dataset'
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
    HTTPValidationError:
      properties:
        detail:
          items:
            type: string
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
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

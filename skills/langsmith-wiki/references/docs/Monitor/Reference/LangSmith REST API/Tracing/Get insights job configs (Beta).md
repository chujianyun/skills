# Get insights job configs (Beta)

> List Insights job configurations for a project.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json get /api/v1/sessions/{session_id}/insights/configs
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
  /api/v1/sessions/{session_id}/insights/configs:
    get:
      tags:
        - tracer-sessions
      summary: Get insights job configs (Beta)
      description: List Insights job configurations for a project.
      operationId: >-
        _Beta__Get_Insights_Job_Configs_api_v1_sessions__session_id__insights_configs_get
      parameters:
        - name: session_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
            title: Session Id
        - name: include_prebuilts
          in: query
          required: false
          schema:
            type: boolean
            default: false
            title: Include Prebuilts
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/GetClusteringJobConfigsResponse'
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
    GetClusteringJobConfigsResponse:
      properties:
        configs:
          items:
            $ref: '#/components/schemas/ClusteringJobConfigResponse'
          type: array
          title: Configs
      type: object
      required:
        - configs
      title: GetClusteringJobConfigsResponse
      description: A collection of Insights job configurations.
    HTTPValidationError:
      properties:
        detail:
          items:
            type: string
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    ClusteringJobConfigResponse:
      properties:
        id:
          anyOf:
            - type: string
              format: uuid
            - type: string
          title: Id
        name:
          type: string
          title: Name
        description:
          anyOf:
            - type: string
            - type: 'null'
          title: Description
        config:
          $ref: '#/components/schemas/SavedRunClusteringJobRequest'
        prebuilt:
          type: boolean
          title: Prebuilt
        schedule_cron:
          anyOf:
            - type: string
            - type: 'null'
          title: Schedule Cron
      type: object
      required:
        - id
        - name
        - config
        - prebuilt
      title: ClusteringJobConfigResponse
      description: An Insights job configuration.
    SavedRunClusteringJobRequest:
      properties:
        name:
          anyOf:
            - type: string
            - type: 'null'
          title: Name
        last_n_hours:
          anyOf:
            - type: integer
            - type: 'null'
          title: Last N Hours
        start_time:
          anyOf:
            - type: string
            - type: 'null'
          title: Start Time
        end_time:
          anyOf:
            - type: string
            - type: 'null'
          title: End Time
        hierarchy:
          anyOf:
            - items:
                type: integer
              type: array
            - type: 'null'
          title: Hierarchy
        partitions:
          anyOf:
            - type: object
              additionalProperties:
                type: string
            - type: 'null'
          title: Partitions
        sample:
          anyOf:
            - type: number
            - type: integer
            - type: 'null'
          title: Sample
        summary_prompt:
          anyOf:
            - type: string
            - type: 'null'
          title: Summary Prompt
        filter:
          anyOf:
            - type: string
            - type: 'null'
          title: Filter
        attribute_schemas:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Attribute Schemas
        user_context:
          anyOf:
            - type: object
              additionalProperties:
                type: string
            - type: 'null'
          title: User Context
        model:
          type: string
          enum:
            - openai
            - anthropic
          title: Model
        cluster_model:
          anyOf:
            - type: string
            - type: 'null'
          title: Cluster Model
        summary_model:
          anyOf:
            - type: string
            - type: 'null'
          title: Summary Model
      type: object
      required:
        - name
        - hierarchy
        - partitions
        - sample
        - summary_prompt
        - filter
        - attribute_schemas
        - model
      title: SavedRunClusteringJobRequest
      description: Saved configuration for an Insights job.
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

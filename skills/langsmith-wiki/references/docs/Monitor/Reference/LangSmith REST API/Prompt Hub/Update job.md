# Update job

> Replace an existing prompt optimization job with a new, modified job.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json patch /api/v1/repos/{owner}/{repo}/optimization-jobs/{job_id}
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
  /api/v1/repos/{owner}/{repo}/optimization-jobs/{job_id}:
    patch:
      tags:
        - optimization-jobs
      summary: Update job
      description: Replace an existing prompt optimization job with a new, modified job.
      operationId: update_job_api_v1_repos__owner___repo__optimization_jobs__job_id__patch
      parameters:
        - name: job_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
            title: Job Id
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PromptOptimizationJobUpdate'
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PromptOptimizationJob'
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
    PromptOptimizationJobUpdate:
      properties:
        status:
          anyOf:
            - $ref: '#/components/schemas/EPromptOptimizationJobStatus'
            - type: 'null'
        result:
          anyOf:
            - $ref: '#/components/schemas/PromptOptimizationResult'
            - type: 'null'
      type: object
      title: PromptOptimizationJobUpdate
    PromptOptimizationJob:
      properties:
        id:
          type: string
          format: uuid
          title: Id
        repo_id:
          type: string
          format: uuid
          title: Repo Id
        status:
          $ref: '#/components/schemas/EPromptOptimizationJobStatus'
        tenant_id:
          type: string
          format: uuid
          title: Tenant Id
        algorithm:
          $ref: '#/components/schemas/EPromptOptimizationAlgorithm'
        config:
          anyOf:
            - $ref: '#/components/schemas/PromptimConfig'
            - $ref: '#/components/schemas/DemoConfig'
          title: Config
        results:
          items:
            $ref: '#/components/schemas/PromptOptimizationResult'
          type: array
          title: Results
        created_at:
          type: string
          format: date-time
          title: Created At
        updated_at:
          type: string
          format: date-time
          title: Updated At
      type: object
      required:
        - id
        - repo_id
        - status
        - tenant_id
        - algorithm
        - config
        - created_at
        - updated_at
      title: PromptOptimizationJob
    HTTPValidationError:
      properties:
        detail:
          items:
            type: string
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    EPromptOptimizationJobStatus:
      type: string
      enum:
        - created
        - running
        - successful
        - failed
      title: EPromptOptimizationJobStatus
    PromptOptimizationResult:
      properties:
        timestamp:
          type: string
          format: date-time
          title: Timestamp
        x:
          type: number
          title: X
        'y':
          type: number
          title: 'Y'
      type: object
      required:
        - timestamp
        - x
        - 'y'
      title: PromptOptimizationResult
    EPromptOptimizationAlgorithm:
      type: string
      enum:
        - promptim
        - demo
      title: EPromptOptimizationAlgorithm
    PromptimConfig:
      properties:
        message_index:
          type: integer
          title: Message Index
        task_description:
          type: string
          title: Task Description
        dataset_name:
          type: string
          title: Dataset Name
        train_split:
          anyOf:
            - type: string
            - type: 'null'
          title: Train Split
        dev_split:
          anyOf:
            - type: string
            - type: 'null'
          title: Dev Split
        test_split:
          anyOf:
            - type: string
            - type: 'null'
          title: Test Split
        evaluators:
          items:
            type: string
            format: uuid
          type: array
          title: Evaluators
        num_epochs:
          type: integer
          title: Num Epochs
        auto_commit:
          type: boolean
          title: Auto Commit
      type: object
      required:
        - message_index
        - task_description
        - dataset_name
        - train_split
        - dev_split
        - test_split
        - evaluators
        - num_epochs
        - auto_commit
      title: PromptimConfig
    DemoConfig:
      properties:
        message_index:
          type: integer
          title: Message Index
        metaprompt:
          additionalProperties: true
          type: object
          title: Metaprompt
        examples:
          items:
            additionalProperties: true
            type: object
          type: array
          title: Examples
        overall_feedback:
          anyOf:
            - type: string
            - type: 'null'
          title: Overall Feedback
      type: object
      required:
        - message_index
        - metaprompt
        - examples
        - overall_feedback
      title: DemoConfig
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

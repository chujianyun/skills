# Create example

> Create a new example.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json post /api/v1/examples
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
  /api/v1/examples:
    post:
      tags:
        - examples
      summary: Create example
      description: Create a new example.
      operationId: create_example_api_v1_examples_post
      requestBody:
        required: true
        content:
          application/json:
            schema:
              description: Create class for Example.
              properties:
                outputs:
                  anyOf:
                    - additionalProperties: true
                      type: object
                    - type: 'null'
                  title: Outputs
                  deprecated: true
                  description: 'Deprecated: use reference_outputs instead.'
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
                  anyOf:
                    - additionalProperties: true
                      type: object
                    - type: 'null'
                  title: Inputs
                split:
                  anyOf:
                    - items:
                        type: string
                      type: array
                    - type: string
                    - type: 'null'
                  title: Split
                  default: base
                id:
                  anyOf:
                    - type: string
                      format: uuid
                    - type: 'null'
                  title: Id
                use_source_run_io:
                  type: boolean
                  title: Use Source Run Io
                  default: false
                use_source_run_attachments:
                  default: []
                  items:
                    type: string
                  title: Use Source Run Attachments
                  type: array
                use_legacy_message_format:
                  default: false
                  description: Use Legacy Message Format for LLM runs
                  title: Use Legacy Message Format
                  type: boolean
                created_at:
                  type: string
                  title: Created At
                reference_outputs:
                  anyOf:
                    - additionalProperties: true
                      type: object
                    - type: 'null'
                  title: Reference Outputs
              required:
                - dataset_id
              title: ExampleCreate
              type: object
              not:
                required:
                  - outputs
                  - reference_outputs
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Example'
      security:
        - API Key: []
        - Tenant ID: []
        - Bearer Auth: []
components:
  schemas:
    Example:
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
      type: object
      required:
        - dataset_id
        - inputs
        - id
        - name
      title: Example
      description: Example schema.
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

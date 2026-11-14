# Ingest runs (batch json)

> Ingests a batch of runs in a single JSON payload. The payload must have `post` and/or `patch` arrays containing run objects.
Prefer this endpoint over single‑run ingestion when submitting hundreds of runs, but `/runs/multipart` offers better handling for very large fields and attachments.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json post /api/v1/runs/batch
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
  /api/v1/runs/batch:
    post:
      tags:
        - runs
      summary: Ingest runs (batch json)
      description: >-
        Ingests a batch of runs in a single JSON payload. The payload must have
        `post` and/or `patch` arrays containing run objects.

        Prefer this endpoint over single‑run ingestion when submitting hundreds
        of runs, but `/runs/multipart` offers better handling for very large
        fields and attachments.
      parameters: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                patch:
                  type: array
                  items:
                    $ref: '#/components/schemas/runs.Run'
                post:
                  type: array
                  items:
                    $ref: '#/components/schemas/runs.Run'
      responses:
        '202':
          description: Runs batch ingested
          content:
            application/json:
              schema:
                type: object
                additionalProperties:
                  allOf:
                    - type: string
                    - type: object
                      properties:
                        message:
                          type: string
        '400':
          description: Bad Request
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/runs.ErrorResponse'
        '403':
          description: Forbidden
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/runs.ErrorResponse'
        '408':
          description: Request body was not fully received within the server time limit
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/runs.ErrorResponse'
        '409':
          description: Conflict
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/runs.ErrorResponse'
        '413':
          description: Request Entity Too Large
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/runs.ErrorResponse'
        '422':
          description: Unprocessable Entity
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/runs.ErrorResponse'
        '429':
          description: Too Many Requests
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/runs.ErrorResponse'
      security:
        - API Key: []
        - Tenant ID: []
        - Bearer Auth: []
components:
  schemas:
    runs.Run:
      type: object
      properties:
        address:
          description: >-
            Addresses the run to an Agent environment in place of session_id or

            session_name, as lrn:agents/{id}/environments/{environment}. The
            environment is

            case-insensitive. Self-hosted deployments need LangSmith v0.18 or
            later.
          type: string
          example: lrn:agents/support-agent/environments/production
        dotted_order:
          type: string
        end_time:
          type: string
        error:
          type: string
        events:
          items:
            additionalProperties: true
            type: object
          type: array
        extra:
          additionalProperties: true
          type: object
        id:
          type: string
        input_attachments:
          additionalProperties: true
          type: object
        inputs:
          additionalProperties: true
          type: object
        name:
          type: string
        output_attachments:
          additionalProperties: true
          type: object
        outputs:
          additionalProperties: true
          type: object
        parent_run_id:
          type: string
        reference_example_id:
          type: string
        run_type:
          type: string
          enum:
            - tool
            - chain
            - llm
            - retriever
            - embedding
            - prompt
            - parser
        serialized:
          additionalProperties: true
          type: object
        session_id:
          type: string
        session_name:
          type: string
        start_time:
          type: string
        status:
          type: string
        tags:
          items:
            type: string
          type: array
        trace_id:
          type: string
    runs.ErrorResponse:
      type: object
      properties:
        details:
          description: Optional error details as JSON string
          type: string
          example: '{"field":"dataset_id","reason":"required"}'
        error:
          description: Error message
          type: string
          example: 'Invalid request: missing required fields'
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

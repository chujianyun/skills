# Get experiment view override configuration by specific ID

> Retrieves a specific experiment view override configuration using both dataset ID and override ID.
This endpoint provides more precise access to experiment view overrides when you have
the specific override ID, useful for direct links or cached references.

The response includes the same column override information as the dataset-level endpoint:
- Column identifiers with validation prefixes
- Color gradient settings for numeric data visualization
- Numeric precision configurations
- Column visibility controls

Both the dataset and override must exist and be accessible by the authenticated user.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json get /datasets/{dataset_id}/experiment-view-overrides/{id}
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
  /datasets/{dataset_id}/experiment-view-overrides/{id}:
    get:
      tags:
        - experiment-view-overrides
      summary: Get experiment view override configuration by specific ID
      description: >-
        Retrieves a specific experiment view override configuration using both
        dataset ID and override ID.

        This endpoint provides more precise access to experiment view overrides
        when you have

        the specific override ID, useful for direct links or cached references.


        The response includes the same column override information as the
        dataset-level endpoint:

        - Column identifiers with validation prefixes

        - Color gradient settings for numeric data visualization

        - Numeric precision configurations

        - Column visibility controls


        Both the dataset and override must exist and be accessible by the
        authenticated user.
      parameters:
        - example: '"550e8400-e29b-41d4-a716-446655440000"'
          description: Dataset ID
          name: dataset_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
        - example: '"123e4567-e89b-12d3-a456-426614174000"'
          description: Experiment view override ID
          name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: Successfully retrieved experiment view override configuration
          content:
            application/json:
              schema:
                $ref: >-
                  #/components/schemas/experiment_view_overrides.ExperimentViewOverride
        '400':
          description: >-
            Invalid ID format" example({"error":"invalid experiment view
            override ID format"})
          content:
            application/json:
              schema:
                type: object
                additionalProperties:
                  type: string
        '401':
          description: Unauthorized access" example({"error":"Unauthorized"})
          content:
            application/json:
              schema:
                type: object
                additionalProperties:
                  type: string
        '404':
          description: >-
            Override not found" example({"error":"experiment view override not
            found"})
          content:
            application/json:
              schema:
                type: object
                additionalProperties:
                  type: string
        '500':
          description: Internal server error" example({"error":"internal server error"})
          content:
            application/json:
              schema:
                type: object
                additionalProperties:
                  type: string
      security:
        - API Key: []
        - Tenant ID: []
        - Bearer Auth: []
components:
  schemas:
    experiment_view_overrides.ExperimentViewOverride:
      type: object
      properties:
        column_overrides:
          type: array
          items:
            $ref: '#/components/schemas/experiment_view_overrides.ColumnOverride'
        created_at:
          type: string
        dataset_id:
          type: string
        id:
          type: string
        modified_at:
          type: string
    experiment_view_overrides.ColumnOverride:
      type: object
      required:
        - column
      properties:
        color_gradient:
          type: array
          maxItems: 20
          items:
            type: array
            items: {}
        color_map:
          additionalProperties: true
          type: object
        column:
          type: string
          maxLength: 200
        disable_colors:
          type: boolean
        hide:
          type: boolean
        precision:
          type: integer
          maximum: 6
          minimum: 1
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

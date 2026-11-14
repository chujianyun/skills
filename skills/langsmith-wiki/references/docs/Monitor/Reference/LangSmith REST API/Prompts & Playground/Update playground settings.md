# Update playground settings

> Update playground settings.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json patch /api/v1/playground-settings/{playground_settings_id}
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
  /api/v1/playground-settings/{playground_settings_id}:
    patch:
      tags:
        - playground-settings
      summary: Update playground settings
      description: Update playground settings.
      operationId: >-
        update_playground_settings_api_v1_playground_settings__playground_settings_id__patch
      parameters:
        - name: playground_settings_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
            title: Playground Settings Id
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PlaygroundSettingsUpdateRequest'
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PlaygroundSettingsResponse'
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
      security:
        - API Key: []
        - Tenant ID: []
        - Organization ID: []
        - Bearer Auth: []
components:
  schemas:
    PlaygroundSettingsUpdateRequest:
      properties:
        name:
          anyOf:
            - type: string
            - type: 'null'
          title: Name
        description:
          anyOf:
            - type: string
            - type: 'null'
          title: Description
        settings:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Settings
        options:
          anyOf:
            - $ref: '#/components/schemas/PlaygroundSavedOptions'
            - type: 'null'
        available_in_playground:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Available In Playground
        available_in_evaluators:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Available In Evaluators
        available_in_agent_builder:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Available In Agent Builder
        available_in_polly:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Available In Polly
        available_in_insights_heavy:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Available In Insights Heavy
        available_in_insights_light:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Available In Insights Light
        oauth_enabled:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Oauth Enabled
        oauth_token_url:
          anyOf:
            - type: string
            - type: 'null'
          title: Oauth Token Url
        oauth_client_id:
          anyOf:
            - type: string
            - type: 'null'
          title: Oauth Client Id
        oauth_client_secret:
          anyOf:
            - type: string
            - type: 'null'
          title: Oauth Client Secret
        oauth_token_endpoint_auth_method:
          anyOf:
            - type: string
              enum:
                - client_secret_basic
                - client_secret_post
            - type: 'null'
          title: Oauth Token Endpoint Auth Method
        oauth_params:
          anyOf:
            - additionalProperties:
                items:
                  type: string
                type: array
              type: object
            - type: 'null'
          title: Oauth Params
        oauth_headers:
          anyOf:
            - additionalProperties:
                items:
                  type: string
                type: array
              type: object
            - type: 'null'
          title: Oauth Headers
      type: object
      title: PlaygroundSettingsUpdateRequest
    PlaygroundSettingsResponse:
      properties:
        id:
          type: string
          format: uuid
          title: Id
        settings:
          additionalProperties: true
          type: object
          title: Settings
        options:
          anyOf:
            - $ref: '#/components/schemas/PlaygroundSavedOptions'
            - type: 'null'
        name:
          anyOf:
            - type: string
            - type: 'null'
          title: Name
        organization_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Organization Id
        created_at:
          type: string
          format: date-time
          title: Created At
        updated_at:
          type: string
          format: date-time
          title: Updated At
        description:
          anyOf:
            - type: string
            - type: 'null'
          title: Description
        settings_type:
          type: string
          enum:
            - complex
            - simple
          title: Settings Type
          default: complex
        created_by_ls_user_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Created By Ls User Id
        updated_by_ls_user_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Updated By Ls User Id
        available_in_playground:
          type: boolean
          title: Available In Playground
          default: true
        available_in_evaluators:
          type: boolean
          title: Available In Evaluators
          default: true
        available_in_agent_builder:
          type: boolean
          title: Available In Agent Builder
          default: false
        available_in_polly:
          type: boolean
          title: Available In Polly
          default: false
        available_in_insights_heavy:
          type: boolean
          title: Available In Insights Heavy
          default: false
        available_in_insights_light:
          type: boolean
          title: Available In Insights Light
          default: false
        oauth_enabled:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Oauth Enabled
        oauth_token_url:
          anyOf:
            - type: string
            - type: 'null'
          title: Oauth Token Url
        oauth_client_id:
          anyOf:
            - type: string
            - type: 'null'
          title: Oauth Client Id
        oauth_client_secret:
          anyOf:
            - type: string
            - type: 'null'
          title: Oauth Client Secret
        oauth_token_endpoint_auth_method:
          anyOf:
            - type: string
              enum:
                - client_secret_basic
                - client_secret_post
            - type: 'null'
          title: Oauth Token Endpoint Auth Method
        oauth_params:
          anyOf:
            - additionalProperties:
                items:
                  type: string
                type: array
              type: object
            - type: 'null'
          title: Oauth Params
        oauth_headers:
          anyOf:
            - additionalProperties:
                items:
                  type: string
                type: array
              type: object
            - type: 'null'
          title: Oauth Headers
      type: object
      required:
        - id
        - settings
        - created_at
        - updated_at
      title: PlaygroundSettingsResponse
    HTTPValidationError:
      properties:
        detail:
          items:
            type: string
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    PlaygroundSavedOptions:
      properties:
        requests_per_second:
          anyOf:
            - type: integer
            - type: 'null'
          title: Requests Per Second
      type: object
      title: PlaygroundSavedOptions
  securitySchemes:
    API Key:
      type: apiKey
      in: header
      name: X-API-Key
    Tenant ID:
      type: apiKey
      in: header
      name: X-Tenant-Id
    Organization ID:
      type: apiKey
      in: header
      name: X-Organization-Id
    Bearer Auth:
      type: http
      description: >-
        Bearer tokens are used to authenticate from the UI. Must also specify
        x-tenant-id or x-organization-id (for org scoped apis).
      scheme: bearer

````

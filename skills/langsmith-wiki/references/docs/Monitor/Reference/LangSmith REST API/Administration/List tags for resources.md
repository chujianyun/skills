# List tags for resources



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json post /api/v1/workspaces/current/tags/resources
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
  /api/v1/workspaces/current/tags/resources:
    post:
      tags:
        - workspaces
      summary: List tags for resources
      operationId: list_tags_for_resources_api_v1_workspaces_current_tags_resources_post
      requestBody:
        content:
          application/json:
            schema:
              items:
                $ref: '#/components/schemas/ListTagsForResourceRequest'
              type: array
              title: Resources
        required: true
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                additionalProperties:
                  items:
                    $ref: '#/components/schemas/TagKeyWithValuesAndTaggings'
                  type: array
                propertyNames:
                  format: uuid
                type: object
                title: >-
                  Response List Tags For Resources Api V1 Workspaces Current
                  Tags Resources Post
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
    ListTagsForResourceRequest:
      properties:
        resource_id:
          type: string
          format: uuid
          title: Resource Id
        resource_type:
          $ref: '#/components/schemas/ResourceType'
      type: object
      required:
        - resource_id
        - resource_type
      title: ListTagsForResourceRequest
    TagKeyWithValuesAndTaggings:
      properties:
        key:
          type: string
          maxLength: 255
          minLength: 1
          title: Key
        description:
          anyOf:
            - type: string
            - type: 'null'
          title: Description
        id:
          type: string
          format: uuid
          title: Id
        created_at:
          type: string
          format: date-time
          title: Created At
        updated_at:
          type: string
          format: date-time
          title: Updated At
        values:
          items:
            $ref: '#/components/schemas/TagValueWithTaggings'
          type: array
          title: Values
      type: object
      required:
        - key
        - id
        - created_at
        - updated_at
      title: TagKeyWithValuesAndTaggings
    HTTPValidationError:
      properties:
        detail:
          items:
            type: string
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    ResourceType:
      type: string
      enum:
        - agent
        - custom_app
        - dashboard
        - dataset
        - deployment
        - evaluator
        - experiment
        - fleet_integration
        - mcp_server
        - project
        - prompt
        - queue
        - sandbox
        - skill
        - snapshot_name
      title: ResourceType
    TagValueWithTaggings:
      properties:
        value:
          type: string
          maxLength: 255
          minLength: 1
          title: Value
        description:
          anyOf:
            - type: string
            - type: 'null'
          title: Description
        id:
          type: string
          format: uuid
          title: Id
        tag_key_id:
          type: string
          format: uuid
          title: Tag Key Id
        created_at:
          type: string
          format: date-time
          title: Created At
        updated_at:
          type: string
          format: date-time
          title: Updated At
        taggings:
          items:
            $ref: '#/components/schemas/Tagging'
          type: array
          title: Taggings
      type: object
      required:
        - value
        - id
        - tag_key_id
        - created_at
        - updated_at
      title: TagValueWithTaggings
    Tagging:
      properties:
        tag_value_id:
          type: string
          format: uuid
          title: Tag Value Id
        resource_type:
          $ref: '#/components/schemas/ResourceType'
        resource_id:
          type: string
          format: uuid
          title: Resource Id
        id:
          type: string
          format: uuid
          title: Id
        created_at:
          type: string
          format: date-time
          title: Created At
      type: object
      required:
        - tag_value_id
        - resource_type
        - resource_id
        - id
        - created_at
      title: Tagging
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

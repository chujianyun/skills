# List repo tags

> Get all repo tags.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json get /api/v1/repos/tags
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
  /api/v1/repos/tags:
    get:
      tags:
        - repos
      summary: List repo tags
      description: Get all repo tags.
      operationId: list_repo_tags_api_v1_repos_tags_get
      parameters:
        - name: limit
          in: query
          required: false
          schema:
            type: integer
            maximum: 100
            minimum: 1
            default: 20
            title: Limit
        - name: offset
          in: query
          required: false
          schema:
            type: integer
            minimum: 0
            title: Offset
            default: 0
        - name: tenant_handle
          in: query
          required: false
          schema:
            anyOf:
              - type: string
              - type: 'null'
            title: Tenant Handle
        - name: tenant_id
          in: query
          required: false
          schema:
            anyOf:
              - type: string
                format: uuid
              - type: 'null'
            title: Tenant Id
        - name: query
          in: query
          required: false
          schema:
            anyOf:
              - type: string
              - type: 'null'
            title: Query
        - name: has_commits
          in: query
          required: false
          schema:
            anyOf:
              - type: boolean
              - type: 'null'
            title: Has Commits
        - name: tags
          in: query
          required: false
          schema:
            anyOf:
              - items:
                  type: string
                type: array
              - type: 'null'
            title: Tags
        - name: is_archived
          in: query
          required: false
          schema:
            anyOf:
              - enum:
                  - 'true'
                  - allow
                  - 'false'
                type: string
              - type: 'null'
            title: Is Archived
        - name: is_public
          in: query
          required: false
          schema:
            anyOf:
              - $ref: '#/components/schemas/TrueFalseLiteral'
              - type: 'null'
            title: Is Public
        - name: upstream_repo_owner
          in: query
          required: false
          schema:
            anyOf:
              - type: string
              - type: 'null'
            title: Upstream Repo Owner
        - name: upstream_repo_handle
          in: query
          required: false
          schema:
            anyOf:
              - type: string
              - type: 'null'
            title: Upstream Repo Handle
        - name: tag_value_id
          in: query
          required: false
          schema:
            anyOf:
              - items:
                  type: string
                  format: uuid
                type: array
              - type: 'null'
            title: Tag Value Id
        - name: repo_type
          in: query
          required: false
          schema:
            anyOf:
              - enum:
                  - prompt
                  - file
                  - agent
                  - skill
                type: string
              - type: 'null'
            title: Repo Type
        - name: repo_types
          in: query
          required: false
          schema:
            anyOf:
              - type: array
                items:
                  enum:
                    - prompt
                    - file
                    - agent
                    - skill
                  type: string
              - type: 'null'
            title: Repo Types
        - name: source
          in: query
          required: false
          schema:
            anyOf:
              - type: string
                enum:
                  - internal
                  - external
              - type: 'null'
            title: Source
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ListTagsResponse'
        '422':
          description: The request has an invalid path, query, header, or body parameter.
          content:
            application/problem+json:
              schema:
                allOf:
                  - $ref: '#/components/schemas/ProblemDetails'
                  - type: object
                    required:
                      - errors
                    properties:
                      errors:
                        type: array
                        items:
                          type: string
                        description: >-
                          One message per invalid parameter, prefixed with its
                          location.
      security:
        - API Key: []
        - Tenant ID: []
        - Bearer Auth: []
components:
  schemas:
    TrueFalseLiteral:
      type: string
      enum:
        - 'true'
        - 'false'
      title: TrueFalseLiteral
    ListTagsResponse:
      properties:
        tags:
          items:
            $ref: '#/components/schemas/TagCount'
          type: array
          title: Tags
      type: object
      required:
        - tags
      title: ListTagsResponse
    ProblemDetails:
      properties:
        type:
          type: string
          title: Type
        title:
          type: string
          title: Title
        status:
          type: integer
          title: Status
        detail:
          type: string
          title: Detail
      type: object
      required:
        - type
        - title
        - status
        - detail
      title: ProblemDetails
      description: Problem details describing an error response, as defined by RFC 7807.
    TagCount:
      properties:
        tag:
          type: string
          title: Tag
        count:
          type: integer
          title: Count
      type: object
      required:
        - tag
        - count
      title: TagCount
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

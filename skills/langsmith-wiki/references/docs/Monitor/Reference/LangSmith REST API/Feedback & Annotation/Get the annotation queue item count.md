# Get the annotation queue item count

> Returns the number of annotation queue items in one status bucket. The two time windows are independent: start_time/end_time bound when an item was archived, min_start_time/max_start_time bound when its trace ran. Items with no trace start time are excluded when either of the latter is set.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json get /api/v1/platform/annotation-queues/{queue_id}/items/count
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
  /api/v1/platform/annotation-queues/{queue_id}/items/count:
    get:
      tags:
        - annotation_queues
      summary: Get the annotation queue item count
      description: >-
        Returns the number of annotation queue items in one status bucket. The
        two time windows are independent: start_time/end_time bound when an item
        was archived, min_start_time/max_start_time bound when its trace ran.
        Items with no trace start time are excluded when either of the latter is
        set.
      parameters:
        - description: Queue ID
          name: queue_id
          in: path
          required: true
          schema:
            type: string
        - description: >-
            Count bucket: all, needs_my_review, needs_others_review, or
            archived.
          name: status
          in: query
          required: true
          schema:
            type: string
            title: Status
        - description: Archived strictly after this time. Only used when status=archived
          name: start_time
          in: query
          schema:
            type: string
            title: Start Time
        - description: Archived strictly before this time. Only used when status=archived
          name: end_time
          in: query
          schema:
            type: string
            title: End Time
        - description: Trace started at or after this time
          name: min_start_time
          in: query
          schema:
            format: date-time
            type: string
            title: Min Start Time
        - description: Trace started at or before this time
          name: max_start_time
          in: query
          schema:
            format: date-time
            type: string
            title: Max Start Time
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: >-
                  #/components/schemas/annotationqueues.AnnotationQueueItemCountResponse
        '400':
          description: Bad Request
          content:
            application/json:
              schema:
                type: object
                additionalProperties:
                  type: string
        '403':
          description: Forbidden
          content:
            application/json:
              schema:
                type: object
                additionalProperties:
                  type: string
        '404':
          description: Not Found
          content:
            application/json:
              schema:
                type: object
                additionalProperties:
                  type: string
        '422':
          description: Unprocessable Entity
          content:
            application/json:
              schema:
                type: object
                additionalProperties:
                  type: string
        '500':
          description: Internal Server Error
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
    annotationqueues.AnnotationQueueItemCountResponse:
      type: object
      properties:
        count:
          type: integer
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

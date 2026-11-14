# List annotation queue items

> List RUN and THREAD items in a single annotation queue for one review status section, with opaque cursor pagination. Optional item_type=RUN|THREAD filters the page. Optional min_start_time/max_start_time bound the item's trace start time; items with no start time are excluded when either bound is set. direction=backward returns items before the supplied cursor. The response contains item metadata only, not expanded run or thread payloads. status=archived returns items whose queue review requirements have been satisfied, not merely items the caller personally marked completed.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json get /api/v1/platform/annotation-queues/{queue_id}/items
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
  /api/v1/platform/annotation-queues/{queue_id}/items:
    get:
      tags:
        - annotation_queues
      summary: List annotation queue items
      description: >-
        List RUN and THREAD items in a single annotation queue for one review
        status section, with opaque cursor pagination. Optional
        item_type=RUN|THREAD filters the page. Optional
        min_start_time/max_start_time bound the item's trace start time; items
        with no start time are excluded when either bound is set.
        direction=backward returns items before the supplied cursor. The
        response contains item metadata only, not expanded run or thread
        payloads. status=archived returns items whose queue review requirements
        have been satisfied, not merely items the caller personally marked
        completed.
      parameters:
        - description: Annotation queue ID
          name: queue_id
          in: path
          required: true
          schema:
            type: string
        - description: 'Review section: needs_my_review, needs_others_review, or archived'
          name: status
          in: query
          required: true
          schema:
            type: string
            enum:
              - needs_my_review
              - needs_others_review
              - archived
            title: Status
        - description: Page size (max 100)
          name: page_size
          in: query
          schema:
            type: integer
            default: 20
            title: Page Size
        - description: Opaque pagination cursor
          name: cursor
          in: query
          schema:
            type: string
            title: Cursor
        - description: Filter to RUN or THREAD
          name: item_type
          in: query
          schema:
            type: string
            enum:
              - RUN
              - THREAD
            title: Item Type
        - description: >-
            Only items whose trace start time is at or after this timestamp.
            Omit or send the zero time for no bound
          name: min_start_time
          in: query
          schema:
            format: date-time
            type: string
            title: Min Start Time
        - description: >-
            Only items whose trace start time is at or before this timestamp.
            Omit or send the zero time for no bound
          name: max_start_time
          in: query
          schema:
            format: date-time
            type: string
            title: Max Start Time
        - description: Pagination direction. backward requires cursor
          name: direction
          in: query
          schema:
            type: string
            enum:
              - forward
              - backward
            default: forward
            title: Direction
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: >-
                  #/components/schemas/annotationqueues.ListAnnotationQueueItemsResponse
        '400':
          description: Bad Request
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/shared.ProblemDetails'
        '403':
          description: Forbidden
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/shared.ProblemDetails'
        '404':
          description: Not Found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/shared.ProblemDetails'
      security:
        - API Key: []
        - Tenant ID: []
        - Bearer Auth: []
components:
  schemas:
    annotationqueues.ListAnnotationQueueItemsResponse:
      type: object
      properties:
        items:
          type: array
          items:
            $ref: '#/components/schemas/annotationqueues.AnnotationQueueListItem'
        next_cursor:
          type: string
        previous_cursor:
          type: string
    shared.ProblemDetails:
      description: RFC 7807 problem details returned on V2 API errors.
      type: object
      properties:
        detail:
          type: string
        details:
          description: >-
            Details is a LangSmith extension carrying structured fields for
            ErrorClass.
          allOf:
            - $ref: '#/components/schemas/shared.ParseErrorDetails'
        error_class:
          description: |-
            ErrorClass is a LangSmith extension sub-categorizing a status code.
            Additional values require expanding this enum and adding a oneOf
            discriminator on Details to keep the class↔details contract typed.
          type: string
          enum:
            - PARSE_FAILURE
        instance:
          type: string
        remedy:
          description: Remedy is a LangSmith extension for user-recoverable errors.
          type: string
        status:
          type: integer
        title:
          type: string
        type:
          type: string
    annotationqueues.AnnotationQueueListItem:
      type: object
      properties:
        added_at:
          type: string
        completed_by:
          items:
            type: string
          type: array
        effective_added_at:
          type: string
        id:
          type: string
        item_type:
          $ref: '#/components/schemas/annotationqueues.AnnotationQueueItemType'
        last_reviewed_time:
          description: >-
            LastReviewedTime is always present on the wire (null until
            reviewed).
          type: string
        project_id:
          type: string
        queue_id:
          type: string
        reserved_by:
          items:
            type: string
          type: array
        run_id:
          type: string
        source_proposed_example_id:
          type: string
        start_time:
          type: string
        thread_id:
          type: string
    shared.ParseErrorDetails:
      description: Structured fields describing an adapter parse failure.
      type: object
      required:
        - adapter
        - item_type
      properties:
        adapter:
          type: string
        item_type:
          type: string
        run_id:
          type: string
    annotationqueues.AnnotationQueueItemType:
      type: string
      enum:
        - RUN
        - THREAD
      x-enum-varnames:
        - AnnotationQueueItemTypeRun
        - AnnotationQueueItemTypeThread
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

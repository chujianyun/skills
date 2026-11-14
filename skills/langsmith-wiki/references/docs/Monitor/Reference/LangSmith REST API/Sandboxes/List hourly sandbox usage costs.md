# List hourly sandbox usage costs

> Returns priced usage per sandbox or snapshot and UTC hour in the half-open requested interval. LCU uses the recorded compute amount for sandboxes; snapshots have zero LCU. LSU allocates the recorded workspace storage amount proportionally to attributed bytes, including checkpoints on their sandbox and snapshots as separate resources. Resource filters preserve each resource's share. Rate changes do not reprice recorded amounts. An access-filtered page can have no items and a non-null next_cursor; continue until next_cursor is null.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json get /api/v2/sandboxes/usage/costs
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
  /api/v2/sandboxes/usage/costs:
    get:
      tags:
        - sandboxes
      summary: List hourly sandbox usage costs
      description: >-
        Returns priced usage per sandbox or snapshot and UTC hour in the
        half-open requested interval. LCU uses the recorded compute amount for
        sandboxes; snapshots have zero LCU. LSU allocates the recorded workspace
        storage amount proportionally to attributed bytes, including checkpoints
        on their sandbox and snapshots as separate resources. Resource filters
        preserve each resource's share. Rate changes do not reprice recorded
        amounts. An access-filtered page can have no items and a non-null
        next_cursor; continue until next_cursor is null.
      parameters:
        - description: Inclusive RFC3339 start time
          name: start_time
          in: query
          required: true
          schema:
            type: string
            format: date-time
            title: Start Time
        - description: Exclusive RFC3339 end time; the range must not exceed 31 days
          name: end_time
          in: query
          required: true
          schema:
            type: string
            format: date-time
            title: End Time
        - description: Resource type filter
          name: resource_type
          in: query
          schema:
            type: string
            enum:
              - SANDBOX
              - SNAPSHOT
            title: Resource Type
        - description: Resource UUID filter; repeat this parameter up to 100 times
          name: resource_ids
          in: query
          style: form
          explode: true
          schema:
            type: array
            items:
              type: string
            title: Resource Ids
        - description: Maximum rows to return
          name: page_size
          in: query
          schema:
            type: integer
            maximum: 100
            minimum: 1
            title: Page Size
            default: 20
        - description: >-
            HOUR returns hourly buckets. RESOURCE sums each resource over the
            requested interval and sets period_start to start_time.
          name: granularity
          in: query
          schema:
            type: string
            enum:
              - HOUR
              - RESOURCE
            default: HOUR
            title: Granularity
        - description: Opaque pagination cursor
          name: cursor
          in: query
          schema:
            type: string
            title: Cursor
        - description: >-
            Include usage totals across the filtered interval (RESOURCE only).
            Omitted when unrestricted resource access cannot be verified or the
            service does not support totals. CLI: use --format raw to show this
            summary.
          name: include_totals
          in: query
          schema:
            type: boolean
            default: false
            title: Include Totals
        - description: >-
            Include bounded daily physical usage for the top 10 resources per
            metric and Other. Requires RESOURCE and include_totals. Omitted when
            unrestricted access or service support is unavailable. CLI: use
            --format raw to show this summary.
          name: include_daily
          in: query
          schema:
            type: boolean
            default: false
            title: Include Daily
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/sandboxes.SandboxUsageCostsResponse'
        '400':
          description: missing or invalid query parameters
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/shared.ProblemDetails'
        '401':
          description: missing or invalid authentication
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/shared.ProblemDetails'
        '403':
          description: forbidden (insufficient permission)
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/shared.ProblemDetails'
        '500':
          description: internal server error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/shared.ProblemDetails'
      security:
        - API Key: []
          Tenant ID: []
        - Bearer Auth: []
          Tenant ID: []
components:
  schemas:
    sandboxes.SandboxUsageCostsResponse:
      type: object
      required:
        - items
        - next_cursor
      properties:
        daily:
          description: >-
            Daily usage over the full filtered interval, independent of
            pagination.

            Omitted unless requested, supported, and unrestricted resource
            access is verified.
          allOf:
            - $ref: '#/components/schemas/sandboxes.SandboxUsageDailyResponse'
        items:
          type: array
          items:
            $ref: '#/components/schemas/sandboxes.SandboxUsageCost'
        next_cursor:
          anyOf:
            - type: string
            - type: 'null'
        totals:
          description: >-
            Totals cover the entire filtered interval, independently of the
            cursor.

            Omitted unless requested and unrestricted resource access is
            verified.
          allOf:
            - $ref: '#/components/schemas/sandboxes.SandboxUsageCostTotals'
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
    sandboxes.SandboxUsageDailyResponse:
      type: object
      required:
        - entries
      properties:
        entries:
          type: array
          items:
            $ref: '#/components/schemas/sandboxes.SandboxUsageDaily'
    sandboxes.SandboxUsageCost:
      type: object
      required:
        - lcu
        - lsu
        - period_start
        - resource_id
        - resource_type
      properties:
        compute_standard_units:
          description: >-
            Recorded compute usage in Standard Units, as a decimal string,
            separate from LCU.

            Null means complete Standard compute usage is unavailable; "0" means
            known zero usage.
          anyOf:
            - type: string
              format: decimal
            - type: 'null'
        lcu:
          description: >-
            Recorded compute usage in LangSmith Compute Units (LCU), as a
            decimal string

            with up to six fractional digits and trailing zeros omitted.
            Snapshots return "0".
          type: string
          format: decimal
          example: '1.234567'
        lsu:
          description: >-
            Allocated storage usage in LangSmith Storage Units (LSU), as a
            decimal string

            with up to six fractional digits and trailing zeros omitted.
          type: string
          format: decimal
          example: '0.000123'
        memory_gib_hours:
          description: >-
            Memory usage in GiB-hours, as a decimal string. Available with
            RESOURCE granularity; null means complete usage is unavailable.
          anyOf:
            - type: string
              format: decimal
            - type: 'null'
        period_start:
          type: string
          format: date-time
        resource_id:
          type: string
          format: uuid
        resource_type:
          $ref: '#/components/schemas/sandboxes.UsageCostResourceType'
        storage_gib_hours:
          description: >-
            Recorded storage usage in GiB-hours from hourly samples, including
            checkpoints. Available with RESOURCE granularity. Missing intervals
            are excluded; null means no usable measurements are available.
          anyOf:
            - type: string
              format: decimal
            - type: 'null'
        storage_standard_units:
          description: >-
            Allocated storage usage in Standard Units, as a decimal string,
            separate from LSU.

            Null means complete Standard storage usage is unavailable; "0" means
            known zero usage.
          anyOf:
            - type: string
              format: decimal
            - type: 'null'
        vcpu_hours:
          description: >-
            CPU usage in vCPU-hours, as a decimal string. Available with
            RESOURCE granularity; null means complete usage is unavailable.
          anyOf:
            - type: string
              format: decimal
            - type: 'null'
    sandboxes.SandboxUsageCostTotals:
      type: object
      required:
        - lcu
        - lsu
      properties:
        compute_standard_units:
          description: >-
            Total compute usage in Standard Units across the entire filtered
            interval,

            independent of pagination, as a decimal string, separate from LCU.

            Null means complete Standard compute usage is unavailable; "0" means
            known zero usage.
          anyOf:
            - type: string
              format: decimal
            - type: 'null'
        lcu:
          type: string
          format: decimal
        lsu:
          type: string
          format: decimal
        memory_gib_hours:
          description: >-
            Memory usage in GiB-hours, as a decimal string. Null means complete
            usage is unavailable.
          anyOf:
            - type: string
              format: decimal
            - type: 'null'
        storage_gib_hours:
          description: >-
            Recorded storage usage in GiB-hours from hourly samples, including
            checkpoints. Missing intervals are excluded; null means no usable
            measurements are available.
          anyOf:
            - type: string
              format: decimal
            - type: 'null'
        storage_standard_units:
          description: >-
            Total storage usage in Standard Units across the entire filtered
            interval,

            independent of pagination, as a decimal string, separate from LSU.

            Null means complete Standard storage usage is unavailable; "0" means
            known zero usage.
          anyOf:
            - type: string
              format: decimal
            - type: 'null'
        vcpu_hours:
          description: >-
            CPU usage in vCPU-hours, as a decimal string. Null means complete
            usage is unavailable.
          anyOf:
            - type: string
              format: decimal
            - type: 'null'
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
    sandboxes.SandboxUsageDaily:
      type: object
      required:
        - is_other
        - period_start
      properties:
        is_other:
          description: >-
            Other combines resources outside the top groups. Their individual
            IDs are omitted.
          type: boolean
        memory_gib_hours:
          description: >-
            Memory usage in GiB-hours, as a decimal string. Null means complete
            usage is unavailable.
          anyOf:
            - type: string
              format: decimal
            - type: 'null'
        period_start:
          type: string
          format: date-time
        resource_id:
          type: string
          format: uuid
        resource_type:
          $ref: '#/components/schemas/sandboxes.UsageCostResourceType'
        storage_gib_hours:
          description: >-
            Recorded storage usage in GiB-hours from hourly samples. Missing
            intervals are excluded; null means no usable measurements are
            available.
          anyOf:
            - type: string
              format: decimal
            - type: 'null'
        vcpu_hours:
          description: >-
            CPU usage in vCPU-hours, as a decimal string. Null means complete
            usage is unavailable.
          anyOf:
            - type: string
              format: decimal
            - type: 'null'
    sandboxes.UsageCostResourceType:
      type: string
      enum:
        - SANDBOX
        - SNAPSHOT
      x-enum-varnames:
        - UsageCostResourceSandbox
        - UsageCostResourceSnapshot
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

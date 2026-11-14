# List issues (Beta)

> **Beta:** This endpoint is in active development and may change without notice.

Returns issues for the authenticated tenant, optionally filtered
by session, status, severity, tag, linked trace, or last modified time.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json get /api/v1/platform/issues
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
  /api/v1/platform/issues:
    get:
      tags:
        - issues
      summary: List issues (Beta)
      description: >-
        **Beta:** This endpoint is in active development and may change without
        notice.


        Returns issues for the authenticated tenant, optionally filtered

        by session, status, severity, tag, linked trace, or last modified time.
      parameters:
        - description: Filter by session ID (UUID)
          name: session_id
          in: query
          schema:
            type: string
            title: Session Id
        - description: Filter by session name (exact match)
          name: session_name
          in: query
          schema:
            type: string
            title: Session Name
        - description: Filter by status
          name: status
          in: query
          schema:
            type: string
            enum:
              - open
              - fixing
              - watching
              - completed
              - ignored
            title: Status
        - description: Filter by severity
          name: severity
          in: query
          schema:
            type: integer
            enum:
              - 0
              - 1
              - 2
              - 3
            title: Severity
        - description: Filter by exact severity (repeatable; OR semantics)
          name: severity_exact
          in: query
          style: form
          explode: true
          schema:
            type: array
            items:
              enum:
                - 0
                - 1
                - 2
                - 3
              type: integer
            title: Severity Exact
        - description: Filter by Engine activity (repeatable; OR semantics)
          name: activity
          in: query
          style: form
          explode: true
          schema:
            type: array
            items:
              enum:
                - fixing
                - watching
                - recurred
              type: string
            title: Activity
        - description: Filter by tag (exact match)
          name: tag
          in: query
          schema:
            type: string
            title: Tag
        - description: Return only issues with a linked run in this trace
          name: trace_id
          in: query
          schema:
            type: string
            format: uuid
            title: Trace Id
        - description: Return only issues updated at or after this RFC3339 timestamp
          name: updated_at
          in: query
          schema:
            type: string
            title: Updated At
        - description: Sort field
          name: sort_by
          in: query
          schema:
            type: string
            enum:
              - default
              - created_at
              - updated_at
              - last_seen
              - last_updated
              - trace_count
              - severity
            title: Sort By
        - description: Group results by issue lifecycle status before applying sort_by
          name: status_first
          in: query
          schema:
            type: boolean
            title: Status First
        - description: Page size (positive integer; defaults to 50, capped at 500)
          name: limit
          in: query
          schema:
            type: integer
            title: Limit
        - description: Page offset (non-negative integer; at most 100000)
          name: offset
          in: query
          schema:
            type: integer
            title: Offset
      responses:
        '200':
          description: OK
          headers:
            X-Pagination-Total:
              description: Total number of matching issues
              schema:
                type: string
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/issues.Issue'
        '400':
          description: Bad Request
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/issues.ErrorResponse'
        '401':
          description: Unauthorized
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/issues.ErrorResponse'
        '403':
          description: Forbidden
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/issues.ErrorResponse'
        '500':
          description: Internal Server Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/issues.ErrorResponse'
      security:
        - API Key: []
        - Tenant ID: []
        - Bearer Auth: []
components:
  schemas:
    issues.Issue:
      type: object
      properties:
        actions:
          type: object
        auto_resolution_evidence:
          type: object
        auto_resolution_state:
          description: >-
            Nil unless eligible: "auto_close" or "prompt". Evidence carries the
            deciding gate.
          type: string
        created_at:
          type: string
        description:
          type: string
        evidence:
          description: Nil for the trace-list issues that are the norm.
          anyOf:
            - allOf:
                - $ref: '#/components/schemas/issues.Evidence'
            - type: 'null'
        first_seen_at:
          type: string
        fix_branch:
          description: >-
            Legacy: branch of the oldest fix in the board's oldest connected
            repository.
          type: string
        fix_dispatched_at:
          type: string
        fix_pr_number:
          type: integer
        fix_prompt:
          description: >-
            Issue-level: the problem every fix shares, and the last time a fix
            run

            was dispatched for this issue — one run works several fixes.
          type: string
        fix_verification:
          $ref: '#/components/schemas/issues.IssueFixVerification'
        fixes:
          description: Newest first.
          type: array
          items:
            $ref: '#/components/schemas/issues.Fix'
        id:
          type: string
        last_seen_at:
          type: string
        linear_context:
          $ref: '#/components/schemas/issues.LinearContext'
        linear_sync:
          $ref: '#/components/schemas/issues.LinearSync'
        name:
          type: string
        proposed_context_fixes:
          type: array
          items:
            type: object
        proposed_examples:
          type: array
          items:
            type: object
        proposed_fix:
          type: string
        proposed_prompt_fixes:
          type: array
          items:
            type: object
        recurrences_since_watching:
          description: >-
            RecurrencesSinceWatching counts linked traces whose run start_time
            is after

            watching_since — i.e. recurrences observed during the current watch
            period.
          type: integer
        session_id:
          type: string
        severity:
          $ref: '#/components/schemas/issues.Severity'
        status:
          $ref: '#/components/schemas/issues.Status'
        tags:
          items:
            type: string
          type: array
        tenant_id:
          type: string
        traces:
          type: object
        updated_at:
          type: string
        validation_result:
          $ref: '#/components/schemas/issues.IssueValidationResult'
        watching_since:
          type: string
    issues.ErrorResponse:
      type: object
      properties:
        error:
          type: string
    issues.Evidence:
      type: object
      required:
        - type
      properties:
        series:
          $ref: '#/components/schemas/issues.SeriesEvidence'
        type:
          $ref: '#/components/schemas/issues.EvidenceType'
    issues.IssueFixVerification:
      type: object
      properties:
        attempt:
          type: integer
        baseline_experiment_id:
          type: string
          format: uuid
        dataset_id:
          type: string
          format: uuid
        parent_deployment_id:
          type: string
          format: uuid
        preview_deployment_id:
          type: string
          format: uuid
        preview_experiment_id:
          type: string
          format: uuid
        reason:
          type: string
        root_trace_ids:
          items:
            type: string
          type: array
        status:
          type: string
          enum:
            - awaiting_preview
            - verifying
            - passed
            - failed
            - inconclusive
            - timeout
            - error
        updated_at:
          type: string
          format: date-time
    issues.Fix:
      type: object
      required:
        - branch
        - created_at
        - id
        - pr_number
        - provider
        - provider_web_base_url
        - repo_url
        - updated_at
      properties:
        branch:
          anyOf:
            - type: string
            - type: 'null'
        created_at:
          type: string
          format: date-time
        id:
          type: string
        pr_number:
          anyOf:
            - type: integer
            - type: 'null'
        provider:
          enum:
            - github
            - gitlab
          allOf:
            - $ref: '#/components/schemas/repohost.Provider'
        provider_web_base_url:
          description: >-
            ProviderWebBaseURL is the instance the fix was opened on; null on
            GitHub fixes from before it was recorded.
          anyOf:
            - type: string
            - type: 'null'
        repo_url:
          type: string
        updated_at:
          type: string
          format: date-time
    issues.LinearContext:
      type: object
      properties:
        github_pr_urls:
          items:
            type: string
          type: array
        workflow_state:
          type: string
    issues.LinearSync:
      type: object
      properties:
        identifier:
          type: string
        issue_id:
          type: string
        last_attempted_at:
          type: string
          format: date-time
        last_error:
          type: string
        last_synced_at:
          type: string
          format: date-time
        linear_issue_id:
          type: string
        state:
          type: string
          enum:
            - pending
            - synced
            - failed
            - auth_required
            - paused
        url:
          type: string
    issues.Severity:
      type: integer
      enum:
        - 0
        - 1
        - 2
        - 3
      x-enum-varnames:
        - SeverityUrgent
        - SeverityHigh
        - SeverityMed
        - SeverityLow
    issues.Status:
      type: string
      enum:
        - open
        - fixing
        - watching
        - completed
        - ignored
      x-enum-varnames:
        - StatusOpen
        - StatusFixing
        - StatusWatching
        - StatusCompleted
        - StatusIgnored
    issues.IssueValidationResult:
      type: object
      properties:
        active_revision_id:
          type: string
          format: uuid
        baseline_experiment_id:
          type: string
          format: uuid
        completed_at:
          type: string
          format: date-time
        dataset_id:
          type: string
          format: uuid
        deployment_id:
          type: string
          format: uuid
        outcome:
          type: string
          enum:
            - reproduced
            - not_reproduced
            - inconclusive
            - error
        reason:
          type: string
        root_trace_ids:
          items:
            type: string
          type: array
    issues.SeriesEvidence:
      type: object
      required:
        - metric_definition
      properties:
        metric_definition:
          $ref: '#/components/schemas/runsanalytics.MetricDefinition'
        run_filter:
          description: Narrows what is measured; the renderer ANDs its root scope over it.
          type: string
        window_end:
          type: string
          format: date-time
        window_start:
          description: >-
            The view the chart opens at, not a clamp. Start alone renders start
            -> now.
          type: string
          format: date-time
    issues.EvidenceType:
      type: string
      enum:
        - series
      x-enum-varnames:
        - EvidenceTypeSeries
    repohost.Provider:
      type: string
      enum:
        - github
        - gitlab
      x-enum-varnames:
        - GitHub
        - GitLab
    runsanalytics.MetricDefinition:
      type: object
      required:
        - type
      properties:
        denominator:
          $ref: '#/components/schemas/runsanalytics.ScalarMetricDefinition'
        entity:
          description: >-
            Entity selects what a type=count metric counts. Only valid when
            type=count;

            defaults to MetricEntityRun. entity=feedback requires
            params.feedback_key

            and counts individual feedback records rather than runs.
          allOf:
            - $ref: '#/components/schemas/runsanalytics.MetricEntity'
        field:
          $ref: '#/components/schemas/runsanalytics.MetricField'
        numerator:
          description: Numerator and Denominator are required when type=ratio.
          allOf:
            - $ref: '#/components/schemas/runsanalytics.ScalarMetricDefinition'
        params:
          description: percentile p or histogram bucket_count
          allOf:
            - $ref: '#/components/schemas/runsanalytics.MetricParams'
        type:
          description: >-
            histogram is reserved and rejected; the tag publishes what is
            accepted.
          enum:
            - count
            - sum
            - avg
            - min
            - max
            - percentile
            - ratio
          allOf:
            - $ref: '#/components/schemas/runsanalytics.MetricType'
    runsanalytics.ScalarMetricDefinition:
      type: object
      required:
        - type
      properties:
        entity:
          description: >-
            Entity selects what a type=count metric counts. Only valid when
            type=count;

            defaults to MetricEntityRun. entity=feedback requires
            params.feedback_key

            and counts individual feedback records rather than runs.
          allOf:
            - $ref: '#/components/schemas/runsanalytics.MetricEntity'
        field:
          $ref: '#/components/schemas/runsanalytics.MetricField'
        filter:
          type: string
        params:
          description: required when type=percentile
          allOf:
            - $ref: '#/components/schemas/runsanalytics.MetricParams'
        type:
          description: An operand is non-composite, so ratio is rejected here too.
          enum:
            - count
            - sum
            - avg
            - min
            - max
            - percentile
          allOf:
            - $ref: '#/components/schemas/runsanalytics.MetricType'
    runsanalytics.MetricEntity:
      type: string
      enum:
        - run
        - feedback
      x-enum-varnames:
        - MetricEntityRun
        - MetricEntityFeedback
    runsanalytics.MetricField:
      type: string
      enum:
        - latency_seconds
        - first_token_seconds
        - total_tokens
        - prompt_tokens
        - completion_tokens
        - total_cost
        - prompt_cost
        - completion_cost
        - feedback_score
        - prompt_token_details.cache_creation
        - prompt_token_details.cache_read
        - prompt_token_details.ephemeral_1h_input_tokens
        - prompt_token_details.ephemeral_5m_input_tokens
        - prompt_token_details.audio
        - prompt_token_details.image
        - prompt_token_details.video
        - completion_token_details.reasoning
        - completion_token_details.audio
        - completion_token_details.image
        - completion_token_details.video
        - prompt_cost_details.cache_creation
        - prompt_cost_details.cache_read
        - prompt_cost_details.ephemeral_1h_input_tokens
        - prompt_cost_details.ephemeral_5m_input_tokens
        - prompt_cost_details.audio
        - prompt_cost_details.image
        - prompt_cost_details.video
        - completion_cost_details.reasoning
        - completion_cost_details.audio
        - completion_cost_details.image
        - completion_cost_details.video
      x-enum-varnames:
        - MetricFieldLatencySeconds
        - MetricFieldFirstTokenSeconds
        - MetricFieldTotalTokens
        - MetricFieldPromptTokens
        - MetricFieldCompletionTokens
        - MetricFieldTotalCost
        - MetricFieldPromptCost
        - MetricFieldCompletionCost
        - MetricFieldFeedbackScore
        - MetricFieldPromptTokenDetailsCacheCreation
        - MetricFieldPromptTokenDetailsCacheRead
        - MetricFieldPromptTokenDetailsEphemeral1H
        - MetricFieldPromptTokenDetailsEphemeral5M
        - MetricFieldPromptTokenDetailsAudio
        - MetricFieldPromptTokenDetailsImage
        - MetricFieldPromptTokenDetailsVideo
        - MetricFieldCompletionTokenDetailsReasoning
        - MetricFieldCompletionTokenDetailsAudio
        - MetricFieldCompletionTokenDetailsImage
        - MetricFieldCompletionTokenDetailsVideo
        - MetricFieldPromptCostDetailsCacheCreation
        - MetricFieldPromptCostDetailsCacheRead
        - MetricFieldPromptCostDetailsEphemeral1H
        - MetricFieldPromptCostDetailsEphemeral5M
        - MetricFieldPromptCostDetailsAudio
        - MetricFieldPromptCostDetailsImage
        - MetricFieldPromptCostDetailsVideo
        - MetricFieldCompletionCostDetailsReasoning
        - MetricFieldCompletionCostDetailsAudio
        - MetricFieldCompletionCostDetailsImage
        - MetricFieldCompletionCostDetailsVideo
    runsanalytics.MetricParams:
      type: object
      properties:
        bucket_count:
          type: integer
        feedback_key:
          type: string
        p:
          type: number
    runsanalytics.MetricType:
      type: string
      enum:
        - count
        - sum
        - avg
        - min
        - max
        - percentile
        - ratio
        - histogram
      x-enum-varnames:
        - MetricTypeCount
        - MetricTypeSum
        - MetricTypeAvg
        - MetricTypeMin
        - MetricTypeMax
        - MetricTypePercentile
        - MetricTypeRatio
        - MetricTypeHistogram
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

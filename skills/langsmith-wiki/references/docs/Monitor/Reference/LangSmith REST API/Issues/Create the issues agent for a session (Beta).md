# Create the issues agent for a session (Beta)

> **Beta:** This endpoint is in active development and may change without notice.

Configures the issues agent for the given tracer session and enqueues
the initial scan. Fails if an agent already exists for the session.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json post /api/v1/platform/sessions/{session_id}/issues-agent
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
  /api/v1/platform/sessions/{session_id}/issues-agent:
    post:
      tags:
        - issues-agent
      summary: Create the issues agent for a session (Beta)
      description: >-
        **Beta:** This endpoint is in active development and may change without
        notice.


        Configures the issues agent for the given tracer session and enqueues

        the initial scan. Fails if an agent already exists for the session.
      parameters:
        - description: Tracer session ID (UUID)
          name: session_id
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/agent.CreateIssuesAgentRequest'
      responses:
        '201':
          description: Created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/agent.IssuesAgent'
        '400':
          description: Bad Request
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/agent.ErrorResponse'
        '401':
          description: Unauthorized
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/agent.ErrorResponse'
        '403':
          description: Forbidden
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/agent.ErrorResponse'
        '409':
          description: Conflict
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/agent.ErrorResponse'
        '500':
          description: Internal Server Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/agent.ErrorResponse'
      security:
        - API Key: []
        - Tenant ID: []
        - Bearer Auth: []
components:
  schemas:
    agent.CreateIssuesAgentRequest:
      type: object
      properties:
        analysis_level:
          description: >-
            AnalysisLevel is how thoroughly Engine monitors the project:
            "standard"

            (the default), "reduced" (fewer traces at lower cost), or "expanded"
            (more

            traces per run, for projects with enough tracing volume). Omit for

            "standard".
          type: string
          enum:
            - standard
            - reduced
            - expanded
        auto_open_fix_pr:
          description: >-
            AutoOpenFixPR opens a pull request for every fix the agent

            produces — one per repository it changed — instead of waiting for
            one to

            be opened from the issue. Has no effect until the board tracks a

            repository, since a fix has nowhere to open. Omit for false.
          type: boolean
        context_hub_repo_handle:
          type: string
        github_base_branch:
          description: 'Legacy: applies to the repo github_repo_url names.'
          type: string
        github_repo_subdir:
          description: 'Legacy: applies to the repo github_repo_url names.'
          type: string
        github_repo_url:
          description: 'Legacy: treated as a one-entry github_repos list.'
          type: string
        github_repos:
          description: Created with the board. Wins over the deprecated fields below.
          type: array
          items:
            $ref: '#/components/schemas/agent.GithubRepoInput'
        priorities:
          items:
            type: string
          type: array
        run_filter:
          description: Runs-filter-DSL trace scope; omit/null/empty for no scope.
          type: string
    agent.IssuesAgent:
      type: object
      properties:
        agent_overview_accepted:
          type: boolean
        analysis_level:
          description: >-
            AnalysisLevel controls coverage vs cost: "standard" (default),
            "reduced"

            (one scan a day, fewer traces per scan), or "expanded" (2x traces
            per

            run). Stored NULL in the DB means standard; reads always return a

            concrete value.
          type: string
          enum:
            - standard
            - reduced
            - expanded
        auto_open_fix_pr:
          description: >-
            When true, every fix run on this board opens a pull request instead
            of

            parking the fix for someone to publish. Defaults to false.
          type: boolean
        context_hub_repo_handle:
          type: string
        created_at:
          type: string
        cron_enabled:
          type: boolean
        cron_schedule:
          type: string
        engine_version:
          type: string
        github_base_branch:
          description: 'Legacy: aliases the oldest GitHub entry in GithubRepos.'
          type: string
        github_repo_subdir:
          description: 'Legacy: aliases the oldest GitHub entry in GithubRepos.'
          type: string
        github_repo_url:
          description: 'Legacy: aliases the oldest GitHub entry in GithubRepos.'
          type: string
        github_repos:
          type: array
          items:
            $ref: '#/components/schemas/agent.GithubRepo'
        id:
          type: string
        issue_count:
          type: integer
        latest_run_id:
          type: string
        latest_thread_id:
          description: >-
            IDs of the latest run on LangSmith Deployments; NULL until first
            trigger.
          type: string
        linear_available:
          type: boolean
        linear_integration:
          $ref: '#/components/schemas/agent.LinearIntegration'
        linear_sync_health:
          $ref: '#/components/schemas/agent.LinearSyncHealth'
        preview_verify_enabled:
          description: >-
            PreviewVerifyEnabled lets this board's fix runs use preview
            deployments

            when issue validation is enabled for its tracing project.
          type: boolean
        preview_verify_no_trigger:
          description: >-
            PreviewVerifyNoTrigger tells fix verification not to request a
            preview.

            The deployment builds one itself for the fix commit.
          type: boolean
        priorities:
          items:
            type: string
          type: array
        red_team_target:
          description: >-
            RedTeamTarget is the external endpoint red-team runs probe instead
            of

            the validation deployment, or null when none is configured.
          anyOf:
            - allOf:
                - $ref: '#/components/schemas/agent.RedTeamTargetView'
            - type: 'null'
        run_filter:
          description: >-
            RunFilter is a runs-filter-DSL string scoping which traces Engine
            analyzes

            (prompt guidance, not an enforced query). NULL = no scope. Clamped
            by

            validateRunFilter.
          type: string
        selected_trace_count:
          description: |-
            Compatibility alias for selected_trace_count_last_14_days.
            Deprecated: use selected_trace_count_last_14_days.
          type: integer
          deprecated: true
        selected_trace_count_last_14_days:
          description: The number of traces Engine inspected in the last 14 days.
          type: integer
        selected_trace_count_last_7_days:
          description: The number of traces Engine inspected in the last 7 days.
          type: integer
        session_agent_overview_repo_id:
          type: string
        session_id:
          type: string
        session_lcu_spend_limit_monthly:
          description: >-
            SessionLCUSpendLimitMonthly is the per-project monthly Engine LCU
            spend

            limit: NULL/negative = no limit; 0 or positive = monthly cap (spend
            is

            never negative, so a cap of 0 always reads as reached). Enforced in

            addition to (and independently of) the org-level limit. Serialized
            as a

            string to preserve NUMERIC(28,6) precision.
          type: string
        session_name:
          description: JOINed from tracer_session
          type: string
        target_auth:
          $ref: '#/components/schemas/agent.TargetAuthStatus'
        tenant_id:
          type: string
        tenant_name:
          description: >-
            JOINed from tenants (workspace label); resolved server-side so the
            org-admin list can label rows across workspaces the caller isn't a
            member of
          type: string
        updated_at:
          type: string
        user_instructions:
          description: >-
            User-owned freeform preferences. Engine reads this as authoritative

            context and reconciles it into the Agent Overview on the next scan,
            but

            never edits it. NULL when the user hasn't set any.
          type: string
        validation_deployment_id:
          description: >-
            ValidationDeploymentID selects the deployment used for baseline
            replay

            and as the parent of fix-verification previews.
          type: string
    agent.ErrorResponse:
      type: object
      properties:
        error:
          type: string
    agent.GithubRepoInput:
      type: object
      properties:
        base_branch:
          type: string
        provider:
          description: Omitted means GitHub.
          enum:
            - github
            - gitlab
          allOf:
            - $ref: '#/components/schemas/repohost.Provider'
        repo_url:
          type: string
        subdir:
          type: string
    agent.GithubRepo:
      type: object
      properties:
        base_branch:
          type: string
        created_at:
          type: string
          format: date-time
        id:
          type: string
        provider:
          enum:
            - github
            - gitlab
          allOf:
            - $ref: '#/components/schemas/repohost.Provider'
        repo_url:
          type: string
        subdir:
          type: string
        updated_at:
          type: string
          format: date-time
    agent.LinearIntegration:
      type: object
      properties:
        enabled:
          type: boolean
        project_id:
          type: string
        project_name:
          type: string
        team_id:
          type: string
        team_key:
          type: string
        team_name:
          type: string
        workspace_id:
          type: string
        workspace_name:
          type: string
    agent.LinearSyncHealth:
      type: object
      properties:
        auth_required:
          type: integer
        failed:
          type: integer
        paused:
          type: integer
        pending:
          type: integer
        synced:
          type: integer
    agent.RedTeamTargetView:
      type: object
      properties:
        auth:
          description: Auth describes the headers sent to this endpoint, and only to it.
          allOf:
            - $ref: '#/components/schemas/agent.TargetAuthStatus'
        kind:
          description: >-
            Kind is the protocol the endpoint speaks: an A2A agent, or an HTTP
            API

            described by an OpenAPI spec.
          type: string
          enum:
            - a2a
            - openapi
        openapi_operations:
          description: |-
            OpenAPIOperations are the operations probes may call on an OpenAPI
            target, by operationId or as "METHOD /path".
          type: array
          items:
            type: string
        url:
          type: string
    agent.TargetAuthStatus:
      type: object
      properties:
        has_unreadable_credentials:
          description: >-
            True when a credential is stored but cannot be read back, so the UI
            can

            offer to replace it instead of showing an unconfigured board.
          type: boolean
        header_names:
          items:
            type: string
          type: array
    repohost.Provider:
      type: string
      enum:
        - github
        - gitlab
      x-enum-varnames:
        - GitHub
        - GitLab
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

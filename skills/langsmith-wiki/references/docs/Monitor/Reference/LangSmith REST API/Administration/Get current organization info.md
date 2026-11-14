# Get current organization info

> Returns organization info for the authenticated user's current organization.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json get /api/v1/platform/orgs/current/info
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
  /api/v1/platform/orgs/current/info:
    get:
      tags:
        - Organizations
      summary: Get current organization info
      description: >-
        Returns organization info for the authenticated user's current
        organization.
      parameters: []
      responses:
        '200':
          description: Organization info
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/orgs.OrganizationInfo'
        '400':
          description: Invalid organization ID
          content:
            application/json:
              schema:
                type: object
                additionalProperties:
                  type: string
        '401':
          description: Unauthorized
          content:
            application/json:
              schema:
                type: object
                additionalProperties:
                  type: string
        '500':
          description: Internal server error
          content:
            application/json:
              schema:
                type: object
                additionalProperties:
                  type: string
      security:
        - API Key: []
        - Organization ID: []
        - Bearer Auth: []
components:
  schemas:
    orgs.OrganizationInfo:
      type: object
      properties:
        api_key_creation_from_api_keys_enabled:
          type: boolean
        avatar_url:
          anyOf:
            - type: string
            - type: 'null'
        byoc_create_saas_workspace_enabled:
          type: boolean
        can_export_usage_backfill:
          type: boolean
        config:
          $ref: '#/components/schemas/authn.OrganizationConfig'
        default_sso_provision:
          type: boolean
        disabled:
          type: boolean
        disabled_model_providers:
          items:
            type: string
          type: array
        display_name:
          type: string
        engine_enabled:
          type: boolean
        engine_lcu_spend_limit_monthly:
          description: >-
            EngineLCUSpendLimitMonthly is the org admin (Layer 3) monthly Engine
            LCU spend

            limit; null means the admin set no limit. The effective enforced
            limit is the

            minimum of this and the finance/plan limits carried on Config.
          type: string
        id:
          type: string
        invites_enabled:
          type: boolean
        ip_allowlist:
          items:
            type: string
          type: array
        ip_allowlist_enabled:
          type: boolean
        is_personal:
          type: boolean
        is_sso_user:
          type: boolean
        jit_provisioning_enabled:
          type: boolean
        llm_auth_proxy_allowed_urls:
          items:
            type: string
          type: array
        llm_auth_proxy_enabled:
          type: boolean
        llm_auth_proxy_jwt_audience:
          type: string
        managed_eval_terms_accepted_at:
          description: >-
            ManagedEvalTermsAcceptedAt is the raw ISO 8601 timestamp string from
            the

            config JSONB of when an org admin accepted the tuned evaluator
            terms;

            null if never accepted. Returned verbatim so the value is
            byte-identical

            to the smith-backend implementation under weighted routing.
          type: string
        managed_evals_enabled:
          description: >-
            ManagedEvalsEnabled is the org-level consent flag for tuned
            evaluators

            (evaluators that spend a LangChain-held provider key).
          type: boolean
        marketplace_payouts_enabled:
          type: boolean
        max_api_key_expiry_days:
          type: integer
        max_pat_expiry_days:
          type: integer
        max_service_key_expiry_days:
          type: integer
        max_tracing_key_expiry_days:
          anyOf:
            - type: integer
            - type: 'null'
        member_disabled:
          type: boolean
        oidc_login_enabled:
          type: boolean
          default: false
        oidc_sso_available:
          type: boolean
          default: false
        org_role_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
        org_role_name:
          anyOf:
            - allOf:
                - $ref: '#/components/schemas/orgs.OrganizationRole'
            - type: 'null'
        pat_creation_disabled:
          type: boolean
        permissions:
          items:
            type: string
          type: array
        public_sharing_disabled:
          type: boolean
        reached_max_workspaces:
          type: boolean
        restrict_browser_secrets:
          type: boolean
          default: false
        scim_group_name_separator:
          type: string
        security_contact:
          type: string
        sso_login_slug:
          type: string
        sso_only:
          type: boolean
        tier:
          type: string
        topic_search_enabled:
          type: boolean
          default: false
        workspace_admin_can_invite_to_org:
          type: boolean
    authn.OrganizationConfig:
      type: object
      properties:
        agent_builder_enabled:
          description: >-
            AgentBuilderEnabled indicates whether Agent Builder is enabled for
            the organization.
          type: boolean
        allow_custom_iframes:
          description: >-
            AllowCustomIframes indicates whether to allow custom iframes for
            trace rendering.
          type: boolean
        arbitrary_cost_tracking_enabled:
          description: >-
            ArbitraryCostTrackingEnabled indicates whether arbitrary cost
            tracking flows are enabled
          type: boolean
        byoc_enabled:
          description: Indicates whether this org can provision BYOC data planes.
          type: boolean
        byoc_external_id:
          readOnly: true
          description: >-
            ByocExternalID is the organization's assigned AWS external ID,
            stored only in org config.
          anyOf:
            - type: string
            - type: 'null'
        byoc_max_data_planes:
          description: >-
            ByocMaxDataPlanes is the maximum number of BYOC data planes this org
            may have provisioned at once.
          type: integer
        can_add_seats:
          description: >-
            CanAddSeats indicates whether this org can invite new users based on
            their plan.
          type: boolean
        can_disable_public_sharing:
          description: >-
            CanDisablePublicSharing indicates whether this org can disable
            public sharing of resources like traces, datasets, and prompts.
          type: boolean
        can_restrict_browser_secrets:
          description: >-
            CanRestrictBrowserSecrets indicates whether the org can restrict
            browser-level secrets in the Playground (enterprise-only).
          type: boolean
        can_set_api_key_max_expiry:
          description: >-
            CanSetApiKeyMaxExpiry indicates whether the org can set a maximum
            expiry duration for API keys (enterprise-only).
          type: boolean
        can_use_abac:
          description: >-
            CanUseAbac indicates whether this org can use attribute-based access
            control policies.
          type: boolean
        can_use_audit_logs:
          description: >-
            CanUseAuditLogs indicates whether this org can use audit logging
            functionality.
          type: boolean
        can_use_bulk_export:
          description: CanUseBulkExport indicates whether this org can create bulk exports.
          type: boolean
        can_use_langgraph_cloud:
          description: >-
            CanUseLanggraphCloud indicates whether this org can use LangGraph
            Platform.
          type: boolean
        can_use_llm_auth_proxy:
          description: >-
            CanUseLLMAuthProxy indicates whether the org can use the LLM auth
            proxy (enterprise-only).
          type: boolean
        can_use_rbac:
          description: >-
            CanUseRbac indicates whether this org can create new users using
            roles based on their plan.
          type: boolean
        can_use_saml_sso:
          description: CanUseSamlSso indicates whether this org can configure SAML SSO.
          type: boolean
        clio_enabled:
          description: CLIOEnabled indicates whether CLIO is enabled for this org.
          type: boolean
        code_evaluator_execution_batch_size:
          description: >-
            CodeEvaluatorExecutionBatchSize is a per-org override for how many
            code-evaluator

            executions are grouped into a single ACE /execute request. nil uses
            the global

            default (RUN_RULES_CODE_EXECUTE_BATCH_SIZE). Consumed only by
            smith-backend; carried

            here so the value survives the org-config JSON round-trip into the
            Python auth payload.
          type: integer
        datadog_rum_session_sample_rate:
          description: >-
            DatadogRumSessionSampleRate indicates the sampling rate for datadog
            RUM sessions.
          type: integer
        demo_lgp_new_graph_enabled:
          description: >-
            DemoLgpNewGraphEnabled indicates whether this org can use the demo
            page for creating new graphs.
          type: boolean
        dev_zero_deployments_enabled:
          description: >-
            DevZeroDeploymentsEnabled indicates whether the org can create
            development deployments that scale to zero.
          type: boolean
        enable_align_evaluators:
          description: >-
            EnableAlignEvaluators indicates whether to enable the align
            evaluators flow for this org.
          type: boolean
        enable_burndown_vs_commit_view:
          description: >-
            Deprecated: EnableBurndownVsCommitView is retained for backward
            compatibility and is always false; contract-usage visibility is no
            longer gated on it.
          type: boolean
        enable_granular_usage_reporting:
          description: >-
            EnableGranularUsageReporting indicates whether the org can use
            granular usage reporting.
          type: boolean
        enable_langgraph_pricing:
          description: >-
            EnableLanggraphPricing indicates whether to show Agent marketplace
            in Langgraph tab.
          type: boolean
        enable_lgp_listeners_page:
          description: >-
            EnableLgpListenersPage indicates whether the lgp listeners page
            should be shown
          type: boolean
        enable_markdown_in_tracing:
          description: >-
            EnableMarkdownInTracing indicates whether markdown is enabled in
            tracing
          type: boolean
        enable_pricing_redesign:
          description: >-
            EnablePricingRedesign indicates whether the pricing redesign is
            enabled
          type: boolean
        enable_querying_v2_endpoints:
          description: >-
            EnableQueryingV2Endpoints indicates whether to enable the querying
            v2 endpoints for this org.
          type: boolean
        enable_run_tree_streaming:
          description: >-
            EnableRunTreeStreaming indicates whether to enable the run tree
            streaming feature for this org.
          type: boolean
        enable_thread_view_playground:
          description: >-
            EnableThreadViewPlayground indicates whether to allow opening
            top-level thread view runs in the playground.
          type: boolean
        enable_threads_improvements:
          description: >-
            EnableThreadsImprovements indicates whether to enable the threads
            improvements feature for this org.
          type: boolean
        engine_default_enabled:
          description: >-
            EngineDefaultEnabled is the plan-level Engine entitlement. An
            explicit false

            disables Engine for the organization outright; true and nil both
            defer to the

            organization's own engine_enabled setting.
          type: boolean
        engine_lcu_spend_limit_monthly:
          description: >-
            EngineLCUSpendLimitMonthly is an optional Metronome-set monthly LCU
            spend limit

            for Engine. nil means no limit at this layer. Both the Metronome
            plan and customer

            custom fields use this single key; the plan-then-customer config
            merge means the

            customer value (when set) overwrites the plan value, so only the
            resolved value

            arrives here. The effective enforced limit is the minimum of this
            and the org admin

            limit (organizations.engine_lcu_spend_limit_monthly).
          type: number
        fleet_builtin_models_enabled:
          description: >-
            FleetBuiltinModelsEnabled indicates whether the org can use Fleet's
            served

            built-in models (the Fast/Pro/Max tiers). Resolved from the
            Metronome

            plan/customer custom field, falling back to organizations.config;
            code

            default false (paid feature, fail-closed).
          type: boolean
        fleet_lcu_spend_limit_monthly:
          description: >-
            FleetLCUSpendLimitMonthly caps an org's monthly Fleet LCU spend,
            resolved from

            Metronome custom fields. nil or negative means unlimited; 0 blocks
            all runs.
          type: number
        gateway_pii_redaction_enabled:
          description: |-
            GatewayPIIRedactionEnabled indicates whether this org can use PII
            detection/redaction inside gateway data protection (guard) policies.
            When this is off, PII-configured guard policies are unavailable as a
            whole. Set by Metronome entitlement, not admin-patchable.
          type: boolean
        ip_allowlist_enabled:
          description: >-
            IPAllowlistEnabled indicates whether this org can configure and
            enforce IP allowlists.

            Set by Metronome entitlement, not admin-patchable.
          type: boolean
        is_anonymous:
          description: >-
            IsAnonymous, when true, restricts members to viewing only themselves
            in

            member-listing endpoints.
          type: boolean
        kv_dataset_message_support:
          description: >-
            KvDatasetMessageSupport indicates whether to use the new messages
            experience for KV datasets.
          type: boolean
        langchain_provider_spend_limit_monthly:
          description: >-
            LangChainProviderSpendLimitMonthly caps monthly at-cost Connect via
            LangSmith

            spend (USD). nil means unset, -1 means unlimited, and any other
            non-positive

            value blocks usage.
          type: number
        langgraph_deploy_own_cloud_enabled:
          description: >-
            LangGraphDeployOwnCloudEnabled indicates whether the org can deploy
            LangGraph cloud to their own cloud.
          type: boolean
        langgraph_enterprise_enabled:
          description: >-
            LangGraphEnterpriseEnabled indicates whether the org has access to
            LangGraph Enterprise features.
          type: boolean
        langgraph_remote_reconciler_enabled:
          description: >-
            LangGraphRemoteReconcilerEnabled indicates whether an org's
            LangGraph deployments are reconciled via a remote reconciler
            instance.
          type: boolean
        langsmith_alerts_poc_enabled:
          description: >-
            LangsmithAlertsPocEnabled indicates whether to enable the legacy
            alerts POC for this org.
          type: boolean
        langsmith_deployment_distributed_runtime_enabled:
          description: >-
            LangSmithDeploymentDistributedRuntimeEnabled indicates whether
            distributed runtime is enabled for the organization.
          type: boolean
        langsmith_deployment_dr_enabled_dev:
          type: boolean
        lgp_templates_enabled:
          description: >-
            LgpTemplatesEnabled indicates whether to enable LGP templates for
            this org.
          type: boolean
        llm_gateway_enabled:
          description: |-
            LLMGatewayEnabled indicates whether this org can use the LLM Gateway
            (admin UI and gateway policies).
          type: boolean
        lmt_enabled:
          description: >-
            LMTEnabled indicates whether this org's plan entitles it to use
            LangSmith

            Managed Tools. Set by Metronome entitlement and required for all

            Managed Tools APIs and MCP requests. Unset or false blocks access.
          type: boolean
        lmt_lsu_spend_limit_monthly:
          description: >-
            LMTLSUSpendLimitMonthly caps an org's monthly Managed Tools LSU
            spend,

            resolved from Metronome custom fields. Unset or zero blocks usage.

            Negative means unlimited; positive values cap monthly LSU usage.

            Per-org only, with no environment default.
          anyOf:
            - type: number
            - type: 'null'
        max_agent_builder_assistants:
          description: >-
            MaxAgentBuilderAssistants is the maximum number of Agent Builder
            assistants allowed for this org.
          type: integer
        max_agent_builder_runs:
          description: >-
            MaxAgentBuilderRuns is the maximum number of Agent Builder runs per
            month.

            Default is -1 (unlimited). Set to a positive value for a specific
            limit.
          type: integer
        max_free_langgraph_cloud_deployments:
          description: >-
            MaxFreeLanggraphCloudDeployments is the maximum number of free
            LangGraph Platform deployments allowed for this org.
          type: integer
        max_identities:
          description: >-
            MaxIdentities is the maximum number of identities allowed in this
            org.
          type: integer
        max_langgraph_cloud_deployments:
          description: >-
            MaxLanggraphCloudDeployments is the maximum number of LangGraph
            Platform deployments allowed for this org.
          type: integer
        max_prompt_webhooks:
          description: MaxPromptWebhooks limits each org's Prompt Hub webhooks.
          type: integer
        max_sandbox_cpu:
          description: >-
            MaxSandboxCpu is the total CPU cores allowed for sandboxes (e.g.,
            "4", "8").
          type: string
        max_sandbox_memory:
          description: >-
            MaxSandboxMemory is the total memory allowed for sandboxes (e.g.,
            "8Gi", "16Gi").
          type: string
        max_sandboxes:
          description: >-
            MaxSandboxes is the maximum number of sandboxes allowed for this
            org.
          type: integer
        max_workspaces:
          description: >-
            MaxWorkspaces is the maximum number of workspaces allowed in this
            org. -1 means no limit.
          type: integer
        message_view_batch_rate_limit_burst:
          description: >-
            MessageViewBatchRateLimitBurst is a per-org override of the POST
            /v2/traces/messages

            burst. nil (or a value <= 0) uses the global default
            (MESSAGE_VIEW_BATCH_RATE_LIMIT_BURST).
          type: integer
        message_view_batch_rate_limit_per_sec:
          description: >-
            MessageViewBatchRateLimitPerSec is a per-org override of the POST
            /v2/traces/messages

            rate limit, which is applied to each workspace separately. nil (or a
            value <= 0)

            uses the global default (MESSAGE_VIEW_BATCH_RATE_LIMIT_PER_SEC).
          type: integer
        models_connect_via_langsmith_enabled:
          description: >-
            ModelsConnectViaLangSmithEnabled indicates whether the org can use
            Connect via

            LangSmith for /langchain gateway model requests. Defaults false.
          type: boolean
        new_rule_evaluator_creation_version:
          description: New Evaluator Version
          type: integer
        plan_tier:
          description: >-
            PlanTier is the organization's payment plan tier (e.g., "free",
            "developer", "plus", "enterprise").

            Populated from Metronome's __tier custom field during auth
            verification.
          type: string
        playground_evaluator_strategy:
          description: >-
            PlaygroundEvaluatorStrategy indicates the method of running
            evaluators in the playground

            options are "cron", "background", or "sync"
          type: string
        premier_plan_approval_date:
          description: >-
            PremierPlanApprovalDate is the date when the org was approved for
            the premier plan in YYYY-MM-DD format.
          type: string
        prompt_optimization_jobs_enabled:
          description: >-
            PromptOptimizationJobsEnabled indicates whether the org can use the
            prompt optimization jobs feature.
          type: boolean
        sandbox_enabled:
          description: SandboxEnabled indicates whether this org can use sandboxes.
          type: boolean
        sandbox_restricted_egress:
          description: >-
            SandboxRestrictedEgress forces sandboxes onto the curated
            restricted-egress

            allowlist, regardless of access control supplied by the caller.
          type: boolean
        show_playground_prompt_canvas:
          description: >-
            ShowPlaygroundPromptCanvas indicates whether to show the playground
            prompt canvas.
          type: boolean
        show_updated_resource_tags:
          description: >-
            ShowUpdatedResourceTags indicates whether to show updated resource
            tags to users in this org.
          type: boolean
        show_updated_sidenav:
          description: >-
            ShowUpdatedSidenav indicates whether to show updated side nav to
            users in this org.
          type: boolean
        startup_plan_approval_date:
          description: >-
            StartupPlanApprovalDate is the date when the org was approved for
            the startup plan in YYYY-MM-DD format.
          type: string
        tenant_skip_topk_facets:
          description: >-
            TenantSkipTopkFacets indicates whether the tenant should skip topk
            facets in run stats.
          type: boolean
        tuned_evals_enabled:
          description: |-
            TunedEvalsEnabled indicates whether this org's plan entitles it to
            use LangChain Tuned Evaluators. Set by Metronome entitlement.
          type: boolean
        use_exact_search_for_prompts:
          description: >-
            UseExactSearchForPrompts indicates whether to use exact search for
            prompts.
          type: boolean
    orgs.OrganizationRole:
      type: string
      enum:
        - ORGANIZATION_ADMIN
        - ORGANIZATION_OPERATOR
        - ORGANIZATION_USER
        - ORGANIZATION_VIEWER
        - ORGANIZATION_RESTRICTED
        - CUSTOM
      x-enum-varnames:
        - OrganizationRoleAdmin
        - OrganizationRoleOperator
        - OrganizationRoleUser
        - OrganizationRoleViewer
        - OrganizationRoleRestricted
        - OrganizationRoleCustom
  securitySchemes:
    API Key:
      type: apiKey
      in: header
      name: X-API-Key
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

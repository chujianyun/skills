# Update current organization info



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json patch /api/v1/orgs/current/info
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
  /api/v1/orgs/current/info:
    patch:
      tags:
        - orgs
      summary: Update current organization info
      operationId: update_current_organization_info_api_v1_orgs_current_info_patch
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/OrganizationUpdate'
        required: true
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/OrganizationInfo'
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
      security:
        - API Key: []
        - Organization ID: []
        - Bearer Auth: []
components:
  schemas:
    OrganizationUpdate:
      properties:
        display_name:
          type: string
          minLength: 1
          pattern: ^[a-zA-Z0-9\-_ ]+$
          title: Display Name
        public_sharing_disabled:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Public Sharing Disabled
        pat_creation_disabled:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Pat Creation Disabled
        api_key_creation_from_api_keys_enabled:
          type: boolean
          title: Api Key Creation From Api Keys Enabled
        unshare_all:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Unshare All
        jit_provisioning_enabled:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Jit Provisioning Enabled
        workspace_admin_can_invite_to_org:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Workspace Admin Can Invite To Org
        invites_enabled:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Invites Enabled
        max_api_key_expiry_days:
          anyOf:
            - type: integer
            - type: 'null'
          title: Max Api Key Expiry Days
        security_contact:
          anyOf:
            - type: string
              format: email
            - type: 'null'
          title: Security Contact
        max_pat_expiry_days:
          anyOf:
            - type: integer
            - type: 'null'
          title: Max Pat Expiry Days
        max_service_key_expiry_days:
          anyOf:
            - type: integer
            - type: 'null'
          title: Max Service Key Expiry Days
        max_tracing_key_expiry_days:
          anyOf:
            - type: integer
            - type: 'null'
          title: Max Tracing Key Expiry Days
        scim_group_name_separator:
          type: string
          maxLength: 1
          minLength: 1
          title: Scim Group Name Separator
        llm_auth_proxy_enabled:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Llm Auth Proxy Enabled
        llm_auth_proxy_jwt_audience:
          anyOf:
            - type: string
            - type: 'null'
          title: Llm Auth Proxy Jwt Audience
        ip_allowlist:
          anyOf:
            - items:
                type: string
              type: array
            - type: 'null'
          title: Ip Allowlist
        disabled_model_providers:
          anyOf:
            - items:
                type: string
              type: array
            - type: 'null'
          title: Disabled Model Providers
        restrict_browser_secrets:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Restrict Browser Secrets
        byoc_create_saas_workspace_enabled:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Byoc Create Saas Workspace Enabled
        llm_auth_proxy_allowed_urls:
          anyOf:
            - items:
                type: string
              type: array
            - type: 'null'
          title: Llm Auth Proxy Allowed Urls
        topic_search_enabled:
          type: boolean
          title: Topic Search Enabled
          default: false
        engine_enabled:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Engine Enabled
        engine_lcu_spend_limit_monthly:
          anyOf:
            - type: number
            - type: string
              pattern: ^(?!^[-+.]*$)[+-]?0*\d*\.?\d*$
            - type: 'null'
          title: Engine Lcu Spend Limit Monthly
      type: object
      title: OrganizationUpdate
      description: Update organization schema.
    OrganizationInfo:
      properties:
        id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Id
        display_name:
          anyOf:
            - type: string
            - type: 'null'
          title: Display Name
        avatar_url:
          anyOf:
            - type: string
            - type: 'null'
          title: Avatar Url
        config:
          $ref: '#/components/schemas/OrganizationConfig'
        topic_search_enabled:
          type: boolean
          title: Topic Search Enabled
          default: false
        engine_enabled:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Engine Enabled
        engine_lcu_spend_limit_monthly:
          anyOf:
            - type: string
              pattern: ^(?!^[-+.]*$)[+-]?0*\d*\.?\d*$
            - type: 'null'
          title: Engine Lcu Spend Limit Monthly
        is_personal:
          type: boolean
          title: Is Personal
        tier:
          anyOf:
            - $ref: '#/components/schemas/PaymentPlanTier'
            - type: 'null'
        reached_max_workspaces:
          type: boolean
          title: Reached Max Workspaces
          default: false
        permissions:
          items:
            type: string
          type: array
          title: Permissions
          default: []
        org_role_name:
          anyOf:
            - $ref: '#/components/schemas/OrganizationRoles'
            - type: 'null'
        org_role_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Org Role Id
        disabled:
          type: boolean
          title: Disabled
          default: false
        member_disabled:
          type: boolean
          title: Member Disabled
          default: false
        is_sso_user:
          type: boolean
          title: Is Sso User
          default: false
        sso_only:
          type: boolean
          title: Sso Only
          default: false
        jit_provisioning_enabled:
          type: boolean
          title: Jit Provisioning Enabled
          default: true
        invites_enabled:
          type: boolean
          title: Invites Enabled
          default: true
        sso_login_slug:
          anyOf:
            - type: string
            - type: 'null'
          title: Sso Login Slug
        public_sharing_disabled:
          type: boolean
          title: Public Sharing Disabled
          default: false
        pat_creation_disabled:
          type: boolean
          title: Pat Creation Disabled
          default: false
        api_key_creation_from_api_keys_enabled:
          type: boolean
          title: Api Key Creation From Api Keys Enabled
        workspace_admin_can_invite_to_org:
          type: boolean
          title: Workspace Admin Can Invite To Org
          default: false
        byoc_create_saas_workspace_enabled:
          type: boolean
          title: Byoc Create Saas Workspace Enabled
          default: true
        marketplace_payouts_enabled:
          type: boolean
          title: Marketplace Payouts Enabled
          default: false
        default_sso_provision:
          type: boolean
          title: Default Sso Provision
          default: false
        max_api_key_expiry_days:
          anyOf:
            - type: integer
            - type: 'null'
          title: Max Api Key Expiry Days
        security_contact:
          anyOf:
            - type: string
            - type: 'null'
          title: Security Contact
        max_pat_expiry_days:
          anyOf:
            - type: integer
            - type: 'null'
          title: Max Pat Expiry Days
        max_service_key_expiry_days:
          anyOf:
            - type: integer
            - type: 'null'
          title: Max Service Key Expiry Days
        max_tracing_key_expiry_days:
          anyOf:
            - type: integer
            - type: 'null'
          title: Max Tracing Key Expiry Days
        scim_group_name_separator:
          type: string
          title: Scim Group Name Separator
          default: ':'
        can_export_usage_backfill:
          type: boolean
          title: Can Export Usage Backfill
          default: false
        llm_auth_proxy_enabled:
          type: boolean
          title: Llm Auth Proxy Enabled
          default: false
        oidc_login_enabled:
          type: boolean
          title: Oidc Login Enabled
          default: false
        llm_auth_proxy_jwt_audience:
          anyOf:
            - type: string
            - type: 'null'
          title: Llm Auth Proxy Jwt Audience
        ip_allowlist:
          items:
            type: string
          type: array
          title: Ip Allowlist
        ip_allowlist_enabled:
          type: boolean
          title: Ip Allowlist Enabled
          default: false
        disabled_model_providers:
          items:
            type: string
          type: array
          title: Disabled Model Providers
        restrict_browser_secrets:
          type: boolean
          title: Restrict Browser Secrets
          default: false
        llm_auth_proxy_allowed_urls:
          anyOf:
            - items:
                type: string
              type: array
            - type: 'null'
          title: Llm Auth Proxy Allowed Urls
        oidc_sso_available:
          type: boolean
          title: Oidc Sso Available
          default: false
        managed_evals_enabled:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Managed Evals Enabled
        managed_eval_terms_accepted_at:
          anyOf:
            - type: string
            - type: 'null'
          title: Managed Eval Terms Accepted At
      type: object
      required:
        - config
        - is_personal
      title: OrganizationInfo
      description: >-
        Information about an organization.


        IMPORTANT: Keep in sync with Go OrganizationInfo in
        smith-go/orgs/handler.go

        while both implementations are in use (weighted routing rollout).
    HTTPValidationError:
      properties:
        detail:
          items:
            type: string
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    OrganizationConfig:
      properties:
        plan_tier:
          anyOf:
            - type: string
            - type: 'null'
          title: Plan Tier
        engine_default_enabled:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Engine Default Enabled
        engine_lcu_spend_limit_monthly:
          anyOf:
            - type: number
            - type: 'null'
          title: Engine Lcu Spend Limit Monthly
        max_identities:
          type: integer
          title: Max Identities
          default: 5
        max_workspaces:
          type: integer
          title: Max Workspaces
          default: 1
        code_evaluator_execution_batch_size:
          anyOf:
            - type: integer
            - type: 'null'
          title: Code Evaluator Execution Batch Size
        message_view_batch_rate_limit_per_sec:
          anyOf:
            - type: integer
            - type: 'null'
          title: Message View Batch Rate Limit Per Sec
        message_view_batch_rate_limit_burst:
          anyOf:
            - type: integer
            - type: 'null'
          title: Message View Batch Rate Limit Burst
        can_use_rbac:
          type: boolean
          title: Can Use Rbac
          default: false
        can_use_abac:
          type: boolean
          title: Can Use Abac
          default: false
        can_use_audit_logs:
          type: boolean
          title: Can Use Audit Logs
          default: false
        can_use_teams:
          type: boolean
          title: Can Use Teams
          default: false
        can_add_seats:
          type: boolean
          title: Can Add Seats
          default: true
        startup_plan_approval_date:
          anyOf:
            - type: string
            - type: 'null'
          title: Startup Plan Approval Date
        partner_plan_approval_date:
          anyOf:
            - type: string
            - type: 'null'
          title: Partner Plan Approval Date
        premier_plan_approval_date:
          anyOf:
            - type: string
            - type: 'null'
          title: Premier Plan Approval Date
        can_disable_public_sharing:
          type: boolean
          title: Can Disable Public Sharing
          default: false
        can_use_langgraph_cloud:
          type: boolean
          title: Can Use Langgraph Cloud
          default: false
        max_langgraph_cloud_deployments:
          type: integer
          title: Max Langgraph Cloud Deployments
          default: 3
        max_free_langgraph_cloud_deployments:
          type: integer
          title: Max Free Langgraph Cloud Deployments
          default: 0
        sandbox_enabled:
          type: boolean
          title: Sandbox Enabled
          default: false
        sandbox_restricted_egress:
          type: boolean
          title: Sandbox Restricted Egress
          default: false
        max_sandboxes:
          type: integer
          title: Max Sandboxes
          default: 10
        max_sandbox_cpu:
          type: string
          title: Max Sandbox Cpu
          default: '200'
        max_sandbox_memory:
          type: string
          title: Max Sandbox Memory
          default: 400Gi
        can_use_saml_sso:
          type: boolean
          title: Can Use Saml Sso
          default: false
        can_use_bulk_export:
          type: boolean
          title: Can Use Bulk Export
          default: false
        show_updated_sidenav:
          type: boolean
          title: Show Updated Sidenav
          default: false
        show_updated_resource_tags:
          type: boolean
          title: Show Updated Resource Tags
          default: false
        kv_dataset_message_support:
          type: boolean
          title: Kv Dataset Message Support
          default: true
        show_playground_prompt_canvas:
          type: boolean
          title: Show Playground Prompt Canvas
          default: false
        allow_custom_iframes:
          type: boolean
          title: Allow Custom Iframes
          default: false
        byoc_enabled:
          type: boolean
          title: Byoc Enabled
          default: false
        byoc_external_id:
          anyOf:
            - type: string
            - type: 'null'
          title: Byoc External Id
          description: >-
            The organization's assigned AWS external ID for BYOC role trust
            policies.
          readOnly: true
        byoc_max_data_planes:
          type: integer
          title: Byoc Max Data Planes
          default: 5
        enable_langgraph_pricing:
          type: boolean
          title: Enable Langgraph Pricing
          default: false
        enable_thread_view_playground:
          type: boolean
          title: Enable Thread View Playground
          default: false
        use_exact_search_for_prompts:
          type: boolean
          title: Use Exact Search For Prompts
          default: false
        langgraph_deploy_own_cloud_enabled:
          type: boolean
          title: Langgraph Deploy Own Cloud Enabled
          default: false
        prompt_optimization_jobs_enabled:
          type: boolean
          title: Prompt Optimization Jobs Enabled
          default: false
        demo_lgp_new_graph_enabled:
          type: boolean
          title: Demo Lgp New Graph Enabled
          default: false
        datadog_rum_session_sample_rate:
          type: integer
          title: Datadog Rum Session Sample Rate
          default: 20
        langgraph_remote_reconciler_enabled:
          type: boolean
          title: Langgraph Remote Reconciler Enabled
          default: false
        langgraph_enterprise_enabled:
          type: boolean
          title: Langgraph Enterprise Enabled
          default: false
        langsmith_alerts_poc_enabled:
          type: boolean
          title: Langsmith Alerts Poc Enabled
          default: true
        tenant_skip_topk_facets:
          type: boolean
          title: Tenant Skip Topk Facets
          default: false
        lgp_templates_enabled:
          type: boolean
          title: Lgp Templates Enabled
          default: false
        enable_align_evaluators:
          type: boolean
          title: Enable Align Evaluators
          default: false
        enable_run_tree_streaming:
          type: boolean
          title: Enable Run Tree Streaming
          default: false
        enable_querying_v2_endpoints:
          type: boolean
          title: Enable Querying V2 Endpoints
          default: false
        enable_threads_improvements:
          type: boolean
          title: Enable Threads Improvements
          default: false
        max_prompt_webhooks:
          type: integer
          title: Max Prompt Webhooks
          default: 1
        playground_evaluator_strategy:
          anyOf:
            - type: string
            - type: 'null'
          title: Playground Evaluator Strategy
          default: sync
        can_set_api_key_max_expiry:
          type: boolean
          title: Can Set Api Key Max Expiry
          default: false
        can_use_llm_auth_proxy:
          type: boolean
          title: Can Use Llm Auth Proxy
          default: false
        can_restrict_browser_secrets:
          type: boolean
          title: Can Restrict Browser Secrets
          default: false
        new_rule_evaluator_creation_version:
          type: integer
          title: New Rule Evaluator Creation Version
          default: 3
        enable_lgp_listeners_page:
          type: boolean
          title: Enable Lgp Listeners Page
          default: false
        clio_enabled:
          type: boolean
          title: Clio Enabled
          default: false
        enable_markdown_in_tracing:
          type: boolean
          title: Enable Markdown In Tracing
          default: false
        enable_pricing_redesign:
          type: boolean
          title: Enable Pricing Redesign
          default: false
        arbitrary_cost_tracking_enabled:
          type: boolean
          title: Arbitrary Cost Tracking Enabled
          default: false
        langsmith_deployment_distributed_runtime_enabled:
          type: boolean
          title: Langsmith Deployment Distributed Runtime Enabled
          default: false
        agent_builder_enabled:
          type: boolean
          title: Agent Builder Enabled
          default: true
        fleet_builtin_models_enabled:
          type: boolean
          title: Fleet Builtin Models Enabled
          default: false
        models_connect_via_langsmith_enabled:
          type: boolean
          title: Models Connect Via Langsmith Enabled
          default: false
        dev_zero_deployments_enabled:
          type: boolean
          title: Dev Zero Deployments Enabled
          default: false
        fleet_lcu_spend_limit_monthly:
          anyOf:
            - type: number
            - type: 'null'
          title: Fleet Lcu Spend Limit Monthly
        langchain_provider_spend_limit_monthly:
          anyOf:
            - type: number
            - type: 'null'
          title: Langchain Provider Spend Limit Monthly
        max_agent_builder_assistants:
          type: integer
          title: Max Agent Builder Assistants
          default: 1000
        enable_granular_usage_reporting:
          type: boolean
          title: Enable Granular Usage Reporting
          default: false
        enable_burndown_vs_commit_view:
          type: boolean
          title: Enable Burndown Vs Commit View
          default: false
          deprecated: true
        max_agent_builder_runs:
          type: integer
          title: Max Agent Builder Runs
          default: -1
        langsmith_deployment_dr_enabled_dev:
          type: boolean
          title: Langsmith Deployment Dr Enabled Dev
          default: false
        ip_allowlist_enabled:
          type: boolean
          title: Ip Allowlist Enabled
          default: false
        llm_gateway_enabled:
          type: boolean
          title: Llm Gateway Enabled
          default: false
        tuned_evals_enabled:
          type: boolean
          title: Tuned Evals Enabled
          default: false
        gateway_pii_redaction_enabled:
          type: boolean
          title: Gateway Pii Redaction Enabled
          default: false
        managed_deep_agents_enabled:
          type: boolean
          title: Managed Deep Agents Enabled
          default: false
        lmt_enabled:
          type: boolean
          title: Lmt Enabled
          default: false
        lmt_lsu_spend_limit_monthly:
          anyOf:
            - type: number
            - type: 'null'
          title: Lmt Lsu Spend Limit Monthly
          description: >-
            Caps an org's monthly Managed Tools LSU spend, resolved from
            Metronome custom fields. Unset or zero blocks usage. Negative means
            unlimited; positive values cap monthly LSU usage. Per-org only, with
            no environment default.
        is_anonymous:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Is Anonymous
      type: object
      title: OrganizationConfig
      description: >-
        Organization level configuration. May include any field that exists in
        tenant config and additional fields.


        Each field's type annotation drives how Metronome custom-field values
        are validated

        when resolving config (see smith-backend's ``_parse_metronome_value``
        and smith-go's

        ``rejectInvalidMetronomeValue``): a value that doesn't fit the annotated
        type is

        dropped and the field keeps whatever value was already resolved for it,
        rather than

        raising. Changing a field's type here changes what Metronome values are
        accepted for it.
    PaymentPlanTier:
      type: string
      enum:
        - no_plan
        - developer
        - developer_01_2026
        - developer_07_2026
        - developer_10_2026
        - plus
        - plus_01_2026
        - plus_07_2026
        - plus_10_2026
        - enterprise
        - developer_legacy
        - plus_legacy
        - free
        - free_07_2026
        - free_10_2026
        - enterprise_legacy
        - startup
        - startup_v0
        - startup_07_2026
        - startup_10_2026
        - partner
        - premier
      title: PaymentPlanTier
    OrganizationRoles:
      type: string
      enum:
        - ORGANIZATION_ADMIN
        - ORGANIZATION_OPERATOR
        - ORGANIZATION_USER
        - ORGANIZATION_VIEWER
        - ORGANIZATION_RESTRICTED
        - CUSTOM
      title: OrganizationRoles
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

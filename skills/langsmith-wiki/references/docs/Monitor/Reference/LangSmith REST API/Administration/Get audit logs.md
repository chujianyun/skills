# Get audit logs

> Retrieve audit log records for the authenticated user's organization in OCSF format.

Requires both start_time and end_time parameters to filter logs within a date range.
Supports cursor-based pagination.

Returns results in OCSF API Activity (Class UID: 6003) format,
which is compatible with security monitoring and SIEM tools.
Reference: https://schema.ocsf.io/1.7.0/classes/api_activity



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json get /api/v1/audit-logs
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
  /api/v1/audit-logs:
    get:
      tags:
        - audit-logs
      summary: Get audit logs
      description: >-
        Retrieve audit log records for the authenticated user's organization in
        OCSF format.


        Requires both start_time and end_time parameters to filter logs within a
        date range.

        Supports cursor-based pagination.


        Returns results in OCSF API Activity (Class UID: 6003) format,

        which is compatible with security monitoring and SIEM tools.

        Reference: https://schema.ocsf.io/1.7.0/classes/api_activity
      operationId: get_audit_logs_api_v1_audit_logs_get
      parameters:
        - name: limit
          in: query
          required: false
          schema:
            type: integer
            maximum: 100
            minimum: 1
            description: Number of items to return
            default: 10
            title: Limit
          description: Number of items to return
        - name: cursor
          in: query
          required: false
          schema:
            anyOf:
              - type: string
              - type: 'null'
            description: Cursor for pagination (base64-encoded JSON string)
            title: Cursor
          description: Cursor for pagination (base64-encoded JSON string)
        - name: workspace_id
          in: query
          required: false
          schema:
            anyOf:
              - type: string
                format: uuid
              - type: 'null'
            description: Filter by workspace ID
            title: Workspace Id
          description: Filter by workspace ID
        - name: start_time
          in: query
          required: true
          schema:
            type: string
            format: date-time
            description: Start datetime (inclusive) in ISO 8601 format
            title: Start Time
          description: Start datetime (inclusive) in ISO 8601 format
        - name: end_time
          in: query
          required: true
          schema:
            type: string
            format: date-time
            description: End datetime (inclusive) in ISO 8601 format
            title: End Time
          description: End datetime (inclusive) in ISO 8601 format
        - name: operations
          in: query
          required: false
          schema:
            anyOf:
              - type: array
                items:
                  $ref: '#/components/schemas/AuditLogOperation'
              - type: 'null'
            description: >-
              Filter by operation names. If omitted, all operations are
              returned.
            title: Operations
          description: Filter by operation names. If omitted, all operations are returned.
        - name: actor_ls_user_ids
          in: query
          required: false
          schema:
            anyOf:
              - items:
                  type: string
                  format: uuid
                type: array
              - type: 'null'
            description: Filter by human actor (ls_user_id).
            title: Actor Ls User Ids
          description: Filter by human actor (ls_user_id).
        - name: actor_api_key_ids
          in: query
          required: false
          schema:
            anyOf:
              - items:
                  type: string
                  format: uuid
                type: array
              - type: 'null'
            description: Filter by API key actor (api_key_id).
            title: Actor Api Key Ids
          description: Filter by API key actor (api_key_id).
        - name: resource_ids
          in: query
          required: false
          schema:
            anyOf:
              - items:
                  type: string
                type: array
              - type: 'null'
            description: >-
              Filter by resource ID. Matches if any resource ID is present on
              the log.
            title: Resource Ids
          description: >-
            Filter by resource ID. Matches if any resource ID is present on the
            log.
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ListAuditLogsOCSFResponse'
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
    AuditLogOperation:
      type: string
      enum:
        - create_api_key
        - delete_api_key
        - create_personal_access_token
        - delete_personal_access_token
        - revoke_personal_access_token
        - reinstate_personal_access_token
        - create_service_key
        - delete_service_key
        - update_service_key
        - create_role
        - update_role
        - delete_role
        - upsert_role_restriction
        - invite_user_to_org
        - invite_users_to_org_batch
        - add_basic_auth_users_to_org
        - update_basic_auth_user
        - delete_org_pending_member
        - update_org_pending_member
        - delete_org_member
        - update_org_member
        - create_sso_settings
        - update_sso_settings
        - delete_sso_settings
        - update_default_sso_provision_organization
        - update_login_methods
        - create_oidc_integration
        - update_oidc_integration
        - delete_oidc_integration
        - create_oidc_sso_settings
        - update_oidc_sso_settings
        - delete_oidc_sso_settings
        - update_organization_info
        - update_business_info
        - update_payment_plan
        - update_payment_method
        - create_payment_setup_intent
        - create_payment_checkout_session
        - confirm_payment_checkout_session
        - create_payment_account_link
        - create_workspace
        - update_workspace
        - delete_workspace
        - add_member_to_workspace
        - add_members_to_workspace_batch
        - delete_workspace_member
        - update_workspace_member
        - delete_workspace_pending_member
        - update_workspace_pending_member
        - read_workspace_encrypted_secrets
        - update_workspace_secrets
        - delete_workspace_secret
        - upsert_workspace_secret
        - read_org_encrypted_secrets
        - update_org_secrets
        - unshare_entities
        - upsert_slack_app_configuration
        - delete_slack_app_configuration
        - upsert_github_app_configuration
        - update_github_app_configuration
        - delete_github_app_configuration
        - upsert_gitlab_connection
        - delete_gitlab_connection
        - set_tenant_handle
        - create_tag_key
        - update_tag_key
        - delete_tag_key
        - create_tag_value
        - update_tag_value
        - delete_tag_value
        - create_tagging
        - delete_tagging
        - create_agent
        - create_agent_environment
        - update_agent
        - delete_agent
        - create_agent_runtime_binding
        - create_agent_environment_api_key
        - delete_agent_environment_api_key
        - create_tracer_session
        - update_tracer_session
        - delete_tracer_session
        - delete_tracer_sessions
        - delete_runs
        - share_run
        - unshare_run
        - share_thread
        - unshare_thread
        - create_dataset
        - create_csv_dataset
        - create_experiment_via_upload
        - create_playground_experiment
        - create_comparative_experiment
        - delete_comparative_experiment
        - delete_dataset
        - delete_datasets
        - update_dataset
        - update_dataset_version
        - update_dataset_splits
        - share_dataset
        - unshare_dataset
        - clone_dataset
        - download_dataset
        - create_example
        - create_examples
        - update_example
        - update_examples
        - update_examples_metadata
        - sync_examples
        - delete_example
        - delete_examples
        - create_bulk_export
        - cancel_bulk_export
        - read_bulk_export_destination
        - create_bulk_export_destination
        - update_bulk_export_destination
        - delete_bulk_export_destination
        - update_ttl_settings
        - update_usage_limit
        - delete_usage_limit
        - create_model_price_map
        - update_model_price_map
        - delete_model_price_map
        - create_chart
        - update_chart
        - delete_chart
        - create_chart_section
        - update_chart_section
        - delete_chart_section
        - clone_chart_section
        - create_org_chart
        - update_org_chart
        - delete_org_chart
        - create_org_chart_section
        - update_org_chart_section
        - delete_org_chart_section
        - create_prompt_webhook
        - update_prompt_webhook
        - delete_prompt_webhook
        - test_prompt_webhook
        - create_deployment
        - update_deployment
        - delete_deployment
        - cancel_deployment_runs
        - create_access_policy
        - delete_access_policy
        - list_access_policies
        - read_access_policy
        - update_access_policy
        - attach_access_policies
        - detach_access_policies
        - read_role_access_policies
        - read_team_access_policies
        - create_team
        - update_team
        - delete_team
        - add_team_members
        - attach_team_access_policy
        - detach_team_access_policy
        - remove_team_member
        - create_team_workspace_grant
        - update_team_workspace_grant
        - delete_team_workspace_grant
        - create_scim_token
        - update_scim_token
        - delete_scim_token
        - create_scim_user
        - update_scim_user
        - delete_scim_user
        - create_scim_group
        - update_scim_group
        - delete_scim_group
        - create_prompt_canvas_quick_action
        - update_prompt_canvas_quick_action
        - delete_prompt_canvas_quick_action
        - create_fleet_usage_limit
        - update_fleet_usage_limit
        - delete_fleet_usage_limit
        - update_credential
        - delete_credential
        - create_experiment_view_override
        - update_experiment_view_override
        - delete_experiment_view_override
        - create_alert_rule
        - update_alert_rule
        - delete_alert_rule
        - test_alert_rule
        - create_forge_configuration
        - update_forge_configuration
        - delete_forge_configuration
        - trigger_forge_configuration
        - add_annotation_queue_reviewer
        - remove_annotation_queue_reviewer
        - create_custom_view
        - update_custom_view
        - delete_custom_view
        - add_items_to_annotation_queue
        - delete_annotation_queue_item
        - update_annotation_queue_item
        - get_annotation_queue_items
        - submit_nps_response
        - submit_product_feedback
        - update_trace_flight_score
        - create_mcp_server
        - update_mcp_server
        - delete_mcp_server
        - register_mcp_server_oauth
        - create_mcp_credential_session
        - invoke_mcp_server
        - invoke_mcp_gateway
        - create_mcp_gateway
        - update_mcp_gateway
        - delete_mcp_gateway
        - refresh_mcp_gateway_tools
        - update_mcp_oidc_connection
        - delete_mcp_oidc_connection
        - create_mcp_profile
        - update_mcp_profile
        - delete_mcp_profile
        - create_agent_policy
        - update_agent_policy
        - delete_agent_policy
        - create_credential
        - read_credential_secret
        - read_credential_oauth2
        - create_oauth_provider
        - update_oauth_provider
        - delete_oauth_provider
        - start_oauth_connection
        - start_agent_auth_secret_input
        - create_agent_auth_connection
        - update_agent_auth_connection
        - delete_agent_auth_connection
        - update_agent_auth_app
        - delete_agent_auth_app
        - create_agent_auth_oidc_integration
        - update_agent_auth_oidc_integration
        - delete_agent_auth_oidc_integration
        - resolve_agent_auth_agent
        - create_agent_auth_app
        - create_tool
        - update_tool
        - delete_tool
        - create_connection
        - update_connection
        - delete_connection
        - create_mcp_vendor_settings
        - update_mcp_vendor_settings
        - delete_mcp_vendor_settings
        - create_evaluator
        - update_evaluator
        - delete_evaluator
        - bulk_delete_evaluators
        - test_evaluator
        - upsert_feature_default_model
        - delete_feature_default_model
        - upsert_feature_disabled_model
        - delete_feature_disabled_model
        - create_fleet_webhook
        - update_fleet_webhook
        - delete_fleet_webhook
        - test_fleet_webhook
        - create_webhook_destination
        - update_webhook_destination
        - delete_webhook_destination
        - test_webhook_destination
        - create_commit
        - create_hub_environment
        - update_hub_environment
        - delete_hub_environment
        - create_directory_commit
        - delete_directory
        - create_gateway_policy
        - update_gateway_policy
        - delete_gateway_policy
        - invoke_gateway
        - purchase_prepaid_gateway_provider_credits
        - create_sandbox_proxy_profile
        - update_sandbox_proxy_profile
        - delete_sandbox_proxy_profile
        - create_sandbox_policy
        - update_sandbox_policy
        - delete_sandbox_policy
        - create_computer_environment
        - update_computer_environment
        - archive_computer_environment
        - update_fleet_feedback
        - delete_fleet_feedback
        - list_sandbox_claims
        - get_sandbox_claim
        - get_sandbox_claim_status
        - create_sandbox_claim
        - update_sandbox_claim
        - delete_sandbox_claim
        - batch_delete_sandbox_claims
        - start_sandbox_claim
        - stop_sandbox_claim
        - generate_sandbox_service_url
        - generate_sandbox_download_url
        - capture_sandbox_snapshot
        - list_sandbox_snapshots
        - get_sandbox_snapshot
        - create_sandbox_snapshot
        - delete_sandbox_snapshot
        - list_sandbox_volumes
        - get_sandbox_volume
        - create_sandbox_volume
        - clone_sandbox_volume
        - update_sandbox_volume
        - delete_sandbox_volume
        - list_sandbox_registries
        - get_sandbox_registry
        - create_sandbox_registry
        - update_sandbox_registry
        - delete_sandbox_registry
        - list_sandbox_functions
        - get_sandbox_function
        - create_sandbox_function
        - update_sandbox_function
        - deploy_sandbox_function
        - delete_sandbox_function
        - generate_sandbox_function_token
        - create_data_plane
        - delete_data_plane
        - update_data_plane
        - create_annotation_queue
        - populate_annotation_queue
        - delete_annotation_queue
        - delete_annotation_queues
        - update_annotation_queue
        - add_runs_to_annotation_queue
        - export_annotation_queue
        - update_annotation_queue_run
        - delete_annotation_queue_run
        - delete_annotation_queue_runs
        - create_annotation_queue_run_status
        - create_annotation_queue_item_status
        - login
        - send_sso_email_confirmation
        - confirm_sso_user_email
        - execute_custom_code
        - generate_dataset
        - evaluate_experiment
        - create_feedback_formula
        - update_feedback_formula
        - delete_feedback_formula
        - create_feedback_config
        - update_feedback_config
        - delete_feedback_config
        - invalidate_mcp_tools_cache
        - mcp_proxy
        - create_onboarding_state
        - update_onboarding_state
        - create_organization
        - delete_pending_organization_invite
        - claim_pending_organization_invite
        - create_playground_settings
        - update_playground_settings
        - delete_playground_settings
        - create_service_account
        - delete_service_account
        - create_tenant
        - create_filter_view
        - update_filter_view
        - rename_filter_view
        - delete_filter_view
        - create_insights_job
        - create_insights_job_config
        - update_insights_job_config
        - delete_insights_job_config
        - update_insights_job
        - delete_insights_job
        - read_charts
        - read_chart_preview
        - read_chart
        - read_chart_section
        - validate_example
        - validate_examples
        - read_shared_delta
        - read_shared_delta_stream
        - generate_shared_dataset_query
        - generate_runs_query
        - read_tracing_dashboard
        - generate_insights_job_config
        - read_dataset_delta
        - delete_pending_workspace_invite
        - claim_pending_workspace_invite
        - list_annotation_queues
        - get_annotation_queue
        - get_annotation_queue_runs
        - get_annotation_queue_run
        - get_annotation_queues_for_run
        - get_annotation_queue_size
        - get_annotation_queue_archived_size
        - get_annotation_queue_total_size
        - resolve_annotation_queue_run
        - get_audit_logs
        - get_sso_settings
        - list_bulk_exports
        - list_bulk_export_destinations
        - get_bulk_export
        - get_bulk_export_runs
        - get_bulk_export_run
        - get_bulk_export_runs_filtered
        - list_chart_sections
        - get_dataset_versions
        - diff_dataset_versions
        - get_dataset_version
        - read_dataset_share_state
        - count_examples
        - list_feedback_formulas
        - get_feedback_formula
        - list_feedback_configs
        - get_mcp_tools
        - mcp_proxy_get
        - get_onboarding_state
        - read_model_price_map
        - list_organizations
        - get_organization_info
        - get_organization_billing_info
        - get_org_dashboard
        - get_company_info
        - list_organization_roles
        - list_permissions
        - list_pending_organization_invites
        - list_org_members
        - get_org_usage
        - get_granular_usage_traces
        - export_granular_usage_traces_csv
        - get_granular_usage_deployments
        - export_granular_usage_deployments_csv
        - export_usage_backfill_csv
        - get_login_methods
        - get_sso_settings_current
        - list_org_service_keys
        - list_org_personal_access_tokens
        - list_all_org_personal_access_tokens
        - list_service_accounts
        - list_filter_views
        - get_filter_view
        - list_insights_jobs
        - list_insights_job_configs
        - get_insights_job
        - get_insights_job_runs
        - get_run_cluster
        - get_usage_limits
        - get_org_usage_limits
        - list_workspaces
        - list_pending_workspace_invites
        - get_workspace_stats
        - list_workspace_members
        - get_shared_tokens
        - get_workspace_usage_limits_info
        - list_tag_keys
        - get_tag_key
        - list_tag_values
        - get_tag_value
        - list_tags
        - list_tags_for_resource
        - list_taggings
        - get_shared_examples_count
        - list_examples
        - get_example
        - get_experiment_view_overrides
        - get_experiment_view_override
        - get_dataset_comparison_view
        - stream_dataset_comparison_view
        - stream_feedback_delta
        - read_comparative_experiments
        - stream_grouped_experiments
        - get_run_url
        - query_run
        - query_runs
        - batch_query_runs
        - query_trace
        - query_traces
        - query_trace_messages
        - batch_query_trace_messages
        - query_thread_messages
        - query_single_thread_stats
        - query_thread_stats
        - query_thread_traces
        - query_threads
        - list_github_thread_outcomes
        - query_github_thread_outcomes
        - list_pairwise_queues
        - get_pairwise_queue
        - list_pairwise_entries
        - read_run
        - read_runs
        - read_example
        - read_examples
        - read_feedback
        - read_feedbacks
        - create_license_share_link
        - create_provisioned_saas_org
        - mint_self_hosted_license
        - invite_provisioned_org_member
        - create_self_hosted_customer
        - update_self_hosted_customer
        - update_self_hosted_license
        - get_self_hosted_customer
        - get_provisioned_saas_org
        - update_provisioned_saas_org
        - create_oauth_client
        - update_oauth_client
        - delete_oauth_client
        - rotate_oauth_client_secret
        - revoke_oauth_grant
        - create_custom_app
        - update_custom_app
        - delete_custom_app
        - bulk_delete_custom_apps
        - update_custom_app_share
        - update_custom_app_claim
        - download_custom_app_source
        - create_custom_app_editing_credential
        - create_custom_app_editing_sandbox
        - delete_custom_app_editing_sandbox
        - create_taskset
        - update_taskset
        - delete_taskset
        - create_taskset_version
        - download_taskset_bundle
        - create_taskset_task
        - create_taskset_task_version
        - delete_taskset_task
        - get_taskset_task_file_content
        - create_taskset_world
        - create_taskset_world_version
        - get_taskset_world_file_content
        - create_taskset_run
        - cancel_taskset_run
        - test_op_generic
      title: AuditLogOperation
      description: Operations that are logged in audit_logs database table.
      x-extensible-enum: true
    ListAuditLogsOCSFResponse:
      properties:
        cursor:
          anyOf:
            - type: string
            - type: 'null'
          title: Cursor
        items:
          items:
            $ref: '#/components/schemas/OCSFApiActivity'
          type: array
          title: Items
      type: object
      required:
        - cursor
        - items
      title: ListAuditLogsOCSFResponse
      description: Response model for listing audit logs in OCSF format with pagination.
    HTTPValidationError:
      properties:
        detail:
          items:
            type: string
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    OCSFApiActivity:
      properties:
        class_uid:
          $ref: '#/components/schemas/OCSFClassUid'
        class_name:
          $ref: '#/components/schemas/OCSFClassName'
        category_uid:
          $ref: '#/components/schemas/OCSFCategoryUid'
        category_name:
          $ref: '#/components/schemas/OCSFCategoryName'
        severity_id:
          $ref: '#/components/schemas/OCSFSeverityId'
        type_uid:
          $ref: '#/components/schemas/OCSFTypeUid'
        activity_id:
          $ref: '#/components/schemas/OCSFActivityId'
        activity_name:
          type: string
          title: Activity Name
        status_id:
          $ref: '#/components/schemas/OCSFStatusId'
        status:
          type: string
          title: Status
        time:
          type: integer
          title: Time
        metadata:
          $ref: '#/components/schemas/OCSFMetadata'
        api:
          $ref: '#/components/schemas/OCSFApi'
        http_request:
          $ref: '#/components/schemas/OCSFHttpRequest'
        http_response:
          $ref: '#/components/schemas/OCSFHttpResponse'
        actor:
          $ref: '#/components/schemas/OCSFActor'
        src_endpoint:
          $ref: '#/components/schemas/OCSFEndpoint'
        resources:
          items:
            $ref: '#/components/schemas/OCSFResourceDetails'
          type: array
          title: Resources
        unmapped:
          $ref: '#/components/schemas/OCSFUnmapped'
      type: object
      required:
        - class_uid
        - class_name
        - category_uid
        - category_name
        - severity_id
        - type_uid
        - activity_id
        - activity_name
        - status_id
        - status
        - time
        - metadata
        - api
        - http_request
        - http_response
        - actor
        - src_endpoint
        - resources
        - unmapped
      title: OCSFApiActivity
      description: >-
        OCSF API Activity event (Class UID: 6003).


        This represents an API call event in the OCSF format.

        Reference: https://schema.ocsf.io/1.7.0/classes/api_activity


        Remember to try to validate the OCSF event against the official OCSF
        schema validator API:
        https://schema.ocsf.io/doc/index.html#/Tools/SchemaWeb.SchemaController.validate

        Or with `test_ocsf_validates_against_schema()` in
        test_audit_logs_models.py.
    OCSFClassUid:
      type: integer
      enum:
        - 6003
      title: OCSFClassUid
      description: OCSF class UIDs.
    OCSFClassName:
      type: string
      enum:
        - API Activity
      title: OCSFClassName
      description: OCSF class names.
    OCSFCategoryUid:
      type: integer
      enum:
        - 6
      title: OCSFCategoryUid
      description: OCSF category UIDs.
    OCSFCategoryName:
      type: string
      enum:
        - Application Activity
      title: OCSFCategoryName
      description: OCSF category names.
    OCSFSeverityId:
      type: integer
      enum:
        - 99
      title: OCSFSeverityId
      description: Severity levels for OCSF events.
    OCSFTypeUid:
      type: integer
      enum:
        - 600300
        - 600301
        - 600302
        - 600303
        - 600304
        - 600399
      title: OCSFTypeUid
      description: OCSF type UIDs for API Activity (class_uid * 100 + activity_id).
    OCSFActivityId:
      type: integer
      enum:
        - 0
        - 1
        - 2
        - 3
        - 4
        - 99
      title: OCSFActivityId
      description: Activity types for API Activity class.
    OCSFStatusId:
      type: integer
      enum:
        - 0
        - 1
        - 2
        - 99
      title: OCSFStatusId
      description: Status values for OCSF events.
    OCSFMetadata:
      properties:
        uid:
          type: string
          format: uuid
          title: Uid
        product:
          $ref: '#/components/schemas/OCSFProduct'
      type: object
      required:
        - uid
        - product
      title: OCSFMetadata
      description: OCSF event metadata.
    OCSFApi:
      properties:
        operation:
          $ref: '#/components/schemas/AuditLogOperation'
      type: object
      required:
        - operation
      title: OCSFApi
      description: OCSF API details object.
    OCSFHttpRequest:
      properties:
        http_method:
          type: string
          title: Http Method
        url:
          $ref: '#/components/schemas/OCSFUrl'
      type: object
      required:
        - http_method
        - url
      title: OCSFHttpRequest
      description: OCSF HTTP request object.
    OCSFHttpResponse:
      properties:
        code:
          anyOf:
            - type: integer
            - type: 'null'
          title: Code
      type: object
      required:
        - code
      title: OCSFHttpResponse
      description: OCSF HTTP response object.
    OCSFActor:
      properties:
        user:
          $ref: '#/components/schemas/OCSFUser'
      type: object
      required:
        - user
      title: OCSFActor
      description: OCSF actor object.
    OCSFEndpoint:
      properties:
        ip:
          anyOf:
            - type: string
            - type: 'null'
          title: Ip
        port:
          anyOf:
            - type: integer
            - type: 'null'
          title: Port
        intermediate_ips:
          anyOf:
            - items:
                type: string
              type: array
            - type: 'null'
          title: Intermediate Ips
      type: object
      required:
        - ip
        - port
        - intermediate_ips
      title: OCSFEndpoint
      description: OCSF network endpoint object.
    OCSFResourceDetails:
      properties:
        uid:
          type: string
          format: uuid
          title: Uid
      type: object
      required:
        - uid
      title: OCSFResourceDetails
      description: OCSF resource details object.
    OCSFUnmapped:
      properties:
        original_audit_log:
          $ref: '#/components/schemas/AuditLogMessage'
      type: object
      required:
        - original_audit_log
      title: OCSFUnmapped
      description: |-
        OCSF unmapped attribute for source-specific data.

        Reference: https://schema.ocsf.io/1.7.0/classes/base_event
    OCSFProduct:
      properties:
        name:
          type: string
          title: Name
        vendor_name:
          type: string
          title: Vendor Name
      type: object
      required:
        - name
        - vendor_name
      title: OCSFProduct
      description: OCSF product object.
    OCSFUrl:
      properties:
        path:
          type: string
          title: Path
      type: object
      required:
        - path
      title: OCSFUrl
      description: OCSF URL object.
    OCSFUser:
      properties:
        uid:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Uid
        credential_uid:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Credential Uid
      type: object
      required:
        - uid
        - credential_uid
      title: OCSFUser
      description: OCSF user object within actor.
    AuditLogMessage:
      properties:
        id:
          type: string
          format: uuid
          title: Id
        operation_name:
          type: string
          title: Operation Name
        operation_succeeded:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Operation Succeeded
        request_time:
          type: string
          format: date-time
          title: Request Time
        api_key_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Api Key Id
        user_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: User Id
        ls_user_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Ls User Id
        organization_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Organization Id
        workspace_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Workspace Id
        enrichments:
          anyOf:
            - $ref: '#/components/schemas/AuditLogEnrichments'
            - type: 'null'
      type: object
      required:
        - id
        - operation_name
        - operation_succeeded
        - request_time
        - api_key_id
        - user_id
        - ls_user_id
        - organization_id
        - workspace_id
        - enrichments
      title: AuditLogMessage
      description: |-
        Represents an audit log message.

        Indexed columns are individual DB columns. All other fields
        (request_method, request_path, client_host, etc.) live in the
        enrichments JSONB column.
    AuditLogEnrichments:
      properties:
        request_method:
          type: string
          title: Request Method
        request_path:
          type: string
          title: Request Path
        client_host:
          anyOf:
            - type: string
            - type: 'null'
          title: Client Host
        client_port:
          anyOf:
            - type: integer
            - type: 'null'
          title: Client Port
        x_forwarded_for:
          anyOf:
            - type: string
            - type: 'null'
          title: X Forwarded For
        response_status_code:
          anyOf:
            - type: integer
            - type: 'null'
          title: Response Status Code
        resource_ids:
          anyOf:
            - items:
                type: string
              type: array
            - type: 'null'
          title: Resource Ids
        resource_owner_ls_user_id:
          anyOf:
            - type: string
            - type: 'null'
          title: Resource Owner Ls User Id
          description: >-
            LangSmith user ID of the member the resource belonged to, set when
            that is not the actor.
        delegated_from_sandbox_id:
          anyOf:
            - type: string
            - type: 'null'
          title: Delegated From Sandbox Id
          description: >-
            Sandbox that made the call under an access-delegation grant, set
            when the actor fields name its delegator rather than a user acting
            directly.
        duration_milliseconds:
          anyOf:
            - type: integer
            - type: 'null'
          title: Duration Milliseconds
          description: Time the server took to handle the request, in milliseconds.
        user_agent:
          anyOf:
            - type: string
            - type: 'null'
          title: User Agent
          description: User-Agent header of the request, truncated to 256 bytes.
        tool_name:
          anyOf:
            - type: string
            - type: 'null'
          title: Tool Name
          description: Tool the request invoked, as named by the caller.
        caller:
          anyOf:
            - type: string
            - type: 'null'
          title: Caller
          description: LangSmith product that made the request, as reported by the caller.
        is_tool_error:
          type: boolean
          title: Is Tool Error
          description: >-
            True when the invoked tool reported a failure inside a successful
            response.
        gateway:
          anyOf:
            - $ref: '#/components/schemas/AuditLogGateway'
            - type: 'null'
          description: Managed Tools gateway the request went through.
        upstream:
          anyOf:
            - $ref: '#/components/schemas/AuditLogUpstream'
            - type: 'null'
          description: Server and tool a Managed Tools gateway routed the call to.
        server:
          anyOf:
            - $ref: '#/components/schemas/AuditLogServer'
            - type: 'null'
          description: Managed Tools MCP server the request reached.
      type: object
      title: AuditLogEnrichments
      description: Non-indexed request metadata stored in the enrichments JSONB column.
    AuditLogGateway:
      properties:
        id:
          type: string
          title: Id
        name:
          type: string
          title: Name
      type: object
      required:
        - id
        - name
      title: AuditLogGateway
      description: Managed Tools gateway a request went through.
    AuditLogUpstream:
      properties:
        server_id:
          type: string
          title: Server Id
        builtin_server_key:
          type: string
          title: Builtin Server Key
        tool_name:
          type: string
          title: Tool Name
      type: object
      required:
        - tool_name
      title: AuditLogUpstream
      description: Server and tool a Managed Tools gateway routed a call to.
    AuditLogServer:
      properties:
        id:
          type: string
          title: Id
        key:
          type: string
          title: Key
        name:
          type: string
          title: Name
        host:
          type: string
          title: Host
      type: object
      required:
        - name
      title: AuditLogServer
      description: Managed Tools MCP server a request reached.
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

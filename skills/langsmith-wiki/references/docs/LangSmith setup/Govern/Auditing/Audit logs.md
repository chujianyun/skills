# Audit logs

> Track and review administrative actions across your LangSmith organization for security, compliance, and operational visibility.

> [!NOTE]
>
> Audit logs are available on [**Enterprise** plans](https://docs.langchain.com/langsmith/pricing-plans.md). If you're interested in upgrading to Enterprise, [contact our sales team](https://www.langchain.com/contact-sales).

LangSmith audit logs provide a tamper-resistant record of administrative and configuration actions taken within your organization. They help you answer questions like:

* **Who** deleted an API key, a dataset, or a deployment?
* **When** was a new member invited, a role modified, or examples updated?
* **What** billing, SSO, or data retention configuration was changed?
* **Which** datasets, tracing projects, or prompt webhooks were modified? In an [agent-based workspace](../../Overview/Agent-based%20workspaces/Agent%20Registry.md), agents are audited too.

Audit logs are useful for security reviews, compliance requirements, and general operational visibility.

## Prerequisites

* Your organization must be on an [**Enterprise** plan](https://docs.langchain.com/langsmith/pricing-plans.md).
* You must have the **Organization Admin** or **Organization Operator** role ([`organization:manage` permission](../Users%20%26%20access%20control/Role-based%20access%20control.md#organization-admin)) to view audit logs.

## What gets logged

Audit logs record changes to organization settings, membership, credentials, workspaces, and other resources. Each event includes the timestamp, the actor, the operation name, the affected resources, and whether it succeeded. For the complete list of operation names, see the [tracked operations reference](#tracked-operations-reference).

## View audit logs in the UI

Organization Admins and Organization Operators can browse audit logs from **Organization Settings > Audit logs**.

The table shows the time, actor, workspace, operation, status, and affected resources for each event. Click a row's timestamp to open the full raw event as JSON in a side panel.

Use the filters above the table to narrow results:

* **Time range**
* **Workspace**
* **Operation**
* **Actor**: A specific user, API key, or service key
* **Resource ID**

Audit logs are also available via the [API](#query-audit-logs-via-api).

## Retention

Audit logs are retained for up to **400 days**. Events older than 400 days may be removed automatically.

## Enable audit logs for self-hosted deployments

Audit logs are available for [self-hosted](../../Self-hosted/Self-hosted%20LangSmith.md) LangSmith instances running Helm chart **0.12.33** or later. Coverage of individual operations has expanded over time. For the chart version that introduced each operation, see [Self-hosted version availability](#self-hosted-version-availability).

Once you've upgraded, use one of the following options to enable audit logs:

* **Enable for a specific organization:** Run the following against your LangSmith PostgreSQL database, replacing `<organization_id>` with the ID copied from the organization settings page in the UI:

  ```sql
  UPDATE organizations SET config = config || '{"can_use_audit_logs": true}' WHERE id = '<organization_id>' AND NOT is_personal;
  ```

* **Enable for all organizations:** Add the following environment variable to `commonEnv` in your `values.yaml`:

  ```yaml
  DEFAULT_ORG_FEATURE_CAN_USE_AUDIT_LOGS: "true"
  ```

  > [!NOTE]
  >
  > This environment variable has no effect on personal organizations.

For more details on self-hosted releases, see the [self-hosted changelog](../../Self-hosted/Reference/Self-hosted%20LangSmith%20changelog.md).

## Query audit logs via API

Use the `GET /api/v1/audit-logs` endpoint ([API reference](../../../Monitor/Reference/LangSmith%20REST%20API/Administration/Get%20audit%20logs.md)) to retrieve audit log events. Results follow the [OCSF API Activity](https://schema.ocsf.io/1.7.0/classes/api_activity) schema.

### Example request

```bash
curl -G \
  'https://api.smith.langchain.com/api/v1/audit-logs' \
  -H 'accept: application/json' \
  -H 'X-API-Key: lsv2_sk_...' \
  -H 'X-Organization-Id: abc123...' \
  -d 'limit=2' \
  --data-urlencode 'start_time=2026-01-01T18:35:16.232Z' \
  --data-urlencode 'end_time=2026-01-13T18:35:16.232Z' \
  --data-urlencode 'operations=create_api_key' \
  --data-urlencode 'operations=delete_api_key'
```

## Response format

Audit log events are returned in [OCSF v1.7.0 API Activity (Class UID 6003)](https://schema.ocsf.io/1.7.0/classes/api_activity) format. Key fields:

| Field | Description |
| - | - |
| `actor.user.uid` | UUID of the user who performed the action. |
| `actor.user.credential_uid` | UUID of the API key, PAT, or service key used to authenticate the request. `null` if the user authenticated via session (e.g., the UI). |
| `api.operation` | The LangSmith operation name (e.g., `create_api_key`, `delete_workspace`). See [tracked operations reference](#tracked-operations-reference) for all values. |
| `status` | `Success`, `Failure`, or `Unknown`. |
| `resources` | List of UUIDs for the resources affected by the operation (e.g., the role that was updated, the workspace that was created). |
| `metadata.uid` | Unique identifier for this audit log event. |
| `unmapped.original_audit_log` | The full LangSmith-native audit log record, including `organization_id` and `workspace_id`. |
| `unmapped.original_audit_log.enrichments.resource_owner_ls_user_id` | UUID of the member who owns the resource the operation acted on, for the operations that record it, such as deactivating or deleting a personal access token. A value different from `actor.user.uid` means an administrator acted on another member's resource. |

## Forwarding to external systems

To forward audit log events to an external SIEM or logging platform, you can run a scheduled function that pulls the previous hour of events every hour. For example, with [AWS Lambda + EventBridge Scheduler](https://docs.aws.amazon.com/lambda/latest/dg/with-eventbridge-scheduler.html), failures land in a dead-letter queue so you know which windows to retry.

## Tracked operations reference

| Category | Operations (`api.operation`) |
| - | - |
| **API keys & credentials** | `create_api_key`, `delete_api_key`, `create_personal_access_token`, `delete_personal_access_token`, `create_service_key`, `delete_service_key`, `update_service_key`, `create_service_account`, `delete_service_account`, `revoke_personal_access_token`, `list_org_personal_access_tokens`, `list_all_org_personal_access_tokens`, `list_org_service_keys` |
| **Roles** | `create_role`, `update_role`, `delete_role` |
| **Organizations** | `create_organization`, `create_provisioned_saas_org`, `create_tenant`, `invite_provisioned_org_member`, `claim_pending_organization_invite`, `delete_pending_organization_invite` |
| **Organization members** | `invite_user_to_org`, `invite_users_to_org_batch`, `update_org_member`, `delete_org_member`, `delete_org_pending_member`, `add_basic_auth_users_to_org`, `update_basic_auth_user` |
| **SSO & authentication** | `create_sso_settings`, `update_sso_settings`, `delete_sso_settings`, `update_login_methods`, `update_default_sso_provision_organization`, `get_sso_settings`, `get_sso_settings_current`, `get_login_methods`, `send_sso_email_confirmation`, `confirm_sso_user_email`, `login` |
| **SCIM provisioning** | `create_scim_token`, `update_scim_token`, `delete_scim_token`, `create_scim_user`, `update_scim_user`, `delete_scim_user`, `create_scim_group`, `update_scim_group`, `delete_scim_group` |
| **Billing & business info** | `update_organization_info`, `update_business_info`, `update_payment_plan`, `update_payment_method`, `create_payment_setup_intent`, `create_payment_checkout_session`, `create_payment_account_link` |
| **Workspaces** | `create_workspace`, `update_workspace`, `delete_workspace`, `add_member_to_workspace`, `add_members_to_workspace_batch`, `delete_workspace_member`, `update_workspace_member`, `delete_workspace_pending_member`, `claim_pending_workspace_invite`, `delete_pending_workspace_invite`, `update_workspace_secrets`, `unshare_entities`, `set_tenant_handle` |
| **Data retention & usage limits** | `update_ttl_settings`, `update_usage_limit`, `delete_usage_limit` |
| **Tracing projects** | `update_tracer_session`, `delete_tracer_session`, `delete_tracer_sessions` |
| **Agents** | `create_agent`, `create_agent_environment`, `update_agent`, `delete_agent`, `create_agent_runtime_binding` |
| **Runs & traces** | `query_run`, `query_runs`, `query_trace`, `query_trace_messages`, `batch_query_trace_messages`, `query_threads`, `query_thread_traces`, `read_run`, `read_runs`, `delete_runs`, `get_run_cluster`, `generate_runs_query` |
| **Datasets** | `create_dataset`, `create_csv_dataset`, `update_dataset`, `delete_dataset`, `delete_datasets`, `update_dataset_version`, `update_dataset_splits`, `share_dataset`, `unshare_dataset`, `clone_dataset`, `download_dataset`, `generate_dataset`, `generate_shared_dataset_query`, `get_dataset_comparison_view`, `stream_dataset_comparison_view`, `read_dataset_delta`, `read_shared_delta`, `read_shared_delta_stream`, `create_experiment_via_upload`, `create_playground_experiment`, `create_comparative_experiment`, `delete_comparative_experiment` |
| **Examples** | `create_example`, `create_examples`, `update_example`, `update_examples`, `delete_example`, `delete_examples`, `read_example`, `read_examples`, `get_example`, `list_examples`, `sync_examples`, `validate_example`, `validate_examples` |
| **Experiments** | `create_experiment_view_override`, `update_experiment_view_override`, `delete_experiment_view_override`, `get_experiment_view_override`, `get_experiment_view_overrides`, `evaluate_experiment` |
| **Evaluators** | `create_evaluator`, `update_evaluator`, `delete_evaluator`, `bulk_delete_evaluators`, `execute_custom_code` |
| **Feedback** | `create_feedback_config`, `update_feedback_config`, `delete_feedback_config`, `create_feedback_formula`, `update_feedback_formula`, `delete_feedback_formula`, `read_feedback`, `read_feedbacks`, `stream_feedback_delta` |
| **Annotation queues** | `create_annotation_queue`, `update_annotation_queue`, `delete_annotation_queue`, `delete_annotation_queues`, `populate_annotation_queue`, `export_annotation_queue`, `add_annotation_queue_reviewer`, `remove_annotation_queue_reviewer`, `add_runs_to_annotation_queue`, `create_annotation_queue_run_status`, `update_annotation_queue_run`, `get_annotation_queue_run`, `get_annotation_queue_runs`, `delete_annotation_queue_run`, `delete_annotation_queue_runs`, `resolve_annotation_queue_run`, `get_pairwise_queue`, `list_pairwise_queues`, `list_pairwise_entries` |
| **Alerts** | `create_alert_rule`, `update_alert_rule`, `delete_alert_rule`, `test_alert_rule` |
| **Filter views** | `create_filter_view`, `update_filter_view`, `delete_filter_view`, `rename_filter_view` |
| **Prompt commits & hub** | `create_commit`, `create_directory_commit`, `delete_directory`, `create_hub_environment`, `update_hub_environment`, `delete_hub_environment` |
| **Prompt canvas quick actions** | `create_prompt_canvas_quick_action`, `update_prompt_canvas_quick_action`, `delete_prompt_canvas_quick_action` |
| **Prompt webhooks** | `create_prompt_webhook`, `update_prompt_webhook`, `delete_prompt_webhook`, `test_prompt_webhook` |
| **Deployments** | `create_deployment`, `update_deployment`, `delete_deployment` |
| **Bulk exports** | `create_bulk_export`, `cancel_bulk_export`, `get_bulk_export`, `get_bulk_export_run`, `get_bulk_export_runs`, `get_bulk_export_runs_filtered`, `list_bulk_exports`, `create_bulk_export_destination`, `update_bulk_export_destination`, `read_bulk_export_destination`, `list_bulk_export_destinations` |
| **Resource tags** | `create_tag_key`, `update_tag_key`, `delete_tag_key`, `create_tag_value`, `update_tag_value`, `delete_tag_value`, `create_tagging`, `delete_tagging` |
| **Access policies** | `create_access_policy`, `delete_access_policy`, `list_access_policies`, `read_access_policy`, `attach_access_policies`, `read_role_access_policies`, `read_team_access_policies` |
| **Teams** | `create_team`, `update_team`, `delete_team`, `add_team_members`, `remove_team_member`, `attach_team_access_policy`, `detach_team_access_policy`, `create_team_workspace_grant`, `update_team_workspace_grant`, `delete_team_workspace_grant` |
| **Custom charts** | `create_chart`, `update_chart`, `delete_chart`, `read_chart`, `read_charts`, `read_chart_preview`, `create_chart_section`, `update_chart_section`, `delete_chart_section`, `clone_chart_section`, `read_chart_section`, `create_org_chart`, `update_org_chart`, `delete_org_chart`, `create_org_chart_section`, `update_org_chart_section`, `delete_org_chart_section`, `read_tracing_dashboard` |
| **Model pricing** | `create_model_price_map`, `update_model_price_map`, `delete_model_price_map` |
| **MCP servers & tools** | `create_mcp_server`, `update_mcp_server`, `delete_mcp_server`, `register_mcp_server_oauth`, `mcp_proxy`, `create_mcp_vendor_settings`, `update_mcp_vendor_settings`, `delete_mcp_vendor_settings`, `invalidate_mcp_tools_cache`, `create_tool`, `update_tool`, `delete_tool` |
| **Gateway policies** | `create_gateway_policy`, `update_gateway_policy`, `delete_gateway_policy` |
| **Forge configurations** | `create_forge_configuration`, `update_forge_configuration`, `delete_forge_configuration`, `trigger_forge_configuration` |
| **Insights jobs** | `create_insights_job`, `update_insights_job`, `delete_insights_job`, `create_insights_job_config`, `update_insights_job_config`, `delete_insights_job_config`, `generate_insights_job_config`, `get_insights_job_runs` |
| **Fleet usage limits & webhooks** | `create_fleet_usage_limit`, `update_fleet_usage_limit`, `delete_fleet_usage_limit`, `create_fleet_webhook`, `update_fleet_webhook`, `delete_fleet_webhook`, `test_fleet_webhook` |
| **Sandbox proxy profiles** | `create_sandbox_proxy_profile`, `update_sandbox_proxy_profile`, `delete_sandbox_proxy_profile` |
| **Playground settings** | `create_playground_settings`, `update_playground_settings`, `delete_playground_settings` |
| **Self-hosted licensing** | `create_self_hosted_customer`, `update_self_hosted_customer`, `mint_self_hosted_license`, `update_self_hosted_license` |
| **Feature model defaults** | `upsert_feature_default_model`, `delete_feature_default_model`, `upsert_feature_disabled_model`, `delete_feature_disabled_model` |
| **Onboarding** | `create_onboarding_state`, `update_onboarding_state` |
| **NPS** | `submit_nps_response` |

## Self-hosted version availability

The following list provides the [self-hosted](../../Self-hosted/Self-hosted%20LangSmith.md) Helm chart version in which each operation was introduced. Operations are available on all later versions. This section applies to [self-hosted](../../Self-hosted/Self-hosted%20LangSmith.md) deployments only; on LangSmith [cloud](../../Cloud/Cloud%20%28SaaS%29.md), all listed operations are available.

> [!NOTE]
>
> Operations introduced in `0.15.0-rc.*` release candidates are available in the `0.15.0` stable release and later. For channel details, refer to [Release policy](../../Self-hosted/Reference/Release%20policy.md).

> [accordion] 0.12.33
>
> `add_member_to_workspace`, `add_members_to_workspace_batch`, `cancel_bulk_export`, `create_api_key`, `create_bulk_export`, `create_bulk_export_destination`, `create_personal_access_token`, `create_service_key`, `create_tag_key`, `create_tag_value`, `create_tagging`, `create_workspace`, `delete_api_key`, `delete_personal_access_token`, `delete_service_key`, `delete_tag_key`, `delete_tag_value`, `delete_tagging`, `delete_usage_limit`, `delete_workspace`, `delete_workspace_member`, `delete_workspace_pending_member`, `set_tenant_handle`, `unshare_entities`, `update_organization_info`, `update_tag_key`, `update_tag_value`, `update_ttl_settings`, `update_usage_limit`, `update_workspace`, `update_workspace_member`, `update_workspace_secrets`

> [accordion] 0.12.34
>
> `add_basic_auth_users_to_org`, `clone_chart_section`, `confirm_payment_checkout_session`, `create_chart`, `create_chart_section`, `create_deployment`, `create_model_price_map`, `create_org_chart`, `create_org_chart_section`, `create_payment_account_link`, `create_payment_checkout_session`, `create_payment_setup_intent`, `create_role`, `create_sso_settings`, `delete_chart`, `delete_chart_section`, `delete_deployment`, `delete_model_price_map`, `delete_org_chart`, `delete_org_chart_section`, `delete_org_member`, `delete_org_pending_member`, `delete_role`, `delete_sso_settings`, `invite_user_to_org`, `invite_users_to_org_batch`, `update_basic_auth_user`, `update_business_info`, `update_chart`, `update_chart_section`, `update_default_sso_provision_organization`, `update_deployment`, `update_login_methods`, `update_model_price_map`, `update_org_chart`, `update_org_chart_section`, `update_org_member`, `update_payment_method`, `update_payment_plan`, `update_role`, `update_sso_settings`

> [accordion] 0.13.3
>
> `update_bulk_export_destination`

> [accordion] 0.13.32
>
> `clone_dataset`, `create_comparative_experiment`, `create_csv_dataset`, `create_dataset`, `create_example`, `create_examples`, `create_experiment_via_upload`, `create_playground_experiment`, `create_prompt_webhook`, `delete_comparative_experiment`, `delete_dataset`, `delete_datasets`, `delete_example`, `delete_examples`, `delete_prompt_webhook`, `delete_tracer_session`, `delete_tracer_sessions`, `read_bulk_export_destination`, `share_dataset`, `test_prompt_webhook`, `unshare_dataset`, `update_dataset`, `update_dataset_splits`, `update_dataset_version`, `update_example`, `update_examples`, `update_prompt_webhook`, `update_tracer_session`

> [accordion] 0.13.37
>
> `attach_access_policies`, `create_access_policy`, `create_scim_group`, `create_scim_token`, `create_scim_user`, `delete_access_policy`, `delete_scim_group`, `delete_scim_token`, `delete_scim_user`, `list_access_policies`, `read_access_policy`, `read_role_access_policies`, `update_scim_group`, `update_scim_token`, `update_scim_user`

> [accordion] 0.15.0-rc.1
>
> `add_annotation_queue_reviewer`, `add_runs_to_annotation_queue`, `batch_query_trace_messages`, `bulk_delete_evaluators`, `claim_pending_organization_invite`, `claim_pending_workspace_invite`, `confirm_sso_user_email`, `count_examples`, `create_alert_rule`, `create_annotation_queue`, `create_annotation_queue_run_status`, `create_commit`, `create_directory_commit`, `create_evaluator`, `create_experiment_view_override`, `create_feedback_config`, `create_feedback_formula`, `create_filter_view`, `create_fleet_usage_limit`, `create_fleet_webhook`, `create_forge_configuration`, `create_gateway_policy`, `create_hub_environment`, `create_insights_job`, `create_insights_job_config`, `create_mcp_server`, `create_mcp_vendor_settings`, `create_onboarding_state`, `create_organization`, `create_playground_settings`, `create_prompt_canvas_quick_action`, `create_sandbox_proxy_profile`, `create_service_account`, `create_tenant`, `create_tool`, `delete_alert_rule`, `delete_annotation_queue`, `delete_annotation_queue_run`, `delete_annotation_queue_runs`, `delete_annotation_queues`, `delete_directory`, `delete_evaluator`, `delete_experiment_view_override`, `delete_feature_default_model`, `delete_feature_disabled_model`, `delete_feedback_config`, `delete_feedback_formula`, `delete_filter_view`, `delete_fleet_usage_limit`, `delete_fleet_webhook`, `delete_forge_configuration`, `delete_gateway_policy`, `delete_hub_environment`, `delete_insights_job`, `delete_insights_job_config`, `delete_mcp_server`, `delete_mcp_vendor_settings`, `delete_pending_organization_invite`, `delete_pending_workspace_invite`, `delete_playground_settings`, `delete_prompt_canvas_quick_action`, `delete_runs`, `delete_sandbox_proxy_profile`, `delete_service_account`, `delete_tool`, `diff_dataset_versions`, `download_dataset`, `evaluate_experiment`, `execute_custom_code`, `export_annotation_queue`, `export_granular_usage_csv`, `export_usage_backfill_csv`, `generate_dataset`, `generate_insights_job_config`, `generate_runs_query`, `generate_shared_dataset_query`, `get_annotation_queue`, `get_annotation_queue_archived_size`, `get_annotation_queue_run`, `get_annotation_queue_runs`, `get_annotation_queue_size`, `get_annotation_queue_total_size`, `get_annotation_queues_for_run`, `get_audit_logs`, `get_bulk_export`, `get_bulk_export_run`, `get_bulk_export_runs`, `get_bulk_export_runs_filtered`, `get_company_info`, `get_dataset_comparison_view`, `get_dataset_version`, `get_dataset_versions`, `get_example`, `get_experiment_view_override`, `get_experiment_view_overrides`, `get_feedback_formula`, `get_filter_view`, `get_granular_usage`, `get_insights_job`, `get_insights_job_runs`, `get_login_methods`, `get_mcp_tools`, `get_onboarding_state`, `get_org_dashboard`, `get_org_usage`, `get_org_usage_limits`, `get_organization_billing_info`, `get_organization_info`, `get_pairwise_queue`, `get_run_cluster`, `get_shared_examples_count`, `get_shared_tokens`, `get_sso_settings`, `get_sso_settings_current`, `get_tag_key`, `get_tag_value`, `get_usage_limits`, `get_workspace_stats`, `get_workspace_usage_limits_info`, `invalidate_mcp_tools_cache`, `list_annotation_queues`, `list_bulk_export_destinations`, `list_bulk_exports`, `list_chart_sections`, `list_examples`, `list_feedback_configs`, `list_feedback_formulas`, `list_filter_views`, `list_insights_job_configs`, `list_insights_jobs`, `list_org_members`, `list_org_personal_access_tokens`, `list_org_service_keys`, `list_organization_roles`, `list_organizations`, `list_pairwise_entries`, `list_pairwise_queues`, `list_pending_organization_invites`, `list_pending_workspace_invites`, `list_permissions`, `list_service_accounts`, `list_tag_keys`, `list_tag_values`, `list_taggings`, `list_tags`, `list_tags_for_resource`, `list_workspace_members`, `list_workspaces`, `login`, `mcp_proxy`, `mcp_proxy_get`, `populate_annotation_queue`, `query_run`, `query_runs`, `query_thread_traces`, `query_threads`, `query_trace`, `query_trace_messages`, `read_chart`, `read_chart_preview`, `read_chart_section`, `read_charts`, `read_dataset_delta`, `read_dataset_share_state`, `read_example`, `read_examples`, `read_feedback`, `read_feedbacks`, `read_model_price_map`, `read_run`, `read_runs`, `read_shared_delta`, `read_shared_delta_stream`, `read_tracing_dashboard`, `register_mcp_server_oauth`, `remove_annotation_queue_reviewer`, `rename_filter_view`, `resolve_annotation_queue_run`, `send_sso_email_confirmation`, `stream_dataset_comparison_view`, `stream_feedback_delta`, `submit_nps_response`, `sync_examples`, `test_alert_rule`, `test_fleet_webhook`, `trigger_forge_configuration`, `update_alert_rule`, `update_annotation_queue`, `update_annotation_queue_run`, `update_evaluator`, `update_experiment_view_override`, `update_feedback_config`, `update_feedback_formula`, `update_filter_view`, `update_fleet_usage_limit`, `update_fleet_webhook`, `update_forge_configuration`, `update_gateway_policy`, `update_hub_environment`, `update_insights_job`, `update_insights_job_config`, `update_mcp_server`, `update_mcp_vendor_settings`, `update_onboarding_state`, `update_playground_settings`, `update_prompt_canvas_quick_action`, `update_sandbox_proxy_profile`, `update_self_hosted_customer`, `update_self_hosted_license`, `update_tool`, `upsert_feature_default_model`, `upsert_feature_disabled_model`, `validate_example`, `validate_examples`

> [accordion] 0.15.0
>
> `create_provisioned_saas_org`, `create_self_hosted_customer`, `invite_provisioned_org_member`, `mint_self_hosted_license`

> [accordion] 0.16.0
>
> `export_granular_usage_deployments_csv`, `export_granular_usage_traces_csv`, `get_granular_usage_deployments`, `get_granular_usage_traces`, `update_service_key`

> [accordion] 0.17.0
>
> `create_agent`, `create_agent_runtime_binding`, `delete_agent`, `list_all_org_personal_access_tokens`, `revoke_personal_access_token`, `update_agent`

`create_agent_environment` is not yet available in a stable self-hosted release.

In 0.16.0, the traces and deployments operations replace `get_granular_usage` and `export_granular_usage_csv`, which are not logged on 0.16.0 and later.

## FAQ

> [accordion] Who can view audit logs?
>
> Users with the [**Organization Admin**](../Users%20%26%20access%20control/Role-based%20access%20control.md#organization-admin) or [**Organization Operator**](../Users%20%26%20access%20control/Role-based%20access%20control.md#organization-operator) role (which grant the `organization:manage` permission) can access audit logs. Workspace-level roles do not provide audit log access.

> [accordion] Are audit logs available on the Plus or Developer plan?
>
> No. Audit logs are an Enterprise feature. See [pricing](https://www.langchain.com/pricing) for plan details.

> [accordion] Is there a UI for viewing audit logs?
>
> Yes. See [View audit logs in the UI](#view-audit-logs-in-the-ui). Audit logs are also available via the [API](#query-audit-logs-via-api).

> [accordion] Are read operations logged?
>
> Audit logs currently primarily focused on write operations. Support for more read operations may be added in the future.

> [accordion] Will more operations be tracked in the future?
>
> Yes. The set of tracked operations expands over time. The [tracked operations reference](#tracked-operations-reference) always reflects the current set of supported operations.

> [accordion] Can I get audit logs in a format other than OCSF?
>
> The API returns events exclusively in OCSF format. The `unmapped.original_audit_log` field within each event contains the raw LangSmith audit log record if you need the data in a different shape.

> [accordion] What is OCSF?
>
> The [Open Cybersecurity Schema Framework (OCSF)](https://schema.ocsf.io/) is an open standard for security event data. LangSmith returns audit log events as OCSF v1.7.0 API Activity (Class 6003) objects.

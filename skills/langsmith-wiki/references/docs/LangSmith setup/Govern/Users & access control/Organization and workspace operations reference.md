# Organization and workspace operations reference

This page provides a comprehensive reference table of [workspace](../Organization/Overview.md#workspaces) and [organization](../Organization/Overview.md#organizations) operations and which roles can perform them.

The list includes API operations in LangSmith along with:

* Which system roles can perform each operation.
* The specific permission string required.
* Notes about partial access or special cases.

> [!NOTE]
>
> For an overview of LangSmith's RBAC system, role definitions, and permission concepts, refer to [Role-based access control](Role-based%20access%20control.md).

## Contents

| Organization-level operations | Workspace-level operations |
| - | - |
| **Core management:** • [Organization settings](#organization-settings): Org info and configuration • [Workspaces](#workspaces): Workspace management • [Organization members](#organization-members): Member management • [Roles and permissions](#roles-and-permissions): Custom roles | **Core resources:** • [Projects](#projects): Organize traces and runs • [Runs](#runs): Individual execution traces • [Datasets](#datasets): Test datasets for evaluation • [Examples](#examples): Individual dataset examples • [Experiments](#experiments): Comparative experiments |
| **Security and authentication:** • [SSO and authentication](#sso-and-authentication): Single sign-on setup • [SCIM](#scim): Identity provisioning • [Access policies](#access-policies): Attribute-based access control • [Organization teams](#organization-teams): Teams and their workspace access | **Monitoring and analysis:** • [Rules](#rules): Automated run rules • [Alerts](#alerts): Alert rules for monitoring • [Feedback](#feedback): Scores and labels on outputs • [Annotation Queues](#annotation-queues): Human review queues • [Charts](#charts): Custom visualizations |
| **Billing and accounts:** • [Billing and payments](#billing-and-payments): Subscription management • [API keys](#api-keys): Org-level keys | **Development and configuration:** • [Prompts](#prompts): Prompt templates (LangChain Hub) • [Custom apps](#custom-apps): User-authored mini web apps • [Deployments](#deployments): Deployment configurations • [MCP Servers](#mcp-servers): Model Context Protocol servers • [Fleet](#fleet): Fleet admin operations |
| **Analytics:** • [Charts and dashboards](#organization-charts-and-dashboards): Org-level visualizations • [Usage and analytics](#usage-and-analytics): Usage tracking and TTL settings | **Workspace management:** • [Model price map](#model-price-map): Per-token model prices • [Workspace settings](#workspace-settings-and-management): Members, settings • [Workspace teams](#workspace-teams): Team members and policies for this workspace • [Tags](#tags): Metadata tagging system • [Bulk Exports](#bulk-exports): Data export operations |

**Additional information:**

* [User-level operations](#user-level-operations): Operations for all authenticated users
* [Permission inheritance](#permission-inheritance): How roles inherit across org/workspaces

## Legend

* ✓ **Allowed**: User with this role can perform this action
* ✗ **Not Allowed**: User with this role cannot perform this action
* ⚠ **Partial**: User has limited access (see notes)

## Organization-level operations

> [!NOTE]
>
> Organization-level operations are controlled by organization roles, which are separate from the RBAC feature. Learn more in the [Role-based access control](Role-based%20access%20control.md#organization-roles) guide.

> [!NOTE]
>
> [Organization Restricted](Role-based%20access%20control.md#organization-restricted) applies to users and workspace-scoped service keys. It holds only `organization:read-metadata`, so it can perform only the operations that require that permission. It lists only the workspaces the user or key is assigned to.

### Organization settings

| Operation | Org Admin | Org Operator | Org User | Org Viewer | Org Restricted | Required Permission |
| - | :-: | :-: | :-: | :-: | :-: | - |
| View organization info | ✓ | ✓ | ✓ | ✓ | ✓ | `organization:read-metadata` |
| View organization dashboard | ✓ | ✓ | ✓ | ✓ | ✗ | `organization:read` |
| Update organization info | ✓ | ✓ | ✗ | ✗ | ✗ | `organization:manage` |
| View billing info | ✓ | ✓ | ✓ | ✓ | ✗ | `organization:read` |
| View company info | ✓ | ✓ | ✓ | ✓ | ✗ | `organization:read` |
| Set company info | ✓ | ✓ | ✗ | ✗ | ✗ | `organization:manage` |

### Workspaces

Organization-level workspace management operations.

| Operation | Org Admin | Org Operator | Org User | Org Viewer | Org Restricted | Required Permission |
| - | :-: | :-: | :-: | :-: | :-: | - |
| List all workspaces | ✓ | ✓ | ✓ | ✓ | ⚠ | `organization:read-metadata` |
| Create workspace | ✓ | ✓ | ✗ | ✗ | ✗ | `organization:manage` |

### Organization members

| Operation | Org Admin | Org Operator | Org User | Org Viewer | Org Restricted | Required Permission | Notes |
| - | :-: | :-: | :-: | :-: | :-: | - | - |
| View organization members | ✓ | ✓ | ✓ | ✓ | ✗ | `organization:read` | |
| View active org members | ✓ | ✓ | ✓ | ✓ | ✗ | `organization:read` | |
| View pending org members | ✓ | ✓ | ✓ | ✓ | ✗ | `organization:read` | |
| Invite member to organization | ✓ | ⚠ | ✗ | ✗ | ✗ | `organization:manage` | Org Operator can only invite Org Users and Org Viewers |
| Invite members (batch) | ✓ | ⚠ | ✗ | ✗ | ✗ | `organization:manage` | Org Operator can only invite Org Users and Org Viewers |
| Add basic auth members | ✓ | ⚠ | ✗ | ✗ | ✗ | `organization:manage` | Org Operator can only add Org Users and Org Viewers |
| Remove organization member | ✓ | ⚠ | ✗ | ✗ | ✗ | `organization:manage` | Org Operator cannot remove Org Admins |
| Update organization member role | ✓ | ⚠ | ✗ | ✗ | ✗ | `organization:manage` | Org Operator can only modify Org Users and Org Viewers |
| Delete pending org member | ✓ | ⚠ | ✗ | ✗ | ✗ | `organization:manage` | Org Operator cannot delete pending Org Admin invites |

### Roles and permissions

| Operation | Org Admin | Org Operator | Org User | Org Viewer | Org Restricted | Required Permission |
| - | :-: | :-: | :-: | :-: | :-: | - |
| List organization roles | ✓ | ✓ | ✓ | ✓ | ✓ | `organization:read-metadata` |
| List available permissions | ✓ | ✓ | ✓ | ✓ | ✓ | N/A (user-level) |
| Create custom role | ✓ | ✓ | ✗ | ✗ | ✗ | `organization:manage` |
| Update custom role | ✓ | ✓ | ✗ | ✗ | ✗ | `organization:manage` |
| Delete custom role | ✓ | ✓ | ✗ | ✗ | ✗ | `organization:manage` |

### SSO and authentication

| Operation | Org Admin | Org Operator | Org User | Org Viewer | Org Restricted | Required Permission |
| - | :-: | :-: | :-: | :-: | :-: | - |
| View SSO settings | ✓ | ✓ | ✓ | ✓ | ✗ | `organization:read` |
| Create SSO settings | ✓ | ✓ | ✗ | ✗ | ✗ | `organization:authentication:manage` + `organization:access-control:manage` |
| Update SSO settings | ✓ | ✓ | ✗ | ✗ | ✗ | `organization:authentication:manage` |
| Delete SSO settings | ✓ | ✓ | ✗ | ✗ | ✗ | `organization:authentication:manage` |
| View login methods | ✓ | ✓ | ✓ | ✓ | ✓ | `organization:read-metadata` |
| Update allowed login methods | ✓ | ✓ | ✗ | ✗ | ✗ | `organization:manage` |
| Set default SSO provision | ✓ | ✓ | ✗ | ✗ | ✗ | `organization:authentication:manage` |

### SCIM

System for Cross-domain Identity Management for user provisioning. For setup instructions, refer to the [SCIM setup guide](User%20management.md#set-up-scim-for-your-organization).

| Operation | Org Admin | Org Operator | Org User | Org Viewer | Org Restricted | Required Permission |
| - | :-: | :-: | :-: | :-: | :-: | - |
| List SCIM tokens | ✓ | ✓ | ✓ | ✓ | ✗ | `organization:read` |
| Get SCIM token | ✓ | ✓ | ✓ | ✓ | ✗ | `organization:read` |
| Create SCIM token | ✓ | ✓ | ✗ | ✗ | ✗ | `organization:manage` |
| Update SCIM token | ✓ | ✓ | ✗ | ✗ | ✗ | `organization:manage` |
| Delete SCIM token | ✓ | ✓ | ✗ | ✗ | ✗ | `organization:manage` |

### Access policies

Attribute-based access control (ABAC) policies for fine-grained permissions.

| Operation | Org Admin | Org Operator | Org User | Org Viewer | Org Restricted | Required Permission |
| - | :-: | :-: | :-: | :-: | :-: | - |
| List access policies | ✓ | ✓ | ✓ | ✓ | ✗ | `organization:read` |
| Get access policy | ✓ | ✓ | ✓ | ✓ | ✗ | `organization:read` |
| Create access policy | ✓ | ✓ | ✗ | ✗ | ✗ | `organization:manage` |
| Delete access policy | ✓ | ✓ | ✗ | ✗ | ✗ | `organization:manage` |
| Attach access policy to role | ✓ | ✓ | ✗ | ✗ | ✗ | `organization:manage` |

### Organization teams

[Teams](Teams.md) and their workspace access. `organization:manage` does not allow these operations.

| Operation | Org Admin | Org Operator | Org User | Org Viewer | Required Permission |
| - | :-: | :-: | :-: | :-: | - |
| List and view teams, members, and access policies | ✓ | ✓ | ✓ | ✓ | `organization:teams:read` |
| View a team's workspace access | ✓ | ✓ | ✓ | ✓ | `organization:teams:read` |
| Create, update, or delete a team | ✓ | ✓ | ✗ | ✗ | `organization:teams:manage` |
| Add or remove team members | ✓ | ✓ | ✗ | ✗ | `organization:teams:manage-members` |
| Attach or detach access policies | ✓ | ✓ | ✗ | ✗ | `organization:teams:manage-policies` |
| Give, change, or remove a team's workspace access | ✓ | ✓ | ✗ | ✗ | `organization:teams:manage-grants` |

### Billing and payments

| Operation | Org Admin | Org Operator | Org User | Org Viewer | Org Restricted | Required Permission |
| - | :-: | :-: | :-: | :-: | :-: | - |
| Create Stripe setup intent | ✓ | ✓ | ✗ | ✗ | ✗ | `organization:manage` |
| Handle payment method creation | ✓ | ✓ | ✗ | ✗ | ✗ | `organization:manage` |
| Change payment plan | ✓ | ✓ | ✗ | ✗ | ✗ | `organization:manage` |
| Create Stripe checkout session | ✓ | ✓ | ✗ | ✗ | ✗ | `organization:manage` |
| Confirm checkout completion | ✓ | ✓ | ✗ | ✗ | ✗ | `organization:manage` |
| Create Stripe account links | ✓ | ✓ | ✗ | ✗ | ✗ | `organization:manage` |

### API keys

| Operation | Org Admin | Org Operator | Org User | Org Viewer | Org Restricted | Required Permission |
| - | :-: | :-: | :-: | :-: | :-: | - |
| List org-scoped service keys | ✓ | ✓ | ✓ | ✓ | ✗ | `organization:read` |
| Create org-scoped service key (workspace-scoped)\* | ✓ | ✓ | ⚠ | ✗ | ✗ | `organization:pats:create` + `workspaces:manage-keys` |
| Create org-scoped service key (org-wide)\* | ✓ | ✗ | ✗ | ✗ | ✗ | `organization:pats:create` + `organization:manage` |
| Delete org-scoped service key (workspace-scoped)\* | ✓ | ✓ | ⚠ | ✗ | ✗ | `organization:read` + `workspaces:manage-keys` |
| Update service key role | ✓ | ✓ | ✗ | ✗ | ✗ | `organization:manage` |
| List own personal access tokens (PATs) | ✓ | ✓ | ✓ | ✗ | ✗ | `organization:read` |
| List every member's personal access tokens (PATs) | ✓ | ✓ | ✗ | ✗ | ✗ | `organization:pats:read` |
| Create personal access token (PAT) | ✓ | ✓ | ✓ | ✗ | ✗ | `organization:pats:create` |
| Deactivate, reactivate, or delete own personal access token (PAT) | ✓ | ✓ | ✓ | ✗ | ✗ | `organization:read` |
| Deactivate, reactivate, or delete another member's personal access token (PAT) | ✓ | ✓ | ✗ | ✗ | ✗ | `organization:pats:manage` |

> [!NOTE]
>
> \* Organization Operators and Organization Users can create or delete workspace-scoped service keys only in workspaces where their role grants `workspaces:manage-keys`, such as the Workspace Admin role. Creating an org-wide service key requires the Organization Admin role.

### Organization charts and dashboards

| Operation | Org Admin | Org Operator | Org User | Org Viewer | Org Restricted | Required Permission |
| - | :-: | :-: | :-: | :-: | :-: | - |
| List org charts | ✓ | ✓ | ✓ | ✓ | ✗ | `organization:read` |
| Get org chart by ID | ✓ | ✓ | ✓ | ✓ | ✗ | `organization:read` |
| Create org chart | ✓ | ✓ | ✗ | ✗ | ✗ | `organization:manage` |
| Update org chart | ✓ | ✓ | ✗ | ✗ | ✗ | `organization:manage` |
| Delete org chart | ✓ | ✓ | ✗ | ✗ | ✗ | `organization:manage` |
| Render org chart | ✓ | ✓ | ✓ | ✓ | ✗ | `organization:read` |
| Get org chart section | ✓ | ✓ | ✓ | ✓ | ✗ | `organization:read` |
| Create org chart section | ✓ | ✓ | ✗ | ✗ | ✗ | `organization:manage` |
| Update org chart section | ✓ | ✓ | ✗ | ✗ | ✗ | `organization:manage` |
| Delete org chart section | ✓ | ✓ | ✗ | ✗ | ✗ | `organization:manage` |
| Render org chart section | ✓ | ✓ | ✓ | ✓ | ✗ | `organization:read` |

### Usage and analytics

| Operation | Org Admin | Org Operator | Org User | Org Viewer | Org Restricted | Required Permission |
| - | :-: | :-: | :-: | :-: | :-: | - |
| View organization usage | ✓ | ✓ | ✓ | ✓ | ✗ | `organization:read` |
| [View granular billable usage](../../Account/Billing%20%26%20usage/Granular%20billable%20usage.md) | ✓ | ✓ | ✓ | ✓ | ✗ | `organization:read` |
| [Export granular usage as CSV](../../Account/Billing%20%26%20usage/Granular%20billable%20usage.md#csv-export) | ✓ | ✓ | ✓ | ✓ | ✗ | `organization:read` |
| View workspace trace retention settings | ✓ | ✓ | ✓ | ✓ | ✗ | `organization:read` |
| Set workspace default trace tier (base/extended) | ✓ | ✓ | ✗ | ✗ | ✗ | `organization:manage` |
| Set workspace extended retention duration (Enterprise) | ✓ | ✓ | ✗ | ✗ | ✗ | `organization:manage` |

## Workspace-level operations

These operations are controlled by [workspace-level roles and permissions](Role-based%20access%20control.md#workspace-roles).

> [!TIP]
>
> To understand what each role means and their overall capabilities, refer to the [Role-based access control](Role-based%20access%20control.md) guide.

### Tracing keys

[Tracing keys](../../Account/Create%20an%20account%20and%20API%20key.md#tracing-keys) grant fixed trace-writing permissions in selected workspaces.

| Operation | Workspace Admin | Workspace Editor | Workspace Viewer | Required permission |
| - | :-: | :-: | :-: | - |
| Create a tracing key | ✓ | ✓ | ✗ | `workspaces:tracing-keys:create` in every selected workspace |

Custom roles require an explicit creation grant. An active creator or organization key manager can delete a tracing key. A workspace key manager needs `workspaces:manage-keys` in every remaining selected workspace.

### Projects

Projects organize traces and runs from your LLM applications.

| Operation | Workspace Admin | Workspace Editor | Workspace Viewer | Required Permission |
| - | :-: | :-: | :-: | - |
| Create a new project | ✓ | ✗ | ✗ | `projects:create` |
| Apply resource tags on project creation | ✓ | ✗ | ✗ | `projects:tag_on_create` |
| View project list | ✓ | ✓ | ✓ | `projects:read` |
| View project details | ✓ | ✓ | ✓ | `projects:read` |
| View prebuilt dashboard | ✓ | ✓ | ✓ | `projects:read` |
| View project metadata (top K values) | ✓ | ✓ | ✓ | `projects:read` |
| Update project metadata (name, description, tags) | ✓ | ✓ | ✗ | `projects:update` |
| Increase project trace retention (base → extended) | ✓ | ✓ | ✗ | `projects:increase-trace-tier`\* |
| Decrease project trace retention (extended → base) | ✓ | ✓ | ✗ | `projects:decrease-trace-tier`\* |
| Create filter view | ✓ | ✓ | ✗ | `projects:update` |
| View filter views | ✓ | ✓ | ✓ | `projects:read` |
| View specific filter view | ✓ | ✓ | ✓ | `projects:read` |
| Update filter view | ✓ | ✓ | ✗ | `projects:update` |
| Delete filter view | ✓ | ✗ | ✗ | `projects:delete` |
| Delete a project | ✓ | ✗ | ✗ | `projects:delete` |
| Delete multiple projects | ✓ | ✗ | ✗ | `projects:delete` |
| Get insights jobs | ✓ | ✓ | ✓ | `projects:read` |
| Get specific insights job | ✓ | ✓ | ✓ | `projects:read` |
| Create insights job | ✓ | ✓ | ✓ | `projects:read` + `rules:create` |
| Update insights job | ✓ | ✓ | ✗ | `projects:update` |
| Delete insights job | ✓ | ✗ | ✗ | `projects:delete` |
| Get insights job configs | ✓ | ✓ | ✓ | `rules:read` |
| Create insights job config | ✓ | ✓ | ✗ | `rules:create` |
| Auto-generate insights job config | ✓ | ✓ | ✗ | `rules:create` |
| Update insights job config | ✓ | ✓ | ✗ | `rules:update` |
| Delete insights job config | ✓ | ✓ | ✗ | `rules:delete` |
| Get run cluster from insights job | ✓ | ✓ | ✓ | `projects:read` |
| Get runs from insights job | ✓ | ✓ | ✓ | `projects:read` |

> [!NOTE]
>
> \* `projects:increase-trace-tier` and `projects:decrease-trace-tier` are independent and can be granted separately in custom roles. For example, you can allow a role to decrease retention without allowing it to increase retention. If a user lacks both permissions, the retention settings UI is hidden entirely. If they have only one, the UI is partially enabled (the disallowed direction is disabled).

> [!NOTE]
>
> Creating a saved filter view modifies an existing project and requires `projects:update`. Comparative-experiment creation requires `experiments:run`. Custom roles that only grant `projects:create` need the corresponding permission for these operations. Tracing keys do not support either operation.

### Runs

Individual execution traces and spans from your LLM applications.

| Operation | Workspace Admin | Workspace Editor | Workspace Viewer | Required Permission |
| - | :-: | :-: | :-: | - |
| Send traces from SDK (includes single run, batch, multipart, and OTEL) | ✓ | ✓ | ✗ | `runs:create` |
| View a specific run | ✓ | ✓ | ✓ | `runs:read` |
| View run inputs | ✓ | ✓ | ✓ | `runs:read` + `runs:read-inputs` |
| View run outputs | ✓ | ✓ | ✓ | `runs:read` + `runs:read-outputs` |
| View trace and thread messages and trajectories | ✓ | ✓ | ✓ | `runs:read` + `runs:read-inputs` + `runs:read-outputs` |
| Download a trace | ✓ | ✓ | ✓ | `runs:read` |
| View thread preview | ✓ | ✓ | ✓ | `runs:read` |
| Query/list runs | ✓ | ✓ | ✓ | `runs:read` |
| View run statistics | ✓ | ✓ | ✓ | `runs:read` |
| View grouped run statistics | ✓ | ✓ | ✓ | `runs:read` |
| Group runs by expression | ✓ | ✓ | ✓ | `runs:read` |
| Generate filter query from natural language | ✓ | ✓ | ✓ | `runs:read` |
| Prefetch runs | ✓ | ✓ | ✓ | `runs:read` |
| Update a run (PATCH) | ✓ | ✓ | ✗ | `runs:create` |
| View run sharing state | ✓ | ✓ | ✓ | `runs:read` |
| Share a run publicly | ✓ | ✓ | ✗ | `runs:share` |
| Unshare a run | ✓ | ✓ | ✗ | `runs:share` |
| Delete runs by trace ID or metadata | ✓ | ✗ | ✗ | `runs:delete` |

### Rules

Automated run rules that trigger actions based on run conditions.

| Operation | Workspace Admin | Workspace Editor | Workspace Viewer | Required Permission |
| - | :-: | :-: | :-: | - |
| List all run rules | ✓ | ✓ | ✓ | `rules:read` |
| Create a run rule | ✓ | ✓ | ✗ | `rules:create` |
| Update a run rule | ✓ | ✓ | ✗ | `rules:update` |
| Delete a run rule | ✓ | ✓ | ✗ | `rules:delete` |
| View rule logs | ✓ | ✓ | ✓ | `rules:read` |
| Get last applied rule | ✓ | ✓ | ✓ | `rules:read` |
| Manually trigger a rule | ✓ | ✓ | ✗ | `rules:update` |
| Trigger multiple rules | ✓ | ✓ | ✗ | `rules:update` |
| Configure per-action data retention | ✓ | ✗ | ✗ | `rules:configure-retention` |

### Alerts

Alert rules for monitoring run conditions.

| Operation | Workspace Admin | Workspace Editor | Workspace Viewer | Required Permission |
| - | :-: | :-: | :-: | - |
| Create alert rule | ✓ | ✓ | ✓ | `runs:read` |
| Update alert rule | ✓ | ✓ | ✓ | `runs:read` |
| Delete alert rule | ✓ | ✓ | ✓ | `runs:read` |
| Get alert rule | ✓ | ✓ | ✓ | `runs:read` |
| List alert rules | ✓ | ✓ | ✓ | `runs:read` |
| Test alert action | ✓ | ✓ | ✓ | `runs:read` |

### Datasets

Test datasets with examples for evaluation.

| Operation | Workspace Admin | Workspace Editor | Workspace Viewer | Required Permission |
| - | :-: | :-: | :-: | - |
| Create a dataset | ✓ | ✓ | ✗ | `datasets:create` |
| Apply resource tags on dataset creation | ✓ | ✓ | ✗ | `datasets:tag_on_create` |
| List datasets | ✓ | ✓ | ✓ | `datasets:read` |
| View dataset details | ✓ | ✓ | ✓ | `datasets:read` |
| Update dataset metadata | ✓ | ✓ | ✗ | `datasets:update` |
| Delete a dataset | ✓ | ✗ | ✗ | `datasets:delete` |
| Upload CSV dataset | ✓ | ✓ | ✗ | `datasets:create` |
| Clone dataset | ✓ | ✓ | ✗ | `datasets:clone` |
| Get dataset version | ✓ | ✓ | ✓ | `datasets:read` |
| Get dataset versions | ✓ | ✓ | ✓ | `datasets:read` |
| Diff dataset versions | ✓ | ✓ | ✓ | `datasets:read` |
| Update dataset version (tags) | ✓ | ✓ | ✗ | `datasets:update` |
| Download dataset (OpenAI format) | ✓ | ✓ | ✓ | `datasets:download` |
| Download dataset (OpenAI fine-tuning format) | ✓ | ✓ | ✓ | `datasets:download` |
| Download dataset (CSV) | ✓ | ✓ | ✓ | `datasets:download` |
| Download dataset (JSONL) | ✓ | ✓ | ✓ | `datasets:download` |
| View dataset sharing state | ✓ | ✓ | ✓ | `datasets:read` |
| Share dataset publicly | ✓ | ✗ | ✗ | `datasets:share` |
| Unshare dataset | ✓ | ✗ | ✗ | `datasets:share` |
| Get index info | ✓ | ✓ | ✓ | `datasets:read` |
| Index dataset | ✓ | ✓ | ✗ | `datasets:update` |
| Sync dataset index | ✓ | ✓ | ✗ | `datasets:update` |
| Remove dataset index | ✓ | ✓ | ✗ | `datasets:update` |
| Search dataset | ✓ | ✓ | ✓ | `datasets:read` |
| Generate synthetic examples | ✓ | ✓ | ✗ | `datasets:update` |
| Get dataset splits | ✓ | ✓ | ✓ | `datasets:read` |
| Update dataset splits | ✓ | ✓ | ✓ | `datasets:read` |
| Run playground experiment (batch) | ✓ | ⚠ | ✗ | `prompts:read` + `datasets:read` + `projects:create` |
| Run playground experiment (stream) | ✓ | ⚠ | ✗ | `prompts:read` + `datasets:read` + `projects:create` |
| Run studio experiment | ✓ | ⚠ | ✗ | `datasets:read` + `projects:create` |

> [!NOTE]
>
> Workspace Editors have partial access because they cannot create projects, which limits their ability to create new experiments.

### Examples

Individual examples within datasets.

| Operation | Workspace Admin | Workspace Editor | Workspace Viewer | Required Permission |
| - | :-: | :-: | :-: | - |
| Count examples | ✓ | ✓ | ✓ | `datasets:read` |
| View a specific example | ✓ | ✓ | ✓ | `datasets:read` |
| List examples | ✓ | ✓ | ✓ | `datasets:read` |
| Create a new example | ✓ | ✓ | ✗ | `datasets:update` |
| Create examples (bulk) | ✓ | ✓ | ✗ | `datasets:update` |
| Update a single example | ✓ | ✓ | ✗ | `datasets:update` |
| Update examples (bulk) | ✓ | ✓ | ✗ | `datasets:update` |
| Update examples (multipart) | ✓ | ✓ | ✗ | `datasets:update` |
| Upload examples from CSV | ✓ | ✓ | ✗ | `datasets:update` |
| Upload examples from JSONL | ✓ | ✓ | ✗ | `datasets:update` |
| Delete a single example | ✓ | ✓ | ✗ | `datasets:update` |
| Delete examples (bulk) | ✓ | ✓ | ✗ | `datasets:update` |
| View examples with runs | ✓ | ✓ | ✓ | `datasets:read` |
| View grouped examples with runs | ✓ | ✓ | ✓ | `datasets:read` |
| Validate a single example | ✓ | ✓ | ✓ | `datasets:read` |
| Validate examples (bulk) | ✓ | ✓ | ✓ | `datasets:read` |

> [!NOTE]
>
> Creating examples from existing runs also requires `runs:read` on each source run's project. The run's inputs and outputs are copied only if you have `runs:read-inputs` and `runs:read-outputs` for that project.

### Experiments

Comparative experiments for evaluating LLM outputs.

| Operation | Workspace Admin | Workspace Editor | Workspace Viewer | Required Permission |
| - | :-: | :-: | :-: | - |
| View comparative experiments | ✓ | ✓ | ✓ | `projects:read` |
| Create comparative experiment | ✓ | ✓ | ✗ | `experiments:run` |
| Delete comparative experiment | ✓ | ✗ | ✗ | `projects:delete` |
| View examples with runs | ✓ | ✓ | ✓ | `datasets:read` |
| View grouped examples with runs | ✓ | ✓ | ✓ | `datasets:read` |
| View grouped experiments | ✓ | ✓ | ✓ | `datasets:read` |
| View feedback delta | ✓ | ✓ | ✓ | `datasets:read` |
| Upload experiment results | ✓ | ⚠ | ✗ | `datasets:create` + `datasets:update` + `projects:create` + `runs:create` |
| Get experiment view overrides | ✓ | ✓ | ✗ | `datasets:update` |
| Create experiment view override | ✓ | ✓ | ✗ | `datasets:update` |
| Update experiment view override | ✓ | ✓ | ✗ | `datasets:update` |
| Delete experiment view override | ✓ | ✓ | ✗ | `datasets:update` |

> [!NOTE]
>
> Workspace Editors have partial access because they cannot create projects, which limits their ability to create new experiments.

### Feedback

Scores, labels, and corrections on LLM outputs.

> [!NOTE]
>
> The feedback formula operations are deprecated in favor of [composite evaluators](../../../Test/Evaluators/Evaluator%20types/UI/How%20to%20create%20a%20composite%20evaluator.md) and are scheduled for removal on 2026-08-20.

| Operation | Workspace Admin | Workspace Editor | Workspace Viewer | Required Permission |
| - | :-: | :-: | :-: | - |
| List feedback formulas (deprecated) | ✓ | ✓ | ✓ | `feedback:read` |
| Get feedback formula (deprecated) | ✓ | ✓ | ✓ | `feedback:read` |
| Create feedback formula (deprecated) | ✓ | ✓ | ✗ | `feedback:create` |
| Update feedback formula (deprecated) | ✓ | ✓ | ✗ | `feedback:update` |
| Delete feedback formula (deprecated) | ✓ | ✓ | ✗ | `feedback:delete` |
| View specific feedback | ✓ | ✓ | ✓ | `feedback:read` |
| List feedbacks | ✓ | ✓ | ✓ | `feedback:read` |
| Create feedback | ✓ | ✓ | ✗ | `feedback:create` |
| Eagerly create feedback | ✓ | ✓ | ✗ | `feedback:create` |
| Update feedback | ✓ | ✓ | ✗ | `feedback:update` |
| Delete feedback | ✓ | ✓ | ✗ | `feedback:delete` |
| Batch ingest feedback | ✓ | ✓ | ✗ | `feedback:create` |
| Create feedback ingest token | ✓ | ✓ | ✗ | `feedback:create` |
| List feedback ingest tokens | ✓ | ✓ | ✗ | `feedback:create` |
| Create feedback with token (no auth required) | ✓ | ✓ | ✓ | N/A (token-based) |
| List feedback configs | ✓ | ✓ | ✓ | `feedback:read` |
| Create feedback config | ✓ | ✓ | ✗ | `feedback:create` |
| Update feedback config | ✓ | ✓ | ✗ | `feedback:update` |

### Annotation queues

Human review queues for LLM outputs.

| Operation | Workspace Admin | Workspace Editor | Workspace Viewer | Required Permission |
| - | :-: | :-: | :-: | - |
| List annotation queues | ✓ | ✓ | ✓ | `annotation-queues:read` |
| Get annotation queue | ✓ | ✓ | ✓ | `annotation-queues:read` |
| Create annotation queue | ✓ | ✓ | ✗ | `annotation-queues:create` |
| Update annotation queue | ✓ | ✓ | ✗ | `annotation-queues:update` |
| Delete annotation queue | ✓ | ✗ | ✗ | `annotation-queues:delete` |
| Populate annotation queue | ✓ | ✓ | ✗ | `annotation-queues:update` |
| Get runs from queue | ✓ | ✓ | ✓ | `annotation-queues:read` |
| Get run from queue (by index) | ✓ | ✓ | ✓ | `annotation-queues:read` |
| Get queues for run | ✓ | ✓ | ✓ | `annotation-queues:read` |
| Get queue total size | ✓ | ✓ | ✓ | `annotation-queues:read` |
| Get queue total archived | ✓ | ✓ | ✓ | `annotation-queues:read` |
| Get queue size | ✓ | ✓ | ✓ | `annotation-queues:read` |
| Add runs to queue | ✓ | ✓ | ✗ | `annotation-queues:update` |
| Update run in queue | ✓ | ✓ | ✗ | `annotation-queues:update` |
| Delete run from queue | ✓ | ✓ | ✗ | `annotation-queues:update` |
| Delete runs from queue (bulk) | ✓ | ✓ | ✗ | `annotation-queues:update` |
| Create identity annotation queue run status | ✓ | ✓ | ✗ | `annotation-queues:update` |
| Export archived runs | ✓ | ✓ | ✓ | `annotation-queues:read` |

### Custom apps

User-authored mini web apps rendered within LangSmith. See [Custom Apps](../../../Monitor/Observe/Monitoring%20%26%20alerting/Custom%20Apps.md).

| Operation | Workspace Admin | Workspace Editor | Workspace Viewer | Required Permission |
| - | :-: | :-: | :-: | - |
| List custom apps | ✓ | ✓ | ✓ | `custom-apps:read` |
| Get custom app | ✓ | ✓ | ✓ | `custom-apps:read` |
| Create custom app | ✓ | ✓ | ✗ | `custom-apps:create` |
| Update custom app | ✓ | ✓ | ✗ | `custom-apps:update` |
| Delete custom app | ✓ | ✓ | ✗ | `custom-apps:delete` |
| Delete custom apps (bulk) | ✓ | ✓ | ✗ | `custom-apps:delete` |
| Download custom app source | ✓ | ✓ | ✗ | `custom-apps:download` |
| Record custom app view | ✓ | ✓ | ✓ | `custom-apps:read` |
| Share custom app org-wide | ✓ | ✓ | ✗ | `custom-apps:update` |
| Claim (unshare) custom app | ✓ | ✓ | ✗ | `custom-apps:update` |

### Prompts

Prompt templates and chains in the LangChain Hub.

| Operation | Workspace Admin | Workspace Editor | Workspace Viewer | Required Permission |
| - | :-: | :-: | :-: | - |
| List prompt repos | ✓ | ✓ | ✓ | `prompts:read` |
| View prompt repo | ✓ | ✓ | ✓ | `prompts:read` |
| Create prompt repo | ✓ | ✓ | ✗ | `prompts:create` |
| Apply resource tags on prompt creation | ✓ | ✓ | ✗ | `prompts:tag_on_create` |
| Fork prompt repo | ✓ | ✓ | ✗ | `prompts:create` |
| Update prompt repo | ✓ | ✓ | ✗ | `prompts:update` |
| Delete prompt repo | ✓ | ✓ | ✗ | `prompts:delete` |
| List commits | ✓ | ✓ | ✓ | `prompts:read` |
| View commit | ✓ | ✓ | ✓ | `prompts:read` |
| Push commit | ✓ | ✓ | ✗ | `prompts:update` |
| List repo tags | ✓ | ✓ | ✓ | `prompts:read` |
| Get all tags | ✓ | ✓ | ✓ | `prompts:read` |
| Create tag | ✓ | ✓ | ✗ | `prompts:tag` |
| Update tag | ✓ | ✓ | ✗ | `prompts:tag` |
| Delete tag | ✓ | ✓ | ✗ | `prompts:tag` |
| View events | ✓ | ✓ | ✓ | `prompts:read` |
| List comments | ✓ | ✓ | ✓ | `prompts:read` |
| Create comment | ✓ | ✓ | ✗ | `prompts:read` |
| Delete comment | ✓ | ✓ | ✗ | `prompts:read` |
| Toggle like | ✓ | ✓ | ✗ | `prompts:read` |
| Optimize prompt | ✓ | ✓ | ✗ | `prompts:update` |
| List optimization jobs | ✓ | ✓ | ✓ | `prompts:read` |
| Create optimization job | ✓ | ✓ | ✗ | `prompts:create` |
| Update optimization job | ✓ | ✓ | ✗ | `prompts:update` |
| Delete optimization job | ✓ | ✓ | ✗ | `prompts:delete` |
| Invoke prompt canvas | ✓ | ✓ | ✗ | `prompts:update` |
| List quick actions | ✓ | ✓ | ✓ | `prompts:read` |
| Create quick action | ✓ | ✓ | ✓ | `prompts:read` |
| Delete quick action | ✓ | ✓ | ✓ | `prompts:read` |
| Update quick action | ✓ | ✓ | ✓ | `prompts:read` |

> [!NOTE]
>
> Some prompt operations support public access for shared prompts.

### Charts

Custom visualizations and dashboards.

| Operation | Workspace Admin | Workspace Editor | Workspace Viewer | Required Permission |
| - | :-: | :-: | :-: | - |
| List charts | ✓ | ✓ | ✓ | `charts:read` |
| Get chart by ID | ✓ | ✓ | ✓ | `charts:read` |
| Create chart | ✓ | ✓ | ✗ | `charts:create` |
| Update chart | ✓ | ✓ | ✗ | `charts:update` |
| Delete chart | ✓ | ✓ | ✗ | `charts:delete` |
| Render chart | ✓ | ✓ | ✓ | `charts:read` |
| List chart sections | ✓ | ✓ | ✓ | `charts:read` |
| Get chart section by ID | ✓ | ✓ | ✓ | `charts:read` |
| Create chart section | ✓ | ✓ | ✗ | `charts:create` |
| Update chart section | ✓ | ✓ | ✗ | `charts:update` |
| Delete chart section | ✓ | ✓ | ✗ | `charts:delete` |
| Render chart section | ✓ | ✓ | ✓ | `charts:read` |

### Deployments

[LangSmith Agent Server](../../../Deploy/Get%20started/LangSmith%20Agent%20Server.md) configurations.

| Operation | Workspace Admin | Workspace Editor | Workspace Viewer | Required Permission |
| - | :-: | :-: | :-: | - |
| Create deployment | ✓ | ✓ | ✗ | `deployments:create` |
| View deployment | ✓ | ✓ | ✓ | `deployments:read` |
| Update deployment | ✓ | ✓ | ✗ | `deployments:update` |
| Delete deployment | ✓ | ✗ | ✗ | `deployments:delete` |

### Model price map

Per-token model prices used to compute run costs. See [Cost tracking](../../../Monitor/Trace/Configuration%20%26%20troubleshooting/Cost%20tracking.md).

| Operation | Workspace Admin | Workspace Editor | Workspace Viewer | Required Permission |
| - | :-: | :-: | :-: | - |
| View model prices | ✓ | ✓ | ✓ | `model-price-map:read` |
| Create a model price entry | ✓ | ✓ | ✗ | `model-price-map:create` |
| Update a model price entry | ✓ | ✓ | ✗ | `model-price-map:update` |
| Delete a model price entry | ✓ | ✓ | ✗ | `model-price-map:delete` |

> [!NOTE]
>
> These permissions replace the `runs:read` and `runs:create` checks that previously gated model prices. Built-in roles keep the access they had. Custom roles created after this change need the `model-price-map` permissions granted explicitly; they appear as their own checkboxes in the custom role editor.

### Workspace settings and management

| Operation | Workspace Admin | Workspace Editor | Workspace Viewer | Required Permission |
| - | :-: | :-: | :-: | - |
| View workspace info | ✓ | ✓ | ✓ | `workspaces:read` |
| View workspace statistics | ✓ | ✓ | ✓ | `workspaces:read` |
| Update workspace (name, description) | ✓ | ✗ | ✗ | `workspaces:manage` |
| Delete workspace | ✓ | ✗ | ✗ | `workspaces:manage` |
| View workspace members | ✓ | ✓ | ✓ | `workspaces:read` |
| View active workspace members | ✓ | ✓ | ✓ | `workspaces:read` |
| View pending workspace members | ✓ | ✓ | ✓ | `workspaces:read` |
| Add member to workspace | ✓ | ✗ | ✗ | `workspaces:manage-members` |
| Add members (batch) | ✓ | ✗ | ✗ | `workspaces:manage-members` |
| Update workspace member role | ✓ | ✗ | ✗ | `workspaces:manage-members` |
| Remove workspace member | ✓ | ✗ | ✗ | `workspaces:manage-members` |
| Delete pending workspace member | ✓ | ✗ | ✗ | `workspaces:manage-members` |
| View workspace trace retention settings | ✓ | ✓ | ✓ | `workspaces:read` |
| Update workspace extended retention duration (Enterprise) | ✓ | ✗ | ✗ | `workspaces:manage` |
| View usage limits | ✓ | ✓ | ✓ | `workspaces:read` |
| View shared entities | ✓ | ✓ | ✓ | `workspaces:read` |
| Bulk unshare entities | ✓ | ✗ | ✗ | `workspaces:manage` |

### Workspace teams

[Workspace-only members and access policies](Teams.md#add-workspace-only-members-and-policies) that teams have in this workspace. `workspaces:manage` does not allow these operations.

| Operation | Workspace Admin | Workspace Editor | Workspace Viewer | Required Permission |
| - | :-: | :-: | :-: | - |
| View the teams with access to this workspace and their workspace-only members and policies | ✓ | ✓ | ✓ | `workspaces:teams:read` |
| View a team's role in this workspace | ✓ | ✓ | ✓ | `workspaces:teams:read` |
| Add or remove workspace-only members | ✓ | ✗ | ✗ | `workspaces:teams:manage-members` |
| Attach or detach workspace-only access policies | ✓ | ✗ | ✗ | `workspaces:teams:manage-policies` |

### Tags

| Operation | Workspace Admin | Workspace Editor | Workspace Viewer | Required Permission |
| - | :-: | :-: | :-: | - |
| List tag keys | ✓ | ✓ | ✓ | `workspaces:read` |
| Get tag key | ✓ | ✓ | ✓ | `workspaces:read` |
| Create tag key | ✓ | ✗ | ✗ | `workspaces:manage` |
| Update tag key | ✓ | ✗ | ✗ | `workspaces:manage` |
| Delete tag key | ✓ | ✗ | ✗ | `workspaces:manage` |
| List tag values | ✓ | ✓ | ✓ | `workspaces:read` |
| Get tag value | ✓ | ✓ | ✓ | `workspaces:read` |
| Create tag value | ✓ | ✗ | ✗ | `workspaces:manage` |
| Update tag value | ✓ | ✗ | ✗ | `workspaces:manage` |
| Delete tag value | ✓ | ✗ | ✗ | `workspaces:manage` |
| List tags | ✓ | ✓ | ✓ | `workspaces:read` |
| List tags for resource | ✓ | ✓ | ✓ | `workspaces:read` |
| List tags for resources (batch) | ✓ | ✓ | ✓ | `workspaces:read` |
| List taggings | ✓ | ✓ | ✓ | `workspaces:read` |
| Create tagging | ✓ | ✗ | ✗ | `workspaces:manage` |
| Delete tagging | ✓ | ✗ | ✗ | `workspaces:manage` |

### Bulk exports

| Operation | Workspace Admin | Workspace Editor | Workspace Viewer | Required Permission |
| - | :-: | :-: | :-: | - |
| List bulk exports | ✓ | ✓ | ✓ | `bulk-exports:read` |
| Get bulk export | ✓ | ✓ | ✓ | `bulk-exports:read` |
| Get bulk export runs | ✓ | ✓ | ✓ | `bulk-exports:read` |
| Get bulk export run | ✓ | ✓ | ✓ | `bulk-exports:read` |
| Create bulk export | ✓ | ✗ | ✗ | `bulk-exports:manage` |
| Cancel bulk export | ✓ | ✗ | ✗ | `bulk-exports:manage` |
| Get bulk export destinations | ✓ | ✓ | ✓ | `bulk-exports:read` |
| Get bulk export destination | ✓ | ✓ | ✓ | `bulk-exports:read` |
| Create bulk export destination | ✓ | ✗ | ✗ | `bulk-exports:manage` |
| Update bulk export destination | ✓ | ✗ | ✗ | `bulk-exports:manage` |
| Get filtered export runs | ✓ | ✓ | ✓ | `bulk-exports:read` |

> [!TIP]
>
> `bulk-exports:read` and `bulk-exports:manage` are dedicated permissions that allow you to grant export access via a [custom role](Role-based%20access%20control.md#custom-roles) without granting the broader `workspaces:manage` scope. This is useful for security-team service keys that need to export traces but should not be able to manage workspaces, members, or secrets.

### MCP servers

Model Context Protocol servers for extended functionality.

| Operation | Workspace Admin | Workspace Editor | Workspace Viewer | Required Permission |
| - | :-: | :-: | :-: | - |
| List MCP servers | ✓ | ✓ | ✓ | `workspaces:read` |
| Get MCP server | ✓ | ✓ | ✓ | `workspaces:read` |
| Create MCP server | ✓ | ✓ | ✓ | `workspaces:read` |
| Update MCP server | ✓ | ✓ | ✓ | `workspaces:read` |
| Delete MCP server | ✓ | ✓ | ✓ | `workspaces:read` |

### Fleet

[Fleet](../../../No-code%20agents/Fleet/No-code%20agents%20with%20LangSmith%20Fleet.md) workspace administration operations.

| Operation | Workspace Admin | Workspace Editor | Workspace Viewer | Required Permission |
| - | :-: | :-: | :-: | - |
| View Fleet admin section (usage, spend) | ✓ | ✗ | ✗ | `fleet:read-admin-config` |
| Manage Fleet spend limits | ✓ | ✗ | ✗ | `fleet:write-admin-config` |

## User-level operations

These operations are available to all authenticated users and don't require specific workspace or organization permissions:

* View own user profile
* Update own user profile
* List organizations for user
* Create new organization
* List pending workspace invites
* Delete pending workspace invite
* Claim pending workspace invite
* List pending organization invites
* Delete pending organization invite
* Claim pending organization invite

## Permission inheritance

### Organization to workspace

* [Organization Admin](Role-based%20access%20control.md#organization-admin) automatically has full permissions in all workspaces.
* [Organization Operator](Role-based%20access%20control.md#organization-operator) only gets workspace access when explicitly added to workspaces with workspace-level roles (or to workspaces they create).
* [Organization User](Role-based%20access%20control.md#organization-user) and [Organization Viewer](Role-based%20access%20control.md#organization-viewer) only get workspace access when explicitly added to workspaces with workspace-level roles.
* A workspace member who belongs to a [team](Teams.md) with access to that workspace also receives the team's workspace role.
* [Organization Restricted](Role-based%20access%20control.md#organization-restricted) users only get workspace access when explicitly added to workspaces with workspace-level roles. Workspace-scoped service keys with this role get access only to the workspaces selected for the key.

For detailed role definitions, refer to [Organization roles](Role-based%20access%20control.md#organization-roles) and [Workspace roles](Role-based%20access%20control.md#workspace-roles).

### Workspace role independence

* Users can have different workspace roles in different workspaces.
* A user might be a [Workspace Admin](Role-based%20access%20control.md#workspace-admin) in one workspace and a [Workspace Viewer](Role-based%20access%20control.md#workspace-viewer) in another.

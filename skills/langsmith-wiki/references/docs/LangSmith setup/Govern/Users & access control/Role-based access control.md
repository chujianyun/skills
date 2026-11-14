# Role-based access control

This reference explains LangSmith's Role-Based Access Control (RBAC) system for managing organization-level and workspace-level permissions.

> [!NOTE]
>
> RBAC (Role-Based Access Control) is an Enterprise feature for managing workspace-level permissions. If you are interested in this feature, [contact our sales team](https://www.langchain.com/contact-sales). Other plans default to using the Admin role for all users.

LangSmith's RBAC system manages user permissions within workspaces. RBAC allows you to control who can access your LangSmith [workspace](../Organization/Overview.md#workspaces) and what they can do within it.

In LangSmith, each user has:

* One [**organization role**](#organization-roles) that applies across the entire organization (separate from workspace RBAC).
  * The Organization User and Organization Viewer roles are only available in organizations on [Plus and Enterprise plans](https://langchain.com/pricing). In Developer organizations (single workspace), all users are assigned the Organization Admin role by default.
* One assigned [**workspace role**](#workspace-roles) per workspace they are a member of (requires Enterprise RBAC feature).

A user can also receive additional workspace roles through [teams](Teams.md). The user then holds the permissions of their assigned role and of each team's role in that workspace.

On Enterprise plans, organizations can also create [custom workspace roles](#custom-roles) with granular permission combinations.

To learn how to set up RBAC and assign roles to users, refer to the [User Management guide](User%20management.md#set-up-access-control). Your identity provider can also assign roles automatically via [SCIM groups](User%20management.md#set-up-scim-for-your-organization) or [SSO Groups Sync](User%20management.md#sso-groups-sync-alternative).

> [!NOTE]
>
> For a comprehensive list of required permissions along with the operations and roles that can perform them, refer to the [Organization and workspace reference](Organization%20and%20workspace%20operations%20reference.md).

## Organization roles

Organization roles control what a user can do across the organization, such as managing billing, members, and workspaces. They are separate from [workspace roles](#workspace-roles), which control access to resources inside a workspace. Organization roles are system-defined and cannot be modified or extended.

| Role | Description | Availability |
| - | - | - |
| [Organization Admin](#organization-admin) | Full permissions to manage organization configuration, users, billing, and workspaces | All plans |
| [Organization Operator](#organization-operator) | Management access to workspaces and users for day-to-day operations, excluding admin-level privileges | [Plus and Enterprise](https://langchain.com/pricing) |
| [Organization User](#organization-user) | Read access to organization information and ability to create personal access tokens | [Plus and Enterprise](https://langchain.com/pricing) |
| [Organization Viewer](#organization-viewer) | Read-only access to organization information | [Plus and Enterprise](https://langchain.com/pricing) |
| [Organization Restricted](#organization-restricted) | Workspace access without organization-wide read access | [Plus and Enterprise](https://langchain.com/pricing) |

> [!NOTE]
>
> In Developer organizations (single workspace), all users are assigned the [Organization Admin](#organization-admin) role by default.

### Organization Admin

**Description**: Full permissions to manage all organization configuration, users, billing, and workspaces.

**Permissions**:

* `organization:manage` - Full control over organization settings, SSO, security, billing
* `organization:read` - Read access to all organization information
* `organization:pats:create` - Create organization-level [personal access tokens](../Organization/Overview.md#personal-access-tokens-pats)
* `organization:pats:read` - View every organization member's personal access tokens
* `organization:pats:manage` - Deactivate, reactivate, or delete any organization member's personal access token

For a comprehensive list of required permissions along with the operations and roles that can perform them, refer to the [Organization and workspace reference](Organization%20and%20workspace%20operations%20reference.md).

**Key Capabilities**:

* Manage [organization settings](../Organization/Workspace%20setup/Set%20up%20hierarchy.md#set-up-an-organization) and branding
* Configure [SSO and authentication methods](User%20management.md#set-up-saml-sso-for-your-organization)
* Manage [billing](../../Account/Billing%20%26%20usage/Manage%20billing%20in%20your%20account.md) and subscription plans
* Create and delete [workspaces](../Organization/Workspace%20setup/Set%20up%20hierarchy.md)
* Invite and remove organization members
* View, deactivate, reactivate, and delete any member's [personal access tokens](../Organization/Overview.md#personal-access-tokens-pats)
* Assign organization and workspace roles to members
* Create and manage [custom roles](#custom-roles)
* Configure RBAC and ABAC (Attribute-Based Access Control) policies
* View organization [usage](../../../Monitor/Trace/Configuration%20%26%20troubleshooting/Usage%20and%20billing.md#usage-limits) and analytics
* View [audit logs](../Auditing/Audit%20logs.md) (Enterprise)

For details on setting up and managing your organization, refer to the [Administration Overview](../Organization/Overview.md#organizations).

### Organization Operator

Management access for day-to-day operations including workspace and user management, but cannot manage Organization Admins or create organization-wide service keys.

**Permissions:**

* `organization:manage` - Control over organization settings, workspaces, and non-admin users
* `organization:read` - Read access to all organization information
* `organization:pats:create` - Create personal access tokens
* `organization:pats:read` - View every organization member's personal access tokens
* `organization:pats:manage` - Deactivate, reactivate, or delete any organization member's personal access token

For a comprehensive list of required permissions along with the operations and roles that can perform them, refer to the [Organization and workspace reference](Organization%20and%20workspace%20operations%20reference.md).

**Key Capabilities:**

* Create and manage [workspaces](../Organization/Workspace%20setup/Set%20up%20hierarchy.md#set-up-a-workspace)
* Invite organization members (all roles except Organization Admin)
* Manage non-admin organization members (modify and remove Organization Users, Viewers, and Operators)
* View, deactivate, reactivate, and delete any member's [personal access tokens](../Organization/Overview.md#personal-access-tokens-pats)
* Assign workspace roles to members
* Create workspace-scoped service keys and service accounts
* Manage organization [billing](../../Account/Billing%20%26%20usage/Manage%20billing%20in%20your%20account.md) and subscription plans
* Create, edit, and delete [custom roles](#custom-roles)
* Configure [SSO and authentication methods](User%20management.md#set-up-saml-sso-for-your-organization)
* View organization [usage](../../../Monitor/Trace/Configuration%20%26%20troubleshooting/Usage%20and%20billing.md#usage-limits) and analytics
* View [audit logs](../Auditing/Audit%20logs.md) (Enterprise)

**Restrictions:**

* Cannot invite, modify, or remove Organization Admins
* Cannot assign the Organization Admin role to users
* Cannot create organization-wide (non-workspace-specific) service keys
* Not automatically added to existing workspaces (only added to workspaces they create or are explicitly invited to)

### Organization User

**Description**: Read access to organization information and ability to create personal access tokens.

**Permissions**:

* `organization:read` - Read access to organization information
* `organization:pats:create` - Create personal access tokens

For a comprehensive list of required permissions along with the operations and roles that can perform them, refer to the [Organization and workspace reference](Organization%20and%20workspace%20operations%20reference.md).

**Key Capabilities**:

* View organization members and workspaces
* View organization settings (but not modify)
* Create [personal access tokens](../Organization/Overview.md#personal-access-tokens-pats) for API access
* Join workspaces they're invited to

**Restrictions**:

* Cannot modify organization settings
* Cannot manage billing or subscriptions
* Cannot create or delete workspaces
* Cannot invite or remove organization members
* Cannot manage roles or permissions

You can add an Organization User to a subset of workspaces and assigned workspace roles (if RBAC is enabled), which specify permissions at the workspace level.

### Organization Viewer

**Description**: Read-only access to organization information.

**Permissions**:

* `organization:read` - Read access to organization information

For a comprehensive list of required permissions along with the operations and roles that can perform them, refer to the [Organization and workspace reference](Organization%20and%20workspace%20operations%20reference.md).

**Key Capabilities**:

* View organization members and workspaces
* View organization settings

**Restrictions**:

* Cannot modify anything at the organization level
* Cannot create personal access tokens
* Cannot manage billing, workspaces, or members

### Organization Restricted

Organization Restricted permits access to assigned workspaces without organization-wide read access. Assign it to users who should work in their own workspaces without seeing other organization members or organization-level details.

Assign Organization Restricted to a user the same way as any other organization role: through a member invite, a [SCIM group](User%20management.md#group-naming-convention), or an [SSO Groups Sync](User%20management.md#sso-groups-sync-alternative) group match. [Just-in-time (JIT) provisioning](Manage%20user%20access%20in%20SSO%20organizations.md) cannot assign it: new users created through JIT receive Organization User, and the SSO default role setting applies only to workspace roles.

The role includes `organization:read-metadata`, but not `organization:read`. Users and keys with this role cannot list organization members or service keys. Organization role metadata remains visible. What a user or key can do inside an assigned workspace, including viewing that workspace's members, depends on its workspace role.

Workspace-scoped [service keys](../Organization/Overview.md#service-keys) can also hold this role. When creating or editing a service key scoped to **Specific Workspaces**, choose Organization Viewer (the default) or Organization Restricted. This choice does not change who can create or edit service keys.

## Workspace roles

Workspace roles are part of the **Enterprise RBAC feature** and control what users can do with resources inside a workspace:

| Role | Description |
| - | - |
| [Workspace Admin](#workspace-admin) | Full permissions for all resources, including workspace settings and member management |
| [Workspace Editor](#workspace-editor) | Full permissions for most resources, cannot manage workspace settings or delete certain resources |
| [Workspace Viewer](#workspace-viewer) | Read-only access to all workspace resources |

> [!NOTE]
>
> RBAC (Role-Based Access Control) is a feature that is only available to [Enterprise](https://langchain.com/pricing) customers. If you are interested in this feature, [contact our sales team](https://www.langchain.com/contact-sales). Other plans default to using the Admin role for all users.

### Workspace Admin

**Description**: Role with full permissions for all resources and ability to manage workspace.

**Permissions**:

* All create, read, update, delete, and share permissions for all resource types
* Workspace management capabilities

For a comprehensive list of required permissions along with the operations and roles that can perform them, refer to the [Organization and workspace reference](Organization%20and%20workspace%20operations%20reference.md).

### Workspace Editor

**Description**: Role with full permissions for most resources. Cannot manage workspace settings or delete certain critical resources.

**Key Differences from Admin**:

* Cannot delete [runs](../../../Monitor/Trace/Observability%20concepts.md#runs)
* Cannot manage workspace settings (change workspace name, etc.)
* Cannot manage workspace members (add, remove, or update member roles)

### Workspace Viewer

**Description**: Read-only access to all workspace resources.

**Permissions**: Read-only access to all resource types.

For a comprehensive list of required permissions along with the operations and roles that can perform them, refer to the [Organization and workspace reference](Organization%20and%20workspace%20operations%20reference.md).

> [!TIP]
>
> For step-by-step instructions on assigning workspace roles to users, refer to the [User Management guide](User%20management.md#assign-a-role-to-a-user).

## Custom roles

> [!NOTE]
>
> Creating custom roles is only available for organizations on the Enterprise plan.

Custom roles are workspace roles that you define. [Organization Admins](#organization-admin) and [Organization Operators](#organization-operator) can create custom roles with specific combinations of workspace-level permissions, then assign them alongside the built-in [workspace roles](#workspace-roles).

### Create a custom role

Custom roles are created at the [organization](../Organization/Overview.md#organizations) level and can be assigned to users in any [workspace](../Organization/Overview.md#workspaces) within that organization.

To create a custom role:

1. Navigate to Organization **Settings** > **Roles**.
2. Click **Create Role**.
3. Enter a **Role Name** and, optionally, a **Description**.
4. Under **Permissions**, select the permissions to include in the role.
5. Click **Create**.

After you create the role, [assign it to users](User%20management.md#assign-a-role-to-a-user) in specific workspaces.

For details on which specific permissions are required for each operation, refer to the [Organization and workspace operations reference](Organization%20and%20workspace%20operations%20reference.md).

Note the following details on custom roles:

* Only Organization Admins and Organization Operators can create and manage custom roles.
* Custom roles are organization-specific (not transferable between organizations).
* Each custom role can have any combination of workspace-level permissions.
* Custom roles cannot have organization-level permissions.
* Users can have different roles (including custom roles) in different workspaces.

### Understand permission behavior

Some permissions offer granular control when used in custom roles:

* `workspaces:manage` does **not** include the ability to manage workspace members. To allow a custom role to add, remove, or update workspace members, you must explicitly grant `workspaces:manage-members`. The built-in Workspace Admin role includes both permissions automatically.
* `workspaces:manage-model-configs` controls the ability to create, edit, or delete [model configurations](../Organization/Workspace%20setup/Manage%20model%20configurations.md) (including attaching [OAuth client credentials](../Organization/Workspace%20setup/Manage%20model%20configurations.md#oauth-client-credentials)) and to change which LangSmith features each model is available in. It is separate from `workspaces:manage`—grant it explicitly on custom roles that should be able to configure models. The built-in Workspace Admin role includes it automatically.
* `workspaces:manage-keys` controls the ability to create and delete workspace API keys (service keys scoped to a workspace). It is separate from `workspaces:manage`—grant it explicitly on custom roles that should be able to manage API keys without full workspace management. To prevent privilege escalation, a key created by a user who does not have `workspaces:manage` cannot be granted more permissions than that user holds, and cannot be assigned a role the organization has marked restricted. The built-in Workspace Admin role includes it automatically.
* `bulk-exports:read` and `bulk-exports:manage` cover the bulk export endpoints (listing, creating, cancelling exports, and managing destinations). Use them in a custom role to grant least-privilege bulk export access without `workspaces:manage`. The built-in Workspace Admin role includes `bulk-exports:manage` and all read-capable roles include `bulk-exports:read` automatically.
* `projects:increase-trace-tier` and `projects:decrease-trace-tier` are independent and can be granted separately. For example, you can allow a role to decrease retention without allowing it to increase retention. If a user lacks both permissions, the retention settings UI is hidden entirely. If they have only one, the UI is partially enabled (the disallowed direction is disabled).
* `runs:read-inputs` and `runs:read-outputs` control whether a role can see run inputs and outputs, and are separate from `runs:read`. A role with `runs:read` but without one of these permissions can still list and open runs, but responses leave out the denied field and its preview. Message and trajectory views require both permissions. To hide inputs or outputs only in specific projects, use an [access policy](Attribute-based%20access%20control.md#control-access-to-run-inputs-and-outputs).
* `projects:update` covers only metadata updates (name, description, tags) and does **not** grant the ability to change trace retention. To allow a custom role to modify trace tier, you must explicitly grant `projects:increase-trace-tier`, `projects:decrease-trace-tier`, or both.

## Restrict roles

> [!NOTE]
>
> Role restriction is available for organizations on the [Enterprise](https://docs.langchain.com/langsmith/pricing-plans.md) plan.

[Organization Admins](#organization-admin) and [Organization Operators](#organization-operator) (roles with the `organization:manage` permission) can mark any role—system or custom—as **restricted**. Restricted roles can only be assigned to workspace members by users who hold the built-in [Workspace Admin](#workspace-admin) role. Users who have the `workspaces:manage-members` permission but do not hold the Workspace Admin role cannot assign restricted roles.

This prevents privilege escalation: even if a user is authorized to manage workspace membership, they cannot grant roles that have been marked out of bounds for them.

No roles are restricted by default. Organizations must explicitly restrict each role.

To restrict a role, in the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-rbac):

1. Navigate to Organization **Settings** > **Roles**.
2. Find the role you want to restrict in the Roles table.
3. Select the **Restricted** checkbox for that role.

After a role is restricted, users who do not hold the Workspace Admin role cannot see or assign it in the member invite, member edit, or API key creation flows. The API also rejects assignment attempts from callers who do not hold the Workspace Admin role. If a user who does not hold the Workspace Admin role creates an API key, they cannot use their own restricted role as the key's default role.

To unrestrict a role, follow the same steps and clear the **Restricted** checkbox.

> [!NOTE]
>
> Role restriction applies to both system roles (Workspace Admin, Workspace Editor, Workspace Viewer) and custom roles. It is available on LangSmith [Cloud](../../Cloud/Cloud%20%28SaaS%29.md) and [Self-hosted](../../Self-hosted/Self-hosted%20LangSmith.md).

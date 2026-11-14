# Set up hierarchy

This page describes setting up and managing your LangSmith [*organization*](../Overview.md#organizations) and [*workspaces*](../Overview.md#workspaces):

* [Set up an organization](#set-up-an-organization): Create and manage organizations for user collaboration, including user management and role assignments.
* [Set up a workspace](#set-up-a-workspace): Configure workspaces to organize your LangSmith resources, manage workspace members, and define collaboration settings.
* [Set up agents and applications](#set-up-agents-and-applications): Group resources within a workspace to further organize them, and take advantage of ABAC permissioning.

> [!TIP]
>
> You may find it helpful to refer to the [overview on LangSmith resource hierarchy](../Overview.md) before you read this setup page.

## Set up an organization

> [!NOTE]
>
> If you're interested in managing your organization and workspaces programmatically, refer to [Manage organizations using the API](../Manage%20your%20organization%20using%20the%20API.md).

### Create an organization

When you log into the [UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-set-up-hierarchy) for the first time, LangSmith will create a personal organization for you automatically. If you'd like to collaborate with others, you can create a separate organization and invite your colleagues to join.

1. Open the **Organizations** drawer by clicking your profile icon in the bottom left
2. Select the organization profile dropdown at the top of the menu.
3. Click **+ Create organization**.

Shared organizations require a credit card before you can use them. You will need to [set up billing](../../../Account/Billing%20%26%20usage/Manage%20billing%20in%20your%20account.md#set-up-billing-for-your-account) to proceed.

### Manage and navigate workspaces

Once you've subscribed to a [plan](https://docs.langchain.com/langsmith/pricing-plans.md) that allows for multiple users per organization, you can set up [workspaces](../Overview.md#workspaces) to collaborate more effectively and isolate LangSmith resources between different groups of users. To navigate between workspaces and access the resources within each workspace (trace projects, annotation queues, etc.), select the desired workspace from the picker in the bottom left of the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-set-up-hierarchy).

### Manage users

Manage membership in your shared organization on the **Members** page of the [organization settings](https://smith.langchain.com/settings). Here you can:

* Invite new users to your organization, selecting workspace membership and (if [RBAC](../../Users%20%26%20access%20control/Role-based%20access%20control.md) is enabled) workspace role.
* Edit a user's organization role.
* Remove users from your organization.

Organizations on the [Enterprise plan](https://docs.langchain.com/langsmith/pricing-plans.md) may set up custom workspace roles in the **Roles** tab. For more details, refer to the [access control setup guide](../../Users%20%26%20access%20control/User%20management.md).

#### Organization roles

Organization-scoped roles are used to determine access to organization settings. The role selected also has an impact on workspace membership:

* **Organization Admin** grants full access to manage all organization configuration, users, billing, and workspaces. Any Organization Admin has `Admin` access to all workspaces in an organization.
* **Organization User** may read organization information, but cannot execute any write actions at the organization level. You can add an Organization User to a subset of workspaces and assigned workspace roles as usual (if [RBAC](../../Users%20%26%20access%20control/Role-based%20access%20control.md) is enabled), which specify permissions at the workspace level.

> [!NOTE]
>
> The [Organization User](../../Users%20%26%20access%20control/Role-based%20access%20control.md#organization-user) and [Organization Viewer](../../Users%20%26%20access%20control/Role-based%20access%20control.md#organization-viewer) roles are only available in organizations on [Plus and Enterprise plans](https://langchain.com/pricing). In Developer organizations (single workspace), all users are assigned the [Organization Admin](../../Users%20%26%20access%20control/Role-based%20access%20control.md#organization-admin) role by default. Custom organization-scoped roles are not available.

For a full list of permissions associated with each role, refer to the [Administration overview](../Overview.md#organization-roles) page.

## Set up a workspace

When you log in for the first time, LangSmith will create a default [workspace](../Overview.md#workspaces) for you in your personal organization. You can use workspaces to separate resources between different business units to establish clear trust boundaries between them. Within each workspace, [Role-Based Access Control (RBAC)](../../Users%20%26%20access%20control/Role-based%20access%20control.md) manages permissions and access levels, which ensures that users only have access to the resources and settings necessary for their role. Most LangSmith activity happens in the context of a workspace, each of which has its own settings and access controls.
For guidance on choosing the right workspace organization model, refer to [Workload isolation](Workload%20isolation.md).

For what changes when a workspace moves from tracing projects to agents and environments, refer to [How agent-based workspaces differ](How%20agent-based%20workspaces%20differ.md).

### Create a workspace

To create a new workspace, navigate to the [**Settings** page](https://smith.langchain.com/settings) **Workspaces** tab in your shared organization and click **Add Workspace**.

Once you have created your workspace, you can manage its members and other configuration by selecting the workspace on the **Settings** page.

> [!NOTE]
>
> Different plans have different limits placed on the number of workspaces that you can use in an organization. For more information, refer to the [pricing page](https://www.langchain.com/pricing-langsmith).

### Manage users

> [!NOTE]
>
> Only [workspace admins](../../Users%20%26%20access%20control/Role-based%20access%20control.md#workspace-admin) can manage workspace membership and, if RBAC is enabled, change a user's workspace role.

For users that are already members of an organization, a workspace admin may add them to a workspace in the **Workspace members** tab on the [**Workspaces settings** page](https://smith.langchain.com/settings/workspaces). Users may also be invited directly to one or more workspaces when they are invited to an organization.

A user can also receive a workspace role through a [team](../../Users%20%26%20access%20control/Teams.md) that has access to the workspace.

### Configure workspace settings

Workspace settings are on the [**Settings** page](https://smith.langchain.com/settings/workspaces) for the selected workspace. Options include the ability to configure members, [model configurations](Manage%20model%20configurations.md), [shared URLs](../../../../Monitor/Debug/Viewing%20%26%20managing%20traces/Manage%20a%20trace.md), and resource tags for [grouping resources](#set-up-agents-and-applications).

Workspace secrets store the API keys that LangSmith uses to call model providers and tools. Add them under  **Settings** > **Integrations** > **Provider secrets**.

### Delete a workspace

> [!WARNING]
>
> Deleting a workspace will permanently delete the workspace and all associated data. This action cannot be undone.

You can delete a workspace through the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-set-up-hierarchy) or via [API](../../../../Monitor/Reference/LangSmith%20REST%20API/Administration/Delete%20workspace.md). You must be a [workspace admin](../../Users%20%26%20access%20control/Role-based%20access%20control.md#workspace-admin) in order to delete a workspace.

In the LangSmith UI:

1. Navigate to **Settings**.
2. Select the workspace you want to delete.
3. Click the delete icon  in the top-right corner of the screen.

## Set up agents and applications

Within a workspace you can group resources, such as tracing projects and datasets, one level further. A workspace may have zero or more of these groups.

What the group is called depends on which information architecture your workspace uses, and the control at the top left tells you which one you are on. An agent-based workspace calls it an [agent](../../../Overview/Agent-based%20workspaces/Agent%20Registry.md#agent) and selects it from the agent picker in the top bar. A project-based workspace calls it an application and selects it from the **Application** picker in the sidebar.

To view every resource in the workspace rather than one group's, select **All agents** in the agent picker, or **All applications** in the application picker. You may tag resources to multiple applications by adding them to the `Application` tag under **Resource Tags** on the **Settings** page.

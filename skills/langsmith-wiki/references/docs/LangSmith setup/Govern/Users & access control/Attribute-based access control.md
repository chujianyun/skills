# Attribute-based access control

> Grant or restrict access to LangSmith resources based on resource tags and root run metadata, using access policies that build on role-based access control.

Attribute-based access control (ABAC) lets organization administrators grant or restrict access to LangSmith resources based on the resources' attributes.

It builds on [role-based access control (RBAC)](Role-based%20access%20control.md). A role grants a permission across a whole workspace, such as reading every project. An access policy narrows or extends that permission to the resources whose attributes match, such as projects tagged `Environment=Development`.

Access policies can match two kinds of attributes:

* **Resource tags** (`resource_tag_key`): The [resource tags](../Organization/Workspace%20setup/Set%20up%20resource%20tags.md) on projects, datasets, prompts, and other workspace resources.
* **Root run metadata** (`root_run_metadata`): The metadata on the root run of each trace. Use it to control which traces a user can read within a project. For details, refer to [Control trace access with root run metadata](#control-trace-access-with-root-run-metadata).

> [!NOTE]
>
> ABAC is available on Enterprise plans. If you are interested in this feature, [contact our sales team](https://www.langchain.com/contact-sales). Other plans default to using the Admin role for all users.

## Before you begin

You must have:

* **ABAC enabled for your organization**: On LangSmith Cloud, ABAC is part of the Enterprise plan. On a self-hosted deployment, [enable ABAC](#enable-abac-on-a-self-hosted-deployment) first.
* **Permission to manage policies**: Creating, editing, or deleting a policy requires `organization:access-control:manage`, which [Organization Admins](Role-based%20access%20control.md#organization-admin) and [Organization Operators](Role-based%20access%20control.md#organization-operator) hold.
* **Resource tags**: For tag-based conditions, [set up resource tags](../Organization/Workspace%20setup/Set%20up%20resource%20tags.md) in your workspace. Policies that use only root run metadata do not require resource tags.
* **API credentials**: To manage policies with the API, use a personal access token (PAT) from a user with `organization:access-control:manage`, or an organization-scoped service key with Organization Admin permissions. Send requests to your API URL. For LangSmith Cloud, find the API URL for your region in [Regional storage](../../Cloud/Cloud%20%28SaaS%29.md#regional-storage). For a self-hosted deployment, use `https://<your-langsmith-domain>/api`.

## Enable ABAC on a self-hosted deployment

ABAC on a [self-hosted](../../Self-hosted/Self-hosted%20LangSmith.md) deployment requires Helm chart 0.11.28 or later (application version 0.12.1). After you upgrade, use one of the following options to enable it:

* **Enable for a specific organization**: Run the following against your LangSmith PostgreSQL database, replacing `<organization_id>` with the ID copied from the organization settings page in the UI:

  ```sql
  UPDATE organizations SET config = config || '{"can_use_abac": true}' WHERE id = '<organization_id>' AND NOT is_personal;
  ```

* **Enable for all organizations**: Add the following environment variable to `commonEnv` in your `values.yaml`:

  ```yaml
  DEFAULT_ORG_FEATURE_CAN_USE_ABAC: "true"
  ```

  > [!NOTE]
  >
  > This environment variable has no effect on personal organizations because [RBAC](Role-based%20access%20control.md) is not enabled for personal organizations.

## Access policy structure

An access policy is a JSON object that sets an effect, one or more condition groups, and the roles the policy applies to:

```json
{
  "name": "Policy Name",
  "description": "Optional description",
  "effect": "allow | deny",
  "condition_groups": [
    {
      "permission": "projects:read",
      "resource_type": "project",
      "conditions": [
        {
          "attribute_name": "resource_tag_key",
          "attribute_key": "Environment",
          "operator": "equals",
          "attribute_value": "Production"
        }
      ]
    }
  ],
  "role_ids": ["<role-uuid>"]
}
```

### Effect

The `effect` determines what happens when conditions match:

* **`allow`**: Grant access when conditions match.
* **`deny`**: Block access when conditions match.

> [!NOTE]
>
> Deny policies always take precedence. If both an allow and deny policy match, access is denied.

### Condition groups

The `condition_groups` array contains one or more condition groups. LangSmith evaluates multiple condition groups with **OR logic**. If any group matches, the policy applies.

Each condition group has the following fields:

* **`permission`**: The permission this group applies to.
* **`resource_type`**: The resource type to match.
* **`conditions`**: An array of conditions, evaluated with **AND logic** within the group.

#### Resource types and permissions

| Resource type | Supported permissions |
| - | - |
| `project` | `projects:read`, `projects:update`, `projects:delete`, `runs:read`, `runs:read-inputs`, `runs:read-outputs`, `runs:share`, `runs:delete`, `projects:increase-trace-tier`, `projects:decrease-trace-tier` |
| `prompt` | `prompts:read`, `prompts:update`, `prompts:delete`, `prompts:share`, `prompts:tag` |
| `dataset` | `datasets:read`, `datasets:update`, `datasets:delete`, `datasets:share`, `datasets:download`, `datasets:clone` |
| `deployment` | `deployments:read`, `deployments:update`, `deployments:delete` |
| `queues` | `annotation-queues:create`, `annotation-queues:delete`, `annotation-queues:read`, `annotation-queues:update` |
| `mcp_server` | `mcp-servers:read`, `mcp-servers:invoke`, `mcp-servers:update`, `mcp-servers:delete`. See [Fleet tool access control](../../../No-code%20agents/Fleet/Additional%20resources/Access%20%26%20oversight.md#tool-access-control). |
| `fleet_integration` | `mcp-servers:read`, `mcp-servers:invoke`. See [Fleet tool access control](../../../No-code%20agents/Fleet/Additional%20resources/Access%20%26%20oversight.md#tool-access-control). |

Some resource types are evaluated differently:

* **Runs**: Runs do not have their own tags. Run permissions (`runs:read`, `runs:read-inputs`, `runs:read-outputs`, `runs:create`, `runs:share`, `runs:delete`) are evaluated against the parent project's tags. For how the input and output permissions affect responses, refer to [Control access to run inputs and outputs](#control-access-to-run-inputs-and-outputs).
* **Agent environments**: In an [agent-based workspace](../../Overview/Agent-based%20workspaces/Agent%20Registry.md), a tracing project is one [environment](../../Overview/Agent-based%20workspaces/Agent%20environments.md) of an agent. A `project` condition group applies to each environment separately rather than to the agent as a whole.
* **Dataset clones**: Cloning copies examples from a source dataset to a target dataset. LangSmith checks `datasets:clone` twice, once against each dataset's tags. A policy must grant `datasets:clone` on both datasets.

#### Conditions

Each condition in the `conditions` array has the following fields:

* **`attribute_name`**: `resource_tag_key` to match resource tags, or `root_run_metadata` to match root run metadata.
* **`attribute_key`**: The tag key or metadata key to match, such as `Environment` or `Application`.
* **`operator`**: The comparison operator.
* **`attribute_value`**: The value to compare against.

The operators below apply to `resource_tag_key` conditions. `root_run_metadata` conditions support only `equals`. For their rules, refer to [Control trace access with root run metadata](#control-trace-access-with-root-run-metadata).

#### Operators

| Operator | Description |
| - | - |
| `equals` | Exact match (case sensitive) |
| `not_equals` | Values differ (case sensitive) |
| `equals_ignore_case` | Exact match (case insensitive) |
| `not_equals_ignore_case` | Values differ (case insensitive) |
| `matches` | Glob pattern matching with `*` and `?` wildcards |
| `not_matches` | Match when value does not match glob pattern |

#### `_if_exists` variants

Each operator has an `_if_exists` variant that matches by default when the tag key is absent, or evaluates the condition normally when the tag exists:

| Operator | Description |
| - | - |
| `equals_if_exists` | Exact match (case sensitive), or if tag key absent |
| `not_equals_if_exists` | Values differ (case sensitive), or if tag key absent |
| `equals_ignore_case_if_exists` | Exact match (case insensitive), or if tag key absent |
| `not_equals_ignore_case_if_exists` | Values differ (case insensitive), or if tag key absent |
| `matches_if_exists` | Glob pattern match, or if tag key absent |
| `not_matches_if_exists` | Match when value does not match glob pattern, or if tag key absent |

> [!TIP]
>
> In an **allow** policy, `_if_exists` variants grant access to resources that either match the condition or do not have the specified tag key. In a **deny** policy, they block resources that either match the condition or do not have the tag key.

### Roles

The `role_ids` array specifies which workspace roles the policy applies to. When a user with that role accesses a resource, the policy conditions are evaluated.

Policies can be attached to [workspace roles](Role-based%20access%20control.md#workspace-roles) (built-in or [custom](Role-based%20access%20control.md#custom-roles)) when creating the policy, or attached later in the UI or with the API.

Policies can also be attached to [teams](Teams.md#access-policies). A team's policies apply to its members in the workspaces the team can access.

To provision users into roles automatically from your identity provider, see [SCIM](User%20management.md#set-up-scim-for-your-organization).

## Managing access policies

Manage access policies in your organization settings with the visual editor, or with the [LangSmith API](https://api.smith.langchain.com/docs#/access_policies). Both require `organization:access-control:manage`.

### Create an access policy in the UI

In the visual editor, each **rule** corresponds to a [condition group](#condition-groups).

To create an access policy:

1. Go to **Settings**, and select **Organization**. Then go to **Permissions** > **Access Policies**. In some versions of the settings page, this page is listed as **ABAC** under **Access and Security**.
2. Under **ABAC**, select the **Policies** tab, and then click **Create Policy**.
3. Enter a **Name** and, optionally, a **Description**.
4. Set **Effect** to **Allow** or **Deny**.
5. Click **Add rule**, and then select a **Resource Type** and **Permission**.
6. Click **Add condition**, and choose the condition source:
   * **Resource tag**: Enter a **Tag Key**, operator, and **Tag Value**. [Create the resource tags](../Organization/Workspace%20setup/Set%20up%20resource%20tags.md) before using them in a policy.
   * **Root-run metadata**: First select **Project** for **Resource Type** and `runs:read` for **Permission**. Enter a **Metadata Key** and a **Metadata Value**. The operator is fixed to `equals`, and **Metadata Value** is prefilled with `${user.ls_user_id}`, which matches the current user. Replace it with a literal value to match a fixed value instead. For requirements and an example, refer to [Create a root run metadata policy in the UI](#create-a-root-run-metadata-policy-in-the-ui).
7. Click **Save condition**, add any more conditions, and then click **Add rule** to return to the policy editor. All conditions within a rule must match, and multiple rules use OR logic.
8. (Optional) Attach the policy to roles. A policy has no effect until you attach it to a role or [team](Teams.md#access-policies). In the dialog under **Roles**, click **Add role**. Select the workspace roles the policy applies to, and click **Add roles**. You can inspect each role's permissions before adding it. You can also attach a policy to roles later.
9. To finish, click **Create policy**.

> [!TIP]
>
> To write the policy as JSON instead, click the **JSON editor** icon () beside **UI** in the policy editor. The JSON editor shows the policy built so far in the [access policy structure](#access-policy-structure).

### Edit or delete an access policy

On the **Policies** tab, use the icons in a policy's **Actions** column. To edit a policy, including attaching or detaching roles, click its edit icon, make your changes, and click **Save changes**. To delete a policy, click its delete icon, enter the policy's name to confirm, and click **Delete**.

> [!WARNING]
>
> Deleting a policy removes its role and team attachments. Deleting a deny policy may grant access. Deleting an allow policy may remove access.

### Attach policies to teams

[Teams](Teams.md) do not create policies. They attach existing ones:

* Attaching a policy to a team requires `organization:teams:manage-policies`.
* A Workspace Admin can attach an existing policy to a team as a [workspace-only policy](Teams.md#add-workspace-only-members-and-policies) in their workspace, with `workspaces:teams:manage-policies`.

## How ABAC works with RBAC

[RBAC](Role-based%20access%20control.md) permissions and ABAC policies are both considered when determining access to resources:

* ABAC **deny** policies override RBAC permissions.
* ABAC **allow** policies can grant access even without RBAC permissions.
* If no ABAC policies match, the system falls back to RBAC.

When a user belongs to [teams](Teams.md), LangSmith evaluates the permissions and policies from the user's role and every team together. A matching deny policy from any source still blocks access.

The access model depends on which features are enabled for the organization:

| RBAC enabled | ABAC enabled | Behavior |
| - | - | - |
| ✗ | ✗ | All workspace members have Admin-level access |
| ✓ | ✗ | Standard RBAC (access based on role permissions) |
| ✓ | ✓ | RBAC + ABAC (fine-grained, attribute-based access control) |

When both RBAC and ABAC are enabled, each request resolves as follows:

| RBAC permits | Allow policy matches | Deny policy matches | Result |
| - | - | - | - |
| ✓ | ✓ | ✗ | **Allowed** |
| ✓ | ✗ | ✗ | **Allowed** (RBAC fallback) |
| ✓ | ✓ | ✓ | **Denied** (deny wins) |
| ✓ | ✗ | ✓ | **Denied** (deny wins) |
| ✗ | ✓ | ✗ | **Allowed** (ABAC grants access) |
| ✗ | ✗ | ✗ | **Denied** |
| ✗ | ✓ | ✓ | **Denied** (deny wins) |

## Control access to run inputs and outputs

`runs:read` controls whether a user can see a run. `runs:read-inputs` and `runs:read-outputs` control whether the user can see the run's inputs and outputs. Message and trajectory views require both.

Policies for these permissions use `resource_type: "project"` and evaluate the tags of each run's parent project. Use them to hide inputs, outputs, or both in sensitive projects while leaving other projects in the workspace unchanged. RBAC and ABAC combine for these permissions the same way they do for any other permission, as described in [How ABAC works with RBAC](#how-abac-works-with-rbac). For an example, refer to [Hide run inputs and outputs in sensitive projects](#6-hide-run-inputs-and-outputs-in-sensitive-projects).

## Control trace access with root run metadata

A `root_run_metadata` condition limits which traces a user can read in a project, based on a key in each trace's root run metadata. Use it to hide some traces in a project, or to show users only the traces labeled for them, without moving traces into separate projects.

A `root_run_metadata` condition is valid only in a condition group with `permission: "runs:read"` and `resource_type: "project"`. It accepts the following fields:

* **`attribute_key`**: A top-level key in the root run metadata. Nested keys are not supported, so the key cannot contain `.`.
* **`operator`**: `equals` only. The match is case sensitive.
* **`attribute_value`**: The value to match, or the placeholder `${user.ls_user_id}`. The placeholder matches the `ls_user_id` of the user making the request. Retrieve this value from [`GET /auth/public`](../../../Monitor/Reference/LangSmith%20REST%20API/Administration/Get%20public%20auth%20info.md). Use the response's `ls_user_id` field, which is distinct from `user_id` or a user object's `id`.

Neither `attribute_key` nor `attribute_value` can contain a double quote or a backslash, and each is limited to 255 bytes. A value that starts with `${` must be exactly `${user.ls_user_id}`.

A condition group can combine `root_run_metadata` conditions with `resource_tag_key` conditions. The tag conditions select the projects the group applies to, and the metadata conditions select the traces in those projects. All conditions in a group must match.

Conditions evaluate only the root run, so all runs in a trace are visible or hidden together. Set the metadata key and value on the root run before ingestion. Root run metadata is immutable after ingestion, so you cannot add or change it later to make a trace match a policy. For how to add metadata, refer to [Add metadata and tags to traces](../../../Monitor/Trace/Configuration%20%26%20troubleshooting/Data%20%26%20privacy/Add%20metadata%20and%20tags%20to%20traces.md).

### Create a root run metadata policy in the UI

> [!NOTE]
>
> The **Root-run metadata** option requires the **Project** resource type and the `runs:read` permission. Root run metadata conditions must also be enabled for your organization. This option is not available in the self-hosted UI; on self-hosted installations, create root run metadata policies with the [API](#7-hide-traces-by-root-run-metadata) instead. On cloud, if the option is disabled after you select that resource type and permission, contact your LangChain representative.

The following example creates a deny policy that hides traces whose root run has `source` set to `customer`.

To create the policy:

1. Open the policy editor, as in steps 1 and 2 of [Create an access policy in the UI](#create-an-access-policy-in-the-ui). Enter `Hide Customer Traces` for **Name** and set **Effect** to **Deny**.
2. Click **Add rule**. Select **Project** for **Resource Type** and `runs:read` for **Permission**.
3. Click **Add condition** and change the source from **Resource tag** to **Root-run metadata**.
4. Enter `source` for **Metadata Key**. The operator is fixed to `equals`. Replace the prefilled `${user.ls_user_id}` in **Metadata Value** with `customer`.
5. Click **Save condition**, then **Add rule**.
6. Under **Roles**, add the workspace roles that should not see these traces. Click **Create policy**.

This produces the [Hide traces by root run metadata](#7-hide-traces-by-root-run-metadata) example policy. Add resource tag conditions to the same rule to limit it to specific projects.

To [show users only the traces labeled for them](#8-show-users-only-the-traces-labeled-for-them), use **Allow** instead. Set **Metadata Key** to `allowed_ls_user_id` and keep the prefilled `${user.ls_user_id}` for **Metadata Value**. Attach the policy to a role without `runs:read`. If the role has `runs:read`, its RBAC permission still grants access to other traces.

### How metadata conditions combine with RBAC

Metadata conditions follow the same precedence as other policies: deny policies apply first, then RBAC, then allow policies.

* **Deny policies**: A deny policy with metadata conditions hides the matching traces instead of blocking the whole project. The user keeps access to the other traces in the project. When several deny policies apply, a trace that matches any of them is hidden.
* **Allow policies**: An allow policy with metadata conditions grants `runs:read` on the matching traces only. When several allow policies apply, the user can read a trace that matches any of them.
* **RBAC**: If the user's role grants `runs:read`, the user can read every trace that a deny policy does not hide, and allow policies have no effect. To limit a role to the traces an allow policy matches, remove `runs:read` from the role.

Requests authenticated with a service key have no associated `ls_user_id`, so conditions using `${user.ls_user_id}` do not match. Requests authenticated with a personal access token (PAT) or a signed-in browser session have the user's `ls_user_id`. For details on PATs and service keys, refer to [API keys](../../Account/Create%20an%20account%20and%20API%20key.md#api-keys).

### Responses under metadata conditions

When metadata conditions apply to a user in a project, LangSmith filters that user's reads in the project to the traces they can see:

* Run lists, trace lists, and run analytics omit hidden traces.
* Requesting a hidden trace or one of its runs by ID returns `404 Not Found`. This includes downloading the trace and opening its messages or trajectory.
* The project list omits run and feedback statistics for the project.

## Example scenarios

### 1. Restrict annotators to their datasets

Allow annotators to only access datasets tagged for their annotation group:

```json
{
  "name": "Annotator Group A Access",
  "effect": "allow",
  "condition_groups": [{
    "permission": "datasets:read",
    "resource_type": "dataset",
    "conditions": [{
      "attribute_name": "resource_tag_key",
      "attribute_key": "Annotation-Group",
      "operator": "equals",
      "attribute_value": "Group-A"
    }]
  }]
}
```

### 2. Block sensitive data

Deny access to datasets containing PII. Since deny policies override allow policies, this blocks access even for users with RBAC permissions:

```json
{
  "name": "Block PII Datasets",
  "effect": "deny",
  "condition_groups": [{
    "permission": "datasets:read",
    "resource_type": "dataset",
    "conditions": [{
      "attribute_name": "resource_tag_key",
      "attribute_key": "Contains-PII",
      "operator": "equals",
      "attribute_value": "true"
    }]
  }]
}
```

### 3. Application-based access with wildcards

Allow engineers to access projects for any application in the "chatbot" family using glob patterns:

```json
{
  "name": "Chatbot Apps Access",
  "effect": "allow",
  "condition_groups": [{
    "permission": "projects:read",
    "resource_type": "project",
    "conditions": [{
      "attribute_name": "resource_tag_key",
      "attribute_key": "Application",
      "operator": "matches",
      "attribute_value": "chatbot-*"
    }]
  }]
}
```

### 4. Client and purpose isolation (AND logic)

Grant access only if both conditions are met - dataset is for training AND belongs to a specific client:

```json
{
  "name": "Client Training Data Access",
  "effect": "allow",
  "condition_groups": [{
    "permission": "datasets:read",
    "resource_type": "dataset",
    "conditions": [
      {
        "attribute_name": "resource_tag_key",
        "attribute_key": "Purpose",
        "operator": "equals",
        "attribute_value": "Training"
      },
      {
        "attribute_name": "resource_tag_key",
        "attribute_key": "Client",
        "operator": "equals",
        "attribute_value": "Acme-Corp"
      }
    ]
  }]
}
```

### 5. Client data plus resources without a `Client` tag using `_if_exists`

Consultants do not have RBAC `datasets:read` permission, but this policy grants them access to datasets tagged `Client=Acme-Corp`, as well as datasets that do not have a `Client` tag at all. Datasets tagged with a different client (e.g., `Client=Other-Corp`) remain blocked:

```json
{
  "name": "Acme Consultant Access",
  "effect": "allow",
  "condition_groups": [{
    "permission": "datasets:read",
    "resource_type": "dataset",
    "conditions": [{
      "attribute_name": "resource_tag_key",
      "attribute_key": "Client",
      "operator": "equals_if_exists",
      "attribute_value": "Acme-Corp"
    }]
  }]
}
```

### 6. Hide run inputs and outputs in sensitive projects

Let users keep browsing runs in projects that contain PII, but hide the runs' inputs and outputs. Each permission gets its own condition group, and the groups are evaluated with OR logic. Users still need `runs:read` to see the runs:

```json
{
  "name": "Hide PII Run Payloads",
  "effect": "deny",
  "condition_groups": [
    {
      "permission": "runs:read-inputs",
      "resource_type": "project",
      "conditions": [{
        "attribute_name": "resource_tag_key",
        "attribute_key": "Contains-PII",
        "operator": "equals",
        "attribute_value": "true"
      }]
    },
    {
      "permission": "runs:read-outputs",
      "resource_type": "project",
      "conditions": [{
        "attribute_name": "resource_tag_key",
        "attribute_key": "Contains-PII",
        "operator": "equals",
        "attribute_value": "true"
      }]
    }
  ]
}
```

### 7. Hide traces by root run metadata

Hide traces whose root run has `source` set to `customer`, in every project. Users whose role grants `runs:read` still see all other traces:

```json
{
  "name": "Hide Customer Traces",
  "effect": "deny",
  "condition_groups": [{
    "permission": "runs:read",
    "resource_type": "project",
    "conditions": [{
      "attribute_name": "root_run_metadata",
      "attribute_key": "source",
      "operator": "equals",
      "attribute_value": "customer"
    }]
  }]
}
```

### 8. Show users only the traces labeled for them

Show each user only the traces whose root run has `allowed_ls_user_id` set to that user's LangSmith user ID. Attach this policy to a role that does not grant `runs:read`, because RBAC permissions take precedence over allow policies:

```json
{
  "name": "Traces Labeled for the Caller",
  "effect": "allow",
  "condition_groups": [{
    "permission": "runs:read",
    "resource_type": "project",
    "conditions": [{
      "attribute_name": "root_run_metadata",
      "attribute_key": "allowed_ls_user_id",
      "operator": "equals",
      "attribute_value": "${user.ls_user_id}"
    }]
  }]
}
```

### 9. Team traces in production projects

Grant access to traces whose root run has `team` set to `payments`, only in projects tagged `Environment=prod`. The tag condition selects the projects, and the metadata condition selects the traces in them:

```json
{
  "name": "Payments Traces in Prod",
  "effect": "allow",
  "condition_groups": [{
    "permission": "runs:read",
    "resource_type": "project",
    "conditions": [
      {
        "attribute_name": "resource_tag_key",
        "attribute_key": "Environment",
        "operator": "equals",
        "attribute_value": "prod"
      },
      {
        "attribute_name": "root_run_metadata",
        "attribute_key": "team",
        "operator": "equals",
        "attribute_value": "payments"
      }
    ]
  }]
}
```

## Tag resources at creation time

When ABAC policies are active, resources are access-controlled based on their tags. To make sure a resource is protected as soon as it is created, you can supply tags directly in the creation request using the `tag_value_ids` parameter.

This is supported on project, dataset, and prompt creation endpoints (including fork and clone operations). Tags are applied atomically in the same database transaction as resource creation.

For full details and examples, see [Tag a resource at creation time](../Organization/Workspace%20setup/Set%20up%20resource%20tags.md#tag-a-resource-at-creation-time) in the resource tags guide.

> [!NOTE]
>
> If you rely on the LangSmith SDK to auto-create tracing projects during trace ingestion, the `tag_value_ids` parameter is not available on that auto-create path. To ensure ABAC policies apply from the start, pre-create the project via `POST /api/v1/sessions` with the desired `tag_value_ids` before starting your trace session.

## Troubleshooting

**Access unexpectedly denied?**

* Check if a deny policy is matching (deny always takes precedence)
* Check if the user has RBAC permissions or a matching allow policy
* Verify the resource has the expected tag and value
* Deny policies with `_if_exists` operators block resources missing that tag key
* For case-sensitive operators (`equals`, `not_equals`), check for case mismatches
* With multiple conditions in a group, all must match (AND logic)

**Access unexpectedly granted?**

* Review RBAC permissions (users may have access via their role)
* Check if an allow policy is too broad (e.g., using wildcards)
* `_if_exists` operators match resources missing that tag key

**Run inputs or outputs missing?**

* Check that the user's role grants `runs:read-inputs` and `runs:read-outputs`, or that an allow policy grants them for the run's project
* Check for a deny policy on `runs:read-inputs` or `runs:read-outputs` that matches the project's tags
* Message and trajectory views return `403 Forbidden` unless both permissions are granted

**Traces missing or returning `404 Not Found`?**

* Check for a deny policy with a `root_run_metadata` condition that matches the trace's root run metadata
* If the user's access comes from an allow policy with `root_run_metadata` conditions, check that the root run has the metadata key and the exact value, including case
* Conditions match top-level keys on the root run only, not metadata on child runs

**Threads, sharing, or experiment comparison returning `403 Forbidden`?**

* These surfaces are unavailable in any project where `root_run_metadata` conditions apply to the user. For the full list, refer to [Responses under metadata conditions](#responses-under-metadata-conditions)

**Policy not taking effect?**

* Confirm the policy is attached to the correct role
* Verify the user has that role in the workspace
* Check that `resource_type` and `permission` match the resource being accessed

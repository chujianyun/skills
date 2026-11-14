# Access & oversight

> Control who can access agents, how they authenticate, and audit everything they do.

Fleet gives you the control layer for scaling agents across your organization: tiered permissions, credential management, human-in-the-loop oversight, and an audit trail for agent actions.

## Permissions and sharing

Fleet combines workspace role permissions with agent sharing. Your role determines which actions you can perform. Agent ownership and sharing determine which agents you can access.

> [!NOTE]
>
> Custom roles are an Enterprise feature. The permissions below apply when Fleet RBAC is enabled for your workspace. For self-hosted v0.17, Fleet RBAC requires LangSmith 0.17.44 or a later v0.17 patch and the [deployment flag](#enable-fleet-rbac-on-self-hosted).

### Configure a Fleet role

To let users use and manage Fleet, create a [custom workspace role](../../../LangSmith%20setup/Govern/Users%20%26%20access%20control/Role-based%20access%20control.md#custom-roles) with these permissions:

| Area | Permissions | Needed for |
| - | - | - |
| Workspace | `workspaces:read` | Access the workspace. |
| Agents | `fleet-agents:read` `fleet-agents:invoke` `fleet-agents:create` `fleet-agents:update` `fleet-agents:delete` | View, run, create, edit, clone, and delete agents. Manage agent connections. |
| Skills | `fleet-skills:read` `fleet-skills:create` `fleet-skills:update` `fleet-skills:delete` | Browse, create, edit, and delete workspace skills. |
| MCP servers | `mcp-servers:read` `mcp-servers:invoke` `mcp-servers:create` `mcp-servers:update` `mcp-servers:delete` | Use tools and install, update, or remove workspace integrations. |
| Deployments | `deployments:read` `deployments:create` `deployments:update` `deployments:delete` | Configure OAuth providers and manage connected accounts through the current Fleet UI. |

Grant each permission explicitly. Create, update, delete, and invoke permissions do not include read permission. Existing agent and skill ownership and sharing checks still apply.

The `deployments:*` permissions also grant access to deployment resources outside Fleet.

### Optional administration permissions

* **View Fleet usage and limits**: Add `fleet:read-admin-config` to view usage reports and usage limits.
* **Manage Fleet limits**: Add `fleet:write-admin-config` to create, update, and delete usage limits. Grant both Fleet admin permissions to view and manage limits.
* **Manage workspace settings**: Add `workspaces:manage` for workspace settings, integration access controls, and OAuth provider management in **Settings**.

For more information, see [Workspace administration](../Configure/Manage%20workspace%20administration.md).

### Share agents

Fleet provides granular control over every agent in two dimensions: **who gets access** and **what they can do**.

* **Who**: Share with individual users or your entire workspace.
* **What**: Three permission levels:
  * **Clone**: copy and customize the agent
  * **Run**: use without modifying
  * **Edit**: full access to change instructions, tools, and settings

You can layer these permissions. Give a core team edit access, share run-only with the broader organization, and revoke at any time.

For setup instructions, see [Change access to the agent](../Configure/Manage%20agent%20settings.md#change-access-to-the-agent).

### Enable Fleet RBAC on self-hosted

Fully self-hosted LangSmith installations enable Fleet role-based access control (RBAC) with a deployment flag. Cloud and hybrid (BYOC) deployments do not need this step.

> [!NOTE]
>
> Fleet RBAC on self-hosted requires LangSmith 0.17.44 or a later v0.17 patch.

To enable Fleet RBAC:

1. Upgrade all services to the required LangSmith version.
2. Create or update [custom roles](#configure-a-fleet-role) with Fleet permissions, and assign them to users. The upgrade does not add Fleet permissions to existing roles.
3. Add the flag to your Helm values, preserving existing `extraEnv` entries:

   ```yaml
   platformBackend:
     deployment:
       extraEnv:
         - name: FLEET_RBAC_PERMISSIONS_ENABLED
           value: "true"
   ```

   The flag defaults to `false`. Setting it to `true` enables Fleet RBAC across all workspaces in the deployment.
4. Apply the values through your normal Helm upgrade process.
5. Call `GET /v1/fleet/config` with your API key and workspace ID. Confirm that the response contains `"rbac_permissions_enabled": true`.

## Agent identity and credentials

Fleet offers two credential models that control how agents authenticate with external tools:

* **Fixed credentials ("Claws")**: The agent uses a single set of credentials regardless of who runs it. Use for shared-resource agents like a team Slack bot where everyone interacts through the same account.
* **User credentials ("Assistants")**: The agent acts on behalf of the individual user who invokes it. Each user authenticates with their own account via OAuth. Use for tools where users have different access levels, like a personal email assistant.

This is configurable per agent, so you can choose the right model for each use case.

For setup instructions, see [Agent identity](../Configure/Agent%20identity.md).

## Tool access control

Fleet provides layered access control for tools, covering both **custom MCP servers** (user-added, workspace-scoped) and **built-in integrations** (platform-provided, such as Gmail, Slack, and GitHub):

* **[Role-based access control (RBAC)](#role-based-permissions)**: Controls access at the role level.
* **[Attribute-based access control (ABAC)](#attribute-based-access-control)**: Adds per-resource granularity on top of RBAC.
* **[Workspace integration policy](#workspace-integration-policy)**: Provides an admin-controlled enable/disable gate for built-in integrations.

> [!NOTE]
>
> Tool access control is an Enterprise feature. If you are interested in this feature, [contact our sales team](https://www.langchain.com/contact-sales).

### Role-based permissions

Role-based access control (RBAC) grants or denies access to all MCP servers and integrations in a workspace based on a user's role. Configure roles in **Settings > Roles**.

The following permissions are available for MCP servers and integrations:

| Permission | Description |
| - | - |
| `mcp-servers:read` | Discover and list MCP servers and integrations |
| `mcp-servers:invoke` | Execute tools from MCP servers and integrations |
| `mcp-servers:create` | Create new MCP server configurations |
| `mcp-servers:update` | Modify MCP server configurations |
| `mcp-servers:delete` | Remove MCP server configurations |

> [!NOTE]
>
> A role with `mcp-servers:read` and `mcp-servers:invoke` can see and use all MCP servers and integrations in the workspace.

For more on RBAC, see [Role-based access control](../../../LangSmith%20setup/Govern/Users%20%26%20access%20control/Role-based%20access%20control.md).

#### Create a role with tool permissions

**1. Open role settings**

Navigate to **Settings > Roles** and click **Create role**.

**2. Configure MCP Servers permissions**

Expand the **MCP Servers** section and select the permissions to include. For example, grant `Read` and `Invoke` for users who need to use tools but not manage server configurations.

**3. Assign the role**

Assign the role to users in the workspace in **Settings > Members**.

### Attribute-based access control

Attribute-based access control (ABAC) adds resource-level granularity on top of RBAC. Admins can tag individual MCP servers or integrations and create policies that grant or restrict access based on those tags.

ABAC operates on two resource types for tools:

| Resource type | Applies to |
| - | - |
| `mcp_server` | Custom MCP servers added to the workspace |
| `fleet_integration` | Built-in integrations (Gmail, Slack, GitHub, etc.) |

> [!NOTE]
>
> A role with no `mcp-servers:*` RBAC permissions can still be granted access to specific tagged resources (e.g. only Notion and Gmail) via an ABAC allow policy. Conversely, a role with broad RBAC access can be restricted from specific resources via an ABAC deny policy.

For details on policy structure, operators, and managing policies via the API, see [Attribute-based access control](../../../LangSmith%20setup/Govern/Users%20%26%20access%20control/Attribute-based%20access%20control.md).

### Workspace integration policy

Built-in integrations have an additional control layer: a workspace-level enable/disable toggle managed from **Settings > Integrations > Access control**. This acts as an admin-controlled baseline that runs before per-user RBAC and ABAC.

If an integration is disabled at the workspace level, no user can access it regardless of their role or ABAC policies.

> [!NOTE]
>
> The Access control page is only visible to admin users (requires `workspaces:manage` permission).

### Policy evaluation order

The three layers evaluate in sequence. The evaluation order differs slightly between custom MCP servers and built-in integrations:

**Custom MCP servers:**

```
ABAC deny → RBAC → ABAC allow
```

**Built-in integrations:**

```
Workspace policy gate → ABAC deny → RBAC → ABAC allow
```

At each step:

1. **Workspace policy gate** (integrations only): If the integration is disabled, access is denied. No further evaluation.
2. **ABAC deny**: If a deny policy matches, access is denied. Deny always wins.
3. **RBAC**: If the user's role grants the required permission, access is allowed (unless step 4 is needed).
4. **ABAC allow**: If RBAC does not grant access, an allow policy can still grant it for specific tagged resources.

## Observability and audit trail

Agent actions in Fleet are captured in a structured [LangSmith trace](../../../Monitor/Overview/LangSmith%20Observability.md), including tool calls, decisions, and outputs. You can inspect, search, and export traces.

Combined with agent identity and permissions, tracing tells you which agent acted, on whose behalf, with what credentials, and what it did at each step.

## Human-in-the-loop oversight

Fleet provides a [central inbox](https://smith.langchain.com/agents/inbox) for reviewing agent actions across all your agents. You can configure agents to pause and request approval before taking specific actions, then review, approve, edit, or reject from one place.

For setup instructions, see [Human-in-the-loop](../Get%20started/Essentials.md#human-in-the-loop).

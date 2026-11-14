# Manage user access in SSO organizations

LangSmith provides flexible controls for managing how users join your [organization](../Organization/Overview.md#organizations) when using [Single Sign-On (SSO) authentication](Authentication%20methods.md). You can independently enable or disable both Just-In-Time (JIT) provisioning and user invites to match your organization's security and onboarding requirements.

When SSO is enabled, you have two independent settings: [JIT provisioning](#jit-provisioning) automatically adds users when they sign in via SSO, while [invites](#invites) allow administrators to invite users manually before they can access the organization. [Configure these settings](#configuration-scenarios) in any combination to control your user onboarding workflow.

This page explains how the settings work and how to configure them.

## Settings

You can control the following two settings independently to manage how users join your organization.

### JIT provisioning

The `jit_provisioning_enabled` setting controls automatic user provisioning. When enabled, users who authenticate via your SSO provider are automatically added to your [organization](../Organization/Overview.md#organizations) and assigned to default [workspaces](../Organization/Overview.md#workspaces) with a default [role](Role-based%20access%20control.md). For more details, refer to [Configure default SSO settings](#configure-default-sso-settings). When disabled, users must be explicitly invited or added via [SCIM](#scim-integration) before they can access the organization.

### Invites

The `invites_enabled` setting controls manual user invitations. When enabled, [organization administrators](../Organization/Overview.md#organization-roles) can send invitations to users before they sign in. Invited users can claim their invite when signing in via SSO. When disabled, manual invitations are not allowed and users can only join via JIT provisioning or [SCIM](#scim-integration).

### Update settings

You can update these settings in the LangSmith UI or with the LangSmith API:

> [tab] UI
>
> In the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-jit-invite-sso):
>
> 1. Navigate to **Settings** > **Organization** > **Access and Security** > **General**.
> 2. Toggle **Enable JIT provisioning** and **Allow invites** as needed.
> 3. [Configure SSO default workspaces and roles](#configure-default-sso-settings) in **Settings** > **SSO configuration**.

> [tab] API
>
> Update organization settings programmatically using the [Update organization info](../../../Monitor/Reference/LangSmith%20REST%20API/Administration/Update%20current%20organization%20info.md) endpoint:
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl -X PATCH https://api.smith.langchain.com/api/v1/organizations/current/info \
>   -H "Authorization: Bearer $LANGSMITH_API_KEY" \
>   -H "Content-Type: application/json" \
>   -d '{
>     "jit_provisioning_enabled": true,
>     "invites_enabled": true
>   }'
> ```
>
> Response includes updated current organization configuration:
>
> ```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> {
>   "id": "org-uuid",
>   "display_name": "My Organization",
>   "jit_provisioning_enabled": true,
>   "invites_enabled": true,
>   "sso_login_slug": "my-org",
>   ...
> }
> ```

> [!NOTE]
>
> Consider the following if you are using [LangSmith self-hosted](../../Self-hosted/Self-hosted%20LangSmith.md):
>
> * The JIT provisioning and the invites settings only apply to the default organization (identified by `default_sso_provision=true`). Other organizations must use invites in self-hosted.
> * The environment variable `SELF_HOSTED_JIT_PROVISIONING_ENABLED` can globally override the JIT provisioning setting. When set to `false`, JIT provisioning is disabled for all organizations regardless of their individual settings.
> * For additional self-hosted user management customizations, refer to [Customize user management](../../Self-hosted/Platform%20auth%20%26%20access%20control/Customize%20user%20management.md).

## How user access works

When a user attempts to sign in via SSO, LangSmith follows this decision flow:

1. User authenticates with SSO provider.
2. LangSmith checks if user already has organization access:
   ```
   ├─ YES → User is signed in
   └─ NO → Continue to step 3
   ```
3. Check if invites are enabled **and** a pending invite exists:
   ```
   ├─ YES → Provision into organization with invite's organization role; provision into workspaces if invite included workspaces
   └─ NO → Continue to step 4
   ```
4. Check if JIT provisioning is enabled:
   ```
   ├─ YES → Automatically provision user with default SSO workspaces/role
   └─ NO → Deny access (user must be added via SCIM or by administrator)
   ```

> [!NOTE]
>
> When both JIT provisioning and invites are enabled, **invites take precedence**. If a user has a pending invitation, they are added with the invite's contents, not the default SSO settings.

## Configuration scenarios

### Open access (both enabled)

**Configuration:**

* ✓ JIT Provisioning enabled
* ✓ Invites enabled

**Behavior:**

* Users can sign in immediately via SSO and are auto-provisioned.
* Admins can send invites to assign specific roles or workspaces.
* Invited users get the invite configuration; non-invited users get default SSO configuration.

**Example:**

```
User alex@company.com signs in via SSO:
  - No invite exists → Added to default workspaces with Viewer role

User billy@company.com signs in via SSO:
  - Invite exists for Editor role in "Production" workspace → Added only to "Production" workspace with Editor role (invite takes precedence)
```

### JIT only (invites disabled)

**Configuration:**

* ✓ JIT Provisioning enabled
* ✗ Invites disabled

**Behavior:**

* All users who authenticate via SSO are automatically provisioned.
* Admins cannot send invitations.
* All new users receive the same default workspaces and role.

### Invite only (JIT disabled)

**Configuration:**

* ✗ JIT Provisioning disabled
* ✓ Invites enabled

**Behavior:**

* Users must be invited before they can access the organization.
* Users without invites are denied access even with valid SSO credentials.
* Fine-grained control over who can access the organization.

**Example:**

```
User alex@company.com signs in via SSO:
  - Has pending invite → Successfully joins organization

User billy@company.com signs in via SSO:
  - No invite → Access denied (must request invite from administrator)
```

### Closed access (both disabled)

**Configuration:**

* ✗ JIT Provisioning disabled
* ✗ Invites disabled

**Behavior:**

* SSO users cannot join the organization automatically.
* Invitations cannot be sent.
* Users must be provisioned through SCIM or directly by an administrator once they are already part of the organization via SCIM.

## User access quick reference

| JIT enabled | Invites enabled | Pending invite | Result |
| - | - | - | - |
| ✓ | ✓ | Yes | Invite claimed (invite configuration used) |
| ✓ | ✓ | No | Auto-provisioned (default SSO configuration) |
| ✓ | ✗ | N/A | Auto-provisioned (default SSO configuration) |
| ✗ | ✓ | Yes | Invite claimed |
| ✗ | ✓ | No | **Access denied** - must be invited |
| ✗ | ✗ | N/A | **Access denied** - must use [SCIM](#scim-integration) or admin |

## Configure default SSO settings

When [JIT provisioning](#jit-provisioning) is enabled, configure default settings for new users:

1. Default workspace role. Choose the [workspace role](Role-based%20access%20control.md#workspace-roles) that users receive when automatically provisioned. For details on what each role can do, refer to [Organization and workspace operations](Organization%20and%20workspace%20operations%20reference.md). Options include:

   * **[Viewer](Role-based%20access%20control.md#workspace-viewer)**: Read-only access
   * **[User](Role-based%20access%20control.md#organization-user)**: Standard access
   * **[Editor](Role-based%20access%20control.md#workspace-editor)**: Can modify resources
   * **[Admin](Role-based%20access%20control.md#workspace-admin)**: Full workspace control

2. Default workspaces. Select one or more workspaces that users are automatically added to. Users receive the same role in all selected workspaces. To configure:

   1. Go to **Settings** > **SSO configuration**.
   2. Set **Default workspace role**.
   3. Select **Default workspaces**.
   4. Save your configuration.

## SCIM integration

If your organization uses [SCIM](User%20management.md#set-up-scim-for-your-organization) (System for Cross-domain Identity Management), users can be automatically provisioned and managed through your identity provider. SCIM provides an additional mechanism for user management that works alongside JIT and invite settings.

> [!NOTE]
>
> SCIM group membership overrides manually assigned roles or roles assigned via JIT provisioning. If you're using SCIM, consider disabling JIT provisioning to avoid conflicts.

## SSO Groups Sync

[SSO Groups Sync](User%20management.md#sso-groups-sync-alternative) is an alternative to SCIM that reads group memberships from the SSO token at login time and assigns org and workspace roles using the SCIM naming convention. The sync runs after JIT and invite resolution on each login, and owns only the memberships it created.

**Precedence with JIT, invites, and SCIM:**

* **SCIM-sourced** memberships are never modified by SSO Groups Sync.
* **SSO Groups Sync–sourced** memberships are fully replaced on each login based on the token's group membership.
* **Manual and JIT-provisioned** memberships are not modified by SSO Groups Sync.

We recommend choosing one of SCIM or SSO Groups Sync per organization, not both, to avoid confusing precedence behavior. For configuration and tradeoffs, refer to [SSO Groups Sync](User%20management.md#sso-groups-sync-alternative).

## Related documentation

* [Set up SSO with OAuth2.0 and OIDC](../../Self-hosted/Platform%20auth%20%26%20access%20control/Set%20up%20SSO%20with%20OAuth2.0%20and%20OIDC.md) (Self-hosted)
* [Set up SAML SSO](User%20management.md#set-up-saml-sso-for-your-organization) (Cloud)
* [Set up SCIM](User%20management.md#set-up-scim-for-your-organization)
* [User management](User%20management.md)
* [Role-based access control](Role-based%20access%20control.md)

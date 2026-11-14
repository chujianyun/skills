# Set up SSO with OAuth2.0 and OIDC

LangSmith [Self-Hosted](../Self-hosted%20LangSmith.md) provides SSO via OAuth2.0 and OIDC, which delegates authentication to your Identity Provider (IdP) to manage access to LangSmith.

The LangSmith implementation supports any provider that is OIDC compliant. Once configured, you will see a login screen that prompts to **Log in via SSO**.

By default, LangSmith Self-Hosted supports the `Authorization Code` flow with `Client Secret`. In this version of the flow, your client secret is stored securely in LangSmith (not on the frontend) and used for authentication and establishing auth sessions.

## Considerations

* You may upgrade a [`basic` auth](Basic%20authentication%20with%20email%20and%20password.md) installation to `oauth` mode, but not a [`none` auth](../../Govern/Users%20%26%20access%20control/Authentication%20methods.md#none) installation.
  * Upgrade a `basic` auth installation by removing the [`basic` auth configuration parameters](Basic%20authentication%20with%20email%20and%20password.md#configuration) and adding the [OAuth with client secret configuration parameters](#configuration). Users may then log in via OAuth **only**. To maintain access post-upgrade, **you must have access to log in via OAuth using an email address that previously logged in via basic auth.**
* LangSmith does **not** support:
  * Moving from SSO to `basic` auth mode in self-hosted.
  * Moving from OAuth with client secret to OAuth with PKCE. To move from PKCE to client secret, see [Migrate from PKCE to client secret](#migrate-from-pkce-to-client-secret).
  * Having both `basic` auth and OAuth at the same time. Ensure you disable the `basic` auth configuration when enabling OAuth.

## Prerequisites

You must have the following to complete the [Provider setup](#provider-setup):

* [Self-hosted](../Self-hosted%20LangSmith.md) and on an [Enterprise plan](https://docs.langchain.com/langsmith/pricing-plans.md).
* An IdP that supports the `Authorization Code` flow with `Client Secret`.
* An IdP that supports using an external discovery/issuer URL. LangSmith uses this to fetch the necessary routes and keys for your IdP.
* The `OIDC`, `email`, and `profile` scopes. LangSmith uses these to fetch the necessary user information and email for your users.

> [!NOTE]
>
> LangSmith SSO is only supported over `https`.

## Configuration

* You will need to set the callback URL in your IdP to `https://<host>/api/v1/oauth/custom-oidc/callback`, where `host` is the domain or IP you have provisioned for your LangSmith instance. This is where your IdP will redirect the user after they have authenticated.
* To terminate the IdP session on logout (so users must re-authenticate), register your LangSmith URL (e.g., `https://<host>`) as a **post-logout redirect URI** (sometimes called "Sign-out redirect URI") in your IdP, then set `OAUTH_IDP_LOGOUT_ENABLED=true` in your environment via `commonEnv` in Helm.
* You will need to provide the `oauthClientId`, `oauthClientSecret`, `hostname`, and `oauthIssuerUrl` in your `values.yaml` file. This is where you will configure your LangSmith instance.
* If you have **not** already configured OAuth with client secret or if you only have personal orgs, you must provide an email address to assign as the `initialOrgAdminEmail` for the newly provisioned SSO org. If you are upgrading from [basic auth](Basic%20authentication%20with%20email%20and%20password.md), LangSmith will reuse your existing org instead.

```yaml Helm
config:
  authType: mixed
  hostname: https://langsmith.example.com
  initialOrgAdminEmail: test@email.com # Set this if required
  oauth:
    enabled: true
    oauthClientId: <YOUR CLIENT ID>
    oauthClientSecret: <YOUR CLIENT SECRET>
    oauthIssuerUrl: <YOUR DISCOVERY URL>
    oauthScopes: "email,profile,openid"
```

## Provider setup

### Microsoft Entra ID IdP setup

Configure Microsoft Entra ID as a single sign-on provider using OAuth2.0 and OIDC. For additional information, refer to Microsoft's [OpenID Connect documentation](https://learn.microsoft.com/en-us/entra/identity-platform/v2-protocols-oidc).

> [!NOTE]
>
> Registering the application in Microsoft Entra ID requires the `Application Administrator` or `Cloud Application Administrator` role, or higher, in your tenant.

#### Step 1. Register the application

1. In the [Microsoft Entra admin center](https://entra.microsoft.com/), go to **Applications** > **App registrations** > **New registration**.
2. Set **Name** to a value that identifies the application, for example, `LangSmith Self-Hosted`.
3. Set **Supported account types** to **Accounts in this organizational directory only (Single tenant)**.
4. Under **Redirect URI**, select **Web** as the platform and enter `https://<host>/api/v1/oauth/custom-oidc/callback`, where `<host>` is the domain of your LangSmith instance.
5. Click **Register**.

From the app's **Overview** page, record the following values for use in Helm configuration:

* **Application (client) ID**: used as `oauthClientId`.
* **Directory (tenant) ID**: used to construct the issuer URL.
* **OIDC issuer URL**: `https://login.microsoftonline.com/<tenant-id>/v2.0`, used as `oauthIssuerUrl`.

> [!WARNING]
>
> Include the `/v2.0` suffix in `oauthIssuerUrl`. Without it, login still works, but [SSO Groups Sync](#sso-groups-sync) does not assign roles.

#### Step 2. Create a client secret

1. In the app registration, go to **Certificates & secrets** > **Client secrets** > **New client secret**.
2. Enter a description, choose an expiration, then click **Add**.
3. Copy the secret **Value** immediately. Microsoft Entra ID hides this value after you leave the page. Use it as `oauthClientSecret`.

Store the Client ID, Client Secret, and Issuer URL in your secret store before configuring Helm.

#### Step 3. Add the email optional claim

Without this step, LangSmith blocks login with the error `Your identity provider did not provide an email address`.

1. In the app registration, go to **Token configuration** > **Add optional claim**.
2. Select **ID** as the token type.
3. Check `email`, then click **Add**.
4. When prompted, accept the request to grant the Microsoft Graph `email` permission.

#### Step 4. Configure LangSmith

Apply the values from the previous steps to your Helm configuration:

```yaml Helm
config:
  authType: mixed
  hostname: https://langsmith.example.com
  initialOrgAdminEmail: test@email.com # Set this if required
  oauth:
    enabled: true
    oauthClientId: "<APPLICATION (CLIENT) ID>"
    oauthClientSecret: "<SECRET>"
    oauthIssuerUrl: "https://login.microsoftonline.com/<TENANT ID>/v2.0"
    oauthScopes: "email,profile,openid"
```

For details about `initialOrgAdminEmail`, refer to the [general configuration section](#configuration).

> [!NOTE]
>
> Microsoft Entra ID's `oid` claim is used as the OIDC `sub` claim by default. For details, refer to [Override sub claim](#override-sub-claim).

To assign org and workspace roles from Microsoft Entra ID groups on login, refer to [SSO Groups Sync](#sso-groups-sync).

### Google workspace IdP setup

You can use Google Workspace as a single sign-on (SSO) provider using [OAuth2.0 and OIDC](https://developers.google.com/identity/openid-connect/openid-connect) without PKCE.

> [!NOTE]
>
> You must have administrator-level access to your organization's Google Cloud Platform (GCP) account to create a new project, or permissions to create and configure OAuth 2.0 credentials for an existing project. We recommend that you create a new project for managing access, since each GCP project has a single OAuth consent screen.

1. Create a new GCP project, see the Google documentation topic [creating and managing projects](https://cloud.google.com/resource-manager/docs/creating-managing-projects)

2. After you have created the project, open the [Credentials](https://console.developers.google.com/apis/credentials) page in the Google API Console (making sure the project in the top left corner is correct)

3. Create new credentials: `Create Credentials > OAuth client ID`

4. Choose `Web application` as the `Application type` and enter a name for the application e.g. `LangSmith`

5. In `Authorized Javascript origins` put the domain of your LangSmith instance e.g. `https://langsmith.yourdomain.com`

6. In `Authorized redirect URIs` put the domain of your LangSmith instance followed by `/api/v1/oauth/custom-oidc/callback` e.g. `https://langsmith.yourdomain.com/api/v1/oauth/custom-oidc/callback`

7. Click `Create`, then download the JSON or copy and save the `Client ID` (ends with `.apps.googleusercontent.com`) and `Client secret` somewhere secure. **You will be able to access these later if needed**.

8. Select `OAuth consent screen` from the navigation menu on the left

   1. Choose the Application type as `Internal`. **If you select `Public`, anyone with a Google account can sign in.**
   2. Enter a descriptive `Application name`. This name is shown to users on the consent screen when they sign in. For example, use `LangSmith` or `<organization_name> SSO for LangSmith`.
   3. Verify that the Scopes for Google APIs only lists email, profile, and openid scopes. Only these scopes are required for single sign-on. If you grant additional scopes it increases the risk of exposing sensitive data.

9. (Optional) control who within your organization has access to LangSmith: [https://admin.google.com/ac/owl/list?tab=configuredApps](https://admin.google.com/ac/owl/list?tab=configuredApps). See [Google's documentation](https://support.google.com/a/answer/7281227?hl=en&fl=1&sjid=9554153972856467090-NA) for additional details.

10. Configure LangSmith to use this OAuth application. For examples, here are the `config`values that would be used for Kubernetes configuration:

    1. `oauthClientId`: `Client ID` (ends with `.apps.googleusercontent.com`)
    2. `oauthClientSecret`: `Client secret`
    3. `hostname`: the domain of your LangSmith instance e.g. `https://langsmith.yourdomain.com` (no trailing slash)
    4. `oauthIssuerUrl`: `https://accounts.google.com`
    5. `oauth.enabled`: `true`
    6. `authType`: `mixed`

### Okta IdP setup

#### Supported features

* IdP-initiated SSO
* SP-initiated SSO
* Just-In-Time provisioning (see [Manage user access in SSO organizations](../../Govern/Users%20%26%20access%20control/Manage%20user%20access%20in%20SSO%20organizations.md))

#### Configuration steps

For additional information, see Okta's [documentation](https://help.okta.com/en-us/content/topics/apps/apps_app_integration_wizard_oidc.htm).
If you have any questions or issues, please contact support via [support.langchain.com](https://support.langchain.com).

**Via Okta Integration Network (recommended)**

> [!NOTE]
>
> For details on SCIM setup, refer to [Set up SCIM for your organization](../../Govern/Users%20%26%20access%20control/User%20management.md#set-up-scim-for-your-organization).

> [!NOTE]
>
> This method of configuration is required in order to use SCIM with Okta.

1. Sign in to [Okta](https://login.okta.com/).
2. In the upper-right corner, select Admin. The button is not visible from the Admin area.
3. Select `Browse App Integration Catalog`.
4. Find and select the LangSmith application.
5. On the application overview page, select Add Integration.
6. Fill in `ApiUrlBase`:
   * Your LangSmith API URL **without the protocol** (`https://`) formatted as `<langsmith_domain>/api/v1`, e.g., `langsmith.yourdomain.com/api/v1`.
   * If your installation is configured with a subdomain / path prefix, include that in the URL, e.g., `langsmith.yourdomain.com/prefix/api/v1`.
7. Leave `AuthHost` empty.
8. (Optional, if planning to use [SCIM](../../Govern/Users%20%26%20access%20control/User%20management.md#set-up-scim-for-your-organization) as well) Fill in `LangSmithUrl`: The `<langsmith_url>` portion from above, e.g., `langsmith.yourdomain.com`.
9. Under Application Visibility, keep the box unchecked.
10. Select Next.
11. Select `OpenID Connect`.
12. Fill in `Sign-On Options`:
    * `Application username format`: `Email`.
    * `Update application username on`: `Create and update`.
    * `Allow users to securely see their password`: leave **unchecked**.
13. Click **Save**.
14. Configure LangSmith to use this OAuth application (see [general configuration section](#configuration) for details about `initialOrgAdminEmail`):

```yaml Helm
config:
  authType: mixed
  hostname: https://langsmith.example.com # the domain of your instance (note no trailing slash)
  initialOrgAdminEmail: test@email.com # Set this if required
  oauth:
    enabled: true
    oauthClientId: "Client ID" # (starts with `0o`)
    oauthClientSecret: "<SECRET>"
    oauthIssuerUrl: "https://company-7422949.okta.com" # the URL of your Okta instance
    oauthScopes: "email,profile,openid"
```

> [!NOTE]
>
> For details on SCIM setup, refer to [Set up SCIM for your organization](../../Govern/Users%20%26%20access%20control/User%20management.md#set-up-scim-for-your-organization).

**Via Custom App Integration**

> [!WARNING]
>
> SCIM is not compatible with this method of configuration. Refer to [**Via Okta Integration Network**](#via-okta-integration-network).

1. Log in to Okta as an administrator, and go to the **Okta Admin console**.
2. Under **Applications** > **Applications** click **Create App Integration**.
3. Select **OIDC - OpenID Connect** as the Sign-in method and **Web Application** as the Application type, then click **Next**.
4. Enter an `App integration name` (e.g., `LangSmith`).
5. Recommended: Check **Core grants > Refresh Token** (see [session length controls](#session-length-controls)).
6. In **Sign-in redirect URIs** put the domain of your LangSmith instance followed by `/api/v1/oauth/custom-oidc/callback`, e.g., `https://langsmith.yourdomain.com/api/v1/oauth/custom-oidc/callback`. If your installation is configured with a subdomain / path prefix, include that in the URL, e.g., `https://langsmith.yourdomain.com/prefix/api/v1/oauth/custom-oidc/callback`.
7. Under **Sign-out redirect URIs**, set the value to your LangSmith URL, e.g., `https://langsmith.yourdomain.com`. This ensures the IdP session is terminated when users log out of LangSmith.
8. Under **Trusted Origins > Base URIs** add your langsmith URL with the protocol, e.g., `https://langsmith.yourdomain.com`.
9. Select your desired option under **Assignments > Controlled access**:
   * Allow everyone in your organization to access.
   * Limit access to selected groups.
   * Skip group assignment for now.
10. Click **Save**.
11. Under **Sign On > OpenID Connect ID Token** set **Issuer** to **Okta URL**.
12. (Optional) Under **General > Login** set **Login initiated by** to `Either Okta or App` to enable IdP-initiated login.
13. (Recommended) Under **General > Login > Email verification experience** fill in the **Callback URI** with the LangSmith URL, e.g., `https://langsmith.yourdomain.com`.
14. Configure LangSmith to use this OAuth application (see [general configuration section](#configuration) for details about `initialOrgAdminEmail`):

```yaml Helm
config:
  authType: mixed
  hostname: https://langsmith.example.com # the domain of your instance (note no trailing slash)
  initialOrgAdminEmail: test@email.com # Set this if required
  oauth:
    enabled: true
    oauthClientId: "Client ID" # (starts with `0o`)
    oauthClientSecret: "<SECRET>"
    oauthIssuerUrl: "https://company-7422949.okta.com" # the URL of your Okta instance
    oauthScopes: "email,profile,openid"
```

#### SP-initiated SSO

Users can sign in using the **Login via SSO** button on the LangSmith homepage.

## Advanced options

### Session length controls

> [!NOTE]
>
> All of the environment variables in this section are for the `platform-backend` service and can be added using `platformBackend.deployment.extraEnv` in Helm.

* By default, session length is controlled by the expiration of the identity token returned by the identity provider
* Most setups should use refresh tokens to enable session length extension beyond the identity token expiration up to `OAUTH_SESSION_MAX_SEC`, which may require including the `offline_access` scope by adding to `oauthScopes` in Helm
* `OAUTH_SESSION_MAX_SEC` (default 1 day) can be overridden to a maximum of one week (`604800`)
* For identity provider setups that don't support refresh tokens, setting `OAUTH_OVERRIDE_TOKEN_EXPIRY="true"` will take `OAUTH_SESSION_MAX_SEC` as the session length, ignoring the identity token expiration

### Scope encoding for strict identity providers

By default, LangSmith encodes the spaces between `oauthScopes` in the authorization request as `+` (the `application/x-www-form-urlencoded` convention). Most identity providers accept this, but some (for example, CA SiteMinder) do not decode `+` as a space and reject the login with an `invalid_scope` error. If your IdP rejects multi-scope logins for this reason, set `urlEncodeScopeSpaces: true` in Helm to encode the spaces as `%20` instead, which is the encoding accepted by all OIDC-compliant providers. This applies only to `authType: mixed` with an OAuth client secret, and defaults to off.

```yaml Helm
config:
  authType: mixed
  hostname: https://langsmith.example.com
  oauth:
    enabled: true
    oauthClientId: <YOUR CLIENT ID>
    oauthClientSecret: <YOUR CLIENT SECRET>
    oauthIssuerUrl: <YOUR DISCOVERY URL>
    oauthScopes: "email,profile,openid"
    urlEncodeScopeSpaces: true
```

### Override sub claim

In some scenarios, it may be necessary to override which claim is used as the `sub` claim from your identity provider.
For example, in SCIM, the resolved `sub` claim and SCIM `externalId` must match in order for login to succeed.
If there are restrictions on the source attribute of the `sub` claim and/or the SCIM `externalId`, set the `ISSUER_SUB_CLAIM_OVERRIDES` environment variable to select which OIDC JWT claim is used as the `sub`.

If an issuer URL **starts with** one of the URLs in this configuration, the `sub` claim is taken from the field name specified.
For example, with the following configuration, a token with the issuer `https://idp.yourdomain.com/application/uuid` would use the `customClaim` value as the `sub`:

```
ISSUER_SUB_CLAIM_OVERRIDES='{"https://idp.yourdomain.com": "customClaim"}'
```

If unset, the default value for this configuration uses the `oid` claim when Azure Entra ID is used as the identity provider:

```
ISSUER_SUB_CLAIM_OVERRIDES='{"https://login.microsoftonline.com/": "oid", "https://sts.windows.net/": "oid", "https://login.microsoftonline.us/": "oid", "https://login.partner.microsoftonline.cn/": "oid"}'
```

### SSO Groups Sync

> [!NOTE]
>
> SSO Groups Sync on self-hosted requires LangSmith chart version **0.15.0-rc.3** (application version **0.15.2rc1**) or later.

[SSO Groups Sync](../../Govern/Users%20%26%20access%20control/User%20management.md#sso-groups-sync-alternative) lets LangSmith assign org and workspace roles from a group membership claim on the OIDC token, as a simpler alternative to [SCIM](../../Govern/Users%20%26%20access%20control/User%20management.md#set-up-scim-for-your-organization). On self-hosted, you must configure the IdP to include groups in the OIDC ID token before LangSmith can read them. Groups in the token can also set membership in [synced teams](../../Govern/Users%20%26%20access%20control/Teams.md#sync-team-members-from-your-identity-provider).

**IdP-side configuration (varies by provider):**

1. Configure your IdP application to emit a group membership claim in the OIDC ID token. The source attribute and the resulting claim name vary by IdP. Common examples include `groups`, `roles`, or a custom claim name. LangSmith does not dictate the source attribute.
2. Depending on your IdP, you may need to add an additional scope (commonly `groups`) to `oauthScopes` to receive the claim. Check your IdP's documentation for the required scope and any additional configuration needed to include group memberships in the token.
3. Group names must follow the [SCIM naming convention](../../Govern/Users%20%26%20access%20control/User%20management.md#group-naming-convention) (e.g., `LS:Organization Admin`, `LS:Organization User:prod:Editor`). The separator is shared with SCIM via [`scim_group_name_separator`](../../Govern/Users%20%26%20access%20control/User%20management.md#configure-custom-separator).

**Helm configuration:**

If your IdP requires an additional OIDC scope to include groups in the token (commonly `groups`), add it to `oauthScopes`:

```yaml Helm
config:
  authType: mixed
  hostname: https://langsmith.example.com
  oauth:
    enabled: true
    oauthClientId: <YOUR CLIENT ID>
    oauthClientSecret: <YOUR CLIENT SECRET>
    oauthIssuerUrl: <YOUR DISCOVERY URL>
    oauthScopes: "email,profile,openid,groups"
```

The exact scope name (`groups`, `roles`, etc.) depends on your IdP. Check your IdP's OIDC documentation.

**LangSmith-side configuration:**

Per-provider SSO Groups Sync settings are stored on the SSO provider record and toggled via the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-self-host-sso) or [API](../../../Monitor/Reference/LangSmith%20reference.md) (not via Helm values).

> [tab] UI
>
> Once your IdP emits the groups claim, configure SSO Groups Sync from the UI: go to **Settings** > **SSO configuration** and scroll to the **SSO Groups Sync** section. The claim name configured in the **Groups claim field** must match the claim emitted by your IdP.

> [tab] API
>
> To configure SSO Groups Sync via the API, first `GET` the current SSO settings to retrieve the provider `id`, then `PATCH` using that `id`:
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> # 1. Fetch the current SSO settings (and the id required for PATCH)
> curl -s "$SELF_HOSTED_LANGSMITH_ENDPOINT/api/v1/orgs/current/sso-settings" \
>   -H "X-Api-Key: $LANGSMITH_API_KEY" | jq .
>
> # 2. PATCH using the id returned above
> curl -s -X PATCH "$SELF_HOSTED_LANGSMITH_ENDPOINT/api/v1/orgs/current/sso-settings/<id>" \
>   -H "X-Api-Key: $LANGSMITH_API_KEY" \
>   -H "Content-Type: application/json" \
>   -d '{
>     "sso_groups_enabled": true,
>     "sso_groups_claim_field": "groups",
>     "sso_groups_required": true,
>     "sso_groups_role_sync_enabled": true
>   }' | jq .
> ```
>
> > [!WARNING]
> >
> > `DELETE` is also available on this resource but is not covered here. `DELETE` removes the SSO provider entirely and locks out login if the org has **Login via SSO only** enabled, or if no other authentication providers (for example, social login) are configured.

#### Emit the groups claim from Microsoft Entra ID

For OIDC on self-hosted, add the groups claim through the App Registration Manifest. Skip the **Token configuration** > **Add groups claim** flow, which does not support display names for cloud-only security groups.

> [!WARNING]
>
> Set the top-level `groupMembershipClaims` property to `"ApplicationGroup"`. Other values change behavior in ways that are hard to diagnose:
>
> * Missing or `"None"`: no groups appear in the token.
> * `"SecurityGroup"` or `"All"`: groups appear, but the `cloud_displayname` value is silently ignored and the token contains group object IDs instead of names.
> * `"ApplicationGroup"`: groups resolve to display names, but only for groups explicitly assigned to the Enterprise Application under **Users and groups**.
>
> The `cloud_displayname` value is only supported for single-tenant applications.

In **App registrations** > your app > **Manifest**, merge the following into the manifest, keeping any existing `optionalClaims.idToken` entries such as `email`:

```json
"groupMembershipClaims": "ApplicationGroup",
"optionalClaims": {
  "idToken": [
    {
      "name": "email",
      "source": null,
      "essential": false,
      "additionalProperties": []
    },
    {
      "name": "groups",
      "source": null,
      "essential": false,
      "additionalProperties": ["cloud_displayname"]
    }
  ],
  "accessToken": [],
  "saml2Token": []
}
```

Then, in **Enterprise applications** > your app > **Users and groups**, assign every group that maps to a LangSmith role. Groups that are not assigned to the Enterprise Application do not appear in the token.

#### Create Microsoft Entra ID groups for SSO Groups Sync

Groups used for SSO Groups Sync must follow the [group naming convention](../../Govern/Users%20%26%20access%20control/User%20management.md#group-naming-convention) documented on the main user management page (for example, `LS:Organization Admins`, `LS:Organization User:Production:Editor`). Group names are case-sensitive and must match the convention exactly.

To create a group in Microsoft Entra ID:

1. In the Microsoft Entra admin center, go to **Groups** > **New group**.
2. Set **Group type** to `Security`.
3. Set **Membership type** to `Assigned` (dynamic membership is not supported).
4. Set **Group name** to a value that matches the naming convention.
5. Add members, then click **Create**.

Group membership changes take effect on each user's next login.

#### Verify the groups claim in the token

After completing IdP-side configuration, verify that the OIDC ID token contains the expected groups claim:

1. Sign out of LangSmith, then sign back in via SSO.
2. In your browser's developer tools, go to **Application** > **Cookies** and locate the OAuth session cookie.
3. Decode the ID token with a JWT decoder (for example, [jwt.io](https://jwt.io)) and confirm the `groups` claim contains display names, not object IDs:

```json
{
  "groups": [
    "LS:Organization Admins",
    "LS:Organization User:Production:Editor"
  ]
}
```

If the claim contains UUIDs instead of names, revisit the `groupMembershipClaims` value in the manifest and confirm the groups are assigned to the Enterprise Application under **Users and groups**.

If the groups claim is correct but LangSmith does not assign roles, check the token's `iss` claim. It must match `oauthIssuerUrl`, which for Microsoft Entra ID is `https://login.microsoftonline.com/<tenant-id>/v2.0`. When they do not match, the `platform-backend` logs show `SSO groups gate skipped: no saml_providers row matched issuer`. An `iss` of `https://sts.windows.net/<tenant-id>/` means `oauthIssuerUrl` is missing the `/v2.0` suffix. Add the suffix as described in [Step 1. Register the application](#step-1-register-the-application).

## PKCE flow (deprecated)

We recommend running with a [`Client Secret`](#provider-setup). However, if your IdP does not support this, you can use the `Authorization Code with PKCE` flow.

> [!WARNING]
>
> The PKCE workflow is **deprecated as of v16** and is scheduled for removal in a future release. [Migrate to the client secret flow](#migrate-from-pkce-to-client-secret) as soon as possible.

### Migrate from PKCE to client secret

You can switch an installation that uses PKCE to OAuth with client secret on its current chart version. Users keep their accounts, organization and workspace memberships, and API keys, as long as they sign in with the same email address.

To migrate:

1. Upgrade to Helm chart version 0.17.23 (LangSmith 0.17.51) or later. Earlier versions can lock out users whose IdP `sub` claim is their email address.

2. In your IdP, configure your existing application as a confidential (web) client:
   * Create a client secret.
   * Add `https://<host>/api/v1/oauth/custom-oidc/callback` as a redirect URI. The client secret flow requires `https`.

3. Update your `values.yaml`. Keep the same `oauthClientId` and `oauthIssuerUrl`, set `authType: mixed`, and add the client secret and `hostname`:

   ```yaml Helm
   config:
     authType: mixed
     hostname: https://langsmith.example.com
     oauth:
       enabled: true
       oauthClientId: <YOUR CLIENT ID>
       oauthClientSecret: <YOUR CLIENT SECRET>
       oauthIssuerUrl: <YOUR DISCOVERY URL>
   ```

4. Run `helm upgrade` **without changing the chart version**. Users must sign in again.

5. Confirm users can sign in, then upgrade LangSmith as a separate `helm upgrade`.

> [!NOTE]
>
> Switch to client secret and upgrade the chart version in separate `helm upgrade` runs. Helm runs the upgrade jobs before it applies the new configuration, so a combined run can fail.

### Requirements

> [!NOTE]
>
> This flow does **not** require a `Client Secret`.

There are a couple of requirements for using OAuth SSO with LangSmith:

* Your IdP must support the `Authorization Code with PKCE` [flow](https://www.oauth.com/oauth2-servers/pkce) (Google does not support this flow for example, but see [above](#with-client-secret-recommended) for an alternative configuration that Google supports). This is often displayed in your OAuth Provider as configuring a "Single Page Application (SPA)"
* Your IdP must support using an external discovery/issuer URL. We will use this to fetch the necessary routes and keys for your IdP.
* You must provide the `OIDC`, `email`, and `profile` scopes to LangSmith. We use these to fetch the necessary user information and email for your users.
* You will need to set the callback URL in your IdP to `http://<host>/oauth-callback`, where host is the domain or IP you have provisioned for your LangSmith instance. This is where your IdP will redirect the user after they have authenticated.
* You will need to provide the `oauthClientId` and `oauthIssuerUrl` in your `values.yaml` file. This is where you will configure your LangSmith instance.

```yaml Helm
config:
  oauth:
    enabled: true
    oauthClientId: <YOUR CLIENT ID>
    oauthIssuerUrl: <YOUR DISCOVERY URL>
```

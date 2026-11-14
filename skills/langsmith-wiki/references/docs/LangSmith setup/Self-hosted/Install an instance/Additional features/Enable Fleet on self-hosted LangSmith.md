# Enable Fleet on self-hosted LangSmith

> Install Fleet and optionally configure tools and triggers on self-hosted LangSmith.

[Fleet](../../../../No-code%20agents/Fleet/No-code%20agents%20with%20LangSmith%20Fleet.md) lets you create and manage agents without writing code. Enable it when your installation needs no-code agents.

## Prerequisites

Fleet requires an [Enterprise](https://langchain.com/pricing) plan and [LangSmith Self-Hosted v0.13](https://changelog.langchain.com/announcements/langsmith-self-hosted-v0-13) or later. This standalone deployment configuration requires v0.15 or later. Install the [base LangSmith platform](../Self-host%20LangSmith%20on%20Kubernetes.md) first.

Fleet provisions an API server, task queue, PostgreSQL, Redis, tool server, and trigger server. It does not require Agent Server hosting.

## Enable Fleet

Generate a Fernet encryption key for Fleet:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Store it as `agent_builder_encryption_key` in your [existing LangSmith app Secret](../../Platform%20auth%20%26%20access%20control/Use%20an%20existing%20secret%20for%20your%20installation%20%28Kubernetes%29.md#parameters). Add the following to your [`langsmith_config.yaml`](../Self-host%20LangSmith%20on%20Kubernetes.md#configure-your-helm-charts):

```yaml
config:
  existingSecretName: "<your-secret-name>"

fleet:
  enabled: true

fleetToolServer:
  enabled: true

fleetTriggerServer:
  enabled: true
```

Alternatively, set `fleet.encryptionKey` inline. Do not commit encryption keys to version control. Both `fleetToolServer` and `fleetTriggerServer` are required.

> [!WARNING]
>
> If you are migrating from the legacy `agentBootstrap` deployment model, contact technical support through the [Support Portal](https://support.langchain.com) before upgrading. Current charts reject `backend.agentBootstrap`, `config.insights`, and `config.polly`; remove these legacy settings rather than setting them to `false`. Disable the legacy `config.agentBuilder.enabled` flag. Preserve existing Fleet data before deleting legacy deployments.

Fleet uses dedicated PostgreSQL and Redis instances by default. To use external databases, configure `fleet.postgres.external` and `fleet.redis.external`:

```yaml
fleet:
  enabled: true
  postgres:
    external:
      enabled: true
      connectionUrl: "<fleet-postgres-connection-url>"
  redis:
    external:
      enabled: true
      connectionUrl: "<fleet-redis-connection-url>"
```

Apply the changes and verify the pods:

```bash
helm upgrade -i langsmith langchain/langsmith --values langsmith_config.yaml --version <version> -n <namespace> --wait --debug
kubectl get pods -n <namespace>
```

### (Optional) Forward caller headers to MCP servers

Header forwarding passes `X-Fleet-Forward-*` headers from a Fleet API run request to the agent's custom MCP servers on each tool call. Use it to give an MCP server, or a policy gateway in front of it, per-run context such as the end user's ID.

Header forwarding requires Helm chart version 0.17.0 or later. It is disabled by default.

To enable it, set `FLEET_MCP_FORWARD_CALLER_HEADERS` on the platform backend and on both Fleet components, then redeploy:

```yaml
platformBackend:
  deployment:
    extraEnv:
      - name: FLEET_MCP_FORWARD_CALLER_HEADERS
        value: "true"
fleet:
  apiServer:
    deployment:
      extraEnv:
        - name: FLEET_MCP_FORWARD_CALLER_HEADERS
          value: "true"
  queue:
    deployment:
      extraEnv:
        - name: FLEET_MCP_FORWARD_CALLER_HEADERS
          value: "true"
```

> [!WARNING]
>
> Set the variable on all three components. The platform backend reads the headers from the request and replaces any forwarded headers the caller put in the run body. If you enable it only on the Fleet components, callers can set forwarded header values directly in the run body.

For how to send forwarded headers, see [Forward caller headers to MCP servers](../../../../No-code%20agents/Fleet/Advanced/Use%20Fleet%20agents%20in%20code.md#forward-caller-headers-to-mcp-servers).

### (Optional) Enable OAuth tools and triggers for Fleet

To enable OAuth-based tools such as Gmail, Slack, or Linear in Fleet, configure the `providerOrgId` and add provider IDs for each integration you want to use. You can enable any combination of providers.

#### Available providers

| Provider | Tools enabled | Trigger enabled |
| - | - | - |
| `googleOAuthProvider` [setup guide](#google-oauth-provider) | Gmail, Google Calendar, Google Sheets, BigQuery | Gmail |
| `linearOAuthProvider` [setup guide](#linear-oauth-provider) | Linear | - |
| `linkedinOAuthProvider` [setup guide](#linkedin-oauth-provider) | LinkedIn | - |
| `microsoftOAuthProvider` [setup guide](#microsoft-oauth-provider) | Outlook, Calendar, Teams, SharePoint, Word, Excel, PowerPoint | Outlook |
| `salesforceOAuthProvider` [setup guide](#salesforce-oauth-provider) | Salesforce | - |
| `slackOAuthProvider` [setup guide](#slack-oauth-provider) | Slack | Slack |

#### General configuration

Add the following to your [`langsmith_config.yaml`](../Self-host%20LangSmith%20on%20Kubernetes.md#configure-your-helm-charts). Include only the providers you need.

```yaml
fleet:
  oauth:
    # Organization ID where OAuth providers are configured
    providerOrgId: "<your-org-id>"
    # Add provider IDs for integrations you want to enable.
    slackOAuthProvider: "<provider-id>"
    googleOAuthProvider: "<provider-id>"
    linkedinOAuthProvider: "<provider-id>"
    linearOAuthProvider: "<provider-id>"
    microsoftOAuthProvider: "<provider-id>"
    salesforceOAuthProvider: "<provider-id>"
```

> [!WARNING]
>
> The provider ID must be unique and cannot end with `-agent-builder` or `-oauth-provider`.

#### Provider setup guides

> [accordion] Google OAuth provider
>
> To enable Google OAuth for Fleet, create an OAuth client in GCP and configure it with the required URLs and credentials.
>
> **1. Create OAuth client in GCP**
>
> Create a new OAuth client app (Web application) in [Google Cloud Console](https://console.cloud.google.com/apis/credentials).
>
> **2. Add URLs to GCP**
>
> Add the following URLs to your OAuth client, replacing `<hostname>` with your LangSmith hostname and `<provider-id>` with the provider ID you'll use (for example, `google`):
>
> **Authorized JavaScript origins:**
>
> * `https://<hostname>`
>
> **Authorized redirect URIs:**
>
> * `https://<hostname>/api-host/v2/auth/callback/<provider-id>`
> * `https://<hostname>/host-oauth-callback/<provider-id>`
>
> **3. Copy credentials**
>
> Copy the **Client ID** and **Client Secret** from the GCP OAuth app.
>
> **4. Configure OAuth provider in LangSmith**
>
> In LangSmith, go to **Settings > OAuth Providers** and add a new provider:
>
> * **Client ID**: from GCP
> * **Client Secret**: from GCP
> * **Authorization URL**: `https://accounts.google.com/o/oauth2/auth`
> * **Token URL**: `https://oauth2.googleapis.com/token`
> * **Provider ID**: Unique string, for example: `google`
>
> **5. Apply the changes**
>
> Add the LangSmith OAuth provider ID to your [`langsmith_config.yaml`](../Self-host%20LangSmith%20on%20Kubernetes.md#configure-your-helm-charts) and deploy:
>
> ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> fleet:
>   oauth:
>     providerOrgId: "<your-org-id>"
>     googleOAuthProvider: "<provider-id>"
> ```
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> helm upgrade -i langsmith langchain/langsmith --values langsmith_config.yaml --version <version> -n <namespace> --wait --debug
> ```

> [accordion] Microsoft OAuth provider
>
> To enable Microsoft OAuth for Fleet, create an Azure app registration, add the required Microsoft Graph delegated permissions, and configure a Microsoft OAuth provider in LangSmith.
>
> **1. Create an Azure app registration**
>
> In the [Microsoft Entra admin center](https://entra.microsoft.com/), go to **Applications > App registrations** and create a new registration.
>
> **2. Choose supported account types**
>
> Select the account type that matches your deployment. If you need users from multiple Microsoft Entra tenants to authenticate, choose a multi-tenant option. If your deployment is limited to one tenant, you can use a single-tenant app registration.
>
> **3. Add the redirect URI**
>
> Add the following web redirect URI, replacing `<hostname>` with your LangSmith hostname and `<provider-id>` with your provider ID:
>
> ```
> https://<hostname>/host-oauth-callback/<provider-id>
> ```
>
> **4. Create a client secret**
>
> In **Certificates & secrets**, create a new client secret. Copy the **Application (client) ID** and the generated client secret value.
>
> **5. Add Microsoft Graph delegated permissions**
>
> In **API permissions**, add the following Microsoft Graph delegated permissions:
>
> * `Mail.ReadWrite`
>
> * `Mail.Send`
>
> * `Calendars.ReadWrite`
>
> * `Team.ReadBasic.All`
>
> * `Channel.ReadBasic.All`
>
> * `Channel.Create`
>
> * `ChannelMessage.Send`
>
> * `ChannelMessage.Read.All`
>
> * `Chat.Create`
>
> * `Chat.ReadWrite`
>
> * `User.ReadBasic.All`
>
> * `Files.ReadWrite.All`
>
> * `Sites.ReadWrite.All`
>
> > [!NOTE]
> >
> > LangSmith automatically requests `offline_access` for Microsoft providers so users can receive refresh tokens.
>
> **6. Grant tenant consent**
>
> Grant admin consent for the tenant if your Microsoft 365 policies require it for these delegated permissions.
>
> **7. Configure OAuth provider in LangSmith**
>
> In LangSmith, go to **Settings > OAuth Providers** and add a new provider:
>
> * **Name**: For example, `Microsoft`
>
> * **Provider ID**: Unique string, for example: `microsoft-oauth-provider`
>
> * **Client ID**: Application (client) ID from Azure
>
> * **Client Secret**: Client secret value from Azure
>
> * **Authorization URL**: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`
>
> * **Token URL**: `https://login.microsoftonline.com/common/oauth2/v2.0/token`
>
> * **Provider Type**: `microsoft`
>
> * **Token endpoint auth method**: `client_secret_post`
>
> > [!NOTE]
> >
> > If you created a single-tenant app registration, replace `common` in the authorization and token URLs with your tenant ID.
>
> **8. Apply the changes**
>
> Add the following to your [`langsmith_config.yaml`](../Self-host%20LangSmith%20on%20Kubernetes.md#configure-your-helm-charts) and deploy:
>
> ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> fleet:
>   oauth:
>     providerOrgId: "<your-org-id>"
>     microsoftOAuthProvider: "<provider-id>"
> ```
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> helm upgrade -i langsmith langchain/langsmith --values langsmith_config.yaml --version <version> -n <namespace> --wait --debug
> ```

> [accordion] Linear OAuth provider
>
> To enable Linear OAuth for Fleet, create a Linear OAuth app and configure it with the required credentials.
>
> **1. Create a Linear OAuth app**
>
> Go to [Linear Settings > API > Applications](https://linear.app/settings/api/applications/new) and create a new OAuth application.
>
> **2. Add callback URL**
>
> Set the callback URL, replacing `<hostname>` with your LangSmith hostname and `<provider-id>` with your provider ID:
>
> ```
> https://<hostname>/host-oauth-callback/<provider-id>
> ```
>
> **3. Copy credentials**
>
> After creating the app, copy the **Client ID** and **Client Secret**.
>
> **4. Configure OAuth provider in LangSmith**
>
> In LangSmith, go to **Settings > OAuth Providers** and add a new provider:
>
> * **Client ID**: from Linear app
> * **Client Secret**: from Linear app
> * **Authorization URL**: `https://linear.app/oauth/authorize`
> * **Token URL**: `https://api.linear.app/oauth/token`
> * **Provider ID**: Unique string, for example: `linear`
>
> **5. Apply the changes**
>
> Add the following to your [`langsmith_config.yaml`](../Self-host%20LangSmith%20on%20Kubernetes.md#configure-your-helm-charts) and deploy:
>
> ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> fleet:
>   oauth:
>     providerOrgId: "<your-org-id>"
>     linearOAuthProvider: "<provider-id>"
> ```
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> helm upgrade -i langsmith langchain/langsmith --values langsmith_config.yaml --version <version> -n <namespace> --wait --debug
> ```

> [accordion] LinkedIn OAuth provider
>
> To enable LinkedIn OAuth for Fleet, create a LinkedIn OAuth app and configure it with the required credentials.
>
> **1. Create a LinkedIn OAuth app**
>
> Go to [linkedin.com/developers/apps](https://www.linkedin.com/developers/apps/) and create a new app.
>
> **2. Add redirect URI**
>
> In your app settings, go to the **Auth** tab. Add the following redirect URI, replacing `<hostname>` with your LangSmith hostname and `<provider-id>` with your provider ID:
>
> ```
> https://<hostname>/host-oauth-callback/<provider-id>
> ```
>
> **3. Copy credentials**
>
> Copy the **Client ID** and **Client Secret** from the Auth tab.
>
> **4. Configure OAuth provider in LangSmith**
>
> In LangSmith, go to **Settings > OAuth Providers** and add a new provider:
>
> * **Client ID**: from LinkedIn app
> * **Client Secret**: from LinkedIn app
> * **Authorization URL**: `https://www.linkedin.com/oauth/v2/authorization`
> * **Token URL**: `https://www.linkedin.com/oauth/v2/accessToken`
> * **Provider ID**: Unique string, for example: `linkedin`
>
> **5. Apply the changes**
>
> Add the following to your [`langsmith_config.yaml`](../Self-host%20LangSmith%20on%20Kubernetes.md#configure-your-helm-charts) and deploy:
>
> ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> fleet:
>   oauth:
>     providerOrgId: "<your-org-id>"
>     linkedinOAuthProvider: "<provider-id>"
> ```
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> helm upgrade -i langsmith langchain/langsmith --values langsmith_config.yaml --version <version> -n <namespace> --wait --debug
> ```

> [accordion] Salesforce OAuth provider
>
> To enable Salesforce OAuth for Fleet, create a Salesforce External Client App, configure its OAuth settings and policies, retrieve its credentials, then configure a Salesforce OAuth provider in LangSmith.
>
> **1. Create an External Client App**
>
> In Salesforce **Setup**, use **Quick Find** to open **External Client App Manager**, then click **New External Client App**.
>
> Under **Basic Information**, set:
>
> * **External Client App Name**: for example, `LangSmith Fleet`
>
> * **Contact Email**: an admin email address
>
> * **Distribution State**: **Local**
>
> > [!NOTE]
> >
> > External Client Apps are the current framework Salesforce uses for OAuth integrations. If **New External Client App** is unavailable, confirm that app creation is enabled for your org under **Setup > External Client App Settings**.
>
> **2. Enable OAuth and configure the OAuth settings**
>
> Expand **API (Enable OAuth Settings)** and select **Enable OAuth**. Then configure:
>
> * **Callback URL**, replacing `<hostname>` with your LangSmith hostname and `<provider-id>` with your provider ID:
>
> ```
> https://<hostname>/host-oauth-callback/<provider-id>
> ```
>
> * **Selected OAuth Scopes**: add **Manage user data via APIs (api)** and **Perform requests at any time (refresh\_token, offline\_access)**.
> * Keep **Require Secret for the Web Server Flow** selected.
> * Leave **Enable Authorization Code and Credentials Flow** and **Enable Client Credentials Flow** unselected. Fleet uses the standard web server (authorization code) flow.
>
> Click **Create**.
>
> **3. Set the OAuth policies**
>
> Open the app, select the **Policies** tab, and click **Edit**:
>
> * **Refresh Token Policy**: select **Refresh token is valid until revoked**.
> * **Permitted Users**: leave **All users may self-authorize**. If you choose **Admin approved users are pre-authorized** instead, you must first assign the app to a permission set or profile, or authorization fails.
>
> Click **Save**.
>
> > [!NOTE]
> >
> > An External Client App is configured in two places: **Settings** (the OAuth definition from the previous step) and **Policies** (this step). Both must be saved.
>
> **4. Copy the credentials**
>
> On the **Settings** tab, under **OAuth Settings**, select **Consumer Key and Secret**. The **Consumer Key** is your Client ID and the **Consumer Secret** is your Client Secret.
>
> > [!NOTE]
> >
> > After you create the app, allow up to 30 minutes for it to propagate before the first connection attempt.
>
> **5. Configure OAuth provider in LangSmith**
>
> In LangSmith, go to **Settings > OAuth Providers**, click **OAuth Provider**, and fill in:
>
> * **Provider ID**: Unique string, for example: `salesforce-oauth-provider`. Use this same value for `salesforceOAuthProvider` in the next step.
> * **Display Name**: For example, `Salesforce`
> * **Client ID**: Consumer Key from Salesforce
> * **Client Secret**: Consumer Secret from Salesforce
> * **Authorization URL**: `https://<MyDomain>.my.salesforce.com/services/oauth2/authorize`
> * **Token URL**: `https://<MyDomain>.my.salesforce.com/services/oauth2/token`
>
> LangSmith recognizes Salesforce automatically from the Token URL, so there is no provider-type or token-auth-method field to set. Leave **Enable PKCE** off to match the web server flow configured above.
>
> > [!NOTE]
> >
> > Replace `<MyDomain>` with your org's My Domain, found under **Setup > My Domain**. For a sandbox, use `https://<MyDomain>--<SandboxName>.sandbox.my.salesforce.com/services/oauth2/authorize` and the matching token URL.
>
> **6. Apply the changes**
>
> Add the following to your [`langsmith_config.yaml`](../Self-host%20LangSmith%20on%20Kubernetes.md#configure-your-helm-charts) and deploy:
>
> ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> fleet:
>   oauth:
>     providerOrgId: "<your-langsmith-org-id>"
>     salesforceOAuthProvider: "<provider-id>"
> ```
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> helm upgrade -i langsmith langchain/langsmith --values langsmith_config.yaml --version <version> -n <namespace> --wait --debug
> ```
>
> > [!WARNING]
> >
> > If sign-in fails: confirm the **Callback URL** in Salesforce exactly matches `https://<hostname>/host-oauth-callback/<provider-id>` (HTTPS, no trailing slash); if you selected **Admin approved users are pre-authorized**, assign the app via a permission set; and if your org enforces login IP ranges, allowlist your Fleet server's egress IPs on the user's profile or set **IP Relaxation** to **Relax IP restrictions** in the app's policies.

> [accordion] Slack OAuth provider
>
> One Slack OAuth provider powers both Slack tools and the Slack apps you add to individual agents, so Slack setup lives with the rest of the Slack integration.
>
> For the full walkthrough, see [Set up Slack on Self-hosted](../../../../No-code%20agents/Fleet/Tools%20and%20automation/Integrate%20Slack%20with%20an%20agent.md#set-up-slack-on-self-hosted). It covers creating the Slack app, adding bot scopes, registering the provider, setting the redirect URI, and configuring Helm values.

### (Optional) Enable GitHub App for Fleet

Fleet integrates with GitHub through a dedicated **GitHub App** (not an OAuth app). The GitHub App provides repository access for Fleet's GitHub tools and supports the user authorization flow required for private repository access.

Setup involves creating a GitHub App, gathering its credentials, storing them as Kubernetes secrets, and referencing them from your [`langsmith_config.yaml`](../Self-host%20LangSmith%20on%20Kubernetes.md#configure-your-helm-charts).

**1. Create a GitHub App**

Go to [GitHub Settings > Developer settings > GitHub Apps](https://github.com/settings/apps) and click **New GitHub App**.

> [!NOTE]
>
> You can create the app under a personal account or an organization. If multiple people will manage the integration, an organization-owned app is recommended.

**2. Fill in basic details**

* **GitHub App name**: Any unique name, for example `acme-langsmith-fleet`. Make a note of the slug GitHub generates (the lowercased, hyphenated form of the name), as this is the value you'll use for `FLEET_GITHUB_APP_SLUG`.
* **Homepage URL**: Your LangSmith hostname, for example `https://langsmith.acme.com`.
* Deselect **Active** under **Webhook** for now. You'll enable it in a later step after generating a webhook secret.

**3. Set callback URLs**

Under **Identifying and authorizing users**, add the following **Callback URL**, replacing `<hostname>` with your LangSmith hostname:

```
https://<hostname>/api/v1/platform/fleet/providers/github-app/auth/callback
```

Select **Redirect on update**.

Under **Post installation**, add the following **Setup URL**:

```
https://<hostname>/api/v1/platform/fleet/providers/github-app/callback
```

Select **Redirect on update**.

**4. Set webhook URL and generate a webhook secret**

Generate a random webhook secret:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(48))"
```

Under **Webhook**:

* Select **Active**.

* Set the **Webhook URL** to:

  ```
  https://<hostname>/api/v1/platform/fleet/providers/github-app/webhooks
  ```

* Paste the generated value into **Webhook secret**. Save it, as you'll need the same value when creating the Kubernetes secret in a later step.

**5. Set repository permissions**

Under **Permissions > Repository permissions**, grant the following:

* **Contents**: Read and write
* **Issues**: Read and write
* **Pull requests**: Read and write
* **Metadata**: Read-only (automatically selected)

Under **Permissions > Account permissions**, grant **Email addresses: Read-only**.

> [!NOTE]
>
> These are the minimum permissions required for Fleet's built-in GitHub tools (issue management, pull request creation, repository content access). Adjust if you need additional tool capabilities.

**6. Choose install visibility**

Under **Where can this GitHub App be installed?**, select the option that matches your distribution needs. For most self-hosted deployments, **Only on this account** is correct.

**7. Create the app**

Click **Create GitHub App**. On the app settings page, note the following values:

| Value | Where to find it | Environment variable |
| - | - | - |
| **App ID** | Numeric, at the top of the page | `FLEET_GITHUB_APP_ID` |
| **Public link** | For example, `https://github.com/apps/acme-langsmith-fleet` | `FLEET_GITHUB_APP_PUBLIC_LINK` |
| App slug | Last path segment of the public link | `FLEET_GITHUB_APP_SLUG` |
| **Client ID** | Under **About** | `FLEET_GITHUB_APP_CLIENT_ID` |

**8. Generate a client secret**

Under **Client secrets**, click **Generate a new client secret** and copy the value. This is `FLEET_GITHUB_APP_CLIENT_SECRET`. GitHub only shows it once.

**9. Generate a private key**

Scroll to **Private keys** and click **Generate a private key**. GitHub downloads a `.pem` file. Keep this file secure, as it grants full access to the GitHub App. The PEM contents are `FLEET_GITHUB_APP_PRIVATE_KEY`.

**10. Generate a state JWT secret**

LangSmith signs short-lived OAuth state tokens with an HMAC key. Generate one:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(48))"
```

This is `FLEET_GITHUB_APP_STATE_JWT_SECRET`.

**11. Create a Kubernetes secret**

Store the sensitive values in a Kubernetes secret:

```bash
kubectl create secret generic fleet-github-app \
  --namespace <your-langsmith-namespace> \
  --from-literal=client_secret="<SECRET>" \
  --from-literal=webhook_secret="<SECRET>" \
  --from-literal=state_jwt_secret="<SECRET>" \
  --from-file=private_key=/path/to/fleet-app.private-key.pem
```

For production deployments, manage this secret through your existing secrets workflow (for example, [Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets) or [External Secrets Operator](https://external-secrets.io/)). See [Use an existing secret](../../Platform%20auth%20%26%20access%20control/Use%20an%20existing%20secret%20for%20your%20installation%20%28Kubernetes%29.md) for more.

**12. Add the configuration to your langsmith\_config.yaml**

Add the following, replacing the placeholder values with the non-sensitive values gathered above:

```yaml
commonEnv:
  - name: FLEET_GITHUB_APP_ID
    value: "<app-id>"
  - name: FLEET_GITHUB_APP_SLUG
    value: "<app-slug>"
  - name: FLEET_GITHUB_APP_PUBLIC_LINK
    value: "https://github.com/apps/<app-slug>"
  - name: FLEET_GITHUB_APP_CLIENT_ID
    value: "<client-id>"
  - name: FLEET_GITHUB_APP_CLIENT_SECRET
    valueFrom:
      secretKeyRef:
        name: fleet-github-app
        key: client_secret
  - name: FLEET_GITHUB_APP_PRIVATE_KEY
    valueFrom:
      secretKeyRef:
        name: fleet-github-app
        key: private_key
  - name: FLEET_GITHUB_APP_WEBHOOK_SECRET
    valueFrom:
      secretKeyRef:
        name: fleet-github-app
        key: webhook_secret
  - name: FLEET_GITHUB_APP_STATE_JWT_SECRET
    valueFrom:
      secretKeyRef:
        name: fleet-github-app
        key: state_jwt_secret

fleetToolServer:
  deployment:
    extraEnv:
      - name: FLEET_GITHUB_APP_ENABLED
        value: "true"
```

> [!NOTE]
>
> `FLEET_GITHUB_APP_ENABLED` must be set on the tool server so the GitHub tools are registered. The remaining `FLEET_GITHUB_APP_*` variables are consumed by the platform backend and live under `commonEnv`.

**13. Deploy and install the app on repositories**

Run the following command to apply the changes:

```bash
helm upgrade -i langsmith langchain/langsmith --values langsmith_config.yaml --version <version> -n <namespace> --wait --debug
```

Once pods are healthy:

1. In LangSmith, open a Fleet agent and go to the GitHub integration in the agent editor.
2. Click **Connect GitHub** to install the app on the repositories Fleet should access.
3. For private repositories, you must explicitly select each repository during installation.

> [!NOTE]
>
> Each user must also authorize the GitHub App against their own GitHub account using the re-auth flow in LangSmith. This allows Fleet to resolve per-user tokens for tools that act on behalf of a user.

## Disable Fleet

To disable Fleet, set these values and apply the Helm upgrade:

```yaml
fleet:
  enabled: false
fleetToolServer:
  enabled: false
fleetTriggerServer:
  enabled: false
```

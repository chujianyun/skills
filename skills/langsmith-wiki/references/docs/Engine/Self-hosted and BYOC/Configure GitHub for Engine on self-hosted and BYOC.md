# Configure GitHub for Engine on self-hosted and BYOC

> Register a GitHub App and configure self-hosted LangSmith or a BYOC data plane so LangSmith Engine can read repositories and open pull requests, on GitHub.com, Enterprise Cloud with data residency, or Enterprise Server.

[LangSmith Engine](../LangSmith%20Engine.md) reads repositories and opens pull requests through a GitHub App that you register. Complete this setup once per LangSmith installation or BYOC data plane. Workspace users then [connect repositories](../Connect%20Engine%20to%20your%20repository.md#connect-repositories) with that App.

* **BYOC**: An Organization Admin saves the App's credentials in the LangSmith UI. See [Configure the App on BYOC](#configure-the-app-on-byoc).
* **Self-hosted**: An operator configures the App's credentials in Helm values. See [Configure the App on self-hosted](#configure-the-app-on-self-hosted).

This configuration is separate from GitHub setup for Agent Server builds and previews.

## Configure the App on BYOC

On a [BYOC](../../LangSmith%20setup/BYOC/Bring%20Your%20Own%20Cloud%20%28BYOC%29.md) data plane, you register your own GitHub App and save its credentials from an Engine project in the LangSmith UI. You do not set environment variables or Helm values. Complete this setup once per data plane: every workspace on the data plane shares the App.

Configuring the App requires the `organization:manage` permission in the organization that owns the data plane. Other users see **An installation administrator must configure the GitHub App.**

To configure the App:

**1. Open the GitHub App settings**

Open a tracing project or agent environment. In its **Engine** tab, select **Configure Engine**. Under **Code repository**, the **GitHub is not configured** notice appears. Click **Configure GitHub App**.

You can also configure the App while first setting up Engine for a project.

**2. Register the App on GitHub**

In the **Set up Engine GitHub App** dialog, click **Create App on GitHub**. The dialog lists the **Homepage URL**, **Redirect URI**, and **Webhook URL** for your data plane. Copy these values into the GitHub registration form.

Configure the remaining settings, permissions, and event subscriptions as described in [Complete the registration form](#complete-the-registration-form). Use the URLs from the dialog, not the self-hosted examples. To choose the App's owner and visibility, see [Choose who owns the App](#choose-who-owns-the-app).

**3. Generate the App credentials**

In the App's settings on GitHub, generate a client secret and a private key. Use the webhook secret that you entered during registration. For details, see [Save the App values](#save-the-app-values). You do not need an OAuth state secret on BYOC.

**4. Save the credentials in LangSmith**

In the dialog, enter:

* **App ID**: The numeric App ID, not the Client ID or installation ID.
* **GitHub App Name**: The name from the App's public URL, for example `my-engine-app`.
* **Client ID**: The App's Client ID.
* **Client secret**: The client secret you generated.
* **Private key (PEM)**: The complete contents of the downloaded PEM file, including newlines.
* **Webhook secret**: The same webhook secret that you entered in GitHub.

Click **Save configuration**. LangSmith stores the secrets encrypted and does not display them again.

**5. Connect repositories**

[Connect repositories](../Connect%20Engine%20to%20your%20repository.md#connect-repositories) and [verify the connection](../Connect%20Engine%20to%20your%20repository.md#verify-the-connection). While you test, check that GitHub delivers webhooks, as described in [Verify webhook delivery](#verify-webhook-delivery).

GitHub sends pull request webhooks to the **Webhook URL** on your data plane. If GitHub cannot reach that URL, Engine can still read code, generate fixes, and open pull requests. Pull request linking and automatic issue completion after a merge do not work.

To change the App later, click **Manage GitHub App**, then **Edit or replace App**. To remove it, click **Delete configuration**. Replacing the App requires you to reconnect repositories. For rotation guidance, see [Change or rotate configuration](#change-or-rotate-configuration).

## Configure the App on self-hosted

On self-hosted LangSmith, an operator registers the App, configures LangSmith, and verifies the connection.

> [!NOTE]
>
> Configuring GitHub for Engine on self-hosted requires LangSmith Helm chart version 0.17.2 or later. Earlier charts expose the `/api-host` routes that GitHub authorization and webhooks use only when Agent Server hosting is enabled (`config.deployment.enabled`).

Use the LangSmith application images supplied with your Helm chart release.

### Before you start

You need:

* **Engine and Sandboxes**: A working [self-hosted Engine deployment](LangSmith%20Engine%20on%20Self-hosted%20and%20BYOC.md) and permission to update its Helm values, secrets, and workloads.
* **GitHub administration**: Permission to register and install an App on the target repositories. Enterprise or organization policies may require approval.
* **Network access**: Browser, service, and sandbox connectivity, plus a webhook route reachable from GitHub. See [Allow network access](#allow-network-access).

### Choose your GitHub environment

Configure one GitHub instance and one App per LangSmith installation.

Set `ENGINE_GITHUB_WEB_BASE_URL` to your GitHub instance's web address:

| GitHub environment | Example web address |
| - | - |
| GitHub.com, including Enterprise Cloud | `https://github.com` |
| Enterprise Cloud with data residency | `https://example.ghe.com` |
| GitHub Enterprise Server (GHES) | `https://<ghes-hostname>` |

Replace the example enterprise address or GHES hostname placeholder with your own. GHES uses the same configuration on cloud infrastructure and on premises.

Use HTTPS on port 443 and a fully qualified hostname, without a path such as `/api/v3` or an organization name. LangSmith determines the API endpoints automatically. SSH Git URLs and custom GitHub ports are not supported.

#### Allow network access

All connections use HTTPS. Configure DNS, routing, and certificate trust for each source:

| Source | Destination | Purpose |
| - | - | - |
| User's browser | GitHub web host and LangSmith authorization callback URL | Sign-in, App authorization, and installation. |
| LangSmith services and Engine workers | GitHub web and API hosts | Authorization, repository information, branch and diff operations, PR creation/status, and App identity. |
| Sandbox hosts | GitHub web host | Clone repositories and push fix branches. |
| GitHub | LangSmith webhook URL | Link PRs to issues and complete issues after a merge. |

For API access, allow the host for your GitHub environment:

* **GitHub.com**: `api.github.com`.
* **Enterprise Cloud with data residency**: `api.example.ghe.com` for a web address of `https://example.ghe.com`.
* **GHES**: The same host as the web address, `<ghes-hostname>`.

GitHub.com and `ghe.com` send webhooks from outside your network; GHES sends them from your GHES environment. The webhook URL must be reachable from that source. Browser access through a VPN does not establish webhook access.

For GitHub IP allow lists, include the outbound addresses of LangSmith services and sandbox hosts, including any NAT gateway addresses.

Sandbox Git traffic requires direct routing to GitHub. Mandatory upstream HTTP/HTTPS forward proxies are not supported; `HTTPS_PROXY` on LangSmith API pods does not configure sandbox Git access.

For private IP addresses or a private CA, include the [private-GHES settings](#private-ghes-deployments) when configuring LangSmith below.

### Register a GitHub App

Register the App on the GitHub instance that hosts your repositories. An App registered on GitHub.com cannot be reused on GHES or a `ghe.com` enterprise.

For `ghe.com`, sign in through your enterprise's identity provider. Use that site throughout registration and installation; your personal GitHub.com account and its Apps are separate.

#### Choose who owns the App

The App's **owner** manages its registration and credentials. An **installation** grants access to selected repositories in an organization or account.

Choose ownership and visibility based on the repositories Engine needs:

| Repositories to connect | App configuration |
| - | - |
| Repositories in one organization | Create the App in that organization. Select **Only on this account** if it does not need installations elsewhere. |
| Repositories in several organizations within an enterprise | Create an enterprise-owned App and install it in each organization. This keeps installation limited to the enterprise. |
| Repositories in multiple organizations, or a mix of organizations and personal accounts, without managed users | Create an organization-owned App with **Any account**, then install it in each target account. On GHES, **Any account** applies only within that server. |
| Repositories owned by one personal account, without managed users | Create the App in the personal account and select **Only on this account**. |

Public visibility allows other accounts to install the App. It does not make repositories public or grant access without installation.

Enterprise-owned Apps have internal visibility and cannot be installed on personal accounts. Install in each organization; an enterprise-account installation does not grant repository access.

> [accordion] Enterprise visibility and managed users
>
> Only enterprise members can authorize an enterprise-owned App. If outside collaborators need to connect repositories, review their enterprise access before choosing that ownership type. See GitHub's [App visibility rules](https://docs.github.com/en/enterprise-cloud@latest/apps/creating-github-apps/registering-a-github-app/making-a-github-app-public-or-private) or the [GHES equivalent](https://docs.github.com/en/enterprise-server@3.20/apps/creating-github-apps/registering-a-github-app/making-a-github-app-public-or-private), selecting your server's documentation version.
>
> [GitHub Enterprise Cloud with data residency](https://docs.github.com/en/enterprise-cloud@latest/admin/data-residency/about-github-enterprise-cloud-with-data-residency) uses Enterprise Managed Users (EMU). Enterprise Cloud on GitHub.com can also use EMU; SSO alone does not mean an enterprise uses EMU.
>
> For EMU, connect organization-owned repositories. A managed user can register an App, but this Engine App cannot be installed on a managed user's personal account. See GitHub's [managed-user restrictions](https://docs.github.com/en/enterprise-cloud@latest/admin/managing-iam/understanding-iam-for-enterprises/abilities-and-restrictions-of-managed-user-accounts#github-apps).
>
> In an EMU enterprise, GitHub can show **This enterprise** instead of **Any account**. **Only on this account** limits an organization-owned App to that organization. Each target organization needs its own installation.
>
> An organization owner can install the App. Repository administrators in an EMU enterprise can install it only when it requests no organization permissions and enterprise policy permits installation.

#### Open the registration form

Choose the tab for the account that owns the App. These paths apply on the GitHub instance selected above:

> [tab] Organization
>
> You must be an organization owner or have permission to manage its Apps.
>
> To open the registration form:
>
> 1. Open your profile menu and select **Your organizations**.
> 2. Next to the organization that should own the App, select **Settings**.
> 3. Open **Developer settings** > **GitHub Apps** > **New GitHub App**.

> [tab] Enterprise
>
> An enterprise owner completes these steps. On GHES, enterprise-owned Apps require version 3.17 or later. On older versions, use an organization-owned App with the visibility needed for your repositories.
>
> To open the registration form:
>
> 1. Open your profile menu. With managed users, select **Your enterprise**. With personal accounts, select **Your enterprises**, then open the enterprise's **Settings**.
> 2. In the enterprise sidebar, under **Settings**, select **GitHub Apps**.
> 3. Select **New GitHub App**.
>
> For GitHub's instructions, see [Create an App for your enterprise](https://docs.github.com/en/enterprise-cloud@latest/admin/managing-github-apps-for-your-enterprise/creating-github-apps-for-your-enterprise).

> [tab] Personal account
>
> Use this option for a personal account without managed users.
>
> Open your profile menu and select **Settings** > **Developer settings** > **GitHub Apps** > **New GitHub App**.

#### Complete the registration form

Use these settings for all GitHub environments and App owners. For field definitions, see [Register a GitHub App](https://docs.github.com/en/enterprise-cloud@latest/apps/creating-github-apps/registering-a-github-app/registering-a-github-app). Replace `https://langsmith.example.com` with the browser-facing URL of your LangSmith deployment.

GitHub labels the authorization callback field **Callback URL** or **Redirect URI**. Both names refer to the URL where GitHub returns users after authorization.

If LangSmith uses a base path, include it. For example, a deployment at `https://langsmith.example.com/langsmith` uses `https://langsmith.example.com/langsmith/api-host/v1/integrations/forge/github/callback` as its authorization callback URL.

| GitHub setting | Value |
| - | - |
| **GitHub App name** | A unique name for your deployment, such as `acme-langsmith-engine`. |
| **Homepage URL** | Your LangSmith URL, such as `https://langsmith.example.com`. |
| **Callback URL** / **Redirect URI** | `https://langsmith.example.com/api-host/v1/integrations/forge/github/callback` |
| **Allow wildcard matching** | Leave disabled, if shown. |
| **Request user authorization (OAuth) during installation** | Enabled. Engine needs the authorization callback to finish connecting an installation. |
| **Expire user authorization tokens** | Leave enabled, if shown. |
| **Enable Device Flow** | Leave disabled. |
| **Setup URL** | Leave unset. When OAuth during installation is enabled, GitHub uses the authorization callback URL and may disable this field. |
| **Redirect on update** | Enabled. Returns users to LangSmith after they update an installation. |
| **Webhook: Active** | Enabled. |
| **Webhook URL** | `https://langsmith.example.com/api-host/v1/integrations/forge/github/webhook` |
| **Webhook secret** | A separately generated random secret, also configured in LangSmith. |
| **SSL verification** | Enabled. |
| **Where can this GitHub App be installed?** | The visibility selected in [Choose who owns the App](#choose-who-owns-the-app). This field does not appear for enterprise-owned Apps. |

For an existing App, manage token expiration under **Optional Features** > **User-to-server token expiration**. See [GitHub's token expiration settings](https://docs.github.com/en/enterprise-cloud@latest/apps/creating-github-apps/authenticating-with-a-github-app/refreshing-user-access-tokens#configuring-your-app-to-use-user-access-tokens-that-expire).

Generate the webhook secret with a cryptographically secure generator or your secret manager, using at least 32 random bytes. Save it for the LangSmith configuration.

Under **Permissions** > **Repository permissions**, configure:

| Permission | Access | Purpose |
| - | - | - |
| **Contents** | Read and write | Read code and push Engine's fix branches. |
| **Pull requests** | Read and write | Create draft PRs and read their status. |
| **Metadata** | Read-only, selected automatically | Identify repositories. |

Leave organization, account, and enterprise permissions unset. Engine's standard investigation and fix workflow does not require administration, workflow, or Checks permissions.

Under **Subscribe to events**, select **Pull request**. These events let Engine link externally created PRs that include Engine's issue reference and mark issues complete after a merge.

Select **Create GitHub App**.

#### Save the App values

After creating the App, open its settings and prepare the credentials:

1. Under **Client secrets**, select **Generate a new client secret** and save it immediately.
2. Under **Private keys**, select **Generate a private key**. Keep the downloaded PEM file; LangSmith needs its complete contents, including newlines.
3. Generate a separate **OAuth state secret** of at least 32 random bytes with your secret manager or a cryptographically secure generator. Use it only in LangSmith; do not enter it into GitHub or reuse the webhook secret.

Use this mapping when configuring LangSmith:

| Value | LangSmith environment variable |
| - | - |
| GitHub instance's web address | `ENGINE_GITHUB_WEB_BASE_URL` |
| **App ID** (numeric) | `ENGINE_GITHUB_APP_ID` |
| **Public link** (full URL) | `ENGINE_GITHUB_APP_PUBLIC_LINK` |
| **Client ID** | `ENGINE_GITHUB_APP_CLIENT_ID` |
| **Client secret** | `ENGINE_GITHUB_APP_CLIENT_SECRET` |
| **Private key** (PEM contents) | `ENGINE_GITHUB_APP_PRIVATE_KEY` |
| **Callback URL** / **Redirect URI** | `ENGINE_GITHUB_OAUTH_REDIRECT_URI` |
| **Webhook secret** | `ENGINE_GITHUB_APP_WEBHOOK_SECRET` |
| **OAuth state secret** | `ENGINE_GITHUB_OAUTH_STATE_SECRET` |

Copy the numeric **App ID**, not the Client ID or installation ID. Copy **Public link** exactly, including its full path; do not use the developer settings URL or an installation URL ending in `/installations/new`.

Use the exact authorization callback URL and webhook secret entered in GitHub. Include any LangSmith base path in the callback URL. The GitHub web address is the one selected in [Choose your GitHub environment](#choose-your-github-environment).

### Configure LangSmith

#### Store credentials

Using your [existing secret-management workflow](../../LangSmith%20setup/Self-hosted/Platform%20auth%20%26%20access%20control/Use%20an%20existing%20secret%20for%20your%20installation%20%28Kubernetes%29.md), create a Kubernetes Secret in the LangSmith namespace for the Client secret, private key, webhook secret, and OAuth state secret. The Helm example references a Secret named `langsmith-engine-github`. You can choose a different Secret name and keys; update the `secretKeyRef` entries to match.

Store credentials in Secrets, not in committed Helm values or command-line arguments. App IDs, Client IDs, and URLs can be included in Helm values.

#### Set Helm values

Enable `hostBackend` and place all `ENGINE_GITHUB_*` settings in `commonEnv`. Merge the following with your existing Helm values, preserving unrelated entries. Replace the placeholders and example URLs:

```yaml
commonEnv:
  - name: ENGINE_GITHUB_WEB_BASE_URL
    value: "https://<ghes-hostname>"
  - name: ENGINE_GITHUB_APP_ID
    value: "<app-id>"
  - name: ENGINE_GITHUB_APP_PUBLIC_LINK
    value: "<public-link-copied-from-github>"
  - name: ENGINE_GITHUB_APP_CLIENT_ID
    value: "<client-id>"
  - name: ENGINE_GITHUB_OAUTH_REDIRECT_URI
    value: "https://langsmith.example.com/api-host/v1/integrations/forge/github/callback"
  - name: ENGINE_GITHUB_APP_CLIENT_SECRET
    valueFrom:
      secretKeyRef:
        name: langsmith-engine-github
        key: client_secret
  - name: ENGINE_GITHUB_APP_PRIVATE_KEY
    valueFrom:
      secretKeyRef:
        name: langsmith-engine-github
        key: private_key
  - name: ENGINE_GITHUB_OAUTH_STATE_SECRET
    valueFrom:
      secretKeyRef:
        name: langsmith-engine-github
        key: oauth_state_secret
  - name: ENGINE_GITHUB_APP_WEBHOOK_SECRET
    valueFrom:
      secretKeyRef:
        name: langsmith-engine-github
        key: webhook_secret

hostBackend:
  enabled: true
```

Remove these variables from component-specific `extraEnv` lists, including `hostBackend.deployment.extraEnv`, to avoid duplicate definitions. The shared configuration supplies the same values to API and background workloads.

The chart's `config.hostname`, `config.frontendHostname` if used, and `config.basePath` must also describe the URL users open in their browser.

#### Private GHES deployments

If GHES uses private IP addresses or a private CA, include the applicable settings below before applying the values file.

**GHES on a private network**

For a GHES hostname that resolves to private IP addresses, configure private DNS and network routing from LangSmith and the sandbox hosts. Also set the following environment variables through the listed Helm values:

| Helm environment list | Variable | Value |
| - | - | - |
| `platformBackend.deployment.extraEnv` | `SSRF_ALLOW_PRIVATE_IPS_ENGINE` | `"true"` |
| `ingestQueue.deployment.extraEnv` | `SSRF_ALLOW_PRIVATE_IPS_ENGINE` | `"true"` |
| `sandboxes.sandboxHost.deployment.extraEnv` | `SSRF_ALLOW_PRIVATE_IPS_EGRESS` | `"true"` |

These settings allow the respective components to reach private addresses; they do not create DNS records or network routes. They affect more than this GitHub hostname. Retain network restrictions for the destinations your deployment actually needs, and keep protections for metadata, loopback, and Kubernetes-internal addresses enabled.

**GHES with a private certificate authority**

LangSmith services and sandbox hosts must trust the CA that signed your GHES certificate. Configuring trust only in your browser or inside a sandbox is insufficient.

Follow [Mount internal CAs for TLS](../../LangSmith%20setup/Self-hosted/Platform%20auth%20%26%20access%20control/Configure%20custom%20TLS%20certificates.md#mount-internal-cas-for-tls) to configure `config.customCa.secretName` and `config.customCa.secretKey`. Include your private CA and any public roots needed for other outbound connections in the bundle.

Also set `REQUESTS_CA_BUNDLE` in `hostBackend.deployment.extraEnv` to `/etc/ssl/certs/custom-ca-certificates.crt`, the path where the chart mounts that bundle. This setting is required for the GitHub integration in addition to the chart's TLS configuration.

Check that the bundle reaches the GitHub integration, platform API and workers, Engine execution workers, and sandbox hosts. Keep TLS verification enabled. The sandbox proxy's own CA is separate from the CA used to verify GHES.

#### Apply the configuration

Apply the complete values file through your normal deployment process, using a matching LangSmith image and chart release. For Helm upgrades, see [Upgrade a self-hosted deployment](../../LangSmith%20setup/Self-hosted/Manage%20an%20instance/Upgrade%20an%20installation.md).

Wait for the affected API and worker rollouts to finish before connecting repositories. Updating a Secret in place does not reload environment variables in running containers; restart affected workloads after credential changes.

### Verify webhook delivery

After the rollout, [connect a test repository and verify the connection](../Connect%20Engine%20to%20your%20repository.md#verify-the-connection). While creating and merging the test PR, check the App's webhook deliveries:

1. In the GitHub App's settings, open **Advanced** > **Recent deliveries**.
2. Confirm that **pull\_request** deliveries reach LangSmith successfully. LangSmith returns HTTP 202 when it accepts a valid signed delivery.

A successful webhook response alone does not prove the event matched an Engine issue. Complete the merge check in [Verify the connection](../Connect%20Engine%20to%20your%20repository.md#verify-the-connection).

### Troubleshoot setup

| Symptom | What to check |
| - | - |
| **GitHub is not configured** | Confirm the App ID, Client ID, Client secret, private key, state secret, and App's public link are set. Check the GitHub URL format and complete the rollout. This notice identifies missing configuration; it does not test whether credentials are valid. |
| GitHub is temporarily unavailable after authorization | Confirm that the Client secret and private key belong to the configured App ID and Client ID. Check GitHub connectivity and certificate trust, then restart **Connect GitHub**. |
| GitHub authorization opens on the wrong instance | Check `ENGINE_GITHUB_WEB_BASE_URL` in shared configuration and remove conflicting component overrides. |
| The callback returns HTML or 404 | Check the `/api-host` route, LangSmith base path, and exact authorization callback URL. |
| Installation does not return to LangSmith | Enable **Request user authorization (OAuth) during installation**. Check the exact authorization callback URL and confirm the Client ID and Client secret belong to this App. Then restart **Connect GitHub** in LangSmith. |
| Repositories appear, but cloning or pushing fails | Check sandbox-host DNS, routing, private-IP settings, certificate trust, and GitHub IP/push policies. |
| PR creation fails after a successful push | Check **Pull requests: Read and write**, draft PR availability, and the selected base branch. |
| A merge does not complete an issue | Check **Pull request** event subscription, webhook reachability, the matching webhook secret, and **Recent deliveries**. Redeliver failed events after correcting the cause. |

If GitHub cannot deliver webhooks, repository reads, fixes, and PR creation can still work. Webhook-driven PR linking and automatic issue completion after merges do not work. Restore delivery and redeliver missed events from GitHub's App settings.

For PRs created with an external coding assistant, preserve the issue reference from **Copy Fix Context** in the PR description. This reference lets Engine link the PR to the issue.

For missing organizations or repositories, see [Troubleshoot repository selection](../Connect%20Engine%20to%20your%20repository.md#troubleshoot-repository-selection).

When asking for help, include your LangSmith and Helm chart versions, GitHub environment and GHES version if applicable, App ownership type, and the step that fails. Do not include private keys, client secrets, webhook secrets, or access tokens.

### Change or rotate configuration

For a private-key rotation, add the new key in GitHub, update the deployment Secret, and restart affected workloads. Validate the connection before removing the old key. Follow the same overlap approach where GitHub supports multiple client secrets.

For webhook-secret rotation, coordinate the GitHub and LangSmith values. Deliveries during a mismatch fail signature verification. Review **Recent deliveries** and redeliver failed events after both sides use the new secret.

Replacing the App requires installing the replacement and reconnecting affected LangSmith workspaces. Plan for an interruption until repository access is restored. Transferring App ownership can also change where it can be installed and its public link; review GitHub's transfer behavior before making the change.

Do not change `ENGINE_GITHUB_WEB_BASE_URL` on an existing connected deployment as a migration procedure. Changing the URL does not migrate repository connections or existing PR references. Plan a migration with LangChain support before switching GitHub instances.

## See also

* [Connect Engine to your repository](../Connect%20Engine%20to%20your%20repository.md): Connect repositories once the GitHub App is configured.
* [Engine on self-hosted and BYOC](LangSmith%20Engine%20on%20Self-hosted%20and%20BYOC.md): Install Engine and choose how it runs its models.
* [Engine security](../LangSmith%20Engine%20security.md): How Engine handles your data and repository access.

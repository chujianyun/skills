# Connect Engine to your repository

> Connect your agent's GitHub repositories or GitLab projects to LangSmith Engine so it can read your source code when investigating issues and propose fixes as pull or merge requests.

Connecting your agent's code repository lets [LangSmith Engine](LangSmith%20Engine.md) read your source code when investigating traces, and propose fixes as pull requests on GitHub or merge requests on GitLab. A connection is optional for trace analysis. For what Engine gains from source access and the permissions it uses, see [Why connect a repository](LangSmith%20Engine.md#why-connect-a-repository).

Engine connects to repositories on GitHub and to projects on GitLab. Engine can use both for the same agent environment.

For GitHub:

* **LangSmith Cloud**: Use the LangChain-managed GitHub App on GitHub.com. Start with [Connect GitHub repositories](#connect-repositories).
* **Self-hosted LangSmith**: An operator first completes [GitHub configuration for self-hosted](Self-hosted%20and%20BYOC/Configure%20GitHub%20for%20Engine%20on%20self-hosted%20and%20BYOC.md) for your GitHub instance. Then, workspace users follow the same repository connection steps below.
* **BYOC**: An Organization Admin first registers a GitHub App and saves it in the LangSmith UI. See [Configure the App on BYOC](Self-hosted%20and%20BYOC/Configure%20GitHub%20for%20Engine%20on%20self-hosted%20and%20BYOC.md#configure-the-app-on-byoc). Then, workspace users follow the same repository connection steps below.

For GitLab, a workspace admin connects a GitLab account's access token in workspace settings. GitLab is available only on LangSmith Cloud. Start with [Connect GitLab](#connect-gitlab).

## GitHub

### Connect repositories

These steps apply to [LangSmith Cloud](../LangSmith%20setup/Cloud/Cloud%20%28SaaS%29.md), and to [self-hosted](../LangSmith%20setup/Self-hosted/Self-hosted%20LangSmith.md) and [BYOC](../LangSmith%20setup/BYOC/Bring%20Your%20Own%20Cloud%20%28BYOC%29.md) deployments with a configured GitHub App.

Enable [Engine](LangSmith%20Engine.md) for your tracing project or agent environment. You need permission to configure Engine in that project and to connect a GitHub integration in your LangSmith workspace. Ask a workspace administrator if those actions are unavailable.

On GitHub, you need permission to install the App on the repositories you want to connect, or access to an existing installation. Your GitHub organization or enterprise may require an administrator to approve the installation. Complete your organization's SSO sign-in when prompted.

> [!NOTE]
>
> For Enterprise Managed Users, connect organization-owned repositories. GitHub does not allow this App to be installed on a managed user's personal account. See [Enterprise Managed Users](Self-hosted%20and%20BYOC/Configure%20GitHub%20for%20Engine%20on%20self-hosted%20and%20BYOC.md#enterprise-managed-users) for the requirements on GitHub.com and `ghe.com`.

For fixes, the repository must permit Engine's branches and PRs. Review [Repository policies](#repository-policies) before testing a fix.

To connect GitHub repositories:

1. Open the tracing project or agent environment. On its **Engine** page, select **Configure Engine**.
2. Under **Code repository**, select **Connect GitHub**. If your workspace already has a connection, the repository picker appears instead.
3. In GitHub, authorize the App configured for your LangSmith deployment. Install it on the organization or account that owns your code and select the repositories it can access. If the App is already installed, LangSmith may ask you to select an existing installation.
4. Complete any GitHub approval prompts and return to LangSmith. Authorizing the App and installing it are separate steps: authorization identifies your GitHub account; installation grants the App access to repositories.
5. In the repository picker, search by account or repository name, select a repository, and click **Connect repository**.
6. Repeat for additional repositories. Each repository can have its own branch and subfolder.

You can also connect repositories while first setting up Engine, under **Connect your agent's code repository**.

#### Choose the branch and subfolder

For each connected repository:

* **Branch**: Select the branch Engine should read and use as the base for fixes. Leave it blank to use the repository's default branch.
* **Subfolder**: Optionally focus Engine on the part of the repository that contains your agent. This setting does not restrict the GitHub App's repository access.

Engine creates fix branches in the connected repository and opens pull requests against the selected base branch. In LangSmith v0.17, pull requests open as drafts. Review and merge those pull requests through your usual GitHub process. Engine does not merge them for you.

#### Connect another organization or account

One GitHub App can have an installation in each of several organizations or accounts. Repositories from those installations can be connected in the same agent environment.

In the repository picker, select **Install on another GitHub organization or repository...**. Complete the GitHub flow, return to LangSmith, and connect the additional repositories. On self-hosted LangSmith, the App's [ownership and visibility](Self-hosted%20and%20BYOC/Configure%20GitHub%20for%20Engine%20on%20self-hosted%20and%20BYOC.md#choose-who-owns-the-app) determine which accounts GitHub offers as installation targets.

On self-hosted LangSmith, all connected repositories must belong to the same GitHub instance. Connecting to a different LangSmith workspace also requires connecting the appropriate installation in that workspace.

#### Manage repository access

Installing an App on **Only select repositories** does not automatically include repositories created later. In the picker, select **Missing a repo? Manage repo access for ...** or **Manage app access →**. Add the repository in GitHub, save the installation settings, and reload the picker.

Removing a repository stops Engine from using it in that agent environment. It does not uninstall the GitHub App or remove its access in other agent environments. Manage the App installation in GitHub to revoke repository access.

#### Verify the connection

Use a test repository and an agent environment with representative traces. On self-hosted LangSmith, ask your operator to [verify webhook delivery](Self-hosted%20and%20BYOC/Configure%20GitHub%20for%20Engine%20on%20self-hosted%20and%20BYOC.md#verify-webhook-delivery) during this test.

To verify the connection:

1. Run an Engine analysis and confirm it can use the repository's source code.
2. Generate a fix for an issue, inspect its diff, and click **Open PR**. Confirm that **View PR** opens a PR on the expected GitHub instance, repository, and base branch.
3. Review and merge the test PR. Confirm the corresponding Engine issue becomes complete.

To create PRs automatically, enable **Open a pull request for every fix** in **Code repository** settings. In LangSmith v0.17, this setting is labeled **Open a draft pull request for every fix**.

#### Repository policies

Repositories must allow Engine to push fix branches. In LangSmith v0.17, they must also support draft PRs. Engine does not use a fork-based contribution workflow.

Engine's Git commits are unsigned. Rules that require signed commits on the fix branch can reject pushes. Branch-name rules, push restrictions, and GHES pre-receive hooks can also reject a fix. In LangSmith v0.17, fix branches use the `issues-agent/` prefix.

Review policies that apply to these branches and the App identity. Keep your normal review and merge requirements on the target branch. A requirement on the target branch may still need to be satisfied when a person merges; configuring the App does not bypass repository policy.

Engine does not fetch Git LFS file contents or initialize Git submodules.

#### Troubleshoot repository selection

| Symptom | What to check |
| - | - |
| GitHub is not configured, or the connection fails before GitHub opens | On self-hosted LangSmith, ask your operator to check the [deployment configuration](Self-hosted%20and%20BYOC/Configure%20GitHub%20for%20Engine%20on%20self-hosted%20and%20BYOC.md#configure-langsmith). |
| Your organization is not an installation target | Confirm your GitHub role, organization approval policy, and the App's visibility. A private App can only be installed on its owning account. |
| Your managed-user account is not an installation target | Use an organization-owned repository. Personal managed-user repositories cannot use this integration. |
| The App is installed, but LangSmith has no connection | Start **Connect GitHub** in LangSmith, including after an administrator approves installation or you install directly from GitHub. On self-hosted LangSmith, ask your operator to [check setup](Self-hosted%20and%20BYOC/Configure%20GitHub%20for%20Engine%20on%20self-hosted%20and%20BYOC.md#troubleshoot-setup) if authorization does not finish. |
| An installation or repository is missing | Check which GitHub account you authorized, the App's selected repositories, and whether the installation was connected to this LangSmith workspace. Complete your organization's SSO authorization when prompted. |
| Authorization succeeds, but the repository cannot be read | Check the App's repository access. On self-hosted LangSmith, also ask your operator to check [GitHub API and sandbox network access](Self-hosted%20and%20BYOC/Configure%20GitHub%20for%20Engine%20on%20self-hosted%20and%20BYOC.md#allow-network-access). Browser sign-in does not test those connections. |
| A fix cannot be pushed | Check rules that apply to the new fix branch, including signed-commit requirements, branch restrictions, and pre-receive hooks. See [Repository policies](#repository-policies). |

## GitLab

Engine connects to GitLab with one access token per workspace. The token belongs to a GitLab account, usually a service account, and that account's group and project memberships decide which projects Engine can read, push fix branches to, and open merge requests in. Unlike GitHub, GitLab has no app to install: you prepare the account in GitLab, then save its token in LangSmith.

> [!NOTE]
>
> GitLab is available only on [LangSmith Cloud](../LangSmith%20setup/Cloud/Cloud%20%28SaaS%29.md). It is not yet available on [self-hosted LangSmith](../LangSmith%20setup/Self-hosted/Self-hosted%20LangSmith.md) or [BYOC](../LangSmith%20setup/BYOC/Bring%20Your%20Own%20Cloud%20%28BYOC%29.md).

### Connect GitLab

Connecting GitLab requires the [Workspace Admin](../LangSmith%20setup/Govern/Users%20%26%20access%20control/Role-based%20access%20control.md#workspace-admin) role, or a custom role with the `workspaces:manage` permission. Other workspace members can view the connection and add the projects it reaches to Engine.

Your GitLab instance must meet these requirements:

* **Version**: GitLab.com, or a self-managed instance running GitLab 16.10 or later. LangSmith renews the token with GitLab's token self-rotation API, which earlier versions do not have.
* **URL**: HTTPS on port 443, with no path. GitLab installed under a relative URL root, such as `https://example.com/gitlab`, is not supported.
* **Network access**: LangSmith reaches GitLab over the internet, and refuses GitLab URLs that resolve to private IP addresses. The instance must also be able to deliver webhooks to LangSmith.

#### Prepare a service account

To prepare the account that Engine acts as:

1. Create a [GitLab service account](https://docs.gitlab.com/user/profile/service_accounts/) for LangSmith. On GitLab.com, a top-level group Owner creates it under the group's **Settings** > **Service accounts**. On GitLab Self-Managed, an administrator creates it by default. Service accounts are available on all GitLab tiers in GitLab 18.11 or later. On earlier Free-tier instances, use a dedicated user account instead.
2. Add the account to the groups or projects Engine should work in, with the **Maintainer** role. **Developer** is the minimum role, but with it LangSmith cannot register the [merge request webhook](#complete-issues-on-merge), so merging a fix does not complete its issue. Before choosing a role, review [Project policies](#project-policies).
3. Create a personal access token for the account with the `api` scope. For a service account, a group Owner or administrator creates the token from the **Service accounts** page.

Use the token only for LangSmith. When you save it, LangSmith rotates it, so the value you pasted stops working and LangSmith holds the only working copy.

#### Save the connection

To connect GitLab:

1. In LangSmith, go to **Settings** > **Integrations** > **GitLab**.
2. In **GitLab URL**, enter `https://gitlab.com` or the HTTPS URL of your instance.
3. In **Access token**, paste the token.
4. Click **Connect GitLab**.

LangSmith checks the token with GitLab and rotates it. The page shows the instance and when the token renews. Under **Connection health**, it shows details including:

* **Instance**: The GitLab URL and version.
* **Token status**: Whether GitLab accepts the token, for example **Accepted by GitLab**.
* **Scopes**: The token's scopes.
* **Expires**: When the current token expires.
* **Webhook URL**: The URL that GitLab delivers merge request webhooks to.
* **Last webhook delivery**: When LangSmith last received a webhook from GitLab.

Each workspace has one GitLab connection, to one GitLab instance.

#### Manage the access token

LangSmith stores the token encrypted and manages its lifetime:

* **Renewal**: LangSmith rotates the token halfway through its lifetime. Each rotation requests a one-year token. If the instance sets a shorter maximum lifetime, LangSmith uses the longest of 180, 90, 60, 30, 14, 7, or 2 days that the instance accepts. An instance that limits tokens to one day cannot be connected.
* **Edit connection**: To replace the token or switch instances, click **Edit connection**, enter the new values, and click **Save connection**. LangSmith revokes the replaced token. After a switch, the GitLab project paths Engine tracks refer to projects on the new instance, and fixes opened on the previous instance are hidden until you switch back.
* **Disconnect**: Click **Disconnect** to revoke the token. Engine loses access to GitLab projects immediately, including runs in progress. LangSmith's webhooks stay on your projects and work again when you reconnect, but merge requests merged in between do not complete their issues.

Deleting a workspace deletes its GitLab connection without revoking the token. The token expires on its own, or you can revoke it in GitLab.

### Add GitLab projects

Once a workspace admin connects GitLab, any user who can configure Engine in an agent environment can add the projects that the GitLab account can reach.

To add GitLab projects:

1. Open the agent environment. On its **Engine** page, select **Configure Engine**.
2. Under **Code repository**, search the repository picker by project name or path. Results are grouped by host, with GitHub repositories first and GitLab projects under a **GitLab** heading. The picker shows the first 20 matching GitLab projects, so refine the search to find others.
3. Select a project to add it.
4. (Optional) Set the project's **Branch** and **Subfolder**. See [Choose the branch and subfolder](#choose-the-branch-and-subfolder).
5. Repeat for additional projects.

You can also add projects while first setting up Engine, under **Connect your agent's code repository**.

If a project is missing from the picker, add the GitLab account to it with at least the **Developer** role. Until a workspace admin connects GitLab, the picker shows **Connect GitLab** to workspace admins and **Ask a workspace admin to connect GitLab.** to other users.

Engine can track GitHub repositories and GitLab projects together in the same agent environment. Each path can be tracked from only one host per agent environment. To track a GitLab project with the same path as a tracked GitHub repository, remove the GitHub repository first.

#### Open merge requests

On GitLab, Engine handles fixes the same way it does on GitHub, with merge requests in place of pull requests. Fix controls keep their names, such as **Open PR** and **View PR**.

* **Fix branches**: Engine pushes each fix to a new `langsmith-engine/<id>` branch in the project.
* **Author**: The connected GitLab account authors commits and merge requests, using its GitLab noreply email address.
* **Merge requests**: Click **Open PR** on an issue to open a merge request against the project's selected branch, or its default branch. Merge requests open ready for review, so pipelines that skip draft merge requests still run.
* **Automatic merge requests**: **Open a pull request for every fix** in **Code repository** settings also applies to GitLab projects.

Review and merge Engine's merge requests through your usual GitLab process. Engine does not merge them for you.

#### Complete issues on merge

LangSmith registers one merge request webhook on each GitLab project Engine tracks. When a merge request with an Engine fix merges, the webhook completes the fix's issue. When one closes without merging, Engine records the closure. Registering the webhook requires the **Maintainer** role on the project.

LangSmith creates or repairs the webhook after you connect GitLab, when you add a project, and each time Engine opens a merge request.

If the webhook cannot work, the project's row under **Code repository** shows a warning icon and a **GitLab settings** link. Hover the icon to see the reason. After you fix what prevents registration, no other step is needed. Engine still reads the project's code and opens merge requests in it.

GitLab delivers the webhook to the **Webhook URL** shown under **Connection health**, so your instance must be able to reach that URL.

#### Verify the GitLab connection

Use a test GitLab project and an agent environment with representative traces.

To verify the connection:

1. Under **Settings** > **Integrations** > **GitLab**, confirm that **Token status** shows **Accepted by GitLab**.
2. Add the test project and confirm that its row under **Code repository** shows no warning.
3. Run an Engine analysis and confirm it can use the project's source code.
4. Generate a fix for an issue, inspect its diff, and click **Open PR**. Confirm that **View PR** opens a merge request on the expected GitLab instance, project, and target branch.
5. Review and merge the test merge request. Confirm that the Engine issue becomes complete and that **Last webhook delivery** updates.

#### Project policies

Engine pushes only its own fix branches, but GitLab does not limit the token to them. The account's role and your branch protection decide what the token can change:

* **Developer**: GitLab's default branch protection prevents Developers from pushing to or merging into the default branch. LangSmith cannot register the merge request webhook.
* **Maintainer**: LangSmith can register the merge request webhook. Maintainers can push to and merge into protected branches that allow Maintainers, which includes the default branch under GitLab's default protection settings.

Add the account only to the projects Engine needs, and protect branches that Engine should not change. Keep your normal review and merge requirements on the target branch.

Push rules can reject Engine's pushes, for example rules that require signed commits, restrict branch names, or check commit author email addresses. As on GitHub, Engine's commits are unsigned, and Engine does not use forks, fetch Git LFS file contents, or initialize Git submodules.

#### GitLab limits

These Engine features are not available for GitLab projects:

* **Fix validation**: [Validating fixes with preview deployments](Validate%20fixes%20automatically.md) requires a GitHub repository.
* **Red Teaming**: [Red Teaming](Proactively%20identify%20issues%20with%20Red%20Teaming.md) runs use only GitHub repositories, with read-only credentials. A GitLab access token cannot be limited to read access, so Red Teaming never receives one.
* **Merge requests opened by other tools**: Engine does not link merge requests opened outside Engine, including by a [coding agent mentioned in Slack](LangSmith%20Engine%20notifications.md#mention-a-coding-agent).
* **Linear**: Engine does not track merge requests linked to a [Linear issue](Find%20and%20fix%20your%20agent%27s%20issues%20with%20LangSmith%20Engine.md#create-a-linear-issue).

#### Troubleshoot GitLab

| Symptom | What to check |
| - | - |
| **GitLab** does not appear under **Settings** > **Integrations** | Personal organizations cannot use Engine, so GitLab does not appear there. GitLab is available only on LangSmith Cloud. |
| Connecting fails with "GitLab rejected the access token" | The token is wrong, expired, or revoked. Create a new token. |
| Connecting fails with "the access token needs the api scope" | Create a token with the `api` scope. |
| Connecting fails with "LangSmith needs GitLab 16.10 or later" | Upgrade the GitLab instance. |
| Connecting fails with "Could not reach GitLab" | Check the URL. The instance must be reachable from the internet over HTTPS on port 443, at a public IP address. |
| Connecting fails with "the GitLab connection could not be saved" | GitLab rotated the token, but LangSmith could not store the new one, so the token you pasted no longer works. Create a new token and connect again. |
| The GitLab settings page shows **GitLab rejected the access token** | The token was revoked or expired, or a renewal did not complete. Create a new token, click **Edit connection**, and save it. |
| The GitLab settings page shows **Token renewal failed** | GitLab refused a scheduled renewal. The banner shows GitLab's reason. The current token keeps working until it expires, and LangSmith retries the renewal. |
| A project is missing from the picker | Check that the GitLab account has at least the **Developer** role on the project, and refine the search if the picker shows its first 20 matches. |
| A project row shows a warning icon, and its tooltip asks for the **Developer** role | Give the GitLab account at least the **Developer** role on the project. Engine runs skip the project until then. |
| A project row shows a warning icon, and its tooltip says merged fixes will not resolve their issues | The tooltip gives the reason, such as a missing **Maintainer** role, merge request events turned off, or GitLab unable to reach the **Webhook URL**. If GitLab disabled the webhook after failed deliveries, re-enable it in the project's webhook settings. See [Complete issues on merge](#complete-issues-on-merge). |
| Engine settings show **Engine can't access GitLab** | The workspace's GitLab connection has a problem. Click **Open GitLab settings** to see it. |
| A fix cannot be pushed | Check branch protection and push rules for the new fix branch. See [Project policies](#project-policies). |

## Self-hosted LangSmith

On self-hosted LangSmith, an operator registers a GitHub App and configures LangSmith before anyone can connect repositories. See [Configure GitHub for Engine on self-hosted](Self-hosted%20and%20BYOC/Configure%20GitHub%20for%20Engine%20on%20self-hosted%20and%20BYOC.md).

## BYOC

On a BYOC data plane, an Organization Admin registers a GitHub App and saves its credentials from **Configure Engine** in the LangSmith UI before anyone can connect repositories. See [Configure the App on BYOC](Self-hosted%20and%20BYOC/Configure%20GitHub%20for%20Engine%20on%20self-hosted%20and%20BYOC.md#configure-the-app-on-byoc).

## See also

* [Set up Engine](Set%20up%20LangSmith%20Engine.md): Turn on Engine for a tracing project and select its repositories.
* [Why connect a repository](LangSmith%20Engine.md#why-connect-a-repository): What Engine gains from source access, and the permissions it uses.
* [Configure GitHub for Engine on self-hosted and BYOC](Self-hosted%20and%20BYOC/Configure%20GitHub%20for%20Engine%20on%20self-hosted%20and%20BYOC.md): Register and configure the GitHub App on self-hosted LangSmith or a BYOC data plane.
* [Engine security](LangSmith%20Engine%20security.md): How Engine handles your data and repository access.

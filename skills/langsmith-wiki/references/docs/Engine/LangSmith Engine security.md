# LangSmith Engine security

> How LangSmith Engine handles your data, the GitHub, GitLab, and model subprocessor controls that govern its access, and its compliance posture.

[LangSmith Engine](LangSmith%20Engine.md) reviews the trace data already in LangSmith, surfaces and prioritizes issues, and opens pull requests with suggested fixes, proposed prompt changes, and evaluations.

Engine is opt-in, advisory, and never trains on your data, and it runs under LangSmith's SOC 2 Type II and ISO 27001 controls. This page describes how Engine handles your data, the controls that govern its GitHub, GitLab, and model access, and its compliance posture for Engine in LangSmith Cloud. For how Engine runs in a self-hosted deployment, see [Engine on self-hosted](Self-hosted%20and%20BYOC/LangSmith%20Engine%20on%20Self-hosted%20and%20BYOC.md).

Engine is delivered as part of LangSmith and inherits LangSmith's security and compliance posture, with additional controls covering the AI inference layer described in the following sections. Engine is never on by default and can only be enabled by an [Organization Admin](../LangSmith%20setup/Govern/Users%20%26%20access%20control/Role-based%20access%20control.md#organization-admin), for organizations on any plan. For LangSmith's platform-level controls, including data encryption and regional handling, see the [Regions FAQ](../LangSmith%20setup/Govern/Additional%20resources/FAQ/Regions%20FAQ.md) and the [LangChain Trust Center](https://trust.langchain.com/).

## What data Engine uses

In LangSmith Cloud, Engine operates on data you have already chosen to share with LangChain: the trace data you send to LangSmith and, separately, the GitHub repository content you grant through the LangChain-managed GitHub App (see [GitHub integration](#github-integration)), or the GitLab projects your connected GitLab account can reach (see [GitLab integration](#gitlab-integration)). Enabling Engine introduces no other customer data sources. The following table summarizes what Engine reads, where it lives, and what it enables.

| **Data source** | **What Engine reads** | **Storage and persistence** | **Enables** |
| - | - | - | - |
| LangSmith workspace content | Trace data and other workspace content you have stored in LangSmith, such as prompts and evaluators. | Within your LangSmith tenant. [Trace retention](../Monitor/Trace/Configuration%20%26%20troubleshooting/Usage%20and%20billing.md#data-retention) is 14 days (base) or up to 180 days (extended) for SaaS customers as of September 14, 2026, chosen per project. | Issue detection, prioritization, and evaluation proposals. |
| GitHub repository | Source code and repository context from the repositories you connect (see [GitHub integration](#github-integration)). | Processed inside an isolated, LangChain-managed sandbox for the duration of each analysis run, then discarded. | Pull request authoring with proposed code fixes. |
| GitLab project | Source code and project context from the projects the connected GitLab account can reach (see [GitLab integration](#gitlab-integration)). | Processed inside an isolated, LangChain-managed sandbox for the duration of each analysis run, then discarded. The access token is stored encrypted in LangSmith. | Merge request authoring with proposed code fixes. |
| Model provider (inference) | Only the content required for each analysis task. | Configured for zero data retention with each Engine model provider (see [Model subprocessors](#model-subprocessors)). | Engine reasoning and generation. |

> [!NOTE]
>
> Engine's read scope may expand over time. This page is updated to reflect material changes. Last reviewed September 16, 2026.

Trace content sent to Engine can include user messages, tool outputs, and PII, and this content is sent to model subprocessors under zero data retention for each analysis task. To remove sensitive fields before traces reach LangSmith, use [client-side masking](../Monitor/Trace/Configuration%20%26%20troubleshooting/Data%20%26%20privacy/Prevent%20logging%20of%20sensitive%20data%20in%20traces.md).

Engine outputs are advisory. It surfaces and tracks issues, proposes pull requests, and recommends dataset examples for offline evaluation. Your engineers and your branch-protection and review policies decide what ships.

## GitHub integration

In LangSmith Cloud, Engine connects to GitHub.com through a LangChain-managed GitHub App. Self-hosted deployments use an [operator-managed App for their GitHub environment](Self-hosted%20and%20BYOC/Configure%20GitHub%20for%20Engine%20on%20self-hosted%20and%20BYOC.md). [BYOC](../LangSmith%20setup/BYOC/Bring%20Your%20Own%20Cloud%20%28BYOC%29.md) deployments use an App you register and [configure in the LangSmith UI](Self-hosted%20and%20BYOC/Configure%20GitHub%20for%20Engine%20on%20self-hosted%20and%20BYOC.md#configure-the-app-on-byoc). For GitLab, see [GitLab integration](#gitlab-integration). Bitbucket and other version control providers are not yet supported.

The App is scoped to:

* **Read access** on the repositories you select at installation.
* **Write access** to open pull requests from new branches it creates. Pushes to existing branches are governed by your branch protection rules.

Access uses GitHub's standard App model: every action runs through a short-lived installation token that expires after one hour, cannot exceed the permissions granted at installation, and cannot reach repositories you did not select. Tokens are minted per analysis run rather than held as a standing credential.

Source code is read only by Engine's automated analysis and is not browsed by LangChain personnel in normal operation. For each run, the selected repository is cloned into an isolated, network-restricted sandbox, used only for that run, and deleted when the run completes (within an hour at most if a run is interrupted). Engine's own operational traces of the analysis are masked by default.

You can revoke Engine's access to GitHub at any time by uninstalling the App from your GitHub organization.

## GitLab integration

In LangSmith Cloud, Engine connects to GitLab.com or a self-managed GitLab instance with a personal access token that a workspace admin saves in LangSmith, usually for a dedicated [service account](Connect%20Engine%20to%20your%20repository.md#prepare-a-service-account). The token requires the `api` scope. Only users with the `workspaces:manage` permission can connect or disconnect GitLab.

The token acts as its GitLab account:

* **Reach**: Engine can access only the groups and projects the account is a member of. Engine needs at least the Developer role to read code, push fix branches, and open merge requests. LangSmith needs the Maintainer role to register merge request webhooks.
* **Write scope**: Unlike a GitHub App installation token, a GitLab access token cannot be narrowed to selected projects or to read-only access. Engine pushes only its own fix branches, but the account's role and your branch protection rules decide what the token can change. Add the account only to the projects Engine needs, and protect branches that Engine should not push to.

LangSmith takes custody of the token when it is saved. It rotates the token immediately, so the value the admin pasted stops working and LangSmith holds the only working copy, encrypted at rest. LangSmith renews the token halfway through each lifetime, for at most one year at a time, and revokes it when an admin disconnects GitLab. Deleting a workspace deletes its connection but does not revoke the token, which then expires on its own.

For each run, Engine clones the GitLab projects it tracks into the same isolated, network-restricted sandbox used for GitHub repositories. A proxy outside the sandbox adds the token only to Git requests for those projects, so code in the sandbox cannot read the token or use it for GitLab API calls. Red Teaming runs use read-only repository credentials. Because a GitLab access token cannot be limited to read access, Red Teaming runs do not receive it and do not use GitLab projects.

Each workspace's merge request webhook has its own URL and secret. LangSmith verifies the secret on every delivery, and a delivery can update only that workspace's issues.

Connecting and disconnecting GitLab are recorded in [audit logs](../LangSmith%20setup/Govern/Auditing/Audit%20logs.md) as `upsert_gitlab_connection` and `delete_gitlab_connection`.

You can revoke Engine's access to GitLab at any time by disconnecting GitLab under **Settings** > **Integrations** > **GitLab**, or by revoking the token or removing the account in GitLab.

## Model subprocessors

In LangSmith Cloud, Engine's model subprocessors (currently OpenAI, Anthropic, Fireworks, and Baseten) are configured for zero data retention and are prohibited under their agreements with LangChain from using customer data to train or fine-tune their models. The [LangChain Trust Center](https://trust.langchain.com/) publishes the authoritative subprocessor list.

In self-hosted deployments, each organization chooses how Engine runs its models:

* **LangSmith Intelligence (LSI):** Engine uses Amazon Bedrock through LSI, under the commitments on this page.
* **Your own model providers:** Engine calls Anthropic, OpenAI, Amazon Bedrock, Google Vertex AI, or Azure AI Foundry with your credentials. Those providers process Engine's requests under your agreements with them, and LangChain receives only usage metadata.

In [BYOC](../LangSmith%20setup/BYOC/Bring%20Your%20Own%20Cloud%20%28BYOC%29.md) deployments, Engine runs only on your own model providers.

See [Choose how Engine runs its models](Self-hosted%20and%20BYOC/LangSmith%20Engine%20on%20Self-hosted%20and%20BYOC.md#choose-how-engine-runs-its-models).

## Key security controls

In LangSmith Cloud, Engine adds the following controls on top of LangSmith's baseline:

* **Explicit opt-in**: Engine is never on by default and can only be enabled by an Organization Admin.
* **Advisory outputs, human at the helm**: Engine does not auto-merge, auto-deploy, or take destructive actions on your systems. Every proposed change is a pull request that follows your branch-protection, review, and merge policies. Proposed prompt changes are written to a separate proposal record in LangSmith and do not modify any prompt until an authorized user explicitly applies them. In both paths, a human decides what ships.
* **Zero data retention configured with each Engine model provider**: Prompts and completions are not persisted by the inference vendor beyond the request.
* **No use of customer data to train or fine-tune any model**: Each provider is bound by agreement not to use customer content for training.
* **Logical tenant isolation**: Engine's access to your data is scoped to your LangSmith tenant. Cross-tenant access is prevented by application-level controls, consistent with LangSmith Cloud's tenancy model. Each analysis run executes inside its own isolated sandbox.
* **Auditability**: Engine surfaces its work as GitHub pull requests or GitLab merge requests, with supporting context in the issue list on the [Engine tab](Find%20and%20fix%20your%20agent%27s%20issues%20with%20LangSmith%20Engine.md). Code changes flow through your branch-protection, review, and automated build controls, so your software development lifecycle remains the system of record for what ships.
* **Client-side PII scrubbing**: LangSmith's [client libraries](../Monitor/Trace/Configuration%20%26%20troubleshooting/Data%20%26%20privacy/Prevent%20logging%20of%20sensitive%20data%20in%20traces.md) can remove sensitive content from traces before they are sent to LangSmith. Recommended for customers handling regulated data.
* **Model selection managed by LangChain**: LangChain selects the specific model used for each Engine task across these subprocessors, and may change selections within that set without separate notification. Adding any new subprocessor follows the standard subprocessor-change notification process.
* **Revocation and deletion**: You can revoke GitHub access at any time by uninstalling the App, revoke GitLab access by disconnecting GitLab, and remove Engine's findings with **Delete all issues** in [Engine settings](Set%20up%20LangSmith%20Engine.md#pause-engine-or-delete-its-issues). Trace data follows your LangSmith [retention and purging](../LangSmith%20setup/Govern/Data%20%26%20compliance/Data%20purging%20for%20compliance.md) settings.

## Compliance posture

Engine operates under LangSmith's control environment, which is audited annually under SOC 2 Type II and certified to ISO 27001. Engine's model subprocessors are listed on the [LangChain Trust Center](https://trust.langchain.com/), which is the authoritative source for procurement and data protection impact assessments.

## Inherent AI risks and mitigations

The following risks are inherent to AI-assisted code generation. LangChain mitigates each in product, and your code-review workflow provides a second layer of defense.

* **Incorrect or hallucinated suggestions**: All Engine output flows through your normal pull-request review and automated checks before any code lands.
* **Prompt injection via trace content**: Trace data can include adversarial content reflected from external sources, for example, web-tool outputs. Any suggestion Engine produces from such traces still passes through human pull-request review before code lands. Treat traces from untrusted sources with care.
* **Out-of-scope decisions**: Engine reasons over traces and connected repositories only. Issues that depend on context Engine cannot see, for example, business-rule changes in a ticketing system, remain a human responsibility.

## See also

* [LangSmith Engine](LangSmith%20Engine.md)
* [Set up Engine](Set%20up%20LangSmith%20Engine.md)
* [Engine on self-hosted and BYOC](Self-hosted%20and%20BYOC/LangSmith%20Engine%20on%20Self-hosted%20and%20BYOC.md)
* [Engine notifications](LangSmith%20Engine%20notifications.md)
* [Prevent logging of sensitive data in traces](../Monitor/Trace/Configuration%20%26%20troubleshooting/Data%20%26%20privacy/Prevent%20logging%20of%20sensitive%20data%20in%20traces.md)
* [Data purging for compliance](../LangSmith%20setup/Govern/Data%20%26%20compliance/Data%20purging%20for%20compliance.md)
* [Audit logs](../LangSmith%20setup/Govern/Auditing/Audit%20logs.md)
* [Regions FAQ](../LangSmith%20setup/Govern/Additional%20resources/FAQ/Regions%20FAQ.md)
* [LangChain Trust Center](https://trust.langchain.com/)

## Contact

For security questions, contact [trust@langchain.dev](mailto:trust@langchain.dev).

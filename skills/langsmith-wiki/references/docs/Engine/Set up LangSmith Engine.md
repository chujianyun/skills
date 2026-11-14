# Set up LangSmith Engine

> Enable LangSmith Engine for your organization, turn it on for a tracing project, and configure what it analyzes.

Setting up [LangSmith Engine](LangSmith%20Engine.md) takes two steps. An [Organization Admin](../LangSmith%20setup/Govern/Users%20%26%20access%20control/Role-based%20access%20control.md#organization-admin) first enables Engine for the organization. Then any user whose [role](../LangSmith%20setup/Govern/Users%20%26%20access%20control/Role-based%20access%20control.md) can update tracing projects turns on Engine for each tracing project or agent environment. Once Engine is running, [configure it](#configure-engine) to focus on the issues and traces that matter to you.

> [!NOTE]
>
> On self-hosted LangSmith, an operator must enable Engine in the LangSmith Helm chart before either step is available. On [BYOC](../LangSmith%20setup/BYOC/Bring%20Your%20Own%20Cloud%20%28BYOC%29.md), an Organization Admin must also add model provider credentials before Engine runs. See [Engine on self-hosted and BYOC](Self-hosted%20and%20BYOC/LangSmith%20Engine%20on%20Self-hosted%20and%20BYOC.md).

## Enable Engine for your organization

> [!NOTE]
>
> You must be an [**Organization Admin**](../LangSmith%20setup/Govern/Users%20%26%20access%20control/Role-based%20access%20control.md#organization-admin) to enable Engine. To find your admins, open **Settings**, select **Members** under **Access and Security**, and look for members with the **Organization Admin** role.

**1. Open Engine settings**

In the [LangSmith console](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-engine-setup), click **Settings** in the bottom-left corner, then select **Engine** under **Engine**.

**2. Toggle Enable Engine**

Toggle **Enable Engine** on and acknowledge the AI features terms of use. The dialog displays the following in-product notice verbatim:

> LangSmith AI features, powered by LangChain-managed inference, bring intelligence to your observability workflow. With LangSmith AI enabled, your team can surface issues faster, run smarter evaluations, and build more reliable LLM applications. By enabling this feature, your organization's trace data will be processed using LangChain-managed LLM keys. Subject to our Terms of Service.

Once Engine is enabled, any user whose role can update tracing projects can set it up for a tracing project or agent environment. Roles with read-only access to projects cannot.

## Turn on Engine for a tracing project

**1. Open Engine and select a project**

In the [LangSmith console](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-engine-setup), select **Engine** in the UI sidebar. The project selector lists projects that are already configured. To set up a project that is not listed, click **+ Set up another project**, then choose it under **Choose a project to analyze**. The **Engine** tab in a tracing project is also available.

**2. Connect a code repository (optional)**

Connecting a repository is optional but recommended, because Engine finds better issues when it can read your source code. See [Why connect a repository](LangSmith%20Engine.md#why-connect-a-repository). Under **Connect your agent's code repository**, select the repositories Engine should use. Only repositories the GitHub App can access are shown. Click **Manage app access →** to update permissions. On LangSmith Cloud, GitLab projects appear once a workspace admin [connects GitLab](Connect%20Engine%20to%20your%20repository.md#connect-gitlab). For GitHub App setup and organization approval, see [Connect Engine to your repository](Connect%20Engine%20to%20your%20repository.md). To give Engine additional project context, select a repository in the **Context Hub repository** field.

Also set `revision_id` on your traces so Engine can match each trace to the commit that produced it. Engine then reasons from the code that ran, for example by comparing the commits shipped between two releases when a metric regresses. See [Record the code version on traces](../Monitor/Trace/Configuration%20%26%20troubleshooting/Data%20%26%20privacy/Add%20metadata%20and%20tags%20to%20traces.md#record-the-code-version-on-traces).

**3. Select preference categories (optional)**

Under **What matters most to you?**, select categories to prioritize for your review (for example, **Tool Call Failures** or **Latency**). Click **+ Add something specific** to describe a custom concern. See [Tell Engine what kinds of issues to focus on](#tell-engine-what-kinds-of-issues-to-focus-on).

**4. Choose an analysis level**

Under **Analysis level**, choose **Reduced**, **Standard** (the default), or **Expanded**. Higher levels analyze more traces and cost more. See [Set the analysis level](LangSmith%20Engine.md#set-the-analysis-level).

**5. Focus on specific traces (optional)**

Under **Focus on specific traces**, narrow Engine's attention to a subset of runs by run name or metadata. Leave it empty to analyze all traces. See [Tell Engine which traces to focus on](#tell-engine-which-traces-to-focus-on).

**6. Start analyzing**

Click **Start Analyzing**. The dialog may show an estimated monthly cost range based on your project's usage. Engine can take up to 20 minutes to analyze your project’s traces and begin making suggestions. While you wait, you can [set up notifications](LangSmith%20Engine%20notifications.md) to be alerted in Slack or via webhook when issues of different priority levels are found.

**7. Review the agent overview document**

Before surfacing issues, Engine generates an agent overview document describing your project's purpose, architecture, and key metrics based on your traces. Review and edit the document, then click **Accept & Continue** to proceed. If the overview is inaccurate, edit it before continuing, since Engine uses it as context for all analysis, so accuracy here affects the quality of detected issues.

You can change any of these choices later in [Configure Engine](#configure-engine). To connect GitHub or GitLab, see [Connect Engine to your repository](Connect%20Engine%20to%20your%20repository.md). To get alerted in Slack or through a webhook when Engine finds issues, see [Engine notifications](LangSmith%20Engine%20notifications.md).

## Configure Engine

On the **Engine** page, click the **Configure Engine**  (gear) icon at the top of the issue list to open the **Engine settings** panel. Use it to give Engine context on your agent, tell it what to focus on, and connect Linear. The panel also holds settings covered elsewhere:

* **Code repository** and **Context repository**: Connect or update the GitHub repositories and GitLab projects Engine reads when diagnosing issues. Each repository or project can have its own **Subfolder** and **Branch** (defaults to the repository default). A Context Hub repository lets Engine propose fixes to instructions, docs, and linked skills. See [Connect Engine to your repository](Connect%20Engine%20to%20your%20repository.md).
* **Notifications**: See [Engine notifications](LangSmith%20Engine%20notifications.md).
* **Agent Server**: Set the baseline Agent Server Engine replays issue traces against. To verify Engine's proposed fixes automatically, select **Verify fixes with preview Agent Servers**. See [Validate fixes automatically](Validate%20fixes%20automatically.md).
* **Analysis level**: See [Set the analysis level](LangSmith%20Engine.md#set-the-analysis-level).
* **Spend limit**: See [Set spend limits and monitor usage](LangSmith%20Engine.md#set-spend-limits-and-monitor-usage).
* **Pause** and **Delete all issues**: See [Pause Engine or delete its issues](#pause-engine-or-delete-its-issues).

### Give context on your agent

During setup, Engine generates an agent overview document describing your project's purpose, architecture, and key metrics. Engine uses it as context for all analysis, so its accuracy affects the quality of detected issues. Under **Agent overview**, edit the document to add any relevant context Engine cannot infer from your traces and to make sure it is accurate. The document's **User Preferences** section also collects what Engine has [learned from your actions on issues](LangSmith%20Engine.md#how-engine-learns-from-your-actions-on-issues), so you can review and correct those calibrations here.

### Tell Engine what kinds of issues to focus on

Under **Preferences**, list the areas Engine should focus on, prioritize, or ignore. Select category chips such as **Cost & Tokens**, **Latency**, or **Tool Call Failures**, or click **+ Add something specific** to describe a custom concern. Engine treats preferences as authoritative and folds them into the agent overview document. Changes take effect on the next scan.

### Tell Engine which traces to focus on

Focus Engine on the traces that matter to keep analysis precise and reduce wasted LSU spend. Use trace scope (the **Focus on specific traces** control) when a project mixes several agents or workloads and you want Engine to analyze only some of them. For example, if a project runs both a production chatbot and a nightly batch job, scope to `Run Name is chatbot` so Engine ignores the batch runs. By default, Engine analyzes all of a project's traces.

Set the scope in either of two places, using the same control:

* **Engine setup**: In the **Find and fix your agent's issues** panel, under **Focus on specific traces**.
* **Engine settings**: In the **Trace filters** section of the [**Engine settings**](#configure-engine) panel. Edits here save automatically.

Add scope conditions with the filter editor. You can add one condition of each kind, **up to two**:

* **Run Name**: Pick a run or agent name. The value field autocompletes from the run names in your project's recent traces.
* **Metadata**: Pick a metadata key, then a value. Both autocomplete from the metadata present on your project's recent runs.

To add a condition, choose its kind from the field selector, fill in the values, then click **Add**. Each condition appears as a chip, for example `Run Name is chatbot` or `env is prod`. Click the **×** on a chip to remove that condition.

> [!NOTE]
>
> **Scope limitation:** The scope filter only accepts run name and metadata conditions. You cannot scope Engine's scan by feedback key, evaluator name, or score threshold. To focus Engine on traces with a specific evaluator's low scores, describe that in your [preferences](#tell-engine-what-kinds-of-issues-to-focus-on) or [agent overview](#give-context-on-your-agent). Engine already factors in all feedback signals automatically. See [How Engine selects traces](LangSmith%20Engine.md#how-engine-selects-traces).

Scope determines which traces Engine analyzes to detect issues and build the agent overview document. Scope set during initial setup applies to Engine's first scan. Scope changed later in the [**Engine settings**](#configure-engine) panel does not re-run Engine immediately. It applies on the next scan.

### Connect to Linear

Under **Linear**, click **Connect**, select a team, optionally select a project for new issues, then click **Save changes**. Engine retains durable links to the issues it creates, but does not synchronize later edits from Linear. Deleting all Engine issues does not delete existing Linear tickets. See [Create a Linear issue](Find%20and%20fix%20your%20agent%27s%20issues%20with%20LangSmith%20Engine.md#create-a-linear-issue).

## Pause Engine or delete its issues

Engine scans your traces on a dynamic schedule tuned to balance cost and performance. To stop scanning a project without deleting its existing issues, click **Pause** in the [**Engine settings**](#configure-engine) panel. Click **Resume** to start scanning again.

Click **Delete all issues** in the same panel to permanently remove the project's issues and Engine settings. This cannot be undone.

To turn off Engine for the whole organization, an Organization Admin toggles **Enable Engine** off under **Settings** > **Engine**. This stops all automatic Engine runs and future Engine billing for the organization.

## See also

* [LangSmith Engine](LangSmith%20Engine.md): How Engine works, how it learns, and what it costs.
* [Find and fix issues](Find%20and%20fix%20your%20agent%27s%20issues%20with%20LangSmith%20Engine.md): Review the issues Engine detects and act on them.
* [Connect Engine to your repository](Connect%20Engine%20to%20your%20repository.md): Connect repositories so Engine can read your code and open pull requests.
* [Engine notifications](LangSmith%20Engine%20notifications.md): Get alerted in Slack, Jira, or a webhook when Engine finds issues.

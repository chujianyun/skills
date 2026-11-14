# Alerts in LangSmith

> [!NOTE]
>
> **Self-hosted version requirement**: Access to alerts requires Helm chart version **0.10.3** or later.

Effective observability in LLM applications requires proactive detection of failures, performance degradations, and regressions. LangSmith's alerts feature helps identify critical issues such as:

* API rate limit violations from model providers.
* Latency increases for your application.
* Application changes that affect feedback scores reflecting end-user experience.
* Unexpected cost spikes from LLM usage.

Alerts in LangSmith are scoped to one [trace container](../../Trace/Observability%20concepts.md#trace-containers), requiring separate configuration for each one you monitor. Which container that is depends on how your workspace is organized.

> [!NOTE]
>
> **Agent-based workspaces.** This section applies if your workspace organizes traces by [agent and environment](../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20Registry.md). To check, look at the control at the top left: it names your workspace. If it shows the LangSmith logo instead, and the sidebar has an **Application** section with an application picker, your workspace is project-based. Skip this section and read [Tracing projects](../../Trace/Observability%20concepts.md#tracing-projects).

An alert is scoped to one [environment](../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20environments.md#select-an-environment) of one [agent](../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20Registry.md#agent). Alerting on production behavior therefore does not require a filter that excludes test traffic, because the environment already excludes it.

> [!NOTE]
>
> **Project-based workspaces.** This section applies if your workspace organizes traces by [tracing project](../../Trace/Observability%20concepts.md#tracing-projects). To check, look at the control at the top left. In a project-based workspace, it shows the LangSmith logo, and the sidebar has an **Application** section with an application picker. If the control shows your workspace name instead, your workspace is agent-based. Skip this section and read [Agent Registry](../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20Registry.md).

An alert is scoped to one tracing project.

> [!TIP]
>
> Alerts can [route](#step-4-configure-notification-channel) to Slack, PagerDuty, Dynatrace, or any HTTP endpoint via webhook. The **Webhook** tab includes [example recipes](#example-recipes) for Microsoft Teams, email, Slack on self-hosted deployments, and Google Chat (which requires middleware).

Follow these steps to configure an alert.

## Step 1: Navigate to create alert

In the [UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-alerts), navigate to the tracing project you would like to configure alerts for, or to the agent environment in an agent-based workspace. Click the **Alerts** icon on the top right-hand corner of the page to view existing alerts for it and set up a new alert.

## Step 2: Select metric type

LangSmith provides threshold-based alerting on the following metrics:

| Metric Type | Description | Use Case |
| - | - | - |
| **Run Count** | Tracks the total number of [runs](../../Trace/Observability%20concepts.md#runs) over a time window. | Monitor whether a pipeline is producing runs at the expected volume and alert when it drops unexpectedly. |
| **Cost** | Tracks the total cost of runs over a time window. | Monitor LLM spending to alert when costs exceed expected thresholds. Requires [cost tracking](../../Trace/Configuration%20%26%20troubleshooting/Cost%20tracking.md) to be configured. |
| **Errors** | Tracks runs with an error status. Alert on total error count or error percent (rate of errored runs out of all runs). | Monitor for failures in an application, or alert when the error rate exceeds an acceptable threshold. |
| **Feedback Score** | Measures the average feedback score. | Track [feedback from end users](../../../Test/Annotation%20Queues/Feedback/Log%20user%20feedback%20using%20the%20SDK.md) or [online evaluation results](../Online%20evaluators/Set%20up%20LLM-as-a-judge%20online%20evaluators.md) to alert on regressions. |
| **Latency** | Measures average run execution time. | Tracks the latency of your application to alert on spikes and performance bottlenecks. |

Additionally, for **Errors** and **Latency**, you can use the filter builder to stack conditions on fields such as **Status**, **Run Type**, **Tag**, and **Error**. For example, you can scope an error alert to runs where **Status** is `error`, **Run Type** is `llm`, **Tag** is `support_agent`, and **Error** matches `RateLimitExceeded`.

Alert filters combine conditions with AND only. For the filter syntax that alert rules accept through the API, refer to [Alert filters](../../Debug/Viewing%20%26%20managing%20traces/Trace%20query%20syntax.md#alert-filters).

## Step 3: Define alert conditions

Alert conditions consist of several components:

* **Aggregation Method**: Average, Percentage, or Count.
* **Comparison Operator**: `>=`, `<=`, or exceeds threshold.
* **Threshold Value**: Numerical value triggering the alert.
* **Aggregation Window**: Time period for metric calculation (choose between 5 or 15 minutes).
* **Feedback Key** (Feedback Score alerts only): Specific feedback metric to monitor.

![Alert Condition Configuration](../../../../assets/images/dcf45e867f62-define-conditions.png)

**Example:** The configuration in the screenshot would generate an alert when more than 5% of runs within the past 5 minutes result in errors.

You can preview alert behavior over a historical time window to understand how many datapoints, and which ones, would have triggered an alert at a chosen threshold (indicated in red). For example, setting an average latency threshold of 60 seconds for a project lets you visualize potential alerts, as shown in the following screenshot.

![Alert Metrics](../../../../assets/images/8da355866e3b-alert-preview.png)

## Step 4: Configure notification channel

> [tab] Slack
>
> Send alert notifications directly to a Slack channel using LangSmith's native Slack integration.
>
> > [!NOTE]
> >
> > The native Slack notification type is available on LangSmith Cloud and on self-hosted deployments with a [configured Slack app](../../../LangSmith%20setup/Self-hosted/Connect%20external%20services/Connect%20self-hosted%20and%20BYOC%20LangSmith%20to%20Slack.md). If your self-hosted deployment does not support that connection, use the [webhook Slack recipe](#example-recipes) in the **Webhook** tab.
>
> **Prerequisites**
>
> * A Slack workspace connected to your LangSmith organization. If you have not connected one yet, LangSmith will prompt you to do so inline when you configure this notification type.
>
> ### 1. Configure the Slack notification
>
> 1. In the **Notification Settings** section of your alert setup, select **Slack**.
> 2. Click the channel selector. If no Slack workspace is linked yet, click **Connect Slack** and complete the OAuth flow to authorize the configured Slack app.
> 3. Select the workspace and channel from the dropdown. Click the refresh icon if the channel does not appear immediately.
> 4. Click **Save** to save the notification configuration.
>
> LangSmith joins the selected public channel when it first delivers a message, if needed. To post to a private channel, invite the configured Slack app to that channel in Slack first.
>
> ### 2. Test the integration
>
> Click **Send Test Notification** to verify that LangSmith can reach the channel. Check the channel for the test message.
>
> ### Notification format
>
> When an alert triggers, LangSmith posts a structured Slack message that includes:
>
> * **Headline**: The alert name and your LangSmith workspace name.
> * **Detail line**: The metric attribute, triggered value, comparison operator, configured threshold, aggregation method, and time window — for example: `Total Cost: $12.50 ≥ $5.00 · avg · 30 min`.
> * **Action buttons**: **View Alert** (links to the alert preview in LangSmith) and **View Runs** (links to the filtered runs that triggered the alert).

> [tab] PagerDuty
>
> Configure PagerDuty as a notification channel using PagerDuty's [Events API v2](https://developer.pagerduty.com/docs/events-api-v2-overview). This integration allows critical LLM application issues to trigger PagerDuty incidents, enabling rapid response through your established incident management workflow.
>
> **Prerequisites**
>
> * An active PagerDuty account with administrator access
> * Appropriate service-level permissions in PagerDuty
>
> If on a custom deployment of LangSmith, make sure there are no firewall settings blocking egress traffic from LangSmith services.
>
> ### 1. Create a Service in PagerDuty
>
> 1. Log in to your PagerDuty account
> 2. Navigate to **Services > Service Directory**
> 3. Click **+ New Service**
> 4. Complete the following fields:
>    * **Name**: Provide a descriptive name (e.g., "LangSmith Monitoring")
>    * **Description**: Add details about the monitored application
>    * **Escalation Policy**: Select the appropriate team escalation policy
>    * **Integration Type**: Select "Events API V2"
> 5. Click **Add Service** to create the service
>
> ### 2. Obtain integration key
>
> After creating the service, retrieve the Integration Key:
>
> 1. From the **Service Directory**, locate and click on your newly created service
> 2. Select the **Integrations** tab
> 3. Find the "Events API V2" integration
> 4. Copy the **Integration Key** (a 32-character alphanumeric string)
>
>    ![PagerDuty Integration Key Location](../../../../assets/images/f6007dceca5e-pager-duty.png)
>
> ### 3. Configure LangSmith alert with PagerDuty
>
> > [!NOTE]
> >
> > To receive the same alert again within an hour of it being triggered, you must resolve the active incident created by the alert in PagerDuty.
>
> ![PagerDuty Setup](../../../../assets/images/5ad74c00061d-pagerduty-setup.png)
>
> 1. In the notification section of your alert set-up in LangSmith, select **PagerDuty**
> 2. Click the key icon to save the Integration Key as a Workspace secret or select an existing Workspace secret. As a best practice, we recommend saving the Integration Key as a Workspace Secret rather than adding it directly. This will allow you to reuse the same key across alerts for a workspace.
> 3. Configure additional notification options:
>    * **Severity**: Maps to PagerDuty incident priority
> 4. Send a test alert by clicking **Send Test Alert**
> 5. Verify the incident is triggered by PagerDuty and contains relevant LangSmith alert information
>
> ### Troubleshooting
>
> If incidents are not being created in PagerDuty:
>
> * Verify the Integration Key is entered correctly in LangSmith
> * Ensure the PagerDuty service is active and not in maintenance mode
> * Check that your PagerDuty account has Events API v2 enabled
> * If an alert trigger appears to be missing in PagerDuty, check whether the expected trigger occurred within one hour of a previous trigger from the same alert rule, and whether the incident created by the previous alert is still open.
> * Review network connectivity if your LangSmith instance is behind a firewall
>
> ### Additional resources
>
> * [PagerDuty Events API v2 Documentation](https://developer.pagerduty.com/docs/events-api-v2/overview/)
> * [PagerDuty Integration Guide](https://support.pagerduty.com/docs/services-and-integrations)

> [tab] Dynatrace
>
> Configure Dynatrace as a notification channel using Dynatrace's [Events API v2](https://docs.dynatrace.com/docs/dynatrace-api/environment-api/events-v2/post-event). This integration sends LangSmith alert events to your Dynatrace environment, enabling correlation with your broader infrastructure monitoring.
>
> **Prerequisites**
>
> * An active Dynatrace environment (SaaS or Managed).
> * A Dynatrace API access token with the `events.ingest` scope.
>
> If you are working from a custom [deployment](../../../LangSmith%20setup/Self-hosted/Self-hosted%20LangSmith.md) of LangSmith, make sure there are no firewall settings blocking egress traffic from LangSmith services.
>
> ### 1. Create an API token in Dynatrace
>
> 1. Log in to your Dynatrace environment.
> 2. Navigate to **Access Tokens**.
> 3. Click **Generate new token**.
> 4. Provide a descriptive name (e.g., "LangSmith Alerts").
> 5. Under **Scopes**, search for and enable `events.ingest` (Ingest events).
> 6. Click **Generate token**.
> 7. Copy the generated token and store it securely. The token is only displayed once.
>
> ### 2. Obtain your Dynatrace environment URL
>
> Your Dynatrace environment URL follows this format:
>
> ```
> https://{your-environment-id}.live.dynatrace.com
> ```
>
> You can find your environment ID in the browser URL bar when logged in to Dynatrace.
>
> ### 3. Configure LangSmith alert with Dynatrace
>
> 1. In the **Notifications Settings** for your alert setup in LangSmith, select **Dynatrace**.
> 2. Enter your Dynatrace environment URL.
> 3. Click the key icon to save the API token as a workspace secret or select an existing workspace secret. As a best practice, save the API token as a workspace secret rather than adding it directly. This allows you to reuse the same token across alerts for a workspace.
> 4. Configure additional notification options:
>    * **Event Type**: Select the Dynatrace event type (e.g., `CUSTOM_ALERT`, `ERROR_EVENT`)
> 5. Send a test alert by clicking **Send Test Notification**.
> 6. Verify the event appears in your Dynatrace environment.
>
> ### Troubleshooting
>
> If events are not appearing in Dynatrace:
>
> * Verify the API token has the `events.ingest` scope and is not expired.
> * Ensure the environment URL is correct and includes your environment ID.
> * Confirm the `Authorization` header format uses `Api-Token` (not `Bearer`).
> * Check that your Dynatrace environment is active and accessible.
> * Review network connectivity if your LangSmith instance is behind a firewall.
>
> ### Additional resources
>
> * [Dynatrace Events API v2 Documentation](https://docs.dynatrace.com/docs/dynatrace-api/environment-api/events-v2/post-event)
> * [Dynatrace Access Tokens](https://docs.dynatrace.com/docs/manage/access-control/access-tokens)

> [tab] Webhook
>
> Webhooks enable integration with custom services and third-party platforms by sending HTTP POST requests when alert conditions are triggered. Use webhooks to forward alert data to ticketing systems, chat applications, or custom monitoring solutions.
>
> **Prerequisites**
>
> * An endpoint that can receive HTTP POST requests
> * Appropriate authentication credentials for your receiving service (if required)
>
> ### 1. Prepare your receiving endpoint
>
> Before configuring the webhook in LangSmith, ensure your receiving endpoint:
>
> * Accepts HTTP POST requests
> * Can process JSON payloads
> * Is accessible from external services
> * Has appropriate authentication mechanisms (if required)
>
> If on a custom deployment of LangSmith, make sure there are no firewall settings blocking egress traffic from LangSmith services.
>
> ### 2. Configure webhook parameters
>
> In the **Monitoring** section of the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-alerts) under the **Alerts** tab, click **+ Alert** to create a. new alert.
>
> In the **Notification Settings** section, complete the webhook configuration with the following parameters:
>
> **Required fields**
>
> * **URL**: The complete URL of your receiving endpoint
>   * Example: `https://api.example.com/incident-webhook`
>
> **Optional fields**
>
> * **Headers**: JSON key-value pairs sent with the webhook request
>   * Common headers include:
>     * `Authorization`: For authentication tokens
>     * `Content-Type`: Usually set to `application/json` (default)
>     * `X-Source`: To identify the source as LangSmith
>   * If no headers, use `{}`
> * **Request Body Template**: Customize the JSON payload sent to your endpoint
>   * Default: LangSmith sends the payload defined and the following additional key-value pairs appended to the payload:
>     * `project_name`: Name of the LangSmith project the alert is scoped to.
>
>     * `workspace_name`: Name of the LangSmith workspace.
>
>     * `alert_rule_id`: A UUID to identify the LangSmith alert. This can be used as a de-duplication key in the webhook service.
>
>     * `alert_rule_name`: The name of the alert rule.
>
>     * `alert_rule_description`: The description of the alert rule (empty string if none set).
>
>     * `alert_rule_type`: The type of alert (as of 04/01/2025 all alerts are of type `threshold`).
>
>     * `alert_rule_attribute`: The attribute associated with the alert rule - `error_count`, `feedback_score`, `latency`, or `cost`.
>
>     * `alert_rule_url`: A direct link to the alert rule in LangSmith.
>
>     * `runs_url`: A direct link to the runs that triggered the alert in LangSmith.
>
>     * `triggered_metric_value`: The value of the metric at the time the threshold was triggered.
>
>     * `triggered_threshold`: The threshold that triggered the alert.
>
>     * `timestamp`: The timestamp that triggered the alert.
>
> > [!NOTE]
> >
> > LangSmith does not perform template substitution on the request body. The auto-populated fields above are merged into the outgoing JSON as top-level keys, alongside the body you configure. Placeholder syntax like `{alert_rule_name}` is sent verbatim to the receiving service. It only resolves to a real value if the receiver itself can extract fields from the incoming JSON (for example, a Power Automate Workflow, an AWS Lambda, or a custom HTTP handler).
>
> ### 3. Test the webhook
>
> Click **Send Test Alert** to send the webhook notification to ensure the notification works as intended.
>
> ### Troubleshooting
>
> If webhook notifications are not being delivered:
>
> * Verify the webhook URL is correct and accessible
>
> * Ensure any authentication headers are properly formatted
>
> * Check that your receiving endpoint accepts POST requests
>
> * Examine your endpoint's logs for received but rejected requests
>
> * Verify your custom payload template is valid JSON format
>
> > [!WARNING]
> >
> > **Send Test Alert does not validate the downstream response.** The UI reports **your configuration is working correctly and the test notification was delivered** even if the receiving endpoint returned an error (for example, a 400 or 422 rejection). Always verify receipt on the receiver side, check your endpoint's logs or the target platform's message history, rather than relying solely on the LangSmith success message.
>
> ### Security considerations
>
> * Use HTTPS for your webhook endpoints
> * Implement authentication for your webhook endpoint
> * Consider adding a shared secret in your headers to verify webhook sources
> * Validate incoming webhook requests before processing them
>
> ### Example recipes
>
> > [accordion] Configure Slack notifications via webhook
> >
> > Here is an example for configuring LangSmith alerts to send notifications to Slack channels using the [`chat.postMessage`](https://api.slack.com/methods/chat.postMessage) API.
> >
> > **Prerequisites**
> >
> > * Access to a Slack workspace.
> > * A LangSmith tracing project, or an agent environment, to set up alerts.
> > * Permissions to create Slack applications.
> >
> > **Step 1: Create a Slack app**
> >
> > 1. Visit the [Slack API Applications page](https://api.slack.com/apps).
> > 2. Click **Create New App**.
> > 3. Select **From scratch**.
> > 4. Provide an **App Name** (e.g., "LangSmith Alerts").
> > 5. Select the workspace where you want to install the app.
> > 6. Click **Create App**.
> >
> > **Step 2: Configure bot permissions**
> >
> > 1. In the left sidebar of your Slack app configuration, click **OAuth & Permissions**.
> > 2. Scroll down to **Bot Token Scopes** under **Scopes** and click **Add an OAuth Scope**.
> > 3. Add the following scopes:
> >    * `chat:write` (Send messages as the app).
> >    * `chat:write.public` (Send messages to channels the app is not in).
> >    * `channels:read` (View basic channel information).
> >
> > **Step 3: Install the app to your workspace**
> >
> > 1. Scroll up to the top of the **OAuth & Permissions** page.
> > 2. Click **Install to Workspace**.
> > 3. Review the permissions and click **Allow**.
> > 4. Copy the **Bot User OAuth Token** that appears (begins with `xoxb-`).
> >
> > **Step 4: Add the bot to a Slack channel**
> >
> > Add the bot to the specific channel you want to receive alerts in. You can add a bot to a Slack channel by mentioning it in the message field (e.g., `@botname`).
> >
> > You also need the channel ID to configure the webhook alert in LangSmith. You can find the channel ID by opening channel details > About.
> >
> > **Step 5: Configure the webhook alert in LangSmith**
> >
> > 1. In LangSmith, navigate to your tracing project, or to your agent environment.
> > 2. Select **Alerts > Create Alert**.
> > 3. Define your alert metrics and conditions.
> > 4. In the notification section, select **Webhook**.
> > 5. Configure the webhook with the following settings:
> >
> > **Webhook URL**
> >
> > ```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > https://slack.com/api/chat.postMessage
> > ```
> >
> > **Headers**
> > \[!NOTE] Replace `xoxb-your-token-here` with your Bot's User OAuth Token
> >
> > ```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > {
> >   "Content-Type": "application/json",
> >   "Authorization": "Bearer xoxb-your-token-here"
> > }
> > ```
> >
> > **Request Body Template**
> > \[!NOTE] It is required to fill in the `{channel_id}` from the value found in Step 4. \
> > \
> > The remaining fields: `alert_name`, `project_name` and `project_url` optionally add additional context to the alert message. You can find your `project_url` in the browser's URL bar. Copy the portion up to but not including any query parameters.
> >
> > ```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > {
> >   "channel": "{channel_id}",
> >   "text": "{alert_name} triggered for {project_name}",
> >   "blocks": [
> >     {
> >       "type": "section",
> >       "text": {
> >         "type": "mrkdwn",
> >         "text": "🚨{alert_name} has been triggered"
> >       }
> >     },
> >     {
> >       "type": "section",
> >       "text": {
> >         "type": "mrkdwn",
> >         "text": "Please check the following link for more information:"
> >       }
> >     },
> >     {
> >       "type": "section",
> >       "text": {
> >         "type": "mrkdwn",
> >         "text": "<{project-url}|View in LangSmith>"
> >       }
> >     }
> >   ]
> > }
> > ```
> >
> > 6. Click **Save** to activate the webhook configuration.
> >
> > **Step 6: Test the integration**
> >
> > 1. In the LangSmith alert configuration, click **Test Alert**.
> > 2. Check your specified Slack channel for the test notification.
> > 3. Verify that the message contains the expected alert information.
> >
> > **(Optional) Step 7: Link to the alert preview in the request body**
> >
> > After creating an alert, you can optionally link to its preview in the webhook's request body.
> >
> > ![Alert Preview Pane](../../../../assets/images/a78aa60febb8-alert-preview-pane.png)
> >
> > To configure this:
> >
> > 1. Save your alert.
> > 2. Find your saved alert in the alerts table and click it.
> > 3. Copy the displayed URL.
> > 4. Click "Edit Alert".
> > 5. Replace the existing project URL with the copied alert preview URL.
>
> > [accordion] Configure Microsoft Teams notifications via webhook
> >
> > Here is an example for configuring LangSmith alerts to send notifications to a Microsoft Teams channel using the [Workflows app](https://support.microsoft.com/en-us/office/create-incoming-webhooks-with-workflows-for-microsoft-teams-8ae491c7-0394-4861-ba59-055e33f75498) (Power Automate). This approach is recommended because it extracts fields from the incoming JSON within the flow, so the auto-populated LangSmith alert fields render correctly in the Teams message.
> >
> > > [!NOTE]
> > >
> > > Microsoft's legacy Office 365 Incoming Webhook connectors are being retired. Use the Workflows app for new integrations.
> >
> > **Prerequisites**
> >
> > * Access to a Microsoft Teams workspace with permissions to add Workflows.
> > * A LangSmith tracing project, or an agent environment, to set up alerts.
> >
> > **Step 1: Create a Workflow in Teams**
> >
> > 1. In Microsoft Teams, navigate to the channel where you want to receive alerts.
> > 2. Click the **...** (More options) menu next to the channel name.
> > 3. Select **Workflows**.
> > 4. Search for and select the **Post to a channel when a webhook request is received** template.
> > 5. Sign in to confirm the connections, then click **Next**.
> > 6. Confirm the team and channel where alerts should be posted, then click **Add workflow**.
> > 7. Copy the generated **HTTP POST URL**—use this in LangSmith.
> >
> > **Step 2: Customize the message in Power Automate (optional)**
> >
> > The default workflow posts the raw JSON body as a card. To format alert details, edit the flow in Power Automate:
> >
> > 1. Open the [Power Automate portal](https://make.powerautomate.com) and edit the workflow you created.
> > 2. Click the **Post card in a chat or channel** action.
> > 3. In the **Adaptive Card** field, reference incoming fields using `triggerOutputs()?['body/alert_rule_name']`, `triggerOutputs()?['body/project_name']`, `triggerOutputs()?['body/triggered_metric_value']`, `triggerOutputs()?['body/triggered_threshold']`, `triggerOutputs()?['body/timestamp']`, and `triggerOutputs()?['body/alert_rule_url']`.
> > 4. Save the flow.
> >
> > **Step 3: Configure the webhook alert in LangSmith**
> >
> > 1. In LangSmith, navigate to your tracing project, or to your agent environment.
> > 2. Select **Alerts > Create Alert**.
> > 3. Define your alert metrics and conditions.
> > 4. In the notification section, select **Webhook**.
> > 5. Configure the webhook with the following settings:
> >
> > **Webhook URL**
> >
> > Paste the HTTP POST URL from your Teams Workflow:
> >
> > ```
> > https://prod-XX.westus.logic.azure.com:443/workflows/.../triggers/manual/paths/invoke?...
> > ```
> >
> > **Headers**
> >
> > ```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > {
> >   "Content-Type": "application/json"
> > }
> > ```
> >
> > **Request Body Template**
> >
> > LangSmith automatically merges the auto-populated alert fields (`alert_rule_name`, `project_name`, `triggered_metric_value`, `triggered_threshold`, `timestamp`, `alert_rule_url`, and others) into the request body as top-level JSON keys. Power Automate reads these fields directly from the incoming payload, so an empty body is sufficient:
> >
> > ```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > {}
> > ```
> >
> > 6. Click **Save** to activate the webhook configuration.
> >
> > **Step 4: Test the integration**
> >
> > 1. In the LangSmith alert configuration, click **Send Test Alert**.
> > 2. Check your specified Teams channel for the test notification.
> > 3. Verify that the card contains the expected alert information.
> >
> > **Reference implementation**
> >
> > For a working example that translates LangSmith webhook payloads (threshold alerts, run rules, and generic events) into formatted Teams Adaptive Cards, see the [langsmith-teams-webhook](https://github.com/langchain-samples/langsmith-teams-webhook) sample repo. The sample runs as a small Python service in front of a Teams Workflow URL, which avoids customizing the Power Automate flow itself.
>
> > [accordion] Configure email notifications via webhook
> >
> > Here is an example for configuring LangSmith alerts to send email notifications using [SendGrid's Mail Send API](https://docs.sendgrid.com/api-reference/mail-send/mail-send). You can use any transactional email provider that exposes an HTTP API (e.g., Mailgun, Amazon SES, Postmark).
> >
> > **Prerequisites**
> >
> > * A SendGrid account with a verified sender identity.
> > * A SendGrid API key with **Mail Send** permissions.
> > * A LangSmith tracing project, or an agent environment, to set up alerts.
> >
> > **Step 1: Create a SendGrid API key**
> >
> > 1. Log in to your [SendGrid dashboard](https://app.sendgrid.com).
> > 2. Navigate to **Settings > API Keys**.
> > 3. Click **Create API Key**.
> > 4. Choose **Restricted Access** and enable **Mail Send > Full Access**.
> > 5. Click **Create & View**, copy the key, and store it securely.
> >
> > **Step 2: Verify your sender email**
> >
> > 1. In SendGrid, navigate to **Settings > Sender Authentication**.
> > 2. Complete either **Domain Authentication** (recommended) or **Single Sender Verification** for the address you want to send from.
> >
> > **Step 3: Configure the webhook alert in LangSmith**
> >
> > 1. In LangSmith, navigate to your tracing project, or to your agent environment.
> > 2. Select **Alerts > Create Alert**.
> > 3. Define your alert metrics and conditions.
> > 4. In the notification section, select **Webhook**.
> > 5. Configure the webhook with the following settings:
> >
> > **Webhook URL**
> >
> > ```
> > https://api.sendgrid.com/v3/mail/send
> > ```
> >
> > **Headers**
> >
> > > [!NOTE]
> > >
> > > Replace `SG.your-api-key-here` with your SendGrid API key.
> >
> > ```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > {
> >   "Content-Type": "application/json",
> >   "Authorization": "Bearer SG.your-api-key-here"
> > }
> > ```
> >
> > **Request Body Template**
> >
> > > [!NOTE]
> > >
> > > Replace `alerts@your-company.com` with your verified sender address and `oncall@your-company.com` with the recipient address. SendGrid does not extract fields from arbitrary top-level JSON keys, so this example uses a fixed subject and body. To include alert-specific values in the email, route the LangSmith webhook through a middleware (such as a Power Automate flow, AWS Lambda, or Zapier webhook) that reads the incoming payload and renders the SendGrid request.
> >
> > ```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > {
> >   "personalizations": [
> >     {
> >       "to": [
> >         {
> >           "email": "oncall@your-company.com"
> >         }
> >       ],
> >       "subject": "LangSmith alert triggered"
> >     }
> >   ],
> >   "from": {
> >     "email": "alerts@your-company.com",
> >     "name": "LangSmith Alerts"
> >   },
> >   "content": [
> >     {
> >       "type": "text/plain",
> >       "value": "A LangSmith alert was triggered. Open your LangSmith workspace to view the alert details, including the project, metric value, threshold, and timestamp."
> >     }
> >   ]
> > }
> > ```
> >
> > 6. Click **Save** to activate the webhook configuration.
> >
> > **Step 4: Test the integration**
> >
> > 1. In the LangSmith alert configuration, click **Send Test Alert**.
> > 2. Check the recipient inbox for the test notification.
> > 3. Verify the email contains the expected alert information.
> >
> > **Using other email providers**
> >
> > The same pattern works with other transactional email APIs that accept static authentication headers. Change the **Webhook URL** and **Headers** to match your provider:
> >
> > | Provider | Webhook URL | Auth header format |
> > | - | - | - |
> > | Mailgun | `https://api.mailgun.net/v3/{your-domain}/messages` | `Authorization: Basic <base64(api:<key>)>` |
> > | Postmark | `https://api.postmarkapp.com/email` | `X-Postmark-Server-Token: <token>` |
> >
> > Adjust the **Request Body Template** to match each provider's expected payload format. Amazon SES is not directly compatible because the SES API requires per-request AWS SigV4 signing, which cannot be expressed as a static header. To use SES, route through a middleware (for example, a Lambda function with an HTTP trigger).
>
> > [accordion] Configure Google Chat notifications via webhook (requires middleware)
> >
> > Google Chat's incoming webhook API (`spaces.messages.create`) only accepts the `text` field at the top level. Because LangSmith merges all 12 alert metadata keys into the request body as top-level fields, Google Chat rejects every request with a 400 error:
> >
> > ```
> > Invalid JSON payload received. Unknown name "project_name" at 'message': Cannot find field.
> > ```
> >
> > There is no Request Body Template that avoids this, even a minimal body such as `{"text": "hello", "project_name": "x"}` will fail. **A translation layer (middleware) is required**, similar to the Amazon SES note in the [email recipe](#configure-email-notifications-via-webhook).
> >
> > **Option A: Cloud Run or Cloud Functions middleware (recommended)**
> >
> > This approach uses a small HTTP handler that receives the LangSmith webhook, extracts the relevant fields, and forwards a clean `{"text": "..."}` payload to a Google Chat space webhook URL.
> >
> > **Prerequisites**
> >
> > * A Google Chat space with an incoming webhook configured. In Google Chat, open the space, then go to **Apps & integrations** > **Add webhooks**, create a webhook, and copy the URL.
> > * A Google Cloud project with Cloud Run or Cloud Functions enabled, or equivalent hosting.
> >
> > **Step 1: Deploy the handler**
> >
> > Deploy the following Python function as a Cloud Run service or Cloud Function:
> >
> > ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import json
> > import os
> > import re
> > import urllib.request
> > from urllib.parse import urlparse
> >
> > ALLOWED_LINK_HOSTS = {"smith.langchain.com"}
> >
> > def build_text(payload):
> >     def safe(v):
> >         # Strip angle brackets to prevent <url|label> link injection
> >         return re.sub(r"[<>]", "", str(v if v is not None else ""))
> >
> >     parsed = urlparse(str(payload.get("runs_url") or ""))
> >     trusted = parsed.scheme == "https" and parsed.hostname in ALLOWED_LINK_HOSTS
> >     return (
> >         f"*{safe(payload.get('alert_rule_name'))}* triggered for "
> >         f"`{safe(payload.get('project_name'))}`\n"
> >         f"{safe(payload.get('alert_rule_attribute'))}: "
> >         f"{safe(payload.get('triggered_metric_value'))} "
> >         f"(threshold {safe(payload.get('triggered_threshold'))})"
> >         + (f"\n<{parsed.geturl()}|View runs>" if trusted else "")
> >     )
> >
> > def handler(request):
> >     if request.headers.get("X-Webhook-Secret") != os.environ["LANGSMITH_SHARED_SECRET"]:
> >         return ("forbidden", 403)
> >     payload = request.get_json(silent=True) or {}
> >     urllib.request.urlopen(
> >         urllib.request.Request(
> >             os.environ["GCHAT_WEBHOOK_URL"],
> >             data=json.dumps({"text": build_text(payload)}).encode(),
> >             headers={"Content-Type": "application/json"},
> >             method="POST",
> >         ),
> >         timeout=10,
> >     )
> >     return ("ok", 200)
> > ```
> >
> > Set the following environment variables for the deployed function:
> >
> > * `GCHAT_WEBHOOK_URL`: The Google Chat space webhook URL.
> > * `LANGSMITH_SHARED_SECRET`: A secret string you choose (used to authenticate incoming requests from LangSmith).
> >
> > **Step 2: Configure the webhook alert in LangSmith**
> >
> > Point the LangSmith webhook at your deployed handler's URL.
> >
> > **Webhook URL**
> >
> > ```
> > https://<your-cloud-run-service-url>/
> > ```
> >
> > **Headers**
> >
> > ```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > {
> >   "Content-Type": "application/json",
> >   "X-Webhook-Secret": "<your-shared-secret>"
> > }
> > ```
> >
> > **Request Body Template**
> >
> > ```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > {}
> > ```
> >
> > The metadata fields (`alert_rule_name`, `project_name`, `runs_url`, etc.) are merged into the body by LangSmith regardless of what you put here, so an empty body is sufficient.
> >
> > > [!NOTE]
> > >
> > > Do not strip `*` or `_` from alert field values in your handler. These characters are also used in Google Chat's basic text formatting, but they appear in LangSmith identifiers (such as `run_count`). Stripping them will corrupt field names in the message.
> >
> > > [!NOTE]
> > >
> > > Google Chat enforces a write rate limit of **1 message per second per space**, shared across all webhooks writing to that space. If you have multiple LangSmith alerts routing to the same space and they fire simultaneously, some messages may be dropped.
> >
> > **Option B: Google Apps Script (no infrastructure required)**
> >
> > Google Apps Script can serve as lightweight middleware without deploying any cloud infrastructure.
> >
> > Create a new Apps Script project at [script.google.com](https://script.google.com), paste the following, and deploy it as a web app (execute as yourself, access to anyone):
> >
> > ```javascript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > function doPost(e) {
> >   var payload = JSON.parse(e.postData.contents);
> >   var secret = e.parameter.secret; // shared secret passed as query param
> >   if (secret !== PropertiesService.getScriptProperties().getProperty("LANGSMITH_SHARED_SECRET")) {
> >     return ContentService.createTextOutput("forbidden").setMimeType(ContentService.MimeType.TEXT);
> >   }
> >   var text =
> >     "*" + (payload.alert_rule_name || "") + "* triggered for `" + (payload.project_name || "") + "`\n" +
> >     (payload.alert_rule_attribute || "") + ": " + (payload.triggered_metric_value || "") +
> >     " (threshold " + (payload.triggered_threshold || "") + ")";
> >   UrlFetchApp.fetch(PropertiesService.getScriptProperties().getProperty("GCHAT_WEBHOOK_URL"), {
> >     method: "post",
> >     contentType: "application/json",
> >     payload: JSON.stringify({ text: text }),
> >   });
> >   return ContentService.createTextOutput("ok").setMimeType(ContentService.MimeType.TEXT);
> > }
> > ```
> >
> > Set `GCHAT_WEBHOOK_URL` and `LANGSMITH_SHARED_SECRET` in **Project Settings > Script Properties**.
> >
> > > [!WARNING]
> > >
> > > Apps Script web apps cannot read custom HTTP request headers, so the shared secret must be passed as a **query string parameter** (`?secret=...`) rather than a header. Include it in the LangSmith webhook URL rather than the Headers field.
>
> ### Additional resources
>
> * [Slack chat.postMessage API Documentation](https://api.slack.com/methods/chat.postMessage)
> * [Slack Block Kit Builder](https://app.slack.com/block-kit-builder/)
> * [Create incoming webhooks with Workflows for Microsoft Teams](https://support.microsoft.com/en-us/office/create-incoming-webhooks-with-workflows-for-microsoft-teams-8ae491c7-0394-4861-ba59-055e33f75498)
> * [Power Automate documentation](https://learn.microsoft.com/en-us/power-automate/)
> * [langsmith-teams-webhook sample repo](https://github.com/langchain-samples/langsmith-teams-webhook)
> * [SendGrid Mail Send API Documentation](https://docs.sendgrid.com/api-reference/mail-send/mail-send)
> * [Google Chat incoming webhooks](https://developers.google.com/chat/how-tos/webhooks)

## Best practices

* Adjust sensitivity based on application criticality
* Start with broader thresholds and refine based on observed patterns
* Ensure alert routing reaches appropriate on-call personnel

# Connect self-hosted and BYOC LangSmith to Slack

> Configure your own Slack app for Engine and alert notifications on self-hosted LangSmith or a BYOC data plane.

LangSmith sends [Engine notifications](../../../Engine/LangSmith%20Engine%20notifications.md) and [alert notifications](../../../Monitor/Observe/Monitoring%20%26%20alerting/Alerts%20in%20LangSmith.md) to Slack through a Slack app that you create. Complete this setup once per self-hosted installation or BYOC data plane. Users then [connect a Slack workspace](#connect-a-slack-workspace) with that app, without supplying app credentials themselves.

* **BYOC**: An Organization Admin saves the app's credentials in the LangSmith UI. See [Create your Slack app on BYOC](#create-your-slack-app-on-byoc).
* **Self-hosted**: An operator configures the app's credentials in the deployment. See [Create your Slack app on self-hosted](#create-your-slack-app-on-self-hosted).

## Create your Slack app on BYOC

On a BYOC data plane, you create the Slack app and save its credentials in your organization settings. You do not set environment variables or Helm values. The app and its workspace connections apply only to the selected data plane. Other data planes and LangSmith Cloud are unaffected.

Configuring the app requires the `organization:manage` permission in the organization that owns the data plane.

To configure the app:

1. In LangSmith, go to **Settings** > **General Settings** > **Slack**, and select your data plane.
2. Click **Configure Slack App**. The **Set up Slack App** dialog opens.
3. Check the **Callback URL**. It defaults to `https://<data-plane-host>/v1/platform/slack/callback`. If your data plane uses a custom ingress, update the URL before you copy the manifest. The URL must use HTTPS and have no query string or fragment.
4. Click **Copy Slack App manifest**, then click **Create App in Slack**. In Slack, select **Create New App** > **From a manifest**, paste the manifest into the **JSON** tab, and create and install the app. The manifest already contains your callback URL.
5. In the new Slack app, open **Basic Information** > **App Credentials**. Copy the **Client ID** and **Client Secret** into the dialog, then save. Use the Client ID, not the App ID or Signing Secret.

LangSmith stores the credentials encrypted and does not display them again. To change them later, click **Edit or replace Slack App**. To remove them, click **Delete configuration**.

After you save the app, [connect a Slack workspace](#connect-a-slack-workspace). Connecting a workspace requires the `organization:integrations:manage` permission.

## Create your Slack app on self-hosted

On self-hosted LangSmith, your operator creates the Slack app and configures it in the deployment. The operator is the person who manages your LangSmith deployment. The deployment exchanges OAuth codes and sends notifications directly to Slack. LangSmith stores the app credentials and encrypted workspace bot tokens in your deployment.

If Slack is not configured on your instance, contact your operator. This notice appears in organization settings and in the **Slack** tab under each Engine project's **Notifications** settings. The operator follows the setup instructions below.

> [!NOTE]
>
> This connection requires LangSmith self-hosted v0.17 or later.

Before starting, make sure you have:

* **Deployment access:** Permission to configure and restart your LangSmith platform backend. For Kubernetes, access to the namespace where LangSmith runs.
* **Slack access:** Permission to create and install an app in the Slack workspace that receives notifications. Obtain administrator approval if your workspace restricts app installation.
* **LangSmith access:** The `organization:manage` permission to connect or disconnect a Slack workspace. An organization administrator can complete this step after the operator configures the deployment.
* **Network access:** Backend HTTPS access to Slack and browser access to your deployment's HTTPS callback. See [Allow network access](#allow-network-access).

Your operator creates one Slack app for the deployment. An [app manifest](https://docs.slack.dev/reference/app-manifest/) is a JSON configuration that creates the bot and sets its permissions. Users reuse this app when connecting a workspace; they do not create an app for each user or project.

To create the app:

1. Copy the JSON below and replace the URL in `oauth_config.redirect_urls`. For the standard ingress, append `/api/v1/platform/slack/callback` to the URL you use to open LangSmith. For example, `https://langsmith.example.com` becomes `https://langsmith.example.com/api/v1/platform/slack/callback`. If LangSmith runs at `https://langsmith.example.com/langsmith`, use `https://langsmith.example.com/langsmith/api/v1/platform/slack/callback`. For a custom ingress or separate API host, use the HTTPS URL that reaches your deployment's Slack callback.
2. Open [Your Apps](https://api.slack.com/apps) and select **Create New App**. Choose **From a manifest**, then click **Continue**.
3. Select the **JSON** tab, paste your edited manifest, and choose your Slack workspace. Click **Next**.
4. Review the five permissions and click **Create and Install**. Complete any Slack authorization or administrator approval prompts.
5. Open the new app's **Basic Information** > **App Credentials**. Copy the **Client ID** and **Client Secret**, using **Show** to reveal the secret. Store them in your deployment's secret manager. Use the Client ID, not the App ID or Signing Secret. You do not send these credentials to LangChain.

```json
{
  "display_information": {
    "name": "LangSmith Notifications",
    "description": "Engine and alert notifications from your LangSmith deployment"
  },
  "features": {
    "bot_user": {
      "display_name": "LangSmith Notifications",
      "always_online": false
    }
  },
  "oauth_config": {
    "redirect_urls": [
      "https://langsmith.example.com/api/v1/platform/slack/callback"
    ],
    "scopes": {
      "bot": [
        "chat:write",
        "channels:read",
        "channels:join",
        "groups:read",
        "reactions:write"
      ]
    }
  },
  "settings": {
    "org_deploy_enabled": false,
    "socket_mode_enabled": false,
    "token_rotation_enabled": false
  }
}
```

The manifest contains configuration, not credentials. Slack generates the app credentials after creation. It configures the five bot scopes requested by self-hosted LangSmith:

* **`chat:write`**: Send notification messages.
* **`channels:read`**: List public channels in the channel picker.
* **`channels:join`**: Join a selected public channel when delivering a notification, if needed.
* **`groups:read`**: List private channels that the bot has been invited to.
* **`reactions:write`**: Add and remove emoji reactions. Notification delivery does not currently use this permission.

Keep token rotation disabled. The integration stores bot tokens and does not refresh rotating tokens. Leave Socket Mode disabled; Event Subscriptions and an app-level token are not required for notification delivery.

Creating or installing the app in Slack does not connect it to LangSmith. Complete [Connect a Slack workspace](#connect-a-slack-workspace) after you [configure the deployment](#configure-your-deployment). LangSmith obtains and stores the workspace bot token through that authorization flow; you do not copy a bot token into the deployment.

### Configure your deployment

Configure these variables on the LangSmith platform backend using your deployment's [environment variable configuration](../Configure%20an%20instance/Configure%20environment%20variables%20in%20the%20Helm%20chart.md):

| Variable | Value |
| - | - |
| `LANGSMITH_SLACK_CLIENT_ID` | Your Slack app's Client ID. |
| `LANGSMITH_SLACK_CLIENT_SECRET` | Your Slack app's Client Secret, supplied from a secret. |
| `LANGSMITH_SLACK_REDIRECT_URI` | The exact HTTPS callback URL saved in Slack. |
| `LANGSMITH_URL` | Your deployment's browser-facing URL. Notification links and the return after authorization use this URL. |

For Helm deployments, including deployments on EKS, configure the app credentials through `platformBackend.deployment.extraEnv`.

First, create a Kubernetes Secret in the namespace where LangSmith runs. If you use a secrets operator, provision `slack-app-credentials` with keys `client-id` and `client-secret` through that operator. To create it manually, save the following as `slack-app-secret.yaml`, replacing all three placeholders. Keep the file containing credentials out of version control.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: slack-app-credentials
  namespace: "<your-langsmith-namespace>"
type: Opaque
stringData:
  client-id: "<your-slack-client-id>"
  client-secret: "<API_KEY>"
```

Apply the Secret:

```bash
kubectl apply -f slack-app-secret.yaml
```

Next, merge these entries into your existing Helm values file. Keep any existing `platformBackend.deployment.extraEnv` entries. Replace the callback URL with the same URL used in your manifest:

```yaml
platformBackend:
  deployment:
    extraEnv:
      - name: LANGSMITH_SLACK_CLIENT_ID
        valueFrom:
          secretKeyRef:
            name: slack-app-credentials
            key: client-id
      - name: LANGSMITH_SLACK_CLIENT_SECRET
        valueFrom:
          secretKeyRef:
            name: slack-app-credentials
            key: client-secret
      - name: LANGSMITH_SLACK_REDIRECT_URI
        value: "https://langsmith.example.com/api/v1/platform/slack/callback"
```

The chart sets `LANGSMITH_URL` from its hostname configuration. Configure `config.hostname`, `config.frontendHostname` if the UI uses a separate host, and `config.basePath` as needed. Avoid adding a duplicate `LANGSMITH_URL` through `extraEnv` or `commonEnv`.

Apply the updated values through your deployment process. If you manage Helm directly, use your existing release name, namespace, chart version, and complete values file:

```bash
helm upgrade <release-name> langchain/langsmith \
  --namespace <your-langsmith-namespace> \
  --version <your-chart-version> \
  --values <path-to-your-existing-values-file> \
  --wait
```

Use a chart version that contains the supported LangSmith release. For upgrade prerequisites, see [Upgrade a self-hosted deployment](../Manage%20an%20instance/Upgrade%20an%20installation.md).

Keep the existing `API_KEY_SALT` encryption secret consistent between the API and notification workers. They use it to encrypt and decrypt stored bot tokens. See [Use an existing secret](../Platform%20auth%20%26%20access%20control/Use%20an%20existing%20secret%20for%20your%20installation%20%28Kubernetes%29.md).

Wait for the platform backend rollout to complete, then reload LangSmith. If you changed a Secret without changing the Helm values, restart the platform backend so it loads the new credentials. Under your organization's **General** settings, the **Slack** section shows **Connect Slack** when configuration is complete.

The backend checks that the app credentials are present and the callback URL is valid. Slack verifies the credentials during authorization. Incorrect credentials can still show **Connect Slack**, then fail when you try to connect.

Changing or removing app credentials does not delete stored workspace connections or notification destinations. Previously stored bot tokens can continue delivering notifications. To stop delivery, disconnect the workspace or delete its notification destinations.

### Allow network access

For this integration, allow the following connections:

* **Backend:** Outbound HTTPS to the Slack Web API at `slack.com` for OAuth exchange, channel lookup, and notifications.
* **Browser:** Access to Slack and your deployment's callback URL and UI.

Slack redirects the browser to your callback. Slack does not need inbound network access to your deployment for notification delivery.

## Connect a Slack workspace

A Slack workspace connection belongs to your LangSmith organization, so you can reuse it across projects:

1. Open your LangSmith instance and go to **Settings** > your organization's **General** settings.
2. Under **Slack**, click **Connect Slack**. You can also connect from the channel selector when configuring an Engine or alert notification.
3. Choose the Slack workspace, review your app's requested permissions, and click **Allow**. Complete administrator approval if required.
4. Confirm that the browser returns to your LangSmith instance and the workspace appears as **Connected**. Choose that workspace and a channel in your notification settings. For a private channel, invite your configured Slack app to the channel first, then refresh the picker. LangSmith joins the selected public channel when it first delivers a message, if needed.
5. Save the destination with the event types and minimum issue severity you need. See [Configure Engine notifications](../../../Engine/LangSmith%20Engine%20notifications.md#notify-a-slack-channel) or [Configure alert notifications](../../../Monitor/Observe/Monitoring%20%26%20alerting/Alerts%20in%20LangSmith.md#step-4-configure-notification-channel).

## Verify delivery

Saving a destination does not send a test message. An Engine destination sends notifications for new events that match its event types and minimum issue severity. Existing issues do not emit a new notification when you save the destination.

To verify an Engine destination:

1. Save a Slack destination for `issue.created` on a test project. Under **Notify when**, select **Issue created**. Set **Minimum issue severity** to **All severities** during testing.
2. Enable [Engine for the test project](../../../Engine/Set%20up%20LangSmith%20Engine.md#turn-on-engine-for-a-tracing-project) and let it analyze new traces. Wait for Engine to create a new issue. If Engine finds no new issue, there is no `issue.created` notification to send.
3. Check that a message arrives in the selected channel and that **View issue** opens your self-hosted instance.

To verify Slack delivery without waiting for a new Engine issue, configure a Slack destination in a test project's alert settings. Click **Send Test Notification** and check the selected channel. See [Test the alert integration](../../../Monitor/Observe/Monitoring%20%26%20alerting/Alerts%20in%20LangSmith.md#2-test-the-integration). This checks the Slack connection, not Engine's event generation.

Slack notifications send content outside your deployment to the selected workspace. Engine messages can include issue titles, descriptions, severity, project information, links, and recurrence charts. Alert messages include alert and workspace names, metric values, thresholds, and links. Choose channels with access appropriate for that content. See [Engine notification format](../../../Engine/LangSmith%20Engine%20notifications.md#notify-a-slack-channel) and [Alert notification format](../../../Monitor/Observe/Monitoring%20%26%20alerting/Alerts%20in%20LangSmith.md#notification-format).

## Troubleshoot the connection

* **Slack is not configured:** Contact your operator. Confirm that your release supports the connection and all three Slack environment variables are set. Reload the UI after restarting the backend.
* **Slack configuration unavailable:** The UI could not load the backend's configuration. Reload the page and have your operator check the backend; this message does not mean app credentials are absent.
* **The backend pod cannot start:** Check that `slack-app-credentials` exists in the same namespace as LangSmith and contains both `client-id` and `client-secret`.
* **Slack rejects the app credentials:** Copy the Client ID and Client Secret from the same Slack app. Update the deployment Secret, restart the platform backend, and start **Connect Slack** again.
* **Authorization cannot start:** Confirm that the app has a bot user, all listed scopes, and permission to install in the selected workspace.
* **Slack reports a redirect mismatch:** Ensure `LANGSMITH_SLACK_REDIRECT_URI` matches the saved Slack Redirect URL, including scheme, host, port, and path.
* **Authorization fails after returning:** Start **Connect Slack** again. Authorization state expires after 10 minutes. Check browser access to the callback, backend access to Slack, and the configured app credentials. Keep token rotation disabled.
* **A private channel is absent:** Invite your configured Slack app to the channel, then refresh the picker.
* **Messages do not arrive:** Confirm Slack Web API access, matching encryption secrets on the API and workers, and the destination's event and severity filters. If someone removed the app from Slack, reconnect the workspace.
* **Links open the wrong host:** Correct your deployment's browser-facing URL configuration.

## See also

* [Engine on self-hosted LangSmith](../../../Engine/Self-hosted%20and%20BYOC/LangSmith%20Engine%20on%20Self-hosted%20and%20BYOC.md)
* [Engine notifications](../../../Engine/LangSmith%20Engine%20notifications.md)
* [Alerts](../../../Monitor/Observe/Monitoring%20%26%20alerting/Alerts%20in%20LangSmith.md)
* [Configure egress](../Configure%20an%20instance/Egress%20for%20billing%20and%20operational%20telemetry.md)

# LangSmith Engine notifications

> Send LangSmith Engine notifications to Slack, Jira Automation, and webhook endpoints.

[LangSmith Engine](LangSmith%20Engine.md) can notify you when it opens a new issue, links a new trace to an existing issue, or fails to complete a run. Notifications bring Engine's findings to the tools your team already watches, so new issues get triaged as they appear instead of waiting until someone opens the **Engine** page. Deliver these notifications to a **Slack channel**, a **Jira Automation incoming webhook**, or an **HTTP webhook endpoint**. Each destination has its own event types and minimum priority, so you can route urgent issues to a paging webhook while sending every issue to a Slack channel.

## Add a destination

Notification destinations are configured per tracing project or agent environment. On the **Engine** page, click **Configure Engine**, then under **Notifications** click **Add**. If no destination exists, the editor opens automatically. For each destination, choose:

* **Destination type**: Select the **Slack**, **Jira**, or **Webhook** tab. See [Notify a Slack channel](#notify-a-slack-channel), [Create Jira work items](#create-jira-work-items), and [Send to a webhook](#send-to-a-webhook).
* **Notify when**: The [event types](#event-types) that trigger a notification.
* **Minimum issue severity**: The issue [severity filter](#severity-filtering) that determines which notifications are sent.

To be alerted when a [watched issue](Find%20and%20fix%20your%20agent%27s%20issues%20with%20LangSmith%20Engine.md#watch-an-issue) recurs, click **Alert me via Slack** on the issue, which opens the same **Notifications** section.

## Event types

| **Notify when** option | Sent when | Webhook event type |
| - | - | - |
| **Issue created** | Engine opens a new issue. | [`issue.created`](#issue-created) |
| **New traces linked to issue** | Engine links a new trace to an existing issue. | [`issue.trace.added`](#issue-trace-added) |
| **Engine failed to complete a run** | An Engine run fails to complete. | [`issue.agent_run.failed`](#issue-agent_run-failed) |

For new destinations, the **Notify when** picker offers **Issue created** and **New traces linked to issue**. Destinations created before **Engine failed to complete a run** was removed from the picker can still receive it. A destination created without an explicit list of event types receives only **Issue created**.

Webhook payloads identify each event by its event type, shown in the last column. See [Webhook payload reference](#webhook-payload-reference).

## Severity filtering

The **Minimum issue severity** setting is stored as a `severity_threshold` from `0` to `3`. For issue events, a notification is delivered only when the issue's `severity` is less than or equal to the threshold. Lower numbers are more urgent.

| Severity | Meaning |
| - | - |
| `0` | Urgent |
| `1` | High |
| `2` | Medium |
| `3` | Low |

The picker offers **High severity only** (`1`), **Medium and high severity** (`2`), and **All severities** (`3`). For example, a destination with `severity_threshold: 1` receives events for `URGENT` (0) and `HIGH` (1) issues only.

Severity thresholds do not apply to [`issue.agent_run.failed`](#issue-agent_run-failed), because run-failure events are scoped to an Engine session rather than to a specific issue.

## Notify a Slack channel

If Slack is not configured on your self-hosted instance, the **Slack** tab shows **Contact your operator to enable Slack notifications**. The operator [creates a Slack app and configures its credentials](../LangSmith%20setup/Self-hosted/Connect%20external%20services/Connect%20self-hosted%20and%20BYOC%20LangSmith%20to%20Slack.md). On a [BYOC](../LangSmith%20setup/BYOC/Bring%20Your%20Own%20Cloud%20%28BYOC%29.md) data plane, an Organization Admin [configures the Slack app](../LangSmith%20setup/Self-hosted/Connect%20external%20services/Connect%20self-hosted%20and%20BYOC%20LangSmith%20to%20Slack.md#create-your-slack-app-on-byoc) under **Settings** > **General Settings** > **Slack**. You then connect a workspace through Slack authorization.

To add a Slack destination:

**1. Connect a Slack workspace**

Connecting a Slack workspace is an organization-level action you perform once, not per project. Connecting or disconnecting a workspace requires the `organization:manage` permission. In your LangSmith instance, open **Settings**, go to your organization's **General** settings, and under **Slack** click **Connect Slack**. Authorize the configured app in Slack. You can connect more than one Slack workspace to an organization.

**2. Add a Slack destination**

On the **Engine** page, click **Configure Engine**. Under **Notifications**, click **Add** if the editor is not already open. Select the **Slack** tab, then use the channel selector to choose a workspace and channel. If no workspace is connected, click **Connect Slack** in the channel selector and complete authorization.

**3. Choose events and severity**

Under **Notify when**, select which [event types](#event-types) post a message to the channel. Under **Minimum issue severity**, choose which issue severities trigger a notification. Click **Add** to save.

LangSmith joins the selected public channel when it first delivers a message, if needed. To post to a private channel, invite the configured Slack app to that channel in Slack first, then refresh the channel picker.

Each Slack message includes the issue title, description, and severity, a **View issue** link back to LangSmith, and (for issue events) a chart of the issue's recurrence over time. If a workspace's connection becomes invalid, for example, the app is removed from Slack, its destinations stop delivering until you reconnect it from your organization's **General** settings.

Slack destinations use the configured Slack app to post messages. They do not send the [webhook payload](#webhook-payload-reference), so webhook signing secrets and custom headers do not apply.

### Mention a coding agent

A Slack destination can mention a coding agent's Slack bot, such as [Open SWE](https://github.com/langchain-ai/open-swe), in the thread of an Engine notification. The mention gives the agent Engine's fix prompt for the issue, so it can work on a fix from Slack.

To mention a coding agent:

1. In Slack, add the agent's bot to the destination's channel.
2. In the Slack destination's settings, select the bot under **Mention agent on new issues**. To use a bot that is not listed, enter its Slack user ID. To stop mentioning the agent, select **None**.
3. (Optional) Under **Message to the agent**, enter an instruction of up to 1,000 characters. When empty, the mention uses `Investigate this issue and open a fix if needed.`
4. Save the destination.

The agent is mentioned in the thread of each **Issue created** message. If the destination notifies on **Fix PR ready**, the mention appears under the **Fix PR ready** message instead, once per issue.

The mention includes an issue marker, `<!-- langsmith-issue {"id":"<issue-id>"} -->`. If the agent includes the marker in the body of a pull request it opens in a GitHub repository [connected to Engine](Connect%20Engine%20to%20your%20repository.md), Engine links the pull request to the issue. Engine checks for the marker only when the pull request is opened, so adding it later has no effect. Engine does not link GitLab merge requests this way.

## Create Jira work items

The **Jira** destination sends Engine events to a Jira Automation incoming webhook. Configure a Jira rule to turn new Engine issues into Jira work items. LangSmith sends the [webhook payload](#webhook-payload-reference) with the `X-Automation-Webhook-Token` header. Jira destinations use this token for authentication and do not have an HMAC signing secret.

Use the final incoming-webhook URL. Jira deliveries do not follow redirects, including redirects on the same host. A `3xx` response is a permanent delivery error and is not retried. This keeps the token and payload on the configured endpoint.

You need permission to manage Jira automation rules and a project where the rule can create work items. Jira Cloud hosts the incoming webhook on Atlassian's infrastructure. For Jira Data Center, verify that your installed version's endpoint accepts the required token header. LangSmith's deployment type does not determine whether you use Jira Cloud or Data Center.

To create a work item for each new Engine issue:

**1. Configure the incoming webhook in Jira**

Create a Jira Automation rule with an **Incoming webhook** trigger. If Jira requires a saved rule to generate the URL, save it without enabling it first.

Select **No work items from the webhook**, called **No issues from the webhook** in older interfaces. Engine sends its own event payload, rather than Jira issue keys.

Generate the trigger's secret/token. Copy the webhook URL and token before saving. Keep the token out of the URL; LangSmith sends it in the authentication header.

**2. Add the Jira creation action**

Restrict the rule to the intended project. Add a **Create work item** action, called **Create issue** in older interfaces. Select an existing project and issue type, and configure any fields Jira requires.

For Jira Cloud, set **Summary** to `{{webhookData.object.name}}`. Set **Description** to:

```text
{{webhookData.object.description}}

Severity: {{webhookData.object.severity}}
LangSmith issue: {{webhookData.object.url}}
```

Jira Cloud exposes the envelope's `data` member as `webhookData`. Use `webhookData.object.*` for issue fields. The extra `.data` in `webhookData.data.object.name` resolves to an empty summary. Verify payload handling in your installed Jira Data Center version before using these mappings there.

**3. Add the Jira destination in LangSmith**

On the **Engine** page, click **Configure Engine**. Under **Notifications**, click **Add** and select **Jira**. Enter the **Jira Webhook URL** and **Jira webhook token** from the trigger.

Under **Notify when**, select only **Issue created** for this creation rule. Choose the **Minimum issue severity**, then click **Add**. Enable the rule in Jira.

**4. Verify Jira created the work item**

After Engine creates an issue that matches your severity filter, check Jira's automation audit log. Confirm that the rule succeeds and creates a work item with the expected summary, description, severity, and LangSmith issue link.

An HTTP success means Jira accepted the webhook, not that it created a work item. Rule conditions, required fields, actor permissions, and automation usage limits can prevent creation.

LangSmith stores the Jira token without displaying it again. To replace it, enter a new token. Changing the webhook URL also requires entering a token for the replacement URL. If you lose the token, rotate it in Jira and update the LangSmith destination.

### Reach a private Jira endpoint

Private Jira endpoints require network access from your LangSmith deployment. In self-hosted and hybrid deployments, webhook delivery runs in the customer data plane. Configure the following before adding the destination:

* **Network access**: Allow DNS resolution and outbound connectivity to Jira from both the LangSmith API and webhook delivery processes. Allow their source addresses through Jira's firewall.
* **Private addresses**: If the endpoint resolves to a private IP, set `SSRF_ALLOW_PRIVATE_IPS_WEBHOOKS=true` for both processes. Kubernetes-internal hostnames also require `SSRF_ALLOW_K8S_INTERNAL=true`. Other webhook URL protections remain active. For configuration, see [Set self-hosted environment variables](../LangSmith%20setup/Self-hosted/Configure%20an%20instance/Configure%20environment%20variables%20in%20the%20Helm%20chart.md).
* **TLS trust**: If Jira uses a private certificate authority, add its CA to the webhook delivery processes' trusted roots. Use system roots or `SSL_CERT_FILE`, retain other required roots, and keep TLS verification enabled.

## Send to a webhook

Forward Engine events to your own incident-management, paging, or chat tooling. Add a destination and select the **Webhook** tab. Enter a URL and, optionally, [custom headers](#custom-headers). Each delivery is [signed](#signing-secret) so you can verify its authenticity.

### Delivery

LangSmith sends a `POST` request with a JSON body to your webhook URL. The request uses `Content-Type: application/json` and includes any custom headers you attached to the destination.

| Property | Value |
| - | - |
| Method | `POST` |
| Body | JSON, [common envelope](#event-envelope) below |
| Scheme | `http://` and `https://` are accepted. `https://` is strongly recommended |
| Signature | `X-LangSmith-Signature` header, signed with the destination's signing secret |
| Timeout | 20 seconds per attempt |
| Attempts | Up to 4 attempts (1 initial plus 3 retries with exponential backoff) on transport errors, HTTP `408`, `425`, `429`, and any HTTP `5xx`. Other `4xx` responses are treated as permanent and are not retried |
| Response | Success is determined from the status code alone. Response bodies are ignored. |

> [!NOTE]
>
> Retries deliver a byte-identical payload, including the same `id`. Dedupe on `id` so a retried delivery does not produce a duplicate downstream effect.

### Custom headers

You can attach arbitrary headers to each destination (for example, `Authorization: Bearer …`) to authenticate the caller at your endpoint. `Content-Type` is always set by LangSmith and cannot be overridden.

### Signing secret

Each **Webhook** destination has a signing secret. LangSmith uses this secret to sign the raw webhook request body and sends the result in the `X-LangSmith-Signature` header. Jira destinations use their token header instead.

The header value has this format:

```text
sha256=<hex-encoded HMAC-SHA256 digest>
```

Verify the signature before parsing or acting on the payload. The HMAC input is the exact raw request body bytes, and the HMAC key is the destination's signing secret. Do not parse and reserialize the JSON body before verification.

```python Python
import hashlib
import hmac
from typing import Optional


def verify_langsmith_signature(
    *,
    body: bytes,
    signing_secret: str,
    signature_header: Optional[str],
) -> bool:
    if not signature_header or not signature_header.startswith("sha256="):
        return False

    expected = "sha256=" + hmac.new(
        signing_secret.encode("utf-8"),
        body,
        hashlib.sha256,
    ).hexdigest()

    return hmac.compare_digest(expected, signature_header)
```

```typescript TypeScript
import { createHmac, timingSafeEqual } from "node:crypto";

export function verifyLangSmithSignature({
  body,
  signingSecret,
  signatureHeader,
}: {
  body: Buffer;
  signingSecret: string;
  signatureHeader: string | undefined;
}) {
  if (!signatureHeader?.startsWith("sha256=")) {
    return false;
  }

  const expected = `sha256=${createHmac("sha256", signingSecret)
    .update(body)
    .digest("hex")}`;

  const expectedBytes = Buffer.from(expected);
  const actualBytes = Buffer.from(signatureHeader);

  return (
    expectedBytes.length === actualBytes.length &&
    timingSafeEqual(expectedBytes, actualBytes)
  );
}
```

### Roll a signing secret

Roll a signing secret when it may have been exposed, or when your organization's credential rotation policy requires a new secret.

To roll a secret, open the destination row in the **Engine settings** panel, click **Roll signing secret**, and confirm. LangSmith generates a new signing secret and uses it for future webhook deliveries immediately. The previous secret stops signing deliveries as soon as the roll completes.

After rolling the secret, update every consumer that verifies `X-LangSmith-Signature` with the new value.

### Test your endpoint

Before pointing a real destination at your endpoint, send a sample payload to verify it accepts and acknowledges within the 20-second timeout:

```bash
curl -X POST https://your-endpoint.example.com/webhook \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $WEBHOOK_SECRET" \
  -d @sample-issue-created.json
```

Use the example body from [`issue.created`](#issue-created) as `sample-issue-created.json`. Verify that:

* The custom `Authorization` header arrives and matches the secret you configured on the destination.
* The handler persists the event keyed by its `id` so retries are deduped.
* The handler returns `2xx` before kicking off slow downstream work.

### Security

* Webhook URLs are validated when the destination is created and again at delivery time. Private and metadata IP ranges are blocked in SaaS. Both `http://` and `https://` are accepted; use `https://` so the payload and any custom headers are not sent in cleartext.
* LangSmith signs webhook bodies with the destination's signing secret. Verify `X-LangSmith-Signature` before processing the payload.
* You can also set custom headers on the destination, such as `Authorization: Bearer …`, for routing or additional authentication at your endpoint.
* Dedupe on the event `id` so that a retried delivery does not cause a duplicate notification.

### Best practices

* **Acknowledge fast.** Respond with `2xx` as soon as you have persisted the event. Move slow work (fan-out, paging, downstream API calls) onto a queue so your handler stays within the 20-second timeout.
* **Tolerate unknown event types.** Ignore `type` values your handler does not recognize. New event types may be added without notice.
* **Tolerate new fields.** Parse payloads with a permissive schema. New fields may be added to existing event types without notice.

## Webhook payload reference

Webhook and Jira destinations receive the JSON payloads below. Slack destinations do not.

### Event envelope

Every event delivered to your endpoint uses the same outer JSON shape.

| Field | Type | Description |
| - | - | - |
| `id` | UUID | Unique identifier for this delivery. Stable across retries. Use it to dedupe. |
| `type` | string | Event type. One of [`issue.created`](#issue-created), [`issue.trace.added`](#issue-trace-added), or [`issue.agent_run.failed`](#issue-agent_run-failed). |
| `created` | integer | Unix seconds (UTC) when the event was enqueued. |
| `request_id` | UUID | Shared by every event fired from the same upstream action. See [Batch coalescing](#batch-coalescing). |
| `data` | object | Event payload. Always contains `data.object`. Contains [`data.trace`](#data-trace) only on [`issue.trace.added`](#issue-trace-added) events. |

### Issue `data.object`

For [`issue.created`](#issue-created) and [`issue.trace.added`](#issue-trace-added), `data.object` is a snapshot of the issue. Treat it as the authoritative state of the issue at the time the event was generated.

| Field | Type | Description |
| - | - | - |
| `id` | UUID | Issue ID. |
| `name` | string | Short title of the issue. |
| `description` | string | Human-readable description. |
| `severity` | integer | `0` (urgent) through `3` (low). See [Severity filtering](#severity-filtering). |
| `tenant_id` | UUID | Workspace the issue belongs to. |
| `tenant_name` | string | Workspace display name. |
| `session_id` | UUID | Tracing project the issue belongs to. |
| `session_name` | string | Tracing project name. |
| `url` | string | Deep link to the issue in the LangSmith UI. |

### Run failure `data.object`

For [`issue.agent_run.failed`](#issue-agent_run-failed), `data.object` describes the Engine run that failed.

| Field | Type | Description |
| - | - | - |
| `tenant_id` | UUID | Workspace the run belongs to. |
| `tenant_name` | string | Workspace display name. |
| `session_id` | UUID | Tracing project the run belongs to. |
| `session_name` | string | Tracing project name. |
| `url` | string | Deep link to the LangSmith project in the UI. |
| `thread_id` | string | Engine thread ID. |
| `run_id` | string | Engine run ID. Omitted when unavailable. |
| `status` | string | Final run status. |
| `error_message` | string | Error text from the failed run. Omitted when unavailable. |
| `occurred_at` | string | RFC 3339 timestamp of when the failure occurred. |

### `data.trace`

`data.trace` is included only on [`issue.trace.added`](#issue-trace-added) events.

| Field | Type | Description |
| - | - | - |
| `run_id` | UUID | ID of the run that was linked to the issue. |
| `trace_id` | UUID | ID of the trace that contains the run. |
| `start_time` | string | RFC 3339 timestamp of when the run started. |
| `comment` | string \| null | Optional note recorded when the trace was linked. Omitted when empty. |

### Batch coalescing

A single upstream action can produce multiple webhook events. When Engine opens a new issue and attaches five traces to it, you receive one [`issue.created`](#issue-created) event and five [`issue.trace.added`](#issue-trace-added) events, all sharing the same `request_id`. Use `request_id` to group these into a single downstream notification.

### `issue.created`

Sent when LangSmith Engine creates a new issue. `data.trace` is omitted.

```json
{
  "id": "b91c1f0e-7c4a-4f53-9d3e-9f1c8e7a2b10",
  "type": "issue.created",
  "created": 1747238400,
  "request_id": "0d2f4f6a-2a3a-4b6e-9b87-5d5b6e8c9a01",
  "data": {
    "object": {
      "id": "9a8b7c6d-5e4f-3a2b-1c0d-9e8f7a6b5c4d",
      "name": "Tool selection inconsistency",
      "description": "Agent repeatedly calls the search tool with identical arguments before terminating.",
      "severity": 1,
      "tenant_id": "11111111-2222-3333-4444-555555555555",
      "tenant_name": "Acme Workspace",
      "session_id": "66666666-7777-8888-9999-aaaaaaaaaaaa",
      "session_name": "prod-api",
      "url": "https://smith.langchain.com/o/11111111-2222-3333-4444-555555555555/projects/p/66666666-7777-8888-9999-aaaaaaaaaaaa?tab=5&issue=9a8b7c6d-5e4f-3a2b-1c0d-9e8f7a6b5c4d"
    }
  }
}
```

### `issue.trace.added`

Sent when a new trace is linked to an existing issue. `data.trace` describes the linked trace.

```json
{
  "id": "c02e3a4b-5c6d-7e8f-9a0b-1c2d3e4f5a6b",
  "type": "issue.trace.added",
  "created": 1747238410,
  "request_id": "0d2f4f6a-2a3a-4b6e-9b87-5d5b6e8c9a01",
  "data": {
    "object": {
      "id": "9a8b7c6d-5e4f-3a2b-1c0d-9e8f7a6b5c4d",
      "name": "Tool selection inconsistency",
      "description": "Agent repeatedly calls the search tool with identical arguments before terminating.",
      "severity": 1,
      "tenant_id": "11111111-2222-3333-4444-555555555555",
      "tenant_name": "Acme Workspace",
      "session_id": "66666666-7777-8888-9999-aaaaaaaaaaaa",
      "session_name": "prod-api",
      "url": "https://smith.langchain.com/o/11111111-2222-3333-4444-555555555555/projects/p/66666666-7777-8888-9999-aaaaaaaaaaaa?tab=5&issue=9a8b7c6d-5e4f-3a2b-1c0d-9e8f7a6b5c4d"
    },
    "trace": {
      "run_id": "f1e2d3c4-b5a6-9788-6655-44332211ffee",
      "trace_id": "abcdefab-1234-5678-9abc-def012345678",
      "start_time": "2026-05-14T12:30:00Z",
      "comment": "Reproduces the same tool-loop pattern."
    }
  }
}
```

### `issue.agent_run.failed`

Sent when LangSmith Engine fails to complete a run. This event is session-scoped, so it does not include `data.trace` and does not use severity filtering.

```json
{
  "id": "4d0e8db2-81e6-4491-b8e5-b13a8f5afc0d",
  "type": "issue.agent_run.failed",
  "created": 1747238500,
  "request_id": "f6bbd48a-0386-403d-9344-31051264b45f",
  "data": {
    "object": {
      "tenant_id": "11111111-2222-3333-4444-555555555555",
      "tenant_name": "Acme Workspace",
      "session_id": "66666666-7777-8888-9999-aaaaaaaaaaaa",
      "session_name": "prod-api",
      "url": "https://smith.langchain.com/o/11111111-2222-3333-4444-555555555555/projects/p/66666666-7777-8888-9999-aaaaaaaaaaaa",
      "thread_id": "thread-123",
      "run_id": "run-456",
      "status": "error",
      "error_message": "RuntimeError: missing API key",
      "occurred_at": "2026-05-14T12:45:00Z"
    }
  }
}
```

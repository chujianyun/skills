# Configure Context Hub commit webhooks

> Send Context Hub commit events to an external HTTPS endpoint and verify that LangSmith signed each request.

[Context Hub](../Prompt%20%26%20Context%20Hub.md) commit webhooks notify external services whenever an agent or skill commit is created in your [workspace](../../../LangSmith%20setup/Govern/Organization/Overview.md#workspaces). Use them to trigger automation from Context Hub changes, including commits created through [LangSmith Fleet](../../../Additional%20documentation/No-code%20agents%20with%20LangSmith%20Fleet.md).

Managing Context Hub webhooks requires the [`prompts:update`](../../../LangSmith%20setup/Govern/Users%20%26%20access%20control/Organization%20and%20workspace%20operations%20reference.md) permission, which [Workspace Admins](../../../LangSmith%20setup/Govern/Users%20%26%20access%20control/Role-based%20access%20control.md#workspace-admin) and [Workspace Editors](../../../LangSmith%20setup/Govern/Users%20%26%20access%20control/Role-based%20access%20control.md#workspace-editor) have by default.

## Add a webhook

Each webhook applies to the entire workspace. Every configured endpoint receives every agent and skill commit, including commits created by Fleet. The `context_hub.commit.created.v1` event does not support filtering by repository or event type.

To add a webhook:

1. In the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-context-hub-webhooks), go to **Settings** > **Integrations** > **Context Hub webhooks**.
2. Click **Add webhook**.
3. Enter a publicly reachable HTTPS URL.
4. (Optional) Add custom request headers, such as an `Authorization` header.
5. Click **Add webhook**.
6. Copy the generated signing secret and store it securely.

The number of subscriptions you can add depends on your workspace configuration.

## Manage a webhook

The webhook list displays endpoint URLs and custom header names. Header values and signing secrets remain hidden until you click **Reveal secrets**. You can reveal them later if you still have permission to manage Context Hub webhooks.

Use the controls on a webhook to manage it:

* **Edit webhook**: Change the HTTPS URL or replace its custom headers. Editing does not change the signing secret.
* **Roll signing secret**: Generate and reveal a new signing secret. LangSmith uses the new secret for future deliveries immediately, and the previous secret stops working. Update every consumer that verifies the webhook.
* **Delete webhook**: Stop the endpoint from receiving future Context Hub commit events from the workspace.

## Delivery

LangSmith sends a JSON `POST` request for each event. Custom headers cannot override `Content-Type` or `X-LangSmith-Signature`, which LangSmith sets after applying custom headers.

| Property | Value |
| - | - |
| Method | `POST` |
| URL | Publicly reachable HTTPS endpoint |
| Content type | `application/json` |
| Signature | `X-LangSmith-Signature` header, signed with the webhook's signing secret |
| Timeout | 20 seconds per attempt |
| Attempts | Up to 4 attempts: 1 initial attempt and up to 3 retries |
| Retry conditions | Transport failures, HTTP `408`, `425`, `429`, and `5xx` responses |
| Permanent responses | Other `4xx` responses are not retried |
| Response handling | A status below `400` succeeds. Response bodies do not affect success. |

Retries contain the byte-identical request body and retain the event `id`. Deduplicate events by `id` before producing downstream effects.

## Verify the signature

Each request includes an `X-LangSmith-Signature` header in this format:

```text
sha256=<lowercase hex HMAC-SHA256 digest>
```

Compute the HMAC-SHA256 digest over the exact raw request body bytes with the webhook's signing secret. Verify the signature before parsing the JSON, and compare the complete header value in constant time. Parsing and reserializing the body before verification can change its bytes and invalidate the signature.

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

## Event envelope

The outer `id`, `type`, `created`, and `data` envelope is frozen. The `.v1` suffix on the event type versions the `data.commit` schema.

```json
{
  "id": "0198...",
  "type": "context_hub.commit.created.v1",
  "created": 1720000000,
  "data": {
    "commit": {
      "repo_id": "...",
      "repo_handle": "my-agent",
      "repo_type": "agent",
      "commit_hash": "newcommithash0002",
      "parent_commit_hash": "parentcommithash0001",
      "created_at": "2023-11-14T22:13:20Z",
      "created_by": "user@example.com",
      "url": "https://smith.example.com/context/my-agent/newcommithash0002",
      "files_changed": [
        { "path": "skills/kept", "action": "modified" },
        { "path": "skills/added", "action": "added" },
        { "path": "skills/gone", "action": "removed" }
      ]
    }
  }
}
```

| Field | Type | Description |
| - | - | - |
| `id` | UUID | Unique event identifier that remains stable across retries. Use it to deduplicate events. |
| `type` | string | Exact event type. Currently `context_hub.commit.created.v1`. |
| `created` | integer | Unix seconds in UTC when the event was enqueued. |
| `data` | object | Versioned event data. Contains `data.commit`. |

### `data.commit`

The `data.commit` object describes the Context Hub commit that triggered the event.

| Field | Type | Description |
| - | - | - |
| `repo_id` | UUID | Context Hub repository ID. |
| `repo_handle` | string | Repository handle. |
| `repo_type` | string | Repository type: `agent` or `skill`. |
| `commit_hash` | string | Hash of the new commit. |
| `parent_commit_hash` | string | Hash of the parent commit. Omitted for an initial commit or when unavailable. |
| `created_at` | string | RFC 3339 timestamp when the commit was created. |
| `created_by` | string | LangSmith user ID that created the commit. Omitted when unavailable. |
| `url` | string | Deep link to the commit in the LangSmith UI. |
| `files_changed` | array | File changes included in the commit. Each entry contains `path` and `action`. |

### `data.commit.files_changed`

Each entry summarizes a changed path. It does not contain the file contents.

| Field | Type | Description |
| - | - | - |
| `path` | string | Path changed by the commit. |
| `action` | string | Change type: `added`, `modified`, or `removed`. |

## Handle event versions

Branch on the complete event type before parsing `data.commit`:

```typescript
if (event.type === "context_hub.commit.created.v1") {
  await handleCommitCreatedV1(event.data.commit);
} else {
  // Ignore unknown event types and versions safely.
}
```

A breaking change to `data.commit` uses a new event type suffix, such as `.v2`. Ignore unknown types instead of trying to parse them as v1, and allow unknown fields so compatible additions do not break your handler.

## Next step

* [Use the Context Hub](Use%20the%20Context%20Hub.md): Create, inspect, and promote agent and skill commits.

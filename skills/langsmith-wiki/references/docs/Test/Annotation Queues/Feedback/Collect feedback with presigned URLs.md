# Collect feedback with presigned URLs

> Use presigned feedback tokens to collect user feedback from client-side applications without exposing your LangSmith API key.

Presigned feedback tokens let you collect [feedback](../../../Monitor/Trace/Observability%20concepts.md#feedback) from client-side applications (browsers, mobile apps, etc.) without exposing your [LangSmith API key](../../../LangSmith%20setup/Account/Create%20an%20account%20and%20API%20key.md). Each token generates a URL scoped to a specific [run](../../../Monitor/Trace/Observability%20concepts.md#runs) and feedback key. Clients submit feedback by calling that URL directly with no authentication required.

This is useful when:

* Your frontend collects thumbs up/down or star ratings from end users.
* You want to embed feedback links in emails, Slack messages, or other external channels.
* You need to decouple feedback collection from your backend.

> [!NOTE]
>
> If you are using [Agent Server](../../../Deploy/Agent%20Server/Capabilities/Agent%20Server.md), presigned feedback URLs are generated automatically when you include `feedback_keys` in the run request. For that workflow, refer to [Collect user feedback for Agent Server runs](../../../Deploy/Agent%20Server/How%20to%20build/How%20to%20collect%20user%20feedback%20for%20Agent%20Server%20runs.md).

## Create a presigned feedback token

Use [`create_presigned_feedback_token()`](https://reference.langchain.com/python/langsmith/client/Client/create_presigned_feedback_token) / [`createPresignedFeedbackToken`](https://reference.langchain.com/javascript/classes/langsmith.client.Client.html#createpresignedfeedbacktoken) to generate a token for a specific run and feedback key. The returned object includes a `url` that clients can call to submit feedback:

```python Python
from langsmith import Client

client = Client()

run_id = "<run_id>"

token = client.create_presigned_feedback_token(
    run_id,
    feedback_key="user_score",
)

print(token.url)
# https://api.smith.langchain.com/api/v1/feedback/tokens/<token_id>
```

```typescript TypeScript
import { Client } from "langsmith";

const client = new Client();

const runId = "<run_id>";

const token = await client.createPresignedFeedbackToken(runId, "user_score");

console.log(token.url);
// https://api.smith.langchain.com/api/v1/feedback/tokens/<token_id>
```

### Set token expiration

Tokens expire after 3 hours by default. Pass `expiration` to customize this with either a `timedelta` (relative) or a `datetime` (absolute):

```python Python
import datetime
from langsmith import Client

client = Client()

run_id = "<run_id>"

token = client.create_presigned_feedback_token(
    run_id,
    feedback_key="user_score",
    expiration=datetime.timedelta(hours=24),
)
```

```typescript TypeScript
import { Client } from "langsmith";

const client = new Client();

const runId = "<run_id>";

const token = await client.createPresignedFeedbackToken(runId, "user_score", {
  expiration: { hours: 24 },
});
```

### Constrain feedback values

Pass `feedback_config` to restrict what values clients can submit. This is useful for enforcing a specific feedback schema (e.g., thumbs up/down, 1–5 stars, or categorical labels):

```python Python
from langsmith import Client

client = Client()

run_id = "<run_id>"

token = client.create_presigned_feedback_token(
    run_id,
    feedback_key="user_score",
    feedback_config={
        "type": "continuous",
        "min": 0,
        "max": 1,
    },
)
```

```typescript TypeScript
import { Client } from "langsmith";

const client = new Client();

const runId = "<run_id>";

const token = await client.createPresignedFeedbackToken(runId, "user_score", {
  feedbackConfig: {
    type: "continuous",
    min: 0,
    max: 1,
  },
});
```

### Create tokens in batch (Python only)

Use `create_presigned_feedback_tokens` (plural) to generate tokens for multiple feedback keys in a single call:

```python Python
from langsmith import Client

client = Client()

run_id = "<run_id>"

tokens = client.create_presigned_feedback_tokens(
    run_id,
    feedback_keys=["thumbs_up", "thumbs_down"],
)

for token in tokens:
    print(f"{token.id}: {token.url}")
```

## Submit feedback with a presigned URL

Once you have a presigned URL, your frontend code or email client submits feedback by sending a `POST` or `GET` request to it. The URL does not require an API key or authentication because the token provides the authorization.

Presigned URL feedback extends a base-retention trace to extended retention by default. There is no opt-out parameter for presigned URLs. For the full retention model, see [data retention auto-upgrades](../../../Monitor/Trace/Configuration%20%26%20troubleshooting/Usage%20and%20billing.md#data-retention-auto-upgrades).

### POST request

Use `POST` from your frontend when a user interacts with a feedback control (e.g., clicking a thumbs up button). `POST` supports `score`, `value`, `comment`, `correction`, and `metadata` fields.

```bash
curl --request POST \
  --url "https://api.smith.langchain.com/api/v1/feedback/tokens/<token_id>" \
  --header "Content-Type: application/json" \
  --data '{
    "score": 1,
    "comment": "This response was helpful!"
  }'
```

### GET request

Use `GET` when embedding a feedback link in an email or Slack message. The user's click triggers the request. `GET` supports `score`, `value`, `comment`, and `correction` as query parameters. `metadata` is not supported with `GET`.

```bash
curl --request GET \
  --url "https://api.smith.langchain.com/api/v1/feedback/tokens/<token_id>?score=1&comment=This%20response%20was%20helpful!"
```

### Submit feedback using the SDK

You can also submit feedback from a presigned token using the SDK, which is useful for server-side workflows where you received a token URL from another service.

```python Python
from langsmith import Client

client = Client()

client.create_feedback_from_token(
    "<token_or_url>",
    score=1,
    comment="This response was helpful!",
)
```

```typescript TypeScript
// Use a direct HTTP request to the presigned URL
await fetch(tokenUrl, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    score: 1,
    comment: "This response was helpful!",
  }),
});
```

## List existing tokens

Retrieve all presigned feedback tokens for a run using `list_presigned_feedback_tokens` / `listPresignedFeedbackTokens`.

```python Python
from langsmith import Client

client = Client()

run_id = "<run_id>"

for token in client.list_presigned_feedback_tokens(run_id):
    print(f"ID: {token.id}, URL: {token.url}, Expires: {token.expires_at}")
```

```typescript TypeScript
import { Client } from "langsmith";

const client = new Client();

const runId = "<run_id>";

for await (const token of client.listPresignedFeedbackTokens(runId)) {
  console.log(`URL: ${token.url}, Expires: ${token.expires_at}`);
}
```

## Related

* [Reference guide on feedback data format](../../../Monitor/Debug/Data%20type%20reference/Feedback%20data%20format.md)
* [Log feedback using the SDK](Log%20user%20feedback%20using%20the%20SDK.md)

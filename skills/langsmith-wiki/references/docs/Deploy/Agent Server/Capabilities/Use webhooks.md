# Use webhooks

> [!NOTE]
>
> This page covers **LangGraph API webhooks**, a way to receive a POST callback when a specific run completes. If you are looking for **LangSmith automation webhooks** (triggered when automation rules match runs or threads), see [Configure webhook notifications for rules](../../../Monitor/Observe/Automations/Configure%20webhook%20notifications%20for%20rules.md).

Webhooks enable event-driven communication from your LangSmith application to external services. For example, you may want to issue an update to a separate service once an API call to LangSmith has finished running.

Many LangSmith endpoints accept a `webhook` parameter. If this parameter is specified by an endpoint that can accept POST requests, LangSmith will send a request at the completion of a run.

When working with LangSmith, you may want to use webhooks to receive updates after an API call completes. Webhooks are useful for triggering actions in your service once a run has finished processing. To implement this, you need to expose an endpoint that can accept `POST` requests and pass this endpoint as a `webhook` parameter in your API request.

Currently, the SDK does not provide built-in support for defining webhook endpoints, but you can specify them manually using API requests.

## Supported endpoints

The following API endpoints accept a `webhook` parameter:

| Operation | HTTP Method | Endpoint |
| - | - | - |
| Create Run | `POST` | `/thread/{thread_id}/runs` |
| Create Thread Cron | `POST` | `/thread/{thread_id}/runs/crons` |
| Stream Run | `POST` | `/thread/{thread_id}/runs/stream` |
| Wait Run | `POST` | `/thread/{thread_id}/runs/wait` |
| Create Cron | `POST` | `/runs/crons` |
| Stream Run Stateless | `POST` | `/runs/stream` |
| Wait Run Stateless | `POST` | `/runs/wait` |

In this guide, we’ll show how to trigger a webhook after streaming a run.

## Set up your assistant and thread

Before making API calls, set up your assistant and thread.

> [tab] Python
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langgraph_sdk import get_client
>
> client = get_client(url=<DEPLOYMENT_URL>)
> assistant_id = "agent"
> thread = await client.threads.create()
> print(thread)
> ```

> [tab] JavaScript
>
> ```js theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { Client } from "@langchain/langgraph-sdk";
>
> const client = new Client({ apiUrl: <DEPLOYMENT_URL> });
> const assistantID = "agent";
> const thread = await client.threads.create();
> console.log(thread);
> ```

> [tab] cURL
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl --request POST \
>     --url <DEPLOYMENT_URL>/assistants/search \
>     --header 'Content-Type: application/json' \
>     --data '{ "limit": 10, "offset": 0 }' | jq -c 'map(select(.config == null or .config == {})) | .[0]' && \
> curl --request POST \
>     --url <DEPLOYMENT_URL>/threads \
>     --header 'Content-Type: application/json' \
>     --data '{}'
> ```

Example response:

```json
{
    "thread_id": "9dde5490-2b67-47c8-aa14-4bfec88af217",
    "created_at": "2024-08-30T23:07:38.242730+00:00",
    "updated_at": "2024-08-30T23:07:38.242730+00:00",
    "metadata": {},
    "status": "idle",
    "config": {},
    "values": null
}
```

## Use a webhook with a graph run

To use a webhook, specify the `webhook` parameter in your API request. When the run completes, LangSmith sends a `POST` request to the specified webhook URL.

For example, if your server listens for webhook events at `https://my-server.app/my-webhook-endpoint`, include this in your request:

> [tab] Python
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> input = { "messages": [{ "role": "user", "content": "Hello!" }] }
>
> async for chunk in client.runs.stream(
>     thread_id=thread["thread_id"],
>     assistant_id=assistant_id,
>     input=input,
>     stream_mode="events",
>     webhook="https://my-server.app/my-webhook-endpoint"
> ):
>     pass
> ```

> [tab] JavaScript
>
> ```js theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> const input = { messages: [{ role: "human", content: "Hello!" }] };
>
> const streamResponse = client.runs.stream(
>   thread["thread_id"],
>   assistantID,
>   {
>     input: input,
>     webhook: "https://my-server.app/my-webhook-endpoint"
>   }
> );
>
> for await (const chunk of streamResponse) {
>   // Handle stream output
> }
> ```

> [tab] cURL
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl --request POST \
>     --url <DEPLOYMENT_URL>/threads/<THREAD_ID>/runs/stream \
>     --header 'Content-Type: application/json' \
>     --data '{
>         "assistant_id": <ASSISTANT_ID>,
>         "input": {"messages": [{"role": "user", "content": "Hello!"}]},
>         "webhook": "https://my-server.app/my-webhook-endpoint"
>     }'
> ```

## Webhook payload

LangSmith sends webhook notifications in the format of a [Run](Runs/Runs.md). The request payload includes run input, configuration, and other metadata in the `kwargs` field. In addition to the standard run fields, the webhook payload also includes `values`, `webhook_sent_at`, and `error` fields.

The full webhook payload contains the following fields:

| Field | Type | Description |
| - | - | - |
| `run_id` | `string` (UUID) | Unique identifier for the run. |
| `thread_id` | `string` (UUID) | Identifier for the thread the run belongs to. |
| `assistant_id` | `string` | Identifier for the assistant that executed the run. |
| `status` | `string` | Final status of the run: `"success"`, `"error"`, `"timeout"`, `"interrupted"`, or `"rollback"`. See [Status values](#status-values) below. |
| `created_at` | `string` (datetime) | Timestamp when the run was created. |
| `updated_at` | `string` (datetime) | Timestamp when the run was last updated. |
| `run_started_at` | `string` (datetime) | Timestamp when the run began executing. |
| `run_ended_at` | `string` (datetime) | Timestamp when the run finished. Omitted if the run has not ended. |
| `webhook_sent_at` | `string` (datetime) | Timestamp when the webhook request was sent. |
| `metadata` | `JSON object` | Custom metadata associated with the run. |
| `kwargs` | `JSON object` | Run input, configuration, and other invocation parameters. |
| `values` | `JSON object` | The state values from the latest checkpoint of the thread. Only present for stateful runs. |
| `multitask_strategy` | `string` | The multitask strategy used for the run. |
| `error` | `JSON object \| null` | Present only if the run ended with an exception (any status other than `"success"`). Contains `error` (error type) and `message` (detail) fields. |

Example payload:

```json
{
  "run_id": "1ef6a5b8-4457-6db0-8b15-cffd3797fa04",
  "thread_id": "9dde5490-2b67-47c8-aa14-4bfec88af217",
  "assistant_id": "agent",
  "status": "success",
  "created_at": "2024-08-30T23:07:38.242730+00:00",
  "updated_at": "2024-08-30T23:07:40.120000+00:00",
  "run_started_at": "2024-08-30T23:07:38.300000+00:00",
  "run_ended_at": "2024-08-30T23:07:40.100000+00:00",
  "webhook_sent_at": "2024-08-30T23:07:40.150000+00:00",
  "metadata": {},
  "kwargs": {
    "input": {
      "messages": [{"role": "user", "content": "Hello!"}]
    }
  },
  "values": {
    "messages": [
      {"role": "user", "content": "Hello!"},
      {"role": "assistant", "content": "Hi there! How can I help you today?"}
    ]
  },
  "multitask_strategy": "reject",
  "error": null
}
```

When a run times out, the `status` field is `"timeout"` and the `error` field contains details about the failure:

```json
{
  "error": {
    "error": "TimeoutError",
    "message": "Run exceeded maximum execution time"
  }
}
```

## Status values

The `status` field takes one of five values:

| Value | When it is sent |
| - | - |
| `"success"` | The run completed normally. Also sent when a run pauses at an [`interrupt()`](https://reference.langchain.com/python/langgraph/types/interrupt) call waiting for human input. The pending interrupt is not visible in the payload, so read the thread state to detect it. |
| `"error"` | The run raised an unhandled exception. The `error` field in the payload contains the error type and message. |
| `"timeout"` | The run exceeded the background job timeout, set by the `BG_JOB_TIMEOUT_SECS` environment variable (default 86400 seconds). |
| `"interrupted"` | The run was cancelled while executing, either by a `multitask_strategy: "interrupt"` policy that preempted it for a newer run, or by a `runs.cancel` call with the default `interrupt` action. |
| `"rollback"` | The run was cancelled while executing and its checkpoints were deleted, either by a `multitask_strategy: "rollback"` policy or by a `runs.cancel` call with `action="rollback"`. The `values` field is `null`. |

A run that is cancelled while still pending never starts executing, so the server sends no webhook for it.

A single thread can receive more than one webhook call. For example, if a new run preempts an in-flight run, the server sends an `"interrupted"` webhook for the preempted run and a separate webhook for the new run when it finishes.

## Secure webhooks

To ensure only authorized requests hit your webhook endpoint, consider adding a security token as a query parameter:

```
https://my-server.app/my-webhook-endpoint?token=YOUR_SECRET_TOKEN
```

Your server should extract and validate this token before processing requests.

## Add headers to webhook requests

> [!NOTE]
>
> Available in `langgraph-api>=0.5.36`.

You can configure static headers to include with all outbound webhook requests. This is useful for authentication, routing, or passing metadata to your webhook endpoint.

Add a `webhooks.headers` configuration to your `langgraph.json` file:

```json
{
  "webhooks": {
    "headers": {
      "X-Custom-Header": "my-value",
      "X-Environment": "production"
    }
  }
}
```

### Use environment variables in headers

To include secrets or environment-specific values without checking them into your configuration file, use the `${{ env.VAR }}` template syntax:

```json
{
  "webhooks": {
    "headers": {
      "Authorization": "Bearer ${{ env.LG_WEBHOOK_TOKEN }}"
    }
  }
}
```

For security, only environment variables starting with `LG_WEBHOOK_` can be referenced by default. This prevents accidentally leaking unrelated environment variables. You can customize this prefix using `env_prefix`:

```json
{
  "webhooks": {
    "env_prefix": "MY_APP_",
    "headers": {
      "Authorization": "Bearer ${{ env.MY_APP_SECRET }}"
    }
  }
}
```

> [!NOTE]
>
> Missing required environment variables will block server startup, ensuring you don't deploy with incomplete configuration.

## Restrict webhook destinations

> [!NOTE]
>
> Available in `langgraph-api>=0.5.36`.

For security or compliance purposes, you can restrict which URLs are valid webhook destinations using the `webhooks.url` configuration:

```json
{
  "webhooks": {
    "url": {
      "allowed_domains": ["*.mycompany.com", "api.trusted-service.com"],
      "require_https": true
    }
  }
}
```

Available options:

| Option | Description |
| - | - |
| `allowed_domains` | Hostname allowlist. Supports wildcards for subdomains (e.g., `*.mycompany.com`). |
| `require_https` | Reject `http://` URLs when `true`. |
| `allowed_ports` | Explicit port allowlist. Defaults to 443 (https) and 80 (http). |
| `disable_loopback` | Disallow loopback addresses and relative URLs when `true`. Defaults to `true` in `langgraph-api` 0.10.0 or later. |
| `max_url_length` | Maximum permitted URL length in characters. |

Because `disable_loopback` defaults to `true`, webhooks to `localhost`, `127.0.0.1`, `host.docker.internal`, or a relative URL are rejected. This commonly affects a local receiver used with `langgraph dev`. To allow them, set `disable_loopback` to `false`:

```json
{
  "webhooks": {
    "url": {
      "disable_loopback": false
    }
  }
}
```

> [!NOTE]
>
> The server also applies an SSRF policy that blocks requests to cloud-metadata endpoints (such as `169.254.169.254`) and cluster-internal hosts by default. The `disable_loopback` option adds control over loopback and relative URLs on top of this baseline. Hosts that match an `allowed_domains` entry skip these SSRF checks.

## Disable webhooks

As of `langgraph-api>=0.2.78`, developers can disable webhooks in the `langgraph.json` file:

```json
{
  "http": {
    "disable_webhooks": true
  }
}
```

This feature is primarily intended for self-hosted deployments, where platform administrators or developers may prefer to disable webhooks to simplify their security posture—especially if they are not configuring firewall rules or other network controls. Disabling webhooks helps prevent untrusted payloads from being sent to internal endpoints.

For full configuration details, refer to the [configuration file reference](../../Get%20started/Reference/LangGraph%20CLI.md#configuration-file).

## Test webhooks

You can test your webhook using online services like:

* **[Beeceptor](https://beeceptor.com/)** – Quickly create a test endpoint and inspect incoming webhook payloads.
* **[Webhook.site](https://webhook.site/)** – View, debug, and log incoming webhook requests in real time.

These tools help you verify that LangSmith is correctly triggering and sending webhooks to your service.

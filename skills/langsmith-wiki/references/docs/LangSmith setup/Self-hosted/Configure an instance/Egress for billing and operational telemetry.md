# Egress for billing and operational telemetry

> [!NOTE]
>
> This page only applies to customers who are not running in offline (air-gapped) mode and assumes you are using a self-hosted LangSmith instance serving version 0.9.0 or later.

Self-hosted LangSmith stores platform data in your environment. Unless you are running in offline mode, LangSmith requires egress to `https://beacon.langchain.com` for the following:

* **Billing telemetry**: License verification and subscription/usage reporting (required)
* **Operational telemetry**: Logs, metrics, and traces for support diagnostics (optional, can be disabled)
* **Usage telemetry**: Anonymized usage snapshots for product insights (optional, can be disabled)

> [!WARNING]
>
> **Egress to `https://beacon.langchain.com` is required.** Refer to the [allowlisting IP section](../../Cloud/Cloud%20%28SaaS%29.md#allowlisting-ip-addresses) for static IP addresses, if needed.

> [!NOTE]
>
> If you enable [Engine](../../../Engine/Self-hosted%20and%20BYOC/LangSmith%20Engine%20on%20Self-hosted%20and%20BYOC.md), content goes to LangSmith Intelligence or your own model providers. With your own providers, LangChain receives only usage metadata through the configured reporting endpoint. See [LangSmith Intelligence for Engine](#langsmith-intelligence-for-engine) for the required destinations.

## Billing telemetry

Billing telemetry is **required** for self-hosted LangSmith instances that are not running in offline mode. This includes license verification and subscription/usage reporting.

> [!NOTE]
>
> Billing telemetry **cannot be disabled**. If you need to run without any egress, [contact our sales team](https://www.langchain.com/contact-sales) about an offline (air-gapped) license.

### What it does

* **License verification**: Validates your LangSmith license key at startup and periodically thereafter.
* **Subscription/usage reporting**: Reports platform usage metrics for billing purposes according to the entitlements in your order.

### What we collect

* License key validation requests
* Aggregated usage counts (number of traces, seats allocated, seats in use)
* Organization and workspace identifiers

### Example payloads

#### License verification

**Endpoint:** `POST beacon.langchain.com/v1/beacon/verify`

**Request:**

```json
{
  "license": "<YOUR_LICENSE_KEY>"
}
```

**Response:**

```json
{
  "token": "Valid JWT" //Short-lived JWT token to avoid repeated license checks
}
```

#### Subscription/usage reporting

**Endpoint:** `POST beacon.langchain.com/v1/beacon/ingest-traces`

**Request:**

```json
{
  "license": "<YOUR_LICENSE_KEY>",
  "trace_transactions": [
    {
      "id": "af28dfea-5358-463d-a2dc-37df1da72498",
      "tenant_id": "3a1c2b6f-4430-4b92-8a5b-79b8b567bbc1",
      "session_id": "b26ae531-cdb3-42a5-8bcf-05355199fe27",
      "trace_count": 5,
      "start_insertion_time": "2025-01-06T10:00:00Z",
      "end_insertion_time": "2025-01-06T11:00:00Z",
      "start_interval_time": "2025-01-06T09:00:00Z",
      "end_interval_time": "2025-01-06T10:00:00Z",
      "status": "completed",
      "num_failed_send_attempts": 0,
      "transaction_type": "type1",
      "organization_id": "c5b5f53a-4716-4326-8967-d4f7f7799735"
    }
  ]
}
```

**Response:**

```json
{
  "inserted_count": 1 //Number of transactions successfully ingested
}
```

## Operational telemetry

As of version **0.11**, LangSmith deployments send operational telemetry by default. This telemetry helps the LangChain team provide proactive support and faster troubleshooting for self-hosted instances.

> [!NOTE]
>
> Operational telemetry is **separate from** billing telemetry. You can disable operational telemetry while billing telemetry remains active.

### What it does

* Enables proactive support and faster troubleshooting of self-hosted instances
* Assists with performance tuning
* Helps prioritize improvements based on real-world usage patterns

### What we collect

* **Request metadata**: Anonymized request counts, sizes, and durations
* **Database metrics**: Query durations, error rates, and performance counters
* **Operational traces**: Timing and error information for high-latency or failed requests (these are **not** customer traces — they are traces about the functioning of the LangSmith instance itself)
* **Log messages**: Warning and error log messages only

> [!NOTE]
>
> We do not collect actual payload contents, database records, or any data that can identify your end users or customers. All telemetry data is associated with an organization and deployment, but never identified with individual users. We **do not collect PII** (personally identifiable information) in any form.

### How to disable

You can disable operational telemetry by setting the following values in your `langsmith_config.yaml` file:

```yaml
config:
  telemetry:
    logs: false
    metrics: false
    traces: false
```

You can also disable individual telemetry types by setting only specific values to `false`.

> [!WARNING]
>
> Disabling operational telemetry stops exporting the logs, metrics, and traces described in this section. It does **not** disable billing telemetry (license verification and subscription/usage reporting).

### Example payloads

#### Operational metrics

**Endpoint:** `POST beacon.langchain.com/v1/beacon/v1/metrics`

**Request:**

```json
{
  "resourceMetrics": [
    {
      "resource": {
        "attributes": [
          {
            "key": "resource.name",
            "value": { "stringValue": "langsmith-metrics" }
          },
          {
            "key": "env",
            "value": { "stringValue": "ls_self_hosted" }
          }
        ]
      },
      "scopeMetrics": [
        {
          "scope": {
            "name": "langsmith.metrics",
            "version": "0.1.0"
          },
          "metrics": [
            {
              "name": "langsmith_http_requests_latency",
              "unit": "seconds",
              "description": "Request latency of LangSmith services",
              "gauge": {
                "dataPoints": [
                  {
                    "asDouble": 12.34,
                    "startTimeUnixNano": 1678886400000000000,
                    "timeUnixNano": 1678886400000000000,
                    "attributes": [
                      {
                        "key": "endpoint",
                        "value": { "stringValue": "/sessions" }
                      },
                      { "key": "method", "value": { "stringValue": "GET" } },
                      {
                        "key": "service_name",
                        "value": { "stringValue": "langsmith_backend" }
                      }
                    ]
                  }
                ]
              }
            },
            {
              "name": "langsmith_http_requests_failed",
              "unit": "1",
              "description": "Counter of failed requests for LangSmith services",
              "sum": {
                "dataPoints": [
                  {
                    "asInt": 456,
                    "startTimeUnixNano": 1678886400000000000,
                    "timeUnixNano": 1678886400000000000,
                    "attributes": [
                      {
                        "key": "endpoint",
                        "value": { "stringValue": "/info" }
                      },
                      { "key": "method", "value": { "stringValue": "POST" } },
                      {
                        "key": "service_name",
                        "value": { "stringValue": "langsmith_platform_backend" }
                      }
                    ],
                    "aggregationTemporality": 2,
                    "isMonotonic": true
                  }
                ]
              }
            }
          ]
        }
      ]
    }
  ]
}
```

#### Operational traces

**Endpoint:** `POST beacon.langchain.com/v1/beacon/v1/traces`

**Request:**

```json
{
  "resourceSpans": [
    {
      "resource": {
        "attributes": [
          {
            "key": "env",
            "value": {
              "stringValue": "ls_self_hosted"
            }
          },
          {
            "key": "service.name",
            "value": {
              "stringValue": "langsmith_backend"
            }
          }
        ]
      },
      "scopeSpans": [
        {
          "scope": {},
          "spans": [
            {
              "traceId": "71699b6fe85982c7c8995ea3d9c95df2",
              "spanId": "3c191d03fa8be0",
              "parentSpanId": "",
              "name": "receive_request",
              "startTimeUnixNano": "1581452772000000321",
              "endTimeUnixNano": "1581452773000000789",
              "droppedAttributesCount": 1,
              "events": [
                {
                  "timeUnixNano": "1581452773000000123",
                  "name": "parse_request",
                  "attributes": [
                    {
                      "key": "request_size",
                      "value": {
                        "stringValue": "100"
                      }
                    }
                  ],
                  "droppedAttributesCount": 2
                },
                {
                  "timeUnixNano": "1581452773000000123",
                  "name": "event",
                  "droppedAttributesCount": 2
                }
              ],
              "droppedEventsCount": 1,
              "status": {
                "message": "status-cancelled",
                "code": 2
              }
            },
            {
              "traceId": "71699b6fe85982c7c8995ea3d9c95df2",
              "spanId": "0932ksdka12345",
              "parentSpanId": "3c191d03fa8be0",
              "name": "process_request",
              "startTimeUnixNano": "1581452772000000321",
              "endTimeUnixNano": "1581452773000000789",
              "links": [],
              "droppedLinksCount": 3,
              "status": {}
            }
          ]
        }
      ]
    }
  ]
}
```

#### Operational log messages

We only export error log messages from self-hosted LangSmith instances. This allows the LangChain team to troubleshoot application errors without requiring back-and-forth communication with your team.

**Endpoint:** `POST beacon.langchain.com/v1/beacon/v1/logs`

**Request:**

```json
{
  "resourceLogs": [
    {
      "resource": {
        "attributes": [
          {
            "key": "service.name",
            "value": {
              "stringValue": "langsmith_backend"
            }
          }
        ]
      },
      "scopeLogs": [
        {
          "scope": {},
          "logRecords": [
            {
              "timeUnixNano": "1581452773000009875",
              "severityNumber": 13,
              "severityText": "Warning",
              "body": {
                "stringValue": "Database connection pool approaching capacity"
              },
              "attributes": [
                {
                  "key": "component",
                  "value": {
                    "stringValue": "langsmith_backend"
                  }
                },
                {
                  "key": "pool_size",
                  "value": {
                    "intValue": "95"
                  }
                }
              ],
              "droppedAttributesCount": 0,
              "traceId": "08040201000000000000000000000000",
              "spanId": "0102040800000000"
            },
            {
              "timeUnixNano": "1581452773000000789",
              "severityNumber": 17,
              "severityText": "Error",
              "body": {
                "stringValue": "Failed to process trace batch"
              },
              "attributes": [
                {
                  "key": "component",
                  "value": {
                    "stringValue": "langsmith_queue_worker"
                  }
                },
                {
                  "key": "error_type",
                  "value": {
                    "stringValue": "timeout"
                  }
                }
              ],
              "droppedAttributesCount": 0,
              "traceId": "",
              "spanId": ""
            }
          ]
        }
      ]
    }
  ]
}
```

## Usage telemetry

Usage telemetry collects anonymized snapshots of your LangSmith instance's usage metrics. This data helps LangChain understand platform adoption patterns and inform product development decisions.

> [!NOTE]
>
> Usage telemetry is **enabled by default** and can be disabled. Unlike billing telemetry, you have full control over whether these snapshots are sent to LangChain.

### What it does

* Captures aggregated usage metrics at regular intervals
* Provides insight into feature adoption and platform growth
* Helps LangChain prioritize improvements and new features based on real-world usage

### What we collect

* **Platform metrics**: Counts of workspaces, projects, experiments, datasets, evaluators, and other platform resources
* **Feature usage**: Counts of run rules, annotation queues, prompts, and prompt-related activity
* **Users**: Total number of registered users and count of active PATs (Personal Access Tokens) in the last 30 days
* **Timestamps**: Time range for the snapshot (from/to timestamps in UTC)

> [!NOTE]
>
> All metrics are **aggregated counts only**. No individual resource data, identifiers, or usage patterns are collected. We do not collect any information that could identify your end users or customers.

### Example payloads

**Endpoint:** `POST /v1/beacon/usage-snapshot`

**Request:**

```json
{
  "license_key": "<YOUR_LICENSE_KEY>",
  "from_timestamp": "2026-03-25T02:00:00+00:00",
  "to_timestamp": "2026-03-26T02:00:00+00:00",
  "measures": {
    "workspaces": 12,
    "users": 63,
    "projects": 87,
    "experiments": 34,
    "datasets": 15,
    "evaluators": 8,
    "run_rules": 5,
    "annotation_queues": 3,
    "annotation_queue_items_reviewed_24h": 41,
    "prompts": 22,
    "prompt_commits": 156,
    "prompt_pulls": 1043,
    "active_pats_30d": 47
  }
}
```

### How to disable

You can disable usage telemetry by setting the following environment variable in your deployment configuration:

```yaml
PHONE_HOME_USAGE_REPORTING_ENABLED: false
```

Add this to the `commonEnv` section of your Helm configuration to permanently disable usage telemetry reporting.

> [!WARNING]
>
> Disabling usage telemetry does **not** affect billing or operational telemetry. License verification and subscription/usage reporting will continue to function normally.

## GitHub for Engine

When you [connect GitHub to Engine](../../../Engine/Self-hosted%20and%20BYOC/Configure%20GitHub%20for%20Engine%20on%20self-hosted%20and%20BYOC.md), allow outbound HTTPS from LangSmith services and sandbox hosts to your GitHub instance. GitHub must also reach LangSmith's webhook URL for automatic PR linking and issue completion after a merge.

These connections are separate from model-provider access. For the required hosts, connection directions, and private-network configuration, see [Engine's GitHub network requirements](../../../Engine/Self-hosted%20and%20BYOC/Configure%20GitHub%20for%20Engine%20on%20self-hosted%20and%20BYOC.md#allow-network-access).

## LangSmith Intelligence for Engine

[Engine](../../../Engine/Self-hosted%20and%20BYOC/LangSmith%20Engine%20on%20Self-hosted%20and%20BYOC.md) reports usage to LangSmith Intelligence (LSI), which can also run its models. If you use your own model providers, LSI receives only usage metadata. [Air-gapped installations](../../../Engine/Self-hosted%20and%20BYOC/LangSmith%20Engine%20on%20Self-hosted%20and%20BYOC.md#air-gapped-installations) do not connect to LSI.

Allow outbound HTTPS to the endpoint configured in `engine.intelligenceBaseUrl` for your [model-provider choice](../../../Engine/Self-hosted%20and%20BYOC/LangSmith%20Engine%20on%20Self-hosted%20and%20BYOC.md#choose-how-engine-runs-its-models):

* **LangSmith Intelligence:** `beacon.aws.langchain.com`. To keep this traffic on private networking, [connect with AWS PrivateLink](../../../Engine/Self-hosted%20and%20BYOC/Configure%20model%20providers%20for%20Engine%20on%20self-hosted%20and%20BYOC.md#connect-with-aws-privatelink).
* **Your own model providers:** `beacon.langchain.com`, the same host this page already requires, for usage reporting. Also allow outbound HTTPS to each provider's API endpoint.

> [!WARNING]
>
> Add each destination as a specific allowlist entry rather than opening general outbound access. Requests to LangSmith Intelligence authenticate with a short-lived license JWT obtained during LangSmith license verification.

### What it does

* **Runs Engine's models**, when an organization chooses LangSmith Intelligence.
* **Records Engine's usage** for billing, whichever way Engine runs its models.

### What we collect

When Engine runs on LangSmith Intelligence, each request may carry the trace content, source code, and intermediate output Engine needs to do its work. LangSmith Intelligence does not persist prompt or completion bodies. When Engine runs on your own model providers, LangSmith Intelligence receives only usage metadata.

LangSmith Intelligence retains the following metadata for usage attribution and billing:

* Account, workspace, and project identifiers used to attribute usage.
* Model and token-usage metadata used for billing.

For the complete data flow and model-provider commitments, see [Engine on Self-hosted](../../../Engine/Self-hosted%20and%20BYOC/LangSmith%20Engine%20on%20Self-hosted%20and%20BYOC.md).

> [!NOTE]
>
> Offline (air-gapped) Self-hosted can run Engine on your own model providers. See [Air-gapped installations](../../../Engine/Self-hosted%20and%20BYOC/LangSmith%20Engine%20on%20Self-hosted%20and%20BYOC.md#air-gapped-installations).

## Our commitment

The following commitments apply to the billing, operational, and usage telemetry described on this page. LangChain will not store sensitive information in that telemetry or share it with a third party. Log messages are filtered to only include error severity levels, and we do not capture log messages that could contain sensitive application data. Engine's use of LangSmith Intelligence is a separate data flow described in [Engine on Self-hosted](../../../Engine/Self-hosted%20and%20BYOC/LangSmith%20Engine%20on%20Self-hosted%20and%20BYOC.md). If you have any concerns about the data being sent, disable optional telemetry or [contact our sales team](https://www.langchain.com/contact-sales).

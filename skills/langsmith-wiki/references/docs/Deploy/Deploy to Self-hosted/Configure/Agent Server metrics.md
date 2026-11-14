# Agent Server metrics

> Reference for Agent Server OpenTelemetry metrics on self-hosted deployments, including Agent Server UI metrics, internal metrics, and Datadog export.

The [Agent Server](../../Agent%20Server/Capabilities/Agent%20Server.md) emits metrics through an OpenTelemetry (OTel) client. Metrics use the `lg_api_` name prefix by default (override with `METRIC_PREFIX`).

On self-hosted deployments, use this page to choose a scrape or push backend, enable the metric sets you need, and look up Prometheus names when building dashboards or alerts.

## Metric backends

Agent Server splits metrics into two sets:

* **Agent Server UI metrics**: Surfaced in the LangSmith Agent Server UI and exposed on the Agent Server Prometheus scrape endpoint (`GET /metrics`, `format=prometheus`) by default.
* **Internal metrics**: Operational and debugging metrics used by LangChain operators. Sent to Datadog when configured. On Prometheus, internal metrics appear only when you opt in.

| Backend | Metric set | Enable |
| - | - | - |
| **Prometheus** (scrape `GET /metrics`) | Agent Server UI metrics by default. Set `EXPOSE_INTERNAL_METRICS_PROMETHEUS=true` to also expose internal metrics on the same endpoint. | Available when the OTel Prometheus exporter is installed |
| **Datadog** (OTLP push) | Internal metrics only | Set `LSD_DD_API_KEY` (or `CUSTOM_LSD_DD_API_KEY`). Metrics push to `https://{LSD_DD_ENDPOINT}/v1/metrics` (default endpoint: `otlp.us5.datadoghq.com`). |

Prometheus and Datadog can run at the same time. Datadog receives the internal complement so UI metrics are not duplicated in both backends.

## Metric tiers

Each metric is assigned a tier that controls whether internal metrics are recorded:

| Tier | Value | Purpose |
| - | - | - |
| **CRITICAL** | `1` | Core health and failure signals. Always recorded when internal metrics are enabled, including on `dev` / `dev_free` deployments. |
| **INFO** | `2` | Operational detail for production monitoring. Default ceiling in production (`METRIC_MAX_EMITTING_TIER=2`). |
| **DEBUG** | `3` | Deeper diagnostics for troubleshooting. Omitted unless you raise `METRIC_MAX_EMITTING_TIER`. |
| **DEEP\_DEBUG** | `4` | Verbose diagnostics. Omitted unless you raise `METRIC_MAX_EMITTING_TIER`. |

Set `METRIC_MAX_EMITTING_TIER` to the highest tier you want recorded for internal metrics. Agent Server UI metrics ignore this setting and always emit.

## Configure export

### Prometheus

To scrape Agent Server UI metrics:

1. Point your Prometheus collector at the Agent Server `/metrics` endpoint (for example, `https://<agent-server-host>/metrics`).
2. Use the default `format=prometheus` query parameter (or omit it).

To also expose internal metrics on the same endpoint, set:

```bash
EXPOSE_INTERNAL_METRICS_PROMETHEUS=true
```

### Datadog

To push internal metrics to Datadog instead of (or alongside) Prometheus:

1. Set `LSD_DD_API_KEY` to your Datadog API key. `DATADOG_METRICS_ENABLED` turns on automatically when the key is present.
2. Optionally set `LSD_DD_ENDPOINT` (default: `otlp.us5.datadoghq.com`) or the legacy alias `CUSTOM_LSD_DD_API_KEY` / `CUSTOM_LSD_DD_ENDPOINT`.

Datadog receives only internal metrics. Continue scraping `/metrics` for Agent Server UI metrics in Prometheus or Grafana.

## Agent Server UI metrics

These metrics have `lsd_web_metric=true`. They appear on the Prometheus `/metrics` scrape by default and power the LangSmith Agent Server UI. Tier values are listed for reference; these metrics always emit regardless of `METRIC_MAX_EMITTING_TIER`.

| Name | Type | Tier | Description |
| - | - | - | - |
| `lg_api_http_requests_total` | Counter | INFO | Total HTTP requests to the Agent Server. |
| `lg_api_http_requests_latency` | Histogram (milliseconds) | INFO | HTTP request latency. |
| `lg_api_run_queue_wait_time_1st_attempt` | Histogram (milliseconds) | INFO | Time jobs spend waiting in the queue before first processing. |
| `lg_api_num_pending_runs` | Gauge | INFO | Runs currently pending. On Postgres backends, the Go core is the source; on in-memory backends, the Python collector emits this gauge. |
| `lg_api_num_running_runs` | Gauge | INFO | Runs currently running. Same runtime split as `lg_api_num_pending_runs`. |
| `lg_api_workers_max` | Gauge | CRITICAL | Maximum worker capacity. Emitted by the Python collector on in-memory runtimes; the Go core emits this on Postgres. |
| `lg_api_workers_active` | Gauge | CRITICAL | Workers currently executing runs. |
| `lg_api_workers_available` | Gauge | CRITICAL | Workers available to accept new runs. |
| `lg_api_pg_pool_max` | Gauge | CRITICAL | Maximum Postgres connection pool size. |
| `lg_api_pg_pool_size` | Gauge | CRITICAL | Connections currently managed by the Postgres pool (idle, in use, or being prepared). |
| `lg_api_pg_pool_available` | Gauge | INFO | Idle connections in the Postgres pool. |
| `lg_api_pg_pool_requests_queued_total` | Counter | CRITICAL | Postgres connection requests queued because a connection was not immediately available. The OTel Prometheus exporter appends `_total` to counter names. |
| `lg_api_pg_pool_requests_errors_total` | Counter | CRITICAL | Postgres connection request errors (timeouts, queue full, and similar failures). |
| `lg_api_redis_pool_max` | Gauge | INFO | Maximum Redis connection pool size. |
| `lg_api_redis_pool_size` | Gauge | INFO | Redis connections currently in use. |
| `lg_api_redis_pool_available` | Gauge | INFO | Idle connections in the Redis pool. |

## Internal metrics

These metrics have `lsd_web_metric=false`. By default they are exported to Datadog when `LSD_DD_API_KEY` is set. Set `EXPOSE_INTERNAL_METRICS_PROMETHEUS=true` to include them on the Prometheus `/metrics` scrape. Internal metrics at or below `METRIC_MAX_EMITTING_TIER` are recorded; higher-tier metrics are omitted.

### Re-encryption

| Name | Type | Tier | Description |
| - | - | - | - |
| `lg_api_reencrypt_writeback_succeeded_counter` | Counter | INFO | Lazy re-encryption replacement writebacks that succeeded. |
| `lg_api_reencrypt_writeback_cas_skipped_counter` | Counter | INFO | Replacement writebacks skipped because a concurrent update changed the stored value. |
| `lg_api_reencrypt_writeback_failed_counter` | Counter | INFO | Replacement writebacks that failed. Reads still return decrypted data. |

All three metrics include `reencryption_table` and `reencryption_column` attributes. See [Monitor lazy re-encryption](../../Agent%20Server/Server%20customization/Encryption%20at%20rest/Configure%20custom%20encryption%20at%20rest.md#monitor-lazy-re-encryption) for operational guidance.

### Run lifecycle

| Name | Type | Tier | Description |
| - | - | - | - |
| `lg_api_run_attempt_started_counter` | Counter | CRITICAL | Run execution attempts started. |
| `lg_api_run_success_counter` | Counter | CRITICAL | Runs completed successfully. |
| `lg_api_run_canceled_by_request_counter` | Counter | CRITICAL | Runs canceled by an explicit cancel request. |
| `lg_api_run_failed_retriable_counter` | Counter | CRITICAL | Runs failed with a retriable error. |
| `lg_api_run_failed_after_retry_counter` | Counter | CRITICAL | Runs that failed after exhausting retries. |
| `lg_api_run_exceed_max_attempts_at_start_counter` | Counter | CRITICAL | Runs rejected at start because max attempts were already exceeded. |
| `lg_api_run_abandoned_by_shutdown_counter` | Counter | CRITICAL | Runs abandoned during server shutdown. |
| `lg_api_run_set_status_error_counter` | Counter | CRITICAL | Errors while updating run status. |
| `lg_api_failed_to_fetch_runs_counter` | Counter | CRITICAL | Failures fetching runs from the queue. |
| `lg_api_run_execution_latency` | Histogram (milliseconds) | INFO | End-to-end run execution latency. |
| `lg_api_run_queue_wait_time_retry_attempt` | Histogram (milliseconds) | INFO | Queue wait time on retry attempts (after the first). |

### Streaming and protocol v2

| Name | Type | Tier | Description |
| - | - | - | - |
| `lg_api_streaming_data_loss_counter` | Counter | CRITICAL | Streaming data loss events. |
| `lg_api_stream_publish_latency` | Histogram (milliseconds) | INFO | Latency publishing stream chunks. |
| `lg_api_stream_data_size_bytes` | Histogram | DEBUG | Size of published stream payloads in bytes. |
| `lg_api_protocol_v2_buffer_evicted_counter` | Counter | INFO | Event Streaming v2 replay buffer evictions. |
| `lg_api_protocol_v2_event_emitted_counter` | Counter | DEBUG | Event Streaming v2 events emitted. |
| `lg_api_protocol_v2_resume_gap_counter` | Counter | INFO | Event Streaming v2 resume gaps detected during replay. |
| `lg_api_protocol_v2_transport_send_failure_counter` | Counter | INFO | Event Streaming v2 transport send failures. |
| `lg_api_protocol_v2_buffer_size` | Gauge | DEBUG | Current Event Streaming v2 replay buffer occupancy per run. Tune `LSD_PROTOCOL_V2_BUFFER_SIZE` when this approaches the limit. |
| `lg_api_protocol_v2_replayed_events` | Histogram | DEBUG | Number of events replayed on Event Streaming v2 reconnect. |

### Server and infrastructure

| Name | Type | Tier | Description |
| - | - | - | - |
| `lg_api_server_started_counter` | Counter | INFO | Server start events. |
| `lg_api_server_requested_to_stop_counter` | Counter | INFO | Graceful shutdown requests received. |
| `lg_api_server_stopped_counter` | Counter | INFO | Server stop events. |
| `lg_api_graph_recursion_limit_error_counter` | Counter | INFO | Graph recursion limit errors. |
| `lg_api_publish_queue_availability` | Gauge | CRITICAL | Redis publish queue availability signal. |

## See also

* [Self-hosted overview](../Deploy%20to%20self-hosted.md)
* [Configure Agent Server for scale](Configure%20Agent%20Server%20for%20scale.md)
* [Troubleshooting for self-hosted deployments](Troubleshooting%20for%20self-hosted%20deployments.md)
* [Agent Server changelog](../../Get%20started/Reference/Agent%20Server%20changelog.md)

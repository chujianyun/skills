# Export LangSmith telemetry to your observability backend

> [!WARNING]
>
> **This section is only applicable for Kubernetes deployments.**

Self-Hosted LangSmith instances produce telemetry data in the form of logs, metrics and traces. This section will show you how to access and export that data to an observability collector or backend.

This section assumes that you have monitoring infrastructure set up already, or you will set up this infrastructure and want to know how to configure LangSmith to collect data from it.

Infrastructure refers to:

* Collectors, such as [OpenTelemetry](https://opentelemetry.io/docs/collector/), [FluentBit](https://docs.fluentbit.io/manual) or [Prometheus](https://prometheus.io/).
* Observability backends, such as [Datadog](https://www.datadoghq.com/) or the [Grafana](https://grafana.com/) ecosystem.

## Logs

For a reference setup, see the [OTel collector example](Configure%20your%20collector%20for%20LangSmith%20telemetry.md#logs).

All services that are part of the LangSmith self-hosted deployment write logs to their node's filesystem and to stdout. In order to access these logs, you need to set up your collector to read from either the filesystem or stdout. Most popular collectors support reading logs from filesystems.

* **OpenTelemetry**: [File Log Receiver](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/filelogreceiver)
* **FluentBit**: [Tail Input](https://docs.fluentbit.io/manual/pipeline/inputs/tail)
* **Datadog**: [Kubernetes Log Collection](https://docs.datadoghq.com/containers/kubernetes/log/?tab=datadogoperator)

## Metrics

For a reference setup, see the [OTel collector example](Configure%20your%20collector%20for%20LangSmith%20telemetry.md#metrics).

### LangSmith services

The following LangSmith services expose metrics at an endpoint, in the Prometheus metrics format. The frontend does not currently expose metrics.

* **Backend**: `http://<langsmith_release_name>-backend.<namespace>.svc.cluster.local:1984/metrics`
* **Platform Backend**: `http://<langsmith_release_name>-platform-backend.<namespace>.svc.cluster.local:1986/metrics`
* **Playground**: `http://<langsmith_release_name>-playground.<namespace>.svc.cluster.local:1988/metrics`
* **(LangSmith Control Plane only) Host Backend**: `http://<langsmith_release_name>-host-backend.<namespace>.svc.cluster.local:1985/metrics`

You can use a [Prometheus](https://prometheus.io/docs/prometheus/latest/getting_started/#configure-prometheus-to-monitor-the-sample-targets) or [OpenTelemetry](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/prometheusreceiver) collector to scrape the endpoints, and export metrics to the backend of your choice.

### Sandbox hosts

For tabbed SmithDB and Sandbox dashboards, see [Monitor self-hosted LangSmith with Datadog or Grafana](Monitor%20self-hosted%20LangSmith%20with%20Datadog%20or%20Grafana.md). The guide covers component collection settings, deployment filters, platform coverage, and compatibility.

### Frontend Nginx

The frontend service exposes its Nginx metrics at the following endpoint: `langsmith-frontend.langsmith.svc.cluster.local:80/nginx_status`. You can either scrape them yourself, or bring up a [Prometheus Nginx exporter](https://github.com/prometheus-community/helm-charts/tree/main/charts/prometheus-nginx-exporter).

> [!WARNING]
>
> **The following sections apply for in-cluster databases only. If you are using external databases, you will need to configure exposing and fetching metrics.**

### Postgres + Redis

If you are using in-cluster Postgres/Redis instances, you can use a Prometheus exporter to expose metrics from your instance. You can deploy a [Postgres exporter](https://github.com/prometheus-community/helm-charts/tree/main/charts/prometheus-postgres-exporter) and/or [Redis exporter](https://github.com/prometheus-community/helm-charts/tree/main/charts/prometheus-redis-exporter).

### Clickhouse

The in-cluster Clickhouse is configured to expose metrics without the need for an exporter. You can use your collector to scrape metrics at `http://<langsmith_release_name>-clickhouse.<namespace>.svc.cluster.local:9363/metrics`

## Traces

For a reference setup, see the [OTel collector example](Configure%20your%20collector%20for%20LangSmith%20telemetry.md#traces).

The LangSmith Backend, Platform Backend, Playground and LangSmith Queue deployments have been instrumented to emit [Otel](https://opentelemetry.io/docs/concepts/signals/traces/) traces. Tracing is toggled off by default, and can be enabled for all LangSmith services with the following in your `langsmith_config.yaml` (or equivalent) file:

```yaml
config:
  tracing:
    enabled: true
    endpoint: "<your_collector_endpoint>"
    useTls: true # / false
    env: "ls_self_hosted" # This value will be set as an "env" attribute in your spans
    exporter: "http" # must be either http or grpc
```

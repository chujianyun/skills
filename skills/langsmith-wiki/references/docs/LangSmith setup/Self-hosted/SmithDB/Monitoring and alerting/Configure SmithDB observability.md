# Configure SmithDB observability

> Scrape SmithDB application metrics and export logs and traces to your existing observability stack.

SmithDB components expose application metrics and can export logs and traces to your existing observability stack. Set this up after you deploy SmithDB services and before you tune capacity or migrate historical data. It provides the signals to validate those changes and investigate failures.

## Metrics

Each SmithDB component exposes application metrics at the fixed `/metrics` path on its HTTP port. Configure your monitoring stack to discover the pods by adding scrape annotations to each component:

> [accordion] Sample Prometheus configuration
>
> ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> smithdb:
>   query:
>     deployment:
>       annotations:
>         prometheus.io/scrape: "true"
>         prometheus.io/path: "/metrics"
>         prometheus.io/port: "8060"
>   ingestion:
>     deployment:
>       annotations:
>         prometheus.io/scrape: "true"
>         prometheus.io/path: "/metrics"
>         prometheus.io/port: "8050"
>   compaction:
>     deployment:
>       annotations:
>         prometheus.io/scrape: "true"
>         prometheus.io/path: "/metrics"
>         prometheus.io/port: "8070"
>   compactionWorker:
>     deployment:
>       annotations:
>         prometheus.io/scrape: "true"
>         prometheus.io/path: "/metrics"
>         prometheus.io/port: "9000"
>   clusterManager:
>     deployment:
>       annotations:
>         prometheus.io/scrape: "true"
>         prometheus.io/path: "/metrics"
>         prometheus.io/port: "8090"
>   migration:
>     job:
>       annotations:
>         prometheus.io/scrape: "true"
>         prometheus.io/path: "/metrics"
>         prometheus.io/port: "9040"
> ```
>
> On LangSmith 0.16, set the migration annotations under `smithdb.migration.deployment.annotations`.
>
> With `smithdb.topology: unified`, annotate the unified pod and scrape port `8060` only:
>
> ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> smithdb:
>   unified:
>     deployment:
>       annotations:
>         prometheus.io/scrape: "true"
>         prometheus.io/path: "/metrics"
>         prometheus.io/port: "8060"
> ```

These are Prometheus-style annotations. Providers with their own discovery format, such as Datadog, need that format applied to the same ports and path. Monitor the PostgreSQL metastore, Kubernetes nodes, and cloud services with your existing infrastructure monitoring.

For which metrics to watch and how to read them, see [Essential SmithDB metrics](Essential%20SmithDB%20metrics.md).

## Logs and traces

SmithDB uses the chart-level OpenTelemetry tracing configuration described in [Export LangSmith telemetry to your observability backend](../../Self-hosted%20observability/Export%20LangSmith%20telemetry%20to%20your%20observability%20backend.md), with one difference: SmithDB exports over OTLP gRPC only. Set `config.observability.tracing.exporter` to `grpc`. With `http`, SmithDB export stays disabled and SmithDB logs remain console-only. The chart adds SmithDB pod and container names as OpenTelemetry resource attributes automatically.

To customize SmithDB log filtering, set `RUST_LOG` for all SmithDB workloads through `smithdb.commonEnv`:

```yaml
smithdb:
  commonEnv:
    - name: RUST_LOG
      value: "warn,smithdb_query=debug,vortex=warn"
```

Confirm the collector is reachable from the LangSmith namespace, apply the chart, then confirm telemetry arrives. To set up or tune a collector, see [Configure your collector for LangSmith telemetry](../../Self-hosted%20observability/Configure%20your%20collector%20for%20LangSmith%20telemetry.md).

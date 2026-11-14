# Configure your collector for LangSmith telemetry

The various services in a LangSmith deployment emit telemetry data in the form of logs, metrics, and traces. You may already have telemetry collectors set up in your Kubernetes cluster, or would like to deploy one to monitor your application.

This page describes how to configure an [OTel Collector](https://opentelemetry.io/docs/collector/configuration/) to gather telemetry data from LangSmith. Note that all of the concepts discussed below can be translated to other collectors such as [Fluentd](https://www.fluentd.org/) or [FluentBit](https://fluentbit.io/).

> [!WARNING]
>
> **This section is only applicable for Kubernetes deployments.**

# Receivers

## Logs

This is an example for a ***Sidecar*** collector to read logs from its own pod, excluding logs from non domain-specific containers. A Sidecar configuration is useful here because we require access to every container's filesystem. A DaemonSet can also be used.

```yaml
filelog:
  exclude:
    - "**/otc-container/*.log"
  include:
    - /var/log/pods/${POD_NAMESPACE}_${POD_NAME}_${POD_UID}/*/*.log
  include_file_name: false
  include_file_path: true
  operators:
    - id: container-parser
      type: container
  retry_on_failure:
    enabled: true
  start_at: end
env:
  - name: POD_NAME
    valueFrom:
      fieldRef:
        fieldPath: metadata.name
  - name: POD_NAMESPACE
    valueFrom:
      fieldRef:
        fieldPath: metadata.namespace
  - name: POD_UID
    valueFrom:
      fieldRef:
        fieldPath: metadata.uid
volumes:
  - name: varlogpods
    hostPath:
      path: /var/log/pods
volumeMounts:
  - name: varlogpods
    mountPath: /var/log/pods
    readOnly: true
```

> [!NOTE]
>
> **This configuration requires 'get', 'list', and 'watch' permissions on pods in the given namespace.**

## Metrics

Metrics can be scraped using the Prometheus endpoints. A single instance ***Gateway*** collector can be used to avoid duplication of queries when fetching metrics. The following config scrapes all of the default named LangSmith services:

```yaml
prometheus:
  config:
    scrape_configs:
      - job_name: langsmith-services
        metrics_path: /metrics
        scrape_interval: 15s
        # Only scrape endpoints in the LangSmith namespace
        kubernetes_sd_configs:
          - role: endpoints
            namespaces:
              names: [<langsmith-namespace>]
        relabel_configs:
          # Only scrape services with the name langsmith-.*
          - source_labels: [__meta_kubernetes_service_name]
            regex: "langsmith-.*"
            action: keep
          # Only scrape ports with the following names
          - source_labels: [__meta_kubernetes_endpoint_port_name]
            regex: "(backend|platform|playground|redis-metrics|postgres-metrics|metrics)"
            action: keep
          # Promote useful metadata into regular labels
          - source_labels: [__meta_kubernetes_service_name]
            target_label: k8s_service
          - source_labels: [__meta_kubernetes_pod_name]
            target_label: k8s_pod
          # Replace the default "host:port" as Prom's instance label
          - source_labels: [__address__]
            target_label: instance
```

> [!NOTE]
>
> **This configuration requires 'get', 'list', and 'watch' permissions on pods, services and endpoints in the given namespace.**

### Traces

For traces, you need to enable the OTLP receiver. The following configuration can be used to listen to HTTP traces on port 4318, and GRPC on port 4317:

```yaml
otlp:
  protocols:
    grpc:
      endpoint: 0.0.0.0:4317
    http:
      endpoint: 0.0.0.0:4318
```

## Processors

### Recommended OTEL processors

The following processors are recommended when using the OTel collector:

* [Batch Processor](https://github.com/open-telemetry/opentelemetry-collector/blob/main/processor/batchprocessor/README.md): Groups the data into batches before sending to exporters.
* [Memory Limiter](https://github.com/open-telemetry/opentelemetry-collector/blob/main/processor/memorylimiterprocessor/README.md): Prevents the collector from using too much memory and crashing. When the soft limit is crossed, the collector stops accepting new data.
* [Kubernetes Attributes Processor](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/k8sattributesprocessor): Adds Kubernetes metadata such as pod name into the telemetry data.

## Exporters

Exporters just need to point to an external endpoint of your liking. The following configuration allows you to configure a separate endpoint for logs, metrics and traces:

```yaml
otlphttp/logs:
  endpoint: <your_logs_endpoint>
otlphttp/metrics:
  endpoint: <your_metrics_endpoint>
otlphttp/traces:
  endpoint: <your_traces_endpoint>
```

> [!NOTE]
>
> **The OTel Collector also supports exporting directly to a [Datadog](https://docs.datadoghq.com/opentelemetry/setup/collector_exporter) endpoint.**

# Example collector configuration: Logs sidecar

```yaml
mode: sidecar
image: otel/opentelemetry-collector-contrib
config:
  receivers:
    filelog:
      exclude:
        - "**/otc-container/*.log"
      include:
        - /var/log/pods/${POD_NAMESPACE}_${POD_NAME}_${POD_UID}/*/*.log
      include_file_name: false
      include_file_path: true
      operators:
        - id: container-parser
          type: container
      retry_on_failure:
        enabled: true
      start_at: end
  processors:
    batch:
      send_batch_size: 8192
      timeout: 10s
    memory_limiter:
      check_interval: 1m
      limit_percentage: 90
      spike_limit_percentage: 80
  exporters:
    otlphttp/logs:
      endpoint: <your-endpoint>
  service:
    pipelines:
      logs/langsmith:
        receivers: [filelog]
        processors: [batch, memory_limiter]
        exporters: [otlphttp/logs]
env:
  - name: POD_NAME
    valueFrom:
      fieldRef:
        fieldPath: metadata.name
  - name: POD_NAMESPACE
    valueFrom:
      fieldRef:
        fieldPath: metadata.namespace
  - name: POD_UID
    valueFrom:
      fieldRef:
        fieldPath: metadata.uid
volumes:
  - name: varlogpods
    hostPath:
      path: /var/log/pods
volumeMounts:
  - name: varlogpods
    mountPath: /var/log/pods
    readOnly: true
```

# Example collector configuration: Metrics and traces Gateway

```yaml
mode: deployment
image: otel/opentelemetry-collector-contrib
config:
  receivers:
    prometheus:
      config:
        scrape_configs:
          - job_name: langsmith-services
            metrics_path: /metrics
            scrape_interval: 15s
            # Only scrape endpoints in the LangSmith namespace
            kubernetes_sd_configs:
              - role: endpoints
                namespaces:
                  names: [<langsmith-namespace>]
            relabel_configs:
              # Only scrape services with the name langsmith-.*
              - source_labels: [__meta_kubernetes_service_name]
                regex: "langsmith-.*"
                action: keep
              # Only scrape ports with the following names
              - source_labels: [__meta_kubernetes_endpoint_port_name]
                regex: "(backend|platform|playground|redis-metrics|postgres-metrics|metrics)"
                action: keep
              # Promote useful metadata into regular labels
              - source_labels: [__meta_kubernetes_service_name]
                target_label: k8s_service
              - source_labels: [__meta_kubernetes_pod_name]
                target_label: k8s_pod
              # Replace the default "host:port" as Prom's instance label
              - source_labels: [__address__]
                target_label: instance
    otlp:
      protocols:
        grpc:
          endpoint: 0.0.0.0:4317
        http:
          endpoint: 0.0.0.0:4318
  processors:
    batch:
      send_batch_size: 8192
      timeout: 10s
    memory_limiter:
      check_interval: 1m
      limit_percentage: 90
      spike_limit_percentage: 80
  exporters:
    otlphttp/metrics:
      endpoint: <metrics_endpoint>
    otlphttp/traces:
      endpoint: <traces_endpoint>
  service:
    pipelines:
      metrics/langsmith:
        receivers: [prometheus]
        processors: [batch, memory_limiter]
        exporters: [otlphttp/metrics]
      traces/langsmith:
        receivers: [otlp]
        processors: [batch, memory_limiter]
        exporters: [otlphttp/traces]
```

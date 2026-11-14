# Deploy an observability stack for your LangSmith deployment

> [!CAUTION]
>
> **Deprecated**: The LangSmith Observability Helm chart is deprecated. We no longer maintain or provide support for it. The documentation below is preserved for reference only.

> [!WARNING]
>
> **This section is only applicable for Kubernetes deployments.**

LangSmith applications expose telemetry data that can be sent to the backend of your choice. If you don’t already have an observability stack, or prefer to keep LangSmith telemetry separate from your main application, you can use the LangSmith Observability Helm chart to deploy a basic observability stack.

# Section 1: Prometheus exporters

Use this section if you would like to only deploy metrics exporters for the components in your self hosted deployment, which you can then scrape using your telemetry. If you would like a full observability stack deployed for you, go to the [End-to-End Deployment Section](Deploy%20an%20observability%20stack%20for%20your%20LangSmith%20deployment.md#prerequisites).

The helm chart provides a set of Prometheus exporters to expose metrics from [Redis](https://github.com/prometheus-community/helm-charts/tree/main/charts/prometheus-redis-exporter), [Postgres](https://github.com/prometheus-community/helm-charts/tree/main/charts/prometheus-postgres-exporter), [Nginx](https://github.com/prometheus-community/helm-charts/tree/main/charts/prometheus-nginx-exporter), and [Kube state metrics](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-state-metrics).

1. Create a local file called `langsmith_obs_config.yaml`
2. Copy over the values from this [file](https://github.com/langchain-ai/helm/blob/main/charts/langsmith-observability/examples/metric-exporters-only.yaml) into `langsmith_obs_config.yaml`, making sure to modify the values to match your LangSmith deployment.
3. Find the latest version of the chart by running `helm search repo langchain/langsmith-observability --versions`.
4. Grab the latest version number, and run `helm install langsmith-observability langchain/langsmith-observability --values langsmith_obs_config.yaml --version <version> -n <namespace> --wait --debug`

This will allow you to scrape metrics at the following service endpoints:

* Postgres: `langsmith-observability-postgres-exporter:9187/metrics`
* Redis: `langsmith-observability-redis-exporter:9121/metrics`
* Nginx: `langsmith-observability-nginx-exporter:9113/metrics`
* KubeStateMetrics: `langsmith-observability-kube-state-metrics:8080/metrics`

You should see the following if the installation went through:

```bash
Release "langsmith-observability" has been installed. Happy Helming!NAME: langsmith-observabilityLAST DEPLOYED: Wed Jun 25 11:17:34 2025NAMESPACE: langsmith-observabilitySTATUS: deployedREVISION: 1
```

And if you run `kubectl get pods -n langsmith-observability`, you should see:

```bash
langsmith-observability-kube-state-metrics-b58bb8db4-bm4g5        1/1     Running   0          2m22slangsmith-observability-nginx-exporter-6d686d9d4b-5qw9v           1/1     Running   0          2m22slangsmith-observability-postgres-exporter-67d5db5684-tffbm        1/1     Running   0          2m22slangsmith-observability-redis-exporter-846c4d65cb-vbtwd           1/1     Running   0          2m22s
```

# Section 2: Full observability stack

> [!WARNING]
>
> **This is not a production observability stack. Use this to gain quick insight into logs, metrics and traces for your deployment. This is only made to handle a few dozen GB of data per day.**

This section will show you how to deploy the end-to-end observability stack for LangSmith, using the [Helm Chart](https://github.com/langchain-ai/helm/tree/main/charts/langsmith-observability).

This chart is built around the open-source LGTM Stack from Grafana. It consists of:

* [Loki](https://grafana.com/docs/loki/latest/) for logs.
* [Mimir](https://grafana.com/docs/mimir/latest/) for metrics + alerting.
* [Tempo](https://grafana.com/docs/tempo/latest/) for traces.
* [Grafana](https://grafana.com/docs/grafana/latest/) for monitoring UI.

As well as [OpenTelemetry Collectors](https://opentelemetry.io/docs/collector/) for gathering the telemetry data.

## Prerequisites

### 1. Compute resources

The resource requests and limits for each part of the stack can be modified in the helm chart. Here are the current allocations (request/limit):

* Loki: `2vCPU/3vCPU + 2Gi/4Gi`
* Mimir: `1vCPU/2vCPU + 2Gi/4Gi`
* Tempo: `1vCPU/2vCPU + 4Gi/6Gi`

Make sure you have those resources allocated before bringing up the helm chart, or modify the resource values in your helm configuration file.

### 2. Cert-Manager

The helm chart uses the OpenTelemetry Operator to provision collectors. The operator require that you have [cert-manager](https://cert-manager.io/docs/installation/) installed in your Kubernetes cluster.

If you do not have it installed, you can run the following commands:

```bash
helm repo add jetstack https://charts.jetstack.iohelm repo updatehelm install cert-manager jetstack/cert-manager -n cert-manager --create-namespace
```

### 3. OpenTelemetry operator

Use the following to install the OpenTelemetry Operator:

```bash
helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-chartshelm repo updatehelm install opentelemetry-operator open-telemetry/opentelemetry-operator -n <namespace>
```

## Installation

The following instructions will bring up OTel collectors, the LGTM stack, Grafana and Prometheus exporters.

1. Create a local file called `langsmith_obs_config.yaml`
2. Copy over the values from this [file](https://github.com/langchain-ai/helm/blob/main/charts/langsmith-observability/examples/e2e-stack.yaml) into `langsmith_obs_config.yaml`, making sure to modify the values to match your LangSmith deployment.
3. Find the latest version of the chart by running `helm search repo langchain/langsmith-observability --versions`.
4. Grab the latest version number, and run `helm install langsmith-observability langchain/langsmith-observability --values langsmith_obs_config.yaml --version <version> -n <namespace> --wait --debug`

> [!NOTE]
>
> **You can selectively collect logs, metrics or traces by modifying the boolean values under `otelCollector` in your config file. You can also selectively bring up each respective piece of the backend (Loki, Mimir, Tempo).**

You should see the following if the install went through:

```bash
Release "langsmith-observability" has been installed. Happy Helming!NAME: langsmith-observabilityLAST DEPLOYED: Wed Jun 25 11:17:34 2025NAMESPACE: langsmith-observabilitySTATUS: deployedREVISION: 1
```

And if you run `kubectl get pods -n langsmith-observability`, you should see:

```bash
langsmith-observability-collector-gateway-collector-7746fb8pzbg   1/1     Running   0          5m26slangsmith-observability-grafana-7c6fc976f9-cdbvr                  1/1     Running   0          2m49slangsmith-observability-kube-state-metrics-b58bb8db4-bm4g5        1/1     Running   0          5m27slangsmith-observability-loki-0                                    2/2     Running   0          5m27slangsmith-observability-loki-chunks-cache-0                       2/2     Running   0          5m27slangsmith-observability-loki-gateway-769fb6fff8-zjsn5             1/1     Running   0          5m27slangsmith-observability-loki-results-cache-0                      2/2     Running   0          5m27slangsmith-observability-mimir-0                                   1/1     Running   0          5m26slangsmith-observability-nginx-exporter-6d686d9d4b-5qw9v           1/1     Running   0          5m27slangsmith-observability-postgres-exporter-67d5db5684-tffbm        1/1     Running   0          5m27slangsmith-observability-redis-exporter-846c4d65cb-vbtwd           1/1     Running   0          5m27slangsmith-observability-tempo-0                                   1/1     Running   0          5m27sopentelemetry-operator-756dff697-vblbn                            2/2     Running   0          12m
```

## Post-Installation

### Enable logs and traces in LangSmith

Once you have installed the observability helm chart, you need to set the following values in your *LangSmith* helm configuration file to enable collection of logs and traces.

```yaml
commonPodAnnotations:
  # E.g.: "langsmith-observability/langsmith-observability-collector-sidecar"
  sidecar.opentelemetry.io/inject: "${LANGSMITH_OBS_NAMESPACE}/${LANGSMITH_OTEL_CRD_NAME}"
observability:
  tracing:
    enabled: true
    # Replace this with the endpoint of your trace collector.
    # E.g.: "http://langsmith-observability-collector-gateway-collector.langsmith-observability.svc.cluster.local:4318/v1/traces"
    endpoint: "http://${GATEWAY_COLLECTOR_SERVICE_NAME}.${LANGSMITH_OBS_NAMESPACE}.svc.cluster.local:4318/v1/traces"
```

> [!NOTE]
>
> 1. To get `${LANGSMITH_OTEL_CRD_NAME}`, you can run `kubectl get opentelemetrycollectors -n ${LANGSMITH_OBS_NAMESPACE}` and select the name of the one with MODE = `sidecar`
> 2. To get `${GATEWAY_COLLECTOR_SERVICE_NAME}` name, run `kubectl get services -n ${LANGSMITH_OBS_NAMESPACE}` and select the one with Ports 4317/4318 AND a ClusterIP set. It should be something like `langsmith-observability-collector-gateway-collector`

Now run `helm upgrade langsmith langchain/langsmith --values langsmith_config.yaml --version <version> -n <langsmith-namespace> --wait --debug`, replacing `<version>` with the chart version you already run. Without `--version`, Helm upgrades to the latest chart, which can move the installation to a new major version.

Once upgraded, if you run `kubectl get pods -n <langsmith-namespace>` you should see the following (note the 2/2 for sidecar collectors):

```bash
langsmith-ace-backend-7dc85f7dff-xjbkj         2/2     Running     0               7m53slangsmith-backend-566b66979c-rgcfh             2/2     Running     1               7m53slangsmith-clickhouse-0                         2/2     Running     0               7m49slangsmith-frontend-7cf8549885-vpkns            2/2     Running     0               7m53slangsmith-platform-backend-5d46db7d9d-f6gh7    2/2     Running     0               7m52slangsmith-platform-backend-5d46db7d9d-lrr4d    2/2     Running     1               7m41slangsmith-platform-backend-5d46db7d9d-pcp27    2/2     Running     0               7m28slangsmith-playground-65d4c9699c-h656r          2/2     Running     0               7m52slangsmith-postgres-0                           2/2     Running     0               7m51slangsmith-queue-bdcd45bd6-htssd                2/2     Running     0               7m52slangsmith-queue-bdcd45bd6-pwdx4                2/2     Running     0               6m31slangsmith-queue-bdcd45bd6-xqrb8                2/2     Running     0               5m11slangsmith-redis-0                              2/2     Running     0               7m51s
```

## Grafana usage

Once everything is installed, do the following: to get your Grafana password:

```bash
kubectl get secret langsmith-observability-grafana -n <langsmith_observability_namespace> -o jsonpath="{.data.admin-password}" | base64 --decode
```

Then port-forward into the `langsmith-observability-grafana` container at port 3000, and open your browser as `localhost:3000`. Use the username `admin` and the password from the secret above to log into Grafana.

Once in Grafana, you can use the UI to monitor logs, metrics and traces. Grafana also comes pre-packaged with sets of dashboards for monitoring the main components of your deployment.

![LangSmith Grafana Dashboards](../../../../assets/images/7e79fca92eb3-langsmith-grafana-dashboards.png)

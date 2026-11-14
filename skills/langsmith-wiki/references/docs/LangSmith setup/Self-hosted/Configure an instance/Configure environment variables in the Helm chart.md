# Configure environment variables in the Helm chart

> How to use commonEnv and extraEnv to configure environment variables across LangSmith services in the Helm chart.

The LangSmith Helm chart provides two ways to inject environment variables into services: `commonEnv` and `extraEnv`. Understanding the difference between them helps you configure your deployment correctly and avoid runtime errors.

## commonEnv

`commonEnv` is a top-level field in `values.yaml` that applies to **all deployments and statefulsets except the `playground` and `aceBackend` services**, which are sandboxed and do not receive `commonEnv` values.

Use `commonEnv` when a variable must be available to most services simultaneously, such as custom CA certificate paths, proxy settings, or feature flags that affect the entire platform.

```yaml
commonEnv:
  - name: MY_ENV_VAR
    value: "my-value"
```

### Services that receive commonEnv

The following services receive `commonEnv`:

* `backend`
* `platformBackend`
* `queue`
* `ingestQueue`
* `frontend`
* `hostBackend`

### Services that do not receive commonEnv

The following services are sandboxed and do **not** receive `commonEnv`:

* `playground`
* `aceBackend`

To set environment variables on these services, use their `extraEnv` directly:

```yaml
playground:
  deployment:
    extraEnv:
      - name: MY_ENV_VAR
        value: "my-value"

aceBackend:
  deployment:
    extraEnv:
      - name: MY_ENV_VAR
        value: "my-value"
```

## extraEnv

`extraEnv` is a per-service field that adds environment variables to a specific service only. Each service that supports `extraEnv` exposes it under `<service>.deployment.extraEnv`.

Use `extraEnv` when a variable applies to one service only, or when you need to set a variable on `playground` or `aceBackend` that `commonEnv` does not reach.

```yaml
backend:
  deployment:
    extraEnv:
      - name: MY_BACKEND_VAR
        value: "backend-value"
```

## No duplicate variable names

The chart uses a `detectDuplicates` helper to validate environment variable names for each service. If the same variable name appears more than once in the combined list of variables for a service (including those added from `commonEnv`, `extraEnv`, and chart-managed variables), Helm fails during template rendering with an error like:

```
Duplicate keys detected: [MY_ENV_VAR]
```

To resolve this, remove the duplicate from either `commonEnv` or the service's `extraEnv` so each variable name appears exactly once per service.

> [!WARNING]
>
> Chart-managed variables (set internally by the Helm chart) count toward duplicate detection. Do not add a variable name to `commonEnv` or `extraEnv` if the chart already manages that variable. Review the [chart values file](https://github.com/langchain-ai/helm/blob/main/charts/langsmith/values.yaml) to see which variables the chart sets by default.

## Example: set a variable on most services but override it on one

To use a common value for most services while overriding it for a specific service, set it in `commonEnv` and add the override to that service's `extraEnv`. Because `playground` and `aceBackend` do not receive `commonEnv`, you must always set variables for those services through their own `extraEnv`.

```yaml
# Apply to all services that receive commonEnv
commonEnv:
  - name: SSRF_ALLOW_K8S_INTERNAL
    value: "true"

# playground does not receive commonEnv — set it directly
playground:
  deployment:
    extraEnv:
      - name: SSRF_ALLOW_K8S_INTERNAL
        value: "true"
      - name: SSRF_ALLOW_PRIVATE_IPS_PLAYGROUND
        value: "true"
```

## Common feature flags

### Reduce batched-run persistence logging

By default, LangSmith logs a success message for every batch of runs it persists via the Go-based ingest queue. On deployments that process a high volume of traces, this can produce excessive log noise.

`FF_PERSIST_BATCHED_RUNS_SUCCESS_LOGGING` defaults to `true` and is injected into all services via `commonEnv` when `ingestQueue.enabled` is `true` (the default). To disable these success log messages, override it in `commonEnv`:

```yaml
commonEnv:
  - name: FF_PERSIST_BATCHED_RUNS_SUCCESS_LOGGING
    value: "false"
```

> [!NOTE]
>
> Setting this flag to `false` suppresses per-batch success messages only. Errors are still logged.

## Related pages

* [Configure LangSmith for scale](Configure%20LangSmith%20for%20scale.md)
* [Playground environment settings](Use%20environment%20variables%20for%20model%20providers.md)
* [LangSmith Helm chart values.yaml](https://github.com/langchain-ai/helm/blob/main/charts/langsmith/values.yaml)

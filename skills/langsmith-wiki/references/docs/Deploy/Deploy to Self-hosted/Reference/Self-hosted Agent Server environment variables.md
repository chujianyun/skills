# Self-hosted Agent Server environment variables

> Environment variables supported by the LangSmith Agent Server when deployed on self-hosted infrastructure.

The Agent Server supports the following environment variables when deployed on [self-hosted](../Deploy%20to%20self-hosted.md) infrastructure. For variables specific to Cloud deployments, see [Cloud Agent Server environment variables](../../Deploy%20to%20Cloud/Reference/Cloud%20Agent%20Server%20environment%20variables.md).

## `BG_JOB_ISOLATED_LOOPS`

Set `BG_JOB_ISOLATED_LOOPS` to `True` to execute background runs in an isolated event loop separate from the serving API event loop.

> [!WARNING]
>
> Enabling this flag does not remove the underlying problem. It moves synchronous blocking work off the serving API's event loop so health checks stop failing, but the blocking code continues to run on the background loop and **will** continue to cause issues in production, like degraded throughput, tail-latency spikes, starved workers, or connection pool exhaustion (see the pool-size caveat below), and poor scaling under load.
>
> To properly resolve those issues, use native async drivers and async code throughout your agent. That means async HTTP clients like `httpx` or `aiohttp` (though we recommend caching the clients to avoid CPU overhead loading the SSL context), async database drivers like `asyncpg` or `psycopg[async]`, and async model SDK's. For unavoidable synchronous libraries, wrap the specific call in `asyncio.to_thread(...)` or `loop.run_in_executor(...)` instead of enabling this flag for the whole deployment.

This environment variable should be set to `True` if the implementation of a graph/node contains synchronous code. In this situation, the synchronous code will block the serving API event loop, which may cause the API to be unavailable. A symptom of an unavailable API is continuous application restarts due to failing health checks.

> [!WARNING]
>
> When `BG_JOB_ISOLATED_LOOPS` is enabled, each background worker runs in its own thread with a **separate Postgres connection pool**. The per-worker pool size is `LANGGRAPH_POSTGRES_POOL_MAX_SIZE // N_JOBS_PER_WORKER`. For example, with `LANGGRAPH_POSTGRES_POOL_MAX_SIZE=20` and `N_JOBS_PER_WORKER=15`, each worker gets a pool of only 1 connection. Small per-worker pools are more susceptible to connection failures because a single stale connection represents a large fraction of the pool. If you enable isolated loops, ensure `LANGGRAPH_POSTGRES_POOL_MAX_SIZE` is large enough to provide at least a few connections per worker.

Defaults to `False`.

## `BG_JOB_MAX_RETRIES`

Maximum number of times a background run will be retried after a retriable failure (e.g. transient database errors, server shutdown cancellations). When a run fails with a retriable error, it is placed back in the queue and resumed from the last checkpointed step. If the run exceeds the maximum number of retries, it is marked as failed.

Defaults to `3`.

## `BG_JOB_SHUTDOWN_GRACE_PERIOD_SECS`

Specifies, in seconds, how long the server will wait for background jobs to finish after the queue receives a shutdown signal. After this period, the server will force termination. Defaults to `180` seconds. The maximum value is `3600` seconds. Set this to ensure jobs have enough time to complete cleanly during shutdown. Added in `langgraph-api==0.2.16`.

## `BG_JOB_TIMEOUT_SECS`

The timeout of a background run can be increased. However, the infrastructure for a Cloud deployment enforces a 1 hour timeout limit for API requests. This means the connection between client and server will timeout after 1 hour. This is not configurable.

A background run can execute for longer than 1 hour, but a client must reconnect to the server (e.g. join stream via `POST /threads/{thread_id}/runs/{run_id}/stream`) to retrieve output from the run if the run is taking longer than 1 hour.

Defaults to `86400`.

## `CORS_ALLOW_ORIGINS`

Set `CORS_ALLOW_ORIGINS` to specify allowed origins.

* Example for allowing a single origin: `CORS_ALLOW_ORIGINS=https://example.com`
* Example for allowing multiple origins: `CORS_ALLOW_ORIGINS=https://example.com,https://app.example.com`

For advanced CORS configuration, see [how to add custom CORS configuration](../../Get%20started/Reference/LangGraph%20CLI.md#customizing-http-middleware-and-headers).

Defaults to `*` (all origins).

## `DEFAULT_A2A_ASSISTANT_ID`

Set `DEFAULT_A2A_ASSISTANT_ID` to the ID of the assistant whose [agent card](../../Agent%20Server/Capabilities/A2A%20endpoint%20in%20Agent%20Server.md#agent-card-discovery) the server returns from `/.well-known/agent-card.json` when the request has no `assistant_id` query parameter.

If it is not set, requests to `/.well-known/agent-card.json` without an `assistant_id` query parameter return a `400` error. The `/a2a/{assistant_id}` endpoints take the assistant ID from the path and ignore this variable.

## Supported Datadog environment variables

Set these environment variables or secrets on the deployment to send Agent Server traces and logs to Datadog. Every variable takes effect only when `DD_API_KEY` is set, which wraps the application process in Datadog's [`ddtrace-run`](https://ddtrace.readthedocs.io/en/stable/installation_quickstart.html) tracer and log-collection agent.

* **`DD_API_KEY`**: Your [Datadog API key](https://docs.datadoghq.com/account_management/api-app-keys/). Required. Sending any traces or logs to Datadog requires it.
* **`DD_LOGS_ENABLED`**: Set to `true` to forward Agent Server logs to Datadog. Omit it or set it to `false` to disable log forwarding.
* **`DD_LOGS_INJECTION`**: Set to `true` to add trace and span identifiers to logs so that logs correlate with traces.
* **`DD_TRACE_ENABLED`**: Controls Datadog trace collection. Set to `true` to collect traces or `false` to disable it.
* **`DD_SITE`**: The Datadog site to send data to, such as `datadoghq.com` or `datadoghq.eu`. Defaults to `datadoghq.com`.
* **`DD_ENV`**: The environment name applied to traces and logs, such as `production`.
* **`DD_SERVICE`**: The service name applied to traces and logs.
* **`DD_TRACE_DEBUG`**: Set to `true` to enable debug logging in the `ddtrace` tracer when troubleshooting.
* **`DD_LOG_LEVEL`**: The Datadog Agent log level, such as `debug`, when troubleshooting.

For the full set of tracing options, see the [`DD_*` environment variables](https://ddtrace.readthedocs.io/en/stable/configuration.html) reference.

> [!NOTE]
>
> Enabling `DD_API_KEY` (and thus `ddtrace-run`) can override or interfere with other auto-instrumentation solutions (such as OpenTelemetry) that you may have instrumented into your application code.

## `FF_OPTIMIZED_STREAMING`

Controls how API servers read streaming run output from Redis. When enabled, they read it from Redis Streams. When disabled, they read it through Redis Pub/Sub.

> [!NOTE]
>
> `FF_OPTIMIZED_STREAMING` requires Agent Server v0.7.93 or later. Storing every run's events and the `true` default first ship in the v0.19.0 release candidates, starting with v0.19.0rc1.

From Agent Server v0.19.0rc1, the server stores the streaming events of every run in Redis Streams, whatever the value of `FF_OPTIMIZED_STREAMING`. A client can resume the stream of any run, not only of runs created with `stream_resumable=True`. [`RESUMABLE_STREAM_TTL_SECONDS`](#resumable_stream_ttl_seconds) sets how long Redis keeps the events. To size Redis memory for them, see [Size Redis memory for streaming](../Configure/Configure%20Agent%20Server%20for%20scale.md#size-redis-memory-for-streaming).

Set `FF_OPTIMIZED_STREAMING=false` to keep reading through Redis Pub/Sub. Change the value in its own deploy, once the deployment runs v0.19.0rc1 or later. If one deploy both upgrades from an earlier version and changes the value, open streams can miss live events from the replicas still on the earlier version until clients reconnect. With Redis Cluster, if the variable is set to `true`, remove it in one deploy, then set it to `false` in the next. In cluster mode, a server where the variable is explicitly `true` sends no live Pub/Sub events, so readers on servers with the flag off miss its events until they reconnect.

In earlier versions, the server stores events only for resumable runs while the flag is disabled. Non-resumable runs started before you enable the flag continue to stream through Redis Pub/Sub.

Accepts boolean values `true` and `false`. Defaults to `true` from Agent Server v0.19.0rc1, and to `false` in earlier versions.

## `FF_PROFILE_IMPORTS`

Set `FF_PROFILE_IMPORTS` to `true` to find out why a graph is slow to load. Defaults to `false`. Added in `langgraph-api==0.6.8`.

Agent Server runs your graph code when it imports your graph modules at startup, so work that happens at import time delays readiness. Examples include network calls, database or client setup, reading large files, and heavy dependency imports. When a graph import takes longer than 3 seconds, the server logs a warning that suggests setting this variable.

With the variable set, the server profiles the import of each Python module it loads from your configuration. This covers your graphs, custom app, auth handler, store, checkpointer, and encryption module. If any function inside an import takes at least 1 second, the server logs a `slow_import_profile` warning that lists up to 10 of the slowest. Each entry shows the function, its cumulative time, and where in your module it was called from. The report has the following format, with illustrative values:

```text
Slow startup for './agent.py:graph' (12.3s)

    Slowest operations:
       10.84s  connect_to_database      clients/db.py:42
               ↳ from agent.py (module-level)
```

The report identifies the slow operation, so you can move it inside a function or initialize it lazily instead of running it at import time.

Keep the following in mind:

* Profiling adds overhead, so the reported times run higher than normal. Remove the variable once you've fixed the problem.
* Calls made at the top level of a module are attributed to `(module-level)` with no line number.
* Operations that take less than 1 second each don't appear in the report, even when many of them add up to a slow import.
* Import profiling works for Python graphs only. JavaScript graphs aren't supported yet.
* Only import time is profiled. Delays after your graph is imported, such as in your custom app lifespan, don't appear.

## `LANGGRAPH_AES_KEY` and `LANGGRAPH_AES_JSON_KEYS`

Set `LANGGRAPH_AES_KEY` to a 16, 24, or 32-byte key to encrypt checkpoints at rest. Set `LANGGRAPH_AES_JSON_KEYS` to a comma-separated list of JSON keys to also encrypt wherever they appear in thread, assistant, run, cron, and store data. `LANGGRAPH_AES_JSON_KEYS` requires `LANGGRAPH_AES_KEY`.

For setup and key rotation, see [Configure AES encryption at rest](../../Agent%20Server/Server%20customization/Encryption%20at%20rest/Configure%20AES%20encryption%20at%20rest.md).

## `LANGGRAPH_API_URL`

Set `LANGGRAPH_API_URL` to the URL that clients use to reach the deployment. The server uses it as:

* The base URL in [A2A agent cards](../../Agent%20Server/Capabilities/A2A%20endpoint%20in%20Agent%20Server.md#agent-card-discovery).
* The `servers` entry in the OpenAPI spec served at `/openapi.json`.
* The `langgraph_api_url` key in each run's metadata.

If it is not set, the server builds agent card URLs from the incoming request. Set it when clients reach the server through a different host, such as a reverse proxy.

## `LANGGRAPH_DEFAULT_RECURSION_LIMIT`

Set `LANGGRAPH_DEFAULT_RECURSION_LIMIT` to the default [recursion limit](https://docs.langchain.com/oss/python/langgraph/graph-api.md#recursion-limit) for runs: the maximum number of supersteps a graph executes before it raises an error. A `recursion_limit` passed in a run's config overrides it.

Defaults to `10011`.

## `LANGGRAPH_POSTGRES_POOL_MAX_SIZE`

Beginning with langgraph-api version `0.2.12`, the maximum size of the Postgres connection pool (per replica) can be controlled using the `LANGGRAPH_POSTGRES_POOL_MAX_SIZE` environment variable. By setting this variable, you can determine the upper bound on the number of simultaneous connections the server will establish with the Postgres database.

For example, if a deployment is scaled up to 10 replicas and `LANGGRAPH_POSTGRES_POOL_MAX_SIZE` is configured to `150`, then up to `1500` connections to Postgres can be established. This is particularly useful for deployments where database resources are limited (or more available) or where you need to tune connection behavior for performance or scaling reasons.

When [`BG_JOB_ISOLATED_LOOPS`](#bg_job_isolated_loops) is enabled, the pool is not shared. Instead, each background worker thread creates its own pool with a maximum size of `LANGGRAPH_POSTGRES_POOL_MAX_SIZE / N_JOBS_PER_WORKER`. Keep this in mind when lowering the pool size. A value that works well for a shared pool may result in very small per-worker pools under isolated loops.

Defaults to `150` connections.

## `LANGGRAPH_THREAD_HISTORY_MAX_STATE_BYTES`

Maximum size, in bytes, of a single [thread history](../../Get%20started/Reference/Agent%20Server%20API/Threads/Get%20Thread%20History.md) response. Each history entry contains the full thread state, so requesting many entries from a large thread can use a large amount of server memory.

If the next state would push the response over this limit, the server returns the states it has so far, which can be fewer than `limit`. The most recent state is always included, even if it alone is larger than the limit. To read older states, page with `before`.

The limit applies to the JSON-encoded response. The server stops reading checkpoints once it reaches the limit, so this also limits how much memory a history request uses. A negative value prevents the server from starting. Available in `langgraph-api>=0.17.0`.

Defaults to `0`, which means no limit.

## `LS_CHECKPOINT_DELETE`

JSON-valued configuration for deferred checkpoint deletion. When enabled, thread delete and prune operations enqueue checkpoints for background deletion instead of deleting synchronously, moving the I/O off the request hot path. Available in `langgraph-api>=0.8.1`.

> [!NOTE]
>
> Only supported with the default PostgreSQL checkpointer backend. Deferred deletes will become the default in a future release.

Accepted fields:

* `enabled` (boolean, default `false`): When `true`, thread delete and prune operations enqueue checkpoints into `checkpoint_delete_queue` and return immediately, and the background worker drains the queue.
* `enabledWorkerOnly` (boolean, default `false`): Runs only the background drain worker without enqueuing new entries. Use this to finish draining the queue after rolling `enabled` back to `false`.
* `pollIntervalMs` (integer, default `5000`): How often the worker polls the queue, in milliseconds.
* `batchSize` (integer, default `25`): Number of checkpoint entries the worker dequeues per transaction. Smaller values spread I/O over more time at the cost of longer drain latency.
* `batchSleepMs` (integer, default `500`): How long the worker sleeps between batches when the queue is non-empty, in milliseconds.

Example: `LS_CHECKPOINT_DELETE='{"enabled":true,"batchSize":10,"pollIntervalMs":1000}'`.

Defaults to disabled (synchronous checkpoint deletion).

## `LS_DEFAULT_CHECKPOINTER_BACKEND`

Sets the default [checkpointer backend](../../Agent%20Server/Develop%20your%20application/Persistence/Configure%20checkpointer%20backend.md) for agent servers that don't specify one in `langgraph.json`. Accepted values: `"default"` (PostgreSQL), `"mongo"`, `"custom"`.

If the application's `langgraph.json` includes a `checkpointer.backend` value, it takes precedence over this variable.

When set to `"mongo"`, you must also provide the MongoDB connection URI via [`LS_MONGODB_URI`](#ls_mongodb_uri).

## `LANGSMITH_TRACING`

Set `LANGSMITH_TRACING` to `false` to disable tracing to LangSmith.

> [!NOTE]
>
> For selective tracing control based on runtime conditions (such as per-client requirements or data sensitivity), see [Conditional tracing](../../../Monitor/Trace/Configuration%20%26%20troubleshooting/Agent%20%26%20environment%20settings/Conditional%20tracing.md).

Defaults to `true`.

## `LOG_COLOR`

This is mainly relevant in the context of using the dev server via the `langgraph dev` command. Set `LOG_COLOR` to `true` to enable ANSI-colored console output when using the default console renderer. Disabling color output by setting this variable to `false` produces monochrome logs. Defaults to `true`.

## `LOG_LEVEL`

Configure [log level](https://docs.python.org/3/library/logging.html#logging-levels). Defaults to `INFO`.

## `LOG_JSON`

Set `LOG_JSON` to `true` to render all log messages as JSON objects using the configured `JSONRenderer`. This produces structured logs that can be easily parsed or ingested by log management systems. Defaults to `false`.

## `N_JOBS_PER_WORKER`

Maximum number of runs a single queue worker executes concurrently from the Agent Server task queue. Defaults to `10`.

This limits concurrent run execution, not the number of API requests your deployment can serve. Request-serving capacity is handled by API servers and scales independently of this value. For tuning guidance, see [Configure Agent Server for scale](../Configure/Configure%20Agent%20Server%20for%20scale.md).

## `LS_APM_OTEL_ENABLED`

To configure OpenTelemetry APM tracing for your deployment, set `LS_APM_OTEL_ENABLED` to `true` and `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT` or `OTEL_EXPORTER_OTLP_ENDPOINT` to the target trace ingestion endpoint. Note that both `LS_APM_OTEL_ENABLED` and one of the other two export endpoints are required to activate OpenTelemetry APM tracing in server versions later than `0.7.17`.

Specify other [`OTEL_*` environment variables](https://opentelemetry.io/docs/collector/configuration/) to configure tracing, logging, and other instrumentation.

```shell
# If you set LS_APM_OTEL_ENABLED AND (OTEL_EXPORTER_OTLP_TRACES_ENDPOINT or OTEL_EXPORTER_OTLP_ENDPOINT),
# the server starts with OpenTelemetry instrumentation enabled.
LS_APM_OTEL_ENABLED=true
OTEL_EXPORTER_OTLP_TRACES_ENDPOINT=<target trace ingestion endpoint>
OTEL_EXPORTER_OTLP_ENDPOINT=https://otlp.nr-data.net
OTEL_SERVICE_NAME=MY_LANGSMITH_DEPLOYMENT
OTEL_EXPORTER_OTLP_HEADERS=api-key=<YOUR_INGEST_LICENSE_KEY>
LANGSMITH_OTEL_ENABLED=true
# Common OTEL settings
OTEL_ATTRIBUTE_VALUE_LENGTH_LIMIT=4095
OTEL_EXPORTER_OTLP_COMPRESSION=gzip
OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE=delta
OTEL_PYTHON_EXCLUDED_URLS=/metrics,/ok,/info
# Optional: OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
```

For example, to submit OpenTelemetry traces to [New Relic's US region](https://docs.newrelic.com/docs/opentelemetry/best-practices/opentelemetry-otlp/), set the following:

```shell
LS_APM_OTEL_ENABLED=true
OTEL_EXPORTER_OTLP_TRACES_ENDPOINT=https://otlp.nr-data.net/v1/traces
OTEL_EXPORTER_OTLP_ENDPOINT=https://otlp.nr-data.net
OTEL_EXPORTER_OTLP_HEADERS=api-key=<YOUR_INGEST_LICENSE_KEY>
```

> [!NOTE]
>
> OTel APM tracing was added in Agent Server version `0.5.32` and is currently in Alpha.

## `LS_MONGODB_URI`

MongoDB connection URI for the MongoDB checkpointer backend. If `LS_MONGODB_URI` is not set, the server reads `MONGODB_URI`.

The URI must point to a replica set member or `mongos` router and must include the database name in the path.

See [Configure checkpointer backend](../../Agent%20Server/Develop%20your%20application/Persistence/Configure%20checkpointer%20backend.md) for details.

## `LSD_CACHE_PACKAGES_DISTRIBUTIONS`

When `LSD_CACHE_PACKAGES_DISTRIBUTIONS` is `true`, the server caches the result of `importlib.metadata.packages_distributions()` once per process. Some packages call that function many times at import time, which slows graph loading, especially when Datadog tracing (`ddtrace`) is enabled. Set it to `false` if your deployment installs or removes packages at runtime.

Defaults to `true`.

## `REDIS_KEY_PREFIX`

> [!NOTE]
>
> **Available in API Server version 0.1.9+**
> This environment variable is supported in API Server version 0.1.9 and above.

Specify a prefix for Redis keys. This allows multiple Agent Server instances to share the same Redis instance by using different key prefixes.

Defaults to `''`.

## `REDIS_URI_CUSTOM`

> [!NOTE]
>
> **Only for Hybrid and Self-Hosted**
> Custom Redis instances are only available for [Hybrid](../Hybrid.md) and [Self-Hosted](../../../LangSmith%20setup/Self-hosted/Self-hosted%20LangSmith.md) deployments.

Specify `REDIS_URI_CUSTOM` to use a custom Redis instance. The value of `REDIS_URI_CUSTOM` must be a valid [Redis connection URI](https://redis.readthedocs.io/en/stable/connections.html#redis.Redis.from_url).

## `REDIS_MAX_CONNECTIONS`

The maximum size of the Redis connection pools (per replica) can be controlled using the `REDIS_MAX_CONNECTIONS` environment variable. It sizes both the Go core's pool and the Python server's pool. These pools do not hold every connection a replica opens to Redis. For example, with [`FF_OPTIMIZED_STREAMING`](#ff_optimized_streaming) enabled, stream reads use a separate pool sized by [`REDIS_STREAM_READ_MAX_CONNECTIONS`](#redis_stream_read_max_connections).

Defaults to `500` for the Go core and `2000` for the Python server.

## `REDIS_STREAM_READ_MAX_CONNECTIONS`

`REDIS_STREAM_READ_MAX_CONNECTIONS` sets the maximum size of the Redis connection pool that each replica uses to read streams. It applies only when [`FF_OPTIMIZED_STREAMING`](#ff_optimized_streaming) is enabled. Each open stream takes a connection from this pool while it waits for events. Available in Agent Server v0.19.0rc1 and later.

This pool is separate from [`REDIS_MAX_CONNECTIONS`](#redis_max_connections). With `FF_OPTIMIZED_STREAMING` enabled, each replica can open up to `REDIS_STREAM_READ_MAX_CONNECTIONS` Redis connections on top of those pools.

If a replica has more open streams than the pool has connections, streams wait for a free connection and their events arrive late. Raise the value when that happens, as long as the Redis `maxclients` limit has room for the extra connections from every replica.

Defaults to `2000`.

## `RESUMABLE_STREAM_TTL_SECONDS`

Time-to-live in seconds for resumable stream data in Redis.

When a run is created and the output is streamed, the stream can be configured to be resumable (e.g. `stream_resumable=True`). If a stream is resumable, output from the stream is temporarily stored in Redis. The TTL for this data can be configured by setting `RESUMABLE_STREAM_TTL_SECONDS`.

From Agent Server v0.19.0rc1, the server stores the streaming output of every run, resumable or not. Each new event on a thread trims the thread's events that are older than `RESUMABLE_STREAM_TTL_SECONDS`, and the remaining events expire `RESUMABLE_STREAM_TTL_SECONDS` after the thread's most recent event.

See the [Python](https://reference.langchain.com/python/langsmith/deployment/sdk/#langgraph_sdk.client.RunsClient.stream) and [JS/TS](https://reference.langchain.com/javascript/langchain-langgraph-sdk/client/RunsClient) SDKs for more details on how to implement resumable streams.

Defaults to `120` seconds.

> [!NOTE]
>
> Setting a very high value for `RESUMABLE_STREAM_TTL_SECONDS` can result in substantial Redis memory usage when there are many concurrent runs with large or frequent streaming output. Set this value to the minimum value to enable recovery during network interruptions and prefer checkpointing for long term durability and execution snapshotting.
> To size Redis memory for the stored events, see [Size Redis memory for streaming](../Configure/Configure%20Agent%20Server%20for%20scale.md#size-redis-memory-for-streaming).

## `AGENT_POSTGRES_IAM_AUTH_PROVIDER`

Set `AGENT_POSTGRES_IAM_AUTH_PROVIDER` to `aws`, `azure`, or `gcp` to replace the password in the PostgreSQL connection URI with a short-lived cloud identity token. Requires `langgraph-api>=0.12.0`.

For provider prerequisites and connection URI requirements, see [Configure IAM authentication for data stores](../../Agent%20Server/Server%20customization/Configure%20IAM%20authentication%20for%20data%20stores.md).

## `AGENT_REDIS_IAM_AUTH_PROVIDER`

Set `AGENT_REDIS_IAM_AUTH_PROVIDER` to `aws`, `azure`, or `gcp` to authenticate Redis connections with a short-lived cloud identity token. Requires `langgraph-api>=0.12.0`.

For provider prerequisites and connection URI requirements, see [Configure IAM authentication for data stores](../../Agent%20Server/Server%20customization/Configure%20IAM%20authentication%20for%20data%20stores.md).

## `LANGGRAPH_SERVER_HOST`

Set `LANGGRAPH_SERVER_HOST` to control which address families the Agent Server listens on:

* **Empty string**: Listen on both IPv4 and IPv6. This is the default as of `langgraph-api>=0.14.0`.
* **`0.0.0.0`**: Listen on IPv4 only.
* **`::`**: Listen on IPv6 only.

Versions before `langgraph-api` 0.14.0 default to `0.0.0.0`, which listens on IPv4 only.

## `LANGSMITH_API_KEY`

To send traces to a self-hosted LangSmith instance, set `LANGSMITH_API_KEY` to an API key created from the self-hosted instance.

## `LANGSMITH_ENDPOINT`

To send traces to a self-hosted LangSmith instance, set `LANGSMITH_ENDPOINT` to the hostname of the self-hosted instance.

## `MOUNT_PREFIX`

Set `MOUNT_PREFIX` to serve the Agent Server under a specific path prefix. This is useful for deployments where the server is behind a reverse proxy or load balancer that requires a specific path prefix.

For example, if the server is to be served under `https://example.com/langgraph`, set `MOUNT_PREFIX` to `/langgraph`.

## `POSTGRES_URI_CUSTOM`

Specify `POSTGRES_URI_CUSTOM` to use a custom Postgres instance. The value of `POSTGRES_URI_CUSTOM` must be a valid [Postgres connection URI](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING-URIS).

Postgres:

* Version 15.8 or higher.
* An initial database must be present and the connection URI must reference the database.

Control Plane Functionality:

* If `POSTGRES_URI_CUSTOM` is specified, the control plane will not provision a database for the server.
* If `POSTGRES_URI_CUSTOM` is removed, the control plane will not provision a database for the server and will not delete the externally managed Postgres instance.
* If `POSTGRES_URI_CUSTOM` is removed, deployment of the revision will not succeed. Once `POSTGRES_URI_CUSTOM` is specified, it must always be set for the lifecycle of the deployment.
* If the deployment is deleted, the control plane will not delete the externally managed Postgres instance.
* The value of `POSTGRES_URI_CUSTOM` can be updated. For example, a password in the URI can be updated.

Database Connectivity:

* The custom Postgres instance must be accessible by the Agent Server. The user is responsible for ensuring connectivity.

## `REDIS_CLUSTER`

> [!WARNING]
>
> This feature is in Alpha.

Set `REDIS_CLUSTER` to `True` to enable Redis Cluster mode. When enabled, the system will connect to Redis using cluster mode. This is useful when connecting to a Redis Cluster deployment.

Defaults to `False`.

## `REDIS_URI_CUSTOM`

Specify `REDIS_URI_CUSTOM` to use a custom Redis instance. The value of `REDIS_URI_CUSTOM` must be a valid [Redis connection URI](https://redis.readthedocs.io/en/stable/connections.html#redis.Redis.from_url).

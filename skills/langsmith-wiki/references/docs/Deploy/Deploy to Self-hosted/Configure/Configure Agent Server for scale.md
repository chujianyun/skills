# Configure Agent Server for scale

> Tune the Agent Server for self-hosted deployments—write load, read load, and example Helm configurations for different load patterns.

The default configuration for the LangSmith Agent Server is designed to handle substantial read and write load across a variety of different workloads. By following the best practices outlined below, you can tune your Agent Server to perform optimally for your specific workload. This page describes scaling considerations for the Agent Server on self-hosted deployments and provides example configurations.

This page covers the Agent Server, which runs your deployed agents. To scale the self-hosted LangSmith instance that ingests traces and runs evaluations, see [Configure LangSmith for scale](../../../LangSmith%20setup/Self-hosted/Configure%20an%20instance/Configure%20LangSmith%20for%20scale.md).

> [!TIP]
>
> If you're not yet familiar with how API servers and queue workers operate at the container level, read the [runtime architecture](../../Agent%20Server/Capabilities/Agent%20Server.md#runtime-architecture) overview first.

For [Cloud](../../Deploy%20to%20Cloud/Cloud%20platform%20features.md#scaling), the platform autoscales automatically and the Helm configurations below do not apply.

## Request vs. run concurrency

Two independent kinds of concurrency determine how the Agent Server scales, and they are controlled separately:

* **Request concurrency** is how many API requests (creating runs, reading thread state, streaming results) the deployment serves at once. API servers handle requests asynchronously, and request concurrency scales horizontally with the number of API server replicas.
* **Run concurrency** is how many runs execute at once. A single queue worker executes up to [`N_JOBS_PER_WORKER`](../Reference/Self-hosted%20Agent%20Server%20environment%20variables.md) runs concurrently (default 10). Run concurrency is capped at the number of queue workers multiplied by `N_JOBS_PER_WORKER`.

Creating a run is a fast write request: the API server persists a pending run and returns immediately, without waiting for the run to execute. If every run slot is busy, additional runs wait in the [queue](../../Agent%20Server/Capabilities/Agent%20Server.md#run-execution-lifecycle) until a slot frees. Raising `N_JOBS_PER_WORKER` or adding queue workers increases run throughput; it does not change how many requests the deployment can serve concurrently.

## Write load

Write load is primarily driven by the following factors:

* Creation of new [runs](../../Agent%20Server/Capabilities/Runs/How%20to%20kick%20off%20background%20runs.md)
* Creation of new checkpoints during run execution
* Writing to long term memory
* Creation of new [threads](../../Agent%20Server/Capabilities/Use%20threads.md)
* Creation of new [assistants](../../Agent%20Server/Capabilities/Assistants/Assistants.md)
* Deletion of runs, checkpoints, threads, assistants and cron jobs

The following components are primarily responsible for handling write load:

* API server: Handles initial request and persistence of data to the database.
* Queue worker: Handles the execution of runs.
* Redis: Handles the storage of ephemeral data about on-going runs.
* Postgres: Handles the storage of all data, including run, thread, assistant, cron job, checkpointing and long term memory.

### Tune `N_JOBS_PER_WORKER` based on assistant characteristics

The default value of [`N_JOBS_PER_WORKER`](../Reference/Self-hosted%20Agent%20Server%20environment%20variables.md) is 10. You can change this value to scale the maximum number of runs that can be executed at a time by a single queue worker based on the characteristics of your assistant.

Some general guidelines for changing `N_JOBS_PER_WORKER`:

* If your assistant is CPU bounded, the default value of 10 is likely sufficient. You might lower `N_JOBS_PER_WORKER` if you notice excessive CPU usage on queue workers or delays in run execution.
* If your assistant is memory bounded, or queue workers are approaching memory limits, lower `N_JOBS_PER_WORKER` to reduce the number of concurrent runs per worker.
* If your assistant is IO bounded, increase `N_JOBS_PER_WORKER` to handle more concurrent runs per worker.

There is no upper limit to `N_JOBS_PER_WORKER`. However, queue workers are greedy when fetching new runs, which means they will try to pick up as many runs as they have available jobs and begin executing them immediately. Setting `N_JOBS_PER_WORKER` too high in environments with bursty traffic can lead to uneven worker utilization, increased run execution times, and high memory usage on queue workers.

### Avoid synchronous blocking operations

Avoid synchronous blocking operations in your code and prefer asynchronous operations. Long synchronous operations can block the main event loop, causing longer request and run execution times and potential timeouts.

For example, consider an application that needs to sleep for 1 second. Instead of using synchronous code like this:

```python
import time

def my_function():
    time.sleep(1)
```

Prefer asynchronous code like this:

```python
import asyncio

async def my_function():
    await asyncio.sleep(1)
```

If an assistant requires synchronous blocking operations, run those in `asyncio.to_thread()` or equivalent.

### Minimize redundant checkpointing

Minimize redundant checkpointing by setting [`durability`](https://docs.langchain.com/oss/python/langgraph/checkpointers#durability-modes) to the minimum value necessary to ensure your data is durable.

The default durability mode is `"async"`, meaning checkpoints are written after each step asynchronously. If an assistant needs to persist only the final state of the run, `durability` can be set to `"exit"`, storing only the final state of the run. This can be set when creating the run:

```python
from langgraph_sdk import get_client

client = get_client(url=<DEPLOYMENT_URL>)
thread = await client.threads.create()
run = await client.runs.create(
    thread_id=thread["thread_id"],
    assistant_id="agent",
    durability="exit"
)
```

### Enable queue workers

By default, the API server manages the queue and does not use queue workers. Enable queue workers by setting `queue.enabled` to `true`:

```yaml
queue:
  enabled: true
```

This offloads queue management from the API server to dedicated queue workers, reducing load on the API server and allowing it to focus on handling requests.

### Size jobs for expected throughput

This section sizes run-execution capacity (queue workers), which is separate from request-serving capacity (API server replicas). For more information, see [Request vs. run concurrency](#request-vs-run-concurrency).

The more runs you execute in parallel, the more jobs you will need to handle the load. There are two main parameters to scale the available jobs:

* `number_of_queue_workers`: The number of queue workers provisioned.
* `N_JOBS_PER_WORKER`: The number of runs that a single queue worker can execute at a time. Defaults to 10.

You can calculate the available jobs with the following equation:

```
available_jobs = number_of_queue_workers * N_JOBS_PER_WORKER
```

Throughput is then the number of runs that can be executed per second by the available jobs:

```
throughput_per_second = available_jobs / average_run_execution_time_seconds
```

Therefore, the minimum number of queue workers you should provision to support your expected steady state throughput is:

```
number_of_queue_workers = throughput_per_second * average_run_execution_time_seconds / N_JOBS_PER_WORKER
```

### Configure autoscaling for bursty write workloads

Autoscaling is disabled by default, but should be configured for bursty workloads. Using the same calculations as the previous section, you can determine the maximum number of queue workers you should allow the autoscaler to scale to based on maximum expected throughput.

### Size Redis memory for streaming

From Agent Server v0.19.0rc1, Redis stores the streaming events of every run, so its memory grows with how much your runs stream. Each new event on a thread trims the thread's events that are older than [`RESUMABLE_STREAM_TTL_SECONDS`](../../Deploy%20to%20Cloud/Reference/Cloud%20Agent%20Server%20environment%20variables.md#resumable_stream_ttl_seconds), `120` seconds by default. The remaining events expire `RESUMABLE_STREAM_TTL_SECONDS` after the thread's most recent event, so an event stays in Redis for at most twice the TTL.

Redis needs at least the following memory for stored events:

```
stream_memory_bytes = peak_streamed_bytes_per_second * (RESUMABLE_STREAM_TTL_SECONDS + min(p95_run_duration_seconds, RESUMABLE_STREAM_TTL_SECONDS)) * 1.35
```

The factor of `1.35` covers the memory Redis uses on top of the event bytes. Keep `stream_memory_bytes` below `maxmemory`, and leave extra room for clients that replay or read streams. For example, with the default TTL, a 2 Gi Redis with `maxmemory` at 75% of its limit holds at most about 5 MB of streamed events per second when runs last 120 seconds or longer, and at most about 10 MB per second when runs are short.

For a Redis instance that you run yourself, such as a self-hosted deployment or one set with [`REDIS_URI_CUSTOM`](../../Deploy%20to%20Cloud/Reference/Cloud%20Agent%20Server%20environment%20variables.md#redis_uri_custom), set `maxmemory` below the memory limit and `maxmemory-policy` to `noeviction`. When Redis reaches `maxmemory`, it refuses new writes until events expire. Without `maxmemory`, a full Redis runs out of memory and restarts empty, which loses queued runs and interrupts every open stream.

## Read load

Read load is primarily driven by the following factors:

* Getting the results of a [run](../../Agent%20Server/Capabilities/Runs/How%20to%20kick%20off%20background%20runs.md)
* Getting the state of a [thread](../../Agent%20Server/Capabilities/Use%20threads.md)
* Searching for [runs](../../Agent%20Server/Capabilities/Runs/How%20to%20kick%20off%20background%20runs.md), [threads](../../Agent%20Server/Capabilities/Use%20threads.md), [cron jobs](../../Agent%20Server/Capabilities/Use%20cron%20jobs.md) and [assistants](../../Agent%20Server/Capabilities/Assistants/Assistants.md)
* Retrieving checkpoints and long term memory

The following components are primarily responsible for handling read load:

* API server: Handles the request and direct retrieval of data from the database.
* Postgres: Handles the storage of all data, including run, thread, assistant, cron job, checkpointing and long term memory.
* Redis: Handles the storage of ephemeral data about on-going runs, including streaming messages from queue workers to api servers.

### Use filtering to reduce results per request

[Agent Server](../../Agent%20Server/Capabilities/Agent%20Server.md) provides a search API for each resource type. These APIs implement pagination by default and offer many filtering options. Use filtering to reduce the number of resources returned per request and improve performance.

### Set TTLs to automatically delete old data

Set a [TTL on threads](../../Agent%20Server/Develop%20your%20application/Persistence/How%20to%20add%20TTLs%20to%20your%20application.md) to automatically clean up old data. Runs and checkpoints are automatically deleted when the associated thread is deleted.

### Avoid polling; use `/join` to monitor a run

Avoid polling the state of a run by using the `/join` API endpoint. This method returns the final state of the run once the run is complete.

If you need to monitor the output of a run in real-time, use the `/stream` API endpoint. This method streams the run output including the final state of the run.

### Configure autoscaling for bursty read workloads

Autoscaling is disabled by default, but should be configured for bursty workloads. Determine the maximum number of API servers you should allow the autoscaler to scale to based on maximum expected throughput.

## Example configurations

> [!NOTE]
>
> The exact optimal configuration depends on your application complexity, request patterns, and data requirements. Use the following examples in combination with the information in the previous sections and your specific usage to update your deployment configuration as needed. If you have any questions, contact support via [support.langchain.com](https://support.langchain.com).

The following table provides an overview comparing different Agent Server configurations for various load patterns (read requests per second / write requests per second) and standard assistant characteristics (average run execution time of 1 second, moderate CPU and memory usage). The request rates drive the required steady-state run throughput, which is sized through queue workers and `N_JOBS_PER_WORKER`, while API server replicas are sized to serve the request volume itself:

| | **[Low / low](#low-reads-low-writes)** | **[Low / high](#low-reads-high-writes)** | **[High / low](#high-reads-low-writes)** | [Medium / medium](#medium-reads-medium-writes) | [High / high](#high-reads-high-writes) |
| :- | :- | :- | :- | :- | :- |
| Write requests per second (Number of write requests being processed by the deployment per second) | 5 | 5 | 500 | 50 | 500 |
| Read requests per second (Number of read requests being processed by the deployment per second) | 5 | 500 | 5 | 50 | 500 |
| **API servers** (1 CPU, 2Gi per server) | 1 (default) | 6 | 10 | 3 | 15 |
| **Queue workers** (1 CPU, 2Gi per worker) | 1 (default) | 10 | 1 (default) | 5 | 10 |
| **`N_JOBS_PER_WORKER`** | 10 (default) | 50 | 10 | 10 | 50 |
| **Redis resources** | 1 CPU 2 Gi (default) | 1 CPU 2 Gi (default) | 1 CPU 2 Gi (default) | 1 CPU 2 Gi (default) | 1 CPU 2 Gi (default) |
| **Postgres resources** | 2 CPU 8 Gi (default) | 4 CPU 16 Gi memory | 4 CPU 16 Gi | 4 CPU 16 Gi memory | 8 CPU 32 Gi memory |

To size Redis for each deployment, set the `redis_cpu`, `redis_cpu_limit`, `redis_memory_mb`, and `redis_memory_limit_mb` fields of the [`resource_spec`](../../Get%20started/Reference/Control%20Plane%20API/Control%20plane%20API%20reference%20for%20Agent%20Server%20hosting.md#resource-spec). Redis memory accepts 512 to 16384 MB, so the minimum is 512 Mi. Redis CPU requires listener 0.13.22 or later, and Redis memory below 2048 requires listener 0.13.27 or later. See [Listener version requirements](Self-hosted%20platform%20features.md#listener-version-requirements).

From Agent Server v0.19.0rc1, Redis memory also depends on how much your runs stream. To size it, see [Size Redis memory for streaming](#size-redis-memory-for-streaming).

Load levels in the examples are defined as:

* Low means approximately 5 requests per second
* Medium means approximately 50 requests per second
* High means approximately 500 requests per second

### Low reads, low writes

The default [LangSmith Agent Server](../../Get%20started/LangSmith%20Agent%20Server.md) configuration will handle this load. No custom resource configuration is needed here.

### Low reads, high writes

You have a high volume of write requests (500 per second) being processed by your deployment, but relatively few read requests (5 per second).

For this, we recommend a configuration like this:

```yaml
# Example configuration for low reads, high writes (5 read/500 write requests per second)
api:
  replicas: 6
  resources:
    requests:
      cpu: "1"
      memory: "2Gi"
    limits:
      cpu: "2"
      memory: "4Gi"

queue:
  replicas: 10
  resources:
    requests:
      cpu: "1"
      memory: "2Gi"
    limits:
      cpu: "2"
      memory: "4Gi"

config:
  numberOfJobsPerWorker: 50

redis:
  resources:
    requests:
      memory: "2Gi"
    limits:
      memory: "2Gi"

postgres:
  resources:
    requests:
      cpu: "4"
      memory: "16Gi"
    limits:
      cpu: "8"
      memory: "32Gi"
```

### High reads, low writes

You have a high volume of read requests (500 per second) but relatively few write requests (5 per second).

For this, we recommend a configuration like this:

```yaml
# Example configuration for high reads, low writes (500 read/5 write requests per second)
api:
  replicas: 10
  resources:
    requests:
      cpu: "1"
      memory: "2Gi"
    limits:
      cpu: "2"
      memory: "4Gi"

queue:
  replicas: 1  # Default, minimal write load
  resources:
    requests:
      cpu: "1"
      memory: "2Gi"
    limits:
      cpu: "2"
      memory: "4Gi"

redis:
  resources:
    requests:
      memory: "2Gi"
    limits:
      memory: "2Gi"

postgres:
  resources:
    requests:
      cpu: "4"
      memory: "16Gi"
    limits:
      cpu: "8"
      memory: "32Gi"
  # Consider read replicas for high read scenarios
  readReplicas: 2
```

### Medium reads, medium writes

This is a balanced configuration that should handle moderate read and write loads (50 read/50 write requests per second).

For this, we recommend a configuration like this:

```yaml
# Example configuration for medium reads, medium writes (50 read/50 write requests per second)
api:
  replicas: 3
  resources:
    requests:
      cpu: "1"
      memory: "2Gi"
    limits:
      cpu: "2"
      memory: "4Gi"

queue:
  replicas: 5
  resources:
    requests:
      cpu: "1"
      memory: "2Gi"
    limits:
      cpu: "2"
      memory: "4Gi"

redis:
  resources:
    requests:
      memory: "2Gi"
    limits:
      memory: "2Gi"

postgres:
  resources:
    requests:
      cpu: "4"
      memory: "16Gi"
    limits:
      cpu: "8"
      memory: "32Gi"
```

### High reads, high writes

You have high volumes of both read and write requests (500 read/500 write requests per second).

For this, we recommend a configuration like this:

```yaml
# Example configuration for high reads, high writes (500 read/500 write requests per second)
api:
  replicas: 15
  resources:
    requests:
      cpu: "1"
      memory: "2Gi"
    limits:
      cpu: "2"
      memory: "4Gi"

queue:
  replicas: 10
  resources:
    requests:
      cpu: "1"
      memory: "2Gi"
    limits:
      cpu: "2"
      memory: "4Gi"

config:
  numberOfJobsPerWorker: 50

redis:
  resources:
    requests:
      memory: "2Gi"
    limits:
      memory: "2Gi"

postgres:
  resources:
    requests:
      cpu: "8"
      memory: "32Gi"
    limits:
      cpu: "16"
      memory: "64Gi"
```

### Autoscaling

If your deployment experiences bursty traffic, you can enable autoscaling to scale the number of API servers and queue workers to handle the load.

Here is a sample configuration for autoscaling for high reads and high writes:

```yaml
api:
  autoscaling:
    enabled: true
    minReplicas: 15
    maxReplicas: 25

queue:
  autoscaling:
    enabled: true
    minReplicas: 10
    maxReplicas: 20
```

> [!NOTE]
>
> Ensure that your deployment environment has sufficient resources to scale to the recommended size. Monitor your applications and infrastructure to ensure optimal performance. Consider implementing monitoring and alerting to track resource usage and application performance.

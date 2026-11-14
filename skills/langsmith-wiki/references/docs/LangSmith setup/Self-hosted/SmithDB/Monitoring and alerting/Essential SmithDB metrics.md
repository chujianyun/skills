# Essential SmithDB metrics

> The SmithDB and LangSmith metrics to monitor on self-hosted LangSmith, what they measure, and how to use them.

SmithDB components expose Prometheus metrics at `/metrics` on each pod's HTTP port. This page lists the metrics worth watching for each component and how to read them. Each table describes the metrics of one component in one line. The section for each metric under the table tells you how to use it. For scrape and export configuration, see [Configure SmithDB observability](Configure%20SmithDB%20observability.md). To check first whether SmithDB is healthy, see [Common SmithDB issues to monitor](Common%20SmithDB%20issues%20to%20monitor.md).

Names are as they appear on `/metrics`. If your collector adds a namespace or prefix, adjust accordingly.

For the tabbed Datadog and Grafana dashboards and their collection requirements, see [Monitor self-hosted LangSmith with Datadog or Grafana](../../Self-hosted%20observability/Monitor%20self-hosted%20LangSmith%20with%20Datadog%20or%20Grafana.md). For Grafana installations without native tabs, the [standalone SmithDB dashboard](https://github.com/langchain-ai/helm/blob/main/charts/langsmith/examples/langsmith-observability/components/smithdb/grafana.json) uses Classic format.

> [!NOTE]
>
> This page covers metrics that SmithDB and LangSmith emit. Also monitor these signals from your infrastructure monitoring:
>
> * Kubernetes: OOM kills, container restarts, CPU and memory against limits, and cache disk usage.
> * Redis: memory use against its limit, and evicted keys. If Redis is full, LangSmith cannot queue new runs. Any eviction means that Redis deleted data that LangSmith still needs, and runs can be lost.
> * Metastore: CPU, connections, and storage of the PostgreSQL database. A slow metastore makes ingestion, queries, and compaction slow.

## LangSmith ingestion pipeline

The LangSmith ingestion pipeline is not part of SmithDB, but it sends all runs to SmithDB and SmithDB problems are often visible here first. Monitor it together with SmithDB. To collect these metrics, see [Export LangSmith telemetry](../../Self-hosted%20observability/Export%20LangSmith%20telemetry%20to%20your%20observability%20backend.md).

| Metric | Description |
| - | - |
| [`langsmith_ingestion_e2e_latency_seconds`](#langsmith_ingestion_e2e_latency_seconds) | Time from when the API receives a run until SmithDB stores it. |
| [`langsmith_ingestion_api_to_worker_latency_seconds`](#langsmith_ingestion_api_to_worker_latency_seconds) | Time that a run waits in Redis before a worker starts it. |
| [`langsmith_ingestion_worker_to_store_latency_seconds`](#langsmith_ingestion_worker_to_store_latency_seconds) | Time of one write from an ingest queue worker to SmithDB. |
| [`langsmith_asynq_ingestion_queue_pending`](#langsmith_asynq_ingestion_queue_pending) | Tasks that wait in Redis for an ingest queue worker. |
| [`langsmith_asynq_ingestion_queue_retry`](#langsmith_asynq_ingestion_queue_retry) | Tasks whose write failed and that wait for another attempt. |
| [`langsmith_asynq_queue_latency_seconds`](#langsmith_asynq_queue_latency_seconds) | Age of the oldest pending task in each Redis queue. |
| [`langsmith_asynq_ingestion_queue_archived`](#langsmith_asynq_ingestion_queue_archived) | Tasks that failed on all attempts. Their runs are lost. |

### `langsmith_ingestion_e2e_latency_seconds`

*Histogram*

Time from when the API receives a run until SmithDB stores it. This is the delay that users see, including the wait in Redis and all retries. During [dual ingestion](../Install%20SmithDB/Install%20LangSmith%20with%20SmithDB.md#step-4-enable-dual-ingestion), compare SmithDB with ClickHouse to see if SmithDB keeps up. Short spikes are normal.

Query: Use p95. The highest bucket is 60 s, so the p99 often stays at 60 s and does not show changes. Filter on `store="smithdb"`. To compare with ClickHouse, split by `store` (`smithdb` or `clickhouse`).

### `langsmith_ingestion_api_to_worker_latency_seconds`

*Histogram*

Time that a run waits in Redis before a worker starts it. If it increases while `langsmith_ingestion_worker_to_store_latency_seconds` is stable, there are not enough ingest queue workers, and the problem is not in SmithDB.

Query: Filter on `store="smithdb"`. To compare with ClickHouse, split by `store` (`smithdb` or `clickhouse`).

### `langsmith_ingestion_worker_to_store_latency_seconds`

*Histogram*

Time of one write from an ingest queue worker to SmithDB. If it increases, the problem is in SmithDB or in its dependencies. Slow writes keep the workers busy, so runs also wait longer in Redis. Continue with the SmithDB ingestion metrics.

Query: Filter on `store="smithdb"`. To compare with ClickHouse, split by `store` (`smithdb` or `clickhouse`). The value is the time of the full batch, recorded once for each run in the batch.

### `langsmith_asynq_ingestion_queue_pending`

*Gauge*

Tasks that wait in Redis for an ingest queue worker. Tasks that wait for a retry are not included. Monitor the trend relative to traffic, not the number. A queue that increases while traffic is stable is a problem. A sudden decrease is healthy if retries stay stable.

Query: Every platform backend pod reports the same value for the whole queue. Use max across pods, not sum.

### `langsmith_asynq_ingestion_queue_retry`

*Gauge*

Tasks whose write failed and that wait for another attempt. These tasks are not in the pending queue. Short increases are normal. If the value stays high, writes from ingest queue workers to SmithDB ingestion fail. After 12 failed attempts (approximately 2.5 hours), the task goes to the archive, and its runs are lost. If `config.settings.redisRunsExpirySeconds` is shorter than this, run data expires in Redis first, and runs are lost before the task reaches the archive.

Query: Every platform backend pod reports the same value for the whole queue. Use max across pods, not sum.

### `langsmith_asynq_queue_latency_seconds`

*Gauge*

Age of the oldest pending task in each Redis queue. LangSmith deletes run data in Redis after a fixed time, set by `config.settings.redisRunsExpirySeconds` in the Helm chart (6 hours by default). Act long before this value reaches that time. The value covers only pending tasks, and the age starts again after each retry. To find tasks that fail again and again, monitor `langsmith_asynq_ingestion_queue_retry`.

Query: Every platform backend pod reports the same value for each queue. Use max across pods and across the ingestion queues, not sum.

### `langsmith_asynq_ingestion_queue_archived`

*Gauge*

Tasks that failed on all attempts. Their runs are lost. An increase means data loss. Archived tasks stay for 90 days, so monitor increases, not the value. Each queue keeps a maximum of 10,000 archived tasks. When the archive is full, the value stops increasing. Then use the ingest queue logs to find new failures.

Query: Every platform backend pod reports the same value for the whole queue. Use max across pods, not sum.

## SmithDB ingestion

| Metric | Description |
| - | - |
| [`ingest_batch_latency`](#ingest_batch_latency) | Time until new data is durable in SmithDB. |
| [`ingest_flush_count`](#ingest_flush_count) | Completed and failed flushes to object storage. |
| [`ingest_flush_rows`](#ingest_flush_rows) | Runs in each flush. |
| [`ingest_flush_duration`](#ingest_flush_duration) | Time of each flush. |
| [`ingest_flush_reason`](#ingest_flush_reason) | Why each flush started. |
| [`ingest_pending_segment_entry_count`](#ingest_pending_segment_entry_count) | Data on an ingestion pod that is not flushed or merged yet. |
| [`semaphore_permits_in_use`](#semaphore_permits_in_use-semaphore_max_permits) [`semaphore_max_permits`](#semaphore_permits_in_use-semaphore_max_permits) | Flushes that run at the same time on an ingestion pod, compared with the limit. |
| [`server_requests_duration`](#server_requests_duration-on-ingestion-pods) | Time of each request to an ingestion pod. |

### `ingest_batch_latency`

*Histogram*

Time until new data is durable in SmithDB. Ingestion collects the runs of the same partition (tenant, project, and day) from all requests, and flushes them together as one segment. SmithDB records one value for each partition in a request, from when the runs arrive until their flush completes. The value includes the wait for the flush, so a p50 above 0.5 s is normal. If the p99 stays high, flushes are slow. Examine `ingest_flush_duration` and the flush semaphores.

### `ingest_flush_count`

*Counter*

Completed and failed flushes to object storage. If the rate of successful flushes (`status="success"`) drops to 0 while runs arrive, writes do not reach object storage. A continuous rate of failed flushes (`status="failure"`) means that object storage or the metastore has errors.

Query: Use the rate, summed across pods. Split by `status` (`success` or `failure`). To separate L0 and L1 flushes, also split by `level`.

### `ingest_flush_rows`

*Histogram*

Runs in each flush. Small L0 flushes are normal, because most tenants and projects send few runs in 500 ms. If rows decrease while the flush rate stays the same, flushes occur too early.

Query: Split by `level` (`L0` or `L1`).

### `ingest_flush_duration`

*Histogram*

Time of each flush, including the time before the flush can start, and flushes that fail. If it increases together with [`object_store_op_duration`](#object_store_op_duration), the cause is object storage. If it increases alone, too many flushes run at the same time (see the [semaphores](#semaphore_permits_in_use-semaphore_max_permits)), or the metastore is slow.

### `ingest_flush_reason`

*Counter*

Why each flush started. `time` means that the flush timer fired, `size` means that the data reached its row limit, and `shutdown` means that the pod stopped. More `size` flushes mean more data for each tenant and project. Many `shutdown` flushes outside of rollouts mean that pods restart.

Query: Use the rate, summed across pods. Split by `reason` and by `level` (`L0` or `L1`).

### `ingest_pending_segment_entry_count`

*Gauge*

Data on an ingestion pod that is not flushed or merged yet. L0 counts data in memory that is not flushed yet. L1 counts segments on the disk cache that are not merged yet. A large L1 value is normal, because SmithDB merges data only after 10 minutes or 25,000 rows. A value that increases continuously means that flushes are late. SmithDB updates the value only at certain events, so it can stay old for some time.

Query: Split by `level` (`L0` or `L1`). Use max across ingestion pods to find the pod with the most pending data.

### `semaphore_permits_in_use`, `semaphore_max_permits`

*Gauges*

Flushes that run at the same time on an ingestion pod, compared with the limit. The `name` label identifies the semaphore: `flush_l0` limits the flushes of new data from memory to small L0 segments (default 200), and `flush_l1` limits the merges of L0 segments into larger L1 segments (default 10). Short peaks at the maximum are normal. If `semaphore_permits_in_use` stays at `semaphore_max_permits`, work waits in the pod. You see this as latency, not as errors.

Query: Filter on the `name` label, for example `name="flush_l0"`.

### `server_requests_duration` on ingestion pods

*Histogram*

Time of each request to an ingestion pod. The `path` label shows the request type. The most common types end with `IngestRunsStream`, the writes of runs from ingest queue workers, and `ExecuteQueryStream`, the reads of the newest segments by query pods. For writes, a `status` other than 0 is a failed write, which the ingest queue worker tries again.

Query: All SmithDB pods report this metric. Select the ingestion pods with the pod or Deployment label that your collector adds, for example `langsmith-smithdb-ingestion`. Filter on `type="grpc"`, because HTTP requests on these pods are health checks and metrics scrapes. For streams, the value covers the full stream.

## SmithDB query

| Metric | Description |
| - | - |
| [`server_requests_duration`](#server_requests_duration-on-query-pods) | Time of each request to a query pod. |
| [`query_fanout_partitions`](#query_fanout_partitions) | Scan partitions that a query must open. More scan partitions make queries slower. |
| [`query_fanout_limit_exceeded_total`](#query_fanout_limit_exceeded_total) | Queries rejected because they must open too many scan partitions. |
| [`query_execution_max_mem_used_bytes`](#query_execution_max_mem_used_bytes) | Peak memory of the largest operator in a query. |
| [`query_admission_queue_length`](#query_admission_queue_length) | Requests that wait because a query pod is at its memory limit. |
| [`query_admission_queue_duration_seconds`](#query_admission_queue_duration_seconds) | Time that a request waits in the admission queue. |
| [`query_admission_queue_rejections_total`](#query_admission_queue_rejections_total) | Requests rejected because the admission queue is full. |

### `server_requests_duration` on query pods

*Histogram*

Time of each request to a query pod. The `path` label shows the request type. The most common types end with `QueryRuns`, which lists runs, `QueryTraces`, which lists traces, and `QueryRun`, which reads one run. If many request types are slow, examine `query_fanout_partitions` (compaction is late) and the admission queue (pods are out of memory).

Query: Select the query pods with the pod or Deployment label that your collector adds. Each query pool has its own Deployment. Split by `path` to find the slow request type, and by `status` to count failures. The `status` label is the gRPC code, where 0 is success.

### `query_fanout_partitions`

*Histogram*

Scan partitions that a query must open. A scan partition is approximately one segment or a group of segments. The more scan partitions a query opens, the slower it is and the more memory it needs. Compaction merges small segments, so queries open fewer scan partitions. If the p99 increases while traffic is stable, compaction is usually late.

### `query_fanout_limit_exceeded_total`

*Counter*

Queries rejected because they must open too many scan partitions. SmithDB query rejects a query that must open more than 10,000 scan partitions. A continuous rate means that user queries fail. Examine compaction first. Wide time ranges can also cause it.

Query: Use the rate, summed across pods.

### `query_execution_max_mem_used_bytes`

*Histogram*

Peak memory of the largest operator in a query, not of the full query. Use it to find request types that need much memory. Use pod memory to see if a pod is near its limit.

### `query_admission_queue_length`

*Gauge*

Requests that wait because a query pod is at its memory limit. New requests wait in the admission queue of the pod, which has 100 places. If the pod has no memory limit, the value always stays at 0.

Query: Use max across query pods to find the pod with the longest queue.

### `query_admission_queue_duration_seconds`

*Histogram*

Time that a request waits in the admission queue before it starts. Long waits make queries slow, but they do not fail.

### `query_admission_queue_rejections_total`

*Counter*

Requests rejected because the admission queue is full. Each rejection is a failed query, and means that a query pod is out of memory. Add replicas or memory.

Query: Use the rate, summed across pods.

## SmithDB compaction

The compaction scheduler keeps its job queue in memory. The queue metrics come from the scheduler pod. The worker metrics come from each worker pod.

| Metric | Description |
| - | - |
| [`compaction_jobs_scheduled`](#compaction_jobs_scheduled-compaction_jobs_executed) [`compaction_jobs_executed`](#compaction_jobs_scheduled-compaction_jobs_executed) | Compaction jobs that the scheduler planned and that workers finished. |
| [`compaction_job_completion`](#compaction_job_completion) | Results of compaction jobs, success or failure. |
| [`compaction_queue_job_count`](#compaction_queue_job_count) | Compaction jobs that wait or run now. |
| [`compaction_queue_job_size`](#compaction_queue_job_size) | Estimated memory of all compaction jobs that wait or run now. |
| [`compaction_queue_oldest_pending_created_at_seconds`](#compaction_queue_oldest_pending_created_at_seconds) | Creation time of the oldest compaction job that waits. |
| [`compaction_job_latency_seconds`](#compaction_job_latency_seconds) | Time from job creation to completion, including the wait. |
| [`compaction_queue_jobs_skipped_capacity`](#compaction_queue_jobs_skipped_capacity) | Jobs skipped because they did not fit on a worker. |
| [`compaction_worker_capacity_used`](#compaction_worker_capacity_used-compaction_worker_capacity_limit) [`compaction_worker_capacity_limit`](#compaction_worker_capacity_used-compaction_worker_capacity_limit) | Memory of running jobs, compared with worker capacity. |
| [`compaction_worker_running_tasks`](#compaction_worker_running_tasks) | Compaction jobs that a worker runs now. |

### `compaction_jobs_scheduled`, `compaction_jobs_executed`

*Counters*

Compaction jobs that the scheduler planned and that workers finished. A gap that closes again is normal. If executed stays below scheduled, there are not enough compaction workers. Examine the worker capacity and the pending queue.

Query: Use the rate, summed across pods.

### `compaction_job_completion`

*Counter*

Results of compaction jobs, success or failure. Single failures are normal, for example when two jobs change the same segment. A job that is too large for every worker, or that does not finish in time, also counts as a failure. If one `job_kind` fails again and again, or has no successes, that job kind does not work.

Query: Use the rate, summed across pods. Split by `status` (`success` or `failure`) and by `job_kind`.

### `compaction_queue_job_count`

*Gauge*

Compaction jobs that wait (`pending`) or run now (`inflight`). Short peaks are normal, for example after many deletes. A pending count that stays high for hours means that compaction is late. Check if the autoscaler adds compaction workers. By default, it scales on CPU, not on pending jobs. To scale on pending jobs, see [Scale with KEDA instead](../Install%20SmithDB/Configure%20SmithDB%20for%20scale.md#scale-with-keda-instead). If the workers are at their maximum replica count, raise the maximum.

Query: Split by `status` (`pending` or `inflight`) and by `job_kind`.

### `compaction_queue_job_size`

*Gauge*

Estimated memory of all compaction jobs that wait or run now. It uses the same unit as worker capacity. If the pending size of one `job_kind` is larger than the free capacity of every worker, those jobs wait until a worker is almost idle. Add compaction workers, or give them more memory.

Query: Split by `status` (`pending` or `inflight`) and by `job_kind`.

### `compaction_queue_oldest_pending_created_at_seconds`

*Gauge*

Creation time of the oldest compaction job that waits. Some jobs wait for hours, because a compaction worker takes the first job that fits in its free capacity, and large jobs wait until a worker is almost idle. Monitor the trend, not a fixed age. An age that increases continuously means that compaction does not keep up. To find which job kind waits, compare [`compaction_queue_job_count`](#compaction_queue_job_count) and [`compaction_queue_job_size`](#compaction_queue_job_size) by `job_kind`.

Query: Calculate the age with `time() - value`, and do not include 0.

### `compaction_job_latency_seconds`

*Histogram*

Time from job creation to completion, including the wait. It increases when compaction workers are full and when jobs are slow. Compare it with worker capacity to find which one.

Query: The highest bucket is 900 s, so percentiles do not show longer times. To find jobs that wait longer, use [`compaction_queue_oldest_pending_created_at_seconds`](#compaction_queue_oldest_pending_created_at_seconds).

### `compaction_queue_jobs_skipped_capacity`

*Counter*

Jobs skipped because they did not fit on a worker. The compaction scheduler counts a job each time a worker asks for work and the job does not fit, so one job can be counted many times. A high rate is normal. Monitor the trend together with the oldest pending age.

Query: Use the rate, summed across pods.

### `compaction_worker_capacity_used`, `compaction_worker_capacity_limit`

*Gauges*

Memory of running jobs, compared with worker capacity. Capacity is an estimate of job memory, by default 80% of the pod memory limit. If most compaction workers stay near their limit, jobs wait and the pending queue increases. Add compaction workers, or give them more memory for larger jobs.

Query: Split `compaction_worker_capacity_used` by `job_kind` to see which job kinds use the capacity.

### `compaction_worker_running_tasks`

*Gauge*

Compaction jobs that a worker runs now. If the sum is 0 while jobs are pending, the compaction workers have stopped. Make sure that they can connect to the compaction scheduler.

Query: Use the sum across compaction workers. Split by `job_kind` to see which job kinds run.

## Shared SmithDB metrics

Several SmithDB components report these metrics.

| Metric | Description |
| - | - |
| [`object_store_op_duration`](#object_store_op_duration) | Time of each operation on object storage. |
| [`sys_jemalloc_resident_bytes`](#sys_jemalloc_resident_bytes) | Memory that the SmithDB process uses. |

### `object_store_op_duration`

*Histogram*

Time of each operation on object storage. Query, ingestion, and compaction pods report this metric. They read and write their data in object storage, so slow object storage makes ingestion, queries, and compaction slow. If the value increases on all components at the same time, the cause is object storage or the network to it.

Query: Split by `op` to find the slow operation type, and by `result` (`success`, `error`, or `canceled`) to find failures. Select one component with the pod or Deployment label that your collector adds.

### `sys_jemalloc_resident_bytes`

*Gauge*

Memory that the SmithDB process uses. Compare it with the pod memory limit. If the value comes near the limit, Kubernetes stops the pod because it is out of memory (OOM kill).

Query: Use max across the pods of a component.

## SmithDB migration

Migration Job pods report these metrics during a [historical migration](../Install%20SmithDB/Migrate%20ClickHouse%20history%20to%20SmithDB.md). Migration does not try failed tasks or jobs again. A failure stops the migration Job before it reaches `Complete`, and the Job keeps running until you fix the failure. See [Migration Job failures](../Install%20SmithDB/Troubleshoot%20SmithDB.md#migration-job-failures).

| Metric | Description |
| - | - |
| [`migration_tasks`](#migration_tasks) | Migration tasks by kind and status. |
| [`migration_jobs`](#migration_jobs) | Migration jobs by kind and status. |
| [`migration_run_tasks_completed_total`](#migration_run_tasks_completed_total) | Run tasks that a pod completed. |
| [`migration_run_task_planned_rows_migrated_total`](#migration_run_task_planned_rows_migrated_total) | Rows in the run tasks that a pod completed. |

### `migration_tasks`

*Gauge*

Migration tasks by kind and status. The `kind` label is `run` or `feedback`. The `status` label is `pending`, `running`, `completed`, or `failed`. The progress is the `completed` count, compared with the total of all statuses. Any `failed` task stops the migration.

Query: Every pod reports the same value for the whole migration. The value comes from the migration task database (TaskDB) and changes every two minutes. Use max across pods, not sum.

### `migration_jobs`

*Gauge*

Migration jobs by kind and status. Run jobs finish as `promoted`, and feedback jobs finish as `validated`. `failed` and `validation_failed` are failures and stop the migration. All other statuses mean that the job is still in progress.

Query: Every pod reports the same value for the whole migration. The value comes from TaskDB and changes every two minutes. Use max across pods, not sum.

### `migration_run_tasks_completed_total`

*Counter*

Run tasks that a pod completed. The rate is the migration throughput in tasks.

Query: Use the rate, summed across pods.

### `migration_run_task_planned_rows_migrated_total`

*Counter*

Rows in the run tasks that a pod completed. ClickHouse counts the rows when the migration plans the tasks. The rate is the migration throughput in rows.

Query: Use the rate, summed across pods.

## Terms

For the terms of the architecture, such as task and segment, see [SmithDB architecture](../Overview/SmithDB%20architecture.md#terms).

| Term | Meaning |
| - | - |
| Partition | The runs of one tenant, one project, and one day. SmithDB ingestion writes each partition to its own segments. |
| Scan partition | One unit of work that a query reads, approximately one segment or a group of segments. It is not the same as a partition. |
| Flush | SmithDB ingestion writes data to object storage as a segment. An L0 flush writes new data from memory. An L1 flush merges L0 segments into one larger segment. |
| L0, L1 segment | SmithDB ingestion flushes a small L0 segment for each partition every 500 ms or 5,000 rows. Later, it merges the L0 segments of a partition into one larger L1 segment. |
| Admission queue | Where new queries wait when the memory of a query pod is at its limit. |
| Compaction job | One unit of compaction work: it merges segments, writes feedback into files, or removes expired and deleted data. The scheduler plans jobs. Workers run them. |

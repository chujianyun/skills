# Common SmithDB issues to monitor

> The first metrics to check on self-hosted LangSmith, and how to detect and fix the SmithDB issues that occur most often in production.

Use these signals to tell whether SmithDB ingestion, queries, and compaction are healthy, and which area to investigate first. For each common issue below, the page lists which signals to monitor, how to find the cause, and what to change. For what each metric measures and how to use it, see [Essential SmithDB metrics](Essential%20SmithDB%20metrics.md).

## Check SmithDB health

Each symptom below lists the metric that shows it. To find the cause, read that metric's section in [Essential SmithDB metrics](Essential%20SmithDB%20metrics.md).

* **Traces appear late after the SDK sends them**: [`langsmith_ingestion_e2e_latency_seconds`](Essential%20SmithDB%20metrics.md#langsmith_ingestion_e2e_latency_seconds). See [LangSmith ingestion falls behind](#langsmith-ingestion-falls-behind).
* **Writes fail and keep retrying**: [`langsmith_asynq_ingestion_queue_retry`](Essential%20SmithDB%20metrics.md#langsmith_asynq_ingestion_queue_retry). See [LangSmith ingestion falls behind](#langsmith-ingestion-falls-behind).
* **New runs take a long time to become durable in SmithDB**: [`ingest_batch_latency`](Essential%20SmithDB%20metrics.md#ingest_batch_latency). Continue with the [SmithDB ingestion metrics](Essential%20SmithDB%20metrics.md#smithdb-ingestion).
* **Ingestion backlog grows and does not drain**: [`ingest_pending_segment_entry_count`](Essential%20SmithDB%20metrics.md#ingest_pending_segment_entry_count). Continue with the [SmithDB ingestion metrics](Essential%20SmithDB%20metrics.md#smithdb-ingestion).
* **UI or API reads of traces are slow**: [`server_requests_duration` on query pods](Essential%20SmithDB%20metrics.md#server_requests_duration-on-query-pods). See [Compaction falls behind and queries get slow](#compaction-falls-behind-and-queries-get-slow) and [One kind of query load slows down other queries](#one-kind-of-query-load-slows-down-other-queries).
* **Compaction workers finish less work than the scheduler plans**: [`compaction_jobs_scheduled`, `compaction_jobs_executed`](Essential%20SmithDB%20metrics.md#compaction_jobs_scheduled-compaction_jobs_executed). See [Compaction falls behind and queries get slow](#compaction-falls-behind-and-queries-get-slow).
* **One compaction job kind fails again and again**: [`compaction_job_completion`](Essential%20SmithDB%20metrics.md#compaction_job_completion).
* **Compaction stays behind for hours**: [`compaction_queue_job_count`](Essential%20SmithDB%20metrics.md#compaction_queue_job_count). See [Compaction falls behind and queries get slow](#compaction-falls-behind-and-queries-get-slow).

## LangSmith ingestion falls behind

LangSmith keeps each new run in Redis until an ingest queue worker writes it to SmithDB. If ingestion cannot keep up, the queue in Redis increases, and users see their runs late. If the queue gets too old, or Redis gets full, LangSmith loses runs.

### Monitor the ingestion backlog

* **Lost runs**: [`langsmith_asynq_ingestion_queue_archived`](Essential%20SmithDB%20metrics.md#langsmith_asynq_ingestion_queue_archived). Each increase means that runs are lost. Alert on every increase.
* **Backlog**: [`langsmith_asynq_ingestion_queue_pending`](Essential%20SmithDB%20metrics.md#langsmith_asynq_ingestion_queue_pending). Compare it with your normal traffic. A queue that increases while traffic is stable is a problem.
* **Failed writes**: [`langsmith_asynq_ingestion_queue_retry`](Essential%20SmithDB%20metrics.md#langsmith_asynq_ingestion_queue_retry). A value that stays high means that writes to SmithDB fail.
* **Age of the backlog**: [`langsmith_asynq_queue_latency_seconds`](Essential%20SmithDB%20metrics.md#langsmith_asynq_queue_latency_seconds). LangSmith deletes run data in Redis after the time set by `config.settings.redisRunsExpirySeconds`, 6 hours by default. Retries do not extend this time. Alert long before the age gets near it.
* **Redis**: Memory use against its limit, evicted keys, and the CPU of each shard. Any eviction means that Redis deleted data that LangSmith still needs.

### Find the cause of the backlog

| What you see | Cause |
| - | - |
| The pending queue and [`langsmith_ingestion_api_to_worker_latency_seconds`](Essential%20SmithDB%20metrics.md#langsmith_ingestion_api_to_worker_latency_seconds) increase. Retries and [`langsmith_ingestion_worker_to_store_latency_seconds`](Essential%20SmithDB%20metrics.md#langsmith_ingestion_worker_to_store_latency_seconds) stay stable. | There are not enough ingest queue workers. |
| Retries or `langsmith_ingestion_worker_to_store_latency_seconds` increase. | Writes are slow or fail. Continue with the [SmithDB ingestion metrics](Essential%20SmithDB%20metrics.md#smithdb-ingestion). |
| Redis memory is near its limit, or Redis evicts keys. | Redis is too small for the backlog. |
| One Redis shard uses much more CPU than the others. | The queue load is on one shard. More workers add more connections to that shard. |

### Reduce the backlog

* **Scale ingest queue workers on the queue length.** The workers mostly wait for the network, so their CPU stays low while the queue increases. An autoscaler that uses CPU does not add workers. Enable [KEDA for the ingest queue](../../Configure%20an%20instance/Configure%20LangSmith%20for%20scale.md#keda-autoscaling-for-langsmith-queues), which scales on the queue length. If a NetworkPolicy limits traffic in the namespace, make sure that KEDA can still read the queue length. If it cannot, KEDA does not scale the workers, and it does not show an error.
* **Set the maximum replica count from your peak load.** The chart's default maximum is a starting point, not a value for your load. Each worker opens connections to Redis, so increase the maximum in small steps and monitor the CPU of the busiest Redis shard.
* **Size Redis for the backlog.** Redis must hold all pending runs until the workers write them, including while writes are slow. If its memory gets near the limit, or it evicts keys, use a larger Redis instance.
* **Scale SmithDB ingestion** if writes are slow or fail. See [Configure SmithDB for scale](../Install%20SmithDB/Configure%20SmithDB%20for%20scale.md).

## Compaction falls behind and queries get slow

SmithDB ingestion writes many small segments. Compaction merges them into fewer, larger segments. If compaction falls behind, each query must open more segments. Queries then get slow, time out, or SmithDB rejects them.

### Monitor compaction and queries

For compaction:

* **Pending jobs**: [`compaction_queue_job_count`](Essential%20SmithDB%20metrics.md#compaction_queue_job_count) with `status="pending"`. A value that stays high for hours means that compaction is late.
* **Oldest pending job**: [`compaction_queue_oldest_pending_created_at_seconds`](Essential%20SmithDB%20metrics.md#compaction_queue_oldest_pending_created_at_seconds). An age that increases continuously means that compaction does not keep up.
* **Worker capacity**: [`compaction_worker_capacity_used` and `compaction_worker_capacity_limit`](Essential%20SmithDB%20metrics.md#compaction_worker_capacity_used-compaction_worker_capacity_limit). If most workers stay near their limit, jobs wait.
* **Worker restarts**: OOM kills of compaction worker pods. A worker that restarts loses its running jobs, and compaction does not make progress.

For queries:

* **Scan partitions**: [`query_fanout_partitions`](Essential%20SmithDB%20metrics.md#query_fanout_partitions). If the p99 increases while traffic is stable, compaction is usually late.
* **Rejected queries**: [`query_fanout_limit_exceeded_total`](Essential%20SmithDB%20metrics.md#query_fanout_limit_exceeded_total). A continuous rate means that user queries fail.
* **Slow and failed requests**: [`server_requests_duration` on query pods](Essential%20SmithDB%20metrics.md#server_requests_duration-on-query-pods). Split by `status`: `4` is a request that timed out, and `1` is a request that was canceled.

### Find the cause of slow queries

Queries can also get slow for other reasons. Before you scale compaction, compare these signals:

| What you see | Cause |
| - | - |
| Scan partitions and pending compaction jobs increase. | Compaction is late. |
| The [admission queue](Essential%20SmithDB%20metrics.md#query_admission_queue_length) is not empty, it rejects requests, or query pods are OOM-killed. | Query pods do not have enough memory. See [One kind of query load slows down other queries](#one-kind-of-query-load-slows-down-other-queries). |
| [`object_store_op_duration`](Essential%20SmithDB%20metrics.md#object_store_op_duration) increases on all components at the same time. | Object storage, or the network to it, is slow. |
| Only some requests are slow, and they cover a wide time range. | The queries read too much data. |

### Help compaction keep up

* **Add compaction workers.** By default, the autoscaler scales compaction workers on CPU, not on pending jobs. To scale on pending jobs, see [Scale with KEDA instead](../Install%20SmithDB/Configure%20SmithDB%20for%20scale.md#scale-with-keda-instead). If the workers are at their maximum replica count, increase the maximum.
* **Give compaction workers more memory** if they are OOM-killed, or if most of them stay near their capacity limit. Worker capacity is 80% of the pod memory limit, so more memory lets larger jobs run. Select a larger [tier](../Install%20SmithDB/Configure%20SmithDB%20for%20scale.md#baseline-tiers) or set the resources of the compaction worker.
* **Limit the time range of queries.** Scripts and API clients that query without a start time make SmithDB read data from all days.
* **Use time-based trace IDs.** If your application sets its own run or trace IDs, use UUIDv7 values. SmithDB uses the time in the ID to find the data of a trace. Random IDs, such as UUIDv4, make queries and deletes read much more data.

## One kind of query load slows down other queries

In cluster mode, the query service serves all SmithDB reads. A heavy load of one kind, such as run statistics on a large project, can slow down all other queries. [Dedicated query services](../Install%20SmithDB/Configure%20SmithDB%20for%20scale.md#dedicated-query-services) move one kind of load to its own pods, so you can size and scale it separately.

For large deployments, such as the large [tier](../Install%20SmithDB/Configure%20SmithDB%20for%20scale.md#baseline-tiers), enable the dedicated query services. Each service needs its own replicas, with the resources of the query tier.

For smaller deployments, enable a service when you see its signals in the following table. To find which kind of request uses the query pods, split [`server_requests_duration` on query pods](Essential%20SmithDB%20metrics.md#server_requests_duration-on-query-pods) by `path`.

| Service | Enable it when |
| - | - |
| Stats query | Project pages and dashboards load slowly, and other queries get slow at the same time. Query pods run out of memory, or SmithDB rejects queries with [`query_fanout_limit_exceeded_total`](Essential%20SmithDB%20metrics.md#query_fanout_limit_exceeded_total), when users open projects with many runs or long time ranges. |
| Mutations | Feedback and run deletions fail or are late while query pods are under load. Ingest queue logs show `IngestFeedback` errors with code `Unavailable`. Without this service, feedback writes and deletions run on the query pods. When those pods restart, feedback writes also fail. |
| Run rules | You have many automation rules or online evaluators, and query latency increases when the rules run. Rule queries that time out are tried again, which adds load to SmithDB and to the LangSmith PostgreSQL database. |

Query pods often use all their memory while their CPU stays low. An autoscaler that uses CPU does not add replicas in this case. Set a minimum replica count that holds your normal load, or give the pods more memory.

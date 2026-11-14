# Scalability & resilience

LangSmith is designed to scale horizontally with your workload. Each instance of the service is stateless, and keeps no resources in memory. The service is designed to gracefully handle new instances being added or removed, including hard shutdown cases.

## Server scalability

As you add more instances to a service, they will share the HTTP load as long as an appropriate load balancer mechanism is placed in front of them. In most deployment modalities we configure a load balancer for the service automatically. In the “self-hosted without control plane” modality it’s your responsibility to add a load balancer. Since the instances are stateless any load balancing strategy will work, no session stickiness is needed, or recommended. Any instance of the server can communicate with any queue instance (through Redis PubSub), meaning that requests to cancel or stream an in-progress run can be handled by any arbitrary instance.

## Queue scalability

As you add more queue workers to a service, they will increase run throughput linearly, as each queue worker is configured to execute a set number of concurrent runs (`N_JOBS_PER_WORKER`, by default 10). This value governs concurrent run execution, not how many API requests the deployment can serve. Each attempt for each run will be handled by a single instance, with exactly-once semantics enforced through Postgres’s MVCC model (refer to section below for crash resilience details). Attempts that fail due to transient database errors are retried up to 3 times. We do not make use of long-lived transactions or locks, this enables us to make more efficient use of Postgres resources.

## Resilience

While a run is being handled by a queue instance, a periodic heartbeat timestamp will be recorded in Redis by that queue worker.

When a graceful shutdown request is received (SIGINT) an instance enters shutdown mode, which

* stops accepting new HTTP requests
* gives any in-progress runs a limited number of seconds to finish (if not finished it will be put back in the queue)
* stops the instance from picking up more runs from the queue

If a hard shutdown occurs due to a server crash or an infrastructure failure, any runs that were in progress will be picked up by an internal sweeper task that looks for in-progress runs that have breached their heartbeat window. The sweeper runs every 2 minutes and will put the runs back in the queue for another instance to pick them up.

## Postgres resilience

For deployment modalities where LangSmith manages the Postgres database, there are periodic backups and continuously replicated standby replicas for automatic failover. This Postgres configuration is available in the [Cloud deployment option](../../Cloud/Cloud%20%28SaaS%29.md) for [Dedicated deployment type](../../../Deploy/Deploy%20to%20Cloud/Cloud%20platform%20features.md#deployment-types) only.

All communication with Postgres implements retries for retry-able errors. If Postgres is momentarily unavailable, such as during a database restart, most/all traffic should continue to succeed. Prolonged failure of Postgres will render the Agent Server unavailable.

## Redis resilience

All data that requires durable storage is stored in Postgres, not Redis. Redis is used only for ephemeral metadata, and communication between instances. Therefore we place no durability requirements on Redis.

All communication with Redis implements retries for retry-able errors. If Redis is momentarily unavailable, such as during a database restart, most/all traffic should continue to succeed. Prolonged failure of Redis will render the Agent Server unavailable.

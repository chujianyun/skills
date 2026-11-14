# LangSmith data plane

The *data plane* consists of your [Agent Servers](../../Agent%20Server/Capabilities/Agent%20Server.md) (deployments), their supporting infrastructure, and the listener application that continuously polls for updates from the [LangSmith control plane](LangSmith%20control%20plane.md).

## Server infrastructure

In addition to the [Agent Server](../../Agent%20Server/Capabilities/Agent%20Server.md) itself, the following infrastructure components for each server are also included in the broad definition of "data plane":

* **PostgreSQL**: persistence layer for user, run, and memory data.
* **Redis**: communication and ephemeral metadata for workers.
* **Secrets store**: secure management of environment secrets.
* **Autoscalers**: scale server containers based on load.

## Listener application

The data plane listener application periodically calls [control plane APIs](LangSmith%20control%20plane.md#control-plane-api) to:

* Determine if new deployments should be created.
* Determine if existing deployments should be updated (i.e. new revisions).
* Determine if existing deployments should be deleted.

In other words, the data plane listener reads the latest state of the control plane (desired state) and takes action to reconcile outstanding deployments (current state) to match the latest state.

## PostgreSQL

PostgreSQL stores server resources (threads, runs, assistants, crons) and items saved in the [long-term memory store](https://docs.langchain.com/oss/python/langgraph/persistence.md#memory-store). It is also the default backend for [checkpoints](https://docs.langchain.com/oss/python/langgraph/persistence.md) (graph execution state). You can optionally store checkpoints in MongoDB instead—see [Configure checkpointer backend](../../Agent%20Server/Develop%20your%20application/Persistence/Configure%20checkpointer%20backend.md). PostgreSQL is always required regardless of the checkpointer backend.

## Redis

Redis is used in each Agent Server as a way for server and queue workers to communicate, and to store ephemeral metadata. No user or run data is stored in Redis.

### Communication

All runs in an Agent Server are executed by a pool of background workers that are part of each deployment. In order to enable some features for those runs (such as cancellation and output streaming) we need a channel for two-way communication between the server and the worker handling a particular run. We use Redis to organize that communication.

1. A Redis list is used as a mechanism to wake up a worker as soon as a new run is created. Only a sentinel value is stored in this list, no actual run information. The run information is then retrieved from PostgreSQL by the worker.
2. A combination of a Redis string and Redis PubSub channel is used for the server to communicate a run cancellation request to the appropriate worker.
3. A Redis PubSub channel is used by the worker to broadcast streaming output from an agent while the run is being handled. Any open `/stream` request in the server will subscribe to that channel and forward any events to the response as they arrive. No events are stored in Redis at any time.

### Ephemeral metadata

Runs in an Agent Server may be retried for specific failures (currently only for transient PostgreSQL errors encountered during the run). In order to limit the number of retries (currently limited to 3 attempts per run) we record the attempt number in a Redis string when it is picked up. This contains no run-specific info other than its ID, and expires after a short delay.

## Data plane features

This section describes various features of the data plane. For platform-specific behavior, see [Cloud platform features](../../Deploy%20to%20Cloud/Cloud%20platform%20features.md) or [Deploy to self-hosted](../../Deploy%20to%20Self-hosted/Deploy%20to%20self-hosted.md).

### Autoscaling

On LangSmith Cloud, [Dedicated deployments](../../Deploy%20to%20Cloud/Cloud%20platform%20features.md#scaling) autoscale separate API server and queue worker pools. Serverless deployments scale between zero and one replica.

On self-hosted data planes, autoscaling depends on the installed operator version and configuration. The current operator uses CPU for HPA scaling. With KEDA enabled, separate queue workers also scale on pending and running [runs](../../Agent%20Server/Capabilities/Runs/Runs.md), using whichever metric requires more replicas. Neither path uses memory as a scaling trigger.

The CPU target is 50% of the CPU limit: `queue_cpu_limit` for queue workers and `cpu_limit` for API servers. The CPU request does not affect the target. For example, `queue_cpu: 0.3` with `queue_cpu_limit: 1.8` gives queue workers a target of 900m per pod. The KEDA backlog target is 75% of the configured jobs per worker, rounded down to at least 1.

To lower a CPU request without changing when the deployment scales, send both the request and the limit in the `resource_spec`. If you omit the limit, it defaults to 2x the request, so lowering the request also lowers the scaling target. See [Resource spec](../Reference/Control%20Plane%20API/Control%20plane%20API%20reference%20for%20Agent%20Server%20hosting.md#resource-spec).

Scale-down behavior depends on the autoscaler and operator version. For self-hosted configuration details, see [Configure Agent Server for scale](../../Deploy%20to%20Self-hosted/Configure/Configure%20Agent%20Server%20for%20scale.md).

### MongoDB checkpointing

> [!NOTE]
>
> Available for [Cloud](../../../LangSmith%20setup/Cloud/Cloud%20%28SaaS%29.md) (with an externally managed MongoDB instance) and [Standalone](../../Deploy%20to%20Self-hosted/Self-host%20standalone%20servers.md) deployments.

You can use MongoDB as an alternative backend for checkpoint storage. When configured, MongoDB handles only checkpoint data—PostgreSQL remains required for all other server resources.

See [Configure checkpointer backend](../../Agent%20Server/Develop%20your%20application/Persistence/Configure%20checkpointer%20backend.md) for setup instructions.

### LangSmith tracing

Agent Server is automatically configured to send traces to LangSmith. See the table below for details with respect to each deployment option.

| Cloud | Hybrid | Self-Hosted |
| - | - | - |
| Required Trace to LangSmith SaaS. | Optional Disable tracing or trace to LangSmith SaaS. | Optional Disable tracing, trace to LangSmith SaaS, or trace to Self-Hosted LangSmith. |

### Telemetry

Agent Server is automatically configured to report telemetry metadata for billing purposes. See the table below for details with respect to each deployment option.

| Cloud | Hybrid | Self-Hosted |
| - | - | - |
| Telemetry sent to LangSmith SaaS. | Telemetry sent to LangSmith SaaS. | Self-reported usage (audit) for air-gapped license key. Telemetry sent to LangSmith SaaS for LangSmith License Key. |

### Licensing

Agent Server is automatically configured to perform license key validation. See the table below for details with respect to each deployment option.

| Cloud | Hybrid | Self-Hosted |
| - | - | - |
| LangSmith API Key validated against LangSmith SaaS. | LangSmith API Key validated against LangSmith SaaS. | Air-gapped license key or Platform License Key validated against LangSmith SaaS. |

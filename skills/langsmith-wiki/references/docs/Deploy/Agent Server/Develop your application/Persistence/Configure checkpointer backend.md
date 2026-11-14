# Configure checkpointer backend

> Configure Agent Server to use PostgreSQL, MongoDB, or a custom implementation for checkpoint storage.

[Agent Server](../../Capabilities/Agent%20Server.md) persists graph state using a checkpointer backend. By default, LangSmith stores checkpoints in PostgreSQL alongside other server data. You can switch to MongoDB or provide a custom implementation.

> [!NOTE]
>
> Regardless of the checkpointer backend, LangSmith always requires PostgreSQL for threads, runs, assistants, crons, and the [memory store](https://docs.langchain.com/oss/python/langgraph/stores.md). The checkpointer backend only controls where checkpoint data is stored.

## Available backends

| Backend | Storage | Configuration | Use case |
| - | - | - | - |
| `default` | PostgreSQL | None (built-in) | Standard deployments |
| `mongo` | MongoDB | `langgraph.json` or `LS_DEFAULT_CHECKPOINTER_BACKEND` env var | Teams with existing MongoDB infrastructure |
| `custom` | User-provided | `langgraph.json` | Custom storage backends (see [custom checkpointer](../../Server%20customization/Replace%20built-in%20backends/How%20to%20use%20a%20custom%20checkpointer.md)) |

## Default (PostgreSQL)

PostgreSQL is the default checkpointer backend. No configuration is needed. To use a custom PostgreSQL instance, set the [`POSTGRES_URI_CUSTOM`](../../../Deploy%20to%20Self-hosted/Reference/Self-hosted%20Agent%20Server%20environment%20variables.md) environment variable.

## Set up MongoDB checkpointing

> [!NOTE]
>
> Requires Agent Server v0.7.64 or later.

### Prerequisites

* A MongoDB **replica set** (standalone `mongod` is not supported). This can be a self-managed replica set, a `mongos` router, or a managed service like MongoDB Atlas.
* A connection URI that includes the database name in the path (e.g., `/langgraph`).

### Select the backend

Set the backend to `"mongo"` using one of these methods:

**In `langgraph.json`** (app-level—bundled with your application code):

```json
{
  "dependencies": ["."],
  "graphs": {
    "agent": "./agent.py:graph"
  },
  "checkpointer": {
    "backend": "mongo",
    "ttl": {
      "strategy": "delete",
      "default_ttl": 43200,
      "sweep_interval_minutes": 10
    }
  }
}
```

**Via environment variable** (platform-level—for operators managing standalone deployments):

```shell
LS_DEFAULT_CHECKPOINTER_BACKEND=mongo
```

The environment variable sets the default backend for agent servers that don't specify one in `langgraph.json`. If `langgraph.json` includes a `backend` value, it takes precedence.

### Provide the MongoDB URI

Set the `LS_MONGODB_URI` environment variable at deploy time:

```shell
LS_MONGODB_URI="mongodb://user:password@host:27017/langgraph?replicaSet=rs0"
```

### Connection URI requirements

The URI must:

* Point to a replica set member or `mongos` router
* Include the target database name in the path

Valid examples:

```
mongodb://user:password@host:27017/langgraph?replicaSet=rs0
mongodb://host1:27017,host2:27017,host3:27017/mydb?replicaSet=prod-rs
mongodb+srv://user:password@cluster.example.net/langgraph
```

### Deploy by environment

> [tab] Standalone (Kubernetes)
>
> The [langgraph-cloud Helm chart](https://github.com/langchain-ai/helm/blob/main/charts/langgraph-cloud/README.md) (v0.2.6+) has built-in MongoDB support. Enable it in your values file:
>
> **Bundled MongoDB** (development and testing):
>
> ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> mongo:
>   enabled: true
>   resources:
>     requests:
>       cpu: 500m
>       memory: 1Gi
>   persistence:
>     size: 8Gi
> ```
>
> The chart deploys a single-node MongoDB replica set and automatically configures the server to use it.
>
> **External MongoDB** (production):
>
> ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> mongo:
>   enabled: true
>   external:
>     enabled: true
>     connectionUrl: "mongodb://user:password@mongo.example.net:27017/langgraph?replicaSet=rs0"
> ```
>
> Or reference an existing Kubernetes secret:
>
> ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> mongo:
>   enabled: true
>   external:
>     enabled: true
>     existingSecretName: "my-mongo-secret"
> ```
>
> The secret must contain a `mongodb_connection_url` key.

> [tab] Standalone (Docker)
>
> If your `langgraph.json` already sets `backend` to `"mongo"`, you only need to provide the URI. Otherwise, set both environment variables:
>
> ```shell theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> docker run \
>     --env-file .env \
>     -p 8123:8000 \
>     -e REDIS_URI="redis://redis:6379" \
>     -e DATABASE_URI="postgres://postgres:postgres@postgres:5432/postgres" \
>     -e LS_DEFAULT_CHECKPOINTER_BACKEND=mongo \
>     -e LS_MONGODB_URI="mongodb://mongo:27017/langgraph?replicaSet=rs0" \
>     -e LANGSMITH_API_KEY="..." \
>     my-image
> ```
>
> See the [standalone server guide](../../../Deploy%20to%20Self-hosted/Self-host%20standalone%20servers.md) for a full Docker Compose example with MongoDB.

> [tab] Cloud
>
> Set `backend` to `"mongo"` in your `langgraph.json`, then add `LS_MONGODB_URI` as an environment variable in your deployment settings in the LangSmith UI.
>
> Your MongoDB instance must be reachable from the Cloud data plane. A managed service like [MongoDB Atlas](https://www.mongodb.com/atlas) works well for this.
>
> PostgreSQL is still auto-provisioned for non-checkpoint data.

## Custom checkpointer

To use a storage backend other than PostgreSQL or MongoDB, implement a custom [BaseCheckpointSaver](https://reference.langchain.com/python/langgraph/checkpoints/#langgraph.checkpoint.base.BaseCheckpointSaver). See [Add custom checkpointer](../../Server%20customization/Replace%20built-in%20backends/How%20to%20use%20a%20custom%20checkpointer.md) for details.

## Related

* [Configure TTLs](How%20to%20add%20TTLs%20to%20your%20application.md) for checkpoint and store item expiration
* [Persistence concepts](https://docs.langchain.com/oss/python/langgraph/persistence.md) in LangGraph
* [Data plane](../../../Get%20started/Deployment%20components/LangSmith%20data%20plane.md) architecture
* [Environment variables](../../../Deploy%20to%20Cloud/Reference/Cloud%20Agent%20Server%20environment%20variables.md) reference

# How to add TTLs to your application

> [!TIP]
>
> **Prerequisites**
> This guide assumes familiarity with [LangSmith](../../../../Monitor/Overview/LangSmith%20Observability.md), [Persistence](https://docs.langchain.com/oss/python/langgraph/persistence.md), and [Cross-thread persistence](https://docs.langchain.com/oss/python/langgraph/stores.md) concepts.

LangSmith persists both [checkpoints](https://docs.langchain.com/oss/python/langgraph/checkpointers.md#checkpoints) (thread state) and [cross-thread memories](https://docs.langchain.com/oss/python/langgraph/stores.md) (store items). You can configure Time-to-Live (TTL) policies in [`langgraph.json`](../Application%20structure.md#configuration-file) to manage the lifecycle of this data automatically, preventing indefinite accumulation.

## Configuring thread and checkpoint TTL

Checkpoints capture the state of conversation threads. Setting a TTL automatically deletes or prunes expired data.

Add a `checkpointer.ttl` configuration to your `langgraph.json` file:

```json
{
  "dependencies": ["."],
  "graphs": {
    "agent": "./agent.py:graph"
  },
  "checkpointer": {
    "ttl": {
      "strategy": "delete",
      "sweep_interval_minutes": 60,
      "default_ttl": 43200
    }
  }
}
```

* `strategy`: Specifies the action taken on expiration. Defaults to `"delete"`.
  * `"delete"`: Removes the entire thread including all associated run and checkpoint data when the TTL expires.
  * `"keep_latest"`: Retains the thread and latest checkpoint, but deletes older checkpoint data that subsequent runs won't need.
* `sweep_interval_minutes`: Defines how often, in minutes, the system checks for expired checkpoints. Defaults to 5 minutes.
* `default_ttl`: Sets the default TTL window in minutes (e.g., 43200 minutes = 30 days). The `delete` window starts when the TTL is applied and does not refresh with activity. The `keep_latest` window refreshes when a run finishes or thread state is updated. If omitted, threads do not expire by default.
* `sweep_limit`: (*Agent server v0.8+*) Sets how many threads the sweeper processes in a single iteration. Defaults to `10000` (Agent server v0.12+) or `1000` (Agent server v0.8-0.11).

> [!NOTE]
>
> Global TTL configuration applies to new threads. The `delete` strategy does not apply retroactively to existing threads. The `keep_latest` strategy applies to an existing thread after a run finishes or its state is updated; inactive existing threads remain unchanged.

## Configuring store item TTL

Store items allow cross-thread data persistence. Configuring TTL for store items helps manage memory by removing stale data.

Add a `store.ttl` configuration to your `langgraph.json` file:

```json
{
  "dependencies": ["."],
  "graphs": {
    "agent": "./agent.py:graph"
  },
  "store": {
    "ttl": {
      "refresh_on_read": true,
      "sweep_interval_minutes": 120,
      "default_ttl": 10080
    }
  }
}
```

* `refresh_on_read`: (Optional, default `true`) If `true`, accessing an item via `get` or `search` resets its expiration timer. If `false`, TTL only refreshes on `put`.
* `sweep_interval_minutes`: (Optional, default `5`) Defines how often, in minutes, the system checks for expired items.
* `default_ttl`: (Optional) Sets the default lifespan of store items in minutes (e.g., 10080 minutes = 7 days). Applies only to items created after this configuration is deployed; existing items are not changed. If you need to clear older items, delete them manually. If omitted, items do not expire by default.

## Combining TTL configurations

You can configure TTLs for both checkpoints and store items in the same `langgraph.json` file to set different policies for each data type. Here is an example:

```json
{
  "dependencies": ["."],
  "graphs": {
    "agent": "./agent.py:graph"
  },
  "checkpointer": {
    "ttl": {
      "strategy": "delete",
      "sweep_interval_minutes": 60,
      "default_ttl": 43200
    }
  },
  "store": {
    "ttl": {
      "refresh_on_read": true,
      "sweep_interval_minutes": 120,
      "default_ttl": 10080
    }
  }
}
```

## Configure per-thread TTL

You can apply [TTL configurations per-thread](../../../Get%20started/Reference/Deployment%20SDK.md).

```python
thread = await client.threads.create(
    ttl={
        "strategy": "delete",
        "ttl": 43200  # 30 days in minutes
    }
)
```

> [!NOTE]
>
> A thread-level TTL overrides the default TTL for that thread and uses the strategy behavior described above.

## Runtime overrides

For store items, pass `ttl` to `put` to override the default lifespan. Pass `refresh_ttl` to `get` or `search` to control whether reads refresh expiration.

## Deployment process

After configuring TTLs in `langgraph.json`, deploy or restart your LangGraph application for the changes to take effect. Use [`langgraph dev`](../../../Get%20started/Develop%20%26%20test/Local%20development%20%26%20testing.md#langgraph-dev) for local development or [`langgraph up`](../../../Get%20started/Develop%20%26%20test/Local%20development%20%26%20testing.md#langgraph-up) for Docker deployment.

For details on other configurable options, refer to the [LangGraph CLI reference page](../../../Get%20started/Reference/LangGraph%20CLI.md#configuration-file).

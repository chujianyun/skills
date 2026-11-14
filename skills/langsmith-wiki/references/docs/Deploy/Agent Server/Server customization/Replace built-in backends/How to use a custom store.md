# How to use a custom store

> Replace the built-in Postgres store with a custom BaseStore implementation in your agent deployment.

When deploying agents to LangSmith, the server provides a built-in Postgres-backed long-term memory store with optional vector search via pgvector. You can replace this with your own [BaseStore](https://reference.langchain.com/python/langchain-core/stores/BaseStore) implementation to use a different storage backend, custom indexing, or specialized search capabilities.

You provide a path to an async context manager that yields a `BaseStore` instance, and the server manages the store's lifecycle automatically.

> [!WARNING]
>
> Custom stores are in **alpha**. This feature may experience breaking changes in minor version updates.

## Define the store

Starting from an **existing** LangSmith application, create a file that defines an async context manager yielding your custom store. If you are beginning a new project, you can create an app from a template using the CLI.

```bash
langgraph new --template=new-langgraph-project-python my_new_project
```

The async context manager pattern lets the server open and close the store connection at the right points in the application lifecycle. The following example uses `AsyncSqliteStore` with semantic search:

> [!NOTE]
>
> SQLite is not recommended for use in production deployments.

```python
# ./src/agent/store.py
import contextlib

from langchain.embeddings import init_embeddings
from langgraph.store.base import IndexConfig
from langgraph.store.sqlite import AsyncSqliteStore

embeddings = init_embeddings("openai:text-embedding-3-small")


@contextlib.asynccontextmanager
async def generate_store():
    """Yield a BaseStore, open for the duration of the server."""
    async with AsyncSqliteStore.from_conn_string(
        "./custom_store.sql",
        index=IndexConfig(
            dims=1536,
            embed=embeddings,
            fields=["$"],
        ),
    ) as store:
        await store.setup()
        yield store
```

> [!NOTE]
>
> When a custom store is configured, it **replaces** the built-in Postgres store entirely. Capabilities like semantic search and TTL sweeping depend on your implementation.

## Configure `langgraph.json`

Add the `store` key to your [`langgraph.json` configuration file](../../Develop%20your%20application/Application%20structure.md#configuration-file-concepts). The `path` points to the async context manager you [defined earlier](#define-the-store).

```json
{
  "dependencies": ["."],
  "graphs": {
    "agent": "./src/agent/graph.py:graph"
  },
  "env": ".env",
  "store": {
    "path": "./src/agent/store.py:generate_store"
  }
}
```

## Start server

Test the server out locally:

```bash
langgraph dev --no-browser
```

The server logs will confirm that your custom store is active:

```
Using custom store. Skipping store TTL sweeper.
```

## Deploying

You can deploy this app as-is to LangSmith or to your self-hosted platform.

## Next steps

* [Use a custom checkpointer](How%20to%20use%20a%20custom%20checkpointer.md) to replace the built-in checkpoint storage.
* Learn about [persistence and memory](https://docs.langchain.com/oss/python/langgraph/persistence.md) in LangGraph.

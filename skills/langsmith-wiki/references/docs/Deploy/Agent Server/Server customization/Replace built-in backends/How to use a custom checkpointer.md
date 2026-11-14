# How to use a custom checkpointer

> Replace the built-in Postgres checkpointer with a custom BaseCheckpointSaver implementation in your agent deployment.

When deploying agents to LangSmith, the server provides a built-in Postgres-backed checkpointer that handles state persistence across graph runs. You can replace this with your own [BaseCheckpointSaver](https://reference.langchain.com/python/langgraph/checkpoints/#langgraph.checkpoint.base.BaseCheckpointSaver) implementation to use a different storage backend.

You provide a path to an async context manager that yields a `BaseCheckpointSaver` instance, and the server manages its lifecycle automatically.

> [!WARNING]
>
> Custom checkpointers are in **alpha**. This feature may experience breaking changes in minor version updates.

> [!TIP]
>
> To use MongoDB instead of PostgreSQL for checkpoint storage, see [Configure checkpointer backend](../../Develop%20your%20application/Persistence/Configure%20checkpointer%20backend.md). This page is for implementing a fully custom storage backend.

## Define the checkpointer

Starting from an **existing** LangSmith application, create a file that defines an async context manager yielding your custom checkpointer. If you are beginning a new project, you can create an app from a template using the CLI.

```bash
langgraph new --template=new-langgraph-project-python my_new_project
```

The async context manager pattern lets the server open and close the database connection at the right points in the application lifecycle:

```python
# ./src/agent/checkpointer.py
import contextlib

class MyCheckpointer(BaseCheckpointSaver):
    def __init__(self):
        super().__init__()
        # Initialize your custom checkpointer here
    ...

    @contextlib.asynccontextmanager
    async def aget(self, config: RunnableConfig):
        # Your custom logic to create a connection pool and initialize your checkpointer here.
        yield


@contextlib.asynccontextmanager
async def generate_checkpointer():
    """Yield a BaseCheckpointSaver, open for the duration of the server."""
    async with AsyncSqliteSaver.from_conn_string("./checkpoints.db") as saver:
        await saver.setup()
        yield saver
```

## Test against the conformance suite

Most open source checkpointer implementations do not yet implement all the operations required by Agent Server. Before configuring your checkpointer, validate it against the conformance test suite to ensure compatibility.

Install the package:

```bash
pip install langgraph-checkpoint-conformance
```

Register your checkpointer and run validation:

```python
import asyncio

from langgraph.checkpoint.conformance import checkpointer_test, validate


@checkpointer_test(name="MyCheckpointer")
async def my_checkpointer():
    async with MyCheckpointer(...) as saver:
        yield saver


async def main():
    report = await validate(my_checkpointer)
    report.print_report()
    assert report.passed_all_base()


asyncio.run(main())
```

The suite auto-detects which extended capabilities your checkpointer implements and runs the appropriate tests. You can also run it as a pytest test:

```python
import pytest

from langgraph.checkpoint.conformance import checkpointer_test, validate


@checkpointer_test(name="MyCheckpointer")
async def my_checkpointer():
    async with MyCheckpointer(...) as saver:
        yield saver


@pytest.mark.asyncio
async def test_conformance():
    report = await validate(my_checkpointer)
    report.print_report()
    assert report.passed_all_base()
```

To view the full list of base and extended operations that the suite validates, refer to the [capabilities](#capabilities) section.

## Configure `langgraph.json`

Add the `checkpointer` key to your [`langgraph.json` configuration file](../../Develop%20your%20application/Application%20structure.md#configuration-file-concepts). The `path` points to the async context manager you [defined earlier](#define-the-checkpointer).

```json
{
  "dependencies": ["."],
  "graphs": {
    "agent": "./src/agent/graph.py:graph"
  },
  "env": ".env",
  "checkpointer": {
    "path": "./src/agent/checkpointer.py:generate_checkpointer"
  }
}
```

## Start server

Test the server out locally:

```bash
langgraph dev --no-browser
```

The server logs will confirm that your custom checkpointer is active.

## Capabilities

The server checks your checkpointer for **base** (required) and **extended** (optional) capabilities at startup. If an extended capability is missing, the server either uses a fallback or disables the corresponding feature.

### Base capabilities (required)

| Method | Description |
| - | - |
| `aput` | Store a checkpoint |
| `aput_writes` | Store pending writes |
| `aget_tuple` | Retrieve a checkpoint |
| `alist` | List checkpoints |
| `adelete_thread` | Delete a thread |

### Extended capabilities (optional)

| Method | Description | Fallback if missing |
| - | - | - |
| `adelete_for_runs` | Delete checkpoints for specific runs | Rollback multitask strategy unavailable |
| `acopy_thread` | Copy a thread | Slow fallback (re-inserts checkpoints one by one) |
| `aprune` | Prune thread history | Thread history pruning unavailable |

## Deploying

You can deploy this app as-is to LangSmith or to your self-hosted platform.

## Next steps

* [Build a custom checkpointer](https://docs.langchain.com/oss/python/langgraph/checkpointers.md#build-a-custom-checkpointer) including delta channel support.
* [Use a custom store](How%20to%20use%20a%20custom%20store.md) to replace the built-in long-term memory store.
* Learn about [persistence and memory](https://docs.langchain.com/oss/python/langgraph/persistence.md) in LangGraph.

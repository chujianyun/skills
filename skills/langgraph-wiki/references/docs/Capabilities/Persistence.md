# Persistence

> LangGraph's persistence layer gives agents short-term memory through checkpointers and long-term memory through stores.

Persistence lets LangGraph applications keep useful information beyond a single graph run. It matters when an agent needs to continue a conversation, resume after an interruption, recover from a failure, or remember information across interactions.

LangGraph provides two complementary persistence systems:

* **[Checkpointers](Checkpointers.md)** persist a thread's graph state as checkpoints. Use them for short-term, thread-scoped memory, including conversation continuity, human-in-the-loop workflows, time travel, and fault tolerance.
* **[Stores](Stores.md)** persist application-defined data outside the graph state. Use them for long-term, cross-thread memory, including user preferences, facts, and shared knowledge.

Most applications can use both: a [checkpointer](Checkpointers.md) tracks the current thread, and a [store](Stores.md) tracks durable information across threads.

## Quickstart

Compile your graph with a checkpointer, a store, or both:

```python
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore

checkpointer = InMemorySaver()
store = InMemoryStore()

graph = builder.compile(checkpointer=checkpointer, store=store)

result = graph.invoke(
    {"messages": [{"role": "user", "content": "Hi, my name is Bob."}]},
    {"configurable": {"thread_id": "thread-1"}},
)
```

> [!NOTE]
>
> **Agent Server handles persistence automatically**
> When using the [Agent Server](https://docs.langchain.com/langsmith/agent-server.md), you do not need to implement or configure checkpointers or stores manually. The server handles persistence infrastructure behind the scenes.

## Checkpointer vs. store

| | Checkpointer | Store |
| - | - | - |
| Persists | Graph state snapshots | Application-defined key-value data |
| Scope | A single thread | Across threads |
| Memory type | Short-term, thread-scoped memory | Long-term, cross-thread memory |
| Use for | Conversation continuity, human-in-the-loop, time travel, and fault tolerance | User preferences, facts, and shared knowledge |
| Access pattern | Pass a `thread_id` in graph config | Read and write items from nodes or application code |
| Full guide | [Checkpointers](Checkpointers.md) | [Stores](Stores.md) |

## Troubleshooting common issues

### PostgresSaver: `thread_id` too long

When using `PostgresSaver` (or `AsyncPostgresSaver`), the `thread_id` is stored in a column with limited length. If your `thread_id` exceeds the column size, you will see a database error.

**Fix:** Keep `thread_id` values under 255 characters. Use a UUID or hash if you need deterministic IDs:

```python
from langchain_core.utils.uuid import uuid7
config = {"configurable": {"thread_id": str(uuid7())[:255]}}
```

### `MemorySaver` does not persist between restarts

`MemorySaver` and `InMemorySaver` store checkpoints in RAM. When the process restarts, all checkpoints are lost.

**Fix:** Use a persistent checkpointer for production:

* `PostgresSaver`: PostgreSQL with async support
* `SqliteSaver`: Local file-based storage for development

### Checkpoints growing unboundedly

Over long conversations, checkpoints accumulate. This can increase latency and storage costs.

**Fix:** Prune old checkpoints periodically or set a retention policy:

```python
from langgraph.checkpoint.postgres import PostgresSaver

checkpointer = PostgresSaver.from_conn_string("postgresql://...")
checkpointer.setup()  # Creates tables with indexes
# Consider adding a cron job to delete checkpoints older than N days
```

### State access from parent graph to subgraph

When a subgraph updates state, the parent graph may not see the changes immediately. This is because each subgraph manages its own checkpoint namespace.

**Fix:** Use [shared state via Store](Stores.md) for data that needs to cross graph boundaries, or configure your subgraph to write to the parent checkpoint.

## Next steps

* [Use checkpointers](Checkpointers.md) to persist and inspect thread state.
* [Use stores](Stores.md) to persist durable data across threads.

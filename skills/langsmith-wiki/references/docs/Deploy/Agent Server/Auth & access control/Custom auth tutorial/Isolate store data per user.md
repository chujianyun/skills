# Isolate store data per user

> Scope long-term store data to each authenticated user in LangSmith Agent Server using auth handlers.

Every [Agent Server](../../../Get%20started/LangSmith%20Agent%20Server.md) includes a Postgres-backed [store](https://docs.langchain.com/oss/python/langgraph/stores.md) for long-term memory and cross-thread data. By default, store namespaces are shared across all callers. To give each user their own isolated store, configure [custom authentication](../Add%20custom%20authentication.md) and add a store [authorization handler](../Authentication%20%26%20access%20control.md#authorization) that rewrites namespaces to include the authenticated user's identity.

This guide shows how to configure that isolation in LangSmith Agent Server. The same pattern works for [self-hosted](../../../../LangSmith%20setup/Self-hosted/Self-hosted%20LangSmith.md) deployments with custom auth enabled.

## How it works

Store items are organized by a **namespace** tuple (for example, `("memories", "preferences")`) and a **key**. Unlike threads and assistants, store namespaces are defined by your application, so authorization works differently:

1. Your `@auth.authenticate` handler validates the caller and returns a unique `identity` for each user.
2. Your `@auth.on.store` handler either **validates** that the namespace starts with that identity, or **rewrites** the namespace to prepend it.
3. The server uses the validated or rewritten namespace for the actual read or write.

A user who writes to logical namespace `("memories",)` with automatic prefix rewriting actually stores data at `("user-123", "memories")`. Another user cannot read or overwrite that data because their requests are scoped to `("user-456", ...)`.

> [!NOTE]
>
> Store authorization handlers receive a **mutable** `value` dict. Changes to `value["namespace"]` take effect on the operation. You do not return a metadata filter like you do for threads.

## Prerequisites

* An Agent Server with [custom authentication](Set%20up%20custom%20authentication.md) configured.
* An `@auth.authenticate` handler that returns a stable, unique `identity` for each end user.

## Configure auth in LangSmith Agent Server

Point your deployment at your auth module in [`langgraph.json`](../../Develop%20your%20application/Application%20structure.md#configuration-file-concepts):

```json
{
  "dependencies": ["."],
  "graphs": {
    "agent": "./src/agent/graph.py:graph"
  },
  "auth": {
    "path": "./src/security/auth.py:auth"
  }
}
```

The `auth` object must expose an instance of `langgraph_sdk.Auth` (commonly named `auth`).

## Choose a store authorization pattern

Store isolation requires a `@auth.on.store` handler. Two common patterns work well; pick one based on where you want user scoping to live.

| Pattern | Where user scope is set | Best when |
| - | - | - |
| **Explicit namespace + deny** | Application code puts `user_id` first in every namespace | You already pass user identity into graph code, or you want namespaces to reflect the full storage path |
| **Automatic prefix rewriting** | Auth handler prepends `ctx.user.identity` to logical namespaces | You want simpler agent code and transparent isolation at the API layer |

Both patterns use a single `@auth.on.store` handler that covers all store actions (`put`, `get`, `search`, `delete`, and `list_namespaces`). You only need action-specific handlers such as `@auth.on.store.put` if you want different rules per operation.

> [!TIP]
>
> If you use a global `@auth.on` handler that denies unhandled requests, register `@auth.on.store` explicitly so store operations are allowed. See the [Auth reference](https://reference.langchain.com/python/langgraph-sdk/auth/Auth) for action-specific handler names.

### Explicit namespace + deny

Your application code includes the user's identity as the first segment of every namespace (for example, `("user-123", "memories")`). The auth handler validates that the caller matches that prefix and rejects mismatches:

```python
from langgraph_sdk import Auth

auth = Auth()

# ... your @auth.authenticate handler ...

@auth.on.store
async def authorize_store(
    ctx: Auth.types.AuthContext,
    value: Auth.types.on.store.value,
):
    """Require the user identity as the first namespace segment."""
    namespace = tuple(value["namespace"])
    if not namespace or namespace[0] != ctx.user.identity:
        raise Auth.exceptions.HTTPException(
            status_code=403,
            detail="Not authorized to access this namespace.",
        )
```

This pattern makes the storage layout explicit in your graph code. A request for namespace `("user-456", "memories")` fails immediately if the authenticated user is `user-123`. The tradeoff is that every store call in your agent must include the user prefix, typically from runtime context such as `config["configurable"]["langgraph_auth_user_id"]`.

### Automatic prefix rewriting

Your application code uses logical namespaces without a user prefix (for example, `("memories", "preferences")`). The auth handler prepends the authenticated user's identity on every store operation:

```python
from langgraph_sdk import Auth

auth = Auth()

# ... your @auth.authenticate handler ...

@auth.on.store
async def scope_store(
    ctx: Auth.types.AuthContext,
    value: Auth.types.on.store.value,
):
    """Isolate store data per user by rewriting namespaces."""
    namespace = tuple(value["namespace"]) if value.get("namespace") else ()
    if not namespace or namespace[0] != ctx.user.identity:
        namespace = (ctx.user.identity, *namespace)
    value["namespace"] = namespace
```

When a client calls `list_namespaces` without a prefix, `value["namespace"]` is empty. The handler above treats an empty namespace as `(ctx.user.identity,)`, so the user only sees their own namespaces.

This pattern keeps agent code simpler because the auth layer handles user isolation transparently. The tradeoff is that you must not also prefix namespaces in application code, or you will double-scope data and break reads. Pick one scoping layer: auth rewriting **or** application-level namespaces, not both.

## Use namespaces in agent code

If you use automatic prefix rewriting, your graph code uses logical namespaces without the user prefix. The auth layer adds the user scope automatically at request time. Put the following in your graph nodes or tools (for example, `graph.py`):

```python
from langgraph.store.base import BaseStore

async def save_preference(state: State, *, store: BaseStore):
    await store.aput(
        ("memories", "preferences"),  # logical namespace
        "settings",
        {"theme": "dark"},
    )

async def load_preference(state: State, *, store: BaseStore):
    item = await store.aget(
        ("memories", "preferences"),
        "settings",
    )
    return item.value if item else {}
```

When User A calls the store API, the server persists data at `("user-a", "memories", "preferences")`. User B's requests never reach that namespace.

If you use **explicit namespace + deny**, include the user identity in every namespace from your graph code instead:

```python
from langchain_core.runnables import RunnableConfig
from langgraph.store.base import BaseStore

async def save_preference(state: State, *, store: BaseStore, config: RunnableConfig):
    user_id = config["configurable"]["langgraph_auth_user_id"]
    await store.aput(
        (user_id, "memories", "preferences"),
        "settings",
        {"theme": "dark"},
    )
```

### Deep Agents and StoreBackend

If you use [Deep Agents](https://docs.langchain.com/oss/python/deepagents/overview.md) with a [`StoreBackend`](https://reference.langchain.com/python/deepagents/backends/store/StoreBackend), align your namespace factory with the auth-scoped layout. When auth prepends `ctx.user.identity`, use logical namespaces in the backend and let auth handle user isolation:

```python
from deepagents.backends import StoreBackend

StoreBackend(
    namespace=lambda rt: ("memories",),  # auth adds user identity
)
```

Alternatively, if you scope by user inside the graph (for example, with `rt.server_info.user.identity`), ensure your auth handler does not double-prefix namespaces. Pick one scoping layer: auth rewriting **or** application-level namespaces, not both.

For more on namespace design, see [Deep Agents backends](https://docs.langchain.com/oss/python/deepagents/backends.md#namespace-factories) and [user-scoped memory](https://docs.langchain.com/oss/python/deepagents/memory.md#user-scoped-memory).

## Test store isolation

With `langgraph dev` running and two test users configured in your auth handler, verify that store data does not leak across users:

```python
import asyncio

from langgraph_sdk import get_client


async def main():
    alice = get_client(
        url="http://localhost:60058",
        headers={"Authorization": "Bearer user1-token"},
    )
    bob = get_client(
        url="http://localhost:60058",
        headers={"Authorization": "Bearer user2-token"},
    )

    # Alice writes a store item
    await alice.store.put_item(
        ["memories"],
        key="note",
        value={"text": "Alice private note"},
    )

    # Bob cannot read Alice's item
    bob_item = await bob.store.get_item(["memories"], key="note")
    if bob_item is None or bob_item["value"]["text"] != "Alice private note":
        print("✅ Bob correctly denied access to Alice's item")
    else:
        print("❌ Bob should not see Alice's store item")

    # Bob writes his own item at the same logical namespace
    await bob.store.put_item(
        ["memories"],
        key="note",
        value={"text": "Bob private note"},
    )

    alice_item = await alice.store.get_item(["memories"], key="note")
    bob_item = await bob.store.get_item(["memories"], key="note")
    assert alice_item["value"]["text"] == "Alice private note"
    assert bob_item["value"]["text"] == "Bob private note"
    print("✅ Each user sees only their own store data")


if __name__ == "__main__":
    asyncio.run(main())
```

## Combine with thread isolation

Store isolation and [thread isolation](Make%20conversations%20private.md) solve different problems:

| Concern | Mechanism | Scopes |
| - | - | - |
| Conversation history | Thread metadata filters (`owner`) | Per-thread checkpoints and messages |
| Long-term memory | Store namespace rewriting | Cross-thread memories, preferences, and documents |

For multi-user agents, configure both. See [Make conversations private](Make%20conversations%20private.md) for thread and run scoping.

## See also

* [Authentication and access control](../Authentication%20%26%20access%20control.md)
* [Set up custom authentication](Set%20up%20custom%20authentication.md)
* [Make conversations private](Make%20conversations%20private.md)
* [Semantic search in deployments](../../Develop%20your%20application/Persistence/How%20to%20add%20semantic%20search%20to%20your%20agent%20deployment.md)
* [LangGraph stores](https://docs.langchain.com/oss/python/langgraph/stores.md)

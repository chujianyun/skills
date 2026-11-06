# Backward compatibility

> Update LangGraph graph code in production without breaking in-flight runs.

Software needs to change in production. New requirements, bug fixes, and refactors all eventually land in your graph code. Because LangGraph runs the latest deployed graph against state that has been [persisted](../Capabilities/Persistence.md) for existing threads, every change you ship is effectively a backward-compatible API change with respect to your existing checkpoints.

Unlike workflow engines that pin a run to the version of code it started with, LangGraph applies the latest graph immediately to *every* thread, both new threads and threads that resume from a checkpoint. This is convenient: bug fixes propagate to in-flight conversations and agents without ceremony. It also means you must reason about how each change interacts with runs that started under the previous version of the code.

There are three categories of compatibility issues to watch for, in roughly the order you will encounter them:

1. [Technical compatibility](#technical-compatibility): The most common; the new code must still load and execute against existing State.
2. [Business compatibility](#business-compatibility): Less common; existing runs should keep following the old business logic even though the code has changed.
3. [Non-determinism](#non-determinism): Only applies to the [Functional API](../Advanced/Build%20with%20the%20Functional%20API/Functional%20API%20overview.md).

> [!TIP]
>
> For a short summary of which graph topology and state changes the runtime supports by default, see [Graph migrations](../Build%20with%20the%20Graph%20API/Graph%20API%20overview.md#graph-migrations). The rest of this page covers the patterns you can apply when a change falls outside that supported set.

## Technical compatibility

Technical compatibility is the equivalent of an API breaking change in a microservice. The "API" here is the contract between your graph code and the data already persisted by the [checkpointer](../Capabilities/Checkpointers.md#checkpointer-libraries) for existing threads. When a thread resumes, LangGraph deserializes the saved state, dispatches it to a node by name, and expects the node to return values that fit the state schema.

Common technical breakages:

* **Renaming or removing a node** while threads are paused at or about to enter that node, for example at an [`interrupt`](https://reference.langchain.com/python/langgraph/types/interrupt) or via a checkpointed conditional edge that still routes to the old name. On resume, LangGraph cannot find the node by its saved name and the run fails. The starting point for resuming a run is the beginning of the node where execution stopped, so a missing node has nowhere to resume from.
* **Renaming or removing a State key** that older checkpoints still contain or that downstream nodes still read.
* **Tightening a State field**, such as making an `Optional` field required, narrowing a type, or adding a new required field with no default. Existing checkpoints will not satisfy the new schema.

Edge topology itself is *not* persisted in the checkpoint. Adding, removing, or rerouting edges between nodes that still exist is safe for in-flight threads. Per the [Graph migrations](../Build%20with%20the%20Graph%20API/Graph%20API%20overview.md#graph-migrations) summary, the only topology change that can break an interrupted thread is renaming or removing a node.

### Recommended patterns

* Add new state fields as `NotRequired` (or `Optional[...] = None`) so old checkpoints still validate:

  ```python
  from typing import NotRequired
  from typing_extensions import TypedDict

  class State(TypedDict):
      messages: list
      summary: NotRequired[str]  # [!code ++]
  ```

* Treat removals as deprecations. Keep the field defined on the state for at least one drain cycle, even if no node reads it, so existing checkpoints continue to load.

* Rename through *add-then-remove*. Add the new field or node alongside the old one, dual-write or route to both for a deprecation window, then remove the old one once you have confirmed no in-flight thread depends on it.

* Keep node functions tolerant of unknown keys. `TypedDict` ignores extra keys at runtime, so leftover state from an older code version will not raise unless a node explicitly reads a missing key.

* Use [time travel](../Capabilities/Use%20time-travel.md) and [`graph.get_state`](https://reference.langchain.com/python/langgraph/graphs/#langgraph.graph.state.CompiledStateGraph.get_state) to spot-check existing threads against the new code in a staging deployment before rolling out.

### Detecting in-flight threads

Before you remove a node, rename a State key, or otherwise make a change that older threads cannot tolerate, you want to know whether any threads are currently parked on the version of the code you are about to drop. LangGraph itself does not maintain a search index over thread state, so the answer depends on where your graph runs.

**If you deploy to [LangSmith](https://docs.langchain.com/langsmith/deployment.md).** Use the Agent Server's thread search to filter by status. The `status` field accepts `idle`, `busy`, `interrupted`, and `error`, so you can bulk-query for `interrupted` or `busy` threads, optionally narrowed with metadata filters. See [Filter by thread status](https://docs.langchain.com/langsmith/use-threads.md#filter-by-thread-status) and [List threads](https://docs.langchain.com/langsmith/use-threads.md#list-threads).

**Anywhere LangGraph runs.** Use [LangSmith tracing](LangSmith%20Observability.md) to monitor which nodes are being entered and exited in production. This is the most reliable signal that a node or state field is no longer reachable in any active code path.

**When you already have a `thread_id`.** Inspect that single thread directly:

* [`graph.get_state(config)`](https://reference.langchain.com/python/langgraph/graphs/#langgraph.graph.state.CompiledStateGraph.get_state) returns the latest checkpoint, including which node the thread is paused at and any pending interrupts.
* [`graph.get_state_history(config)`](https://reference.langchain.com/python/langgraph/graphs/#langgraph.graph.state.CompiledStateGraph.get_state_history) returns the full chronological list of checkpoints for the thread.

When in doubt, keep the deprecated node or field in place until both the Agent Server thread list and tracing show no further activity on it.

## Business compatibility

Sometimes a change is technically valid (every existing checkpoint still loads and every node still resolves), but the *meaning* of the new graph differs from the old one. The new behavior is correct for new threads, and you do not want to retroactively apply it to threads that started under the old logic.

For example, suppose your graph runs `intake → triage → respond`, and you decide to insert a new `policy_check` step between `triage` and `respond`:

* Threads that have already passed `triage` should continue straight to `respond` (the old flow).
* New threads should run the full new flow.

The recommended pattern is to record the relevant *behavioral version* on the state at thread start, then branch on it with a [conditional edge](../Build%20with%20the%20Graph%20API/Graph%20API%20overview.md#conditional-edges):

```python
from typing import NotRequired
from typing_extensions import TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    request: str
    flow_version: NotRequired[int]
    response: NotRequired[str]


def intake(state: State) -> dict:
    # Stamp new threads with the current flow version. Existing threads
    # that resume past `intake` keep whatever value was already saved.
    return {"flow_version": state.get("flow_version", 2)}


def triage(state: State) -> dict: ...
def policy_check(state: State) -> dict: ...
def respond(state: State) -> dict: ...


def after_triage(state: State) -> str:
    if state.get("flow_version", 1) >= 2:
        return "policy_check"
    return "respond"


builder = StateGraph(State)
builder.add_node("intake", intake)
builder.add_node("triage", triage)
builder.add_node("policy_check", policy_check)
builder.add_node("respond", respond)
builder.add_edge(START, "intake")
builder.add_edge("intake", "triage")
builder.add_conditional_edges("triage", after_triage, ["policy_check", "respond"])
builder.add_edge("policy_check", "respond")
builder.add_edge("respond", END)

graph = builder.compile()
```

Old threads that resume after `triage` read `flow_version` from their saved state (or fall through to the v1 default) and skip `policy_check`. New threads start at `intake`, are stamped with `flow_version=2`, and run the new path. Once all v1 threads have completed, you can remove the version flag and the conditional edge.

This pattern only works if you set the version *at thread start*, before any branch that needs to be versioned. Setting it later means existing threads will not have it set when they need it.

## Non-determinism

This category only applies to the [Functional API](../Advanced/Build%20with%20the%20Functional%20API/Functional%20API%20overview.md) and to [**tasks**](../Advanced/Build%20with%20the%20Functional%20API/Functional%20API%20overview.md#task) or [`interrupt`](https://reference.langchain.com/python/langgraph/types/interrupt) calls inside a [Graph API](../Build%20with%20the%20Graph%20API/Graph%20API%20overview.md) **node**. Plain Graph API **nodes** [re-run from the start of the node function](../Build%20with%20the%20Graph%20API/Graph%20API%20overview.md#re-execution-and-idempotency) on resume; design side effects to be idempotent, but you do not need to preserve task call order unless you use **tasks** or [`interrupt`](https://reference.langchain.com/python/langgraph/types/interrupt) in that **node**.

A Functional API **entrypoint** compiles to a single **node** that replays the entrypoint body from the beginning when a run resumes, using cached [`@task`](https://reference.langchain.com/python/langgraph/func/task) results to skip work that has already been done. Two kinds of changes break this model:

* **Adding, removing, or reordering `@task` calls or [`interrupt`](https://reference.langchain.com/python/langgraph/types/interrupt) calls** that come *before* the resume point. LangGraph matches cached results and resume values to calls by their position in the replay, so shifting that position can cause the wrong cached value to be replayed against a different call.
* **Introducing non-deterministic operations outside of a `@task`**, such as `time.time()`, `random.random()`, or a network call inlined in the entrypoint body. On replay these produce different values than they did on the first run, which can change the control flow.

For a deeper treatment with examples, see [Determinism](../Advanced/Build%20with%20the%20Functional%20API/Functional%20API%20overview.md#determinism) and [Common pitfalls](../Advanced/Build%20with%20the%20Functional%20API/Functional%20API%20overview.md#common-pitfalls) in the Functional API guide.

If you need to make non-trivial code changes to an `@entrypoint` that has in-flight runs, the safest options are:

* Let in-flight runs drain before deploying the change.
* Wrap any new logic in a new `@task` so its results are checkpointed independently.
* Register a new entrypoint under a new graph name in `langgraph.json` for the new behavior, and route new threads to it.

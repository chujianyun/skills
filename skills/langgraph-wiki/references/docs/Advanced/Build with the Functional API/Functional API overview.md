# Functional API overview

> Learn Functional API entrypoints and tasks, how checkpointing and replay work, and how to avoid common resume pitfalls.

The **Functional API** adds LangGraph features ([persistence](../../Capabilities/Persistence.md), [memory](../../Capabilities/Memory.md), [human-in-the-loop](../../Capabilities/Interrupts.md), and [streaming](../../Capabilities/Streaming.md)) to ordinary functions. Use standard language control flow (`if` / `else`, loops, and function calls) instead of declaring a graph of nodes and edges.

This page is the concept reference for entrypoints, tasks, checkpointing, and resume rules. For a design walkthrough, see [Thinking in the Functional API](Thinking%20in%20the%20Functional%20API.md). For an ordered build path, see the [Build checklist for the Functional API](Build%20checklist%20for%20the%20Functional%20API.md).

The Functional API uses two building blocks:

* **`@entrypoint`**: Marks a function as the start of a workflow. It manages execution, interrupts, and checkpointing.
* **`@task`**: Marks a discrete unit of work (for example, an API call). Tasks return a future-like object that you can await or resolve with `.result()`.

## Functional API vs. Graph API

This comparison is optional if you already chose the Functional API. For a side-by-side decision guide, see [Choosing between Graph and Functional APIs](../../Get%20started/Choosing%20between%20Graph%20and%20Functional%20APIs.md). Both APIs share the same underlying runtime, so you can use them together in the same application.

High-level differences:

* **Control flow**: The Functional API uses standard language constructs. The [Graph API](../../Build%20with%20the%20Graph%20API/Graph%20API%20overview.md) uses nodes and edges.
* **State**: The Graph API requires declaring [state](../../Build%20with%20the%20Graph%20API/Graph%20API%20overview.md#state) and often [reducers](../../Build%20with%20the%20Graph%20API/Graph%20API%20overview.md#reducers). The Functional API keeps state scoped to the function: tasks pass values as return values, with no shared state schema.
* **Checkpointing**: The Graph API checkpoints after each [super-step](../../Build%20with%20the%20Graph%20API/Graph%20API%20overview.md#super-steps). The Functional API saves task results to the entrypoint checkpoint.
* **Visualization**: The Graph API supports graph diagrams. The Functional API does not, because the graph is built at runtime.

## Entrypoint

The `@entrypoint` decorator creates a workflow from a function. It manages long-running work and [interrupts](../../Capabilities/Interrupts.md).

### Definition

Pass a [checkpointer](../../Capabilities/Persistence.md) when you need persistence or human-in-the-loop. Identify each run with a `thread_id` in config. A thread is the durable identity for one conversation or workflow run.

An **entrypoint** is a function decorated with `@entrypoint`.

The function **must accept a single positional argument** as the workflow input. To pass multiple values, use a dictionary (or similar) as that argument.

Decorating the function produces a workflow object (a [`Pregel`](https://reference.langchain.com/python/langgraph/pregel/#langgraph.pregel.Pregel.stream) instance). Call `invoke` or `ainvoke` to run it.

> [tab] Sync
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langgraph.checkpoint.memory import InMemorySaver
> from langgraph.func import entrypoint
>
> checkpointer = InMemorySaver()
>
>
> @entrypoint(checkpointer=checkpointer)
> def my_workflow(name: str) -> str:
>     return f"Hello, {name}"
>
>
> config = {"configurable": {"thread_id": "1"}}
> my_workflow.invoke("Alice", config)  # "Hello, Alice"
> ```

> [tab] Async
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import asyncio
>
> from langgraph.checkpoint.memory import InMemorySaver
> from langgraph.func import entrypoint
>
> checkpointer = InMemorySaver()
>
>
> @entrypoint(checkpointer=checkpointer)
> async def my_workflow(name: str) -> str:
>     return f"Hello, {name}"
>
>
> config = {"configurable": {"thread_id": "1"}}
> asyncio.run(my_workflow.ainvoke("Alice", config))  # "Hello, Alice"
> ```

> [!WARNING]
>
> **Serialization**
> Entrypoint **inputs** and **outputs** must be JSON-serializable when a checkpointer is configured. See [Serialization](#serialization).

### Run and resume

Call `invoke` or `ainvoke` for a final result. For streams, see [Stream with the Functional API](Stream%20with%20the%20Functional%20API.md).

Resume after [`interrupt`](https://reference.langchain.com/python/langgraph/types/interrupt) by passing a resume value in [`Command`](https://reference.langchain.com/python/langgraph/types/Command). For recipes, see [Add human-in-the-loop with the Functional API](Add%20human-in-the-loop%20with%20the%20Functional%20API.md).

After an error, resume the same `thread_id` with `None`. See [Resume after an error](Configure%20Functional%20API%20tasks.md#resume-after-an-error).

### Short-term memory

When an `entrypoint` has a `checkpointer`, successive invocations on the same **thread id** store state in [checkpoints](../../Capabilities/Checkpointers.md#checkpoints).

Add a keyword-only `previous` parameter. LangGraph sets it to the last value saved on this thread. On the first run it is `None`. To save a different value for the next run, use [`entrypoint.final`](https://reference.langchain.com/python/langgraph/func/entrypoint/final). See [Return a different saved value](Add%20memory%20with%20the%20Functional%20API.md#return-a-different-saved-value).

For accumulate and inspecting checkpoints, see [Save state on a thread](Add%20memory%20with%20the%20Functional%20API.md#save-state-on-a-thread).

### Injectable parameters

You can skip this until you add [memory](Add%20memory%20with%20the%20Functional%20API.md) or [custom streaming](Stream%20with%20the%20Functional%20API.md).

When declaring an `entrypoint`, you can request additional parameters that LangGraph injects at runtime:

| Parameter | Description |
| - | - |
| **previous** | The return value from the previous invocation on the same thread (requires a checkpointer). See [short-term memory](Add%20memory%20with%20the%20Functional%20API.md#save-state-on-a-thread). |
| **config** | A [`RunnableConfig`](https://reference.langchain.com/python/langchain-core/runnables/config/RunnableConfig) object with run-time configuration values. |
| **store** | A [`BaseStore`](https://reference.langchain.com/python/langchain-core/stores/BaseStore) instance for [long-term memory](Add%20memory%20with%20the%20Functional%20API.md#save-facts-across-threads). Also available as `runtime.store`. |
| **writer** | A `StreamWriter` for custom streaming. Also available as `runtime.stream_writer`. See [Stream with the Functional API](Stream%20with%20the%20Functional%20API.md). |
| **runtime** | A [`Runtime`](https://reference.langchain.com/python/langgraph/runtime/Runtime) object for the current run, including context, store, and writer. |

> [!WARNING]
>
> Declare injectable parameters with the appropriate name and type annotation.

> [accordion] Requesting injectable parameters
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from typing import Any
>
> from langchain_core.runnables import RunnableConfig
> from langgraph.checkpoint.memory import InMemorySaver
> from langgraph.func import entrypoint
> from langgraph.runtime import Runtime
> from langgraph.store.memory import InMemoryStore
>
> checkpointer = InMemorySaver()
> store = InMemoryStore()
>
>
> @entrypoint(
>     checkpointer=checkpointer,
>     store=store,
> )
> def my_workflow(
>     some_input: dict,  # The input (for example, passed via `invoke`)
>     *,
>     previous: Any = None,  # Short-term memory from the previous invocation
>     config: RunnableConfig,  # Run-time configuration
>     runtime: Runtime,  # Context, store, and writer for the current run
> ) -> dict:
>     memory_store = runtime.store
>     writer = runtime.stream_writer
>     return {
>         "previous": previous,
>         "some_input": some_input,
>         "has_store": memory_store is not None,
>         "has_writer": writer is not None,
>         "thread_id": config["configurable"]["thread_id"],
>     }
> ```

## Task

A **task** is a discrete unit of work (for example, an API call or data step). Tasks have two key properties:

* **Concurrent execution**: Calling a task starts it immediately. The entrypoint blocks only when you wait for the result, so independent tasks can overlap.
* **Checkpointing**: Task results are saved so resume can restore them. See [persistence](../../Capabilities/Persistence.md).

### Definition

Define tasks with the `@task` decorator:

```python
from langgraph.func import task


@task
def slow_computation(input_value: int) -> int:
    # Long-running or side-effecting work
    return input_value * 2
```

> [!WARNING]
>
> **Serialization**: Task **outputs** must be JSON-serializable to support checkpointing.

### Execution

Call **tasks** only from an **entrypoint**, another **task**, or a [Graph API node](../../Build%20with%20the%20Graph%20API/Graph%20API%20overview.md#nodes). Do not call them from application code outside the workflow.

Calling a task returns a future immediately. Resolve it with `.result()` (sync) or `await` (async).

> [tab] Sync
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langgraph.checkpoint.memory import InMemorySaver
> from langgraph.func import entrypoint, task
>
> checkpointer = InMemorySaver()
>
>
> @task
> def slow_computation(input_value: int) -> int:
>     return input_value * 2
>
>
> @entrypoint(checkpointer=checkpointer)
> def my_workflow(some_input: int) -> int:
>     future = slow_computation(some_input)
>     return future.result()
> ```

> [tab] Async
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langgraph.checkpoint.memory import InMemorySaver
> from langgraph.func import entrypoint, task
>
> checkpointer = InMemorySaver()
>
>
> @task
> async def slow_computation(input_value: int) -> int:
>     return input_value * 2
>
>
> @entrypoint(checkpointer=checkpointer)
> async def my_workflow(some_input: int) -> int:
>     return await slow_computation(some_input)
> ```

### When to use a task

Use **tasks** when you need:

* **Checkpointing**: Save a long-running result so resume does not recompute it.
* **Human-in-the-loop**: Wrap work you should not redo after a pause in a task, for example an LLM call. Resume after an [interrupt](../../Capabilities/Interrupts.md) restores the result. For randomness, see [Determinism](#determinism).
* **Parallel execution**: Run independent I/O-bound work concurrently.
* **Observability**: Track discrete steps in [LangSmith](https://docs.langchain.com/langsmith/observability.md).
* **Retries**: Apply retry policies to discrete units of work. See [Configure Functional API tasks](Configure%20Functional%20API%20tasks.md).

## Resume and checkpointing

Resume replay depends on serialization, determinism, and idempotency.

### Serialization

Two rules apply when a checkpointer is configured:

1. `entrypoint` inputs and outputs must be JSON-serializable.
2. `task` outputs must be JSON-serializable.

Use Python primitives such as dictionaries, lists, strings, numbers, and booleans.

Serialization is what makes task results and intermediate values restorable for human-in-the-loop, fault tolerance, and parallel execution. Non-serializable values raise a runtime error when a checkpointer is configured.

### Determinism

Resume does **not** continue from the exact line where execution stopped. Execution returns to a checkpoint boundary and **replays** forward until it hits the pause again.

For the Functional API, replay starts at the beginning of the **entrypoint**. LangGraph restores completed [**task**](#task) and [**subgraph**](../../Capabilities/Subgraphs.md) results from the checkpointer instead of recomputing them. That preserves step order across pauses, including for long-running or non-deterministic **task** outputs.

For **human-in-the-loop**, put non-deterministic work (for example, random values) and side effects (for example, file writes or API calls) in [**tasks**](#task).

Different runs can produce different results. Resuming a **specific** thread should replay the same persisted **task** and **subgraph** results.

Guidelines:

* **Avoid repeating work**: Give each side effect in an entrypoint its own **task** so resume restores outputs instead of re-running them.
* **Encapsulate non-deterministic operations**: Keep values that change between attempts (random numbers, wall-clock time) inside **tasks**.
* **Use idempotent operations**: For partial failures and retries, see [Idempotency](#idempotency).

### Idempotency

Idempotency means running the same operation more than once has the same effect as running it once. Place API calls and other writes inside **tasks**, and design those tasks to be safe if they run again.

On resume, LangGraph restores completed **task** results. A **task** that started but did not finish may run again, so use idempotency keys or check existing results before writing.

## Pause for human review

This workflow writes an essay and [interrupts](../../Capabilities/Interrupts.md) for human review:

```python
import time

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.func import entrypoint, task
from langgraph.types import interrupt


@task
def write_essay(topic: str) -> str:
    """Write an essay about the given topic."""
    time.sleep(1)  # Placeholder for a long-running task.
    return f"An essay about topic: {topic}"


@entrypoint(checkpointer=InMemorySaver())
def workflow(topic: str) -> dict:
    """Write an essay and pause for review."""
    essay = write_essay(topic).result()
    is_approved = interrupt({
        # Any JSON-serializable payload. Surfaces as an Interrupt when streaming.
        "essay": essay,
        "action": "Please approve/reject the essay",
    })

    return {
        "essay": essay,
        "is_approved": is_approved,
    }
```

Invoke with a topic such as `"cat"`. The run writes the essay, then pauses at `interrupt`. The pause can last indefinitely. Resume starts at the beginning of the entrypoint.

The `write_essay` task result is restored, not recomputed.

For stream, resume, and tool-call review, see [Add human-in-the-loop with the Functional API](Add%20human-in-the-loop%20with%20the%20Functional%20API.md).

## Common pitfalls

### Handling side effects

Put side effects (writing a file, sending an email) in tasks so resume does not run them again.

> [tab] Incorrect
>
> The file write runs in the entrypoint, so resume executes it a second time.
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langgraph.checkpoint.memory import InMemorySaver
> from langgraph.func import entrypoint
> from langgraph.types import interrupt
>
> checkpointer = InMemorySaver()
>
> @entrypoint(checkpointer=checkpointer)
> def my_workflow(inputs: dict) -> int:
>     # Runs again on resume.
>     with open("output.txt", "w") as f:  # [!code highlight]
>         f.write("Side effect executed")  # [!code highlight]
>     value = interrupt("question")
>     return value
> ```

> [tab] Correct
>
> The side effect lives in a task, so resume restores the checkpointed result.
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langgraph.checkpoint.memory import InMemorySaver
> from langgraph.func import entrypoint, task
> from langgraph.types import interrupt
>
> checkpointer = InMemorySaver()
>
> @task  # [!code highlight]
> def write_to_file() -> None:  # [!code highlight]
>     with open("output.txt", "w") as f:
>         f.write("Side effect executed")
>
> @entrypoint(checkpointer=checkpointer)
> def my_workflow(inputs: dict) -> int:
>     write_to_file().result()
>     value = interrupt("question")
>     return value
> ```

### Non-deterministic control flow

Encapsulate time and randomness in tasks so resume returns the same values.

* In a task: Get random number (5) → interrupt → resume → (returns 5 again) → ...
* Not in a task: Get random number (5) → interrupt → resume → get new random number (7) → ...

With multiple [`interrupt`](https://reference.langchain.com/python/langgraph/types/interrupt) calls, LangGraph matches resume values **by index** to each interrupt. If resume changes the order of interrupts, a resume value can attach to the wrong interrupt. See [Determinism](#determinism).

> [tab] Incorrect
>
> Reading the clock in the entrypoint can change which branch runs on resume.
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import time
>
> from langgraph.checkpoint.memory import InMemorySaver
> from langgraph.func import entrypoint, task
> from langgraph.types import interrupt
>
> checkpointer = InMemorySaver()
>
> @task
> def slow_task(x: int) -> int:
>     return x
>
> @entrypoint(checkpointer=checkpointer)
> def my_workflow(inputs: dict) -> dict:
>     t0 = inputs["t0"]
>     t1 = time.time()  # [!code highlight]
>
>     delta_t = t1 - t0
>
>     if delta_t > 1:
>         result = slow_task(1).result()
>         value = interrupt("question")
>     else:
>         result = slow_task(2).result()
>         value = interrupt("question")
>
>     return {"result": result, "value": value}
> ```

> [tab] Correct
>
> Read the clock inside a task so resume restores the same timestamp and branch.
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import time
>
> from langgraph.checkpoint.memory import InMemorySaver
> from langgraph.func import entrypoint, task
> from langgraph.types import interrupt
>
> checkpointer = InMemorySaver()
>
> @task
> def slow_task(x: int) -> int:
>     return x
>
> @task  # [!code highlight]
> def get_time() -> float:  # [!code highlight]
>     return time.time()
>
> @entrypoint(checkpointer=checkpointer)
> def my_workflow(inputs: dict) -> dict:
>     t0 = inputs["t0"]
>     t1 = get_time().result()  # [!code highlight]
>
>     delta_t = t1 - t0
>
>     if delta_t > 1:
>         result = slow_task(1).result()
>         value = interrupt("question")
>     else:
>         result = slow_task(2).result()
>         value = interrupt("question")
>
>     return {"result": result, "value": value}
> ```

## Learn more

* [Thinking in the Functional API](Thinking%20in%20the%20Functional%20API.md)
* [Build checklist for the Functional API](Build%20checklist%20for%20the%20Functional%20API.md)
* [Compose Functional API workflows](Compose%20Functional%20API%20workflows.md)
* [Configure Functional API tasks](Configure%20Functional%20API%20tasks.md)
* [Stream with the Functional API](Stream%20with%20the%20Functional%20API.md)
* [Add human-in-the-loop with the Functional API](Add%20human-in-the-loop%20with%20the%20Functional%20API.md)
* [Add memory with the Functional API](Add%20memory%20with%20the%20Functional%20API.md)
* [Graph API overview](../../Build%20with%20the%20Graph%20API/Graph%20API%20overview.md)
* [Choosing between Graph and Functional APIs](../../Get%20started/Choosing%20between%20Graph%20and%20Functional%20APIs.md)

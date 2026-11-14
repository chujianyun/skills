# Query threads using the SDK

> Programmatically fetch and inspect multi-turn conversation threads from your LangSmith projects.

If you're building a conversational agent or any multi-turn application, LangSmith automatically groups your [runs](../Data%20type%20reference/Run%20%28span%29%20data%20format.md) into [*threads*](../../Trace/Observability%20concepts.md#threads). Querying threads lets you replay full conversations, audit agent behavior across sessions, build analytics on conversation length and latency, and feed downstream workflows like [fine-tuning](../../../Test/Datasets%20%26%20Experiments/Fine-tuning/Fine-tune%20models%20with%20Smithtune.md) and evaluation.

The SDK exposes two methods for working with threads:

| Method | Use when |
| - | - |
| `client.threads.query()` ([Python](https://reference.langchain.com/python/langsmith/resources/threads/threads/AsyncThreadsResource/query), [TypeScript](https://reference.langchain.com/javascript/langsmith/client/Langsmith/Threads/query)) | You want to browse the threads in a project |
| `client.threads.list_traces()` / `client.threads.listTraces()` ([Python](https://reference.langchain.com/python/langsmith/resources/threads/threads/AsyncThreadsResource/list_traces), [TypeScript](https://reference.langchain.com/javascript/langsmith/client/Langsmith/Threads/listTraces)) | You already know the thread ID and need its traces |

Both methods take a project ID. If you only have the project name, look it up with `aread_project()` / `readProject()` first, as the examples below do. In Python, both methods are async.

> [!NOTE]
>
> To query the threads of an agent, an experiment, or the evaluators, [find its project ID](Resolve%20an%20agent%20environment.md) and pass it as the project ID.

> [!NOTE]
>
> These methods replace `list_threads` / `listThreads` and `read_thread` / `readThread`, which are deprecated. LangSmith Cloud removes them on January 31, 2027, and self-hosted LangSmith removes them in v0.19. The new methods require `langsmith>=0.10.15` (Python) or `langsmith>=0.8.9` (TypeScript) and, on self-hosted LangSmith, v0.16 or later. For the full list of changes, see the [migration guide](../../Reference/SmithDB%20API%20migration/Migrate%20thread%20methods%20to%20SmithDB.md).

## How threads work

Each run you create can carry a `thread_id` in its metadata. LangSmith uses this to group runs into threads. The backend looks for `thread_id` in `metadata` (falling back to `session_id`).

> [!NOTE]
>
> We recommend using **UUID v7** thread IDs. UUIDv7 embeds a timestamp, which preserves correct time-ordering of threads. The LangSmith SDK exports a uuid7 helper (Python v0.4.43+, JS v0.3.80+):
>
> * **Python**: `from langsmith import uuid7`
> * **JS/TS**: `import { uuid7 } from 'langsmith'`

If you're using a [tracing integration](../../Trace/Tracing%20setup/Integrations/Integrations.md), pass `thread_id` in the run metadata:

```python Python
from langsmith import traceable, uuid7

THREAD_ID = str(uuid7())

@traceable(metadata={"thread_id": THREAD_ID})
def my_agent(user_message: str) -> str:
    ...
```

```typescript TypeScript
import { traceable } from "langsmith/traceable";
import { uuid7 } from "langsmith";

const THREAD_ID = uuid7();

const myAgent = traceable(
  async (userMessage: string) => {
    // ...
  },
  { metadata: { thread_id: THREAD_ID } }
);
```

## List threads in a project

`threads.query` returns the threads in a project, one row per thread with its aggregates. Results are paginated with a cursor; the SDK iterates through every page for you.

```python Python
import asyncio

from langsmith import Client


async def main():
    client = Client()
    project = await client.aread_project(project_name="my-project")

    async for thread in client.threads.query(project_id=str(project.id)):
        print(thread.thread_id)
        print(f"  {thread.count} traces")
        print(f"  last active: {thread.max_start_time}")


asyncio.run(main())
```

```typescript TypeScript
import { Client } from "langsmith";

const client = new Client();
const project = await client.readProject({ projectName: "my-project" });

for await (const thread of client.threads.query({ project_id: project.id })) {
  console.log(thread.thread_id);
  console.log(`  ${thread.count} traces`);
  console.log(`  last active: ${thread.max_start_time}`);
}
```

```text Output
conv-abc123
  3 traces
  last active: 2026-02-25T10:05:42+00:00
conv-def456
  1 traces
  last active: 2026-02-25T09:30:00+00:00
```

### Parameters

| Parameter | Type | Default | Description |
| - | - | - | - |
| `project_id` | `string` | — | **Required.** Project ID. |
| `min_start_time` | `datetime` / ISO `string` | 1 day ago | Only include threads with traces started after this time. Widen this window to surface older threads. |
| `max_start_time` | `datetime` / ISO `string` | now | Only include threads with traces started before this time. |
| `filter` | `string` | — | Filter expression evaluated against each thread's root runs, using [LangSmith trace query syntax](Trace%20query%20syntax.md). |
| `page_size` | `int` | — | Number of threads per page. |
| `cursor` | `string` | — | Cursor for the next page, when you paginate by hand. |

### Return value

An async iterator of `Thread` objects. The most useful fields:

| Field | Type | Description |
| - | - | - |
| `thread_id` | `string` | The thread identifier. |
| `count` | `int` | Number of traces in this thread. |
| `min_start_time` | `datetime` (Python) / `string` (TypeScript) | Timestamp of the earliest trace. |
| `max_start_time` | `datetime` (Python) / `string` (TypeScript) | Timestamp of the most recent trace. |
| `first_trace_id`, `last_trace_id` | `string` | First and last trace of the thread in the query window. |
| `first_inputs`, `last_outputs` | `string` | Truncated previews of the first input and last output. |
| `last_error`, `num_errored_turns` | `string`, `int` | Last error message and number of traces that errored. |
| `total_tokens`, `total_cost` | `int`, `number` | Token and cost totals across the thread. |
| `latency_p50`, `latency_p99` | `number` | Latency percentiles across the thread's traces. |
| `feedback_stats` | `object` | Aggregated feedback on the thread. |

A `Thread` does not embed its runs. To get them, call `threads.list_traces` with the `thread_id`.

## Read the traces of a single thread

When you already know the `thread_id`, use `threads.list_traces` / `threads.listTraces`. It returns the thread's traces (root runs) in ascending `start_time` order.

```python Python
import asyncio

from langsmith import Client


async def main():
    client = Client()
    project = await client.aread_project(project_name="my-project")

    async for trace in client.threads.list_traces(
        "conv-abc123",
        project_id=str(project.id),
        selects=["TRACE_ID", "NAME", "START_TIME"],
    ):
        print(trace.trace_id, trace.name, trace.start_time)


asyncio.run(main())
```

```typescript TypeScript
import { Client } from "langsmith";

const client = new Client();
const project = await client.readProject({ projectName: "my-project" });

for await (const trace of client.threads.listTraces("conv-abc123", {
  project_id: project.id,
  selects: ["TRACE_ID", "NAME", "START_TIME"],
})) {
  console.log(trace.trace_id, trace.name, trace.start_time);
}
```

Each item is a lightweight `ThreadTrace`, not a full run. Only the fields listed in `selects` are populated; without `selects`, you get `trace_id` only. Use [`traces.list_runs`](../../Reference/SmithDB%20API%20migration/Migrate%20trace%20methods%20to%20SmithDB.md) to get a trace's child runs (tool calls, sub-chains).

### Parameters

| Parameter | Type | Default | Description |
| - | - | - | - |
| `thread_id` | `string` | — | **Required.** The thread to read (first positional argument). |
| `project_id` | `string` | — | **Required.** Project ID. |
| `selects` | `string[]` | `["TRACE_ID"]` | Fields to return. List `TRACE_ID` too if you need it alongside other fields. For example `NAME`, `START_TIME`, `END_TIME`, `LATENCY`, `INPUTS`, `OUTPUTS`, `INPUTS_PREVIEW`, `OUTPUTS_PREVIEW`, `ERROR`, `TOTAL_TOKENS`, `TOTAL_COST`. |
| `filter` | `string` | — | Filter expression evaluated against each trace's root run. |
| `page_size` | `int` | — | Number of traces per page. |
| `cursor` | `string` | — | Cursor for the next page, when you paginate by hand. |

### Return value

An async iterator of `ThreadTrace` objects, sorted by `start_time` ascending.

## Examples

The snippets below continue the samples above: in Python, run them inside the same `async def main()`, with `client` and `project` already set.

### Filter threads by run properties

Pass a filter expression to narrow results using [LangSmith trace query syntax](Trace%20query%20syntax.md). For example, to surface only threads containing at least one failed run:

```python Python
async for thread in client.threads.query(
    project_id=str(project.id),
    filter='eq(status, "error")',
):
    print(thread.thread_id, thread.last_error)
```

```typescript TypeScript
for await (const thread of client.threads.query({
  project_id: project.id,
  filter: 'eq(status, "error")',
})) {
  console.log(thread.thread_id, thread.last_error);
}
```

### Look back further than 24 hours

By default, `threads.query` only surfaces threads with traces from the last day. Pass `min_start_time` to widen the window:

```python Python
from datetime import datetime, timedelta, timezone

async for thread in client.threads.query(
    project_id=str(project.id),
    min_start_time=datetime.now(timezone.utc) - timedelta(days=2),
):
    print(thread.thread_id)
```

```typescript TypeScript
for await (const thread of client.threads.query({
  project_id: project.id,
  min_start_time: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
})) {
  console.log(thread.thread_id);
}
```

### Reconstruct a conversation

`threads.list_traces` returns traces oldest first, so you can replay a conversation turn by turn. Select `INPUTS` and `OUTPUTS` to get the full payloads:

```python Python
async for trace in client.threads.list_traces(
    "conv-abc123",
    project_id=str(project.id),
    selects=["INPUTS", "OUTPUTS"],
):
    user_msg = (trace.inputs or {}).get("messages", [{}])[-1].get("content", "")
    assistant_msg = (trace.outputs or {}).get("content", "")
    print(f"User:      {user_msg}")
    print(f"Assistant: {assistant_msg}")
    print()
```

```typescript TypeScript
for await (const trace of client.threads.listTraces("conv-abc123", {
  project_id: project.id,
  selects: ["INPUTS", "OUTPUTS"],
})) {
  const inputs = trace.inputs as { messages?: Array<Record<string, string>> } | undefined;
  const outputs = trace.outputs as Record<string, string> | undefined;
  const messages = inputs?.messages ?? [];
  const userMsg = messages.at(-1)?.content ?? "";
  const assistantMsg = outputs?.content ?? "";
  console.log(`User:      ${userMsg}`);
  console.log(`Assistant: ${assistantMsg}`);
}
```

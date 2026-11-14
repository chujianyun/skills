# Query traces using the SDK

The recommended way to query [runs](../../Trace/Observability%20concepts.md#runs) (the span data in LangSmith traces) is to use the `runs.query` method in the [SDK](https://reference.langchain.com/python/langsmith/) or the `POST /api/v2/runs/query` endpoint in the [API](../../Reference/LangSmith%20REST%20API/LangSmith%20API%20reference.md). LangSmith stores traces in a simple format that is specified in the [Run (span) data format](../Data%20type%20reference/Run%20%28span%29%20data%20format.md).

This page covers:

* [Use filter arguments](#use-filter-arguments): keyword-based filtering using SDK parameters.
* [Use filter query language](#use-filter-query-language): complex queries using LangSmith's filter syntax.
* [Query trace trees with child-run predicates](#query-trace-trees-with-child-run-predicates): combine server-side narrowing with the runs of each trace.
* [Rate limits](#rate-limits): limits and best practices.

> [!NOTE]
>
> If you are looking to export a large volume of traces, we recommend that you use the [Bulk Data Export](../Bulk%20export%20trace%20data/Bulk%20export%20trace%20data.md) functionality, as it will better handle large data volumes and will support automatic retries and parallelization across partitions.

> [!NOTE]
>
> `runs.query` replaces `list_runs` / `listRuns` and `read_run` / `readRun`, which are deprecated. LangSmith Cloud removes them on January 31, 2027, and self-hosted LangSmith removes them in v0.19. The new methods require `langsmith>=0.10.15` (Python) or `langsmith>=0.8.9` (TypeScript) and, on self-hosted LangSmith, v0.16 or later. For the full list of changes, see the [migration guide](../../Reference/SmithDB%20API%20migration/Migrate%20run%20queries%20to%20SmithDB.md).

> [!NOTE]
>
> To query the traces of an agent, an experiment, or the evaluators, [find its project ID](Resolve%20an%20agent%20environment.md) and pass it as the project ID.

## Use filter arguments

For simple queries, you don't have to rely on our query syntax. You can use the filter arguments specified in the [filter arguments reference](Trace%20query%20syntax.md#filter-arguments).

> [!WARNING]
>
> **Prerequisites**
>
> Initialize the client, look up the project ID, and set a time window before running the below code snippets:
>
> * `runs.query` takes project IDs, not a project name.
> * It only looks back **1 day** unless you pass `min_start_time`. The snippets below use a 7-day window. One query can span at most 401 days.
> * It returns only the run `ID` unless you pass `selects` (uppercase field names such as `NAME`, `INPUTS`, `OUTPUTS`).
> * In Python, `client.runs` is async: run the snippets inside an `async` function, for example with `asyncio.run()`. Each query returns an async iterator that pages through the results for you.

```python Python
from datetime import datetime, timedelta, timezone

from langsmith import Client

client = Client()
project_id = str(client.read_project(project_name="<your_project>").id)
since = datetime.now(timezone.utc) - timedelta(days=7)
```

```typescript TypeScript
import { Client } from "langsmith";

const client = new Client();
const projectId = (await client.readProject({ projectName: "<your_project>" })).id;
const since = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString();
```

```java Java
import com.langchain.smith.client.LangsmithClient;
import com.langchain.smith.client.okhttp.LangsmithOkHttpClient;
import com.langchain.smith.models.runs.RunQueryV2Params;
import java.time.OffsetDateTime;

LangsmithClient client = LangsmithOkHttpClient.fromEnv();
String projectId = "<your_project_id>";
OffsetDateTime since = OffsetDateTime.now().minusDays(7);

// Run any of the queries below with: client.runs().queryV2(params)
```

Below are some examples of ways to list runs using keyword arguments:

### List all runs in a project

```python Python
project_runs = [
    run
    async for run in client.runs.query(
        project_ids=[project_id],
        min_start_time=since,
        selects=["ID", "NAME", "RUN_TYPE", "START_TIME"],
    )
]
```

```typescript TypeScript
const projectRuns = [];
for await (const run of client.runs.query({
  project_ids: [projectId],
  min_start_time: since,
  selects: ["ID", "NAME", "RUN_TYPE", "START_TIME"],
})) {
  projectRuns.push(run);
}
```

```java Java
import com.langchain.smith.models.runs.RunSelectField;

RunQueryV2Params projectRuns = RunQueryV2Params.builder()
    .addProjectId(projectId)
    .minStartTime(since)
    .addSelect(RunSelectField.ID)
    .addSelect(RunSelectField.NAME)
    .build();
```

### List LLM and chat runs in the last 24 hours

```python Python
todays_llm_runs = [
    run
    async for run in client.runs.query(
        project_ids=[project_id],
        min_start_time=datetime.now(timezone.utc) - timedelta(days=1),
        run_type="LLM",
    )
]
```

```typescript TypeScript
const todaysLlmRuns = [];
for await (const run of client.runs.query({
  project_ids: [projectId],
  min_start_time: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(),
  run_type: "LLM",
})) {
  todaysLlmRuns.push(run);
}
```

```java Java
import com.langchain.smith.models.runs.RunType;

RunQueryV2Params todaysLlmRuns = RunQueryV2Params.builder()
    .addProjectId(projectId)
    .minStartTime(OffsetDateTime.now().minusDays(1))
    .runType(RunType.LLM)
    .build();
```

### List root runs in a project

Root runs are runs that have no parents. These are assigned a value of `True` for `is_root`. You can use this to filter for root runs.

```python Python
root_runs = client.runs.query(
    project_ids=[project_id],
    min_start_time=since,
    is_root=True,
)
```

```typescript TypeScript
const rootRuns = client.runs.query({
  project_ids: [projectId],
  min_start_time: since,
  is_root: true,
});
```

```java Java
RunQueryV2Params rootRuns = RunQueryV2Params.builder()
    .addProjectId(projectId)
    .minStartTime(since)
    .isRoot(true)
    .build();
```

### List runs without errors

```python Python
correct_runs = client.runs.query(
    project_ids=[project_id],
    min_start_time=since,
    has_error=False,
)
```

```typescript TypeScript
const correctRuns = client.runs.query({
  project_ids: [projectId],
  min_start_time: since,
  has_error: false,
});
```

```java Java
RunQueryV2Params noErrorRuns = RunQueryV2Params.builder()
    .addProjectId(projectId)
    .minStartTime(since)
    .hasError(false)
    .build();
```

### List runs by run ID

If you have a list of run IDs, you can list them directly. Pass the project ID too; you can combine `ids` with the other filters.

```python Python
run_ids = ["a36092d2-4ad5-4fb4-9c0d-0dba9a2ed836", "9398e6be-964f-4aa4-8ae9-ad78cd4b7074"]
selected_runs = client.runs.query(
    project_ids=[project_id],
    min_start_time=since,
    ids=run_ids,
)
```

```typescript TypeScript
const runIds = [
  "a36092d2-4ad5-4fb4-9c0d-0dba9a2ed836",
  "9398e6be-964f-4aa4-8ae9-ad78cd4b7074",
];
const selectedRuns = client.runs.query({
  project_ids: [projectId],
  min_start_time: since,
  ids: runIds,
});
```

```java Java
RunQueryV2Params runIdsRuns = RunQueryV2Params.builder()
    .addProjectId(projectId)
    .minStartTime(since)
    .ids(runIds)
    .build();
```

### Fetch a single run by ID

To fetch a single run by its ID, use the `runs.retrieve` method. It needs the ID of the project the run belongs to. For a run from a public share link, use the [public runs methods](../../Reference/SmithDB%20API%20migration/Migrate%20feedback%20and%20sharing%20methods%20to%20SmithDB.md) instead.

```python Python
run_id = "a36092d2-4ad5-4fb4-9c0d-0dba9a2ed836"
run = await client.runs.retrieve(
    run_id,
    project_id=project_id,
    selects=["NAME", "INPUTS", "OUTPUTS"],
)

# Access run data
print(run.inputs)
print(run.outputs)
print(run.name)
```

```typescript TypeScript
const runId = "a36092d2-4ad5-4fb4-9c0d-0dba9a2ed836";
const run = await client.runs.retrieve(runId, {
  project_id: projectId,
  selects: ["NAME", "INPUTS", "OUTPUTS"],
});

// Access run data
console.log(run.inputs);
console.log(run.outputs);
console.log(run.name);
```

```java Java
import com.langchain.smith.models.runs.Run;
import com.langchain.smith.models.runs.RunRetrieveV2Params;

Run run = client.runs().retrieveV2(
    runId,
    RunRetrieveV2Params.builder().projectId(projectId).build()
);
```

> [!TIP]
>
> **Replay traces locally with LangGraph**
>
> If you're using LangGraph with checkpointing, you can fetch a trace from LangSmith and replay it locally for debugging. See [LangGraph's time travel and replay documentation](https://docs.langchain.com/oss/python/langgraph/use-time-travel.md) for details on resuming execution from checkpoints.

## Use filter query language

For more complex queries, you can use the filter query language. The following examples cover the most common patterns. For the full operator and field reference, including all comparators, filterable fields, value formatting rules, and a quick-reference example table, refer to [Trace query syntax: filter query language](Trace%20query%20syntax.md#filter-query-language).

### List all root runs in a conversational thread

This is the way to fetch runs in a conversational thread. For more information on setting up threads, refer to our [how-to guide on setting up threads](../Configure%20threads.md). To list threads and their traces directly, see [Query threads](Query%20threads%20using%20the%20SDK.md).
Threads are grouped by setting a shared thread ID. The LangSmith UI lets you use either of the following metadata keys: `session_id` or `thread_id`. The session ID is also known as the tracing project ID. The following query matches on either of them.

```python Python
group_key = "<your_thread_id>"
filter_string = f'and(in(metadata_key, ["session_id","thread_id"]), eq(metadata_value, "{group_key}"))'
thread_runs = client.runs.query(
    project_ids=[project_id],
    min_start_time=since,
    filter=filter_string,
    is_root=True,
)
```

```typescript TypeScript
const groupKey = "<your_thread_id>";
const filterString = `and(in(metadata_key, ["session_id","thread_id"]), eq(metadata_value, "${groupKey}"))`;
const threadRuns = client.runs.query({
  project_ids: [projectId],
  min_start_time: since,
  filter: filterString,
  is_root: true,
});
```

```java Java
String groupKey = "<your_thread_id>";

String filterString = String.format(
    "and(in(metadata_key, [\"session_id\",\"thread_id\"]), eq(metadata_value, \"%s\"))",
    groupKey
);

RunQueryV2Params threadRuns = RunQueryV2Params.builder()
    .addProjectId(projectId)
    .minStartTime(since)
    .filter(filterString)
    .isRoot(true)
    .build();
```

### List all runs called "extractor" whose root of the trace was assigned feedback "user\_score" score of 1

```python Python
client.runs.query(
    project_ids=[project_id],
    min_start_time=since,
    filter='eq(name, "extractor")',
    trace_filter='and(eq(feedback_key, "user_score"), eq(feedback_score, 1))',
)
```

```typescript TypeScript
client.runs.query({
  project_ids: [projectId],
  min_start_time: since,
  filter: 'eq(name, "extractor")',
  trace_filter: 'and(eq(feedback_key, "user_score"), eq(feedback_score, 1))',
});
```

```java Java
RunQueryV2Params extractorRuns = RunQueryV2Params.builder()
    .addProjectId(projectId)
    .minStartTime(since)
    .filter("eq(name, \"extractor\")")
    .traceFilter("and(eq(feedback_key, \"user_score\"), eq(feedback_score, 1))")
    .build();
```

### List runs with "star\_rating" key whose score is greater than 4

```python Python
client.runs.query(
    project_ids=[project_id],
    min_start_time=since,
    filter='and(eq(feedback_key, "star_rating"), gt(feedback_score, 4))',
)
```

```typescript TypeScript
client.runs.query({
  project_ids: [projectId],
  min_start_time: since,
  filter: 'and(eq(feedback_key, "star_rating"), gt(feedback_score, 4))',
});
```

```java Java
RunQueryV2Params runs = RunQueryV2Params.builder()
    .addProjectId(projectId)
    .minStartTime(since)
    .filter("and(eq(feedback_key, \"star_rating\"), gt(feedback_score, 4))")
    .build();
```

### List runs that took longer than 5 seconds to complete

Pass the latency as a number of seconds.

```python Python
client.runs.query(project_ids=[project_id], min_start_time=since, filter="gt(latency, 5)")
```

```typescript TypeScript
client.runs.query({ project_ids: [projectId], min_start_time: since, filter: "gt(latency, 5)" });
```

```java Java
RunQueryV2Params runs = RunQueryV2Params.builder()
    .addProjectId(projectId)
    .minStartTime(since)
    .filter("gt(latency, 5)")
    .build();
```

### List all runs where status is not "error"

```python Python
client.runs.query(project_ids=[project_id], min_start_time=since, filter='neq(status, "error")')
```

```typescript TypeScript
client.runs.query({ project_ids: [projectId], min_start_time: since, filter: 'neq(status, "error")' });
```

```java Java
RunQueryV2Params runs = RunQueryV2Params.builder()
    .addProjectId(projectId)
    .minStartTime(since)
    .filter("neq(status, \"error\")")
    .build();
```

### List all runs where start\_time is greater than a specific timestamp

To bound the time window itself, prefer the `min_start_time` and `max_start_time` arguments; a `start_time` filter only narrows results inside that window.

```python Python
client.runs.query(
    project_ids=[project_id],
    min_start_time=since,
    filter='gt(start_time, "2023-07-15T12:34:56Z")',
)
```

```typescript TypeScript
client.runs.query({
  project_ids: [projectId],
  min_start_time: since,
  filter: 'gt(start_time, "2023-07-15T12:34:56Z")',
});
```

```java Java
RunQueryV2Params runs = RunQueryV2Params.builder()
    .addProjectId(projectId)
    .minStartTime(since)
    .filter("gt(start_time, \"2023-07-15T12:34:56Z\")")
    .build();
```

### List all runs that contain the string "substring"

```python Python
client.runs.query(project_ids=[project_id], min_start_time=since, filter='search("substring")')
```

```typescript TypeScript
client.runs.query({ project_ids: [projectId], min_start_time: since, filter: 'search("substring")' });
```

```java Java
RunQueryV2Params runs = RunQueryV2Params.builder()
    .addProjectId(projectId)
    .minStartTime(since)
    .filter("search(\"substring\")")
    .build();
```

### List all runs that are tagged with the git hash "2aa1cf4"

```python Python
client.runs.query(project_ids=[project_id], min_start_time=since, filter='has(tags, "2aa1cf4")')
```

```typescript TypeScript
client.runs.query({ project_ids: [projectId], min_start_time: since, filter: 'has(tags, "2aa1cf4")' });
```

```java Java
RunQueryV2Params runs = RunQueryV2Params.builder()
    .addProjectId(projectId)
    .minStartTime(since)
    .filter("has(tags, \"2aa1cf4\")")
    .build();
```

### List all runs that started after a specific timestamp and either have a non-error status or a "Correctness" feedback score equal to 0

Pass the timestamp as `min_start_time` and keep the `or` condition in `filter`.

```python Python
client.runs.query(
    project_ids=[project_id],
    min_start_time=datetime(2026, 7, 15, 12, 34, 56, tzinfo=timezone.utc),
    filter='or(neq(status, "error"), and(eq(feedback_key, "Correctness"), eq(feedback_score, 0.0)))',
)
```

```typescript TypeScript
client.runs.query({
  project_ids: [projectId],
  min_start_time: "2026-07-15T12:34:56Z",
  filter: 'or(neq(status, "error"), and(eq(feedback_key, "Correctness"), eq(feedback_score, 0.0)))',
});
```

```java Java
RunQueryV2Params runs = RunQueryV2Params.builder()
    .addProjectId(projectId)
    .minStartTime(OffsetDateTime.parse("2026-07-15T12:34:56Z"))
    .filter("or(neq(status, \"error\"), and(eq(feedback_key, \"Correctness\"), eq(feedback_score, 0.0)))")
    .build();
```

### Complex query: List all runs where tags include "experimental" or "beta" and latency is greater than 2 seconds

```python Python
client.runs.query(
    project_ids=[project_id],
    min_start_time=since,
    filter='and(or(has(tags, "experimental"), has(tags, "beta")), gt(latency, 2))',
)
```

```typescript TypeScript
client.runs.query({
  project_ids: [projectId],
  min_start_time: since,
  filter: 'and(or(has(tags, "experimental"), has(tags, "beta")), gt(latency, 2))',
});
```

```java Java
RunQueryV2Params runs = RunQueryV2Params.builder()
    .addProjectId(projectId)
    .minStartTime(since)
    .filter("and(or(has(tags, 'experimental'), has(tags, 'beta')), gt(latency, 2))")
    .build();
```

### Search trace trees by full text

You can use the `search()` function without any specific field to do a full text search across all string fields in a run. This allows you to quickly find traces that match a search term.

```python Python
client.runs.query(
    project_ids=[project_id],
    min_start_time=since,
    filter='search("image classification")',
)
```

```typescript TypeScript
client.runs.query({
  project_ids: [projectId],
  min_start_time: since,
  filter: 'search("image classification")',
});
```

```java Java
RunQueryV2Params runs = RunQueryV2Params.builder()
    .addProjectId(projectId)
    .minStartTime(since)
    .filter("search(\"image classification\")")
    .build();
```

### Check for presence of metadata

If you want to check for the presence of metadata, you can use the `eq` operator, optionally with an `and` statement to match by value. This is useful if you want to log more structured information about your runs.

```python Python
# Check for any run with the "user_id" metadata key
client.runs.query(
    project_ids=[project_id],
    min_start_time=since,
    filter="eq(metadata_key, 'user_id')",
)
# Check for runs with user_id=4070f233-f61e-44eb-bff1-da3c163895a3
client.runs.query(
    project_ids=[project_id],
    min_start_time=since,
    filter="and(eq(metadata_key, 'user_id'), eq(metadata_value, '4070f233-f61e-44eb-bff1-da3c163895a3'))",
)
```

```typescript TypeScript
// Check for any run with the "user_id" metadata key
client.runs.query({
  project_ids: [projectId],
  min_start_time: since,
  filter: `eq(metadata_key, 'user_id')`,
});
// Check for runs with user_id=4070f233-f61e-44eb-bff1-da3c163895a3
client.runs.query({
  project_ids: [projectId],
  min_start_time: since,
  filter: `and(eq(metadata_key, 'user_id'), eq(metadata_value, '4070f233-f61e-44eb-bff1-da3c163895a3'))`,
});
```

```java Java
RunQueryV2Params runsWithUserId = RunQueryV2Params.builder()
    .addProjectId(projectId)
    .minStartTime(since)
    .filter("eq(metadata_key, 'user_id')")
    .build();

RunQueryV2Params runsForUser = RunQueryV2Params.builder()
    .addProjectId(projectId)
    .minStartTime(since)
    .filter("and(eq(metadata_key, 'user_id'), eq(metadata_value, '4070f233-f61e-44eb-bff1-da3c163895a3'))")
    .build();
```

### Check for environment details in metadata

A common pattern is to add environment information to your traces via metadata. If you want to filter for runs containing environment metadata, you can use the same pattern as above:

```python Python
client.runs.query(
    project_ids=[project_id],
    min_start_time=since,
    filter="and(eq(metadata_key, 'environment'), eq(metadata_value, 'production'))",
)
```

```typescript TypeScript
client.runs.query({
  project_ids: [projectId],
  min_start_time: since,
  filter: `and(eq(metadata_key, 'environment'), eq(metadata_value, 'production'))`,
});
```

```java Java
RunQueryV2Params runs = RunQueryV2Params.builder()
    .addProjectId(projectId)
    .minStartTime(since)
    .filter("and(eq(metadata_key, 'environment'), eq(metadata_value, 'production'))")
    .build();
```

### Check for thread ID in metadata

A common way to associate traces in the same conversation is by using a shared thread ID. If you want to filter runs based on a thread ID in this way, you can search for that ID in the metadata.

```python Python
client.runs.query(
    project_ids=[project_id],
    min_start_time=since,
    filter="and(eq(metadata_key, 'thread_id'), eq(metadata_value, 'a1b2c3d4-e5f6-7890'))",
)
```

```typescript TypeScript
client.runs.query({
  project_ids: [projectId],
  min_start_time: since,
  filter: `and(eq(metadata_key, 'thread_id'), eq(metadata_value, 'a1b2c3d4-e5f6-7890'))`,
});
```

```java Java
RunQueryV2Params runs = RunQueryV2Params.builder()
    .addProjectId(projectId)
    .minStartTime(since)
    .filter("and(eq(metadata_key, 'thread_id'), eq(metadata_value, 'a1b2c3d4-e5f6-7890'))")
    .build();
```

### Negative filtering on key-value pairs

You can use negative filtering on metadata, input, and output key-value pairs to exclude specific runs from your results. Here are some examples for metadata key-value pairs but the same logic applies to input and output key-value pairs.

```python Python
# Find all runs where the metadata does not contain a "thread_id" key
client.runs.query(
    project_ids=[project_id],
    min_start_time=since,
    filter="and(neq(metadata_key, 'thread_id'))",
)

# Find all runs where the thread_id in metadata is not "a1b2c3d4-e5f6-7890"
client.runs.query(
    project_ids=[project_id],
    min_start_time=since,
    filter="and(eq(metadata_key, 'thread_id'), neq(metadata_value, 'a1b2c3d4-e5f6-7890'))",
)

# Find all runs where there is no "thread_id" metadata key and the "a1b2c3d4-e5f6-7890" value is not present
client.runs.query(
    project_ids=[project_id],
    min_start_time=since,
    filter="and(neq(metadata_key, 'thread_id'), neq(metadata_value, 'a1b2c3d4-e5f6-7890'))",
)

# Find all runs where the thread_id metadata key is not present but the "a1b2c3d4-e5f6-7890" value is present
client.runs.query(
    project_ids=[project_id],
    min_start_time=since,
    filter="and(neq(metadata_key, 'thread_id'), eq(metadata_value, 'a1b2c3d4-e5f6-7890'))",
)
```

```typescript TypeScript
// Find all runs where the metadata does not contain a "thread_id" key
client.runs.query({
  project_ids: [projectId],
  min_start_time: since,
  filter: `and(neq(metadata_key, 'thread_id'))`,
});

// Find all runs where the thread_id in metadata is not "a1b2c3d4-e5f6-7890"
client.runs.query({
  project_ids: [projectId],
  min_start_time: since,
  filter: `and(eq(metadata_key, 'thread_id'), neq(metadata_value, 'a1b2c3d4-e5f6-7890'))`,
});

// Find all runs where there is no "thread_id" metadata key and the "a1b2c3d4-e5f6-7890" value is not present
client.runs.query({
  project_ids: [projectId],
  min_start_time: since,
  filter: `and(neq(metadata_key, 'thread_id'), neq(metadata_value, 'a1b2c3d4-e5f6-7890'))`,
});

// Find all runs where the thread_id metadata key is not present but the "a1b2c3d4-e5f6-7890" value is present
client.runs.query({
  project_ids: [projectId],
  min_start_time: since,
  filter: `and(neq(metadata_key, 'thread_id'), eq(metadata_value, 'a1b2c3d4-e5f6-7890'))`,
});
```

```java Java
// Find all runs where the metadata does not contain a "thread_id" key
RunQueryV2Params runsWithoutThreadId = RunQueryV2Params.builder()
    .addProjectId(projectId)
    .minStartTime(since)
    .filter("and(neq(metadata_key, 'thread_id'))")
    .build();

// Find all runs where the thread_id in metadata is not "a1b2c3d4-e5f6-7890"
RunQueryV2Params runsWithOtherThreadId = RunQueryV2Params.builder()
    .addProjectId(projectId)
    .minStartTime(since)
    .filter("and(eq(metadata_key, 'thread_id'), neq(metadata_value, 'a1b2c3d4-e5f6-7890'))")
    .build();

// Find all runs where there is no "thread_id" metadata key and the "a1b2c3d4-e5f6-7890" value is not present
RunQueryV2Params runsWithoutThreadIdOrValue = RunQueryV2Params.builder()
    .addProjectId(projectId)
    .minStartTime(since)
    .filter("and(neq(metadata_key, 'thread_id'), neq(metadata_value, 'a1b2c3d4-e5f6-7890'))")
    .build();

// Find all runs where the thread_id metadata key is not present but the "a1b2c3d4-e5f6-7890" value is present
RunQueryV2Params runsWithValueNotThreadId = RunQueryV2Params.builder()
    .addProjectId(projectId)
    .minStartTime(since)
    .filter("and(neq(metadata_key, 'thread_id'), eq(metadata_value, 'a1b2c3d4-e5f6-7890'))")
    .build();
```

### Combine multiple filters

If you want to combine multiple conditions to refine your search, you can use the `and` operator along with other filtering functions. Here's how you can search for runs named "ChatOpenAI" that also have a specific `thread_id` in their metadata:

```python Python
client.runs.query(
    project_ids=[project_id],
    min_start_time=since,
    filter="and(eq(name, 'ChatOpenAI'), eq(metadata_key, 'thread_id'), eq(metadata_value, '69b12c91-b1e2-46ce-91de-794c077e8151'))",
)
```

```typescript TypeScript
client.runs.query({
  project_ids: [projectId],
  min_start_time: since,
  filter: `and(eq(name, 'ChatOpenAI'), eq(metadata_key, 'thread_id'), eq(metadata_value, '69b12c91-b1e2-46ce-91de-794c077e8151'))`,
});
```

```java Java
RunQueryV2Params runs = RunQueryV2Params.builder()
    .addProjectId(projectId)
    .minStartTime(since)
    .filter("and(eq(name, 'ChatOpenAI'), eq(metadata_key, 'thread_id'), eq(metadata_value, '69b12c91-b1e2-46ce-91de-794c077e8151'))")
    .build();
```

### Tree filter

List all runs named "RetrieveDocs" whose root run has a "user\_score" feedback of 1 and any run in the full trace is named "ExpandQuery".

This type of query is useful if you want to extract a specific run conditional on various states or steps being reached within the trace.

```python Python
client.runs.query(
    project_ids=[project_id],
    min_start_time=since,
    filter='eq(name, "RetrieveDocs")',
    trace_filter='and(eq(feedback_key, "user_score"), eq(feedback_score, 1))',
    tree_filter='eq(name, "ExpandQuery")',
)
```

```typescript TypeScript
client.runs.query({
  project_ids: [projectId],
  min_start_time: since,
  filter: 'eq(name, "RetrieveDocs")',
  trace_filter: 'and(eq(feedback_key, "user_score"), eq(feedback_score, 1))',
  tree_filter: 'eq(name, "ExpandQuery")',
});
```

```java Java
RunQueryV2Params runs = RunQueryV2Params.builder()
    .addProjectId(projectId)
    .minStartTime(since)
    .filter("eq(name, \"RetrieveDocs\")")
    .traceFilter("and(eq(feedback_key, 'user_score'), eq(feedback_score, 1))")
    .treeFilter("eq(name, 'ExpandQuery')")
    .build();
```

## Query trace trees with child-run predicates

Use `trace_filter` to match fields on the root run and `tree_filter` to match supported searchable fields on any run in the trace tree. For predicates over arbitrary returned child-run fields, such as nested `inputs`, `outputs`, or `extra` payloads, use the steps below:

1. Narrow candidate root traces server-side with `filter`, `trace_filter`, `tree_filter`, `run_type`, metadata filters, and the `ls_run_depth` [system metadata key](../../Trace/Tracing%20setup/Manual%20instrumentation/Metadata%20parameters%20reference.md#ls_run_depth).
2. Fetch the runs of each candidate trace with `traces.list_runs` / `traces.listRuns`.
3. Apply your predicate locally to the fields that are not available as server-side filter fields.

The following example returns root traces that contain a tool run whose output contains a specific value. The server-side `tree_filter` narrows candidates to traces that contain the relevant tool run, and the local predicate checks the `outputs` payload.

```python Python
import asyncio
from datetime import datetime, timedelta, timezone

from langsmith import Client


async def main():
    client = Client()
    project_id = str(client.read_project(project_name="<your_project>").id)

    matching_trace_ids = []
    async for candidate in client.runs.query(
        project_ids=[project_id],
        min_start_time=datetime.now(timezone.utc) - timedelta(days=7),
        is_root=True,
        tree_filter='and(eq(run_type, "tool"), eq(name, "<tool_name>"))',
        selects=["TRACE_ID"],
    ):
        response = await client.traces.list_runs(
            str(candidate.trace_id),
            project_id=project_id,
            selects=["NAME", "RUN_TYPE", "OUTPUTS"],
        )
        if any(
            run.run_type == "tool"
            and run.name == "<tool_name>"
            and "<expected_value>" in str(run.outputs or {})
            for run in response.items
        ):
            matching_trace_ids.append(candidate.trace_id)


asyncio.run(main())
```

```typescript TypeScript
import { Client } from "langsmith";

const client = new Client();
const projectId = (await client.readProject({ projectName: "<your_project>" })).id;

const matchingTraceIds: string[] = [];
for await (const candidate of client.runs.query({
  project_ids: [projectId],
  min_start_time: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString(),
  is_root: true,
  tree_filter: 'and(eq(run_type, "tool"), eq(name, "<tool_name>"))',
  selects: ["TRACE_ID"],
})) {
  const response = await client.traces.listRuns(candidate.trace_id!, {
    project_id: projectId,
    selects: ["NAME", "RUN_TYPE", "OUTPUTS"],
  });
  const hasMatchingChild = (response.items ?? []).some(
    (run) =>
      run.run_type === "tool" &&
      run.name === "<tool_name>" &&
      JSON.stringify(run.outputs ?? {}).includes("<expected_value>"),
  );
  if (hasMatchingChild) {
    matchingTraceIds.push(candidate.trace_id!);
  }
}
```

### Advanced: export flattened trace view with child tool usage

The following Python example demonstrates how to export a flattened view of traces, including information on the tools (from nested runs) used by the agent within each trace.
This can be used to analyze the behavior of your agents across multiple traces.

This example queries all tool runs within a specified number of days and groups them by their trace ID. It then fetches the relevant information for each root run, such as the run name, inputs, outputs, and combines that information with the child run information.

To optimize the query, the example:

1. Selects only the necessary fields when querying tool runs to reduce query time.
2. Fetches root runs in batches of IDs. A root run's ID is its trace ID.

```python Python
import asyncio
from collections import defaultdict
from datetime import datetime, timedelta, timezone

from langsmith import Client


async def main():
    client = Client()
    project_id = str(client.read_project(project_name="my-project").id)
    num_days = 30
    since = datetime.now(timezone.utc) - timedelta(days=num_days)

    # Collect all tools invoked within each trace
    tools_by_trace = defaultdict(set)
    async for run in client.runs.query(
        project_ids=[project_id],
        min_start_time=since,
        run_type="TOOL",
        # We don't need inputs, outputs, and other values that may increase the query time
        selects=["TRACE_ID", "NAME"],
    ):
        tools_by_trace[str(run.trace_id)].add(run.name)

    # Fetch the root runs in batches
    data = []
    trace_ids = list(tools_by_trace)
    trace_batch_size = 50
    for i in range(0, len(trace_ids), trace_batch_size):
        async for root_run in client.runs.query(
            project_ids=[project_id],
            min_start_time=since,
            ids=trace_ids[i : i + trace_batch_size],
            selects=["ID", "NAME", "RUN_TYPE", "INPUTS", "OUTPUTS"],
        ):
            data.append(
                {
                    "run_id": root_run.id,
                    "run_name": root_run.name,
                    "run_type": root_run.run_type,
                    "inputs": root_run.inputs,
                    "outputs": root_run.outputs,
                    "tools_involved": list(tools_by_trace[str(root_run.id)]),
                }
            )
    return data


data = asyncio.run(main())

# (Optional): Convert to a pandas DataFrame
import pandas as pd

df = pd.DataFrame(data)
df.head()
```

### Advanced: export retriever IO for traces with feedback

This query is useful if you want to fine-tune embeddings or diagnose end-to-end system performance issues based on retriever behavior.
The following Python example demonstrates how to export retriever inputs and outputs within traces that have a specific feedback score.

```python Python
import asyncio
from collections import defaultdict
from datetime import datetime, timedelta, timezone

from langsmith import Client


async def main():
    client = Client()
    project_id = str(client.read_project(project_name="your-project-name").id)
    num_days = 1
    since = datetime.now(timezone.utc) - timedelta(days=num_days)

    # List all retriever runs in traces with "user_score" feedback
    retriever_data = defaultdict(lambda: defaultdict(list))
    async for run in client.runs.query(
        project_ids=[project_id],
        min_start_time=since,
        run_type="RETRIEVER",
        # This time we do want to fetch the inputs and outputs, since they
        # may be adjusted by query expansion steps.
        selects=["TRACE_ID", "INPUTS", "OUTPUTS"],
        trace_filter='eq(feedback_key, "user_score")',
    ):
        for k, v in (run.inputs or {}).items():
            retriever_data[str(run.trace_id)][f"retriever.inputs.{k}"].append(v)
        for k, v in (run.outputs or {}).items():
            retriever_data[str(run.trace_id)][f"retriever.outputs.{k}"].extend(v)

    # Fetch the root runs, with their feedback, in batches
    data = []
    trace_ids = list(retriever_data)
    trace_batch_size = 50
    for i in range(0, len(trace_ids), trace_batch_size):
        async for root_run in client.runs.query(
            project_ids=[project_id],
            min_start_time=since,
            ids=trace_ids[i : i + trace_batch_size],
            selects=["ID", "NAME", "INPUTS", "OUTPUTS", "FEEDBACK_STATS"],
        ):
            feedback = {
                f"feedback.{k}": v.avg
                for k, v in (root_run.feedback_stats or {}).items()
            }
            inputs = {f"inputs.{k}": v for k, v in (root_run.inputs or {}).items()}
            outputs = {f"outputs.{k}": v for k, v in (root_run.outputs or {}).items()}
            data.append(
                {
                    "run_id": root_run.id,
                    "run_name": root_run.name,
                    **inputs,
                    **outputs,
                    **feedback,
                    **retriever_data[str(root_run.id)],
                }
            )
    return data


data = asyncio.run(main())

# (Optional): Convert to a pandas DataFrame
import pandas as pd

df = pd.DataFrame(data)
df.head()
```

## Rate limits

`runs.query` (`POST /api/v2/runs/query`) has a dedicated, higher rate limit than the deprecated `POST /runs/query` endpoint: 300 requests per 10 seconds per API key in LangSmith Cloud. Requests that exceed it return `429 Too Many Requests`. It is not subject to the per-tenant limits of the deprecated endpoint. For general best practices, see [Run query endpoint rate limits](../../Trace/Configuration%20%26%20troubleshooting/Usage%20and%20billing.md#run-query-endpoint).

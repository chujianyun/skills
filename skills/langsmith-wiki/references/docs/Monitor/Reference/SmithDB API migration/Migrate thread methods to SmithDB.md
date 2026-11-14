# Migrate thread methods to SmithDB

> Migrate the LangSmith SDK thread methods to their SmithDB-backed equivalents.

These methods query threads and list the traces inside a thread. For deprecation dates, minimum SDK versions, and the agent prompt that applies to every method, see [Migrate to SmithDB-backed APIs](Migrate%20to%20SmithDB-backed%20APIs.md).

## Threads: query

Query threads within a project, with cursor-based pagination. Returns threads matching the given time range and optional filter.

### Main changes

#### Method name

> [tab] Python
>
> | Before | After |
> | - | - |
> | `client.list_threads()` | `client.threads.query()` |
>
> > [!NOTE]
> >
> > `client.threads.query()` is now async. Call it with `await`.
>
> See the [reference](https://reference.langchain.com/python/langsmith/_openapi_client/resources/threads/ThreadsResource/query) for the full parameter and field list.

> [tab] TypeScript
>
> | Before | After |
> | - | - |
> | `client.listThreads()` | `client.threads.query()` |
>
> See the [reference](https://reference.langchain.com/javascript/langsmith/_openapi_client/Langsmith/Threads/query) for the full parameter and field list.

> [tab] Java
>
> > [!NOTE]
> >
> > Java never had a dedicated thread-listing method. The closest legacy equivalent is the generic run query, manually grouped by the `thread_id` metadata convention.
>
> | Before | After |
> | - | - |
> | `client.runs().query()` (generic, grouped client-side) | `client.threads().query()` |
>
> See the [reference](https://javadoc.io/doc/com.langchain.smith/langsmith-java/latest/com/langchain/smith/services/blocking/ThreadService.html) for the full parameter list.

> [tab] Go
>
> > [!NOTE]
> >
> > Go never had a dedicated thread-listing method. The closest legacy equivalent is the generic run query, manually grouped by the `thread_id` metadata convention.
>
> | Before | After |
> | - | - |
> | `client.Runs.Query()` (generic, grouped client-side) | `client.Threads.Query()` |
>
> See the [reference](https://pkg.go.dev/github.com/langchain-ai/langsmith-go#ThreadService.QueryAutoPaging) for the full parameter list.

> [tab] cURL
>
> | Before | After |
> | - | - |
> | `POST /api/v1/runs/query` (`is_root=true`, grouped client-side) | `POST /api/v2/threads/query` |
>
> See the [API doc](../LangSmith%20REST%20API/Threads/Query%20threads.md) for the full parameter and field list.

#### Query parameters

> [tab] Python
>
> | Before (`list_threads`) | After (`threads.query`) | Notes |
> | - | - | - |
> | `project_id` XOR `project_name` | `project_id` | the new method takes only the UUID; resolve a name via `aread_project()` first, same pattern as `Runs: query` |
> | `start_time` (defaults to 1 day ago) | `min_start_time` + `max_start_time` | Optional; default to a 1-day window ending now, same as `start_time` |
> | `offset` + `limit` | `cursor` + `page_size` | Offset pagination replaced by cursor pagination |
> | `filter` (evaluated against runs) | `filter` | Same syntax; now evaluated against each thread's root run |

> [tab] TypeScript
>
> | Before (`listThreads`) | After (`threads.query`) | Notes |
> | - | - | - |
> | `projectId` XOR `projectName` | `project_id` | the new method takes only the UUID; resolve a name via `readProject()` first |
> | `startTime` (defaults to 1 day ago) | `min_start_time` + `max_start_time` | Optional; default to a 1-day window ending now, same as `startTime` |
> | `offset` + `limit` | `cursor` + `page_size` | Offset pagination replaced by cursor pagination |
> | `filter` | `filter` | Same syntax; now evaluated against each thread's root run |

> [tab] Java
>
> No query parameters to map. There was no dedicated method. The old approach used the generic run query (`is_root=true`, manual grouping by `thread_id` metadata). `threads().query()` takes `projectId`, `minStartTime`, `maxStartTime` (both optional, defaulting to a 1-day window ending now), `filter`, `pageSize`, `cursor`.

> [tab] Go
>
> No query parameters to map. There was no dedicated method. The old approach used the generic run query (`IsRoot: true`, manual grouping by `thread_id` metadata). `Threads.Query()` takes `ProjectID`, `MinStartTime`, `MaxStartTime` (both optional, defaulting to a 1-day window ending now), `Filter`, `PageSize`, `Cursor`.

> [tab] cURL
>
> `POST /api/v2/threads/query` body fields: `project_id`, `min_start_time` (optional), `max_start_time` (optional), `filter`, `page_size`, `cursor` (all `snake_case`). `min_start_time`/`max_start_time` default to a 1-day window ending now when omitted.

#### Response fields

> [tab] Python
>
> Python's legacy `ListThreadsItem` only has `thread_id`, `runs` (full embedded `Run[]`), `count`, `min_start_time`, `max_start_time`. It has no token/cost/latency/feedback fields at all.
>
> The new `Thread` never embeds the full run list (that is what `threads.list_traces` is for) but adds real `feedback_stats`, `latency_p50`/`latency_p99`, cost/token sums with per-category `_details`, `first_trace_id`/`last_trace_id`, `first_inputs`/`last_outputs` previews, `last_error`, `num_errored_turns`.
>
> | Before (legacy `ListThreadsItem`) | After (new `Thread`) | Notes |
> | - | - | - |
> | `thread_id` | `thread_id` | Unchanged |
> | `runs` (full embedded `Run[]`) | *(not available)* | Use `threads.list_traces` for per-trace detail |
> | `count` | `count` | Unchanged |
> | `min_start_time` | `min_start_time` | Unchanged |
> | `max_start_time` | `max_start_time` | Unchanged |
> | *(not available)* | `start_time` | New: a reference start time for this row, for example for sorting |
> | *(not available)* | `trace_id` | New: a representative root trace UUID, for example for deep links |
> | *(not available)* | `first_trace_id`, `last_trace_id` | New: chronologically first/last trace UUID in the query window |
> | *(not available)* | `first_inputs`, `last_outputs` | New: truncated previews from the first/last trace |
> | *(not available)* | `last_error` | New |
> | *(not available)* | `num_errored_turns` | New |
> | *(not available)* | `latency_p50`, `latency_p99` | New |
> | *(not available)* | `total_tokens`, `total_cost` | New |
> | *(not available)* | `total_token_details`, `total_cost_details` | New: per-category dicts, unlike `threads.list_traces` these are not wrapped in `.raw` |
> | *(not available)* | `feedback_stats` | New |

> [tab] TypeScript
>
> | Before (legacy `ListThreadsItem`) | After (new `Thread`) | Notes |
> | - | - | - |
> | `thread_id` | `thread_id` | Unchanged |
> | `runs` (full embedded `Run[]`) | *(not available)* | Use `threads.listTraces` for per-trace detail |
> | `count` | `count` | Unchanged |
> | `min_start_time` | `min_start_time` | Unchanged |
> | `max_start_time` | `max_start_time` | Unchanged |
> | `total_tokens` | `total_tokens` | Unchanged |
> | `total_cost` | `total_cost` | Unchanged |
> | `latency_p50`, `latency_p99` | `latency_p50`, `latency_p99` | Unchanged |
> | `feedback_stats` | `feedback_stats` | Unchanged |
> | `first_inputs`, `last_outputs` | `first_inputs`, `last_outputs` | Unchanged |
> | `last_error` | `last_error` | Unchanged |
> | *(not available)* | `start_time` | New: a reference start time for this row, for example for sorting |
> | *(not available)* | `trace_id` | New: a representative root trace UUID, for example for deep links |
> | *(not available)* | `first_trace_id`, `last_trace_id` | New: chronologically first/last trace UUID in the query window |
> | *(not available)* | `num_errored_turns` | New |
> | *(not available)* | `total_token_details`, `total_cost_details` | New: per-category dicts, unlike `threads.listTraces` these are not wrapped in `.raw` |

> [tab] Java
>
> `Thread` has 19 fields: `threadId`, `count`, `feedbackStats`, `firstInputs`, `firstTraceId`, `lastError`, `lastOutputs`, `lastTraceId`, `latencyP50`, `latencyP99`, `maxStartTime`, `minStartTime`, `numErroredTurns`, `startTime`, `totalCost`, `totalCostDetails`, `totalTokenDetails`, `totalTokens`, `traceId` (all `Optional`).
>
> The legacy SDK never had a typed response for this. Java's closest equivalent grouped raw `runs().query()` results by the `thread_id` metadata client-side. Every field below is new.
>
> | New `Thread` method | Notes |
> | - | - |
> | `threadId()` | |
> | `count()` | |
> | `minStartTime()`, `maxStartTime()`, `startTime()` | |
> | `firstTraceId()`, `lastTraceId()`, `traceId()` | `traceId()` is a representative root trace UUID, for example for deep links, in addition to the first/last trace UUIDs |
> | `firstInputs()`, `lastOutputs()` | Truncated previews from the first/last trace |
> | `lastError()` | |
> | `numErroredTurns()` | |
> | `latencyP50()`, `latencyP99()` | |
> | `totalTokens()`, `totalCost()` | |
> | `totalTokenDetails()`, `totalCostDetails()` | Per-category maps |
> | `feedbackStats()` | |

> [tab] Go
>
> `Thread` has 19 fields, in `PascalCase` Go struct form (e.g. `ThreadID`, `Count`, `LatencyP50`).
>
> The legacy SDK never had a typed response for this. Go's closest equivalent grouped raw `Runs.Query()` results by the `thread_id` metadata client-side. Every field below is new.
>
> | New `Thread` field | Notes |
> | - | - |
> | `ThreadID` | |
> | `Count` | |
> | `MinStartTime`, `MaxStartTime`, `StartTime` | |
> | `FirstTraceID`, `LastTraceID`, `TraceID` | `TraceID` is a representative root trace UUID, for example for deep links, in addition to the first/last trace UUIDs |
> | `FirstInputs`, `LastOutputs` | Truncated previews from the first/last trace |
> | `LastError` | |
> | `NumErroredTurns` | |
> | `LatencyP50`, `LatencyP99` | |
> | `TotalTokens`, `TotalCost` | |
> | `TotalTokenDetails`, `TotalCostDetails` | Per-category maps |
> | `FeedbackStats` | |

> [tab] cURL
>
> JSON response fields use `snake_case`: `thread_id`, `count`, `feedback_stats`, `first_inputs`, `first_trace_id`, `last_error`, `last_outputs`, `last_trace_id`, `latency_p50`, `latency_p99`, `max_start_time`, `min_start_time`, `num_errored_turns`, `start_time`, `total_cost`, `total_cost_details`, `total_token_details`, `total_tokens`, `trace_id`.
>
> The legacy API never had a dedicated threads endpoint. The closest equivalent was `POST /api/v1/runs/query`, grouped client-side by the `thread_id` metadata. Every field below is new.
>
> | New `threads.query` response field | Notes |
> | - | - |
> | `thread_id` | |
> | `count` | |
> | `min_start_time`, `max_start_time`, `start_time` | |
> | `first_trace_id`, `last_trace_id`, `trace_id` | `trace_id` is a representative root trace UUID, for example for deep links, in addition to the first/last trace UUIDs |
> | `first_inputs`, `last_outputs` | Truncated previews from the first/last trace |
> | `last_error` | |
> | `num_errored_turns` | |
> | `latency_p50`, `latency_p99` | |
> | `total_tokens`, `total_cost` | |
> | `total_token_details`, `total_cost_details` | Per-category dicts |
> | `feedback_stats` | |

### Examples

#### List threads in a project

Fetch every thread with activity in a project during a time range.

> [tab] Python
>
> > [tab] Before
> >
> > ```python Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > from langsmith import Client
> >
> > client = Client()
> > threads = client.list_threads(project_name="default")
> > for thread in threads:
> >     print(thread["thread_id"], thread["count"])
> > ```
>
> > [tab] After
> >
> > ```python After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import asyncio
> > from datetime import datetime, timedelta, timezone
> >
> > from langsmith import Client
> >
> >
> > async def main():
> >     client = Client()
> >     project = await client.aread_project(project_name="default")
> >     async for thread in client.threads.query(
> >         project_id=str(project.id),
> >         min_start_time=datetime.now(timezone.utc) - timedelta(days=30),
> >         max_start_time=datetime.now(timezone.utc),
> >     ):
> >         print(thread.thread_id, thread.count)
> >
> >
> > asyncio.run(main())
> > ```

> [tab] TypeScript
>
> > [tab] Before
> >
> > ```ts Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import { Client } from "langsmith";
> >
> > const client = new Client();
> > const threads = await client.listThreads({ projectName: "default" });
> > for (const thread of threads) {
> >   console.log(thread.thread_id, thread.count);
> > }
> > ```
>
> > [tab] After
> >
> > ```ts After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import { Client } from "langsmith";
> >
> > const client = new Client();
> > const project = await client.readProject({ projectName: "default" });
> > for await (const thread of client.threads.query({
> >   project_id: project.id,
> >   min_start_time: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString(),
> >   max_start_time: new Date().toISOString(),
> > })) {
> >   console.log(thread.thread_id, thread.count);
> > }
> > ```

> [tab] Java
>
> > [tab] Before
> >
> > ```kotlin Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import com.langchain.smith.client.LangsmithClient
> > import com.langchain.smith.client.okhttp.LangsmithOkHttpClient
> > import com.langchain.smith.models.runs.RunQueryParams
> > import com.langchain.smith.models.sessions.SessionListParams
> >
> > val client: LangsmithClient = LangsmithOkHttpClient.fromEnv()
> >
> > val project = client.sessions().list(
> >     SessionListParams.builder().name("default").limit(1L).build()
> > ).items().first()
> >
> > // v1 has no dedicated thread grouping — the generic run query returns raw
> > // root runs, with no built-in way to bucket them by thread.
> > val rootRuns = client.runs().query(
> >     RunQueryParams.builder()
> >         .addSession(project.id())
> >         .isRoot(true)
> >         .build()
> > ).runs()
> > for (run in rootRuns) {
> >     println("${run.traceId()} ${run.id()}")
> > }
> > ```
>
> > [tab] After
> >
> > ```kotlin After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import java.time.OffsetDateTime
> >
> > import com.langchain.smith.client.LangsmithClient
> > import com.langchain.smith.client.okhttp.LangsmithOkHttpClient
> > import com.langchain.smith.models.sessions.SessionListParams
> > import com.langchain.smith.models.threads.ThreadQueryParams
> >
> > val client: LangsmithClient = LangsmithOkHttpClient.fromEnv()
> >
> > val project = client.sessions().list(
> >     SessionListParams.builder().name("default").limit(1L).build()
> > ).items().first()
> >
> > val threads = client.threads().query(
> >     ThreadQueryParams.builder()
> >         .projectId(project.id())
> >         .minStartTime(OffsetDateTime.now().minusMonths(1))
> >         .maxStartTime(OffsetDateTime.now())
> >         .build()
> > ).items()
> > for (thread in threads) {
> >     println("${thread.threadId().get()} ${thread.count().get()}")
> > }
> > ```

> [tab] Go
>
> > [tab] Before
> >
> > ```go Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > package main
> >
> > import (
> > 	"context"
> > 	"fmt"
> >
> > 	"github.com/langchain-ai/langsmith-go"
> > )
> >
> > func main() {
> > 	ctx := context.Background()
> > 	client := langsmith.NewClient()
> >
> > 	sessions, err := client.Sessions.List(ctx, langsmith.SessionListParams{
> > 		Name:  langsmith.F("default"),
> > 		Limit: langsmith.F(int64(1)),
> > 	})
> > 	if err != nil {
> > 		panic(err.Error())
> > 	}
> > 	projectID := sessions.Items[0].ID
> >
> > 	runs, err := client.Runs.Query(ctx, langsmith.RunQueryParams{
> > 		Session: langsmith.F([]string{projectID}),
> > 		IsRoot:  langsmith.F(true),
> > 	})
> > 	if err != nil {
> > 		panic(err.Error())
> > 	}
> >
> > 	threads := map[string]int{}
> > 	for _, run := range runs.Runs {
> > 		metadata, ok := run.Extra["metadata"].(map[string]interface{})
> > 		if !ok {
> > 			continue
> > 		}
> > 		threadID, ok := metadata["thread_id"].(string)
> > 		if ok {
> > 			threads[threadID]++
> > 		}
> > 	}
> > 	for threadID, count := range threads {
> > 		fmt.Println(threadID, count)
> > 	}
> > }
> > ```
>
> > [tab] After
> >
> > ```go After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > package main
> >
> > import (
> > 	"context"
> > 	"fmt"
> > 	"time"
> >
> > 	"github.com/langchain-ai/langsmith-go"
> > )
> >
> > func main() {
> > 	ctx := context.Background()
> > 	client := langsmith.NewClient()
> >
> > 	sessions, err := client.Sessions.List(ctx, langsmith.SessionListParams{
> > 		Name:  langsmith.F("default"),
> > 		Limit: langsmith.F(int64(1)),
> > 	})
> > 	if err != nil {
> > 		panic(err.Error())
> > 	}
> > 	projectID := sessions.Items[0].ID
> >
> > 	maxStart := time.Now().UTC()
> > 	minStart := maxStart.AddDate(0, -1, 0)
> >
> > 	iter := client.Threads.QueryAutoPaging(ctx, langsmith.ThreadQueryParams{
> > 		ProjectID:    langsmith.F(projectID),
> > 		MinStartTime: langsmith.F(minStart),
> > 		MaxStartTime: langsmith.F(maxStart),
> > 	})
> > 	for iter.Next() {
> > 		thread := iter.Current()
> > 		fmt.Println(thread.ThreadID, thread.Count)
> > 	}
> > 	if err := iter.Err(); err != nil {
> > 		panic(err.Error())
> > 	}
> > }
> > ```

> [tab] cURL
>
> > [tab] Before
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > PROJECT_ID=$(curl -s "https://api.smith.langchain.com/api/v1/sessions?name=default&limit=1" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" | jq -r '.[0].id')
> >
> > curl -s -X POST "https://api.smith.langchain.com/api/v1/runs/query" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" \
> >   -H "Content-Type: application/json" \
> >   -d "$(jq -n --arg pid "$PROJECT_ID" '{"session": [$pid], "is_root": true}')" \
> >   | jq '[(.runs // [])[] | select(.extra.metadata.thread_id != null)] | group_by(.extra.metadata.thread_id) | map({
> >       thread_id: .[0].extra.metadata.thread_id,
> >       count: length
> >     })'
> > ```
>
> > [tab] After
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > PROJECT_ID=$(curl -s "https://api.smith.langchain.com/api/v1/sessions?name=default&limit=1" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" | jq -r '.[0].id')
> >
> > MAX_START=$(date -u +%Y-%m-%dT%H:%M:%SZ)
> > MIN_START=$(date -u -d '-1 month' +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -v-1m +%Y-%m-%dT%H:%M:%SZ)
> > curl -X POST "https://api.smith.langchain.com/api/v2/threads/query" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" \
> >   -H "Content-Type: application/json" \
> >   -d "$(jq -n --arg pid "$PROJECT_ID" --arg min "$MIN_START" --arg max "$MAX_START" '{
> >     "project_id": $pid,
> >     "min_start_time": $min,
> >     "max_start_time": $max
> >   }')"
> > ```

#### Find threads with errors

Find threads that had a turn end in an error.

> [tab] Python
>
> > [tab] Before
> >
> > ```python Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > from langsmith import Client
> >
> > client = Client()
> > threads = client.list_threads(project_name="default", filter='eq(status, "error")')
> > for thread in threads:
> >     print(thread["thread_id"])
> > ```
>
> > [tab] After
> >
> > ```python After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import asyncio
> > from datetime import datetime, timedelta, timezone
> >
> > from langsmith import Client
> >
> >
> > async def main():
> >     client = Client()
> >     project = await client.aread_project(project_name="default")
> >     async for thread in client.threads.query(
> >         project_id=str(project.id),
> >         min_start_time=datetime.now(timezone.utc) - timedelta(days=30),
> >         max_start_time=datetime.now(timezone.utc),
> >         filter='eq(status, "error")',
> >     ):
> >         print(thread.thread_id, thread.last_error)
> >
> >
> > asyncio.run(main())
> > ```

> [tab] TypeScript
>
> > [tab] Before
> >
> > ```ts Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import { Client } from "langsmith";
> >
> > const client = new Client();
> > const threads = await client.listThreads({
> >   projectName: "default",
> >   filter: 'eq(status, "error")',
> > });
> > for (const thread of threads) {
> >   console.log(thread.thread_id, thread.last_error);
> > }
> > ```
>
> > [tab] After
> >
> > ```ts After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import { Client } from "langsmith";
> >
> > const client = new Client();
> > const project = await client.readProject({ projectName: "default" });
> > for await (const thread of client.threads.query({
> >   project_id: project.id,
> >   min_start_time: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString(),
> >   max_start_time: new Date().toISOString(),
> >   filter: 'eq(status, "error")',
> > })) {
> >   console.log(thread.thread_id, thread.last_error);
> > }
> > ```

> [tab] Java
>
> > [tab] Before
> >
> > ```kotlin Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import com.langchain.smith.client.LangsmithClient
> > import com.langchain.smith.client.okhttp.LangsmithOkHttpClient
> > import com.langchain.smith.models.runs.RunQueryParams
> > import com.langchain.smith.models.sessions.SessionListParams
> > import kotlin.jvm.optionals.getOrNull
> >
> > val client: LangsmithClient = LangsmithOkHttpClient.fromEnv()
> >
> > val project = client.sessions().list(
> >     SessionListParams.builder().name("default").limit(1L).build()
> > ).items().first()
> >
> > val rootRuns = client.runs().query(
> >     RunQueryParams.builder()
> >         .addSession(project.id())
> >         .isRoot(true)
> >         .filter("eq(status, \"error\")")
> >         .build()
> > ).runs()
> > for (run in rootRuns) {
> >     println("${run.traceId()} ${run.error().getOrNull()}")
> > }
> > ```
>
> > [tab] After
> >
> > ```kotlin After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import java.time.OffsetDateTime
> >
> > import com.langchain.smith.client.LangsmithClient
> > import com.langchain.smith.client.okhttp.LangsmithOkHttpClient
> > import com.langchain.smith.models.sessions.SessionListParams
> > import com.langchain.smith.models.threads.ThreadQueryParams
> > import kotlin.jvm.optionals.getOrNull
> >
> > val client: LangsmithClient = LangsmithOkHttpClient.fromEnv()
> >
> > val project = client.sessions().list(
> >     SessionListParams.builder().name("default").limit(1L).build()
> > ).items().first()
> >
> > val threads = client.threads().query(
> >     ThreadQueryParams.builder()
> >         .projectId(project.id())
> >         .minStartTime(OffsetDateTime.now().minusMonths(1))
> >         .maxStartTime(OffsetDateTime.now())
> >         .filter("eq(status, \"error\")")
> >         .build()
> > ).items()
> > for (thread in threads) {
> >     println("${thread.threadId().get()} ${thread.lastError().getOrNull()}")
> > }
> > ```

> [tab] Go
>
> > [tab] Before
> >
> > ```go Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > package main
> >
> > import (
> > 	"context"
> > 	"fmt"
> >
> > 	"github.com/langchain-ai/langsmith-go"
> > )
> >
> > func main() {
> > 	ctx := context.Background()
> > 	client := langsmith.NewClient()
> >
> > 	sessions, err := client.Sessions.List(ctx, langsmith.SessionListParams{
> > 		Name:  langsmith.F("default"),
> > 		Limit: langsmith.F(int64(1)),
> > 	})
> > 	if err != nil {
> > 		panic(err.Error())
> > 	}
> > 	projectID := sessions.Items[0].ID
> >
> > 	runs, err := client.Runs.Query(ctx, langsmith.RunQueryParams{
> > 		Session: langsmith.F([]string{projectID}),
> > 		IsRoot:  langsmith.F(true),
> > 		Filter:  langsmith.F(`eq(status, "error")`),
> > 	})
> > 	if err != nil {
> > 		panic(err.Error())
> > 	}
> >
> > 	threadIDs := map[string]bool{}
> > 	for _, run := range runs.Runs {
> > 		metadata, ok := run.Extra["metadata"].(map[string]interface{})
> > 		if !ok {
> > 			continue
> > 		}
> > 		if threadID, ok := metadata["thread_id"].(string); ok {
> > 			threadIDs[threadID] = true
> > 		}
> > 	}
> > 	for threadID := range threadIDs {
> > 		fmt.Println(threadID)
> > 	}
> > }
> > ```
>
> > [tab] After
> >
> > ```go After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > package main
> >
> > import (
> > 	"context"
> > 	"fmt"
> > 	"time"
> >
> > 	"github.com/langchain-ai/langsmith-go"
> > )
> >
> > func main() {
> > 	ctx := context.Background()
> > 	client := langsmith.NewClient()
> >
> > 	sessions, err := client.Sessions.List(ctx, langsmith.SessionListParams{
> > 		Name:  langsmith.F("default"),
> > 		Limit: langsmith.F(int64(1)),
> > 	})
> > 	if err != nil {
> > 		panic(err.Error())
> > 	}
> > 	projectID := sessions.Items[0].ID
> >
> > 	maxStart := time.Now().UTC()
> > 	minStart := maxStart.AddDate(0, -1, 0)
> >
> > 	iter := client.Threads.QueryAutoPaging(ctx, langsmith.ThreadQueryParams{
> > 		ProjectID:    langsmith.F(projectID),
> > 		MinStartTime: langsmith.F(minStart),
> > 		MaxStartTime: langsmith.F(maxStart),
> > 		Filter:       langsmith.F(`eq(status, "error")`),
> > 	})
> > 	for iter.Next() {
> > 		thread := iter.Current()
> > 		fmt.Println(thread.ThreadID, thread.LastError)
> > 	}
> > 	if err := iter.Err(); err != nil {
> > 		panic(err.Error())
> > 	}
> > }
> > ```

> [tab] cURL
>
> > [tab] Before
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > PROJECT_ID=$(curl -s "https://api.smith.langchain.com/api/v1/sessions?name=default&limit=1" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" | jq -r '.[0].id')
> >
> > curl -s -X POST "https://api.smith.langchain.com/api/v1/runs/query" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" \
> >   -H "Content-Type: application/json" \
> >   -d "$(jq -n --arg pid "$PROJECT_ID" '{"session": [$pid], "is_root": true, "filter": "eq(status, \"error\")"}')" \
> >   | jq -r '[(.runs // [])[].extra.metadata.thread_id] | unique | .[]'
> > ```
>
> > [tab] After
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > PROJECT_ID=$(curl -s "https://api.smith.langchain.com/api/v1/sessions?name=default&limit=1" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" | jq -r '.[0].id')
> >
> > MAX_START=$(date -u +%Y-%m-%dT%H:%M:%SZ)
> > MIN_START=$(date -u -d '-1 month' +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -v-1m +%Y-%m-%dT%H:%M:%SZ)
> > curl -X POST "https://api.smith.langchain.com/api/v2/threads/query" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" \
> >   -H "Content-Type: application/json" \
> >   -d "$(jq -n --arg pid "$PROJECT_ID" --arg min "$MIN_START" --arg max "$MAX_START" '{
> >     "project_id": $pid,
> >     "min_start_time": $min,
> >     "max_start_time": $max,
> >     "filter": "eq(status, \"error\")"
> >   }')"
> > ```

## Threads: list traces

Retrieve all traces belonging to a specific thread within a project.

### Main changes

#### Method name

> [tab] Python
>
> | Before | After |
> | - | - |
> | `client.read_thread()` | `client.threads.list_traces()` |
>
> > [!NOTE]
> >
> > `client.threads.list_traces()` is now async. Call it with `await`.
>
> See the [reference](https://reference.langchain.com/python/langsmith/_openapi_client/resources/threads/ThreadsResource/list_traces) for the full parameter and field list.

> [tab] TypeScript
>
> | Before | After |
> | - | - |
> | `client.readThread()` | `client.threads.listTraces()` |
>
> See the [reference](https://reference.langchain.com/javascript/langsmith/_openapi_client/Langsmith/Threads/listTraces) for the full parameter and field list.

> [tab] Java
>
> > [!NOTE]
> >
> > Java never had a dedicated per-thread method. The closest legacy equivalent is the generic run query filtered by the `thread_id` metadata convention.
>
> | Before | After |
> | - | - |
> | `client.runs().query()` (filtered by `thread_id`) | `client.threads().listTraces()` |
>
> See the [reference](https://javadoc.io/doc/com.langchain.smith/langsmith-java/latest/com/langchain/smith/services/blocking/ThreadService.html) for the full parameter list.

> [tab] Go
>
> > [!NOTE]
> >
> > Go never had a dedicated per-thread method. The closest legacy equivalent is the generic run query filtered by the `thread_id` metadata convention.
>
> | Before | After |
> | - | - |
> | `client.Runs.Query()` (filtered by `thread_id`) | `client.Threads.ListTraces()` |
>
> See the [reference](https://pkg.go.dev/github.com/langchain-ai/langsmith-go#ThreadService.ListTracesAutoPaging) for the full parameter list.

> [tab] cURL
>
> | Before | After |
> | - | - |
> | `POST /api/v1/runs/query` (`filter=eq(thread_id, ...)`) | `GET /api/v2/threads/{thread_id}/traces` |
>
> See the [API doc](../LangSmith%20REST%20API/Threads/Query%20thread%20traces.md) for the full parameter and field list.

#### Query parameters

> [tab] Python
>
> `read_thread`'s `is_root` has no new equivalent. `list_traces` always returns traces (root runs) only, matching its name. `read_thread`'s `order` (asc/desc) also has no new equivalent: results are always sorted by `start_time` ascending, a fixed server-side order.
>
> | Before (`read_thread`) | After (`list_traces`) | Notes |
> | - | - | - |
> | `thread_id` | `thread_id` (path param) | Unchanged |
> | `project_id` XOR `project_name` | `project_id` | The new method takes only the UUID |
> | `is_root` | *(not available)* | The new method always returns traces (root runs) only |
> | `order` | *(not available)* | No sort/order field on the new method |
> | `filter` | `filter` | Same syntax, now evaluated against each root trace run |
> | `select` (arbitrary run field list) | `selects` | The new method uses `ThreadTraceSelectField`, a 24-value uppercase enum |
> | *(not available)* | `page_size` + `cursor` | The new method adds cursor pagination |

> [tab] TypeScript
>
> `readThread`'s `isRoot` has no new equivalent. `listTraces` always returns traces (root runs) only, matching its name. `readThread`'s `order` (asc/desc) also has no new equivalent: results are always sorted by `start_time` ascending, a fixed server-side order.
>
> | Before (`readThread`) | After (`listTraces`) | Notes |
> | - | - | - |
> | `threadId` | `threadId` (path param) | Unchanged |
> | `projectId` XOR `projectName` | `project_id` | The new method takes only the UUID |
> | `isRoot` | *(not available)* | The new method always returns traces (root runs) only |
> | `order` | *(not available)* | No sort/order field on the new method |
> | `filter` | `filter` | Same syntax, now evaluated against each root trace run |
> | `select` (arbitrary run field list) | `selects` | The new method uses a 24-value uppercase enum |
> | *(not available)* | `page_size` + `cursor` | The new method adds cursor pagination |

> [tab] Java
>
> No query parameters to map. There was no dedicated method. `listTraces(threadId, params)` takes `projectId`, `filter`, `pageSize`, `cursor`, `selects` (24-value enum). Results are always sorted by `startTime` ascending, a fixed server-side order.

> [tab] Go
>
> No query parameters to map. There was no dedicated method. `ListTraces(ctx, threadID, params)` takes `ProjectID`, `Filter`, `PageSize`, `Cursor`, `Selects` (24-value enum). Results are always sorted by `StartTime` ascending, a fixed server-side order.

> [tab] cURL
>
> `GET /api/v2/threads/{thread_id}/traces` query params: `project_id`, `filter`, `page_size`, `cursor`, `selects` (repeatable), all `snake_case`. Results are always sorted by `start_time` ascending, a fixed server-side order.

#### Response fields

> [tab] Python
>
> The legacy `read_thread` returns full `Run` objects (a generator). The new `ThreadTrace` is lightweight: preview fields (`inputs_preview`/`outputs_preview`) instead of full `inputs`/`outputs`, no embedded child runs. `selects` controls what's populated, the same as `traces.query`.
>
> | Before (legacy `Run` field, via `read_thread`) | After (new `ThreadTrace` field) | Notes |
> | - | - | - |
> | `id` | *(not available)* | the legacy root run `id` and `trace_id` were identical; the new API exposes only `trace_id` |
> | `trace_id` | `trace_id` | Returned by default when `selects` is omitted |
> | `name` | `name` | Omitted unless included in `selects` |
> | `start_time` | `start_time` | Omitted unless included in `selects` |
> | `end_time` | `end_time` | Omitted unless included in `selects` |
> | `run_type` | `op` | Renamed; encoded as a number instead of a string |
> | `inputs` | `inputs_preview`, or `inputs` for the untruncated payload | Truncated preview by default; select `INPUTS` for the full payload |
> | `outputs` | `outputs_preview`, or `outputs` for the untruncated payload | Truncated preview by default; select `OUTPUTS` for the full payload |
> | `error` | `error_preview`, or `error` for the full message | Truncated summary by default; select `ERROR` for the full error message |
> | `latency` (property) | `latency` | Native field instead of a computed `timedelta` property |
> | `total_tokens`, `prompt_tokens`, `completion_tokens` | `total_tokens`, `prompt_tokens`, `completion_tokens` | Unchanged |
> | `total_cost`, `prompt_cost`, `completion_cost` | `total_cost`, `prompt_cost`, `completion_cost` | Unchanged |
> | `prompt_token_details`, `completion_token_details` | `prompt_token_details`, `completion_token_details` | Field now wraps the dict; access `.raw` |
> | `prompt_cost_details`, `completion_cost_details` | `prompt_cost_details`, `completion_cost_details` | Field now wraps the dict; access `.raw` |
> | `first_token_time` | `first_token_time` | Omitted unless included in `selects` |
> | *(not available)* | `thread_id` | New: the thread UUID this trace belongs to |
> | `child_runs`, `child_run_ids` | *(not available)* | No embedded child runs; use `traces.list_runs` for descendant runs |

> [tab] TypeScript
>
> The legacy `readThread` returns full `Run` objects (an async generator). The new `ThreadTrace` is lightweight: preview fields (`inputs_preview`/`outputs_preview`) instead of full `inputs`/`outputs`, no embedded child runs. `selects` controls what is populated, the same as `traces.query`.
>
> | Before (legacy `Run` field, via `readThread`) | After (new `ThreadTrace` field) | Notes |
> | - | - | - |
> | `id` | *(not available)* | the legacy root run `id` and `trace_id` were identical; the new API exposes only `trace_id` |
> | `trace_id` | `trace_id` | Returned by default when `selects` is omitted |
> | `name` | `name` | Omitted unless included in `selects` |
> | `start_time` | `start_time` | Omitted unless included in `selects` |
> | `end_time` | `end_time` | Omitted unless included in `selects` |
> | `run_type` | `op` | Renamed; encoded as a number instead of a string |
> | `inputs` | `inputs_preview`, or `inputs` for the untruncated payload | Truncated preview by default; select `INPUTS` for the full payload |
> | `outputs` | `outputs_preview`, or `outputs` for the untruncated payload | Truncated preview by default; select `OUTPUTS` for the full payload |
> | `error` | `error_preview`, or `error` for the full message | Truncated summary by default; select `ERROR` for the full error message |
> | `latency` | `latency` | Native field on the new type |
> | `total_tokens`, `prompt_tokens`, `completion_tokens` | `total_tokens`, `prompt_tokens`, `completion_tokens` | Unchanged |
> | `total_cost`, `prompt_cost`, `completion_cost` | `total_cost`, `prompt_cost`, `completion_cost` | Unchanged |
> | `prompt_token_details`, `completion_token_details` | `prompt_token_details`, `completion_token_details` | Unchanged |
> | `prompt_cost_details`, `completion_cost_details` | `prompt_cost_details`, `completion_cost_details` | Unchanged |
> | `first_token_time` | `first_token_time` | Omitted unless included in `selects` |
> | *(not available)* | `thread_id` | New: the thread UUID this trace belongs to |
> | `child_runs`, `child_run_ids` | *(not available)* | No embedded child runs; use `traces.listRuns` for descendant runs |

> [tab] Java
>
> `ThreadTrace` has 24 `Optional` fields: `traceId`, `threadId`, `name`, `startTime`, `endTime`, `latency`, `op`, token/cost fields with per-category `_details`, `inputsPreview`/`outputsPreview`/`inputs`/`outputs`, `errorPreview`/`error`, `firstTokenTime`.
>
> | Before (legacy `RunSchema` method) | After (new `ThreadTrace` method) | Notes |
> | - | - | - |
> | `id()` | *(not available)* | the legacy root run `id()` and `traceId()` were identical; the new API exposes only `traceId()` |
> | `traceId()` | `traceId()` | Returned by default when `selects` is omitted |
> | `name()` | `name()` | Omitted unless included in `selects` |
> | `startTime()` | `startTime()` | Omitted unless included in `selects` |
> | `endTime()` | `endTime()` | Omitted unless included in `selects` |
> | `runType()` | `op()` | Renamed; encoded as a number instead of a string |
> | `inputs()` | `inputsPreview()`, or `inputs()` for the untruncated payload | Truncated preview by default; select `INPUTS` for the full payload |
> | `outputs()` | `outputsPreview()`, or `outputs()` for the untruncated payload | Truncated preview by default; select `OUTPUTS` for the full payload |
> | `error()` | `errorPreview()`, or `error()` for the full message | Truncated summary by default; select `ERROR` for the full error message |
> | `latency()` | `latency()` | Unchanged |
> | `totalTokens()`, `promptTokens()`, `completionTokens()` | `totalTokens()`, `promptTokens()`, `completionTokens()` | Unchanged |
> | `totalCost()`, `promptCost()`, `completionCost()` | `totalCost()`, `promptCost()`, `completionCost()` | Unchanged |
> | `promptTokenDetails()`, `completionTokenDetails()` | `promptTokenDetails()`, `completionTokenDetails()` | Unchanged |
> | `promptCostDetails()`, `completionCostDetails()` | `promptCostDetails()`, `completionCostDetails()` | Unchanged |
> | `firstTokenTime()` | `firstTokenTime()` | Omitted unless included in `selects` |
> | *(not available)* | `threadId()` | New: the thread UUID this trace belongs to |
> | `childRuns()`, `childRunIds()` | *(not available)* | No embedded child runs; use `traces().listRuns()` for descendant runs |

> [tab] Go
>
> `ThreadTrace` has 24 fields, in `PascalCase` Go struct form.
>
> | Before (legacy root `Run` field) | After (new `ThreadTrace` field) | Notes |
> | - | - | - |
> | `ID` | *(not available)* | the legacy root run `ID` and `TraceID` were identical; the new API exposes only `TraceID` |
> | `TraceID` | `TraceID` | Returned by default when `Selects` is omitted |
> | `Name` | `Name` | Omitted unless included in `Selects` |
> | `StartTime` | `StartTime` | Omitted unless included in `Selects` |
> | `EndTime` | `EndTime` | Omitted unless included in `Selects` |
> | `RunType` | `Op` | Renamed; encoded as a number instead of a string |
> | `Inputs` | `InputsPreview`, or `Inputs` for the untruncated payload | Truncated preview by default; select `INPUTS` for the full payload |
> | `Outputs` | `OutputsPreview`, or `Outputs` for the untruncated payload | Truncated preview by default; select `OUTPUTS` for the full payload |
> | `Error` | `ErrorPreview`, or `Error` for the full message | Truncated summary by default; select `ERROR` for the full error message |
> | `Latency` | `Latency` | Unchanged |
> | `TotalTokens`, `PromptTokens`, `CompletionTokens` | `TotalTokens`, `PromptTokens`, `CompletionTokens` | Unchanged |
> | `TotalCost`, `PromptCost`, `CompletionCost` | `TotalCost`, `PromptCost`, `CompletionCost` | Unchanged |
> | `PromptTokenDetails`, `CompletionTokenDetails` | `PromptTokenDetails`, `CompletionTokenDetails` | Unchanged |
> | `PromptCostDetails`, `CompletionCostDetails` | `PromptCostDetails`, `CompletionCostDetails` | Unchanged |
> | `FirstTokenTime` | `FirstTokenTime` | Omitted unless included in `Selects` |
> | *(not available)* | `ThreadID` | New: the thread UUID this trace belongs to |
> | `ChildRuns`, `ChildRunIDs` | *(not available)* | No embedded child runs; use `Traces.ListRuns` for descendant runs |

> [tab] cURL
>
> JSON response fields use `snake_case`, matching the table below.
>
> | Before (legacy root run field) | After (new `ThreadTrace` field) | Notes |
> | - | - | - |
> | `id` | *(not available)* | the legacy root run `id` and `trace_id` were identical; the new API exposes only `trace_id` |
> | `trace_id` | `trace_id` | Returned by default when `selects` is omitted |
> | `name` | `name` | Omitted unless included in `selects` |
> | `start_time` | `start_time` | Omitted unless included in `selects` |
> | `end_time` | `end_time` | Omitted unless included in `selects` |
> | `run_type` | `op` | Renamed; encoded as a number instead of a string |
> | `inputs` | `inputs_preview`, or `inputs` for the untruncated payload | Truncated preview by default; select `INPUTS` for the full payload |
> | `outputs` | `outputs_preview`, or `outputs` for the untruncated payload | Truncated preview by default; select `OUTPUTS` for the full payload |
> | `error` | `error_preview`, or `error` for the full message | Truncated summary by default; select `ERROR` for the full error message |
> | `latency` | `latency` | Unchanged |
> | `total_tokens`, `prompt_tokens`, `completion_tokens` | `total_tokens`, `prompt_tokens`, `completion_tokens` | Unchanged |
> | `total_cost`, `prompt_cost`, `completion_cost` | `total_cost`, `prompt_cost`, `completion_cost` | Unchanged |
> | `prompt_token_details`, `completion_token_details` | `prompt_token_details`, `completion_token_details` | Unchanged |
> | `prompt_cost_details`, `completion_cost_details` | `prompt_cost_details`, `completion_cost_details` | Unchanged |
> | `first_token_time` | `first_token_time` | Omitted unless included in `selects` |
> | *(not available)* | `thread_id` | New: the thread UUID this trace belongs to |
> | `child_runs`, `child_run_ids` | *(not available)* | No embedded child runs; use `traces.list_runs` for descendant runs |

### Examples

#### List every trace (turn) in a thread

Fetch all the traces (conversation turns) that belong to one thread.

> [tab] Python
>
> > [tab] Before
> >
> > ```python Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > from langsmith import Client
> >
> > client = Client()
> > thread_id = "<thread-id>"
> > for run in client.read_thread(thread_id=thread_id, project_name="default"):
> >     print(run.id, run.start_time)
> > ```
>
> > [tab] After
> >
> > ```python After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import asyncio
> >
> > from langsmith import Client
> >
> >
> > async def main():
> >     client = Client()
> >     project = await client.aread_project(project_name="default")
> >     thread_id = "<thread-id>"
> >     async for trace in client.threads.list_traces(
> >         thread_id, project_id=str(project.id), selects=["TRACE_ID", "START_TIME"]
> >     ):
> >         print(trace.trace_id, trace.start_time)
> >
> >
> > asyncio.run(main())
> > ```

> [tab] TypeScript
>
> > [tab] Before
> >
> > ```ts Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import { Client } from "langsmith";
> >
> > const client = new Client();
> > let threadId = "<thread-id>";
> > for await (const run of client.readThread({ threadId, projectName: "default" })) {
> >   console.log(run.id, run.start_time);
> > }
> > ```
>
> > [tab] After
> >
> > ```ts After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import { Client } from "langsmith";
> >
> > const client = new Client();
> > const project = await client.readProject({ projectName: "default" });
> > let threadId = "<thread-id>";
> > for await (const trace of client.threads.listTraces(threadId, {
> >   project_id: project.id,
> >   selects: ["TRACE_ID", "START_TIME"],
> > })) {
> >   console.log(trace.trace_id, trace.start_time);
> > }
> > ```

> [tab] Java
>
> > [tab] Before
> >
> > ```kotlin Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> >
> > import com.langchain.smith.client.LangsmithClient
> > import com.langchain.smith.client.okhttp.LangsmithOkHttpClient
> > import com.langchain.smith.models.runs.RunQueryParams
> > import com.langchain.smith.models.sessions.SessionListParams
> >
> > val client: LangsmithClient = LangsmithOkHttpClient.fromEnv()
> >
> > val project = client.sessions().list(
> >     SessionListParams.builder().name("default").limit(1L).build()
> > ).items().first()
> >
> > var threadId = "<thread-id>"
> >
> > val runs = client.runs().query(
> >     RunQueryParams.builder()
> >         .addSession(project.id())
> >         .isRoot(true)
> >         .filter("eq(thread_id, \"$threadId\")")
> >         .build()
> > ).runs()
> > for (run in runs) {
> >     println("${run.id()} ${run.startTime().get()}")
> > }
> > ```
>
> > [tab] After
> >
> > ```kotlin After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> >
> > import com.langchain.smith.client.LangsmithClient
> > import com.langchain.smith.client.okhttp.LangsmithOkHttpClient
> > import com.langchain.smith.models.sessions.SessionListParams
> > import com.langchain.smith.models.threads.ThreadListTracesParams
> >
> > val client: LangsmithClient = LangsmithOkHttpClient.fromEnv()
> >
> > val project = client.sessions().list(
> >     SessionListParams.builder().name("default").limit(1L).build()
> > ).items().first()
> >
> > var threadId = "<thread-id>"
> >
> > val traces = client.threads().listTraces(
> >     threadId,
> >     ThreadListTracesParams.builder()
> >         .projectId(project.id())
> >         .addSelect(ThreadListTracesParams.Select.TRACE_ID)
> >         .addSelect(ThreadListTracesParams.Select.START_TIME)
> >         .build()
> > ).items()
> > for (trace in traces) {
> >     println("${trace.traceId().get()} ${trace.startTime().get()}")
> > }
> > ```

> [tab] Go
>
> > [tab] Before
> >
> > ```go Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > package main
> >
> > import (
> > 	"context"
> > 	"fmt"
> > 	"time"
> >
> > 	"github.com/langchain-ai/langsmith-go"
> > )
> >
> > func main() {
> > 	ctx := context.Background()
> > 	client := langsmith.NewClient()
> >
> > 	sessions, err := client.Sessions.List(ctx, langsmith.SessionListParams{
> > 		Name:  langsmith.F("default"),
> > 		Limit: langsmith.F(int64(1)),
> > 	})
> > 	if err != nil {
> > 		panic(err.Error())
> > 	}
> > 	projectID := sessions.Items[0].ID
> > 	threadID := "<thread-id>"
> >
> > 	runs, err := client.Runs.Query(ctx, langsmith.RunQueryParams{
> > 		Session: langsmith.F([]string{projectID}),
> > 		IsRoot:  langsmith.F(true),
> > 		Filter:  langsmith.F(fmt.Sprintf(`eq(thread_id, "%s")`, threadID)),
> > 	})
> > 	if err != nil {
> > 		panic(err.Error())
> > 	}
> > 	for _, run := range runs.Runs {
> > 		fmt.Println(run.ID, run.StartTime)
> > 	}
> > }
> > ```
>
> > [tab] After
> >
> > ```go After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > package main
> >
> > import (
> > 	"context"
> > 	"fmt"
> > 	"time"
> >
> > 	"github.com/langchain-ai/langsmith-go"
> > )
> >
> > func main() {
> > 	ctx := context.Background()
> > 	client := langsmith.NewClient()
> >
> > 	sessions, err := client.Sessions.List(ctx, langsmith.SessionListParams{
> > 		Name:  langsmith.F("default"),
> > 		Limit: langsmith.F(int64(1)),
> > 	})
> > 	if err != nil {
> > 		panic(err.Error())
> > 	}
> > 	projectID := sessions.Items[0].ID
> > 	threadID := "<thread-id>"
> >
> > 	iter := client.Threads.ListTracesAutoPaging(ctx, threadID, langsmith.ThreadListTracesParams{
> > 		ProjectID: langsmith.F(projectID),
> > 		Selects:   langsmith.F([]langsmith.ThreadListTracesParamsSelect{langsmith.ThreadListTracesParamsSelectTraceID, langsmith.ThreadListTracesParamsSelectStartTime}),
> > 	})
> > 	for iter.Next() {
> > 		trace := iter.Current()
> > 		fmt.Println(trace.TraceID, trace.StartTime)
> > 	}
> > 	if err := iter.Err(); err != nil {
> > 		panic(err.Error())
> > 	}
> > }
> > ```

> [tab] cURL
>
> > [tab] Before
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > PROJECT_ID=$(curl -s "https://api.smith.langchain.com/api/v1/sessions?name=default&limit=1" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" | jq -r '.[0].id')
> > THREAD_ID="<thread-id>"
> >
> > curl -s -X POST "https://api.smith.langchain.com/api/v1/runs/query" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" \
> >   -H "Content-Type: application/json" \
> >   -d "$(jq -n --arg pid "$PROJECT_ID" --arg tid "$THREAD_ID" '{"session": [$pid], "is_root": true, "filter": ("eq(thread_id, \"" + $tid + "\")")}')" \
> >   | jq '.runs // []'
> > ```
>
> > [tab] After
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > PROJECT_ID=$(curl -s "https://api.smith.langchain.com/api/v1/sessions?name=default&limit=1" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" | jq -r '.[0].id')
> > THREAD_ID="<thread-id>"
> >
> > curl -G "https://api.smith.langchain.com/api/v2/threads/$THREAD_ID/traces" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" \
> >   --data-urlencode "project_id=$PROJECT_ID" \
> >   --data-urlencode "selects=TRACE_ID" \
> >   --data-urlencode "selects=START_TIME"
> > ```

#### Select specific trace's fields

Request just the fields you need instead of every field, to reduce response size.

> [tab] Python
>
> > [tab] Before
> >
> > ```python Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > from langsmith import Client
> >
> > client = Client()
> > thread_id = "<thread-id>"
> > for run in client.read_thread(
> >     thread_id=thread_id,
> >     project_name="default",
> >     select=["id", "total_tokens", "total_cost"],
> > ):
> >     print(run.id, run.total_tokens, run.total_cost)
> > ```
>
> > [tab] After
> >
> > ```python After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import asyncio
> >
> > from langsmith import Client
> >
> >
> > async def main():
> >     client = Client()
> >     project = await client.aread_project(project_name="default")
> >     thread_id = "<thread-id>"
> >     async for trace in client.threads.list_traces(
> >         thread_id,
> >         project_id=str(project.id),
> >         selects=["TRACE_ID", "TOTAL_TOKENS", "TOTAL_COST"],
> >     ):
> >         print(trace.trace_id, trace.total_tokens, trace.total_cost)
> >
> >
> > asyncio.run(main())
> > ```

> [tab] TypeScript
>
> > [tab] Before
> >
> > ```ts Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import { Client } from "langsmith";
> >
> > const client = new Client();
> > let threadId = "<thread-id>";
> > for await (const run of client.readThread({
> >   threadId,
> >   projectName: "default",
> >   select: ["id", "total_tokens", "total_cost"],
> > })) {
> >   console.log(run.id, run.total_tokens, run.total_cost);
> > }
> > ```
>
> > [tab] After
> >
> > ```ts After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import { Client } from "langsmith";
> >
> > const client = new Client();
> > const project = await client.readProject({ projectName: "default" });
> > let threadId = "<thread-id>";
> > for await (const trace of client.threads.listTraces(threadId, {
> >   project_id: project.id,
> >   selects: ["TRACE_ID", "TOTAL_TOKENS", "TOTAL_COST"],
> > })) {
> >   console.log(trace.trace_id, trace.total_tokens, trace.total_cost);
> > }
> > ```

> [tab] Java
>
> > [!NOTE]
> >
> > The Before example omits `total_cost` here. Selecting it on the legacy `RunSchema` type triggers a known deserialization bug in the current Java binding (it expects a string, the API returns a number).
>
> > [tab] Before
> >
> > ```kotlin Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> >
> > import com.langchain.smith.client.LangsmithClient
> > import com.langchain.smith.client.okhttp.LangsmithOkHttpClient
> > import com.langchain.smith.models.runs.RunQueryParams
> > import com.langchain.smith.models.sessions.SessionListParams
> > import kotlin.jvm.optionals.getOrNull
> >
> > val client: LangsmithClient = LangsmithOkHttpClient.fromEnv()
> >
> > val project = client.sessions().list(
> >     SessionListParams.builder().name("default").limit(1L).build()
> > ).items().first()
> >
> > var threadId = "<thread-id>"
> >
> > // Note: selecting total_cost here triggers a known deserialization bug in the
> > // v1 Java binding (RunSchema.totalCost() expects a string, the API returns a
> > // number) — omitted to keep this example runnable; see the migration notes.
> > val runs = client.runs().query(
> >     RunQueryParams.builder()
> >         .addSession(project.id())
> >         .isRoot(true)
> >         .filter("eq(thread_id, \"$threadId\")")
> >         .addSelect(RunQueryParams.Select.ID)
> >         .addSelect(RunQueryParams.Select.TOTAL_TOKENS)
> >         .build()
> > ).runs()
> > for (run in runs) {
> >     println("${run.id()} ${run.totalTokens().getOrNull()}")
> > }
> > ```
>
> > [tab] After
> >
> > ```kotlin After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> >
> > import com.langchain.smith.client.LangsmithClient
> > import com.langchain.smith.client.okhttp.LangsmithOkHttpClient
> > import com.langchain.smith.models.sessions.SessionListParams
> > import com.langchain.smith.models.threads.ThreadListTracesParams
> > import kotlin.jvm.optionals.getOrNull
> >
> > val client: LangsmithClient = LangsmithOkHttpClient.fromEnv()
> >
> > val project = client.sessions().list(
> >     SessionListParams.builder().name("default").limit(1L).build()
> > ).items().first()
> >
> > var threadId = "<thread-id>"
> >
> > val traces = client.threads().listTraces(
> >     threadId,
> >     ThreadListTracesParams.builder()
> >         .projectId(project.id())
> >         .addSelect(ThreadListTracesParams.Select.TRACE_ID)
> >         .addSelect(ThreadListTracesParams.Select.TOTAL_TOKENS)
> >         .addSelect(ThreadListTracesParams.Select.TOTAL_COST)
> >         .build()
> > ).items()
> > for (trace in traces) {
> >     println("${trace.traceId().get()} ${trace.totalTokens().getOrNull()} ${trace.totalCost().getOrNull()}")
> > }
> > ```

> [tab] Go
>
> > [tab] Before
> >
> > ```go Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > package main
> >
> > import (
> > 	"context"
> > 	"fmt"
> > 	"time"
> >
> > 	"github.com/langchain-ai/langsmith-go"
> > )
> >
> > func main() {
> > 	ctx := context.Background()
> > 	client := langsmith.NewClient()
> >
> > 	sessions, err := client.Sessions.List(ctx, langsmith.SessionListParams{
> > 		Name:  langsmith.F("default"),
> > 		Limit: langsmith.F(int64(1)),
> > 	})
> > 	if err != nil {
> > 		panic(err.Error())
> > 	}
> > 	projectID := sessions.Items[0].ID
> > 	threadID := "<thread-id>"
> >
> > 	runs, err := client.Runs.Query(ctx, langsmith.RunQueryParams{
> > 		Session: langsmith.F([]string{projectID}),
> > 		IsRoot:  langsmith.F(true),
> > 		Filter:  langsmith.F(fmt.Sprintf(`eq(thread_id, "%s")`, threadID)),
> > 		Select: langsmith.F([]langsmith.RunQueryParamsSelect{
> > 			langsmith.RunQueryParamsSelectID,
> > 			langsmith.RunQueryParamsSelectTotalTokens,
> > 			langsmith.RunQueryParamsSelectTotalCost,
> > 		}),
> > 	})
> > 	if err != nil {
> > 		panic(err.Error())
> > 	}
> > 	for _, run := range runs.Runs {
> > 		fmt.Println(run.ID, run.TotalTokens, run.TotalCost)
> > 	}
> > }
> > ```
>
> > [tab] After
> >
> > ```go After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > package main
> >
> > import (
> > 	"context"
> > 	"fmt"
> > 	"time"
> >
> > 	"github.com/langchain-ai/langsmith-go"
> > )
> >
> > func main() {
> > 	ctx := context.Background()
> > 	client := langsmith.NewClient()
> >
> > 	sessions, err := client.Sessions.List(ctx, langsmith.SessionListParams{
> > 		Name:  langsmith.F("default"),
> > 		Limit: langsmith.F(int64(1)),
> > 	})
> > 	if err != nil {
> > 		panic(err.Error())
> > 	}
> > 	projectID := sessions.Items[0].ID
> > 	threadID := "<thread-id>"
> >
> > 	iter := client.Threads.ListTracesAutoPaging(ctx, threadID, langsmith.ThreadListTracesParams{
> > 		ProjectID: langsmith.F(projectID),
> > 		Selects: langsmith.F([]langsmith.ThreadListTracesParamsSelect{
> > 			langsmith.ThreadListTracesParamsSelectTraceID,
> > 			langsmith.ThreadListTracesParamsSelectTotalTokens,
> > 			langsmith.ThreadListTracesParamsSelectTotalCost,
> > 		}),
> > 	})
> > 	for iter.Next() {
> > 		trace := iter.Current()
> > 		fmt.Println(trace.TraceID, trace.TotalTokens, trace.TotalCost)
> > 	}
> > 	if err := iter.Err(); err != nil {
> > 		panic(err.Error())
> > 	}
> > }
> > ```

> [tab] cURL
>
> > [tab] Before
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > PROJECT_ID=$(curl -s "https://api.smith.langchain.com/api/v1/sessions?name=default&limit=1" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" | jq -r '.[0].id')
> > THREAD_ID="<thread-id>"
> >
> > curl -s -X POST "https://api.smith.langchain.com/api/v1/runs/query" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" \
> >   -H "Content-Type: application/json" \
> >   -d "$(jq -n --arg pid "$PROJECT_ID" --arg tid "$THREAD_ID" '{"session": [$pid], "is_root": true, "filter": ("eq(thread_id, \"" + $tid + "\")"), "select": ["id", "total_tokens", "total_cost"]}')" \
> >   | jq '.runs // []'
> > ```
>
> > [tab] After
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > PROJECT_ID=$(curl -s "https://api.smith.langchain.com/api/v1/sessions?name=default&limit=1" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" | jq -r '.[0].id')
> > THREAD_ID="<thread-id>"
> >
> > curl -G "https://api.smith.langchain.com/api/v2/threads/$THREAD_ID/traces" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" \
> >   --data-urlencode "project_id=$PROJECT_ID" \
> >   --data-urlencode "selects=TRACE_ID" \
> >   --data-urlencode "selects=TOTAL_TOKENS" \
> >   --data-urlencode "selects=TOTAL_COST"
> > ```

## See also

* [Traces](Migrate%20trace%20methods%20to%20SmithDB.md)
* [Dataset experiment runs](Migrate%20dataset%20experiment%20runs%20to%20SmithDB.md)
* [Migration overview](Migrate%20to%20SmithDB-backed%20APIs.md)
* [Search conversation content with AI using the SDK](../../Debug/Viewing%20%26%20managing%20traces/Filter%20traces.md#search-with-ai-using-the-sdk)

# Migrate trace methods to SmithDB

> Migrate the LangSmith SDK trace methods to their SmithDB-backed equivalents.

These methods query traces and list the runs inside a trace. For deprecation dates, minimum SDK versions, and the agent prompt that applies to every method, see [Migrate to SmithDB-backed APIs](Migrate%20to%20SmithDB-backed%20APIs.md).

## Traces: query

Returns a list of traces (root runs) for a single tracing project. Each item carries the trace's root run plus optional trace-wide aggregates (`total_tokens`, `total_cost`, `first_token_time`) under `trace_aggregates`, so clients never have to merge by `trace_id`.

Traces are scanned within a `start_time` window: `min_start_time` defaults to 24 hours before the request, `max_start_time` defaults to the request time. Set either explicitly to widen or narrow the window.

Supports filters (`trace_filter`, `tree_filter`) and field projection (`selects`).

### Main changes

#### Method name

> [tab] Python
>
> | Before | After |
> | - | - |
> | `client.list_runs(is_root=True)` (generic) | `client.traces.query()` |
>
> > [!NOTE]
> >
> > `client.traces.query()` is now async. Call it with `await`.
>
> See the [reference](https://reference.langchain.com/python/langsmith/_openapi_client/resources/traces/TracesResource/query) for the full parameter and field list.

> [tab] TypeScript
>
> | Before | After |
> | - | - |
> | `client.listRuns({ isRoot: true })` (generic) | `client.traces.query()` |
>
> See the [reference](https://reference.langchain.com/javascript/langsmith/_openapi_client/Langsmith/Traces/query) for the full parameter and field list.

> [tab] Java
>
> | Before | After |
> | - | - |
> | `client.runs().query()` (generic, `isRoot(true)`) | `client.traces().query()` |
>
> See the [reference](https://javadoc.io/doc/com.langchain.smith/langsmith-java/latest/com/langchain/smith/services/blocking/TraceService.html) for the full parameter list.

> [tab] Go
>
> | Before | After |
> | - | - |
> | `client.Runs.Query()` (generic, `IsRoot: true`) | `client.Traces.Query()` |
>
> See the [reference](https://pkg.go.dev/github.com/langchain-ai/langsmith-go#TraceService.QueryAutoPaging) for the full parameter list.

> [tab] cURL
>
> | Before | After |
> | - | - |
> | `POST /api/v1/runs/query` (`is_root=true`) | `POST /api/v2/traces/query` |

#### Query parameters

> [tab] Python
>
> * `session` (a list of project UUIDs) becomes `project_id`, a single UUID; `traces.query` scopes to exactly one project per call.
> * `is_root` is removed: `traces.query` is always scoped to root runs implicitly.
> * The generic `filter` (evaluated against any run) has no direct equivalent; use `trace_filter` or `tree_filter` instead.
> * `trace_filter` and `tree_filter` carry over unchanged; both already existed on `list_runs`.
> * `trace_ids` is new: a fast-path restriction to a known set of trace UUIDs, more efficient at scale than an equivalent `trace_filter`.
> * `start_time` (no default) becomes `min_start_time`, which defaults to 24 hours ago when omitted.
> * `max_start_time` is new, defaulting to the request time; `list_runs`'s `end_time` filtered by a run's own end timestamp, not a scan-window bound.
> * `select` is renamed `selects`; entries route to `trace_aggregates` (`total_tokens`, `total_cost`, `first_token_time`) or `root_run` (everything else).

> [tab] TypeScript
>
> * `session` (a list of project UUIDs) becomes `project_id`, a single UUID; `traces.query` scopes to exactly one project per call.
> * `isRoot` is removed: `traces.query` is always scoped to root runs implicitly.
> * The generic `filter` (evaluated against any run) has no direct equivalent; use `trace_filter` or `tree_filter` instead.
> * `traceFilter` and `treeFilter` carry over as `trace_filter`/`tree_filter`; both already existed on `listRuns`. Note the v1 method took camelCase options (`traceFilter`); the v2 resource method takes the wire-format `snake_case` keys directly.
> * `trace_ids` is new: a fast-path restriction to a known set of trace UUIDs, more efficient at scale than an equivalent `trace_filter`.
> * `startTime` (no default) becomes `min_start_time`, which defaults to 24 hours ago when omitted.
> * `max_start_time` is new, defaulting to the request time; `listRuns`'s `endTime` filtered by a run's own end timestamp, not a scan-window bound.
> * `select` is renamed `selects`; entries route to `trace_aggregates` (`total_tokens`, `total_cost`, `first_token_time`) or `root_run` (everything else).

> [tab] Java
>
> * `session` (`List<String>` of project UUIDs) becomes `projectId`, a single UUID; `traces().query()` scopes to exactly one project per call.
> * `isRoot` is removed: `traces().query()` is always scoped to root runs implicitly.
> * The generic `filter` (evaluated against any run) has no direct equivalent; use `traceFilter` or `treeFilter` instead.
> * `traceFilter` and `treeFilter` carry over unchanged; both already existed on `RunQueryParams`.
> * `traceIds` is new: a fast-path restriction to a known set of trace UUIDs, more efficient at scale than an equivalent `traceFilter`.
> * `startTime` (no default) becomes `minStartTime`, which defaults to 24 hours ago when omitted.
> * `maxStartTime` is new, defaulting to the request time; `RunQueryParams`'s `endTime` filtered by a run's own end timestamp, not a scan-window bound.
> * `select` is renamed `selects`; entries route to `traceAggregates` (`totalTokens`, `totalCost`, `firstTokenTime`) or `rootRun` (everything else).

> [tab] Go
>
> * `Session` (`[]string` of project UUIDs) becomes `ProjectID`, a single UUID; `Traces.Query()` scopes to exactly one project per call.
> * `IsRoot` is removed: `Traces.Query()` is always scoped to root runs implicitly.
> * The generic `Filter` (evaluated against any run) has no direct equivalent; use `TraceFilter` or `TreeFilter` instead.
> * `TraceFilter` and `TreeFilter` carry over unchanged; both already existed on `RunQueryParams`.
> * `TraceIDs` is new: a fast-path restriction to a known set of trace UUIDs, more efficient at scale than an equivalent `TraceFilter`.
> * `StartTime` (no default) becomes `MinStartTime`, which defaults to 24 hours ago when omitted.
> * `MaxStartTime` is new, defaulting to the request time; `RunQueryParams`'s `EndTime` filtered by a run's own end timestamp, not a scan-window bound.
> * `Select` is renamed `Selects`; entries route to `TraceAggregates` (`TotalTokens`, `TotalCost`, `FirstTokenTime`) or `RootRun` (everything else).

> [tab] cURL
>
> * `session` (a list of project UUIDs) becomes `project_id`, a single UUID.
> * `is_root` is removed: the endpoint is always scoped to root runs implicitly.
> * The generic `filter` has no direct equivalent; use `trace_filter` or `tree_filter` instead. Both already existed on `POST /api/v1/runs/query`.
> * `trace_ids` is new: a fast-path restriction to a known set of trace UUIDs.
> * `start_time` (no default) becomes `min_start_time`, which defaults to 24 hours ago when omitted.
> * `max_start_time` is new, defaulting to the request time.
> * `select` is renamed `selects`.

#### Response fields

> [tab] Python
>
> * `root_run` carries the same `Run` shape as Runs: query (`id`, `name`, `run_type`, `status`, and so on), gated by `selects`.
> * `total_tokens`/`total_cost` move off `root_run` onto `trace_aggregates`, summed across every run in the trace instead of just the root run. `trace_aggregates` is omitted entirely from the response when no aggregate field was selected.
> * `trace_aggregates.first_token_time` is new

> [tab] TypeScript
>
> * `root_run` carries the same `Run` shape as Runs: query (`id`, `name`, `run_type`, `status`, and so on), gated by `selects`.
> * `total_tokens`/`total_cost` move off `root_run` onto `trace_aggregates`, summed across every run in the trace instead of just the root run. `trace_aggregates` is omitted entirely from the response when no aggregate field was selected.
> * `trace_aggregates.first_token_time` is new

> [tab] Java
>
> * `rootRun()` carries the same `RunSchema` shape as Runs: query (`totalTokens()`, `name()`, `runType()`, `status()`, and so on), gated by `selects`.
> * `totalTokens()`/`totalCost()` move off `rootRun()` onto `traceAggregates()`, summed across every run in the trace instead of just the root run.
> * `traceAggregates().firstTokenTime()` is new

> [tab] Go
>
> * `RootRun` carries the same `Run` shape as Runs: query, gated by `Selects`.
> * `TotalTokens`/`TotalCost` move off `RootRun` onto `TraceAggregates`, summed across every run in the trace instead of just the root run. Check for an absent `TraceAggregates` via `trace.TraceAggregates.JSON.RawJSON() == ""`, since it is a value type, not a pointer.
> * `TraceAggregates.FirstTokenTime` is new

> [tab] cURL
>
> JSON response fields use `snake_case`, matching the bullets below.
>
> * `root_run` carries the same shape as Runs: query, gated by `selects`.
> * `total_tokens`/`total_cost` move off `root_run` onto `trace_aggregates`, summed across every run in the trace instead of just the root run.
> * `trace_aggregates.first_token_time` is new

### Examples

#### List traces (root runs)

Fetch every trace (root run) in a project, replacing `list_runs(is_root=True)`.

> [tab] Python
>
> > [tab] Before
> >
> > ```python Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > from langsmith import Client
> >
> > client = Client()
> > project = client.read_project(project_name="default")
> >
> > root_runs = list(client.list_runs(project_id=project.id, is_root=True, limit=5))
> > for root_run in root_runs:
> >     print(root_run.trace_id, root_run.name)
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
> >     count = 0
> >     async for trace in client.traces.query(
> >         project_id=str(project.id),
> >         min_start_time=datetime.now(timezone.utc) - timedelta(days=30),
> >         max_start_time=datetime.now(timezone.utc),
> >         selects=["NAME"],
> >     ):
> >         print(trace.root_run.trace_id, trace.root_run.name)
> >         count += 1
> >         if count >= 5:
> >             break
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
> > const project = await client.readProject({ projectName: "default" });
> >
> > for await (const run of client.listRuns({ projectId: project.id, isRoot: true, limit: 5 })) {
> >   console.log(run.trace_id, run.name);
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
> > let count = 0;
> > for await (const trace of client.traces.query({
> >   project_id: project.id,
> >   min_start_time: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString(),
> >   max_start_time: new Date().toISOString(),
> >   selects: ["NAME"],
> > })) {
> >   console.log(trace.root_run?.trace_id, trace.root_run?.name);
> >   count += 1;
> >   if (count >= 5) break;
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
> > val rootRuns = client.runs().query(
> >     RunQueryParams.builder()
> >         .addSession(project.id())
> >         .isRoot(true)
> >         .limit(5L)
> >         .build()
> > ).runs()
> > for (run in rootRuns) {
> >     println("${run.traceId()} ${run.name()}")
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
> > import com.langchain.smith.models.runs.RunSelectField
> > import com.langchain.smith.models.sessions.SessionListParams
> > import com.langchain.smith.models.traces.TraceQueryParams
> > import kotlin.jvm.optionals.getOrNull
> >
> > val client: LangsmithClient = LangsmithOkHttpClient.fromEnv()
> >
> > val project = client.sessions().list(
> >     SessionListParams.builder().name("default").limit(1L).build()
> > ).items().first()
> >
> > val traces = client.traces().query(
> >     TraceQueryParams.builder()
> >         .projectId(project.id())
> >         .minStartTime(OffsetDateTime.now().minusMonths(1))
> >         .maxStartTime(OffsetDateTime.now())
> >         .addSelect(RunSelectField.NAME)
> >         .build()
> > ).items().take(5)
> > for (trace in traces) {
> >     println("${trace.rootRun().get().traceId().getOrNull()} ${trace.rootRun().get().name().getOrNull()}")
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
> > 	rootRuns, err := client.Runs.Query(ctx, langsmith.RunQueryParams{
> > 		Session: langsmith.F([]string{projectID}),
> > 		IsRoot:  langsmith.F(true),
> > 		Limit:   langsmith.F(int64(5)),
> > 	})
> > 	if err != nil {
> > 		panic(err.Error())
> > 	}
> > 	for _, run := range rootRuns.Runs {
> > 		fmt.Println(run.TraceID, run.Name)
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
> > 	iter := client.Traces.QueryAutoPaging(ctx, langsmith.TraceQueryParams{
> > 		ProjectID:    langsmith.F(projectID),
> > 		MinStartTime: langsmith.F(minStart),
> > 		MaxStartTime: langsmith.F(maxStart),
> > 		Selects:      langsmith.F([]langsmith.RunSelectField{langsmith.RunSelectFieldName}),
> > 	})
> > 	count := 0
> > 	for iter.Next() {
> > 		trace := iter.Current()
> > 		fmt.Println(trace.RootRun.TraceID, trace.RootRun.Name)
> > 		count++
> > 		if count >= 5 {
> > 			break
> > 		}
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
> >   -d "$(jq -n --arg pid "$PROJECT_ID" '{"session": [$pid], "is_root": true, "limit": 5}')" \
> >   | jq '(.runs // []) | map({trace_id: .trace_id, name: .name})'
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
> > curl -X POST "https://api.smith.langchain.com/api/v2/traces/query" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" \
> >   -H "Content-Type: application/json" \
> >   -d "$(jq -n --arg pid "$PROJECT_ID" --arg min "$MIN_START" --arg max "$MAX_START" '{
> >     "project_id": $pid,
> >     "min_start_time": $min,
> >     "max_start_time": $max,
> >     "page_size": 5,
> >     "selects": ["NAME"]
> >   }')" | jq '.items | map({trace_id: .root_run.trace_id, name: .root_run.name})'
> > ```

#### Get a trace's total tokens and cost

Read a trace's token and cost totals from `trace_aggregates` instead of the root run, where v1 kept them.

> [tab] Python
>
> > [tab] Before
> >
> > ```python Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > from langsmith import Client
> >
> > client = Client()
> > project = client.read_project(project_name="default")
> >
> > root_runs = list(client.list_runs(project_id=project.id, is_root=True, limit=5))
> >
> > for root_run in root_runs:
> >     print(root_run.trace_id, root_run.total_tokens, root_run.total_cost)
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
> >     count = 0
> >     async for trace in client.traces.query(
> >         project_id=str(project.id),
> >         min_start_time=datetime.now(timezone.utc) - timedelta(days=30),
> >         max_start_time=datetime.now(timezone.utc),
> >         selects=["NAME", "TOTAL_TOKENS", "TOTAL_COST"],
> >     ):
> >         count += 1
> >         if trace.trace_aggregates is not None:
> >             print(
> >                 trace.root_run.name,
> >                 trace.trace_aggregates.total_tokens,
> >                 trace.trace_aggregates.total_cost,
> >             )
> >         if count >= 5:
> >             break
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
> > const project = await client.readProject({ projectName: "default" });
> >
> > for await (const rootRun of client.listRuns({ projectId: project.id, isRoot: true, limit: 5 })) {
> >   console.log(rootRun.trace_id, rootRun.total_tokens, rootRun.total_cost);
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
> > let count = 0;
> > for await (const trace of client.traces.query({
> >   project_id: project.id,
> >   min_start_time: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString(),
> >   max_start_time: new Date().toISOString(),
> >   selects: ["NAME", "TOTAL_TOKENS", "TOTAL_COST"],
> > })) {
> >   count += 1;
> >   if (trace.trace_aggregates) {
> >     console.log(trace.root_run?.name, trace.trace_aggregates.total_tokens, trace.trace_aggregates.total_cost);
> >   }
> >   if (count >= 5) break;
> > }
> > ```

> [tab] Java
>
> > [!NOTE]
> >
> > The Before example reads `totalTokens` only. `totalCost` is omitted because reading it on the v1 `RunSchema` type triggers a known deserialization bug in the current Java binding (it expects a string, the API returns a number).
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
> >         .limit(5L)
> >         .build()
> > ).runs()
> >
> > // totalCost() is omitted here — RunSchema.totalCost() has a known
> > // deserialization bug in the v1 Java binding.
> > for (rootRun in rootRuns) {
> >     println("${rootRun.traceId()} ${rootRun.totalTokens().getOrNull()}")
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
> > import com.langchain.smith.models.runs.RunSelectField
> > import com.langchain.smith.models.sessions.SessionListParams
> > import com.langchain.smith.models.traces.TraceQueryParams
> > import kotlin.jvm.optionals.getOrNull
> >
> > val client: LangsmithClient = LangsmithOkHttpClient.fromEnv()
> >
> > val project = client.sessions().list(
> >     SessionListParams.builder().name("default").limit(1L).build()
> > ).items().first()
> >
> > val traces = client.traces().query(
> >     TraceQueryParams.builder()
> >         .projectId(project.id())
> >         .minStartTime(OffsetDateTime.now().minusMonths(1))
> >         .maxStartTime(OffsetDateTime.now())
> >         .addSelect(RunSelectField.NAME)
> >         .addSelect(RunSelectField.TOTAL_TOKENS)
> >         .addSelect(RunSelectField.TOTAL_COST)
> >         .build()
> > ).items()
> >
> > var count = 0
> > for (trace in traces) {
> >     count++
> >     val aggregates = trace.traceAggregates().getOrNull()
> >     if (aggregates != null) {
> >         println("${trace.rootRun().get().name().getOrNull()} ${aggregates.totalTokens().getOrNull()} ${aggregates.totalCost().getOrNull()}")
> >     }
> >     if (count >= 5) break
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
> > 	rootRuns, err := client.Runs.Query(ctx, langsmith.RunQueryParams{
> > 		Session: langsmith.F([]string{projectID}),
> > 		IsRoot:  langsmith.F(true),
> > 		Limit:   langsmith.F(int64(5)),
> > 	})
> > 	if err != nil {
> > 		panic(err.Error())
> > 	}
> >
> > 	for _, rootRun := range rootRuns.Runs {
> > 		fmt.Println(rootRun.TraceID, rootRun.TotalTokens, rootRun.TotalCost)
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
> > 	iter := client.Traces.QueryAutoPaging(ctx, langsmith.TraceQueryParams{
> > 		ProjectID:    langsmith.F(projectID),
> > 		MinStartTime: langsmith.F(minStart),
> > 		MaxStartTime: langsmith.F(maxStart),
> > 		Selects: langsmith.F([]langsmith.RunSelectField{
> > 			langsmith.RunSelectFieldName,
> > 			langsmith.RunSelectFieldTotalTokens,
> > 			langsmith.RunSelectFieldTotalCost,
> > 		}),
> > 	})
> > 	count := 0
> > 	for iter.Next() {
> > 		trace := iter.Current()
> > 		count++
> > 		if trace.TraceAggregates.JSON.RawJSON() != "" {
> > 			fmt.Println(trace.RootRun.Name, trace.TraceAggregates.TotalTokens, trace.TraceAggregates.TotalCost)
> > 		}
> > 		if count >= 5 {
> > 			break
> > 		}
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
> > START_TIME=$(date -u -d '-1 month' +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -v-1m +%Y-%m-%dT%H:%M:%SZ)
> > RESP=$(curl -s -X POST "https://api.smith.langchain.com/api/v1/runs/query" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" \
> >   -H "Content-Type: application/json" \
> >   -d "$(jq -n --arg pid "$PROJECT_ID" --arg start "$START_TIME" '{"session": [$pid], "is_root": true, "limit": 5, "start_time": $start}')")
> > echo "$RESP" | jq '(.runs // [])[] | {trace_id, total_tokens, total_cost}'
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
> > curl -X POST "https://api.smith.langchain.com/api/v2/traces/query" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" \
> >   -H "Content-Type: application/json" \
> >   -d "$(jq -n --arg pid "$PROJECT_ID" --arg min "$MIN_START" --arg max "$MAX_START" '{
> >     "project_id": $pid,
> >     "min_start_time": $min,
> >     "max_start_time": $max,
> >     "page_size": 5,
> >     "selects": ["NAME", "TOTAL_TOKENS", "TOTAL_COST"]
> >   }')"
> > ```

#### Find traces by status, or fetch traces by ID

Filter traces by status (for example, errored) with `trace_filter`, or skip filtering and fetch known traces directly and faster with `trace_ids`.

> [tab] Python
>
> > [tab] Before
> >
> > ```python Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > from langsmith import Client
> >
> > client = Client()
> > project = client.read_project(project_name="default")
> >
> > # v1 has no root-run-only filter concept — is_root plus a regular filter is
> > # the closest equivalent, still scanning every run to match.
> > error_traces = client.list_runs(
> >     project_id=project.id,
> >     is_root=True,
> >     filter='eq(status, "error")',
> >     limit=5,
> > )
> > for run in error_traces:
> >     print(run.trace_id)
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
> >
> >     # trace_filter is implicitly root-run-only — no is_root needed.
> >     count = 0
> >     async for trace in client.traces.query(
> >         project_id=str(project.id),
> >         min_start_time=datetime.now(timezone.utc) - timedelta(days=30),
> >         max_start_time=datetime.now(timezone.utc),
> >         trace_filter='eq(status, "error")',
> >     ):
> >         print(trace.root_run.trace_id)
> >         count += 1
> >         if count >= 5:
> >             break
> >
> >     # trace_ids is a fast-path when you already know which traces you want.
> >     trace_id = "<trace-id>"
> >     async for trace in client.traces.query(
> >         project_id=str(project.id),
> >         min_start_time=datetime.now(timezone.utc) - timedelta(days=30),
> >         max_start_time=datetime.now(timezone.utc),
> >         trace_ids=[trace_id],
> >     ):
> >         print(trace.root_run.trace_id)
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
> > const project = await client.readProject({ projectName: "default" });
> >
> > // v1 has no root-run-only filter concept — isRoot plus a regular filter is
> > // the closest equivalent, still scanning every run to match.
> > for await (const run of client.listRuns({
> >   projectId: project.id,
> >   isRoot: true,
> >   filter: 'eq(status, "error")',
> >   limit: 5,
> > })) {
> >   console.log(run.trace_id);
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
> >
> > // trace_filter is implicitly root-run-only — no is_root needed.
> > let count = 0;
> > for await (const trace of client.traces.query({
> >   project_id: project.id,
> >   min_start_time: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString(),
> >   max_start_time: new Date().toISOString(),
> >   trace_filter: 'eq(status, "error")',
> > })) {
> >   console.log(trace.root_run?.trace_id);
> >   count += 1;
> >   if (count >= 5) break;
> > }
> >
> > // trace_ids is a fast-path when you already know which traces you want.
> > let traceId = "<trace-id>";
> > for await (const trace of client.traces.query({
> >   project_id: project.id,
> >   min_start_time: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString(),
> >   max_start_time: new Date().toISOString(),
> >   trace_ids: [traceId],
> > })) {
> >   console.log(trace.root_run?.trace_id);
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
> > // v1 has no root-run-only filter concept — isRoot plus a regular filter is
> > // the closest equivalent, still scanning every run to match.
> > val runs = client.runs().query(
> >     RunQueryParams.builder()
> >         .addSession(project.id())
> >         .isRoot(true)
> >         .filter("eq(status, \"error\")")
> >         .limit(5L)
> >         .build()
> > ).runs()
> > for (run in runs) {
> >     println(run.traceId())
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
> > import com.langchain.smith.models.traces.TraceQueryParams
> >
> > val client: LangsmithClient = LangsmithOkHttpClient.fromEnv()
> >
> > val project = client.sessions().list(
> >     SessionListParams.builder().name("default").limit(1L).build()
> > ).items().first()
> >
> > val maxStart = OffsetDateTime.now()
> > val minStart = maxStart.minusMonths(1)
> >
> > // trace_filter is implicitly root-run-only — no is_root needed.
> > val errorTraces = client.traces().query(
> >     TraceQueryParams.builder()
> >         .projectId(project.id())
> >         .minStartTime(minStart)
> >         .maxStartTime(maxStart)
> >         .traceFilter("eq(status, \"error\")")
> >         .build()
> > ).items().take(5)
> > for (trace in errorTraces) {
> >     println(trace.rootRun().get().traceId().get())
> > }
> >
> > // traceIds is a fast-path when you already know which traces you want.
> > var traceId = "<trace-id>"
> > val knownTraces = client.traces().query(
> >     TraceQueryParams.builder()
> >         .projectId(project.id())
> >         .minStartTime(minStart)
> >         .maxStartTime(maxStart)
> >         .traceIds(listOf(traceId))
> >         .build()
> > ).items()
> > for (trace in knownTraces) {
> >     println(trace.rootRun().get().traceId().get())
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
> > 	// v1 has no root-run-only filter concept — IsRoot plus a regular filter is
> > 	// the closest equivalent, still scanning every run to match.
> > 	runs, err := client.Runs.Query(ctx, langsmith.RunQueryParams{
> > 		Session: langsmith.F([]string{projectID}),
> > 		IsRoot:  langsmith.F(true),
> > 		Filter:  langsmith.F(`eq(status, "error")`),
> > 		Limit:   langsmith.F(int64(5)),
> > 	})
> > 	if err != nil {
> > 		panic(err.Error())
> > 	}
> > 	for _, run := range runs.Runs {
> > 		fmt.Println(run.TraceID)
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
> > 	// trace_filter is implicitly root-run-only — no is_root needed.
> > 	iter := client.Traces.QueryAutoPaging(ctx, langsmith.TraceQueryParams{
> > 		ProjectID:    langsmith.F(projectID),
> > 		MinStartTime: langsmith.F(minStart),
> > 		MaxStartTime: langsmith.F(maxStart),
> > 		TraceFilter:  langsmith.F(`eq(status, "error")`),
> > 	})
> > 	count := 0
> > 	for iter.Next() {
> > 		trace := iter.Current()
> > 		fmt.Println(trace.RootRun.TraceID)
> > 		count++
> > 		if count >= 5 {
> > 			break
> > 		}
> > 	}
> > 	if err := iter.Err(); err != nil {
> > 		panic(err.Error())
> > 	}
> >
> > 	// trace_ids is a fast-path when you already know which traces you want.
> > 	traceID := "<trace-id>"
> > 	knownIter := client.Traces.QueryAutoPaging(ctx, langsmith.TraceQueryParams{
> > 		ProjectID:    langsmith.F(projectID),
> > 		MinStartTime: langsmith.F(minStart),
> > 		MaxStartTime: langsmith.F(maxStart),
> > 		TraceIDs:     langsmith.F([]string{traceID}),
> > 	})
> > 	for knownIter.Next() {
> > 		trace := knownIter.Current()
> > 		fmt.Println(trace.RootRun.TraceID)
> > 	}
> > 	if err := knownIter.Err(); err != nil {
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
> > # v1 has no root-run-only filter concept — is_root plus a regular filter is
> > # the closest equivalent, still scanning every run to match.
> > curl -s -X POST "https://api.smith.langchain.com/api/v1/runs/query" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" \
> >   -H "Content-Type: application/json" \
> >   -d "$(jq -n --arg pid "$PROJECT_ID" '{"session": [$pid], "is_root": true, "filter": "eq(status, \"error\")", "limit": 5}')" \
> >   | jq '(.runs // []) | map(.trace_id)'
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
> >
> > # trace_filter is implicitly root-run-only — no is_root needed.
> > curl -s -X POST "https://api.smith.langchain.com/api/v2/traces/query" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" \
> >   -H "Content-Type: application/json" \
> >   -d "$(jq -n --arg pid "$PROJECT_ID" --arg min "$MIN_START" --arg max "$MAX_START" '{
> >     "project_id": $pid,
> >     "min_start_time": $min,
> >     "max_start_time": $max,
> >     "page_size": 5,
> >     "trace_filter": "eq(status, \"error\")"
> >   }')" | jq '.items | map(.root_run.trace_id)'
> >
> > # trace_ids is a fast-path when you already know which traces you want.
> > TRACE_ID="<trace-id>"
> > curl -s -X POST "https://api.smith.langchain.com/api/v2/traces/query" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" \
> >   -H "Content-Type: application/json" \
> >   -d "$(jq -n --arg pid "$PROJECT_ID" --arg min "$MIN_START" --arg max "$MAX_START" --arg tid "$TRACE_ID" '{
> >     "project_id": $pid,
> >     "min_start_time": $min,
> >     "max_start_time": $max,
> >     "trace_ids": [$tid]
> >   }')" | jq '.items | map(.root_run.trace_id)'
> > ```

## Traces: list runs

Returns runs for a trace ID within min/max start time. Optional `filter`; repeatable `selects` to select fields to return.

### Main changes

#### Method name

> [tab] Python
>
> | Before | After |
> | - | - |
> | `client.list_runs(trace_id=...)` (generic) | `client.traces.list_runs()` |
>
> > [!NOTE]
> >
> > `client.traces.list_runs()` is now async. Call it with `await`.
>
> See the [reference](https://reference.langchain.com/python/langsmith/_openapi_client/resources/traces/TracesResource/list_runs) for the full parameter and field list.

> [tab] TypeScript
>
> | Before | After |
> | - | - |
> | `client.listRuns({ traceId })` (generic) | `client.traces.listRuns()` |
>
> See the [reference](https://reference.langchain.com/javascript/langsmith/_openapi_client/Langsmith/Traces/listRuns) for the full parameter and field list.

> [tab] Java
>
> | Before | After |
> | - | - |
> | `client.runs().query()` (generic, `.trace(traceId)`) | `client.traces().listRuns()` |
>
> See the [reference](https://javadoc.io/doc/com.langchain.smith/langsmith-java/latest/com/langchain/smith/services/blocking/TraceService.html) for the full parameter list.

> [tab] Go
>
> | Before | After |
> | - | - |
> | `client.Runs.Query()` (generic, `Trace: traceID`) | `client.Traces.ListRuns()` |
>
> See the [reference](https://pkg.go.dev/github.com/langchain-ai/langsmith-go#TraceService.ListRuns) for the full parameter list.

> [tab] cURL
>
> | Before | After |
> | - | - |
> | `POST /api/v1/runs/query` (`trace` field) | `GET /api/v2/traces/{trace_id}/runs` |

#### Query parameters

> [tab] Python
>
> * `trace_id`/`trace` moves from a query param to a path param.
> * `project_id` is new and **required** (the SmithDB partition key); `list_runs(trace_id=...)` did not need it.
> * `filter` is unchanged.
> * `min_start_time`/`max_start_time` are new. Unlike `traces.query`, neither has a default: omit both and runs are not filtered by time at all. They are individually optional but must be passed together if either is set.
> * `select` is renamed `selects`, using the same 44-value enum as `traces.query`.

> [tab] TypeScript
>
> * `traceId`/`trace` moves from a query param to a path param.
> * `project_id` is new and **required** (the SmithDB partition key); `listRuns({ traceId })` did not need it.
> * `filter` is unchanged.
> * `min_start_time`/`max_start_time` are new. Unlike `traces.query`, neither has a default: omit both and runs are not filtered by time at all. They are individually optional but must be passed together if either is set.
> * `select` is renamed `selects`, using the same 44-value enum as `traces.query`.

> [tab] Java
>
> * `traceId` moves from a query param (`.trace(traceId)`) to a positional path param.
> * `projectId` is new and **required** (the SmithDB partition key); the generic `runs().query()` did not need it.
> * `filter` is unchanged.
> * `minStartTime`/`maxStartTime` are new. Unlike `traces().query()`, neither has a default: omit both and runs are not filtered by time at all. They are individually optional but must be passed together if either is set.
> * `select` is renamed `selects` (44-value enum).

> [tab] Go
>
> * `traceID` moves from a query param (`Trace: traceID`) to a positional path param.
> * `ProjectID` is new and **required** (the SmithDB partition key); the generic `Runs.Query()` did not need it.
> * `Filter` is unchanged.
> * `MinStartTime`/`MaxStartTime` are new. Unlike `Traces.Query()`, neither has a default: omit both and runs are not filtered by time at all. They are individually optional but must be passed together if either is set.
> * `Select` is renamed `Selects`.

> [tab] cURL
>
> * `trace` moves from a body field to a path segment, `{trace_id}`.
> * `project_id` is new and **required** (the SmithDB partition key); `POST /api/v1/runs/query` did not need it.
> * `filter` is unchanged.
> * `min_start_time`/`max_start_time` are new. Unlike `traces.query`, neither has a default: omit both and runs are not filtered by time at all. They are individually optional but must be passed together if either is set.
> * `select` is renamed `selects`.

#### Response fields

> [tab] Python
>
> The response has a single `items` field: a list of `Run` objects in `start_time` order, same shape as the [Runs: query](Migrate%20run%20queries%20to%20SmithDB.md) response.

> [tab] TypeScript
>
> The response has a single `items` field: an array of `Run` objects in `start_time` order, same shape as the [Runs: query](Migrate%20run%20queries%20to%20SmithDB.md) response.

> [tab] Java
>
> The response has a single `items()` method, returning `Optional<List<Run>>`: the trace's runs in `start_time` order, same shape as the [Runs: query](Migrate%20run%20queries%20to%20SmithDB.md) response.

> [tab] Go
>
> The response has a single `Items` field, typed `[]Run`: the trace's runs in `start_time` order, same shape as the [Runs: query](Migrate%20run%20queries%20to%20SmithDB.md) response.

> [tab] cURL
>
> The JSON response has a single `items` array field: the trace's runs in `start_time` order, same shape as the [Runs: query](Migrate%20run%20queries%20to%20SmithDB.md) response.

### Examples

#### List every run in a trace

Fetch all the runs that belong to one trace, given its trace ID.

> [tab] Python
>
> > [tab] Before
> >
> > ```python Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > from langsmith import Client
> >
> > client = Client()
> > project = client.read_project(project_name="default")
> > trace_id = "<trace-id>"
> > runs = list(client.list_runs(project_id=project.id, trace_id=trace_id))
> > for run in runs:
> >     print(run.name, run.run_type, run.status)
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
> >     trace_id = "<trace-id>"
> >     response = await client.traces.list_runs(
> >         trace_id,
> >         project_id=str(project.id),
> >         selects=["NAME", "RUN_TYPE", "STATUS"],
> >     )
> >     for run in response.items:
> >         print(run.name, run.run_type, run.status)
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
> > const project = await client.readProject({ projectName: "default" });
> > let traceId = "<trace-id>";
> > const runs = [];
> > for await (const run of client.listRuns({ projectId: project.id, traceId })) {
> >   runs.push(run);
> > }
> > for (const run of runs) {
> >   console.log(run.name, run.run_type, run.status);
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
> > let traceId = "<trace-id>";
> > const response = await client.traces.listRuns(traceId, {
> >   project_id: project.id,
> >   selects: ["NAME", "RUN_TYPE", "STATUS"],
> > });
> > for (const run of response.items ?? []) {
> >   console.log(run.name, run.run_type, run.status);
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
> > var traceId = "<trace-id>"
> >
> > val runs = client.runs().query(
> >     RunQueryParams.builder()
> >         .addSession(project.id())
> >         .trace(traceId)
> >         .build()
> > ).runs()
> > for (run in runs) {
> >     println("${run.name()} ${run.runType()} ${run.status()}")
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
> > import com.langchain.smith.models.traces.TraceListRunsParams
> > import com.langchain.smith.models.traces.TraceQueryParams
> > import kotlin.jvm.optionals.getOrNull
> >
> > val client: LangsmithClient = LangsmithOkHttpClient.fromEnv()
> >
> > val project = client.sessions().list(
> >     SessionListParams.builder().name("default").limit(1L).build()
> > ).items().first()
> >
> > var traceId = "<trace-id>"
> >
> > val response = client.traces().listRuns(
> >     traceId,
> >     TraceListRunsParams.builder()
> >         .projectId(project.id())
> >         .addSelect(TraceListRunsParams.Select.NAME)
> >         .addSelect(TraceListRunsParams.Select.RUN_TYPE)
> >         .addSelect(TraceListRunsParams.Select.STATUS)
> >         .build()
> > )
> > for (run in response.items().getOrNull() ?: emptyList()) {
> >     println("${run.name().getOrNull()} ${run.runType().getOrNull()} ${run.status().getOrNull()}")
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
> > 	traceID := "<trace-id>"
> >
> > 	runs, err := client.Runs.Query(ctx, langsmith.RunQueryParams{
> > 		Session: langsmith.F([]string{projectID}),
> > 		Trace:   langsmith.F(traceID),
> > 	})
> > 	if err != nil {
> > 		panic(err.Error())
> > 	}
> > 	for _, run := range runs.Runs {
> > 		fmt.Println(run.Name, run.RunType, run.Status)
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
> > 	traceID := "<trace-id>"
> >
> > 	response, err := client.Traces.ListRuns(ctx, traceID, langsmith.TraceListRunsParams{
> > 		ProjectID: langsmith.F(projectID),
> > 		Selects: langsmith.F([]langsmith.TraceListRunsParamsSelect{
> > 			langsmith.TraceListRunsParamsSelectName,
> > 			langsmith.TraceListRunsParamsSelectRunType,
> > 			langsmith.TraceListRunsParamsSelectStatus,
> > 		}),
> > 	})
> > 	if err != nil {
> > 		panic(err.Error())
> > 	}
> > 	for _, run := range response.Items {
> > 		fmt.Println(run.Name, run.RunType, run.Status)
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
> > TRACE_ID="<trace-id>"
> >
> > curl -s -X POST "https://api.smith.langchain.com/api/v1/runs/query" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" \
> >   -H "Content-Type: application/json" \
> >   -d "$(jq -n --arg pid "$PROJECT_ID" --arg tid "$TRACE_ID" '{"session": [$pid], "trace": $tid}')" \
> >   | jq '.runs // []'
> > ```
>
> > [tab] After
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > PROJECT_ID=$(curl -s "https://api.smith.langchain.com/api/v1/sessions?name=default&limit=1" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" | jq -r '.[0].id')
> > TRACE_ID="<trace-id>"
> >
> > curl -G "https://api.smith.langchain.com/api/v2/traces/$TRACE_ID/runs" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" \
> >   --data-urlencode "project_id=$PROJECT_ID" \
> >   --data-urlencode "selects=NAME" \
> >   --data-urlencode "selects=RUN_TYPE" \
> >   --data-urlencode "selects=STATUS"
> > ```

#### Get only the LLM calls in a trace

Narrow a trace's runs down to a specific run type, for example just the LLM calls.

> [tab] Python
>
> > [tab] Before
> >
> > ```python Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > from langsmith import Client
> >
> > client = Client()
> > project = client.read_project(project_name="default")
> > trace_id = "<trace-id>"
> > llm_runs = list(
> >     client.list_runs(
> >         project_id=project.id,
> >         trace_id=trace_id,
> >         filter='eq(run_type, "llm")',
> >     )
> > )
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
> >     trace_id = "<trace-id>"
> >     response = await client.traces.list_runs(
> >         trace_id,
> >         project_id=str(project.id),
> >         filter='eq(run_type, "llm")',
> >         selects=["NAME", "STATUS"],
> >     )
> >     llm_runs = response.items
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
> > const project = await client.readProject({ projectName: "default" });
> > let traceId = "<trace-id>";
> > const llmRuns = [];
> > for await (const run of client.listRuns({
> >   projectId: project.id,
> >   traceId,
> >   filter: 'eq(run_type, "llm")',
> > })) {
> >   llmRuns.push(run);
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
> > let traceId = "<trace-id>";
> > const response = await client.traces.listRuns(traceId, {
> >   project_id: project.id,
> >   filter: 'eq(run_type, "llm")',
> >   selects: ["NAME", "STATUS"],
> > });
> > const llmRuns = response.items ?? [];
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
> > var traceId = "<trace-id>"
> >
> > client.runs().query(
> >     RunQueryParams.builder()
> >         .addSession(project.id())
> >         .trace(traceId)
> >         .filter("eq(run_type, \"llm\")")
> >         .build()
> > ).runs()
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
> > import com.langchain.smith.models.traces.TraceListRunsParams
> > import com.langchain.smith.models.traces.TraceQueryParams
> >
> > val client: LangsmithClient = LangsmithOkHttpClient.fromEnv()
> >
> > val project = client.sessions().list(
> >     SessionListParams.builder().name("default").limit(1L).build()
> > ).items().first()
> >
> > var traceId = "<trace-id>"
> >
> > client.traces().listRuns(
> >     traceId,
> >     TraceListRunsParams.builder()
> >         .projectId(project.id())
> >         .filter("eq(run_type, \"llm\")")
> >         .addSelect(TraceListRunsParams.Select.NAME)
> >         .addSelect(TraceListRunsParams.Select.STATUS)
> >         .build()
> > )
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
> > 	traceID := "<trace-id>"
> >
> > 	_, err = client.Runs.Query(ctx, langsmith.RunQueryParams{
> > 		Session: langsmith.F([]string{projectID}),
> > 		Trace:   langsmith.F(traceID),
> > 		Filter:  langsmith.F(`eq(run_type, "llm")`),
> > 	})
> > 	if err != nil {
> > 		panic(err.Error())
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
> > 	traceID := "<trace-id>"
> >
> > 	_, err = client.Traces.ListRuns(ctx, traceID, langsmith.TraceListRunsParams{
> > 		ProjectID: langsmith.F(projectID),
> > 		Filter:    langsmith.F(`eq(run_type, "llm")`),
> > 		Selects: langsmith.F([]langsmith.TraceListRunsParamsSelect{
> > 			langsmith.TraceListRunsParamsSelectName,
> > 			langsmith.TraceListRunsParamsSelectStatus,
> > 		}),
> > 	})
> > 	if err != nil {
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
> > TRACE_ID="<trace-id>"
> >
> > curl -s -X POST "https://api.smith.langchain.com/api/v1/runs/query" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" \
> >   -H "Content-Type: application/json" \
> >   -d "$(jq -n --arg pid "$PROJECT_ID" --arg tid "$TRACE_ID" '{"session": [$pid], "trace": $tid, "filter": "eq(run_type, \"llm\")"}')" \
> >   | jq '.runs // []'
> > ```
>
> > [tab] After
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > PROJECT_ID=$(curl -s "https://api.smith.langchain.com/api/v1/sessions?name=default&limit=1" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" | jq -r '.[0].id')
> > TRACE_ID="<trace-id>"
> >
> > curl -G "https://api.smith.langchain.com/api/v2/traces/$TRACE_ID/runs" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" \
> >   --data-urlencode "project_id=$PROJECT_ID" \
> >   --data-urlencode "filter=eq(run_type, \"llm\")" \
> >   --data-urlencode "selects=NAME" \
> >   --data-urlencode "selects=STATUS"
> > ```

## See also

* [Query runs](Migrate%20run%20queries%20to%20SmithDB.md)
* [Threads](Migrate%20thread%20methods%20to%20SmithDB.md)
* [Migration overview](Migrate%20to%20SmithDB-backed%20APIs.md)
* [Search conversation content with AI using the SDK](../../Debug/Viewing%20%26%20managing%20traces/Filter%20traces.md#search-with-ai-using-the-sdk)

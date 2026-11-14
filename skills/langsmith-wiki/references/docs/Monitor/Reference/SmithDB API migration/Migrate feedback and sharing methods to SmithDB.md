# Migrate feedback and sharing methods to SmithDB

> Migrate the LangSmith SDK feedback, annotation queue, and public run methods to their SmithDB-backed equivalents.

These methods add runs to annotation queues and read them back, share runs publicly, and create feedback. For deprecation dates, minimum SDK versions, and the agent prompt that applies to every method, see [Migrate to SmithDB-backed APIs](Migrate%20to%20SmithDB-backed%20APIs.md).

## Annotation queues: add runs

Add runs to an annotation queue. The legacy `POST /api/v1/annotation-queues/{queue_id}/runs` and `POST /api/v1/annotation-queues/{queue_id}/runs/by-key` endpoints are both deprecated. Use the annotation queue items API instead: each run is one `RUN` item with its ID plus the `project_id` (project UUID) and `start_time` lookup keys, so the run can be located directly instead of scanned for.

> [!NOTE]
>
> In Python and TypeScript, the items API is on the new client resources (`client.annotation_queues.items` / `client.annotationQueues.items`), so the [Exceptions](Migrate%20to%20SmithDB-backed%20APIs.md#exceptions) table applies. On self-hosted, the items endpoints need LangSmith v0.16.14 or later.

### Main changes

#### Method name

> [tab] Python
>
> | Before | After |
> | - | - |
> | `client.add_runs_to_annotation_queue()` | `client.annotation_queues.items.create()` (async) |

> [tab] TypeScript
>
> | Before | After |
> | - | - |
> | `client.addRunsToAnnotationQueue()` | `client.annotationQueues.items.create()` |

> [tab] Java
>
> | Before | After |
> | - | - |
> | `client.annotationQueues().runs().create()` | `client.annotationQueues().items().create()` |

> [tab] Go
>
> | Before | After |
> | - | - |
> | `client.AnnotationQueues.Runs.New()` | `client.AnnotationQueues.Items.New()` |
>
> See the [reference](https://pkg.go.dev/github.com/langchain-ai/langsmith-go#AnnotationQueueItemService.New) for the full parameter list.

> [tab] cURL
>
> | Before | After |
> | - | - |
> | `POST /api/v1/annotation-queues/{queue_id}/runs` | `POST /api/v1/platform/annotation-queues/{queue_id}/items` |

#### Inputs

The request takes a list of items (up to 100 per call) instead of a list of run IDs. Each run becomes one item:

| Field | Value |
| - | - |
| `item_type` | `RUN` |
| `run_id` | The run ID |
| `project_id` | The run's project UUID (`project_id` on a run from `runs.query`; `session_id` is also accepted as an alias) |
| `start_time` | The run's start time (RFC3339) |

`extend_trace_retention` is unchanged. It stays an optional query parameter and defaults to `false`. When omitted, adding runs does not change their retention. Set it to `true` to upgrade the traces of added runs from base to extended retention, as described in [Data retention auto-upgrades](../../Trace/Configuration%20%26%20troubleshooting/Usage%20and%20billing.md#data-retention-auto-upgrades). Thread items are not upgraded.

> [tab] Python
>
> | Before | After |
> | - | - |
> | `run_ids=[...]` or `runs=[RunKey, ...]` | `items=[{"item_type": "RUN", "run_id", "project_id", "start_time"}, ...]` |

> [tab] TypeScript
>
> | Before | After |
> | - | - |
> | `string[]` or `RunKey[]` (second argument) | `{ items: [{ item_type: "RUN", run_id, project_id, start_time }] }` |

> [tab] Java
>
> | Before (`RunCreateParams`) | After (`ItemCreateParams`) |
> | - | - |
> | `.bodyOfRunsUuidArray(List<String>)` | `.addItem(ItemCreateParams.Item)` with `itemType(RUN)`, `runId`, `projectId`, `startTime` |
> | `.queueId(String)` | `.queueId(String)` |

> [tab] Go
>
> | Before (`AnnotationQueueRunNewParams`) | After (`AnnotationQueueItemNewParams`) |
> | - | - |
> | `Body: AnnotationQueueRunNewParamsBodyRunsUuidArray` | `Items: []AnnotationQueueItemNewParamsItem` with `ItemType`, `RunID`, `ProjectID`, `StartTime` |

> [tab] cURL
>
> | Before (body) | After (body) |
> | - | - |
> | `["<run-id>", ...]` | `{"items": [{"item_type": "RUN", "run_id", "project_id", "start_time"}]}` |

#### Response

The items API returns `{"items": [...]}`, one created queue item per input (`id`, `queue_id`, `item_type`, `run_id`, `project_id`, `start_time`, `added_at`, `last_reviewed_time`). Use the item `id` with the other items endpoints (update, delete, status). The legacy Python and TypeScript methods returned nothing.

### Examples

#### Add runs to a queue

> [tab] Python
>
> Build one `RUN` item per run from the run objects you already have.
>
> > [tab] Before
> >
> > ```python Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > from langsmith import Client
> >
> > client = Client()
> > queue_id = "<queue-id>"
> > runs = list(client.list_runs(project_name="default", limit=5))
> > client.add_runs_to_annotation_queue(queue_id, run_ids=[run.id for run in runs])
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
> >     queue_id = "<queue-id>"
> >     project_id = "<project-id>"
> >     page = await client.runs.query(
> >         project_ids=[project_id],
> >         min_start_time=datetime.now(timezone.utc) - timedelta(days=30),
> >         selects=["ID", "PROJECT_ID", "START_TIME"],
> >         page_size=5,
> >     )
> >     runs = page.items
> >     await client.annotation_queues.items.create(
> >         queue_id,
> >         items=[
> >             {
> >                 "item_type": "RUN",
> >                 "run_id": str(run.id),
> >                 "project_id": str(run.project_id),
> >                 "start_time": run.start_time.isoformat(),
> >             }
> >             for run in runs
> >         ],
> >     )
> >
> >
> > asyncio.run(main())
> > ```

> [tab] TypeScript
>
> Build one `RUN` item per run from the run objects you already have.
>
> > [tab] Before
> >
> > ```ts Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import { uuid7 } from "langsmith";
> > import { Client } from "langsmith";
> >
> > const client = new Client();
> > let queueId = "<queue-id>";
> > const runs = [];
> > for await (const run of client.listRuns({ projectName: "default", limit: 5 })) {
> >   runs.push(run);
> > }
> > await client.addRunsToAnnotationQueue(
> >   queueId,
> >   runs.map((run) => run.id),
> > );
> > ```
>
> > [tab] After
> >
> > ```ts After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import { Client } from "langsmith";
> >
> > const client = new Client();
> > let queueId = "<queue-id>";
> > let projectId = "<project-id>";
> > const page = await client.runs.query({
> >   project_ids: [projectId],
> >   min_start_time: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString(),
> >   selects: ["ID", "PROJECT_ID", "START_TIME"],
> >   page_size: 5,
> > });
> > const runs = page.items ?? [];
> > await client.annotationQueues.items.create(queueId, {
> >   items: runs.map((run) => ({
> >     item_type: "RUN" as const,
> >     run_id: run.id,
> >     project_id: run.project_id!,
> >     start_time: run.start_time!,
> >   })),
> > });
> > ```

> [tab] Java
>
> Add one `ItemCreateParams.Item` per run.
>
> > [tab] Before
> >
> > ```kotlin Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import com.langchain.smith.client.LangsmithClient
> > import com.langchain.smith.client.okhttp.LangsmithOkHttpClient
> > import com.langchain.smith.models.annotationqueues.AnnotationQueueAnnotationQueuesParams
> > import com.langchain.smith.models.annotationqueues.runs.RunCreateParams
> > import com.langchain.smith.models.runs.RunQueryParams
> > import com.langchain.smith.models.sessions.SessionListParams
> >
> > val client: LangsmithClient = LangsmithOkHttpClient.fromEnv()
> >
> > var queueId = "<queue-id>"
> > var projectId = "<project-id>"
> > val runs = client.runs().query(
> >     RunQueryParams.builder().session(listOf(projectId)).limit(5L).build()
> > ).items()
> >
> > client.annotationQueues().runs().create(
> >     RunCreateParams.builder()
> >         .queueId(queueId)
> >         .bodyOfRunsUuidArray(runs.map { it.id() })
> >         .build()
> > )
> > ```
>
> > [tab] After
> >
> > ```kotlin After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import com.langchain.smith.client.LangsmithClient
> > import com.langchain.smith.client.okhttp.LangsmithOkHttpClient
> > import com.langchain.smith.models.annotationqueues.AnnotationQueueAnnotationQueuesParams
> > import com.langchain.smith.models.annotationqueues.items.ItemCreateParams
> > import com.langchain.smith.models.runs.RunQueryV2Params
> > import com.langchain.smith.models.runs.RunSelectField
> > import com.langchain.smith.models.sessions.SessionListParams
> > import java.time.OffsetDateTime
> >
> > val client: LangsmithClient = LangsmithOkHttpClient.fromEnv()
> >
> > var queueId = "<queue-id>"
> > var projectId = "<project-id>"
> > val runs = client.runs().queryV2(
> >     RunQueryV2Params.builder()
> >         .addProjectId(projectId)
> >         .minStartTime(OffsetDateTime.now().minusDays(30))
> >         .addSelect(RunSelectField.ID)
> >         .addSelect(RunSelectField.PROJECT_ID)
> >         .addSelect(RunSelectField.START_TIME)
> >         .pageSize(5L)
> >         .build()
> > ).items()
> >
> > val params = ItemCreateParams.builder().queueId(queueId)
> > for (run in runs) {
> >     params.addItem(
> >         ItemCreateParams.Item.builder()
> >             .itemType(ItemCreateParams.Item.ItemType.RUN)
> >             .runId(run.id().get())
> >             .projectId(run.projectId().get())
> >             .startTime(run.startTime().get())
> >             .build()
> >     )
> > }
> > client.annotationQueues().items().create(params.build())
> > ```

> [tab] Go
>
> Add one `AnnotationQueueItemNewParamsItem` per run.
>
> > [tab] Before
> >
> > ```go Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > package main
> >
> > import (
> > 	"context"
> > 	"time"
> >
> > 	"github.com/langchain-ai/langsmith-go"
> > )
> >
> > ctx := context.Background()
> > client := langsmith.NewClient()
> >
> > queueID := "<queue-id>"
> > projectID := "<project-id>"
> > found, err := client.Runs.Query(ctx, langsmith.RunQueryParams{
> > 	Session: langsmith.F([]string{projectID}),
> > 	Limit:   langsmith.F(int64(5)),
> > })
> > runIDs := make([]string, len(found.Runs))
> > for i, run := range found.Runs {
> > 	runIDs[i] = run.ID
> > }
> > _, err = client.AnnotationQueues.Runs.New(ctx, queueID, langsmith.AnnotationQueueRunNewParams{
> > 	Body: langsmith.AnnotationQueueRunNewParamsBodyRunsUuidArray(runIDs),
> > })
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
> > ctx := context.Background()
> > client := langsmith.NewClient()
> >
> > queueID := "<queue-id>"
> > projectID := "<project-id>"
> > found, err := client.Runs.QueryV2(ctx, langsmith.RunQueryV2Params{
> > 	ProjectIDs:   langsmith.F([]string{projectID}),
> > 	MinStartTime: langsmith.F(time.Now().UTC().AddDate(0, 0, -30)),
> > 	Selects: langsmith.F([]langsmith.RunSelectField{
> > 		langsmith.RunSelectFieldID,
> > 		langsmith.RunSelectFieldProjectID,
> > 		langsmith.RunSelectFieldStartTime,
> > 	}),
> > 	PageSize: langsmith.F(int64(5)),
> > })
> > items := make([]langsmith.AnnotationQueueItemNewParamsItem, len(found.Items))
> > for i, run := range found.Items {
> > 	items[i] = langsmith.AnnotationQueueItemNewParamsItem{
> > 		ItemType:  langsmith.F(langsmith.AnnotationQueueItemNewParamsItemsItemTypeRun),
> > 		RunID:     langsmith.F(run.ID),
> > 		ProjectID: langsmith.F(run.ProjectID),
> > 		StartTime: langsmith.F(run.StartTime),
> > 	}
> > }
> > _, err = client.AnnotationQueues.Items.New(ctx, queueID, langsmith.AnnotationQueueItemNewParams{
> > 	Items: langsmith.F(items),
> > })
> > ```

> [tab] cURL
>
> `POST /runs` takes an array of run-ID strings. `POST /items` takes an `items` array of objects.
>
> > [tab] Before
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > QUEUE_ID="<queue-id>"
> > RUN_ID="<run-id>"
> >
> > curl -X POST "https://api.smith.langchain.com/api/v1/annotation-queues/$QUEUE_ID/runs" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" \
> >   -H "Content-Type: application/json" \
> >   -d "[\"$RUN_ID\"]"
> > ```
>
> > [tab] After
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > QUEUE_ID="<queue-id>"
> > RUN_ID="<run-id>"
> > PROJECT_ID="<project-id>"
> > START_TIME="2026-06-01T12:00:00Z"
> >
> > curl -X POST "https://api.smith.langchain.com/api/v1/platform/annotation-queues/$QUEUE_ID/items" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" \
> >   -H "Content-Type: application/json" \
> >   -d "{\"items\": [{\"item_type\": \"RUN\", \"run_id\": \"$RUN_ID\", \"project_id\": \"$PROJECT_ID\", \"start_time\": \"$START_TIME\"}]}"
> > ```

## Annotation queues: read runs

List and count the runs in an annotation queue. The legacy `GET /api/v1/annotation-queues/{queue_id}/runs`, `GET /api/v1/annotation-queues/{queue_id}/run/{index}`, and `GET /api/v1/annotation-queues/{queue_id}/size` endpoints are deprecated, as are `total_size` and `total_archived`. Use the annotation queue items API instead: list or count the items in one review status, then fetch each run with the lookup keys on its item.

> [!NOTE]
>
> In Python and TypeScript, the items API is on the new client resources (`client.annotation_queues.items` / `client.annotationQueues.items`). The [Exceptions](Migrate%20to%20SmithDB-backed%20APIs.md#exceptions) table applies to them. On self-hosted, listing items needs LangSmith v0.16.17 or later. `retrieve_placement` needs v0.16.20 or later. The count endpoint needs v0.17.1 or later. No 0.16 release includes it.

### Main changes

#### Method name

> [tab] Python
>
> | Before | After |
> | - | - |
> | `client.list_runs_from_annotation_queue()` | `client.annotation_queues.items.list()` (async iterator) |
> | `client.get_run_from_annotation_queue()` | `client.annotation_queues.items.list()` |
> | None | `client.annotation_queues.items.retrieve_count()` (async) |

> [tab] TypeScript
>
> | Before | After |
> | - | - |
> | `client.listRunsFromAnnotationQueue()` | `client.annotationQueues.items.list()` |
> | `client.getRunFromAnnotationQueue()` | `client.annotationQueues.items.list()` |
> | `client.getSizeFromAnnotationQueue()` | `client.annotationQueues.items.retrieveCount()` |

> [tab] Java
>
> | Before | After |
> | - | - |
> | `client.annotationQueues().runs().list()` | `client.annotationQueues().items().list()` |
> | `client.annotationQueues().retrieveRun()` | `client.annotationQueues().items().list()` |
> | `client.annotationQueues().retrieveSize()`, `retrieveTotalSize()`, `retrieveTotalArchived()` | `client.annotationQueues().items().retrieveCount()` |

> [tab] Go
>
> | Before | After |
> | - | - |
> | `client.AnnotationQueues.Runs.List()` | `client.AnnotationQueues.Items.List()` or `ListAutoPaging()` |
> | `client.AnnotationQueues.GetRun()` | `client.AnnotationQueues.Items.List()` |
> | `client.AnnotationQueues.GetSize()`, `GetTotalSize()`, `GetTotalArchived()` | `client.AnnotationQueues.Items.GetCount()` |

> [tab] cURL
>
> | Before | After |
> | - | - |
> | `GET /api/v1/annotation-queues/{queue_id}/runs` | `GET /api/v1/platform/annotation-queues/{queue_id}/items` |
> | `GET /api/v1/annotation-queues/{queue_id}/run/{index}` | `GET /api/v1/platform/annotation-queues/{queue_id}/items` |
> | `GET /api/v1/annotation-queues/{queue_id}/size`, `/total_size`, `/total_archived` | `GET /api/v1/platform/annotation-queues/{queue_id}/items/count` |

There is no lookup by index. To read the run at a position, page through the list with `page_size` and the cursor from the previous page. To find an item's position, use `retrieve_placement`. The method is `retrievePlacement` in TypeScript and Java, `GetPlacement` in Go, and `GET /api/v1/platform/annotation-queues/{queue_id}/items/{item_id}/placement` in cURL. It returns the item's review status (`section`), zero-based `position`, and a `cursor` for listing from that point. The cursor counts runs and threads together and ignores start-time bounds. Pass it only to a list request without `item_type`, `min_start_time`, or `max_start_time`.

#### Review status

The items API requires a `status`. The legacy endpoints defaulted to `needs_my_review` when you omitted it.

| Before | After | Contains |
| - | - | - |
| `needs_my_review` (or omitted) | `needs_my_review` | Items you have not reviewed yet |
| `needs_others_review` | `needs_others_review` | Items you reviewed that still need other reviewers |
| `completed` | `archived` | Items that met the queue's review requirements |

The legacy `archived=true` flag on the list endpoint also maps to `archived`. The items API does not accept `completed`.

`needs_my_review` and `needs_others_review` are relative to the caller. A personal access token returns its owner's split. A service key returns the split for its service account, not for any human reviewer. Together they cover every item still in the queue.

For counts, the legacy totals map to:

| Before | `status` on the count endpoint |
| - | - |
| `size` | `needs_my_review` or `needs_others_review` |
| `total_size` | `all` |
| `total_archived` | `archived` (`start_time` and `end_time` still filter on when the item was archived) |

#### Item type

The items API returns runs and threads. Pass `item_type` as `RUN` to list only runs, as the legacy endpoints did. The count endpoint has no `item_type` filter, so counts include thread items.

#### Response

Each item holds the run's lookup keys (`run_id`, `project_id`, `start_time`) and queue metadata (`id`, `added_at`, `last_reviewed_time`, `reserved_by`, `completed_by`), not the run itself. To read a run's name, inputs, or outputs, pass those keys to the [run retrieve method](Migrate%20run%20retrieval%20to%20SmithDB.md#runs-retrieve). The list returns an opaque `next_cursor` for pagination. The SDKs iterate across pages for you.

The count endpoint returns `{"count": <n>}` instead of `{"size": <n>}`.

### Examples

#### List and count runs waiting for review

> [tab] Python
>
> The legacy Python client had no size method, so the count is new.
>
> > [tab] Before
> >
> > ```python Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > from langsmith import Client
> >
> > client = Client()
> > queue_id = "<queue-id>"
> > runs = list(
> >     client.list_runs_from_annotation_queue(queue_id, status="needs_my_review")
> > )
> > for run in runs:
> >     print(run.name)
> >
> > first_run = client.get_run_from_annotation_queue(queue_id, index=0)
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
> >     queue_id = "<queue-id>"
> >     count = await client.annotation_queues.items.retrieve_count(
> >         queue_id, status="needs_my_review"
> >     )
> >     print(count.count)
> >
> >     # Items carry the run's lookup keys, not its contents.
> >     async for item in client.annotation_queues.items.list(
> >         queue_id, status="needs_my_review", item_type="RUN"
> >     ):
> >         run = await client.runs.retrieve_v2(
> >             item.run_id,
> >             project_id=item.project_id,
> >             start_time=item.start_time,
> >             selects=["NAME", "STATUS", "INPUTS", "OUTPUTS"],
> >         )
> >         print(run.name, run.status)
> >
> >
> > asyncio.run(main())
> > ```

> [tab] TypeScript
>
> `items.list()` returns an async iterable that fetches further pages as you loop.
>
> > [tab] Before
> >
> > ```ts Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import { Client } from "langsmith";
> >
> > const client = new Client();
> > let queueId = "<queue-id>";
> > const { size } = await client.getSizeFromAnnotationQueue(queueId);
> > console.log(size);
> >
> > for await (const run of client.listRunsFromAnnotationQueue(queueId, {
> >   status: "needs_my_review",
> > })) {
> >   console.log(run.name, run.status);
> > }
> >
> > const firstRun = await client.getRunFromAnnotationQueue(queueId, 0);
> > ```
>
> > [tab] After
> >
> > ```ts After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import { Client } from "langsmith";
> >
> > const client = new Client();
> > let queueId = "<queue-id>";
> > const { count } = await client.annotationQueues.items.retrieveCount(queueId, {
> >   status: "needs_my_review",
> > });
> > console.log(count);
> >
> > // Items carry the run's lookup keys, not its contents.
> > for await (const item of client.annotationQueues.items.list(queueId, {
> >   status: "needs_my_review",
> >   item_type: "RUN",
> > })) {
> >   const run = await client.runs.retrieveV2(item.run_id!, {
> >     project_id: item.project_id!,
> >     start_time: item.start_time,
> >     selects: ["NAME", "STATUS", "INPUTS", "OUTPUTS"],
> >   });
> >   console.log(run.name, run.status);
> > }
> > ```

> [tab] Java
>
> `autoPager()` fetches further pages as you loop.
>
> > [tab] Before
> >
> > ```kotlin Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import com.langchain.smith.client.LangsmithClient
> > import com.langchain.smith.client.okhttp.LangsmithOkHttpClient
> > import com.langchain.smith.models.annotationqueues.AnnotationQueueRetrieveRunParams
> > import com.langchain.smith.models.annotationqueues.AnnotationQueueRetrieveSizeParams
> > import com.langchain.smith.models.annotationqueues.runs.RunListParams
> >
> > val client: LangsmithClient = LangsmithOkHttpClient.fromEnv()
> >
> > var queueId = "<queue-id>"
> > val size = client.annotationQueues().retrieveSize(
> >     queueId,
> >     AnnotationQueueRetrieveSizeParams.builder()
> >         .status(AnnotationQueueRetrieveSizeParams.Status.NEEDS_MY_REVIEW)
> >         .build()
> > ).size()
> > println(size)
> >
> > val runs = client.annotationQueues().runs().list(
> >     queueId,
> >     RunListParams.builder().status(RunListParams.Status.NEEDS_MY_REVIEW).build()
> > )
> > for (run in runs) {
> >     println("${run.name()} ${run.status()}")
> > }
> >
> > val firstRun = client.annotationQueues().retrieveRun(
> >     0L,
> >     AnnotationQueueRetrieveRunParams.builder().queueId(queueId).build()
> > )
> > ```
>
> > [tab] After
> >
> > ```kotlin After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import com.langchain.smith.client.LangsmithClient
> > import com.langchain.smith.client.okhttp.LangsmithOkHttpClient
> > import com.langchain.smith.models.annotationqueues.items.ItemListParams
> > import com.langchain.smith.models.annotationqueues.items.ItemRetrieveCountParams
> > import com.langchain.smith.models.runs.RunRetrieveV2Params
> > import java.time.OffsetDateTime
> >
> > val client: LangsmithClient = LangsmithOkHttpClient.fromEnv()
> >
> > var queueId = "<queue-id>"
> > val count = client.annotationQueues().items().retrieveCount(
> >     queueId,
> >     ItemRetrieveCountParams.builder().status("needs_my_review").build()
> > ).count().get()
> > println(count)
> >
> > // Items carry the run's lookup keys, not its contents.
> > val page = client.annotationQueues().items().list(
> >     queueId,
> >     ItemListParams.builder()
> >         .status(ItemListParams.Status.NEEDS_MY_REVIEW)
> >         .itemType(ItemListParams.ItemType.RUN)
> >         .build()
> > )
> > for (item in page.autoPager()) {
> >     val run = client.runs().retrieveV2(
> >         item.runId().get(),
> >         RunRetrieveV2Params.builder()
> >             .projectId(item.projectId().get())
> >             .startTime(OffsetDateTime.parse(item.startTime().get()))
> >             .addSelect(RunRetrieveV2Params.Select.NAME)
> >             .addSelect(RunRetrieveV2Params.Select.STATUS)
> >             .addSelect(RunRetrieveV2Params.Select.INPUTS)
> >             .addSelect(RunRetrieveV2Params.Select.OUTPUTS)
> >             .build()
> >     )
> >     println("${run.name().orElse("")} ${run.status().map { it.toString() }.orElse("")}")
> > }
> > ```

> [tab] Go
>
> `ListAutoPaging()` fetches further pages as you loop. Item start times are RFC3339 strings, so parse them before passing them to `GetV2`.
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
> > ctx := context.Background()
> > client := langsmith.NewClient()
> >
> > queueID := "<queue-id>"
> > size, err := client.AnnotationQueues.GetSize(ctx, queueID, langsmith.AnnotationQueueGetSizeParams{
> > 	Status: langsmith.F(langsmith.AnnotationQueueGetSizeParamsStatusNeedsMyReview),
> > })
> > if err != nil {
> > 	panic(err.Error())
> > }
> > fmt.Println(size.Size)
> >
> > runs, err := client.AnnotationQueues.Runs.List(ctx, queueID, langsmith.AnnotationQueueRunListParams{
> > 	Status: langsmith.F(langsmith.AnnotationQueueRunListParamsStatusNeedsMyReview),
> > })
> > if err != nil {
> > 	panic(err.Error())
> > }
> > for _, run := range *runs {
> > 	fmt.Println(run.Name)
> > }
> >
> > firstRun, err := client.AnnotationQueues.GetRun(ctx, queueID, 0, langsmith.AnnotationQueueGetRunParams{})
> > if err != nil {
> > 	panic(err.Error())
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
> > ctx := context.Background()
> > client := langsmith.NewClient()
> >
> > queueID := "<queue-id>"
> > count, err := client.AnnotationQueues.Items.GetCount(ctx, queueID, langsmith.AnnotationQueueItemGetCountParams{
> > 	Status: langsmith.F("needs_my_review"),
> > })
> > if err != nil {
> > 	panic(err.Error())
> > }
> > fmt.Println(count.Count)
> >
> > // Items carry the run's lookup keys, not its contents.
> > iter := client.AnnotationQueues.Items.ListAutoPaging(ctx, queueID, langsmith.AnnotationQueueItemListParams{
> > 	Status:   langsmith.F(langsmith.AnnotationQueueItemListParamsStatusNeedsMyReview),
> > 	ItemType: langsmith.F(langsmith.AnnotationQueueItemListParamsItemTypeRun),
> > })
> > for iter.Next() {
> > 	item := iter.Current()
> > 	startTime, err := time.Parse(time.RFC3339Nano, item.StartTime)
> > 	if err != nil {
> > 		panic(err.Error())
> > 	}
> > 	run, err := client.Runs.GetV2(ctx, item.RunID, langsmith.RunGetV2Params{
> > 		ProjectID: langsmith.F(item.ProjectID),
> > 		StartTime: langsmith.F(startTime),
> > 		Selects: langsmith.F([]langsmith.RunGetV2ParamsSelect{
> > 			langsmith.RunGetV2ParamsSelectName,
> > 			langsmith.RunGetV2ParamsSelectStatus,
> > 			langsmith.RunGetV2ParamsSelectInputs,
> > 			langsmith.RunGetV2ParamsSelectOutputs,
> > 		}),
> > 	})
> > 	if err != nil {
> > 		panic(err.Error())
> > 	}
> > 	fmt.Println(run.Name, run.Status)
> > }
> > if err := iter.Err(); err != nil {
> > 	panic(err.Error())
> > }
> > ```

> [tab] cURL
>
> `GET /runs` returns an array of full runs. `GET /items` returns `{"items": [...], "next_cursor": ...}`, and each run is a separate `GET /api/v2/runs/{run_id}` call.
>
> > [tab] Before
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > QUEUE_ID="<queue-id>"
> >
> > SIZE=$(curl -s "https://api.smith.langchain.com/api/v1/annotation-queues/$QUEUE_ID/size?status=needs_my_review" \
> >   -H "x-api-key: $LANGSMITH_API_KEY")
> >
> > RUNS=$(curl -s "https://api.smith.langchain.com/api/v1/annotation-queues/$QUEUE_ID/runs?status=needs_my_review" \
> >   -H "x-api-key: $LANGSMITH_API_KEY")
> > echo "$RUNS" | jq -r '.[] | "\(.name) \(.status)"'
> >
> > FIRST_RUN=$(curl -s "https://api.smith.langchain.com/api/v1/annotation-queues/$QUEUE_ID/run/0" \
> >   -H "x-api-key: $LANGSMITH_API_KEY")
> > ```
>
> > [tab] After
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > QUEUE_ID="<queue-id>"
> >
> > COUNT=$(curl -s "https://api.smith.langchain.com/api/v1/platform/annotation-queues/$QUEUE_ID/items/count?status=needs_my_review" \
> >   -H "x-api-key: $LANGSMITH_API_KEY")
> >
> > # Items carry the run's lookup keys, not its contents. Pass next_cursor back as
> > # ?cursor= to fetch the next page.
> > ITEMS=$(curl -s "https://api.smith.langchain.com/api/v1/platform/annotation-queues/$QUEUE_ID/items?status=needs_my_review&item_type=RUN" \
> >   -H "x-api-key: $LANGSMITH_API_KEY")
> >
> > while read -r RUN_ID PROJECT_ID START_TIME; do
> >   RUN=$(curl -s "https://api.smith.langchain.com/api/v2/runs/$RUN_ID?project_id=$PROJECT_ID&start_time=$START_TIME&selects=NAME&selects=STATUS&selects=INPUTS&selects=OUTPUTS" \
> >     -H "x-api-key: $LANGSMITH_API_KEY")
> >   echo "$RUN" | jq -r '"\(.name) \(.status)"'
> > done < <(echo "$ITEMS" | jq -r '.items[] | "\(.run_id) \(.project_id) \(.start_time)"')
> > ```

## Share and read public runs

Share a trace, remove its public access, or read the runs in a publicly shared trace. The v2 methods use explicit SmithDB coordinates and return select-driven run objects.

Public read methods do not require a LangSmith API key. Treat the share token as a secret because anyone with the token can read the shared trace.

### Main changes

#### Method names

> [tab] Python
>
> | Before | After |
> | - | - |
> | `client.share_run()` | `client.runs.share.create()` |
> | `client.unshare_run()` | `client.runs.share.delete()` |
> | `client.list_shared_runs()` | `client.public.runs.query()` |
> | `client.read_shared_run()` | `client.public.runs.retrieve()` |
> | `client.read_run_shared_link()` | `client.runs.retrieve(selects=["SHARE_URL"])` |
>
> > [!NOTE]
> >
> > The v2 resource methods are async. Call them with `await`.

> [tab] TypeScript
>
> | Before | After |
> | - | - |
> | `client.shareRun()` | `client.runs.share.create()` |
> | `client.unshareRun()` | `client.runs.share.delete()` |
> | `client.listSharedRuns()` | `client.public.runs.query()` |
> | `client.listSharedRuns({ runIds: [...] })` | `client.public.runs.retrieve()` |
> | `client.readRunSharedLink()` | `client.runs.retrieve({ selects: ["SHARE_URL"] })` |
>
> TypeScript did not have a direct equivalent of Python's `read_shared_run`. Filtered `listSharedRuns` calls migrate to the point-read method.

> [tab] Java
>
> The Java SDK has no legacy convenience methods to migrate. Use [`ShareService`](https://javadoc.io/doc/com.langchain.smith/langsmith-java/latest/com/langchain/smith/services/blocking/runs/ShareService.html) and the public [`RunService`](https://javadoc.io/doc/com.langchain.smith/langsmith-java/latest/com/langchain/smith/services/blocking/public_/RunService.html) for v2 access. Kotlin uses the Java SDK; there is no separate Kotlin reference site.

> [tab] Go
>
> The Go SDK has no legacy convenience methods to migrate. Use [`RunShareService`](https://pkg.go.dev/github.com/langchain-ai/langsmith-go#RunShareService) and [`PublicRunService`](https://pkg.go.dev/github.com/langchain-ai/langsmith-go#PublicRunService) for v2 access.

> [tab] cURL
>
> | Operation | Before | After |
> | - | - | - |
> | Share | `PUT /api/v1/runs/{run_id}/share` | `POST /api/v2/runs/{run_id}/share` |
> | Unshare | `DELETE /api/v1/runs/{run_id}/share` | `DELETE /api/v2/runs/{trace_id}/share` |
> | Query public runs | `POST /api/v1/public/{share_token}/runs/query` | `POST /api/v2/public/{share_token}/runs/query` |
> | Retrieve a public run | `GET /api/v1/public/{share_token}/run/{run_id}` | `GET /api/v2/public/{share_token}/run/{run_id}` |
> | Read share state | `GET /api/v1/runs/{run_id}/share` | `GET /api/v2/runs/{run_id}?selects=SHARE_URL` |
>
> The legacy `GET /api/v1/public/{share_token}/run` endpoint without a run ID has no direct v2 equivalent.

#### Share and unshare parameters

> [tab] Python
>
> * `runs.share.create` takes the run ID as its positional argument. Pass `session_id` (the tracing project UUID) and `trace_id` (the root trace UUID).
> * `runs.share.delete` takes the root trace ID, not an arbitrary child run ID. Pass the tracing project UUID as `session_id`.
> * `share_id` is removed. The server generates the share token.

> [tab] TypeScript
>
> * `runs.share.create` takes the run ID as its positional argument. Pass `session_id` and the root `trace_id` in the options object.
> * `runs.share.delete` takes the root trace ID and an options object containing `session_id`.
> * `shareId` is removed. The server generates the share token.

> [tab] cURL
>
> * The v2 share request body contains `session_id` and `trace_id`.
> * The v2 unshare path identifies the root trace. Its request body contains `session_id`.
> * The v2 unshare operation is idempotent and returns `204 No Content`.

Although generated parameter types may mark these coordinates as optional, provide `session_id` and `trace_id` when sharing, and provide `session_id` when unsharing. SmithDB uses these coordinates for the lookup.

#### Public read parameters

* `public.runs.query` takes the share token and a `selects` list. The token scopes the query to the complete shared trace. The legacy run-ID filter and cursor response are removed.
* `public.runs.retrieve` requires the run ID, share token, exact run `start_time`, and a `selects` list. Obtain the exact stored start time from `public.runs.query`.
* The public point read returns only selected fields. Use `ID`, `NAME`, `RUN_TYPE`, `STATUS`, and `START_TIME` for the examples below.
* To retrieve the public URL for an authenticated run, call `runs.retrieve` with `selects=["SHARE_URL"]`, then read `run.share_url`. Supplying `start_time` gives SmithDB the most efficient lookup.

Do not construct the public URL from the API origin. Retrieving `share_url` uses the deployment's configured application origin and works for both Cloud and self-hosted deployments.

#### Responses

| Operation | Before | After |
| - | - | - |
| Share | Run ID, shared trace ID, and share token | `share_token` |
| Unshare | `{"message": "Run unshared"}` | `204 No Content` |
| Query public runs | `runs` and `cursors` | `items` |
| Retrieve a public run | Full legacy run | Select-driven run object |
| Read share state | Share-state object or `null` | Run object with `share_url` when shared |

### Examples

The examples query the public trace before the point read because `public.runs.retrieve` requires the run's exact stored `start_time`.

> [tab] Python
>
> > [tab] Before
> >
> > ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > # Share a trace.
> > share_url = client.share_run(run_id)
> >
> > # Read the shared runs and one specific run.
> > runs = list(client.list_shared_runs(share_token))
> > run = client.read_shared_run(share_token, run_id=run_id)
> >
> > # Check whether the run is shared.
> > share_url = client.read_run_shared_link(run_id)
> >
> > # Remove public access.
> > client.unshare_run(run_id)
> > ```
>
> > [tab] After
> >
> > ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > PUBLIC_RUN_SELECTS = ["ID", "NAME", "RUN_TYPE", "STATUS", "START_TIME"]
> >
> > # Share a trace.
> > share = await client.runs.share.create(
> >     run_id,
> >     session_id=project_id,
> >     trace_id=trace_id,
> > )
> > if not share.share_token:
> >     raise RuntimeError("The server did not return a share token")
> > share_token = share.share_token
> >
> > # Query the public trace and use its stored start time for a point read.
> > response = await client.public.runs.query(
> >     share_token,
> >     selects=PUBLIC_RUN_SELECTS,
> > )
> > runs = response.items
> > item = next(run for run in runs if str(run.id) == run_id)
> > run = await client.public.runs.retrieve(
> >     run_id,
> >     share_token=share_token,
> >     selects=PUBLIC_RUN_SELECTS,
> >     start_time=item.start_time,
> > )
> >
> > # Retrieve the deployment-aware public URL for an authenticated run.
> > authenticated_run = await client.runs.retrieve(
> >     run_id,
> >     project_id=project_id,
> >     start_time=item.start_time,
> >     selects=["SHARE_URL"],
> > )
> > share_url = authenticated_run.share_url
> >
> > # Remove public access by root trace ID.
> > await client.runs.share.delete(trace_id, session_id=project_id)
> > ```

> [tab] TypeScript
>
> > [tab] Before
> >
> > ```typescript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > // Share a trace.
> > const shareUrl = await client.shareRun(runId);
> >
> > // Read the shared runs and one specific run.
> > const runs = await client.listSharedRuns(shareToken);
> > const [run] = await client.listSharedRuns(shareToken, {
> >   runIds: [runId],
> > });
> >
> > // Check whether the run is shared.
> > const existingShareUrl = await client.readRunSharedLink(runId);
> >
> > // Remove public access.
> > await client.unshareRun(runId);
> > ```
>
> > [tab] After
> >
> > ```typescript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > const PUBLIC_RUN_SELECTS = [
> >   "ID",
> >   "NAME",
> >   "RUN_TYPE",
> >   "STATUS",
> >   "START_TIME",
> > ] as const;
> >
> > // Share a trace.
> > const share = await client.runs.share.create(runId, {
> >   session_id: projectId,
> >   trace_id: traceId,
> > });
> > if (!share.share_token) {
> >   throw new Error("The server did not return a share token");
> > }
> > const shareToken = share.share_token;
> >
> > // Query the public trace and use its stored start time for a point read.
> > const response = await client.public.runs.query(shareToken, {
> >   selects: [...PUBLIC_RUN_SELECTS],
> > });
> > const runs = response.items ?? [];
> > const item = runs.find((candidate) => candidate.id === runId);
> > if (!item?.start_time) {
> >   throw new Error("The public run or its start_time was not found");
> > }
> > const run = await client.public.runs.retrieve(runId, {
> >   share_token: shareToken,
> >   selects: [...PUBLIC_RUN_SELECTS],
> >   start_time: item.start_time,
> > });
> >
> > // Retrieve the deployment-aware public URL for an authenticated run.
> > const authenticatedRun = await client.runs.retrieve(runId, {
> >   project_id: projectId,
> >   start_time: item.start_time,
> >   selects: ["SHARE_URL"],
> > });
> > const shareUrl = authenticatedRun.share_url;
> >
> > // Remove public access by root trace ID.
> > await client.runs.share.delete(traceId, { session_id: projectId });
> > ```

> [tab] cURL
>
> > [tab] Before
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > # Share a run.
> > curl --request PUT \
> >   "$API_URL/api/v1/runs/$RUN_ID/share" \
> >   --header "X-API-Key: $LANGSMITH_API_KEY"
> >
> > # Query the public trace and retrieve one public run.
> > curl --request POST \
> >   "$API_URL/api/v1/public/$SHARE_TOKEN/runs/query" \
> >   --header "Content-Type: application/json" \
> >   --data '{}'
> > curl "$API_URL/api/v1/public/$SHARE_TOKEN/run/$RUN_ID"
> >
> > # Read the share state, then remove public access.
> > curl "$API_URL/api/v1/runs/$RUN_ID/share" \
> >   --header "X-API-Key: $LANGSMITH_API_KEY"
> > curl --request DELETE \
> >   "$API_URL/api/v1/runs/$RUN_ID/share" \
> >   --header "X-API-Key: $LANGSMITH_API_KEY"
> > ```
>
> > [tab] After
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > # Share a trace.
> > curl --request POST \
> >   "$API_URL/api/v2/runs/$RUN_ID/share" \
> >   --header "X-API-Key: $LANGSMITH_API_KEY" \
> >   --header "Content-Type: application/json" \
> >   --data "{\"session_id\":\"$PROJECT_ID\",\"trace_id\":\"$TRACE_ID\"}"
> >
> > # Query the public trace.
> > curl --request POST \
> >   "$API_URL/api/v2/public/$SHARE_TOKEN/runs/query" \
> >   --header "Content-Type: application/json" \
> >   --data '{"selects":["ID","NAME","RUN_TYPE","STATUS","START_TIME"]}'
> >
> > # Retrieve one public run using its exact start time from the query response.
> > curl --get "$API_URL/api/v2/public/$SHARE_TOKEN/run/$RUN_ID" \
> >   --data-urlencode "start_time=$START_TIME" \
> >   --data-urlencode "selects=ID" \
> >   --data-urlencode "selects=NAME" \
> >   --data-urlencode "selects=RUN_TYPE" \
> >   --data-urlencode "selects=STATUS" \
> >   --data-urlencode "selects=START_TIME"
> >
> > # Retrieve the deployment-aware public URL for an authenticated run.
> > curl --get "$API_URL/api/v2/runs/$RUN_ID" \
> >   --header "X-API-Key: $LANGSMITH_API_KEY" \
> >   --data-urlencode "project_id=$PROJECT_ID" \
> >   --data-urlencode "start_time=$START_TIME" \
> >   --data-urlencode "selects=SHARE_URL"
> >
> > # Remove public access by root trace ID.
> > curl --request DELETE \
> >   "$API_URL/api/v2/runs/$TRACE_ID/share" \
> >   --header "X-API-Key: $LANGSMITH_API_KEY" \
> >   --header "Content-Type: application/json" \
> >   --data "{\"session_id\":\"$PROJECT_ID\"}"
> > ```

## Feedback: create

Create feedback (a score, correction, or comment) for a run.

### Main changes

#### Required parameter

The method name and endpoint are unchanged. Only the session (project) ID requirement changes.

> [tab] Python
>
> > [!WARNING]
> >
> > `create_feedback` now requires `session_id`, the UUID of the project (session) that owns the run. It was previously optional.
>
> | Before | After | Notes |
> | - | - | - |
> | `session_id` (optional) | `session_id` (**required**) | UUID of the project that owns the run; resolve it with `client.read_project()` if you do not already have it |

> [tab] TypeScript
>
> > [!WARNING]
> >
> > `client.createFeedback` now requires `sessionId`, the UUID of the project (session) that owns the run. It was previously optional.
>
> | Before | After | Notes |
> | - | - | - |
> | `sessionId` (optional) | `sessionId` (**required**) | UUID of the project that owns the run; resolve it with `client.readProject()` if you do not already have it |

> [tab] Java
>
> > [!WARNING]
> >
> > `FeedbackCreateSchema.sessionId()` is now required. It was previously optional.
>
> | Before | After | Notes |
> | - | - | - |
> | `sessionId()` (optional) | `sessionId()` (**required**) | UUID of the project that owns the run; resolve it with `client.sessions().list()` if you do not already have it |

> [tab] Go
>
> > [!WARNING]
> >
> > `FeedbackCreateSchemaParam.SessionID` is now required. It was previously optional.
>
> | Before | After | Notes |
> | - | - | - |
> | `SessionID` (optional) | `SessionID` (**required**) | UUID of the project that owns the run; resolve it with `client.Sessions.List()` if you do not already have it |

> [tab] cURL
>
> > [!WARNING]
> >
> > `POST /api/v1/feedback` now requires a `session_id` field in the request body. It was previously optional.
>
> | Before | After | Notes |
> | - | - | - |
> | `session_id` (optional) | `session_id` (**required**) | UUID of the project that owns the run; resolve it with `GET /api/v1/sessions` if you do not already have it |

### Examples

#### Provide `session_id` when creating feedback

> [tab] Python
>
> `create_feedback` now requires `session_id` in addition to `run_id`.
>
> > [tab] Before
> >
> > ```python Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > from langsmith import Client
> >
> > client = Client()
> > run_id = "<run-id>"
> > client.create_feedback(
> >     run_id=run_id,
> >     key="user_feedback",
> >     score=1,
> > )
> > ```
>
> > [tab] After
> >
> > ```python After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > from langsmith import Client
> >
> > client = Client()
> > run_id = "<run-id>"
> > session_id = "<session-id>"
> > client.create_feedback(
> >     run_id=run_id,
> >     key="user_feedback",
> >     score=1,
> >     session_id=session_id,
> > )
> > ```

> [tab] TypeScript
>
> `client.createFeedback` now requires `sessionId` in addition to `runId`.
>
> > [tab] Before
> >
> > ```ts Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import { Client } from "langsmith";
> >
> > const client = new Client();
> > let runId = "<run-id>";
> > await client.createFeedback(runId, "user_feedback", {
> >   score: 1,
> > });
> > ```
>
> > [tab] After
> >
> > ```ts After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import { Client } from "langsmith";
> >
> > const client = new Client();
> > let runId = "<run-id>";
> > let sessionId = "<session-id>";
> > await client.createFeedback(runId, "user_feedback", {
> >   score: 1,
> >   sessionId,
> > });
> > ```

> [tab] Java
>
> `.create()` now requires `.sessionId()` in addition to `.runId()`.
>
> > [tab] Before
> >
> > ```kotlin Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import com.langchain.smith.client.LangsmithClient
> > import com.langchain.smith.client.okhttp.LangsmithOkHttpClient
> > import com.langchain.smith.models.feedback.FeedbackCreateSchema
> >
> > val client: LangsmithClient = LangsmithOkHttpClient.fromEnv()
> >
> > var runId = "<run-id>"
> > client.feedback().create(
> >     FeedbackCreateSchema.builder()
> >         .runId(runId)
> >         .key("user_feedback")
> >         .score(1.0)
> >         .build()
> > )
> > ```
>
> > [tab] After
> >
> > ```kotlin After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import com.langchain.smith.client.LangsmithClient
> > import com.langchain.smith.client.okhttp.LangsmithOkHttpClient
> > import com.langchain.smith.models.feedback.FeedbackCreateSchema
> >
> > val client: LangsmithClient = LangsmithOkHttpClient.fromEnv()
> >
> > var runId = "<run-id>"
> > var sessionId = "<session-id>"
> > client.feedback().create(
> >     FeedbackCreateSchema.builder()
> >         .runId(runId)
> >         .key("user_feedback")
> >         .score(1.0)
> >         .sessionId(sessionId)
> >         .build()
> > )
> > ```

> [tab] Go
>
> `Feedback.New` now requires `SessionID` in addition to `RunID`.
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
> > 	"github.com/langchain-ai/langsmith-go/shared"
> > )
> >
> > ctx := context.Background()
> > client := langsmith.NewClient()
> >
> > runID := "<run-id>"
> > var err error
> > _, err = client.Feedback.New(ctx, langsmith.FeedbackNewParams{
> > 	FeedbackCreateSchema: langsmith.FeedbackCreateSchemaParam{
> > 		RunID: langsmith.F(runID),
> > 		Key:   langsmith.F("user_feedback"),
> > 		Score: langsmith.F[langsmith.FeedbackCreateSchemaScoreUnionParam](https://docs.langchain.com/langsmith/shared.UnionFloat(1.0)),
> > 	},
> > })
> > ```
>
> > [tab] After
> >
> > ```go After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > package main
> >
> > import (
> > 	"context"
> >
> > 	"github.com/langchain-ai/langsmith-go"
> > 	"github.com/langchain-ai/langsmith-go/shared"
> > )
> >
> > ctx := context.Background()
> > client := langsmith.NewClient()
> >
> > runID := "<run-id>"
> > sessionID := "<session-id>"
> > var err error
> > _, err = client.Feedback.New(ctx, langsmith.FeedbackNewParams{
> > 	FeedbackCreateSchema: langsmith.FeedbackCreateSchemaParam{
> > 		RunID:     langsmith.F(runID),
> > 		Key:       langsmith.F("user_feedback"),
> > 		Score:     langsmith.F[langsmith.FeedbackCreateSchemaScoreUnionParam](https://docs.langchain.com/langsmith/shared.UnionFloat(1.0)),
> > 		SessionID: langsmith.F(sessionID),
> > 	},
> > })
> > ```

> [tab] cURL
>
> `POST /api/v1/feedback` now requires a `session_id` field in addition to `run_id`.
>
> > [tab] Before
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > RUN_ID="<run-id>"
> >
> > curl -X POST "https://api.smith.langchain.com/api/v1/feedback" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" \
> >   -H "Content-Type: application/json" \
> >   -d "$(jq -n --arg run "$RUN_ID" '{"run_id": $run, "key": "user_feedback", "score": 1}')"
> > ```
>
> > [tab] After
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > RUN_ID="<run-id>"
> > SESSION_ID="<session-id>"
> >
> > curl -X POST "https://api.smith.langchain.com/api/v1/feedback" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" \
> >   -H "Content-Type: application/json" \
> >   -d "$(jq -n --arg run "$RUN_ID" --arg session "$SESSION_ID" '{"run_id": $run, "key": "user_feedback", "score": 1, "session_id": $session}')"
> > ```

## See also

* [Retrieve runs](Migrate%20run%20retrieval%20to%20SmithDB.md)
* [Dataset experiment runs](Migrate%20dataset%20experiment%20runs%20to%20SmithDB.md)
* [Migration overview](Migrate%20to%20SmithDB-backed%20APIs.md)

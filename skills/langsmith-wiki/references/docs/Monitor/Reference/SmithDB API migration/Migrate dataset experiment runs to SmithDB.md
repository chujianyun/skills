# Migrate dataset experiment runs to SmithDB

> Migrate the LangSmith SDK dataset experiment run methods to their SmithDB-backed equivalents.

These methods query the runs attached to a dataset experiment. For deprecation dates, minimum SDK versions, and the agent prompt that applies to every method, see [Migrate to SmithDB-backed APIs](Migrate%20to%20SmithDB-backed%20APIs.md).

## Dataset experiment runs: query

Query dataset examples together with the experiment runs recorded against each example. Accepts one or more `experiment_ids` so you can view runs from multiple experiments side by side; results are returned as a cursor-paginated page.

### Main changes

#### Method name

> [tab] Python
>
> | Before | After |
> | - | - |
> | `client.get_experiment_results()` | `client.datasets.experiment_runs.query()` |
>
> > [!NOTE]
> >
> > `client.datasets.experiment_runs.query()` is now async. Call it with `await`.
>
> See the [reference](https://reference.langchain.com/python/langsmith/_openapi_client/resources/datasets/experiment_runs/ExperimentRunsResource/query) for the full parameter and field list.

> [tab] TypeScript
>
> | Before | After |
> | - | - |
> | *(no legacy public `Client` method)* | `client.datasets.experimentRuns.query()` |
>
> See the [reference](https://reference.langchain.com/javascript/langsmith/_openapi_client/resources/Datasets/ExperimentRuns/query) for the full parameter and field list.

> [tab] Java
>
> | Before | After |
> | - | - |
> | `client.datasets().runs().query()` | `client.datasets().experimentRuns().query()` |
>
> See the [reference](https://javadoc.io/doc/com.langchain.smith/langsmith-java/latest/com/langchain/smith/services/blocking/datasets/ExperimentRunService.html) for the full parameter list.

> [tab] Go
>
> | Before | After |
> | - | - |
> | `client.Datasets.Runs.Query()` | `client.Datasets.ExperimentRuns.Query()` |
>
> See the [reference](https://pkg.go.dev/github.com/langchain-ai/langsmith-go#DatasetExperimentRunService.Query) for the full parameter list.

> [tab] cURL
>
> | Before | After |
> | - | - |
> | `POST /api/v1/datasets/{dataset_id}/runs` | `POST /api/v2/datasets/{dataset_id}/experiment-runs` |
>
> See the [API doc](../LangSmith%20REST%20API/Datasets/Fetch%20experiment%20runs%20for%20dataset%20examples.md) for the full parameter and field list.

#### Query parameters

> [tab] Python
>
> > [!WARNING]
> >
> > `experiment_ids` is required and replaces `session_ids`. Values are still experiment tracing-project UUIDs—if you only know the experiment's name, resolve it first: `client.read_project(project_name="my-experiment").id`, or `await client.aread_project(project_name="my-experiment")` in async code.
>
> | Before (`get_experiment_results`) | After (`datasets.experiment_runs.query`) | Notes |
> | - | - | - |
> | `project_id` | `experiment_ids` | `get_experiment_results` accepted one project/experiment; the new method accepts a required non-empty list |
> | `limit` | *(removed)* | Use `page_size` for per-request batch size |
> | *(not available)* | `page_size` | Per-request result count (default 20, max 100) |
> | *(handled internally)* | `cursor` | Pass the previous page's `next_cursor` to fetch the next page |
> | `preview` | `selects` | Omitted `selects` returns only run IDs; use `INPUTS_PREVIEW` and `OUTPUTS_PREVIEW` for previews, or `INPUTS` and `OUTPUTS` for full payloads |
> | *(not exposed)* | `sort` | Use `{by, order}` for feedback-score sorting |
> | `filters` | `filters` | Unchanged; maps experiment UUID strings to filter expressions |
> | `comparative_experiment_id` | `comparative_experiment_id` | Unchanged |
> | *(not exposed)* | `example_ids` | Optional example UUID filter, max 1000 |

> [tab] TypeScript
>
> > [!WARNING]
> >
> > `experiment_ids` is required and replaces `session_ids`. Values are still experiment tracing-project UUIDs—if you only know the experiment's name, resolve it first: `(await client.readProject({ projectName: "my-experiment" })).id`.
>
> | Before | After (`datasets.experimentRuns.query`) | Notes |
> | - | - | - |
> | *(no legacy public `Client` method)* | `experiment_ids` | Required and non-empty |
> | *(no legacy public `Client` method)* | `page_size` | Defaults to 20, max 100 |
> | *(no legacy public `Client` method)* | `cursor` | Pass the previous page's `next_cursor` instead of a numeric offset |
> | *(no legacy public `Client` method)* | `selects` | Omitted `selects` returns only run IDs; use `INPUTS_PREVIEW` and `OUTPUTS_PREVIEW` for previews, or `INPUTS` and `OUTPUTS` for full payloads |
> | *(no legacy public `Client` method)* | `sort` | Use `{ by, order }` for feedback-score sorting |
> | *(no legacy public `Client` method)* | `filters` | Maps experiment UUID strings to filter expressions |
> | *(no legacy public `Client` method)* | `comparative_experiment_id` | Scopes pairwise-annotation feedback |
> | *(no legacy public `Client` method)* | `example_ids` | Optional example UUID filter, max 1000 |

> [tab] Java
>
> > [!WARNING]
> >
> > `experimentIds()` is required and replaces `sessionIds()`. Values are still experiment tracing-project UUIDs—if you only know the experiment's name, resolve it first: `client.sessions().list(SessionListParams.builder().name("my-experiment").build()).items().first().id()`.
>
> | Before (`RunQueryParams`) | After (`ExperimentRunQueryParams`) | Notes |
> | - | - | - |
> | `sessionIds()` | `experimentIds()` | Renamed; required and non-empty |
> | `limit()` | *(removed)* | Use `pageSize()` for per-request batch size |
> | *(not available)* | `pageSize()` | Per-request result count (default 20, max 100) |
> | `offset()` | `cursor()` | Pass the previous page's `nextCursor()` instead of a numeric offset |
> | `preview()` | `selects()` | Omitted selects return only run IDs; add `Select.INPUTS_PREVIEW` and `Select.OUTPUTS_PREVIEW` for previews |
> | `sortParams()` | `sort()` | Shape changed from `sortBy()` / `sortOrder()` to `by()` / `order()` |
> | `filters()` | `filters()` | Unchanged |
> | `comparativeExperimentId()` | `comparativeExperimentId()` | Unchanged |
> | `exampleIds()` | `exampleIds()` | Unchanged, max 1000 |
> | `format()` | *(removed)* | The new endpoint returns JSON only |
> | `includeAnnotatorDetail()` | *(removed)* | No new JSON equivalent |

> [tab] Go
>
> > [!WARNING]
> >
> > `ExperimentIDs` is required and replaces `SessionIDs`. Values are still experiment tracing-project UUIDs—if you only know the experiment's name, resolve it first: list sessions filtered by `Name` and take the first result's `ID`.
>
> | Before (`DatasetRunQueryParams`) | After (`DatasetExperimentRunQueryParams`) | Notes |
> | - | - | - |
> | `SessionIDs` | `ExperimentIDs` | Renamed; required and non-empty |
> | `Limit` | *(removed)* | Use `PageSize` for per-request batch size |
> | *(not available)* | `PageSize` | Per-request result count (default 20, max 100) |
> | `Offset` | `Cursor` | Pass the previous page's `NextCursor` instead of a numeric offset |
> | `Preview` | `Selects` | Omitted selects return only run IDs; use `InputsPreview` and `OutputsPreview` select constants for previews |
> | `SortParams` | `Sort` | Shape changed from `SortBy` / `SortOrder` to `By` / `Order` |
> | `Filters` | `Filters` | Unchanged |
> | `ComparativeExperimentID` | `ComparativeExperimentID` | Unchanged |
> | `ExampleIDs` | `ExampleIDs` | Unchanged, max 1000 |
> | `Format` | *(removed)* | The new endpoint returns JSON only |
> | `IncludeAnnotatorDetail` | *(removed)* | No new JSON equivalent |

> [tab] cURL
>
> > [!WARNING]
> >
> > `experiment_ids` is required and replaces `session_ids`. Values are still experiment tracing-project UUIDs—if you only know the experiment's name, resolve it first: `GET /api/v1/sessions?name=my-experiment` and take `.[0].id`.
>
> | Before (`POST /api/v1/datasets/{dataset_id}/runs` body) | After (`POST /api/v2/datasets/{dataset_id}/experiment-runs` body) | Notes |
> | - | - | - |
> | `session_ids` | `experiment_ids` | Renamed; required and non-empty |
> | `limit` | *(removed)* | Use `page_size` for per-request batch size |
> | *(not available)* | `page_size` | Per-request result count (default 20, max 100) |
> | `offset` | `cursor` | Pass the previous page's `next_cursor` instead of a numeric offset |
> | `preview` | `selects` | Omitted `selects` returns only run IDs; use `INPUTS_PREVIEW` and `OUTPUTS_PREVIEW` for previews, or `INPUTS` and `OUTPUTS` for full payloads |
> | `sort_params` | `sort` | Shape changed from `{sort_by, sort_order}` to `{by, order}` |
> | `filters` | `filters` | Unchanged; maps experiment UUID strings to filter expressions |
> | `comparative_experiment_id` | `comparative_experiment_id` | Unchanged |
> | `example_ids` | `example_ids` | Unchanged, max 1000 |
> | `format=csv` | *(removed)* | The new endpoint returns JSON only |
> | `include_annotator_detail` | *(removed)* | No new JSON equivalent |

#### Response fields

Each page item is a dataset example paired with the runs produced for it—not a bare `Run`. Its `runs` field holds the same `Run` objects returned by [Querying runs](#response-fields); see that section for the per-run fields. The tables below describe the rest of the item: the example fields alongside `runs`.

> [tab] Python
>
> `get_experiment_results` returned experiment results with an `examples_with_runs` iterator. `datasets.experiment_runs.query` returns a paginated page object (`page.items`, `page.next_cursor`); each item has:
>
> | Field | Notes |
> | - | - |
> | `id` | Dataset example UUID |
> | `dataset_id` | Parent dataset UUID |
> | `name` | Example name, if set |
> | `created_at` / `modified_at` | Example timestamps |
> | `inputs` / `outputs` | Example input and reference-output payloads |
> | `metadata` | Example metadata |
> | `source_run_id` | Run UUID the example was created from, if any |
> | `attachment_urls` | Pre-signed download URL per attachment name |
> | `runs` | This example's runs—see [Querying runs](#response-fields) |

> [tab] TypeScript
>
> The legacy dataset runs endpoint was not exposed on the public TypeScript `Client`. `datasets.experimentRuns.query` returns a paginated page (`page.getPaginatedItems()`, `page.next_cursor`); each item has:
>
> | Field | Notes |
> | - | - |
> | `id` | Dataset example UUID |
> | `dataset_id` | Parent dataset UUID |
> | `name` | Example name, if set |
> | `created_at` / `modified_at` | Example timestamps |
> | `inputs` / `outputs` | Example input and reference-output payloads |
> | `metadata` | Example metadata |
> | `source_run_id` | Run UUID the example was created from, if any |
> | `attachment_urls` | Pre-signed download URL per attachment name |
> | `runs` | This example's runs—see [Querying runs](#response-fields) |

> [tab] Java
>
> `runs().query` returned an optional list. `experimentRuns().query` returns a page object (`items()`, `nextCursor()`); each item has:
>
> | Field | Notes |
> | - | - |
> | `id()` | Dataset example UUID |
> | `datasetId()` | Parent dataset UUID |
> | `name()` | Example name, if set |
> | `createdAt()` / `modifiedAt()` | Example timestamps |
> | `inputs()` / `outputs()` | Example input and reference-output payloads |
> | `metadata()` | Example metadata |
> | `sourceRunId()` | Run UUID the example was created from, if any |
> | `attachmentUrls()` | Pre-signed download URL per attachment name |
> | `runs()` | This example's runs—see [Querying runs](#response-fields) |

> [tab] Go
>
> `Datasets.Runs.Query` returned a slice pointer. `Datasets.ExperimentRuns.Query` returns an `ItemsCursorPostPagination` (`Items`, `NextCursor`); each item has:
>
> | Field | Notes |
> | - | - |
> | `ID` | Dataset example UUID |
> | `DatasetID` | Parent dataset UUID |
> | `Name` | Example name, if set |
> | `CreatedAt` / `ModifiedAt` | Example timestamps |
> | `Inputs` / `Outputs` | Example input and reference-output payloads |
> | `Metadata` | Example metadata |
> | `SourceRunID` | Run UUID the example was created from, if any |
> | `AttachmentURLs` | Pre-signed download URL per attachment name |
> | `Runs` | This example's runs—see [Querying runs](#response-fields) |

> [tab] cURL
>
> `POST /api/v1/datasets/{dataset_id}/runs` returned a JSON array. `POST /api/v2/datasets/{dataset_id}/experiment-runs` returns `{ "items": [...], "next_cursor": "..." }`; each item has:
>
> | Field | Notes |
> | - | - |
> | `id` | Dataset example UUID |
> | `dataset_id` | Parent dataset UUID |
> | `name` | Example name, if set |
> | `created_at` / `modified_at` | Example timestamps |
> | `inputs` / `outputs` | Example input and reference-output payloads |
> | `metadata` | Example metadata |
> | `source_run_id` | Run UUID the example was created from, if any |
> | `attachment_urls` | Pre-signed download URL per attachment name |
> | `runs` | This example's runs—see [Querying runs](#response-fields) |

### Examples

#### Query experiment runs and request preview fields

> [tab] Python
>
> `preview=True` returned truncated inputs/outputs automatically. In the new API, request that explicitly: pass `INPUTS_PREVIEW` and `OUTPUTS_PREVIEW` in `selects` for the same truncated shape, or `INPUTS`/`OUTPUTS` for the untruncated values. Omitting `selects` returns only `id`.
>
> > [tab] Before
> >
> > ```python Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > from langsmith import Client
> >
> > client = Client()
> > experiment_id = client.read_project(project_name=experiment_name).id
> > results = client.get_experiment_results(
> >     project_id=experiment_id,
> >     limit=20,
> >     preview=True,
> > )
> > examples_with_runs = list(results["examples_with_runs"])
> > ```
>
> > [tab] After
> >
> > ```python After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > from langsmith import Client
> > import asyncio
> >
> >
> > async def main():
> >     client = Client()
> >     experiment_id = client.read_project(project_name=experiment_name).id
> >     page = await client.datasets.experiment_runs.query(
> >         str(dataset_id),
> >         experiment_ids=[str(experiment_id)],
> >         page_size=20,
> >         selects=["ID", "NAME", "STATUS", "INPUTS_PREVIEW", "OUTPUTS_PREVIEW"],
> >     )
> >     return page.items
> >
> >
> > examples_with_runs = asyncio.run(main())
> > ```

> [tab] TypeScript
>
> The new TypeScript SDK method exposes the experiment-runs query endpoint. The legacy direct endpoint request shape is shown in the cURL tab. Pass `INPUTS_PREVIEW` and `OUTPUTS_PREVIEW` in `selects` for truncated inputs/outputs, or `INPUTS`/`OUTPUTS` for the untruncated values. Omitting `selects` returns only `id`.
>
> > [tab] Before
> >
> > ```ts Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > // The legacy dataset runs endpoint was not exposed on the public TypeScript Client.
> > // Use the cURL example for the old request body shape.
> > ```
>
> > [tab] After
> >
> > ```ts After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import { uuid7 } from "langsmith";
> > import { Client } from "langsmith";
> >
> > const client = new Client();
> > const experimentId = (await client.readProject({ projectName: experimentName })).id;
> > const page = await client.datasets.experimentRuns.query(datasetId, {
> >   experiment_ids: [experimentId],
> >   page_size: 20,
> >   selects: ["ID", "NAME", "STATUS", "INPUTS_PREVIEW", "OUTPUTS_PREVIEW"],
> > });
> > const examplesWithRuns = page.getPaginatedItems();
> > ```

> [tab] Java
>
> `preview(true)` returned truncated inputs/outputs automatically. In the new API, request that explicitly: add `Select.INPUTS_PREVIEW` and `Select.OUTPUTS_PREVIEW` for the same truncated shape, or `Select.INPUTS`/`Select.OUTPUTS` for the untruncated values. Omitting selects returns only `id`.
>
> > [tab] Before
> >
> > ```kotlin Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import com.langchain.smith.client.LangsmithClient
> > import com.langchain.smith.client.okhttp.LangsmithOkHttpClient
> > import com.langchain.smith.models.datasets.runs.RunQueryParams
> >
> > val client: LangsmithClient = LangsmithOkHttpClient.fromEnv()
> > val examplesWithRuns = client.datasets().runs().query(
> >     datasetId,
> >     RunQueryParams.builder()
> >         .addSessionId(experimentId)
> >         .limit(20L)
> >         .preview(true)
> >         .build()
> > )
> > ```
>
> > [tab] After
> >
> > ```kotlin After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import com.langchain.smith.client.LangsmithClient
> > import com.langchain.smith.client.okhttp.LangsmithOkHttpClient
> > import com.langchain.smith.models.datasets.experimentruns.ExperimentRunQueryParams
> > import com.langchain.smith.models.runs.RunSelectField
> >
> > val client: LangsmithClient = LangsmithOkHttpClient.fromEnv()
> > val page = client.datasets().experimentRuns().query(
> >     datasetId,
> >     ExperimentRunQueryParams.builder()
> >         .addExperimentId(experimentId)
> >         .pageSize(20L)
> >         .addSelect(RunSelectField.ID)
> >         .addSelect(RunSelectField.NAME)
> >         .addSelect(RunSelectField.STATUS)
> >         .addSelect(RunSelectField.INPUTS_PREVIEW)
> >         .addSelect(RunSelectField.OUTPUTS_PREVIEW)
> >         .build()
> > )
> > val examplesWithRuns = page.items()
> > ```

> [tab] Go
>
> `Preview: true` returned truncated inputs/outputs automatically. In the new API, request that explicitly: add the `InputsPreview` and `OutputsPreview` select constants for the same truncated shape, or `Inputs`/`Outputs` for the untruncated values. Omitting selects returns only `ID`.
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
> > ctx := context.Background()
> > client := langsmith.NewClient()
> > examplesWithRuns, err := client.Datasets.Runs.Query(ctx, datasetID, langsmith.DatasetRunQueryParams{
> > 	SessionIDs: langsmith.F([]string{experimentID}),
> > 	Limit:      langsmith.F(int64(20)),
> > 	Preview:    langsmith.F(true),
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
> > )
> >
> > ctx := context.Background()
> > client := langsmith.NewClient()
> > page, err := client.Datasets.ExperimentRuns.Query(ctx, datasetID, langsmith.DatasetExperimentRunQueryParams{
> > 	ExperimentIDs: langsmith.F([]string{experimentID}),
> > 	PageSize:      langsmith.F(int64(20)),
> > 	Selects: langsmith.F([]langsmith.RunSelectField{
> > 		langsmith.RunSelectFieldID,
> > 		langsmith.RunSelectFieldName,
> > 		langsmith.RunSelectFieldStatus,
> > 		langsmith.RunSelectFieldInputsPreview,
> > 		langsmith.RunSelectFieldOutputsPreview,
> > 	}),
> > })
> > ```

> [tab] cURL
>
> `preview: true` returned truncated inputs/outputs automatically. In the new API, request that explicitly: pass `INPUTS_PREVIEW` and `OUTPUTS_PREVIEW` in `selects` for the same truncated shape, or `INPUTS`/`OUTPUTS` for the untruncated values. Omitting `selects` returns only `id`.
>
> > [tab] Before
> >
> > ```bash Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > curl -X POST "https://api.smith.langchain.com/api/v1/datasets/$DATASET_ID/runs" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" \
> >   -H "Content-Type: application/json" \
> >   -d "$(jq -n --arg eid "$EXPERIMENT_ID" '{
> >     "session_ids": [$eid],
> >     "limit": 20,
> >     "preview": true
> >   }')"
> > ```
>
> > [tab] After
> >
> > ```bash After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > curl -X POST "https://api.smith.langchain.com/api/v2/datasets/$DATASET_ID/experiment-runs" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" \
> >   -H "Content-Type: application/json" \
> >   -d "$(jq -n --arg eid "$EXPERIMENT_ID" '{
> >     "experiment_ids": [$eid],
> >     "page_size": 20,
> >     "selects": ["ID", "NAME", "STATUS", "INPUTS_PREVIEW", "OUTPUTS_PREVIEW"]
> >   }')"
> > ```

#### Page through results

Both examples below fetch up to 100 results across as many pages as that takes, then stop—so the two are comparable operations, not "one page" vs. "everything." Adjust the `100`/`page_size` values for your own use case.

> [tab] Python
>
> `get_experiment_results` paginates internally and stops once `limit` total results are returned. `datasets.experiment_runs.query` has no total-count `limit`; iterate the returned page with `async for` and `break` once you have enough.
>
> > [tab] Before
> >
> > ```python Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > from langsmith import Client
> >
> > client = Client()
> > experiment_id = client.read_project(project_name=experiment_name).id
> > # get_experiment_results paginated internally; increase `limit` to fetch
> > # more results in a single call. There is no cursor to pass in manually.
> > results = client.get_experiment_results(
> >     project_id=experiment_id,
> >     limit=100,
> > )
> > examples_with_runs = list(results["examples_with_runs"])
> > ```
>
> > [tab] After
> >
> > ```python After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > from langsmith import Client
> > import asyncio
> >
> >
> > async def main():
> >     client = Client()
> >     experiment_id = client.read_project(project_name=experiment_name).id
> >     page = await client.datasets.experiment_runs.query(
> >         str(dataset_id),
> >         experiment_ids=[str(experiment_id)],
> >         page_size=1,
> >     )
> >     runs = []
> >     async for run in page:
> >         runs.append(run)
> >         if len(runs) >= 100:
> >             break
> >     return runs
> >
> >
> > examples_with_runs = asyncio.run(main())
> > ```

> [tab] TypeScript
>
> The legacy dataset runs endpoint wasn't exposed on the public TypeScript `Client`. `client.datasets.experimentRuns.query(...)` returns an async iterable—use `for await...of` (no extra `await` needed) and `break` once you have enough.
>
> > [tab] Before
> >
> > ```ts Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > // The legacy dataset runs endpoint was not exposed on the public TypeScript Client.
> > // Use the cURL example for the old request body shape.
> > ```
>
> > [tab] After
> >
> > ```ts After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import { uuid7 } from "langsmith";
> > import { Client } from "langsmith";
> >
> > const client = new Client();
> > const experimentId = (await client.readProject({ projectName: experimentName })).id;
> > const runs: unknown[] = [];
> > for await (const run of client.datasets.experimentRuns.query(datasetId, {
> >   experiment_ids: [experimentId],
> >   page_size: 1,
> > })) {
> >   runs.push(run);
> >   if (runs.length >= 100) break;
> > }
> > ```

> [tab] Java
>
> The legacy endpoint returns one page per call with no auto-pager—loop manually, incrementing `offset`, and stop once you have enough. `.experimentRuns().query(...).autoPager()` walks pages for you—break out of the loop once you have enough runs.
>
> > [tab] Before
> >
> > ```kotlin Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import com.langchain.smith.client.LangsmithClient
> > import com.langchain.smith.client.okhttp.LangsmithOkHttpClient
> > import com.langchain.smith.models.datasets.runs.RunQueryParams
> > import com.langchain.smith.models.datasets.runs.ExampleWithRunsCh
> >
> > val client: LangsmithClient = LangsmithOkHttpClient.fromEnv()
> > val examplesWithRuns = mutableListOf<ExampleWithRunsCh>()
> > var offset = 0L
> > val limit = 20L
> > while (true) {
> >     val page = client.datasets().runs().query(
> >         datasetId,
> >         RunQueryParams.builder()
> >             .addSessionId(experimentId)
> >             .limit(limit)
> >             .offset(offset)
> >             .build()
> >     ).orElse(emptyList())
> >     examplesWithRuns.addAll(page)
> >     if (examplesWithRuns.size >= 100 || page.size.toLong() < limit) break
> >     offset += limit
> > }
> > ```
>
> > [tab] After
> >
> > ```kotlin After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import com.langchain.smith.client.LangsmithClient
> > import com.langchain.smith.client.okhttp.LangsmithOkHttpClient
> > import com.langchain.smith.models.datasets.experimentruns.ExperimentRunQueryParams
> >
> > val client: LangsmithClient = LangsmithOkHttpClient.fromEnv()
> > val page = client.datasets().experimentRuns().query(
> >     datasetId,
> >     ExperimentRunQueryParams.builder()
> >         .addExperimentId(experimentId)
> >         .pageSize(1L)
> >         .build()
> > )
> > var count = 0
> > for (run in page.autoPager()) {
> >     count++
> >     if (count >= 100) break
> > }
> > ```

> [tab] Go
>
> The legacy endpoint returns one page per call with no auto-pager—loop manually, incrementing `Offset`, and stop once you have enough. On the new endpoint, paginate manually by setting `Cursor` on the request from the previous response's `NextCursor` and stopping once you have enough; avoid `QueryAutoPaging` here—it sends the cursor as a query parameter, which this POST endpoint doesn't read, so it silently refetches the first page forever.
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
> > ctx := context.Background()
> > client := langsmith.NewClient()
> > var examplesWithRuns []langsmith.ExampleWithRunsCh
> > offset := int64(0)
> > limit := int64(20)
> > for {
> > 	page, err := client.Datasets.Runs.Query(ctx, datasetID, langsmith.DatasetRunQueryParams{
> > 		SessionIDs: langsmith.F([]string{experimentID}),
> > 		Limit:      langsmith.F(limit),
> > 		Offset:     langsmith.F(offset),
> > 	})
> > 	examplesWithRuns = append(examplesWithRuns, *page...)
> > 	if len(examplesWithRuns) >= 100 || int64(len(*page)) < limit {
> > 		break
> > 	}
> > 	offset += limit
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
> >
> > 	"github.com/langchain-ai/langsmith-go"
> > )
> >
> > ctx := context.Background()
> > client := langsmith.NewClient()
> > params := langsmith.DatasetExperimentRunQueryParams{
> > 	ExperimentIDs: langsmith.F([]string{experimentID}),
> > 	PageSize:      langsmith.F(int64(1)),
> > }
> > var examplesWithRuns []langsmith.DatasetExperimentRunQueryResponse
> > for {
> > 	page, err := client.Datasets.ExperimentRuns.Query(ctx, datasetID, params)
> > 	examplesWithRuns = append(examplesWithRuns, page.Items...)
> > 	if page.NextCursor == "" || len(examplesWithRuns) >= 100 {
> > 		break
> > 	}
> > 	params.Cursor = langsmith.F(page.NextCursor)
> > }
> > ```

> [tab] cURL
>
> Raw HTTP has no auto-pagination helper: pass the previous response's `next_cursor` back in as `cursor` to fetch the next page.
>
> > [tab] Before
> >
> > ```bash Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > curl -X POST "https://api.smith.langchain.com/api/v1/datasets/$DATASET_ID/runs" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" \
> >   -H "Content-Type: application/json" \
> >   -d "$(jq -n --arg eid "$EXPERIMENT_ID" '{
> >     "session_ids": [$eid],
> >     "limit": 20,
> >     "offset": 20
> >   }')"
> > ```
>
> > [tab] After
> >
> > ```bash After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > curl -X POST "https://api.smith.langchain.com/api/v2/datasets/$DATASET_ID/experiment-runs" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" \
> >   -H "Content-Type: application/json" \
> >   -d "$(jq -n --arg eid "$EXPERIMENT_ID" --arg cursor "$NEXT_CURSOR" '{
> >     "experiment_ids": [$eid],
> >     "page_size": 20,
> >     "cursor": $cursor
> >   }')"
> > ```

#### Sort by feedback score

Sort dataset examples by a feedback score, supported only when you query a single experiment. In Go and Java, this replaces the legacy `sort_params.sort_by`/`sort_params.sort_order` (now `sort.by`/`sort.order`); Python and TypeScript gain sorting for the first time in the new API.

> [tab] Python
>
> `get_experiment_results` did not support sorting by feedback score.
>
> > [tab] Before
> >
> > ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > # get_experiment_results did not support sorting results by feedback score.
> > ```
>
> > [tab] After
> >
> > ```python After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > from langsmith import Client
> > import asyncio
> >
> >
> > async def main():
> >     client = Client()
> >     experiment_id = client.read_project(project_name=experiment_name).id
> >     page = await client.datasets.experiment_runs.query(
> >         str(dataset_id),
> >         experiment_ids=[str(experiment_id)],
> >         sort={"by": "feedback.correctness", "order": "ASC"},
> >     )
> >     return page.items
> >
> >
> > examples_with_runs = asyncio.run(main())
> > ```

> [tab] TypeScript
>
> The legacy dataset runs endpoint was not exposed on the public TypeScript `Client`, so there was no way to sort by feedback score before the new API.
>
> > [tab] Before
> >
> > ```ts Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > // The legacy dataset runs endpoint was not exposed on the public TypeScript Client.
> > // Use the cURL example for the old request body shape.
> > ```
>
> > [tab] After
> >
> > ```ts After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import { uuid7 } from "langsmith";
> > import { Client } from "langsmith";
> >
> > const client = new Client();
> > const experimentId = (await client.readProject({ projectName: experimentName })).id;
> > const page = await client.datasets.experimentRuns.query(datasetId, {
> >   experiment_ids: [experimentId],
> >   sort: { by: "feedback.correctness", order: "ASC" },
> > });
> > ```

> [tab] Java
>
> `sortParams()` is replaced by `sort()`, with `sortBy()`/`sortOrder()` renamed to `by()`/`order()`.
>
> > [tab] Before
> >
> > ```kotlin Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import com.langchain.smith.client.LangsmithClient
> > import com.langchain.smith.client.okhttp.LangsmithOkHttpClient
> > import com.langchain.smith.models.datasets.runs.RunQueryParams
> > import com.langchain.smith.models.datasets.runs.SortParamsForRunsComparisonView
> >
> > val client: LangsmithClient = LangsmithOkHttpClient.fromEnv()
> > val examplesWithRuns = client.datasets().runs().query(
> >     datasetId,
> >     RunQueryParams.builder()
> >         .addSessionId(experimentId)
> >         .sortParams(
> >             SortParamsForRunsComparisonView.builder()
> >                 .sortBy("correctness")
> >                 .sortOrder(SortParamsForRunsComparisonView.SortOrder.ASC)
> >                 .build()
> >         )
> >         .build()
> > )
> > ```
>
> > [tab] After
> >
> > ```kotlin After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import com.langchain.smith.client.LangsmithClient
> > import com.langchain.smith.client.okhttp.LangsmithOkHttpClient
> > import com.langchain.smith.models.datasets.experimentruns.ExperimentRunQueryParams
> >
> > val client: LangsmithClient = LangsmithOkHttpClient.fromEnv()
> > val page = client.datasets().experimentRuns().query(
> >     datasetId,
> >     ExperimentRunQueryParams.builder()
> >         .addExperimentId(experimentId)
> >         .sort(
> >             ExperimentRunQueryParams.Sort.builder()
> >                 .by("feedback.correctness")
> >                 .order("ASC")
> >                 .build()
> >         )
> >         .build()
> > )
> > ```

> [tab] Go
>
> `SortParams` is replaced by `Sort`, with `SortBy`/`SortOrder` renamed to `By`/`Order`.
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
> > ctx := context.Background()
> > client := langsmith.NewClient()
> > examplesWithRuns, err := client.Datasets.Runs.Query(ctx, datasetID, langsmith.DatasetRunQueryParams{
> > 	SessionIDs: langsmith.F([]string{experimentID}),
> > 	SortParams: langsmith.F(langsmith.SortParamsForRunsComparisonView{
> > 		SortBy:    langsmith.F("correctness"),
> > 		SortOrder: langsmith.F(langsmith.SortParamsForRunsComparisonViewSortOrderAsc),
> > 	}),
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
> > )
> >
> > ctx := context.Background()
> > client := langsmith.NewClient()
> > page, err := client.Datasets.ExperimentRuns.Query(ctx, datasetID, langsmith.DatasetExperimentRunQueryParams{
> > 	ExperimentIDs: langsmith.F([]string{experimentID}),
> > 	Sort: langsmith.F(langsmith.DatasetExperimentRunQueryParamsSort{
> > 		By:    langsmith.F("feedback.correctness"),
> > 		Order: langsmith.F("ASC"),
> > 	}),
> > })
> > ```

> [tab] cURL
>
> > [tab] Before
> >
> > ```bash Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > curl -X POST "https://api.smith.langchain.com/api/v1/datasets/$DATASET_ID/runs" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" \
> >   -H "Content-Type: application/json" \
> >   -d "$(jq -n --arg eid "$EXPERIMENT_ID" '{
> >     "session_ids": [$eid],
> >     "sort_params": {
> >       "sort_by": "correctness",
> >       "sort_order": "ASC"
> >     }
> >   }')"
> > ```
>
> > [tab] After
> >
> > ```bash After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > curl -X POST "https://api.smith.langchain.com/api/v2/datasets/$DATASET_ID/experiment-runs" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" \
> >   -H "Content-Type: application/json" \
> >   -d "$(jq -n --arg eid "$EXPERIMENT_ID" '{
> >     "experiment_ids": [$eid],
> >     "sort": {
> >       "by": "feedback.correctness",
> >       "order": "ASC"
> >     }
> >   }')"
> > ```

## See also

* [Threads](Migrate%20thread%20methods%20to%20SmithDB.md)
* [Feedback and annotation queues](Migrate%20feedback%20and%20sharing%20methods%20to%20SmithDB.md)
* [Migration overview](Migrate%20to%20SmithDB-backed%20APIs.md)

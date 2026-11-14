# Migrate to SmithDB-backed APIs

> Migrate your existing LangSmith SDK methods to their SmithDB-backed equivalents for faster agent observability.

## Context

In May 2026, we released [SmithDB](https://www.langchain.com/blog/introducing-smithdb?utm_source=docs), a new observability database built for modern AI agents. SmithDB delivers industry-leading performance across every key observability workload, making core LangSmith experiences dramatically faster.

New SDK methods are required to query your traces with SmithDB. This guide helps you migrate your codebase.

## Why migrate

* Queries run up to 12x faster on SmithDB. See the [benchmarks](https://www.langchain.com/blog/introducing-smithdb?utm_source=docs#performance).
* On LangSmith Cloud, the new query endpoints have higher rate limits than the deprecated ones.
* Dedicated methods for [traces](Migrate%20trace%20methods%20to%20SmithDB.md) and [threads](Migrate%20thread%20methods%20to%20SmithDB.md) replace filtering runs by hand.
* The deprecated methods stop working on January 31, 2027 on LangSmith Cloud, and when ClickHouse is turned off on self-hosted, at the latest with v0.19. Migrating early avoids a last-minute rush.

## Migrate with an AI agent

Copy the following prompt into your coding agent. It first sums up the change in plain words and waits for your go. Then it finds every SDK method and direct API call to the deprecated endpoints, waits for your approval, and migrates them locally. It pushes and opens a pull request only if you approve.

Migrate off deprecated LangSmith endpoints

Help me migrate this codebase off deprecated LangSmith API endpoints. On LangSmith Cloud they stop working on January 31, 2027. On self-hosted they stop working when ClickHouse is turned off, at the latest with the upgrade to v0.19. Calls may go through a LangSmith SDK (Python, TypeScript/JavaScript, Go or Java) or straight over HTTP; handle all of them.

Work in 4 phases, in order. Stop only where a phase says STOP, and wait for my go. Do not edit any file before I approve phase 2.

**Phase 1: summary in plain words (read only)**

Source of truth: fetch [https://docs.langchain.com/langsmith/smithdb-sdk-migration.md](Migrate%20to%20SmithDB-backed%20APIs.md) first (minimum SDK versions per language, exception changes, discontinued methods). Then fetch only the area pages this codebase needs. Each one has before/after examples in Python, TypeScript, Go, Java and cURL:

* Searching the runs in a project: [https://docs.langchain.com/langsmith/smithdb-sdk-migration-query-runs.md](Migrate%20run%20queries%20to%20SmithDB.md)
* Fetching one run by ID, its child runs, and its URL: [https://docs.langchain.com/langsmith/smithdb-sdk-migration-runs.md](Migrate%20run%20retrieval%20to%20SmithDB.md)
* Querying traces, their token and cost aggregates, and the runs in one trace: [https://docs.langchain.com/langsmith/smithdb-sdk-migration-traces.md](Migrate%20trace%20methods%20to%20SmithDB.md)
* Querying threads and the traces in one thread: [https://docs.langchain.com/langsmith/smithdb-sdk-migration-threads.md](Migrate%20thread%20methods%20to%20SmithDB.md)
* Querying the runs of an experiment on a dataset: [https://docs.langchain.com/langsmith/smithdb-sdk-migration-experiments.md](Migrate%20dataset%20experiment%20runs%20to%20SmithDB.md)
* Feedback, annotation queues, and shared runs: [https://docs.langchain.com/langsmith/smithdb-sdk-migration-feedback.md](Migrate%20feedback%20and%20sharing%20methods%20to%20SmithDB.md)

Then explain it to someone who does not know this codebase. No code, no file paths, at most 5 short bullets:

* What LangSmith is changing, in one sentence.
* Why we need to migrate: why LangSmith made this change, and what it brings us (see the guide's "Why migrate" section; the higher rate limits apply on LangSmith Cloud only).
* When the deprecated endpoints stop working for us (see the top of this prompt: a date on Cloud, a release on self-hosted), and what breaks if we do nothing.
* Which parts of this codebase seem affected, from a quick search (for example "the evaluation scripts").
* Rough size of the work: small, medium or large.

Then STOP and ask me whether to go on to phase 2.

**Phase 2: inventory and plan (read only)**

Search the whole repo (app code, scripts, notebooks, tests, CI and infra config, in every language it uses) for every SDK method and endpoint in the "Affected methods and endpoints" section of the guide's overview page:

* SDK calls in Python, TypeScript/JavaScript, Go and Java/Kotlin. In Go and Java some replacements keep a similar name under a new service, so match on the guide's before/after, not on the name alone.
* Feedback creation (`create_feedback`, `createFeedback`, `Feedback.New`, `feedback().create()`): the method and endpoint keep their name, but the project (session) ID is now required. List every call that does not pass it.
* Direct HTTP calls to the deprecated paths, with or without `/api/v1`, in raw or built URLs and any HTTP client (requests, httpx, fetch, axios, net/http, OkHttp, curl).
* Files under tests, fixtures, templates or task folders count as call sites if they run against a real LangSmith (scripts, build steps, notebooks).
* Match method names, not call syntax: a method can be passed as a reference (`asyncio.to_thread`, `functools.partial`, callbacks, `getattr`) with no parenthesis after it.

Keep raw HTTP calls as raw HTTP calls: change only the path, request body, response handling and pagination, following the guide's cURL examples. Note each raw call that would be simpler with an SDK method, for phase 4.

Show a table: file:line, language, SDK or HTTP, current call, replacement, risk.

Flag as risk: code reading `total_tokens`, `total_cost`, `prompt_*` or `completion_*` from a runs query (no longer includes child runs; use the traces query and its aggregates), and catches of old exception classes.

List per language: current version, latest stable, guide minimum.

If you find more than about 20 call sites, propose splitting the work into separate PRs by area (one folder, service or package each), with the call-site count per PR, and ask which one to do first. Phase 3 then covers only the PR I pick.

Number every decision you need from me (1, 2, 3...), each with your proposed answer, so I can approve or reject them one by one (for example "1 yes, 2 no, 3 yes").

Then STOP and wait for my approval.

**Phase 3: migrate (after approval, only the scope and decisions I approved)**

1. Upgrade each LangSmith SDK in use to its latest stable release (and its lockfile: uv.lock/poetry.lock, package-lock/pnpm-lock/yarn.lock, go.sum, Gradle/Maven). The guide's minimum is only the floor. If the latest release breaks something unrelated to this migration, use the newest version that works, never below the minimum, and say why in the PR.
2. Migrate each call site from the table. The v2 queries take `project_ids` (UUIDs), not a project name. Resolve a plain project by name as the guide shows. If the project is an agent environment, an experiment or the workspace evaluators, propose resolving it with [https://docs.langchain.com/langsmith/resolve-an-agent](../../Debug/Viewing%20%26%20managing%20traces/Resolve%20an%20agent%20environment.md), and flag that it is beta and needs a newer SDK and server.
3. Run tests, linters and the build for every language touched. Re-run the phase 2 search and show it finds nothing, or explain each leftover.
4. Keep the changes local: commit them, do not push. Show me a summary: per file, what changed and why, plus anything left for review. Then STOP. Push and open a pull request only if I approve.

**Phase 4: feedback and follow-ups**

1. List the raw HTTP calls noted in phase 2 that could use an SDK method instead. For each, say what the SDK would bring to that call site, for example automatic pagination, retries with backoff on rate limits and server errors, typed parameters that catch field renames, deprecation warnings before an endpoint is removed, or config from the environment, plus anything else that applies to it. Then ask me if I want to switch them in a separate change. Skip this if there are none.
2. List anything the guide did not cover or got wrong, as a short note I can send to LangChain. Always end with this note, even if it is empty ("nothing to report").

**Rules**

* If the guide does not cover a call site or parameter, search the rest of the LangSmith docs first ([https://docs.langchain.com/langsmith](../../Overview/LangSmith%20Observability.md), including the API reference). Then ask me, and include a proposed replacement with the doc link that backs it, or say you found nothing. Never apply an uncovered change without my go.
* Do not call write endpoints or change LangSmith data while testing.
* Never push a branch, open a pull request or post anything to GitHub without my go.

## Deprecation and removal

Each SDK method and its underlying endpoint share the same deprecation date.

| Deployment | Deprecation | Removal |
| - | - | - |
| All Cloud regions | End of July 2026 | 31 Jan 2027 |
| Self-Hosted | `v0.16` | `v0.19` |

For details on how LangSmith deprecates and removes API endpoints and SDK methods, see [API and SDK deprecation policy](../../../LangSmith%20setup/Cloud/Reference/API%20and%20SDK%20deprecation%20policy.md).

## Minimum SDK version

The new SDK methods are available starting at these SDK versions:

| Language | Package | Minimum version |
| - | - | - |
| Python | `langsmith` | `>=0.10.15` |
| TypeScript | `langsmith` | `>=0.8.9` |
| Java | `langsmith-java` | `0.1.0-beta.22` |
| Go | `langsmith-go` | `v0.25.4` |
| CLI | `langsmith-cli` | `v0.2.44` |

The [LangSmith CLI](../../../LangSmith%20setup/Govern/Tools/LangSmith%20CLI.md) queries the same SmithDB-backed endpoints and requires `v0.2.44` or later.

## About self-hosted

* The new methods documented in this guide require self-hosted version 0.16 or later, independent of the data store used.
* The deprecated methods stop working once ClickHouse is disabled.
* Where possible, the SDK raises a warning or error identifying the version to upgrade to, instead of failing without explanation.

## Methods by area

The before and after change for each method is documented on the page for its area.

> [card] [Query runs](Migrate%20run%20queries%20to%20SmithDB.md)
>
> Search the runs in a project: filters, field projection, sorting, and pagination. The largest surface area in the migration.

> [card] [Retrieve runs](Migrate%20run%20retrieval%20to%20SmithDB.md)
>
> Fetch one run by ID, load its child runs, and build the URL of a run in the LangSmith UI.

> [card] [Traces](Migrate%20trace%20methods%20to%20SmithDB.md)
>
> Query the traces in a project, read their token and cost aggregates, and list the runs that belong to one trace.

> [card] [Threads](Migrate%20thread%20methods%20to%20SmithDB.md)
>
> Query the threads in a project and list the traces (turns) that belong to one thread.

> [card] [Dataset experiment runs](Migrate%20dataset%20experiment%20runs%20to%20SmithDB.md)
>
> Query the runs recorded by an experiment on a dataset, including pagination and sorting by feedback score.

> [card] [Feedback and sharing](Migrate%20feedback%20and%20sharing%20methods%20to%20SmithDB.md)
>
> Create feedback on a run, add runs to an annotation queue, and share, unshare, or read publicly shared runs.

## Affected methods and endpoints

Every SDK method and API endpoint below is deprecated and stops working on the removal date above. Search your codebase for all of them. Endpoint paths are relative to `/api/v1`; the area pages have before/after examples for each one, except where noted.

### SDK methods

> [tab] Python
>
> Deprecated methods on `Client` and `AsyncClient`:
>
> | Deprecated | Replacement |
> | - | - |
> | `list_runs()` | `client.runs.query()` |
> | `read_run()` | `client.runs.retrieve()` |
> | `get_run_url()` | `client.runs.get_url()` |
> | `list_threads()` | `client.threads.query()` |
> | `read_thread()` | `client.threads.list_traces()` |
> | `share_run()` | `client.runs.share.create()` |
> | `unshare_run()` | `client.runs.share.delete()` |
> | `read_run_shared_link()`, `run_is_shared()` | `client.runs.retrieve(selects=["SHARE_URL"])` |
> | `list_shared_runs()` | `client.public.runs.query()` |
> | `read_shared_run()` | `client.public.runs.retrieve()` |
> | `get_experiment_results()` | `client.datasets.experiment_runs.query()` |
> | `add_runs_to_annotation_queue()` | `client.annotation_queues.items.create()` |
> | `list_runs_from_annotation_queue()`, `get_run_from_annotation_queue()` | `client.annotation_queues.items.list()` |
> | `delete_run_from_annotation_queue()` | `client.annotation_queues.items.delete_all()` |
> | `evaluate_run()`, `aevaluate_run()` | No replacement: run the evaluator yourself and log the result with `create_feedback()` |

> [tab] TypeScript
>
> Deprecated methods on `Client`:
>
> | Deprecated | Replacement |
> | - | - |
> | `listRuns()` | `client.runs.query()` |
> | `readRun()` | `client.runs.retrieve()` |
> | `getRunUrl()` | `client.runs.getURL()` |
> | `listThreads()`, `listGroupRuns()` | `client.threads.query()` |
> | `readThread()` | `client.threads.listTraces()` |
> | `shareRun()` | `client.runs.share.create()` |
> | `unshareRun()` | `client.runs.share.delete()` |
> | `readRunSharedLink()` | `client.runs.retrieve({ selects: ["SHARE_URL"] })` |
> | `listSharedRuns()` | `client.public.runs.query()` |
> | `addRunsToAnnotationQueue()` | `client.annotationQueues.items.create()` |
> | `listRunsFromAnnotationQueue()`, `getRunFromAnnotationQueue()` | `client.annotationQueues.items.list()` |
> | `deleteRunFromAnnotationQueue()` | `client.annotationQueues.items.deleteAll()` |
> | `getSizeFromAnnotationQueue()` | `client.annotationQueues.items.retrieveCount()` |

> [tab] Java
>
> | Deprecated | Replacement |
> | - | - |
> | `client.runs().query()`, `queryV1()` | `client.runs().queryV2()` |
> | `client.runs().retrieve()`, `retrieveV1()` | `client.runs().retrieveV2()` |
> | `client.datasets().runs().query()` | `client.datasets().experimentRuns().query()` |
> | `client.annotationQueues().runs().create()`, `createByKey()` | `client.annotationQueues().items().create()` |
> | `client.annotationQueues().runs().list()`, `client.annotationQueues().retrieveRun()` | `client.annotationQueues().items().list()` |
> | `client.annotationQueues().runs().update()` | `client.annotationQueues().items().update()` |
> | `client.annotationQueues().runs().deleteAll()`, `deleteQueue()` | `client.annotationQueues().items().deleteAll()` |
> | `client.annotationQueues().retrieveSize()`, `retrieveTotalSize()`, `retrieveTotalArchived()` | `client.annotationQueues().items().retrieveCount()` |
> | `client.annotationQueues().createRunStatus()` | `client.annotationQueues().items().createStatus()` |

> [tab] Go
>
> | Deprecated | Replacement |
> | - | - |
> | `client.Runs.Query()`, `QueryAutoPaging()`, `QueryV1()` | `client.Runs.QueryV2()` |
> | `client.Runs.Get()`, `GetV1()` | `client.Runs.GetV2()` |
> | `client.Datasets.Runs.Query()` | `client.Datasets.ExperimentRuns.Query()` |
> | `client.AnnotationQueues.Runs.New()`, `NewByKey()` | `client.AnnotationQueues.Items.New()` |
> | `client.AnnotationQueues.Runs.List()`, `client.AnnotationQueues.GetRun()` | `client.AnnotationQueues.Items.List()` |
> | `client.AnnotationQueues.Runs.Update()` | `client.AnnotationQueues.Items.Update()` |
> | `client.AnnotationQueues.Runs.DeleteAll()`, `DeleteQueue()` | `client.AnnotationQueues.Items.DeleteAll()` |
> | `client.AnnotationQueues.GetSize()`, `GetTotalSize()`, `GetTotalArchived()` | `client.AnnotationQueues.Items.GetCount()` |
> | `client.AnnotationQueues.NewRunStatus()` | `client.AnnotationQueues.Items.NewStatus()` |

### Endpoints

| Deprecated | Replacement | Area |
| - | - | - |
| `POST /runs/query` | `POST /api/v2/runs/query` | [Query runs](Migrate%20run%20queries%20to%20SmithDB.md) |
| `GET /runs/{run_id}` | `GET /api/v2/runs/{run_id}` | [Retrieve runs](Migrate%20run%20retrieval%20to%20SmithDB.md) |
| `POST /runs/group` | `POST /api/v2/threads/query` | [Threads](Migrate%20thread%20methods%20to%20SmithDB.md) |
| `GET /runs/{run_id}/share` | `GET /api/v2/runs/{run_id}?selects=SHARE_URL` | [Feedback and sharing](Migrate%20feedback%20and%20sharing%20methods%20to%20SmithDB.md) |
| `PUT /runs/{run_id}/share` | `POST /api/v2/runs/{run_id}/share` | [Feedback and sharing](Migrate%20feedback%20and%20sharing%20methods%20to%20SmithDB.md) |
| `DELETE /runs/{run_id}/share` | `DELETE /api/v2/runs/{trace_id}/share` (takes the trace ID) | [Feedback and sharing](Migrate%20feedback%20and%20sharing%20methods%20to%20SmithDB.md) |
| `POST /datasets/{dataset_id}/runs` | `POST /api/v2/datasets/{dataset_id}/experiment-runs` | [Dataset experiment runs](Migrate%20dataset%20experiment%20runs%20to%20SmithDB.md) |
| `GET /public/{share_token}/run/{run_id}` | `GET /api/v2/public/{share_token}/run/{run_id}` | [Feedback and sharing](Migrate%20feedback%20and%20sharing%20methods%20to%20SmithDB.md) |
| `POST /public/{share_token}/runs/query` | `POST /api/v2/public/{share_token}/runs/query` | [Feedback and sharing](Migrate%20feedback%20and%20sharing%20methods%20to%20SmithDB.md) |

The annotation queue run endpoints move to the queue items API under `/api/v1/platform/annotation-queues`. For adding runs to a queue, see [Annotation queues: add runs](Migrate%20feedback%20and%20sharing%20methods%20to%20SmithDB.md#annotation-queues-add-runs). For listing and counting queue items, see [Annotation queues: read runs](Migrate%20feedback%20and%20sharing%20methods%20to%20SmithDB.md#annotation-queues-read-runs). For the other endpoints, see the [API reference](https://docs.langchain.com/langsmith/smith-api) for request and response shapes.

| Deprecated (`/annotation-queues/...`) | Replacement (`/api/v1/platform/annotation-queues/...`) |
| - | - |
| `POST /{queue_id}/runs`, `POST /{queue_id}/runs/by-key` | `POST /{queue_id}/items` |
| `GET /{queue_id}/runs`, `GET /{queue_id}/run/{index}` | `GET /{queue_id}/items` |
| `GET /{queue_id}/runs/resolve/{queue_run_id}` | `GET /{queue_id}/items/{item_id}/placement` |
| `PATCH /{queue_id}/runs/{queue_run_id}` | `PATCH /{queue_id}/items/{item_id}` |
| `DELETE /{queue_id}/runs/{queue_run_id}`, `POST /{queue_id}/runs/delete` | `POST /{queue_id}/items/delete` |
| `GET /{queue_id}/size`, `GET /{queue_id}/total_size`, `GET /{queue_id}/total_archived` | `GET /{queue_id}/items/count` |
| `POST /status/{annotation_queue_run_id}` | `POST /items/{queue_item_id}/status` |

## Exceptions

> [tab] Python
>
> The SmithDB-backed methods raise new exception classes instead of the legacy `langsmith.utils` exception classes.
>
> | Before (`langsmith.utils`) | After (`langsmith`) | Notes |
> | - | - | - |
> | `LangSmithError` | `LangsmithError` | Base exception class for the SDK; casing changed |
> | `LangSmithAPIError` | `InternalServerError` | 5xx |
> | `LangSmithRequestTimeout` | `APITimeoutError` | Raised when a request times out |
> | `LangSmithUserError` | *(removed)* | No direct equivalent. The 403 org-scoped-key case now raises `PermissionDeniedError`; client-side argument validation now raises a standard `ValueError` or `TypeError` |
> | `LangSmithRateLimitError` | `RateLimitError` | 429; unchanged name |
> | `LangSmithAuthError` | `AuthenticationError` | 401 |
> | `LangSmithNotFoundError` | `NotFoundError` | 404; unchanged name |
> | `LangSmithConflictError` | `ConflictError` | 409; unchanged name |
> | `LangSmithConnectionError` | `APIConnectionError` | Raised when the client cannot connect to the API |
> | `LangSmithExceptionGroup` | *(removed)* | No equivalent |
> | *(not available)* | `APIError` | New: base class for all API-related errors, with `message`, `request`, and `body` attributes |
> | *(not available)* | `APIStatusError` | New: base class for all 4xx/5xx status errors |
> | *(not available)* | `BadRequestError` | New: 400 |
> | *(not available)* | `PermissionDeniedError` | New: 403 |
> | *(not available)* | `UnprocessableEntityError` | New: 422 |
> | *(not available)* | `APIResponseValidationError` | New: raised when a response does not match the expected schema |

> [tab] TypeScript
>
> The SmithDB-backed methods raise new exception classes instead of plain `Error`.
>
> | Before (plain `Error`) | After (`langsmith`) | Notes |
> | - | - | - |
> | *(not available)* | `LangsmithError` | base class for all SDK errors |
> | *(not available)* | `InternalServerError` | 5xx |
> | *(not available)* | `APIConnectionTimeoutError` | Raised when a request times out |
> | *(not available)* | `RateLimitError` | 429 |
> | *(not available)* | `AuthenticationError` | 401 |
> | *(not available)* | `NotFoundError` | 404 |
> | *(not available)* | `ConflictError` | 409 |
> | *(not available)* | `APIConnectionError` | Raised when the client cannot connect to the API |
> | *(not available)* | `APIError` | base class for all API-related errors, with `status`, `headers`, and `error` properties |
> | *(not available)* | `BadRequestError` | 400 |
> | *(not available)* | `PermissionDeniedError` | 403 |
> | *(not available)* | `UnprocessableEntityError` | 422 |
> | *(not available)* | `APIUserAbortError` | Raised when a request is aborted via an `AbortController` |

> [tab] Java
>
> No change. Error handling is unaffected by this migration.

> [tab] Go
>
> No change. Error handling is unaffected by this migration.

> [tab] cURL
>
> No change. Error handling is unaffected by this migration.

## Discontinued

The following methods are discontinued. They call the retired `/feedback/formulas` endpoints, which return `410 Gone` on composite-feedback v2 and are scheduled for removal on 2026-08-20. Composite scores are now managed as [composite evaluators](../../../Test/Evaluators/Evaluator%20types/UI/How%20to%20create%20a%20composite%20evaluator.md), which implement a composite score as a code evaluator plus a run rule. There is no SDK replacement.

### Feedback formula methods

| Python | TypeScript |
| - | - |
| [`list_feedback_formulas`](https://reference.langchain.com/python/langsmith/client/Client/list_feedback_formulas) | NA |
| [`get_feedback_formula_by_id`](https://reference.langchain.com/python/langsmith/client/Client/get_feedback_formula_by_id) | NA |
| [`create_feedback_formula`](https://reference.langchain.com/python/langsmith/client/Client/create_feedback_formula) | NA |
| [`update_feedback_formula`](https://reference.langchain.com/python/langsmith/client/Client/update_feedback_formula) | NA |
| [`delete_feedback_formula`](https://reference.langchain.com/python/langsmith/client/Client/delete_feedback_formula) | NA |

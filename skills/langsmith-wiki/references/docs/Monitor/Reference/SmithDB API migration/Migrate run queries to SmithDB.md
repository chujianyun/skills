# Migrate run queries to SmithDB

> Migrate the LangSmith SDK run query methods to their SmithDB-backed equivalents.

Run queries are the largest surface area in the migration, so they have their own page. For deprecation dates, minimum SDK versions, and the agent prompt that applies to every method, see [Migrate to SmithDB-backed APIs](Migrate%20to%20SmithDB-backed%20APIs.md).

## Runs: query

Query runs from a project with optional filtering and field projection. Returns a paginated result set.

### Main changes

#### Method name

> [tab] Python
>
> | Before | After |
> | - | - |
> | `client.list_runs()` | `client.runs.query()` (alias to `client.runs.query_v2()`) |
>
> > [!NOTE]
> >
> > `client.runs.query()` is now async. Call it with `await`.
>
> See the [reference](https://reference.langchain.com/python/langsmith/_openapi_client/resources/runs/RunsResource/query_v2) for the full parameter and field list.

> [tab] TypeScript
>
> | Before | After |
> | - | - |
> | `client.listRuns()` | `client.runs.query()` (alias to `client.runs.queryV2()`) |
>
> See the [reference](https://reference.langchain.com/javascript/langsmith/_openapi_client/Langsmith/Runs/queryV2) for the full parameter and field list.

> [tab] Java
>
> | Before | After |
> | - | - |
> | `client.runs().query()` | `client.runs().queryV2()` |
>
> See the [reference](https://javadoc.io/doc/com.langchain.smith/langsmith-java/latest/com/langchain/smith/services/blocking/RunService.html) for the full parameter list.

> [tab] Go
>
> | Before | After |
> | - | - |
> | `client.Runs.Query()` | `client.Runs.QueryV2()` |
>
> See the [reference](https://pkg.go.dev/github.com/langchain-ai/langsmith-go#RunService.QueryV2AutoPaging) for the full parameter list.

> [tab] cURL
>
> | Before | After |
> | - | - |
> | `POST /api/v1/runs/query` | `POST /api/v2/runs/query` |
>
> See the [API doc](../LangSmith%20REST%20API/Tracing/Query%20runs%20%28query-runs%29.md) for the full parameter and field list.

#### Query parameters

> [tab] Python
>
> > [!WARNING]
> >
> > `project_name` is not supported in `runs.query`. Pass `project_ids` with the project UUID instead. To look up a UUID by name, use `client.read_project(project_name="my-project")`, or `await client.aread_project(project_name="my-project")` in async code.
>
> > [!WARNING]
> >
> > `min_start_time` defaults to **1 day ago** when omitted. `list_runs` with no `start_time` returned all historical runs; `runs.query` without `min_start_time` silently scopes the query to the last 24 hours. Pass an explicit `min_start_time` if you need a wider window.
>
> | Before (`list_runs`) | After (`runs.query`) | Notes |
> | - | - | - |
> | `project_name` | *(removed)* | Use `project_ids` with UUID(s)—see warning above |
> | `project_id` | `project_ids` | Now takes a list; mutually exclusive with `reference_dataset_id` |
> | `run_type` | `run_type` | Values must now be uppercase: `"LLM"`, `"CHAIN"`, `"TOOL"`, `"RETRIEVER"`, `"EMBEDDING"`, `"PROMPT"`, `"PARSER"` |
> | `trace_id` | `trace_id` | Unchanged |
> | `reference_example_id` | `reference_examples` | Now takes a list of UUIDs |
> | `query` | *(removed)* | No equivalent |
> | `filter` | `filter` | Syntax unchanged |
> | `trace_filter` | `trace_filter` | Unchanged |
> | `tree_filter` | `tree_filter` | Unchanged |
> | `is_root` | `is_root` | Unchanged |
> | `parent_run_id` | *(removed)* | No equivalent |
> | `start_time` | `min_start_time` | Renamed; defaults to 1 day ago—see warning above |
> | `error` | `has_error` | Renamed |
> | `run_ids` | `ids` | Renamed |
> | `select` | `selects` | Field names are now uppercase (`"NAME"`, `"STATUS"`, etc.) |
> | `limit` | *(removed)* | Use `page_size` for per-request batch size |
> | *(not available)* | `max_start_time` | Upper bound for `start_time`; defaults to now |
> | *(not available)* | `page_size` | Per-request result count (default 100, max 1000) |
> | *(not available)* | `reference_dataset_id` | Alternative to `project_ids`; mutually exclusive |
> | *(not available)* | `cursor` | Pass `next_cursor` from previous response to fetch next page |

> [tab] TypeScript
>
> > [!WARNING]
> >
> > `projectName` is not supported in `client.runs.query`. Pass `project_ids` with the project UUID instead. To look up a UUID by name, use `client.readProject({ projectName: "my-project" })`.
>
> > [!WARNING]
> >
> > `min_start_time` defaults to **1 day ago** when omitted. `listRuns` with no `startTime` returned all historical runs; `client.runs.query` without `min_start_time` silently scopes the query to the last 24 hours. Pass an explicit `min_start_time` if you need a wider window.
>
> | Before (`listRuns`) | After (`client.runs.query`) | Notes |
> | - | - | - |
> | `projectName` | *(removed)* | Use `project_ids` with UUID(s)—see warning above |
> | `projectId` | `project_ids` | Renamed to `snake_case`; now takes a list; mutually exclusive with `reference_dataset_id` |
> | `runType` | `run_type` | Renamed to `snake_case`; values must now be uppercase: `"LLM"`, `"CHAIN"`, `"TOOL"`, `"RETRIEVER"`, `"EMBEDDING"`, `"PROMPT"`, `"PARSER"` |
> | `traceId` | `trace_id` | Renamed to `snake_case` |
> | `referenceExampleId` | `reference_examples` | Renamed to `snake_case`; now takes a list of UUIDs |
> | `query` | *(removed)* | No equivalent |
> | `filter` | `filter` | Syntax unchanged |
> | `traceFilter` | `trace_filter` | Renamed to `snake_case` |
> | `treeFilter` | `tree_filter` | Renamed to `snake_case` |
> | `isRoot` | `is_root` | Renamed to `snake_case` |
> | `parentRunId` | *(removed)* | No equivalent |
> | `startTime` | `min_start_time` | Renamed to `snake_case`; defaults to 1 day ago—see warning above |
> | `error` | `has_error` | Renamed |
> | `id` | `ids` | Renamed |
> | `select` | `selects` | Field names are now uppercase (`"NAME"`, `"STATUS"`, etc.) |
> | `limit` | *(removed)* | Use `page_size` for per-request batch size |
> | `order` | *(removed)* | No equivalent |
> | `executionOrder` | *(removed)* | No equivalent |
> | *(not available)* | `max_start_time` | Upper bound for `start_time`; defaults to now |
> | *(not available)* | `page_size` | Per-request result count (default 100, max 1000) |
> | *(not available)* | `reference_dataset_id` | Alternative to `project_ids`; mutually exclusive |
> | *(not available)* | `cursor` | Pass `next_cursor` from previous response to fetch next page |

> [tab] Java
>
> > [!WARNING]
> >
> > `minStartTime()` defaults to **1 day ago** when omitted. `query()` with no `startTime()` returned all historical runs; `queryV2()` without `minStartTime()` silently scopes the query to the last 24 hours. Pass an explicit `minStartTime()` if you need a wider window.
>
> | Before (`RunQueryParams`) | After (`RunQueryV2Params`) | Notes |
> | - | - | - |
> | `session()` | `projectIds()` | Renamed; now takes explicit project UUIDs |
> | `runType()` | `runType()` | Values must now be uppercase |
> | `trace()` | `traceId()` | Renamed |
> | `referenceExample()` | `referenceExamples()` | Renamed to plural |
> | `query()` | *(removed)* | No equivalent |
> | `filter()` | `filter()` | Syntax unchanged |
> | `traceFilter()` | `traceFilter()` | Unchanged |
> | `treeFilter()` | `treeFilter()` | Unchanged |
> | `isRoot()` | `isRoot()` | Unchanged |
> | `parentRun()` | *(removed)* | No equivalent |
> | `startTime()` | `minStartTime()` | Renamed; defaults to 1 day ago—see warning above |
> | `error()` | `hasError()` | Renamed |
> | `id()` | `ids()` | Renamed |
> | `select()` | `selects()` | Field names are now uppercase |
> | `limit()` | *(removed)* | Use `pageSize()` |
> | `order()` | *(removed)* | No equivalent |
> | `executionOrder()` | *(removed)* | No equivalent |
> | `cursor()` | `cursor()` | Unchanged |
> | *(not available)* | `maxStartTime()` | Upper bound for start time; defaults to now |
> | *(not available)* | `pageSize()` | Per-request result count (default 100, max 1000) |
> | *(not available)* | `referenceDatasetId()` | Alternative to `projectIds()` |

> [tab] Go
>
> > [!WARNING]
> >
> > `MinStartTime` defaults to **1 day ago** when omitted. `Query()` with no `StartTime` returned all historical runs; `QueryV2()` without `MinStartTime` silently scopes the query to the last 24 hours. Pass an explicit `MinStartTime` if you need a wider window.
>
> | Before (`RunQueryParams`) | After (`RunQueryV2Params`) | Notes |
> | - | - | - |
> | `Session` | `ProjectIDs` | Renamed; now takes explicit project UUIDs |
> | `RunType` | `RunType` | Values must now be uppercase: `RunQueryV2ParamsRunTypeLLM`, `RunQueryV2ParamsRunTypeChain`, etc. |
> | `Trace` | `TraceID` | Renamed |
> | `ReferenceExample` | `ReferenceExamples` | Renamed to plural |
> | `Query` | *(removed)* | No equivalent |
> | `Filter` | `Filter` | Unchanged |
> | `TraceFilter` | `TraceFilter` | Unchanged |
> | `TreeFilter` | `TreeFilter` | Unchanged |
> | `IsRoot` | `IsRoot` | Unchanged |
> | `ParentRun` | *(removed)* | No equivalent |
> | `StartTime` | `MinStartTime` | Renamed; defaults to 1 day ago—see warning above |
> | `Error` | `HasError` | Renamed |
> | `ID` | `IDs` | Renamed |
> | `Select` | `Selects` | Field name constants are now uppercase (e.g., `RunQueryV2ParamsSelectName`) |
> | `Limit` | *(removed)* | Use `PageSize` |
> | `Order` | *(removed)* | No equivalent |
> | `ExecutionOrder` | *(removed)* | No equivalent |
> | `Cursor` | `Cursor` | Unchanged |
> | *(not available)* | `MaxStartTime` | Upper bound for start time; defaults to now |
> | *(not available)* | `PageSize` | Per-request result count (default 100, max 1000) |
> | *(not available)* | `ReferenceDatasetID` | Alternative to `ProjectIDs` |

> [tab] cURL
>
> > [!WARNING]
> >
> > `min_start_time` defaults to **1 day ago** when omitted. `POST /api/v1/runs/query` with no `start_time` returned all historical runs; `POST /api/v2/runs/query` without `min_start_time` silently scopes the query to the last 24 hours. Pass an explicit `min_start_time` if you need a wider window.
>
> | Before (v1 `POST /api/v1/runs/query` body field) | After (v2 `POST /api/v2/runs/query` body field) | Notes |
> | - | - | - |
> | `session` | `project_ids` | Renamed; both take an array of project UUIDs. `project_ids` is mutually exclusive with `reference_dataset_id` |
> | `run_type` | `run_type` | Values must now be uppercase: `"LLM"`, `"CHAIN"`, `"TOOL"`, `"RETRIEVER"`, `"EMBEDDING"`, `"PROMPT"`, `"PARSER"` |
> | `trace` | `trace_id` | Renamed |
> | `reference_example` | `reference_examples` | Renamed to plural; now takes an array of UUIDs |
> | `query` | *(removed)* | No equivalent |
> | `filter` | `filter` | Syntax unchanged |
> | `trace_filter` | `trace_filter` | Unchanged |
> | `tree_filter` | `tree_filter` | Unchanged |
> | `is_root` | `is_root` | Unchanged |
> | `parent_run` | *(removed)* | No equivalent |
> | `start_time` | `min_start_time` | Renamed; defaults to 1 day ago—see warning above |
> | `error` | `has_error` | Renamed |
> | `id` | `ids` | Renamed to plural |
> | `select` | `selects` | Field names are now uppercase (`"NAME"`, `"STATUS"`, etc.) |
> | `limit` | *(removed)* | Use `page_size` for per-request batch size |
> | *(not available)* | `max_start_time` | Upper bound for `start_time`; defaults to now |
> | *(not available)* | `page_size` | Per-request result count (default 100, max 1000) |
> | *(not available)* | `reference_dataset_id` | Alternative to `project_ids`; mutually exclusive |
> | *(not available)* | `cursor` | Pass `next_cursor` from previous response to fetch next page |

#### Response fields

> [!WARNING]
>
> Token and cost fields no longer include child-run usage. In v1, each parent run, including the root run, carried the summed usage of the LLM runs beneath it. In v2, these fields report only the run's own usage. A root or chain run that made no model call of its own returns them empty (`None`, `null`, or omitted from the JSON), not the trace total.
>
> To read a trace's total tokens and cost, use [Traces: query](Migrate%20trace%20methods%20to%20SmithDB.md) and read `total_tokens` and `total_cost` from `trace_aggregates`. `trace_aggregates` has no prompt or completion split.

> [tab] Python
>
> Pass SCREAMING\_SNAKE\_CASE strings to `selects` (eg. `"ID"`, `"NAME"`, `"STATUS"`) to control which fields are populated on each `Run`; only selected fields are non-`None`. Default `selects` contains only `"ID"`.
>
> | Before (v1 `Run` attribute) | After (v2 `Run` attribute) | Notes |
> | - | - | - |
> | `run.id` | `run.id` | Unchanged; returned by default when `selects` is omitted |
> | `run.name` | `run.name` | Unchanged |
> | `run.run_type` | `run.run_type` | Values are now uppercase Literals: `"LLM"`, `"CHAIN"`, etc. |
> | `run.status` | `run.status` | Values: `"SUCCESS"`, `"ERROR"`, `"PENDING"` |
> | `run.start_time` | `run.start_time` | Unchanged |
> | `run.end_time` | `run.end_time` | Unchanged |
> | `run.error` | `run.error` | Unchanged |
> | `run.inputs` | `run.inputs` | Unchanged |
> | `run.outputs` | `run.outputs` | Unchanged |
> | `run.tags` | `run.tags` | Unchanged |
> | `run.extra` | `run.extra` | Unchanged |
> | `run.metadata` | `run.metadata` | Unchanged |
> | `run.events` | `run.events` | Unchanged |
> | `run.reference_example_id` | `run.reference_example_id` | Unchanged |
> | `run.trace_id` | `run.trace_id` | Unchanged |
> | `run.dotted_order` | `run.dotted_order` | Unchanged |
> | `run.parent_run_id` | *(removed)* | Use `run.parent_run_ids` (list of all ancestor UUIDs, root first) |
> | `run.parent_run_ids` | `run.parent_run_ids` | Unchanged |
> | `run.session_id` | `run.project_id` | Renamed; `session_id` was the project UUID |
> | `run.feedback_stats` | `run.feedback_stats` | Unchanged |
> | `run.app_path` | `run.app_path` | Unchanged |
> | `run.attachments` | `run.attachments` | v2 returns pre-signed download URLs instead of raw bytes |
> | `run.total_tokens` | `run.total_tokens` | Own usage only; no longer summed from child runs |
> | `run.prompt_tokens` | `run.prompt_tokens` | Own usage only; no longer summed from child runs |
> | `run.completion_tokens` | `run.completion_tokens` | Own usage only; no longer summed from child runs |
> | `run.total_cost` | `run.total_cost` | Own usage only; no longer summed from child runs |
> | `run.prompt_cost` | `run.prompt_cost` | Own usage only; no longer summed from child runs |
> | `run.completion_cost` | `run.completion_cost` | Own usage only; no longer summed from child runs |
> | `run.first_token_time` | `run.first_token_time` | Unchanged |
> | `run.latency` (property) | `run.latency_seconds` | Renamed; was a computed `timedelta` property, now a native `float` field |
> | `run.in_dataset` | `run.is_in_dataset` | Renamed |
> | `run.child_run_ids` | *(removed)* | No equivalent |
> | `run.child_runs` | *(removed)* | No equivalent |
> | `run.serialized` | *(removed)* | Use `run.manifest` |
> | `run.manifest_id` | *(removed)* | Use `run.manifest` |
> | *(not available)* | `run.is_root` | New |
> | *(not available)* | `run.manifest` | New: full manifest object (replaces `serialized` and `manifest_id`) |
> | *(not available)* | `run.error_preview` | New: truncated error snippet |
> | *(not available)* | `run.inputs_preview` | New: truncated inputs preview |
> | *(not available)* | `run.outputs_preview` | New: truncated outputs preview |
> | *(not available)* | `run.thread_id` | New: conversation thread UUID |
> | *(not available)* | `run.reference_dataset_id` | New: dataset UUID for the reference example |
> | *(not available)* | `run.share_url` | New: public share URL (only set when the run has been shared) |
> | `run.prompt_token_details` | `run.prompt_token_details.raw` | Field now wraps the dict; access `.raw` to get `dict[str, int]` (element type unchanged) |
> | `run.completion_token_details` | `run.completion_token_details.raw` | Field now wraps the dict; access `.raw` to get `dict[str, int]` (element type unchanged) |
> | `run.prompt_cost_details` | `run.prompt_cost_details.raw` | Field now wraps the dict; access `.raw` to get `dict[str, float]` (was `dict[str, Decimal]`) |
> | `run.completion_cost_details` | `run.completion_cost_details.raw` | Field now wraps the dict; access `.raw` to get `dict[str, float]` (was `dict[str, Decimal]`) |

> [tab] TypeScript
>
> Pass SCREAMING\_SNAKE\_CASE strings to `selects` (eg. `"ID"`, `"NAME"`, `"STATUS"`) to control which fields are populated on each `Run`. Default `selects` contains only `"ID"`.
>
> | Before (v1 `Run` property) | After (v2 `Run` property) | Notes |
> | - | - | - |
> | `run.id` | `run.id` | Unchanged |
> | `run.name` | `run.name` | Unchanged |
> | `run.runType` | `run.run_type` | Renamed to `snake_case`; values are now uppercase: `"LLM"`, `"CHAIN"`, etc. |
> | `run.status` | `run.status` | Values: `"SUCCESS"`, `"ERROR"`, `"PENDING"` |
> | `run.startTime` | `run.start_time` | Renamed to `snake_case` |
> | `run.endTime` | `run.end_time` | Renamed to `snake_case` |
> | `run.error` | `run.error` | Unchanged |
> | `run.inputs` | `run.inputs` | Unchanged |
> | `run.outputs` | `run.outputs` | Unchanged |
> | `run.tags` | `run.tags` | Unchanged |
> | `run.extra` | `run.extra` | Unchanged |
> | *(not available)* | `run.metadata` | New: previously accessed via `run.extra.metadata` |
> | `run.events` | `run.events` | Unchanged |
> | `run.referenceExampleId` | `run.reference_example_id` | Renamed to `snake_case` |
> | `run.traceId` | `run.trace_id` | Renamed to `snake_case` |
> | `run.dottedOrder` | `run.dotted_order` | Renamed to `snake_case` |
> | `run.parentRunId` | *(removed)* | Use `run.parent_run_ids` (list of all ancestor UUIDs, root first) |
> | `run.parentRunIds` | `run.parent_run_ids` | Renamed to `snake_case` |
> | `run.sessionId` | `run.project_id` | Renamed; `sessionId` was the project UUID |
> | `run.feedbackStats` | `run.feedback_stats` | Renamed to `snake_case` |
> | `run.appPath` | `run.app_path` | Renamed to `snake_case` |
> | `run.attachments` | `run.attachments` | v2 returns pre-signed download URLs instead of raw bytes |
> | `run.totalTokens` | `run.total_tokens` | Renamed to `snake_case`; own usage only; no longer summed from child runs |
> | `run.promptTokens` | `run.prompt_tokens` | Renamed to `snake_case`; own usage only; no longer summed from child runs |
> | `run.completionTokens` | `run.completion_tokens` | Renamed to `snake_case`; own usage only; no longer summed from child runs |
> | `run.totalCost` | `run.total_cost` | Renamed to `snake_case`; own usage only; no longer summed from child runs |
> | `run.promptCost` | `run.prompt_cost` | Renamed to `snake_case`; own usage only; no longer summed from child runs |
> | `run.completionCost` | `run.completion_cost` | Renamed to `snake_case`; own usage only; no longer summed from child runs |
> | `run.firstTokenTime` | `run.first_token_time` | Renamed to `snake_case` |
> | `run.latency` | `run.latency_seconds` | Renamed; was a computed property, now a native `number` field (seconds) |
> | `run.inDataset` | `run.is_in_dataset` | Renamed |
> | `run.childRunIds` | *(removed)* | No equivalent |
> | `run.childRuns` | *(removed)* | No equivalent |
> | `run.serialized` | *(removed)* | Use `run.manifest` |
> | `run.manifestId` | *(removed)* | Use `run.manifest` |
> | `run.shareToken` | *(removed)* | Use `run.share_url` (full URL, only set when the run has been shared) |
> | *(not available)* | `run.is_root` | New |
> | *(not available)* | `run.manifest` | New: full manifest object (replaces `serialized` and `manifestId`) |
> | *(not available)* | `run.error_preview` | New: truncated error snippet |
> | *(not available)* | `run.inputs_preview` | New: truncated inputs preview |
> | *(not available)* | `run.outputs_preview` | New: truncated outputs preview |
> | *(not available)* | `run.thread_id` | New: conversation thread UUID |
> | *(not available)* | `run.reference_dataset_id` | New: dataset UUID for the reference example |
> | *(not available)* | `run.share_url` | New: public share URL (only set when the run has been shared) |
> | *(not available)* | `run.prompt_token_details` | New: per-category prompt token breakdown |
> | *(not available)* | `run.completion_token_details` | New: per-category completion token breakdown |
> | *(not available)* | `run.prompt_cost_details` | New: per-category prompt cost breakdown |
> | *(not available)* | `run.completion_cost_details` | New: per-category completion cost breakdown |

> [tab] Java
>
> Add `RunQueryV2Params.Select` values (eg. `Select.NAME`, `Select.STATUS`) via `.addSelect(...)` to control which fields are populated; unselected fields return empty `Optional` values. `selects()` defaults to `ID` only.
>
> | Before (`RunSchema` method) | After (`Run` method) | Notes |
> | - | - | - |
> | `run.id()` | `run.id()` | Unchanged |
> | `run.name()` | `run.name()` | Unchanged |
> | `run.runType()` | `run.runType()` | Values are now uppercase: `"LLM"`, `"CHAIN"`, etc. |
> | `run.status()` | `run.status()` | Values: `"SUCCESS"`, `"ERROR"`, `"PENDING"` |
> | `run.startTime()` | `run.startTime()` | Unchanged |
> | `run.endTime()` | `run.endTime()` | Unchanged |
> | `run.error()` | `run.error()` | Unchanged |
> | `run.inputs()` | `run.inputs()` | Unchanged |
> | `run.outputs()` | `run.outputs()` | Unchanged |
> | `run.tags()` | `run.tags()` | Unchanged |
> | `run.extra()` | `run.extra()` | Unchanged |
> | `run.events()` | `run.events()` | Unchanged |
> | `run.feedbackStats()` | `run.feedbackStats()` | Unchanged |
> | `run.inputsPreview()` | `run.inputsPreview()` | Unchanged |
> | `run.outputsPreview()` | `run.outputsPreview()` | Unchanged |
> | `run.referenceExampleId()` | `run.referenceExampleId()` | Unchanged |
> | `run.traceId()` | `run.traceId()` | Unchanged |
> | `run.dottedOrder()` | `run.dottedOrder()` | Unchanged |
> | `run.parentRunId()` | *(removed)* | Use `run.parentRunIds()` (list of all ancestor UUIDs, root first) |
> | `run.parentRunIds()` | `run.parentRunIds()` | Unchanged |
> | `run.sessionId()` | `run.projectId()` | Renamed; `sessionId()` returned the project UUID |
> | `run.appPath()` | `run.appPath()` | Unchanged |
> | `run.firstTokenTime()` | `run.firstTokenTime()` | Unchanged |
> | `run.totalTokens()` | `run.totalTokens()` | Own usage only; no longer summed from child runs |
> | `run.promptTokens()` | `run.promptTokens()` | Own usage only; no longer summed from child runs |
> | `run.completionTokens()` | `run.completionTokens()` | Own usage only; no longer summed from child runs |
> | `run.totalCost()` | `run.totalCost()` | Return type changed from `Optional<String>` to `Optional<Double>`; own usage only; no longer summed from child runs |
> | `run.promptCost()` | `run.promptCost()` | Return type changed from `Optional<String>` to `Optional<Double>`; own usage only; no longer summed from child runs |
> | `run.completionCost()` | `run.completionCost()` | Return type changed from `Optional<String>` to `Optional<Double>`; own usage only; no longer summed from child runs |
> | `run.promptTokenDetails()` | `run.promptTokenDetails()` | Unchanged |
> | `run.completionTokenDetails()` | `run.completionTokenDetails()` | Unchanged |
> | `run.promptCostDetails()` | `run.promptCostDetails()` | Unchanged |
> | `run.completionCostDetails()` | `run.completionCostDetails()` | Unchanged |
> | `run.priceModelId()` | `run.priceModelId()` | Unchanged |
> | `run.inDataset()` | `run.isInDataset()` | Renamed |
> | `run.referenceDatasetId()` | `run.referenceDatasetId()` | Unchanged |
> | `run.threadId()` | `run.threadId()` | Unchanged |
> | `run.shareToken()` | *(removed)* | Use `run.shareUrl()` (full URL, only set when the run has been shared) |
> | `run.childRunIds()` | *(removed)* | No equivalent |
> | `run.directChildRunIds()` | *(removed)* | No equivalent |
> | `run.serialized()` | *(removed)* | Use `run.manifest()` |
> | `run.manifestId()` | *(removed)* | Use `run.manifest()` |
> | `run.messages()` | *(removed)* | No equivalent |
> | `run.executionOrder()` | *(removed)* | No equivalent |
> | `run.lastQueuedAt()` | *(removed)* | No equivalent |
> | `run.traceFirstReceivedAt()` | *(removed)* | No equivalent |
> | `run.traceMaxStartTime()` | *(removed)* | No equivalent |
> | `run.traceMinStartTime()` | *(removed)* | No equivalent |
> | `run.traceTier()` | *(removed)* | No equivalent |
> | `run.traceUpgrade()` | *(removed)* | No equivalent |
> | `run.ttlSeconds()` | *(removed)* | No equivalent |
> | *(not available)* | `run.attachments()` | New: pre-signed download URLs for attachments (replaces S3 URL fields) |
> | *(not available)* | `run.latencySeconds()` | New: wall-clock duration in seconds |
> | *(not available)* | `run.isRoot()` | New |
> | *(not available)* | `run.errorPreview()` | New: truncated error snippet |
> | *(not available)* | `run.manifest()` | New: full manifest, typed as `Optional<Manifest>` (replaces `serialized()` and `manifestId()`) |
> | *(not available)* | `run.metadata()` | New: metadata, typed as `Optional<Metadata>` (was derived from `extra.metadata`) |
> | *(not available)* | `run.shareUrl()` | New: public share URL (only set when the run has been shared) |
> | *(not available)* | `run.threadEvaluationTime()` | New |

> [tab] Go
>
> Pass `RunQueryV2ParamsSelect` constants (eg. `RunQueryV2ParamsSelectName`, `RunQueryV2ParamsSelectStatus`) to `Selects` to control which fields are populated; unselected fields are zero-valued on the returned struct. `Selects` defaults to `ID` only.
>
> | Before (`RunSchema` field) | After (`Run` field) | Notes |
> | - | - | - |
> | `run.ID` | `run.ID` | Unchanged |
> | `run.Name` | `run.Name` | Unchanged |
> | `run.RunType` | `run.RunType` | Values changed to uppercase: `"LLM"`, `"CHAIN"`, etc. |
> | `run.Status` | `run.Status` | Values: `"SUCCESS"`, `"ERROR"`, `"PENDING"` |
> | `run.TraceID` | `run.TraceID` | Unchanged |
> | `run.DottedOrder` | `run.DottedOrder` | Unchanged |
> | `run.AppPath` | `run.AppPath` | Unchanged |
> | `run.StartTime` | `run.StartTime` | Unchanged |
> | `run.EndTime` | `run.EndTime` | Unchanged |
> | `run.Error` | `run.Error` | Unchanged |
> | `run.Events` | `run.Events` | Unchanged; element type is now `RunEvent` (was `map[string]interface{}`) |
> | `run.Extra` | `run.Extra` | Unchanged; type is now `interface{}` (was `map[string]interface{}`) |
> | `run.FeedbackStats` | `run.FeedbackStats` | Unchanged; element type is now `RunFeedbackStat` |
> | `run.FirstTokenTime` | `run.FirstTokenTime` | Unchanged |
> | `run.Inputs` | `run.Inputs` | Unchanged; type is now `interface{}` (was `map[string]interface{}`) |
> | `run.InputsPreview` | `run.InputsPreview` | Unchanged |
> | `run.Outputs` | `run.Outputs` | Unchanged; type is now `interface{}` (was `map[string]interface{}`) |
> | `run.OutputsPreview` | `run.OutputsPreview` | Unchanged |
> | `run.ParentRunIDs` | `run.ParentRunIDs` | Unchanged |
> | `run.PriceModelID` | `run.PriceModelID` | Unchanged |
> | `run.PromptCost` | `run.PromptCost` | Own usage only; no longer summed from child runs |
> | `run.PromptCostDetails` | `run.PromptCostDetails.Raw` | Field now wraps the map; access `.Raw` to get `map[string]float64` (was `map[string]string`) |
> | `run.PromptTokenDetails` | `run.PromptTokenDetails.Raw` | Field now wraps the map; access `.Raw` to get `map[string]int64` (element type unchanged) |
> | `run.PromptTokens` | `run.PromptTokens` | Own usage only; no longer summed from child runs |
> | `run.CompletionCost` | `run.CompletionCost` | Own usage only; no longer summed from child runs |
> | `run.CompletionCostDetails` | `run.CompletionCostDetails.Raw` | Field now wraps the map; access `.Raw` to get `map[string]float64` (was `map[string]string`) |
> | `run.CompletionTokenDetails` | `run.CompletionTokenDetails.Raw` | Field now wraps the map; access `.Raw` to get `map[string]int64` (element type unchanged) |
> | `run.CompletionTokens` | `run.CompletionTokens` | Own usage only; no longer summed from child runs |
> | `run.TotalCost` | `run.TotalCost` | Own usage only; no longer summed from child runs |
> | `run.TotalTokens` | `run.TotalTokens` | Own usage only; no longer summed from child runs |
> | `run.ReferenceDatasetID` | `run.ReferenceDatasetID` | Unchanged |
> | `run.ReferenceExampleID` | `run.ReferenceExampleID` | Unchanged |
> | `run.Tags` | `run.Tags` | Unchanged |
> | `run.ThreadID` | `run.ThreadID` | Unchanged |
> | `run.SessionID` | `run.ProjectID` | Renamed |
> | `run.InDataset` | `run.IsInDataset` | Renamed |
> | `run.ChildRunIDs` | *(removed)* | No equivalent |
> | `run.DirectChildRunIDs` | *(removed)* | No equivalent |
> | `run.ExecutionOrder` | *(removed)* | No equivalent |
> | `run.InputsS3URLs` | *(removed)* | Internal storage URL; not exposed in v2 |
> | `run.LastQueuedAt` | *(removed)* | No equivalent |
> | `run.ManifestID` | *(removed)* | Use `run.Manifest` |
> | `run.ManifestS3ID` | *(removed)* | Internal storage URL; not exposed in v2 |
> | `run.Messages` | *(removed)* | No equivalent |
> | `run.OutputsS3URLs` | *(removed)* | Internal storage URL; not exposed in v2 |
> | `run.ParentRunID` | *(removed)* | Use `run.ParentRunIDs` |
> | `run.S3URLs` | *(removed)* | Internal storage URL; not exposed in v2 |
> | `run.Serialized` | *(removed)* | Use `run.Manifest` |
> | `run.ShareToken` | *(removed)* | Use `run.ShareURL` |
> | `run.TraceFirstReceivedAt` | *(removed)* | No equivalent |
> | `run.TraceMaxStartTime` | *(removed)* | No equivalent |
> | `run.TraceMinStartTime` | *(removed)* | No equivalent |
> | `run.TraceTier` | *(removed)* | No equivalent |
> | `run.TraceUpgrade` | *(removed)* | No equivalent |
> | `run.TtlSeconds` | *(removed)* | No equivalent |
> | *(not available)* | `run.Attachments` | New: maps attachment filename to pre-signed download URL |
> | *(not available)* | `run.ErrorPreview` | New: truncated error snippet |
> | *(not available)* | `run.IsRoot` | New |
> | *(not available)* | `run.LatencySeconds` | New: wall-clock duration in seconds |
> | *(not available)* | `run.Manifest` | New: full manifest object (replaces `Serialized` and `ManifestID`) |
> | *(not available)* | `run.Metadata` | New: arbitrary user-defined JSON metadata |
> | *(not available)* | `run.ShareURL` | New: public share URL (only set when the run has been shared) |
> | *(not available)* | `run.ThreadEvaluationTime` | New |

> [tab] cURL
>
> Field names in the JSON response use `snake_case`.
>
> Pass SCREAMING\_SNAKE\_CASE strings in the `selects` JSON array (eg. `"ID"`, `"NAME"`, `"STATUS"`) to control which fields are populated. Default `selects` contains only `"ID"`.
>
> | Before (v1 response field) | After (v2 response field) | Notes |
> | - | - | - |
> | `id` | `id` | Unchanged |
> | `name` | `name` | Unchanged |
> | `run_type` | `run_type` | Values changed to uppercase: `"LLM"`, `"CHAIN"`, etc. |
> | `status` | `status` | Values: `"SUCCESS"`, `"ERROR"`, `"PENDING"` |
> | `trace_id` | `trace_id` | Unchanged |
> | `dotted_order` | `dotted_order` | Unchanged |
> | `app_path` | `app_path` | Unchanged |
> | `start_time` | `start_time` | Unchanged |
> | `end_time` | `end_time` | Unchanged |
> | `error` | `error` | Unchanged |
> | `events` | `events` | Unchanged |
> | `extra` | `extra` | Unchanged |
> | `feedback_stats` | `feedback_stats` | Unchanged |
> | `first_token_time` | `first_token_time` | Unchanged |
> | `inputs` | `inputs` | Unchanged |
> | `inputs_preview` | `inputs_preview` | Unchanged |
> | `outputs` | `outputs` | Unchanged |
> | `outputs_preview` | `outputs_preview` | Unchanged |
> | `parent_run_ids` | `parent_run_ids` | Unchanged |
> | `price_model_id` | `price_model_id` | Unchanged |
> | `prompt_cost` | `prompt_cost` | Own usage only; no longer summed from child runs |
> | `prompt_cost_details` | `prompt_cost_details.raw` | Field now wraps the object; read `.raw` for the same `{category: cost}` mapping, now with numeric values (was strings) |
> | `prompt_token_details` | `prompt_token_details.raw` | Field now wraps the object; read `.raw` for the same `{category: count}` mapping (values unchanged) |
> | `prompt_tokens` | `prompt_tokens` | Own usage only; no longer summed from child runs |
> | `completion_cost` | `completion_cost` | Own usage only; no longer summed from child runs |
> | `completion_cost_details` | `completion_cost_details.raw` | Field now wraps the object; read `.raw` for the same `{category: cost}` mapping, now with numeric values (was strings) |
> | `completion_token_details` | `completion_token_details.raw` | Field now wraps the object; read `.raw` for the same `{category: count}` mapping (values unchanged) |
> | `completion_tokens` | `completion_tokens` | Own usage only; no longer summed from child runs |
> | `total_cost` | `total_cost` | Own usage only; no longer summed from child runs |
> | `total_tokens` | `total_tokens` | Own usage only; no longer summed from child runs |
> | `reference_dataset_id` | `reference_dataset_id` | Unchanged |
> | `reference_example_id` | `reference_example_id` | Unchanged |
> | `tags` | `tags` | Unchanged |
> | `thread_id` | `thread_id` | Unchanged |
> | `session_id` | `project_id` | Renamed |
> | `in_dataset` | `is_in_dataset` | Renamed |
> | `child_run_ids` | *(removed)* | No equivalent |
> | `direct_child_run_ids` | *(removed)* | No equivalent |
> | `execution_order` | *(removed)* | No equivalent |
> | `inputs_s3_urls` | *(removed)* | Internal storage URL; not exposed in v2 |
> | `last_queued_at` | *(removed)* | No equivalent |
> | `manifest_id` | *(removed)* | Use `manifest` |
> | `manifest_s3_id` | *(removed)* | Internal storage URL; not exposed in v2 |
> | `messages` | *(removed)* | No equivalent |
> | `outputs_s3_urls` | *(removed)* | Internal storage URL; not exposed in v2 |
> | `parent_run_id` | *(removed)* | Use `parent_run_ids` |
> | `s3_urls` | *(removed)* | Internal storage URL; not exposed in v2 |
> | `serialized` | *(removed)* | Use `manifest` |
> | `share_token` | *(removed)* | Use `share_url` |
> | `trace_first_received_at` | *(removed)* | No equivalent |
> | `trace_max_start_time` | *(removed)* | No equivalent |
> | `trace_min_start_time` | *(removed)* | No equivalent |
> | `trace_tier` | *(removed)* | No equivalent |
> | `trace_upgrade` | *(removed)* | No equivalent |
> | `ttl_seconds` | *(removed)* | No equivalent |
> | *(not available)* | `attachments` | New: maps attachment filename to pre-signed download URL |
> | *(not available)* | `error_preview` | New: truncated error snippet |
> | *(not available)* | `is_root` | New |
> | *(not available)* | `latency_seconds` | New: wall-clock duration in seconds |
> | *(not available)* | `manifest` | New: full manifest object (replaces `serialized` and `manifest_id`) |
> | *(not available)* | `metadata` | New: previously nested under `extra.metadata` |
> | *(not available)* | `share_url` | New: public share URL (only set when the run has been shared) |
> | *(not available)* | `thread_evaluation_time` | New |

#### Rate limiting

The SmithDB-backed method has a dedicated, higher rate limit than the method it replaces. Limits apply in Cloud, per API key.

> [tab] Python
>
> | | Before (`client.list_runs()`) | After (`client.runs.query()`) |
> | - | - | - |
> | Limit | 10 requests per 10 seconds | 300 requests per 10 seconds |

> [tab] TypeScript
>
> | | Before (`client.listRuns()`) | After (`client.runs.query()`) |
> | - | - | - |
> | Limit | 10 requests per 10 seconds | 300 requests per 10 seconds |

> [tab] Java
>
> | | Before (`client.runs().query()`) | After (`client.runs().queryV2()`) |
> | - | - | - |
> | Limit | 10 requests per 10 seconds | 300 requests per 10 seconds |

> [tab] Go
>
> | | Before (`client.Runs.Query()`) | After (`client.Runs.QueryV2()`) |
> | - | - | - |
> | Limit | 10 requests per 10 seconds | 300 requests per 10 seconds |

> [tab] cURL
>
> | | Before (`POST /api/v1/runs/query`) | After (`POST /api/v2/runs/query`) |
> | - | - | - |
> | Limit | 10 requests per 10 seconds | 300 requests per 10 seconds |

The deprecated method is also subject to per-tenant limits that vary by query shape, described in [Query traces using the SDK](../../Debug/Viewing%20%26%20managing%20traces/Query%20traces%20using%20the%20SDK.md#rate-limits). The SmithDB-backed method is not subject to those per-tenant limits.

Requests that exceed a limit return `429 Too Many Requests`. For general rate limit information, see [Usage and billing](../../Trace/Configuration%20%26%20troubleshooting/Usage%20and%20billing.md#rate-limits).

### Examples

#### List all runs in a project

> [tab] Python
>
> `runs.query` does not accept a project name directly. Resolve the project UUID with `client.aread_project()` first, then pass it as a string in `project_ids`.
>
> > [tab] Before
> >
> > ```python Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > from langsmith import Client
> >
> > client = Client()
> > runs = client.list_runs(project_name="default")
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
> >     runs = client.runs.query(project_ids=[str(project.id)])
> >
> >
> > asyncio.run(main())
> > ```

> [tab] TypeScript
>
> `client.runs.query` does not accept a project name directly. Resolve the project UUID with `client.readProject()` first, then pass it as a string in `project_ids`.
>
> > [tab] Before
> >
> > ```ts Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import { Client } from "langsmith";
> >
> > const client = new Client();
> > const runs = client.listRuns({ projectName: "default" });
> > ```
>
> > [tab] After
> >
> > ```ts After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import { Client } from "langsmith";
> >
> > const client = new Client();
> > const project = await client.readProject({ projectName: "default" });
> > const runs = client.runs.query({ project_ids: [project.id] });
> > ```

> [tab] Java
>
> `queryV2()` does not accept a project name directly. Resolve the project UUID with `client.sessions().list()` first, then pass it as a string in `projectIds()`.
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
> > val runs = client.runs().query(
> >     RunQueryParams.builder().addSession(project.id()).build()
> > ).items()
> > ```
>
> > [tab] After
> >
> > ```kotlin After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import com.langchain.smith.client.LangsmithClient
> > import com.langchain.smith.client.okhttp.LangsmithOkHttpClient
> > import com.langchain.smith.models.runs.RunQueryV2Params
> > import com.langchain.smith.models.sessions.SessionListParams
> >
> > val client: LangsmithClient = LangsmithOkHttpClient.fromEnv()
> >
> > val project = client.sessions().list(
> >     SessionListParams.builder().name("default").limit(1L).build()
> > ).items().first()
> > val runs = client.runs().queryV2(
> >     RunQueryV2Params.builder().addProjectId(project.id()).build()
> > ).items()
> > ```

> [tab] Go
>
> `QueryV2()` does not accept a project name directly. Resolve the project UUID with `client.Sessions.List()` first, then pass it as a string in `ProjectIDs`.
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
> >
> > sessions, err := client.Sessions.List(ctx, langsmith.SessionListParams{
> > 	Name:  langsmith.F("default"),
> > 	Limit: langsmith.F(int64(1)),
> > })
> > project := sessions.Items[0]
> >
> > runs, err := client.Runs.Query(ctx, langsmith.RunQueryParams{
> > 	Session: langsmith.F([]string{project.ID}),
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
> >
> > sessions, err := client.Sessions.List(ctx, langsmith.SessionListParams{
> > 	Name:  langsmith.F("default"),
> > 	Limit: langsmith.F(int64(1)),
> > })
> > project := sessions.Items[0]
> >
> > runs, err := client.Runs.QueryV2(ctx, langsmith.RunQueryV2Params{
> > 	ProjectIDs: langsmith.F([]string{project.ID}),
> > })
> > ```

> [tab] cURL
>
> `POST /api/v2/runs/query` does not accept a project name directly. Resolve the project UUID with a `GET /api/v1/sessions` request first, then pass it as a string in `project_ids`. For an agent environment, an experiment, or the evaluators, [resolve it](../../Debug/Viewing%20%26%20managing%20traces/Resolve%20an%20agent%20environment.md), which is in beta, to get the project UUID.
>
> > [tab] Before
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > PROJECT_ID=$(curl -s "https://api.smith.langchain.com/api/v1/sessions?name=default&limit=1" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" | jq -r '.[0].id')
> >
> > curl -X POST "https://api.smith.langchain.com/api/v1/runs/query" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" \
> >   -H "Content-Type: application/json" \
> >   -d "$(jq -n --arg pid "$PROJECT_ID" '{"session": [$pid]}')"
> > ```
>
> > [tab] After
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > PROJECT_ID=$(curl -s "https://api.smith.langchain.com/api/v1/sessions?name=default&limit=1" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" | jq -r '.[0].id')
> >
> > curl -X POST "https://api.smith.langchain.com/api/v2/runs/query" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" \
> >   -H "Content-Type: application/json" \
> >   -d "$(jq -n --arg pid "$PROJECT_ID" '{"project_ids": [$pid]}')"
> > ```

#### Selecting fields

> [tab] Python
>
> `list_runs` returns a default set of fields with no selection needed. `runs.query` returns only `id` by default—pass `selects=[...]` to request more. Field names are now uppercase (`"name"` → `"NAME"`).
>
> > [tab] Before
> >
> > ```python Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > from langsmith import Client
> >
> > client = Client()
> > # returns a default set of fields; no explicit selection needed
> > runs = client.list_runs(project_name="default")
> > for run in runs:
> >     print(run.id, run.name, run.run_type, run.status, run.start_time, run.inputs, run.error)
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
> >     # must explicitly list every field needed; default returns only id
> >     async for run in client.runs.query(
> >         project_ids=[str(project.id)],
> >         selects=["ID", "NAME", "RUN_TYPE", "STATUS", "START_TIME", "INPUTS", "ERROR"],
> >     ):
> >         print(run.id, run.name, run.run_type, run.status, run.start_time, run.inputs, run.error)
> >
> >
> > asyncio.run(main())
> > ```

> [tab] TypeScript
>
> `listRuns` returns a default set of fields with no selection needed. `client.runs.query` returns only `id` by default—pass `selects: [...]` to request more. Field names are now uppercase (`"name"` → `"NAME"`).
>
> > [tab] Before
> >
> > ```ts Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import { Client } from "langsmith";
> >
> > const client = new Client();
> > // returns a default set of fields; no explicit selection needed
> > const runs = client.listRuns({ projectName: "default" });
> > for await (const run of runs) {
> >   console.log(run.id, run.name, run.run_type, run.status, run.start_time, run.inputs, run.error);
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
> > // must explicitly list every field needed; default returns only id
> > for await (const run of client.runs.query({
> >   project_ids: [project.id],
> >   selects: ["ID", "NAME", "RUN_TYPE", "STATUS", "START_TIME", "INPUTS", "ERROR"],
> > })) {
> >   console.log(run.id, run.name, run.run_type, run.status, run.start_time, run.inputs, run.error);
> > }
> > ```

> [tab] Java
>
> `query()` returns a default set of fields with no selection needed. `queryV2()` returns only `id` by default—call `.addSelect(RunQueryV2Params.Select.X)` for each field you need.
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
> > // returns a default set of fields; no explicit selection needed
> > val runs = client.runs().query(
> >     RunQueryParams.builder().addSession(project.id()).build()
> > ).items()
> > for (run in runs) {
> >     println("${run.id()} ${run.name()} ${run.runType()} ${run.status()} ${run.startTime()} ${run.inputs()} ${run.error()}")
> > }
> > ```
>
> > [tab] After
> >
> > ```kotlin After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import com.langchain.smith.client.LangsmithClient
> > import com.langchain.smith.client.okhttp.LangsmithOkHttpClient
> > import com.langchain.smith.models.runs.RunQueryV2Params
> > import com.langchain.smith.models.runs.RunSelectField
> > import com.langchain.smith.models.sessions.SessionListParams
> >
> > val client: LangsmithClient = LangsmithOkHttpClient.fromEnv()
> >
> > val project = client.sessions().list(
> >     SessionListParams.builder().name("default").limit(1L).build()
> > ).items().first()
> > // must explicitly list every field needed; default returns only id
> > val runs = client.runs().queryV2(
> >     RunQueryV2Params.builder()
> >         .addProjectId(project.id())
> >         .addSelect(RunSelectField.ID)
> >         .addSelect(RunSelectField.NAME)
> >         .addSelect(RunSelectField.RUN_TYPE)
> >         .addSelect(RunSelectField.STATUS)
> >         .addSelect(RunSelectField.START_TIME)
> >         .addSelect(RunSelectField.INPUTS)
> >         .addSelect(RunSelectField.ERROR)
> >         .build()
> > ).items()
> > for (run in runs) {
> >     println("${run.id()} ${run.name()} ${run.runType()} ${run.status()} ${run.startTime()} ${run.inputs()} ${run.error()}")
> > }
> > ```

> [tab] Go
>
> `Query` returns a default set of fields with no selection needed. `QueryV2` returns only `ID` by default—pass `Selects` with the uppercase field constants you need (e.g. `RunQueryV2ParamsSelectName`).
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
> > sessions, err := client.Sessions.List(ctx, langsmith.SessionListParams{
> > 	Name:  langsmith.F("default"),
> > 	Limit: langsmith.F(int64(1)),
> > })
> > project := sessions.Items[0]
> >
> > // returns a default set of fields; no explicit selection needed
> > runs, err := client.Runs.Query(ctx, langsmith.RunQueryParams{
> > 	Session: langsmith.F([]string{project.ID}),
> > })
> > for _, run := range runs.Runs {
> > 	fmt.Println(run.ID, run.Name, run.RunType, run.Status, run.StartTime, run.Inputs, run.Error)
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
> >
> > 	"github.com/langchain-ai/langsmith-go"
> > )
> >
> > ctx := context.Background()
> > client := langsmith.NewClient()
> >
> > sessions, err := client.Sessions.List(ctx, langsmith.SessionListParams{
> > 	Name:  langsmith.F("default"),
> > 	Limit: langsmith.F(int64(1)),
> > })
> > project := sessions.Items[0]
> >
> > // must explicitly list every field needed; default returns only id
> > runs, err := client.Runs.QueryV2(ctx, langsmith.RunQueryV2Params{
> > 	ProjectIDs: langsmith.F([]string{project.ID}),
> > 	Selects: langsmith.F([]langsmith.RunSelectField{
> > 		langsmith.RunSelectFieldID,
> > 		langsmith.RunSelectFieldName,
> > 		langsmith.RunSelectFieldRunType,
> > 		langsmith.RunSelectFieldStatus,
> > 		langsmith.RunSelectFieldStartTime,
> > 		langsmith.RunSelectFieldInputs,
> > 		langsmith.RunSelectFieldError,
> > 	}),
> > })
> > for _, run := range runs.Items {
> > 	fmt.Println(run.ID, run.Name, run.RunType, run.Status, run.StartTime, run.Inputs, run.Error)
> > }
> > ```

> [tab] cURL
>
> `POST /api/v1/runs/query` returns a default set of fields with no selection needed. `POST /api/v2/runs/query` returns only `id` by default—pass `selects` with the uppercase field names you need (e.g. `"NAME"`).
>
> > [tab] Before
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > PROJECT_ID=$(curl -s "https://api.smith.langchain.com/api/v1/sessions?name=default&limit=1" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" | jq -r '.[0].id')
> >
> > curl -X POST "https://api.smith.langchain.com/api/v1/runs/query" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" \
> >   -H "Content-Type: application/json" \
> >   -d "$(jq -n --arg pid "$PROJECT_ID" '{"session": [$pid]}')"
> > ```
>
> > [tab] After
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > PROJECT_ID=$(curl -s "https://api.smith.langchain.com/api/v1/sessions?name=default&limit=1" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" | jq -r '.[0].id')
> >
> > curl -X POST "https://api.smith.langchain.com/api/v2/runs/query" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" \
> >   -H "Content-Type: application/json" \
> >   -d "$(jq -n --arg pid "$PROJECT_ID" '{"project_ids": [$pid], "selects": ["ID", "NAME", "RUN_TYPE", "STATUS", "START_TIME", "INPUTS", "ERROR"]}')"
> > ```

#### Filter by run type and time range

> [tab] Python
>
> `start_time` is renamed to `min_start_time`, and `run_type` values are now uppercase (`"llm"` → `"LLM"`).
>
> > [tab] Before
> >
> > ```python Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > from datetime import datetime, timedelta
> >
> > from langsmith import Client
> >
> > client = Client()
> > runs = client.list_runs(
> >     project_name="default",
> >     start_time=datetime.now() - timedelta(days=1),
> >     run_type="llm",
> > )
> > ```
>
> > [tab] After
> >
> > ```python After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import asyncio
> > from datetime import datetime, timedelta
> >
> > from langsmith import Client
> >
> >
> > async def main():
> >     client = Client()
> >     project = await client.aread_project(project_name="default")
> >     runs = client.runs.query(
> >         project_ids=[str(project.id)],
> >         min_start_time=datetime.now() - timedelta(days=1),
> >         run_type="LLM",
> >     )
> >
> >
> > asyncio.run(main())
> > ```

> [tab] TypeScript
>
> `startTime` (camelCase) becomes `min_start_time` (snake\_case, matching the v2 request body), and `runType` values are now uppercase (`"llm"` → `"LLM"`).
>
> > [tab] Before
> >
> > ```ts Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import { Client } from "langsmith";
> >
> > const client = new Client();
> > const runs = client.listRuns({
> >   projectName: "default",
> >   startTime: new Date(Date.now() - 24 * 60 * 60 * 1000),
> >   runType: "llm",
> > });
> > ```
>
> > [tab] After
> >
> > ```ts After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import { Client } from "langsmith";
> >
> > const client = new Client();
> > const project = await client.readProject({ projectName: "default" });
> > const oneDayAgo = new Date(Date.now() - 24 * 60 * 60 * 1000);
> > const runs = client.runs.query({
> >   project_ids: [project.id],
> >   min_start_time: oneDayAgo.toISOString(),
> >   run_type: "LLM",
> > });
> > ```

> [tab] Java
>
> `.startTime()` is renamed to `.minStartTime()`, and `.runType()` now takes the new `RunQueryV2Params.RunType` enum instead of `RunTypeEnum`.
>
> > [tab] Before
> >
> > ```kotlin Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import java.time.OffsetDateTime
> >
> > import com.langchain.smith.client.LangsmithClient
> > import com.langchain.smith.client.okhttp.LangsmithOkHttpClient
> > import com.langchain.smith.models.runs.RunQueryParams
> > import com.langchain.smith.models.runs.RunTypeEnum
> > import com.langchain.smith.models.sessions.SessionListParams
> >
> > val client: LangsmithClient = LangsmithOkHttpClient.fromEnv()
> >
> > val project = client.sessions().list(
> >     SessionListParams.builder().name("default").limit(1L).build()
> > ).items().first()
> > val runs = client.runs().query(
> >     RunQueryParams.builder()
> >         .addSession(project.id())
> >         .startTime(OffsetDateTime.now().minusDays(1))
> >         .runType(RunTypeEnum.LLM)
> >         .build()
> > ).items()
> > ```
>
> > [tab] After
> >
> > ```kotlin After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import java.time.OffsetDateTime
> >
> > import com.langchain.smith.client.LangsmithClient
> > import com.langchain.smith.client.okhttp.LangsmithOkHttpClient
> > import com.langchain.smith.models.runs.RunQueryV2Params
> > import com.langchain.smith.models.runs.RunType
> > import com.langchain.smith.models.sessions.SessionListParams
> >
> > val client: LangsmithClient = LangsmithOkHttpClient.fromEnv()
> >
> > val project = client.sessions().list(
> >     SessionListParams.builder().name("default").limit(1L).build()
> > ).items().first()
> > val runs = client.runs().queryV2(
> >     RunQueryV2Params.builder()
> >         .addProjectId(project.id())
> >         .minStartTime(OffsetDateTime.now().minusDays(1))
> >         .runType(RunType.LLM)
> >         .build()
> > ).items()
> > ```

> [tab] Go
>
> `StartTime` is renamed to `MinStartTime`, and `RunType` now takes the new `RunQueryV2ParamsRunType` enum instead of `RunTypeEnum`.
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
> > sessions, err := client.Sessions.List(ctx, langsmith.SessionListParams{
> > 	Name:  langsmith.F("default"),
> > 	Limit: langsmith.F(int64(1)),
> > })
> > project := sessions.Items[0]
> >
> > runs, err := client.Runs.Query(ctx, langsmith.RunQueryParams{
> > 	Session:   langsmith.F([]string{project.ID}),
> > 	StartTime: langsmith.F(time.Now().Add(-24 * time.Hour)),
> > 	RunType:   langsmith.F(langsmith.RunTypeEnumLlm),
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
> > sessions, err := client.Sessions.List(ctx, langsmith.SessionListParams{
> > 	Name:  langsmith.F("default"),
> > 	Limit: langsmith.F(int64(1)),
> > })
> > project := sessions.Items[0]
> >
> > runs, err := client.Runs.QueryV2(ctx, langsmith.RunQueryV2Params{
> > 	ProjectIDs:   langsmith.F([]string{project.ID}),
> > 	MinStartTime: langsmith.F(time.Now().Add(-24 * time.Hour)),
> > 	RunType:      langsmith.F(langsmith.RunTypeLlm),
> > })
> > ```

> [tab] cURL
>
> `start_time` is renamed to `min_start_time`, and `run_type` values are now uppercase (`"llm"` → `"LLM"`).
>
> > [tab] Before
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > PROJECT_ID=$(curl -s "https://api.smith.langchain.com/api/v1/sessions?name=default&limit=1" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" | jq -r '.[0].id')
> >
> > curl -X POST "https://api.smith.langchain.com/api/v1/runs/query" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" \
> >   -H "Content-Type: application/json" \
> >   -d "$(jq -n --arg pid "$PROJECT_ID" '{"session": [$pid], "run_type": "llm", "start_time": "2025-01-01T00:00:00Z"}')"
> > ```
>
> > [tab] After
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > PROJECT_ID=$(curl -s "https://api.smith.langchain.com/api/v1/sessions?name=default&limit=1" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" | jq -r '.[0].id')
> >
> > curl -X POST "https://api.smith.langchain.com/api/v2/runs/query" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" \
> >   -H "Content-Type: application/json" \
> >   -d "$(jq -n --arg pid "$PROJECT_ID" '{"project_ids": [$pid], "run_type": "LLM", "min_start_time": "2025-01-01T00:00:00Z"}')"
> > ```

#### Filter root runs only

> [tab] Python
>
> `is_root` is unchanged.
>
> > [tab] Before
> >
> > ```python Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > from langsmith import Client
> >
> > client = Client()
> > runs = client.list_runs(project_name="default", is_root=True)
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
> >     runs = client.runs.query(project_ids=[str(project.id)], is_root=True)
> >
> >
> > asyncio.run(main())
> > ```

> [tab] TypeScript
>
> `isRoot` (camelCase) becomes `is_root` (snake\_case, matching the v2 request body).
>
> > [tab] Before
> >
> > ```ts Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import { Client } from "langsmith";
> >
> > const client = new Client();
> > const runs = client.listRuns({ projectName: "default", isRoot: true });
> > ```
>
> > [tab] After
> >
> > ```ts After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import { Client } from "langsmith";
> >
> > const client = new Client();
> > const project = await client.readProject({ projectName: "default" });
> > const runs = client.runs.query({
> >   project_ids: [project.id],
> >   is_root: true,
> > });
> > ```

> [tab] Java
>
> `.isRoot()` is unchanged.
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
> > val runs = client.runs().query(
> >     RunQueryParams.builder().addSession(project.id()).isRoot(true).build()
> > ).items()
> > ```
>
> > [tab] After
> >
> > ```kotlin After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import com.langchain.smith.client.LangsmithClient
> > import com.langchain.smith.client.okhttp.LangsmithOkHttpClient
> > import com.langchain.smith.models.runs.RunQueryV2Params
> > import com.langchain.smith.models.sessions.SessionListParams
> >
> > val client: LangsmithClient = LangsmithOkHttpClient.fromEnv()
> >
> > val project = client.sessions().list(
> >     SessionListParams.builder().name("default").limit(1L).build()
> > ).items().first()
> > val runs = client.runs().queryV2(
> >     RunQueryV2Params.builder().addProjectId(project.id()).isRoot(true).build()
> > ).items()
> > ```

> [tab] Go
>
> `IsRoot` is unchanged.
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
> >
> > sessions, err := client.Sessions.List(ctx, langsmith.SessionListParams{
> > 	Name:  langsmith.F("default"),
> > 	Limit: langsmith.F(int64(1)),
> > })
> > project := sessions.Items[0]
> >
> > runs, err := client.Runs.Query(ctx, langsmith.RunQueryParams{
> > 	Session: langsmith.F([]string{project.ID}),
> > 	IsRoot:  langsmith.F(true),
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
> >
> > sessions, err := client.Sessions.List(ctx, langsmith.SessionListParams{
> > 	Name:  langsmith.F("default"),
> > 	Limit: langsmith.F(int64(1)),
> > })
> > project := sessions.Items[0]
> >
> > runs, err := client.Runs.QueryV2(ctx, langsmith.RunQueryV2Params{
> > 	ProjectIDs: langsmith.F([]string{project.ID}),
> > 	IsRoot:     langsmith.F(true),
> > })
> > ```

> [tab] cURL
>
> `is_root` is unchanged.
>
> > [tab] Before
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > PROJECT_ID=$(curl -s "https://api.smith.langchain.com/api/v1/sessions?name=default&limit=1" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" | jq -r '.[0].id')
> >
> > curl -X POST "https://api.smith.langchain.com/api/v1/runs/query" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" \
> >   -H "Content-Type: application/json" \
> >   -d "$(jq -n --arg pid "$PROJECT_ID" '{"session": [$pid], "is_root": true}')"
> > ```
>
> > [tab] After
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > PROJECT_ID=$(curl -s "https://api.smith.langchain.com/api/v1/sessions?name=default&limit=1" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" | jq -r '.[0].id')
> >
> > curl -X POST "https://api.smith.langchain.com/api/v2/runs/query" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" \
> >   -H "Content-Type: application/json" \
> >   -d "$(jq -n --arg pid "$PROJECT_ID" '{"project_ids": [$pid], "is_root": true}')"
> > ```

> [!WARNING]
>
> To list traces, use `traces.query` instead of `is_root=True`. Root runs from `runs.query` do not carry trace-wide token or cost totals: their token and cost fields cover only the root run's own usage, and are empty when the root made no model call. `traces.query` returns trace-wide `total_tokens` and `total_cost` under `trace_aggregates`. See [Traces: query](Migrate%20trace%20methods%20to%20SmithDB.md).

#### Fetch runs by ID list

> [tab] Python
>
> `id=[...]` is renamed to `ids=[...]`. `project_ids` is now required even when filtering by run IDs—v1 allowed omitting the project context.
>
> > [tab] Before
> >
> > ```python Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > from langsmith import Client
> >
> > client = Client()
> > runs = client.list_runs(id=["<run-id-1>", "<run-id-2>"])
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
> >     runs = client.runs.query(
> >         project_ids=[str(project.id)],
> >         ids=["<run-id-1>", "<run-id-2>"],
> >     )
> >
> >
> > asyncio.run(main())
> > ```

> [tab] TypeScript
>
> `id: [...]` is renamed to `ids: [...]`. `project_ids` is now required even when filtering by run IDs—v1 allowed omitting the project context.
>
> > [tab] Before
> >
> > ```ts Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import { Client } from "langsmith";
> >
> > const client = new Client();
> > const runs = client.listRuns({ id: ["<run-id-1>", "<run-id-2>"] });
> > ```
>
> > [tab] After
> >
> > ```ts After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import { Client } from "langsmith";
> >
> > const client = new Client();
> > const project = await client.readProject({ projectName: "default" });
> > const runs = client.runs.query({
> >   project_ids: [project.id],
> >   ids: ["<run-id-1>", "<run-id-2>"],
> > });
> > ```

> [tab] Java
>
> `.addId(...)` is unchanged—call it once per run ID. `.addProjectId(...)` is now required even when filtering by run IDs—v1 allowed omitting the project context.
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
> > var runId1 = "<run-id-1>"
> > var runId2 = "<run-id-2>"
> > val runs = client.runs().query(
> >     RunQueryParams.builder()
> >         .addSession(project.id())
> >         .addId(runId1)
> >         .addId(runId2)
> >         .build()
> > ).items()
> > ```
>
> > [tab] After
> >
> > ```kotlin After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import com.langchain.smith.client.LangsmithClient
> > import com.langchain.smith.client.okhttp.LangsmithOkHttpClient
> > import com.langchain.smith.models.runs.RunQueryV2Params
> > import com.langchain.smith.models.sessions.SessionListParams
> >
> > val client: LangsmithClient = LangsmithOkHttpClient.fromEnv()
> >
> > val project = client.sessions().list(
> >     SessionListParams.builder().name("default").limit(1L).build()
> > ).items().first()
> > val runs = client.runs().queryV2(
> >     RunQueryV2Params.builder()
> >         .addProjectId(project.id())
> >         .addId("<run-id-1>")
> >         .addId("<run-id-2>")
> >         .build()
> > ).items()
> > ```

> [tab] Go
>
> `ID: [...]` is renamed to `IDs: [...]`. `ProjectIDs` is now required even when filtering by run IDs—v1 allowed omitting the project context.
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
> >
> > sessions, err := client.Sessions.List(ctx, langsmith.SessionListParams{
> > 	Name:  langsmith.F("default"),
> > 	Limit: langsmith.F(int64(1)),
> > })
> > project := sessions.Items[0]
> >
> > runID1 := "<run-id-1>"
> > runID2 := "<run-id-2>"
> > runs, err := client.Runs.Query(ctx, langsmith.RunQueryParams{
> > 	Session: langsmith.F([]string{project.ID}),
> > 	ID:      langsmith.F([]string{runID1, runID2}),
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
> >
> > sessions, err := client.Sessions.List(ctx, langsmith.SessionListParams{
> > 	Name:  langsmith.F("default"),
> > 	Limit: langsmith.F(int64(1)),
> > })
> > project := sessions.Items[0]
> >
> > runID1 := "<run-id-1>"
> > runID2 := "<run-id-2>"
> > runs, err := client.Runs.QueryV2(ctx, langsmith.RunQueryV2Params{
> > 	ProjectIDs: langsmith.F([]string{project.ID}),
> > 	IDs:        langsmith.F([]string{runID1, runID2}),
> > })
> > ```

> [tab] cURL
>
> `id` is renamed to `ids`. `project_ids` is now required in the request body even when filtering by run IDs—v1 allowed omitting the project context.
>
> > [tab] Before
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > RUN_ID_1="<run-id-1>"
> > RUN_ID_2="<run-id-2>"
> >
> > curl -X POST "https://api.smith.langchain.com/api/v1/runs/query" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" \
> >   -H "Content-Type: application/json" \
> >   -d "$(jq -n --arg r1 "$RUN_ID_1" --arg r2 "$RUN_ID_2" '{"id": [$r1, $r2]}')"
> > ```
>
> > [tab] After
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > PROJECT_ID=$(curl -s "https://api.smith.langchain.com/api/v1/sessions?name=default&limit=1" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" | jq -r '.[0].id')
> >
> > RUN_ID_1="<run-id-1>"
> > RUN_ID_2="<run-id-2>"
> >
> > curl -X POST "https://api.smith.langchain.com/api/v2/runs/query" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" \
> >   -H "Content-Type: application/json" \
> >   -d "$(jq -n --arg pid "$PROJECT_ID" --arg r1 "$RUN_ID_1" --arg r2 "$RUN_ID_2" '{"project_ids": [$pid], "ids": [$r1, $r2]}')"
> > ```

#### Iterate through runs

> [tab] Python
>
> `list_runs` auto-paginates transparently, fetching up to 100 runs per API call and stopping once `limit` results are returned. `runs.query` does not accept a total `limit`; iterate with `async for` and `break` once you have enough, or use the returned page's `has_next_page()`/`get_next_page()` for manual page-by-page control.
>
> > [tab] Before
> >
> > ```python Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > from langsmith import Client
> >
> > client = Client()
> > runs = client.list_runs(project_name="default", limit=150)
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
> >     runs = []
> >     async for run in client.runs.query(
> >         project_ids=[str(project.id)],
> >     ):
> >         runs.append(run)
> >         if len(runs) >= 150:
> >             break
> >
> >
> > asyncio.run(main())
> > ```

> [tab] TypeScript
>
> `listRuns` auto-paginates transparently. `client.runs.query` returns an async iterable of individual runs—use `for await` and `break` once you have enough.
>
> > [tab] Before
> >
> > ```ts Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import { Client } from "langsmith";
> >
> > const client = new Client();
> > const runs: unknown[] = [];
> > for await (const run of client.listRuns({ projectName: "default" })) {
> >   runs.push(run);
> >   if (runs.length >= 150) break;
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
> > const runs: unknown[] = [];
> > for await (const run of client.runs.query({
> >   project_ids: [project.id],
> > })) {
> >   runs.push(run);
> >   if (runs.length >= 150) break;
> > }
> > ```

> [tab] Java
>
> `.autoPager()` is used the same way on both `query()` and `queryV2()`—break out of the loop once you have enough runs.
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
> > val runs = mutableListOf<Any>()
> > for (run in client.runs().query(
> >     RunQueryParams.builder().addSession(project.id()).build()
> > ).autoPager()) {
> >     runs.add(run)
> >     if (runs.size >= 150) break
> > }
> > ```
>
> > [tab] After
> >
> > ```kotlin After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import com.langchain.smith.client.LangsmithClient
> > import com.langchain.smith.client.okhttp.LangsmithOkHttpClient
> > import com.langchain.smith.models.runs.RunQueryV2Params
> > import com.langchain.smith.models.sessions.SessionListParams
> >
> > val client: LangsmithClient = LangsmithOkHttpClient.fromEnv()
> >
> > val project = client.sessions().list(
> >     SessionListParams.builder().name("default").limit(1L).build()
> > ).items().first()
> > val runs = mutableListOf<Any>()
> > for (run in client.runs().queryV2(
> >     RunQueryV2Params.builder().addProjectId(project.id()).build()
> > ).autoPager()) {
> >     runs.add(run)
> >     if (runs.size >= 150) break
> > }
> > ```

> [tab] Go
>
> `QueryAutoPaging` is renamed to `QueryV2AutoPaging`; both use the same `iter.Next()`/`iter.Current()` pattern—break out of the loop once you have enough runs.
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
> >
> > sessions, err := client.Sessions.List(ctx, langsmith.SessionListParams{
> > 	Name:  langsmith.F("default"),
> > 	Limit: langsmith.F(int64(1)),
> > })
> > project := sessions.Items[0]
> >
> > runs := []langsmith.RunSchema{}
> > iter := client.Runs.QueryAutoPaging(ctx, langsmith.RunQueryParams{
> > 	Session: langsmith.F([]string{project.ID}),
> > })
> > for iter.Next() {
> > 	runs = append(runs, iter.Current())
> > 	if len(runs) >= 150 {
> > 		break
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
> >
> > 	"github.com/langchain-ai/langsmith-go"
> > )
> >
> > ctx := context.Background()
> > client := langsmith.NewClient()
> >
> > sessions, err := client.Sessions.List(ctx, langsmith.SessionListParams{
> > 	Name:  langsmith.F("default"),
> > 	Limit: langsmith.F(int64(1)),
> > })
> > project := sessions.Items[0]
> >
> > runs := []langsmith.Run{}
> > iter := client.Runs.QueryV2AutoPaging(ctx, langsmith.RunQueryV2Params{
> > 	ProjectIDs: langsmith.F([]string{project.ID}),
> > })
> > for iter.Next() {
> > 	runs = append(runs, iter.Current())
> > 	if len(runs) >= 150 {
> > 		break
> > 	}
> > }
> > ```

> [tab] cURL
>
> The v1 API returns all matching runs in one response with no cursor. The v2 API paginates—pass the `cursor` from a response's `next_cursor` field to fetch the next page.
>
> > [tab] Before
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > PROJECT_ID=$(curl -s "https://api.smith.langchain.com/api/v1/sessions?name=default&limit=1" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" | jq -r '.[0].id')
> >
> > curl -X POST "https://api.smith.langchain.com/api/v1/runs/query" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" \
> >   -H "Content-Type: application/json" \
> >   -d "$(jq -n --arg pid "$PROJECT_ID" '{"session": [$pid], "limit": 150}')"
> > ```
>
> > [tab] After
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > PROJECT_ID=$(curl -s "https://api.smith.langchain.com/api/v1/sessions?name=default&limit=1" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" | jq -r '.[0].id')
> >
> > # Fetch pages, passing the cursor from each response's next_cursor field
> > # to fetch the next page, until 150 runs are collected or pages run out.
> > TOTAL=0
> > CURSOR=""
> > while :; do
> >   BODY=$(jq -n --arg pid "$PROJECT_ID" --arg cursor "$CURSOR" \
> >     'if $cursor == "" then {"project_ids": [$pid]} else {"project_ids": [$pid], "cursor": $cursor} end')
> >   RESPONSE=$(curl -s -X POST "https://api.smith.langchain.com/api/v2/runs/query" \
> >     -H "x-api-key: $LANGSMITH_API_KEY" \
> >     -H "Content-Type: application/json" \
> >     -d "$BODY")
> >   TOTAL=$((TOTAL + $(echo "$RESPONSE" | jq '.items | length')))
> >   CURSOR=$(echo "$RESPONSE" | jq -r '.next_cursor // empty')
> >   [ "$TOTAL" -lt 150 ] && [ -n "$CURSOR" ] || break
> > done
> > ```

#### Filter runs with errors

> [tab] Python
>
> `error=True/False` is renamed to `has_error=True/False`.
>
> > [tab] Before
> >
> > ```python Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > from langsmith import Client
> >
> > client = Client()
> > runs = client.list_runs(project_name="default", error=True)
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
> >     runs = client.runs.query(project_ids=[str(project.id)], has_error=True)
> >
> >
> > asyncio.run(main())
> > ```

> [tab] TypeScript
>
> `error: true/false` is renamed to `has_error: true/false`.
>
> > [tab] Before
> >
> > ```ts Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import { Client } from "langsmith";
> >
> > const client = new Client();
> > const runs = client.listRuns({ projectName: "default", error: true });
> > ```
>
> > [tab] After
> >
> > ```ts After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import { Client } from "langsmith";
> >
> > const client = new Client();
> > const project = await client.readProject({ projectName: "default" });
> > const runs = client.runs.query({
> >   project_ids: [project.id],
> >   has_error: true,
> > });
> > ```

> [tab] Java
>
> `.error(true/false)` is renamed to `.hasError(true/false)`.
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
> > val runs = client.runs().query(
> >     RunQueryParams.builder().addSession(project.id()).error(true).build()
> > ).items()
> > ```
>
> > [tab] After
> >
> > ```kotlin After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import com.langchain.smith.client.LangsmithClient
> > import com.langchain.smith.client.okhttp.LangsmithOkHttpClient
> > import com.langchain.smith.models.runs.RunQueryV2Params
> > import com.langchain.smith.models.sessions.SessionListParams
> >
> > val client: LangsmithClient = LangsmithOkHttpClient.fromEnv()
> >
> > val project = client.sessions().list(
> >     SessionListParams.builder().name("default").limit(1L).build()
> > ).items().first()
> > val runs = client.runs().queryV2(
> >     RunQueryV2Params.builder().addProjectId(project.id()).hasError(true).build()
> > ).items()
> > ```

> [tab] Go
>
> `Error` is renamed to `HasError`.
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
> >
> > sessions, err := client.Sessions.List(ctx, langsmith.SessionListParams{
> > 	Name:  langsmith.F("default"),
> > 	Limit: langsmith.F(int64(1)),
> > })
> > project := sessions.Items[0]
> >
> > runs, err := client.Runs.Query(ctx, langsmith.RunQueryParams{
> > 	Session: langsmith.F([]string{project.ID}),
> > 	Error:   langsmith.F(true),
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
> >
> > sessions, err := client.Sessions.List(ctx, langsmith.SessionListParams{
> > 	Name:  langsmith.F("default"),
> > 	Limit: langsmith.F(int64(1)),
> > })
> > project := sessions.Items[0]
> >
> > runs, err := client.Runs.QueryV2(ctx, langsmith.RunQueryV2Params{
> > 	ProjectIDs: langsmith.F([]string{project.ID}),
> > 	HasError:   langsmith.F(true),
> > })
> > ```

> [tab] cURL
>
> `error` is renamed to `has_error`.
>
> > [tab] Before
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > PROJECT_ID=$(curl -s "https://api.smith.langchain.com/api/v1/sessions?name=default&limit=1" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" | jq -r '.[0].id')
> >
> > curl -X POST "https://api.smith.langchain.com/api/v1/runs/query" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" \
> >   -H "Content-Type: application/json" \
> >   -d "$(jq -n --arg pid "$PROJECT_ID" '{"session": [$pid], "error": true}')"
> > ```
>
> > [tab] After
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > PROJECT_ID=$(curl -s "https://api.smith.langchain.com/api/v1/sessions?name=default&limit=1" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" | jq -r '.[0].id')
> >
> > curl -X POST "https://api.smith.langchain.com/api/v2/runs/query" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" \
> >   -H "Content-Type: application/json" \
> >   -d "$(jq -n --arg pid "$PROJECT_ID" '{"project_ids": [$pid], "has_error": true}')"
> > ```

#### Filter by metadata

> [tab] Python
>
> The `filter` string syntax is unchanged: `eq(metadata_key, ...)` checks for key presence, combined with `eq(metadata_value, ...)` to match a specific value.
>
> > [tab] Before
> >
> > ```python Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > from langsmith import Client
> >
> > client = Client()
> > filter_str = 'and(eq(metadata_key, "user_id"), eq(metadata_value, "u_123"))'
> > runs = client.list_runs(project_name="default", filter=filter_str)
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
> >     filter_str = 'and(eq(metadata_key, "user_id"), eq(metadata_value, "u_123"))'
> >     project = await client.aread_project(project_name="default")
> >     runs = client.runs.query(project_ids=[str(project.id)], filter=filter_str)
> >
> >
> > asyncio.run(main())
> > ```

> [tab] TypeScript
>
> The `filter` string syntax is unchanged: `eq(metadata_key, ...)` checks for key presence, combined with `eq(metadata_value, ...)` to match a specific value.
>
> > [tab] Before
> >
> > ```ts Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import { Client } from "langsmith";
> >
> > const client = new Client();
> > const filterStr = 'and(eq(metadata_key, "user_id"), eq(metadata_value, "u_123"))';
> > const runs = client.listRuns({ projectName: "default", filter: filterStr });
> > ```
>
> > [tab] After
> >
> > ```ts After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import { Client } from "langsmith";
> >
> > const client = new Client();
> > const filterStr = 'and(eq(metadata_key, "user_id"), eq(metadata_value, "u_123"))';
> > const project = await client.readProject({ projectName: "default" });
> > const runs = client.runs.query({
> >   project_ids: [project.id],
> >   filter: filterStr,
> > });
> > ```

> [tab] Java
>
> The `.filter(...)` string syntax is unchanged: `eq(metadata_key, ...)` checks for key presence, combined with `eq(metadata_value, ...)` to match a specific value.
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
> > val filterStr = "and(eq(metadata_key, \"user_id\"), eq(metadata_value, \"u_123\"))"
> > val runs = client.runs().query(
> >     RunQueryParams.builder().addSession(project.id()).filter(filterStr).build()
> > ).items()
> > ```
>
> > [tab] After
> >
> > ```kotlin After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import com.langchain.smith.client.LangsmithClient
> > import com.langchain.smith.client.okhttp.LangsmithOkHttpClient
> > import com.langchain.smith.models.runs.RunQueryV2Params
> > import com.langchain.smith.models.sessions.SessionListParams
> >
> > val client: LangsmithClient = LangsmithOkHttpClient.fromEnv()
> >
> > val project = client.sessions().list(
> >     SessionListParams.builder().name("default").limit(1L).build()
> > ).items().first()
> > val filterStr = "and(eq(metadata_key, \"user_id\"), eq(metadata_value, \"u_123\"))"
> > val runs = client.runs().queryV2(
> >     RunQueryV2Params.builder().addProjectId(project.id()).filter(filterStr).build()
> > ).items()
> > ```

> [tab] Go
>
> The `Filter` string syntax is unchanged: `eq(metadata_key, ...)` checks for key presence, combined with `eq(metadata_value, ...)` to match a specific value.
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
> >
> > sessions, err := client.Sessions.List(ctx, langsmith.SessionListParams{
> > 	Name:  langsmith.F("default"),
> > 	Limit: langsmith.F(int64(1)),
> > })
> > project := sessions.Items[0]
> >
> > filterStr := `and(eq(metadata_key, "user_id"), eq(metadata_value, "u_123"))`
> > runs, err := client.Runs.Query(ctx, langsmith.RunQueryParams{
> > 	Session: langsmith.F([]string{project.ID}),
> > 	Filter:  langsmith.F(filterStr),
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
> >
> > sessions, err := client.Sessions.List(ctx, langsmith.SessionListParams{
> > 	Name:  langsmith.F("default"),
> > 	Limit: langsmith.F(int64(1)),
> > })
> > project := sessions.Items[0]
> >
> > filterStr := `and(eq(metadata_key, "user_id"), eq(metadata_value, "u_123"))`
> > runs, err := client.Runs.QueryV2(ctx, langsmith.RunQueryV2Params{
> > 	ProjectIDs: langsmith.F([]string{project.ID}),
> > 	Filter:     langsmith.F(filterStr),
> > })
> > ```

> [tab] cURL
>
> The `filter` string syntax is unchanged: `eq(metadata_key, ...)` checks for key presence, combined with `eq(metadata_value, ...)` to match a specific value.
>
> > [tab] Before
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > PROJECT_ID=$(curl -s "https://api.smith.langchain.com/api/v1/sessions?name=default&limit=1" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" | jq -r '.[0].id')
> >
> > FILTER='and(eq(metadata_key, "user_id"), eq(metadata_value, "u_123"))'
> >
> > curl -X POST "https://api.smith.langchain.com/api/v1/runs/query" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" \
> >   -H "Content-Type: application/json" \
> >   -d "$(jq -n --arg pid "$PROJECT_ID" --arg f "$FILTER" '{"session": [$pid], "filter": $f}')"
> > ```
>
> > [tab] After
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > PROJECT_ID=$(curl -s "https://api.smith.langchain.com/api/v1/sessions?name=default&limit=1" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" | jq -r '.[0].id')
> >
> > FILTER='and(eq(metadata_key, "user_id"), eq(metadata_value, "u_123"))'
> >
> > curl -X POST "https://api.smith.langchain.com/api/v2/runs/query" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" \
> >   -H "Content-Type: application/json" \
> >   -d "$(jq -n --arg pid "$PROJECT_ID" --arg f "$FILTER" '{"project_ids": [$pid], "filter": $f}')"
> > ```

#### Complex boolean filters

Nested `and()` / `or()` filter expressions still work. Keep `or()` operands on the same field kind: SmithDB rejects OR across run fields and feedback fields in one expression (for example mixing `status` with `feedback_key`).

> [tab] Python
>
> > [tab] Before
> >
> > ```python Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > from langsmith import Client
> >
> > client = Client()
> > filter_str = (
> >     'and(gt(start_time, "2023-07-15T12:34:56Z"),'
> >     ' or(eq(status, "error"), eq(run_type, "llm")))'
> > )
> > runs = client.list_runs(project_name="default", filter=filter_str)
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
> >     filter_str = (
> >         'and(gt(start_time, "2023-07-15T12:34:56Z"),'
> >         ' or(eq(status, "error"), eq(run_type, "llm")))'
> >     )
> >     project = await client.aread_project(project_name="default")
> >     runs = client.runs.query(project_ids=[str(project.id)], filter=filter_str)
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
> > const filterStr =
> >   'and(gt(start_time, "2023-07-15T12:34:56Z"),' +
> >   ' or(eq(status, "error"), eq(run_type, "llm")))';
> > const runs = client.listRuns({ projectName: "default", filter: filterStr });
> > ```
>
> > [tab] After
> >
> > ```ts After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import { Client } from "langsmith";
> >
> > const client = new Client();
> > const filterStr =
> >   'and(gt(start_time, "2023-07-15T12:34:56Z"),' +
> >   ' or(eq(status, "error"), eq(run_type, "llm")))';
> > const project = await client.readProject({ projectName: "default" });
> > const runs = client.runs.query({
> >   project_ids: [project.id],
> >   filter: filterStr,
> > });
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
> > val filterStr = "and(gt(start_time, \"2023-07-15T12:34:56Z\")," +
> >     " or(eq(status, \"error\"), eq(run_type, \"llm\")))"
> > val runs = client.runs().query(
> >     RunQueryParams.builder().addSession(project.id()).filter(filterStr).build()
> > ).items()
> > ```
>
> > [tab] After
> >
> > ```kotlin After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import com.langchain.smith.client.LangsmithClient
> > import com.langchain.smith.client.okhttp.LangsmithOkHttpClient
> > import com.langchain.smith.models.runs.RunQueryV2Params
> > import com.langchain.smith.models.sessions.SessionListParams
> >
> > val client: LangsmithClient = LangsmithOkHttpClient.fromEnv()
> >
> > val project = client.sessions().list(
> >     SessionListParams.builder().name("default").limit(1L).build()
> > ).items().first()
> > val filterStr = "and(gt(start_time, \"2023-07-15T12:34:56Z\")," +
> >     " or(eq(status, \"error\"), eq(run_type, \"llm\")))"
> > val runs = client.runs().queryV2(
> >     RunQueryV2Params.builder().addProjectId(project.id()).filter(filterStr).build()
> > ).items()
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
> > ctx := context.Background()
> > client := langsmith.NewClient()
> >
> > sessions, err := client.Sessions.List(ctx, langsmith.SessionListParams{
> > 	Name:  langsmith.F("default"),
> > 	Limit: langsmith.F(int64(1)),
> > })
> > project := sessions.Items[0]
> >
> > filterStr := `and(gt(start_time, "2023-07-15T12:34:56Z"), or(eq(status, "error"), eq(run_type, "llm")))`
> > runs, err := client.Runs.Query(ctx, langsmith.RunQueryParams{
> > 	Session: langsmith.F([]string{project.ID}),
> > 	Filter:  langsmith.F(filterStr),
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
> >
> > sessions, err := client.Sessions.List(ctx, langsmith.SessionListParams{
> > 	Name:  langsmith.F("default"),
> > 	Limit: langsmith.F(int64(1)),
> > })
> > project := sessions.Items[0]
> >
> > filterStr := `and(gt(start_time, "2023-07-15T12:34:56Z"), or(eq(status, "error"), eq(run_type, "llm")))`
> > runs, err := client.Runs.QueryV2(ctx, langsmith.RunQueryV2Params{
> > 	ProjectIDs: langsmith.F([]string{project.ID}),
> > 	Filter:     langsmith.F(filterStr),
> > })
> > ```

> [tab] cURL
>
> > [tab] Before
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > PROJECT_ID=$(curl -s "https://api.smith.langchain.com/api/v1/sessions?name=default&limit=1" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" | jq -r '.[0].id')
> >
> > FILTER='and(gt(start_time, "2023-07-15T12:34:56Z"), or(eq(status, "error"), eq(run_type, "llm")))'
> >
> > curl -X POST "https://api.smith.langchain.com/api/v1/runs/query" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" \
> >   -H "Content-Type: application/json" \
> >   -d "$(jq -n --arg pid "$PROJECT_ID" --arg f "$FILTER" '{"session": [$pid], "filter": $f}')"
> > ```
>
> > [tab] After
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > PROJECT_ID=$(curl -s "https://api.smith.langchain.com/api/v1/sessions?name=default&limit=1" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" | jq -r '.[0].id')
> >
> > FILTER='and(gt(start_time, "2023-07-15T12:34:56Z"), or(eq(status, "error"), eq(run_type, "llm")))'
> >
> > curl -X POST "https://api.smith.langchain.com/api/v2/runs/query" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" \
> >   -H "Content-Type: application/json" \
> >   -d "$(jq -n --arg pid "$PROJECT_ID" --arg f "$FILTER" '{"project_ids": [$pid], "filter": $f}')"
> > ```

#### Scoped filters: filter, trace\_filter, tree\_filter

> [tab] Python
>
> `filter`, `trace_filter`, and `tree_filter` are unchanged. `filter` applies to the matched run, `trace_filter` to the root of its trace, and `tree_filter` to other runs in the trace tree (siblings and children).
>
> > [tab] Before
> >
> > ```python Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > from langsmith import Client
> >
> > client = Client()
> > runs = client.list_runs(
> >     project_name="default",
> >     filter='eq(name, "RetrieveDocs")',
> >     trace_filter='and(eq(feedback_key, "user_score"), eq(feedback_score, 1))',
> >     tree_filter='eq(name, "ExpandQuery")',
> > )
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
> >     runs = client.runs.query(
> >         project_ids=[str(project.id)],
> >         filter='eq(name, "RetrieveDocs")',
> >         trace_filter='and(eq(feedback_key, "user_score"), eq(feedback_score, 1))',
> >         tree_filter='eq(name, "ExpandQuery")',
> >     )
> >
> >
> > asyncio.run(main())
> > ```

> [tab] TypeScript
>
> `filter`, `trace_filter`, and `tree_filter` are unchanged. `filter` applies to the matched run, `trace_filter` to the root of its trace, and `tree_filter` to other runs in the trace tree (siblings and children).
>
> > [tab] Before
> >
> > ```ts Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import { Client } from "langsmith";
> >
> > const client = new Client();
> > const runs = client.listRuns({
> >   projectName: "default",
> >   filter: 'eq(name, "RetrieveDocs")',
> >   traceFilter: 'and(eq(feedback_key, "user_score"), eq(feedback_score, 1))',
> >   treeFilter: 'eq(name, "ExpandQuery")',
> > });
> > ```
>
> > [tab] After
> >
> > ```ts After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import { Client } from "langsmith";
> >
> > const client = new Client();
> > const project = await client.readProject({ projectName: "default" });
> > const runs = client.runs.query({
> >   project_ids: [project.id],
> >   filter: 'eq(name, "RetrieveDocs")',
> >   trace_filter: 'and(eq(feedback_key, "user_score"), eq(feedback_score, 1))',
> >   tree_filter: 'eq(name, "ExpandQuery")',
> > });
> > ```

> [tab] Java
>
> `.filter()`, `.traceFilter()`, and `.treeFilter()` are unchanged. `filter` applies to the matched run, `traceFilter` to the root of its trace, and `treeFilter` to other runs in the trace tree (siblings and children).
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
> > val runs = client.runs().query(
> >     RunQueryParams.builder()
> >         .addSession(project.id())
> >         .filter("eq(name, \"RetrieveDocs\")")
> >         .traceFilter("and(eq(feedback_key, \"user_score\"), eq(feedback_score, 1))")
> >         .treeFilter("eq(name, \"ExpandQuery\")")
> >         .build()
> > ).items()
> > ```
>
> > [tab] After
> >
> > ```kotlin After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import com.langchain.smith.client.LangsmithClient
> > import com.langchain.smith.client.okhttp.LangsmithOkHttpClient
> > import com.langchain.smith.models.runs.RunQueryV2Params
> > import com.langchain.smith.models.sessions.SessionListParams
> >
> > val client: LangsmithClient = LangsmithOkHttpClient.fromEnv()
> >
> > val project = client.sessions().list(
> >     SessionListParams.builder().name("default").limit(1L).build()
> > ).items().first()
> > val runs = client.runs().queryV2(
> >     RunQueryV2Params.builder()
> >         .addProjectId(project.id())
> >         .filter("eq(name, \"RetrieveDocs\")")
> >         .traceFilter("and(eq(feedback_key, \"user_score\"), eq(feedback_score, 1))")
> >         .treeFilter("eq(name, \"ExpandQuery\")")
> >         .build()
> > ).items()
> > ```

> [tab] Go
>
> `Filter`, `TraceFilter`, and `TreeFilter` are unchanged. `Filter` applies to the matched run, `TraceFilter` to the root of its trace, and `TreeFilter` to other runs in the trace tree (siblings and children).
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
> >
> > sessions, err := client.Sessions.List(ctx, langsmith.SessionListParams{
> > 	Name:  langsmith.F("default"),
> > 	Limit: langsmith.F(int64(1)),
> > })
> > project := sessions.Items[0]
> >
> > runs, err := client.Runs.Query(ctx, langsmith.RunQueryParams{
> > 	Session:     langsmith.F([]string{project.ID}),
> > 	Filter:      langsmith.F(`eq(name, "RetrieveDocs")`),
> > 	TraceFilter: langsmith.F(`and(eq(feedback_key, "user_score"), eq(feedback_score, 1))`),
> > 	TreeFilter:  langsmith.F(`eq(name, "ExpandQuery")`),
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
> >
> > sessions, err := client.Sessions.List(ctx, langsmith.SessionListParams{
> > 	Name:  langsmith.F("default"),
> > 	Limit: langsmith.F(int64(1)),
> > })
> > project := sessions.Items[0]
> >
> > runs, err := client.Runs.QueryV2(ctx, langsmith.RunQueryV2Params{
> > 	ProjectIDs:  langsmith.F([]string{project.ID}),
> > 	Filter:      langsmith.F(`eq(name, "RetrieveDocs")`),
> > 	TraceFilter: langsmith.F(`and(eq(feedback_key, "user_score"), eq(feedback_score, 1))`),
> > 	TreeFilter:  langsmith.F(`eq(name, "ExpandQuery")`),
> > })
> > ```

> [tab] cURL
>
> `filter`, `trace_filter`, and `tree_filter` are unchanged. `filter` applies to the matched run, `trace_filter` to the root of its trace, and `tree_filter` to other runs in the trace tree (siblings and children).
>
> > [tab] Before
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > PROJECT_ID=$(curl -s "https://api.smith.langchain.com/api/v1/sessions?name=default&limit=1" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" | jq -r '.[0].id')
> >
> > FILTER='eq(name, "RetrieveDocs")'
> > TRACE_FILTER='and(eq(feedback_key, "user_score"), eq(feedback_score, 1))'
> > TREE_FILTER='eq(name, "ExpandQuery")'
> >
> > curl -X POST "https://api.smith.langchain.com/api/v1/runs/query" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" \
> >   -H "Content-Type: application/json" \
> >   -d "$(jq -n \
> >     --arg pid "$PROJECT_ID" \
> >     --arg f "$FILTER" \
> >     --arg tf "$TRACE_FILTER" \
> >     --arg treef "$TREE_FILTER" \
> >     '{"session": [$pid], "filter": $f, "trace_filter": $tf, "tree_filter": $treef}')"
> > ```
>
> > [tab] After
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > PROJECT_ID=$(curl -s "https://api.smith.langchain.com/api/v1/sessions?name=default&limit=1" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" | jq -r '.[0].id')
> >
> > FILTER='eq(name, "RetrieveDocs")'
> > TRACE_FILTER='and(eq(feedback_key, "user_score"), eq(feedback_score, 1))'
> > TREE_FILTER='eq(name, "ExpandQuery")'
> >
> > curl -X POST "https://api.smith.langchain.com/api/v2/runs/query" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" \
> >   -H "Content-Type: application/json" \
> >   -d "$(jq -n \
> >     --arg pid "$PROJECT_ID" \
> >     --arg f "$FILTER" \
> >     --arg tf "$TRACE_FILTER" \
> >     --arg treef "$TREE_FILTER" \
> >     '{"project_ids": [$pid], "filter": $f, "trace_filter": $tf, "tree_filter": $treef}')"
> > ```

## See also

* [Retrieve runs](Migrate%20run%20retrieval%20to%20SmithDB.md)
* [Traces](Migrate%20trace%20methods%20to%20SmithDB.md)
* [Migration overview](Migrate%20to%20SmithDB-backed%20APIs.md)
* [Search conversation content with AI using the SDK](../../Debug/Viewing%20%26%20managing%20traces/Filter%20traces.md#search-with-ai-using-the-sdk)

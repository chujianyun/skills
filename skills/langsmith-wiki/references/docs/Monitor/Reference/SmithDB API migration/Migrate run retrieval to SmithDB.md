# Migrate run retrieval to SmithDB

> Migrate the LangSmith SDK methods that retrieve a single run or build a run URL.

These methods read a single run or build a link to one. To migrate run queries, see [Query runs](Migrate%20run%20queries%20to%20SmithDB.md). For deprecation dates and minimum SDK versions, see [Migrate to SmithDB-backed APIs](Migrate%20to%20SmithDB-backed%20APIs.md).

## Runs: retrieve

Fetch a single run by ID. Returns only the run ID by default—specify a field selection list to retrieve additional data.

### Main changes

#### Method name

> [tab] Python
>
> | Before | After |
> | - | - |
> | `client.read_run()` | `client.runs.retrieve()` (alias to `client.runs.retrieve_v2()`) |
>
> > [!NOTE]
> >
> > `client.runs.retrieve()` is now async. Call it with `await`.
>
> See the [reference](https://reference.langchain.com/python/langsmith/_openapi_client/resources/runs/RunsResource/retrieve_v2) for the full parameter and field list.

> [tab] TypeScript
>
> | Before | After |
> | - | - |
> | `client.readRun()` | `client.runs.retrieve()` (alias to `client.runs.retrieveV2()`) |
>
> See the [reference](https://reference.langchain.com/javascript/langsmith/_openapi_client/Langsmith/Runs/retrieveV2) for the full parameter and field list.

> [tab] Java
>
> | Before | After |
> | - | - |
> | `client.runs().retrieve()` | `client.runs().retrieveV2()` |
>
> See the [reference](https://javadoc.io/doc/com.langchain.smith/langsmith-java/latest/com/langchain/smith/services/blocking/RunService.html) for the full parameter list.

> [tab] Go
>
> | Before | After |
> | - | - |
> | `client.Runs.Get()` | `client.Runs.GetV2()` |
>
> See the [reference](https://pkg.go.dev/github.com/langchain-ai/langsmith-go#RunService.GetV2) for the full parameter list.

> [tab] cURL
>
> | Before | After |
> | - | - |
> | `GET /api/v1/runs/{run_id}` | `GET /api/v2/runs/{run_id}` |
>
> See the [API doc](../LangSmith%20REST%20API/Tracing/Get%20a%20single%20run.md) for the full parameter and field list.

#### Query parameters

> [tab] Python
>
> > [!WARNING]
> >
> > `runs.retrieve` requires a new `project_id` field that `read_run` did not need. It also accepts an optional `start_time`—providing it speeds up retrieval but is not required.
>
> | Before (`read_run`) | After (`runs.retrieve`) | Notes |
> | - | - | - |
> | `run_id` | `run_id` | Unchanged |
> | `load_child_runs` | *(removed)* | Fetch the trace's runs with `traces.list_runs` and filter by `parent_run_ids`. See [Load a run's child runs](#load-a-runs-child-runs) |
> | *(not available)* | `project_id` | **Required**—UUID of the project that owns the run |
> | *(not available)* | `start_time` | Optional—run's start time (RFC3339); providing it speeds up retrieval. Required for SmithDB-only self-hosted below v0.18 |
> | *(all fields returned by default)* | `selects` | Field projection; defaults to `["ID"]` only; field names are uppercase |

> [tab] TypeScript
>
> > [!WARNING]
> >
> > `client.runs.retrieve` requires a new `project_id` field that `readRun` did not need. It also accepts an optional `start_time`—providing it speeds up retrieval but is not required.
>
> | Before (`readRun`) | After (`client.runs.retrieve`) | Notes |
> | - | - | - |
> | `runId` | `runId` | Unchanged (positional parameter) |
> | `options.loadChildRuns` | *(removed)* | Fetch the trace's runs with `client.traces.listRuns` and filter by `parent_run_ids`. See [Load a run's child runs](#load-a-runs-child-runs) |
> | *(not available)* | `project_id` | **Required**—`snake_case`; UUID of the project that owns the run |
> | *(not available)* | `start_time` | Optional—`snake_case`; run's start time (RFC3339); providing it speeds up retrieval. Required for SmithDB-only self-hosted below v0.18 |
> | *(all fields returned by default)* | `selects` | Field projection; defaults to `["ID"]` only; field names are uppercase |

> [tab] Java
>
> > [!WARNING]
> >
> > `retrieveV2()` requires `projectId()`, which replaces the removed `sessionId()`. `startTime()` remains optional—providing it speeds up retrieval but is not required.
>
> | Before (`RunRetrieveParams`) | After (`RunRetrieveV2Params`) | Notes |
> | - | - | - |
> | `runId()` | `runId()` | Unchanged |
> | `sessionId()` | *(removed)* | Replaced by `projectId()` |
> | `startTime()` | `startTime()` | Still optional; providing it speeds up retrieval. Required for SmithDB-only self-hosted below v0.18 |
> | `excludeS3StoredAttributes()` | *(removed)* | No equivalent |
> | `excludeSerialized()` | *(removed)* | No equivalent |
> | `includeMessages()` | *(removed)* | No equivalent |
> | *(not available)* | `projectId()` | **Required**—UUID of the project that owns the run |
> | *(all fields returned by default)* | `selects()` | Field projection; defaults to `["ID"]` only; field names are uppercase |

> [tab] Go
>
> > [!WARNING]
> >
> > `GetV2()` requires `ProjectID`, which replaces the removed `SessionID`. `StartTime` remains optional—providing it speeds up retrieval but is not required.
>
> | Before (`RunGetParams`) | After (`RunGetV2Params`) | Notes |
> | - | - | - |
> | `runID` (positional) | `runID` (positional) | Unchanged |
> | `ExcludeS3StoredAttributes` | *(removed)* | No equivalent |
> | `ExcludeSerialized` | *(removed)* | No equivalent |
> | `IncludeMessages` | *(removed)* | No equivalent |
> | `SessionID` | *(removed)* | Replaced by `ProjectID` |
> | `StartTime` | `StartTime` | Still optional; providing it speeds up retrieval. Required for SmithDB-only self-hosted below v0.18 |
> | *(not available)* | `ProjectID` | **Required**—UUID of the project that owns the run |
> | *(all fields returned by default)* | `Selects` | Field projection; defaults to `["ID"]` only; field name constants are uppercase (e.g., `RunGetV2ParamsSelectName`) |

> [tab] cURL
>
> `run_id` remains in the URL path. All other parameters are query string values with `snake_case` names.
>
> > [!WARNING]
> >
> > `GET /api/v2/runs/{run_id}` requires a new `project_id` query param. `start_time` remains optional—providing it speeds up retrieval but is not required.
>
> | Before (`GET /api/v1/runs/{run_id}` param) | After (`GET /api/v2/runs/{run_id}` param) | Notes |
> | - | - | - |
> | `run_id` (path) | `run_id` (path) | Unchanged |
> | *(not available)* | `project_id` (query) | **Required**—UUID of the project that owns the run |
> | `start_time` (query) | `start_time` (query) | Still optional; providing it speeds up retrieval. Required for SmithDB-only self-hosted below v0.18 |
> | *(all fields returned by default)* | `selects` (query, repeatable) | Field projection; defaults to `["ID"]` only; field names are uppercase |

#### Response fields

> [tab] Python
>
> Pass SCREAMING\_SNAKE\_CASE strings to `selects` (eg. `"ID"`, `"NAME"`, `"STATUS"`) to control which fields are populated on the returned `Run`; only selected fields are non-`None`. Default `selects` contains only `"ID"`.
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
> | `run.total_tokens` | `run.total_tokens` | Unchanged |
> | `run.prompt_tokens` | `run.prompt_tokens` | Unchanged |
> | `run.completion_tokens` | `run.completion_tokens` | Unchanged |
> | `run.total_cost` | `run.total_cost` | Unchanged |
> | `run.prompt_cost` | `run.prompt_cost` | Unchanged |
> | `run.completion_cost` | `run.completion_cost` | Unchanged |
> | `run.first_token_time` | `run.first_token_time` | Unchanged |
> | `run.latency` (property) | `run.latency_seconds` | Renamed; was a computed `timedelta` property, now a native `float` field |
> | `run.in_dataset` | `run.is_in_dataset` | Renamed |
> | `run.child_run_ids` | *(removed)* | Filter the trace's runs on `parent_run_ids`. See [Load a run's child runs](#load-a-runs-child-runs) |
> | `run.child_runs` | *(removed)* | Group the trace's runs by the last entry in `parent_run_ids`. See [Load a run's child runs](#load-a-runs-child-runs) |
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
> Pass SCREAMING\_SNAKE\_CASE strings to `selects` (eg. `"ID"`, `"NAME"`, `"STATUS"`) to control which fields are populated on the returned `Run`. Default `selects` contains only `"ID"`.
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
> | `run.totalTokens` | `run.total_tokens` | Renamed to `snake_case` |
> | `run.promptTokens` | `run.prompt_tokens` | Renamed to `snake_case` |
> | `run.completionTokens` | `run.completion_tokens` | Renamed to `snake_case` |
> | `run.totalCost` | `run.total_cost` | Renamed to `snake_case` |
> | `run.promptCost` | `run.prompt_cost` | Renamed to `snake_case` |
> | `run.completionCost` | `run.completion_cost` | Renamed to `snake_case` |
> | `run.firstTokenTime` | `run.first_token_time` | Renamed to `snake_case` |
> | `run.latency` | `run.latency_seconds` | Renamed; was a computed property, now a native `number` field (seconds) |
> | `run.inDataset` | `run.is_in_dataset` | Renamed |
> | `run.child_run_ids` | *(removed)* | Filter the trace's runs on `parent_run_ids`. See [Load a run's child runs](#load-a-runs-child-runs) |
> | `run.child_runs` | *(removed)* | Group the trace's runs by the last entry in `parent_run_ids`. See [Load a run's child runs](#load-a-runs-child-runs) |
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
> Add `RunRetrieveV2Params.Select` values (eg. `Select.NAME`, `Select.STATUS`) via `.addSelect(...)` to control which fields are populated; unselected fields return empty `Optional` values. `selects()` defaults to `ID` only.
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
> | `run.totalTokens()` | `run.totalTokens()` | Unchanged |
> | `run.promptTokens()` | `run.promptTokens()` | Unchanged |
> | `run.completionTokens()` | `run.completionTokens()` | Unchanged |
> | `run.totalCost()` | `run.totalCost()` | Return type changed from `Optional<String>` to `Optional<Double>` |
> | `run.promptCost()` | `run.promptCost()` | Return type changed from `Optional<String>` to `Optional<Double>` |
> | `run.completionCost()` | `run.completionCost()` | Return type changed from `Optional<String>` to `Optional<Double>` |
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
> Pass `RunGetV2ParamsSelect` constants (eg. `RunGetV2ParamsSelectName`, `RunGetV2ParamsSelectStatus`) to `Selects` to control which fields are populated; unselected fields are zero-valued on the returned struct. `Selects` defaults to `ID` only.
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
> | `run.PromptCost` | `run.PromptCost` | Unchanged |
> | `run.PromptCostDetails` | `run.PromptCostDetails.Raw` | Field now wraps the map; access `.Raw` to get `map[string]float64` (was `map[string]string`) |
> | `run.PromptTokenDetails` | `run.PromptTokenDetails.Raw` | Field now wraps the map; access `.Raw` to get `map[string]int64` (element type unchanged) |
> | `run.PromptTokens` | `run.PromptTokens` | Unchanged |
> | `run.CompletionCost` | `run.CompletionCost` | Unchanged |
> | `run.CompletionCostDetails` | `run.CompletionCostDetails.Raw` | Field now wraps the map; access `.Raw` to get `map[string]float64` (was `map[string]string`) |
> | `run.CompletionTokenDetails` | `run.CompletionTokenDetails.Raw` | Field now wraps the map; access `.Raw` to get `map[string]int64` (element type unchanged) |
> | `run.CompletionTokens` | `run.CompletionTokens` | Unchanged |
> | `run.TotalCost` | `run.TotalCost` | Unchanged |
> | `run.TotalTokens` | `run.TotalTokens` | Unchanged |
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
> Pass SCREAMING\_SNAKE\_CASE strings as repeated `selects` query parameters (eg. `selects=NAME&selects=STATUS`) to control which fields are populated. Default `selects` contains only `"ID"`.
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
> | `prompt_cost` | `prompt_cost` | Unchanged |
> | `prompt_cost_details` | `prompt_cost_details.raw` | Field now wraps the object; read `.raw` for the same `{category: cost}` mapping, now with numeric values (was strings) |
> | `prompt_token_details` | `prompt_token_details.raw` | Field now wraps the object; read `.raw` for the same `{category: count}` mapping (values unchanged) |
> | `prompt_tokens` | `prompt_tokens` | Unchanged |
> | `completion_cost` | `completion_cost` | Unchanged |
> | `completion_cost_details` | `completion_cost_details.raw` | Field now wraps the object; read `.raw` for the same `{category: cost}` mapping, now with numeric values (was strings) |
> | `completion_token_details` | `completion_token_details.raw` | Field now wraps the object; read `.raw` for the same `{category: count}` mapping (values unchanged) |
> | `completion_tokens` | `completion_tokens` | Unchanged |
> | `total_cost` | `total_cost` | Unchanged |
> | `total_tokens` | `total_tokens` | Unchanged |
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
> | | Before (`client.read_run()`) | After (`client.runs.retrieve()`) |
> | - | - | - |
> | Limit | 30 requests per 60 seconds | 300 requests per 10 seconds |

> [tab] TypeScript
>
> | | Before (`client.readRun()`) | After (`client.runs.retrieve()`) |
> | - | - | - |
> | Limit | 30 requests per 60 seconds | 300 requests per 10 seconds |

> [tab] Java
>
> | | Before (`client.runs().retrieve()`) | After (`client.runs().retrieveV2()`) |
> | - | - | - |
> | Limit | 30 requests per 60 seconds | 300 requests per 10 seconds |

> [tab] Go
>
> | | Before (`client.Runs.Get()`) | After (`client.Runs.GetV2()`) |
> | - | - | - |
> | Limit | 30 requests per 60 seconds | 300 requests per 10 seconds |

> [tab] cURL
>
> | | Before (`GET /api/v1/runs/{run_id}`) | After (`GET /api/v2/runs/{run_id}`) |
> | - | - | - |
> | Limit | 30 requests per 60 seconds | 300 requests per 10 seconds |

Requests that exceed a limit return `429 Too Many Requests`. For general rate limit information, see [Usage and billing](../../Trace/Configuration%20%26%20troubleshooting/Usage%20and%20billing.md#rate-limits).

### Examples

#### Fetch a single run by ID

> [tab] Python
>
> `runs.retrieve` requires an additional `project_id` (UUID) parameter that `read_run` did not need. It also accepts an optional `start_time`—providing it speeds up retrieval but is not required. Resolve the project UUID via `client.aread_project()` first.
>
> > [tab] Before
> >
> > ```python Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > from langsmith import Client
> >
> > client = Client()
> > run_id = "<run-id>"
> > run = client.read_run(run_id)
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
> >     run_id = "<run-id>"
> >     start_time = "2026-06-01T12:00:00Z"  # Optional, but speeds up retrieval
> >     run = await client.runs.retrieve(
> >         run_id=run_id,
> >         project_id=str(project.id),
> >         start_time=start_time,
> >     )
> >
> >
> > asyncio.run(main())
> > ```

> [tab] TypeScript
>
> `client.runs.retrieve` requires an additional `project_id` (UUID) parameter that `readRun` did not need. It also accepts an optional `start_time`—providing it speeds up retrieval but is not required. Resolve the project UUID via `client.readProject()` first.
>
> > [tab] Before
> >
> > ```ts Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import { Client } from "langsmith";
> >
> > const client = new Client();
> > let runId = "<run-id>";
> > await client.readRun(runId);
> > ```
>
> > [tab] After
> >
> > ```ts After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import { Client } from "langsmith";
> >
> > const client = new Client();
> > const project = await client.readProject({ projectName: "default" });
> > let runId = "<run-id>";
> > let startTime = "2026-06-01T12:00:00Z"; // Optional, but speeds up retrieval
> > await client.runs.retrieve(runId, {
> >   project_id: project.id,
> >   start_time: startTime,
> > });
> > ```

> [tab] Java
>
> `retrieveV2()` requires an additional `projectId()` (UUID) parameter that `client.runs().retrieve()` did not need. It also accepts an optional `startTime()`—providing it speeds up retrieval but is not required. Resolve the project UUID via `client.sessions().list()` first.
>
> > [tab] Before
> >
> > ```kotlin Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import com.langchain.smith.client.LangsmithClient
> > import com.langchain.smith.client.okhttp.LangsmithOkHttpClient
> >
> > val client: LangsmithClient = LangsmithOkHttpClient.fromEnv()
> >
> > var runId = "<run-id>"
> > client.runs().retrieve(runId)
> > ```
>
> > [tab] After
> >
> > ```kotlin After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import java.time.OffsetDateTime
> >
> > import com.langchain.smith.client.LangsmithClient
> > import com.langchain.smith.client.okhttp.LangsmithOkHttpClient
> > import com.langchain.smith.models.runs.RunRetrieveV2Params
> > import com.langchain.smith.models.sessions.SessionListParams
> >
> > val client: LangsmithClient = LangsmithOkHttpClient.fromEnv()
> >
> > val project = client.sessions().list(
> >     SessionListParams.builder().name("default").limit(1L).build()
> > ).items().first()
> >
> > var runId = "<run-id>"
> > var startTime = "<run-start-time-rfc3339>" // Optional, but speeds up retrieval
> > client.runs().retrieveV2(
> >     runId,
> >     RunRetrieveV2Params.builder()
> >         .projectId(project.id())
> >         .startTime(OffsetDateTime.parse(startTime))
> >         .build()
> > )
> > ```

> [tab] Go
>
> `GetV2()` requires an additional `ProjectID` (UUID) parameter that `client.Runs.Get()` did not need. It also accepts an optional `StartTime`—providing it speeds up retrieval but is not required. Resolve the project UUID via `client.Sessions.List()` first.
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
> > runID := "<run-id>"
> > run, err := client.Runs.Get(ctx, runID, langsmith.RunGetParams{})
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
> > runID := "<run-id>"
> > startTime := time.Date(2026, 6, 1, 12, 0, 0, 0, time.UTC) // Optional, but speeds up retrieval
> > projectID := "<project-id>"
> > run, err := client.Runs.GetV2(ctx, runID, langsmith.RunGetV2Params{
> > 	ProjectID: langsmith.F(projectID),
> > 	StartTime: langsmith.F(startTime),
> > })
> > ```

> [tab] cURL
>
> `GET /api/v2/runs/{run_id}` requires an additional `project_id` (UUID) query parameter that `GET /api/v1/runs/{run_id}` did not need. It also accepts an optional `start_time`—providing it speeds up retrieval but is not required. Resolve the project UUID via a `GET /api/v1/sessions` request first.
>
> > [tab] Before
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > RUN_ID="<run-id>"
> >
> > curl "https://api.smith.langchain.com/api/v1/runs/$RUN_ID" \
> >   -H "x-api-key: $LANGSMITH_API_KEY"
> > ```
>
> > [tab] After
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > PROJECT_ID=$(curl -s "https://api.smith.langchain.com/api/v1/sessions?name=default&limit=1" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" | jq -r '.[0].id')
> >
> > RUN_ID="<run-id>"
> > START_TIME="2025-01-01T12:00:00Z" # Optional, but speeds up retrieval
> >
> > curl "https://api.smith.langchain.com/api/v2/runs/$RUN_ID?project_id=$PROJECT_ID&start_time=$START_TIME" \
> >   -H "x-api-key: $LANGSMITH_API_KEY"
> > ```

#### Selecting fields

> [tab] Python
>
> `read_run` returns a full run object with no selection needed. `runs.retrieve` returns only `id` by default—pass `selects=[...]` to request more.
>
> > [tab] Before
> >
> > ```python Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > from langsmith import Client
> >
> > client = Client()
> > run_id = "<run-id>"
> > run = client.read_run(run_id=run_id)
> > print(run.name, run.status, run.total_tokens)
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
> >     run_id = "<run-id>"
> >     start_time = "2026-06-01T12:00:00Z"  # Optional, but speeds up retrieval
> >     run = await client.runs.retrieve(
> >         run_id=run_id,
> >         project_id=str(project.id),
> >         start_time=start_time,
> >         selects=["NAME", "STATUS", "TOTAL_TOKENS"],
> >     )
> >     print(run.name, run.status, run.total_tokens)
> >
> >
> > asyncio.run(main())
> > ```

> [tab] TypeScript
>
> `readRun` returns a full run object with no selection needed. `client.runs.retrieve` returns only `id` by default—pass `selects: [...]` to request more.
>
> > [tab] Before
> >
> > ```ts Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import { Client } from "langsmith";
> >
> > const client = new Client();
> > let runId = "<run-id>";
> > const retrievedRun = await client.readRun(runId);
> > console.log(retrievedRun.name, retrievedRun.status, retrievedRun.total_tokens);
> > ```
>
> > [tab] After
> >
> > ```ts After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import { Client } from "langsmith";
> >
> > const client = new Client();
> > let runId = "<run-id>";
> > let startTime = "2026-06-01T12:00:00Z";
> > let projectId = "<project-id>";
> > const retrievedRun = await client.runs.retrieve(runId, {
> >   project_id: projectId,
> >   start_time: startTime,
> >   selects: ["NAME", "STATUS", "TOTAL_TOKENS"],
> > });
> > console.log(retrievedRun.name, retrievedRun.status, retrievedRun.total_tokens);
> > ```

> [tab] Java
>
> `.retrieve()` returns a full run object with no selection needed. `.retrieveV2()` returns only `id` by default—call `.addSelect(...)` for each field you need.
>
> > [tab] Before
> >
> > ```kotlin Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import com.langchain.smith.client.LangsmithClient
> > import com.langchain.smith.client.okhttp.LangsmithOkHttpClient
> >
> > val client: LangsmithClient = LangsmithOkHttpClient.fromEnv()
> >
> > var runId = "<run-id>"
> > val run = client.runs().retrieve(runId)
> > println("${run.name()} ${run.status()} ${run.totalTokens()}")
> > ```
>
> > [tab] After
> >
> > ```kotlin After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import java.time.OffsetDateTime
> >
> > import com.langchain.smith.client.LangsmithClient
> > import com.langchain.smith.client.okhttp.LangsmithOkHttpClient
> > import com.langchain.smith.models.runs.RunRetrieveV2Params
> > import com.langchain.smith.models.sessions.SessionListParams
> >
> > val client: LangsmithClient = LangsmithOkHttpClient.fromEnv()
> >
> > val project = client.sessions().list(
> >     SessionListParams.builder().name("default").limit(1L).build()
> > ).items().first()
> >
> > var runId = "<run-id>"
> > var startTime = "<run-start-time-rfc3339>"
> > val run = client.runs().retrieveV2(
> >     runId,
> >     RunRetrieveV2Params.builder()
> >         .projectId(project.id())
> >         .startTime(OffsetDateTime.parse(startTime))
> >         .addSelect(RunRetrieveV2Params.Select.NAME)
> >         .addSelect(RunRetrieveV2Params.Select.STATUS)
> >         .addSelect(RunRetrieveV2Params.Select.TOTAL_TOKENS)
> >         .build()
> > )
> > println("${run.name()} ${run.status()} ${run.totalTokens()}")
> > ```

> [tab] Go
>
> `Get` returns a full run struct with no selection needed. `GetV2` returns only `ID` by default—pass `Selects` with the fields you need.
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
> > runID := "<run-id>"
> > run, err := client.Runs.Get(ctx, runID, langsmith.RunGetParams{})
> > fmt.Println(run.Name, run.Status, run.TotalTokens)
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
> > runID := "<run-id>"
> > startTime := time.Date(2026, 6, 1, 12, 0, 0, 0, time.UTC)
> > projectID := "<project-id>"
> > run, err := client.Runs.GetV2(ctx, runID, langsmith.RunGetV2Params{
> > 	ProjectID: langsmith.F(projectID),
> > 	StartTime: langsmith.F(startTime),
> > 	Selects: langsmith.F([]langsmith.RunGetV2ParamsSelect{
> > 		langsmith.RunGetV2ParamsSelectName,
> > 		langsmith.RunGetV2ParamsSelectStatus,
> > 		langsmith.RunGetV2ParamsSelectTotalTokens,
> > 	}),
> > })
> > fmt.Println(run.Name, run.Status, run.TotalTokens)
> > ```

> [tab] cURL
>
> `GET /api/v1/runs/{run_id}` returns a full run object with no selection needed. `GET /api/v2/runs/{run_id}` returns only `id` by default—pass `selects` query parameters for the fields you need.
>
> > [tab] Before
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > RUN_ID="<run-id>"
> >
> > curl "https://api.smith.langchain.com/api/v1/runs/$RUN_ID" \
> >   -H "x-api-key: $LANGSMITH_API_KEY"
> > ```
>
> > [tab] After
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > PROJECT_ID=$(curl -s "https://api.smith.langchain.com/api/v1/sessions?name=default&limit=1" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" | jq -r '.[0].id')
> >
> > RUN_ID="<run-id>"
> > START_TIME="2026-06-01T12:00:00Z"
> >
> > curl "https://api.smith.langchain.com/api/v2/runs/$RUN_ID?project_id=$PROJECT_ID&start_time=$START_TIME&selects=NAME&selects=STATUS&selects=TOTAL_TOKENS" \
> >   -H "x-api-key: $LANGSMITH_API_KEY"
> > ```

#### Handle a not-found run

> [tab] Python
>
> `read_run` raised `LangSmithNotFoundError` from `langsmith.utils` for a missing run. `runs.retrieve` raises `NotFoundError` from `langsmith` instead.
>
> > [tab] Before
> >
> > ```python Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > from langsmith import Client
> > from langsmith.utils import LangSmithNotFoundError
> >
> > client = Client()
> > run_id = "<run-id>"
> >
> > try:
> >     run = client.read_run(run_id)
> > except LangSmithNotFoundError:
> >     print(f"Run {run_id} not found")
> > ```
>
> > [tab] After
> >
> > ```python After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import asyncio
> >
> > from langsmith import Client
> > from langsmith import NotFoundError
> >
> >
> > async def main():
> >     client = Client()
> >     project = await client.aread_project(project_name="default")
> >     run_id = "<run-id>"
> >     start_time = "2026-06-01T12:00:00Z"
> >
> >     try:
> >         run = await client.runs.retrieve(
> >             run_id=run_id,
> >             project_id=str(project.id),
> >             start_time=start_time,
> >         )
> >     except NotFoundError:
> >         print(f"Run {run_id} not found")
> >
> >
> > asyncio.run(main())
> > ```

> [tab] TypeScript
>
> `client.runs.retrieve` raises `NotFoundError` for a missing run.
>
> > [tab] Before
> >
> > ```ts Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import { uuid7 } from "langsmith";
> > import { Client } from "langsmith";
> >
> > const client = new Client();
> > let runId = "<run-id>";
> >
> > try {
> >   await client.readRun(runId);
> > } catch (e: any) {
> >   if (e?.status === 404) {
> >     console.log(`Run ${runId} not found`);
> >   }
> > }
> > ```
>
> > [tab] After
> >
> > ```ts After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import { uuid7 } from "langsmith";
> > import { Client, NotFoundError } from "langsmith";
> >
> > const client = new Client();
> > const project = await client.readProject({ projectName: "default" });
> > let runId = "<run-id>";
> > const startTime = "2026-06-01T12:00:00Z";
> >
> > try {
> >   await client.runs.retrieve(runId, {
> >     project_id: project.id,
> >     start_time: startTime,
> >   });
> > } catch (e) {
> >   if (e instanceof NotFoundError) {
> >     console.log(`Run ${runId} not found`);
> >   }
> > }
> > ```

> [tab] Java
>
> `.retrieve()` and `.retrieveV2()` both raise `com.langchain.smith.errors.NotFoundException`—unchanged, since the Java SDK was already Stainless-generated before SmithDB.
>
> > [tab] Before
> >
> > ```kotlin Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import com.langchain.smith.client.LangsmithClient
> > import com.langchain.smith.client.okhttp.LangsmithOkHttpClient
> > import com.langchain.smith.errors.NotFoundException
> >
> > val client: LangsmithClient = LangsmithOkHttpClient.fromEnv()
> >
> > var runId = "<run-id>"
> > try {
> >     client.runs().retrieve(runId)
> > } catch (e: NotFoundException) {
> >     println("Run $runId not found")
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
> > import com.langchain.smith.errors.NotFoundException
> > import com.langchain.smith.models.runs.RunRetrieveV2Params
> > import com.langchain.smith.models.sessions.SessionListParams
> >
> > val client: LangsmithClient = LangsmithOkHttpClient.fromEnv()
> >
> > val project = client.sessions().list(
> >     SessionListParams.builder().name("default").limit(1L).build()
> > ).items().first()
> >
> > var runId = "<run-id>"
> > var startTime = "<run-start-time-rfc3339>"
> > try {
> >     client.runs().retrieveV2(
> >         runId,
> >         RunRetrieveV2Params.builder()
> >             .projectId(project.id())
> >             .startTime(OffsetDateTime.parse(startTime))
> >             .build()
> >     )
> > } catch (e: NotFoundException) {
> >     println("Run $runId not found")
> > }
> > ```

> [tab] Go
>
> `Get` and `GetV2` both return a `*langsmith.Error` you can inspect with `errors.As`—unchanged, since the Go SDK was already Stainless-generated before SmithDB. Check `StatusCode` for `404`.
>
> > [tab] Before
> >
> > ```go Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > package main
> >
> > import (
> > 	"context"
> > 	"errors"
> > 	"fmt"
> >
> > 	"github.com/langchain-ai/langsmith-go"
> > )
> >
> > ctx := context.Background()
> > client := langsmith.NewClient()
> >
> > runID := "<run-id>"
> > _, err := client.Runs.Get(ctx, runID, langsmith.RunGetParams{})
> > if err != nil {
> > 	var apiErr *langsmith.Error
> > 	if errors.As(err, &apiErr) && apiErr.StatusCode == 404 {
> > 		fmt.Printf("Run %s not found\n", runID)
> > 	} else {
> > 		panic(err)
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
> > 	"errors"
> > 	"fmt"
> > 	"time"
> >
> > 	"github.com/google/uuid"
> > 	"github.com/langchain-ai/langsmith-go"
> > )
> >
> > ctx := context.Background()
> > client := langsmith.NewClient()
> >
> > runID := "<run-id>"
> > startTime := time.Date(2026, 6, 1, 12, 0, 0, 0, time.UTC)
> > projectID := "<project-id>"
> > _, err := client.Runs.GetV2(ctx, runID, langsmith.RunGetV2Params{
> > 	ProjectID: langsmith.F(projectID),
> > 	StartTime: langsmith.F(startTime),
> > })
> > if err != nil {
> > 	var apiErr *langsmith.Error
> > 	if errors.As(err, &apiErr) && apiErr.StatusCode == 404 {
> > 		fmt.Printf("Run %s not found\n", runID)
> > 	} else {
> > 		panic(err)
> > 	}
> > }
> > ```

> [tab] cURL
>
> Both `GET /api/v1/runs/{run_id}` and `GET /api/v2/runs/{run_id}` return HTTP 404 for a missing run. Check the response status code.
>
> > [tab] Before
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > RUN_ID="<run-id>"
> >
> > HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
> >   "https://api.smith.langchain.com/api/v1/runs/$RUN_ID" \
> >   -H "x-api-key: $LANGSMITH_API_KEY")
> >
> > if [ "$HTTP_STATUS" = "404" ]; then
> >   echo "Run $RUN_ID not found"
> > fi
> > ```
>
> > [tab] After
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > PROJECT_ID=$(curl -s "https://api.smith.langchain.com/api/v1/sessions?name=default&limit=1" \
> >   -H "x-api-key: $LANGSMITH_API_KEY" | jq -r '.[0].id')
> >
> > RUN_ID="<run-id>"
> > START_TIME="2025-01-01T12:00:00Z"
> >
> > HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
> >   "https://api.smith.langchain.com/api/v2/runs/$RUN_ID?project_id=$PROJECT_ID&start_time=$START_TIME" \
> >   -H "x-api-key: $LANGSMITH_API_KEY")
> >
> > if [ "$HTTP_STATUS" = "404" ]; then
> >   echo "Run $RUN_ID not found"
> > fi
> > ```

#### Load a run's child runs

The `load_child_runs` flag and the nested `child_runs` field are removed. Fetch every run in the trace with `traces.list_runs`, then filter on `parent_run_ids`, which holds each run's full ancestor chain, root first and closest parent last.

> [tab] Python
>
> Replace `read_run(run_id, load_child_runs=True)` with `client.traces.list_runs`.
>
> > [tab] Before
> >
> > ```python Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > from langsmith import Client
> >
> > client = Client()
> > run_id = "<run-id>"
> >
> > run = client.read_run(run_id, load_child_runs=True)
> >
> > # `child_runs` holds the direct children, each with its own nested `child_runs`.
> > # `child_run_ids` holds every descendant, at any depth.
> > for child in run.child_runs or []:
> >     print(child.name, child.run_type, len(child.child_runs or []))
> > print(len(run.child_run_ids or []), "descendants")
> > ```
>
> > [tab] After
> >
> > ```python After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import asyncio
> > from collections import defaultdict
> >
> > from langsmith import Client
> >
> >
> > async def main():
> >     client = Client()
> >     project = await client.aread_project(project_name="default")
> >     # A root run is its own trace, so `trace_id` is also the run ID.
> >     trace_id = "<trace-id>"
> >
> >     trace_runs = await client.traces.list_runs(
> >         trace_id,
> >         project_id=str(project.id),
> >         selects=["ID", "NAME", "RUN_TYPE", "PARENT_RUN_IDS", "START_TIME", "END_TIME"],
> >     )
> >
> >     # `parent_run_ids` is the full ancestor chain, root first, closest parent
> >     # last. A run is a descendant of any ID in that chain, at any depth, not
> >     # only of the immediate parent. This flat list replaces `child_run_ids`.
> >     descendants = [
> >         run for run in (trace_runs.items or []) if trace_id in (run.parent_run_ids or [])
> >     ]
> >     print(len(descendants), "descendants")
> >
> >     # Optional: rebuild the nested `child_runs` shape instead of a flat list.
> >     by_parent = defaultdict(list)
> >     for run in trace_runs.items or []:
> >         if run.parent_run_ids:
> >             # The last ancestor is the immediate parent.
> >             by_parent[run.parent_run_ids[-1]].append(run)
> >
> >     def attach(run):
> >         run.child_runs = by_parent.get(run.id, [])
> >         for child in run.child_runs:
> >             attach(child)
> >
> >     for run in trace_runs.items or []:
> >         attach(run)
> >
> >     children = by_parent.get(trace_id, [])
> >     for child in children:
> >         print(child.name, child.run_type, len(child.child_runs))
> >
> >
> > asyncio.run(main())
> > ```

> [tab] TypeScript
>
> Replace the `loadChildRuns` option with `client.traces.listRuns`.
>
> > [tab] Before
> >
> > ```ts Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import { Client } from "langsmith";
> >
> > const client = new Client();
> > let runId = "<run-id>";
> >
> > const run = await client.readRun(runId, { loadChildRuns: true });
> >
> > // `child_runs` holds the direct children, each with its own nested `child_runs`.
> > // `child_run_ids` holds every descendant, at any depth.
> > for (const child of run.child_runs ?? []) {
> >   console.log(child.name, child.run_type, (child.child_runs ?? []).length);
> > }
> > console.log((run.child_run_ids ?? []).length, "descendants");
> > ```
>
> > [tab] After
> >
> > ```ts After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import { Client } from "langsmith";
> >
> > const client = new Client();
> > const project = await client.readProject({ projectName: "default" });
> > // A root run is its own trace, so `traceId` is also the run ID.
> > let traceId = "<trace-id>";
> >
> > const traceRuns = await client.traces.listRuns(traceId, {
> >   project_id: project.id,
> >   selects: ["ID", "NAME", "RUN_TYPE", "PARENT_RUN_IDS", "START_TIME", "END_TIME"],
> > });
> >
> > // `parent_run_ids` is the full ancestor chain, root first, closest parent last.
> > // A run is a descendant of any ID in that chain, at any depth, not only of the
> > // immediate parent. This flat list replaces `child_run_ids`.
> > const descendants = (traceRuns.items ?? []).filter((traceRun) =>
> >   (traceRun.parent_run_ids ?? []).includes(traceId),
> > );
> > console.log(descendants.length, "descendants");
> >
> > // Optional: group the runs by immediate parent to walk the trace as a tree,
> > // which is the information `child_runs` used to carry.
> > type TraceRun = NonNullable<typeof traceRuns.items>[number];
> > const byParent = new Map<string, TraceRun[]>();
> > for (const traceRun of traceRuns.items ?? []) {
> >   const ancestors = traceRun.parent_run_ids ?? [];
> >   if (ancestors.length === 0) continue;
> >   // The last ancestor is the immediate parent.
> >   const parentId = ancestors[ancestors.length - 1];
> >   byParent.set(parentId, [...(byParent.get(parentId) ?? []), traceRun]);
> > }
> >
> > const children = byParent.get(traceId) ?? [];
> > for (const child of children) {
> >   console.log(child.name, child.run_type, (byParent.get(child.id!) ?? []).length);
> > }
> > ```

> [tab] Java
>
> Nothing to migrate: the Java SDK never loaded child runs in one call, so use `client.traces().listRuns()` to walk a trace's runs.

> [tab] Go
>
> Nothing to migrate: the Go SDK never loaded child runs in one call, so use `client.Traces.ListRuns()` to walk a trace's runs.

> [tab] cURL
>
> Nothing to migrate: `GET /api/v1/runs/{run_id}` never returned child runs, so use `GET /api/v2/traces/{trace_id}/runs` to walk a trace's runs.

## Runs: get URL

Get the LangSmith UI URL for a run.

### Main changes

#### Method name

> [tab] Python
>
> | Before | After |
> | - | - |
> | `client.get_run_url()` | `client.runs.get_url()` |
>
> > [!NOTE]
> >
> > `client.runs.get_url()` is now async. Call it with `await`.
>
> See the [reference](https://reference.langchain.com/python/langsmith/_openapi_client/resources/runs/RunsResource/get_url) for the full parameter list.

> [tab] TypeScript
>
> | Before | After |
> | - | - |
> | `client.getRunUrl()` | `client.runs.getURL()` |
>
> See the [reference](https://reference.langchain.com/javascript/langsmith/_openapi_client/Langsmith/Runs/getURL) for the full parameter list.

> [tab] Java
>
> > [!NOTE]
> >
> > The Java SDK has no legacy equivalent for retrieving a run's UI URL.
>
> | Before | After |
> | - | - |
> | *(no legacy method)* | `client.runs().getUrl()` |
>
> See the [reference](https://javadoc.io/doc/com.langchain.smith/langsmith-java/latest/com/langchain/smith/services/blocking/RunService.html) for the full parameter list.

> [tab] Go
>
> > [!NOTE]
> >
> > The Go SDK has no legacy equivalent for retrieving a run's UI URL.
>
> | Before | After |
> | - | - |
> | *(no legacy method)* | `client.Runs.GetURL()` |
>
> See the [reference](https://pkg.go.dev/github.com/langchain-ai/langsmith-go#RunService.GetURL) for the full parameter list.

> [tab] cURL
>
> > [!NOTE]
> >
> > The REST API has no legacy equivalent for retrieving a run's UI URL.
>
> | Before | After |
> | - | - |
> | *(no legacy endpoint)* | `GET /api/v2/runs/{run_id}/url` |

#### Parameters

> [tab] Python
>
> > [!WARNING]
> >
> > `runs.get_url` needs the run's `project_id` and `trace_id` passed directly, instead of resolving them from a `run` object or a `project_name`/`project_id` fallback.
>
> | Before (`get_run_url`) | After (`runs.get_url`) | Notes |
> | - | - | - |
> | `run` (`RunBase`) | *(removed)* | No full run object needed; pass its identifying fields individually |
> | `project_name` | *(removed)* | No equivalent; resolve the project UUID yourself if you only have its name |
> | `project_id` | `project_id` | **Required**; still the project (session) UUID |
> | *(not available)* | `run_id` | **Required** (positional); the run's ID, previously read from `run.id` |
> | *(not available)* | `trace_id` | **Required**; the run's trace UUID, previously read from `run` internally |
> | *(not available)* | `start_time` | Optional; run's start time (RFC3339); omit if unknown |

> [tab] TypeScript
>
> > [!WARNING]
> >
> > `client.runs.getURL` needs the run's `project_id` and `trace_id` passed directly, instead of resolving them from a `run` object or a `runId` fallback.
>
> | Before (`getRunUrl`) | After (`getURL`) | Notes |
> | - | - | - |
> | `run` (`Run`) | *(removed)* | No full run object needed; pass its identifying fields individually |
> | `runId` | `runID` (positional) | Unchanged purpose; now the first positional argument instead of a named option |
> | `projectOpts` | *(removed)* | No equivalent; resolve the project UUID yourself |
> | *(not available)* | `project_id` | **Required**; `snake_case`; the project (session) UUID |
> | *(not available)* | `trace_id` | **Required**; `snake_case`; the run's trace UUID |
> | *(not available)* | `start_time` | Optional; `snake_case`; run's start time (RFC3339); omit if unknown |

> [tab] Java
>
> | Before | After (`RunGetUrlParams`) | Notes |
> | - | - | - |
> | *(no legacy method)* | `runId` | **Required** (positional); the run's ID |
> | *(no legacy method)* | `projectId()` | **Required**; the project (session) UUID |
> | *(no legacy method)* | `traceId()` | **Required**; the run's trace UUID |
> | *(no legacy method)* | `startTime()` | Optional; run's start time (RFC3339); omit if unknown |

> [tab] Go
>
> | Before | After (`RunGetURLParams`) | Notes |
> | - | - | - |
> | *(no legacy method)* | `runID` (positional) | **Required**; the run's ID |
> | *(no legacy method)* | `ProjectID` | **Required**; the project (session) UUID |
> | *(no legacy method)* | `TraceID` | **Required**; the run's trace UUID |
> | *(no legacy method)* | `StartTime` | Optional; run's start time (RFC3339); omit if unknown |

> [tab] cURL
>
> | Before | After (`GET /api/v2/runs/{run_id}/url`) | Notes |
> | - | - | - |
> | *(no legacy endpoint)* | `run_id` (path) | **Required** |
> | *(no legacy endpoint)* | `project_id` (query) | **Required**; the project (session) UUID |
> | *(no legacy endpoint)* | `trace_id` (query) | **Required**; the run's trace UUID |
> | *(no legacy endpoint)* | `start_time` (query) | Optional; run's start time (RFC3339); omit if unknown |

#### Response

> [tab] Python
>
> | Before | After | Notes |
> | - | - | - |
> | `str` (the URL) | `RunGetURLResponse.url` | Response is now wrapped in an object; read the `.url` attribute |

> [tab] TypeScript
>
> | Before | After | Notes |
> | - | - | - |
> | `string` (the URL) | `RunGetURLResponse.url` | Response is now wrapped in an object; read the `.url` property |

> [tab] Java
>
> | Before | After | Notes |
> | - | - | - |
> | *(no legacy method)* | `RunGetUrlResponse.url`() | Returns `Optional<String>` |

> [tab] Go
>
> | Before | After | Notes |
> | - | - | - |
> | *(no legacy method)* | `RunGetURLResponse.URL` | Returns a `string` |

> [tab] cURL
>
> | Before | After | Notes |
> | - | - | - |
> | *(no legacy endpoint)* | `{"url": "..."}` | JSON object with a single `url` field |

### Examples

#### Get a run's URL

> [tab] Python
>
> `get_run_url` accepts a full run object. `runs.get_url` is async and needs the run's `project_id` (its `session_id` under the old v1 schema) and `trace_id` passed individually, with `start_time` optional.
>
> > [tab] Before
> >
> > ```python Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > from langsmith import Client
> >
> > client = Client()
> > run_id = "<run-id>"
> > run = client.read_run(run_id)
> > url = client.get_run_url(run=run)
> > print(url)
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
> >     run_id = "<run-id>"
> >     project_id = "<project-id>"
> >     run = await client.runs.retrieve(
> >         run_id,
> >         project_id=project_id,
> >         selects=["ID", "PROJECT_ID", "TRACE_ID", "START_TIME"],
> >     )
> >     response = await client.runs.get_url(
> >         run.id,
> >         project_id=run.project_id,
> >         trace_id=run.trace_id,
> >         start_time=run.start_time.isoformat(),  # Optional, but speeds up retrieval
> >     )
> >     print(response.url)
> >
> >
> > asyncio.run(main())
> > ```

> [tab] TypeScript
>
> `getRunUrl` accepts a full run object. `runs.getURL` needs the run's `project_id` (its `session_id` under the old v1 schema) and `trace_id` passed individually, with `start_time` optional.
>
> > [tab] Before
> >
> > ```ts Before theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import { Client } from "langsmith";
> >
> > const client = new Client();
> > let runId = "<run-id>";
> > const url = await client.getRunUrl({ runId });
> > console.log(url);
> > ```
>
> > [tab] After
> >
> > ```ts After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import { Client } from "langsmith";
> >
> > const client = new Client();
> > let runId = "<run-id>";
> > let projectId = "<project-id>";
> > const run = await client.runs.retrieve(runId, {
> >   project_id: projectId,
> >   selects: ["ID", "PROJECT_ID", "TRACE_ID", "START_TIME"],
> > });
> > const response = await client.runs.getURL(run.id!, {
> >   project_id: run.project_id!,
> >   trace_id: run.trace_id!,
> >   start_time: run.start_time!, // Optional, but speeds up retrieval
> > });
> > console.log(response.url);
> > ```

> [tab] Java
>
> The Java SDK has no legacy equivalent. `runs().getUrl` needs the run's `projectId()` and `traceId()`, with `startTime()` optional.
>
> ```kotlin After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import com.langchain.smith.client.LangsmithClient
> import com.langchain.smith.client.okhttp.LangsmithOkHttpClient
> import com.langchain.smith.models.runs.RunGetUrlParams
> import com.langchain.smith.models.runs.RunRetrieveV2Params
>
> fun main() {
>     val client: LangsmithClient = LangsmithOkHttpClient.fromEnv()
>
>     var runId = "<run-id>"
>     var projectId = "<project-id>"
>     val run = client.runs().retrieveV2(
>         runId,
>         RunRetrieveV2Params.builder()
>             .projectId(projectId)
>             .addSelect(RunRetrieveV2Params.Select.ID)
>             .addSelect(RunRetrieveV2Params.Select.PROJECT_ID)
>             .addSelect(RunRetrieveV2Params.Select.TRACE_ID)
>             .addSelect(RunRetrieveV2Params.Select.START_TIME)
>             .build()
>     )
>
>     val response = client.runs().getUrl(
>         run.id().get(),
>         RunGetUrlParams.builder()
>             .projectId(run.projectId().get())
>             .traceId(run.traceId().get())
>             .startTime(run.startTime().get().toString()) // Optional, but speeds up retrieval
>             .build()
>     )
>     println(response.url().get())
> }
> ```

> [tab] Go
>
> The Go SDK has no legacy equivalent. `Runs.GetURL` needs the run's `ProjectID` and `TraceID`, with `StartTime` optional.
>
> ```go After theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> package main
>
> import (
> 	"context"
> 	"fmt"
> 	"time"
>
> 	"github.com/langchain-ai/langsmith-go"
> )
>
> func main() {
> 	ctx := context.Background()
> 	client := langsmith.NewClient()
>
> 	runID := "<run-id>"
> 	projectID := "<project-id>"
> 	run, err := client.Runs.GetV2(ctx, runID, langsmith.RunGetV2Params{
> 		ProjectID: langsmith.F(projectID),
> 		Selects: langsmith.F([]langsmith.RunGetV2ParamsSelect{
> 			langsmith.RunGetV2ParamsSelectID,
> 			langsmith.RunGetV2ParamsSelectProjectID,
> 			langsmith.RunGetV2ParamsSelectTraceID,
> 			langsmith.RunGetV2ParamsSelectStartTime,
> 		}),
> 	})
> 	if err != nil {
> 		panic(err.Error())
> 	}
>
> 	response, err := client.Runs.GetURL(ctx, run.ID, langsmith.RunGetURLParams{
> 		ProjectID: langsmith.F(run.ProjectID),
> 		TraceID:   langsmith.F(run.TraceID),
> 		StartTime: langsmith.F(run.StartTime.Format(time.RFC3339)), // Optional, but speeds up retrieval
> 	})
> 	if err != nil {
> 		panic(err.Error())
> 	}
> 	fmt.Println(response.URL)
> }
> ```

> [tab] cURL
>
> The REST API has no legacy equivalent. `GET /api/v2/runs/{run_id}/url` needs the run's `project_id` and `trace_id` query parameters, with `start_time` optional.
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> RUN_ID="<run-id>"
> PROJECT_ID="<project-id>"
>
> RUN=$(curl -s "https://api.smith.langchain.com/api/v2/runs/$RUN_ID?project_id=$PROJECT_ID&selects=TRACE_ID&selects=START_TIME" \
>   -H "x-api-key: $LANGSMITH_API_KEY")
> TRACE_ID=$(echo "$RUN" | jq -r '.trace_id')
> START_TIME=$(echo "$RUN" | jq -r '.start_time') # Optional, but speeds up retrieval
>
> curl "https://api.smith.langchain.com/api/v2/runs/$RUN_ID/url?project_id=$PROJECT_ID&trace_id=$TRACE_ID&start_time=$START_TIME" \
>   -H "x-api-key: $LANGSMITH_API_KEY"
> ```

## See also

* [Query runs](Migrate%20run%20queries%20to%20SmithDB.md)
* [Feedback and annotation queues](Migrate%20feedback%20and%20sharing%20methods%20to%20SmithDB.md)
* [Migration overview](Migrate%20to%20SmithDB-backed%20APIs.md)

# Agent Server changelog

**Subscribe**: Our changelog includes an [RSS feed](https://docs.langchain.com/langsmith/agent-server-changelog/rss.xml) that can integrate with [Slack](https://slack.com/help/articles/218688467-Add-RSS-feeds-to-Slack), [email](https://zapier.com/apps/email/integrations/rss/1441/send-new-rss-feed-entries-via-email), Discord bots like [Readybot](https://readybot.io/) or [RSS Feeds to Discord Bot](https://rss.app/en/bots/rssfeeds-discord-bot), and other subscription tools.

[Agent Server](../../Agent%20Server/Capabilities/Agent%20Server.md) is an API platform for creating and managing agent-based applications. It provides built-in persistence, a task queue, and supports deploying, configuring, and running assistants (agentic workflows) at scale. This changelog documents all notable updates, features, and fixes to Agent Server releases.

## Release cadence

`langgraph-api` maintains three release streams:

* `latest`: Published every morning with the latest bug fixes and test features. Semantic versioning uses a dev tag off the minor version, for example `0.9.0.dev1`.
* `rc` (release candidate): Published every three weeks and patched as needed during the bake window for critical bug backfills. Recommended for users who want to test a feature in the next stable release. Semantic versioning uses an rc tag off the minor version, for example `0.9.0rc1`.
* `stable`: Published every three weeks from rc. Patched for security-related dependency bumps or critical bug fixes. This is the default version used by new deployments and is recommended for production use. Semantic versioning uses minor bumps for regular promotions (for example `0.9.0`) and patch bumps for backfills (for example `0.9.1`).

Deployments use the newest `stable` version by default and are automatically updated to the newest `stable` version on each new revision. To pin to a specific version, set [`api_version`](LangGraph%20CLI.md#pinning-api-version) to the desired version in langgraph.json.

## v0.19

Latest version: `0.19.0rc1`

This minor line is still a release candidate. The last stable release is `0.18.0`.

### Changes

#### New Features

* `langgraph dev` runs on the Go core with SQLite, matching deployed servers more closely.
* On 0.19 only, set `FF_INMEM_CORE=false` to run `langgraph dev` on the Python in-memory runtime instead of the Go core; install `langgraph-runtime-inmem>=0.39,<0.40` if your environment doesn't already have it. Data saved by one runtime doesn't appear in the other.

#### Fixes

* Fixes checkpoint writes from JS graphs continuing to run after the graph's request to the checkpointer timed out.
* Fixes the per-priority queue metrics to count only runs that can start, and renames them to `lg_api_num_startable_runs` and `lg_api_startable_runs_wait_time_{max,med}`; the `/metrics?format=json` keys under `queue.by_priority` change to match.
* Fixes store reads over 4 MiB failing with `RESOURCE_EXHAUSTED`.

#### General Notes

* The Agent Server OpenAPI spec is now titled "LangSmith Agent Server".

> [accordion] v0.19 releases
>
> **2026-11-12**
>
> ## v0.19.0rc1
>
> ### New Features
>
> * `langgraph dev` runs on the Go core with SQLite, matching deployed servers more closely.
> * On 0.19 only, set `FF_INMEM_CORE=false` to run `langgraph dev` on the Python in-memory runtime instead of the Go core; install `langgraph-runtime-inmem>=0.39,<0.40` if your environment doesn't already have it. Data saved by one runtime doesn't appear in the other.
>
> ### Fixes
>
> * Fixes checkpoint writes from JS graphs continuing to run after the graph's request to the checkpointer timed out.
> * Fixes the per-priority queue metrics to count only runs that can start, and renames them to `lg_api_num_startable_runs` and `lg_api_startable_runs_wait_time_{max,med}`; the `/metrics?format=json` keys under `queue.by_priority` change to match.
> * Fixes store reads over 4 MiB failing with `RESOURCE_EXHAUSTED`.
>
> ### General Notes
>
> * The Agent Server OpenAPI spec is now titled "LangSmith Agent Server".

## v0.18

Latest version: `0.18.0`

### Changes

#### New Features

* When a deployment is stopped before becoming ready, shutdown logs now report which startup phase was stuck and for how long, including guidance when the phase is customer graph code.
* Updated CI infrastructure to run MCP conformance tests (`0.2.0-alpha.12`) against specific protocol revisions with isolated baselines.
* The MCP endpoint now also accepts clients on MCP revision 2026-07-28, which send their protocol version and capabilities with each request and discover the server with `server/discover`.
* Added `FF_RESUME_DRAINED_RUNS` to resume runs stopped by `RunControl.request_drain()` from their checkpoint instead of failing them. Requires langgraph 1.2.15+ in the deployment's dependencies; on older langgraph the flag is ignored with a startup warning.
* Hands off in-flight runs to another replica when a replica shuts down, on Postgres-backed deployments running langgraph 1.2.15 or later with `FF_RESUME_DRAINED_RUNS` enabled.
* Add `LANGGRAPH_THREAD_HISTORY_MAX_STATE_BYTES` (off by default) to cap how much thread state one history request returns. When set, history returns the newest state, then stops before the entry that would exceed the limit.
* GET and POST /threads/{thread_id}/history accept `select` to return only the named fields of each state, including single keys of the state values such as `values.messages`. On Postgres-backed servers, `select` also keeps the server from loading the unselected state.
* Supports OpenTelemetry SDK 1.45 and Prometheus exporter 0.66. Prometheus metrics now include `otel_scope_*` labels, and resource attributes include `service.instance.id`.
* JS graphs can call their own deployment with the SDK client, using the `langgraph_api:url` context variable as its `apiUrl`, including under custom auth.
* MCP clients on revision 2026-07-28 that support form elicitation are now asked for input when a graph pauses on `interrupt()` with a text question, and the tool call resumes with their answers.
* MCP clients on revision 2026-07-28 that don't declare form elicitation now get error -32021, naming the capability, when a tool pauses with a question a form could answer, instead of an explicit error result.
* MCP clients on revision 2026-07-28 now get typed forms for interrupts that declare a `response_schema`, and graphs that call MCP tools through `langchain.mcp` or `@langchain/mcp-adapters` pass those tools' form and URL questions on to the client.
* MCP clients on revision 2026-07-28 can now approve, edit, reject or answer tool calls that LangChain's human-in-the-loop middleware pauses, in Python and JS, in batched and per-call mode.
* Run attempts are now stored in postgres. Note that during rollout of this change active runs might run for more than the allocated number of retries on failure.
* Adds a feature flag to opt into multi-process execution mode, which spins up separate python processes to execute runs. Set `DISPATCH_MODE=multi-process` so the Go queue worker claims background runs and executes them. This is a beta feature in active development. It is only available for python at the moment.
* Emits terminal run failure metrics (`lg_api_run_failed_terminal_counter`, labeled by `error_category`) and sweeper failure metrics (`lg_api_sweep_failed_counter`) in multi-process mode.

#### Fixes

* MCP tool results are now JSON instead of Python repr() text, failed runs include the error message, and a tool that pauses on interrupt() returns an explicit error result instead of looking like a success.
* Preserves request IDs in worker logs for runs started or resumed through HTTP event-streaming commands.
* Fixes runs on Redis Cluster that kept running after a cancel or rollback request once a failover or scale-in removed a Redis node.
* Fixes A2A SendMessage ignoring non-blocking configuration.
* Fixes `input.respond` failing with `no_such_interrupt` while the interrupt's run is still going; the answer is now queued and applied when the run pauses.
* Fixes `input.respond` rejecting interrupts with `no_such_interrupt` when the run that raised them then failed, timed out or was cancelled, or was started from an earlier checkpoint.
* Ignores a `cron_id` sent in a run's or cron's `config.configurable`, `context` or `checkpoint`; the server sets it for cron runs.
* `run.start` input sent while a thread is paused on several interrupts now returns `invalid_argument` and leaves the thread paused, instead of starting a run that fails.
* Ignores server-reserved keys such as cron\_id and **after\_seconds** when they arrive in a v2 event-streaming run.start config, in a cron's stored checkpoint, or in a request header matched by http.configurable\_headers, as the REST routes already do for request bodies.
* Lower Agent Server memory use for streaming v2 SSE connections, which no longer keep a per-run event replay buffer.
* Thread event streams now reject a thread the caller can't read before streaming: `POST /threads/{thread_id}/stream/events` returns 403 or 404 instead of a 200 with an error frame (422 for a malformed thread ID), and the WebSocket endpoint closes with 4403, 4404 or 4422.
* A message sent with `run.start` while a run is going is now queued at once instead of after up to 5 seconds, and is no longer lost when sent while answered interrupts are running or after cancelling a run that had none open.
* Fixes run cancellation so a run that a worker starts during the cancel is still stopped, a run that finishes during the cancel keeps its final status, and running runs stop within one heartbeat interval even if their cancel signal is lost.
* Fixes the Redis run queue starting two runs of one thread at the same time, and keeps a thread's next run moving after a pending run is cancelled or deleted.
* Lets browser clients resume a run stream after a dropped connection by exposing the `Location` header to cross-origin requests.
* Fixes v3 streaming to respect graph output schemas for Python and JavaScript graphs.
* The MCP endpoint now runs on the official MCP Python SDK. GET and DELETE return 405, a bad Accept header returns 406, and an unknown MCP-Protocol-Version header returns 400.
* Fixes history and state operations failing for factory graphs when using the gRPC checkpointer.
* Accepts `stream_mode` `"tools"` on the run routes again, so `useStream` apps that track tool progress can send messages. These routes don't stream tool events yet.
* The thread stream honors the `stream_mode` filter that `threads.join_stream` (Python) and `threads.joinStream` (JS) send, instead of returning every event.
* Runs whose stream events can't be published now finish instead of stopping early and being recorded as successful, timed-out runs end their stream with an `error` event, and resumable runs in `messages` stream mode replay their message events when rejoined.
* Fixes JS graphs streamed in `messages` mode with subgraphs never sending `messages/complete`, and a JS graph process that crashes now and then no longer stops the whole server on its fourth exit.
* Fixes API errors for up to 90 seconds after the core restarts, and abandoned thread streams holding server resources until they were garbage collected.
* Fixes `http.disable_event_streaming`, which was ignored and left v2 event streaming mounted.
* Ends a streaming response whose client has stopped reading for 2 minutes, instead of keeping its stream open indefinitely.
* Fixes runs on threads that once used the event streaming endpoints streaming in the event streaming format instead of their requested stream modes.
* Fixes Playwright's browser driver and other subprocesses started from worker threads failing to launch on LangSmith Deployment.
* After a dropped connection, `runs.join_stream` and `runs.join` reconnect with the same `stream_mode` and `cancel_on_disconnect` instead of dropping them.
* Fixes thread history and checkpoint cleanup failing for threads whose first run used `durability="exit"` with a DeltaChannel.
* Stateless runs now return `Location` and `Content-Location` headers that point at the run, so clients can reconnect to a dropped stateless stream, and SDK `on_run_created` callbacks receive the run's temporary `thread_id`.
* Ignores the `webhook` field on run and cron requests when `http.disable_webhooks` is set, so the server no longer resolves or stores the client-supplied URL.
* Fixes a goroutine leak in the Go core when a Redis stream read fails after its client has stopped reading (optimized streaming).
* Fixes thread streams resumed with a `Last-Event-ID` of `0` or a millisecond timestamp returning no events, and `<ms>-*` ids failing on thread and run streams.
* Resuming a stream in `langgraph dev` with `Last-Event-ID` no longer skips events published in the same millisecond.
* Fixes JS graphs streaming one Anthropic reply under two message ids in legacy `messages` mode.
* The thread stream now accepts a negative `Last-Event-ID` such as `-1`, as run join does, and replays every event.
* Fixes `langgraph dev` letting a thread's next run start before an interrupted run has stopped, interrupts not stopping runs older than four minutes, and rollbacks requested before a restart rerunning the run.
* Fixes a memory leak in `langgraph dev` where every closed thread stream left behind a queue that kept receiving state updates.
* `stream_mode="events"` now omits events from runs tagged `nostream` (`langsmith:nostream` in LangGraph.js), as the `messages` stream mode does.
* Restores terminal error events for interrupted and rolled-back streamed runs, including interrupt replay on resumable streams, and reports user interrupts as interrupted rather than failed on v2 streams.
* Fixes `GET /threads/{thread_id}/runs/{run_id}/stream` returning only one mode when `stream_mode` lists several, as the Python SDK and JS SDK 1.12+ send.
* Fixes a bug where worker heartbeats could be lost on redis restart causing all active runs to be swept. Worker heartbeats now write to postgres. (The redis heartbeat is also preserved until `0.19.0` for backwards compatibility during upgrades).
* Stops copying the run context and other internal run config into every checkpoint's metadata, so checkpoint rows no longer grow with the size of the run context.
* Fixes startup failures with FastAPI included routers when custom-route authentication or auth-first middleware ordering is enabled, while preserving nested route path parameters for authentication and middleware.
* Ignores a `fairness_weight` returned by a priority callback, with a warning, instead of failing the run.
* Ships langgraph-sdk 0.4.12. Its `PrioritySettings` no longer offers `fairness_weight`, and its documentation now states that -5 runs first, matching the server.
* Exposes queue loop metrics when `DISPATCH_MODE` is set to `multi-process`.
* Allows redis-py 8.x in Agent Server images and user graph dependencies.
* Reduces memory use for thread get and search responses on large threads, because thread values are no longer decoded and re-encoded.
* Fixes dropped events in live streams on LangSmith-hosted deployments when a thread streams large state (over 8 MB) more than a minute apart.
* Fixes `run.start` with a fork checkpoint while the thread waits on an interrupt: it now starts a new run from that checkpoint instead of answering the interrupt, or being refused when several are pending.
* Replays a run's stored events in pages instead of inside Redis, so rejoining a long run no longer stalls Redis for other clients
* Fixes the per-priority queue metrics to count only runs that can start, and renames them to `lg_api_num_startable_runs` and `lg_api_startable_runs_wait_time_{max,med}`; the `/metrics?format=json` keys under `queue.by_priority` change to match.
* Fixes store reads over 4 MiB failing with `RESOURCE_EXHAUSTED`.

#### Security

* Store operations from graphs now reject namespace labels that are empty or contain `.`, as the HTTP store API does, so such a label can no longer read or change another namespace's items.
* Updates Python dependencies to address known security vulnerabilities.
* The MCP endpoint now rejects requests whose `Origin` header the server's CORS settings don't allow (HTTP 403), on every MCP revision, to block DNS rebinding. Loopback origins are always allowed, and a `*` wildcard allows no other origin, so list your browser MCP clients' origins in `CORS_ALLOW_ORIGINS` or `CORS_CONFIG`. Also fixes a `CORS_CONFIG` with only `allow_origin_regex` allowing every origin.
* Updates Go builds to mitigate the eMudhra certificate authority compromise.
* Updates Python certificate trust bundles.
* Patches Agent Server networking and tracing dependencies.
* Updates bundled dependencies to address security vulnerabilities.

> [accordion] v0.18 releases
>
> **2026-11-12**
>
> ## v0.18.0
>
> ### Fixes
>
> * Fixes the per-priority queue metrics to count only runs that can start, and renames them to `lg_api_num_startable_runs` and `lg_api_startable_runs_wait_time_{max,med}`; the `/metrics?format=json` keys under `queue.by_priority` change to match.
> * Fixes store reads over 4 MiB failing with `RESOURCE_EXHAUSTED`.
>
> ### Security
>
> * Updates bundled dependencies to address security vulnerabilities.
>
> **2026-11-11**
>
> ## v0.18.0rc8
>
> ### Fixes
>
> * Replays a run's stored events in pages instead of inside Redis, so rejoining a long run no longer stalls Redis for other clients
>
> **2026-11-10**
>
> ## v0.18.0rc7
>
> ### Security
>
> * Includes dependency and security maintenance updates.
>
> **2026-11-10**
>
> ## v0.18.0rc6
>
> ### Fixes
>
> * Fixes `run.start` with a fork checkpoint while the thread waits on an interrupt: it now starts a new run from that checkpoint instead of answering the interrupt, or being refused when several are pending.
>
> **2026-11-10**
>
> ## v0.18.0rc5
>
> ### Fixes
>
> * Allows redis-py 8.x in Agent Server images and user graph dependencies.
> * Reduces memory use for thread get and search responses on large threads, because thread values are no longer decoded and re-encoded.
> * Fixes dropped events in live streams on LangSmith-hosted deployments when a thread streams large state (over 8 MB) more than a minute apart.
>
> **2026-11-05**
>
> ## v0.18.0rc4
>
> ### New Features
>
> * Emits terminal run failure metrics (`lg_api_run_failed_terminal_counter`, labeled by `error_category`) and sweeper failure metrics (`lg_api_sweep_failed_counter`) in multi-process mode.
>
> ### Fixes
>
> * Ships langgraph-sdk 0.4.12. Its `PrioritySettings` no longer offers `fairness_weight`, and its documentation now states that -5 runs first, matching the server.
> * Exposes queue loop metrics when `DISPATCH_MODE` is set to `multi-process`.
>
> **2026-11-04**
>
> ## v0.18.0rc3
>
> ### Security
>
> * Includes dependency and security maintenance updates.
>
> **2026-11-03**
>
> ## v0.18.0rc2
>
> ### Fixes
>
> * Ignores a `fairness_weight` returned by a priority callback, with a warning, instead of failing the run.
>
> **2026-10-30**
>
> ## v0.18.0rc1
>
> ### New Features
>
> * When a deployment is stopped before becoming ready, shutdown logs now report which startup phase was stuck and for how long, including guidance when the phase is customer graph code.
> * Updated CI infrastructure to run MCP conformance tests (`0.2.0-alpha.12`) against specific protocol revisions with isolated baselines.
> * The MCP endpoint now also accepts clients on MCP revision 2026-07-28, which send their protocol version and capabilities with each request and discover the server with `server/discover`.
> * Added `FF_RESUME_DRAINED_RUNS` to resume runs stopped by `RunControl.request_drain()` from their checkpoint instead of failing them. Requires langgraph 1.2.15+ in the deployment's dependencies; on older langgraph the flag is ignored with a startup warning.
> * Hands off in-flight runs to another replica when a replica shuts down, on Postgres-backed deployments running langgraph 1.2.15 or later with `FF_RESUME_DRAINED_RUNS` enabled.
> * Add `LANGGRAPH_THREAD_HISTORY_MAX_STATE_BYTES` (off by default) to cap how much thread state one history request returns. When set, history returns the newest state, then stops before the entry that would exceed the limit.
> * GET and POST /threads/{thread_id}/history accept `select` to return only the named fields of each state, including single keys of the state values such as `values.messages`. On Postgres-backed servers, `select` also keeps the server from loading the unselected state.
> * Supports OpenTelemetry SDK 1.45 and Prometheus exporter 0.66. Prometheus metrics now include `otel_scope_*` labels, and resource attributes include `service.instance.id`.
> * JS graphs can call their own deployment with the SDK client, using the `langgraph_api:url` context variable as its `apiUrl`, including under custom auth.
> * MCP clients on revision 2026-07-28 that support form elicitation are now asked for input when a graph pauses on `interrupt()` with a text question, and the tool call resumes with their answers.
> * MCP clients on revision 2026-07-28 that don't declare form elicitation now get error -32021, naming the capability, when a tool pauses with a question a form could answer, instead of an explicit error result.
> * MCP clients on revision 2026-07-28 now get typed forms for interrupts that declare a `response_schema`, and graphs that call MCP tools through `langchain.mcp` or `@langchain/mcp-adapters` pass those tools' form and URL questions on to the client.
> * MCP clients on revision 2026-07-28 can now approve, edit, reject or answer tool calls that LangChain's human-in-the-loop middleware pauses, in Python and JS, in batched and per-call mode.
> * Run attempts are now stored in postgres. Note that during rollout of this change active runs might run for more than the allocated number of retries on failure.
> * Adds a feature flag to opt into multi-process execution mode, which spins up separate python processes to execute runs. Set `DISPATCH_MODE=multi-process` so the Go queue worker claims background runs and executes them. This is a beta feature in active development. It is only available for python at the moment.
>
> ### Fixes
>
> * MCP tool results are now JSON instead of Python repr() text, failed runs include the error message, and a tool that pauses on interrupt() returns an explicit error result instead of looking like a success.
> * Preserves request IDs in worker logs for runs started or resumed through HTTP event-streaming commands.
> * Fixes runs on Redis Cluster that kept running after a cancel or rollback request once a failover or scale-in removed a Redis node.
> * Fixes A2A SendMessage ignoring non-blocking configuration.
> * Fixes `input.respond` failing with `no_such_interrupt` while the interrupt's run is still going; the answer is now queued and applied when the run pauses.
> * Fixes `input.respond` rejecting interrupts with `no_such_interrupt` when the run that raised them then failed, timed out or was cancelled, or was started from an earlier checkpoint.
> * Ignores a `cron_id` sent in a run's or cron's `config.configurable`, `context` or `checkpoint`; the server sets it for cron runs.
> * `run.start` input sent while a thread is paused on several interrupts now returns `invalid_argument` and leaves the thread paused, instead of starting a run that fails.
> * Ignores server-reserved keys such as cron\_id and **after\_seconds** when they arrive in a v2 event-streaming run.start config, in a cron's stored checkpoint, or in a request header matched by http.configurable\_headers, as the REST routes already do for request bodies.
> * Lower Agent Server memory use for streaming v2 SSE connections, which no longer keep a per-run event replay buffer.
> * Thread event streams now reject a thread the caller can't read before streaming: `POST /threads/{thread_id}/stream/events` returns 403 or 404 instead of a 200 with an error frame (422 for a malformed thread ID), and the WebSocket endpoint closes with 4403, 4404 or 4422.
> * A message sent with `run.start` while a run is going is now queued at once instead of after up to 5 seconds, and is no longer lost when sent while answered interrupts are running or after cancelling a run that had none open.
> * Fixes run cancellation so a run that a worker starts during the cancel is still stopped, a run that finishes during the cancel keeps its final status, and running runs stop within one heartbeat interval even if their cancel signal is lost.
> * Fixes the Redis run queue starting two runs of one thread at the same time, and keeps a thread's next run moving after a pending run is cancelled or deleted.
> * Lets browser clients resume a run stream after a dropped connection by exposing the `Location` header to cross-origin requests.
> * Fixes v3 streaming to respect graph output schemas for Python and JavaScript graphs.
> * The MCP endpoint now runs on the official MCP Python SDK. GET and DELETE return 405, a bad Accept header returns 406, and an unknown MCP-Protocol-Version header returns 400.
> * Fixes history and state operations failing for factory graphs when using the gRPC checkpointer.
> * Accepts `stream_mode` `"tools"` on the run routes again, so `useStream` apps that track tool progress can send messages. These routes don't stream tool events yet.
> * The thread stream honors the `stream_mode` filter that `threads.join_stream` (Python) and `threads.joinStream` (JS) send, instead of returning every event.
> * Runs whose stream events can't be published now finish instead of stopping early and being recorded as successful, timed-out runs end their stream with an `error` event, and resumable runs in `messages` stream mode replay their message events when rejoined.
> * Fixes JS graphs streamed in `messages` mode with subgraphs never sending `messages/complete`, and a JS graph process that crashes now and then no longer stops the whole server on its fourth exit.
> * Fixes API errors for up to 90 seconds after the core restarts, and abandoned thread streams holding server resources until they were garbage collected.
> * Fixes `http.disable_event_streaming`, which was ignored and left v2 event streaming mounted.
> * Ends a streaming response whose client has stopped reading for 2 minutes, instead of keeping its stream open indefinitely.
> * Fixes runs on threads that once used the event streaming endpoints streaming in the event streaming format instead of their requested stream modes.
> * Fixes Playwright's browser driver and other subprocesses started from worker threads failing to launch on LangSmith Deployment.
> * After a dropped connection, `runs.join_stream` and `runs.join` reconnect with the same `stream_mode` and `cancel_on_disconnect` instead of dropping them.
> * Fixes thread history and checkpoint cleanup failing for threads whose first run used `durability="exit"` with a DeltaChannel.
> * Stateless runs now return `Location` and `Content-Location` headers that point at the run, so clients can reconnect to a dropped stateless stream, and SDK `on_run_created` callbacks receive the run's temporary `thread_id`.
> * Ignores the `webhook` field on run and cron requests when `http.disable_webhooks` is set, so the server no longer resolves or stores the client-supplied URL.
> * Fixes a goroutine leak in the Go core when a Redis stream read fails after its client has stopped reading (optimized streaming).
> * Fixes thread streams resumed with a `Last-Event-ID` of `0` or a millisecond timestamp returning no events, and `<ms>-*` ids failing on thread and run streams.
> * Resuming a stream in `langgraph dev` with `Last-Event-ID` no longer skips events published in the same millisecond.
> * Fixes JS graphs streaming one Anthropic reply under two message ids in legacy `messages` mode.
> * The thread stream now accepts a negative `Last-Event-ID` such as `-1`, as run join does, and replays every event.
> * Fixes `langgraph dev` letting a thread's next run start before an interrupted run has stopped, interrupts not stopping runs older than four minutes, and rollbacks requested before a restart rerunning the run.
> * Fixes a memory leak in `langgraph dev` where every closed thread stream left behind a queue that kept receiving state updates.
> * `stream_mode="events"` now omits events from runs tagged `nostream` (`langsmith:nostream` in LangGraph.js), as the `messages` stream mode does.
> * Restores terminal error events for interrupted and rolled-back streamed runs, including interrupt replay on resumable streams, and reports user interrupts as interrupted rather than failed on v2 streams.
> * Fixes `GET /threads/{thread_id}/runs/{run_id}/stream` returning only one mode when `stream_mode` lists several, as the Python SDK and JS SDK 1.12+ send.
> * Fixes a bug where worker heartbeats could be lost on redis restart causing all active runs to be swept. Worker heartbeats now write to postgres. (The redis heartbeat is also preserved until `0.19.0` for backwards compatibility during upgrades).
> * Stops copying the run context and other internal run config into every checkpoint's metadata, so checkpoint rows no longer grow with the size of the run context.
> * Fixes startup failures with FastAPI included routers when custom-route authentication or auth-first middleware ordering is enabled, while preserving nested route path parameters for authentication and middleware.
>
> ### Security
>
> * Store operations from graphs now reject namespace labels that are empty or contain `.`, as the HTTP store API does, so such a label can no longer read or change another namespace's items.
> * Updates Python dependencies to address known security vulnerabilities.
> * The MCP endpoint now rejects requests whose `Origin` header the server's CORS settings don't allow (HTTP 403), on every MCP revision, to block DNS rebinding. Loopback origins are always allowed, and a `*` wildcard allows no other origin, so list your browser MCP clients' origins in `CORS_ALLOW_ORIGINS` or `CORS_CONFIG`. Also fixes a `CORS_CONFIG` with only `allow_origin_regex` allowing every origin.
> * Updates Go builds to mitigate the eMudhra certificate authority compromise.
> * Updates Python certificate trust bundles.
> * Patches Agent Server networking and tracing dependencies.

## v0.17

Latest version: `0.17.2`

### Changes

#### New Features

* Adds `exclude_metadata` to thread search and count to exclude threads whose metadata matches any given object
* Added `FF_RESUME_DRAINED_RUNS` to resume runs stopped by `RunControl.request_drain()` from their checkpoint instead of failing them. Requires langgraph 1.2.15+ in the deployment's dependencies; on older langgraph the flag is ignored with a startup warning.
* Hands off in-flight runs to another replica when a replica shuts down, on Postgres-backed deployments running langgraph 1.2.15 or later with `FF_RESUME_DRAINED_RUNS` enabled.
* Add `LANGGRAPH_THREAD_HISTORY_MAX_STATE_BYTES` (off by default) to cap how much thread state one history request returns. When set, history returns the newest state, then stops before the entry that would exceed the limit.
* GET and POST /threads/{thread_id}/history accept `select` to return only the named fields of each state, including single keys of the state values such as `values.messages`. On Postgres-backed servers, `select` also keeps the server from loading the unselected state.
* Supports OpenTelemetry SDK 1.45 and Prometheus exporter 0.66. Prometheus metrics now include `otel_scope_*` labels, and resource attributes include `service.instance.id`.
* Defaults to the Go checkpointer on langgraph >= 0.5; set `PREFER_GRPC_CHECKPOINTER=false` to temporarily restore the Python checkpointer.
* Add lazy AES key rotation with versioned ciphertext envelopes and legacy-key migration.

#### Fixes

* Speeds up DeltaChannel reads on Postgres for threads that existed before the channel was added and had `update_state` run under langgraph before 1.2.13.
* Fixes a prune that could delete DeltaChannel history needed by later reads on threads where `update_state` ran under langgraph before 1.2.13.
* Fixes runs on Redis Cluster that kept running after a cancel or rollback request once a failover or scale-in removed a Redis node.
* Fixes `input.respond` failing with `no_such_interrupt` while the interrupt's run is still going; the answer is now queued and applied when the run pauses.
* Fixes `input.respond` rejecting interrupts with `no_such_interrupt` when the run that raised them then failed, timed out or was cancelled, or was started from an earlier checkpoint.
* `run.start` input sent while a thread is paused on several interrupts now returns `invalid_argument` and leaves the thread paused, instead of starting a run that fails.
* Preserves request IDs in worker logs for runs started or resumed through HTTP event-streaming commands.
* A message sent with `run.start` while a run is going is now queued at once instead of after up to 5 seconds, and is no longer lost when sent while answered interrupts are running or after cancelling a run that had none open.
* Thread event streams now reject a thread the caller can't read before streaming: `POST /threads/{thread_id}/stream/events` returns 403 or 404 instead of a 200 with an error frame (422 for a malformed thread ID), and the WebSocket endpoint closes with 4403, 4404 or 4422.
* Restores 0.17.0rc1 handling of `run.start` input sent while a run is going, so a resume sent right after an interrupt (for example from `RemoteGraph`) resumes the run instead of starting a new one with the resume value as input.
* Lower Agent Server memory use for streaming v2 SSE connections, which no longer keep a per-run event replay buffer.
* Fixes history and state operations failing for factory graphs when using the gRPC checkpointer.
* Fixes Playwright's browser driver and other subprocesses started from worker threads failing to launch on LangSmith Deployment.
* Fixes thread history and checkpoint cleanup failing for threads whose first run used `durability="exit"` with a DeltaChannel.
* JS graphs now pass each write's task path to the checkpointer, which DeltaChannel writes from parallel tasks need to replay in the order they ran.
* Fixes thread state reading back parallel writes to a delta channel in a different order than the run produced them, for writes made after this upgrade on Postgres and MongoDB checkpointers.
* Fixes run cancellation on the local dev server: rolling back a running background run no longer leaves that run's messages in the thread, and cancelling runs by status or deleting an assistant now actually stops runs that are executing.
* Fixes thread and run event streams closing as if they had finished when reading events fails; the stream now ends with an `error` frame.
* Fixed a bug where `cache_set()`'s `ttl` argument was ignored on the in-memory (non-Postgres/gRPC) cache backend; entries now expire at the requested ttl instead of the fixed 24-hour default.
* Removes the outdated "running in lite mode" warning that Agent Servers logged when validating with a LangSmith API key instead of a license key. These servers already have every feature.
* Fixes paused threads showing as `idle` after a run is cancelled or rolled back before its first checkpoint. A cancelled run now reports why in `cancel_reason`, instead of the thread's `error`.
* Fixes crons created with top-level `context` stopping after their first run on the in-memory runtime.
* Fixes `GET /threads/{thread_id}/storage` returning 500 when core-server owns all database access.
* Fixed Postgres connections closed server-side (e.g. by idle\_session\_timeout) being reused from the pool.
* Fixes AES-encrypted JSON data losing number formatting and precision (for example, `4.0` stored as `4`).
* Fixed `langgraph dev` losing data: thread state and long-term store items are now saved to `.langgraph_api/` every 10 seconds as intended, and a restart no longer deletes every thread when saved state references a class from the graph file or one that was moved or renamed (an unreadable file is kept as a `.bak` copy).
* Allows redis-py 8.x in Agent Server images and user graph dependencies.
* Replays a run's stored events in pages instead of inside Redis, so rejoining a long run no longer stalls Redis for other clients

#### Security

* Store operations from graphs now reject namespace labels that are empty or contain `.`, as the HTTP store API does, so such a label can no longer read or change another namespace's items.
* Updates Agent Server Go builds, Datadog initialization, uv, and telemetry certificate dependencies.
* Updates bundled dependencies to address security vulnerabilities.

#### General Notes

* Removes the built-in Python Postgres store; the Go store is now always used and `LANGGRAPH_STORE_BACKEND` is ignored. Custom stores and the in-memory runtime are unaffected.

> [accordion] v0.17 releases
>
> **2026-11-12**
>
> ## v0.17.2
>
> ### Fixes
>
> * Replays a run's stored events in pages instead of inside Redis, so rejoining a long run no longer stalls Redis for other clients
>
> ### Security
>
> * Updates bundled dependencies to address security vulnerabilities.
>
> **2026-11-03**
>
> ## v0.17.1
>
> ### Fixes
>
> * Allows redis-py 8.x in Agent Server images and user graph dependencies.
>
> ### Security
>
> * Updates Agent Server Go builds, Datadog initialization, uv, and telemetry certificate dependencies.
>
> **2026-10-29**
>
> ## v0.17.0
>
> ### Security
>
> * Includes dependency and security maintenance updates.
>
> **2026-10-28**
>
> ## v0.17.0rc8
>
> ### Fixes
>
> * Fixes thread history and checkpoint cleanup failing for threads whose first run used `durability="exit"` with a DeltaChannel.
>
> **2026-10-27**
>
> ## v0.17.0rc7
>
> ### Fixes
>
> * Fixes Playwright's browser driver and other subprocesses started from worker threads failing to launch on LangSmith Deployment.
>
> **2026-10-26**
>
> ## v0.17.0rc6
>
> ### New Features
>
> * Supports OpenTelemetry SDK 1.45 and Prometheus exporter 0.66. Prometheus metrics now include `otel_scope_*` labels, and resource attributes include `service.instance.id`.
>
> ### Fixes
>
> * Fixes history and state operations failing for factory graphs when using the gRPC checkpointer.
>
> **2026-10-23**
>
> ## v0.17.0rc5
>
> ### New Features
>
> * GET and POST /threads/{thread_id}/history accept `select` to return only the named fields of each state, including single keys of the state values such as `values.messages`. On Postgres-backed servers, `select` also keeps the server from loading the unselected state.
>
> **2026-10-19**
>
> ## v0.17.0rc4
>
> ### New Features
>
> * Add `LANGGRAPH_THREAD_HISTORY_MAX_STATE_BYTES` (off by default) to cap how much thread state one history request returns. When set, history returns the newest state, then stops before the entry that would exceed the limit.
>
> ### Fixes
>
> * Lower Agent Server memory use for streaming v2 SSE connections, which no longer keep a per-run event replay buffer.
>
> ### Security
>
> * Store operations from graphs now reject namespace labels that are empty or contain `.`, as the HTTP store API does, so such a label can no longer read or change another namespace's items.
>
> **2026-10-16**
>
> ## v0.17.0rc3
>
> ### New Features
>
> * Added `FF_RESUME_DRAINED_RUNS` to resume runs stopped by `RunControl.request_drain()` from their checkpoint instead of failing them. Requires langgraph 1.2.15+ in the deployment's dependencies; on older langgraph the flag is ignored with a startup warning.
> * Hands off in-flight runs to another replica when a replica shuts down, on Postgres-backed deployments running langgraph 1.2.15 or later with `FF_RESUME_DRAINED_RUNS` enabled.
>
> ### Fixes
>
> * Restores 0.17.0rc1 handling of `run.start` input sent while a run is going, so a resume sent right after an interrupt (for example from `RemoteGraph`) resumes the run instead of starting a new one with the resume value as input.
>
> **2026-10-15**
>
> ## v0.17.0rc2
>
> ### Fixes
>
> * Fixes runs on Redis Cluster that kept running after a cancel or rollback request once a failover or scale-in removed a Redis node.
> * Fixes `input.respond` failing with `no_such_interrupt` while the interrupt's run is still going; the answer is now queued and applied when the run pauses.
> * Fixes `input.respond` rejecting interrupts with `no_such_interrupt` when the run that raised them then failed, timed out or was cancelled, or was started from an earlier checkpoint.
> * `run.start` input sent while a thread is paused on several interrupts now returns `invalid_argument` and leaves the thread paused, instead of starting a run that fails.
> * Preserves request IDs in worker logs for runs started or resumed through HTTP event-streaming commands.
> * A message sent with `run.start` while a run is going is now queued at once instead of after up to 5 seconds, and is no longer lost when sent while answered interrupts are running or after cancelling a run that had none open.
> * Thread event streams now reject a thread the caller can't read before streaming: `POST /threads/{thread_id}/stream/events` returns 403 or 404 instead of a 200 with an error frame (422 for a malformed thread ID), and the WebSocket endpoint closes with 4403, 4404 or 4422.
>
> **2026-10-10**
>
> ## v0.17.0rc1
>
> ### New Features
>
> * Adds `exclude_metadata` to thread search and count to exclude threads whose metadata matches any given object
> * Defaults to the Go checkpointer on langgraph >= 0.5; set `PREFER_GRPC_CHECKPOINTER=false` to temporarily restore the Python checkpointer.
> * Add lazy AES key rotation with versioned ciphertext envelopes and legacy-key migration.
>
> ### Fixes
>
> * Speeds up DeltaChannel reads on Postgres for threads that existed before the channel was added and had `update_state` run under langgraph before 1.2.13.
> * Fixes a prune that could delete DeltaChannel history needed by later reads on threads where `update_state` ran under langgraph before 1.2.13.
> * JS graphs now pass each write's task path to the checkpointer, which DeltaChannel writes from parallel tasks need to replay in the order they ran.
> * Fixes thread state reading back parallel writes to a delta channel in a different order than the run produced them, for writes made after this upgrade on Postgres and MongoDB checkpointers.
> * Fixes run cancellation on the local dev server: rolling back a running background run no longer leaves that run's messages in the thread, and cancelling runs by status or deleting an assistant now actually stops runs that are executing.
> * Fixes thread and run event streams closing as if they had finished when reading events fails; the stream now ends with an `error` frame.
> * Fixed a bug where `cache_set()`'s `ttl` argument was ignored on the in-memory (non-Postgres/gRPC) cache backend; entries now expire at the requested ttl instead of the fixed 24-hour default.
> * Removes the outdated "running in lite mode" warning that Agent Servers logged when validating with a LangSmith API key instead of a license key. These servers already have every feature.
> * Fixes paused threads showing as `idle` after a run is cancelled or rolled back before its first checkpoint. A cancelled run now reports why in `cancel_reason`, instead of the thread's `error`.
> * Fixes crons created with top-level `context` stopping after their first run on the in-memory runtime.
> * Fixes `GET /threads/{thread_id}/storage` returning 500 when core-server owns all database access.
> * Fixed Postgres connections closed server-side (e.g. by idle\_session\_timeout) being reused from the pool.
> * Fixes AES-encrypted JSON data losing number formatting and precision (for example, `4.0` stored as `4`).
> * Fixed `langgraph dev` losing data: thread state and long-term store items are now saved to `.langgraph_api/` every 10 seconds as intended, and a restart no longer deletes every thread when saved state references a class from the graph file or one that was moved or renamed (an unreadable file is kept as a `.bak` copy).
>
> ### General Notes
>
> * Removes the built-in Python Postgres store; the Go store is now always used and `LANGGRAPH_STORE_BACKEND` is ignored. Custom stores and the in-memory runtime are unaffected.

## v0.16

Latest version: `0.16.11`

### Changes

#### New Features

* Added `A2A_A2UI_ENABLED` to turn A2UI on for every assistant in a deployment (a per-assistant `metadata.a2a.a2ui` setting still wins), and assistants with A2UI disabled now drop A2UI output instead of failing the request.
* Cancelled runs now report why they were cancelled. The `UserInterrupt` message (shown in LangSmith traces, the thread `error`, and server logs) distinguishes an explicit API cancel, `on_disconnect="cancel"`, a run superseded by `multitask_strategy="interrupt"` and `"rollback"` (naming the superseding run id), and assistant deletion.
* Added `GET /threads/{thread_id}/storage`, which reports the bytes a thread's checkpoints occupy in the built-in checkpointer (checkpoints, channel values per channel, pending writes). Returns 501 when a custom checkpointer is configured.
* Interrupts now include an optional `response_schema` (JSON Schema for the expected resume value) in thread state, run outputs, and A2A artifacts when the graph provides one.
* `/ok` now reports the health of each dependency it checks (database, Redis, the JS runtime, and core-api) under a `services` key, so a failing health check identifies which component is unhealthy. The HTTP status code is unchanged.
* The agent server now reports DeltaChannel usage. It adds `delta_channel_read_counter` (by `seed_kind`) and `delta_channel_replay_depth` metrics, plus deployment metadata for DeltaChannel usage and the installed `deepagents`, `langgraph-checkpoint` and `langgraph-checkpoint-postgres` versions.
* Supports OpenTelemetry SDK 1.45 and Prometheus exporter 0.66. Prometheus metrics now include `otel_scope_*` labels, and resource attributes include `service.instance.id`.

#### Fixes

* Studio auth users now include ls\_user\_id when available.
* Added support for A2UI DataParts containing a single message object.
* Pin the optional OpenTelemetry tracer's Requests dependency to a patched version independently of the application lockfiles.
* Fix global checkpointer TTL not being applied when runs implicitly create threads, including named threads created with `if_not_exists="create"`.
* Fix an in-memory rollback cancellation error when a run is deleted while its remaining stream events are being consumed.
* Fixed historical subgraph replay when using the gRPC checkpointer.
* Prevent obsolete Python package files and metadata from surviving dependency upgrades in Agent Server images.
* Fix gRPC checkpointer failures when private runtime config contains non-JSON values.
* Fix HTTPS webhooks failing with `AttributeError: 'bytes' object has no attribute 'encode'` on 0.15.0rc4 and later.
* Retriable errors during a run (such as transient database connection drops) are no longer emitted to streaming clients as terminal `error` events when the run is retried and recovers, so clients no longer fail requests that the server successfully completes.
* Fix TypeScript tool interrupts that resume without running the tool.
* A2A replies to a message made only of data parts no longer repeat the previous turn's answer or tool UI.
* Speeds up thread search by metadata on large thread tables, which could previously take seconds for filters matching few threads.
* Fixes a bug where loopback client calls might not be cancelled if their parent call was cancelled first.
* Fix agent server startup crash (`ImportError: _ExtendedAttributes`) caused by an unpinned Datadog tracer install pulling opentelemetry-api 1.45.0.
* Fixes crons created with top-level `context` failing with a 400 every time they fire.
* Fixes pending interrupts being erased when a run ends without a state snapshot, which made later answers fail with `no_such_interrupt`.
* Fixes threads on the in-memory server that stopped picking up new runs after the server was killed mid-run. Those runs are now retried on restart.
* Fixes a memory leak in the Go core's Postgres checkpointer caused by an outdated Datadog tracing dependency.
* Fixes `run_id` missing from checkpoint metadata in thread history and state on deployments that use the Go checkpointer.
* Cron scheduler claims due crons in bounded batches, so a large backlog no longer OOMs and drops crons.
* Fixes thread history failing for threads whose first run used `durability="exit"` with a delta channel.
* Speeds up state reads for threads that use DeltaChannel on Postgres when `PREFER_GRPC_CHECKPOINTER=false`.
* Speeds up keep-latest checkpoint pruning on long threads with Postgres.
* Threads using a delta channel with `durability="exit"` no longer lose state after the channel's first snapshot.
* Speeds up state reads and runs on long threads that use DeltaChannel with Postgres.
* Fixes DeltaChannel reads on Postgres that could miss the channel's snapshot on long threads, and speeds up reading older checkpoints and history.
* Fixes delta channels reading back empty or incomplete on threads where `update_state` ran under langgraph before 1.2.13.
* Speeds up DeltaChannel reads on Postgres for threads that existed before the channel was added and had `update_state` run under langgraph before 1.2.13.
* Fixes a prune that could delete DeltaChannel history needed by later reads on threads where `update_state` ran under langgraph before 1.2.13.
* Preserves request IDs in worker logs for runs started or resumed through HTTP event-streaming commands.
* Fixes history and state operations failing for factory graphs when using the gRPC checkpointer.
* Fixes Playwright's browser driver and other subprocesses started from worker threads failing to launch on LangSmith Deployment.
* Fixes JS deployments cancelling in-flight runs and streams on shutdown instead of draining gracefully.

#### Security

* Update the Go toolchain to 1.26.8 and upgrade golang.org/x/mod to address checksum database verification vulnerabilities.
* Update the JavaScript runtime's Hono dependency to 4.13.7.
* Pin patched IDNA in the isolated OpenTelemetry installation to address CVE-2026-45409.
* Update bundled npm tooling to address vulnerabilities in tar, ip-address, and brace-expansion.
* Ensure LangGraph Server images install AnyIO 4.14.2 or newer to address upstream security vulnerabilities.
* JS/TS custom auth handlers now have their request mutations applied by the server, including the store namespace rewrite used to scope items per user. This fixes cross-user store isolation in LangGraph.js deployments following the documented pattern. Namespaces produced by any custom auth handler, Python or JS, are now validated before reaching the store: an empty or period-containing label is rejected with 422 instead of writing an item that cannot be read back.
* Updates bundled Datadog serverless-init, ddtrace, langgraph-sdk, and MongoDB Go driver to clear known CVEs.
* Updates Agent Server's Go toolchain and HTTP/2 dependencies with upstream security fixes.
* Store operations from graphs now reject namespace labels that are empty or contain `.`, as the HTTP store API does, so such a label can no longer read or change another namespace's items.
* Updates PyJWT, urllib3 and Werkzeug to patched versions to address published security advisories.
* Updates undici in the JS graph server to a patched version to address published security advisories.
* Updates Agent Server's Go toolchain to mitigate CVE-2026-111943 in certificate-chain verification.
* Updates certifi, Hono and Vite to patched versions to address published security advisories.
* Patches Agent Server networking and tracing dependencies.
* Pins the optional OpenTelemetry tracer's certificate bundle.
* Updates bundled dependencies to address security vulnerabilities.

> [accordion] v0.16 releases
>
> **2026-11-12**
>
> ## v0.16.11
>
> ### Security
>
> * Updates bundled dependencies to address security vulnerabilities.
>
> **2026-11-03**
>
> ## v0.16.10
>
> ### Security
>
> * Patches Agent Server networking and tracing dependencies.
> * Pins the optional OpenTelemetry tracer's certificate bundle.
>
> **2026-10-28**
>
> ## v0.16.9
>
> ### Fixes
>
> * Fixes JS deployments cancelling in-flight runs and streams on shutdown instead of draining gracefully.
>
> **2026-10-27**
>
> ## v0.16.8
>
> ### Fixes
>
> * Fixes Playwright's browser driver and other subprocesses started from worker threads failing to launch on LangSmith Deployment.
>
> **2026-10-26**
>
> ## v0.16.7
>
> ### Fixes
>
> * Fixes history and state operations failing for factory graphs when using the gRPC checkpointer.
>
> **2026-10-23**
>
> ## v0.16.6
>
> ### New Features
>
> * Supports OpenTelemetry SDK 1.45 and Prometheus exporter 0.66. Prometheus metrics now include `otel_scope_*` labels, and resource attributes include `service.instance.id`.
>
> **2026-10-22**
>
> ## v0.16.5
>
> ### Security
>
> * Updates certifi, Hono and Vite to patched versions to address published security advisories.
>
> **2026-10-22**
>
> ## v0.16.4
>
> ### Security
>
> * Updates PyJWT, urllib3 and Werkzeug to patched versions to address published security advisories.
> * Updates undici in the JS graph server to a patched version to address published security advisories.
> * Updates Agent Server's Go toolchain to mitigate CVE-2026-111943 in certificate-chain verification.
>
> **2026-10-20**
>
> ## v0.16.2
>
> ### Security
>
> * Store operations from graphs now reject namespace labels that are empty or contain `.`, as the HTTP store API does, so such a label can no longer read or change another namespace's items.
>
> **2026-10-15**
>
> ## v0.16.1
>
> ### Fixes
>
> * Preserves request IDs in worker logs for runs started or resumed through HTTP event-streaming commands.
>
> ### Security
>
> * Updates Agent Server's Go toolchain and HTTP/2 dependencies with upstream security fixes.
>
> **2026-10-09**
>
> ## v0.16.0
>
> ### Security
>
> * Includes dependency and security maintenance updates.
>
> **2026-10-09**
>
> ## v0.16.0rc7
>
> ### New Features
>
> * The agent server now reports DeltaChannel usage. It adds `delta_channel_read_counter` (by `seed_kind`) and `delta_channel_replay_depth` metrics, plus deployment metadata for DeltaChannel usage and the installed `deepagents`, `langgraph-checkpoint` and `langgraph-checkpoint-postgres` versions.
>
> ### Fixes
>
> * Fixes thread history failing for threads whose first run used `durability="exit"` with a delta channel.
> * Speeds up state reads for threads that use DeltaChannel on Postgres when `PREFER_GRPC_CHECKPOINTER=false`.
> * Speeds up keep-latest checkpoint pruning on long threads with Postgres.
> * Threads using a delta channel with `durability="exit"` no longer lose state after the channel's first snapshot.
> * Speeds up state reads and runs on long threads that use DeltaChannel with Postgres.
> * Fixes DeltaChannel reads on Postgres that could miss the channel's snapshot on long threads, and speeds up reading older checkpoints and history.
> * Fixes delta channels reading back empty or incomplete on threads where `update_state` ran under langgraph before 1.2.13.
> * Speeds up DeltaChannel reads on Postgres for threads that existed before the channel was added and had `update_state` run under langgraph before 1.2.13.
> * Fixes a prune that could delete DeltaChannel history needed by later reads on threads where `update_state` ran under langgraph before 1.2.13.
>
> **2026-10-08**
>
> ## v0.16.0rc6
>
> ### Security
>
> * Updates bundled Datadog serverless-init, ddtrace, langgraph-sdk, and MongoDB Go driver to clear known CVEs.
>
> **2026-10-07**
>
> ## v0.16.0rc5
>
> ### Fixes
>
> * Fixes a memory leak in the Go core's Postgres checkpointer caused by an outdated Datadog tracing dependency.
> * Fixes `run_id` missing from checkpoint metadata in thread history and state on deployments that use the Go checkpointer.
> * Cron scheduler claims due crons in bounded batches, so a large backlog no longer OOMs and drops crons.
>
> **2026-10-06**
>
> ## v0.16.0rc4
>
> ### Security
>
> * Includes dependency and security maintenance updates.
>
> **2026-10-06**
>
> ## v0.16.0rc3
>
> ### Fixes
>
> * Fixes crons created with top-level `context` failing with a 400 every time they fire.
> * Fixes pending interrupts being erased when a run ends without a state snapshot, which made later answers fail with `no_such_interrupt`.
> * Fixes threads on the in-memory server that stopped picking up new runs after the server was killed mid-run. Those runs are now retried on restart.
>
> **2026-09-25**
>
> ## v0.16.0rc2
>
> ### Fixes
>
> * Fix agent server startup crash (`ImportError: _ExtendedAttributes`) caused by an unpinned Datadog tracer install pulling opentelemetry-api 1.45.0.
>
> **2026-09-25**
>
> ## v0.16.0rc1
>
> ### New Features
>
> * Added `A2A_A2UI_ENABLED` to turn A2UI on for every assistant in a deployment (a per-assistant `metadata.a2a.a2ui` setting still wins), and assistants with A2UI disabled now drop A2UI output instead of failing the request.
> * Cancelled runs now report why they were cancelled. The `UserInterrupt` message (shown in LangSmith traces, the thread `error`, and server logs) distinguishes an explicit API cancel, `on_disconnect="cancel"`, a run superseded by `multitask_strategy="interrupt"` and `"rollback"` (naming the superseding run id), and assistant deletion.
> * Added `GET /threads/{thread_id}/storage`, which reports the bytes a thread's checkpoints occupy in the built-in checkpointer (checkpoints, channel values per channel, pending writes). Returns 501 when a custom checkpointer is configured.
> * Interrupts now include an optional `response_schema` (JSON Schema for the expected resume value) in thread state, run outputs, and A2A artifacts when the graph provides one.
> * `/ok` now reports the health of each dependency it checks (database, Redis, the JS runtime, and core-api) under a `services` key, so a failing health check identifies which component is unhealthy. The HTTP status code is unchanged.
>
> ### Fixes
>
> * Studio auth users now include ls\_user\_id when available.
> * Added support for A2UI DataParts containing a single message object.
> * Pin the optional OpenTelemetry tracer's Requests dependency to a patched version independently of the application lockfiles.
> * Fix global checkpointer TTL not being applied when runs implicitly create threads, including named threads created with `if_not_exists="create"`.
> * Fix an in-memory rollback cancellation error when a run is deleted while its remaining stream events are being consumed.
> * Fixed historical subgraph replay when using the gRPC checkpointer.
> * Prevent obsolete Python package files and metadata from surviving dependency upgrades in Agent Server images.
> * Fix gRPC checkpointer failures when private runtime config contains non-JSON values.
> * Fix HTTPS webhooks failing with `AttributeError: 'bytes' object has no attribute 'encode'` on 0.15.0rc4 and later.
> * Retriable errors during a run (such as transient database connection drops) are no longer emitted to streaming clients as terminal `error` events when the run is retried and recovers, so clients no longer fail requests that the server successfully completes.
> * Fix TypeScript tool interrupts that resume without running the tool.
> * A2A replies to a message made only of data parts no longer repeat the previous turn's answer or tool UI.
> * Speeds up thread search by metadata on large thread tables, which could previously take seconds for filters matching few threads.
> * Fixes a bug where loopback client calls might not be cancelled if their parent call was cancelled first.
>
> ### Security
>
> * Update the Go toolchain to 1.26.8 and upgrade golang.org/x/mod to address checksum database verification vulnerabilities.
> * Update the JavaScript runtime's Hono dependency to 4.13.7.
> * Pin patched IDNA in the isolated OpenTelemetry installation to address CVE-2026-45409.
> * Update bundled npm tooling to address vulnerabilities in tar, ip-address, and brace-expansion.
> * Ensure LangGraph Server images install AnyIO 4.14.2 or newer to address upstream security vulnerabilities.
> * JS/TS custom auth handlers now have their request mutations applied by the server, including the store namespace rewrite used to scope items per user. This fixes cross-user store isolation in LangGraph.js deployments following the documented pattern. Namespaces produced by any custom auth handler, Python or JS, are now validated before reaching the store: an empty or period-containing label is rejected with 422 instead of writing an item that cannot be read back.

## v0.15

Latest version: `0.15.14`

### Changes

#### New Features

* Adds A2A\_A2UI\_ENABLED and A2A\_A2UI\_TOOL\_CALL\_RESULTS so A2UI can be enabled for every assistant and published from listed tools as spec DataParts next to unchanged tool results, accepts object-valued A2UI DataParts, and stops A2A replies from repeating an earlier turn's answer or UI.
* Supports OpenTelemetry SDK 1.45 and Prometheus exporter 0.66. Prometheus metrics now include `otel_scope_*` labels, and resource attributes include `service.instance.id`.

#### Fixes

* Expand `sse-starlette` compatibility to include the 3.4.x release line.
* Thread-stream runs can route traces to an additional LangSmith project.
* Add A2A task-only history responses with historyScope.
* Support A2UI v0.9 clients that negotiate with standard A2A extension headers and canonical MIME types.
* Fixed historical subgraph replay when using the gRPC checkpointer.
* Fix gRPC checkpointer failures when private runtime config contains non-JSON values.
* Fixed `/runs/wait`, `/runs/{run_id}/join` and the A2A task endpoint returning an empty `{"__interrupt__": []}` instead of the run's final state when the graph state merely contained the text `__interrupt__` (for example when a retrieval agent quoted documentation about interrupts).
* Fix HTTPS webhooks failing after the AnyIO security upgrade.
* Fix agent server startup crash (`ImportError: _ExtendedAttributes`) caused by an unpinned Datadog tracer install pulling opentelemetry-api 1.45.0.
* Fixes a memory leak in the Go core's Postgres checkpointer caused by an outdated Datadog tracing dependency.
* Fixes Playwright's browser driver and other subprocesses started from worker threads failing to launch on LangSmith Deployment.
* Update bundled ddtrace to 4.15.6 to address CVE-2026-116588.
* Fixes pyasn1 decoder denial-of-service vulnerabilities in Agent Server images.

#### Security

* Fix grpc-go security vulnerabilities by upgrading to 1.83.2.
* Fix vulnerabilities reported in the embedded Datadog init binary by updating it to 1.10.4.
* Refresh system packages when rebuilding Wolfi-based Python and Node Agent Server images.
* Update bundled npm tooling to address vulnerabilities in tar, ip-address, and undici.
* Backport Python dependency security updates and prevent obsolete Python package files from surviving upgrades.
* Backport Go and Hono security dependency updates.
* JS/TS custom auth handlers now have their request mutations applied by the server, including the store namespace rewrite used to scope items per user. This fixes cross-user store isolation in LangGraph.js deployments following the documented pattern. Namespaces produced by any custom auth handler, Python or JS, are now validated before reaching the store: an empty or period-containing label is rejected with 422 instead of writing an item that cannot be read back.
* Updates bundled Datadog serverless-init, ddtrace, langgraph-sdk, MongoDB Go driver, and OpenTelemetry SDK to clear known CVEs.
* Updates Agent Server's Go toolchain and HTTP/2 dependencies with upstream security fixes.
* Store operations from graphs now reject namespace labels that are empty or contain `.`, as the HTTP store API does, so such a label can no longer read or change another namespace's items.
* Updates bundled PyJWT, urllib3, Werkzeug, langgraph-sdk, and undici to clear known CVEs.
* Updates Agent Server's Go toolchain to mitigate CVE-2026-111943 in certificate-chain verification.
* Updates bundled certifi and Hono to clear known CVEs.
* Patches Agent Server networking and tracing dependencies and fixes a loopback cancellation race.
* Update bundled npm tooling to address vulnerabilities in brace-expansion and undici.
* Fixes a crash when decoding malformed compressed stream frames.

> [accordion] v0.15 releases
>
> **2026-11-12**
>
> ## v0.15.14
>
> ### Security
>
> * Fixes a crash when decoding malformed compressed stream frames.
>
> **2026-11-07**
>
> ## v0.15.13
>
> ### Security
>
> * Update bundled npm tooling to address vulnerabilities in brace-expansion and undici.
>
> **2026-11-06**
>
> ## v0.15.12
>
> ### Fixes
>
> * Update bundled ddtrace to 4.15.6 to address CVE-2026-116588.
> * Fixes pyasn1 decoder denial-of-service vulnerabilities in Agent Server images.
>
> **2026-11-04**
>
> ## v0.15.11
>
> ### Security
>
> * Patches Agent Server networking and tracing dependencies and fixes a loopback cancellation race.
>
> **2026-10-27**
>
> ## v0.15.10
>
> ### Fixes
>
> * Fixes Playwright's browser driver and other subprocesses started from worker threads failing to launch on LangSmith Deployment.
>
> **2026-10-23**
>
> ## v0.15.9
>
> ### New Features
>
> * Supports OpenTelemetry SDK 1.45 and Prometheus exporter 0.66. Prometheus metrics now include `otel_scope_*` labels, and resource attributes include `service.instance.id`.
>
> **2026-10-22**
>
> ## v0.15.8
>
> ### Security
>
> * Updates bundled certifi and Hono to clear known CVEs.
>
> **2026-10-22**
>
> ## v0.15.7
>
> ### Security
>
> * Updates Agent Server's Go toolchain to mitigate CVE-2026-111943 in certificate-chain verification.
>
> **2026-10-20**
>
> ## v0.15.6
>
> ### Security
>
> * Updates bundled PyJWT, urllib3, Werkzeug, langgraph-sdk, and undici to clear known CVEs.
>
> **2026-10-19**
>
> ## v0.15.5
>
> ### Security
>
> * Updates Agent Server's Go toolchain and HTTP/2 dependencies with upstream security fixes.
> * Store operations from graphs now reject namespace labels that are empty or contain `.`, as the HTTP store API does, so such a label can no longer read or change another namespace's items.
>
> **2026-10-08**
>
> ## v0.15.4
>
> ### Security
>
> * Updates bundled Datadog serverless-init, ddtrace, langgraph-sdk, MongoDB Go driver, and OpenTelemetry SDK to clear known CVEs.
>
> **2026-10-07**
>
> ## v0.15.3
>
> ### Fixes
>
> * Fixes a memory leak in the Go core's Postgres checkpointer caused by an outdated Datadog tracing dependency.
>
> **2026-10-06**
>
> ## v0.15.2
>
> ### Security
>
> * Includes dependency and security maintenance updates.
>
> **2026-09-25**
>
> ## v0.15.1
>
> ### Fixes
>
> * Fix agent server startup crash (`ImportError: _ExtendedAttributes`) caused by an unpinned Datadog tracer install pulling opentelemetry-api 1.45.0.
>
> **2026-09-25**
>
> ## v0.15.0
>
> ### Security
>
> * Includes dependency and security maintenance updates.
>
> **2026-09-24**
>
> ## v0.15.0rc8
>
> ### New Features
>
> * Adds A2A\_A2UI\_ENABLED and A2A\_A2UI\_TOOL\_CALL\_RESULTS so A2UI can be enabled for every assistant and published from listed tools as spec DataParts next to unchanged tool results, accepts object-valued A2UI DataParts, and stops A2A replies from repeating an earlier turn's answer or UI.
>
> **2026-09-24**
>
> ## v0.15.0rc7
>
> ### Security
>
> * JS/TS custom auth handlers now have their request mutations applied by the server, including the store namespace rewrite used to scope items per user. This fixes cross-user store isolation in LangGraph.js deployments following the documented pattern. Namespaces produced by any custom auth handler, Python or JS, are now validated before reaching the store: an empty or period-containing label is rejected with 422 instead of writing an item that cannot be read back.
>
> **2026-09-22**
>
> ## v0.15.0rc6
>
> ### Fixes
>
> * Fix HTTPS webhooks failing after the AnyIO security upgrade.
>
> **2026-09-22**
>
> ## v0.15.0rc5
>
> ### Fixes
>
> * Fixed `/runs/wait`, `/runs/{run_id}/join` and the A2A task endpoint returning an empty `{"__interrupt__": []}` instead of the run's final state when the graph state merely contained the text `__interrupt__` (for example when a retrieval agent quoted documentation about interrupts).
>
> **2026-09-22**
>
> ## v0.15.0rc4
>
> ### Security
>
> * Backport Python dependency security updates and prevent obsolete Python package files from surviving upgrades.
> * Backport Go and Hono security dependency updates.
>
> **2026-09-20**
>
> ## v0.15.0rc3
>
> ### Fixes
>
> * Fix gRPC checkpointer failures when private runtime config contains non-JSON values.
>
> ### Security
>
> * Update bundled npm tooling to address vulnerabilities in tar, ip-address, and undici.
>
> **2026-09-17**
>
> ## v0.15.0rc2
>
> ### Fixes
>
> * Fixed historical subgraph replay when using the gRPC checkpointer.
>
> ### Security
>
> * Refresh system packages when rebuilding Wolfi-based Python and Node Agent Server images.
>
> **2026-09-09**
>
> ## v0.15.0rc1
>
> ### Fixes
>
> * Expand `sse-starlette` compatibility to include the 3.4.x release line.
> * Thread-stream runs can route traces to an additional LangSmith project.
> * Add A2A task-only history responses with historyScope.
> * Support A2UI v0.9 clients that negotiate with standard A2A extension headers and canonical MIME types.
>
> ### Security
>
> * Fix grpc-go security vulnerabilities by upgrading to 1.83.2.
> * Fix vulnerabilities reported in the embedded Datadog init binary by updating it to 1.10.4.

## v0.14

Latest version: `0.14.10`

### Changes

#### New Features

* Custom encryption (`LANGGRAPH_ENCRYPTION`) now works with the gRPC Postgres checkpointer (`PREFER_GRPC_CHECKPOINTER=true`). Existing AES-encrypted checkpoints remain readable when migrating to custom encryption.
* Custom auth can now accept LangSmith API keys alongside the existing handler. Set `auth.allow_langsmith_api_keys: true` in `langgraph.json` (requires `LANGGRAPH_AUTH_TYPE=langsmith`). Requests with an `Authorization` header still go to custom auth. All others go to LangSmith (`x-api-key`). LangSmith-authenticated callers are have two parameters: ctx.user.identity = LangSmith user\_id (or missing) and ctx.permissions = \["authenticated"]. `@auth.on` handlers still run. Off by default.
* Supports OpenTelemetry SDK 1.45 and Prometheus exporter 0.66. Prometheus metrics now include `otel_scope_*` labels, and resource attributes include `service.instance.id`.

#### Fixes

* Fixed delta-channel reconstruction dropping the writes stored at the checkpoint a channel seeds from when that checkpoint predates the channel's migration to DeltaChannel.
* Custom encryption JSON handlers now receive an `EncryptionContext` matching the encrypted value. Checkpoint JSON columns use `field="metadata"` or `field="channel_values"`; run config metadata decrypts as `model="run"`, `field="metadata"`. Blob handlers are unchanged. Handlers ignoring model and field need no change, and the at-rest format is unchanged.
* Fix duplicate queue scheduler startup for deployments that use a custom FastAPI or Starlette app.
* Fixes webhook field allowlists.
* Fixed intermittent run creation failures caused by thread lock contention with custom encryption.
* Fixes a bug where the sweeper could fail for large back logs of pending runs.
* Fixes a problem where runs.join did not respect the cancel\_on\_disconnect parameter.
* Fixes v2 thread streaming failures caused by Redis Cluster `MOVED` redirects.
* Fixed cancellation of JavaScript agent runs so signal-aware graph nodes, tools, and model calls stop after an interrupt.
* Fixes a bug with historical subgraph replay.
* Refresh system packages when rebuilding Wolfi-based Python and Node Agent Server images.
* Fix gRPC checkpointer failures when private runtime config contains non-JSON values.
* Fix agent server startup crash (`ImportError: _ExtendedAttributes`) caused by an unpinned Datadog tracer install pulling opentelemetry-api 1.45.0.
* Fixes a memory leak in the Go core's Postgres checkpointer caused by an outdated Datadog tracing dependency.
* Fixes Playwright's browser driver and other subprocesses started from worker threads failing to launch on LangSmith Deployment.

#### Security

* Fixes a bug where create\_run auth could be bypassed by a run using if\_not\_exists.
* Fixed the default wildcard CORS policy so browser credentials are disabled unless trusted origins are configured.
* Bumping @langchain/langgraph to `1.4.12` and @langchain/langgraph-checkpoint to `1.1.5` to resolve [GHSA-j87f-x5h5-gr75](https://github.com/langchain-ai/langgraphjs/security/advisories/GHSA-j87f-x5h5-gr75).
* Patch AnyIO vulnerabilities in server dependencies, preserve HTTPS webhook compatibility, and prevent obsolete Python package files from surviving image upgrades.
* Update bundled npm tooling to address dependency vulnerabilities in server images.
* Updates Agent Server's Go toolchain and HTTP/2 dependencies with upstream security fixes.
* Patches Agent Server certificate bundles, networking, Go toolchain, and tracing dependencies.
* Updates gRPC certificate roots and pins the optional OpenTelemetry certificate bundle.

> [accordion] v0.14 releases
>
> **2026-11-06**
>
> ## v0.14.10
>
> ### Security
>
> * Includes dependency and security maintenance updates.
>
> **2026-10-31**
>
> ## v0.14.9
>
> ### Security
>
> * Patches Agent Server certificate bundles, networking, Go toolchain, and tracing dependencies.
> * Updates gRPC certificate roots and pins the optional OpenTelemetry certificate bundle.
>
> **2026-10-27**
>
> ## v0.14.8
>
> ### Fixes
>
> * Fixes Playwright's browser driver and other subprocesses started from worker threads failing to launch on LangSmith Deployment.
>
> **2026-10-23**
>
> ## v0.14.7
>
> ### New Features
>
> * Supports OpenTelemetry SDK 1.45 and Prometheus exporter 0.66. Prometheus metrics now include `otel_scope_*` labels, and resource attributes include `service.instance.id`.
>
> ### Security
>
> * Updates Agent Server's Go toolchain and HTTP/2 dependencies with upstream security fixes.
>
> **2026-10-07**
>
> ## v0.14.6
>
> ### Fixes
>
> * Fixes a memory leak in the Go core's Postgres checkpointer caused by an outdated Datadog tracing dependency.
>
> **2026-09-25**
>
> ## v0.14.5
>
> ### Fixes
>
> * Fix agent server startup crash (`ImportError: _ExtendedAttributes`) caused by an unpinned Datadog tracer install pulling opentelemetry-api 1.45.0.
>
> **2026-09-22**
>
> ## v0.14.4
>
> ### Security
>
> * Patch AnyIO vulnerabilities in server dependencies, preserve HTTPS webhook compatibility, and prevent obsolete Python package files from surviving image upgrades.
> * Update bundled npm tooling to address dependency vulnerabilities in server images.
>
> **2026-09-18**
>
> ## v0.14.3
>
> ### Fixes
>
> * Fix gRPC checkpointer failures when private runtime config contains non-JSON values.
>
> **2026-09-17**
>
> ## v0.14.2
>
> ### Fixes
>
> * Refresh system packages when rebuilding Wolfi-based Python and Node Agent Server images.
>
> **2026-09-14**
>
> ## v0.14.1
>
> ### Fixes
>
> * Fixes a bug with historical subgraph replay.
>
> **2026-09-08**
>
> ## v0.14.0
>
> ### Security
>
> * Includes dependency and security maintenance updates.
>
> **2026-09-08**
>
> ## v0.14.0rc10
>
> ### Fixes
>
> * Fixed cancellation of JavaScript agent runs so signal-aware graph nodes, tools, and model calls stop after an interrupt.
>
> **2026-09-04**
>
> ## v0.14.0rc9
>
> ### Security
>
> * Includes dependency and security maintenance updates.
>
> **2026-09-03**
>
> ## v0.14.0rc8
>
> ### Security
>
> * Includes dependency and security maintenance updates.
>
> **2026-09-01**
>
> ## v0.14.0rc7
>
> ### Security
>
> * Includes dependency and security maintenance updates.
>
> **2026-08-27**
>
> ## v0.14.0rc6
>
> ### Security
>
> * Includes dependency and security maintenance updates.
>
> **2026-08-26**
>
> ## v0.14.0rc5
>
> ### Security
>
> * Includes dependency and security maintenance updates.
>
> **2026-08-25**
>
> ## v0.14.0rc4
>
> ### Security
>
> * Includes dependency and security maintenance updates.
>
> **2026-08-25**
>
> ## v0.14.0rc3
>
> ## New Features
>
> * Custom auth can now accept LangSmith API keys alongside the existing handler. Set `auth.allow_langsmith_api_keys: true` in `langgraph.json` (requires `LANGGRAPH_AUTH_TYPE=langsmith`). Requests with an `Authorization` header still go to custom auth. All others go to LangSmith (`x-api-key`). LangSmith-authenticated callers are have two parameters: ctx.user.identity = LangSmith user\_id (or missing) and ctx.permissions = \["authenticated"]. `@auth.on` handlers still run. Off by default.
>
> ### Fixes
>
> * Fixes v2 thread streaming failures caused by Redis Cluster `MOVED` redirects.
>
> **2026-08-24**
>
> ## v0.14.0rc2
>
> ### Fixes
>
> * Fixes a problem where runs.join did not respect the cancel\_on\_disconnect parameter.
>
> **2026-08-21**
>
> ## v0.14.0rc1
>
> ### New Features
>
> * Custom encryption (`LANGGRAPH_ENCRYPTION`) now works with the gRPC Postgres checkpointer (`PREFER_GRPC_CHECKPOINTER=true`). Existing AES-encrypted checkpoints remain readable when migrating to custom encryption.
>
> ### Fixes
>
> * Fixed delta-channel reconstruction dropping the writes stored at the checkpoint a channel seeds from when that checkpoint predates the channel's migration to DeltaChannel.
> * Custom encryption JSON handlers now receive an `EncryptionContext` matching the encrypted value. Checkpoint JSON columns use `field="metadata"` or `field="channel_values"`; run config metadata decrypts as `model="run"`, `field="metadata"`. Blob handlers are unchanged. Handlers ignoring model and field need no change, and the at-rest format is unchanged.
> * Fix duplicate queue scheduler startup for deployments that use a custom FastAPI or Starlette app.
> * Fixes webhook field allowlists.
> * Fixed intermittent run creation failures caused by thread lock contention with custom encryption.
> * Fixes a bug where the sweeper could fail for large back logs of pending runs.
>
> ### Security
>
> * Fixes a bug where create\_run auth could be bypassed by a run using if\_not\_exists.
> * Fixed the default wildcard CORS policy so browser credentials are disabled unless trusted origins are configured.
> * Bumping @langchain/langgraph to `1.4.12` and @langchain/langgraph-checkpoint to `1.1.5` to resolve [GHSA-j87f-x5h5-gr75](https://github.com/langchain-ai/langgraphjs/security/advisories/GHSA-j87f-x5h5-gr75).

## v0.13

Latest version: `0.13.8`

### Changes

#### New Features

* Add per-method unary response-bytes rate limit to the core server.
* Add AWS IAM auth support for Redis connections.
* Accept A2A file parts as LangChain multimodal content blocks.
* Reduce JavaScript API Docker image size and SBOM component count.
* Add support for A2A FilePart outputs and configurable per-assistant media modes on agent cards.
* Add Python 3.14 support for Agent Server runtimes and images.
* Add `A2A_ALLOWED_TOOL_CALL_RESULTS` environment variable to restrict A2A tool call results to an allowlist of tool names.

#### Fixes

* Fix missing request metadata and trace correlation in Go core logs.
* Fix self-hosted Studio graph visualization for factory graphs with subgraphs when xray rendering is enabled.
* Disable rate limiting and warn when the rate-limit configuration is invalid instead of preventing server startup.
* Configure core rate limits exclusively through environment variables.
* Rename Postgres IAM auth provider environment variable to `AGENT_POSTGRES_IAM_AUTH_PROVIDER`.
* Rename Redis IAM auth provider environment variable to AGENT\_REDIS\_IAM\_AUTH\_PROVIDER.
* Fix queue entrypoint import order to prevent port binding conflicts when running alongside the API.
* Fix A2A streaming to return final output as an Artifact and filter task history to public conversation turns.
* Fix store search and list\_namespaces to scope namespace matching to segment boundaries and treat namespace labels as literal characters.
* Fix bug where cancelled runs could be retried if the worker died before acknowledging the cancellation.
* Fix JavaScript graph checkpointer failures when tool routing uses Send objects.
* Reject Send.timeout in gRPC serialization to prevent silent loss of per-task timeout semantics.
* Fix silent pruning failure for DeltaChannel threads when custom at-rest encryption is configured.
* Restore A2A tool-result DataParts in task history and streamed status updates.
* Restore support for `langgraph-sdk` versions starting at 0.3.5.
* Fix agent server startup crash (`ImportError: _ExtendedAttributes`) caused by an unpinned Datadog tracer install pulling opentelemetry-api 1.45.0.

#### Security

* Enforce thread authorization filters during conditional thread creation on the Postgres runtime ([GHSA-747p-c922-m55f](https://github.com/langchain-ai/helm/security/advisories/GHSA-747p-c922-m55f)). Affected versions did not consistently apply custom `@auth` filters on this path, so an authenticated user who knew another user's thread ID could create a run against that thread and observe or modify its conversation state. Deployments using only the in-memory runtime were not affected.
* Bumping @langchain/langgraph to 1.4.12 and @langchain/langgraph-checkpoint to 1.1.5 to resolve [GHSA-j87f-x5h5-gr75](https://github.com/langchain-ai/langgraphjs/security/advisories/GHSA-j87f-x5h5-gr75).
* Fix grpc-go security vulnerabilities by upgrading to 1.83.2.
* Fix vulnerabilities reported in the embedded Datadog init binary by updating it to 1.10.4.
* Pin the optional OpenTelemetry tracer's Requests dependency to a patched version.
* Update the Go toolchain to 1.26.8 and upgrade `golang.org/x/mod` to address checksum database verification vulnerabilities.
* Backport patched Python and JavaScript dependencies to address security advisories.
* Refresh system packages when rebuilding Wolfi-based Python and Node Agent Server images.
* Update bundled npm tooling to address dependency vulnerabilities in server images.
* Patch AnyIO vulnerabilities in server dependencies, preserve HTTPS webhook compatibility, and prevent obsolete Python package files from surviving image upgrades.

> [accordion] v0.13 releases
>
> **2026-09-25**
>
> ## v0.13.8
>
> ### Fixes
>
> * Fix agent server startup crash (`ImportError: _ExtendedAttributes`) caused by an unpinned Datadog tracer install pulling opentelemetry-api 1.45.0.
>
> **2026-09-22**
>
> ## v0.13.7
>
> ### Security
>
> * Update bundled npm tooling to address dependency vulnerabilities in server images.
> * Patch AnyIO vulnerabilities in server dependencies, preserve HTTPS webhook compatibility, and prevent obsolete Python package files from surviving image upgrades.
>
> **2026-09-17**
>
> ## v0.13.6
>
> ### Security
>
> * Refresh system packages when rebuilding Wolfi-based Python and Node Agent Server images.
>
> **2026-09-15**
>
> ## v0.13.5
>
> ### Security
>
> * Pin the optional OpenTelemetry tracer's Requests dependency to a patched version.
> * Update the Go toolchain to 1.26.8 and upgrade `golang.org/x/mod` to address checksum database verification vulnerabilities.
> * Backport patched Python and JavaScript dependencies to address security advisories.
>
> **2026-09-04**
>
> ## v0.13.4
>
> ### Security
>
> * Fix vulnerabilities reported in the embedded Datadog init binary by updating it to 1.10.4.
>
> **2026-09-01**
>
> ## v0.13.3
>
> ### Security
>
> * Fix grpc-go security vulnerabilities by upgrading to 1.83.2.
>
> **2026-08-28**
>
> ## v0.13.2
>
> ### Fixes
>
> * Restore support for `langgraph-sdk` versions starting at 0.3.5.
>
> **2026-08-27**
>
> ## v0.13.1
>
> ### Security
>
> * Includes dependency and security maintenance updates.
>
> **2026-08-20**
>
> ## v0.13.0
>
> ### Security
>
> * Includes dependency and security maintenance updates.
>
> **2026-08-20**
>
> ## v0.13.0rc6
>
> ### Security
>
> * Bumping @langchain/langgraph to 1.4.12 and @langchain/langgraph-checkpoint to 1.1.5 to resolve [GHSA-j87f-x5h5-gr75](https://github.com/langchain-ai/langgraphjs/security/advisories/GHSA-j87f-x5h5-gr75).
>
> **2026-08-17**
>
> ## v0.13.0rc5
>
> ### Security
>
> * Enforce thread authorization filters during conditional thread creation on the Postgres runtime ([GHSA-747p-c922-m55f](https://github.com/langchain-ai/helm/security/advisories/GHSA-747p-c922-m55f)). Affected versions did not consistently apply custom `@auth` filters on this path, so an authenticated user who knew another user's thread ID could create a run against that thread and observe or modify its conversation state. Deployments using only the in-memory runtime were not affected.
>
> **2026-08-12**
>
> ## v0.13.0rc4
>
> ### New Features
>
> * Add `A2A_ALLOWED_TOOL_CALL_RESULTS` environment variable to restrict A2A tool call results to an allowlist of tool names.
>
> **2026-08-08**
>
> ## v0.13.0rc3
>
> ### New Features
>
> * Add support for A2A FilePart outputs and configurable per-assistant media modes on agent cards.
> * Add Python 3.14 support for Agent Server runtimes and images.
>
> ### Fixes
>
> * Restore A2A tool-result DataParts in task history and streamed status updates.
>
> **2026-08-06**
>
> ## v0.13.0rc2
>
> ### Security
>
> * Includes dependency and security maintenance updates.
>
> **2026-08-04**
>
> ## v0.13.0rc1
>
> ### New Features
>
> * Add per-method unary response-bytes rate limit to the core server.
> * Add AWS IAM auth support for Redis connections.
> * Accept A2A file parts as LangChain multimodal content blocks.
> * Reduce JavaScript API Docker image size and SBOM component count.
>
> ### Fixes
>
> * Fix missing request metadata and trace correlation in Go core logs.
> * Fix self-hosted Studio graph visualization for factory graphs with subgraphs when xray rendering is enabled.
> * Disable rate limiting and warn when the rate-limit configuration is invalid instead of preventing server startup.
> * Configure core rate limits exclusively through environment variables.
> * Rename Postgres IAM auth provider environment variable to `AGENT_POSTGRES_IAM_AUTH_PROVIDER`.
> * Rename Redis IAM auth provider environment variable to AGENT\_REDIS\_IAM\_AUTH\_PROVIDER.
> * Fix queue entrypoint import order to prevent port binding conflicts when running alongside the API.
> * Fix A2A streaming to return final output as an Artifact and filter task history to public conversation turns.
> * Fix store search and list\_namespaces to scope namespace matching to segment boundaries and treat namespace labels as literal characters.
> * Fix bug where cancelled runs could be retried if the worker died before acknowledging the cancellation.
> * Fix JavaScript graph checkpointer failures when tool routing uses Send objects.
> * Reject Send.timeout in gRPC serialization to prevent silent loss of per-task timeout semantics.
> * Fix silent pruning failure for DeltaChannel threads when custom at-rest encryption is configured.

## v0.12

Latest version: `0.12.12`

### Changes

#### New Features

* Emit agent server metrics through the OpenTelemetry Prometheus client, updating latency units to milliseconds and renaming several pool counters.
* Add search result cost limiting for assistants, runs, crons, and threads.
* Add opt-in trace logging for the Redis run queue.
* Add gRPC-backed store backend supporting get and put operations with TTL.
* Add rate-limit configured-limit gauges and per-bucket key tags to runtime metrics.
* Add delete, search, and list namespaces to the gRPC store.
* Add `langsmith_session_name` field to runs to store the LangSmith tracing project name.
* Add Azure IAM auth support for Postgres connections.
* Add Azure IAM auth support for Redis connections.
* Add FIPS variants of Wolfi Python and Node.js server images.
* Add `A2A_ALLOWED_TOOL_CALL_RESULTS` environment variable to restrict A2A tool call results to an allowlist of tool names.

#### Fixes

* Update customer-facing support links to the Support Portal.
* Fix Redis Cluster pub/sub connection failures on TLS-only clusters.
* Fix race condition causing spurious no\_such\_interrupt errors on stateless thread commands.
* Fix custom stream events from subgraphs being dropped when using stream\_subgraphs=True on JS deployments.
* Fix join\_stream to correctly include namespaced subgraph events when filtering by stream mode.
* Fix OpenAPI docstring parsing warnings for affected assistant, event streaming, and inmem deploy routes.
* Fix race condition in WebSocket input respond by waiting for interrupt persistence.
* Assign JavaScript worker ports per entrypoint to prevent collisions in shared network namespaces.
* Fix histogram bucket configuration in OTLP metrics client.
* Fix per-run context not being forwarded to graph factory functions.
* Fix race condition in default LangSmith trace replica initialization.
* Fix race condition in in-memory stream publishing that could cause panics.
* Fix inmem thread creation to default values to None.
* Extend read-idle timeout for JS deployments from 15 to 30 seconds.
* Fix JavaScript remote graph runs to forward the requested durability mode.
* Disable rate limiting with a warning instead of preventing startup when given invalid rate-limit configuration.
* Rename IAM authentication environment variables for Postgres and Redis to prevent naming collisions.
* Accept and convert A2A FilePart inputs to LangChain multimodal content blocks.
* Fix custom JavaScript auth port conflicts between colocated API and queue worker processes.
* Fix store search and list\_namespaces to match namespace segments exactly and treat `_` and `%` as literal characters.
* Fix JS graph checkpointer failures when tool routing uses Send objects.
* Fix A2A streaming to return final outputs as Artifacts before terminal status and restrict task history to public client and agent conversation turns.
* Restore support for `langgraph-sdk` versions starting at 0.3.5.

#### Security

* Fix store API discarding authorization filters returned by auth handlers.
* Enable FIPS 140-3 compliance by default in the Go core-server.
* Enable FIPS mode for Node.js crypto in Wolfi/Chainguard FIPS Agent Server images by linking the base image's FIPS-validated OpenSSL provider.
* Enforce thread authorization filters during conditional thread creation on the Postgres runtime ([GHSA-747p-c922-m55f](https://github.com/langchain-ai/helm/security/advisories/GHSA-747p-c922-m55f)). Affected versions did not consistently apply custom `@auth` filters on this path, so an authenticated user who knew another user's thread ID could create a run against that thread and observe or modify its conversation state. Deployments using only the in-memory runtime were not affected.
* Bumping @langchain/langgraph to 1.4.12 and @langchain/langgraph-checkpoint to 1.1.5 to resolve [GHSA-j87f-x5h5-gr75](https://github.com/langchain-ai/langgraphjs/security/advisories/GHSA-j87f-x5h5-gr75).
* Fix grpc-go security vulnerabilities by upgrading to 1.83.2.
* Fix vulnerabilities reported in the embedded Datadog init binary by updating it to 1.10.4.
* Refresh system packages when rebuilding Wolfi-based Python and Node Agent Server images.
* Patch AnyIO vulnerabilities in server dependencies, preserve HTTPS webhook compatibility, and prevent obsolete Python package files from surviving image upgrades.
* Update bundled npm tooling to address dependency vulnerabilities in server images.

#### General Notes

* Remove unused `bun` runtime from server images.

> [accordion] v0.12 releases
>
> **2026-09-22**
>
> ## v0.12.12
>
> ### Security
>
> * Patch AnyIO vulnerabilities in server dependencies, preserve HTTPS webhook compatibility, and prevent obsolete Python package files from surviving image upgrades.
> * Update bundled npm tooling to address dependency vulnerabilities in server images.
>
> **2026-09-17**
>
> ## v0.12.11
>
> ### Security
>
> * Refresh system packages when rebuilding Wolfi-based Python and Node Agent Server images.
>
> **2026-09-15**
>
> ## v0.12.10
>
> ### Security
>
> * Fix grpc-go security vulnerabilities by upgrading to 1.83.2.
> * Fix vulnerabilities reported in the embedded Datadog init binary by updating it to 1.10.4.
>
> **2026-08-28**
>
> ## v0.12.9
>
> ### Fixes
>
> * Restore support for `langgraph-sdk` versions starting at 0.3.5.
>
> **2026-08-27**
>
> ## v0.12.8
>
> ### Security
>
> * Includes dependency and security maintenance updates.
>
> **2026-08-20**
>
> ## v0.12.7
>
> ### Security
>
> * Bumping @langchain/langgraph to 1.4.12 and @langchain/langgraph-checkpoint to 1.1.5 to resolve [GHSA-j87f-x5h5-gr75](https://github.com/langchain-ai/langgraphjs/security/advisories/GHSA-j87f-x5h5-gr75).
>
> **2026-08-18**
>
> ## v0.12.6
>
> ### Security
>
> * Includes dependency and security maintenance updates.
>
> **2026-08-17**
>
> ## v0.12.5
>
> ### Security
>
> * Enforce thread authorization filters during conditional thread creation on the Postgres runtime ([GHSA-747p-c922-m55f](https://github.com/langchain-ai/helm/security/advisories/GHSA-747p-c922-m55f)). Affected versions did not consistently apply custom `@auth` filters on this path, so an authenticated user who knew another user's thread ID could create a run against that thread and observe or modify its conversation state. Deployments using only the in-memory runtime were not affected.
>
> **2026-08-13**
>
> ## v0.12.4
>
> ### New Features
>
> * Add `A2A_ALLOWED_TOOL_CALL_RESULTS` environment variable to restrict A2A tool call results to an allowlist of tool names.
>
> **2026-08-11**
>
> ## v0.12.3
>
> ### Security
>
> * Includes dependency and security maintenance updates.
>
> **2026-08-09**
>
> ## v0.12.2
>
> ### Security
>
> * Includes dependency and security maintenance updates.
>
> **2026-08-07**
>
> ## v0.12.1
>
> ### Security
>
> * Includes dependency and security maintenance updates.
>
> **2026-08-04**
>
> ## v0.12.0
>
> ### Security
>
> * Includes dependency and security maintenance updates.
>
> **2026-08-04**
>
> ## v0.12.0rc10
>
> ### Fixes
>
> * Fix A2A streaming to return final outputs as Artifacts before terminal status and restrict task history to public client and agent conversation turns.
>
> **2026-08-04**
>
> ## v0.12.0rc9
>
> ### Security
>
> * Includes dependency and security maintenance updates.
>
> **2026-08-03**
>
> ## v0.12.0rc8
>
> ### Fixes
>
> * Fix store search and list\_namespaces to match namespace segments exactly and treat `_` and `%` as literal characters.
> * Fix JS graph checkpointer failures when tool routing uses Send objects.
>
> **2026-07-24**
>
> ## v0.12.0rc7
>
> ### Security
>
> * Includes dependency and security maintenance updates.
>
> **2026-07-23**
>
> ## v0.12.0rc6
>
> ### Security
>
> * Includes dependency and security maintenance updates.
>
> **2026-07-23**
>
> ## v0.12.0rc5
>
> ### Security
>
> * Includes dependency and security maintenance updates.
>
> **2026-07-21**
>
> ## v0.12.0rc4
>
> ### Fixes
>
> * Accept and convert A2A FilePart inputs to LangChain multimodal content blocks.
> * Fix custom JavaScript auth port conflicts between colocated API and queue worker processes.
>
> **2026-07-20**
>
> ## v0.12.0rc3
>
> ### Fixes
>
> * Rename IAM authentication environment variables for Postgres and Redis to prevent naming collisions.
>
> **2026-07-17**
>
> ## v0.12.0rc2
>
> ### Fixes
>
> * Disable rate limiting with a warning instead of preventing startup when given invalid rate-limit configuration.
>
> **2026-07-15**
>
> ## v0.12.0rc1
>
> ### New Features
>
> * Emit agent server metrics through the OpenTelemetry Prometheus client, updating latency units to milliseconds and renaming several pool counters.
> * Add search result cost limiting for assistants, runs, crons, and threads.
> * Add opt-in trace logging for the Redis run queue.
> * Add gRPC-backed store backend supporting get and put operations with TTL.
> * Add rate-limit configured-limit gauges and per-bucket key tags to runtime metrics.
> * Add delete, search, and list namespaces to the gRPC store.
> * Add `langsmith_session_name` field to runs to store the LangSmith tracing project name.
> * Add Azure IAM auth support for Postgres connections.
> * Add Azure IAM auth support for Redis connections.
> * Add FIPS variants of Wolfi Python and Node.js server images.
>
> ### Fixes
>
> * Update customer-facing support links to the Support Portal.
> * Fix Redis Cluster pub/sub connection failures on TLS-only clusters.
> * Fix race condition causing spurious no\_such\_interrupt errors on stateless thread commands.
> * Fix custom stream events from subgraphs being dropped when using stream\_subgraphs=True on JS deployments.
> * Fix join\_stream to correctly include namespaced subgraph events when filtering by stream mode.
> * Fix OpenAPI docstring parsing warnings for affected assistant, event streaming, and inmem deploy routes.
> * Fix race condition in WebSocket input respond by waiting for interrupt persistence.
> * Assign JavaScript worker ports per entrypoint to prevent collisions in shared network namespaces.
> * Fix histogram bucket configuration in OTLP metrics client.
> * Fix per-run context not being forwarded to graph factory functions.
> * Fix race condition in default LangSmith trace replica initialization.
> * Fix race condition in in-memory stream publishing that could cause panics.
> * Fix inmem thread creation to default values to None.
> * Extend read-idle timeout for JS deployments from 15 to 30 seconds.
> * Fix JavaScript remote graph runs to forward the requested durability mode.
>
> ### Security
>
> * Fix store API discarding authorization filters returned by auth handlers.
> * Enable FIPS 140-3 compliance by default in the Go core-server.
> * Enable FIPS mode for Node.js crypto in Wolfi/Chainguard FIPS Agent Server images by linking the base image's FIPS-validated OpenSSL provider.
>
> ### General Notes
>
> * Remove unused `bun` runtime from server images.

## v0.11

Latest version: `0.11.4`

### Changes

#### New Features

* Added DeltaChannel-aware pruning that preserves only the minimum ancestor checkpoints needed for state reconstruction, replacing the previous approach that refused to prune threads with active delta channels. Supported across the Postgres, SQLite, DeferredDelete, and in-memory runtimes.
* Added DeltaChannel-aware pruning for the MongoDB checkpointer, preserving only the minimum ancestor checkpoints and delta-channel blobs needed for state reconstruction.
* Added opt-in Prometheus metrics scrape support. Set `LSD_PROM_METRICS_ENABLED=true` to expose OTel metrics (run lifecycle, latency, stream, worker gauges) on a dedicated Prometheus scrape endpoint at port `LSD_PROM_METRICS_PORT` (default 9464). Datadog OTLP push continues to work alongside Prometheus when both are configured.
* Added opt-in Go core rate limits for unary core-api RPCs and Redis stream publish bytes, with Redis-backed GCRA enforcement, shadow/enforce modes, and `LS_RATE_LIMITS` bootstrap config with YAML override.
* Allow passing custom certificate and key files (`ssl_certfile`, `ssl_keyfile`) to run the dev server over HTTPS.
* Added `coreApi.runQueueTraceLog` config flag (`LSD_RUN_QUEUE_TRACE_LOG` env var, default `false`) to enable verbose Redis run-queue trace logs.
* Added rate-limit observability metrics, including configured-limit gauges (`lg_api_rate_limit_configured_rate`, `lg_api_rate_limit_configured_burst`) and a per-bucket `rate_limit_key` tag on decision, error, and cost metrics.
* Added core search cost rate limits for assistants, runs, crons, and threads search, wired through existing rate-limit config and metrics.
* Added the `langsmith_session_name` field to each run. This field is the LangSmith tracing project name when tracing is enabled. Exposed support via `/info` so Studio can detect API versions that support this field.
* Added `-fips` variants of Wolfi Python and JS server images (for example `3.13-wolfi-fips`, `22-wolfi-fips`), built with the Go FIPS 140 cryptographic module and FIPS-hardened OpenSSL for Node.
* Added DeltaChannel-aware pruning that preserves only the minimum ancestor checkpoints needed for state reconstruction, replacing the previous approach that refused to prune threads with active delta channels.
* Added the `langsmith_session_name` field to each run and exposed support via `/info` so Studio can detect API versions that support this field.

#### Fixes

* Bumping @langchain/langgraph to 1.4.12 and @langchain/langgraph-checkpoint to 1.1.5 to resolve [GHSA-j87f-x5h5-gr75](https://github.com/langchain-ai/langgraphjs/security/advisories/GHSA-j87f-x5h5-gr75).
* Fixed protocol v2 runs on JS graphs failing silently. The sidecar rejected `streamEvents` with a 400 due to strict stream-mode validation, the error was swallowed, and runs falsely reported success with 0 nodes executed. Relaxed stream-mode validation at the HTTP boundary and now raise a clear error on non-2xx sidecar responses instead of masking the failure.
* Fixed protocol v2 event streaming against JS sidecar (remote) graphs, which were incorrectly served through the legacy reconstruction path. Remote graphs now use LangGraphJS's native v3 stream for v2 event-streaming runs, resolving tool calls not rendering, headless interrupts never executing or resuming, and `400: tool_use ids must be unique` errors on the final message after a resume.
* Delete run now skips checkpoint deletion for threads using DeltaChannel and removes only the run record. Checkpoints that store delta writes later checkpoints depend on are preserved. Use thread prune APIs to reclaim checkpoint storage on delta-channel threads.
* Fixed Prometheus metrics export and aligned OpenTelemetry exporter configuration.
* Loosened the `starlette` lower bound introduced in 0.11.0rc1 back to `>=0.38.6` so `langgraph-api` can be installed alongside environments that pin older Starlette versions. Builds still resolve Starlette to 1.0.1 through the lockfile.
* Fixed HTTP `input.respond` validation for Event Streaming v2 to read pending interrupts from the durable thread row instead of rebuilding thread state, preventing valid HITL resumes from incorrectly returning `no_such_interrupt` after reconnects, redeploys, or thread-state lookup failures.
* Fixed `input.respond` so optional `update` and `goto` parameters are forwarded into the same `Command` as the resume value.
* Fixed DeltaChannel replay for channels that migrated from a non-delta channel to DeltaChannel. The checkpointer did not correctly recognize the head seed checkpoint, which could produce incorrect reconstructed state for non-additive reducers.
* Fixed custom stream events emitted from subgraphs not being forwarded to the client when using `stream_mode=["custom"]` with `stream_subgraphs=True` on JS deployments.
* Fixed a bug where calling `join_stream` with a `stream_mode` filter could cause non-message events from subgraphs to be incorrectly filtered from the results.
* Fixed JS worker port collisions when the API server and queue worker run as separate containers in the same Kubernetes pod. The queue entrypoint now offsets loopback ports.
* Fixed Redis Cluster pub/sub failing to connect on TLS-only clusters when `REDIS_CLUSTER=true`, which previously attempted to dial port `0`.
* Fixed OTLP latency histogram bucket configuration after the metrics migration so latency metrics use legacy second-scale buckets converted to milliseconds, restoring accurate p95/p99 for long HTTP polls, queue waits, and run execution.
* Made queue runs query field selection explicit for backwards compatibility, so new run schema fields can be added without breaking older server versions during rollbacks.
* Disable rate limiting with a warning instead of preventing startup when given invalid rate-limit configuration.

#### Security

* Enforce thread authorization filters during conditional thread creation on the Postgres runtime ([GHSA-747p-c922-m55f](https://github.com/langchain-ai/helm/security/advisories/GHSA-747p-c922-m55f)). Affected versions did not consistently apply custom `@auth` filters on this path, so an authenticated user who knew another user's thread ID could create a run against that thread and observe or modify its conversation state. Deployments using only the in-memory runtime were not affected.

#### General Notes

* Includes security dependency updates for PyJWT, LangSmith, cryptography, Hono, undici, `golang.org/x/net`, `golang.org/x/crypto`, and Starlette.
* Agent Server metrics are now emitted through the OpenTelemetry/Prometheus client on the dedicated Prometheus scrape endpoint (`LSD_PROM_METRICS_PORT`, default 9464). Set `LSD_PROM_METRICS_ENABLED=true` to enable the endpoint and `EXPOSE_INTERNAL_METRICS_PROMETHEUS=true` to expose the internal metrics migrated from the main API `/metrics` path. By default, the Prometheus endpoint serves only LSD Deployment UI metrics.
* **Potentially breaking** for Prometheus scrapers and dashboards: point collectors at the OTLP Prometheus port instead of the main API `/metrics` path. `lg_api_http_requests_latency_seconds` is now `lg_api_http_requests_latency` and reports milliseconds instead of seconds. Pool request counters now use a `_total` suffix (`lg_api_pg_pool_requests_queued_total`, `lg_api_pg_pool_requests_errors_total`). The `lg_api_pending_runs_wait_time_*` gauges are removed in favor of the `lg_api_run_queue_wait_time_1st_attempt` latency histogram.
* Wolfi (`chainguard-base-fips`) server images now ship a FIPS-compliant Go core-server and FIPS-mode Node, and no longer include the unused bun runtime.
* Applied stranded Postgres migration `061` for `thread_ls_user_id_idx` and `thread_assistant_id_idx` btree indexes.

> [accordion] v0.11 releases
>
> **2026-08-20**
>
> ## v0.11.4
>
> ### Security
>
> * Bumping @langchain/langgraph to 1.4.12 and @langchain/langgraph-checkpoint to 1.1.5 to resolve [GHSA-j87f-x5h5-gr75](https://github.com/langchain-ai/langgraphjs/security/advisories/GHSA-j87f-x5h5-gr75).
>
> **2026-08-17**
>
> ## v0.11.3
>
> ### Security
>
> * Enforce thread authorization filters during conditional thread creation on the Postgres runtime ([GHSA-747p-c922-m55f](https://github.com/langchain-ai/helm/security/advisories/GHSA-747p-c922-m55f)). Affected versions did not consistently apply custom `@auth` filters on this path, so an authenticated user who knew another user's thread ID could create a run against that thread and observe or modify its conversation state. Deployments using only the in-memory runtime were not affected.
>
> **2026-07-28**
>
> ## v0.11.2
>
> ### Security
>
> * Includes dependency and security maintenance updates.
>
> **2026-07-17**
>
> ## v0.11.1
>
> ### Fixes
>
> * Disable rate limiting with a warning instead of preventing startup when given invalid rate-limit configuration.
>
> **1970-01-01**
>
> ## v0.11.0
>
> ### New Features
>
> * Added DeltaChannel-aware pruning that preserves only the minimum ancestor checkpoints needed for state reconstruction, replacing the previous approach that refused to prune threads with active delta channels.
> * Added opt-in Prometheus metrics scrape support. Set `LSD_PROM_METRICS_ENABLED=true` to expose OTel metrics (run lifecycle, latency, stream, worker gauges) on a dedicated Prometheus scrape endpoint at port `LSD_PROM_METRICS_PORT` (default 9464). Datadog OTLP push continues to work alongside Prometheus when both are configured.
> * Added `coreApi.runQueueTraceLog` config flag (`LSD_RUN_QUEUE_TRACE_LOG` env var, default `false`) to enable verbose Redis run-queue trace logs.
> * Added the `langsmith_session_name` field to each run and exposed support via `/info` so Studio can detect API versions that support this field.
> * Added `-fips` variants of Wolfi Python and JS server images (for example `3.13-wolfi-fips`, `22-wolfi-fips`), built with the Go FIPS 140 cryptographic module and FIPS-hardened OpenSSL for Node.
>
> ### Fixes
>
> * Fixed protocol v2 runs on JS graphs failing silently. The sidecar rejected `streamEvents` with a 400 due to strict stream-mode validation, the error was swallowed, and runs falsely reported success with 0 nodes executed. Relaxed stream-mode validation at the HTTP boundary and now raise a clear error on non-2xx sidecar responses instead of masking the failure.
> * Fixed protocol v2 event streaming against JS sidecar (remote) graphs, which were incorrectly served through the legacy reconstruction path. Remote graphs now use LangGraphJS's native v3 stream for v2 event-streaming runs, resolving tool calls not rendering, headless interrupts never executing or resuming, and `400: tool_use ids must be unique` errors on the final message after a resume.
> * Delete run now skips checkpoint deletion for threads using DeltaChannel and removes only the run record. Checkpoints that store delta writes later checkpoints depend on are preserved. Use thread prune APIs to reclaim checkpoint storage on delta-channel threads.
> * Fixed HTTP `input.respond` validation for Event Streaming v2 to read pending interrupts from the durable thread row instead of rebuilding thread state, preventing valid HITL resumes from incorrectly returning `no_such_interrupt` after reconnects, redeploys, or thread-state lookup failures.
> * Fixed `input.respond` so optional `update` and `goto` parameters are forwarded into the same `Command` as the resume value.
> * Fixed DeltaChannel replay for channels that migrated from a non-delta channel to DeltaChannel. The checkpointer did not correctly recognize the head seed checkpoint, which could produce incorrect reconstructed state for non-additive reducers.
> * Fixed custom stream events emitted from subgraphs not being forwarded to the client when using `stream_mode=["custom"]` with `stream_subgraphs=True` on JS deployments.
> * Fixed a bug where calling `join_stream` with a `stream_mode` filter could cause non-message events from subgraphs to be incorrectly filtered from the results.
> * Fixed Redis Cluster pub/sub failing to connect on TLS-only clusters when `REDIS_CLUSTER=true`, which previously attempted to dial port `0`.
> * Made queue runs query field selection explicit for backwards compatibility, so new run schema fields can be added without breaking older server versions during rollbacks.
>
> **2026-07-09**
>
> ## v0.11.0rc14
>
> ### Fixes
>
> * Fixed OTLP latency histogram bucket configuration after the metrics migration so latency metrics use legacy second-scale buckets converted to milliseconds, restoring accurate p95/p99 for long HTTP polls, queue waits, and run execution.
> * Made queue runs query field selection explicit for backwards compatibility, so new run schema fields can be added without breaking older server versions during rollbacks.
>
> **2026-07-08**
>
> ## v0.11.0rc13
>
> ### Fixes
>
> * Fixed JS worker port collisions when the API server and queue worker run as separate containers in the same Kubernetes pod. The queue entrypoint now offsets loopback ports.
> * Fixed Redis Cluster pub/sub failing to connect on TLS-only clusters when `REDIS_CLUSTER=true`, which previously attempted to dial port `0`.
>
> **2026-07-08**
>
> ## v0.11.0rc12
>
> ### New Features
>
> * Added `-fips` variants of Wolfi Python and JS server images (for example `3.13-wolfi-fips`, `22-wolfi-fips`), built with the Go FIPS 140 cryptographic module and FIPS-hardened OpenSSL for Node.
>
> **2026-07-07**
>
> ## v0.11.0rc11
>
> ### New Features
>
> * Added the `langsmith_session_name` field to each run. This field is the LangSmith tracing project name when tracing is enabled. Exposed support via `/info` so Studio can detect API versions that support this field.
>
> ### General Notes
>
> * Applied stranded Postgres migration `061` for `thread_ls_user_id_idx` and `thread_assistant_id_idx` btree indexes.
>
> **2026-07-02**
>
> ## v0.11.0rc10
>
> ### New Features
>
> * Added core search cost rate limits for assistants, runs, crons, and threads search, wired through existing rate-limit config and metrics.
>
> ### General Notes
>
> * Wolfi (`chainguard-base-fips`) server images now ship a FIPS-compliant Go core-server and FIPS-mode Node, and no longer include the unused bun runtime.
>
> **2026-07-01**
>
> ## v0.11.0rc9
>
> ### Fixes
>
> * Fixed a bug where calling `join_stream` with a `stream_mode` filter could cause non-message events from subgraphs to be incorrectly filtered from the results.
>
> **2026-06-30**
>
> ## v0.11.0rc8
>
> ### General Notes
>
> * Agent Server metrics are now emitted through the OpenTelemetry/Prometheus client on the dedicated Prometheus scrape endpoint (`LSD_PROM_METRICS_PORT`, default 9464). Set `LSD_PROM_METRICS_ENABLED=true` to enable the endpoint and `EXPOSE_INTERNAL_METRICS_PROMETHEUS=true` to expose the internal metrics migrated from the main API `/metrics` path. By default, the Prometheus endpoint serves only LSD Deployment UI metrics.
> * **Potentially breaking** for Prometheus scrapers and dashboards: point collectors at the OTLP Prometheus port instead of the main API `/metrics` path. `lg_api_http_requests_latency_seconds` is now `lg_api_http_requests_latency` and reports milliseconds instead of seconds. Pool request counters now use a `_total` suffix (`lg_api_pg_pool_requests_queued_total`, `lg_api_pg_pool_requests_errors_total`). The `lg_api_pending_runs_wait_time_*` gauges are removed in favor of the `lg_api_run_queue_wait_time_1st_attempt` latency histogram.
>
> **2026-06-30**
>
> ## v0.11.0rc7
>
> ### Fixes
>
> * Fixed custom stream events emitted from subgraphs not being forwarded to the client when using `stream_mode=["custom"]` with `stream_subgraphs=True` on JS deployments.
>
> ### General Notes
>
> * Includes security dependency updates for PyJWT, LangSmith, cryptography, Hono, undici, `golang.org/x/net`, `golang.org/x/crypto`, and Starlette.
>
> **2026-06-26**
>
> ## v0.11.0rc6
>
> ### New Features
>
> * Added rate-limit observability metrics, including configured-limit gauges (`lg_api_rate_limit_configured_rate`, `lg_api_rate_limit_configured_burst`) and a per-bucket `rate_limit_key` tag on decision, error, and cost metrics.
>
> **2026-06-25**
>
> ## v0.11.0rc5
>
> ### Fixes
>
> * Fixed DeltaChannel replay for channels that migrated from a non-delta channel to DeltaChannel. The checkpointer did not correctly recognize the head seed checkpoint, which could produce incorrect reconstructed state for non-additive reducers.
>
> **2026-06-18**
>
> ## v0.11.0rc4
>
> ### Fixes
>
> * Fixed HTTP `input.respond` validation for Event Streaming v2 to read pending interrupts from the durable thread row instead of rebuilding thread state, preventing valid HITL resumes from incorrectly returning `no_such_interrupt` after reconnects, redeploys, or thread-state lookup failures.
> * Fixed `input.respond` so optional `update` and `goto` parameters are forwarded into the same `Command` as the resume value.
>
> **2026-06-18**
>
> ## v0.11.0rc3
>
> ### New Features
>
> * Added `coreApi.runQueueTraceLog` config flag (`LSD_RUN_QUEUE_TRACE_LOG` env var, default `false`) to enable verbose Redis run-queue trace logs.
>
> **2026-06-17**
>
> ## v0.11.0rc2
>
> ### Fixes
>
> * Loosened the `starlette` lower bound introduced in 0.11.0rc1 back to `>=0.38.6` so `langgraph-api` can be installed alongside environments that pin older Starlette versions. Builds still resolve Starlette to 1.0.1 through the lockfile.
>
> **2026-06-11**
>
> ## v0.11.0rc1
>
> ### General Notes
>
> * Includes dependency and security maintenance updates.
>
> ### New Features
>
> * Added DeltaChannel-aware pruning that preserves only the minimum ancestor checkpoints needed for state reconstruction, replacing the previous approach that refused to prune threads with active delta channels. Supported across the Postgres, SQLite, DeferredDelete, and in-memory runtimes.
> * Added DeltaChannel-aware pruning for the MongoDB checkpointer, preserving only the minimum ancestor checkpoints and delta-channel blobs needed for state reconstruction.
> * Added opt-in Prometheus metrics scrape support. Set `LSD_PROM_METRICS_ENABLED=true` to expose OTel metrics (run lifecycle, latency, stream, worker gauges) on a dedicated Prometheus scrape endpoint at port `LSD_PROM_METRICS_PORT` (default 9464). Datadog OTLP push continues to work alongside Prometheus when both are configured.
> * Added opt-in Go core rate limits for unary core-api RPCs and Redis stream publish bytes, with Redis-backed GCRA enforcement, shadow/enforce modes, and `LS_RATE_LIMITS` bootstrap config with YAML override.
> * Allow passing custom certificate and key files (`ssl_certfile`, `ssl_keyfile`) to run the dev server over HTTPS.
>
> ### Fixes
>
> * Fixed protocol v2 runs on JS graphs failing silently. The sidecar rejected `streamEvents` with a 400 due to strict stream-mode validation, the error was swallowed, and runs falsely reported success with 0 nodes executed. Relaxed stream-mode validation at the HTTP boundary and now raise a clear error on non-2xx sidecar responses instead of masking the failure.
> * Fixed protocol v2 event streaming against JS sidecar (remote) graphs, which were incorrectly served through the legacy reconstruction path. Remote graphs now use LangGraphJS's native v3 stream for v2 event-streaming runs, resolving tool calls not rendering, headless interrupts never executing or resuming, and `400: tool_use ids must be unique` errors on the final message after a resume.
> * Delete run now skips checkpoint deletion for threads using DeltaChannel and removes only the run record. Checkpoints that store delta writes later checkpoints depend on are preserved. Use thread prune APIs to reclaim checkpoint storage on delta-channel threads.
> * Fixed Prometheus metrics export and aligned OpenTelemetry exporter configuration.

## v0.10

Latest version: `0.10.3`

### Changes

#### New Features

* Added cron retrieval by ID endpoint (`GET /runs/crons/{cron_id}`).
* Added DeltaChannel-aware pruning that preserves only the minimum ancestor checkpoints needed for state reconstruction, replacing the previous behavior that refused to prune threads with active delta channels. Supported across the Postgres, SQLite, DeferredDelete, and in-memory runtimes.

#### Fixes

* Fixed Event Streaming v2 run start handling so checkpoint replay targets supplied via `config.configurable.checkpoint_id` are honored.
* Fixed Event Streaming v2 `input.respond` returning `no_such_interrupt` for legitimate interrupts on the postgres backend over HTTP `POST /commands`.
* Fixed a bug where a thread's `checkpoint_map` from a prior time-travel run would persist and contaminate a subsequent `Command(resume=...)`, causing nested subgraphs to incorrectly replay from the start.
* Fixed protocol v2 runs on JS graphs failing silently. The sidecar rejected `streamEvents` with a 400 due to strict stream-mode validation, the error was swallowed, and runs falsely reported success with 0 nodes executed. Relaxed stream-mode validation at the HTTP boundary and now raise a clear error on non-2xx sidecar responses instead of masking the failure.
* Fixed protocol v2 event streaming against JS sidecar (remote) graphs, which were incorrectly served through the legacy reconstruction path. Remote graphs now use LangGraphJS's native v3 stream for v2 event-streaming runs, resolving tool calls not rendering, headless interrupts never executing or resuming, and `400: tool_use ids must be unique` errors on the final message after a resume.
* Make queue runs query backwards compatible with later versions that add new fields.

#### Security

* **Potentially breaking** Loopback webhook targets are now denied by default to fix an authentication-bypass primitive ([GHSA-2c9q-c2q9-qgqv](https://github.com/langchain-ai/helm/security/advisories/GHSA-2c9q-c2q9-qgqv)). The `webhooks.url.disable_loopback` policy now defaults to `true`, blocking relative-URL webhooks (which dispatch through the in-process ASGI transport and bypass auth), as well as localhost / 127.x / ::1 / host.docker.internal absolute URLs and any hostname that DNS-resolves into the loopback range (mitigating DNS rebinding). Deployments that legitimately need loopback webhooks (e.g. `langgraph dev` with a localhost webhook receiver, or production setups that dispatch to a custom FastAPI route mounted on the same server) can opt back in by setting `webhooks.url.disable_loopback: false` in `langgraph.json` (or the equivalent `LANGGRAPH_WEBHOOKS` JSON env var). Only do this when you control the routes that loopback webhooks reach, as those routes are dispatched without authentication.
* **Potentially breaking** `POST /runs` and `POST /threads/{thread_id}/runs` now authorize the attached assistant via the`assistants.read` auth event (matching cron creation and direct GET) instead of the previously-used `assistants.search` event with an incomplete payload ([GHSA-jfj5-wrj9-63x4](https://github.com/langchain-ai/helm/security/advisories/GHSA-jfj5-wrj9-63x4)). Deployments that registered only `@auth.on.assistants.read` (and no `.search` handler) were vulnerable to a cross-user authorization bypass; their existing read handler will now be invoked on the run-creation path. As a defense-in-depth follow-up, client-supplied run/cron metadata is no longer forwarded into the `assistants.read` auth event payload from `Runs.put` or `Crons.put`, and inmem/postgres runtimes now agree on the value shape. Breaking change for deployments with custom auth handlers: (1) any `@auth.on.assistants.search` handler that was previously invoked during run creation is no longer called there—ensure you have an equivalent`@auth.on.assistants.read` handler returning the same owner-style filter; (2) `value["metadata"]` on the `assistants.read` event invoked from run/cron creation is no longer populated, so handlers that inspected or mutated it must move that logic into `@auth.on.runs.create_run` and `@auth.on.crons.create` and rely on returning a filter for ownership enforcement.
* Deployments now see a structured warning at server start listing every uncovered dispatch path along with a default-deny snippet to copy. The warning is silent for deployments that register a global `@auth.on` handler or that only use `@auth.authenticate` without any resource-level handlers.

#### General Notes

* v0.10.0rc1 includes breaking changes for security and correctness. Refer to the [Security section](#security) for more details.
* v0.10.0 is the stable promotion of the v0.10.0rc line. Note in particular the potentially breaking security changes in 0.10.0rc1.

> [accordion] v0.10 releases
>
> **2026-07-09**
>
> ## v0.10.3
>
> ### Fixes
>
> * Make queue runs query backwards compatible with later versions that add new fields.
>
> **2026-07-08**
>
> ## v0.10.2
>
> ### Fixes
>
> * Includes dependency and security maintenance updates.
>
> **2026-07-06**
>
> ## v0.10.1
>
> ### Fixes
>
> * Includes dependency and security maintenance updates.
>
> **2026-06-10**
>
> ## v0.10.0
>
> ### General Notes
>
> * v0.10.0 is the stable promotion of the v0.10.0rc line. Note in particular the potentially breaking security changes in 0.10.0rc1.
> * Includes dependency and security maintenance updates.
>
> ### New Features
>
> * Added DeltaChannel-aware pruning that preserves only the minimum ancestor checkpoints needed for state reconstruction, replacing the previous behavior that refused to prune threads with active delta channels. Supported across the Postgres, SQLite, DeferredDelete, and in-memory runtimes.
>
> **2026-06-05**
>
> ## v0.10.0rc3
>
> ### Fixes
>
> * Fixed protocol v2 event streaming against JS sidecar (remote) graphs, which were incorrectly served through the legacy reconstruction path. Remote graphs now use LangGraphJS's native v3 stream for v2 event-streaming runs, resolving tool calls not rendering, headless interrupts never executing or resuming, and `400: tool_use ids must be unique` errors on the final message after a resume.
>
> **2026-06-02**
>
> ## v0.10.0rc2
>
> ### Fixes
>
> * Fixed protocol v2 runs on JS graphs failing silently. The sidecar rejected `streamEvents` with a 400 due to strict stream-mode validation, the error was swallowed, and runs falsely reported success with 0 nodes executed. Relaxed stream-mode validation at the HTTP boundary and now raise a clear error on non-2xx sidecar responses instead of masking the failure.
>
> **2026-06-01**
>
> ## v0.10.0rc1
>
> ### General Notes
>
> * v0.10.0rc1 includes breaking changes for security and correctness. Refer to the [Security section](#security) for more details.
> * Includes dependency and security maintenance updates.
>
> ### New Features
>
> * Added cron retrieval by ID endpoint (`GET /runs/crons/{cron_id}`).
>
> ### Fixes
>
> * Fixed Event Streaming v2 run start handling so checkpoint replay targets supplied via `config.configurable.checkpoint_id` are honored.
> * Fixed Event Streaming v2 `input.respond` returning `no_such_interrupt` for legitimate interrupts on the postgres backend over HTTP `POST /commands`.
> * Fixed a bug where a thread's `checkpoint_map` from a prior time-travel run would persist and contaminate a subsequent `Command(resume=...)`, causing nested subgraphs to incorrectly replay from the start.
>
> ### Security
>
> * **Potentially breaking** Loopback webhook targets are now denied by default to fix an authentication-bypass primitive ([GHSA-2c9q-c2q9-qgqv](https://github.com/langchain-ai/helm/security/advisories/GHSA-2c9q-c2q9-qgqv)). The `webhooks.url.disable_loopback` policy now defaults to `true`, blocking relative-URL webhooks (which dispatch through the in-process ASGI transport and bypass auth), as well as localhost / 127.x / ::1 / host.docker.internal absolute URLs and any hostname that DNS-resolves into the loopback range (mitigating DNS rebinding). Deployments that legitimately need loopback webhooks (e.g. `langgraph dev` with a localhost webhook receiver, or production setups that dispatch to a custom FastAPI route mounted on the same server) can opt back in by setting `webhooks.url.disable_loopback: false` in `langgraph.json` (or the equivalent `LANGGRAPH_WEBHOOKS` JSON env var). Only do this when you control the routes that loopback webhooks reach, as those routes are dispatched without authentication.
> * **Potentially breaking** `POST /runs` and `POST /threads/{thread_id}/runs` now authorize the attached assistant via the`assistants.read` auth event (matching cron creation and direct GET) instead of the previously-used `assistants.search` event with an incomplete payload ([GHSA-jfj5-wrj9-63x4](https://github.com/langchain-ai/helm/security/advisories/GHSA-jfj5-wrj9-63x4)). Deployments that registered only `@auth.on.assistants.read` (and no `.search` handler) were vulnerable to a cross-user authorization bypass; their existing read handler will now be invoked on the run-creation path. As a defense-in-depth follow-up, client-supplied run/cron metadata is no longer forwarded into the `assistants.read` auth event payload from `Runs.put` or `Crons.put`, and inmem/postgres runtimes now agree on the value shape. Breaking change for deployments with custom auth handlers: (1) any `@auth.on.assistants.search` handler that was previously invoked during run creation is no longer called there—ensure you have an equivalent`@auth.on.assistants.read` handler returning the same owner-style filter; (2) `value["metadata"]` on the `assistants.read` event invoked from run/cron creation is no longer populated, so handlers that inspected or mutated it must move that logic into `@auth.on.runs.create_run` and `@auth.on.crons.create` and rely on returning a filter for ownership enforcement.
> * Deployments now see a structured warning at server start listing every uncovered dispatch path along with a default-deny snippet to copy. The warning is silent for deployments that register a global `@auth.on` handler or that only use `@auth.authenticate` without any resource-level handlers.

## v0.9.0

### General Notes

* v0.9.0 is the stable promotion of the v0.9.0rc line.
* Includes dependency and security maintenance updates.

**2026-05-11**

## v0.9.0rc1

### General Notes

* Added cron metadata filtering in /runs/crons/search and /runs/crons/count, matching metadata filter behavior already available for assistants/threads.
* Added Postgres checkpointer pool tuning knobs for cases when loading lots of large checkpoints at once. LANGGRAPH\_CHECKPOINTER\_POSTGRES\_POOL\_MIN\_SIZE and LANGGRAPH\_CHECKPOINTER\_POSTGRES\_POOL\_TIMEOUT\_SECONDS can now be set.
* Fixed a crash in update\_state in the mongo checkpointer when a thread has no prior checkpoint.
* Includes dependency updates for security vulnerabilities.

### New Features

#### Delta channel support

Delta channels are now supported so checkpoints can store incremental state updates instead of repeatedly storing full channel payloads, which helps with large, append-heavy state like message histories.

To use, define state channels with LangGraph's DeltaChannel reducer pattern in your graph state.
This behavior is enabled when the installed langgraph is >= 1.2.
Docs: [DeltaChannel reference](https://docs.langchain.com/oss/python/langgraph/pregel.md#deltachannel)

#### Event streaming APIs

Event streaming APIs are being introduced, with a unified event-streaming surface intended for richer real-time run events and command/event workflows.

The feature flag `FF_V2_EVENT_STREAMING` can be set to true to enable the new event streaming APIs.

The new endpoints include:

* `POST /threads/{thread_id}/stream/events`
* `POST /threads/{thread_id}/commands`
* `WS /threads/{thread_id}/stream/events`

Docs:

* [Agent Server API reference](Agent%20Server%20API/Agent%20Server%20API%20reference.md)
* [LangGraph event streaming reference](https://docs.langchain.com/oss/python/langgraph/event-streaming.md)

**2026-05-05**

## v0.8.7

* Reverted changes from #3296 temporarily to address issues with the upcoming 0.8.6 release.

**2026-05-04**

## v0.8.6

* Integrated DeltaChannel into the Postgres checkpointer for efficient snapshot and delta processing.
* Introduced new v2 streaming primitives to the API for enhanced data handling.
* Enabled dynamic port discovery for in-memory operations.
* Linked A2A tool result messages with `toolCallId` correlation metadata to maintain alignment with initiating tool calls.
* Fixed an issue where JS studio experiments didn't update the experiment screen, ensuring correct run routing to the experiment's tracing project with `reference_example_id` set.

**2026-04-30**

## v0.8.5

* Addressed security vulnerabilities in langgraph JavaScript dependencies reported by Datadog and npm.

**2026-04-29**

## v0.8.4

* Included trace/span IDs in access logs to improve trace correlation in Datadog and OTel.

**2026-04-28**

## v0.8.3

* Added support for IAM-based authentication with Google Cloud Memorystore in cluster mode for secure access.

**2026-04-27**

## v0.8.2

* Fixed the `langgraph-api` queue entrypoint to start correctly on IPv6-only clusters by ensuring the health/metrics server appropriately binds with an IPv6 literal.

**2026-04-23**

## v0.8.1

* Improved performance by skipping the large `values` column in thread state and run endpoints when the full thread body isn't required.
* Capped checkpoint ingestion batch size and delay window to minimize long-running transactions and row lock contention, with new configuration flags for batch size and delay control.

**2026-04-16**

## v0.8.0

This minor version moves run queue polling from Postgres to Redis, saving database load and improving performance.

Under the hood, Agent Server uses a durable run queue to manage run execution. Workers poll the queue for new runs and execute them. Previously, the queue polling logic went through Postgres. This could result in long running queries especially under high load. With this update, the queue polling logic now goes through Redis and then fetches run details from Postgres. This makes the hot path for queue polling substantially faster and reduces the load on the database.

This does not require code changes to upgrade, but there are a few things to be aware of:

* In the deployment immediately after upgrading, the queue will shift over. There may be a brief window where threads are scheduled non-chronologically. Run execution order is still guaranteed within each thread.
* **Self-hosted only:** Redis traffic may increase slightly. In internal testing, the increase was modest.
* **Self-hosted only:** This release raises the minimum Redis version to 6.2. The Redis-backed run queue enqueues runs with the `ZADD ... LT` flag, which was added in Redis 6.2. On Redis 5.0 through 6.1, run enqueue fails with a generic `ERR syntax error` that does not indicate a version mismatch, so upgrade Redis to 6.2 or later before deploying this version. Valkey 8 includes the flag. See [self-hosted dependency versions](../../../LangSmith%20setup/Self-hosted/Install%20an%20instance/Minimum%20versions%20for%20self-hosting%20dependencies.md).

**2026-04-15**

## v0.7.103

* Resolved migration version conflict for checkpoint\_delete\_queue, ensuring proper execution and added duplicate version detection for future migrations.

**2026-04-14**

## v0.7.102

* Improved handling of parallel interrupts by merging multiple interrupt chunks and ensuring consistent interrupt return behavior.
* Updated Vite dependency to patch security vulnerabilities CVE-2026-39363 and CVE-2026-39364.
* Pinned the Datadog image version to `1.9.9` due to missing `arm64` support in `1.9.10` manifest.

**2026-04-14**

## v0.7.101

* Bumped Go stdlib to 1.25.9 to address high severity vulnerabilities CVE-2026-32280 and CVE-2026-32282.
* Improved error propagation in DD and OTEL tracers to handle UserInterrupt exceptions without causing generator errors.

**2026-04-10**

## v0.7.100

* Implemented background deletion of checkpoints to improve thread deletion and pruning performance, reducing I/O pressure and enhancing efficiency.
* Bumped `@hono/node-server` from 1.19.12 to 1.19.13 to fix a security issue with the Serve Static Middleware.
* Updated hono from version 4.12.9 to 4.12.12, including critical security patches for middleware and utilities.
* Upgraded the hono library to version 4.12.12, addressing several security vulnerabilities.
* Implemented strict version locking for build dependencies to ensure consistency across builds.

**2026-04-09**

## v0.7.99

* Updated OpenAPI configuration to prevent 405 errors in `/docs` "try it" requests when using Istio with a path prefix.
* Replaced `signal.raise_signal(SIGINT)` with `sys.exit` in `queue_with_signal` to improve shutdown reliability and handle stuck threads.
* Added opt-in TLS configuration for executor clients, preserving backward-compatible cleartext behavior for existing non-loopback deployments.
* Adjusted the precedence order for Datadog API key configuration to ensure proper key usage.

**2026-04-06**

## v0.7.98

* Fixed an import issue in `langgraph dev` to ensure the dev server works without environment variables and added a regression test.

**2026-04-06**

## v0.7.97

* Improved error propagation for JS graphs, ensuring clearer error messages from the `/assistants/<ID>/schemas` endpoint.
* Ensured stable startup when environment variables like `LANGGRAPH_SERVER_HOST` are set to an IPv6 address.
* Enhanced query performance by using `->>` for string value filters in `EqAuthFilter`, enabling the use of B-tree indexes.

**2026-04-03**

## v0.7.96

* Enhanced database performance by disabling nested loops and respecting lower `statement_timeout` settings when specified.

**2026-04-03**

## v0.7.95

* Resolved a `BlockingError` by ensuring `ddtrace` is imported at module load time, preventing async context conflicts during initialization.
* Propagated `ddtrace` context to worker ensuring `langgraph.graph_load` has a parent span instead of emitting as a root.
* Added support for `Prefer: return=minimal` on `PATCH /threads/{id}` to improve efficiency by returning a 204 status with no body.
* Enhanced `run_server` with dynamic port discovery to automatically select an available port when the default port (`2024`) is in use.

**2026-03-31**

## v0.7.94

* Resolved an issue where JavaScript installs would incorrectly succeed after retry timeouts, ensuring proper failure handling.
* Added a `langgraph.graph_load` ddtrace span around the graph factory load to improve APM visibility.

**2026-03-31**

## v0.7.93

* Enabled `FF_OPTIMIZED_STREAMING` flag support from environment variables in `core-api` mode.

**2026-03-31**

## v0.7.92

* Fixed an issue where `keep_latest` threads could accumulate checkpoints indefinitely by recreating the `thread_ttl` entry upon run completion.
* Improved import performance by caching `importlib.metadata.packages_distributions()`, significantly reducing startup time when using `ddtrace` with Google API packages.

**2026-03-29**

## v0.7.91

* Upgraded cryptography dependency from 46.0.5 to 46.0.6 to address a security issue related to name constraints in peer name verification.
* Introduced an optimized streaming implementation using Redis Streams with a new protocol version (v2) for better performance and resumability, featuring payload compression and support for Redis Cluster read replicas.

**2026-03-27**

## v0.7.90

* Improved error handling in the DR flow and set a 30-second default timeout for tests to ensure timely CI failure tracking.
* Upgraded picomatch from 4.0.3 to 4.0.4 to address critical security vulnerabilities.

**2026-03-25**

## v0.7.89

* Enhanced queue server metrics and established a requirement for the OpenTelemetry SDK.
* Added a missing tag for the `COUNTER_RUN_FAILED_AFTER_RETRY` metric to improve monitoring accuracy.

**2026-03-24**

## v0.7.87

* Implemented retries for run failures due to Redis-related streaming errors, with warning logs for visibility.

**2026-03-23**

## v0.7.86

* Set default `DD_TRACE_ENABLED=false` in all images to reduce Orchestrion log noise for non-Datadog deployments.

**2026-03-23**

## v0.7.84

* Downgraded noisy warning-level logs to info level to reduce log clutter, focusing on informational status messages like license lite mode and tracing disabled.
* Enhanced Go `core-api-grpc` with Orchestrion DD APM tracing for automatic instrumentation and improved trace context propagation.

**2026-03-19**

## v0.7.82

* Ensured A2A protocol compliance by preserving `kind` discriminators and using lowercase states/roles in responses for all client method name formats.

**2026-03-18**

## v0.7.79

* Introduced beta release of the `swr` function for improved data fetching capabilities.
* Upgraded the Go runtime to version 1.25.8 across all Dockerfiles and `go.mod` to address multiple CVEs.

**2026-03-17**

## v0.7.77

* Introduced `HTTP_MAX_REQUEST_BODY_BYTES` config to limit HTTP request body size to 300MB, returning a 413 error for oversized requests to prevent memory exhaustion.
* Added support for accessing store and checkpointer via config in JS graph factories to facilitate deep agent initialization.
* Updated `pyasn1` dependency from version 0.6.2 to 0.6.3 to enhance security and fix parsing issues.
* Added instrumentation to log time to first byte (TTFB) and response size for streaming endpoints, improving access log details.

**2026-03-17**

## v0.7.76

* Relaxed `starlette-sse` version bounds to improve dependency compatibility.

**2026-03-17**

## v0.7.75

* Correctly closed streams in `Runs.Enter` to prevent buffer issues and added a configurable environment variable for window size.

**2026-03-16**

## v0.7.74

* Cleaned up some false error logs during queue shutdown operations.

**2026-03-16**

## v0.7.73

* Improved thread search performance with `extract` by avoiding unnecessary detoasting of large JSONB values.

**2026-03-13**

## v0.7.72

* Updated undici package from version 7.22.0 to 7.24.0 to address multiple security vulnerabilities.

**2026-03-13**

## v0.7.71

* Cleaned up the API by removing unused parameters from Threads State Checkpoint and Runs create methods.
* Fixed the `POST /threads/prune` with `strategy=delete` to ensure thread records are fully removed, not just checkpoint data.
* Added A2A 1.0 `kind` discriminators to response objects, removed `{"task": ...}` wrapper, and fixed Anthropic streaming metadata issues.
* Added support for custom encryption in the Redis queue to enhance data security.

**2026-03-11**

## v0.7.69

* Added optional `timezone` field to crons, allowing `next_run_date` computation in user's specified timezone, defaulting to UTC.
* Corrected the handling of 401 status codes in authentication exceptions to prevent incorrect defaulting to 403.

**2026-03-10**

## v0.7.68

* Fixed issues with non-DR checkpoint AES JSON to improve functionality and extend test coverage.
* Fixed A2A streaming to correctly emit interrupt artifacts as separate `artifact-update` events according to the specification.
* Ensured secure tarfile extraction by only extracting validated and safe members to prevent arbitrary file write vulnerabilities.
* Enhanced security by requiring an exact match for the `noauth` path in authentication middleware.
* Fixed stale checkpoint values being written to thread state during rollback in multitasking strategy.

**2026-03-06**

## v0.7.66

* Added a fallback to `LS_CHECKPOINTER_BACKEND` for default checkpointer configuration when `LANGGRAPH_CHECKPOINTER` is unset.

**2026-03-05**

## v0.7.65

* Fixed a bug in `messages-tuple` streaming mode where `tool_call_chunks` contained `args_json` instead of `args`, preventing message reconstruction and causing errors.

**2026-03-05**

## v0.7.64

* Enabled the MongoDB checkpointer URI to be set via `LS_MONGODB_URI` or `MONGODB_URI` environment variables, with precedence rules.

**2026-03-04**

## v0.7.63

* Fixed a bug that could potentially deadlock queue instances by exhausting workers with invalid runs.

**2026-03-02**

## v0.7.61

* Fixed a race condition to ensure graceful shutdown of the health and metric server.

**2026-02-27**

## v0.7.59

* Updated the Redis queue to use zset with threads, reducing CPU usage by 25% and improving performance by eliminating unnecessary locking and optimizing indexes.

**2026-02-26**

## v0.7.58

* Upgraded `langgraph-checkpoint` to 4.0.0 in `storage_postgres/uv.lock` to address CVE-2026-27794, with adjustments for dependency pinning issues.

**2026-02-26**

## v0.7.57

* Fixed a regression preventing all users from creating crons associated with system graphs.

**2026-02-25**

## v0.7.56

* Added support for `ttl`, `index`, and `refresh_ttl` parameters in store HTTP API endpoints to align with the SDK and in-process store interface.
* Added support for the `?include=ttl` query parameter in the `GET /threads/{thread_id}` endpoint to return TTL information.
* Updated metrics reporting to accurately account for PostgreSQL and Redis connections, ensuring consistent statistics between GRPC and Python metrics.

**2026-02-25**

## v0.7.55

* Fixed a bug that caused duplicate run scheduling in the new cron scheduler backend.
* Refactored the `GET /docs` endpoint to read from a static OpenAPI spec for improved compatibility with custom ingress configurations.

**2026-02-24**

## v0.7.54

* Resolved an issue where the custom encryption context for gRPC services was not loading correctly due to hardcoded values.

**2026-02-24**

## v0.7.52

* Added feedback URLs to the `/wait` and `/join` endpoint responses under a `__feedback__` key when `feedback_keys` are supplied.
* Added feedback\_keys support to the distributed runtime, including presigned feedback token generation using langsmith-go SDK.
* Upgraded Werkzeug from version 3.1.5 to 3.1.6 to address a Windows security issue with special device names in multi-segment paths.
* Upgraded Go runtime to 1.25.7 to address critical and high severity CVEs identified in vulnerability scans.

**2026-02-22**

## v0.7.51

* Improved license check resilience during upstream outages, including a cached fallback, a 24-hour grace period, and automatic cleanup of Redis entries.
* Ensured assistant descriptions and names are synced on startup when `LANGSERVE_GRAPHS` config changes.
* Enhanced the Checkpointer API by introducing a two-level protocol hierarchy and fixing capability detection to support extended methods directly.

**2026-02-20**

## v0.7.49

* Reserved metadata keys in request payloads are now silently stripped rather than causing a 422 error, enhancing user experience.
* Fixed an issue where store default TTL was not applied to items written without an explicit TTL parameter.

**2026-02-19**

## v0.7.46

* Structured error payloads in webhooks now include `error` and `message` fields, replacing the previous flat string format, which may affect systems parsing the `error` field.
* Expanded store auth tests with namespace-rewriting to enhance namespace handling and cross-user isolation.

**2026-02-19**

## v0.7.45

* Replaced null bytes with U+FFFD in all handling paths to prevent key collisions.

**2026-02-19**

## v0.7.44

* Increase flexibility of database URI parser
* Add additional validation on some payloads

**2026-02-18**

## v0.7.40

* Fixed a regression in assistant creation by ensuring `metadata` and `config` are populated as empty objects `{}` instead of `null` when not provided.

**2026-02-17**

## v0.7.39

* Ensured auth configuration is passed correctly in distributed runtime operations to improve executor functionality.
* Added support for Red Hat UBI-9 based Docker images for enterprise customers using RHEL-based containers.
* Added graceful shutdown handoff for distributed runtime, allowing in-flight runs to transfer to the next pod without using a retry attempt.

**2026-02-17**

## v0.7.38

* Added `state_updated_at` field to threads for tracking meaningful state changes, allowing filtering and sorting based on these changes.
* Added support for scheduling crons within the core system.
* Ensured accurate display of the `https` protocol in agent cards using the x-forwarded-proto header for proper A2A client functionality.

**2026-02-15**

## v0.7.37

* Added generic fallbacks for `acopy_thread`, `aprune`, and `adelete_for_runs` in the BYOC checkpointer adapter, simplifying implementation for custom checkpointers.

**2026-02-13**

## v0.7.36

* Updated A2A protocol support to v1.0 RC, renamed JSON-RPC methods, added a ListTasks handler, and enhanced role, state, and part formats for improved integration and compliance.
* Improved authentication filtering for `Crons.search()` and `Crons.count()` to prevent unauthorized thread information access.
* Fixed gaps in BYOC checkpointer for copy, rollback, and namespace filtering operations, ensuring proper handling across different storage backends.

**2026-02-13**

## v0.7.35

* Added an optional `context` parameter to MCP `tools/call` and A2A `message/send` and `message/stream` endpoints, enabling middleware to inject runtime context from headers.

**2026-02-13**

## v0.7.33

* Enhanced the Redis fixture by removing custom checkpointer test skips, improving typed serialization, and adding missing Redis methods.
* Resolved a stored XSS vulnerability in the handle\_ui endpoint by sanitizing message names in single-quoted HTML onload attributes.
* Fixed an authorization bypass issue in `put_item` to ensure correct namespace rewrite by the auth handler.
* Enforced assistant ownership checks during run creation, preventing execution on unowned assistants while ensuring system assistants remain accessible to all authenticated users.
* Implemented AES encryption for checkpoint blobs and writes in the Go checkpointer when using LANGGRAPH\_AES\_KEY.
* Implemented initial checkpointer gRPC servicer with all necessary methods and conversion helpers.

**2026-02-11**

## v0.7.32

* Sanitized error messages in streams and A2A responses to protect sensitive information like database connection strings and internal hostnames.
* Fixed a bug in `join_run_stream` to correctly handle multiple `stream_mode` parameters, ensuring proper parsing of stringified JSON lists.
* Added build, test, and publish processes for Node.js 24 images, supporting the latest LTS version.
* Enhanced custom checkpointer adapter with new capabilities and improved metadata enrichment for consistent API responses.
* Added stricter version constraints for langgraph libraries in executor Docker images to prevent unintended upgrades.
* Enhanced security by sanitizing SSE event and id fields to prevent CR/LF injection.
* Fixed an issue causing cron-created runs to use default encryption contexts instead of properly propagating the specified ones.

**2026-02-11**

## v0.7.31

* Corrected metadata reading functionality to ensure accurate data processing.

**2026-02-10**

## v0.7.30

* Propagated cron metadata for more comprehensive scheduling information.
* Merges cron metadata on `PATCH` requests to align with other endpoints by preserving existing data.

**2026-02-10**

## v0.7.29

* Refined authentication semantics for cron creation to prevent privilege escalation and ensure independent filtering for crons, threads, and assistants.
* Validated tar file entries to prevent directory traversal vulnerabilities in the cloudflared download process.
* Added an IDs filter to the `SearchThreadsRequest` to streamline thread endpoint operations.
* Updated the fallback mechanism to use a Python Postgres connection for thread state, fixing issues with worker completion checkpoints.
* Introduced a feature-flagged initial version of the Redis queue implementation with ongoing updates.

**2026-02-07**

## v0.7.28

* Internal maintenance and stability improvements for MCP and gRPC.

**2026-02-07**

## v0.7.27

* Improved MCP tool input schemas by removing common message types for cleaner tool definitions.
* Added name sanitization for MCP tools to ensure valid tool names.

**2026-02-07**

## v0.7.26

* Added validation for system keys on ingress.

**2026-02-06**

## v0.7.25

* Switched the Python queue worker to use core go `Runs.next()`.
* Fixed a monitoring issue in the long query monitor

**2026-02-06**

## v0.7.24

* Optimized Postgres connection handling to prevent hitting connection limits under high load and removed unnecessary error logs.
* Switched to a new backend for runs management and streaming using gRPC.

**2026-02-05**

## v0.7.23

* Corrected the unmarshaling process for the `input` field in `RunCommand` to ensure accurate data mapping and enable a previously gated JS test.
* Ensured race condition handling for run streaming by fully subscribing before execution starts, with added support for the `FF_LOG_DROPPED_EVENTS` environment variable.

**2026-02-04**

## v0.7.22

* Ensured `get_store()` works in custom routes, enabling Store access from user-defined Starlette endpoints.

**2026-02-05**

## v0.7.21

* Support for PATCH /crons/{cron_id}

**2026-02-04**

## v0.7.19

* Custom encryption improvements for core API.

**2026-02-04**

## v0.7.18

* Update thread streaming for core API usage.

**2026-02-03**

## v0.7.17

* Instrumentation for OTEL now requires explicit opt-in with `LS_APM_OTEL_ENABLED=true` for improved control.

**2026-02-03**

## v0.7.16

* Switched threads streaming to the new gRPC backend for improved performance.
* Introduced replica tracing in DR for enhanced evaluation capabilities in Studio.

**2026-02-03**

## v0.7.15

* Added support for pausing crons with a new `is_enabled` field, allowing only enabled crons to be executed.
* Introduced gRPC server support for JSON encryption and decryption operations.

**2026-02-02**

## v0.7.14

* Ensured selected system fields are excluded from custom encryption to prevent unnecessary encryption of non-sensitive data.
* Introduced a custom checkpointer adapter with unit tests to validate implementation checks.

**2026-01-29**

## v0.7.13

* Fixed a bug where the app state was not properly preserved through requests when a mount prefix was set.

**2026-01-28**

## v0.7.11

* Added configuration to control which payload fields can be exposed to webhooks.
* Updated all dependencies in the `/api/langgraph_api/js` group, including `@langchain/core`, `hono`, `@types/react`, and `prettier`, to the latest versions for improved performance and security.
* Upgraded `hono` from version 4.11.4 to 4.11.7 to address multiple security vulnerabilities in the middleware.

**2026-01-27**

## v0.7.10

* Increased the gRPC server startup timeout to 1 minute to prevent occasional connection timeouts with the core server.
* Updated @langchain/langgraph from version 1.1.0 to 1.1.2, introducing mixed schema support for StateGraph and type bag patterns for GraphNode and ConditionalEdgeRouter utilities.

**2026-01-23**

## v0.7.9

* A2A `messageId` is now mapped to LangChain message IDs for proper message tracking across protocols.

**2026-01-22**

## v0.7.7

* Ensured preservation of custom configurable fields in checkpoint metadata during gRPC serialization.

**2026-01-21**

## v0.7.5

* Enforced custom encryption for values, interrupts, and errors when setting a thread's status, resolving previous inconsistencies.
* Added A2A validation checks in `message/stream` and `message/send` routes for `parts`, `role`, and `messageId` fields.
* Added native A2A interrupt support: `input-required` state is now returned when graphs are interrupted. Use the new `command` parameter in `message/stream` and `message/send` requests to resume with a `Command` payload.
* Mounted `.well-known/agent-card.json` under `/a2a/{assistant_id}/` for A2A agent discovery.
* Added proper A2A error codes for task existence checks in `tasks/cancel`.

**2026-01-21**

## v0.7.4

* Fixed a bug with Redis URL parsing for `ssl_cert_reqs` field, ensuring compatibility with redis-go.
* Added a gRPC client for streaming runs, controlled by the `FF_USE_CORE_API` feature flag.

**2026-01-20**

## v0.7.2

* Updated `@langchain/langgraph` to version 1.1.0, introducing type utilities for graph nodes and conditional edges for enhanced TypeScript ergonomics.

**2026-01-17**

## v0.7.0

* Switched to using the Go assistants implementation by default for improved performance.
* Added `LANGGRAPH_AES_JSON_KEYS` configuration to enable AES encryption for specified JSON fields using a key name allowlist.

**2026-01-16**

## v0.6.39

* Added gRPC client support for `Threads.State()` to the Python `core-api`, improving thread ID and run counting operations.

**2026-01-15**

## v0.6.36

* Validated the length of `$and` and `$or` in auth filters and optimized unnecessary root-level filters.

**2026-01-12**

## v0.6.35

* Unified the error format by removing the `code` field and standardizing all errors to return JSON with a `detail` field.

**2026-01-12**

## v0.6.34

* Small fixes for feature-flagged internal environments (unreleased).

**2026-01-12**

## v0.6.33

* Small fixes for feature-flagged internal environments (unreleased).

**2026-01-11**

## v0.6.32

* Small fixes for feature-flagged internal environments (unreleased).

**2026-01-11**

## v0.6.31

* Properly respected the disable\_a2a setting to ensure accurate configuration handling.

**2026-01-09**

## v0.6.29

* Fix minor bugs.

**2026-01-09**

## v0.6.28

* Added support for `ParentCommand` to correctly propagate control to parent graphs, enhancing command handling and navigation.
* Added a Python gRPC client for managing run operations, enhancing consistency between Go and Python implementations.

**2026-01-08**

## v0.6.27

* Fixed a regression issue in handling empty thread metadata.

**2026-01-08**

## v0.6.26

* Fixed the port configuration issue for the persistence gRPC server.

**2026-01-08**

## v0.6.25

* Ran the core-api gRPC server in the executor tier to support loopback API calls in graphs and removed unnecessary configuration for disabling the server.

**2026-01-07**

## v0.6.24

* Fixed the behavior of the liveness probe in the executor tier, addressing issues from version 0.6.23.

**2026-01-07**

## v0.6.23

* Integrated gRPC server health check with `/ok` endpoint in liveness probe to ensure proper startup coordination.
* Reverted the previous change to disable the checkpointer and added a condition to enable RemoteCheckpointer only during testing.
* Suppressed `langgraph_auth_*` and `langgraph_request_id` fields in checkpoint metadata to prevent inclusion of transient user data.

**2026-01-06**

## v0.6.22

* Resolved an error caused by missing encryption contexts when using blob-only custom encryption, ensuring proper function without errors.

**2026-01-06**

## v0.6.21

* Introduced a Python gRPC client for run operations, including `Search`, `Get`, `Delete`, `Cancel`, `Stats`, and `Sweep`, with updated API implementation and a new unit test suite for enum mappings.

**2026-01-06**

## v0.6.19

* Reproduced OSS implementations of `get_state` and `update_state` in the engine server and re-enabled `test_weather_subgraph`.

**2026-01-05**

## v0.6.18

* Added functionality to enforce specific license claims for self-hosted Enterprise users, enabling remote disabling of the Agent Builder product.
* Added a new Prune endpoint for better resource management.
* Merged graph configuration with invoke configuration in Pregel, giving precedence to invoke settings.
* Introduced the `include=ttl` query parameter to the GET /threads/{id} endpoint for optional TTL information retrieval without affecting standard read performance.
* Introduced a `keep_latest` TTL strategy to preserve the latest state while pruning older checkpoints via the core API.

**2025-12-31**

## v0.6.17

* Ensured ongoing runs are stopped when an agent is deleted to prevent lingering processes.

**2025-12-30**

## v0.6.16

* Streamlined and consolidated run operations in the Go persistence layer, improving efficiency and consistency across packages.

**2025-12-26**

## v0.6.15

* Improved the utility converting custom route docstrings to OpenAPI schema content by adding error handling when parsing docstrings, applicable for users with custom Starlette apps.

**2025-12-23**

## v0.6.12

* Improved resolve\_embeddings to be more robust, enabling multiple calls without errors.
* Updated `@langchain/langgraph` from version 1.0.4 to 1.0.7, adding support for resumableStreams on remote graphs and undeprecating toolsCondition.
* Implemented `RemoteCheckpointer` to enable subgraph checkpointing, enhancing task execution reliability.

**2025-12-20**

## v0.6.11

* Made the maximum number of retries configurable for enhanced customization.

**2025-12-20**

## v0.6.10

* Ensured run cancellation only processes 'message' type Redis events, improving pubsub client reliability.
* Added custom encryption for the Store API `value` field, allowing users to choose which keys to encrypt for enhanced security.
* Enabled streaming for subgraph custom events by updating TeeStream to handle event types separately.

**2025-12-18**

## v0.6.9

* Enforced stable JSON keys for custom encryption, removed model-type-specific custom JSON functions, and improved error handling for double-encryption scenarios.

**2025-12-18**

## v0.6.8

* Added profiling feature to enhance performance analysis and monitoring.

**2025-12-18**

## v0.6.7

* Logged server startup time for improved monitoring and diagnostics.

**2025-12-17**

## v0.6.5

* Added a warning log that triggers during import time for improved visibility.

**2025-12-16**

## v0.6.4

* Enhanced custom encryption by parallelizing metadata and config processes, added encryption for thread.config and some checkpoints, improved tests and schema consistency.
* Ensured the Go server starts as `core-api` in the queue entrypoint for consistent runtime behavior.

**2025-12-15**

## v0.6.2

* Resolved an issue that caused duplicate calls to middleware when `mount_prefix` was specified.

**2025-12-15**

## v0.6.0

This minor version updates the streaming APIs `/join-stream` and `/stream` behavior with respect to the `last-event-id` parameter to align with the SSE spec. Previously, passing a last-event-id would return that message in addition to any following messages. Going forward, these APIs will only return new messages following the provided last-event-id. For example, with the following stream, previously passing a last-event-id of `2` would return the messages with ids `2` and `3`, but will now only return the message with id `3`:

```json
{
    "id": 1,
    "event": "message",
    "data": {
        "content": "Excluded"
    }
},
{
    "id": 2,
    "event": "message",
    "data": {
        "content": "Passed last-event-id"
    }
},
{
    "id": 3,
    "event": "message",
    "data": {
        "content": "Included"
    }
}
```

This bump also includes some fixes, including a bug exposing unintended internal events in run streams.

**2025-12-12**

## v0.5.42

* Modified the Go server to rely solely on the CLI `-service` flag for determining service mode, ignoring the globally set `FF_USE_CORE_API` for better deployment specificity.

**2025-12-11**

## v0.5.41

Fixed an issue with cron jobs in hybrid mode by ensuring proper initialization of the ENTERPRISE\_SAAS global flag.

**2025-12-10**

## v0.5.39

* Completed the implementation of custom encryptions for runs and crons, along with simplifying encryption processes.
* Introduced support for streaming subgraph events in both `values` and `updates` stream modes.

**2025-12-10**

## v0.5.38

* Implemented complete custom encryption for threads, ensuring all thread data is properly secured and encrypted.
* Ensured Redis attempt flags are consistently expired to prevent stale data.
* Added core authentication and support for OR/AND filters, enhancing security and flexibility.

**2025-12-09**

## v0.5.37

Added a `name` parameter to the assistants count API for improved search flexibility.

**2025-12-09**

## v0.5.36

* Introduced configurable webhook support, allowing users to customize submitted webhooks and headers.
* Added an `/ok` endpoint at the root for easier health checks and simplified configuration.

**2025-12-08**

## v0.5.34

Introduced custom encryption middleware, allowing users to define their own encryption methods for enhanced data protection.

**2025-12-08**

## v0.5.33

Set Uvicorn's keep-alive timeout to 75 seconds to prevent occasional 502 errors and improve connection handling.

**2025-12-06**

## v0.5.32

Introduced OpenTelemetry telemetry agent with support for New Relic integration.

**2025-12-05**

## v0.5.31

Added Py-Spy profiling for improved analysis of deployment performance, with some limitations on coverage.

**2025-12-05**

## v0.5.30

* Always configure loopback transport clients to enhance reliability.
* Ensured authentication headers are passed for remote non-stream methods in JS.

**2025-12-04**

## v0.5.28

* Introduced a faster, Rust-based implementation of uuid7 to improve performance, now used in langsmith and langchain-core.
* Added support for `$or` and `$and` in PostgreSQL auth filters to enable complex logic in authentication checks.
* Capped psycopg and psycopg-pool versions to prevent infinite waiting on startup.

**2025-11-26**

## v0.5.27

* Ensured `runs.list` with filters returns only run fields, preventing incorrect status data from being included.
* (JS) Updated `uuid` from version 10.0.0 to 13.0.0. and `exit-hook` from version 4.0.0 to 5.0.1.

**2025-11-24**

## v0.5.26

Resolved issues with `store.put` when used without AsyncBatchedStore in the JavaScript environment.

**2025-11-22**

## v0.5.25

* Introduced the ability to search assistants by their `name` using a new endpoint.
* Casted store\_get return types to tuple in JavaScript to ensure type consistency.

**2025-11-21**

## v0.5.24

* Added executor metrics for Datadog and enhanced core stream API metrics for better performance tracking.
* Disabled Redis Go maintenance notifications to prevent startup errors with unsupported commands in Redis versions below 8.

**2025-11-20**

## v0.5.20

Resolved an error in the executor service that occurred when handling large messages.

**2025-11-19**

## v0.5.19

Upgraded built-in langchain-core to version 1.0.7 to address a prompt formatting vulnerability.

**2025-11-19**

## v0.5.18

Introduced persistent cron threads with `on_run_completed: {keep,delete}` for enhanced cron management and retrieval options.

**2025-11-19**

## v0.5.17

Enhanced task handling to support multiple interrupts, aligning with open-source functionality.

**2025-11-18**

## v0.5.15

Added custom JSON unmarshalling for `Resume` and `Goto` commands to fix map-style null resume interpretation issues.

**2025-11-14**

## v0.5.14

Ensured `pg make start` command functions correctly with core-api enabled.

**2025-11-13**

## v0.5.13

Support `include` and `exclude` (plural form key for `includes` and `excludes`) since a doc incorrectly claimed support for that. Now the server accepts either.

**2025-11-10**

## v0.5.11

* Ensured auth handlers are applied consistently when streaming threads, aligning with recent security practices.
* Bumped `undici` dependency from version 6.21.3 to 7.16.0, introducing various performance improvements and bug fixes.
* Updated `p-queue` from version 8.0.1 to 9.0.0, introducing new features and breaking changes, including the removal of the `throwOnTimeout` option.

**2025-11-10**

## v0.5.10

Implemented healthcheck calls in the queue /ok handler to improve Kubernetes liveness and readiness probe compatibility.

**2025-11-09**

## v0.5.9

* Resolved an issue causing an "unbound local error" for the `elapsed` variable during a SIGINT interruption.
* Mapped the "interrupted" status to A2A's "input-required" status for better task status alignment.

**2025-11-07**

## v0.5.8

* Ensured environment variables are passed as a dictionary when starting langgraph-ui for compatibility with `uvloop`.
* Implemented CRUD operations for runs in Go, simplifying JSON merges and improving transaction readability, with PostgreSQL as a reference.

**2025-11-07**

## v0.5.7

Replaced no-retry Redis client with a retry client to handle connection errors more effectively and reduced corresponding logging severity.

**2025-11-06**

## v0.5.6

* Added pending time metrics to provide better insights into task waiting times.
* Replaced `pb.Value` with `ChannelValue` to streamline code structure.

**2025-11-05**

## v0.5.5

Made the Redis `health_check_interval` more frequent and configurable for better handling of idle connections.

**2025-11-05**

## v0.5.4

Implemented `ormsgpack` with `OPT_REPLACE_SURROGATES` and updated for compatibility with the latest FastAPI release affecting custom authentication dependencies.

**2025-11-03**

## v0.5.2

Added retry logic for PostgreSQL connections during startup to enhance deployment reliability and improved error logging for easier debugging.

**2025-11-03**

## v0.5.1

* Resolved an issue where persistence was not functioning correctly with LangChain.js's createAgent feature.
* Optimized assistants CRUD performance by improving database connection pooling and gRPC client reuse, reducing latency for large payloads.

**2025-10-31**

## v0.5.0

This minor version now requires langgraph-checkpoint versions later than 3.0 to prevent a deserialization vulnerability in earlier versions of the langgraph-checkpoint library.
The `langgraph-checkpoint` library is compatible with `langgraph` minor versions 0.4, 0.5, 0.6, and 1.0.

This version removes default support for deserialization of payloads saved using the "json" type, which has never been the default.
By default, objects are serialized using msgpack. Under certain uncommon situations, payloads were serialized using an older "json" mode. If those payloads contained custom python objects, those will no longer be deserializable unless you provide a `serde` config:

```json
{
    "checkpointer": {
        "serde": {
            "allowed_json_modules": [
                ["my_agent", "my_file", "SomeType"],
            ]
        }
    }
}
```

**2025-10-29**

## v0.4.47

* Validated and auto-corrected environment configuration types using TypeAdapter.
* Added support for LangChain.js and LangGraph.js version 1.x, ensuring compatibility.
* Updated hono library from version 4.9.7 to 4.10.3, addressing a CORS middleware security issue and enhancing JWT audience validation.
* Introduced a modular benchmark framework, adding support for assistants and streams, with improvements to the existing ramp benchmark methodology.
* Introduced a gRPC API for core threads CRUD operations, with updated Python and TypeScript clients.
* Updated `hono` package from version 4.9.7 to 4.10.2, including security improvements for JWT audience validation.
* Updated `hono` dependency from version 4.9.7 to 4.10.3 to fix a security issue and improve CORS middleware handling.
* Introduced basic CRUD operations for threads, including create, get, patch, delete, search, count, and copy, with support for Go, gRPC server, and Python and TypeScript clients.

**2025-10-21**

## v0.4.46

Added an option to enable message streaming from subgraph events, giving users more control over event notifications.

**2025-10-21**

## v0.4.45

* Implemented support for authorization on custom routes, controlled by the `enable_custom_route_auth` flag.
* Set default tracing to off for improved performance and simplified debugging.

**2025-10-18**

## v0.4.44

Used Redis key prefix for license-related keys to prevent conflicts with existing setups.

**2025-10-16**

## v0.4.43

Implemented a health check for Redis connections to prevent them from idling out.

**2025-10-15**

## v0.4.40

* Prevented duplicate messages in resumable run and thread streams by addressing a race condition and adding tests to ensure consistent behavior.
* Ensured that runs don't start until the pubsub subscription is confirmed to prevent message drops on startup.
* Renamed platform from langgraph to improve clarity and branding.
* Reset PostgreSQL connections after use to prevent lock holding and improved error reporting for transaction issues.

**2025-10-10**

## v0.4.39

* Upgraded `hono` from version 4.7.6 to 4.9.7, addressing a security issue related to the `bodyLimit` middleware.
* Allowed customization of the base authentication URL to enhance flexibility.
* Pinned the 'ty' dependency to a stable version using 'uv' to prevent unexpected linting failures.

**2025-10-08**

## v0.4.38

* Replaced `LANGSMITH_API_KEY` with `LANGSMITH_CONTROL_PLANE_API_KEY` to support hybrid deployments requiring license verification.
* Introduced self-hosted log ingestion support, configurable via `SELF_HOSTED_LOGS_ENABLED` and `SELF_HOSTED_LOGS_ENDPOINT` environment variables.

**2025-10-06**

## v0.4.37

Required create permissions for copying threads to ensure proper authorization.

**2025-10-03**

## v0.4.36

* Improved error handling and added a delay to the sweep loop for smoother operation during Redis downtime or cancellation errors.
* Updated the queue entrypoint to start the core-api gRPC server when `FF_USE_CORE_API` is enabled.
* Introduced checks for invalid configurations in assistant endpoints to ensure consistency with other endpoints.

**2025-10-02**

## v0.4.35

* Resolved a timezone issue in the core API, ensuring accurate time data retrieval.
* Introduced a new `middleware_order` setting to apply authentication middleware before custom middleware, allowing finer control over protected route configurations.
* Logged the Redis URL when errors occur during Redis client creation.
* Improved Go engine/runtime context propagation to ensure consistent execution flow.
* Removed the unnecessary `assistants.put` call from the executor entrypoint to streamline the process.

**2025-10-01**

## v0.4.34

Blocked unauthorized users from updating thread TTL settings to enhance security.

**2025-10-01**

## v0.4.33

* Improved error handling for Redis locks by logging `LockNotOwnedError` and extending initial pool migration lock timeout to 60 seconds.
* Updated the BaseMessage schema to align with the latest langchain-core version and synchronized build dependencies for consistent local development.

**2025-09-30**

## v0.4.32

* Added a GO persistence layer to the API image, enabling GRPC server operation with PostgreSQL support and enhancing configurability.
* Set the status to error when a timeout occurs to improve error handling.

**2025-09-30**

## v0.4.30

* Added support for context when using `stream_mode="events"` and included new tests for this functionality.
* Added support for overriding the server port using `$LANGGRAPH_SERVER_PORT` and removed an unnecessary Dockerfile `ARG` for cleaner configuration.
* Applied authorization filters to all table references in thread delete CTE to enhance security.
* Introduced self-hosted metrics ingestion capability, allowing metrics to be sent to an OTLP collector every minute when the corresponding environment variables are set.
* Ensured that the `set_latest` function properly updates the name and description of the version.

**2025-09-26**

## v0.4.29

Ensured proper cleanup of redis pubsub connections in all scenarios.

**2025-09-25**

## v0.4.28

* Added a format parameter to the queue metrics server for enhanced customization.
* Corrected `MOUNT_PREFIX` environment variable usage in CLI for consistency with documentation and to prevent confusion.
* Added a feature to log warnings when messages are dropped due to no subscribers, controllable via a feature flag.
* Added support for Bookworm and Bullseye distributions in Node images.
* Consolidated executor definitions by moving them from the `langgraph-go` repository, improving manageability and updating the checkpointer setup method for server migrations.
* Ensured correct response headers are sent for a2a, improving compatibility and communication.
* Consolidated PostgreSQL checkpoint implementation, added CI testing for the `/core` directory, fixed RemoteStore test errors, and enhanced the Store implementation with transactions.
* Added PostgreSQL migrations to the queue server to prevent errors from graphs being added before migrations are performed.

**2025-09-23**

## v0.4.27

Replaced `coredis` with `redis-py` to improve connection handling and reliability under high traffic loads.

**2025-09-22**

## v0.4.24

* Added functionality to return full message history for A2A calls in accordance with the A2A spec.
* Added a `LANGGRAPH_SERVER_HOST` environment variable to Dockerfiles to support custom host settings for dual stack mode.

**2025-09-22**

## v0.4.23

Use a faster message codec for redis streaming.

**2025-09-19**

## v0.4.22

Ported long-stream handling to the run stream, join, and cancel endpoints for improved stream management.

**2025-09-18**

## v0.4.21

* Added A2A streaming functionality and enhanced testing with the A2A SDK.
* Added Prometheus metrics to track language usage in graphs, middleware, and authentication for improved insights.
* Fixed bugs in Open Source Software related to message conversion for chunks.
* Removed await from pubsub subscribes to reduce flakiness in cluster tests and added retries in the shutdown suite to enhance API stability.

**2025-09-11**

## v0.4.20

Optimized Pubsub initialization to prevent overhead and address subscription timing issues, ensuring smoother run execution.

**2025-09-11**

## v0.4.19

Removed warnings from psycopg by addressing function checks introduced in version 3.2.10.

**2025-09-11**

## v0.4.17

Filtered out logs with mount prefix to reduce noise in logging output.

**2025-09-10**

## v0.4.16

* Added support for implicit thread creation in a2a to streamline operations.
* Improved error serialization and emission in distributed runtime streams, enabling more comprehensive testing.

**2025-09-09**

## v0.4.13

* Monitored queue status in the health endpoint to ensure correct behavior when PostgreSQL fails to initialize.
* Addressed an issue with unequal swept ID lengths to improve log clarity.
* Enhanced streaming outputs by avoiding re-serialization of DR payloads, using msgpack byte inspection for json-like parsing.

**2025-09-04**

## v0.4.12

* Ensured metrics are returned even when experiencing database connection issues.
* Optimized update streams to prevent unnecessary data transmission.
* Upgraded `hono` from version 4.9.2 to 4.9.6 in the `storage_postgres/langgraph-api-server` for improved URL path parsing security.
* Added retries and an in-memory cache for LangSmith access calls to improve resilience against single failures.

**2025-09-04**

## v0.4.11

Added support for TTL (time-to-live) in thread updates.

**2025-09-04**

## v0.4.10

In distributed runtime, update serde logic for final checkpoint -> thread setting.

**2025-09-02**

## v0.4.9

* Added support for filtering search results by IDs in the search endpoint for more precise queries.
* Included configurable headers for assistant endpoints to enhance request customization.
* Implemented a simple A2A endpoint with support for agent card retrieval, task creation, and task management.

**2025-08-30**

## v0.4.7

Stopped the inclusion of x-api-key to enhance security.

**2025-08-29**

## v0.4.6

Fixed a race condition when joining streams, preventing duplicate start events.

**2025-08-29**

## v0.4.5

* Ensured the checkpointer starts and stops correctly before and after the queue to improve shutdown and startup efficiency.
* Resolved an issue where workers were being prematurely cancelled when the queue was cancelled.
* Prevented queue termination by adding a fallback for cases when Redis fails to wake a worker.

**2025-08-28**

## v0.4.4

* Set the custom auth thread\_id to None for stateless runs to prevent conflicts.
* Improved Redis signaling in the Go runtime by adding a wakeup worker and Redis lock implementation, and updated sweep logic.

**2025-08-27**

## v0.4.3

* Added stream mode to thread stream for improved data processing.
* Added a durability parameter to runs for improved data persistence.

**2025-08-27**

## v0.4.2

Ensured pubsub is initialized before creating a run to prevent errors from missing messages.

**2025-08-25**

## v0.4.0

Minor version 0.4 comes with a number of improvements as well as some breaking changes.

* Emitted attempt messages correctly within the thread stream.
* Reduced cluster conflicts by using only the thread ID for hashing in cluster mapping, prioritizing efficiency with stream\_thread\_cache.
* Introduced a stream endpoint for threads to track all outputs across sequentially executed runs.
* Made the filter query builder in PostgreSQL more robust against malformed expressions and improved validation to prevent potential security risks.

This minor version also includes a couple of breaking changes to improve the usability and security of the service:

* In this minor version, we stop the practice of automatically including headers as configurable values in your runs. You can opt-in to specific patterns by setting **configurable\_headers** in your agent server config.
* Run stream event IDs (for resumable streams) are now in the format of `ms-seq` instead of the previous format. We retain backwards compatibility for the old format, but we recommend using the new format for new code.

**2025-08-25**

## v0.3.4

* Added custom Prometheus metrics for Redis/PG connection pools and switched the queue server to Uvicorn/Starlette for improved monitoring.
* Restored Wolfi image build by correcting shell command formatting and added a Makefile target for testing with nginx.

**2025-08-22**

## v0.3.3

* Added timeouts to specific Redis calls to prevent workers from being left active.
* Updated the Golang runtime and added pytest skips for unsupported functionalities, including initial support for passing store to node and message streaming.
* Introduced a reverse proxy setup for serving combined Python and Node.js graphs, with nginx handling server routing, to facilitate a Postgres/Redis backend for the Node.js API server.

**2025-08-21**

## v0.3.1

Added a statement timeout to the pool to prevent long-running queries.

**2025-08-21**

## v0.3.0

* Set a default 15-minute statement timeout and implemented monitoring for long-running queries to ensure system efficiency.
* Stop propagating run configurable values to the thread configuration, because this can cause issues on subsequent runs if you are specifying a checkpoint\_id. This is a **slight breaking change** in behavior, since the thread value will no longer automatically reflect the unioned configuration of the most recent run. We believe this behavior is more intuitive, however.
* Enhanced compatibility with older worker versions by handling event data in channel names within ops.py.

**2025-08-20**

## v0.2.137

Fixed an unbound local error and improved logging for thread interruptions or errors, along with type updates.

**2025-08-20**

## v0.2.136

* Added enhanced logging to aid in debugging metaview issues.
* Upgraded executor and runtime to the latest version for improved performance and stability.

**2025-08-19**

## v0.2.135

Ensured async coroutines are properly awaited to prevent potential runtime errors.

**2025-08-18**

## v0.2.134

Enhanced search functionality to improve performance by allowing users to select specific columns for query results.

**2025-08-18**

## v0.2.133

* Added count endpoints for crons, threads, and assistants to enhance data tracking (#1132).
* Improved SSH functionality for better reliability and stability.
* Updated @langchain/langgraph-api to version 0.0.59 to fix an invalid state schema issue.

**2025-08-15**

## v0.2.132

* Added Go language images to enhance project compatibility and functionality.
* Printed internal PIDs for JS workers to facilitate process inspection via SIGUSR1 signal.
* Resolved a `run_pkey` error that occurred when attempting to insert duplicate runs.
* Added `ty run` command and switched to using uuid7 for generating run IDs.
* Implemented the initial Golang runtime to expand language support.

**2025-08-14**

## v0.2.131

Added support for `object agent spec` with descriptions in JS.

**2025-08-13**

## v0.2.130

* Added a feature flag (FF\_RICH\_THREADS=false) to disable thread updates on run creation, reducing lock contention and simplifying thread status handling.
* Utilized existing connections for `aput` and `apwrite` operations to improve performance.
* Improved error handling for decoding issues to enhance data processing reliability.
* Excluded headers from logs to improve security while maintaining runtime functionality.
* Fixed an error that prevented mapping slots to a single node.
* Added debug logs to track node execution in JS deployments for improved issue diagnosis.
* Changed the default multitask strategy to enqueue, improving throughput by eliminating the need to fetch inflight runs during new run insertions.
* Optimized database operations for `Runs.next` and `Runs.sweep` to reduce redundant queries and improve efficiency.
* Improved run creation speed by skipping unnecessary inflight runs queries.

**2025-08-11**

## v0.2.129

* Stopped passing internal LGP fields to context to prevent breaking type checks.
* Exposed content-location headers to ensure correct resumability behavior in the API.

**2025-08-08**

## v0.2.128

Ensured synchronized updates between `configurable` and `context` in assistants, preventing setup errors and supporting smoother version transitions.

**2025-08-08**

## v0.2.127

Excluded unrequested stream modes from the resumable stream to optimize functionality.

**2025-08-08**

## v0.2.126

* Made access logger headers configurable to enhance logging flexibility.
* Debounced the Runs.stats function to reduce the frequency of expensive calls and improve performance.
* Introduced debouncing for sweepers to enhance performance and efficiency (#1147).
* Acquired a lock for TTL sweeping to prevent database spamming during scale-out operations.

**2025-08-06**

## v0.2.125

Updated tracing context replicas to use the new format, ensuring compatibility.

**2025-08-06**

## v0.2.123

Added an entrypoint to the queue replica for improved deployment management.

**2025-08-06**

## v0.2.122

Utilized persisted interrupt status in `join` to ensure correct handling of user's interrupt state after completion.

**2025-08-06**

## v0.2.121

* Consolidated events to a single channel to prevent race conditions and optimize startup performance.
* Ensured custom lifespans are invoked on queue workers for proper setup, and added tests.

**2025-08-04**

## v0.2.120

* Restored the original streaming behavior of runs, ensuring consistent inclusion of interrupt events based on `stream_mode` settings.
* Optimized `Runs.next` query to reduce average execution time from \~14.43ms to \~2.42ms, improving performance.
* Added support for stream mode "tasks" and "checkpoints", normalized the UI namespace, and upgraded `@langchain/langgraph-api` for enhanced functionality.

**2025-07-31**

## v0.2.117

Added a composite index on threads for faster searches with owner-based authentication and updated the default sort order to `updated_at` for improved query performance.

**2025-07-31**

## v0.2.116

Reduced the default number of history checkpoints from 10 to 1 to optimize performance.

**2025-07-31**

## v0.2.115

Optimized cache reuse to enhance application performance and efficiency.

**2025-07-30**

## v0.2.113

Improved thread search pagination by updating response headers with `X-Pagination-Total` and `X-Pagination-Next` for better navigation.

**2025-07-30**

## v0.2.112

* Ensured sync logging methods are awaited and added a linter to prevent future occurrences.
* Fixed an issue where JavaScript tasks were not being populated correctly for JS graphs.

**2025-07-29**

## v0.2.111

Fixed JS graph streaming failure by starting the heartbeat as soon as the connection opens.

**2025-07-29**

## v0.2.110

Added interrupts as default values for join operations while preserving stream behavior.

**2025-07-28**

## v0.2.109

Fixed an issue where config schema was missing when `config_type` was not set, ensuring more reliable configurations.

**2025-07-28**

## v0.2.108

Prepared for LangGraph v0.6 compatibility with new context API support and bug fixes.

**2025-07-27**

## v0.2.107

* Implemented caching for authentication processes to enhance performance and efficiency.
* Optimized database performance by merging count and select queries.

**2025-07-27**

## v0.2.106

Made log streams resumable, enhancing reliability and improving user experience when reconnecting.

**2025-07-27**

## v0.2.105

Added a heapdump endpoint to save memory heap information to a file.

**2025-07-25**

## v0.2.103

Used the correct metadata endpoint to resolve issues with data retrieval.

**2025-07-24**

## v0.2.102

* Captured interrupt events in the wait method to preserve previous behavior from langgraph 0.5.0.
* Added support for SDK structlog in the JavaScript environment for enhanced logging capabilities.

**2025-07-24**

## v0.2.101

Corrected the metadata endpoint for self-hosted deployments.

**2025-07-22**

## v0.2.99

* Improved license check by adding an in-memory cache and handling Redis connection errors more effectively.
* Reloaded assistants to preserve manually created ones while discarding those removed from the configuration file.
* Reverted changes to ensure the UI namespace for gen UI is a valid JavaScript property name.
* Ensured that the UI namespace for generated UI is a valid JavaScript property name, improving API compliance.
* Enhanced error handling to return a 422 status code for unprocessable entity requests.

**2025-07-19**

## v0.2.98

Added context to langgraph nodes to improve log filtering and trace visibility.

**2025-07-19**

## v0.2.97

* Improved interoperability with the ckpt ingestion worker on the main loop to prevent task scheduling issues.
* Delayed queue worker startup until after migrations are completed to prevent premature execution.
* Enhanced thread state error handling by adding specific metadata and improved response codes for better clarity when state updates fail during creation.
* Exposed the interrupt ID when retrieving the thread state to improve API transparency.

**2025-07-17**

## v0.2.96

Added a fallback mechanism for configurable header patterns to handle exclude/include settings more effectively.

**2025-07-17**

## v0.2.95

* Avoided setting the future if it is already done to prevent redundant operations.
* Resolved compatibility errors in CI by switching from `typing.TypedDict` to `typing_extensions.TypedDict` for Python versions below 3.12.

**2025-07-16**

## v0.2.94

* Improved performance by omitting pending sends for langgraph versions 0.5 and above.
* Improved server startup logs to provide clearer warnings when the DD\_API\_KEY environment variable is set.

**2025-07-16**

## v0.2.93

Removed the GIN index for run metadata to improve performance.

**2025-07-16**

## v0.2.92

Enabled copying functionality for blobs and checkpoints, improving data management flexibility.

**2025-07-16**

## v0.2.91

Reduced writes to the `checkpoint_blobs` table by inlining small values (null, numeric, str, etc.). This means we don't need to store extra values for channels that haven't been updated.

**2025-07-16**

## v0.2.90

Improve checkpoint writes via node-local background queueing.

**2025-07-15**

## v0.2.89

Decoupled checkpoint writing from thread/run state by removing foreign keys and updated logger to prevent timeout-related failures.

**2025-07-14**

## v0.2.88

Removed the foreign key constraint for `thread` in the `run` table to simplify database schema.

**2025-07-14**

## v0.2.87

Added more detailed logs for Redis worker signaling to improve debugging.

**2025-07-11**

## v0.2.86

Honored tool descriptions in the `/mcp` endpoint to align with expected functionality.

**2025-07-10**

## v0.2.85

Added support for the `on_disconnect` field to `runs/wait` and included disconnect logs for better debugging.

**2025-07-09**

## v0.2.84

Removed unnecessary status updates to streamline thread handling and updated version to 0.2.84.

**2025-07-09**

## v0.2.83

* Reduced the default time-to-live for resumable streams to 2 minutes.
* Enhanced data submission logic to send data to both Beacon and LangSmith instance based on license configuration.
* Enabled submission of self-hosted data to a LangSmith instance when the endpoint is configured.

**2025-07-03**

## v0.2.82

Addressed a race condition in background runs by implementing a lock using join, ensuring reliable execution across CTEs.

**2025-07-03**

## v0.2.81

Optimized run streams by reducing initial wait time to improve responsiveness for older or non-existent runs.

**2025-07-03**

## v0.2.80

Corrected parameter passing in the `logger.ainfo()` API call to resolve a TypeError.

**2025-07-02**

## v0.2.79

* Fixed a JsonDecodeError in checkpointing with remote graph by correcting JSON serialization to handle trailing slashes properly.
* Introduced a configuration flag to disable webhooks globally across all routes.

**2025-07-02**

## v0.2.78

* Added timeout retries to webhook calls to improve reliability.
* Added HTTP request metrics, including a request count and latency histogram, for enhanced monitoring capabilities.

**2025-07-02**

## v0.2.77

* Added HTTP metrics to improve performance monitoring.
* Changed the Redis cache delimiter to reduce conflicts with subgraph message names and updated caching behavior.

**2025-07-01**

## v0.2.76

Updated Redis cache delimiter to prevent conflicts with subgraph messages.

**2025-06-30**

## v0.2.74

Scheduled webhooks in an isolated loop to ensure thread-safe operations and prevent errors with PYTHONASYNCIODEBUG=1.

**2025-06-27**

## v0.2.73

* Fixed an infinite frame loop issue and removed the dict\_parser due to structlog's unexpected behavior.
* Throw a 409 error on deadlock occurrence during run cancellations to handle lock conflicts gracefully.

**2025-06-27**

## v0.2.72

* Ensured compatibility with future langgraph versions.
* Implemented a 409 response status to handle deadlock issues during cancellation.

**2025-06-26**

## v0.2.71

Improved logging for better clarity and detail regarding log types.

**2025-06-26**

## v0.2.70

Improved error handling to better distinguish and log TimeoutErrors caused by users from internal run timeouts.

**2025-06-26**

## v0.2.69

Added sorting and pagination to the crons API and updated schema definitions for improved accuracy.

**2025-06-26**

## v0.2.66

Fixed a 404 error when creating multiple runs with the same thread\_id using `on_not_exist="create"`.

**2025-06-25**

## v0.2.65

* Ensured that only fields from `assistant_versions` are returned when necessary.
* Ensured consistent data types for in-memory and PostgreSQL users, improving internal authentication handling.

**2025-06-24**

## v0.2.64

Added descriptions to version entries for better clarity.

**2025-06-23**

## v0.2.62

* Improved user handling for custom authentication in the JS Studio.
* Added Prometheus-format run statistics to the metrics endpoint for better monitoring.
* Added run statistics in Prometheus format to the metrics endpoint.

**2025-06-20**

## v0.2.61

Set a maximum idle time for Redis connections to prevent unnecessary open connections.

**2025-06-20**

## v0.2.60

* Enhanced error logging to include traceback details for dictionary operations.
* Added a `/metrics` endpoint to expose queue worker metrics for monitoring.

**2025-06-18**

## v0.2.57

* Removed CancelledError from retriable exceptions to allow local interrupts while maintaining retriability for workers.
* Introduced middleware to gracefully shut down the server after completing in-flight requests upon receiving a SIGINT.
* Reduced metadata stored in checkpoint to only include necessary information.
* Improved error handling in join runs to return error details when present.

**2025-06-17**

## v0.2.56

Improved application stability by adding a handler for SIGTERM signals.

**2025-06-17**

## v0.2.55

* Improved the handling of cancellations in the queue entrypoint.
* Improved cancellation handling in the queue entry point.

**2025-06-16**

## v0.2.54

* Enhanced error message for LuaLock timeout during license validation.
* Fixed the \$contains filter in custom auth by requiring an explicit ::text cast and updated tests accordingly.
* Ensured project and tenant IDs are formatted as UUIDs for consistency.

**2025-06-13**

## v0.2.53

* Resolved a timing issue to ensure the queue starts only after the graph is registered.
* Improved performance by setting thread and run status in a single query and enhanced error handling during checkpoint writes.
* Reduced the default background grace period to 3 minutes.

**2025-06-12**

## v0.2.52

* Now logging expected graphs when one is omitted to improve traceability.
* Implemented a time-to-live (TTL) feature for resumable streams.
* Improved query efficiency and consistency by adding a unique index and optimizing row locking.

**2025-06-12**

## v0.2.51

* Handled `CancelledError` by marking tasks as ready to retry, improving error management in worker processes.
* Added LG API version and request ID to metadata and logs for better tracking.
* Added LG API version and request ID to metadata and logs to improve traceability.
* Improved database performance by creating indexes concurrently.
* Ensured postgres write is committed only after the Redis running marker is set to prevent race conditions.
* Enhanced query efficiency and reliability by adding a unique index on thread\_id/running, optimizing row locks, and ensuring deterministic run selection.
* Resolved a race condition by ensuring Postgres updates only occur after the Redis running marker is set.

**2025-06-07**

## v0.2.46

Introduced a new connection for each operation while preserving transaction characteristics in Threads state `update()` and `bulk()` commands.

**2025-06-05**

## v0.2.45

* Enhanced streaming feature by incorporating tracing contexts.
* Removed an unnecessary query from the Crons.search function.
* Resolved connection reuse issue when scheduling next run for multiple cron jobs.
* Removed an unnecessary query in the Crons.search function to improve efficiency.
* Resolved an issue with scheduling the next cron run by improving connection reuse.

**2025-06-04**

## v0.2.44

* Enhanced the worker logic to exit the pipeline before continuing when the Redis message limit is reached.
* Introduced a ceiling for Redis message size with an option to skip messages larger than 128 MB for improved performance.
* Ensured the pipeline always closes properly to prevent resource leaks.

**2025-06-04**

## v0.2.43

* Improved performance by omitting logs in metadata calls and ensuring output schema compliance in value streaming.
* Ensured the connection is properly closed after use.
* Aligned output format to strictly adhere to the specified schema.
* Stopped sending internal logs in metadata requests to improve privacy.

**2025-06-04**

## v0.2.42

* Added timestamps to track the start and end of a request's run.
* Added tracer information to the configuration settings.
* Added support for streaming with tracing contexts.

**2025-06-03**

## v0.2.41

Added locking mechanism to prevent errors in pipelined executions.
